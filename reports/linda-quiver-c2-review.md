# Review: Linda's Quiver C2

Reviewer: miso-reviewer, 2026-10-26. The coordinator saved this file.

**Verdict: FIX**

Clean:
- No core code changed. D-253's deviation holds.
- Statics are reset. The subscription is cleaned up in `OnDestroy`, and beats stop on `levelEnded`.
- No new work on the AI thread.
- Pickup rules match the plan.
- LF, no BOM, no private IDs.

## Must fix
1. **Commit units can't be built in order.** C1 and C2 share whole files (`GroundedArrowField.cs` calls into `.Pickup.cs`, and `Unit_Linda.prefab`'s `LindaQuiver` block already has the beat fields). New units:
   - (a) all quiver scripts and tests, C1 and C2;
   - (b) the `PlayModeStaticReset` line;
   - (c) the two cloners;
   - (d) the prefabs, data and wiring tests.

   This is the coordinator's job; it goes into the plan's commit log.

## Should fix
1. **Linda replies after dying.** `Bark` checks only `!speaker`. Skip it when `!speaker.IsAlive`; the toss stops or vanishes if Linda is dead.
2. **The pickup decision isn't tested.** It lives in `TryPickUp`. Move it into the pure class, test the stale-lock, dead-Linda and G3 cases, and rename `StackUnlocksWhenTheEnemyLeaves_ThenItCanBeTaken`.
3. **`Linda_HandBackBeatTimingsAreSet` pins tuning values.** Keep only the ordering and positive-value checks.

## Notes
- **Several stacks in one move** start one beat each, and they pile up; judge in play.
- **The `ShowText` popup** has a fixed 1.2 s and its default motion; tune in play.
- **Rule edges:**
  - While Linda is dead, nothing is picked up and arrows stay.
  - Allied units in another faction (`Unit_Toba_Ally`) don't pick up.
  - `Resurrect` plugs the unit before it is alive, so a unit revived on arrows probably doesn't pick them up.
- **Unity noise in the tree:** the TMP fallback asset and two ProjectSettings files. Never stage them.

---

# Re-review after fixes (2026-10-26)

**Verdict: FIX** (one new must-fix; every earlier fix is correct)

- The `unitBorn` hook is safe: it is unsubscribed, never double-picks, and leaves G3 unchanged. The only core change is still the reset line. LF, no BOM, no private IDs. The merged units build in order.

## Must fix
1. **The locked look goes stale** (`GroundedArrowField.Pickup.cs:78-82`, `ArrowPickupRules.cs:33`).
   - `Pickup` stores the lock state, but the view only refreshes when an arrow is taken.
   - Result: an enemy stepping onto a free stack never shows the locked look, and `OnChanged` isn't raised. A Bergson with a full quiver can also leave a stale red look behind.
   - Fix: compare the lock before and after, and when it changed, call `RefreshView` and `OnChanged`.
   - Play-check step: an enemy walks onto a free arrow, and the stack shows the locked look at once.

## Notes
- A player-faction decoy or summon spawned on a stack picks it up. That is consistent with D-254.
