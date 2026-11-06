# Report: Linda's Explosive Arrow locked until after the Bloom (Mark's memory)

Plan: none (size S, D-408)    Agent: implementer    Branch: thj/onboarding
Outcome: done

## What changed

- `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`: `LevelAbilityLock`, Linda's entry (unit fileID 127187638987842907, the placed Linda: first entry, 1 AP at turn 1) gets a 6th ability, `Linda_Ability_ExplosiveArrow` (guid 8710a80b...). One inserted line, text edit, no re-save churn (git diff: 1 insertion).
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_PostBloom_UnlockExplosiveArrow.asset` (+ `.meta`, new guid 5c7e2a91...): `UnlockAbilitiesSequence`, `unlockAll: 0`, lists only the Explosive Arrow preset. Copied from `Memory4Mark_Hold_UnlockDuo`.
- `Memory4Mark_PostBloom_SequentialSequence.asset`: new sequence inserted as first step of `sequenceList`.
- `Features/Onboarding/Editor/HearthMemoryMarkTests.cs` and `.Flow.cs`: two expectations that pinned the old lock list and unlock count updated (see Decisions). No GuidedAbilityHint added.

## Acceptance criteria

- [x] Compile clean: console had 0 errors after refresh and compile.
- [x] New asset imports: loads as `UnlockAbilitiesSequence` named `Memory4Mark_PostBloom_UnlockExplosiveArrow`.
- [x] Full EditMode run: first run 1410 tests, 13 failed = the 11 expected reds + 2 that pinned the lock list. After updating those two expectations, `HearthMemoryMarkTests` re-run: 29 tests, 10 failed, the same 10 layout reds as in `m4-mark-tweaks-verify.md` (identical messages). `AIRegressionTest.Baseline_MatchesCurrentAI` is still the known red (seen in the full run; not re-run after the test edit, as it is unaffected). A final full run after the test edits was not done; the subset re-run covers the only files touched.
- [x] Prefab diff is just the one line. Editor was not in Play mode and no prefab stage was open (checked via editor before editing).

## Save reset

no

## Decisions I made

- Two tests went red because they pin Linda's exact lock list and the unlock-sequence count; updated just those expectations as the task allowed: `EveryDuoAndCleanseIsLockedOnEveryHero` (Linda's expected list also contains `Linda_Ability_ExplosiveArrow`) and `TheHoldRevealsTheTopClawsAndUnlocksOnlyTheMarkLucyDuo` (now expects two unlock sequences, one of them the new PostBloom one). Names left as they are.
- Linda is identified as unit 127187638987842907 via the Linda prefab instance (source guid a5261f30..., Unit_Linda) in the level; the other three entries are untouched.

## Needs THJ

none

## Docs to update

- `design/demo-spec.md` / build log: Memory 4 lock list now includes Linda's Explosive Arrow until after the Bloom (coordinator's call).

## Risks and loose ends

Answers to the checks:
- `Memory4Mark_Hold_UnlockDuo.asset` has `unlockAll: 0`, one ability (the Mark-Lucy Duo). Nothing before PostBloom unlocks Explosive Arrow: the only `UnlockAbilitiesSequence` assets in this memory's folder are Hold_UnlockDuo and the new one; no `unlockAll: 1` anywhere in the folder; the level prefab references no unlock sequence directly.
- The Bloom stage does not need Explosive Arrow. Its steps are camera, two Dialog nodes, `Memory4Mark_Bloom_LucyCastsCyclone` (`CastAbilitySequence` of the cast ability a0a2d8d9..., Lucy's Cyclone, not the arrow), Lucy runs ahead. The two `GuidedAbilityHint`s on the level point at ability 4a7d0771... (turn 1) and the Mark-Lucy Duo (pulse once unlocked); neither is the arrow. Objective condition types are `EntitiesDestroyed`, `TurnReached` and `UnitTileOccupied`, with no ability-based condition. Caveat: if a player needs Linda's arrow to kill Claws in an earlier stage, she can't now; I did not trace the Claw layout against that.
- Family Super Time looks unreachable in this level. `LevelStartFPFiller` produces 99 Family Time points at level start (clamped to the cap), so the points are full from turn 1, and `GUnit.CheckIfFactionSuperTimeAvailable` is true when they are full and a unit has a faction role. But the only caller of `ActivateFactionSuperTime` for the player faction is `GUnit.ActivateFactionSuperTime`, and the only asset referencing the `Bergsons_Ability_FamilySuperTime` ability (guid efdd5184...) is `Unit_TobaEnemy.prefab`; the other call site is the Goblin Queen boss death. None of Linda, Lucy, John or Mark carries that ability, and the lock list has no Super Time ability. So there is no player-facing trigger found. I read code and asset references only, not play-tested; a different trigger (an input binding by name) would not show in my grep. Linda's `superTimeAbility` is the same Explosive Arrow preset, so the known gap (a locked `superTimeAbility` still casts) would matter only if some path does trigger it. Nothing changed for it.
- Left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, TMP font, `PreloadScreen.unity`, `ProjectSettings` (their uncommitted changes were already there).

## Proposed commits

1. `feat(onboarding): lock Linda's Explosive Arrow in Mark's memory until the Bloom is over` (plain): `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`, `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_PostBloom_UnlockExplosiveArrow.asset`, `...UnlockExplosiveArrow.asset.meta`, `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_PostBloom_SequentialSequence.asset`, `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs`. One unit: the tests only change because of this data.

## Other branches

none

## How to see it

1. Open `GB_m4-mark` in Prefab Mode, select the root, look at `LevelAbilityLock`: Linda's entry (first) lists 6 abilities, the last being `Linda_Ability_ExplosiveArrow`.
2. Open `Memory4Mark_PostBloom_SequentialSequence`: first step is `Memory4Mark_PostBloom_UnlockExplosiveArrow`.
3. Play Mark's memory: Linda's Explosive Arrow is unavailable through the Bloom; after the Bloom cut-in finishes and PostBloom starts, it unlocks (no pulse).
