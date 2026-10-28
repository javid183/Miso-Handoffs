# Review: level flight and the catch kink (D-278)

Reviewer: miso-reviewer, 2026-10-27. The coordinator saved this file.

**Verdict: FIX**

## Must fix
1. **Upward shots can land one cell too far.**
   - The height curve clamps at 1, but the linear term still overshoots by a frame's step (about 0.1 at 60 fps). Up shots end at anchor + 0.19 + u, and `NearestCell` flips once u is above 0.06, about 40% of up shots at 60 fps.
   - Affected: the Fire and Heal arrows, bow shots with no hit, and the `ResolveLandingCell` occupant check.
   - Fix: make the landing cell independent of the lift and the overshoot.
   - The `StraightArrows_LiftKeepsClearOfTheNextCell` test compares two constants; replace it.

## Should fix
1. `tangentMode: 21` is invalid. Use 69 (linear, both sides, broken) on all six keys.
2. Stale comments: `ProjectileCatchAndReturn.cs:65` and the comment in `CatchSweep` still say "Mark's hand". Rewrap line 310.
3. Merge commits 1 and 2: until the prefabs carry the flag, the marker shows the wrong cell.

## Notes
- No core change.
- The VerticalFactor path equals Direct plus the lift.
- The sweep overlap holds, the freeze point sits on the drawn path, and there's no retrigger.
- Play check: up shots reach about 0.19 + overshoot + 0.1 past the anchor. Also watch enemies with a low collider top on horizontal shots.

---

# Re-review after fixes (2026-10-27)

**Verdict: APPROVE.**

- **Landing:** the logical end uses the same radius source and context as `Projectile.Initialize`. `DirectionNormal` equals the sign for every cardinal shot, and copies never land.
- **Curve tangents:** 69.
- **Core and compile:** no core change, low compile risk.

Notes:
- Edge case: if the catch can't prepare a copy, the arrow lands at end of range. Unreachable in practice.
- How `QuiverArrow` feeds the rule is covered by the play check only.
