# Player Skill Trees — Demo Redesign (on `main`, committed and merged 2026-10-04)

> **Current values live in the GDD (D-047).** The trees as built, read from the prefabs on 2026-10-16, are on the character sheets: [John](gdd/characters/john.md#skill-tree), [Linda](gdd/characters/linda.md#skill-tree), [Lucy](gdd/characters/lucy.md#skill-tree), [Mark](gdd/characters/mark.md#skill-tree), [Toba](gdd/characters/toba.md#skill-tree). How SP and FSP are earned and spent: [PR-6 to PR-8](gdd/progression-economy.md#experience-and-levels). This file keeps the redesign's intent, its template and reasoning, the data changes and the verification history. Where the build differs from the intent, the table below says so. **Still not verified by play:** a combat playtest of the nodes is `playtests/playtest-plan.md`, item (n).

## Rules (design intent)
- Every unit tree: **6 nodes, 8 pips, 4 tiers** at unit level (SP spent) 0/1/2/3, **2 prerequisite edges** (A→C, B→F).
- Template: Tier I = A Signature unlock (1) + B Core (2) · Tier II = C Signature+ (1, needs A) + D Bond/squad-wide (1) · Tier III = E Trick (1) · Tier IV = F Mastery (2, needs B).
- One locked signature ability per unit, unlocked for 1 SP at Tier I. Duos and synergies stay unlocked by default; the family tree only upgrades them (except Tempest Bloom and Catch & Return).
- Each unit's first 3 SP earn 1 Family SP each (3 per unit, 15 total). The XP table was left as it was, which leaves 2 SP of headroom over a full tree ([PR-6, PR-7](gdd/progression-economy.md#experience-and-levels)).
- **Code changes:**
  - `SkillTree.cs` now honours the node's **Upgrade Levels** field as a cap (0 = no cap). Levels authored above the cap stay free for runes, Papa's Shelter, etc.
  - `UpgradeLevelBarUI.Initialize` is guarded against an empty level list.

## Unit trees
The slots of the template, by unit. Each node's effect, pips and unlock level: the sheet linked in the column head.

| | [John](gdd/characters/john.md#skill-tree) | [Lucy](gdd/characters/lucy.md#skill-tree) | [Linda](gdd/characters/linda.md#skill-tree) | [Mark](gdd/characters/mark.md#skill-tree) | [Toba](gdd/characters/toba.md#skill-tree) |
|---|---|---|---|---|---|
| A | Father's Resolve (lock) | Blink (lock) | Harmonic Slam (lock) | Command (lock) | Protective Shell (lock) |
| B | Shield Up | Sidewinders | Longshot | Heavy Hands | Healing Wind |
| C | Decisive Resolve | Rapid Blink | Diminishing Blow | Sapping Order | Guardian's Reach |
| D | Of the Same Blood | Kindled Spirits | Move as One | Flowing Guard | Provoking Presence |
| E | Sundering Strikes | Lingering Embers | Louder Crescendo | Stunning Vault | Nature's Rhythm |
| F | Battering Charge | Cyclone Power | Power-Piercing Arrows | Atman Body | Nature's Gambit |

### Where the build differs from this design
| Design | As built (GDD, 2026-10-16) | Where |
|---|---|---|
| Tiers at 0 / 1 / 2 / 3 SP spent | Nodes unlock at 0, 0, 2, 2, 3 and 5 SP spent | [PR-7](gdd/progression-economy.md#experience-and-levels), Progression Q2 |
| A unit's first 3 SP each earn 1 FSP | 1 FSP when the SP spent reaches 2, 3 and 5; only purchases in the skill-tree panel count | [PR-8](gdd/progression-economy.md#family-skill-points-and-family-level), Progression Q1 |
| Sidewinders +1 / +2, capped at 2 | Set up with upgrade mode 0, unlike every other numeric node: the likely cause of the "+3" and the "Maxed Out" seen in play | [Lucy](gdd/characters/lucy.md#open-questions) Q1 |
| Nature's Rhythm: +1 AP | Raises his AP cap only; he still starts each turn with 2 AP | [Toba](gdd/characters/toba.md#open-questions) Q4 |
| Sidewinder Blitz (Mark–Lucy Duo node) | Named Chained Assault | [Mark](gdd/characters/mark.md#open-questions) Q5 |
| Rune overlaps deferred (below) | Already built for unlocks and level-ups | [Deferred and dropped](gdd/progression-economy.md#deferred-and-dropped) |

## Family tree
Nine nodes, no prerequisites, grouped by the design as the Trio's (the starting three), Mark's and Toba's. As built they sit on the character trees and cost 15 FSP in all ([PR-8](gdd/progression-economy.md#family-skill-points-and-family-level)). Effects and pips: each sheet's Skill tree section and the [Duos](gdd/family-systems.md#duos) and [Synergies](gdd/family-systems.md#synergies) tables.

| Group | Nodes | Sits on |
|---|---|---|
| Trio | Tempest Bloom (unlock), Marks-Sisters | Lucy's tree |
| Trio | John-Linda Dance, Hide and Seek | John's tree |
| Mark | Chained Assault (designed as Sidewinder Blitz), Family Watchers, Head Start, Catch & Return (unlock) | Mark's tree |
| Toba | Healing Marks | Toba's tree |

Family Time and Family Lookout were removed, because main ran ATB then. (`main` has run FTP since `92853a5a9`; the GDD lists both as dropped.)

## Data changes
- **Prefabs** (`Unit_John`/`Lucy`/`Linda`/`Mark`/`Toba`): skillTree overrides rewritten. `LucyFactionSharedStats` and `MarkFactionSharedStats` additional stat sources were added, and both IDs were added to all 5 stat profiles.
- **Locks** (`lockedByDefault 1`, SP1 unlock, `upgradable 1`): Teleport, Harmonic Slam, Command, Dom Barrier.
- **Level and stat additions:** Dash range level 2; Fist Blitz Stat_DMG 1/1.2/1.4; Mark_John radius stat-backed (base 3 + Stat_AUXADD, FSP levels); Mark_Linda cooldown stat-backed (base 2 − Stat_CLD, FSP level).

## Verification so far
- Static parse of every edited file.
- Unity compile: 0 errors.
- `Tools/Skill Trees/Run Smoke Test (Play Mode)` (editor-only `Core/Editor/SkillTreeSmokeTest.cs`): ALL PASSED. It checks tiers, edges, caps, locks, 15 FSP, auras, Watchers radius and race cooldown. It reads runtime values and does not play combat.
- The Upgrades panel was checked visually: John, Linda, Lucy, Mark and the family tab. Toba was locked in that save.
- 2026-10-16: the GDD read every tree from the prefabs and `SkillTree.cs` (a static read, not play). The differences are in the table above.
- **Not done:** a combat playtest of any node. Tracked in `playtests/playtest-plan.md`, item (n).

## Deferred by THJ
- Rune overlaps: buying Sundering Strikes, Lingering Embers, Stunning Vault, Sapping Order or Diminishing Blow removes the matching rune from the altar pool, and maxed range nodes block their range runes. (Partly built already: see the differences table.)
