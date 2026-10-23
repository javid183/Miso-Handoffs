# Report: Lucy's role follow-up hits the wrong enemy (fix)

Plan: plans/2026-10-23-lucy-role-target-fix.md (decision D-152; investigation reports/lucy-role-wrong-target.md)    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (code, tests, compile, EditMode). THJ's play check is still needed.

## What changed

F1, core `GUnit` (ordered attacker memory):
- `Core/Units/Runtime/RecentAttackerMemory.cs` (new, 59 lines): plain generic class. `Record(attacker, capacity)` removes the attacker if it is already there (reference equality), appends it, and drops the oldest while the memory is over capacity. `MostRecent` gives the newest or null. `AgeOf(x)` gives 0 for the newest and -1 when x is absent. It uses a private per-instance lock and no Unity-object APIs.
- `Core/Units/Runtime/GUnit.cs` (+6/-10): the `HashSet<GUnit> _recentAttacksMemory` field becomes `readonly RecentAttackerMemory<GUnit>`. `RecordGettingTargeted` calls `Record(attacker, GlobalSettingsSO.Instance.unitsAttackMemorySize)`. `GetRecentAttackFactor` uses `AgeOf` (the same formula, `fade^age`). `GetMostRecentAttacker` returns `MostRecent`. The public API is unchanged.
- `Core/Units/Editor/RecentAttackerMemoryTests.cs` (new, 133 lines, 10 tests). New folder `Core/Units/Editor/`.

F2, Lucy (candidate ranking):
- `Features/Player/Lucy/Scripts/LucyRoleTargetRanking.cs` (new, 67 lines): a pure static ranking (`Candidate<T>`, `Pick`, `FallbackRadius`).
- `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (+100/-15): `PrepareTargets` builds the candidates (existing filters kept) and calls the ranking. A new private `MeasureActionArea` (plus `PushAll` and `ShapeReach`) works out the triggering action's own area and whether it knocks units back. It adds `using ...AbilitySystem.Effects`.
- `Features/Player/Lucy/Scripts/Editor/LucyRoleTargetRankingTests.cs` (new, 143 lines, 15 tests). New folder `Features/Player/Lucy/Scripts/Editor/`.

The `.meta` files Unity generated go with each new file and folder. Line endings: everything is LF, like its neighbours. The Core files have a BOM (as `GUnit.cs` does); the Lucy files have none (as their folder does). No statics were added; the test class uses a `const`.

## The ranking as built

The filters are unchanged, applied in `PrepareTargets` across every hostile faction in list order: not downed, a footprint cell inside Lucy's zone (`GetCellsInRange`, untouched), and `GetMostRecentAttacker() != Lucy`. For each enemy that passes:
- **Direct target**: named in the last action's targets (bundles flattened as before), or standing on one of its target cells.
- **Hit by the acting unit**: the action's owner exists and `GetMostRecentAttacker() == owner`. With F1 this is now really the last unit that hit it.
- **Distance**: 0 when named; otherwise the minimum footprint distance to the action's target cells, measured in Lucy's role traverse mode (Adjacent, as before); `int.MaxValue` when there is no target cell.

`Pick` then works in three steps:
1. The direct target nearest the target cell; on a tie, the earlier one in list order.
2. Only when there is no direct target, and the action is not a Move and has an owner: the nearest enemy "hit by the acting unit" within `fallbackRadius`, with the same tie rule.
3. Otherwise nobody, and the role doesn't fire.

`fallbackRadius = max(areaReach, 1) + (knocksBack ? 1 : 0)`. `areaReach` is the largest radius of a Surrounding `AEffectCompound` in the triggering action's effect tree. When the compound uses an area shape, it is the shape's farthest cell (every level, plus the footprint) instead. The walk goes through compound children, `AEffectSpawner.NestedCompound`, `AEffectDashAttack` (transporter and attack), and `AEffectTransporter`/`AEffectCommand` on-tile and end-tile compounds. These are the public accessors the targeting preview uses, so no core file was changed. `knocksBack` is true when the tree contains an `AEffectPusher`.

Values from the current assets:
- Linda Bow Attack: no Surrounding area, so radius 1.
- Linda Explosive Arrow ("Explosive Crescendo"): the shape is a plus of reach 1, so radius 1.
- Mark Vault: the end-tile compound is Surrounding radius 1 and pushes one cell, so radius 2.
- Mark Assault Blitz: its target is the enemy unit itself, so it is a direct target.

## AI-thread check

The AI worker thread does read this memory. `UtilityVariable.TargetRecentAttackFactor` (`Core/Systems/AISystem/UtilityScore/UtilityVariables.cs:162`) calls `GUnit.GetRecentAttackFactor`, which the scorer evaluates on the worker. The main thread writes the memory in `RecordGettingTargeted`, via `AEffectBase.Apply` and `AEffectVortexPull`. The old `HashSet` had no protection at all. The new memory locks every read and write on a private per-instance object, compares by reference only, and touches no Unity API. `GetRecentAttackFactor` still reads `GlobalSettingsSO.Instance.unitsAttackMemoryFadeFactor`, which is a plain field read and not new. `RememberAttack` and the memorable-attacks memory are a separate list, not touched. The blackboard doesn't read the recent-attacker memory. The other readers are `BarkManager.cs:164` and Lucy, both on the main thread.

Side effect on AI scoring: `TargetRecentAttackFactor` now really ranks by recency. Before, a re-hit didn't move the attacker, so its factor could be stale. This is a scoring change for graphs that use the variable. The AI regression report still shows 38/709 failures, the same count as after the Dark Shaman heal work (`shaman-heal-c1.md`), and all of them are asset or graph-level checks.

## How Mark's trigger still works

`fc4a7dad0` added the fallback because Mark's Vault targets a **cell** (the landing cell). Its end-tile compound hits the **adjacent** cells and pushes the victims one cell further, so no victim is on the target cell. It also changed `AEffectBase` to tag bundle and cell victims with the attacker. In the new code, Vault's victims are "hit by Mark" (F1 makes that reliable) and sit at distance 1 to 2 from the landing cell. The fallback radius for Vault is 2 (area 1 + knockback 1), which equals the original `Radial <= 2` from `fc4a7dad0`, so they qualify. Assault Blitz targets the enemy (`targetType` occupant), so it is a direct target. Mark's Command moves an ally and hits no enemy; the commanded ally's own attack is a separate action with that ally as owner, ranked normally. When Lucy herself is commanded, the trigger excludes her as before.

The radius-4 case from `4f27914d0` is the zone check in `GetCellsInRange` (`<=` and Lucy's traverse mode). That code is untouched, so an enemy at the zone's edge is still a candidate. That commit also widened the fallback from 2 to Lucy's role radius (3). This fix deliberately narrows that back to the action's own area, as the plan asks.

## Acceptance criteria

- [x] Bow shot or Explosive Arrow on B, with C (Linda-tagged or splashed) next to B and earlier in turn order: Lucy hits B. Tests: `Pick_SplashedNeighbourEarlierInList_TargetedEnemyWins`, `Pick_TargetedEnemyNotLastHitByActingUnit_StillWins`. Play check needed.
- [x] Linda shoots C, then B: Lucy hits B. Test: `Pick_ShotCThenB_BWins`. Play check needed.
- [x] Lucy already followed up on B and Linda hits B again: Lucy hits B. B's newest attacker becomes Linda again, so the `!= Lucy` filter passes. Tests: `Record_HitByLucyThenByLindaAgain_LindaIsNewest`, `Record_AttackerAlreadyRemembered_MovesToNewest`. Play check needed.
- [x] Targeted unit can't be hit: nearest qualifying enemy within the action's own area, or nothing. Tests: `Pick_NoTargetedEnemy_NearestHitEnemyWithinRadiusWins`, `..._HitEnemyOutsideRadius_None`, `..._NearbyEnemyNotHitByActingUnit_None`, `Pick_FallbackNotAllowed_None`, `FallbackRadius_*`. Play check needed.
- [x] Mark still triggers Lucy, and the radius-4 case still fires: reasoning above, plus test `Pick_VaultLandingKnocksEnemyBack_EnemyTwoCellsOutStillPicked`. **Play check needed** (Vault in particular).
- [x] `GetMostRecentAttacker()` returns the newest attacker, also when it attacked before, sized by `unitsAttackMemorySize`. Tests: the 10 `RecentAttackerMemoryTests` (size 2, size 1, size 0, re-add, eviction, empty, null).
- [x] Barks using the instigator (`BarkManager.cs:164`) still work: same call and return type, and the result is now actually the newest. Not play-checked.
- [x] Compile clean and EditMode green except the known red. Forced refresh and recompile through the Unity MCP: no errors, only pre-existing warnings. Full EditMode run: 650 total, 649 passed, 1 failed, the known red `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (38/709 checks, same as before; not re-baselined). The 25 new tests are compiled into `Assembly-CSharp-Editor` and were part of that run. A filtered re-run of just the two new classes was refused afterwards because the editor had entered Play mode (not started by me). I did not stop it.

## Save reset

No.

## Decisions I made

- **The fallback radius adds 1 when the action knocks units back.** The plan said "the triggering ability's own area/radius, fallback 1". Without the +1, Mark's Vault victims, pushed to distance 2, would no longer trigger Lucy, which breaks the Mark criterion. With it, Vault gets 2, matching the original value from `fc4a7dad0`. Linda's attacks stay at 1. This is a small numeric deviation that serves the plan's own acceptance criterion; flagged for the coordinator.
- **"The action's own area" is not `RuntimeAbility.Parameters.radius`.** That field is the cast range (5+ for Linda's bow, from `Stat_RANGE`). Using it would have been as loose as the old bug. I measured the area from the effect tree instead, as described above.
- **"Hit by the triggering action" uses `GetMostRecentAttacker() == acting unit`** (the existing proxy, now reliable with F1). The alternative was listening to `onAbilityEffectPerformedOn` or reading `CombatLevelRunHandler._affectedAbilityEffectPerforms`, which is private core code outside the plan.
- **The direct-target tie-break uses the distance to the nearest target cell** (0 for an enemy named in the targets), then list order. Ranking candidates over every hostile faction keeps the faction-order tie-break that `FirstMatchAcrossGroups` gave. Lucy no longer calls `FirstMatchAcrossGroups`; it and its tests stay.
- **The ranking is generic and lives in Lucy's feature folder** (namespace `MISO.Core.Features.Bergsons`), not in core `FactionRoleRules`, to keep the core surface unchanged.

## Needs THJ

None beyond the play check. The coordinator should confirm the knockback +1 (first decision above).

## Docs to update

- `tech/core-systems.md` or `tech/combat-architecture.md`, if they describe `GUnit` attacker memory: it is now ordered (move-to-newest, evict-oldest), with a lock for the AI worker.
- `build-log.md`: this step.

## Risks and loose ends

- **AI scoring:** `TargetRecentAttackFactor` now reflects true recency. Graphs that use it may score differently in play (a fix, but a behaviour change). The regression failure count is unchanged.
- **Push distance assumed 1:** `AEffectPusher.distance` is private, so a knockback of 2+ cells in a future ability would fall outside the fallback. That only matters when the direct target can't be taken.
- **Stale "hit by":** an enemy whose last attacker is the acting unit from an *earlier* turn, standing within the tight radius, can still be a fallback pick. This is much narrower than before (radius 1 to 2 instead of 3, and only when no direct target qualifies).
- **`AEffectVortexPull` and area shapes on the preset itself** (preset-level Surrounding) are not walked. Preset-level Surrounding targets cells around the owner, which are already direct targets.
- The investigation's secondary suspect (`LastActions[0]` is the oldest completed entry) is not addressed; it is out of scope.
- The editor was in Play mode at the end of my run (not started by me); a filtered re-run of the new tests could not start.

## Proposed commits

1. `fix(units): remember attackers in order so the most recent attacker is the newest` (**core**):
   - `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs`
   - `miso/Assets/_Project/Core/Units/Runtime/RecentAttackerMemory.cs` and `.meta`
   - `miso/Assets/_Project/Core/Units/Editor.meta`
   - `miso/Assets/_Project/Core/Units/Editor/RecentAttackerMemoryTests.cs` and `.meta`

   Lines: GUnit +6/-10, new 59 + 133.
2. `fix(lucy): the Family Role follow-up hits the enemy the ally actually targeted` (plain; builds on 1):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyRoleTargetRanking.cs` and `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/LucyRoleTargetRankingTests.cs` and `.meta`

   Lines: handler +100/-15, new 67 + 143.

Leave out the uncommitted Dark Shaman heal files (`Core/FX/...`, `FutureTargets*`), `Packages/` and `ProjectSettings/`.

## Other branches

All branches, per the plan (built on `thj/quick-wins`).

## How to see it

1. Open a combat level with Linda, Lucy and Mark. Recompile (Ctrl+R).
2. **Repro A (splash):** put two enemies B and C in vertically adjacent cells inside Lucy's zone, with C earlier in the enemy turn order (C above B). Fire Linda's Explosive Arrow at B's cell so the splash hits C. Press Lucy's QTE: she should hit **B**. Then fire Linda's Bow at C, then at B, and press the QTE after the second shot: she should hit **B**.
3. **Repro B (repeat target):** after Lucy has followed up on B once, have Linda hit B again. Lucy's QTE should come up and she should hit **B**, not a neighbour, and she shouldn't be skipped.
4. **Mark triggers Lucy:** Mark's Vault landing next to an enemy inside Lucy's zone, the enemy pushed one cell: Lucy's QTE comes up and she hits that enemy. Assault Blitz on an enemy in her zone: she hits that enemy.
5. **Out-of-zone target:** Linda shoots an enemy outside Lucy's zone. Another enemy that the same shot did not hit, two or more cells away but inside Lucy's zone, should **not** draw Lucy (no QTE). If the shot splashed an enemy inside her zone (Explosive Arrow), Lucy takes that one.
6. **Zone edge (radius-4 case):** Linda hits an enemy standing on the outer ring of Lucy's zone outline: Lucy still triggers.
7. Optional: an enemy's damage bark after a hit should still name the unit that hit it last.
