# Cyclone v2: player-facing text (proposals)

Owner: narrative agent · Branch `thj/cyclone` · 2026-11-12 · Status: **proposals, working text**. THJ signs off the wording when he plays it. Nothing here is in the glossary or any asset yet.

Read from: `design/cyclone-redesign.md` (§4, §6, §7, approved as v2, D-530), `glossary.md`, `conventions.md`, GDD `characters/lucy.md`, and the current strings in the assets below (read only).

## House style found in the assets

- Ability descriptions: third person, present tense, one or two sentences, about 60 to 150 characters ("Leaps to a nearby tile fracturing the ground, slightly damaging and pushing enemies back."). AP and cooldown are not written in ability descriptions (the old "(1 FP)" suffix on Family Roles is the exception and is outdated).
- Skill-tree nodes: one short line naming the effect, no numbers ("Lucy's Cyclone hits harder.", "Lucy can blink more often.").
- Run upgrades: "<Unit>'s <Ability> applies <Status> for 2 turns." (Howling Gale, Harmonic Slam, Sword Vulnerable, Embers Burn all follow it).
- The Cyclone is written with a capital C in Lucy's own strings ("Lucy's Cyclone", "the Cyclone"); the Tempest Bloom strings say "cyclone". Proposals below use the capital everywhere.
- "cells" (the design word, and the built Steer text) over "tiles"; both appear in older assets.

All new text is placeholder until THJ plays it. Per conventions (D-348), nothing is tagged in the asset; this report is the list.

## 1. Cyclone (ability)

Asset: `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`

| Field | Old | New |
| --- | --- | --- |
| `title` | Cyclone | Cyclone (unchanged) |
| `description` | Creates a tornado that moves and damages enemies. | **Option A (recommended):** Summons a Cyclone for 3 enemy turns. On cast and after each enemy turn, it pulls enemies on its arms one cell in, then hits those beside it. Enemies can't pass or shoot through it. |

Other options for `description`:

| Option | Text | Feel |
| --- | --- | --- |
| A | Summons a Cyclone for 3 enemy turns. On cast and after each enemy turn, it pulls enemies on its arms one cell in, then hits those beside it. Enemies can't pass or shoot through it. | Plain rules in their order: lifetime, timing, pull, hit, block. About 180 characters, the longest of the three; the most complete. |
| B | Summons a Cyclone for 3 enemy turns. It Whirls on cast and after each enemy turn, pulling enemies on its arms one cell in and hitting those beside it. Blocks enemies. | Names the Whirl on screen, so the tooltip matches the combat log line "Whirl: pulled 2, hit 3". Needs "Whirl" approved as a player-facing term. About 170 characters. |
| C | Lucy's Cyclone holds a cross. On cast and after each enemy turn, enemies on its arms are dragged in and hit. The family passes through but can't stop in it. | The design's own sentence, in the narrator's voice. Says what it spares (the family) but leaves out the lifetime and the ranged block, and uses "cross" without showing it. Better as the unlock hint (5) than as the tooltip. |

Notes:
- "those beside it" is the on-screen word for the design's **touching cells** (the 4 cells next to it). "Touching" reads oddly in a tooltip.
- A and B leave out "the family passes through but can't stop in it": the move preview shows it, and the tooltip has no room. If THJ wants it in, swap A's last sentence for "Enemies can't pass or shoot through it; the family can pass but not stop." (about 200 characters).
- "3 ×" is left off the tooltip: no other ability description gives a multiplier, and the board already draws "3 ×" on the touching cells.

## 2. Steer (ability, replaces the Cyclone button while a Cyclone is out)

Asset: `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset`

| Field | Old | New |
| --- | --- | --- |
| `title` | Steer | Steer (unchanged, see below) |
| `description` | Move the Cyclone up to 3 cells, not through walls or enemies. It then pulls enemies on its arms one cell in. Once a turn. | Moves the Cyclone up to 3 cells, not through walls or enemies. Then it pulls enemies on its arms one cell in, without hitting them. Once a turn. |

Changes and why:
- "Move" becomes "Moves": every other ability description is third person; the built text is the only imperative one.
- Adds "without hitting them": the difference between a Gust and a Whirl is the thing players will get wrong, and it costs four words.
- "Once a turn" kept from the built text (design §7 says "once a turn").

On the name: keep **Steer**. It says what the player does (Lucy moves it; it never moves itself) and reads clearly on a button. Alternatives considered, not recommended: "Drive the Wind" (warmer, but long for the button), "Gust" (clashes with the Gust that follows the move).

## 3. Cyclone Power (skill-tree node, 2 pips: ×1.2 / ×1.4)

Asset: `miso/Assets/_Project/Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`, prefab override `skillTree.nodes.Array.data[5].description` (title at `data[5].title`).

| Field | Old | New |
| --- | --- | --- |
| `title` | Cyclone Power | Cyclone Power (unchanged) |
| `description` | Lucy's Cyclone hits harder. | **Option A (recommended): unchanged**, "Lucy's Cyclone hits harder." |

Options:

| Option | Text | Feel |
| --- | --- | --- |
| A | Lucy's Cyclone hits harder. | Still true under v2: Steer's Gust never hits, so "hits" can only mean the Whirl. Matches every other node (no numbers). No change needed. |
| B | Each Whirl of Lucy's Cyclone hits harder. | Names the moment it improves; needs "Whirl" on screen (as option 1B). |
| C | Lucy's Cyclone hits harder (+20% per level). | Gives the number, which no other node does today. Percent written by hand (locale bug). Only if nodes start showing numbers generally. |

## 4. Howling Gale (run upgrade)

Asset: `miso/Assets/_Project/Resources/RunUpgrades/LucyCycloneWeak/RU_LucyCycloneWeak.asset`

| Field | Old | New |
| --- | --- | --- |
| `title` | Howling Gale | Howling Gale (unchanged) |
| `description` | Lucy's Cyclone applies Weak for 2 turns. | Lucy's Cyclone applies Weak for 2 turns to every enemy it hits. |

Notes: keeps the house pattern ("applies Weak for 2 turns") and adds "to every enemy it hits", which tells the player a Steer's Gust (no hit) doesn't apply it. The old text is not wrong, so leaving it is also fine.

Related string, same upgrade (unlock list), optional:

| Asset / field | Old | New |
| --- | --- | --- |
| `miso/Assets/_Project/Resources/Unlockables/UnlockableSet.asset`, entry `id: LucyCycloneWeak`, `title` | Cyclone Weak | Howling Gale (so the unlock list uses the upgrade's name; check where this title shows before changing) |
| same entry, `description` | Lucy's Cyclone applies Weak. | Lucy's Cyclone applies Weak to every enemy it hits. |

## 5. Unlock hint (optional, one line)

Where: the Cyclone unlock beat on `thj/onboarding` (after the interruption). No string for it exists on `thj/cyclone`; the onboarding owner places it.

| Option | Text | Feel |
| --- | --- | --- |
| A (recommended) | Lucy's Cyclone holds a cross: when the enemy turn ends, foes on its arms are dragged in and hit, while the family walks straight through. | The design's sentence folded into one line; says what it stops and what it spares (principle 3). |
| B | Lucy's Cyclone holds a cross of wind, dragging in and striking any foe on its arms as the enemy turn ends. | Shorter, more narrator; leaves the family's pass-through for the board to teach. |
| C | Lucy's Cyclone holds a cross. At the end of the enemy turn, enemies on its arms are dragged in and hit. The family passes through but can't stop in it. | The design's three sentences verbatim: most exact, but three lines, not one. |

"Foes" appears only here, as narrator flavor; the tooltips keep "enemies".

## Glossary proposals (for THJ; not added yet)

| Term (player-facing) | Code name | Proposed meaning | On screen? |
| --- | --- | --- | --- |
| **Cyclone** | `Lucy_Cyclone_Ability`, `Cyclone.prefab` | Lucy's ability and the thing it leaves on the board. Always capital C ("Lucy's Cyclone", "the Cyclone"); the lowercase "cyclone" in the Tempest Bloom texts is the old form | Yes (existing) |
| **Steer** | `Lucy_Ability_Steer` | The ability that replaces Cyclone's button while one is out: moves it up to 3 cells, then a Gust. Once a turn | Yes (button, tooltip) |
| **Whirl** | `CycloneWhirlSteps` | The Cyclone's only damage: on cast and after each enemy turn, pull then hit | In the combat log for sure; in tooltips only if options 1B / 3B are chosen |
| **Gust** | (Steer's pull) | The pull alone, no hit, after a Steer | Combat log ("Gust: pulled 1"); not in tooltips (the Steer text says "without hitting them" instead) |
| **arms** | | The 8 cells in straight lines, 2 out from the Cyclone | Yes, in the Cyclone and Steer tooltips ("enemies on its arms") |
| **cross** | | The Cyclone plus its arms, drawn on the ground | Unlock hint only (option 5); design word elsewhere |
| touching cells | | The 4 cells next to the Cyclone, where the Whirl hits | Design word only. On screen: "beside it" |
| pull | `AEffectPusher` (forced move) | Moving an enemy 1 cell toward the Cyclone | Yes, as a plain verb |

Gap found, not new: **Weak** (and Burn, Vulnerable) are on screen in several run upgrades but not in the glossary. Worth a status-effects section once their rules are confirmed.

## Not in scope, flagged

- GDD `characters/lucy.md` line 24 (Cyclone row) and lines 52 and 77 still describe v1 ("lasts 5 turns, moves up to 3 cells a turn toward units", "7 ×"); design build step 5 rewrites them (game designer).
- The Tempest Bloom node (`Unit_Lucy.prefab`, `skillTree.nodes.Array.data[6].description`) and `RU_LindaLucyCycloneSpreadUnlock.asset` write "cyclone" in lowercase; a one-letter fix when someone is in those files.
- The duplicate Cyclone assets under `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/` (design §10) were not read; if they carry a description, it would need the same text.
