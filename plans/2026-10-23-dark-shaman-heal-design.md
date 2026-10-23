# Dark Shaman: heal the dark brood

Size: S/M    Tier: 3 (new enemy rule and AI content; THJ's request)    Assigned to: miso-game-designer
Branch: all (built on `thj/quick-wins`)
Status: approved 2026-10-23 (D-150). THJ's answers: Q1 **1 AP like the summon** (not ending the turn; `apConsumptionType` Singular, Closure if it proves too strong); Q2 values yes; Q3 no self-heal; Q4 yes to both. Tech plan: `2026-10-23-dark-shaman-heal-tech.md`

## Why

THJ's request (2026-10-23, the last quick win): give the Dark Shaman an ability that heals nearby dark enemies (Dark Claw, Black Claw, Dark Worm, other Dark Shamans). It reuses a copy of the summon animation, and the AI picks it over the summon when a wounded ally is near. The designer sets the starting values and changes the Shaman's stats or behaviour only if needed.

## Goal

The Shaman becomes the pack's healer. Its heal is strong enough that the player wants to kill it first, and weak and slow enough that a fight never stalls.

## Acceptance criteria

- [ ] A new Shaman ability heals one wounded dark ally in range: 10 HP at the Standard tier, never above max HP. It ends the Shaman's turn and has a cooldown of 2.
- [ ] Dark Claw, Black Claw, Dark Worm (split children included) and Dark Shaman carry a new hidden tag. No other unit can be healed: no goblins, no bosses, not the Shaman itself.
- [ ] With an ally at 75% HP or less in range, the Shaman heals instead of summoning and instead of a normal attack. With no wounded ally in range, its behaviour is unchanged.
- [ ] It never targets an ally above 75% HP or a non-dark unit (AI log check).
- [ ] The cast plays the new `Heal` state, a copy of `SpawnEnemy`. The heal lands on the same frame as the summon (14).
- [ ] The player sees the heal: the camera focuses the cast, a green "+10" pops over the target, and its mini HP bar rises.
- [ ] EditMode suite green, except `AIRegressionTest.Baseline_MatchesCurrentAI`, which stays red and is not re-baselined.

## Scope

In: one ability preset, its effect and its utility graph; a new GTag on four unit prefabs; an animation clip and state; the green heal number; a GDD rule.
Out: walking toward wounded allies; heal VFX art; any change to the summon, the attack or the Shaman's stats; enemy ability text on screen (enemies.md Q7).

## Touches

Systems: ability data, AI utility graph (data only: no new variable or custom eval), tag set, Shaman animator, `DamageNumberManager` (small addition), possibly `FutureTargetsPanelUI` (see UX)
USPs: none directly (see USP check)
Docs: `design/gdd/enemies.md` (new EN-11, roster note), `glossary.md` (ability and tag names, via narrative)

## Problem and evidence

What is built today (**V** = verified in data or code, **A** = assumed):

| Aspect | Today | Source |
| --- | --- | --- |
| Shaman | 50 HP, 2 AP. Attack: 8 × `Stat_DMG`, Manhattan range 2, ends the turn, cooldown 1. Summon: 1 Dark Claw within 2 cells, 1 AP, cooldown 3. Walk uses the generic ranged walk graph. **V** | `Unit_DarkShaman.prefab` (abilities 0 attack, 1 walk, 2 summon), `Resources/UnitSpecific/Enemy/DarkShaman/` |
| Summon AI score | `3 − 2 × [nearest family member ≤ attack radius]`: 3 when no family member is within 2 cells, else 1. **V** | `DarkShaman_Summon_UtilityScoreEvaluator.asset` |
| Attack AI score | About 2 to 3 for a normal shot at full range. A shot that would finish its target adds about +3.3 (`1 / (abs(damage − HP) + 0.3)`). Adjacent targets are penalised. **V** (read from the graph; the exact numbers depend on the recent-attack factors) | `Generic_RangedDirectAttack_UtilityScoreEvaluator.asset` |
| AI choice | Greedy: every available ability × every candidate target is scored, and the best score is taken, one action at a time. Scores ≤ −100 are dropped. **V** | `AIUnitBrain.GetTurnAction`, `GenerateScoredTurnActions` |
| "Dark" in data | **Nothing.** All enemies share the `Enemy` faction. Tags in use: Black Claw `EntityState.Leader`, Masher and Deev Immovable/Unable to Swap. No family or kin tag exists. **V** | `Resources/Tags/GTagSet.asset`, the unit prefabs |
| Heal to reuse | `Dom_Heal_AttributeModifierEffect__Enemy` and `HealthPotionAttributeModifierEffect` (an `AEffectAttributeModifier` on `Specs_Health`), and `Dom_Ability_Heal_Enemy` (targeted, cell occupant, relation Ally, ranged reach) as the preset pattern. Their AI graphs (`DomEnemy_Heal_…`, `Generic_Heal_…`) read the **owner's** HP (Attribute node owner = Self), so they don't fit a heal cast on others. **V** | `Resources/UnitSpecific/Player/Dom/Abilities/Heal/`, `Features/Player/Shared/Items/HealthPotion/` |
| Graph building blocks | The utility graph can read a **target's** attribute (`Value`, `Upper Bound`, `Normalized Value`) and test a target's tag, so "wounded" and "dark" are data only. **V** | `UtilityScoreEvaluator.ResolveAttributeValue`, `ResolveTagExistence` |
| Target filter | The AI's candidate list does **not** apply `targetSelectTagQuery`, but the execution check does (`FactionControllerBase` target selection). The graph must reject what the preset's tag query rejects, or the AI could pick a target that then fails. **V** | `AIUnitBrain.GetAbilityCandidateTargets`, `FactionControllerBase.cs` ~l.274, ~l.609 |
| Line of sight | No line-of-sight system exists. **V** (no LOS code under `Core/`) | |
| Heal numbers | `DamageNumberTrigger.ShowDamage` skips values below 1, and nothing pops a heal. **A** (the HP-change wiring to `ShowDamage` was not traced) | `Core/FX/Runtime/DamageNumberTrigger.cs` |
| Heal VFX | None to reuse. The potion and Dom's heal have no VFX effect. `LindaAttackHealArrow.prefab` is a projectile. **V** | |

Root problem: the Shaman only adds bodies. A support caster that undoes the player's damage turns it into a priority target, which is a decision a summoner alone does not force.

## Options compared

**A. Who counts as dark**

| Option | Player experience | Rules / cost | Risk | Pick |
| --- | --- | --- | --- | --- |
| A1. New hidden tag `Kin.Dark` on the four prefabs; preset tag query + graph tag check | Clear: "the dark brood" | Data only; a new dark enemy just gets the tag | A level instance that overrides `tagSet` could drop the tag (check) | **Yes** |
| A2. Explicit unit list in a script | Same | Code, and a new enemy needs a code edit | Low | No |
| A3. Faction (Ally of the Shaman) | It would heal goblins and bosses too | None | It heals the Masher and the Queen: wrong fantasy, stalls boss fights | No |

**B. Shape**

| Option | Player experience | Balance | Pick |
| --- | --- | --- | --- |
| B1. Single target, range 3, 10 HP, ends the turn, cooldown 2 | Readable: one green pulse on one unit | Max 5 HP per turn per Shaman | **Yes** |
| B2. Area (all dark within 2), 6 HP each | A pack-wide surge; bigger moment | Scales with pack size: 4 Claws = 24 HP a cast. Stalls fights | No |
| B3. % of the target's max HP (30%) | Numbers vary by target (5 on a Claw, 12 on a Black Claw) | Self-balancing, but less predictable to read | No |
| B0. Do nothing | — | — | No (THJ asked for it) |

## Lens notes

**Creative.** Target feeling: the Shaman is the brood's heart. Leave it standing and the pack keeps getting back up. Kill it and the pack is mortal. The moment we design for: the player drops the Black Claw to 8 HP and ends the turn. The Shaman raises its staff (the summon pose), a green "+10" rises over the Claw, and the player thinks "next time, the Shaman goes first". It's the genre's "kill the cleric" moment (Fire Emblem's enemy staff users), placed on a fragile back-liner that the family can reach with Lucy's range, Mark's mobility or a Duo. For warmth against dread: the Corruption cares for its own, and the Bergsons beat it by caring for each other better.

**Systems.**
- **Rules.** Targeted, cell occupant, relation Ally, tag query `Kin.Dark`, `includeSelf` 0, ranged reach on. Range 3, Manhattan (`cellApplyTraverseMode` Adjacent, the same diamond shape as its attack), no line of sight. Effect: `+10 × Stat_DMG` of the Shaman to `Specs_Health` (a copy of `Dom_Heal_AttributeModifierEffect__Enemy`, without the potion's `!CheckIfHealthFull`, which checks the caster). AP: all that's left (`Closure`, like its attack). Cooldown 2.
- **Why `Stat_DMG`:** the heal then scales with tier like the Shaman's own damage (Tutorial 5, Early 8, Standard and Late 10). **A:** the factor reads the caster's stat, as the attack's does.
- **Why it ends the turn:** with 1 AP, a turn could be heal + attack, or heal + summon, every other turn. Ending the turn makes the Shaman's turn "shoot or mend", which caps healing at 10 HP per 2 turns per Shaman. Move + heal is still possible (move first).
- **Pace check.** The family deals about 32 per round from basic attacks and about 71 with reactions and Duos (`combat-balance.md` model). One Shaman undoes at most about 7% to 15% of that. Two Shamans can heal each other, but a 50 HP Shaman dies in about one family round anyway.
- **Never above max HP. A:** `Specs_Health` clamps at its max, as the potion relies on. The implementer confirms.
- **Levers:** heal factor (10), cooldown (2), range (3), the "wounded" threshold (75%), the score base and slope (below), the Leader bonus.
- **AI rule (data only, new graph `DarkShaman_Heal_UtilityScoreEvaluator`):**
  - `valid = Tag(Target, Kin.Dark) × [Target HP Normalized ≤ 0.75] × [ManhattanDistanceToTarget ≥ 1]`
  - `base = 3.5 + 2 × (1 − Target HP Normalized) + 0.5 × Tag(Target, EntityState.Leader)`
  - `score = Lerp(−1000, base, valid)`: an invalid target lands at −1000 and is dropped.
  - Range: 4.0 for an ally at 75%, 5.0 at 25%, plus 0.5 on a Black Claw. That always beats the summon (≤ 3), a normal attack (about 2 to 3) and, as far as the graphs show, a walk. A shot that would kill a Bergson (about 5.3 and up) still wins over most heals.
- **What "wounded" means:** 75% of max HP or less. A Claw (16) qualifies at 12, a Black Claw (40) at 30. At 75% the heal is rarely wasted on the bigger units.
- **What "nearby" means:** within heal range of where the Shaman stands when it chooses. No walk-to-heal pull: the Shaman's positioning stays as it is, and the player can bait it by fighting out of its range.
- **Should it ever prefer attacking or moving?** Attacking: yes, when the shot would finish a family member. An AI that skips an obvious kill looks broken, and a member's death drives Revenge (CR-25). Moving: only when no ally is wounded. The ending-the-turn rule already stops heal + anything else.
- **Failure cases:** (1) healing a nearly full unit: blocked by the 75% gate and the max-HP clamp. (2) Healing every turn so fights stall: blocked by cooldown 2 and ending the turn. Two Shamans alternating on one Black Claw is the worst case (+10 per turn): watch it in playtests. (3) The AI picks a target that the execution check rejects: avoided because the graph's tag check matches the preset's tag query. (4) A level instance overrides the tag set: the implementer checks the Claw, Worm and Shaman instances in levels and the Worm split children.

**UX.**
- **What's shown:** the camera focuses the Shaman (`hasCameraFocus` on), it plays `Heal`, the target's mini HP bar rises, and a green "+10" pops over the target. The heal number is new: today `DamageNumberTrigger` ignores HP gains. Add a heal pop-up through `DamageNumberManager.ShowText` (green, "+N") for any HP gain from an ability. That also gives the potion and Linda–Toba heals a number (Q4).
- **Shift view and threat:** the heal targets allies, so it should not appear in the danger zone or the threat arcs (both count Attack abilities only: CR-39, CR-43). **A:** the implementer confirms that the heal is not classed as an attack.
- **Likeliest misread:** the next-targets list (EN-10). `AIUnitBrain.PredictNextTargets` adds every unit the planned action touches except the Shaman itself (**V**), so the list would show a Dark Claw portrait as the Shaman's "target". Recommend hiding non-hostile units from that list for now (a small fix). A "will heal" icon is better, but it's a later polish.
- **Hover info:** the Shaman's ability list isn't shown on any screen today (Q7). Name proposal for narrative: **"Dark Mending"**, description "Heals a wounded dark ally."

## Animation

Duplicate `Features/Enemy/Dark Shaman/Art/Animations/A_Enemy_DarkShaman_SpawnEnemy_Side.anim` (**V**: it's the clip behind the `SpawnEnemy` state's blend tree in `AC_Enemy_DarkShaman.controller`, guid `27a5d294…`) as `A_Enemy_DarkShaman_Heal_Side.anim`. Add a state **`Heal`** with the same blend-tree setup (DirectionX/DirectionY) and no transition to Idle, like `SpawnEnemy`. On the prefab's new ability entry, set `animationData.stateName: Heal`, `abilityActivationFrame: 14` and `sideVisualMode: 1`, copied from the summon entry. It plays by name through `EntityAnimationHandler`, with no triggers. Optional: add `Heal` to `EnemyIdleReturnTransitionTests` (the Shaman's `Hit` and `Spawn` cases are there).

## Re-tweak

None. The Shaman's HP, attack, summon and walk stay as they are. The heal only replaces the summon or a normal attack on turns when an ally is wounded. Watch two-Shaman fights. If they run past about 3 rounds, drop the heal to 8 or the cooldown to 3 before touching the Shaman.

## AIRegressionTest

This changes AI content: a new utility graph, a fourth ability on `Unit_DarkShaman` and a new tag on four prefabs. The golden master's baked catalogs will move, so `Baseline_MatchesCurrentAI` stays red (it's already known red). **No re-baseline** (THJ's rule). The utility-variable list and the custom-eval hosts don't change, because no new variable or custom eval is used.

## USP check

- **Family Roles:** neutral. A priority back-line target rewards the roles that reach it (Mark's mobility, Lucy's range).
- **Synergies / Duos:** mildly stronger. Burst Duos (Fist Blitz, Linda–Lucy) gain a clear job: finish the Shaman, or finish a unit before it's mended.
- **Home:** neutral on purpose.

## Recommendation

A1 + B1 with the values above:

| Value | Start | Summon, for comparison |
| --- | --- | --- |
| Targets | `Kin.Dark` allies, not self, at ≤ 75% HP | — |
| Range | 3, Manhattan, no line of sight | 2 (spawn radius) |
| Heal | 10 × `Stat_DMG` (10 at Standard) | — |
| AP | Ends the turn | 1 AP |
| Cooldown | 2 | 3 |
| AI score | `3.5 + 2 × missing% + 0.5 Leader`, valid targets only | 1 or 3 |

**Playtest signal:**
- Worked: the player notices the heal, at least once says or acts "kill the Shaman first", and fights with a Shaman last about as long as before (+0.5 round at most).
- Failed: the Shaman heals the same unit turn after turn, it targets a full or nearly full unit, or players don't notice the heal at all (then the feedback is too weak).
- Check in the AI log: heal scores of 4.0 to 5.5, and a kill shot on a Bergson outscoring the heal.

## Questions for THJ

1. **Should the heal end the Shaman's turn?** Recommend yes (shoot or mend; it caps healing). The alternative is 1 AP like the summon: then heal + attack is possible every other turn. Blocks: the preset's AP value.
2. **Heal 10 (× `Stat_DMG`), cooldown 2, range 3: OK as starting values?** Recommend yes. Blocks: the preset and effect data.
3. **Can the Shaman heal itself?** Recommend no: it stays the clean priority target. Two Shamans can still heal each other. Blocks: `includeSelf`.
4. **Add a green "+N" heal pop-up for every unit (the potion and Healing Marks included), and hide allies from an enemy's next-targets list?** Recommend yes to both (small code, outside the Core systems list). Without them, the heal is easy to miss and the next-targets list misleads. Blocks: the feedback part of the build only.

## Docs to update if approved

- `design/gdd/enemies.md`: new **EN-11. Dark Mending (Dark Shaman)** with the values above, *Built* once done. Roster Notes for the Dark Shaman: "Caster, summoner, healer". Source line: add `DarkShaman/Heal/` and the `Kin.Dark` tag in `GTagSet.asset`. EN-5 is unchanged.
- `glossary.md` (narrative owns it): the ability name and "dark brood" / `Kin.Dark`, as proposals.
- `tech/pace-timings.md`: nothing, unless the heal pop-up gets its own timing.

## Risks

- A tag dropped by a level-instance override, or Worm split children spawned without the tag: the implementer checks.
- The score comparison with walk and kill shots is read from the graphs, not run: confirm it in the AI log on one level with a Shaman, a Black Claw and a Claw.
- The `Stat_DMG` read assumes the caster's stat: confirm with the stat probe window.

## Gates

Compile / EditMode tests (`AIRegressionTest.Baseline_MatchesCurrentAI` stays red) / review / play check: yes (THJ, one level with a Shaman and wounded Claws; feel chunk, so play before commit) / docs: enemies.md EN-11
