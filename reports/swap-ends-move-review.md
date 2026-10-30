# Review: swap ends a move

Reviewer: miso-reviewer, 2026-10-29 (saved by the coordinator; the reviewer has no write tool). Plan `plans/2026-10-29-swap-ends-move.md`.

**Verdict: APPROVE.** Must fix: none. Should fix: none.

Notes:
1. Guard and timing correct: both events after both plugs, nothing on the `CanOccupy` bail-out; same order as the pusher (plug, event while `IsInProgress`, `WaitForEndOfFrame`, done).
2. The swap is a normal action, so Linda's Watch waits for `ActionsProgressComplete` (wait list), as with the push.
3. No listener throws: `EnemyAlertTracker` (null and worker-thread checks, then `CheckSight`), John's CommandShieldDash (returns unless a Command is in flight), Papa's Shelter (idempotent; swapping Lucy or John now refreshes it, a real small fix), presenters set a dirty flag. AI doesn't subscribe; the golden master shouldn't move.
4. Watch can fire twice on one swap (`oncePerPhase` 0, wait list keeps the second entry). THJ allowed it (D-323).
5. Linda swapped with an enemy can trigger Watch on it (bundle target skips the "targets Linda" check). THJ allowed it (D-323).
6. BOM and LF kept, no trailing newline as before, no private IDs.
7. Loose end: the header comment in `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.Events.cs` (lines 18-21) lists what raises `unitEndMoving` and doesn't mention the swap. Fix on a later touch of that file.
8. Not verified: compile, EditMode (expect only the known red, CHECKS 710 FAILURES 39), THJ's play check.
9. The single core commit is correct.
