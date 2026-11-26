# Report: M1 "The Ridge" round 4.4: duo lock, Encore cast, potion hint, defeat by stage

Plan: plans/2026-11-25-m1-ridge-4-4-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done. Built and EditMode-tested; nothing checked in Play mode. Two things for THJ: the wiring now carries his tuned health factors (Findings 2), and his "visible in editor" toggle state is reset to hidden (Findings 3).

## What changed

All paths are under `miso/Assets/_Project/`. LF, no BOM, like the files around them. No core files.

**First: THJ's level re-tweak kept.**
- `MissionWiring.Ridge.Layout.Ambush.cs`: the ambush tiles are now THJ's: Black Claw prefab 2,2 (block 3,7); Dark Claws -1,2, 5,2, 4,1, -1,4 (block 0,7, 6,7, 5,6, 0,9).
- `MissionWiring.Ridge.Layout.cs`: removing the old dropped Claw now skips units listed in the ambush group, as the moved-Claw step already did. The Black Claw stands on that old tile, 2,2.
- **Health factors:** the wiring now uses THJ's tuned values. His prefab had the pocket Claws at **1.6** (5,-2) and **1.2** (5,-1), and the Black Claw at **0.75**. My first wiring run overwrote them with the old constants (0.75 / 0.75 / 0.45). I changed the constants to his numbers (`PocketClawHealthFactors` by tile, `BlackClawHealthFactor`) and re-ran, so they are back and stay on later runs.

**1. Family Footrace locked until "Race you to the top."**
- `MissionWiring.Ridge.cs`:
  - new `FootracePath`;
  - Mark's lock list is now Cleanse, Command and Family Footrace. Linda's whole-bar lock already included it;
  - `UnlockedAtTheLedge` now leaves out Cleanse and Family Footrace;
  - `WireBowHint` → `WireHints` keeps exactly two `GuidedAbilityHint`s, both `WhenUnlocked`: Linda's bow, then Family Footrace.
- `MissionWiring.Ridge.Sequences.cs`: new `M1Ridge_Cleared_UnlockDuo` (`UnlockAbilitiesSequence`, Family Footrace only), right after the reunion dialogue that ends on "Race you to the top.", before the reunion signal.
- `M1Ridge_Catch_Unlock.asset` no longer unlocks Family Footrace.

**2. Linda's Encore in the ambush.**
- `Features/Levels/Sequences/CastAbilitySequence.cs` (shared with other levels):
  - It now also accepts `ApplyMode.Self`: the target is the caster, and no cell is looked up (`targetCell` is ignored).
  - A Self cast is skipped with a warning when the caster hasn't learned the ability (upgrade level below 0) or when `CheckActivationFeasibility` fails. Encore needs grounded arrows.
  - Targeted casts behave exactly as before. The readiness check only applies to Self casts, so a scripted cast of an ability not yet learned in a memory isn't suddenly skipped.
  - New `Resolved.OnSelf`/`Targets` and the pure `SelfCastBlocker`.
- The cast step `M1Ridge_Ambush_LindaCastRecall` (THJ's asset, untouched) now comes after the camera returns to the family and **before** `EnablePlayerInputSequence`. The wiring builds it only if it is missing, and keeps an existing one as it is.

**3. Potion hint after the potion page.**
- New `Features/Onboarding/PouchHint.cs`. Once `Begin()` is called, the item pouch button on the abilities bar bobs about once a second (`AbilitiesBarHUDUI.BobItemPouch`). It stops for good once the pouch is opened or the potion is used (`abilityPerformed` with the potion preset). It holds no static state and listens to the bus only while it runs.
- New partial `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.PouchState.cs`: read-only `IsPouchOpen`.
- The optional potion-button pulse is not built.
- Wiring: a `PouchHint` on "Ridge Switches" (potion preset, 1 s), a third `SignalAction` `M1Ridge_PouchHint` → `PouchHint.Begin`, and a new `SignalSequence` `M1Ridge_Ambush_PouchHint` right after the potion page.

**4. Defeat by stage.**
- New `Features/Onboarding/StageDefeatRelax.cs`. `Relax()` sets the player faction's `LivingUnitsLOCondition` in the running level's defeat objectives back to 0, so from then on one sibling may fall and the level is lost only with both down.
- It changes only the running level's own data. A restart loads the level again with "at most one standing" (`WireDefeat` is unchanged).
- Wiring: a `StageDefeatRelax` on "Ridge Switches", a fourth `SignalAction` `M1Ridge_FamilyMayFall` → `Relax`, and a `SignalSequence` `M1Ridge_Ambush_FamilyMayFall` after the pouch-hint signal (S4's on-complete, before control returns).

**Final ambush order:** input off, HUD off → camera on the clue → discovery → west camera → reveal → caption → east camera → bell lines → reunion signal → potion page → **pouch hint** → **family may fall** → camera on the family → **Encore** → input on → HUD on → turn reset.

**Step lists:** the wiring keeps existing step lists, so I set the `M1Ridge_Cleared` and `M1Ridge_Ambush` step lists to the wiring's order once, in the editor. The next runs gave no warning.

## Level read-back and diff

- **Before** (THJ's version): 51 cells, ambush on block 3,7 (b), 0,7, 6,7, 5,6, 0,9. The fall and ambush units were *active* (his editor toggle).
- **After:** the same grid character for character, with `level hidden ambush 3,7 0,7 6,7 5,6 0,9`. The "listed but active" warnings are gone.
- **Prefab diff against THJ's version:** +117 / −8. The 8 deletions are all `m_IsActive: 1 → 0` on the 8 hidden units (Findings 3). The insertions are the second hint, the unlock lists, the `PouchHint`, the `StageDefeatRelax` and the two new `SignalAction`s. None of his health factors change after the fix.
- **Idempotent:** a second run left the level, the mission and every M1Ridge sequence byte-identical.
- **Open prefab:** GB_m1-ridge was open in Prefab Mode in THJ's editor, not dirty. I closed it before wiring so it couldn't save the old version over the new one, which is the likely cause of round 4.3's revert. Nothing unsaved was lost.

## Tests

| Run | Result |
|---|---|
| `M1RidgeTests`, `M1RidgeLayoutTests`, `SearchRidgeTests`, `FactionTurnLOConditionTests`, new `PouchHintAndDefeatRelaxTests`, `CastAbilitySequenceTests` | 88/88 passed |
| Full EditMode suite | **2714 total, 2713 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |
| `AIRegressionTest.Baseline_MatchesCurrentAI` by name | **46**, the same lines as before |

What the tests cover:
- `M1RidgeTests`:
  - `FamilyFootraceIsLockedUntilTheRaceYouLine`: locked on both bars; the only unlock is right after the "Race you to the top." dialogue;
  - `TheLedgeUnlocks…`: Family Footrace is not unlocked at the ledge;
  - `HerBowAndThenFamilyFootracePulseOnceEachIsUnlocked`: two hints kept;
  - Mark's lock list;
  - the ambush order after the page: pouch, may fall, camera, Encore cast with the Encore preset, control, reset.
- `CastAbilitySequenceTests`:
  - `SelfPreset_ResolvesOnTheCasterWithoutACell` (no cell lookup, target = caster);
  - `SelfPreset_StillNeedsItsUnitAndAbility`;
  - `SelfCast_IsSkippedWhenNotLearned`, `SelfCast_IsSkippedWhenItsActivationCheckFails`, `SelfCast_GoesAheadWhenLearnedAndUsable`;
  - `PresetNeitherTargetedNorSelf_FailsWithReason` replaces `PresetNotTargeted_FailsWithReason` (Surrounding still refused);
  - `EverythingPresent_Resolves` also checks the targeted path's `Targets`.
- `PouchHintAndDefeatRelaxTests`:
  - the hint waits for its call; opening the pouch ends it for good; using the potion ends it and another ability doesn't; the bob interval;
  - the relax sets only the family's check to 0 and changes nothing without one;
  - The Ridge wires both signals to the right methods;
  - the level's defeat count is still 1 until the relax.
- `M1RidgeLayoutTests`: THJ's block; ambush tiles as placed, not on the plateau Claws or in the top zone; THJ's health factors.

Needs THJ's play check:
- the bobbing pouch on the HUD;
- Encore actually casting (it needs grounded arrows);
- the duo hint's look;
- the loss rules before and after the ambush.

## Findings

1. **Are arrows usually grounded when Encore casts? Probably, but not checked in play.** Arrows Linda fires and that aren't caught, refunded or picked up lie on the ground. The plateau fight before the ambush is mostly bow and Watch shots, so some are usually down, unless Mark picked them up or a catch returned them. When none are down, the feasibility check fails and the cast is skipped with one warning, and the sequence goes on.
2. **THJ's health factors are now in the wiring:** pocket 1.6 / 1.2, Black Claw 0.75. That is about 26 and 19 HP for the pocket pair at the early tier, far above the design's 12, and the "second catch finishes the pair" reasoning no longer holds. That's his call; the design doc and the playtest notes should follow.
3. **THJ's "visible in editor" toggle gets reset by the wiring.** The wiring keeps hidden units inactive in the prefab, as built since 4.1, so the 8 units he had toggled visible are hidden again. At play the level would hide them anyway (`HiddenLevelUnits.Awake`, with a warning). To edit them visibly, toggle them on after wiring and off again before playing, or just play: Awake hides them.
4. **The AI's copy of the defeat check** is taken when stages advance (`objectivesSetAdvanced`), before the relax runs, so the AI still sees "at most one standing" until the next stage change. It only affects the AI's intent weighting, not the loss rule. Note only.
5. **The leftover `M1Ridge_Cleared_PotionPage.asset` + `.meta`** is still untracked. Delete it.

## Decisions I made

- The Self-cast readiness check (learned, feasible) applies only to Self casts, so other levels' targeted casts don't change.
- The pouch-open state is read through a new read-only accessor in a partial file, `AbilitiesBarHUDUI.PouchState.cs`, rather than editing the big file.
- The defeat relax and the pouch hint sit on the existing "Ridge Switches" child and listen to two new signals, the same pattern as the reunion.
- The Encore cast asset is kept as THJ made it (unit nickname, timeout, roles off). The wiring only creates it when it is missing.
- The ambush test now checks only that the pack doesn't start in the top zone, not "not beside it": THJ's -1,4 is beside the zone tile 0,4.

## Proposed commits (after THJ's play check)

4.3 and the Neutral fix are still uncommitted and touch the same files, so they go together with 4.4, except the shared cast change:

1. `feat(levels): CastAbilitySequence also casts Self abilities on their user, skipped when not learned or not usable` (plain, shared): `Features/Levels/Sequences/CastAbilitySequence.cs`, `Features/Levels/Sequences/Editor/CastAbilitySequenceTests.cs`.
2. `feat(onboarding): The Ridge's ambush close in, turn reset, duo lock and hints, Encore, potion hint and defeat by stage` (plain):
   - `Content/Levels/Greybox/GB_m1-ridge.prefab`
   - `Features/Onboarding/Editor/MissionWiring.Ridge.cs`, `.Sequences.cs`, `.Layout.cs`, `.Layout.Ambush.cs`, `HearthMemoryWiring.Mark.Level.cs`
   - `M1RidgeTests.cs`, `M1RidgeLayoutTests.cs`, `PouchHintAndDefeatRelaxTests.cs` + `.meta`
   - `Features/Onboarding/FactionTurnLOCondition.cs`/`OpenTurnWatch.cs` if still uncommitted, `PouchHint.cs` + `.meta`, `StageDefeatRelax.cs` + `.meta`, `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.PouchState.cs` + `.meta`
   - `Resources/Sequences/M1Ridge/`: the Ambush and Cleared step lists, `M1Ridge_Catch_Unlock`, the three ambush cameras, and new `M1Ridge_Cleared_UnlockDuo`, `M1Ridge_Ambush_PouchHint`, `M1Ridge_Ambush_FamilyMayFall`, `M1Ridge_Ambush_ResetTurn`, `M1Ridge_Ambush_LindaCastRecall` (THJ's), each with its `.meta`
   - THJ's `HiddenLevelUnits.cs` and `BlackClaw_Ability_Attack_Effect_AttrMod.asset`, if he wants them in.

Not to stage: `miso.slnx`, `LevelM2-C1.prefab`, `M1Ridge_Cleared_PotionPage` (delete), `claude-handoff/`.

## Save reset

No. Play mode was never started.

## How to see it

Clear the save and set `deactivateIntroOutroSequences` off. Close GB_m1-ridge's Prefab Mode before playing or re-wiring.

1. **Family Footrace locked:** on family turn 1 and after the ledge, neither Linda's nor Mark's bar shows Family Footrace (the bow comes back at the ledge; Footrace doesn't).
2. **Unlocked by the race line:** when the pocket is cleared, after "Race you to the top.", Family Footrace appears on both bars and pulses until it is used. The bow's pulse still works as before.
3. **Defeat before the ambush:** let a sibling fall on the plateau (before the ambush). The level is lost.
4. **The ambush:** the pack appears on THJ's tiles (Black Claw block 3,7; Claws 0,7, 6,7, 5,6, 0,9). After the potion page and the camera back on the family:
   - Linda casts Encore with no input, and her grounded arrows come back (if none are down, a console warning and nothing else);
   - control and the HUD return;
   - the turn resets, and the Black Claw close-up plays.
5. **Potion hint:** after the ambush, the pouch button bobs about once a second. Open the pouch, or use the potion: it stops and doesn't come back.
6. **Defeat after the ambush:** during "Drive them off the ridge", let one sibling fall. The level goes on. Let both fall: the level is lost.
7. **Restart:** restart mid-level. One sibling down loses again until the next ambush.

## Review (miso-reviewer, 4.3 + 4.4, 2026-11-25), pasted by the coordinator

**APPROVE.** Should-fix: (1) `CastAbilitySequence.cs:134-142` Self-cast feasibility check outside the try (an effect check can throw with input off) → wrap and `yield break`; (2) `PouchHint.cs:69` `FindObjectsByType` every frame → cache/refresh per bob; (3) `MissionWiring.Ridge.Layout.Ambush.cs:10-12` long comment line. Notes: only Memory 4 Cyclone and the Ridge Encore use `CastAbilitySequence` (targeted path unchanged); scripted Encore ignores cooldown and the level lock (fine for M1); THJ's 5 s Encore timeout may return input while arrows still fly (watch in play); defeat relax touches the level instance only (restart restores it); AI's copy of the defeat check stays at 1 until the next stage change (intent weighting only); turn reset runs one frame after input returns. Separate commit first: `CastAbilitySequence.cs` + `CastAbilitySequenceTests.cs`.

## Should-fixes from the 4.3 + 4.4 review (miso-implementer, 2026-11-25)

1. **`CastAbilitySequence`: the Self-cast check is now guarded.** New `SelfCastBlockerSafely(name, upgradeLevel, isFeasible)` reads the upgrade level and runs the activation check inside a try/catch. A throw is logged (`Debug.LogException`) and counts as a reason to skip: the sequence warns and stops the cast, the same as for the activation call. `PlaySequence` uses it.
   - New tests: `SelfCast_IsSkippedWhenItsCheckThrows` and `SelfCast_IsSkippedWhenReadingItsLevelThrows`, both expecting the logged exception.
   - `SelfCast_GoesAheadWhenLearnedAndUsable` also checks the guarded path.
2. **`PouchHint` no longer searches the scene every frame.** The bars are cached and looked up again once per bob, or straight away when the cache is empty or a cached bar is gone. The cache is cleared in `OnDisable`.
3. **`MissionWiring.Ridge.Layout.Ambush.cs`:** the class comment is rewrapped.

The wiring wasn't re-run (not needed): the level and every M1Ridge asset are byte-identical to the end of round 4.4.

| Run | Result |
|---|---|
| `CastAbilitySequenceTests`, M1/Ridge classes, `FactionTurnLOConditionTests`, `PouchHintAndDefeatRelaxTests` | 90/90 passed |
| Full EditMode suite | 2716 total, 2715 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |

Files: `Features/Levels/Sequences/CastAbilitySequence.cs`, `Features/Levels/Sequences/Editor/CastAbilitySequenceTests.cs`, `Features/Onboarding/PouchHint.cs`, `Features/Onboarding/Editor/MissionWiring.Ridge.Layout.Ambush.cs`. LF, no BOM.

## THJ's play of 4.4: Encore cast and the ledge Blitz (miso-implementer, 2026-11-25)

### 1. Encore didn't cast: fixed (no core code)

**Cause** (confirmed in code): Encore's check `LindaQuiver.HasGroundedArrows` also asks for Encore's full AP cost (`RecallRules.CanRecall(…, EncoreAp.points, EncoreAp.cost)`). By the time the scripted cast runs, Linda has spent her AP; the turn reset comes after the cast.

**Fix:**
- New `Features/Levels/Sequences/IWaivableApCheck.cs`: a unit component that adds its own AP check to an ability can leave the AP part out for the length of a scope (`IDisposable WaiveApCost()`).
- `LindaQuiver.EncoreAp.cs` implements it with a counter. While the AP part is waived, the check compares (0, 0) for AP and cost, which blocks nothing. **Grounded arrows and quiver room still count.**
  - `LindaQuiver.cs` changes one line: `HasGroundedArrows` reads `EncoreApForCheck`.
  - Outside a scripted cast the check is exactly as before. The bar, the grey reason and the AI read `EncoreAp` unchanged.
- `CastAbilitySequence`: new serialized option **`ignoreApCost`**, default **off**, so Memory 4's cast and any other existing cast check exactly as before.
  - When it is on, a Self cast's feasibility check runs inside `CheckWithApWaived`: every `IWaivableApCheck` on the caster waives the AP part, and the waiver is put back afterwards, also when the check throws. The throw is still caught by the existing guard.
  - Targeted casts run no feasibility check, so the option only matters for Self casts.
- **THJ's `M1Ridge_Ambush_LindaCastRecall.asset`:** one field added, `ignoreApCost: 1`; the rest of his asset is unchanged.
- The wiring's `BuildEncoreCast` sets the option too, for a freshly built asset; an existing one is still kept. The wiring wasn't re-run.

**AP spent: none.** `AbilityOrchestrator.ActivateAbility` → `RuntimeAbility.Activate` charges no AP; AP is charged only on the player's action path (`FactionControllerBase`). The turn reset right after the cast refills AP anyway.

**Tests:**
- `CastAbilitySequenceTests`:
  - `IgnoringTheApCost_WaivesItOnlyWhileChecking`;
  - `IgnoringTheApCost_KeepsTheChecksAnswerAndPutsTheWaiverBackWhenItThrows` (no arrows still blocks);
  - `IgnoringTheApCost_IsOffByDefault`.
- `EncoreApTests.TheFeasibilityCheck_LeavesTheApOutWhileWaivedButStillNeedsArrows`: with 0 AP, waived, no grounded arrows → not castable; an arrow down → castable; the waiver over → blocked again. The existing test still covers the AP check with the option off.
- `M1RidgeTests`: the ambush's Encore cast has `ignoreApCost` on.

| Run | Result |
|---|---|
| `CastAbilitySequenceTests`, `EncoreApTests`, M1/Ridge classes, `PouchHintAndDefeatRelaxTests` | 98/98 passed |
| Full EditMode suite | 2720 total, 2719 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |

**Files:**
- `Features/Levels/Sequences/IWaivableApCheck.cs` + `.meta` (new)
- `Features/Levels/Sequences/CastAbilitySequence.cs`
- `Features/Levels/Sequences/Editor/CastAbilitySequenceTests.cs`
- `Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`, `LindaQuiver.EncoreAp.cs`
- `Features/Player/Linda/Scripts/Quiver/Editor/EncoreApTests.cs`
- `Features/Onboarding/Editor/MissionWiring.Ridge.Sequences.cs`, `M1RidgeTests.cs`
- `Resources/Sequences/M1Ridge/M1Ridge_Ambush_LindaCastRecall.asset`

`CastAbilitySequence`, `IWaivableApCheck` and the quiver change belong in the shared-cast commit.

### 2. Mark sometimes ends on prefab 7,-3 after killing the ledge Claw: investigated (no code changed)

**What the code does** (`Core/Systems/AbilitySystem/Effects/Runtime/AEffectDashAttack.cs`):
- **`ApplyUnguarded` (:142-153)** decides once, at activation, with `PredictsLethal` (:220-227 → `AbilityDamagePreview.PredictsLethalOn`, `damage >= hp`):
  - **predicted lethal:** no staging. Mark strikes from where he stands, then hops straight into the target cell (`ApplyDirect`);
  - **not predicted lethal:** Mark first walks to `TryResolveApproachCell`, which is `path[^2]`, the tile before the target on the path (:58-82). Coming up the east column, that is **7,-3**.
- **`DashAttackIE` (:155-202)**, after the hit: waits `vacatedCellCheckDelay`, then hops into the target cell only if `entity.CurrentCell == approachCell && targetCell.IsWalkable` (:185-193). **Mark's `Mark_Ability_Attack_Primary_Effect_DashEffect.asset` sets `vacatedCellCheckDelay: 0` (line 32)**, so the check happens right after the attack's effects report done, in a single attempt.
- **Ending on 7,-3 therefore needs both:**
  - (a) Mark stood on, or staged to, 7,-3: either the preview wasn't lethal, or the auto move-attack walked him there first. `PlayerController.TryFindApproachCell` (:1411-1450) picks a cell in Blitz range and prefers to stay back, so it isn't always 7,-3.
  - (b) The one-shot "vacated cell" check didn't see the cell free.
- **Why (b) can miss:** the check doesn't wait for the target to be gone. It only waits `WaitForEndOfFrame` plus "no attack effect in progress", then 0 s. If the Claw's removal from the cell lands later than that, for any reason, the hop is skipped for good.
  - `GUnit.Die` → `DieInternal` unplugs at once (`GUnit.cs:771-775`), but `Die` is called from the HP attribute's `onMinReached`, wired in the Inspector.
  - `IsWalkable` is also false while anything is stashed or planted with walking disallowed on the cell (`GridCell.cs:22-27`).
- **Why (a) can happen:**
  - The preview leaves out damage-reduction chances below 100% (`AbilityDamagePreview.ApplyGuaranteedDecrementModifiers`) and leaves crits out entirely. Blitz's crit chance reads `Stat_CRC` × 0, so it's off.
  - The hit is `8 × Stat_DMG`, bounded by `StatUB_DMG` (`Mark_Ability_Attack_Primary_Effect_AttrMod.asset`). With Stat_DMG exactly 1, the prediction is 8 ≥ 8: lethal. Anything that leaves Mark's Stat_DMG under 1 makes the preview round to 7 and stage.
  - Continuous Attack is off then (the start signal), and the ledge Claw can't move (Unaware, skipped), so neither explains it.
- **Not reproduced in edit mode:** the lethal check, the transporter and the death path all need a running level (units initialized on a grid, the HP attribute's death event). I couldn't pin which of (a)/(b) THJ hit without a log from a run where it happened.

**Smallest fixes, in order of preference:**
1. **Data, not core:** set `vacatedCellCheckDelay` on `Mark_Ability_Attack_Primary_Effect_DashEffect.asset` to about 0.2. The field's own tooltip says the delay is there to give death and push reactions time to resolve; 0 removes that margin. One field, it affects every Blitz, and it adds a 0.2 s beat.
2. **Core, robust:** in `DashAttackIE` (:185-193), instead of one check after the delay, wait up to a short limit (for example 0.5 s) until the target is no longer alive or no longer on the cell, then check `IsWalkable` and hop. That fixes (b) whatever the timing.
3. **Level only:** let S1 also accept 7,-3 again (THJ dropped that in 4.3). It hides the symptom for M1, not the Blitz behaviour.

**To pin it in play:** a temporary log in `DashAttackIE` (direct or staged, preview damage vs HP, and `targetCell.IsWalkable` / the target's `IsAlive` at the check). The coordinator can schedule it with THJ.
