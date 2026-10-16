# AP and points model: Fixed vs Shared AP; FTP vs ATB vs no resource for passives

Size: L    Tier: 3    Assigned to: miso-game-designer
Branch: all (the answer decides what both `main` and `thj/home-test` run; today `main` = ATB, `thj/home-test` = FTP, both PerUnit AP)
Status: waiting on THJ

## Why

The two branches run different combat resources (`branches.md`), the Home demo is written against FTP with an "if ATB wins, swap Swift/Spirited" clause (`design/demo-spec.md`, Scope and assumptions), and the merge question "does FTP or ATB win?" is open in `status.md`. Pilot 1 (`status.md`, Next: pilots).

## Goal

One AP model and one passive resource that both branches can run after the merge, chosen on what it does to the four USPs, the QTE pillar and the "too easy" finding.

## Acceptance criteria

- [ ] THJ picks an AP model and a passive resource (or sends this back).
- [ ] The pick is logged as a `D-NNN` row with scope `all`.
- [ ] The docs in "Docs to update" are changed to match.
- [ ] The follow-up tech plan (by the coordinator) and the playtest check below exist before any code changes.

## Scope

In: the rules of AP, the passive resource, how Family Roles and Duos are paid and capped, Bergson Time, what Home effects feed.
Out: per-ability damage numbers, enemy balance, Sisters' Rivalry's own tuning (touched only where it interacts), code.

## Touches

Systems: `APConsumer` / `ActionPoints` / `FamilyActionPoints` (core), `PointConsumer` / `FamilyTimePoints` / `ATBGauge` (core), `FactionRoleHandlerBase` (core), `UnitsCooperationHandler` (core), `PlayerController` Reactive Interrupt (core), `GlobalSettings.asset` (core), Home `HomeSendOffApplier` / `HomeFiresidePayoff` / `HomeCampfirePanel`.
USPs: Family Roles, Synergies, Duos, Home.
Docs: `design/demo-spec.md`, `glossary.md`, `branches.md`, `design/combat-balance.md`, `design/player-skill-trees.md`, `tech/mechanics-brief.md`.

---

## Problem and evidence

**THJ's framing:** choose (a) Fixed vs Shared AP and (b) FTP vs ATB vs no resource for passives.

**Root problem (my restatement):** the passive resource does not currently create a decision. Family Roles fire on their own (behind a QTE prompt), cost 1, and have no per-phase cap, so whichever resource pays for them is either "always enough" (ATB refills in real time) or "spent by whatever triggers first" (FTP drains on auto-triggers and doesn't come back between levels). Neither version asks the player "when do I want my family to act for each other?", and that question is what the Family Roles USP and the QTE pillar both want. The FTP-vs-ATB split is the symptom; the missing decision (and the missing cap) is the cause. AP is a separate, smaller question.

### Verified in code (2026-10-16, `thj/home-test`)

- `GlobalSettings.asset`: `pointConsumptionMode: 0` (FTP), `aPConsumptionMode: 1` (PerUnit), `aPAvailabilityBasedOnUnitCount` = 2 / 5 / 6 / 8 (Shared pool by squad size 1–4), `aPConsumptionEscalationFactors` = [1,1,2,4].
- `PointConsumer` is a plain switch: FTP spends the faction's `FamilyTimePoints`; ATB spends the unit's own `ATBGauge`. A unit without a gauge falls back to FTP.
- Family Roles: `requiredFTP` 1 and `oncePerPhase: 0` on John, Linda, Lucy and Mark (`Unit_*.prefab`). Toba has no role. AI factions skip payment (`FactionControllerBase.ActivateFactionRoleIfFeasible`).
- **The role QTE is already an opt-in.** `PlayerController.ActivateFactionRole` shows the prompt; only a successful QTE runs the role and pays for it (`base.ActivateFactionRole` → `PointConsumer.TryConsume`). Ignoring it silences the role for those targets and costs nothing. So the player already chooses *whether* each role fires; what's missing is a reason to say no.
- **`oncePerPhase` is really "once per faction turn".** `FactionRoleHandlerBase` clears `ActivatedAtThisPhase` on every `turnEnded`, which fires for each faction. With Neutral or Stranger factions acting between enemy turns, a capped role could still fire 2–3 times a round.
- **A Home max bonus is lost on the first death.** `FamilyTimePoints.UpdateCap` sets the practical max to the sum of the living heroes' FP, so Soul Flower Tea's +2 (and the Fireside +2) disappear when any hero falls.
- **Duo cost, finding:** every `CooperationEntry` has `fPCost` 1 and `allConsumeAP: 0` (only the activator spends AP). `Available` checks that *each* partner can pay 1; `ExecuteIE` then calls `TryConsume(1)` *for each partner*. In FTP mode both calls hit the same family pool, so **a duo costs 2 FTP**, and with exactly 1 FTP left the duo is offered, the first spend succeeds and the second fails silently (the duo runs for 1). In ATB mode it costs 1 step from each partner's gauge. Whether 2 is intended is a question below.
- FTP pool: max = sum of the squad's FP attributes (`FamilyTimePoints` constructor; `UnitBase.prefab` FP attribute is backed by `Stat_FP`). The Demo Spec gives the resulting scale as 3 × (heroes − 1), so 6 for a 3-hero sortie and 9 for the 4-hero dungeon (not re-derived from the data here). At each new level (not a restart) the pool gains `FPGain × max` (`FactionTracker.OnLevelLoad`). Producers: pass-by tags (`Bergsons_Ability_TagATBFill_Effect_FunctionCaller`, whose name is swapped with its ATB sibling), abilities with `fpFill` (John's Dash and Shield, Lucy's Teleport and Cyclone, Linda's Harmonic Slam, Toba's Heal/Swap/Taunt/Barrier), the FP potion, Family Dedication, Home rations, `LevelStartFPFiller`.
- ATB: per-unit gauge; fills in real time while enemies act and while allies animate (`CombatLevelRunHandler.HandleATBFill`). Unspent AP converts 1:1 into steps at the end of the player turn (`GUnit.ConvertUnusedApToAtbSteps`, PerUnit only; the Shared version `ConvertSharedFamilyApToAtbSteps` is an empty stub). A unit at 0 AP on its own turn with a full gauge gets +1 AP.
- Bergson Time (Reactive Interrupt, key L): `HandleReactiveInterrupt` returns at once in FTP mode, and `CanAffordFactionRole` reads the ATB gauge only. Porting it to FTP means changing that check to `PointConsumer` and removing the early return; the rest (time scale, pause, unit selection) doesn't depend on the resource.
- Shared AP: one family pool, per-unit escalating cost, and `Closure` consumption is a no-op, so "an attack ends that hero's turn" does not hold in Shared mode. AP→ATB conversion is not implemented there.
- Home on FTP: `HomeSendOffApplier` calls `FamilyTimePoints.AddMaxBonus` (Soul Flower Tea +2, Soul Gourd Pie +1); `HomeFiresidePayoff` makes the first duo or first role free, or adds +2 FP cap; the campfire ration `ftpGain` calls `ProduceFTP`; Dining Table T2 is `Stat_FP` level 1. In ATB mode all of these do nothing or close to nothing (`build-log.md` M6 Step C: "FTP does little in ATB mode"). `LevelStartFPFiller` already has an ATB-fill field, so the Demo Spec's "swap to ATB pre-fill" has a hook.

### Playtests and notes

- `vision.md`: QTEs were fun everywhere, not only in the enemy phase; passive synergies were liked (Linda into Lucy's cyclone; Sisters' Rivalry, though it played as overpowered).
- `design/combat-balance.md`, playtest 2026-10-08 (ATB era, on `main`-equivalent data): still easy; Linda does 46–72 % of the damage, partly because her role fired 3× in one enemy phase; Sisters' Rivalry chained 4 kills in one turn; the Mark–Lucy duo is 0 AP and hits 11–16 × 3. "If > 50 %, her uncapped family role is the lever."
- Home playtests (Oct 13–15, FTP): the Fireside payoffs work ("first Family Role free once, the second costs FP"); the Quickberry Tart +1 AP pip works. No playtest has compared FTP and ATB head to head, and none has tried Shared AP with the current escalation.
- `design/player-skill-trees.md`: Family Time and Family Lookout were removed from the family tree "because main runs ATB", so the skill tree has already been bent by the resource choice once.

What we don't know: how often players pressed L in ATB runs, whether FTP ran dry in the 4-level dungeon, and how long players spent per turn. The playtest at the end asks for these.

## Options compared

### (a) AP

| | Fixed AP (PerUnit, 2 each) | Shared AP (pool 2/5/6/8, escalation [1,1,2,4]) |
| --- | --- | --- |
| Player experience | Every hero acts each turn; positioning per hero; "who goes first" matters through synergies | Family-wide budget; a hero can act 3–4 times at rising cost; "family" as an economy |
| Rules complexity | Low; genre-standard (XCOM) | Medium-high: the price of an action depends on how many that hero already took |
| Implementation | Running today on both branches | Built but not played; `Closure` no-op breaks "attacks end turn"; no AP→ATB conversion; HUD must show per-hero next cost |
| Risk | Low. AP-giving synergies (Sisters' Rivalry, John's AP Transfer, Mark–Linda race) stay readable as gifts | Hero-ball: the 3-hero pool of 5 vs 6 fixed means fewer actions, and the best hero takes 3 (cost 1+1+2 = 4) while others idle; AP gifts become pool top-ups and lose their "from sister to sister" meaning |
| USP effect | Synergies that grant AP stay personal (good for Synergies, Duos) | Thematically "family", but it erases *who* helped whom, which is the point of Family Roles and Synergies |

### (b) Passive resource

| | A: FTP as is | B: ATB as is | C: No resource | D: Hybrid "family points with turn income" (pre-critic leaning; see A+ below) |
| --- | --- | --- | --- | --- |
| Rule | One family pool, ~6/9, refilled by tags, abilities, items, Home | Per-hero 3-step gauge, real-time fill on enemy turns, unspent AP → steps, Bergson Time | Roles and duos free; roles once per enemy phase per hero; duos AP + cooldown | FTP pool kept; each hero ending the player turn with ≥ 1 unspent AP adds +1 FTP (max +1 per hero per turn); roles once per enemy phase per hero; Bergson Time spends FTP; duo cost stated once (2 from the pool) |
| Player experience | Family budget across a mission; drains on auto-triggers; no enemy-turn agency besides QTE | Strong enemy-turn agency (L); "hold AP for the enemy phase" choice; personal, not family | Passives always on, readable; no budget decisions | "Act now or keep a hand free for the family" each turn; family budget; enemy-turn agency (L) |
| Rules complexity | Low | Medium; real-time fill is opaque (depends on animation length and game speed) | Lowest | Medium-low: one bar, one income rule, one cap |
| Implementation | None (today on `thj/home-test`) | None (today on `main`); Home effects need the ATB swap | Data (oncePerPhase on), duo fPCost 0, Home FTP effects redesigned | Data (oncePerPhase on, duo cost) + three small core changes: income at `EndTurn` (next to the existing AP→ATB call), `CanAffordFactionRole` via `PointConsumer`, remove the FTP early return in `HandleReactiveInterrupt` |
| Risk | Hoarding or early dumping; roles fire on low-value triggers and drain the family | Turn-based game with a real-time economy; Home effects become ~dead; the family has no shared stake | Linda's role 1×/phase still strong; loses the Home's best planning goal (Soul Flower Tea) | Income could flood the pool (see systems lens); Bergson Time on a shared pool could let one hero spend it all |
| QTE / reaction pillar | QTE yes, interrupt no | Both | QTE yes, interrupt no (could be ported, but there's nothing to spend) | Both |
| Family Roles | Shared budget = family stake; uncapped | Per-hero = personal; uncapped | Always on, capped | Shared budget + cap + choice of when |
| Synergies | Pass-by tag fills the family pool | Tag fills one gauge | Tag loses its reward (needs another) | Tag fills the family pool |
| Duos | 2 FTP (accidental) | 1 step each | AP only | 2 FTP (stated) |
| Home | Everything works | Tea / Pie / Fireside / Dining T2 / rations need a swap | Tea, Pie, Fireside cap, Dining T2, FTP rations all need replacing | Everything works as written |

**A+ (recommended after the critic pass):** A with D's cap, Bergson Time and duo fix, but **without the turn income**. The rule: one family FTP pool as today; each hero's role at most once per round (reset at the start of the player turn); Bergson Time spends FTP and counts as that hero's role for the round; a duo costs 2 from the pool, checked as 2; a Home max-FTP bonus survives a death. Turn income stays a lever, used only if playtests show the pool running dry. Same Home and USP column as D; less code (no income hook, no income HUD); keeps the across-the-mission scarcity the dungeon is built on.

Option E, "ATB with a family flavour" (pool the gauges, keep real-time fill), was considered and dropped: it keeps B's opacity and still needs the Home swap. Option F, "Shared AP + FTP", is covered by the AP table.

## Lens notes

The lens notes below were written for the pre-critic leaning (D). The critic pass removed D's turn income; the parts about income (ghost segment, income pips, flood risk) apply only if that lever is turned on. Everything else carries over to A+.

### Creative

Target experience (A+): *the family's bar is low and doesn't come back, so every role that fires is someone choosing to protect someone else. I let Lucy's follow-up prompt pass on a Claw that doesn't matter, because I know Linda will be exposed when the Masher moves, and when it lunges, John's shield is there.* The moment we design for: the enemy phase of the Warren's Level 3, family bar at 2, the Masher steps toward Lucy, and the player presses L to freeze time and send John in, knowing it leaves nothing for Linda's shot.

- A is warm (one family bar) but passive: the family protects itself on autopilot until the bar runs out, often on a trigger the player didn't care about.
- B gives the best single moment (Bergson Time) but each hero has their own gauge. It reads as a JRPG ATB system, not as a family under pressure, and it isn't original.
- C keeps the passives warm and constant, but nothing is at stake: protection is free, so it doesn't mean much.
- D turns "I didn't use all my AP" into "I kept a hand free for my family", which is the Children of Morta feeling (everyone gives something so someone else is safe) expressed as a rule. I haven't seen this exact loop (unspent action feeding a shared reactive pool spent through a time-stop) in the inspirations: Midnight Suns' Heroism is a shared pool but is spent on your own turn; XCOM's Overwatch is per unit and has no shared stake; FFT's Charge Time is per unit.

### Systems

D's rules, proposed starting values:

| Lever | Start value | Why |
| --- | --- | --- |
| Pool max | As today (≈ 6 for 3 heroes, 9 for 4) | Home bonuses are tuned against it |
| Level-start gain (`FPGain`) | As today | Not changed by this plan |
| Turn income | +1 FTP per hero who ends the player turn with ≥ 1 unspent AP; max +1 per hero | Costs a real action (half a hero's turn) for 1 FTP, so it is a trade, not free money |
| Role cost | 1 | As today |
| Role cap | Once per enemy phase per hero (`oncePerPhase: 1`) | Directly targets Linda's 3× per phase; also keeps one hero from draining the pool |
| Bergson Time | Spends the role's cost from the pool; counts as that hero's role for the phase; 0.5 s re-entry cooldown as today | No extra cost: the time-stop is a way to aim the role, not a new power |
| Duo cost | 2 total from the pool, checked as 2 (fix the "1 left" case) | Makes today's actual behavior the rule; the Fireside "first duo free" keeps meaning something |
| Tag (pass-by) | +1 FTP once per pair per turn, as today | Keeps Synergies paying the family |

Interactions and failure cases:

- **Income flood.** A 4-hero squad that ends every turn with 1 AP each gets +4 per turn on a 9 pool. That is the main risk; the cap is the safety, and the lever is the income per hero (try +1 per two unspent AP if the bar sits full).
- **"Pass the turn" degenerate play.** Ending with a full 2 AP gives the same +1 as ending with 1, so skipping a whole hero's turn gains nothing extra. Good: the cheapest legal trade is "move but don't attack".
- **AP gifts.** Sisters' Rivalry and John's AP Transfer give AP that, if unspent, turns into FTP. That's acceptable (it's still a family gift), but Sisters' Rivalry's chain (4 kills in a turn) is its own problem and not fixed here.
- **Masher counter.** Enemy roles don't pay (AI skips payment) and aren't affected.
- **ATB-only content.** The Mark–Linda race gives the winner +1 ATB (`UnitsCooperationHandler`) and the "Mark Turn ATB Fill Floor" run upgrade sets a gauge floor; both need an FTP equivalent (+1 FTP; "start each turn with ≥ 1 FTP") or are dropped. Family Time / Family Lookout (removed skill-tree nodes) could come back.
- **Fixed AP + D.** Shared AP and D don't combine well: unspent shared AP is one number, so "which hero kept a hand free" disappears. That is one more reason to keep Fixed AP.

### UX

What's shown when (D):

- **Player turn:** the family bar shows the current FTP and a ghost segment for the income it will get if the turn ended now ("+2 at turn end"). Each hero portrait with unspent AP shows a small family-point pip, so "ending here gives +1" is visible before clicking End Turn.
- **End Turn:** the income lands as one animated gain with the source heroes' portraits flashing (reuse the FP gain VFX).
- **Enemy phase:** each hero's portrait shows "role ready" or "role used this phase". When the family can afford a role, an "L: Bergson Time" hint shows near the bar; it greys out at 0 FTP or when every hero's role is used.
- **Duo button:** "2" on the family-point icon, red if the bar is below 2.

Likeliest misread: the player thinks unspent AP is lost (genre habit) or that it carries over as AP. The pip on the portrait and the ghost segment are there for that. Second: "my role didn't fire": once-per-phase needs a visible "used" state, or players will read it as a bug.

Where the lenses disagree: creative wants Bergson Time to cost more (so it feels like a sacrifice); systems wants it free (it's an aiming tool, and a surcharge makes the QTE pillar a tax). I lean free, and would revisit only if playtests show L pressed every phase.

## USP check

- **Family Roles:** strengthened. A per-phase cap plus a shared budget makes each role a choice; Bergson Time lets the player decide which family member to protect.
- **Synergies:** neutral to slightly strengthened. The pass-by tag keeps feeding the family pool; AP-giving synergies now have a second value (unspent AP turns into family points).
- **Duos:** neutral. Cost made explicit (2); the Fireside "first duo free" still matters.
- **Managing the Home as a Family:** strengthened against B and C. Every FTP effect in the Demo Spec keeps working, and Soul Flower Tea stays the dungeon's planning goal. No Swift/Spirited swap is needed.

Fixed AP: neutral on purpose. Shared AP would be "family" in name but weakens Synergies' and Family Roles' sense of who helps whom.

## Effect on the Home demo

- **A / D:** nothing changes. Quickberry Tart (+1 AP on turn 1) still works under Fixed AP. Under D an unspent Tart AP also turns into +1 FTP, which is fine.
- **B:** Spirited dishes (Tea, Pie) and rations swap to ATB pre-fill through `LevelStartFPFiller`'s ATB field or a new `DishEffect` field; Fireside "FP cap +2" needs an ATB meaning (+1 step on every gauge?); Dining Table T2 (`Stat_FP`) needs a new stat. Roughly one implementer session plus a Demo Spec pass.
- **C:** Tea, Pie, Fireside cap, Dining T2 and FTP rations all need new effects; "first role free" means nothing. The Demo Spec's clearest planning goal is gone. Largest Home cost.
- **Shared AP:** Quickberry Tart becomes +1 to the family pool on turn 1 (works through the redirect in `APConsumer.Produce`); Hungry Moon is enemy-side and unaffected.

## Effect on the QTE and reaction-timing pillar

Every option keeps the role QTE prompts (they're independent of the resource). Only B and D keep Bergson Time. Under D the time-stop is more legible than under B, because the player can see the family bar instead of four real-time gauges whose fill depends on how long the enemy's animations last.

## Implementation cost and risk

| Option | Work | Core systems touched | Risk |
| --- | --- | --- | --- |
| Fixed AP | None | None | None |
| Shared AP | Fix `Closure`, write the Shared conversion, HUD next-cost per hero, re-tune pool | APConsumer, PlayerController | Medium-high; also changes the AI regression catalogs if enemy AP paths move |
| A | Duo cost fix only | UnitsCooperationHandler | Low |
| B | Home swap (above), skill-tree nodes stay removed | Home only (not core) | Low-medium |
| C | Data (oncePerPhase, fPCost 0), tag reward replacement, Home redesign | Data + Home | Medium (design work) |
| D | Data (oncePerPhase 1 on four prefabs, duo cost); turn income in `PlayerController.EndTurn`; `CanAffordFactionRole` via `PointConsumer`; remove the FTP return in `HandleReactiveInterrupt`; HUD: income ghost, role-used state, L hint; replace two ATB-only rewards | PlayerController, UnitsCooperationHandler, GlobalSettings (all core, Tier 3) | Medium: a few small core edits; the HUD work is the larger part |

D can be split so each step is playtestable on its own: (1) data only: role cap and the duo cost made explicit; (2) turn income; (3) Bergson Time on FTP; (4) HUD.

## Critics

Three critics ran in parallel, one lens each, all given the leaning **Fixed AP + D**. The `miso-design-critic` agent type wasn't registered in this session, so they ran as read-only agents with the critic definition's instructions and output format (`claude-config/agents/miso-design-critic.md`).

| Critic | Strongest point | What I did with it |
| --- | --- | --- |
| Creative | Turn income dissolves the pressure the dungeon is built on ("one point left on Level 3: John's shield or Linda's shot") and rewards idling. Under Fixed AP the only way to earn it is a hero who didn't attack, which is banking, not a family moment. | **Accepted.** The income is dropped from the recommendation (A+). It stays as a lever if the pool runs dry. |
| Systems | D's income (≤ 1 per hero) equals what the cap lets roles spend (≤ 1 per hero), and the pool starts full with other income on top, so banking is either worthless or a fixed tax. | **Accepted**, same change. |
| Systems | `oncePerPhase` resets on every faction's turn end, so the cap leaks with Neutral/Stranger factions. Duo check must compare the summed cost. `UpdateCap` loses Home bonuses on a death. | **Accepted, verified in code.** The cap is now "once per round" (reset at the player turn start); the duo is checked as 2; Home bonuses survive deaths. All three are in A+. |
| Systems | "Roles auto-pay first come, first served; let the player arm or skip roles." | **Rejected on the facts:** the role QTE already is the opt-in, and payment happens only on success (verified). Kept the underlying point for UX: the prompt must show the cost and the "uses this hero's role" consequence, so saying no is a decision and not a missed QTE. |
| Systems / creative | D does nothing about Sisters' Rivalry chains (5 attacks, 4 kills in a turn), and Fixed AP leans on it as the family's AP-layer identity. | **Agreed it's real, kept out of scope.** It's a separate balance item (a once-per-turn cap is the obvious candidate), listed under Docs/follow-ups. |
| UX | The worst misread is Bergson Time: L on John early in the enemy phase silently costs his shield later in the round, while the bar still shows FTP. Needs per-hero "role ready / used" pips, an "uses John's role this round" label on the interrupt, and a visible "L: Bergson Time" hint only when it can be used. | **Accepted.** These become required HUD for A+ (below). |
| UX | A duo can spend the reserve the player meant for the enemy phase; the bar's carry-over between levels is unexplained. | **Accepted:** duo hover greys the 2 segments it takes; the level-start banner says where the FTP came from. |
| Creative | Play Shared AP before locking Fixed: it's the only option where the family shows in the AP rules. | **Not taken as the recommendation.** Systems and UX both said don't ship Shared (half-built, hero-ball, unreadable cost, and it breaks "per hero" rules). Offered to THJ as an optional experiment in Q2. |
| Creative | Bergson Time capped and counted as the role "becomes a numbers choice". | **Partly.** Kept "counts as the role" (otherwise L doubles role uses and undoes the cap) but kept it free of surcharge, so the time-stop is about *aiming* the family's help. Q4 asks THJ. |

What changed my mind: both the creative and systems critics, independently, hit the turn income from opposite sides (feeling and numbers). That's enough to drop it. What didn't: the "no opt-out" claim, which the code contradicts.

## Recommendation

**Fixed AP + A+ ("Family Points, capped, with Bergson Time")**, scope `all`. On merge, `main` moves from ATB to FTP.

Rules and starting values:

| Rule | Start value | Data / code |
| --- | --- | --- |
| AP | Fixed, 2 per hero, as today | No change |
| Family pool | As today (≈ 6 for 3 heroes, 9 for 4), starts full, level-start `FPGain`, no refill otherwise except tags, abilities, items, Home | No change |
| Role cost | 1 | No change |
| Role cap | Once per round per hero, reset at the start of the player turn | `oncePerPhase: 1` on the four role prefabs, plus the reset moved from "any `turnEnded`" to the player faction's turn start (core, `FactionRoleHandlerBase`) |
| Declining a role | Ignore the QTE: no cost, role stays available for the next trigger this round | Already how it works; the prompt must show cost and consequence |
| Bergson Time | Available in FTP mode; spends the role's cost; counts as that hero's role this round; no surcharge | `HandleReactiveInterrupt` early return removed, `CanAffordFactionRole` via `PointConsumer` and the role cap, `ConsumeActionCost` override checked (core, `PlayerController`) |
| Duo cost | 2 from the pool, checked as 2 | `CooperationEntry.Available` and `ExecuteIE` (core); Fireside "first duo free" keeps working |
| Home max bonus | Survives deaths | `FamilyTimePoints.UpdateCap` keeps `AddMaxBonus` amounts (core) |
| ATB-only rewards | Mark–Linda race winner: +1 FTP instead of +1 ATB. "Mark Turn ATB Fill Floor" run upgrade: retire, or "start each round with ≥ 1 FTP" | `UnitsCooperationHandler` (core), `RU_MarkTurnATBFillFloor` |
| Turn income (lever, off) | +1 FTP per hero ending the turn with ≥ 1 unspent AP | Only if the playtest shows the pool empty by the Warren's Level 3 with Soul Flower Tea eaten |

Required HUD (from the UX pass):

- Each hero portrait: role ready / used this round.
- Role QTE prompt: "1 FP" and the hero's name; on Bergson Time selection: "uses John's role this round".
- "L: Bergson Time" hint near the bar, only while some hero can afford an unused role.
- Duo hover: the 2 segments it will take shown on the bar, red if short.
- Level start: the "From Home" banner (or bar tooltip) says where the opening FTP came from (carried, level start, dish).
- Bar shows its max, including Home bonuses.

Why A+ over the others: it is the only option that gives Family Roles a cap (the Linda finding), keeps a family-wide stake (Family Roles USP), keeps both halves of the reaction pillar (QTE plus Bergson Time), and leaves every Home effect in the Demo Spec working (Home USP), for a handful of small core edits plus HUD. B keeps the time-stop but makes the Home's food and Fireside rewards near-dead and the economy real-time. C is the cleanest read but removes the "who do I protect" stake and the Home's best planning goal. Shared AP is half-built and hides who helped whom.

Rollout, each step playtestable alone:

1. **Data:** role cap on (`oncePerPhase: 1`). With the faction-turn leak this is approximate, but it's free and shows the Linda effect at once.
2. **Core fixes:** cap reset per round, duo checked as 2, Home bonus survives deaths.
3. **Bergson Time on FTP.**
4. **HUD** list above.
5. Swap the two ATB-only rewards.

**Playtest signal** (one Home sortie plus the Warren, THJ or Part B participant):

- **Worked:** Linda's damage share under 50 % in a full squad; at least one role QTE declined on purpose per level (combat log: QTE ignored with FTP ≥ 1); Bergson Time used at least once per level; FTP at the start of Warren Level 4 is 1–3 without Soul Flower Tea and visibly more with it; the player can say before the enemy phase which heroes' roles are live.
- **Failed:** FTP sits at max most rounds (pool too big: shrink it, or drop the level-start gain), or is 0 from Level 2 on (turn on the income lever); Bergson Time never pressed (discoverability) or pressed every round (too cheap); players call the role cap a bug.

The combat log doesn't record FTP/AP changes or QTE results yet (`tech/combat-log.md`); adding "FP spent/gained" and "role QTE ignored" lines is part of the follow-up so the signal can be read.

## Questions for THJ

**Q1. Which passive resource do both branches use?**

- Context: `main` runs ATB, `thj/home-test` runs FTP; the Home demo is written against FTP; playtests found the uncapped roles too strong. Touches Family Roles, Duos, Home, the QTE pillar.
- Options:
  - A+, capped FTP with Bergson Time (recommended): a few core edits plus HUD; Home unchanged.
  - B, ATB: no core edits, but a Home swap pass and still uncapped roles.
  - C, no resource: data edits plus a Home redesign; loses the budget.
  - D, A+ with turn income: more code; the critics found it flattens scarcity.
- Recommendation: A+. It's the only option that caps roles, keeps the family stake and Bergson Time, and leaves the Home spec intact.
- Blocked meanwhile: the merge resource question in `branches.md`, the Demo Spec AP/FTP assumption, any FTP/ATB balance work. Not blocked: Home presentation work and the report-card pilot.

**Q2. Fixed or Shared AP?**

- Context: both branches run Fixed (2 each). Shared (pool 2/5/6/8, escalation [1,1,2,4]) exists but is unplayed, its `Closure` no-op means attacks don't end a hero's turn, and its ATB conversion is a stub.
- Options:
  - Fixed (recommended): no work.
  - Shared: fix `Closure`, add the HUD next-cost, re-tune; medium cost and risk of hero-ball.
  - Fixed now plus a one-session Shared experiment later, on a scratch branch, after its two gaps are fixed.
- Recommendation: Fixed. Family AP sharing already comes through Sisters' Rivalry, John's AP Transfer and the Mark–Linda race, which keep "who helped whom" visible.
- Blocked meanwhile: nothing; Fixed is what runs.

**Q3. Is a duo meant to cost 2 FTP (1 per partner) or 1?**

- Context: data says `fPCost` 1, but in FTP mode each partner pays it from the same pool, so a duo costs 2, and with 1 left it runs for 1.
- Options:
  - 2, checked properly (recommended): matches what players have been playing.
  - 1 total: duos become cheap next to capped roles.
- Recommendation: 2. A duo is two family members giving at once, and "first duo free" stays a real payoff.
- Blocked meanwhile: the duo fix in rollout step 2.

**Q4. What does Bergson Time cost?**

- Context: under A+ it spends FTP. If it doesn't count as the hero's role for the round, it doubles role uses and undoes the cap.
- Options:
  - The role's cost, counts as the role (recommended).
  - The role's cost +1, counts as the role: more weight, but taxes the QTE pillar.
  - The role's cost, does not count as the role: more agency, cap leaks.
- Recommendation: the first. The time-stop is a way to *aim* the family's help, not extra help.
- Blocked meanwhile: rollout step 3.

**Q5. When does this apply to `main`?**

- Context: the decision is scoped `all`, but `main` has no Home and runs ATB; `branches.md` asks how and when `thj/home-test` merges.
- Options:
  - Build A+ on `thj/home-test` now, and `main` picks it up at merge (recommended).
  - Switch `main` to FTP now too (one setting), with the cap data, before the merge.
  - Wait for the merge and build once on `main`.
- Recommendation: build on `thj/home-test` now. The Home demo is where FTP is exercised and playtested; the merge carries it over, and the switch on `main` is one setting plus this data.
- Blocked meanwhile: `main` keeps ATB until then; its skill-tree nodes Family Time / Family Lookout (removed "because main runs ATB") stay removed until you say whether they come back.

## Docs to update if approved

- `design/demo-spec.md` (coordinator): replace the "If ATB wins, Swift and Spirited swap" assumption with the chosen model; the "FTP scale" open question gets the pool values; note that Home max-FTP bonuses survive deaths.
- `glossary.md` (narrative): ATB and Bergson Time entries (Bergson Time no longer "ATB mode only"); "once per round" for Family Roles; duo cost 2.
- `branches.md` (coordinator): the combat-resource line for both branches; close the "FTP or ATB on merge" question.
- `design/combat-balance.md` (me): role cost and cap line; the Linda lever marked as applied.
- `design/player-skill-trees.md` (me): note whether Family Time / Family Lookout return.
- `tech/mechanics-brief.md` / `tech/combat-architecture.md` (coordinator): after the build, the points section.
- `decisions.md` (coordinator): a `D-NNN` row per answered question.
- Follow-ups for `status.md` (coordinator): Sisters' Rivalry chain cap (balance, Tier 3); combat-log lines for FP spent/gained and role QTE ignored; `ATBGaugeView.RefreshMarkers` writes the point count into `nameLabel` (UX critic's finding, not verified here; only matters if B wins).

## Risks

- Choosing on design reasoning without a head-to-head playtest. Handled by the staged rollout and the playtest signal.
- Core-system edits (Tier 3) before the merge, so `main` and `thj/home-test` diverge further. Handled by scoping the decision `all` and building it once, after the merge question is answered.

## Gates

Compile / tests / review: in the follow-up tech plan, not here. Play check: yes (THJ's time, one sortie plus the Warren). Docs: listed above.
