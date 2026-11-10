# Family Roles round 2: systems critique

Critic: `miso-design-critic`, lens **systems**. Target: [`2026-11-09-family-roles-round2-design.md`](2026-11-09-family-roles-round2-design.md) (recommendation P). Read 2026-11-09: the draft in full, round 1, `vision.md`, GDD (`combat-rules.md`, `family-systems.md`, `enemies.md`, `characters/john|linda|lucy|mark.md`), the after-Hearth onboarding plan, `tech/core-systems.md`, `decisions.md` (D-216, D-061); code: `FactionRoleHandlerBase.cs`, `JohnFactionRoleHandler.cs`, `JohnPassiveAbility_Wrath.cs`, `LindaFactionRoleHandler.cs`, `MarkFactionRoleHandler.cs`, `MarkPassiveAbility_AtmanFocus.cs`, `UtilityVariables.cs`, the four `Unit_*.prefab` role components and Mark's Focus tables, `John_Ability_Attack_Sword.asset`, `John_Ability_Shield.asset`, `DarkClaw_Ability_Attack.asset`. Paths under `miso/Assets/_Project/`.

## Strongest objection: P makes roles readable, not decided

THJ's test is "is arming it a real decision?". Two of P's three principles fail it by construction. Principle 2 ("an action worth taking on its own") and principle 3 ("a resource built by ordinary play") both mean the arm is a by-product of what the hero does anyway. John casts Shield Up for its ×0.6, Wrath, +1 FTP (CR-11) and Shield Flare. Mark lands Fist Blitzes because it's his basic attack. Then the two press choices the draft counts as real don't hold up either:

- **John's press is indifferent in S2.** Each guard turns a ≈3 hit into ≈0.9 (×0.5 × 0.6). With five identical Claws, it makes no difference to HP *which* hit the third guard absorbs, so declining one prompt to "save the shield" moves damage between sisters without reducing it. The draft's own line declines a guard on Lucy (15 HP) to save one for Linda (20 HP), which is the wrong way round. Round 1 saved the guard for Lucy (round 1 S2, line 311).
- **Mark's press is dominated** (point 2).

What P does fix is THJ's *other* complaint, "you never know what you did for it to work". Every prompt now traces back to a visible cause. That is worth having, but it is legibility, not challenge, and the draft's decision counts ("2 decisions", "1 real press choice") treat "a cause exists" as if it meant "a choice exists". The only gate that makes a real choice on paper is Linda's lane on a two-front board (S3), plus John's Shield Up on turns where he has to move to reach his target, and none of the three scenarios shows that John turn.

**Change:** re-grade S1 and S2 honestly (point 3). Make the Step 2 read-out ask two separate questions: "did you know why it fired?" (legibility) and "did you ever not arm it / not press it, and was that right?" (decision). Add one John scenario where Shield Up competes with move + Sword (River beat 1 is a candidate). Give J2 and M2 a cost that bites (points 1 and 2). Otherwise P passes on legibility, THJ still finds it "just a click", and the stop rule fires on a design that was never given a real trade.

## Other points

### 1. J2's "strike before you raise it" is free at the front and punishing at the back

- **Evidence.** Sword: 1 AP, cooldown 0 (`John_Ability_Attack_Sword.asset` `coolDownV` 0; GDD John). Wrath is spent by *any* damage John deals to an enemy (`JohnPassiveAbility_Wrath.cs:134-138`).
  - **A John in melee** plays Sword then Shield Up every turn, which is his normal 2-AP turn. So "can't raise until he strikes" never costs him anything. J2 reduces to "at most 3 absorbs per enemy turn".
  - **A John who stayed beside the sisters** to guard (which is the posture J1's range 2 rewards), with no enemy in Sword reach, can't spend Wrath. So he can't raise the shield and gets no guard on the next enemy turn, unless he Shield Dashes up to 3 cells off his post (cooldown 2). Stacks also carry over between turns (Wrath.cs keeps `_stacks`; only `_shieldUpActive` resets, `:126-130`). A John who didn't strike therefore starts the next enemy turn one hit from breaking.
  - **J2 counts more than guards.** Wrath gains on *every* health loss while shielded (`OnHealthDecreased`, `:150-162`), not only on guards. That includes hits aimed at John himself, Burn and poison ticks, and the Deev's pools (EN-7, 6 × per tick). The more the enemy focuses John, the fewer guards he has. It's the opposite of how a tank should play, and the player can't control it.
  - **Filling Wrath is a reward** (+105% at 3, ×2.05), so the player is pushed to *press*, not to ration.
  - **One counter, two jobs** means the "fortress" lever (Wrath max 3 → 2) also cuts the punish to +70%. That needs a per-stack retune at the same time (+35% → +50%).
- **Change.** Make the break cost the next turn instead of "strike first": *"A broken shield can't be raised on John's next turn"* (a one-turn block, applied on break). Declining at Wrath 2 then really protects next turn's guard, and a backline John isn't forced off his post. Alternatively, count only guarded hits toward the break, which lets the player control it but separates it from Wrath: a second counter, so weigh that against D-295. Put Wrath max and per-stack in the lever table as a linked pair.
- **Cost claim.** J2 is S–M, not S. The break has to remove Shield Up's damage-taken modifier in the middle of an enemy action, inside a health-change callback. That is the code `JohnFactionRoleHandler.cs:179-185` warns about (a shared `Stat_DR` context that once caused a StackOverflow with Shield + role active together). `RelayArea` can also put two allies' hits on John in one action, so the break can land between the two, and the second hit then lands without ×0.6. Shield Up's `activationTagQuery` is empty today (verified), so the block needs a new tag plus code to add and remove it. This needs EditMode tests for an area relay that crosses the break.

### 2. M2's press is always yes, and the house rule tests the opposite economy

- **Evidence.**
  - **The trade.** The counter is a free Fist Blitz: 8 + Focus damage (`MarkFactionRoleHandler.cs:88-102`). Under M2 it costs 1 Focus. The barrier table on `Unit_Mark.prefab` is 0/3/5/7/8/9, so one Focus is worth 1–3 HP of barrier and +1 damage. 8+ damage for 1–3 HP of barrier is always worth it.
  - **No reason to bank.** Focus also drops 2 per hit on Mark (`atmanFocusLostPerHit` 2). And the attacker that set off the counter has already used its turn: an enemy basic attack ends that enemy's turn (CR-6). So nothing argues for keeping Focus in reserve.
  - **The arm is automatic too.** Mark Blitzes every turn he can.
  - **The house rule.** "Press while Focus ≥ 1" can't simulate M2 at all. As built, the counter *earns* +1 Focus (it is his basic-attack preset; the handler raises `abilityPerformed`, `:100`; `AtmanFocus.cs:113-120`). So in the session Mark's Focus climbs with each counter, where under M2 it would fall by 1. That is a 2-Focus swing per counter in the wrong direction.
- **Change.** Either make the spend bite, or say plainly that Mark stays a free "instinct" role like Lucy (M1). Options that bite:
  - *"The counter spends all his Focus and adds it to the hit"*: a bet between a big counter now and barrier and damage on his own turn.
  - Cost 2 Focus, the lever's top value.

  For the session, the house rule has to subtract by hand: track Focus on paper, −1 per counter, ignoring the +1 the game adds.

### 3. The scenarios' decision counts don't survive a recheck

- **S1 (rechecked).** "Mark has nothing in reach (2,4 is 4 away, Blitz 2)" contradicts S3. In S3 Mark goes 3,1 → 3,3 (2 of his 3 move) and Blitzes 2,4 from there, and S1 has the same tiles and the same assumed move 3.
  - **The line the draft misses.** Linda shoots 2,4 once (10 → 4), then Mark moves and Blitzes it dead (8 ≥ 4). That kills 2,4 for sure, keeps Linda at 2 arrows (Watch armed under L2), gives Mark Focus 1 (counter armed under M2), and Mark steps into 2,4 (Fist Blitz rule). On the enemy turn 1,5 and 3,5 go for Mark. Any that ends on 2,5 or 2,3 is in Linda's north lane.
  - **This beats both of the draft's lines.** Linda takes 0 hits instead of 1, and 2 arrows are left instead of 1.
  - **The draft's ★ is weakly dominated by its own "spend" line.** In both, 2,4 dies before striking and 1,5 and 3,5 strike unanswered. The "freed AP" is never used in the ★ line. And ★ is worse if 2,4 ends on 3,3: also 2 steps and beside Mark, but not in the lane. That is THJ's kept-AP objection reproduced inside P. S1's real decision is Mark's move, not a role.
  - **The lane isn't a decision either.** West is ✗, north is the default.
- **S1 paths.** The Watch depends on two unstated assumptions: 2,4 breaks the 2,2 / 3,3 tie toward Linda, and 2,4 acts before 1,5. 1,5 can reach 2,2 in 4 steps too, and if it gets there first the Watch hits 1,5 (10 → 4, survives) instead.
- **S2.** The one press choice is indifferent (strongest objection). "Turn 2: Wrath 3 kills a Claw" is true at Wrath 1 too (8 × 1.35 = 10.8 ≥ 10), so the break changes nothing on turn 2 in Memory 3.
- **S3** holds as the draft's best case. In the 1-wide corridor (row 1 from x 5) the gauntlet must end in the east lane, so the Watch is close to certain whatever the move order. One slip: "1,5 reaches 2,3 and strikes him [Mark on 3,4]" can't happen. Claw attacks are Adjacent (`DarkClaw_Ability_Attack.asset` `cellApplyTraverseMode` 1; CR-15), and 2,3 is diagonal to 3,4. The Claw has to take 3,3 (4 steps, reachable), so the outcome stands but the grid arrow is wrong. Also, whether Mark's Blitz lands on 3,4 or on 2,3 is assumed. On 2,3 he stands in Linda's north column, and the North line changes.
- **Change.**
  - S1: correct Mark's reach, add the Mark-Blitz line, regrade, and count 1 decision there (Mark's), not 2.
  - S2: count 0 real press choices, unless one attacker hits harder, one sister is low, or the J2 change in point 1 applies.
  - S3: fix the 2,3 arrow.
  - All three: state the action order and tie-breaks for every Watch.

### 4. With no role sink, FTP stops binding, and Pass-by loses its reward

- **Evidence.**
  - **FTP's jobs under P.** Duos at 2 FTP with cooldown 2–3 (DU-1/2). Mark's Continuous Attack also still costs FTP (MA-2; D-216's "free" isn't built), so "FTP is the Duo meter only" isn't true with `requiredFTP` 0 alone.
  - **Income.** It keeps coming in: Shield Up +1 (which J1 makes a near-every-turn cast), Slam +1, Blink +1, Pass-by +1/+2, level fills.
  - **What binds instead.** Pools start full (River John+Lucy 8, Ridge 5: CR-10, onboarding F5). With roles at 0, a Duo's cooldown limits it before FTP does in most fights. FTP becomes a meter that's always full, and Pass-by's only payoff (FTP fill, `core-systems.md` "Pass-by") becomes a dead choice.
  - **THJ's stated direction.** That runs against his view that Duos come too much early and should be finishers.
  - **The session can't see it.** The house rule "+99 FTP" hides all of this.
- **Change.** In Step 2, set `requiredFTP` 0 on the four role components (data) instead of pressing L, so the FTP economy is real. Log FTP at fight end and Duos per fight. Bring DU-5 (Duo cost 3 if FTP ends fights above 4) into this plan's levers rather than leaving FTP's job to a later plan. Say what Pass-by fills if FTP is never short.

### 5. P weakens three roles and makes Lucy's stronger

- **Evidence.** Under P, John (gate + cap), Linda (one lane + L2) and Mark (Focus) all lose uses. Lucy loses her only limit: the 1 FTP per follow-up she pays today (prefab `requiredFTP` 1). FR-4's planned cap of 3 is cut as "never built". She then fires on every qualifying family hit within 3 of her, about 6 damage each (2 × 3), unlimited, on both turns. That is the "free reward competing with Synergies" THJ complained about, on the one hero left as an "instinct" role, in a game his pacing check calls too easy.
- **Change.** Keep FR-4's per-round cap of 3 on Lucy in the session (house rule: stop pressing after 3 a round), or test U3 Kindle alongside U1 rather than after. Read her follow-ups per fight and their share of damage from the combat log.

### 6. Linda: the default makes most boards automatic, and a corridor is a solved kill zone

- **Evidence.**
  - **The default.** Her bow shoots along her row or column only (GDD Linda), so "the direction of her last shot" always faces the enemy she shot. When that enemy comes at her, it usually ends in that lane. On a one-front board, the default *is* the answer (S1: west ✗).
  - **AI.** The enemy AI has no role-zone input (`UtilityVariables.cs` enum: distance, presence, path and attractiveness terms only). So on a 1-wide approach (the Ridge's row 1, Memory 1's throat, the Trailhead's 1-wide trail) every melee enemy going for her ends in the faced lane, every turn. Free roles plus pickup, Encore and the kill hand-back keep her refilling, and L2 is the only brake.
  - **Undefined default.** Explosive Crescendo targets any cell within 5, often diagonal, so "the direction of her last shot" has no answer for it.
  - **L2's trade is thin.** It's real only when her second AP buys something. Her 1-AP options are a move, Slam (cooldown 1) or Crescendo (cooldown 2), and in S1 the freed AP is unused.
- **Change.**
  - Define the default for a non-cardinal shot: dominant axis, ties to the previous facing.
  - Count the *two-front share* of Ridge/Trail fights when judging "facing changed at least once a fight".
  - Accept the corridor as the designed overwatch payoff, or flag C2-lite (one AI variable penalising ending in a drawn lane) as the lever if Watch in corridors reads as free.
  - Count Watch prompts per fight on corridor levels as well as on open ones.

## Per option

- **A (as built + Lucy preview):** ship the preview regardless. A alone leaves "just a click" untouched for all four.
- **C (kept AP):** don't ship. The withdrawal is right, and S1 shows the same domination survives inside L2.
- **P:** ship to the house-rule session **with changes**: J2's break blocks next turn's Shield Up, M2 with a cost that bites (or honest M1), Lucy capped in the session, real FTP (`requiredFTP` 0, not +99), and the scenarios regraded. As drafted, it tests legibility and will be judged on challenge.
- **P+ (THJ's full set):** not now. J3 (the swap) is the one item that gives the press a real cost (John leaves his post). If point 1's change doesn't make John's press a choice, J3 is the next thing to try, before minimum range or the ember pool.

## What would change my mind

- In the session, with real FTP, THJ declines a John guard or skips Shield Up at least once a fight *and says it was the right call*. Or Mark keeps Focus rather than countering at least once a fight. Either would show the presses are choices without my changes.
- FTP is under 4 at most fight ends with roles free, which would mean Duos still bind it.
- Lucy's follow-ups stay under about a fifth of family damage per fight when uncapped.
