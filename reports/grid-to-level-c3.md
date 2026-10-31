# Report: Grid-to-level C3 (window, menu, play)

Plan: plans/2026-10-26-grid-to-level-tech.md (C3)    Agent: miso-implementer (sonnet)    Branch: thj/onboarding
Outcome: done (play check by THJ still to do)

## What changed

- `Core/Levels/Editor/GridToLevel/GridToLevelWindow.cs` (new): **Tools > Levels > Build Level From Grid...**. Doc path (remembered in `EditorPrefs`, default `<repo>/claude-handoff/design/level-chunks.md` from `Application.dataPath`), Browse and Reload, reload on focus when the file changed, block dropdown (id - title, last block remembered), preview (tiles, units and hazards by type with their prefab names, level name, tier, alert, origin, template and its objectives with the "NOT the defaults" warning, output path), errors then warnings, Build/Rebuild (confirm "Rebuild replaces GB_<id> and any edits made to it"; leaves Prefab Mode first if that level is open), Open in Prefab Mode, Play (`EditorLevelLoader.LoadLevel(level, requireIncluded: false)`). Build is disabled while any error stands or Play mode is active. All caches are instance fields.
- `GridTemplateObjectives.cs` (new): reads a template's objectives and compares a fingerprint (branching mode, objectives, decisions: values, condition types, referenced object names) with `LevelBase.prefab`'s. `Validate` now adds a Warning when they differ.
- `GridToLevelBuilder.cs`: the camera fallback warning names the two real menu items; `RemoveStrayEntity` reports an Error and returns false when the component survives `DestroyImmediate`.
- `GridToLevelSettingsTests.cs`: Strip tests now build under `EditorSceneManager.NewPreviewScene` (never the open scene); new tests: `Build_FailingAfterValidationWritesNoOutputFolder` (template with no tilemap passes validation, fails in the build, no folder), `Strip_ReportsAnErrorWhenAnotherComponentKeepsTheEntityAlive` (GUnit + `MemorableAttackMemoryShare`, expects Unity's "Can't remove" log), `Objectives_*` (2).
- `claude-handoff/tools/grid_render.py`: docstring line that `level` lines are read by the builder, not drawn.
- New content: five `GB_` prefabs (below).

## Acceptance criteria

- [x] Window, preview, listed errors/warnings, objectives warning: built; opened once via the menu with no console error. Needs THJ's eyes for layout.
- [x] Rebuild confirm, Open, Play: coded; Play not pressed (per instruction). Needs the play check.
- [x] Missing-reference check: builds report no issues for all five.
- [x] Round trip, 5 of 5 (table below).
- [x] EditMode suite: 1099 run, 1098 pass; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched).
- [x] Active scene (`PreloadScreen`) not dirty after the full suite.

## Verification table

Built with `GridToLevelBuilder.Build(block, GridLevelPalette.Load())`, read back with `python claude-handoff/tools/level_to_grid.py "Content/Levels/Greybox/GB_<id>.prefab"`, both sides normalised (`#`->`_`, drawing aids and R/d -> `.`, cropped to the cells).

| Block | Tiles | Placed | Rows match | level_to_grid summary |
| --- | --- | --- | --- | --- |
| `24-nook` | 37 | 6 | yes | 3 Dark Claw, John, Linda, Lucy; Standard |
| `27-snare` | 45 | 9 | yes | 2 Spike, 2 Trap, 2 Dark Claw, family 3 |
| `33-deev-wave` | 57 | 6 | yes | Deev (3x2), Spike, family 4 |
| `11-spread-pools` | 49 | 8 | yes | 4 CP_Spawner, family 4 |
| `m1-linda` | 18 | 4 | yes | 3 Dark Claw, Linda; "enemy tier Tutorial; all enemies start alert: yes" |

`m1-linda` was built from the plan's block with `level tier tutorial` and `level alert all` appended in memory only; I did not edit the plan doc. No build issues or warnings on any of them.

## Kept GB_ prefabs (Content/Levels/Greybox/)

`GB_24-nook`, `GB_27-snare`, `GB_33-deev-wave`, `GB_11-spread-pools`, `GB_m1-linda` (each with its `.meta`). They appear in the level toolbar dropdown.

## Save reset

no

## Decisions I made

- Objective defaults = the objectives of `LevelBase.prefab` (fingerprint compare), not a hard-coded shape; the default template `LevelM1-C2` passes (test).
- The objectives warning lives in `Validate` (so tests and the window both see it) and is shown once, in its own box, not repeated in the issue list.
- Output path is shown, not editable.
- Dependent-component test uses a GUnit on an environment slot (an Editor-folder helper component can't be attached).
- `Debug.LogWarning/LogError` on build issues carries the block id only (no private IDs).

## Needs THJ

Play check below.

## Docs input (for tech/level-tools.md and the skill)

- Menu: Tools > Levels > Build Level From Grid... Pick the doc (default `design/level-chunks.md`), pick a block, read the preview, Build. Output `Content/Levels/Greybox/GB_<id>.prefab`; the level shows up in the level toolbar.
- `level` lines (after `--`, ignored by the drawing tool):
  ```
  level name Memory 1 · Linda
  level tier tutorial          (standard | early | tutorial | late; no line = Standard)
  level alert all
  level origin 11,-10
  level template Content/Levels/Generic Levels/Medium/M1/LevelM1-C2.prefab   (relative to Assets/_Project/)
  ```
- Template: default `LevelM1-C2` (palette asset can change it). Kept: environment, lighting, music, camera, faction relations, objectives. Stripped (palette toggles, default on): all GridCells and anything placed on the grid, `LevelSequenceTrigger`s, intro/outro sequences, turn-order override, variant groups, `LevelAlertSettings` (re-added from `level alert all`). `LevelStartFPFiller` is rebound to the placed player units (build warning lists its kept values).
- Rebuild rule: rebuilding asks, then replaces the prefab whole (GUID kept); once a level is hand-edited the prefab is the master and `level_to_grid.py` reads it back.
- Known limits: objectives are the template's (window warns if not the defaults); `R` and `d` build as floor with a warning; `E @ ~ ?` are plain floor; template scenery props (rocks, statues, background art) remain and don't match the new shape; no per-unit HP, deploy slots, sequences or Mission wiring; the Greybox palette falls back to the code table for empty slots.

## Docs to update

Coordinator: `tech/level-tools.md`, the skill section, catalogue header, README map, onboarding structure plan; plan log with commit hashes.

## Risks and loose ends

- Unity logs "Serialization depth limit 10 exceeded" for ability classes during the suite; pre-existing, unrelated.
- Rebuild while the level is the one open in Prefab Mode: the window leaves Prefab Mode first.
- Line endings: new files LF like the other GridToLevel files.
- Dirty files `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*` untouched.

## Proposed commits

1. `feat(levels): build-level-from-grid window with preview, rebuild confirm, open and play` (plain): `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/{GridToLevelWindow.cs,GridToLevelWindow.cs.meta,GridTemplateObjectives.cs,GridTemplateObjectives.cs.meta,GridToLevelBuilder.cs,GridToLevelSettingsTests.cs}`
2. `content(levels): greybox levels built from the first five grid blocks` (separate, revertable): the five `GB_*.prefab` and `.meta` files under `miso/Assets/_Project/Content/Levels/Greybox/`.

(`grid_render.py` is in `claude-handoff/`; coordinator commits it there.)

## Other branches

none

## How to see it / play check

1. Tools > Levels > Build Level From Grid... : the block list should show every chunk; pick `24-nook`; preview shows 37 tiles, units by type, template `LevelM1-C2`, "defaults" objectives.
2. Build (it exists, so it says Rebuild and asks); then Open in Prefab Mode.
3. Pick `GB_24-nook` in the level toolbar dropdown (or press Play in the window) and play it: the Claws should come, Linda's Watch on 4,2, win screen. Check FTP is available and enemies act in the sandbox mission (no `LevelSequenceTrigger` holding them).
4. Also try `GB_33-deev-wave` (Deev 3x2) and `GB_m1-linda` (tier Tutorial, enemies start alert).
