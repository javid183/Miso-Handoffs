# Review: onboarding C3b segment 2 (Lucy) + untag Linda's text

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-01. Report: `reports/onboarding-c3b-seg2.md`.

**Verdict: FIX** (both must-fixes are commit grouping, not code)

## Must fix

1. `GB_m1-linda.prefab`'s whole diff is reimport noise (`animationEvents` overrides); not in commit 1.
2. `HearthMemoryWiring.Linda.cs` can't be split by hunk (hunk at line 27 mixes untag and shared-helper lines). Commit 1 takes the whole file (the helpers compile alone and are unused until the Lucy script); commit 2 = Lucy files, `Memory2Lucy/**`, `GB_m2-lucy`.

## Should fix

1. `HearthMemoryWiring.Lucy.cs:75-83`: HUD shows stage 2's lines with initial values during the interruption (`SetObjectives` runs before `WaitThenEvaluateNewStage`). Hide HUD after disabling input, show after enabling.
2. `HearthMemoryWiring.Lucy.cs:74`: camera back focuses Lucy's cell (0.75, 1.25), not the whole-level centre; may push room 2 off screen.

## Notes

- Stage 1 fires at player turn 2 start (cap) or one frame after a death (usually player turn; enemy turn if a Claw dies there). On the enemy turn the AI waits for the sequence, and the revealed three act that turn (fresh `ToPlayUnits` snapshot). Matches spec.
- `CameraSequence` sets all faction turn flags off/on; each faction's `StartTurn`/`EndTurn` resets them, nothing stays wrong past the turn. Skip is safe; input always restored.
- AI worker overlap on reveal: same exposure as spawns; THJ's restore-race logging would catch it. Revealed Claws show no predicted-target markers until the next ability or turn start.
- Stage 2 can't win before the reveal; hidden units aren't in `AllUnits`. Turn cap counts from stage 2's start: ends at turn 4 when stage 1 ends on turn 1, turn 5 if stage 1 ended by its cap.
- Start: zero-duration fade then 0.8 s fade-in; whether the grid flashes first is a play check.
- Wiring idempotent, editor-only, no statics, metas present, no private IDs, no `[PLACEHOLDER]` left; Watch image guid resolves to `Tut-FR-1.png`. Tests check data, not runtime.
