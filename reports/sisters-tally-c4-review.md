# Sisters' tally C4: review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Two should-fix (second optional). THJ's play check still needed.

## Should fix

1. `Editor/SistersTallyStepTests.cs` 140-151 and 189-202: the test counter has no `CanvasGroup`, so `FadeOut` stops at its guard (`SistersTallyCounterUI.cs:80`). `FadeOut_WithTheHudHidden_EndsHidden` and the "back with the HUD" assert in `Return_AfterTheFade_...` pass without the fade running. Add a `CanvasGroup`, `DOTween.Complete(group)` after the first `MoveNext`, and assert show-alone ended and the counter shows after return; or rename and drop those asserts.
2. (Optional) `SistersTallyCounterUI.cs:80`: an early stop in `FadeOut` after `ShowAlone` leaves `_shownAlone` true (invisible in play, alpha 0). On early stop, set `_shownAlone = false` and slide back.

## Notes (verified)

- Every step checks `Enabled` first; nothing before the check raises `Changed`.
- No hang: missing counter, not eligible, already faded, failing save or listener (caught, tested), pause mid-fade (`SetUpdate(true)`, tested). The show-alone slide (Core `UIPanelAnimator`, scaled time) only waits for resume. `SkipStep` has no callers.
- Level end or restart mid-fade: scenes unload, a fresh counter appears; an interrupted fade never marks.
- Faded rule unchanged; marks keyed by distinct asset names; `PlayJustOnce` 0; no new statics.
- `Resources/Sequences/SistersTally/` fits the feature-folder pattern.
- Trail wiring: 8-step order matches; lines, speakers, sides, delays preserved; pick line `SpeakAsThePick(endLines, 1)` right; idempotent; old asset GUID now holds Linda's line only.
- `LevelBase.prefab`: exactly 2 reference lines. Commit 1 alone doesn't change behaviour.
- Tests: the old pile test change is legitimate; the order test pins all 8 positions and that return is absent.
- No core edits, no private IDs, LF, no BOM. Two-commit split builds in order; file lists complete (incl. folder meta and Reply asset meta); THJ's files excluded.
- Designer FYI: The Trail's results panel never shows the tally rows (fade marks during the outro); MVP returns.
- Not verified: EditMode not re-run; not played.
