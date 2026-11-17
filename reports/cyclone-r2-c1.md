# Report: Cyclone round 2, C1 (Steer ends in a Whirl; one rule; Cyclone Power)

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C1)    Agent: miso-implementer    Branch: thj/cyclone
Outcome: partial (code and tests written; both assemblies compile clean in an offline Roslyn check; the EditMode suite was NOT run, see "Needs THJ / coordinator")

## What changed

All under `miso/Assets/_Project/`.

- `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Steer.cs`: `GustRoutine`, `GustStreakSeconds` and `LastGustPulled` removed. `SteerRoutine(path, holdOwnerSource = null)` now runs the full `WhirlRoutine(holdOwnerSource)` after the move; `TrySteer` passes `CombatLevelRunHandler.Instance`. The inner Whirl is disposed in a `finally`, so a stopped Steer ends its Whirl and releases its hold.
- `CycloneEntity.Whirl.cs`: `StartPulls` loses the `started` list (only the Gust used it); the Whirl's final `NotifyReadyChanged` is skipped while a Steer is still running (the Steer announces ready once, at its own end); passes `carried` 0 to the log; header comment updated.
- `ICycloneWhirlSteps.cs` / `CycloneWhirlSteps.cs`: `Log(int carried, int pulled, int hit, GUnit[] targets)`.
- `CycloneRules.cs`: `WhirlLogDetail(carried, pulled, hit)` gives "carried N, pulled N, hit M".
- `CycloneSteerSteps.cs` / `ICycloneSteerSteps.cs`: `LogGust` and the `"Gust"` log id removed.
- `CycloneSteerRules.cs`: `GustLogDetail` removed.
- `AEffectCycloneSteer.cs`, `CycloneSteerPreview.cs`, `CycloneWhirlPlanner.cs`, `CycloneWhirlSteps.cs`: "Gust" wording in comments replaced.
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`: `Stat_DMG` upgradeLevels factors 1.2 -> 1.333333 and 1.4 -> 1.666667 (two lines). With the hit's `baseFactor` 3 and Stat_DMG 1 this is 3 / 4 / 5 (3.999999 -> 4, 5.000001 -> 5). Hit effect asset unchanged.
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`: recorders updated; the three Gust tests replaced by Steer-Whirl tests (below).
- `Features/Player/Lucy/Scripts/Editor/CycloneWhirlTests.cs`: recorder and the log assertion take `carried` (expects `(0, 1, 2)`).

Nothing in `Core/` touched. No new statics, no new AbilityPreset, no prefab or unit ability-list change. No `.meta` files added.

## Acceptance criteria

- [x] Steer = move then a full Whirl, hit credited to the cast: `Steer_EndsInAFullWhirlAtTheDestinationOnly` (beats Swell, Streaks, Burst, Done; pull from the destination only; hits on pulled and touching enemies; one report per hit through `steps.Report`, the same path every Whirl hit uses), `Steer_WhirlPullsThenWaitsForReactionsThenHits`, `Whirl_PullOrderAndImmovable_AreTheSameAfterASteer`, `Steer_WhirlCanPullIntoTheCellTheCycloneLeft_AndThePreviewPlansTheSame`. Written, not yet run.
- [x] No double hold, hold released on abort: `Steer_WhirlHoldsTheTurnSwitchOnce_AndReleasesItAtTheEnd` (no hold while gliding, one hold in the Whirl, none after), `Steer_StoppedPartWayThroughItsWhirl_ReleasesTheHold`. The Steer registers no hold of its own; only the Whirl does.
- [x] Dispose deferred during the Steer's Whirl: `ADisposeDuringTheSteersWhirl_WaitsForItsEnd` (the Whirl's own finally re-defers because `IsSteering` is still true; the Steer's finally then disposes).
- [x] Masher counter ignores the Steer's hit: structural. The hit is reported by the Whirl steps with the cast as source; the Masher rule already ignores a hit whose source is the Cyclone cast (`MasherCounterRules` is unchanged, `MasherCounterWhirlTests` covers the rule). `TheSteersHit_IsCreditedToTheCast_NotToTheSteerAsAnAction` checks the cast is a Cyclone cast, the Steer is not and reports no targets, and the Steer's Whirl reports once per hit. The live path needs the verifier's play check.
- [x] Howling Gale Weak on Steer hits: structural. The Steer's hit goes through `steps.Hit`, the same compound as every Whirl hit (Weak is nested in it; `CycloneHowlingGaleTests` covers the compound). Play check to confirm.
- [x] Log reads "Whirl · Lucy: carried N, pulled N, hit M", carried 0 until the carry exists: `WhirlLogLine_NamesCarriedPulledAndHit`, plus the `(0, 1, 2)` assertions.
- [x] No "Gust" left: case-insensitive grep over `Assets/` .cs, .asset, .prefab, .unity: only a font asset's glyph table matches (not ours). No code names, comments, tests or strings remain.
- [x] Cyclone Power exactly 3 / 4 / 5: `CyclonePower_HitIsThreeFourFiveTimesDamage` (3 cases, one per level). It reads the asset's `Stat_DMG` levels and the hit's `baseFactor` and checks `round(3 x 1 x factor)` and a floor with 0.01 slack, so it does not rely on rounding luck. It is a formula check on the live assets, not a full ability-runtime evaluation.
- [ ] EditMode all green except the known red: NOT RUN (see below).

## Save reset

no

## Decisions I made

- Hold owner for the Steer's Whirl is an optional `holdOwnerSource` parameter on `SteerRoutine` (default null, `TrySteer` passes the live run handler). Same behavior in the game; it lets a test use a real handler without touching statics.
- Cyclone Power: changed the stat level factors rather than the hit modifier, because the hit's `baseFactor` is shared by every level. Used 1.333333 / 1.666667 (not 4/3 and 5/3 exactly) so the product rounds to 4 / 5 under any rounding mode.
- Dispose of the inner Whirl iterator in a `finally` so a Steer stopped mid-Whirl (object disabled, `StopCoroutine`) still releases the turn-switch hold.
- Steer preview (`CycloneSteerPreview`) is unchanged apart from its comment: it still previews the pull only. Damage on ghosts is C4.
- `whirlHitTimes` and `TouchLabel` are left as they are (the cross label still reads them); C4 removes both with the label.

## Needs THJ / coordinator

- I could not drive the open editor's Test Runner (the Unity MCP failed to connect, and the command line cannot open a locked project). I compiled both assemblies offline with Unity's Roslyn and the editor's own response files (`Assembly-CSharp` and `Assembly-CSharp-Editor`): zero errors. The new and updated tests have not run. Please run EditMode in the editor (focus the editor, Ctrl+R, Test Runner, EditMode, Run All). Expected: green except `AIRegressionTest.Baseline_MatchesCurrentAI`. AIRegression inner count: before 43 (per plan), after not measured; nothing in the AI path or any ability list changed, so 43 is expected.
- Please open `Lucy_Cyclone_Ability.asset` once in the editor to confirm it loads (two float edits, low risk).

## Docs to update

- `design/cyclone-redesign.md` as-built and GDD `characters/lucy.md` LU-4 / LU-6 (Steer = move then Whirl; Cyclone Power 3 / 4 / 5): owners per plan (C5).
- `reports/cyclone-c2.md` mentions the Gust and the old log line: history, leave.

## Risks and loose ends

- Plan miss: `OnTurnEnding` / `StartWhirl` refuse while `IsSteering`, and `CanBeSteered` refuses while `IsWhirling`. Both still hold, but a Steer's Whirl running with `IsSteering` true means `NotifyReadyChanged` fires only at the Steer's end. If a UI listener needs a "busy" change at the Whirl's start, it does not get one (same as before for the glide).
- Plan miss: `Steer_*` tests build the `holdOwnerSource` handler with `AddComponent` in edit mode (the pattern the existing turn-switch test already uses). If a future handler `Awake` needs scene objects, those two tests would need a different seam.
- The Steer's Whirl now includes the swell wait (`swellSeconds`, 0.2 s) and the reaction settle wait (up to 15 s cap), so a Steer takes noticeably longer than the old Gust. That is the design, but watch the feel.
- A Steer into a dead end where nothing is hit still plays the swell and the burst beat; if THJ finds that heavy, C4 can shorten it.
- (Corrected in the fix round) The Steer action does NOT stay open to the end of the Whirl: it closes once the pull is done; see "Fix round".

## Proposed commits

1. `feat(lucy): a Steer ends in a full Whirl at its destination, and Cyclone Power hits for 3, 4 and 5 times damage` (plain, one unit: the code, data and tests only work together, and the log line change touches the shared Whirl step interface):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSteer.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Steer.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Whirl.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPreview.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerRules.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlPlanner.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneSteerSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneWhirlSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneWhirlTests.cs`
   - `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`

   If THJ prefers two commits, the Cyclone Power asset line pair plus `CyclonePower_HitIsThreeFourFiveTimesDamage` can split off as `feat(lucy): Cyclone Power hits for 3, 4 and 5 times damage`, but that test lives in `CycloneSteerTests.cs` with the Steer tests, so one commit is cleaner. Do not stage `PreloadScreen.unity` or `ProjectSettings/*` (THJ's).

## Other branches

none (scope: `thj/cyclone`)

## How to see it

1. In Unity, focus the editor and let it recompile; Test Runner, EditMode, Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red.
2. Play a level with Lucy, cast the Cyclone, then Steer it up to 3 cells with an enemy on an arm of the destination and one beside it. The Cyclone should glide, swell, pull the arm enemy one cell, wait for reactions, then hit every touching enemy with damage numbers and a burst.
3. The combat log line should read "Whirl · Lucy: carried 0, pulled N, hit M". There is no "Gust" line.
4. With Cyclone Power bought to levels 2 and 3 (and Lucy's damage 1 in a sandbox), the hit is 4 and 5 (base 3).
5. Steer next to a Masher: it should not counter. If Howling Gale is unlocked, the hit enemies show Weak.

## Fix round

Review: `reports/cyclone-r2-c1-review.md` (verdict FIX). All five items done; both assemblies compile with zero errors in the offline Roslyn check; EditMode still not run (editor not drivable).

- Must-fix (action open through the Whirl): `AEffectCycloneSteer.WaitForSteer` now waits on `CycloneSteerRules.SteerActionOpen(isSteering, isWhirling, isPulling)`: open while gliding and while the Whirl pulls, closed for the reaction and hit phase and after an abort. `IsSteering` still runs to the end of the Whirl, so Dispose stays deferred and the Cyclone is not steerable again early. Class comment fixed. Test: `SteerAction_StaysOpenThroughTheGlideAndThePullOnly` (5 cases). Matches how the cast closes after its pull.
- Cyclone Power test now runs the engine's own stat step: it reads the Stat_DMG level factor and policy from the cast and the hit's base factor, applies `AAttributeModifier.ModifyWithPolicyBasic` (the function the ability stat set uses) and the whole-health rounding, for levels 1 to 3. It is not the full `StatBackedEvaluationProbe` path (that needs a Lucy prefab, faction and registry in edit mode, and I could not run it to check), so crit, the faction's `StatUB_DMG` bound and Lucy's real damage are not covered; the reviewer's by-hand check of those stands.
- Credit test renamed `TheSteer_ReportsNoTargetsOfItsOwn_ItsWhirlReportsEachHit`; the static asset facts about the Masher rule are dropped (that rule has its own tests); it asserts one Whirl report per hit (2 enemies, 2 reports).
- Unused usings removed from `CycloneSteerSteps.cs`, `ICycloneSteerSteps.cs`, `CycloneEntity.Steer.cs`.
- Two long comment lines reflowed (`CycloneEntity.Whirl.cs`, `CycloneSteerTests.cs`).

Extra files touched in this round: `CycloneSteerRules.cs` (new helper), `AEffectCycloneSteer.cs` (already in the commit list). No new files, so the proposed commit's file list is unchanged. Not done: the Linda-folder stray ability copy (backlog, per the review).
