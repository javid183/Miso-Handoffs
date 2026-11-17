# Review: Cyclone round 2, C1 (branch `thj/cyclone`, uncommitted)

Reviewer: `miso-reviewer` (saved by the coordinator; the reviewer has no Write tool). Verdict: **FIX**. EditMode not run when reviewed.

## Must fix

1. **A Steer's Whirl stalls 15 s before its hit, and Watch fires after the hit.** `AEffectCycloneSteer.cs:78-86` with `CycloneEntity.Whirl.cs:116-122` and `CycloneWhirlSteps.cs:72-80`. `WaitForSteer` keeps the Steer effect `IsInProgress` until `IsSteering` is false, which is now the end of the whole Whirl. `AbilityPreset.ApplyMapped` (`AbilityPreset.cs:144`) waits on that flag, so Lucy's action stays open. The Whirl's reaction wait needs no action in progress, so it only exits on `ReactionTimeoutSeconds` (15 s) on every Steer, and Family Roles answer "once Lucy's action is done", so Watch reacts after the hit, breaking "pull, reactions, hit". Tests miss it because the recorder fakes `ReactionsSettled`.
   Fix: as the cast does (`AEffectCycloneSpawner.HoldCastWhileWhirlPulls`), close the Steer action once the Whirl's pull is done and keep `IsSteering` true to the end, e.g. `WaitWhile(() => cyclone && cyclone.IsSteering && (!cyclone.IsWhirling || cyclone.IsPulling))`. Put the predicate in a plain helper (e.g. `CycloneSteerRules.SteerActionOpen(isSteering, isWhirling, isPulling)`) and test it: open while gliding and pulling, closed in the reaction and hit phase, closed after an abort. Update the class comment at lines 17-18; the report's risk item 63 ("still true") is wrong.

## Should fix

1. `CyclonePower_HitIsThreeFourFiveTimesDamage` (CycloneSteerTests.cs, ~600-628) checks the data, not the game: it re-multiplies `baseFactor` by the YAML factor. Drive the real path (`StatBackedEvaluationProbe.SimulateFromSerialized` with the Lucy prefab and Bergsons faction, or a `RuntimeAbility` at upgrade level N) and assert the resolved factor and `NormalizeValueChange` give 3 / 4 / 5; at least also assert the bound max is at least 5 and the health change is integer. By hand the values are right (3 x 1.333333 = 3.999999 and 3 x 1.666667 = 5.000001 round to 4 and 5; Bergsons `StatUB_DMG` is 9999; with a crit levels 2 and 3 come to 6 and 8).
2. `TheSteersHit_IsCreditedToTheCast_NotToTheSteerAsAnAction` (~574-590) is mostly static asset facts; rename or trim it, or assert the recorder's reported source.
3. Unused usings after the Gust removal: `CycloneSteerSteps.cs` (`MISO.Core.Management`, `MISO.Core.Units`), `ICycloneSteerSteps.cs` (`MISO.Core.Units`), `CycloneEntity.Steer.cs` (`MISO.Core.Systems.AbilitySystem.Effects`, `MISO.Core.Units`, likely).
4. Reflow two over-long comment lines: `CycloneEntity.Whirl.cs:15` and the header comment of `CycloneSteerTests.cs` (~20).

## Notes

- Hold, abort and Dispose are correct as written (one owner for the hold; nested try/finally; Dispose deferral; `NotifyReadyChanged` once). Unity does not run a coroutine's `finally` on `StopCoroutine` or destroy, so the inner Dispose helps only manual drivers such as tests; in game the level end and `CombatLevelRunHandler.OnDestroy` clear the holds.
- Howling Gale is shared through `steps.Hit`; Weak lands only on enemies hit. Credit and the Masher classification are the shared, unchanged path.
- No "Gust" left in `Assets/` except a third-party font glyph table. No private IDs, no new statics, no `Core/` change, BOM and CRLF kept, file list matches the diff.
- Stray legacy copy: `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/` holds an unreferenced old `Lucy_Cyclone_Ability.asset` and `Lucy_Cyclone_Effect_AttrMod.asset` (baseFactor 10, old factors). Backlog line, not C1 scope.
- AI regression count should stay 43; needs measuring. After the fix the play check should time a Steer (no long pause before the hit) and confirm Watch fires before the hit.

## Re-review (fix round): APPROVE

Saved by the coordinator. No must-fix. The must-fix is resolved: `CycloneSteerRules.SteerActionOpen(isSteering, isWhirling, isPulling)` is `isSteering && (!isWhirling || isPulling)`; every path traced (glide, Whirl start, pull done, no pulls, pull timeout, abort, Cyclone destroyed); `IsSteering` still runs to the end so Dispose stays deferred. The Cyclone Power test now uses `AAttributeModifier.ModifyWithPolicyBasic`, the engine's own step; it leaves out other stat sources, the `StatUB_DMG` bound and crit (reviewer's hand check: 3 / 4 / 5, crits 6 / 8 at levels 2 and 3); moving it to `StatBackedEvaluationProbe` is a later improvement. Credit test is fine. Usings and BOM/CRLF fine. Nit: rewrap the class comment at `AEffectCycloneSteer.cs:17-20`. EditMode still not run. Play check after C4: time a Steer (no long pause before the hit) and confirm Watch fires on a pulled enemy before the hit.
