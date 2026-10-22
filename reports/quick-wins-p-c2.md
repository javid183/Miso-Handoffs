# Report: quick-wins-p chunk C2 (EndLevel waits as fields)

Plan: `claude-handoff/plans/2026-10-22-quick-wins-p-pace-tech.md` section C2 (D-107, plan approved as D-141).

## Diff summary
Only `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs` (core file, behaviour-neutral apart from the intended timing):
- Added `[SerializeField, Min(0f), Tooltip(...)] private float endLevelDelayBeforeHudHide = 0.25f;` and `endLevelDelayAfterHudHide = 0.25f;` right after `timeBetweenFactionTurns`.
- In `EndLevel`, the two `WaitForSeconds(0.5f)` around `HideHUD()` now use those fields.
- Line endings/BOM preserved: BOM present, 0 CR (LF), checked after edit.

## Scene serialization
Handler GUID 29fbeae1d38e49fd93fdc4a0a9bff8a8 is used in `Scenes/CombatLevelContainerScene.unity` (line 1439), `Scenes/DevScenes/TestLevel.unity` (line 1576), `Scenes/DevScenes/SampleScene.unity` and `SampleScene 1.unity`. No prefabs hold it. Where it appears, scenes/prefabs have only `timeBetweenFactionTurns: 0.5` and no `endLevelDelay*` keys (grepped). The two dev SampleScene files have no `timeBetweenFactionTurns` line at all (stale/other component data). Scenes not edited. Unity deserializes missing fields as the C# initialiser (0.25), so behaviour is 0.25 s immediately. On the next save of CombatLevelContainerScene and TestLevel, Unity will write `endLevelDelayBeforeHudHide: 0.25` and `endLevelDelayAfterHudHide: 0.25` into the handler component (scene diff noise of two lines each).

## Compile
Refresh/recompile via Unity MCP succeeded; console shows no errors, only pre-existing warnings (CS0108 on `ResetPlayModeState` etc., none from the new lines).

## EditMode
522 tests: 521 passed, 1 failed = known red `AIRegressionTest.Baseline_MatchesCurrentAI` (untouched). No new tests (two timing values).

## How to see it
Play a level and finish it by win, by defeat, and the mission-complete ending: each reaches its outro/panels about 0.5 s sooner (two waits cut from 0.5 s to 0.25 s). Tune per scene via the handler's inspector fields. Not play-tested (Play mode not entered).

## Proposed commit
1. `CombatLevelRunHandler.cs` alone (core file), message e.g. "feat(combat): level-end waits around the HUD hide are fields, 0.25 s each".

## Risks and loose ends
None. Scenes unchanged; no static state added.
