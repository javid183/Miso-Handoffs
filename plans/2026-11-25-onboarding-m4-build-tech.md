# M4 "The White Mothers": build (The circles, Mithra's Rest, the Queen)

Size: L    Tier: 2 (inside an approved design, D-690; no core code)    Assigned to: miso-implementer (5.1 opus, 5.2 and 5.3 sonnet)
Branch: thj/onboarding-demo
Status: draft (coordinator, 2026-11-25); dispatch on THJ's go

## Why

THJ approved M4's paper levels as written (D-690): `plans/2026-11-22-onboarding-d3-paper-levels.md` §"M4 · three levels" (from line 466). The rules it rests on: the Queen is the boss, Toba + Linda + Lucy fixed + 1 pick, no duel (D-613); Mithra's Rest = heal + relic (D-612), 50% HP and FTP filled (D-626); Cleanse only in M4-1 (D-614); the sisters' first Duo is planned in M4-1 (D-470). Code facts: `reports/onboarding-m3-m4-code-checks.md` (T-11, T-12, Cleanse).

## Goal

The M4 mission plays `GB_m4-cleanse` → Mithra's Rest → `Level3-C1` with Toba, Linda, Lucy and the picked John or Mark, as the paper levels describe.

## Acceptance criteria

**5.1 · M4-1 The circles (`GB_m4-cleanse`)**
- [ ] New prefab `Content/Levels/Greybox/GB_m4-cleanse.prefab` built from block `m4-cleanse` with the grid-to-level tool (`tech/level-tools.md`); read back with `tools/level_to_grid.py`, it matches the block (terrain, units, pools, deploy slot 1,4). Nothing existing is overwritten (D-621).
- [ ] Squad: Linda 0,4, Lucy 0,3, Toba 1,3 placed; one `Unit_Placeholder` on 1,4 for the pick.
- [ ] Enemies at Standard tier, no overrides: Dark Claws 7,4, 8,5, 8,3, 6,7, 6,1; Dark Shaman 9,4; Corruption pools 5,7, 11,5, 5,1, each spawning a Claw about every 4th turn with at most one alive per pool (use the existing pool/spawner settings from `Level2-C1-TArtEx`; report the values used). 8,4 is empty.
- [ ] All alert; family first.
- [ ] One stage, two objectives together: "Cleanse the circles." (all three pools destroyed) and "Defeat the dark claws." (defeat all). Default loss.
- [ ] Cleanse is usable here (no `LevelAbilityLock` entry for it). The Cleanse button pulses once (`GuidedAbilityHint`, WhenUnlocked). Toba's level-start line plays (placeholder until 5.3).
- [ ] `LevelStartFPFiller` 99 at level start, so Marks-Sisters (2 FTP) is affordable on turn 1.
- [ ] Dressing: the background art from `Level2-C1-TArtEx` copied under the new prefab's art root, aligned to the grid; gameplay objects aren't copied. If it can't be aligned cheaply, leave the greybox look and say so (THJ dresses it).
- [ ] An editor menu wires it idempotently (`Tools/Onboarding/The circles: Apply Wiring`, partial file in `Features/Onboarding/Editor/`, pattern `MissionWiring.Ridge*.cs`), with EditMode tests `M4CirclesTests` (layout, groups, factions, objectives, FP filler, no Cleanse lock).

**5.2 · Mission, roster, Mithra's Rest, the Queen**
- [ ] `M4 - The White Mothers.asset` graph is `GB_m4-cleanse` → `LevelDivineRelicRoom 1` → `Level3-C1`, labels (1/3) to (3/3). The old levels (duel `LevelDomFight`, `Level2-C1-TArtEx`, `Level2-C2`, `Level2-C3-1`, `Level2-C3-2`) leave the graph; their files are unchanged. Edit through Unity's serialization or an editor script; `Mission.cs` (core) is not edited.
- [ ] Roster: Toba, Linda, Lucy fixed + 1 free slot (John or Mark); Toba removed from `forcedExcludedUnits`. One Toba in every M4 level (T-11: the roster skips a Nickname already placed). Check the pick lands on the placeholder, not a fixed unit (fill order isn't specified: test it).
- [ ] `Unit_Toba.prefab`'s `unlockedAfterMission` = the M3 mission asset (`M2 - The Trail`). Report what else reads that field (Home character select, Family tree) and what changes visibly at Home after M3.
- [ ] `M4SquadSlots`: table reduced to the three graph levels (the new one included), FP filler rules kept right for them; re-runnable. `M4SquadPickTests` rewritten for the new roster (3 fixed, Toba not excluded) and graph.
- [ ] Mithra's Rest (`LevelDivineRelicRoom 1.prefab`, edit in place): level title "Mithra's Rest"; a `SafeRoomFunction` with the Healing Room's heal (`healHpModifer` `baseFactor` 0.5 on `StatUB_HP`) and its `TriggerOverlapTerminal`, copied from the Healing Room; `LevelStartFPFiller` 99; objective "Rest by the fire, take the relic, then go on."; campfire props (existing art, placeholder fine). The `DR_PickUp_HeavenlySword` already in the prefab stays (T-12: it's placed; check it's on a reachable cell near the altar and report its cell).
- [ ] `Level3-C1`: the roster works with Toba placed, the sisters placed (place them if they aren't) and the deploy slot for the pick; nothing else changes (Queen values as built).
- [ ] Cleanse locked in Mithra's Rest and `Level3-C1` (`LevelAbilityLock` by unit prefab, pattern `HearthMemoryWiring.Rules.LockCleanse`). Report every other level in the demo's mission graph (River, Ridge, Trail/M3) that still has Cleanse unlocked; don't change them here (M3 gets its lock in the M3 plan).
- [ ] Tests: `M4SquadPickTests` (rewritten), a test that the graph is the three levels in order, Mithra's Rest heal value and FP filler, the Cleanse locks. `OnboardingMissionGraphTests` still pass.

**5.3 · Lines and scenes (after `miso-narrative`'s text)**
- [ ] Toba's level-start line in M4-1; the campfire scene when the heal triggers in Mithra's Rest (family recovers, Toba's line); the Queen's end sequence (saving Ryker). Built with existing sequence players (`DialogNodeSequence`, camera, etc.), text from `design/m4-text.md`, placeholders marked as 3.1b did.
- [ ] Covering tests updated; the full EditMode suite after this chunk.

## Scope

In: the three M4 levels, the mission asset, roster, Toba's unlock field, `M4SquadSlots` and its tests, the Cleanse locks in M4-2/M4-3, the lines and three scenes.
Out:
- M3 (its own plan, greybox first, D-689) and its Toba reveal.
- Any core-systems code. `Mission.cs`, `CombatLevelRunHandler`, `SafeRoomFunction` are used as they are.
- New mechanics for the pools or the Shaman; final art; Rations (Home Kitchen not in the demo).
- Re-baselining the AI regression test.

## Touches

Systems: grid-to-level builder (editor), `HiddenLevelUnits` not needed; `LevelAbilityLock`, `GuidedAbilityHint`, `LevelStartFPFiller` (core, data only), `SafeRoomFunction` (core, data only), mission data (`Mission.cs` core, data only), roster fill (core, read only), `DivineRelicPickUp`, sequences.
USPs: Synergies (Explosive Arrow cross, Tempest Bloom, Toba's Healing Marks), Duos (Marks-Sisters first use), Family Roles (Toba's Provoking Presence). Home: Toba's unlock after M3 shows at Home.
Docs: under Gates.

## Approach

Three chunks, one implementer at a time, riskiest first. `miso-narrative` writes `design/m4-text.md` in parallel with 5.1 (it writes only under `claude-handoff/`).

- **5.1 (opus):** the new level and its wiring menu + tests. It's first because the pools' spawn settings, the Shaman, the two-objective stage and the dressing are the unknowns. Report pool values, the Shaman's preset, and whether Explosive Arrow and Marks-Sisters are unlocked for the sisters at this point of a fresh demo save (Linda's tree and D-470); if either isn't, stop and report (that's a design question, not a build fix).
- **5.2 (sonnet):** mission, roster, Toba's unlock, `M4SquadSlots` + tests, Mithra's Rest, Queen roster, Cleanse locks.
- **5.3 (sonnet):** the three scenes with the narrative text.
- One `miso-reviewer` pass over 5.1 to 5.3; full suite after 5.3; then THJ plays M4 to the Queen's death from a cleared save.

### To check during the build (report each)

- The pick fills the placeholder, not a fixed seat (T-11).
- A roster-fixed Toba and the placed Toba: one unit in each level (T-11 says yes; confirm in a test).
- Pools spawn with one alive each and stop when cleansed; "Cleanse the circles" completes when the last pool dies.
- The relic pickup in Mithra's Rest is walkable and grants 3 uses; the heal triggers once.
- Toba's unlock change doesn't break the Home character select or Bond Threads (D-366 era tests, `HomeVisitsTests`).

## Risks

- **Statics:** none expected; any new one needs a `PlayModeStaticReset` hook.
- **AI:** new level only, existing enemies. Run `AIRegressionTest.Baseline_MatchesCurrentAI` by name after 5.1 and compare with **46** (D-687). Don't re-baseline.
- **Serialized renames:** none.
- **Save data:** no shape change. Toba's unlock moves earlier (after M3, not M4): a save that finished M3 before this change sees Toba once the field changes; play checks use a cleared save.
- **Assets:** prefabs through editor scripts or the builder; small YAML only for single fields. Show the prefab diff stat in the report. `.meta` files with their assets.
- **Events / sequences:** existing players only; the heal trigger fires once.
- **Other branches:** none; onboarding only. `tech/onboarding-merge.md` gets the M4 rows (home-test merge, D-341 light touch).

## Gates

- Compile clean (verifier).
- Tests: `M4CirclesTests` after 5.1; `M4SquadPickTests`, `OnboardingMissionGraphTests`, `HomeVisitsTests` after 5.2; full EditMode suite after 5.3; AI regression by name after 5.1 (46).
- Review: one `miso-reviewer` pass over the three chunks (nothing core).
- Gate 7: the implementer reads `GB_m4-cleanse` back with `level_to_grid.py`; the coordinator renders it and compares with `m4-cleanse`.
- Play check: yes, THJ's time: M4 from a cleared save (or the dev cheat to unlock it) to the Queen's death, with John once and Mark once if time allows. "How to see it" goes in the report.
- Docs after the play check: GDD `missions-structure.md` (M4 rows, MI-3, MI-22, MI-25, Q11), `characters/toba.md`, `plans/2026-11-18-bond-threads-design.md` §10 (owner `miso-game-designer`); `glossary.md` once text is approved (`miso-narrative`); `status.md`, `build-log.md`, `tech/onboarding-merge.md` M4 rows, `tech/classic-fallback.md` if a wiring point moves (coordinator).

## Commits (after THJ's play check; proposed)

1. `feat(onboarding): M4 opens on a new level, The circles` (prefab + `.meta`, wiring menu, `M4CirclesTests`)
2. `feat(onboarding): M4 runs The circles, Mithra's Rest and the Queen with Toba in the squad` (mission asset, Toba prefab field, `M4SquadSlots`, relic room, `Level3-C1`, tests)
3. `feat(onboarding): M4 lines and scenes` (sequences + `.meta`, text)
