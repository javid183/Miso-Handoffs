# Onboarding structure C3: the Hearth memory levels and sequences

Size: L (two chunks)    Tier: 2 (content + editor tool; THJ: "Start C3"; any core change found → stop, Tier 3)    Assigned to: `miso-game-designer` (block lines) → `miso-implementer` (C3a, C3b) → `miso-reviewer` → THJ play check per chunk
Branch: `thj/onboarding`. Status: **C3a done 2026-11-01**, committed `3c99b3ee6` (component, sequence, `level hidden`, tests), `a161e0956` (four levels), `9ace80c28` (Hearth wiring + XP test); review FIX → fixed → APPROVE; EditMode 1172/1173 known red only; THJ play-checked OK; reveal route D-346. C3b not started; open: what segment 4's revealed Claws do after the mother falls

## Why

The Hearth (`Content/Levels/M0 - The Hearth.asset`) still plays three old M1 levels as placeholders. C3 builds the four memory segments from their paper blocks with the grid tool and gives them their rules and scenes, so THJ can play and time the memory (structure tech `plans/onboarding/2026-10-26-onboarding-structure-tech.md` § C3; paper plan `plans/onboarding/2026-10-26-onboarding-levels.md` § The Hearth memory; decisions D-200, D-226, D-235, D-338, D-344, D-345).

## Goal

New game → the Hearth plays memory segments 1–4 in order with no XP, alert enemies, full family time points at each start, the scripted cues, and ends in the Hearth close.

## Acceptance criteria

C3a (levels, playable without scenes):
- [ ] `GB_m1-linda`, `GB_m2-lucy`, `GB_m3-john`, `GB_m4-mark` built from their blocks with `level tier tutorial`, `level alert all`, `level xp none`, `level fp full`; each round-trips through `level_to_grid.py` to the same tiles and units.
- [ ] The Hearth's level graph is the four segments in order (old M1 levels unlinked from it, their prefabs untouched); `completionXPReward` 0.
- [ ] Cue enemies (segment 2's three Claws on 9,3 / 10,2 / 9,1; segment 4's Claws by the mother) are placed and stay out of play until revealed: not targetable, not in turn order, no AI turns, not blocking tiles, not counted by objectives. A reveal action brings them in, alert.
- [ ] EditMode test: `LevelXpChecker.CheckMission(M0 - The Hearth)` reports nothing, and the XP resource id resolves (not empty).
- [ ] Per-instance HP from the paper tables (segment 1 A 14 / B 6 / C 2; segment 2 placed 6; segment 4 prism 6, gallery and hall 8).

C3b (sequences):
- [ ] Each segment's win is its punchline stage with the turn cap from its table; the end sequence fades the grid out with `OutroCutsceneKeepGridHidden` and plays the Hearth cutaway (`DialogNodeSequence`, placeholder still + lines from `plans/onboarding/onboarding-narrative-draft.md`); the next segment fades it back in. Segment 4 keeps the grid on through the mother's scene and the walk; fades on the win.
- [ ] Segment 2's stage-1 interruption and segment 4's mother scene freeze, move the camera, reveal the cue enemies, play their lines, and resume.
- [ ] Segment 4: Tempest Bloom at the open — a sequence casting it if sequences can fire abilities, else `LevelStartRunUpgradeGrant` with `RU_LindaLucyCycloneSpreadUnlock` plus the guided action; Mark walks in from the edge (`MoveUnitSequence`); stage 2 win on a Bergson reaching 6,9 / 7,9 / 8,9; Tempest Bloom gone in The River.
- [ ] The Hearth open and close Home states (`homeState`), and the first level's start panels per the segment 1 table.

## Scope

In: the four memory levels, their data, the hide/reveal of cue enemies (existing pieces, or a small non-core component + a grid-tool line), the Hearth wiring, sequences and placeholder text, the Hearth XP test.
Out: The River, The Ridge, The Trail (C4); Home visits (C5); final art (mother wolf, cub, stills are placeholders: `Home - Imported/Entities/Characters/Wolf/Wolf.prefab`, `NPCs/Ryker/Ryker.prefab`); final narrative; Bond Lite; the timed pacing run.

## Touches

Systems: Levels/Mission (data only), LevelSequence and LSB actions (use, not change), GridToLevel tool (editor), possibly a new non-core component in `Features/Onboarding/`. Core: none expected; `GUnit`, `FactionTracker`, turn order, AI, `MissionTracker` behaviour changes → stop and ask.
USPs: Family Roles, Synergies (Tempest Bloom), Duos (Chained Assault), Continuous Attack.
Docs: `tech/level-tools.md` (any new line), `tech/combat-architecture.md` (any new component), structure tech § C3 status, `status.md`, `build-log.md` (coordinator).

## Approach

**Step 0 · Game designer (paper, before C3a).** In the four memory blocks of the levels plan: add the `level` lines (`name`, `tier tutorial`, `alert all`, `xp none`, `fp full`, `camera` where the rule wouldn't show the right opening); draw segment 2's three cue Claws as enemies on 9,3 / 10,2 / 9,1 and segment 4's Claws, the mother and the cub on their tiles; mark the cue enemies with a proposed `level hidden x,y …` line (the tool gets it in C3a); keep the tables in step.

**C3a · opus (risk first).**
1. **Hide/reveal check, before any building.** Find how a placed unit can stay out of play until a sequence reveals it with existing pieces (inactive GameObject + an LSB/sequence that activates and registers it, `LevelSpecificBehaviour`, faction or alert hooks…). Check every system that collects units at level start (turn order, AI, objectives "all enemies dead", grid occupancy, enemy alert, FTP/roles, camera bounds, fast-forward roster). If the only route changes a core system's behaviour, stop and report the options. If a small non-core component does it, build it (+ tests) and add `level hidden x,y …` to the grid tool (parse, preview, build, tests).
2. Build the four levels with the tool; round-trip each with `level_to_grid.py`; set the per-instance HP; place the mother and cub as non-combat placeholders (or note what's missing).
3. Wire the Hearth's level graph to the four segments; keep `completionXPReward` 0.
4. The Hearth XP EditMode test.
Report: the reveal route chosen, what each level needed by hand after the build (so a rebuild doesn't lose it), anything from the paper plans' "To check" rows answered on the way (can a sequence fire an ability? Bloom copy range? Chained Assault's "within 4"?).

**C3b · sonnet.** Sequences and stages per the acceptance list, using the reveal from C3a. One level at a time, segment 1 first.

## Risks

- **Statics:** any new component holds none, or gets a `PlayModeStaticReset` hook.
- **Hidden units and core lists:** the main risk; step 1 checks every collector before building. Abort/restart: a restart reloads the level, so hidden state must come from the prefab, not runtime state.
- **AI content:** new levels don't change `AIRegressionTest`'s levels; stays known red, never re-baselined.
- **Prefabs:** levels from the tool; hand edits after the build are logged (the prefab becomes the master).
- **Merge safety (D-341):** the Hearth asset and `GB_` levels are new on this branch; nothing for `tech/onboarding-merge.md` unless a shared file is touched.
- **Save data:** testing may reset the save; say so in reports.

## Gates

Per chunk: compile clean / EditMode (only `AIRegressionTest.Baseline_MatchesCurrentAI` red) / review / THJ play check (yes: C3a the four levels from the toolbar and a new game into the Hearth; C3b the full Hearth) / commits split (component + tool line + tests; levels; Hearth wiring + XP test; sequences per segment) / docs above.
