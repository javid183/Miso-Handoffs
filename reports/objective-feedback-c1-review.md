# Review: objective feedback C1 (tick, pulse, sound)

2026-11-10, `miso-reviewer` (read-only; saved by the coordinator). **Verdict: FIX.**

## Must fix

1. **The level-winning objective still plays the met sound after the HUD hides** (breaks D-477). `HideHUD` → `ObjectivesPanelUI.Hide` only slides the panel off (`UIPanelAnimator.Hide`, `DOAnchorPos`); the GameObject stays active, so the `UpdateObjectives` coroutine runs on: 1 frame + 1 s delay + `Show` + strikethrough → `PlayMetFeedback` ~2–3 s after the win, while `EndLevel` hides the HUD at ~0.25 s + 0.5 s slide. Click sound with no line visible, on every won level. Same when a `HUDSequence` hides the HUD during a stage-complete sequence. Fix (Features only): a "feedback allowed" state on `ObjectivesPanelUI`, cleared when `Hide` starts, set in `Show`; the entry skips `PlayMetFeedback` when false; add `panelVisible` to the pure rule + a test ("panel hidden, line met, no pulse"). Trade-off: a stage-completing line met while a sequence hides the HUD loses its pulse (strikethrough only). Files: `ObjectiveEntryUI.cs` 76-84, 105-118; `ObjectivesPanelUI.cs` 98-118, 125-130.

## Should fix

1. `AudioStorage.asset` hand-edited YAML (valid; placeholder = `A_UI_Click` clip GUID); report should say so and say 4 lines, not 3. THJ swaps the clip in the inspector.

## Notes

- Flag carry-over across the rebuild works (matched by `LevelObjective` reference); stage-completing line pulses once; old met lines silent; defeat/ongoing never pulse; a line met before its first `Show` won't pulse (acceptable).
- Overlapping coroutines: no double pulse; pulse resets scale before starting.
- DOTween: `SetLink`, killed in `OnDisable`/`OnDestroy`; fine.
- Pre-existing: an old `UpdateObjectives` coroutine can walk destroyed entries after a rebuild (`MissingReferenceException` on TMP); not caused here.
- No core, no statics, BOM/LF kept, no private IDs; one commit.
