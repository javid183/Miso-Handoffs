# Report: Steer Whirl hits the enemies it passed

Plan: none written (S-size rule change from the coordinator, chunk 1.9; decision D-648, reverses D-583)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`. None is a core file; `CombatLevelRunHandler.ReportDamageOutsideAbility` and the Masher's Whirl-hit rule were not touched.

- `Cyclone/CycloneEntity.Steer.cs`: the closing Whirl is started with `WhirlRoutine(holdOwnerSource, KnockLanded)`, no skip list. The pass hits, the knock, routing and the log are unchanged (`hitOnTheWay` still feeds the Steer log line). Header comment updated.
- `Cyclone/CycloneEntity.Whirl.cs`: removed the `skipHits` parameter of `WhirlRoutine` and the skip logic of `HitTargets` (only the Steer used it). Whirls from a cast or the end of a turn are unchanged.
- `Cyclone/CycloneOutcome.cs`: the preview's Whirl no longer filters out passed enemies, so `Hit` now includes a passed enemy that ends up beside the stop. `HitCount` already added pass + knock + Whirl and `AllHit` already listed each unit once, so `CycloneOutcomeView` shows the summed damage in the enemy's one segment (the skull comes from the health bar's own check). Comments updated. The cast preview needed no change (a cast has no passed enemies).
- `Cyclone/CycloneSteerPreview.cs`: comment only.
- Tests: see below.

## Acceptance criteria

- [x] Passed enemy beside the stop takes the pass hit then the Whirl hit: `WhirlOnPassed_APassedEnemyBesideTheStop_TakesThePassHitThenTheWhirlHit`, `WhirlOnPassed_APassedEnemyThePullBringsBesideTheStop_TakesBothHits`.
- [x] Knocked enemy unchanged (two hits): existing knock tests pass untouched; `WhirlOnPassed_AKnockedEnemyStillTakesTwoHits_AndAPassedOneBesideTheStopToo`.
- [x] Passed enemy outside the Whirl takes only the pass hit: `WhirlOnPassed_APassedEnemyOutsideTheWhirl_TakesOnlyThePassHit` and the preview case below.
- [x] Previews agree with the execution: `WhirlOnPassed_Preview_ShowsBothHitsOnAPassedEnemyBesideTheStop_AndEqualsTheExecution` and `WhirlOnPassed_Preview_ShowsOnlyThePassHitOnAPassedEnemyOffTheArms_AndEqualsTheExecution` (both use `PreviewThenExecute`, which compares the executed hits with the outcome's hit counts), plus the updated existing preview tests (damage 6 = two hits summed).
- [x] Old one-hit assertions updated, new tests added (below). A passed enemy the pass hit kills gets no Whirl hit: `WhirlOnPassed_APassedEnemyThePassHitKills_TakesNoWhirlHit`.

## Chunks

### Chunk 1: Whirl on passed enemies

- Changed: the four source files above and three test files.
- Tests changed (all in `CycloneSteerTests`; each asserted "a passed enemy is never hit by the Whirl", the removed rule):
  - `.Knock.cs`: `OnTheWay_EachEnemyIsHitInPathOrder_AsTheCycloneReachesItsCell_AndTheWhirlHitsTheOneBesideIt` (renamed; now First, Second, Second, 3 reports, Whirl log 1 hit); `TheGlide_FollowsTheRouteRoundTheCorner_...` (passed enemy pulled beside the stop is hit twice; the hit-position check records only the first hit); `OnTheWay_AHeavyIsHitOnTheWayAndByTheWhirlBesideIt_AndStays` (renamed); `ThePlanIsWhatHappens_EveryEnemyHitAsOftenAsItsCircumstancesSay` (renamed; Passed now hit twice). File header comment updated.
  - `.Preview.cs`: `SteerPreview_EqualsTheExecution_ForAClawAboveWithTheFamilyAround` (second Claw is in both PassHit and Hit); `..._APassedEnemyThatIsNotPulled_..._WithBothHitsSummed` and `..._APassedEnemyThePullMoves_..._WithBothHitsSummed` (renamed; Hit contains the passed enemy, damage 6).
- New: `Editor/CycloneSteerTests.WhirlOnPassed.cs` (+ `.meta`), 7 tests, cases under acceptance.
- Results: `MISO.Core.Features.Bergsons.EditorTests` (Cyclone/Lucy and the rest of that namespace) run through the Unity MCP: 957/957 pass. The first run after the code change had 11 failures: 7 were the old-rule assertions above, 4 (`SteerPreview_LeavesNothingBehind_WhenTheAimEnds`) were leftovers from the failing tests and passed once those were fixed. Full suite and AI regression not run, as instructed.
- Decisions and loose ends: removed the unused `skipHits` parameter instead of leaving it dead (same behavior, no other caller). Howling Gale and cast credit need no change: the Whirl hit goes through the same Hit and Report path, as for the knocked enemy.

## Save reset

no

## Decisions I made

- Removed `skipHits` from `WhirlRoutine`/`HitTargets` instead of passing null.
- The Steer log line still says "hit N on the way" and lists pass + knocked targets; the Whirl's own line now also counts the passed enemies it hits. Left as is.

## Needs THJ

none

## Docs to update

`design/gdd/characters/lucy.md` (designer's file, not edited by me):
- LU-4 step 3 (Hit): replace the last sentence ("After a Steer, the Whirl skips the enemies that Steer already hit on its way (LU-6).") with: "After a Steer, the Whirl also hits the enemies the Steer passed, if they end up beside it: they take the pass hit and then the Whirl's hit (LU-6)."
- LU-6 item 4: keep the pass rule; append "The closing Whirl may hit it again (item 6)." and replace the D-583 cite with D-648.
- LU-6 item 6: replace "Its hit skips every enemy hit on the way (it can still pull one in), and hits the knocked enemy again. So a Steer hits every enemy it passes or leaves beside it once, and the knocked enemy twice." with: "Its hit lands on every enemy beside the Cyclone after the pull, the enemies passed on the way and the knocked enemy included. So a passed enemy that ends up beside the stop (already there or pulled in) takes two hits, the pass hit and the Whirl's, like the knocked enemy; a passed enemy left outside the Whirl takes one; one the pass hit kills takes no more."
- LU-6 aim preview: "(the knocked enemy's two hits summed in one)" becomes "(an enemy's several hits, such as the knocked or a passed enemy's two, summed in one)".
- `plans/2026-11-19-cyclone-reset-tech.md` line 36 (one hit per enemy per Steer) is superseded; coordinator to note.

## Risks and loose ends

- Balance: a Steer through a line of enemies that ends beside several of them now deals up to double on those; THJ judges at the play check.
- No new presentation code: the Whirl's breath and hit simply have targets in more Steers.

## Proposed commits

1. `feat(lucy): the Cyclone Steer's Whirl also hits the enemies it passed`: the four `Cyclone/*.cs` files above, `Editor/CycloneSteerTests.Knock.cs`, `Editor/CycloneSteerTests.Preview.cs`, `Editor/CycloneSteerTests.WhirlOnPassed.cs` and its `.meta` (plain, not core). One commit: the tests only pass with the code.

## Other branches

none stated (applies to all per the request; coordinator decides whether `main` needs it).

## How to see it

1. Open a level with Lucy and a few enemies. Cast the Cyclone on a free cell, with one enemy A in a straight line from it.
2. Steer so the Cyclone passes A and stops on the cell right after A (A is then beside the stop), or two cells past A (the Whirl pulls A in beside the stop).
3. Aim first: A's damage preview shows two Cyclone hits summed (twice the single-hit number you see on an enemy that is only hit once, e.g. a Whirl-only enemy), with a skull if that kills.
4. Click: A takes a pass hit as the Cyclone enters its cell, then the Whirl hit after the breath; the two total the preview.
5. Route that turns (right through A, then up one): A ends diagonal to the stop, is not pulled and takes only the pass hit; the preview shows a single hit.
6. The knocked enemy still takes two hits (knock, then Whirl).

## Review (miso-reviewer, 2026-11-24)

Verdict: APPROVE.
- Not a core change (Cyclone feature files and tests only).
- Preview equals execution: the planner drops its passHit filter just as execution drops skipHits; both preview tests check it with PreviewThenExecute.
- Knocked enemy unchanged; dead units skipped (IsAlive check in the Whirl loop, gone-set in the planner; test covers it).
- No callers of skipHits remain.
- LF/no BOM kept, no private IDs, no statics.
- Should fix: CycloneSteerPreview.cs header comment, edited line (~21) is overlong; re-wrap.
