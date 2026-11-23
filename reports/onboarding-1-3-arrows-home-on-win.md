# Report: Chunk 1.3, Linda's arrows come home when a level is won

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.3, item H-08)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: **built** (second session, after THJ's D-627 on the hook). Core event plus feature, all covering tests pass and the full EditMode suite passes, apart from the known GridToLevel flake, which passes when rerun alone. The play check is still to do (timing against the outro, how the flight looks).

## What changed

- **Core (Tier 3, D-627):** a new bus event, `GlobalEventBus.levelWonBeforeOutro` (a plain `UnityEvent`). `CombatLevelRunHandler.EndLevel` raises it as its first step on a win, before any wait, the HUD hide, the resurrection or the outro. `levelEnded` and everything else keep their behaviour and timing.
- **Feature:** on that event, every grounded arrow of Linda's goes back into her quiver at once, then flies home with Encore's flight and chunk 1.5's gold glow and trail. No AP, no Encore cast, no bark. Nothing happens on a loss, with no field, with the quiver switched off, with Linda dead or with a full quiver.

## The name

`levelWonBeforeOutro`: the name says both the condition (a win) and the timing (before the outro). A bare `levelWon` would sit next to `levelEnded` and invite the guess that it fires at the same time. The doc comment on the field repeats it: win only, first step of `EndLevel`, about half a second of board before the outro's first step, `levelEnded` after the outro as before.

## Exact core diff

1. `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs` (BOM, LF kept). Lines 41 to 45, under `[Header("Level-Related")]`, right after `objectivesSetAdvanced`:
   ```csharp
   // Raised on a win only (never on a defeat), by CombatLevelRunHandler.EndLevel as its first step: before the
   // HUD hides, before the fallen family is raised and before the outro (the ending sequence) starts, so a
   // listener still has about half a second of the board before the outro's first step. levelEnded comes later,
   // after the outro, as before.
   public UnityEvent levelWonBeforeOutro = new();
   ```
   No static was added (the bus's statics, `Instance` and `InstanceReady`, are unchanged and already reset).
2. `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs` (BOM, LF kept). One line, 713, in `EndLevel`, after `_levelEnded = true; ClearTurnSwitchHolds();` and before `PersistUnitStates`:
   ```csharp
   RaiseLevelWonBeforeOutro(result);
   ```
3. New partial `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.LevelWon.cs` (+ `.meta`; BOM, LF like its siblings), 26 lines:
   - `private void RaiseLevelWonBeforeOutro(LevelObjectiveEvaluationResult result)`: returns unless the result is a win, returns without a bus, invokes the event inside `try/catch` with `Debug.LogException`, so a listener that throws can't stop the level from ending (the same guard as `RaiseTurnEnding`).
   - `public static bool RaisesLevelWonBeforeOutro(LevelObjectiveEvaluationResult result)`: true only for `Win`.
4. New test `miso/Assets/_Project/Core/Managers/Editor/LevelWonBeforeOutroTests.cs` (+ `.meta`, new folder `Core/Managers/Editor` + `Editor.meta`).

It covers the real win, the cheat win (`BypassCurrentLevelWithWinResult` goes through `EndLevel`) and every level. A defeat and an ongoing result raise nothing.

## Timing (arrows back before the ending sequence's first step)

The quiver is refilled **synchronously** inside the event: `RecallRules.Resolve` calls `quiver.Add` before anything else, so the count is right in the same frame the level ends. That is at least `endLevelDelayBeforeHudHide` (0.25 s) + `HideHUD` + `endLevelDelayAfterHudHide` (0.25 s) before `PlayOutro`. The flights (`recallFlightSeconds`, 0.45 s) are only the visual that follows and normally land before the outro starts as well. If THJ shortens the end delays, the count is still right; only the last flights would overlap the outro's first step. They end by themselves, and the field closes on `levelEnded`, after the outro.

## Acceptance criteria

- [x] **New bus event, raised at the start of `EndLevel` on a win, before the outro.** Evidence: `LevelWonBeforeOutroTests.AWin_RaisesItOnce_AtTheStartOfEndLevel_BeforeLevelEnded` steps the real `EndLevel` coroutine once (by reflection) on a bare run handler. The event fires once and `levelEnded` doesn't. The routine stops at the first line that needs a running level (the player controller), well before the HUD wait and `PlayOutro`.
- [x] **Not on a loss.** `ADefeat_DoesNotRaiseIt`, `OnlyAWinRaisesIt(Win/Defeat/Ongoing)`.
- [x] **Purely additive.** One field, one call line, one new partial; `levelEnded` untouched (diff above). `NoBus_TheWinStepStillRuns`: no bus, no throw.
- [x] **On a win, every grounded arrow returns to the quiver.** `WinReturnTests.TheWinSignal_RefillsTheQuiverAtOnce_AndEmptiesTheBoard`: the bus event refills the quiver, empties the board and leaves `GroundedCount` at 0, all in the same call.
- [x] **Encore's return path and the 1.5 glow.** The same `RecallRules.Resolve` and `RecallFlight` (which calls `DressRecallFlight`). The look itself needs the play check.
- [x] **No AP, not an Encore cast.** No `RuntimeAbility` runs. `TheWinReturn_IsNoAbility_SoNoCastAndNoAp`: no `abilityStarted` and no `abilityPerformed` raised. The return kind is `Other`, not `Recall`.
- [x] **Nothing on a loss, without Linda or a field.** `LevelEndedAlone_SendsNothingHome`, `LindaDead_NothingReturns`, `QuiverOff_NothingReturns`, `NoField_NothingHappens`, `ClosedField_NothingReturns`, `FullQuiver_NothingReturns`, plus the rule table `ShouldReturn_...` (6 cases).
- [x] **Guarded for the AI thread, unsubscribes on disable.** The listener runs only on the main thread (the bus calls it from the `EndLevel` coroutine). The only value it changes that the worker thread reads is `GroundedArrowField.GroundedCount`, a plain int, already worker-safe; the rule is pure. `Disabled_StopsListening` checks that `OnDisable` removes the listener.
- [x] **Back before the ending sequence's first step.** Refill is immediate (above); the visual timing goes to the play check.
- [x] **Listener in new files.** `QuiverWinReturn.cs`, `GroundedArrowField.WinReturn.cs`, `WinReturnRules.cs`. One hunk in `LindaQuiver.cs` (below).
- [x] **EditMode tests.** 21 new tests, all pass.

Needs the verifier's play check: the flights and glow on screen, and that they land before the outro.

## Chunks

### Chunk 1.3: arrows home on a win

- First session: blocked on the hook (options in the history of this report; THJ chose a new core bus event, D-627).
- Second session, changed files:
  - Core: `Core/Managers/GlobalEventBus.cs`, `Core/Managers/CombatLevelRunHandler.cs`, `Core/Managers/CombatLevelRunHandler.LevelWon.cs` (+ `.meta`), `Core/Managers/Editor.meta`, `Core/Managers/Editor/LevelWonBeforeOutroTests.cs` (+ `.meta`).
  - Feature: `Features/Player/Linda/Scripts/Quiver/QuiverWinReturn.cs` (+ `.meta`), `GroundedArrowField.WinReturn.cs` (+ `.meta`), `WinReturnRules.cs` (+ `.meta`), `Editor/WinReturnTests.cs` (+ `.meta`), `LindaQuiver.cs` (one hunk).
- Criteria met: all, with evidence above; the look and timing need the play check.
- Decisions and loose ends: below.

## Reviews and checks

- Covering fixtures (`LevelWonBeforeOutroTests`, `WinReturnTests`): 21 of 21 passed.
- Full EditMode suite: 2550 total, 2548 passed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit), 1 failed: `GridToLevelTests.Builder_RebuildNeedsOverwriteAndKeepsTheGuid`, "m_LockCount == 0", the known flake.
- Rerun of the GridToLevel fixtures alone (95 tests): 94 passed, 1 failed, this time a different test (`GridToLevelSettingsTests.Settings_NoTierLineGivesStandardEvenWhenTheTemplateIsNot`), same "m_LockCount == 0".
- Rerun of those two tests by name: 2 of 2 passed. So the failures are the flake, not this change.
- `AIRegressionTest` not run: no AI graph, AI ability or unit prefab touched.
- No compile errors in the console after the refresh.

## Save reset

No.

## Decisions I made

- **Event name `levelWonBeforeOutro`**, a plain `UnityEvent` placed under "Level-Related"; see "The name".
- **The raise sits in a small new partial with a try/catch**, not a bare one-liner in `EndLevel`. The behaviour is the same, but a throwing listener is logged instead of killing the end-of-level coroutine. `EndLevel` gets one call line.
- **Raised right after `ClearTurnSwitchHolds()`**, before the state persistence. That is "the start of `EndLevel`". The arrows don't touch the persisted unit or item state (the quiver starts each level full), so order against persistence doesn't matter.
- **Return kind `QuiverReturnKind.Other`** instead of a new `LevelWon` value. Adding the value would mean a second hunk in `LindaQuiver.cs` (where the enum lives). `QuiverLogListener` and `QuiverReturnCue` treat any kind the same, so the behaviour is equal: the "+N" cue shows on Linda and the combat log annotates the last action line with "+N arrows, quiver N/N". Neither reads as Encore. No bark.
- **A win sibling of `RecallTo` (`ReturnAllOnWin`)** in a new partial, instead of a flag on `RecallTo`. `GroundedArrowField.Recall.cs` stays untouched for chunk 1.5's commit. It repeats about 20 lines of `RecallTo` (start positions, resolve, redraw, flights), minus the bark, with its own kind. Unlike `RecallTo`, it refills even without a grid and skips only the flights then, so it's testable in EditMode and never leaves the count wrong.
- **A separate component, `QuiverWinReturn`,** added in `LindaQuiver.Start` beside `QuiverPipsView`, `QuiverReturnCue` and `QuiverLogListener`, with its own `OnEnable`/`Start` subscribe and `OnDisable` unsubscribe. Linda's death deactivates her, which unsubscribes it; resurrection re-subscribes it.
- The core test drives the real `EndLevel` by reflection and stops at the first `NullReferenceException` (no player controller in a bare handler). That was the only way to check the raise inside `EndLevel` itself, not just the helper. If `EndLevel` later gets more setup at its top, the test still holds as long as the raise stays first.

## Needs THJ

- The play check (see "How to see it").
- The `core-systems.md` note below: THJ adds it.

## Docs to update

**`tech/core-systems.md` note (text for THJ to add):**

> Note 2026-11-23 (D-627, chunk 1.3 of the onboarding demo, `reports/onboarding-1-3-arrows-home-on-win.md`). **On `thj/onboarding-demo`.** Additive; no existing signature or timing changed:
> - *Event bus:* new `GlobalEventBus.levelWonBeforeOutro` (plain `UnityEvent`, "Level-Related"). Raised on a win only.
> - *Level run:* `CombatLevelRunHandler.EndLevel` raises it as its first step (after `ClearTurnSwitchHolds`, before persistence, the HUD wait, the resurrection and `PlayOutro`), through `RaiseLevelWonBeforeOutro` in the new partial `CombatLevelRunHandler.LevelWon.cs` (try/catch, so a throwing listener can't stop the level ending; pure `RaisesLevelWonBeforeOutro(result)`). The cheat win goes through it too. A defeat raises nothing. `levelEnded` still fires after the outro. Listeners get at least `endLevelDelayBeforeHudHide` + HUD hide + `endLevelDelayAfterHudHide` (about 0.5 s) before the outro's first step. User: Linda's grounded arrows fly home (`QuiverWinReturn`). Tests: `Core/Managers/Editor/LevelWonBeforeOutroTests.cs`. `CombatLog` doesn't listen to it.

## Risks and loose ends

- **`LindaQuiver.cs` is shared with chunk 1.4.** My hunk is separate (lines 126 to 127 in `Start`; 1.4's is at about 197 to 203, in `HasGroundedArrows`). See "Proposed commits".
- **The feature depends on chunk 1.5:** it calls `RecallFlight(Vector3, LindaQuiver, float, float)`, the 1.5 signature in `GroundedArrowField.Recall.cs`. So commit 2 must come after the 1.5 commit.
- Arrows can't travel with Linda once she's gone: if she dies on the winning blow, she's inactive when the event fires, so nothing returns. The quiver starts every level full, so nothing is lost; it's only what the player sees. Changing it would mean raising before the death handling, which is out of scope.
- The combat log line: "+N arrows, quiver N/N" is added to the last action's line (the winning blow). Harmless; listed in case THJ wants it silent.

## Proposed commits

Order: chunks 1.4 and 1.5 first (their own commits), then these two.

1. **`feat(core): raise levelWonBeforeOutro on a win, before the ending sequence`** (core, own commit):
   - `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs`
   - `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs`
   - `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.LevelWon.cs`
   - `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.LevelWon.cs.meta`
   - `miso/Assets/_Project/Core/Managers/Editor.meta`
   - `miso/Assets/_Project/Core/Managers/Editor/LevelWonBeforeOutroTests.cs`
   - `miso/Assets/_Project/Core/Managers/Editor/LevelWonBeforeOutroTests.cs.meta`
2. **`feat(linda): grounded arrows fly home to the quiver when a level is won`**:
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverWinReturn.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/GroundedArrowField.WinReturn.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/WinReturnRules.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/WinReturnTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`: **only this hunk** if 1.4 isn't committed yet. Once 1.4's commit has taken its hunk, the whole file is just this one:
     ```diff
     @@ -124,4 +124,6 @@ (LindaQuiver.Start)
                  // The combat log lines for the playtest signals.
                  if (!GetComponent<QuiverLogListener>()) gameObject.AddComponent<QuiverLogListener>();
     +            // The arrows fly home when the level is won.
     +            if (!GetComponent<QuiverWinReturn>()) gameObject.AddComponent<QuiverWinReturn>();
              }
     ```
     If 1.4 must be committed after this, stage the hunk with `git apply --cached` from a patch of just this hunk (interactive `add -p` isn't available).

## Other branches

none

## How to see it

1. Open a level with Linda (for example the `GB_m1-linda` greybox, or any level she's in).
2. Shoot two or three arrows, so they lie on the board and her quiver pips drop.
3. Win the level: clear the objectives, or use the win cheat (`BypassCurrentLevelWithWinResult`).
4. Right as the level ends, before the HUD hides: every grounded arrow flies to Linda with the gold glow and trail, the "+N" cue shows on her, and there's no bark. All arrows land before the outro's first step.
5. Lose a level with arrows on the ground: nothing flies.
6. Optional: in the combat log, the winning action's line ends with "+N arrows, quiver N/N"; no Encore cast and no AP change are logged.
