# M9 Readability Pass

2026-10-04 · Status: **final, approved by THJ for implementation as M9.** Written from THJ's first playtest notes on Home and the comment round on this tab (all threads resolved). The rule changes in "Demo Spec changes" go into the Demo Spec as each build step lands; everything else is presentation and goes in the Build Log. Repo files: `claude-handoff/design/m9-readability.md` (this design) and `claude-handoff/playtests/playtest-plan.md` (playtests).

## Why this pass

THJ's playtest found that Home works but does not communicate. Three root causes:

1. **Information is pulled, not pushed.** State lives in windows and cards; the house view shows only avatars and two-chip bubbles.
2. **Nothing on screen shows the future.** The sim knows when crops ripen, orders land, Omens fall and missions close, but none of it is visible. This causes the missing urgency, the failed chores, the missed order times and the "why not go to the dungeon now?" question.
3. **The family reads as a workforce.** The Porch queue, wandering, word chips and silent characters say "units waiting for jobs", not "a family getting ready together".

The line the UX must support: *a family gets ready, together, for a fight they can't avoid, and every day at home decides who they'll be when the full moon rises.*

## Principles

The screen answers three questions without a click: what are we trying to do and how close is the threat; what is everyone doing and what will it produce; what just changed.

- **The family is the interface.** Feedback comes from a character's mouth, position or animation before it comes from a panel.
- **Exaggerate.** Every meaningful gain gets a moment, a place in the house and a mention at dinner.
- **No dead seats.** A seat is offered only if it produces something. The Kitchen's Experiment is the one labelled risk.

## A. Goal and threat

- **Queen's Might (HUD).** Next to the moon strip, one pip per thread she still has. A cut thread breaks with a crack and a dinner reaction. Hovering lists what waits in the Warren today ("Reinforcement waves, Black Claw pack, Mountain Deev elite"), each line naming the mission that removes it.
- **Warren card.** The same list as a danger rating that drops as threads are cut. Early attempts stay allowed, labelled "Scouting run: you'll face her at full strength."
- **War council, Day 1 Dawn.** A short beat at the Map Table. John: "We're not ready. Every place on this map feeds her. Cut what we can before the full moon." Mary: "And we eat, train and look after each other while we do it."
- **Mission cards lead with why.** The first line is a purpose tag: *Weakens the Queen*, *Supplies* or *Secret*. Windowed missions get "Gone after tomorrow". A "Days left 5 · Open missions 6" line shows that not everything fits.
- **The Warren is pinned.** An authored, fixed map position; a large unique icon with a corruption glow; the moon countdown on its node.
- **Visible decay.** The Great Moon tints redder each day, Mountain Light shifts colder, and a corruption overlay around the Warren on the world map grows a step per day. Each Dawn a bark reports what the Queen did, framing the Omens as her doing.

## B. Time as a calendar

- **The moon strip is the calendar.** The seven Great Moon phases (top-left HUD, the deadline hand, not the Little Moon) carry event icons in a row under the moons: a gourd when a plot ripens, a sword when Ben delivers, a cloud on Omen nights, a star when a pattern is visible, an X on a mission's last day, the Queen on Day 7. A day shows up to two icons by priority (Queen and deadlines, closing missions, deliveries, ripening crops, star nights), then "+N"; hovering a day lists everything.

*(Sketch in the doc: Moon calendar sketch · Day 3, one event row under the strip.)*

The moons keep their size and phase shadow; the icon row sits under the strip (about 28 px), so it never covers a moon. Today's moon is larger with a gold ring; past days are dimmed. Icons in the sketch are placeholders.

- **"N nights remain" Dawn card** with the moon phase. It is the one piece of time text in the house (an exception to the M8 "no date text" decision), kept for now and easy to remove.
- **The Dawn tick is felt.** On the first two Dawns the camera glides to the moon, the phase shadow slides with a sound sting and the day's pip lights up; after that it plays in the HUD only.
- **The Little Moon travels** its arc across the sky over the day.
- **The lapse shows work:** chimney smoke while Mary cooks, sparks at Ben's bench, pages turning at the desk. Gain pops fly to where they go (resource bar, pantry shelf, character). A bell calls everyone to dinner at Dusk. At night only rooms with someone awake are lit.

## C. The house shows its own state

- **Station props are the stations.** The bench, bookshelf, stove and so on are the clickable stations with a hover outline; the invisible hotspots go. Placeholders where no prop exists: a training dummy (Yard), a telescope (roof), a sickbed (Care), the Map Table.
- **A badge above each station:** seat pips (●●○), a state icon (Working, Idle, Needs input, Ready, Blocked) and a progress line ("Study 1/2", "Ready at Dawn", "Ripe tomorrow").
- **Mary and Ben are visible workers.** Mary stands at the stove when she will cook ("Mary cooks 1 Gourd Omelette this afternoon"). Ben hammers while an order runs; without one his badge reads "Ben is idle. Place an order."
- **Navigation.** A station dock (buttons mirroring the badges; a click glides the camera there and opens the window; hotkeys 1–0). A roster strip (portraits with slot chips, "Free", Wounded or Away, a skill-point badge; drag a portrait onto a dock button to seat). An overview zoom (one key frames the whole house; the camera returns to it at each phase change).
- **Slot recap.** After each lapse a short strip lists what was gained, spent, progressed and unlocked, then collapses into the HUD. The Dusk report and the Dawn night recap use the same four groups.

## D. No dead seats, and Care

- **Forecast.** `HomeSimulation` resolves the next slot on a copy of the save, so every seat shows its result before you commit ("→ +1 progress, finishes this slot", "→ 3 Gourd Omelette", "→ nothing: no Hearty Gourd in stock"). The same forecast feeds the moon's Begin tooltip and the calendar icons.
- **Dead seats are disabled with a reason** (table below). A seat that only gives Bond says "Bond only". Carried-over assignments that became invalid overnight are released at Dawn with a bark ("Linda's free, the journal is finished").
- **Late Workshop orders** are allowed and warned: the order shows its delivery Dawn on the calendar and flags "Arrives after the full moon" when it is too late for the Warren.

| Station | Dead case | What the seat does instead |
| --- | --- | --- |
| Homestead | Tending with no planted plot, and the pen has no hens or feed | Seat disabled: "Nothing to tend"; planting is greyed with no seeds or no free plot |
| Homestead (Dawn) | Hens with no feed lay nothing | Warning on the pen badge and the calendar the day before: "Feed runs out: no eggs tomorrow" |
| Kitchen | Batch without the ingredients | Auto-switches to a recipe it can cook, or disabled if none |
| Kitchen | Pantry full (4, or 6 with Kitchen T2) | Seat disabled: "Pantry full"; Mary's badge says the same |
| Kitchen | Experiment with no ingredients in stock | Disabled; with ingredients it stays open as the labelled risk |
| Workshop | Helper on a day with no order placed that day | Disabled: "No order to speed up" (a helper only speeds an order placed the same day) |
| Study | Nothing on the desk, empty shelf, or item already finished | Disabled: "Nothing to read" |
| Study | Second reader when one slot of progress is left | Allowed, marked "Bond only" |
| Yard | Teacher with no Student, or Student with no Teacher | The lone seat is disabled until its partner is seated |
| Yard | The Teacher's lesson is at its cap (6 points at Yard T1) | That Teacher is disabled: "Lesson maxed, try another teacher" |
| Porch | One person assigned alone | Not offered without a partner (idle Porch Bond still applies) |
| Fireside | One person alone | Not offered |
| Stargaze | One watcher with nothing new to chart and no Omen tonight | Disabled; two watchers stay allowed, marked "Bond only" |
| Stargaze | A watcher other than Mark on a Crown-only night | Disabled for that watcher: "Only Mark can read the Crown" |
| Care | No one Wounded, or already tended today | No seat exists |
| Send-off | Empty pantry | The meal pick shows "No meal today" instead of an empty list |

**Care is one visit to the patient.**

- Wounded keeps today's rule: no sortie and no Yard, everything else allowed.
- A Wounded character gets a "Needs care" badge with one carer seat on their portrait and bubble. The carer goes to the patient wherever they are: at the desk, in the kitchen, or at the bedside at night ("Sit up with them", the old Vigil).
- One slot of care, in any slot, is enough: recovery at the next Dawn (with Toba, right after that slot). The badge then reads "Recovers at Dawn" and the seat closes.
- One carer tends every Wounded that slot; each carer–patient pair gains the Care Bond.
- Day and night give the same result at a different cost (a work slot or a night seat), and the seat says so.
- The badge and seat exist only while someone is hurt; the sickbed prop is where an unseated patient rests.

**Affinities are shown.** Picker tiles carry a star and a one-line talent ("★ Linda: plot grows 1 day faster"); each station window has a "Good at this" row. Keyed Study items stay a light puzzle: the key reader shows as "?" with the hint and is named after the first partial read.

## E. A family, not a workforce

- **Dawn starts in their rooms.** Everyone wakes where they slept and walks to their station when assigned; whoever is still in their room is free, and the roster strip says so. Dinner stays the one family meal.
- **People stay put.** The wander epoch goes. Unassigned characters take one personality spot for the whole slot: Linda plays violin in the garden, Mark meditates in the Yard, Lucy is on the roof, John chats at Ben's bench, Toba is with the hens. At night anyone without a night seat goes to their own room and the light goes out (needs bedroom anchors).
- **Home barks** on `HomeSpeech` (or the `BarkDialogueTable` CSV format). Triggers: phase start, assignment, result, idle, thread cut, Wounded, low pantry, days left, last mission won or lost, Bond gains and level-ups, new unlocks. Conditions: who is involved, current mood. Pacing: per-character lines, cooldowns, priority. Mood follows the moon (calm on Day 1, tense by Day 5). Barks also advise ("Mary: pantry's bare, who's helping me cook?"). About 60 placeholder lines to start.
- **Idles.** Inventory what MortaStory ships first: there are idles for everyone except Toba (not in CoM), solo and in groups. Solo idles become personality spots and station work; group idles play when two or more characters share a station, a spot or the Door. `HomeDayRunner` decides which set plays, instead of main's last-completed-mission rule (mind the two `HomeState` types). Toba uses combat art until he has idles.
- **Porch Break and Fireside Talk.** Renamed so day and night read from the name; each window has a "Costs:" line (a day work slot, or one of the two night seats).
- **Night seats choose between knowledge and closeness.** Stargazing keeps its +2 Bond for two watchers, plus charts and Omen reveals. The Fireside is the Bond night: +5 Bond, Bond level-up scenes play there, and the pair gets a small combat payoff for the next mission, one of three picked per pair (their first duo together is free; the first Family Role either of them uses is free; the family FP cap is +2), given only if both are in the squad. One person alone at the Fireside is not offered.

## F. Make gains loud

- **Three tiers.** Headline: a full card at Dusk, one at a time, spoken by the character involved, with a permanent trace in the house (recipe learned, mission revealed, thread cut, weapon delivered, upgrade active, Bond level, skill point earned). Progress: a pop and a badge update. Resources: pops that fly to the bar while the counter ticks.
- **Traces in the house:** dishes fill the pantry shelf, upgraded weapons hang on Ben's rack, crops grow in the plots, the book being read lies open on the desk.
- **Before → after on a person:** "John 32 → 35 HP", not "+2% max HP". A Family sheet in the roster strip breaks each stat down by source (Lessons, Kitchen T2, weapon).
- **Combat shows what Home gave.** A short "From Home" banner at level start lists the meal, the Omen ("Unknown Omen in effect" if unrevealed), Wounded at 50% and rations waiting. Each effect is also a status tag with a tooltip. The turn-1 extra AP pip carries the food icon with "Quickberry Tart +1 AP".
- **Skill trees come back.** SP badges on the portrait, avatar and room; the Dining Table announces it; the room (or the renamed Upgrades button) opens the tree.

## G. Bond with a purpose

- **Most family abilities are open from the start; a few are locked, each with a short, visible unlock.** Duos, combo synergies, pass-by and Family Roles are our USPs, so most are usable from the first fight.
- **Showcase lock: Linda–Toba.** Toba is the newcomer (not in CoM) and Linda–Toba is his only duo, locked until the pair reaches Bond L2. It starts close (about 18/25); the Picnic (+5 for every pair) is a catch-up. Toba's other pairs start lower (about 5–8), so the roster shows he is new. Mark's duos are open. The Toba–Mark duo is dropped.
- **One or two more locks** (THJ picks, see Still open), for example Sister's Rivalry opened by a Bond level on Linda–Lucy, or a Family Role or pass-by upgrade opened by a pair's first level-up.
- When a lock opens, its scene plays at the Fireside that night (or at the next Dusk if it was earned by day).
- **Bond progress is visible:** seating a pair shows "+5 Bond · Linda & Toba 18/25 → their duo"; the roster hover shows each pair's bar and what it unlocks.

## H. Introducing each function

Each introduction: the owner says 2–3 lines, the prop is highlighted, the player does it once, and a Home Guide page unlocks (what it does, what it uses and makes, who is good at it). Stations open when they become useful:

| Moment | Function | Introduced by | First action |
| --- | --- | --- | --- |
| Prologue (as now) | Dining Table, Map Table, Kitchen, Homestead, Porch, Bond | — | As built |
| Day 1 Dawn | War council (the goal), Study | John, Linda | Put the Old Map Fragment on the desk |
| Day 1 Dawn | Workshop | Ben | Look at an order (no purchase forced) |
| Night 1 | Stargaze, Fireside | Mark, Mary | Watch the lore night |
| Day 2 Dawn | Yard | John | Seat a lesson |
| First Wounded | Care | Toba | Seat a carer |
| First SP earned | Personal room and tree | The character | Spend it |

## I. Missions worth it, home keeps running

- **Missions show their haul** up front as icons with counts (gold, materials, key items, XP, the thread cut), with "Only here" on key items.
- **The squad comes home at Dusk carrying it:** they walk in through the Door, the loot flies into the stores, their results lead the Dining Table, and XP and skill points show on their portraits.
- **Home keeps running on sortie days:** the stay-home crew, Mary and Ben work through a normal lapse.
- **Kevin** joins as an assignable, home-only worker: Homestead and Kitchen helper seats, both day slots, base effect, no talents, no Bond, never on a sortie. He takes chores so the fighters can train, study, bond or go out. Balance: +2 chore seats a day (a sortie day keeps 6 of 12 seats at home instead of 4 of 10); worst case about +14 crop yield a week, limited in effect by the pantry cap; gold and materials unchanged. Joey is dropped.
- **The night recap folds into Dawn:** night results pop at night (roof, Fireside, bedside); the old "Last night" card becomes the Dawn recap strip; new charts and revealed Omens land on the calendar and the map.
- **The Send-off is a scene** using the see-off idles: the family gathers at the Door, Mary hands over the meal, a stay-home character says a line, the squad walks out. The mission preview stays in the window.
- **Balance check:** compare a full home day and a sortie day in the sim, so a sortie is clearly worth more than staying in.

## Demo Spec changes (approved)

Apply each to the Demo Spec when the step that builds it lands:

| Change | Demo Spec section | Step |
| --- | --- | --- |
| Late Workshop orders are allowed and warned (closes the open question) | Workshop rules; Open questions | 1 |
| Care is one visit attached to the patient, in any slot; one carer tends every Wounded; the seat closes after one slot. The Wounded rule itself is unchanged | Dungeon and Wounded (Wounded); Night (Vigil) | 1 |
| The Warren has a fixed map node | Missions | 2 |
| Porch and Hearth are named Porch Break and Fireside Talk | Bond; Night | 4 |
| Kevin: assignable home-only chore worker (Homestead, Kitchen helper), both day slots, no Bond, no sortie | Roster; Homestead and Kitchen | 4 |
| The Fireside hosts Bond level-up scenes and gives the pair a small combat payoff next mission; no lone Fireside seat | Night; Bond | 6 |
| Showcase pair is Linda–Toba (existing duo, locked until Bond L2, starts about 18); Toba's other pairs start about 5–8; Toba–Mark dropped | Bond; Open questions | 6 |
| Station unlocks are staggered: Study and Workshop on Day 1, Yard on Day 2, Care on the first Wounded | Prologue rules | 6 |
| The Picnic keeps its Family Skill Point for now | Family Event (no change yet) | — |

## Build plan (M9)

Before M9: the batched Play pass from the handoff (items a–n) as planned. The 24 placeholder lines wait for step 4, where barks and scenes are written together.

**Status (Oct 14).** All six steps are built and committed (1a to 6d-2, the Home Guide last), each with its Demo Spec edits applied; details per step are in the Build Log. EditMode on Oct 13: 437 run, 436 pass (the AI baseline red). Part A of the playtest was run on Oct 13 and its fixes are committed; the open checks and the Part B cold playtest are in `claude-handoff/playtests/playtest-plan.md`.

1. **Forecast and no dead seats.** Sim dry-run and seat forecasts; disabled seats with reasons (the table in D); Dawn release of invalid carry-overs; Care as a patient visit; the late-order warning. Done when every row of the D table has an edit-mode test and a forecast matches the real resolve for a full test day.
2. **Goal and calendar.** Queen's Might, the moon-strip event row and hover, the "N nights remain" card, the Dawn tick, the Little Moon arc, the moon tint, the Warren's fixed node and card, "why go" mission cards with their haul, the war council beat. Done when a new player can answer "why not the Warren yet?" from the screen alone.
3. **House state.** Prop markers and badges, Mary and Ben at work, the station dock, roster strip, overview zoom, slot recap, the night recap at Dawn, lapse work effects. Done when one glance at the house tells which stations are working, idle, blocked or ready.
4. **Family presence.** Waking in rooms, personality spots, bedrooms at night, the Home bark table (about 60 placeholder lines, plus the 24 existing ones), the idle inventory and wiring, Kevin, the Send-off scene, the Porch Break and Fireside Talk names. Done when there is no queue at Dawn, no wandering, and characters speak on the listed triggers.
5. **Loud gains.** Tiered Dusk cards, traces in the house, before→after stats and the Family sheet, the combat "From Home" banner and tags, the turn-1 AP pip, SP badges and the route to the trees, the squad's return at Dusk. Done when every gain in a test day is visible at the moment, in the house and at dinner.
6. **Bond and onboarding.** The Linda–Toba lock and the chosen extra locks, Bond previews, Fireside scenes and payoff, staged introductions, the Home Guide. Done when the Linda–Toba duo can be unlocked in a normal week and each station is introduced by its owner when it first matters.

After steps 2 and 4, a cold playtest with someone new (see the playtest plan).

## Still open

- **Family growth:** how Family level and FSP are earned. THJ's idea: a hidden family level fed by pair Bond level-ups (for example 3 for level 2, 7 for level 3); FSP from family levels, special occasions (such as the Picnic) and personal skill-tree milestones; a pair's Bond levels make that pair's duo, synergies, pass-by and bonuses available, a few granted outright. A 7-day demo gives maybe 3–5 Bond level-ups, so the family tree (9 nodes, 15 FSP) needs a demo-sized slice.
- **Extra locks (decided 2026-10-12):** Sisters' Rivalry (Linda–Lucy Bond Lv 2) and John's Command Shield Dash after Mark's Command (John–Mark Bond Lv 2); Pass-By opens at Bond Lv 1 for every pair, so only Toba's pairs earn it. Linda–Toba duo at Lv 2. A later pass may shift every lock one level higher and grant Lv 1 and Pass-By in the prologue for theatrical purposes.
- **Fireside payoff, what else can be rewarded:** decide what other rewards the Fireside (or a Bond level) can give a pair. Examples: a paired-ability efficiency bonus (Toba with someone: Toba heals that person more during the next sortie; John with someone: John takes less damage during his Family Role for that person), a duo that hits harder, an extra pass-by effect. Today only three exist: first duo free, first Family Role free, FP cap +2.
- **Numbers to tune with the sim:** the Linda–Toba start (18/25), Toba's other pairs (6), the Fireside payoff (free vs 1 less FP, the FP cap bonus of 2), Kevin's yield.
- **Assets from THJ:** Kevin's side sprite, Idle and Walk (Run optional); station prop placeholders where none exist.
