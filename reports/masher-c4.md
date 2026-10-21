# Report: Masher reckless tank, C4 (handler rewrite)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (C4)    Agent: miso-implementer    Branch: masher-tweak
Outcome: done (compiles, EditMode green except the known red; every in-game criterion needs the play check)

## What changed

Paths are under `miso/Assets/_Project/`.

**T3(a) suppression query (core, commit 1)**
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleProvocationSuppression.cs` (+ `.meta`), new. A static, read-only query for Family Role handlers:
  - `IsSuppressed(RuntimeAbility)`;
  - `InvolvesSuppressedAction()`, true when an action in progress, or `SessionLogs.LastActions[0]`, is listed;
  - `Suppress` / `Release`;
  - `internal ResetPlayModeState()`.
  It's additive: with nothing listed, it returns false at once. UTF-8 BOM and LF, like `FactionRoleRules.cs` next to it.
- `Core/Managers/PlayModeStaticReset.cs`: one line, `FactionRoleProvocationSuppression.ResetPlayModeState();` (CRLF kept).
- `Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`: one condition in `CheckTriggerConditions`, `&& !FactionRoleProvocationSuppression.InvolvesSuppressedAction()` (CRLF kept).
- `Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs`: one early return in `CheckTriggerConditions` (CRLF kept).
- `Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleProvocationSuppressionTests.cs` (+ `.meta`), new: 4 tests.

**Handler rewrite (commit 2)**
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs` is now `partial`. It keeps the initialization, the role zone (`GetCellsInRange`) and the hover preview, together with the preview's helpers (`TryPickAttackCell`, `TryFindApproachCell` and the rest), which are untouched for C5.
  - `Initialize` and `InitializePartially` now call the base (item 8), through `WithInertSuperTimeAbility` (see Decisions).
  - The duplicate `turnEnded` lambda is gone, because the base adds the same one.
  - `OnDisable` and `OnDestroy` call `StopCounter()`.
  - `OnDamaged`, `PrepareTargets`, `Activate`, `AbilityTargetFrom` and `_approachCell` moved out, which also removes the old `:77` drop guard.
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs` (+ `.meta`), new: the inputs, the Duo record, the queue and pump, the turn-switch hold, the chain cap, the step and aim through `MasherCounterRules`, the answer and the toggle. LF, no BOM, matching the main file.
- `Features/Enemy/Masher Goblin/Scripts/MasherCounterQueue.cs` (+ `.meta`), new: the pure FIFO queue. A `ChosenAbility` entry merges with a waiting `ChosenAbility` entry from the same provoker. `PushFront` handles retries.
- `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`:
  - the `Classify` doc comment now names each caller-side exclusion (item 9): non-ability damage and burn, Pass-by, and allied AI units such as Toba as an ally and the Deer. It also defines `ownerIsPlayerFaction`;
  - new pure `MinDistance4(footprint, targetCells)`, used for the step's distance.
- `Features/Enemy/Masher Goblin/Editor/MasherCounterQueueTests.cs` (+ `.meta`), new: 11 tests.
- `Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs`: 3 `MinDistance4` tests.
- `Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs`: `OnFamilyRoleActivated` hides the tether only for John, Linda, Lucy and Mark handlers (item 7). CRLF kept.

## How the counter works now (C4 items 1 to 6, 10, 11)

- **Inputs.** `onUnitDamageDone` on this Masher (not lethal, Masher alive, not silenced) goes through `Classify`:
  - `ownerIsPlayerFaction`: `owner.Faction == CombatLevel.PlayerFaction`;
  - role: `owner.AbilityOrchestrator.FactionRoleAbility == source`;
  - Duo: `CooperationHandler.TryGetSecondPerformer(source, owner)`, or a partner ability of the open Duo record;
  - acting: the owner's controller `CurrentlySelectedUnit == owner`;
  - player phase: `CombatLevelRunHandler.CurrentFaction == PlayerFaction`.

  Ignore and Duo results are dropped there. A Duo is answered only from its record.
- **Duo record.**
  - `onSynergyTriggered("Duo", entryId)` opens it, with the entry's partners in execution order.
  - The Masher's HP `onValueDecreased` adds pending damage.
  - The next `onAbilityEffectPerformedOn` from a partner's ability on this Masher, or on one of its cells, confirms that partner as "struck".
  - The trigger's `abilityPerformed` closes the record and enqueues one `Duo` entry chosen by `PickDuoPartner`. Reachable uses the step rule; `ActedOrder` is the partner's place in the entry order.
- **Queue and pump.**
  - The first enqueue registers the turn-switch hold (`CombatLevelRunHandler.RegisterTurnSwitchHold(this)`) and starts a coroutine.
  - The coroutine waits, one frame at a time, until every check below is idle. It then waits one more frame and checks again:
    - `SessionLogs.ActionInProgress` (all controllers);
    - `ActionsInProgress.Length`;
    - `QuickTimeEventHandler.IsEventActive`;
    - `SequenceInProgress`.
  - Then it dequeues and drops the entry in any of these cases:
    - the provoker is dead or downed;
    - the Masher is dead, downed, silenced or turn-skipped (Stunned);
    - there is nothing to do (not adjacent, and no step);
    - the cap is reached.
  - Otherwise it calls `TryPlayFactionRole(Unit, onComplete)`. If that returns false, the entry goes back to the head, the hold stays, and the pump waits for idle again (retry). On success it consumes the cap and waits for `onComplete`.
  - When the queue is empty and the flow is idle, it resets the cap and releases the hold.
  - On `turnEnded` it clears the queue and the open Duo. If no answer is running, it also stops the pump, resets the cap and releases the hold.
  - On disable or destroy, everything is dropped and released.
- **Step and aim.**
  - Already adjacent (`IsAdjacent4` from the footprint): no step.
  - Otherwise, when `_walk.CheckActivationFeasibility()` passes (Crippled fails it), every free walk cell with a path becomes a `MasherStepCandidate` (adjacent after the step, `MinDistance4`, walk length), and `RankStep` picks one.
  - After the step, `PickAttackCell` picks the struck cell among the provoker's own `OccupiedCells`. With no adjacent cell, there is no slam.
- **The blow** is the role ability (`ability` = `MasherGoblin_Ability_Counter`), not the unit's `DefaultOccupiedCellAbility`.
- **Toggle** `counterCanProvokeFamilyRoles` (serialized, default true, under a "Counter" header). When it is false:
  - no `abilityStarted` for the slam;
  - `ability` and `_walk` are listed in the suppression query from the start of `Activate` until after the answer's `abilityPerformed` and the controller's release (the point where Mark and Linda have checked).

  `abilityActivationStarted` and `abilityPerformed` still fire.
- **Statics.** Only the T3(a) query is static, and it is hooked in `PlayModeStaticReset`. The handler has no static state. All its waits are frame-based (`yield return null`), so they run during a QTE pause (timeScale 0).

## Acceptance criteria (C4 scope)

- [ ] Player's turn: a chosen ability that hurts the Masher makes it step 1 tile toward the striker (unless adjacent, blocked or Crippled), and it slams once if adjacent. **Play check.**
  - Code: `OnDamaged`, `TryPlanAnswer`, `Activate`.
  - Tests: the rules (C2), plus the queue merge.
- [ ] The slam hits the struck tile and the 4 around it, both sides, at the slam's damage. **Play check.** This is data (C3); the answer uses the counter preset.
- [ ] A side or back tile of the cross gives a step only. **Play check.** Code: `TryPickAnswerCell` uses `PickAttackCell`, which is tested in C2.
- [ ] Own turn, aim only at an adjacent enemy unit's tile: data (C3, `targetType` 2); C4 doesn't touch the AI. **Play check.**
- [ ] Continuous Attack, approach and dash attacks are answered once, after the whole action, from the end tile. **Play check.**
  - Code: the pump waits for idle plus one frame, and measures the striker's tile when it plays the answer.
  - Test: `Enqueue_ChosenAbilitySameProvoker_MergesIntoOne`.
- [ ] A Duo is answered once, on the partner who struck, or by the D-095 tie rule. **Play check.**
  - Code: the Duo record.
  - Tests: `PickDuoPartner` (C2).
- [ ] A Family Role hit is answered on either turn, after the role resolves; on the enemy turn, after the current enemy unit's action. **Play check.** Code: `Classify` gives Reaction, and the pump's idle wait covers it, including `AIController.isActionInProgress`, which counts `IsComputing`.
- [ ] An answer pending when the player's last action ends the turn plays before the switch. **Play check.** Code: the hold is registered on the first enqueue and released only by the pump once it is idle and empty, never after a failed start. Test: `TurnSwitchHoldTests` (C1).
- [ ] Burn, Pass-by and allied AI hits don't provoke it. **Play check.**
  - Code: `ownerIsPlayerFaction`.
  - Burn and Pass-by never reach the damage event (see Classify's doc).
  - Test: `Classify` (C2).
- [ ] Hits that land during an answer are queued, not dropped. **Play check.**
  - Code: the `:77` guard is gone; `OnDamaged` only enqueues.
  - Tests: queue FIFO and retry.
- [ ] With the toggle false, no Family Role fires because of an answer; with it true, today's behaviour holds. **Play check** (Mark's enemy-turn chain and Linda's lane, on and off).
  - Code: `Activate`, plus the Mark and Linda checks.
  - Tests: `FactionRoleProvocationSuppressionTests`.
- [ ] An 11th answer in one root action doesn't happen, a warning is logged, and the next root action answers normally. **Play check** (needs a forced chain).
  - Code: the pump's cap check, one warning per root action, and the reset when idle and empty or on `turnEnded`.
  - Tests: `MasherChainCap` (C2).
- [ ] The "did not initialize its role ability" warning is gone. **Play check.** Code: the base initializers now run, so `_abilitiesInitialized` is set. The prefab already had one handler (C3).
- [x] The EditMode suite is green except the known red. Unity MCP, Run All: 345 tests, 344 passed, 1 failed.
  - The failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, with the same report as after C3: CHECKS 706, FAILURES 35, `expected 90, found 95`.
  - Targeted re-run after the last edit: 72/72. That covered the queue, rules, suppression and `TurnSwitchHoldTests` classes, by full class name.
- [x] Compile: clean. No `error CS` in the console or `Editor.log`; only the warnings that were already there.
- Preview criteria: C5, unchanged here.

## Save reset

No.

## Decisions I made

- **The base initializers run against a stand-in super-time ability** (same behaviour). The Masher's `superTimeAbility` has no preset, and `RuntimeAbility.Initialize` dereferences `preset`, so calling `base.Initialize` as the plan says would throw a NullReferenceException in `AbilityOrchestrator.Initialize`.
  - `WithInertSuperTimeAbility` swaps in `ability.Copy()` for the call and puts the original back afterwards. Nothing serialized changes, and `SuperTimeAbility` reads as before. Super time is player-only (`PlayerController.SuperTimeUnits`).
  - The copy: no save registration (not upgradable), an empty global stat id (ignored), and its own animation-event list.
  - Alternatives: a null guard in `FactionRoleHandlerBase` (core), or a preset in the prefab (data). Say if you prefer one of them.
- **The answer's slam is the role ability (the counter preset), not `_attack`.** That is what C3 wired the role handler to (D-096: tune the counter by data). It resets the counter's cooldown, not the slam's.
- **The suppression query is a small standalone registry** (`FactionRoleProvocationSuppression`, next to `FactionRoleHandlerBase`), not a static on the Masher handler. This keeps commit 1 independent of the handler and reusable by another reactive enemy.
- **Mark and Linda check the session log**, through `InvolvesSuppressedAction()`, not the `obj` argument. Both roles wait for processes to complete, and Linda's `obj` is the moved unit, not an ability. When they evaluate (on `ActionsProgressComplete` and on the answer's `abilityPerformed`), the log's last action is the counter or the walk.
- **Duo "reachable" follows the C2 review literally:** already adjacent, or `RankStep` finds a step. It could instead be read as "can end adjacent and strike", which is closer to D-095's "the one it can reach". That is a one-line change in `IsReachable` (use `slamsAfter`). **The coordinator may want THJ's reading.**
- **Duo "acted first"** is the partner's place in the cooperation entry's partner order, which is the execution order.
- **Duo damage attribution.** Damage that no partner effect event confirms is credited to the partner whose ability raised the most recent event. This covers hits that land after their partner's last event.
- **Chosen-ability merging.** Several hits from the acting unit's chosen action (follow-ups, multi-hit) merge into one waiting entry. Reactions and Duos never merge: one answer per resolved reaction.
- **The cap warning is logged once per root action**, not once per dropped hit.
- **Tether filter:** an explicit list of the four family handler types. The Masher's handler shares their namespace, so a namespace check wouldn't work.
- **`EnqueueProvocation` does nothing while the Masher is inactive**, so a disabled Masher can never hold the turn switch.

## Needs THJ

None that blocks. The two readings above (super-time stand-in, Duo "reachable") are flagged for the coordinator.

## Docs to update

- `tech/core-systems.md`, Family Roles row: `FactionRoleProvocationSuppression` (read-only query, static, reset in `PlayModeStaticReset`), checked by Mark's and Linda's role handlers.
- `tech/combat-architecture.md`: how the Masher counter flows (queue, pump idle conditions, hold, cap, toggle).
- `build-log.md`: C4 section (coordinator).

## Risks and loose ends

- **Linda timing.** Linda's queued trigger is processed on `ActionsProgressComplete`, which fires inside the answer's completion. If another controller is still busy at that moment, it is processed later, after the suppression is released, and she could fire with the toggle off. That's unlikely: the pump starts an answer only when everything is idle. Worth watching in the toggle-off play case.
- **Duo attribution with `executeInParallel` entries.** Both partners' events interleave, so "struck" could be credited to the wrong partner. All seven Duos should be checked for that flag; I didn't audit them.
- **Masher answer during the enemy turn.** The pump needs two idle frames between enemy units. If the AI chains units without an idle frame, the answer waits for the next gap, at the latest the end of the enemy turn, since the hold blocks the switch. The verifier should watch C1 review item (d), `TrySelectUnit` → `CleanupUnitTurn()`, during Mark's enemy-turn chain.
- **Lucy's decoy**, or any other player-faction summon that owns an ability, counts as a provoker, and the Masher steps toward it.
- **John relay (plan Risks).** The slam still raises `abilityStarted` before the action is recorded, as before, so John may never relay it. That is the existing follow-up.
- The preview (main file) still uses the old range-based `TryPickAttackCell` / `TryFindApproachCell` and `_attack`, unchanged for C5. Until C5 lands, the preview can disagree with the new aim rule.
- `FactionRoleHandlerBase`'s comment at `_abilitiesInitialized` still names the Masher as the handler that skips the base. It's a stale comment in a core file, which I left alone.

## Proposed commits

1. `feat(family-roles): let an enemy answer suppress Mark's and Linda's role triggers` (**core**, own commit, D-103):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleProvocationSuppression.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleProvocationSuppression.cs.meta`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleProvocationSuppressionTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleProvocationSuppressionTests.cs.meta`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs`

   With nothing listed, nothing changes. It stands alone.
2. `feat(masher): queue counters, step and slam by the adjacency rule, hold the turn switch, cap chains, roles toggle` (**core**: the Masher handler is on the core list; risky):
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs.meta`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherCounterQueue.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherCounterQueue.cs.meta`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherDuoCredit.cs` (revision 1)
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherDuoCredit.cs.meta` (revision 1)
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterQueueTests.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterQueueTests.cs.meta`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherDuoCreditTests.cs` (revision 1)
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherDuoCreditTests.cs.meta` (revision 1)
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs`

   **It depends on 1**: `Counter.cs` calls `FactionRoleProvocationSuppression`. It also builds on C1's hold API and C3's prefab.

Order: 1 then 2. Leave unstaged `miso/Packages/*` and `miso/ProjectSettings/*`, which were already dirty and aren't part of this work.

## Other branches

`thj/home-test` needs both commits, together with C1 to C3, when the Masher work merges there.

## How to see it

1. Inspector: `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`, root `MasherGoblinFactionRoleHandler`. A "Counter" header shows **Counter Can Provoke Family Roles**, ticked.
2. Play `LevelE3-C1` (or `LevelM1-C3`). The console should no longer show "MasherGoblinFactionRoleHandler ... did not initialize its role ability".
3. Hit the Masher with a ranged attack from 3 or more tiles. It steps 1 tile toward the striker and doesn't slam. Hit it again from the side so it ends next to the striker: it slams the striker's tile, and the plus hurts goblins too.
4. End the turn with an attack that provokes it. The Masher answers before the enemy phase banner.
5. Mark: Continuous Attack on the Masher draws one answer, after the last hit.
6. A Duo where both partners hit the Masher draws one answer, on the partner chosen by the D-095 rule.
7. Enemy turn: let Mark's role strike the Masher. It answers after the current enemy unit finishes. Untick the toggle and repeat: Mark doesn't strike back at the Masher's answer, and Linda doesn't shoot at its step.
8. Cripple the Masher: hit from range, and it doesn't step.
9. Test Runner > EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` is red.

## Revision 1 (after the FIX review, D-115)

Review: `reports/masher-c4-review.md`. Applied the coordinator's three items. The base-init swap (review should-fix 1) and the Duo "reachable" rule are unchanged; both wait on THJ.

1. **Must fix: Duo partner credit.**
   - New pure class `Features/Enemy/Masher Goblin/Scripts/MasherDuoCredit.cs` (+ `.meta`, BOM and LF). Pending damage goes to the **next partner `onAbilityEffectPerformedOn`, whatever its target**, and that clears the pending damage and the suspect. When no event follows the damage, the suspect fallback in `Finish()` credits the partner whose ability was last active when the health dropped.
   - The class comment explains the ordering: `AEffectCompound.Apply` applies its effects and only then raises `onAbilityEffectPerformedOn` for the ability (`AEffectCompound.cs:156-162`).
   - The handler now delegates to it: `OnDuoHealthDecreased` calls `OnDamage`, the partner event calls `OnPartnerEvent`, `CloseDuo` calls `Finish` and then `IsStruck`. `TouchesThisMasher` and the per-record `Struck` list are gone.
   - Tests: `Features/Enemy/Masher Goblin/Editor/MasherDuoCreditTests.cs` (+ `.meta`), 8 tests. They cover a splash centred elsewhere, events without damage, damage with no following event (suspect), damage before any event, zero damage, an out-of-range index and `Begin` resetting.
2. **Should fix 2: suppression release.**
   - The role suppression is no longer released in `Finish`. The pump releases it after the next idle settle, at the top of the next loop iteration, before it dequeues.
   - It is also released at pump exit, on the `turnEnded` backstop and in `StopCounter` (disable or destroy).
   - New edge: if the Masher's own AI action starts before the flow settles, which needs an enemy-turn answer followed straight away by the Masher's own move, that own-turn walk or slam is still listed when the toggle is off. Mark and Linda would then not react to it. It's rare, and it only matters with the toggle off. Watch it in play.
3. **Should fix 3: tether filter.** `JohnTetherPresenter.OnFamilyRoleActivated` now hides the tether when `handler.Unit && handler.Unit.Faction == CombatLevel.Instance.PlayerFaction` (with null guards), instead of checking a closed list of handler types. CRLF kept.

Checks:
- Unity MCP refresh and recompile: console clean, no `error CS`.
- **Full** EditMode suite: 353 tests, 352 passed, 1 failed. The failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, unchanged (CHECKS 706, FAILURES 35).
- No Play mode, no git writes, save not reset.

Commit lists after revision 1:
- Commit 1 (core, suppression query): unchanged.
- Commit 2 (handler rewrite) adds `MasherDuoCredit.cs`, `MasherDuoCreditTests.cs` and their `.meta` files (listed above under Proposed commits). Its other files are unchanged. 14 files.
- The order and dependency stay the same: 1, then 2.
