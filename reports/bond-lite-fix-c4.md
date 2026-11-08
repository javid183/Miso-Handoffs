# Report: Bond Lite play fixes C4 (Yard staging)

Plan: plans/onboarding/2026-11-07-bond-lite-play-fixes.md (C4, "Text and adjustments", Log camera trap)    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done, nothing staged. EditMode 1614/1616 passed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, plus a one-off `GridToLevelFpTests.Build_FpFullAddsAWiredFillerToATemplateWithoutOne` failure from a Unity internal assert (`m_LockCount == 0`). That test passed in the run before and passes alone. Framing checked in Play without changing the save. The full path after a real Trail win still needs THJ's play check.

Paths are under `miso/Assets/_Project/`.

## What changed

- `Features/Onboarding/HomeCameraFocusSequence.cs` (+ `.meta`): new sequence step. It calls `CameraHandler.Initialize()`, then pans to a world point and waits for the pan to end. Hold-to-skip snaps it to the end. No statics.
- `Features/Onboarding/Editor/HomeVisitsWiring.Yard.cs` (+ `.meta`): new partial. Builds The Trail's Home state, the yard focus step and the Bond/Margaret lines.
- `Features/Onboarding/Editor/HomeVisitsWiring.cs`: The Trail is out of `SearchingMissions` and gets its own `homeState`. The Yard chain is now focus, Y12-1 to Y12-6, Bond step, Bond line + Y12-7, pointer. Y12-5 and Y12-6 are added to the Yard dialogue. Class summary updated.
- `Features/Onboarding/Editor/HomeVisitsTests.cs`: The Trail's test case is dropped from the Searching test, and the chain test is updated to the 5 steps and their texts (renamed `..._FocusLinesBondBondLineThenThePointer`).
- `Features/Onboarding/Editor/HomeVisitsTests.Yard.cs` (+ `.meta`): new partial with 7 tests. They cover The Trail's own state, its idles (Lucy training, Linda moved, the rest as Searching, no shared actor, Lucy seated by her training idle), the focus point inside Lucy's training area, that the focus is not a `CameraSequence`, that no Yard line says "family point", and that the chain's step names are distinct.
- `Content/Levels/HomeStates-Idles/The Trail - HomeState.asset` (+ `.meta`): new.
- `Resources/Sequences/HomeVisits/Yard_FocusOnTheYard_HomeCameraFocusSequence.asset` (+ `.meta`): new. Focus (32.2, 1.0), 1.5 s.
- `Resources/Sequences/HomeVisits/Yard_BondReached_DialogNodeSequence.asset` (+ `.meta`): new, two Narrator lines.
- `Resources/Sequences/HomeVisits/Yard_Midnight_DialogNodeSequence.asset`: Y12-5 and Y12-6 added.
- `Resources/Sequences/HomeVisits/Yard_Midnight_SequentialSequence.asset`: two steps added (focus first, Bond lines after the Bond step).
- `Content/Levels/M2 - The Trail.asset`: one line changed, `homeState` now points at the new state.

All assets come from Tools > Onboarding > Wire Home Visits, run through the menu. I ran it twice: the second run changed nothing (same hashes), and the first left no noise (no other HomeVisits asset changed, and the Searching state is untouched). Not touched: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, `CameraHandler.cs` and every other core file, `HomeManager`, `SequentialSequence`, `CameraSequence` and the Home scene.

## The camera trap and the fix

- **How the opening leaves the camera.** The intro clip (`AC_HomeAnimator` / `Anim_IntroAnimation`) animates `Camera Controller`, the MainCamera's orthographic size and the `CameraHandler` enable. In the scene, the rig sits at (11.36, 20.13) and MainCamera at local (-12.69, -24.38). The camera's world position therefore equals `InitialCameraPosition` (-1.32, -4.25): before `Initialize()` the view is already at the start view, but the rig is not. `_targetZoom` is 0 until the first `SetZoom`. A focus moves the rig, so it lands 12.69/24.38 off, with a wrong zoom target.
- **Existing Home camera steps:** none in the Home chains. The clue scene, the Hearth close and the station pages are dialogue and tutorial steps only. In Home, `CameraSequence` is used nowhere.
- **Why not `CameraSequence`.** It calls `CombatLevelRunHandler.Instance?.SetAllFactionsActive(...)`. After a mission, `LevelRunHandlerBase._instance` still holds the destroyed combat handler, and `?.` does not see a destroyed Unity object, so in Home it would walk the old level's faction controllers. Its focus also has the same offset problem.
- **The fix, no core change:** `HomeCameraFocusSequence` calls `Initialize()` first. That puts camera local at zero, sets inputs (guarded, only once), runs `SetZoom(default 7)` and puts the rig on `InitialCameraPosition`. The view does not move, because the camera was already there. Then it calls `Focus(point, 1.5 s)`.
- **Play check (framing).** I set an in-memory chain (the focus asset plus the Yard lines, not marked once) as `HomeManager.MissionCompletionSequence` and loaded Home. After the pan the rig and camera were both at (33.40, 1.00), ortho 7, which is where the point was at the time. I applied The Trail's state by hand, because THJ's save has M4 completed, so Home picks the M4 state. Lucy trained with the dummies, Linda stood to her left, and the dialogue box sat below them. I then moved the point to (32.2, 1.0) so the frame is centred on Linda, Lucy and the dummies (checked with a screenshot).
- **After the chain:** the opening's own `Initialize()` snaps the rig back to `InitialCameraPosition` in one frame: a cut of about 34 units, from the yard to the house. It comes right after the last dialogue box closes, so it reads as a scene cut and not as a glitch, but it is a jump. If THJ prefers a pan, a second `HomeCameraFocusSequence` at the end of the chain aimed at (-1.32, -4.25) would make `Initialize()` a no-op visually. That is one line in the wiring. I did not add it because it would change the chain order he set.

## The Trail's Home state

- A copy of the Searching idles with two swaps:
  - `LucySadSit` becomes `LucyTraining` (actors Lucy and Training Objects; area x 28.25 to 38.93, y -1.33 to 2.85).
  - `LindaSadLay` becomes **`LindaHair`**, offset (17, -5.5).
- **Why `LindaHair`:**
  - It is a single actor standing in place, so it reads as Linda watching her sister.
  - Not a bed, sad-lay or Wolf idle, and no prop.
  - The others don't fit:
    - `LindaViolin` / `LindaPlayViolin` carry the violin stand along.
    - `LindaKevinCat` takes Kevin, who is already in the state.
    - `LindaForest` has no authored area.
    - Every Linda + Lucy idle seats Lucy.
  - Moved to the yard's left edge, she stands about three units left of Lucy, clear of the dummies. Checked in Play.
- **Conflicts checked** (asset actor lists; a test also guards this): John, Mary, Ben, Kevin and Joey's idles use only their own actor. Nothing else uses Lucy or Training Objects. `MargaretLucyTraining` is not in the state. Lucy is seated only by `LucyTraining`.
- **When it shows:**
  - The furthest completed mission decides the state (`GlobalSettings.homeStateMissionMode` = Furthest; graph Hearth, River and Ridge, Trail, M4). So the new state shows on the first Home load after The Trail.
  - It also shows on **every later Home load until M4 is won**. Lucy keeps training and Linda keeps standing there (the Yard scene plays only once).
  - After M4 the M4 state shows. Hearth, River and Ridge loads still show Searching.

## Acceptance criteria

- [x] New Home state, Lucy on `LucyTraining`, Linda near, no conflicting idles, The Trail points at it through the wiring: `HomeVisitsTests.Yard` (5 state tests), `SearchingLookIsTheHomeStateOf` without The Trail.
- [x] Chain order and texts (focus, Y12-1 to Y12-6, Bond step, "Linda & Lucy's Bond reached Lv 2.", Y12-7 with "Margaret: ", pointer): `TheTrailPlaysTheYardChainWhenItIsWon_FocusLinesBondBondLineThenThePointer`.
- [x] Pointer "Family point" wording: the pointer reads "The Family Skill Tree has room for the two of us now." and no Yard line says "Family point", so there was nothing to change. A test guards it.
- [x] Camera lands on the yard during Home's opening: seen in Play (rig and camera on the point, zoom 7). Unit-tested only that the point lies inside Lucy's training area.
- [x] Point granted once: unchanged Bond step and existing tests (`TheYardsBondStep_PaysTheSistersOneFamilyPoint_Once`, `BondActivitySequenceTests`).
- [ ] **Needs THJ's play:** win The Trail with F10. Home should open in the new state, pan to the yard and play the lines and the Bond line in order, then stations should work. Then replay The Trail: no Yard and no hang. Expected from the code: the chain is marked once, so `SequencePlayer` calls back at once. Not played end to end.

## Save reset

No. I backed up `SaveData.json` before Play, and after Play and both test runs it has the same SHA-1 (`7bed26c6...`, 01:12). Nothing in the Play check wrote played-sequence state (in-memory chain, not marked once; no Bond step).

**THJ's current save has M4 completed and the Yard already played.** On that save, The Trail's state does not show (M4's does) and the Yard won't play again. To play the acceptance path he needs a save before The Trail's win, or a fresh save.

## Decisions I made

- **A new step, not a `CameraSequence` or a subclass of it:** it avoids the stale combat handler call (see above). Same behaviour as asked: "a small sequence step that ensures `Initialize()` has run before focusing".
- **The step lives in `Features/Onboarding/`** next to `BondActivitySequence`, in the same namespace.
- **The focus is a world point on the asset**, not a scene transform: an asset can't reference the Home scene. It sits inside Lucy's training area, and a test checks that.
- **1.5 s pan** instead of the camera default of 0.5 s, so the 34-unit move doesn't whip.
- **The Bond line and Y12-7 share one new dialogue asset**, so the box doesn't close and reopen between them. The pointer stays its own asset.
- **Night lines kept** (Y12-1 "It's past midnight."), as decided. The Home art at the yard reads as night in Play.

## Needs THJ

None blocking. One taste call: the cut from the yard back to the house after the scene. Keep the snap, or add a pan back as the chain's last step (one line in the wiring)?

## Docs to update

- `tech/home-system.md`: `HomeCameraFocusSequence` is the way to move the camera in a scene that plays inside Home's opening. Use it, not `CameraSequence` (offset rig and zero zoom target before `Initialize()`; stale combat handler after a mission).
- Plan C4 log: built. The Trail has its own Home state until M4.

## Risks and loose ends

- `CameraSequence` used anywhere at Home after a mission would hit the stale `CombatLevelRunHandler` (`LevelRunHandlerBase._instance` is never cleared when the combat scene unloads). Nothing does that today. Left as it is (core file).
- The step calls `Initialize()` a second time per load (the opening calls it again). It is harmless: inputs are guarded, and position and zoom are set again.
- Hold-to-skip during the pan snaps to the yard. Since the step is not a `CameraSequence`, a hold that starts during the pan does not put the chain into fast-forward (it does once the dialogue shows, as before).
- `GridToLevelFpTests.Build_FpFullAddsAWiredFillerToATemplateWithoutOne` failed once on a Unity internal assert log in a full run. It passed in the other full run and alone. Looks flaky, not mine.
- In my Play check, the edge scroller moved the camera after the opening because the mouse sat at the game view's edge. It is unrelated.

## Proposed commits

1. `feat(home): camera focus step that sets the Home camera up first, for scenes in Home's opening`: `Features/Onboarding/HomeCameraFocusSequence.cs` + `.meta` (plain; compiles alone, no data uses it yet).
2. `feat(onboarding): stage the Yard with Lucy training, a pan to the yard and the Bond line`:
   - `Features/Onboarding/Editor/HomeVisitsWiring.cs`
   - `Features/Onboarding/Editor/HomeVisitsWiring.Yard.cs` + `.meta`
   - `Features/Onboarding/Editor/HomeVisitsTests.cs`
   - `Features/Onboarding/Editor/HomeVisitsTests.Yard.cs` + `.meta`
   - `Content/Levels/HomeStates-Idles/The Trail - HomeState.asset` + `.meta`
   - `Content/Levels/M2 - The Trail.asset`
   - `Resources/Sequences/HomeVisits/Yard_FocusOnTheYard_HomeCameraFocusSequence.asset` + `.meta`
   - `Resources/Sequences/HomeVisits/Yard_BondReached_DialogNodeSequence.asset` + `.meta`
   - `Resources/Sequences/HomeVisits/Yard_Midnight_DialogNodeSequence.asset`
   - `Resources/Sequences/HomeVisits/Yard_Midnight_SequentialSequence.asset`

   Plain: the wiring, its data and its tests only work together, and the tests need commit 1.

Per the play-test-before-commit rule, commit after THJ plays it.

## Other branches

None (Bond Lite is on `thj/bond-lite` only).

## How to see it

1. Use a save from before The Trail's win, for example one with River and Ridge done. THJ's current save has M4 done and the Yard played, so it won't show it.
2. Pick The Trail on the world map (the clue scene plays), then press F10 to win the level.
3. At Home: after the intro the camera pans for 1.5 s from the house to the yard. Lucy is training with the dummies and Linda stands to her left.
4. Lines in order:
   - Linda/Lucy Y12-1 to Y12-6, ending "You pin it, I burn it?" / "…That's faster.".
   - Narrator "Linda & Lucy's Bond reached Lv 2.".
   - Narrator "Margaret: First thing you two have done together all year.".
   - Lucy's pointer line.
5. When the last box closes, the view cuts back to the house (judge the cut). Stations take clicks. The skill tree's Family tab has the Linda & Lucy nodes open and one Family skill point.
6. Load Home again, without replaying: Lucy still trains in the yard and no scene plays. This lasts until M4 is won.
7. Replay The Trail and win it with F10: Home opens with no Yard scene, no pan and no hang, and stations work.
