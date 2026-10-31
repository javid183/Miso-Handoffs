# Grid → Level: build a playable level from a grid block

Size: M    Tier: 3 (new tool)    Assigned to: miso-implementer (C1 opus, C2–C3 sonnet), then miso-reviewer and miso-verifier
Branch: all (editor-only code; built on the current branch, `thj/onboarding`)
Status: approved by THJ 2026-10-26 (D-236 to D-239); checked against the onboarding levels 2026-10-26 (round-trip criterion corrected, D-240; see [Onboarding fit](#onboarding-fit)); C1 dispatched 2026-10-31 on `thj/onboarding` (D-337)

## Why

Level ideas are drafted as `grid` blocks (`design/level-chunks.md`, `plans/onboarding/2026-10-26-onboarding-levels.md`; skill `miso-level-chunks`). `tools/level_to_grid.py` reads a level into a block; nothing goes the other way, so every level is still laid out by hand. D-235 (reversing D-201) makes the implementer create the onboarding levels from the paper plans, with THJ editing them afterwards, and THJ is planning a workflow to create levels from designer plans. This tool is that workflow's first step: a block becomes a playable level in seconds, which the implementer then wires (missions, sequences, data) and THJ then edits.

## Goal

A menu tool that builds a level prefab from one grid block, by copying a template level and replacing its grid content. The result is playable at once from the level toolbar, and it reads back identically with `level_to_grid.py`.

## Acceptance criteria

- [ ] **Tools › Levels › Build Level From Grid…** opens a window: pick a markdown doc (default `claude-handoff/design/level-chunks.md`), pick a block by `id`, see the template, the output path and a preview (tiles, units by type, settings, the template's objectives), then Build. Unknown characters, ragged rows, missing prefabs and a template whose objectives aren't the defaults are listed before anything is written.
- [ ] Build writes `Assets/_Project/Content/Levels/Greybox/GB_<id>.prefab` (D-236): a copy of the template level (D-237) with its grid content and level-specific extras stripped (list below), then one GridCell per walkable tile and every unit and hazard the block holds, each under its cell's `occupantRoot`, as the editor's own drag tool places them.
- [ ] Coordinates hold: block tile `x,y` becomes `GridCell - (x, y)` at local position `(x × 0.5 + 0.25, y × 0.5 + 0.25)`, offset by `level origin` when given. Big units (Masher 2 × 2, Deev 3 × 2) sit on their anchor tile (bottom left of their group) at their footprint's centroid.
- [ ] `level` lines set the name, enemy tier, "all enemies start alert" and origin, and may pick another template (D-238). Objectives are the template's; the window warns when they aren't "defeat every enemy / lose when the family is down".
- [ ] The level's name and ID are its own (`GB_<id>` unless `level name` says otherwise), never the template's.
- [ ] Camera bounds are assigned on build, through the existing camera boundary tool.
- [ ] The level appears in the level toolbar's dropdown and plays from it (sandbox mission; no Mission asset touched). The window's **Play** button does the same.
- [ ] Round trip: `python claude-handoff/tools/level_to_grid.py "Content/Levels/Greybox/GB_<id>.prefab"` prints the source block's rows **after normalising** (D-240), for every block in the verification set. `level_to_grid.py` can't print them verbatim: it prints every missing tile as `_` (never `#`), the drawing aids (`@ E ~ ? R d`) as `.`, (correction from C1: `level_to_grid.py` draws a big unit's character on every footprint tile, so big units need no normalising), and crops to the cells' bounding box. So both sides are normalised the same way before comparing: `#` → `_`, drawing aids → `.`, then cropped to the cells. The C1 builder test compares the same way in C#.
- [ ] No missing references in the built prefab (the stripped extras leave none behind).
- [ ] Rebuilding an existing `GB_` prefab asks first, then regenerates it whole.
- [ ] EditMode tests pass (parser and builder); `AIRegressionTest.Baseline_MatchesCurrentAI` stays the known red and is not re-baselined.

## Scope

In: an editor-only parser for `grid` blocks; the `GridLevelPalette` asset (D-239); the builder (copy, strip, build); the window and menu; a small refactor of the camera boundary tool so it runs on one prefab path; tests; docs.
Out (later, after a level has been played, D-238): objectives from the block (exit tiles, survive N turns, protect), per-unit HP or "starts alert", deploy slots, sequences and cues, Mission wiring, environment art. Nothing at runtime changes.

## Touches

Systems: level prefabs (data); reads and sets serialized fields of `LevelBase`, `CombatLevel`, `GridCell`, `LevelAlertSettings` (core) through `SerializedObject` only, with no API or behaviour change; `Core/Camera/Editor/CameraBoundaryBatchTool.cs` (editor, refactor); the level toolbar and `EditorLevelLoader` (used, unchanged).
USPs: none directly (tooling for level content that showcases Roles, Synergies and Duos).
Docs: `claude-config/skills/miso-level-chunks/SKILL.md` (new section), `tech/level-tools.md` (new), the catalogue header, `README.md` map, `plans/onboarding/2026-10-26-onboarding-structure-tech.md` C3 and C4 (a line: build the levels with this tool first).

## How levels are built today (read 2026-10-26)

| Fact | Where |
| --- | --- |
| A level prefab nests `LevelBase.prefab` (Grid with `GridManager`, Tilemap, camera, the `Level` component with objectives, `EnemyAlertTracker`, faction relations) and an environment prefab (caves: `Content/LevelEnvironments/Cave/TestLevel/Prefabs/TestLevel.prefab`) | `Content/Levels/LevelBase.prefab`; every cave level |
| GridCells are instances of `Content/Levels/_Common/Prefabs/GridCell.prefab`, children of the LevelBase Grid transform, named `GridCell - (x, y)`, at `x × 0.5 + 0.25, y × 0.5 + 0.25` | e.g. `LevelLucyJohn-C1.prefab`; `GridManager` maps cells by `grid.WorldToCell(position)` |
| Units **and** hazards (`CP_Spawner`, spikes, webs) are children of their cell's `occupantRoot` (a serialized field on `GridCell`) | `LevelM1-C1.prefab`; `GridCell.cs:65` |
| The editor drag tool places an entity exactly this way: parent to `occupantRoot`, position = `GridPluggableEntity.Centroid(footprint)` | `Core/Systems/GridSystem/Editor/GridEntityDragTool.cs:303-331` |
| Footprints grow up and right from the anchor | `GridPluggableEntity.FootprintCoords` |
| Rock props are sprites only and block nothing; the playable map is the set of GridCells | `Cave_Obstacle_Rock_01.prefab` has no script |
| "All enemies start alert" is a separate `LevelAlertSettings` component, on levels that set it | `Core/Systems/EnemyAlertSystem/Runtime/LevelAlertSettings.cs`; `LevelMountainDeev.prefab` |
| Enemy tier is `CombatLevel.enemyTier` (an override on the LevelBase instance) | `CombatLevel.cs:48`; `Level1-C1_TArtEx.prefab` |
| **Every level checked carries its own extras:** a `LevelSequenceTrigger` (locks the enemy faction until a family unit walks into its collider), intro and outro sequences (that level's dialogue and actors), and usually a turn-order override (`_overrideTurnOrders` 1). `LevelBase.prefab` has none of these | `LevelLucyJohn-C1`, `LevelLindaJohn-C1`, `Level1-C2`, `LevelE1-C1`, `LevelM1-C2` |
| The level toolbar lists every prefab with a `LevelBase` under `Content/Levels` and loads it with `requireIncluded: false`; a level outside any mission plays in a sandbox mission | `Core/Levels/Editor/LevelMainToolbar.cs:16, 133`; `LevelFastForwardRoster.cs:126`; `Mission.CreateSandbox` |
| `AIRegressionTest` skips level prefabs under `/Content/Levels/` | `tech/mechanics-brief.md` |

## Block syntax added

`level` lines go after `--` with the drawing annotations. `grid_render.py` ignores lines it doesn't know, so drawings are unaffected (C3 adds them to its docstring as "read by the builder, not drawn").

```
level name Memory 1 · Linda
level tier tutorial          (standard | early | tutorial | late)
level alert all              (adds LevelAlertSettings with allEnemiesStartAlert on)
level origin 11,-10          (block tile 0,0 sits on GridCell (11, -10); default 0,0)
level template Content/Levels/Generic Levels/Medium/M1/LevelM1-C2.prefab   (default: the palette's)
```

Characters: the set `level_to_grid.py` reads and `grid_render.py` draws. `.`, `@`, `E`, `?`, `~` are floor (the last three are drawing aids for now); `#` and `_` are no tile; `R` and `d` are floor with a warning (no prefab yet); units, hazards and big units come from the palette.

## The template and what is stripped (D-237)

The builder copies the template with `AssetDatabase.CopyAsset` (new GUID), opens the copy with `PrefabUtility.LoadPrefabContents`, strips, builds, saves and unloads. It keeps the template's environment, lighting, music, camera handler, faction relations and objectives, and strips:

| Stripped | Why |
| --- | --- |
| Every GridCell instance and everything under it; units, hazards and placeholders placed elsewhere | The block is the new map |
| `LevelSequenceTrigger` components | They lock the enemies until a family unit walks into a collider that belongs to the old layout |
| Intro and outro sequences (set to none), and sequence objects that referenced removed units | They belong to the template's story |
| The turn-order override (`_overrideTurnOrders` off) | Family first by default; a block can't ask for anything else yet |
| Variant groups | They point at removed units |
| `LevelAlertSettings` | Re-added from the block's `level alert` line, so the block alone decides it |

Each item has a toggle in the palette (default on), so a template whose sequence should survive can keep it. **Default template:** `LevelM1-C2` (a cave level with "defeat all" objectives and no intro or outro of its own). The implementer confirms it is clean; THJ can change it in the palette at any time.

Graduation: when a level built here is wired into a mission (onboarding structure C3, C4), move it into that mission's folder in Unity. Its GUID, and so every reference to it, survives the move.

## Approach

### C1 · Parser, model and builder core (opus; the risky chunk)

Folder `Assets/_Project/Core/Levels/Editor/GridToLevel/` (editor assembly; namespace `MISO.Core.Levels.CEditor.GridToLevel`).

- `GridBlock.cs`, `GridBlockParser.cs`: read a markdown file, find the ```` ```grid ```` fences, parse `id`, `title`, rows (the bottom row is y 0), cells (terrain and unit per token, as the Python parser does), big-unit groups resolved to their anchor (the bottom-left tile of each connected group of `O` or `D`; a group of the wrong size is an error), and `level` lines. Errors carry the tile and the line number.
- `GridToLevelBuilder.cs`: copy the template, strip (table above), then for each walkable tile add a `GridCell.prefab` instance under the template's Grid transform, named and positioned as above; for each unit or hazard add an instance of its prefab under the anchor cell's `occupantRoot` (read with `SerializedObject`, as the drag tool does) at the footprint centroid; set the level name; save. Use `PrefabUtility` throughout: never edit `.meta` files or YAML by hand.
- C1 uses a palette built in code (the same table as `level_to_grid.py`, plus the default template) so it can be tested before C2's asset exists.
- Tests (`GridToLevelTests.cs` in the same `Editor/` folder): the parser on small inline blocks (ragged rows, an unknown character, a 3 × 2 group, `level` lines); the builder into `Assets/_Project/Content/Levels/Greybox/__Test/`, read back (cells by position, units by the cell whose `occupantRoot` they sit under, footprint anchors, no `LevelSequenceTrigger`, no missing references) and compared with the model; the test folder is deleted in `TearDown`.

Acceptance for C1: building chunk 24 (`24-nook`) in a test gives 37 GridCells and 6 units on the right tiles; parsing every block in `design/level-chunks.md` and `plans/onboarding/2026-10-26-onboarding-levels.md` raises no error.

### C2 · Palette asset, level settings, camera bounds (sonnet; two commits)

- **Commit 1, camera tool refactor:** extract `public static bool AssignBoundary(string prefabPath)` from `CameraBoundaryBatchTool` (the body of its per-prefab loop); both menu items call it. Behaviour unchanged; its own commit, so it can be reverted alone.
- **Also in commit 2 (D-342):** rebind the template's `LevelStartFPFiller.units` (if present) to the family units the block places, or an empty list when it places none; never save a null entry.
- **Commit 2:** `GridLevelPalette` ScriptableObject (D-239) at `Content/Levels/Greybox/GridLevelPalette.asset`: character → prefab, the default template, the strip toggles, the output folder. "Reset to defaults" fills it with the C1 table. Settings from `level` lines: `levelName` and `enemyTier` on the level component; `level alert all` adds `LevelAlertSettings` to the level root with `allEnemiesStartAlert` on; `level origin` shifts every tile; `level template` overrides the default. After saving, `CameraBoundaryBatchTool.AssignBoundary(path)`.

Acceptance for C2: a block with `level tier tutorial` and `level alert all` builds a level whose `level_to_grid.py` summary reads "enemy tier Tutorial; all enemies start alert: yes"; camera bounds are set.

### C3 · Window, menu, play, docs (sonnet)

- `GridToLevelWindow.cs`: **Tools › Levels › Build Level From Grid…** Doc path (remembered in `EditorPrefs`), a block dropdown, the preview (tiles, units by type, settings, template and its objectives, errors and warnings), output path, **Build** (confirm when the file exists: "Rebuild replaces GB_<id> and any edits made to it"), **Open** (Prefab Mode), **Play** (`EditorLevelLoader.LoadLevel(level, requireIncluded: false)`, as the toolbar does).
- `grid_render.py` docstring: `level` lines are read by the builder, not drawn.
- Docs: the skill gets a section "Building a level from a grid" (when to use it, the `level` lines, the template and strip list, the rebuild rule: once a level has been edited by hand, the prefab is the master and `level_to_grid.py` reads it back); `tech/level-tools.md` (new) describes the three tools together; the catalogue header, the `README.md` map, and a line in the onboarding structure plan's C3 and C4: "build each level from its paper grid with Build Level From Grid, then wire it".

## Risks

- [x] **Statics:** none planned. If the window caches parsed blocks, keep them as instance fields (domain reload is off; editor statics survive play mode).
- [ ] Code the AI reads: none.
- [ ] Serialized renames: none.
- [ ] Saved data: none.
- [x] **Assets:** all prefab work through `PrefabUtility` and `SerializedObject`, never hand-written YAML. The template copy keeps its nested `LevelBase` and environment instances linked, so later fixes to `LevelBase.prefab` reach built levels.
- [x] **Template leftovers:** stripping can leave references to removed objects (sequences, variant groups, triggers). The builder clears each known one, and the test and the window both check for missing references after the build.
- [x] **AI content:** none touched. Built levels live under `/Content/Levels/`, which `AIRegressionTest` skips.
- [ ] Events and coroutines: none.
- [x] **Other branches:** editor-only and self-contained; it merges to `main` with the onboarding work.
- [x] **Sandbox play:** a level outside any mission plays in a sandbox mission. Check in play that FTP, items and Revenge behave (the roster is whoever the level places). If the sandbox gives no FTP, Duos can't be tested there; that's a sandbox fix, out of scope, reported if found.
- [x] **Overwriting:** a rebuild replaces the prefab, after a confirm. Once a level has been edited by hand, the prefab is the master.
- [x] **Environment art:** the template's background is drawn for its own shape. Expected until THJ's edit pass; the grid tiles are visible.

## Verification set (verifier)

Build these, read each back with `level_to_grid.py`, and compare the rows with the block, both normalised as in the acceptance criteria (D-240):

| Block | Why |
| --- | --- |
| `24-nook` (catalogue) | Family, Claws, rows of missing tiles |
| `27-snare` | Spikes and traps |
| `33-deev-wave` | 3 × 2 Deev, marked tiles as floor, side pockets |
| `11-spread-pools` | Corruption pools, gaps inside the map |
| `m1-linda` (onboarding plan) | A real D-235 level, with `level tier tutorial` and `level alert all` added to its block |

Then play `GB_24-nook` from the toolbar to a win: the Claws come, Linda's Watch fires on 4,2, the win screen shows. No `LevelSequenceTrigger` holds the enemies.

## Onboarding fit

Checked 2026-10-26 against the ten blocks in [`onboarding/2026-10-26-onboarding-levels.md`](onboarding/2026-10-26-onboarding-levels.md), which onboarding structure C3 and C4 build (D-235).

**The tool builds:** every tile, hero and enemy in all ten blocks (only `c`, `a`, `J`, `L`, `U`, `M`, with `#` walls and `_` water gaps); the tier and "all enemies start alert" from `level` lines; a different template and origin per block, so each level can sit on the source the paper plan names (segment 1 on `Level1-C1-2`, the River on `LevelLucyJohn-C1`, the Ridge on `LevelLindaJohn-C1`, the pile on `LevelLucyJohn-C3`).

**Before building:** each block needs its `level` lines. Memory 1–4: `tier tutorial`, `alert all`. River and Ridge: `tier tutorial`. M2's four: `tier early`. Plus `template` and `origin` where the plan names a source. The game designer adds them to the paper plan (their file); the implementer may add them in C3 and C4 and report it.

**Left to the wiring in structure C3 and C4** (out of v1, D-238):

| Need | Levels |
| --- | --- |
| Stage objectives: punchline or turn cap | Memory 1–4 |
| Exit objective (`E` builds as plain floor) | M2 trailhead |
| "Unit on tiles" stage on 6,9 / 7,9 / 8,9 | Memory 4 |
| Per-instance HP (6, 8, 12, 16) | Memory 1, 2, 4; M2 blood |
| Spawns on cue (`cells … spawn` lines are drawing notes) | Memory 2 and 4, the pile's rear wave (its "starts alert" variant) |
| The mother and the cub (`R` on 7,10 builds as floor, with a warning) | Memory 4 |
| Sequences, `LevelStartFPFiller`, Tempest Bloom grant | Memory 1–4, M2 |

**Watch out:** segment 1's template `Level1-C1-2` carries the D-131 grid-fade outro, which the default strip removes. Every memory segment needs that fade (paper plan, grid fade rule), so C3 re-adds it to each segment (or keeps it on segment 1 with the palette's sequence toggle off). The templates' background art won't match the new shapes; expected until THJ's edit pass.

## Gates

Compile clean / EditMode suite green except the known red / review: yes (editor tool; the camera tool refactor is checked for unchanged behaviour) / play check: yes, one session in THJ's editor (verifier, after THJ agrees a time) / docs: skill, `tech/level-tools.md`, catalogue header, README map, onboarding structure plan C3–C4.

## THJ's answers (2026-10-26)

| # | Question | Answer |
| --- | --- | --- |
| 1 | Where do built levels go? | `Content/Levels/Greybox/GB_<id>.prefab` (D-236) |
| 2 | What is a level built from? | A copy of an existing level, stripped (D-237) |
| 3 | Which settings in the first version? | Name, tier, alert, origin; objectives later (D-238) |
| 4 | Rebuild policy | Replace after a confirm; a hand-edited level becomes the master (recommendation, no objection) |
| 5 | Fit with D-201 | Superseded by D-235: this tool is the first step of the plan-to-level workflow |
| 6 | Where the character → prefab table lives | A `GridLevelPalette` asset (D-239) |

## Docs to update when done

- `claude-config/skills/miso-level-chunks/SKILL.md`: "Building a level from a grid" (master; THJ runs the sync to `.claude/skills`).
- `tech/level-tools.md` (new, coordinator).
- `design/level-chunks.md`: one line in the header (game designer).
- `README.md`: `tools/` and the greybox folder (coordinator).
- `plans/onboarding/2026-10-26-onboarding-structure-tech.md`: C3 and C4 start from this tool (coordinator).
- `build-log.md`: a dated section per chunk.
