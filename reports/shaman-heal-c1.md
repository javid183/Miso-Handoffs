# Report: Dark Shaman heal, C1 (heal ability and AI, data only)

Plan: plans/2026-10-23-dark-shaman-heal-tech.md (C1)    Agent: miso-implementer    Branch: thj/quick-wins (not switched)
Outcome: done (data only, no game code changed; one test file gained two test cases)

## What changed

All paths under `miso/Assets/_Project/`.

New:
- `Resources/UnitSpecific/Enemy/DarkShaman/Heal.meta`: folder meta for the new Heal folder.
- `Resources/UnitSpecific/Enemy/DarkShaman/Heal/DarkShaman_Heal_AttributeModifierEffect.asset` (+ `.meta`, guid `67d4af92…`): the heal effect, `+10 × Stat_DMG` on `Specs_Health`, Additive.
- `Resources/UnitSpecific/Enemy/DarkShaman/Heal/DarkShaman_Ability_Heal.asset` (+ `.meta`, guid `b89c7488…`): the heal preset.
- `Resources/UnitSpecific/Enemy/DarkShaman/Heal/DarkShaman_Heal_UtilityScoreEvaluator.asset` (+ `.meta`, guid `12c77483…`): the heal's AI graph.
- `Features/Enemy/Dark Shaman/Art/Animations/A_Enemy_DarkShaman_Heal_Side.anim` (+ `.meta`, guid `79a6fbdd…`): copy of the SpawnEnemy clip (only `m_Name` differs).

Changed:
- `Resources/Tags/GTagSet.asset`: new root tag `Kin` with hidden sub-tag `Dark` (`showInGame: 0`, no icon, a designer-facing description).
- `Resources/Tags/GTagRegistry.asset`: the same 15 lines in its accumulated copy of GTagSet's roots (the registry keeps a serialized copy; the last tag commit edited both the same way).
- `Features/Enemy/Dark Claw/Prefabs/Unit_DarkClaw.prefab`: tag set override, 1 entry `Kin.Dark` (Persistent, lifeTurns -1).
- `Features/Enemy/Dark Claw/Prefabs/Unit_BlackClaw.prefab`: tag set size 1 → 2, `data[1] = Kin.Dark` (it is a variant of Dark Claw and already overrode `data[0]` with `EntityState.Leader`, so it needed its own entry).
- `Features/Enemy/Dark Worm/Prefabs/Unit_DarkWorm.prefab`: tag set override, 1 entry `Kin.Dark`.
- `Features/Enemy/Dark Shaman/Prefabs/Unit_DarkShaman.prefab`: tag set override `Kin.Dark`; abilities 3 → 4, `data[3]` = `DarkShaman_Ability_Heal`, `stateName: Heal`, `abilityActivationFrame: 14`, `sideVisualMode: 1`, stat sources Ability/Unit/Faction (copied from the summon entry).
- `Features/Enemy/Dark Shaman/Art/Animations/AC_Enemy_DarkShaman.controller`: new state `Heal` (no transitions) with a 1D blend tree on `DirectionY` (-1/0/1, all three the Heal_Side clip), same setup as `SpawnEnemy`; added to the Base Layer's child states.
- `Core/Animation/EntityAnimation/Editor/EnemyIdleReturnTransitionTests.cs`: `[TestCase(DarkShaman, "Heal")]` added to both tests (no Idle transition; clip plays once).
- Review should-fix: that test class's summary now says "hit, spawn and ability-cast states". Recompiled with no errors; `EnemyIdleReturnTransitionTests` passes 28/28.

Not mine: `miso/Assets/TextMesh Pro/.../LiberationSans SDF - Fallback.asset` was already modified before I started (in the session's initial git status).

Every prefab diff shows only the intended lines. Unity's save moved two existing `idleSpeedJitter` / `idleAnimationData.randomizeStartFrame` modification blocks inside the list (pure reorder); I removed that noise by re-applying the tag/ability blocks to the committed file, then reimported and re-read the prefabs in the editor to confirm the values.

## The preset as built

`DarkShaman_Ability_Heal` (copy of `Dom_Ability_Heal_Enemy`, then):
- `title: Dark Shaman Heal` (shows in the AI log; enemy ability names aren't on screen), `description: '[PLACEHOLDER] Heals a wounded dark ally.'`
- `actionType: 2` (Ability). **Dom's template is `1` (Attack)**, which would have put the heal in the danger zone and threat arcs, so I changed it (see the classification check below).
- `apConsumptionType: 1` (Singular, 1 AP), cooldown constant 2, radius constant 3.
- `targetType: 2` (CellOccupant), `applyMode: 0` (Targeted; Dom's was Self), `activationMode: 2` (EventBasedAnimated, like the Shaman's attack), `targetFactionRelation: 1` (Ally), `includeSelf: 0`.
- `allowRangedReach: 1`, `cellApplyTraverseMode: 1` (Adjacent = Manhattan diamond, same as `DarkShaman_Ability_Attack`).
- `targetSelectTagQuery`: one entry `Kin.Dark`, policy Self, expectation Present; query policy All.
- `hasCameraFocus: 1`, `showAffectedArea: 0` (like the Shaman's attack), icon cleared (Dom's potion icon).
- `statAttributes`: kept the 8 entries (Stat_HP, Stat_DMG, …) so `Stat_DMG` resolves the same way the attack's does.
- `utilityScoreEvaluator`: `DarkShaman_Heal_UtilityScoreEvaluator`.

## The effect and the HP clamp

`DarkShaman_Heal_AttributeModifierEffect` (copy of `Dom_Heal_AttributeModifierEffect__Enemy`): one modifier on `Specs_Health`, policy Additive, factor StatBacked `10 × Stat_DMG`, bounded min 0 / max `1 × StatUB_DMG` (the exact pattern of the Shaman's attack AttrMod; `StatUB_DMG` is 9999 in the enemy faction). No feasibility check (Dom's enemy effect had none either).

HP clamp: `RuntimeAAttribute.SetValue` (`Core/Systems/AbilitySystem/Attributes/Runtime/RuntimeAAttribute.cs` l.60) sets `BaseValue = Mathf.Clamp(newValue, MinValue, MaxValue)`, so a heal never takes HP above max. Read in code, not tested in play. Note for C2: the `difference` it reports to `onValueChanged` (l.61) is computed from the **unclamped** value, so an overheal reports the full 10. A heal pop-up driven by that event would show "+10" on a unit that only gained 3.

## The graph as built

`DarkShaman_Heal_UtilityScoreEvaluator`, created in the editor from the graph model (nodes, edges, `operands` = the full variable list, as the graph window writes it). Node types only: Tag, Attribute, Variable, Constant, Comparison, Multiply, Subtract, Add, Lerp. No new utility variable, no custom eval.

- `hp` = Attribute `Specs_Health`, owner Target, port Normalized Value; "if doesn't exist" = 1 (a target without HP counts as full, so invalid).
- `valid = Tag(Target, Kin.Dark, Present) × [hp ≤ 0.75] × [ManhattanDistanceToTarget ≥ 1]`
- `base = 3.5 + (1 − hp) × 2 + Tag(Target, EntityState.Leader, Present) × 0.5`
- `Score = Lerp(−1000, base, valid)`

The graph's tag check (`Kin.Dark`, exact id on the target) matches the preset's tag query (`Kin.Dark`, policy Self, Present). I evaluated the saved YAML offline with a small script that follows the evaluator's rules: Kin.Dark at 75% → 4.0; at 25% → 5.0; Black Claw (Leader) at 25% → 5.5; at 80% → −1000; untagged ally → −1000; distance 0 (self) → −1000. 75% is exact for a Claw (12/16) and a Black Claw (30/40), so the gate includes them.

## Tag coverage and level overrides

- Tagged: `Unit_DarkClaw`, `Unit_BlackClaw` (Leader + Kin.Dark), `Unit_DarkWorm`, `Unit_DarkShaman`. Checked in the editor after reimport.
- Worm split children: `DarkWorm_Ability_Split` spawns `Unit_DarkWorm` itself (same prefab guid), and neither `AGUnitSpawner` nor `DarkWormPassiveAbility` touches tags, so split children carry the tag. The Shaman's summon spawns `Unit_DarkClaw`, so summoned Claws carry it too.
- Level overrides: I searched every `.prefab` and `.unity` under `Assets` for `tagSet.tagEntries`. The only level hits (`Level1/Level1-C3 1.prefab`, `Level2/Level2-C2.prefab`) override `GridCell.prefab`, not a unit. No instance of the four units overrides its tag set (46 Dark Claw, 4 Black Claw, 10 Shaman, 2 Worm instances). Nothing to fix.
- No other unit has the tag.

## Attack classification

The danger zone and threat arcs read `UnitThreatAnalysis.IsReadyAttack` / `GetReadyAttackAbilities`, which count only `ActionType == Attack`. The heal is `Ability` (2), so it is excluded. The only other `ActionType.Attack` check is the cursor catalog (player cursor; not reached for enemy abilities). `AttackReachTests` pass. Not checked in play.

## Compile and EditMode

- Refresh + recompile: no console errors. The warnings are the existing ones (serialization depth on `GTag.subTags` and `StatBackedValue`, three CS warnings in editor tools).
- EditMode (editor open, run via the Unity MCP test runner): **608 / 609 passed**; the one failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (the known red). The new `EnemyIdleReturnTransitionTests` Heal cases pass.

## What AIRegressionTest now reports

38 failures out of 709 checks. My change adds these three:
- `graphs.count: expected 28, found 29`
- `graphs.unexpected …/DarkShaman/Heal/DarkShaman_Heal_UtilityScoreEvaluator.asset: new evaluator is not in today's baseline`
- `abilities.unexpected …/DarkShaman/Heal/DarkShaman_Ability_Heal.asset: new ability is not in today's baseline` (`abilities.count` was already failing: expected 90, found 96, with five other unexpected abilities that were already there)

The others were already there: `intent.unit-tile.enemy`; node, edge and fingerprint drift on six Generic graphs; the five other unexpected abilities; `Mark_Lucy_MARK_Duo_Ability` evaluator; `Unit_Placeholder` missing; `StuntCamActorSet` unexpected; missing abilities on `Unit_Toba_Ally`, `Unit_TobaEnemy`, `Unit_Lucy`; and a fatal NRE in `AIStrategyPlanner.HandleLivingUnitsCondition` (l.163) from `RunStress`. `utility.variables` passes (no new variable). The Shaman's units checks (`units.ability Unit_DarkShaman/*`) pass, since the check looks for missing abilities, not extra ones. I didn't re-baseline and didn't add catalog lines.

## Acceptance criteria (C1)

- [x] Fourth Shaman ability: Kin.Dark ally, not self, Manhattan 3, 10 × caster `Stat_DMG`, clamped at max, 1 AP, cooldown 2. Data checked in the editor; the clamp is read in code. **Needs play:** the heal amount (10 at Standard) and that `Stat_DMG` resolves on the caster (check with the stat probe).
- [x] `Kin.Dark` on Dark Claw, Black Claw, Dark Worm (incl. split children), Dark Shaman only; no level instance drops it. Checked in the editor and by grep.
- [ ] AI heals when an ally is at ≤ 75% in range, a kill shot still wins, otherwise unchanged, never targets an ally above 75% or a non-dark unit. The graph is checked offline (scores 4.0 to 5.5, −1000 when invalid). **Needs THJ's play check / AI log.**
- [x] Cast plays `Heal` (copy of `SpawnEnemy`), frame 14, camera focus on. Data checked; the idle-return tests cover the new state. **Needs play** to see it.
- [x] Not in the Shift danger zone or threat arcs: `actionType` Ability, read in code. **Needs play** to confirm.
- [x] Compile clean; EditMode green except the known red, no re-baseline.

## Save reset

No.

## Decisions I made

- `actionType` set to Ability (2), not the template's Attack (1), so the heal stays out of the danger zone and threat arcs, as the plan requires.
- `title` "Dark Shaman Heal", like the summon's "Dark Shaman Summon" (used in the AI log); `description` tagged `[PLACEHOLDER]`. The narrative name ("Dark Mending") comes later.
- The effect's bound uses the attack's `1 × StatUB_DMG` cap instead of Dom's WIS-based constant (20 + 12 WIS), so the heal scales only with `10 × Stat_DMG`.
- `showAffectedArea` 0 (like the Shaman's attack; Dom's player-facing potion had 1) and the icon cleared: neither is shown for enemy abilities.
- The Attribute node's "if doesn't exist" value is 1, so a target without `Specs_Health` is never "wounded".
- The `Kin.Dark` tag has a short designer description; it's hidden in game.
- Added the optional `Heal` cases to `EnemyIdleReturnTransitionTests`.

## Needs THJ

None.

## Docs to update

- `design/gdd/enemies.md`: EN-11 Dark Mending, *Built* once played (game designer). Source line: `Resources/UnitSpecific/Enemy/DarkShaman/Heal/` and `Kin.Dark` in `GTagSet.asset`.
- `glossary.md`: ability name and the "dark brood" / `Kin.Dark` proposal (narrative).
- `tech/core-systems.md`: nothing (no core code touched; the tag set is data).

## Risks and loose ends

- **For C2 (heal pop-up):** `RuntimeAAttribute.SetValue` reports the unclamped difference, so a heal on a nearly full unit reports +10 even when less is gained (see the effect section).
- **For C2 (next targets):** `PredictNextTargets` will now list the healed Claw as the Shaman's target, as the design expected.
- `Stat_DMG` on the caster: the heal reads it the same way as the Shaman's attack AttrMod (stat-backed through the ability's stat sources Ability/Unit/Faction), but this isn't confirmed in play.
- The AI's candidate list ignores `targetSelectTagQuery`; the graph's `Kin.Dark` check covers it. If someone later changes the preset's query, the graph must change with it.
- The heal takes the same `allowRangedReach` path as the attack: no line of sight, so it heals through units in between (by design).
- `GTagRegistry.asset` is a serialized copy that `OnValidate` rebuilds. I edited it by hand to match GTagSet (as the last tag commit did). If Unity rewrites it later, expect it to match.

## Proposed commits

1. `feat(tags): hidden Kin.Dark tag on the dark brood`: `Resources/Tags/GTagSet.asset`, `Resources/Tags/GTagRegistry.asset`, `Unit_DarkClaw.prefab`, `Unit_BlackClaw.prefab`, `Unit_DarkWorm.prefab` (plain; data). The Shaman prefab's tag line goes in commit 3 with its ability entry, since both are in one file.
2. `feat(anim): Heal state for the Dark Shaman (copy of its summon cast)`: `A_Enemy_DarkShaman_Heal_Side.anim` + `.meta`, `AC_Enemy_DarkShaman.controller`, `EnemyIdleReturnTransitionTests.cs` (plain).
3. `feat(enemy): the Dark Shaman heals a wounded dark ally`: `Resources/UnitSpecific/Enemy/DarkShaman/Heal.meta`, `Heal/DarkShaman_Heal_AttributeModifierEffect.asset` + `.meta`, `Heal/DarkShaman_Ability_Heal.asset` + `.meta`, `Heal/DarkShaman_Heal_UtilityScoreEvaluator.asset` + `.meta`, `Unit_DarkShaman.prefab` (AI content; moves the known-red `AIRegressionTest`). Depends on 1 and 2.

THJ play-tests before any commit (feel chunk). C2 can land as its own commits after.

## Other branches

None (it goes to `main` with the `thj/quick-wins` merge).

## How to see it

1. Open a level with a Dark Shaman and Dark Claws / a Black Claw (or drop `Unit_DarkShaman`, `Unit_BlackClaw` and two `Unit_DarkClaw` into a test level), with the AI log on.
2. **Wounded ally in range:** bring a Claw to ≤ 12/16 HP (or the Black Claw to ≤ 30/40) within 3 Manhattan tiles of the Shaman, then end the turn. Expect: the camera focuses the Shaman, it plays the summon-like `Heal` pose, and the Claw gains 10 HP (never above max). AI log: heal score 4.0 to 5.0 for a Claw, +0.5 on the Black Claw, above the summon (≤ 3) and the normal attack.
3. **Out of range:** the same wounded Claw 4+ tiles away. Expect no heal (the Shaman doesn't walk to heal); it attacks, summons or walks as before.
4. **Ally above 75%:** only lightly hurt allies (e.g. Claw at 13/16). Expect no heal; the log shows the heal at −1000 for them (dropped).
5. **Kill shot:** leave a family member killable by the Shaman's attack (≤ its damage) while a Claw is wounded in range. Expect the attack to win (the kill bonus should score above about 5.3); compare both scores in the log.
6. **Two Shamans:** wound one Shaman, keep the other within 3. Expect it to heal the other Shaman, never itself. Watch the cooldown: at most one heal every other turn per Shaman.
7. **1 AP:** on a heal turn the Shaman can still act with its second AP (attack, summon or walk).
8. **Shift view:** hold Shift during the player's turn. The Shaman's danger zone and threat arcs should be unchanged by the heal (attack range only).
9. Not visible yet (C2): no green "+10" pop-up, and the next-targets list may show the healed Claw.
