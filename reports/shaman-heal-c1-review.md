# Review: Dark Shaman heal C1 (ability and AI, data only)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins`.
Plan: `plans/2026-10-23-dark-shaman-heal-tech.md` C1 (D-150). Implementer report: `reports/shaman-heal-c1.md`.

**Verdict: APPROVE.** No must-fix. One should-fix (test class summary wording), sent back.

## Should fix

1. `EnemyIdleReturnTransitionTests.cs` class summary still says "hit and spawn states"; it now also covers the `Heal` ability state.

## Notes

- **Diff vs report:** matches exactly (TMP font, Packages, ProjectSettings excluded). LF and BOM unchanged.
- **Tag:** `Kin` / `Dark` (`showInGame: 0`) identical in `GTagSet.asset` and `GTagRegistry.asset`; ids are name paths (no guids). Registry order matches `AccumulateTags()`; `Awake`/`OnValidate` rebuild it anyway. No core tag or referenceable-id code touched. `UnitBase.prefab` has `tagEntries: []`, so size-1 overrides add without truncating; Black Claw keeps `data[0] = EntityState.Leader`, adds `data[1] = Kin.Dark`. Summon spawns `Unit_DarkClaw`, Worm split spawns `Unit_DarkWorm`: both tagged. Level `tagSet` overrides are on GridCell only. Hidden tags filtered by `ShowInGame` in tooltip, `GUnit`, combat log.
- **Effect:** one Additive modifier on `Specs_Health`, StatBacked `10 × Stat_DMG`, bounded like the Shaman attack's; caster stats via the prefab entry's Ability/Unit/Faction sources. No feasibility check. `RuntimeAAttribute.SetValue` clamps to max; the HP-changed `difference` is unclamped (line 61): C2 must use the real gain.
- **Preset:** matches the plan (Targeted, CellOccupant, Ally, `Kin.Dark` query, no self, ranged reach, traverse like the attack, radius 3, cooldown 2, `apConsumptionType 1`, camera focus, `activationMode 2`). `actionType 2` (Ability) like the summon. Nothing relies on heals being Attack (`UnitThreatAnalysis`, cursor catalog, `CombatLog`, `BarkManager`, Masher/Lucy/`PlayerController`/`AEffectCommand` checked); counters and cooperation read `IsBasicAttack` (0); faction-role triggers need a family target.
- **Graph:** node encodings checked against `UtilityScoreEvaluator`; edges implement `Lerp(-1000, 3.5 + 2(1-hp) + 0.5·Leader, valid)`; tag check matches the query; `GetActualTarget` resolves the occupant first; existing node types only. Wired on the preset; the preset is `data[3]` on the Shaman.
- **Animation:** clip byte-identical to `SpawnEnemy_Side` but for `m_Name`; `Heal` copies the state and its 1D DirectionY blend tree, no transitions, unique fileIDs. 17 keyframes at 1/12 s: frame 14 inside.
- **Prefabs:** only tag and ability-entry lines; `hitEffects`/death untouched; no code indexes abilities by position. A later Unity save may reorder the hand-placed modification blocks (noise).
- **AI regression:** test file unchanged (no re-baseline); data only.
- **Commit grouping** tags → animation → ability+graph+prefab works; each builds alone. Commit 1's message shouldn't say the Shaman is tagged (its tag line is in commit 3).
- **For the play test:** a kill shot outscoring the heal (not evaluated offline); `Stat_DMG` on the caster (10 at Standard); the heal can target dormant (`Status.Inactive`) or stunned dark allies ≤ 75% (not in the design; check it's wanted); heal + attack every other turn (1 AP).
