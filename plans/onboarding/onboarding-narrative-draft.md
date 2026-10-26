# Onboarding first hour · narrative draft (placeholder grade)

Narrative agent, 2026-10-26. Step **A5** of `plans/onboarding/2026-10-25-onboarding-first-hour-workplan.md`. Design: `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` (D-168 to D-180). Branch `thj/onboarding`, scope `all`. Read-only on `miso/`; `glossary.md` unchanged (proposals at the end).

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

## Step 1 · Memory, Linda's version (Linda alone, 4 Dark Claws)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| M1-1 | Linda (off) | The Caeldippo caves. Three Claws, one arrow. That's the whole story. | Level dialogue (start) | Her joke: modest words, impossible claim |
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
| M2-2 | Lucy (off) | And then more came. At least ten! | Interruption (spawn on cue) | **Key line** from the design. Freeze, camera to the spawn points, `GUnitSpawn` |
| M2-3 | Linda (off) | There were four. | Interruption | |
| M2-4 | Lucy (off) | *Ten.* | Interruption | Spawn plays on this line, then resume |
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

## Step 5 · Hearth close (Home state; `FirePlace` / `MoreFire`, then `WolfSitDoor`; night; morning)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| H5-1 | Margaret | Every one of you saved her. That's the only version I believe. | Home scene | Lets the warmth back in after the death, without a joke about it |
| H5-2 | John | Ten Claws, Lucy. | Home scene | The laughter beat |
| H5-3 | Lucy | At least. | Home scene | |
| H5-4 | Lucy | Ryker? Come back by the fire. | Home scene (`WolfSitDoor`) | Ryker stays by the door |
| H5-5 | Margaret | Let her sit. She remembers too. | Home scene | The only hint of why she leaves (drawn by her mother's memory). Night falls after this line |
| H5-6 | Lucy | The door's open. Ryker's gone. | Home scene (morning, `FamilyDinnerSad` or `WolfSadSit` empty) | |
| H5-7 | Mark | I'm staying. Until she's home. | Home scene | Mark stays (D-172) |

## Step 6 · World map (two pins, both needed)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| W6-1 | John | Two go out, two stay. Someone's here when she comes back. | World map, on first open | **Key line** ("searching in shifts"). A (rec.): John decides, as the father. B (Margaret): "Two of you out, two by the door. She'll come home to someone." C (Mark): "Two search, two wait. Waiting is also searching." Not an objective line: it's the family's rule, and the two pins say the rest |
| W6-2 | Lucy | The river. She always drinks there. | World map, The River pin hover/select | Proposed habit for Ryker (Miso, open question 1) |
| W6-3 | Linda | The ridge. She liked the wind up there. | World map, The Ridge pin hover/select | |

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

## Step 11 · M2 · The Trail (Lucy, Linda + John or Mark)

**Squad pick (Map Table): the one left behind**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| S11-J | John | Go. I'll keep the fire lit and the door open. | Map Table, John stays | **Key line** (design). Option B: "I'll be here. Someone should be, when she comes home." |
| S11-M | Mark | I'll sit by the door. Someone calm should be here when she comes home. | Map Table, Mark stays | Option B: "Waiting is my part. I'm good at it." |

**Route choice and the pile**

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| T11-1 | Lucy | Her blood. | Mission map, "follow the blood" node select | Optional flavour; node names are placeholders |
| T11-2 | Linda | His tracks. | Mission map, "follow the tracks" node select | |
| T11-3 | Lucy | Linda… what if she's in there? | Level dialogue (pile level start) | **Key beat.** The rivalry barks stop from here (scoped bark suppression cue) |
| T11-4 | Linda | Then we find her. Together. | Level dialogue | The turn: back to back |
| T11-5 | Linda | Still counting? | Level dialogue (end), tally fades on this line | **Key lines** (design). Linda asks, Lucy answers (open question 4) |
| T11-6 | Lucy | …No. | Level dialogue | |
| T11-7J | John | She's not here, Lucy. Her tracks go on. Down, to the Rootwell. | Level dialogue (end), John variant | Not an objective line: it's the relief and the next dread in one |
| T11-7M | Mark | She isn't among them. The tracks go down. Into the Rootwell. | Level dialogue (end), Mark variant | |
| T11-8 | Lucy | If he saved her, why didn't he bring her home? | Level dialogue (end) | **Lucy's M4 motive line**, placement A (open question 3) |

## Step 12 · Home visit 3 (Yard scene, night; Bond; first Family point)

| ID | Speaker | Line | Where | Notes |
|---|---|---|---|---|
| Y12-1 | Linda | It's past midnight. | Home scene, Yard (Lucy burning straw targets) | |
| Y12-2 | Lucy | Can't sleep. I keep seeing that pile. | Home scene | Coping, not training |
| Y12-3 | Lucy | If they've hurt her… | Home scene | **Key line** (design) |
| Y12-4 | Linda | Then we'll be ready. | Home scene | **Key line** (design). Linda picks up her bow |
| Y12-5 | Lucy | You pin it, I burn it? | Home scene, after the first race | They find setting each other up works better |
| Y12-6 | Linda | …That's faster. | Home scene | Bond level-up plays here |
| Y12-7 | Margaret | First thing you two have done together all year. | Home scene, from the porch | Grants the Family point as a story reward (D-173). Option B: no Margaret; Linda: "Don't tell anyone." / Lucy: "Too late. Grandma's watching." |
| Y12-8 | Lucy / Linda | "Your turn, then mine." / "Then mine." | Family-tree choice, Sister's Rivalry card | Flavour line on the choice, after the rules text |
| Y12-9 | Lucy | Mark's story. The shot into my fire. | Family-tree choice, Tempest Bloom card | The callback to M4-8 |
| Y12-10 | Linda | It never happened. | (same) | |
| Y12-11 | Lucy | Yet. | (same) | |

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
