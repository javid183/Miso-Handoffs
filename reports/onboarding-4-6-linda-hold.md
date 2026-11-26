# Report: M1 "The Ridge" round 4.6, Linda waits until Mark reaches the ledge

Plan: plans/2026-11-25-m1-ridge-4-6-tech.md    Agent: miso-implementer (opus)    Branch: thj/onboarding-demo
Outcome: done (not played; THJ's play check owed)

## What changed

- `Features/Onboarding/HoldUnitsUntilSignal.cs` (new, + `.meta`): feature component. Gives its units `Status.Inactive` (the player controller's skip-turn tag) and removes it on `Release()`. Only removes a tag it added. Starts holding the first time another faction's turn ends (see Decisions). A release during the units' own turn gives back the AP the hold took at that turn's start, refreshes the unit panel and marks the unit energetic. Listens to `turnStarted`/`turnEnded` on the bus while enabled, guarded against the AI worker thread. No statics.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Hold.cs` (new, + `.meta`): partial. `ReleaseLindaSignal = "M1Ridge_ReleaseLinda"`, the release `SignalSequence` (`M1Ridge_Catch_ReleaseLinda`), `EnsureFirstStep` (puts it first in the existing Catch list, only once), `WireHold` (component on "Ridge Switches" with Linda, plus a listener that calls `Release`).
- `Features/Onboarding/Editor/MissionWiring.Ridge.cs`: switches holder goes from 4 to 5 listeners and calls `WireHold`. Comments updated.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs`: `BuildCatch` builds the release step first and puts it at the head of the seed list.
- `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.cs` (new, + `.meta`): 11 tests (8 component, 3 wiring).
- `Content/Levels/Greybox/GB_m1-ridge.prefab`: "Ridge Switches" gains `HoldUnitsUntilSignal` (units: Linda) and a fifth `SignalAction` (`M1Ridge_ReleaseLinda` → `Release`). Only additions: +45 lines.
- `Resources/Sequences/M1Ridge/M1Ridge_Catch_SequentialSequence.asset`: the release step inserted at index 0 (+1 line).
- `Resources/Sequences/M1Ridge/M1Ridge_Catch_ReleaseLinda.asset` (new, + `.meta`): SignalSequence with key `M1Ridge_ReleaseLinda` and duration 0.

Diff stat (tracked): prefab +45, Sequences.cs 8 (+5/-3), Ridge.cs 12 (+8/-4), Catch asset +1. Totals: 4 files, 59 insertions, 7 deletions. New files: component 205 lines, wiring partial 55, tests 231, release asset 17, plus 4 `.meta` files.

## Acceptance criteria

- [x] Linda can't be selected or moved on the family's first turn until the ledge stage completes. How: the skip-turn tag is checked by `IsSelectableUnitCell`, `UnitSelectionState.ApplyCondition`, `ToPlayUnits` and `AutoSelectUnit`. Tests: `HoldingAddsTheTagAndReleasingRemovesIt`, `TheHoldTagIsWhatThePlayerControllerSkips`, `TheHoldStartsWhenAnotherFactionsTurnEndsNotItsOwn`. In-game behaviour needs the play check.
- [x] Release doesn't remove a pre-existing tag: `ReleasingLeavesATagSomethingElseSet`.
- [x] A restarted level holds again: `ARestartedLevelHoldsAgain`. A restart reloads the level (`GameHandler.RestartLevel` → `LoadLevel`), so the component starts fresh. No static state.
- [x] Wiring: component on the level with Linda only (`TheRidgeHoldsLindaOnly`). The release signal calls `Release` (`TheRidgesReleaseSignalReleasesTheHold`). The release is the Catch sequence's first step, exactly once (`TheLedgeStagesEndReleasesLindaFirstAndOnce`).
- [x] Prefab cells and units unchanged: `level_to_grid.py` output is identical before and after (six-unit ambush pack still hidden). Health factors and active flags untouched (the prefab diff only adds the two components).
- [ ] Visual and turn flow in Play: not played (no Play session without THJ's OK). Needs the play check below.

## Chunks

### Chunk 1 (whole plan): Linda's hold

- Changed: all files listed above.
- Criteria met: see above. Compile clean. Covering tests 70/70 (HoldUnitsUntilSignalTests, M1RidgeTests, M1RidgeLayoutTests, PouchHintAndDefeatRelaxTests, LevelPassByOffTests). Full EditMode suite 2782: 2781 passed, 0 failed, 1 skipped (Explicit AI baseline); the last recorded run was 2770/2771 plus the 11 new tests. `AIRegressionTest.Baseline_MatchesCurrentAI` run by name: 46 failures of 733 checks, the same as the last recorded count. Not strictly needed (no AI graphs, abilities or unit prefabs changed), but the plan asked for it.
- Decisions and loose ends: see the sections below.

## Check during the build (each answered)

1. **Turn ends as usual while Linda is held.** `FactionPhaseData.ToPlayUnits` leaves out skipped units, so once Mark is out of AP, `TakeActionState.GetNextState` returns null and the turn-end request goes out (`RequestEndTurnSafe`). There's no stall waiting for Linda. Mark is always selectable, and `AutoSelectUnit` picks only from `ToPlayUnits`, so the turn can't end on its own before Mark acts. In `Reinitialize`, a skipped unit gets `Consume(Closure)` (0 AP) at the turn start. That is why the release gives her AP back (see Decisions).
   - **Race to watch in the play check:** when Mark reaches the ledge with his **last** AP, the turn-end check (`ToPlayUnits.Count <= 0`) runs right after `abilityPerformed`. `abilityPerformed` drives `UpdateObjectives` → the stage completes → `SequencePlayer.Play(Catch)`. Unity starts nested coroutines synchronously, so the release step (signal, then `Release`) should run inside that same call, before the check. Linda is then counted and the turn stays open. If the stage completion slips to a later frame, the turn end is already queued and runs after the Catch sequence, and Linda loses her shot. One known way that could happen: an objective re-check deferred by a death on that very frame. Mark's Blitz waits for the dead Claw to leave its tile before hopping on, so this should not occur, but I did not verify it in Play. If it shows up, the fix touches the turn switch (core).
2. **Other readers of `Status.Inactive`:**
   - AI targeting of Linda: not affected. `AIFactionBrain` only skips its own units. No AI graph or ability asset references the tag.
   - Objectives: the player controller's `objectivesIgnoreTagsQuery` is `EntityState.IgnoreObjective`. The AI controller's lists `Status.Inactive`, but it applies only to AI-faction units. TilesOccupied, LivingUnits and defeat counts are unaffected (no objective code calls `IsUnitTurnSkipped`).
   - FR / Watch: `PlayerController.CanAffordFactionRole` returns false for a skipped unit, so a held Linda can't Watch. That is why the hold starts only after the enemies' opening turn, and the release comes at the latest at the start of the enemies' second turn (fallback). Her Watch is therefore never blocked.
   - Duo: Family Footrace is locked until the reunion anyway.
   - Pass-by: the handler's `excludedTags` lists `Status.Inactive`, so a held Linda gives and receives no Pass-by. The siblings are split by the rock on turn 1, so this has no effect.
   - Revenge: `revengeTagQuery` expects the tag absent, so a held Linda wouldn't take revenge if Mark fell. The level is lost with one down at that stage anyway.
   - Catch & Return: once released in the same turn, Linda is not skipped and has her AP back, so she is a valid shooter. The Catch sequence's select step then selects her.
   - MissionMap and John's target query: not in this level.
3. **Fallback path:** stage 1's turn fallback completes at the start of the enemies' second turn → Catch → release first. The family's turn is not open then, so no AP is given back. The family's second turn resets her AP as usual (she is no longer skipped), and her bar unlocks in the same Catch sequence. One small difference from before: with 0 AP during the first family turn she converts no unused AP to ATB steps at that turn's end (`ConvertUnusedApToAtbSteps`). Before 4.6 an idle Linda did.
4. **Exact moment:** the hold goes on in `turnEnded` of the enemies' opening turn. `CombatLevelRunHandler.SwitchTurnIE` then waits `timeBetweenFactionTurns` and calls `PlayerController.StartTurn`, which auto-selects a unit and gives input back. So the tag is in place before the family's first turn and before any click. Between the Family Role page and that point, input is off (rockfall sequence) or it is the enemies' turn.

## What it looks like (visual)

At the family's turn start, `Consume(Closure)` drops her AP to 0. That raises `APConsumer.OnValueChange` → `GUnit.HandleExhaustion` → `goExhausted`, so she looks exhausted like a spent unit. The component also calls `MarkExhausted` on her own turn start while held. On a release during the family's turn, AP comes back (a silent reset), followed by `MarkEnergetic` and a unit-panel refresh. Not seen in Play; THJ to confirm.

## Reviews and checks

- (written by the coordinator)

## Review fixes

The review (APPROVE) accepted both deviations and asked for two should-fixes and one check.

1. **A release before the hold now cancels it.** `Release()` with no hold in place sets `Released = true` and returns, so a later turn end never starts the hold. New test: `AReleaseBeforeTheHoldMeansNoHoldWhenATurnEnds`.
2. **AP restore tested in edit mode.** An `APConsumer` can be built in edit mode with the same per-unit AP attribute setup `ActionCompletionChargeTests` uses; `IsAlive` is set by reflection. Two new tests:
   - `AReleaseDuringTheFamilysTurnGivesThePointsBackOnce`: AP goes 0 → 2 on the first release; after spending again, a second release leaves 0.
   - `AReleaseOnAnotherFactionsTurnGivesNoPoints`: a release outside the family's turn stays at 0.
3. **Barks while Linda is held (reported, not changed).** `BarkManager.CanSpeak` rejects a speaker that matches `ignoredSpeakerTagsQuery` (which lists `Status.Inactive`, set in `CombatLevelContainerScene`). In `ShowBark` the bark is then dropped: no other speaker is picked and nothing is logged unless debug logging is on. The hold lasts from the end of the enemies' opening turn until the release (on the main path within the family's first turn; on the fallback, at the start of the enemies' second turn). During that time:
   - **The Ridge's low-health bark** (`Bark_Phase_M1Ridge_LowHP`) runs at the start of the family's turn. If **Mark** is under half health then, the speaker is Linda, so on the family's first turn that line is dropped. It plays at a later family turn start if he is still under half (each line plays once per save). Linda being hurt makes Mark speak, which still works. Whether Mark can be under half after the enemies' opening turn depends on the Claws' reach; I did not check it in Play.
   - **The general low-health bark** (`Bark_Phase_CharacterHealth_Low`, with Linda's own lines such as "I can still draw the bow.") is dropped for Linda on the family's first turn too, if she is hurt.
   - **Enemy-killed barks** (`Bark_EnemyDied`): branches on the dead enemy's type and its `Killer` output; the speaker comes from the CSV's Unit column. Mark's ledge kill would normally give a Mark line. If a branch can hand a Mark kill to a Linda line, it is dropped while she is held. I did not trace every branch of the graph.
   - **Unit-selected barks:** Linda can't be selected while held, so none.
   - **Family Footrace barks:** locked until the reunion.
   - **Forced barks:** none. No M1 sequence has a bark step.
   - After the release (the Catch sequence's first step) she barks normally.

Tests after the fixes:
- 14 new tests, all passing (was 11).
- HoldUnitsUntilSignalTests + M1RidgeTests + M1RidgeLayoutTests: 60/60.
- Full EditMode suite: 2785; 2784 passed, 0 failed, 1 skipped (the Explicit AI baseline).
- AI regression not re-run, since no AI content changed after the 46-failure run.

Files touched by the fixes: `HoldUnitsUntilSignal.cs` (now 210 lines) and `HoldUnitsUntilSignalTests.cs` (now 302 lines). Both are LF with no BOM, and they belong to the same proposed commit.

## THJ's tweaks folded in

THJ play-checked 4.6 (all good) and then tuned the level and its sequences himself. His version is now the truth. This round makes the wiring and the tests match it, so running the menu again keeps his work.

**His tweaks, and what the wiring does now**
- **Two more rocks** on prefab tiles (2,1) and (3,3), in a new hidden group `ambush-rock`.
  - Layout: `AmbushRockGroupId = "ambush-rock"`, `AmbushRockTiles = {(2,1),(3,3)}` (the group's own order).
  - `EnsureAmbushRocks` reuses the rock already on each tile, or places one from the rock prefab, and hides it.
  - `SetHiddenGroups` writes the fourth group. Before this change, a re-run would have dropped it, since the groups are written whole.
- **Ambush units saved active.** THJ saved the Black Claw and all five ambush Dark Claws active (the six `m_IsActive` 0→1 changes from his hidden-group toggle button).
  - The two new rocks also had no `m_IsActive` 0 override, so they would have been in play from the start. Their group membership and the reveal step say they are meant to be hidden.
  - All eight are back to inactive. That diff is only `m_IsActive` changes: the six flipped back and two override entries added for the rocks.
- **The ambush step list:** `M1Ridge_Rockfall_Shake` then `M1Ridge_Ambush_RevealRock` (group `ambush-rock`, waitAfterReveal 0.6, which is also the field's default) right after the discovery dialogue, before the west-path camera. `BuildAmbush` builds the same two steps in the same place.
- **The cleared step list** no longer has the plateau camera and the plateau dialogue. `BuildCleared` no longer builds them, and its seed list matches.
- **Lines** are now constants in `MissionWiring.Ridge.cs` and used in the seeds:
  - `DiscoveryWarningLine = "Mark. Listen. Not again!"`
  - `BellLine = "Six. Hit the big one only at my side."`
  - The dialogue assets already held THJ's text and are seeded once, so they were not rewritten.

**Re-run check.** Before running the menu I copied the prefab, the M1Ridge sequence folder, the mission and the rock prefab, then compared each with its copy afterwards.
- No step-list warnings: the ambush and cleared seeds match THJ's lists.
- Mission and rock prefab: unchanged.
- Prefab: only the intended `m_IsActive` changes, plus the known reorder of the ambush unit list (same units). I put the list back in THJ's order by hand.
- The two ambush camera assets gained (0.75, 0.75) again (the known loose end, not one of his tweaks). I restored them from the copies.
- `level_to_grid.py` read-back: same cells, units and groups as THJ's version. The "listed but active" warnings for the six ambush units are gone.

**Tests**
- M1RidgeLayoutTests:
  - `Rock()` now means the rock on the shared tile.
  - The groups check lists `ambush-rock`.
  - New `TheAmbushRocksWaitHiddenOnThePlateauPaths`: two rocks from the rock prefab, hidden, not on a Claw's tile or in the top zone, three rocks in all.
  - `TheRockIsNeitherAnEnemyTargetNorCountedByClearingTheRidge` is renamed `NoRockIsAnEnemyTargetOrCountedByClearingTheRidge` and now checks all three rocks: Neutral faction, Neutral allied with Enemy, and clearing counts only the Enemy faction.
  - `TheAmbushPackWaitsHiddenOnBothPathsAndStartsAlert` needed no change; it failed only because of the active flags.
- M1RidgeTests:
  - The ambush test now expects two reveals, the shake and the rock reveal right after the discovery dialogue, the discovery's last line equal to `DiscoveryWarningLine`, and the bell dialogue's first line equal to `BellLine`.
  - `ThePocketClearedGivesTheReunionAndThePlateauButNoPotionPage` is renamed `ThePocketClearedGivesTheReunionWithTheCameraStayingOnTheFamilyAndNoPotionPage`: no camera step, and control comes back right after the top-up.
- Results:
  - HoldUnitsUntilSignalTests + M1RidgeTests + M1RidgeLayoutTests: 61/61.
  - Full EditMode suite: 2862 total; 2856 passed, 5 failed, 1 skipped (the Explicit AI baseline).
  - The 5 failures are all in `M3DefenceTests` (three `EachHoldStageIsThePickHoldingThePushTileForOneTurnStart` cases, `StageTwoIsThePickOnThePushTileLitAsAGoal...`, `TheLevelIsLostWhenNoBergsonStandsOrThePickFalls`). Confirmed cause: THJ's local `GB_m3-defence.prefab` change replaces five managed-reference ids with `-2` (null), so those objective conditions read as null. I did not touch that file.
- AI regression not re-run: no AI graph, ability or unit prefab changed (the rocks reuse the existing rock prefab).

**Assets now unused (not deleted):** `Resources/Sequences/M1Ridge/M1Ridge_Cleared_CameraToPlateau.asset` and `M1Ridge_Plateau_DialogNodeSequence.asset`, each with its `.meta`. Nothing references them.

**Still open (unchanged):** a re-run still re-adds (0.75, 0.75) to `M1Ridge_Ambush_CameraOnEastPath` and `M1Ridge_Ambush_CameraOnFamily`, and reorders the ambush unit list, until those builders follow the hand-tuned assets.

**Files touched this round**
- Code: `MissionWiring.Ridge.Layout.Ambush.cs` (+9), `MissionWiring.Ridge.Layout.cs`, `MissionWiring.Ridge.Sequences.cs`, `MissionWiring.Ridge.cs` (constants and comments).
- Tests: `M1RidgeLayoutTests.cs`, `M1RidgeTests.cs`.
- Asset: `GB_m1-ridge.prefab` (`m_IsActive` only, on top of THJ's version).
- THJ's own files belong in the same commit: his prefab edits, `M1Ridge_Ambush_RevealRock.asset` + `.meta`, `M1Ridge_Ambush_SequentialSequence.asset`, `M1Ridge_Cleared_SequentialSequence.asset`, and the two dialogue assets.
- All code files are LF with no BOM.
- Diff stat, tracked files in scope (THJ's edits and the 4.6 work included): 12 files, 322 insertions, 47 deletions.

**Proposed commits, revised.** Commit 1 stays as listed. Add a second commit after it:
- `feat(onboarding): The Ridge drops two more rocks as the ambush comes, recounts the pack and cuts the plateau camera`
- Files: THJ's assets above, plus the layout, sequence and line changes and the two test files.
- Some files carry hunks of both commits (the prefab, `MissionWiring.Ridge.cs`, `MissionWiring.Ridge.Sequences.cs`). If a split by hunk is too fiddly, the two commits can merge into one.

## Save reset

No.

## Decisions I made

- **The hold starts when the enemies' opening turn ends, not at level start** (plan: "at level start (before the first family turn)"). Holding from level start would block Linda's Watch on that enemy turn (`CanAffordFactionRole` checks the skip tag). The Watch page and her line "Anything in my line gets an arrow" set that turn up. The rule in code: the first end of another faction's turn starts the hold. The turn order here is Enemy, Family, Neutral. Same stated behaviour on the family's turn. Tier 2.
- **The release gives back the AP the hold took** (only during the family's open turn, only if the hold was on at that turn's start, only if she has 0). Without it, Linda released mid-turn has 0 AP: she couldn't take the catch shot, and since she wouldn't count in `ToPlayUnits` the turn would end. This matches the 4.5 behaviour, where she had full AP on turn 1. Tier 2.
- New partial `MissionWiring.Ridge.Hold.cs` instead of growing `MissionWiring.Ridge.cs` (571 lines). The existing `WireSwitches` only changed its listener count and gained one call.
- Wiring tests live in `HoldUnitsUntilSignalTests` (as `PouchHintAndDefeatRelaxTests` does), since `M1RidgeTests` is not partial.

## Needs THJ

None, beyond the play check. If the turn-end race above shows up, fixing it touches the turn switch (core): a decision then.

## Docs to update

- `design/demo-spec.md` / M1 paper level (designer): on the family's first turn only Mark acts; Linda is held until he reaches the ledge or the round moves on.
- `tech/core-systems.md`: nothing (no core change).

## Risks and loose ends

- The turn-end race when Mark reaches the ledge with his last AP (see check 1). It is the key thing to watch in the play check.
- **Re-running the wiring menu has side effects outside 4.6** (already known as a loose end): it adds (0.75, 0.75) (prefab tile 1,1) to `M1Ridge_Ambush_CameraOnEastPath` and `M1Ridge_Ambush_CameraOnFamily`, and reorders the ambush hidden-group unit list (same units). After my run I hand-reverted those three hunks to their committed state (small YAML edits, Unity re-imported). The diff now holds only the 4.6 additions. Any later re-wire will bring them back until the layout or wiring tool is fixed.
- Fallback: Linda earns no unused-AP ATB steps at the end of the family's first turn (she has 0 AP while held).
- The bell line still says "Five" (pre-existing loose end, untouched).

## Proposed commits

1. `feat(onboarding): The Ridge holds Linda out of the family's turns until Mark reaches the ledge`. Files: `Features/Onboarding/HoldUnitsUntilSignal.cs` + `.meta`, `Features/Onboarding/Editor/MissionWiring.Ridge.Hold.cs` + `.meta`, `Features/Onboarding/Editor/MissionWiring.Ridge.cs`, `Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs`, `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.cs` + `.meta`, `Content/Levels/Greybox/GB_m1-ridge.prefab`, `Resources/Sequences/M1Ridge/M1Ridge_Catch_SequentialSequence.asset`, `Resources/Sequences/M1Ridge/M1Ridge_Catch_ReleaseLinda.asset` + `.meta` (plain; one unit, since the prefab references the new component and the tests check the wiring).

Do not stage: `LevelM2-C1.prefab`, `miso.slnx`, `M1Ridge_Cleared_PotionPage.asset` (+ `.meta`).

## Other branches

None.

## How to see it

1. Play `MS2 - The Ridge` from the start (or the level directly).
2. After Linda's Family Role page, let the enemies' opening turn play. If a Claw ends in her line, her Watch prompt should still appear.
3. The family's first turn: Linda should look exhausted (greyed). Clicking her does nothing and Tab/switch never lands on her; only Mark is selected.
4. Main path: move Mark, then Blitz the ledge Claw so he lands on the ledge (8,3) with his **last** AP. Expect: the turn does **not** end. Mark's line plays, Linda's bar unlocks, she is selected with 2 AP and looks normal, and she can shoot through the Claws at Mark (the catch). **This is the check that matters most.**
5. Also try reaching the ledge with AP left over: same result, and Mark can still spend his remaining AP.
6. Fallback: on turn 1, don't reach the ledge and spend Mark's AP. The turn should end by itself (no waiting for Linda). At the start of the enemies' second turn the Catch plays (Linda released, bar unlocked). On the family's second turn Linda has her AP and is selectable.
7. Restart the level from the pause or defeat menu: Linda is held again on the first family turn.
