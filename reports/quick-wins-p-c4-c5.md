# Report: quick-wins P, C4 (banner side) and C5 (end-panel delay field)

Plan: `plans/2026-10-22-quick-wins-p-pace-tech.md`. Nothing staged or committed. Play mode was not entered; no scene/prefab edited; no save reset.

## Proposed commits

### Commit 1 (C4, not core): banner side option
- `miso/Assets/_Project/Features/UI/Panels/Scripts/PhaseVisualsUI.cs` (modified, LF, no BOM kept; +24 lines)
- `miso/Assets/_Project/Features/UI/Panels/Scripts/Editor/PhaseVisualsMirrorTests.cs` (new, 31 lines, UTF-8 BOM like TurnStartPauseTests) + `.cs.meta`
- `miso/Assets/_Project/Features/UI/Panels/Scripts/Editor.meta` (new folder meta, Unity-generated)

What: serialized `side` (`BannerSide` Left/Right, default Right, tooltip). In `Awake`, only on Left, mirrors the root's `anchorMin.x`, `anchorMax.x`, `pivot.x` (x -> 1-x) and negates x of the current `anchoredPosition`, `shownAnchoredPosition`, `hiddenAnchoredPosition`. Done once in `Awake`; `UpdateValues`/`PlaySequence`/`HideInstant` just read the (now mirrored) fields. Content not flipped. Pure helper `public static Vector2 MirrorX(Vector2, float axisSum)` (1 for anchors/pivot, 0 for positions). Right = no change.

Tests: 3 new EditMode tests (anchor/pivot flip, position negation keeps y, double mirror restores) all pass.

### Commit 2 (C5, core): end-panel delay field
- `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs` (modified, LF, BOM kept; +4/-1)

What: `[SerializeField, Min(0f), Tooltip(...)] endLevelDelayBeforeEndPanel = 0.25f` after `endLevelDelayAfterHudHide`; used in place of the hard-coded `1` in the `ExecuteWithDelay(... EndLevel ...)` call. Behaviour change by design: default 0.25 s instead of 1 s (existing scene instances without the serialized value pick up 0.25 via the initialiser; if the scene already has a serialized value it would not, but this field is new so it does).

## Results
- Compile: via Unity MCP, refresh + recompile OK; console shows only pre-existing warnings, no errors.
- EditMode: 525 total, 524 passed, 1 failed = known `AIRegressionTest.Baseline_MatchesCurrentAI` (untouched). The new mirror tests pass (also run alone: 3/3).
- Not verified in play: slide direction and end-menu timing.

## How to see it
- C4: select the PhaseVisuals instance in `CombatLevelContainerScene`, set `Side` to Left, play a combat; the turn banner slides in from the left edge, 16 px from it, same height and timing; Right is unchanged.
- C5: finish a level that has an end dialog; after the last line the menu should appear about 0.75 s later (0.5 s dialogue hide + 0.25 s). Tune `End Level Delay Before End Panel` on the CombatLevelRunHandler in the Inspector.

## Risks and loose ends
- C4: with Left, the root's current `anchoredPosition` is mirrored at Awake; if some other script repositions the banner before Awake, that isn't covered (none seen).
- AI regression output prints as before (35 failures, known red).
