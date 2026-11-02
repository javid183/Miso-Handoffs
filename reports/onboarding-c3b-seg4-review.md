# Review: onboarding C3b segment 4 (Mark)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-01. Report: `reports/onboarding-c3b-seg4.md`.

**Verdict: APPROVE** (no core change, no statics; the two-commit split builds in order)

## Should fix

1. `GuidedAbilityHint.cs:58-62`: using the hinted ability before `firstTurn` ends the hint (a turn-1 Chained Assault kills the turn-2 pulse). End only once `turn >= firstTurn`, or document it.
2. `HearthMemoryMarkTests.cs:140-164`: stage 2 test should check each condition's faction is Bergsons, no Bergson starts on 6,9 / 7,9 / 8,9, no hidden Claw on them.
3. `HearthMemoryMarkTests.cs:96-99`: assert the stage 1 `LivingUnits` faction is Enemy.

## Notes

- `firstTurn` default 1: segment 3 data unchanged. Three hints on three different buttons.
- Stage 1 cap fires at turn 3 start; all seven dead leaves the Enemy controller, so the revealed pair act next enemy turn (play check).
- Mother's fall: LSB swap to an unpacked rotated copy (collider off, not a unit); re-run wiring after changing the standing mother; overlap with 8,9 is a play check.
- Stage 2: tiles are floor; goal highlight stands in for the cub marker (small deviation); a Bergson already on the tiles when stage 1 ends wins after the scene (unlikely).
- Bloom grant cleared on mission enter/quit; restart logs a refused repeat (upgrade still owned).
- Hand edits intact; one harmless `managedReferences[-2]` override. LF, metas, no private IDs, no tag. Don't stage the Linda/Lucy tests (no content diff) or `GB_m1`.
- Not done: optional stage-1 FTP refill, Home open/close, lines M4-4 to M4-7.
