# Report: Sisters' tally C4, steps and pile wiring

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md    Agent: miso-implementer (sonnet)    Branch: thj/onboarding
Outcome: done (needs THJ's play check)

## What changed

New (all in `Features/Onboarding/SistersTally/`, LF, no BOM):
- `SistersTallyFadeOutSequence.cs`: "Tally: fade out" (`Game/Sequence/Onboarding/Tally: fade out`). Serialized `fadeSeconds` (1.5). Switch off: nothing, nothing marked. Otherwise, if the counter is found and the tally is visible, it shows the counter alone then fades it; then marks itself played and calls `SistersTally.RefreshFaded`. No counter or not eligible: still marks and completes. `SkipStep` hides the counter at once and marks.
- `SistersTallyReturnSequence.cs`: "Tally: return". Marks itself, refreshes. Takes no time. Not placed in any level.
- `SistersTallyShowAloneSequence.cs`: "Tally: show alone" (a third, tiny step, see design choice). Marks nothing.
- `SistersTallyStepRules.cs`: shared logic (`Complete`: marks then refreshes, each in try/catch so a failing save or listener can't hang a step; switch off does nothing).
- `Editor/SistersTallyStepsSetup.cs`: menu `Tools/Onboarding/Set Up Sisters' Tally Steps`. Creates the three assets in `Resources/Sequences/SistersTally/` and points `SistersTallySource.fadeStep` / `returnStep` on `LevelBase.prefab` at fade and return. Idempotent.
- `Editor/SistersTallyStepTests.cs`: 18 tests.

Edited:
- `SistersTallyCounterUI.cs`: fade tween now `.SetUpdate(true)` (unscaled time); new `HideAtOnce()` for Skip.
- `Editor/SearchWiring.Trail.cs`: pile outro split and the two tally steps inserted (script stays the source).
- `Editor/SearchTrailTests.cs`: the pile-end test no longer assumes one dialogue asset; new order test.

Assets:
- `LevelBase.prefab`: only the two reference lines (see Risks).
- `Trail_Pile_End_SequentialSequence.asset`: now 8 steps. `Trail_Pile_End_DialogNodeSequence.asset` keeps only Linda's "Still counting?". New `Trail_Pile_End_Reply_DialogNodeSequence.asset` holds "…No.", John/pick's Rootwell line (still spoken through generic slot 1, now node index 1), Lucy's last line. Texts, speakers, order unchanged.
- 3 new step assets + metas.

New outro order: DisablePlayerInput, HideHUD, CameraOnPile, Tally: show alone, "Still counting?", Tally: fade out, Reply lines, OutroCutscene.

## Design choice: counter visible during Linda's line

A tiny "Tally: show alone" step placed before Linda's line; the fade step (after the line) then fades it and ends the show-alone state. Why this one: the existing sequence types are strictly sequential (no parallel type), so "fade in parallel with the line" is not possible without a new type; a "show alone then wait for the next step" flag on the fade step would make one step span two positions and need cross-step state. A separate step is stateless in the asset, reusable, and the fade step is still self-sufficient: if run without show-alone it shows the counter alone itself. The faded rule is unchanged (fade played and return not played); show-alone marks nothing. The switch off makes all three no-ops.

## timeScale finding

`Time.timeScale` is set to 0 by: the pause menu (`CombatLevelRunHandler.HandlePauseToggleRequested`), tutorial panels (`CombatLevelUIManager.ShowTutorial`), and co-op QTEs. The pile outro itself sets none, and the tutorial is the pile's intro, not its outro, but the player can open the pause menu during the outro. The fade used scaled DOTween, so a pause mid-fade would have stalled the step until resume. Fixed: `FadeOut` is `SetUpdate(true)`; the wait is a frame-based `WaitWhile`, so it ends at timeScale 0. Test reads DOTween's unscaled flag by reflection. Not changed: the slide in/out uses `UIPanelAnimator` (Core UI), still scaled time, so a pause during the show-alone slide delays it until resume (it is not forever). Left alone as core; fine unless THJ wants it.

## Acceptance criteria

- [x] Steps check `Enabled` first, no-op/mark nothing when off: tests `FadeOut_WithTheSwitchOff...`, `Return_WithTheSwitchOff...`, `FadeOut_Skip_WithTheSwitchOff...`, `ShowAlone_DoesNothing...`.
- [x] Fade marks played, tally reads faded: `FadeOut_MarksItselfPlayed_AndTheTallyThenReadsFaded`.
- [x] After return the tally isn't faded and counter shows again: `Return_AfterTheFade...`.
- [x] Completes with counter missing or level not eligible: `FadeOut_FinishesAndMarks_WhenTheCounterIsMissing` / `...NotEligible`, `Return_FinishesWhenTheLevelIsNotEligible`; failing save/listener can't hang.
- [x] Skip reaches end state: `FadeOut_Skip_GoesStraightToHiddenAndMarked`.
- [x] Return built, tested, not placed (wiring test asserts no return step in the outro).
- [x] Source's two references point at the new assets on `LevelBase.prefab`: test `TheLevelBaseTallySource_PointsAtTheFadeOutAndReturnSteps`.
- [x] Trail wiring order and line texts: `ThePileOutroShowsTheTallyAloneForLindasLineThenFadesItBeforeLucyAnswers`; `ThePileOpensWithTheItemsPanel...` and `NoLineCarriesThePlaceholderTag` still green. Wiring run twice: all changed/new files byte-identical after the second run.
- [x] EditMode suite: 1739 of 1740 pass; the one failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. (An earlier run had 7 failures from my test sharing state between tests; fixed.)
- [ ] Needs the play check (not run): the actual slide-in, visible counter during "Still counting?", the fade look and length, and the result panel (the real fade tween with a real CanvasGroup is only checked for its unscaled flag).

## Save reset

no (no save touched; tests use a made-up played list).

## Decisions I made

- Third step "Tally: show alone" (above). Same behavior as the plan's options.
- Kept the existing `Trail_Pile_End_DialogNodeSequence` asset name for Linda's line (no orphan asset); the rest is the new `..._Reply_...` asset.
- New step assets live in `Resources/Sequences/SistersTally/` (next to the Search and Common sequence folders); `Trail wiring` calls `SistersTallyStepsSetup` to find or create them, so a Trail run alone is enough, and the menu also does the prefab link.
- Skip does not call `EndSequence`; a running fade ends by itself when `HideAtOnce` kills its tween.
- Marked even if Play Just Once is off; the faded rule needs the mark regardless.

## Needs THJ

none

## Docs to update

- first-hour design / status / build log: C4 built; return exists, unplaced; show-alone step added.
- `tech/classic-fallback.md`: no new wiring point beyond the Trail outro; coordinator's call.

## Risks and loose ends

- `LevelBase.prefab`: Unity's own save added 7 missing GlobalEventBus event fields (noise). I restored the file from HEAD and applied only the two reference lines by hand, so the diff is 2 lines; nothing else needs re-saving. The setup menu changes it only if a reference differs (it won't now).
- If a mission replays The Pile after Return has been placed and played, the fade step would run again and fade the counter for that level only (fade already marked, return marked, so the tally isn't "faded"). Not reachable until return is placed.
- Dev-skip path: skipping dialogue in the outro skips dialogue and camera only; show-alone and fade still play, so the fade happens.
- `UIPanelAnimator` slide runs on scaled time (above).
- Console shows only pre-existing warnings and serialization depth notices.

## Proposed commits

1. `feat(onboarding): sisters' tally fade out, return and show alone steps`: `SistersTally/SistersTallyStepRules.cs`, `SistersTallyFadeOutSequence.cs`, `SistersTallyReturnSequence.cs`, `SistersTallyShowAloneSequence.cs`, `SistersTallyCounterUI.cs`, `Editor/SistersTallyStepsSetup.cs`, `Editor/SistersTallyStepTests.cs` (each with .meta), `Resources/Sequences/SistersTally.meta`, `Resources/Sequences/SistersTally/` (3 assets + metas), `Content/Levels/LevelBase.prefab` (plain; must go with the assets whose GUIDs it references)
2. `feat(onboarding): the pile's closing lines show the sisters' tally, then fade it`: `Features/Onboarding/Editor/SearchWiring.Trail.cs`, `SearchTrailTests.cs`, `Resources/Sequences/Search/Trail/Trail_Pile_End_DialogNodeSequence.asset`, `Trail_Pile_End_SequentialSequence.asset`, `Trail_Pile_End_Reply_DialogNodeSequence.asset` + `.meta` (plain; depends on 1)

Do not stage: AIFactionBrain.cs, AIUnitBrain.cs, PreloadScreen.unity, ProjectSettings/*.

## Other branches

none

## How to see it

1. Open Unity, let it compile. Optional: `Tools/Onboarding/Wire Search: Trail` again (changes nothing).
2. From a fresh save or one before The Trail's pile, play The Trail with John or Mark (Lucy and Linda deployed) and kill a few enemies so the counter has numbers.
3. Reach the pile and win. During the outro the HUD hides, the camera goes to the pile, then the counter slides in alone while Linda says "Still counting?".
4. After her line, the counter fades out over about 1.5 s, then Lucy says "…No." and the rest plays unchanged.
5. Try opening the pause menu mid-fade: the fade should keep going.
6. At the mission-end panel there are no tally rows and the MVP row is back. Start a later mission with both sisters (M4): no counter (return isn't placed).
7. Optional: change the fade time on `Resources/Sequences/SistersTally/SistersTally_FadeOut.asset`.

## Fix round (review should-fixes)

Date 2026-11-08. Both review should-fixes done; nothing else changed.

### Changed files (this round)

- `E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyCounterUI.cs`: `FadeOut` stopping early at its guard now ends show-alone (`_shownAlone = false`) and slides back (instant), so the counter is never left pinned. Doc comment updated.
- `E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyStepTests.cs`:
  - Helper `GiveTheCounterAFadeGroup` gives the test counter a `CanvasGroup` and also calls the counter's `OnEnable` by reflection (edit mode never runs it, so the counter did not follow tally changes; the "back with the HUD" assert needed this). `OnDisable` is called in `TearDown`.
  - `Drain` takes an optional fade group and completes its tween before each step, so the fade ends without real time.
  - `FadeOut_WithTheHudHidden_EndsHidden` renamed `FadeOut_WithTheHudHidden_EndsShowAloneAndHidesTheNumbers`: fade runs for real, asserts alpha 0, then undoes the faded mark and asserts the counter is not showing (only a show-alone that never ended could keep it on screen).
  - `Return_AfterTheFade_...`: now with a fade group; asserts alpha 0 after the fade, back to 1 and showing after return.
  - New `FadeOut_StoppingEarlyAfterShowAlone_DoesNotLeaveTheCounterPinned`.

### How I checked the asserts bite

Temporarily removed (then restored the file from a copy, diff clean): (a) `_shownAlone = false` at the end of `FadeOut`: the HUD-hidden test failed. (b) `_shownAlone = false` in the new early-stop branch: the new test failed. (c) `StaysFadedOut` made to never clear the faded-out flag: the Return test failed on "back with the HUD". (First combined run had (c) masking (a), so (a) and (b) were rerun without (c).) Not mutation-checked: the DOFade call itself; the existing unscaled-time test covers that the tween exists.

### Test result

Full EditMode suite via the open editor: 1741 total, 1740 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched). `SistersTallyStepTests`: 19/19. Console errors: one Unity "Objects are trying to be loaded during a domain backup" message from recompiling, none from the code. No save reset. LF kept, no private IDs.

### Updated proposed commits (full paths, each `.cs`/asset with its `.meta`)

Commit 1: `feat(onboarding): sisters' tally fade out, return and show alone steps`
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyStepRules.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyFadeOutSequence.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyReturnSequence.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyShowAloneSequence.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyCounterUI.cs
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyStepsSetup.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyStepTests.cs (+ .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/SistersTally.meta
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/SistersTally/ (3 step assets, each with .meta)
- E:/Work/Projects/miso/miso/Assets/_Project/Content/Levels/LevelBase.prefab

Commit 2: `feat(onboarding): the pile's closing lines show the sisters' tally, then fade it` (depends on 1)
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Trail.cs
- E:/Work/Projects/miso/miso/Assets/_Project/Features/Onboarding/Editor/SearchTrailTests.cs
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/Search/Trail/Trail_Pile_End_DialogNodeSequence.asset
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/Search/Trail/Trail_Pile_End_SequentialSequence.asset
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/Search/Trail/Trail_Pile_End_Reply_DialogNodeSequence.asset
- E:/Work/Projects/miso/miso/Assets/_Project/Resources/Sequences/Search/Trail/Trail_Pile_End_Reply_DialogNodeSequence.asset.meta

Do not stage: AIFactionBrain.cs, AIUnitBrain.cs, PreloadScreen.unity, ProjectSettings/*.
