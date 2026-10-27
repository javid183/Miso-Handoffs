# Linda at a distance: rewarding the far game and the fetch

Size: L    Tier: 3 (Family Roles, Synergies, Duos; touches a built Duo in a core script)    Assigned to: game designer
Branch: all (prototype on `thj/linda-quiver`, after C4 of the [quiver tech plan](2026-10-26-linda-quiver-tech.md))
Status: waiting on THJ

## Why

THJ's play check of the quiver prototype (C1–C3, 2026-10-27): the family packs around John, so arrows land where nobody is, walking pickup is rare and Recall becomes the normal way back. The walk-and-hand-back is the best moment and it happens too rarely. Linda has nothing that rewards playing apart. The Mark–Linda Duo pulls the pair together, against their own Synergy, while THJ wants them "distant but synced".

## Goal

Find the smallest prototype step that makes distance pay off (Linda standing apart, family walking out to her arrows) without raising Linda's damage share, and set the direction for a distant-but-synced Mark–Linda Duo.

## Problem and evidence

THJ's four observations are symptoms. Below them are four causes (V = verified in data or code, A = assumed):

- **R1. Everything good happens up close; nothing rewards spreading out.** John relays hits on allies within 2 cells, and since D-120 he takes area hits once for everyone covered. Papa's Shelter needs Lucy next to John. Mark's Counter reaches 2 cells. Lucy's follow-up reaches 3 cells. Pass-by gives +2 FTP for meeting (CR-11). The Footrace ends with the pair next to each other (V: family-systems.md FR table, Synergies, CR-11). The one thing that usually punishes clumping, area attacks, is cancelled by the area relay. So the best formation is already solved: ball up around John. **This goes beyond Linda.** It flattens positioning for the whole family (a later formation review, Q5).
- **R2. Recall always beats walking on AP.** Every move costs 1 AP (CR-6). Walking out costs 1 AP per stack and leaves John's cover. Recall costs 1 AP for every stack, safely (LI-8). Walking only wins when the move was happening anyway (V: rules).
- **R3. Linda's kit has no distance payoff.** Watch is lane-based, range 4. Pierce rewards lining enemies up, not standing apart (V: linda.md).
- **R4. The Footrace's shape works against Catch & Return.** The loser stops on `path[^2]`, one cell short of the winner, so they always end adjacent. Catch needs 2 or more cells in line (`minTileDistance` 2) (V: `UnitsCooperationHandler.Mark_Linda_LoserStop`, `ProjectileCatchAndReturn`).
- **Unknown (A):** whether the enemy AI picks out isolated units. `UtilityVariables` has ally and enemy presence terms, but I didn't read the evaluator assets. If it doesn't, standing apart costs Linda only John's cover.

## Options compared

| Option | Player experience | Rules complexity | Implementation cost | Risk | USP effect |
| --- | --- | --- | --- | --- | --- |
| 0. Do nothing | Recall stays the default; the hand-back stays rare | None | None | The quiver's best moment fades | Neutral |
| a. **Lookout** (Linda): at the end of the family turn, if no Bergson is within 2 cells of her, Watch reaches +1 cell until the next player turn | She takes a post; her lanes grow | Low: one condition, read once | Low–medium: a non-core component adds a `Stat_RANGE` modifier; preview work | Lonely-sniper feel; more Watch triggers (bounded by the quiver) | Family Roles + |
| a2. "Big Sister's Eye" (creative critic): Watch also answers enemies that close in on a Bergson fetching her arrows | She stays back to guard whoever walks out: distance as trust | Medium | Medium–high: changes `LindaFactionRoleHandler` (on the core list) and needs non-lane shots | Off-lane shots break the bow's shape | Family Roles ++ |
| b. **Fetch**: a walking pickup gives +1 FTP (once per Bergson per turn, family cap +2 per round; none for G3 instant pickups) | Walking out pays the family; balances pass-by's "meet" with a "fetch" | Low | Low: `GUnit.ProduceFTP` is public (V), called from the quiver's pickup | FTP pays for Watch (D-246): fetching becomes more Linda shots | Duos + (FTP), Synergies + |
| b2. Mark the runner: he also picks up arrows next to his path | Mark is the one who fetches | Low | Low (pickup field, non-core) | Fewer arrows left for the others to walk to | Synergies + |
| R2-lever. Recall cooldown 2 → 3 | Recall is the backup, not the habit | None | Data, one value | Linda runs dry more often (wanted, up to a point) | Neutral |
| c. **Long Pass** replaces the Footrace (Duo, below) | Two siblings far apart playing catch across the board | Medium | Medium–high: a new Duo in `UnitsCooperationHandler` (core); shares the D-257 catch QTE | Damage share if it gets a multiplier (dropped, see Critics) | Duos ++, Synergies + |
| c2. "Fetch Race": the Footrace targets a grounded stack; the winner throws it to Linda; they end apart | A sprint for the arrows | Medium | Medium (same core handler) | Only works when arrows are down | Duos + |
| d. John: relay radius 2 → 1 (data, held 1–2) | Less safety at the core; spreading costs less | None | Data | Retunes a built, play-tested role (D-119 to D-129); hits every fight | Family Roles − for John |
| e. **Cues**: a hand-back variant per sibling; a call-out bark that grows with distance; a glint on stacks someone can reach this turn | The fetch is seen and heard | Low | Low–medium: tweens and lines (narrative) | Glint misread as loot | Family Roles / feel + |

## Proposed rules (IDs proposed: the next free LI numbers)

- **LI-13. Lookout.** When the family ends its turn, if no other Bergson stands within 2 cells (radial, the same reach as John's zone) of Linda, she has Lookout until the next player turn: Watch lanes +1 (range 4 → 5; 6 → 7 with Longshot). It is checked **once**: pushes and Commands during the enemy phase don't switch it off (UX critic). Her bow and Crescendo are unchanged, so moving her with the Dance before a shot gains nothing (systems critic). No damage bonus.
- **LI-14. Fetch.** A Bergson whose own move picks up arrows (LI-7) gives the family +1 FTP. At most once per Bergson per turn, at most +2 per round for the family. Instant pickups (G3: an arrow landing on a Bergson's tile) and Mark's catch give no FTP. Linda fetching her own arrows counts.
- **LI-8 (amended). Recall cooldown 3** (was 2). Everything else is unchanged.
- **Cues.** One hand-back variant per picker (tween shape + line; the lines are placeholders for `miso-narrative`). John: an underhand lob, "Yours, I believe." Lucy: the arrow flicked over with a spark. Mark: a spinning throw Linda catches one-handed (a hint at the catch). Toba: handed over in a leaf. Linda herself: a quiet "One more." When the picker is 4 or more cells from Linda, the line becomes a call across the field ("Linda! Catch!"). A soft glint at the start of the player turn, only on stacks some Bergson can reach this turn.
- **Mark–Linda Duo: Long Pass** (name for narrative/THJ). It replaces the Family Footrace. The pair must share a row or column, at least 2 apart. Activated by either partner, 0 AP + 2 FTP + 1 arrow. **One target step** (UX critic): the player picks a target cell on one of Mark's lanes, within Linda's bow range of Mark. Linda's arrow flies to Mark, piercing as normal on the way. Mark's catch QTE (D-257): **pressed**, Mark sends it down the chosen lane as a bow shot (6 × damage, pierce, no multiplier), then it goes back into her quiver. **Missed**, it flies on past Mark as a normal shot and lands (LI-6). Both outcomes are previewed: the pressed path solid, the missed path ghosted. The arrow's leg is meant to end at Mark, so the D-257 timing problem (the arrow flying past during the QTE) may not arise here. The tech spike confirms.

## Lens notes

- **Creative.** The target experience: Linda holds a far post, the family's eyes at the edge, and someone leaves John's shelter to run her an arrow; the call across the field and her catch are the warmth set against the dread of standing apart. The moment designed for: Mark three lanes away and Linda on a ridge, an arrow passing between them on a press, nobody moving. John holds the centre and Linda watches the edge: two protectors, not one. "Limited ammo, walk over it" is the genre default (quiver plan). The family carrying arrows to her is the original part, so the rewards go to whoever walks out.
- **Systems.** The levers are the Lookout radius (2) and bonus (+1), the Fetch amount and caps (+1, 1 per Bergson, +2 per family), and the Recall cooldown (3). Interactions:
  - Watch still costs 1 FTP (D-246), and Fetch feeds FTP, so the family cap stops Fetch from paying for unlimited Watch.
  - Lookout adds triggers, but the quiver bounds them.
  - Sisters' Rivalry and Tempest Bloom are untouched.
  - The Dance pickup counts for Fetch (a forced move is still a walk).
  - Failure cases: Linda dies at her post (watch her HP and deaths); FTP piles up (DU-5 says fights end above 4); a Bergson parks at the end of her range and catches every miss for free (G3 gives no Fetch, but that hole in the quiver exists today: watch the share of instant pickups).
- **UX.**
  - **Seen when:** while any Bergson's move is previewed, Linda's Lookout lanes draw dashed out to the +1 cell, even though FR-10 and FR-11 would hide her zone (it equals her attack reach), plus an eye mark over her.
  - **Previews:** if a ghost tile enters her 2-cell radius, the lanes flash and "Lookout lost" shows over Linda. On End Turn, the state locks and the eye stays until the player phase.
  - **Fetch** shows on the FTP bar as a pulsing pip during the move preview (the FTP icon, never a second "+1" next to "+N arrows"). It is greyed when that Bergson has used Fetch or the family cap is reached.
  - **Likeliest misread:** "she didn't shoot at 5". Hence the locked state and the eye.

## USP check

- **Family Roles:** strengthens. Watch gains a positional choice; John covers the core, Linda the edge.
- **Synergies:** strengthens. The fetch becomes a reason to cross the board; Long Pass gives Catch & Return its natural setup.
- **Duos:** strengthens. Mark–Linda stops working against its own Synergy; Fetch feeds Duo FTP.
- **Home:** neutral on purpose. A later workshop item could widen the Lookout radius or the call-out range.

## Critics

Three critics ran in parallel on 2026-10-27, each blind to the others. `miso-design-critic` wasn't available in this session, so read-only Explore agents ran with critic briefs (one lens each).

| Lens | Strongest point | What I did with it |
| --- | --- | --- |
| Systems | The leaning didn't touch R2: Recall still wins the AP sums, and Lookout sends arrows further out. Fetch can be farmed (a Bergson parked at the end of range), turns into more Watch through FTP, and Long Pass with ×1.5 raises her share | **Accepted.** Recall cooldown 3 joins the step; no Fetch for instant pickups; family cap +2 per round; Long Pass has no multiplier; Lookout applies to Watch only. Their falsifiers are the playtest signals |
| Creative | Lookout pays her for having nobody near: a lone sniper, against warmth, against John. +1 range and +1 FTP are bookkeeping. Reward the walker; make the long throw the moment; Long Pass is a genre bounce unless it is Mark's palm deflect and an exchange of lines | **Partly accepted.** The walker's reward and the call-out across the field are in; Long Pass gets Mark's catch animation and a sibling exchange. "Big Sister's Eye" goes in as a2, not this step (it touches a core-listed handler and needs off-lane shots). Not accepted: dropping Lookout. THJ asked for distance; framing it as a post that guards the edge, with the family coming to her, keeps it warm |
| UX | Lookout is invisible: FR-10/FR-11 hide her zone, the +1 is a single extra tile, and another unit's move can break it with no sign. Long Pass is three decisions plus a QTE | **Accepted.** Dashed Lookout lanes and the eye; "Lookout lost" on ghost previews; the state locked at End Turn; one-step Long Pass targeting with both outcomes previewed; the glint only on reachable stacks |

Rejected: the creative critic's "Recall only pulls arrows with no Bergson within 3". It makes the near hand-backs happen, not the far ones. It is kept as a lever if cooldown 3 fails. "Cut the Footrace now as Fetch Race" is option c2 in Q4.

## Recommendation

**Step D1, "distance pass" (after C4; non-core; every lever a toggle on one config asset so THJ can switch each off in play):**

1. LI-13 Lookout (radius 2, +1 Watch range, locked at End Turn) with its preview: dashed lanes, eye, "Lookout lost".
2. LI-14 Fetch (+1 FTP, 1 per Bergson per turn, +2 per family per round, none for instant pickups), shown on the FTP bar.
3. Recall cooldown 3 (data).
4. Cues: hand-back variants per picker, the call-out at 4 or more cells, the reachable-stack glint.
5. Log lines (with C5): pickup kind (walk / instant / catch / Recall) and the picker's distance to Linda; Lookout on or off at End Turn; Linda's distance to her nearest sibling at End Turn; Fetch FTP.

**Step D2 (after the D-257 spike):** Long Pass replaces the Footrace (Q4), plus b2 Mark the runner if D1 shows Mark rarely fetches. John stays as built (Q5).

**Playtest signals** (M4 and M6 with a full squad; compare against the C4 build):
- Walking pickups ≥ 30% of arrow returns (under 30% falsifies D1).
- Recall at most once per level.
- Linda's average distance to her nearest sibling at End Turn up ≥ 1 cell.
- Lookout on at ≥ 40% of End Turns.
- Linda's damage share ≤ 65% and not above the C4 build.
- No Linda death attributable to Lookout in 3 or more levels.
- FTP at fight end not above C4 + 2.
- Instant pickups under 15% of returns.
- THJ and testers name the hand-backs and call-outs unprompted.
- Cold players can say why Watch reached 5 tiles.

## Questions for THJ

1. **Reward Linda's distance itself?** *Context:* THJ asked for a distant game. The creative critic warns a "be alone" reward feels lonely. *Options:* (a) Lookout as above; (b) "Big Sister's Eye" (her Watch guards fetchers; core handler, later); (c) only reward the fetchers. *Recommendation:* (a) now, (b) as a later node. *Blocks:* D1 item 1.
2. **Fetch pays FTP?** *Context:* walking out costs AP and cover; pass-by pays +2 for meeting. *Options:* (a) +1 FTP, capped as above; (b) cues only, no reward. *Recommendation:* (a). *Blocks:* D1 item 2.
3. **Recall cooldown 3 in the same test?** *Context:* Recall beats walking on AP (R2); without a change, the test can't tell whether the rewards work. *Options:* (a) cooldown 3; (b) keep 2; (c) recalled arrows arrive at the start of the next turn (code). *Recommendation:* (a), as a toggle. *Blocks:* D1 item 3.
4. **Mark–Linda Duo?** *Context:* the Footrace ends the pair adjacent (R4); you want distant-but-synced with D-257's QTE catch. *Options:* (a) Long Pass replaces the Footrace; (b) Fetch Race; (c) keep the Footrace, with the loser stopping 2 or more cells away in line; (d) keep as is. *Recommendation:* (a), planned after the D-257 spike. It is a new Duo in `UnitsCooperationHandler` (core). *Blocks:* D2 and the D-257 spike's scope.
5. **John's pull?** *Context:* R1 is family-wide; the area relay (D-120) removes the main cost of clumping. *Options:* (a) leave John as built, and open a separate formation review covering every proximity reward; (b) test relay radius 1 now. *Recommendation:* (a). Change one thing at a time, and John's numbers are play-tested. *Blocks:* nothing in D1.

## Docs to update if approved

- [`characters/linda.md`](../design/gdd/characters/linda.md): LI-13, LI-14, LI-8 cooldown (*Planned* until played).
- [`family-systems.md`](../design/gdd/family-systems.md): the Duos table, Mark–Linda row (Long Pass, if Q4 (a)); a Catch & Return note; a CR-11 cross-link for Fetch.
- [`combat-rules.md`](../design/gdd/combat-rules.md): CR-11 (Fetch as an FTP source).
- [`characters/mark.md`](../design/gdd/characters/mark.md): Head Start node (Footrace) → a Long Pass node; MA-3 note.
- `glossary.md` (Lookout, Fetch, Long Pass; `miso-narrative`).
- The quiver tech plan (D1 and D2 chunks), `decisions.md`, `status.md` (coordinator).
