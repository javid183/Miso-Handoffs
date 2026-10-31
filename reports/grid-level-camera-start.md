# Report: grid-level camera start

Plan: `plans/2026-10-31-grid-level-camera-start.md`. Branch `thj/onboarding`. No git writes. `CameraHandler.cs` untouched.

## Files changed (all under `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/`, LF, no BOM)

New (each with its `.meta`):
- `CameraStartRule.cs`: pure placement maths.
- `CameraStartTool.cs`: scene/prefab side (`PlaceOnRoot`, `PlaceOnPrefab`) and the menu item **Tools > Levels > Place Camera Start**.
- `GridToLevelCameraStartTests.cs`: 16 tests.

Edited (small):
- `GridBlock.cs`: `GridLevelSettings.CameraTile` / `HasCameraTile`.
- `GridBlockParser.cs`: `level camera X,Y` line (error "camera 'v' is not X,Y"); unknown-setting message lists `camera`.
- `GridToLevelBuilder.cs`: `GridBuildResult.CameraStart`; after the boundary step succeeds, `CameraStartTool.PlaceOnPrefab` runs on the saved prefab (warning if it fails).
- `GridToLevelWindow.cs`: preview row "Camera start"; after a build, an info box with the result.

Five `Content/Levels/Greybox/GB_*.prefab` (+ metas) were modified in place by Place Camera Start (untracked files, not rebuilt).

## The rule as built

- View = 2 x zoom high, x 16/9 wide (constant `CameraStartRule.Aspect`; the editor has no screen). Zoom is the *effective* default zoom: the same cap/clamp `CameraHandler.Awake` applies (max zoom limited by the boundary, default clamped to [min, max]). Deviation from "template's default zoom": same intent, but matches what plays.
- Tile box = every `GridCell` (walkable and hazard) +- half a cell. Player box = every player-faction unit's footprint (position +- `EffectivePlacementSize` x cell size / 2); faction taken from `LevelFactionRelations.playerFactionRef`.
- Per axis: if the tile box fits the view, the centre. Otherwise shifted the least needed to keep the player box + half a tile in view; if that does not fit either, centred on the player box. No player units: tile centre.
- Then clamped to the boundary with the camera's own clamp formula (after the boundary was assigned).
- `level camera x,y`: view centre on that tile (origin applied), also boundary-clamped.
- Locator found via `CameraHandler.initialLocator`; created as child `InitialCameraPosition` of the CameraHandler if null. World x, y set, z kept.
- World units: tiles are 0.5 world units here, so the default view (zoom 2) is 7.11 x 4.00 = 14.2 x 8 tiles.

## Per-level placements (Place Camera Start, world units)

| Level | Locator (x, y) | Tile box (x, y, w, h) | Player box (x, y, w, h), units | One screen? |
|---|---|---|---|---|
| GB_24-nook | 2.25, 1.50 | 0, 0, 4.5, 3.0 | 0, 0, 2.5, 1.5 (3) | yes |
| GB_27-snare | 2.25, 1.25 | 0, 0, 4.5, 2.5 | 1, 0, 3.0, 2.0 (3) | yes |
| GB_33-deev-wave | 2.75, 1.75 | 0, 0, 5.5, 3.5 | 1, 0.5, 3.0, 2.5 (4) | yes |
| GB_11-spread-pools | 2.25, 1.75 | 0, 0, 4.5, 3.5 | 1, 0, 2.5, 0.5 (4) | yes |
| GB_m1-linda | 1.25, 1.75 | 0.5, 0, 1.5, 5.0 | 0.5, 0, 0.5, 0.5 (1) | no, 5.0 tall vs 4.0 view; pulled down toward Linda (y 1.75; x centred) |

No locator was missing (none created). Four fit one screen with margin to spare; m1-linda is the only one larger than the view.

## Tests

All 16 new tests pass: rule (view size, fits = centre, big level pulled by the least, players already in view not moved, players too spread centred on, no players, boundary clamp, zoom cap), parser (camera line ok / absent / not a coordinate), builder (locator at level centre with z kept, camera line moves the view, template without locator gets one, 60-wide level keeps player units in view, `PlaceOnPrefab` on an existing level). Covered all plan test items.

Full EditMode suite: 1126 total, 1125 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red). Compiled clean (no console errors).

## Needs THJ's play check

- Open each of the five GB levels: opening view shows the player units and the whole (small) level, nothing at the screen edge. For m1-linda, the view should sit around Linda with the tall column running up off-screen.
- Aspect is assumed 16:9; a different window aspect changes how much is visible, not where the centre is.
- Runtime `Initialize` sets the camera position without clamping; the clamp here is done at placement time so the start is already inside the boundary.

## Decisions / notes

- Preview before a build cannot show the exact camera start (it needs the built world positions); the window shows how it will be worked out (or the override tile), and the exact position plus the "bigger than one screen / pulled toward player units" note appear in the build result box and the Place Camera Start console log.
- The faction lookup duplicates the few lines `RebindStartFiller` uses rather than refactoring the builder.
- Loose end: `Describe()` text is the only place the "bigger than one screen" wording lives.

## Proposed commits (in order)

1. Tool + tests:
   - `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/CameraStartRule.cs` (+ `.meta`)
   - `.../CameraStartTool.cs` (+ `.meta`)
   - `.../GridToLevelCameraStartTests.cs` (+ `.meta`)
   - `.../GridBlock.cs`, `GridBlockParser.cs`, `GridToLevelBuilder.cs`, `GridToLevelWindow.cs`
2. The five levels, first commit of these files (each `.prefab` with its `.prefab.meta`):
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_11-spread-pools.prefab`
   - `.../GB_24-nook.prefab`
   - `.../GB_27-snare.prefab`
   - `.../GB_33-deev-wave.prefab`
   - `.../GB_m1-linda.prefab`

Not touched: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*`, the TMP fallback font asset. No game save reset.

## How to see it

Tools > Levels > Place Camera Start with a level prefab selected (or open in Prefab Mode); the console logs the position. Or build a block with `level camera 3,1` in its notes and check the info box in Build Level From Grid.
