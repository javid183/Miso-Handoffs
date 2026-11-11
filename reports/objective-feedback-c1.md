# Report: Objective feedback C1 (tick, pulse, sound)

Plan: plans/onboarding/2026-11-10-objective-feedback-tech.md (C1 only)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check by THJ pending)

## What changed

- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectiveFeedbackRules.cs` (+ .meta): pure rule. `ShouldPulse(seenUnmet, nowSatisfied, mode)` (true only for Win mode, unmet then met) and `SeenUnmetAfterShow`.
- `.../Panels/Scripts/ObjectiveEntryUI.cs` (BOM, LF kept): tracks `_seenUnmet`; `Initialize(context, seenUnmet = false)`; in `Show`, after the success strikethrough, `PlayMetFeedback()` (scale pulse 1.08 over 0.3 s, then `AudioHandler.PlayUI`). New serialized fields `metSoundID` (`[AudioID(AudioCategory.UI)]`, default `A_UI_ObjectiveMet`), `metPulseScale`, `metPulseSeconds` (defaults live in code, prefab not edited). Pulse tween linked to the object, killed in `OnDisable` (scale reset) and `OnDestroy`.
- `.../Panels/Scripts/ObjectivesPanelUI.cs`: `SetObjectives` carries each line's "seen unmet" flag onto the rebuilt entry for the same `LevelObjective`.
- `.../Panels/Editor/ObjectiveFeedbackRulesTests.cs` (+ .meta): 8 tests.
- `miso/Assets/_Project/Resources/Audio/AudioStorage.asset`: new UI entry `A_UI_ObjectiveMet` (3 appended lines of YAML).

No core file touched. No new statics (no reset hook needed). Panel fold logic untouched.

## Acceptance criteria

- [x] Mid-level objective met: strikethrough, then one pulse, one sound: `Show` runs `PlayStrikethrough` then `PlayMetFeedback` only when `ShouldPulse`. Rule unit-tested; the visual and audio need THJ's play check.
- [x] Panel open: unchanged `ObjectivesFoldRules.AfterObjectivesChanged` path.
- [x] Stage advance does not re-pulse finished lines: a rebuilt entry only inherits the "seen unmet" flag, which is cleared once the line has been shown met (`SeenUnmetAfterShow`), so lines already met stay silent. Tested (`LineIsMetOnceThenRebuiltMet_DoesNotPulseAgain`, `LineFirstShownAlreadyMet_DoesNotPulse`).
- [x] The objective that completes a stage (met in the same update the panel rebuilds) still pulses, because its old entry's flag is carried to the new one.
- [x] Failure strikethrough has no success sound: only Win mode pulses (`FailureLine_DoesNotPulse`, `OngoingLine_DoesNotPulse`).
- [x] Tests green: full EditMode run 1780 total, 1779 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (known). The 8 new tests pass.
- Per D-477 the last objective of a level gets no visible tick (HUD hides first); nothing was changed for it.

## Save reset

no

## Decisions I made

- Pulse target is the entry root transform (scale 1.08, 0.3 s, out and back), modelled on `QuiverUI.Pulse()`; values are serialized fields.
- Sound id default is in code, so the prefab did not need an edit.
- Rule carries the flag by `LevelObjective` reference across `SetObjectives`, rather than pulsing every satisfied entry that is shown "changed". Same observable behaviour the plan asks for, and it also covers the stage-completing line.

## Needs THJ

- Real clip for `A_UI_ObjectiveMet`. The entry currently points at the same clip as `A_UI_Click` (placeholder, so it is audible and gives no unknown-ID warning). Replace the clip in `Resources/Audio/AudioStorage.asset` > UI entries.

## Docs to update

- `tech/combat-architecture.md` UI note (coordinator): objective lines pulse via `ObjectiveFeedbackRules`; `A_UI_ObjectiveMet` id.

## Risks and loose ends

- If two `UpdateEntries` coroutines overlap, the flag is cleared at the start of `Show`, so a line still pulses once.
- Pulse scales the entry in a vertical layout; if the line clips against the panel mask edge at 1.08, lower `metPulseScale` on the prefab.
- Not run in Play mode; the editor was open, tests were run through the Test Runner (MCP).

## Proposed commits

1. `feat(ui): a met objective pulses once and plays a sound after its strikethrough`: `ObjectiveFeedbackRules.cs`, `ObjectiveEntryUI.cs`, `ObjectivesPanelUI.cs`, `ObjectiveFeedbackRulesTests.cs`, both new `.meta` files, `AudioStorage.asset` (plain, not core)

(All under `miso/Assets/_Project/Features/UI/Panels/` plus `Resources/Audio/AudioStorage.asset`.)

## Other branches

main, when this branch merges.

## How to see it

1. Open a level with a mid-level objective or stage, for example a Hearth memory with two stages (Linda's or Lucy's).
2. Play; meet the first-stage objective. Expect: panel unfolds, line strikes through, then one small pulse and a click sound.
3. After the stage advances, the earlier line replays its strikethrough but does not pulse or sound again; the new stage's line pulses when met.
4. A failure objective (Defeat mode) strikes through with no pulse or sound.

## Fix round (review verdict FIX)

- `ObjectivesPanelUI`: new `_feedbackAllowed` (default true), set false when `Hide` starts, true in `Show`. `UpdateObjectives` passes `() => _feedbackAllowed` to `ObjectiveEntryUI.Show`.
- `ObjectiveEntryUI.Show(float, Func<bool> feedbackAllowed = null)`: the pulse rule is now evaluated after the strikethrough, so a hide that began meanwhile suppresses the pulse and the sound. The level-winning line and a stage-completing line met while a sequence hides the HUD get strikethrough only (accepted trade-off).
- `ObjectiveFeedbackRules.ShouldPulse` gained `panelVisible` (default true). New test `PanelHidden_LineMet_DoesNotPulse`; suite now 9 rule tests.
- Correction: `AudioStorage.asset` was hand-edited YAML, 4 lines added (not 3); valid, and the placeholder reuses the `A_UI_Click` clip GUID. THJ swaps the clip in the inspector.
- Full EditMode run: 1781 total, 1780 passed, 1 failed = known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- Changed files in this round: `ObjectiveEntryUI.cs`, `ObjectivesPanelUI.cs`, `ObjectiveFeedbackRules.cs`, `ObjectiveFeedbackRulesTests.cs` (same single proposed commit). Not checked in Play.

## Round 3 (pulse not visible enough)

- `ObjectiveEntryUI`: pulse is now scale 1.2 over 0.4 s (out and back) plus a gold flash (`metFlashColor`, default 1.0/0.82/0.3) at the same time. Serialized fields `metPulseScale`, `metPulseSeconds`, `metFlashColor`; the prefab stores none of them, so the new defaults apply and THJ can tune them in the inspector.
- The struck line is coloured by rich-text tags, so a text colour tween would be overridden. The flash instead re-tints the tag colour from the line's colour (success or failure) to gold and back, so the line ends in its normal strikethrough colour.
- New `StopPulse()` (kills the tween, restores scale 1 and the strikethrough colour) runs when a new pulse starts and on disable; destroy kills the tween.
- Hidden-panel rule and the 9 rule tests unchanged. Full EditMode run: see result line below.
- Files: `ObjectiveEntryUI.cs` only. Not checked in Play.

## Round 4 (deferred feedback after the cut-in)

- `ObjectiveFeedbackRules`: new `Decide(seenUnmet, pending, satisfied, mode, panelVisible)` returning None / PlayNow / Defer, plus `PendingAfter` and `ShouldFlushPending`. `ShouldPulse` kept as a wrapper (PlayNow only).
- `ObjectiveEntryUI`: a Win line met while the panel is hidden or hiding is marked pending (after its strikethrough) instead of dropped. `FlushPendingFeedback(withSound)` plays pulse, flash and sound once and clears the flag; a line not yet revealed or still striking through keeps waiting and plays when its own reveal finishes. `Initialize` takes the pending flag.
- `ObjectivesPanelUI`: `SetObjectives` carries pending by `LevelObjective` reference like the seen-unmet flag, so a rebuilt entry plays once, not once per rebuild. After `Show` finishes, waiting lines pulse together with one sound.
- Level win: the HUD is never shown again, so nothing flushes and the last objective stays silent. Next level: `SetObjectives` runs before `ShowHUD` and only carries flags for the same objective objects, so stale pending cannot replay.
- Tests added (15 rule tests now): met while hidden is deferred, plays on show, level ends never plays, pending survives a rebuild and plays once, defeat not deferred.
- Full EditMode run: "summary":{"total":1787,"passed":1786,"failed":1,"skipped":0,"durationSeconds":213.2318554,"resultState":"Failed(Child)"}. Only the known AIRegressionTest.Baseline_MatchesCurrentAI failed.
- Files: ObjectiveFeedbackRules.cs, ObjectiveEntryUI.cs, ObjectivesPanelUI.cs, ObjectiveFeedbackRulesTests.cs. Not checked in Play.

## Round 5 (defer the strikethrough too)

- A Win line met while the panel is hidden is no longer struck: it stays plain (pending) and, when the panel shows again, strikes, then pulses, flashes and plays the sound (`PlayDeferred`). `UpdateVisuals` skips the struck style while a line is pending, so it is never shown pre-struck.
- A deferred line rebuilt by a stage advance while hidden carries its pending flag, stays plain, and plays once on return. If the HUD starts hiding during a visible strikethrough, the line goes back to pending and replays whole on return.
- Unchanged: lines met with the panel visible, failure lines (no deferral), old met lines rebuilt (silent). The level-winning line is met while hidden, so it stays unstruck and silent; that panel is never shown again, so nothing is visible either way. Try Again / level change: pending is carried only by the same objective objects, as in round 4.
- Reviewer fixes: orphaned comment moved above `PlayMetFeedback` and reworded ("Scale pulse, colour flash and one UI sound"); `StopPulse()` at the top of `PlayStrikethrough`.
- New rule `StrikesNow(action)` and tests (hidden+met deferred strike, visible+met strikes with feedback, old line rebuilt silent, failure immediate, rebuilt-while-hidden plays once on return).

## Round 6 (new lines get feedback)

- `ObjectiveFeedbackRules.NewLines<T>(old, now)`: lines added by a stage advance. Counts only when the old list is non-empty and all of it is still present, so a first list, level change and Try Again (old lines gone) give none. `DecideArrival` and `FlushOrder` (met line before new lines) are pure and tested.
- `ObjectiveEntryUI`: new line stays invisible until its arrival, then fades from the gold flash colour to its normal colour over `newLineSeconds` (default 0.3, field) with its own sound `newSoundID` (default `A_UI_ObjectiveNew`); no scale pulse. While the panel is hidden it stays invisible and arrives on return. Tween killed on disable/destroy.
- `ObjectivesPanelUI`: `SetObjectives` marks new lines and carries unplayed arrivals across a rebuild; one arrival sound per stage advance (`ClaimArrivalSound`); on `Show` a flush coroutine plays met lines first (together, one sound), waits for them, then the new lines. Visible stage advances play in list order (met line first) through the existing reveal loop. A level win never shows the panel again, so it stays silent.
- `AudioStorage.asset`: hand-edited, 4 lines appended for `A_UI_ObjectiveNew`, same placeholder (click) clip as the met entry; LF kept. THJ supplies the real clip.
- Full EditMode run (rounds 5 and 6 together): "summary":{"total":1801,"passed":1800,"failed":1,"skipped":0,"durationSeconds":195.0405723,"resultState":"Failed(Child)"}. Only the known AIRegressionTest.Baseline_MatchesCurrentAI failed. Not checked in Play.
- Files: ObjectiveEntryUI.cs, ObjectivesPanelUI.cs, ObjectiveFeedbackRules.cs, ObjectiveFeedbackRulesTests.cs, AudioStorage.asset.

## Round 7 (re-review fixes)

1. Defer branch now calls `UpdateVisuals()` after the pending flag is set, so a line already on screen that is met while hidden returns plain (not struck, not struck twice) and strikes on return.
2. A new line waits (in `UpdateObjectives`) while any entry is still playing met feedback, so arrivals come after the met pulse and sound.
3. Outro guard: the panel reads `CombatLevelRunHandler.Instance.IsLevelEnded` (public, read only, set for both win and loss before the HUD hides; no core edit). Feedback is allowed only while the level is running (`FeedbackAllowed()`); the flush on HUD return drops all pending met feedback and arrivals when the level has ended and never plays them. Pure rule: `ShouldFlushPending(pending, visible, levelEnded)`. Loss path: same gate, so no success feedback after a loss. Note: `_levelEnded` is never reset in the handler, so this relies on each combat level starting a fresh handler (it already does for `IsLevelEnded` elsewhere).
4. On return from hidden, new lines arrive one after another with the same 1 s spacing as the visible path (shared `LineRevealSeconds`), after the met feedback.
- Tests: level ended never flushes; level running flushes when visible.
- Full EditMode run: "summary":{"total":1803,"passed":1802,"failed":1,"skipped":0,"durationSeconds":176.9717821,"resultState":"Failed(Child)"}. Only the known AIRegressionTest.Baseline_MatchesCurrentAI failed. Not checked in Play.
- Files: ObjectiveEntryUI.cs, ObjectivesPanelUI.cs, ObjectiveFeedbackRules.cs, ObjectiveFeedbackRulesTests.cs.

## Round 8 (win line stays struck)

1. `ObjectiveFeedbackRules.Decide` takes `levelEnded`: once the level has ended the result is None (strike now, no pulse, no sound, no deferral). `ObjectiveEntryUI.Show` gets a `levelEnded` callback from the panel (`CombatLevelRunHandler.Instance.IsLevelEnded`); when it is true the entry drops any waiting feedback first, then shows the completed style. The win line never goes plain.
2. Safety net: `DropPendingFeedback` now, for a shown entry that was waiting, restores the default colour and calls `UpdateVisuals()`, so a dropped met line is struck and a dropped new line is visible. `ObjectivesPanelUI.Show` calls `DropAllPendingFeedback` before the slide-in when the level has ended.
3. Test: level ended + met (visible or hidden, pending or not) gives None, strikes now, no pending.
- Full EditMode run: "summary":{"total":1804,"passed":1803,"failed":1,"skipped":0,"durationSeconds":186.7150178,"resultState":"Failed(Child)"}. Only the known AIRegressionTest.Baseline_MatchesCurrentAI failed. Not checked in Play.
- Files: ObjectiveEntryUI.cs, ObjectivesPanelUI.cs, ObjectiveFeedbackRules.cs, ObjectiveFeedbackRulesTests.cs.
