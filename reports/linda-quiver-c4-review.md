# Review: Linda's Quiver C4

Reviewer: miso-reviewer, 2026-10-27. The coordinator saved this file. The code was not compiled (the editor was open).

**Verdict: FIX**

Clean:
- No definite compile error found; every API was checked against its signature.
- LF, no BOM, no private IDs, unique GUIDs.
- No AI-thread work and no new statics.
- The Encore title doesn't move `AIRegressionTest`.

## Must fix
1. **Commit units 1 and 2 don't build in order.** `QuiverAimPresenter:218` uses `arrow.Mode` from `QuiverArrow.cs:31`, and unit 1 needs `QuiverReturnKind` and `NoteArrowIcon` from `LindaQuiver.cs`. Merge them.

## Should fix
1. **`QuiverReturnCue.cs:194, 240`:** cues and flashes freeze when Linda is deactivated at death. Destroy them in `OnDisable`.
2. **`QuiverReturnCue.cs:234`:** the `FindFirstObjectByType` lookup for the Mark flash is fragile. Filter to a live catcher in Linda's faction.
3. **`UnitPanelUI.RoleBadge.cs:79-82`:** the `EmptyQuiver` tooltip still says "Shift shows them". Skip that line.
4. **Dead code:**
   - `ArrowIcon` and `NoteArrowIcon` are never read.
   - `QuiverPipRules.ZoneShown` is tested but unused.
   - The `HidesRoleZone` comment claims a gameplay effect it doesn't have.
5. **`ClosedField_RefusesALanding...`** can't fail (it passes a null cell). Use a real `GridCell`, or rename it.
6. **`[PLACEHOLDER]` handling:**
   - The Encore tooltip shows the tag. Strip it in `AbilitiesBarHUDUI.cs:194`.
   - Tag the invented strings (badge line, "Linda has no arrows", "Quiver full", "+N arrows (N left)").
7. **`GroundedArrowField.cs:277`:** the badge and the icon share sorting order 50. Order them.
8. **`QuiverAimPresenter.cs:307`:** it allocates a list every frame. When `landing` is null, `CollectPreviewPathHits` also re-runs every frame. Fix both.

## Notes
- **Move-preview presenter:** safe while idle. Before the core hook:
  - move `IMovePreviewPathSource` into `Core/Interactions`, so Core doesn't depend on Linda's folder;
  - check that `_previewPath[0]` is the mover's cell.
- **`RoleZonePresenter` (Core):** it now imports Linda's namespace, a Core → feature dependency. There is no behaviour change for other units.
- **Follow zone:** the move preview's follow zone hides at 0 arrows, even on a path that would pick some up.
- **D-258 return path:** it can't double count.
- **Timing:** the "+1" cue shows when the toss starts, not when it arrives.
