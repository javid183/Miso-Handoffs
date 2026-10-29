# Review: role prompt destroyed-target lock (core)

Reviewer: miso-reviewer, 2026-10-29. Saved by the coordinator.

**Verdict: FIX** (one must-fix, sent back)

## Must fix

- `UISpotlightHandler.cs:123` reads `target.position` every frame. A target destroyed after it got its spotlight (the split worm, during the execution visual) throws every frame and freezes the mask.
- Fix: skip destroyed targets and pack the arrays.

## Verified

- No compile errors were found by reading. Nothing switches on `FactionRoleQTEOutcome`.
- Every path after the press releases the flow exactly once: all targets gone, gone before activation, owner gone.
- `TargetsGone` never silences.
- **Arrows:** no arrow is spent for a Watch that was skipped. The only `onFamilyRoleOutcome` listener is `RoleBarkPresenter`; the quiver spends on Watch activation.
- **Living checks:**
  - destroyed objects, dead units and revive/stash deaths all fail the check;
  - a split worm fails it from `DiePermanently` onward;
  - a downed unit still counts as living (harmless).
- **Camera:** normal focus is unchanged. "Nothing to frame" returns before any state is set.
- **Hygiene:**
  - line endings and BOM kept;
  - no new statics, no private IDs;
  - the `.meta` GUID is valid and unique.

## Notes

- On a `TargetsGone` skip, the role unit still shows its execute bark, because the outcome event says "pressed". Cosmetic; THJ's call.
- Already there before this change:
  - the `PlayerController.ActivateFactionRole` override ignores `onCompletion`;
  - `UISpotlightHandler.Update` allocates two `Vector4[16]` arrays per frame.
