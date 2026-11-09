# Onboarding first hour · narrative draft (placeholder grade)

Narrative agent, 2026-10-26. Step **A5** of `plans/onboarding/2026-10-25-onboarding-first-hour-workplan.md`. Design: `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` (D-168 to D-180). Branch `thj/onboarding`, scope `all`. Read-only on `miso/`; `glossary.md` unchanged (proposals at the end).

**Answered 2026-10-26 (D-234):** open questions 1–8 all as recommended (one year; Bloom is Mark's claim; Lucy's line at Toba in M4; Linda asks "Still counting?"; stone axe and leaf wrapper; "Dad"/"Father"; scoped barks later, level sequences in the greybox; Mark's line without Grandma). The glossary and lore rows still wait on THJ.

**Quiver folded in 2026-10-30 (D-331 to D-334).** M1-1 ended on her last arrow (D-331; superseded by D-384, now "Seven Claws. One arrow."); segment 1's Watch panel says each shot spends an arrow, and no other quiver panel (D-333); route B is Encore's first use, with Linda's line and cue (D-334, rows T11-B1 to T11-B4); the Ridge catch line is in as a proposal, with no AP refund anywhere (D-332). The other quiver beats wait in [Proposed quiver beats, THJ to pick](#proposed-quiver-beats-thj-to-pick). Source: `reports/onboarding-quiver-impact.md`.

**Grade (D-180).** Greybox text: one short line per beat, 2–4 for a cutaway, enough to play and time the flow. Every line here goes in as `[PLACEHOLDER] ` until THJ approves it. All of it is Tier 3 (story beats, lore). Where a line matters, options are given with the recommended one first.

**Binding rules used.** Margaret alive and hosting the Hearth (D-178). One narrator per memory segment, unreliable-narrator jokes; the mother's death is never joked about and the jokes stop there (D-171). Ryker is the only thread and is "she" (D-169). Q1: directed dialogue, no scenery narration, no line explains an objective. Forms of address follow the open proposal (Lucy: "Dad", Linda: "Father"; see open question 6).

**How to read.** IDs are for discussion only (handoff-side; never in the game repo).
- **Where** values: *Home scene* (real Home state, dialogue over an idle), *Cutaway* (dialogue over the painted hearth still between memory levels), *Interruption* (play freezes, camera shows the change, then resumes), *Level dialogue* (level start or end sequence, or a trigger tile), *Bark* (bark system; "scoped" means it must only play in that mission or level), *Framed beat* (first-trigger beat, D-175: pause, both avatars, two lines), *Map Table* (Home scene at the Map Table).
- **(off)** after a speaker: a voice from the hearth over the frozen memory, no portrait in the memory scene, or the teller's hearth portrait.

---

## Step 0 · Hearth open (Home state, `MargaretStoryNight` idle; Ryker lies by the fire)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| H0-1 | Margaret | A year tonight. Ryker, come by the fire. They're going to lie about you. | Home scene | **Key line.** A (rec.): sets the unreliable-narrator frame in Margaret's dry voice. B: "A year tonight since she came home. Who tells it first?" (plain, warmer). C: "Every year, a different story. Who's lying first?" (the game's joke stated up front). "A year" is a proposed fact (open question 1) |
| H0-2 | Lucy | Me! I saved her. | Home scene | |
| H0-3 | Linda | You were crying. | Home scene | |
| H0-4 | Margaret | Eldest first. Linda. | Home scene | Hand-off 1 → segment 1 |

## Step 1 · Memory, Linda's version (Linda alone, 3 Dark Claws + 4 revealed in a side room, D-384)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M1-1 | Linda (off) | Seven Claws. One arrow. | Level dialogue (end, the outro punchline) | Approved 2026-11-04 (D-384). A tall-tale brag over the reworked level: 3 Claws, then 4 more revealed in a side room (7 in all), and she can take those 4 with one Explosive Arrow. Lucy answers it in C1-1 ("That's not how it went!"). Options: `reports/linda-memory-punchline.md`. History: "Three Claws, one arrow." (first draft), then "The Caeldippo caves. Three Claws. My last arrow. That's the whole story." (D-331, 3-Claw level, superseded) |
| P1-1 | Panel | **Watch.** When an enemy ends its move in Linda's row or column, press [key] to shoot it. Each shot spends an arrow. | Level start, the Watch panel (second of the two segment 1 panels) | D-333. Ability text in the established voice, `[PLACEHOLDER]` until signed off. "[key]" is the QTE key glyph. No first-empty-quiver panel: arrows, pickup and Encore are taught through play |
| M1-2 | Linda | Walk into my line. | Bark (scoped: memory), first Watch QTE | The story beat for her Family Role's first use (S8, joke form). Doesn't count as seen (D-175) |
| M1-3 | Lucy (off) | They did *not* line up for you. | Interruption (on the first Watch trigger) | Freeze on the Claws standing in her row |
| M1-4 | Linda (off) | They were very polite Claws. | Interruption | Resume |

**Cutaway 1** (painted still, hand-off 2)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| C1-1 | Lucy | That's not how it went! | Cutaway | |
| C1-2 | Linda | That's exactly how it went. | Cutaway | |
| C1-3 | Margaret | Then you tell it, Lucy. | Cutaway | → segment 2 |

## Step 2 · Memory, Lucy's version (Lucy; Fire Embers, Cyclone)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M2-1 | Lucy (off) | So. I'm in the cave. Alone. Very brave. | Level dialogue (start) | |
| M2-2 | Lucy (off) | Then ten more! | Interruption (spawn on cue) | **Changed by THJ 2026-11-09 (D-457, built and played).** 10 Claws appear. Freeze, camera to the spawn points, `GUnitSpawn`. History: "And then more came. At least ten!" |
| M2-3 | Linda (off, at the hearth) | Two. | Interruption | **Changed by THJ 2026-11-09 (D-457).** 8 of the 10 fade out. History: "There were four." / "Three." |
| M2-4 | Lucy (off) | Four. | Interruption | **Changed by THJ 2026-11-09 (D-457).** 2 new Claws appear, then resume; the fight continues with 4 Claws. History: "*Ten.*" |
| M2-5 | Lucy | And the wind caught fire. Obviously. | Bark (scoped: memory), first Cyclone | Her story beat for Cyclone; her fire is "bigger" in her version |

**Cutaway 2**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| C2-1 | John | Ten? | Cutaway | |
| C2-2 | Lucy | At *least*. | Cutaway | |
| C2-3 | Margaret | Go on, John. Your turn to be modest. | Cutaway | → segment 3 |

## Step 3 · Memory, John's version (John, Linda, Lucy; Family Role → Wrath)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M3-1 | John (off) | Every Claw in that cave wanted my girls. Not one of them got them. | Level dialogue (start) | Frames the protect half of his loop without naming a mechanic |
| M3-2 | Lucy (off) | Dad, you were *behind* us. | Interruption (level start, after M3-1) | His joke: in his version he's always in front |
| M3-3 | John (off) | In front. Always in front. | Interruption | Resume |
| M3-4 | John | Not my girls. | Bark (scoped: memory), first John role QTE | Story beat for his Family Role |
| M3-5 | John | My turn. | Bark (scoped: memory), first Wrath-charged Shield Dash | The punish half |

**Sisters' bicker barks** (segment 3 only; enemy killed, ideally "killed an enemy the other sister damaged"; see open question 7)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M3-6 | Lucy | Mine! | Bark (scoped: segment 3) | |
| M3-7 | Linda | That one was mine. | Bark (scoped) | |
| M3-8 | Lucy | You aimed. I burned. Burning wins. | Bark (scoped) | |
| M3-9 | Linda | That's two. | Bark (scoped) | |
| M3-10 | Lucy | Three! | Bark (scoped) | |
| M3-11 | Linda | You can't count smoke. | Bark (scoped) | |

**Segment 3 end and Cutaway 3**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M3-12 | Lucy | Dad, who got the most? | Level dialogue (end) | The Sister's Rivalry **setup** |
| M3-13 | John | You both did. | Level dialogue (end) | **Key line** (design) |
| M3-14 | Lucy | I did. | Level dialogue (end) | Said together with M3-15 if the dialogue box allows two speakers; otherwise back to back |
| M3-15 | Linda | I did. | Level dialogue (end) | |
| C3-1 | Mark | You're all forgetting the best part. | Cutaway | Mark walks in late at the hearth too |
| C3-2 | Lucy | You weren't even there. | Cutaway | |
| C3-3 | Mark | I was there for the end. The end is the part that matters. | Cutaway | |
| C3-4 | Margaret | Sit, Mark. Tell it. | Cutaway | → segment 4 |

## Step 4 · Memory, Mark's version (all four; Atman's Focus, Continuous Attack, Chained Assault; Tempest Bloom once)

**History.** Not what plays today: see [Memory 4 as in the game](#memory-4-as-in-the-game-synced-2026-11-06).

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M4-1 | Mark (off) | Then I arrived. | Level dialogue, when Mark walks in (turn 1 or 2) | |
| M4-2 | Lucy (off) | Late. | Level dialogue | |
| M4-3 | Mark (off) | Exactly on time. | Level dialogue | |
| M4-4 | Mark | I closed my eyes. I didn't need them. | Bark (scoped: memory), first Atman's Focus | |
| M4-5 | Mark (off) | Lucy's fire, my fists. As we practiced. | Bark or interruption, first Chained Assault | Duo story beat |
| M4-6 | Lucy (off) | We never practiced that. | (same) | |
| M4-7 | Mark (off) | I practiced. You followed. | (same) | |
| M4-8 | Mark (off) | And Linda shot straight into Lucy's fire, and the whole cave bloomed. | Interruption (the one-off Tempest Bloom) | **Key beat.** The Bloom is Mark's claim, which sets up the later callback. See open question 2 |
| M4-9 | Linda (off) | Did I? | Interruption | |
| M4-10 | Mark (off) | In my version, you did. | Interruption | The last joke |

**The ending: cub saved, mother lost** (staged in-engine; no jokes from here, no interruptions)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M4-11 | Mark (off) | Then her mother came. | Level dialogue (staged) | Plain, short. Mark keeps his voice level; that is the tone shift |
| M4-12 | Mark (off) | She stood over the cub until the last Claw fell. | Level dialogue | |
| M4-13 | Mark (off) | She didn't get up again. | Level dialogue | |
| M4-14 | Lucy (off) | She saved her. We only carried her home. | Level dialogue | Lucy, the most attached, gives the credit away. Options: B (Linda): "That part, we all tell the same." |

## Memory 4 as in the game (synced 2026-11-06)

Narrative agent, branch `thj/onboarding`. THJ has finished tuning this level and **his text is the master**: this section records it word for word and in playback order. Sources: `Resources/Sequences/Hearth/Memory4Mark/*DialogNodeSequence.asset` and the objectives in `Content/Levels/Greybox/GB_m4-mark.prefab`. The assets carry no `[PLACEHOLDER] ` tags. Where an older table below disagrees, this one wins. IDs `THJ-n` and `OBJ-n` are new, for discussion only. The speaker column comes from each node's character; "(off)" keeps the draft's reading, since the assets don't mark it.

### Dialogue

| Plays in | ID | Speaker | Line in the game | Status against the rework draft |
|---|---|---|---|---|
| Intro (`Start`) | N1-1 | Mark (off) | Claws in every tunnel. And on the ledge, a wolf standing over her cub. | As drafted (option A) |
| Intro | N1-2 | Mark (off) | The family was there. Most of it. The best part was still on its way. | As drafted (option A) |
| Bloom cut-in, on John's gesture, before Lucy's Cyclone (`Bloom`) | THJ-1 | John | Lucy! Keep them busy! | **New, THJ's.** Replaces N1-3 "Lucy! Keep them in their hole!" |
| Bloom cut-in, after the Cyclone; Lucy then runs ahead | THJ-2 | Lucy | You deal with them. I'll save the cub. | **New, THJ's** |
| Bloom cut-in, last line before Linda's turn | N2-1 | John | Linda! Through her storm! | As drafted (option A). Now follows Lucy's line and run |
| Arrival, stage 1 complete (`Arrival`) | M4-8 | Mark (off) | And Linda shot straight into Lucy's fire, and the whole cave bloomed. | As drafted |
| Arrival | M4-9 | Linda (off) | Did I? | As drafted |
| Arrival | M4-10 | Mark (off) | In my version, you did. | As drafted |
| Arrival, after the post-Bloom reveal and scripted moves (`PostBloom`) | THJ-3 | John | We need to cut their reinforcements. | **New, THJ's** |
| Arrival, same beat; John then moves | THJ-4 | John | I'll make sure they stay in their hole. | **New, THJ's** |
| Arrival, on Mark's reveal | M4-1 | Mark (off) | And then I arrived. | As drafted |
| Arrival | M4-2 | Lucy (off) | Late. | As drafted |
| Arrival, last line before the reset; Mark is then selected | M4-3 | Mark (off) | Exactly on time. | As drafted |
| Hold, stage 2 complete (`Hold`) | N5-1 | John | I'll hold them off. You save them. | As drafted |
| Hold, after the reveal and the Duo unlock | M4-5 | Mark (off) | Lucy's fire, my fists. As we practiced. | As drafted |
| Hold | M4-6 | Lucy (off) | We never practiced that. | As drafted |
| Hold, last line | M4-7 | Mark (off) | I practiced. You followed. | As drafted |
| Outro, after the mother falls (`End`) | M4-11 | Mark (off) | She never left her cub. Not once. | As drafted (N7 option A) |
| Outro | M4-12 | Mark (off) | She held on until the last Claw fell. | As drafted (N7 option A) |
| Outro, after Lucy and Mark walk to the cub | M4-13 | Mark (off) | The cub cried out. | As drafted |
| Outro | M4-14 | Lucy (off) | She saved her. We only carried her home. | As drafted |
| Outro cutaway, over the hearth still | H5-1 | Narrator node | Margaret: Every one of you saved her. That's the only version I believe. | Words as drafted. "Margaret: " is part of the text, since no Margaret dialogue character exists |
| Outro cutaway | H5-2 | John | Ten Claws, Lucy. | As drafted. John, not Margaret: settles the speaker note under "Cutaway check" |
| Outro cutaway | H5-3 | Lucy | At least. | As drafted |

### Objectives

| Stage | ID | Text in the game | Replaces (the wiring tool's text, never in the draft's tables) |
|---|---|---|---|
| 1 (the Bloom) | none | Two objectives, both hidden and with no text | Unchanged |
| 2 (after the arrival) | OBJ-1 | John: Cut the reinforcement path. | "John: hold the den mouth." |
| 3 (after the hold) | OBJ-2 | Kill the dark claws near the cub. | "Save the cub." |
| 3 | OBJ-3 | Hold the den mouth with John. | "Turns left in the memory: {remaining_0}." |

Stage 2's second objective is hidden and has no text. The prefab also overrides a `factionStateObjectives` string, "Eliminate all enemies. {x} remaining."; whether it shows on screen in this level wasn't checked.

### No longer in the game

| ID | Old text | Now |
|---|---|---|
| N1-3 | Lucy! Keep them in their hole! | **Replaced** by THJ-1 "Lucy! Keep them busy!" The hole now appears in THJ-4 |
| M4-4 | I closed my eyes. I didn't need them. | **Not in the game, no replacement.** No match in the text, data or code files under `Assets/`, so this bark plays nowhere today; see flag 6 |
| Objective | John: hold the den mouth. | **Replaced** by OBJ-1 |
| Objective | Save the cub. | **Replaced** by OBJ-2 |
| Objective | Turns left in the memory: {remaining_0}. | **Replaced** by OBJ-3 |

### Flags for THJ (nothing changed for these)

1. **THJ-3 and OBJ-1 against the Q1 rule.** "We need to cut their reinforcements." states the objective shown at the start of stage 2; the draft's binding rule says no line explains an objective. "Reinforcements" is also a planner's word for a father under pressure. Keep as an exception, or relax the rule for this level?
2. **One cell, two names.** OBJ-1's "reinforcement path" and OBJ-3's "den mouth" point at the same tile. Neither term is in the glossary. Which is the player-facing one?
3. **"dark claws" in OBJ-2.** The glossary writes **Dark Claw**, capitalised, and every line here says "Claws". Lowercase is the one mismatch with the glossary.
4. **Objective format.** OBJ-1 uses "John: ..." and OBJ-3 "... with John." for the same unit. Intended difference?
5. **Margaret as text.** "Margaret: " sits in a Narrator node because she has no dialogue character, unlike John and Lucy beside her in the same cutaway. Also, H5-1 to H5-3 play only in this cutaway today, while Step 5 lists them as Home scene.
6. **M4-4's Atman's Focus bark.** Drop it, or keep it for later? Its row stays as a record until then.
7. **For the coordinator, not a text issue.** `HearthMemoryWiring.Mark.Sequences.cs` and `HearthMemoryWiring.Mark.cs` still hold the old N1-3 and objective strings, and don't build THJ-2 to THJ-4; `HearthMemoryMarkTests.Flow.cs` asserts the old strings. As read, running Wire Memory 4 (Mark) again would overwrite THJ's text. Not run or tested here.

## Memory 4 rework (D-398), draft for THJ

**History from here to "Old Step 4 lines, status".** Kept for its reasoning and options; the wording and order that play are in the section above.

Narrative agent, 2026-11-05. Source: `plans/onboarding/2026-11-05-m4-mark-rework.md` (beat list, "Lines needed", "Player experience"). **This section replaces the Step 4 tables above once THJ signs off**; until then the Step 4 rows stay as history. Every line goes in as `[PLACEHOLDER] ` until approved. Tier 3 throughout. Beat numbers are the plan's.

**Speakers.** "(off)" = a voice from the hearth over the memory (Mark is the teller). John and Lucy without "(off)" speak inside the memory, as in Step 3. Where a line matters, options are listed with the recommended one first.

### Opening (beat 0b)

| ID | Speaker | Line | Where it plays | Replaces / notes |
|---|---|---|---|---|
| N1-1 | Mark (off) | Claws in every tunnel. And on the ledge, a wolf standing over her cub. | Level dialogue, intro sequence, camera on the den then the ledge | **New.** Sets the den, the mother and the cub; no rule, no objective. **A (rec.)**: plain picture, lets the board do the rest. **B**: "Picture it. A den full of Claws, and one mother between them and her cub." (warmer, foreshadows her fall). **C**: "A cave full of Claws. One wolf, one cub, and nowhere to run." (more dread) |
| N1-2 | Mark (off) | The family was there. Most of it. The best part was still on its way. | Level dialogue, right after N1-1 | **New.** The boast that sets up "And then I arrived." **A (rec.)**: Mark claims the arrival before it happens. **B**: "Everyone was there. Well. Almost everyone." (drier; lets Lucy's "Late." do more). **C**: drop N1-2 and keep N1-1 alone if the intro runs long |
| N1-3 | John | Lucy! Keep them in their hole! | Level dialogue, just before `CastAbilitySequence` casts her Cyclone on 4,4 | **Replaced in the game by THJ's "Lucy! Keep them busy!" (THJ-1).** Original note: "Shut the den" in a father's shout, not an instruction to the player. **A (rec.)**: blunt and warm. **B**: "Lucy, shut the den!" (THJ's words, plainest). **C**: "Lucy! Give them a storm to sit in." (lighter, names her Cyclone without the word) |
| N2-1 | John | Linda! Through her storm! | Level dialogue, right after the Cyclone lands, still in the opening | **New.** Points her at the storm without naming a button; the layout leaves one lane anyway. **A (rec.)**: short, clear. **B**: "Linda. Thread it through the wind." (the archer's word; softer). Keep John on "storm/wind": Mark then retells it as "fire" in M4-8, which is the tall-tale gap (and echoes Lucy's "the wind caught fire", M2-5) |

### After the Bloom (beat 4, start of the arrival cut-in)

| ID | Speaker | Line | Where it plays | Replaces / notes |
|---|---|---|---|---|
| M4-8 | Mark (off) | And Linda shot straight into Lucy's fire, and the whole cave bloomed. | Arrival sequence, first line, over the split arrows | **Moved** from the opening interruption. **Fits better now**: it lands after the player's own shot, so the boast is about something they just did. Unchanged |
| M4-9 | Linda (off) | Did I? | Arrival sequence | **Moved**, unchanged. Still works when the player made the shot: Linda doubts it ever happened, which keeps open question 2 (the Bloom is Mark's claim) and the Yard callback ("It never happened." / "Yet.") |
| M4-10 | Mark (off) | In my version, you did. | Arrival sequence | **Moved**, unchanged. No longer "the last joke": the arrival and the Duo hint follow. Lucy runs to 9,3 after this line. **In the game:** Lucy already ran, to 8,3, in the Bloom cut-in; John's THJ-3 and THJ-4 follow this line |

### The arrival (beat 4, after Lucy's run and the reveal)

| ID | Speaker | Line | Where it plays | Replaces / notes |
|---|---|---|---|---|
| M4-1 | Mark (off) | And then I arrived. | Arrival sequence, on the `arrival` reveal, camera on Mark | **Replaces** "Then I arrived." (THJ's wording). Pays off N1-2. Fits: it plays the moment he appears |
| M4-2 | Lucy (off) | Late. | Arrival sequence | Unchanged. Lands harder now that the Bloom happened without him |
| M4-3 | Mark (off) | Exactly on time. | Arrival sequence, last line before the Reset and the fresh turn | Unchanged. Ends the cut-in over Mark's full AP bar (the plan's answer to "did I lose my turn?") |
| M4-4 | Mark | I closed my eyes. I didn't need them. | Bark (scoped: memory), first Atman's Focus | **Not in the game, no replacement (2026-11-06).** Original note: Unchanged. Most likely fires during his entrance chain |

### The hold (beat 7)

| ID | Speaker | Line | Where it plays | Replaces / notes |
|---|---|---|---|---|
| N5-1 | John | I'll hold them off. You save them. | Hold sequence, first line, John on 7,5 | **New, THJ's line, recommended as is.** "Them" means the mother and the cub, and only the cub survives: the line pays off quietly at the end. **Alt**: "Nothing gets past me. Go. Save them." (more of a shield; one beat longer) |
| M4-5 | Mark (off) | Lucy's fire, my fists. As we practiced. | Hold sequence, after the `top` reveal, before the Duo unlocks | **Moved** from "first Chained Assault bark" to the Duo hint. Fits: it names both halves (her fire, his fists) without naming a button, and the pulse on Lucy and Mark does the rest |
| M4-6 | Lucy (off) | We never practiced that. | Hold sequence | **Moved**, unchanged |
| M4-7 | Mark (off) | I practiced. You followed. | Hold sequence, last line, camera back | **Moved**, unchanged. The last joke of the memory now (D-171: none from the mother's fall on) |

### The ending (beat 9, outro; no jokes, no interruptions)

The mother falls on screen first (LSB `motherFalls`). Recommend a held camera, about one second of silence, before M4-11 (the plan's risk about the fast cutaway).

| ID | Speaker | Line | Where it plays | Replaces / notes |
|---|---|---|---|---|
| M4-11 | Mark (off) | She never left her cub. Not once. | Outro, after the fall, camera on the ledge | **Replaces** "Then her mother came." (she is on screen from the start now). Level voice, no boast; that is the tone shift. Options below |
| M4-12 | Mark (off) | She held on until the last Claw fell. | Outro, still on the ledge, before the walk | **Replaces** "She stood over the cub until the last Claw fell." Kept the old line's ending, since now it is literally what the player watched |
| M4-13 | Mark (off) | The cub cried out. | Outro, after Lucy reaches 8,9 and Mark 9,9 | **Replaces** "She didn't get up again." (the fall shows it; saying it after reads twice). The plan calls this line "the narrator's"; Mark is the narrator here |
| M4-14 | Lucy (off) | She saved her. We only carried her home. | Outro, last line before the fade | Unchanged |

N7 options for M4-11 / M4-12 (the ending's key lines):

- **A (rec.)**: "She never left her cub. Not once." / "She held on until the last Claw fell." Says what the player saw (she stood there all fight) and why she falls now. "Held on" hints she was already hurt, without adding a fact.
- **B**: "She'd stood over her cub the whole fight." / "When it was over, she lay down beside her." Gentler, no hint of wounds; the fall reads as exhaustion.
- **C**: "She was hurt long before we came." / "She waited until the last Claw fell." Explains the fall outright. **Adds a lore fact** (her wounds came before the family), so Tier 3 on its own.

### Cutaway check (unchanged)

"Ten Claws, Lucy." / "At least." (H5-2 / H5-3) still works, and better: Mark's telling now shows 13 placed Claws (6 in the den, 2 with Mark, 5 by the mother) plus the pool spawns, so Lucy's "at least ten" from M2 is backed by the next teller, and John's tease turns into a concession. "At least." becomes her win. **Speaker note:** this draft gives the line to **John** in the Home scene after Margaret's H5-1; the rework plan's beat 9 says "Margaret". I kept John (it answers his C2-1 "Ten?"). THJ to confirm. **Settled by the game (2026-11-06):** the asset gives the line to John, in the level's outro cutaway.

### Old Step 4 lines, status

| Old ID | Status in the rework |
|---|---|
| M4-1 | Reworded ("And then I arrived."), moved to the arrival cut-in after the Bloom |
| M4-2, M4-3 | Kept, same beat |
| M4-4 | Kept in this draft (first Atman's Focus bark). **Not in the game** as of 2026-11-06 |
| M4-5 to M4-7 | Kept, moved to the hold sequence as the Duo hint |
| M4-8 to M4-10 | Kept, moved from the opening to after the player's shot |
| M4-11, M4-12 | Rewritten (N7) |
| M4-13 | Replaced by "The cub cried out." |
| M4-14 | Kept |
| New | N1-1, N1-2, N1-3 (**replaced in the game** by THJ-1), N2-1, N5-1 |
| New in the game, THJ's | THJ-1 to THJ-4, OBJ-1 to OBJ-3 |

## Step 5 · Hearth close (Home state; `FirePlace` / `MoreFire`, then `WolfSitDoor`; night; morning)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| H5-1 | Margaret | Every one of you saved her. That's the only version I believe. | Home scene | Lets the warmth back in after the death, without a joke about it |
| H5-2 | John | Ten Claws, Lucy. | Home scene | The laughter beat |
| H5-3 | Lucy | At least. | Home scene | |
| H5-4 | Lucy | Ryker? Come back by the fire. | Home scene (`WolfSitDoor`) | Ryker stays by the door. **Built (placeholder text), `thj/bond-lite`** |
| H5-5 | Margaret | Let her sit. She remembers too. | Home scene | The only hint of why she leaves (drawn by her mother's memory). Night falls after this line. **Built (placeholder text), `thj/bond-lite`**: Narrator node, text "Margaret: Let her sit. She remembers too." |
| H5-5a | Narrator | The fire burned low. By morning, the door stood open. | Home scene, between H5-5 and H5-6 | **New bridge line (D-436). Built (placeholder text), `thj/bond-lite`.** Carries the night-to-morning skip, since Home can't change state mid-scene |
| H5-6 | Lucy | The door's open. Ryker's gone. | Home scene (morning, `FamilyDinnerSad` or `WolfSadSit` empty) | **Built (placeholder text), `thj/bond-lite`**, words unchanged (the optional trim to "Ryker's gone." was not taken) |
| H5-7 | Mark | I'm staying. Until she's home. | Home scene | Mark stays (D-172). **Built (placeholder text), `thj/bond-lite`** |

**As built on `thj/bond-lite`** (`HomeVisitsWiring.Hearth.cs`, `Hearth_Close_DialogNodeSequence.asset`): H5-4, H5-5, H5-5a, H5-6, H5-7 play at Home after the Hearth, then W6-1, then the World Map page (Step 6). H5-1 to H5-3 stay in the Memory 4 outro cutaway. Text source: `reports/bond-lite-fixes-text.md`.

## Step 6 · World map (two pins, both needed)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| W6-1 | John | Two go out, two stay. Someone's here when she comes back. | **As built:** Home dialogue right after H5-7, just before the World Map page (was: world map, on first open) | **Built (placeholder text), `thj/bond-lite`.** **Key line** ("searching in shifts"). A (rec.): John decides, as the father. B (Margaret): "Two of you out, two by the door. She'll come home to someone." C (Mark): "Two search, two wait. Waiting is also searching." Not an objective line: it's the family's rule, and the two pins say the rest |
| W6-2 | Lucy | The river. She always drinks there. | World map, The River pin hover/select | Proposed habit for Ryker (Miso, open question 1) |
| W6-3 | Linda | The ridge. She liked the wind up there. | World map, The Ridge pin hover/select | |

**World Map page. Built (placeholder text), `thj/bond-lite`** (`Resources/Tutorials/WorldMap_Tutorial.asset`). Plays at Home after W6-1, once per save.

| Field | Text |
|---|---|
| Title | World Map |
| Body | • Open the world map at the fireplace.<br>• Pick a pin to choose a mission: The River or The Ridge, in either order.<br>• Each mission takes two Bergsons. The other two stay home. |

## Step 7 · The River (John, Lucy)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| R7-1 | Lucy | Ryker! *Ryker!* | Level dialogue (start) | From the old M2, kept |
| R7-2 | Lucy | Her prints. I'd know them anywhere. | Level dialogue, clue trigger tile | Clue 1 |
| R7-3 | John | Blood. Not much. She was still walking. | Level dialogue, clue trigger | Clue 2. John worries out loud (every family member cares) |
| R7-4 | Lucy | That's her fur. Dad, she fought. | Level dialogue, clue trigger | Clue 3 (white fur) |
| R7-5 | John | One clean blow each. A stone axe. Someone fought for her. | Level dialogue, clue trigger on the dead Dark Claws | Clue 4. "Stone axe" matches Toba's Exquisite Stone Axe; John can't place it |
| R7-6 | John | Stand by me, little spark. | Bark (scoped), first time Lucy is next to John | Invites Papa's Shelter (highlighted). Lucy reply option: "I'm not little." |
| R7-7 | John | Lucy. If it gets hot, aim at me. | Level dialogue or bark, first Shield Up in this level | Invites Shield Flare (D-176: discovered, not taught) |
| R7-8 | Lucy | *At* you? | (same) | |
| R7-9 | John | Trust me. | (same) | |
| R7-10 | Lucy | Dad, you're counting mine, right? | Bark (scoped), on a Lucy kill | Running joke, River side |
| R7-11 | John | I'm counting Claws. | Bark (scoped) | |
| R7-12 | Lucy | Same thing. | Bark (scoped) | |
| R7-13 | Lucy | Someone was here with her. | Level dialogue (end) | Clue summary in her words, no objective |

**Framed first-trigger beats that can fall here** (real combat; the memory didn't count)

| ID | Speakers | Lines | Where | Notes |
|---|---|---|---|---|
| F-Lu | Lucy / John | "Right behind you, Dad." / "I can feel the heat." | Framed beat, Lucy's Family Role (follow-up) | Taught here (design) |
| F-Jo | John / Lucy | "Not while I'm here." / "Dad, I had it!" | Framed beat, John's Family Role, if it first fires here | If it first fires in M2 with Linda: "Not while I'm here." / "…Thank you, Father." |

## Step 8 · Home visit 1 (Workshop for the outgoing pair)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| V1-1 | Ben | You two are next? Hand them over. I'll be quick. | Home scene, Workshop | Preparing, not leisure. Works for either pair |
| V1-2a | Lucy | Mark. Tell Linda I got five. | Home scene (River done first; Mark leaving) | Go-between joke, order A |
| V1-3a | Mark | I'm not keeping score. | Home scene | |
| V1-4a | Lucy | Yes, you are. | Home scene | |
| V1-2b | Mark | Linda says to tell you she's ahead. | Home scene (Ridge done first; Lucy leaving) | Order B |
| V1-3b | Lucy | Tell her she's wrong. | Home scene | |
| V1-4b | Mark | I'm not keeping score. | Home scene | |

## Step 9 · The Ridge (Linda, Mark)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| G9-1 | Mark | A man's tracks. Deep. He was carrying something. | Level dialogue, clue trigger | Clue 1 |
| G9-2 | Linda | Healing herbs, crushed fresh. | Level dialogue, clue trigger | Clue 2 |
| G9-3 | Mark | Someone knew which ones to pick. | (same) | |
| G9-4 | Linda | A leaf wrapper. It still smells of salve. | Level dialogue, clue trigger | Clue 3 (poultice wrapper). Proposed: a leaf bound with grass (open question 5) |
| G9-5 | Mark | Whoever he is, he's tending something. | Level dialogue (end) | "Something", not "her": they don't know yet |
| G9-6 | Mark | Linda. Shoot at me. | Level dialogue or bark (scoped), first time Linda has a line on Mark from 2+ cells | Invites Catch & Return (open by default, D-177) |
| G9-7 | Linda | Gladly. | (same) | |
| G9-8 | Mark | From a distance. | (same) | |
| G9-8a | Mark / Linda | "Yours." / "Show-off." | Bark (scoped), first Catch & Return catch (the arrow lands back in her hands) | **Proposed** (THJ to approve). Mark's quiet show-off (D-291), Linda answers in kind. The catch returns the arrow to her quiver and that is all: no AP refund (D-332), so no "shot back" or "Return to Sender" wording |
| G9-9 | Linda | Tell Lucy I'm ahead. | Bark (scoped), on a Linda kill | **Key line** (design) |
| G9-10 | Mark | I'm not keeping score. | Bark (scoped) | |
| G9-11 | Linda | Yes, you are. | Bark (scoped) | |
| G9-12 | Mark | Six. | Bark (scoped), a later Linda kill | Pays off: he is keeping score. Order A variant (Mark carries Lucy's message): "Lucy says five." |

**Framed first-trigger beats that can fall here**

| ID | Speakers | Lines | Where | Notes |
|---|---|---|---|---|
| F-Ma | Mark / Linda | "No one touches her." / "I had it." … "I know." | Framed beat, Mark's Family Role (Linda hit, Mark answers) | Taught by Linda's fragility (design). Two lines if the frame holds only two: drop "I know." |
| F-Li | Linda / Mark | "Into my line." / "You've waited all day for that." | Framed beat, Linda's Family Role, first real trigger | |

## Step 10 · Home visit 2 (skill tree; Map Table clue scene; M2 pin)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| V2-1 | Linda | Next time, I don't miss. | Home scene, guided skill spend (Linda returned) | One line framing the spend, no explanation |
| V2-2 | Lucy | Next time, more fire. | Home scene, guided skill spend (Lucy returned) | |
| V2-3 | Lucy | Her prints, her blood, her fur. And Claws cut down with a stone axe. | Map Table | River clues |
| V2-4 | Mark | A man's tracks, deep. Carrying something. | Map Table | Ridge clues |
| V2-5 | Linda | And herbs. A poultice. | Map Table | |
| V2-6 | John | Someone's carrying her. And tending her. | Map Table | The two halves meet. Every family member speaks |
| V2-7 | Lucy | Then where is he taking her? | Map Table | The M2 pin appears on this line, silently (Q11 one-at-a-time reveal) |

**Skill Tree page. Built (placeholder text), `thj/bond-lite`** (`Resources/Tutorials/SkillTree_Tutorial.asset`, on the Grandma Table). Plays by itself on the first Home load where the Grandma Table is open (after River and Ridge), once per save.

| Field | Text |
|---|---|
| Title | Skill Tree |
| Body | • Bergsons earn skill points as they level up.<br>• Each Bergson has a tree. Spend points here to learn new skills.<br>• The Family tab opens later. |

## Step 11 · M2 · The Trail (Lucy, Linda + John or Mark)

**Squad pick (Map Table): the one left behind**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| S11-J | John | Go. I'll keep the fire lit and the door open. | Map Table, John stays | **Key line** (design). Option B: "I'll be here. Someone should be, when she comes home." |
| S11-M | Mark | I'll sit by the door. Someone calm should be here when she comes home. | Map Table, Mark stays | Option B: "Waiting is my part. I'm good at it." |

**Proposal 2026-11-09, waiting on THJ: why The Trail restarts the tally at 0 (pacing check P8; D-445, D-450). Chosen by narrative per THJ 2026-11-09, waiting on the line pass.** Nothing above or below is changed; these are new rows, none approved (tag `[PLACEHOLDER]` when built). THJ's steer: Linda is the one who wants to change the mood, Lucy (more attached to Ryker) keeps them on finding him; plain B was also acceptable.

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| **T11-0a** | Linda | Zero–zero. Rematch? | Level dialogue (start of *The Trail*, the reworked level; counter on screen at 0–0) | Linda reaches for the old joke to lift the mood. The tally is the reason she says it: the board reads 0–0 |
| **T11-0b** | Lucy | Later. Ryker first. | Level dialogue (same) | Lucy declines without ending the game: "Later", not "No". The counter keeps running, which is what the pile needs |
| T11-0c (optional) | Linda | …Counting anyway. | Level dialogue (same) | Only if testers don't read that the count continues. Drop it for urgency |

**Check against the pile.** T11-5 / T11-6 stay as they are: Linda asks "Still counting?", Lucy answers "…No." Lucy deferred the count at the start ("Later") and drops it at the pile, so her answer is the turn; Linda, who wanted the count, is the one who asks, as in open question 4 (a). No swap of speakers is needed (a swap would have Lucy ask about a count she postponed, and Linda let it go, which reverses the arc). One pre-existing note: T11-3 / "The rivalry barks stop from here" still holds, so the "Later" at the start is the last spoken sign of the joke before the pile.

**Slot.** The start of *The Trail* (`GB_m2-tracks` as reworked in [after-Hearth design](2026-11-09-onboarding-after-hearth-design.md) › M2, where the empty Trailhead is cut), in that level's start dialogue, using an existing dialogue slot and no new tech. Where the pick's stays-home line plays, put these after it. The tally is eligible in The Trail and shows at 0–0 there. Not checked in Unity: the implementer confirms the reworked level has a start dialogue and the HUD shows at its start. Fallback slot: the Map Table send-off, one extra pair after V2-7 (worse: it lands on "Then where is he taking her?").

**Rejected.** A "Stories don't count" (Lucy: "Fireside kills don't count. Grandma's stories, all of them." Linda: "Then start from zero. I'll still win."): Lucy's joke first reads as indifference to Ryker and drains the urgency. C "A stake" (Lucy: "Rematch. Loser carries the pack home." Linda: "You'll be carrying it."): same problem, and the pile has to undo the bet.
**THJ decides:** accept T11-0a/0b (with or without 0c); nothing else.

**Route choice and the pile**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| T11-1 | Lucy | Her blood. | Mission map, "follow the blood" node select | Optional flavour; node names are placeholders |
| T11-2 | Linda | His tracks. | Mission map, "follow the tracks" node select | |

**Route B "Follow the tracks": Encore's first use** (D-334; Linda's arrows land on the Archers' ledge, which nobody can reach)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| T11-B1 | Lucy | Your arrows are up there with them. | Bark (scoped: route B), first time a Linda arrow is grounded on the ledge | The cue: says the problem, not the answer. Option B: "Sis. Your arrows." (shorter, if the bark box is tight) |
| T11-B2 | Linda | Not for long. | (same) | Promises Encore without naming it |
| T11-B3 | Linda | Come home. | Bark (scoped: route B), first Encore cast | **Key line.** A (rec.): plain, and it carries the whole act (they are bringing Ryker home); it is already one of Encore's cast barks (`RecallLines`). B: "Back to me." (plain, no echo). C: "Once more, from the top." (the musician, matching the name Encore; lighter) |
| T11-B4 | (UI) | Encore button pulses when Linda has 0 arrows and grounded arrows exist | Route B, once | Cue, not text: the empty-quiver hint ("No arrows; walk over them or use Encore.") and Encore's final tooltip (D-327) do the teaching. Tech to check (pulse may not exist); fine to drop if T11-B1/B2 land |
| T11-3 | Lucy | Linda… what if she's in there? | Level dialogue (pile level start) | **Key beat.** The rivalry barks stop from here (scoped bark suppression cue) |
| T11-4 | Linda | Then we find her. Together. | Level dialogue | The turn: back to back |
| T11-5 | Linda | Still counting? | Level dialogue (end), tally fades on this line | **Key lines** (design). Linda asks, Lucy answers (open question 4) |
| T11-6 | Lucy | …No. | Level dialogue | |
| T11-7J | John | She's not here, Lucy. Her tracks go on. Down, to the Rootwell. | Level dialogue (end), John variant | Not an objective line: it's the relief and the next dread in one |
| T11-7M | Mark | She isn't among them. The tracks go down. Into the Rootwell. | Level dialogue (end), Mark variant | |
| T11-8 | Lucy | If he saved her, why didn't he bring her home? | Level dialogue (end) | **Lucy's M4 motive line**, placement A (open question 3) |

## Step 12 · Home visit 3 (Yard scene, night; Bond; first Family skill point)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| Y12-1 | Linda | It's past midnight. | Home scene, Yard (Lucy burning straw targets) | |
| Y12-2 | Lucy | Can't sleep. I keep seeing that pile. | Home scene | Coping, not training |
| Y12-3 | Lucy | If they've hurt her… | Home scene | **Key line** (design) |
| Y12-4 | Linda | Then we'll be ready. | Home scene | **Key line** (design). Linda picks up her bow |
| Y12-5 | Lucy | You pin it, I burn it? | Home scene, after the first race | They find setting each other up works better. **Built (placeholder text), `thj/bond-lite`** |
| Y12-6 | Linda | …That's faster. | Home scene | Bond level-up plays here. **Built (placeholder text), `thj/bond-lite`**: the Bond step runs right after this line |
| Bond | Narrator | Linda & Lucy's Bond reached Lv 2. | Home scene, right after the Bond step | **New (D-436). Built (placeholder text), `thj/bond-lite`** (`Yard_BondReached_DialogNodeSequence.asset`). Same shape as the locked-node line "Opens with Linda & Lucy's Bond, Lv 2" (glossary › Bond) |
| Y12-7 | Margaret | First thing you two have done together all year. | Home scene, from the porch | **Built (placeholder text), `thj/bond-lite`**: Narrator node, text "Margaret: First thing you two have done together all year." Grants the Family skill point (on screen "Family skill point", D-439; formerly "Family point" here) as a story reward (D-173). Option B: no Margaret; Linda: "Don't tell anyone." / Lucy: "Too late. Grandma's watching." |
| Y12-8 | Lucy / Linda | "Your turn, then mine." / "Then mine." | Family-tree choice, Sister's Rivalry card | Flavour line on the choice, after the rules text |
| Y12-9 | Lucy | Mark's story. The shot into my fire. | Family-tree choice, Tempest Bloom card | The callback to M4-8 |
| Y12-10 | Linda | It never happened. | (same) | |
| Y12-11 | Lucy | Yet. | (same) | |

**As built on `thj/bond-lite`** (`HomeVisitsWiring.cs`, `HomeVisitsWiring.Yard.cs`; The Trail's own Home state with Lucy training): camera focus on the yard, Y12-1 to Y12-6, Bond step, Bond line, Y12-7, Lucy's pointer line, pan back. Night lines kept. Y12-8 to Y12-11 not built. Flag (not changed): the pointer line says "The Family Skill Tree has room for the two of us now."; the glossary term is the Family tree (its Family tab), so "Family tree" may read cleaner. THJ's call.

## M4 send-off and M4

**Send-off (Map Table)**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| X-1 | Lucy | She's in the Rootwell. We're bringing her home. | Map Table, send-off | |
| X-2J / X-2M | John / Mark | We go together. / Together, then. | Map Table, whoever was picked | The one left home gets S11-J or S11-M again (repeat line) |

**Framed first triggers (real combat, D-175)**

| ID | Speakers | Lines | Where | Notes |
|---|---|---|---|---|
| F-SR | the sister who killed / the other | "Your turn." / "Watch this." | Framed beat, Sister's Rivalry first trigger | **Key lines** (design). Works in either order, same two lines |
| F-SR2 | Lucy / Linda | "Who got the last one?" / "We both did." | Level dialogue, end of that fight | The quiet callback to M3-13. Tally returns as flavour after this |
| F-TB | Lucy / Linda | "Remember that shot?" / "This time it's real." | Framed beat, Tempest Bloom first trigger | **Key lines** (callback to the memory's one-off shot) |
| F-TB2 | Lucy / Linda | "Don't tell Mark." / "He'll say he saw it." | Level dialogue, end of that fight | If Mark is in the squad, instead Mark: "I told you so." |

**Lucy's motive line, placement B** (if not at the end of M2): `Mission 4/Level1C3/Level1C3_End_DialogNodeSequence.asset`, replacing node 5 "How dare you steal our wolf?": Lucy: **"If you saved her, why didn't you bring her home?"** Toba's next line ("I didn't take her. She came willingly.") then answers her directly. With placement B, node 14 ("If we are not killing this thief…") becomes "Thief or not, Ryker is coming home with me." (old Q2-4 option A).

**John's key M4 lines, John and Mark versions** (D-172: John or Mark is in the M4 squad)

| Where | Current (John) | John version | Mark version | Lines that change with it |
|---|---|---|---|---|
| `Mission 4/Level1C3/Level1C3_End_DialogNodeSequence.asset` node 22 | Put Ryker down, Lucy. | Keep. Softer option (old Q2-1): "Lucy. Let her choose. We stay right beside her." | Set her down, Lucy. Let her choose. | Node 19, Linda: "Father... Ryker protected him." → "Mark… Ryker protected him."; node 20 narration "John looked at the wolf cub…" → "Mark looked…"; node 23 Lucy "Dad!" → "Mark!" |
| `Mission 4/Level2C2/Level2C2_EndDialogNodeSequence.asset` (after Linda "I will. Father?") | We came together. We continue together. | Keep | We came in together. We go on together. | Linda's "I will. Father?" → "I will. Mark?"; narration "John looked at the wounded hind…" → "Mark looked…" |
| `Mission 4/Level3C1/Level3C1_EndDialogNodeSequence.asset` | She stays at our house until we find a way. | Keep | She comes home with us. We'll find a way. | Option B (Mark): "She stays with us. Grandma will know what to do." Adds a lore hint about Margaret (open question 8) |

---

## Proposed quiver beats, THJ to pick

Not approved; none of these is in the scenes above. Each teaches pickup or the hand-back through play (D-333). Pick any, all or none.

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| Q-1 | Lucy (off) / Linda (off) | "And then?" / "And then I walked over and picked them up." | Level dialogue (end of segment 1) | M1 close: her deadpan teaches pickup, and the joke stays hers |
| Q-2 | John / Linda | "Dropped these." / "Thank you, Father." | Hand-back (scoped: segment 3), first time John's kill hands her arrows back (D-307) | Segment 3 hand-back: the protect half of his loop, in small. Only fires if his Wrath kill lands on her arrows (designer finding 4) |
| Q-3 | Lucy / Linda | "Here." / "Thanks." | Hand-back lines (scoped: the pile), replacing the teasing ones | The pile: the rivalry barks stop (T11-3), so the hand-backs go quiet too. Her quiver starts full there (LI-10), so this only plays if a sister picks one up |
| Q-4 | Lucy / Linda / Lucy | "You'll want this back." / "It's singed." / "It's *better*." | Home scene, Yard, after Y12-6 (Lucy hands back an arrow from a burnt straw target) | The Yard: the first friendly hand-back between them, before Margaret's line |

---

## Proposed glossary entries and lore facts (Tier 3, for THJ)

Nothing below is in `glossary.md` yet. "Approved" means a THJ decision already exists; I add it to the glossary once THJ says go.

| Entry | Proposed text | Status |
|---|---|---|
| **Margaret (Grandma)** | John's mother; alive in Miso's timeline; hosts the Hearth and hands the telling to each Bergson | Approved (D-178); glossary row pending. Her relation to John: from Children of Morta, THJ to confirm |
| **Ryker** | Lucy's wolf cub, "she". Saved in the Caeldippo caves; her mother died protecting her. Toba calls her Waya, the Fangmother (M4) | Proposed (Miso). Canon status of Ryker herself: THJ |
| **Caeldippo caves** | Where the family saved Ryker from Dark Claws | Design calls it canon; THJ to confirm |
| **The Hearth** | The prologue: the family's yearly retelling of Ryker's rescue; also the name of its Home state | Proposed term |
| **Ryker's night** (the anniversary) | One year since the rescue at the start of the game | Proposed fact (open question 1) |
| **The River, The Ridge, The Trail** | The two pair missions and M2 | Working titles from the design; confirm as player-facing names |
| **Searching in shifts** | While Ryker is missing, someone always stays home in case she comes back | Approved as design (D-172); the phrase is proposed |
| **Sisters' tally** | The HUD and results-screen kill count while both sisters are in the squad | Proposed UI term |
| **Toba's stone axe as the River clue** | The Claws at the river were killed by a stone axe; the family can't place it until M4 | Proposed (matches his Exquisite Stone Axe) |
| **The leaf wrapper** | Toba's poultices are wrapped in a leaf bound with grass | Proposed (Miso) |
| Ryker's habits | Drinks at the river; likes the wind on the ridge | Proposed, flavour only (W6-2, W6-3) |

## Open questions

1. **How long since the rescue?**
   - Context: H0-1 says "A year tonight". M4 still calls Ryker "the wolf cub", so the gap must be short.
   - Options: (a) one year; (b) unstated ("Ryker's night"); (c) a few years, which would mean changing M4's "cub".
   - Recommendation: (a). An anniversary is the reason for the Hearth.
   - Blocked meanwhile: H0-1 wording and the glossary's Ryker row. Nothing in the greybox.
2. **Is Tempest Bloom Mark's invention?**
   - Context: M4-8 to M4-10 make the memory's one-off Bloom Mark's generous claim ("In my version, you did"). That makes the Yard choice ("It never happened." / "Yet.") and the first trigger ("This time it's real.") pay off.
   - Options: (a) Mark's claim, which the sisters deny; (b) it really happened, and the callback is nostalgia ("Remember that shot?" / "Like at the caves.").
   - Recommendation: (a). It fits the unreliable-narrator frame and turns the unlock into a promise.
   - Blocked meanwhile: M4-8 to M4-10, Y12-9 to Y12-11, F-TB, F-TB2.
3. **Where does Lucy's motive line go?**
   - Context: "If he saved her, why didn't he bring her home?"
   - Options: (a) the end of M2, after the tracks lead to the Rootwell (T11-8); (b) M4's confrontation, aimed at Toba ("If you saved her, why didn't *you*…"), replacing "How dare you steal our wolf?"; (c) both, the second as an echo.
   - Recommendation: (b). Toba's "She came willingly" answers it in the very next node, and it removes the "thief" line's cruelty at the source. (a) is the fallback if M4's text can't change before the playtest.
   - Blocked meanwhile: T11-8, and M4 `Level1C3_End` nodes 5 and 14.
4. **Who asks "Still counting?"**
   - Options: (a) Linda asks, Lucy answers "…No."; (b) the reverse.
   - Recommendation: (a). Lucy started the count, so her letting it go is the turn.
   - Blocked meanwhile: T11-5 and T11-6. The greybox can use (a).
5. **Toba's traces: how specific?**
   - Context: R7-5 (stone axe) and G9-4 (leaf wrapper) give him a recognisable kit before M4. This is Miso lore.
   - Options: (a) stone axe and leaf wrapper as written; (b) generic ("an axe", "a wrapper"); (c) also show his mask or a carved token at the Ridge, which ties to the open mask question in `reports/narrative-q1-q2-proposals.md` (Decision 2b).
   - Recommendation: (a). It's concrete and pays off when he appears with the axe. (c) waits until the mask's reason is decided.
   - Blocked meanwhile: the wording of R7-5 and G9-4 only.
6. **Forms of address** (carried over, Decision 6 of the earlier report).
   - Context: this draft uses Lucy "Dad", Linda "Father", and both say "Grandma".
   - Options: (a) as written; (b) both say "Dad"; (c) both say "Father".
   - Recommendation: (a). It gives two voices in one word.
   - Blocked meanwhile: nothing (a find-and-replace later).
7. **Scoped barks** (tech, for the coordinator; Decision 9 of the earlier report is still open).
   - Context: the segment 3 bicker barks, the River and Ridge joke barks, the memory's first-use barks, and suppressing the rivalry barks at the pile all need barks limited to one mission or level, plus a "killed an enemy the other sister damaged" condition if it's wanted.
   - Options: (a) a mission or level filter on bark rows; (b) put these lines in `LevelSequenceTrigger`s and level sequences; (c) a per-level bark-set override.
   - Recommendation: (a). It's the smallest and reusable. For the greybox, (b) is fine.
   - Blocked meanwhile: none of the text. It decides where the lines are placed in B2 to B5.
8. **Mark's "She stays" line: mention Grandma?**
   - Options: (a) "She comes home with us. We'll find a way."; (b) "She stays with us. Grandma will know what to do." (hints that Margaret knows forest lore).
   - Recommendation: (a). (b) adds lore nobody has decided yet.
   - Blocked meanwhile: the Mark variant of that line only.

## What this answers or supersedes in `reports/narrative-q1-q2-proposals.md`

| Item there | Status after this draft |
|---|---|
| Q2-1 (Lucy and John share the concern) | **Superseded.** Its M1, M2 and M3 sequences are cut (D-169). The shared worry now lives in R7-3 and R7-5, W6-1, S11-J/M and the every-member Map Table scene. The optional softer "Put Ryker down" is carried into the M4 table above |
| Q2-2 (Ryker is "she") | **Answered** (D-169); this draft uses "she" throughout |
| Q2-3a (where the masked man is set up) | **Superseded** by the River and Ridge clues (unseen stranger: stone axe, deep tracks, poultice) |
| Q2-3b (why the mask), Q2-3c ("Masked Stranger" plate) | **Still open.** Unchanged; see open question 5 |
| Q2-4 ("If we are not killing this thief") | **Answered in part.** Motivated by the new motive line (open question 3); option A, "Thief or not…", kept as its pair |
| Q2-5 (why they go home after A Wolf's Blood) | **Superseded.** The mission is cut |
| Q2-6 (Margaret / M5 grandma line) | **Answered** by D-178 (alive, hosts). The M5 lines are moot (M5 cut). The glossary row is proposed above |
| Q2-7 (forest name) | **Still open.** This draft avoids naming the forest; The River and The Ridge stand in |
| Q1 M1/M2 slice and its S8 placements | **Superseded** (levels restructured). Reused here: the Rivalry kill-bark idea (now scoped to segment 3 and the pair missions). Dropped: the old bark "Still counting, Linda?", so T11-5 stays fresh |
| Decision 6 (forms of address) | **Still open** (open question 6) |
| Decision 9 (scoped barks, role-fired hook) | **Still open** (open question 7). The role-fired hook is now the first-trigger beat tech (A4b) |
