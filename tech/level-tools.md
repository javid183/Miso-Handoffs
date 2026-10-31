# Level tools: grid blocks ↔ level prefabs

Owner: coordinator. Three tools around one format, the `grid` block (legend and rules: skill `miso-level-chunks`, catalogue `design/level-chunks.md`). Plan: `plans/2026-10-26-grid-to-level-tech.md` (D-236 to D-240, D-342, D-343).

| Tool | Direction | Where |
|---|---|---|
| `tools/grid_render.py` | block → SVG drawing | `python claude-handoff/tools/grid_render.py <doc.md>` |
| `tools/level_to_grid.py` | prefab → block (read-only, YAML) | `python claude-handoff/tools/level_to_grid.py "Content/Levels/<...>.prefab"` |
| **Build Level From Grid** | block → playable prefab | Unity: **Tools › Levels › Build Level From Grid…** (`Core/Levels/Editor/GridToLevel/`, editor-only) |

## Build Level From Grid

1. Pick the doc (remembered; default `design/level-chunks.md`) and a block by `id`. The preview shows tiles, units by type, settings, the template and its objectives, and every error or warning before anything is written.
2. **Build** writes `Content/Levels/Greybox/GB_<id>.prefab` (D-236). It appears in the level toolbar's dropdown. **Play** loads it in a sandbox mission (roster = whoever the level places); **Open** opens it in Prefab Mode.
3. Wire it (mission, sequences, data), then THJ edits it.

**`level` lines** go after `--`, one per line; the drawing tool ignores them:

```
level name Memory 1 · Linda
level tier tutorial          (standard | early | tutorial | late; no line = Standard)
level alert all
level origin 11,-10
level template Content/Levels/Generic Levels/Medium/M1/LevelM1-C2.prefab   (relative to Assets/_Project/)
```

**Template.** Default `LevelM1-C2` (set in `Content/Levels/Greybox/GridLevelPalette.asset`, which also holds the character → prefab table; empty slots fall back to the built-in table). Kept: environment, lighting, music, camera, faction relations, objectives. Stripped: every GridCell and everything on the grid, `LevelSequenceTrigger`s, intro and outro sequences, the turn-order override, variant groups, `LevelAlertSettings` (re-added by `level alert all`). A template's `LevelStartFPFiller` is pointed at the placed player units (empty if none); the build warns with the values it keeps. Camera bounds are set on every build.

**Coordinates.** Tile `x,y` → `GridCell - (x, y)` at `(x × 0.5 + 0.25, y × 0.5 + 0.25)`, plus the origin; cells sit under the Grid's Tilemap; units and hazards under their cell's occupant root at the footprint centroid (big units on their bottom-left tile).

**Rebuild rule.** Rebuilding asks, then replaces the prefab whole (GUID kept). Once a level has been edited by hand, the prefab is the master: read it back with `level_to_grid.py` instead of rebuilding.

**Known limits.** Objectives are the template's (warned when they aren't the defaults); `R` and `d` build as floor with a warning, `E @ ~ ?` as plain floor; the template's scenery (rocks, statues, background) stays and doesn't match the new shape; no per-unit HP, deploy slots, sequences or Mission wiring yet.

**Built so far** (verification set, kept for play): `GB_24-nook`, `GB_27-snare`, `GB_33-deev-wave`, `GB_11-spread-pools`, `GB_m1-linda`.
