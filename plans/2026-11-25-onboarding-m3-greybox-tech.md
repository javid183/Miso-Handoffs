# M3 "Hold the yard": greybox build

Size: L    Tier: 2 (inside an approved design; no core code), one Tier 3 question (6.3)    Assigned to: miso-implementer (6.1 opus, 6.2 and 6.4 sonnet)
Branch: thj/onboarding-demo
Status: draft (coordinator, 2026-11-25); runs after M4 (D-691), on THJ's go

## Why

THJ approved M3 with the Masher in the yard (D-688) and asked for a greybox first, necks open, no barriers (D-689). Design: `plans/2026-11-22-onboarding-d3-paper-levels.md` §"M3 · Defence" (block `m3-defence`, gate 7 checked 2026-11-25) and its "Greybox first" section. Rules: the stone moves while the pusher stands at it (D-608), the pusher is whoever is picked (D-622), "Still counting?" plays at the end (D-624), the Heavenly Sword pickup on 8,6 (D-625). Code facts: `reports/onboarding-m3-m4-code-checks.md` (T-8, T-9, T-10, T-14, T-15, Masher, Cleanse).

## Goal

The M3 mission (`M2 - The Trail`) plays the new `GB_m3-defence` as its only level: clear the yard (Masher + two Claws), the pick pushes the stone for three turns while the sisters hold three waves, finish them, the tally fades, Toba appears.

## Acceptance criteria

**6.1 · Level, stone and stages**
- [ ] New `Content/Levels/Greybox/GB_m3-defence.prefab` built from block `m3-defence` with the grid-to-level tool; `level_to_grid.py` read-back matches the block. Necks 2,3 and 8,3 are plain floor (D-689). 1,3 and 9,3 are no-tile gaps.
- [ ] Squad: Linda 4,4, Lucy 6,4, `Unit_Placeholder` on 5,4. Early tier, all alert, family first.
- [ ] Opening: Masher anchor 3,6 (factor 0.45), Dark Claws 7,7 and 5,6 (0.8). Hidden groups: `w1` Claws 0,0, 1,0; `w2` Claws 10,0, 9,0, 10,1; `w3` Claws 0,2, 10,2 (all 0.8, come in alert). Mushrooms on 1,1 and 9,1.
- [ ] The stone: variants of `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab` titled "Stone" (placeholder), one per notch (start + 3 notches), each its own hidden group; the start stone visible on 5,8; each notch = `HideUnitsSequence` (current) + `RevealUnitsSequence` (next). Toba in hidden group `toba` on 5,8, revealed after the last stone hides. In-level faction relation Enemy–Neutral = Ally (as M1), so Claws ignore the stone.
- [ ] Heavenly Sword pickup (`DR_PickUp_HeavenlySword.prefab`) under cell 8,6 at local zero.
- [ ] Cleanse locked for every unit (`LevelAbilityLock`, unit prefabs, pattern `HearthMemoryWiring.Rules.LockCleanse`). Linda–Lucy Duo locked (D-470, pattern from M2). FP filled at start (`LevelStartFPFiller`).
- [ ] Two new feature-side objective conditions in `Features/Onboarding/` (no Core file changed), each with EditMode tests:
  - **Pick on tiles:** a Bergson that isn't a fixed roster unit (the squad's free pick) stands on the given tiles. Fixed units read from the mission roster, not hard-coded names, if that's cheap; otherwise "not Linda or Lucy" with a comment.
  - **Pick held the tiles:** counts family turn starts at which the pick stood on the tiles since the stage began; completes at the family turn start where the count reaches N (N = 1). A turn start with the pick off the tile doesn't count, so the stone waits while he's away (D-608 exactly; the built `TurnReached` would complete mid-turn when he steps back on).
- [ ] Stages: **S1** "Clear the yard." (the opening three dead) → sequence: the pick's line + camera on the stone. **S2** "{Pick}: push the stone." (pick on 5,7) → reveal `w1`, line, camera (the Trail's arrival pattern). **S3a/b/c** "Hold them off (1/3)…(3/3)" (pick held 5,7 at one turn start) → notch, reveal `w2` after S3a and `w3` after S3b; after S3c the last stone hides. **S4** "Finish them." (defeat all) → end sequence: tally fade (`SistersTally_FadeOut`, moved from the Pile; Linda "Still counting?" · Lucy "…No."), camera on the cave, reveal `toba` (non-hostile), his lines, fade home. Placeholders for lines until 6.4.
- [ ] Masher close-up: comes from `EnemyIntroductionController` on first sight (name only); nothing to build. Report whether a fresh demo save has seen "Masher" before M3 (it shouldn't: M1 no longer has one).
- [ ] Wiring menu `Tools/Onboarding/Hold the Yard: Apply Wiring`, idempotent, partial files in `Features/Onboarding/Editor/` (pattern `MissionWiring.Circles*.cs`); tests `M3DefenceTests` (layout, groups, factors, stone variants and groups, relations, pickup cell, locks, stages).

**6.2 · Mission and the old Trail**
- [ ] `M2 - The Trail.asset`'s graph is one node, `GB_m3-defence`. Everything keyed to the mission stays (the Yard as completion sequence, Map Table clue scene, Home state, the tally, station unlocks after M3, Toba's unlock from 5.2).
- [ ] The four `GB_m2-*` Trail prefabs are renamed with `AssetDatabase.MoveAsset` (suffix `_legacy`, D-621; guids kept) and leave the graph. `SearchWiring.Trail` and `SearchTrailTests` follow the new paths and still pass, but the wiring menu no longer wires a level the mission plays (comment why).
- [ ] `SistersTally_FadeOut` plays at M3's end, not at the Pile; the Pile file is unchanged otherwise.
- [ ] `OnboardingMissionGraphTests`, Home tests that read the Trail mission, and the tally tests pass.

**6.3 · Tally credit for mushroom kills (only if THJ says yes)**
- [ ] When a sister's ability sets off an exploding mushroom, enemies the blast kills count for her (`SistersTallyListener`, a window like the Bloom window; feature-side, not core). Tests for: arrow-set blast kill counts for Linda; ember-set for Lucy; an enemy-set or ownerless blast counts for no one.

**6.4 · Lines**
- [ ] The M3 lines from `design/m3-text.md` (`miso-narrative`) replace the placeholders; covering tests; full EditMode suite.

## Scope

In: the new level, stone variants, two feature-side conditions, wiring and tests, the mission graph, the Trail renames, the tally fade move, Cleanse/Duo locks, lines; 6.3 if THJ says yes.
Out: barriers (chunk 3.0, decided after THJ plays, D-689); the "no AP while pushing" lever; final art and stone animation; any core code; M4.

## Touches

Systems: grid-to-level builder; `HiddenLevelUnits`, `RevealUnitsSequence`, `HideUnitsSequence`; objective conditions (new feature-side ones; `LevelObjectiveConditions.cs` and `AIStrategyPlanner` unchanged: the new types fall into the planner's skip, D-686); `LevelAbilityLock`; `SistersTallyListener` (6.3); mission data (`Mission.cs` core, data only); `EnemyIntroductionController` (read only).
USPs: Family Roles (the pusher's own Role while anchored), Synergies (Cyclone into the mushroom blast, Shield/Catch on whatever closes), Home (station unlocks and Toba after M3, unchanged keys).
Docs: under Gates.

## Approach

6.1 (opus, riskiest: stone swap, the held-tile condition, stage timing) → 6.2 (sonnet) → 6.3 (sonnet, only on THJ's yes) → 6.4 (sonnet, after the text). `miso-narrative` writes `design/m3-text.md` alongside. One review over all chunks; full suite after the last; THJ plays M3 to Toba from a cleared save, then decides on barriers.

### To check during the build (report each)
- A notch's Hide + Reveal on the same cell runs without the reveal landing on a neighbour (hide first, then reveal).
- The pick-held condition completes at the family turn start (family first: the turn number ticks at the family turn start, `CombatLevelRunHandler.cs:505-535`) and the wave reveal lands before input.
- Shots across 1,3 / 9,3 (T-15): Linda's bow from 1,4 to 1,1, Lucy's ember the same; code says yes, confirm in the play check.
- The AI planner turns a `TilesOccupied` objective into intents; the new conditions are skipped (no handler), so enemies aren't drawn to 5,7 by the objective. Report if that changes how the waves move compared with the paper.

## Risks

- **Statics:** the held-tile condition keeps per-stage state on the condition instance, not in a static; any static needs a `PlayModeStaticReset` hook.
- **AI:** new condition types are outside the planner's list (skip, D-686); the AI regression test by name after 6.1, compared with **46** (D-687; a new rock variant may add a line, as `Unit_Rock` did, D-673; explain any change, don't re-baseline).
- **Serialized renames:** none in code; the prefab renames keep guids.
- **Save data:** no shape change.
- **Assets:** prefabs and mission data through editor scripts; prefab diff stats in the report.
- **Other branches:** none; `tech/onboarding-merge.md` M3 rows.

## Gates

- Compile clean; `M3DefenceTests` + the condition tests after 6.1; Trail/graph/Home/tally tests after 6.2; full EditMode suite after the last chunk; AI regression by name (46).
- One `miso-reviewer` pass over all chunks (nothing core).
- Gate 7: read-back of `GB_m3-defence` vs `m3-defence` (coordinator renders).
- Play check (THJ): M3 from a cleared save to Toba; then the barriers decision.
- Docs after the play check: GDD `missions-structure.md` M3 rows, `enemies.md` (Masher's first appearance), `design/level-chunks.md` ("the anchor" knob) (`miso-game-designer`); glossary (`miso-narrative`); `status.md`, `build-log.md`, `tech/onboarding-merge.md`, `tech/classic-fallback.md` (coordinator).

## Commits (after THJ's play check; proposed)

1. `feat(onboarding): objective conditions for the squad pick on a tile` (the two conditions + tests)
2. `feat(onboarding): M3 becomes Hold the yard` (prefab, stone variants, wiring, `M3DefenceTests`)
3. `feat(onboarding): the Trail's levels leave the mission and keep their files` (mission asset, renames, Trail wiring/tests, tally fade move)
4. `feat(sisters-tally): mushroom blast kills count for the sister who set it off` (6.3, if built)
5. `feat(onboarding): M3 lines`
