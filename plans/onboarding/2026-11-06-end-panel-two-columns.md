# End-of-level panel: two columns, room for more objectives

Size: M    Tier: 2 (layout chosen by THJ on 2026-11-06)    Assigned to: miso-implementer (opus: prefab plus scene overrides)
Branch: all
Status: approved

## Why

THJ's screenshot of `GB_m4-mark`'s win: six objective rows overflow the frame and run under the Close button. Three rows are blank (turn-cap objectives with no display text). The panel has a fixed aspect ratio, about 80% of screen height is already used, and there's plenty of spare width.

## Goal

The panel shows stats and resources on the left and objectives on the right, with Close below the frame, and never overflows however many objectives a level has.

## Acceptance criteria

- [ ] Layout at 1920x1080 (and it holds at 16:10): left column has the stat rows and collected resources; right column has the Objectives title and list. Title banner on top. The Close button doesn't cover any content.
- [ ] 8 rows fit with no scrolling; beyond that only the list scrolls, with a visible scrollbar, by mouse wheel and drag. The list resets to the top each time the panel opens.
- [ ] A long objective text doesn't run into its Success or Fail label (wrap or truncate, whichever the row prefab handles best; report which).
- [ ] An objective with empty or whitespace text gets no row. If none has text, the Objectives title and list are hidden. Logic in a small public static method with EditMode tests. Win and defeat both use it.
- [ ] All three instances in `CombatLevelContainerScene` (`missionEndPanel`, `levelWonPanel`, `levelLostPanel`) look right, including any that hide their stats: if the left column is empty the objectives take the frame, centered, with no hole on the left.
- [ ] The scene diff contains only the three panels. Screenshots of each with 3 and 12 rows go in the report (a temporary test harness is fine; don't commit it).
- [ ] `MissionEndPanelUI` keeps its serialized references wired; no missing references in the console. All tests pass except the known AI baseline and the 10 known `HearthMemoryMarkTests` layout reds.

## Scope

In: `Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/` (`SessionEndPanel.prefab`, `ObjectiveItem.prefab` if needed), `Core/UI/Runtime/SessionEndPanel/MissionEndPanelUI.cs`, the three instances' overrides in `Scenes/CombatLevelContainerScene.unity`, a new test file.

Out: `CombatLevelUIManager.cs` (core). What counts as Success or Fail: every win objective is marked Success today, including unmet alternatives; the coordinator flags this to THJ separately, **don't change it**. Stat values, texts, fonts, art. `PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font (THJ's uncommitted changes: never touch or save them).

## Touches

Systems: end-of-level UI (not core).
USPs: none.
Docs: coordinator updates status, decisions, build log.

## Approach

1. **Read first:** prefab tree today: `Background` 500x707, `AspectRatioFitter`, `VerticalLayoutGroup` with 150 top padding; `StatsPanel`; nested resources bar; `Objectives` (fixed 120 tall, rows added under it); `CloseBtn`; canvas reference 1920x1080, match height. The scene has 526 lines mentioning this prefab, with many `m_SizeDelta` and `m_AnchoredPosition` overrides on the three instances; **read them first**. Stale layout overrides will beat your prefab values, so revert those that conflict, and keep any deliberate ones (title text, close text, hidden stats).
2. Build the layout with an editor script or the Unity tools, not hand-written YAML. Keep existing GameObjects and fileIDs where you can (reparent rather than recreate) so overrides and references survive. Remove the `AspectRatioFitter`; check the frame sprite is sliced and stretches cleanly.
3. `objectivesParent` must become the ScrollRect's content so `AddObjectives` keeps working; rows have a 30 height. Reference code: `MissionEndPanelUI.AddObjectives`.
4. Save the scene with only the needed changes; the editor is open and THJ works in it, so stop and report if Play mode is on or the scene has unsaved changes you didn't make.

## Risks

- Scene and prefab: biggest risk. Report `git diff --stat` for the scene; a large unrelated diff is a failure.
- Nothing new is static. No save data. No AI.
- Other branches need this when merged: the report says so.

## Gates

Compile / tests / review / play check by THJ: yes (win Memory 4, lose once, finish a mission if handy; the panel is on M2's win path, so gate 6 applies) / docs: status, decisions, build log.
