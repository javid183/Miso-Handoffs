# Review: D1-C1 (config, Far state, Watch factor), 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: APPROVE**

**Checked:**
- **Runtime copy only:** `PrepareRuntime` makes new `RuntimeStatAttribute`s, and nothing writes to an asset or a save.
- **Only Watch's arrow changes:** the preview matches the hit.
- **Ordering:** the factor is set before Watch fires, and the lock is taken on the player's `turnEnded`, after every action.
- **Who counts:** matches D-285.
- **Toggle off:** exactly 1.0.
- **Hygiene:** no statics; bus subscriptions are paired.
- **Prefab:** a one-line edit.
- No core change. LF, no BOM, no private IDs. One commit unit.

**Should fix (sent to the implementer):** use the effective upgrade level, not `CurrentLevel`, so a run bonus isn't overwritten.

**Notes:**
- Turn 1 might miss the first `turnStarted`. Hardening was asked for, and it goes in the play check.
- The near scale is 0.8333 in float, so a hit landing exactly on .5 can round up by one. The preview does the same arithmetic.
- `Refresh` runs every frame. C2 should reuse its result.
- `LindaFarState` itself is covered only by the play check.
