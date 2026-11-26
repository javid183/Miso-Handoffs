# Report: M2 The River, round 2

Plan: plans/2026-11-26-m2-river-round2-tech.md    Agent: miso-implementer    Branch: main
Outcome: R2 done. Built, wired on THJ's prefab, tested; the full EditMode suite is green. Not played (THJ's play check). One deviation from the plan's mechanism for the shared potion page needs the coordinator's nod (decision 1). R1 has its own report (`reports/m2-round2-r1-lucy-followup.md`).

## Round 2 (R2)

### What changed

All paths are under `miso/Assets/_Project/`. Every `.cs` file here is LF with no BOM, like its neighbours (`git ls-files --eol`: `w/lf`, `eol=lf`). An earlier draft said CRLF; that came from a broken shell check.

**Code**
- `Features/Onboarding/PlayOncePerSaveSequence.cs` (new, runtime, + `.meta`): a step that plays a wrapped sequence only if it's not on the save's played list (`PlayedSequencesTracker`, keyed by the wrapped asset's name), plays it in place, then marks it. No statics. Not core.
- `Features/Onboarding/Editor/OnboardingHealthPotionPage.cs` (new, + `.meta`): builds the shared page: `Resources/Sequences/Shared/` with the once-per-save step, the page sequence (page, then the pouch-hint signal), the tutorial step, the panels and the signal step. Also owns the shared signal `Onboarding_PouchHint` and the page text (moved from M1, unchanged).
- `Features/Onboarding/Editor/MissionWiring.River.Ambush.cs` (new partial, + `.meta`): the hidden groups, the Duo lock, the potion on the mission, the ambush sequence and its builders.
- `Features/Onboarding/Editor/MissionWiring.River.cs`: summary rewritten for THJ's layout; `ArcherTile` (11,2) → `RunnerTile` (12,2); `LucyRushTile` (= ford 7,2); hidden groups and Duo lock called from the wiring; stage 2 = the four ring Claws, its end plays the ambush; wave Claws' health factor; the switches child gets a `PouchHint` and a second signal listener; the mission gets one Health Potion.
- `Features/Onboarding/Editor/MissionWiring.River.Sequences.cs`: Shelter page and its panels; Lucy's run in the rush; the Pile's position now measured from the east edge cell 13,2 (14,2 is gone), so the props land on the same spots.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs` (M1): the ambush's potion page and pouch-hint steps replaced by the shared step; the potion text constants and `BuildPotionPanels` removed (moved to the shared builder).
- `Features/Onboarding/Editor/MissionWiring.Ridge.cs` (M1): `PotionPanelsPath` removed; `PouchHintSignal` now the shared `Onboarding_PouchHint`.

**Tests**
- `Features/Onboarding/Editor/M2RiverTests.cs`: updated to THJ's layout and the new groups, stages, locks, rush, ambush and potion (41 tests, was 30).
- `Features/Onboarding/Editor/M1RidgeTests.cs`: the ambush-order test and the potion-only-in-the-ambush test now look for the shared step.
- `Features/Onboarding/Editor/OnboardingHealthPotionPageTests.cs` (new, + `.meta`): 6 tests.

**Assets**
- `Content/Levels/Greybox/GB_m2-river.prefab` (edited in place, never rebuilt): THJ's 80 tiles untouched. The five `ring` units and THJ's four corridor Archers are saved inactive. New hidden group `ambush` (the four corridor Archers) and `wave` (new instances: Dark Worm 10,2; Dark Claws 11,3 and 11,1 at ×0.45). The John–Lucy Duo is merged into John's and Lucy's lock entries next to Cleanse. The stage 2 objective lists the four Claws, and the stage plays the ambush on completion. `River Switches` has a `PouchHint` and a second `SignalAction`. Pile pieces: same positions, new sorting orders (the grid's top row is now y 7).
- `Content/Levels/MS1 - The River.asset`: `initialItemsAvailability` = one `Bergsons_Ability_HealthPotion`.
- `Resources/Sequences/M2River/`: 16 new assets (+ `.meta`): `M2River_Intro_ShelterPage`, `M2River_Shelter_Panels`, `M2River_Rush_LucyRuns`, `M2River_Ambush_SequentialSequence`, `_Ambush_CameraOnCorridors`, `_Ambush_RunnerLeavesRun`, `_Ambush_ArcherLeaves`, `_Ambush_Horn`, `_Ambush_Shake`, `_Ambush_Horn_DialogNodeSequence`, `_Ambush_RevealArchers`, `_Ambush_CorridorArcherRuns1` to `4`, `_Ambush_RevealWave` (names as of the review fix round). Changed: `M2River_Intro_SequentialSequence` and `M2River_Rush_SequentialSequence` (one step inserted each, see decision 3), and `M2River_Rush_CameraToShallows` (the ring's Archer now on 12,2).
- `Resources/Sequences/Shared.meta` and `Resources/Sequences/Shared/` (new): `Onboarding_HealthPotion_OncePerSave`, `Onboarding_HealthPotion_Page` (the save key), `_PageTutorial`, `_Panels`, `_PouchHint` (+ `.meta` each).
- `Resources/Sequences/M1Ridge/M1Ridge_Ambush_SequentialSequence.asset` (M1): the potion page and pouch-hint steps replaced by the shared step (3-line diff).
- `Content/Levels/Greybox/GB_m1-ridge.prefab` (M1): one line, the pouch hint's listener now listens for `Onboarding_PouchHint` (2-line diff).

I didn't touch `LucyFactionRoleHandler.cs`, `LucyRoleSplitFollowUpTests.cs` (R1), `miso.slnx` or any unit prefab.

### What the level does now (as wired)

- **Start:** intro as before, then after "Lucy's Family Role" the new "Sheltered by John" page, then the two lines. Lucy starts on 0,2 next to John on 1,2, so she starts Sheltered.
- **Stage 1** (hidden, unchanged): every enemy dead. Its end plays the rush.
- **Rush:** input/HUD off → "There, by the water. Fur." → camera to the shallows → John walks to 9,2 → ring revealed (four Claws, the Archer on 12,2) → **Lucy runs to 7,2** → turn reset → "Lucy! At me!" / "At you?" → Shield Up → embers pulse signal → input/HUD on. The pulse is a `GuidedAbilityHint` switched on by the signal, so it runs as soon as input returns.
- **Stage 2 "Help John.":** the four ring Claws dead. The Archer doesn't count. Its end plays the ambush.
- **Ambush:**
  1. Input/HUD off.
  2. The camera frames the shallows and the four corridor ends.
  3. The ring's Archer walks to 14,7 (by its nickname: until the corridor Archers come in it is the only Archer in play).
  4. `HideUnitsSequence ring` takes it off the board: no death, no XP, no objective count. It touches only ring units still in play, so dead Claws are left alone.
  5. The horn: a stand-in sound, a camera shake, and the caption "Horn Sounding".
  6. The four corridor Archers come in and walk, one after another: 6,7 → 8,4; 15,7 → 13,4; 6,-3 → 8,0; 15,-3 → 13,0.
  7. The wave comes in (worm 10,2, Claws 11,3 and 11,1; a taken tile → nearest free one).
  8. The shared potion page and pouch hint (once per save).
  9. Input/HUD on.

  "Clear the river." shows as stage 2 completes. The level checks stage 3 only after the ambush has ended (`WaitThenEvaluateNewStage`), so the hidden units are in by then.
- **Stage 3 "Clear the river.":** every enemy dead → the Pile outro, unchanged.
- **Potion:** the mission starts with one Health Potion.

### Acceptance criteria (R2)

- [x] `GB_m2-river` keeps THJ's tweak; nothing rebuilds it. The wiring edits it in place; "Build Level" still refuses. `TheTilesAndUnitsMatchTheTweakedLayout` checks the full 16 × 11 layout, tile by tile, units included. `TheBuildNeverReplacesTheLevel` still passes.
- [x] The John–Lucy Duo is locked, and Cleanse stays locked: `TheJohnLucyDuoIsLockedForBothNextToCleanse`, `CleanseIsLockedForEveryHero`, `RiverCleanseLockTests`.
- [x] The "Sheltered by John" page comes right after the Role page, and Lucy starts next to John: `TheIntroCallsVisitsThePileShowsLucysRoleThenHerShelterThenTheRoleLinesAndGivesNoInput`, `TheShelterPageExplainsTheExtraOrbNextToJohn`, `LucyStartsNextToJohn`.
- [x] Rush order with Lucy → 7,2 between the reveal and the reset; reset → lines → Shield Up kept: `TheRushMovesJohnRevealsTheRingRunsLucyResetsTheTurnThenTheLinesThenHisShield`, `TheLinesStandBetweenTheResetAndTheShield`, `LucyRunsToTheFordTwoTilesFromTheRushTile`. **Play check:** the run, and the pulse when control returns.
- [x] Stage 2 = the four ring Claws: `StageTwoIsHelpJohnTheRingsFourClawsDead`. Its end is the ambush: `ThreeQueuedStagesTheClearingTheRingAndThenEveryEnemy`.
- [x] Ambush wired in order: `TheAmbushSendsTheArcherOffSoundsTheHornBringsTheCorridorsAndTheWaveThenThePotionPage`, `TheCorridorArchersRunToTheMirroredStops`, `TheCorridorArchersWaitHiddenAtTheCorridorEnds`, `TheWaveWaitsHiddenInTheMiddle`. **Play check:** the walks, the leave, the horn, the reveals at runtime.
- [x] One Health Potion; one shared page, once per save across M1 and M2, with the pouch hint only when the page plays. Tests: `TheMissionStartsWithOneHealthPotion`, `ThePotionPageSignalStartsThePouchHint`, `BothAmbushesPlayTheSameStepOnce`, `TheStepWrapsThePageSequenceUnderItsSaveName`, `ThePageSequenceIsThePageThenThePouchHint`, `BothLevelsListenForThePouchHintSignal`, `ThePagePlaysInTheFirstMissionAndIsSkippedInTheOther`, and the M1 ambush tests. **Play check:** M2 then M1 on one save (How to see it).
- [x] Pile ending unchanged: same props and positions, same outro. The props stand past x 13, on tiles with no cell: `ThePilePropsStandPastTheEastEdgeAndBlockNothing`, `TheClearingMeetsTheShallowsOnlyThroughTheFord`, `TheOutroClosesInOnThePile…`. **Play check:** whether the camera reaches the props.
- [x] The five ring units and every new hidden unit are saved inactive: `TheRingWaits…`, `TheCorridorArchersWait…`, `TheWaveWaits…`, `OnlyTheFamilyAndTheClearingStartInPlay`.
- [x] Covering tests, and the full suite green (below).

### Tests

Open editor, Unity MCP, never in Play mode.

| Run | Result |
|---|---|
| `M2RiverTests`, `M1RidgeTests`, `M1RidgeLayoutTests`, `SearchRidgeTests`, `SearchRiverTests`, `RiverCleanseLockTests`, `PouchHintAndDefeatRelaxTests`, `OnboardingHealthPotionPageTests` | 122/123 on the first run. The one failure was my test's helper: it read M1's switches name. Fixed; all pass in the full run |
| Full EditMode suite | **2929 total: 2928 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |
| `AIRegressionTest` | Not run: no AI graph, AI ability or unit prefab changed (only placed instances in the level) |

Before the tests: 8 `M2RiverTests` failed against THJ's prefab, and the wiring threw (`TilePosition` needed cell 14,2). The rerun test `TheWiringRerunLeavesTheLevelUnchanged` is kept. It now also hashes the shared `Onboarding_HealthPotion_*` assets and fails on any warning or error during the rerun. A second `Apply Wiring` run gave a clean console. The full suite left the file set as it was.

### The stand-in sound

`Content/Audio/SFX/Enemies/Goblin Queen/Charge/Goblin Queen Charge.wav` (1.17 s). There's no horn, trumpet or bugle clip in the project; a goblin war cry is the closest. Constant `MissionWiringRiver.HornClipPath`; THJ swaps the clip on `M2River_Ambush_Horn.asset` (or the constant).
- Its `waitForFinish` is off, so the shake plays with it.
- `AudioSequence` plays through the sequence player's audio source. In this level that's `AudioSources/DefaultAmbient` (Ambience mixer group, no clip of its own), so the horn follows the Ambience volume. A real horn may want its own source; not changed.

### Text (placeholders for `miso-narrative`, untagged per D-348)

New:
- Ambush caption (top notification, no speaker): "Horn Sounding".
- Shelter page, title "Sheltered by John". Text: "• While Lucy stands next to John, she is Sheltered by John." / "• Sheltered, she fires an extra orb with her basic attack." The words come from the in-game status ("Sheltered by John", "Lucy gains an extra orb to fire.") and panel ("Lucy fires an extra orb with her basic attack while standing next to John."). Glossary: "Sheltered by John" may be new there (narrative).

Unchanged and reused: the Health Potion page title and text (M1's, word for word), and every 3.2 line.

### Decisions I made

1. **The shared page plays through a new step, not a top-level `SequencePlayHandle`** (same behaviour, different mechanism; **coordinator, please confirm**).
   - `SequencePlayer` holds one `playingSequence`. Calling `Play` on it while the ambush runs overwrites that slot and the ambush's completion callback. When the page ends, the slot is cleared, and when the ambush ends its handler then dereferences null.
   - So the page can't be started at top level in the middle of either ambush. Starting it after the ambush would move M1's page out of its place.
   - Instead, `PlayOncePerSaveSequence` checks `PlayedSequencesTracker` itself, plays the wrapped page sequence in place, then marks it. It's the same self-guard pattern as `BondActivitySequence`.
   - The key is still the asset name, `Onboarding_HealthPotion_Page`; never rename it. The page sequence is also `PlayJustOnce`, so a direct top-level play would use the same key.
   - The pouch hint is the page sequence's second step, so it plays only with the page.
2. **The ring's Archer stays in `ring`; no `runner` group.** `HideUnitsSequence` touches only units in play (`UnitOutOfPlay.IsInPlay`: active, alive, on a cell). When stage 2 ends the four Claws are dead, so `HideUnits ring` takes out only the Archer. If it's dead too, the step does nothing.
3. **The intro and rush step lists were updated once by hand.** Step lists are seeded once (WiringSeed), so the wiring warned and kept the old lists.
   - With a one-off editor call, I inserted `M2River_Intro_ShelterPage` after the Role page and `M2River_Rush_LucyRuns` after the ring reveal (the code's order). M1's ambush list got the same treatment (page + pouch hint → shared step).
   - Re-running both wirings then logged nothing. A fresh build gets these orders from code.
4. **Lucy's run uses `MoveUnitSequence` by nickname.** If she already stands on 7,2, or the tile is taken, the move is cancelled with a console warning and she stays. The only realistic blocker is John stuck on 7,2 because Lucy stood on 9,2 (T-13 in the 3.2 report). I added no fallback.
5. **The ring's Archer is found by nickname, the corridor Archers through the `ambush` group** (corrected in the review fix round; the first version found the corridor Archers by tile, which was wrong). The ring's Archer may have walked during stage 2, so a tile wouldn't find it. When it's dead, the move logs "No unit found named 'Archer Goblin'" and skips.
6. **The ambush starts with a wide camera** over the shallows and the corridor ends, so the Archer's exit and the corridors are in view. The plan named no camera.
7. **The corridor Archers keep their own health** (no factor; the plan named none). The runner keeps ×0.45.
8. **The Pile's anchor moved** from 14,2 to 13,2 (`EastEdgeTile`). The props land on the same world spots.
9. **The paper block in `MissionWiringRiver` is kept** as the builder's input. The summary says it's no longer the layout; the builder refuses anyway.
10. **M1's old potion assets are left in place, unreferenced:** `M1Ridge_Ambush_PotionPage`, `M1Ridge_Ambush_PouchHint`, `M1Ridge_Potion_Panels` (+ `.meta`). They could be deleted in the M1 commit if THJ wants.

### Needs THJ

None beyond the play check. The coordinator should confirm decision 1.

### Risks and loose ends

- **M1's wiring drifts from its committed assets.** Re-running `The Ridge: Apply Layout and Wire` also did two things outside this task:
  - it added a focus point (0.75, 0.75) to `M1Ridge_Ambush_CameraOnEastPath` and `M1Ridge_Ambush_CameraOnFamily`;
  - it reordered the `ambush` group's units in `GB_m1-ridge.prefab`.

  I restored those three changes from HEAD (file contents only, no git write), so M1's diff is just the shared-page step and the signal line. The drift predates this task (probably the last M1 commit changed code without a re-run, or the assets were hand-tuned). M1's tests pass both ways. Worth a look before M1 is next re-wired.
- **Corridor congestion:** the four walks are serial, about 4 to 6 s in all.
  - A hero on a corridor end: that Archer comes in on the nearest free tile and still walks to its stop.
  - A hero on a stop tile, or blocking the only path: that walk is cancelled (warning) and the Archer stays where it came in.
- **The horn on the ambient source.** If a later system puts a looping ambience on `DefaultAmbient`, the horn would replace it until the next clip. Nothing does today.
- **Stage 2 can complete on the enemies' turn.** The ambush then plays mid-enemy-turn. Revealed units are alert and can act on the next enemy turn. No turn reset was asked for.
- **No camera bounds check** for the wide ambush framing (y -3..7) or the Pile (x 15..16): play check.

### Docs to update

- D3 paper block for M2: redraw to THJ's layout, with the ring Archer on 12,2, the corridor Archers hidden, the wave and the stops (coordinator, as planned).
- `tech/onboarding-merge.md` / `status.md`: new runtime step `PlayOncePerSaveSequence` (Features/Onboarding); the shared folder `Resources/Sequences/Shared/`; save key `Onboarding_HealthPotion_Page` (coordinator).
- Glossary: "Sheltered by John" if new (narrative).

### Save reset

No. Play mode was never started. For the play check: clear the save once before the first mission, then **don't** clear it between M2 and M1.

### Proposed commits (updated split)

R1 first, as in its report. Then:

1. `refactor(onboarding): keep the first River level as GB_s1-river_v1 and stop its wiring from touching the mission` (plain). Unchanged from the 3.2 report:
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_s1-river.prefab` + `.meta` (deleted) and `GB_s1-river_v1.prefab` + `.meta` (added)
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.River.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchRiverTests.cs`
2. `feat(onboarding): health-potion page shared by The Ridge and The River, once per save` (plain; M1 touched). Builds on its own, before the River commit, which needs it:
   - `miso/Assets/_Project/Features/Onboarding/PlayOncePerSaveSequence.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/OnboardingHealthPotionPage.cs` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Shared.meta` and `miso/Assets/_Project/Resources/Sequences/Shared/` (5 assets + 5 `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs`
   - `miso/Assets/_Project/Resources/Sequences/M1Ridge/M1Ridge_Ambush_SequentialSequence.asset`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab`
   - Optional, if THJ agrees: delete `M1Ridge_Ambush_PotionPage.asset`, `M1Ridge_Ambush_PouchHint.asset`, `M1Ridge_Potion_Panels.asset` (+ `.meta`)

   Note: `OnboardingHealthPotionPageTests.cs` checks both ambushes, so it goes in commit 3.
3. `feat(onboarding): The River on the tweaked level with John's rush, Shield Flare, the corridor ambush and a health potion` (plain). This is 3.2 commit 2 plus round 2 M2:
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.River.cs` + `.meta`, `MissionWiring.River.Sequences.cs` + `.meta`, `MissionWiring.River.Ambush.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/M2RiverTests.cs` + `.meta`, `OnboardingHealthPotionPageTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m2-river.prefab` + `.meta`
   - `miso/Assets/_Project/Content/Levels/MS1 - The River.asset`
   - `miso/Assets/_Project/Features/Onboarding/MoveGroupUnitSequence.cs` + `.meta`, `miso/Assets/_Project/Features/Onboarding/Editor/MoveGroupUnitSequenceTests.cs` + `.meta` (review fix round)
   - `miso/Assets/_Project/Resources/Sequences/M2River.meta` and `miso/Assets/_Project/Resources/Sequences/M2River/` (35 assets + 35 `.meta`)

**Order note:** the brief listed the M1 shared page last. Committed last, the River commit would refer to `OnboardingHealthPotionPage` before it exists and wouldn't build alone, so I put it second. To keep it last, move `PlayOncePerSaveSequence.cs` and `OnboardingHealthPotionPage.cs` (+ the Shared assets) into the River commit, and leave a final commit with only the M1 files (the two Ridge wiring files, `M1RidgeTests.cs`, the M1 ambush asset and `GB_m1-ridge.prefab`).

Not to stage: `miso/miso.slnx`, `.mcp.json`, `powershell.exe`, `claude-handoff/`, and R1's Lucy files (their own commit).

### How to see it

Before you start: `GlobalSettings` › `deactivateIntroOutroSequences` off. **Clear the save once** (new player).

1. **M2 The River** (from the world map or however you start `MS1 - The River`):
   - Intro: "Lucy's Family Role" page, then the new **"Sheltered by John"** page, then the two lines. Lucy stands next to John; her status shows "Sheltered by John".
   - The John–Lucy Duo button is missing from both bars all level; Cleanse is missing too.
   - The pouch shows one Health Potion.
   - Clear the clearing. Rush: John walks to 9,2, the ring appears (Archer on 12,2), then **Lucy runs to 7,2**, then "Lucy! At me!" / "At you?", then Shield Up. When control returns: Lucy's Fire Embers pulse at once, full AP, objective "Help John.".
   - Kill the four ring Claws (leave the Archer alive the first time). Ambush:
     - The camera widens over the corridors.
     - The Archer walks out the north-east corridor to 14,7 and fades away (no death, no XP popup).
     - The goblin cry plays with a camera shake, then "Horn Sounding".
     - Four Archers appear at the corridor ends and walk to 8,4 · 13,4 · 8,0 · 13,0.
     - A worm and two Claws appear around 10,2 / 11,3 / 11,1.
     - **The Health Potion page** shows, then the pouch button bobs until you open it or drink.
     - Objective "Clear the river.".
   - Win: the Pile close-up, the five clue lines, the outro, the drops (unchanged).
   - Retry once with the ring's Archer killed first: the ambush skips its walk and fade (a console warning names the missing Archer), and the rest plays.
2. **M1 The Ridge, same save (don't clear it):** play to the ambush at the clue. The pack comes, the points top up, and **no potion page or pouch bob** this time; then the sibling-may-fall step, the camera back, Linda's Encore, control back.
3. **The other order:** clear the save, play M1's ambush first (the page shows there, as before), then M2's ambush (no page).
4. Watch for: the camera reaching the Pile past x 13, and the wide ambush frame fitting.

## Review fix round (miso-implementer, 2026-11-26)

Editor not in Play mode. I did the must-fix and all four should-fixes, and corrected the report. R1's Lucy files and M1's three unused potion assets are untouched.

### What changed

1. **Must-fix: the corridor runs find their Archer through the `ambush` group.**
   - New non-core step `Features/Onboarding/MoveGroupUnitSequence.cs` (+ `.meta`, LF). It moves the group's member at a given place in its list, wherever that unit stands now.
   - A member that's not in play (still hidden, dead or taken off the board) is skipped: no move, and the step never falls back to a tile lookup.
   - The walk itself is `MoveUnitSequence`'s: it calls that class's public `PickMoveAbility` and `CanReachDestination`. `Core/Levels/Runtime/MoveUnitSequence.cs` is unchanged.
   - `MissionWiring.River.Ambush.cs`: `BuildMoveByTile` is replaced by `BuildGroupMove`. Run i moves `ambush` member i to `AmbushStopTiles[i]`. The group lists the Archers in start-tile order, and a test checks that member i waits on start tile i.
   - The comment that was wrong about this is rewritten.
   - Assets: `M2River_Ambush_CorridorArcherRuns1` to `4` (new). The old `M2River_Ambush_ArcherRuns1` to `4` (untracked, made in this round, referenced by nothing) are removed. The kept ambush step list was updated once to the new steps, as in decision 3.
   - **The ring Archer's exit move:** checked, and it doesn't have the same issue.
     - It finds its unit by nickname ("Archer Goblin") among living, active units. When it plays, the corridor Archers are still hidden (inactive), and no hero has that name.
     - So it can only move the ring's Archer, or nothing if it's dead (warning, skip).
     - Kept as `MoveUnitSequence`. A test now asserts that John's and Lucy's nicknames differ from the Archer's.
2. **`PlayOncePerSaveSequence`** now overrides `StartSequence()` and clears `_playingWrapped` before `base.StartSequence()`, like `HideUnitsSequence` does with `_skipFade`.
3. **Rename:** `M2River_Ambush_ArcherRuns` → `M2River_Ambush_RunnerLeavesRun`, through `AssetDatabase.RenameAsset`. The GUID is kept (checked before and after).
4. **`M2RiverTests` comments** now say "the tweaked layout" instead of "THJ".
5. **Report:** the line-ending claim is fixed (LF), and the M2River count is corrected to 16 new assets, 35 in all. Decision 5, the congestion risk and the commit list are updated.

### Tests

- New `Features/Onboarding/Editor/MoveGroupUnitSequenceTests.cs` (+ `.meta`), 4 tests:
  - `PickMember_AHeroOnTheStartTile_IsNotPicked_TheMemberIsWhereverItCameIn`: a hero on 6,7 with the Archer on 7,7; the step picks the Archer.
  - `PickMember_AMemberNotInPlay_PicksNothingEvenWithAUnitOnItsStartTile`: the member hidden, then dead.
  - `PickMember_TakesTheMemberAtItsPlaceInTheList` (with the edge cases).
  - `Set_KeepsTheIndexAtZeroOrAbove`.
- `M2RiverTests` ambush test: each run is a `MoveGroupUnitSequence` on `ambush` with member i, stop i, and member i on start tile i. No step in the ambush finds its unit by tile. The runner's step name and the hero nicknames are checked.
- `The River: Apply Wiring` re-run: clean console. `TheWiringRerunLeavesTheLevelUnchanged` green.
- `M2RiverTests`, `M1RidgeTests`, `OnboardingHealthPotionPageTests`, `MoveGroupUnitSequenceTests`, `HideUnitsSequenceTests`: 89/89 passed.
- Full EditMode suite: **2945 total: 2944 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit; not run, no AI content changed). The total includes R1's tests.
- After the suite, `git diff` on M1 is still only the ambush step list and the one signal line.

### Commits

The split is unchanged. Commit 3 (The River) also takes `MoveGroupUnitSequence.cs` + `.meta` and `MoveGroupUnitSequenceTests.cs` + `.meta`, and its M2River folder now holds 35 assets + 35 `.meta`.
