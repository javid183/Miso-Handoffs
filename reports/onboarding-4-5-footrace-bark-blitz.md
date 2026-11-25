# Report: Blitz hop wait, race listener fix, Family Footrace result bark (round 4.5)

Plan: coordinator's brief of 2026-11-25 (THJ's decisions after the 4.4 play)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done. Built and EditMode-tested; nothing checked in Play mode. Two core changes (A and B, both approved by THJ), each kept to its own files. No other core change. The level wiring was not re-run, and GB_m1-ridge is unchanged.

## What changed

### A. Core: the Blitz hop waits briefly for a killed target to leave its cell

`Core/Systems/AbilitySystem/Effects/Runtime/AEffectDashAttack.cs` (LF, no BOM):
- `DashAttackIE` records, before the attack, the unit standing on the attacked cell (the target, or the cell's occupant when the target is the cell).
- After the attack, and after `vacatedCellCheckDelay` (unchanged semantics), the hop is no longer decided on a single instant check:
  - **The cell is free:** decided at once, no added delay.
  - **The victim survived** (alive, health left, still on the cell): decided at once, no hop and no wait.
  - **The victim is dead, gone from the cell, or at 0 health but the cell isn't free yet:** wait frame by frame, up to `MaxVacateWait` = 0.5 s, then decide.
  - The wait uses scaled time (`Time.deltaTime`), matching the effect's other waits (`WaitForSeconds`).
- New public pure helper `DecideVacate(cellWalkable, targetGone, targetHealthDepleted, waited, maxWait)` → `Decide`/`Wait`, plus the private `IsVictimGone` and `IsVictimHealthDepleted`.
- Test `Core/Systems/AbilitySystem/Effects/Editor/DashAttackVacateTests.cs`, 4 tests: a free cell is decided at once; a survivor is decided at once; a killed target is waited for; the wait ends at the limit.
- **Not verified in play:** whether this removes THJ's "Mark stays on 7,-3". It covers cause (b) from the 4.4 investigation, a late-leaving target. If the cause is a non-lethal preview with a hit that also doesn't kill, this changes nothing, and that would be correct.

### B. Core: the race damage-bonus listener comes off the event it was added to

`Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs` (BOM and LF kept): `Mark_Linda_ConsumeRaceDamage` now removes itself from `abilityPerformed`, the event `Mark_Linda_ApplyBonus` adds it to. Before, it removed itself from `abilityActivationStarted`, so a copy stayed on `abilityPerformed` after every race. One line plus a comment.
- Test `Core/Systems/AbilitySystem/Abilities/Editor/RaceDamageListenerTests.cs`:
  - setup: a bus as the current one, the handler holding a winner, the listener added to `abilityPerformed`;
  - a basic attack by the winner is raised;
  - checked: the listener count on `abilityPerformed` is back to where it was, and the winner is cleared. The count is read by reflection from UnityEvent's runtime call list.
  - The test fails against the old line.

### C. Feature: the Family Footrace result bark (every level)

- **Component:** new `Features/Player/Shared/Synergies/FamilyFootraceBark.cs`. It listens to `GlobalEventBus.onSynergyTriggered`; on id `"Mark-Linda Race"` (constant `RaceSynergyId`), the unit is the winner and `targets[0]` the loser.
  - The winner's line shows, then the loser's reply 0.6 s later, in the same popup and the same way as the arrow hand-back barks: a live speaker, `silenceBarks` respected, `DamageNumberManager.ShowText`, the `[PLACEHOLDER] ` tag stripped. The bark helper is copied from `GroundedArrowField.Pickup.cs`.
  - Lines (placeholder-tagged until THJ approves §13):
    - Linda wins: Linda "Too slow, little brother." / Mark "You started early.";
    - Mark wins: Mark "Patience climbs faster." / Linda "That one didn't count.".
    - No tie case.
  - Bus binding: it binds on enable and rebinds whenever `GlobalEventBus.Instance` changes (checked in `Update`; the bus can wake after the unit, and every level brings its own). It lets go on disable, and stops a pending reply. No static state.
- **Placement:** on **Linda's unit prefab only** (`Features/Player/Linda/Prefabs/Unit_Linda.prefab`), so it exists in every level she's in and a race is barked once. Mark's prefab doesn't carry it.
  - Added by a one-off editor step (load prefab contents, add the component, save).
  - Prefab diff: +17 lines. The added component, plus two `LindaQuiver` fields (`recallFlightColor`, `recallTrailWidth`) that the prefab hadn't stored yet; Unity wrote them at their code defaults when it re-saved. No change in behaviour.
- **Tests:** `Features/Player/Shared/Synergies/Editor/FamilyFootraceBarkTests.cs`, 8 tests:
  - the line choice for Linda, for Mark, and for anyone else (no bark);
  - the placeholder tag and the 0.6 s reply delay;
  - the id matches the string `UnitsCooperationHandler` raises (read from the source file);
  - only Linda's prefab carries the component;
  - binding adds one listener, binding twice adds no second one, unbinding removes it;
  - a new bus takes over and the old one is let go.

## Tests

| Run | Result |
|---|---|
| New tests (A, B, C) + `CastAbilitySequenceTests`, `EncoreApTests`, `M1RidgeTests`, `M1RidgeLayoutTests` | all passed (B's test re-run alone after a test-setup fix: 1/1) |
| Full EditMode suite | **2733 total, 2732 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |
| `AIRegressionTest.Baseline_MatchesCurrentAI` by name | **46**, the same lines as before (no new or lost line from the Linda prefab or the core changes) |

## Proposed commits (in this order)

1. **Encore free cast** (from round 4.4's fix; plain, shared): `feat(levels): scripted Self casts can leave the AP part of an ability's own check out`:
   - `Features/Levels/Sequences/IWaivableApCheck.cs` + `.meta`
   - `Features/Levels/Sequences/CastAbilitySequence.cs`, `Features/Levels/Sequences/Editor/CastAbilitySequenceTests.cs`
   - `Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`, `LindaQuiver.EncoreAp.cs`, `Editor/EncoreApTests.cs`
   - The M1 bits (`MissionWiring.Ridge.Sequences.cs`, `M1RidgeTests.cs`, `M1Ridge_Ambush_LindaCastRecall.asset`) go with the M1 commit.
2. **A, core:** `fix(core): a dash attack waits briefly for a killed target to leave its cell before deciding the hop`:
   - `Core/Systems/AbilitySystem/Effects/Runtime/AEffectDashAttack.cs`
   - `Core/Systems/AbilitySystem/Effects/Editor/DashAttackVacateTests.cs` + `.meta`
3. **B, core:** `fix(core): the Family Footrace damage bonus listener is removed from the event it was added to`:
   - `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`
   - `Core/Systems/AbilitySystem/Abilities/Editor/RaceDamageListenerTests.cs` + `.meta`
4. **C, feature:** `feat(bergsons): Linda and Mark tease each other when Family Footrace ends`:
   - `Features/Player/Shared/Synergies/FamilyFootraceBark.cs` + `.meta`
   - `Features/Player/Shared/Synergies/Editor/FamilyFootraceBarkTests.cs` + `.meta`
   - `Features/Player/Linda/Prefabs/Unit_Linda.prefab`

A, B and C don't depend on each other; the Encore commit is independent too. Not to stage: `miso.slnx`, `LevelM2-C1.prefab`, `M1Ridge_Cleared_PotionPage` (leftover, delete), `claude-handoff/`.

## Decisions I made

- **A:** the wait only happens when the victim is dead, gone or at 0 health. A survivor costs no extra time, so ordinary non-lethal Blitzes keep their pace. Scaled time, like the rest of the effect.
- **C:** placed on Linda's unit, not Mark's and not both, so one race gives one bark without a de-duplication rule. The race happens only when both are in the level anyway.
- **C:** bus rebinding is a cheap equality check in `Update` instead of the static `InstanceReady` event, which would need a static subscription.

## Risks and loose ends

- A's effect on THJ's 7,-3 case is unverified until a play. If it still happens, the temporary log suggested in the 4.4 report would tell which side (preview or vacate) it is.
- C's bark fires wherever Family Footrace is used (M1 and later missions), and every time; the lines don't play once only. §13 suggested `PlayOnce`. If THJ wants once per level or per save, that's a small follow-up.
- The four lines are placeholders, waiting for THJ (§13).

## Save reset

No. Play mode was never started.

## How to see it

1. **Footrace bark:** in any level with both siblings, after Family Footrace is unlocked (M1: after "Race you to the top."), use it.
   - If Linda gets there first: "Too slow, little brother." over Linda, then "You started early." over Mark about half a second later.
   - If Mark wins: "Patience climbs faster.", then Linda's "That one didn't count.".
   - With *silence barks* on in GlobalSettings, nothing shows.
2. **Race bonus listener:** run two Family Footraces in one level, each followed by the winner's basic attack. The bonus applies once per race and nothing stacks. Not visible as such; the edit-mode test covers it.
3. **Blitz hop:** on M1's family turn 1, Move Mark, then Blitz the ledge Claw (8 HP) from different starting tiles. Each kill should leave Mark on the Claw's tile (7,-2, block 8,3). A Blitz that doesn't kill leaves him beside the target, with no extra pause.
4. **Encore (from 4.4's fix):** in the ambush, after the potion page and the camera back on the family, Linda casts Encore with no AP and her grounded arrows fly back. If none are on the ground, there's one console warning and nothing else.

## Review (miso-reviewer, 4.5, 2026-11-25), pasted by the coordinator

**APPROVE** on all four (Encore free cast, Core A Blitz vacate wait, Core B race listener, Feature C Footrace bark). Should-fix (Core A): `AEffectDashAttack.cs:252-257` `IsVictimGone` treats a pushed-off living victim as gone, so Mark can wait 0.5 s and not hop if someone else steps on the cell → wait only for dead/destroyed/0 HP; add a test on a real unit state. Notes: report misdescribed line endings (files are CRLF; kept as they were); `IsInProgress` window up to 0.5 s longer if the owner is destroyed mid-wait (pre-existing pattern). Commit plan: merge the Self-cast and AP-waiver work into one `CastAbilitySequence` commit (CastAbilitySequence + tests, `IWaivableApCheck`, LindaQuiver files, EncoreApTests), before the M1 commit; A and B in their own commits; C its own.
