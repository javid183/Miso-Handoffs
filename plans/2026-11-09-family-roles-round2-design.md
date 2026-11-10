# Family Roles, round 2: armed on the hero's turn, fired for the family

Size: L    Tier: 3 (the rule of a main mechanic and a USP; core role handlers and settings for any prototype)    Assigned to: miso-game-designer
Branch: all. `main` since THJ merged `thj/onboarding` on 2026-11-09 (D-456). `thj/home-test` notes in [Branches](#branches).
Status: waiting on THJ (critics reconciled, 2026-11-09)

## Why

Round 1 ([`2026-11-09-family-roles-rethink-design.md`](2026-11-09-family-roles-rethink-design.md)) recommended **C, kept AP**, and THJ approved its test (D-457 to D-460), then paused it before playing with an objection: *"What makes players keep their AP instead of using it? If there are enemies alive while shooting with Linda, why should I not spend it right away? ... For John it's a bit different: he's not ranged and might not reach. Does this not require extra AP? Is 2 enough?"* He made a counter-proposal per hero (John: Shield Up gate, stamina, swap at any range; Linda: facing lane, minimum range 2; Lucy: free with better feedback, or an ember pool; Mark: not covered) and asked for a designer and critics discussion before deciding anything. This plan is that discussion: my draft (P), three critics, and the revision (P2).

## Goal

Settle where kept AP stands, turn THJ's proposal into per-hero rules where each hero has a real decision, and recommend one set with a test that needs no code first, under a stop rule that can't kill an idea before it's played.

## Acceptance criteria

- [x] Round 1's scenarios rechecked against THJ's objection, with a plain verdict on C and its variants.
- [x] The per-hero principle compared with A and C.
- [x] Each hero: rules, values, interactions, failure cases, files and core status; THJ's items weighed.
- [x] A complexity count (recounted with the UX critic's numbers), and what to cut.
- [x] S1 and S2 redone, a Linda scenario and a John scenario added, decisions and prompts counted after the critics' corrections.
- [x] The test: what a house-rule session can and can't show, then code in order.
- [x] Critics reconciled; recommendation and at most six questions in the five-part format.

## Scope

In: the arming rule and trigger of each role, John's Wrath as a limit and his swap, Linda's trigger (family filter or facing), Lucy's preview and trigger, Mark's options, the readability the arms need, the FTP economy once roles are free, the test.
Out: role effects beyond what is listed, enemy AI, the Cyclone redesign, level rebuilds (flagged only), the graded QTE (named as the next experiment), the Fireside mapping (noted).

## Touches

Systems: Family Roles (core: `FactionRoleHandlerBase`, the four Bergson handlers, `FactionControllerBase`), settings (core: `GlobalSettingsSO`), `AEffectSwapper` (core, for the swap), John's Wrath and Blood Debt passives, role zones, role badge and the prompt UI (not core), the attack preview (UI plus the core preview path).
USPs: Family Roles (main), Synergies, Duos (FTP), Home (Fireside note).
Docs: [Docs to update](#docs-to-update-if-approved).

## Approach

Recheck round 1, state the principle, design each hero, take the three critics, revise, count the complexity, play it on paper, then a two-step test with a stop rule per hero.

Read for this plan (2026-11-09): round 1; the three critic notes (`2026-11-09-family-roles-round2-critic-creative.md`, `-systems.md`, `-ux.md`); `vision.md`; the GDD (`family-systems.md`, `combat-rules.md`, `enemies.md`, the four character sheets); `combat-balance.md`; `decisions.md` (D-036 to D-042, D-216, D-244, D-246, D-292 to D-295, D-322, D-323, D-350, D-393, D-457 to D-460); the after-Hearth plan; `tech/core-systems.md`; code: `FactionRoleHandlerBase.cs`, the four Bergson role handlers, `JohnPassiveAbility_Wrath.cs`, `JohnPassiveAbility_BloodDebt.cs`, `MarkPassiveAbility_AtmanFocus.cs`, the role components on the four `Unit_*.prefab` (`requiredFTP`, `requiredTimeScale`, `activationPhase`, `oncePerPhase`), `Mark_Ability_Walk.asset`, `John_Ability_Shield.asset`; prefabs `GB_s2-ridge`, `GB_m3-john`, `GB_s1-river` read back with `level_to_grid.py`.

---

## Problem and evidence

### Round 1 revisited: THJ is right

**Kept AP fails where it was supposed to work.** The decision C promised was "spend this AP now, or keep it for the role". That is only a decision when the kept answer is worth about as much as the action it replaces.

- **A kept answer is the same action, later and conditional.** Linda's Watch is her bow shot (6, an arrow; LI-11). Mark's counter is his Fist Blitz preset (8). Lucy's follow-up is about one ember attack. Shooting now hits the target you choose, for sure, and can kill it before it acts. So with a target in reach, **spending now is at least as good, almost always**.
- **Keeping only happens when it is free or when nothing else can do the job.** Nothing in reach: keeping costs nothing, so it isn't a decision. An answer no action can give: only John's guard (you can't prevent a hit on your own turn). Keeping that changes what the enemy does (zone denial): our AI has no role-zone input (`UtilityVariables.cs`), so it doesn't exist.
- **For a melee hero 2 AP is not enough.** A melee turn is move + attack; keeping one AP gives up the attack whenever he has to move.

| Round 1 scenario | Claimed | What holds | Verdict |
|---|---|---|---|
| S1 The Ridge, K1 (Linda keeps 1, Mark keeps 2) | A kill box | Linda's second shot kills 2,4 now, for sure. Mark's keep was free only if he couldn't reach; in fact he can move 3 and Blitz 2,4 (systems critic), so his keep was a mistake | Dominated |
| S1, K3 (Mark Blitzes, Linda keeps both) | Aggressive | Worse for Linda than two shots; the only real choice is Mark's, an ordinary turn | No role decision |
| S1, K2 (spend everything) | Costs HP | The line a good player takes; with C they see no roles | Honest default |
| S2 Memory 3 (Shield Up + keep 1) | The lesson | Real for John (no own-turn way to prevent a hit), but it needed John's turn-1 limit raised and its best part came from the guard being limited, not from AP | John's verb, not AP |
| S3 The River (John step + keep 1) | One choice | Real for John only, for the same reason | John only |

**C, as tested, doesn't survive.** Its one live part was John. Two variants go on the shelf: C1, a kept answer stronger than the action (a new number per role, still a lottery); C2, enemies reading kept zones (core AI, golden-master churn).

### The principle, revised

My draft's principle was *"each role is armed by a choice on the hero's own turn, made with something that hero already does."* The critics broke it from two sides:

- **Systems:** "made with something the hero already does" is exactly the problem. John casts Shield Up for its own value and Mark lands Blitzes because it's his basic attack, so the arm is a by-product: **readable, not decided**.
- **Creative:** every arm was about the hero's own stance (his shield, her facing, his Focus), so nothing depended on where the *other* Bergsons stood. That is overwatch with new art, and the family drops out of the setup. FR-1's fantasy is a role that "protects or supports the family".

Both point to the same fix. **Revised principle:**

> **A role is armed on its hero's own turn and fires for another Bergson. The arm is either an action that competes with attacking, or a position relative to the family, never what the hero would do anyway.**

Every rule below is checked against two questions: what is the hero's real decision on their own turn, where both answers are reasonable? And does the trigger need another family member?

---

## Options compared

| | **A. As built** (free per D-036) **+ Lucy preview** | **C. Kept AP** | **P. My draft** | **P2. Revised (recommended)** | **P+. THJ's full proposal** |
|---|---|---|---|---|---|
| The rule | As built | Roles answer only with kept AP | John: guard with shield up, Wrath breaks it; Linda: faced lane, last arrow; Lucy: as built + preview; Mark: counter spends Focus | **John:** guards while his shield is up, at any range, by switching places; three hits break the shield for a turn. **Linda:** Watch fires on an enemy that ends in her lines **next to another Bergson**. **Lucy:** follows up a Bergson **standing beside her**, shown in previews. **Mark:** as built | P + stamina replacing Wrath, minimum range 2, ember pool |
| Own-turn decision | None | Keep or spend (dominated) | Mostly by-products (systems critic) | John: strike or raise the shield; Linda and Lucy: where to stand relative to the family; Mark: dive or stay by the family (table [below](#the-real-decisions-after-the-critics)) | As P2, plus more resources |
| Press decision | Always yes | Always yes | John only at the breaking hit; Mark's always yes | **John, every press** (he leaves his post); the others always yes (honest) | Same |
| Family-shaped | Incidental | No | Solo stances | **Every trigger needs another Bergson** | Partly |
| New to learn | 0 | 1 | About 8 (UX recount) | About 5, −1 (count [below](#complexity-budget)) | About 12 |
| New on-screen elements | 0 | 0 | About 6 (UX recount) | 3 new, 4 re-meant, 3 removed | 6 or more |
| Implementation | Preview S–M | M, core | S per hero | Readability chunk S–M; John J1+J2 S–M; swap M (core); Linda and Lucy filters S each | Several M chunks, core targeting |
| Risk | THJ's "just a click" stays | Roles vanish | Tests legibility, judged on challenge | The swap's readability; Linda's filter too rare; FTP unbound | Scope; tuned levels break |
| USP | FR as is | FR − | FR + | **FR ++, Synergies +**, Duos + (with an FTP lever) | FR +, Synergies − |

---

## The real decisions, after the critics

The systems critic's test, answered per hero. "Both reasonable" means a player could defend either answer on that board; where there's no decision, it says so.

| Hero | Real decision on their own turn | When both answers are reasonable | Where there isn't one | The press |
|---|---|---|---|---|
| **John** | **Strike, or raise the shield.** When he has to move to reach, his 2 AP buy move + Sword *or* move + Shield Up, not both | Whenever no enemy is beside him at the start of his turn ([S4](#s4-the-river-clearing-turn-1-strike-or-guard), the River) | When an enemy is already beside him: Sword + Shield Up, both. Accepted: holding the line pays. After a break, the next turn is a strike turn (no shield), by rule | **Real every time with the swap:** pressing pulls him off his post and drops the ally on his tile; on the third hit it also costs next turn's shield |
| **Linda** | **Where to stand so her lines cross the tiles beside her siblings**, vs the best tile to shoot from now. The siblings decide too: stand in Linda's line or not | When the best firing tile and the covering tile differ ([S1](#s1-the-ridge-rush-pack-turn-1-linda--mark-as-built), [S3](#s3-the-ridge-with-the-pack-awake-who-does-linda-cover)) | When she is the target herself: her Watch can't fire then. Her own answers (Harmonic Slam, a step away) and John's and Mark's roles cover her. Accepted: it's "Family Watch" | Always yes. Accepted; the graded QTE (FR-2) is the next experiment for presses with no choice |
| **Lucy** | **Stand beside the striker** (her follow-up, Papa's Shelter beside John) at 15 HP, **or stay back** at ember range 3 | Most boards with melee strikers ([S4](#s4-the-river-clearing-turn-1-strike-or-guard)) | When the striker is out of her ember reach anyway | Always yes (as above) |
| **Mark** | **Dive to kill, or stay within 2 of where the siblings will be hit** (his counter is already for others and positional) | When enemies are spread ([S1](#s1-the-ridge-rush-pack-turn-1-linda--mark-as-built): forward or hold) | When enemies come to the family anyway: then the counter is incidental, as today | Always yes. My draft's Focus cost didn't fix this (systems critic) |

So after the changes, three heroes decide by **where the family stands relative to each other**, and John decides by **an action that competes with his attack** and by a press that costs him his post. That is family-shaped and decided. The honest gaps: three of four presses still have one right answer, and Mark stays closest to "incidental".

---

## Per hero (P2)

### John: the shield arms the guard, the guard reaches anyone, Wrath boils over

**Today (verified).** The handler relays any enemy action that targets a family member within 2 (radius held to 1–2), on any phase, unlimited, 1 FTP each; the hit moves to John at ×0.5. Wrath: Shield Up arms it until John's side starts its next turn; **every health loss** while armed, or through the role, adds a stack (max 3), including his own hits, Burn ticks and the Deev's pools (`OnHealthDecreased`); his next damaging ability spends them for +35% each (GDD JO-1; the asset's value; the code default is 0.15). Stacks persist until spent. **Blood Debt already marks the attacker of a guarded hit** (`JohnPassiveAbility_BloodDebt.OnFamilyRoleActivated`, verified), until another enemy hurts family. Shield Up: 1 AP, cooldown 1, ×0.6 damage taken, +1 FTP; its `activationTagQuery` is empty today. John's prompt pauses the game (`requiredTimeScale` 0); the others run in real time (1).

**Rules.**

- **J1. Shield-Up gate.** *"John guards the family while his shield is up."*
- **J2. Wrath boils over (revised).** *"Three hits under the shield fill his Wrath: he throws the shield aside, and can't raise it on his next turn."* Every hit counts, as Wrath does today. On the break, Shield Up ends at once (its ×0.6 too: the dread half), and Shield Up is blocked for John's next turn only. My draft's "can't raise it until he strikes" was free for a front-line John (Sword + Shield Up is his normal turn) and punished a guarding John with no one in reach (systems critic). The one-turn block costs both the same, and it makes declining at Wrath 2 mean "keep next turn's shield".
- **J3. The swap, at any range (in the test).** *"When he guards, John switches places with that family member and takes the hit."* No range: the father reaches the child in danger.

**Why J3 is now in the test, not deferred.** The creative critic: the swap is the heart of THJ's John, it's the only thing that gives *every* press a cost you can see (John leaves the chokepoint, the ally lands on his tile), and a stop rule that judges John without it can end the topic before it's played. The systems critic reached the same place from the other side: "J3 is the next thing to try" if John's press isn't a choice. Without J3 the press is a choice only at the breaking hit. **Accepted**, with the UX critic's readability risk handled as a staging problem (below), and its order in the code moved forward.

| J3 question | Answer |
|---|---|
| Pathing, line of sight | A teleport: no path, ignores walls and gaps (like Encore), on `AEffectSwapper` (core; raises `unitEndMoving` for both, D-322) |
| The attacker's hit | Single target: rewritten to John (today's `RetargetToJohn`). Cell and area attacks land where aimed, on whoever is there now, so the area relay record isn't needed. A charge keeps its destination (`keepCellTargets`) |
| One ally per guard | An area hit on two sisters: John stands in front of one. A father can only stand in front of one child at a time: a feature of the fiction, not a loss (creative critic) |
| Who it can't reach | Toba (another faction), decoys and protectees; John while Crippled or Stunned (**to check** in `AEffectSwapper`) |
| Side effects | The ally lands where John stood, maybe beside other enemies; the next enemy re-plans on the new board. Papa's Shelter forms or breaks. Arrow pickup on a swap: **to check** (LI-7). Linda's Watch: allies don't trigger it |
| Readability | The weakest point (UX critic). Staged: the tether (FR-13, already drawn at any length) shows who; the paused prompt carries a cost line (below); a short swap beat. John's zone and cover marker go (no range), one layer fewer |
| Cost | M, core (`JohnFactionRoleHandler.Activate` rebuilt on the swapper during an enemy action in progress; `GetCellsInRange`; presenters). The riskiest chunk, behind its own toggle |

**Staging the break (creative and UX critics).** My draft's "Shield broken" popup told the player John failed, and today's third stack pops "Max Wrath" in the gain colour, which under J2 is the moment the shield goes: a misread either way. One beat instead: John throws the shield aside with a bark (for `miso-narrative`, e.g. "Get away from them!"), text "Wrath boils over" (placeholder). Shield Up's greyed tooltip reads as a promise: "Wrath first, shield next turn". **The prompt carries the cost** (UX): "Guard Lucy · 1 hit left", and "Guard Lucy · the shield goes" on the breaking guard, so the press is an informed choice.

**Blood Debt (creative point 3): already built.** The guarded Claw already carries Blood Debt (verified), so a Wrath Shield Dash or Sword next turn lands ×1.3 on the Claw that went for the child, until an unguarded hit moves the mark. No change needed; worth one line in the Hearth.

**Levers.** Wrath max and per-stack are a **linked pair** (systems critic): 3 hits / +35% (start); 2 hits / +50% if John becomes a fortress. The block length (1 turn).

**Failure cases.** *John forgotten:* Shield Up never cast: the badge says "Shield down" (below). *Can't control the break:* hits aimed at John drain his guards: true, and in fiction (a father under attack can't cover the others); if it reads as unfair, count only guarded hits (a second counter, against D-295, so only as a lever). *Swap reads as a bug:* if a cold player can't say who swapped with whom after the enemy turn, fall back to range 2 without the swap (creative critic's own stop condition).

**Code.** J1 + J2: **S–M** (systems critic, accepted): the break removes Shield Up's damage-taken modifier in the middle of an enemy action, inside a health callback, which is the code path `JohnFactionRoleHandler` warns about (a shared `Stat_DR` context once caused a StackOverflow with Shield + role together); an area relay can cross the break, so the second hit lands without ×0.6; the block needs a new tag, set and cleared in code. EditMode tests for an area relay across the break. Files: `JohnFactionRoleHandler` (**core**), `JohnPassiveAbility_Wrath` (not core), `John_Ability_Shield.asset` (data). J3: M, core, its own tech plan.

### Linda: Family Watch watches the family

**Today (verified).** Watch fires when an enemy ends a move in her row or column within 4, all four half-lanes, spending an arrow and 1 FTP. FR-10 hides her zone because it equals her bow's reach.

**Rule (revised).** *"Linda's Watch fires on an enemy that ends its move in her lines next to another Bergson."* Next to: the four neighbouring tiles (CR-15). Another Bergson: John, Lucy or Mark (not Toba, not decoys, as John's tag query). Her bow is unchanged.

This is the creative critic's proposal, and it replaces my draft's facing lane. It is THJ's minimum-range intent (Watch shoots at what goes for someone else) moved from the bow to the trigger, which is a filter in `LindaFactionRoleHandler` with **no core targeting work and no preview churn**. What it does:

- **The decision becomes the family's positions.** Linda decides where her lines cross the tiles beside her siblings; her siblings decide whether to stand in her lines.
- **It answers the corridor problem** (systems point 6): on a 1-wide approach, enemies going for Linda end next to Linda only, so they don't set off Watch. Corridors stop being free kill zones.
- **It answers THJ's arrow complaint without a new rule:** Watch fires less, so she keeps arrows for her own turn. L2 (the last arrow) becomes a lever, not a rule (UX: it was an off-by-one rule; systems: its trade was thin).
- **Memory 1 gets no roles for free:** Linda is alone, so Watch can never fire. No per-level switch.
- **No new on-screen element:** her zone becomes the watched tiles (tiles in her lines beside a sibling), drawn with her existing bow icons. It no longer equals her bow reach, so FR-10 stops hiding it.
- **Cost:** she loses her self-defence Watch, so she is weaker up close. That is what THJ's minimum range wanted, and Harmonic Slam, John's guard and Mark's counter are her answers.

**THJ's facing lane** stays as the alternative (Q3), with the UX critic's fixes if chosen: the rule in one line, *"Linda faces the way she last shot, or the way you turn her"* (moves don't change it; a diagonal shot takes the longer axis, a tie keeps the old facing); the picker as a control on her HUD, not arrows on the board; her lane drawn on the family's turn even when she isn't selected; End Turn pulses her badge if her lane holds no enemy that could end in it. **Both together** (lane + family filter) is too narrow to fire.

**Minimum range 2 on the bow:** not recommended. No minimum-range concept exists in the code (core targeting work plus every preview, CR-37), it breaks Memory 1's throat and the Ridge's opening, and the family filter gets its intent without either.

**Interactions.** Tempest Bloom: the Cyclone drifts toward units, so it is often near the family, and the loved shot stays possible and stays a surprise. Catch & Return: a sibling in her line is also where Mark catches (if the node is bought). Pushes, Command moves and Toba's swap still count as moves (D-322), filtered the same way. With the quiver off (LI-14), the filter still limits her.

**Failure case.** Watch fires on under about 1 in 4 enemy turns with enemies awake and in range (the creative critic's own bar). Lever: "within 2 of another Bergson"; then the facing lane alone.

**Code: S.** `LindaFactionRoleHandler.PrepareTargets` and `GetCellsInRange` (the watched tiles; **core** handler); `RoleZonePresenter` draws them (not core).

### Lucy: beside the family, and shown before it happens

**Today (verified).** Her follow-up fires on any phase when a family member's action really lowered an enemy's HP within 3 of her: 2 embers × 3, preferring the aimed enemy (`LucyRoleTargetRanking`), skipping an enemy whose most recent attacker is Lucy. 1 FTP each, no cap.

**The systems critic's point 5 is right:** under my draft Lucy lost her only limit (FTP) while the other three lost uses; she'd fire on every qualifying family hit, both turns: the free reward THJ complained about, on the one role left free.

**U-R. Rule (revised).** *"Lucy follows up a Bergson standing beside her."* The creative critic's replacement for Kindle: armed by keeping her close to family, which a fragile 15-HP child pays for in danger, and which Papa's Shelter already rewards beside John. A filter in her handler; no mark on enemies; her reach to the enemy stays 3. "Beside her": where the striker stood **when its action started** (Mark's Blitz and John's Dash move him; whether the handler can read the start tile at action complete is **to check**). THJ said she can stay free: she stays free, with no counter or pool, just armed by position. Kindle (U3) is rejected: it made her role about herself and made her act first (creative critic).

**U1. Preview (all branches, any time), redesigned with the UX critic.** My draft put her zone glyph on the enemy's tile (reads as "Lucy's zone") and her damage on the target's panel (not open when her pick isn't the hovered target, which is the "random" case).

| When | Shown |
|---|---|
| Another Bergson's damaging ability is previewed on a single target, or on the firing pick of a multi-target one, and Lucy would follow up (the striker beside her, the hit lowers HP and doesn't kill, the enemy within 3 of her, her ranking picks it) | An arc from Lucy to her pick (the tether's look, in her colour); a ghost "+6" in her colour above the pick's **mini HP bar** (CR-49, always visible); on an open panel, her part as a hatched "if pressed" segment |
| Her embers would finish it | No tinted skull: the skull keeps meaning "this hit kills" (CR-46) |
| An enemy in her reach is skipped by the "hit last" rule | A small crossed ember on it, the first time it matters (or the rule goes; why it exists is **to check**) |

Enemy-turn follow-ups (after a Watch or a counter) stay unpreviewed: a surprise. **Code: S–M**, its own tech plan: a preview helper beside `LucyRoleTargetRanking` (not core), a hook in the attack preview path (`PlayerController` / `UnitThreatAnalysis`, **core**, additive), the arc and ghost number (UI).

**Ember pool (U2): rejected.** It reads as the quiver re-themed (THJ's words), adds a fourth counter, caps without choosing, its Focus ability arms the role by giving up an action (the kept-AP problem), and "Focus" is Mark's resource. All three critics agree.

### Mark: as built, honestly

**Today (verified).** Enemy phase only (`activationPhase` 4), after an enemy's action hits a family member other than Mark, if the attacker is within 2; a free Fist Blitz (8 + Focus), which also earns him +1 Focus.

**My draft's M2 (counter spends 1 Focus) is withdrawn.** The systems critic: one Focus is 1–3 HP of barrier against 8+ damage, and hits on Mark drain Focus anyway, so the press is always yes; and his Focus comes from Blitzes he lands anyway, so the arm is a by-product. The UX critic: a cost decision can't live in a 1 s real-time window. The house rule couldn't even simulate it (the counter earns Focus as built).

**Recommended: M1, as built.** Mark's role already passes the revised principle's family test (it fires only for hits on others) and is positional (the attacker within 2 of him). His decision is **dive or stay by the family** (S1). His press has one answer, said plainly. Levers if he still reads as free:

| Lever | Rule | Note |
|---|---|---|
| Designed limit | Once per enemy turn (D-042, never built) | Bounds him; no choice added |
| Focus bet | *"His counter spends all his Focus and adds it to the hit"* | A real bet (a big counter now vs barrier and damage later); needs his prompt paused: `requiredTimeScale` 0 on his role (data, verified field) and a cost line |
| Start Focus 1 | "He arrives centred" (creative) | Only matters with a Focus rule |

### Every role: no FTP, and what FTP is for then

Roles cost no FTP (D-036): `requiredFTP` 0 on the four role components (data). **The systems critic's point 4:** with no role sink, pools start full (River 8, Ridge 5), income keeps coming (Shield Up, Slam, Blink, Pass-by, level fills), Duo cooldowns bind before FTP, and Pass-by's only payoff (FTP) becomes a dead choice. Mark's Continuous Attack still costs FTP (MA-2; D-216's "free" isn't built), so "FTP is the Duo meter only" isn't true yet. That runs against THJ's "Duos as finishers". So:

- In the session, set `requiredFTP` 0 in data (not +99 FTP), and log FTP at fight end and Duos per fight.
- Lever DU-5 (Duo cost 3) comes into this plan, used if FTP ends most fights above 4.
- What Pass-by is for when FTP is never short is a question for THJ (Q6).

---

## Readability the arms need (UX critic)

The UX critic's strongest point: an arm only fixes "you never know what you did" if the player can see, **before End Turn**, which roles are armed, and **on the enemy turn**, why one didn't fire. Today: the role badge is a 14 px dot (Ready / NoFtp / EmptyQuiver, `RoleBadgeRules`), green for John with his shield down once FTP is gone; John's Wrath is "2/3" in a panel box, Mark's Focus is a number, there are no Focus pips; the role-zone glyphs are already the worst-read element on the board (B4 finding 1, `status.md`, 2026-10-21). Accepted, with three pieces on existing layers and one prerequisite:

| # | Piece | What | New or re-meant |
|---|---|---|---|
| 0 | **Contrast fix first** | B4 item 1: role-zone and cover glyphs readable on dark floors | Fixes an existing element. **A blocker for P2, not polish** |
| 1 | **Armed badge with a reason** | `GetRoleBadgeState` (already marks "switch here when roles stop costing FTP") reads the arm: Ready, "Shield down", "Wrath first, shield next turn", "No family beside" (Lucy), "Empty quiver". The tooltip is each hero's one line | Re-meant |
| 2 | **Hovering End Turn shows the armed roles** | The Shift layer (FR-9) limited to armed roles: John's guard targets if his shield is up, Linda's watched tiles, Mark's radius. The same drawing stays up through the enemy turn | Re-meant (an existing layer, a new moment) |
| 3 | **"Would have fired" ghost** | When a trigger happens but its arm is off, the role glyph shows greyed and crossed for about 0.6 s over the unit that would have acted, with two words ("Shield down", "No family beside", "Not next to family"). Each handler evaluates its trigger before its gate, so it's a few lines per handler | **New, necessary**: it teaches the arms without a tutorial, and silence teaches nothing |

Deferred (each listed in [what to cut](#complexity-budget)): the badge row beside End Turn (the hover covers it), threat arcs on John's paused prompt, world-space shield segments on John (the prompt's cost line carries the decision), Focus pips under Mark (Mark has no Focus rule now).

---

## Lens notes (P2)

### Creative

**Target experience.** The family covers each other, and you arrange that: you keep Lucy beside her father so her fire follows his sword, you stand Mark where Linda's arrows cross, and when a Claw goes for the youngest, John comes across the room. Every role on the enemy's turn is someone answering *for* someone.

**The moment designed for:** the enemy turn where John holds the corridor on two Wrath and a Claw lunges at Lucy, three tiles behind. Press, and he leaves the corridor, takes the hit, and throws his shield aside ("Get away from them!"); next turn he strikes the Claw that went for her (Blood Debt). Or let Lucy take it and keep the door.

**Original?** Shield gates and overwatch are known; a role that only fires when the family stands in a certain relation to each other is not. That's the USP made into the setup.

**Creative vs systems, where they disagree:** creative wants the graded QTE on presses with no choice now; systems wants one variable per test. I keep the graded QTE as the next experiment (FR-2's plan), not in this test.

### Systems

**The rules (P2).** (1) Roles cost no FTP. (2) John guards only while his shield is up. (3) Three hits under the shield fill Wrath; the shield goes and is blocked for his next turn. (4) His guard switches places with the ally, at any range. (5) Watch fires only on an enemy that ends in Linda's lines next to another Bergson. (6) Lucy follows up only a Bergson standing beside her. (7) Mark as built.

**Levers and starting values.**

| Lever | Start | Range | Where |
|---|---|---|---|
| Hits before the break / Wrath per stack (linked) | 3 / +35% | 2 / +50% | Wrath passive (data) |
| Shield block after the break | 1 turn | 0–1 | Rule |
| Guard range | Any (swap) | 2 without the swap (fallback) | Handler |
| Linda's "next to" | 1 tile | 2 | Handler |
| Linda's last arrow (L2) | Off | On, if she still runs dry | Quiver rule (data on LI-5) |
| Lucy's "beside" | 1 tile | — | Handler |
| Lucy's cap | None | 3 a round (FR-4) | If her share stays high |
| Mark | As built | Once per enemy turn; Focus bet with a paused prompt | Handler, data |
| Duo cost | 2 FTP | 3 (DU-5) | If FTP ends fights above 4 |

**Interactions.** Shield Up stays the family's defensive hub (guard, Wrath, Shield Flare, and Command Shield Dash after a Command). With the swap, Papa's Shelter can form or break on the enemy turn. Linda's filter and Lucy's beside rule both reward a tight family, which Pass-by also rewards (if Pass-by keeps a payoff, Q6). Masher counters (EN-2) on the player's turn are guarded only if Shield Up is on that turn. A declined guard still silences that target for the turn (as built).

**Failure cases.** *Linda too rare* (under 1 in 4): widen "next to", then the facing alternative. *Lucy too rare*: if follow-ups drop under about one a fight, widen to "within 2", or drop the filter and cap at 3. *Lucy still too strong*: her share of family damage above about a fifth: the cap. *Tight-family dominant*: everyone hugs; enemy area attacks (the Masher slam) are the natural answer, so watch whether hugging is ever wrong. *FTP always full*: DU-5. *John fortress*: the linked lever.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Family's turn | Armed badges with reasons; Linda's watched tiles; the Lucy arc and "+6" on other heroes' attack previews | As now | "Lucy's follow-up is certain": the hatched "if pressed" segment, no skull |
| Hover End Turn | Armed roles only, on the board | End Turn | "Mark's radius is a danger zone": it's in his role colour and quadrant |
| Enemy turn, armed role fires | The prompt; John's with a cost line and the tether to the ally at any range | The key | After a swap, "where did everyone go?": the tether and the swap beat |
| Enemy turn, unarmed role | The ghost with two words | — | None: that's what the ghost is for |
| John's break | "Wrath boils over" beat and bark; Shield Up greyed "Wrath first, shield next turn" | — | Reading Wrath full as good news only: the cost line warned on the breaking guard |

---

## USP check

- **Family Roles:** strengthened, and made family-shaped: every trigger needs another Bergson, every arm is a choice on the hero's turn.
- **Synergies:** strengthened. A tight family arms Linda and Lucy and meets Papa's Shelter, Shield Flare and Catch & Return on the way; the preview shows Lucy's combo before you commit.
- **Duos:** FTP freed from roles; it needs a lever (DU-5) to keep Duos as finishers.
- **Managing the Home as a Family:** neutral on purpose. `thj/home-test`'s Fireside "first Family Role free" means nothing once roles are free; remap on merge (e.g. John starts the sortie with his shield up).

---

## Critics

All three read the draft P independently. Their strongest points and what I did:

| Critic | Strongest point | What I did |
|---|---|---|
| **Systems** | P makes roles readable, not decided: John's Shield Up and Mark's Focus come from what they do anyway; Mark's press is always yes; John's S2 press moves damage without reducing it (and my line saved the guard for the wrong sister) | **Accepted.** Rewrote the principle (an arm must compete with attacking or be a position relative to family). Withdrew M2. Added S4, where John's Shield Up competes with move + Sword. Regraded S1 and S2 (Mark can move and Blitz 2,4; S2's press is small in HP). Added the [real decisions table](#the-real-decisions-after-the-critics), with the gaps stated |
| Systems, point 1 | J2's "strike first" is free at the front and punishing at the back; Wrath counts every hit; Wrath max and per-stack are linked; J2 costs S–M | **Accepted:** the break now blocks the next turn's shield; levers linked; cost raised; area-relay-across-the-break test named. Counting only guarded hits kept as a lever (a second counter) |
| Systems, point 4 | No role sink: FTP always full, Pass-by dead; +99 FTP hides it | **Accepted:** `requiredFTP` 0 in data for the session, FTP logged, DU-5 in the levers, Pass-by to THJ (Q6) |
| Systems, point 5 | Lucy gets stronger while the others get weaker | **Accepted:** her beside rule bounds her; cap 3 as a lever; her damage share read in the log |
| Systems, point 6 | Linda's default facing is already right on one-front boards; corridors become free kill zones; Crescendo has no direction | **Accepted** by changing Linda's rule: the family filter doesn't fire on enemies going for her, so corridors aren't kill zones, and there's no default to get wrong. The facing fixes are kept for the alternative |
| Systems, scenario errors | S1: Mark can Blitz 2,4; S2: Wrath 1 already kills on turn 2; S3: a Claw striking diagonally; S1's Watch depends on enemy order | **Fixed:** S1 redone with Mark's Blitz; S2's turn 2 says the extra Wrath pays only on Shield Dash and through Blood Debt; S3's paths written out tile by tile (every strike from a 4-way neighbour); every Watch states its order and tie-break assumption |
| **Creative** | Every gate was the hero's own stance: overwatch with new art; P cut THJ's two family ideas (the swap, Watch for others) | **Accepted as the new principle.** Swap in the test; Linda's family filter replaces the facing lane (no core work, Memory 1 silent for free); Lucy's beside rule replaces Kindle |
| Creative, point 1 | Don't let the stop rule judge John without the swap | **Accepted:** the stop rule is now per hero, and John isn't judged until J3 has been played. Dropped "any range without the swap" from the questions |
| Creative, point 3 | Stage J2 as Wrath boiling over; Blood Debt on the Claw that went for Lucy | **Accepted** the staging; Blood Debt **already does this** (verified in code), so no change |
| Creative, point 4 | Mark starts at Focus 1 | **Moot** with M2 withdrawn; kept as a lever with the Focus bet |
| Creative, point 6 | Graded QTE for presses with no choice | **Deferred** to the next experiment: one variable per test. Added the session question "did you tell anyone about a role?" |
| **UX** | You can't see which roles are armed before End Turn, or why one didn't fire; the badge stays green; the glyphs are already the worst-read element | **Accepted:** contrast fix as a prerequisite; badge re-meant with reasons; End Turn hover shows armed roles; the "would have fired" ghost |
| UX, point 1 | "Max Wrath" in the gain colour is a misread; the guard choice is made blind | **Accepted:** one "Wrath boils over" beat; a cost line on John's prompt. Threat arcs on the prompt and shield segments deferred (budget) |
| UX, point 2 | Linda's picker on the board misclicks; the default can't be recited | **Moot** for the recommendation (no picker); fixes kept for the facing alternative |
| UX, point 4 | Mark's 1 s prompt can't carry a cost decision | **Accepted:** M2 withdrawn; the Focus bet lever needs a paused prompt (data) |
| UX, point 5 | Lucy's preview as drafted fails in the "random" case | **Accepted** the redesign: an arc, a ghost "+6" over the mini HP bar, a hatched segment, no tinted skull, a crossed ember for the skip rule |
| UX, point 6 | P adds about 8 rules and 6 elements, not 4.5 and 1 | **Accepted** the recount; P2 recounted [below](#complexity-budget) |
| UX, the test | THJ can't test readability: he knows the rules. A cold player is needed | **Accepted:** the session now tests decisions only; readability goes to a cold player after the readability chunk |

**Rejected or not taken:** the creative critic's "both lane and filter" option (too narrow; it's one or the other, Q3); the UX critic's badge row beside End Turn (the hover covers it, within budget); the systems critic's "Focus cost 2" for Mark (still always yes).

---

## Complexity budget

THJ: "too many mechanics, too little challenge"; D-295: one sentence per feature, at most one new element unless necessary, more than one new thing to track goes to THJ as a question.

**Recount, read as a player (the UX critic's method).**

| | P (draft), UX recount | **P2** |
|---|---|---|
| Rules added | About 8: John 3 (gate, three hits, his own hits count), Linda 3 (one lane, the default, last arrow), Mark 2 (spends Focus, earns none) | **5:** John 3 (*guards while his shield is up*; *three hits throw the shield aside for a turn*; *he switches places*), Linda 1 (*watches for enemies next to family*), Lucy 1 (*follows a Bergson beside her*). Mark 0 |
| Rules removed | 1–2 (FTP, FR-10) | **2:** roles spend FTP; John's "within 2" |
| New on-screen | About 6 | **3, each necessary:** the "would have fired" ghost (teaches the arms), Lucy's arc and ghost number (THJ asked for her feedback), the swap beat (the swap can't read without it) |
| Re-meant (existing) | — | **4:** the badge's states, the zones on End Turn hover and through the enemy turn, John's prompt line, the Wrath beat (replaces "Max Wrath") |
| Removed from screen | 0 | **3:** John's zone and cover marker (no range), the NoFtp badge state; plus FR-10's hiding for Linda |

Net: about +3 rules, each one sentence on its hero's badge; John carries three of them, which is THJ's own proposal and goes to him as Q2.

**Cut or deferred to stay there.** From my draft: Linda's facing picker and default (replaced), L2 (lever), M2 and "counters earn no Focus" (withdrawn), J2's "until he strikes" (replaced). From THJ's set: stamina as its own system (Wrath carries it), minimum range on the bow, the ember pool. From the critics: the badge row by End Turn, threat arcs on the prompt, shield segments on John, Focus pips, the graded QTE (next experiment). From the design: Pilot 1's caps (FR-4) and the "Watch 2/2" label (FR-6), never built; kept AP.

---

## Paper scenarios

Frames read from the prefabs on 2026-11-09 with `level_to_grid.py`: `GB_s2-ridge` (plan tiles = prefab + 1 in x, with a border), `GB_m3-john` (+1 in x and y, with a border), `GB_s1-river` (no offset; `#` and `_` both mean no tile). x from the left, y from the bottom. Claws attack **4-way neighbours only** (`DarkClaw_Ability_Attack.asset`, Adjacent; CR-15). **AI paths and order are assumed:** each Claw takes the shortest path to a free 4-way neighbour of its nearest target; ties are stated. Values: Tutorial Claw HP 10, hits ≈3 (round 1's figure, assumed), Linda's bow 6 (×0.6 per further enemy), Crescendo 8 on a cell within 5 and its neighbours, Fist Blitz 8 within 2 (he steps into the cell of a kill, otherwise ends beside the target), Mark's move 3 (`Mark_Ability_Walk.asset`, 3 × `Stat_SPD`, SPD 1 assumed; John and Lucy assumed the same), Claws move 4, Wrath +35% a stack. Catch & Return isn't bought yet at the Ridge (the Family tree opens after the Yard), so arrows pass Mark.

### S1. The Ridge, rush pack, turn 1 (Linda + Mark), as built

Gauntlet (7,1, 8,1) asleep. 2,4 starts Alerted (3 from Linda) and wakes 1,5 and 3,5 (EN-15). The draft missed that Mark can reach 2,4: 3,1 → 3,3 (2 steps), then Blitz (3,3 to 2,4 is 2).

```grid id=rr2-s1-perhero title="S1 The Ridge, P2: forward line, Mark finishes 2,4 (GB_s2-ridge)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,3 2,5 linda watched: her line, beside Mark
arrow 2,1 2,4 linda dx=-8 one shot (10 to 4)
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz: dead, he steps in
arrow 3,5 2,5 enemy Watch if it ends here
arrow 1,5 1,4 enemy
step 2,4 1
step 2,5 2
note 2,1 2 arrows left
```

| Line | Player's turn | Enemy turn (assumed) | Result | Grade |
|---|---|---|---|---|
| **Forward (drawn)** | Linda shoots 2,4 once (10 → 4; quiver 2). Mark moves to 3,3 and Blitzes it (8 ≥ 4, dead) and steps into 2,4 | 1,5 and 3,5 go for Mark. His free neighbours: 1,4, 2,5, 3,4, 2,3. 1,5 picks 1,4 or 2,5; 3,5 picks 3,4 or 2,5 (1 step each; the tie-break is unknown). A Claw ending on 2,5 is in Linda's column next to Mark: **Watch** (6), before it strikes. Mark doesn't counter hits on himself | Linda 0 hits, 2 arrows. Mark 2 hits. 0–1 Watch, depending on the tie | ★ |
| **Hold** | Linda shoots 2,4 twice (dead; quiver 1). Mark stays on 3,1, beside her | 1,5 runs to 1,1 and strikes Linda: **counter** (1,1 is 2 from Mark; 8 → 2). 3,5 reaches 3,2 (3 steps) and strikes Mark, or 2,2 (4 steps) and strikes Linda (**counter** again, 2,2 is 2 from Mark). No Watch: 1,1 and 2,2 are next to Linda only | Linda 1–2 hits, 1 arrow. Mark 0–1 hits. 1–2 counters | ★ |
| Today | Two shots on 2,4 | 3 prompts (Watch, two counters), 0 choices (round 1) | | — |
| **Count (P2)** | **1 real decision:** forward or hold. It's Mark's (where he stands) and Linda's (one arrow or two), and it decides which roles can fire | Forward: 0–1 prompts. Hold: 1–2. **Each traces to where Mark stood** | Both lines reasonable: Linda's HP and arrows vs Mark's | |

*Coordinator, grid check 2026-11-09:* in the forward line, the Watch on 2,5 has to fly past Mark on 2,4 (Linda 2,1 → 2,5 along column 2). **To check** whether her arrow passes an ally; if it doesn't, the forward line has no Watch at all.

My draft counted 2 decisions here, and its ★ was dominated by its own "spend" line (systems critic). Corrected: one decision, and it's a family-position decision.

### S2. Memory 3, John's telling (John 1 AP, sisters 0 AP), as built

Five Claws, all alert. Order: (4,4) first (D-393, `turnOrder` 0); then assumed (6,5), (7,4), (2,5), (1,4).

```grid id=rr2-s2-perhero title="S2 Memory 3, P2: Shield Up, the first guard swaps John and Lucy (GB_m3-john)"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
cells 3,1 5,1 linda watched: beside John
arrow 4,4 4,3 4,2 enemy first: John, Wrath 1
arrow 6,5 6,4 6,3 6,2 enemy on Lucy: guard?
arrow 4,1 6,1 john dy=-8 swap
arrow 6,1 4,1 lucy dy=8 swap
arrow 7,4 7,3 7,2 7,1 enemy re-plans: John, Wrath 3
arrow 2,5 2,4 2,3 2,2 enemy unguarded
arrow 1,4 1,3 1,2 1,1 enemy unguarded
step 6,2 1
step 7,1 2
note 4,1 Shield Up
```

| | P2 (J1, J2, J3; Linda's filter) | |
|---|---|---|
| Player's turn | John: Shield Up (hinted; his only AP). The guard is armed because of it | 1 decision, hinted |
| Enemy turn | (4,4) → 4,2 strikes John (×0.6): Wrath 1. (6,5) → 6,2 on Lucy: **prompt** "Guard Lucy · 1 hit left". Pressed: John and Lucy swap (4,1 ↔ 6,1), John takes ×0.5 × 0.6 (≈0.9): Wrath 2; Blood Debt on that Claw. (7,4) re-plans on the new board: 7,1 is beside John (3 steps), so it strikes him: Wrath 3, **Wrath boils over**, no prompt. (2,5) → 2,2 and (1,4) → 1,1 strike Linda, unguarded (Blood Debt moves to the last of them). No Watch: Linda's watched tiles (3,1, 5,1, next to John or Lucy) stay empty | |
| The press, honestly | At Tutorial damage the HP difference is small, as the systems critic said. What the press changes is visible: pressed, Lucy ends beside (4,4)'s Claw and John on the right; declined, Lucy takes ≈3, John keeps the middle and his shield for one more guard (then (7,4) goes for Lucy: another prompt). It's a tutorial: a small choice you can see | 1 press with a visible consequence |
| Turn 2 | Wrath 1 already lets the Sword kill a Claw (8 × 1.35 = 10.8, systems critic), so the extra Wrath pays only on Shield Dash: 4 × 2.05 = 8.2 to each Claw beside the path, 10.7 on the Blood Debt Claw (kills; at Wrath 1 or 2 it doesn't: 7.0, 8.8). Which Claws a Dash reaches depends on where the swap left John (assumed). His shield is blocked this turn | |
| **Count** | **1–3 prompts** (today 6), all John's; **1 press with a consequence**. Only John's role fires, with no per-level switch: Linda's filter finds no Claw next to a sibling in her lines, and no family damage on the enemy turn means no follow-up | |

### S3. The Ridge with the pack awake: who does Linda cover?

The same as-built tiles with every enemy awake (the level's "all enemies start alert" flag, MI-27; data). Threats come from two directions: the rush down the north pocket, and the gauntlet along row 1, a 1-wide corridor from x 5. Mark's line is fixed so the choice is Linda's: 3,1 → 3,3, Blitz 2,4 (10 → 2), ending beside it on **3,4 (assumed; if he ends on 2,3, he stands in Linda's column and her watched tiles change)**. Order assumed: the gauntlet first, then the rush.

```grid id=rr2-s3-family title="S3 The Ridge, all awake, P2: Linda covers Mark (GB_s2-ridge tiles)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,4 linda watched: beside Mark
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz (10 to 2)
arrow 2,1 2,4 linda dx=-8 kills it
arrow 1,5 2,5 2,4 enemy Watch
arrow 7,1 6,1 5,1 4,1 3,1 enemy dy=6 strikes Linda
arrow 8,1 7,1 6,1 5,1 4,1 enemy dy=14
step 2,4 1
note 3,4 Mark ends here
```

| Line (P2, the family filter) | Linda's turn | Enemy turn | Result | Grade |
|---|---|---|---|---|
| **Cover Mark (drawn)** | Shoots 2,4 (2 HP, 3 away: dead; quiver 2). Now 2,4 is a free tile in her column next to Mark | 7,1 runs to 3,1 (4 steps) and strikes Linda: next to Linda only, no Watch. 8,1 ends on 4,1, can't reach anyone. 1,5 takes 2,5 → 2,4 (2 steps; the shorter way to Mark) and ends in her column next to Mark: **Watch** (10 → 4), then it strikes Mark. 3,5 strikes Mark from beside him (no move) | Linda 1 hit, Mark 2. 2,4 dead; gauntlet untouched; quiver 1 | ★ |
| **Thin the gauntlet** | Crescendo on 7,1 (5 away): 7,1 and 8,1 both 10 → 2 (quiver 2). 2,4 (2 HP) stays beside Mark | 7,1 (2 HP) reaches 3,1 and strikes Linda (no Watch). 8,1 ends on 4,1. 1,5 finds 2,4 taken and takes 1,4 → 1,3 → 2,3 → 3,3 (4 steps), next to Mark but not in her lines: no Watch. 2,4 and 3,5 strike Mark from beside him | Linda 1 hit, Mark 3. Both gauntlet Claws at 2: next turn one bow shot down row 1 pierces both | ● |
| **Count (P2)** | **2 decisions** (north or east; which also decides whom her Watch can cover) | 1 or 0 prompts, each traced to the tile she cleared next to Mark | Both reasonable: Mark's HP now vs a gauntlet set up for one pierce | |

*Coordinator, grid check 2026-11-09:* the drawing shows Mark's move to 3,3 and the Blitz, and notes him ending on 3,4. The enemy lines (3,5 striking without moving, 2,4 and 3,3 "next to Mark") all assume Fist Blitz leaves him on 3,4 beside the target when it doesn't kill. **To check** where a non-lethal Blitz lands him.

**THJ's facing lane on the same board** (the alternative, Q3; drawn in `rr2-s3-lane`). The facing rule lets Linda cover herself, so the corridor works for her: Crescendo east and face east, and the Watch kills 7,1 (2 HP) on 3,1 before it strikes; 8,1 ends on 4,1 with no Watch (with L2) or a second Watch (without L2). North: as "Cover Mark", but Watch fires on any Claw ending in her column. Count: 3 decisions (target, arrows, lane). The difference between the rules is the choice: **facing asks "which way is the danger"; the family filter asks "who am I covering"**. On this board that's Linda or Mark.

```grid id=rr2-s3-lane title="S3 alternative, facing lane: Linda faces east (GB_s2-ridge tiles)"
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
arrow 8,1 7,1 6,1 5,1 4,1 enemy dy=14
arrow 1,5 1,4 1,3 2,3 3,3 enemy
step 3,1 1
note 3,4 Mark ends here
```

### S4. The River clearing, turn 1: strike or guard? (John + Lucy), as built

Added for the systems critic: the board where John's Shield Up competes with his attack. Three Claws asleep within 2 of each other (5,3, 6,4, 6,2); Archers far on their islands. John 1,3, Lucy 0,3.

```grid id=rr2-s4-river title="S4 The River clearing, P2: John strikes or raises the shield (GB_s1-river)"
# # . . . . # # . . _ . _ . . # #
# . . . . . . # . a _ . _ a . # #
# . . . . . c # _ _ . . . _ _ . .
U J . . . c . . . . . @ . . . . .
# . . . . . c # _ _ . . . _ _ . .
# . . . . . . # . a _ . _ . . # #
# # . . . . # # . . _ . _ . . # #
--
range 5,3 2 enemy wake together
arrow 1,3 4,3 john dy=8 step
arrow 0,3 3,3 lucy dy=-8 step: beside John
arrow 4,3 5,3 john Sword, or Shield Up
step 4,3 1
step 3,3 2
note 3,3 Sheltered; follows John
```

| Line | Player's turn | Enemy turn (assumed) | Grade |
|---|---|---|---|
| **Strike** | John steps to 4,3 (wakes 5,3 at 1, which spreads to 6,4 and 6,2). Lucy steps to 3,3, beside him (Sheltered). John's Sword on 5,3 (8 → 2): Lucy's **follow-up** (striker beside her, 5,3 is 2 from her): 6, dead. Lucy's second AP: free (6,4 and 6,2 are 4 from her, out of ember reach) | 6,4 and 6,2 come for John or Lucy; no shield, no guard. Lucy (15) takes up to 2 hits | ★ |
| **Guard** | John steps to 4,3 and raises Shield Up. Lucy steps beside him and embers 5,3 (main 4, plus a sidewinder or two: 4–10; how the sidewinders pick is **to check**) | Three Claws (or two) strike. Each hit on Lucy: a **prompt** (swap; they're adjacent, so the board barely moves). The third hit under the shield, his own or a guard, makes Wrath boil over, and the cost line says so: decline it and the shield stays for next turn | ★ |
| Hang back | Lucy stays at 2,3 (out of reach of John's side), embers from range | No follow-up (not beside the striker), no Shelter | ● |
| **Count** | **2 real decisions:** John's (damage now or a guard) and Lucy's (beside him or back). Prompts: strike 1 (follow-up), guard 1–3 (the breaking one is a real press) | | |

### Totals

| | Today | P (draft, as claimed) | **P2 (corrected)** |
|---|---|---|---|
| S1 | 0 decisions, 3 prompts | 2 / 1 | **1 / 0–2** |
| S2 | 0 / 6 | 1 + a press / 2 | **1 hinted + 1 press with a consequence / 1–3** |
| S3 | — / 3–4 | 3 / 1 | **2 / 0–1** (facing alternative: 3 / 1–2) |
| S4 | 0 / 2 (round 1) | — | **2 / 1–3** |

Fewer prompts than today, each traced to where the family stood or what John did, and one or two real decisions per board.

---

## Recommendation

**P2.** Roles cost no FTP. **John** guards while his shield is up, at any range, by switching places; three hits make his Wrath boil over, and the shield is gone for his next turn. **Linda's** Watch fires on an enemy that ends in her lines next to another Bergson. **Lucy** follows up a Bergson standing beside her, and shows it in the other heroes' previews (arc and "+6"). **Mark** as built. Readability first: the glyph contrast fix, the armed badge with reasons, armed roles shown on End Turn hover and through the enemy turn, the "would have fired" ghost. Kept AP withdrawn; THJ's facing lane is the alternative for Linda (Q3); stamina, minimum range, the ember pool, Kindle and Mark's Focus cost are not recommended.

### The stop rule, per hero

D-457's stop rule judged all roles at once after one session. That can kill John before his swap exists (creative critic), and it judges readability with a player who knows the rules (UX critic). Revised:

- **Per hero:** a hero whose rule fails goes back to as built (free); the others carry on.
- **John isn't judged until J3 has been played.**
- **Readability is judged by a cold player**, not by THJ.
- **The full stop** (lock every role as built, ship Lucy's preview, move the energy to Synergies) happens if John with the swap fails *and* the family filters give no decisions.

### Step 1: paper (this plan, ~15 minutes)

S1 to S4. Pass if each P2 line gives at least one real decision and every prompt traces back to one.

### Step 2: house-rule session (THJ, no code, one evening)

**What it can show:** whether the arms and filters change what THJ does on his turn, and whether the presses are choices; the FTP economy with free roles. **What it can't show:** readability (THJ knows the rules), the swap, the ghost, Lucy's preview.

**Data for the session (Tier 3, reversible):** `requiredFTP` 0 on the four role components (not +99 FTP, systems critic), and `requiredTimeScale` 0 on Linda's and Lucy's roles so their prompts pause and the filters can be judged (it changes the feel; note it).

| Hero | House rule |
|---|---|
| John | Press his guard only while Shield Up is on. Count every hit he takes under the shield; on the third, decline every further guard that turn and don't cast Shield Up on his next turn |
| Linda | Press Watch only for an enemy that ended next to John, Lucy or Mark |
| Lucy | Press her follow-up only if the striker stood beside her when it struck |
| Mark | As built |

Levels: Memory 3, the River, the Ridge (as built, then with "all enemies start alert"), one M4 or M6 fight, on `main`.

**Read after the session, two questions per hero** (systems critic): *Did you know why it fired?* (legibility, which THJ can only half-answer), and *Did you ever not arm it, not press it, or stand somewhere else because of it, and was that right?* (decision). And one for the creative critic: *Did you tell anyone about a role afterward? Which one?* Log: FTP at fight end, Duos per fight, Lucy's share of family damage, prompts per enemy turn.

### Step 3: code, in order (each behind its own Global Settings toggle, D-460, defaulting to as built)

| Order | Chunk | Size | Core items (Tier 3) |
|---|---|---|---|
| 0 | Glyph contrast fix (B4 item 1) | S | — |
| 0 | Lucy's preview (U1, redesigned), all branches | S–M | The attack preview path, additive |
| 1 | Readability: the armed badge, End Turn hover, the ghost; roles free (data) | S–M | Each handler's ghost hook |
| 2 | John J1 + J2 (the break, the block, the beat, the cost line) | S–M | `JohnFactionRoleHandler` |
| 3 | **John J3, the swap** | M | `JohnFactionRoleHandler.Activate`, `AEffectSwapper` mid enemy action |
| 4 | Linda's family filter and watched tiles | S | `LindaFactionRoleHandler` |
| 5 | Lucy's beside rule | S | `LucyFactionRoleHandler` |

After chunks 1–3, a **cold player** (not THJ) plays the Ridge and the River: can they say before End Turn which roles are armed, and after the enemy turn why one didn't fire (UX critic's test)? Can they say who John swapped with (creative critic's test)?

**Playtest signal.** *Worked:* players name the family member a role answered for ("he went for Lucy", "she covered Mark"); John's shield goes at least once a fight, and a guard is declined at least once a fight and called right; Linda's Watch fires on at least 1 in 4 enemy turns with enemies in range; Lucy's follow-ups between about one and three a fight, under a fifth of family damage; FTP ends most fights at 4 or less (else DU-5); rounds per fight toward 1.6–2.6. *Failed:* as each failure case above, then that hero's lever, then that hero back to as built.

### What it means for the Hearth

| Memory | Under P2 |
|---|---|
| 1 (Linda alone) | No Watch can fire (no sibling): THJ's "no FR before John" for free. The FP drain can go |
| 3 (John) | Only John's role fires (S2), with no switch. The lesson becomes Shield Up → guard → Wrath boils over → strike the Claw that went for them |
| 4 (Mark) | Linda's Watch can fire next to John, Lucy's follow-ups next to Mark. If THJ wants no roles at all here, it still needs the per-level role switch (after-Hearth F3) |
| River, Ridge | Their ★s hold (Shield Up + Wrath Shield Dash; Explosive Arrow + Blitz). The River gets harder by itself (fewer free guards) |

---

## Questions for THJ

**Q1. Replace the kept-AP test with P2 and its per-hero stop rule?**
- Context: kept AP is dominated whenever a target is in reach (THJ's objection, rechecked). My first per-hero draft made roles readable but not decided (systems critic) and solo-shaped (creative critic); P2 arms each role on the hero's turn and fires it for another Bergson. D-458 (player-turn roles free) still fits; D-459 is replaced; D-460 holds.
- Options: (a) P2: paper, one house-rule session (data: `requiredFTP` 0, prompts paused), code in order, a cold-player check, the per-hero stop rule; (b) P2 with D-457's all-at-once stop rule; (c) lock roles as built now (free) and move to Synergies, keeping Lucy's preview and the readability fixes.
- Recommendation: (a).
- Blocked: every Family Role chunk; the Hearth's role exposure (after-Hearth Q2).

**Q2. John: Shield-Up gate, Wrath boils over (shield gone for a turn), and the swap at any range, all in the test, with John not judged until the swap is played?**
- Context: these are your three John ideas, with Wrath carrying the stamina (one counter, already on the HUD; Memory 3 and the River teach it). The swap is the only thing that makes every guard press a choice (he leaves his post), and the riskiest code (core, mid enemy action). Three rules for one hero exceed D-295's "one new thing", so it's your call.
- Options: (a) all three, the swap as code chunk 3; (b) gate + break only, the swap only if the press still feels like a click; (c) gate only.
- Recommendation: (a).
- Blocked: John's chunks 2 and 3; the session's John rule.

**Q3. Linda: the family filter, or your facing lane?**
- Context: the filter (*"Watch fires on an enemy that ends in her lines next to another Bergson"*) asks "who am I covering": no picker, no core work, Memory 1 silent for free, corridors no longer free kill zones, she keeps arrows; she can't cover herself. The facing lane asks "which way is the danger": one picker on her HUD, works on one-front boards for her own defence; the UX and systems critics found its default already right on most boards. Both together is too narrow to fire. Minimum range on the bow isn't recommended (core targeting work, breaks Memory 1 and the Ridge).
- Options: (a) family filter; (b) facing lane (with the UX fixes and L2 as a lever); (c) filter in the session, facing kept ready as the fallback if it fires too rarely.
- Recommendation: (c), which is (a) with a named fallback.
- Blocked: Linda's chunk 4; the session's Linda rule.

**Q4. Lucy: follows up only a Bergson beside her, plus the preview now?**
- Context: you said she can stay free and needs much better feedback. Free and unlimited, she'd get stronger while the others get weaker (systems critic). The beside rule keeps her free and makes standing near the family the choice, at 15 HP. The ember pool reads as the quiver (all three critics). The preview is wanted under every option.
- Options: (a) beside rule + preview; (b) free + preview, cap 3 a round as a lever; (c) the ember pool.
- Recommendation: (a), with the preview built first, on every branch.
- Blocked: Lucy's preview tech plan; chunk 5.

**Q5. Mark: as built?**
- Context: he wasn't in your proposal. His counter is already for others and positional, so his decision is dive or stay by the family. My Focus-cost idea was always a yes press (systems critic) and can't be decided in a 1 s window (UX critic).
- Options: (a) as built; (b) once per enemy turn (D-042, never built); (c) the Focus bet (*"spends all his Focus and adds it to the hit"*), with his prompt paused.
- Recommendation: (a) for the test, (b) as the first lever if his counters carry fights.
- Blocked: nothing in the first test.

**Q6. Once roles are free, what is FTP for, and what does Pass-by give?**
- Context: with no role sink, pools stay near full and Duo cooldowns bind first, so Duos come often (against your "Duos as finishers"), and Pass-by's only payoff (FTP) stops mattering. Mark's Continuous Attack still costs FTP (D-216's "free" not built).
- Options: (a) Duo cost 3 (DU-5) if FTP ends most fights above 4, and decide Pass-by after the logs; (b) give Pass-by another payoff now (for a later plan); (c) keep roles at 1 FTP after all.
- Recommendation: (a): read the session's FTP log first.
- Blocked: the FTP side of the session read-out.

Names for `miso-narrative` if approved: the "Wrath boils over" beat and John's bark, the ghost's two-word reasons, the badge lines.

## Docs to update (if approved)

After the test, and only for what's adopted:

- `design/gdd/family-systems.md`: FR-3 (no FTP: built), FR-4 and FR-6 (dropped), the role table's trigger column for John, Linda and Lucy, a new **FR-14** for the principle (next free FR ID), FR-9 (armed roles on End Turn hover and through the enemy turn), FR-10 (no longer applies to Linda), FR-12 and FR-13 (John's zone and cover marker go, the tether stays, at any range), a new rule for the "would have fired" ghost and one for Lucy's preview (or CR, beside CR-45, CR-46, CR-49), the Deferred table (kept AP and its variants, the ember pool, Kindle, Mark's Focus cost).
- Character pages: John JO-1 (Wrath boils over, the block), his role line (the swap); Linda LI-11, LI-14 (the filter); Lucy's role line; Mark unchanged.
- `design/gdd/combat-rules.md`: CR-6 (roles free), CR-13 (FTP).
- `design/combat-balance.md`: the "2 reactions per hero per round" assumption.
- Onboarding: the after-Hearth plan's Family Role dependencies (a P2 column), Memory 1's FP drain, Memory 3's lesson text.
- `plans/family-role-chunk.md`: items superseded.
- `decisions.md` (coordinator): Q1 to Q6. Note: D-457 to D-459 are used twice on 2026-11-09 (the Family Roles test and the Lucy-memory gag).

Grids in this plan, to render: `rr2-s1-perhero` (changed), `rr2-s2-perhero` (changed), `rr2-s3-family` (new), `rr2-s3-lane` (kept as the facing alternative, Mark's landing noted), `rr2-s4-river` (new).

## Branches

- **`main`** (and everything that was `thj/onboarding`, D-456): the session and any switch.
- **`thj/home-test`**: no quiver; roles at 1 FTP; the Fireside "first Family Role free" (D-040) to remap once roles are free.

## Risks

- **The swap reads as a bug:** the cold-player check; fallback range 2 without the swap.
- **Linda's filter fires too rarely:** widen "next to", then the facing lane.
- **The tight family dominates:** watch whether hugging is ever wrong (area attacks).
- **FTP unbound:** DU-5, then Q6.
- **The session is half-blind:** THJ can't judge readability; the cold player after chunks 1–3.
- **Paper assumptions:** AI tie-breaks and order, Mark's Blitz landing tile, John's and Lucy's move 3, Claw hits ≈3, sidewinder targeting; the session is the real check.
- **J2's break mid-action:** the `Stat_DR` context history; EditMode tests on an area relay across the break.

## Gates

Design only. Step 1: THJ's time (~15 min). Step 2: THJ's time (one session; data changes on four prefabs, reversible). Step 3: tech plans (coordinator) → implementer (compile, EditMode tests) → reviewer → THJ play check per chunk → a cold player after chunks 1–3. Docs only after adoption.
