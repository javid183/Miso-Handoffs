# Review: Linda's Quiver C3 (Recall)

Reviewer: miso-reviewer, 2026-10-26. The coordinator saved this file.

**Verdict: APPROVE** (no must-fix)

Checked:
- Arithmetic and conservation.
- Level and thread safety of `HasGroundedArrows`.
- Cooldown 2: traced, she can't use it on her next turn and can on the one after.
- 1 AP: set the same way as her other abilities.
- The turn hold: `minimumDuration` 0.5 covers the 0.45 s flight, and a wiring test guards it.
- Flight cleanup on level end and on Linda's death.
- Function Caller wiring.
- Prefab array: 9 → 10, nothing reordered.
- Saves: unaffected.
- No core change. LF, no BOM, no private IDs.
- The commit grouping builds in order.

## Should fix
1. `RecallRules.QuiverAfter` isn't used by game code. Delete it, or assert it against `Resolve`.
2. `GroundedCount_ReadsZeroOnceTheFieldIsClosed` leaves the static pointing at a destroyed object, and adds an object to the open scene. Add a test-only reset and call it in `finally`.
3. Recall's prefab entry copies a Duo's `disableTargetCellIndication: 1`. Decide it on purpose.

## Notes
- Recall is usable with a full quiver and grounded arrows. That can't happen today, but it matters for the Fireside +1.
- The `[PLACEHOLDER]` tag will show in the tooltip; the Dark Shaman heal already does the same.
- Event order: the quiver's change event fires before the stacks redraw. C4 presenters should listen to the field's event.
- The script GUIDs look hand-typed, but they are unique.
