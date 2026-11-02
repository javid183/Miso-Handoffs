# Report: C4c The Trail (`level deploy` line, four levels, starts-alert Claw, mission data)

Plan: plans/onboarding/2026-11-01-onboarding-c4-search-levels.md (C4c), check: reports/onboarding-c4-0-check.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. It compiles.
- After phase 1, the full EditMode run was 1249 tests, 1248 passing.
- At the end it was 1261 tests, 1260 passing.
- Both times the only failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (names read from the runs). The new variant adds two failures inside that test; see Risks.

Not play-checked, nothing committed, the save was not reset, and Play mode was not entered. No core system was changed. The mission map and the OR join behave as the C4-0 check predicted; a test drives `MissionRouteProgress` on the real graph.

## Phase 1 · `level deploy x,y` (D-351)

**What changed** (all in `Core/Levels/Editor/GridToLevel/`, editor-only):
- `GridBlock.cs`:
  - adds `GridLevelSettings.Deploy` (a list of tiles);
  - adds `GridLegend.PlayerUnitChars` = `JLUMT` and `IsPlayerUnit`.
- `GridBlockParser.cs`: new key `deploy`, read by `ReadDeploy`. Several `level deploy` lines add up, like `level hidden`.
  - A token that isn't `X,Y` is an error.
  - A tile that isn't one of the block's floor tiles is an error.
  - A tile given twice is a warning, and the tile gets one slot.
  - A family member (`J L U M T`) drawn on the tile is removed from the placements and replaced by the slot, with a warning ("the 'J' drawn there is replaced by a deploy slot").
  - Any other unit on the tile is an error, and the unit stays.
  - The "unknown level setting" message now lists `deploy`.
- `GridPalette.cs` / `GridLevelPalette.cs`: new `DeploySlotPrefab` / `deploySlotPrefab`.
  - Default: `Features/Player/PlaceHolder/Unit_Placeholder.prefab`.
  - An empty asset slot falls back to the default. The palette asset itself is unchanged.
- `GridToLevelBuilder.Deploy.cs` (new):
  - `ValidateDeploy`: the slot prefab must exist with a `GUnitPlaceHolder` on its root.
  - `PlaceDeploySlots`: one instance per tile under the cell's occupant root, at the tile's centre (as units are placed), with `initialDirection` (1, 0). The hand-made levels' slots face right, and the unit that fills a slot takes its facing.
  - `DescribeDeploy` for the preview.
- `GridToLevelBuilder.cs`: calls `ValidateDeploy` and `PlaceDeploySlots` (after the grid is built).
- `GridToLevelWindow.cs`: a "Deploy slots" row in the preview.

**Tests.** New `GridToLevelDeployTests.cs`, 8 tests, all passing:
- parse, and lines adding up;
- a bad argument, an off-floor tile, an empty line;
- a duplicate cell;
- a family member replaced, with a warning;
- an enemy on the tile;
- the preview text;
- the build: two slots on their cells, prefab instances of `Unit_Placeholder`, facing right, the drawn J gone, and the warning in the build result;
- no line means no slot.

**Docs for the line** (for `tech/level-tools.md` and the skill master):

```
level deploy 2,1             (a deploy slot on each tile: the mission roster fills it with a unit when the level loads;
                              several lines add up; a family member drawn on the tile is replaced by the slot, with a warning;
                              any other unit there is an error)
```

- "Known limits" should drop "deploy slots".
- `level_to_grid.py` still reads a slot back as `note x,y deploy slot`; it could emit `level deploy x,y` instead.

## Phase 2 · The Trail

### Blocks

In `plans/onboarding/2026-10-26-onboarding-levels.md` I added three lines to each block: `level name`, `level tier early` and `level deploy`.

| Block | `level name` | `level deploy` |
|---|---|---|
| `m2-trailhead` | The Trailhead | 2,1 |
| `m2-blood` | Follow the blood | 2,1 |
| `m2-tracks` | Follow the tracks | 2,1 |
| `m2-pile` | The Pile | 2,5 |

The ids are unchanged. The SVGs need no redraw: the drawing tool ignores `level` lines.

### Levels

Built with the grid tool's builder at the default paths: `Content/Levels/Greybox/GB_m2-trailhead.prefab`, `GB_m2-blood`, `GB_m2-tracks` and `GB_m2-pile` (plus `.meta`s).

| Level | Cells | Placed (including the slot) | Build warnings |
|---|---|---|---|
| Trailhead | 7 | 3 | the `E` exit builds as floor; the J on 2,1 is replaced |
| Blood | 17 | 8 | the J is replaced |
| Tracks | 25 | 6 | the J is replaced |
| Pile | 54 | 6 | the J on 2,5 is replaced |

**Round trip.** `level_to_grid.py` reads all four back with the same tiles and units, plus `note … deploy slot` for each slot. The trailhead, blood and tracks levels read back shifted y−1 because their row 0 is all wall. Each level places Linda, Lucy and one slot. The template's statue and rocks stay, as in the River and the Ridge.

### The starts-alert Claw (new asset)

`Features/Enemy/Dark Claw/Prefabs/Unit_DarkClaw_StartsAlert.prefab` (+ `.meta`) is a prefab **variant** of `Unit_DarkClaw`. It adds `EnemyAlertSettings` with `startsAlert` on and `alwaysAlert` off. It was made by `SearchWiringTrail.EnsureStartsAlertClaw`, which is re-runnable. `Unit_DarkClaw.prefab` is unchanged.

A spawned unit reads this flag through `unitBorn` → `EnemyAlertTracker.Register` (C4-0 check, question 8).

### Wiring: `Features/Onboarding/Editor/SearchWiring.Trail.cs` (new), Tools › Onboarding › Wire Search: Trail

The wiring is idempotent: a second run left all four levels, the mission and the variant byte-identical.

**Trailhead**
- Start: input off, HUD off, Lucy "Her trail starts here." / Linda "Then we follow it. Together.", input and HUD on.
- **Win:** the template's "defeat every enemy" is replaced, because an enemy-free level would meet it at once. The new win is one objective, "Follow the trail: reach the end of the path.": a `TilesOccupiedLOCondition` with faction Bergsons, any family member, on the exit tile 6,1. The goal-tile highlight marks it.
- The win opens the mission map: with two routes ahead, `ShouldShowMissionMap` is set.
- **FTP drain:** a `LevelStartFPFiller` on the level's event bus, wired to `levelStarted`, with `fpAmountToFill` −99, ATB 0, heal off. It lists the placed sisters, because it reads the pool through its first unit. The points clamp to 0. Only the trailhead drains.

**Follow the blood**
- Start: Lucy "Her blood.", then the panel "Family Time Points and Pass-by" (image `Tut-FR-5`, the existing FP Consumption still).
- Health: the gully column 4,3 / 4,4 / 4,5 gets factor **0.75** (16 × 0.75 = **12** at Early, whose health row is 1). The side gully 6,4 / 6,5 keeps the Claw's own 16.
- The wiring first reverts any old health override on every unit, then sets these.

**Follow the tracks**
- Start: Linda "His tracks."
- Stages, queued:
  - **Stage 1:** both ledge Archers dead (4,5 and 4,6), one `UnitDeathLOCondition` each. Its `OnCompleteSequence` is the **Encore cue**: input off → the camera to the ledge (midpoint of the two Archer tiles), holding 0.8 s → Lucy "Your arrows are up there with them." / Linda "Not for long." → the camera back to the opening view → input on.
  - **Stage 2:** every enemy dead.
- No health overrides.

**The pile**
- Start: Lucy "Linda… what if she's in there?" / Linda "Then we find her. Together.", then the panel "Items" (placeholder image).
- Stages, queued:
  - **Stage 1** (hidden): `TurnReachedLOCondition` with `turn` 1. It counts from the stage start, so it completes when turn 2 begins. Its `OnCompleteSequence` is an `LSBExecutionSequence`, call id `rearWave`.
  - The level root's `LevelSpecificBehaviour` holds one `GUnitSpawnManipulationAction`: execute on call, once, two cells (0,6 and 0,5), unit = the starts-alert variant.
  - **Stage 2:** every enemy dead. The level can't end before the wave arrives: stage 2 starts only after stage 1, and new-stage evaluation waits for the sequence.
- End: input off, HUD off, a close-up on the pile, then:
  - Linda "Still counting?" / Lucy "…No."
  - the free pick: "She isn't among them. Her tracks go on, down to the Rootwell."
  - Lucy "If he saved her, why didn't he bring her home?"
  - then `OutroCutscene`.
- **The free pick speaks through `GenericCharacter_1`.** `MissionTracker` fills that slot with the one roster unit that isn't fixed, so it is John or Mark, whoever came.
- **Props:** `Search Scenery/Animal pile (placeholder)` over the 2 × 2 of rock, as three tinted squares (no colliders).

**Mission (`Content/Levels/M2 - The Trail.asset`)**
- **Graph:** trailhead (initial) → Follow the blood, trailhead → Follow the tracks; both → an **OR InterNode** → The Pile. 5 nodes and 5 edges, with positions laid out for the graph editor.
- `initialItemsAvailability`: Health Potion ×2 (`Bergsons_Ability_HealthPotion`), Family Trinket ×1 (`Bergsons_Ability_FPPotion`, titled "Family Trinket").
- Roster checked, unchanged: Lucy and Linda fixed, 1 free slot, Toba excluded.
- **XP and drops unchanged (40 XP, 5 Gold, no drops).** The paper plan gives no numbers for M2; THJ or the designer should set them.

### Tests: `Features/Onboarding/Editor/SearchTrailTests.cs` (new), 12 tests, all passing

- **All four levels:** Early tier, only the sisters placed, one slot facing right on its tile; level names unique in the mission.
- **Trailhead:** no enemies, one exit objective on 6,1 for the Bergsons, the drain filler (−99, ATB 0, no heal, a sister first, one `levelStarted` call), and only the trailhead drains.
- **Blood:** the Pass-by panel; only the gully column is overridden, at 0.75.
- **Tracks:** stage 1 holds the two ledge Archers, the Encore cue's camera then lines, and stage 2 is "every enemy".
- **Pile:**
  - stage 1 is a turn condition, then the `rearWave` LSB;
  - the spawn action: once, the variant, cells 0,6 / 0,5;
  - no unit or slot starts on a spawn cell;
  - stage 2 is "every enemy";
  - the items panel, the tally line order, and the pick's line on `GenericCharacter_1`.
- **Tags:** no line carries `[PLACEHOLDER]`.
- **The variant:** a prefab variant whose source is `Unit_DarkClaw`, `startsAlert` on, `alwaysAlert` off; the shared Claw doesn't start alert.
- **Graph shape:** the OR join and the five edges.
- **The route map:**
  - The trailhead has several entity neighbours, so the map opens.
  - After the trailhead, both routes are Available and the pile is Unavailable.
  - After either route, the pile is Available and the other route is Missed (`MissionRouteProgress` on the resolved graph).
- **Mission data:** roster and items.

## Hand edits each level needs after a build

None by hand. After rebuilding any of the four levels with the grid tool, run **Tools › Onboarding › Wire Search: Trail**. It re-applies everything:

| Level | What the wiring writes |
|---|---|
| Trailhead | intro, exit win, drain filler |
| Blood | intro, gully health |
| Tracks | intro, stages, Encore cue |
| Pile | intro, outro, stages, rear-wave behaviour, props |
| `M2 - The Trail.asset` | graph and items |

A rebuild alone leaves the trailhead winning at once (template objectives) and the Claws at default health.

## Decisions I made

- **Trail lines.** The trailhead's lines are mine. The draft's "stays home" line (S11-J or S11-M) depends on who was left behind, and a sequence can't branch on the roster. It needs a roster condition in sequences, or a home-side line.
- **Route lines.** The draft's map-select lines (T11-1 "Her blood." / T11-2 "His tracks.") open their routes, because the map has no per-node lines.
- **The pick's line** is one merged line for John and Mark ("She isn't among them. Her tracks go on, down to the Rootwell."), spoken through the generic slot. The draft has a John version (T11-7J) and a Mark version (T11-7M).
- **When the tally plays.** It plays at the end, as the draft places it (T11-5, T11-6). The paper plan has it fade when the rear wave arrives.
- **The Encore cue lines** are T11-B1 and T11-B2. The draft has them as a bark on the first grounded arrow; here they play on the "both Archers dead" stage, per the plan.
- **Spawn timing.** The `Turn reached 2` stage is `turn` 1: the condition counts turns from the stage start, so 1 means "when turn 2 begins".
- **The mission graph node ids changed once:** the old single node wasn't flagged initial, so it wasn't reused. This has no save effect, because progress is kept by level name.

## Placeholder lines and panels (wording not signed off, untagged)

- **Trailhead (mine):** Lucy "Her trail starts here." / Linda "Then we follow it. Together."
- **Blood:** Lucy "Her blood." (T11-1). The panel "Family Time Points and Pass-by" is my wording: "Duos and Family Roles spend the family's shared time points. A Duo costs 2. / The pool is empty. Walk a Bergson through another family member to fill it: +1 for each one passed."
- **Tracks:** Linda "His tracks." (T11-2). The Encore cue is Lucy "Your arrows are up there with them." / Linda "Not for long." (T11-B1, T11-B2).
- **Pile start:** T11-3 / T11-4. The panel "Items" is my wording: "The family carries two Health Potions and one Family Trinket. / Select a Bergson, then the item in the abilities bar. A Potion heals; the Trinket restores 5 family time points." The image is a placeholder (`Tut-FR-1`).
- **Pile end:** T11-5, T11-6, the merged T11-7 (above), T11-8.
- **Objective texts:** "Follow the trail: reach the end of the path."; "Bring down the Archer on the ledge." / "Bring down the second Archer."; "Eliminate all enemies. {alive_0} remaining."

## Risks and loose ends

- **`AIRegressionTest.Baseline_MatchesCurrentAI`:** the new `Unit_DarkClaw_StartsAlert` is picked up as a unit. `units.count` becomes 22 against an expected 21, plus its "unexpected" line, so the known-red test now reports 41 failures instead of 39. I didn't re-baseline it. The fix session should include the variant.
- **Spawn on an occupied cell.** `SpawnAt` skips a cell that is occupied at turn 2, silently. A family member standing on 0,6 or 0,5 blocks that Claw.
- **FTP on the route levels.** A bought `Stat_FPG` upgrade still adds 1–2 FTP when a route level loads (C4-0 check, question 4). Only the trailhead drains.
- **The map opens again** after the chosen route, with only the pile to pick (C4-0 check, question 3).
- **Reimport noise, left in place** (not mine to commit): `GB_m1-linda.prefab`, `GB_m3-john.prefab`, `GB_s1-river.prefab`, and now `GB_s2-ridge.prefab` (8 lines of Lucy/Linda `animationEvents` sizes). Also THJ's `HearthMemoryLindaTests.cs` / `HearthMemoryLucyTests.cs`, the AI runtime files and ProjectSettings. The four new Trail levels carry no such noise.

## Proposed commits (in order)

1. `feat(levels): a level deploy grid line places deploy slots` (editor tool):
   - `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/GridBlock.cs`
   - `GridBlockParser.cs`, `GridPalette.cs`, `GridLevelPalette.cs`, `GridToLevelBuilder.cs`, `GridToLevelWindow.cs`
   - `GridToLevelBuilder.Deploy.cs` + `.meta`
   - `GridToLevelDeployTests.cs` + `.meta`
2. `feat(enemies): a Dark Claw variant that starts alert` (plain; it adds a unit the AI baseline counts):
   - `miso/Assets/_Project/Features/Enemy/Dark Claw/Prefabs/Unit_DarkClaw_StartsAlert.prefab` + `.meta`
3. `feat(onboarding): The Trail mission levels and wiring` (plain):
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m2-trailhead.prefab`, `GB_m2-blood.prefab`, `GB_m2-tracks.prefab`, `GB_m2-pile.prefab` + `.meta`s
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Trail.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchTrailTests.cs` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/Trail.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/Trail/*` (20 assets + `.meta`s)
   - `miso/Assets/_Project/Content/Levels/M2 - The Trail.asset`

   The mission data could be split out, but its test needs the levels, so I'd keep it in this commit.

The handoff repo gets the four blocks' `level` lines in `plans/onboarding/2026-10-26-onboarding-levels.md`.

All the files I wrote are LF without a BOM (CR count 0).

## Play check for THJ

1. **World map → The Trail.**
   - The squad pick offers John or Mark for the free slot; Toba is excluded.
   - The trailhead: the pick appears on 2,1 (the slot), facing right, next to Lucy and Linda.
   - The two lines play, then the FTP bar drops to 0 as the level starts.
   - Walk anyone onto the east end (6,1, highlighted): the level is won, then the **mission map** with "Follow the blood" and "Follow the tracks". The pile is greyed.
2. **Follow the blood** ("Her blood." → the Pass-by panel):
   - FTP starts at 0.
   - Walk Linda through the family to 4,1 and watch the FTP rise.
   - A Duo up column 4 should kill the three gully Claws at a median mash (12 HP each). The side gully's two take 16.
3. **Follow the tracks** (other save, or replay) ("His tracks."):
   - Linda shoots the ledge Archers from row 1.
   - When both are down: the camera rests on the ledge, then "Your arrows are up there with them." / "Not for long.", then back.
   - Check the cue doesn't land on top of a Duo's framed beat.
   - Encore should bring the grounded arrows home.
4. After either route, the map shows again with only The Pile. Pick it.
5. **The pile:**
   - Opening lines and the "Items" panel. The items bar shows 2 potions and 1 trinket; the pick and the sisters arrive with their HP.
   - Turn 2: two Claws appear on 0,6 / 0,5 already awake (no sleeping marker), and they act on the enemy turn.
   - Kill all: close-up on the pile, the tally lines, the pick's line spoken by John or Mark (whoever came), Lucy's last line, then the mission end.
   - Rewards are still the old 40 XP / 5 Gold.
6. Restart a route level and the pile once: the slot is filled again, the drain doesn't repeat outside the trailhead, and the rear wave comes back on turn 2.
7. **Sandbox Play** from the grid tool on a Trail level should ask who fills the slot (placeholder assignment window).
