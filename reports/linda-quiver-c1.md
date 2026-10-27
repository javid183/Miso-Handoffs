# Report: Linda's Quiver, C1 (quiver, spending, landing, gating)

Plan: plans/2026-10-26-linda-quiver-tech.md (chunk C1)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done (EditMode green except the known red, message unchanged; play criteria not verified in play)

## What changed

All paths under `miso/Assets/_Project/`. All files are LF, no BOM (new files written LF to match the Linda/Lucy/Mark scripts and the prefabs; edited files kept LF).

New, `Features/Player/Linda/Scripts/Quiver/` (folder `.meta` included):
- `QuiverState.cs` (+ `.meta`): plain-C# count, never below 0 or above size; `TrySpend`, `Add` returns how many went in.
- `LindaQuiver.cs` (+ `.meta`): component on Linda. `Count`, `Size` (serialized, 4), `Spend()`, `Add(n)`, `OnChanged`; feasibility receivers `HasArrow(HBoolean)` and `HasGroundedArrows(HBoolean)` (plain reads, AI-thread safe). Reads as full even without Awake (edit-mode prefab checks).
- `ArrowLandingRules.cs` (+ `.meta`): pure static. `LineCells(from, to)` (Bresenham, shooter excluded) and `ChooseLanding(path, lastEnemyHit, endOfFlight, isValid, fallback)`.
- `GroundedArrowStacks.cs` (+ `.meta`): plain-C# cell → stack registry with locks: `Add`, `Take(cell, max)` (refuses locked), `TakeAll`, `SetLocked`, `Clear`, `Total`.
- `GroundedArrowField.cs` (+ `.meta`): per-level MonoBehaviour (created on first landing, moved into the level's scene). Holds the stacks, polls locks (a living enemy of Linda on the cell), draws the placeholder views (the arrow's own sprite tilted, on sorting layer `WorldUI`; a TMP stack number when 2+; locked = reddish-grey icon and red number). Emptied and closed on `levelEnded`. Static `_current` with `ResetPlayModeState()`; static `GroundedCount` and `CanHoldArrow(cell)`.
- `QuiverArrow.cs` (+ `.meta`): sibling of `Projectile` on the arrow prefabs. Spends in `Start` unless `MarkAsCopy()` was called; tracks the last enemy touched in its own `OnTriggerEnter2D`; lands once, from `Projectile.onDisposeReady`. Landing modes: `LastEnemyHitOrEndOfFlight` (bow, Watch), `EndOfFlight` (Crescendo, Duo arrows). Hooks for the cloners: `LandAt(cell)`, `HoldLanding()`, `ReleaseLanding()`, `ReturnToQuiver()`.

New tests, `Features/Player/Linda/Scripts/Quiver/Editor/` (namespace `MISO.Core.Features.Bergsons.EditorTests`, folder `.meta` included):
- `ArrowLandingRulesTests.cs` (14), `QuiverStateTests.cs` (8, one drives a real `LindaQuiver` component), `GroundedArrowStacksTests.cs` (9), `QuiverWiringTests.cs` (10: Linda has a quiver of 4, the four arrow prefabs have `QuiverArrow` with the right mode, the five spawn effects say `HasArrow`). Each with `.meta`.

Edited:
- `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`: flags each split copy with `MarkAsCopy`; the original gets `LandAt(cyclone cell)` before its `Dispose`.
- `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`: flags the bounce clone as a copy; in bounce modes holds the original's landing while the catch is pending; on the catch (`Apply`) returns it to the quiver (+1); on miss / no QTE / disable releases it to land normally.
- `Core/Managers/PlayModeStaticReset.cs` (core list, Infrastructure): one line, `GroundedArrowField.ResetPlayModeState()` (fully qualified, no new `using`). The hook the plan allows.
- `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: `LindaQuiver` (size 4) added to the root (new MonoBehaviour + `m_AddedComponents` entry of the variant).
- `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab` (mode 0), `LindaExplosiveArrow.prefab`, `LindaAttackFireArrow.prefab`, `LindaAttackHealArrow.prefab` (mode 1): `QuiverArrow` added to the root.
- `activationFeasibilityCheckFunction: HasArrow` on five spawn effects: `Resources/UnitSpecific/Player/Linda/Attack/Primary Attack/Linda_Ability_PrimaryAttackM_Effect_Spawn.asset`, `.../Attack/Explosive Arrow/Linda_Ability_ExplosiveArrow_Effect_Spawn.asset`, `.../Faction Role/Linda_Ability_FactionRole_Effect_Spawn.asset`, `Resources/Abilities/Cooperation/Linda_Lucy/Linda/Linda_Lucy_LINDA_Duo_Ability_Effect_Spawn.asset`, `Resources/Abilities/Cooperation/Linda_Toba/Linda/Linda_Toba_LINDA_Duo_Ability_Effect_Spawn.asset`.

Unity did not re-serialize anything during the batch runs: `git status` shows only these files, plus the three files that were already modified before I started (`LiberationSans SDF - Fallback.asset`, `EditorSettings.asset`, `ProjectSettings.asset`; not mine, not to stage).

## Acceptance criteria

- [ ] **Bow from 4 leaves 3; icon on the last enemy hit (pierce through 2: on the second), or at end of range on a miss.** Not verified in play. Code: the bow's spawn effect spawns `LindaAttackArrow`, whose `QuiverArrow.Start` calls `Spend()` (4 → 3). Its trigger records the cell of every living enemy it touches, so the last one wins (the second when it pierces two); an enemy standing on the end cell counts as last. On a miss the landing is the end of flight, which for this `travelEntireRadius` projectile is the furthest existing cell in range. Rules EditMode-tested (`Hit_LandsOnTheEnemysCell`, `PierceThroughTwo_LandsOnTheSecond`, `Miss_LandsAtEndOfRange`).
- [x] **Past a hole or into a wall: last valid cell of its path.** EditMode: `EndIsAHole_...`, `EndIntoAWall_...`, `HoleMidPath_EndBlocked_...`, `HitCellBlocked_...`, `NothingValid_LandsOnTheShooter`. "Valid" (`GroundedArrowField.CanHoldArrow`): the cell exists, its planted object isn't `DisallowWalk`, and any occupant is a unit.
- [ ] **Crescendo on its centre cell; Marks-Sisters / Healing Marks at the end of the line; each costs 1.** Not verified in play. Code: `LindaExplosiveArrow`, `LindaAttackFireArrow` (Marks-Sisters, Linda's side only) and `LindaAttackHealArrow` (Healing Marks, Linda's side only) carry `QuiverArrow` in `EndOfFlight` mode; each spends 1 in `Start`. The heal arrow does nothing unless its owner has a `LindaQuiver`. Wiring EditMode-tested (`QuiverWiringTests`).
- [ ] **Watch spends 1 per trigger; at 0 no prompt, and bow, Crescendo and both arrow Duos greyed out.** Not verified in play. Code: Watch fires `LindaAttackArrow` (spends 1). The five spawn effects say `HasArrow`; `RuntimeAbility.CheckActivationFeasibility` (used by `Active`, so the panel greys them) asks the quiver through `GameEntityMessage`; `FactionRoleHandlerBase.CheckTriggerConditions` already calls it, so at 0 Watch never prompts; `CooperationEntry.Available` checks the Linda partner ability's `Active`/`ActiveNoAPConsidered`, so both Duos grey out. Data EditMode-tested; the receiver is tested on a live component.
- [ ] **Tempest Bloom: 1 spent, 1 grounded. Catch & Return: 0 net spent, nothing grounded.** Not verified in play. Code: the scatter marks its copies (no spend, no land) in the frame `GetClone` makes them, before their `Start`; the original spent at launch and lands on the cyclone's cell. Mark: the bounce clone is marked a copy (it's made and deactivated in the same frame, so its `Start` runs only after the flag); the original's landing is held from the catch trigger, and on the catch it gets `ReturnToQuiver()` (+1), so the net is 0 and neither flight lands. A missed QTE releases the hold and the original lands normally.
- [ ] **Two arrows on one tile show "2"; an arrow under a living enemy shows the locked state.** Not verified in play. Code: the field draws the number for stacks of 2+, and polls each stack cell every frame for a living enemy of Linda's faction; locked = reddish-grey icon, red number. Stack and lock logic EditMode-tested (`GroundedArrowStacksTests`).
- [x] **EditMode tests: landing rules, quiver arithmetic, field stack add/take/lock.** 41 new tests, all pass.

## Test results

Full EditMode suite, command line, Unity 6000.3.4f1 (editor closed). Results and logs: `C:/Users/javid/AppData/Local/Temp/claude/E--Work-Projects-miso/038223eb-f0c2-4e68-9c09-24e1fd210f68/scratchpad/` (`before.xml`, `after2.xml` and `.log`s).

- Before the change: 743 tests, 742 passed, 1 failed (`AIRegressionTest.Baseline_MatchesCurrentAI`: "CHECKS: 709 FAILURES: 38").
- After (final code): 784 tests, 783 passed, 1 failed, the same test. Its failure message, with the timing lines (`graphs.stress.*`) removed, is **identical** before and after (diffed line by line). No compile errors; no compiler warnings in the new or edited files.

## Save reset

No.

## Decisions I made

- **Spending waits for `Start`**, as the plan says. I checked both cloners: the scatter calls `MarkAsCopy` right after each `GetClone` in the same trigger callback; Mark's clone is made and set inactive in the same frame, and `Start` of an inactive object runs only when it's activated. Projectiles are destroyed, not pooled (`SpawnableEntity.Dispose` → `Destroy` after `disposeDelay`).
- **Landing hooks `Projectile.onDisposeReady`** (an existing public UnityEvent) instead of `OnDisable`/`OnDestroy`. Same behavior, safer: Mark's clone is deactivated on purpose (`OnDisable` would land it), and scene unload destroys projectiles without `Dispose` (so nothing lands at level end). Lands exactly once (a `_resolved` flag; `Dispose` can be called more than once).
- **The level-ending guard is in the field**: after `levelEnded` it is closed and refuses landings. Same effect as the plan's flag on `QuiverArrow`.
- **Only a paid arrow lands.** A shot fired with an empty quiver by a path that doesn't check feasibility (see "Super time" below) takes nothing and leaves nothing. This keeps "board + quiver ≤ 4".
- **Where the flight ended** is the cell whose anchor is nearest the projectile at `Dispose`. `Projectile`'s target cell and radius are private (no core change), and both bow and Crescendo end exactly on their target cell's anchor.
- **Gating on the Duo effect assets, not in `PlayerController.prefab`.** The prefab only references Linda's partner presets; the spawn effects are separate assets, so the edit is there (no prefab change needed). Same behavior.
- **Catch & Return holds the original's landing during the catch.** The plan says "+1 on the catch, neither lands", but the original keeps flying during the QTE and can be disposed before the catch resolves. The hold makes it wait; a miss releases it.
- **Tempest Bloom lands under the Cyclone even though the Cyclone blocks walking** (`Cyclone.prefab` has `disallowWalk: 1`). The gap-fill says "lands on the cell where it split"; the general blocked rule would move it one cell back toward Linda. I took the gap-fill literally (`LandAt` bypasses the validity check). **Coordinator: please confirm**, or I switch it to the general rule (one line).
- Placeholder view: the projectile's own sprite, tilted, on `WorldUI` (above units), number only for 2+; no text words, so no `[PLACEHOLDER]` tag was needed.

## Needs THJ

None for C1 itself. Two points for the coordinator to decide or pass on (see Risks): the Tempest Bloom landing cell above, and Linda's super time.

## Docs to update

- `tech/combat-architecture.md`: the quiver and the field (LindaQuiver on Unit_Linda; GroundedArrowField per level, static reset; QuiverArrow on four arrow prefabs; `HasArrow` on five spawn effects; landing on `onDisposeReady`).
- `tech/core-systems.md`: `PlayModeStaticReset` gains the `GroundedArrowField` reset (if the file tracks such additions).

## Risks and loose ends

- **Linda's super time fires Explosive Crescendo** (`superTimeAbility` on her role handler is `Linda_Ability_ExplosiveArrow`). `ActivateSuperTime` calls `Orchestrator.ActivateAbility` directly, so it ignores the gating: with arrows it spends 1 and lands one at the centre; at 0 it still fires, spends nothing, lands nothing. The design doesn't mention super time; worth a line from the designer.
- **`DisallowWalk` objects** that block a landing include Toba's wall, Lucy's Cyclone, `AOE_Attack`, `CP_Spawner` (corruption pool spawner) and `MushroomExplosion`. The rule follows the plan's "blocked (`DisallowWalk`)". The gap-fill about sharing a tile with hazards holds for anything that doesn't set `DisallowWalk`; for a corruption pool it depends on whether the pool object itself or only its spawner blocks walking. Worth a look in play.
- **Bow arrows fly over walls** (the projectile travels to the furthest existing cell, as before). An arrow shot "past" a wall mid-line lands beyond it, where the flight ended. Only an end cell that is blocked or missing falls back.
- **Mark: catch animation interrupted.** If the catch animation never reaches its apply frame, the held arrow stays held until Mark's component is disabled (then it lands). Same for two catches overlapping before the first applies: the first is released and lands. Arrows are never duplicated; at worst one is not returned.
- **Same-frame double fire.** Spending happens in `Start` (next frame); if an arrow ability and Watch both pass the `HasArrow` check in the same frame at 1 arrow, the second shot is unpaid (fires, doesn't land). Not seen in the flows I read.
- **G3 is not in C1**: an arrow whose landing falls back to Linda's own cell (no valid cell on its path) is grounded under her. C2 picks it up.
- The field polls lock state every frame (only while stacks exist; a handful of cells). C2's pickup can reuse `GroundedArrowStacks.Take` and `GroundedArrowField.Current`.
- `LindaQuiver.HasGroundedArrows` is in place for C3's Recall; nothing uses it yet.
- `AIRegressionTest`: unchanged by this chunk (message identical). Recall (C3) is the change the plan expects might move it.

## Proposed commits

1. `feat(linda): add the quiver, arrow landing rules and grounded arrow field` (plain; touches one core file for the reset hook):
   `Features/Player/Linda/Scripts/Quiver.meta`, `Features/Player/Linda/Scripts/Quiver/{QuiverState,LindaQuiver,ArrowLandingRules,GroundedArrowStacks,GroundedArrowField,QuiverArrow}.cs` + their `.meta`, `Features/Player/Linda/Scripts/Quiver/Editor.meta`, `Features/Player/Linda/Scripts/Quiver/Editor/{ArrowLandingRulesTests,QuiverStateTests,GroundedArrowStacksTests}.cs` + their `.meta`, `Core/Managers/PlayModeStaticReset.cs`.
   (The reset line references `GroundedArrowField`, so it ships with it. If THJ wants every core-file line on its own, it can be a second commit right after this one.)
2. `feat(linda): Tempest Bloom copies and Catch & Return bounces leave Linda's arrow count alone` (plain):
   `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`, `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`.
3. `feat(linda): Linda's shots spend arrows from a quiver of 4 and land on the board` (risky: prefab and ability data; the gating and the quiver component must land together, or her arrow abilities are always greyed out):
   `Features/Player/Linda/Prefabs/Unit_Linda.prefab`, `LindaAttackArrow.prefab`, `LindaAttackFireArrow.prefab`, `LindaAttackHealArrow.prefab`, `LindaExplosiveArrow.prefab`, the five `..._Effect_Spawn.asset` files listed above, `Features/Player/Linda/Scripts/Quiver/Editor/QuiverWiringTests.cs` + `.meta`.

THJ's rule is play-test before commit for feel chunks; the plan sets the first play check after C3.

## Other branches

`thj/home-test` and `thj/onboarding` once this reaches `main` (THJ moves it), as the plan says.

## How to see it

1. Open Unity, let it compile. Open a level with Linda and some enemies (for example M4).
2. Bow-shoot an enemy: the arrow sprite (tilted) appears on that enemy's tile, reddish-grey because the enemy stands on it (locked). Kill the enemy: it turns white.
3. Shoot into empty ground: the arrow lies at the end of range. Shoot a line of two enemies: it lies under the second.
4. Shoot twice onto the same tile: a "2" appears beside the icon.
5. After four arrow shots (bow, Crescendo, Watch triggers or the Linda–Lucy / Linda–Toba Duos), the bow, Crescendo and both Duos are greyed out, and an enemy stepping into her lane gives no Watch prompt. There is no count on screen yet (C4); the cheat that resets cooldowns doesn't refill arrows.
6. With the Tempest Bloom unlock: shoot through Lucy's Cyclone; three copies fly, one arrow lies under the Cyclone. With Mark's Catch & Return: the caught arrow leaves nothing on the board and doesn't use up an arrow.
7. Next level: no arrows on the board, full quiver.
