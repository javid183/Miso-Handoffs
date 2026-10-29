# Quiver feedback pass: deeper feedback in the one layer

Size: M    Tier: 2 (presentation inside THJ's directions D-301), plus THJ's balance call D-302    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all, built on `thj/linda-quiver` (after `79ca381e8`)
Status: dispatched 2026-10-28

## Why

THJ's play check of the strip-down (2026-10-28): the single layer works, but it should give **clearer, deeper feedback in the same places**, not new text in new places (D-294, D-295). The HUD quiver he built by hand replaces the code-built one.

## Changes (THJ's seven points)

1. **Shift shows her arrows.** While Left Shift's status view is up (`ShowStatsHoverPreview`, the mini health bar giving way to the stat panel, `UnitMiniHealthBar`), Linda's arrows under her feet must still read. Find out why they don't today: hidden, covered by the panel, or sorted under it. Make them show with the Shift view, either above it or as part of it, without touching core code. If only core can do it, STOP and report.
2. **Empty state under her feet.** At 0 arrows, the row under her feet shows **one crossed-out arrow** (the arrow sprite with a thin slash over it, drawn by a second sprite or a rotated thin line, muted red), instead of four dark outlines. With 1 or more arrows the row is unchanged.
3. **HUD quiver feedback** (THJ's `LindaQuiver.prefab`, point 6). All tweens use DOTween, are short (0.12 to 0.3 s) and are killed or completed on hide and destroy:
   - **Empty:** the body and rim tint to a muted red/grey (or an outline if the art makes that cleaner) while the quiver is empty; back to normal when she has an arrow.
   - **Primary ability armed:** while her primary ability (slot 1, the bow) is hovered on the bar or selected (key 1 or a click), the quiver scales up a little (about 1.12) and back down when that ends.
   - **Primary with no arrows:** the same trigger at 0 arrows plays a bigger punch (about 1.3, then back) instead, as a "no arrows" signal. It plays once per hover or press, not in a loop.
   - **Arrows gained** (pickup, catch, Encore): each newly shown arrow glows briefly (a brighten-and-fade on its image, or a short scale pop), and the quiver gives a light pulse.
4. **Encore lines:** thinner (about half today's `LineWidth`) and partly transparent (alpha about 0.6). They also get the **moving shine** the enemy threat line has (the threat line on `UnitBase.prefab`, `GUnit.threatIndicatorLine`, shines from the enemy to the player in a loop). Reuse that same material and shader, set on the Encore lines through a serialized reference (on `LindaQuiver` / Linda's prefab), so the shine runs **from each arrow stack to Linda**. If the shine comes from code rather than the material, mirror it in the quiver folder without changing core.
5. **Encore AP cost 2** (D-302). Data only: the cost field on `Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset`. Check that the button, the tooltip and the AP preview show 2, and that the known-red `AIRegressionTest` message is unchanged.
6. **Use THJ's HUD prefab.** `Features/UI/Panels/Prefabs/UI/HUD/LindaQuiver.prefab` (body, rim, 4 arrows, placed by hand) is already instanced in `CharacterHUD.prefab` (THJ's uncommitted edit, part of this change).
   - Delete the code that builds the HUD quiver at run time. `UnitPanelUI.Quiver.cs` drives the instance instead: shown only on Linda's panel, its arrow count from the quiver.
   - `QuiverUI.cs` (THJ's): keep it as the prefab's view and put the point 3 feedback there. Clean it:
     - remove `using NUnit.Framework;`, which breaks player builds;
     - put it in the panel scripts' namespace (the script GUID stays, so the prefab reference holds);
     - add serialized references to the body and rim for the tint;
     - keep his `ShowArrowCharges(int)`.
   - Remove anything in `QuiverHudRules` / `QuiverSprites` / `LindaQuiver` that only served the code-built HUD, along with its tests. Keep the rules that still apply.
   - Don't move or resize his objects. His layout is the layout.
7. **Grounded arrows:**
   - Shift the icon a little to the right within the tile (about 0.15 to 0.2 of a cell).
   - Draw **one** arrow per stack instead of overlapping ones. When the stack holds 2 or more, show a small `xN` beside it (a small world-space TMP, using the font the existing UI uses).
   - Keep the subtle dark tint under a living enemy. Keep everything sorted below every HP bar.
   - The ghost arrow while aiming moves the same way, so it still matches.

## Acceptance

- [ ] Holding Shift with Linda on the board: her arrow row is visible and correct.
- [ ] At 0 arrows the row under her feet shows a single crossed arrow; with arrows it's unchanged.
- [ ] The HUD uses `LindaQuiver.prefab`'s objects (no run-time HUD quiver building remains). It shows the exact count and appears only on Linda's panel.
- [ ] The HUD tints when empty, scales up on primary hover or select, punches at 0 arrows, and glows the new arrows on gain. No tween survives a hide or panel switch (no stuck scale or colour).
- [ ] Encore lines are thinner, partly transparent, and show the threat line's moving shine from stack to Linda.
- [ ] Encore costs 2 AP everywhere it's shown.
- [ ] Grounded arrows: one icon, nudged right, with a small `xN` for N ≥ 2. The tint is kept, it never covers an HP bar, and the ghost matches.
- [ ] `QuiverUI.cs` has no NUnit import and lives in a namespace.
- [ ] EditMode passes, with only the known red failing. Tests cover the pure parts: the empty-row rule, the `xN` label rule (none at 1, `x2` at 2), the HUD feedback trigger rules (armed vs punch, gain detection) and the Encore cost value.

## Constraints

- No core code (`tech/core-systems.md`); Core never imports Linda (D-272). Reading core state (Shift held, the selected ability, hover) is fine.
- Complexity budget (D-295): no new elements beyond these. The only text added is the `xN`, which THJ asked for.
- No statics without a `PlayModeStaticReset` hook. No per-frame allocations. Every DOTween is killed on disable or destroy.
- Lessons from D-280 to D-282: sort below HP bars, `QuiverLevelAccess`, no root objects created in `Start`.
- Keep line endings and BOM. No private IDs in code.
- Don't touch THJ's unrelated local edits: `GlobalSettings.asset` (intro/outro off) and `CombatLevelContainerScene.unity`.

## Commit units (the implementer lists files per unit in the report)

1. Encore AP cost 2 (data, plus the test).
2. HUD: THJ's prefab, `QuiverUI`, `CharacterHUD.prefab`, the panel wiring, the feedback, and removal of the code-built HUD.
3. Under her feet: the Shift fix and the empty crossed arrow.
4. Grounded arrows: a single icon with `xN`, nudged right, and the ghost.
5. Encore lines: thinner and transparent, with the shine.

## Gates

- Unity is closed: the implementer runs EditMode on the command line (CLAUDE.md path).
- Review.
- THJ plays, then the commits.

## Commit log

THJ play-checked 2026-10-29. `661890964` Encore 2 AP; `51954e2c6` HUD prefab + feedback; `45cb29d76` arrow row on panel + empty; `d8651dd3c` single arrow + xN; `7c6f5e57c` Encore lines.
