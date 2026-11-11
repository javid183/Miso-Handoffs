# Report: M2 The Trail challenge rebuild (C3)

Plan: plans/onboarding/2026-11-11-m2-trail-levels-tech.md (section C3)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done, with one design-doc gap fixed in the build input and three behaviours for the coordinator to decide on (below). Play check by THJ still to do.

## What changed

- `Content/Levels/Greybox/GB_m2-trailhead|tracks|blood|pile.prefab`: rebuilt with the grid tool (same `GridToLevelBuilder.Build`, overwrite on, GUIDs and `.meta` unchanged) from the revision-2 blocks, then wired.
- `Features/Onboarding/Editor/SearchWiring.Trail.cs`: class made `partial`; new constants; Trailhead, Blood, Tracks rewritten; Pile search tiles/props moved; `SetHealth` now only sets the tracks' factors; `Tiles()` takes an aggregation and target; removed the Archer/Encore code, `LedgeArcherTiles`, `Dies`, `InitialView`. LF, no BOM kept.
- `Features/Onboarding/Editor/SearchWiring.Trail.Arrivals.cs` (+ `.meta`): new partial: `BuildArrival` (input off, camera on the group, reveal, pick's remark, camera back, input on), `BuildFraming` (camera move over several points), `FamilyPoint`, `UnitPoints`, `GroupPoints`. LF, no BOM.
- `Features/Onboarding/Editor/SearchTrailTests.cs`: updated (see Tests). LF, no BOM.
- `Resources/Sequences/Search/Trail/`: new assets with `.meta`: `Trail_Trailhead_Start_CameraOnBothPairs`, `Trail_Trailhead_Start_Bark_DialogNodeSequence`, `Trail_Tracks_Arrival_{CameraOnGroup,Reveal,Bark_DialogNodeSequence,CameraBack,SequentialSequence}`, `Trail_Blood_Arrival_` (same five), `Trail_Blood_Start_CameraFromTheEnd`, `Trail_Blood_End_{CameraOnTheEnd,DialogNodeSequence,SequentialSequence}`. Changed: `Trail_Trailhead_Start_SequentialSequence`, `Trail_Blood_Start_SequentialSequence`, `Trail_Tracks_Start_DialogNodeSequence` (three lines now), `Trail_Pile_End_CameraOnPile` (pile moved).
- `Content/Levels/M2 - The Trail.asset`: untouched (no diff, sequences and home state not edited).

## Acceptance criteria

All levels
- [x] Rebuilt from the blocks, wired; second wiring run: md5 of the four prefabs, the mission and all 48 Trail sequence files identical to the first run. Evidence: hash diff, `git status`.
- [x] HP factors: Trailhead, Blood, Pile have no override; Tracks Dark Claws 0.8, Black Claw 0.5, hidden pack included. Test `OnlyTheTracksOverrideEnemyHealthAndNothingElseIsOverridden` (Claw at Early 16, tracks 12.8).
- [x] All enemies alert (`EveryEnemyStartsAlertOnEveryLevel`), sisters' Duo locked, no FTP filler (pool starts full), no Pass-by or Items panel (tests unchanged and green). Revealed units alert: `HiddenLevelUnits` docs and tracker code only; needs the play check.
- [~] Late arrivals as hidden groups revealed by a stage at the start of turn 2: built (see finding 1). The reveal sequence is exactly input off, camera, reveal, bark, camera back, input on (`AssertArrival`). Needs the play check for the actual moment.

Per level
- [x] Trailhead: 12 x 2 (23 cells), rock at 6,0, Lucy 3,1, Linda 4,1, slot 3,0, Claws 0,1 / 1,0 / 8,1 / 9,1. Intro: the two existing lines, then a camera over all four Claws, then "Behind us!" spoken by the generic pick. Win = defeat all. `EveryLevelPlacesTheUnitsAndCellsOfItsGridBlock`, `...OneDeploySlot...`, `NoLevelShowsAPanel...`.
- [x] Tracks: 10 x 5 (42 cells), Linda 0,2, Lucy 1,2, slot 0,1, Black Claw 7,2, Dark Claws 5,2 / 8,0, hidden `pack` 9,3 / 9,1. Intro: "His tracks.", caption "Black Claw. Hit it, and the pack comes for you." (narrator), pick's "That big one leads them." Stage 1 = turn-2 stage (onComplete = pack arrival, bark "More answering the call!"), stage 2 = defeat all. No Archer or Encore stage.
- [x] Blood: 20 x 5 (45 cells), Linda 0,1, Lucy 1,1, slot 0,0, Claws 4,2 / 9,3 / 9,0 / 14,2, hidden `gullies` 4,4 / 14,4 (bark "One behind us. One ahead!"). Objective "Follow the blood. Two of you, to its end." = `TilesOccupiedLOCondition`, Bergsons, `AtLeast` 2 of 18,1 / 19,1 / 19,0 (the `Tiles()` helper has an aggregation parameter now); the every-enemy-dead fallback is hidden from the panel (`visibleToUser` false, empty text; this works with existing data, see finding 3). Opening: camera starts on the end tiles, pans to the family, "Her blood." Outro: close-up on the end tiles, Lucy's clue line, `OutroCutscene`. Test `FollowTheBloodIsWonByTwoOfTheFamily...`.
- [x] Pile: 11 x 6 (48 cells), Lucy 3,5, Linda 4,5, slot 5,4, props over 4,2 to 5,3, search = any Bergson on 3,3 or 6,3, then Lucy's line, then `west` (1,4, 1,0) and `east` (9,3, 10,1) revealed, no Archer, Claws at 1.0. Outro unchanged (8 steps, test green).
- [x] Reveal on an occupied tile: finding 2.
- [x] Tests: see below.

## The four to-check findings (from the code)

1. **Turn-2 stage timing.** `TurnReachedLOCondition` is relative: it starts counting at its first evaluation (level start, turn 1), so "turn 2" is `turn = 1`, not 2 (the wiring constant `TurnsUntilArrival` = 1; the plan's "2" would fire at the start of turn 3). The turn counter goes up when the turn order wraps to the first faction (the family goes first), then the player phase starts, then `UpdateObjectives` runs, the stage completes and its onComplete sequence plays (`CombatLevelRunHandler.SwitchTurnIE`, `UpdateObjectives`). So it fires at the start of the family's turn 2, after the phase banner starts and after `StartTurn`, with input disabled by the sequence's first step a frame later (not literally "before input"; a click in that frame is theoretically possible; the phase animation plays at the same time as the camera move). The next stage is checked only after the sequence has played, so stage 2's defeat-all sees the revealed units. If every visible enemy dies on turn 1 the enemy faction skips its turn and turn 2 still comes round. No runtime code needed. Not played, so unverified. Also: `TryGetTurnLimit` exists but its only use is commented out, and the AI treats the condition as a false objective; nothing shows a turn cap.
2. **Reveal on an occupied tile.** `HiddenLevelUnits.Reveal` calls `cell.PlugEntity(unit)`, which falls back to the nearest free cell (breadth-first over adjacent cells) when the tile can't be occupied; only when no cell is free is the unit switched off again with a warning. So it shifts, it never fails silently, and the grid tool needs nothing. A Cyclone counts if it blocks `CanOccupy`; I did not check that.
3. **Hiding one objective in the panel.** Works: `visibleToUser` is per objective (precedent: the Lucy memory's hidden first stage). But the panel and the goal highlight read from stages in a way that shaped the Blood wiring: the panel shows every visible objective of the active stage and all earlier stages (no dedupe), the goal highlight only reads the active stage, and the win panel row text is the first sentence of each objective's text (empty text = no row). So for Blood: stage 1 = Any [visible goal line, hidden turn-2 objective]; stage 2 = Any [visible goal with empty text (keeps the end tiles lit and adds no second line), hidden every-enemy-dead with empty text]. Consequences to check in play: the stage-1 goal line stays in the panel after turn 2 but is never re-evaluated (it will not strike through; the level ends at once on a win anyway); the empty visible entry in stage 2 may draw as a blank row and plays the "new objective" sound at turn 2. If THJ dislikes that, the options are (a) make stage 2's goal hidden (no blank row, but the end tiles stop glowing from turn 2) or (b) accept the duplicate line with the same text.
   Tracks: its stage 1 has only a hidden objective, so **the panel is empty on turn 1** and the defeat-all line arrives with stage 2 at turn 2 (same pattern as the Lucy memory's first stage). Showing the count on turn 1 would go stale and duplicate (same cause).
8. **Black Claw damage at Early.** `BlackClaw_Ability_Attack_Effect_AttrMod`: 10 x `Stat_DMG` (Dark Claw: 6 x `Stat_DMG`), ability stat factor 1, enemy faction `Stat_DMG` row for Early = 0.75. So 7.5 per hit at Early (the Claw's 4.5 shows as 4 in the logs; 7.5 shows as 7 or 8 depending on rounding, `RuntimeAAttribute` uses `Mathf.Round`/`RoundToInt`, which rounds half to even, so probably 8; read from play). How the call works: `MemorableAttackMemoryShare` on each Claw listens to `onAbilityPerformedOn`; when an ability lands on a Black Claw within `listenRange` of that Claw, the Claw taunts itself with that ability (`TauntByAbility`). It registers its listener in `Start`, so a hidden Claw only listens once it is revealed: the pack that arrives on turn 2 is not called by a hit from turn 1, but is called by any later hit on the leader (confirms the design's note). Claw alive check and "not already remembered" apply. Not read: the exact `listenRange` value on the prefabs.

## Design-doc gap (decision for the coordinator)

The revision-2 blocks for `m2-tracks` and `m2-blood` list hidden tiles (`level hidden pack 9,3 9,1`, `level hidden gullies 4,4 14,4`) that are drawn `.`, so no unit stands there and the tool builds empty groups. I built from the doc text with a `c` drawn at those four tiles (in memory only; the doc is untouched). The designer should add those `c` marks to the blocks so a rebuild from the doc matches.

## Tests and console

- `SearchTrailTests`: 19 of 19 pass. New or changed: layouts and cells of all four blocks, deploy slots, health factors (tracks only), openings (Trailhead pair of dialogs plus camera, tracks three lines, blood), tracks turn-2 stage and arrival, Blood's AtLeast 2 objective with the hidden fallback and the clue outro, hidden groups on all four levels, placeholder-tag scan including Blood. Removed: the Encore test, the old Blood one-stage test (Blood is two stages now).
- Full EditMode run (before removing the old Blood test): 1877 total, 1875 passed, 2 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI` and that old Blood test. After removing it the Trail suite alone ran 19/19; I did not re-run all 1,876 (4 minutes), so the expected full result is 1875 passed, 1 known red.
- Console after recompile: no compile errors; one editor message "Objects are trying to be loaded during a domain backup" from the reload, plus the usual warnings and serialization-depth notices. Wiring log: "The Trail wired..." with no exception. Grid tool warnings: the "J drawn there is replaced by a deploy slot" x4 (expected).

## Left on disk, unreferenced (not deleted)

- `Trail_Tracks_Encore_{CameraToLedge,CameraBack,DialogNodeSequence,SequentialSequence}`.
- From earlier: `Trail_PassBy_*`, `Trail_Pile_Start_TutorialSequence` / `_Panels`, `Trail_Pile_RearWave`; `Unit_DarkClaw_StartsAlert.prefab` (kept, still the Hearth Claw's variant source).

## Save reset

no

## Decisions I made

- `TurnReachedLOCondition` value 1 for "start of turn 2" (relative counting).
- Late-arrival and Black Claw lines are plain dialogue lines, not barks: the generic pick speaks through `GenericCharacter_1` like the Pile outro; the Black Claw caption is a narrator line in the Tracks intro, placed before its first-appearance close-up (the close-up has no text slot, no runtime change).
- "Camera back" returns to the family's start point (middle of sisters and slot), not to where the family stands on turn 2, since a sequence asset can't point at a unit. Camera framing uses several focus points at once (Trailhead's four Claws, Blood's two gullies); whether the camera zooms to fit all of them is unchecked.
- Blood stage wiring as in finding 3. Hidden-fallback objectives have empty text so the win panel does not list them.
- Line texts are untagged (as the other Trail lines); working lines to list for the line pass: "Behind us!", the Black Claw caption, "That big one leads them.", "More answering the call!", "One behind us. One ahead!", the Blood clue line, plus the objective text.

## Needs THJ / coordinator

- Finding 3's Blood panel behaviour (blank row, stale line, or no glow after turn 2) and the empty Tracks panel on turn 1: accept or pick an option.
- Design doc: add the `c` marks (gap above).

## Risks and loose ends

- Needs play: turn-2 moment, camera framing and return, empty-text visible objective, goal tiles lit after turn 2, revealed units arriving alert, Black Claw hit value, pack on the leader.
- `AIRegressionTest` stays red (its report lists a new Dark Shaman graph; not mine).
- Not checked in play: the design's to-check rows 3, 4, 5, 7, 9.
- PlayModeStaticReset: no new statics.

## Proposed commits

1. `feat(onboarding): The Trail's wiring brings in hidden Claws at the start of turn 2, adds the Black Claw route and the reach goal on the blood route`: `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Trail.cs`, `SearchWiring.Trail.Arrivals.cs` and its `.meta`, `SearchTrailTests.cs` (editor code and tests; plain).
2. `feat(levels): rebuild The Trail's four levels as the two-front challenge and rewire them` (depends on 1; the prefabs, sequence assets and their `.meta` only work together): the four `GB_m2-*.prefab`, and under `Resources/Sequences/Search/Trail/` the changed `Trail_Blood_Start_SequentialSequence`, `Trail_Pile_End_CameraOnPile`, `Trail_Tracks_Start_DialogNodeSequence`, `Trail_Trailhead_Start_SequentialSequence` plus all new `Trail_Trailhead_Start_*`, `Trail_Tracks_Arrival_*`, `Trail_Blood_Arrival_*`, `Trail_Blood_Start_CameraFromTheEnd`, `Trail_Blood_End_*` assets with their `.meta`.

Do not stage: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, ProjectSettings, TMP fallback font (THJ's).

## How to see it

1. Open each `GB_m2-*` prefab in Prefab Mode and compare with the blocks (hidden Claws are switched off on 9,3 / 9,1 (tracks), 4,4 / 14,4 (blood), the Pile's four).
2. Play M2: Trailhead (camera over both pairs, "Behind us!"), Tracks (Black Claw caption, close-up, bark; arrivals at turn 2), Blood (camera on the end first; reach with two of the family; arrivals at turn 2; clue line), Pile (search 3,3 or 6,3).
3. Re-run Tools > Onboarding > Wire Search: Trail: `git status` should not change.
