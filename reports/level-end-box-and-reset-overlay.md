# Empty narrator box at level end; exhausted overlay after phase Reset (2026-11-05)

Explore, read-only. Paths under `miso/Assets/_Project/`.

## Empty narrator box (onboarding content + a latent flaw also on `main`)

- The 4 Hearth cutaway dialogues (`Resources/Sequences/Hearth/Memory{1Linda,2Lucy,3John,4Mark}/*_End_Cutaway_DialogNodeSequence.asset`) start with an Image node (narrator character, empty text). Played from each memory level's `outroSequence` (`CombatLevelRunHandler.EndLevel` :702 → `LevelBase.PlayOutro` :88).
- `Core/Levels/Runtime/DialogNodeSequence.cs:37` calls `dialogUI.Show(sequenceNodes[0])` whatever the type; `Core/UI/Runtime/Dialogue/DialoguePlayerUI.cs` `Show` :68 → `SetCharacter` :83 → `ShowIE` → `ShowDialogueBox` :306 (clears text, plays the box show animation); only then `ShowImageIE` :214 hides the box → ~1 s empty frame.
- Fix hook: in `Show`/`ShowIE`, when the first node is an Image node, skip `ShowDialogueBox`, set `_isCurrentNodeImage = true`, still fire `OnShowFinished`; `WriteDialogueIE` :250-253 already shows the box for the first text node after an image. Also reset `_isCurrentNodeImage` at the start of `Show` (carries over between sequences). Not core. On `main` the only image node is in `Mission 4/Level1C3_Start` (position unchecked).

## Exhausted overlay after Reset (on `main` too)

- Overlay: `GUnit.HandleExhaustion` (:943) fires `goExhausted`/`goEnergetic`, driven by `APConsumer.OnValueChange` (:398); `turnEnded` (:392-397) forces energetic; `MarkExhausted`/`MarkEnergetic` (:953/:959) also from `AIController` :87/:125, `PlayerController` :430-446.
- `ResetCurrentPhase` (:543) → `FactionControllerBase.RestartTurn` (:300) → `StartTurn` → `FactionPhaseState.Reinitialize` (:66) → `APConsumer.ResetToInitial()`; PerUnit mode → `ActionPoints.ResetToInitial` sets the value silently (`ActionPoints.cs:131`), so no `OnValueChange`; `RestartTurn` raises no `turnEnded` either → overlay stays. From `8aab1534f`/`1aa614892` (2026-09-23), on `main`.
- Smallest fix: end of `FactionControllerBase.RestartTurn`, after `StartTurn()`: for each alive unit, `MarkEnergetic()` if it has AP else `MarkExhausted()`. Covers player and AI. Don't make `ResetToInitial` non-silent. Core file (`FactionControllerBase.cs`): behaviour change → THJ's OK (CLAUDE.md).
