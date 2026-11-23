# Report: Chunk 1.3, Linda's arrows come home when a level is won

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.3, item H-08)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: **blocked**. No existing hook fires on a win before the ending sequence without a core change. Nothing was built for this chunk.

## What changed

Nothing for this chunk. (Chunk 1.5's Encore glow and trail sit on the same flight, so whatever lands here gets the gold look for free.)

## What I found

The brief asked me to stop and report if no early hook exists. I checked every path from "objectives say Win" to the outro, all of it in core `CombatLevelRunHandler`:

1. `UpdateObjectives`: `EvaluateObjectives` returns Win. Then `ForceEndTurnSafe()`, `_levelEnded = true`, `StartCoroutine(EndLevel(result))`.
2. `EndLevel`, in order:
   1. Persist states (and items, on a win only).
   2. Input to None.
   3. Wait `endLevelDelayBeforeHudHide` (0.25 s).
   4. `HideHUD()`.
   5. Wait `endLevelDelayAfterHudHide` (0.25 s).
   6. Resurrect the dead family (win).
   7. `MissionTracker.MarkCurrentLevelCompleted()` then **`PlayOutro()`** (win).
   8. Only after the outro: `GlobalEventBus.levelEnded(endResult)`.

What I looked at, and why none of it works:

- **`levelEnded`**, the only win/loss event, fires **after** the outro. Too late, and the arrow field closes on it.
- **`turnEnded`** (from `ForceEndTurnSafe`) fires on a loss too. It may also be delayed (`WaitWhile !CanEndTurn`).
- **`objectivesSetAdvanced`** fires only when a stage advances, not on the final win.
- **`MissionTracker.MarkCurrentLevelCompleted`** raises nothing. Its state is readable only after the outro's first step has already run, in the same frame.
- **`FactionTracker.PersistItemState`** (win only) keeps its state private.
- **`Sequence` / `SequencePlayer`** raise nothing when a sequence starts, only when it ends.
- **`LevelObjectives`** keeps no result; its aggregation settings are private.

## Options

1. **Core, Tier 3 (recommended).** Add one bus event, for example `GlobalEventBus.levelWon` (a plain `UnityEvent`). Raise it at the top of `EndLevel` when `result == Win`, before the first wait.
   - It is about 0.5 s plus the HUD hide before `PlayOutro`, which is room for Encore's 0.45 s flight.
   - The quiver listens, recalls every grounded arrow without the AP or the cast, and unsubscribes on disable.
   - Two core files (`GlobalEventBus.cs`, `CombatLevelRunHandler.cs`); one field plus one line; no behaviour change for anything else.
   - Exact on the win, the cheat win (`BypassCurrentLevelWithWinResult`, which goes through `EndLevel`) and every level.
2. **Non-core, polling (Tier 2, fragile).** A quiver-side component polls the public `CombatLevelRunHandler.IsLevelEnded` each frame. When it turns true, it decides win or loss from the objectives' cached state.
   - Timing is fine (caught the next frame, at least 0.5 s before the outro).
   - The win test is a guess: no public result exists, and a winning evaluation returns before the defeat objectives are re-evaluated, so their `Satisfied` is stale.
   - The aggregation modes are private, and the cheat win evaluates nothing.
   - It reads core internals by inference. I don't recommend it.
3. **Non-core, data (Tier 2, partial).** A new first step in each level's outro sequence (a "return Linda's arrows" sequence).
   - Exact (the outro plays only on a win) and in time (it is the first step).
   - Needs a data sweep over every level's outro, plus a rule for new levels.
   - Levels without an outro get nothing. That costs no gameplay: the quiver starts every level full anyway, so this item is about what the player sees.

**Recommendation:** option 1. It is the only exact, every-level hook. The core change is small and additive, and it can be reviewed and reverted alone.

## Ready to build once a hook is chosen (for the next session)

These points come from the code read, so the build is short:

- **Recall path:** `GroundedArrowField.RecallTo(quiver)` already refills the quiver at once (`RecallRules.Resolve`), then starts the flights (`RecallFlight`, now with chunk 1.5's glow and trail). It spends no AP: the AP belongs to the ability. Calling it directly is no Encore cast, because no `RuntimeAbility` runs, so no `abilityPerformed` and no stats.
- **Two small changes it needs:**
  - A win variant without the recall bark (the ending sequence is about to start). For example, an optional `bark` flag, or a sibling `ReturnAllOnWin(quiver)` in a new partial.
  - A return kind other than `Recall`, so the log line and the return cue don't read as Encore. For example, a new `QuiverReturnKind.LevelWon`. Today only `GroundedArrowField.Recall.cs` passes `Recall`; `QuiverLogListener` and `QuiverReturnCue` read any kind.
- **Guards:**
  - Nothing on a loss (the event or check is win-only).
  - Nothing without Linda or a field (`GroundedArrowField.Current` null, quiver switched off, Linda dead: `RecallTo` already returns 0).
  - Skip when the quiver is full or no arrows lie on the ground (`RecallRules.CanRecall`).
  - The handler only runs on the main thread from the bus. The field's `GroundedCount` read stays worker-safe.
  - Subscribe in `OnEnable`/`Start` and unsubscribe in `OnDisable`, like `LindaQuiver.Subscribe`.
- **Tests:** a pure rule (when the win return happens: win only, Linda alive, field open, arrows grounded, room in the quiver), plus a field-level test that the count is restored with no AP change. The timing against the outro goes to the play check.
- **Overlap:** a quiver-side subscriber would touch `LindaQuiver.cs` (already changed by chunk 1.4) unless it lives in a new partial with its own `OnEnable`/`OnDisable`. Today `LindaQuiver.cs` has `OnEnable` → `Subscribe()` and its own `OnDisable`. Prefer a separate small component added in `Start` beside `QuiverPipsView` and the others; that is a one-line hunk in `LindaQuiver.cs`.

## Acceptance criteria

- [ ] On a win, every grounded arrow flies back: not built (blocked on the hook).
- [ ] Quiver count restored before the ending sequence's first step: not built.
- [ ] No AP spent, not an Encore cast: not built (the recall path already meets both; see above).
- [ ] Nothing on a loss; nothing without Linda or a field: not built.
- [ ] AI-thread guarded and cleaned up on disable: not built.
- [ ] EditMode tests: not written.

## Chunks

### Chunk 1.3: arrows home on a win

- Changed: nothing.
- Criteria met: none (blocked).
- Decisions and loose ends: stopped as the brief asked; options above.

## Reviews and checks

- Full EditMode suite (run once for chunks 1.2 and 1.5; nothing changed here): 2529 total, 2525 passed, 1 skipped (Explicit AI test), 3 failed. All three were "m_LockCount == 0" in the GridToLevel fixtures, the known flake; those fixtures passed 34 of 34 when rerun alone.

## Save reset

No.

## Decisions I made

- Stopped before any code, per the brief's rule for a missing hook.

## Needs THJ

**Which hook for "arrows come home on a win"?**
1. **What:** the game raises no event on a win before the ending sequence. The only end event fires after it.
2. **Why it matters:** H-08 needs the arrows back before the ending sequence's first step, in every level.
3. **Options:**
   - (1) A new `levelWon` bus event raised at the start of `EndLevel` on a win (core, Tier 3, two lines).
   - (2) Poll the level-ended flag and guess the result from objective state (non-core, fragile).
   - (3) A first step in every level's outro (data sweep; levels without an outro get nothing).
4. **Recommendation:** (1).
5. **Default if no answer:** nothing is built; H-08 waits.

## Docs to update

- If option 1 is picked: `tech/core-systems.md` "Level run" row (the new `levelWon` event and where it's raised).

## Risks and loose ends

- `GroundedArrowField` closes on `levelEnded`, after the outro. A win return before that is safe; after it, the field is already empty.

## Proposed commits

none (nothing built)

## Other branches

none

## How to see it

Not built yet.
