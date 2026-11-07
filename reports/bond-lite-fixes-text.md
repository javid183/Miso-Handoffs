# Bond Lite play fixes · text (miso-narrative, 2026-11-07)

For `plans/onboarding/2026-11-07-bond-lite-play-fixes.md` (C2, C3, C4). Everything here is placeholder grade (D-348: not tagged in assets; listed here). Page bodies follow the existing tutorial style: `• ` bullets, one per line (`\n` between). Margaret = Narrator node with the text prefix "Margaret: " (no Margaret dialogue character).

## 1. World map page (C2)

Plays after the Hearth close, with W6-1 just before it as a dialogue line (fits: it is the family's rule, the page is the how).

| Order | Kind | Speaker | Text |
|---|---|---|---|
| 1 | Dialogue | John | Two go out, two stay. Someone's here when she comes back. |
| 2 | Page title | | World Map |
| 3 | Page body | | • Open the world map at the fireplace.<br>• Pick a pin to choose a mission: The River or The Ridge, in either order.<br>• Each mission takes two Bergsons. The other two stay home. |

Notes
- Line 1 assumes the map opens from the Fireplace station (`Fireplace (world map)` in the C5 plan). If the player reaches it some other way, drop that bullet.
- "The River" / "The Ridge" are still working titles (glossary row pending); use whatever the pins show.
- W6-1 moves from "World map, on first open" to the Home dialogue before the page. W6-2 / W6-3 (pin hover) unchanged.

## 2. Skill tree page, Grandma Table (C3)

| Field | Text |
|---|---|
| Title | Skill Tree |
| Body | • Bergsons earn skill points as they level up.<br>• Each Bergson has a tree. Spend points here to learn new skills.<br>• The Family tab opens later. |

Notes
- "The Family tab opens later" is honest at this point (it opens after The Trail) and names the tab so the Yard can pay it off. If the tab's on-screen label is not "Family", use its label.
- Avoided "Family point" on purpose, see Glossary below.

## 3. Bond level-up line (C4)

Narrator node, immediately after the Bond rises. Uses the exact shape of the lock line `Opens with Linda & Lucy's Bond, Lv 2` so the player links the two.

- **A (rec.):** `Linda & Lucy's Bond reached Lv 2.` Plain, matches the lock line word for word.
- B: `Linda & Lucy's Bond reached Lv 2. New Family skills are open.` Says what it does; longer, and "Family skills" is not a glossary term yet.
- C: `Bond up! Linda & Lucy, Lv 2.` Punchier, more game-UI; less in the narrator's voice.

## 4. Lines as built

### H5-4 to H5-7, Hearth close (C2)

| ID | Node | Text |
|---|---|---|
| H5-4 | Lucy | Ryker? Come back by the fire. |
| H5-5 | Narrator | Margaret: Let her sit. She remembers too. |
| H5-5a (new, optional) | Narrator | The fire burned low. By morning, the door stood open. |
| H5-6 | Lucy | The door's open. Ryker's gone. |
| H5-7 | Mark | I'm staying. Until she's home. |

Changes
- **Added H5-5a** (proposal, THJ): the draft has night falling after H5-5 and H5-6 in the morning. In one dialogue sequence with no Home-state change, H5-5 to H5-6 reads as the same minute. H5-5a carries the time skip. If C2 can switch Home state (night, then morning) between the lines, drop H5-5a. If H5-5a stays, H5-6 can trim to `Ryker's gone.` (the door is already said).
- H5-4 reads best with Ryker visible by the door (`WolfSitDoor`). If the close plays in a state without her, the line still works (she is off-screen, Lucy calls her).
- Otherwise words as drafted.

### Y12-5 to Y12-7, the Yard (C4)

Recommended order: Y12-1 to Y12-4, Y12-5, Y12-6, **Bond step + Bond line**, Y12-7, pointer. The draft has the level-up on Y12-6 ("…That's faster." is the moment they work together); the plan puts the Bond step right after Y12-4, before they have done anything together. Text works either way, the story works better with the Bond after Y12-6.

| ID | Node | Text |
|---|---|---|
| Y12-5 | Lucy | You pin it, I burn it? |
| Y12-6 | Linda | …That's faster. |
| Bond | Narrator | Linda & Lucy's Bond reached Lv 2. |
| Y12-7 | Narrator | Margaret: First thing you two have done together all year. |

Changes: none to the words.

Flag (staging): Y12-1 "It's past midnight." and Y12-2 "Can't sleep…" assume night. The new Home state is a copy of Searching; if it is daylight, use Y12-1 `You've been out here for hours.` and Y12-2 `I keep seeing that pile.` (Y12-3, Y12-4 unchanged).

## 5. Workshop page (`Resources/Tutorials/Workshop_Tutorial.asset`)

Current: title `Workshop`; body `• Gear up the pair going out next.` / `• Equip each hero here before you pick the next mission.`

It still fits: it was written for the moment after the first pair mission, and that is when it now plays. One small gap: on a click, the player knew where they were; played by itself, the page should say what it points at. Suggested (optional):

`• This is the Workshop. Gear up the pair going out next.`
`• Equip each Bergson here before you pick the next mission.`

("hero" to "Bergson" for consistency with the new pages; either is fine.)

Flag: plan C3 acceptance says the Workshop page plays "on the first Home load after the Hearth", but the Workshop unlocks after River or Ridge. The text assumes after the first pair mission; after the Hearth, "the pair going out next" would be wrong (nobody has gone out yet).

## Glossary (proposed rows, THJ)

| Term | Proposed text | Status |
|---|---|---|
| Bond (update the Home row; now on screen on `thj/bond-lite`) | Relationship level between two family members, written `<A> & <B>'s Bond, Lv N` on screen. Opens Family-tree nodes for that pair (Bond Lite: Linda & Lucy only, Lv 2 opens Sister's Rivalry and Tempest Bloom). Raised by Home scenes (the Yard). No Bond meter (D-433) | Proposed |
| skill points | Points each Bergson earns on level-up, spent in their own skill tree at the Grandma Table | Proposed (term already used in plans) |
| **Clash to settle:** "Family point" | The Bond Lite plans call the Family Skill Point (FSP) a "Family point", but on screen **Family Points (FP)** already means the combat FTP pool (D-204). If the Yard ever shows a "+1 Family point" line, players will mix them up. Suggest "Family skill point" on screen for FSP | Needs THJ |
