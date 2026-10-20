# Report: Masher reckless tank, C3 (data)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (C3)    Agent: miso-implementer    Branch: masher-tweak
Outcome: done

## What changed

- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterPresetBuilder.cs` (+ `.meta`): new editor tool, menu **Tools/Masher/Build Counter Preset**. It copies `MasherGoblin_Ability_Attack.asset` to `MasherGoblin_Ability_Counter.asset` with `AssetDatabase.CopyAsset`, and sets `targetType` to CellOccupant (2) on both presets through `SerializedObject`. It refuses, with a warning, if the counter asset already exists. Kept under `Editor/` so the copy can be rebuilt. UTF-8 BOM and LF, like `MasherCounterRulesTests.cs` next to it.
- `miso/Assets/_Project/Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Counter.asset` (+ `.meta`, GUID `f88aedf9f32f0ad44a5d60d7981d9444`): new, made by running the tool once through the MCP. It is byte-identical to the Attack preset except `m_Name`.
- `.../Attack/MasherGoblin_Ability_Attack.asset`: `targetType` 3 → 2. Saving the asset through Unity also wrote five newer fields that were missing from the file (`autoMoveAllowed: 0`, `introducible: 0`, `introductionSequence`, `allyTargetTagQuery` empty, `ghostSource: 0`, `affectedAreaPreviewSprite`). Each one is at its code default (`ghostSource` 0 = `AbilityOwner`, the initializer), so nothing behaves differently.
- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`, edited through `PrefabUtility.LoadPrefabContents` / `SaveAsPrefabAsset` (MCP `execute_code`), not by hand:
  - root handler `&-4332957646936667060`: `ability.preset` = counter, `stateName: PrimaryAttack`, `abilityActivationFrame: 12`, `sideVisualMode: 1` (see Decisions);
  - child handler `&8123456789123456791` on `Visual` removed, together with its `m_AddedComponents` entry;
  - Unity also serialized the root handler's newer base fields at their code defaults (`showRoleZone: 1`, `roleZoneSprite`, `roleZoneSlot: 0`, `declineTexts: []`, `playDeclineBark: 1`). No behaviour change.
  - The diff is 9 lines added and 141 removed; the file stays LF.
- `miso/Assets/_Project/Core/Systems/AISystem/Editor/AIRegressionTest.cs`: one `ExpectedAbilityCatalog` line, in path order after the Attack line (D-104). Nothing else changed; LF, no BOM, as before.

## Shared and copied references (asked by the coordinator)

`AssetDatabase.CopyAsset` copied only the preset: `MasherGoblin_Ability_Attack.asset` has no sub-assets. Every reference is **shared**:

- `baseLevel.effects[0]` → `MasherGoblin_Ability_SpawnerEffect.asset`, shared;
  - which spawns `Prefabs/AOE_Attack _MasherGoblin_Variant.prefab` (the AOE prefab), shared;
  - which runs `MasherGoblin_Ability_CompoundEffect.asset`, shared;
  - which applies `MasherGoblin_Ability_Attack_Effect_AttrMod.asset`, the 10 × `Stat_DMG` damage, shared.
- `utilityScoreEvaluator` → `MasherGoblin_Attack_UtilityScoreEvaluator.asset`, shared. Only the AI reads it; the counter isn't on the unit's list, so it doesn't matter today.
- Nothing was copied. To tune the counter's damage or area later, copy the spawner, AOE variant, compound and AttrMod chain, or at least the AttrMod together with everything that points at it. Nothing in the chain references `MasherGoblin_Ability_Attack_Effect_TagMod.asset`; I left it alone.

## Child FXRunner `7667962937869190177`: kept

It is used. It sits on the `Visual` child, next to the `Animator`, with `sfxID: A_SFX_Generic_Footstep`. `A_Enemy_MasherGoblin_Move_Side.anim` has two `PlaySFXSlot` animation events, and Unity delivers them to components on the Animator's GameObject. That makes this FXRunner the Masher's footstep sound. Nothing references it by fileID: the root handler and the orchestrator's FX calls use the root FXRunner `519988111897751012`.

## Acceptance criteria (C3)

- [x] Compiles: refresh and recompile are clean, with no errors and no Masher warnings. Unrelated warnings were already there (CS0108/0618/0414 in editor tools, "Serialization depth limit" on `RuntimeAbility`).
- [x] The prefab has one handler, not two. Scratch `execute_code` (instantiated with HideAndDontSave, destroyed after, nothing saved) found:
  - `MasherGoblinFactionRoleHandler` count = 1, on the root;
  - preset = `MasherGoblin_Ability_Counter`, state `PrimaryAttack`, frame 12, side 1.
- [ ] "The did not initialize its role ability warning is gone in Play": **needs the verifier's play check.** No Play mode was run. The root handler, which had no preset and so raised that warning, now has one.
- [x] The counter isn't on the unit's ability list: the list is `[MasherGoblin_Ability_Attack, MasherGoblin_Ability_Walk]` (scratch check). The AI unit catalog line didn't change.
- [x] Both presets report `TargetType == CellOccupant` (scratch check, read through the `TargetType` property).
- [x] The AI catalog failure is unchanged:
  - `AIRegressionTest.Baseline_MatchesCurrentAI` ran alone before my changes and in the full suite after.
  - Same 35 failures, same names. The only text difference is the existing `abilities.count` mismatch: `expected 89, found 94` became `expected 90, found 95`.
  - No new `abilities.unexpected` line. Checks went from 704 to 706: the counter's `abilities.name` and `abilities.evaluator` checks are new, and both pass.
- [x] EditMode, Run All (MCP): 327 tests, 326 passed, 1 failed. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).

Test coverage: this chunk is data only, with no new logic to unit-test. The catalog line is checked by `AIRegressionTest` itself; everything else was checked by the scratch check above, and the warning needs the play check.

## Save reset

No.

## Decisions I made

- **Menu path `Tools/Masher/Build Counter Preset`, not `MISO/Masher/...`** as the brief said. `conventions.md` and the implementer rules put editor tools under `Tools/`, and every existing tool menu sits there (`Tools/AI/...`, `Tools/Levels/...`). Same behaviour. Easy to rename if the coordinator prefers the brief's path.
- **`targetType` set through `SerializedObject` in the tool**, not by a YAML edit, so a rebuild also reapplies it. The tool sets it on Attack before the copy and again on the counter.
- **Also copied `animationData.sideVisualMode: 1`** to the root handler, beyond the plan's two fields. The old child handler, which played the counter until now, and the unit's own Attack both use 1 (LeftIsFlippedRight). Left at 0, the counter could face the wrong way when striking left. This keeps today's look, in line with D-096 (copy of the slam).
- **The tool is kept** under `Editor/`, as the brief asked, so the copy can be rebuilt. It refuses to overwrite an existing counter.
- **Prefab edits through Unity's prefab API** (MCP `execute_code`), not hand-edited YAML and not added to the tool. They were one-off, and Unity wrote the diff.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` or the Masher notes: the counter preset exists, its references are shared with the slam, and the builder lives at `Tools/Masher/Build Counter Preset`.
- `editor-checks.md` (optional): a single-test `run_tests` run of `AIRegressionTest` takes about 40 s; `get_test_job` times out on the first 60 s wait and returns on the second.

## Risks and loose ends

- Shared effect chain: a damage or area change to the slam also changes the counter until the chain is copied (accepted for now, D-096).
- The root handler now serializes `showRoleZone: 1`, which was already its runtime value from the field initializer. If Shift or role-zone presenters treat the Masher handler like a Bergson one, that predates this chunk; I didn't check it.
- The AI target is now a `GUnit` (`targetType` 2). The plan's Big Ogre 2 × 2 check stays with the verifier's play run.
- The plan's C3 Accept line "the warning is gone in Play" is not verified here (no Play mode).

## Proposed commits

1. `feat(masher): add counter preset copied from the slam, aim slams at units, one role handler on the prefab` (plain data, but the prefab touches the Family Roles handler wiring, so worth a reviewer diff):
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterPresetBuilder.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterPresetBuilder.cs.meta`
   - `miso/Assets/_Project/Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Counter.asset`
   - `miso/Assets/_Project/Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Counter.asset.meta`
   - `miso/Assets/_Project/Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Attack.asset`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`
2. `test(ai): list the Masher counter preset in the AI regression ability catalog`:
   - `miso/Assets/_Project/Core/Systems/AISystem/Editor/AIRegressionTest.cs`

   It is separate because it is a test-only change to a golden-master file (D-104), easy to revert alone. It depends on commit 1: without the asset it would add an `abilities.missing` failure.

Leave unstaged: `miso/Packages/*`, `miso/ProjectSettings/*`, which were already dirty and aren't part of this work.

## Other branches

`thj/home-test` needs this together with the rest of the Masher work at merge (already noted in the plan's Risks).

## How to see it

1. In Project, open `Resources/UnitSpecific/Enemy/Masher Goblin/Attack/`. `MasherGoblin_Ability_Counter` sits next to `MasherGoblin_Ability_Attack`. Both show Target Type = Cell Occupant in the Inspector.
2. Open `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`:
   - the root has one `MasherGoblinFactionRoleHandler`, with Ability preset = the counter, state `PrimaryAttack` and frame 12;
   - `Visual` has the Animator and the footstep FXRunner, and no handler;
   - the GUnit's ability list is Attack and Walk.
3. Tools > Masher > Build Counter Preset now logs "already exists; not overwriting".
4. Play `LevelE3-C1` and hurt the Masher. The "did not initialize its role ability" warning should no longer appear. The counter still behaves as before until C4.
5. Test Runner > EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` is red, with 35 failures as before.
