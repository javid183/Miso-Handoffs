# Report: C3a, the Hearth memory levels (hidden units, levels, Hearth wiring)

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (C3a steps 2 to 4; step 1's check is `reports/onboarding-c3a-reveal-check.md`, option A approved as D-346)

Paths are under `miso/Assets/_Project/` unless they start with `claude-handoff/`. All new and edited files are LF with no BOM, matching the folders they sit in. No core-system file was changed.

## What changed

**Hidden units (runtime, non-core, `Features/Onboarding/`)**
- `HiddenLevelUnits.cs` (new): a MonoBehaviour for the level root. It holds groups `{ id, GUnit[] units }` (default id `hidden`) and a `Reveal(groupId)` method that runs the spawn steps on each unit that is still hidden: `SetActive(true)` → `Initialize(true)` → `PlugEntity` on the parent cell (which falls back to the nearest free cell) → `AddFactionControllerMidWay` if the faction has no controller → `RegisterUnit`, which raises `unitBorn`. Under `LevelAlertSettings.AllEnemiesStartAlert` the alert tracker registers the unit as alert. The method refuses before the factions are prepared (`CurrentFactionControllerOrNull == null`) and warns on an unknown group or a unit with no cell. `Awake` hides any listed unit that the prefab left active, with a warning. The class holds no statics. Its pure helpers are `FindGroup` and `StillHidden`.
- `RevealUnitsSequence.cs` (new): a `Sequence` asset (`Game/Sequence/RevealUnitsSequence`) with a group id and a wait after the reveal (0.6 s by default, for the spawn animation). It finds the level's `HiddenLevelUnits` and reveals the group.

**Grid tool (editor, `Core/Levels/Editor/GridToLevel/`)**
- `GridBlock.cs`: `GridLevelSettings.Hidden` (a list of `GridHiddenGroup { Id, Tiles, Line }`) and `FindHiddenAt`.
- `GridBlockParser.cs`: reads `level hidden [group] x,y …`. The optional first word names the group, and repeated lines add tiles to it (exempt from the "given twice" warning).
  - Warnings: a tile with no unit, a tile given twice.
  - Errors: no tiles, a token that isn't X,Y, a tile off the floor.
  - New public helpers: `PlacementCovering` (big units cover several tiles) and `HiddenDefaultGroup`.
- `GridToLevelBuilder.Hidden.cs` (new partial): `ApplyHidden` sets each hidden placement inactive and lists it on a `HiddenLevelUnits` added to the root. Levels without the line get no component. `DescribeHidden` gives the preview text.
- `GridToLevelBuilder.cs`: one line in `Build` calls `ApplyHidden` after the XP step.
- `GridToLevelWindow.cs`: a "Hidden units" preview row (group, tile, unit character, and "(no unit)" when a tile is empty).

**Round-trip script**
- `claude-handoff/tools/level_to_grid.py` (in the private repo, asked for by the coordinator): reads the level's `HiddenLevelUnits` (found by the script's GUID, taken from its `.meta`) and the instances' `m_IsActive`. It writes `level hidden [group] x,y …` after the notes, with the offset applied. Problems go in the summary under "Hidden units:": a listed unit that is active, an inactive unit in no group, or a listed reference that isn't a placed unit. Docstring updated. Checked on the old `GB_m1-linda` before the rebuild: same output as before.

**Levels (`Content/Levels/Greybox/`)**
- `GB_m1-linda.prefab`: rebuilt (it had no hand edits), then per-instance HP set.
- `GB_m2-lucy.prefab`, `GB_m3-john.prefab`, `GB_m4-mark.prefab` (new, with `.meta`): built from the designer's blocks in `plans/onboarding/2026-10-26-onboarding-levels.md`. The hand edits are listed below.

**Hearth wiring**
- `Content/Levels/M0 - The Hearth.asset`: the three node payloads now point at m1, m2 and m3. A fourth node (m4, new GUID, position 941,192) is added, plus an edge from m3 to m4. `completionXPReward` stays 0. The old M1 level prefabs are untouched; they are only unlinked.

**Tests**
- `Core/Levels/Editor/GridToLevel/GridToLevelHiddenTests.cs` (new, 9 tests): parsing (default group, named groups that add up, the no-unit warning, the off-floor error, a bad token or no tiles, a repeated tile), the preview text, and two builds: hidden units inactive and listed while the others stay active, and no component without the line.
- `Features/Onboarding/Editor/HiddenLevelUnitsTests.cs` (new, 3 tests): `FindGroup` and `StillHidden` (empty slots, repeats, units already in play, list order).
- `Features/Onboarding/Editor/HearthMemoryLevelsTests.cs` (new, 3 tests): the XP resource id resolves; `LevelXpChecker.CheckMission(The Hearth)` is empty; the graph is the four memory levels in order, with nothing else left in it.

## Hand edits after the build (the prefab is now the master for these)

Done through editor scripts run from the Unity bridge (the same calls a `Tools/` script would make). A rebuild from the block loses them, so redo them after any rebuild.

1. **Per-instance HP** (m1, m2, m4). This follows the existing per-instance pattern: Level1 levels override the damage factor the same way, so I used it for HP. The override is on the unit's own `Stat_HP` factor (`statAttributes.attributeEntries[0].upgradeLevels[0].factor`). The enemy prefab is unchanged.
   - A Dark Claw's max HP is 16 (prefab) × 0.6 (Enemy faction, Tutorial row) × the unit factor, and Health snaps to whole numbers (`changeInInteger`, `RuntimeAAttribute.MaxValue`). Factor = target ÷ 9.6, rounded to 4 places.

   | Level | Tile | HP | Factor |
   | --- | --- | --- | --- |
   | m1 | 2,6 (A) | 14 | 1.4583 |
   | m1 | 2,7 (B) | 6 | 0.625 |
   | m1 | 2,9 (C) | 2 | 0.2083 |
   | m2 | 3,3 and 4,2 | 6 | 0.625 |
   | m4 | prism 1,4 / 5,4 / 3,6 | 6 | 0.625 |
   | m4 | gallery 12,2 / 10,2 | 8 | 0.8333 |
   | m4 | hall 8,8 / 9,7 | 8 | 0.8333 |

   Hidden Claws and m3 keep the Tutorial default (10).
2. **Mother and cub** (m4). Both placeholders are scenery under a new `Memory Scenery` child of the level root, not under a grid cell. Neither prefab has a `GUnit` or grid entity: Wolf has an Animator, 2 SpriteRenderers and a BoxCollider2D; Ryker has an Animator and a SpriteRenderer. So neither is in turn order, the objectives, the grid or the XP check.
   - `Mother (placeholder)`: `Features/Home - Imported/Entities/Characters/Wolf/Wolf.prefab` on tile 8,10, scaled 0.5 (its sprite is about 2 × 2 tiles at full size).
     - Its BoxCollider2D is turned off on the instance.
     - Its two SpriteRenderers had a missing material (GUID `08b186db…` resolves to nothing), so they get `Sprite-Lit-Default`, the material Ryker uses.
     - Its sort order 600 draws it above the units.
   - `Cub (placeholder)`: `Features/NPCs/Ryker/Ryker.prefab` on tile 7,10, no changes.

## Round-trip results

`level_to_grid.py` reads each prefab back. A scratch comparer, `C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\9fe122c2-8960-46cb-b7ce-373dc3e29bd0\scratchpad\roundtrip.py`, checks the paper block against what it reads, in block coordinates: floor tiles, units by character and tile, and hidden groups. I ran it after the build and again after the hand edits:

| Level | Floor tiles | Units | Hidden groups | Result |
| --- | --- | --- | --- | --- |
| GB_m1-linda | 18 same | 4 same | none | OK |
| GB_m2-lucy | 28 same | 6 same | `hidden`: 9,3 10,2 9,1 | OK |
| GB_m3-john | 42 same | 7 same | none | OK |
| GB_m4-mark | 62 same | 13 same | `hidden`: 9,9 9,8 | OK |

What `level_to_grid.py` prints beyond the tiles:
- m4 prints `note 7,10 Ryker` and lists Ryker under "placed by position, not under a cell". That is expected: the cub is scenery, and the paper block marks 7,10 as `R`. Wolf is listed under "Not drawn".
- The only build warning was m4's `'R' has no prefab yet` (7,10 builds as floor, as the paper says).
- `level xp none` reported no XP left in any level.

## Tests

- New: 15 (12 run on their own first, all passing).
- Full EditMode suite with the editor open, through the Test Runner bridge: **1171 run, 1170 passed, 1 failed**. The failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (39 failures, `graphs.count: expected 28, found 29`, the same signature as before). It was not re-baselined.
- Coverage by acceptance criterion (C3a):
  - Four levels built with the four `level` lines, round trip exact: covered by the round-trip run above; tier, alert, XP and FP come from the existing tool tests and these builds.
  - Hearth graph in order, `completionXPReward` 0: `HearthMemoryLevelsTests.TheHearthPlaysTheFourMemoryLevelsInOrder`.
  - Cue enemies placed and out of play until revealed: the build side (inactive and listed) is `GridToLevelHiddenTests.Build_HiddenUnitsAreInactiveAndListed` plus the round trip. **The runtime side needs the verifier's play check:** not targetable, not in turn order, no AI turn, tile free, not counted, then in alert after the reveal.
  - XP test (CheckMission empty, XP id resolves): `HearthMemoryLevelsTests`.
  - Per-instance HP: set and logged above; the in-play bar value needs the play check.

## Not verified

- **No Play session was run.** Nothing about the reveal is checked at runtime: turn order, AI, the alert state on arrival, objective counts, the spawn animation, the nearest-cell fallback, and the enemy introduction pop.
- No `RevealUnitsSequence` asset exists yet, and nothing calls `Reveal`. That belongs to C3b, so the hidden Claws never appear in this chunk's levels.
- The HP values on screen (the snap to whole numbers is read from code, not seen).
- How the mother and cub look in the level. The Wolf placeholder may still need scale or sorting work. The fixes I made to it, listed above, are small and its own prefab is unchanged.
- The m1 enemy turn order (A, B, C), a "To check" row in the paper plan. `PrepareFactions` orders by `TurnOrder`, and units with equal values follow the `FindObjectsByType` order, which Unity does not define. Not checked.

## Save reset

No.

## Decisions I made

- `level hidden` takes an optional first word as the group name (default `hidden`), so one level can reveal two groups at different cues. The paper lines (no name) parse unchanged.
- Per-instance HP goes through the unit's `Stat_HP` factor, the pattern Level1's damage overrides already use. The factor is tied to the Tutorial tier row (0.6): if that row changes, these HP values move with it.
- The mother and cub are scenery under `Memory Scenery`, not grid entities, so they stay out of every combat list. The Wolf's collider is off and its missing material is replaced on the instance only.
- The new Hearth node copies the third node's fields (`options: 1`, entity type), as Unity does when an array grows; the diff is checked.

## Needs THJ

None. One art call stays open, as before: the placeholder mother (Wolf) and cub (Ryker).

## Docs to update

- `tech/level-tools.md`:
  - add the `level hidden [group] x,y …` line to the list;
  - Known limits: "no per-unit HP" still holds for the tool (HP is a hand edit, logged here);
  - add m2, m3 and m4 to "Built so far";
  - `level_to_grid.py` now writes `level hidden`.
- `tech/combat-architecture.md`: `HiddenLevelUnits` and `RevealUnitsSequence` (non-core, `Features/Onboarding/`), with the reveal steps and the "refused before factions are prepared" rule.
- Structure tech § C3 status, `status.md`, `build-log.md` (coordinator).

## Risks and loose ends

- **Objectives before the reveal (C3b).** The levels keep the template's objectives ("defeat every enemy"), which count only units already in play. In m2, the two in-play Claws dying before the stage-1 reveal would win the level. C3b's stages must replace that objective, or the reveal must come first. The same holds in m4 for the seven in-play Claws and stage 1.
- **The Tempest Bloom grant (C3b).** `LevelStartRunUpgradeGrant` refuses an upgrade whose unit is not in the squad. The Hearth's roster has 3 fixed slots and the levels place their own heroes, so check that Linda and Lucy count as in the squad for m4.
- **AI thread.** A reveal goes through the same `unitBorn` → `AIFactionBrain.NotifyUnitsPresenceChange` path as a summon, including that method's existing Unity-object check (`unit && …`) on the worker thread. That code is unchanged and pre-existing.
- `LSBExecutionSequence` throws a null reference on an unknown call id (from the step 1 report). This matters only if a reveal is ever fired through an LSB.
- **Pre-existing modifications not touched:** the TMP fallback font, `AIFactionBrain.cs` / `AIUnitBrain.cs` (THJ's temporary diagnostic) and `ProjectSettings` were modified before this run. They are not part of any commit below.

## Proposed commits

1. `feat(levels): hidden level units that a sequence reveals, and a level hidden grid line` (plain; uses core APIs unchanged, so the reviewer should check that against `core-systems.md`):
   - `Features/Onboarding/HiddenLevelUnits.cs` + `.meta`
   - `Features/Onboarding/RevealUnitsSequence.cs` + `.meta`
   - `Features/Onboarding/Editor/HiddenLevelUnitsTests.cs` + `.meta`
   - `Core/Levels/Editor/GridToLevel/GridBlock.cs`
   - `Core/Levels/Editor/GridToLevel/GridBlockParser.cs`
   - `Core/Levels/Editor/GridToLevel/GridToLevelBuilder.cs`
   - `Core/Levels/Editor/GridToLevel/GridToLevelBuilder.Hidden.cs` + `.meta`
   - `Core/Levels/Editor/GridToLevel/GridToLevelWindow.cs`
   - `Core/Levels/Editor/GridToLevel/GridToLevelHiddenTests.cs` + `.meta`
2. `feat(onboarding): the four Hearth memory levels` (plain; needs commit 1 for the component):
   - `Content/Levels/Greybox/GB_m1-linda.prefab`
   - `Content/Levels/Greybox/GB_m2-lucy.prefab` + `.meta`
   - `Content/Levels/Greybox/GB_m3-john.prefab` + `.meta`
   - `Content/Levels/Greybox/GB_m4-mark.prefab` + `.meta`
3. `feat(onboarding): the Hearth plays the four memory levels, with no experience` (plain):
   - `Content/Levels/M0 - The Hearth.asset`
   - `Features/Onboarding/Editor/HearthMemoryLevelsTests.cs` + `.meta`

Private repo (coordinator): `claude-handoff/tools/level_to_grid.py` and this report.

## Other branches

none (all files are new on `thj/onboarding` or belong to it).

## How to see it

1. **Tools › Levels › Build Level From Grid…**, doc `claude-handoff/plans/onboarding/2026-10-26-onboarding-levels.md`, block `m2-lucy`. The "Hidden units" row reads `'hidden': 9,3 c 10,2 c 9,1 c`. Don't press Build: it would drop the HP edit.
2. Open `GB_m2-lucy` (Prefab Mode). The level root has a **Hidden Level Units** with one group of three Claws, and those three are inactive under cells 9,3 / 10,2 / 9,1.
3. In `GB_m4-mark`, `Memory Scenery` holds the mother on 8,10 and the cub on 7,10.
4. From the level toolbar, play `GB_m2-lucy`. Only two Claws are on the board, and 9,3, 10,2 and 9,1 are walkable. With nothing revealing them yet, killing the two wins the level (see the objectives risk above).
5. To try a reveal before C3b: create a `RevealUnitsSequence` asset (Create › Game › Sequence), group `hidden`, and play it from a level sequence trigger. The three Claws appear with the spawn animation, alert, and take the enemy turn.
6. New game: the Hearth runs m1 → m2 → m3 → m4, with no XP at the end.

## Fix round (review `reports/onboarding-c3a-review.md`, verdict FIX)

All five items are fixed. No core file was touched and no level was rebuilt. The four level prefabs and the Hearth asset are unchanged by this round: every hidden Claw's `GUnit` sits on its instance root, so the corrected builder would switch off the same objects.

- **Must fix: a revealed unit that died came back on a second reveal.** `HiddenLevelUnits` now keeps a per-instance `HashSet<GUnit> _revealed`, which starts empty because a restart reloads the level. It is filled before the unit is switched on, and the units to bring in are `PendingReveal(groupId)`: listed, inactive and not in `_revealed`. `MarkRevealed` is public for the test. New test `HiddenLevelUnitsTests.PendingReveal_ARevealedUnitSwitchedOffAgainIsNotRevealedTwice`: two Claws are loaded with `LoadPrefabContents`, so the open scene is untouched (checked: not dirty). One is revealed and switched off again, and only the other stays pending. An unknown group has nothing pending.
- **Should fix 1: the builder switched off the instance root.**
  - `GridToLevelBuilder.Hidden.cs`: `ValidateHidden`, called from `Validate`, refuses the build with an error when a hidden tile's prefab has no `GUnit` on its root.
  - `ApplyHidden` takes the root's `GUnit` and switches off `unit.gameObject`, the object the runtime switches back on.
  - No test: building it needs a palette prefab with the unit on a child, and none exists.
- **Should fix 2: no guard when a unit got no cell or no faction.** `RevealUnit` now:
  - resolves the faction from `FactionRef` before anything changes; with no faction it warns and the unit stays hidden;
  - after `PlugEntity`, warns if `CurrentCell` is null (no free cell) or the faction is still null, unplugs the unit if it was plugged, switches it off again and skips it. It stays in `_revealed`, because `Initialize` has already run and must not run twice.
  - Not testable outside Play mode; for the play check.
- **Should fix 3: the parser's group handling.** A group name must start with a letter (`^[A-Za-z][A-Za-z0-9_-]*$`), and any other first token is read as a tile. So `level hidden 2;0 2,0` now gives "hidden tile '2;0' is not X,Y" and still hides 2,0 in the default group. A group is created only when its first valid tile is added, so a line whose only tile is a repeat leaves no empty group.
  - New test `Parser_ABadFirstTokenIsReadAsATile`.
  - Updated `Parser_NoTilesOrABadTileIsAnError` (checks the message and that no group is made) and `Parser_ATileGivenTwiceIsAWarningAndLeavesNoEmptyGroup`.
- **Should fix 4:** `GridBlock.FindHiddenAt`, which nothing used, is removed.

Files changed this round: `Features/Onboarding/HiddenLevelUnits.cs`, `Features/Onboarding/Editor/HiddenLevelUnitsTests.cs`, `Core/Levels/Editor/GridToLevel/GridBlock.cs`, `GridBlockParser.cs`, `GridToLevelBuilder.cs` (one call to `ValidateHidden`), `GridToLevelBuilder.Hidden.cs`, `GridToLevelHiddenTests.cs`. All of them are in proposed commit 1; the commit split is unchanged.

Full EditMode suite, run again with the editor open: **1173 run, 1172 passed, 1 failed**. The failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, same signature, 39 failures; it was not re-baselined. There are two more tests than the first run.

Still not verified: the runtime reveal, including the new skip paths. They need the play check.
