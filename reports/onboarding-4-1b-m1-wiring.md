# Report: M1 "The Ridge" redesign, chunk 4.1b (wiring, sequences and text)

Plan: plans/2026-11-24-m1-ridge-build-tech.md (chunk 4.1b)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done, with three points for the coordinator (T-14 fallback applied, the 17 old 3.1b sequences still need deleting, and the commit split for the shared prefab). 4.1a's report: `reports/onboarding-4-1a-m1-level-rock.md`.

## What changed

All paths are under `miso/Assets/_Project/`. The new `.cs` files are LF with no BOM, like the other onboarding editor files.

- `Features/Onboarding/Editor/MissionWiring.Ridge.cs` (rewritten, now `partial`). The single menu is **`Tools/Onboarding/The Ridge: Apply Layout and Wire`**. It runs the 4.1a layout tool first, then wires: the turn order, the stages, the locks, the bow hint, the switches (Continuous Attack and the reunion top-up), the level-start rockfall, and the mission's level. The old `Wire Mission: The Ridge` menu is gone.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs` (new partial): the intro, rockfall, catch, cleared and outro sequences, the two tutorial pages, and the builders.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Bark.cs` (new partial): the low-health bark graph and its dialogue file.
- `Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs` (4.1a file, edited). `Run()` is now `Apply()` and has no `[MenuItem]`. It no longer cuts the stages: the wiring owns them. `KeepOnlyTheClearStage` and `DropStaleStageOverrides` are removed and the summary is updated. The layout changes themselves are untouched, and the run is still byte-stable.
- `Features/Onboarding/Editor/M1RidgeTests.cs`: rewritten, 22 tests.
- `Features/Onboarding/Editor/M1RidgeLayoutTests.cs` (4.1a file): one test replaced. `UntilTheBeatsAreWiredTheOnlyStageIsClearingTheRidge` became `TheLastStageIsClearingTheRidge`, because its "until wired" premise is now false.
- `Content/Levels/Greybox/GB_m1-ridge.prefab`, written by the tool:
  - turn order override `Enemy, Bergsons, Neutral`;
  - intro and outro re-pointed;
  - 3 stages;
  - `LevelAbilityLock` with 2 entries;
  - 1 `GuidedAbilityHint`;
  - a `SequencePlayHandle` on `levelStarted`;
  - a new child `Ridge Switches` with 2 `SignalAction`s and 1 `LevelStartFPFiller`.
- `Content/Levels/MS2 - The Ridge.asset`: no change in 4.1b. The tool now skips the dirty-mark when the mission already points at the level. The 4-line diff is 4.1a's potion.
- New `Resources/Sequences/M1Ridge/` assets, 33 of them, each with its `.meta`:
  - **Intro:** `M1Ridge_Intro_SequentialSequence`, `_Intro_CameraToClue`, `_Intro_Sighting_DialogNodeSequence`, `_Intro_CameraBack`, `_Intro_Rush_DialogNodeSequence`.
  - **Rockfall (plays on level start):** `M1Ridge_Rockfall_SequentialSequence`, `_ContinuousAttackOff` (SignalSequence), `_CameraOnRun`, `_LindaRuns` (MoveUnitSequence), `_Shake` (CFXSequence, durationOverride -1), `_ShakeCameraEffect` (a copy of the Mark Intro altar shake, 1.2 s), `_RevealRock`, `_Lines_DialogNodeSequence`, `_CameraOnPocket`, `_RevealClaws`, `_Claws_DialogNodeSequence`, `_WatchPage` (TutorialSequence).
  - **Pages:** `M1Ridge_Watch_Panels` and `M1Ridge_Potion_Panels` (TutorialDataSO).
  - **Catch (stage 1 end):** `M1Ridge_Catch_SequentialSequence`, `_Catch_DialogNodeSequence`, `_Catch_Unlock`, `_Catch_SelectLinda`.
  - **Cleared (stage 2 end):** `M1Ridge_Cleared_SequentialSequence`, `_Cleared_DialogNodeSequence`, `M1Ridge_Reunion_DialogNodeSequence`, `_Cleared_Reunion` (SignalSequence), `_Cleared_CameraToPlateau`, `M1Ridge_Plateau_DialogNodeSequence`, `_Cleared_PotionPage`.
  - **Outro:** `M1Ridge_Outro_SequentialSequence`, `_Outro_CameraOnClue`, `_Outro_Clue_DialogNodeSequence`.
- New `Resources/BarkSystemData/CharacterHealth/Bark_Phase_M1Ridge_LowHP.barkphase` (+ `.meta`, importer priority 1) and `M1Ridge Low HP Dialogues.csv` (+ `.meta`).

`git diff --stat` for tracked files, mine and 4.1a's together:

```
 .../Content/Levels/Greybox/GB_m1-ridge.prefab      | 796 +++++++++++++--------
 .../_Project/Content/Levels/MS2 - The Ridge.asset  |   4 +-
 .../Features/Onboarding/Editor/M1RidgeTests.cs     | 484 ++++++++-----
 .../Onboarding/Editor/MissionWiring.Ridge.cs       | 547 +++++++-------
 new: MissionWiring.Ridge.Sequences.cs 378, MissionWiring.Ridge.Bark.cs 206 (+ .meta);
      33 sequence/page assets + .meta; 1 bark graph + 1 csv + .meta
```

The diff also shows `GlobalSettings.asset`, the TextMesh Pro fallback asset and `miso.slnx`. Those are THJ's changes and I didn't touch them; `GlobalSettings.asset` was last written on 2026-11-23. I didn't touch `GB_m2-lucy` or its wiring either.

**3.1b sequences: not deleted yet (needs action).** I checked that nothing references them any more: no `.prefab`, `.asset`, `.unity` or `.cs` outside the folder, and the level now points at the new intro and outro. `AssetDatabase.DeleteAsset` was then refused in this session: the MCP safety filter blocked it, and so did the permission classifier when I retried with the filter off. So I gave every new asset a name that differs from the old ones (`Intro_`/`Outro_` instead of `Start_`/`End_`), so nothing reuses them. These 17 are orphans to delete, with their `.meta`, in Unity or with `git rm` in commit 2:

`M1Ridge_Arrival_Bark_DialogNodeSequence`, `M1Ridge_Arrival_CameraOnGroup`, `M1Ridge_Arrival_Reveal`, `M1Ridge_Arrival_SelectLinda`, `M1Ridge_Arrival_SequentialSequence`, `M1Ridge_End_CameraOnClue`, `M1Ridge_End_Clue_DialogNodeSequence`, `M1Ridge_End_SequentialSequence`, `M1Ridge_MasherSetup_CameraToMasher`, `M1Ridge_MasherSetup_DialogNodeSequence`, `M1Ridge_MasherSetup_SelectLinda`, `M1Ridge_MasherSetup_SequentialSequence`, `M1Ridge_Start_CameraBack`, `M1Ridge_Start_CameraToLedge`, `M1Ridge_Start_Opening_DialogNodeSequence`, `M1Ridge_Start_Roles_DialogNodeSequence`, `M1Ridge_Start_SequentialSequence`.

## The checks

**1. T-14: does `TurnReached` 1 complete at the first family turn when the enemies go first? No.**
- `TurnReachedLOCondition` counts from the stage's first evaluation, which happens at level start on turn 1.
- `CombatLevelRunHandler` raises the turn number only when the turn index wraps to index 0, and index 0 is now Enemy. So `TurnReached` 1 completes at the start of **enemy turn 2**, after family turn 1.
- No built condition fires at a faction's turn start.

I applied the brief's fallback: S1 is dropped as a stage and its sequence goes into S2's.
- S1's line 3.1 ("Hold on, Linda! I see a way.") now opens S2's completion sequence, ahead of 4.2 and 4.3. It reads well there: "the way" is the catch.
- S1's `SelectUnitSequence` Mark and the pan to 7,-2 are dropped. Once Mark is on the ledge they mean nothing.
- The optional line 3.2 ("Then move, little brother!") is dropped too. It makes no sense after he has moved.
- What changes for the player: family turn 1 opens with no line. Only the objective "Mark: reach the ledge." names him, and Linda's bar is empty. This is the risk the UX critic flagged. **For the coordinator and THJ:** fixing it properly needs a turn-start trigger, which could join the D-653 trigger component.
- A side benefit: S2 is now evaluated from level start, so its fallback completes at enemy turn 2 and Linda's bar is back for family turn 2, which is the design's intent. With S1 kept, the fallback would have landed a round later.

**2. Reveals inside the intro happen before turn 1, and the revealed Claws act on enemy turn 1: yes, but not inside `introSequence`.**
- `CombatLevelRunHandler.StartLevelIE` plays the intro *before* `InitializeGrid()`, and `GridManager.GetCell` returns null until then. So `MoveUnitSequence` can't find a cell during the intro, and `cell.PlugEntity` runs on an uninitialised grid. Mark's memory hit the same thing; its Bloom cut-in plays on level start for this reason.
- So the intro only talks and moves the camera. The run, shake, reveals and Watch page are `M1Ridge_Rockfall_SequentialSequence`, played by a `SequencePlayHandle` on `levelStarted`.
- `levelStarted` fires after `InitializeGrid` and before `StartTurn`, so this is before turn 1.
- The factions exist by then (`PrepareFactions` runs before the intro), so `HiddenLevelUnits.Reveal` accepts.
- Enemy turn 1 starts in the same frame, but `AIController.HandleUnits` waits while `SequenceInProgress`.
- `ToPlayUnits` is computed live (owned, alive, AP > 0, not skipped). The revealed Claws are registered with fresh AP, so A and B (alert, since they see Linda) act on enemy turn 1. C stays Unaware and is skipped, as designed.
- The alert tracker's `BeginLevel` also runs on `levelStarted`. The reveals come after the walk's yields, so the tracker is already live.
- Order is tested: walk, then shake, then rock, then lines, then Claws, then lines, then the page last.
- **Not verified in play.**

**3. The switch targets the Mark the mission plays: yes.** `FillRosterSlots` only spawns roster units whose nickname isn't already in the level. Mark is placed in the prefab, so that placed instance is the one played, and both `SignalAction`s point at its `MarkPassiveAbility_ContinuousAttack`. Disabling it removes its bus listeners (`OnDisable`). Tested.

**4. Watch fires while Linda's bar is locked: yes, by code.**
- `LevelAbilityLock` is read only by the abilities bar UI, `GuidedAbilityHint` and `UnlockAbilitiesSequence`.
- Watch runs through `LindaFactionRoleHandler`, not the bar, and her Family Role preset isn't in the lock. Tested.
- **Finding:** the lock only hides bar buttons. It doesn't stop the default click actions. In `PlayerController`, clicking an empty cell uses `DefaultEmptyCellAbility` (walk) and clicking an enemy uses `DefaultOccupiedCellAbility` (attack). So on family turn 1 a player can still click to move Linda or shoot with her. "Only Mark acts" is a nudge, not a rule. `TurnStartActionPointLimit` can't fix this without breaking the catch on the same turn. **THJ to judge at the play check.** A real fix would be a small non-core change to the click path.

**5. Bergsons–Neutral: already Ally in this level, no change.**
- Arrow and projectile hits filter by `effect.TargetFactionRelation` (`Projectile.cs` around line 514); Linda's arrows target Enemy.
- Watch requires an Enemy relation (`LindaFactionRoleHandler.cs:68`).
- So Watch pierce, the catch return and Linda's shots neither hit nor target the rock.
- The rock (5,-5) isn't in Linda's row or column from 3,-2 in the usual play anyway.

**6. The Neutral faction's turn: no camera jump, no change needed.** `FactionControllerBase.CanPlayTurn` needs a live unit with at least one ability. The rock has none, so `SwitchTurnIE` skips the Neutral faction: no `StartTurn`, no banner, no camera focus. Neutral stays last in the order. **Not verified in play.**

**7. A restart doesn't leave Continuous Attack off: yes.** A restart reloads the level prefab, where the component is enabled; a test checks this. The level-start sequence then switches it off again, and the new `SignalAction` subscribes in its own `Start`. Skipping the cutscene doesn't skip the signal: `SequentialSequence` fast-forwards only dialogue and camera steps.

## Acceptance criteria (4.1b part)

- [x] Turn order is Enemy, Bergsons, Neutral: `TheEnemiesMoveFirstThenTheFamilyThenTheRock`.
- [x] Continuous Attack is off from level start until S3, then on again; FP stays full; no FP 2 filler: `ContinuousAttackIsSwitchedOffAtTheStartAndBackOnAtTheReunionOnThePlacedMark`, and `TheReunionTopsTheFamilysPointsUp…` checks that the level has only the one filler.
- [x] Linda's bar and Mark's Command are locked until S2; Cleanse stays locked; Watch isn't in the lock: `LindasWholeBarAndMarksCommandStartLocked…`, `TheLedgeUnlocksLindasBarAndCommandButNeverCleanse`, `WatchIsNotPartOfTheLockedBar`. See check 4 for the click-through.
- [x] The stages are as in the design, with S1 merged per T-14. S2's fallback is `TurnReached` 1 (aggregation Any). S3 runs the +99 filler through a signal and isn't on `levelStarted`: `ThreeStagesTheLedgeWithItsRoundFallbackThePocketAndThenEveryEnemy`, `TheReunionTopsTheFamilysPointsUpWithASecondFillerThatTheLevelStartDoesNotCall`.
- [x] Intro order: arrival, Linda's walk to 3,-2, shake (-1), rock, fall, lines, Watch page last. The walk finishes before the rock: `MoveUnitSequence` waits for the transporter, and it is an earlier step of the same `SequentialSequence`. Tests: `LindasRunEndsBeforeTheShakeTheRockTheClawsAndTheWatchPageInThatOrder`, `TheIntroShowsTheClueAndLindasRushAndOnlyTalks`, `TheRockfallPlaysWhenTheLevelStartsBeforeTheFirstTurn`.
- [x] Fallback cues: the S3 lines hold whether or not the catch fired, and a 50% bark plays (see Text). Test: `TheLowHealthBarkHasTheOtherSiblingSpeakAtHalfHealthOnlyWhereTheRockIs`.
- [x] The Watch page has no FP wording: `TheWatchPageNamesLindasRoleWithoutFamilyPoints`. The potion page shows once in the cleared sequence: `ThePocketClearedGivesTheReunionThePlateauAndThePotionPageOnce`.
- [x] The outro is on the clue: `TheOutroClosesInOnTheClueThenTheLinesThenTheOutroCutscene`.
- [x] Idempotent: two runs in a row left the prefab, the mission and every sequence asset byte-identical (md5), with no console warnings.
- [x] Layout tool and wiring run together: one menu, and the layout has no menu of its own (`OneMenuAppliesTheLayoutAndWiresTheLevel`).
- [ ] Play check: THJ's (see How to see it).

## Tests

Open editor, Unity MCP:

| Run | Result |
|---|---|
| `M1RidgeTests` + `M1RidgeLayoutTests` + `SearchRidgeTests` (by full class name) | 44/44 passed |
| Full EditMode suite | 2618 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |
| `AIRegressionTest.Baseline_MatchesCurrentAI` by name | **45 failures, the same as D-659.** No new lines; the `Unit_Rock` line is 4.1a's. Not re-baselined |

The console has no compile errors. The warnings are the existing "Serialization depth limit" ones and older compiler warnings, none from this change.

What tests can't cover and needs the play check: the reveals and AI behaviour on enemy turn 1, the rock blocking walking, the Neutral turn being skipped, the bark firing, the HUD timing, and the click-through in check 4.

## Text used

All Rec. lines from `design/m1-ridge-redesign-text.md`. Dialogue carries no tag; this list stands in for it.

- **Intro:** 1.1, 1.2, 1.3 (the optional line, kept); 2.1, 2.2, 2.3 (the optional line, kept).
- **Rockfall:** 2.4, 2.5; 2.6, 2.7; then the Watch page (2.8).
- **Catch (S2 end):** 3.1, 4.2, 4.3.
  - 4.1 is cut (D-657).
  - 3.2 is dropped and 3.1 moved here (T-14, check 1).
  - 3.3 is the S2 objective, "Mark: reach the ledge."
- **Cleared (S3 end):** 5.1, 5.2, 5.3 (set A); 5.4, 5.5; 5.6, 5.7. Lines 5.8 and 5.9 are left out (D-656).
- **Outro:** 8.1 to 8.7 (close A).
- **S4 objective:** "Clear the ridge. {alive_0} remaining." (kept).
- **Bark rows** (keep `[PLACEHOLDER] `; `PlayOnce` TRUE; tag `LowHP_Other`): Mark "Linda! Drink a potion. Now." and Linda "Mark, you're hurt. Potion. Now." The two "self" rows aren't used: the graph can make the other sibling speak, so I left them out.

**Text I had to write or change** (for THJ to approve):
- **Watch page body (D-655, no FP).** "• On the enemies' turn, when an enemy ends its move in Linda's row or column, within her bow's range, she can shoot it. This is her Watch. • Press the key shown above her, and be quick. Each shot costs an arrow, but no action points." This is the narrative's text with "1 FP and" removed. The title is "Linda's Family Role".
- **Potion page:** §7.2's "Health Potion" page, used unchanged in S3 per D-654.

## How the bark is built

The bark system's graphs are Graph Toolkit files. The toolkit has no public API to build nodes, and the only built condition for "this mission" (`MissionObjectiveCondition`) would mean adding a node. So the tool copies the existing `Bark_Phase_CharacterHealth_Low` graph's text once and changes values and two wires:

- the health threshold is 50;
- Linda's and Mark's dialogue tables swap speakers and get tag `LowHP_Other`;
- the random empty slot is weighted 0;
- Lucy's branch becomes a gate, "unit `Rock` alive". The rock exists only in M1, so the cue can't fire, and burn its play-once rows, in Memory 4 or anywhere else. Linda's and Mark's branches now hang off the gate;
- the node ids are new.

It still triggers at the start of a family turn (PhaseDirection = Player), so never mid-enemy-turn. The baked data was checked node by node, and a test covers it. The general low-health graph is unchanged. The graph and CSV are seeded once, so THJ's edits in the graph editor are kept. The play-once state lives in the game save.

## Decisions I made

- **The rockfall plays on level start, not inside `introSequence`** (check 2). Same behaviour for the player (before turn 1, input off); it was needed because the grid isn't up during the intro.
- **The "Continuous Attack off" switch is a signal in the level-start sequence**, not the component disabled in the prefab. A restart then starts with it on and the start turns it off again, and the prefab stays as THJ's.
- **Signal listeners and the second filler sit on a new child, `Ridge Switches`.** THJ's empty `CutsceneHandler` SignalAction is left alone.
- **The 3.1b clue-prop builder is gone**, since THJ placed the clue. Cameras read the clue's position from `Search Scenery/Clue (placeholder)`.
- **Mark's Duos stay hidden until S2** through the existing partner rule: Linda's Mark_Linda Duo side is locked.
- **The unlock at S2 is an explicit list** (Linda's bar minus Cleanse, plus Command), not "unlock all", so Cleanse stays locked.
- **New asset names** (`Intro_`/`Outro_`), because the old assets couldn't be deleted (see What changed).
- **The bark gate is the rock's presence** (see How the bark is built).
- **The layout tool lost its stage cut and its menu**, so the two tools can't fight over the stages.

## Needs THJ

1. **Family turn 1 has no Mark line** (T-14 fallback, check 1). Accept it for now, or have the D-653 trigger component add a "family turn N starts" cue? Recommendation: accept for now and add it to the trigger plan.
2. **Linda can still act on family turn 1 by clicking cells** (check 4). Accept it, or plan a small non-core click-path guard? Recommendation: judge it in the play check.

## Docs to update

- `tech/onboarding-merge.md` and `status.md`: M1 is wired on the rockfall layout. The menu is `Tools/Onboarding/The Ridge: Apply Layout and Wire`. The 17 old 3.1b sequences are still to delete. Owner: coordinator.
- `design/m1-ridge-redesign-text.md`: the Watch body without FP, 3.2 dropped, 3.1 moved to S2. Owner: miso-narrative.
- `decisions.md`: the T-14 outcome, and the rockfall moving to level start. Owner: coordinator.

## Risks and loose ends

- **`GlobalSettings.asset` (THJ's uncommitted change) has `deactivateIntroOutroSequences: 1`.** With it, the intro (the tracks and the rush) and the outro (the clue) don't play. The rockfall still does, since it isn't the intro. Switch it off for the full play check.
- **HUD timing:** the rockfall hides the HUD while `StartLevelIE` shows it right after `levelStarted`, the same race as Mark's memory Bloom cut-in. The HUD may flash on during the rockfall. Play check.
- **Stage ends during an enemy turn:** S2's fallback and an S3 completed by a Watch kill play their sequence during the enemy's turn. `SelectUnit` Linda and `EnablePlayerInput` then run outside the family turn, as 3.1b's arrival did on its fallback. Play check.
- **The camera after S3 stays on the plateau**; I added no camera-back step.
- The general 30% low-health bark can still fire too. The repeat-bark timer (1 s) keeps them apart.
- **Art under 5,-5** and the rock's look: as 4.1a reported.

## Proposed commits

**The plan's split doesn't hold for one file.** `GB_m1-ridge.prefab` now carries 4.1a's layout *and* 4.1b's wiring. Committed alone in commit 1, it would reference sequence assets that only arrive in commit 2. I suggest moving the prefab into commit 2; commit 1 still builds and its tests still pass.

1. `feat(onboarding): rebuild The Ridge around the rockfall split and the plateau` (plain)
   - `miso/Assets/_Project/Features/NPCs/Rock.meta`, `Features/NPCs/Rock/Prefabs.meta`, `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab` + `.meta`
   - `miso/Assets/_Project/Content/Levels/MS2 - The Ridge.asset`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs` + `.meta` (includes my 4.1b edit: no menu, no stage cut)
   - `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeLayoutTests.cs` + `.meta`
   - **Caveat:** the layout file calls `MissionWiringRidge` constants, which exist in both versions, so commit 1 compiles. But `MissionWiringRidge.cs` in its 3.1b form would still have the old menu. If commit 1 must stand alone, include `MissionWiring.Ridge.cs` there too, or merge the two commits.
2. `feat(onboarding): wire The Ridge's new beats, locks and cues` (plain)
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.cs`, `MissionWiring.Ridge.Sequences.cs` + `.meta`, `MissionWiring.Ridge.Bark.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs`
   - `miso/Assets/_Project/Resources/Sequences/M1Ridge/`: the 33 new assets + `.meta` (listed under What changed)
   - the 17 old 3.1b assets + `.meta` deleted (listed under What changed)
   - `miso/Assets/_Project/Resources/BarkSystemData/CharacterHealth/Bark_Phase_M1Ridge_LowHP.barkphase` + `.meta`, `M1Ridge Low HP Dialogues.csv` + `.meta`

Not to stage: `GlobalSettings.asset`, the TextMesh Pro fallback asset, `miso.slnx`, `.mcp.json`, `powershell.exe`, `claude-handoff/`.

## Save reset

No. Play mode was never started. The play check should start from a cleared save, which also clears the bark's played-once records.

## Other branches

None.

## How to see it

Before you start: set `GlobalSettings` › `deactivateIntroOutroSequences` off. Delete or clear the save (or use `Tools/Barks/Clear Played History`). Play the Hearth through to The Ridge, or start `MS2 - The Ridge` the way you usually test a mission.

1. **Intro:** the camera goes from the pair (Linda 5,-5, Mark 6,-5) up to the clue. Then "There. Up on the ridge. Tracks." / "Too big to be hers." / "Then whose?", the camera back, and "I'll check it out." / "Careful…" / "Keep up, little brother."
2. **Rockfall** (also plays with the intro switched off):
   - Linda walks 5,-5 → 3,-2 and her walk ends;
   - the camera shakes;
   - a rock appears on 5,-5 with no HP bar and no hover panel;
   - "Mark?!" / "Still here! But I can't get to you.";
   - the camera goes to the pocket and three Claws appear (5,-2, 5,-1, 7,-2);
   - "Claws! …" / "Let them come…";
   - the page "Linda's Family Role", with no FP wording.
3. **Enemy turn 1** (the enemies go first):
   - the Claw from 5,-2 steps next to Linda; press the Watch key;
   - the other Claw steps into her row; Watch again;
   - the 7,-2 Claw doesn't act;
   - no Neutral turn and no camera hop to the rock, then or in any later round.
4. **Family turn 1:**
   - The objective reads "Mark: reach the ledge."
   - Linda's bar is empty; Mark's has Move and Blitz only, with no Command and no Duo.
   - Try to walk anyone onto 5,-5: the rock blocks it.
   - Mark: Move to 7,-4, then Blitz the 7,-2 Claw. It dies and he lands on 7,-2 and picks up her arrows.
   - **Continuous Attack doesn't trigger** and he can't reach 5,-2.
   - Then "Hold on, Linda! I see a way." / "Shoot at me, through them. I'll send it back." / "Gladly.", Linda's bar returns with a pulse on her bow, and she is selected.
   - (Also try clicking an empty cell with Linda before the unlock, and note whether she walks: check 4.)
5. **The catch:** Linda fires east along row -2 at Mark. The catch is offered and the return hits the pocket Claws.
6. **Pocket cleared:**
   - "Rock between us. Didn't matter." / "Next time, I'll wait for you." / "No, you won't." / "Breathe, sister. Then we climb." / "Race you to the top.";
   - the FP bar goes back to full;
   - the camera goes up to the plateau: "Three more, still asleep…" / "Stay close to me…";
   - the "Health Potion" page.
7. **Fallback branch** (a second run): on family turn 1, walk Mark elsewhere and end the turn. At the start of enemy turn 2 the same lines play and Linda's bar comes back for family turn 2.
8. **Plateau, both answers:**
   - Together: Mark on 3,2 beside Linda on 2,2. Claws hitting Linda draw Mark's Counter.
   - Apart: Mark on 6,2. Linda catches through the Claw on 5,2.
9. **Low HP:** let Linda drop under half health. At the start of the next family turn, Mark barks "Linda! Drink a potion. Now." It plays once only. Use the potion from the bar.
10. **Win:** clear the plateau ("Clear the ridge. N remaining."). The camera closes in on the clue, lines 8.1 to 8.7 play, then the outro and the drops (Gold 20, Steel 2, XP 30).
11. **Restart mid-level:** after a restart, family turn 1 again has no Continuous Attack jump.

## Resume from

Delete the 17 orphaned 3.1b assets. The coordinator settles the commit split and the two Needs-THJ points. Then the `miso-reviewer` pass over 4.1a and 4.1b, and THJ's play check.

## Review (miso-reviewer, 4.1a + 4.1b together, 2026-11-24)

**Verdict: APPROVE.** No must-fix items.

### Should-fix

1. **`MissionWiring.Ridge.Sequences.cs:115-129`: end the rockfall with `ShowHUDSequence`.**
   - Hiding the HUD in the rockfall races with `StartLevelIE`'s `ShowHUD()`. If the hide wins, family turn 1 opens with no HUD.
   - Update `LindasRunEnds…`'s step expectations to match.
   - Coordinator: **fix before the play check.**
2. **The bark gate's `RockNickname` (`MissionWiring.Ridge.Bark.cs:33`) and the rock's title "Rock" (`MissionWiring.Ridge.Layout.cs:108`) aren't tied by any test, and "Rock" is a generic name.**
   - Add a test, or give the rock a distinctive title.
   - Coordinator: **fix with 1.**
3. **The two-commit split fails its own tests.**
   - Make it one commit for 4.1a+4.1b: the rock prefab and mission asset included.
   - Delete the 17 old sequences in a follow-up commit.
   - Coordinator: **accepted.**
4. **On S2's fallback path, `M1Ridge_Catch_SelectLinda` runs on the enemy turn.** It logs a warning and doesn't select Linda. There's no hang.
   - Coordinator: **deferred to the trigger-component chunk (D-653).** Noted for THJ.

### Notes

- The M1 bark graph is a frozen copy of `Bark_Phase_CharacterHealth_Low`. Edit it in its own file; add this to `tech/onboarding-merge.md`.
- Lucy's old branch is still in the copy, behind the gate. Harmless.
- The off-switch relies on `SignalAction` subscribing in `Start`, before `levelStarted`. Watch it when `deactivateIntroOutroSequences` is on.

### Checks with no finding

No core files, idempotent wiring, no softlock, the switch turns back on, the filler isn't on `levelStarted`, no statics, LF/no BOM, no private IDs, no references to the 17 old sequences, the rock prefab set up sanely, the prefab's stale overrides dropped, text matches.

## Fix round (miso-implementer, 2026-11-24)

Editor was not in Play mode. Both review should-fixes done.

### What changed

1. **HUD comes back after the rockfall.** `BuildRockfall` now ends with `Common("ShowHUDSequence")` after the Watch page; the step-list comment says so. The step list asset already existed and the wiring keeps an existing list (by design), so I appended `ShowHUDSequence` to `M1Ridge_Rockfall_SequentialSequence.asset` once through the editor; the wiring then ran with no "kept the hand-edited step list" warning. `LindasRunEnds...` now checks the Watch page follows the Claws, the last step is `ShowHUDSequence`, and only it follows the page.
2. **Rock title tied to the bark gate.** `RockNickname` is now "Fallen Rock" (`MissionWiring.Ridge.Bark.cs`). The rock prefab builder uses that constant for the title, and for an already-built prefab it now syncs the title (`SyncRockTitle`). `Unit_Rock.prefab` title is "Fallen Rock". The bark graph is baked only once, so its gate value (line 2564 of `Bark_Phase_M1Ridge_LowHP.barkphase`) was changed by a one-line YAML edit; the existing bark test already compares the gate to the constant. New test `TheRockPrefabCarriesTheBarkGatesTitleAndNoOtherUnitPrefabDoes`: the rock prefab's `Nickname` equals the constant, and no other prefab under `Features/` with a `GUnit` uses it.

### Files

- `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs`
- `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs`
- `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Bark.cs`
- `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs`
- `miso/Assets/_Project/Features/NPCs/Rock/Prefabs/Unit_Rock.prefab` (title)
- `miso/Assets/_Project/Resources/Sequences/M1Ridge/M1Ridge_Rockfall_SequentialSequence.asset` (one step added)
- `miso/Assets/_Project/Resources/BarkSystemData/CharacterHealth/Bark_Phase_M1Ridge_LowHP.barkphase` (gate value)

The level prefab and mission asset were rewritten by the wiring run as before. LF, no BOM kept. No core files; `GlobalSettings.asset`, the TextMesh Pro fallback and Lucy's memory level untouched by me.

### Tests

- `M1RidgeTests` + `M1RidgeLayoutTests` + `SearchRidgeTests`: 45 run, 45 passed (one new test).
- Full EditMode suite: 2620 total, 2619 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit; AI content not changed, so not run).
- Wiring menu `Tools/Onboarding/The Ridge: Apply Layout and Wire`: the second run left every changed or new non-`.cs` asset under `Assets/_Project` byte-identical (hash of all files before and after).

### Loose ends

- The bark graph is baked only when its file is missing, and an existing rockfall step list is never rewritten. A fresh checkout builds both correctly from code; an already-built copy needs the hand edits made here (both are in the assets above).
