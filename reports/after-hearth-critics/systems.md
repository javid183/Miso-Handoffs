# Systems critique: onboarding after the Hearth (option B)

2026-11-10. Read-only critic (Explore agent following `.claude/agents/miso-design-critic.md`, lens systems; the critic agent type wasn't available in the session). Saved by the coordinator, content unchanged.

## 1. Strongest objection

**At the plan's own numbers, the plain play beats or matches the ★ play in most beats. The one beat where the ★ is risky, the River ford, goes from trivial to lethal depending on how the Family Roles rethink lands.**

- **River ford, plain play wins.** Archers at factor 0.33 ≈ 7.9 HP. Lucy, Sheltered, fires main ember (4) + two sidewinders (3 each) = 10 (`characters/lucy.md`, Papa's Shelter in `family-systems.md`). From 10,4 only the 9,5 Archer is within 3 (13,5 and 9,1 are 4 away), so she embers one island per turn; each Archer is woken by the hit and dies on her turn before it shoots (EN-16). Assumes the sidewinders land on the only target in range.
- **River ford, the ★ is worse.** The copies are clones of the main fireball (`JohnShieldRelay.LaunchCopies` → `GetClone(copyPrefab…)`), about 4 each. One Flare puts 4 on each Archer, kills none, wakes all three.
- **Cost depends on the rethink.** The ★ turn spends all John's AP (move + Shield Up). Under Kept AP (C), John can't guard; Lucy on 11,4 is within 3 of two Archers (range 3, cooldown 1, 6 × damage = 4.5 at Early) and the two woken far-bank Claws move 4 and hit her: up to 4 × 4.5 = 18 vs her 15 HP in one enemy turn. Under roles as built (A), the guard takes each hit at ×0.5 × 0.6 ≈ 1.35: nothing at stake.
- **Other beats have a safer plain play:** Ridge gauntlet by Explosive Arrow from out of sight, or bow + Fist Blitz + Continuous Attack; Trail and Pile Archers shot from 4 tiles where they can't reach; the Pile Duo works as opener, not finisher.
- **The criterion can't be met.** No caps + asleep enemies = the safe one-at-a-time play is always open. "Plain play costs a third of a hero's HP" can't hold under A (Lucy's follow-up adds 6 after every family hit; John's guard soaks the rest). "Holds under either outcome" (F1–F7) is false for the central beat.

## 2. Other risks

1. **Memory 4's "pools stop for good" won't work as specified (checked in code).** The spawner is a `HazardEntity` registered with its faction controller; `FactionControllerBase.PhaseTick` (lines 390–391) calls `PhaseTick()` on every registered entity, filtering only `IsUnityNull()`; `HazardEntity.PhaseTick` (136–176) checks only `shouldTick`, `IsAlive`, `CurrentCell`. So `GameObjectActivationManipulationAction` / `MonoBehaviourActivationManuipluationAction` don't stop it; pools keep firing turns 1–8. Fix needs `ShouldTick = false` (public property, line 70) or killing the hazard: a small new action, not data. Knock-on: Chained Assault hits nearest first within 4; a live pool Claw or left-side Claw nearer than a `top` Claw takes a slot, a top Claw survives, the memory doesn't end. 7.7 vs 7 holds, but "exactly three in reach" depends on where Mark stands; the level doesn't force it.
2. **Duo contradiction; FTP may not survive to the Pile under A.** The Trail lists "★ Marks-Sisters up column 4 from 4,1" vs the criterion "first real-combat Duo is the Pile's finisher". At the Pile, after the one-move search Linda can walk to 3,4 and fire the Duo that same turn (0 AP, needs 1 AP left, DU-1) before the west Claws act; 3,4 is next to pile cell 4,4, so that step may also complete the search. The Duo becomes the opener; "Still counting?" plays over another kill. Under A, Lucy's follow-up, Watch and John's guard each cost 1 FTP across two levels; pool 8–10, refilled only on mission entry; F7's "one Duo stays affordable" was never counted.
3. **The 1-tile island rule makes every Archer a free target for Linda.** Archer reach 3 (`ArcherGoblin_Ability_Attack.asset` radiusV 3), Linda's bow 4. Trail: from 4,1 she hits 4,5 at 4; Pile: from 5,6 she hits 9,6 at 4. At factor 0.5 (12 HP) two shots each; arrows land on unreachable ledges (LI-6), so a 3-arrow quiver forces an Encore turn (2 AP): dead time, no threat; the Trail's "~3 min" unlikely. The Pile's "★ Shield Flare from 7,4" does 4 of 12: three Flares, not an answer.
4. **Stale arrow falloff.** C4b's correction (`reports/onboarding-c4b-ridge.md` 226–230): falloff is **1.0** in code, not 0.6 (plan's Memory 1 check, GDD) or 0.9 ("6 + 5.4"). The catch does 12 per Claw; a plain bow from 4,1 hits both gauntlet Claws for 6, Fist Blitz (8) kills one, Continuous Attack the other (14 and 14 vs 10.4) in one turn, no Vault, no catch. Or wait out Explosive's cooldown and fire from 2,1 (5 tiles, outside sight 3): 8 on 6,1 / 7,1 / 8,1. Ridge beat 1: one Explosive Arrow leaves all four Claws on 1.6; a plain bow up column 1 pierces 1,4 and 1,5 at 6; the pack dies before any enemy turn, nobody loses HP. F5's "full 3" is wrong too: Continuous Attack costs 1, 2, 3 FTP, so 5 FTP buys two swings.
5. **Geometry on unverified projectile rules.** `JohnShieldRelay.FindTargetCell` (277–280) stops at a missing cell: if gaps/rock aren't cells, the Trail's Flare via the 3,4 gap fails. The Pile's bow across rock (6,6–8,6) still "to check". Whether Sheltered sidewinders aimed at a shielded John flare one by one is open.

## 3. Per option

- **A:** don't ship; slower one-at-a-time play, no question asked.
- **B:** ship with changes: make each ★ beat a place the plain play can't support (e.g. Archers must die in the same enemy turn, or they can shoot every tile Lucy can ember from); re-derive every number with falloff 1.0 and role spend under both A and C; drop Marks-Sisters from the Trail; a `ShouldTick` action for the pools; price the River ford separately for A and C.
- **C:** don't ship; merges two beats that each fail their forcing test.
- **D:** don't ship.

## 4. What would change my mind

- Combat logs from a cold run on B's prefabs showing the ★ in each pair mission (a Flare hitting 2+ Archers, a catch) and the plain play leaving a hero below two thirds HP, with the rethink switch on and off.
- A code check showing sidewinders spread across targets rather than stacking (then the single-island plain play does ~7, doesn't kill, and the Flare wins).
- A play check showing the Pile's reveal ends the family's turn (then the Duo can't fire on reveal).

**Bears on:** Q6 (objection 1, risks 3–4), Q4 (risk 1; John off the board now needs no new code), Q1 (risks 2–3), Q2 (A/C independence fails at the ford and for Pile FTP). Q3, Q5: no systems impact.
