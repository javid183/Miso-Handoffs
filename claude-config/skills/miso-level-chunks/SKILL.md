---
name: miso-level-chunks
description: Design Miso level content on paper with tile-addressable grids: reusable chunks and enemy or challenge patterns where each family mechanic is a possible answer, full paper levels ready to greybox, and grid reads of existing level prefabs. Use whenever work touches level layouts, encounters, a level's enemies or hazards, a tutorial or showcase level, or drawing a grid.
---

# Miso level chunks

A Miso level is a puzzle: the family's tools (abilities, Family Roles, Synergies, Duos) are the pieces, and a better solve should give a better result. Design on paper before anyone greyboxes. A text grid every agent can read, diff and cite by tile is cheaper to iterate than a prefab, and a drawing generated from it is what makes it readable by eye.

Everything here rests on one format: a fenced `grid` block in a markdown doc, drawn by `claude-handoff/tools/grid_render.py`. The text is the master, and the drawings are output. Never edit an SVG by hand.

## Which job is this

- **A chunk or a pattern.** A small piece of a level (up to about 11 × 11) that asks the player one question. It goes in the catalogue, `claude-handoff/design/level-chunks.md`, which is also the reference for the legend, the patterns, the knobs and what has been checked.
- **A paper level** (or a mission's set of levels) that a builder can greybox without asking a design question. It goes in a design plan under `claude-handoff/plans/`. `plans/onboarding/2026-10-26-onboarding-levels.md` is the worked example.
- **Reading an existing level.** Turn a level prefab into a grid block with `claude-handoff/tools/level_to_grid.py` (below).
- **Building a level from a block.** Turn a paper grid into a playable greybox prefab with **Build Level From Grid** in Unity (below).

Real work often uses all three: read the source level, reuse catalogue chunks, write the paper level.

## What's true before you design

Design against the game as built, not as remembered. Read:

- `design/gdd/family-systems.md` (Roles, Duos, Synergies, Pass-by), the character sheets, `enemies.md` (including the alert state, EN-12 to EN-17), `combat-rules.md` (tiers CR-32, previews CR-37 to CR-43), and `missions-structure.md` (objective conditions MI-17 and MI-18, "all enemies start alert" MI-27).
- Plans whose rules aren't in the GDD yet: an open plan's recommended values may be used, but the doc says so.
- The catalogue's enemy and hazard references and its "To check" table: they hold the movement and reach values read from the presets, and the questions already asked.

When a number isn't in the GDD, read the preset (`Resources/UnitSpecific/...`, `Features/Hazards/...`) or the script. Mark every claim as verified (and where) or assumed, and put each assumption in a to-check row. A chunk that only works if an assumption holds says so.

Facts that are easy to get wrong:

- **Coordinates:** x counts from 0 at the left, y from 0 at the **bottom**, as in Unity's grid. Write tiles as `3,4` in prose and tables.
- **Ranges are Manhattan steps** unless the ability says otherwise. Linda's arrow is row or column only. Movement is four-way, so diagonal pockets can't be walked into.
- **The playable map is the set of GridCells.** Rock props (`Cave_Obstacle_Rock_01`, `BecStatue`) are sprites only and block nothing. In a paper level, `#` and `_` both mean "no GridCell here" (or an obstacle entity with a component). Tell the builder which.
- **Big units' footprints** grow up and right from the anchor tile: the Masher is 2 × 2, the Deev 3 × 2.
- **Alert state:** enemies start Unaware. They wake when a family member, an ally, a decoy or a protectee stops within sight (3 Manhattan steps through walls, 2 for the Masher). They also wake when something happens to them, or when a family ability lands within 2. Waking spreads within 2. Bosses always start alert, and a level can set "all enemies start alert". For every drawing, check who starts within 3 of the family; that decides whether the opening is a setup turn or a crisis.

## The grid format

````
```grid id=07-bell title="7. The bell"
# c . . . c #
# . c b c . #
# . U J . L #
--
arrow 3,0 3,1 john ring
range 3,1 5 enemy the pack hears
step 3,0 1
```
````

- Cells are separated by spaces. A cell is one terrain character, one unit character, or both (`c^` is a Dark Claw on spikes). The legend lives in `grid_render.py`'s docstring and at the top of the catalogue. Read it there rather than copying it.
- Annotations go after `--`: `arrow` (a path through tile centres, `dx=`/`dy=` to separate two arrows on one lane), `zone`, `cells`, `range X,Y R` (every walkable tile within R steps), `step` (a numbered badge) and `note`. Colours are `john linda lucy mark toba enemy heal shaman note` or a hex value.
- The drawing shows the intended solve, not every option: one or two arrows for the smart play, a tint for the zone that matters (a lane, a heal or summon range, a danger zone), and step numbers when order matters. Keep labels to a few words.
- Every block needs a unique `id`. The catalogue numbers chunks (`19-mender`); paper levels use a short slug.

## Designing a chunk

1. **One question**, in a sentence the player would recognise: "the arena tilts every time you hit it: where do you end your turn?"
2. **Answers table:** Answer | How | grade. Use ★ for a smart solve, ● for one that works at a cost, ✗ for a trap. Aim for at least two ★ from different family members or systems, so there's a real choice. The *How* names the tiles and states the distance it relies on ("from 4,1 the Shaman on 4,5 is 4 tiles away").
3. **Count every distance** against the real values: embers 3, Linda's arrow 4 in a line, Crescendo 5, Command 4, Vault 3, Blink 5, Fist Blitz 2, Shield Dash 3; Claws move 4, Archers 3 and shoot 3, Worms 1. A ★ that's one tile out of reach is the most common error.
4. **Knobs:** the variables that turn one chunk into a family of them (passage width, distance against a range, clocks, who acts first, symmetry, tier, what's at stake, who is awake). The catalogue's "Pattern knobs" table is the shared list. Add to it when a new knob appears.
5. **Teach one new layer at a time.** A combination chunk comes after its parts have chunks of their own.
6. **Update the catalogue around it:** the contents table, the coverage table (mechanic → ★, ●, ✗ chunks), the gaps (a mechanic with no ★ gets a chunk idea), the enemy and hazard references, and to-check.

## Designing a paper level

Start from a source map where one exists (read it with the tool), reuse catalogue chunks by number, and give every level this table, as the onboarding plan does:

| Item | What it holds |
|---|---|
| Source | The level prefab it reworks, or "new"; what changes |
| Teaches | The one thing this level teaches |
| Twist | What makes it more than the lesson, separate from it |
| Squad | Who plays, and where each starts |
| Enemies | Types, tier, in-play HP if tuned per instance |
| Turn budget | Expected turns, and the cap if there is one |
| First trigger | Where the first Role, Synergy or Duo fires, and why the layout forces it there |
| Win / loss | Only what the objective conditions can express (MI-18); stages if needed |
| Cues | Lines, panels, sequences, and when they play |
| Alert | Who is awake at the start, or "all enemies start alert" |
| FTP, drops, clue | Starting FTP, level-start fills, rewards, story clues |
| Fallback | What happens when the player misses the intended play |
| Time | Minutes for a cold player |

Flag anything that needs new tech or touches a core system (`tech/core-systems.md`). It goes to THJ, not into the level quietly.

## Reading an existing level

```
python claude-handoff/tools/level_to_grid.py "Content/Levels/Level1/Level1-C2.prefab" [more prefabs] [--id <id>] [--no-shift]
```

Paths are relative to `miso/Assets/_Project`, as the GDD's Source lines write them. The tool prints a ready-to-paste `grid` block and a summary: tile count, enemy tier, the alert setting, objective texts, what was placed, scenery left out, anything it couldn't place, and anything off the grid. It reads the prefab YAML only, so Unity can stay open, and it never writes.

- **The title carries the offset.** "offset x-11, y+10" means grid x = prefab x − 11 and grid y = prefab y + 10, so a builder adds 11 back to x and subtracts 10 from y. Keep the title when you paste the block, so tiles can be mapped back to `GridCell - (x, y)`.
- Units are placed by following their parent to the GridCell they sit under. Anything placed by position instead is listed: check those in the editor.
- Deploy slots, story units and the Goblin Queen come out as `note` lines.
- If a GUID is missing, rebuild the map with `claude-handoff/reward-tools/build_guidmap.py`. If a prefab has no GridCells, it nests another level: run the tool on that one.

## Building a level from a grid

In Unity, **Tools › Levels › Build Level From Grid…** turns one block into `Content/Levels/Greybox/GB_<id>.prefab`, playable at once from the level toolbar (sandbox mission). Full reference: `claude-handoff/tech/level-tools.md`.

- **When:** a paper level is ready to greybox. Build first, then wire the mission, sequences and data; THJ edits after.
- **`level` lines** after `--` set what the grid can't: `level name <text>`, `level tier standard|early|tutorial|late` (no line = Standard), `level alert all`, `level origin x,y`, `level template <path under Assets/_Project/>`, `level camera x,y` (the tile the opening view centres on), `level xp none` (placed enemies give no XP; for memory levels), `level fp full` (family time points topped up to full at level start), `level hidden [group] x,y …` (units on those tiles start out of play until a level sequence reveals the group; cue enemies instead of spawns), `level deploy x,y …` (a deploy slot for the mission roster's free pick instead of a drawn hero). The drawing tool ignores them.
- **Camera start:** the build places the Camera's `InitialCameraPosition` so the opening view shows the whole level when it fits one screen at the default zoom, and otherwise is pulled toward the player units' starting tiles. Add `level camera x,y` when the opening should look somewhere else (an objective, an incoming threat). **Tools › Levels › Place Camera Start** re-places it on an existing prefab.
- **Template:** a copy of `LevelM1-C2` by default; it keeps the environment, camera, faction relations and **objectives** (the window warns when they aren't "defeat every enemy / lose when the family is down"), and strips the template's grid, triggers, sequences, turn-order override, variant groups and alert settings.
- **Enemy facing:** enemy prefabs face left by default (`Unit_DarkClaw` `initialDirection.x` = -1). The build sets `initialDirection.x` = 1 on every placed enemy, hidden ones too, whose footprint centre is left of the middle of the family's main group: heroes and deploy slots, grouped by column, with a gap above 3 splitting them (so a hero who starts apart, like Mark in `GB_m4-mark`, is left out), and the largest group is the main one. Enemies on the middle or to the right keep the default. Check it after building, and set it by hand on levels built before this rule or edited by hand. Include it in any wiring tool for the level.
- **Check after building:** read it back with `level_to_grid.py`; the rows should match the block once `#` → `_`, drawing aids → `.`, cropped to the cells.
- **Rebuild rule:** a rebuild replaces the prefab whole (it asks first). Once a level has been edited by hand, the prefab is the master; read it back instead of rebuilding.
- **Not from the block yet:** objectives, per-unit HP, deploy slots, sequences and cues, Mission wiring, matching scenery.

## Drawing

```
python claude-handoff/tools/grid_render.py <doc.md> [--out <folder>]
```

It writes one SVG per block and an `index.html` sheet into a folder next to the doc, named after it (or `--out`). Rerun it after every grid edit. In the doc, link each drawing under its block: `![19](level-chunks/19-mender.svg)`.

**Who runs it.** The game designer agent has no shell. It writes the grid blocks, and its summary lists every doc whose grids changed. The coordinator runs the renderer, **looks at the drawings**, and fixes or returns anything that doesn't match the text before reporting. A session with a shell renders and checks its own.

**What to check in a drawing:** every unit is on the tile the text says, every claimed distance holds when counted on the axes, rows have equal length (the renderer warns otherwise), arrows start and end on the intended tiles, labels don't overlap, a footprint doesn't run into a wall, and each ✗ really fails. Report what you checked in the drawing and what you only read in the text: they are not the same claim.

## Extending the tools

When a new enemy, hazard or terrain appears, add it to both tools rather than working around it:

- In `grid_render.py`, add its character to the terrain or unit table, give it a look, and add it to the docstring and the `LEGEND` list. Then add it to the catalogue's legend block.
- In `level_to_grid.py`, map its prefab to the same character (`UNIT_CHARS`, `TERRAIN_CHARS`), or to a note (`NOTE_NAMES`).

A tool change is reviewed like any other: say what you changed in your report. A new tool, or a new kind of output from one, is THJ's call (`escalation.md`).

## Rules

- **Propose; THJ decides.** A chunk may suggest a new enemy rule or mechanic, but only as a question in a plan, never as a fact in the catalogue.
- **Names** come from `glossary.md`; new ones are proposals.
- **One home per fact.** Rules and values live in the GDD; the catalogue and plans cite rule IDs and copy only the numbers the geometry needs, with their source.
- **Branch:** say which branch a level or chunk assumes when it differs (`branches.md`).
- Chunks and paper levels live in `claude-handoff/`, never in the shared repo.
