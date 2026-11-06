# Report: End-of-level panel, two columns, room for more objectives

Plan: plans/onboarding/2026-11-06-end-panel-two-columns.md    Agent: miso-implementer    Branch: thj/onboarding (scope: all)
Outcome: done, pending THJ's play check (real win and defeat, real mouse). Nothing staged or committed.

Decisions built: D-409 (two columns, Close below the frame, list scrolls past about 8 rows), D-410 (empty text gets no row).

Updated after review (`reports/end-panel-two-columns-review.md`, Should fix 1 and 3): the panel now holds an input lock while open, and the commit proposal is split. See "Review fix: input lock" and "`MainResource_SP` white square".

## What changed

- `miso/Assets/_Project/Core/UI/Runtime/SessionEndPanel/MissionEndPanelUI.cs`: new public static `TryGetObjectiveRowText`; new serialized `statsColumn`, `objectivesColumn`, `objectivesScroll`; blank objectives skipped; empty columns hidden; list goes back to the top when the panel fills; player input locked while the panel is enabled. +66/-5.
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/SessionEndPanel.prefab`: frame 1040x520, `AspectRatioFitter` removed; new `Columns` > `StatsColumn` (holds `StatsPanel`, `CollectedResources`) and `Objectives` (reparented, same fileID) > `ObjectivesScroll` > `Viewport` > `Content`, plus a scrollbar; `objectivesParent` now points at `Content`; Close sits 14 below the frame. +810/-110.
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/ObjectiveItem.prefab`: name gets all spare width, no wrap, ellipsis; state label has a fixed 90 width; the two `ContentSizeFitter`s that fought the row's layout group are gone. +6/-36.
- `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`: only the three panel instances (details under the criteria). Numstat +268/-1964 by default, +8/-1704 with `--histogram`, nearly all of it removed stale overrides.
- `miso/Assets/_Project/Core/UI/Editor/MissionEndPanelObjectiveRowTests.cs` and `.meta`: new, 15 test cases (10 row and wiring, 5 input lock), all pass.

`git diff --stat`, default algorithm, for the tracked files:

```
.../Runtime/SessionEndPanel/MissionEndPanelUI.cs   |   71 +-
.../UI/Home/SessionEndPanel/ObjectiveItem.prefab   |   42 +-
.../UI/Home/SessionEndPanel/SessionEndPanel.prefab |  920 +++++++-
.../Scenes/CombatLevelContainerScene.unity         | 2232 +++-----------------
4 files changed, 1150 insertions(+), 2115 deletions(-)
```

`CombatLevelUIManager.cs` is untouched. No core system changed: the panel only calls `PlayerInputController`'s existing public lock methods.

The review fix didn't save or dirty the scene or the prefabs: their stat lines are the same as before it, and the document-by-document compare still shows only the three panel instances, in HEAD's order.

## Acceptance criteria

How each was checked: "tests" = EditMode; "render" = offscreen render of copies of the real scene instances with harness data; "Play" = short Play session with an instance of the prefab, not the scene instances and not a real level.

- [x] **Layout at 1920x1080, holds at 16:10.** Left has stats and resources, right has the Objectives title and list, banner on top; Close is below the frame on all three (measured). Render at both sizes.
- [x] **8 rows fit with no scrolling; beyond that only the list scrolls, with a visible scrollbar.** Play: 8 rows has no bar (viewport 490x240, content 240); 9 rows shows the bar (viewport 470x240, content 270).
- [ ] **Scrolling by real mouse wheel and drag: needs THJ's play check.** The handlers work in Play when called directly: one wheel notch moves one row (30 px, using the scene input module's 6 per tick), dragging the list moves it and clamps at the end, and the scrollbar value moves the list. No physical mouse went through the input module.
- [x] **List resets to the top on open.** `AddObjectives` sets the position to the top. Checked by scrolling and refilling in the render harness, with an empty list on that refill, so it also needs a look in the play check.
- [x] **Long text doesn't reach the state label: truncates.** Font shrinks to the row's existing minimum (15), then an ellipsis. See the second row in any screenshot. Wrapping was rejected because rows are 30 tall.
- [x] **Blank text gets no row; if none has text, title and list are hidden; static method with tests; win and defeat both use it.** `TryGetObjectiveRowText` is covered by tests. Both outcomes go through `AddObjectives`. Each harness run added 2 blank objectives and they got no rows; with no objectives the column is inactive (flag checked, not screenshotted). Only the win and lost display states were rendered, never a real defeat.
- [x] **All three instances look right; hidden stats leave no hole.** Won and Lost hide their stats, so `StatsColumn` turns off and the objectives take the frame, centered. See screenshots.
- [x] **Scene diff contains only the three panels; screenshots with 3 and 12 rows.** A document-by-document compare against HEAD shows 276 documents with the same IDs and order, and exactly 3 changed: `363410393`, `1798532284`, `1992923117`. No large unrelated diff.
- [x] **Serialized references wired, no missing references.** Scene instances: 15 references each, 0 null, 0 missing scripts; `missionEndPanel`, `levelWonPanel`, `levelLostPanel` and `levelLostCloseBtnText` all resolve. No console errors.
- [x] **Tests.** Full EditMode, run after the scene reorder and the input lock: 1433 total, 1422 passed, 11 failed, and the 11 are exactly the known ones (`AIRegressionTest.Baseline_MatchesCurrentAI` plus 10 `HearthMemoryMarkTests`).

## Review fix: input lock

**Applied.** `MissionEndPanelUI` calls `AddInputLock(this)` in `OnEnable` and `RemoveInputLock(this)` in `OnDisable`, both null-safe. The three checks, from reading the code plus 5 EditMode tests. None of this was run in Play with a real wheel or click, so it's part of THJ's play check.

1. **The lock blocks `Player.Scroll`: yes.** `Scroll.performed` goes through `ActiveCheckGuard(Camera)`, and any lock makes `ActiveActionMode` `None`. A test pins that Camera mode is off while the panel is open.
2. **UI clicks and wheel on the panel still work: yes, by code.** The lock never disables an action; it only skips `PlayerInputController`'s own callbacks. `closeButton` is a plain `Button` listener, and the `ScrollRect` gets its wheel and drag from the scene's `InputSystemUIInputModule`, which has its own actions asset reference. Neither passes through `ActiveCheckGuard`.
3. **No exit path can leave it held.**
   - Win: Close runs `ShowMissionMapThenLoad`, which deactivates `levelWonPanel`, so `OnDisable` releases before the map opens.
   - Defeat and Mission Complete: the panel stays on until the scene unloads (`EndMission` or `RestartLevel`, including the sandbox restart). The lock lives on the `PlayerInputController` in that same scene, so it goes with it. Levels load additively, so a new controller can already be `Instance` at that point; the release is then a harmless no-op on the new one, which never held the lock.
   - Repeated `OnEnable` is safe: locks are a set keyed by owner, and a test pins it. Tests also cover a destroyed controller and no controller.

**What else it blocks while the panel is open:**

- Camera mode: keyboard pan, edge scroll, wheel zoom. A held pan stops at once (`UpdateMovement` checks the mode), so no drift.
- Interact mode: world clicks, Cancel, Switch unit, Toggle, cycle move path.
- Pause mode: `PauseGame`, so the pause key won't open the pause menu.
- Anything checking `IsInputLocked`: the End Turn button and ability bar (both hidden by then), and `LowHealthPresenter`, which reads the lock as "banner up" and can delay a pending turn-live heartbeat by up to its 4 s limit. Harmless at level end.
- Not blocked: `SkipLine`, `SkipDialogue`, `ShowStats`, `ReactiveInterrupt`, which aren't gated.

**Things to know:**

- Pause was the only other way out of the panel. If `EndMission`'s save never calls back, Close does nothing more and the pause key is blocked too. `EndLevel` already requests mode `None`, so Pause was only sometimes available before. I didn't trace `SaveLoadManager.Save`'s failure path.
- After Close on a win the lock is released before the mission map opens, so the mode requested earlier returns. If that's `Camera | Pause`, the wheel can still zoom behind the map. Same as before this fix; left alone as out of scope.

## `MainResource_SP` white square

Both: a real data gap, but the harness is why it showed.

- **Real gap:** `Resources/GResources/GResourceSet.asset` has `resourceIcon: {fileID: 0}` for `SP` (also for `XP`). `Image` draws a null sprite as a white square.
- **Harness:** I forced every tracked resource to 12. The panel only shows resources with a non-zero collected amount.
- **In real play I found no way to reach it.** Level-ups add SP straight to `UnitResources`, and the `CollectResource` call there is commented out. Every data reference to `MainResource_SP` under `Assets/_Project` is a requirement or cost, a settings field, or the panel's `trackedResources`; none is a pickup or reward. This is from reading code and data, not from a play session. Not fixed, as asked. A future SP reward would show the white square.

**Scene overrides.** Removed 428 stale layout overrides (144 Mission End, 142 Won, 142 Lost), including Won's and Lost's padding and spacing. Kept the deliberate ones: names, active states, banner and Close text, MVP label, Lost's red sprite, `trackedResources`, root rect. Added: Won and Lost frames at 620x450, and their scene-only subtitle moved to first child (`insertIndex: 0`) so it stays above the columns.

**Screenshots** are in `claude-handoff/reports/end-panel-two-columns-shots/`: `{MissionEndPanel,LevelWonPanel,LevelLostPanel}_{3,8,12}rows_16x9.png` and `..._12rows_16x10.png`, 12 files.

They use harness data, and every tracked resource is forced to 12. On the 3- and 8-row shots I detached the scrollbar, because `ScrollRect` only auto-hides it in Play mode; the Play check above is the evidence that it hides.

## Save reset

No.

## Decisions I made

- Reused the existing `Objectives` object as the right column, so its fileID and overrides survive.
- The list height is fixed at exactly 8 rows (240), so it scrolls from row 9 even on Mission End, where the frame has spare room below the list.
- Won and Lost use a narrower frame (620x450 by scene override), because a 1040 frame around one column looked hollow.
- Scroll sensitivity is 5, so one wheel notch is one row. Other panels use 1.
- Scrollbar uses the same built-in sprites as `Workshop` and `LevelSelect`, tinted, so no new art.
- An objective whose first sentence is blank (text like `.`) also gets no row, since it would show an empty label. Slightly beyond the plan's wording, same intent.
- Added two prefab wiring tests beyond the plan's logic tests.
- Used an offscreen harness for the screenshots rather than Play mode, plus one short Play session (with THJ's untitled empty scene) for what only behaves properly in Play. Left Play afterwards. Everything ran in memory, so no harness files are in the project. The editor is back on its one untitled scene, not dirty.
- Unity moved the unrelated MissionMap block (3 documents, byte-identical) into sorted order on save. I moved it back with a small script so the diff is strictly the three panels.

## Needs THJ

None. Play check below (gate 6: this panel is on M2's win path).

## Docs to update

- `status.md`, `decisions.md`, `build-log.md`: coordinator, per the plan.
- `tech/` notes: nothing changes.

## Risks and loose ends

- **Win marking, out of scope as planned:** every win objective still shows Success, including unmet alternatives. Now that rows are readable this will be more visible on Memory 4.
- **Next scene save may re-sort:** any later editor save of this scene will probably move the MissionMap block again, as it did for me (about 70 moved lines, no content change). If it appears in a later diff, it's harmless.
- **Reopening without a scene reload:** `AddObjectives` still doesn't clear old rows, as before. The review traced this and found it can't happen today (`SetObjectives` runs once per scene load).
- **Empty case:** a Won or Lost panel with no objective text shows the subtitle in a mostly empty 450-tall frame. It doesn't overflow, but I didn't screenshot it.
- **Left column capacity:** Mission End's left column fits today's 4 stat rows, and 5 would fit. Turning on both `TimeStat` and `MoneyGatheredStat` (6 rows, 465) would overflow the 420 available; the frame would need to grow.
- **Existing visuals, unchanged:** the dark green Success label has low contrast on the green frame.
- **Collapsed viewport outside runtime:** the `Viewport` rect is driven by the `ScrollRect`. With the scrollbar detached, my harness measured it at height 0 until I stretched it by hand, so it may look collapsed when viewing the prefab. At runtime it's correct (Play check).
- **Console:** three "Serialization depth limit" warnings appeared in my filtered read. They name `AbilitiesBarHUDUI`, `UnitPanelUI` and `UnitAbilityButtonUI`, which I didn't touch. I didn't check whether they predate this work.
- **THJ's files:** the font, `PreloadScreen.unity`, `ProjectSettings/*`, `AIFactionBrain.cs` and `AIUnitBrain.cs` hash the same at the first check as after the final test run.
- **`UnitAnimationSequence.cs` changed while I worked, and not by me.** Its hash went from `08ca2ec6` to `6605d8ed`, and its modified time moved from 15:48 to 16:30 today. I never opened or wrote it, and all my edits were to other files. It's the change under review, so someone else is probably writing to the project at the same time; worth a check by the coordinator. The final test run compiled that newer version. The Memory 4 assets and `UnitAnimationSequenceTests.cs` weren't hashed; `git status` lists the same entries and I didn't touch them.

## Proposed commits

1. `tweak(ui): long objective text on the end-of-level panel truncates before its state label` (plain; works alone):
   - `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/ObjectiveItem.prefab`
2. `feat(ui): end-of-level panel shows two columns and a scrolling objectives list` (risky: prefab and scene; one unit, since the script needs the new wiring. Includes the input lock, whose code and tests share files with the layout change):
   - `miso/Assets/_Project/Core/UI/Runtime/SessionEndPanel/MissionEndPanelUI.cs`
   - `miso/Assets/_Project/Core/UI/Editor/MissionEndPanelObjectiveRowTests.cs`
   - `miso/Assets/_Project/Core/UI/Editor/MissionEndPanelObjectiveRowTests.cs.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/SessionEndPanel.prefab`
   - `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`

Screenshots stay in `claude-handoff/`, not the shared repo.

## Other branches

All branches need this when merged (scope: all): `main`, `thj/home-test`, and any branch carrying `CombatLevelContainerScene.unity`. Expect conflicts in that scene if another branch edits these three instances' overrides; take this version's override blocks for them.

## How to see it

1. Win Memory 4 (`GB_m4-mark`). Check that the Stats panel has stats and resources on the left, objectives on the right, no blank rows, and Close below the frame.
2. If that level has more than 8 rows with text, scroll the list with the wheel, by dragging the list and by dragging the scrollbar. With 8 or fewer, confirm no scrollbar shows. Either way, the wheel must not zoom the camera behind the panel, and Close must still work.
3. Lose a level. The red panel should show "Mission Failed!", then the Objectives list, centered, with no gap on the left and only the conditions that caused the loss.
4. Finish a level that shows the Victory panel if handy. Same centered layout, with Continue below the frame.
5. Optional: set the Game view to 16:10 and repeat one of them.
