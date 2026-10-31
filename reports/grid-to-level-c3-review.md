# Review: grid-to-level C3

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. **Verdict: APPROVE.**

## Should fix (sent back as a small fix round)

1. `GridToLevelWindow.cs:163-169`: doc path `TextField` re-parses and writes `EditorPrefs` per keystroke; use `DelayedTextField`.
2. `GridToLevelWindow.cs:256`: the objectives warning is filtered by message text; share a const (or a flag on `GridIssue`).
3. `Build_FailingAfterValidationWritesNoOutputFolder` writes to `Greybox/__NeverMade` outside the test folder; clean it in `finally` or move it under the test folder.

## Notes

- Window does all of C3 (EditorPrefs path, remembered block, preview with objectives warning, errors before writing, Build disabled on errors and in Play, rebuild confirm and Prefab Mode exit, Open, Play as the toolbar). No static state.
- C2 should-fixes and the preview-scene tests done.
- Objectives check compares `branchingMode`, `lObjectives`, `decisions` with `LevelBase.prefab` (references by name).
- GB_ prefabs: all references resolve, no `LevelSequenceTrigger`, `levelName` = `GB_<id>`, sequences cleared, no turn-order override; only `GB_m1-linda` has the tier and alert. None has a `LevelStartFPFiller` (the default template has none). Inherited harmless leftovers: empty `SignalAction` on `CutsceneHandler`, spec tag `P0.Combat`, stale `turnOrders`, an orphan objectives override, unused `indices`.
- No effect elsewhere: `AIRegressionTest` skips them, no Mission or `GameDataSO` references, not under `Resources`.
- **`GB_m1-linda`** was built with `level tier tutorial` and `level alert all` added in memory: add those lines to the block in `plans/onboarding/2026-10-26-onboarding-levels.md` before structure C3 rebuilds it.
- Rebuild from Prefab Mode with unsaved edits: Unity's save prompt; cancelling it still builds. Check once in play.
- New `.cs` files are CRLF on disk like the folder, stored LF by `.gitattributes`.
- Commit split sensible (tool code + tests; the five prefabs alone).
