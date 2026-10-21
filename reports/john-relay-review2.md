# John relay re-review after revision 1 (miso-reviewer, 2026-10-21; saved by the coordinator)

Verdict: **APPROVE**

## Should fix (minor)

1. **`JohnFactionRoleHandler.ApplyReductionUntilCompleted`:** after an aborted run, the completion handler stays attached until the attacker's next `PhaseTick`. A rerun of the same ability, such as a second Masher answer in the same phase, could remove `JFR_DR` that a newer relay still holds. Fix with a per-run token, or log it as a known edge.
2. **`PlayerController.EndTurnAvailable`:** the query also schedules a refresh. It's guarded, so it can't loop or stall; rename it or comment it so nobody uses it in a turn-flow wait.

## Checked

- **D-126:** sound. Moving effects (Transporter, DashAttack, Swapper, Command, ghost destination) keep their cell targets, and no slam is misclassified.
- **D-127:** the hold logic is correct, and removal by id leaves Shield's DR alone. The tests are real.
- **End Turn gate:** minimal, can't stall.
- **Null checks, `IsAreaAttack` tests, level-end clear:** all present.
- **No IDs** in any added line.
- **Line endings:** no churn (CRLF on disk, LF in the index).
- **Commits:** J-B builds alone with the staged patch, and J3 is independent. Keep J-B separate: it's the risky core change.

## Notes

1. **For THJ.** `Unit_John.prefab` (~:2199-2204, :2436) already removes `JFR_DR` on John's first HP loss: a persistent `RemoveStatAttributeModifier("Unit, JFR_DR")` on `onValueDecreased`. So in play the reduction ends at his first hit. With overlapping relays, the second relayed hit lands without it, which contradicts D-127's "last completion". Dropping that call is a prefab change outside this plan.
2. **J3 commit proposal:** `CombatLevelUIManager` End Turn behaviour changes, and `PlayerController.EndTurnAvailable` is new and public. Both are a Tier 2 core bugfix (D-128); say so in the proposal, and update `core-systems.md`.
3. **Charges still hit the ally on the destination cell**, with John added as an extra target (accepted under D-126). Put this in the play check so it isn't reported as a bug.
4. **Golden master:** no impact.
