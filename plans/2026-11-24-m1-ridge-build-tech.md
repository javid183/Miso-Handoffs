# M1 "The Ridge" redesign: build

Size: M    Tier: 2 (inside an approved design; no core code)    Assigned to: miso-implementer (opus)
Branch: thj/onboarding-demo
Status: approved (THJ's go, 2026-11-24)

## Why

THJ played M1 and didn't like it: the Masher was stuck on its tiles (`playtests/2026-11-23-m1-play-check.md`). The redesign `plans/2026-11-24-m1-ridge-redesign.md` is approved: D-648 to D-653, all decided by THJ. This plan builds it.

## Goal

M1 plays THJ's beats 1 to 8 and the plateau ending "Together or apart" on THJ's own `GB_m1-ridge`, with fallbacks for the two cues that will need code later.

## Acceptance criteria

The design's criteria (redesign plan, "Acceptance criteria"), made checkable:

- [ ] `GB_m1-ridge` matches block `m1-ridge-2` (redesign plan §7) when read back with `level_to_grid.py` (block = prefab + (1,5)). THJ's art, the clue prop and `alertRangeBonus` -1 are unchanged.
- [ ] Tile 5,-5 exists. Linda starts on 5,-5 and Mark on 6,-5. The Masher and the Claws on 2,2 and 5,2 are gone. The plateau has Claws on 1,4, 3,4 and 5,4 (factor 0.7, visible). The pocket Claws 5,-2 and 5,-1 (0.7) and 7,-2 (0.45) are in hidden group `fall`.
- [ ] A neutral, unmovable rock unit with no abilities sits in hidden group `rock` on 5,-5. Once revealed it blocks walking, shows no HP bar or hover clutter, isn't counted by "defeat all enemies", and isn't targeted by enemies.
- [ ] Intro (D-652): arrival lines and camera on the clue; Linda walks to 3,-2 (`MoveUnitSequence`); camera shake (`CFXSequence` + `ShakeCameraEffect`, `durationOverride` -1); `rock` and `fall` are revealed; the Watch page (`TutorialSequence`) plays last.
- [ ] Turn order is Enemy, Bergsons, Neutral.
- [ ] Mark's `MarkPassiveAbility_ContinuousAttack` is off from level start until S3 completes, then back on (D-649). FP stays full: no FP 2 filler.
- [ ] Linda's bar and Mark's Command are locked (`LevelAbilityLock`) until S2 completes. Watch still fires while her bar is locked.
- [ ] Stages S1 to S4 are as in redesign plan §5 "Systems". S2 also completes on its `TurnReached` fallback (aggregation any). S3 tops FTP back up to full through a second `LevelStartFPFiller`, which isn't wired to `levelStarted`.
- [ ] Fallback cues (D-653): the S3 lines react to Catch & Return, and an `HPBelowPercent` bark at 50% nudges the potion.
- [ ] `MS2 - The Ridge.asset` `initialItemsAvailability` holds `Bergsons_Ability_HealthPotion` × 1. Its other fields are unchanged.
- [ ] Every line and page uses the text from `design/m1-ridge-redesign-text.md` (`miso-narrative`), marked as placeholder the same way 3.1b did (until THJ approves the text).
- [ ] `M1RidgeTests` is rewritten to match (layout, groups, factors, turn order, locks, switch, stages, potion). The rock's Neutral faction and its exclusion from "defeat all" are covered by an edit-mode test.
- [ ] No softlock: every stage that waits on the player also completes on a turn fallback, or is reached anyway.

## Scope

In: THJ's prefab edits, the rock prefab variant, `MissionWiring.Ridge.cs` rewritten, the `Resources/Sequences/M1Ridge/` sequences, the mission's potion, `M1RidgeTests`, the narrative's text pasted in.
Out:
- The trigger component for Catch & Return, low HP and "ability used" (D-653: its own plan, after M1).
- The Watch page on the first prompt (D-652: not wanted).
- Final art for the rock.
- Lucy's memory level (`GB_m2-lucy` and its wiring: still hands-off, D-643).
- M2 to M4.
- Any core-systems code.

## Touches

Systems:
- Level prefab and wiring: `Features/Onboarding/Editor/MissionWiring.Ridge.cs`, `Content/Levels/Greybox/GB_m1-ridge.prefab`.
- Sequences: `Resources/Sequences/M1Ridge/`.
- Hidden groups: `HiddenLevelUnits`, `RevealUnitsSequence`.
- `LevelAbilityLock`, `SignalSequence`/`SignalAction`, `LevelStartFPFiller`, `TutorialSequence`.
- Bark graph (`HPBelowPercent`).
- Mission data `MS2 - The Ridge.asset`. Data only: `Mission.cs` (core) is not edited.
- New rock unit prefab variant, modelled on `Features/NPCs/Deer/Prefabs/Deer.prefab`.

USPs: Family Roles (Watch, Counter), Synergies (Catch & Return).

Docs: listed under Gates.

## Approach

Two chunks, run one after the other by one implementer. The riskiest parts come first (the rock in a hidden group, the reveals inside the intro).

### Chunk 4.1a: level and rock (data)

- Apply the change list in redesign plan §7 "Source" to THJ's committed `GB_m1-ridge` (`f20f9a5ab`): add tile 5,-5, move the units, remove the Masher and the two Claws, set the factors, and set up hidden groups `fall` and `rock`. Remove the old `back` group and 3.1b's stages.
  - Use an editor script, or `GridToLevelBuilder`'s helpers on the existing prefab. Hand-edit YAML only for single fields.
  - **Don't** rebuild from the block (D-651).
- Create the rock: a prefab variant like the Deer, in the Neutral faction, Unmovable, with no abilities and no HP bar or hover. Place it in group `rock` on 5,-5.
  - First check that a neutral unit works inside `HiddenLevelUnits`. If it doesn't, stop and report; don't change core code.
- Add the potion to `MS2 - The Ridge.asset`.
- Tests: the layout and groups (match the block), the rock's faction and its exclusion from "defeat all", and the potion.
- Read back with `level_to_grid.py` and compare with block `m1-ridge-2`.
- Model: opus. Review: with the feature.

### Chunk 4.1b: wiring, sequences and text

- Rewrite `MissionWiring.Ridge.cs`: turn order; stages S1 to S4 with their sequences; the two ability locks and their unlock; the Continuous Attack switch off and on (`SignalSequence` → `SignalAction` on the component's `enabled`); the second FTP filler at S3; the intro sequence (beats 1, 2 and 4); the outro on the clue (3.1b's `M1Ridge_End_*`); the low-HP bark. Keep the wiring idempotent, like 3.1b's.
- Use the text in `design/m1-ridge-redesign-text.md`. If a line is missing, use a marked placeholder and list it.
- Remove 3.1b's sequences that are no longer used. List them in the report; don't leave orphans.
- Rewrite `M1RidgeTests`. Run `SearchRidgeTests` too, because it covers Catch & Return being open by default.
- Model: opus. Review: one `miso-reviewer` pass over 4.1a and 4.1b together.

### To check during the build (from the design's risk list; report each one)

- `TurnReached` 1 completes at the first family turn when the enemies go first (T-14). If it doesn't, move S1's sequence into S2.
- Reveals inside the intro happen before turn 1, and the revealed Claws act on enemy turn 1.
- The Mark placed in the level is the one the mission plays, so the switch hits the right component.
- Watch fires while Linda's bar is locked.

## Risks

- **Statics:** none expected. If any are added, they need a `PlayModeStaticReset` hook.
- **AI:**
  - The AI reads the rock as a unit; check it isn't a target.
  - The new unit prefab may move the AI regression test. Run `AIRegressionTest.Baseline_MatchesCurrentAI` by name and compare with the last count, **44** (D-644). Don't re-baseline it.
- **Serialized renames:** none.
- **Save data:** no shape change. The potion is mission start data, and play checks start from a cleared save (D-636).
- **Assets:** prefab edits go through an editor script or the builder's helpers. Show the scene/prefab diff stat in the report.
- **Event subscriptions:** sequences use the existing players. Ability locks and the switch are undone by their unlock steps. Check that a restart mid-level doesn't leave Continuous Attack off (level restart reloads the prefab: confirm).
- **Other branches:** none. Onboarding-only; `main` gets it when THJ merges.

## Gates

- Compile: clean console (verifier).
- Tests:
  - `M1RidgeTests` and `SearchRidgeTests` after each chunk.
  - The full EditMode suite after 4.1b.
  - The AI regression test by name, compared with 44.
- Review: one `miso-reviewer` pass over 4.1a and 4.1b together (nothing core).
- Gate 7: the implementer reads the built prefab back with `level_to_grid.py`; the coordinator renders it and compares with `m1-ridge-2`.
- Play check: yes, THJ's time. A full M1 run to a win, from a cleared save (the "How to see it" list goes in the report).
- Docs to update after the play check:
  - GDD `missions-structure.md` M1 row; `plans/2026-11-22-onboarding-d3-paper-levels.md` (`m1-ridge` superseded); `design/level-chunks.md` (chunk "torn apart, one line"). Owner: `miso-game-designer`.
  - `glossary.md`, if text is approved. Owner: `miso-narrative`.
  - `status.md`, `build-log.md`, `tech/onboarding-merge.md`. Owner: coordinator.

## Commits (after THJ's play check)

1. `feat(onboarding): rebuild The Ridge around the rockfall split and the plateau` (prefab, rock variant + `.meta`, mission asset, 4.1a tests)
2. `feat(onboarding): wire The Ridge's new beats, locks and cues` (wiring, sequences + `.meta`, `M1RidgeTests`)
