# Dark Shaman heal: tech plan

Size: S/M    Tier: 3 (decided: D-150)    Assigned to: miso-implementer, one chunk at a time
Branch: all (built on `thj/quick-wins` @ `403de3bf8`; last quick win before the merge into `main`)
Status: approved design; tech plan written 2026-10-23, ready to dispatch C1

## Why

THJ's last quick win: the Dark Shaman heals wounded dark allies. Design: [`2026-10-23-dark-shaman-heal-design.md`](2026-10-23-dark-shaman-heal-design.md) (values, AI rule, evidence table). THJ's answers in D-150; the one change from the design: **the heal costs 1 AP like the summon** (`apConsumptionType: Singular`), not "ends the turn".

## Goal

The Shaman heals one wounded dark ally in range and the player can see it, with the AI choosing it over summoning when an ally is hurt.

## Acceptance criteria

- [ ] A fourth Shaman ability heals one `Kin.Dark` ally (not itself) within Manhattan range 3 by 10 × the Shaman's `Stat_DMG` (10 at Standard), never above max HP. 1 AP, cooldown 2.
- [ ] `Kin.Dark` (hidden tag) is on Dark Claw, Black Claw, Dark Worm (incl. its split children) and Dark Shaman, and on no other unit; no level instance drops it.
- [ ] With a dark ally at ≤ 75% HP in range, the AI heals instead of summoning and instead of a normal attack; a shot that kills a family member still wins; no wounded ally in range → behaviour unchanged. It never targets an ally above 75% or a non-dark unit (AI log).
- [ ] The cast plays the new `Heal` state (copy of `SpawnEnemy`), activation frame 14, camera focus on.
- [ ] Every ability HP gain on any unit shows a green "+N" pop-up over the unit (Shaman heal, potion, Healing Marks, Linda–Toba heals).
- [ ] The enemy next-targets list shows only hostile units (a healed Claw is not shown as the Shaman's target).
- [ ] The heal is not in the Shift danger zone or threat arcs (not an attack).
- [ ] Compile clean; EditMode green except `AIRegressionTest.Baseline_MatchesCurrentAI` (stays red, **no re-baseline**).

## Scope

In: tag, effect, preset, utility graph, animation clip and state, prefab ability entry (C1); heal pop-up and next-targets filter (C2).
Out: walk-to-heal; heal VFX art; any change to the Shaman's stats, attack, summon or walk; enemy ability text on screen.

## Touches

Systems: tags (`Resources/Tags/GTagSet.asset`, data only), ability data and effects (new assets only; **no code change** to `AbilityPreset`/`AEffect*` core), AI utility graph (data only: new asset, no new variable or custom eval; `AIUnitBrain` untouched), unit prefabs (`Unit_DarkShaman`, Dark Claw, Black Claw, Dark Worm + split child), Shaman animator, `DamageNumberManager`/`DamageNumberTrigger` (C2), the next-targets panel UI (C2; filter in the UI, **not** in `AIUnitBrain.PredictNextTargets`, which is core AI).
USPs: Synergies/Duos (light).
Docs: `design/gdd/enemies.md` EN-11 "Dark Mending" (game designer, once built), glossary name proposal (narrative), this plan's commit log, build log.

## Approach

### C1. Heal ability and AI (data, `opus`: AI content and prefabs)

All asset work, preferably through the Unity MCP and editor (or careful YAML edits); paths per the design's evidence table.
1. **Tag:** add hidden `Kin.Dark` to `Resources/Tags/GTagSet.asset` (follow how `EntityState.Leader` is defined). Add it to the tag sets of `Unit_DarkShaman`, Dark Claw, Black Claw, Dark Worm and the Worm's split-child prefab. Grep level prefabs/scenes for instances that override `tagSet` on these units and fix any that would drop it; report them.
2. **Effect:** copy `Resources/UnitSpecific/Player/Dom/Abilities/Heal/Dom_Heal_AttributeModifierEffect__Enemy` into `Resources/UnitSpecific/Enemy/DarkShaman/Heal/` as `DarkShaman_Heal_AttributeModifierEffect`: `+10 × Stat_DMG` of the caster to `Specs_Health`. Don't copy the potion's caster-full-HP check. Confirm HP clamps at max (report how).
3. **Preset:** `DarkShaman_Ability_Heal` from `Dom_Ability_Heal_Enemy`'s pattern: targeted, cell occupant, relation Ally, `targetSelectTagQuery` `Kin.Dark`, `includeSelf` off, ranged reach on, Manhattan range 3 (same traverse mode as the Shaman's attack), cooldown 2, `apConsumptionType: Singular` (1 AP), camera focus on, not classed as an attack (check the Shift/threat code's test).
4. **Utility graph:** new `DarkShaman_Heal_UtilityScoreEvaluator` (data only): `valid = Tag(Target, Kin.Dark) × [Target HP Normalized ≤ 0.75] × [ManhattanDistanceToTarget ≥ 1]`; `base = 3.5 + 2 × (1 − Target HP Normalized) + 0.5 × Tag(Target, EntityState.Leader)`; `score = Lerp(−1000, base, valid)`. Build it from the nodes `ResolveAttributeValue` / `ResolveTagExistence` support; use an existing Shaman graph as the template.
5. **Animation:** duplicate `Features/Enemy/Dark Shaman/Art/Animations/A_Enemy_DarkShaman_SpawnEnemy_Side.anim` as `A_Enemy_DarkShaman_Heal_Side.anim`; add state `Heal` to `AC_Enemy_DarkShaman.controller` with the same blend-tree setup as `SpawnEnemy` and no transition to Idle (animations play by name through `EntityAnimationHandler`). Optionally add `Heal` to `EnemyIdleReturnTransitionTests`.
6. **Prefab:** add the ability as the fourth entry on `Unit_DarkShaman.prefab`, copying the summon entry's `animationData` (`stateName: Heal`, `abilityActivationFrame: 14`, `sideVisualMode: 1`) and wiring the graph. Prefab diffs only the intended lines (remove serializer noise).
7. **Tests:** if any pure logic is added (none expected), test it. `AIRegressionTest` will move: leave it red; do not add catalog lines or re-baseline unless THJ asks (unlike D-104, there's no request here; report what it now reports).
- Acceptance: the C1 criteria (all but the pop-up and next-targets lines).

### C2. Heal pop-up and next-targets filter (code, `sonnet`)

1. **Heal pop-up:** where HP changes reach `DamageNumberTrigger.ShowDamage` (trace it; the design assumed, didn't trace), show HP gains from abilities and items as a green "+N" via `DamageNumberManager.ShowText` (or a heal path on the trigger), N rounded like damage numbers; serialized colour. Don't show regen ticks or level-start HP restores if those also raise HP (say which sources pop).
2. **Next-targets filter:** in the next-targets panel UI (find it, e.g. `FutureTargetsPanelUI`), show only units hostile to the enemy that plans (`FactionsRelationType`), so allies the Shaman heals aren't listed. Don't change `AIUnitBrain.PredictNextTargets` (core AI).
3. Pure logic (e.g. "pops for this change") with EditMode tests if extracted.
- Acceptance: the pop-up and next-targets criteria.

## Risks

- **AI content:** `AIRegressionTest` moves (already known red; no re-baseline). Nothing the AI thread reads changes in code: only data (graph, tag, preset).
- **Graph/preset mismatch:** the AI candidate list doesn't apply `targetSelectTagQuery` but execution does; the graph's tag check must match, or the AI picks a target that fails.
- **Tag coverage:** level-instance `tagSet` overrides and Worm split children.
- **`Stat_DMG` read on the caster** (the design assumes it); confirm in play with the stat probe.
- **1 AP:** heal + attack in one turn is possible every other turn (THJ's choice; Closure is the fallback).
- **Prefabs:** small diffs; the Shaman prefab is a `UnitBase` variant (keep `hitEffects`/death wiring untouched).
- **Statics:** none expected.

## Gates

Per chunk: compile; EditMode (known red only); reviewer; **THJ's play test before each commit** (one level with a Shaman, a Black Claw and Claws; AI log for scores 4.0–5.5 and a Bergson kill shot outscoring a heal); docs after: EN-11 in `enemies.md` (game designer), glossary proposal (narrative).

## Commit log

(filled in as chunks are committed)

- C2: built (`reports/shaman-heal-c2.md`): green "+N" from the real capped gain via a per-unit `HealPopTracker` claimed on `onAbilityEffectPerformedOn` (compound heals from `AEffectCompound`, bare-modifier heals on `RuntimeAbility` completion: same-frame only if the preset has no minimum duration/wait and `actualTargets` on); next-targets panel lists only units hostile to its planner. Review APPROVE (`reports/shaman-heal-c2-review.md`), both should-fixes applied (comment, tracker + 6 sequence tests). EditMode 624/625 (known red only). Follow-up noted: hovering a Shaman still highlights the healed Claw's cell (`GUnit.SetFutureTargetsHover`, core). THJ play-tested: no "+N" appeared. Cause (read, not seen): the Shaman heal, potion and Dom heal fire on an animation event (`activationMode 2`) and report completion frames later, after the end-of-frame drop. Fix: `HealPopWindow` tracks running abilities (`abilityActivationStarted` → `abilityPerformed`, cleared on turn start/end); a gain during a running ability pops at once; the old claim stays as fallback; gains outside abilities still dropped. 5 more tests; EditMode 653/654 (known red). Gaps: a passive self-heal during an ability also pops; abilities raising neither event (some faction roles; the Linda–Toba duo path not checked) won't pop. Waiting on THJ's re-test, then two commits.
- C1: built (`reports/shaman-heal-c1.md`): `Kin.Dark` in `GTagSet` and `GTagRegistry`, on Dark Claw, Black Claw (own second entry), Dark Worm, Dark Shaman; effect, preset (classed Ability, not Attack, unlike Dom's template), graph, `Heal` clip and state, fourth ability on the Shaman. EditMode 608/609 (known red; `AIRegressionTest` now also flags the new graph and ability; no re-baseline). Review APPROVE (`reports/shaman-heal-c1-review.md`), test summary wording fixed. THJ: stunned and dormant dark allies can be healed too (D-151, kept as built). THJ play-tested it: good. Committed on `thj/quick-wins`: `2b8e4ea88` (tag), `e81c20f59` (animation), `2095e4eaf` (ability, effect, graph, Shaman prefab with its tag). Left out: six asset edits from THJ's play session (Mark–Lucy duo, Dark/Black Claw walk, Dom Swap, Lucy Cyclone value changes plus serializer fields), not part of this chunk. **For C2:** the HP change event reports the unclamped amount, so the pop-up must use the real gained HP; the healed Claw shows in next-targets until C2.
