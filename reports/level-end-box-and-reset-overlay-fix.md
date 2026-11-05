# Report: Image-first dialogue box and exhausted tint after Reset

Plan: decisions D-388, D-389 (cause report `reports/level-end-box-and-reset-overlay.md`)    Agent: miso-implementer    Branch: thj/onboarding (both units general, for `main`)
Outcome: done (code only; not compiled, not tested, not played: Unity MCP down)

## What changed

Unit A (D-388, not core):
- `miso/Assets/_Project/Core/UI/Runtime/Dialogue/DialoguePlayerUI.cs`: `Show` computes `OpensTextBoxAtStart(firstNode)` (new public static pure rule: false only when the first node is an Image). It sets `_isCurrentNodeImage = !opensTextBox` at every `Show` (no carry-over between dialogues) and passes the result to `ShowIE(bool)`, which skips `ShowDialogueBox` for an image-first dialogue but still fires `OnShowFinished`. New private `_isImageAppearing` (true during `ShowImageIE`'s fade-in, reset in `Show`); `SkipDialogue` finishes an image node only once it is no longer appearing (see Decisions).
- `miso/Assets/_Project/Core/UI/Editor/DialogueOpeningTests.cs` (+ `.meta`, new): 3 tests on `OpensTextBoxAtStart` (Image → false; every other node type → true; null → true).
- `DialogNodeSequence.cs` not touched (not needed).

Unit B (D-389, core: `FactionControllerBase.cs`):
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`: `RestartTurn` calls new private `RefreshExhaustionAfterRestart()` after `StartTurn()`: for each `AliveUnits` unit, `MarkEnergetic()` if `IsEnergeticAfterRestart(unit.APConsumer.Points)` else `MarkExhausted()`. New public static pure rule `IsEnergeticAfterRestart(int pointsLeft) => pointsLeft > 0` (same threshold as `GUnit.HandleExhaustion`). No AP or event change; `ActionPoints.ResetToInitial` stays silent.
- `miso/Assets/_Project/Core/Interactions/Editor/RestartTurnTintTests.cs` (+ `.meta`, new): 4 tests on the rule (2, 1 → energetic; 0, -1 → exhausted).

Encoding kept: `DialoguePlayerUI.cs` LF, no BOM; `FactionControllerBase.cs` LF with BOM. New tests follow their folder neighbours (`DialogueOpeningTests.cs` no BOM like `CursorFinalPickTests.cs`; `RestartTurnTintTests.cs` BOM like `TurnStartPauseTests.cs`), LF. `.meta` files hand-written (2-line form like their neighbours, fresh GUIDs).

## Callers checked (Unit B)

- `RestartTurn` callers: only `CombatLevelRunHandler.ResetCurrentPhase` (:551), on the current faction's controller after it can end its turn. Override: `AIController.RestartTurn` (:52) stops `HandleUnits`/`_predictTargets`, cancels the brain, then calls `base.RestartTurn()`, so the marking runs for AI factions too, after the virtual `StartTurn` has restarted `HandleUnits` (that coroutine's first statement yields, so no AI marks race it). `PlayerController` doesn't override `RestartTurn`; its `StartTurn` override runs inside the base call, before the marking.
- Only this faction's alive units are marked; `MarkEnergetic`/`MarkExhausted` already no-op when `visualizePlayabilityInTurn` is off (the same flag that gates the `OnValueChange` hook).
- PerUnit mode (all AI factions always, player when PerUnit): `ResetToInitial` is silent, so the tint was stuck; now set from `Points`. Turn-skipped units (Stunned/Unaware) get `Consume(Closure)` → 0 AP → exhausted, matching what the AP event shows for them.
- Shared mode (player faction only; `IsPlayerSharedMode` needs the player faction): `APConsumer.ResetToInitial` and `ResetSharedPool` already fire `OnValueChange` → `HandleExhaustion` with the same `Points > 0` rule, so the new marking sets the same tint again (redundant, not conflicting). Skipped units in Shared mode read the family pool, so they show energetic, as the existing event already makes them.

## Acceptance criteria

- [x] Image-first dialogue doesn't open the text box; `_isCurrentNodeImage` set; `OnShowFinished` still fires; box opens on the first text node via `WriteDialogueIE` :250-253 (code; rule covered by `DialogueOpeningTests`, the UI flow needs the play check).
- [x] `_isCurrentNodeImage` reset at each `Show` (code; play check).
- [x] Text-first dialogues unchanged: `ShowIE(true)` is the old path; `_isCurrentNodeImage` was false after any text node anyway (play check).
- [x] Prompt/skip for image-first: input is hooked in `Show` as before; the "Space" Skip Indicators are children of the dialogue box panels in `DialoguePanel.prefab`, so during an image they are hidden exactly as for a mid-dialogue image today; Space finishes the image node once it has faded in; Skip All works (play check).
- [x] After a phase Reset every alive unit of the faction shows the tint matching its AP, player and AI, both AP modes (code; rule covered by `RestartTurnTintTests`; the wiring needs the play check).
- [ ] Compiles, EditMode suite passes: not run (Unity MCP down, editor not driven).

## Save reset

no

## Decisions I made

- Unit A: added `_isImageAppearing` so a Space press during an image-first dialogue's 1 s fade-in doesn't finish the image node early. Without it, setting `_isCurrentNodeImage` at `Show` (new) would let that press start the first text node while the image is still fading in, and `ShowImageIE` would then set `_isShowingImage`/`_isCurrentNodeImage` after the text node, leaving the image up over the text. During the fade a press now falls through to the old path (`_skipWait = true`, which `PrintDialoguesIE` resets before waiting), which is what a press during a mid-dialogue image fade already did. No other path changes: in existing flows `_isCurrentNodeImage` only becomes true together with the end of the fade.
- Unit A: the decision is pulled into `DialoguePlayerUI.OpensTextBoxAtStart(SequenceNode)` (public static, pure) for the test.
- Unit B: the rule is pulled into `FactionControllerBase.IsEnergeticAfterRestart(int)` (public static, pure, like `TurnStartPauseAfter`) for the test. It covers the threshold, not the wiring: testing `RestartTurn` itself would need a live `GUnit`, `Faction`, `CombatLevel` and the event bus, too heavy for EditMode. The play check covers the wiring.

## Needs THJ

none (D-389 is THJ's OK for the core change)

## Docs to update

- `tech/core-systems.md` (Faction controllers row): `RestartTurn` now resets each alive unit's exhausted/energetic tint from its AP after `StartTurn`; new public static `IsEnergeticAfterRestart`.

## Risks and loose ends

- Not compiled. Watch for: `SequenceNode` (global namespace) used from `MISO.Core.UI.Runtime.EditorTests`; it is already used from `DialoguePlayerUI`, so it should resolve.
- `SetCharacter` still runs for the first node even when it's an image. Unchanged; it would throw for an image node with no character on side Left/Right (`characterData.characterAvatar` at :179), as it already does today. The Hearth cutaways use the narrator character, so fine.
- For an image-first dialogue `SetCharacter` takes the image node's character (`_isNarrator`); the first text node then shows its own box and, if its narrator flag differs, does the existing hide/show swap. That swap is on already-hidden/already-shown panels (zero-length tweens), so no visible flicker expected; the play check should confirm.
- An image node with no sprite as the first node fades nothing (`HideImageIE` path); with `_isCurrentNodeImage` now set, Space finishes it. Mid-dialogue, the same node is stuck until Skip All (old behaviour, not changed).
- On `main` the only image node is in `Mission 4/Level1C3_Start` (position unchecked); if it is the first node, that dialogue also changes (box no longer pops in empty).
- `AIRegressionTest` unaffected (no AI-readable code touched; `AIFactionBrain.cs`/`AIUnitBrain.cs` local changes are THJ's, untouched).

## Proposed commits

1. `fix(dialogue): a dialogue that opens on an image keeps the text box closed until its first line`: `miso/Assets/_Project/Core/UI/Runtime/Dialogue/DialoguePlayerUI.cs`, `miso/Assets/_Project/Core/UI/Editor/DialogueOpeningTests.cs`, `miso/Assets/_Project/Core/UI/Editor/DialogueOpeningTests.cs.meta` (plain)
2. `fix(turns): restarting a phase resets each unit's exhausted tint from its AP`: `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`, `miso/Assets/_Project/Core/Interactions/Editor/RestartTurnTintTests.cs`, `miso/Assets/_Project/Core/Interactions/Editor/RestartTurnTintTests.cs.meta` (core)

Independent; either order. Both cherry-pick cleanly to `main` (no onboarding dependency).

## Other branches

`main` (both commits).

## How to see it

Not verified: compile, tests, play (Unity MCP down). First: open Unity, Ctrl+R, check the console, run EditMode > Run All (only `AIRegressionTest.Baseline_MatchesCurrentAI` may be red).

Play checks:
1. Unit A, image-first: finish any Hearth memory (e.g. Memory 1 Linda). At the end cutaway the narrator image fades in with no empty text box first; Space after the fade moves to the first line and the box opens with text; the rest plays as before.
2. Unit A, skip during fade: in the same cutaway press Space during the image's fade-in: nothing breaks, the image finishes appearing and waits; then Space advances. Esc/Skip All during the image ends the dialogue cleanly.
3. Unit A, text-first: play any normal level intro dialogue (text first node) and a dialogue with an image in the middle: box behaviour unchanged.
4. Unit A, back-to-back: a level whose outro dialogue follows another dialogue (or replay a memory end): the second dialogue opens normally (no stuck image state).
5. Unit B, player PerUnit: in a combat level spend all AP on a unit (it darkens), use the phase Reset: it shows energetic and is selectable; units still with AP stay energetic.
6. Unit B, AI: let an enemy unit act (it darkens), hit Reset during the AI phase: its tint clears and the AI replays the turn, darkening units as they finish.
7. Unit B, stunned/Unaware unit: Reset in a turn where one of the faction's units is turn-skipped: it stays exhausted (PerUnit).
8. Unit B, Shared AP mode (if a level/setting uses it): Reset after spending the family pool: units energetic, same as before.
