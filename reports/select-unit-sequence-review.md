# Review: `SelectUnitSequence` (2026-11-06)

Reviewer verdict: **ESCALATE** to THJ. Read from the code; nothing played. The reviewer can't write files, so the coordinator saved this condensed copy.

## Must decide

The follow-up coroutine gets Mark selected, but about 3 runs in 4 the turn start's random pick first runs on another hero: a full `Switch` animation (`GUnit.cs:936`; deselecting doesn't stop it), a possible `UnitSelected` bark (`BarkManager.cs:241`; gating not decoded), the unit panel filled for that hero, and a camera focus toward them.

Recommended fix, core: a one-shot preferred unit. `TrySelectUnit` stores the unit when the controller is busy; `AutoSelectUnit` (`PlayerController.cs:479`) uses it if alive and in `toPlayUnits`, otherwise the random pick; `EndTurn` clears it. Removes the coroutine, frame counting, the public `GetScriptedSelectDecision`, and both should-fixes. No behavior change when nothing is stored.

## Should fix, only if the coroutine stays

1. No level-end guard (`PlayerController.ScriptedSelection.cs:17`): add `&& !handler.IsLevelEnded`.
2. The wait can overwrite the player's choice (`SelectUnitSequence.cs:67-72`): give up if the controller goes busy again with `PhaseData.ActiveUnit` set.

## Verified

Turn ending and unit dying are safe. No statics, no private IDs, CRLF no BOM matching neighbours. Asset GUID and script match. The step is last of 12, after ResetTurn, CameraOnMark, EnablePlayerInput and ShowHUD. `PlayerController`'s existing behavior unchanged: `partial` only. No AI impact.

## Notes

- Not seen in play. Tests cover the rules and failure warnings, not the select path.
- If a Claw dies on an enemy turn, the reset does nothing and the step only warns, so Mark isn't selected.
- Hold-to-skip: camera steps collapse; if `RestartTurn` ran after a direct select, Mark would lose it silently. Check in play.
- `HearthMemoryWiring.Mark.Sequences.cs` omits this step; rerunning it would drop the selection (tool's menu entry is retired).
