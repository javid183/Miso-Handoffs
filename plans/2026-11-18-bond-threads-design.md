# Bond Threads: a small track for every pair (design)

Size: L    Tier: 3 (major design: replaces the Family tree's layout, touches all four USPs, needs one parked core change)    Assigned to: miso-game-designer
Branch: all
Status: waiting on THJ

## Why

THJ (2026-11-18): give each pair of Bergsons a small bond skill tree. Each Bond level opens a tier; some skills upgrade. It must stay small, because pairs grow as n(n−1)/2: 5 fighters make 10 pairs, 6 make 15, 7 make 21. Today the pair content is scattered: the "Family tree" is nine pair nodes parked on four personal trees ([`player-skill-trees.md`](../design/player-skill-trees.md)), Bond Lite gates three of them for one pair only ([Family systems](../design/gdd/family-systems.md) BO-4), and the bond-tree change for the sisters is approved but parked (D-519 to D-524).

## Goal

One small, readable track per pair, where a Bond level is a moment in that relationship, the family's existing Synergies and Duos are the content, and the whole thing browses in two clicks however many pairs there are.

## Acceptance criteria (for the design, once approved)

- [ ] Every pair has at most 3 knots and 1 upgrade line (≤ 2 pips).
- [ ] Every built pair Synergy and Duo has exactly one home in a track; nothing built is lost.
- [ ] No knot is a brand-new mechanic: each is built, planned, or a small variant of something built.
- [ ] Any pair is reachable in 2 inputs from the skill-tree page.
- [ ] The onboarding demo's teaching order (Papa's Shelter, Shield Flare, Catch & Return before M4; the sisters' first Duo in M4 after the Yard, D-470) still holds.

## Scope

In: the direction, names, the track shape, the 10 tracks, the Family tree's and personal trees' fate, the menu, the demo cut, a build outline for the TD.
Out: final numbers (playtest), final text and names (`miso-narrative`), Toba's Family Role design (FR-7, still open), Trios (D-215, deferred).

## Touches

Systems: Bond Lite (`BondStore`, `BondSettingsSO`, `HomeLockRules`, `BondNodeGate`, `BondSources`), `SkillTree` data on the `Unit_*` prefabs, `UnlockableSet`, the skill-tree panel (`AbilityUpgradePanelUI`), `RuntimeAbility` **(core, D-523's parked "requires unlock" field)**, `LucyPassiveAbility_PapasShelter` (generalized), small new passive components.
USPs: all four. Synergies and Duos become the tracks' content; Family Roles feed Toba's "One of Us"; Home is where Bond is earned.
Docs: GDD Family systems (BO-x, DU-x, SY-x), Progression (PR-8, PR-19), the five sheets (family nodes leave the personal trees), glossary (names), Demo Spec (Bond), `player-skill-trees.md`.

---

## 1. Direction

**A relationship has three moments, so a track has three knots.** Level 1 is who they already are, level 2 is what they learn together, level 3 is who they become. The knots reuse the Bond levels Bond Lite already saves (10 / 25 / 45 points, BO-1), so there is no new progression currency.

Principles:

1. **Content first from what exists.** The family already has 6 pair Synergies, 7 Duos and 7 Duo upgrade nodes. They fill most knots. New effects are only small twists on built ones.
2. **Lv 1 is open for people who already are family.** Pairs that start together start at Lv 1, so the first knot is the family as the player meets it. Toba, the newcomer, starts below Lv 1 with everyone, and earning his knots *is* his story.
3. **A knot always needs both.** It works only when both members are in the squad (as Duos already do, DU-3). This makes squad choice a relationship choice.
4. **Bond levels learn, Family skill points upgrade.** Reaching a level teaches its knot for free; FSP buy the upgrade pips. The relationship is the unlock; FSP is the family's investment.
5. **Using a pair grows a pair.** Any knot that fires counts as help between them (BO-2's help tally), so the loop closes in combat, not only at Home.

## 2. Name

| Option | On screen | For | Against |
| --- | --- | --- | --- |
| **Threads** (recommended) | Each pair: "Linda & Lucy's Thread". The overview of all of them: **the Tapestry**. A level step on a thread: a **knot** | A thread is a line, which is what the track is; two threads tied make a knot at each level; all threads together weave the family, which gives the whole-family view a name for free | A new word next to "Bond". Keep Bond as the level ("Linda & Lucy's Bond, Lv 2", the glossary's approved shape) and Thread as the track |
| Bonds | "Linda & Lucy's Bond" (track and level share the word) | No new word | "Bond tree" is not a tree; flat |
| Kinship | "Kinship: Linda & Lucy" | Warm, clear | Abstract, no metaphor to build the UI on |
| Hearthbonds | | Ties to the Hearth, the old project name | Long; reads like a currency |

Placeholder thread names per pair are in §5. All names go to `miso-narrative` (glossary owner).

## 3. Shape: a tree, or something better?

| Shape | What it is | Verdict |
| --- | --- | --- |
| Branching tree per pair | Choices inside each pair | No: 10 trees with branches is the scale problem THJ wants to avoid, and a pair's choices barely matter when the squad is 2 to 4 |
| **Straight line of 3 knots** (recommended) | Lv 1 → Lv 2 → Lv 3, upgrades as pips on a knot | Fits Bond's 3 levels exactly; one row of UI; 30 knots in all |
| Line with a fork at Lv 3 | Pick 1 of 2 at the last knot | Kept as an option for a pair that needs a choice (the sisters, §5 note) |
| Support matrix (Fire Emblem) | A half grid of 5 × 5 | Good debug view, poor player view: no sense of a family |
| **Web / Tapestry** (recommended for the overview) | Five portraits in a ring, ten threads between them; thread style shows level | The only shape that shows "the family as a whole" at a glance |

**Recommendation:** the *data* is a straight thread per pair; the *presentation* is a web of all threads (the Tapestry) plus a per-character list of that character's threads (§9).

## 4. Rules (proposed)

- **R1.** Each pair of fighting Bergsons has one Thread: 3 knots, one per Bond level (Lv 1 at 10, Lv 2 at 25, Lv 3 at 45; BO-1). Kevin has none (home-only, D-004).
- **R2.** Reaching a Bond level learns that level's knot at once, for good, at no cost. A Bond level is never lost (open for the full game: the Home demo relocks each moon, Home Q2).
- **R3.** A knot may have one upgrade line of 1 or 2 pips, bought with Family skill points in the Threads screen.
- **R4.** A knot works only while both members are in the squad. Exception: One of Us (§6).
- **R5.** Lv 1 holds who they already are: the pair's existing Synergy, plus their Pass-by (PB-4 already gates Pass-by at Lv 1). Lv 2 holds their Duo where one exists; a Duo stays hidden until then (D-523's lock). Lv 3 is a twist on their Lv 1 or Lv 2 skill, never a new mechanic.
- **R6.** Starting Bond: pairs that start the game together start at 10 (Lv 1); Linda & Lucy keep 15 (BO-1); Mark's pairs start at 10 when he joins; Toba's pairs start at 6 (Lv 0), as in the Demo Spec.
- **R7.** When a knot's effect fires between them, it counts as help for their Bond: 1 per event, at most 3 per pair per mission, paid at mission complete (BO-2's rule, widened from Rivalry, Duos and John's role to every knot).
- **R8.** Budget per pair, for every future fighter too: 3 knots, 1 upgrade line, ≤ 2 pips.

## 5. The ten threads

Status: **Built** (in `main`), **Planned** (decided, not built), **New·S** (small new effect, mostly reusing a built component), **New·D** (data only if the field exists).

| Pair · thread (placeholder) | Lv 1 · who they are | Lv 2 · what they learn | Lv 3 · who they become | Upgrade pips (FSP) |
| --- | --- | --- | --- | --- |
| **John & Linda** · *First Dance* | **Fetch:** John's Sword kill on her arrows sends them straight back to her quiver (LI-13). Built, today always on | **John-Linda Dance** (Duo). Built | **Steady Shoulder:** Linda next to John: +1 arrow range. New·S (Pair Aura, see §12) | Dance +1 movement, 2 pips. Built node |
| **John & Lucy** · *Papa's Ember* | **Papa's Shelter** and **Shield Flare**. Built, open today (the one Lv 1 with two skills: both are taught before M4) | **Hide and Seek** (Duo). Built | **Long Shelter:** Papa's Shelter works within 2 cells of John (his role reach), not only next to him. New·D/S | Hide and Seek +1 decoy, 2 pips. Built node |
| **John & Mark** · *Shield and Fist* | **Command Shield Dash.** Built (L2 on `thj/home-test`, D-010) | **Family Watchers** (Duo). Built | **Settle the Debt:** Mark deals ×1.3 to the enemy carrying John's Blood Debt (JO-2), as John does. New·S (reads the built mark) | Watchers +1 radius, 2 pips. Built node |
| **John & Toba** · *Open Door* | Pass-by + **Kin Healing:** Toba's heals on John ×1.25. Pass-by built (PB-4); Kin Healing is TO-2, planned | **Shared Shield:** John's Shield Up also covers Toba while Toba stands next to him (60% damage taken until John's next turn). New·S | **Kin Healing ×1.5** · counts toward One of Us | — |
| **Linda & Lucy** · *Still Counting* | **Tempest Bloom.** Built; open from the start because the sisters start at Lv 1, which is D-519's "Bloom open" | **Marks-Sisters** (Duo). Built; hidden until Lv 2 needs D-523's lock. First used in M4 after the Yard (D-470) | **Sisters' Rivalry** (Bond Lite version: +1 AP, once per turn per sister). Built | Marks-Sisters damage, 2 pips. Built node (D-521's "second node" becomes these pips) |
| **Linda & Mark** · *Catch!* | **Catch & Return.** Built (today 1 FSP) | **Family Footrace** (Duo). Built (Arrow Chase on hold) | **Return to Sender:** once per turn, a catch refunds Linda's shot (+1 AP). Planned (D-228) | Head Start, 1 pip. Built node |
| **Linda & Toba** · *Healing Song* (showcase) | Pass-by + Kin Healing + Toba's kill hand-back of her arrows (LI-13, built) | **Healing Marks** (Duo). Built; Bond L2 already (D-010) | **Kin Healing ×1.5** · counts toward One of Us | Healing Marks heal, 2 pips. Built node |
| **Lucy & Mark** · *Sparks and Stillness* | **Spark of Focus:** when Lucy's role embers hit an enemy within 2 cells of Mark, he gains 1 Focus (once a round). New·S | **Chained Assault** (Duo). Built | **Chain Reaction:** Chained Assault reaches a 4th target. New·D if the target count is a field | Chained Assault damage, 2 pips. Built node |
| **Lucy & Toba** · *Kindling* | Pass-by + Kin Healing | **Kindling:** when Toba heals Lucy, her next Fire Embers gets one more sidewinder (Papa's Shelter's level bump, for one attack). New·S | **Kin Healing ×1.5** · counts toward One of Us | — |
| **Mark & Toba** · *Tea and Quiet* | Pass-by + Kin Healing | **Still Water:** Toba's heals on Mark add 1 Focus. New·S | **Kin Healing ×1.5** · counts toward One of Us | — |

**Sisters note.** D-520 put the Duo and Rivalry together at Lv 2, with FSP choosing between them. This design moves Rivalry to Lv 3: it played as overpowered (vision, playtests), and the sisters' arc goes from counting kills to standing back to back ("Still counting?" / "…No."), so the Duo is the turning point and Rivalry, the AP gift between them, is what their competition becomes. If THJ wants D-520's choice kept, the sisters' Lv 2 is the one fork: pick one, the other arrives at Lv 3.

**Toba's four threads share one template** (Lv 1 Pass-by + Kin Healing, Lv 2 one pair twist, Lv 3 Kin Healing ×1.5), so one heal component and four small twists cover them. Kin Healing stays inside D-202 ("combat reads no Bond"): combat reads the learned knot, not the Bond score.

Count: 30 knots. Built: 15 (6 Lv 1, 7 Duos, Rivalry, Toba's hand-back). Planned: Kin Healing (one component, 8 knots), Return to Sender. New small: 8 (Steady Shoulder, Long Shelter, Settle the Debt, Spark of Focus, Chain Reaction, Shared Shield, Kindling, Still Water). Upgrade pips: 13, all existing family nodes.

## 6. About the pair, and the family as a whole

The pair:

- **Every knot names both and needs both** (R4). No knot buffs one of them alone.
- **Each level is a moment.** A Bond level-up plays the Demo Spec's beat (a Bond scene for the showcase pair, a Dining Table line for the others) and the line names the knot: "Linda & Lucy's Bond reached Lv 2. They learned Marks-Sisters." The Yard (BO-3) is already this moment for the sisters.
- **The knots act out the relationship:** John carries Linda's arrows back and dances with her; he shelters Lucy; Mark settles his father's debts; the sisters stop counting; Toba is healed, sheltered and shown in, one family member at a time.

The family:

- **The Tapestry is the family portrait.** All ten threads in one picture; a thick weave means a close family, a faint thread is a relationship the player has neglected. It is the only screen that shows the whole family at once.
- **One of Us (Toba becomes family).** When Toba reaches Bond Lv 2 with 3 of his 4 family partners, he becomes family: he gives and takes Revenge (RV-1), and gains his Family Role (FR-7, D-224, design still open). This is the strongest "family as a whole" beat the system can give, and it finally gives FR-7 its trigger. A scene plays at the next Dawn or Dusk.
- **Squad screen.** Before a sortie the squad panel lists the knots the chosen squad brings ("This squad: Tempest Bloom, Papa's Shelter, Shield Flare, Catch & Return"). Choosing who goes becomes choosing which relationships go.
- **Later, not now:** a family gift at a total of Bond levels across all pairs (the hidden family level, PR-9, deferred by D-221), and Trios as triangles of the Tapestry where all three threads are at Lv 2 or more (D-215, deferred). The Tapestry has room for both without a new screen.

## 7. What happens to the Family tree

It becomes the Threads. Every node it holds today is already a pair node:

| Family node today | Sits on | Becomes |
| --- | --- | --- |
| Tempest Bloom (unlock, 1 FSP) | Lucy | Linda & Lucy Lv 1 (free) |
| Marks-Sisters (2 pips) | Lucy | Linda & Lucy Lv 2 pips |
| Sister's Rivalry (Bond Lite, 1 FSP) | Lucy | Linda & Lucy Lv 3 (free) |
| John-Linda Dance (2 pips) | John | John & Linda Lv 2 pips |
| Hide and Seek (2 pips) | John | John & Lucy Lv 2 pips |
| Chained Assault (2 pips) | Mark | Lucy & Mark Lv 2 pips |
| Family Watchers (2 pips) | Mark | John & Mark Lv 2 pips |
| Head Start (1 pip) | Mark | Linda & Mark Lv 2 pip |
| Catch & Return (unlock, 1 FSP) | Mark | Linda & Mark Lv 1 (free) |
| Healing Marks (2 pips) | Toba | Linda & Toba Lv 2 pips |
| Trio group (placeholder) | — | Tapestry triangles, later (D-215) |

The Family tab of the skill-tree page becomes the Tapestry. FSP keep their name and source (PR-8: a character's 2nd, 3rd and 5th SP spent; the Yard's story grant) and buy pips only.

**Economy flag.** Supply is 15 FSP (16 with the Yard); demand becomes 13 pips, so a full family maxes everything. Either accept that (Bond levels are the scarce part: time at Home) or lower the grant to 2 FSP per character (10) so pips are a choice. Recommendation: 10, decided after a playtest.

## 8. What happens to the personal trees

They stay as they are (6 nodes, 8 pips, unlocks at 0/0/2/2/3/5, D-222), minus the family nodes parked on them (John's 2, Lucy's 2 or 3, Mark's 4, Toba's 1), which move to the Threads. Personal = "me", Threads = "us".

- The slot-D family auras (Of the Same Blood, Kindled Spirits, Move as One, Flowing Guard) stay personal: each is one person's gift to everyone, not a pair's.
- Personal growth still feeds the family: FSP keep coming from SP spent (PR-8).
- Family Role upgrades (John's ×0.5 → 0.4 → 0.3, D-217) belong on the personal tree when built; a role is one person's.

## 9. The menu

Two views, both at the Grandma Table's skill-tree page. "Select one character and switch the other" is the right instinct; this makes it a list so the switch is one press.

**A. A character's Threads tab** (next to their Skills tab). The selected character is the anchor; their 4 threads are 4 rows, 3 knots each. Every pair the anchor has is on one screen; nothing to scroll.

```
 [John] [Linda] [Lucy] [Mark] [Toba]           ← same character tabs as today (anchor)
 ┌ Lucy ─────────────── Skills | THREADS ────────────────────────────┐
 │                         Lv 1            Lv 2            Lv 3       │
 │ (Linda)  Bond Lv 2   [◆ Bloom]──────[◆ Marks-Sis ●●○]──[◇ Rivalry]  │
 │ (John)   Bond Lv 1   [◆ Shelter·Flare]─[◇ Hide&Seek ○○]─[◇ Long Sh.] │
 │ (Mark)   Bond Lv 1   [◆ Spark]──────[◇ Chained ○○]────[◇ Chain R.]  │
 │ (Toba)   Bond Lv 0   [◇ Kin Heal]───[◇ Kindling]──────[◇ Kin H. II] │
 ├────────────────────────────────────────────────────────────────────┤
 │ Marks-Sisters · Linda & Lucy's Bond, Lv 2 · Learned                 │
 │ A fire arrow along a line: 12 × damage to every enemy.              │
 │ Upgrade 1/2: ×1.2 → ×1.35 · costs 1 Family skill point   [Upgrade]  │
 └────────────────────────────────────────────────────────────────────┘
   ◆ learned  ◇ opens at that level  ● pip bought  ○ pip open
```

Inputs: the existing character keys switch the anchor; Up/Down picks the partner row; Left/Right picks the knot. Rows sort by Bond level, highest first, so the relationships that matter now sit on top. A "can upgrade" glint marks knots with an affordable pip.

**B. The Tapestry** (the old Family tab). Five portraits in a ring; ten threads between them. Thread style shows the level (faint dashed Lv 0, one strand Lv 1, two strands Lv 2, braided Lv 3); a glint marks a thread with a new knot or an affordable pip. Hovering a portrait lights its 4 threads and dims the rest. Clicking a thread opens view A with that pair's row selected. It answers "which relationships have I neglected?" in one look.

**Why it scales:** with 7 fighters, view A is 6 rows (still one screen) and the Tapestry has 21 threads, kept readable by hover-to-focus. The squad panel (§6) is the third, smallest view.

## 10. The demo

**The onboarding demo (Hearth → M4 send-off, on `main`):** John, Linda, Lucy and Mark fight; Toba joins after M4. So 6 threads show; Toba's portrait is a silhouette in the Tapestry, his threads hidden (a promise).

| Thread | Level in the demo | Shown |
| --- | --- | --- |
| Linda & Lucy | Lv 1 at start → **Lv 2 at the Yard** (built scene) | Bloom learned; Marks-Sisters learned at the Yard and first used in M4 (D-470); the Yard's FSP buys its first pip; Rivalry locked: "Opens with Linda & Lucy's Bond, Lv 3" |
| John & Lucy | Lv 1 | Papa's Shelter, Shield Flare (both taught before M4) |
| John & Mark | Lv 1 | Command Shield Dash |
| Linda & Mark | Lv 1 | Catch & Return (taught before M4) |
| John & Linda | Lv 1 | Fetch (the built hand-back) |
| Lucy & Mark | Lv 1 | Spark of Focus, or Pass-by only if it isn't built for the demo |

**Cap: Lv 2, sisters only.** Every Lv 2 and Lv 3 knot is visible but locked, with its name: that is what shows the system's depth without building it. This matches the after-Hearth design's "Duos locked until M4" and "the sisters' first Duo is the first Duo".

**The Home demo (`thj/home-test`, 7 days, 5 fighters):** all 10 threads; Linda & Toba reach Lv 2 (Healing Marks, D-010) and one or two more with a focused week; Lv 3 (45 points) isn't reachable in a week, so it stays a teaser there too. Same cap.

**Demo build cost:** chunks C1 to C3 below, plus Spark of Focus if wanted. No Lv 3 effect needs building for the demo.

## 11. Scale check

| Fighters | Pairs | Knots | Pips (max) |
| --- | --- | --- | --- |
| 5 (now) | 10 | 30 | 20 (13 used) |
| 6 | 15 | 45 | 30 |
| 7 | 21 | 63 | 42 |

What keeps it manageable as it grows: R8's budget; Lv 1 is always existing content plus Pass-by; a newcomer's threads share one template (as Toba's do); view A grows by one row per fighter.

## 12. Build outline (for the TD; a tech plan follows approval)

| Chunk | What | Core? | Demo |
| --- | --- | --- | --- |
| C1 | Thread data: one asset per pair (two unit ids, 3 knots each pointing at an unlockable or a skill-tree node with its level). Generalize `HomeLockRules` / `BondNodeGate` from the sisters to every pair; free learn on level-up through the existing unlock path (PR-19); `BondSettings` start values (R6) | No | Yes |
| C2 | Duo lock: D-523's "requires unlock" field on `RuntimeAbility` (approved, parked by D-524) | **Yes**, own commit, THJ's OK | Yes |
| C3 | Threads tab + Tapestry, replacing the Family tab in `AbilityUpgradePanelUI`; move the family nodes off the personal trees' data | No | Yes |
| C4 | Pair Aura: generalize `LucyPassiveAbility_PapasShelter` (partner, radius, stat or level bump) → Steady Shoulder, Long Shelter, Kindling | No | No |
| C5 | Kin Healing (one component on Toba, per-partner factor read from learned knots); Spark of Focus, Still Water (Focus add), Settle the Debt (reads Blood Debt), Shared Shield, Chain Reaction; Return to Sender (D-228) | No | Spark only, optional |
| C6 | One of Us: Toba's Revenge flags on; his Family Role when designed (FR-7) | No | No |
| C7 | Help tally: any knot firing counts as help (`BondSources`, R7) | No | Optional |

## 13. Conflicts with past decisions

| Decision | This design | Needs |
| --- | --- | --- |
| D-519 Bloom open | Lv 1 for a pair that starts at Lv 1: open in practice | Nothing |
| D-520 Duo and Rivalry both at Lv 2, FSP picks | Duo Lv 2, Rivalry Lv 3, both free | THJ (Q3) |
| D-521 Marks-Sisters as a second node | Becomes the Duo knot's pips | Nothing |
| D-523 / D-524 Duo lock parked | Needed by C2 | Unpark |
| D-010 Command Shield Dash at L2 (`thj/home-test`) | Lv 1 | THJ |
| BO-1 start values (only the sisters above 0) | Every starting pair at 10; Toba's at 6 | THJ |
| D-231 no Bond meter | Levels shown (knots, thread style), never points | Confirm |
| D-202 combat reads no Bond | Kept: combat reads learned knots | Nothing |
| PR-8 FSP 15 vs 13 pips | Everything maxes | THJ (Q4) |
| PR-19 Bloom and Catch & Return cost 1 FSP | Free at their level | THJ (Q2) |

## 14. Questions for THJ

1. **Name:** Threads / Tapestry / knots (recommended), plain Bonds, or Kinship?
2. **Cost:** knots free on reaching the Bond level, FSP for pips only (recommended), or Bond Lite's model (the level opens a knot, 1 FSP learns it)?
3. **Sisters:** Rivalry at Lv 3 (recommended), or keep D-520 as the one fork at Lv 2?
4. **FSP supply:** keep 15 (everything maxes at the end) or lower to 10 (pips become choices)? Recommended: decide at the playtest, lean 10.
5. **One of Us:** Toba becomes family at Lv 2 with 3 of 4 (recommended), all 4, or a fixed story beat?
6. **Demo cap:** Lv 2 for the sisters only, everything else visible and locked (recommended)?
7. **John & Lucy's Lv 1** holds two Synergies (both taught before M4). Accept the one exception, or move Shield Flare to Lv 3 and change the onboarding?

## Risks

- **Gating built content breaks the onboarding.** Handled by R6 (starting pairs at Lv 1) and by keeping everything taught before M4 on Lv 1; check every `LevelAbilityLock` and Hearth memory kit against the knot list in C1.
- **Steady Shoulder stretches Watch.** Linda's role zone is her arrow range, so +1 range also widens Watch (6 → 7 with Longshot). Cap at 6 or accept; check in play.
- **Rivalry at Lv 3 is late for players who liked it.** Its AP gift is the strongest pair effect; moving it later is deliberate (vision: "played as overpowered").
- **Mark joins mid-campaign; Toba later.** `BondStore` needs entries created at join (start values from R6), not at new game.
- **Two words (Bond, Thread).** Mitigated by one fixed line shape: "Linda & Lucy's Bond, Lv 2" on every knot card.

## Gates

Design review by THJ (this plan). Then a tech plan (`miso-tech-plan`) for C1 to C3; compile / EditMode (known red only) / review for code / THJ play check of the Threads screen and the Yard → M4 flow. Docs after approval: GDD Family systems and Progression, the five sheets, glossary, Demo Spec, `player-skill-trees.md`.
