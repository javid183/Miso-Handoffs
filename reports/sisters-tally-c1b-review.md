# Sisters' tally C1b: review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Three should-fix.

## Should fix

1. `SistersTallyListener.cs:174`, `:236`: `_countedByDuo` is cleared only on a level change, so a revived enemy the Duo counted can never count again. Remove the unit from it in `OnUnitBorn` before `RecordDeployed`; add a test. (Only player units are resurrected today, `CombatLevelRunHandler:711`.)
2. `SistersTallyTests.Attribution.cs:257` `Level_StaysEligibleWhenASisterFalls` can't fail (nothing reads deaths for eligibility). Make it real (sister `unitDied` then a John `unitBorn` keeps it eligible) or drop it.
3. `SistersTallyTests.Attribution.cs:312`: the Hearth asset test checks only the unit's own active flag; a sister under an inactive hidden-group parent would read as deployed. Treat a unit as placed only when it and every parent up to the level root are active.

## Notes (verified)

- Bracket opens for any Duo with a sister (`UnitsCooperationHandler.Execute:481` names every partner); `AEffectCoOpTrigger` holds the trigger until `ExecuteIE` ends, `abilityPerformed` after `holdTimeAfterActionCompletion`; the trigger's report (`CombatLevelRunHandler.OnAbilityComplete`) and the close can arrive in either order, safe because CoOp-trigger reports are always ignored. Partner abilities raise no damage events. Splits, `FakeDie`, spawner deaths never reach the minimum. `turnEnded` close can't cut off a Duo.
- Eligibility: `levelStarted` after roster slots filled; revealed units arrive via `RegisterUnit` → `unitBorn`. No roster placeholder in the Hearth levels.
- Re-enabling the source mid-level would leave the level ineligible (`Connect` resets, `levelStarted` doesn't re-fire); nothing does that today.
- Accepted risk (design): any other enemy death inside the bracket (burn tick, hazard, ally passive, death explosion during the hold) counts for the Duo's sisters.
- ATB: turn-end safety close may not fire per unit; the main close still works.
- Real `IsDuoTrigger`, `IsEnemyOfPlayer`, `DeployedPlayerUnits` are not covered by EditMode (fakes): play check needed.
- Scope reaches beyond the Hearth: M1 `Level1-C2` now shows the tally (coordinator decided to leave it, D-452; THJ told); one-sister test levels hide it.
- Diff = 5 modified + new `SistersTallyTests.Attribution.cs` (+ `.meta`); prefab change only `excludedMissions: []`, LF kept; no private IDs; no new statics; listeners symmetric. Single commit right.
