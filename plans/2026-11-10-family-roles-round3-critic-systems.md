# Family Roles round 3: systems critique

Critic: `miso-design-critic`, lens **systems**. Target: the "Round 3" section of [`2026-11-09-family-roles-round2-design.md`](2026-11-09-family-roles-round2-design.md) (recommendation R3), plus THJ's two notes of 2026-11-10 00:51 and 00:52 (John's guard should be a stamina or posture limit that is damage-based and doesn't feed his attack; Lucy's reach plus "beside" is a double gate). Read 2026-11-10: round 3 in full, the round-2 systems critique, GDD (`combat-rules.md` CR-5/6/10–13/19–21/32, `family-systems.md` FR-1 to FR-13 and Duos, `enemies.md`, `characters/john|linda|lucy|mark.md`), `combat-balance.md`, `tech/core-systems.md`. Code, paths under `miso/Assets/_Project/`: `JohnFactionRoleHandler.cs`, `JohnPassiveAbility_Wrath.cs`, `JohnPassiveAbility_BloodDebt.cs`, `LindaFactionRoleHandler.cs`, `LucyFactionRoleHandler.cs`, `MarkFactionRoleHandler.cs`, `AEffectPusher.cs`, `AEffectDashAttack.cs`, `Projectile.cs`, `GlobalEventBus.cs`, `FactionRoleProvocationSuppression.cs`, `MasherCounterRules.cs`, the push assets of Vault and Shield Dash, the enemy attack effect assets, and `Unit_MasherGoblin.prefab`.

## Strongest point: John's press is close to dominant, and "the swaps limit themselves" doesn't hold

Round 3 makes position John's whole price. But on paper the price is close to zero, so pressing is the default answer and THJ's test fails for John.

- **Attackers that already struck are spent.** An enemy's basic attack ends its turn (CR-6). The child who lands on John's tile can only be hit by enemies that haven't acted yet, and those re-plan. The family then gets its own turn first, with 2 AP each, to step out.
- **S6, prompt 2, re-graded.** Pressing puts Linda on 6,1, between the Claws on 6,2 and 7,1, but both have already attacked this turn. The only enemy left, (1,4), now reaches John on 2,1 by walking 3 steps to 1,1, instead of reaching Linda.
  - **Pressed:** Linda takes 0, and John takes about 1 (the guard) plus about 2 (the direct hit, ×0.6).
  - **Declined (the draft's line):** Linda takes two hits of about 3 each, so about 6 of her 20.
  - **Her next turn after a press:** she shoots 6,2 at point blank, or Harmonic Slams both Claws (Crippled, then she steps away, +1 FTP).
  - So pressing is right, and the draft's "2 real presses" is really 3 automatic ones.
- **A bad landing is undone by the next swap.** If the child who landed is attacked next, the prompt comes up again, and pressing swaps John back. The landing cost only sticks when the next attack goes to someone else.
- **The press halves the damage on every hit.** Each press turns a hit H on a 15 or 20 HP sister into 0.5 H on John's 32 HP (0.3 H with Shield Up), at any range. HP persists between levels and attrition is the real pressure (`combat-balance.md`, playtest 2026-10-08). So "always press until John is low" is the strategy, and the decision only appears late in a mission.
- **Blood Debt in S6 is wrong.** Blood Debt goes to the last enemy to hurt another family member (`JohnPassiveAbility_BloodDebt.cs:73-77, 95-104`). After the declined prompts that is the Claw on 1,1 that hit Linda last, not the one beside John. Turn 2's "Sword ×2.05 on the Blood Debt Claw beside him" doesn't happen.

**Change:** adopt THJ's damage-based guard limit (point 1). Re-grade S6 with the press as the right answer. Drop "the swaps limit themselves" as the argument for having no limit.

## Points

### 1. John: free unlimited swapping needs a limit, and THJ's posture is the right shape

**Why a limit.** See above: HP is the only brake today, and it binds late. Two more ways the swap breaks:

- **Free movement across the board, on the family's turn too.** The handler relays enemy actions "on either side's turn" (`JohnFactionRoleHandler.cs:41-42`), and the Masher counters every hit (EN-2). So Lucy embers the Masher from 3 tiles, the Masher walks over and slams her, and John swaps in from anywhere. He ends up beside the Masher with both his AP left.
- **A swap is a "stop".** It wakes Unaware enemies around both tiles (EN-13). Whether it picks up Linda's arrows (LI-7) is to check.

**Scale, from the enemy assets** (raw hit = base factor × `Stat_DMG`, enemy faction ×1; tiers from CR-32):

| Enemy | Standard | Early ×0.75 | Tutorial ×0.5 |
|---|---|---|---|
| Dark Claw, Archer (`*_Attack_Effect_AttrMod` 6) | 6 | 4 (4.5, halves to even) | 3 |
| Masher (8, an area that hits both sides, counters every hit) | 8 | 6 | 4 |
| Shaman 8, Worm 8, Black Claw 10 | 8 / 8 / 10 | 6 / 6 / 8 (7.5) | 4 / 4 / 5 |
| Goblin Queen: strike 7.5 per member within 1 of the struck cell; charge 10 per member next to her path, plus a push | 7.5 / 10 | — (bosses are Standard) | — |
| Mountain Deev: pools 6 per tick, for 3 turns | 6 | — | — |

**Proposal.**

- **The pool.** Posture counts the *raw* hit, the number the threat preview shows. John has **12**, **18 with Shield Up** (this replaces Shield Up's Wrath job), refilled at the start of his turn.
- **The guard.** A guard is allowed while posture is above 0. The hit that takes it to 0 or below is still guarded, then posture breaks: no swaps until John's next turn.
- **What that gives at Standard:**
  - Claws: 2 guards (6, then 6 breaks it), or 3 with Shield Up.
  - Early: 3 guards (4, 4, 4), or 5 with Shield Up.
  - Tutorial: 4 guards, or 6 with Shield Up.
  - Queen: her charge (10) and the next hit break it, against 3 guards today. Boss hits break it; Tutorial pecks barely dent it, which is THJ's "small hits don't burn it".
- **What it costs John.** At most about 6 HP of guarded hits per enemy turn (12 × 0.5), or about 5.4 with Shield Up (18 × 0.3). That's sustainable on 32 HP over a 3-round fight, so he still guards most turns, but he can't absorb the whole turn: on a 4- or 5-hit turn the player picks which 2 or 3 to take. That makes the decision real.
- **The loop it ends.** It also ends the Masher loop of point 4: with 18 posture, the third counter of 8 breaks it.

**Wrath and Blood Debt under posture.**

- **Wrath goes.** THJ: a guard can't strengthen John's attack.
  - **What it removes:** at most +105% on one ability per turn. Under free unlimited swaps, Wrath 3 would have been every turn, Sword 16.4, or 21.3 on the Blood Debt target. Removing it cuts damage in a game the playtests call too easy, so it's a balance gain, not a loss.
  - **The kill it took with it:** Sword 8 plus Lucy's follow-up 6 is 14, short of a 16 HP Claw. Wrath used to close that gap (`combat-balance.md`, John changes of 2026-10-08).
  - **Reuse:** `WrathStacks` and `JohnWrathBadgeUI` can become the posture meter.
- **Blood Debt stays.** It already rewards *after* the danger, on John's turn, and it isn't tied to guarding. Blood Debt ×1.3 makes the Sword 10, and 10 plus 6 is 16, so it keeps the kill line Wrath gave. Fix one thing: on a guard it marks the *oldest* action in progress (`JohnPassiveAbility_BloodDebt.cs:85-87`, `inProgress[0]`), while John's handler deliberately uses the action that triggered him (`JohnFactionRoleHandler.cs:41-42`). Use the same action.
- **Revenge** (when a family member dies) is where his anger already lives.

**Rules count.** Posture adds 1 and Wrath removes 1, so it's still +4 −2. Cost: S–M on John's handler. The pre-reduction value of the hit has to be read at the trigger; `AbilityDamagePreview` computes it, to check.

### 2. Linda: on the family's turn, the cause clause is the as-built rule

- **Evidence.**
  - On the family's turn, every enemy that moves is moved by the family: the pushes from Vault and Shield Dash, Command, Toba's swap. The one exception is the Masher's counter walk, and it ends next to the family member it attacks, so the protection clause catches it anyway. So "a family member moved it" adds nothing on the player's turn: Watch fires exactly as built (D-322) on every incidental push.
  - Shield Dash pushes every enemy beside its path and its end cell. Vault pushes every enemy beside its landing, and when the tile straight away is blocked it **slides sideways** to the free neighbour farthest from Mark (`Mark_Ability_Attack_Vault_Effect_PusherEffect.asset`: `pushMode` 1, `dragStraightOnly` 0; `AEffectPusher.cs:70-80` picks the max distance among walkable 4-neighbours). So an enemy can slide into her lines that the player didn't aim there.
  - The brake on the player's turn is the quiver (3 arrows). The real decision is "press, or keep the arrow for a lined-up pierce", not "where her lines cross the setters' pushes". Pressing is usually right: a Watch arrow is a free action, while her own shot costs 1 AP and the same arrow.
  - Arrows passing an ally (the coordinator's check): allies don't block. The projectile only claims units that match its effect's faction (`Projectile.cs:483-485, 509-515`), and her trigger ignores units in between (`LindaFactionRoleHandler.cs:30-39`). S5 and S8 hold.
  - **But in S5, Mark lands 2 tiles up her column** (2,3). With Catch & Return bought (MA-3, `minTileDistance` 2), both of her arrows stop at Mark with a catch prompt. If the player presses it, neither reaches 2,5: no damage, and the arrow goes back to her quiver.
  - Code: `unitEndMoving` carries only the moved unit (`GlobalEventBus.cs:53`). The cause is still readable as the owner of the latest action in progress (`SessionLogs.ActionsInProgress`): Mark's Vault or his counter, an enemy's own walk. So no "last moved by" record is needed. S, not S–M.
- **Change.**
  - Say plainly that player-turn Linda is the as-built rule. Grade S5 as the setter's decision (Mark's Vault target) plus the quiver choice.
  - Add the catch case to S5, or move Mark off her column.
  - If incidental Watches from Shield Dash read as free, the lever is Watch on Mark's moves only, on the family's turn.

### 3. The Setter: pick "away from the victim", and the code then needs two changes

- **Evidence.**
  - **Where Mark lands.** Fist Blitz lands on the approach cell, `path[^2]` of his shortest path to the attacker (`AEffectDashAttack.cs:55-77`). So his landing is set by where he stands.
  - **Which way the push goes.** The pusher measures "away" only from the owner's cell (`AEffectPusher.cs:97-107`). `TryGetPushPreview` takes an override, but `ApplyUnguarded` doesn't. "Away from the victim" needs that option (core, S).
  - **When the far tile is taken.** Under "away from the victim", Mark coming from the far side lands on the push tile and blocks his own knockback. In S8, Mark at 5,1 or 4,0 would approach the attacker through 4,2.
  - **Blocked pushes.** "If the tile is blocked, it isn't moved (as other pushes do)" is true for Shield Dash (`dragStraightOnly` 1) but false for Vault's asset, which slides sideways (point 2). With the slide, the knockback can land beside another sibling or out of Linda's line.
  - **Gaps and hazards.** Push candidates are walkable cells only (`PathWalkable`), so there are no pushes into gaps or off the edge (no falls), and none into the Cyclone (it blocks walking). A walkable hazard can be entered.
  - **Immovable enemies.** The Masher and the Deev are Immovable (EN-3), so they get no knockback. The Queen isn't on the list; whether her 1 × 2 footprint can be pushed is to check.
  - **What the knockback can't do.** An enemy's basic attack ends its turn, so the knockback never saves anyone from *that* enemy. Its whole value is feeding Watch and setting up the next turn.
- **Change.**
  - The rule: away from the victim, with a straight push only (`dragStraightOnly` on, so a blocked tile means no knockback).
  - The landing: Fist Blitz's approach cell skips the push tile when another free neighbour exists.
  - S8: delete the last sentence ("north of the attacker … south"). Under this rule the knockback would still go east. Mark's decision is "within 2, and not behind the attacker"; the family's is "line up behind the victim".
  - Cost: S–M, as the draft says, but two core changes (the push reference, the landing choice), not one.

### 4. Roles free: the enemy-turn chain is the new free lunch, and the Masher can loop

- **Evidence.**
  - **What one hit sets off.** One enemy hit on a family member within 2 of Mark gives:
    - Mark: 8, plus 1 to 5 from Atman's Focus;
    - Watch: 6, if the attacker is knocked into her lines;
    - Lucy: 6, if the striker was beside her.
  - **What that does to Claws.** That's about 20 or more, so every Claw (16 HP, Standard and Early) that attacks the S8 formation dies on its own turn, before the family acts. John's swap halves the hit, too. The AI has no input for role zones (round-2 critique, `UtilityVariables.cs`), so Claws keep walking into it.
  - **What still limits it.** Only Linda's quiver. The caps of FR-4 (Mark 1 per round, Lucy 3) are planned, not built. FTP was the last brake, and R3 removes it.
  - **The Masher loop, on paper.**
    1. A Masher counter (or slam) hits a sibling, and John swaps in.
    2. Mark counters hits on John (`MarkFactionRoleHandler.cs` PrepareTargets: any ally other than Mark).
    3. Reactions provoke the Masher (`MasherCounterRules.cs:15`). `counterCanProvokeFamilyRoles` is 1 on `Unit_MasherGoblin.prefab:898`, and John's handler never checks `FactionRoleProvocationSuppression`.
    4. The Masher counters Mark, John swaps again, Mark counters again, and so on.
    5. The only stop is the hidden safety cap, `MasherChainCap.Max` 10 per root action (`MasherCounterRules.cs:59`). 10 Fist Blitzes at 8 or more is 80, the Masher's HP at Standard, with no AP spent, while John takes about 2 per loop with Shield Up.
    6. As built, FTP (2 per loop) stops this.
- **Change.**
  - Build FR-4's cap on Mark (once per enemy turn) and a cap on Lucy together with "roles free", not after.
  - John's posture (point 1) ends the loop.
  - Make the Masher's counter not provoke roles (`counterCanProvokeFamilyRoles` 0), or have John's handler check the suppression too.
  - In the session, log chained prompts per enemy turn, and enemies killed on their own turn.

### 5. Lucy: THJ is right about the double gate, but dropping the reach needs Papa's Shelter kept and a cap

- **Without the reach.** Her follow-up can land as far as the striker's reach plus 1 from her:

  | Striker's attack | Farthest target from Lucy |
  |---|---|
  | John's Sword | 2 |
  | Fist Blitz | 3 |
  | Vault | 5 (6 with Long Vault) |
  | Linda's bow | 5 (7 with Longshot) |
  | Explosive Crescendo | 7 |
  | Shield Dash | 5 to 8 |

  Each follow-up is 6 (2 embers × 3).
- **What that rewards.** The safest formation gets everything: both sisters at the back, Lucy beside Linda, following each shot and each Watch for free. Linda shoots up to 2 times a turn, quiver permitting. If Lucy stands beside two siblings, up to 4 strikes a turn qualify. With the quiver and no cap, that's about 12 free damage a turn, against her own 1-AP Fire Embers of 7 to 13.
- **Family Shelter makes it worse.** Shelter beside *anyone* points the same way as "beside": a Lucy who can follow at all is always Sheltered and a level up. Her position stops being a choice. Papa's Shelter as built (John only) is what makes "beside John, up front" compete with "beside Linda, at the back".
- **Code.** Recording the striker's tile at the start of the action follows the existing HP snapshot (`LucyFactionRoleHandler.cs`, `_hpAtActionStart` keyed by `ActionLogEntry`): S, as the draft says. Dropping the reach changes `GetCellsInRange`, which also drives her role zone (FR-10/11 hide it when it matches her attack reach). It would then be drawn from the striker, not from her.
- **Change.**
  - Drop the 3-tile reach (one gate: "beside her when they acted").
  - Keep Papa's Shelter for John only. Drop Family Shelter, or use the per-sibling gifts of Q4.
  - Cap follow-ups at 2 per round. The old model counted 2 reactions per hero per round (`combat-balance.md`, Model).

### 6. FTP's job, and two cost estimates that are low

- **FTP.** With roles free, FTP pays only for Duos (2 each; the check before use tests 1 per partner, DU-2) and Mark's Continuous Attack, which is planned to go free too (D-216).
  - The full family's maximum is 14. The pool starts full, carries over between levels, and the Duos' cooldowns of 2 to 3 bind before FTP does.
  - Pass-by's only payoff becomes a dead choice.
  - R3's tables never say this. The round-2 critique's point 4 still stands: DU-5 (Duo cost 3) is the lever, and logging FTP at fight end is the test.
- **John's swap: M, not "M, simpler".**
  - Area attacks: the Queen's strike hits every member within 1 of the struck cell, and the Masher's slam covers 2 × 2. Swap with whom when two are inside?
  - Moving attacks: the Queen's charge (`FamilyRoleRelay.MovesToTarget`, `keepCellTargets`) moves during the action, so when does the swap happen?
  - `RelayArea` answers these for the relay, not for a swap.
  - Add posture on top, and the estimate is M to M+.
- **Core claims.** They match `core-systems.md`: the role handlers and the `AEffect*` family, `AEffectSwapper` included, are core Tier 3. The Setter's two changes (point 3) are both core.

## Per option

- **A (as built):** a baseline only. It fails D-464 for Linda and Lucy.
- **R3:** ship to the session with changes:
  - John gets posture, and Wrath is removed (point 1);
  - the Setter's rule is fixed (point 3);
  - Mark and Lucy get caps alongside free roles (point 4);
  - Lucy's reach is dropped, with Papa's Shelter kept for John only (point 5);
  - S6 and S8 are re-graded.

  As drafted, John's press and the enemy-turn chain are both near-automatic.
- **Mark alternatives:** M-T (Tag-in) has none of the Setter's enemy-turn chain risk and is the fallback if the chain still reads as free with caps on.

## What would change my mind

- In play, with no posture, THJ declines a John swap at least once per fight *because of where the child would land*, and says it was right.
- With roles free and no caps, enemies killed on their own turn stay under about 1 per enemy turn on Claw levels (The Pile, the Ridge all-alert).
- With the reach dropped, Lucy's follow-ups stay under about a fifth of family damage per fight.
