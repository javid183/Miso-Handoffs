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

## Re-review after rounds 2–4 (2026-11-10)

**Verdict: APPROVE.** No must-fix.

Should fix (after THJ's play): (1) `ObjectiveEntryUI.cs:117` orphaned comment: move above `PlayMetFeedback` (~130) and say "scale pulse, colour flash and one UI sound". (2) `PlayStrikethrough` (~152): call `StopPulse()` at the top next to `_strikethroughTween?.Kill()`, so a running pulse can't overwrite the per-character reveal.

Notes: pending plays once (flush clears first; deferred entries have `_seenUnmet` false); Show/Hide races handled; revealing entries play via their own decide; level win defers and never flushes (unchecked risk: an outro containing a `ShowHUDSequence` would flush it); end panel doesn't use `ObjectiveEntryUI`; restart / Try Again / next level unload scenes, no carry-over; rich-text re-tint rebuilds from `_displayText`, no nested tags, restores success colour; tween cleanup fine; no core, no statics; BOM/LF as HEAD; `AudioStorage.asset` hand-edited (4 lines, placeholder clip). Minor: feedback allowed from the start of the slide-in (cosmetic).
