# Spike: Mark's Catch & Return with a QTE (D-257)

Explore, read-only, 2026-10-27. The coordinator saved this summary.

**Finding:** it can be built with no core code. On contact, `ProjectileCatchAndReturn` sets `Projectile.enabled = false` on Linda's arrow. `Update` is the only thing that moves the arrow, so it freezes at Mark, keeping its hit count, falloff, target and quiver hold. Linda's ability stays in progress while the arrow is frozen.

- **Decline:** set `enabled = true` and release the hold. The same arrow carries on with its remaining range and falloff, and lands normally.
- **Press:** return the arrow to the quiver and play the catch animation; at `applyFrame` 3 (about 0.3 s), hide the original and activate the return clone, wiring `clone.onDestroy` to `original.Dispose`. Linda's action then stays open until the return flight ends. Add an unscaled fallback timer (about 1 s) in case the animation never reaches `Apply`.
- **QTE failed to start, or `OnDisable`:** re-enable the arrow and release it.
- **Do not** disable the collider: re-enabling it would fire a new trigger and re-open the QTE.

**Today's bugs this fixes:**
- **Double damage:** the original arrow is never stopped (`_pending.Dispose()` is commented out at line 141). With the automatic catch it flies on and damages everything past Mark, while the clone also flies back.
- **Return overshoot:** the return clone flies `Radius` cells, so it overshoots past Linda. Fix it with a `LindaAttackArrow` variant that has `travelEntireRadius: 0`, kept out of Mark's whitelist.

**Rejected options:**
- **Time-scale pause (b):** it covers only the QTE window, and it conflicts with the hit slow-mo and the reactive interrupt. Use it only as an optional bullet-time look, through `TimeScaleCache`.
- **Starting the QTE early (c):** arrival time is hard to predict, and the window is longer than many shots.
- **Re-launching a copy on a decline (d):** it needs core changes, because the hit count and remaining range are private.

**Size:** S–M, about 60–100 lines in `ProjectileCatchAndReturn.cs`, plus `triggerWithQTE: 1` on `Unit_Mark.prefab`.

**Risks:**
- The arrow freezes at the edge of Mark's collider.
- Only one QTE can run at a time, and only one arrow is held per Mark.
- The return flight re-hits enemies between them, with falloff restarting at 1.0; check balance.
- Triggers still reach a disabled component: confirm in play.
- The QTE window length is approximate, because the scene values weren't read.
