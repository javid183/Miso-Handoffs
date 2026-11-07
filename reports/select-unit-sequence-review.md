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

## Re-review after the preferred-unit rework: **APPROVE**

Read from the code; never played. One should-fix: the doc comment at `PlayerController.ScriptedSelection.cs:16`.

- With nothing stored, `AutoSelectUnit` is unchanged. With a unit stored there's one fewer `Random` draw, and nothing depends on it.
- The preference can't leak: `EndTurn` clears it (`PlayerController.cs:247`), `Take` clears on every use, and each level gets a new controller (`Faction.cs:72-76`).
- Stored at the last step because `PlayPending` holds the controller busy: holds. `RestartTurn` runs before the step while `ShowHUD` is non-instant; skip doesn't collapse `ShowHUD`.
- On the arrival path the preference is used before the player can act. Elsewhere a mid-action step can linger and replace one random pick, cost-free, gone at `EndTurn`; disclosed in the class comment.
- `Clear` and `Take` call sites have no automated test. Play steps that matter most: last-AP kill and hold-to-skip.

`__CameraStartTest`: not caused by this change. `GridToLevelCameraStartTests.cs:28-29` ignores `DeleteAsset`'s result, so a refused delete passes silently; cause of the refusal not established. Next run of the class should clear it. Separate task if it recurs: log the failed delete. Don't stage the folder.

Line endings: the repo stores these as LF (`text eol=lf`); new CRLF files normalize on `git add`.
