# Report: Mark's starting kit, Command instead of Vault

Plan: plans/2026-11-23-onboarding-m1-m2-build-tech.md (chunk 3.1a)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (no stop condition hit; one point for THJ under "Needs THJ", about old dev saves)

## What changed

- `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Command/Mark_Ability_Attack_Command.asset`: `lockedByDefault` 1 → 0. Command is available from a new save's first fight.
- `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`: `lockedByDefault` 0 → 1. Vault is off Mark's bar.
- `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/MarkStartingKitTests.cs` (+ `.meta`): new, 6 EditMode tests that pin the kit.

`Unit_Mark.prefab` is **not** changed. Each asset edit is one line, LF and no BOM kept, both files clean before. No overlap with THJ's uncommitted files or the Phase 1 changes.

## Investigation (step 1)

- **How the tree gates the bar.** The action bar shows `AbilityOrchestrator.Abilities`, which keeps only `RuntimeAbility.Available` = `upgradeLevel >= 0` (or a run upgrade unlocks it) and the squad allows it. A runtime ability starts at `AbilityPreset.DefaultUpgradeLevel`: -1 when the preset is `lockedByDefault`, otherwise 0. Command's tree node `nodes[0]` (Ability mode, `upgradeLevels` 0, `unlockLevel` 0) "buys" Command by raising it from -1 to 0 for the preset's `unlockResourceRequirements` (1 SP). `unlockLevel` 0 only means "no unit level needed". So before this chunk: Command locked until 1 SP is spent; Vault open.
- **Where Vault's availability comes from.** Only from its preset: `lockedByDefault: 0`. No tree node, run upgrade or level unlocks it, and no level lock hides it (no level, sequence or hint references the Vault or Command GUIDs; only `Unit_Mark.prefab` and three run upgrades do).
- **Save.** An ability is saved only when its preset is `upgradable` (`RuntimeAbility.Initialize`, key `<Nickname>-<preset>-sd`). Command is upgradable and saved; Vault is **not** upgradable, so it's never in the save. THJ's current save holds `Mark-Mark_Ability_Attack_Command-sd` and no Vault key. The change adds no key and changes no stored value.
- **Super Time.** `superTimeAbility` on Mark's `MarkFactionRoleHandler` points at the Vault preset. Mark's handler doesn't override `ActivateSuperTime` (the base is a no-op), and his super-time entry has `targetSelectionAnimationMode: 0` (None), so the only use (`PlayerController.ActivateFactionSuperTime` → `HandleTargetSelectionAnim`) returns at once. The reference stays as it is, and nothing about Super Time changes. Locking the Vault preset makes that super-time copy start at -1, but nothing reads its `Available`.
- **Run upgrades.** `RU_MarkVaultRange` and `RU_MarkVaultStun` require Vault (`requiredAbility`). `RunUpgradeTracker.HasRequiredAbility` checks `ability.Available`, so they drop out of the offers by themselves. `RU_MarkCommandWeak` requires Command and can now be offered from the start.
- **Ability introductions.** Neither preset is `introducible`, so no new intro card plays.
- **AI regression baseline.** It lists each preset's evaluator and each unit's ability list, not lock flags. Neither changes, so it doesn't move. Not run, as instructed.
- **Levels and tests that could assume Vault:** see "Acceptance criteria" below. No code under `Features/Onboarding` names Vault or Command, and no EditMode test asserted the old kit, so no test needed updating.

None of the four stop conditions holds: no core code; no save shape or stored value changes; Super Time keeps its preset; memory 4's beats don't touch Vault or Command (below).

## Acceptance criteria

- [x] **A new save reaches M1 with Command on Mark's bar and no Vault.** Evidence: `DefaultUpgradeLevel` is 0 for Command and -1 for Vault (`MarkStartingKitTests.CommandIsOpenFromTheStart`, `VaultIsLockedFromTheStart`). The bar filters on that (`AbilityOrchestrator.Abilities`). A new save has no Command entry, so the default applies. The in-game look on the Ridge needs the verifier's or THJ's play check (see "How to see it").
- [x] **The levels where Mark appears still work as designed.** Levels and missions that place Mark: `GB_m4-mark` (Hearth memory 4), `GB_s2-ridge` / `MS2 - The Ridge`, the Trail (Mark as the free pick), M4 *The White Mothers* (free pick), plus older levels outside the demo path (`M3 - Mark Intro` levels, `GB_11-spread-pools`, `GB_33-deev-wave`, test levels). What changes in each:
  - **Memory 4 (`GB_m4-mark`):** Mark arrives with Primary, Walk and **Command** instead of Vault. The level's `LevelAbilityLock` locks only Duos, Cleanse and Linda's Explosive Arrow. Its hints are Linda's bow and the Mark–Lucy Duo, and its sequences cast Lucy's Cyclone and unlock the Duo. None names Vault or Command, so every scripted beat runs unchanged (`HearthMemoryMarkTests` pass). New player options: Command can move John off the den mouth, as John's own move already could, and can steer a living Cyclone through the existing Command–Cyclone hook. Neither is scripted against.
  - **The Ridge (`GB_s2-ridge`, today's M1):** Command on the bar, no Vault. No lock or hint names either, so the start, clue and end sequences are unchanged. Chunk 3.1b's "Vault hidden" lock is no longer needed.
  - **The Trail and M4 (free pick):** if Mark is picked, he has Command and no Vault. Their wiring has no ability locks or hints for Mark.
  - **Older campaign levels:** same kit swap. Paper chunks in `design/level-chunks.md` that list Vault as an answer (for example the "Vault + Fist Blitz" rows) lose that answer. They aren't on the demo path.
- [x] **The covering tests pass, updated only where they asserted the old kit.** None asserted it, so none were changed. New `MarkStartingKitTests` passes 6/6. `HearthMemoryMarkTests`, `M4SquadPickTests`, `CycloneSteerTests` (including the Command partials), `AEffectCommandNonUnitTargetTests`, `SearchRidgeTests`, `SearchTrailTests`, `FactionRoleHandlerPartialInitTests` and `RuntimeAbilityInitializeTests` all passed in the full run.
- [x] **The full EditMode suite passes.** Unity MCP, editor open: 2560 total, 2558 passed, 1 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). The one failure was `GridToLevelTests.Builder_RebuildNeedsOverwriteAndKeepsTheGuid` with "m_LockCount == 0", the known editor-open flake. Rerun alone, `GridToLevelTests` passed 20/20. Console: no compile errors.

## Chunks

### Chunk 3.1a: Mark's starting kit, Command instead of Vault

- Changed: `Mark_Ability_Attack_Command.asset`, `Mark_Ability_Attack_Vault.asset`, `MarkStartingKitTests.cs` (+ `.meta`).
- Criteria met: all four, with the evidence above. The in-game look is for the play check.
- Decisions and loose ends: see the sections below.

## Reviews and checks

- 3.1a: (written by the coordinator)

## Save reset

No. I didn't touch the save. For a check, use a new save (`Tools > Save Data > Clear Save Data`): see "Needs THJ".

## Decisions I made

- I flipped the two presets' `lockedByDefault` flags instead of removing Vault from `Unit_Mark.prefab`'s ability list. The kit is the same, but the prefab, the AI regression baseline's ability list and the Super Time reference all stay as they are, and Vault comes back with a single flag if THJ wants it again (Tier 2 data change).
- Command's `unlockResourceRequirements` (1 SP) stay in the asset. They're hidden and unused while the preset isn't locked, and they're kept in case the flag is flipped back.
- I didn't change the tree: `nodes[0]` still points at Command and still reads "Unlocks Command.". With Command at level 0 and no higher levels, that node shows as maxed, and its child "Command applies Weak" (`nodes[2]`) is no longer graph-locked. It's still gated at unit level 2.

## Needs THJ

1. **Old dev saves.** *What:* in a save made before this change, Mark loses Vault, because Vault was never saved. He gains Command only if that save already spent the SP on it, because the save stores Command at -1 otherwise. *Why it matters:* an old save that never bought Command has a Mark with no Vault and no Command until 1 SP is spent. *Options:* (a) accept it and clear old saves for demo checks (recommended: the demo starts from a new save, and nothing was migrated); (b) a small save migration that raises a stored Command -1 to 0. *Recommendation:* (a). *Default if no answer:* (a).
2. **Is Vault ever reachable in the demo?** The plan's wording "Vault behind the tree" could mean buyable. As built, Vault is fully off: no tree node unlocks it. Making it buyable means repointing a tree node to Vault (new title, text and icon), making Vault `upgradable` (a new save key) and giving it an SP cost. That's a design and save change for the designer and THJ, not part of this chunk.

## Docs to update

- `design/gdd/characters/mark.md`: starting kit is Command, not Vault. Vault is built but locked. Command's tree node is owned from the start. (Game designer, as the plan's gates say.)
- `design/gdd/progression-economy.md`: "Stunning Vault" (tree, 1 SP) and the Vault runes. The node is still buyable at level 3 with no Vault (see Risks).
- Plan 3.1b step 3: the "Vault hidden if 3.1a hasn't already removed it" lock isn't needed.

## Risks and loose ends

- **Stunning Vault node** (`nodes[4]`, an unlockable literal at unit level 3) can still be bought although Vault is locked. It would do nothing. It's unlikely within the demo's levels, but the designer should hide or re-target it.
- **`Tools/Skill Trees/Run Smoke Test (Play Mode)`** (`Core/Editor/SkillTreeSmokeTest.cs`, a menu tool, not in the suite) will now report Mark's "Command locked at start" and the "8 pips" check as failing, because Command no longer starts at -1. It needs updating if anyone still uses it. I left it alone (out of scope).
- `Unit_Mark.prefab` has a stale override `abilityOrchestrator.abilities.Array.data[8]` (Linda–Lucy Duo) past the array size of 8. It's harmless and untouched.
- An extra SP effectively frees up for Mark, since Command no longer costs one.

## Proposed commits

1. `tweak(mark): Mark starts with Command instead of Vault`: `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Command/Mark_Ability_Attack_Command.asset`, `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`, `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/MarkStartingKitTests.cs`, `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/MarkStartingKitTests.cs.meta` (plain data + test; game-wide kit change, reviewed alone)

## Other branches

`main` and other branches keep the old kit. It goes with the onboarding demo; carry it over only if THJ wants the kit change outside the demo.

## How to see it

1. `Tools > Save Data > Clear Save Data` (a new save).
2. Play from `Scenes/PreloadScreen.unity` through the Hearth to the world map, then start The Ridge. Or use the toolbar level picker on `GB_s2-ridge` and assign the squad.
3. Select Mark: his bar shows Fist Blitz, Walk and Command (plus any duo or Cleanse the level allows), with no Vault.
4. In the Home skill tree, Mark's first node "Command" shows as owned. "Command applies Weak" waits only on unit level 2.
5. Optional: play Hearth memory 4 (`GB_m4-mark`). Mark arrives with Command, and the Bloom, arrival, hold and Duo beats run as before.
