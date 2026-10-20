# Masher Goblin: reckless tank (counter-attack rework)

Size: M    Tier: 3 (Masher handler is a core system; changes an enemy rule)    Assigned to: miso-game-designer
Branch: all (work on `main`)
Status: waiting on THJ (open questions only; the rules are decided)

> **Revision 2 (2026-10-20).** Revised to THJ's decisions D-092 to D-098 (`decisions.md`). Changes from revision 1:
> - **Provokers:** Duos and Family Roles now provoke it. Roles and other reactions do so in any phase.
> - **Out of reach:** it always steps toward the attacker; the edge pull is gone.
> - **The blow:** the counter is a copy of the slam, plus area and friendly fire included, at 10 ×. The 7 × single-target counter is gone.
> - **Aim:** one aim rule for both slams; it strikes only from next to its target's tile.
> - **Roles:** a toggle sets whether its counter can provoke a Family Role. There is no limit per turn.
> - **Kept from revision 1:** the answer comes after the acting member's whole action, Crippled means no step and Stunned means no answer, the preview fixes, and the Q2 component finding.
> - **Questions:** the answered ones are removed. Two new open questions: a hidden safety stop, and when an enemy-turn answer happens.

## Why

THJ wants the Masher to bring its own challenge to a level: hit it and it comes for you. Today its answer borrows the own-turn slam and the generic damage event, so who provokes it, where it aims and how far it reaches are side effects of code written for other purposes. The fix is a rule set of its own, which THJ has now decided (D-092 to D-098). Request: coordinator task of 2026-10-20.

## Goal

Every hit drags the Masher one step toward whoever struck it. When it ends next to them it brings its full slam down on their tile, and anyone standing around them is hit too, goblins included. The player lures it, chooses who stands where, and decides how far to let its answers chain into the family's reactions.

## Problem and evidence

**THJ's brief:** (1) the counter should hit only its attacker; (2) it hurts other enemies; (3) only on the player's turn; (4) it must be adjacent to the attacker to hit. Goal: "a really reckless tank, challenging, but one the player can strategize around: move it around (lure it) and avoid getting hit." THJ's decisions then refined these. Point 1 became "single target **aim**" with the plus area kept (D-095). Point 2 was reversed: friendly fire stays, as Reckless (D-095). Point 3 holds for chosen abilities and Duos but not for reactions (D-094).

### What is built today (verified in code and data unless marked)

| Aspect | Today | Source |
| --- | --- | --- |
| Trigger | Any `onUnitDamageDone` on the Masher from an ability whose owner is alive and not downed, if the hit was not lethal, the Masher's own controller is not mid-action and it is not turn-skipped (Stunned) | `MasherGoblinFactionRoleHandler.cs:70-81` |
| What counts as a hit | `onUnitDamageDone` is raised only for abilities that complete, only when the owner's faction is hostile to the target, and only for HP loss | `CombatLevelRunHandler.cs:774-799` |
| Which turn | Not gated by turn. During the enemy turn the AI controller is usually mid-action (`isActionInProgress`, `FactionControllerBase.cs:72`), which blocks most enemy-turn counters by accident, not by rule | `:77` |
| Reactions provoke it | Yes, when the timing allows: Lucy's embers (`OnActionComplete`, every phase) and Linda's role arrow (`OnUnitEndMoving`, every phase). Mark's role fires only on the enemy phase (`Unit_Mark.prefab` `activationPhase: 4`), where `:77` usually blocks it | role prefabs `triggerEvents`/`activationPhase` |
| Duos provoke it | Probably not: duo partner abilities are silent and raise no bus events (`tech/combat-log.md:275`), so their damage likely never reaches `onUnitDamageDone`. *Assumed, to check in play* | |
| Counter attack | The Masher's basic attack `MasherGoblin_Ability_Attack` (`Unit.DefaultOccupiedCellAbility`, `:57`) has radius 1, Adjacent (4 directions), measured from every footprint tile, and target type Cell or Occupant (`targetType: 3`). It spawns `AOE_Attack _MasherGoblin_Variant`. That spawn's `MasherGoblin_Ability_CompoundEffect` hits the struck tile plus its 4 neighbours (`applyMode` Surrounding, radius 1, `includeCentralCell`), on **any faction** (`targetFactionRelation: -1`), for 10 × `Stat_DMG` (`..._Attack_Effect_AttrMod`) | `Resources/UnitSpecific/Enemy/Masher Goblin/Attack/` |
| Aim | It picks any tile in its attack range whose splash covers the attacker (`TryPickAttackCell`, `:181-201`). So an attacker on a side or back tile of the cross, 2 tiles from its footprint, gets hit without the Masher moving. The AI on its own turn can also aim at an empty tile | `:203-226`; `targetType: 3` |
| Movement budget | Its normal walk, `MasherGoblin_Ability_Walk`: radius = 1 × `Stat_SPD` (×1 for enemies) = **1 tile**. Path-walkable, through allies (`ignoreRelationOnWalk: 1`); the whole 2 × 2 footprint must fit | `Walk.asset:59-62, 99`; `:296-342` |
| Unreachable | It steps to the tile that brings it closest, then does nothing (`:320-329`, `:139-146`). This already matches D-093 | |
| Crippled | The walk preset is blocked by Crippled, but the counter calls the walk directly and never checks it, so a Crippled Masher may still step. *To check in play* | `Walk.asset:23-28`; `:161` |
| Cost | Free: no AP, no FTP (`FactionControllerBase.cs:199`); it resets both cooldowns afterwards (`:131-134`) | |
| Limit | None (`oncePerPhase: 0`, never read) | `Unit_MasherGoblin.prefab:813` |
| Two components (Q2) | There is a handler on the root (`ability` empty) and one on a child object (hand-made id, `ability` = Attack preset). Only the root's is ever started: the orchestrator calls `GetComponent` on the unit root (`AbilityOrchestrator.cs:50, 63`). So it cannot counter twice, and the child is dead weight. The root's empty `ability` causes the "did not initialize its role ability" warning | `Unit_MasherGoblin.prefab:745-1017`; `FactionRoleHandlerBase.cs:80-82, 175-185` |
| Preview | Hovering the Masher while aiming shows the step ghost, the path, every splash tile and the damage on the attacker. It is measured from the attacker's **current** tile, and hidden after the first answer in a turn (`ActivatedAtThisPhase`, set in `FactionRoleHandlerBase.cs:150`, read at `:369`) | `:367-426` |
| Announced as | A Family Role: the base `Activate` raises `RaiseFamilyRoleActivated` | `FactionRoleHandlerBase.cs:151` |

## The rules (decided, with the designer's details marked)

- **Provokers (D-092, D-094):**
  - On the family's turn: the ability the player chose for the acting member (its own hits and projectiles), and Duos.
  - In any phase, the family's turn or the enemies': Family Roles and other reactions.
  - Not provokers: burn, Pass-by, allied AI units (Toba as an ally, the Deer), and anything else on the enemies' turn.
- **Which Duo partner (D-095):** the partner who struck it. If both did, the one it can reach. If it can reach both, the one who acted first.
- **When (designer, from revision 1):** for a chosen ability or a Duo, the answer comes once the acting member's whole action is over (follow-ups included, e.g. Mark's Continuous Attack). It is measured from the tile the member ends on. A reaction is answered when that reaction completes. So one player action can draw two answers: one for the actor, then one for Lucy if her embers also hit it.
- **Step (D-093):** every provoking hit makes it take its normal move (1 tile; the 2 × 2 must fit on a free path) toward the provoker, whatever the distance. If the path is blocked, it doesn't step. If it is already next to the provoker, it doesn't step.
- **Aim (D-095), on the counter and on its own-turn slam:** it strikes only when it stands next to its target's tile (four directions, from any of its 4 tiles). The struck cell is the target's tile, so standing on a side or back tile of the cross no longer starts the attack. It never aims at an empty tile.
- **The blow (D-095, D-096):** a copy of its main slam, with the same aim, area, damage and range: 10 × to everyone on the target's tile and the 4 around it, its own side included (Reckless).
- **Statuses (designer, unchanged from revision 1):** a Crippled Masher can't step (it answers only if already next to the provoker), as its walk already says. A Stunned one doesn't answer (already true).
- **Toggle (D-097):** `counterCanProvokeFamilyRoles` (working name) on the Masher, default **true**. When it is false, the Masher's answers start no Family Role (no John relay, no Mark punch, no Linda lane shot). There is no other loop guard.
- **Limit (D-098):** none per turn, in either direction.

## Options compared (revision 1, for the record)

Revision 1 compared four options: A "Reckless" (answer every hit it can reach), B once per member per turn, C "Winded" (each answer costs it 1 AP on its next turn), and D "Lumber" (it steps closer even when it can't reach). It recommended A with a 7 × single-target answer, an edge pull at 3 tiles, and Roles and Duos excluded. THJ chose the rules above: A's "no limit", D's "always step", and the slam kept whole. The comparison is in this file's revision 1 in `claude-handoff` history.

## Lens notes

**Creative.** Target experience: the Masher is a wall of muscle the family has to *handle*. Every hit drags it a step, and when it lands next to someone it brings its whole slam down, on goblins too if they are in the way. The moments I'm designing for:
- Mark lands a blow. The Masher lumbers a step and raises its club. John's shield prompt flashes, and John eats half of the blow.
- Next turn the family has walked the brute, one tile at a time, into a knot of Dark Claws, and baits it into slamming them.

With friendly fire kept, luring it into its own side is now a real tactic. That is original next to the genre-default counter (Fire Emblem's enemy-phase counters).

**Systems.**
- Levers: the step (1 tile), the counter preset's values (a copy of the slam's, so tuning is data only, D-096), and the toggle.
- Interactions:
  - **John's role** (on action start, every phase) can take any answer aimed at an ally within 2 of him, at × 0.5. It costs 1 FTP each time. *To check in play.*
  - **Mark's role** (enemy phase only): an answer during the enemy turn that hits an ally within his reach makes him punch. That punch is a reaction, so it provokes another answer. See the chains below.
  - **Linda's role:** an answering step that ends in her lane makes her shoot, which provokes another step toward her.
  - **Lucy's role:** her embers after a family action provoke an answer aimed at Lucy.
  - **Linda's Harmonic Slam** (Crippled): no step, so its answers stop unless someone is already next to it.
  - **Mark's Stunning Vault:** a Stunned Masher doesn't answer.
  - **2 × 2 footprint:** 8 tiles touch it. Its step needs a free 2 × 2 spot, so corridors and its own goblins can deny it.
  - **Immovable:** unchanged (Combat rules Q8 is out of scope).
  - **Ranged attackers** (Linda 4, Lucy 3): every hit pulls it 1 tile closer. Each poke costs nothing now, but brings it closer to a strike.
  - **Attacks that move the attacker** (CR-7, John's Dash, Mark's Vault): the answer is measured from the end tile.
  - **Friendly fire:** a slam on a family member standing next to goblins hurts the goblins. Kills by friendly fire give no XP or gold (CR-22).
  - **Several Mashers:** one Masher's slam can provoke nothing in another (they are allies, so `onUnitDamageDone` isn't raised, `CombatLevelRunHandler.cs:777`).
- Failure cases:
  1. A Role ↔ counter chain that runs long (see below).
  2. The family pulls it around for free with ranged pokes. This is accepted by D-093; each pull brings it closer.
  3. Corridor maps make it inert. Level note: give the Masher room.
  4. Answers mid-enemy-turn confuse the AI's plan (open question O2).

### How a Role ↔ counter chain ends (toggle true)

Chains are possible in two places:

**Mark (enemy turn only).**
- The loop: an answer hits an ally within 2 of Mark, so Mark punches (Fist Blitz, 8 ×). The punch is a reaction, so the Masher answers again, steps if needed and slams. That hits Mark or an ally, so Mark punches again.
- **This is the only true ping-pong.**

**Linda (any turn).**
- The loop: an answering step ends in her lane within range, so she shoots. The arrow provokes another step toward her.
- **It ends by itself:** once the Masher stands next to her it no longer steps, so it no longer "ends a move" in her lane. At most about 4 to 6 links.

**John** doesn't loop: his relay is a reaction to the answer, not a hit on the Masher. **Lucy** doesn't loop: her trigger is a *family* action finishing.

What ends a chain today:

1. **FTP.** Each role costs 1 FTP (`requiredFTP` 1, FR-3 "built today"). The pool is 14 to 24 for the full family. A chain stops when the pool can't pay. *Verified in the GDD; the cost per role is read from the data by the GDD.*
2. **The QTE.** Each role needs a press within 1 s. A missed press skips the role, and the role's targets are silenced for `silenceTurnsOnIgnore` turns (0 on the roles read, so no silence). Declining ends the chain at once.
3. **HP.** Each link deals 10 × (slam, × 0.5 through John) to the family and 8 × (Mark) or 6 × (Linda) to the Masher. With 80 HP, the Masher dies after about 10 of Mark's punches. Mark dies sooner unless John relays.
4. **The role's own feasibility.** The base trigger check also needs `ability.CheckActivationFeasibility()` (`FactionRoleHandlerBase.cs:123`). If Fist Blitz has a cooldown, Mark's role fires once per cooldown and the Mark loop has length 1. *Not read; FR table, Mark row, already flags "check whether the cooldown already gives 1".*
5. **Reach.** Mark's role needs the Masher within 2 of him, so a blocked step or a Crippled Masher ends it.

So today the chain is bounded by FTP and the player's presses. **It becomes unbounded if roles stop costing FTP (FR-3, planned) before the per-round role limits (FR-4) exist:** then only HP and the QTE stop it. That is why a hidden safety stop is worth having (O1).

**UX.**
- *Before committing an attack:* hovering the Masher while aiming shows:
  - its step ghost and path when it would step;
  - when it ends next to the attacker: the 5 tiles of the slam centred on the attacker's tile, and the damage on every unit inside, goblins included;
  - when it can't reach: the step only, with no slam tiles.
- *Duos:* the preview picks the partner by the D-095 rule.
- *Roles:* they are automatic, so there is no preview. John's tether already shows his relay.
- *Changes needed:*
  1. Centre the slam on the attacker's tile (today it can be any cross tile that covers them).
  2. Show the step at any range, without slam tiles when it can't reach (matches today's partial-step preview).
  3. Measure from the attacker's **end** tile.
  4. Keep showing it after the first answer in a turn.
  5. Show damage on every unit in the cross, not only the attacker.
  6. Add a Duo case.
  - Nice to have: the role badge tooltip says what provokes it and that it hits its own side (narrative agent).
- *While moving:* the Shift danger zone (CR-43: move 1 plus adjacent aim, without splash) is exactly where it can *aim*. Standing diagonally next to a target it can aim at is not shown as danger, because splash is excluded by design. This is accepted; the hover preview covers it.
- *Likeliest misread:* a member standing *next to* the attacker is hit by the slam and the player didn't expect it. Mitigation: the preview shows damage on every unit in the cross (change 5).
- *Second misread:* a long chain on the enemy turn feels like the game took control. Mitigation: the toggle, and the QTE (declining ends it).

## USP check

- **Family Roles: strengthens, with a risk.** Roles become part of the Masher puzzle: John's relay absorbs answers, Linda's lane shots drag it toward her, and Mark's punches can start a duel. The risk is chains that feel automatic; the toggle and the QTE are the answer.
- **Synergies: neutral on purpose.** Synergy hits count as the acting member's action or as reactions, by who owns them.
- **Duos: neutral to slightly positive.** Duos carry the same risk as other attacks (D-092). The "which partner" rule makes the Duo partners' positions matter.
- **Home: neutral.**
- **Pillars:**
  - Reaction timing: role prompts during its answers, on both turns. Stronger.
  - Family combat: who stands next to whom matters more, because the slam hits them all.

## Proposed GDD wording (not written yet)

> **EN-2. Counter-attack (Masher Goblin).** When the Masher is hurt and survives, it answers whoever hurt it. Two kinds of hit provoke it: during the family's turn, the ability the player chose for a family member, or a Duo; on either turn, a Family Role or another reaction. For a chosen ability or a Duo, it answers once the member's action is over. For a reaction, it answers when that reaction is done. For a Duo, it answers the partner who struck it; if both did, the one it can reach; if it can reach both, the one who acted first. Each answer, it takes one step (its normal move, 1 tile) toward that member, however far away they are, unless it is already next to them. If it then stands next to them, it slams their tile (EN-11). It answers every such hit, with no limit per turn. A Crippled Masher can't step; a Stunned one doesn't answer. Hovering the Masher while aiming an attack shows the answer in advance: its step, and if it reaches, the slammed tiles and the damage. Whether its answers can set off Family Roles is a setting on the Masher (on by default). *Planned*

> **EN-3. Immovable (Masher Goblin, Mountain Deev).** Can't be pushed, pulled, swapped or moved by Mark's Command (except as [Combat rules](combat-rules.md) Q8 notes). The Masher is also Reckless: every hit drags it a step toward whoever struck it (EN-2), and its slam hurts its own side. *Built* (Reckless as in EN-2 and EN-11: *Planned*)

> **EN-11. Slam (Masher Goblin).** The Masher's attack, on its own turn and when it answers (EN-2). It strikes only a unit whose tile is next to it, never an empty tile: 10 × damage to everyone on that tile and the four around it, goblins included. *Planned*

**Answer to Enemies Q2 (D-098):** no limit per turn, in either direction: it answers every provoking hit, and a Family Role can provoke it as often as the role fires. A toggle on the Masher (D-097) sets whether its answers can set off Family Roles. The second counter component (on a child object, with a hand-made id) is never started, because only the root's is initialized (`AbilityOrchestrator.cs:50, 63`), so it can't counter twice. Remove it in the build.

## Open questions for THJ

**O1. A hidden safety stop for Role ↔ counter chains?**
- *Question:* add a crash guard that cuts a chain of answers after a fixed number of links, never meant to be reached in play?
- *Context:* with the toggle on (D-097) and no limit (D-098), the Mark loop is bounded only by FTP, QTE presses and HP. If roles become free (FR-3) before role limits exist (FR-4), only HP and presses remain. A bug (for example a zero-length animation, or a role firing without a QTE in Family Super Time) could recurse without end.
- *Options:*
  - (a) None. The design bounds hold today. The risk is a hang if they ever don't.
  - (b) **Cap at 32 answers per chain.** A chain is everything started by one root action (a player action, or one enemy unit's action). Past the cap, the Masher ignores provoking hits until that root action has resolved, and a warning goes to the Console and the combat log. 32 is above any real chain: an FTP pool of 24 at most, and Linda's lane chain about 6 links.
    - Where it lives: a private constant (or a serialized field marked "debug") in `MasherGoblinFactionRoleHandler`. The counter resets when the root action completes, and at `turnEnded` as a backstop.
    - It is hidden: no UI, no GDD rule.
  - (c) The same, but global: one chain counter shared by every reactive handler (roles and the Masher), in the turn flow. This is wider protection, but it touches core turn flow (`CombatLevelRunHandler`).
- *Recommendation:* (b). It is local to the Masher, has no feel impact, and a few lines with a test. (c) is worth it later, if a second enemy gets a reaction.
- *Blocked meanwhile:* nothing in design. The implementer needs the answer before closing the build.

**O2. When a Family Role provokes it during the enemies' turn, when does it answer?**
- *Question:* does the answer interrupt the enemy turn at once, or wait until the current enemy unit's action ends?
- *Context:* D-094 allows enemy-turn answers. Today the handler refuses while its own controller is mid-action (`:77`), and `TryPlayFactionRole` refuses too (`FactionControllerBase.cs:185`). The AI also plans the whole faction on a worker thread, so an answer step that moves the Masher mid-turn can leave its plan stale.
- *Options:*
  - (a) **Wait** until the current enemy unit's action completes, then answer. If the Masher hasn't acted yet this turn, the AI replans it from its new tile. Answers are free, and its own turn's AP is untouched.
  - (b) Interrupt at once: the most dramatic, but it needs changes inside the AI controller's turn flow (core, Tier 3) and risks breaking AI plans.
  - (c) Queue every enemy-turn answer to the end of the enemy turn: simplest, but answers come late and lose cause and effect.
- *Recommendation:* (a). It keeps cause and effect (Mark punches, the Masher turns on him right after), and it fits how roles already wait (`WaitForProcessesToComplete`).
- *Blocked meanwhile:* the enemy-turn part of the trigger code. The player-turn part can be built.

## Scope

In:
- the trigger (provokers, phases, Duo partner);
- the step and aim rules;
- the counter preset (a copy of the slam);
- the aim rule on the own-turn slam;
- the toggle and the safety stop (if O1 is approved);
- the preview changes;
- the prefab cleanup;
- tests;
- the GDD wording.

Out:
- the Masher's AI targeting on its own turn, beyond the aim rule;
- Immovable exceptions (Combat rules Q8);
- Family Role cost and limits (FR-3, FR-4);
- enemy introduction text.

## Build cost (rough, M to L)

1. **Counter preset:** a copy of `MasherGoblin_Ability_Attack` (`MasherGoblin_Ability_Counter`, effect sub-assets copied or shared), made by a one-off editor script. It goes on the root handler's `ability` slot, **not** on the unit's ability list, so the AI never picks it. The handler then initializes its base `ability` (this also fixes the warning). Remove the dead child component.
2. **Aim rule, data:** on both presets, target type Occupant only (`targetType` 3 → 2), so the struck cell is always a unit's tile.
3. **Aim rule, code:** `TryPickAttackCell` accepts only the target's own tile.
4. **Trigger:**
   - phase gating: chosen ability or Duo on the player's turn; reactions in any phase;
   - "after the whole action" timing;
   - the Duo partner rule;
   - Crippled check;
   - getting Duo damage to the handler (Duo partner abilities seem silent, see Risks).
5. **Enemy-turn answers** (O2 a): wait for the current enemy action, then answer, then let the AI replan the Masher.
6. **Toggle:** `counterCanProvokeFamilyRoles` (bool, default true). When false, the answer must not start role triggers. The likely route is to activate it without `abilityStarted`/`abilityPerformed`, or tagged so role handlers skip it. Either way it must still raise the damage events that John's passives (Wrath, Blood Debt) listen to.
7. **Safety stop** (O1 b): a counter with reset points, a warning, and a test.
8. **Preview:** the six changes in UX.
9. **Tests:** EditMode tests for the pure rules (aim cell, step choice, Duo partner pick, provoker filter by phase, chain cap).

## Core-system impact

- **`MasherGoblinFactionRoleHandler.cs` is core** (Family Roles row in `tech/core-systems.md`). Every behaviour change here is Tier 3, now approved in principle by D-092 to D-098.
- **`FactionRoleHandlerBase.cs`:** no change expected. The handler starts *using* the base `ability` slot and initialization.
- **Turn flow and AI (`FactionControllerBase`, `AIController`, `AIFactionBrain`):** enemy-turn answers (D-094) need the Masher to act while its own faction's turn is in progress. Option O2 (a) aims to do this from the handler by waiting for the current action, then asking the AI to replan. If the controller's in-progress guard (`FactionControllerBase.cs:185`) or the AI's plan can't be handled from outside, this becomes a **core behaviour change (Tier 3)**. The tech plan must settle it.
- **Duos (`UnitsCooperationHandler`, core):** if Duo damage never reaches `onUnitDamageDone`, making Duos provoke it may need Duos to report damage. That is a core change; the alternative is for the handler to listen to the Duo trigger's own events. Tech plan to check.
- **Family Roles:** no change to the Bergson handlers. They already trigger in the needed phases.
- **Ability data:** two `targetType` changes and a new preset. No change to `AbilityPreset` code.
- **Damage preview:** used as is.
- **AI regression:** the own-turn aim change (`targetType` 3 → 2) changes which cells the AI can aim at, so `AIRegressionTest.Baseline_MatchesCurrentAI` may shift if its scenarios include a Masher. It is already red; don't re-baseline it.

## Risks

- **Announced as a Family Role** (`FactionRoleHandlerBase.cs:151`): role UI, John's tether, barks, the combat log and future FR-4 counters see the answer as a role. With enemy-turn answers this matters more. Audit the listeners.
- **Hits during an answer are dropped** (`:77`). Under "no limit", a reaction landing mid-answer (Linda's shot on the step) must be queued, not dropped. Otherwise the chain rules above are wrong in practice.
- **Duo damage may be invisible** to the handler (silent partner abilities).
- **Toggle off must not mute John's passives:** the route chosen must still raise the damage events.
- **The preview must use the attacker's end tile, and must survive the first answer.**
- **Corridor pinning:** where its 2 × 2 can't step, melee hits are free unless the attacker is already adjacent. Accepted.

## Gates

- Compile.
- EditMode tests.
- Review.
- Play check: yes, in M7 or M8 with a Masher. Cover:
  - melee bait;
  - ranged pull;
  - a slam hitting goblins;
  - a John relay;
  - Linda's lane chain;
  - the Mark chain on the enemy turn, with the toggle on and off;
  - a Duo with both partners striking;
  - Crippled;
  - two answers in one turn with the preview still shown.
- Docs to update.

## Critics

Revision 1 had one critic pass. The `miso-design-critic` agent type was not available, so a separate `miso-game-designer` instance ran it read-only. These findings still apply in revision 2:
- the preview is hidden after the first answer;
- the answer is announced as a Family Role;
- hits during an answer are dropped;
- Mark's Continuous Attack swings again only after a kill, so the answer waits for the whole action.

Its other proposals (the 7 × single-target answer, the edge pull, excluding Roles and Duos) were overtaken by THJ's decisions. Revision 2 was not re-critiqued: it applies THJ's rules and adds no new design choice, apart from O1 and O2, which go to THJ.

## Docs to update if approved

- `design/gdd/enemies.md`: EN-2, EN-3, new EN-11; Q2 answered (D-098); the Roster note.
- `design/gdd/combat-rules.md`: CR-22 keeps the Masher as the both-sides example; Statuses table, Reckless line ("every hit drags it toward the striker; its slam hits its own side").
- `design/combat-balance.md`: the Masher lines at :32, :90, :96.
- `design/gdd/family-systems.md`: a note in the role table (or Related) that roles provoke the Masher in any phase.
- `glossary.md` (narrative agent): the Masher Goblin line.
