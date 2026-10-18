# Report: B4 R2 · Family Role Phase 0 bugfixes (F1, F3, F4, F5)

Plan: plans/2026-10-18-family-role-phase0-1.md (chunk R2 only)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

Tier 2 bugfixes in core systems (Family Roles, PlayerController), approved as D-062 / D-063. No queue, no retry, no new rule, no new serialized field, no change to an existing public API. The one public addition is the pure helper class `FactionRoleRules` and its enum (new file); nothing existing changed signature.

## What changed

Paths under `miso/Assets/_Project/`.

- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs` (+ `.meta`, new): static pure helpers with no state and no Unity objects, plus the enum `FactionRoleQTEOutcome { Pressed, Ignored, CouldNotStart }`. `AnyUnsilenced` (F1, :25), `ShouldSilence` (F3, :32), `IsFootprintInRange` (F4, :36), `FirstMatchAcrossGroups` (F5, :47). BOM + CRLF, like the folder's neighbours.
- **F1** `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs:116-117`: `Targets.Except(SilencedTargets).Any()` became `FactionRoleRules.AnyUnsilenced(Targets, SilencedTargets)`. A null `SilencedTargets` means nothing is silenced; otherwise it still runs the same `Except(...).Any()` with the default comparer. Null `Targets` now returns false where it used to throw (unreachable today: every `PrepareTargets` sets `Targets` before it returns true).
- **F3** `Core/Interactions/Runtime/PlayerController.cs:1520-1534, 1563-1571` (`ActivateFactionRole`): the old `ignoreActions` chain is now built by a local `BuildSkipActions(outcome)`. Its first step calls `SilenceFactionRole()` only when `FactionRoleRules.ShouldSilence(outcome)` is true. The remaining steps are unchanged (`cleanupActions` (hide role visual, hide spotlight), camera back to the saved focus point, `ClearInProgressAndRefreshEndTurn`, `Time.timeScale = 1`). `ignoreActions = BuildSkipActions(Ignored)` is still passed to `StartEvent` as the QTE's ignore callback, so a timer that runs out with no press silences exactly as before. `if (!started)` now runs `couldNotStartActions = BuildSkipActions(CouldNotStart)`: the same cleanup without the silence.
- **F4** `Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs:63-64`: `!GetCellsInRange().Contains(attacker.CurrentCell)` became `!FactionRoleRules.IsFootprintInRange(attacker.OccupiedCells, attacker.CurrentCell, GetCellsInRange())`. The attacker counts if any of its occupied cells is one of Mark's range cells. That is Lucy's existing `e.OccupiedCells.Any(rangeCells.Contains)` pattern. An empty footprint (unit not placed properly) falls back to the anchor cell, the old check.
- **F5** `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs:53-56`: `enemyFactions[0].Controller.AliveUnits.Where(!IsDowned).FirstOrDefault(pred)` became `FactionRoleRules.FirstMatchAcrossGroups(enemyFactions, f => f.Controller.AliveUnits, e => !e.IsDowned && pred)`. Factions are searched in list order, units in list order, first match wins. The predicate is unchanged, so the in-range check, `GetMostRecentAttacker() != Unit` (skip the enemy she hit last) and the tied-to-action checks all stay. `GetFactionEnemies` already filters out factions without a controller (`LevelFactionRelations.cs:73`), so `f.Controller` is safe.
- `Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs` (+ `.meta`, new): 19 EditMode tests, namespace `MISO.Core.Systems.AbilitySystem.Abilities.EditorTests`.

## Acceptance criteria

- [x] F1: no throw when `SilencedTargets` is null. Tests `AnyUnsilenced_*` (null silenced = none silenced, all silenced = false, partial = true, null targets = false).
- [x] F3: a QTE that could not start skips the role without silencing; a real ignore still silences; no queue. Tests `ShouldSilence_*` cover the decision. The wiring in `PlayerController` (which outcome goes to which path) needs the **verifier's play check**: busy QTE (for example a synergy QTE active when a role triggers), then the same enemy triggers the role again later in that enemy turn.
- [x] F4: Mark measures from the attacker's whole footprint. Tests `IsFootprintInRange_*`, including "anchor outside, footprint cell inside = true". **Play check:** a multi-tile enemy whose anchor is just outside Mark's diamond but another of its cells is inside attacks an ally, and Mark's prompt appears.
- [x] F5: Lucy searches every hostile faction, first match in list order, no nearest rule. Tests `FirstMatchAcrossGroups_*` (match only in the second group, first group wins, list order inside a group, no match). **Play check** needs a level with two hostile factions.
- [x] Compiles with no console errors. EditMode suite: 98 tests, 97 passed, 1 failed: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, all graph, ability and prefab baseline drift plus its fatal NRE; nothing references the code changed here). The new class run alone: 19/19.

## Save reset

No.

## Decisions I made

- F1: null-safe helper at the call site instead of initialising the field. It covers both "never set" and `Silence()` copying a null `Targets`. Same behaviour otherwise.
- F3: built the two skip chains from one local builder so they cannot drift apart; the only difference is the silence step. A `false` from `StartEvent` for other reasons (QTE mode not implemented, no pooled button, input action missing) also counts as "could not start": none of these showed the player a prompt they could answer.
- F4: added the empty-footprint fallback to the anchor cell so a single-tile or mis-placed attacker behaves exactly as before.
- Helpers are generic (no `GridCell`/`GUnit` types) so the tests need no scene or Unity objects. No statics with state, so no `PlayModeStaticReset` hook needed.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` (coordinator): Family Roles: a role whose QTE cannot start is skipped without silencing; Mark measures the attacker's footprint; Lucy searches all hostile factions. `FactionRoleRules` holds the pure decisions.
- `reports/b4-family-role-facts.md` rows for Mark and Lucy and bug list items 1, 5 (anchor part) and 6 (first-faction part) are now outdated, if it is kept current.
- `build-log.md` entry (coordinator).

## Risks and loose ends

- F3: when a role cannot start because of a busy QTE, its targets are no longer muted, so the same enemy can raise the role again on its next action event. There is still no retry: each event checks once. If the other QTE is still active then, it skips again quietly. Expected by the plan; worth a look in the play check.
- F3: the could-not-start path still shows the prompt visual for an instant (`ShowFactionRolePromptVisual` runs before `StartEvent`) and the cleanup hides it. Unchanged from today.
- F4: Mark can now trigger against big enemies he could not before. The retaliation reuses Fist Blitz on `Targets = { attacker }`. `ability.CheckTargetSelectionCondition(attacker)` is still checked, but whether Fist Blitz's own effect or animation handles a multi-tile target whose anchor is out of reach is not verified here. Reviewer and play check.
- F4: Mark's own range is still measured from his anchor cell (`GetCellsInRange` uses `Unit.CurrentCell`). Mark is single-tile, and the plan only covers the attacker side.
- Not touched, noticed: the "same action also targeted Mark" block (facts bug 5) is out of scope (the Family Role chunk). R1's `Unit_Mark.prefab` change was left alone.
- AI: none of the changed code runs on the AI worker (role handlers and `PlayerController` run on the main thread only).

## Proposed commits

1. `fix(family-roles): null-safe silence check, no silence when the role QTE can't start, Mark footprint range, Lucy all hostile factions (B4 F1 F3 F4 F5)` (core):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs.meta`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs.meta`

   One commit, as the brief asks. All four fixes use the new helper file, so it cannot go in alone. Do not stage `Unit_Mark.prefab` (R1), `Packages/*` or `ProjectSettings.asset` with it.

## Other branches

`thj/home-test` gets these on its next merge of `main`.

## How to see it

1. Recompile (Ctrl+R). Window > General > Test Runner > EditMode > run `FactionRoleRulesTests` (19 green).
2. F1: start any combat level and let an enemy act before you select a unit. No `ArgumentNullException` from `FactionRoleHandlerBase.CheckFeasibility` in the console.
3. F3: in an enemy turn, make a role trigger while another QTE is up (for example a synergy QTE). The role is skipped and the camera, time scale and End Turn button recover. Later in the same enemy turn the same enemy can trigger the role again. Let a normal role prompt run out without pressing: that enemy does not trigger it again this turn (as before).
4. F4: put a multi-tile enemy (Goblin Queen or another big unit) so that only a non-anchor cell is inside Mark's radius-2 diamond, and let it hit an ally next to Mark. Mark's strike-back prompt appears.
5. F5: in a level with two hostile factions, have a family action hit an enemy of the second faction inside Lucy's radius 3. Her ember prompt appears (before, only the first faction was searched).
