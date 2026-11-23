# Report: Onboarding 3.1b, M1 the Ridge on a new `GB_m1-ridge`

Plan: plans/2026-11-23-onboarding-m1-m2-build-tech.md (section 3.1b)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: paused (THJ shut down). The build, the wiring and the tests are done and green; THJ's play check (with a win) and the review are still to do. Nothing is half-written: every file compiles, every asset is saved, Play mode was never started.

## What changed

- `miso/Assets/_Project/Content/Levels/Greybox/GB_s2-ridge.prefab` (+ `.meta`) → renamed to `GB_s2-ridge_v1.prefab` (+ `.meta`) with `AssetDatabase.MoveAsset`. The GUID is kept (`f1922cc21c98df8469b643b2f0ba7a5c`). Git shows this as a delete plus an untracked pair, so stage both sides together.
- `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Ridge.cs` (LF, no BOM, kept): `LevelPath` now points at `_v1`. Removed: `WireMission()` and its call, `MissionPath`, and the reward consts (`GoldReward`, `SteelReward`, `XpReward`, `GoldId`, `SteelId`). Updated the summary, the log line and the menu name ("Wire Search: Ridge (first version)"). Dropped the now-unused `System.IO` / `System.Linq` usings.
- `miso/Assets/_Project/Features/Onboarding/Editor/SearchRidgeTests.cs` (LF, ASCII): removed `MissionAsset()` and three tests: `TheMissionPlaysOnlyTheRidge`, `TheMissionGivesGoldAndSteelEveryTimeAndThirtyExperience` and `TheRosterIsLindaAndMarkFixed`. Their checks moved to `M1RidgeTests`. Updated the header comment.
- **New** `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab` (+ `.meta`, GUID `be49e5e1615a87e46a719d35c0f31047`). Built by `GridToLevelBuilder.Build` (the code behind `Tools/Levels/Build Level From Grid...`), called through Unity MCP, from the block in the scratch file `m1-ridge.md`. That block is the paper block `m1-ridge` with one change, Mark moved to 3,2 (the fallback for the Counter check; see the to-checks below). The tool then wired the prefab.
- **New** `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.cs` (class `MissionWiringRidge`, menu `Tools/Onboarding/Wire Mission: The Ridge`). I ran it twice; the second run left no console warnings.
- **New** `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs` (20 tests). Unity creates its `.meta` on import.
- **New** folder `miso/Assets/_Project/Resources/Sequences/M1Ridge/` (+ folder `.meta`): 17 assets, each with its `.meta`:
  - Start: `M1Ridge_Start_SequentialSequence`, `_Start_CameraToLedge`, `_Start_Opening_DialogNodeSequence`, `_Start_CameraBack`, `_Start_Roles_DialogNodeSequence`.
  - Masher setup: `M1Ridge_MasherSetup_SequentialSequence`, `_CameraToMasher`, `_DialogNodeSequence`, `_SelectLinda`.
  - Arrival: `M1Ridge_Arrival_SequentialSequence`, `_CameraOnGroup`, `_Reveal`, `_Bark_DialogNodeSequence`, `_SelectLinda`.
  - End: `M1Ridge_End_SequentialSequence`, `_CameraOnClue`, `_Clue_DialogNodeSequence`.
- `miso/Assets/_Project/Content/Levels/MS2 - The Ridge.asset`: the graph node's `payload` now points at `GB_m1-ridge`. One line in the diff. GUID, name, node guid, drops, experience and roster are unchanged.

## Acceptance criteria (this chunk)

- [x] The old level is renamed and keeps its GUID. Nothing in `Assets` references the old GUID any more (grep over `.asset`/`.prefab`/`.unity`). The old tool can't touch the mission. Evidence: `M1RidgeTests.TheFirstVersionsToolWiresItsOwnLevelAndNeverTheMission`, and `SearchRidgeTests` passes (10/10) against `_v1`.
- [x] `GB_m1-ridge` is built from block `m1-ridge`: 38 cells, 8 units placed, no build issues. Tests cover the tiles, the missing cells, the Masher's only neighbours (4,0 and 7,0), the hidden group `back` (1,4 and 3,4), Early tier and all enemies alert.
- [x] Turn order is family first: the level keeps the default order, with no override (test).
- [x] HP factors are set on the placed units: Claws 0.8, Masher 0.45 (test).
- [x] Start sequence: input off, HUD off, camera from Linda to the ledge, the pair's two lines, camera back to the pair, two Role lines. It does not end with `EnablePlayerInputSequence` or `ShowHUDSequence` (test). Input and HUD come back at the turn start, after the enemy cards.
- [x] Masher stage: when the pack dies, the setup runs (camera along the corridor to the Masher, two lines, one saying to aim at it, camera back on Linda, input on). Stage 2 is the Masher dead (shown) or the stage's turn 2 (hidden); when it completes, `back` is revealed. Stage 3 is the Masher dead again (shown), so the goal stays on screen. Stage 4 is defeat all (tests).
- [x] Cleanse is locked for Linda and Mark and nothing else. No Vault lock: chunk 3.1a already took Vault off game-wide (test).
- [x] No first-sleeper / Asleep panel: no `SequencePlayHandle` on the level (test).
- [x] Clue props at 12,0; the end sequence is the close-up, the clue lines, then the outro (test).
- [x] The mission is re-pointed and keeps its GUID, name, drops (Gold 20, Steel 2, XP 30) and its fixed Linda + Mark roster (tests).
- [ ] THJ's play check, with a win: not done (paused).

Tests run in the open editor:
- `M1RidgeTests` 20/20 and `SearchRidgeTests` 10/10.
- 216/216 across all `GridToLevel*` fixtures, `OnboardingMissionGraphTests`, `OnboardingOpeningSetupTests`, `HomeVisitsTests`, `BondSourcesTests`, `SearchTrailTests`, `SearchRiverTests` and `WiringSeedTests`.
- No full-suite run: nothing shared or core was touched. `AIRegressionTest` was not run.

## To-checks

- **T-17 (does a hit on Mark count for his Counter?): no, it fails.** `MarkFactionRoleHandler.PrepareTargets` asks for a hit ally with `u != Unit`, so a hit on Mark himself never triggers his Counter. **I applied the fallback: Mark starts on 3,2**, not 4,3. From 3,2 he is 2 from Linda's neighbours 2,0 and 1,1, so a Claw hitting her there draws his Counter. His walk to the ledge is 2 steps longer.
- **T-4 (what does Encore do with arrows locked under a living Masher?)**: by code read, Encore (Recall) brings back **every** grounded arrow, locked stacks included (`RecallRules`: "locked stacks and walled-off cells included"). So the "Linda alone" answer refills her quiver through Encore. Not played.
- **T-1 (arrow falloff)**: no falloff by default. On `LindaAttackArrow.prefab`, `onHitExtraModifier.factor` reads from the stat (`factorReadMode` 1): `baseFactor` 1 × `Stat_DMGD` 1 (level 0 on `Linda_Ability_PrimaryAttack`) = 1. The 0.9 is the unused `constantValue`. `SearchRidgeTests.TheCatchKillsAGauntletClawButOneBlitzDoesNot` asserts this and passes. M1 uses only first hits anyway. The Trail logs' "6 then 4" must come from something else (a run upgrade or the tier); not traced.

## Placeholder lines (for miso-narrative)

None of these carry the `[PLACEHOLDER]` tag in the asset: dialogue shows the tag on screen (`conventions.md` › Text), and the onboarding tests forbid it. This list stands in for the tag.

1. Start, `M1Ridge_Start_Opening_DialogNodeSequence`: Mark "I'll take the high path. Keep them off me." · Linda "Keep up, little brother."
2. Start, `M1Ridge_Start_Roles_DialogNodeSequence`: Linda "Anything that steps into my line gets an arrow." · Mark "Anything that touches her answers to me."
3. Masher setup, `M1Ridge_MasherSetup_DialogNodeSequence`: Mark "I'll knock it over." · Linda "Don't stand next to it. Aim at it and look where it slams." (The paper had "Don't stand next to it. Look."; I reworded it to tell the player to aim, as decided for the Masher setup.)
4. Arrival bark, `M1Ridge_Arrival_Bark_DialogNodeSequence`: Linda "More of them. Behind us!" (The paper names the bark but gives no text; this one is mine.)
5. End, `M1Ridge_End_Clue_DialogNodeSequence`: the old Ridge's five clue lines, copied unchanged (they matched the old asset).
6. Objective texts: "Get past the Masher." and "Clear the ridge. {alive_0} remaining."

## Paper tiles vs the built prefab

The built prefab matches the paper block `m1-ridge` tile for tile, with one exception: **Mark is on 3,2, not 4,3** (the Counter fallback). Everything else is as drawn:
- Linda on 1,0.
- Pack on 0,4, 2,4 and 1,3.
- Hidden `back` on 1,4 and 3,4.
- Masher anchor on 5,0.
- Room 0..3 × 0..4, corridor 4..12 on row 0, ledge 4..8 on row 3 with 8,2 and 8,1.
- No cells at 4,1, 7,1, 5,2 or 6,2.
- `level` lines: name The Ridge, tier early, alert all, hidden back.

The drawing annotations (arrows, zones, notes) aren't read by the builder. The block that was built is in the scratch file `C:\Users\javid\AppData\Local\Temp\claude\9ec5439f3060d705\a7664ea6-6a12-471f-a9f1-6029da993a5c\scratchpad\m1-ridge.md`. The paper doc still shows M on 4,3: the designer should update it.

## Chunks

### Chunk 3.1b: M1, the Ridge (paused before the play check)

- Changed: everything under "What changed".
- Criteria met: see above.
- Decisions and loose ends: see below.

## Save reset

No.

## Decisions I made

- I applied the T-17 fallback (Mark on 3,2), as the plan allows when T-17 fails. It fails by code read.
- I built from a scratch copy of the paper block (only Mark's tile changed) through the builder's API, not the window. The result is the same as building from the window.
- Tool name: `MissionWiring.Ridge.cs` / `MissionWiringRidge`, menu "Wire Mission: The Ridge". Its sequences are in `Resources/Sequences/M1Ridge/` with the prefix `M1Ridge_`, all new paths.
- I read "the intro" as the Search missions' opening (input and HUD off). There is no `IntroCutscene`, and no Family Role tutorial panel: the old Ridge's "Mark's Family Role" panel is not reused. Easy to add if wanted.
- Pack-dead condition: `EntitiesDestroyedLOCondition` on the three placed pack Claws. Masher-dead condition: `UnitDeathLOCondition`. Stage 2 then stage 3 follow the Trail's "Blood" pattern (goal or hidden turn 2, then the goal again).
- Cleanse path: a const of its own in the new tool, not `HearthMemoryRules.CleansePath`. That class is still uncommitted Phase 1 code, and using it would tie this commit to it.
- The Masher setup and the arrival end with `SelectUnit` Linda + `EnablePlayerInputSequence`, like the Trail's arrivals. H-01 is about start sequences only.
- The mission's drops, experience and roster are not rewritten by the new tool (re-point only). Their asserts moved to `M1RidgeTests`.
- No FTP filler: the built level has none, and the pool starts full with the mission (as on the Trail).

## Needs THJ

None blocking. To confirm at the play check: Mark's start on 3,2 (the fallback).

## Docs to update

- Paper doc `plans/2026-11-22-onboarding-d3-paper-levels.md`, block `m1-ridge`: Mark on 3,2 (T-17 failed). Also the Linda setup line, if the reword is kept. Owner: designer.
- `tech/onboarding-merge.md` and status: the Ridge now plays `GB_m1-ridge`; `GB_s2-ridge_v1` is kept. Owner: coordinator.

## Risks and loose ends

- **The Masher's enemy card (first-appearance close-up) plays at the first player turn with the Claws**, not at the Masher stage as the paper says. The cards play for every new enemy at turn start; deferring the Masher's would need new code (not in the plan).
- **Not built (not in the plan's list):** Mark's "Linda. Shoot at me." / "Gladly." lines when he first stands on 7,0, and the `GuidedAbilityHint` fallback (T-5). No tile trigger exists that fits without new code.
- Whether Encore is on Linda's bar in M1 isn't checked (Memory 1 unlocks it in-level). It matters for the "Linda alone" answer.
- The renamed prefab's root object may still carry the name "GB_s2-ridge" inside its YAML until it's next saved. Harmless.
- AI paths may differ from the paper's (the pack's landing tiles): play check.

## Proposed commits

1. `refactor(onboarding): keep the first Ridge level as GB_s2-ridge_v1 and stop its wiring from touching the mission`: `GB_s2-ridge.prefab` + `.meta` (deleted), `GB_s2-ridge_v1.prefab` + `.meta` (added), `SearchWiring.Ridge.cs`, `SearchRidgeTests.cs` (plain)
2. `feat(onboarding): rebuild The Ridge as GB_m1-ridge with the Masher beat, and point the mission at it`: `GB_m1-ridge.prefab` + `.meta`, `MissionWiring.Ridge.cs` + `.meta`, `M1RidgeTests.cs` + `.meta`, `Resources/Sequences/M1Ridge/` (folder `.meta` + 17 assets + `.meta`s), `Content/Levels/MS2 - The Ridge.asset` (plain)

Commit 2 depends on commit 1: its test checks the old tool. Both are separate from the Phase 1 files and THJ's files; there is no overlap.

## Other branches

None.

## How to see it

1. Open `Content/Levels/Greybox/GB_m1-ridge.prefab` and compare it with the paper block (Mark on 3,2).
2. Start a new save, play the Hearth through, and pick The Ridge on the world map. Or start the mission `MS2 - The Ridge` the way you usually test a mission.
3. Opening: the camera goes from Linda to the high path, then the pair's two lines, the camera back, the two Role lines. Then the enemy cards (the Claws and the Masher) play, and only after them do input and the HUD return.
4. Enemy turn 1: a Claw next to Linda draws Watch; a Claw hitting Linda from 2,0 or 1,1 draws Mark's Counter.
5. Kill the three pack Claws. The camera runs to the Masher, then "I'll knock it over." / "Don't stand next to it. Aim at it…". Aim an ability at the Masher to see its slam preview. The objective reads "Get past the Masher."
6. On the next family turn, the camera shows two Claws arriving at the top of the room (1,4 and 3,4) and Linda's bark.
7. Catch & Return: Linda on 3,0, Mark on 7,0 (via the ledge 4,3 → 8,3 → 8,0). Each caught arrow hits the Masher out and back. It has about 36 HP.
8. Kill the Masher, then the rest ("Clear the ridge."). Win: the close-up on the clue at 12,0, the clue lines, the outro, then the drops (Gold 20, Steel 2, XP 30).

## Resume from

The build is complete. Next: the coordinator's look and THJ's play check with a win (step 8 above). Then the review together with chunk 3.2.
