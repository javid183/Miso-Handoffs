# Review: feedback pass C4 (low-HP state and presenter)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins` (C1 `07f4e44fe`, C2 `8d531ec64`, C3 `616af0754` + `ee2613f59`).
Plan: `plans/2026-10-22-feedback-pass-tech.md` C4 (D-146, D-147). Implementer report: `reports/feedback-c4.md`.

**Verdict: FIX** (one must-fix; sent back with the two should-fixes). The three calls the coordinator accepted (turn-start beat waits for the banner, max 4 s; an announcement extends a running single cycle and keeps its sting; pause = `timeScale == 0`) are implemented soundly.

## Must fix

1. **A lethal hit from above 25% counted as a crossing.** `RuntimeAAttribute.SetValue` raises `onValueChanged` before `onMinReached` (`RuntimeAAttribute.cs:65-83`), and only `Die` sets `IsAlive = false` (`GUnit.cs:775`). So the bar saw alive + health 0 and played the sting and 3 cycles on a death. Fix: health at the minimum is never low (`health > 0f` in `LowHealthRules.IsLow`), plus a test.

## Should fix

1. **The sting played even when the announcement was dropped** (`LowHealthPresenter.cs:197-200`): two crossings on one hit would play two stings over one run once a sound is set. Fix: play it only when `Request` returns true.
2. **The live-turn flag wasn't cleared on turn end** (`LowHealthCadence.cs` + bus hooks): `StartTurn()`'s auto-select fires before `turnStarted` (`CombatLevelRunHandler.cs:528-529`), so a player-twice-in-a-row turn could play a selection cycle under the banner. Fix: clear on `turnEnded`, plus a test.

## Notes

- **Turn 1 has no banner** (`CombatLevelRunHandler.cs:194-197` starts it without `PlayPhaseAnimation`), so the level-start announcement plays as turn 1 begins, while the HUD slides in. Fine by the design; the report's play step was corrected. A tutorial at turn 1 freezes the clock and vignette correctly (the sting has already played).
- **Resurrect differs by death path:** revived in place (`DieRevivable`, `OnHeal`) keeps the known state, so coming back ≤ 25% is a crossing and announces; deactivated then `Resurrect`ed forgets it (not a crossing). Both defensible; THJ may want them to match.
- **Max-HP buffs/debuffs can cross** with no hit and announce (by design).
- **Mid-level join:** a crossing between a unit enabling without `unitBorn` and the next rescan plays no announcement (the bar still pulses). Narrow; check Toba's join in play.
- **Sound:** banner lock is taken before `turnStarted`; the wait is a poll on the pause-aware clock and holds nothing. Extend-not-drop and the pause rule as accepted. Vignette canvas order −1: under the HUD canvas (Overlay, 0), over the world and world-space bars/panels; raycasts off; its own canvas so the volume red flash can't erase it; generated texture and sprite destroyed in `OnDestroy`. Presenter: bus re-bind like C2's; bars unsubscribed before rescans, on bus change and destroy; no coroutines, tweens, statics or AI exposure; empty ids play nothing. Bar pulse: player units only; colour restored on clear, death and `OnDisable`.
- **Scenes:** only the new object plus one child entry under `---Management---`; unique fileIDs.
- **Conventions:** LF; BOM only on `LowHealthRulesTests.cs` like its neighbour; namespaces and `Editor` folders match; no private IDs. One commit; leave `Packages/*`, `ProjectSettings/*` out.
