# Linda at a distance: rewarding the far game and the fetch

Size: L    Tier: 3 (Family Roles, Synergies, Duos; a built Duo in a core script)    Assigned to: game designer
Branch: all (prototype on `thj/linda-quiver`, after C4 of the [quiver tech plan](2026-10-26-linda-quiver-tech.md))
Status: rev 2, waiting on THJ (rev 1 answered 2026-10-27: D-263 to D-265)

## Why

THJ's play check of the quiver prototype (C1–C3, 2026-10-27):
- The family packs around John, so arrows land where nobody is.
- Walking pickup is rare, and Encore (Recall's on-screen name, D-262) is the normal way back.
- The walk and the hand-back are the best moment, and they happen too rarely.
- Nothing rewards Linda for playing apart.
- The Mark–Linda Duo pulls the pair together, against their own Synergy. THJ wants them "distant but synced".

## Goal

Find the smallest prototype step that makes distance pay off (Linda apart, the family walking out to her arrows) without undoing the quiver's cut to her damage share, and design a distant-but-synced Mark–Linda Duo.

## Rev 2 changes (THJ, 2026-10-27)

- Lookout's +1 range is out. THJ: her Watch already covers most of the board; damage from far away is easier to understand. Below: a **Far Watch** comparison, **Big Sister's Eye** described concretely, and a **fetcher reward** comparison.
- Fetch's +1 FTP becomes a **skill-node upgrade** (D-264). Base fetching gets cues only, unless a fetcher reward replaces them.
- Encore cooldown 3 in the test, as a toggle (D-263).
- No Long Pass (D-265). **Fetch Race** is detailed below, with two alternatives. The Duo stays distinct from Mark's QTE catch, approved as its own step C3b (D-260, D-261).
- John's question (Q5 in rev 1) stays open.

## Problem and evidence

V = verified in data or code; A = assumed.

- **R1. Everything good happens up close.** John's relay (2 cells, area hits once since D-120), Papa's Shelter, Mark's Counter (2), Lucy's follow-up (3), Pass-by's +2 FTP for meeting (CR-11), and the Footrace all pay for standing together. Nothing pays for spreading out, and the area relay cancels the usual cost of clumping (V: family-systems.md). This is family-wide (Q5).
- **R2. Encore beats walking on AP.** One AP brings back every stack, safely. Walking costs 1 AP per stack and means leaving John's cover (CR-6, LI-8) (V). Answered for the test by D-263.
- **R3. Linda's kit has no distance payoff.** Watch is lanes of range 4; pierce rewards lining enemies up (V).
- **R4. The Footrace ends the pair adjacent.** The loser stops on `path[^2]`, but Catch & Return needs 2 or more cells (V: `UnitsCooperationHandler.Mark_Linda_LoserStop`, `ProjectileCatchAndReturn.minTileDistance`).
- **A.** Whether the enemy AI hunts isolated units is unread: `UtilityVariables` has presence terms, and I didn't read the evaluator assets. This sets the real cost of standing apart.

## Q1 study: rewarding Linda's distance with Watch damage

**What distance is measured.**

| Measure | What it rewards | Interaction with pierce (×0.6 per next enemy) | Read | Verdict |
| --- | --- | --- | --- | --- |
| From the target (Linda → enemy) | Long shots. Her lanes already reach 4, so most Watch shots are 2–4 cells | Per target, later enemies are farther, so the bonus offsets falloff and the 7/4/3 lines get stronger. Limiting it to the first enemy hit avoids that | Hard: the number depends on where the enemy stops | Rewards the wrong thing (targets far away, not Linda apart) |
| **From the nearest sibling (Linda → any Bergson)** | Linda standing apart: THJ's goal | One multiplier for the whole shot; falloff unchanged | Easy: one state on Linda, seen on her ghost tile | **Recommended** |

**Steps.** One step reads best: **Far** = no Bergson within 2 cells of Linda (radial, the same reach as John's zone, so "outside Papa's cover"). A second step (≥ 4 cells: ×1.75) would add a number to track and little play.

**Locked at End Turn.** The state is set when the family ends its turn and holds until the next player turn, so pushes and Commands in the enemy phase never flip it (UX critic, rev 1). Watch is the only arrow she fires in that window, so the bonus is Watch-only by construction. In code it can be a duration `Stat_DMG` modifier, the same pattern as the Footrace's bonus (V: `Mark_Linda_ApplyBonus`).

**The damage share, honestly.** Any Watch damage-up raises Linda's share: the very thing the quiver was meant to cut (46–72%). The quiver bounds the number of shots, not their size. Two ways to run it:
- **Additive:** Watch 6× near, ×1.5 when Far = 9×. Her share can only go up. It needs the quiver to bind hard.
- **Trade (recommended):** Watch base 6× → 5× near, ×1.5 when Far = 7.5×. In today's clumped play her share **drops** about 17%; she earns back more than today only by standing apart. Distance becomes a real trade: John's cover for more damage.

**Preview.**
- Linda's ghost tile shows a **Far** mark (her bow-eye icon) when the tile qualifies.
- Another Bergson's ghost entering her 2-cell radius flashes "Far lost" over Linda.
- After End Turn, the mark stays on Linda through the enemy phase.
- The Watch prompt reads "Arrows 3 → 2 · Far ×1.5".
- Damage numbers and the hover preview include the multiplier (CR-17 rule: what a preview promises, the action does).

## Q1 study: Big Sister's Eye, concretely

**What it does.** When a Bergson picks up Linda's arrows by walking, they are **under Linda's eye** until the next player turn. If an enemy ends its move next to them, or starts an attack on them, Linda's Watch triggers on that enemy even outside her lanes, if it is within her range (radial). The shot flies straight to the enemy (no pierce), spends 1 arrow, uses the normal Watch prompt and damage, and lands on the enemy's tile (LI-6). Because it fires before the swing, it protects the fetcher by killing or softening the attacker; it doesn't cancel the attack.

**How it reads.**
- A Linda-coloured eye on the fetcher.
- While the Watch prompt is up, a thin tether from Linda to the covered fetcher, the same look as John's tether (FR-13).
- The prompt says "Covering Mark".

**Cost.**
- A second trigger in `LindaFactionRoleHandler` (on the quiver plan's core-change list), plus an off-lane shot. The Crescendo arrow already flies to any cell, so the projectile exists; the trigger is the new part.
- Medium–high to build, plus a role-zone question: her zone is no longer only lanes.

**Verdict:** the warmest option ("she stays back so the one who goes out is safe"), but too big for D1. A good **skill node** later. D1 tests its cheap cousin, Watched (below).

## Q1 study: fetcher rewards

All of them are given only for a walking pickup (not an instant pickup on landing, G3, nor a catch), once per Bergson per turn. Linda fetching her own arrows gets nothing extra (Far Watch covers her).

| Reward | Feel | Build cost | Read | Note |
| --- | --- | --- | --- | --- |
| **Watched**: the fetcher takes ×0.75 damage until the next player turn | "Linda has your back": replaces the cover they left. Answers R1 directly | **Lowest**: one duration modifier from the pickup code (like John's `JFR_DR`, a DR stat) | **Clear**: the eye icon on the unit; hit previews show the reduced damage | John's relay still wins inside his zone; it matters only outside it |
| +1 movement on the next move | Run out, get back | Low: the same mechanism as Move as One (LI-2) | Clear: the ghost's reach grows | Doesn't help in the enemy phase, which is the real cost |
| Free 1-tile step after the pickup (0 AP) | "Grab and duck back": the best feel | Medium: a new 0-AP action and an input state. CR-6 says any action needs ≥ 1 AP, so a pickup made with the last AP gets nothing unless a core rule changes | Medium: an extra prompt in the flow | A later node ("Light Feet") |
| +1 FTP | Feeds Duos | Low (`GUnit.ProduceFTP`, V) | Medium (the FTP bar) | Node upgrade (D-264) |
| Big Sister's Eye | The warmest | Medium–high | Clear | Later node (above) |

**Cheapest to build and to read: Watched.** It is also the one that answers the root cause: leaving John costs cover, and Linda gives cover back.

## Q4 study: the Mark–Linda Duo

**Fetch Race (recommended).** Mark races Linda's own arrow.

- **Rules:**
  - Duo, 0 AP + 2 FTP + 1 arrow, cooldown 2 (Head Start −1 kept).
  - Linda aims a bow shot down one of her lanes, as her bow: range, pierce, damage, and the landing cell from the C4 marker.
  - At the same moment Mark sprints toward that landing cell. The target must be a cell Mark can reach (his move radius +1, as the Footrace uses today). He picks up every grounded stack on his path.
  - He ends on the landing cell, or on the nearest free cell next to it if an enemy stands there, and catches the arrow as it lands.
  - He tosses the whole bundle to Linda (the hand-back beat, call-out variant). The shot costs her 0 net arrows.
  - No QTE: the race is the synced moment, and the catch QTE belongs to the Synergy.
- **Win flavour:** a landing cell out of Mark's reach can't be targeted (greyed with "Too far for Mark"), so there is no random loss.
- **Why it's distant but synced:** they act in one beat and end far apart. Linda stays at her post; Mark ends at the far end of her lane, next to the enemy she just hit, with his AP ready for a Fist Blitz. Often he ends **in line with Linda and 2 or more cells away**, which sets up next turn's Catch & Return. The Duo builds the Synergy's geometry instead of breaking it (R4).
- **Distinct from the catch:** in the catch, Mark stands in her line and the arrow comes to him (QTE, back to her hands, D-260/D-261). In the Race, Mark runs after the arrow, anywhere, and ends far out.
- **How it reads:** one decision (her lane). The preview shows the arrow path with damage, the landing marker, Mark's path and ghost, and "+N arrows" for the stacks he sweeps.
- **Cost and core touch points:** `UnitsCooperationHandler` (core): new `Mark_Linda` targeting and resolve code replacing the race's; a simultaneous move and projectile; Mark's path reusing `Mark_Linda_Path` and the ghosts. Linda's leg uses her bow as a partner preset, like the arrow Duos. Landing suppression and the bundle hand-back live in the non-core quiver code (`QuiverArrow`, `LindaQuiver`). `PlayerController.prefab` entry and presets are data. Medium–high; its own commit. The old race's bonus listener has a mismatch (added to `abilityPerformed`, removed from `abilityActivationStarted`, lines 1395/1408); the rework removes it.

**Alternative 1: Family Gauntlet** (name to the narrative pass). Mark and Linda must share a row or column, 3 or more apart. Until the next player turn, the cells between them are a gauntlet: an enemy that ends a move in it is shot by Linda (Watch rules, 1 arrow) and then struck by Mark, who dashes along the line (Fist Blitz). A pincer across the board. Distinct from the catch (a trap, not a bounce). Cost: high (two role handlers, both core-listed); readability needs a drawn corridor.

**Alternative 2: Footrace, apart.** Keep the race; the loser stops at the furthest cell of their path that is in line with the winner and 2 or more cells away, instead of next to them. The smallest change (`Mark_Linda_LoserStop`, core). It fixes R4 but adds nothing about distance or arrows.

## Proposed rules (IDs proposed; rev 1's LI-13 Lookout is withdrawn and not reused)

- **LI-14. Fetch FTP** (a skill node, D-264): a walking pickup gives +1 FTP, at most once per Bergson per turn, at most +2 per family per round. Not in D1.
- **LI-15. Far Watch.** If no Bergson stands within 2 cells of Linda when the family ends its turn, her Watch deals ×1.5 until the next player turn. Watch base 6× → 5× (toggle).
- **LI-16. Watched.** A walking pickup makes the picker take ×0.75 damage until the next player turn, once per Bergson per turn; Linda excluded.
- **LI-8 (amended).** Encore cooldown 3 (D-263, toggle).

## Lens notes

- **Creative.** Linda holds a far post with fewer people near her, and hits harder for it; whoever leaves John's shelter to run her an arrow comes back under her eye. Two protectors: John holds the centre, Linda the edge. The moment designed for: Mark tearing down her lane after her arrow, scooping it up next to the goblin she just hit, and throwing it back across the field ("Too slow, sis!").
- **Systems.** The levers:
  - the Far radius (2), multiplier (×1.5) and base (5×);
  - Watched (×0.75);
  - the Encore cooldown (3).

  Failure cases:
  - She parks far away and wins on damage. The trade base and the quiver bound this; watch her share.
  - Watched makes fetchers tanks: it is once per turn and outside John's zone only by accident; ×0.75 is mild.
  - Fetch Race as a free shot every 2 turns: it costs 2 FTP and needs Mark's AP turn to follow.
- **UX.** The Far mark and "Far lost" on ghosts, locked at End Turn. Watched's eye on the unit. Fetch Race in one decision with the full preview. Likeliest misread: "her Watch did less damage" when a sibling stood next to her at End Turn. Hence the prompt line and the mark.

## USP check

- **Family Roles:** strengthens. Watch gains a positional trade; Watched gives her role a protective side.
- **Synergies:** strengthens. Fetch Race sets up Catch & Return's geometry.
- **Duos:** strengthens. Mark–Linda becomes distant and synced, distinct from the catch.
- **Home:** neutral on purpose (Fetch FTP and the later nodes are progression).

## Critics

Rev 1: three parallel critics (Explore agents with critic briefs; `miso-design-critic` wasn't available), each blind to the others.

| Lens | Strongest point | What I did with it |
| --- | --- | --- |
| Systems | Encore wins on AP (R2); Fetch FTP farmable through instant pickups and into Watch; Long Pass ×1.5 raises her share | Encore cooldown 3 (D-263); no rewards for instant pickups; rev 2 uses the trade base for Far Watch |
| Creative | A "be alone" reward feels lonely; reward the walker; Big Sister's Eye; cut the Footrace, make it a Fetch Race | Watched as the cheap Big Sister's Eye; the full version as a node; Fetch Race detailed |
| UX | Range changes are invisible under FR-10/FR-11; state flips mid-phase; Long Pass is three decisions | Far locked at End Turn with marks; Fetch Race is one decision |

Rev 2 was not re-critiqued: the changes follow THJ's answers and the rev 1 critics' points. If THJ wants it, a systems critic on Far Watch's share is the one worth running.

## Recommendation

**Step D1, "distance pass"** (after C4, alongside or after C3b; non-core; each lever a toggle on one config asset):
1. LI-15 Far Watch: trade base 5×, ×1.5 when Far, locked at End Turn; Far mark, "Far lost", the prompt line.
2. LI-16 Watched (×0.75) with the eye icon.
3. Encore cooldown 3 (D-263).
4. Cues: a hand-back variant per picker (John's lob, Lucy's spark, Mark's spin throw, Toba's leaf, Linda's "One more."); a call-out when the picker is 4 or more cells away; a glint only on stacks reachable this turn. Lines from `miso-narrative`, tagged `[PLACEHOLDER]`.
5. Log lines (with C5): pickup kind and the picker's distance to Linda; Far on/off at End Turn; Linda's distance to her nearest sibling; Watch damage near/far; Watched hits reduced.

**Step D2:** Fetch Race replaces the Footrace (core, own commit), after C3b, so the catch and the Race can be told apart in play.

**Playtest signals** (M4, M6 with a full squad; against the C4 build):
- Walking pickups ≥ 30% of returns (below that, D1 failed).
- Encore at most once per level.
- Linda's distance to her nearest sibling at End Turn up ≥ 1 cell.
- Far at ≥ 40% of End Turns.
- **Linda's damage share not above the C4 build** (over it: drop ×1.5 to ×1.25 or keep the base trade).
- No Linda death attributable to standing Far in 3 or more levels.
- Fetchers outside John's zone take a hit at least once per level (Watched matters).
- THJ and testers mention the hand-backs unprompted.
- Cold players can say why her Watch hit harder.

## Questions for THJ

Answered 2026-10-27: Encore cooldown 3 (D-263); Fetch FTP is a node (D-264); not Long Pass (D-265).

1. **How should Far Watch work?** *Context:* any Watch damage-up raises the share the quiver was cutting. *Options:* (a) Far from the nearest sibling, one step ×1.5, base 6× → 5× (trade); (b) the same without the trade (9× far); (c) distance from the target, first enemy only. *Recommendation:* (a). *Blocks:* D1 item 1.
2. **Which fetcher reward?** *Context:* fetching costs cover; you asked for something for the fetcher. *Options:* (a) Watched, ×0.75 damage until the next player turn; (b) +1 movement on the next move; (c) a free 1-tile step after the pickup (needs a CR-6 exception); (d) cues only. *Recommendation:* (a) now; Big Sister's Eye and the free step as later nodes. *Blocks:* D1 item 2.
3. **Which Mark–Linda Duo?** *Context:* the Footrace ends them adjacent (R4); the Duo must differ from the QTE catch (D-260). *Options:* (a) Fetch Race as above; (b) Family Gauntlet; (c) Footrace, apart; (d) keep the Footrace. *Recommendation:* (a), as D2 after C3b. It replaces the race code in `UnitsCooperationHandler` (core). *Blocks:* D2's tech plan.
4. **Where does the Fetch FTP node live?** *Context:* D-264 makes it an upgrade. *Options:* (a) a Family node on Linda's tree (she has none today); (b) a run upgrade; (c) the Home workshop quiver adds it. *Recommendation:* (a). *Blocks:* nothing in D1; progression docs.
5. **John's pull (still open).** *Context:* R1 is family-wide; the area relay removes the cost of clumping. *Options:* (a) leave John as built and open a separate formation review of every proximity reward; (b) test relay radius 1 now. *Recommendation:* (a). *Blocks:* nothing in D1.

## Docs to update if approved

- [`characters/linda.md`](../design/gdd/characters/linda.md): LI-14 to LI-16, LI-8 cooldown, Encore name (*Planned*).
- [`family-systems.md`](../design/gdd/family-systems.md): the Mark–Linda Duo row (Fetch Race), the Watch row (Far), Catch & Return note.
- [`characters/mark.md`](../design/gdd/characters/mark.md): Head Start node wording.
- [`progression-economy.md`](../design/gdd/progression-economy.md): the Fetch FTP node; later nodes (Big Sister's Eye, Light Feet).
- `glossary.md` (Far Watch, Watched, Fetch Race; `miso-narrative`).
- The quiver tech plan (D1, D2), `decisions.md`, `status.md` (coordinator).
