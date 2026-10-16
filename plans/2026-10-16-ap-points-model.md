# AP and points model: Fixed vs Shared AP; how Family Roles and Duos are paid and limited

Size: L    Tier: 3    Assigned to: miso-game-designer
Branch: all (decided once for both branches; built on `thj/home-test` first. Today `thj/home-test` = FTP, `main` = ATB; both PerUnit AP)
Status: waiting on THJ (revision 4).
- Decided: Q1 roles free, limits only (D-036); Q3 Fixed AP (D-037); Q4 simple press now, graded QTE next (D-034); Q5 Bergson Time deferred (D-038); Q6 duo costs 2 FTP, checked properly (D-035).
- Open: Q2 (Linda) and Q7 (Fireside).

## Revision notes

**Revision 4 (2026-10-16).** THJ decided Q1 (D-036), Q3 (D-037) and Q5 (D-038). On Q2 he **rejected excluding pushes**: pushes and forced movement are the combos players feel they authored. He also said:
- the real cause is the rook-like trigger (her whole row and column, not blocked by units in the way);
- if any range limit applies, exclude the tiles next to her, so enemies coming to attack her aren't the target;
- without a solid alternative, cap her at a number with the same condition.

What changed:
- Covering Fire is withdrawn; its threat condition and push exclusion are gone.
- Five Linda options were evaluated concretely: excluding adjacent tiles, blocked lanes, shorter range, a plain cap, and combinations.
- **The recommendation is now "Watch Shots"**, a cap: her trigger is unchanged (pushes count), with 2 shots per round, each enemy at most once per round, and at most 1 of the 2 spent during your own turn.
- A brief critic pass on the Linda options ran (systems; creative and UX together).
- Q7 is re-confirmed for free, limited roles.

**Revision 3 (2026-10-16).** THJ's answers:
- Q4 decided: the role QTE stays a simple press now; the graded QTE comes next (**D-034**).
- Q6 decided: a duo costs 2 FTP, checked properly (**D-035**).
- Q1 open: "leaning towards 1". This is ambiguous: it can mean option (a) from revision 2 (roles free with charges) or "a role costs 1 FTP". Q1 below asks him to confirm.
- Q2 open: give every role a limit (a very high one for John is the same as none), but tests show only Linda over-triggering, and he thinks her trigger condition is the cause.

What changed:
- **Two concrete role designs compared**, plus a hybrid: **A** FTP pays 1 per role with a limit; **B** roles free with per-role limits, with Linda fixed through her trigger condition; **C** = B plus paid extra uses.
- **New section: why Linda fires so often**, from the code.
- **Recommendation is now B** ("Covering Fire"). Linda's fix moves from a quiver count to her trigger condition, and every role gets a real per-round limit field. **C is a lever** to measure after B, not part of the first build.
- A third critic pass ran (systems; creative and UX together).

**Revision 2 (2026-10-16).**
- ATB dropped as a leading option: playtesters found it confusing.
- Roles stop paying FTP; duos keep FTP.
- Bergson Time deferred.
- The decision moved to positioning, John's HP and duo spending.
- Second critic pass.

**Revision 1 (2026-10-16).** "A+": FTP pays roles, a once-per-round cap, Bergson Time on FTP. Dropped in revision 2 because a cost on roles adds counting, not choice, when the QTE makes everyone press.

## Why

The two branches run different combat resources (`branches.md`). The Home demo is written against FTP (`design/demo-spec.md`). The merge question "FTP or ATB?" is open (`status.md`). Pilot 1.

## Goal

One AP model and one rule for paying and limiting Family Roles and Duos. It should:
- be simple enough for players who found ATB confusing;
- fix Linda's dominance;
- give real decisions;
- keep the QTE everyone likes.

## Acceptance criteria

- [ ] THJ answers the open questions (Q1, Q2, Q3, Q5, Q7).
- [ ] Each answer is a `D-NNN` row, scope `all` (D-034 and D-035 already logged).
- [ ] The docs in "Docs to update" are changed.
- [ ] A coordinator tech plan exists before any code change.

## Scope

In: AP rule; role payment and limits; Linda's trigger; the role QTE's job (decided: simple press); Bergson Time; what the Home feeds.
Out: per-ability damage numbers, enemy balance, Sisters' Rivalry's cap (a follow-up), code.

## Touches

Systems:
- core: `FactionRoleHandlerBase`, `UnitsCooperationHandler`, `PointConsumer` / `FamilyTimePoints`, the `PlayerController` role prompt, `GlobalSettings.asset`;
- the four `*FactionRoleHandler`s (Linda's trigger);
- Home `HomeFiresidePayoff`.

USPs: Family Roles, Synergies, Duos, Home.
Docs: `design/demo-spec.md`, `glossary.md`, `branches.md`, `design/combat-balance.md`, `design/player-skill-trees.md`.

---

## Problem and evidence

**Root problem.** Family Roles create no decision: the prompt invites a press, a press always helps, and ignoring it is free, so roles are effectively automatic. Two needs are mixed together:
1. **Limiting how much roles do.** Only Linda is a problem in tests.
2. **Giving the player decisions about the family protecting itself.**

A resource on roles tried to do both and did neither well.

### Why Linda fires so often (verified in code, 2026-10-16)

| Condition | Linda | John, Mark, Lucy |
| --- | --- | --- |
| Trigger event | `OnUnitEndMoving` (`triggerEvents: 64`): **any enemy that ends any move** in her area | John: an action starts (`1`); Mark and Lucy: an action completes (`4`) |
| What must happen | Nothing else: the enemy doesn't have to threaten anyone | **An enemy attacks or hits an ally** (John, Mark), or **an ally acts on an enemy** (Lucy) |
| Area | Her straight lines (row and column), radius **4 × `Stat_RANGE`** (`Linda_Ability_FactionRole`, `straightDirectionCellsOnly: 1`, `allowRangedReach: 1`); Longshot adds range | Small radii around the unit |
| Phases | `activationPhase: -1` = player, ally and enemy phases | John, Lucy -1; Mark 4 (enemy only) |
| Forced moves | `AEffectPusher` raises `unitEndMoving`, so **pushes count** (e.g. enemies pushed into her lines on your own turn) | Not relevant |
| Cap | None (`oncePerPhase: 0`) | None |

So Linda's chances scale with *every enemy movement on the map*. Each enemy moves most turns, and her cross is up to 16+ tiles. The others scale with *enemy attacks on the family*, about one per enemy attack. That explains the 3 shots per enemy phase and her 46–72 % damage share, and why tests show only her over-triggering.

### Other code facts

- The role QTE is an opt-in: only a successful press runs the role and pays for it; ignoring is free (`PlayerController.ActivateFactionRole`). All role QTEs are `TimedPress`.
- `oncePerPhase` is a single bool. It resets on every faction's `turnEnded`, so it means "once per faction turn", not per round, and it can't count to 2 or track targets.
- Paying for roles:
  - The cost is paid *after* the role runs (`FactionControllerBase.ActivateFactionRole`).
  - `TryPlayFactionRole` doesn't check affordability.
  - `requiredFTP` is 1 on all four heroes today.
  - Only matters for designs that charge FTP (A, C).
- The duo cost bug (2 charged, checked as 1 per partner) is fixed by D-035.
- FTP:
  - Pool about 6 (3 heroes) / 9 (4 heroes). Starts full; small gain per new level.
  - Fed by pass-by tags, `fpFill` abilities, potions and Home dishes.
  - `UpdateCap` drops Home max bonuses on a death.
- Shared AP: `Closure` is a no-op; the AP→ATB conversion is a stub.
- Bergson Time: ATB-only.

### Playtests and notes

- THJ, 2026-10-16:
  - ATB too confusing for recent testers.
  - Everyone loves the QTE (the shift toward faster, action-like play), and nobody declines it.
  - L untested.
  - Only Linda over-triggers.
- `design/combat-balance.md`, 2026-10-08:
  - Still easy.
  - Linda 46–72 % of the damage; 3 role shots in one enemy phase.
  - Sisters' Rivalry chains.

## Options compared

### (a) AP

Fixed (2 each) vs Shared (pool 2/5/6/8, escalation [1,1,2,4]). Shared is unplayed:
- attacks don't end a hero's turn;
- no conversion;
- harder to read.

THJ's earlier leaning and every critic pass favour **Fixed**. Q3 asks him to confirm.

### (b) Role designs

| | **A: FTP pays 1 per role use, plus a per-role limit** | **B: roles free, per-role limits, Linda fixed by trigger ("Covering Fire")** (recommended) | **C: hybrid, B + paid extra uses** (lever after B) |
| --- | --- | --- | --- |
| Rule | Each role use costs 1 from the family pool; each role also has a uses-per-round number | No FTP on roles. Every role gets a uses-per-round field. Linda's trigger is narrowed (below) | As B. Once a role's free uses for the round are spent, a further trigger still prompts, costs 1 FP, and looks different (kitchen icon, other colour, hold to confirm) |
| Fixes Linda | Only by the cap and by draining FTP; her trigger stays as wide | At the source: she fires only when the family is threatened | As B |
| Decision | Weak: players press while they can pay; roles and duos compete through reflex | Positioning on your turn (who covers whom); John's HP; duo spending | B's decisions, plus one real priced decision at the moment roles run out: an extra use now or a duo later |
| Feel (creative) | Protection becomes a purchase ("a father shielding his daughter is a transaction") | Linda becomes "a mother watching over her children", not a turret | Strongest Home link if the prompt carries family flavour ("from Mary's kitchen") |
| Readability (UX) | Two things to count; a missing prompt reads as "out of FTP" | Pips per role; John shows none | Free and paid prompts must look clearly different, or players drain the duo budget by reflex |
| Home | Spirited dishes (Tea, Pie) pay roles and duos; Fireside works | Spirited dishes pay duos; Fireside "first Family Role free" needs a replacement | Spirited dishes pay duos and extra uses; Fireside works again (first extra use free) |
| Build | Data (`requiredFTP` already 1) + a real per-round counter + pay-before-effect fix + affordability check in `TryPlayFactionRole` | `requiredFTP` 0; a per-round counter per role (replaces the `oncePerPhase` bool); Linda's trigger change in `LindaFactionRoleHandler` (+ a per-target set); pips; prompt text | B + the FTP fixes from A + a distinct paid prompt |
| Critics (round 3) | Don't ship (all) | Ship with changes (all) | Ship only after B is measured, priced against a duo, with a distinct hold-to-confirm prompt |

### Linda, revision 4: options evaluated (replaces Covering Fire below)

Facts that matter here (verified):
- `LindaFactionRoleHandler.GetCellsInRange` takes every grid cell within footprint distance radius (4 × `Stat_RANGE`) on her row or column, **with no occupancy check**. So her lanes go straight through units (THJ's "rook covering the board with penetration"). A 1×1 Linda watches up to 16 cells.
- Pushes raise `unitEndMoving` and count; per THJ they must keep counting.
- The base condition already skips her when the last action targeted her. So an enemy that attacks her doesn't trigger her (systems critic; consistent with `FactionRoleHandlerBase.CheckTriggerConditions`).
- `ApplyFactionRolesIfPossible` gives the event to the first feasible "Immediately" role. Linda uses `WaitForProcessesToComplete`, so this pre-emption is minor for her.

| Option | What it does to her triggers | Fiction | Readability | Verdict |
| --- | --- | --- | --- | --- |
| **Exclude adjacent tiles** (distance 1) | Removes 4 of ~16 cells. Stops melee enemies that end next to her. Ranged enemies stopping 2–4 tiles away, and anything walking through her lanes, still trigger. It also blocks a push that lands an enemy next to her, the first combo players try | Fits ("too close to draw"; she relies on John and Mark up close) | One more invisible reason for "she didn't fire" | Small effect; conflicts with "pushes count". Optional add-on (Q2 option c), not the fix |
| **Blocked lanes** (stop at the first unit) | Fewer triggers on crowded boards, none fewer on open ones. John and Mark standing in front of her block her own lanes | Archer-like | Players must trace lanes on every push preview; pushed enemies often land behind another unit, so combos silently break | Rejected by both critics |
| **Shorter range** (3 × `Stat_RANGE`) | 16 → 12 cells; still uncapped, so 3+ shots per phase on busy boards. Devalues Longshot | Neutral | Simple | Shrinks the area, not the count. Rejected |
| **Plain cap N per round, each enemy once** | Directly limits the count. N = 2 halves the observed 3+ per enemy phase; once per enemy stops one enemy shuffling, or being pushed twice, from eating both | Neutral (a watchful archer with two ready arrows) | Two pips on Linda | THJ's fallback; works |
| **Cap 2 with at most 1 on your own turn** (recommended) | As the cap, but a push combo on your turn can use only 1 shot, so at least 1 is always left for the enemy phase | Watches over the family on the enemy turn *and* plays in your combos | Two pips; the second greys "for the enemy turn" during your turn | Systems critic's fix for the "burn both on your own turn" failure |

Why the split: with one shared pool, a shot on your own turn is certain and a shot saved for the enemy phase may never come. Players would spend both on push combos, and her watching role would vanish (systems critic). The creative critic raised the same tension from the other side: one shared pool makes players avoid the combo they authored. Splitting 1 + 1 keeps both.

Known limitation (accepted): in the enemy phase the shots go to the first enemies that trigger her, not to the most dangerous one. The player can hold fire by ignoring the prompt, and the prompt shows "Watch Shot 1 of 2" so that's a visible choice. Choosing the most threatening target automatically would need deferred resolution, a bigger change, kept out.

Implementation:
- A per-round int and a per-enemy set on the role, cleared at the player turn start. **Not** the `oncePerPhase` bool, which resets on every faction's turn end.
- A "player-turn shots used" count capped at 1.
- If adjacent tiles are excluded (option c), use footprint distance, so a wider unit doesn't leak.

Minimum HUD:
- Two arrow pips on Linda's portrait and over her unit; the second shows "enemy turn" during your turn.
- A "Linda fires" marker on the landing tile in the push preview, when a shot is available.
- Her lane overlay on hover.

Likeliest misread: "I pushed into her lane and she didn't fire". The cause is a used shot, the per-enemy rule, or the 1-per-own-turn rule; the pips and the push-preview marker answer it.

### Linda's "Covering Fire" trigger (revision 3, withdrawn in revision 4)

Start values; each line is its own lever:
1. **Threat condition.** She fires only at an enemy that ends its move **next to a family member** (within 1 tile). This matches the other three roles: all four react to the family being threatened.
2. **Each enemy at most once per round** (a per-target set, cleared at the start of the player turn).
3. **Voluntary moves only.** Pushes and other forced moves don't trigger her. This stops "push enemies into her lane" farming, but it also removes any combo that relies on it (see Q2).
4. **Free uses per round: 2.**
5. **Phases: enemy phase only?** This is Q2's sub-option. With 1–3 in place her own-turn triggers mostly vanish anyway.

Range stays 4 × `Stat_RANGE`, so Longshot keeps its value. If she stays above about 40 % of damage after 1–4, lower her role damage, not the trigger.

Bait risk (systems critic): players can park John next to the enemy path so that Linda fires. That is positioning to protect the family, which is the decision we want, so it's acceptable as long as each enemy triggers her only once.

### Per-role limits (B)

One field on every role, "uses per round", refilled at the start of the player turn (a real round counter, not the per-faction-turn bool):

| Role | Start value | Why |
| --- | --- | --- |
| Linda | 2 per round, each enemy once, at most 1 on your own turn; trigger unchanged (revision 4) | The only one over-triggering |
| Lucy | 2 | Tests don't show over-triggering; the field exists to tune later |
| Mark | 2 | Same |
| John | Unlimited (no pips shown); his cost is his HP | THJ: a very high limit "would be the same as nothing". The prompt shows his HP cost; a guard stops it from downing him |

## Where the decision comes from (B)

1. **Positioning on your turn.** Where each Bergson ends the turn decides who covers whom. Under Covering Fire this matters for Linda too: her shots go where the family stands. This is the main decision. A later step adds coverage tiles to the move preview.
2. **John pays with his HP.** "John takes 4: 9 → 5 HP" on the prompt; declining at low HP is a real choice.
3. **Duos.** The family bar is a mission-long budget spent on your turn, with full information.
4. **C, if added:** the only enemy-turn prompt that needs thought is the paid one.
5. **The graded QTE (D-034, next)** adds skill, not choice.

## Lens notes (revision 3)

**Creative.**
- Target: *on my turn I place the family to cover each other, and on the enemy turn it pays off. Linda's arrow lands the moment a Claw steps up to Lucy, because Linda was watching her.*
- All four roles now share one fiction: when the family is threatened, someone answers.
- C's priced extra ("Mary's kitchen lets Linda loose one more") is the strongest Home-to-battle link, but only with that flavour.

**Systems.**
- The essential B work is a real round counter per role, a per-target set for Linda, and excluding forced moves.
- C prices a small per-hit effect in mission-long currency against duos at 2. Data first: if players always buy, the pool is gone by Level 3; if never, it's dead. Price it or drop it.

**UX.**
- Minimum HUD for B:
  - pips under each portrait for free uses left, none for John;
  - the prompt names the role and its stakes;
  - a small ring on an enemy Linda already shot this round;
  - the family bar labelled as paying duos, with the duo cost marked.
- Likeliest misread under B: an enemy steps into her lane far from the family, no prompt appears, and the player thinks she's broken. The prompt text and the Home Guide line "Linda covers family members within reach" address that.
- Under C: a reflex press on a paid prompt, so it needs hold-to-confirm and a distinct look.

## USP check

- **Family Roles:** strengthened. All four roles are now reactions to a threatened family member, with in-character limits.
- **Synergies:** neutral. Pass-by still feeds the bar. Push-into-Linda combos keep working (revision 4), limited to 1 shot on your own turn.
- **Duos:** strengthened. They're the main thing the family bar buys (D-035).
- **Home:** neutral under B (Spirited dishes pay duos; Fireside needs a new payoff). Strengthened under C (the kitchen pays for extra protection).

## Dropping ATB, and the Home demo

- **Lost:**
  - Bergson Time as built;
  - the "hold AP for the gauge" choice;
  - per-hero gauges;
  - the Mark–Linda race's +1 ATB (becomes +1 FTP);
  - the Mark ATB-floor run upgrade (retire or rework).
  - On `main`, Family Time / Family Lookout could return.
- **Home:**
  - Swift (Quickberry Tart +1 AP turn 1) unchanged under Fixed AP.
  - Spirited (Tea +2 max FTP, Pie +1, FTP rations) unchanged in rules.
  - The Demo Spec's "if ATB wins, swap" assumption goes.
  - Fireside: Q7.
  - Home max-FTP bonuses should survive deaths (`UpdateCap` fix).

## The QTE pillar

- Decided (D-034): simple press now, graded QTE next (a press always fires; in the window gives a bonus, start ×1.25).
- A harder press as a gate was rejected by every critic pass: a miss reads as a family member failing to protect another.
- Bergson Time: defer (Q5).

## Implementation (B)

1. **Data:**
   - `requiredFTP` 0 on the four role prefabs;
   - uses-per-round values;
   - the Fireside replacement.
2. **Core:**
   - a per-role round counter refilled at the player turn start (replaces the `oncePerPhase` bool);
   - Linda's Covering Fire in `LindaFactionRoleHandler` (threat check, per-target set, voluntary moves only);
   - John guard;
   - duo check (D-035);
   - `UpdateCap` keeps Home bonuses.
3. **UX:** pips, prompt text, Linda's shot ring, bar label.
4. **Later:**
   - C (after B is measured);
   - the graded QTE;
   - coverage tiles in the move preview;
   - race reward → FTP.

Steps 1–2 alone test the Linda fix. Risk medium-low; all Tier 3.

## Critics

**Round 1** (revision 1, turn income):
- Income dropped (creative, systems).
- Cap leak, duo bug and Home-bonus loss verified (systems).
- "No opt-out" rejected; the QTE is the opt-in.
- Pips and stake labels needed (UX).

**Round 2** (revision 2, P1–P4):
- P1 (FTP on roles) and P3 (hard gate) rejected by all.
- P2 shipped with changes: John's decline, pips, one rhythm, bar label, FTP-surplus levers.
- A quiver choice is a guess without enemy move order.

**Round 3** (this revision; read-only agents with the `miso-design-critic` instructions):

| Critic | Strongest point | What I did |
| --- | --- | --- |
| Systems | No design makes the free press a choice; a cap of N means "fires N times". Only C's paid extra adds a real decision. **The behaviour-changing lever is B's trigger**, not caps or FTP | Accepted. B leads with the trigger; caps are a tuning field; C is the decision lever after measurement |
| Systems | `oncePerPhase` can't do "2 per round"; it resets per faction turn and Linda is active in every phase | Accepted: a real round counter and a per-target set are in B |
| Systems | FTP is paid after the effect and `TryPlayFactionRole` skips the check | Recorded: only needed if A or C ships |
| Systems | Covering Fire can be farmed with pushes and bait | Accepted for pushes (excluded); bait accepted as intended positioning |
| Systems | C's price doesn't compare with a duo; it will be always or never | Accepted: C waits for data and must be priced against a duo |
| Creative | A turns protection into a purchase | Accepted: A not recommended |
| Creative | Covering Fire is the right fiction; keep it whatever else is decided | Kept |
| UX | Under C, free and paid prompts look alike, so players drain the duo budget by reflex | Accepted: hold-to-confirm, distinct look, kitchen icon |
| UX | John's cap is noise | Accepted: no pips for John |

**Round 4** (Linda options only; read-only agents with the critic instructions):

| Critic | Strongest point | What I did |
| --- | --- | --- |
| Systems | Excluding adjacent tiles removes only 4 cells; the cap is what cuts output. One shared pool makes players burn both shots on certain own-turn combos, so her watch disappears. Suggested N = 2, at most 1 on the player's turn, with a separate per-round int and per-enemy set | **Accepted**: this is the recommendation |
| Systems | Adjacent exclusion blocks a push landing next to her, contradicting "pushes count"; it must use footprint distance | Accepted: adjacency becomes an optional add-on (Q2 c) |
| Systems / UX | Blocked lanes make John and Mark block her and silently break push combos | Accepted: rejected |
| Systems / UX | Shorter range without a cap still gives 3+ shots per phase | Accepted: rejected |
| Creative | First-come shots go to whoever moves first, not to the enemy closing on Lucy, so it's an ammo counter, not a protector | Partly: accepted as a limitation; holding fire (ignoring the prompt with "1 of 2" shown) is the player's tool. Threat priority needs deferred resolution, kept out |
| UX | "I pushed into her lane and she didn't fire" will read as a bug | Accepted: pips over Linda and a "Linda fires" marker in the push preview |

What I kept against a critic: the creative critic says no design makes declining meaningful without enemy intent shown. I accept that for the enemy-turn press and place the decisions elsewhere (positioning, John, duos). Showing enemy intent (Into the Breach style) is a bigger feature, outside this plan.

## Recommendation

**Fixed AP (D-037) + roles free with limits (D-036) + Linda's "Watch Shots"**, scope `all`; on merge, `main` moves from ATB to FTP. In short:
- roles cost no FTP;
- every role has a uses-per-round field (Linda 2, Lucy 2, Mark 2, John unlimited and paid with HP);
- Linda keeps her trigger (pushes count), with 2 shots per round, each enemy at most once per round, and at most 1 on your own turn;
- duos cost 2 FTP (D-035);
- the simple-press QTE stays, with a prompt that names the stakes (D-034);
- Bergson Time deferred;
- C (paid extra uses) is measured after B.

**Playtest signal** (a Home sortie plus the Warren):
- **Worked:**
  - Linda 30–40 % of damage;
  - the four roles fire at similar rates;
  - testers position to protect, out loud;
  - John is declined at least once at low HP;
  - FTP at fight end is 0–3;
  - the QTE is still enjoyed.
- **Failed:**
  - "Linda's role is broken" (she fires too rarely: widen the threat to 2 tiles);
  - Linda still above 40 % (lower her damage);
  - a duo every turn with FTP above 4 (consider C, or remove the level-start gain).
- Add combat-log lines: role fired / declined, uses left, FP spent/gained.

## Questions for THJ

Decided:
- Q1: roles free, limits only (D-036).
- Q3: Fixed AP (D-037).
- Q4: simple press now, graded QTE next (D-034).
- Q5: Bergson Time deferred (D-038).
- Q6: duo costs 2 FTP, checked properly (D-035).

**Q2. How is Linda limited?**
- Context:
  - Her trigger is any enemy ending any move (pushes included) in her row or column up to 4 × `Stat_RANGE`, through units, in every phase, uncapped.
  - That's why only she over-triggers (46–72 % of damage).
  - Pushes keep counting (your call).
  - Every option uses a real per-round counter and a per-enemy set, cleared at your turn start.
- Options:
  - **(a)** 2 shots per round, each enemy once, at most 1 of them on your own turn, so 1 is always left for the enemy phase; trigger unchanged (recommended).
  - **(b)** 2 shots per round, each enemy once, one shared pool (your plain cap). Simplest, but players will likely spend both on certain own-turn push combos and her enemy-turn watch disappears.
  - **(c)** (a) plus no shots at enemies on the 4 tiles next to her ("too close to draw"). Small effect (4 of about 16 cells); also blocks pushes that land an enemy next to her.
  - **(d)** 3 shots per round, each enemy once, at most 1 on your turn. A looser cap if 2 makes her feel weak.
- Recommendation: (a). The cap cuts her count where it matters. The split keeps both her push combos and her watching role. The trigger stays as players know it. Blocked lanes and a shorter range were evaluated and rejected: blocked lanes make John and Mark block her own shots and silently break push combos; a shorter range without a cap still gives 3+ shots on busy boards.
- Blocked meanwhile: the Linda build step and the other roles' limit values. Not blocked: the role cost change (D-036), the duo fix (D-035), Home presentation.

**Q7. What replaces the Fireside "first Family Role free" payoff?**
- Context: roles are now free (D-036), so "first role free" does nothing. It is one of the three Fireside payoffs a pair can earn for the next sortie. The Home → roles link is the one players feel most.
- Options:
  - **(a)** Each of the pair gets +1 role use in the sortie's first round (Linda a third watch shot), and John's first redirect takes no damage, since his uses are unlimited (recommended). Data plus a small hook on the new per-round counter.
  - **(b)** Their first duo together is free. It already exists as a payoff, so the pair's three options would shrink to two.
  - **(c)** Drop it, keeping two payoffs: first duo free, FP cap +2. No work; less variety.
- Recommendation: (a). It keeps the Home feeding the roles, uses the new limit field, and gives John something meaningful.
- Blocked meanwhile: the Home data step (`HomeFiresidePayoff`) and the Demo Spec's Fireside line.

## Docs to update if approved

- `design/demo-spec.md` (coordinator):
  - remove "if ATB wins";
  - FTP pays duos (and extra uses if C);
  - Fireside list;
  - Home bonuses survive deaths.
- `glossary.md` (narrative):
  - Family Role (free, uses per round, the "family threatened" trigger);
  - FTP (pays Duos);
  - a name for Linda's Covering Fire;
  - Bergson Time deferred.
- `branches.md`: the resource line; close the merge question.
- `design/combat-balance.md` (me): role limits; Linda's trigger; the Linda lever applied.
- `design/player-skill-trees.md` (me): Longshot still extends her cover; Family Time / Lookout.
- `decisions.md`: D-034 and D-035 already logged; one row per answer.
- Follow-ups for `status.md`:
  - Sisters' Rivalry cap;
  - combat-log lines;
  - the role silently skipped when another QTE is active;
  - the race reward and the ATB-floor upgrade;
  - showing enemy intent (a larger feature, for later).

## Risks

- No head-to-head playtest yet: staged rollout plus the signal above.
- Tier 3 core edits before the merge: build once on `thj/home-test` and carry it over.

## Gates

Compile / tests / review: in the tech plan. Play check: yes (THJ's time). Docs: as listed above.
