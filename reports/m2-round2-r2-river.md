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

## Round 3 (miso-implementer, 2026-11-26)

THJ played round 2 and asked for four changes. All four are done. No core change. M1, R1's Lucy files and M1's unused potion assets are untouched.

### What changed

1. **The ambush has no wide camera.** `M2River_Ambush_CameraOnCorridors` is out of the ambush code and its step list, so the camera stays on the fight. The asset (new, untracked, unreferenced) is deleted. No other ambush step frames the corridors. `Points.Corridors` is removed.
2. **The four corridor Archers walk at the same time.**
   - `Features/Onboarding/MoveGroupUnitSequence.cs` now takes a list of walks (`Walk { memberIndex, destination }`). It starts every walk together and waits until all have ended.
   - One asset, `M2River_Ambush_CorridorArchersRun` (group `ambush`, members 0–3 to 8,4 · 13,4 · 8,0 · 13,0), replaces `M2River_Ambush_CorridorArcherRuns1` to `4`. Those four (new, untracked, unreferenced) are deleted.
   - The runner's exit (`M2River_Ambush_RunnerLeavesRun`) is unchanged.
   - **Shared move effect: checked, no core change needed.**
     - The Archer's walk effect (`ArcherGoblin_Ability_Walk_Effect_Transport`) keeps per-move state on the shared asset: `IsInProgress`, `_owner`, `_parameters`, `_statCtx`, `_playedMovementAnimation`.
     - Each walk runs as its own coroutine on its own unit, with its own path. During the walk the shared fields are read only for walkability, which uses the owner's faction (all four are Enemy), and for tile and end-of-move effects. This effect has none: `onTileEffects` 0, `movementEndEffect` 0, `differentEffectsOnEndTile` off.
     - `IsInProgress` is cleared by the first walk to end, so the step doesn't wait on it. It waits for each unit's own end of move: the bus's `unitEndMoving` for that unit, or the unit dead or off the board. A 15 s cap stops a missed end from holding the sequence.
     - The class remarks say walks started together are only right for move effects like this one. A test guards the Archer effect's lack of tile and end effects.
3. **Rush order:** ring reveal → Lucy's run → turn reset → **John: "They were waiting for us!"** (new, `M2River_Rush_Surprised_DialogNodeSequence`) → Shield Up → "Lucy! At me!" / "At you?" → embers pulse → input and HUD on.
   - The surprised line (click to continue) now sits between the reset and the cast.
   - The kept rush step list was updated once with a one-off editor call: surprised line inserted after the reset, John's call moved after the shield. The code builds the same order.
4. **The four corridor Archers' health factor is ×0.75** (`AmbushArcherHealthFactor`). The runner keeps ×0.45.

Code files changed this round: `MoveGroupUnitSequence.cs`, `MissionWiring.River.cs` (health factors and summary), `MissionWiring.River.Sequences.cs` (rush order, new line constant `SurprisedLine`), `MissionWiring.River.Ambush.cs` (no camera, one group walk, factor), `M2RiverTests.cs`, `MoveGroupUnitSequenceTests.cs`. All LF, no BOM.

### Text

New placeholder (untagged, D-348): John, in the rush after the turn reset: "They were waiting for us!"

### Tests

- `M2RiverTests` has 42 tests.
  - Rush test renamed `TheRushMovesJohnRevealsTheRingRunsLucyResetsTheTurnThenJohnsSurpriseHisShieldAndHisCall`; it checks every step is adjacent.
  - `ALineStandsBetweenTheResetAndTheShield` replaces the old lines test.
  - Ambush test: no camera step, one group walk between the two reveals with four walks in member order.
  - Corridor Archers at ×0.75.
  - New `TheArchersMoveEffectHasNothingThatReadsTheSharedMover`.
- `MoveGroupUnitSequenceTests` has 5 tests: the walks list, and the new `WalkOver_OnTheUnitsOwnEndOfMoveDeathOrLeaving_NotOnAnotherUnitsEnd`.
- The River wiring re-run left a clean console. `TheWiringRerunLeavesTheLevelUnchanged` green.
- `M2RiverTests`, `MoveGroupUnitSequenceTests`, `OnboardingHealthPotionPageTests`: 53/53.
- Full EditMode suite: **2947 total: 2946 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit; not run, no AI content or unit prefab changed).
- M1's diff is still only the ambush step list and the signal line.

The wiring and tests waited until THJ left Play mode; nothing ran while he was playing.

### Commits

The split is unchanged. Commit 3 (The River) still takes `MoveGroupUnitSequence.cs` + `.meta` and `MoveGroupUnitSequenceTests.cs` + `.meta`. Its M2River folder is now **32 assets + 32 `.meta`**: round 3 added `M2River_Ambush_CorridorArchersRun` and `M2River_Rush_Surprised_DialogNodeSequence`, and removed `M2River_Ambush_CameraOnCorridors` and `M2River_Ambush_CorridorArcherRuns1` to `4`.

### What THJ checks in play

1. **Rush:** after the ring appears and Lucy reaches 7,2:
   - "They were waiting for us!", then John raises Shield Up, then "Lucy! At me!" / "At you?".
   - When control returns: Shield Up still on John, full AP, the embers pulse.
2. **Ambush:**
   - The camera doesn't move.
   - The runner Archer walks out and fades, then the horn and its caption.
   - **The four corridor Archers come in and walk at the same time**, each to its stop. Watch that all four arrive, that none freezes mid-walk or in a walk pose, and that control comes back only after the last one stops.
   - Then the wave, the potion page (if not yet seen on this save), and control back.
3. **Health:** the corridor Archers die a bit sooner than a full Archer (×0.75).
4. **Edge case (optional):** stand John or Lucy on a corridor end before the last ring Claw dies. That Archer comes in on a free tile nearby and still walks to its stop; the hero isn't moved.

### Round 3 review fixes (`MoveGroupUnitSequence.cs`)

- **A walk that ends without the end-of-move event no longer holds the cutscene for 15 s.** From the frame after its start, a walk is over once its unit stands plugged (`PluggedProperly`) on a cell other than its start tile while the shared move effect isn't moving. A walker is unplugged between steps, so a moving unit never counts. This covers the move-block-tag stop mid-path. Only a walk that never leaves its start tile and raises no event still waits for the 15 s cap; the remarks say so.
  - New test `WalkOver_StoppedMidPathWithoutTheEvent_IsOverOnceStandingOffItsStartAndTheEffectStopped`.
  - `WalkOver` now takes the start cell, the frame count and the effect's moving flag.
- **The final animation stop skips units that died on the way**, so their death animation plays.
- **The remarks add a condition:** walking together is only safe when the walkers' paths and stop tiles don't cross, because the core walk still places a mover on a taken stop tile.
- **Tests:** `M2RiverTests` + `MoveGroupUnitSequenceTests` 48/48 (6 group-move tests). Full EditMode suite **2948 total: 2947 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit). Edits and runs waited until THJ left Play mode. No asset changed, so no re-wire was needed. File stays LF.

## Round 4 (miso-implementer, 2026-11-26)

THJ played round 3, tweaked `GB_m2-river.prefab` again (saved 17:22) and asked for five changes. All are wired on his prefab. No core change. I didn't touch M1, R1's files or THJ's `Unit_John.prefab`.

### THJ's prefab, as read

- 75 cells; the old 0,2 cell is gone.
- John is on 1,2 and Lucy on 2,2.
- Clearing: worm 5,2, Claws 6,3 and 6,1.
- `ring`: Claws on 9,3 · 10,2 · 8,2 · 9,1 (John's straight neighbours on 9,2), plus the Archer on 12,2. All five were saved active.
- `ambush`: Archers on 6,7 · 15,7 · 6,-3 · 15,-3. `wave`: worm 10,2, Claws 11,3 and 11,1.
- The ring Claw and the wave worm both stand on 10,2. When the wave comes in, the worm takes the nearest free tile if the Claw is still there.

### What changed

1. **Lucy's Cyclone ends at the start of the rush.**
   - New non-core step `Features/Onboarding/EndCycloneSequence.cs` (asset `M2River_Rush_EndLucysCyclone`), right after input/HUD off and before John's move.
   - It finds Lucy's live Cyclone through `CycloneRegistry.LiveFor` and ends it with `CycloneEntity.Dispose()`, the game's own end path (the same one used when its last pip goes). A Whirl, Steer or burst in progress finishes first; then it leaves its cell.
   - The step waits until the Cyclone is gone, at most 5 s. With no Cyclone out, nothing happens. Cyclone code isn't core.
2. **Potion page:** no change. Skipped because THJ's save already has it played, as designed.
3. **John acts first.**
   - The existing `HoldUnitsUntilSignal` on the `River Switches` child holds Lucy (`Status.Inactive`: she can't be selected and gets no AP at turn start).
   - New non-core component `Features/Onboarding/HoldUntilFirstAction.cs` beside it:
     - it starts the hold on the bus's `levelStarted`, which fires after the intro and before the first family turn starts;
     - it releases her on John's first `abilityPerformed`, the event the faction controller raises when an action completes. Lucy's own actions and enemies' actions don't release her.
   - The release during the family's turn gives back the AP the hold took (`HoldUnitsUntilSignal` already does this), so she can act at once.
   - **Her follow-up while held, checked in code:**
     - Family Roles never look at the skip-turn tags: only the Masher's handler calls `IsUnitTurnSkipped`.
     - `Lucy_Ability_FactionRole` has an empty activation tag query and `apConsumptionType` Ineffective (no AP needed).
     - So her follow-up still answers John's first hit. **Play check.**
   - No new cue: the intro already says it ("Stay by me." / "Hit them first, Dad. My embers will be right behind.").
4. **The Archer on 12,2 is in play from the start.**
   - It's out of every hidden group and saved active. It plays alert from turn 1 (the level starts every enemy alert) and keeps ×0.45.
   - Stage 1 can no longer be "every enemy dead", or the clearing would wait for the Archer. New non-core objective condition `Features/Onboarding/LivingUnitsExceptLOCondition.cs`: living enemies other than the listed units ≤ 0, listing only that Archer. Worm halves still count.
   - Stage 2 is still the four ring Claws.
   - Its escape at the ambush: the run is unchanged (`M2River_Ambush_RunnerLeavesRun`, by nickname). It's taken off the board by the new non-core step `Features/Onboarding/HideNamedUnitSequence.cs` (asset `M2River_Ambush_RunnerLeaves`): the one unit in play with that nickname, fade, then `UnitOutOfPlay.TakeOut`. No death, no XP.
   - Dead, or two Archers in play: nothing happens. At that point the corridor Archers are still hidden.
   - The old `M2River_Ambush_ArcherLeaves` (untracked, unreferenced) is deleted.
5. **The John–Lucy Duo is unlocked.** The wiring removes it from every lock entry (`UnlockDuo`); Cleanse stays locked.

**Rush on the new ring:**
- John walks 7,2 → 8,2 → 9,2 while the ring is hidden; hidden units don't hold their tiles.
- The reveal puts a Claw whose tile is taken on the nearest free tile.
- Lucy's run to 7,2 is unchanged.

### Decisions I made

1. **Rush order kept as THJ hand-edited it.**
   - The kept rush step list had Lucy's run after "Lucy! At me!" / "At you?". My round-3 order put it right after the reveal, so THJ moved it by hand.
   - The wiring keeps hand-edited lists, so I changed the code to his order: reveal → reset → "They were waiting for us!" → Shield Up → "Lucy! At me!" / "At you?" → Lucy runs to 7,2 → embers hint.
   - The click line between the reset and the cast is still there. Tests assert this order. **Coordinator:** tell me if that move wasn't intended.
2. **The Archer isn't in a group revealed at level start.** `HiddenLevelUnits` switches off any listed unit that is active and warns, and a reveal before the first turn is refused. So it's in no group, and the leave step finds it by nickname.
3. **Stage 1 uses a new condition** rather than "≤ 1 living enemy". The count would complete the clearing early if the Archer died first while a worm half was still alive.
4. **The hold starts on `levelStarted`**, not on `HoldUnitsUntilSignal`'s own trigger (the first end of another faction's turn). The family moves first here, so that trigger would come too late.

### Loose ends

- If the player ends turn 1 without acting with John, Lucy stays held until John's first action. That could be his guard on the enemies' turn, or his first action on turn 2.
- The release comes from the first completed action of any kind, a move included.
- THJ's Shield Flare change (`JohnShieldRelay` `pattern` 1, straight) is in his `Unit_John.prefab`; the ring now matches it. Comments and tests no longer mention diagonals.

### Tests

- `M2RiverTests` has 44 tests:
  - new layout block (wave units left out of the drawing because of the shared 10,2 tile);
  - ring on the straight neighbours, only Claws;
  - new `TheShallowsArcherIsInPlayFromTheStartInNoHiddenGroup`;
  - in-play set includes the Archer;
  - new `StageOneIsNoEnemyLeftStandingButTheShallowsArcherAndHidden`;
  - new `TheJohnLucyDuoIsOpenAndCleanseStaysLocked`;
  - new `LucyIsHeldUntilJohnsFirstAction`;
  - rush test renamed `TheRushEndsLucysCycloneMovesJohnRevealsTheRingResetsTheTurnThenJohnsSurpriseShieldCallAndLucysRun`;
  - ambush test with the named leave step.
- New `RiverRushAndHoldStepsTests` (5): the release rule; hold at level start and release on John's first action only; `EndLive` ends only the caster's Cyclone; `PickOnly` (hidden, dead, two in play); `CountLiving` (listed, dead, ignored).
- The River wiring re-run left a clean console. Rerun test green.
- `M2RiverTests`, `RiverRushAndHoldStepsTests`, `MoveGroupUnitSequenceTests`, `OnboardingHealthPotionPageTests`, `RiverCleanseLockTests`, `HoldUnitsUntilSignalTests`: 76/76.
- Full EditMode suite: **2955 total: 2954 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit; not run, no AI content or unit prefab changed by us).
- One group run hit the previous build while a compile error (a duplicated `[Test]`) was pending. I fixed it, recompiled, and every result above is from the fixed build.
- M1's diff is unchanged.

### Commits (updated)

- **THJ's own, separate commit:** `miso/Assets/_Project/Features/Player/John/Prefabs/Unit_John.prefab` (Shield Flare straight). Not ours; it goes in before or with the River commit, since the ring is laid out for it.
- **Commit 3 (The River)** now also takes, each with its `.meta`:
  - `Features/Onboarding/EndCycloneSequence.cs`
  - `Features/Onboarding/HoldUntilFirstAction.cs`
  - `Features/Onboarding/HideNamedUnitSequence.cs`
  - `Features/Onboarding/LivingUnitsExceptLOCondition.cs`
  - `Features/Onboarding/Editor/RiverRushAndHoldStepsTests.cs`

  The M2River folder is now **33 assets + 33 `.meta`**: added `M2River_Rush_EndLucysCyclone` and `M2River_Ambush_RunnerLeaves`, removed `M2River_Ambush_ArcherLeaves`. Commits 1 and 2 are unchanged.

### What THJ checks in play

1. **Start:**
   - Lucy (2,2) can't be selected; John can.
   - John hits the worm or a Claw: Lucy's follow-up prompt appears (she's still held), and her ember fires on the key.
   - After John's action Lucy is selectable with her full AP.
   - The Archer on 12,2 is on the board and alert from turn 1.
2. **Duo:** the John–Lucy Duo button is on both bars. Cleanse isn't.
3. **Clearing:**
   - Killing the worm, its halves and the two Claws starts the rush even with the Archer alive.
   - Killing the Archer first doesn't.
4. **Rush:**
   - Cast Lucy's Cyclone on 7,2 before the last kill: at the rush it fades first, then John walks 7,2 → 8,2 → 9,2.
   - The four Claws come in on 9,3 · 10,2 · 8,2 · 9,1.
   - Then the reset, "They were waiting for us!", Shield Up, "Lucy! At me!" / "At you?", Lucy runs to 7,2, the hint.
   - Shield Flare copies fly straight into the ring.
5. **Ambush:**
   - The Archer (if alive, wherever it stands) walks to 14,7 and fades; with it dead the walk and fade are skipped.
   - Then the horn and the rest as before.
   - The wave worm takes a free tile next to 10,2 if a ring Claw is still standing there.

### Round 4 review fixes

- **The Archer on 12,2 is passive until the ambush** (THJ's answer). Previously it was alert from turn 1 and could walk west into John's rush path.
  - New non-core component `Features/Onboarding/KeepUnitsPassive.cs` (+ `.meta`) on `River Switches`, listing only that Archer.
  - On the bus's `levelStarted` (after the intro, before the first turn) it gives the Archer the `Status.Unaware` tag. `AIController.prefab`'s skip-turn query lists that tag (with Stunned), so the AI never moves or attacks with it.
  - Under `level alert all` the enemy alert tracker keeps no Unaware units of its own. It only ever wakes units it put in its own list (`WakeOne`/`Wake`/`SetAlerted` check `_unaware`), so nothing wakes this one: not sight, not noise, not hits.
  - **What I chose:** it stays passive regardless, even when the player attacks it. It can still be targeted, hit and killed.
  - The tag is hidden in game (`ShowInGame` off), and the tracker draws Unaware markers only for its own units, so there's no marker or pop. Nothing else reads `Status.Unaware`: the only asset that references it is the AI controller's skip query.
  - It doesn't drop out of anything that matters:
    - stage 1 already leaves it out;
    - it isn't in stage 2;
    - for stage 3 the ambush takes it off the board first, or it's dead;
    - the objective-ignore query doesn't list the tag.
  - The ambush still walks it out (`MoveUnitSequence` moves it whatever the AI does) and takes it off the board.
  - No core change.
- **Should-fixes:**
  - The wiring log line now says "Cleanse locked and the John-Lucy Duo open, Lucy held until John's first action, the shallows' Archer kept passive".
  - The `M2RiverTests` header now says the Duo is open.
  - `BlockDocument` is commented as the original paper block, kept only as the first build's input and no longer the layout (diagonal ring and Flare arrows out of date). The block itself is unchanged, since the builder never runs again.
  - The class summary says the Archer stands still.
- **Tests:**
  - New `TheShallowsArcherIsKeptPassiveUntilTheAmbush`: the component sits on the switches child and lists only the Archer, and the AI controller's skip-turn query contains the tag it adds.
  - The existing `EnemyAlertDataTests` already check that this query skips a unit with the tag.
  - That the Archer actually stays put through the turns, also when hit, can't run in edit mode: **THJ's check**.
  - River wiring re-run with a clean console.
  - `M2RiverTests` (45), `RiverRushAndHoldStepsTests`, `OnboardingHealthPotionPageTests`, `RiverCleanseLockTests`, `EnemyAlertDataTests`: 70/70.
  - Full EditMode suite **2956 total: 2955 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit).
  - One wiring run hit the previous build while a missing `using` stopped the compile. I fixed it, recompiled, and re-ran the wiring; the results above are from the fixed build.
- **Commit 3 (The River)** also takes `miso/Assets/_Project/Features/Onboarding/KeepUnitsPassive.cs` + `.meta`.
- **THJ checks in play:**
  - The Archer on 12,2 never moves or shoots during the enemy turns of the clearing and of the ring fight, even when John or Lucy attacks it.
  - Its info panel shows no Unaware marker or pop.
  - John's rush to 9,2 is never blocked by it.
  - At the ambush it walks to 14,7 and fades.

## Round 5 (miso-implementer, 2026-11-26)

THJ played round 4 ("ok, great") and asked for one change: **the John–Lucy Duo is locked from the level start and unlocks at the ambush**, after the Shield Flare beat, with a HUD pulse and a bark. No core change. I didn't touch the files the coordinator is committing (`Unit_John.prefab`, the shared potion page and M1 swap, the old River rename).

### What changed

- **Lock:** the wiring locks the Duo again for John and Lucy (`LockDuo`, merged next to Cleanse; it replaces round 4's `UnlockDuo`). Cleanse stays locked all level; nothing in the level unlocks it.
- **Unlock:** `M2River_Ambush_UnlockDuo`, an existing `UnlockAbilitiesSequence` (`unlockAll` off, only the Duo preset), as The Ridge unlocks Family Footrace. `LevelAbilityLock.Unlock` opens the preset for every unit, and the bar hides a Duo only while it or its partner is locked, so it shows for both John and Lucy once unlocked.
- **HUD pulse:** a second `GuidedAbilityHint` on `River Switches`, on the Duo preset, in `WhenUnlocked` mode, as The Ridge hints its Duo. It waits for the level lock to unlock the Duo and pulses its button until the Duo is used. The embers pulse stays first and switched off until the rush. The HUD is hidden during the ambush, so the pulse shows when input and the HUD come back.
- **Bark:** new non-core step `Features/Onboarding/UnitBarkSequence.cs` (asset `M2River_Ambush_DuoBark`).
  - It shows one line over a unit's head in the same floating popup as the arrow hand-back and Family Footrace barks (`DamageNumberManager.ShowText`), then waits while it shows (1.8 s).
  - It strips the placeholder tag like those barks, respects `silenceBarks`, and does nothing if the speaker isn't alive.
  - Speaker: John.
- **Ambush order:** … corridor Archers walk → wave comes in → **Duo unlocks → John's bark** → potion page (once per save) → input and HUD on. The Duo beat comes before the potion page, so it never depends on the page; a save that has seen the page skips only the page.
- The kept ambush step list was updated once with a one-off editor call (unlock and bark inserted after the wave reveal). Re-running the wiring then logged nothing.

### Found and kept: THJ's hand edits in the rush

The kept rush assets differed from round 4's code. As before, I kept THJ's version and changed the code to match:
- **Order:** reset → "They were waiting for us!" → Shield Up → **Lucy runs to 7,2 → "Lucy! Fire at me!" / "At you?"** → embers hint. Lucy now runs before John's call; the click line between the reset and the cast is still there.
- **Text:** John's call is now **"Lucy! Fire at me!"** (was "Lucy! At me!"). The constant `AtMeLine` now matches, so a fresh build writes his line.

**Coordinator:** both look intentional (THJ played and approved round 4).

### Text (placeholders)

- New bark, John: "Together, Lucy, like we practised!" (the asset holds it with the `[PLACEHOLDER] ` tag, which the bark popup strips on screen, as the other barks do).
- Changed by THJ in the asset (now the code's text too): John "Lucy! Fire at me!".

### Tests

- `M2RiverTests` has 46 tests:
  - `TheJohnLucyDuoIsLockedAtTheStartForBothAndCleanseStaysLocked` (Duo locked for both at start; exactly one unlock in the level, the ambush's, Duo only, Cleanse never unlocked);
  - new `ThePulseOnTheDuoStartsWhenTheAmbushUnlocksIt`;
  - embers pulse test now expects two pulses, embers first;
  - ambush test: unlock right after the wave, bark right after the unlock, both before the potion page, bark speaker, tag and shown text;
  - rush test renamed `TheRushEndsLucysCycloneMovesJohnRevealsTheRingResetsTheTurnThenJohnsSurpriseShieldLucysRunAndCall` for THJ's order and line.
- `RiverRushAndHoldStepsTests` has 6 tests: new `Shown_StripsThePlaceholderTagOnly`.
- The River wiring re-run left a clean console. Rerun test green.
- `M2RiverTests`, `RiverRushAndHoldStepsTests`, `OnboardingHealthPotionPageTests`, `RiverCleanseLockTests`, `GuidedAbilityHintTests`: 70/70.
- Full EditMode suite: **2958 total: 2957 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit).
- Two group runs failed against THJ's newer rush assets (his order and his line) before I matched the code. The results above are after that, from the final build.

### Commits (updated)

- **Commit 3 (The River)** also takes `miso/Assets/_Project/Features/Onboarding/UnitBarkSequence.cs` + `.meta`.
- Its M2River folder is now **35 assets + 35 `.meta`**: added `M2River_Ambush_UnlockDuo` and `M2River_Ambush_DuoBark`.
- The rest is as in Round 4 and the Round 4 review fixes, minus what the coordinator commits separately.

### What THJ checks in play

1. **Start to the ring fight:** the John–Lucy Duo button is on neither bar; Cleanse isn't either.
2. **Ambush:**
   - After the corridor Archers and the wave come in: "Together, Lucy, like we practised!" floats over John for about 2 s.
   - Then the potion page, only if this save hasn't seen it; then control returns.
3. **After the ambush:**
   - The Duo button is on John's and Lucy's bars and pulses when either is selected, until the Duo is used.
   - Cleanse stays hidden.
4. With barks silenced in settings, the bark is skipped and the Duo still unlocks and pulses.

## Final alignment (miso-implementer, 2026-11-26)

THJ tweaked round 5 himself and said "All good. Commit". The wiring code and tests now match his version, and his assets are the master.

### Changes

1. **Ambush bark:** `DuoBarkLine` = `"[PLACEHOLDER] Lucy, lets play hide and seek!"` (THJ's text, verbatim). The test checks the shown text "Lucy, lets play hide and seek!".
2. **Intro:** `M2River_Intro_CameraBack` is dropped from the wiring's intro list: call → camera to the Pile → Lucy's Role page → Shelter page → Role lines. The asset (untracked, unreferenced) is deleted. The intro test expects one camera step, `M2River_Intro_CameraToPile`.
3. **Ambush:** THJ's new step `M2River_Ambush_LucyRuns` (`MoveUnitSequence`, by nickname "Lucy", destination 9,1) is now built by the wiring (`AmbushLucyTile` = 9,1), at THJ's place: after `M2River_Ambush_RevealArchers`, before `M2River_Ambush_CorridorArchersRun`. The ambush test checks the step, its unit and tile, and that the Archers' group walk follows it.

### THJ's edits to `GB_m2-river.prefab` and `M2River_Intro_CameraToPile.asset` may be lost

**Needs the coordinator and THJ.**

- A River wiring run at **19:27:36**, before this round, rewrote every asset the wiring owns, all within the same second: `GB_m2-river.prefab`, `M2River_Intro_CameraToPile`, `M2River_Intro_CameraBack`, the bark, the panels, the Shared potion assets and more. Not mine: I ran nothing between round 5 and this message. It's most likely the `TheWiringRerunLeavesTheLevelUnchanged` test inside the full suite that showed the 3 failures; that test calls `MissionWiringRiver.Run()`.
- That run reset the bark's line to the old "Together, Lucy, like we practised!", which is why the coordinator's text was needed. It would also have reset any of THJ's changes to wiring-owned values in the prefab (unit states, groups, health factors, locks, stages, switches, Pile props) and in the camera asset (focus points, duration, wait).
- What I can tell:
  - The current `M2River_Intro_CameraToPile` is exactly what the wiring writes: from Lucy and John to the Pile, wait 0.8.
  - My wiring run left the prefab and the camera byte-identical (md5 before and after), so they hold the wiring's values now.
  - THJ's step-list edits and his new `M2River_Ambush_LucyRuns` survived (the wiring keeps step lists), and stayed byte-identical through my run.
  - The bark is back to THJ's text, written by the wiring from the new constant.
- I can't rebuild THJ's lost edits: the files are untracked and nothing kept an earlier copy.
- **THJ:** please check the River intro camera and anything you changed on the level prefab before committing. Tell us what you'd changed so the wiring can carry it.
- **Risk:** the rerun test overwrites hand edits to wiring-owned values on the real assets whenever the suite runs. Until the wiring carries them, keep hand edits to those values out of the River assets, or decide to make that test non-destructive.

### Tests

- River wiring re-run left a clean console; THJ's intro list, ambush list and `M2River_Ambush_LucyRuns` stayed byte-identical.
- `M2RiverTests` (46), `RiverRushAndHoldStepsTests`, `OnboardingHealthPotionPageTests`, `RiverCleanseLockTests`, `MoveGroupUnitSequenceTests`: 65/65.
- Full EditMode suite: **2958 total: 2957 passed, 0 failed, 1 skipped** (`AIRegressionTest`, Explicit).

### File list for the River commit

All under `miso/Assets/_Project/`, each with its `.meta` where it has one:

- **Level and mission:** `Content/Levels/Greybox/GB_m2-river.prefab` + `.meta`; `Content/Levels/MS1 - The River.asset` (modified).
- **Wiring:** `Features/Onboarding/Editor/MissionWiring.River.cs`, `MissionWiring.River.Sequences.cs`, `MissionWiring.River.Ambush.cs` (+ `.meta` each); `Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs` (modified).
- **Steps and components:** `Features/Onboarding/MoveGroupUnitSequence.cs`, `EndCycloneSequence.cs`, `HideNamedUnitSequence.cs`, `HoldUntilFirstAction.cs`, `KeepUnitsPassive.cs`, `LivingUnitsExceptLOCondition.cs`, `UnitBarkSequence.cs` (+ `.meta` each).
- **Tests:** `Features/Onboarding/Editor/M2RiverTests.cs`, `MoveGroupUnitSequenceTests.cs`, `RiverRushAndHoldStepsTests.cs`, `OnboardingHealthPotionPageTests.cs` (+ `.meta` each). The last one checks both ambushes, so it goes with The River.
- **Sequences:** `Resources/Sequences/M2River.meta` and `Resources/Sequences/M2River/`, **35 assets + 35 `.meta`**:
  - **Ambush:** `M2River_Ambush_CorridorArchersRun`, `_DuoBark`, `_Horn`, `_Horn_DialogNodeSequence`, `_LucyRuns`, `_RevealArchers`, `_RevealWave`, `_RunnerLeaves`, `_RunnerLeavesRun`, `_SequentialSequence`, `_Shake`, `_UnlockDuo`.
  - **Intro:** `M2River_Intro_Call_DialogNodeSequence`, `_CameraToPile`, `_LucyRolePage`, `_Roles_DialogNodeSequence`, `_SequentialSequence`, `_ShelterPage`.
  - **Panels:** `M2River_LucyRole_Panels`, `M2River_Shelter_Panels`.
  - **Outro:** `M2River_Outro_CameraOnPile`, `_Clue_DialogNodeSequence`, `_SequentialSequence`.
  - **Rush:** `M2River_Rush_AtMe_DialogNodeSequence`, `_CameraToShallows`, `_EndLucysCyclone`, `_FlareHint`, `_JohnRushes`, `_JohnShieldUp`, `_LucyRuns`, `_ResetTurn`, `_RevealRing`, `_SequentialSequence`, `_Sighting_DialogNodeSequence`, `_Surprised_DialogNodeSequence`.

Not to stage: `miso/miso.slnx`, `.mcp.json`, `powershell.exe`, `claude-handoff/`. Already committed by the coordinator: `Unit_John.prefab`, the shared potion page and M1 swap, and the old River rename.
