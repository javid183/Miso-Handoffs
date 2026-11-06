# Report: Hearth pool Claws (R2)

Plan: plans/onboarding/2026-11-05-m4-mark-rework-tech.md (R2)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: partial (the editor script and tests are written; the assets are NOT built yet, because Unity never imported the scripts)

## What changed

- `miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawWiring.cs`: menu Tools > Onboarding > Wire Hearth Pool Claws. Idempotent. Builds everything below in `Features/Onboarding/Hearth/PoolClaw/`.
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawTests.cs`: 5 EditMode tests.
- Nothing else touched. No `.meta` files exist yet for the two scripts (Unity has not imported them).

What the script creates (not yet on disk):
- `Unit_DarkClaw_Hearth.prefab`: variant of `Unit_DarkClaw_StartsAlert` (itself a variant of `Unit_DarkClaw`), `lethalDamageXpBonus` 0 and `abilityDamageXpReward` 0.
- `CP_Hearth_GUnitSpawnerEffect.asset`: `AssetDatabase.CopyAsset` of the shared spawner effect (fresh GUID), `unitPrefab` set to the Hearth Claw.
- `CP_Hearth_SpawnerCompoundEffect.asset`: copy of the shared compound, `effects` = [the new spawner effect].
- `CP_Spawner_Hearth.prefab`: variant of `CP_Spawner`, `intervalMode` SpecificTurns, `specificTurns` 1..8, `phaseTickEffect` = the new compound, `enableSpawnLimit` true, `spawnLimit` 1.

## Alert finding (key check)

Spawned Claws are Unaware by default, but there is a per-unit switch, no core code needed.
- `EnemyAlertTracker.Register` (`Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.cs:119-137`) runs on first sight of a unit, at level start or when it spawns. It reads `EnemyAlertSettings.StartsAlert` (line 126) and calls `EnemyAlertRules.StartsUnaware` (`EnemyAlertRules.cs:150-154`): a hostile unit starts Unaware only if the level's all-start-alert is off, the unit's `startsAlert` and `alwaysAlert` are off, and no hostile is in its sight.
- So `EnemyAlertSettings.startsAlert = 1` on the Claw prefab makes it spawn alert. The variant inherits that from the existing `Unit_DarkClaw_StartsAlert` (made for the Search trail, `SearchWiring.Trail.cs:93-125`). The shared `Unit_DarkClaw` has no alert settings and is unchanged.
- R3 sets the level to all alert anyway, which gives the same result. The prefab flag keeps the pools correct if reused elsewhere.

## Acceptance criteria

- [ ] The variant spawns a 0-XP Claw each enemy turn while its own Claw is dead: set up in the script, not built or run. Mechanism checked in code: `HazardEntity.ShouldFireOnCurrentTurn` (`HazardEntity.cs:181-189`) fires `phaseTickEffect` on listed turns; `AGUnitSpawner.ApplyUnguarded` returns when `CanSpawnMore()` is false (limit 1, dead units pruned). Needs the verifier's play check.
- [x] The alert answer with file:line: above.
- [ ] Tests: written (Claw XP fields 0 via `LevelXpChecker.UnitXpFields`, starts alert, effects point at the Claw, turn list covers 1-8, spawnLimit 1, compound is the phase effect, shared spawner and Claw unchanged). Not compiled or run.

## Save reset

no

## Decisions I made

- Built the Claw as a variant of the existing `Unit_DarkClaw_StartsAlert` rather than adding alert settings again: same behaviour, less duplication.
- Also zeroed `abilityDamageXpReward` (already 0 on the base) so the XP checker's two fields are explicit.
- Folder: `Features/Onboarding/Hearth/PoolClaw/`.

## Needs THJ

Blocked on the editor, not on a design question. The Unity editor is open but the MCP bridge timed out or dropped on every call (refresh, execute_menu_item, run_tests) for about 10 minutes, and the new scripts were never imported (no `.meta`). It may be busy, unfocused, or showing a modal. Please focus the editor and let it compile, or tell me it is free to retry. Then run Tools > Onboarding > Wire Hearth Pool Claws and the `HearthPoolClawTests` fixture. Compilation of my two files is unverified. I did not run the full suite and make no suite claim.

## Docs to update

- Plan R3: the pool prefab is `Features/Onboarding/Hearth/PoolClaw/CP_Spawner_Hearth.prefab`, once built.

## Risks and loose ends

- `EnemyAlertTracker.Register` skips units already in `_known`, so a revived Claw keeps its state. Not an issue for a fresh spawn.
- The tests assume the wiring menu has been run; they fail with a message pointing to it otherwise.

## Proposed commits

1. `feat(onboarding): Hearth pool spawner that summons a no-experience alert Claw on turns 1 to 8`: `Features/Onboarding/Hearth.meta`, `Hearth/PoolClaw.meta`, the four assets with their `.meta`, `Features/Onboarding/Editor/HearthPoolClawWiring.cs`, `HearthPoolClawTests.cs` and their `.meta` (plain; after the script has been run).

## Other branches

none

## How to see it

1. Focus Unity, let it compile.
2. Tools > Onboarding > Wire Hearth Pool Claws.
3. Open `Features/Onboarding/Hearth/PoolClaw/CP_Spawner_Hearth.prefab`: Interval Mode SpecificTurns, turns 1-8, spawn limit 1.
4. Test Runner > EditMode > `HearthPoolClawTests`.

## Review fixes (appended)

Edited `HearthPoolClawTests.cs` only (LF, no BOM):
1. Shared-assets test: dropped the intervalMode assert; now asserts the shared `CP_Spawner` phaseTickEffect is still `CP_SpawnerCompoundEffect` and that compound's `effects[0]` is still `GUnitSpawnerEffect`.
2. New test `ThePoolClawIsAVariantOfTheStartsAlertClaw`: asset type is Variant and its source path is `Unit_DarkClaw_StartsAlert.prefab`.
3. `ThePoolClawStartsAlert` asserts the settings component is not null first.

Not compiled or run: the MCP bridge still drops (session disconnected on refresh), so the menu tool, the second-run md5 check, `HearthPoolClawTests` and `CastAbilitySequenceTests` are all still to do once the editor answers.
