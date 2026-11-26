# M3 "Hold the yard": lines

Owner: miso-narrative. Scope `all` (`main`).
**Current text: the 2026-11-26 redesign** (plan `plans/2026-11-26-m3-redesign.md` › Text impact, level `m3-defence-3`; build tech plan `plans/2026-11-26-m3-redesign-build-tech.md`, chunk 7.2). THJ's decisions of 2026-11-26: the squad is **Linda and Lucy only**; Mark is placed on the stone, held, not playable, and can be attacked; the level is lost if he falls; the stone moves one notch at each family turn start for 4 turns; six barricades close two necks; the Masher comes up the east lane; the end stays.
Status: **Approved by THJ 2026-11-26 (D-731 to D-735).** Every **Rec.** line in §0 to §6 is approved as written, with the answers folded in: the unit is **Barricade** (D-731); notch 4 has one line and no branch (D-732); the loss rule shows on screen, M3.6.6 and M3.6.7 (D-733); Toba opens with "You moved the stone. Thank you." and Mark closes with "We follow. Stay sharp." (D-734); "the wall" is speech only and Mark gives no push count (D-735). Alternatives stay in the tables as history; paste only the Rec. Kept as written: **"Still counting?" / "…No."** (D-624). Canon (Q7): nothing new is claimed; the M4 §5 questions stay open. §7 is the final line map for the build (chunk 7.2).
The 2026-11-25 draft (yard opening, John or Mark as the pick, 3 notches) is kept as history under [Superseded](#superseded-2026-11-25-draft-old-level-m3-defence) at the end. Nothing below depends on it.

How to paste (same rules as `m1-ridge-redesign-text.md` and `m4-text.md`):
- **Dialogue** (`DialogNodeSequence`, `Line(Who.X, Side.Y, "...")`): paste **without** a tag. Dialogue shows `[PLACEHOLDER]` and the onboarding tests forbid it (`conventions.md` › Text).
- **Barks** (CSV rows): approved, so the CSV blocks below carry no `[PLACEHOLDER] ` prefix. (The bark system would strip it anyway.)
- **On-screen text** (§6): approved; paste as written.
- **Rec.** is the line to paste; alternatives are for THJ, one line on the feel of each.
- **IDs** (`M3.x.y`) are for the build (7.2) to map lines to sequences; they are design labels and never go into code comments or test names (CLAUDE.md, no private IDs). The **Build slot** column names the sequence or constant the line lands in, as the wiring is today (`MissionWiring.HoldTheYard.Sequences.cs`).
- **Sides** as built: Linda Left, Lucy Right, Toba Right. Mark: Right (suggested; the builder may swap).
- **Mark speaks as himself** now: `Who.Mark`, not the pick's generic dialogue slot (`SpeakAsThePick` and the John versions go).
- Lines stay under about 55 characters so they fit a bubble.

**Changed from the 2026-11-25 draft** is marked **(new)**, **(changed)** or **(kept)** in each row.

Cast: **Linda, Lucy** (playable), **Mark** (on the stone, a voice and a target), **Toba** (the end only). No John line anywhere in M3.

Voice (as in M1 and M4):
- **Linda:** older sister, quick, proud, dry. **Lucy:** the youngest, fierce and open; short lines. Between them: a race, not a quarrel. The race **ends** at "Still counting?" / "…No.", and M4's first Duo ("Together this time, Lucy." / "No counting.") pays it off. Barks here keep the rivalry bright, never mean.
- **Mark:** calm, clipped, a dry streak. On the stone he is all effort: short lines, no speeches. He is the one person in the level who can't fight, and he says so once.
- **Toba:** gentle, plain, unhurried; short sentences, no jokes. A stranger being slowly trusted.

Terms (glossary): **Dark Claws**, **Masher Goblin** (the close-up shows the name only, EN-10), **Rootwell**, **Ryker** (she). **the stone** in lines (unit title "Stone", placeholder). **Barricade** for the unit (D-731); in speech a row of three is **the wall**, a spoken word only, never an on-screen term (D-735). The D-689 ban on "wall" / "barrier" / "they break" lifts with the barricades: it existed only because they were deferred. "Wounded" and "Bloodied" are not used.

Canon not touched (M4 file's §5 questions stay open): who Ryker is, why Toba hid in the cave, whether he carried or tended her, how he knows her.

---

## 0. Level start (new)

Order (plan › Cues): input off → camera over the Masher (its close-up plays on first sight, EN-10) → **M3.0.1** → camera over the east wall → camera on Mark at the stone → **M3.0.2**, **M3.0.3** → camera back on the yard (w1 is already at the west lane) → **M3.0.4**, **M3.0.5** → objective "Hold them off. 4 turns left." → input on. Build slot: the level-start sequence (`M3Defence_Start_*`, which today only reveals the stone).

| ID | Speaker | Trigger | Rec. line | Alternatives / notes | Status |
|---|---|---|---|---|---|
| M3.0.1 | Linda | Masher close-up | Every hit brings that one a step closer. | A: "Shoot that one and it comes for you." (blunter; the slam is implied). B, two lines: Lucy "It's slow." / Linda "Hit it, and it isn't." (the sisters' banter carries the rule; one line longer). **Rec.** states the new rule plainly (the UX critic: the old "keep your distance" taught the old rule). Linda says it because her bow is what pulls it | **(changed)** from old 0.1 |
| M3.0.2 | Mark | Camera on Mark at the stone | A cave behind this stone. I'll shift it. | A: "There's a cave behind this. Give me time." (softer, no job named). **Rec.** keeps the Mark line from the old draft (old 1.1 M), now said at the stone instead of after a yard fight | **(changed)** from old 1.1 M |
| M3.0.3 | Mark | Same dialog | I can't push and fight. Keep them off me. | A: "Four pushes. Don't let them near." (gives the count in his voice; must change if the hold length lever moves to 3 or 5). B: "Can't fight and push. The yard's yours." (hands the level to the sisters; says less about him being a target). **Rec.** is the one line that tells the player Mark is not theirs to move and that he can be hit. No push count: the objective carries it (D-735) | **(new)**, approved |
| M3.0.4 | Linda | Camera back on the yard | Keep them off him, Lucy! | **(kept)** from old 2.1, now in the opening (w1 is on the board at start). Same text as the built `PushLine` plus Lucy's name | **(changed)** trigger |
| M3.0.5 | Lucy | Same dialog, optional | And keep count, sister. | A: "Nobody touches Mark." (protective; drops the race). B: "Mine, mostly." (cockier). **Rec.** opens the tally race the HUD is showing; it pays off at "Still counting?" | **(kept)** from old 2.2 |

Cut order if the opening runs long: M3.0.5, then M3.0.1 (the close-up still shows the name; the counter preview teaches the pull). M3.0.3 is the last to cut.

```csharp
Line(Who.Linda, Side.Left, "Every hit brings that one a step closer."),   // M3.0.1, Masher close-up
Line(Who.Mark, Side.Right, "A cave behind this stone. I'll shift it."),   // M3.0.2
Line(Who.Mark, Side.Right, "I can't push and fight. Keep them off me."),  // M3.0.3
Line(Who.Linda, Side.Left, "Keep them off him, Lucy!"),                   // M3.0.4
Line(Who.Lucy, Side.Right, "And keep count, sister."),                    // M3.0.5, optional
```

(The `// M3.x.y` tags are for this file only; strip them when pasting.)

---

## 1. Mark on each notch (new: four notches, Mark only)

The stone moves one notch at the start of family turns 2, 3, 4 and 5. Each notch: camera on the stone → notch → Mark's line → (arrival, §2, on notches 1 and 2) → camera back. Lines get shorter and more urgent; effort, not talk. Build slots: `M3Defence_Notch1..4_*` (the build adds Notch4; the old `OpenLine` "It's moving... it's open!" moves to notch 4 and is replaced by M3.1.4).

| ID | Speaker | Trigger | Rec. line | Alternatives / notes | Status |
|---|---|---|---|---|---|
| M3.1.1 | Mark | Notch 1 (turn 2 start), before the w2 arrival | It moves. | A: "It's giving." (the old John line, works for Mark too, a little warmer). **Rec.** flat, a fact: Mark's voice | **(kept)** from old 3.3 M |
| M3.1.2 | Mark | Notch 2 (turn 3 start), before the w3 arrival | Halfway. Hold them. | A: "Halfway. Don't stop." (urges the sisters on). With four notches, notch 2 is the true halfway | **(kept)** from old 3.4 M |
| M3.1.3 | Mark | Notch 3 (turn 4 start), no wave: the crisis turn | Nearly. Keep them off me. | A: "One more. Don't let them near." B: "Almost. Hold." (shortest). **Rec.** is the second and last time he asks for help; this is the turn breachers are one move from him | **(new)** |
| M3.1.4 | Mark | Notch 4 (turn 5 start), the stone rolls away; **always**, whether the Masher is alive or dead | It's open! Now the big one! | A: "It's open. The big one's at the wall!" (THJ's beat, most vivid; only true if the Masher stands at the east neck, and wrong if it's still in the lane or already in the yard). B: "Open! Mind the big one!" (a warning, not a call to arms). **Rec.** hands over to the threat wherever the Masher is. Then "Finish them." shows. **D-732:** the line plays even if the Masher is already dead; THJ accepts the rare mismatch. No branch | **(new)**, approved |
| ~~M3.1.4b~~ | Mark | ~~Same, the Masher is dead~~ | ~~It's open. Finish them.~~ | **Dropped (D-732):** no branch at notch 4 | dropped |

```csharp
Line(Who.Mark, Side.Right, "It moves."),                    // M3.1.1, notch 1
Line(Who.Mark, Side.Right, "Halfway. Hold them."),          // M3.1.2, notch 2
Line(Who.Mark, Side.Right, "Nearly. Keep them off me."),    // M3.1.3, notch 3
Line(Who.Mark, Side.Right, "It's open! Now the big one!"),  // M3.1.4, notch 4, always
```

---

## 2. Wave arrivals (changed: new counts and timing)

w1 is on the board at start (its line is M3.0.4). w2 comes in on notch 1, w3 on notch 2, with the built arrival pattern (camera on the wave, reveal, bark, camera back). One sister per wave. Both lines leave out the number of Claws, so they survive the wave-size levers. Build slots: `M3Defence_Notch1_Bark_*` (built `Wave2Line`) and `M3Defence_Notch2_Bark_*` (built `Wave3Line`).

| ID | Speaker | Trigger | Rec. line | Alternatives / notes | Status |
|---|---|---|---|---|---|
| M3.2.1 | Lucy | w2 revealed (2 Claws, east lane, behind the Masher) | More from the east! Mine! | A: "Behind the big one! Mine!" (points at the Masher's pack; the plow lesson). B: "Two more, east. Easy." (gives the count; breaks if it changes). **Rec.** claims the lane: the race in one word. Same as the built `Wave2Line` plus "Mine!" | **(changed)** from old 3.1 |
| M3.2.2 | Linda | w3 revealed (2 west, 1 east) | Both lanes at once. Try to keep up. | A: "Both lanes! Split with me, Lucy!" (an order; tells the player the answer). B: "Both sides now!" (the built `Wave3Line`, shortest). **Rec.** keeps the challenge: the race is closest in the last wave | **(kept)** from old 3.2 |

```csharp
Line(Who.Lucy, Side.Right, "More from the east! Mine!"),           // M3.2.1, w2
Line(Who.Linda, Side.Left, "Both lanes at once. Try to keep up."), // M3.2.2, w3
```

---

## 3. Hold events (new)

These fire on events that may happen in the enemy turn, so a **bark** (non-blocking) fits better than a dialog. The build needs a trigger for each (an event the bark system or a level condition can hear); if a trigger isn't cheap, drop the row.

| ID | Speaker | Trigger | Rec. line | Alternatives / notes | Status |
|---|---|---|---|---|---|
| M3.3.1 | Linda | **First barricade destroyed**, either neck, once | A barricade's down! They're coming through! | A: Lucy "They're through! Get to Mark!" (names the answer: defend him; urgent, fierce). B: Mark "They're through. I can't stop now." (the dread: he can't defend himself). **Rec.** names the thing that broke, so the player learns the word, and doesn't name a side, so it fits either neck. The "they break walls" cue the old §7 deferred | **(new)** |
| M3.3.2 | Lucy | **First enemy attack on Mark**, once, optional | Get away from him! | Replaces John's "Not him." (John is out). A: Linda "Mark! Hold on!" **Rec.** fierce, short, her | **(new)**, optional |
| M3.3.3 | Mark | Reply to M3.3.2, same event, optional | Still pushing. | A: "I'm fine. Keep going." **Rec.** the dry streak: he's hurt and won't make it a moment | **(new)**, optional |

```csv
Linda,1,TRUE,A barricade's down! They're coming through!,M3_BarricadeDown
Lucy,1,TRUE,Get away from him!,M3_MarkHit
Mark,1,TRUE,Still pushing.,M3_MarkHitReply
```

(Tags are suggestions. If M3.3.1 plays as a dialog instead, paste it without the tag.)

---

## 4. The tally race: barks (kept, unchanged)

The old §4 stands as written: the four rows below, max 4, only if cheap. Mushroom blasts now sit at 1,4 and 8,4, under each front, so M3.4.1/M3.4.2 are more likely to fire.

| ID | Speaker | Trigger | Line | Status |
|---|---|---|---|---|
| M3.4.1 | Linda | First mushroom blast on an enemy, once | Mushrooms count, you know. | **(kept)** old 4.1 |
| M3.4.2 | Lucy | Same event, reply, optional | Only if you lit it. | **(kept)** old 4.2 |
| M3.4.3 | Lucy | Tally lead changes to Lucy, once | One ahead. | **(kept)** old 4.3 |
| M3.4.4 | Linda | Tally lead changes to Linda, once | Not for long. | **(kept)** old 4.4 |

```csv
Linda,1,TRUE,"Mushrooms count, you know.",M3_MushroomBlast
Lucy,1,TRUE,Only if you lit it.,M3_MushroomReply
Lucy,1,TRUE,One ahead.,M3_LeadLucy
Linda,1,TRUE,Not for long.,M3_LeadLinda
```

---

## 5. End: the tally, Toba (kept; 5.9 changed to Mark)

Order as built: "Finish them." complete → input off, HUD off → the tally alone (`SistersTally ShowAlone`) → **M3.5.1** → tally fades → **M3.5.2** → camera on the cave → Toba revealed → **M3.5.3 to M3.5.9** → outro. Build slot: `M3Defence_End_*` (`StillCountingLine`, `NoLine`, `TobaLines`). Note: in the redesign the stone rolls away on notch 4, so the end no longer needs `M3Defence_End_HideLastStone` (the build's call).

| ID | Speaker | Trigger | Line | Notes | Status |
|---|---|---|---|---|---|
| M3.5.1 | Linda | The tally, alone on screen | Still counting? | Written (D-624) | **(kept)** |
| M3.5.2 | Lucy | Same | …No. | Written (D-624); the single ellipsis character U+2026 | **(kept)** |
| M3.5.3 | Toba | Revealed at the cave mouth | You moved the stone. Thank you. | **Rec. changed** (was alt B of old 5.3): Mark pushed the stone in front of the player for four turns, so Toba's first words acknowledge it. A: "Please. Don't be afraid." (the old Rec., plainest). Built placeholder "You held them. Good." is replaced. Approved (D-734) | **(changed)**, approved |
| M3.5.4 | Linda | Same dialog | Who are you? | As old 5.4 | **(kept)** |
| M3.5.5 | Toba | Same dialog | I am Toba. I know the way to the Rootwell. | As old 5.5. **Canon (the Rootwell)** | **(kept)** |
| M3.5.6 | Toba | Same dialog | And I know where Ryker is. | As old 5.6. **Canon (Ryker)** | **(kept)** |
| M3.5.7 | Lucy | Same dialog | Ryker? Where is she? | As old 5.7 | **(kept)** |
| M3.5.8 | Toba | Same dialog | I will take you. Follow me. | As old 5.8. **Canon (Toba's role)** | **(kept)** |
| M3.5.9 | Mark | After Toba's last line, before the fade | We follow. Stay sharp. | **Changed:** Mark speaks (he's there; John isn't). A: "Then we follow. Lead on." (the old Mark line; the first family member to accept Toba). B: Linda "Fine. Lead on, and we'll see." (wary-dry). **Rec.** accepts the help, not the man, which keeps Toba "not yet family" (D-048). Approved (D-734) | **(changed)**, approved |

```csharp
Line(Who.Linda, Side.Left, "Still counting?"),                          // M3.5.1 (kept)
Line(Who.Lucy, Side.Right, "…No."),                                     // M3.5.2 (kept)
Line(Who.Toba, Side.Right, "You moved the stone. Thank you."),          // M3.5.3
Line(Who.Linda, Side.Left, "Who are you?"),                             // M3.5.4
Line(Who.Toba, Side.Right, "I am Toba. I know the way to the Rootwell."), // M3.5.5
Line(Who.Toba, Side.Right, "And I know where Ryker is."),               // M3.5.6
Line(Who.Lucy, Side.Right, "Ryker? Where is she?"),                     // M3.5.7
Line(Who.Toba, Side.Right, "I will take you. Follow me."),              // M3.5.8
Line(Who.Mark, Side.Right, "We follow. Stay sharp."),                   // M3.5.9
```

(Toba's lines are seeded through `SpeakAsToba` as built; there is no `Who.Toba` in the shared writer. Sides as built put Toba and Lucy both Right; the builder may move Lucy Left for M3.5.7.)

---

## 6. On-screen text (changed)

Build slots: `HoldObjectives` and `FinishObjective` in `MissionWiring.HoldTheYard.cs` (today "Hold them off (1/3)" etc.; the 7.1 placeholders are "Hold them off (4)" to "(1)").

| ID | Where | Rec. text | Alternatives / notes | Status |
|---|---|---|---|---|
| M3.6.1 | Objective S1 (turn 1) | Hold them off. 4 turns left. | Same shape as M1's "Clear the ridge. {alive_0} remaining." A: "Hold them off: 4 turns." (shorter, the design plan's shape). B: "Hold the yard. 4 turns left." (echoes the mission name). The countdown fixes the "(1/4) reads as one done" misread | **(new)** |
| M3.6.2 | Objective S2 (turn 2) | Hold them off. 3 turns left. | As above | **(new)** |
| M3.6.3 | Objective S3 (turn 3) | Hold them off. 2 turns left. | As above | **(new)** |
| M3.6.4 | Objective S4 (turn 4) | Hold them off. Last turn. | A: "Hold them off. 1 turn left." (strict pattern). **Rec.** "Last turn." reads as the crisis it is, avoids "1 turns" plural traps, and stays true if the hold length lever changes | **(new)** |
| M3.6.5 | Objective S5 | Finish them. | Unchanged | **(kept)** |
| M3.6.6 | **Objective text of Mark's defeat group** (the loss condition "Mark falls"), shown with the hold objectives S1 to S4 | Keep Mark standing. | A: "Mark must not fall." (colder; not chosen). Mark falling is a new way to lose; this says so on screen. **D-733:** shown | **(new)**, approved |
| M3.6.7 | **Defeat message of Mark's defeat group**, shown when the level is lost because Mark fell | Mark has fallen. | A: "Mark fell. The stone stays shut." (not chosen). **D-733:** shown | **(new)**, approved |
| M3.6.8 | Unit title of the barricade | Barricade | **D-731** | **(new)**, approved |

Gone: "Clear the yard." (S1 of the old level) and "{Pick}: push the stone." (the pick is out of M3).

---

## 7. Line map for the build (7.2): final

Final for chunk 7.2 (approved 2026-11-26, D-731 to D-735). Paste the Rec. text from §0 to §6 for each ID. Bark rows need a trigger the build can hear; if one isn't cheap, the row is dropped (the build's call, as §3 and §4 say), not reworded.

| Build slot today | Today's placeholder | Becomes |
|---|---|---|
| Start sequence (stone reveal only) | none | M3.0.1 (at the Masher close-up), M3.0.2 to M3.0.5 (at Mark, then the yard) |
| `CaveLine` / `M3Defence_Cave_*` | "There's a cave behind that stone." (the pick) | Gone; its job moves to M3.0.2 |
| `PushLine` / `M3Defence_Push_*` | "Keep them off him!" (Linda) | M3.0.4, in the start sequence |
| Notch1 line (new) | none | M3.1.1 |
| `Wave2Line` / Notch1 bark | "More from the east!" (Lucy) | M3.2.1 |
| Notch2 line (new) | none | M3.1.2 |
| `Wave3Line` / Notch2 bark | "Both sides now!" (Linda) | M3.2.2 |
| Notch3 line (was `OpenLine`) | "It's moving... it's open!" (the pick) | M3.1.3 |
| Notch4 line (new) | none | M3.1.4, always (no branch, D-732) |
| Bark events (new) | none | M3.3.1, M3.3.2, M3.3.3 (CSV) |
| Tally barks | none built | M3.4.1 to M3.4.4 (CSV, only if cheap) |
| `StillCountingLine`, `NoLine` | as written | M3.5.1, M3.5.2 (unchanged) |
| `TobaLines` | "You held them. Good." / "I know the way to the Rootwell. And where Ryker is." | M3.5.3, M3.5.5, M3.5.6, M3.5.8 (Toba); M3.5.4, M3.5.7 (sisters) and M3.5.9 (Mark) as separate dialog nodes |
| `HoldObjectives`, `FinishObjective` | "Hold them off (1/3)" ... / "Finish them." | M3.6.1 to M3.6.4, M3.6.5 |
| Mark's defeat group: objective text (new) | none | M3.6.6 "Keep Mark standing." (D-733) |
| Mark's defeat group: defeat message (new) | none | M3.6.7 "Mark has fallen." (D-733) |
| Barricade unit title | "Barricade" | M3.6.8 (D-731) |

---

## 8. Questions for THJ (answered 2026-11-26)

Answers: **Q1** Barricade (D-731). **Q2** "the wall" in speech only, never on screen (D-735, coordinator, my default). **Q3** no push count in Mark's line; M3.0.3 Rec. stands (D-735). **Q4** no branch; "It's open! Now the big one!" always, rare mismatch accepted; M3.1.4b dropped (D-732). **Q5** yes, both: M3.6.6 as the defeat group's objective text, M3.6.7 as its defeat message (D-733). **Q6** "You moved the stone. Thank you." approved, with Mark's closing "We follow. Stay sharp." (D-734). **Q7** nothing new claimed; no change, the M4 §5 questions stay open.

The questions as asked:

- **Q1 · The barricade's name.** Options: **Barricade** (rec.: plain, reads at once, matches the rule sentence "goblins can't get past the barricades"); **Palisade** (rustic sharpened stakes, matches the planned sprite; a word some players must look up); **Stakes** (homely, short; reads as a weapon, not a wall). On screen it is only the unit title and M3.3.1.
- **Q2 · "the wall" in speech.** Characters call a row of three barricades "the wall" (M3.1.4 alt A, and your own "the big one's at the wall"). OK as a spoken word only, never on screen as a term? If not, M3.1.4 Rec. already avoids it.
- **Q3 · Mark's count in M3.0.3.** "Four pushes" (alt A) puts the countdown in his voice but ties the line to the hold-length lever. Rec. leaves the count to the objective.
- **Q4 · The handover when the Masher is already dead.** Can notch 4 branch? If not: keep "It's open! Now the big one!" (rare mismatch) or use "It's open! Finish them!" for both.
- **Q5 · Say the loss condition on screen?** M3.6.6 "Keep Mark standing." as a second objective line, and/or M3.6.7 on the loss panel. Both cost a text key; neither is in the build plan yet.
- **Q6 · Toba's first words.** M3.5.3 changed to "You moved the stone. Thank you." (acknowledges Mark's four turns). Canon-neutral, but it is his first line in the demo.
- **Q7 (canon, still open from M4 §5):** M3.5.5 to M3.5.8 assert only that Toba knows the way to the Rootwell and where Ryker is, and offers to lead. Nothing on why he hid or how he knows her.

## 9. Glossary rows (applied to `glossary.md` 2026-11-26, section "M3: Hold the yard")

| Term | Row | Status |
| --- | --- | --- |
| **Barricade** | M3's breakable barrier unit (`Unit_Barricade`, a `Unit_Rock` variant): Neutral, Unmovable, 8 HP in M3; goblins can't pass and attack it; the family walks through, can't stop on it, can't hurt it; no repair. On screen: unit title "Barricade" and "the barricades". Not "barrier" on screen | Approved (D-731), applied |
| **the wall** (speech only) | A row of three barricades across a neck, as the characters say it. Never a term on screen | Approved (D-735), applied |
| **the stone** | The rock on the cave at 4,12 that **Mark** pushes in M3, one notch per family turn for 4 turns, then it rolls away; unit title "Stone" (placeholder); five variants. Not "Fallen Rock" (M1) | Applied (unit title still placeholder) |
| **Hold the yard** | M3's on-screen name (mission asset still `M2 - The Trail`); level prefab `GB_m3-defence-3` | Applied |
| **the pick** (design word) | No longer used in M3 (squad is Linda and Lucy, fixed). Still used in `m4-text.md` if M4 keeps a free seat | Applied |
| **Masher Goblin** | First appearance in the demo is M3, walking up the east lane; its counter "every hit brings it a step closer" | Applied (Enemies row) |
| **Toba, Rootwell, Ryker** | M3 is Toba's first appearance and the Rootwell's first mention. Their rows stay proposed in `m4-text.md` §6 and `m1-ridge-redesign-text.md` §10 (Q7: no canon change) | Not applied: still proposed |

---
---

# Superseded: 2026-11-25 draft (old level `m3-defence`)

Kept as history. Written for the approved paper level of 2026-11-22 (D-688 to D-690): a yard opening with the Masher, the squad Linda, Lucy + a pick (John or Mark), the pick pushing the stone over three notches. **Superseded on 2026-11-26** by the redesign above (D-722 and THJ's 2026-11-26 decisions: John out, Mark held on the stone, four notches, barricades, the Masher in the east lane). Do not paste from this section.

## Old 0. Level start: the Masher (optional)

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 0.1 | Linda | Masher close-up | That one hits back. Keep your distance. | A: "Big one. Don't stand next to it." B: "Lucy. Not too close." | Superseded by M3.0.1 |
| 0.2 | The pick (J) | Same dialog, optional | John: Stay behind me. | Alt: "I'll take the front. You two keep your distance." | Dropped (John out) |
| 0.2 | The pick (M) | Same | Mark: Mind the distance. Then strike. | Alt: "Range first. Then strike." | Dropped |

## Old 1. S1 complete: the cave behind the stone

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 1.1 | The pick (J) | S1 complete, camera on the stone | John: There's a cave behind that stone. I'll move it. | A: "A cave. Someone's inside. I'll move the stone." B: "There's a cave behind that stone. Give me time." | Dropped |
| 1.1 | The pick (M) | Same | Mark: A cave behind that stone. I'll shift it. | A: "A cave behind the stone. Hold the yard; I'll shift it." B: "There's a cave. Something's hidden there." | Became M3.0.2 |

Herb-link option (not Rec., canon-adjacent): "Herbs, drying at the edge. Someone's in there."

## Old 2. S2 complete: wave 1 arrives

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 2.1 | Linda | w1 revealed | Keep them off him, Lucy! | A: "Keep them off him!" B: "Here they come! Keep them off him!" | Became M3.0.4 |
| 2.2 | Lucy | Same dialog, optional | And keep count, sister. | A: "Mine, mostly." B: "Don't fall behind." | Became M3.0.5 |

## Old 3. The hold: waves w2 and w3, and the stone's notches

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 3.1 | Lucy | w2 revealed (three Claws, east lane) | Three more from the east! Mine! | A: "Three on my side. Easy." B: "More! Good." | Became M3.2.1 (count dropped) |
| 3.2 | Linda | w3 revealed (both lanes) | Both lanes at once. Try to keep up. | A: "Both lanes! Lucy, split with me!" B: "Both lanes. Is that all?" | Became M3.2.2 |

| # | Speaker | Trigger | John (J) | Mark (M) | Flag |
|---|---|---|---|---|---|
| 3.3 | The pick | Notch 1 | It's giving. | It moves. | Mark's became M3.1.1; John's dropped |
| 3.4 | The pick | Notch 2 | Halfway. Keep them off me. | Halfway. Hold them. | Mark's became M3.1.2; John's dropped |
| 3.5 | The pick | Notch 3, the stone rolls | Almost... there. | Almost. One more. | Dropped (four notches now: M3.1.3, M3.1.4) |

## Old 4. The tally race

Unchanged; now §4 (M3.4.1 to M3.4.4).

## Old 5. End

5.1 to 5.8 unchanged as M3.5.1 to M3.5.8, except 5.3's Rec. ("Please. Don't be afraid.", now alt A of M3.5.3).

| # | Speaker | Trigger | John (J) | Mark (M) | Flag |
|---|---|---|---|---|---|
| 5.9 | The pick | After Toba's last line | Then lead on, Toba. | Then we follow. Lead on. | John's dropped; Mark's is alt A of M3.5.9 |

## Old 6. Objective texts

| Stage | Text | Flag |
|---|---|---|
| S1 | Clear the yard. | Gone (no yard opening) |
| S2 | {Pick}: push the stone. | Gone (no pick) |
| S3a to c | Hold them off (1/3). | Replaced by the countdown M3.6.1 to M3.6.4 |
| S4 | Finish them. | Kept as M3.6.5 |
| (lever) | Keep {Pick} at the stone. | Gone; the redesign's lever is M3.6.6 |

## Old 7 to 9

- Old §7 (not covered): M3-07 Home, the Heavenly Sword's pickup text, the Masher's own barks, all Toba lines after the fade: still out of this file. The deferred "they break walls" cue is now M3.3.1.
- Old §8 canon flags: carried into §8 Q7 above.
- Old §9 glossary rows: carried into §9 above, with "the stone" and "the pick" updated.
