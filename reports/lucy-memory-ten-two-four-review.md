# Review: Lucy's memory "ten → Two. → Four." (uncommitted, `main`)

Saved by the coordinator from `miso-reviewer`'s hand-back (the reviewer is read-only), 2026-11-09.

**Verdict: FIX.** One must-fix: the fade isn't a full fade on screen. Nothing needs escalating.

## What checks out

- **Removal is clean:** stage-2 win (`LivingUnitsLOCondition`), turn order, AI (`UpcomingTurnOrder`, `AIStrategyPlanner`, `AIBlackboard`) read `controller.AllUnits`; alert/threat read `AliveUnits`; barks, combat log, mission stats, health snapshots use `FindObjectsByType<GUnit>` (skips inactive); `CombatLevelRunHandler._units` built at level start; tally reacts only to `unitDied` / `onUnitDamageDone`; `HiddenLevelUnits._revealed` stays right; restart reloads the prefab. Harmless leftovers: `AIFactionBrain._unitBrains`, `EnemyAlertTracker._unaware`/`_known`, `GameEntityMessage.Hosts`.
- **No core-system file edited;** only existing public members (`AllUnits`, `GridCell.UnplugEntity`, `HideThreatLine`, `HideGhost`, `SetActive`, `HiddenLevelUnits.SetGroups`).
- **No new runtime static** (`_skipFade` is an instance field reset in `StartSequence`).
- **Skip:** `SequentialSequence` skips only dialog and camera steps; a skipped cut-in still ends with 4 Claws.
- **Tests** can fail and check real behaviour. No private IDs; CRLF/BOM match siblings; prefab diff additions only (151 vs 115 documents); step GUIDs in planned order.
- **Commits:** file list matches `git status`; two-commit split right; metas with assets.

## Must fix

1. **`HideUnitsSequence.Fade()`: only the bodies fade.** The shadow (`A_Enemy_DarkClaw_Idle_Side.anim` animates `Shadow`'s `m_Color` incl. alpha every frame, overwriting the step's alpha) and the mini health bars (Canvas/Image, shown while alive) stay fully visible for 0.8 s, then vanish at once. Fix: at fade start disable each picked unit's `Animator`(s); fade child canvases through a `CanvasGroup` (get or add, set `alpha`), not `Canvas.enabled` (`UnitMiniHealthBar.Refresh` re-enables it each frame). Optional pure test for collecting renderers/canvas groups.

## Notes

- **Thread race (low risk, existing pattern):** `UnitOutOfPlay.TakeOut` removes from `PhaseData.OwnedUnits` on the main thread while AI `PlanStrategy` jobs (queued by the reveal's `unitBorn`) may enumerate it; the fade runs ≥1.4 s later, so almost surely done. `RegisterUnit` mutates in place the same way. If it shows, assign a new filtered list.
- **Spawn fallback:** if a unit stands on a `ten` tile at reveal, `RevealUnit` falls back to the nearest free cell, which could be a kept tile, so more than 2 could survive. Unlikely (Lucy 7+ tiles away); glance in the play check.
- **ATB branches:** a faded unit would leave its gauge view (not relevant on FTP `main`).
- AC 1–5 need THJ's play check before commit 2. Docs owed: levels plan Segment 2, narrative draft M2 lines.
