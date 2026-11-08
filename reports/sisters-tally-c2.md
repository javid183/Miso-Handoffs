# Report: Sisters' tally, C1 review fixes + C2 (HUD counter and core hook)

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (C1 should-fixes + C2). Not play-checked. C3 and C4 not started.

## What changed

### Part 1: C1 should-fixes (C1 files only; they stay in C1's commit)

- `Features/Onboarding/SistersTally/SistersTally.cs`: removed the unused public `Run` (it handed out the live run). Added `public static bool IsAtMinimum(float value, float min) => value <= min;`, with a comment on why it's needed (fake deaths and spawner-bound deaths are reported lethal while HP is above the minimum).
- `SistersTallySource.cs`: `DiedFromDamage` now calls `SistersTally.IsAtMinimum(health.Value, health.Bounds.min)`. Same behaviour.
- `SistersTallyListener.cs`: rewrote the comment above `OnLevelEnded`. It now says plainly that a mid-mission win (`Win`) banks; the last level's win (`MissionComplete`) is not banked and stays as the current attempt, which `Current` already shows; a restart from the mission-end panel replays that level with the same mission key, so banking it would count it twice; a defeat drops the attempt. No code change.
- `Editor/SistersTallyTests.cs`:
  - New `AtMinimum_AtOrBelowTheMinimumCounts_IncludingOverkill` (0/0, -12/0 overkill, 1/1 for a non-zero minimum).
  - New `AtMinimum_AboveTheMinimumDoesNotCount` (0.5/0, 40/0).
  - Stronger `SwitchOff_TheLevelDoesNotConnect_AndNothingCounts`: an eligible level runs and Linda kills. Then the next level connects with the switch off, as a new entry. The test checks:
    - `Changed` stays silent and the state is untouched. A real level start would have reset the new entry to 0.
    - Bus events (damage, `Defeat`, `Win`) then reach no tally handler: no `Changed`, and the count stays 1–0.

### Part 2: C2

- **Core hook (its own commit):**
  - `Core/UI/Runtime/HudPanelBase.cs` (new, + `.meta`): an abstract `MonoBehaviour` with `IEnumerator Show(bool instant = false)` and `Hide(bool instant = false)`. It's a base class, not an interface, because Unity can't serialize an interface field.
  - `Core/UI/Runtime/CombatLevelUIManager.cs` (+6 lines; BOM and LF kept):
    - one field `[SerializeField] private HudPanelBase extraHudPanel;` with a tooltip;
    - in `HideHUD` and `ShowHUD`: `var f = extraHudPanel ? StartCoroutine(extraHudPanel.Hide/Show(instant)) : null;` started beside the other panels, and `if (f != null) yield return f;` after the other yields. With the field empty, timing is unchanged (no extra frame).
  - Nothing else in that file changed.
- `Features/Onboarding/SistersTally/SistersTallyCounterUI.cs` (new, + `.meta`): a `HudPanelBase`.
  - Fields: `countLbl` (TMP), `panelAnimator` (`UIPanelAnimator`, slides with the HUD) and `content` (`CanvasGroup`, carries whether the tally shows, and the fade).
  - Plain static rules: `SlidIn`, `ContentShown`, `IsVisible`, `StaysFadedOut`, `Format` ("Linda N · Lucy N").
  - It subscribes to `SistersTally.Changed` in `OnEnable` and unsubscribes in `OnDisable`. The handler is wrapped in try/catch, so it can't stop the listeners after it.
  - For C4:
    - `static Find()`
    - `IsShowing`
    - `ShowAlone(instant)`: on screen while the HUD is hidden. It still shows only if the tally does.
    - `StopShowingAlone(instant)`
    - `FadeOut(duration)`: a DOTween alpha fade. It finishes at once if the counter isn't showing (switch off, not eligible, already faded or off screen). When the fade ends, the alone mode ends and the numbers stay hidden until the tally reads faded.
- `Features/Onboarding/SistersTally/Editor/SistersTallyCounterSetup.cs` (new, + `.meta`): menu **Tools > Onboarding > Place Sisters' Tally Counter**, idempotent.
  - Opens the container scene additively if it isn't open. Creates the counter only if it's missing, re-wires references, fills empty portraits, then saves. It closes the scene again if it opened it.
  - Once the counter exists, placement and look are left alone, so hand tuning survives a re-run.
- `Features/Onboarding/SistersTally/Editor/SistersTallyCounterTests.cs` (new, + `.meta`): 10 tests (see criteria).
- `Scenes/CombatLevelContainerScene.unity`: changed only by running the menu item through the Unity MCP, and saved. Diff checked by fileID against HEAD: 0 objects removed, 23 documents added, 2 changed:
  - **Added:** `---------UI--------/Canvas/SistersTallyCounter`. Components: RectTransform, CanvasRenderer, Image, HorizontalLayoutGroup, ContentSizeFitter, CanvasGroup, UIPanelAnimator, SistersTallyCounterUI. Children `LindaIcon` (Image `Avatar_Linda` + LayoutElement), `CountLbl` (TMP) and `LucyIcon` (Image `Avatar_Lucy` + LayoutElement). It sits right after `ObjectivesPanel` in sibling order.
  - **Changed:** `---Management---/GameSessionUIManager` › `CombatLevelUIManager.extraHudPanel` = SistersTallyCounter.
  - **Changed:** `Canvas` RectTransform › one new child entry.
  - Git's line diff shows "58 deletions"; those are reordered blocks, not removals. LF kept.
  - A second run logs "nothing to change".

Placement: **top centre** of the HUD canvas. Anchor and pivot (0.5, 1), shown at (0, -25), hidden at (0, 150), sliding up like the Level Info panel; about 48 px high, width fits the content. This keeps it clear of:
- Level Info top-left, which holds the FTP and AP indicators and the turn order;
- Objectives top-right;
- the unit panel bottom-left and centre;
- End Turn and the status tooltips bottom-right.

Look (placeholder):
- background: the Level Info `InfoPanel` sprite and colour;
- font: Level Info's `alagard SDF`, size 24; the `·` glyph is in its static atlas (checked);
- portraits: each unit prefab's `unitHUDImage`;
- `visibilityTags`: copied from Level Info ("Generic"), so the dev HUD toggle treats it like the rest of the HUD.

Placeholder text for the narrative layer: "Linda N · Lucy N" (`SistersTallyCounterUI.Format`). Per D-348 it carries no tag.

## Acceptance criteria

- [x] C1 should-fix 1 (`Run` removed): grep found no users; it compiles.
- [x] C1 should-fix 2 (`OnLevelEnded` comment): rewritten as asked.
- [x] C1 should-fix 3 (minimum check + test incl. overkill; stronger switch-off test): `SistersTally.IsAtMinimum`, the two `AtMinimum_*` tests and the rewritten switch-off test.
- [x] HUD counter shows while eligible and not faded, and updates on each counted kill:
  - rule tests: `Visible_WhenEligibleNotFaded_AndTheHudIsShown`, `Hidden_WhenNotEligible`, `Hidden_WhenFaded`, `Format_ReadsLindaThenLucy`;
  - live component test: `Component_FollowsTheTally_AndAThrowFreeUpdateReachesLaterListeners`. A kill sets the label and alpha 1, listeners after the counter still hear both changes, and nothing updates after `OnDisable`.
- [x] Switch (HUD part): `Hidden_WhenTheSwitchIsOff`. The rule also reads `SistersTally.Current`, which is already the default while off.
- [x] Hides and shows with the HUD (`HideHUD`/`ShowHUD`):
  - core hook as above;
  - rule test `Hidden_WhenTheHudIsHidden_UnlessShownAlone`;
  - wiring test `Scene_HasTheCounter_WiredToTheHud`: one counter, the manager field points at it, its refs and both portraits are set, and re-running the setup changes nothing.
  - The live slide needs the play check.
- [x] Exposed for C4 (show alone while the HUD is hidden; fade over a given time): `ShowAlone`, `StopShowingAlone`, `FadeOut(duration)`, `Find()`. Rule tests `Hidden_AfterAFadeOut` and `AFadeOut_HoldsUntilTheTallyReadsFaded_ThenTheTallyDecides`. The tween itself needs the play check (in C4).
- [x] Doesn't cover the objectives, FTP/AP or unit panel: placed in the free top centre (see above). **Needs THJ's eye in play.**
- [x] EditMode suite: run through the Unity MCP after a recompile (no compile errors, no new warnings): **1658 tests, 1657 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red)**. That's 12 more than C1's 1646 (2 `AtMinimum` + 10 counter tests). After the run the editor was back to THJ's state: only `PreloadScreen.unity` open, not dirty, not playing.

## Save reset

No.

## Decisions I made

- The hook's field type is a new abstract `MonoBehaviour` base, `HudPanelBase`, in `Core/UI/Runtime/`. No existing panel base fits (all HUD panels derive straight from `MonoBehaviour`), and Unity can't serialize an interface field. It lands in the hook commit, so the hook compiles and reverts alone.
- Two layers instead of one:
  - the `UIPanelAnimator` slide follows the HUD (and the alone mode);
  - a `CanvasGroup` alpha carries eligibility and the fade.
  - Reason: the dev `HUDVisibilityToggle` slides every animator with a matching tag. With one layer it could slide in a counter for a squad without the sisters. With two, it only moves an invisible panel.
- A finished `FadeOut` holds the numbers hidden (`StaysFadedOut`) until the tally itself reads faded or not eligible. C4's step can therefore mark itself played after the fade without the counter popping back for a moment. If the step never marks itself, the counter stays hidden for that level and resets when its component is disabled.
- `_hudShown` starts true, because HUD panels start on screen in the scene; the first `HideHUD` sets it.
- No static instance, so nothing new to reset: C4 finds the counter with `SistersTallyCounterUI.Find()`.
- The setup leaves an existing counter's position and look alone and only re-wires, so THJ's tuning survives a re-run.

## Needs THJ

None. The play check is needed: placement and the slide (see How to see it).

## Docs to update

- `tech/core-systems.md` (coordinator), Combat UI manager row:
  - optional `extraHudPanel` (a `HudPanelBase`) is hidden and shown by `HideHUD`/`ShowHUD`;
  - new base `Core/UI/Runtime/HudPanelBase.cs`.
- First-hour design tally row (designer): the counter sits at the top centre of the HUD, placeholder look.
- `status.md`, `build-log.md` (coordinator).

## Risks and loose ends

- **Not play-checked.** The live slide, the placement over real levels and the update on a real kill are covered only by tests and the code read.
- The counter shows in M4 as well (Lucy + Linda roster) until C4 wires the fade at The Trail's pile. That is expected.
- C4 notes:
  - call `ShowAlone` before `FadeOut` while the HUD is hidden. `FadeOut` does nothing if the counter is off screen.
  - mark the step played and call `SistersTally.RefreshFaded()` afterwards. `RefreshFaded` raises `Changed` even with the switch off, so check `Enabled` first (reviewer's note on C1).
- `UIPanelAnimator` tweens use scaled time, like the rest of the HUD, and so does the fade.
- While running the setup the first time, Unity logged once "Objects are trying to be loaded during a domain backup". It came from the recompile while the container scene was open additively for my layout read; it hasn't happened again since.

## Proposed commits

Do not stage THJ's uncommitted `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity` or `ProjectSettings/*`.

1. `feat(onboarding): sisters' tally counts Lucy's and Linda's kills per mission` (plain; carries the one `PlayModeStaticReset` line, which only compiles with these files):
   - `miso/Assets/_Project/Features/Onboarding/SistersTally.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTally.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyRun.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyListener.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallySource.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Content/Levels/LevelBase.prefab`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
2. `feat(ui): the combat HUD can hide and show one extra panel with the others` (**core**, alone; compiles without 1 and 3):
   - `miso/Assets/_Project/Core/UI/Runtime/HudPanelBase.cs` (+ `.meta`)
   - `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs`
3. `feat(onboarding): sisters' tally counter on the combat HUD` (plain; needs 1 and 2):
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyCounterUI.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyCounterSetup.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyCounterTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`

The `Editor.meta` and the `SistersTally.meta` folder file go in commit 1, because the folder is created there. Commit 3's files sit inside folders that already exist by then. Per the play-test-before-commit rule, THJ plays commit 3 (a feel chunk) before it is shown.

## Other branches

None (onboarding-only feature).

## How to see it

A fresh save is not required. You need a save where The Trail (`M2 - The Trail`) is open, i.e. The River and The Ridge are done. Use the world map, not the level quick-load, so the mission roster (with both sisters) is active.

1. In Unity, open `Scenes/CombatLevelContainerScene` and select `Canvas/SistersTallyCounter`. It's at the top centre, showing "Linda 0 · Lucy 0" with the two avatars.
2. In the Test Runner (EditMode), filter "SistersTally": 41 green (31 counting + 10 counter).
3. Play and start The Trail from the world map with John or Mark. The counter slides in at the top centre with the rest of the HUD. Check it doesn't sit on anything you care about.
4. Kill an enemy with Linda, then with Lucy. Each kill bumps her number at once. Kills by John or Mark, or by the `K`/`F11` cheats, add nothing.
5. When the HUD hides (dialogue, end of level), the counter slides out with it and comes back with it.
6. Win the level, or press `F10` to win it: the next Trail level keeps the numbers. Restart Level drops that level's kills.
7. The River, The Ridge and the Hearth memories show no counter.
8. To move or restyle it, edit `SistersTallyCounter` in the scene by hand. Re-running **Tools > Onboarding > Place Sisters' Tally Counter** keeps your changes.
