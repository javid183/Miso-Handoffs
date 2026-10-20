# Report: Masher reckless tank, C1 (core turn-flow holds)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (chunk C1)    Agent: miso-implementer    Branch: masher-tweak
Outcome: done (compile checked outside the editor; EditMode suite not run, see below)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/AIController.cs`: the per-unit wait in `HandleUnits` (line 96) also waits while this controller's own `PhaseData.IsInProgress` is true (D-101).
- `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs`: the class is now `partial`. `SwitchTurnIE`'s `WaitWhile` gets `|| IsTurnSwitchHeld()` as its last term. `EndLevel` calls `ClearTurnSwitchHolds()` right after `_levelEnded = true` (D-102).
- `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs` (+ `.meta`), new partial:
  - public `RegisterTurnSwitchHold(object)`, `ReleaseTurnSwitchHold(object)` and `HasTurnSwitchHolds`;
  - private `ClearTurnSwitchHolds()` and `IsTurnSwitchHeld()` (the watchdog: logs a warning naming the owners);
  - `OnDestroy` clears the holds;
  - nested public `TurnSwitchHoldSet`: plain C#, no Unity objects. It holds the `HashSet<object>` and the 5 s watchdog, so the tests can drive it.
- `miso/Assets/_Project/Core/Interactions/Editor/TurnSwitchHoldTests.cs` (+ `.meta`), new: 10 EditMode tests for the hold set and the watchdog.

No new statics. The hold set is an instance field (`readonly`) on the run handler, so there's no `PlayModeStaticReset` hook.

## Acceptance criteria

- [x] Compiles: I built `Assembly-CSharp` and `Assembly-CSharp-Editor` with Unity 6000.3.4f1's bundled Roslyn. The source lists and references came from the generated `.csproj` files, and the output went to the scratchpad only. No errors. The only warnings in the touched files are two that were already there (`CombatLevelRunHandler.cs` switch expressions, CS8509 and CS8524). The open editor had not refreshed yet, so its console still has to confirm this.
- [ ] Suite unchanged: **not run.** The editor is open and the brief said not to use batch mode. Next step: Test Runner > EditMode > Run All. The new tests are in `MISO.Core.Interactions.EditorTests.TurnSwitchHoldTests`. Expected: all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.
- [x] No holds means identical turn flow (reviewer reads the diff):
  - with an empty set, `IsTurnSwitchHeld()` returns false, and its only side effect is resetting a private timer;
  - it is the last `||` term, so it runs only when the existing conditions are already clear;
  - the new `OnDestroy` and the `EndLevel` call only clear the set. `LevelRunHandlerBase` has no `OnDestroy`, so nothing is hidden.
- [x] EditMode test for the hold set without a scene: `TurnSwitchHoldTests` covers:
  - register and release;
  - the same owner twice counts as one hold;
  - two owners;
  - releasing an unknown owner is a no-op;
  - clear;
  - the watchdog is still held at exactly 5 s, clears just past it and names the owners;
  - a skipped frame restarts the timer;
  - release then register restarts the timer;
  - a Unity owner is named by its name.

  The wiring itself (the `SwitchTurnIE` wait, `EndLevel`, `OnDestroy`) needs a scene, so the reviewer reads it and the verifier checks it in play once C4 registers holds.

## Deadlock reasoning (item 1, AIController)

`PhaseData.IsInProgress` has three writers on the AI side:
- `FactionControllerBase.TryTakeAction` (:950, set true; set false at :963, before `abilityPerformed` is raised);
- `TryPlayFactionRole` (:187 and :190);
- the AI loop never sets it directly.

The new term is in the wait at the top of the inner loop. That wait runs before `PrepareUnitTurn` and `PerformAction`, never inside them:
- `PerformAction` (→ `TryTakeAction`) is called after the wait has passed, so the wait can't block the AI's own action.
- After `PerformAction`, line 118 already waits `while (PhaseData.IsInProgress)`. In the normal flow the flag is false when the loop comes back to line 96, so the new term is a no-op today.
- The flag is true at line 96 only if something set it in between, which today can only be a `TryPlayFactionRole` on this controller (the C4 Masher answer). That flag is cleared by the role's own completion callback, which doesn't depend on the AI loop. So the wait ends when the answer ends.
- First pass for a unit: `TrySelectUnit` and the camera focus don't set the flag.
- The only way to hang is a flag stuck at true. That would already hang line 118 and `GuardedRequestEndTurnIE` (:184) today. The new term adds no new way to get stuck.

So: no deadlock.

## Save reset

No.

## Decisions I made

- The hold bookkeeping and watchdog live in a nested plain class, `CombatLevelRunHandler.TurnSwitchHoldSet`, instead of loose fields. It behaves the same, and it can be tested without a scene. It is a public nested type, so it is part of the core API surface; it could be made `internal` only by giving up the tests.
- `RegisterTurnSwitchHold` ignores null owners and any call after `_levelEnded`. A hold registered during the end-of-level flow would otherwise only stall a switch that no longer matters until the watchdog clears it. This is a small addition to the plan.
- The watchdog counts only consecutive frames where the holds alone block the switch:
  - the check is the last `||` term in the wait, so it isn't evaluated on frames where an action or sequence blocks;
  - a skipped frame restarts the timer.

  Without this, a Masher answer running (the controller is busy) would eat into the 5 s, and a long chain of answers would trip the watchdog falsely. Real time uses `Time.realtimeSinceStartup`. When it fires, it clears all holds and logs one warning, which names each owner as `name (Type)`, or `destroyed Type`, or `ToString()`.
- The test file goes in the existing `Core/Interactions/Editor/` (next to `InputLockTests`), not a new `Core/Managers/Editor/`, to avoid a new folder and folder `.meta`.
- I wrote both new `.meta` files myself (the minimal `fileFormatVersion` + `guid` form used by the project's other script metas, fresh GUIDs), so the commits are complete before Unity imports the files.

## Needs THJ

None for C1. One thing for the coordinator before C4 (see the first loose end).

## Docs to update

- `tech/core-systems.md` / `tech/combat-architecture.md`: `CombatLevelRunHandler` has a public turn-switch hold API (`RegisterTurnSwitchHold` / `ReleaseTurnSwitchHold` / `HasTurnSwitchHolds`) with a 5 s real-time watchdog. Holds are cleared on level end and destroy. The class is now partial (`CombatLevelRunHandler.TurnSwitchHolds.cs`).
- `build-log.md`: C1 section (coordinator).

## Risks and loose ends

- **For C4 (important):** the line-96 wait alone doesn't close the enemy-turn race D-101 is about. It only helps when the answer has already started when the loop reaches line 96. The sequence:
  1. `TryTakeAction` clears `IsInProgress` and raises `abilityPerformed` in the same callback.
  2. The AI loop leaves line 118 and reaches line 96 in the next frame (or the same frame), then calls `PrepareUnitTurn`.
  3. The planned pump waits for idle plus one extra frame, so the AI usually starts computing first.
  4. `TryPlayFactionRole` then refuses while `AIController.isActionInProgress` is true, because that includes `_factionBrain.IsComputing`.
  5. When the brain finishes, there is a same-frame window. If the pump's check runs after `IsComputing` turns false but before the AI coroutine resumes at line 107, the answer starts first. Then `PerformAction` reaches `TryTakeAction`, which returns early (:948, `IsInProgress` is already true), and `PerformAction` still returns true.
  6. The loop then waits on line 118 and replans. But the phase state was already advanced to TakeAction with the stale ability and targets, so the next `PerformAction` goes straight to `TryTakeAction` with the old plan.

  Suggestions for C4:
  - (a) the pump retries when `TryPlayFactionRole` returns false (it must anyway);
  - (b) on the enemy turn, only start an answer when the AI controller's `isActionInProgress` is false **and** has stayed false for a frame;
  - (c) or, a follow-up core change: the AI loop re-checks `PhaseData.IsInProgress` right before `PerformAction`, and discards the plan (without advancing phase states) if an answer slipped in.

  I didn't build any of these: they are outside C1 and would change behaviour.
- The outer waits at lines 73 and 83, and `TrySelectUnit` → `CleanupUnitTurn()`, don't wait on `PhaseData.IsInProgress`. If an answer is still running when the AI moves to the next unit, `Cleanup()` runs phase-state cleanups during the answer. That was already true before this change (C1 didn't touch it). The verifier should watch for it in the "Mark's chain on the enemy turn" case.
- `SwitchTurnIE` doesn't wait on `QuickTimeEventHandler.IsEventActive`, but the C4 pump does. If a QTE could be open while no controller is busy and a hold is up, the watchdog could time out while the player is still reacting. I believe QTEs only run inside an action (the controller is busy), so the timer doesn't run then. Unverified.
- The watchdog uses real time, so it also runs while the game is paused (`timeScale` 0), if the switch is waiting on holds alone at that moment. The pump's frame wait still advances when paused, so this should resolve on its own. Unverified.
- I couldn't verify in the editor: the console compile, the Test Runner run, or any play behaviour. No hold is registered until C4, so there's nothing to see in play yet.

## Proposed commits

1. `fix(ai): AI turn loop waits for its own action in progress before planning the next action` (core). Files:
   - `miso/Assets/_Project/Core/Interactions/Runtime/AIController.cs`: hunk `@@ -95,7 +95,8 @@`. The `WaitWhile` in `HandleUnits` gets `|| PhaseData.IsInProgress` (1 line changed, 1 added).
2. `feat(turn-flow): add turn-switch holds so pending reactions finish before the turn switches` (core). Depends on nothing in commit 1. Files:
   - `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs`: 3 hunks, +4 / −2:
     - `@@ -70,7 +70,7 @@`: `class` → `partial class`;
     - `@@ -459,7 +459,8 @@`: `|| IsTurnSwitchHeld()` in the `SwitchTurnIE` wait;
     - `@@ -653,6 +654,7 @@`: `ClearTurnSwitchHolds()` in `EndLevel`.
   - `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs` + `.meta` (new, 116 lines).
   - `miso/Assets/_Project/Core/Interactions/Editor/TurnSwitchHoldTests.cs` + `.meta` (new, 10 tests).

   The tests could be a third commit, but they only compile with commit 2, so I'd keep them together.

All `.cs` files touched or added are UTF-8 with BOM and LF, matching the existing two files. Check `git status` after Unity imports: if Unity rewrites either new `.meta` (it shouldn't), stage its version.

## Other branches

`thj/home-test` needs both commits when the Masher work merges there (per the plan's Risks; coordinator notes it in `branches.md`).

## How to see it

1. Focus the editor and let it recompile (Ctrl+R). The console should show no errors.
2. Window > General > Test Runner > EditMode > Run All. `TurnSwitchHoldTests` (10 tests) should be green, and the only red test should be `AIRegressionTest.Baseline_MatchesCurrentAI`.
3. Play any combat level (e.g. `Generic Levels/Easy/E3/LevelE3-C1`) through a few player and enemy turns. Turn flow and AI pacing should feel exactly as before: nothing registers a hold yet, and the AI wait is a no-op without a Masher answer.
4. Optional sanity check of the watchdog: during the player's turn, run `CombatLevelRunHandler.Instance.RegisterTurnSwitchHold("test")` from a debugger or a temporary cheat, then end the turn. The switch should stall for about 5 s, then a warning naming `test` appears and the turn switches.
