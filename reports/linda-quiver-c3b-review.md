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
