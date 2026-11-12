# Cyclone C3 review

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. Branch `thj/cyclone`, uncommitted tree.

**Verdict: FIX** (one must-fix). Core hook (`ITargetSelectionRangeProvider` + 4-line check in `FactionControllerBase.ComputeAbilityRangeCells`) is additive, main-thread only (AI uses its own range code), and has no clean non-core alternative; THJ approved it (D-539).

## Must fix
1. Steer button greyed for the rest of the turn after a cast: the cast completes (bar refresh) while `IsWhirling` is still true; nothing refreshes the bar when the Whirl ends (`AbilitiesBarHUDUI.CycloneSteer.cs:23-30`, `CycloneEntity.Whirl.cs:142-153`, `AEffectCycloneSpawner.cs:54-63`). Fix: refresh when the Cyclone is ready again (event at the end of Whirl/Steer routines, or a step calling `CombatLevelUIManager.Instance.RefreshUnitControlPanel(SessionLogs.CurrentSelectedUnit)`). Don't make the cast wait for the whole Whirl (deadlock with `ReactionsSettled`). Likely also Super Time.

## Should fix
1. Report's AI claim wrong: `AIUnitBrain.GetAbilityCandidateTargets` (:388-466) never calls `CheckTargetSelectionCondition`; an AI-controlled Lucy could pick any cell, spend 1 AP + cooldown, "Steer not done". → coordinator: refuse in `AEffectCycloneSteer.CheckActivationFeasibility` when the owner is AI-controlled (worker-safe).
2. `CycloneSteerTests.cs:309-314` can't fail (two fresh `RuntimeAbility` objects): drop or relabel.
3. Test for `TargetSelectionRange.TryGetProvided` (false for cast / no provider; true for live Steer with cells around the Cyclone).
4. `ITargetSelectionRangeProvider.cs:31-35`: document main-thread only (Unity null check, allocation).
5. `CycloneEntity.Whirl.cs:64,84`: add `|| IsSteering` guard to `StartWhirl`/`OnTurnEnding`.

## Notes
- Button swap safe at the ability level (each refuses at the wrong time); Super Time uses its own guard; Duos match by trigger preset; skill tree points at the cast; locks hide both; cooldown/AP correct; restart/fade covered. Lucy memory reset not traced; character select shows first N abilities (Steer index 8).
- Glide: Cyclone stays planted on the old cell, ability in progress blocks input/end turn; `Relocate` fires plug-state twice (walk highlight recompute; play check).
- Gust: `unitEndMoving` fires, no report, no Masher provocation, log line ignored by tally/Masher/BondLite.
- Preview: same planner as the real Gust; `Clear()` → `GUnit.HideGhost()` may hide another preview's ghost; nothing until the cursor moves if already on the cell.
- Scatter safe; AI danger per job OK.
- AI regression 42 → 43 = new preset in the project-wide catalog scan; only removable by re-baselining (fix session).
- Commit order A, A2, B, D1, C1 1–8, C, D2, D3 compiles with whole files; widen C1 commit 3's message (inert Steer code until D2).
- Hygiene OK; `Unit_Lucy` diff has 2 harmless default QTE lines; stale `data[8]` stat-profile override now applies to Steer (matches others); setup tool re-runnable.
- Play checks: Steer right after a cast; Mark's role doesn't answer a Steer; walk highlight flicker on relocate.

## Re-review of the fix round (2026-11-12): APPROVE
Must fix done (`CycloneEntity.Ready.cs:17-24`, called from Whirl/Steer `finally` and `Dispose`; main thread; skips with no selection; safe after level end and unload; a few extra refreshes, no flicker). AI-Lucy refusal worker-safe (`AEffectCycloneSteer.cs:88-92`). Should fixes 2–5 done. Item 7 skip justified (only the Masher's preview ghosts enemies, Masher never pulled). Commit order still compiles with `Ready.cs` in C1 commit 3. Play checks: Steer clickable once the first Whirl ends, also after a Super Time cast while Lucy is selected.
