# M1 "The Ridge" redesign: lines and tutorial pages

Owner: miso-narrative. Scope `thj/onboarding-demo`. Written 2026-11-24 for the approved redesign (`plans/2026-11-24-m1-ridge-redesign.md`, D-648 to D-653).
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

Order (plan §5, §7): input and HUD off → camera to the clue → sighting lines → camera back → Linda rushes → walk → shake → rock on 5,-5 → rock lines → camera on the pocket, Claws revealed → Claw lines → Watch page (D-652). The intro ends there; the enemy turn comes next.

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

## 2. Watch tutorial page (beat 4, D-652)

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
| 3.1 | 5 | Stage S1 `onCompleteSequence` (`TurnReached` 1), camera on Mark, before `SelectUnitSequence` Mark and the pan to 7,-2 | Mark (L) | Hold on, Linda! I see a way. | **Rec.:** the camera pan to 7,-2 that follows shows "the way". B "Hold on, Linda! I'm coming." (warmer, but he doesn't reach her this turn). C "Hold on. I'll clear you a path." (calm Mark) |
| 3.2 | 5 | Same dialog | Linda (R) | Then move, little brother! | Optional, recommended: her bar is locked, and this tells the player it's Mark's turn, in her voice (UX critic: "Linda's empty bar looks like a bug") |
| 3.3 | 5 | Stage S2 objective text (shown) | Objective | Mark: reach the ledge. | The plan's text, kept. Replaces 3.1b's "Get past the Masher." |
| — | 5 | Mark steps onto 7,-2 and picks up her arrows | (hand-back) | *No new line* | The built hand-back plays by itself: Mark "Yours, sister." / "Nothing is lost." / "It returns to you.", Linda "Thank you, Mark." (`HandBackLines.cs`, still `[PLACEHOLDER]`). That covers the critic's "Your arrows, Linda." moment |

## 4. Before Linda's bar unlocks (beat 5 → 6)

Stage S2 `onCompleteSequence`, before `UnlockAbilitiesSequence`. As briefed, Mark also says the plateau Claws are asleep here (they've been on screen since the start and didn't move on enemy turn 1, and the Unaware tag is hidden, D-645). §5 repeats it in other words when the camera actually goes up there.

| # | Beat | Hangs on | Speaker (side) | Rec. line | Alternatives / notes |
|---|---|---|---|---|---|
| 4.1 | 5 → 6 | `M1Ridge_Catch_DialogNodeSequence` (S2 complete) | Mark (L) | The ones up top are asleep. These aren't. | B "Leave the sleepers up top. These two first." (more of an order). If THJ wants the asleep line only at §5, cut 4.1 |
| 4.2 | 6 | Same dialog | Mark (L) | Shoot at me, through them. I'll send it back. | **Rec.:** says what the return preview will show before she aims (UX), and it still reads as advice if S2 completed on its turn fallback with Mark out of line. B "Linda! Shoot through them. I'll send it back." (the plan's line; it assumes he's already in line) |
| 4.3 | 6 | Same dialog, last line; then unlock, `SelectUnitSequence` Linda, `GuidedAbilityHint` on her bow | Linda (R) | Gladly. | **Rec.:** 3.1b's paper line, a sister happy to aim at her brother. B "Don't you dare drop it." (teases, and plants the catch) |

## 5. Pocket cleared (S3): fallback for Catch & Return, reunion, plateau, Counter

Stage S3 `onCompleteSequence` (the three pocket Claws destroyed). D-653: these ship first, in place of a trigger on the catch. **They must be true whether the catch fired or not** (plan §3, beat 7), so they react to saving each other across the gap, not to the catch itself. They stay true once the trigger exists (§7), so nothing needs rewriting then.

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

## 6. Low HP, fallback bark (beat 8, D-653)

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

## 7. Final variants for the trigger component (later chunk, D-653)

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
| The rock unit's name (Neutral `GUnit` on 5,-5, D-650), if hover or a card ever shows it | Fallen Rock | "Boulder", "Rockfall". Only matters if the name shows anywhere (plan: "to check: no HP bar or hover clutter") |

---

## 10. Glossary changes (proposed, not applied until THJ approves the text)

| Term | Proposal |
|---|---|
| **Ryker** | Add under a new "Story" table: the one the family is searching for after the Hearth ("Ryker's gone"; "Then we find her. Together."); she. Already on screen (`SearchWiring.River.cs`, `HomeVisitsWiring.Hearth.cs`). Canon status unknown: mark it Miso-only until THJ says otherwise |
| **Health Potion** | Add to the combat terms: item `Bergsons_Ability_HealthPotion`, title "Health Potion"; "potion" in speech. M1 starts with one (`initialItemsAvailability`) |
| **Counter** (Mark's Family Role) | Add to the combat terms as a design word: GDD `characters/mark.md` calls Mark's role Counter. On screen the page title is "Mark's Family Role" and lines don't name it. Ask THJ whether "Counter" becomes a screen name (like Watch) or stays a design word |
| **FP on tutorial pages** | Add a note to the FTP row: Mark's and Lucy's Role pages and the Trail's pass-by page still say "family time point"; new pages write "FP" (pending THJ, §2) |
| **Fallen Rock** | Only if THJ approves §9 |
