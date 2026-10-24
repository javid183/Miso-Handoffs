# Enemy alert C2: review

Reviewer: `miso-reviewer`, 2026-10-24. Saved by the coordinator.

**Verdict: APPROVE** (no must-fix; four should-fix).

## Should fix

1. Quiet tag add (`EnemyAlertTracker.Visuals.cs:148-164`, `unit.enabled = false` around the add) is safe today: no `OnEnable`/`OnDisable` on `GUnit`, `GridPluggableEntity`, `GameEntity`; `Update` only ticks ATB; the code running during the add doesn't read `enabled` (`CombatLog.OnTagChanged`, `JohnShieldRelay`; `BarkManager.cs:1030` isn't called then). No cleaner non-core route (`GTagSet` has no silent add; `showInGame` off also kills the panel line and tooltip, `EntityInfoPanelUI.cs:149`, `TagTooltipManagerUI.cs:82`). Keep it, and add a reflection test that fails if those classes ever declare `OnEnable`/`OnDisable`. Backlog (Tier 3, THJ): a data-driven "pop on gain" flag on `GTag` read by `GUnit.ShowTagGained`.
2. Marker sorting ties with the unit's world canvas (`Visuals.cs:98-109`; `DynamicTop`, order 0), so it can flicker against the info panel and bars. Use order +1 (or a serialized offset); consider hiding it while the info panel is up; replace the magic `1097219007` (l.41) with `SortingLayer.NameToID("DynamicTop")`.
3. A "!" pops on an enemy killed by the hit that wakes it (`Visuals.cs:168-175, 183-185`): play step-0 pops a frame later so the `IsAlive` check filters it.
4. `ShowsMarker` truth-table tests add little (`EnemyAlertVisualTests.cs:32-41`); fine to keep.

## Notes

- `UnitMiniHealthBar` reference from Core: compiles (no asmdefs); precedent `GUnit.cs:6` uses `MISO.Content.UI`. Acceptable.
- Lifecycle checked: death/FakeDie, revive, off-board wave units, level end, disable/destroy, decoys, in-flight pops, missing `DamageNumberManager`, pushes, facing flip. LateUpdate cost low (no allocations).
- Stagger uses spread depth; start-alert spreads pass `showPop: false`.
- No statics, balanced subscriptions, no core code, no private IDs, LF/no BOM.
- Commit shape: C1 commit 2 and C2 can't compile apart. Cleanest: (1) data-only commit `GTagRegistry.asset`, `GTagSet.asset`, `AIController.prefab` (core turn-flow data, inert until the tag is added); (2) everything else (tracker partials, settings components, visual rules, `LevelBase.prefab`, three test files, metas). Both after THJ's play check.
- Play check: marker size (placeholder lamp), position against the open info panel, sorting.

## Re-check after fix round 1 (2026-10-24): APPROVE

- Reflection test (`EnemyAlertVisualTests.cs:64-75`) covers `GUnit`, `GridPluggableEntity`, `GameEntity` with `DeclaredOnly`.
- Sorting: canvas order + `markerSortingOffset` (1); fallback layer by name; marker hidden while the unit's `EntityInfoPanelUI` is active (looked up once per marker; trivial per-frame cost; no null access).
- Every pop waits at least one frame; the `IsAlive` check drops a pop for a unit killed by its waking hit.
- Should fix: both changed files became CRLF (the folder is LF; `.gitattributes` says `eol=lf`). Convert back before commit (sent to the C3 run).
