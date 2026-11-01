# Report: C3b segment 1, Linda's memory level sequences and win stage

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md (C3b, segment 1 only)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. Compiles, EditMode 1176 run, 1175 pass, only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known). Not play-checked.

## Built
- **Win stage:** one stage, group aggregation Any, two visible objectives: "Eliminate all enemies. {alive_0} remaining." (the template's own) and a `TurnReachedLOCondition` turn=2 ("The memory ends in {remaining_0} turns."). The condition counts turns since the first evaluation (turn 1), so it fires when turn 3 begins: the player gets exactly 2 turns, matching "budget 2, cap 3". No core change.
- **Start** (`introSequence`): DisablePlayerInput, HideHUD, Hearth line (Margaret hands Linda the telling), tutorial sequence with two pages (Moving and AP; Watch, ending "Each shot spends an arrow."), EnablePlayerInput, ShowHUD. The grid is untouched at the start.
- **End** (`outroSequence`, plays on Win after the HUD hides): DisablePlayerInput, punchline "Three Claws. My last arrow." (Linda), `FadeOutGridSequence`, Hearth cutaway (placeholder still node held to the end, then Lucy "That's not how it went!", Linda "That's exactly how it went.", Margaret "Then you tell it, Lucy."), `OutroCutsceneKeepGridHidden` (enable input, show HUD; no grid fade-in).
- All text carries `[PLACEHOLDER] `. Margaret has no dialogue character asset, so her lines use the Narrator character with a "Margaret:" prefix in the text. Panel images reuse existing tutorial sprites. The hearth still is a flat 16x9 brown PNG.
- Homestate: not done (see below).

## Files
New (each with .meta, folders too):
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs` (Tools > Onboarding > Wire Memory 1 (Linda); re-runnable, creates assets and rewrites the level's Level component fields)
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLindaTests.cs` (3 tests)
- `miso/Assets/_Project/Resources/Sequences/Hearth.meta`, `Hearth/HearthStill_Placeholder.png`, `Hearth/Memory1Linda.meta`
- `Resources/Sequences/Hearth/Memory1Linda/`: `Memory1Linda_Start_DialogNodeSequence`, `_Start_Panels` (TutorialDataSO), `_Start_TutorialSequence`, `_Start_SequentialSequence`, `_End_Punchline_DialogNodeSequence`, `_End_Cutaway_DialogNodeSequence`, `_End_SequentialSequence` (all .asset + .meta)
Modified: `Content/Levels/Greybox/GB_m1-linda.prefab`.

## Prefab hand edits (GB_m1-linda; a grid-tool rebuild loses them, re-run the menu item)
Done by the script through serialized data, not YAML: `introSequence`, `outroSequence`; `lObjectives.winObjectiveGroups[0]` aggregationMode Any, objectives resized to 2, objective 2 = TurnReachedLOCondition(turn 2, factionRef Enemy), visible. Per-instance HP edits untouched (the diff touches only these lines).

## Noise to NOT commit
`GB_m2-lucy`, `GB_m3-john`, `GB_m4-mark` prefabs show small unit-instance diffs (`ability.animationEvents.Array.size 26` added) that Unity wrote when it reimported after my refresh. Not mine; I tried to revert them and the revert was denied, so please discard them (or leave out of the commit). Also pre-existing: AI brain scripts, TMP font, ProjectSettings.

## Tests
`HearthMemoryLindaTests`: win stage shape (Any, enemies-dead + TurnReached(2), both visible); end order (punchline, fade out, cutaway with still, KeepGridHidden, no fade-in); start (Hearth line, 2-page panel set, "Each shot spends an arrow."). Not covered, needs play: the turn cap actually firing at turn 3, dialogue/panel presentation, the image node click flow.

## THJ play check
New game into the Hearth, segment 1: Margaret line, then the two panels, then play. Check: HUD shows both objective lines and the turn countdown (2 then 1); the level ends when turn 3 starts if you don't kill all; on win the punchline, grid fades out, still + three cutaway lines (click to advance past the still), then the next level. Placeholder tag will show on screen: the dialogue UI does not strip `[PLACEHOLDER] `. If the cutaway looks wrong after the still, the image-node flow is the thing to look at. Save not reset.

## Found for segments 2-4
- **Grid fade-in:** each level is its own scene, so the next level's grid starts fully visible (GridCell listens for the fade events only after Start). Nothing needs to fade it in for it to appear; to get a visible fade-in, segment 2's start must hide the grid instantly then fade in (as `Level1C1-2` does with its Intro then Outro common sequences). I did NOT touch `GB_m2-lucy`: that needs a new sequence asset (e.g. FadeOut with duration 0 + FadeIn), not a one-field change.
- Win-stage turn semantics: `TurnReachedLOCondition.turn=N` fires when turn N+1 begins (counted from the first evaluation); `queueWinGroups` gives stages with an `onCompleteSequence` per group (useful for segment 2's interruption and segment 4's stage 2).
- Sequences available: `RevealUnitsSequence` (C3a), `MoveUnitSequence`, `CameraSequence`, `LSBExecutionSequence`, `UnitAnimationSequence`, `SignalSequence`, `PlayerInputSequence`; I did not check whether any fires an ability (`LSBExecutionSequence` is the candidate).
- `Mission.homeState` is the Home state applied AFTER completing the mission (HomeStateManager reads it from the furthest/last completed mission), so it is the Hearth *close* state; the open state is `GameData.InitialHomeState`. No HomeState asset exists to point at, so both are left for the Home run (new HomeState assets with idles, not a one-line data change).

## Proposed commits
1. `feat(onboarding): wire the first Hearth memory level's start, end and win stage`: HearthMemoryWiring.Linda.cs(+meta), HearthMemoryLindaTests.cs(+meta), Resources/Sequences/Hearth/** (with metas), GB_m1-linda.prefab.

## Fix round
- HUD line now "Turns left in the memory: {remaining_0}." (prefab re-wired by re-running the menu item; the diff shows the new text).
- The wiring reuses an existing `TurnReachedLOCondition` in the slot and only sets `turn`; the managed-reference id stayed the same on the re-run.
- Test asserts the punchline index is >= 0 before indexing.
- `SpriteByGuid` logs a warning when a panel image is missing.
- EditMode re-run: only `AIRegressionTest.Baseline_MatchesCurrentAI` red. GB_m2/m3/m4 reimport diffs left alone.
