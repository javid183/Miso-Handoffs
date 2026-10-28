# Report: Linda at a distance, D1-C1: config, Far state and the Watch factor

Plan: plans/2026-10-28-linda-distance-d1-tech.md (chunk D1-C1)    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 19e02893a)
Outcome: done (compiled offline against the editor's own compiler inputs; the Unity Test Runner and the play check are still to be done by THJ)

No core-system code was changed. Watch's factor and the hover damage preview both work without core code, so there is no Tier 3 question.

## The damage chain I found

| Step | Watch (role) | Bow |
| --- | --- | --- |
| Ability preset | `Linda_Ability_FactionRole` (effects: `_Effect_Spawn` only) | `Linda_Ability_PrimaryAttack` (effects: `PrimaryAttackM_Effect_Spawn`) |
| Spawn effect | `Linda_Ability_FactionRole_Effect_Spawn` → `LindaAttackArrow` | `Linda_Ability_PrimaryAttackM_Effect_Spawn` → `LindaAttackArrow` (same prefab, same component fileID) |
| Arrow's damage | `LindaAttackArrow.Projectile.effect` = `Linda_Ability_PrimaryAttackM_Effect_Compound` → `PrimaryAttackM_Effect_AttrMod`: `Specs_Health`, Subtractive, StatBacked **6 × Stat_DMG** (cap 1 × `StatUB_DMG` = 9999), crit extra mod ×1.5 | same |
| Stat context | `AEffectSpawner` passes the role's `RuntimeAbility` into `Projectile.Initialize`; `SpawnableEntity.Activate` applies the effect with it | the bow's `RuntimeAbility` |

So the 6× lives only in the bow's AttrMod, shared by both. `Linda_Ability_FactionRole_Effect_Compound` and `_Effect_AttrMod` (baseFactor **7**) are referenced by nothing: dead data, untouched.

How `6 × Stat_DMG` evaluates (`StatResolver.Resolve`): it folds the sources Faction → Equipment → Unit → **Ability** in that order, and the role preset's own `statAttributes` has a `Stat_DMG` entry, policy Multiplicative, factor 1. Each `RuntimeAbility` gets its own copy of that set (`preset.StatAttributes.Copy()` + `PrepareRuntime`, so a new `RuntimeStatAttribute` per ability instance). The Ability factor therefore multiplies the whole result, and only for arrows fired by that one ability.

**Mechanism chosen: option (c).** `LindaFarState` keeps the runtime `BaseValue` of the role ability's own `Stat_DMG` at `authored (1) × factor ÷ offFactor (6)`: 5/6 near, 1.25 Far, exactly 1 with Far Watch off. It uses the public `RuntimeStatAttribute.SetValue`. Why this route:
- **Watch only.** The bow, Explosive Crescendo, Harmonic Slam and the Duo arrows evaluate against their own abilities, so they can't change.
- **The preview matches without core code.** `AbilityDamagePreview.ComputeFor` passes the same `RuntimeAbility` as the stat context to `SimulateApply`, so the preview reads the same multiplier (the Watch target-selection preview in `PlayerController.ShowDamagePreview`, and any other caller).
- **Everything else keeps working.** Pierce falloff (`onHitExtraModifier`, applied after), crits and Revenge (a unit-stat modifier) multiply on top as today.
- **Nothing persists.** Only the runtime value changes, never the shared serialized entries, the preset or any save data (the stat set saves upgrade levels only).

Options (a) and (b) were not needed: (a) would need a new AttrMod plus a per-arrow hook, and `OnHitExtraModifier` is a read-only serialized field already used for the falloff; (b) would need a new prefab plus the same Far hook.

## What changed

- `Features/Player/Linda/Scripts/Quiver/LindaDistanceTuning.cs` (+ .meta): new ScriptableObject. Four toggles (Far Watch, Encore cooldown, fetch cues, distance log); near 5 / Far 7.5 / off 6; radius 2; call-out distance 4; Encore cooldown on 3 / off 2. `WatchFactor(far)` and `WatchDamageScale(far)`. C3 to C5 read the other fields; nothing reads them yet.
- `Features/Player/Linda/Data.meta`, `Data/LindaDistanceTuning.asset` (+ .meta): new folder and the one asset instance, all toggles on.
- `Features/Player/Linda/Scripts/Quiver/FarWatchRules.cs` (+ .meta): pure static. Footprint rectangles, who counts, radial footprint distance, `Evaluate` (Far, nearest index, nearest distance), the factor table and the damage scale.
- `Features/Player/Linda/Scripts/Quiver/FarWatchLock.cs` (+ .meta): pure state machine (level start near / live on her side's turn / locked from her side's End Turn until its next turn) and the `FarSource` enum.
- `Features/Player/Linda/Scripts/Quiver/LindaFarState.cs` (+ .meta): component on Linda, added at run time by `LindaQuiver.Start` beside the other quiver components (nothing is created as its own root).
  - Listens to `levelStarted`, `turnStarted`, `turnEnded`, `onFamilyRolePrompt` and `onFamilyRoleActivated`, and refreshes every frame so the preview follows the squad live.
  - Exposes `IsFar`, `Source`, `IsLocked`, `WatchFactor`, `NearestUnit`, `NearestDistance`, `EvaluateLive()`, `EvaluateAt(origin)` (for the C2 ghost-tile mark) and an `OnLocked` event (for the C5 End Turn line). No statics.
- `Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`: serialized `distanceTuning` + `DistanceTuning`; adds `LindaFarState` in `Start`.
- `Features/Player/Linda/Scripts/Quiver/QuiverLevelAccess.cs`: `SquadControllerOf(GUnit)`, the player's controller when the unit is in the player's faction (null-safe, no `CombatLevel.PlayerFaction`).
- `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: one YAML line, `distanceTuning` on the `LindaQuiver` component.
- `Features/Player/Linda/Scripts/Quiver/Editor/FarWatchRulesTests.cs` (+ .meta): 29 cases.
- `Features/Player/Linda/Scripts/Quiver/Editor/FarWatchLockTests.cs` (+ .meta): 9 tests (12 after the review tweaks).
- `Features/Player/Linda/Scripts/Quiver/Editor/FarWatchWiringTests.cs` (+ .meta): 13 cases on the data.

All new files are LF with no BOM, like their neighbours. Paths are under `miso/Assets/_Project/`.

## Who counts, and what it filters on

`LindaFarState` reads the player controller's `AllUnits` (`PhaseData.OwnedUnits`, `GUnit`s only). A unit counts when it is on the grid, isn't Linda, is in Linda's faction, `IsAlive && !IsDowned`, and isn't spawned. The filters, with evidence:
- **Decoys (Blink and Hide and Seek).**
  - Both spawners (`Lucy_Ability_Teleport_DecoySpawner`, `John_Lucy_Duo_LUCY_Ability_DecoySpawner`) spawn `Lucy_Decoy_ValidVariant`, a `GUnit` of the Bergsons faction.
  - It carries `Status.Inactive` (2 turns) and `EntityState.IgnoreObjective` (permanent).
  - `PlayerController.prefab`'s `objectivesIgnoreTagsQuery` matches `EntityState.IgnoreObjective`, so the filter is the public `FactionControllerBase.IsUnitIgnoredForObjectives(unit)`, the same check objectives use.
  - Also excluded as spawned: any unit with a `BoundSpawner` (opt-in summon link). No player unit uses it today.
- **The Cyclone:** `Features/Player/Lucy/Prefabs/Cyclone.prefab`, an `OnGridEntity` (its class identifier still says `CollectibleEntity`). Not a `GUnit`, so never in the unit list.
- **Toba's wall:** `Toba_Wall.prefab`, a `HazardEntity`. Not a `GUnit`.
- **Other factions' allies (`Unit_Toba_Ally`):** only the player controller's own units are read, and the rule also checks the faction.
- **Dead, downed or removed units:** `IsAlive`, `IsDowned` (the bark system treats downed as fallen) and `CurrentCell`.
- **Toba in the squad:** counts as a Bergson.

## Lock timing (bus order, read-only check of `CombatLevelRunHandler.SwitchTurnIE`)

1. `SwitchTurnIE` waits while any controller `isActionInProgress`, a sequence is playing, `LevelSpecificBehaviour.InProgress`, or a turn-switch hold is registered.
2. Then `EndTick()` → `EndTurn()` → `turnEnded(player)`.
3. Then `WaitForSeconds(timeBetweenFactionTurns)`, the next controller's `TurnStartPause`, `PlayPhaseAnimation` and `StartTurn()` → `turnStarted(next)`.

So the lock at `turnEnded` of Linda's faction comes after the last player action and before any enemy acts. At level start, `levelStarted` is invoked right before the first `StartTurn()` (lines 194–197), and `LindaFarState` resets to near then. An ally faction's turn between the player and the enemy keeps the lock.

## Acceptance criteria (C1's share: the Far items without visuals)

- [x] **Toggle off: Watch hits 6×.** The scale is exactly 1 and `BaseValue` = authored. `FarWatchWiringTests.WatchDamage_Off_IsTodaysSix` checks arrow 6 × authored 1 × scale 1 = 6. In play: THJ.
- [x] **5× when a counted unit is within 2 (radial, footprint) at End Turn, 7.5× when none.** The rule is covered by `FarWatchRulesTests`; the data chain is covered by `FarWatchWiringTests.WatchDamage_On_*` (5 and 7.5). In play: THJ.
- [x] **Locked through the enemy phase.** `FarWatchLockTests` (holds through enemy and ally turns, unlocks at the player's next turn, near at level start, near when enemies act first). In play: THJ (an enemy push next to her doesn't change the hit).
- [x] **Live on a player-phase Watch.** `FarWatchLockTests.OwnTurn_IsLive`. In play: THJ (Mark Commands an enemy into her lane).
- [x] **Only Watch changes.** By construction: only the role `RuntimeAbility`'s own stat set is written. `WatchAndBow_FireTheSameArrow` documents the shared arrow. In play: THJ checks a bow hit stays 6×.
- [x] **Who counts: Toba near; a decoy, the Cyclone, the wall, other factions and dead units don't count.** The rule is covered by `FarWatchRulesTests`; the data by `Decoys_AreIgnoredByThePlayerControllersObjectiveQuery` and `CycloneAndWall_AreNotUnits`. In play: THJ.
- [x] **The hover damage preview matches the hit.** It shares the stat context (see above). In play: THJ.
- [x] **EditMode tests for the Far rule, the factor table and the lock.**
- [ ] **Run in Unity.** Not done by me: the editor is open, so no batch run. I compiled `Assembly-CSharp` and `Assembly-CSharp-Editor` offline: the editor's own Roslyn, its `.rsp` files from `Library/Bee` plus my new files, output to the scratchpad. Both have 0 errors and no warnings in my files. I also ran the real `FarWatchRulesTests` and `FarWatchLockTests` code outside Unity with Unity's NUnit and CoreModule: 38 of 38 cases pass. `FarWatchWiringTests` needs the AssetDatabase, so THJ's Test Runner has to run it.

**Tests for THJ** (Test Runner > EditMode): Run All. The only accepted red is `AIRegressionTest.Baseline_MatchesCurrentAI`. For a quick check, filter on `MISO.Core.Features.Bergsons.EditorTests` (`FarWatchRulesTests`, `FarWatchLockTests`, `FarWatchWiringTests`, plus the existing `QuiverWiringTests`).

**AIRegressionTest:** the known-red message should not move. No ability preset, effect, utility graph or unit ability list changed. Its unit catalog lists ability names only, and `Unit_Linda`'s change is one `LindaQuiver` field. The AI never reads role abilities (no `FactionRole` reference under `AISystem/Runtime`). Please confirm the message reads as before.

## Save reset

No.

## Decisions I made

- **The Watch factor goes on the role ability's own runtime `Stat_DMG` multiplier** (option (c) above). The arrow, the presets and the prefabs stay as they are. With the toggle off the factor is exactly today's.
- **The off factor (6) is the divisor.** A wiring test asserts that it equals the arrow AttrMod's `baseFactor`, so drift is caught. The tuning's factors are therefore absolute (5 / 7.5 times Stat_DMG). In exact terms, Watch deals factor ÷ 6 of the bow's full damage, equipment's flat bonus included.
- **Live state is evaluated every frame during the player phase, and again on the role's prompt and activation.** The value at the hit equals the value at the trigger, because family positions don't change between the trigger and the arrow landing.
- **"Downed" counts as not living,** matching how the rest of the code treats fallen units.
- **The asset lives in a new `Features/Player/Linda/Data/` folder,** not under Resources (the plan says it is not loaded from Resources).
- **All four toggles are on in the asset** (the test configuration). The three not built yet do nothing until C3 to C5.
- **"Her side" is Linda's own faction,** read from the bus's faction argument. The squad comes from `QuiverLevelAccess.SquadControllerOf`, so Linda outside the player's faction is never Far.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` (coordinator): Far Watch scales Watch through its ability's own Stat_DMG multiplier, written by `LindaFarState`; the role's own Compound/AttrMod (7×) is unused.
- GDD Linda LI-15 and glossary "Far": per the plan, after the play check.

## Risks and loose ends

- **Shared stat entries.** `AbilityDamagePreview.CopySharedStatFactors` (core) writes `CurrentLevel.factor` into Duo partner abilities' stat entries, and those entries are shared with the preset asset because `StatAttributeSet.Copy()` shares `attributeEntries`. It isn't the role ability and I didn't touch it, but it is a latent asset-mutation bug in the preview: it persists across Play sessions with domain reload off. Not in scope; flagging for the backlog.
- **Float precision.** 5/6 isn't exact in float, so 6 × 5/6 × DMG can land a hair off. Damage rounds to nearest (`NormalizeValueChange`), so it only matters on an exact .5, and the preview does the same arithmetic, so preview and hit still agree.
- **Per-frame cost.** During the player phase, each frame reads about 5 units (tag match, footprint). Small, but it allocates; C2 can share the evaluation for the mark.
- **`LindaFarState` never puts the authored value back if it is disabled while Linda lives.** No current path disables it.
- **Dead data.** The role's unused `Linda_Ability_FactionRole_Effect_Compound` / `_Effect_AttrMod` (7×) could mislead someone tuning Watch.
- **Import order.** The editor hasn't imported the new files yet. On focus, Unity compiles and then imports the asset with my hand-written metas (GUIDs checked unique in the project).

## Proposed commits

Superseded by the list in "Review tweaks" below.

1. `feat(linda): Far Watch scales Watch damage by distance from the family at End Turn`. Files:
   - `LindaDistanceTuning.cs`, `FarWatchRules.cs`, `FarWatchLock.cs` and `LindaFarState.cs`, each with its .meta;
   - `LindaQuiver.cs`, `QuiverLevelAccess.cs`;
   - `Data.meta`, `Data/LindaDistanceTuning.asset` and its .meta;
   - `Prefabs/Unit_Linda.prefab`;
   - `Editor/FarWatchRulesTests.cs`, `Editor/FarWatchLockTests.cs` and `Editor/FarWatchWiringTests.cs`, each with its .meta.

   Kind: risky (changes Watch's damage in play).

   One commit, because `LindaQuiver.cs` carries both the tuning field and the component hook, and the asset, the prefab line and the component only work together. Per the plan, the play check comes after C1 + C2, so it should be committed after that play.

## Other branches

`main` and `thj/home-test` get this when the quiver goes there.

## How to see it

No Far visuals yet (that is C2), so read damage numbers and the combat log. Let X be today's bow hit on a given enemy without a crit. Expected: Watch near = 5/6 X, Watch Far = 1.25 X, toggle off = X. Ignore crit hits (×1.5).

1. Focus the editor so it compiles, then run the EditMode tests (above).
2. Select `Assets/_Project/Features/Player/Linda/Data/LindaDistanceTuning.asset`: four toggles on, 5 / 7.5 / 6, radius 2. Select `Unit_Linda.prefab` > `LindaQuiver` > Distance test: the asset is assigned.
3. Play a level with Linda and John (M4, for example). Shoot an enemy with the bow and note the damage (X).
4. **Near, locked:** end the turn with John 2 cells from Linda (diagonals count as 1). When an enemy walks into her lane in the enemy phase, accept Watch. The hit should be about 5/6 X, and a second pierced enemy about 0.6 of that.
5. **Far, locked:** end the turn with nobody within 2 of Linda. Watch in the enemy phase should hit about 1.25 X. If an enemy pushes or pulls Mark next to her in that enemy phase, later Watch hits stay 1.25 X.
6. **Who counts:**
   - Toba in the squad within 2 at End Turn: near.
   - A Lucy decoy (Blink) within 2 and no Bergson within 2: still Far.
   - A downed or dead Bergson within 2: still Far.
7. **Live in the player phase:** with nobody within 2, have Mark Command an enemy into her lane on your turn. Watch hits about 1.25 X. Move John next to her and repeat: about 5/6 X.
8. **Preview:** if a damage preview shows on the target's health bar for a Watch, it equals the hit.
9. **Only Watch:** the bow, Explosive Crescendo and the arrow Duos hit as in step 3 whatever her distance.
10. **Toggle off:** untick Far Watch on the asset, even in Play. Watch hits X in every case.
11. The combat log's damage lines show each hit's value. The Far and factor lines come in C5.

## Review tweaks (after APPROVE, same day)

1. **Effective upgrade level.** `LindaFarState.ApplyWatchDamage` now reads the authored multiplier the way the stat set itself does: `entry.upgradeLevels[set.GetEffectiveUpgradeLevel(entry.Attribute)].factor`, where it used `CurrentLevel.factor`. A run bonus on Watch's `Stat_DMG` is kept.
2. **Turn 1 hardening.**
   - `FarWatchLock` now records whether any turn event was seen since the level started (`TurnSeen`). It has a new `AssumeOwnTurnIfActing(bool)`: with no turn event seen and her side acting, the phase becomes "her side's turn, live".
   - `LindaFarState.RefreshNow` calls it on every refresh until a turn event is seen.
   - "Her side is acting" comes from the new `QuiverLevelAccess.IsSquadTurn(unit)`: the level isn't ended and `CombatLevelRunHandler.Instance.CurrentFactionControllerOrNull` is the squad's controller. That getter is public and read-only, and the quiver's "+N arrows" preview already reads it. No core change.
   - Before the first turn, the run handler's current controller is the first side to act. So if enemies open the level, Linda still counts as near, as before.
   - Three new tests in `FarWatchLockTests`:
     - `MissedFirstTurnStart_OwnSideActing_IsLive`;
     - `MissedFirstTurnStart_OtherSideActing_StaysNear`;
     - `AssumeOwnTurn_IgnoredOnceATurnWasSeen`.
3. **One computed state for everyone.**
   - `LindaFarState.Reading` is a `FarWatchReading` with `Enabled`, `Far`, `Source` (live, locked or level start), `NearestUnit`, `NearestDistance` and `Factor`. It is set on every refresh: each frame, each turn event, and the Watch prompt and activation.
   - `IsFar`, `Source`, `WatchFactor`, `NearestUnit` and `NearestDistance` now read from it.
   - `RefreshNow()` is public: the prompt calls it so the factor it prints is the one Watch will use.
   - C2's presenters read `Reading`. They evaluate only for hypothetical positions: `EvaluateAt` for Linda's ghost tile, and the new `EvaluateWithMove(mover, origin)` for another unit's ghost.

Also found while building C2: **the per-frame check allocated.** `IsUnitIgnoredForObjectives` goes through `GTagRegistry.Match`, which uses LINQ and builds hash sets. `LindaFarState` now caches each unit's "spawned" answer once per level (the decoy's `EntityState.IgnoreObjective` is a permanent tag) and clears the cache on `levelStarted`. With the cache, the live check, the ghost-tile check and the move-preview check allocate nothing per frame.

**Split for separate commits:**
- `LindaQuiver` is now `partial`. Its `Start` calls the partial method `AddFarViews()`, which C2 implements in `LindaQuiver.FarViews.cs`; without that file the call compiles to nothing.
- The two text and font wiring tests went into C2's `FarDisplayWiringTests.cs`.
- Checked offline (Unity's own Roslyn and `.rsp` files; HEAD copies of the three files C2 modifies):
  - C1 alone: game assembly and editor assembly, 0 errors;
  - C1 + C2: both assemblies, 0 errors;
  - no warnings in either.

**Tests (outside Unity, real test code with Unity's NUnit and CoreModule):** rules 29 and lock 12, all pass (80 of 80 together with C2's display tests). `FarWatchWiringTests` (13) still needs THJ's Test Runner.

### Proposed commits (C1, final)

1. `feat(linda): Far Watch scales Watch damage by distance from the family at End Turn`. Files, under `miso/Assets/_Project/Features/Player/Linda/`:
   - `Scripts/Quiver/`: `LindaDistanceTuning.cs`, `FarWatchRules.cs`, `FarWatchLock.cs` and `LindaFarState.cs`, each with its .meta; `LindaQuiver.cs` and `QuiverLevelAccess.cs`;
   - `Data.meta`, `Data/LindaDistanceTuning.asset` and its .meta;
   - `Prefabs/Unit_Linda.prefab`;
   - `Scripts/Quiver/Editor/`: `FarWatchRulesTests.cs`, `FarWatchLockTests.cs` and `FarWatchWiringTests.cs`, each with its .meta.

   Kind: risky. C2's commit goes on top of it (see `linda-d1-c2.md`). Both wait for THJ's play check (`playtests/2026-10-28-linda-d1-far-play-check.md`).
