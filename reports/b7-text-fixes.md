# B7 · Text fixes (Oct 2026 playtest, Batch 1)

Narrative agent, 2026-10-18, branch `thj/oct-build-fixes` (= main). Read-only on the Unity project; nothing under `miso\` was edited.

## 1. Where the strings live

| File | Key / line | Current text |
| --- | --- | --- |
| `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelRunUpgradeRoom.prefab` | `levelName`, l.1772 | `Daryani's Shop` |
| same | `lObjectives.winObjectiveGroups.Array.data[0].objectives.Array.data[0].displayTextTemplate`, l.1860 | `Exit the refuge.` |
| `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelHealingRoom.prefab` | `levelName`, l.1820 | `Anahita's Ashiyan` |
| same | `lObjectives...data[0].displayTextTemplate`, l.1908 | `Exit the refuge.` |
| `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom.prefab` | `levelName` l.1917 / `displayTextTemplate` l.2005 | `Mithra's Gift` / `Exit the refuge.` |
| `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom 1.prefab` | `levelName` l.1891 / `displayTextTemplate` l.1979 | `Mithra's Gift` / `Exit the refuge.` |
| `miso/Assets/_Project/Resources/Tags/LevelSpecTags.asset` | `P0.HealngRoom.displayName`, l.36 | `Anahita's Ashiyan` |
| `miso/Assets/_Project/Resources/Tags/GTagRegistry.asset` | `HealngRoom.displayName`, l.173 | `Anahita's Ashiyan` |

No other hits for "Exit the refuge", Daryani, Anahita or Ashiyan (dialogue, sequences, CSVs, UI prefabs, scenes, .cs builders).

**"far ther": not found anywhere on this branch.** Searched all of `miso/Assets` (assets, prefabs, scenes, CSV, JSON, txt, .cs string literals), including splits across YAML line wraps, `\n`, rich-text tags and hyphens. Every "farther"/"further" in player text is spelled correctly:
- `Resources/Sequences/Mission 1/Level1C2/Level1C2_End_DialogNodeSequence.asset` l.34: "Father's mark. There's a passage behind that stone. He went farther."
- `Resources/Sequences/Mission 5/Home_Mission5_Selected_ExitHome_DialogNodeSequence.asset` l.33: "We finally know he went farther. I keep wondering what he found."
- `Resources/Sequences/Mission 6/LevelE2-C2/LevelE2-C2_Start_DialogNodeSequence.asset` l.23 and `Mission X/LevelE2-C1/LevelE4-C1_Start_DialogNodeSequence.asset` l.23: "Farther within The Arcanum, the path narrowed. ..."
- `Mission 6/LevelE2-C2/LevelE2-C2_End_DialogNodeSequence.asset` l.73 and `Mission X/.../LevelE4-C1_End_DialogNodeSequence.asset` l.73: "Then there may be more signs of him farther in."
- `Resources/BarkSystemData/Abilities/John/Ability_John_Primary - Sheet1.csv` l.3: "You will go no farther."
- `Features/Player/Linda/Prefabs/Unit_Linda.prefab` l.553: "Linda's arrows travel farther."

Same typo class (to gether, there fore, fa ther, bro ther, ano ther, whe ther, etc.): no hits. Either the typo was in an older build, or it is produced at runtime (e.g. a text box breaking a word). Needs the playtester's screenshot or the screen it was on.

## 2. What is wrong with "Exit the refuge."

What the rooms do (from the prefabs and code):
- **Daryani's Shop** (`LevelRunUpgradeRoom`): a `RunUpgradeAltar` drops 3 run upgrades; taking one withdraws the others. Nothing is paid. `allowedKinds` is empty, so the offer can be any kind (Ability Rune, Divine Relic, New Ability, Passive), not only runes. The level is won when any Bergson stands on one exit tile.
- **Anahita's Ashiyan** (`LevelHealingRoom`): stepping onto a trigger strip in front of the statue heals every Bergson once (`SafeRoomFunction`), then the statue's light goes out (`DisableRoomFunction`). Won when a Bergson stands on the exit tile, GridCell (13, -2) at the right edge.

The problem: the objective is the only instruction in the room and it names only the last step. It doesn't say why the player is here (take an upgrade; heal), so a player can walk straight out and lose the reward. "Refuge" is also a word the player never sees anywhere else, and it doesn't match the room's own name. Neighbouring objectives name the action and the place: "Pick up the Divine Relic and activate the altar.", "Reach the Pathmother.", "All units reach the exit."

## 3. Proposed changes

| Location | Current text | Proposed text | Tier | Note |
| --- | --- | --- | --- | --- |
| `LevelRunUpgradeRoom.prefab`, `lObjectives.winObjectiveGroups.Array.data[0].objectives.Array.data[0].displayTextTemplate` (l.1860) | `Exit the refuge.` | **Main:** `Choose one of Daryani's wares, then reach the exit.` | 2 | "Wares" fits the shop and stays true whatever kind of upgrade drops. 51 chars, the same length as the Divine Relic objective |
| same | `Exit the refuge.` | **Alt:** `Take one upgrade, then reach the exit.` | 2 | Plainer and more mechanical; "upgrade" matches the glossary's run upgrade |
| `LevelHealingRoom.prefab`, `lObjectives...data[0].displayTextTemplate` (l.1908) | `Exit the refuge.` | **Main:** `Approach the glowing statue to heal, then reach the exit.` | 2 | Points at the visible cue (the statue's light, which goes out after the heal). 57 chars |
| same | `Exit the refuge.` | **Alt:** `Stand before the statue to heal the family, then reach the exit.` | 2 | Says that everyone is healed. Longer (63 chars); check that it fits the objective box |
| Typo "far ther" | (not found) | none | 1 | Can't fix until we know where it was seen. Ask playtester S for the screen or a screenshot |

Notes for the implementer:
- Change only the `value:` on the lines given. Keep the trailing period (every neighbouring objective has one; the stats panel shows "<text>: Success").
- Per `conventions.md`, non-trivial asset edits go through an editor script; a one-line `value:` change on a prefab override can reasonably be done in the Inspector (Level component › lObjectives).
- "then" describes the intended order, but nothing in code stops the player from leaving without taking an upgrade or healing. That's a design or tech question, not a text one.
- Please check in play that the heal strip really sits in front of the statue. The prefab data suggests it does, but no one has seen it.

## 4. Questions for THJ (Tier 3, not decided)

1. **Mithra's Gift** (`LevelDivineRelicRoom.prefab`, `LevelDivineRelicRoom 1.prefab`) has the same `Exit the refuge.` but wasn't reported, and I found no altar or relic pickup in either prefab. What does the player do there? Once that's known, I'll write a matching line (Tier 2).
2. **"Shop"**: Daryani's Shop charges nothing (pick one of three, free). Keep the name, or should the room cost something? Also confirm whether Daryani, Anahita, Mithra and "Ashiyan" are meant as Children of Morta canon or Miso inventions.
3. Should "refuge" or "safe room" become the player-facing term for these rooms? If so, it goes in the glossary; today it appears nowhere else on screen.

## 5. Glossary (for approval, not added)

- **Daryani's Shop**: dungeon safe room, pick one of three run upgrades (`LevelRunUpgradeRoom`, tag `P1.Rune`).
- **Anahita's Ashiyan**: dungeon safe room, heals the squad once at the statue (`LevelHealingRoom`, tag `P0.HealngRoom`; the tag id's misspelling is code-only, leave it).
- **Mithra's Gift**: dungeon safe room, Divine Relic (`LevelDivineRelicRoom`, tag `P0.RewardRoom` / `P1.DivineRelic`).
