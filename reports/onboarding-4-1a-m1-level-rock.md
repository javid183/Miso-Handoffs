# Report: M1 "The Ridge" redesign build

Plan: plans/2026-11-24-m1-ridge-build-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: partial (chunk 4.1a done; 4.1b, the wiring, sequences and text, not started)

## What changed

Chunk 4.1a only. Details under "Chunks" below.

## Acceptance criteria

The 4.1a criteria are ticked under Chunk 4.1a. The rest of the plan's criteria (intro, turn order, Continuous Attack switch, locks, stages S1 to S4, cues, text, the rewritten `M1RidgeTests`) belong to 4.1b.

## Chunks

### Chunk 4.1a: level and rock (data)

**Changed files** (`git diff --stat` for tracked files, line counts for new ones):

```
 .../Content/Levels/Greybox/GB_m1-ridge.prefab      | 607 ++++++++-------------
 .../_Project/Content/Levels/MS2 - The Ridge.asset  |   4 +-
 .../Features/Onboarding/Editor/M1RidgeTests.cs     | 189 +------
 3 files changed, 223 insertions(+), 577 deletions(-)

 new  Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs   377 lines (+ .meta)
 new  Features/Onboarding/Editor/M1RidgeLayoutTests.cs           290 lines (+ .meta)
 new  Features/NPCs/Rock/Prefabs/Unit_Rock.prefab                127 lines (+ .meta, GUID b04900dc7139c68468ce9431a0ca84f0)
 new  folders Features/NPCs/Rock (+ Rock.meta) and Features/NPCs/Rock/Prefabs (+ Prefabs.meta)
```

All paths are under `miso/Assets/_Project/`. The new `.cs` files are LF with no BOM, like the other onboarding editor files. `M1RidgeTests.cs` stays LF. I didn't touch `GlobalSettings.asset`, the TextMesh Pro fallback asset or `miso.slnx` (THJ's uncommitted changes), or `MissionWiring.Ridge.cs`, the 3.1b sequences, or `GB_m2-lucy` and its wiring.

**How it was built.** A new editor tool, `MissionWiringRidgeLayout` (menu `Tools/Onboarding/The Ridge: Apply Rockfall Layout`), opens THJ's committed `GB_m1-ridge` with `PrefabUtility.LoadPrefabContents` and edits it in place. It does not rebuild it. I ran it through the Unity MCP four times. The last two runs left the prefab byte-identical, so the tool can be re-run safely. What it does:

- Adds GridCell `(5, -5)` from the same `GridCell.prefab`, placed with `grid.GetCellCenterWorld` the way `GridToLevelBuilder` does it, and slots it next to `(4, -5)` in the hierarchy. The camera boundary doesn't change: 5,-5 lies inside the old bounds.
- Moves Linda from 4,-5 to 5,-5. Mark stays on 6,-5.
- Removes the Masher (anchor -1,3) and the Claw on 2,2. Moves the Claw on 5,2 up to 5,4: it keeps its overrides, including the facing THJ gave it.
- Makes the Claw on 1,4 visible, so the plateau is 1,4, 3,4 and 5,4.
- Hides the Claws on 5,-2, 5,-1 and 7,-2 in group `fall`.
- Adds the rock in group `rock` on 5,-5 (details below). Group `back` is gone, along with its stale empty entry.
- Health factors on the placed Claws: plateau 0.7, pocket 0.7, ledge 7,-2 0.45.
- Cuts the stages down to the single "every enemy dead" stage. Details under Decisions.
- Faction relations in this level: Enemy and Neutral are now Ally. Details under Decisions.
- Adds 1 × `Bergsons_Ability_HealthPotion` to `MS2 - The Ridge.asset` › `initialItemsAvailability`.

Kept from THJ's edit: the `TestLevel` art, the light stands, the rock props, the clue (Search Scenery › Clue), `alertRangeBonus` -1 (tested), `allEnemiesStartAlert` off, the Cleanse lock, and the intro and outro references. The prefab diff only removes the Masher and Claw instances, the stale stage overrides and the `back` group, and adds the cell, the rock and the overrides listed above.

**`level_to_grid.py` read-back** (after the last run):

```grid id=src-gb_m1-ridge title="Source: GB_m1-ridge (offset x+1, y+5)"
_ _ . . . _ _ _ _
. . c . c . c _ _
. . . . _ . . _ _
. . . . . . . . _
_ _ . . _ . . . _
_ _ . . _ _ _ . .
_ _ . . . _ c _ .
_ _ _ _ . . c _ c
_ _ _ _ . _ _ _ .
_ _ _ _ . . _ . .
_ _ _ _ _ . L M _
--
level hidden fall 6,3 6,4 8,3
```

- Level: The Ridge; 51 tiles; enemy tier Early; all enemies start alert: no
- Objective text: Clear the ridge. {alive_0} remaining.
- Placed: 6 × Unit_DarkClaw, 1 × Unit_Linda, 1 × Unit_Mark
- Hidden units: group rock: a listed unit that is not a placed unit (fileID 3530633706927750278)
- Scenery props: 1 × BecStatue, 3 × Cave_Obstacle_Rock_01

Every row matches block `m1-ridge-2` (redesign plan §7), and so does the `level hidden fall 6,3 6,4 8,3` line. The tool can't name the rock: `Unit_Rock`'s GUID isn't in `claude-handoff/reward-tools/guidmap.json`, so it reports the rock as "not a placed unit". Running `build_guidmap.py` would fix that; I didn't, because it writes into `claude-handoff/`. A test checks the rock's tile and group instead (below).

**The rock**, `miso/Assets/_Project/Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`:

- A prefab variant of `Features/_Common/Prefabs/UnitBase.prefab`, like the Deer.
- Overrides: name `Unit_Rock`, title "Rock", `factionRef` Neutral, `resurrectable` off, `visualizePlayabilityInTurn` off.
- Tags `EntityState.Unmovable` and `EntityState.Unable to Swap`, both permanent.
- `entityInfoPanelUI` set to none, so hovering it shows no info panel. `GUnit.ShowInfoPanel` and `ShowDamagePreview` return early when it is null.
- The `Visual/UnitInfoHook/MiniHealthBar` GameObject is switched off, so it has no mini HP bar.
- The Body sprite is the cave's `CaveRock 01.png`, as a stand-in until final art.
- The base already has no abilities, no revenge and no ATB gauge; the variant keeps those.
- In the level, it sits under GridCell (5,-5)'s occupant root, inactive, and is listed alone in group `rock`. Linda stands on the same cell. That is fine: the cell only gathers active occupants, and `HiddenLevelUnits` skips the rock until a reveal. `Reveal` falls back to the nearest free cell if Linda is still standing there. In 4.1b, her scripted walk must come first.

**Does a neutral unit work in `HiddenLevelUnits` without code?** Yes, by reading the code. `HiddenLevelUnits.Reveal` checks that the unit has a faction, then calls `run.AddFactionControllerMidWay(Neutral)`. That builds the Neutral `AIController` mid-level through `EnsureFactionController` and inserts it by turn order. Then it calls `RegisterUnit`. Level2's Deer already plays as a Neutral unit. I found one real problem and fixed it with data, not code:

- In the `LevelBase` template, Enemy–Neutral is **Enemy** (relationType 2). The AI takes its targets from `GetFactionEnemies` (`AIBlackboard`), and the alert tracker's sight checks use `AreHostile`. So the Claws would have targeted the rock, and a rock within 3 tiles of a Claw would have woken it.
- In this level's `LevelFactionRelations`, that entry is now Ally. Bergsons–Neutral was already Ally.

**Criteria met**

- [x] The layout matches `m1-ridge-2` when read back: the block above. `M1RidgeLayoutTests.TheTilesAndUnitsMatchThePaperBlock` rebuilds the block from the prefab's cells and units and compares it string for string. THJ's art, clue and `alertRangeBonus` -1 are unchanged (`TheLevelKeepsItsHandEditedAlertSettingsAtEarlyTier`; the prefab diff touches no art).
- [x] Tile 5,-5 exists. Linda is on 5,-5 and Mark on 6,-5. The Masher and the Claws on 2,2 and 5,2 are gone. The plateau Claws on 1,4, 3,4 and 5,4 are visible at 0.7. The pocket Claws 5,-2 and 5,-1 (0.7) and 7,-2 (0.45) are in hidden group `fall`. Tests: `TheSiblingsStartSideBySideOnTheNewTile`, `TheMasherIsGoneAndSixClawsRemain`, `ThePlateauClawsAreInPlayAndThePocketAndLedgeClawsFallInLater`, `ClawsCarryTheirHealthFactors`.
- [x] (data) A neutral, unmovable rock with no abilities sits in hidden group `rock` on 5,-5, with no HP bar and no info panel. It isn't counted by "defeat all enemies", which is a `LivingUnitsLOCondition` on the Enemy faction's controller only, and the rock is Neutral. It isn't an enemy target, because Enemy–Neutral is Ally in this level. Tests: `TheRockPrefabIsANeutralUnmovableUnitWithNoAbilitiesAndNoHealthDisplay`, `TheRockWaitsHiddenOnTheSharedTile`, `TheRockIsNeitherAnEnemyTargetNorCountedByClearingTheRidge`. **Not verified in play:** that the revealed rock blocks walking (by code: an occupant makes `IsWalkable` false), how hover feels, and what the AI actually does.
- [x] `MS2 - The Ridge.asset` › `initialItemsAvailability` holds `Bergsons_Ability_HealthPotion` × 1. The diff is those 3 lines and nothing else (`TheMissionStartsWithOneHealthPotion`; `TheMissionKeepsItsDropsAndExperience` and `TheRosterIsLindaAndMarkFixed` still pass).

**Tests** (open editor, Unity MCP, run by full class name):

| Class | Result |
|---|---|
| `MISO.Core.Features.Onboarding.EditorTests.M1RidgeLayoutTests` (new) | 11/11 |
| `MISO.Core.Features.Onboarding.EditorTests.M1RidgeTests` | 8/8 |
| `MISO.Core.Features.Onboarding.EditorTests.SearchRidgeTests` | 11/11 |
| Total | 30/30 |

The console has no compile errors. The only warnings are the existing "Serialization depth limit" ones, which aren't from this change.

**`M1RidgeTests`: what broke and what I did.** Before my change, 8 of its 19 tests were already red against THJ's committed `f20f9a5ab`: the old layout, alert and clue tests. Removing 3.1b's stages would have broken more. I **removed** the 11 tests whose subject no longer exists, rather than marking them, so the suite stays honest. 4.1b rewrites the class anyway.

- Removed because of the layout:
  - `TheLevelIsTheRidgeAtEarlyTierWithEveryEnemyAlert`: THJ turned all-alert off.
  - `TheRoomLedgeAlcoveAndCorridorAreTheGridsCells`: 38 cells; there are 51 now.
  - `ThePairAndTheEnemiesStandOnTheirTiles`: the old tiles.
  - `TheMashersOnlyNeighboursAreBesideItInTheCorridor`
  - `TheBackPairStartsHidden`
  - `ClawsAndTheMasherCarryTheirHealthFactors`: 0.8 / 0.45.
  - `NoFirstSleeperPanelSinceEveryEnemyStartsAlert`: its premise is false now.
  - `TheClueLiesAtTheCorridorsEndAndTheEndClosesInOnIt`: clue on 12,0, a tile that no longer exists.
- Removed because of the stages:
  - `FourStagesRunThePackTheMasherWithTheLateClawsAndTheRest`
  - `TheMasherSetupShowsItThenTwoLinesOneSayingToAimAtIt` and `TheArrivalRevealsTheBackPair`: they test sequences nothing plays any more; 4.1b deletes those sequences.
- Kept, and still true: `TheFamilyMovesFirst` (4.1b flips it to Enemy first), `CleanseIsLockedForBothAndNothingElse`, `TheStartPans…` (3.1b's intro is still wired), `NoLineCarriesThePlaceholderTag`, the three mission tests, and `TheFirstVersionsToolWiresItsOwnLevelAndNeverTheMission`.
- Its unused helpers went with the tests. Its header now points at `M1RidgeLayoutTests` for the layout.

**AI regression.** I ran `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` by name: **45 failures, against 44 (D-644). The one new line is `units.unexpected Assets/_Project/Features/NPCs/Rock/Prefabs/Unit_Rock.prefab: new unit prefab is not in today's baseline`.** It is the same kind of line D-255 accepted for new presets. The `units.count` line now lists 24 prefabs, `Unit_Rock` among them; it was already a failure. I did not re-baseline anything.

**Decisions and loose ends:** see "Decisions I made" and "Risks and loose ends" below.

## Reviews and checks

- 4.1a: none yet. The plan has one `miso-reviewer` pass over 4.1a and 4.1b together.

## Save reset

No. Play mode was never started.

## Decisions I made

- **Enemy–Neutral made allies in `GB_m1-ridge`'s `LevelFactionRelations`** (data, this level only). The plan assumed Neutral was not hostile to the enemies. The template makes them hostile, so without this the Claws would target the rock and it could wake them. The plan's intent (no targeting) is kept, so it is the same behaviour. A side effect to check in play: Neutral is now "player side" for the alert tracker and an ally of both camps. Harmless for a unit with no abilities that never moves.
- **Stages: one "every enemy dead" stage, not none.** I kept 3.1b's last stage ("Clear the ridge. {alive_0} remaining.", `LivingUnitsLOCondition` Enemy ≤ 0) and dropped the other three. This keeps the level winnable between 4.1a and 4.1b, and gives the "rock isn't counted" test a real condition to check. 4.1b replaces it with S1 to S4.
- **The dropped stages' overrides were removed from the prefab too.** Unity had kept them in the modification list after the array shrank, so `level_to_grid.py` still printed "Get past the Masher." The tool deletes only stage overrides past index 0 and the objective-condition objects nothing points at any more.
- **Intro and outro references left as they are** (3.1b's `M1Ridge_Start_*` and `M1Ridge_End_*`). The plan says to remove 3.1b's stages; 4.1b rewrites the intro and reuses the outro. The intro's camera points are from the old layout, so they will look wrong until 4.1b.
- **Facing:** I kept THJ's hand-set facings and didn't apply the builder's facing rule. The moved 5,4 Claw keeps its left facing from 5,2.
- **The layout is a re-runnable tool** in its own file (`MissionWiring.Ridge.Layout.cs`), not inside `MissionWiring.Ridge.cs`. The plan leaves that file to 4.1b. 4.1b can fold the tool in or keep it; its constants (`SharedTile`, `FallTiles`, `PlateauTiles`, group ids, factors) are public for 4.1b's wiring and tests.
- **New layout tests in their own class** (`M1RidgeLayoutTests`), so 4.1b can rewrite `M1RidgeTests` without losing the layout, rock and potion checks.
- **The rock's location:** `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`, beside the Deer, following the `Unit_<Name>` naming.

## Needs THJ

None.

## Docs to update

- `claude-handoff/reward-tools/guidmap.json`: rebuild it (`build_guidmap.py`) so `level_to_grid.py` names `Unit_Rock`. Owner: coordinator.
- `tech/onboarding-merge.md` / `status.md`: 4.1a done; the M1 level is on the rockfall layout with one interim stage. Owner: coordinator.

## Risks and loose ends

- **Not verified in play** (no Play session was allowed):
  - the Neutral controller is created mid-level on reveal;
  - the revealed rock blocks the tile;
  - hover on the rock shows nothing distracting;
  - the Claws ignore it.
- **The Neutral turn will focus the camera on the rock.** `AIController.HandleUnits` focuses on each unit, waits `waitTimeAfterFocus`, finds no action and ends the turn. So once the rock is revealed, every round has a short Neutral turn with a camera hop to 5,-5, and maybe a phase banner. Two data-only options, if THJ dislikes it:
  - leave Neutral out of the turn order override in 4.1b (to check: does the controller still get a turn?);
  - give the rock the `Unaware` tag, so `AIController`'s skip query drops it. This is a hack with possible side effects.

  To check in 4.1b's play test.
- **Art under 5,-5.** THJ's `TestLevel` art was drawn when 5,-5 was a gap. The new tile may sit on painted rock or a hole until the art is touched up. The rock unit covers it once it is revealed, but Linda starts there.
- **The rock's look:** `CaveRock 01` on the unit's Body with size 0.8 × 1.24 and no animator controller (the base has none). Its scale and pivot are not checked by eye.
- **Don't run `Tools/Onboarding/Wire Mission: The Ridge` (3.1b's tool) before 4.1b.** It still targets the old layout. Its first pass throws on a missing cell (8,3) before it saves anything, so it can't damage the prefab, but it no longer works.
- **`GridToLevelBuilder` rebuild rule:** the prefab is the master now. Never rebuild `GB_m1-ridge` from the block (D-651); re-run the layout tool instead.
- **For 4.1b:**
  - Linda's `MoveUnitSequence` must run before `RevealUnitsSequence` `rock`, or the rock lands on the nearest free cell.
  - `fall` and `rock` can be revealed in either order.

## Proposed commits

Per the plan, chunk 4.1a goes into commit 1, after THJ's play check, together with 4.1b's commit 2.

1. `feat(onboarding): rebuild The Ridge around the rockfall split and the plateau` (plain):
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab`
   - `miso/Assets/_Project/Content/Levels/MS2 - The Ridge.asset`
   - `miso/Assets/_Project/Features/NPCs/Rock.meta`
   - `miso/Assets/_Project/Features/NPCs/Rock/Prefabs.meta`
   - `miso/Assets/_Project/Features/NPCs/Rock/Prefabs/Unit_Rock.prefab` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeLayoutTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs` (the trimmed tests; it could move to commit 2 with 4.1b's rewrite instead)

Not to stage: `GlobalSettings.asset`, the TextMesh Pro fallback asset, `miso.slnx` (THJ's), `claude-handoff/`.

## Other branches

None.

## How to see it

1. Open `Content/Levels/Greybox/GB_m1-ridge.prefab`.
   - Linda and Mark stand side by side on the bottom row (5,-5 and 6,-5).
   - Under GridCell (5,-5) there is an inactive `Unit_Rock`.
   - The Masher and the Claws on 2,2 and 5,2 are gone.
   - Claws stand on the plateau at 1,4, 3,4 and 5,4.
   - The Claws on 5,-2, 5,-1 and 7,-2 are inactive.
   - The root's Hidden Level Units lists `fall` (three Claws) and `rock` (the rock).
2. Open `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`: Neutral faction, the two tags, no abilities, Entity Info Panel UI empty, MiniHealthBar off.
3. Open `Content/Levels/MS2 - The Ridge.asset`: Initial Items Availability holds one health potion.
4. In Play (once 4.1b wires the intro), the reveals and the rock can be seen in a run. Before 4.1b, a run starts with the pocket Claws and the rock hidden and is won by clearing the three plateau Claws: nothing reveals the hidden ones yet.

## Resume from

Chunk 4.1b: rewrite `MissionWiring.Ridge.cs` (turn order Enemy, Bergsons, Neutral; S1 to S4; locks; the Continuous Attack switch; the second FTP filler; the intro with Linda's walk, the shake, `RevealUnitsSequence` `rock` and `fall`, and the Watch page; the outro; the low-HP bark), then rewrite `M1RidgeTests`, then run the full EditMode suite.
