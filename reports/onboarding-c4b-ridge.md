# Report: C4b The Ridge (`GB_s2-ridge`), Catch & Return by default, sleeper sight beat

Plan: plans/onboarding/2026-11-01-onboarding-c4-search-levels.md (C4b), check: reports/onboarding-c4-0-check.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. It compiles. Full EditMode suite: 1239 run, 1238 pass, and the one failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (the name was read from the run). After I put the River prefab back to its committed version, I re-ran the River, Ridge and sight-beat tests: 28 of 28 pass. Not play-checked, nothing committed, the save was not reset, and Play mode was not entered.

## Unit 1 · Catch & Return open by default (THJ decision D-352)

- `Resources/Unlockables/UnlockableSet.asset`: the `MarkLindaSynergy` entry (id `_MarkLindaSynergy`) now has `unlockedByDefault: 1`. That is a one-line change; the file is LF and nothing else in it changed.
- **What it opens.** `FactionTracker.HasMetaUnlockable` is now true for every save (`FactionTracker.cs:468-473`), so `ProjectileCatchAndReturn.TryCatch` passes its unlock gate (`ProjectileCatchAndReturn.cs:147`) from the start, in every mission.
- **Mark's Family-tree node** (node 9, "Catch & Return", `upgradeMode` UnlockableLiteral, `familyAbility` on, `Unit_Mark.prefab:392-831`):
  - It reads as **owned**: `GetCurrentLevel` returns 0, against −1 for locked (`SkillTree.cs:237`).
  - It is **no longer purchasable**: `CanUpgrade` is false once the state is unlocked (`SkillTree.cs:199`), so `TryUpgrade` refuses it and no Family SP can be spent on it.
  - **No refund.** A save that already bought it keeps the literal in `UnlockedLiterals`. The 1 Family SP it cost stays spent, and nothing gives it back.
  - **Nothing breaks downstream.** No other node lists it as a prerequisite (its guid `ba17205d…` appears only on itself). `IsUnlockedByGraph` treats it as maxed, so a child added later would open at once.
  - The node's description still promises the catch itself. When the designer gives it an upgrade effect, the text should change with it.
- **Tests.** No test asserted that it was locked: a grep for `MarkLindaSynergy` and `unlockedByDefault` in the tests found nothing. The new test `SearchRidgeTests.CatchAndReturnIsOpenByDefault` pins the new value.
- **Run upgrades.** A run upgrade that grants this literal would now count as already met (`RunUpgradeTracker.cs:383`). No run upgrade grants it, so nothing changes there.

## Unit 2 · Sleeper sight beat

- **New `Features/Onboarding/SleeperSightBeatSequence.cs`** (runtime sequence, about 120 lines with comments). It holds no static state.
  - It finds the Unaware enemy nearest the family by Manhattan distance; on a tie the first one wins.
  - It draws that enemy's sight tiles from `EnemyAlertTracker.TryGetUnawareRangeTiles` (`EnemyAlertTracker.cs:455`) with `GridCell.SetShiftPreview(ShiftPreviewLayer.EnemyMove, true)` (`GridCell.ShiftPreview.cs:68`) for `duration` (1.5 s), then clears exactly the cells it lit.
  - Exits:
    - the beat ending clears;
    - **skip** (`SkipStep`) clears and ends the wait;
    - **level end** (`CombatLevelRunHandler.IsLevelEnded`, or no run handler) ends the wait and clears;
    - **restart** reloads the level and its cells, and the next play clears its stale list first.
  - With no sleeper, or no family, it draws nothing.
  - The pure parts are `NearestSleeper` and `BeatOver`, both public static functions with no state, tested in `SleeperSightBeatTests` (4 tests).
- **Shared sequence** (`SearchWiring.Shared.cs`): `Search_FirstSleepingEnemy_SequentialSequence` (still `PlayJustOnce`) is now: disable input → the "Asleep" panel → the sight beat (`Search_FirstSleepingEnemy_SightBeat.asset`) → enable input.
  - The River gets it through the shared asset. **Wire Search: River** was re-run. The River's prefab needs no change, so I put it back to the committed version; see the risks below.
- A clash to watch in play: if the player holds Shift over another enemy during the beat, both previews write the same layer, and the first to clear clears both.

## Unit 3 · The Ridge

- **Block** (`claude-handoff/plans/onboarding/2026-10-26-onboarding-levels.md`):
  - id `ridge` → `s2-ridge`; image line → `onboarding-levels/s2-ridge.svg`;
  - added `level name The Ridge` and `level tier tutorial`;
  - drew `onboarding-levels/s2-ridge.svg` with `grid_render.py`. The renderer writes into a folder named after the doc, so I moved the one new SVG into place and deleted that folder.
  - The old `onboarding-levels/ridge.svg` is still there; delete it if it's no longer wanted.
- **Level `Content/Levels/Greybox/GB_s2-ridge.prefab`** (new, plus `.meta`): built from `s2-ridge` with the grid tool's builder and the default output path. No issues: 31 cells, 7 units, Tutorial, no alert line.
  - **Round trip:** `level_to_grid.py` reads back the same map (shifted x−1 because column 0 is all wall): 5 Dark Claws, Linda, Mark, tier Tutorial.
  - The template's statue and rocks are still there, as in the River.
- **Wiring `Features/Onboarding/Editor/SearchWiring.Ridge.cs`** (new, plus `.meta`), menu item **Tools › Onboarding › Wire Search: Ridge**. You can run it again at any time.
  - **Start:**
    - input off, HUD hidden;
    - the panel "Mark's Family Role" (Counter);
    - the opening lines;
    - input and HUD back on;
    - then, from the level's start event, the shared first-sleeper panel and sight beat, once per save. That gives the coordinator's order: role panel, opening lines, sleeping-enemy panel.
  - **Gauntlet health:** the two Claws on 7,1 and 8,1 get a per-instance override of their `Stat_HP` entry, factor **0.8333** (16 × 0.8333 × Tutorial 0.6 = 8). The entry is found by id, not by index. The shared Claw prefab is unchanged. The other three Claws stay at 1.
  - **Clue props** on 13,1 under `Search Scenery/Clue (placeholder)`: Tracks 1, Tracks 2, Herbs and Wrapper (tinted squares, no colliders). They are ground marks in the units' shadow slot for the tile's row, order 50 (row index 5), and are reused on re-runs.
  - **End:** input off, HUD hidden, a close-up camera on 13,1, the clue lines, then `OutroCutscene`.
  - **Win:** the default, defeat every enemy.
  - **The rush wakes at start by sight:** confirmed from the data and geometry with the default alert. 2,4 is 3 from Linda on 2,1 (sight 3), so it starts alert, and its spread (alert range 2) reaches 1,5 and 3,5. The gauntlet is 4 from Mark (out of sight) and out of the rush's spread. Tested.
- **Mission `Content/Levels/MS2 - The Ridge.asset`:**
  - the graph has one node, `GB_s2-ridge`, initial, no edges;
  - drops Gold 20 + Steel 2, fixed, with `resourceCollectionCount` 2;
  - `completionGoldReward` 0, `completionXPReward` 30;
  - roster checked, unchanged: Linda + Mark fixed, 0 free.
- **Shared helpers:** to reuse the River's code, `SearchWiringShared.BuildCamera(folder, …)` now holds the camera helper (the River calls it; same output). `Child`, `Piece`, `ClawLook` and `EnsurePropSprite` in `SearchWiring.River.cs` went from private to internal. The River's behaviour is unchanged: its tests pass, and its re-run left the River's own assets the same.
- **Tests `SearchRidgeTests`** (12):
  - level name, tier, default alert and win;
  - unit tiles;
  - rush wake and gauntlet sleep geometry;
  - gauntlet-only health factors;
  - start order and panel;
  - the shared panel's handle and single `levelStarted` call, the same asset as the River's;
  - clue position, sprites, sorting and colliders, and the end close-up;
  - no placeholder tag;
  - graph, drops and XP, roster;
  - Catch & Return default.

### Vault and catch, checked against the real data

- **Vault over the queue (6,1 → 9,1): works.**
  - Mark's Vault radius is `Stat_RANGE`: base 3 plus the level-0 value 0, with the additive policy, so **3**. Its cap reads `StatUB_SPD`, which the Bergsons faction sets to ×9999, so in effect there is no cap (`Mark_Ability_Attack_Vault.asset:82-101, 218-229`; `BergsonsFaction.asset:220-228`; `StatAttributeSet.CalculateStatFactor :139-143`; `AAttributeModifier.ModifyWithPolicyBasic :106-115`).
  - Jump mode, ranged reach, and the landing cell must be free. 9,1 is free, and 7,1 / 8,1 are crossed.
- **The catch: works, and the numbers beat the paper.**
  - Linda's bow reaches 4 (`radiusV` base 4 + `Stat_RANGE`). From 5,1 the arrow passes 7,1 and 8,1 and reaches Mark on 9,1: on the line, 4 ≥ 2 tiles away, an ally, a whitelisted arrow, and the gate is now open.
  - Damage is base 6. The falloff per earlier hit is the arrow's `onHitExtraModifier` (0.9 × `Stat_DMGD`). The only `Stat_DMGD` entry is the ability's own, at ×1, so the falloff is **0.9**, not 0.6.
    - Out: 7,1 takes 6, 8,1 takes 5.4. Neither dies at HP 8.
    - The return copy restarts its hit count: 8,1 takes 6, 7,1 takes 5.4.
    - Totals are **11.4 each**, so both die with room to spare.
  - If the catch is missed, the arrow lands under 8,1 as the plan says.
  - Not run in play: the arrow-hit rules (hit by contact, the return copy's first hit at full damage) are read from the code, not observed.

## Save reset

No.

## Decisions I made

- **The sleeper beat plays after the panel and before input comes back**, so the player sees the sight tiles before acting. Input-off steps were added around the panel and beat. The old shared sequence had only the panel.
- **The opening lines are my placeholder** (see below). The draft has no Ridge opening; its lines are clue, bark or framed-beat lines.
- **Mark's panel uses `Tut-FR-1.png` as a placeholder still** (the generic "Activate Passive" prompt). No Mark role image or clip exists in `Resources/Tutorials`.
- **The Catch & Return test sits in `SearchRidgeTests`** (unit 3), because unit 1 is a data change only.

## Needs THJ

None.

## Proposed commits (in order)

1. `feat(onboarding): Catch & Return is open from the start` (data):
   - `miso/Assets/_Project/Resources/Unlockables/UnlockableSet.asset`
2. `feat(onboarding): the sleeping-enemy panel shows the nearest sleeper's sight` (plain):
   - `miso/Assets/_Project/Features/Onboarding/SleeperSightBeatSequence.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SleeperSightBeatTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Shared.cs` (the beat in the shared sequence)
   - `miso/Assets/_Project/Resources/Sequences/Search/Shared/Search_FirstSleepingEnemy_SightBeat.asset` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/Shared/Search_FirstSleepingEnemy_SequentialSequence.asset`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchRiverTests.cs` (the shared steps now include the beat)
3. `feat(onboarding): The Ridge pair mission level and wiring` (plain):
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_s2-ridge.prefab` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Ridge.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchRidgeTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.River.cs` (the helpers shared with the Ridge)
   - `miso/Assets/_Project/Resources/Sequences/Search/Ridge.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/Ridge/*` (7 assets + `.meta`s)
   - `miso/Assets/_Project/Content/Levels/MS2 - The Ridge.asset`

   Note: `SearchWiring.Shared.cs` also gains `BuildCamera`, which the River (commit 3) and the Ridge both use. Because it's in commit 2, commit 2 builds alone, and commit 3 depends on it.

Leave out: `GB_m1-linda.prefab`, `GB_m3-john.prefab`, `ProjectSettings/*`, the two AI runtime files and the two Hearth test files. All of them were modified before this work or are reimport noise.

The handoff repo (not the shared repo): the block edit in `plans/onboarding/2026-10-26-onboarding-levels.md` and the new `plans/onboarding/onboarding-levels/s2-ridge.svg`.

All the files I wrote are LF without a BOM (CR count 0).

## Placeholder lines (wording not signed off, untagged in the assets)

- **Start (mine):** Mark "They've seen us." / Linda "Good. I hate waiting."
- **Panel "Mark's Family Role" (mine, from the role's facts):** "On the enemies' turn, when an enemy within 2 tiles of Mark attacks another family member, he can strike back with Fist Blitz. / Press the key shown above him. It costs 1 family time point and no action points."
- **End (draft G9-1 to G9-5, all at the close-up):** Mark "A man's tracks. Deep. He was carrying something." / Linda "Healing herbs, crushed fresh." / Mark "Someone knew which ones to pick." / Linda "A leaf wrapper. It still smells of salve." / Mark "Whoever he is, he's tending something."
- **Shared "Asleep" panel:** unchanged from C4a.

## "Send one my way." discovery bark: steps for THJ

No condition exists for "Mark stands in Linda's line with enemies between" or for "Linda has ≥ 1 arrow" (C4-0 check, question 7). The closest gate is "Mark vaults in the Ridge":

1. Open `Resources/BarkSystemData/Abilities/Mark/Bark_Ability_Mark.barkability` (Performing Ability).
2. From **Bark Entry**, chain through the True outputs:
   - **Ability Condition**: Phase `Performed`, Ability `Mark_Ability_Attack_Vault` (`Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`).
   - **Performer Condition**: `Mark`.
   - **Level Condition**: Level Name `The Ridge`.
   - Optional: **Faction Unit Count Condition**, enemy side, At Least 1 alive.
3. Text: Mark "Send one my way." Optionally follow with the draft's G9-6 to G9-8: Mark "Linda. Shoot at me." / Linda "Gladly." / Mark "From a distance."
4. Turn on play only once, then save.
5. Test: Vault in the Ridge.

The better gates need new bark condition nodes: "Linda has ≥ 1 arrow" would read `LindaQuiver`, and the line check would compare Mark's and Linda's rows or columns with an enemy between them. That is feature work in the bark system, for later.

## Risks and loose ends

- **Re-saving a level that places John or Lucy adds instance noise.** Running Wire Search: River again wrote about 60 lines of `animationEvents` size and frame overrides on the John and Lucy instances into `GB_s1-river.prefab`. It's the same noise `GB_m3-john` and `GB_m1-linda` show. The River needed no change for the beat, so I put its prefab back to the committed version with `git show HEAD:… > file`; that is read-only git plus a file write. `GB_s2-ridge` (Linda and Mark) has none of it. The cause looks like the John and Lucy prefabs' ability `animationEvents` re-serializing differently from what the instances stored. It is worth a look outside C4.
- **Unity logged "Unsupported type Vector2f" twice** during the wiring run, attributed to `SearchWiring.River.cs` around `SaveAssets`. It's an engine-side serialization message; no asset came out wrong (diffs checked, tests pass).
- `PlayedSequencesTracker` keys on the sequence's asset name. Don't rename `Search_FirstSleepingEnemy_SequentialSequence`, or saves will show the panel again.

## Play check for THJ

1. **Ridge** from the world map: the "Mark's Family Role" panel → "They've seen us." / "Good. I hate waiting." → (first pair mission on this save) the "Asleep" panel → the nearest sleeper's sight tiles show for about 1.5 s → input back.
2. The rush pack (1,5 / 2,4 / 3,5) is awake from the start. The gauntlet Claws (7,1 / 8,1) show the sleeping marker.
3. Turn 1, Linda shoots 2,4. Enemy turn: a Claw hits Linda within 2 of Mark → the Counter prompt.
4. **Gauntlet:** Linda to 5,1, Mark to 6,1, Vault to 9,1 over both Claws. Linda shoots east → press the catch prompt → the arrow comes back and both Claws die. Linda's quiver count is unchanged, and no AP comes back.
5. Miss the catch once (restart): the arrow lands under 8,1.
6. Kill all: close-up on 13,1, the five lines, then the rewards Gold 20, Steel 2, XP 30.
7. **River** on the same save after the Ridge: no "Asleep" panel. On a fresh save, River first: the panel plus the sight beat after the River's intro.
8. **Skill tree:** Mark's "Catch & Return" node shows as owned and can't be bought.
9. During the beat, hold Shift over another enemy: check the two previews don't leave tiles stuck.
