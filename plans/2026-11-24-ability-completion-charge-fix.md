# Ability completion charges the unit that acted (core bugfix)

Size: S/M    Tier: 3 decided (THJ, D-657)    Assigned to: miso-implementer (opus: core)
Branch: `thj/onboarding-demo` (scope all: the bug is on `main`; list it for the next merge)
Status: approved, dispatched 2026-11-24

## Why

THJ's play check (2026-11-24) logged `NullReferenceException` at `FactionPhaseState.cs:73` (`FactionPhaseData.UpdateUnitActionPoints`), from `FactionControllerBase.SetTakeActionState`'s completion lambda (line ~748) via `AbilityCostOverride.Charge`. Trace: `reports/console-errors-2026-11-24.md`. In Memory3John, John's Shield Slam won the level; `EndLevel` started the outro while the slam was still finishing; by its completion the player controller had left TakeActionState and `PhaseData.ActiveUnit` was null. The throw stops the completion chain: no AP charged, `onCompletion` never runs (`IsInProgress` stays true, `abilityPerformed` not raised), `RuntimeAbility.OnCompletionShared` cleanup skipped. Harmless at level end; the same race mid-level would soft-lock the turn. Old code (line 73 from 2026-09-15), on `main`.

## Approach

- In `SetTakeActionState`'s `ApplyAction` (or wherever the action starts), capture the acting unit and ability as locals. The completion lambda uses those locals for the AP count, `AbilityCostOverride.Charge`, the `recordFree` callback and the consume.
- Add a consume path that takes the unit and ability (e.g. `ConsumeActionCost(GUnit unit, RuntimeAbility ability, int count)` → `unit.APConsumer.Consume(ability.Parameters.apConsumptionType, count)`), keeping the existing `ConsumeActionCost(int)` signature and behaviour for other callers. Same for `FactionPhaseData.UpdateUnitActionPoints` if needed (additive overload; no existing signature changes).
- If the captured unit itself is gone (destroyed), skip only the charge and still run the rest of the completion chain.
- Find, if cheap, which call cleared `ActiveUnit` (candidates in the trace) and report it; don't change turn flow beyond the fix.

## Acceptance

- An ability whose completion arrives after the controller left TakeActionState (ActiveUnit cleared or changed) charges the unit that acted, raises no exception, and its completion chain runs to the end (`onCompletion`, `abilityPerformed`, `OnCompletionShared` cleanup).
- Normal actions charge exactly as before (same AP, same free-cost override behaviour incl. the Cyclone's free Steer).
- EditMode tests for both cases (pure where possible).
- Full EditMode suite: only the 8 expected `M1RidgeTests` fail (D-651). AI regression not needed unless the AI's action path changes (AI controllers share `FactionControllerBase`: if the change touches the AI path, run it by name and compare with 44, D-644).

## Gates

Core: own commit, `miso-reviewer` on this chunk alone, full suite. `tech/core-systems.md` note (coordinator). THJ's play check: win a level with a final attack (e.g. Memory 3), no console error.

## Proposed commit

`fix(core): an ability's completion charges the unit that acted, even after the selection moved on`
