# Cyclone round 3 C2: review

Reviewer: miso-reviewer (text saved by the coordinator). Verdict: **APPROVE**. Must fix: none.

Verified: diff matches the report's file list; no core file touched; LF, no BOM, no private IDs, no new statics. Direction on the larger axis, tie tries row then column; refusals (wall, edge, unit, walk-blocking or stashed entity, planted entity on the cell, heavy/Immovable/large, neutral/ally/family); adjacent cells allowed; `CanShoveFront` is the Steer's expression extracted unchanged; one-argument `IsValidCastCell` untouched; worker-safe plain references; preview and execution both call `CastShoveFor`; abort restores unit and drawing in `finally`; the renamed Steer test is legitimate.

## Should fix (one fix round, after C3 because C3 edits the same files)

1. `CycloneCastOnEnemyTests.ThePreview_ShowsTheShoveTheCastMakes_ThenTheWhirlOnTheBoardItLeaves` (~485-529) rebuilds the preview by hand: it never runs `CycloneCastPreview` and the execution half is circular (hard-coded landing, plan handed to the routine). Compare `plan.LandingOf(claw)` with the unit's cell after the run and drive the real preview or `ApplyUnguarded` with the recorder.
2. `AEffectCycloneSpawner.Shove.cs:76-136`: `IsInProgress` is an instance field on a ScriptableObject; if the coroutine is killed, `finally` does not run, and with domain reload off the stale true hangs `AbilityPreset.Activate`'s `WaitWhile(IsInProgress)` next session. Set it false at the top of `ApplyUnguarded` or reset it via the play-mode reset hook.
3. `AEffectCycloneSpawner.cs:36-48`: `TryCollectTargetSelectionCells` bypasses `ProxySelectionOwner` and `IgnoreRelationOnSelection` (both off on the asset). One-line comment saying the provider assumes neither is set.
4. Remove the unused `using` lines in `CycloneWhirlSteps.cs` and `CycloneCastPreview.cs`.

## Notes

- Range highlight: only accepted cells are lit now (family, ally, planted, stashed, other occupied cells no longer). Put on the play-check list for THJ; easy to narrow.
- `IsPullableBy` treats a null `TagSet` as pullable (before: threw). No golden-master change expected (count 43).
- Watch and "no Crippled damage" covered structurally only; play check needed.
- For C3's review: `gliding` and `offItsCell` must still cover the fling; C3 replaces only the glide loop in `ShoveThenCast`.
