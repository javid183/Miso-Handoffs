# Report: C3b, untag Linda's text (A) and segment 2, Lucy's memory level (B)

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: both done. Compiles; EditMode 1184 run, 1183 pass, the one failure is `Baseline_MatchesCurrentAI` (the known red; name read from the run). Not play-checked. Save not reset. Both wiring menu items were re-run.

## A. Untag Linda's text (commit unit 1)
- `HearthMemoryWiring.Linda.cs`: the tag constant and every use removed; dialogue and panel text are written as they show. Re-ran Tools > Onboarding > Wire Memory 1 (Linda).
- Also (found while re-running with the new missing-sprite warning): the Watch panel's image GUID `9d2bb3f0...` has no asset in the project (the old `Tutorial_FR_Linda` and `Tutorial_AP_Abilities` point at the same missing image). Switched the Watch panel to `Tut-FR-1.png` (`2097e2cd...`). The first-run panel therefore had an empty image; fixed now.
- `HearthMemoryLindaTests.cs`: new test that no line or panel page starts with `[PLACEHOLDER]`.
- Assets touched: `Memory1Linda_Start_Panels`, `_Start_DialogNodeSequence`, `_End_Punchline_DialogNodeSequence`, `_End_Cutaway_DialogNodeSequence`, and `GB_m1-linda.prefab` (see noise below).
- Placeholder lines (wording still unapproved, now untagged): "Margaret: Eldest first. Linda."; both panels (Moving and AP / Watch); "Three Claws. My last arrow."; cutaway "That's not how it went!", "That's exactly how it went.", "Margaret: Then you tell it, Lucy."; objective text "Turns left in the memory: {remaining_0}."

## B. Segment 2, Lucy (commit unit 2)
New files (each with .meta; folders too):
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs` (Tools > Onboarding > Wire Memory 2 (Lucy), re-runnable), `HearthMemoryLucyTests.cs` (7 tests).
- `Resources/Sequences/Hearth/Memory2Lucy/`: `_GridHiddenAtStart` (a `GridVisualSequence`, showGrid off, duration 0), `_Start_DialogNodeSequence`, `_Start_SequentialSequence`, `_Interruption_CameraToRoom`, `_Interruption_Reveal` (`RevealUnitsSequence`, group "hidden"), `_Interruption_DialogNodeSequence`, `_Interruption_CameraBack`, `_Interruption_SequentialSequence`, `_End_Punchline_DialogNodeSequence`, `_End_Cutaway_DialogNodeSequence`, `_End_SequentialSequence`.
Modified: `HearthMemoryWiring.Linda.cs` (helpers made `internal`, `John` added to the speaker list, `BuildDialog` takes a folder), `GB_m2-lucy.prefab`.

What it does:
1. **Start:** disable input, hide HUD, grid hidden at once (duration-0 grid sequence, no new runtime code), grid fades in (existing `FadeInGridSequence`), Lucy: "So. I'm in the cave. Alone. Very brave.", input and HUD back.
2. **Stage 1** (queued stage, Any): 2 Claws dead (`LivingUnits` Enemy dead >= 2) or turn 2 reached (turn=1, hidden from the HUD). Its `OnCompleteSequence`: disable input, camera to the room (average of the three hidden Claws' cells), `RevealUnitsSequence`, Lucy "Then ten more!" / Linda "Three.", camera back to Lucy, enable input.
3. **Stage 2 (win, Any):** all enemies dead (alive <= 0) or `TurnReached` turn=3; both shown ("Eliminate all enemies. {alive_0} remaining.", "Turns left in the memory: {remaining_0}.").
4. **End:** disable input, punchline "And the wind caught fire. Obviously." (Lucy), `FadeOutGridSequence`, cutaway over the placeholder still (John "Ten?", Lucy "At least.", Margaret "Go on, John. Your turn to be modest."), `OutroCutsceneKeepGridHidden`.

Prefab edits (by script, serialized data only): `introSequence`, `outroSequence`, `lObjectives` (queue on, two groups, `onCompleteSequence` on group 1). Per-instance HP (3,3 and 4,2 = 0.625) untouched. A rebuild with the grid tool loses these: re-run the menu item.

Decisions and differences:
- **Interruption lines** follow the levels plan and your message ("Then ten more!" / "Three."). The narrative draft still has "And then more came. At least ten!" / "There were four." / "Ten." (four, from before the cue enemies were three). The draft needs updating, or the lines swapped.
- **Punchline:** the draft has no end line for segment 2; I used M2-5 ("And the wind caught fire. Obviously."), which the draft meant as a Cyclone bark. Easy to change in the script.
- **Stage 2's turn cap is counted from when stage 2 begins** (`TurnReachedLOCondition` starts counting at its first evaluation), not from the level start. Stage 1 normally ends on turn 1, so turn=3 means "turn 4 begins". If stage 1 ends by its cap at turn 2, stage 2 ends at turn 5. An absolute turn would need a core or new-condition change; not done.
- `CameraSequence` sets every faction's turn flag off at its start and on at its end (existing behaviour; the old mid-level camera sequence does the same). Watch this in play.

Tests (`HearthMemoryLucyTests`): grid hidden at once then faded in before Lucy speaks; the three Claws are inactive in the prefab and the reveal names their group; stage 1 conditions and the interruption order (input off, camera to room, reveal, lines, camera back, input on; the room is right of Lucy); stage 2 conditions and visibility; no shared condition between slots; end order with no fade-in; no placeholder tag. Not covered: everything at runtime.

## Reveal, read in code (first real use of `RevealUnitsSequence`)
Read `HiddenLevelUnits.Reveal` against `reports/onboarding-c3a-reveal-check.md`: activate, `Initialize(true)`, `PlugEntity` on the parent cell, `RegisterUnit` on the existing Enemy controller (sorted by turn order, raises `unitBorn`, which the AI brain, alert tracker and role zones listen to; with `level alert all` they come in alert). The reveal happens on the player's turn, so the enemy turn that follows builds from the larger `AllUnits`. Dead Claws stay in `AllUnits`, so "dead >= 2" counts them and the later "alive <= 0" counts the three. The new stage is evaluated only after the interruption ends (`WaitThenEvaluateNewStage` waits for the sequence player), so stage 2 cannot be satisfied before the Claws exist. Not run, so unverified: the new-stage wait, the AI taking its turn with the new brains, spawn animation timing.

## Play check for THJ
New game into the Hearth, past segment 1. Segment 2: grid hidden then fading in under Lucy's line (watch for a one-frame flash of the grid before it hides); HUD shows the stage-1 line; kill both Claws on turn 1 with embers: camera to the far room, three Claws appear (alert, visible, spawn animation), lines, camera back to Lucy, input works; HUD then shows three lines (stage 1 done, kill-all, turns left). The enemy turn: the three Claws act. Win by kill-all or turn 4: punchline, grid fades out, still plus cutaway (click past the still), next level. Also try not killing on turn 1 (stage 1 by turn 2) and check the interruption still plays.

## Noise and loose ends
- `GB_m1-linda`, `GB_m3-john`, `GB_m4-mark` (and `GB_m2-lucy`) carry Unity reimport diffs on unit instances (`animationEvents` sizes and frames). Only `GB_m2` belongs in unit 2 deliberately; the rest are not mine and may ride along or be discarded.
- The Linda wiring script's helpers are now shared (`internal`); segments 3-4 can call them too.

## Findings for segments 3-4
- A group-based reveal plus `CameraSequence` works as a queued stage's `OnCompleteSequence`; segment 4's mother scene can use the same pieces.
- Instant grid hide at a level start needs only a `GridVisualSequence` asset with duration 0 (made for segment 2); segment 3 needs the same fade-in start.
- The speaker list now has John; Mark and Margaret are not dialogue characters (Margaret uses Narrator with a name prefix).
- Still not checked: whether a sequence can fire an ability (`LSBExecutionSequence` is the candidate) for segment 4's Tempest Bloom.

## Proposed commits
1. `fix(onboarding): the first memory level's text carries no placeholder tag`: HearthMemoryLindaTests.cs, the tag/panel-image hunks of HearthMemoryWiring.Linda.cs, Memory1Linda assets, GB_m1-linda.prefab.
2. `feat(onboarding): the second Hearth memory level's start, interruption, stages and end`: HearthMemoryWiring.Lucy.cs(+meta), HearthMemoryLucyTests.cs(+meta), Resources/Sequences/Hearth/Memory2Lucy/** (with metas), GB_m2-lucy.prefab, and the shared-helper hunks of HearthMemoryWiring.Linda.cs.
