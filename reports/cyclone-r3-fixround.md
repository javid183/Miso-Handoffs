# Report: Cyclone round 3 fix round (C2 and C3 review items)

Plan: none (fix round from reviews cyclone-r3-c2-review.md, cyclone-r3-c3-review.md)    Agent: miso-implementer    Branch: thj/cyclone
Outcome: done

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/Scripts/` (LF kept):
- `Editor/CycloneCastOnEnemyTests.cs`: the preview test now drives the real `CycloneCastPreview` (its private `Preview` with caster, spawner, prefab copy and range set as target selection leaves them) and compares each ghost cell with `plan.LandingOf(claw)`, the hazard ring, then runs `ShoveThenCast` and checks the unit's cell is that same landing. No hard-coded landing. New test `ACastKilledMidShove_DoesNotLeaveTheNextCastStuckInProgress`.
- `Cyclone/AEffectCycloneSpawner.cs`: `ApplyUnguarded` sets `IsInProgress = false` first (C2 #2); one-line comment in `TryCollectTargetSelectionCells` (C2 #3).
- `Cyclone/AEffectCycloneSpawner.Shove.cs`: "glide" comments and the local `gliding` renamed to fling/`flinging`; header rewrapped.
- `Cyclone/ICycloneShoveSteps.cs`: "glide" comment to "fling".
- `Cyclone/CycloneEntity.Steer.cs`: removed the `SteerSecondsPerCell` property. The serialized field `steerSecondsPerCell` stays: it is still read by the Steer's loop (and the prefab has no serialized override).
- `Cyclone/CycloneWhirlSteps.cs`: removed unused `using` MISO.Core.Systems.AI and MISO.Core.TagSystem. `Cyclone/CycloneCastPreview.cs`: removed MISO.Core.TagSystem and MISO.Core.Units.Factions. `Cyclone/ICycloneWhirlSteps.cs`: removed `using UnityEngine;`. (Compiles clean, so they were unused.)
- `Editor/CycloneWhirlInputLockTests.cs` (new, 3 tests, Unity makes the `.meta`): real `CycloneWhirlSteps.HoldInput`: hold twice locks and one release unlocks; another owner's lock survives; release after the controller is destroyed does not throw.

Untouched: `MasherCounterCycloneTests.cs`, THJ's uncommitted files, core files.

## Acceptance criteria

- [x] C2 #1: real preview driven; fails if the preview stops passing the shove to `ForCast` (the shoved enemy would have no ghost). Covered by EditMode test.
- [x] C2 #2: covered by the new test (the routine is dropped mid-shove, the next `ApplyUnguarded` starts clean).
- [x] C2 #3, C2 #4, C3 #1, #2, #3: done as asked.
- [x] C3 #4: covered by the three input lock tests.

## Save reset

no

## Decisions I made

- C2 #2: put the reset in `AEffectCycloneSpawner.cs` (where the `ApplyUnguarded` override lives), not the Shove partial.
- The preview test calls the private `Preview` by reflection and uses an instantiated copy of the prefab with its hit effect cleared, because the test units have no health attribute for the damage preview. The shove and Whirl planning are unchanged.
- C3 #4 went in a new test file rather than appending to an existing one.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- The test calls private members of `CycloneCastPreview` by name (`Preview`, `_view`, `_range`, `_caster`, `_spawner`, `_prefab`); a rename breaks it loudly.
- Full EditMode: 2160 run, 2157 passed, 1 skipped (the ignored repro), 1 failed: AIRegressionTest.Baseline_MatchesCurrentAI (43 failures, as known). One unrelated GridToLevelCameraStartTests case failed once with a Unity internal lock-count assertion during the full run (the editor reconnected mid-run) and passed on its own rerun.

## Proposed commits

1. `test(lucy): the cast-on-enemy preview test drives the real preview; the Whirl input lock has tests`: `Editor/CycloneCastOnEnemyTests.cs`, `Editor/CycloneWhirlInputLockTests.cs` + `.meta` (plain)
2. `fix(lucy): a cast killed mid-shove can't leave the Cyclone cast stuck in progress; comment, wording and unused usings cleanups`: `AEffectCycloneSpawner.cs`, `AEffectCycloneSpawner.Shove.cs`, `ICycloneShoveSteps.cs`, `CycloneEntity.Steer.cs`, `CycloneWhirlSteps.cs`, `CycloneCastPreview.cs`, `ICycloneWhirlSteps.cs` (plain)

Caution: several of these files also carry THJ's other uncommitted Cyclone changes in the working tree; check the diff before staging.

## Other branches

none

## How to see it

1. Test Runner > EditMode > run `CycloneCastOnEnemyTests` and `CycloneWhirlInputLockTests`.
