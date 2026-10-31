# Grid-to-level: place the camera start

Size: S    Tier: 2 (editor tool, non-core; THJ asked for it 2026-10-31)    Assigned to: `miso-implementer` → `miso-reviewer` → THJ play check
Branch: `thj/onboarding`. Status: **done 2026-10-31**, committed `9d3ac5623` (tool + tests), `652f2075e` (the five `GB_` levels). Review FIX, fix round done (coordinator check); EditMode 1126/1127 known red only; THJ play-checked the opening views OK

## Why

Every level's Camera has a child `InitialCameraPosition`, assigned to `CameraHandler.initialLocator`; `CameraHandler.Awake` (`Core/Camera/Runtime/CameraHandler.cs:145`) moves the camera there (x, y; z kept) at level start, then the boundary clamp applies. The grid builder keeps the template's locator where it was in `LevelM1-C2`, so the built `GB_` levels start looking at the wrong place (THJ, play check 2026-10-31: the units and much of the grid sit at the screen's left edge).

THJ's rule: place it so the view covers the player units' starting tiles and the intended part of the level; most levels fit one screen at the default zoom, but not all.

## Build (editor-only, `Core/Levels/Editor/GridToLevel/`; `CameraHandler.cs` is not changed)

1. **Placement rule** (pure static helper, tested):
   - View size at the template's default zoom: height = 2 × `defaultZoom` (orthographic size), width = height × 16/9 (the game's aspect; take it from the existing camera code if a constant exists).
   - Target = centre of the bounding box of every built tile (walkable and hazard cells).
   - If that box is larger than the view, shift the target the least amount needed so the bounding box of the player units' footprints (every placed unit of the player faction) stays fully in view, with half a tile of margin. If even the player units don't fit, centre on them.
   - No player units: the tile-box centre.
   - Then clamp the target inside the camera boundary the build just assigned, the same way the runtime clamp does, so what the editor shows is what plays.
2. **Override line:** `level camera x,y` (tile coordinates, in the block's own `x,y` system) puts the view centre on that tile instead. Parsed with the other `level` lines; errors in the preview like the others.
3. **Builder:** after the camera bounds step, find the locator through the template's `CameraHandler.initialLocator` (serialized field, not the object name). If it is null, create a child `InitialCameraPosition` under the camera and assign it. Set its world x, y; keep its z. The preview lists the camera start (and says when the level is bigger than one screen and the view was pulled toward the player units).
4. **Existing prefabs:** a menu item **Tools › Levels › Place Camera Start** (acts on the selected level prefab or the open Prefab Mode stage), using the same rule (no override line). Use it on the five verification levels: `GB_24-nook`, `GB_27-snare`, `GB_33-deev-wave`, `GB_11-spread-pools`, `GB_m1-linda`. Don't rebuild them.

## Tests

The placement rule: small level fits (centre), big level pulls toward the player units, player units too big (centre on them), no player units, boundary clamp, override line parsing. Builder: a build sets the locator's x, y and keeps z; a template with no locator gets one. Full EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

## Docs (coordinator)

`tech/level-tools.md` and the `miso-level-chunks` skill master (`claude-config/skills/miso-level-chunks/SKILL.md`): the `level camera` line and the rule.

## Gates

Review / EditMode / THJ plays the five `GB_` levels and checks the opening view. Commits: tool + tests; then the five `GB_` levels (first commit of those files).
