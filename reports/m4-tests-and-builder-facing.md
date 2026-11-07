# Report: Memory 4 tests follow THJ's prefab; Build Level From Grid sets enemy facing

Plan: none (coordinator brief, 2026-11-06)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done

## What changed

Task 1 (tests follow the prefab; prefab and sequences untouched except the one asset in the small addition below)
- `Features/Onboarding/Editor/HearthMemoryMarkTests.cs`: 15 Claws (4 Bloom, 2 den, 2 arrival, 3 top hidden, 2 top visible, 2 left), each now also checked for zero experience; three hidden groups (arrival, top, left); scripted tiles include the PostBloom Claw walk target; the John-walks-three-tiles geometry line is gone (John now starts on (4,2) and is scripted to (7,2)); new `LethalXpBonusOf` helper.
- `HearthMemoryMarkTests.Flow.cs`: stages 1 and 2 end on objective or cap, stage 3 needs both objectives; stage 3 test rewritten (six Claws all dead or cap 4; John on the den mouth or cap 4; both objective texts); Bloom cut-in test follows the new order and lines; arrival test follows the nested PostBloom sequence; new test for the PostBloom (left reveal before any walk, the three Claw walks by tile, John to (7,2), arrow unlock once); new `Conditions` helper.
- `HearthMemoryWiring.Mark.cs`, `.Layout.cs`, `.Level.cs`: constants moved to the prefab only as far as the tests read them (John start, cub tiles, top Claw tiles, den-edge health as per-Claw floats incl. 12.48, `LeftClaws`/`LeftGroupId`, `PostBloomClawWalkTo`, `SaveStageClaws`, current objective texts; `TurnsLeftText` renamed `SaveCapObjectiveText`). `ClawPlan` health became float and includes the left Claws. The tool stays retired and not rerun.

Small addition (John's gesture)
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Bloom_John_UnitAnimationSequence.asset`: `mode` 2 to 3 (HoldLastFrame), nothing else. The Bloom cut-in test now pins it (and John's nickname).

Task 2 (builder facing)
- New `Core/Levels/Editor/GridToLevel/GridToLevelBuilder.Facing.cs`: `TryGetMainGroupCentre`, `EnemyShouldFaceRight` (the small testable rule) and `FaceEnemiesTowardsTheFamily`.
- `GridToLevelBuilder.cs`: one call, right after the grid is built and before the xp zeroing. Nothing else.
- New `GridToLevelFacingTests.cs`: 7 rule tests, 3 build tests.

## Acceptance criteria

- [x] The ten reds green, tests pin THJ's values: `HearthMemoryMarkTests` 31/31 pass (30 old, 1 new). Pinned: positions, 15 Claws with health and hidden state, zero XP per Claw, stages and aggregation, reveal groups, ordering, texts, destinations.
- [x] `NothingInTheHearthGivesExperience` is green in the full run (THJ fixed the two Claws; no test change).
- [x] `mode` of John's gesture: pinned as HoldLastFrame, per the later instruction.
- [x] Builder sets `initialDirection.x` = 1 on enemies left of the main group, new builds only, existing levels not touched: `GridToLevelFacingTests` pass; the enemy prefab asset is checked unchanged.
- [x] Full EditMode run before my last small test edit: 1463 tests, 2 failed (`AIRegressionTest.Baseline_MatchesCurrentAI`, and my PostBloom test, fixed after). The Mark and Facing classes were then rerun: 41/41. I did not rerun the whole suite after that last fix; the only code touched since was that one test.

Needs the verifier or THJ: nothing needs a play check for the tests; building a level with enemies left of the family and looking at the facing is the play check for Task 2.

## Save reset

no

## Decisions I made

- "Main group" rule: heroes (placed player-faction units, plus `level deploy` slots) are grouped by column, a gap above 3 columns (`MaxGroupGap`) splits them, the largest group is the main group (leftmost on a tie), and an enemy whose column is left of that group's middle gets x = 1. The middle (not the left edge) because THJ's prefab turns the Claws directly above Lucy and Linda (column 3) right; a left-edge rule would leave them facing left. With his heroes (3, 3, 4, 14) Mark is dropped and the middle is 3.5; his prefab's facing agrees with the rule for every Claw.
- Big units use their anchor column. A level with no player faction on its template is left alone. y of the direction is kept.
- Test names and comments in the wiring file say the hold stage text is "John: Cut the reinforcement path." etc.; the texts are pinned as constants and will need updating whenever narrative rewords them (same as before).
- Dropped pins, because they are camera tuning rather than rules: `Arrival_CameraOnMark` focus on Mark's cell (it is now (7.25, 1.75)), the Bloom `CameraToDen` step (gone from the cut-in; the test now asserts the cut-in has no camera step). Nothing was deleted to get green; the old Bloom geometry check lost only its John line.
- The PostBloom test's "walk end is free" check allows a Claw the Bloom kills: the left Claw on (3,7) walks to (3,5), which a stage-1 Claw holds at the start.
- Kept `HearthMemoryWiringMark` out of date where tests don't read it (retired tool): hidden groups in `WireLayout` don't include `left`, and the sequences builder is untouched.

## Needs THJ

none

## Docs to update

- `claude-config/skills/miso-level-chunks/SKILL.md` (Enemy facing, line 110) and "Not from the block yet" (line 113): the build now sets facing for new levels; the rule is as above. Coordinator to update.
- Build log entry; Segment 4 of the onboarding plan still shows the old design (already noted in the review).

## Risks and loose ends

- The den's east Claw has 12.48 health (unit factor 1.3, others about 0.6 to 1.04): looks deliberate for stage 3, mention only.
- The rule's enemy-in-the-same-column case (x equal to the middle) keeps the default. An enemy right above a lone hero column faces left.
- A single hero or deploy slot makes that column the middle: enemies strictly left of it turn.
- `__CameraStartTest` did not come back under Content/Levels/Greybox (checked).
- Unstaged and left alone as told: `AIFactionBrain.cs`, `AIUnitBrain.cs`, TMP fallback font, `PreloadScreen.unity`, `ProjectSettings/*`. `GB_m4-mark.prefab` is not modified.
- `AIRegressionTest.Baseline_MatchesCurrentAI` is red as expected (42 failures), untouched.

## Proposed commits

1. `test(onboarding): the Memory 4 tests follow the hand-tuned level` (plain): `HearthMemoryMarkTests.cs`, `HearthMemoryMarkTests.Flow.cs`, `HearthMemoryWiring.Mark.cs`, `HearthMemoryWiring.Mark.Layout.cs`, `HearthMemoryWiring.Mark.Level.cs` (under `miso/Assets/_Project/Features/Onboarding/Editor/`). Needs the John asset commit first if the HoldLastFrame pin is in the same run, so commit 2 goes before it.
2. `fix(onboarding): John's Bloom gesture holds its last frame` (plain): `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Bloom_John_UnitAnimationSequence.asset`. Commit this first (the test in commit 1 pins it).
3. `feat(levels): Build Level From Grid turns enemies left of the family to face right` (plain): `GridToLevelBuilder.cs`, `GridToLevelBuilder.Facing.cs` + `.meta`, `GridToLevelFacingTests.cs` + `.meta` (under `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/`). Independent of 1 and 2.

Order: 2, 1, 3 (3 can go anywhere).

## Other branches

none

## How to see it

1. Test Runner > EditMode > Run `HearthMemoryMarkTests` and `GridToLevelFacingTests` (41 tests, all green).
2. Facing: draw a block like `c c . L U . c . . . . . . . . M` with no `level` lines, run Tools > Levels > Build Level From Grid, open the new prefab: the two left Claws have `initialDirection` (1, 0), the right one (-1, 0). Delete the prefab after.
3. John's gesture: open `GB_m4-mark` and let the level start; he should freeze on the last frame of the gesture until his idle step (THJ to look).
