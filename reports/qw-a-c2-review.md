# Review: quick wins C2 (John's shield animation variants)

Reviewer: miso-reviewer (read-only; saved by the coordinator)    Branch: thj/quick-wins    Date: 2026-10-21
Verdict: **APPROVE**

## Must fix

None.

## Should fix

1. `EntityAnimationHandler.cs:263-275` `ReplayIdleIfPlaying` checks only that the current state name is the idle, then replays with no frame callback and `flushRemainingEvents: false`. If anything ever plays the idle state with frame callbacks (an ability whose state name is `Idle`, or a frozen state), a tag change mid-ability would drop its remaining frame events, activation included, and hang the ability. Latent today (nothing on John does it). Fix: `if (_actionOnFrame != null || _freezeOnEnd) return;` before the replay.
2. `JohnShieldRelay.cs:74-78` subscribes `unitDied` / `levelEnded` only if `GlobalEventBus.Instance` exists at `OnEnable`. Death is still covered (tag removal raises `OnTagRemoved`; `SyncShieldPose` checks `IsAlive`); level end is not. Low stakes: subscribe lazily, or accept and note it.

## Notes

- With no suffix set, `Play`, `IsPlaying`, `HandleFrameAction` / `_playReady`, `Stop()` and return-to-idle behave as before. `HasState` checks layer 0, the layer `Play` uses. The controller is unchanged since THJ's `3ae174a93` (no transitions or parameters added).
- Shield Up gains its tag during `Taunt`, so no mid-ability replay; the pose arrives when `Taunt` ends.
- Death doesn't fight the Die animation (current state is `Die` when the variant clears; no `Die_Shield`).
- Subscriptions symmetric (OnEnable/OnDisable; OnDisable clears the variant). No statics (`ShieldStateSuffix` is a const). Not read by the AI.
- Frame timing confirmed: shielded attack clips 8 frames at 10 fps (0.8 s), normal 12 frames (1.2 s); `Unit_John.prefab` abilities[0] activation frame 4 with its event at frame 4, inside 0 to 7. `Run_Shield` 8 frames at 12 fps (loop, 2 SFX events); `Idle_Shield` 8 at 7 fps (loop).
- Line endings: all four files LF; `EntityAnimationHandler.cs` keeps its BOM. `.meta` GUID unique. No private IDs.
- One commit is fine (handler not core); optional split handler+tests / relay.
- Untested by EditMode: the idle-replay path and the `IsPlaying` alias (play check).
- Known edges: `PlaySwitchAnimation` compares the plain switch name; a variant change during a QTE pause replays the idle at animator speed 0; shorter shielded attack recovery (feel point for THJ).
