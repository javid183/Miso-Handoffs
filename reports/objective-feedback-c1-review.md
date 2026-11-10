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

## Re-review after rounds 5–6 (2026-11-10)

(Pasted by the coordinator; the reviewer runs read-only.)

**Verdict: FIX.**

Must fix: (1) `ObjectiveEntryUI.cs:96,115-120`: a line already on screen and met while hidden keeps the struck rich text from `UpdateVisuals`, because the Defer branch only resets the colour. It slides back in struck, then goes plain and strikes again. Fix: call `UpdateVisuals()` in the Defer branch after `_pendingFeedback` is set. The win line on screen is unaffected (the panel is off screen at about 0.75 s, the decision comes at about 1 s). (2) `ObjectivesPanelUI.cs:122-128`: in a stage advance with the HUD visible, the new line's arrival and sound start in the same frame as the met pulse and sound. Before `Show` on an `ArrivalPending` entry, wait while any entry `IsPlayingFeedback`.

Checks: the win line is still struck on screen at the moment of the win (`UpdateEntries` → `UpdateVisuals`, not pending), same as HEAD; the report's "stays unstruck" is inaccurate. `NewLines` is safe because `VisibleWinObjectives` is cumulative; edge: an advance from an empty visible list gets no arrival. No stuck-invisible paths; colour restored on disable and on met-before-arrival. No statics. AudioStorage valid, 8 lines, placeholder clip. No private IDs; LF and BOM as HEAD.

Notes: the outro `ShowHUDSequence` risk is still unchecked. Pacing differs between the visible path (one at a time, 1 s apart) and return from hidden (all together). Not checked in Play.

Coordinator follow-up: `ShowHUDSequence` is referenced by `Sequences/Common/OutroCutscene.asset` and `OutroCutsceneKeepGridHidden.asset` (the shared win outros), so the risk is real; sent to the implementer with the two must-fixes.

## Re-review after round 7 (2026-11-10)

(Pasted by the coordinator.)

**Verdict: FIX.**

Must fix: (1) The win line shows unstruck during the outro. `_levelEnded` is set in the frame of the win, so at about 1 s the entry's Defer branch (`ObjectiveEntryUI.cs:116-120`) makes the struck win line plain. The outro's `ShowHUDSequence` then slides the panel back in with the line plain, and `DropAllPendingFeedback` (`ObjectivesPanelUI.cs:159-162, 204-209`) only runs after the slide-in and clears flags without restyling. HEAD showed it struck. Dropped new lines also stay at `HiddenColor`. Fix: `DropPendingFeedback` restores `defaultColor` and calls `UpdateVisuals()` when shown; `ObjectivesPanelUI.Show` drops pending feedback before the slide-in when `LevelEnded`.

Checks: the two earlier must-fixes are done (`ObjectiveEntryUI.cs:119`, `ObjectivesPanelUI.cs:129`). (a) Try Again, level change and sandbox restart unload all scenes and reload `CombatLevelContainerScene`, so the handler is fresh each time; a stale `_levelEnded` is impossible. (b) `_levelEnded` is set in `UpdateObjectives` before `EndLevel` and `UpdateEntries` on win and loss, and also by `EndLevel` and the win cheat; that is before the Defer decision and before any outro ShowHUD. (c) Read-only use of the existing public `IsLevelEnded`; handler unchanged; stateless static property. Pacing on return matches the visible path. No private IDs; LF and BOM as HEAD. Not checked in Play.
