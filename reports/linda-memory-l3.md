# Report: Linda memory level data (L3)

Plan: plans/onboarding/2026-11-04-linda-memory-tuning.md (L3; D-373, D-380, D-381, D-382)    Agent: implementer    Branch: thj/onboarding
Outcome: done. Wired through Tools > Onboarding > Wire Memory 1 (Linda), run twice in the open editor (prefab was not in Prefab Mode). No Play mode.

## What changed

All code in `miso/Assets/_Project/Features/Onboarding/Editor/` (LF kept):
- `HearthMemoryWiring.Linda.cs`: new consts `UnlockSequencePath`, `ExplosiveArrowPath`, `EncorePath`; `EnsureUnlockStep()` (called in `Run` before `WireLevel`) and `WireAbilityLock()` (called in `WireLevel` after the hidden claws).
  - Lock: `LevelAbilityLock` on the level object, one entry, `Unit_Linda`, abilities Explosive Arrow + Encore.
  - Hint: `GuidedAbilityHint` on the level object, `Set(ExplosiveArrow, 1)` (same as John's call) + `startMode = WhenUnlocked`. Only rewritten when ability/mode differ.
  - Sequence: new `Memory1Linda_Interruption_UnlockAbilities.asset` (`UnlockAbilitiesSequence`, `unlockAll` off, both presets), created or rewritten by the wiring; inserted into `Memory1Linda_Interruption_SequentialSequence` immediately before the first `EnablePlayerInputSequence`; skipped if already present.
- `HearthMemoryLindaTests.cs`: 3 new tests (lock entry; unlock step after dialogue and camera-back and before input/HUD, exactly one; hint on Explosive Arrow with WhenUnlocked).

Interruption order now: DisableInput, HideHUD, CameraToRoom, LSBExecution, Reveal, Dialogue, CameraBack, **UnlockAbilities**, EnableInput, ShowHUD (the 9 hand-made steps are unchanged, one inserted).

## Diff summary (prefab and assets)

- Prefab run 1 vs saved pre-run diff: only (a) two `addedObject` entries in a PrefabInstance's added-components list, (b) the `LevelAbilityLock` MonoBehaviour (Linda unit ref, Explosive Arrow guid 8710a80b..., Encore guid c5e9a7f3...), (c) the `GuidedAbilityHint` MonoBehaviour (`startMode: 1`, first/last turn 1, amplitude 0.15, period 1), plus shifted hunk line offsets. Nothing else.
- Interruption sequence: +1 line (the new step). New asset and `.meta`.
- Run 2: md5 of the prefab and all `Memory1Linda_Interruption_*.asset` files identical to run 1.
- Saved diffs: `C:/Users/javid/AppData/Local/Temp/claude/E--Work-Projects-miso/fc8a7484-be48-4d45-8fd7-e011d7c2c808/scratchpad/before.diff` and `after1.diff`.

## turnOrder preserved: yes

The six `propertyPath: turnOrder` override blocks are in both the before diff and the after diff, and `diff before after` shows no changed line inside them (only hunk offsets).

## Acceptance

- [x] Lock, unlock step, hint wired and idempotent: run twice, byte-identical.
- [x] Tests: new tests pass. EditMode Run All: 1339 total. Failures: `AIRegressionTest.Baseline_MatchesCurrentAI` (known), plus `GridToLevelTests.Builder_StripsTheTemplates...` and `Builder_WritesNothingWhenThePaletteLacksAPrefab`. Those two failed with "GB_24-nook.prefab already exists" in `Greybox/__Test`, a leftover from the editor session dropping its MCP connection mid-run; the folder is gone now and the whole `GridToLevelTests` class re-ran 20/20 green. Unrelated to this chunk.
- Needs THJ play check (below).

## Save reset
no

## Decisions I made
- Insert point is "before the first EnablePlayerInputSequence" (equals after CameraBack in the current order).
- Hint uses `Set(arrow, 1)` like John's, since turn fields are ignored in WhenUnlocked mode.

## Needs THJ
none

## Risks and loose ends
- Super Time still casts the Explosive Arrow preset without the bar (accepted earlier).
- `Memory1Linda_Interruption_CameraBack/CameraToRoom.asset` were already dirty before this run (THJ's edits); not touched by me.
- Encore pulse: after the unlock, the Encore button only pulses when the quiver is empty.

## Proposed commits
1. `feat(onboarding): the Linda memory locks Explosive Arrow and Encore until the interruption unlocks them`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLindaTests.cs`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-linda.prefab` (includes THJ's claw `turnOrder` overrides)
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Interruption_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Interruption_UnlockAbilities.asset` + `.meta`
   - Decide separately: `Memory1Linda_Interruption_CameraBack.asset` and `_CameraToRoom.asset` (THJ's earlier edits, not mine).

## How to see it (play check for THJ)
1. Open the Linda memory; start. Linda's bar has no Explosive Arrow or Encore (and number keys skip them).
2. Play stage 1 and 2 until Linda reaches the gather tile: interruption plays; after camera-back both buttons appear without reselecting Linda.
3. Explosive Arrow pulses (hint) the moment input returns, on any turn; using it ends the pulse.
4. Spend all arrows: Encore breathes; arrow pickup or Encore use stops it. Hint and Encore pulse do not stack.
5. Claw turn order matches your 0/1/2 values.
6. Re-run Tools > Onboarding > Wire Memory 1 (Linda): no file changes.

## Review fixes

- `TheInterruptionUnlocksBothAbilitiesBeforeInputAndHudReturn` (HearthMemoryLindaTests.cs only): each `FindIndex` (dialog, cameraBack, input, hud) is now asserted `>= 0` with a message, and the unlock step's abilities are asserted to be exactly the Explosive Arrow and Encore presets (`CollectionAssert.AreEquivalent`). LF, no BOM kept.
- Compiled with no errors. EditMode Run All: 1339 total, 1337 passed, 2 failed, 0 skipped.
- Failures: the known `AIRegressionTest.Baseline_MatchesCurrentAI`, and `QuiverWiringTests.RecallAbility_IsTwoApCooldownTwoSelfCast` (description no longer contains "2 AP"; Recall's text was changed in commit 87174b9, so the test needs updating by whoever owns that change). Not caused by this edit.
