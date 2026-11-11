# M2 The Trail: levels rework (after-Hearth chunk 3)

Size: L (data + editor wiring, no runtime code)    Tier: 2 (tech choices; design approved D-466 to D-475, order D-501)    Assigned to: `miso-implementer` (sonnet)
Branch: `thj/after-hearth` (onboarding content; counts as `all` once merged)
Status: C1 committed `e3a45983b` (2026-11-11, D-506) as the base; challenge redesign follows (D-505, `plans/onboarding/2026-11-11-post-hearth-challenge-design.md`). C2 text still open.

## Why

The after-Hearth design (`plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`, section "M2 · The Trail", build-order chunk 3) turns The Trail from a walk + routes into challenge levels: a one-turn Trailhead fight, both routes reworked, The Pile rebuilt with a real search and a two-sided ambush, the sisters' Duo locked (D-470). Never queued until D-501.

## Goal

The four Trail levels play as the design's blocks say, wired by an updated **Wire Search: Trail**, with the tests following.

## Acceptance criteria

All four levels (`Content/Levels/Greybox/GB_m2-trailhead`, `GB_m2-tracks`, `GB_m2-blood`, `GB_m2-pile`):
- [ ] Layout, unit placement, tier Early, deploy slot and alert settings match the design's grid block for that level (blocks renamed to `m2-*` ids, see C0). Linda and Lucy placed at 2,1 and 1,1, the free pick's slot at 0,1 (Pile: sisters on the top row, slot at 4,6, as the block).
- [ ] Every enemy starts alert (`LevelAlertSettings.allEnemiesStartAlert`, from `level alert all`).
- [ ] The Linda–Lucy Duo (`Resources/Abilities/Cooperation/Linda_Lucy/Trigger/Linda_Lucy_Duo_Ability.asset`) is locked for both sisters via `LevelAbilityLock` (pattern `HearthMemoryWiring.John.cs:139-172`), hidden from the bar. The free pick's Duos are not locked.
- [ ] No FTP drain anywhere (the −99 `LevelStartFPFiller` goes from Trailhead, Tracks, Blood). FTP is full (5) at the Trailhead's first player turn: if the mission does not start full by default, the wiring adds a +99 filler instead (say which in the report).
- [ ] No Pass-by panel on either route; no Items panel at the Pile. Their sequence assets may stay on disk unreferenced (list them in the report; don't delete).
- [ ] Enemy HP factors (prefab override on `Stat_HP` factor, via the existing `SetHealth`): Dark Claws 0.6, Archer Goblins 0.25, on every Trail level. No other overrides left.

Per level:
- [ ] **Trailhead:** two Claws at 5,1 and 6,1; 9 cells; the exit tile and its objective go. Win = defeat all enemies; winning opens the mission map as before. Intro lines unchanged (new lines come in C2).
- [ ] **Follow the tracks:** Archers at 4,5 and 4,6 (static, as today), Claws at 7,1 / 8,1 / 10,1. Stage 1 (both Archers dead → Encore cue) and stage 2 (defeat all) unchanged.
- [ ] **Follow the blood:** gully Claws 4,3 / 4,4 / 4,5, side gully 6,4 / 6,5. Intro "Her blood." and the end clue unchanged; win = defeat all.
- [ ] **The Pile:** pile props on 4,3–5,4 (existing `BuildPileProps`, re-placed to the new footprint if needed). Stage 1 "Search the pile." = `TilesOccupiedLOCondition`, player faction, Any, tiles 4,5 and 5,5 (goal-tile highlight shows). On completing it: reveal hidden groups `west` (Claws 0,4 1,4 2,4) and `east` (Claws 9,4 9,3, Archer 9,6) with `RevealUnitsSequence`; revealed units are alert. Stage 2 = defeat all. The turn-2 rear wave (`WireRearWave`, `GUnitSpawnManipulationAction`) is removed; the starts-alert Claw variant stays on disk (other levels may use it; check and report). After the search tile and before the reveal, Lucy says "No white fur… she's not here." (D-504, working line, in the existing dialog style). Intro lines and the 8-step outro unchanged (minus the Items panel).
- [ ] Mission asset: graph, roster and items unchanged (re-running `WireMission` must leave the file as is, or the diff is explained).

Process:
- [ ] Built with **Tools > Levels > Build Level From Grid...** from the design doc's blocks, then **Tools > Onboarding > Wire Search: Trail** re-run; the tool stays idempotent (a second run changes nothing).
- [ ] `SearchTrailTests` updated to the new layouts and rules (deploy slots, no drain, factors, no Pass-by/Items panels, Pile tile search + reveal instead of the rear wave, Duo lock on all four, all-alert on all four); EditMode suite: every test passes except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: the four prefabs (rebuilt), `Features/Onboarding/Editor/SearchWiring.Trail.cs`, `SearchTrailTests.cs`, Trail sequence assets the tool regenerates.
Out: new text (C2), runtime code, core systems, the Home flow, the River and Ridge (chunk 4), the goal-tile colour (chunk 5), `M2 - The Trail.asset` sequences/home state (owned by `HomeVisitsWiring`), THJ's uncommitted files (AI diagnostic, `PreloadScreen.unity`, ProjectSettings, TMP font).

## Touches

Systems: level prefabs, onboarding editor wiring, grid-to-level tool (used, not changed). No core system changed.
USPs: Synergies (Shield Flare, Catch & Return as answers), Duos (locked).
Docs: after build — design plan as-built note + `design/gdd/missions-structure.md` M2 rows + `design/level-chunks.md` island/perch knob (`miso-game-designer`); `plans/onboarding/2026-10-26-onboarding-levels.md` M2 sections marked superseded (designer); `tech/onboarding-merge.md` / `tech/classic-fallback.md` only if a wiring point is added (coordinator).

## Code facts (Explore, 2026-11-11)

- Grid tool: `Core/Levels/Editor/GridToLevel/`; saves to `Content/Levels/Greybox/GB_<block id>.prefab`, overwriting (GUID kept) from the template; strips sequences, triggers, alert settings → the wiring must be re-run after every rebuild. Lines `level alert all`, `level hidden <group> tiles`, `level deploy` all implemented.
- Wiring: `SearchWiring.Trail.cs` (menu at line 73; Trailhead 129-163, drain 182-204, Blood 208-231, Pass-by panel 236-251, Tracks 255-326, Pile 337-419, rear wave 423-469, props 473-486, mission 490-550, HP 622-662). Re-runnable by design. No hand edits on the prefabs since the last run (only reserialization noise `bb8c8b966`).
- Reveal examples: `HearthMemoryWiring.Lucy.cs:186-196,367`, `Mark.Sequences.cs:111`. Mind `Mark.Level.cs:58-63`: the next stage is checked only after the stage's onComplete sequence has played.
- HP: Early row is 1.0 in `EnemyFaction.asset`; Claw base 16 → 0.6 ≈ 9.6.

## Approach

**C0 · designer (before C1).** Rename the four block ids in the design plan so the tool rebuilds the existing prefabs: `after-trailhead` → `m2-trailhead`, `after-trail` → `m2-tracks`, `after-blood` → `m2-blood`, `after-pile` → `m2-pile`; image links follow. Coordinator re-renders and checks. (D-502.)

**C1 · implementer, sonnet.** Rebuild the four levels from the blocks, update the wiring per the criteria, re-run it twice (idempotence), update the tests, run EditMode. Report in `reports/m2-trail-levels-c1.md` (`templates/report.md`), listing every file changed and proposed commits.

**C2 · text, after THJ picks.** Trailhead start: the rematch line (THJ's pick pending, `trail-tally-rematch-line`) and the "stays home" line; the Pile's relief line is in from C1 as a working line (D-504) and is revisited at the line pass. `miso-narrative` drafts, THJ approves, then a small wiring update (implementer).

## Risks

- Rebuild wipes wiring: always rebuild → wire, never hand-edit (D-405's prefab-is-master doesn't apply here: no hand edits exist).
- Revealed units and `allEnemiesStartAlert`: the tracker registers late units under the all-alert rule (`EnemyAlertTracker.cs:80,131`); confirm in play.
- Stage timing: the reveal must run in stage 1's onComplete so stage 2 starts with the units live.
- `AIRegressionTest` may shift: stays known red, never re-baselined.
- Statics: none new expected; if any, `PlayModeStaticReset` hook.
- Unity editor: the implementer works in THJ's open editor (menus, MCP); THJ stays out of Play meanwhile.
- Line endings/BOM kept per file.

## Gates

Compile clean / EditMode (known red only) / `miso-reviewer` (editor code + tests) / THJ play check: Trailhead → each route → Pile, a win played through (M2 win path; check FTP full, Duo hidden, alert, Pile reveal on the search tile) / docs above.

---

## C3 · The challenge rebuild (D-511)

Status: approved by THJ 2026-11-11 (D-505 to D-511); in progress.
Design: `plans/onboarding/2026-11-11-post-hearth-challenge-design.md` **revision 2** (blocks `m2-trailhead`, `m2-tracks`, `m2-blood`, `m2-pile`; the River and Ridge blocks are out of scope, chunk 4). Text: working lines from `reports/m2-trail-c3-lines.md` (`miso-narrative`), revisited at the line pass (D-504 precedent). Assigned: `miso-implementer` (sonnet). Base: `e3a45983b`.

### Acceptance criteria

All four levels:
- [ ] Rebuilt from the revision-2 blocks with the grid tool, then **Wire Search: Trail**; a second wiring run changes nothing.
- [ ] HP factors: Trailhead, Blood, Pile Claws ×1.0 (no override); Tracks Dark Claws ×0.8, Black Claw ×0.5. No other overrides.
- [ ] All enemies alert, revealed ones too; sisters' Duo locked; FTP full; no Pass-by/Items panels (unchanged from C1).
- [ ] Every "late arrival" is a hidden group revealed by a stage that completes at the **start of the family's turn 2** (before input): onComplete = input off → camera to the group → reveal → bark → camera back → input on. If `TurnReachedLOCondition` 2 completes at a different moment, use the closest existing way and report it; stop and report if it needs runtime code.

Per level:
- [ ] **Trailhead:** 12 × 2, rock 6,0; Lucy 3,1, Linda 4,1, slot 3,0; Claws 0,1, 1,0 (behind) and 8,1, 9,1 (ahead). Opening camera shows both pairs; the pick's bark ("Behind us!" working line) at the start, after the existing intro lines. Win = defeat all → mission map.
- [ ] **Follow the tracks ("the bell"):** 10 × 5, rocks 4,3 and 6,1; Linda 0,2, Lucy 1,2, slot 0,1; Black Claw (`Unit_BlackClaw`) 7,2; Dark Claws 5,2, 8,0; hidden `pack` 9,3, 9,1 revealed at turn 2 with camera + bark. The Black Claw's first-appearance close-up (EN-10, as built) shows with its intro line, and the pick's bark ("That big one leads them." working line) plays at the start. The old Archer/Encore stages are gone. Win = defeat all.
- [ ] **Follow the blood:** 20 × 5 per the block; Linda 0,1, Lucy 1,1, slot 0,0; Claws 4,2, 9,3, 9,0, 14,2; hidden `gullies` 4,4, 14,4 revealed at turn 2 with camera + bark. Objective line "Follow the blood. Two of you, to its end." Win group: `TilesOccupiedLOCondition`, player faction, `AggregationMode.AtLeast` 2 of 18,1 / 19,1 / 19,0 (the wiring's `Tiles()` helper gets an aggregation parameter) **or** every enemy dead, the second **hidden from the objectives panel**. If the panel can't hide one objective without runtime code, stop and report (don't build a workaround). Opening camera on the end tiles (`level camera 18,1`), then back. Reaching the end plays the clue close-up line, then the win. "Her blood." intro stays.
- [ ] **The Pile:** 11 × 6 per the block; Lucy 3,5, Linda 4,5, slot 5,4; pile props on 4,2–5,3; search = any Bergson on 3,3 or 6,3 → Lucy's "No white fur… she's not here." (D-504) → reveal `west` (1,4, 1,0) and `east` (9,3, 10,1); no Archer; Claws ×1.0. Outro unchanged.
- [ ] Reveal on an occupied tile: find what `HiddenLevelUnits.Reveal` does (skip / shift / fail) and report it; if it fails silently, make the wiring choose free reveal tiles only if the tool already supports that, otherwise report.
- [ ] `SearchTrailTests` updated to the new layouts and rules (positions, factors, hidden groups and turn-2 stages, Blood's AtLeast-2 objective and hidden fallback, Tracks' Black Claw, Pile without the Archer). Full EditMode suite: all pass except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

### Out

The River and the Ridge (chunk 4), Cyclone changes, runtime or core code (stop and report if needed), new UI, the rematch / "stays home" lines (C2), deleting old unreferenced assets (list them).

### Gates

Compile clean / EditMode (known red only) / `miso-reviewer` / coordinator reads the report / THJ's timed play of M2 with each pick, both routes (win path; to-check rows 3, 4, 5, 7, 8, 9 of the design are play checks) / docs: GDD `missions-structure.md` M2 rows, `level-chunks.md` knobs, 11-09 plan sections marked superseded (designer); narrative draft lines (narrative); build log (coordinator).

## C4 · Trail balance values (D-516, D-518)

C3 committed `9e9e0ca63` (2026-11-11).

Source: THJ's C3 play (`playtests/2026-11-11-trail-c3-play.md`), the balance design (`plans/2026-11-11-trail-balance-design.md`), decisions D-516 to D-518. Size S, data only, `sonnet`. Runs after the C3 fix round is committed. Chained Assault is untouched (D-517: THJ tunes it). Bloom and the sisters' Duo node (D-519, D-520) are a separate plan.

### Acceptance criteria

1. All four Trail blocks in `design/level-chunks.md` (owner: designer; coordinator routes the one-word change) read `level tier standard`; the four `GB_m2-*` prefabs are rebuilt from them and rewired (`Tools/Onboarding/Wire Search: Trail`, idempotent: second run, no diff). Prefab `enemyTier` = Standard on all four.
2. Follow the tracks: the two Claws and the turn-2 pair have no HP override (16 HP at Standard); the Black Claw's HP factor is 0.75 (30 HP). No other level has an HP override.
3. `Lucy_Cyclone_Effect_AttrMod` damage factor 7 → 3. Cooldown unchanged (2). The dead Linda-folder copy and the orphaned `PassByEffect_AttrMod` are not touched.
4. `SearchTrailTests` asserts literals: tier Standard on all four levels; Tracks overrides (none on Claws, 0.75 on the Black Claw); the Cyclone asset's factor 3.
5. EditMode suite: all pass except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (it may move with the Cyclone data; never re-baselined).
6. THJ plays the Trail both picks (play-test before commit).

### Commits

One for the Trail data (blocks-built prefabs, wiring, tests); the Cyclone value in its own commit (global, revertable alone).
