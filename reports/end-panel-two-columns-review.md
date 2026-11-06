# Review: two-column end panel (2026-11-06)

Reviewer verdict: **APPROVE**, no must-fix. Read from the code and YAML; nothing run. The reviewer can't write files, so the coordinator saved this condensed copy.

## Should fix

1. **The wheel also zooms the camera behind the panel.** `Player.Scroll` isn't gated by pointer over UI (`PlayerInputController.cs:59`, `CameraHandler.cs:165-169`), and `PlayerController.cs:254` likely sets `Camera | Pause` again after the delayed force end of turn, so a win on the player's turn shows the panel with zoom live. Fix: hold `PlayerInputController.Instance.AddInputLock(this)` while the panel is enabled. Also blocks Pause while it's open.
2. **Fixed 8-row height leaves Won and Lost hollow with few rows** (about 190 of 435 px empty with 3 rows). Nothing broken. THJ's call at the play check; if he dislikes it, size the list to `min(rows, 8) * 30` and fit the frames.
3. `ObjectiveItem.prefab` truncation can be its own commit.

## Verified

- **Scene:** by YAML document against HEAD, only instances `363410393`, `1798532284`, `1992923117` differ. Removed overrides: rect or transform, plus `m_Spacing` and `m_Padding.m_Top` on `Background`'s layout group. No text, active state, sprite, name or `trackedResources` override removed. MissionMap block byte-identical and in HEAD's order; the next save will probably re-sort it, harmless.
- **References:** `levelLostCloseBtnText` and the panels resolve; only the `AspectRatioFitter` was removed.
- **ScrollRect:** content is `objectivesParent`; a test pins it.
- **Rows doubling on reopen can't happen today:** `SetObjectives` is reached only once per scene load (`_levelEnded` guard; restarts reload the container).
- **Empty rows:** win and defeat share the logic. A defeat whose only condition has blank text shows "Mission Failed!" alone; THJ should see it once.
- **Input:** `InputSystemUIInputModule` has the scroll action wired, one tick is about one row. Action asset binding unconfirmed. No gamepad route on this panel, same as before.
- No new statics, no AI code, no core change, line endings kept, no private IDs, no harness left.

## Loose ends, unchanged

Every win objective shows Success. Low contrast on Success and Failed labels. `MainResource_SP` shows a white square in the harness. Other branches need this when merged.
