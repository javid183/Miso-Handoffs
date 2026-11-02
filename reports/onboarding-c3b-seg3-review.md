# Review: onboarding C3b segment 3 (John)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-01. Report: `reports/onboarding-c3b-seg3.md`.

**Verdict: FIX** (one small must-fix in `GuidedAbilityHint`)

Non-core: reads `abilityPerformed`, `TurnNumber`, `UnitAbilityButtonUI.Ability`; changes only `localScale`. No statics. Commit 1 (hint) builds alone; Linda/Lucy hunks belong in commit 2.

## Must fix

1. `GuidedAbilityHint.cs:70-97`: scale restored only in `OnDestroy`/`End()`, no `OnDisable`; disabling mid-pulse leaves the button scaled; the subscribe coroutine dies on disable; nothing ends the hint on level end (won on turn 1 without Shield Up). Add `OnDisable` restore, subscribe/unsubscribe in `OnEnable`/`OnDisable`, optionally end on level end.

## Should fix

1. `:114` pulse phase from absolute time jumps on target found; store a pulse start.
2. `:107-120` `FindObjectsByType` 4×/s on turn 1; re-find on `unitSelectionChanged` (+ slow fallback).
3. `HearthMemoryWiring.John.cs:146` `??` on a Unity object; use `if (!hint)`.
4. `GuidedAbilityHintTests.cs:53-59` "other ability" test passes nulls; no positive end test; no restore test.
5. `HearthMemoryJohnTests.cs:129` placeholder check: `Contains`, cover panel title and objective templates.

## Notes

- Wiring matches the brief; idempotent (`Claim<T>`); Linda/Lucy edits behaviour-neutral (`Who.Mark` appended, `private` → `internal`).
- `GB_m3-john` commit 2 carries reimport noise on unit instances along with the real hunks.
- `TurnNumber` counts rounds: the hint lasts through enemy turn 1. Turn-restart path not checked (hint stays ended; fine).

## Rework re-review (Claws arrive at the end of player turn 1): APPROVE

Turn switch traced (`CombatLevelRunHandler.cs:464-541, 1049-1090`): `turnEnded` fires in `EndTurn()` with `TurnNumber` still 1; the Enemy controller is inserted at index 1 (> current 0), so no shift; next index is Enemy, no faction skipped or doubled; turn 2 on the wrap. `unitBorn` listeners as `SpawnAt`; new `turnEnded` listeners added mid-invoke don't fire this time. AI waits on `SequenceInProgress`; input and HUD restored. Win can't fire before the arrival (0 alive, 0 dead). Non-core, no statics. Split builds in order.

Should fix (optional): `TurnEndSequenceTrigger.cs:95` scope to `GetComponent<HiddenLevelUnits>()`; `:61-78` stop the subscribe coroutine in `OnDisable` or skip a second add; `HearthMemoryJohnTests.cs:150-157` assert the condition's state and comparison.

Play check: the enemy phase banner shows while the arrival line is on screen; the Claws' AI may walk instead of attacking in place (could set off Watch).
