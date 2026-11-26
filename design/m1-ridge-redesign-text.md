# M1 "The Ridge" redesign: lines and tutorial pages

Owner: miso-narrative. Scope `thj/onboarding-demo`. Written 2026-11-24 for the approved redesign (`plans/2026-11-24-m1-ridge-redesign.md`, D-662 to D-667).
Status: **proposed, waiting on THJ.** Every line here is Tier 3 until he approves it.

How to paste:
- **Dialogue** (`DialogNodeSequence`, `Line(Who.X, Side.Y, "...")`): paste the line **without** a tag. Dialogue shows `[PLACEHOLDER]` on screen and the onboarding tests forbid it (`conventions.md` › Text, D-348). This file is the placeholder list until THJ signs off.
- **Barks** (CSV rows): keep the `[PLACEHOLDER] ` prefix; the bark system strips it.
- **Tutorial pages** (`TutorialDataSO`): the YAML form is given so it pastes straight into `pageText` (same shape as `Ridge_Start_Panels` / `River_Start_Panels`).
- Sides follow `MissionWiring.Ridge.cs`: **Mark Left, Linda Right.**
- **Rec.** is the line to paste. The alternatives are for THJ; one line on the feel of each.
- Sequence asset names in "Hangs on" are suggestions in the `M1Ridge_` style; the implementer may name them differently.

Voice: Linda is the older sister, quick and proud ("Keep up, little brother", "I hate waiting"). Mark is the younger brother, calm and sure of himself, with a monk's short sentences ("Mind before fist") and a dry streak ("In my version, you did"). They're searching for Ryker (Lucy left to find her at the end of the Hearth). Lines stay under about 55 characters so they fit a bubble.

---

## 1. Intro (`M1Ridge_Start_SequentialSequence`)

Order (plan §5, §7): input and HUD off → camera to the clue → sighting lines → camera back → Linda rushes → walk → shake → rock on 5,-5 → rock lines → camera on the pocket, Claws revealed → Claw lines → Watch page (D-666). The intro ends there; the enemy turn comes next.

| # | Beat | Hangs on | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|---|---|
| 1.1 | 1 Arrival | After the camera reaches the clue (≈2,6). `M1Ridge_Start_Sighting_DialogNodeSequence` | Linda (R) | There. Up on the ridge. Tracks. | "Mark. Look, up there." (softer, makes him look). Either way, she sees it first: she's the one who runs |
| 1.2 | 1 | Same dialog | Mark (L) | Too big to be hers. | "Someone came this way. Not long ago." (plainer, no Ryker). Rec. ties the tracks to the search and plants the man the outro reveals |
| 1.3 | 1 | Same dialog | Linda (R) | Then whose? | Optional. Cut it if the intro feels long; 2.1 follows on fine without it |
| — | | Camera back to the pair | | | |
| 2.1 | 2 Rush | `M1Ridge_Start_Rush_DialogNodeSequence`, before `MoveUnitSequence` | Linda (R) | I'll check it out. | THJ's own words, kept |
| 2.2 | 2 | Same dialog | Mark (L) | Careful. The rock up here is loose. | **Rec.:** foreshadows the fall, so it reads as earned, not random. B "Linda, wait. Look before you run." (the brother who thinks first). C "Slow down. This ridge doesn't forgive." (more dread) |
| 2.3 | 2 | Same dialog, last line | Linda (R) | Keep up, little brother. | Optional. Callback to 3.1b's opening line; she's already running as she says it |
| — | | `MoveUnitSequence` Linda 5,-5 → 3,-2, then `CFXSequence` shake, then the rock revealed on 5,-5 | | | |
| 2.4 | 2 Rockfall | `M1Ridge_Start_Rockfall_DialogNodeSequence`, after the rock lands | Linda (R) | Mark?! | The plan's cue, kept |
| 2.5 | 2 | Same dialog | Mark (L) | Still here! But I can't get to you. | **Rec.:** says the problem in plain words and sets up beat 5. B "I'm fine! The way's blocked." (shorter, less fear). C "Here! Stay put. I'll find a way round." (Mark takes charge; but "round" promises a path he doesn't have this turn) |
| — | | Camera on the pocket, `RevealUnitsSequence` group `fall` | | | |
| 2.6 | 2 Claws | `M1Ridge_Start_Claws_DialogNodeSequence` | Mark (L) | Claws! The noise woke them. | Explains why they appear (the rockfall), as the plan wants |
| 2.7 | 2 → 4 | Same dialog, last line before the page | Linda (R) | Let them come. Anything in my line gets an arrow. | **Rec.:** the old Role line, reworded; it hands straight over to the Watch page. B "Good. I hate waiting." (the first Ridge's line; pure attitude, teaches nothing) |
| 2.8 | 4 Watch page | `TutorialSequence` + new `TutorialDataSO` (suggested name `M1Ridge_Watch_Panels`), last step of the intro | Page | See §2 | |

## 2. Watch tutorial page (beat 4, D-666)

Same shape as `Ridge_Start_Panels` ("Mark's Family Role") and `River_Start_Panels` ("Lucy's Family Role"): a "<Name>'s Family Role" title, two bullets, what it does first, then the key and the cost.

| Field | Rec. | Notes |
|---|---|---|
| pageTitle | Linda's Family Role | Matches the other two Role pages. B "Family Watch" (the role's screen name, D-328) |
| pageText | • On the enemies' turn, when an enemy ends its move in Linda's row or column, within her bow's range, she can shoot it. This is her Watch.<br>• Press the key shown above her, and be quick. Each shot costs 1 FP and an arrow, but no action points. | "Be quick": the prompt is real time with a 1 s window (FR-2). "1 FP": see the FP note below |

YAML to paste:

```yaml
  pages:
  - pageTitle: Linda's Family Role
    pageType: 0
    videoClip: {fileID: 0}
    image: {fileID: 21300000, guid: 2097e2cde38afeb49a8ae81a6fc4246f, type: 3}
    pageText: "• On the enemies' turn, when an enemy ends its move in Linda's
      row or column, within her bow's range, she can shoot it. This is her Watch.\n•
      Press the key shown above her, and be quick. Each shot costs 1 FP and an arrow,
      but no action points."
```

(The image GUID is the placeholder sprite the other Role pages use.)

**FP note for THJ.** The glossary says the HUD writes **Family Points (FP)** (D-204), but the three older pages (Mark's and Lucy's Role pages, the Trail's pass-by page) still say "family time point". The Rec. uses "FP", to match the HUD. If THJ would rather match the older pages for now, swap in "1 family time point". Either way, those three pages should be brought in line later.

## 3. First family turn: Mark alone (beat 5)

| # | Beat | Hangs on | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|---|---|
| 3.1 | 5 | Stage S1 `onCompleteSequence` (`TurnReached` 1), camera on Mark, before `SelectUnitSequence` Mark and the pan to 7,-2. *(As built, it opens the Catch dialog instead; replaced there by §11 C1.)* | Mark (L) | Hold on, Linda! I see a way. | **Rec.:** the camera pan to 7,-2 that follows shows "the way". B "Hold on, Linda! I'm coming." (warmer, but he doesn't reach her this turn). C "Hold on. I'll clear you a path." (calm Mark) |
| 3.2 | 5 | Same dialog | Linda (R) | Then move, little brother! | Optional, recommended: her bar is locked, and this tells the player it's Mark's turn, in her voice (UX critic: "Linda's empty bar looks like a bug") |
| 3.3 | 5 | Stage S2 objective text (shown) | Objective | Mark: reach the ledge. | The plan's text, kept. Replaces 3.1b's "Get past the Masher." |
| — | 5 | Mark steps onto 7,-2 and picks up her arrows | (hand-back) | *No new line* | The built hand-back plays by itself: Mark "Yours, sister." / "Nothing is lost." / "It returns to you.", Linda "Thank you, Mark." (`HandBackLines.cs`, still `[PLACEHOLDER]`). That covers the critic's "Your arrows, Linda." moment |

## 4. Before Linda's bar unlocks (beat 5 → 6)

> **Replaced (2026-11-24, after THJ's playtest):** the built Catch dialog (3.1 + 4.2 + 4.3, as wired in `MissionWiring.Ridge.Sequences.cs`) is superseded by §11. The lines below are kept for the record.

Stage S2 `onCompleteSequence`, before `UnlockAbilitiesSequence`. As briefed, Mark also says the plateau Claws are asleep here (they've been on screen since the start and didn't move on enemy turn 1, and the Unaware tag is hidden, D-645). §5 repeats it in other words when the camera actually goes up there.

| # | Beat | Hangs on | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|---|---|
| 4.1 | 5 → 6 | `M1Ridge_Catch_DialogNodeSequence` (S2 complete) | Mark (L) | The ones up top are asleep. These aren't. | B "Leave the sleepers up top. These two first." (more of an order). If THJ wants the asleep line only at §5, cut 4.1 |
| 4.2 | 6 | Same dialog | Mark (L) | Shoot at me, through them. I'll send it back. | **Rec.:** says what the return preview will show before she aims (UX), and it still reads as advice if S2 completed on its turn fallback with Mark out of line. B "Linda! Shoot through them. I'll send it back." (the plan's line; it assumes he's already in line) |
| 4.3 | 6 | Same dialog, last line; then unlock, `SelectUnitSequence` Linda, `GuidedAbilityHint` on her bow | Linda (R) | Gladly. | **Rec.:** 3.1b's paper line, a sister happy to aim at her brother. B "Don't you dare drop it." (teases, and plants the catch) |

## 5. Pocket cleared (S3): fallback for Catch & Return, reunion, plateau, Counter

Stage S3 `onCompleteSequence` (the three pocket Claws destroyed). D-667: these ship first, in place of a trigger on the catch. **They must be true whether the catch fired or not** (plan §3, beat 7), so they react to saving each other across the gap, not to the catch itself. They stay true once the trigger exists (§7), so nothing needs rewriting then.

Order: lines → FTP top-up (framed as the reunion: the "breathe" line comes right before it) → Continuous Attack back on → camera up to the plateau → asleep line → Counter line.

| # | Beat | Hangs on | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|---|---|
| 5.1 | 7 (fallback) | `M1Ridge_Cleared_DialogNodeSequence` | Mark (L) | Rock between us. Didn't matter. | The nod to the catch: they fought as one across the gap, whether the catch happened or not |
| 5.2 | 7 | Same dialog | Linda (R) | Next time, I'll wait for you. | |
| 5.3 | 7 | Same dialog | Mark (L) | No, you won't. | **Set A (Rec.):** owns her rush, a laugh after the scare. **Set B:** Linda "You came for me." / Mark "You'd have done the same. Louder." (warmer). **Set C:** Mark "Still standing?" / Linda "Thanks to you. Don't let it go to your head." / Mark "Too late." (lighter) |
| 5.4 | Reunion (FTP top-up) | `M1Ridge_Reunion_DialogNodeSequence`, just before the `SignalSequence` that runs the +99 filler | Mark (L) | Breathe, sister. Then we climb. | Frames the refill as Mark steadying her, not as a resource. B "Meet me at the top." (plainer) |
| 5.5 | Reunion | Same dialog | Linda (R) | Race you to the top. | A nod to their Duo ("the race"). Two lines, as the critic asked |
| — | | Continuous Attack on, camera up to the plateau and its three Claws | | | |
| 5.6 | 9 | `M1Ridge_Plateau_DialogNodeSequence` | Mark (L) | Three more, still asleep. Pick your ground before they wake. | **Rec.:** names the setup turn the plan builds in ("a cautious player gets a setup turn"). B "They're asleep up there. Get set before they wake." (the plan's line). Different words from 4.1 on purpose |
| 5.7 | 9 Counter | Same dialog | Mark (L) | Stay close to me. Whatever hits you answers to me. | **The one Counter line (no page, plan §8).** "Stay close" teaches the range, "hits you" the trigger. **Rec.** keeps the old Role line's shape. B "Stand near me, and nothing hits you for free." (shorter, wry). C "Stay in reach. If they strike you, I strike them." (most literal) |
| 5.8 | 9 (optional) | Same dialog | Linda (R) | Or I keep my distance, and you catch. | **Optional, THJ's call.** Names the other answer (apart: the catch line), so the plateau reads as a choice. Without it, the choice is left for players to find, which may be the point |
| 5.9 | 9 (optional, with 5.8) | Same dialog | Mark (L) | Your call, sister. | Only with 5.8 |

Objective S4: **Clear the ridge. {alive_0} remaining.** (as built, kept).

## 6. Low HP, fallback bark (beat 8, D-667)

`HPBelowPercent` 50 on a Bergson, `PlayOnce` TRUE, M1 only if the bark graph can be scoped to the level (otherwise it plays the first time in any mission, which still reads fine). Recommended: the **other** sibling speaks, since a nudge from family is warmer and the hurt one is the one who should act. If the graph can only make the hurt unit speak, use the self rows.

CSV rows (`Unit,Weight,PlayOnce,Dialogue,Tag`; tag name `LowHP` is a suggestion):

```csv
Mark,1,TRUE,[PLACEHOLDER] Linda! Drink a potion. Now.,LowHP_Other
Linda,1,TRUE,"[PLACEHOLDER] Mark, you're hurt. Potion. Now.",LowHP_Other
Linda,1,TRUE,[PLACEHOLDER] I need a potion.,LowHP_Self
Mark,1,TRUE,"[PLACEHOLDER] A potion, then back to it.",LowHP_Self
```

| Who speaks | Rec. | Alternatives / notes |
|---|---|---|
| Mark, when Linda is low | Linda! Drink a potion. Now. | "You're bleeding. Drink something!" (closer to the plan's "Linda, drink something!", but "potion" points to the item) |
| Linda, when Mark is low | Mark, you're hurt. Potion. Now. | "Drink a potion, you stubborn monk." (more teasing) |
| Self, Linda | I need a potion. | |
| Self, Mark | A potion, then back to it. | |

"Potion" in speech; the item is **Health Potion** on screen (`Bergsons_Ability_HealthPotion`, title "Health Potion").

**Suggestion for THJ (fallback gap).** The bark alone doesn't say *where* the potion is. If that worries him, a one-page potion tutorial (§7.2's page) could ship now inside S3's sequence (the pocket cleared, just before the plateau, where low HP is most likely) with a built `TutorialSequence`. When the trigger lands, the page moves to it.

---

## 7. Final variants for the trigger component (later chunk, D-667)

For the small non-core trigger (synergy by id, ability used, HP threshold). Not for the first M1 build.

### 7.1 Catch & Return trigger

Fires on the first `"Catch & Return"` synergy in M1, after the returned arrow lands. A non-blocking bubble is best (as the hand-back is), so the player's turn keeps going; a short `DialogNodeSequence` works too. §5's lines stay as they are.

| # | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|
| 7.1a | Mark (L) | Told you I'd send it back. | **Set A (Rec.):** keeps 4.2's promise, and Linda's reply invites a second catch, which teaches it twice |
| 7.1b | Linda (R) | Again. Do that again. | |
| | | | **Set B:** Linda "You caught it?" / Mark "I always catch it." (Mark smug, Linda surprised). **Set C:** Mark "Out through them, home to you." / Linda "Not bad, little brother." (warm, a little poetic). Avoid "Show-off." here: it's already Linda's hand-back reply to Lucy |

### 7.2 First low HP → line and potion page

The first time a sibling's HP falls to 50% or less; plays at the next family turn start (plan §3, beat 8), never mid-enemy-turn. Replaces §6's bark in M1.

| # | Hangs on | Speaker (side) | Rec. line | Notes |
|---|---|---|---|---|
| 7.2a | Trigger sequence, if Linda is the one hurt | Mark (L) | You're hurt. Drink a potion before you do anything brave. | Affectionate dig at her rush. B "You're hurt. Drink a potion. Now." |
| 7.2b | Trigger sequence, if Mark is the one hurt | Linda (R) | You're bleeding, little brother. Potion first. | B "Mark, you're hurt. Potion. Now." |
| 7.2c | Same sequence, after the line: `TutorialSequence` + new page (suggested `M1Ridge_Potion_Panels`) | Page | See below | Same style as the Trail's "Items" page |

| Field | Rec. | Notes |
|---|---|---|
| pageTitle | Health Potion | The item's title in the bar |
| pageText | • The family carries one Health Potion on this mission.<br>• Select the hurt Bergson, then the Health Potion in the abilities bar. It heals them. | Wording follows the Trail's Items page ("Select a Bergson, then the item in the abilities bar"). No AP or HP numbers: I didn't confirm its AP cost from the asset, and its heal changes with level (10 / 25 / 40) |

```yaml
  pages:
  - pageTitle: Health Potion
    pageType: 0
    videoClip: {fileID: 0}
    image: {fileID: 21300000, guid: 2097e2cde38afeb49a8ae81a6fc4246f, type: 3}
    pageText: "• The family carries one Health Potion on this mission.\n•
      Select the hurt Bergson, then the Health Potion in the abilities bar. It heals
      them."
```

---

## 8. Outro on the clue (`M1Ridge_End_Clue_DialogNodeSequence`)

Camera on the clue, then the lines, then `OutroCutscene` (as 3.1b built). The new version opens with a callback to her rush (beat 1), keeps the facts the Home recap repeats (`HomeVisitsWiring.cs`: "A man's tracks, deep. Carrying something." / "And herbs. A poultice."), and closes on the reunion.

| # | Speaker (side) | Rec. line | Was (3.1b) | Notes |
|---|---|---|---|---|
| 8.1 | Linda (R) | Told you there was something up here. | (new) | Callback to beat 1 |
| 8.2 | Mark (L) | A man's tracks. Deep. He was carrying something. | Same | Kept: the Home recap quotes it |
| 8.3 | Linda (R) | Healing herbs, crushed fresh. And a leaf wrapper. | "Healing herbs, crushed fresh." | Two old lines folded into one |
| 8.4 | Mark (L) | It still smells of salve. He's tending something. | "Someone knew which ones to pick." / "A leaf wrapper. It still smells of salve." / "Whoever he is, he's tending something." | Folded; same facts |
| 8.5 | Linda (R) | Or someone. | (new) | Hope and dread together: is it Ryker? Doesn't say. The Home recap ("Someone's carrying her. And tending her.") pays it off |
| 8.6 | Mark (L) | Next time, we climb together. | (new) | **Close A (Rec.):** the family motif ("Then we follow it. Together." on the Trail) |
| 8.7 | Linda (R) | …Fine. Together. | (new) | |
| | | | | **Close B:** Mark "Let's take this home." / Linda "Race you." (light, calls back 5.5). **Close C:** stop at 8.5 (darkest, shortest). If THJ prefers the old five clue lines unchanged, keep them and add only 8.1 and Close A |

---

## 9. UI label

| Where | Rec. | Alternatives / notes |
|---|---|---|
| The rock unit's name (Neutral `GUnit` on 5,-5, D-664), if hover or a card ever shows it | Fallen Rock | "Boulder", "Rockfall". Only matters if the name shows anywhere (plan: "to check: no HP bar or hover clutter") |

---

## 10. Glossary changes (proposed, not applied until THJ approves the text)

| Term | Proposal |
|---|---|
| **Ryker** | Add under a new "Story" table: the one the family is searching for after the Hearth ("Ryker's gone"; "Then we find her. Together."); she. Already on screen (`SearchWiring.River.cs`, `HomeVisitsWiring.Hearth.cs`). Canon status unknown: mark it Miso-only until THJ says otherwise |
| **Health Potion** | Add to the combat terms: item `Bergsons_Ability_HealthPotion`, title "Health Potion"; "potion" in speech. M1 starts with one (`initialItemsAvailability`) |
| **Counter** (Mark's Family Role) | Add to the combat terms as a design word: GDD `characters/mark.md` calls Mark's role Counter. On screen the page title is "Mark's Family Role" and lines don't name it. Ask THJ whether "Counter" becomes a screen name (like Watch) or stays a design word |
| **FP on tutorial pages** | Add a note to the FTP row: Mark's and Lucy's Role pages and the Trail's pass-by page still say "family time point"; new pages write "FP" (pending THJ, §2) |
| **Fallen Rock** | Only if THJ approves §9 |

---

## 11. Revision 2026-11-24: Catch dialog, in-action version

> **Superseded by §12 (2026-11-24, THJ):** Mark alone, one line, no promise to send it back; Linda says nothing. C1 to C3 below, 7.1a/7.1b and 5.1 to 5.3 are kept for the record only.

THJ after playing: "The dialog lines between catch and return should be shorter and sound more like in action. They now sound as if there are no enemies close by."

Hangs on `M1Ridge_Catch_DialogNodeSequence` (`BuildCatch` in `MissionWiring.Ridge.Sequences.cs`), S2 complete, before the unlock and `SelectUnitSequence` Linda. The pocket Claws are on her, the rock between them. So: combat-bark register, shouted across the gap, a few words a line. They still have to teach the catch (aim at Mark, through the Claws, it comes back) and still read right if S2 ended on its turn fallback with Mark out of line. Mark stays the calm, clipped one; Linda stays proud and teasing, even under pressure. No FP.

| # | Speaker (side) | Replaces | Rec. line | Alternative | Notes |
|---|---|---|---|---|---|
| C1 | Mark (L) | "Hold on, Linda! I see a way." | Linda! Aim at me! | Linda! Over here! | **Rec.** gives the order at once: she aims at *him*. The alt just pulls her eye to him; it could read as "come to me", which she can't |
| C2 | Mark (L) | "Shoot at me, through them. I'll send it back." | Through them. I'll send it back! | Hit them on the way. I'll send it back! | "Send it back" kept on purpose: the later trigger line (7.1a, "Told you I'd send it back.") pays it off. The alt is more explicit about the Claws taking the hit both ways |
| C3 | Linda (R) | "Gladly." | Catch it, little brother! | Don't drop it! | **Rec.** is her voice under fire ("Keep up, little brother") and names the catch. The alt is 4.3's old B, shorter and tenser |

Lines to paste (Rec. set, no tag, per the dialogue rule at the top):

```csharp
Line(Who.Mark, Side.Left, "Linda! Aim at me!"),
Line(Who.Mark, Side.Left, "Through them. I'll send it back!"),
Line(Who.Linda, Side.Right, "Catch it, little brother!"),
```

Two-line cut, if THJ wants it shorter still: drop C1 and open C2 with her name, "Linda! Through them, at me!" then C3. It loses "I'll send it back", so the return preview alone teaches the return.

Status: **proposed, waiting on THJ** (Tier 3, like the rest of this file). The old lines in §3.1, §4.2 and §4.3 are kept above for the record.

---

## 12. Revision 2026-11-24 (2): the surprise catch, and the ambush at the clue

Inputs: THJ's direction of 2026-11-24 on the Catch set-up ("Mark: one line if can't two. Yes cut Linda's reply. Don't hint what Mark is going to do with it, only asking Linda to do it; let it be a surprise for the player. Then their reaction after can adjust to that, like with Linda's surprise but without wanting to admit it directly"), and section 12 of `plans/2026-11-24-m1-ridge-ambush-design.md` (option A approved: plateau kept, then "reach the clue together", then a Black Claw + 4 Dark Claws from behind, the potion page at the end of the ambush sequence).

Rules held: mid-fight register wherever enemies are on the board; Mark calm and clipped, Linda proud and teasing; no FP anywhere; under about 55 characters. Sides as built: **Mark Left, Linda Right.** Dialogue pastes without a tag; barks keep `[PLACEHOLDER] `.

Status: **proposed, waiting on THJ** (Tier 3).

### 12.1 Catch set-up (replaces §11 C1 to C3)

Hangs on `M1Ridge_Catch_DialogNodeSequence` (`BuildCatch`), S2 complete, before the unlock, `SelectUnitSequence` Linda and the `GuidedAbilityHint` on her bow. Mark only. Linda says nothing: she is the player, Mark is guiding. Nothing about catching or sending it back; the return is the surprise.

| # | Speaker (side) | Rec. line | Alternative | Notes |
|---|---|---|---|---|
| K1 | Mark (L) | Linda! Shoot through them. At me! | Linda! Aim at me. Through them! | **Rec.:** the targets first, then the odd part last, so "At me!" lands as the surprise in the order. Alt puts the strange ask first, which makes the player stop and wonder (a little more mystery, a little less clear on the Claws). Both one line, both still read right if S2 ended on its turn fallback with Mark out of line |

Two-line form, if THJ wants a beat of urgency first: Mark "Linda!" / Mark "Through them, at me. Now!"

```csharp
Line(Who.Mark, Side.Left, "Linda! Shoot through them. At me!"),
```

### 12.2 Reaction right after the catch lands (replaces §7.1, for the later trigger chunk)

Fires on the first `"Catch & Return"` in M1, after the returned arrow lands; a non-blocking bubble (as the hand-back) is best, since the turn goes on and the other pocket Claw may still be standing. Linda is surprised and impressed and will not say so; Mark takes it dry and keeps her shooting (the second catch the plan relies on).

| # | Speaker (side) | Rec. line | Alternative | Notes |
|---|---|---|---|---|
| R1 | Linda (R) | Lucky catch. | Huh. You caught it. | **Rec.:** the surprise dressed as a shrug: she won't call it skill. Alt is flatter, the surprise shows a bit more |
| R2 | Mark (L) | Then shoot again. | Shoot again. Before they move. | **Rec.:** dry ("test my luck, then") and it invites the second catch. Alt is more fight-aware, less teasing |

Avoid "Show-off." here: it is already Linda's hand-back reply to Lucy.

### 12.3 Pocket cleared (replaces §5.1 to §5.3; §5.4 onwards kept)

Hangs on `M1Ridge_Cleared_DialogNodeSequence`, S2 complete (the three pocket Claws dead). The plateau sleepers are still up top, so the register stays low and quick. **Must read right whether the catch fired or not** (D-667 fallback): both sets react to Mark asking her to shoot at him, which always happened, and to the surprise without naming it. If the trigger (12.2) ships, these follow it without repeating it.

| # | Speaker (side) | Rec. line (Set A) | Alternative (Set B) | Notes |
|---|---|---|---|---|
| P1 | Linda (R) | Next time, warn me. | You asked me to shoot you. | **Set A (Rec.):** her surprise turned into a complaint: she was caught off guard and won't admit it. **Set B:** she states it as if it were his mistake, works even more plainly without a catch |
| P2 | Mark (L) | You'd have argued. | And you didn't even pause. | A: dry, knows his sister. B: a little dig back, sibling tone |
| P3 | Linda (R) | ...I'd have won. | Don't make it a habit. | A: the last word is hers, still not admitting. B: the same, gruffer |

§5.4 ("Breathe, sister. Then we climb." / "Race you to the top.") and §5.6 to §5.9 (plateau, Counter) follow unchanged.

### 12.4 The ambush at the clue (plan §12, N1 to N11)

| # | Where (plan) | Speaker (side) | Rec. line | Alternative | Notes |
|---|---|---|---|---|---|
| N1 | S3 complete (plateau cleared), camera on the clue | Mark (L) | The tracks, sister. Together this time. | Linda (R): "Now the tracks. I'll even wait for you." | **Rec.:** points up and says "together", which the objective then repeats. Alt: Linda owns her rush from beat 2 with a joke; the "together" lives in the objective only |
| N2 | S4 objective | Objective | Reach the clue together. | Both Bergsons: reach the clue. | Plan's text kept. Alt is more literal if "together" is misread as "one is enough" |
| N3a | Ambush sequence, camera on the clue | Linda (R) | Told you there was something up here. | (cut it) | §8.1 moved here: callback to her rush. Optional if the sequence runs long |
| N3b | Same dialog | Mark (L) | A man's tracks. Deep. He was carrying something. | A man's tracks, deep. Carrying something. | §8.2 moved. The Home recap quotes these facts (`HomeVisitsWiring.cs`). Alt is the recap's exact wording |
| N3c | Same dialog | Linda (R) | Healing herbs, crushed fresh. And a leaf wrapper. | Herbs, crushed fresh. A poultice. | §8.3 moved. Alt matches the recap's "And herbs. A poultice." |
| N4 | Same dialog, last line before the turn-round camera | Linda (R) | Mark. Listen. Behind us. | Mark (L): "We're not alone. Behind us." | **Rec.:** she is the one with sharp eyes (she saw the tracks first); breaks the discovery mid-thought. Alt gives it to the calm one, colder |
| N5 | After `RevealUnitsSequence` `ambush` | Narrator | Black Claw. Hit it, and the pack comes for you. | (none: reused as is) | The Trail's caption (`SearchWiring.Trail.cs` `BlackClawCaption`), reused for M1. Approve it for M1 |
| N6 | After the east-path camera | Mark (L) | Five. Hit the big one only at my side. | They follow the big one. Stay close when you hit it. | **Rec.:** tense, counts them, ties the Black Claw to Counter (stand by me when you hit it). Alt is plainer on the rule, less tense, and doesn't count them |
| N7 | Same dialog (optional) | Linda (R) | Then keep up, little brother. | Five? I've got arrows for six. | **Rec.:** her opening line from the first Ridge, now said shoulder to shoulder. Alt: pure bravado under pressure |
| N8 | Same dialog, last line, just before `SignalSequence` `M1Ridge_Reunion` (optional) | Mark (L) | Breathe. Back to back. | (none: cut the line) | Frames the FTP top-up as the two of them steadying, as §5.4 did ("Breathe, sister"). Cut it if N7 is cut, so Mark doesn't speak twice in a row |
| N9 | Potion page, last step before control returns | Page | See below | | Kept from §7.2c with one change |
| N10 | S5 objective | Objective | Drive them off the ridge. {alive_0} remaining. | Hold the ridge. {alive_0} remaining. | Plan's text kept. Alt is shorter and fits "they came for us" |
| N11 | Outro on the clue, after the win (`M1Ridge_End_Clue_DialogNodeSequence`) | See 12.5 | | | |

Lines to paste for the ambush dialog (Rec. set, no tag; narrator call as the Trail builds it):

```csharp
// discovery (camera on the clue)
Line(Who.Linda, Side.Right, "Told you there was something up here."),
Line(Who.Mark, Side.Left, "A man's tracks. Deep. He was carrying something."),
Line(Who.Linda, Side.Right, "Healing herbs, crushed fresh. And a leaf wrapper."),
Line(Who.Linda, Side.Right, "Mark. Listen. Behind us."),
// after the reveal: the Black Claw caption, as in SearchWiring.Trail.cs
// after the east-path camera
Line(Who.Mark, Side.Left, "Five. Hit the big one only at my side."),
Line(Who.Linda, Side.Right, "Then keep up, little brother."),
Line(Who.Mark, Side.Left, "Breathe. Back to back."),
```

**N9, potion page (`M1Ridge_Potion_Panels`).** One change: "carries one" is false if the family already drank it on the plateau (the low-HP bark can prompt that). "Brought" stays true either way. The rest fits the start of a fight as is.

| Field | Rec. | Was |
|---|---|---|
| pageTitle | Health Potion | Same |
| pageText | • The family brought one Health Potion on this mission.<br>• Select the hurt Bergson, then the Health Potion in the abilities bar. It heals them. | "The family carries one Health Potion on this mission." |

```yaml
  pages:
  - pageTitle: Health Potion
    pageType: 0
    videoClip: {fileID: 0}
    image: {fileID: 21300000, guid: 2097e2cde38afeb49a8ae81a6fc4246f, type: 3}
    pageText: "• The family brought one Health Potion on this mission.\n•
      Select the hurt Bergson, then the Health Potion in the abilities bar. It heals
      them."
```

### 12.5 Outro (N11; replaces §8.1 and §8.4 to §8.7; §8.2 and §8.3 moved to N3)

Camera on the clue after the win, then `OutroCutscene`. "Next time, we climb together" no longer fits (they did). Close on having stood together, then back to the clue for the hope-and-dread hook. I kept the salve line here rather than in N3: the Home recap only quotes the tracks and the herbs, and this gives the outro a reason to look at the clue again.

| # | Speaker (side) | Rec. line (Close A) | Alternative (Close B) | Notes |
|---|---|---|---|---|
| O1 | Linda (R) | Still in one piece, little brother? | Mark (L): "It still smells of salve. He's tending something." | **Close A (Rec.):** sibling check-in after the fight, then the clue, ending dark. **Close B:** clue first, ending on the family motif |
| O2 | Mark (L) | Side by side. Nothing got through. | Linda (R): "Or someone." | A: Mark, quietly proud of "together" |
| O3 | Mark (L) | It still smells of salve. He's tending something. | Mark (L): "Then we follow it. Together." | A: §8.4 kept. B: the Trail's family motif, word for word |
| O4 | Linda (R) | Or someone. | (B ends at O3) | A: §8.5 kept. The Home recap ("Someone's carrying her. And tending her.") pays it off |

### 12.6 What is unchanged

§5.4 to §5.9, §6 (low-HP bark), §9 (Fallen Rock). The Black Claw close-up stays the name only (X-05). Nothing for M3 until its paper level is approved.

---

## 13. Footrace barks (2026-11-25)

THJ: a short bark (floating bubble, one line, not a dialogue panel: "there is already too much dialog happening") when Family Footrace ends, depending on who got there first. The winner speaks; the loser's reply is optional. Each line is 2 to 6 words, sibling teasing, no FP. Status: **proposed, waiting on THJ** (Tier 3).

**Who said "Race you".** As built (`MissionWiring.Ridge.Sequences.cs`, `BuildCleared`) and in §5.5, **Linda** says "Race you to the top." and Mark says "Breathe, sister. Then we climb." The brief for this section had Mark saying it. The lines below are written for the built order (her challenge). If THJ moves "Race you" to Mark, only M-W2's alternative ("You did say race.") needs to change; everything else works either way.

Timing: winner's bubble when the race resolves, the reply about 0.6 s later, non-blocking, the way the hand-back plays. The plateau Claws are still asleep nearby, so the register stays quick and low-key, no shouting.

Avoided on purpose: "Keep up, little brother" (already 2.3 and N7), "Show-off." (Linda's hand-back reply to Lucy), "...I'd have won." (P3), "Side by side" (O2).

| # | Outcome | Speaker | Rec. line | Alternative | Notes |
|---|---|---|---|---|---|
| L-W | Linda wins | Linda | Too slow, little brother. | First. As always. | **Rec.:** her usual "little brother" jab, and she's proud of it. Alt: older-sister smugness, says she's won before |
| L-R | Linda wins (reply, optional) | Mark | You started early. | I let you win. | **Rec.:** dry, and true: she called the race and ran. Alt: the classic little-brother excuse, said deadpan |
| M-W | Mark wins | Mark | Patience climbs faster. | You did say race. | **Rec.:** a monk's short saying, with a dig at her rushing (beat 2). Alt: turns her own challenge back on her (only works while Linda is the one who says "Race you") |
| M-R | Mark wins (reply, optional) | Linda | That one didn't count. | Rematch. After the Claws. | **Rec.:** a sore loser who won't admit it, as in P1 to P3. Alt: she wants another go and keeps the fight in mind |
| T-W | Tie (optional, if the race can end level) | Linda | I was first. | Draw. For now. | Linda speaks first in a tie: she always claims it. **Rec.:** she claims it anyway. Alt: she grudgingly allows a draw, and wants a rematch |
| T-R | Tie (reply, optional) | Mark | We both were. | Together, then. | **Rec.:** calm, and ends the argument. Alt: a quiet nod to "together", which the clue objective uses next (N1, N2) |

CSV rows, if the barks go in the CSV (`Unit,Weight,PlayOnce,Dialogue,Tag`; the tags are suggestions and need a trigger on the race result, which may not exist yet: an implementer question):

```csv
Linda,1,TRUE,"[PLACEHOLDER] Too slow, little brother.",Footrace_LindaWins
Mark,1,TRUE,[PLACEHOLDER] You started early.,Footrace_LindaWins_Reply
Mark,1,TRUE,[PLACEHOLDER] Patience climbs faster.,Footrace_MarkWins
Linda,1,TRUE,[PLACEHOLDER] That one didn't count.,Footrace_MarkWins_Reply
Linda,1,TRUE,[PLACEHOLDER] I was first.,Footrace_Tie
Mark,1,TRUE,[PLACEHOLDER] We both were.,Footrace_Tie_Reply
```

`PlayOnce` TRUE, because the Duo can be used more than once in M1 and the same tease twice would wear thin. If THJ wants a bark every time, set it to FALSE and add the alternatives as second rows (Weight 1 each), so the two lines take turns.
