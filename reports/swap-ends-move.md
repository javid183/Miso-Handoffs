# Report: Toba's swap ends a move (core), so Linda's Watch can fire on it

Plan: plans/2026-10-29-swap-ends-move.md    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done (code written; compile, EditMode run and play check are THJ's, the editor is open)

## What changed

- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectSwapper.cs` (core, approved as D-322): after a successful swap, `SwapIE` raises `GlobalEventBus.Instance.unitEndMoving` for each swapped unit that still exists and is alive. Nothing is raised on the `CanOccupy` bail-out. No `unitStartMoving`. BOM kept, LF kept, no trailing newline kept (as before).

Exact diff:

```diff
@@ -63,6 +63,11 @@ namespace MISO.Core.Systems.AbilitySystem.Effects
             aCell.PlugEntity(b);
             bCell.PlugEntity(a);
 
+            // Both units now stand on a new cell, so the swap ends a move for each of them, the same way a push
+            // ends one for the pushed unit. Listeners that react to a finished move (such as Linda's Watch) see it.
+            if (a && a.IsAlive) GlobalEventBus.Instance.unitEndMoving.Invoke(a);
+            if (b && b.IsAlive) GlobalEventBus.Instance.unitEndMoving.Invoke(b);
+
             yield return new WaitForEndOfFrame();
             
             IsInProgress = false;
```

No test file added (see Decisions).

## Acceptance criteria

- [ ] Toba swaps an enemy into Linda's row/column within Watch range: Watch fires once. Code path checked (Linda's `PrepareTargets` takes an enemy, alive, not downed, in `GetCellsInRange()`; zone is read after both plugs). Needs THJ's play check.
- [ ] Swapping two allies, or an enemy out of her lines: no Watch. `PrepareTargets` rejects non-enemies and out-of-zone units. Needs play check.
- [ ] Linda herself swapped: no Watch on herself, no error. Her own event fails the enemy-relation check. Needs play check. See the risk below about the enemy she is swapped with.
- [x] A failed swap raises nothing: the invokes sit after the `CanOccupy` `yield break` (by reading the code).
- [ ] Enemy Toba behaves the same: the same `AEffectSwapper` asset (`Dom_Ability_Swap_Effect_Swapper.asset`, the only user of this effect) serves both; Linda's `activationPhase` is -1 (all phases). Needs play check.
- [ ] EditMode passes with only the known red (CHECKS 710 FAILURES 39): not run, the editor is open. THJ runs it. No test was added.

## Save reset

No.

## Decisions I made

- Guard is `a && a.IsAlive` (exists and alive), per the plan's "alive and not destroyed". The pusher only checks `IsAlive`; the extra Unity null check runs on the main thread inside the coroutine, so it is safe. Downed units (still `IsAlive`) raise the event, same as the pusher.
- Events are raised after both units are plugged, a then b, so each listener sees the final board (Linda's zone is right even if she was one of the two).
- No EditMode test: driving `SwapIE` needs a real grid (`CanOccupy` -> `TryGetFootprintCells` via the grid), `GridCell.PlugEntity` (nearest-cell fallback, plug events), `GUnit.PlaySwapVFX` (serialized `swapAnimation` object, null in a bare test unit -> NRE) and a live `GlobalEventBus.Instance` (private setter, only set in `Awake`, which does not run in EditMode). That is not cheap and would need test hooks in core files outside the approved scope.

## Needs THJ

none (one behaviour to be aware of below; decide only if it shows up in play).

## Docs to update

- `tech/combat-architecture.md` / `tech/mechanics-brief.md` (wherever `unitEndMoving` sources are listed): the swap now raises it for both units.
- The plan's listener note says Linda's Watch is "once per phase": her prefab has `oncePerPhase: 0`, so that line in the plan is not accurate (see risks).

## Risks and loose ends

Listener check (grep `unitEndMoving` over `Assets/_Project`), confirmed against the plan:

- `GlobalEventBus.Awake` forwards it as `ActionFlowEvent.OnUnitEndMoving` to `CombatLevelRunHandler.CheckFactionRoleAbilities`. Only `Unit_Linda.prefab` has bit 64 in `triggerEvents` (checked every prefab/asset). Confirmed.
- `RoleZonePresenter`, `MovePreviewCoverPresenter`, `QuiverAimPresenter`: UI refresh only. Confirmed.
- `EnemyAlertTracker.Events.OnUnitEndMoving` -> `CheckSight(unit)`: a swapped unit may be spotted, as after a push. Confirmed, accepted in the plan.
- `JohnPassiveAbility_CommandShieldDash`: returns unless `_commandInFlight` is set (only during John's Command). Confirmed.
- `LucyPassiveAbility_PapasShelter.OnPlugChanged`: refreshes when Lucy or John is swapped. Confirmed (small fix).
- Persistent (serialized) listeners in `LevelBase.prefab` and the Home scene: `m_Calls: []`. AI: no subscriber. MissionTracker stats / CombatLog: do not listen to it.

Things that could surprise on a swap:

1. **Two enemies swapped, both ending in Linda's lines: Watch can fire twice.** Linda's handler is `activationMoment: WaitForProcessesToComplete` and `oncePerPhase: 0`. Each event adds a (Linda, unit) entry to the faction's wait list; `ProcessFRApplyWaitList` fires the first feasible one and returns without clearing the rest, so after her Watch completes the next `ActionsProgressComplete` can fire the second one (if she can pay the FTP again). Toba's swap targets any faction (`factionRelation: -1`), so enemy Toba swapping two of its own allies inside her lines is the likely case. A multi-unit pull (vortex) already raises one end event per unit, so this matches existing behaviour, but it is not literally "once". If THJ wants one Watch per swap, that is a Family Roles change (not this file).
2. **Linda swapped with an enemy: Watch can fire on that enemy.** The base trigger check skips when the last action targets Linda, but Toba's swap passes its two units as one `GameEntityBundle` target, so `Targets.Contains(Unit)` is false. If the enemy lands in her new lines (it takes her old cell, so it is in line whenever the two started in the same row or column within range), Watch fires on it. Looks reasonable to me, but it differs from "an action that targets Linda never provokes her".
3. Like the push, the event is raised mid-action (`IsInProgress` still true); Linda's role waits for processes to complete, so it plays after the swap finishes.

## Proposed commits

1. `fix(abilities): a swap ends a move for both swapped units`: `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectSwapper.cs` (core, alone).

## Other branches

Any branch that has Linda's Watch and Toba's swap (all, per the plan). The change is self-contained in one file.

## How to see it

1. Recompile (Ctrl+R) and run EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red, message unchanged (CHECKS 710 FAILURES 39).
2. Open a level with Linda and Toba (Dom) in the party and an enemy nearby. Make sure Linda has enough family points for Watch.
3. With Toba, swap an ally with an enemy so the enemy lands in Linda's row or column within her Watch range (hold Shift with Linda selected to see her zone). Watch's prompt comes up once, after the swap finishes.
4. Swap two allies, then swap an enemy to a cell outside her lines: no Watch.
5. Swap Linda herself with an ally: no Watch, no console error.
6. Optional edge: swap two units where `CanOccupy` fails (for example a large unit into a cell it does not fit): nothing moves, no Watch.
7. Enemy phase: in a level where an enemy Toba exists, let it swap an ally of yours (from its view, an enemy) into Linda's lines: Watch fires as it does after an enemy push. Watch for the double-Watch case (risk 1) if it swaps two of its own units inside her lines.
