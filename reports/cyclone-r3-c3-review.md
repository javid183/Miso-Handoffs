# Cyclone round 3 C3: review

Reviewer: miso-reviewer (text saved by the coordinator). Verdict: **APPROVE**. Must fix: none.

Verified: order unchanged (landings, pull, reactions, hit; one Steer landing after the fling); only pullable 1x1 units lean, moved units skip the inhale, no breath/swell/lock with no targets; swell 0.1 s only before a pull; burst check and targets re-taken after the exhale (the two tests would fail on old code); input lock via the public `AddInputLock/RemoveInputLock` with one cached owner, released at the hit, on early stop, in `finally`, and in `CycloneEntity.OnDisable`; stacks safely with banner/tutorial/mission-end locks; pause blocked during the breath; no core file changed; lean/recoil move the `Visual` child, drag and fling move the root (as round 2's glide did); durations 0.202 / 0.302 / +0.2 / 0.121 s match; only asset change is `swellSeconds` 0.1; LF, no BOM, no private IDs, no new statics.

## Should fix (the fix round)

1. `CycloneEntity.Steer.cs:24`: remove `SteerSecondsPerCell` (no caller).
2. `ICycloneWhirlSteps.cs:5`: remove the unused `using UnityEngine;`.
3. Comments still say "glide": `ShoveThenCast` summary, `ICycloneShoveSteps.DeltaTime`, and rewrap the long header line (~14) in `AEffectCycloneSpawner.Shove.cs`.
4. No test covers the real `CycloneWhirlSteps.HoldInput`. Add one in `Core/Interactions/Editor/InputLockTests.cs` pattern: hold(true) twice locks, hold(false) unlocks, another owner's lock survives, release after the controller is destroyed does not throw.

## Notes

- Input guard: the plan said STOP if the guard needs a core file; it used the public lock API with no core edit. Coordinator confirmed at Tier 2 (D-569).
- The 0.06 s recoil runs after the hit, so the Whirl and its turn-switch hold end 0.06 s later whenever anyone recoils: a turn-end Whirl with a pull waits +0.16 s, not +0.1 s. Put on THJ's pace check.
- Shove loose end (low risk): if Lucy's coroutine dies mid-fling, the shoved enemy's root and hop offset are not restored (only a scene teardown does that).
- Rare Steer path: if `CanEndOn(end)` fails after the fling, riders snap back (visual only).
- Play check still needed: lean depth and feel, click-blocking during the breath, round 2 item 25, level end mid-beat. The cross view's own swell still eases over its 0.2 s constant (C1's file).
