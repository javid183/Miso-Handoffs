# Report: Onboarding demo 3.2, M2 "The River" on the new `GB_m2-river`

Plan: plans/2026-11-23-onboarding-m1-m2-build-tech.md (chunk 3.2; paper level: plans/2026-11-22-onboarding-d3-paper-levels.md, block `m2-river` as revised by D-724/D-725)    Agent: miso-implementer    Branch: main
Outcome: done. Built, wired, tested; the full EditMode suite is green. Not played (THJ's play check). Four points need the coordinator: the turn-reset order (decision 1), the placeholder-tag conflict (decision 4), T-16's worm count, and one edge-case risk (the clearing dying on the enemies' turn).

## What changed

All paths are under `miso/Assets/_Project/`. New `.cs` files are LF with no BOM, like the other onboarding editor files; edited files kept LF/no BOM.

- `Content/Levels/Greybox/GB_s1-river.prefab` → `GB_s1-river_v1.prefab` (+ `.meta`): `AssetDatabase.MoveAsset`. GUID `7b97feea24ccadf409a0d87a1f5402be` kept; prefab and meta byte-identical to HEAD (md5 checked).
- `Features/Onboarding/Editor/SearchWiring.River.cs`: now wires only the first version. `LevelPath` → `GB_s1-river_v1.prefab`. Removed `MissionPath`, the drop and experience constants and `WireMission()`. Menu renamed to `Tools/Onboarding/Wire Search: River (first version)`, like the Ridge's. The summary comment says it never touches the mission.
- `Features/Onboarding/Editor/SearchRiverTests.cs`: the 3 mission tests (graph, drops, roster) and the `MissionAsset()` helper removed; they moved to `M2RiverTests`. Header comment updated.
- `Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs`: `LevelPath` now points at `MissionWiringRiver.LevelPath` (the new level); comment updated. `RiverCleanseLockTests` (unchanged) therefore checks the new level. The old `_v1` prefab keeps the lock it already had.
- `Features/Onboarding/Editor/MissionWiring.River.cs` (new): `MissionWiringRiver`, two menus:
  - `Tools/Onboarding/The River: Build Level`: builds `GB_m2-river` from the embedded paper block with `GridToLevelBuilder`. It refuses to run if the prefab exists.
  - `Tools/Onboarding/The River: Apply Wiring`: re-runnable. It writes the turn order (Bergsons, Enemy, Neutral), the HP factors, the Cleanse lock (`MissionWiringWhiteMothers.LockCleanse`), the 3 stages, the reset call, the embers pulse and its switch, the Pile props, the intro and outro, and re-points the mission.
- `Features/Onboarding/Editor/MissionWiring.River.Sequences.cs` (new partial): the intro, rush and outro sequences, the Lucy role page, the Pile props and the builders.
- `Features/Onboarding/Editor/M2RiverTests.cs` (new): 30 tests (28 in the first round, 2 added in the review fix round).
- `Content/Levels/Greybox/GB_m2-river.prefab` (+ `.meta`, GUID `573f2525d038a6e42b8014b9d4876d95`): new. The builder made it (67 tiles, 10 units placed), then the wiring edited it.
- `Content/Levels/MS1 - The River.asset`: one line. The graph node's `payload` now points at `GB_m2-river`. The node id, GUID, name, drops (Gold 20, Timber 1, Fabric 1), XP 30 and roster (John and Lucy fixed) are unchanged.
- `Resources/Sequences/M2River/` (new folder + `.meta`): 19 assets, each with its `.meta`:
  - **Intro:** `M2River_Intro_SequentialSequence`, `_Intro_Call_DialogNodeSequence`, `_Intro_CameraToPile`, `_Intro_CameraBack`, `_Intro_LucyRolePage` (TutorialSequence), `_Intro_Roles_DialogNodeSequence`, `M2River_LucyRole_Panels` (TutorialDataSO).
  - **Rush (end of stage 1):** `M2River_Rush_SequentialSequence`, `_Rush_Sighting_DialogNodeSequence`, `_Rush_CameraToShallows`, `_Rush_JohnRushes` (MoveUnitSequence), `_Rush_RevealRing` (RevealUnitsSequence), `_Rush_ResetTurn` (LSBExecutionSequence), `_Rush_JohnShieldUp` (CastAbilitySequence), `_Rush_AtMe_DialogNodeSequence`, `_Rush_FlareHint` (SignalSequence).
  - **Outro:** `M2River_Outro_SequentialSequence`, `_Outro_CameraOnPile`, `_Outro_Clue_DialogNodeSequence`.

`git diff --stat -- miso/` (tracked files): the old prefab and meta show as deleted (they reappear untracked as `_v1`), `MS1 - The River.asset` 2 lines, `MissionWiring.RiverCleanseLock.cs` 6, `SearchRiverTests.cs` 56, `SearchWiring.River.cs` 72. `miso/miso.slnx` is THJ's change and I didn't touch it. I didn't touch M1, `GB_m2-lucy` or the Trail's tally.

## What the level does (as wired)

- **Layout:** block `m2-river`, 15 × 5.
  - Lucy 0,2, John 1,2.
  - Clearing (in play, alert): Dark Worm 5,2 (factor left at the prefab's, 1); Dark Claws 6,3 and 6,1 at 0.8.
  - Hidden group `ring`: Dark Claws 8,3, 10,3, 8,1, 10,1 and `Unit_ArcherGoblin` 11,2, all at 0.45.
  - Tier Early, all alert, family first. The only link between the clearing and the shallows is 7,2.
- **Start filler:** I added the builder line `level fp full`, because the paper says "FTP full at start". The filler lists John and Lucy, fp 99.
- **Intro** (no input or HUD at the end, H-01):
  1. Input and HUD off.
  2. Lucy "Ryker! Ryker!".
  3. The camera goes to the Pile and back.
  4. The "Lucy's Family Role" page (the existing follow-up clip, as built).
  5. John "Stay by me." and a new Lucy follow-up line.
- **Stage 1 (hidden):** no living enemy (`LivingUnitsLOCondition`, Enemy, alive ≤ 0).
  - Hidden ring units are inactive and in no faction, so they don't count.
  - The worm's halves join the enemy faction, so they keep the stage open.
  - The objective check after a death waits one frame "so Darkworm halves register" (`CombatLevelRunHandler.EvaluateObjectivesAfterDeaths`).
  - Its end plays the rush.
- **Rush:**
  1. Input and HUD off.
  2. John "There, by the water. Fur."
  3. The camera moves from the clearing to the shallows.
  4. `MoveUnitSequence` takes John to 9,2.
  5. `RevealUnitsSequence ring` (0.6 s).
  6. **The turn reset** (the LSB `reset` call, Bergsons only).
  7. John "Lucy! At me!" and Lucy "At you?" (after the review fix round; they give the restart time to land).
  8. `CastAbilitySequence`: Shield Up on John (Self cast, `ignoreApCost` on, Family Roles off).
  9. A signal switches on the pulse on Lucy's Fire Embers.
  10. Input and HUD on.

  The enemy introductions (the Archer's card, if not seen yet) wait for the sequence to end, so they play last.
- **Stage 2 "Help John.":** `EntitiesDestroyed` (All) over the 4 ring Claws and the Archer.
- **Stage 3 "Clear the river.":** every enemy dead.
- **Outro:**
  1. Input and HUD off.
  2. Close-up on the Pile.
  3. The first version's five clue lines (prints, blood, fur, the stone axe, "someone was here").
  4. `OutroCutscene`.

  There is no sisters' tally.
- **Pile props:** `Search Scenery/Pile (placeholder)` sits at virtual tile 15,2, where there are no cells. Its pieces are Prints 15,1, Fur 15,2, Fallen Claw 15,3 and 16,1, and Pile Stones 16,2 and 16,3. Positions come from the grid's own step. Sprites only, no colliders. Sorted in each row's band, like the old clue.
- **Loss:** the template's (no Bergson standing).

## Acceptance criteria (3.2 part)

- [x] `GB_m2-river` matches the block: tiles, units, hidden group, turn order and HP factors. Tests: `TheTilesAndUnitsMatchThePaperBlock`, `TheBuildBlockParsesCleanWithTheLevelLines`, `TheClearingMeetsTheShallowsOnlyThroughTheFord`, `TheEnemiesAreEarlyTierAllAlertAndTheFamilyMovesFirst`, `TheClearingIsTheWormAtItsOwnHealthAndTwoClawsAtTheirFactor`, `TheRingWaitsHiddenAroundTheRushTileWithTheArcherAndAllAtTheRingFactor`, `TheFamilyStartsOnItsTiles`.
- [x] The old prefab is kept as `GB_s1-river_v1` with its GUID, nothing points at it, and the old tool no longer touches the mission. Tests: `TheFirstVersionIsKeptUnderItsOwnNameAndItsToolNeverTouchesTheMission`, `NoAssetReferencesTheFirstVersion`; `SearchRiverTests` still pass on `_v1`.
- [x] The beats are wired in paper order: the clearing, the rush, the ring, Shield Up, the turn reset, the embers pulse, the Pile clue. The reset is one step earlier than the paper; see decision 1. Tests: `ThreeQueuedStages…`, `StageOne…`, `StageTwo…`, `StageThree…`, `TheRushMovesJohnRevealsTheRingResetsTheTurnThenRaisesHisShield`, `TheShieldIsJohnsShieldUpOnHimselfAtNoActionPointCost`, `TheResetCallStartsOnlyTheFamilysTurnOver`, `ThePulseOnLucysEmbersIsSwitchedOnByTheRush`, `TheOutroClosesInOnThePile…WithNoTally`. **Play check needed.**
- [x] Cleanse is locked for every hero: `CleanseIsLockedForEveryHero`, `RiverCleanseLockTests`.
- [x] The intro hands over no input or HUD (H-01): `TheIntroCallsVisitsThePileShowsLucysRoleThenTheRoleLinesAndGivesNoInput`.
- [x] The mission is re-pointed and keeps its drops and roster: `TheMissionPlaysOnlyTheNewRiver`, `TheMissionKeepsItsDropsAndExperience`, `TheRosterIsJohnAndLucyFixed`.
- [x] Placeholder lines are listed below. Untagged; see decision 4.
- [x] The build never replaces the level (`TheBuildNeverReplacesTheLevel`). The wiring is idempotent: a second run left the prefab, the mission and all 19 sequence assets byte-identical (md5), with no console warnings.
- [ ] A win played through: THJ's play check (How to see it).

## Tests

Open editor, Unity MCP, not in Play mode:

| Run | Result |
|---|---|
| `M2RiverTests`, `SearchRiverTests`, `RiverCleanseLockTests`, `SearchRidgeTests`, `M1RidgeTests` | 79/79 passed |
| Full EditMode suite | **2887 total: 2886 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). The 5 known `M3DefenceTests` failures and the `GridToLevel` flake did not show up this run |
| `AIRegressionTest` | Not run: no AI graph, AI ability or unit prefab changed |

Console: no compile errors, and no warnings from the build or wiring runs.

Tests can't cover the following, so THJ's play check needs to: the worm's splits and the stage waiting for every half, the walk, the reveal, the reset and the cast at runtime, Shield Up still being on John when the player gets control, the Archer's card coming after the sequence, the pulse, the Flare copies, the camera reaching the Pile past the edge, and the win.

## To-checks

**T-16: does a Dark Worm split on its first damage? Yes, which matches THJ's rule (D-623). But the worm splits into fewer worms than the paper counts.**
- `Core/Entities/Runtime/DarkWorm/DarkWormPassiveAbility.cs`, `HandleHealthChanged` → `HandleDamaged`: any drop in health splits the worm while it has a next level. A killing blow is turned into "1 HP left" and splits too: `lethalDamagePreventsSplit` is 0 on `Unit_DarkWorm.prefab`. Hits during the 0.8 s split delay don't split it twice. Only the last level dies normally.
- **The difference:** the prefab has **3 levels**, not 4:
  - level 0: 12 HP, 6 damage, scale 1.6;
  - level 1: 6 HP, 4 damage;
  - level 2: 4 HP, 2 damage.

  So one worm takes 1 + 2 = **3 split hits, then leaves 4 small worms of 4 HP**. The paper counts 7 split hits and 8 small worms.
- **Smallest fix, if THJ wants the paper's count:** add a fourth entry to `darkWormDataList` on `Unit_DarkWorm.prefab` (data only, no code). For example, level 2 at 6 HP / 3 damage, then a level 3 at 4 HP / 2 damage, with the visuals set like level 2. This changes every worm in the game. I didn't make it. If THJ keeps 3 levels, only the paper and EN-4's numbers change.

**T-6: which embers flare off John's Shield Up? Every one of them.**
- Lucy's main ember (`AttackFireBall`), all six sidewinder prefabs (`AttackFireBallSideWinder1..6`) and her follow-up ember (`Lucy_Ability_FactionRole_Effect_Spawn` → `AttackFireBall`) are all `LucyFireballProjectile`.
- `LucyFireballProjectile.Activate` hands any of them that reaches a shielded John to `JohnShieldRelay.TryReceive`. The relay absorbs it and queues it. Each ember gets its own Taunt, then 4 copies fly out along the diagonals (`pattern` Diagonal, `range` 2) and hit the first enemy on each line.
- The copies are the main-ember prefab (`copyPrefab`). They carry the incoming ember's owner, parameters and stat context (`Projectile.GetClone`). A relayed copy is never relayed again.
- So two embers on John give two Flares: 8 copies, enough for both hits on each ring Claw.
- Damage per copy is not traced to a number; it's in the play check.

**T-13: John's walk to 9,2 has one route and one possible blocker.**
- `MoveUnitSequence` uses John's walk (`John_Ability_Walk`) with an unlimited radius. `ignoreRelationOnWalk` is 1 (Ally), so he walks through Lucy.
- When stage 1 ends no enemy is alive, and the ring is hidden. So nothing on the way blocks him.
- The only route is through 7,2 (the clearing's only exit), then 8,2, then 9,2. Path length = |x−7| + |y−2| + 2:
  - 8 steps from his start, 1,2;
  - 10 at most, from 1,0 or 1,4;
  - 3 from 6,2.
- **Blocker:** Lucy standing on 9,2. The end cell must be free, so the move is cancelled with a console warning and John stays where he is. The ring still comes out around 9,2, and Shield Up is cast where he stands.
- Lucy on 8,2 or 7,2 does not block. If Lucy stands on a ring tile, that ring unit comes in on the nearest free cell.

## Text (placeholders for `miso-narrative`)

New lines (stand-ins, untagged; see decision 4):
- Intro, Lucy: "Hit them first, Dad. My embers will be right behind." (`MissionWiringRiver.FollowUpLine`)
- Rush, John: "There, by the water. Fur."
- Rush, John: "Lucy! At me!"
- Rush, Lucy: "At you?" (the paper writes "*At* you?"; I left out the asterisks, because the dialogue box would show them)

Kept from the first version (not new): Lucy "Ryker! Ryker!"; John "Stay by me."; the five outro clue lines. The "Lucy's Family Role" page text and clip, unchanged. Objectives: "Help John.", "Clear the river." (from the paper).

## Decisions I made

1. **The turn reset runs before Shield Up, not after it** (paper order: cast → lines → reset).
   - The reset calls `CombatLevelRunHandler.ResetCurrentPhase` → `RestartTurn` and then `Tick()`. `Tick()` runs the family's phase tick. Shield Up's `Status.ShieldUp` tag (`lifeTurns` 1) and its DR modifiers (1 turn) expire on that tick.
   - So in the paper order, John would have lost his shield before the player gets control.
   - With the reset first, the cast lands after the tick and the turn still starts with full AP. The restart itself lands a frame or more after the reset step (`ResetCurrentPhase` defers it, and `LSBExecutionSequence` waits only for the action set), so since the review fix round John's call and Lucy's reply sit between the reset and the cast.
   - The restarted turn's introductions and its input hand-over wait until the sequence ends (`EnemyIntroductionController.PlayPending` waits on `SequenceInProgress`), so H-01 still holds.
   - The player sees the same thing; only the order of two invisible steps changed.
2. **The embers pulse is switched on by the rush**, not started by turn or unlock.
   - `GuidedAbilityHint` can't start "at the rush": its turn window is fixed, and `WhenUnlocked` needs Fire Embers locked, which would take them away from the clearing fight.
   - So the hint sits switched off on a `River Switches` child. A `SignalAction` turns it on when the rush sends `M2River_FlareHint`. Its window is turn 1 to 99, so it lasts until Lucy uses her embers.
   - Built from existing components; no new code. It ends on any use of Fire Embers, not only on John.
3. **I kept Lucy's role page in the intro, as built**, and added `level fp full` (the paper: "FTP full at start").
4. **The stand-in lines are not tagged `[PLACEHOLDER]`.**
   - The brief asked for the tag, but dialogue does not strip it: only the quiver and footrace barks do (`HandBackLines.Strip`). The tag would show on screen.
   - `conventions.md` (D-348) says not to tag dialogue and to list the lines in the report. Every existing wiring test asserts dialogue has no tag (`NoLineCarriesThePlaceholderTag`).
   - So I followed the convention and listed the lines above. **Coordinator:** confirm, or decide otherwise.
5. **Stage 1 counts every living enemy instead of naming the clearing's units.** Naming them can't follow the worm, whose halves are new units, and the hidden ring isn't counted anyway.
6. **New sequence folder `Resources/Sequences/M2River/`**, built the way `MissionWiring.HoldTheYard` builds its level (Build Level + Apply Wiring menus, block embedded in code). Nothing points at the old `Search/River` assets.
7. **The Cleanse-lock tool now targets the new level** (one constant), so its test covers the level the mission plays.
8. **The old tool's menu is now "(first version)"**, like the Ridge's.

## Needs THJ

1. **T-16 worm count.** Keep the worm's 3 levels (3 split hits, 4 small worms: update the paper and EN-4), or add a fourth level to `Unit_DarkWorm.prefab` (7 split hits, 8 small worms: every worm in the game)? Recommendation: judge the clearing at the play check first. The paper already says beat 1 may run long.

## Docs to update

- GDD `enemies.md` EN-4: the worm splits on its first damage; levels and counts per T-16. Owner: game designer.
- D3 paper level, M2: the worm's split counts (T-16); "*At* you?" written without asterisks. Owner: designer.
- `tech/onboarding-merge.md` and `status.md`: M2 is built on `GB_m2-river`. Menus: `Tools/Onboarding/The River: Build Level` / `Apply Wiring`. The old level is `GB_s1-river_v1`, wired by `Wire Search: River (first version)`. Owner: coordinator.

## Risks and loose ends

- **The clearing dies on the enemies' turn** (for example a Revenge kill):
  - The reset does nothing (Bergsons only), and Shield Up is cast on the enemies' turn.
  - The ring, revealed mid-turn, can act at once.
  - At the family's turn start the normal tick removes Shield Up, so the player's first turn with the ring has no shield to ember.
  - The fix isn't a one-liner: holding stage 1 until the family's turn (`FactionTurnLOCondition`, as M1 does) runs into the same tick, because the reset is then deferred behind that turn's introductions.
  - Play check first. If it happens, options: accept it, or add a small non-core "cast after the turn has started" step.
- **The camera to the Pile:** the props sit 1 to 2 tiles past the grid. The camera's bounds may stop short of them. The builder logged that it widened the bounds for the small grid. Play check.
- **Cooldown:** if John used Shield Up himself on the turn the clearing dies, the reset's tick should bring the cooldown (1) back to 0 before the cast. If not, the cast is skipped with a warning (`CastAbilitySequence.SelfCastBlocker`). Play check.
- **The pulse** ends on any use of Fire Embers, including embers fired straight at a ring Claw.
- **`GlobalSettings` `deactivateIntroOutroSequences`:** if it is still on locally (see the M1 report), the intro and the outro won't play. The rush is a stage sequence and plays either way.
- **The first version's sequence assets** (`Resources/Sequences/Search/River/`) are only used by `GB_s1-river_v1`; left as they are.

## Proposed commits

1. `refactor(onboarding): keep the first River level as GB_s1-river_v1 and stop its wiring from touching the mission` (plain)
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_s1-river.prefab` + `.meta` (deleted) and `GB_s1-river_v1.prefab` + `.meta` (added): a rename, stage both sides
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.River.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchRiverTests.cs`
   - Builds and tests on its own. The mission still points at the same GUID, now `_v1`. The Cleanse-lock tool still points at `SearchWiringRiver.LevelPath`, now `_v1`, which keeps its lock.
2. `feat(onboarding): The River rebuilt as GB_m2-river with John's rush, the ring and Shield Flare` (plain)
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.River.cs` + `.meta`, `MissionWiring.River.Sequences.cs` + `.meta`, `M2RiverTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs` (needs `MissionWiringRiver`, so it goes here)
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m2-river.prefab` + `.meta`
   - `miso/Assets/_Project/Content/Levels/MS1 - The River.asset`
   - `miso/Assets/_Project/Resources/Sequences/M2River.meta` and `miso/Assets/_Project/Resources/Sequences/M2River/` (the 19 assets + 19 `.meta` listed under What changed)

Not to stage: `miso/miso.slnx`, THJ's untracked `M3Defence_Notch3_HideLastStone.asset`, `.mcp.json`, `powershell.exe`, `claude-handoff/`.

## Save reset

No. Play mode was never started. For the play check, start from a cleared save, so the Archer's and the worm's introduction cards show as they will for a new player.

## Other branches

None.

## How to see it

Before you start: set `GlobalSettings` › `deactivateIntroOutroSequences` off. Clear the save. Play the Hearth through to The River from the world map, or start `MS1 - The River` the way you usually test a mission.

1. **Intro:**
   - "Ryker! Ryker!"; the camera goes east past the shallows to the grey Pile props and back.
   - The "Lucy's Family Role" page (clip).
   - "Stay by me." / "Hit them first, Dad. My embers will be right behind."
   - Input is not handed over yet; the Dark Worm's introduction card (if new) plays, then family turn 1.
2. **The clearing:**
   - No objective is shown (stage 1 is hidden).
   - Hit the worm once: it splits into two on its tile and the nearest free tile. Hit a half: it splits again. The smallest worms (4 HP) die. Count the splits for T-16.
   - John striking within 3 of Lucy draws her follow-up. A Claw going for Lucy within 2 of John is taken by his guard.
3. **The rush** (when the last worm and Claw die on the family's turn):
   - "There, by the water. Fur."; the camera goes to the shallows; John walks through 7,2 to 9,2.
   - Four Claws appear on his diagonals and an Archer on 11,2.
   - "Lucy! At me!" / "At you?", then John raises Shield Up.
   - **When control returns, check Shield Up is still on John:** the shield pose, the Shield Up status on his unit panel, and Lucy's ember preview on him showing the diagonal copies. If it's gone, the turn restart landed after the cast: note it.
   - The Archer's card plays (new save), then control returns.
   - Check: every family member has full AP; the objective reads "Help John."; Lucy's Fire Embers button pulses when she's selected.
   - (Try once with Lucy standing on 9,2 before the last kill: John should stay put and the console should say the move was cancelled.)
4. **The Flare:**
   - Move Lucy to 7,2 or 8,2 and aim her embers at John: the preview shows the diagonal copies.
   - Fire: John taunts once per ember, and the copies hit the ring Claws. Note the damage per copy for T-6 and whether Shield Up is still on John.
5. **Win:** kill the ring and the Archer ("Help John." done; "Clear the river." completes at once). The camera closes in on the Pile, then the five clue lines, the outro, and the drops (Gold 20, Timber 1, Fabric 1, XP 30). No "Still counting?".
6. **Old level:** `Content/Levels/Greybox/GB_s1-river_v1.prefab` still opens. Nothing plays it.

## Review fix round (miso-implementer, 2026-11-26)

Editor not in Play mode. Both should-fixes from the review are done.

### What changed

1. **The lines now stand between the reset and the Shield Up cast.** The rush is now: ... reveal → reset → John "Lucy! At me!" / Lucy "At you?" → Shield Up → embers pulse signal → input and HUD on.
   - `ResetCurrentPhase` restarts the turn in a deferred call (`ExecutionUtils.ExecuteWithDelay`, waiting while an action is in progress). `LSBExecutionSequence` only waits for the action set, not for the restart. The click-to-continue lines give the restart time to land before the cast.
   - I found nothing sturdier among the existing pieces. There is no "wait seconds" or "wait for the phase restart" sequence (the common folder holds only input, HUD, grid fades and cutscenes). A sturdier option would be a small non-core sequence that waits for the turn restart; I didn't add it.
   - `MissionWiring.River.Sequences.cs`: step order and comment changed.
   - The rush's step-list asset already existed. The wiring keeps an existing list, and moving a dialogue step doesn't count as a structural change, so it wouldn't warn either. So I swapped the two steps once in `M2River_Rush_SequentialSequence.asset` with a one-off editor call, then re-ran `The River: Apply Wiring`, with no console warnings. A fresh build gets the new order from code.
2. **New test `TheWiringRerunLeavesTheLevelUnchanged`.** It hashes `GB_m2-river.prefab`, `MS1 - The River.asset` and every `M2River/*.asset`, runs `MissionWiringRiver.Run()`, and asserts every hash is unchanged and no sequence asset was added.
   - Also new: `TheLinesStandBetweenTheResetAndTheShield`.
   - The order test is renamed `TheRushMovesJohnRevealsTheRingResetsTheTurnThenTheLinesThenHisShield` and now asserts the new order.

### Tests

- `M2RiverTests`: 30/30 passed.
- Full EditMode suite: **2889 total: 2888 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit; not run, since no AI content changed).
- `git status` after the suite shows the same file set as before. The rerun test changed nothing.

### Files for the commits

Commit 1 is unchanged. Commit 2's list is unchanged too; two of its files changed content in this round:
- `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.River.Sequences.cs`
- `miso/Assets/_Project/Features/Onboarding/Editor/M2RiverTests.cs`
- `miso/Assets/_Project/Resources/Sequences/M2River/M2River_Rush_SequentialSequence.asset` (step order)

## Resume from

The coordinator decides on decisions 1 and 4 and the T-16 question. Then a `miso-reviewer` pass over 3.1b and 3.2 together, and THJ's play check.
