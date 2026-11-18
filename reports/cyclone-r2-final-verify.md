# Report: Cyclone round 2 final gate (C1..C4)

Plan: plans/2026-11-17-cyclone-round2-tech.md    Agent: miso-verifier    Branch: thj/cyclone (all work uncommitted)
Outcome: partial (quiet checks all pass; Play-mode criteria not run, THJ has not agreed a time)

## What changed

- Nothing. Verification only: no game file edited, no git write, Play mode not entered.

## Result

PARTIAL. Compile clean, EditMode 2114 run / 2113 passed / 1 failed (the known red only), C4 non-Play criteria pass against code and tests. In-game looks and live wiring are Not run.

## Compile

- Forced refresh with compile request through the Unity MCP, then Editor.log read after it: the latest reload (`Reloading assemblies after finishing script compilation`, log line about 145988) has no `error CS`. The 24 `error CS` lines in the log are all earlier in the session (around line 109000, a duplicate `HazardCells` in `CycloneOutcomeView`, already fixed).
- Compile warnings (`warning CS`): only `AssetOpener.cs` (CS0618) and `HelperOverlayPanel.cs` (CS0414), both outside Cyclone, Grid and AI runtime files and pre-existing. None from Cyclone, Grid or AI files.
- Console (errors and warnings after the refresh): only "Serialization depth limit 10 exceeded" warnings on Core types (`StatBackedValueBase`, `GTag.subTags`, via `RuntimeAbility._owner` and similar), "Objects are trying to be loaded during a domain backup", and test-run noise (`listener failed`, "reached its activation frame without targets", "Unsupported type Vector2f"). None name a Cyclone, Grid or AI file. The serialization-depth warnings are on Core serialized types, not on anything this branch's changes introduce by name (not diffed against HEAD; 371 such lines are in the whole Editor.log).

## Tests

- Full EditMode via Unity MCP: **2114 run, 2113 passed, 1 failed, 0 skipped**, 437 s.
- Only failure: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714  FAILURES: 43`** (read from the saved result file with Python; matches the expected count). It does not fail the gate.
- Matches the implementer's C4 fix-round figure (2114 / 2113 / 1).

## Acceptance criteria (C4, no Play mode)

- Pass: cross drawn as tint on the 4 touching cells plus one chevron per arm tip, no label, no streaks. Evidence: `CyclonePreviewTests` `Cross_TintsTheFourTouchingCells_ChevronsTheFourArmTips_AndWritesNoNumber`, `Cross_AtTheBoardEdge_DrawsOnlyTheCellsThatExist`, `ArmTips_AreTheFarCellOfEachArm_PointingBack` (all in the green run). `TouchLabel` and `WhirlHitTimes` no longer appear anywhere under `Lucy/Scripts` (grep empty).
- Pass: cross dims during Cyclone cast aim and Steer aim, drawn at the landing only during Steer. Evidence: `Cross_DimsAndHides_ByLook`, `AimState_DimsWhileAiming_MovesTheCrossToTheLanding_AndComesBack`.
- Pass: cast aim preview ghosts, tethers, damage on the ghost. Evidence: `CastPreview_GhostsForPulledEnemies_TheHitOnTheGhost_AndNothingLeftAfterwards`, `OutcomeView_CarriesTheHealthBarOverToTheGhost_AndPutsItBack`.
- Pass: Steer preview equals plan equals execution (one planner). Evidence: `CycloneSteerPreview.cs` calls `effect.PlanFor` (line 146) and `CycloneOutcomePlanner.ForSteer` (line 157); tests `SteerPreview_GhostsStandWhereTheExecutedSteerLeavesEveryone_AndTheHitMatches`, `SteerPreview_ACellPastABlockedFront_ShowsTheWayRoundThePlanTakes`, `SteerPreview_ToACellItCantReach_DrawsNothingButTheDimmedCross`, `PlanPulls_ReadsTheBoardItIsGiven`.
- Pass: preview removed on cancel, click, level end, unbind. Evidence: `SteerPreview_LeavesNothingBehind_WhenTheAimEnds` (4 cases).
- Pass: hit numbers 3 / 4 / 5 by Cyclone power. Evidence: `HitPreview_ThePrefabsHit_PreviewsThreeFourFiveByCyclonePower` (3 cases).
- Pass: cast preview attaches to each level's event bus once (the review's must-fix). Evidence: `CastPreview_IsPutOnTheLevelsEventBusOnce`; code in `CycloneCastPreviewAttach.cs` (AfterSceneLoad hidden DontDestroyOnLoad watcher, compares `GlobalEventBus.Instance` per frame, no static field so no `PlayModeStaticReset` hook needed). The live Preload > Home > level path is Not run.
- Pass: single burst length constant. `CycloneCrossView.BurstTime = CycloneEntity.BurstSeconds` (0.3).
- Pass: wobble rules. Evidence: five `Wobble_*` tests (path crosses only within the move, heavy qualifies, light never, family heavy never, spent or gone never).
- Pass: C4 test files hold the reported counts: 17 tests in `CyclonePreviewTests.cs`, 7 in `CycloneSteerTests.Preview.cs` (attribute count by grep; includes TestCase variants).
- Not run: needs a play session: first-frame draw when the cursor already rests on a cell; preview survives the player's hover refresh; health panel offset onto a ghost; wobble motion and pip flicker; visual look of tint, chevrons, tether, hazard ring; cross dim when End Turn is pressed mid-aim.

## Bugs found

None.

## Save reset

No.

## Editor checks corrections

- Confirmed: `get_test_job` for the full suite times out or reports "plugin session disconnected" several times (domain reload and test host); retrying with `wait_timeout` works. The final result (about 61k characters) is saved to a file instead of returned, and `result.summary` plus `progress.failures_so_far` hold the counts and failure name; the AI inner count is in the failure message. Full run takes about 7 to 8 minutes now (437 s for 2114 tests), not about 10 s.
- `refresh_unity` with `compile: request, mode: force` returns at once; I read the Editor.log after it for the latest reload rather than the console.

## Remains for THJ's play check

From `playtests/2026-11-17-cyclone-round2-play-check.md` (sections: Cross drawing, Cast aim preview, Steer aim preview, Carry and the closing Whirl, Heavies, Numbers and texts, Known gaps). Everything in it is Not run. Priority points:

1. The cast preview appears at all in the normal flow (Preload > Home > level), the one thing the review flagged.
2. Steer aim: first-frame draw with the cursor already on a reachable cell, preview staying drawn while hovering enemies, health panel moved onto a ghost and put back, orange hazard ring, End Turn mid-aim restoring the cross.
3. Cross look (tint, chevrons, no label), cross dimming and landing cross.
4. Wobble and pip flicker with a Masher or the Goblin Queen headed through the Cyclone.
5. Carry and closing Whirl, heavies (C1 to C3c) and the numbers and texts sections.

## Risks and loose ends

- The C4 hunks in shared files (`CycloneEntity.cs`, `CycloneRules.cs`, `CycloneSteerPreview.cs`, `CycloneWhirlPlanner.cs`) are mixed with earlier uncommitted chunks, so the commit split needs care (see the C4 report).
- Do not stage `PreloadScreen.unity`, `ProjectSettings/*` or the TMP fallback font.

## Docs to update

- `tech/editor-checks.md`: the suite timing and retry notes above.

## Proposed commits

None (verification only).

## Other branches

None.

## How to see it

1. Test Runner > EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 714 / 43).
2. Then the play check file above.
