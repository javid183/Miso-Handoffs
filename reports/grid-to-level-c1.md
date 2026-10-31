# Report: Grid to level, C1 (parser, model and builder core)

Plan: plans/2026-10-26-grid-to-level-tech.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (C1 only; C2 and C3 not started)

## What changed

All new, editor-only, under `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/` (namespace `MISO.Core.Levels.CEditor.GridToLevel`; LF, no BOM, like the folder's other files):

- `GridBlock.cs`: the model (`GridDocument`, `GridBlock`, `GridTile`, `GridPlacement`, `GridLevelSettings`, `GridIssue`) and `GridLegend` (the character set of `grid_render.py` / `level_to_grid.py`, big-unit sizes).
- `GridBlockParser.cs`: reads the ```` ```grid ```` fences of a markdown file or string, as `grid_render.py` does (id, title, rows bottom-up, tokens of terrain + unit, `--` annotations); resolves each connected `O` / `D` group to one unit on its bottom-left anchor (wrong-sized group = error); reads `level name|tier|alert|origin|template` lines. Every issue carries its line, and its tile where it has one.
- `GridPalette.cs`: plain C# palette, `CreateDefault()` = the `level_to_grid.py` table (12 units, 6 hazards), GridCell prefab, default template `LevelM1-C2`, output folder `Content/Levels/Greybox`, five strip toggles (default on). C2 replaces it with the `GridLevelPalette` asset.
- `GridToLevelBuilder.cs`: `Validate` (block errors, template, GridCell prefab, a prefab per character with the drawn footprint size) and `Build` (load template contents, strip, add cells, place units and hazards, set the level name, drop event listeners left pointing at removed objects, report any other leftover reference, save). `FindMissingReferences` is public for the tests and C3's window.
- `GridToLevelTests.cs`: 20 EditMode tests (11 parser, 2 doc parses, 7 builder).
- `.meta` files for the folder and the five scripts (Unity-generated).

Nothing else touched. No core file changed; `LevelBase`, `CombatLevel`, `GridCell`, `GridManager` and `LevelAlertSettings` are only read or set through `SerializedObject` (or read through existing public getters: `PlacementSize`, `AnchorPoint`, `Centroid`, `FootprintCoords`).

## Acceptance criteria (C1)

- [x] Building `24-nook` gives 37 GridCells and 6 units on the right tiles: `Builder_NookGives37CellsAnd6UnitsOnTheirTiles` (cells compared by grid position and name; each unit by the cell whose occupant root it sits under, at that cell's anchor point).
- [x] Parsing every block in `design/level-chunks.md` (33 blocks) and `plans/onboarding/2026-10-26-onboarding-levels.md` (15 blocks) raises no error: `Parser_EveryBlockInTheChunkCatalogueParses`, `Parser_EveryBlockInTheOnboardingLevelsParses`. Warnings only: exit tiles build as floor (02, 03, 04, 08, m2-trailhead) and `R` has no prefab (12, 18, m4-mark). No block needed parser leniency: no ragged rows, no unknown characters, every big-unit group is a full rectangle.
- [x] Builder tests into `Content/Levels/Greybox/__Test/`, read back and compared; folder deleted in TearDown (and `Greybox/` too when the test created it); no missing references; no `LevelSequenceTrigger` left: `Builder_StripsTheTemplatesExtrasAndLeavesNoMissingReferences` (also checks no `LevelAlertSettings`, intro/outro none, turn-order override off, no variant groups, level name and root name `GB_24-nook`).
- [x] C# round trip for chunk 24, normalised: `Builder_NookReadsBackAsItsBlockOnceNormalised`. I also ran `level_to_grid.py` on a probe build of 24-nook: it printed the block's rows with `#` as `_` and `@` as `.`, summary "Level: GB_24-nook; 37 tiles". (Probe deleted afterwards.)
- Also covered: big units on their anchor at the footprint centroid (`Builder_BigUnitsSitOnTheirAnchorAtTheFootprintCentre`, Deev 3 × 2 and Masher 2 × 2), every hazard prefab placed under its cell incl. a unit and a hazard on one tile, `level name` naming the level, nothing written when a prefab is missing, rebuild refused without overwrite and keeping the GUID with it.

Not C1 (later chunks): the window, menu, Play button, tier / alert / origin / template applied from `level` lines (parsed and tested, not applied), camera bounds, the palette asset.

## Verification

- Compiles clean (no new warnings or errors in the console).
- `GridToLevelTests`: 20 / 20 pass.
- Full EditMode suite: 1084 tests, 1083 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red; not touched or re-baselined).
- After the suite, `git status -- miso` shows only the new `GridToLevel/` folder (plus THJ's four pre-existing dirty files, untouched). No `Greybox` folder left.
- Probe builds (deleted afterwards) of 24-nook on six templates, read back with `FindMissingReferences`: see Findings.

## Not verified

- No Play session (not asked; plan's play check is the verifier's, after C3). A built level has not been loaded from the level toolbar yet.
- `level_to_grid.py` round trip for the rest of the verification set (27, 33, 11, m1-linda): verifier, after C2 / C3.

## Save reset

No.

## Decisions I made

- **Save instead of copy (same behaviour):** the plan says `AssetDatabase.CopyAsset` then `LoadPrefabContents` on the copy. I load the template's contents directly and `PrefabUtility.SaveAsPrefabAsset` to the output path. The result is the same (a variant of `LevelBase`, nested instances linked, new GUID for a new file), the template is never touched, and a rebuild over an existing `GB_` prefab keeps its GUID, so a level already referenced survives a rebuild. Tested.
- **Cells go under the Tilemap, not the Grid transform** (plan wording vs code): `GridManager.GatherCells` reads `tilemap.GetComponentsInChildren<GridCell>()`, and every level checked has its cells under `Grid/Tilemap`. Positions come from `grid.GetCellCenterWorld`, which equals `x × 0.5 + 0.25` on `LevelBase`'s grid and stays right if a template's grid is offset.
- **Strip toggles:** five, for the extras (sequence triggers, intro/outro, turn-order override, variant groups, alert settings). GridCells and grid entities (units, hazards, deploy slots, story actors placed anywhere) are always removed, since the block is the new map.
- A sequence trigger's object goes whole when it holds only a transform, a 2D collider and the trigger; otherwise only the component goes.
- Event listeners (`m_PersistentCalls`) left pointing at a removed object are deleted; every other leftover reference is a build warning, not silently cleared.
- Ragged rows, two terrain or two unit characters in one token, and a unit on `#`/`_` are errors (the Python renderer only warns on ragged rows); `E` and `R`/`d` are warnings.
- No statics: regex patterns are `const` strings, the palette is built per call.
- Doc-parse tests read `claude-handoff/` relative to the project and `Assert.Ignore` when it is absent (it is local only), so other checkouts stay green. The builder tests use an inline copy of chunk 24.

## Findings

- **The plan's round-trip normalisation is wrong for big units.** It says `level_to_grid.py` prints "a big unit's tiles as `.` plus a `note` on its anchor". The code draws the unit's character on every footprint tile (`to_block`, footprint loop; checked on `LevelMountainDeev`: six `D`). So big units need no normalisation; the C# comparison mirrors the code. The verifier should compare the same way.
- **Default template `LevelM1-C2` is clean:** after the strip no reference to a removed object remains. It did carry a `LevelSequenceTrigger` (`Environment/SequenceTrigger`) and four deploy slots, both removed. Its level name was "The First Path (2/3)", replaced.
- **The onboarding templates leave `LevelStartFPFiller.units` pointing at removed units** (`Level1-C1-2` is clean; `LevelLucyJohn-C1`, `LevelLucyJohn-C3` and `LevelLindaJohn-C1` each leave two). Saved, these become null entries, and `LevelStartFPFiller.OnLevelStarted` dereferences `units[0]` without a null check, so the level would throw at start. The builder warns but doesn't clear them (not in the plan's strip list, and clearing would change what the level does). **Coordinator's call:** add `LevelStartFPFiller` to the strip list (C2), or have C3 / C4 rewire it to the built units.
- `LevelMarkIntro-C1` (not in any plan, probed for coverage) leaves objective conditions and a `LevelSpecificBehaviour` pointing at removed cells and units, and has a pre-existing missing `Animator` controller on `Background`. A level like that isn't a usable template without its objectives being redone; C3's objective warning will show it.
- Toba: the palette's `T` is `Features/Player/Dom/Prefabs/Unit_Toba.prefab`, as `level_to_grid.py` reads it; `Level1-C3` uses `Unit_Toba_Ally` (named `Unit_Dom`), which the Python table doesn't map. No block uses `T` today.

## Needs THJ

None.

## Docs to update

- `tech/level-tools.md` (coordinator, C3): the builder reuses `GridToLevelBuilder.FindMissingReferences` for the window's check.
- Plan, acceptance criterion "Round trip": big units are not drawn as anchor notes (see Findings).
- Plan, "How levels are built today": GridCells are children of `Grid/Tilemap`.

## Risks and loose ends

- C2 must apply `level tier`, `level alert all`, `level origin` and `level template` (parsed into `GridBlock.Settings`; the builder ignores them now) and add `CameraBoundaryBatchTool.AssignBoundary`.
- `LevelStartFPFiller` on onboarding templates (Findings).
- `FindMissingReferences` iterates every serialized property of every component; fast enough on these levels (a build plus checks takes well under a second), but it reads the Tilemap's data too.

## Proposed commits

1. `feat(levels): build a level prefab from a grid block (parser, palette and builder, with tests)`: `miso/Assets/_Project/Core/Levels/Editor/GridToLevel.meta`, `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/GridBlock.cs` (+ `.meta`), `GridBlockParser.cs` (+ `.meta`), `GridPalette.cs` (+ `.meta`), `GridToLevelBuilder.cs` (+ `.meta`), `GridToLevelTests.cs` (+ `.meta`) (plain; editor-only, one unit: the tests need the builder)

## Other branches

None (editor-only; merges to `main` with the onboarding work).

## How to see it

There is no menu yet (C3). To see C1 working:

1. Window › General › Test Runner › EditMode, filter `GridToLevelTests`, Run Selected: 20 pass, and no `Content/Levels/Greybox` folder is left afterwards.
2. To look at a built level, comment out the body of `TearDown` in `GridToLevelTests.cs`, run `Builder_NookGives37CellsAnd6UnitsOnTheirTiles`, then open `Content/Levels/Greybox/__Test/GB_24-nook.prefab`: the 24-nook shape on the M1-C2 cave, three Dark Claws at the top, Linda on the left, John and Lucy in the nook. Restore `TearDown` and delete `Greybox/` afterwards.
