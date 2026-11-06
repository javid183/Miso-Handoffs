# Opening order: basics before the first Family Role

> **THJ, 2026-11-05 (D-397): not adopted.** Linda's memory stays first and as tuned; Lucy's opens with a multi-shot, not a basic rule. Panel stays "Watch"; Encore as is. Kept for reference if a cold playtest shows the first Role confuses.

Size: L    Tier: 3 (level order and first-exposure design of the opening; touches narrative hand-offs)    Assigned to: miso-game-designer
Branch: `thj/onboarding` (the working main, D-396). Nothing here touches `thj/home-test`.
Status: waiting on THJ

## Why

THJ's own playtest of the Hearth memory (2026-11-05): the tutorial **begins with Family Roles**, the mechanic only Miso has, which may confuse a new player; the opening may also be paced too quickly. He takes the optimistic view: the onboarding can be tuned. This plan looks for fixes inside the onboarding structure. If it can't be polished in time, the fallback is the shortened classic opening (D-396); a fix that also helps that fallback is a plus.

## Goal

A brand-new player meets the basic turn (select, move, attack, AP, end turn, a normal enemy turn) before the first Family Role fires, and meets that Role as a named family system, without making the Hearth longer.

## Acceptance criteria

- [ ] The first Family Role prompt a cold player sees comes **after** they have finished at least one full player turn and watched one enemy turn with no Role in it.
- [ ] The first Role is introduced as a **Family Role** (the term the River and the Ridge already use), on its own panel, not stacked with the basics.
- [ ] No level in the Hearth carries more than ~6 new things (today segment 1 carries ~19).
- [ ] Hearth total time unchanged (± 0.5 min on paper); first Role QTE by ~6 min (today ≈ 2.5).
- [ ] No level prefab edit is needed; every change is data, wiring tools, tests or text.

## Scope

In: the order of the four memory segments, the panels at the start of the first two, the narrative hand-offs that the order change touches (proposals for `miso-narrative`), one optional trim in Linda's segment.
Out: the content of each segment (THJ's tuned levels stay as they are), the search missions, Roles' FTP cost (FR-3), a first-trigger framed beat (B6, unbuilt), a per-level role mute (not built), the classic fallback itself.

## Touches

Systems: the Hearth mission's level graph (`M0 - The Hearth` asset, data); `HearthMemoryWiring.Linda.cs` and `.Lucy.cs` (panels and grid fade at start); `HearthMemoryLevelsTests` (order) and the Linda/Lucy wiring tests. No core system.
USPs: Family Roles (main), Synergies and Duos (neutral), Home (neutral).
Docs: see [Docs to update](#docs-to-update-if-approved).

---

## Problem and evidence

### What a new player meets today, in order (first ~5 minutes)

Times are the levels plan's cold estimates (30–45 s a unit on first turns, 10–25 s an enemy turn, 15 s a panel), not a timed run. Geometry from the segment 1 grid and table in [the levels plan](2026-10-26-onboarding-levels.md#segment-1--lindas-telling-seven-claws-one-arrow); panel text and stages read from `HearthMemoryWiring.Linda.cs` (verified).

| ~Time | What happens | New for the player | Asked to understand? |
|---|---|---|---|
| 0:00 | Hearth open (Home state, Margaret, 3–4 lines) | The frame | — |
| 0:45 | Segment 1 loads: Margaret "Eldest first. Linda." | — | — |
| 0:50 | **Two panels back to back:** "Moving and AP" (select, move, 2 AP, end turn) then "Watch" ("When an enemy ends its move in Linda's row or column, press the key shown above her to shoot it. Each shot spends an arrow.") | 1 select · 2 move · 3 AP · 4 end turn · **5 Watch (the first Family Role, explained before the player has moved once)** · 6 arrows | Yes, all at once, before any of it is relevant |
| 1:15 | Turn 1: Linda walks up the 1-wide throat, shoots up column 2; the arrow pierces | 7 attack and targeting · 8 pierce · 9 her quiver count drops (3 → 2) · 10 objective text ("Eliminate all dark claws.") | By doing |
| 1:15 | The Claws stand still: they start Unaware (D-384) | 11 Unaware / waking (untaught until the search's "Asleep" panel) | No |
| **~2:15** | **Enemy turn 1, the player's first ever.** B (turn order 0) walks down the throat and stops in Linda's column → **Watch QTE**, real time, 1 s window (FR-2); her quiver drops again on the enemy's turn | 12 enemy turn · 13 **the first QTE of the game, which is the first Family Role** | Expected to recall a panel read ~80 s earlier, inside a 1 s window |
| ~2:45 | Turn 2; stage 1 ends at its cap (2) or all dead → "Gather your arrows." | 14 staged objectives · 15 arrows on the ground and pickup (LI-7) | Yes |
| ~3:30 | Linda on 2,7 → the cut-in: camera, the phase **resets** (fresh turn), 4 Claws revealed, **Explosive Arrow and Encore appear**, Explosive Arrow pulses | 16 phase reset · 17 Explosive Arrow · 18 Encore (pulses when the quiver is empty, G3) | Yes (the pulse) |
| ~4:30 | Stage 3 to cap 4; punchline "Seven Claws. One arrow."; grid fade; cutaway | 19 the turn countdown ("Turns left in the memory") | — |
| ~5:00 | Segment 2, Lucy: Fire Embers (sidewinder), Cyclone unlocked mid-level with a pulse | Embers, sidewinder, Cyclone | — |

**Where the first Family Role fires:** Linda's Watch, on enemy turn 1 of segment 1, ~2:15 in. The geometry makes it near certain: the throat is 1 wide and all three Claws stand in column 2, so the first Claw to move ends in her column (derived from the grid, not played). **Is the player asked to understand it then?** Yes: the Watch panel came before turn 1, and the prompt asks for a press inside 1 s.

What the rest of the Hearth adds, for comparison (from the four wiring tools and the plan): segment 2 (Lucy) ~3 new things; segment 3 (John) ~5 (Shield Up, Wrath stacks, John's Role with its paused prompt and tether, Lucy's follow-up untaught, turn-1 AP limit; Duos locked, D-393); segment 4 (Mark) ~6 (four units, Tempest Bloom by hints, Continuous Attack, Mark's Counter untaught, Chained Assault, the mother's scene).

### The root problem

Not "the Role fires too early" by itself. Four things stack in the same 90 seconds:

1. **No baseline.** The player's first enemy turn is also their first Role. They never see what an enemy turn normally looks like, so they can't tell "what the Claws do" from "what Linda does on their turn". (Evidence: the throat geometry; Claws start Unaware, so turn 1 has no enemy action; enemy turn 1 is the first.)
2. **Density.** Segment 1 carries ~19 firsts, about 4 a minute; no other level in the opening carries more than ~6. The Role is one item in the densest level of the game. THJ's "paced too quickly" matches this: the pace problem is per minute in segment 1, not the Hearth's length (which is long on paper: ≈ 17 min against 12–15).
3. **Taught before relevant.** The Watch panel is the second of two panels shown before the player has moved, ~80 s before it matters, and it is about a real-time press.
4. **No frame for the USP.** The word "Family Role" never appears in the Hearth: the panel is titled "Watch", the prompt says "Activate Passive" (FR-2). The player learns "Linda has a trick", not "every Bergson has a Family Role", which is the idea the River's and the Ridge's panels ("Lucy's Family Role", "Mark's Family Role", read from their panel assets) then assume.

A fifth, smaller one: Watch spends an arrow, so the first Role and the quiver lesson are tangled. The arrow count drops on the enemy's turn without the player choosing.

So the Role is not wrong as an early beat. It is **untaught by experience** (no baseline), **taught too early by text**, and **buried** in the densest level.

---

## Options compared

| | **A. Tidy segment 1 in place** | **B. Mute Watch in segment 1** | **C. Lucy first, then Linda (recommended)** | **D. Add a basics beat to segment 1** |
|---|---|---|---|---|
| What changes | Linda stays first. "Moving and AP" stays; the Watch page is retitled "Linda's Family Role" and gains one line of frame; Encore stays locked in the memory, so the cut-in adds one button | FTP drained to 0 in segment 1 (`LevelStartFPFiller` −99), so Watch can't pay and never fires (verified: `FactionControllerBase.ActivateFactionRoleIfFeasible` needs `CanConsume(requiredFTP)`, and every role costs 1 today). First Role becomes John's in segment 3 | Hearth order becomes **Lucy → Linda → John → Mark**. "Moving and AP" moves to Lucy's start; Linda's start keeps the Watch page alone, retitled as her Family Role. Lucy is alone, so no Role, Synergy or Duo can fire in the first level (levels plan, segment 2) | A first stage in segment 1 where Linda moves and shoots a sleeping Claw out of the lanes before the pack can reach her column (or turn-1 AP limit, the existing `TurnStartActionPointLimit`) |
| First Role at | ~2:15 (unchanged) | ~9 min (segment 3) | **~6 min** (Linda's enemy turn 1, now in the second level) | ~3:00 |
| Baseline enemy turn first? | No | Yes | **Yes** (Lucy's alert Claws walk and strike, or the revealed three walk in) | Partly (one quiet enemy turn) |
| Density of the first level | ~17 | ~16 (no Watch, still pierce, quiver, pickup, Explosive Arrow) | **~8** (Lucy) then **~9** (Linda, basics already known) | ~19, spread over one more turn |
| Pace and Hearth time | Same | Same | **Same** (same four levels; panel moves) | +~0.75 min on a Hearth already over target |
| Narrative ("each member's telling") | Unchanged | Linda's boast loses its trick | Hand-offs rewritten: Lucy grabs the first telling, Linda's "Seven Claws. One arrow." answers Lucy's "ten" (4–6 lines, `miso-narrative`) | Unchanged |
| Cost: levels | None | None | None (no prefab edit) | THJ's hand-tuned `GB_m1-linda` edited again |
| Cost: tech | Wiring text + one lock entry | Wiring data + test | Mission graph data, two wiring tools (panels, grid fade-in at Linda's start), tests | Prefab + wiring + tests |
| Risk | Keeps the root problem (no baseline) | Segment 3 then fires three Roles with only John's taught; Linda's role badge shows a can't-pay state from the first second (`UnitPanelUI.RoleBadge` reads `CanConsume`); stops working when FR-3 (roles free) is built; contradicts the demo spec's rule (roles free) | Linda's segment starts Unaware right after a level where Claws are awake; the design criterion "Role QTE by ~5 min" moves to ~6 | Adds time; still the densest level |
| USP: Family Roles | + (named) | − (hidden 9 min, then three at once) | **++** (named, on its own, against a baseline, still in the first ~6 min) | + |
| Helps the classic fallback? | A little (panel text reusable) | Its **mechanism** helps: the fallback's John + Lucy level could mute Lucy's untaught follow-up the same way | **Yes**: the classic M1 already plays a basics level (`Level1-C1_TArtEx`, John + Lucy) before Linda's level (`Level1-C1-2`, which `GB_m1-linda` was built from), so both openings teach in the same order and the new Watch panel carries over | No |

Doing nothing is a real option only if the timed cold run shows new players read Watch fine; THJ's own play says otherwise, so it is not in the table.

---

## Lens notes

### Creative

**Target experience.** The first minute should feel like being handed the game by the family, not quizzed by it: Lucy, too impatient to wait her turn, blasts two Claws and then swears there were ten. Only then does Linda, the eldest, take the floor with something nobody else can do. The first Family Role should land as **the family's secret**, shown by its proudest member, not as rule number five on a card.

**The moment designed for:** Linda's first enemy turn in her own telling. The player now knows what Claws do on their turn (Lucy's level showed them walking in and swinging). This time one steps into Linda's line, the prompt pops, and an arrow takes it before it can act. That contrast is the "oh, that's Miso" beat.

Why C is better than the genre default here: a dry "tutorial level first" would delay the family; C keeps a Bergson telling a tall tale from the first second, and the sister order makes the rivalry the spine of the Hearth from minute one. Lucy, canonically the most attached to Ryker, grabbing the first telling is in character; Margaret's "Eldest first" ritual being broken by her is a warm family beat rather than a loss. Linda's "Seven Claws. One arrow." gets sharper as a reply to "ten" than as a cold open. Sister's Rivalry's arc (setup at the Hearth, payoff in M4) is set up harder.

What it costs: Linda's boast as the very first line of the game was a strong hook. The trade is worth it: the first line becomes Lucy's "So. I'm in the cave. Alone. Very brave.", which is a joke a cold player gets with no rules.

### Systems

**Rules.** None change. C changes the order of four existing levels and moves one panel page. Options A's title change is text; the Encore lock is data on an existing component (`LevelAbilityLock`, G1).

**What C must carry (verified in the wiring tools unless marked):**

| Item | Today | After C |
|---|---|---|
| Hearth level graph | Linda, Lucy, John, Mark (asserted by `HearthMemoryLevelsTests.TheHearthPlaysTheFourMemoryLevelsInOrder`) | Lucy, Linda, John, Mark; test updated |
| Lucy's start | Grid hidden at once, then fades in; one Lucy line | Same, **plus** the "Moving and AP" panel after her line (a `TutorialSequence`, as Linda's start builds it). The fade works the same coming from the Hearth open (the first sequence hides the grid itself) |
| Linda's start | Margaret line, two panels; no grid hide/fade (it was first) | **Adds** grid hidden + fade-in (the previous level's end keeps the grid hidden, `OutroCutsceneKeepGridHidden`, D-131's re-placed rule); one panel: Watch, retitled; Margaret's line replaced (narrative) |
| Cutaways | Linda's ends "Then you tell it, Lucy."; Lucy's ends "Go on, John." | Swapped hand-offs (narrative proposals below) |
| FTP, XP, quiver | Each level fills FTP (+13), gives no XP, Linda starts full (LI-10) | Unchanged: each level sets its own (assumed per-level from the plan's mission rules; to check that nothing reads "first level of the mission") |
| Level display names | `level name Memory 1 · Linda`, `Memory 2 · Lucy` | If shown on screen, swap the display names only; prefab file names stay (`GB_m1-linda` etc.) to avoid churn. **To check** whether `level name` shows to the player |

**Interactions.** Lucy's level has alert Claws within 2–3 tiles at start (3,3 and 4,2 against Lucy on 1,2), HP 6, Tutorial damage ≈ 3. A fumbling first turn costs her HP, not the level. Its stage-1 interruption resets the phase and unlocks Cyclone with a pulse: a guided moment, fine in a first level. Linda's segment then starts with sleeping Claws (D-384); the player has just seen awake ones. That is a new state with no panel until the search, but it is benign: the Claws simply don't move until she's close, which is a free turn to practise the throat.

**Levers.**

| Lever | Start value | Where |
|---|---|---|
| Hearth order | Lucy, Linda, John, Mark | Mission graph |
| Panels at Lucy's start | 1 page, "Moving and AP" (the existing text) | `HearthMemoryWiring.Lucy.cs` |
| Panels at Linda's start | 1 page, title "Linda's Family Role" (or "Family Role: Watch"), text as today plus one frame line (narrative to word; idea: "Every Bergson has a Family Role that acts on the enemies' turn.") | `HearthMemoryWiring.Linda.cs` |
| Encore in segment Linda | Optional (Q3): stays locked for the memory; only Explosive Arrow appears at the cut-in | `LevelAbilityLock` entry and the unlock sequence list |

**Failure cases.**
- *A player kills Lucy's two Claws and never sees an enemy strike.* The three revealed Claws still walk in on enemy turn 1 (7+ tiles, they reach the throat's far mouth), so a plain enemy turn is guaranteed; a strike is likely by turn 2.
- *A player misses the first Watch press.* Costs nothing (FR-2); in a 1-wide throat with three Claws there are more tries.
- *Watch empties the quiver before the player understands arrows.* Unchanged from today; stage 2 ("Gather your arrows.") answers it.
- *Dominant strategy:* none; no rule or number changes.

**Why not B as the main fix.** It works with data today, but only because Roles still cost 1 FTP, which the design means to remove (FR-3, the demo spec's AP/FTP line). It also hides the USP for ~9 minutes and then fires three Roles at once in segment 3, with only John's taught. Its mechanism is better kept as a tool for the classic fallback (below).

### UX

| Moment (after C) | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Level 1 start (Lucy) | Lucy's line; **one** panel, Moving and AP | Lucy, an ember on a Claw, End turn | Doesn't move at all (she can attack from her tile). Fine: Linda's level needs movement and teaches it by layout (the throat) |
| Lucy's first ember | The main ember and a sidewinder that picks its own target | — | Reads the sidewinder as a bonus, not a rule. Fine: no decision depends on it yet |
| Enemy turn 1 (Lucy) | Claws walk in / strike; no prompt | — | None: this is the baseline |
| Interruption (Lucy) | Camera to room 2, three Claws revealed, Cyclone button appears and pulses | Cyclone | Thinks the fresh turn is a bug (phase reset). The camera move and lines make it read as the story |
| Level 2 start (Linda) | **One** panel: "Linda's Family Role" (Watch) | Linda, up the throat | Same as today, but now it is the only text and it is about the next minute |
| First Watch QTE | "Activate Passive" prompt above Linda, 1 s | The key | Misses the window; or doesn't link the arrow count dropping to the shot. The panel's "Each shot spends an arrow" and stage 2 carry it, as today |
| Cut-in (Linda) | Four Claws revealed; **one** new button (Explosive Arrow) pulsing, if Q3 is yes | Explosive Arrow | — |

**One on-screen element?** C adds none; it removes one panel from the busiest moment. The retitle is text replacing text. The prompt's "Activate Passive" wording against "Family Role" in the panel is a mismatch worth a look by the narrative agent, but it is shared UI on every Role (FR-2), so it is out of this plan; noted in Questions as information only.

**Where the lenses disagree.** Creative would like the first Role to be a framed beat (a pause, Linda's line, the QTE); UX and the complexity budget say a level-start panel right before the relevant turn is enough for now, and B6 (first-trigger framed beat) is unbuilt. I lean UX: try C with a single panel; if the timed run shows the first press still lost, the framed beat is the next lever, not more text.

---

## USP check

- **Family Roles:** strengthened. The first Role still comes in the first ~6 minutes, now named as a Family Role, alone on its panel, after the player has seen a normal enemy turn to contrast it with. Every Role still fires in the memory.
- **Synergies:** neutral on purpose. Tempest Bloom stays in segment 4 at ≈ 11 min (unchanged: the total before it is the same).
- **Duos:** neutral on purpose. Chained Assault stays in segment 4; Duos stay locked in John's segment (D-393).
- **Managing the Home as a Family:** neutral on purpose (Hearth open and close unchanged).

## Critics

The `miso-design-critic` agent type was not available in this session (the spawn failed: not in the agent list). I ran the three lenses myself as adversarial passes; the coordinator may want real critics before THJ reads this. The strongest point from each pass and what I did:

| Lens | Strongest objection | What I did |
|---|---|---|
| Creative | "Eldest first. Linda." is a warm ritual and "Seven Claws. One arrow." is the best cold open the Hearth has; Lucy first loses it | Kept the ritual by having Lucy break it (in character: most attached, most impatient); Linda's boast becomes the reply to "ten", which is a stronger joke. Narrative agent to write the hand-off |
| Systems | Lucy first means alert Claws in reach on the very first turn, and Linda's sleeping Claws then contradict what level 1 just showed | Accepted both: Tutorial damage can't lose the level, and sleeping Claws give a free practice turn. Flagged the Unaware misread for the timed run |
| Systems | Is the order baked in anywhere besides the graph (grid fade, the Hearth open hand-off, "first level" flags)? | Checked the four wiring tools: only the grid hide/fade at Linda's start and the panels depend on order. FTP/XP/quiver are per level (assumed from the plan; to check in the build) |
| UX | A level-start panel for a real-time Role is still "taught before relevant" | Partly accepted: the gap shrinks from ~80 s and two pages to one page right before her first turn, and the basics are already known. A just-in-time panel needs an on-first-trigger hook (B6), not built. Kept as the next lever |

## Recommendation

**Option C, with A's retitle; Encore's lock is THJ's call (Q3).**

1. **Reorder the Hearth: Lucy → Linda → John → Mark.** No prefab changes.
2. **Move "Moving and AP"** to the start of Lucy's level, after her first line.
3. **Linda's level starts with one panel**, titled as her Family Role, with one frame line saying every Bergson has one (wording by `miso-narrative`).
4. **Grid fade-in at Linda's start** (she now follows a segment end that keeps the grid hidden).
5. **Narrative hand-offs** rewritten for the new order (proposals for `miso-narrative`, THJ signs off): Hearth open, Lucy interrupts Margaret's "Eldest first" ("Me first. I found her."; Margaret: "Youngest first, then."); Lucy's cutaway hands to Linda (Linda: "Ten?" / Lucy: "At least." / Margaret: "Linda?"); Linda's cutaway hands to John (her "That's exactly how it went." stays; Margaret: "Go on, John. Your turn to be modest."). John's and Mark's segments are unchanged.
6. **Optional (Q3):** Encore stays locked through Linda's segment, so the cut-in adds a single button. Encore's first real lesson is already M2 route B (D-334).

**Starting values:** as in the Levers table. Expected: first Role QTE ≈ 5.7–6.5 min; first level ~8 new things, Linda's ~9; Hearth total unchanged (≈ 17 on paper).

**Playtest signal (the timed cold run).**
- *Worked:* after Linda's level, the player can say what Watch does in their own words ("if a Claw walks into her line she shoots it when I press"); the first Watch press lands, or the second does; nobody asks "what just happened?" on enemy turn 1 of level 1; the player uses the words "Family Role" or understands Lucy's in the River without re-reading.
- *Failed:* the first Watch press is still missed and not understood, or the player can't explain why the arrow count dropped. Next lever, in order: the first-trigger framed beat (B6, new tech), then Encore locked if not already, then option D in Linda's level.
- *Watch also:* whether players stall in Lucy's level on turn 1 (alert Claws in reach), and whether sleeping Claws in Linda's level read as broken.

**For the classic fallback (not designed here):** C makes the onboarding teach in the same order as the classic M1 (a basics level, then Linda's level), and the retitled Watch page can be reused on `Level1-C1-2`. Option B's mechanism (FTP drained to 0 so roles can't pay) is a data-only way to keep Lucy's untaught follow-up quiet in the classic's John + Lucy first level, while roles still cost FTP. Worth a line in the coordinator's fallback recipe.

## Questions for THJ

**Q1. Reorder the Hearth to Lucy → Linda → John → Mark?**
- Context: today the first level carries ~19 new things and the first Family Role fires on the player's first enemy turn, ~2:15 in, explained by a panel read before they moved. Lucy's level has no Role, Synergy or Duo (she's alone) and shows a normal enemy turn.
- Options: (a) reorder (C); (b) keep Linda first and tidy her level (A); (c) mute Watch in Linda's level through FTP 0 (B); (d) add a basics stage to Linda's level (D, prefab edit, +0.75 min).
- Recommendation: (a). It costs no level edits and no time, and it moves the first-Role criterion from "by ~5 min" to "by ~6 min" (the design's acceptance criterion D-168 set; this changes it).
- Blocked: the wiring and test changes, the narrative hand-offs, the timed cold run's Hearth part.

**Q2. Name the first Role as a "Family Role" on Linda's panel?**
- Context: the Hearth never says "Family Role"; the panel says "Watch", the prompt "Activate Passive". The River and the Ridge panels already say "Lucy's Family Role" and "Mark's Family Role".
- Options: (a) title "Linda's Family Role" with one frame line ("Every Bergson has a Family Role that acts on the enemies' turn."); (b) title only, no extra line; (c) leave as "Watch".
- Recommendation: (a), wording by `miso-narrative`. It replaces text, adds no element.
- Blocked: the panel text in `HearthMemoryWiring.Linda.cs`.

**Q3. Keep Encore locked through Linda's memory segment?**
- Context: the cut-in unlocks two buttons at once (D-373). Encore's real first use is M2 route B (D-334); the Encore pulse (G3) still teaches it there. Without Encore, an empty quiver in the last stage is answered by pickups, and the stage cap ends the telling anyway.
- Options: (a) lock Encore for the segment, unlock only Explosive Arrow; (b) keep both (today).
- Recommendation: (a) for the timed run; easy to revert (one lock entry and one unlock list).
- Blocked: nothing else; can be decided after Q1.

**Q4 (information, no decision needed now).** The Role prompt says "Activate Passive" on every Role (FR-2), while panels say "Family Role". It is shared combat UI, so out of this plan. If the timed run shows the word confuses, it goes to its own small text change.

No game rule or `design/demo-spec.md` value changes in the recommendation. Option B would lean on the built 1-FTP role cost that the demo spec says goes away (roles free), which is one reason it isn't recommended.

## Docs to update (if approved)

- `plans/onboarding/2026-10-26-onboarding-levels.md` (designer): Hearth section order and hand-offs, segment headings ("Segment 1 · Lucy", "Segment 2 · Linda"; level prefab names unchanged), cues rows (panels), Hearth time table and the "Firsts" line (Role ≈ 6 min).
- `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` (designer): flow table rows 1–2 swapped; acceptance criterion "Role QTE within ~5 min" → "~6 min, after one plain enemy turn".
- `plans/onboarding/onboarding-narrative-draft.md` (`miso-narrative`): H0-4, the Lucy and Linda cutaways (C1-3, C2-1 to C2-3), Linda's start line, the Watch panel P1-1 retitle and frame line.
- `design/gdd/missions-structure.md`: when the pending Hearth row lands (levels plan's Docs list), it lists the new order.
- `decisions.md` (coordinator): Q1–Q3 answers. `tech/classic-fallback.md` (coordinator, once it exists): the reusable Watch page and the FTP-0 mute note.
- No GDD rule ID changes.

## Risks

- **Paper estimates.** Times and first-counts are cold-rate estimates from the plan, not a timed run; the order of magnitude (19 vs ~8) is the evidence, not the exact numbers.
- **Unaware in Linda's level** follows a level of awake Claws: watch in the run.
- **Hidden order dependencies** in the build (level display names, anything reading "first level of the Hearth"): to check when wiring; none found in the four wiring tools.
- **Narrative churn:** 4–6 placeholder lines change; the final narrative layer is last anyway.

## Gates

Design only. Build after THJ's answers: data, two wiring tools and tests on `thj/onboarding` (implementer), THJ plays the Hearth, then the timed cold run. Docs as listed above.
