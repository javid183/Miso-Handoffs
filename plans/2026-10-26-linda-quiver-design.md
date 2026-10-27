# Linda's Quiver

Size: L    Tier: 3 (how a main mechanic works; Family Roles; a new grid object)    Assigned to: game designer
Branch: all (to be built on `main` inside the [Family Role chunk](family-role-chunk.md), replacing Linda's part of item 1)
Status: approved for a prototype (THJ, 2026-10-26); pierce and the Watch cap are reconsidered after the playtest

## Why

Linda deals 46–72% of the family's damage ([`combat-balance.md`](../design/combat-balance.md), October playtests): her Watch role ([Family systems](../design/gdd/family-systems.md#family-roles), Linda row) fires on every enemy that ends a move in her row or column, with no limit, and her arrows pierce. The planned fix is a per-round cap of 2 shots (D-039, D-041, D-042; FR-4, FR-5). THJ, 2026-10-26: a flat cap throws away good moments and doesn't improve how she plays. His idea: give her a **quiver**.

## Goal

Limit Linda's arrows with a resource that lives on the board and can be won back, so that her Watch becomes a real choice and her turns get a new decision, instead of a hidden counter that resets every round.

## Problem and evidence

- Watch costs 1 FTP on `main` today and has no limit (FR-3, FR-4 "Built, differs"). D-036 makes roles free; D-042 caps them per round. The per-round counter is new code either way (D-061).
- Playtests: one Linda shot hits 2–4 enemies (7/4/3); her role fired 3× in one enemy phase; Sisters' Rivalry chained 4 kills in one turn (M5 C2 R1).
- Fights are tuned to last 1.6–2.6 rounds (`combat-balance.md`), so any limit that resets each round barely bites across a fight.
- Masher play check item 16: the Masher stepping into her lane makes her shoot again on every step.

## Options compared

| Option | Player experience | Rules complexity | Implementation cost | Risk | USP effect |
| --- | --- | --- | --- | --- | --- |
| A. Do nothing | Linda carries every fight; other kits feel optional | None | None | Balance stays broken | Watch stays the only role that matters |
| B. Per-round cap of 2 (D-042, planned) | Same Linda, fewer shots; a 3rd trigger is silently lost | Low (a pip count) | Low: a per-round counter (needed for the other roles anyway) | Trims her peak, not her share across a fight; missed moments | Neutral |
| **C. Quiver (THJ's idea, recommended)** | An archer who fetches her arrows; the family helps; Watch is a choice; Recall is a big moment | Medium: arrow count, grounded arrows, pickup, Recall | Medium–high: a new grid object, pickup on move paths, Recall, UI | New state to read; a dump-to-recall loop; tuning the size | Strong: Watch gets a cost with a choice; Catch & Return gets a purpose; new Synergy and Duo hooks; a Home upgrade |
| D. Watch arrows don't pierce | Same Linda, less damage per reaction | Very low | Very low (data) | Cuts damage only; overuse stays | Neutral |
| E. Aimed Watch (she picks one lane at turn end, XCOM overwatch) | A deliberate guard decision each turn | Low–medium | Medium: an aim step and a facing on the zone | Another click per turn; strong enemies avoid one lane easily | Mild |

C can take D as a lever later if her share stays high.

## Proposed design (option C)

Rule IDs are proposed, the next free LI numbers. All values are starting points for a playtest.

- **LI-3. Quiver.** Linda carries a number of arrows: 4 at the start. The count shows as a segmented bar under her unit (the old ATB bar view) and on her unit panel.
- **LI-4. What spends an arrow.** One per shot: bow attack, Watch (her Family Role), Explosive Crescendo, and the arrow Duos she fires (Linda–Lucy Marks-Sisters, Linda–Toba Healing Marks). Tempest Bloom's split copies and Mark's Catch & Return bounce spend nothing extra. Harmonic Slam, Cleanse and movement need no arrow.
- **LI-5. Empty quiver.** With 0 arrows her arrow abilities can't be used and Watch does not trigger (her zone hides; her badge shows an empty quiver). Recall is its own button (LI-8).
- **LI-6. Where an arrow lands.** On the tile of the last enemy it hit. With no enemy hit, at the end of its range; Explosive Crescendo's on its centre cell; Duo arrows at the end of their line. An arrow is never lost: one that would land in a pit, off the grid or on a blocked cell lands on the last valid cell of its path. A tile can hold several arrows (a stack count).
- **LI-7. Pickup.** Any Bergson whose move path enters a tile with arrows picks them all up, and they go straight back to Linda's quiver (up to its size; extras stay on the tile). Forced and Duo moves count (Command, John–Linda Dance). An arrow under a living enemy can't be reached until the enemy moves or dies. Enemies ignore arrows (for now).
- **LI-8. Recall.** Its own button, usable whenever at least one arrow is grounded (THJ, 2026-10-26). 1 AP, cooldown 2 (once every other turn). Every grounded arrow, including one under a living enemy or behind a wall, flies in a straight line back to Linda, ignoring obstacles, and refills the quiver. Base Recall deals no damage. Tempest Bloom copies never land, so she owns exactly her quiver size in arrows.
- **LI-9. Catch & Return.** When Mark bounces her arrow back (as built), it ends in Linda's quiver instead of on the ground.
- **LI-10. Level end.** All arrows come back; she starts every level with a full quiver.
- **LI-11. No round limit on Watch.** The quiver is her limit: this supersedes D-041 and Linda's part of D-042 (FR-4, FR-5). Lucy, Mark and John keep their caps. No backstop cap in the prototype (THJ, 2026-10-26); reconsider after the playtest.
- **LI-12. Fireside.** D-040's "Linda gets a third shot" becomes "+1 arrow at sortie start, above her quiver size".

**Growth**

| Source | Effect | Starting value |
| --- | --- | --- |
| Skill node "Deep Quiver" | Quiver size, within the cap of 6 total (THJ, 2026-10-26) | +1, 1 pip |
| Skill node "Barbed Recall" | Recalled arrows hit enemies on their way back, each enemy once per Recall | 3 × damage, no falloff |
| Workshop: a quiver for her free slot (instead of Shin Armor) | Quiver size, within the cap of 6 | +1 |
| Run upgrade (optional) | Recall cooldown, or pickup from 1 cell away (not size) | −1 / on |

Total arrows are capped at 6 (4 base + 1 tree + 1 workshop); the Fireside arrow (LI-12) is a one-sortie bonus above it. Further growth goes to Recall and pickup, not size.

**Seeds for later Synergies and Duos** (not in this plan's scope): Lucy's Cyclone gathers arrows it passes and scatters them when it ends; Toba blooms a grounded arrow into a healing sprout; the John–Linda Dance as a cleanup move; an Explosive Crescendo node that sets off grounded arrows next to it; an enemy that steals grounded arrows.

## Lens notes (designer's own pass, before the critics)

- **Creative.** An archer who has to fetch her arrows, with the family handing them back, is a small family moment that happens every fight. Mark catching her arrow becomes a deliberate play. Grounded arrows put her story on the board, like Into the Breach's readable state.
- **Systems.** Players may fire their last arrow into nothing to unlock Recall; the cooldown of 2 stops it looping. Recall damage is on the tree so arrow placement can't become her best attack at the start. Sisters' Rivalry chains and the Masher lane chain are capped by arrows without touching either rule. D-036 removed the FTP cost because a cost "adds counting without choice"; the quiver's cost is Linda's own, visible and recoverable by moving, and doesn't starve the Duos' FTP.
- **UX.** Needs: the arrow count always visible; a grounded-arrow icon with a stack number; move previews showing "+N arrows" on the path; the Watch badge and zone reflecting an empty quiver. Risk: the role QTE window is 1 s, which is short for "save my last arrow?".

## USP check

- **Family Roles:** Watch gets a cost with a decision; the press becomes meaningful.
- **Synergies:** Catch & Return gains a purpose (LI-9); grounded arrows open new ones.
- **Duos:** arrow Duos cost an arrow as well as FTP; John–Linda Dance gains a use.
- **Home:** a workshop quiver and the Fireside arrow.

## Critics

Three critics (creative, systems, UX), run in parallel on 2026-10-26, each blind to the others.

| Lens | Strongest point | What I did with it |
| --- | --- | --- |
| Systems | The quiver limits shots per level, not damage per shot. At 4 arrows she is empty in round 1; at 8 (tree + workshop + Fireside) she never runs dry in a 2.5-round fight, and LI-11 removed the cap. Arrows land where melee is happening, so John and Mark pick them up for free (Fist Blitz steps into the kill cell). Pierce, the real cause (7/4/3), is untouched | **Accepted.** Pierce goes on the table as D, tested first. Quiver growth is capped (total 6). A Watch backstop of 3 per round stays in the prototype until data says it can go |
| UX | The choice the quiver creates is made blind: Watch is a 1 s real-time press, and the player can't see where the arrow lands or whether it can come back. Linda ends the enemy phase at 0, with no zone and a bow that says Recall, and no answer to "why can't she shoot?" (the same "trigger but blocked" confusion the role-readability work fixed) | **Accepted.** The Watch prompt shows "Arrows 3 → 2"; bow and Crescendo previews show the landing tile; arrows draw above sprites with a stack number and a "locked under enemy" state; arrow-shaped pips, not the ATB segments (D-036 dropped ATB as confusing) |
| Creative | Automatic pickup is a routing optimisation, not an act of care; the "family hands her arrows back" beat isn't felt. "Limited ammo, walk over it" is the genre default; the original part is the family part | **Partly accepted.** A pickup plays a short named hand-back (toss + bark + Linda's reply), once per pickup. Not accepted: cutting the never-lost rule (a lost arrow is a worse feel-bad than the rule's cost) |

Points raised by two or more critics, now changed in the rules:
- **Recall at any time** (systems + UX). LI-5/LI-8 locked Recall to an empty quiver, which forces "fire the last arrow into nothing, then Recall": two AP, no damage. Recall becomes its own button, usable whenever at least one arrow is grounded. This changes THJ's "abilities change to Recall when empty" (question 2).
- **LI-7 vs LI-8 contradiction** (UX). Recall is magic: it pulls every arrow, including those under living enemies and behind walls, in a straight line ignoring obstacles. Walking pickup still needs the tile free.
- **Barbed Recall** (systems). Hits each enemy once per Recall, not once per arrow; otherwise four arrows behind a clump is 12× per enemy for 1 AP.
- **Conservation** (systems). Tempest Bloom copies never land. Linda owns exactly her quiver size in arrows; nothing duplicates them.
- **Previews** (UX). Recall shows each return line (and Barbed Recall damage, CR-45/CR-46 style); the move preview shows "+N arrows" per cycled path (CR-17); a Duo greyed out for arrows says so.

Not changed, noted as risks: the Duos' arrow tax (systems: taxes the USP; kept because they are her strongest shots, revisit with data); Catch & Return as a free double shot (systems: could become dominant; it is gated behind a Family Skill Point); implementation cost is above "medium–high" (pickup on collider overlap vs the logical path; `GridCell` has one planted-entity slot) and needs a tech spike before commitment.

## Recommendation

As approved by THJ (2026-10-26): **a minimal quiver prototype, alone.** The designer's earlier "D first" and "Watch cap of 3" are not in the test; both are reconsidered after it.

1. **Prototype (C, minimal):** quiver 4, Recall as its own button (1 AP, cooldown 2, any time ≥ 1 arrow is grounded, no damage), walking pickup by any Bergson with the hand-back beat, arrows back at level end, Catch & Return into the quiver, no Watch cap. Pierce unchanged. No skill nodes, no workshop item, no Fireside change yet. The previews from the UX critic ship with it (arrow pips, "Arrows 3 → 2" on the Watch prompt, landing tile, grounded-arrow icon with stack and locked state, "+N arrows" per path, Recall lines).
2. **After the playtest:** decide pierce (D) and a Watch cap from the logs.
3. **If it works:** growth within the cap of 6 total, then through Recall and pickup.

Playtest signals (M4, M6 with a full squad; read the combat logs; compare against the current build):
- Linda's damage share below 50%.
- Recall used about once per level; Linda has no turn with nothing useful to do.
- The player sometimes declines a Watch prompt to save an arrow (a sign the choice is real).
- Other Bergsons pick up arrows without being told to, and testers talk about it (creative critic's test).
- The quiver is empty or nearly so by round 2 in at least 60% of fights (systems critic's test); if arrows mostly come back by incidental walk-overs and it is never empty, the quiver isn't the limit.
- Cold players can say how many arrows Linda has and why Watch stopped, after one or two enemy phases (UX critic's test).

## Questions for THJ

Answered by THJ, 2026-10-26: 1 (b), quiver only, reconsider pierce after the playtest; 2 (a), its own button; 3 (b), no cap in the test, reconsider after it; 4 (a), cap at 6.

1. **Pierce first?** Context: all three critics name pierce (one shot hitting 2–4) as the cause the quiver doesn't touch. Options: (a) Watch arrows don't pierce now, quiver after; (b) quiver only; (c) both together. Recommendation: (a). Blocks: the first playtest build.
2. **Recall any time, or only when empty?** Context: empty-only forces dumping the last arrow (2 AP, no damage) and confuses the bow slot. Options: (a) separate button, any time ≥ 1 arrow grounded; (b) your swap-when-empty. Recommendation: (a). Blocks: the Recall rule.
3. **Keep a Watch cap in the prototype?** Context: the quiver alone may not bind in melee fights. Options: (a) cap 3 per round until data says otherwise; (b) no cap. Recommendation: (a). Blocks: LI-11.
4. **How does she grow?** Context: quiver size growth undoes the fix. Options: (a) cap total arrows at 6, grow Recall and pickup instead; (b) size growth as first proposed. Recommendation: (a). Blocks: Deep Quiver, the workshop item.

## Docs to update if approved

The GDD changes wait until the prototype is played: the rules go in as *Planned* when the tech plan starts, and settle after the playtest.

[`linda.md`](../design/gdd/characters/linda.md) (LI-3 to LI-12, Q2), [`family-systems.md`](../design/gdd/family-systems.md) (FR-4, FR-5, FR-6 "Watch" wording, Catch & Return row, D-040 note), [`combat-rules.md`](../design/gdd/combat-rules.md) (grounded arrows as a grid object, if it has a home for those), [`progression-economy.md`](../design/gdd/progression-economy.md) (Deep Quiver, Barbed Recall, the workshop quiver), [`family-role-chunk.md`](family-role-chunk.md) (items 1 and 10), `glossary.md` (Quiver, Recall), `decisions.md`.
