# Sisters' tally C3 (results row): review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Three should-fix.

## Should fix

1. `Editor/SistersTallyResultRowSetup.cs:38`, `:137-140`: `AssetDatabase.SaveAssets()` saves every dirty asset, and `EditorSceneManager.SaveScene` saves THJ's unsaved edits when the container scene was already open. If the scene was already open, only mark it dirty and say "scene left unsaved, save it yourself" (or save only when opened here; at least say so in the class summary). Disk diff was clean this time.
2. `Editor/SistersTallyResultRowTests.cs` `Refresh_ShowsTheRowWithTheCounts_WhenEligible`: `StringAssert.Contains("Sisters' tally", ...)` can't fail (prefab stores that text). Set the label to something else before `Refresh()`, or drop it. The count assert is real.
3. `SistersTallyResultRow.cs:9`: comment says "Linda N - Lucy N" (hyphen); code uses an en dash.

## Notes (verified)

- Fill order correct: mission-end root inactive in the scene; `ShowSessionEndPanel` → `SetActive(true)` → `OnEnable` → `Refresh()` before `UpdateValues`, `AddResources`, `RefreshStatsColumn()`. Component on the panel root is right.
- Scoping robust: only `CombatLevelContainerScene.unity` uses the prefab (GUID `aa3540594ff954bc9baa1fd3c5a43a93`); only the mission-end instance has the override; a re-created instance fails safe (row hidden), caught by `ContainerScene_FlagsOnlyTheMissionEndPanel`.
- Prefab diff: only the new row instance, its child entry under `StatsColumn`, the root component. GUIDs check. LF kept. The four hand-restored icon overrides may be rewritten to 0 by Unity on a later save (noise, not this change).
- `EligibleInMission`: set in `BeginLevel`/`SetEligible(true)`, cleared by `DropMission` on a mission key change, not saved; reset via `ResetPlayModeState`. Edge: if the only both-sisters level was lost and the replay lacks both, the row still shows (counts exclude the lost attempt).
- Faded: the row reads the last faded value, so **The Trail's end will show no row once C4's fade is in** (intended).
- No core edits, no private IDs. Single commit fine.
- THJ's look still needed (placement under `StatsPanel`, icon, sizing).
