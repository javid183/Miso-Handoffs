# Masher Goblin: reckless tank (counter-attack rework)

Size: M    Tier: 3 (Masher handler is a core system; changes an enemy rule)    Assigned to: miso-game-designer
Branch: all (work on `main`)
Status: waiting on THJ

## Why

THJ wants the Masher to bring its own challenge to a level: hit it and it comes for you. Today its answer is the same area slam it uses on its own turn, so it hits bystanders and its own goblins, it answers from too far, it answers Family Roles (which can chain), and it shuffles toward attackers it can't reach. The root problem is that **the counter has no rule of its own**: it borrows the own-turn slam and the generic damage event, so who provokes it, whom it hits and how far it reaches are all side effects. The design below gives the counter its own small, readable rule set. Request: coordinator task of 2026-10-20 (THJ's four points, quoted under "Problem and evidence").

## Goal

The Masher answers the family member who hurt it, one blow, only when it can reach them in a step, so the player can lure it, bait it with a sturdy member and stay out of its reach with the others.

## Problem and evidence

**THJ's four points:** (1) the counter is an area slam that can hit several targets; it should hit only its attacker. (2) It hurts other enemies; not wanted. (3) It should happen only on the player's turn. (4) It must be adjacent to the attacker to hit, and must not counter when it can't reach. Goal: "a really reckless tank, challenging, but one the player can strategize around: move it around (lure it) and avoid getting hit."

### What is built today (verified in code and data unless marked)

| Aspect | Today | Source |
| --- | --- | --- |
| Trigger | Any `onUnitDamageDone` on the Masher from an ability whose owner is alive and not downed, if the hit was not lethal and the Masher's own controller is not mid-action and it is not turn-skipped (Stunned) | `MasherGoblinFactionRoleHandler.cs:70-81` |
| What counts as a hit | `onUnitDamageDone` is raised only for abilities that complete, only when the owner's faction is hostile to the target, and only for HP loss | `CombatLevelRunHandler.cs:774-799` |
| Which turn | Not gated by turn. During the enemy turn the AI controller is usually mid-action (`isActionInProgress`, `FactionControllerBase.cs:72`), which blocks most enemy-turn counters by accident, not by rule. Mark's role fires only on the enemy phase (`Unit_Mark.prefab` `activationPhase: 4`), so it is usually blocked too | `:77` |
| Reactions provoke it | Yes. Lucy's embers (`OnActionComplete`, every phase), Linda's role arrow (`OnUnitEndMoving`, every phase) and Mark's Continuous Attack hits all count. Linda's arrow can loop: the counter step ends in her lane, she shoots, it counters again | role prefabs `triggerEvents`/`activationPhase`; GDD `combat-balance.md:96` |
| Duos provoke it | Probably not: duo partner abilities are silent and raise no bus events (`tech/combat-log.md:275`), so their damage likely never reaches `onUnitDamageDone`. *Assumed, to check in play* | |
| Counter attack | The Masher's basic attack `MasherGoblin_Ability_Attack` (`Unit.DefaultOccupiedCellAbility`, `:57`): radius 1, Adjacent (4 directions), from every footprint tile. It spawns `AOE_Attack _MasherGoblin_Variant`, whose `MasherGoblin_Ability_CompoundEffect` hits the struck tile plus its 4 neighbours (`applyMode` Surrounding, radius 1, `includeCentralCell`), **any faction** (`targetFactionRelation: -1`), 10 × `Stat_DMG` (`..._Attack_Effect_AttrMod`) | presets in `Resources/UnitSpecific/Enemy/Masher Goblin/Attack/` |
| Reach | It picks any tile in its attack range whose plus-shaped splash covers the attacker (`TryPickAttackCell`, `:181-201`), so it can hit an attacker 2 tiles from its footprint without moving, and 3 after a step | `:203-226` |
| Movement budget | Its normal walk, `MasherGoblin_Ability_Walk`: radius = 1 × `Stat_SPD` (×1 for enemies) = **1 tile**, path-walkable, through allies (`ignoreRelationOnWalk: 1`), whole 2 × 2 footprint must fit | `Walk.asset:59-62, 99`; `:296-342` |
| Unreachable | It still steps to the tile that brings it closest, then does nothing (`TryFindApproachCell` keeps a non-attacking cell that reduces distance, `:320-329`; `Activate` walks, then `Attack` finds no cell, `:139-146`) | |
| Crippled | The walk preset is blocked by Crippled (`activationTagQuery` Status.Crippled), but the counter calls the walk directly and never checks it, so a Crippled Masher may still step. *To check in play* | `Walk.asset:23-28`; `:161` |
| Cost | Free: no AP, no FTP (AI controllers don't pay, `FactionControllerBase.cs:199`); it resets both cooldowns after (`:131-134`) | |
| Limit per turn | None. `oncePerPhase: 0` on the prefab, and the handler never reads it | `Unit_MasherGoblin.prefab:813` |
| Two components (Q2) | The prefab has two handlers: one on the root (`-4332957646936667060`, `ability` empty) and one added to a child object (`8123456789123456791`, hand-made id, `ability` = Attack preset). Only the root's is ever started: the orchestrator calls `_owner.GetComponent<FactionRoleHandlerBase>()` on the unit root (`AbilityOrchestrator.cs:50, 63`), and the handler subscribes only in `Initialize`. So it **cannot** counter twice; the child is dead weight. The root's empty `ability` is why the "did not initialize its role ability" warning shows | `Unit_MasherGoblin.prefab:745-1017`; `FactionRoleHandlerBase.cs:80-82, 175-185` |
| Own turn | AI uses the same slam (move 1, then slam; the attack costs all AP left) | `Attack.asset:57` (`Closure`) |
| Preview | Hovering the Masher while aiming a non-move ability shows the ghost at its step tile, the step path, every tile of the splash, and the damage on the attacker; nothing if the hit is lethal. It measures from the attacker's **current** tile | `:367-426` |
| Statuses | `EntityState.Unable to Swap`, `EntityState.Unmovable` (shown "Immovable"), `Status.Reckless` | `Unit_MasherGoblin.prefab:240-250` |

Evidence the current state is a problem: THJ's points; `combat-balance.md` lists "first Masher counter loop" to watch and "decide on the Masher counter limit" as open; Enemies Q2.

## Options compared

All four options share the **base rules** that answer THJ's points directly:
- **Who provokes:** on the family's turn only, damage from **the ability the player chose for the acting member** (its own hits and projectiles, e.g. Tempest Bloom copies of Linda's arrow). Not Family Roles, not Synergy hits owned by another member (Shield Flare copies are John's, so Lucy's fireball that sets them off is answered only for its own hit), not burn, not anything on the enemies' turn. (Duos: see Q2 for THJ.)
- **When:** once, **after the acting member's whole action ends** (follow-ups included), measured from the tile the member ends on. One action, at most one answer.
- **Whom it hits:** that member only, one blow, single tile. No splash; no goblin is hurt.
- **Reach:** it may take one step (its normal move, 1 tile, the whole 2 × 2 must fit on a free path) to stand next to the member (four directions, from any of its tiles). If no such spot exists, no hit (whether it still steps is Q4).
- **Crippled:** no step (answers only if already next to the member). **Stunned:** no answer.

| | A. Reckless (base rules, no limit) | B. Grudge (base + once per member per turn) | C. Winded (base + each answer costs it 1 AP next turn) | D. Lumber (base, but it steps toward you even when it can't reach) |
| --- | --- | --- | --- | --- |
| How it feels | It answers every time it can reach. Each poke from 2 tiles drags it a step: luring costs HP. Melee members pay for every swing | Each member pays once per turn, then swings freely. Reads as "it remembers who hit it", less reckless | Baiting it is rewarded: two answers and it stands winded on its turn. Strong lure economy, but the tank gets easier the more you poke it | Ranged members pull it from anywhere for free; the "safe ring" rule blurs |
| How the player plays around it | Kill it from 3+ tiles (Linda, Lucy), use Duos, put John next to the melee striker so his role takes the answer at half, cripple it, pin it in a corridor where its 2 × 2 can't step | Same, plus "spread the first hits across members"; second swings are free, so Mark's Continuous Attack becomes the obvious answer | Poke it twice with John every turn and it never acts: a likely dominant strategy | Kite it with Linda forever; it never reaches anyone |
| Rules complexity | Low: one rule, matches the Shift danger zone | Low-medium: a hidden per-member counter the player must track | Medium: a new status (Winded) and AP debt across turns | Low, but two outcomes for "out of reach" |
| Build cost (rough) | M: handler gating and reach, new single-target counter preset, slam relation change, preview fixes, prefab cleanup, tests | A + small per-member set reset at turn start | A + AP debt on the enemy's next turn (touches AP, a core system) + status + UI | A minus the "no step" change (closest to today) |
| Risk | Melee members may avoid it entirely if the answer hurts too much (lever: counter damage) | Hidden state is the likeliest misread ("why didn't it answer?") | Trivialises the Masher; core AP change | Unlimited range pulls let ranged members drag it anywhere (it gets *closer*, so more dangerous, not less, but the pull is free at any range). A bounded version is Q4 (c) |
| USP effect | Roles: John's relay becomes the key answer; Linda's Harmonic Slam cripple matters. Duos: the safe way in (if THJ agrees) | Same as A, weaker | Neutral | Neutral |

**Leaning: A.** It is THJ's four points as one rule, the identity ("reckless") is intact, and its reach equals what the Shift danger zone already draws. B is the lever if playtests show melee members simply won't touch it.

### Cross-cutting choices inside A

| Choice | Recommended | Alternative | Why |
| --- | --- | --- | --- |
| Step distance | Its normal move: 1 tile | A "charge" of 2 | With 1, the counter zone is exactly the Shift danger zone (move range + adjacent attack, no splash: CR-43), so no new preview is needed. 2 would put Lucy (range 3) in reach at her max range and leave only Linda safe |
| Counter damage | **7 ×** `Stat_DMG` (7 on Standard, 5 on Early, 4 on Tutorial; 4 through John's relay) | 10 × (the slam's value) | With no limit, a member who swings twice eats two answers; at 10 that makes melee a pure tax (critic, accepted). 7 reads as a quick answer next to the 10 × slam |
| Off-reach pull (Q4) | **Lumber at the edge:** an attacker exactly one tile outside its reach (3 tiles from its footprint) makes it step 1 toward them, no hit | No step at all | Gives the ranged members a free, readable lure (Lucy at her max range 3 pulls it into her own danger zone: a real choice); Linda at 4 stays out of it. Still no hit without reach (point 4) |
| Own-turn slam | Keeps its plus-shaped splash, 10 ×, but hits the **family only** | Make it single-target too | THJ's point 2 is about goblins being hurt. The splash is the Masher's big telegraphed blow and punishes the family for bunching; the counter is the quick answer. Two blows, two jobs |
| Family Roles provoke? | No | Yes | Roles fire without a choice. If Lucy's embers provoked it, it would walk to Lucy after the player swung with John (misread), and Linda's lane arrow would loop. "Roles chip it safely" is a USP plus |
| Duos provoke? | No (THJ's call, Q2) | Yes, against the activator | Likely already true in code; "it can't answer the family acting together" is a clean Duo moment. Duos are capped by FTP and cooldown 2, so not a free kill |
| Allied AI units (Toba as an ally, the Deer) | Don't provoke (not the family's turn) | | Follows point 3 |
| Mark's Continuous Attack follow-ups | Part of Mark's action: the answer comes once, after the chain ends | Answer each follow-up | MA-2 swings again only after a kill and auto-targets the lowest-health enemy, so Mark doesn't choose the follow-up (critic, checked in `characters/mark.md`); answering mid-chain would also interleave with its QTE |

## Lens notes

**Creative.** Target experience: the Masher is a wall of muscle that the family has to *handle*, not just hit. Every swing at it is a decision: who takes the answer, and where will it stand afterwards? The moment I'm designing for: Mark lands a blow, the Masher lumbers one step and raises its club, John's shield prompt flashes, John steps in and eats half of it; next turn the family has walked the brute one tile at a time into Linda's lane. That is family against brute force, warmth against dread. The genre default is "counter = free retaliation" (Fire Emblem's enemy phase counters, Into the Breach's predictable telegraphs); the twist here is that the answer *moves it*. No push, pull or Command can move it (Immovable), so provoking it is the player's only way to steer it; on its own turn it still walks wherever the AI likes.

**Systems.**
- Rules: the base rules above.
- Levers and start values: step 1 tile; answer 7 ×; lumber at the edge (3 tiles) on; no limit per turn; slam 10 ×, family only, on its own turn.
- Interactions:
  - **John's role** fires on an enemy action start in every phase (`Unit_John.prefab` `triggerEvents: 1`, `activationPhase: -1`), and the counter raises `abilityStarted` (`:148`), so John within 2 of the struck member can take the answer at × 0.5. *To check in play.* John striking it himself gets no relay (he's the target).
  - **Mark's role** fires only on the enemy phase, so it never meets a counter. **Lucy's** and **Linda's** role hits no longer provoke it: no loop.
  - **Linda's Harmonic Slam** cripples: a Crippled Masher can't step, so poking it from 2 tiles is safe for a turn. This needs the Crippled check the counter lacks today.
  - **Mark's Vault with Stunning Vault**: a Stunned Masher doesn't answer at all (already true, `:77`).
  - **Multi-tile 2 × 2**: adjacency is four-direction from any of its 4 tiles (8 tiles touch it). Its step needs a free 2 × 2 spot on a path: corridors, walls and its own goblins can deny it, which is a positioning tool, not a bug.
  - **Immovable**: unchanged. John's Super Time pull ignores it (Combat rules Q8); out of scope.
  - **Ranged attackers**: inside 2 tiles of its footprint, anyone is answered. At exactly 3 (Lucy's max range, or Linda) it lumbers 1 tile closer without hitting; at 4+ (only Linda) nothing happens.
  - **Attacks that move the attacker** (CR-7 walk-then-attack, John's Dash, Mark's Vault): the answer is measured from where the attacker ends, after the whole action.
  - **Burn, push damage, Pass-by**: no answer (burn ticks on its own turn; it can't be pushed; Pass-by deals no damage).
  - **Several Mashers** (the Warren "Masher-heavy wave" on `thj/home-test`): each answers only its own attacker. Removing friendly fire makes that wave harder (they no longer slam each other).
- Failure cases: (1) melee members refuse to engage (watch; lever: damage 7, or option B); (2) Linda and Duos kill it with no risk (fine if it takes several turns; watch turn count); (3) corridor maps make it inert (level design note: give it room); (4) the counter kills a member on a hit the player didn't expect (only if the preview is wrong, see UX).

**UX.**
- *Before committing an attack:* hovering the Masher while aiming shows (existing preview, adjusted) its step ghost and path if it steps, **one** red tile (the attacker's), and the damage on the attacker. At the edge (3 tiles) it shows the ghost and path only, no red tile and no damage: "it comes closer, it doesn't hit". If it won't react at all (4+ tiles, Crippled and not adjacent, Stunned, the hit kills it, a Duo or other non-provoking action) nothing is shown.
- *The preview must survive the first answer:* today it is hidden once the Masher has answered in a turn (`ActivatedAtThisPhase`, set in the base `Activate`, `FactionRoleHandlerBase.cs:150`, read at `:369` of the handler). Under "no limit" that would hide every later answer: the likeliest surprise hit. In scope.
- *While moving:* the Shift danger zone and the enemy threat arcs already show exactly the counter zone (move 1 + adjacent attack, no splash), so "am I safe to swing from here?" is answered by the tools the player already uses.
- *Changes needed:* (1) one tile instead of the splash; (2) a step without a hit only at the edge (today it shows a closest step at any range, `:399-407`); (3) measure from the attacker's **end** tile when the attack moves the attacker; (4) hide it for non-provoking actions (Duos, if THJ agrees); (5) keep it after the first answer in a turn. Nice to have: the Masher's role badge tooltip says what provokes it (text for the narrative agent).
- *Likeliest misread:* expecting the own-turn splash on the counter, or the reverse. Mitigation: the counter preview marks one tile, the own-turn intent marks five; the role badge tooltip states "answers the one who hit it".

## USP check

- **Family Roles:** strengthens. John's relay becomes the natural way to absorb the answer; Linda's cripple and Mark's stun shut it down; roles chip it without provoking it.
- **Synergies:** neutral on purpose. Synergy hits that belong to the acting member's own ability (Tempest Bloom copies of Linda's arrow) count as hers; others don't provoke.
- **Duos:** strengthens if THJ accepts Q2 (Duos don't provoke): the family acting together is the safe way in.
- **Home:** neutral. Omens that remove or buff the Masher (Red Veil at Goblin Camp) are unaffected.
- **Pillars:** reaction timing (John's prompt during the player's own turn), family-driven combat (who takes the answer), emotional tone (brute force against a family that protects each other). No pillar weakened.

## Recommendation

**Option A, "Reckless", amended after the critic pass.** Start values: the answer comes once after the acting member's whole action; step 1 tile (its normal move); answer 7 × `Stat_DMG` on that member only; an attacker exactly 3 tiles away makes it lumber 1 tile closer without hitting; no limit per turn; own-turn slam keeps its plus splash at 10 × but hits the family only.

**Playtest signals.**
- Works: players say where they will swing *from* before swinging; at least once per fight a member lures it (a melee bait or Lucy's edge pull); John's relay fires on an answer; the Masher dies in 3–5 rounds in M7/M8.
- Fails: melee members never attack it (→ answer 5 ×, or option B); it is dragged around without ever answering (→ turn off the edge pull); players are surprised by an answer (→ preview bug: the moved-attacker case or the preview hidden after the first answer).

### Proposed GDD wording (not written yet)

> **EN-2. Counter-attack (Masher Goblin).** During the family's turn, when the ability the player chose for a family member hurts the Masher and it survives, the Masher answers that member, and only that member, once the member's action is over. If the member isn't next to it (four directions, from any of its four tiles), it first takes one step (its normal move, 1 tile) to a free spot next to them. The answer is one blow, 7 × damage, to that member alone: nobody else, family or goblin, is hurt. If no free spot next to the member is within its step, there is no blow; if the member is just one tile further (3 tiles from the Masher), it still lumbers 1 tile toward them. It answers every such action, with no limit per turn. Family Roles, Duos, burn and anything on the enemies' turn don't provoke it. A Crippled Masher can't step; a Stunned one doesn't answer. Hovering the Masher while aiming an attack shows the answer in advance: its step, the struck tile and the damage. *Planned*

> **EN-3. Immovable (Masher Goblin, Mountain Deev).** Can't be pushed, pulled, swapped or moved by Mark's Command (except as [Combat rules](combat-rules.md) Q8 notes). The Masher is also Reckless: it answers whoever hurts it (EN-2), so provoking it is the family's only way to steer it. *Built* (Reckless as in EN-2: *Planned*)

> **EN-11. Slam (Masher Goblin).** On its own turn the Masher slams a tile next to it: 10 × damage to every family member on that tile and the four around it. Goblins are not hurt. *Planned*

**Proposed answer to Enemies Q2:** no limit per turn. Only the ability the player chose provokes it, and it answers once after the whole action, so it answers at most once per action, and the loop through Family Roles is gone. The second counter component (on a child object, hand-made id) is never started, because only the root's is initialized (`AbilityOrchestrator.cs:50, 63`), so it can't counter twice; remove it in the build, and give the root component the new counter preset.

## Questions for THJ

**Q1. Limit per turn (Enemies Q2).**
- Context: the counter fires on every provoking hit; with reactions excluded, the count is capped by the family's AP.
- Options: (a) no limit, the most reckless; (b) once per family member per turn: melee members pay once, a hidden counter to track; (c) once per turn in total: the first striker is the sacrifice, everyone else swings free, the least threatening.
- Recommendation: (a). It is the identity, and the reach rule already gives the player a way out. (b) is the fallback lever.
- Blocked: the handler's trigger code. Data and preview work can start.

**Q2. Do Duos provoke it?**
- Context: Duo partner abilities seem to raise no damage event today (to check), so Duos probably don't provoke it now.
- Options: (a) no: "it can't answer the family acting together"; (b) yes, against the activator; (c) yes, against the partner it can reach.
- Recommendation: (a). It costs nothing to build, gives Duos a clear moment, and is limited by FTP and cooldowns.
- Blocked: the provoking-hit filter and its preview gate.

**Q3. Do Family Roles provoke it?**
- Context: today Lucy's embers and Linda's role arrow provoke it, and Linda's arrow can loop with the counter step.
- Options: (a) no; (b) yes, against the role's owner, with one answer per role per turn to stop loops.
- Recommendation: (a). Roles fire without a choice, so answering them breaks "I decide who takes the hit", and (b) needs a loop guard.
- Blocked: same as Q2.

**Q4. When it can't reach the attacker, does it still step closer?**
- Context: your point 4 says no counter when it can't reach; today it steps toward the attacker from any range. Your goal includes luring it, and under (a) only a member who takes the hit can lure it.
- Options: (a) no step, no hit: the simplest read ("outside the red zone it stays put"), but ranged members can't lure; (b) it always steps closer without hitting: free pulls from any range; (c) **lumber at the edge**: only an attacker exactly 3 tiles away pulls it 1 tile, no hit; at 4+ nothing.
- Recommendation: (c). It keeps "no hit without reach", gives Lucy (range 3) a lure that puts her in its zone next turn, and leaves Linda at 4 as the only fully safe poke. It costs one extra preview state (ghost, no red tile).
- Blocked: the reach code.

**Q5. Own-turn slam: keep the area?**
- Context: your point 2 is about goblins being hurt; the counter becomes single-target either way.
- Options: (a) keep the plus splash, family only; (b) single-target on its turn too; (c) keep the splash and friendly fire on its own turn only.
- Recommendation: (a). It keeps a heavy, telegraphed blow that punishes bunching, distinct from the quick answer.
- Blocked: one data value (`MasherGoblin_Ability_CompoundEffect.targetFactionRelation`).

**Q6. Step distance and damage.**
- Context: its normal move is 1 tile, so the hit zone equals the Shift danger zone. With no limit, a member who swings twice takes two answers.
- Options: (a) 1 tile, 10 × (today's slam value); (b) 1 tile, 7 ×; (c) a 2-tile charge, 10 ×.
- Recommendation: (b). A quick answer next to the 10 × slam, and melee members can still afford to engage; 5 × is the next lever down, 10 × the lever up.
- Blocked: nothing; the start values can be changed later.

## Scope

In: the Masher's counter rule, its counter preset, its slam's faction filter, its hover preview, prefab cleanup, GDD wording.
Out: the Masher's AI on its own turn (targeting is unchanged); Immovable exceptions (Combat rules Q8); Family Role limits (FR-4); enemy introduction text.

## Touches

Systems: Family Roles (core: `MasherGoblinFactionRoleHandler.cs` is listed in `tech/core-systems.md`), ability data (new preset assets; the core `AbilityPreset` code is not changed), damage preview (core, used as is, no change expected).
USPs: Family Roles, Duos.
Docs: see "Docs to update".

## Core-system impact

- **`MasherGoblinFactionRoleHandler.cs` is core** (Family Roles row). Changing its behavior is Tier 3, which this plan asks for. The changes are inside this handler: trigger gating (family turn, acting member, exclude role and Duo abilities), the reach rule, the Crippled check, a single-target counter ability, preview fixes.
- **`FactionRoleHandlerBase.cs`**: no change expected. If the handler starts using the base `ability` slot, it should call the base initialization so the slot is ticked (and the warning goes); that is a use of the base, not a change to it.
- **AP, damage preview, AI code**: no change.
- **AI regression:** the slam's faction filter change (and a new preset, if added to the unit's ability list) can change how the AI scores the Masher's attack, so `AIRegressionTest.Baseline_MatchesCurrentAI` may shift if its scenarios include a Masher. That test is already red; don't re-baseline it. Keep the counter preset **off** the unit's ability list (role handler only) so the AI never picks it on its own turn.

## Risks

- **The answer is announced as a Family Role.** The base `Activate` raises `RaiseFamilyRoleActivated(this)` (`FactionRoleHandlerBase.cs:151`), so role UI, John's tether, role barks, the combat log and any future FR-4 limit counters see the Masher's answer as a role. Tech plan: audit those listeners (most already filter on Bergson handlers).
- **Hits during an answer are dropped.** `:77` ignores damage while the Masher's controller is busy. If the player can act while an answer plays, a quick second swing gets no answer and no explanation. Tech plan: confirm input is locked during the answer, or queue the hit.
- **Waiting for the end of the action** needs a clear "action over" signal for the acting member (after follow-ups such as Continuous Attack). Tech plan to name it.
- The provoking-hit filter needs to know the player's acting unit and which ability is a Family Role or a Duo. If that can't be read cleanly from the handler, the fallback is "owner is a player-faction unit, on the player's turn, and the ability is not that unit's role ability", which still excludes Duos if they raise no damage event. Tech plan to confirm.
- The preview must use the attacker's end tile; the moved-attacker case is the most likely surprise.
- Corridor pinning: where its 2 × 2 can't step, melee hits are free. Accepted as a positioning tool; level note: give the Masher room.

## Gates

Compile / EditMode tests (pure reach, edge-pull and provoking-hit rules as testable helpers) / review / play check: yes (M7 or M8 with a Masher: melee bait, Lucy's edge pull, John relay, Crippled, corridor, Duo, two answers in one turn with the preview still shown) / docs to update.

## Critics

One critic pass (the `miso-design-critic` agent type was not available in this session, so a separate `miso-game-designer` instance ran read-only in the critic role). It kept Option A. Its points and what I did:

1. **Luring was the weakest part.** Under the first draft only a member who took the hit could lure it, and Option D's risk was stated backwards (stepping closer makes it more dangerous). *Accepted:* added "lumber at the edge" (Q4 c) and made it the recommendation; corrected D's risk; corrected "provoking it is the only way to move it" (it walks on its own turn).
2. **10 × with no limit makes melee a pure tax.** *Accepted:* the answer starts at 7 ×, the slam stays at 10 ×.
3. **Code facts missed:** the preview is hidden after the first answer in a turn (`ActivatedAtThisPhase`); the answer is announced as a Family Role; hits during an answer are dropped (`:77`). *Verified and accepted:* in UX and Risks; the preview fix is in scope.
4. **Continuous Attack was misread:** MA-2 swings again only after a kill, on the lowest-health enemy. *Verified in `characters/mark.md` and accepted:* the answer now comes once, after the acting member's whole action, from their end tile. That one rule also covers moved attackers.
5. **Trigger wording and Shield Flare.** *Accepted:* "the ability the player chose for the acting member"; Shield Flare copies (John's) don't provoke. The corridor note was added to Risks.

Not changed: "no limit" (the critic agreed), excluding Duos and Family Roles (the critic agreed).

## Docs to update if approved

- `design/gdd/enemies.md`: EN-2, EN-3, new EN-11; Q2 answered; Roster note.
- `design/gdd/combat-rules.md`: CR-22 (drop the Masher as the both-sides example); Statuses table, Reckless line.
- `design/combat-balance.md`: the Masher lines at :7, :32, :90, :96.
- `glossary.md` (narrative agent): Masher Goblin line ("answers whoever hurts it"); a name for the counter blow if it gets one.
- `tech/combat-log.md:151` (the "Masher's area attack hits its own side" note), coordinator.
