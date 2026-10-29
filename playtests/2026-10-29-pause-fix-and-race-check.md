# Play check: Explosive Arrow pause fix and the AI restore-race diagnostic

For THJ, 2026-10-29. Branch `thj/linda-quiver`. Both are uncommitted.
- **Pause fix (core, reviewed):** gets committed after this check (D-311).
- **Diagnostic:** temporary and never committed (D-312).

## Before playing

1. Stop Play mode, then press Ctrl+R. You should see no compile errors.
2. Run EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. The new tests are `EntityAnimationHandlerCatchUpTests` and `RuntimeAbilityActivationFrameGuardTests`.

## A. Explosive Arrow (pause fix)

3. Cap the frame rate at 10 (for example a temporary `Application.targetFrameRate = 10`). Start John's Map level 2.
4. Pick Explosive Arrow several times:
   - Linda holds her aim pose and nothing fires.
   - When you confirm a target, it fires once, at that target.
   - Cancel and pick it again: no stray shot.
5. Back at normal fps: the bow, Crescendo and a few other units' abilities look and time as before.

## B. Goblin on the wrong tile (diagnostic)

6. **Widen the window** (optional, it helps a lot): open Window > Analysis > Profiler, tick Deep Profile, and press Record. It makes the AI planning much slower, so the race window is wider. Turn it off afterwards.
7. Play "Ryker is lost" level 3, with several enemies alive.
8. **Trigger it:** have John Shield Dash into an enemy so the push moves it, ideally more than one tile. Then act with Lucy straight away so her FR fires. Repeat a few times.
9. **Watch the Console** for `[AI-RESTORE-RACE] ...`. If it appears, try Lucy's basic attack on the pushed enemy. Send me the Console lines and the combat log.
10. **If it doesn't appear:** after several tries with Deep Profile, the race becomes unlikely and I'll look elsewhere. A warning from another ability (a pull, a knockback, a Masher step) also counts; say which ability it was.
