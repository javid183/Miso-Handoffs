# Mark–Linda Duo: name proposals

Owner: miso-narrative · 2026-10-27 · Status: **all PROPOSED, placeholder until THJ approves** (Tier 3)
Sources: `plans/2026-10-27-linda-distance-design.md` (Q4, step D2), `decisions.md` D-265 / D-268, `design/gdd/family-systems.md` (Duos), `design/gdd/characters/mark.md`, `linda.md`, the barks CSVs.

## The brief

- Replaces **Family Footrace** (`Mark_Linda_Duo`). Linda shoots down a lane; Mark sprints after the arrow, sweeps her grounded arrows on his path, reaches the landing cell as the arrow lands, and tosses the bundle back to her quiver. If Catch & Return is unlocked, its QTE can happen at the end. They end far apart, in sync.
- THJ: it should sound like **Mark racing Linda's arrow**. Not "Fetch Race" (the working name, D-268), not "Long Pass" (D-265), and clearly apart from **Catch & Return**.
- Avoid in the name: *catch*, *return*, *pass*, *fetch*. Also avoid *echo* (Echoing Retreat) and *mark* used as a common noun if possible (Marks-Sisters, Healing Marks).

**The family of names today:** John-Linda Dance, Hide and Seek, Marks-Sisters, Healing Marks, Chained Assault, Family Footrace, Family Watchers. Two strands: childhood games the siblings would have played (Hide and Seek, Footrace, Dance), and plain verb-object action names. Linda's own kit adds a musical strand (Harmonic Slam, Explosive Crescendo, Encore). A good name sits in the first strand and can wink at the third. Mark's tree keeps **Head Start** (cooldown −1); a race name keeps that node's name working.

## Names

| # | Name | Why |
| --- | --- | --- |
| 1 | **Race the Arrow** (recommended) | Says exactly what THJ asked for: Mark races her arrow, not her. Reads like a dare between siblings ("bet you can't race my arrow"), sits next to Hide and Seek and Footrace, and keeps Head Start meaningful. 14 characters. |
| 2 | **Arrow Chase** (runner-up) | Shorter and more like a game's name (like Tag or Hide and Seek). Slightly less clear on who chases what, but the animation answers that at once. 11 characters, the safest fit on a button. |
| 3 | **Keep Pace** | The sync reading: Mark arrives as the arrow lands, a tie, not a win. "Pace" is both running and tempo, so it touches Linda's musical kit. Loses the word "arrow", so it says less on its own. |
| 4 | **Tempo Run** | Linda sets the tempo with the shot, Mark runs it. Musical plus speed, one per sibling. Sounds a bit like a gym drill. |
| 5 | **First to the Mark** | Archery "mark" (the target) and his name in one pun; a race to the spot she marks. Fun, but it collides with Marks-Sisters and Healing Marks, and the pun may read as a typo for "Mark's". Flag only if THJ likes puns. |
| 6 | **Neck and Neck** | The race idiom for a dead heat: distant but synced, as a phrase. No arrow in it, so it needs the description to land. |
| 7 | **Fugue** | Music term: voices that chase each other, from the Latin for "flight". The most Linda name here, and a perfect metaphor, but obscure on a button and says nothing about Mark. |
| 8 | **Outrun the Arrow** | Strongest race feel, but promises Mark *beats* the arrow; in the design he meets it as it lands. Keep as a fallback if the timing changes. |

Not proposed: "Family Footrace" variants (the old Duo), anything with Catch, Return, Pass, Fetch (rejected or taken).

## Duo description (house style: what it does first, flavor second)

> **Race the Arrow.** Linda shoots down a lane and Mark races her arrow to where it lands, sweeping up her grounded arrows on the way and tossing the bundle back to her quiver.

Short variant for tight tooltips: *Linda shoots; Mark races the arrow to its landing, gathers her grounded arrows and tosses them home.*

Terms: "lane" (her row or column), "grounded arrows" and "quiver" follow the quiver design; none has a glossary row yet (see below).

## Barks when the Duo fires (placeholder)

Voice check against the CSVs: Linda is dry, steady, a little teasing with Mark ("Too quiet, even for you."); Mark is calm, breath-and-center, few words ("I hear more this way.").

| Speaker | Line | Feel |
| --- | --- | --- |
| Linda | Keep up, little brother. | Big-sister tease; the dare behind the name |
| Linda | Bring them all back. | Practical, about the bundle; trusts him |
| Mark | I will be there when it lands. | Calm certainty; the sync |
| Mark | Run with the arrow, not after it. | His monk framing of the race |

Alternates if wanted: Linda "On my count." / Mark "Loose it. I am already running."
CSV tag on entry if used before approval: `[PLACEHOLDER] `.

## Proposed glossary rows (do not add until THJ approves)

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Race the Arrow** [PROPOSED] (replaces Family Footrace; working name Fetch Race, D-268) | `Mark_Linda_Duo`, `UnitsCooperationHandler` (Mark_Linda) | The Mark–Linda Duo. Linda shoots down a lane; Mark sprints to the landing cell, picks up her grounded arrows on his path and tosses the bundle back to her quiver (0 net arrows). Catch & Return's QTE can follow if unlocked. Not "Long Pass" (D-265). Awaiting THJ |

The Duo row in the glossary (line 48, "Mark–Linda (the race)") would then read "Mark–Linda (Race the Arrow)". Separately, the quiver terms (quiver, grounded arrow, Encore per D-262) have no glossary rows yet; worth a pass once D1/D2 land.

## For THJ

1. Pick a name: recommended **Race the Arrow**, runner-up **Arrow Chase**.
2. Approve or swap the description and the four barks.
3. Should the node **Head Start** keep its name? It fits either race name.
