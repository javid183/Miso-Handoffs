# Review: objective feedback C2 (result summary line), 2026-11-10

(Pasted by the coordinator; the reviewer runs read-only.)

**Verdict: APPROVE.** No must-fix.

Should fix: `Core/UI/Runtime/SessionEndPanel/MissionEndPanelUI.cs:188` allocates an empty list to skip the objective rows (`foreach (var objective in summaryLine != null ? new List<MissionEndObjective>() : sessionEndObjectives)`); wrap the loop in `if (summaryLine == null)` instead. Readability only.

Checks: neither `MissionEndPanelUI.cs` nor `LevelResultLine.cs` is on the core list; `CombatLevel.Instance` read only. Loss and other levels unchanged (`ReplacesRows` needs a win; no component → null → old loop). Stats column untouched; `SessionEndObjectives` still filled. Pure rule tested (win+enabled+text; loss, disabled, blank). Data tests: exact lines, flag on, 4 paths, no other level prefab has the component (root check correct). Wiring idempotent (`Ensure`; save only on change); Linda/Lucy/John tools gain one line each, nothing reverted. Retired Mark tool doesn't call `Ensure` (rerunning it would lose THJ's hand edits anyway). Re-running a memory tool re-enables a line THJ unticked (same as the tools' existing overwrites). Prefab diffs +17 pure additions each; GB_m4-mark only additions; script GUID matches. `LineFor` guards a null/destroyed level. No private IDs, no new statics, CRLF/BOM kept. Component placed in `Core/UI/Runtime/SessionEndPanel` (not Features) so Core never reads a Features type: reasonable, not a core-list file.

Risks: the summary row reuses the objective row prefab, so the green Success tag shows (THJ to confirm); `main` needs this on merge. Not checked in Play.
