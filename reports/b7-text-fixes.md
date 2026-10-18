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

---

## Round 2 (2026-10-18, after THJ's answers)

State on disk when this was written: the Round 1 main lines are already in the prefabs. `LevelRunUpgradeRoom.prefab` l.1860 reads "Choose one of Daryani's wares, then reach the exit." and `LevelHealingRoom.prefab` l.1908 reads "Approach the glowing statue to heal, then reach the exit." Both Mithra's Gift prefabs still say "Exit the refuge."

### R2.1 · Typo "went far ther"

| Location | Current text | Proposed text | Tier | Note |
| --- | --- | --- | --- | --- |
| `miso/Assets/_Project/Resources/Sequences/Mission 5/Home_Mission5_Selected_ExitHome_DialogNodeSequence.asset`, `sequenceNodes[1].Text` (l.33), Lucy's line (`characterEnum: 3`) | `We finally know he went farther. I keep wondering what he found.` | No change: the asset is already correct | 1 | This is the line THJ describes: a Home mission-selection dialogue, played once (`PlayJustOnce: 1`) when Mission 5 is selected and the family leaves Home. The text on disk is plain ASCII "farther": an exact search for `went farther\.` matches it, and a search for any non-ASCII or invisible character between "far" and "ther" (soft hyphen, zero-width space or joiner, no-break space, BOM) finds nothing |

So the typo was in the playtest build but is not on this branch. Most likely it was fixed after that build (for example by a dialogue pass through the Dialogue Excel import). **To confirm:** the coordinator can run read-only `git log -S "far ther" -- "miso/Assets/_Project/Resources/Sequences"` to find the fixing commit, and QA should look at the line in play once.

What I searched, case-insensitive:
- Patterns: `went\s+far`, `know\s+he\s+went`, `finally\s+know`, `far\s*\n\s*ther`, `far ther`, `far("|<tag>|\n| -|- )`, `f\s?a\s?r\s?t\s?h\s?e\s?r`, `fa rther`, `fart her`, `far[non-ASCII]+ther`, and the invisible characters listed above.
- Where: all of `miso/` except `Library`, `Temp`, `Logs` and `obj`. That covers YAML sequences and dialogue assets, prefabs, scenes, CSV, JSON, txt and .cs.
- There are no .xlsx, .xls or .ods workbooks anywhere in the repo.
- The only "went far…" hits in the project are this line and "He went farther." in `Mission 1/Level1C2/Level1C2_End_DialogNodeSequence.asset` l.34, which is also correct.

### R2.2 · Mithra's Gift objective

| Location | Current text | Proposed text | Tier | Note |
| --- | --- | --- | --- | --- |
| `LevelDivineRelicRoom.prefab`, `lObjectives.winObjectiveGroups.Array.data[0].objectives.Array.data[0].displayTextTemplate` (l.2005) | `Exit the refuge.` | **Main:** `Take the Divine Relic from the altar, then reach the exit.` | 2 | Same shape as the other two rooms. "Divine Relic" is capitalised, as in the Mark intro objective ("Pick up the Divine Relic and activate the altar.") and the code's kind name. 57 chars |
| `LevelDivineRelicRoom 1.prefab`, same key (l.1979) | `Exit the refuge.` | the same string as the line above | 2 | Keep the two prefabs identical |
| (alternative, both prefabs) | `Exit the refuge.` | **Alt:** `Claim Mithra's gift at the altar, then reach the exit.` | 2 | Echoes the room name and hides the mechanic. Less clear for a new player; I prefer the main line |

### R2.3 · Glossary

Added to `claude-handoff/glossary.md` (THJ's answer is the approval):
- A new "Dungeon safe rooms" section with the three room names, their code names and tags, what each room does, and where each part of the name comes from (Daryani, Anahita and Mithra are Children of Morta canon; "Ashiyan" and "Shop" are Miso's).
- A canon table that records only that the names are canon; their canon roles are not asserted.

### R2.4 · Room name for Daryani's room, and the group term

**Where a room name appears on screen.** All three places read `LevelBase.levelName`:
1. Mission map node title (`MissionMapNodeUI.cs` l.63)
2. Map mission info panel title (`MapMissionInfoPanelUI.cs` l.122)
3. Combat HUD level info panel (`CombatLevelUIManager.cs` l.89 → `LevelInfoPanelUI.SetLevelName`)

The data is the `levelName` override in each room prefab: `LevelRunUpgradeRoom.prefab` l.1772, `LevelHealingRoom.prefab` l.1820, `LevelDivineRelicRoom.prefab` l.1917, `LevelDivineRelicRoom 1.prefab` l.1891.

Separately, the **mission map legend** (`MissionMapUI.PopulateLegend` → `MissionMapLegendRow`) labels each room-type icon with the spec tag's `displayName`, and it ignores `showInGame`. The labels live in both `Resources/Tags/LevelSpecTags.asset` and `Resources/Tags/GTagRegistry.asset`:
- `P0.HealngRoom` → "Anahita's Ashiyan" (LevelSpecTags l.36, GTagRegistry l.173)
- `P0.RewardRoom` → "Mithra's Gift" (LevelSpecTags l.43, GTagRegistry l.180)

**Tech warning (for the TD, not text):** `LevelName` is also an identity key, not just a label. The code uses it for:
- `GameHandler.LoadLevel`, `Mission.FirstOrDefault(l => l.LevelName == …)` and `MissionTracker` completed-level progress;
- the bark "Level Name" condition;
- the route seed, `Animator.StringToHash(LevelName)` in `CombatLevel.cs` l.146.

Renaming a room can break saved mission progress and changes that room's random seed. The Validation Dashboard's `LevelNameUniquenessCheck` also requires distinct names, yet both Mithra's Gift prefabs share one, worth a look. A rename should go through the TD.

**Daryani's room name: Tier 3, THJ picks.**

| Option | Feel |
| --- | --- |
| **Keep "Daryani's Shop"** (my recommendation if gold or prices are planned for this room) | Honest once it charges. The objective already fits it |
| **"Daryani's Wares"** (main rename if it stays free) | Keeps the merchant flavour without promising a sale. Matches the objective ("Choose one of Daryani's wares…"), so the objective needs no change |
| "Daryani's Cache" (alternative) | A stash found in the dark, free to take. More dungeon, less merchant. The objective would then read `Take one find from Daryani's cache, then reach the exit.` |

Question for THJ: is Daryani a merchant in Children of Morta canon? If not, "Shop" and "Wares" lose their footing, and "Cache" is the safer pick.

**Group term: "refuge".**
- After the Mithra's Gift line changes, "refuge" appears nowhere on screen (the only hits were the four "Exit the refuge." objectives).
- My recommendation: no player-facing group term for now. Each room shows its own name. Keep "safe room" as the internal and docs term (it matches the folder `DungeonSafeRooms`). No strings change for this.
- One related legend issue (Tier 2): `P0.RewardRoom` is labelled "Mithra's Gift" but is also Daryani's room's tag, so the map legend calls the shop "Mithra's Gift". Two fixes, either works:
  - (a) Give Daryani's room its own P0 tag. That's a TD and data change.
  - (b) Relabel `P0.RewardRoom` with a type word in the style of its neighbours ("Hostile", "Boss Lair"): **main** `Reward`, **alt** `Altar`. Change `displayName: Mithra's Gift` in LevelSpecTags l.43 and GTagRegistry l.180.
  
  THJ to choose (a) or (b). Also unchecked: if `P1.Rune` or `P1.DivineRelic` icons appear in the legend, their empty `displayName` falls back to the raw ids "Rune" and "DivineRelic" (no space). The fix would be `displayName: Divine Relic` for `P1.DivineRelic` (LevelSpecTags l.64), a Tier 1 fix. It needs a look at the map legend in play first.

---

## Round 3 (2026-10-18): a name for Daryani's room

THJ confirmed that Daryani is Children of Morta's merchant and that "Shop" is not a Morta word. The room: an altar drops three run upgrades, the player takes one for free, the rest vanish, then the player reaches the exit.

**What I know of Daryani in canon: low confidence.** I can't recall her role or any lines from Children of Morta well enough to cite them. Everything below rests only on THJ's word that she is the merchant. Nothing here quotes or assumes other canon.

| Option | Feel | Tier |
| --- | --- | --- |
| **Main: `Daryani's Wares`** | Still the merchant, but promises goods rather than a sale, so free doesn't jar. Matches the objective already in the prefab ("Choose one of Daryani's wares…"), so only the name changes | 3 (name; THJ picks) |
| **Alt: `Daryani's Cache`** | Goods she left in the dark for the family: free to take, more dungeon and less market. The objective would need to change too | 3 |

**Exact strings that would change**

| Location | Current | Main (Wares) | Alt (Cache) |
| --- | --- | --- | --- |
| `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelRunUpgradeRoom.prefab`, `levelName` override (l.1772) | `Daryani's Shop` | `Daryani's Wares` | `Daryani's Cache` |
| same prefab, `lObjectives.winObjectiveGroups.Array.data[0].objectives.Array.data[0].displayTextTemplate` (l.1860) | `Choose one of Daryani's wares, then reach the exit.` | no change | `Take one find from Daryani's cache, then reach the exit.` |

- `levelName` is the only place the room name lives, and it is what the mission map node, the map mission panel and the combat HUD show.
- No tag, bark, sequence, CSV or .cs references "Daryani's Shop" (searched all of `miso/`, excluding `Library`, `Temp`, `Logs` and `obj`). The legend label for this room comes from `P0.RewardRoom` ("Mithra's Gift"); see R2.4 (a)/(b). Renaming the room doesn't change it.
- **TD check before the rename:** `LevelName` is also the level's identity key (it's used to load the level, for saved mission progress and for the route seed; see R2.4). A save made with "Daryani's Shop" mid-mission may no longer match. I'll update the glossary once THJ confirms the pick.
