# Player Skill Trees — Demo Redesign (on `main`, committed and merged 2026-10-04)

> **Status: not verified by play.** Only the logic smoke test passed. THJ suspects some values or nodes are wrong. Example: this doc says Sidewinders is +1/+2, but the game already shows +3. Every value below must be checked in play; see `playtests/playtest-plan.md`, item (n). Treat the numbers here as the design intent, not confirmed behaviour.

## Rules
- Every unit tree: **6 nodes, 8 pips, 4 tiers** at unit level (SP spent) 0/1/2/3, **2 prerequisite edges** (A→C, B→F).
- Template: Tier I = A Signature unlock (1) + B Core (2) · Tier II = C Signature+ (1, needs A) + D Bond/squad-wide (1) · Tier III = E Trick (1) · Tier IV = F Mastery (2, needs B).
- One locked signature ability per unit, unlocked for 1 SP at Tier I. Duos and synergies stay unlocked by default; the family tree only upgrades them (except Tempest Bloom and Catch & Return).
- Each unit's first 3 SP earn 1 Family SP each (3 per unit, 15 total). XP table left at 10 entries, so a unit can earn 10 SP; the tree costs 8, leaving 2 SP of headroom.
- **Code changes:**
  - `SkillTree.cs` now honours the node's **Upgrade Levels** field as a cap (0 = no cap). Levels authored above the cap stay free for runes, Papa's Shelter, etc.
  - `UpgradeLevelBarUI.Initialize` is guarded against an empty level list.

## Unit trees
| | John | Lucy | Linda | Mark | Toba |
|---|---|---|---|---|---|
| A | Father's Resolve (lock) | Blink (lock) | Harmonic Slam (lock) | Command (lock) | Protective Shell (lock) |
| B | Shield Up 0.6→0.5→0.4 | Sidewinders +1/+2 (cap 2 of 5; base attack already has 1; **in-game shows +3: check**) | Longshot +1/+2 range | Heavy Hands Fist Blitz ×1.2/×1.4 | Healing Wind ×1.5/×2 |
| C | Decisive Resolve (2 AP) | Rapid Blink (cd 1→0) | Diminishing Blow (Slam Weak) | Sapping Order (Command Weak) | Guardian's Reach +1 |
| D | Of the Same Blood: family HP ×1.2 | Kindled Spirits: family crit +10% | Move as One | Flowing Guard: family evasion +5% | Provoking Presence +1 (personal) |
| E | Sundering Strikes (Sword Vulnerable) | Lingering Embers (Burn) | Louder Crescendo ×1.2 | Stunning Vault | Nature's Rhythm +1 AP |
| F | Battering Charge: Dash +1/+2 | Cyclone Power ×1.2/×1.4 | Power-Piercing 0.6→0.8→1.0 | Atman Body DR 0.1/0.2 | Nature's Gambit +1/+2 |

## Family tree (9 nodes, 15 FSP, no prerequisites)
| Group | Node | Pips | Effect |
|---|---|---|---|
| Trio | Tempest Bloom (unlock) | 1 | Projectiles split through the cyclone |
| Trio | Marks-Sisters | 2 | ×1.2/×1.35 |
| Trio | John-Linda Dance | 2 | +1/+2 |
| Trio | Hide and Seek | 2 | 2→3→4 decoys |
| Mark | Sidewinder Blitz | 2 | ×1.2/×1.35 |
| Mark | Family Watchers | 2 | Radius 3→4→5 |
| Mark | Head Start | 1 | Race cd 2→1 |
| Mark | Catch & Return (unlock) | 1 | Mark returns Linda's arrows |
| Toba | Healing Marks | 2 | ×1.5/×2 |

Family Time and Family Lookout were removed, because main runs ATB.

## Data changes
- **Prefabs** (`Unit_John`/`Lucy`/`Linda`/`Mark`/`Toba`): skillTree overrides rewritten. `LucyFactionSharedStats` and `MarkFactionSharedStats` additional stat sources were added, and both IDs were added to all 5 stat profiles.
- **Locks** (`lockedByDefault 1`, SP1 unlock, `upgradable 1`): Teleport, Harmonic Slam, Command, Dom Barrier.
- **Level and stat additions:** Dash range level 2; Fist Blitz Stat_DMG 1/1.2/1.4; Mark_John radius stat-backed (base 3 + Stat_AUXADD, FSP levels); Mark_Linda cooldown stat-backed (base 2 − Stat_CLD, FSP level).

## Verification so far
- Static parse of every edited file.
- Unity compile: 0 errors.
- `Tools/Skill Trees/Run Smoke Test (Play Mode)` (editor-only `Core/Editor/SkillTreeSmokeTest.cs`): ALL PASSED. It checks tiers, edges, caps, locks, 15 FSP, auras, Watchers radius and race cooldown. It reads runtime values and does not play combat.
- The Upgrades panel was checked visually: John, Linda, Lucy, Mark and the family tab. Toba was locked in that save.
- **Not done:** a combat playtest of any node. Tracked in `playtests/playtest-plan.md`, item (n).

## Deferred by THJ
- Rune overlaps: buying Sundering Strikes, Lingering Embers, Stunning Vault, Sapping Order or Diminishing Blow removes the matching rune from the altar pool, and maxed range nodes block their range runes.
