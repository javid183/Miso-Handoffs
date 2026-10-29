# Report: Ability pause-frame skip (an ability fires before its target is picked)

Plan: plans/2026-10-29-ability-pause-frame-skip.md    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 19f75ff0d), scope all
Outcome: done (code and tests written; not compiled or run by me: the editor is open, THJ compiles and runs the suite)

## Root cause (confirmed by reading)

- `PlayerController` target selection calls `RuntimeAbility.HandleTargetSelectionAnim(true)`. For `TargetSelectionAnimationMode.PauseFrame` this plays the ability clip with `OnAnimationFrame` as the frame callback. `_activationRequested` is false and `_targets` is null on the first use, or still holds the last use's targets.
- `EntityAnimationHandler.HandleFrameAction` reads the animator's current frame once per Update and runs every frame it missed in one loop. On a slow frame the animator can jump from below the pause frame (5 for Explosive Arrow) to at or past the activation frame (7).
- In that loop, frame 5 calls `OnAnimationFrame`, which calls `AnimationHandler.Pause()`. `Pause()` only sets flags and `animator.speed = 0`. Nothing tells the loop to stop, so it goes on to frame 7. The activation event (added in `RuntimeAbility.Initialize`) calls `_ActivateAbility()`, which starts `preset.Activate(..., _targets, ...)`. `AbilityPreset.cs:391` is `foreach (var target in targets)`, which throws a NullReferenceException on null. After an earlier use, the same skip fires silently at the old targets instead.
- I found two more ways for the same activation to run before confirmation. I didn't change the first; the guard now blocks both:
  - `Play(..., flushRemainingEvents: true)` while the clip is paused runs the frames left after the pause, the activation frame included.
  - `HandleTargetSelectionAnim(true)` can be called again while the clip is held (TargetSelectionState.OnEnterState with no targets picked). It then calls `Resume()` without a confirmation.
- `Pause()` has exactly one caller, `RuntimeAbility.OnAnimationFrame` (RuntimeAbility.cs:453). `Resume()` has one too: `RuntimeAbility.PlayAbilityAnimation` (line 513). The other `Pause()`/`Resume()` calls in the code base are `ATBGauge`'s (GUnit.cs:1340, 1349), a different class.

## What changed

- `Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs` (core): the class is now `partial`.
  - New flag `_heldAtPause`: `Pause()` sets it; `Resume()` and every `Play` clear it (in `Play`, after the flush, so a pause raised by the flush itself can't carry over to the new clip).
  - The catch-up loop is now a call to `CatchUpFrames`. The loop stops at the frame whose callback paused the clip, and `_lastFrame` is set to that frame.
  - While held, `HandleFrameAction` returns before running any frame callbacks or the end-of-clip `Stop()`. The `_playReady` re-acquire still runs first, as before, so a `Play` with flush during the hold behaves as it did before.
- `Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.FrameCatchUp.cs` (new, core): the `_heldAtPause` field, two delegates cached per handler (so the per-frame catch-up allocates nothing), and the pure `public static int CatchUpFrames(currentFrame, totalFrames, isLooping, Func<int> lastFrame, Func<int,bool> invokeFrame)`. It keeps the old loop's behaviour exactly, including two quirks:
  - The loop bound reads the last frame live, so a callback that starts a new play cuts the catch-up short.
  - A looping clip that wraps through frame 0 runs one extra frame.
- `Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs` (core): the activation event's listener calls `OnActivationFrame()` instead of `_ActivateAbility()`. One line.
- `Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.ActivationFrameGuard.cs` (new, core): the pure rule `public static bool ShouldRunActivationFrame(pausesForTargetSelection, activationRequested, hasTargets)`, true when there are targets and (the ability doesn't pause for target selection, or activation was requested). `OnActivationFrame()` applies it:
  - When it passes: `_ActivateAbility()`, as before.
  - PauseFrame without a confirmation: skips and sets `_abilityAnimationPlayStarted = false`, so the confirm plays the clip again from the start instead of resuming a clip that has already passed its activation frame. Without this, a skip could lock the turn.
  - Confirmed but `_targets` null (not reachable today: `Activate` always sets targets): skips and logs an error naming the ability.
- `Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerCatchUpTests.cs` (new): 11 tests of `CatchUpFrames`.
- `Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityActivationFrameGuardTests.cs` (new): 4 tests of `ShouldRunActivationFrame`.
- Four `.meta` files for the new scripts, written by hand with fresh GUIDs.

Line endings and BOM: every touched or new file is LF. The runtime files and the abilities test have a BOM, like their neighbours; the animation test has none, like its neighbours. No new statics: the static members are pure methods, and the new fields are per instance. No private IDs in code or test names.

## Why the resume can't skip or double-fire

- **Before confirmation.** The catch-up stops at the pause frame with `_lastFrame = 5`, whatever frame the animator reached during the slow frame (call it F, F >= 5). The animator is then frozen at F (speed 0). While held, Update does nothing, so frames 6 to F stay pending and the end-of-clip `Stop()` can't throw the paused clip away.
- **After confirmation.** `Activate` sets `_targets` and `_activationRequested`, then `PlayAbilityAnimation` calls `Resume()`, which clears the hold. The next Update catches up from frame 6:
  - If F is still before the end, it runs 6..F (and later frames as the clip advances). Frame 7 runs exactly once, now with targets.
  - If the slow frame already took a one-shot clip past its end, the frame reads as wrapped. The non-looping wrap branch then runs 6..last, so frame 7 still runs exactly once, followed by the usual end-of-clip `Stop()`.
  - In both cases `_lastFrame` is then past 7. The only way back to 7 is a looping clip wrapping round, which is the same as today. On that wrap the pause frame doesn't pause again, because `_activationRequested` is true.
- **Guard.** Before confirmation the activation frame can't fire in PauseFrame mode, even with leftover targets. If it is ever reached early (flush or re-entry, above), the skip resets the "clip started" flag, so the confirm replays the clip and the ability fires once. It doesn't hang.
- **Abilities that don't pause.** For them the guard only checks `_targets != null`, and `Activate` always sets it before the clip plays. `_heldAtPause` is only ever set by `Pause()`. For them, the extracted loop runs the same frames as before (tests below).

## Acceptance criteria

- [x] A frame jump across the pause and activation frames stops at the pause; activation runs once, only after confirmation, on the chosen targets. Tests: `SlowFrame_JumpingPastPauseAndActivation_StopsAtThePauseFrame`, `Resume_AfterTheSlowFrame_RunsTheActivationFrameOnce`, `Resume_AnimatorAlreadyPastTheEndOfAOneShotClip_RunsTheRemainingFramesOnce`, `Resume_AnimatorStillOnThePauseFrame_RunsFramesAsTheClipAdvances`, `PauseOnFrameZero_StopsAtFrameZero`, `PauseWhileRunningTheEndOfAOneShotClip_StopsAtThePauseFrame`. Needs THJ's play check at 10 fps.
- [x] No NRE and no firing at stale targets. Tests: `PausesForTargets_NotConfirmed_DoesNotRun` (no targets, and leftover targets), `NoTargets_NeverRuns`, `PausesForTargets_Confirmed_Runs`. Needs the play check.
- [x] Abilities that don't use PauseFrame behave exactly as before. Tests: `NoPause_RunsEveryMissedFrame`, `NoPause_FirstFrames_RunFromFrameZero`, `NoPause_OneShotClipReachingItsEnd_...`, `NoPause_LoopingClipWrappingThroughZero_RunsTheSameFramesAsBefore`, `NoPause_CallbackStartingANewPlay_CutsTheCatchUpShortAsBefore`, `NoPauseForTargets_WithTargets_Runs`. Needs the play check at normal fps.
- [ ] EditMode suite green except the known red: **not run by me** (the editor is open). 15 new tests. THJ: Ctrl+R, then Test Runner > EditMode > Run All. Expect only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

## Save reset

No.

## Decisions I made

- I pulled the catch-up loop out into the pure static `CatchUpFrames` so the tests drive the real loop, not a copy. It keeps the old loop's live bound and its looping off-by-one exactly (same behaviour, a different shape).
- While held, `HandleFrameAction` also skips the end-of-clip `Stop()`, not just the frame callbacks. Without that, a slow frame past the clip's end would swap the paused clip for idle. The later `Resume()` would then land on idle, and the ability would never fire and would lock the turn. The plan's "resume must fire exactly once" needs this.
- The guard's PauseFrame skip resets `_abilityAnimationPlayStarted`, so the confirm replays the clip rather than resuming one that is past its activation frame. This is the plan's "a skipped activation can't leave the ability or the unit hanging".
- The hold check comes after the `_playReady` re-acquire, so a `Play(..., flush)` during the hold still flushes the remaining frames as it did before. The guard then blocks the activation in that flush and lets the confirm replay the clip.
- The confirmed-but-no-targets branch logs an error instead of throwing a NullReferenceException. It is unreachable today.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md`, Abilities row: `RuntimeAbility`'s activation frame runs only with targets, and, for PauseFrame target selection, only after confirmation (`RuntimeAbility.ActivationFrameGuard.cs`). `EntityAnimationHandler` is not on the core list, but the plan treats it as core; the coordinator decides whether to add it with a note: the catch-up stops when a frame callback pauses the clip, and a held clip runs no callbacks or end-of-clip stop until it resumes or a new clip plays.

## Risks and loose ends

- **Backlog item on the activation frame** (status.md, filed 2026-10-18: an `abilityActivationFrame` at or past the clip's last frame freezes an ability; the line numbers quoted there are from an older file). This change doesn't touch it or make it worse.
  - The activation event still never fires when its frame is outside the clip, exactly as before.
  - In PauseFrame mode the pause frame is clamped to at most activation - 1. If that is also past the clip's end, the pause never happens and the outcome is the same as today.
  - The hold only exists after a pause that really happened.
- **A pause that stays on after a cancel (not changed).** `_paused` stays true after a cancelled PauseFrame selection: `Stop()` restores the speed but never clears `_paused`. Because `Play` only sets `animator.speed` while `!_paused`, later clips keep the speed captured at `Pause()` (the idle speed jitter, for example, isn't applied) until the next `Resume()`. The same holds when a `Play` comes in during a hold: the new clip stays at speed 0. I didn't rely on `_paused` for that reason; the new `_heldAtPause` is cleared by every `Play`.
- **Looping wrap off-by-one (not changed).** When a looping clip wraps through frame 0, the catch-up runs one frame past the current one. That frame then runs again on the next Update, so a callback on it can fire twice. A test pins it as it is; a fix is a separate change.
- If Unity imported the new scripts before my `.meta` files existed, it may have written its own GUIDs. Check `git status` shows one `.meta` per new script.
- `AIRegressionTest` and AI code are untouched.

## Proposed commits

1. `fix(abilities): an ability that pauses for target selection no longer fires before the target is picked on a slow frame` (core, one commit)
   - miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs
   - miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.FrameCatchUp.cs
   - miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.FrameCatchUp.cs.meta
   - miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs
   - miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.ActivationFrameGuard.cs
   - miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.ActivationFrameGuard.cs.meta
   - miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerCatchUpTests.cs
   - miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerCatchUpTests.cs.meta
   - miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityActivationFrameGuardTests.cs
   - miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityActivationFrameGuardTests.cs.meta

Not part of this commit: the files already modified before this task (two LevelLucyJohn prefabs, GlobalSettings.asset, EditorSettings.asset, ProjectSettings.asset).

## Other branches

`main` (the plan's scope is all branches; THJ ports it). `EntityAnimationHandler.cs` and `RuntimeAbility.cs` are identical on `main` and on this branch's HEAD (`git diff --stat main HEAD` shows nothing), so the commit should apply cleanly.

## How to see it

1. Stop Play mode if it's running, focus Unity and press Ctrl+R. The console should show no compile errors.
2. Window > General > Test Runner > EditMode > Run All. Expect the 15 new tests (`EntityAnimationHandlerCatchUpTests`, `RuntimeAbilityActivationFrameGuardTests`) to pass, and only `AIRegressionTest.Baseline_MatchesCurrentAI` to be red.
3. Cap the frame rate at 10, using a cheat or a temporary `Application.targetFrameRate = 10`, or the Game view's VSync / frame-rate setting.
4. Start John's Map level 2, from a fresh launch too. Pick Linda's Explosive Arrow several times:
   - Linda's clip always holds at its aim pose (it may hold a frame or two later than the pause frame at 10 fps) and nothing fires.
   - On confirming a target, the arrow fires once, at that target.
   - Cancel and pick again: no stray shot at the previous target.
5. At normal fps, play the bow primary, Crescendo and a few other units' abilities: they look and time exactly as before.
