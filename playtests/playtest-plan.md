# Home Playtest Plan

Updated 2026-10-15 (the Oct 14 run and the Oct 14–15 fixes folded in; details in `build-log.md`). Replaces `M9-Playtest-Plan.md` and `Batch-Playtest-Run-Plan.md`. Design: `design/m9-readability.md`. Current state and known issues: `status.md`.

Three parts:

- **Part 0, carried over from M8:** the batched checks from before M9, with the latest result.
- **Part A, verification run per M9 step:** functional checks with expected results. Claude can drive them in Cowork with computer use, or THJ runs them.
- **Part B, cold playtest:** watching someone new play. This is the real test of M9.

## Status at a glance

| Part | Status (Oct 15) |
| --- | --- |
| 0 (M8 carry-over) | Mostly done; open: (j), (k) FAIL, (m) replay on a gain, (n) node combat effects (Hide and Seek 1 verified) |
| A, step 1 | Done except 1.2 lone stargazer (Night 1 can't test it), 1.3 risk marking |
| A, step 2 | Done; 2.4 tint FAIL (cyan art can't turn red) |
| A, step 3 | Done except the diamond hover outline; 3.6 FAIL at Night (frames the roof) |
| A, step 4 | Done except Kevin's walk; 4.4 bark pace judged from the log; 4.6 the free family doesn't walk to the Door |
| A, step 5 | Done except the weapon on the rack (5.2) |
| A, step 6 | Done |
| B | Not run yet (needs a new participant) |

Open bugs are in `status.md` (Backlog) and `build-log.md`. Fixed Oct 15 (`849c318ab`, `2f828e662`): Dawn lines and the Weapon card lost on sortie days, the Kitchen forecast ignoring a morning batch, no card for recipes learned in the Study, Linda shown twice at Dawn, the FP gain effect playing at level load.

## Setup and rules (all parts)

- Unity 6000.3.4f1 with the project open. Play from `Scenes/PreloadScreen.unity` (playing the Home scene directly leaves `GameHandler` unloaded and some panels throw).
- Resetting the game save is fine when a check needs it; say so in the results (D-025). To restart a run without one, use "Start a new moon cycle" on the end screen or New Cycle in Sim Debug.
- Stop Play before any script edit. After a compile (Ctrl+R, about 60–80 s), check the Console; read the Editor log on disk for full stack traces.
- Run once before Part A, Play off: `Tools/Home/Build Demo Content`, `Tools/Home/Add Combat Tags`, `Tools/Home/Build House Traces`, `Tools/Home/Add Bond Locks`; then enter Play (the unlockable registry reloads).
- **Fast route to Day 7:** `Tools/Home/Sim Debug` → Skip prologue → Unlock the Picnic (test) → Run to next Dawn ×6 → Day 7: pick four, "Choose Goblin Queen's Warren with 4/4", Advance (Depart), "Win" in the Sortie section (or play the levels). Playing the tutorials from PreloadScreen does not reset the Home save.
- **Combat cheats:** K kills the hovered unit (hover its feet, about 20 px below the sprite centre, after clicking inside the Game view); **F11** on a hovered enemy kills its whole faction (was N+K). H heals. `[` −1 HP (Shift −10). `]` +1 AP. **F12 completes the objective** (was Numpad 6; wins the level on all but a few levels); wait until the level intro has ended before pressing it. Use it only to skip fights the check does not need.
- If the Claude desktop window takes keyboard focus, click the Unity toolbar before pressing keys. The edge of the Game view scrolls the Home camera (leave the cursor mid-screen after clicking a top-edge button).
- The Claude desktop window can sit over the top-right corner of the Game view: clicks there (a window's X, "Stand up") never reach Unity. Move the window before judging a button dead.
- **Sim Debug test tools:** "+5 (test)" per Bond pair, "Grant +5" materials, "Grant study item", "Grant dish (test)" (one portion of any recipe into the pantry), "Unlock the Picnic (test)".
- **Record results** as a dated section in `claude-handoff/build-log.md` titled "YYYY-MM-DD Playtest: <part, step or session>", with Verified / Not verified / Findings. Give each finding a severity:
  - **Blocker:** the player can't continue or can't understand the goal.
  - **Major:** the player misreads state or wastes a slot.
  - **Minor:** cosmetic.

## Run order

Cheapest first, one Unity session each.

1. **Sim Debug only, no combat:** Part A steps 1 (open rows), 2, 3 and 4. *Done Oct 13 (Run 1).*
2. **Day 7 route:** Part 0 (e), (f) Skip, (j), (m); Part A step 5 items 1–3, 6. *Done Oct 13 (Run 2); (e) Oct 14; (j) still open.*
3. **Combat:** Part 0 (d), (k), (l); Part A step 5 item 4 and step 6 items 1–4. F12 once the thing under test has been seen. *Done Oct 13 (Run 3 and leftovers).*
4. **Skill trees (n):** one unit at a time, then the family tab. Start with the Sidewinders question.
5. **New game from PreloadScreen:** Part A step 6 items 5–6 (staged unlocks, Home Guide) and Part 0 (h), the full demo run. Needs a fresh save: ask THJ first. *Done Oct 13 (fresh save, Day 1 → Queen on Day 7, cheats on).*
6. **Part B** with a new participant.

## Part 0: carried over from M8

| Check | Result (Oct 13) |
| --- | --- |
| (a) Report card hides under the Picnic card on Day 7 | PASS (Oct 5) |
| (b) Camera after "Start a new moon cycle" | PASS: frames the house overview, the War council shows |
| (c) K on the Goblin Queen, K on a player unit | PASS once the hover is on her feet; her telegraph tiles after death not re-checked |
| (d) "Returning home..." on Loss / mission-end close buttons | Never seen: Retreat, Return Home (Defeat) and the stats Close all load Home in under a second, so the label has no time to show; no dead button either way |
| (e) Stargaze report line | PASS (Oct 14): night lines, chart line and the Overnight recap |
| (f) Hold the Picnic | PASS after a win; Skip PASS (straight to the end screen); the hold is not remembered across a Play restart |
| (g) Queen's Chamber retry | PASS (Oct 5) |
| (h) Full demo run from PreloadScreen | Done Oct 13 with cheats (fresh save, tutorials, Day 1 → Queen on Day 7, end screen). Part B is the uncheated version |
| (i) Station window X button | Not a game bug: the Claude desktop window covered that corner; X and Escape work |
| (j) Main's idles inside the camera boundary | Not run |
| (k) Enemy-info panels | FAIL: hover or click shows only the HP bar |
| (l) Lucy's role in Rest and Upgrade rooms | PASS: no exception in the Warren Rest Room; with no enemy her follow-up has nothing to hit (expected) |
| (m) FP gain VFX on the HUD | Fixed Oct 15: `FPGainAnimation` saved inactive (it played at level load). Replay on a gain not seen: FP was at its cap |
| (n) Skill trees | Panel text and purchase work; the Bond Lv 2 duo is granted free and saved; purchases survive a Play restart (Oct 14); Hide and Seek 1 = 3 decoys (Oct 15). Other node combat effects still to check |

**(n) Skill trees in full.** Spec: `design/player-skill-trees.md`. Open the panel from the toolbar "Skill Trees (n SP)" button (or `Tools/Skill Trees/Open Upgrades Panel`). For every node:

- The panel shows the right title, description, cost and pip count, the tier gate (unit level 0/1/2/3) and the prerequisite lock (A→C, B→F).
- The effect changes in combat by the stated amount: Shield Dash range, Blink cooldown 1→0, Sidewinder count, Cyclone, Explosive and Fist Blitz damage, Heal, Shell, Taunt and Swap radius, Nature's Rhythm +1 AP, Atman Body.
- Signature abilities (Father's Resolve, Blink, Harmonic Slam, Command, Protective Shell) are hidden until bought, work after, and survive save and reload.
- Effect unlocks apply: Vulnerable, Weak (Slam, Command), Burn, Stun, Move as One.
- Family bonuses apply only while the owner is in the squad: John HP ×1.2, Lucy crit +10%, Mark evasion +5%.
- Family SP is earned at 1/2/3 SP spent; each family node works (Tempest Bloom, Marks-Sisters, John-Linda Dance, Hide and Seek, Sidewinder Blitz, Family Watchers radius 3→5, Head Start race cooldown 2→1, Catch & Return, Healing Marks).
- Synergies still fire: Command → Shield Dash, Papa's Shelter extra ember at max Sidewinders, Sisters' Rivalry (these three are also Bond-locked since M9 6b).
- Mark's and Toba's trees appear only after their unlock missions.
- If a tree suddenly looks empty (`ArgumentOutOfRangeException` in `UpgradeLevelBarUI`), restart Unity.

## Part A: verification run, per M9 step

Each check: what to do, then what should happen.

### Step 1: Forecast and no dead seats

1. **Empty Study.** Seat a reader with nothing on the desk. Expected: refused with "Nothing to read". *Verified.*
2. **Dead-seat table.** Full pantry, Workshop helper with no order, a capped Teacher, a lone Porch or Fireside seat, a lone stargazer with nothing to chart. Expected: each refused with its reason; a second reader on a 1-slot item shows "Bond only". A lone Porch, Fireside or Yard seat is allowed while planning and released when the slot starts. *Verified: full pantry, Workshop with no order, lone Porch / Fireside released at slot start, "Bond only" on a second reader (fixed Oct 13). Capped Teacher verified Oct 14. Open: lone stargazer (Night 1's lore-only Great Moon counts as chartable).*
3. **Experiment.** With ingredients, Experiment stays available and is marked as a risk; an unknown mix gives Mystery Stew. *Verified, except the risk marking (missing, Minor). Oct 15: Mary's badge now reads the morning ("won't cook: the morning's cooking fills the pantry").*
4. **Forecast vs result.** Note the forecast on three seated stations, run the slot, compare with the recap. Expected: they match. *Verified Oct 13 (Study, Yard, Homestead, Care matched the recap and the Dusk report).*
5. **Carry-over release.** Finish a Study item, go to the next Dawn. Expected: the reader is released with a report line. *Verified.*
6. **Care by day.** A Wounded character shows "Needs care" with one carer seat; a Morning carer goes to the patient, the badge reads "Recovers at Dawn", the seat closes. On the morning after a sortie Care is refused with "Already on the mend". *Verified Oct 13 (Toba tended John: recovered; the Care intro holds the moon).*
7. **Vigil and Toba.** On the sortie night, the Vigil seat accepts a carer, the chip changes from "Needs care" to "Tended", the carer walks to the bedside, the patient recovers at Dawn. Toba by day: recovery right after the slot. *Verified (Toba by day Oct 13, Vigil Oct 14).*
8. **Late order.** On Day 6 an order needing 2 Dawns shows its delivery Dawn and "Arrives after the full moon" and is still allowed. *Verified.*

### Step 2: Goal and calendar

1. **Calendar on Day 1.** Icons: a gourd on Day 2 (plot 1); stars on nights 2–3 (Hound), 3–4 (Lantern), 5–6 (Crown); clouds on nights 2, 4, 6 (only once the Omen is revealed); an X on Day 3 (Scout Post's last day); the Queen on Day 7. More than two events shows "+N"; hovering a day lists them all. Icons are one-letter placeholder badges (Q, X, D, R, O, *). *Verified Oct 13 (Day 1 badge is a blank square: Minor).*
2. **Moons stay readable.** Today's moon larger with a gold ring, past days dimmed, icons never cover a moon or overlap the neighbour's row. *Verified.*
3. **Dawn card.** "N nights remain" at each Dawn with the right number. *Verified after the fix (centred, "5 / 2 / 1 nights remain").*
4. **Little Moon and tint.** The Little Moon moves along its arc during the day (blind-tuned: adjust `HomeWorldMoons.DriveLittleArc`); the Great Moon is redder on Day 5 than Day 1. *Arc moves (Oct 14). Tint FAIL: `GreatTint` multiplies cyan art, so it only darkens.*
5. **Queen's Might.** Count the pips on Day 1, win Goblin Camp: one pip breaks and the hover list loses its line. *Verified (6 of 7 after Goblin Camp; 2 of 7 cut on the end screen).*
6. **Warren.** Same place every day (`WorldMapPanelUI.warrenOffset`, default 0, 230, scale 1.4), on screen and clear of the grid, with the countdown; its card shows the danger list and "Scouting run" while a thread stands. *Verified.*
7. **Mission cards.** Purpose tag first, "(only here)" on key items in the "Drops:" line, "Gone after tomorrow" on Scout Post on Day 2. *Verified, but the purpose tag comes after the description (Minor).*
8. **War council.** The Day 1 Dawn beat plays once, with John's and Mary's lines. *Verified after the fix (above the dock; holds the moon until "To work").*

Not built: the Dawn tick camera glide and sting, the Warren's own icon and corruption overlay, haul icons.

### Step 3: House state

1. **Glance test.** Without opening a window, name which stations are working, idle, blocked or ready; check against the windows. *Verified Oct 14.*
2. **Badges.** Seat pips match the seated count; the progress line matches the window ("Study 1/2", "Ready at Dawn", "Ripe tomorrow"). Badge Side (Bottom, Top, Right, Left, Custom) on a selected prop moves the badge. *Verified (Badge Side Oct 14).*
3. **Props.** Every station opens from its prop; the old screens never open; clicking the Great Moon never opens the room under it; the prologue veils the indicator and badge; hovering a diamond lights the prop outline. *Verified except the diamond hover outline. Badges and bubbles now hide under the map, skill trees and pause menu (fixed Oct 13).*
4. **Dock.** One button per room in cycle order, then Map; keys 1–9 and 0 glide the camera and open the window; locked rooms are disabled. *Verified.*
5. **Roster.** Chips show the station, Free, Hurt, Away, Picnic; dragging a portrait onto a dock button seats the character, or shows the refusal. *Verified (refusal reason fixed Oct 13).*
6. **Overview.** O or the first dock button frames the house with badges readable; the camera returns there at each phase change (not while a window, the map or a lapse is up). *FAIL (Oct 14, 3 of 3 nights): "Go into the night" frames the roof / Stargaze side.*
7. **Recap strip.** After a lapse, "Dawn to Noon" etc. with gained, spent, progressed and unlocked; after sleep, "Overnight" with the night's lines (no "Last night" card). Hides after 10 s, hover keeps it, the Recap tab reopens it. *Verified.*
8. **Mary, Ben and effects.** Mary slides to the stove when she will cook, Ben to his bench during an order, both go back when idle. During a lapse: smoke at the Kitchen, sparks at the Workshop, pages in the Study, dust in the Yard, leaves in the Homestead. *Verified; lapse effects spawn (Oct 14) but are small from the overview.*

### Step 4: Family presence

1. **Dawn and night.** At Dawn everyone starts in their bedroom and walks out when assigned; at night the unseated go to their rooms. *Verified.*
2. **No wandering.** During a slot the unseated stay at their spot (Linda her room, Mark his meditation corner, Lucy the hall, John the sofa, Toba the barnyard, Kevin the barnyard). *Verified Oct 14 (idle log).*
3. **Idles.** Nobody is on screen twice (idle plus avatar); an avatar hides while its idle plays and returns after; the Dusk table scene changes by day (Pray, WarReportWA1 from Day 4, WarReportCA3 from Day 6) with Mary and Ben leaving their spots; the war-report scene no longer plays by itself; the prologue still plays the old idles; the Strict Groups switch on the Idle Director changes group scenes. Watch the `[Home idles]` Console lines (Linda was seen twice once). *Dusk scenes by day verified (Pray, WarReportCA3 on Day 7); Linda shown twice at Dawn fixed Oct 15 (`HomeIdleDirector` re-hides claims).*
4. **Barks.** Over one day each trigger fires where it applies (phase start, assignment, result, idle, low pantry, days left, sortie result, Bond); no repeats within the cooldown; no `[PLACEHOLDER]` tag on screen; pace feels right (gap 5 s, idle after 45 s). `[Home barks]` lines in the Console. *Fire and log seen; wrong-speaker and repeat issues logged Oct 13 (Minor); pace from the log: idle lines every ~50 s, two lines alternating (Oct 14).*
5. **Kevin.** Only Homestead and Kitchen helper seats, both day slots; Free in the roster; refused elsewhere with the reason; never in a squad; no Bond; side-view avatar with a correct size, facing and walk. *Verified except the side-view walk.*
6. **Send-off.** With the Send-off window open, the family at home walks to the Door (the Wounded stay in bed); `JohnGate` plays when John goes; they walk back after. *Squad gathers with a bark and `JohnGate` (Oct 14); the free family at home stays put.*
7. **Names.** "Porch Break" and "Fireside Talk", each with a "Costs:" line. *Verified.*

### Step 5: Loud gains

1. **Headline cards.** Learn a recipe, reveal a mission, cut a thread on one day: cards at Dusk one at a time, each spoken by the right character, before the Dining Table; a reload does not replay them. *Thread-cut, Skill-point and Bond cards verified in order before the Dining Table; recipe and mission-reveal cards and no replay after reload verified Oct 14; Study recipes and the Weapon card on a sortie day fixed and verified Oct 15.*
2. **Traces.** Pantry shelf shows dishes, an upgraded weapon hangs on the rack, plots grow, the studied book lies on the desk. Nudge the anchors under "House Traces" if needed. *Placeholders verified Oct 14 (pantry, plot, desk); the sword on the rack still not clear.*
3. **Before → after.** After Kitchen T2, John reads "32 → 38 HP" and has 38 HP in a fight; with 5 Toughness points 35; both 42. Hovering a portrait opens the Family sheet with the per-source breakdown. *Verified Oct 13 (Run 2).*
4. **Combat banner.** A squad with Quickberry Tart on an Omen day: the "From Home" banner lists the meal and the Omen ("Unknown Omen in effect" if not revealed); units carry status tags; the turn-1 extra AP pip shows the food icon and "Quickberry Tart +1 AP". A non-Home mission shows no banner and no pip. *Verified Oct 13: banner lists the meal and the Omen (Hungry Moon now has a combat effect, so it shows); turn-1 pip shows "Quickberry Tart +1 AP" (placeholder tint, no icon yet) after THJ's AP fix and the turn-end countdown; back to 2 AP on turn 2.*
5. **SP badges.** A hero with unspent SP shows a blue "SP n" chip on the bubble and a count on the roster card; the chip or the toolbar "Skill Trees (n SP)" opens the panel (on its first hero); the Dining Table announces new points once per increase; spending drops the badges after closing; the toolbar fits its buttons. *Verified (chip, roster count, toolbar count; the toolbar button sometimes needs two clicks).*
6. **Squad return.** At Dusk the squad walks in from the Door, up to four loot lines rise over them, and their results lead the Dining Table card in gold. *Loot lines over the squad and gold results lead verified; the walk-in hidden behind the Dusk cards.*
7. **Console.** No errors from `InitializePartially` when the Family sheet or SP chips are used. *Verified.*

*Oct 13: all items checked in Play except those marked open.*

### Step 6: Bond and onboarding

1. **Linda–Toba lock.** The pair starts at 18/25, Toba's other pairs at 6. The duo is unavailable in combat until Bond L2 and works after. Seating the pair shows the preview ("Linda & Toba +5 Bond 22 → 27/45 → Lv 2: their duo, a Bond scene"); the roster hover shows each pair's bar and what the next level opens. *Verified.*
2. **Unlock moment.** Reach L2 at the Fireside: the scene plays at the next Dawn (the time button is not blocked) and the duo works in the next fight. A level-up by day plays at the next Dusk. The unlock survives save and reload; a new moon cycle locks it again. *Verified. Since Oct 13 Bond Lv 2 also learns the duo for free (no Family Skill Point); confirmed on a fresh save (log "Bond Lv 2 grants Healing Marks", saved).*
3. **Extra locks.** Linda–Lucy below L2: a kill gives no AP or ready attack (Sisters' Rivalry); at L2 it does. John–Mark below L2: no Shield Dash after Mark's Command; at L2 it works. Toba cannot pass by with another character until their pair reaches L1. The Dining Table says "<pair>: <ability> now works in combat". Check the combat log's synergy lines. *Verified Oct 13: Sisters' Rivalry off at Lv 1, on at Lv 2 (combat log line); Shield Dash QTE after Command at Lv 2; Dining Table lines for both pairs. Shield Dash below Lv 2 verified Oct 14 (combat log: no Shield Dash after Command at Lv 1).*
4. **Fireside payoff.** Seat a pair at the Fireside, send both on a sortie: the report names the boost (first duo free, first Family Role free, or FP cap +2). In combat it applies once. A pair that stays home keeps it; an ended sortie keeps nothing unspent; stopping Play mid-sortie and re-running gives it back. A level with a Masher Goblin shows one warning per Masher and no error. *Verified: first duo free, first Family Role free once (the second costs FP).*
5. **Staged unlocks** (compare with the cycle's `stagedUnlocks` off): *Verified Oct 13 on a fresh save (Day 1 Study hold, Night 1 Stargaze and Fireside, Day 2 Yard hold, first Wounded opens Care and Vigil with Toba's hold). "Open the workshop" refused on staged saves: fixed Oct 13.*
   - Day 1 Dawn: Study and Workshop open, introduced by Linda (balloon) and Ben (toast). The Study introduction holds the time button until something is on the desk.
   - Night 1: Stargaze and Fireside open (Mark, Mary), nothing forced.
   - Day 2 Dawn: the Yard opens, John introduces it, the time button is held until a lesson is seated. Closed rooms are veiled and refuse seats with a reason.
   - First Wounded: Care and Vigil open, Toba introduces Care, a carer seat is required before time moves on at Dawn or Noon. Nothing is held at Dusk.
6. **Home Guide.** The toolbar "Home Guide" lists Kitchen, Homestead and Porch at the start; the others appear after their introduction. The "?" in a station window opens its page (greyed out until unlocked). "Good at this" matches the affinities; "Opens" reads right. *Verified: pages appear after each introduction.*

## Part B: cold playtest

**Who:** someone who has never seen the Home system, ideally a tactics or management player. A new participant each session if possible.

**When:** now that step 6 is built: one session covering the prologue and a full week.

**Length:** the prologue, then Days 1–3 (60–75 minutes), or the full week.

**Build:** fresh progress from PreloadScreen, no Sim Debug window, cheats off unless a fight stalls.

### Protocol

- Tell them only: "This is a family tactics game. Play as you like and think aloud."
- Don't explain or point. If they are stuck for more than 2 minutes, give the smallest hint and log it as a finding.
- Log as you go:

| Time | Day / slot | What they tried | Confusion or misread | Quote |
| --- | --- | --- | --- | --- |
| | | | | |

- Count per Home day: time spent (target about 5 minutes), windows opened, seats the game refused, times they asked "what is this?".

### Questions at the end of Day 2 (core)

The pass works if they answer at least 4 of 5 correctly without looking around.

1. What happens at the full moon?
2. Why didn't you go to the Warren yet?
3. What is Lucy doing right now?
4. What will you have tomorrow morning?
5. Who would you send to the Study, and why?

### Follow-up questions

- What does the row of moons tell you?
- Who is free right now, and how can you tell?
- What did the family gain yesterday?
- What happens when someone gets hurt?
- Who in the family do you feel you know best so far, and why?
- Why are Linda and Toba spending time together?

### Reporting

A dated section "Playtest: cold playtest N" in `build-log.md` with the participant profile, the score on the five core questions, the per-day counts, and findings by severity. Map each finding to a section letter of the M9 design (A–I). Open questions for THJ at the end.
