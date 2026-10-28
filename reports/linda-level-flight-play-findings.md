# Level flight: THJ's play findings, diagnosed (Explore, read-only, 2026-10-27)

## Pierce stopping early on small enemies
Nothing stops the flight early: hits don't dispose the arrow, and the end-cell enemy is damaged by `Activate(_targetCell)` on arrival.

**Small-enemy colliders** (y-range from the cell anchor):
- Dark Worm: −0.218 … +0.135
- Dark Claw: −0.010 … +0.252

**Causes, ranked:**
1. **Missed middle-cell hits** (worm, then worm; marker on the second): the lift can't cause these, since both paths cross the box fully. Suspect: the arrow is a static trigger moved by transform with no Rigidbody2D, and idle units' Dynamic bodies go to sleep. Box2D doesn't update static-trigger contacts against sleeping bodies; the preview's `OverlapCircleAll` does see them. This is pre-existing. Check with a Kinematic Rigidbody2D on the arrow prefabs.
2. **Landing falls back to the previous enemy when the end-cell enemy dies.** With the lift, the end-cell overlap window on DOWN shots is only 0.045+u, so the trigger record is often missed. This is new with D-278.
3. **Preview and runtime differ on an occupied end cell.** The preview aims at the occupant's TargetPoint, the runtime at the floor. With the lift, the preview misses end-cell worms on DOWN shots and every worm on horizontal shots with an occupied end. This is new with D-278.
4. **UP overshoot** grazes a low collider one tile past range, so the arrow lands past the marker.

**Options:**
- (i) A sprite-only lift: a child visual offset, with the collider on the Direct path. Medium; prefab restructure.
- (ii) Direct plus `destinationMode` Occupant: preview equals runtime. A hit ends on the target's body; a miss still slopes.
- (iii) (ii) plus lowering the spawn to 0.186. It moves every Linda projectile.
- (iv) Full revert, keeping the catch-point fix, `LogicalEndCell` and `travelsWholeRange`.

**Recommendation:** (iv) plus the Occupant part of (ii). Also cache the logical end cell's enemy while the arrow flies, and the presenter's end-cell occupant as `lastHit`. Do (i) later if the slope still bothers THJ.

## The V at the end tile
Not a snap. The grounded icon is drawn at the floor, tilted down-left, while the arrow's sprite and trail stay 0.19 higher for 0.1 s. Fix: hide the arrow's visual and clear its trail when it lands. The revert also removes it.

## Pips over the HP bar of the enemy below
The pips are on WorldUI (order 49), above every unit bar (DynamicTop, order 0). Fix: put the pips on DynamicTop, order −1.

## Catch & Return has no barks
No synergy bark exists anywhere. `RoleBarkPresenter` only hears role events, and `RaiseSynergy` is heard by the combat log and the Masher.
- Non-core hook: serialized prompt, success and miss lines on `ProjectileCatchAndReturn`, shown with `DamageNumberManager.ShowText` like the role barks, respecting `silenceBarks`.
- Core alternative: a Synergy trigger type in `BarkManager`.
