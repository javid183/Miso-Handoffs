# Family Roles, round 2: each role armed by its own hero's verb

Size: L    Tier: 3 (the rule of a main mechanic and a USP; core role handlers and settings for any prototype)    Assigned to: miso-game-designer
Branch: all. `main` since THJ merged `thj/onboarding` on 2026-11-09 (D-456). `thj/home-test` notes in [Branches](#branches).
Status: draft (critics pending)

## Why

Round 1 ([`2026-11-09-family-roles-rethink-design.md`](2026-11-09-family-roles-rethink-design.md)) recommended **C, kept AP**, and THJ approved its test (D-460 to D-463), then paused it before playing with an objection: *"What makes players keep their AP instead of using it? If there are enemies alive while shooting with Linda, why should I not spend it right away? ... For John it's a bit different: he's not ranged and might not reach. Does this not require extra AP? Is 2 enough?"* He also made a counter-proposal per hero (John: Shield Up gate, stamina, swap at any range; Linda: facing lane, minimum range 2; Lucy: free with better feedback, or an ember pool; Mark: not covered). He wants a designer and critics discussion before deciding anything.

## Goal

Settle where kept AP stands, turn THJ's proposal into concrete per-hero rules with costs, and recommend one set with a test that needs no code first, under the same stop rule as D-460.

## Acceptance criteria

- [ ] Round 1's scenarios rechecked against THJ's objection, with a plain verdict on C and on any variant of it.
- [ ] The per-hero principle compared with A and C (experience, complexity, readability, cost, risk, USP, what's lost).
- [ ] Each hero: rules, starting values, interactions, failure cases, files and core status; THJ's specific items weighed (Shield Up gate, stamina vs Wrath, swap at any range, facing lane, last arrow, minimum range, Lucy preview vs ember pool, Mark options).
- [ ] A complexity count, and what to cut.
- [ ] S1 and S2 redone under per-hero rules, plus a new scenario for Linda's lane, in grid format on real prefab tiles, with decisions and prompts counted.
- [ ] The cheapest test: house rules first, then code in order.
- [ ] Recommendation and questions in the five-part format.

## Scope

In: the arming rule of each role, John's Wrath as a limit, the swap, Linda's lane and last arrow, minimum range, Lucy's preview and ember pool, Mark's options, the cost of roles (FTP), the test.
Out: role triggers and effects beyond what is listed, enemy AI, the Cyclone redesign, level rebuilds (only flagged), the Fireside mapping (noted).

## Touches

Systems: Family Roles (core: `FactionRoleHandlerBase`, the four Bergson handlers, `FactionControllerBase`), settings (core: `GlobalSettingsSO`), John's Wrath passive, Linda's quiver, Mark's Atman's Focus (not core), role zones and badge, the attack preview (UI plus the core preview path).
USPs: Family Roles (main), Synergies (John's Shield Up becomes their hub), Duos (FTP cleaner), Home (Fireside note).
Docs: [Docs to update](#docs-to-update-if-approved).

## Approach

Recheck round 1 honestly, state the principle, design each hero, count the complexity, play it on paper, then a two-step test (house rules, then code in order). Critics run by the coordinator after this draft.

Read for this plan (2026-11-09): round 1 in full; `vision.md`; the GDD (`family-systems.md`, `combat-rules.md`, `enemies.md`, the four character sheets); `combat-balance.md`; `decisions.md` (D-036 to D-042, D-244, D-246, D-292 to D-295, D-322, D-323, D-350, D-393, D-460 to D-463); the onboarding-after-Hearth plan; `tech/core-systems.md`; code: `FactionRoleHandlerBase.cs`, `JohnFactionRoleHandler.cs`, `JohnPassiveAbility_Wrath.cs`, `LindaFactionRoleHandler.cs`, `LucyFactionRoleHandler.cs`, `MarkFactionRoleHandler.cs`, `MarkPassiveAbility_AtmanFocus.cs`, the four `Unit_*.prefab` role components, `Mark_Ability_Walk.asset`, `John_Ability_Shield.asset`; prefabs `GB_s2-ridge` and `GB_m3-john` read back with `level_to_grid.py`.

---

## Problem and evidence

### Round 1 revisited: THJ is right

**Kept AP fails where it was supposed to work.** The decision C promised was "spend this AP now, or keep it for the role". That is only a decision when the kept answer is worth about as much as the action it replaces. Read against the code:

- **A kept answer is the same action, later and conditional.** Linda's Watch is her bow shot (6, an arrow, LI-11: "just her shot"). Mark's counter is his Fist Blitz preset (8). Lucy's follow-up is about one ember attack. Shooting now hits the target you choose, for sure, and can kill it before it acts. Watch hits only if the enemy ends its move in her lines. So with a target in reach, **spending now is at least as good, almost always**.
- **Keeping only happens when it is free or when nothing else can do the job.** (1) Nothing is in reach: keeping costs nothing, so it isn't a decision, it's "end turn". (2) The answer does something no action can: only John's guard qualifies (you can't prevent a hit on your own turn). (3) Keeping changes what the enemy does (zone denial): our AI has no variable for role zones (verified, `UtilityVariables.cs`, round 1 evidence 3), so this doesn't exist.
- **For a melee hero, 2 AP is not enough.** THJ's John point holds for Mark too: a melee turn is move + attack. Keeping one AP means giving up the attack whenever he has to move. So the keep is either free (nothing in reach) or it costs the whole offensive turn.

| Round 1 scenario | What round 1 claimed | What actually holds | Verdict |
|---|---|---|---|
| S1 The Ridge, K1 (Linda shoots once and keeps 1, Mark keeps 2) | A kill box, "safe" | Linda's second shot kills 2,4 now, for sure; the Watch kills it only if it ends in her lanes. Mark keeps because nothing is in reach (2,4 is 4 from him, Fist Blitz 2): free, not chosen | Linda's keep is dominated; Mark's is free |
| S1, K3 (Mark Blitzes, Linda keeps both) | "Aggressive", two Watch answers | Strictly worse for Linda than two shots on 2,4: the same two arrows, both waiting on enemy paths. The only real choice in K3 is Mark's step + Blitz, an ordinary turn | No role decision |
| S1, K2 (spend everything) | "Works, costs HP" | This is the line a good player takes. With C, they see no roles | The honest default |
| S2 Memory 3 (Shield Up + keep 1) | "The lesson" | Real: John's guard has no own-turn equivalent and his Sword can't reach (Claws 3 or more away). But it needed John's turn-1 limit raised 1 → 2, and its best part (save the one guard for Lucy) comes from the guard being **limited**, not from AP | Real, but it's John's verb, not AP |
| S3 The River (John step + keep 1) | One enemy-turn choice | Real for John for the same reason (sword now vs a prevented hit later) | Real, John only |

**So C, as tested, doesn't survive.** Its one live part is John, and John's own verb (Shield Up) gives the same decision more cleanly. Two variants survive on paper and go on the shelf, not into the test:

| Variant of C | What makes keeping worth it | Cost | Status |
|---|---|---|---|
| C1. A kept answer is stronger (e.g. ×1.5, or a Watch hit cancels the enemy's attack) | The answer beats the action it replaced, so keeping is a bet with a payout | A new number or rule on every role; still a lottery without AI awareness | Shelf |
| C2. Enemies read kept zones (round 1 option D, partial) | Keeping controls the board even when nothing fires | Core AI utility variable per enemy, golden-master churn (`AIRegressionTest`); roles fire less | Shelf |

THJ's objection also lands on one recommendation below (Linda's last arrow), and the plan says where.

### The principle

**Each role is armed by a choice on the hero's own turn, made with something that hero already does.** Kept AP armed roles with "doing nothing", and doing nothing loses to doing something. The per-hero rule works only where the arming choice is one of these:

1. **Free and predictive**: it costs no AP, only a guess about the enemy turn (Linda's facing).
2. **An action worth taking on its own**: the arming is a side effect of a good move (John's Shield Up already gives 60% damage taken and arms Wrath).
3. **A resource built by ordinary play, with another use**: spending it on the role costs something real (Mark's Focus is also his barrier).

A rule that arms a role by giving up an action (kept AP, a "Focus" ability that only builds a counter) falls back into THJ's objection. That test is applied to every option below.

---

## Options compared

| | **A. As built** (free per D-036 if wanted) **+ Lucy preview** | **C. Kept AP** (round 1) | **P. Per hero (recommended set)** | **P+. THJ's full proposal** |
|---|---|---|---|---|
| The rule | Roles fire when triggered; press to answer | "On the enemy's turn a role answers only with AP its Bergson kept" | John guards while his shield is up; Linda watches the lane she faces; Mark counters with Focus; Lucy as built, shown in previews | P, plus: John's guard swaps places at any range; stamina replaces Wrath; Linda can't shoot adjacent tiles; Lucy runs on an ember pool |
| When the player decides | The prompt (always yes) | Own turn: keep or spend (dominated, see above) | Own turn, with each hero's verb; and at the prompt for John and Mark, where declining now saves something | Same, more often |
| Player experience | Fun, authorless; Lucy stops "randomly coming about" | Roles mostly vanish for good players | Roles you set up: "John raised his shield", "Linda's facing the corridor", "Mark has Focus to spend" | Bigger swings (John flies across the map), Linda fragile up close |
| New things to learn | 0 | 1 (keeping) | 3 short conditions, no new resource (count below) | About 7, two of them resources |
| New on-screen elements | 0 (the preview reuses the stepped damage segment) | 0 | 1: Linda's facing picker (necessary). John's and Linda's zones change, Lucy's preview reuses existing pieces | 3 or more (stamina bar, ember counter, facing picker) |
| Readability | Lucy better; others unchanged | "Why didn't Linda shoot?" | Each role shows its arm: shield up, lane drawn, Focus pips | The swap reshuffles the board mid enemy turn |
| Implementation | Lucy preview: S–M, UI plus the core preview path | M, core | S per hero; each touches its core role handler (below) | Adds an M core swap, an M core minimum range, two M resources, level retunes |
| Risk | THJ stays stuck with "just a click" for three of four roles | Roles vanish; THJ's objection | Linda's lane fires too rarely; Mark starts with no counter; John fortress with Shield Up every turn (bounded by Wrath) | Scope; breaks Memory 3, the River and Memory 1 tuning; too many counters |
| What's lost that players love | Nothing | Most enemy-turn prompts | Fewer prompts (each one set up); accidental Watch-through-Cyclone becomes a choice of lane | John's area guard (one swap covers one ally), Linda's point-blank shots |
| USP effect | FR as is, Synergies + (preview shows the combo) | FR −, really | **FR ++** (authored, presses become choices for John and Mark), **Synergies +** (Shield Up hub, lane through the Cyclone), **Duos +** (FTP freed) | FR +, Synergies − (complexity crowds them out) |
| Cost to find out | 0 | — (withdrawn) | **One house-rule session (no code), then S chunks in order** | Several M chunks before knowing |

Doing nothing is A. It stays the stop-rule fallback, and Lucy's preview is worth building under every column.

---

## Per hero

### John: Shield Up arms the guard; Wrath is the stamina

**Today (verified).** John's handler relays any enemy action that targets a family member within 2 (radius held to 1–2), on any phase, unlimited, 1 FTP each; the hit moves to John at ×0.5 (`JohnFactionRoleHandler`, `receivedDamageModifier`). Wrath (`JohnPassiveAbility_Wrath`): casting Shield Up arms it until John's side starts its next turn; every hit he takes while armed, or through his role, adds a stack (max 3); his next damaging ability spends them all for +35% each (GDD JO-1; the asset's value; the code default is 0.15, so the prefab overrides it). Stacks persist until spent. Shield Up: 1 AP, cooldown 1, ×0.6 damage taken until his next turn, +1 FTP.

**What the onboarding relies on.** Memory 3's lesson is Shield Up → guard → Wrath → the punish (round 1 S2: turn 2 Wrath 2 makes the Sword kill a 10-HP Claw). The River's beat 1 ★ is "John Shield Up beside Lucy ... then a Wrath Shield Dash" (after-Hearth plan). Both survive J1 and J2 unchanged; both break if Wrath is dropped.

**Rules (recommended).**

- **J1. Shield-Up gate.** John's guard answers only while his Shield Up is on. Range stays 2. One sentence: *"John guards the family while his shield is up."* This is THJ's proposal as he wrote it, and it passes the principle test (2): Shield Up is already worth casting.
- **J2. Wrath is the stamina.** Every hit John takes under the shield, his own or a guarded one, adds Wrath as today. **When Wrath fills (3), the shield breaks**: Shield Up ends at once (its ×0.6 too), so no more guards this enemy turn, and he can't raise it again until he spends his Wrath. One sentence: *"Three hits fill his Wrath and break his shield; he has to strike before he can raise it again."*

Why not stamina replacing Wrath, as THJ suggested: THJ's worry was two systems. This is one: the counter that limits the shield is the counter that pays the punish, and it's already on the HUD (Wrath box, popups). A new stamina in hit points would add a bar, a "posture" state and a cooldown rule, and remove the damage half of John's identity, which Memory 3 and the River teach. Counting hits (pips) also reads better than counting damage.

THJ's posture cooldown maps onto J2 directly: the break *is* the posture drop, and "can't raise it until he strikes" *is* the cooldown, set by what he does rather than by a timer.

**Optional J3. Swap at any range (THJ).** On the guard prompt, John and the ally switch places; the hit lands where it was aimed, on John. Range: none.

| Question | Answer |
|---|---|
| Pathing | A teleport, not a walk: no path, ignores walls and gaps (like Encore). Built on `AEffectSwapper` (core), which already raises `unitEndMoving` for both units (D-322) |
| Line of sight | None needed; the grid has none for teleports |
| The attacker's hit | Single target: rewritten to John (today's `RetargetToJohn`). Cell and area attacks: they land where aimed, on whoever is there, so the per-action relay record (`FamilyRoleRelay`) isn't needed. A charge keeps its destination (today's `keepCellTargets`) |
| What it loses | One swap covers one ally. Today's relay covers every ally an area attack catches (the Masher slam on two sisters); the swap covers one, and if John's old tile is also in the area, the ally is still hit there |
| Who it can't reach | Toba (another faction; John's tag query), decoys and protectees; John while Crippled or Stunned (to check which statuses block a swap in `AEffectSwapper`) |
| Side effects | The ally lands on John's old tile, maybe beside other enemies: the next enemy re-plans on the new board. Papa's Shelter forms or breaks. Arrow pickup on a swap: **to check** (LI-7 counts cell-by-cell moves). Linda's Watch: allies don't trigger it |
| The decision it adds | Real, at the prompt: pressing pulls John off his post (a chokepoint, the corridor); declining keeps him there. Today's press has no such cost |
| Readability | The weakest point: the board changes mid enemy turn. Needs a strong swap beat; the tether (FR-13) already draws arcs at any length. John's zone and his cover marker (FR-12) go, one fewer grid layer |
| Cost | M, core (`JohnFactionRoleHandler.Activate` rewritten around the swapper, `GetCellsInRange`, presenters), during an enemy action in progress: the riskiest item in this plan |

J3 is good creatively ("Papa's coming") and gives the press a real cost, but it is the most expensive and least readable item, and J1 + J2 answer THJ's main point without it. **Recommend: test J1 + J2 at range 2 first; decide J3 after (Q3).** A cheap halfway step exists: any range without the swap (John takes the hit from where he stands; the radius clamp is code, small). The fiction is weaker ("how does he take it from across the room?").

**Interactions (J1 + J2).** Shield Flare already needs Shield Up (JO-3), so Shield Up becomes the family's hub: guard, Wrath, Shield Flare, and Command Shield Dash after a Command. Papa's Shelter is unaffected. Bond Lite's "John's role covering the other" source (BO-2) fires less. Masher counters (EN-2) on the player's own turn are guarded only if Shield Up is on that turn. A guard declined still silences that target for the rest of the turn (as built, `Silence()`), which suits "save the shield for Lucy".

**Failure cases.** *Fortress:* John casts Shield Up every turn: bounded by J2 (three hits, then he must strike). *Never armed:* players forget Shield Up, so John's role disappears: the badge shows "Raise your shield to guard" (text, placeholder), and the Shield Up hint in Memory 3 already teaches it. *Too soft for the sisters:* fewer guards; THJ's pacing check says the game is too easy, so partly the point. Watch the sisters' HP at fight end.

**Code (J1 + J2): S.** `JohnFactionRoleHandler.CheckTriggerConditions` gains the shield check (**core**, the handler is on the Family Roles list); `JohnPassiveAbility_Wrath` exposes `ShieldUpActive` and, at max stacks, ends Shield Up (removes its damage-taken modifier; the modifier's id in `John_Ability_Shield.asset` **to check**) and sets a tag that blocks Shield Up (not core). The block can be data: the Shield preset has an `activationTagQuery` (verified present; that it can carry a "Wrath full" block is **to check**). Badge and zone: `RoleBadgeState.cs`, `RoleZonePresenter` (not core) show John's zone only while the shield is up. About 60–100 lines with EditMode tests.

### Linda: the lane she faces

**Today (verified).** Watch fires when an enemy ends a move in her row or column within 4 (radial distance, same row or column; `LindaFactionRoleHandler.GetCellsInRange`), all four half-lanes, spending an arrow and 1 FTP. FR-10 hides her zone because it equals her bow's reach. She starts levels facing east (`initialDirection.x` 1 on `Unit_Linda.prefab`); her sprite only flips left and right (`EntityAnimationHandler`).

**Rules (recommended).**

- **L1. One lane.** *"Linda watches the lane she faces."* Watch fires only for enemies that end a move in one half-lane: the four directions from her tile, up to her arrow's range, units between not blocking (as today). FFT-style, as THJ proposed, but the facing is chosen any time on her turn, not as a forced step at End Turn.
- **L2. The last arrow (data on LI-5).** Watch never spends her last arrow: it needs 2 in the quiver. Today's "empty quiver: no Watch" moves from 0 to 1. Her zone hides at 1, as it does at 0 today.

**Picking the lane (UI).**

| Item | Proposal |
|---|---|
| Default | The direction of her last shot on this turn (bow, Crescendo, a Duo arrow); else of her last move; else what she faced last turn (level start: east). So shooting north and ending the turn watches north, with no extra click |
| Changing it | While Linda is selected on the family's turn, four small arrows at her feet; click one (or press a direction key) to face that way. Free, any time, no AP. **The one new on-screen element, necessary**: without it the choice can't be made |
| Shown | Her lane, drawn with her existing bow icons (FR-8), on the faced half-line only. Because it no longer equals her attack reach, FR-10 stops hiding it: drawn when she is selected, and **kept on the board from End Turn through the enemy turn** (one change to `RoleZonePresenter`), so the player sees what she's watching while it matters |
| Sprite | Flips left and right only (verified); north and south show through the lane alone. Up and down idle frames: **to check** |
| Misread | "Why didn't she shoot that one?": the lane drawn through the enemy turn answers it; the badge tooltip adds the facing ("Watching north") |

The quiver plan rejected "aimed Watch" as "another click per turn" (option E). The default is what answers that: the click is only needed when the player wants something other than the lane she just shot down.

**Interactions.** Encore, pickup and landing are unchanged (a Watch arrow lands as today, LI-6). Tempest Bloom: the loved "Watch through Lucy's Cyclone" now happens when the Cyclone is in her faced lane, so it becomes a choice ("face the Cyclone") rather than an accident; it still lands on the enemy turn, so it keeps some surprise. Catch & Return: facing a lane with Mark in it is how you set the catch up on the enemy turn. Toba's swap and pushes still count as moves (D-322) but only into the faced lane. With the quiver switched off (LI-14) the lane still limits her, which removes D-330's "no limit at all" case.

**THJ's objection, applied to L2.** L2 does bring a small version of it back: on a turn with 3 arrows and a target in reach, the second shot now and a Watch later compete for the same arrow. The difference from kept AP is that Watch costs no AP, so the second AP still buys a move, a Slam or half an Encore, and the facing itself is free. On paper (S1, S3) the lines come out within a hit of each other, which is what a real choice looks like. If THJ finds it reads as "always shoot twice", the lever is to drop L2 (lane only).

**Minimum range 2 (THJ, to discuss).** *"Her bow can't hit a tile next to her."*

- **For:** Watch then only fires on enemies that stop 2 or more tiles away, which in practice means enemies going for someone else: "Family Watch" literally watches over the family. Harmonic Slam (cripple the adjacent ones, step away) gets a job; John's guard and Mark's counter protect her up close. Linda gets weaker, which the "too easy" note wants.
- **Against:** melee enemies end their moves next to their target, so when the target is Linda, Watch never fires; with L1 a lane is 3 tiles (2 to 4), so Watch may fire too rarely to be felt. Her own turn costs a step whenever a Claw is beside her. **There is no minimum-range concept in the code** (searched: no `minRange` or equivalent in `Core/`), so it is core targeting work plus every attack preview (CR-37): M, core. And it breaks tuned levels: Memory 1 (Claws come down the throat to her), The Ridge (the rush ends on 1,1 and 2,2, next to her; Mark starts beside her), Memory 3 (only partly: it removes the Watch prompts on 2,2 and 1,1, which THJ wanted gone anyway). Each to re-check on paper.
- **Recommend:** not in this test. Keep it as Linda's lever if L1 leaves her too strong (Q4).

**Code (L1 + L2): S–M.** `LindaFactionRoleHandler.GetCellsInRange` (both overloads) filters to the faced half-line (**core** handler); a small facing component on Linda (`Features/Player/Linda`, not core) that listens to her own abilities for the default; the picker UI (not core); `RoleZonePresenter` draws her lane through the enemy turn (not core); L2 in the Watch effect's `HasArrow` check or in `LindaQuiver` (not core; whether the check takes a count is **to check**).

### Lucy: free, and shown before it happens

**Today (verified).** Her follow-up fires on any phase when a family member's action (not hers, not the Linda–Lucy Duo) really lowered an enemy's HP within 3 of her: 2 embers × 3 on one enemy, preferring the aimed one (`LucyRoleTargetRanking`), skipping an enemy whose most recent attacker is Lucy. Nothing on the player's turn shows it's coming, and on multi-target hits (a pierce, a Shield Dash) she may pick an enemy the player didn't aim at. That, plus no preview, is "randomly coming about".

**U1. Preview (recommended, all branches, whatever the test says).** While the player previews another Bergson's damaging ability on a target:

| When | Shown | Where |
|---|---|---|
| The previewed hit lowers an enemy's HP, the enemy would survive, and it is within 3 of Lucy (who is alive and not silenced) | Her Fireball role icon (FR-8) on that enemy's tile, in her quadrant | The tile of the enemy her ranking would pick (the same `LucyRoleTargetRanking`, so what the preview promises the action does, CR-37's rule) |
| Same | Her damage as a second segment on its HP bar, in her role colour (the stepped preview's second segment, CR-45) | The target's info panel |
| The hit plus her embers would kill | The lethal skull in her tint (as CR-46 draws the "this click" kill) | Same |
| The hit alone kills, or nothing in her reach is hurt | Nothing (she won't fire) | — |

Enemy-turn follow-ups (after a Watch or a counter) can't be previewed; they stay a surprise, and that's fine. The ranking's "skip the enemy she hit last" is a hidden rule; if the preview shows it confusing people, simplify the ranking after (not now). No new element: an existing icon and the existing second segment, used in a new place. **Code: S–M**, needs its own tech plan: a preview helper next to `LucyRoleTargetRanking` (not core), a hook in the attack preview path (`PlayerController` / `UnitThreatAnalysis`, **core**, additive), drawn through `EntityInfoPanelUI` / `DamagePreviewRules` (UI). THJ asked for this independently of the rest ("needs much better feedback"), so it can go first.

**U2. Ember pool (THJ's alternative): not recommended.** Start 3, +1 a turn, a Focus ability builds more, each follow-up spends one.

- It reads as the quiver re-themed, which THJ named himself. The family would carry four counters: Wrath, arrows, Mark's Focus, embers.
- It caps the follow-up but adds no choice: the follow-up stays automatic, so "just a click" stays. Pilot 1's cap (Lucy 3 a round, D-042) was the same idea, never built.
- Her Focus ability arms the role by giving up an action: the kept-AP problem again (1 AP for embers later vs an ember attack now).
- "Focus" is Mark's resource (Atman's Focus, MA-1): the name needs to change if it's ever built (`miso-narrative`).
- Cost: M (a resource like the quiver, HUD, an ability, the handler gate, core).

**U3. Principled fallback, if U1 still feels random: Kindle.** *"Lucy follows up on enemies her own embers hit since her turn."* Armed on her turn by her own verb; it makes order matter (Lucy first, then the others). Costs one mark on the enemy (a new element, or Burn's look) and a filter in her handler (core), and roughly halves her follow-ups. Q5.

Her follow-ups already fire less often than Linda's (they need a family hit within 3 of her), so leaving her free is the cheapest place to keep one "instinct" role.

### Mark: three options

**Today (verified).** Mark's counter fires only on the enemy's phase (`activationPhase` 4 on `Unit_Mark.prefab`; the others fire on every phase), after an enemy's action hits a family member other than Mark (his handler skips himself), if the attacker is within 2; it is his Fist Blitz (8). Atman's Focus: +1 per basic attack he lands (max 5), Focus is damage (+1 to +5) and a barrier (3 to 9), a hit costs 2 Focus. **The counter, being his Fist Blitz preset, also earns Focus** (`OnAbilityPerformed` counts any basic-attack preset of his, and his handler raises `abilityPerformed`; read in code, not tested).

| | **M1. Free, as built** | **M2. Counters spend Focus (recommended)** | **M3. Bodyguard** |
|---|---|---|---|
| Rule | As today | *"Mark's counter spends 1 Focus."* Counters earn none | *"Mark counters for the family member he ended his turn beside."* |
| Armed by | Nothing (position, incidentally) | His Fist Blitzes on his own turn (principle 3) | His move (principle 1) |
| The press | Always yes | A real choice: Focus is his barrier and damage, so a counter makes him easier to hurt | Always yes |
| New to learn | 0 | 1 condition; Focus pips exist | 1 condition, his zone changes |
| Start of a level | Counters at once | Focus 0: no counter until he has landed a Blitz (lever: start at 1) | Counters at once |
| Code | 0 | S: `MarkFactionRoleHandler` check and spend (**core**), `MarkPassiveAbility_AtmanFocus` a `TrySpend` and no gain from the role's own instance (not core) | S–M: the handler's target rule (**core**) and his zone (not core) |
| Risk | The odd one out: three roles armed, one free | Mark's role rarely seen early; Focus balance (barrier drains faster) | Positional rules on top of a positional role |

M2 is THJ's "quiver re-themed" idea placed where a resource already exists. It also bounds the Masher counter loops (D-097, D-098), since each counter costs Focus. **Recommend M2, with M1 as the fallback** (Q6). Mark isn't in the Hearth's roles (after-Hearth plan F3), so his first counters are in The Ridge.

### Every role: no FTP

Under P, roles cost no FTP (D-036, never built). FTP becomes the Duo meter only (D-216), as round 1 also wanted. Cheapest: `requiredFTP` 0 on the four role components (data, Tier 3).

---

## Lens notes

### Creative

**Target experience.** Each Bergson looks after the family in their own way, and you set it up with what they already do: John raises his shield, Linda turns to face the corridor, Mark builds his Focus in the fight, Lucy's fire follows wherever the family strikes. On the enemy's turn you watch your plan play out, and twice a turn you choose: does John take this hit, and break his shield, or let Lucy take it? Does Mark spend his calm on a counter?

**The moment designed for:** the enemy turn where John is on two Wrath and a Claw goes for Lucy. Press, and his shield breaks; he'll have to strike next turn, with everything he took. Warmth (he takes it for her) against dread (now nothing guards Linda).

**Original or default?** Shield-gated guards and facing lanes are known (FFT's facing, XCOM's overwatch cone). What stays Miso is that the four answers differ and feed each other: Shield Up is also Shield Flare's condition, Linda's lane is also where Mark catches and the Cyclone splits, the Wrath you build by guarding is what the punish spends. The swap (J3) would be the most original piece; it's held back for cost, not for taste.

**Creative vs systems.** Creative wants J3 now (the father who runs across the room). Systems wants the cheapest test first. I lean to systems for the order and put J3 to THJ (Q3).

### Systems

**The rules (P).**

1. John's guard answers only while his Shield Up is on; range 2 (J1).
2. Each hit he takes under the shield adds Wrath (as built); when Wrath fills, the shield breaks and can't be raised until he spends it (J2).
3. Linda's Watch fires only in the half-lane she faces (L1), and never with her last arrow (L2).
4. Lucy's follow-up as built, shown in other heroes' attack previews (U1).
5. Mark's counter spends 1 Focus and earns none (M2).
6. Roles cost no FTP.

**Levers and starting values.**

| Lever | Start | Range | Where |
|---|---|---|---|
| John's guard range | 2 | 2 → any (J3, or any without the swap) | Handler |
| Hits before the shield breaks (Wrath max) | 3 | 2–4 | `maxStacks` on the Wrath passive (data) |
| Wrath per stack | +35% (asset) | 25–40% | Prefab (data) |
| Linda's lane length | Her arrow range (4, Longshot 5–6) | — | Existing |
| Arrows Watch must leave | 1 | 0 (off) – 1 | Rule (L2) |
| Mark's counter cost | 1 Focus | 1–2 | Rule (M2) |
| Mark's Focus at level start | 0 | 0–1 | `AtmanFocus` (data) |
| Lucy | Free, no limit | U3 if still random | — |

**Interactions** are listed per hero above. Across heroes: John's Shield Up + Lucy beside him (Papa's Shelter) + her ember on him (Shield Flare) is now the family's planned defensive turn, which is what the River teaches. Linda facing a lane that holds both Mark and the enemy behind him sets up Catch & Return on the enemy turn. Mark's counters no longer chain freely with the Masher's (EN-2).

**Failure cases.**

- *Linda's lane is never hit:* Watch fires on under about 1 in 4 enemy turns where enemies are awake and in range. Lever: drop L2 first, then widen to two lanes (her row or her column).
- *Facing is never changed:* the default always fits. Not a failure: the default is the choice when it's obvious; watch whether S3-like boards make players change it.
- *John fortress:* Shield Up every turn with Wrath under 3: possible when enemies hit him rarely; then lower Wrath max to 2.
- *Mark absent:* counters under one a fight because Focus is spent or broken. Lever: start Focus 1.
- *Too hard:* the sisters lose most guards; hits that were free are now real. THJ's pacing check asks for this; watch HP at fight end and rounds per fight (target 1.6–2.6, `combat-balance.md`).

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| John's turn | Badge: Ready only while Shield Up is on; his zone drawn only then | Shield Up (as now) | "John stopped guarding": the badge tooltip says "Raise your shield to guard" |
| John's shield breaks | Popup "Shield broken" (placeholder) in the Wrath colours; Shield Up greyed with "Strike first" | — | "Why can't I raise it?": the greyed tooltip |
| Linda's turn | Her faced lane in her bow icons; four arrows at her feet while selected | A direction (only to change the default) | Thinking the lane is her attack reach: it's drawn only on one side, so it reads as a direction |
| End Turn to enemy turn | Linda's lane stays drawn; John's zone stays if the shield is up | — | "Why didn't she shoot that one?": it wasn't in the drawn lane |
| Another hero's attack preview | Lucy's icon on her pick, her damage as a second segment, skull in her tint if together lethal | The attack | Taking the skull as certain: it needs the press, like every role |
| Mark's prompt | Focus pips (existing) drop by one on press | The key, or not | "Pressing costs nothing": the pip drop on the first press teaches it |

One new element (Linda's facing arrows). John's zone shows less often, Linda's zone shows on one side, Lucy's preview reuses an icon and a segment. Net, fewer tiles marked on the board than today.

---

## Complexity budget

THJ: "too many mechanics, too little challenge" (pacing check). D-295: one sentence per feature, at most one new element, name what it replaces.

| Item | Player learns (+) | Goes away (−) | On screen |
|---|---|---|---|
| Roles cost no FTP | — | "Roles spend FTP", running dry (−1) | — |
| J1 Shield-Up gate | "Guards while the shield is up" (+1) | "John guards anyone within 2, always" | John's zone shows less |
| J2 Wrath breaks the shield | "Three hits break it; strike to raise it again" (+1) | — (Wrath already taught) | Popup, greyed button (existing pieces) |
| J3 Swap at any range | "He switches places" (+1) | His range rule (−1); his zone and cover marker (−2 elements) | Swap beat |
| Stamina replacing Wrath | A stamina amount, posture, cooldown (+3) | Wrath (−1) | A bar (+1) |
| L1 One lane | "She watches the lane she faces" (+1) | FR-10's hiding exception (−1, a UI rule) | Facing arrows (+1) |
| L2 Last arrow | A value on an existing rule (+0.5) | — | — |
| Minimum range 2 | "Not next to her" (+1) | — | Previews change |
| U1 Lucy preview | 0 | The surprise on the player's turn | Reused icon and segment |
| U2 Ember pool | A resource, refill, an ability (+3) | — | A counter (+1) |
| M2 Focus counter | "Counters spend Focus" (+1) | — | Existing pips |

**The recommended set P** (no FTP, J1, J2, L1, L2, U1, M2): about +4.5 to learn, −2, one new element. **P+** (adds J3, stamina, minimum range, ember pool): about +12, −5, four new elements.

**What to cut if P is adopted** (each one goes to THJ, none is quietly dropped):

1. Roles' FTP cost, and with it the "FTP drain" teaching in the first hour (already delayed, after-Hearth plan).
2. From the design: Pilot 1's per-round caps (FR-4) and the "Watch 2/2" label (FR-6), never built; kept AP (round 1), withdrawn.
3. FR-10's hiding rule for Linda becomes dead code by itself (her zone no longer equals her reach); Lucy's still applies.
4. Not adding stamina as its own system (Wrath carries it), the ember pool, and minimum range in this round.
5. Later, if the swap is adopted: John's zone and cover marker.

---

## Paper scenarios

Same frames as round 1, read again from the prefabs on 2026-11-09 with `level_to_grid.py` (`GB_s2-ridge`: the plan's tiles are the prefab's plus one in x, with a border; `GB_m3-john`: plus one in x and y, with a border; both unchanged since round 1). x from the left, y from the bottom. **AI paths are assumed** (shortest path to a free tile beside a target; order where it matters is stated). Values: Tutorial Claw HP 10 (16 × 0.6, rounded as round 1), Claw hits ≈3 at Tutorial ×0.5 (round 1's figure, assumed), Linda's bow 6 (×0.6 per further enemy), Crescendo 8 on a cell within 5 and its neighbours, Fist Blitz 8 within 2, Mark's move 3 (`Mark_Ability_Walk.asset`, 3 × `Stat_SPD`, SPD 1 assumed), Claws move 4, Wrath +35% a stack.

### S1. The Ridge, rush pack, turn 1 (Linda + Mark), as built

Gauntlet (7,1, 8,1) asleep. 2,4 starts Alerted (3 from Linda) and wakes 1,5 and 3,5 (EN-15). Linda faces east at level start.

```grid id=rr2-s1-perhero title="S1 The Ridge, per hero: one arrow now, Linda faces north (GB_s2-ridge)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,2 2,3 2,4 2,5 linda faced lane: north
arrow 2,1 2,4 linda dx=-8 one shot (10 to 4)
arrow 2,4 2,3 2,2 enemy dx=8 Watch kills it
arrow 1,5 1,4 1,3 1,2 1,1 enemy
arrow 3,5 3,4 3,3 enemy
arrow 3,1 3,2 mark
step 2,2 1
note 2,1 2 arrows left
```

| Line | Player's turn | Enemy turn | Grade |
|---|---|---|---|
| **Per hero ★ (drawn): one arrow, face north** | Linda shoots 2,4 once (10 → 4; quiver 3 → 2); she shot north, so she faces north with no click. Mark has nothing in reach (2,4 is 4 away, Blitz 2) and steps to 3,2 beside her; Focus 0, so no counter is armed | 2,4 runs to 2,2, beside both, and ends in her lane: **Watch** (6 ≥ 4, dead before it strikes; quiver 1). 1,5 reaches 1,1 (west, not faced) and strikes Linda; 3,5 reaches 3,3 and strikes Mark | ★ |
| Spend everything | Linda shoots 2,4 twice (dead; quiver 1: Watch off by L2). Mark steps up | 1,5 and 3,5 strike unanswered | ● |
| Face west instead | As ★, but she turns west (one click) | 1,1 is her west lane: Watch on 1,5 (10 → 4), it survives and strikes; 2,4 strikes her from 2,2 | ✗ (worse) |
| Today | Two shots on 2,4 | 3 prompts (Watch, two counters), 0 choices (round 1) | — |
| **Count (per hero)** | **2 decisions** (one arrow or two; which lane) | **1 prompt, traced to both** | |

Against THJ's objection: "two shots now" and "one shot + Watch" both kill 2,4 before it strikes and both leave one arrow; the Watch line frees an AP and risks 2,4 not ending in the lane. Close to even, so a real choice, not a dominated one. Mark's role is absent here under M2 (Focus 0 at start), and also as built (no ally is hit within 2 of him), so the Ridge's opening shows no counter either way.

### S2. Memory 3, John's telling (John 1 AP, sisters 0 AP), as built

Five Claws, all alert; (4,4) acts first, straight at John (D-393). John's guard radius 2 drawn as round 1 did (radial assumed). Linda faces east (prefab), and has no AP.

```grid id=rr2-s2-perhero title="S2 Memory 3, per hero: Shield Up arms the guard, Wrath breaks it (GB_m3-john)"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
zone 2,1 6,3 john shield up: guard on
cells 3,1 5,1 linda faced lane: east
arrow 4,4 4,3 4,2 enemy first: John, Wrath 1
arrow 6,5 6,4 6,3 6,2 enemy guard, Wrath 2
arrow 7,4 7,3 7,2 7,1 enemy guard, Wrath 3: breaks
arrow 2,5 2,4 2,3 2,2 enemy unguarded
arrow 1,4 1,3 1,2 1,1 enemy unguarded
step 6,2 1
step 7,1 2
note 4,1 Shield Up
```

| | Per hero (J1 + J2, L1) | Grade |
|---|---|---|
| Player's turn | John: Shield Up (hinted; his only AP). The guard is armed **because** of it. Sisters: nothing | One decision, hinted |
| Enemy turn | (4,4) strikes John (×0.6): Wrath 1. (6,5) → 6,2 on Lucy: **guard prompt** (Lucy is 2 from John): press, John takes ×0.5 × 0.6: Wrath 2. (7,4) → 7,1 on Lucy: **guard prompt**: press, Wrath 3, **the shield breaks**. (2,5) → 2,2 and (1,4) → 1,1 strike Linda (20 HP), unguarded. No Watch (she faces east; 3,1 and 5,1 stay empty). No follow-up (no family damage) | |
| The choice inside the turn | Decline the second Lucy prompt and Lucy takes one hit (≈3 of 15), but the shield holds for one of Linda's two. Order matters and the shield is limited, so the press means something. (Declining silences Lucy for that turn, as built) | ★ |
| Turn 2 | Wrath 3: Sword 8 × 2.05 = 16.4 kills a Claw, or Shield Dash 4 × 2.05 ≈ 8.2 each with a push beside the sisters. He can't raise the shield before striking: the memory's lesson is now a rule, not only a hint | ★ the lesson |
| J3 variant (swap) | The first guard swaps John (4,1) and Lucy (6,1): Lucy lands beside (4,4)'s Claw, which has acted; (7,4) re-plans on the new board and probably strikes John at 6,1 (Wrath 3, break). Same count, more movement to follow | ● readable? |
| **Count** | **2 prompts** (today 6), each answering the Shield Up; **1 real press choice**. Only John's role fires, with no per-level switch: the sisters' roles are quiet because Linda faces east and nothing hurts an enemy | |

### S3. The Ridge with the pack awake, turn 1: which way does Linda face?

The new scenario. The same as-built tiles with every enemy awake (the level's "all enemies start alert" flag, MI-27; the after-Hearth plan wants an awake Ridge pack), so threats come from two directions: the rush down the north pocket, the gauntlet along row 1. Mark's line is fixed so the choice is Linda's: Mark moves 3,1 → 3,3 and Blitzes 2,4 (2 away; 10 → 2; Focus 1), ending beside it on 3,4 (assumed). The rush then goes for Mark.

```grid id=rr2-s3-lane title="S3 The Ridge, all awake: Linda faces east (GB_s2-ridge tiles)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 3,1 4,1 5,1 6,1 linda faced lane: east
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz
arrow 2,1 7,1 linda dy=-10 Crescendo on 7,1
arrow 7,1 6,1 5,1 4,1 3,1 enemy dy=6 Watch kills it
arrow 8,1 7,1 6,1 5,1 4,1 enemy dy=14 no Watch: last arrow
arrow 1,5 1,4 1,3 2,3 enemy
step 3,1 1
note 2,1 2 arrows left
```

| Line | Linda's turn | Enemy turn (gauntlet moves first, assumed) | Result | Grade |
|---|---|---|---|---|
| **East (drawn)** | Crescendo on 7,1 (5 away): 7,1 and 8,1 both 10 → 2 (quiver 2). Faces east (she shot east). One AP left: stays | 7,1 runs to 3,1 to strike her, ends in her lane: **Watch** kills it before it strikes (quiver 1). 8,1 ends on 4,1, can't reach her; no Watch (L2). North: 2,4 (2 HP) and 3,5 strike Mark from beside him, 1,5 reaches 2,3 and strikes him: three hits on Mark (the first soaked by his Focus-1 barrier, which then breaks) | Linda 0 hits, Mark 3. One gauntlet Claw dead, one at 2; 2,4 at 2 | ★ |
| North | Shoots 2,4 (2 HP: dead; quiver 2). Faces north | 7,1 (10) reaches 3,1, strikes Linda (not her lane). 8,1 ends on 4,1. 1,5 comes 2,5 → 2,4 to reach Mark, ends in her lane: **Watch** (10 → 4; quiver 1), then strikes Mark; 3,5 strikes Mark | Linda 1 hit, Mark 2. 2,4 dead; gauntlet untouched | ★ |
| Spend | Crescendo east and shoots 2,4 (quiver 1: no Watch) | 7,1 (2 HP) strikes Linda from 3,1; 1,5 and 3,5 strike Mark | Linda 1 hit, Mark 2. 2,4 dead, gauntlet both at 2 | ● |
| Today (all four lanes, 1 FTP each) | Any of these | Watch on 3,1 **and** on 4,1 **and** on 2,4, until the quiver is empty; she starts turn 2 with 0 arrows (THJ's complaint) | | — |

**Count:** **3 decisions** on Linda's turn (which target, how many arrows, which lane), 1 prompt in each per-hero line, each traced to the facing. The three lines end within one hit of each other and differ in **who gets hurt** (Linda at 20 HP or Mark at 15) and **which group is thinned**: a real choice. Today the same board gives three or four Watch prompts and an empty quiver.

---

## Recommendation

**P, the per-hero set: roles cost no FTP; John guards while his shield is up (range 2) and Wrath breaks the shield at 3; Linda watches the lane she faces and never spends her last arrow; Lucy stays free and shows in the other heroes' previews; Mark's counter spends 1 Focus.** Kept AP is withdrawn (C1 and C2 on the shelf). Deferred to THJ: John's swap at any range (Q3), Linda's minimum range (Q4). Not recommended: stamina as a new system (Wrath carries it), the ember pool.

The stop rule of D-460 stays: if the house-rule session says the gates don't feel like decisions, lock roles as built (free, D-036), ship Lucy's preview, and move the energy to Synergies.

### Step 1: paper (this plan, about 15 minutes)

S1 to S3 above. Pass if each per-hero line gives at least one real decision on the player's turn and every prompt traces back to one.

### Step 2: house-rule session (no code, one evening)

Play Memory 3, the River (John + Lucy), the Ridge (as built, and once with "all enemies start alert" if THJ ticks it in the level, which is data), and one M4 or M6 fight, on `main`.

| Hero | House rule | What it can't simulate |
|---|---|---|
| All | Press **L** first (+99 FTP), so FTP never limits a role | — |
| John | Press his guard only while Shield Up is on. When the Wrath box shows 3, decline every further guard that turn, and don't cast Shield Up again until he has attacked | His ×0.6 staying on after the "break" |
| Linda | At End Turn, say her lane out loud (default: the way she last shot). Press Watch only for an enemy that ended in that lane. Don't press while her quiver shows 1 | The lane isn't drawn; judge it in the 1 s window, and let it go when unsure |
| Lucy | Unchanged | The preview (needs code) |
| Mark | Press his counter only while his Focus shows 1 or more | The Focus spend (not deducted) |

Side effects to ignore, as in round 1: let-pass prompts still appear, play the decline bark, and silence that target for the turn.

**Read after the session:** Did raising the shield feel like choosing to guard? Did the shield breaking change what John did next turn? Did picking a lane feel like a choice, at least once a fight? Did Mark's counter feel earned? Were fights harder? Two clear noes on John and Linda: stop, lock as built, Synergies.

### Step 3: code, in this order (each behind Global Settings toggles, D-463)

| Order | Chunk | Size | Core items (Tier 3) |
|---|---|---|---|
| 0 (any time, all branches) | Lucy's preview (U1) | S–M | The attack preview path (`PlayerController` / `UnitThreatAnalysis`), additive |
| 1 | Roles cost no FTP; J1; J2 | S | `JohnFactionRoleHandler`; `requiredFTP` data on four prefabs; the switch in `GlobalSettingsSO` |
| 2 | L1 (facing, picker, lane through the enemy turn); L2 | S–M | `LindaFactionRoleHandler` |
| 3 | M2 | S | `MarkFactionRoleHandler` |
| Later, only if THJ asks | J3 swap at any range | M | `JohnFactionRoleHandler.Activate`, `AEffectSwapper` use mid enemy action |
| Later, only if Linda stays too strong | Minimum range 2 | M | Targeting and range helpers in the ability system, every attack preview |

Switch shape: one toggle per rule in Global Settings beside the AP and passive modes (D-463), each defaulting to "as built", so THJ can turn one hero's rule off without a rebuild. Each chunk needs the coordinator's tech plan.

**Playtest signal.** *Worked:* players say why a role fired ("his shield was up", "she was facing the corridor"); John's shield breaks at least once a fight and he strikes the next turn (combat log: Wrath lines); Linda's facing changes from the default at least once a fight on two-front boards; Watch leaves her an arrow on her own turn; fewer prompts per enemy turn than today; at least one planned role + Synergy a fight (Shield Flare off a raised shield, Watch through the Cyclone, a catch); rounds per fight toward 1.6–2.6. *Failed:* Linda's Watch fires on under about 1 in 4 enemy turns with enemies in range (drop L2, then widen); John's role unseen because Shield Up is never cast (badge text, Hearth hint); Mark's counter under one a fight (start Focus 1, then M1).

### What it means for the Hearth

| Memory | Under P | Versus kept AP |
|---|---|---|
| 1 (Linda) | The FP drain no longer silences Watch (roles are free), and the throat is exactly the lane she faces: Watch fires unless the level turns her role off. **Needs the per-level, per-hero role switch** (after-Hearth F1/F2) or the drain kept for that level | Kept AP silenced it for free; P doesn't |
| 3 (John) | Only John's role fires, with no switch (S2). The lesson (Shield Up → guard → Wrath → strike) becomes the rule | Same result, without the AP-limit change |
| 4 (Mark) | Mark: Focus 0, no counter. John: only with Shield Up. Linda: one lane. Lucy's follow-ups on the player's turn still fire. **Needs the switch** if THJ wants no roles at all | Mostly automatic under C |
| River, Ridge | Their ★s hold: Shield Up + Wrath Shield Dash (River), Explosive Arrow + Blitz chain (Ridge). The River gets harder by itself (fewer free guards) | Similar |

So P costs the onboarding one small core item that C didn't: the per-level role switch the after-Hearth plan already asked for under A or B.

---

## USP check

- **Family Roles:** strengthened. Four different arms (a stance, a facing, a resource, an instinct), each set on the hero's own turn; John's and Mark's presses become real choices.
- **Synergies:** strengthened. Shield Up becomes their hub (guard, Wrath, Shield Flare, Command Shield Dash); Linda's lane is where the Cyclone split and Mark's catch happen on the enemy turn, by choice. Lucy's preview shows the follow-up combo before you commit.
- **Duos:** cleaner: FTP is the Duo meter only.
- **Managing the Home as a Family:** neutral on purpose. Note: `thj/home-test`'s Fireside "first Family Role free" means nothing once roles are free; it needs a new payoff if that branch merges (e.g. John starts the sortie with his shield up), for a later plan.

## Critics

*Placeholder: the coordinator runs three critics (creative, systems, UX) on this draft and sends their notes back for reconciliation.*

---

## Questions for THJ

**Q1. Replace the kept-AP test with this per-hero test, under the same stop rule?**
- Context: kept AP is dominated whenever a target is in reach (round 1 revisited); its one live part was John, and his Shield Up carries it better. D-460 to D-463 approved the kept-AP steps; D-461 (player-turn roles free) still fits; D-462 (John's one guard per kept AP) would be replaced by J1 + J2; D-463 (the switch's home) holds.
- Options: (a) per-hero test: paper, one house-rule session, then the code order above; (b) run the kept-AP session anyway as a comparison; (c) lock roles as built now (free, D-036) and move to Synergies, keeping only Lucy's preview.
- Recommendation: (a).
- Blocked: every Family Role chunk, the per-level role switch, the Hearth's role exposure (after-Hearth Q2).

**Q2. John's limit: should Wrath be the stamina?**
- Context: you proposed a stamina that drops the shield, with Wrath possibly dropped. Wrath already counts the hits John takes under the shield, it's on the HUD, and Memory 3 and the River teach it.
- Options: (a) Wrath breaks the shield when it fills (3), and he can't raise it until he strikes; (b) a separate stamina (in damage), Wrath removed, Memory 3 and the River's ★s redone; (c) no limit: the Shield-Up gate alone.
- Recommendation: (a). One counter, two jobs, nothing new on screen.
- Blocked: the J2 chunk; the house rule's "decline at Wrath 3".

**Q3. John's swap at any range: now, later, or never?**
- Context: it makes the press a real cost (John leaves his post) and is the most original part, but it's the riskiest code (a core swap mid enemy action), loses the area guard (one swap, one ally), and reshuffles the board on the enemy turn.
- Options: (a) after J1 + J2 are played, as its own chunk; (b) any range without the swap (cheap, weaker fiction); (c) keep range 2.
- Recommendation: (a), deciding after the session.
- Blocked: nothing in the first test.

**Q4. Linda: the facing picker, the last arrow, and minimum range.**
- Context: the lane defaults to the way she last shot, so the click is only needed to look elsewhere; L2 keeps an arrow for her turn (your complaint) but brings back a small "shoot now or keep it" choice; minimum range 2 has no support in the code (core targeting work) and breaks Memory 1's throat and the Ridge's opening.
- Options: (a) lane with the default and the picker, plus L2, no minimum range; (b) lane only (no L2); (c) lane plus minimum range in the same test.
- Recommendation: (a); minimum range kept as her lever if she stays too strong.
- Blocked: the L chunk; the per-level switch for Memory 1.

**Q5. Lucy: preview now, on every branch?**
- Context: you said she can stay free but needs much better feedback. The preview reuses her icon and the stepped damage segment, and follows her real target ranking. The ember pool reads as the quiver re-themed, adds a fourth counter, and its Focus ability has the kept-AP problem (and Mark's name).
- Options: (a) preview now (independent of Q1); (b) preview, and Kindle (she follows up only on enemies her embers hit) if it still feels random; (c) the ember pool.
- Recommendation: (a), with (b) as the fallback.
- Blocked: Lucy's preview tech plan.

**Q6. Mark: does his counter need an arm?**
- Context: he wasn't in your proposal. As built, his counter is free, enemy-phase only, for an ally hit within 2 of him, and it earns Focus. With the others armed, a free Mark is the odd one out.
- Options: (a) counters spend 1 Focus and earn none; (b) free as built; (c) he counters only for the family member he ended his turn beside.
- Recommendation: (a), with Focus 0 at level start as a value to watch (lever: 1).
- Blocked: the M chunk; the Ridge's house rule.

Names for `miso-narrative` if approved: the "Shield broken" popup, Linda's facing tooltip ("Watching north"), John's badge line.

## Docs to update (if approved)

After the test, and only for what's adopted:

- `design/gdd/family-systems.md`: FR-3 (no FTP: built), FR-4 and FR-6 (dropped), John's, Linda's and Mark's role rows (arm conditions), a new **FR-14** for the arming principle (next free FR ID), FR-9 and FR-10 (Linda's lane drawn through the enemy turn; FR-10 no longer applies to her), a new FR rule for Lucy's preview (or CR, beside CR-45 and CR-46), the Deferred table (kept AP and its variants; ember pool).
- Character pages: John JO-1 (Wrath breaks the shield; Q1 there), his role line; Linda LI-5 (threshold), LI-11 (the lane), LI-14 (the lane with the quiver off); Lucy's role line; Mark MA-1 (Focus spent by counters).
- `design/gdd/combat-rules.md`: CR-6 (roles free), CR-13 (FTP pays Duos only).
- `design/combat-balance.md`: the "2 reactions per hero per round" assumption.
- Onboarding: the after-Hearth plan's Family Role dependencies table (P column), Memory 1's FP drain, Memory 3's lesson text.
- `plans/family-role-chunk.md`: items superseded.
- `glossary.md`: the facing and shield-break terms if named.
- `decisions.md` (coordinator): Q1 to Q6; the Family Roles test rows were renumbered D-460 to D-463 (they had collided with the Lucy-memory gag's D-457 to D-459).

Grids in this plan, to render: `rr2-s1-perhero`, `rr2-s2-perhero`, `rr2-s3-lane`.

## Branches

- **`main`** (and everything that was `thj/onboarding`, D-456): the test and any switch go here.
- **`thj/home-test`**: no quiver (L2 has no meaning there until the merge), roles at 1 FTP, Fireside "first Family Role free" (D-040) to remap once roles are free.

## Risks

- **Linda's Watch too rare** with one lane and L2: levers in order (drop L2, then two lanes).
- **John's role forgotten** when Shield Up isn't cast: the badge line and Memory 3's hint.
- **Mark absent early** (Focus 0): start Focus 1, or M1.
- **The onboarding needs the per-level role switch** (Memory 1, Memory 4) that kept AP would have avoided: small core item, already asked for by the after-Hearth plan.
- **AI paths in the paper test are assumed**; the session is the real check.
- **Scope creep** into the swap and minimum range: both held behind THJ's questions.
- **Values assumed:** Claw hits ≈3 at Tutorial, Mark's move 3, Linda's start facing east (read from the prefab), the counter earning Focus (read, not tested).

## Gates

Design only. Step 1: THJ's time (~15 min). Step 2: THJ's time (one session, no code). Step 3: tech plans (coordinator) → implementer (compile, EditMode tests) → reviewer → THJ play check per chunk. Docs only after adoption.
