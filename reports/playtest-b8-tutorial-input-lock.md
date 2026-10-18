# Report: Playtest B8, tutorial input lock (chunk C5)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md (C5 only)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (compiles, EditMode green except the known red; play check still needed)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/InputLockSet.cs` (new, + `.meta`): small pure class. A set of lock owners (keyed by owner, so the same owner locking twice or releasing twice can't unbalance it) and a static `Effective(inputActive, locked, requested)` that gives the mode the guards should see.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerInputController.cs` (core): holds an `InputLockSet`. New `AddInputLock(object owner)`, `RemoveInputLock(object owner)`, `IsInputLocked`. `ActiveActionMode` now returns `None` while any lock is held. `SetInteractionMode` is unchanged: it still records the requested mode while locked, so the lock hides the mode without overwriting it.
- `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs` (core): `ShowTutorial` takes the lock (owner = the UI manager); `OnTutorialClosed` releases it; a new private `OnDestroy` also releases it, so a level torn down with the tutorial open can't leave input locked.
- `miso/Assets/_Project/Core/Interactions/Editor/InputLockTests.cs` (new, + `.meta`; the `Core/Interactions/Editor` folder and its `.meta` are new): 12 EditMode tests.

`PlayerController`, `CombatLevelRunHandler`, `EnemyIntroductionController` and `TutorialViewManager` are untouched.

## Acceptance criteria

- [x] While a tutorial panel is open, mouse clicks, Cancel, Switch, Toggle and Pause do nothing in combat. Every one of these goes through `ActiveCheckGuard`, which reads `ActiveActionMode`, and that is `None` while the lock is held. Tests: `Lock_BlocksEveryMode_AndRestoresOnRelease`. Needs the verifier's play check (Level 1 tutorial).
- [x] When it closes, the input mode that was active before comes back. Tests: `Lock_BlocksEveryMode_AndRestoresOnRelease` (mid player turn, `All`) and `LockBetweenTurns_ReturnsBetweenTurnMode` (`Camera | Pause`). Needs the play check.
- [x] A turn change while it is open does not turn input back on. `PlayerController` and `CombatLevelRunHandler` still call `SetInteractionMode`, but the lock hides the result until release. Test: `TurnChangeWhileLocked_StaysBlocked_AndNewModeReturnsOnRelease`.
- [x] Tutorials fired mid player turn and between turns both work: the same two tests as above. Needs the play check.
- [x] Several lockers don't clash. Tests: `TwoLockers_InputStaysBlockedUntilBothRelease`, `LockSet_SameOwnerTwice_OneReleaseUnlocks`, `ReleaseWithoutAcquire_IsHarmless`, `SaveRestoreLockerInsideTutorialLock_DoesNotLeakIntoRequestedMode` (the enemy introduction's save, set and restore running under the tutorial lock).
- [x] No new statics: the lock lives on the per-scene `PlayerInputController` instance, so no `PlayModeStaticReset` hook is needed.
- [x] Compile clean (no console errors). EditMode: 79 tests, 78 pass. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, which is known red for its old reasons (same 35 failures before and after this change).

## Save reset

No.

## Decisions I made

- **A lock that masks the mode instead of save/restore (Tier 2, core).** The plan offered either approach. Save/restore needs guards in every `SetInteractionMode` caller, and restoring a saved snapshot after a turn change would bring back a stale mode. With the mask, the callers need no change, and the lock can't lose the mode the way the `ActiveActionMode` getter does when input is inactive. Behaviour on release: input returns to the mode the game currently wants. That is the mode from before the tutorial unless the turn changed while it was open; then it is the new turn's mode, which is what the plan's risk note asks for.
- **Locks are keyed by owner rather than a bare count.** Owner keys make lock and release idempotent per owner. The tutorial already double-subscribes `OnClosed` when `ShowTutorial` runs twice; with keys, a double close can't unlock a lock someone else holds.
- **The API added to core classes is the small lock API only:** `AddInputLock`, `RemoveInputLock` and `IsInputLocked` on `PlayerInputController`, and a private `OnDestroy` on `CombatLevelUIManager`. One behaviour change: `ActiveActionMode` reads `None` while a lock is held. Today only the tutorial takes a lock.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` (coordinator): one line on the pattern: "To block player input for an overlay, call `PlayerInputController.AddInputLock(owner)` and `RemoveInputLock(owner)`. The lock hides the mode; `SetInteractionMode` calls made meanwhile still apply on release."
- `build-log.md` at the end of the batch.

## Risks and loose ends

Risks for the reviewer:
1. **`ActiveActionMode` semantics while locked.** It reads `None`, so `CameraHandler` and `CameraEdgeScroller` stop any camera movement while the tutorial is open (they gate on the Camera flag). This is intended: time is paused and the panel is modal. Check that no other reader of `ActiveActionMode` depends on it while a tutorial is open. There are 3 readers (`CameraHandler` x2, `CameraEdgeScroller`) plus `EnemyIntroductionController`.
2. **Enemy introduction snapshot.** `EnemyIntroductionController` saves `ActiveActionMode` before its sequence. If an introduction starts *while* a tutorial is open, it saves `None` and restores `None` when it finishes, even after the tutorial closes. That is the same lossy pattern as before (it already saved `None` when input was inactive). It probably can't happen, because the introduction waits on `SessionLogs.SequenceInProgress` and the tutorial runs inside a `TutorialSequence`, but I did not verify that the flag is set during a `TutorialSequence`. If it is a concern, a follow-up could move the introduction onto `AddInputLock(this)` too. I left it out of scope.
3. **Actions that aren't gated by mode still fire during a tutorial:** `ReactiveInterrupt`, `SkipLine`, `SkipDialogue`, `ShowStats`. These were never gated and aren't in the acceptance list. `ReactiveInterrupt` matters most: `PlayerController.HandleReactiveInterrupt` returns early in FTP mode (`main`'s mode), but in ATB mode it could set `Time.timeScale` while the tutorial has time paused. Worth a ticket if ATB comes back.
4. **Releases dropped while locked.** Releases that happen while the lock is held are dropped: `Move.canceled` and `Toggle.canceled` are gated too. The camera stops itself, so Move is fine. If Toggle is held when a tutorial opens and released during it, `Toggle(false)` never arrives. That was already true for any mode change that removes `Interact`.
5. **`CombatLevelUIManager.OnDestroy` is new.** Neither the class nor `LevelUIManagerBase` had one, so it hides nothing. It calls `PlayerInputController.Instance` with a Unity-null check, which is safe when the controller is destroyed first.

Loose ends:
- Not fixed, already there before this change: if `ShowTutorial` runs twice while a tutorial is open, it caches `timeScale` 0 and subscribes `OnClosed` twice, so time can stay at 0 after closing. The lock itself is unaffected.

## Proposed commits

1. `fix: lock player input while a tutorial panel is open (B8)` (core): `miso/Assets/_Project/Core/Interactions/Runtime/PlayerInputController.cs`, `miso/Assets/_Project/Core/Interactions/Runtime/InputLockSet.cs`, `miso/Assets/_Project/Core/Interactions/Runtime/InputLockSet.cs.meta`, `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs`, `miso/Assets/_Project/Core/Interactions/Editor.meta`, `miso/Assets/_Project/Core/Interactions/Editor/InputLockTests.cs`, `miso/Assets/_Project/Core/Interactions/Editor/InputLockTests.cs.meta`

It doesn't depend on C3 or C4 (uncommitted, untouched here). Line endings kept: all of these files are LF with a BOM.

## Other branches

`thj/home-test` on its next merge of `main` (as for C1 to C4). The Home's `HomeManager` uses `SetInteractionMode` only; no Home code takes a lock, so it behaves the same there.

## How to see it

1. Open Level 1 (it has a `TutorialSequence`) and press Play.
2. When a tutorial panel appears, click grid tiles behind it, press Cancel (right click or Esc, per bindings), Switch, Toggle and Pause: nothing happens in combat, and the pause menu does not open. The tutorial's own Next, Prev and Close buttons still work.
3. Close the tutorial: during the player turn, clicking a tile selects or moves as usual; between turns, camera and Pause work and clicks don't act.
4. If a tutorial fires at turn start or while the enemy plays, check that input stays dead until the panel is closed, then matches the turn (full control on the player turn, camera and Pause otherwise).
5. Tests: Window > General > Test Runner > EditMode > `MISO.Core.Interactions.EditorTests.InputLockTests` (12 tests).
