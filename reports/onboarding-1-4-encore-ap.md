# Report: Chunk 1.4, Encore's 2 AP

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.4, decision D-609)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done

## What changed

- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/RecallRules.cs`: `HasAp(points, apCost)` and a `CanRecall` overload that also needs the AP.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.EncoreAp.cs` (+ `.meta`, new partial): `EncoreAp` reads the unit's AP left and Encore's cost (found from the unit's own abilities, never hard-coded; the shared-pool factor comes through `APConsumer.GetActionCost`), plus a test seam.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`: `HasGroundedArrows` also requires the AP.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverTextRules.cs`: `NeedsAp(cost)` placeholder line ("[PLACEHOLDER] Needs 2 AP") and `GreyReason` takes optional `points` and `apCost` (defaults ask for nothing, so existing callers and tests are unchanged). Order: no grounded arrows, quiver full, then needs AP.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverAbilityInfo.cs`: `GreyReason` passes the AP values to the text rule.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreApTests.cs` (+ `.meta`): new tests.

No core file changed (`ActionPoints`, `APConsumer`, `RuntimeAbility` untouched). The ability asset is untouched (still "(2 AP)", `apConsumptionType` 2).

## Acceptance criteria

- [x] (1) At 1 AP Encore is greyed with a reason and can't be cast: `Active` ANDs `CheckActivationFeasibility`, which sends `HasGroundedArrows`; it now returns false below the cost. Tests: `TheFeasibilityCheck_BlocksAtOneApAndAllowsAtTwo` (real field with a grounded arrow, quiver with room), `GreyReason_NamesTheCostWhenTheApIsShort`, `HasAp_NeedsTheFullCost`, `CanRecall_AlsoNeedsTheAp`. The tooltip reads the same values, so greyed and reason agree.
- [x] (2) With 2 or more AP and grounded arrows it works as before: same test, cost and cost+2 return true; `GreyReason` returns null at the cost. The cost taken is unchanged (ability's own cost).
- [x] (3) Text still says "(2 AP)": `Encore_CostsTwoApAndTheTextSaysSo`, plus the existing `RecallAbility_IsTwoApCooldownTwoSelfCast`.
- [x] (4) EditMode tests cover (1) and (2): `EncoreApTests` (new, 14 cases).
- [x] (5) Quiver fixtures pass: `QuiverWiringTests`, `QuiverReadabilityTests`, `QuiverSwitchTests`, `RecallRulesTests`, `EncoreApTests` all green (run with the two Onboarding fixtures: 95 of 95).
- Full EditMode suite: see "Reviews and checks".
- Needs the verifier's play check: a real Linda at 1 AP in the Hearth (greyed, tooltip line, not castable) and at 2 AP (casts, costs 2). The tests fix the AP numbers by a seam; they don't run a real `APConsumer`.

## Chunks

### Chunk 1.4: Encore's 2 AP

- Changed: see "What changed".
- Criteria met: see above.
- Decisions and loose ends: see below.

## Reviews and checks

- Full EditMode suite: first run 2512 tests, 2510 passed, 1 skipped (the Explicit AI test), 1 failed: `GridToLevelXpTests.Build_XpNoneLeavesPlacedEnemiesAtZeroAndTheEnemyPrefabUnchanged` ("m_LockCount == 0" from `PrefabUtility.UnloadPrefabContents`; the Unity MCP session dropped during that run). The same fixture passes alone (6 of 6). Unrelated to this change. A second full run: 2512 total, 2511 passed, 0 failed, 1 skipped (Explicit AI test).

## Save reset

no

## Decisions I made

- The AP check sits in `HasGroundedArrows` (the feasibility check Encore already names), as the plan said. The message carries no ability, so the quiver finds Encore among its unit's abilities with the existing `QuiverAbilityInfo.IsRecall` and reads the cost from it. Cached after the first find.
- Points and cost are compared with `APConsumer.Points` and `GetActionCost`, so the same check is right in the shared-AP mode (where core already compares the pool to the cost) and in the PerUnit mode (where core only asks for more than 0).
- Unknown cost or no unit (a quiver that never woke) means no AP requirement, so prefab checks and tests that build a bare quiver behave as before.
- The "Needs N AP" line also shows when the unit has 0 AP; that is true and cheap, not a separate case.

## Needs THJ

none

## Docs to update

- Placeholder line "Needs 2 AP" for the narrative agent: `QuiverTextRules.NeedsAp`.

## Risks and loose ends

- The AI worker thread: `HasGroundedArrows` is reached from `RuntimeAbility.Active`, which the AI brain reads (`AIUnitBrain` checks `a.Active` for its own unit's abilities). The new code only reads plain values (`_unit is null` check, `APConsumer`, `AbilityOrchestrator.AllAbilities`, `Parameters`), no `GetComponent`, no Unity `==`.
- Does the AI use Encore? No: Encore appears in no AI graph or AI ability asset (only in its own ability and effect assets), and Linda is player-controlled. If an AI unit ever used it, at 1 AP it would now not offer it (the same as the fix intends). So `AIRegressionTest` was not run, as agreed.
- The old behaviour was only reachable in the PerUnit AP mode; in the shared mode core already compared the full cost.
- `GroundedArrowField.Recall.cs` uses the old three-argument `CanRecall` at cast time; left alone (the activation check already gated it).
- Noticed, not changed: nothing else.

## Proposed commits

1. `fix(linda): Encore needs its full AP cost left, and its tooltip says so` (plain):
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/RecallRules.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.EncoreAp.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverTextRules.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverAbilityInfo.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreApTests.cs` + `.meta`

## Other branches

none

## How to see it

1. Open `Scenes/PreloadScreen.unity`, start a level with Linda (the Hearth memory 1 or any combat level) in the PerUnit AP mode.
2. Land an arrow, then spend AP until Linda has 1 left: hover Encore. It is greyed and its tooltip ends with "Needs 2 AP". Clicking does nothing.
3. With 2 or more AP, Encore is usable and takes 2 AP; the tooltip text still says "(2 AP)".

## Coordinator check (2026-11-23)

Size S, outside core: no reviewer (gate 3). Read the diff: the cost is read from the ability (`GetActionCost`), the cached `RuntimeAbility`, `APConsumer` and `AbilityOrchestrator` are plain C# classes (no Unity `==` on the worker thread), and `ActionPoints`/`APConsumer` are untouched. Accepted. A real 1 AP / 2 AP check goes into THJ's batched Phase 1 play check.
