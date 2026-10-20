# Explore: tether invisible (C8) and missing sword icons on multi-tile enemies (2026-10-20)

**Bug A, tether (regression from C8, a2a19fb46).** The arc is drawn, but:
1. The material borrowed from John's `ThreatLineRenderer` (`M_LineShine`, URP Sprite Unlit, `_BaseColor` dark red 0.5/0/0.063) is multiplied by the vertex colour, so John's orange (0.902, 0.624, 0) ends up near-black (about 0.45, 0, 0). The shine band is frozen at timeScale 0.
2. Default layer order 0 puts it under both endpoint units (sprites are order 1 + 10 × the cell's vertical layer index via `GridPluggableEntity.Plug` L216-219).
3. Width 0.015 and alpha 0.7 make it worse.
Fix: Sprites/Default material (`GetFallbackMaterial()`), keep the head anchor; sort just above both endpoints' sprites (THJ chose that over Overlay, D-088); width about 0.025.

**Bug B, multi-tile sword icons (older than this pass, commit 26e5a517e, Aug 26).** The reach includes the enemy's cells (Unconstrained walkability has no occupancy filter). But `GridCell.SetInAttackRange` (L382-389) redirects every covered cell to `OverlayOrigin` (the anchor), and `FitOverlaysToOccupantFootprint` (L517-552, `_recenterOverlays` L474-476) moves the single icon to the footprint centroid at Default −9, under the boss sprite. The Shift layer does the same (`GridCell.ShiftPreview.cs:77-78`, `_shiftPreviewRoot` L204-218). The override icon isn't moved. Multi-tile enemies: Masher Goblin 2×2, Goblin Queen 1×2, Mountain Deev 3×2.
Fix: per-tile icons (THJ, D-088). Drop the redirect for the attack icon and remove it from `_recenterOverlays`; on the Shift layer apply the attack part locally while the move frame still wraps the footprint, and give `_shiftAttackRenderer` its own parent or cancel the centroid offset. If boss sprites cover the per-tile icons, raise the icon's order on occupied cells.
