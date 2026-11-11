# Review: Synergy aim preview C1 (shared lanes + Shield Flare), 2026-11-10

(Pasted by the coordinator; the reviewer runs read-only.)

**Verdict: APPROVE.** No must-fix.

Should fix:
1. `Features/Player/John/Scripts/ShieldFlareGeometry.cs:37-38`: `Directions(pattern)` hands out shared `static readonly Vector2Int[]` arrays (mutable; would persist across plays with domain reload off). Return `IReadOnlyList<Vector2Int>`.
2. `Features/Player/John/Scripts/JohnShieldRelay.cs:264-265`: the walk comment now sits above `KindAt`; move it to `CollectCopyTargetCells` (or drop) and give `KindAt` its own line.

Notes: extraction parity checked line by line (same loop, order, stop rules, `lastFree`); `TryCollectCopyTargetCells` unchanged. Geometry pure, but the relay's `KindAt` probe reads GridManager/CombatLevel (an AI caller would need its own probe; none today). Lanes and bars share `CollectCopyTargetCells`; pick-to-effect mapping matches `AbilityDamagePreview.CollectMappedPicks`. Shared pre-existing gaps: preview skips `_unit.IsAlive`; fireball may hit something before John (`Projectile.TryHitOnContact`), neither preview checks; second burst on a double pick sees the board after the first. Flare has no unlock gate (only shield-up). Lifecycle: polls each frame, hides on null/other ability/level ended; listeners rebound; OnDisable/OnDestroy clean; only static is a readonly Color. No core file changed. Scene: one root object only. No private IDs; LF kept. One commit right. Nit: `FlareLaneColor` duplicates the relay's `popupColor`.

Two-pick gap: a non-core mirror of the pick list (record hovered cell when `TargetCellCount` rises, pop when it falls) works for mouse picks but drifts for gamepad/scripted/co-op picks. Clean fix: an additive read-only `IReadOnlyList<GridCell> TargetCells` getter on `FactionControllerBase` (core, Tier 3). Reviewer suggests: ship C1 as is; ask THJ for the getter if he wants persistent lanes.
