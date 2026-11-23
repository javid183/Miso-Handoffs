# Report: Vault buyable in Mark's skill tree

Plan: plans/2026-11-23-onboarding-m1-m2-build-tech.md (chunk 3.1a-2)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: blocked (stopped before any change: as specified, a bought Vault would not stick, and every fix touches core code or Mark's Super Time)

## What changed

Nothing. No file under `miso/` was edited. I read the code and the assets and stopped at the save step.

## The blocker: Vault's save key is registered twice

D-637 makes Vault `upgradable: 1`, so its runtime ability registers the save key `Mark-Mark_Ability_Attack_Vault-sd`. The post-merge save check is right that the key appears by itself. But Mark has **two** runtime copies of the Vault preset, and both register that same key:

1. The one on his bar, in `AbilityOrchestrator.abilities`.
2. The Super Time copy, `MarkFactionRoleHandler.superTimeAbility` (`Unit_Mark.prefab:2824-2825`, preset Vault).

How the code handles that:

- `AbilityOrchestrator.InitializePartially` / `Initialize` (`Core/Systems/AbilitySystem/Abilities/Runtime/AbilityOrchestrator.cs:47-50, 56-64`) first initializes the bar abilities, then the role handler. `FactionRoleHandlerBase.InitializePartially` / `Initialize` (`FactionRoleHandlerBase.cs:100, 109`) then initializes `superTimeAbility`.
- `RuntimeAbility.InitializePartially` / `Initialize` (`RuntimeAbility.cs:213-215, 228-230`) reset the level to the preset default and call `SaveLoadManager.Register(key, this)` when the preset is `upgradable`.
- `SaveLoadManager.Register` (`Core/Managers/SaveLoadManager.cs:64-79`) keeps one entry per key. A second registration **replaces** the entry's `Save` closure. So the Super Time copy, registered last, is the one that gets saved.
- The tree buys the bar copy: `SkillTree.TryGetRuntimeAbility` uses `GetAbilityFromAllTypesByPreset` (`AbilityOrchestrator.cs:137-139`), which never looks at `superTimeAbility`.

What happens in Home: Mark buys Vault, and the bar copy goes from -1 to 0. The Super Time copy stays at -1. The next save writes `{upgradeLevel: -1}` (`RuntimeAbility.CaptureState`, `:569`). The next `InitializePartially` reloads -1 into the bar copy. `AbilityUpgradePanelUI.cs:126, 186` and `FactionTracker.cs:58` call it on every refresh and before each buy. Result: the SP is spent and Vault drops back to locked. At the latest, it's locked again in the next fight.

Nobody has hit this before because no Super Time preset is upgradable today: John's Taunt, Linda's Explosive Arrow, Lucy's Cyclone and Mark's Vault are all `upgradable: 0`. Vault would be the first.

I didn't confirm it with a run: Unity is closed and a throwaway test would have added files. The chain above is all plain code, so a short EditMode repro is cheap if THJ wants one before choosing.

## Options (Tier 3: core code or Mark's Super Time)

1. **Core fix (recommended): the Super Time copy doesn't register for saving.** It never owns progress: the tree, the run upgrades and the bar all work on the orchestrator's copy. This needs a small additive change to `RuntimeAbility` (for example an optional "don't register for saving" argument on `Initialize` / `InitializePartially`) and to `FactionRoleHandlerBase` (pass it for `superTimeAbility`). Both are core systems. It touches John, Linda and Lucy too, though their presets aren't upgradable, so nothing changes for them today. It also prevents the same trap if any other Super Time preset becomes upgradable later. Its own commit and review, plus the full suite.
2. **Data: give Super Time its own non-upgradable Vault preset.** Copy `Mark_Ability_Attack_Vault.asset` with its effect sub-assets to a Super Time preset, set it to `upgradable: 0`, and point `superTimeAbility` at it. There's no code change, but it changes which preset Mark's Super Time uses (a 3.1a stop condition). Copying a preset with sub-assets needs an editor script (`AssetDatabase.CopyAsset`), so it can't be done while Unity is closed. It also leaves a second Vault to keep in sync, and `MarkStartingKitTests.SuperTimeStillPointsAtVault` changes.
3. **Data: clear Mark's Super Time preset.** Mark's Super Time does nothing today: the base `ActivateSuperTime` is a no-op, and target selection mode is None (3.1a report). But `PlayerController.cs:1761` calls `SuperTimeAbility.HandleTargetSelectionAnim` with no preset check, and `FactionRoleHandlerPartialInitTests` expects Mark's handler to carry an event-based animated ability. That's a risk of a null reference or a failing test. Not recommended.
4. **Core alternative: initialize the role handler before the bar abilities** in `AbilityOrchestrator`, so the bar copy registers last. It's smaller, but it only works by ordering, changes init order for every unit, and is still core. Not recommended.

**Recommendation:** option 1, then this chunk as planned on top. **Default if no answer:** the chunk stays parked. Vault stays fully locked (the 3.1a state), which is playable.

## Ready to apply once the save point is decided

I checked the rest of the chunk, and it holds as planned with field edits only:

- **Vault preset** (`Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`, LF, no BOM): `upgradable: 0` → `1`. `unlockResourceRequirements: []` → the 1 SP entry (`resourceRef.entityID: MainResource_SP`, `amount: 1`). `higherLevels` is empty, so `MaxUpgradeLevel` is 0, and the tree node goes from Upgradable (level -1) to Maxed (level 0) after one buy. `SkillTree.GetNextRequirements` shows the preset's `UnlockResourceRequirements` while the level is below 0.
- **Command preset:** `unlockResourceRequirements` → `[]`.
- **`Unit_Mark.prefab`, node 0 overrides:**
  - `abilityPreset` → Vault (`guid: 9d3564d11bff7c24c8dce9f7b157f998`, `fileID: 11400000`).
  - `title` → `Vault`.
  - `icon` → Vault's icon (`fileID: -4875225888458068294, guid: 1f0832a1e278af04f8d9a3fae4227efb`), following the Command node, which uses its preset's icon.
  - `upgradeDescription` → `Unlocks Vault.`
  - `description` → a line based on the preset's own: "Mark leaps to a nearby tile, fracturing the ground, slightly damaging and pushing enemies back." A Vault line exists, so no `[PLACEHOLDER]` tag. Conventions (D-348) also say tree panels show tags, so the line is listed here for the narrative pass instead.
  - Node mode stays Ability, with `unlockLevel` 0, `upgradeLevels` 0 and the same guid.
- **Graph:** today `edges[0]` runs from node 0 (Command) to node 2 (Sapping Order), and `edges[1]` from node 1 to node 5. Re-point `edges[0].inputNodeGuid` from `8e73a18d-…` (Sapping Order) to `6e2a6359-3131-4be7-af7a-2a4d8d8119c9` (Stunning Vault):
  - Sapping Order is then gated only by unit level 2, not by Vault.
  - Stunning Vault waits for Vault to be bought (`IsUnlockedByGraph`: the previous node's level must be at least its max, 0) and for unit level 3. This also closes the 3.1a loose end where Stunning Vault could be bought without Vault.
  - The Home tree UI lays nodes out by row and column, not edges (`AbilityTreePanelUI.cs:71, 111`), so the layout doesn't move.
- **Run upgrades:** `RU_MarkVaultRange` and `RU_MarkVaultStun` require Vault, and `RunUpgradeTracker.HasRequiredAbility` checks `Available` (upgrade level 0 or higher). So they're offered once the purchase sticks. That's why the save point blocks this check too.
- **Tests to update in `MarkStartingKitTests`:**
  - `VaultIsNotSaved` becomes "Vault is saved".
  - `TheFirstTreeNodeStillPointsAtCommand` becomes "the first node unlocks Vault for 1 SP".
  - New tests: Command has no unlock cost; the Stunning Vault node sits behind the Vault node; Sapping Order has no graph parent.
  - With option 1: a test that the Super Time copy doesn't register the key.
- **`SkillTreeSmokeTest`** (menu tool, not in the suite): its Mark checks would flip from Command to Vault, cheap to update in the same pass.

## Acceptance criteria

- [ ] Mark's first tree node unlocks Vault for 1 SP, and Command stays open: not built. The data is ready (above), but blocked on the save point.
- [ ] Children re-pointed (Sapping Order free of Vault, Stunning Vault behind Vault): not built. It's a single edge field change.
- [ ] Vault run upgrades appear once Vault is bought: not built. Depends on the purchase sticking.
- [ ] Tests extended: not built.

## Chunks

### Chunk 3.1a-2: Vault buyable in the tree

- Changed: none.
- Criteria met: none. I stopped at the save step (see "The blocker").
- Decisions and loose ends: see "Options" and "Ready to apply".

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- I stopped instead of building the data part without `upgradable`. Without it, a purchase is never saved at all, so a partial build would have looked done but wasn't.
- No tests run: nothing changed.

## Needs THJ

1. **How to keep a bought Vault saved.**
   - *What:* Mark's Super Time copy of Vault registers the same save key as the Vault on his bar and overwrites it, so a bought Vault reverts to locked.
   - *Why it matters:* D-637 can't work as data alone. The SP is spent and Vault doesn't stay.
   - *Options:* (1) a small core fix so the Super Time copy doesn't register for saving; (2) a separate non-upgradable Super Time Vault preset (editor script, changes Mark's Super Time reference); (3) clear Mark's Super Time preset; (4) reorder init in `AbilityOrchestrator`.
   - *Recommendation:* (1), as its own core commit, then the chunk on top.
   - *Default if no answer:* parked, and Vault stays locked as in 3.1a.

## Docs to update

- `reports/merge-origin-main-2026-11-23-save-read.md` / plan 3.1a-2 "Data": `upgradable: 1` also needs the duplicate-key fix (above).
- `tech/core-systems.md` (if option 1): note on Family Roles / Ability runtime that the Super Time copy doesn't save.

## Risks and loose ends

- The same trap applies to any future change that makes a Super Time preset upgradable (John's Taunt, Linda's Explosive Arrow, Lucy's Cyclone). Option 1 covers it.
- The plan's "`[PLACEHOLDER]` if no Vault line" conflicts with conventions D-348 (no tags in tree text). It's moot here because a Vault line exists.

## Proposed commits

None (nothing changed). Once option 1 is chosen, the likely split is:

1. `fix(abilities): Super Time copies don't overwrite the ability's save entry` (core)
2. `feat(mark): Vault is bought in Mark's skill tree in place of Command` (plain data + tests)

## Other branches

None.

## How to see it

Nothing to see yet. To see the blocker once Vault is set to `upgradable: 1` without a fix:

1. Clear the save.
2. In Home, give Mark 1 SP and buy the Vault node.
3. Leave and reopen the skill tree, or start a fight: Vault is locked again and the SP is gone.
