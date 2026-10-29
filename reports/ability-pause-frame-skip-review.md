# Review: ability pause-frame skip (core)

Reviewer: miso-reviewer, 2026-10-29. Saved by the coordinator.

**Verdict: APPROVE.** No turn lock.

## Why no turn lock

- Frame callbacks and the end-of-clip `Stop()` are gated by the new `_heldAtPause`. It is set only in `Pause()`, and cleared in `Resume()` and in every `Play` (`EntityAnimationHandler.cs:215`), which covers `SimplePlay`, `SimplePlayEndFrozen`, `Stop` and `Initialize`.
- **Cancel:** goes through `Stop()`, which clears the hold. The guard skips the frames flushed after it, because no activation was requested.
- **Death or hit while held:** the new `Play` clears the hold.
- **Restart:** all fields are per instance.

## Other checks

- **Resume:** continues from frame 6. Frame 7 fires once, including when the animator wraps.
- **Replay from start:** only runs when activation wasn't requested, so it can't loop.
- **`CatchUpFrames`:** identical to the old loop. All 11 tests were checked by hand.
- **Abilities that never pause:** unchanged.
- **Hygiene:** no per-frame allocations, line endings and BOM kept, no private IDs, unique GUIDs.
- **Commit:** one commit of 10 files, matching the report.

## Should fix (follow-up, needs THJ's OK; already there before this change)

- `EntityAnimationHandler.cs:224`: `_paused` stays true after a cancel, or when a `Play` arrives while held. `Play` then skips setting the speed, so a hurt or death clip played while held stays at speed 0 and never fires its callbacks. A lock is possible if a unit can be hit during its own target selection.
- Fix: clear `_paused` in `Play`. This changes behaviour after a pause (for example, idle jitter after a cancel).

## Backlog notes (already there before this change)

- A long hitch can carry a one-shot clip past its activation frame before `Stop()`, so the ability never activates. Applies to every ability.
- A PauseFrame ability left held when the turn ends keeps `_abilityAnimationPlayStarted` set. A later pick could then call `Resume()` on another clip.

## Other notes

- `LevelLucyJohn-C1.prefab` and `LevelLucyJohn-C2.prefab` show as modified, predating this work. Not part of this commit.
