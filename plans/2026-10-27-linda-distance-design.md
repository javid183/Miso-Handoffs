# Linda at a distance: rewarding the far game and the fetch

Size: L    Tier: 3 (Family Roles, Synergies, Duos)    Assigned to: game designer
Branch: all (prototype on `thj/linda-quiver`, after C4 of the [quiver tech plan](2026-10-26-linda-quiver-tech.md))
Status: rev 3, final. D1 ready for a tech plan (edge questions answered: D-285, D-286; the Fetch FTP node location is still open). Arrow Chase has its own plan: [`2026-10-28-arrow-chase-design.md`](2026-10-28-arrow-chase-design.md) (after D1)

## Why

THJ's play check of the quiver prototype (C1–C3, 2026-10-27) found five things:

- The family packs around John, so arrows land where nobody is.
- Walking pickup is rare, and Encore (Recall's on-screen name, D-262) is the normal way back.
- The walk and the hand-back are the best moment, and they happen too rarely.
- Nothing rewards Linda for playing apart.
- The Mark–Linda Duo pulls the pair together, against their own Synergy.

## Goal

A first prototype step (D1) that tests whether distance feels rewarded: Linda standing apart, and the family walking out to her arrows. It must not raise her damage share in the way the family plays today.

## History

- **Rev 1:** Lookout (+1 Watch range), Fetch +1 FTP, Long Pass.
- **Rev 2:** Far Watch, Watched, Fetch Race.
- **THJ's answers:**
  - D-263: Encore cooldown 3 as a toggle.
  - D-264: Fetch FTP is a skill node.
  - D-265: no Long Pass.
  - D-266: Far Watch with the trade.
  - D-267: cues only for fetchers.
  - D-268, D-271: Arrow Chase replaces the Footrace, after D1.
  - D-269: John stays as built; a formation review later.
- **Changes since rev 2 that this plan relies on:**
  - Mark's catch is a QTE with the arrow frozen on its path (D-260, D-261, D-273 to D-278; D-279 keeps the old arrow slope).
  - Lucy follows up only on real damage (D-275, D-277).
  - Arrow hits may move to the grid on `main` (D-279, `arrow-hits-by-grid` in `status.md`).

## Problem and evidence

V = verified in data or code; A = assumed.

- **R1. Everything good happens up close.** John's relay (2 cells; area hits once, D-120), Papa's Shelter, Mark's Counter (2), Lucy's follow-up (3), Pass-by +2 FTP (CR-11) and the Footrace all pay for standing together. Nothing pays for spreading out (V: `family-systems.md`). This is family-wide; THJ moved it to a later formation review (D-269).
- **R2. Encore beats walking on AP.** One AP brings back every stack; walking costs 1 AP per stack and leaves John's cover (CR-6, LI-8) (V). The test answer is D-263.
- **R3. Linda's kit has no distance payoff** (V: `linda.md`). The test answer is D-266.
- **R4. The Footrace ends the pair adjacent.** The loser stops on `path[^2]`, but the catch needs 2 or more cells (V: `UnitsCooperationHandler.Mark_Linda_LoserStop`; D-274). The answer is Arrow Chase.
- **A.** Whether the enemy AI hunts isolated units is unread (`UtilityVariables` has presence terms; the evaluator assets were not read). It sets the real price of Far.

## Options considered (summary; details in rev 1 and rev 2)

| Option | Fate |
| --- | --- |
| Lookout: +1 Watch range when apart | Dropped: her lanes already cover most of the board (THJ) |
| Far Watch with the trade | **D1** (D-266) |
| Far Watch, additive (9×), or measured from the target | Rejected: raises her share; target distance rewards pierce lines, not standing apart |
| Fetcher rewards: Watched, +1 move, a free step, +1 FTP | Cues only in D1 (D-267); +1 FTP becomes a node (D-264); the others are later nodes |
| Big Sister's Eye (her Watch covers fetchers) | Later node: it touches `LindaFactionRoleHandler` (core-listed) |
| Encore cooldown 3 | **D1** (D-263) |
| John's relay radius 1 | Not now (D-269) |
| Long Pass, Fetch Race, Family Gauntlet, Footrace apart | **Arrow Chase** (D-268, D-271): [own plan](2026-10-28-arrow-chase-design.md) |

## D1: the distance pass (ready for a tech plan)

Four items, all non-core where possible. Each lever is a toggle on one config asset (`LindaDistanceTuning` or similar; the tech plan names it), so THJ can switch each off in play. With every toggle off, the build plays like C4.

### D1.1 Far Watch (LI-15, D-266)

**Rule.**
- **Base Watch:** 5× damage (was 6×).
- **Far:** if Linda is Far, her Watch deals 7.5×. Only Watch changes: bow, Explosive Crescendo and the arrow Duos keep their values.
- **Pierce:** falloff applies as usual. Near: 5 → 3 → 1.8. Far: 7.5 → 4.5 → 2.7. Rounding per CR-19.
- **Multipliers:** Revenge and crits multiply as they do today.

**Who counts for the 2-cell check (D-285).** Every *living* unit of the player's squad other than Linda: John, Lucy, Mark, and Toba when he is in the squad.
- Not counted: decoys (Blink, Hide and Seek), the Cyclone, Toba's wall, allied units of another faction (e.g. `Unit_Toba_Ally`, as in D-254), and dead or removed units.
- Distance is the footprint distance, radial (diagonals count as 1, like John's zone, FR table). Far = no counted unit at distance ≤ 2, so a 5 × 5 box around Linda must be free of family.

**When the check runs.**
- **End Turn:** when the family ends its turn, after the last action resolves and before the first enemy acts. The state is **locked** until the next player turn starts. Pushes, pulls, deaths and Commands during the enemy phase never change it.
- **Player phase:** Watch can trigger on the player's own turn (a push, a Command move, a Masher answer, D-039/D-119). Then Far is checked **live**, at the moment of the trigger (D-286).
- **Level start:** before the family's first End Turn there is no locked state, so an enemy phase can't come first. If a level opens with enemies acting, Linda counts as near.

**What the player sees.**

| When | Where | What |
| --- | --- | --- |
| Player phase, always | Over Linda, next to her arrow pips | A **Far mark** (her `BowArrow` icon with an eye, in her role colour) while she is Far right now; nothing when near |
| Previewing Linda's move | Her ghost tile | The Far mark if that tile would be Far, with the others where they stand |
| Previewing another unit's move | Over Linda | "Far lost" (the mark struck through) if that ghost comes within 2 of her while she is Far now; "Far" (the mark) if the move takes the last nearby unit away |
| Hovering her role badge, or Shift | Grid | Her 2-cell box outlined, faint, in her colour (only the tiles that must stay clear) |
| After End Turn, enemy phase | Over Linda | The mark stays if she locked Far, with a small lock pip; none if near |
| Watch prompt | Prompt text | "Arrows 3 → 2 · Far 7.5×" or "Arrows 3 → 2 · 5×" |
| Watch hits | Damage numbers | Real values. The role badge tooltip: "Watch: 5×. Far (no family within 2 at End Turn): 7.5×." |

`[PLACEHOLDER]` on all strings (D-272).

**Implementation notes for the tech plan (A).** Watch spawns an arrow prefab through `Linda_Ability_FactionRole_Effect_Spawn` (V), the same arrow as her bow (A, by GUID). A global `Stat_DMG` modifier would also scale player-phase bow shots, so the factor must apply to Watch arrows only. For example: `QuiverArrow` knows it came from Watch, or a Watch variant of the arrow prefab sets 5× and a Far factor of ×1.5. The tech plan picks one, with no core code. The Far check needs the squad list and footprint distance, both read-only.

**Acceptance.**
- [ ] Toggle off: Watch hits as today (6×), no mark, no box.
- [ ] Toggle on, John 2 cells from Linda at End Turn: Watch hits 5× in the enemy phase; the second pierced enemy takes 3 (before stats).
- [ ] Toggle on, nobody within 2 at End Turn: Watch hits 7.5× through the whole enemy phase, even after an enemy pushes Mark next to her. The mark and its lock pip stay.
- [ ] Toba in the squad within 2 at End Turn: near. A Lucy decoy within 2: still Far. A dead Bergson within 2: still Far.
- [ ] A player-phase Watch (an enemy Commanded into her lane) uses the live state at the trigger.
- [ ] The ghost mark and "Far lost" match the state End Turn would produce for that position.
- [ ] The prompt and tooltip show the right factor; the hover damage preview matches the hit (CR-17 rule).
- [ ] EditMode tests: the Far rule (who counts, radial ≤ 2, footprints), the factor table, the lock-until-player-turn state.

### D1.2 Encore cooldown 3 (LI-8 amended, D-263)

**Rule.** Encore keeps everything as built (1 AP, usable with ≥ 1 arrow grounded and room in the quiver, D-256), with cooldown 3: used on turn N, it is next usable on turn N+3. Toggle off: cooldown 2. The cooldown shows on the button and in the tooltip as today.

**Acceptance.**
- [ ] On: used on turn 1, greyed on 2 and 3, usable on 4. Off: usable on 3.
- [ ] The tooltip and the cooldown counter show the active value.
- [ ] The known-red `AIRegressionTest` message is unchanged (a value change on an existing preset).

### D1.3 Fetcher cues (D-267: cues only)

**Rules (presentation only; no rule change).**

- **A hand-back variant per picker.** It replaces the generic toss and lines on a *walking* pickup (the picker's own move, forced moves and Duo moves included):
  - **John:** an underhand lob; a fatherly line.
  - **Lucy:** the arrow flicked over with a small spark trail; a teasing line.
  - **Mark:** a spinning throw Linda catches one-handed (it foreshadows the catch); a bragging line.
  - **Toba:** a short hand-off arc, wrapped in a leaf; a polite, slightly formal line (he isn't family yet, D-048).
  - **Linda herself:** no toss; she slips it into the quiver; a quiet line ("One more.").
- **The call-out.** If the picker is **4 or more cells** from Linda (footprint, radial) when picking up, the picker's line becomes a shout ("Linda! Catch!"), the toss becomes a long high arc, and Linda's reply becomes a catch line. Below 4: the normal variant.
- **One beat per move.** A move that picks up several stacks plays one hand-back with the total ("+3"). The second hand-back by the same picker in a turn uses a short line (no repeats).
- **Not affected:**
  - Instant pickups when an arrow lands on a Bergson (G3) keep today's short beat.
  - Encore keeps its return flight.
  - Mark's catch keeps its own animation and cue (D-259 "+1").
  - While Linda is dead nothing is picked up (D-254).
- **Optional, only if cheap:** a one-time glint at the start of the player turn on stacks that **some Bergson with AP can reach this turn** (the UX critic: a glint on everything reads as loot). If computing reach is not cheap, skip it in D1.
- Lines from `miso-narrative`, tagged `[PLACEHOLDER]`. Beat timings stay fields on `LindaQuiver` and non-blocking (D-247, D-253).

**Acceptance.**
- [ ] Each of the five pickers plays its own toss and lines; Linda's own pickup plays no toss.
- [ ] A pickup 4 or more cells from Linda plays the shout, the long arc and the catch reply; at 3 cells the normal variant.
- [ ] A move through two stacks plays one beat with "+N"; no line repeats twice in a row for a picker in one turn.
- [ ] Instant pickups, Encore and the catch are unchanged.
- [ ] The beat never blocks input.

### D1.4 Log lines (with C5's `CombatLog.Quiver`)

Added to C5's lines (spend, land, pickup, Encore, declined Watch):

- **Level start:** the state of each D1 toggle and the Watch factors, so a log says which build it is.
- **At each End Turn:** Linda's cell; the nearest counted unit and its distance; Far yes/no.
- **Each Watch shot:** phase; the factor used (5 / 7.5 / 6 when off); Far source (locked / live); damage per target.
- **Each pickup:** kind (walk / instant / catch / Encore / Duo), picker, number of arrows, the picker's distance to Linda, whether the call-out played.
- **Linda's damage taken while Far** (for the "Far gets her killed" signal).

**Acceptance.**
- [ ] One level played gives every line above.
- [ ] `CombatLogTests` covers the End Turn Far line and the pickup kind.

### D1 playtest signals

Missions M4 and M6 with a full squad, compared against the C4 build with every toggle off.

| Signal | Pass | Means |
| --- | --- | --- |
| Walking pickups as a share of all returns | ≥ 30% | The fetch happens. Below: D1 failed on R2 |
| Encore uses per level | ≤ 1 | Encore is the backup |
| Linda's distance to the nearest counted unit at End Turn | Up ≥ 1 cell on average | Players move her out |
| End Turns with Linda Far | 30–60% | A real choice. Near 0: the reward is too small; near 100: too safe or too strong |
| Linda's damage share | Not above C4 | The trade holds. Above: Far 7.5× → 7× or base 5× → 4.5× |
| Watch damage, near vs Far shots | Both appear | Both states are played |
| Linda deaths or ≤ 25% HP while Far | Under 1 in 3 levels | Far isn't a trap (and answers the AI question A) |
| Call-outs per level | ≥ 1 | Long fetches happen |
| THJ and testers | Mention the hand-backs and the call-out unprompted; can say why Watch hit harder | Feel and readability |

## USP check

- **Family Roles:** strengthens. Watch gains a positional trade (John's cover, or more damage).
- **Synergies:** neutral in D1 (Arrow Chase sets up the catch later).
- **Duos:** neutral in D1; Arrow Chase strengthens them later.
- **Home:** neutral on purpose (Fetch FTP and the later nodes are progression).

## Critics

Rev 1: three critics run in parallel (Explore agents with critic briefs). The systems critic named R2, so Encore cooldown 3 went in. The creative critic warned of a lonely reward and pushed for rewarding the walker, which led to the cues and the later nodes. The UX critic flagged invisible state changes, so the state now locks at End Turn and the marks were added. Rev 2 and rev 3 follow THJ's answers. Arrow Chase had its own critics: see its plan.

## Questions for THJ

Answered: Q1 (D-266), Q2 (D-267, D-264), Q3 (D-263), Q4 (D-268, D-271), Q5 (D-269). Rev 2's "where does the Fetch FTP node live" is still open; it doesn't block D1.

Rev 3's edge questions, answered 2026-10-28: a player-phase Watch uses the live Far state (D-286); Toba and every living squad unit count for "near" (D-285). D1.1 above already follows both.

Still open (it doesn't block D1):

1. **Where does the Fetch FTP node live?** (from rev 2) *Context:* D-264 made it an upgrade; Linda has no family nodes. *Options:* (a) a Family node on Linda's tree; (b) a run upgrade; (c) on the workshop quiver. *Recommendation:* (a). *Blocks:* progression docs only.

## Docs to update if approved

- [`characters/linda.md`](../design/gdd/characters/linda.md): LI-15 Far Watch, LI-8 cooldown 3 (toggle), the Encore name (D-262), the Watch row; *Planned* until played.
- [`family-systems.md`](../design/gdd/family-systems.md): the Watch row in the Family Roles table (5× / 7.5×, Far).
- [`progression-economy.md`](../design/gdd/progression-economy.md): the Fetch FTP node (LI-14); later nodes Big Sister's Eye, Watched, a free step.
- `glossary.md` (Far, Far Watch, Encore; `miso-narrative`) and the hand-back lines.
- The quiver tech plan (a D1 chunk), `decisions.md`, `status.md` (backlog: formation review, D-269) (coordinator).
- Arrow Chase's docs: see its plan.
