# Review: Cyclone reset (thj/cyclone, 4b84d47f1..359882aed)

Reviewer: miso-reviewer, 2026-11-19, one review for the whole feature (no core chunk). Saved by the coordinator (the reviewer is read-only).

## Verdict: APPROVE

No must-fix. Planner, preview and execution share one rule; cleanup on abort covered; no core file, no new statics, AI path unchanged.

## Should fix

1. **Preview vs execution with a lethal pass hit** (`CycloneOutcome.cs` `ForSteer` / `Whirl`, ~106-161): the preview plans the closing Whirl's pulls with every passed enemy standing; the live Whirl re-plans on the real board, where a passed enemy killed on the way is gone. A passed enemy 2+ cells behind the stop sits on the back arm and is pulled, so this is common: the preview shows a pull ghost (with skull) for a unit that will be dead, and pulls depending on its cell can differ. Fix: leave passed units whose pass hit is lethal off the Whirl's board in `ForSteer` (same damage/health check the view uses); add a preview-equals-execution test with a lethal pass hit.
2. **Playtest reference in a test comment**: `Editor/CycloneSteerPlannerTests.cs:402` "The screenshot layouts". Describe the layouts in plain words.
3. **Comments still describing the carry or wobble**: `Editor/CyclonePreviewTests.cs:20-23` (class header) and `:187-209` (comments and assert messages: "the carry", "Rider"); `Cyclone/CycloneWhirlPlanner.cs:20`; `Cyclone/CycloneCrossView.cs:18`; `Cyclone/CycloneUnitDrawings.cs:7,10`.
4. **Carry leftovers**: `CycloneWindMotion.Fling` (`:47`) `fromOffset`/`fromTilt` always zero from its only caller (`CycloneKnockMotion.cs`); same for `ICycloneShoveSteps.DrawUnit` (`:26`) `offset`/`tilt`. `CycloneRules.CastShoveDirections` (`CycloneRules.CastOnEnemy.cs:55`) returns a second column direction at a tie that `CastKnock` never reads; its doc comment and `CycloneCastOnEnemyTests.cs:170-177` pin the two-entry list. Return the single onward direction (rename to match the knock) or document that only the first is used.
5. **Over-long comment lines** after edits: `AEffectCycloneSteer.cs:21`, `CycloneEntity.Whirl.cs:17`, `CycloneOutcome.cs:11,14`, `CycloneOutcomeView.cs:13,15`, `CycloneSteerPreview.cs` header. Cosmetic.

## Notes

- Checked OK: one rule for range, target check, execution (`PlanTo_AgreesWithLines_ForEveryCell` + four preview-then-execute tests); knock order and axis (`Right(d) = (d.y, -d.x)`, pinned per direction); safety net (three branches tested); one hit per enemy (both `HitTargets` calls drop `skipHits`; cast and enemy-turn Whirls pass null); `finally` cleanup (stop mid-glide, mid-knock, `Plug` throwing); no core file; no statics; AI thread safe; LF/no BOM on all 56 paths; no private IDs in added lines; report lists match the diff.
- Event order differs from the plan: the Cyclone relocates before the knocked enemy's end-of-move event (same frame; Watch reads the final board). Play-check item.
- Pass hits fire when the glide reaches the cell's centre.
- If a pass hit ends the level, later pass hits are skipped but the knock still runs (harmless).
- Pre-existing, not regressions: Cyclone disabled mid-Steer without destroy leaves `IsSteering` true (same as `IsWhirling` before); a failed landing after the fling raises no end-of-move after the start-of-move.
- No AI content changed; golden master unaffected.
- Bookkeeping: report header out of date; `tech/core-systems.md` line 112 still lists `CycloneWobble` and `CycloneCarryPlanner`.

---

# Review 2: addendum (b62e2a7fd..3b566e5bf: free route, knock damage, no avoidance)

Reviewer: miso-reviewer, 2026-11-20. **Verdict: APPROVE.** No must-fix.

Should fix (cosmetic, ride a later commit): `CycloneEntity.Steer.cs:218` `HitOnce` comment is one 163-character line; `AEffectCycloneSteer.cs:15` header line 128 characters. Rewrap both.

Checked OK: route search (no revisits, steps counted, shorter path resets, only routes whose stop holds compete, tie-break as specified, `Direction` = last step, safety net uses it, knock landing never a route cell, ~52 prefixes, plain data only); planner/preview/execution share `PlanFor`, the glide walks `plan.Path`; knock hit through the same `Hit`/`Report` after relocate and before `Landed` (a kill skips `Landed`), cast uses the same static helpers before the spawn; preview `HitCount` 2 for the knocked enemy, lethal knock removed from the Whirl board; R3 touches no core file, remaining AI tests meaningful, regression 43 unchanged; LF, no BOM, no statics, no private IDs.

Notes: the cast's knock hit lands even if the cast is then refused (only possible if the hit's reactions fill the cast cell; accepted). Preview lethal check for the knocked enemy ignores a landing hazard's damage (rare; play-check item 23). R1's turning-route preview test and two header rewrites sit in the R2 commit; per-commit test state reasoned, not run (planner identical at R1 and HEAD).
