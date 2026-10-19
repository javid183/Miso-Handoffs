# Review: role-zone-unit-sprites C1 (code)

Plan: `plans/2026-10-19-role-zone-unit-sprites.md` (D-075). Report: `reports/role-zone-unit-sprites-c1.md`. Branch: thj/fr-readability; uncommitted working tree compared against HEAD. Reviewer: miso-reviewer (saved by the coordinator; the reviewer has no write tool).

## Verdict: APPROVE

## Must fix

None.

## Should fix (optional)

1. `GridCell.RoleZone.cs` line 171 puts the sprite's pivot at the quadrant centre. All five sprites in use have a centre pivot (0.5, 0.5), so this is correct today. A future icon with another pivot would sit off-centre. One-line fix: subtract `(Vector2)sprite.bounds.center * scale`, or say in the tooltip that the pivot must be Center.

## Notes

- **Additive only on the core files: met.** `FactionRoleHandlerBase` gains two new fields and two accessors, with explicit enum values 0 to 3. `SetRoleZone` gains two parameters, has two callers, removal still runs locally first, and the origin redirect forwards the sprite and slot.
- **Quadrant fit: correct.** It uses a uniform scale, so the aspect is kept. The position depends only on the slot, so a lone zone stays in its corner. The footprint extension gives the same world size as before.
- **Renderer reuse and cleanup: correct.** Every refit resets sprite, colour, position and scale. The layer set's lists stay aligned, and it compares sprites with `ReferenceEquals`.
- **No new statics; main thread only.** The AI is not involved.
- **BOM and LF kept.** New files have no BOM and minimal metas.
- **Tests:** the fit geometry, and the per-owner sprite and slot entries in the layer set. Rendering itself is left to the play check.
- **Follow-zone draw order:** same sprite, slot and RGB, only the alpha differs, so either order gives the same colour. No fix is needed. The plan's Risks line saying the follow zone draws on top is wrong, because `int.MinValue` sorts first. The coordinator has corrected it.
- **Separate warning set:** agreed. Sharing the set would hide the "could not give its role zone" warning.
- **Commit:** one commit is justified by the coupled signatures. An optional split that still compiles: `RoleZoneSlot.cs` + `.meta` + `FactionRoleHandlerBase.cs` first, then the rest.
- **Risks:** no AI, save or other-branch impact. How the downscaled icons look is a play-check item.
