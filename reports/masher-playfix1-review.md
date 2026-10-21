# masher-playfix1 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **APPROVE**

Should fix (applied before commit, Tier 1):
1. `GUnit.ShowGhostAt(Vector3, Vector2)`: use `abilityOrchestrator ? abilityOrchestrator.AnimationHandler : null` (Unity null check), not `?.`.
2. Same method: for a vertical facing (x ≈ 0) fall back to the body's last side (`_lastNonUpFaceDirection.x` or the handler's current x), not `_currentFaceDirection.x`.

Notes: flash fix complete (no profile swap, unscaled time, snapshot iteration closes the skipped-volume path, single tracked revert); no remaining stuck path found; statics already reset in `PlayModeStaticReset`. Expected behaviour for THJ: any hit flash fades the reactive border and death vignette as soon as it lands (not new); the reactive border fades in over 0.5 s real time; hit flashes now last their full duration (the old double revert halved them). Ghost: old signature unchanged, shared flip rule, slam faces the striker; Queen/Worm/Toba ghosts flip like their bodies (check art in play). Commits independent; `main` has the same `VolumeCameraEffect` (carry fix over). core-systems: add the `ShowGhostAt` overload.
