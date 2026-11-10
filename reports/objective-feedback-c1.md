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
