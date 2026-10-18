# Report: B4 R2 · Family Role Phase 0 bugfixes (F1, F3, F5)

Plan: plans/2026-10-18-family-role-phase0-1.md (chunk R2 only)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (F4 pulled after review, D-065)

Tier 2 bugfixes in core systems (Family Roles, PlayerController), approved as D-062 / D-063. No queue, no retry, no new rule, no new serialized field, no change to an existing public API. The one public addition is the pure helper class `FactionRoleRules` and its enum (new file); nothing existing changed signature.

**F4 pulled (D-065).** The reviewer found that Fist Blitz (`AEffectDashAttack`) picks its dash destination from the enemy's anchor cell. With F4, Mark could therefore punch big enemies from a distance. THJ moved F4 to the later Family Role chunk. The F4 change was reverted (`MarkFactionRoleHandler.cs` is identical to HEAD) and its helper and tests were removed. Everything needed to reapply it is saved in `reports/b4-f4-mark-footprint.patch.md`.

## What changed

Paths under `miso/Assets/_Project/`.

- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs` (+ `.meta`, new): static pure helpers with no state and no Unity objects, plus the enum `FactionRoleQTEOutcome { Pressed, Ignored, CouldNotStart }`. `AnyUnsilenced` (F1), `ShouldSilence` (F3), `FirstMatchAcrossGroups` (F5). BOM + CRLF, like the folder's neighbours.
- **F1** `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs:116-117`: `Targets.Except(SilencedTargets).Any()` became `FactionRoleRules.AnyUnsilenced(Targets, SilencedTargets)`. A null `SilencedTargets` means nothing is silenced; otherwise it still runs the same `Except(...).Any()` with the default comparer. Null `Targets` now returns false where it used to throw (unreachable today: every `PrepareTargets` sets `Targets` before it returns true).
- **F3** `Core/Interactions/Runtime/PlayerController.cs:1520-1534, 1563-1571` (`ActivateFactionRole`): the old `ignoreActions` chain is now built by a local `BuildSkipActions(outcome)`. Its first step calls `SilenceFactionRole()` only when `FactionRoleRules.ShouldSilence(outcome)` is true. The remaining steps are unchanged (`cleanupActions` (hide role visual, hide spotlight), camera back to the saved focus point, `ClearInProgressAndRefreshEndTurn`, `Time.timeScale = 1`). `ignoreActions = BuildSkipActions(Ignored)` is still passed to `StartEvent` as the QTE's ignore callback, so a timer that runs out with no press silences exactly as before. `if (!started)` now runs `couldNotStartActions = BuildSkipActions(CouldNotStart)`: the same cleanup without the silence.
- **F5** `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs:53-56`: `enemyFactions[0].Controller.AliveUnits.Where(!IsDowned).FirstOrDefault(pred)` became `FactionRoleRules.FirstMatchAcrossGroups(enemyFactions, f => f.Controller.AliveUnits, e => !e.IsDowned && pred)`. Factions are searched in list order, units in list order, first match wins. The predicate is unchanged, so the in-range check, `GetMostRecentAttacker() != Unit` (skip the enemy she hit last) and the tied-to-action checks all stay. `GetFactionEnemies` already filters out factions without a controller (`LevelFactionRelations.cs:73`), so `f.Controller` is safe.
- `Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs` (+ `.meta`, new): 14 EditMode tests, namespace `MISO.Core.Systems.AbilitySystem.Abilities.EditorTests`.

## Acceptance criteria

- [x] F1: no throw when `SilencedTargets` is null. Tests `AnyUnsilenced_*` (null silenced = none silenced, all silenced = false, partial = true, null targets = false).
- [x] F3: a QTE that could not start skips the role without silencing; a real ignore still silences; no queue. Tests `ShouldSilence_*` cover the decision. The wiring in `PlayerController` (which outcome goes to which path) needs the **verifier's play check**: busy QTE (for example a synergy QTE active when a role triggers), then the same enemy triggers the role again later in that enemy turn.
- [ ] F4: **pulled from R2 (D-065)**, parked in `reports/b4-f4-mark-footprint.patch.md`. It first needs `AEffectDashAttack` to approach multi-tile targets by their footprint.
- [x] F5: Lucy searches every hostile faction, first match in list order, no nearest rule. Tests `FirstMatchAcrossGroups_*` (match only in the second group, first group wins, list order inside a group, no match). **Play check** needs a level with two hostile factions.
- [x] Compiles with no console errors. EditMode suite after the F4 revert: 93 tests, 92 passed, 1 failed: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, all graph, ability and prefab baseline drift plus its fatal NRE; nothing references the code changed here). `FactionRoleRulesTests`: 14/14.

## Save reset

No.

## Decisions I made

- F1: null-safe helper at the call site instead of initialising the field. It covers both "never set" and `Silence()` copying a null `Targets`. Same behaviour otherwise.
- F3: built the two skip chains from one local builder so they cannot drift apart; the only difference is the silence step. A `false` from `StartEvent` for other reasons (QTE mode not implemented, no pooled button, input action missing) also counts as "could not start": none of these showed the player a prompt they could answer.
- Helpers are generic (no `GridCell`/`GUnit` types) so the tests need no scene or Unity objects. No statics with state, so no `PlayModeStaticReset` hook needed.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` (coordinator): Family Roles: a role whose QTE cannot start is skipped without silencing; Lucy searches all hostile factions. `FactionRoleRules` holds the pure decisions.
- `reports/b4-family-role-facts.md`: bug list item 1 and the first-faction part of item 6 are now outdated, if the file is kept current. Mark's anchor-only check (item 5) still holds.
- `build-log.md` entry (coordinator).

## Risks and loose ends

- F3: when a role cannot start because of a busy QTE, its targets are no longer muted, so the same enemy can raise the role again on its next action event. There is still no retry: each event checks once. If the other QTE is still active then, it skips again quietly. Expected by the plan; worth a look in the play check.
- F3: the could-not-start path still shows the prompt visual for an instant (`ShowFactionRolePromptVisual` runs before `StartEvent`) and the cleanup hides it. Unchanged from today.
- F4 parked: reapply from `reports/b4-f4-mark-footprint.patch.md`, which holds the hunk, the helper and 5 tests, in the Family Role chunk, after footprint-aware approach in `AEffectDashAttack` (shared core code).
- Not touched, noticed: the "same action also targeted Mark" block (facts bug 5) is out of scope (the Family Role chunk).
- AI: none of the changed code runs on the AI worker (role handlers and `PlayerController` run on the main thread only).

## Proposed commits

1. `fix(family-roles): null-safe silence check, no silence when the role QTE can't start, Lucy searches all hostile factions (B4 F1 F3 F5)` (core):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs.meta`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs.meta`

   One commit (7 files). All three fixes use the new helper file. `MarkFactionRoleHandler.cs` has no change. Do not stage `Packages/*` or `ProjectSettings.asset` with it.

## Other branches

`thj/home-test` gets these on its next merge of `main`.

## How to see it

1. Recompile (Ctrl+R). Window > General > Test Runner > EditMode > run `FactionRoleRulesTests` (14 green).
2. F1: start any combat level and let an enemy act before you select a unit. No `ArgumentNullException` from `FactionRoleHandlerBase.CheckFeasibility` in the console.
3. F3: in an enemy turn, make a role trigger while another QTE is up (for example a synergy QTE). The role is skipped and the camera, time scale and End Turn button recover. Later in the same enemy turn the same enemy can trigger the role again. Let a normal role prompt run out without pressing: that enemy does not trigger it again this turn (as before).
4. F5: in a level with two hostile factions, have a family action hit an enemy of the second faction inside Lucy's radius 3. Her ember prompt appears (before, only the first faction was searched).
