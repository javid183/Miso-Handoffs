# Report: Objective feedback, C2 result summary line

Plan: plans/onboarding/2026-11-10-objective-feedback-tech.md    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check by THJ still to do)

## What changed

Code + tests (commit 1), all under `miso/Assets/_Project/`:
- Core/UI/Runtime/SessionEndPanel/LevelResultLine.cs (+.meta): new level-root component, one string + enabled flag; pure rule `ReplacesRows(isWin, enabled, text)` and `LineFor(result)` (reads `CombatLevel.Instance`). Not a core-list system; no statics.
- Core/UI/Runtime/SessionEndPanel/MissionEndPanelUI.cs: `SetObjectives` passes `LevelResultLine.LineFor(result)` to `AddObjectives`; with a line, the column holds that one row (Success state) instead of the objective rows. Loss, no component, blank or disabled line: unchanged. Stats column untouched. Not on the core list.
- Features/Onboarding/Editor/HearthMemoryWiring.ResultLines.cs (+.meta): `HearthMemoryResultLines` holds the four exact lines, `Ensure` adds/updates the component idempotently, menu `Tools/Onboarding/Wire Hearth Result Lines` applies to all four prefabs touching nothing else.
- HearthMemoryWiring.Linda.cs / .Lucy.cs / .John.cs: one `HearthMemoryResultLines.Ensure(...)` line each in WireLevel, so re-runs keep the line.
- Core/UI/Editor/LevelResultLineTests.cs (+.meta): row-choice rule.
- Features/Onboarding/Editor/HearthMemoryResultLineTests.cs (+.meta): each memory has its exact line; no other prefab under Content/Levels has the component.

Level data (commit 2; needs commit 1 first, the prefabs reference the script GUID):
- Content/Levels/Greybox/GB_m1-linda.prefab, GB_m2-lucy.prefab, GB_m3-john.prefab, GB_m4-mark.prefab: each +17 lines, pure additions (component + its added-object entry). Checked with git diff: nothing of THJ's hand edits changed, including GB_m4-mark.

## Acceptance criteria

- [x] Memory won shows its single line: code path + prefab data in place; wiring tests cover data, rule tests cover the choice. Panel rendering needs THJ's play check.
- [x] Other levels and losses unchanged: rule tests; test confirms no other level prefab has the component.
- [x] Console clean: only pre-existing compiler warnings after compile; no new errors from this work.
- [x] EditMode: 1815 of 1816 pass; only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Save reset

no

## Decisions I made

- Component lives next to the panel (Core/UI/Runtime/SessionEndPanel, namespace MISO.Core.UI.Runtime) rather than Features, to avoid Core code reading a Features type. Not a core-list file.
- Memory 4 is set by the new small menu tool, not by the retired Mark tool (it would overwrite hand edits).
- `SessionEndObjectives` list is still filled with the win objectives; only the rendered rows change (nothing reads it elsewhere).

## Needs THJ

none

## Docs to update

- design/gdd/missions-structure.md MI-18 note (designer); tech/combat-architecture.md UI note (coordinator).

## Risks and loose ends

- The line row reuses the objective row prefab, so it shows the green "Success" tag beside the text. If THJ wants no tag, a follow-up tweak is needed.
- During the test run the MCP session disconnected once (editor reload); the rerun completed fine. Console holds unrelated errors/log lines from tests ("listener failed", "Can't remove GUnit").
- Lines are final text per THJ; no placeholder tag.

## Proposed commits

1. feat(ui): a level can name one summary line that its won panel shows in place of the objective rows: the 3 new runtime/editor files with .meta, MissionEndPanelUI.cs, HearthMemoryWiring.ResultLines.cs(+.meta), HearthMemoryWiring.Linda/Lucy/John.cs, both test files with .meta (plain)
2. feat(onboarding): the four Hearth memories show one result line when won: GB_m1-linda, GB_m2-lucy, GB_m3-john, GB_m4-mark prefabs (plain)

## Other branches

main, when this branch merges.

## How to see it

1. Play the Hearth, win Memory 1: the won panel's objectives column shows only "Seven Claws. One arrow." (likewise memories 2 to 4 with their lines).
2. Win any other level: rows as before. Lose a memory: defeat rows as before.
