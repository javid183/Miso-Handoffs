# Linda's Quiver: placeholder text

Narrative agent, 2026-10-26, branch `thj/linda-quiver`. Read-only on `miso\`. For chunks C2 (hand-back barks), C3 (Recall) and C4 (UI strings) of [`plans/2026-10-26-linda-quiver-tech.md`](../plans/2026-10-26-linda-quiver-tech.md); rules from [`plans/2026-10-26-linda-quiver-design.md`](../plans/2026-10-26-linda-quiver-design.md).

**Every line below is a placeholder.** In data, prefix each with `[PLACEHOLDER] ` (stripped on screen). The ability name (section 2) and the glossary rows (section 4) are Tier 3 proposals and need THJ. The rest is Tier 2: new text in the established voice.

Voice references used: the role barks on the prefabs (`In my sights.` / `Clean shot.`, `No!` / `I got you!`, `Leave some for me!` / `Catch this!`, `Not my family.` / `Breathe. Strike.`, Toba's `Let me light your way!`), and the house description style (`Shoots an arrow that damages enemies in a row.`, `Attacks enemies that move within her range. (1 FP)`, badge line `Needs 2 FTP; Pass-by refills FTP.`).

## 1. Hand-back barks

The beat is about 0.6 s: picker line, then Linda's reply, both as over-head popups. Lines are 1 to 5 words so they read in one glance. Every picker line works with every Linda reply (they are picked independently), and no line names a mechanic.

Character notes behind the lines:
- **John**: the father; warm, brief, a little proud of her.
- **Lucy**: the cheeky younger sister; teasing, never sour. Avoids `Catch` (her role line is already `Catch this!`).
- **Mark**: the monk; few words, calm, a touch of the koan.
- **Toba**: the newcomer, not yet family (D-048). Polite, slightly unsure of his place, nature-minded. He never says "sis" or uses family words for her.

### Picker lines (3 each)

| Picker | Line 1 | Line 2 | Line 3 | Feel |
| --- | --- | --- | --- | --- |
| John | `Catch, Linda!` | `Dropped this, love.` | `Here. Keep shooting.` | A father tossing it back without breaking stride |
| Lucy | `Sis! Yours!` | `Found one!` | `You owe me!` | Pleased with herself; the sibling tease |
| Mark | `Yours, sister.` | `Nothing is lost.` | `It returns to you.` | Quiet; the arrow's return as a small lesson |
| Toba | `Linda! Your arrow.` | `Yours, I think?` | `The ground gives it back.` | Helpful and a bit careful with her; the earth image is his |

### Linda's replies

Generic (any picker):

| # | Line | Feel |
| --- | --- | --- |
| G1 | `Got it.` | Calm, the default |
| G2 | `Thanks.` | Plain warmth |
| G3 | `Back where it belongs.` | Her precision; a quiver in order |
| G4 | `Every one counts.` | Names the stakes without naming the mechanic |

Optional, one per picker (use when the picker is that sibling; otherwise fall back to the generic set):

| Picker | Line | Feel |
| --- | --- | --- |
| John | `Thanks, Dad.` | The only place she calls him that in combat text; flag for THJ (see notes) |
| Lucy | `Show-off.` | Fond sibling jab; answers all three of Lucy's lines |
| Mark | `Thank you, Mark.` | She matches his formality |
| Toba | `Thank you, Toba.` | Kind to the newcomer; their showcase pair at Home |

Suggested mix: 50% the picker's own reply, 50% a generic one, so the sibling lines stay special.

### Linda picking up her own arrows (no reply)

| # | Line | Feel |
| --- | --- | --- |
| S1 | `There you are.` | Fond, to the arrow |
| S2 | `Waste not.` | Practical, the careful archer |

### Data block (paste-ready)

```
John:  [PLACEHOLDER] Catch, Linda! | [PLACEHOLDER] Dropped this, love. | [PLACEHOLDER] Here. Keep shooting.
Lucy:  [PLACEHOLDER] Sis! Yours! | [PLACEHOLDER] Found one! | [PLACEHOLDER] You owe me!
Mark:  [PLACEHOLDER] Yours, sister. | [PLACEHOLDER] Nothing is lost. | [PLACEHOLDER] It returns to you.
Toba:  [PLACEHOLDER] Linda! Your arrow. | [PLACEHOLDER] Yours, I think? | [PLACEHOLDER] The ground gives it back.
Linda reply, generic: [PLACEHOLDER] Got it. | [PLACEHOLDER] Thanks. | [PLACEHOLDER] Back where it belongs. | [PLACEHOLDER] Every one counts.
Linda reply, to John: [PLACEHOLDER] Thanks, Dad.
Linda reply, to Lucy: [PLACEHOLDER] Show-off.
Linda reply, to Mark: [PLACEHOLDER] Thank you, Mark.
Linda reply, to Toba: [PLACEHOLDER] Thank you, Toba.
Linda self-pickup: [PLACEHOLDER] There you are. | [PLACEHOLDER] Waste not.
```

Notes for the implementer:
- G3 (an arrow landing on a Bergson's tile goes straight back) uses the same lines: the Bergson on the tile is the picker.
- Several stacks picked up in one move: one beat per pickup, as the tech plan says; avoid repeating the last line used by the same picker if cheap to do.
- The barks respect `GlobalSettingsSO.silenceBarks` like the role barks.

## 2. Recall

### Name

| Option | Feel | Notes |
| --- | --- | --- |
| **A. Encore** (recommended) | Musical, like the rest of her kit (Harmonic Slam, Explosive Crescendo): the arrows come back for another round. Warm, a little showy | The later skill node becomes "Barbed Encore". The design docs and code keep `Recall` (`Linda_Ability_Recall`); only the screen says Encore |
| B. Recall | Plain and instantly clear; what the design docs already call it | Safest for the cold-player test; no voice |
| Not chosen: Homecoming | Fits the family theme | Clashes with Home, the system and game mode |

Recommendation: **Encore**. It is in her voice, it says "again", and the description below tells the player what it does in its first words. If THJ prefers zero risk for the prototype's cold-player test, use Recall now and revisit after the playtest.

### Description (house style: what it does first)

`Every grounded arrow returns to her quiver, flying straight past walls and enemies. (1 AP, cooldown 2)`

- If the ability tooltip already shows AP and cooldown in their own fields, drop the parenthesis.
- No "deals no damage" clause: nothing in the line suggests damage. Barbed Recall/Encore will add its own line later.

### Cast barks (Linda)

| # | Line | Feel |
| --- | --- | --- |
| R1 | `Back to me.` | Calm command; works for either name |
| R2 | `Once more, from the top.` | The musician; pairs best with Encore. With Recall, use `Come home.` instead |

## 3. UI strings

| Where | Proposed text | Notes |
| --- | --- | --- |
| Quiver label, unit panel | `Quiver 3/4` (format `Quiver {count}/{size}`) | The pips under her unit need no text. Write "arrows", never "ammo" or "shots" |
| Watch prompt line | `Arrows 3 → 2` (format `Arrows {n} → {n-1}`) | Check that the in-game TMP font has the → glyph (U+2192); it's only used in editor text today. Fallback: `Arrows 3 > 2` |
| Greyed-ability reason (bow, Crescendo) | `No arrows` | Short reason, as asked. Optional longer tooltip: `No arrows. Pick them up or use Encore.` |
| Greyed Duo reason (Marks-Sisters, Healing Marks) | `Linda has no arrows` | The Duo panel is shared, so it names her |
| Greyed Recall reason | `No grounded arrows` | When the board holds none of her arrows |
| Empty-quiver badge tooltip line | `No arrows; walk over them or use Encore.` | Mirrors `Needs 2 FTP; Pass-by refills FTP.` With option B: `No arrows; walk over them or Recall.` |
| Move preview label | `+1 arrow` / `+2 arrows` (format `+{n} arrow` / `+{n} arrows`) | Count only what fits in her quiver. If some stay behind: `+1 arrow (1 left)` |
| Grounded-arrow tooltip (free) | `Linda's arrow. Any Bergson can pick it up.` / stacked: `Linda's arrows ×2. Any Bergson can pick them up.` | Optional, if the icon gets a hover |
| Locked-arrow tooltip | `Under an enemy. Encore still reaches it.` | With option B: `Under an enemy. Recall still reaches it.` |
| Quiver full on pickup (optional popup) | `Quiver full` | Only if extras stay on the tile and the beat needs to say why |

### Existing descriptions that now need the arrow cost (Tier 2, optional for the prototype)

| Asset | Current | Proposed |
| --- | --- | --- |
| `Linda_Ability_PrimaryAttack` | `Shoots an arrow that damages enemies in a row.` | `Shoots an arrow that damages enemies in a row. (1 arrow)` |
| `Linda_Ability_ExplosiveArrow` | `Looses an arrow skyward to fall upon her enemies with explosive force.` | `Looses an arrow skyward to fall upon her enemies with explosive force. (1 arrow)` |
| `Linda_Ability_FactionRole` | `Attacks enemies that move within her range. (1 FP)` | `Attacks enemies that move within her range. (1 FP, 1 arrow)` (Watch keeps 1 FTP in the prototype, D-246) |

## 4. Proposed glossary rows (not added; THJ approves)

For the Combat terms table:

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Quiver** [PROPOSED] | `LindaQuiver` | Linda's arrows: 4, full at the start of every level. Her shots (bow attack, Watch, Explosive Crescendo, her side of the arrow Duos) spend 1 each; at 0 they can't be used and Watch doesn't trigger. Shown as arrow pips under her unit and `Quiver 3/4` on her panel. Write "arrows", never "ammo" or "shots" |
| **grounded arrow** [PROPOSED] | `GroundedArrowField` (cell → stack) | One of Linda's arrows lying on a tile after a shot; never lost. Any Bergson whose move enters the tile **picks it up** and hands it back (the **hand-back**, the toss and two barks). Under a living enemy it is **locked** until the enemy moves or dies. Enemies ignore it |
| **Encore** [PROPOSED] (alt. **Recall**) | `Linda_Ability_Recall` | Linda's ability: every grounded arrow returns to her quiver in a straight line, past walls and enemies, locked ones too. 1 AP, cooldown 2, usable with at least 1 grounded arrow. Design docs call it Recall |

Rows to revisit when this is approved:
- The **Linda** row in The family says "2 per round from one pool (D-041)". The quiver supersedes that cap in the prototype (LI-11).
- **Conflict to settle:** the glossary's proposed "Role uses per round: **Watch**" uses Watch as a label for any role's uses ("Watch 2/2", "Watch Shots"), while the design plans use **Watch** as the name of Linda's Family Role. One word can't mean both; I suggest Watch stays Linda's role name and the uses label gets another word (for example "uses left").

## Needs THJ

1. Encore or Recall (section 2).
2. `Thanks, Dad.`: is "Dad" how the Bergson children address John? Children of Morta canon wasn't checked; `Thanks, Father.` and the generic `Thanks.` are the fallbacks.
3. The three glossary rows and the Watch wording conflict.
