# Toba's swap ends a move (core), so Linda's Watch can fire on it

Size: S    Tier: 3, approved by THJ 2026-10-29 (D-322)    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all, built on `thj/linda-quiver` (HEAD `55cde5ce5`)

## Why

Linda's Watch only reacts to `GlobalEventBus.unitEndMoving`. John's push (`AEffectPusher.MoveEntity`, line ~186) raises it for the pushed unit, mid-action, so Watch fires. Toba's swap (`Dom_Ability_Swap` -> core `AEffectSwapper.SwapIE`) moves both units with Unplug/Plug and raises nothing, so Watch never sees it.

## Change

In `Core/Systems/AbilitySystem/Effects/Runtime/AEffectSwapper.cs`, `SwapIE`, right after `aCell.PlugEntity(b); bCell.PlugEntity(a);` (only on a successful swap, not on the `CanOccupy` bail-out), raise `GlobalEventBus.Instance.unitEndMoving.Invoke(unit)` for each swapped unit that is still alive and not destroyed. Raise it the same way the pusher does (check how `AEffectPusher` guards and calls it and mirror that). End event only; no `unitStartMoving`.

## Listeners (from Explore, verify)

- Family Roles via `CombatLevelRunHandler.CheckFactionRoleAbilities`: only Linda listens to this event; once per phase; her `PrepareTargets` takes enemies in her row or column only.
- `RoleZonePresenter`, `MovePreviewCoverPresenter`, `QuiverAimPresenter`: UI refreshes.
- `EnemyAlertTracker.Events` `CheckSight`: a swapped unit may now be spotted (same as after a push; accepted).
- `JohnPassiveAbility_CommandShieldDash`: returns unless John's Command is in flight.
- `LucyPassiveAbility_PapasShelter.RefreshState`: idempotent; swapping Lucy or John now refreshes it (a small fix).
- Grounded-arrow pickup and hazards use plug events, already raised by the swap: no double fire.
- AI does not subscribe.

## Acceptance

- [ ] Toba swaps an enemy into Linda's row or column within her Watch range: Watch fires on it (with the usual prompt), once.
- [ ] Swapping two allies, or an enemy out of her lines: no Watch.
- [ ] Linda herself swapped: no Watch on herself; no error.
- [ ] A failed swap (`CanOccupy` false) raises nothing.
- [ ] Enemy Toba's swap behaves the same way (consistent with the push).
- [ ] EditMode passes, only the known red fails; its message unchanged (CHECKS 710 FAILURES 39). Add a test only if the coroutine can be driven cheaply in EditMode; otherwise say why not.

## Constraints

- Core: only `AEffectSwapper.cs`, minimal. Keep line endings and BOM. No private IDs.
- Hands off: the AI diagnostic (`AIFactionBrain.cs`, `AIUnitBrain.cs`), THJ's local edits (GlobalSettings.asset, John_Ability_Attack_Dash.asset, PreloadScreen.unity, LevelLucyJohn-C1/C2/C3, LevelLindaJohn-C1, LevelE2-C1 prefabs, EditorFPSLimiter.cs, ProjectSettings, TMP fallback).
- The editor is open: no batch Unity. THJ compiles and runs the tests.

## Commit units

1. `fix(abilities): a swap ends a move for both swapped units` (core, alone).

## Commit log

THJ play-checked 2026-10-29 (all steps pass), EditMode 1045/1046 (known red only, unchanged). `e76b5da70`.
