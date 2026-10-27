# Review: Linda's Quiver C1

Reviewer: miso-reviewer, 2026-10-26. Saved by the coordinator; the reviewer has no write tool.

**Verdict: FIX**

- No core change except the allowed reset line in `PlayModeStaticReset.cs`. Landing hooks the existing public `SpawnableEntity.onDisposeReady`.
- Nothing new on the AI thread. LF, no BOM everywhere. No private IDs.

## Must fix

1. **A kill shot isn't recorded** (`QuiverArrow.cs:118`, `NearestOccupiedCell` line 204).
   - `Projectile`'s `OnTriggerEnter2D` runs first and damages at once.
   - On a kill, `GUnit.Die` sets `IsAlive` to false, unplugs the unit and disables its colliders.
   - `QuiverArrow` then rejects the hit, and the arrow lands at end of range.
   - Fix: drop the `IsAlive` condition. Fall back to `unit.LastCell`, then to the cell nearest the unit's position.
2. **Tempest Bloom** (D-252). The override cell is the end of flight with no hit; run it through `ArrowLandingRules.ChooseLanding(LineCells(origin, override), null, override, CanHoldArrow, origin)`. Update the comments.
3. **A field can be created after level end or during unload** (`QuiverArrow.cs:151`, `GroundedArrowField.GetOrCreate`).
   - Fix: create the field at level start (`LindaQuiver.Start`).
   - `Ground` uses `GroundedArrowField.Current` only, and does nothing when it is null or closed.

## Should fix

1. **Catch & Return gives the +1 late**: it waits for `Apply`, and a second arrow during the animation swaps the held one. Fix: return the arrow in `OnCaught` once the catch has succeeded (Bounces modes).
2. **`ArrowLandingRulesTests`**: `PierceThroughTwo_LandsOnTheSecond` and `Hit_LandsOnTheEnemysCell` don't test pierce.
   - Rename them to what they test.
   - Move the hit-recording and spend/land/hold/return state into a plain C# class and test it: a copy never spends, an arrow lands once, hold then release, hold then return, an unpaid shot never lands, a killed enemy still counts.
3. **Commits**: the `PlayModeStaticReset.cs` line gets its own commit, right after the scripts commit (coordinator).

## Notes

- **Duo arrow through the Cyclone**: a Marks-Sisters arrow (`LindaAttackFireArrow` is on the Cyclone's whitelist) lands by the Tempest Bloom rule. Add one line to the GDD.
- **Hand-written YAML GUIDs and fileIDs**: `QuiverWiringTests` checks they load. Unity may re-serialize the three spawn assets later.
- **Play cases for the verifier**:
  - a kill shot mid-path
  - pierce through 2
  - Tempest Bloom
  - Catch & Return, caught and missed
  - Crescendo
  - both Duos
  - Watch at 0
- **Known edges**:
  - Two shots in the same frame at 1 arrow: the second fires unpaid.
  - The stack icon comes from the first arrow type that landed.

---

# Re-review after fixes (2026-10-26)

**Verdict: APPROVE**

- All five fixes are correct.
- The only core change is still the reset line. LF, no BOM, no private IDs.
- The commit units build in order: scripts+tests → reset line → cloners → prefabs/data/wiring tests.

Notes:
- **Landing with no field:** if `Current` is null the arrow vanishes. Today that only happens at level end or unload. If arrows ever fire outside a `CombatLevel`, return it to the quiver instead.
- **For C3:** `GroundedArrowField.GroundedCount` reads `_current` without checking the level. Recall's check depends on it.
- **Still to see in play:**
  - a kill shot mid-path
  - pierce through 2
  - Tempest Bloom
  - Catch & Return, caught and missed
  - Crescendo
  - both Duos
  - Watch at 0
