# Report: Memory 4 (Mark) rework, R3: level, wiring tool and tests

Plan: plans/onboarding/2026-11-05-m4-mark-rework-tech.md (R3), design plans/onboarding/2026-11-05-m4-mark-rework.md (D-398)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done, with one approved-fallback deviation (T3: Mark is visible from the start, not hidden). Needs the coordinator's OK, see "Needs THJ".

## What changed

- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs`: rewritten. Constants (all tiles given as drawing coords through `FromDrawing`), the menu entry, shared lookups. Deletes the old tool's 9 obsolete sequence assets.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs` (new): intro, Bloom cut-in, arrival, hold and ending sequences with the approved lines.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Layout.cs` (new): stock pools swapped for `CP_Spawner_Hearth`, hero tiles, Claw plan (tiles, health, hidden state, no XP; adds the fifth top Claw), hidden groups `arrival` and `top`.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Level.cs` (new): 3 stages, Duo and Cleanse locks, 2 hints, turn-1 AP cap, Tempest Bloom grant, LSB calls `motherFalls` and `reset`, and the Bloom cut-in on `levelStarted` (`SequencePlayHandle`).
- `Features/Onboarding/Editor/HearthMemoryMarkTests.cs` + `HearthMemoryMarkTests.Flow.cs` (new partial): rewritten, 28 tests.
- `Content/Levels/Greybox/GB_m4-mark.prefab`: THJ's hand edits plus the tool's output.
- `Resources/Sequences/Hearth/Memory4Mark/`: 3 assets modified, 9 deleted (old mother scene, old arrival, Mark's walk-in), 26 new (all with `.meta`).
- `Core/` files, other levels and THJ's AI diagnostic, scene and settings files: not touched.

`git status` (scoped to `miso/`, my files only): M `GB_m4-mark.prefab`, M `HearthMemoryWiring.Mark.cs`, M `HearthMemoryMarkTests.cs`, M `Memory4Mark_End_SequentialSequence.asset`, M `Memory4Mark_Start_Opening_DialogNodeSequence.asset`, M `Memory4Mark_Start_SequentialSequence.asset`, D ×9 old assets (+ metas), ?? the 4 new `.cs` (+ metas) and 26 new assets (+ metas). Not mine and not to stage: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `EditorSettings.asset`, `ProjectSettings.asset`, and `Features/Onboarding/Editor/_GuidedSpendScratch.unity(.meta)` (a scratch scene that showed up during the full test run; it looks like a test leftover, not my code).

## Coordinate mapping

**Prefab cell = drawing tile − (1, 0)**: the prefab counts columns one lower; rows are the same. Checked on every landmark: pools drawing 0,4 / 4,7 = prefab (-1,4) / (3,7); the gap drawing 4,3 = prefab (3,3), no cell; den Claws drawing 1,4 2,4 6,4 7,4 4,5 4,6 = prefab (0,4) (1,4) (5,4) (6,4) (3,5) (3,6); Mark drawing 15,2 = (14,2); mother drawing 9,10 = (8,10), cub 8,10 = (7,10) (so the design's guess about the cub and mother tiles holds). Cell names equal `Grid.WorldToCell`, which is what `GridManager.GetCell` (used by the cast and move sequences) keys on; a test checks that.

| What | Drawing | Prefab |
|---|---|---|
| Lucy / Linda / John / Mark start | 4,1 / 4,2 / 10,5 / 15,2 | (3,1) / (3,2) / (9,5) / (14,2) |
| Cyclone cast | 4,4 | (3,4) |
| Lucy's run | 9,3 | (8,3) |
| John's objective | 7,5 | (6,5) |
| Bloom Claws (6, 6, 6, 3 HP) | 2,4 6,4 4,5 4,6 | (1,4) (5,4) (3,5) (3,6) |
| Den edge Claws (10 HP) | 1,4 7,4 | (0,4) (6,4) |
| `arrival` Claws (8 HP) | 11,2 13,2 | (10,2) (12,2) |
| `top` hidden Claws (7 HP) | 9,8 10,8 10,7 | (8,8) (9,8) (9,7) |
| Visible top Claws (8 HP) | 10,9 11,8 | (9,9) (10,8), (10,8) is new |
| Walk to the cub | Lucy 8,9, Mark 9,9 | (7,9) (8,9) |

THJ's prefab had Linda on (3,1) and Lucy on (5,2), John on the objective (6,5), and the top group as visible (9,7) (8,8) with hidden (9,8) (9,9). The tool moves them to the design's start grid. HP: in-play health = 16 × 0.6 (Tutorial row) × unit factor; the tool writes factor = HP / 9.6. Where THJ's illustrative values differed from the levers table (4,5 was 9.6, 4,6 was 6, top hidden were 8, den edges 9.6), the design's values win.

## Acceptance criteria

Design criteria (play needed for most; what the data guarantees is tested):

- [ ] Cold player fires the Bloom on turn 1, 4 in 5: play. Data: only Linda has AP on turn 1 (Linda 1, Lucy/John/Mark 0), her bow pulses on turn 1, Lucy's Cyclone is cast on (3,4) by the cut-in, and the Tempest Bloom grant is on the level. Tested.
- [ ] Mark's arrival → fresh turn, camera on Mark, chain clears his two Claws: play. Data: arrival sequence order (boast, Lucy runs, camera east, reveal `arrival`, lines, `reset` call, camera on Mark's tile, input on) and the 8-HP Claws. Tested.
- [ ] John on 7,5 plays his line, reveals the mother's Claws, unlocks only Mark–Lucy, which pulses until used: data tested (stage 2 condition, hold sequence order, `UnlockAbilitiesSequence` lists only `Mark_Lucy_Duo_Ability`, nothing else unlocks, WhenUnlocked hint). Play for feel.
- [ ] Lucy and Mark reach a tile with 3 Duo targets in the same turn: play. See T13/T15: the reach is 5 from Lucy and walks may be 3.
- [ ] Last of the five dies → mother falls, walk to the cub, end, win, no "reach the cub" goal: data tested (stage 3 = all five, outro order, no tile stage). Play for the walk.
- [ ] Every stage moves on at a cap: data tested (caps 1, 2, 4, each counted from when its stage begins). Play for flow.
- [x] No Duo other than Mark–Lucy and no Cleanse: every Duo trigger and `CleanseAbility` each hero carries (placed unit or its prefab) is locked; only Mark–Lucy unlocks. Tested.

Tech plan extras:

- [x] Tool idempotent: md5 of the prefab and all 31 `Memory4Mark` assets (+ metas) and the hearth still identical before and after a second run (prefab `c74f39f001abe1ba5cb3b7a7e2655cc0`; THJ's original before the first run was `087e49624c0323a5c19b9c477ac9443e`, a copy is in my scratchpad).
- [x] `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` passes.
- [x] `SharedObjectiveConditionTests` pass (and a per-level check inside the Mark tests).
- [x] Stage 3 cannot complete before the `top` reveal: test `TheSaveStageCannotCompleteBeforeTheTopClawsAreRevealed` (the only hidden units in stage 3 are `top`, the reveal sits in stage 2's sequence and nowhere earlier, no earlier stage counts a hidden unit). The runtime guarantee is `CombatLevelRunHandler.UpdateObjectives` → `WaitThenEvaluateNewStage` (CombatLevelRunHandler.cs:640-670): a new stage is first evaluated only after its `onCompleteSequence` stops playing.
- EditMode: see "Test results".

## Test results

- `HearthMemoryMarkTests` 28/28, `HearthMemoryLevelsTests`, `SharedObjectiveConditionTests`, `CastAbilitySequenceTests` 11/11, `HearthPoolClawTests` 6/6: all pass (Test Runner through the Unity MCP; first batch 53/53, second 45/45).
- **Full suite: not confirmed.** I started it through the Unity MCP. The MCP session then dropped ("plugin session disconnected"), Unity stopped answering pings, and my watchers on the fallback file `%USERPROFILE%/AppData/LocalLow/Dead Mage/miso/TestResults.xml` were killed by Claude Code because the machine was critically low on memory. At 01:58 the file still held the earlier 45-test run (written 01:43:35), so there is no full-suite result. **To do:** check that Unity is responsive, then run Window > General > Test Runner > EditMode > Run All. The only expected red is `AIRegressionTest.Baseline_MatchesCurrentAI` (it may also shift with the new layout; not touched or re-baselined).

## Open checks (from the code)

- **T3, can `HiddenLevelUnits` hide a player unit? Mechanically yes, but the hero comes in without his Duos.** Duo partners are bound once, when the faction controller initializes: `FactionControllerBase.Initialize` → `CooperationHandler.Initialize(this)` (FactionControllerBase.cs:106) → `CooperationPartner.Initialize(controller.AllUnits)` (UnitsCooperationHandler.cs:54, :94). A hidden Mark isn't in `AllUnits` then, so the Mark–Lucy entry is invalid for the whole level, which kills the climax. The `unitDied` hook is also closed over the start list (FactionControllerBase.cs:98). Fixing it needs a core change. **Applied the design's fallback**: Mark stands on 15,2 from the start, in play; only the two Claws are in `arrival`. Since he is in play, his turn-1 AP is capped to 0 too (so Linda stays the only unit that can act). No walk-in: from 15,2 his Blitz on 13,2 is 2 tiles, as the chain needs, so the old "walks in" step would break it. The camera moves east before the reveal, so he reads as arriving.
- **T6, does an arrow cross the gap at 4,3? Yes.** Linda's Bow Attack has `allowRangedReach` on, so cells past a gap in her row or column are targetable (GridCell.cs:872-889). The arrow (`LindaAttackArrow`, `travelEntireRadius`) flies in world space to the farthest existing cell within range (Projectile.cs:150-167), so no cell is needed under it. Fallback not needed.
- **T7, how far do the Bloom copies fly? The full arrow range (4), counted from the Cyclone tile.** `LucyCycloneProjectileScatter` clones the arrow from the Cyclone's cell (LucyCycloneProjectileScatter.cs:30), and `GetClone` keeps the arrow's own parameters, Radius included, with the Cyclone cell as the start (Projectile.cs:124-131, then :150-167). From 4,4: left to the pool 0,4 (through 2,4 then 1,4), right to 7,4, up to the pool 4,7 (through 4,5 then 4,6). That's the design's "full 4" case: with 6/6/6/3 the four Bloom Claws die and 1,4 and 7,4 (10 HP, 3.6 damage) survive. Fallback not needed. Damage figures need play.
- **T12, does a tile objective mark its tile? Yes.** `CombatLevel.RefreshGoalHighlights` (CombatLevel.cs:201-232) lights the tiles of every visible, active, unsatisfied win objective that uses `UnitTileOccupiedLOCondition`. The cells have `Highlight_LevelGoal` assigned. The stage 2 objective is visible, so 7,5 is marked.
- **T13, where is Chained Assault's reach measured from? From Lucy, and it is 5, not 4.** `Mark_Lucy_Duo_Ability` has `proxySelectionOwner` on with `Unit_Lucy`, and the player controller takes the range source from that (FactionControllerBase.cs:779-780). Its radius is a constant 5, Adjacent (Manhattan) distance, ranged reach on. So whoever triggers it, the reach is 5 from Lucy, as the design wanted (Lucy's tile). **But at 5, from 9,5 the two visible Claws (10,9 and 11,8, both 5 away) are inside the reach.** The Duo still takes exactly 3 targets that the player picks, so "3 targets" holds, but a player who picks a visible Claw (8 HP) won't kill it (about 7.7 damage). Design levers if it plays wrong: visible Claws' HP down to 7, or move 11,8. For THJ's play check.
- **T15, hero walk range: 3 for Lucy, Mark and John, 4 for Linda (base factors), times `Stat_SPD`.** The walk presets read `Stat_SPD` with base 3 (`Lucy_Ability_Walk`, `Mark_Ability_Walk`, `John_Ability_Walk`) and 4 (`Linda_Ability_Walk`). I couldn't evaluate `Stat_SPD` outside Play mode (the unit-level entry has factor 0, so the value comes from another source). If it's 1: John 10,5 → 7,5 (3) fine, Lucy 9,3 → 9,5 (2) fine, **Mark 11,2 → 9,4 (4) doesn't fit**. Design fallback: Mark goes to 9,3 instead (the Duo is from Lucy, so it still works; his Counter range to 9,6 / 10,5 then needs a check). For THJ's play check.
- **T2, extra (already in the tech check):** `Unlock(presets)` unlocks only the listed presets, for every unit that has them (LevelAbilityLock.cs:70-78). The other Duos and Cleanse stay locked; no "unlock per preset" needed.

## Save reset

No.

## Decisions I made

- **The Bloom cut-in plays on `levelStarted`, not in the intro.** The grid isn't initialized while the intro plays (CombatLevelRunHandler.cs:185 then :190), so `GridManager.GetCell` returns null and `CastAbilitySequence` would skip the cast. The intro now holds the grid fade-in and N1-1/N1-2; a `SequencePlayHandle` wired to the level's `levelStarted` (the Search levels' pattern, `SearchWiringShared.WirePlayOnLevelStart`) plays N1-3, the cast and N2-1. Same beats; side effect: player turn 1 has started underneath (input and HUD are off during it). Tier 2 in effect; flagged for play.
- Added a camera step to the den before John's call, so the cast is in view ("in view" per the design).
- The `reset` call only restarts the player's phase (`requireSpecificFaction` on, Bergsons). The same in the expected flow; it does nothing if a cap ever fires the arrival on another faction's turn.
- Locks: each hero gets every Duo trigger it carries (placed unit or its prefab) plus Cleanse, which covers the §Q7 oddities. In this level's units, Mark doesn't carry `Linda_Lucy_Duo_Ability` and nobody carries a duplicate; the union with the prefab covers them if they come back.
- The Tempest Bloom one-mission grant is kept (without it the Cyclone doesn't split arrows).
- Old assets the earlier tool made (mother scene, Mark's walk-in, old arrival lines) are deleted by the tool, since nothing uses them.
- `Mark (off)` says "The cub cried out." (the approved draft gives it to Mark, not the narrator). The cutaway is unchanged, with John on "Ten Claws, Lucy.".
- Lines carry no `[PLACEHOLDER]` tag (approved as drafted; the existing test keeps that rule).
- Stage caps are relative to the stage start (`TurnReachedLOCondition` counts from its first evaluation), so 1 / 2 / 4 give "turn 2 / 3 / 5 begins" when every stage starts on turn 1, as the design's table says.

## Needs THJ

1. **Mark visible from the start instead of hidden (T3).**
   - Context: a hidden hero comes in without his Duos, because Duo partners are bound when the level starts (core: `UnitsCooperationHandler`, `FactionControllerBase`). Chained Assault would never work.
   - Options: (a) keep the design's fallback, built: Mark on 15,2 from the start, AP 0 on turn 1, camera east at the arrival; (b) a core change so a revealed hero rebinds the Duos (Tier 3, not built).
   - Recommendation: (a).
   - Blocked: nothing; (a) is built and tested.
2. **Duo reach 5 (T13)** and **walk 3 (T15)**: see the play-check list; the design's levers are ready (visible Claws' HP, Mark to 9,3).

## Docs to update

- Levels plan Segment 4 and the design: Mark visible from the start (T3 fallback); T6, T7, T12, T13 (reach 5 from Lucy), T15 answers.
- `tech/` notes (optional): "a hidden hero has no Duos"; "intro sequences can't use cell lookups; use a level-start sequence".

## Risks and loose ends

- HUD and input during the Bloom cut-in: the run handler shows the HUD right after `levelStarted` while the cut-in hides it; a flicker or a visible HUD is possible. Turn-1 auto-selection may also move the camera to Linda during the cut-in.
- The cast is on the player's turn with `canProvokeFamilyRoles` off, so no `abilityStarted`; `CombatLevelRunHandler.OnAbilityStart` (camera focus, health snapshot) doesn't run for it. Watch for log warnings at the cast.
- Ending walks: a pool Claw standing on (7,9) or (8,9), or on the route, makes that walk a silent no-op.
- Mark visible at 15,2 before the arrival: if Linda walks instead of shooting, the den Claws may path toward him on enemy turn 1.
- The narrative draft's "one second of silence" before M4-11 is a recommendation, not built.
- `AIRegressionTest` may shift with the new layout; not touched.

## Proposed commits

1. `feat(onboarding): rebuild Mark's memory around the Bloom, Mark's arrival, John's hold and the Mark and Lucy Duo` (plain, one unit: the tool, its tests and the prefab and assets it writes only work together; THJ's prefab edits go with it):
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Layout.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Level.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs` + `.meta`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/` (3 modified, 9 deleted with their `.meta`, 26 new with their `.meta`): stage with `git add -A -- miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark`
   - Not: `_GuidedSpendScratch.unity`, the AI files, `PreloadScreen.unity`, the project settings.

Per THJ's play-test-before-commit rule, this is a gameplay chunk: THJ plays it before the commit.

## Other branches

None (onboarding-only).

## How to see it

1. Open Unity on `thj/onboarding` (the tool has already been run; to rebuild: Tools > Onboarding > Wire Memory 4 (Mark), safe to re-run).
2. Open `Content/Levels/Greybox/GB_m4-mark.prefab`: Lucy (3,1), Linda (3,2), John (9,5), Mark (14,2); the Claws on (10,2) (12,2) (8,8) (9,8) (9,7) are switched off; two `CP_Spawner_Hearth` pools; on the level object, Hidden Level Units (`arrival`, `top`), Level Ability Lock, 2 Guided Ability Hints, Turn Start Action Point Limit, Sequence Play Handle.
3. Play the Hearth to Memory 4 (or the level directly): Mark's two lines over the fade-in, John's call, Lucy's Cyclone on the crossing, John's call to Linda, Linda selected with her bow pulsing. Shoot up her column through the storm.
4. Arrival: the boast, Lucy runs to the passage, the camera goes east, two Claws appear in front of Mark, the three lines, fresh turn with the camera on Mark.
5. Chain Mark on the two Claws; walk John to the marked tile (6,5): his line, three Claws by the mother, the Duo pulses on Lucy and Mark.
6. Lucy to (8,5), Mark close by, Chained Assault on the three new Claws; end turn; the last two die to Counters or on turn 2. The ending plays: the mother falls, Lucy and Mark walk to the cub, the fade, the hearth.

## For THJ's play check

- Bloom: 4 Claws die (2,4 / 6,4 / 4,5 / 4,6), 1,4 and 7,4 survive.
- Bloom cut-in: no HUD flicker or camera jump; the cast lands in view; Lucy's cast warns nothing in the console.
- Arrival: Lucy's run isn't blocked; the reset gives a fresh turn; the camera ends on Mark; the player starts with Mark (selection is random).
- Mark's walk: does 11,2 → 9,4 fit (T15)? If not, 9,3.
- Chained Assault from 9,5: reach 5 (T13) also covers the two visible Claws. Does the player pick the three new ones? Do all three die?
- Mark's Counters on enemy turn 1, from wherever he ended.
- Pools: a Claw spawns on enemy turns while the pool's own Claw is dead; John holds 7,5.
- Ending: both walks happen (end tiles free), the mother swap shows, the cutaway plays.
- Caps: let each stage time out once and check the flow still ends.

## Fix-ups (after review, 2026-11-06)

From `reports/m4-r3-review.md` (approved, three should-fix items):

1. **The intro no longer gives back input and the HUD.** `HearthMemoryWiring.Mark.Sequences.cs`: the intro ends after Mark's opening lines, without `EnablePlayerInputSequence` / `ShowHUDSequence`. The Bloom cut-in (on `levelStarted`) already disables both at its start and restores them at its end. This removes the show/hide flicker and keeps the End Turn button from being live during the cut-in (`PhaseControlPanelUI` ignores the input switch). Tests: `TheIntroFadesTheGridInUnderMarksOpening` now asserts the intro has no Enable/Show step; `TheBloomCutInPlaysWhenTheLevelStartsAndLucyCastsOnTheCrossing` also asserts the HUD is hidden at the cut-in's start and shown at its end.
2. **FP full is now checked.** `TheMemoryRulesAreTheHearths` asserts one `LevelStartFPFiller` with `fpAmountToFill` ≥ the grid builder's full amount (99), wired to the level's `levelStarted`. The wiring tool doesn't set it: it comes from the level build (`level fp full`), and the prefab has it (99, wired). The test checks it survives.
3. **Test count corrected:** `HearthMemoryMarkTests` has 28 tests, not 29 (above fixed). Still 28 after the fix-ups (no test added, two extended).

**Status: code edited, NOT compiled, tool NOT re-run, tests NOT run.** Unity didn't answer the MCP (four tries: pings unanswered, a forced refresh timed out after 60 s), so per the coordinator I stopped. Until the tool is re-run, the prefab's intro asset on disk still has the two trailing steps, and `TheIntroFadesTheGridInUnderMarksOpening` will fail. **To do, once Unity responds:**
1. Let it compile and check the console for errors.
2. Run Tools > Onboarding > Wire Memory 4 (Mark) twice, with md5 before and after the second run on `GB_m4-mark.prefab` and `Resources/Sequences/Hearth/Memory4Mark/*`. Only `Memory4Mark_Start_SequentialSequence.asset` should change against the earlier run.
3. Run `HearthMemoryMarkTests` and `HearthMemoryLevelsTests`. No full-suite run from agents: THJ runs All.

Files touched in the fix-ups (same commit as before): `HearthMemoryWiring.Mark.Sequences.cs`, `HearthMemoryMarkTests.cs`, `HearthMemoryMarkTests.Flow.cs`, plus `Memory4Mark_Start_SequentialSequence.asset` once the tool re-runs. Line endings: these files are LF without a BOM, like the other Hearth wiring files, and they stay that way (the coordinator's note said CRLF; the files never were).

**For THJ's play check (added):**
- During the opening cut-in, the HUD stays hidden and End Turn can't be clicked. If the run handler's own HUD show at level start still wins the race (it runs in the same frame as `levelStarted`), the fallback is a one-frame wait (or a `HideHUDSequence` repeat) at the cut-in's start.

### Fix-ups verified (after THJ restarted Unity)

- Not in Play mode; forced refresh and compile: no console errors.
- md5 (prefab + all 62 files in `Memory4Mark/`, assets and metas) before the first run matched the earlier run's record, so nothing changed on disk in between.
- Run 1: only `Memory4Mark_Start_SequentialSequence.asset` changed (`ac9bdba2…` → `f7201def…`): the intro lost its two trailing steps (Enable input, Show HUD). The prefab is unchanged (`c74f39f0…`).
- Run 2: all 63 checksums identical to run 1. The tool is idempotent.
- `HearthMemoryMarkTests` (28) + `HearthMemoryLevelsTests` (3): 31/31 passed, including `NothingInTheHearthGivesExperience`. No full suite (THJ runs All).
- Nothing deleted; `_GuidedSpendScratch.unity` left alone.
- The "Status: NOT compiled" note above is superseded: compiled, re-run, tested.

## Pools (THJ's play: the pools never summoned)

**Root cause: the two pool cells weren't part of the grid.** In the hand-edited prefab, `GridCell - (-1, 4)` and `GridCell - (3, 7)` (the drawing's 0,4 and 4,7) sat directly under `Grid`, beside `Grid/Tilemap`, not under it. The grid takes in only the cells under its tilemap: `GridManager.GatherCells` does `tilemap.GetComponentsInChildren<GridCell>()` (Core/Systems/GridSystem/Runtime/GridManager.cs:58-60). Neither cell was ever initialized, so `GridCell.Initialize` never plugged what stood on it (GridCell.cs:198-199). The pool's `HazardEntity.Plug` never ran (HazardEntity.cs:103-115), so it never registered with the Enemy controller for phase ticks (HazardEntity.cs:118-133) and never ticked, whatever its turn list. The spawner, its turn list (1 to 8), its spawn limit and both effects match the stock ones field for field; they weren't the cause. The two cells had no neighbours either, so nothing could walk onto them. The tool kept these cells as they were (it never moved cells), so the problem came in with the hand edit.

Evidence (edit mode, the same calls the level start makes): before the fix the grid gathered 61 of 63 cells and neither pool. After it: 63 of 63, with a pluggable `CP_Spawner_Hearth` on both pool cells. A read-only scan of every level prefab under `Content/Levels` found no other level with cells outside its tilemap. I did not enter Play mode; THJ's replay is the final check.

**Fix (no core change):** `HearthMemoryWiring.Mark.Layout.cs` now starts the layout step by moving any cell that isn't under the grid manager's tilemap under it, keeping its world position (`AdoptCellsOutsideTheTilemap`; `Tilemap(root)` is public for the test). New test `HearthMemoryMarkTests.EveryCellIsOneTheGridTakesIn`. The Hearth pool tool and its assets are unchanged (not the cause).

**Runs and tests:**
- Not in Play mode; compiled with no errors.
- Before run 1, md5s matched the fix-up record.
- Run 1: only `GB_m4-mark.prefab` changed (`c74f39f0…` → `8b4690b3…`); every `Memory4Mark` asset was unchanged.
- Run 2: identical to run 1.
- `HearthMemoryMarkTests` (now 29), `HearthMemoryLevelsTests` (3) and `HearthPoolClawTests` (6): 38/38 passed. No full suite.

**Commits:** this all goes into the single Memory 4 commit already proposed (the layout file, the test file and the prefab are already in it). Nothing new for the Hearth pool tool's commit.

**For THJ's play check:** on enemy turn 1 each pool summons a Claw (both pools are empty at the start). After that, a pool summons again on an enemy turn only once its own Claw is dead (turns 1 to 8). The pool tiles can now also be walked next to and targeted like any cell.
