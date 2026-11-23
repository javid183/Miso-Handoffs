# Onboarding demo 3.1 and 3.2: build M1 (the Ridge) and M2 (the River)

Size: L    Tier: 2 (built from approved paper levels; Tier 3 points are marked and stop the chunk)    Assigned to: `miso-implementer` (opus), one chunk at a time
Branch: `thj/onboarding-demo` (D-604)
Status: approved paper levels (D-631); tech plan by the coordinator 2026-11-23; chunk 3.1a in progress

## Why

THJ approved the M1 and M2 paper levels (D-631). The spec is `plans/2026-11-22-onboarding-d3-paper-levels.md`, section 3:
- M1: block `m1-ridge`, with its stage list and sequence list.
- M2: block `m2-river`, the same.
- Section 5 holds the to-checks.

The item text is in `design/demo-tweaks-snapshot.md` section 6 (M1-01 to M1-03, M2-01 to M2-06) and X-26. Parent plan: `plans/2026-11-22-onboarding-demo.md`, Phase 3.

## Goal

The Ridge and the River missions each play the new paper level from new prefabs `GB_m1-ridge` and `GB_m2-river`. The old prefabs are kept under new names. Mark starts with Command instead of Vault.

## Decisions this rests on

- D-621 (THJ): a big change gets a new prefab and the old one is renamed. Never overwrite the old level.
- D-605, D-606, D-619, D-620, D-632, D-633: M1's Masher beat, side path, ledge, setup (camera, two lines, preview), start tiles, and Mark's Move = Command.
- D-607, D-623, D-630: M2's Pile is a clue only. The worm stays as built, splitting on its first damage; T-16 checks the code matches.
- D-614: no Cleanse in M1 or M2.
- D-611 / H-01: enemy introduction cards play last. No `EnablePlayerInputSequence` or `ShowHUDSequence` at the end of the start lists.
- Placeholder text: the paper level's lines, tagged `[PLACEHOLDER]`. `miso-narrative` replaces them later.

## Facts from the code (Explore, 2026-11-23; verify before relying)

- **Grid builder:**
  - `Tools/Levels/Build Level From Grid...` writes `Content/Levels/Greybox/GB_{block id}.prefab`.
  - It refuses to overwrite unless asked, and a rebuild keeps the GUID.
  - It reads the `level` lines: `name`, `tier`, `alert`, `hidden`, `deploy`.
  - It has no HP-factor key, so set factors in the wiring.
  - It places the 2×2 Masher from four `O` cells (T-3, tested), and maps `w` to the worm.
- **`SearchWiring.Ridge.cs` and `.River.cs`:**
  - Hard-coded `LevelPath` / `MissionPath` consts (`MS2 - The Ridge.asset`, `MS1 - The River.asset`).
  - They write the start and end sequences, the clue props at fixed tiles, the first-sleeper handle, the mission graph (one node, `payload = level`) and the drops.
  - Ridge also forces enemies first and clears HP overrides. Both contradict the new M1.
  - Their tests (`SearchRidgeTests`, `SearchRiverTests`) assert the old layouts.
  - `WiringSeed` never rewrites an existing step list: give new levels **new sequence asset paths**.
- **Missions:** each points at its level only through the graph node `payload`. Renaming the old prefab keeps its GUID, so each mission must be re-pointed. A mission-wiring step does that.
- **Building blocks:**
  - `MoveUnitSequence` (move a unit by nickname or tile; no range limit; cancels if blocked).
  - `RevealUnitsSequence` (`HiddenLevelUnits.Reveal(groupId)`).
  - `CastAbilitySequence` (needs a Cell-target `Targeted` preset; no AP spent).
  - Turn reset: `LSBExecutionSequence` → `CurrentPhaseManipulationAction` `Mode.Reset` → `RestartTurn()`, which refills AP. The pattern is in `HearthMemoryWiring.Lucy.cs`.
  - `GuidedAbilityHint` (turn window or when unlocked; no unit-on-tile condition, T-5).
  - `CameraSequence` (via `SearchWiringShared.BuildCamera`).
- **Mark (`Unit_Mark.prefab`):**
  - Vault is at `abilities[2]` and Command at `abilities[3]`.
  - Vault is also his `superTimeAbility`.
  - Command is the skill-tree node `nodes[0]`.
  - How the tree gates the action bar is not traced.
- **Masher:** the counter preview (`MasherGoblinFactionRoleHandler.Preview.cs`) only shows **while the player is aiming an ability** and hovers the Masher, not on a plain hover. The setup lines must say so, e.g. "aim at it and look".

## Chunks

### 3.1a: Mark's starting kit, Command instead of Vault (X-26, D-633)

- **Goal:** across the demo, Mark starts with Command available and Vault not in his starting kit. In the paper level's words, his skill tree "unlocks Command instead of Vault".
- **Step 1, investigate:**
  - how a skill-tree node gates an ability on the bar (Command's node `unlockLevel` 0, `Unit_Mark.prefab:545`);
  - where Vault's availability comes from;
  - what uses Vault as `superTimeAbility` (FTP Super Time);
  - which levels and tests depend on Mark having Vault: the Hearth memory 4, the Trail, M4, `M4SquadPickTests`, the Cyclone and Command tests.
- **Then the smallest data change** that gives this kit: Command open, Vault behind the tree.
- **Stop and report before changing anything if any of these holds:**
  - It needs code in a core system.
  - It changes save data, or what an existing save owns.
  - It changes which ability Mark's Super Time uses.
  - It breaks Memory 4's scripted beats.

  Each of these is Tier 3. THJ decides what Super Time does without Vault.
- **Accept when:**
  - A new save reaches M1 with Command on Mark's bar and no Vault.
  - Memory 4 and the levels after M1 still work as designed. List what changed for each.
  - The covering tests pass, updated only where they asserted the old kit.
- **Commit:** its own. Review: its own (it changes a unit prefab and possibly the skill tree). Model: opus.

### 3.1a-2: Vault buyable in the tree (D-637), after 3.1b

- **Goal:** Mark's skill tree node that unlocked Command (`nodes[0]`) now unlocks Vault, at the cost Command had (1 SP). Command stays open from the start (3.1a).
- **Data:** Vault's preset gets `upgradable: 1` (a new save key, approved by THJ in D-637) and the `unlockResourceRequirements` Command had; Command's are cleared. The node's title, text and icon become Vault's (text `[PLACEHOLDER]` if no Vault line exists).
- **Graph:** children of `nodes[0]` that are about Command ("Command applies Weak", `nodes[2]`) must not end up gated behind Vault; the "Stunning Vault" node (`nodes[4]`) should sit behind the Vault node. If that needs more than re-pointing node fields, stop and report the options.
- **Check:** the Vault run upgrades (`RU_MarkVaultRange`, `RU_MarkVaultStun`) appear once Vault is bought; `SkillTreeSmokeTest` updated to the new kit if cheap.
- **Tests:** extend `MarkStartingKitTests`. Commit: its own, after 3.1a's. Review: its own (save key). Model: opus.

### 3.1b: M1, the Ridge (new `GB_m1-ridge`)

1. **Rename the old level.** `GB_s2-ridge.prefab` becomes `GB_s2-ridge_v1.prefab` through `AssetDatabase.MoveAsset`, which keeps the GUID.
   - `SearchWiring.Ridge.cs` and `SearchRidgeTests` follow the rename: they keep wiring and testing the old level, **minus the mission step**. The old tool must never re-point the mission again.
   - Remove its `WireMission` call, or guard it off. Drop the mission and roster asserts.
   - The old level stays playable from its prefab; nothing references it in the game.
2. **Build `GB_m1-ridge`** from block `m1-ridge` with the grid builder (new file).
3. **New wiring tool.** `MissionWiring.M1Ridge.cs`, or a name that fits the folder's pattern, with its own menu item and new sequence asset paths (a new folder, e.g. `Resources/Sequences/M1Ridge/`). It writes, as the paper level says:
   - **Turn order:** family first. No enemies-first override.
   - **Per-unit HP factors:** as listed.
   - **Start sequence:**
     - the intro;
     - the camera from Linda along the ledge to Mark and back, with the two placeholder lines;
     - the Role cue lines (M1-03, Watch and Counter);
     - nothing that gives input or HUD at the end (H-01).
   - **The Masher stage:** the setup is a camera on the Masher, two placeholder lines (one says to aim at it to see its slam) and the existing counter preview (D-620). The hidden `back` pack is revealed on the stage's turn 2 (`RevealUnitsSequence`).
   - **Ability locks:** Cleanse hidden for both. Vault hidden if 3.1a hasn't already removed it.
   - **The clue:** props and the end sequence (camera close-up, the clue dialogue, outro) at the paper level's clue tile (12,0). Not the old 13,1.
   - **Mission (`MS2 - The Ridge.asset`):**
     - re-point the graph to `GB_m1-ridge`;
     - keep today's drops unless the paper level says otherwise;
     - keep the mission's GUID and name, because the station unlocks, Home visits and the opening setup reference the mission.
   - **No first-sleeper or "Asleep" panel:** M1 is `alert all`.
   - Stages and triggers: follow the pattern of the Trail's arrivals (`SearchWiring.Trail.Arrivals.cs`) for "on turn N of a stage".
4. **To-checks to answer in the report,** by reading code or with a short Play session:
   - T-17: does a hit on Mark count for his Counter?
   - T-4: what does Encore do with arrows locked under a living Masher?
   - T-1: arrow falloff, for M1's first hits only.

   Fallbacks are in the paper level. T-17's fallback is Mark starting on 3,2: apply it only if T-17 fails, and say so.
5. **Tests:** a new `M1RidgeTests` checks the layout read from the prefab (units on the paper tiles, the Masher anchor 5,0), the sequence order, the locks, the mission payload and the old tool no longer touching the mission. Plus the covering fixtures.

Commit: its own: the rename plus the old tool trimmed, then the new level, tool and tests. Two commits if they separate cleanly. Review: with the feature, after 3.2. Model: opus.

### 3.2: M2, the River (new `GB_m2-river`)

1. **Rename the old level** the same way: `GB_s1-river.prefab` becomes `GB_s1-river_v1.prefab`. Trim `SearchWiring.River.cs` and its tests the same way.
2. **Build `GB_m2-river`** from block `m2-river`.
3. **New wiring tool** with new sequence asset paths. It writes:
   - **Start sequence:** the call line, the camera, the Role cue lines (M2-06), no input or HUD at the end.
   - **The clearing stage** (Lucy's follow-up, John's guard).
   - **The rush (M2-03):**
     1. `MoveUnitSequence` takes John to 9,3 (T-13: path and blockers from wherever he stands).
     2. `RevealUnitsSequence` reveals group `ring` (3 Claws and 1 worm on his diagonals).
     3. `CastAbilitySequence` casts Shield Up on John. Check the preset fits the step's Cell-target rule. If it doesn't, stop and report the options (Tier 2: a variant step, not core).
     4. The turn resets (the Lucy memory pattern).
     5. The player casts Lucy's embers on John. The fallback is a `GuidedAbilityHint` pulse on Lucy's ember for that turn window, plus the aim preview.
   - **Shield Flare dialogue:** placeholders (M2-02).
   - **Ending (M2-04):** the Pile as a **clue only**. Pile props in the zone the paper level marks (15,2 to 16,4, props with no cells), then the camera, the clue dialogue and the outro. **Not** the sisters' tally or "Still counting?". That stays with the Trail (D-607), so don't move or change the Trail's tally wiring.
   - **Mission (`MS1 - The River.asset`):** re-point to `GB_m2-river`. Keep its GUID, name and drops.
4. **To-checks:**
   - T-16: does a worm split on its first damage? If the code splits only on death, report it with the smallest fix. Don't fix it: it touches every worm.
   - T-6: which embers flare off John's Shield Up.
   - T-13: the rush path.
5. **Tests:** a new `M2RiverTests`, with the same shape as M1's. Then the full EditMode suite (end of feature).

Commit: its own, split like 3.1b. Review: one `miso-reviewer` pass over 3.1b and 3.2 together (3.1a is reviewed alone). Model: opus.

## Acceptance criteria (feature)

- [ ] New saves play M1 on `GB_m1-ridge` and M2 on `GB_m2-river`, from the world map after the Hearth. Each matches its paper block: tiles, units, hidden groups, turn order, HP factors.
- [ ] The old prefabs exist as `GB_s2-ridge_v1` and `GB_s1-river_v1` with their GUIDs. Nothing in the game points at them, and the old tools no longer touch the missions.
- [ ] M1's beats run in the paper order: the opening pan, the pack fight with Watch and Counter firing, the Masher setup, Catch & Return on the Masher, the `back` pack on turn 2, the clue.
- [ ] M2's beats run in the paper order: the clearing, John's rush, the ring, Shield Up, the turn reset, the player's Shield Flare, the Pile clue.
- [ ] Mark has Command and no Vault in M1. Cleanse is hidden in both levels.
- [ ] Start sequences hand over input only after the enemy cards (H-01).
- [ ] Placeholders are tagged. Their list is in the reports for `miso-narrative`.
- [ ] Covering tests per chunk. The full EditMode suite is green at the end of 3.2.
- [ ] A win played through on each mission: THJ's play check, or the verifier with THJ's time. This covers the mission drops, gate 6.

## Risks

- **New statics:** none expected. If one is needed, add a `PlayModeStaticReset` hook.
- **`WiringSeed` and step lists:** new asset paths only. Never point a new tool at the old sequence assets.
- **Missions referenced by GUID elsewhere:** the opening setup, the stations (D-618), Home visits. Keep the mission assets, and only re-point their payloads.
- **Mark's kit change is game-wide (3.1a):** Memory 4, the Trail, M4 and the Cyclone or Command tests may assume Vault. The chunk lists them and stops on a Tier 3 point.
- **The Pile:** the Trail's Pile and tally stay untouched (D-607). M2 only adds props and a clue.
- **Shared scenes:** none. Levels are prefabs.
- **AI content:** none changed. Don't run `AIRegressionTest`; new levels don't affect its baseline.
- **THJ's uncommitted files, and the Phase 1 changes still uncommitted:** leave them alone and keep commits separable. List any overlap.

## Gates

- Compile with a clean console.
- Covering tests per chunk; the full suite at the end of 3.2.
- Reviews: 3.1a alone; 3.1b and 3.2 together.
- Grids: drawn already (gate 7). Redraw if a block changes.
- THJ's play check per mission before its commits, including a win.
- **Docs, by their owners after approval:**
  - GDD `missions-structure.md` (the M1 and M2 rows), `enemies.md` (the Masher's first appearance; EN-4 if T-16 changes the text) and `mark.md` (Command vs Vault): game designer.
  - `tech/onboarding-merge.md`: coordinator.
  - The D3 plan's "superseded" notes: designer.
