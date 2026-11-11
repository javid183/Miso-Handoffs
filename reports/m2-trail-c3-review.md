# Review: M2 Trail C3 (challenge rebuild)

Reviewer: `miso-reviewer` (read-only; filed by the coordinator from its hand-back, 2026-11-11).
Plan: `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` (C3). Implementer report: `reports/m2-trail-c3.md`. Suite: `reports/m2-trail-c3-verify.md` (1875/1876, known AI red only).

**Verdict: FIX** (two small must-fixes; Blood panel layout is THJ's call).

## Checked and fine

- Layouts, cells, deploy slots, all-alert, hidden groups on all four levels match the revision-2 blocks; factors on the Tracks only (hidden pack included); Duo lock and no filler unchanged.
- Arrival order (input off → camera → reveal → bark → camera back → input on) in both arrival assets and asserted.
- Black Claw on the Tracks at 7,2; Pile Archer and Tracks Encore stage gone.
- `TurnReachedLOCondition` turn = 1 is right (counts from its first check, `CombatLevelRunHandler.cs:196-199`; the phase banner holds input, D-142).
- Blood can't lock or win wrongly: dead heroes don't occupy cells; two down → hidden kill-all still wins; killing all visible enemies on turn 1 still waits for the turn-2 pair; the tile goal can't be met on turn 1; empty-text win objectives don't list on the win panel.
- Reveal on an occupied tile shifts to the nearest free cell.
- No core/runtime/AI changes, no new statics, no private IDs, LF/no BOM kept, file list matches the diff.

## Must fix

1. Commit grouping: wiring, generated assets and tests only work together → one commit (coordinator: adopted).
2. Tests compare the wiring's own constants with the serialized values, so a wrong constant passes: assert literals instead — `turn == 1` (comment: counts from the first check), Blood end tiles 18,1 / 19,1 / 19,0 with target 2, Pile search tiles 3,3 / 6,3.

## Should fix

1. Arrival "camera back" returns to the family's start point (stale on the 20-wide Blood level). Option: end the arrival with `SelectUnitSequence` on Linda (focuses the camera; logs and continues if she's dead).
2. Black Claw caption order: "His tracks." → caption → pick's "That big one leads them." → close-up. Caption last would sit right before the close-up. THJ / designer call.
3. `CellPoint(GameObject root, GUnit unit)` (`SearchWiring.Trail.Arrivals.cs:72`): `root` unused.

## Blood panel trade-off (THJ)

The blank stage-2 goal still builds a row: at turn 2 the panel opens and plays the new-line sound for a blank line, during the arrival camera. Options: (a) accept; (b) hide the stage-2 goal (no row, end tiles stop glowing from turn 2); (c) same text (line shows twice); (d) a short useful second line instead of blank (data + narrative line); (e) runtime filter skipping empty-text entries (`ObjectivesPanelUI` not core, `LevelObjectives` core → THJ's OK, own small plan).

## Notes

- Doc gap was Blood only (the committed Tracks block already had the `c`s); fixed in the design doc since.
- On a kill-all win, the Blood outro still shows the end tiles and Lucy's line with the family elsewhere: play check.
- Turn 2 stacks the phase banner, the arrival camera and the panel opening: play check.
- Idempotence not re-verified read-only; code is deterministic.
