# Narrative · Q2 story logic fixes and Q1 first slice (Missions 1 and 2)

Narrative agent, 2026-10-20. Bundle **N** of `plans/2026-10-20-quick-wins-triage.md`. Scope `all`. Read-only on `miso\`: **nothing in the game was changed**, and `glossary.md` is unchanged until THJ approves.

Everything below is **Tier 3** (story beats, names, lore), so every line waits for THJ. When approved lines go into the assets, anything still open keeps the `[PLACEHOLDER] ` tag.

**How to read the tables.**
- Paths are under `miso/Assets/_Project/Resources/Sequences/` unless they say otherwise.
- "Node" is the 1-based position in the asset's `sequenceNodes` list.
- TB = the narration text box (`TextBox_Dialogue`, no portrait).
- Speakers come from each node's `characterData` (it wins over `characterEnum` at runtime; see `Sequence.ResolveCharacterData`).

**Play order on `main`** (from the mission graph): M1 John's Map → M2 Ryker is lost / M5 The Healer → M3 A Wolf's Blood / M3 No More Waiting (Mark) → M4 Into the Rootwell. The playtest's "Blood Wolf" is M3 *A Wolf's Blood* (`Mission 3/LevelLindaJohn-*`).

---

## Q2 · Story logic fixes

### Q2-1 · Lucy keeps the Ryker thread; Lucy and John share the concern

**Reading of the item.** The task list says "Ryker and John share the concern". I read it as **Lucy and John**: Ryker is the wolf who is missing, so she can't share the worry. If THJ meant something else, this section changes. **(Decision 1)**

**What's wrong today.**
- John brushes the worry off. In M1 he answers Lucy with an objective. In M2 his first reply is "She sometimes wanders into the forest on her own."
- Then M3 *A Wolf's Blood* takes the thread away from Lucy. Linda and John follow Ryker's blood trail **behind her back** ("I don't want her to find out", "without Lucy knowing"). At the end John is still holding back ("Be ready, and I will tell you"), and the mission briefing promises the secret.
- **Nobody ever says Ryker is a wolf.** The first hint is Lucy's "Is it wolf blood?" halfway through M2. Until then "Ryker still hasn't come home" reads like a missing person, which probably also caused the "he" slip in Q2-2.

**Proposed fix.**
- John worries out loud from the first scene.
- Linda's secret becomes "check before we raise her hopes", and John promises Lucy hears it from him.
- At the end of A Wolf's Blood, John tells her everything and gives her the lead.
- The first Ryker line says she's a cub.

The mission still plays as John and Linda only.

| Where | Node | Speaker | Current | Proposed | Why |
| --- | --- | --- | --- | --- | --- |
| `Mission 1/Level1C1/Level1C1_Start_DialogNodeSequence.asset` | 4 | Lucy | Dad, Ryker still hasn't come home. We should be looking for her. | Dad, Ryker still hasn't come home. She's only a cub. We should be looking for her. | First mention: Ryker is a wolf cub, and she's a "she" |
| same | 5 | John | We won't stay long. Keep close. We have to get past these Corruption creatures to reach the place. | I know. I've been listening for her at night too. We look here, then we look for her. | John shares the worry and makes a promise. Also drops the objective-explaining half (Q1) |
| `Mission 2/Mission2_Beginning_DialogNodeSequence.asset` | 2 | John | How long has she been gone, Lucy? She sometimes wanders into the forest on her own. | Three nights now. I keep looking at the tree line too. | He already knows how long, because he's been counting. Removes the dismissal |
| same | 3 | Lucy | She's never stayed away this long... What if she's hurt? | *(keep)* | |
| `Mission 3/Home_Mission3_Selected_DialogNodeSequence.asset` | 3 | Linda | I don't want her to find out. | I don't want Lucy to hear it until we're sure. | The secret becomes care, not exclusion |
| same | 10 | John | Then show me. Just the two of us, without Lucy knowing. | Then show me. If it's Ryker's trail, Lucy hears it from me. Tonight. | John carries Lucy's thread even while she's away |
| `Mission 3/Mission3_End_DialogNodeSequence.asset` | 6 | John | We found a clue. It may tell us where she is. | A wolf's trail, Lucy. And a man's boot beside it. | He tells her the truth straight away. Also sets up the masked man (Q2-3) |
| same | 7, 8 | Lucy | Where, Father? Where? / Let's go right now, please. | A man? Someone took her? / Where, Dad? Let's go now. | Lucy reacts to the man; the second line keeps her urgency |
| same | 9 | John | We will all go together. It's a dangerous place. | The Rootwell. We go at first light, all of us. | Names the place he was holding back |
| same | 10 | John | Be ready, and I will tell you. | You lead, Lucy. She knows your voice. | Hands her the thread. Its payoff: in M4 Ryker stands with the stranger, and Lucy's voice isn't enough |
| `Content/Levels/M3 - Blood Trail of A Wolf.asset` (`missionDescription`) | – | briefing | Follow the blood trail Linda found in the forest, and learn where it leads before Lucy discovers what John and Linda are hiding from her. | Linda has found a wolf's blood trail in the forest. Follow it with John, and learn the truth before Lucy's hopes ride on a guess. | The briefing no longer promises a secret kept from Lucy |

Optional, for M4 (`Mission 4/Level1C3/Level1C3_End_DialogNodeSequence.asset`, node 22, John: "Put Ryker down, Lucy."): soften to "Lucy. Let her choose. We stay right beside her." Today John sides with the stranger against his daughter in one line. The proposal keeps him with Lucy and still lets Ryker lead.

Canon and glossary: none. Ryker as "Lucy's wolf cub" is already in the data (M4 calls her "the wolf cub"). Once THJ approves, I'll add **Ryker** to the glossary (Lucy's wolf cub; Toba calls her Waya, "the Fangmother"; marked as Miso, not confirmed canon).

---

### Q2-2 · Ryker's pronoun

Every line says she/her except one.

| Where | Node | Speaker | Current | Proposed |
| --- | --- | --- | --- | --- |
| `Mission 2/LevelLucyJohn-C1/LevelLucyJohn-C1_End_DialogNodeSequence.asset` | 2 | Lucy | Maybe he has gone there again. | Maybe she's gone there again. |

I checked every sequence, the mission briefings, the bark CSVs and the level prefabs: no other he/him for Ryker. The M11 briefing has a grammar slip in the same thread; it's covered in Q2-3. Glossary: Ryker is "she" (added with Q2-1).

---

### Q2-3 · Set up the masked man

**What the data already decides.** The masked man **is Toba**. He removes the mask in M4 (`Level1C3_End`, node 6), and all his lines there use the Toba speaker. So *who* he is is settled. What's missing:
1. **No setup.** The first mention is M4 `Level1C3_Start` node 5, "Lucy was already running at **the** masked man", as if the player already knew him. The only clues before that are the human boot heel in A Wolf's Blood and "something, or someone, had been dragged away" in M2.
2. **Why the mask** is never said. **(Decision 2b)**
3. **His name shows too early.** The speaker plate reads "Toba" (`Dom_DialogueCharacter.characterName`) from his first line, and the narration says "Toba" in `Level2C2_End` and `Level3C1_Start`. But he only gives his name in the last scene of M4 ("I... we don't even know your name." / "Toba."), which is a lovely beat that the early labels spoil.

**Options for where to set him up (Decision 2a):**

| | Where | Lines | Feel |
| --- | --- | --- | --- |
| **A (recommended)** | End of M2, `Mission 2/LevelLucyJohn-C3/LevelLucyJohn-C3_End_DialogNodeSequence.asset`, after node 8 ("Then she's alive somewhere.") | TB: "Across the river, something moved between the trees. A man in a carved mask, watching them." / Lucy: "Dad, did you see him?" / TB: "When John looked again, the trees were empty." / John: "I saw him." | Lucy sees him first, so the man belongs to her thread, and "thief" in M4 is her theory, not a random insult. John believing her is the shared concern from Q2-1. The boot heel in A Wolf's Blood then confirms what she saw |
| B | End of A Wolf's Blood, `Mission 3/LevelLindaJohn-C2/LevelLindaJohn-C2_End_DialogNodeSequence.asset`, after node 11 | TB: "At the mouth of the Rootwell, a masked figure turned to look at them, then stepped into the dark." | Strong dread, right before M4, and it also explains going home (Q2-5). But Lucy isn't there, so it's weaker on Q2-1 |
| C | Mark's intro, `Mission Mark Intro/MarkIntroC3/LevelMarkIntroC3_End_DialogNodeSequence.asset`, after "I'm coming home with you to find her." | Mark: "There's a man in a mask hunting near the river. He doesn't hunt goblins for sport. Keep clear of him." | Mark knows the forest. But this mission is optional in order, so not every player gets the setup before M4 |

Recommended: **A**, plus the Q2-1 line in `Mission3_End` ("a man's boot beside it"), so the player hears about him twice before he appears.

**Why the mask (Decision 2b, proposed lore, not canon):**
1. **A hunting mask of his people** (recommended). It fits his healing words ("Naya torun, Veyama", "Unshak'torah"), the "quiet tribal gesture" in `Level2C3_End`, and the Persian-named world. He takes it off to speak as himself, which is what the unmasking beat already does.
2. A filter against Corruption air. That's practical, but it raises questions about why the Bergsons don't need one.
3. He hides his face from goblins who know him. That's a hook, but it's new plot to pay off later.

If THJ picks 1, one line in `Level1C3_End` (node 6) carries it: "The stranger removed his mask, carved bark painted with old signs. His breathing was steady, untouched by the fight."

**Name before introduction (Decision 2c):**
- **Recommended:** until he says "Toba." in `Level3C1_EndDialogNodeSequence`, the speaker plate reads **"Masked Stranger"** (a Generic character slot, `GenericCharacter_1`, whose `characterName` is empty today), and the narration says "the stranger". Lines to change:
  - `Level2C2_EndDialogNodeSequence` nodes 1, 4, 8 ("Toba ran…", "Toba placed his palm…", "Toba looked at the Bergsons…");
  - `Level3C1_StartDialogNodeSequence` nodes 5–6 ("Toba looked at her…");
  - `Level2C3_EndDialogNodeSequence` ("Toba and the Bergsons rushed…" and the `{Frame: Toba…}` note).
  - Assigning a Generic slot is a data change for the implementer.
- Alternative: keep "Toba" everywhere and cut Linda's "we don't even know your name" beat. Not recommended: it's one of the warmest moments in M4.

**Typos and duplicates to fix along the way:**
- `Level1C3_Start` nodes 1 and 2 are the **same line twice** ("John and the girls followed the wolf and human tracks…"). Delete node 2.
- `Level1C3_End` node 1: "toward masked man's head" → "toward the masked man's head".
- **M11 briefing** (`Content/Levels/M11 - Sisters.asset`): "the name the masked man gave Ryker… why Ryker called as Waya" → "Lucy can't stop thinking about the name Toba gave Ryker. She asks Linda to come into the forest and help her understand why he calls her Waya." By M11 he's named, and this fixes the grammar too (`narrative-world.md` Q4).

Glossary after approval: **Toba** row gets "first met as the Masked Stranger (M4)"; the mask's meaning is marked as Miso, proposed.

---

### Q2-4 · "If we are not killing this thief"

`Mission 4/Level1C3/Level1C3_End_DialogNodeSequence.asset`, node 14, Lucy: **"If we are not killing this thief, I'm taking Ryker home."**

What's wrong:
- A girl casually proposing to kill a man reads cruel, not fierce.
- It comes right after Linda's "No ugly words, Lucy... you promised", so it escalates past what the family just agreed.
- Toba's reply ("With the cub's help, I can find the Pathmother") answers the "taking Ryker home" half, which is the part worth keeping.

| Option | Line | Feel |
| --- | --- | --- |
| **A (recommended)** | Thief or not, Ryker is coming home with me. | Same defiance, no killing, and Toba's reply still lands |
| B | Fine. No ugly words. But Ryker comes home with me. | She grudgingly keeps the promise to Linda. Warmer, a little softer |
| C | If you're not a thief, why the mask? | Uses the mask (Q2-3) and puts him on the spot. But then Toba's next line doesn't answer it; it would need a new Toba line ("So the goblins don't know my face.", which fits Decision 2b option 3) |

Keep Lucy's later "The thief is also a poet. Great!" (`Level2C1_Start` node 4) and "One wrong move, masked man, and I'll roast you." They're her sulk running down, and they read fine once the killing line is gone.

---

### Q2-5 · Why the family goes home after A Wolf's Blood

`Mission 3/LevelLindaJohn-C2/LevelLindaJohn-C2_End_DialogNodeSequence.asset`, nodes 12–14:
- Linda: "Oh, Father... what if someone took Ryker?"
- John: "To enter the Rootwell, we need to be ready."
- John: "Come on. Let's go back home."

John and Linda are standing at the entrance with fresh tracks, and the only reason given for leaving is "be ready". Players asked why they don't go in.

| Option | Lines (replace nodes 13–14) | Feel |
| --- | --- | --- |
| **A (recommended)** | John: "Then Lucy has to be with us. I won't find her wolf behind her back." / John: "And the Rootwell is no place for two. We go home, and we come back as a family." | Uses Q2-1 and the game's theme (the family fights together). M4 then opens with all three, so it pays off at once |
| B | John: "The Rootwell runs deep, and the Corruption runs deeper. Two of us won't come back out." / John: "Home. We come back with everyone." | Danger only. Clear, but it misses the Lucy thread |
| C | John: "The tracks go underground. We'll need light, food and every hand we have." / John: "Let's go home." | Practical, but flat |

With Q2-3 option B (the masked figure at the cave mouth), A still works. Linda's line then becomes "Father... he went in. What if he has Ryker?"

---

### Q2-6 · The Mission 5 grandma line

The mission is **M5 The Healer** (`Mission 5/`). Two lines mention Grandma. I believe the playtest item is the first:

| Where | Node | Speaker | Current |
| --- | --- | --- | --- |
| `Mission 5/Home_Mission5_Selected_ExitHome_DialogNodeSequence.asset` | 3 | Lucy | How can you think we'll find Grandpa Adam after all these years? Even Grandma's gone. |
| `Mission 5/LevelE1-C1/LevelE1-C1_End_DialogNodeSequence.asset` | 5 | Lucy | Grandma would know about her. I keep thinking we can ask her when we get home... then I remember. |

**The real problem is a canon decision, not the wording (Decision 4).**
- M1 opens with "Since Grandma Margaret's death". Miso has her dead.
- But **Home shows her alive**: the Home cutscenes cast Grandma = Margaret at the Dining Table (`build-log.md`, Home cutscene mapping), and Home has a Grandma Table, Bed and Chair.
- As far as I recall, Children of Morta's Margaret is alive and at the heart of the family. **THJ to confirm against canon**; I'm not asserting it.
- Separately, "Even Grandma's gone" is a non sequitur (her death says nothing about whether Adam can be found) and it's harsh for Lucy.

| Option | What changes | Lines |
| --- | --- | --- |
| **A (recommended if canon has her alive)** Margaret is alive | M1 opening, M5 Exit line, M5 C1 End line | M1 `Level1C1_Start` node 1: "Grandma Margaret had kept a journal all her life. Lately, John had begun reading it." / M5 Exit node 3, Lucy: "Grandpa's been gone longer than I've been alive, Dad. What if there's nothing left to find?" / M5 C1 End node 5, Lucy: "Grandma would know about her. We should ask her when we get home." / node 7, Linda: "Her journal brought us here. She's still guiding us." (unchanged in meaning) |
| B Margaret is dead (Miso's choice) | M5 Exit line only, plus Home must stop showing her | M5 Exit node 3, Lucy: "Grandpa's been gone longer than I've been alive, Dad. What if there's nothing left to find?" Keep the C1 End grief line; it's good. **Home conflict:** Grandma at the dinner table and her furniture need a decision (a memory, or removed) |
| C Keep both lines; fix only the logic | M5 Exit line only | Same Lucy line as B. Leaves the Home conflict open |

In every option John's answer (node 4, "I don't know if we'll find him, Lucy. But I need to know where he went.") stays; it answers the new line well.

Small consistency fixes in the same thread:
- Lucy says "Grandpa Adam" here but "Grandfather" in `LevelE1-C2_End`. Proposed: Lucy says **Grandpa**, Linda says **Grandfather** (matching "Dad"/"Father", see Decision 6).
- The M1 briefing says "Margaret's old books"; the dialogue says "her journal". Proposed: "journal" everywhere.

Glossary after approval: add **Margaret (Grandma)** and **Adam Bergson** (John's father) to the canon table with their status.

---

### Q2-7 · Name "this part of the forest"

`Mission 2/LevelLucyJohn-C1/LevelLucyJohn-C1_Start_DialogNodeSequence.asset`:
- node 1, John: "Why do you think she could be in this part of the forest?"
- node 2, Lucy: "Because she came into this part of the forest once before, and I found her here."

John is a hunter who knows these woods, yet he can't name them. The river he and Lucy follow (C1 End, C2 End) is unnamed too, but only the forest was flagged.

| Option | Name | Feel | Canon |
| --- | --- | --- | --- |
| **A (recommended)** | **Gorgan Wood** | *Gorgan* is Persian for "land of wolves" (the old name of the Hyrcanian forest region). Fits Ryker and the Fangmother, and the world's Persian naming thread (Anahita, Mithra, Hegmataneh, Deev) | Miso invention; check against `narrative-world.md` Q2 (Persian thread) |
| B | **Ryker's Hollow** | What the family calls the spot where Lucy found her cub. Warm and private; no lore weight | Miso invention, family nickname |
| C | **Silverleaf Wood** | Where the Silverleaf grows that Lucy burns to call Mark. Ties M2 to the Mark intro | Miso invention; makes Silverleaf a local plant |

Proposed lines (with A):
- node 1, John: "Gorgan Wood. You think she came back here?"
- node 2, Lucy: "She ran off here once before. I found her down by the river."
- node 3 is cut (Q1, below).

Follow-on: C1 End nodes 1–2 ("Last time, I went as far as the river… Maybe he has gone there again.") now repeat node 2. See the Q1 table for the merge.

Glossary after approval: add the name under a new **Places** section, marked Miso.

---

## Q1 · Directed dialogue pass, first slice: Missions 1 and 2

**The rule (Q1):** every line earns its place. Cut scenery narration and lines that explain the objective. Move what's useful into barks or in-level triggers. Use the room for S8 beats (a first Duo, Synergy or Family Role).

**Two tools for moved lines:**
- **In-level trigger:** `LevelSequenceTrigger` already plays a sequence when a family member steps onto a trigger area, once per level.
- **Barks:** the bark CSVs in `Resources/BarkSystemData/` (Unit Selected, Pass-by with a partner tag, Enemy Killed, Low HP, Falls).
  - **Tech question (Decision 9):** I found no way to limit a bark to one mission. Story barks (anything about Ryker) would play everywhere. They need a mission or level filter, or they stay as sequences.

**S1 slot map used for S8** (from the task list): 1.1 = M1 level 1 as is, 1.2 = Linda-focused, 1.3 = John-focused, 2.1 = M2 C1 with Linda, 2.2 = Lucy + John's Family Role. **S1 will rework these levels**, so the S8 beats below are pinned to *beats*, not files, and move with the levels.

### Mission 1 · John's Map

**`Mission 1/Level1C1/Level1C1_Start_DialogNodeSequence.asset`** (first scene of the game after the intro; John + Lucy)

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | TB | Since Grandma Margaret's death, John had begun reading her journal. | **Keep**, wording depends on Decision 4 | (Q2-6 option A) "Grandma Margaret had kept a journal all her life. Lately, John had begun reading it." |
| 2 | TB | One sketch had brought him back to the caves where he had found his father's sword. | **Keep, tighten**; sets up Linda | "One sketch led him, with Lucy and Linda, back to the caves where he once found his father's sword." (Linda appears alone in the next level with no setup today) |
| 3 | Lucy | So we came all this way because of a drawing? | **Keep** | Her voice in one line |
| 4 | Lucy | Dad, Ryker still hasn't come home… | **Keep, edit** | Q2-1 |
| 5 | John | We won't stay long. Keep close. We have to get past these Corruption creatures to reach the place. | **Cut** the objective half | Q2-1: "I know. I've been listening for her at night too. We look here, then we look for her." |

**`Level1C1-2_Start`** (Linda alone; S1 slot 1.2 "Linda-focused")

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | TB | Linda had taken the other passage at the fork. More corrupted creatures stood between her and the far end. | **Keep first sentence, cut second** (scenery and objective) | "Linda had taken the other passage at the fork." |
| 2 | Linda | More of them. I'll have to clear this passage. | **Cut**; replace with an **S8 beat** (first time Linda's Family Role can fire) | "Come on, then. Walk into my line." Frames her role (she shoots enemies who end their move in her row or column) in her voice, without naming the mechanic |

**`Level1C1-2_End`**, node 1, Linda: "I have to join Father and Lucy." → **Cut** (it explains the next objective). If a beat is wanted, make it a trigger line on the exit tile: "Hold on, Lucy. I'm coming."

**`Mission 1/Level1C2/Level1C2_Start_DialogNodeSequence.asset`** (all three together for the first time; S1 slot 1.3)

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | TB | Together again, they reached a place John remembered well. | **Keep** | |
| 2 | John | This is where I found his sword years ago. The one I carry. | **Keep** | |
| 3 | Linda | Then perhaps we can find him this time. Do you think so, Father? | **Keep, tighten** | "Then maybe he went on from here, Father." Sets up the passage find at the level's end |
| 4 | John | There was no sign of him. I thought the trail ended here. | **Keep** | |
| 5 | Lucy | Those creatures aren't going to let us look. | **Cut** (objective); replace with **S8 Sister's Rivalry setup** | Lucy: "Then let's look fast. Linda, I'm counting." |
| 6 | John | Then we clear them out. | **Cut**; replace | Linda: "Count slowly. You'll want to get it right." |

This is the **Setup** step of the Sister's Rivalry mini-arc (S8): the first time both sisters share a board. Supporting barks, all Tier 3 proposals (they'd go in as `[PLACEHOLDER]` until approved):
- `Enemy Dies Dialogues.csv` (Lucy): "That's one more than you." / "Still counting, Linda?"
- `Enemy Dies Dialogues.csv` (Linda): "Cleaner than yours." / "Keep up, little sister."
- `Units PassBy Dialogues.csv`:
  - Lucy, tag Linda: "Race you to the next one." (exists; keep)
  - Linda, tag Lucy: "Wait for the opening." (exists; keep)

These are general barks, so they're safe in every mission and need no scoping. Do they fire only when the sister is on the board? That's for the implementer to check.

### Mission 2 · Ryker is lost

**`Mission 2/Mission2_Beginning_DialogNodeSequence.asset`** (at Home, before the sortie)

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | Lucy | We're home now, Dad. Can we please go and look for Ryker? | **Keep** | |
| 2 | John | How long has she been gone, Lucy? She sometimes wanders into the forest on her own. | **Rewrite** (Q2-1) | "Three nights now. I keep looking at the tree line too." |
| 3 | Lucy | She's never stayed away this long... What if she's hurt? | **Keep** | |
| 4 | John | Come, sweetheart. We'll find her together. | **Keep** | |

**`LevelLucyJohn-C1_Start`** (S1 slot 2.1)

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | John | Why do you think she could be in this part of the forest? | **Rewrite** (Q2-7) | "Gorgan Wood. You think she came back here?" |
| 2 | Lucy | Because she came into this part of the forest once before, and I found her here. | **Rewrite** (Q2-7) | "She ran off here once before. I found her down by the river." |
| 3 | Lucy | The difference is, now it is full of Corruption creatures. | **Cut** (scenery; the board shows it) | |
| 4 | John | Stay close to me. We move forward together. | **Replace with S8 beat** (first Duo, John–Lucy *Hide and Seek*) | John: "If they crowd us, we play Hide and Seek. Like when you were small." / Lucy: "I always won." Their Duo makes Lucy hide behind decoys. The level adds 3 FTP at load, enough for one Duo (2 FTP). **Check:** is the John–Lucy Duo available this early on `main`? If not, keep John's original line |

**`LevelLucyJohn-C1_End`**: node 1, Lucy, "Last time, I went as far as the river, Father, and found her there." → **Cut** (now said in C1 Start). Node 2 → "Maybe she's gone there again." (Q2-2). Node 3, John, "Then we go toward the river." → **Keep**.

**`LevelLucyJohn-C2_Start`** (S1 slot 2.2: Lucy + John's Family Role)

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | Lucy | Ryker! Ryker! | **Keep** | |
| 2 | Lucy | Do you want us to split up, Father? We could search more ground that way. | **Keep, tighten** | "We'd cover more ground if we split up, Dad." **Data slip:** `characterEnum` says John while `characterData` says Lucy (Lucy shows). Set both to Lucy when editing |
| 3 | John | Never! We move together. | **Replace with S8 beat** (first time John's Family Role is the focus) | "Never. You stay where my shield can reach you." Frames his role (he shields a nearby family member who's attacked) as a father's rule |
| new 4 | Lucy | – | **Move here** from `LevelLucyJohn-C2_End` nodes 1–2 | "Linda goes into the caves alone, and I can't? You still don't trust…" (merged). Today this argument opens the *end* scene, a whole fight after the line it answers |

Then `LevelLucyJohn-C2_End` starts at node 3 (John finds the blood). Optional trigger line when John's role first fires in this level, Lucy: "…Okay. Maybe stay close." It pays off the argument through play. It needs a role-fired hook, which only exists for barks; that's a tech question.

**`LevelLucyJohn-C3_Start`**

| Node | Speaker | Current | Verdict | Proposed |
| --- | --- | --- | --- | --- |
| 1 | TB | A pile of slaughtered animal bodies had been heaped together. | **Keep, tighten** | "Ahead, slaughtered animals lay heaped together." |
| 2 | TB | Corruption shamans had killed many animals for their dark rituals. | **Cut** | Explains too early, and Toba reveals it in M4 ("They sacrifice animals to the Corruption") |
| 3 | Lucy | No, no… | **Keep** | |
| 4 | Lucy | Father… what if Ryker is somewhere in that pile? Is she? | **Keep, tighten** | "Dad… what if Ryker's in there?" |
| 5 | John | For now, help me kill these filth, so we can reach the bodies and search through them. | **Rewrite** (objective explaining; Q2-1) | "If she is, we bring her home. Stay with me." |

`LevelLucyJohn-C3_End`: keep as is. It's the emotional close and earns its length. Add the Q2-3 option A beat (the masked man across the river) after node 8.

### Summary of the slice

- **M1:** 13 opening nodes → 3 cut, 5 kept, 5 rewritten (two of them S8 beats: Linda's role, Sister's Rivalry setup). Plus 1 end node cut.
- **M2:** 15 opening nodes → 2 cut and 1 merged, 6 kept, 6 rewritten (two of them S8 beats: the first Duo, John's Family Role). Plus 1 end node cut and the C2 argument moved to where it belongs.
- **Not in this slice:** the end scenes beyond what Q2 touches, and Missions 3 onward. A Wolf's Blood repeats the "kill them first, then I'll tell you" pattern (`LevelLindaJohn-C1_Start` node 2, `-C2_Start` nodes 2–4) that Q1 should cut next.

---

## Decisions for THJ

1. **Q2-1 reading:** "Ryker and John share the concern" read as **Lucy and John**. Right?
2. **Masked man:**
   - (a) where he's set up: **M2 end, Lucy sees him** (rec.) / A Wolf's Blood cave mouth / Mark's intro;
   - (b) why the mask: **his people's hunting mask** (rec.) / Corruption filter / hiding from goblins;
   - (c) plate reads "Masked Stranger" until he says "Toba." (rec.).
3. **"Thief" line:** **"Thief or not, Ryker is coming home with me."** (rec.) / B / C.
4. **Is Grandma Margaret alive?** This is canon (Children of Morta) and Home already shows her. Alive → option A (rec. if canon agrees); dead → B, and Home needs a fix.
5. **Going home after A Wolf's Blood:** **"Not behind Lucy's back; not as two"** (rec.) / danger only / supplies.
6. **Forms of address:** Lucy says "Dad" and "Grandpa", Linda says "Father" and "Grandfather". OK?
7. **Forest name:** **Gorgan Wood** (rec.) / Ryker's Hollow / Silverleaf Wood.
8. **Q1 slice:** approve the cuts and moves, and the four S8 beats: Linda's role (M1 L2), Sister's Rivalry setup (M1 L3), first Duo *Hide and Seek* (M2 C1, if available on `main`), John's role (M2 C2).
9. **Tech (for the coordinator):** story barks need a per-mission filter, and a "role fired" hook for trigger lines. Until then, moved lines stay as sequences or `LevelSequenceTrigger`s.

After approval I'll update `glossary.md` (Ryker, Toba's first appearance, Margaret and Adam, the forest name, a new Places section) and the matching rows in `design/gdd/narrative-world.md` (Q1, Q4).
