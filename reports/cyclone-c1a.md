# Report: Cyclone redesign, C1a (anchored Cyclone)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer (opus)    Branch: thj/cyclone
Outcome: done (play check pending; C1a is meant to be committed together with C1b)

## What changed

New, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/` (namespace `MISO.Core.Features.Bergsons`, LF, no BOM; folder `.meta` included):
- `CycloneEntity.cs` (+ .meta): `CycloneEntity : OnGridEntity`. Overrides `PhaseTick` (one pip lost on the owner's phase start, which is the family turn start; fades at 0), `TurnGeneralTick` (does nothing: no move, no life loss), `Activate` (does nothing: no landing hit, no hit on a unit entering its cell), `Initialize` (sets `IsTargetable = false`, registers, adds the cross and pips views), `Dispose` (unregisters, hides views). New serialized fields `armLength` (2) and `whirlHitTimes` (3, used for the label now; C1b should read it for the real hit). No field moved, so no `[FormerlySerializedAs]` was needed.
- `CycloneRules.cs` (+ .meta): pure rules: `IsValidCastCell` (no unit, nothing stashed, no planted entity), life countdown, pips, arm cells (nearest ring first, with inward direction), touching cells, the "3 ×" label, cell spacing.
- `CycloneRegistry.cs` (+ .meta): static list of live Cyclones for the one-at-a-time rule. Read on the AI worker thread (through the activation check), so it uses plain reference compares under a lock. `ResetPlayModeState()` registered in `PlayModeStaticReset`.
- `AEffectCycloneSpawner.cs` (+ .meta): `AEffectSpawner` subclass for the cast. `CheckActivationFeasibility` false while the caster's Cyclone is out (button off); `CheckTargetSelectionCondition` refuses cells that aren't empty (so `IsLegalAbilityTarget`, the cursor and the click refuse them); `ApplyUnguarded` refuses both cases again with a warning, never silently.
- `CycloneCrossView.cs` (+ .meta): placeholder cross while the Cyclone is out: two inward wind streaks on each of the 8 arm cells (Default layer, order -5: over the grid's own overlays, under units) and a "3 ×" label on the 4 touching cells (DynamicTop -5: under HP bars). Own renderers under its own root, not the grid cells' highlight flags, so no preview erases it.
- `CyclonePipsView.cs` (+ .meta): 3 placeholder dots under the Cyclone (DynamicTop -1, like the quiver pips), bright = left, dark = spent.
- `CycloneSprites.cs` (+ .meta): code-made placeholder sprites (streak, dot).

New, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/` (LF, no BOM):
- `CycloneAnchoredSetup.cs` (+ .meta): one-off, re-runnable editor tool `Tools/Lucy/Apply Anchored Cyclone Setup`. Switches the prefab's entity script and the spawn effect's script through `SerializedObject` (keeps every value and reference), sets the anchored values and the ability numbers. Run once via the Unity MCP; results below.
- `CycloneTestGrid.cs` (+ .meta): shared test helper (hand-built grid, bus, reflection setters).
- `CycloneLifeTests.cs`, `CycloneCastTests.cs`, `GridEntityLifetimeTests.cs` (+ .meta each): 18 new EditMode tests.

Modified:
- `Features/Player/Lucy/Prefabs/Cyclone.prefab`: root entity script `OnGridEntity` → `CycloneEntity`; `motionMode` TowardsUnits → Stationary (also turns the base pass-by trigger off), `lifeTurns` 5 → 3, `isTargetable` 1 → 0, `applyPassByEffect` 1 → 0; `disallowWalk` stays 1; Unity added the missing defaults (`activateOnTile: 0`, `activationMode: 0`) and the two new fields. `LucyCycloneProjectileScatter.selfEntity` still points at the same component (tested). `effect` (the old 7× compound, with the Howling Gale Weak) and `passByEffect` stay referenced but never fire; C1b decides what to reuse.
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Effect_Spawn.asset`: script `AEffectSpawner` → `AEffectCycloneSpawner`; Unity wrote the base class's default fields that the old file lacked (empty queries, `revertible: 0`); `entityToSpawn` unchanged.
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`: `coolDownV` 2 → 4, `radiusV` 4 → 3. AP cost (1) unchanged. This preset is also Lucy's Super Time ability.
- `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (**core: role handler**, smallest guard): `ActivateSuperTime` picks only cells passing `CycloneRules.IsValidCastCell` (was `IsWalkable`, which accepted spikes/webs and other non-blocking planted entities, and threw on an empty list). Skips with a warning when her Cyclone is already out or no empty cell exists.
- `Core/Managers/PlayModeStaticReset.cs` (**core**): one line, `CycloneRegistry.ResetPlayModeState()`, the documented pattern for a new static.

Not touched: `OnGridEntity` and every other core runtime file, the Linda-folder Cyclone copies, THJ's uncommitted files.

## Acceptance criteria (C1a share of C1)

- [x] Never moves by itself, no target choice, no random walk: `TurnGeneralTick` and `PhaseTick` overridden without `Move`; prefab Stationary. Test `CycloneLifeTests.TurnStarts_NeverMoveIt` (3 cases: TowardsUnits/TurnGeneral, RandomWalk/TurnGeneral, RandomWalk/Turn with an owner and an enemy on the grid; cell, planted slot and position unchanged after 4 rounds) and `CycloneCastTests.LivePrefab_IsAnAnchoredCyclone`.
- [x] Life 3 pips, one lost at each family turn start, none on other turn starts: `OneRound_LosesOnePip`, `OtherTurnStarts_LoseNoPip`, `PipsChanged_RaisedOncePerFamilyTurnStart`, `FadedCyclone_IgnoresLaterTicks`.
- [x] Cast in round 1 → alive through enemy turns 1, 2, 3, fades as round 4 starts: `CastInRoundOne_LastsThroughThreeEnemyTurns_FadesAsRoundFourStarts`.
- [x] Pips shown on it: `CyclonePipsView` (placeholder). Play check.
- [x] Old landing hit and pass-by hit don't fire: `Activate` is a no-op; pass-by off by Stationary + `applyPassByEffect` 0 (prefab test). **Until C1b lands the Cyclone deals no damage at all** (expected).
- [x] `isTargetable` off: prefab value 0 and forced off in `Initialize` (prefab test).
- [x] Cast range 3, cooldown 4, 1 AP: `LiveAbility_CastsTheCycloneAtRange3_Cooldown4`.
- [x] One Cyclone at a time: `OneCycloneAtATime_PerCaster` (feasibility false while hers is alive and registered; other casters unaffected; true after it fades).
- [x] Only on an empty cell; preview refuses others: `EmptyCell_Accepted`, `CellWithUnit_Refused`, `CellWithPlantedEntity_Refused`, `CellWithAnotherCyclone_Refused`, `CellWithSpentPlantedEntity_Accepted`. The cursor/hover refusal itself is a play check.
- [x] Super Time picks only valid cells, never silently fails: code guard + warnings; play check (not unit tested: needs the role handler's orchestrator).
- [x] Cross drawn while out (8 arm cells with wind lines, "3 ×" on 4 touching cells): geometry tested in `Cross_HasEightArmCellsAndFourTouchingCells`; drawing is a play check.
- [x] AOE warnings and hazards keep their lifetimes: `GridEntityLifetimeTests` (plain grid entity loses one per turn start and one per owner phase start; the real `AOE_Attack.prefab` is still a plain `OnGridEntity` with 1 turn of life and ends on the next turn start; `HazardEntity` loses one per phase start and per turn start). `OnGridEntity` is unchanged by construction.
- [x] `disallowWalk` kept true (prefab test), so `GroundedArrowField.CanHoldArrow` and today's blocking are unchanged.

**EditMode suite:** 1917 run, 1916 passed, 1 failed: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (42 failing checks, none about the Cyclone; both `Lucy_Cyclone_Ability` name/evaluator checks pass). Not re-baselined. Compile clean (no new warnings from these files).

## Save reset

No.

## Decisions I made

- One-at-a-time is enforced in the cast effect's activation check (button off while hers is out) plus an execution-time refusal; C3 turns this button into Steer, so the "off" state is temporary.
- The "empty cell" rule also refuses a cell with a stashed entity (same idea as no unit); a planted entity that is no longer alive doesn't count.
- The spawner subclass replaces the cast's script instead of using the string hooks (`targetSelectCustomCall` sends to the target cell, which has no handler). Same behavior as asked; no core file changed for it.
- Cross and pips are own renderers (not `GridCell.SetHighlight`/`SetWarningHighlight`), because those are shared bools other previews clear. No grid API change. Sorting picked per the layers listed above.
- The asset switch went through a re-runnable editor tool (GUID change), not hand YAML. The diffs are small (shown above).
- `whirlHitTimes` lives on the entity now only to draw the label; C1b should use it for the actual Whirl hit so the label can't drift.
- Ability description text ("Creates a tornado that moves and damages enemies.") left as is: wording is C5 / narrative.

## Needs THJ

1. **Super Time while her Cyclone is out.** Today's code now skips Lucy's Super Time cast with a console warning (nothing happens on screen for her). Alternative: Super Time replaces the old Cyclone with a fresh one on a valid cell. Recommendation: replace (Super Time should never be wasted), but it's a game rule, so I built the minimal skip. Coordinator/THJ to decide; it's a two-line change either way.

## Docs to update

- `tech/core-systems.md` (coordinator): `PlayModeStaticReset` now resets `CycloneRegistry`; `LucyFactionRoleHandler.ActivateSuperTime` picks only empty cells and can skip with a warning.
- GDD `characters/lucy.md` (designer, at C5): cast range 3, cooldown 4, empty cell only, one at a time, 3 pips, no damage until the Whirl.

## Risks and loose ends

- **No Cyclone damage between C1a and C1b.** Don't play-test C1a for balance; commit together with C1b as the plan says.
- `effect` on the prefab (old 7× compound) is still referenced, so previews or AI scoring that read `AEffectSpawner.NestedCompound` may still describe a 7× hit; the cast cell is always empty now, so the hover preview should show nothing. Check in play; C1b replaces it.
- Memory 4 (`Memory4Mark_Bloom_LucyCastsCyclone`, seal at (3,4)) and any scripted Cyclone cast now refuse a cell with a unit or a planted entity (warning in the console). If (3,4) is occupied in that scene, the cast won't happen. C5 checks Memory 4; worth a look in the C1 play check.
- `CombatLevelRunHandler.ResetCurrentPhase` re-runs the family's `PhaseTick`; if it's ever used mid-turn, the Cyclone loses an extra pip (same as every other registered entity today). Not changed.
- The Cyclone still blocks everyone (`disallowWalk`); per-faction walking is C2.
- `LucyCycloneProjectileScatter` unchanged; the null-cell-during-move risk only returns with Steer (C3).
- Dead Linda-folder Cyclone copies untouched (they still use `OnGridEntity`).
- The cross isn't hidden when the HUD/grid is hidden for cutscenes; if that reads badly in a memory, a hide hook is a small follow-up.

## Proposed commits

Assuming C1a and C1b are committed together after THJ's play check; C1b's files slot in after commit 3.

1. `feat(lucy): the Cyclone stays where it is cast, loses one pip at each family turn start, can't be targeted and shows its cross and pips` (plain): `Features/Player/Lucy/Scripts/Cyclone.meta`, `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.cs`(+.meta), `CycloneRules.cs`(+.meta), `CycloneRegistry.cs`(+.meta), `AEffectCycloneSpawner.cs`(+.meta), `CycloneCrossView.cs`(+.meta), `CyclonePipsView.cs`(+.meta), `CycloneSprites.cs`(+.meta), `Features/Player/Lucy/Scripts/Editor/CycloneAnchoredSetup.cs`(+.meta), `Features/Player/Lucy/Prefabs/Cyclone.prefab`, `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Effect_Spawn.asset`, `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`, plus the tests `Editor/CycloneTestGrid.cs`, `CycloneLifeTests.cs`, `CycloneCastTests.cs`, `GridEntityLifetimeTests.cs` (+.meta each). (The prefab and assets reference the new scripts, so they go together; tests can be split into their own commit right after if preferred.)
2. `chore(core): reset the live Cyclone list between play sessions` (core): `Core/Managers/PlayModeStaticReset.cs`. Depends on 1.
3. `fix(lucy): Super Time casts the Cyclone only on an empty cell and skips with a warning when none is free or hers is already out` (core: role handler): `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`. Depends on 1.

All paths under `miso/Assets/_Project/`. Don't stage THJ's uncommitted files (AI brains, PreloadScreen, ProjectSettings, TMP fallback font).

## Other branches

`thj/home-test` lacks the Cyclone redesign; merges later with the rest (plan).

## How to see it

1. Open any level with Lucy (e.g. a Trail fight). Select Lucy, pick Cyclone: the range is 3 cells; hovering a cell with a unit, spikes/web/pool/mushroom shows the refused cursor and a click does nothing.
2. Cast on an empty cell: the Cyclone appears and stays; faint inward wind streaks on the 2 cells in each straight direction, "3 ×" on the 4 touching cells, 3 bright dots under it. No damage happens (expected until the Whirl chunk).
3. The Cyclone button is unavailable while it's out (and shows cooldown 4 afterwards).
4. End turn: through the enemy turn it doesn't move and keeps 3 dots; enemies never target it. At the start of your next turn one dot goes dark. Cast in round 1 → still there during enemy turns 1, 2, 3; gone as round 4 starts (End animation).
5. Fill the family Super Time with Lucy in the roster: her Cyclone lands only on an empty cell. With her Cyclone already out, nothing is cast and the console shows "Lucy's Super Time Cyclone skipped: her Cyclone is already on the board."
6. Masher/Queen area warnings and hazards should behave as before.
