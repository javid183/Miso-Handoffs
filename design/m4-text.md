# M4 "The White Mothers": lines

Owner: miso-narrative. Scope `thj/onboarding-demo`. Written 2026-11-25 for the approved M4 paper levels (D-690; plan `plans/2026-11-22-onboarding-d3-paper-levels.md` › M4).
Status: **proposed, waiting on THJ.** Every line here is Tier 3 until he approves it. **§3 (saving Ryker) is a story beat and needs his explicit approval, with answers to the canon questions in §5.**

How to paste (same rules as `m1-ridge-redesign-text.md`):
- **Dialogue** (`DialogNodeSequence`, `Line(Who.X, Side.Y, "...")`): paste **without** a tag. Dialogue shows `[PLACEHOLDER]` and the onboarding tests forbid it (`conventions.md` › Text). This file is the placeholder list until THJ signs off.
- **Rec.** is the line to paste; alternatives are for THJ, one line on the feel of each.
- **Sides** are not fixed yet (no M4 wiring). Suggested: Toba Left, Linda Right in M4-1 and M4-2; the implementer may swap. Lucy and the pick take whichever side is free.
- Lines stay under about 55 characters so they fit a bubble.

Cast, as fixed: **Toba, Linda, Lucy + one pick, John or Mark.** Every line below is written for **Toba, Linda and Lucy**, who are always present. A line for the fourth seat comes in **a John and a Mark version**, marked **(J)** and **(M)**, and is optional unless noted: if THJ would rather not branch on the pick, cut them all and nothing breaks.

Voice:
- **Toba:** the newcomer, a healer and nature lover, gentle, plain, unhurried. He is a stranger who is slowly trusted: short sentences, no jokes, speaks of the forest as a living thing. He knows this place; the family doesn't.
- **Linda:** older sister, quick and proud, a little dry.
- **Lucy:** the youngest, fierce and open; Ryker is hers. Her lines get shorter and rawer the nearer Ryker is.
- **John:** father, warm and steady, few words. **Mark:** calm, clipped, a dry streak ("Mind before fist").
- The sisters have just stopped counting kills (M3: "Still counting?" / "…No."). M4-1 is their first Duo: they fight as a pair now, not a race.

Terms used (glossary): **Cleanse** (the button), **Duo**, **Family Points (FP)** if ever needed on a page (none here), **Heavenly Sword** (a Divine Relic), **Corruption**, **dark enemies**. "Wounded" and "Bloodied" are never used. The planted pools are called **circles** on screen (the level name is "The circles"); "pool" is a design word.

---

## 1. M4-1 "The circles" (`GB_m4-cleanse`)

Order: level start, input off → camera on the nearest circle (north, 5,7) then the other two (south 5,1, east 11,5, behind the Shaman) → Toba's line → camera back on the squad → **Cleanse button pulses once** (`GuidedAbilityHint`, WhenUnlocked) → input on. The sister line plays after Toba, before input. Keep the whole thing under about 10 seconds: the player is about to plan the demo's only real fight.

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 1.1 | Toba | Level start, camera on the circles | Three circles. They feed the dark. | A: "Those circles feed the dark. Cleanse them." (says the verb, so the pulsing button reads as the answer). B: "Three circles. The Corruption rises from each." (more dread, no instruction). **Rec.** names the problem and leaves the button to do the pointing; if THJ wants the word on screen, use A. Don't also say "Cleanse" in 1.2 | Placeholder |
| 1.2 | Toba | Same dialog, camera back on the squad, as the Cleanse button pulses | Close to each, and Cleanse. | A: "Stand close. Cleanse each one." B: "Burn it out. Stay close." ("burn" would clash with Lucy's Burn status). 1.1 + 1.2 are the two-line version. **If the whole point is one line:** keep 1.1 only, the pulse carries the rest | Placeholder |
| 1.3 | Linda | After Toba, optional | Together this time, Lucy. | A: "Lucy. Pick a side." (action first). B: "Same line, little sister?" (callback to the Duo). **Rec.:** says "together", which the first Duo is. Use "this time" so it quietly pays off the tally without naming it | Placeholder |
| 1.4 | Lucy | Same dialog, reply, optional | No counting. | A: "Together. I like that." B: "Keep up, sister." (flips Linda's old line on her). **Rec.** is two words: it closes the M3 beat ("…No.") with a smile. Only with 1.3 | Placeholder |
| 1.5 | The pick (J) | Same dialog, last, optional | John: Circles first. I'll hold the middle. | John (warm, practical): "Circles first. I'll hold the middle." Alt: "Stay together. Cleanse, then fight." | Placeholder |
| 1.5 | The pick (M) | Same | Mark: Mind before fist. Circles first. | Mark (calm): "Mind before fist. Circles first." Alt: "Cleanse, then strike. Don't rush." | Placeholder |

Objective texts (already planned; checked): **"Cleanse the circles."** and **"Defeat the dark claws."** Both fit (plan §M4-1). One note: the plan's "dark claws" is lower case on purpose; the glossary writes **Dark Claw**. If the objective bar capitalises other enemy names, write "Defeat the Dark Claws." The Dark Shaman is not named in the text; fine.

Lines to paste (Rec. set, no tag; Toba Left, Linda Right):

```csharp
Line(Who.Toba, Side.Left, "Three circles. They feed the dark."),
Line(Who.Toba, Side.Left, "Close to each, and Cleanse."),
Line(Who.Linda, Side.Right, "Together this time, Lucy."),
Line(Who.Lucy, Side.Left, "No counting."),
// optional, by the pick:
Line(Who.John, Side.Right, "Circles first. I'll hold the middle."),
Line(Who.Mark, Side.Right, "Mind before fist. Circles first."),
```

(`Who.Toba` is assumed to exist; the implementer checks the `Who` enum, Toba's dialog portrait may be new art.)

---

## 2. M4-2 "Mithra's Rest" (reworks `LevelDivineRelicRoom 1.prefab`)

### 2.1 Objective text

Current plan text: **"Rest by the fire, take the relic, then go on."** Checked.

| Check | Verdict |
|---|---|
| Fits the screen | Yes (43 characters) |
| Order matches play | Yes if the heal triggers by the fire and the relic is on the altar; the player may take the relic first, which still reads right ("Rest... take... go on" is a list, not a sequence) |
| Terms | "Relic" is the glossary's word; "Heavenly Sword" is its name, not shown in the objective. Fine: the pickup names itself |
| "Go on" | Soft, but the exit does the rest. Alternative: "then go on to the Queen." (names the boss: a story fact, THJ's call) |
| Alternatives | A (Rec.): keep as written. B: "Rest by the fire. Take the relic. Then go on." (three sentences, easier to scan). C: "Rest. Take the sword. Go on." (shortest, but "sword" names the relic and the room may later hold another) |

Rec.: keep A. If the objective updates as steps finish, the same words work as a counter ("Rest by the fire" ticks off after the heal).

### 2.2 Campfire scene, when the heal triggers

Order: the heal fires (HP to 50%, FP filled) → the family recovers (animation and the heal VFX) → dialog. The Heavenly Sword is **not** in the scene: the player takes it on the altar after. Tone: the one calm moment of the demo before the boss, **warmth against dread** (vision pillar 3). Toba leads: this is his place. Nobody jokes; the light stays on the fire.

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 2.1 | Toba | Heal triggers, camera on the fire | Sit. Let the fire do its work. | A: "Sit by the fire. It will mend you." B: "Sit. This is a good fire." ("good" is his kind of word, the lightest option). **Rec.** says what the fire does without him claiming magic | Placeholder |
| 2.2 | Toba | Same dialog, as the family recovers (the heal VFX) | There. Breathe. | A: "Breathe. It's working." Very short on purpose: this is the beat | Placeholder |
| 2.3 | Lucy | Same dialog | Toba. How far is Ryker? | A: "Is she close?" (rawer). B: "How much further?" **Rec.** names Ryker in her voice; it is a question Toba can answer without telling us where she is (see 2.4 and §5 Q4) | Placeholder |
| 2.4 | Toba | Same dialog | Close. Rest while you can. For her. | A: "Close. Rest now, so you can reach her." B: "Closer than you think." (more dread, less comfort). **Rec.** gives her the reason to sit: she wants to run on, and he steers that into resting | Placeholder |
| 2.5 | Linda | Same dialog, last, or on the pickup of the relic | There's a sword on the altar. Take it. | A: "Take the sword, Lucy." (to the sister, who is the one pushing on). B: "That sword's meant for someone. Take it." (leaves its use open). **Rec.** hands over to the objective. If the player takes the relic first, move it before 2.1 | Placeholder |
| 2.6 | The pick (J) | Same dialog, optional, before 2.5 | John: Eat something. All of you. | Warm father line; no rations exist in this demo (plan: rations need the Home Kitchen), so "Eat something" is only a gesture. Alt: "Sit down, Lucy. She'll wait for us." | Placeholder |
| 2.6 | The pick (M) | Same | Mark: Rest is part of the fight. | Alt: "Breathe in. Out. Then we go." | Placeholder |

Lines to paste (Rec. set, no tag):

```csharp
Line(Who.Toba, Side.Left, "Sit. Let the fire do its work."),
Line(Who.Toba, Side.Left, "There. Breathe."),
Line(Who.Lucy, Side.Left, "Toba. How far is Ryker?"),
Line(Who.Toba, Side.Left, "Close. Rest while you can. For her."),
// optional, by the pick:
Line(Who.John, Side.Right, "Eat something. All of you."),
Line(Who.Mark, Side.Right, "Rest is part of the fight."),
Line(Who.Linda, Side.Right, "There's a sword on the altar. Take it."),
```

Count: 5 lines without the pick (2.1 to 2.5), 6 with it.

**Canon touch, light.** Calling the place Mithra's Rest and the fire a healing one is Persian myth dressing the game already uses (Mithra's Gift, Anahita's Ashiyan); 2.1 does not claim Mithra's role. The glossary's Mithra row ("name is canon, role not recorded") stays as it is. No line speaks the name Mithra aloud.

---

## 3. Level3-C1 end: saving Ryker (M4-3)

**THIS IS A STORY BEAT. IT NEEDS THJ'S APPROVAL BEFORE ANYONE BUILDS IT.** It is the demo's emotional end: the first time the player sees Ryker in the flesh after the Hearth's loss. The lines below are a proposal that **invents nothing about Ryker's species, injuries or history**, and they assume the answers in §5 only where marked. Read §5 first.

What the docs already fix (checked against the plan, snapshot, narrative-world, Hearth text):
- Ryker is a **she** (every on-screen line says "her": "Then we find her. Together."; the Ridge recap: "Someone's carrying her. And tending her.").
- She **vanished from the Bergson house** (the Hearth ending), and **Lucy** is the one most bound to her (GDD: "her bond with Ryker"; Lucy left the house to look for her).
- The snapshot calls her **"the cub"** (memory 4, "already has the cub") and gives her wolf idle art (WolfSitDoor, WolfSadSit). So a wolf cub is the likeliest reading. **Not confirmed as canon**, so the Rec. lines never say "wolf" or "cub".
- Toba **knows where she is** (M3 end). He is also the likeliest one who carried and tended her (the Ridge's clues). **Not confirmed**, so the Rec. lines don't say who.
- Whether the Queen took Ryker, or only guards the way to her, is not decided (the plan: "saving Ryker after the Goblin Queen dies").

**Order:** the Queen dies → Family Super Time ends (as built) → silence beat, camera off the body → camera on where Ryker is (a cage, a nest, a ledge: the level artist's pick) → the lines → fade, home. No fight is left. Input off from the Queen's death to the fade.

### 3.1 Rec. set (Option A): found, alive, frightened

| # | Speaker | Trigger | Rec. line | Alternatives / notes | Flag |
|---|---|---|---|---|---|
| 3.1 | Lucy | Camera finds Ryker | Ryker! | The only word she says before she runs. Alt: "Ryker?" (she's afraid it's too late). **Rec.** is relief | **Needs approval** |
| 3.2 | Ryker | Same dialog | (a small sound: no words) | Sound only: a whimper or a soft cry. Ryker never speaks. This is a bark or an SFX on her prop or unit, not a `Line`. Needs the Ryker sound asset (art/audio, not narrative) | **Needs approval** |
| 3.3 | Lucy | Same dialog | She's breathing. She's alive. | A: "She's alive!" (shorter). **Rec.** says the thing the player is afraid of out loud, and settles it | **Needs approval** |
| 3.4 | Toba | Same dialog | Frightened. Tired. Nothing worse. | A: "Frightened, and tired. She'll mend." B: "Hungry, and afraid. That is all." Toba is the healer, so he is the one who reads her state: **this line asserts her condition** (see §5 Q3) | **Needs approval** |
| 3.5 | Linda | Same dialog | You scared us half to death, you know. | A: "You gave us a fright, little one." (**"little one"** hints she is small; use only if §5 Q1 says a cub). B: "Stubborn thing. Just like Lucy." (a joke about Lucy's stubbornness; THJ to decide if it's family-kind or unkind). **Rec.** has no species and keeps the family dry-warm tone | **Needs approval** |
| 3.6 | The pick (J) | Same dialog, optional | John: Come on. Let's take her home. | John: warm, a father's relief. Alt: "Well done, all of you." (praise to the children, for after the fight). Pick only one | **Needs approval** |
| 3.6 | The pick (M) | Same | Mark: Home. All of us. | Mark: calm, minimal. Alt: "She's safe. That is enough." | **Needs approval** |
| 3.7 | Lucy | Same dialog, last | I've got you. I've got you. | **Rec.** is the beat: she says it twice, she's holding her. A: "I'm here. I'm not leaving you." (clearer, less poetic). B: "Don't ever do that again." (anger and love; rawer, loses the quiet) | **Needs approval** |
| 3.8 | Toba | After a beat, camera on the family, optional | The fire is low. Let's get her home. | A: "Come. Her place is with you." (Toba's quiet claim that the family is hers, and a nod to the family he is not yet part of). **Rec.** is the plainest. Toba ends the scene because he is the one who knows the way out too | **Needs approval** |

Lines to paste, **only after approval** (Rec. set, no tag; the Ryker sound is a separate asset):

```csharp
Line(Who.Lucy, Side.Left, "Ryker!"),
// (Ryker: a small sound, no words)
Line(Who.Lucy, Side.Left, "She's breathing. She's alive."),
Line(Who.Toba, Side.Right, "Frightened. Tired. Nothing worse."),
Line(Who.Linda, Side.Right, "You scared us half to death, you know."),
// optional, by the pick:
Line(Who.John, Side.Right, "Come on. Let's take her home."),
Line(Who.Mark, Side.Right, "Home. All of us."),
Line(Who.Lucy, Side.Left, "I've got you. I've got you."),
Line(Who.Toba, Side.Right, "The fire is low. Let's get her home."),
```

Count: 7 spoken lines without the pick, 8 with it (within the 4 to 8 asked), plus the Ryker sound. Cut to 5 if THJ wants it shorter: 3.1, 3.3, 3.4, 3.7, 3.8.

### 3.2 Alternative (Option B): found, not shown. Use this if Ryker's state or kind is uncertain

If THJ can't yet say what Ryker is, how she looks or what the Queen did, **don't show her**: the camera stays on a door, a cage or a nest, the sound is heard, and the family reacts to a sound and to Toba's word. It asserts no state and no species, and it needs no Ryker art in the scene (only the sound). It can be upgraded to Option A later without rewriting the family's lines.

| # | Speaker | Trigger | Line | Notes | Flag |
|---|---|---|---|---|---|
| B.1 | Lucy | Camera on the door or cage, Ryker unseen but heard (small sound) | Ryker? | She stops. She's afraid to be wrong | **Needs approval** |
| B.2 | Toba | Same dialog | That's her. She is alive. | Toba says what Lucy hasn't dared to | **Needs approval** |
| B.3 | Lucy | Same dialog | Ryker. I'm here. | She goes to the door. Cut to the fade; the reunion itself happens at Home | **Needs approval** |
| B.4 | The pick (J) / (M) | Same dialog, optional | John: Go. We're right behind you. / Mark: Go. We'll hold the hall. | Gives Lucy permission to run. John's is a father's, Mark's the brother-in-arms. Pick one per pick | **Needs approval** |

Lines to paste, only after approval:

```csharp
Line(Who.Lucy, Side.Left, "Ryker?"),
// (Ryker: a small sound, no words)
Line(Who.Toba, Side.Right, "That's her. She is alive."),
Line(Who.Lucy, Side.Left, "Ryker. I'm here."),
// optional, by the pick:
Line(Who.John, Side.Right, "Go. We're right behind you."),
Line(Who.Mark, Side.Right, "Go. We'll hold the hall."),
```

Count: 3 spoken lines, 4 with the pick.

**Rec.: Option A if §5 Q1 to Q3 get answers; Option B until they do.**

---

## 4. What is unchanged, and what this file doesn't cover

- **M3's end** (Toba appears: "he knows the way to the Rootwell and where Ryker is", M3-06): a separate text task. These M4 lines assume that beat and don't repeat it: Toba knows the Rootwell and has been with the family since then (he is a fixed squad member).
- **Barks** for M4 (kills, low HP, the Queen's fight, Cleanse): not in this file. None are proposed here.
- **Close-ups and captions** for the Dark Shaman and the Goblin Queen (EN-10 pattern): separate.
- **The Queen's own lines**, the "ritual frame" and any Home recap of M4: separate.
- **The Heavenly Sword pickup text** (its name and description): data, from PR-30. This file only calls it "the sword" (2.5).

---

## 5. Canon questions for THJ (answer before §3 is built)

These are questions, not guesses. Nothing here is asserted as canon.

1. **Who and what is Ryker?** Wolf cub (the snapshot's "cub", the wolf idles), or something else? Is she a pet, a ward, a lost child of the Rootwell, or a creature with her own story (the masked man gave her the name Waya in M11)? Option A's "little one" (3.5 alt) depends on it. The GDD itself flags it open (narrative-world Q1).
2. **Who is Ryker to the family, and to Lucy in particular?** The Hearth and Ridge lines say Lucy is bound to her and the whole family searches. Does the player already know why (the Hearth memories), so the scene only has to pay off? 3.1 and 3.7 assume a love like a sister's or a pet's, nothing more.
3. **What is her state when found?** Option A says alive, frightened and tired, not hurt (3.4). Is that right, or is she injured, ill or unconscious? Option B says alive and nothing else.
4. **How did she come to be there?** Did the Queen take her, did she go to the Rootwell herself, did Toba carry her there and hide her, or does the Queen merely guard the way? 2.3/2.4 ("how far is Ryker?" / "Close") and 3.4 stay neutral on this.
5. **Toba and Ryker.** The Ridge clues (a man's deep tracks, carrying something; herbs; a poultice; "Someone's carrying her. And tending her.") point at Toba. Is that his role in the story? If yes, 3.4 can become his line of knowledge ("She is as I left her."), and the family's thanks follows. If no, the clues point at someone else, and Toba's M3 line "I know where Ryker is" needs a different reason.
6. **Does Ryker speak, or make a sound only?** The proposal is a sound. If she has a voice later, the sound should match it.
7. **Does the demo end here, or does a Home scene follow?** The plan fades "home". Option A and B end at the fade; a reunion at Home (Ryker by the fire) would be a separate scene and the best place for the Lucy–Ryker warmth.
8. **The fourth seat.** Is it acceptable to ship pick-specific lines (J / M) in M4, or should the squad's lines be written without them? Either works: the pick lines are all optional.
9. **Toba's place in the scene.** He is "not yet family" (D-048). Does the family's reaction acknowledge him here (3.8 alt "Come. Her place is with you.")? A line like that would be the first step of his arc; if THJ wants that kept for later, use the Rec.
10. **Names to approve:** the level name **"The circles"** (plan; "pool" stays a design word) and the objective "Cleanse the circles." Both come from the plan, so they are only listed here for completeness.

---

## 6. Glossary proposals (not applied; `glossary.md` is untouched)

| Term | Proposal | Status |
| --- | --- | --- |
| **Mithra's Rest** | Replaces **Mithra's Gift** in the "Dungeon safe rooms" table: `LevelDivineRelicRoom 1`, heals the squad by 50% and fills FP, gives the Heavenly Sword (D-612, D-626). The old name stays for the unreworked `LevelDivineRelicRoom` | Name set by the plan; confirm on screen |
| **circles** (design word: pools) | Add to the Combat terms: the planted pools Cleanse destroys, **circles** on screen (level "The circles", objective "Cleanse the circles."); `pool` is a design word. Dark Shaman and Dark Claws are unchanged | Proposed |
| **Cleanse** | Add the term: the shared family ability, 1 AP, destroys Corruption within 1 cell; **in this demo only in M4-1** (D-614); Toba has none | Proposed |
| **Heavenly Sword** | Add to the Combat terms as a Divine Relic: three shared uses, a 3 × 3 of 10 × within 5, for the mission (PR-30 to PR-32); walk-on in M3 (8,6), given again at Mithra's Rest | Proposed |
| **Ryker** | Add under a new "Story" table: **she**, the one the family searches for (the Hearth), Lucy's bond; found at the end of M4. **Species and role: Miso-only until THJ answers §5 Q1** (already proposed in `m1-ridge-redesign-text.md` §10; not applied there either) | Proposed |
| **the Rootwell** | Add under "Story": the dangerous place where Ryker may be, file name "The White Mothers". Already in `narrative-world.md`. The mission is "The White Mothers" in the demo; the Rootwell is the place. Check: which of the two names does the player see in the map? | Proposed |
| **Toba, joins after M3** | The Toba row says he joins "after M4"; the plan moves it to after M3 (found under the stone). Update the row, and `toba.md` when THJ confirms | Needs THJ |
| **Marks-Sisters** | A Duo node name ("Duo damage, 2 pips"). The Duo's own on-screen name is not decided. No line here names it. Open: should the first-use Duo have a screen name? | Open |
