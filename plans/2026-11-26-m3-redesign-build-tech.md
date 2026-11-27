# M3 "Hold the yard" round two: build

Size: L    Tier: 2 (inside the approved design; no core code)    Assigned to: miso-implementer (7.1 opus, 7.2 sonnet)
Branch: all (THJ is on `main`, D-723)
Status: waiting on THJ's go

## Why

THJ played the M3 greybox (D-722, `playtests/2026-11-25-m3-play-check.md`) and approved the redesign `plans/2026-11-26-m3-redesign.md` (block `m3-defence-3`, gate 7 checked 2026-11-26) with these answers:
- D-724: the squad is **Linda and Lucy only**. No John and no pick slot.
- D-725: Mark is held from level start. The stone moves a notch at each family turn start for 4 turns. The level is lost if Mark falls.
- D-726: six barricades, data only (option A).
- D-727: the Masher in the east lane, as proposed.
- D-728: waves as proposed. THJ tunes them in play.
- D-729: barricades are hand-placed by the wiring, with no grid character.

Code facts: `reports/2026-11-26-m3-barrier-code-read.md`.

## Goal

The M3 mission (`M2 - The Trail`) plays the redesigned level. Linda and Lucy hold two 3-wide necks closed by barricades for 4 turns. Mark, held on the stone, is the target. The Masher comes up the east lane. Then they finish the enemies, the tally fades, and Toba appears.

## Acceptance criteria

**7.1 · Level, barricades, Mark, stone, stages, roster (opus)**

*Prefabs*
- [ ] The old `Content/Levels/Greybox/GB_m3-defence.prefab` is renamed `GB_m3-defence_v1.prefab` with `AssetDatabase.MoveAsset`, so its guid is kept (D-621 pattern).
- [ ] A new `GB_m3-defence.prefab` is built from block `m3-defence-3` with the grid-to-level tool, with these changes from the drawn block:
  - **No John:** 4,10 is plain floor (D-724).
  - **w3's east Claw goes on 8,2**, not stacked on 8,0 (T-M12 avoided).
- [ ] The `level_to_grid.py` read-back of the new prefab matches the block, apart from those two changes and the hand-placed units listed below.
- [ ] The mission graph of `M2 - The Trail.asset` points to the new prefab. Everything keyed to the mission still works: the Yard completion sequence, the Map Table clue, the Home state, the station unlocks, Toba's button.

*Roster*
- [ ] In `M2 - The Trail.asset`, `missionRoster.freeSlotsCount` is 0. The fixed slots stay Linda and Lucy.
- [ ] The `Unit_Placeholder` deploy slot is gone from the level.
- [ ] Linda starts on 2,8 and Lucy on 7,8.
- [ ] Anything tied to the old pick is removed from this level's wiring: `PickOnTilesLOCondition`, `PickHeldTilesLOCondition`, `PickFallenLOCondition`, and the `{pick_0}` text. The condition classes themselves stay, since other code and tests may use them; a grep says so.

*Mark*
- [ ] `Unit_Mark` is placed in the level on 4,11, in the Bergsons faction, and is not a roster seat.
- [ ] Mark has the persistent tags `EntityState.Unmovable` and `EntityState.Unable to Swap` for this level, set on the instance, not on his prefab.
- [ ] Mark is held all level by `HoldUnitsUntilSignal`, through a new serialized option `holdFromLevelStart`:
  - When on, `Hold()` runs at the first turn start (or in `Start`, whichever comes first and is safe).
  - Nothing releases it.
  - When off, the component behaves exactly as today (M1 unchanged).
  - EditMode tests cover the option's state logic, and the existing `HoldUnitsUntilSignalTests` still pass.
- [ ] Report on T-M1, from reading the code; THJ's play confirms it:
  - whether Mark's Family Role (Counter) is off while he carries `Status.Inactive`;
  - whether enemies target him;
  - whether the next-targets display shows him;
  - whether pushes, pulls and Cyclone knocks leave him on 4,11.
  If his Role would still fire, say how to switch it off for this level (for example a `LevelAbilityLock` on the role, or the role's own tag gate). Stop and report if that needs core code.
- [ ] T-M3: placing a hero outside the roster in a roster mission has no side effects (XP, Bond, the tally, the party panel, the FP filler). Report what you find. The FP filler lists Linda and Lucy only.
- [ ] T-M4: does the AI planner read the family's defeat group (Mark destroyed) as an intent? Report yes or no. If yes, every enemy may head for Mark: report it, don't change it.

*Barricades*
- [ ] A new `Unit_Barricade.prefab`, a variant of `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`, next to it in `Features/NPCs/Rock/Prefabs/`:
  - title "Barricade" (placeholder), Neutral, Unmovable, Unable to Swap, no abilities;
  - HP that comes out at **8** in this level (set per instance through the health-factor route the level already uses, or on the prefab; say which);
  - the unit HP bar shows.
- [ ] Six barricades are placed on 0,6, 1,6, 2,6, 6,6, 7,6 and 8,6.
- [ ] The level's faction relations:
  - **Enemy–Neutral goes back to Enemy** (the `LevelBase` default), so goblins can't pass barricades and attack them.
  - **Bergsons–Neutral stays Ally**, so the family walks through but can't stop on them.
  - `MakeEnemyAndNeutralAllies` is removed from this wiring.
- [ ] Report on requirement 3 of the design (`plans/2026-11-26-m3-redesign.md` §"Barrier requirements"), from reading the code: no family ability, Duo, Role, the Heavenly Sword or Lucy's Whirl damages a Neutral unit. List any effect that hits all factions (the mushroom blast is fine either way).
- [ ] T-M6: the damage rounding at Early. Report what a Claw hit and a Masher slam deal to an 8 HP barricade.

*The stone and Toba*
- [ ] The stone moves to 4,12. It needs **five** stone variants (start plus 4 notches), so add `Unit_Rock_Stone4`.
- [ ] Toba is hidden in group `toba` on 4,12.
- [ ] **The stone is no longer Neutral**, so the now-hostile Enemy–Neutral relation doesn't make it a target. Move the stone variants to a faction allied with Enemy that has the relation entries `GetFactionEnemies` needs: Stranger is the first candidate (Ally with Bergsons, Enemy and Neutral in `LevelBase`; check whether a Stranger unit present at start creates a controller and needs an "enemies" map key, the Ridge lesson). Change the faction on the level instances or on the variants, whichever leaves M1's `Unit_Rock` untouched. Report what you chose and why.
- [ ] A test proves Enemy–Stranger (or the chosen faction) is Ally and Enemy–Neutral is Enemy in the level.

*Enemies and objects*
- [ ] The Masher is placed at anchor 6,1, factor 0.6.
- [ ] Waves, all Dark Claws at factor 1.0 that come in alert:
  - `w1` on 0,1, 1,1 and 2,1, **in play at start**, not hidden;
  - hidden `w2` on 8,0 and 8,1;
  - hidden `w3` on 0,0, 2,0 and 8,2.
- [ ] Mushrooms on 1,4 and 8,4. The Heavenly Sword pickup under 8,10. Early tier, all alert, FP full at start.
- [ ] Turn order: Bergsons, Enemy, Neutral, plus the stone's faction if it needs a seat.
- [ ] The camera starts on 4,6.
- [ ] Cleanse and the Linda–Lucy Duo stay locked as built.

*Stages and defeat*
- [ ] **S1 to S4**, objectives "Hold them off (4)", "(3)", "(2)", "(1)" (placeholder countdown text, narrative later). Each stage completes at the next family turn start:
  - Use the built `TurnReachedLOCondition` with turns 2, 3, 4 and 5 (family acts first, so the turn number ticks at the family turn start).
  - If that completes at the wrong moment, use a small feature-side "family turn starts since the stage began" condition instead, following `PickHeldTilesLOCondition`'s counting. Report which one you used.
- [ ] What each stage end does:
  - S1 end: notch 1, then the `w2` arrival.
  - S2 end: notch 2, then the `w3` arrival.
  - S3 end: notch 3.
  - S4 end: notch 4 and the stone rolls away (the last variant hides).
  - Each arrival uses the existing arrival pattern: input off, camera, reveal, bark, camera back, input on.
- [ ] **S5** "Finish them.": living Enemy units ≤ 0. It completes with barricades standing, because they are Neutral. Its end sequence is as built: the tally fade, "Still counting?", the reveal of Toba (non-hostile), and the fade home.
- [ ] Defeat:
  - The level's template group (no playable Bergson standing) stays.
  - A second group is lost when **Mark is destroyed** (`EntitiesDestroyedLOCondition` on Mark), from level start.
  - The pick-fallen group is removed.
  - The aggregation is Any, as built.
- [ ] Level-start cues: camera over the Masher, then the east wall, then Mark at the stone with his line (placeholder). There's no John line.

*Lines and code rules*
- [ ] Lines are placeholders. Keep the existing ones where they still fit, and drop John's. Text is chunk 7.2.
- [ ] The wiring menu `Tools/Onboarding/Hold the Yard: Build Level` / `Apply Wiring` rebuilds and re-wires the new level and is idempotent. Keep the partial files (`MissionWiring.HoldTheYard*.cs`), and update the class comment and the `BlockDocument` string to the new block. If a file gets too big, put the new parts (barricades, Mark) in new partial files.
- [ ] `M3DefenceTests` is rewritten for the new level. It covers:
  - layout and gaps;
  - barricade tiles, faction, HP and tags;
  - Mark's tile, tags, hold option and absence from the roster;
  - the roster (2 fixed seats, 0 free);
  - wave groups, tiles and factors; the Masher's anchor and factor;
  - the stone variants, groups and faction; the relations;
  - the mushroom and pickup cells; the locks;
  - the stages and the defeat groups.
- [ ] No private IDs in code, comments, test names or log text. No Core file is changed: list any you think you need and stop.

**7.2 · Lines (sonnet, after the text is approved)**
- [ ] `miso-narrative` updates `design/m3-text.md` for the sisters-only squad, Mark's lines on the stone, the countdown objective and the Masher handover. THJ approves the text. The lines then replace the placeholders, with covering tests.

## Scope

In: the new prefab and the old one's rename, the barricade prefab, the fifth stone variant, the hold-from-start option, wiring and tests, the mission roster and graph.
Out:
- the core AI barrier rule (option C, only on the play trigger, D-726);
- any Masher code (D-727);
- a grid-tool barricade character (D-729);
- final text (7.2), art, the stone animation;
- the levers in the design's playtest-signals table (THJ tunes after play).

## Touches

Systems:
- grid-to-level builder;
- `HoldUnitsUntilSignal` (feature);
- `HiddenLevelUnits`, `RevealUnitsSequence`, `HideUnitsSequence`;
- objective conditions (built ones);
- `LevelFactionRelations` (core, **data only**), mission data (`Mission.cs` core, **data only**);
- unit prefabs (a new rock variant).
No core code.

USPs:
- Family Roles: Linda's Watch on the west front. Mark's Role must be off.
- Synergies: Cyclone into the mushroom blast, and Sister's Rivalry with the tally.
- Home: unchanged keys after M3.

Docs: under Gates.

## Approach

7.1 runs as one implementer run (opus), because the pieces only work together. It has a fixed order inside the run:
1. the hold option and its tests;
2. the barricade prefab and the stone faction;
3. the level build and wiring;
4. the tests.

Then the covering tests, one `miso-reviewer` pass (nothing core, so with the feature), the full suite, and the AI regression test by name. THJ plays M3 from a cleared save. 7.2 follows once the text is approved. `miso-narrative` can draft `m3-text.md` in parallel with 7.1.

## Risks

- **Statics:** the new hold option keeps state on the component instance. Any new static needs a `PlayModeStaticReset` hook.
- **AI regression:**
  - Run `AIRegressionTest.Baseline_MatchesCurrentAI` by name after 7.1 and compare with **50** (D-715).
  - `Unit_Barricade` and `Unit_Rock_Stone4` are new `GUnit` prefabs outside `Content/Levels/`, so expect about +2 "unexpected unit" lines, like the stone variants in D-715.
  - Explain every change. Don't re-baseline.
- **Faction relations:** a unit whose faction has no "enemies" map entry throws `KeyNotFoundException` (the Ridge lesson). The stone's new faction and the Neutral barricades both need checking at level start in Play. The verifier's console check covers it.
- **Option A's pull:** barricades attract enemies even when a gap is open. That is accepted for the greybox (D-726).
- **Serialized fields:** the new `holdFromLevelStart` field defaults to false, so M1 is unchanged. No renames.
- **Save data:** no shape change.
- **Assets:** prefabs and mission data change through editor scripts. Put the prefab diff stats in the report.
- **Reveal onto a taken cell** (w3's 8,2 if a w2 Claw still stands there): cosmetic. Report what the reveal does.

## Gates

- Compile clean. `M3DefenceTests`, `HoldUnitsUntilSignalTests`, the mission-graph and Home tests that read the Trail, and the tally tests pass. The full EditMode suite runs after 7.1. The AI regression runs by name (50 → explain).
- One `miso-reviewer` pass over 7.1.
- Gate 7: read-back of the new prefab against `m3-defence-3`, done by the coordinator.
- Play check (THJ, from a cleared save, to Toba):
  - Mark is untouchable by the player and hittable by enemies, and his Role doesn't fire;
  - Claws break barricades;
  - the Masher's walk;
  - the stone's countdown;
  - the playtest-signals table in the design plan.
- Docs after the play check:
  - `miso-game-designer`: d3 paper levels §M3 (supersede `m3-defence`), GDD `missions-structure.md` M3 row, `level-chunks.md` (the barricade as a knob), GDD enemies (Masher in the lane);
  - `miso-narrative`: glossary ("Barricade");
  - coordinator: `status.md`, `build-log.md`, `tech/onboarding-merge.md`, `tech/core-systems.md` (none expected).

## Commits (after THJ's play check; proposed)

1. `feat(onboarding): a held unit can be held from level start` (the hold option + tests)
2. `feat(onboarding): Hold the yard round two: barricades, Mark on the stone, the Masher in the east lane` (prefabs, barricade and stone variants, mission roster and graph, wiring, `M3DefenceTests`)
3. `feat(onboarding): M3 lines` (7.2)
