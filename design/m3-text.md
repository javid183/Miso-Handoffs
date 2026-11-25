# M3 "Hold the yard": lines

Owner: miso-narrative. Scope `thj/onboarding-demo`. Written 2026-11-25 for the approved M3 paper level (D-688 to D-690; plan `plans/2026-11-22-onboarding-d3-paper-levels.md` › M3, stages S1 to S4; tech plan `plans/2026-11-25-onboarding-m3-greybox-tech.md` 6.1 and 6.4).
Status: **proposed, waiting on THJ.** Every line here is Tier 3 until he approves it. The one beat already written and kept as is: **"Still counting?" / "…No."** (D-624).

How to paste (same rules as `m1-ridge-redesign-text.md` and `m4-text.md`):
- **Dialogue** (`DialogNodeSequence`, `Line(Who.X, Side.Y, "...")`): paste **without** a tag. Dialogue shows `[PLACEHOLDER]` and the onboarding tests forbid it (`conventions.md` › Text). This file is the placeholder list until THJ signs off.
- **Barks** (CSV rows): keep the `[PLACEHOLDER] ` prefix; the bark system strips it. Rows for the tally barks are in §4; the arrival lines (§3.1) can be a dialog or the same text as barks, the builder's choice.
- **Rec.** is the line to paste; alternatives are for THJ, one line on the feel of each.
- **Sides** are not fixed (no M3 wiring yet). Suggested, to match M4: Linda Right, Lucy Left, Toba Left, the pick Right. The implementer may swap.
- Lines stay under about 55 characters so they fit a bubble.

Cast, as fixed: **Linda, Lucy + one pick, John or Mark.** Toba appears only at the end. Lines for the pick come in a **John (J)** and a **Mark (M)** version. The sisters' lines never depend on the pick, so cutting every pick line loses nothing but the stone's commentary.

Voice (as in M1 and M4):
- **Linda:** older sister, quick, proud, dry. **Lucy:** the youngest, fierce and open; short lines. Between them: a race, not a quarrel. They tease; they don't wound. The race **ends** at the last line of the level ("Still counting?" / "…No."), and M4's first Duo ("Together this time, Lucy." / "No counting.") pays it off. So the barks here keep the rivalry bright, and never mean.
- **John:** warm, steady, few words. **Mark:** calm, clipped, a dry streak.
- **Toba:** the newcomer, a healer; gentle, plain, unhurried; short sentences, no jokes, speaks of the forest as a living thing. He is a stranger being slowly trusted.

Terms (glossary): **Dark Claws**, **Masher Goblin** (the enemy's name; the on-screen close-up shows the name only, EN-10), **Rootwell**, **Ryker** (she). The stone is called **the stone** in lines (the unit's placeholder title is "Stone"). No line says "wall", "barrier" or "they break" (D-689). "Wounded" and "Bloodied" are not used.

Canon I did **not** touch (the M4 file's §5 questions stay open): who or what Ryker is, why Toba hid in the cave, whether Toba carried or tended Ryker, how he knows her. §5 below says "Ryker" and "she" only, as every screen line already does.

---

## 0. Level start: the Masher (optional)

Order: level start, input off → camera on the Masher (the close-up shows its name, EN-10) → one line → camera back → input on. The close-up needs no text from me; this is the optional spoken line.

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 0.1 | Linda | Masher close-up | That one hits back. Keep your distance. | A: "Big one. Don't stand next to it." (the rule, plain). B: "Lucy. Not too close." (shortest; her to Lucy). **Rec.** teaches the Masher's rule in a sister's voice. Linda gives it, not the pick: the pick is not on screen yet in the story sense, the sisters are the ones fighting | Placeholder |
| 0.2 | The pick (J) | Same dialog, optional | John: Stay behind me. | John: "I'll take the front. You two keep your distance." Alt: "Stay behind me." fits his Shield Up | Placeholder |
| 0.2 | The pick (M) | Same | Mark: Mind the distance. Then strike. | Mark: "Mind before fist." (his motto, too stock). Alt: "Range first. Then strike." | Placeholder |

Cut 0.2 first if the opening runs long. 0.1 alone is enough.

---

## 1. S1 complete: the cave behind the stone

Order: the Masher and two Claws dead → input off, camera on the stone (5,8) → the pick's line → camera back, **S2 objective "{Pick}: push the stone."** shows. Plan placeholder: "There's a cave behind that stone." Kept as the base so the stone's purpose is told in one line.

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 1.1 | The pick (J) | S1 complete, camera on the stone | John: There's a cave behind that stone. I'll move it. | A: "A cave. Someone's inside. I'll move the stone." (hints a person; the reveal at the end is a person, so it's a fair plant, but it commits that someone is there). B: "There's a cave behind that stone. Give me time." (shorter, leaves out the job) | Placeholder |
| 1.1 | The pick (M) | Same | Mark: A cave behind that stone. I'll shift it. | A: "A cave behind the stone. Hold the yard; I'll shift it." (Mark gives the order himself, but then 2.1 repeats it). B: "There's a cave. Something's hidden there." (more dread, less plain) | Placeholder |

Notes:
- The line tells the player **why** the pick walks away from the fight: the stone needs moving. "I'll move it" is the job; the push mechanic ("while he stands at the stone, it moves; if he leaves, it stops", D-608) is the **objective's** to teach, not the line's.
- If THJ wants the herb link from M1 (the Ridge's tracks and salve), option for either pick: **"Herbs, drying at the edge. Someone's in there."** It ties the stone to the Ridge's clue. It also tells the player a person is in the cave before the reveal, and tells them Toba is the tracker. That is a canon-adjacent hint (see M4 §5 Q5), so it is **not** the Rec. THJ's call.

Lines to paste:

```csharp
Line(Who.John, Side.Right, "There's a cave behind that stone. I'll move it."),
Line(Who.Mark, Side.Right, "A cave behind that stone. I'll shift it."),
```

(Only one plays: the one for whoever was picked.)

---

## 2. S2 complete: wave 1 arrives (S2: the pick reached 5,7)

Order (the Trail's arrival pattern, plan Cues): input off → camera on the west lane (0,0 and 1,0) → `w1` revealed → the sister's bark → camera back → S3a objective **"Hold them off (1/3)."** → input on. **A sister speaks here**, so it works for John or Mark.

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 2.1 | Linda | w1 revealed | Keep them off him, Lucy! | A: "Keep them off him!" (the plan's line, shorter; fine on its own). B: "Here they come! Keep them off him!" (adds the arrival). **Rec.** adds her sister's name, because the next line is Lucy's | Placeholder |
| 2.2 | Lucy | Same dialog, optional | And keep count, sister. | A: "Mine, mostly." (shorter, cockier). B: "Don't fall behind." **Rec.** reminds the player of the race the tally HUD is showing, without bragging. One line each, no more: a fight is on | Placeholder |

The pick says nothing here; he is at the stone, and 3.3 is his voice during the hold.

```csharp
Line(Who.Linda, Side.Right, "Keep them off him, Lucy!"),
Line(Who.Lucy, Side.Left, "And keep count, sister."),
```

Cut 2.2 and the arrival still reads: Linda's line alone is the plan's cue.

---

## 3. The hold: waves w2 and w3, and the stone's notches

Each wave plays the Trail's arrival pattern: input off → camera on the lane → reveal → bark → camera back → input. Each bark is one line from a sister, never both (the plan's turn rhythm). The notch lines are the pick's, **optional**, non-blocking bubbles if the bubble system allows it, as the hand-back does.

### 3.1 Arrival barks

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 3.1 | Lucy | w2 revealed (after S3a: three Claws, east lane) | Three more from the east! Mine! | A: "Three on my side. Easy." B: "More! Good." (shortest). **Rec.** claims the lane: the rivalry starts here, with Lucy taking the lane Linda doesn't have. If they are both on one side at that moment (the paper warns about it) the "mine" is only bravado, which suits her | Placeholder |
| 3.2 | Linda | w3 revealed (after S3b: Claws from both lanes, 0,2 and 10,2) | Both lanes at once. Try to keep up. | A: "Both lanes! Lucy, split with me!" (an order, less teasing, tells the player the answer: split the fronts). B: "Both lanes. Is that all?" (bravado). **Rec.** is a challenge: the last wave is when the race is closest. The hint "split" is the plan's ★, and it is shown by the lanes themselves | Placeholder |

### 3.2 The pick, on each notch (optional)

The stone shifts one notch when S3a, S3b and S3c complete; after S3c it rolls away. Three small lines, getting more urgent. Stand-at-the-stone, effort, not talk: each is under five words.

| # | Speaker | Trigger | John (J) | Mark (M) | Notes |
|---|---|---|---|---|---|
| 3.3 | The pick | Notch 1 (S3a done) | It's giving. | It moves. | The first turn the player sees the stone shift. John: warm, a little breathless. Mark: flat, a fact |
| 3.4 | The pick | Notch 2 (S3b done) | Halfway. Keep them off me. | Halfway. Hold them. | The one place the pick asks for help in so many words. Alt (J): "Nearly. Hold on, girls." Alt (M): "Halfway. Don't stop." |
| 3.5 | The pick | Notch 3 (S3c done), the stone rolls | Almost... there. | Almost. One more. | Then the roll is the sequence's own (sound + camera), no line over it. Alt (J): "There she goes!" (a laugh of relief) Alt (M): "Done." |

If THJ only wants one: **3.4** (it asks the sisters for help in a way a player can feel). If none, the stone's shifting is already visible.

### 3.3 Lines to paste and CSV

Dialogue (arrival bark as a one-line dialog, or the same lines as barks if the arrival is a bark, **THJ's or the builder's choice**):

```csharp
Line(Who.Lucy, Side.Left, "Three more from the east! Mine!"),
Line(Who.Linda, Side.Right, "Both lanes at once. Try to keep up."),
// notches, by the pick (non-blocking if possible):
Line(Who.John, Side.Right, "It's giving."),
Line(Who.John, Side.Right, "Halfway. Keep them off me."),
Line(Who.John, Side.Right, "Almost... there."),
Line(Who.Mark, Side.Right, "It moves."),
Line(Who.Mark, Side.Right, "Halfway. Hold them."),
Line(Who.Mark, Side.Right, "Almost. One more."),
```

---

## 4. The tally race: barks (max 4, only if cheap)

The tally HUD (built) shows the kills. These barks depend only on **a mushroom blast** or **a kill**, so they are cheap. Two are written so that they are **true whoever got the credit** for a mushroom kill (tech plan 6.3 is open: until THJ says yes, a blast kill counts for no one).

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 4.1 | Linda | First exploding mushroom goes off (a blast on an enemy), bark, once | Mushrooms count, you know. | A: "Does a mushroom count?" (a question; then 4.2 answers). B: "That one was ours." **Rec.** is a rule dispute between sisters that is true even if the credit rule says it doesn't count (6.3 not built). Plays the **moment** the tally question comes up | Placeholder |
| 4.2 | Lucy | Same event, reply bark, optional | Only if you lit it. | A: "Not unless you lit it." (a bit crisper). B: "I'll take that one." (if 6.3 gave her the credit; **don't use** if the blast counts for no one). **Rec.** is a joke on the rule 6.3 may make real | Placeholder |
| 4.3 | Lucy | A sister takes the lead for the first time (tally lead changes to Lucy), once | One ahead. | A: "That's one more." B: "Catch up." (rawer, shorter). Dependent on the HUD event being easy to read (X-02/X-03): **only if cheap** | Placeholder |
| 4.4 | Linda | Lead changes to Linda, once | Not for long. | A: "Keep up, Lucy." (her Ridge line; the sister call). B: "One ahead? Enjoy it." **Rec.** answers the lead without giving a number | Placeholder |

Bark rows (`Unit,Weight,PlayOnce,Dialogue,Tag`; the tag names are suggestions):

```csv
Linda,1,TRUE,"[PLACEHOLDER] Mushrooms count, you know.",M3_MushroomBlast
Lucy,1,TRUE,[PLACEHOLDER] Only if you lit it.,M3_MushroomReply
Lucy,1,TRUE,[PLACEHOLDER] One ahead.,M3_LeadLucy
Linda,1,TRUE,[PLACEHOLDER] Not for long.,M3_LeadLinda
```

If the lead-change event isn't cheap, **ship 4.1 and 4.2 only**; if even the mushroom event is hard, ship none and rely on §3.1.

---

## 5. End: the tally, the stone, Toba

Order (plan End, D-624, M3-06): **S4 "Finish them." complete** → input off → the tally alone on screen (`SistersTally_FadeOut`): Linda **"Still counting?"** · Lucy **"…No."** → the tally fades → camera on the cave (the stone is gone) → **Toba revealed** (non-hostile) → lines → fade, home.

Kept exactly as written (THJ, D-624):

| # | Speaker | Trigger | Line | Notes | Flag |
|---|---|---|---|---|---|
| 5.1 | Linda | The tally, alone on screen | Still counting? | **Kept.** Her voice, no change | Written (D-624) |
| 5.2 | Lucy | Same | …No. | **Kept.** Keep the ellipsis character as in the original | Written (D-624) |

Then Toba. The first time the family sees him, as a stranger. He doesn't explain why he hid, why he is here or who he is to Ryker (M4 §5 Q4, Q5). Sisters are wary, **not hostile** (he is a non-hostile unit in a sequence).

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 5.3 | Toba | Revealed at the cave mouth | Please. Don't be afraid. | A: "Don't be afraid. I mean no harm." (says it twice; a stranger's first words are reassurance). B: "You moved the stone. Thank you." (warmer; he is grateful, and says nothing yet about who he is). **Rec.** is the plainest. Use B if THJ wants the pick's work acknowledged | Placeholder |
| 5.4 | Linda | Same dialog | Who are you? | A: "You. Who are you?" (sharper). B: "Hold it. Who are you?" (weapon up). **Rec.** is the simplest question. She asks, not Lucy: Lucy's question is about Ryker (5.7) | Placeholder |
| 5.5 | Toba | Same dialog | I am Toba. I know the way to the Rootwell. | A: "Toba. I know the paths to the Rootwell." B: "My name is Toba. The Rootwell is not far." ("not far" is a claim on distance that M4 never makes; **avoid** unless THJ confirms). **Rec.** keeps M3-06's fact | Placeholder, **canon (the Rootwell)** |
| 5.6 | Toba | Same dialog | And I know where Ryker is. | A: "And I know where the one you seek is." (distant, keeps the name for Lucy). B: "And I know where she is." (after Lucy says the name; see 5.7) | Placeholder, **canon (Ryker)** |
| 5.7 | Lucy | Same dialog | Ryker? Where is she? | A: "Where? Tell me where!" (rawer; keeps to her M4 voice). B: "Ryker. You know her?" (**don't use**: asks how he knows, which is M4 §5 Q5). **Rec.** says her name, which is the whole point of her | Placeholder |
| 5.8 | Toba | Same dialog | I will take you. Follow me. | A: "I will show you. Come." B: "Come. I will show you." The line is also the promise M4 keeps (he leads the way) | Placeholder, **canon (Toba's role)** |

**The family reaction** (one line, the pick; optional, and either version can be dropped for a sister line):

| # | Speaker | Trigger | John (J) | Mark (M) | Notes |
|---|---|---|---|---|---|
| 5.9 | The pick | After Toba's last line, before the fade | Then lead on, Toba. | Then we follow. Lead on. | Alt (J): "Come, girls. We follow him." Alt (M): "We follow. Stay sharp." (cautious, Mark's dry). **Sister alternative if THJ drops the pick lines:** Linda: "Fine. Lead on, and we'll see." (wary-dry); Lucy: "Please. Hurry." (the closest she's been to begging) |

Note on 5.9: Mark's "Lead on" is the first time a family member **accepts** Toba. If THJ would rather keep Toba "not yet family" for longer (D-048), use Linda's version ("and we'll see"): it accepts the help, not the man.

The fade home follows: M3-07 (the house reacting to Toba) is not part of this file.

```csharp
Line(Who.Linda, Side.Right, "Still counting?"),   // the tally alone on screen (kept)
Line(Who.Lucy, Side.Left, "…No."),                // (kept)
Line(Who.Toba, Side.Left, "Please. Don't be afraid."),
Line(Who.Linda, Side.Right, "Who are you?"),
Line(Who.Toba, Side.Left, "I am Toba. I know the way to the Rootwell."),
Line(Who.Toba, Side.Left, "And I know where Ryker is."),
Line(Who.Lucy, Side.Left, "Ryker? Where is she?"),
Line(Who.Toba, Side.Left, "I will take you. Follow me."),
// optional, by the pick:
Line(Who.John, Side.Right, "Then lead on, Toba."),
Line(Who.Mark, Side.Right, "Then we follow. Lead on."),
```

(`Who.Toba` is assumed to exist, as in M4. The `…` in "…No." is the single ellipsis character U+2026 in the original; keep it.)

---

## 6. Objective texts (checked)

| Stage | Current | Verdict | Alternative |
|---|---|---|---|
| S1 | Clear the yard. | Fits. Says what to do; "the yard" names the place, which the mission title echoes | "Defeat the enemies." (colder, no place) |
| S2 | {Pick}: push the stone. | Fits (about 23 characters). Same shape as "Mark: reach the ledge." (M1). Works for John and Mark. | "{Pick}: reach the stone." (accurate for the first step, but "push" tells the whole job; since the pick may also have to **stay** on the tile, S3 is where "push" fits, see below) |
| S3a to c | Hold them off (1/3) | Fits. Punctuation: the others end with a full stop, so **"Hold them off (1/3)."** keeps them consistent (see the M1 objectives "Clear the ridge. {alive_0} remaining."). The "(1/3)" tells the player how long, which matters because the pick **waits** | "Hold the yard (1/3)." (echoes the mission name, better as a theme; the sisters also hold the yard, not only the pick) |
| S4 | Finish them. | Fits. Plain, a little cold; matches Linda's tone | "Finish off the rest." / "Clear the yard." (**avoid**: it's S1's text) |

One extra check for S3: the pick has to **stay on the tile**, and the objective doesn't say it. Rec. keep S2 as is, and let S3a to c be short; if THJ finds players leaving the tile, a second line under it: **"Keep {Pick} at the stone."** (alt: "{Pick} stays at the stone."). That one costs a new text key; it's a design lever, not a line I'd add now.

The capitalised form for the enemy, if an objective ever names it: **Dark Claws** (glossary), as in the M4 note.

---

## 7. What is unchanged, and what this file doesn't cover

- M3-07 (Home: the house reacts to Toba, then the Linda–Lucy scene): separate text task.
- The Heavenly Sword's pickup text: data (PR-30), unchanged. A walk-on in this level (8,6); no line speaks about it. If THJ wants a one-line bark when it's picked up first time, say so: **Lucy "A sword? Heavy." / Linda "Take it. Use it."** is the sort of thing it would be (not proposed here).
- The Masher's own barks, deaths, close-up captions: not in this file.
- "They break walls": deferred with the barriers (D-689). When barriers return, the cue needs a new row.
- All Toba lines after the fade (the Rootwell, M4 on): in `m4-text.md`. Voice kept consistent: short sentences, "Please" and "I will", never a joke.

---

## 8. Canon and name flags

- **Toba reveals** he knows the way to the Rootwell and where Ryker is (5.5, 5.6, 5.8). These are M3-06's own facts; the lines assert nothing more. **Not stated:** why he was in the cave, that he carried or tended Ryker, or how he knows her name (M4 §5 Q4, Q5). Lucy's 5.7 alt B ("You know her?") is exactly that question, so it is a no.
- **Linda's "Who are you?"** (5.4) treats Toba as a stranger. If the Ridge clue (a man's tracks, herbs, a poultice) is Toba's, Mark and Linda could name that here ("The tracks on the ridge. That was you."). Not written: M4 §5 Q5 is open.
- **"The Rootwell"** is a place name already in `narrative-world.md`; 5.5 says it aloud for the first time in the demo. Check that the player doesn't see "The White Mothers" (the M4 file name) at the same time.
- **"Stone"** is the unit's placeholder title (tech plan). The lines say "the stone". If THJ renames it, the one line it appears in is 1.1.
- **No new character or place names** here.

---

## 9. Glossary proposals (not applied; `glossary.md` is untouched)

| Term | Proposal | Status |
| --- | --- | --- |
| **Hold the yard** | M3's on-screen name: the one level of the mission whose asset is still `M2 - The Trail` (the Trail's levels are renamed `_legacy`). Level prefab `GB_m3-defence` (design word: defence) | Proposed; check the mission's screen title |
| **the yard** | The play area of M3: used in the objective "Clear the yard." and in lines. Not to be confused with the Home's yard scene (the Linda–Lucy scene, today's "Yard") | Proposed; name clash worth checking with THJ |
| **the stone** | The rock on the cave (5,8) the pick pushes, three notches, then it rolls away; unit title "Stone" (placeholder). Not "Fallen Rock" (M1's rock, `m1-ridge-redesign-text.md` §9) | Proposed |
| **the pick** (design word) | The squad's free seat, John or Mark (D-622): not shown on screen; lines name John or Mark | Proposed (already used in `m4-text.md`) |
| **Masher Goblin** | Already in the table. Add: first appearance in the demo is M3's opening yard fight, not M1 | Needs THJ (the glossary is `miso-narrative`'s, wait for approval) |
| **Toba, joins after M3** | Already proposed in `m4-text.md` §6. M3 is where he appears (5.3 to 5.8) | Needs THJ |
| **Rootwell** | Already proposed in `m4-text.md` §6; 5.5 is its first mention | Proposed |
| **Ryker** | Already proposed in `m1-ridge-redesign-text.md` §10; this file only says "she" | Proposed |
