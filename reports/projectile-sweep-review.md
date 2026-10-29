# Review: core Projectile sweep (D-300), 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: FIX**

## Must fix
1. **Hit order on a long frame.** Physics runs before `Update`, so the trigger reports the end-position body before the next-frame sweep adds the nearer skipped bodies. That reverses the falloff. Fix: drain the pending step at the start of `OnTriggerEnter2D`, guarded by `enabled && IsAlive`.

## Should fix
1. **Scope.** Only the four `TargetReachAndHit` arrows are swept (`LindaAttackArrow`, `Return`, `Fire`, `Heal`). Every enemy shot, Lucy fireball and the explosive arrow is `TargetReach` and unaffected, so there is no balance impact on enemies. Correct the report.
2. **Tests** check the helpers only. Add a step test for a frozen step. The trigger-versus-sweep order is left to the 10 fps play check.

## Notes
- Dedupe, the end-cell skip and arrival are correct.
- The last step is swept before dispose. A freeze keeps the step, and a decline sweeps it.
- No statics, no AI path; BOM and LF are kept.
- New preview difference: a glancing contact between preview samples now counts as a hit at runtime.
- With the sweep in place, the kinematic bodies on Linda's arrows are no longer needed for sleeping bodies. Keeping them or not is THJ's call.
