# M3 "Hold the yard": lines

Owner: miso-narrative. Scope `all` (`main`).
**Status: approved by THJ 2026-11-26 (D-745, D-749, D-750).** The revision for the pick, written 2026-11-26 for D-739 and D-741 to D-745 and the plan `plans/2026-11-26-m3-pick-and-opening.md` (block `m3-defence-4`) › Text impact. It replaces the Mark-on-the-stone version (D-731 to D-735; see [History](#history) at the end). Still standing from that version: Barricade (D-731), no branch at the stone's last notch (D-732), Toba's opening and the closing line (D-734), "the wall" in speech only and no push count (D-735). D-733's Mark texts are reworded by D-745. §D8 is the line map for the build; the glossary rows (§D9) are applied.

The design in one paragraph (D-741 to D-745): the squad is **Linda, Lucy and the pick (John or Mark)**, chosen on the Trail's roster. The layout is the round-two one (barricades, two lanes, the Masher in the east lane). Stages: **S1 "Clear the yard."** (3 Dark Claws at the stone; w1 already in the west lane) → **S2 "{pick}: push the stone."** (the pick walks to the lit push tile; on arrival they are held, out of combat, and the Masher is revealed with its close-up) → **S3 to S5, a 3-turn hold** (notch 1 brings w2, notch 2 brings w3, notch 3 rolls the stone away and the pick rejoins) → **S6 "Finish them."**. The pick falling loses, from level start.

**Pick lines (D-749).** A "pick line" is said by whoever the pick is, through the pick's dialogue slot (`SpeakAsThePick`). Every pick line has **one text for both picks** (Mark's approved line), except **M3.0.3**, which has a Mark text and a John text (a small per-pick text option in Onboarding). No other John-only versions.

How to paste: dialogue without a tag; barks and on-screen text as written (all approved). `M3.x.y` IDs are design labels only; never in code comments or test names. Lines stay under about 55 characters. **Sides:** Linda Left, Lucy Right, Toba Right, the pick Right (suggested; the builder may swap).

**Cast.** **Linda, Lucy** (playable all level). **The pick, John or Mark** (playable in the opening and the finish; held at the stone during the hold, a voice and a target). **Toba** (the end only). The one not picked is not in M3 and has no line.

**Voice.**
- **Linda:** older sister, quick, proud, dry. **Lucy:** the youngest, fierce and open; short lines. A race, not a quarrel; it ends at "Still counting?" / "…No." (D-624), and M4's first Duo pays it off.
- **Mark:** calm, clipped, a dry streak. On the stone: effort, short lines.
- **John:** the father; warm, steady, plain words; thinks of his girls first. His one own line here (M3.0.3) is that worry: he can't shield them.
- **Toba:** gentle, plain, unhurried; a stranger slowly trusted.

**Terms** (glossary): Dark Claws, Masher Goblin (close-up shows the name only), Barricade (unit, D-731), "the wall" (speech only, D-735), the stone, Rootwell, Ryker (she). The rule the player must get: *while the pick pushes, they're out of the fight, and they can be hit* (said once, M3.0.3). Canon: nothing new claimed (M4 §5 questions stay open: who Ryker is, why Toba hid in the cave, how he knows her).

## Changes against the Mark-on-the-stone version

Every line that still fits is kept **word for word**; only its trigger or speaker slot moves.

| ID | Mark-on-the-stone text (D-731 to D-735) | Approved now | What changed and why |
|---|---|---|---|
| Header, cast, voice | Squad Linda and Lucy; Mark on the stone; `Who.Mark`; no John line | Squad Linda, Lucy + the pick; pick lines through the pick slot; John speaks M3.0.3 | D-741, D-749 |
| §0 order | Masher close-up at level start; Mark's lines at level start | Level start: the stone and its Claws, then w1 in the west lane. The cave line moves to S1's end; the Masher close-up and the push line move to S2's end | D-742, D-743 |
| M3.0.1 Linda | Every hit brings that one a step closer. | **Same.** Trigger: the Masher's reveal at the push | D-743 |
| M3.0.2 Mark | A cave behind this stone. I'll shift it. | **Same, for both picks.** Trigger: S1 complete | Pick line, D-749 |
| M3.0.3 Mark | I can't push and fight. Keep them off me. | **Mark: same. John: "I can't push and shield you. Keep them off me."** Trigger: S2 complete (the pick is held) | D-749. The one pick line with two texts; it carries the "out of the fight" rule |
| M3.0.4 Linda | Keep them off him, Lucy! | **Same.** Trigger: S2 complete | "him" fits John and Mark |
| M3.0.5 Lucy | And keep count, sister. | **Same.** Trigger: S2 complete, optional | — |
| M3.0.6 to M3.0.8 | none | **New:** level start | D-750 |
| M3.1.1 Mark | It moves. | **Same, for both picks**, notch 1 | D-749 |
| M3.1.2 Mark | Halfway. Hold them. | **Dropped** | Notch 2 of 3 is not halfway |
| M3.1.3 Mark | Nearly. Keep them off me. | **Same, for both picks**, moved to notch 2 | Notch 2 is now the crisis turn (breachers one move from the held pick) |
| M3.1.4 Mark | It's open! Now the big one! | **Same, for both picks**, moved to notch 3 (the roll and the release) | D-732 kept: always plays, no branch. D-749: John says it too |
| M3.2.1, M3.2.2 | w2 / w3 lines | **Same, same notches** | — |
| M3.3.1 Linda | A barricade's down! They're coming through! | **Same** | — |
| M3.3.2 Lucy | Get away from him! | **Same.** Trigger: first enemy attack on the held pick | "him" fits both |
| M3.3.3 Mark | Still pushing. | **Same, for both picks** (one CSV row per character, same text) | D-749 |
| M3.4.1 to M3.4.4 | Tally barks | **Same** | — |
| M3.5.1 to M3.5.8 | The end | **Same** | D-734 kept |
| M3.5.9 Mark | We follow. Stay sharp. | **Same, for both picks**, now a pick line | Fits John: the father decides and warns his girls |
| M3.6.1 | Hold them off. 4 turns left. | **Dropped** | 3 hold stages (D-742) |
| M3.6.2 to M3.6.4 | 3 turns left / 2 turns left / Last turn. | **Same text**, now S3, S4, S5 | — |
| M3.6.5 | Finish them. | **Same**, now S6 | — |
| M3.6.6 | Keep Mark standing. | **Keep {pick} standing.** | D-745 (rewords D-733) |
| M3.6.7 | Mark has fallen. | **{pick} has fallen.** | D-745 |
| M3.6.8 | Barricade | **Same** | D-731 |
| M3.6.9, M3.6.10 | "Gone" | **Back:** "Clear the yard." (S1), "{pick}: push the stone." (S2) | D-742. Written `{pick}`, the variable `PickOnTilesLOCondition` exposes |

---

## D0. Level start

Order (plan › UX): input off → camera on the stone with the three Claws at it → **M3.0.6** → camera on the west lane (w1) → **M3.0.7**, **M3.0.8** → camera on the yard → objective "Clear the yard." with the defeat line "Keep {pick} standing." → input on. The Masher is hidden; no close-up here.

| ID | Speaker | Trigger | Line | Notes | Status |
|---|---|---|---|---|---|
| M3.0.6 | Linda | Camera on the Claws at the stone | Something's behind that stone. They want it. | Gives the stone a stake before anyone pushes it and sets up the cave line. Doesn't say what or who is inside. Not chosen: Lucy "Why are they scratching at a rock?"; no line | Approved (D-750) |
| M3.0.7 | Lucy | Camera on w1 in the west lane, optional | More at the west wall! | Short, points | Approved (D-750) |
| M3.0.8 | Linda | Same dialog, optional | It'll hold. For now. The yard first. | Heads off "must I kill w1 to clear the yard?" and plants "the wall is your clock" | Approved (D-750) |

Trigger note: D-750's log row says the pair plays "when w1 reaches the wall". In this layout w1 is in play in the west lane from level start, and the level-start camera shows it walking at the wall, so the pair sits in the level-start dialog as drafted. If the build fires it later (w1's first hit on a west barricade), the text is unchanged.

Cut order: M3.0.7 and M3.0.8 together (the objective text still names the yard), then M3.0.6.

```csharp
Line(Who.Linda, Side.Left, "Something's behind that stone. They want it."), // M3.0.6
Line(Who.Lucy, Side.Right, "More at the west wall!"),                        // M3.0.7, optional
Line(Who.Linda, Side.Left, "It'll hold. For now. The yard first."),          // M3.0.8, optional
```

## D1. S1 complete: the cave

Camera on the stone → the pick's line → 4,11 lights → objective "{pick}: push the stone.".

| ID | Speaker | Trigger | Line | Notes |
|---|---|---|---|---|
| M3.0.2 | The pick (both) | "Clear the yard." complete, camera on the stone | A cave behind this stone. I'll shift it. | One text for both picks (D-749). The pick is 1 to 4 tiles from the stone, so "this stone" reads |

## D2. S2 complete: the push, the Masher

Order (plan › Stages S2): the pick reaches 4,11 and is held → input off → camera on the east lane → the Masher revealed, close-up → **M3.0.1** → camera on the pick at the stone → **M3.0.3** → **M3.0.4**, **M3.0.5** → camera back → objective "Hold them off. 3 turns left." → input on.

| ID | Speaker | Trigger | Line | Notes |
|---|---|---|---|---|
| M3.0.1 | Linda | Masher close-up | Every hit brings that one a step closer. | Not a pick line |
| M3.0.3 | The pick: **Mark** | Camera on the pick at the stone | I can't push and fight. Keep them off me. | **The one pick line with two texts (D-749).** It teaches the rule |
| M3.0.3 | The pick: **John** | Same | I can't push and shield you. Keep them off me. | Names what John gives up, his shield (his zone is off while held, D-744): answers "is John still covering people?" |
| M3.0.4 | Linda | Same dialog | Keep them off him, Lucy! | — |
| M3.0.5 | Lucy | Same dialog, optional | And keep count, sister. | At the push it reads as a jab ("keep up"), the tally already running |

Cut order: M3.0.5, then M3.0.4. M3.0.3 is the last to cut (it is the rule).

```csharp
Line(Who.Linda, Side.Left, "Every hit brings that one a step closer."),  // M3.0.1, Masher close-up
// pick slot (SpeakAsThePick), M3.0.3:
//   Mark: "I can't push and fight. Keep them off me."
//   John: "I can't push and shield you. Keep them off me."
Line(Who.Linda, Side.Left, "Keep them off him, Lucy!"),                   // M3.0.4
Line(Who.Lucy, Side.Right, "And keep count, sister."),                    // M3.0.5, optional
```

## D3. The pick on each notch

Each notch: camera on the stone → notch → the pick's line → (wave arrival, §D4, on notches 1 and 2) → camera back. One text for both picks (D-749).

| ID | Trigger | Line | Notes |
|---|---|---|---|
| M3.1.1 | Notch 1 (P+1 start), before w2 | It moves. | — |
| M3.1.3 | Notch 2 (P+2 start), before w3: the crisis turn | Nearly. Keep them off me. | The second and last time the pick asks for help |
| M3.1.4 | Notch 3 (P+3 start): the stone rolls away, the pick is released; **always**, Masher alive or dead (D-732) | It's open! Now the big one! | Also the pick rejoining. Then "Finish them." |

(M3.1.2 "Halfway. Hold them." is dropped: notch 2 of 3 is not halfway.)

```csharp
// pick slot (SpeakAsThePick), one text for both picks
"It moves."                    // M3.1.1, notch 1
"Nearly. Keep them off me."    // M3.1.3, notch 2
"It's open! Now the big one!"  // M3.1.4, notch 3, always
```

## D4. Wave arrivals

w1 is in the west lane from level start. w2 on notch 1, w3 on notch 2.

```csharp
Line(Who.Lucy, Side.Right, "More from the east! Mine!"),           // M3.2.1, w2, notch 1
Line(Who.Linda, Side.Left, "Both lanes at once. Try to keep up."), // M3.2.2, w3, notch 2
```

## D5. Barks: hold events and the tally race

Non-blocking barks; the build needs a trigger for each it can hear. If a trigger isn't cheap, the row is dropped (the build's call), not reworded. M3.3.3 is one row per character with the same text; only the pick on the board can say it (if the bark system doesn't filter by who is present, that's the build's call). Tags are suggestions.

| ID | Speaker | Trigger | Line |
|---|---|---|---|
| M3.3.1 | Linda | First barricade destroyed, either neck, once | A barricade's down! They're coming through! |
| M3.3.2 | Lucy | First enemy attack on the held pick, once, optional | Get away from him! |
| M3.3.3 | Mark or John (the pick) | Reply to M3.3.2, optional | Still pushing. |
| M3.4.1 | Linda | First mushroom blast on an enemy, once (only if cheap) | Mushrooms count, you know. |
| M3.4.2 | Lucy | Same event, reply, optional | Only if you lit it. |
| M3.4.3 | Lucy | Tally lead changes to Lucy, once | One ahead. |
| M3.4.4 | Linda | Tally lead changes to Linda, once | Not for long. |

```csv
Linda,1,TRUE,A barricade's down! They're coming through!,M3_BarricadeDown
Lucy,1,TRUE,Get away from him!,M3_PickHit
Mark,1,TRUE,Still pushing.,M3_PickHitReply
John,1,TRUE,Still pushing.,M3_PickHitReply
Linda,1,TRUE,"Mushrooms count, you know.",M3_MushroomBlast
Lucy,1,TRUE,Only if you lit it.,M3_MushroomReply
Lucy,1,TRUE,One ahead.,M3_LeadLucy
Linda,1,TRUE,Not for long.,M3_LeadLinda
```

## D6. End

Order as built: "Finish them." complete → input off, HUD off → the tally alone (`SistersTally ShowAlone`) → **M3.5.1** → tally fades → **M3.5.2** → camera on the cave → Toba revealed → **M3.5.3 to M3.5.9** → outro. The stone already rolled away on notch 3.

| ID | Speaker | Line | Notes |
|---|---|---|---|
| M3.5.1 | Linda | Still counting? | D-624 |
| M3.5.2 | Lucy | …No. | D-624; the single ellipsis character U+2026 |
| M3.5.3 | Toba | You moved the stone. Thank you. | D-734; fits either pick |
| M3.5.4 | Linda | Who are you? | — |
| M3.5.5 | Toba | I am Toba. I know the way to the Rootwell. | Canon (the Rootwell), nothing new claimed |
| M3.5.6 | Toba | And I know where Ryker is. | Canon (Ryker) |
| M3.5.7 | Lucy | Ryker? Where is she? | — |
| M3.5.8 | Toba | I will take you. Follow me. | Canon (Toba's role) |
| M3.5.9 | The pick (both) | We follow. Stay sharp. | D-734; one text for both picks (D-749). Accepts the help, not the man: Toba is not yet family (D-048) |

```csharp
Line(Who.Linda, Side.Left, "Still counting?"),                          // M3.5.1
Line(Who.Lucy, Side.Right, "…No."),                                     // M3.5.2
Line(Who.Toba, Side.Right, "You moved the stone. Thank you."),          // M3.5.3
Line(Who.Linda, Side.Left, "Who are you?"),                             // M3.5.4
Line(Who.Toba, Side.Right, "I am Toba. I know the way to the Rootwell."), // M3.5.5
Line(Who.Toba, Side.Right, "And I know where Ryker is."),               // M3.5.6
Line(Who.Lucy, Side.Right, "Ryker? Where is she?"),                     // M3.5.7
Line(Who.Toba, Side.Right, "I will take you. Follow me."),              // M3.5.8
// pick slot (SpeakAsThePick): "We follow. Stay sharp."                 // M3.5.9
```

(Toba's lines are seeded through `SpeakAsToba` as built; there is no `Who.Toba` in the shared writer. The builder may move Lucy Left for M3.5.7.)

## D7. On-screen text

| ID | Where | Text | Status |
|---|---|---|---|
| M3.6.9 | Objective S1 | Clear the yard. | Approved |
| M3.6.10 | Objective S2 (4,11 lit) | {pick}: push the stone. | Approved; `{pick}` = the pick's nickname, as `PickOnTilesLOCondition` exposes it |
| M3.6.2 | Objective S3 (on the push) | Hold them off. 3 turns left. | Approved |
| M3.6.3 | Objective S4 (notch 1) | Hold them off. 2 turns left. | Approved |
| M3.6.4 | Objective S5 (notch 2) | Hold them off. Last turn. | Approved |
| M3.6.5 | Objective S6 (notch 3) | Finish them. | Approved |
| M3.6.6 | Defeat group's objective text, shown from level start | Keep {pick} standing. | Approved (D-745) |
| M3.6.7 | Defeat group's defeat message | {pick} has fallen. | Approved (D-745) |
| M3.6.8 | Barricade unit title | Barricade | Approved (D-731) |

If a defeat objective can't show `{pick}` (plan T-P4), this comes back to THJ; the plan's fallback "Keep the pusher standing." is not approved.

## D8. Line map for the build

One text per slot. The one exception is the M3.0.3 push line, which has a Mark text and a John text (D-749). Slot names are today's (`MissionWiring.HoldTheYard.Sequences.cs`, the Mark-placed wiring); the tech plan may rename or replace them for the stages above. Every placeholder in the middle column is replaced.

| Stage / slot | Today's placeholder | Becomes |
|---|---|---|
| Level start (today: camera on the Masher, the east wall, Mark) | `MarkStartLine` "There's a cave behind that stone. I'll shift it." / `LindaStartLine` "Keep them off him!" | Stone and Claws → M3.0.6 Linda "Something's behind that stone. They want it."; west lane → M3.0.7 Lucy "More at the west wall!", M3.0.8 Linda "It'll hold. For now. The yard first." (both optional). No Masher, no pick line |
| S1 complete (new) | none | M3.0.2 pick "A cave behind this stone. I'll shift it." |
| S2 complete (new) | none | Masher close-up → M3.0.1 Linda "Every hit brings that one a step closer."; M3.0.3 pick: **Mark** "I can't push and fight. Keep them off me." / **John** "I can't push and shield you. Keep them off me."; M3.0.4 Linda "Keep them off him, Lucy!"; M3.0.5 Lucy "And keep count, sister." (optional) |
| Notch 1 | none | M3.1.1 pick "It moves."; then w2 → M3.2.1 Lucy "More from the east! Mine!" (`Wave2Line`) |
| Notch 2 | none | M3.1.3 pick "Nearly. Keep them off me."; then w3 → M3.2.2 Linda "Both lanes at once. Try to keep up." (`Wave3Line`) |
| Notch 3 (roll, release) | `Notch3Line` "It's moving... keep them off me!" | M3.1.4 pick "It's open! Now the big one!", always |
| Notch 4 | `Notch4Line` "It's open! The big one's at the wall!" | **Gone** (no notch 4) |
| Bark events | none | M3.3.1 Linda "A barricade's down! They're coming through!"; M3.3.2 Lucy "Get away from him!"; M3.3.3 "Still pushing." (a Mark row and a John row, same text); M3.4.1 to M3.4.4 as §D5 (only if cheap) |
| End | `StillCountingLine`, `NoLine`, `TobaLines` ("You held them. Good." / "I know the way to the Rootwell. And where Ryker is.") | M3.5.1 to M3.5.8 as §D6; M3.5.9 pick "We follow. Stay sharp." in the pick slot (not `Who.Mark`) |
| Objectives | "Hold them off (4)" … / "Finish them." | M3.6.9 "Clear the yard."; M3.6.10 "{pick}: push the stone."; M3.6.2 "Hold them off. 3 turns left."; M3.6.3 "Hold them off. 2 turns left."; M3.6.4 "Hold them off. Last turn."; M3.6.5 "Finish them." |
| Defeat group (the pick falls) | Mark's group | M3.6.6 "Keep {pick} standing."; M3.6.7 "{pick} has fallen." |
| Barricade title | "Barricade" | M3.6.8 "Barricade" |

## D9. Glossary rows (applied to `glossary.md` 2026-11-26, section "M3: Hold the yard")

| Term | Row | Status |
|---|---|---|
| **the stone** | The rock on the cave mouth at 4,12. The pick walks to the push tile below it and is held there, out of combat; one notch at each family turn start for 3 turns, then it rolls away and the pick rejoins. Unit title "Stone" (placeholder). Not "Fallen Rock" (M1) | Applied (replaces "Mark pushes… for 4 turns") |
| **the pick** (design word) | The free squad seat, John or Mark, chosen on the Trail's roster; back in M3 as the one who pushes the stone. On screen only as `{pick}`. Pick lines go through the pick's dialogue slot, one text for both picks except M3.0.3 (D-749) | Applied |
| **Hold the yard** | Level prefab `GB_m3-defence` (grid block `m3-defence-4`); was wrongly `GB_m3-defence-3` (a grid block name, not a prefab) | Applied (fix) |
| **Masher Goblin** (Enemies row) | M3: hidden until the pick reaches the push tile, then revealed with its close-up at the bottom of the east lane | Applied |
| **Barricade**, **the wall** | Unchanged | — |
| **Toba, Rootwell, Ryker** | Still proposed (`m4-text.md` §6, `m1-ridge-redesign-text.md` §10); no canon change | Not applied |

## D10. Questions for THJ (answered 2026-11-26)

- **Q1 · Can a pick line have two texts?** Answer **(b)** (D-749): Mark's lines for both picks, except M3.0.3, where John says "I can't push and shield you. Keep them off me.". The other John versions are dropped, including the John bark text (his M3.3.3 row says "Still pushing.").
- **Q2 · The new level-start line.** Answer **(a)** (D-750): Linda "Something's behind that stone. They want it.", and the west-wall pair M3.0.7/M3.0.8 kept.
- **Q3 · John's notch-3 line.** Follows from Q1: Mark's "It's open! Now the big one!" for both (D-749).
- Loss texts: "Keep {pick} standing." / "{pick} has fallen." (D-745). Stages and countdown as drafted.

---

## History

- **Mark on the stone** (approved 2026-11-26, D-731 to D-735; parked by D-739 and D-741; superseded by this revision): squad Linda and Lucy only, Mark placed on the stone as `Who.Mark`, four notches, the Masher close-up and Mark's lines at level start, "Keep Mark standing." / "Mark has fallen.". Every line of it that survives is in the tables above word for word (the changes table lists each one); the ones dropped are M3.1.2 "Halfway. Hold them." and M3.6.1 "Hold them off. 4 turns left.". Its full text, alternatives and answered questions are in this file's history in the `claude-handoff` repo (before the 2026-11-26 approval of this revision).
- **2026-11-25 draft** (old level `m3-defence`: yard opening with the Masher, John or Mark as the pick, 3 notches, "Hold them off (1/3)"): superseded on 2026-11-26. Its surviving lines became M3.0.2, M3.0.4, M3.0.5, M3.1.1, M3.2.1, M3.2.2 and the end; full text in the same history.
- Not covered by this file: M3-07 Home, the Heavenly Sword's pickup text, the Masher's own barks, all Toba lines after the fade.
