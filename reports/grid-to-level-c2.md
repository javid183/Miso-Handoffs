# Report: Grid-to-level C2 (palette asset, level settings, camera bounds)

Plan: plans/2026-10-26-grid-to-level-tech.md (C2)    Agent: miso-implementer (sonnet)    Branch: thj/onboarding
Outcome: done

## What changed

- `Core/Camera/Editor/CameraBoundaryBatchTool.cs`: new `public static bool AssignBoundary(string prefabPath)` holding the per-prefab body (load, find `CameraHandler`, compute from the grid, set, save, unload; false plus a warning when there is no handler or no cells). The "All Levels" menu item keeps its cheap `CombatLevel` pre-filter and calls it. File keeps its BOM and CRLF.
- `Core/Levels/Editor/GridToLevel/GridLevelPalette.cs` (new): ScriptableObject with unit and hazard tables (code string + prefab), GridCell prefab, template level, output folder, five strip toggles. `[Button] ResetToDefaults()` fills it from `GridPalette.CreateDefault()`. `ToPalette()` lays every filled slot over the built-in table (empty slot or missing asset = the code table). `Load()` returns the asset's palette or the default one. `CreateAsset()` makes the asset (no menu item; I ran it once).
- `Content/Levels/Greybox/GridLevelPalette.asset` + metas, `Greybox.meta` (new).
- `GridToLevelBuilder.cs`: `TemplatePathFor` (the `level template` line with the `Assets/_Project/` prefix, or the palette's; `Validate` and `Build` use it); `ApplyLevelSettings` (name, `enemyTier` set explicitly, Standard when there is no tier line; `level alert all` adds or reuses `LevelAlertSettings` and turns on `allEnemiesStartAlert`); `level origin` shifts every cell (name and position) while the block coordinates stay for footprints; `RemoveStrayEntity` (own prefab root goes whole, a part of a larger nested prefab loses only the entity component, with a warning); `RebindStartFiller` (D-342: units become the placed units whose `FactionRef` equals the level's `playerFactionRef`, in block order, or an empty list; never a null; build warning lists `fpAmountToFill`, `atbGaugeAmountToFill`, `heal`; runs after the grid and before the missing-reference check); output folder created just before saving; `CameraBoundaryBatchTool.AssignBoundary(path)` after the save (warning if it returns false).
- `GridPalette.cs`: comment reworded (no `claude-handoff/` path).
- `GridToLevelSettingsTests.cs` (new, 11 tests) + meta.

## Acceptance criteria

- [x] `level tier tutorial` + `level alert all` block builds a level that `level_to_grid.py` reads as "enemy tier Tutorial; all enemies start alert: yes": built a probe through `GridLevelPalette.Load()`, ran `python claude-handoff/tools/level_to_grid.py "Content/Levels/Greybox/GB_probe.prefab"`, got exactly that. Probe deleted.
- [x] Camera bounds set: `Camera_BoundaryHugsTheBuiltMap` (matches `TryComputeBoundaryFromGrid`, differs from the template's).
- [x] Tier / alert / origin / template lines applied: `Settings_TierAlertOriginAndTemplateLinesAreApplied`, `Settings_NoTierLineGivesStandardEvenWhenTheTemplateIsNot`, `Settings_MissingTemplateIsAnErrorAndWritesNothing`.
- [x] Filler rebound to player units or emptied, no nulls: `Filler_IsReboundToThePlacedPlayerUnitsWithNoNullEntries`, `Filler_IsEmptiedWhenTheBlockHasNoPlayerUnits`.
- [x] Strip leaves a nested environment intact: `Strip_KeepsTheRestOfANestedEnvironmentWhenOneEntityInsideItGoes`; whole unit instances still go: `Strip_RemovesAWholePlacedUnitInstance`.
- [x] Palette asset: `PaletteAsset_*` (3 tests, one reads the real asset).
- [x] EditMode suite: 1095 run, 1094 pass; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).
- Needs the verifier's play check: nothing beyond C1's sandbox-play items; no runtime code changed.

## Save reset

no

## Decisions I made

- `AssignSelectedLevelBoundary` (the "Selected Level" menu item) is left as it was. It edits a live selection with Undo, so it has no prefab path to pass; only the batch item calls `AssignBoundary`. Behaviour of both is unchanged.
- The batch item keeps its `CombatLevel` pre-filter outside `AssignBoundary`, so its processed/skipped counts are exactly as before.
- Palette semantics: an empty slot falls back to the code table (so clearing a slot can't remove a character; set it to another prefab instead). Strip toggles, output folder, template and GridCell prefab come straight from the asset when set.
- Palette entries store the grid character as a one-character string (Unity does not serialize `char`).
- Used Alchemy `[Button]` (no label overload exists, so it shows as "Reset To Defaults").
- Tests build their template copies with `LoadPrefabContents` + `SaveAsPrefabAsset` rather than `AssetDatabase.CopyAsset`, because a second `CopyAsset` of the M1 template logged "Unsupported type Vector2f" in the importer and failed a test (Unity-side noise, unrelated to this code).
- The template's `LevelStartFPFiller` warning is a build Warning on every build from a template that has one, even when values are unchanged.

## Needs THJ

none

## Docs to update

- `tech/level-tools.md` (C3): `GridLevelPalette` semantics (fallback to the code table), `AssignBoundary`, the filler warning.
- Plan: C2 done; commit hashes to the log.

## Risks and loose ends

- `Content/Levels/Greybox/` now exists in the repo with only the palette asset (the C1 tests recreate and remove their own `__Test` folder inside it).
- Nested-prefab stray entity: only the component is removed (tested; no console error), the host object stays. No current template has this case.
- Camera tool logs a "grid smaller than viewport" notice for small blocks; harmless, and it widens the boundary.
- The two edited-but-unrelated dirty files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*`) were not touched.

## Proposed commits

1. `refactor(camera): extract AssignBoundary from the camera boundary batch tool` (plain, revertable alone): `miso/Assets/_Project/Core/Camera/Editor/CameraBoundaryBatchTool.cs`
2. `feat(levels): grid-to-level palette asset, level lines, start filler rebind and camera bounds` (plain): `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/{GridLevelPalette.cs,GridLevelPalette.cs.meta,GridPalette.cs,GridToLevelBuilder.cs,GridToLevelSettingsTests.cs,GridToLevelSettingsTests.cs.meta}`, `miso/Assets/_Project/Content/Levels/Greybox.meta`, `miso/Assets/_Project/Content/Levels/Greybox/GridLevelPalette.asset`, `.../GridLevelPalette.asset.meta`

Depends on commit 1 (the builder calls `AssignBoundary`).

## Other branches

none

## How to see it

1. Open `Assets/_Project/Content/Levels/Greybox/GridLevelPalette.asset`: 12 units, 6 hazards, GridCell, template `LevelM1-C2`, strip toggles. "Reset To Defaults" refills it.
2. Run the EditMode tests `GridToLevelSettingsTests` (all green).
3. Optional: in the console, `GridToLevelBuilder.Build(block, GridLevelPalette.Load())` for a block with `level tier tutorial` / `level alert all`, then `python claude-handoff/tools/level_to_grid.py "Content/Levels/Greybox/GB_<id>.prefab"` (the window arrives in C3).
