# Review: Linda's Quiver C3b (Mark's catch with a QTE)

Reviewer: miso-reviewer, 2026-10-27. The coordinator saved this file. The code is not compiled yet (the editor is open).

**Verdict: FIX**

What passed:
- Arrow accounting holds.
- The prefab copy is valid.
- No core change.
- No compile blockers found.
- The 3 commit units build in order.

## Must fix
1. **`ProjectileCatchAndReturn.cs:120` and `:334-347`:** with `triggerWithQTE: 1`, `GoSlowMo` runs on every prompt. It forces timescale 1 over any running slow-mo (the reactive interrupt during Watch), then writes back a stale value. D-260 says no bullet-time. Drop the calls, or make them a no-op at about 1 and go through `TimeScaleCache`.

## Should fix
1. **`:72` apply-on-disable runs during teardown:** `RefundShot` calls `CombatLevelUIManager.Instance` without a null guard. During unload or after the level ends, dispose instead of launching the return.
2. **`CatchReturnWiringTests.cs` is CRLF:** convert it to LF.
3. **`CatchFreezeRulesTests.cs:36-49`:** two tests repeat the decline test under misleading names. Merge them or rename them.

## Play-check items
- Linda isn't hit when the return copy arrives on her cell.
- The arrow's Animator doesn't re-show the hidden original.
- Balance: the return re-hits enemies with falloff starting again at 1.0.

---

# Re-review after fixes (2026-10-27)

**Verdict: APPROVE.** All the fixes are correct and nothing new looks like it would fail to compile.

Should fix:
- `GroundedArrowField.Current` stays non-null after `levelEnded`, so the teardown check needs `IsOpen`. Sent to the implementer as a final tweak.

Notes:
- The unused `timescale` field may raise warning CS0414.
- Mark can't catch while Linda is absent in practice: only Linda's arrows are whitelisted, and she always creates the field.

---

# Faster catch prompt review (D-273, 2026-10-27)

**Verdict: APPROVE**

- **Compile risk:** none found.
- **Defaults:** keep every other QTE identical (-1 and 1, taken from the initializers).
- **Animator speed:** restored in `Prepare`, after the preload, and in `Finish`, so pooled buttons are safe.
- **Prefab edit:** minimal.
- **House rules:** LF, no BOM, no private IDs.
- **Remaining commits:** the core QTE change, then the prefab and wiring test.

Play: check the catch prompt, then a role prompt straight after it on the same pooled button.

---

# Play-findings fixes + Lucy review (2026-10-27)

**Verdict: APPROVE.** No compile risks found.

- **CatchSweep YAML:** valid.
- **The sweep:** allocates nothing per frame, and there is no double damage beyond Mark: physics never sees the overshot position.
- **The clamp:** arrival still fires exactly once.
- **Lucy:**
  - The snapshot is taken before `abilityActivationStarted` handlers run, then pruned and cleared on rebind.
  - D-152 ordering is kept.
  - A status-only hit, a hit reduced to 0, a miss or evade, or net healing gives no follow-up.
- **Only core change:** Lucy's handler. LF, no BOM, no private IDs.
- **Commit order builds:** core QTE → catch fixes → Mark prefab + wiring tests → Lucy.

**Should fix (sent to the implementer):** set the one-chance guard `_lastSeen` only after the whitelist check, so a passing non-catchable projectile can't reset it.

**Notes:**
- The CatchSweep filter has no layer mask; adding one is optional hardening.
- The frozen arrow at `returnSource` can still trigger on an enemy overlapping Mark's hand.
