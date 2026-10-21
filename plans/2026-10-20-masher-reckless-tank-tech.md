# Masher Goblin: reckless tank (tech plan)

Size: L    Tier: 3 (core: Masher handler, AI controller, level run)    Assigned to: miso-implementer (opus for C1, C3, C4; sonnet for C2, C5)
Branch: masher-tweak (THJ's branch from `main`; merges to `main` later)
Status: approved 2026-10-20 (T1 to T4 all (a): D-101 to D-104); C1–C4 done; C5 in progress

## Why

THJ's request of 2026-10-20: make the Masher a reckless tank. Design: `plans/2026-10-20-masher-reckless-tank-design.md` (revision 2). Rules decided by THJ: D-092 to D-100 (`decisions.md`). This plan says how to build it. Research: two Explore sweeps on 2026-10-20; the findings are folded in below with file:line refs. Paths are under `miso/Assets/_Project/`. "H" = `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs`.

## Goal

Every provoking hit makes the Masher step 1 tile toward the unit that struck it. If it then stands 4-directionally next to that unit, it slams that unit's tile with a copy of its main slam (plus area, 10 ×, both sides hurt). The own-turn slam uses the same aim rule.

## The rules to build (from D-092 to D-100)

1. **Provokers.**
   - On the player's turn: the acting unit's chosen ability (follow-ups and projectiles included) and Duos.
   - In any phase: Family Roles and other reactions.
   - Never: burn, Pass-by, allied AI units, anything that isn't a player-faction unit.
2. **Duo partner.** It answers the partner who struck it. If both struck it, the one it can reach. If it can reach both, the one who acted first.
3. **Timing.**
   - A chosen ability or Duo is answered once the whole action has resolved (follow-ups, QTEs, roles, sequences), from the striker's tile at that moment.
   - A reaction is answered once that reaction has resolved.
   - On the enemy turn: after the current enemy unit's action completes (D-100). The AI then plans the Masher from its new tile on its next action. It already replans every action from the live board (`AIController.cs:154-158`, `_blackboard.Update`), so no replan API is needed.
4. **Step.** One normal move (1 tile, 2 × 2 footprint must fit on a free path) toward the provoker, at any distance. It doesn't step when it is already next to the provoker, when the path is blocked, or when it is Crippled.
5. **Aim, counter and own turn.** The struck cell is the target's own tile (one of `OccupiedCells`), and the Masher must be 4-directionally next to it from any footprint tile. It never aims at an empty tile.
6. **Blow.** The counter is a copy of the main slam (D-096): plus area, any faction, 10 × `Stat_DMG`.
7. **Statuses.** Stunned: no answer (already true). Crippled: no step (new).
8. **Toggle** `counterCanProvokeFamilyRoles`, default true (D-097). Scope: see T3.
9. **No limit** per turn (D-098).
10. **Safety stop** (D-099). At most 10 answers per root action. Past that, provoking hits are ignored until the root action resolves, and a `Debug.LogWarning` is written. The counter resets when the root action resolves, and on `turnEnded` as a backstop.

## Questions for THJ before dispatch (Tier 3)

**T1. The AI turn loop must wait while a Masher answer runs (core, `AIController`).**
- *Context:* the AI loop waits only on *other* controllers before planning the next unit (`AIController.cs:96-98`). An enemy-turn answer runs on the AI's own controller. The loop can then plan on a worker thread while the Masher moves, and leave stale targets (`FactionControllerBase.cs:948`). This can't be fixed from the handler.
- *Options:*
  - (a) **Recommended.** Add `|| PhaseData.IsInProgress` to that wait. One line, no API change, its own commit. It changes core AI timing only while an action is already running.
  - (b) No enemy-turn answers until a later pass, which goes back on D-094.

**T2. The turn switch must wait for a queued answer (core, `CombatLevelRunHandler`).**
- *Context:* when the player's last action ends the turn, `RequestEndTurnSafe` runs 0.1 s after `abilityPerformed` (`FactionControllerBase.cs:976-979`). `SwitchTurnIE` waits only on `isActionInProgress`, sequences and level behaviour (`CombatLevelRunHandler.cs:460-462`). A queued answer that waits for the action to finish can slip past the turn switch. The last attack of a turn is very often the one that provokes it.
- *Options:*
  - (a) **Recommended.** An additive public hold: `CombatLevelRunHandler.RegisterTurnSwitchHold(object)` / `ReleaseTurnSwitchHold(object)`, plus a hold-count check in the `SwitchTurnIE` wait. The handler holds while its queue isn't empty.
    - Reusable by any future reactive enemy.
    - The hold set is cleared on level end and in `ResetPlayModeState` if static (it shouldn't be static).
    - Own commit, core review.
  - (b) Answer at once from inside `abilityPerformed`, like today: no core change. But a "whole action" answer then fires before follow-ups and roles, and the attacker's end tile is wrong for Continuous Attack and approach attacks.
  - (c) Drop queued answers at turn end. No core change, but the turn's last hit is often never answered.

**T3. What the toggle can block (D-097).**
- *Context:* when the toggle is false, the answer must start no Family Role. Each role reacts differently:
  - **John:** relays only on the enemy turn. He reads `abilityStarted` plus `ActionsInProgress[0]`. The handler can skip `abilityStarted`. Finding: John probably can't relay a Masher answer even today, because the Masher raises `abilityStarted` before the action is recorded (H:148-149, `RuntimeAbility.cs:311,336`). The verifier checks this in play.
  - **Mark:** fires on the answer's `abilityPerformed`, which must still be raised for John's Blood Debt (`JohnPassiveAbility_BloodDebt.cs:73-77`). The handler can't stop him cleanly. Mark's prefab has a `triggerAbilityBlacklist` (`MarkFactionRoleHandler.cs:19,31`), but it is static data, not the Masher's toggle.
  - **Linda:** fires on `unitEndMoving` from the step's transporter (`AEffectTransporter.cs:190,202`). It isn't configurable without a core change in the effects family.
  - **Lucy:** never reacts to an enemy action.
- *Options:*
  - (a) **Recommended.** Add a read-only query `IsRoleProvocationSuppressed(RuntimeAbility)` (a static on the Masher handler, or a small registry). Mark's and Linda's role handlers check it before triggering. When the toggle is false, the answer's ability and its step are listed there.
    - This touches two Bergson role handlers. Family Roles are core, but this is an additive check.
    - Fully honours D-097.
  - (b) The toggle blocks John only (inside the handler). Mark and Linda still react. Cheap, but the toggle mostly does nothing.
  - (c) Use Mark's blacklist (data) for Mark, leave Linda. Partial, and it isn't per Masher.

**T4. `AIRegressionTest` catalog line.**
- *Context:* the test catalogs every ability asset (`AIRegressionTest.cs:113`, Masher at `:156-157`). A new `MasherGoblin_Ability_Counter` asset adds a second failure, `abilities.count` / `abilities.unexpected`, on the already-red test. The unit catalog stays green, because the counter isn't on the unit's ability list. `targetType` isn't in the baseline.
- *Options:*
  - (a) **Recommended.** Add one `ExpectedAbilityCatalog` line for the new asset. This is not a re-baseline, and touches nothing else in the test.
  - (b) Leave it. The test stays red for one more reason, and its dedicated fix session adds the line.

Everything else below is within the approved design, Tier 1 or 2.

## Acceptance criteria

- [ ] A chosen ability that hurts the Masher on the player's turn makes it step 1 tile toward the striker, unless it is already adjacent, blocked or Crippled. If it then stands next to the striker, it slams the striker's tile once.
- [ ] The slam hits everyone on the struck tile and the 4 around it, enemies and the family alike, at the slam's damage.
- [ ] Standing on a side or back tile of its cross, not adjacent to it, no longer gets a unit hit. The answer is only a step.
- [ ] On its own turn, the Masher only aims at a tile holding an enemy unit that it stands next to (AI candidates come from `targetType` 2).
- [ ] Mark's Continuous Attack, approach attacks and dash attacks are answered once, after the whole action, from the tile the striker ends on.
- [ ] A Duo is answered once: on the partner who struck it, or by the D-095 tie rule.
- [ ] A Family Role hit is answered on either turn, after the role resolves. On the enemy turn, after the current enemy unit's action (needs T1).
- [ ] An answer pending when the player's last action ends the turn still plays before the turn switches (needs T2(a)).
- [ ] Burn, Pass-by and allied AI hits don't provoke it.
- [ ] Hits that land during an answer are queued and answered afterwards, not dropped.
- [ ] With the toggle false, no Family Role fires because of an answer (scope per T3). With it true, today's role behaviour holds.
- [ ] An 11th answer in one root action doesn't happen. A warning is logged, and the next root action answers normally.
- [ ] The "did not initialize its role ability" warning is gone, and the prefab has one handler, not two.
- [ ] Hover preview while aiming at the Masher:
  - it shows the step at any range, and slam tiles only when it would end adjacent;
  - the slam is centred on the striker's tile;
  - every unit in the cross shows its damage;
  - it still shows after the first answer in a turn;
  - it uses the striker's end tile for basic-attack approach and `AEffectDashAttack` abilities.
- [ ] EditMode suite green except `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).
- [ ] New EditMode tests cover the pure rules (C2).

## Scope

In:
- the counter preset;
- the `targetType` change;
- prefab cleanup and the toggle field;
- the handler rewrite (queue, provoker filter, Duo tracking, Crippled, chain cap, toggle);
- the core holds per T1, T2 and T3;
- the preview changes;
- the rules class and its tests.

Out:
- Masher AI scoring beyond the aim rule;
- Immovable exceptions;
- Family Role cost and limits (FR-3, FR-4);
- the end-tile preview for `AEffectTransporter` and `AEffectCommand` abilities (John's Shield Dash, Mark's Vault): their preview measures from the current tile. Logged as a follow-up (Tier 2 below);
- John's relay of Masher answers, if play shows it never worked (follow-up, not a fix here).

## Touches

Systems:
- `MasherGoblinFactionRoleHandler.cs` (core, Family Roles);
- `AIController.cs` (core, T1);
- `CombatLevelRunHandler.cs` (core, T2);
- `MarkFactionRoleHandler.cs` and `LindaFactionRoleHandler.cs` (core, T3(a));
- the Masher presets and prefab (data);
- `AIRegressionTest.cs` (T4(a), one line).

No change: `FactionRoleHandlerBase.cs`, `UnitsCooperationHandler.cs`, `GlobalEventBus.cs`, `AbilityDamagePreview`, `UnitThreatAnalysis`.

USPs: Family Roles (provokers and the toggle) and Duos (provokers).

Docs:
- GDD `enemies.md`, `combat-rules.md` and `family-systems.md` (game designer; the wording is in the design plan);
- `glossary.md` (narrative);
- `tech/combat-architecture.md` and `tech/core-systems.md`, the turn-switch hold note (coordinator);
- `build-log.md` (coordinator);
- the GDD mirror re-sync.

## Approach (chunks; one implementer run each, one commit each unless noted)

### C1. Core turn-flow holds (opus; T1, T2)

- `AIController.cs:96-98`: add `|| PhaseData.IsInProgress` to the per-unit wait.
- `CombatLevelRunHandler`:
  - a private `HashSet<object> _turnSwitchHolds` and the public methods `RegisterTurnSwitchHold(object)` / `ReleaseTurnSwitchHold(object)`;
  - add `|| _turnSwitchHolds.Count > 0` to the `SwitchTurnIE` `WaitWhile` (`:460-462`);
  - clear the holds on level end and on destroy;
  - instance fields only, no static.
- Two commits: AI wait, then turn-switch hold. Each is reviewed as a core change.
- Accept:
  - compiles, and the suite is unchanged;
  - with no holds registered, turn flow is identical (reviewer reads the diff);
  - an EditMode test for the hold set, if it can be reached without a scene; otherwise reviewer-only.

### C2. Pure rules class and tests (sonnet)

Add `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`. It is static and pure, over `Vector2Int` or generic `T` cells, following the pattern of `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs` and `RoleZoneRules.cs`. Functions:

- `IsAdjacent4(footprint, targetCells)`.
- `PickAttackCell`: the target's own tile that is adjacent.
- `RankStep`, over candidate (canAttack, distanceToTarget, walkLength) entries:
  - adjacent-capable cells win, shortest walk first;
  - otherwise the cell that strictly reduces distance, nearest first, then shortest walk;
  - otherwise none.
- `Classify(provoker facts)`, returning ChosenAbility / Duo / Reaction / Ignore. The inputs are flags, not Unity objects:
  - is the owner player-faction;
  - is it the owner's `FactionRoleAbility`;
  - is it a Duo trigger or partner;
  - is the owner the acting unit;
  - is it the player phase.
- `PickDuoPartner(partners with struck, reachable, actedOrder)`.
- `ChainCap`, a small struct: `TryConsume()`, `Reset()`, `Max = 10`.

Tests go in `Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs`. Accept: every rule above has tests (including the cap at 10 and the D-095 tie rule), and the suite is green apart from the known red.

### C3. Data (opus; T4)

Write a one-off editor script under `Features/Enemy/Masher Goblin/Editor/`, menu `MISO/Masher/Build Counter Preset`. It copies `MasherGoblin_Ability_Attack.asset` to `MasherGoblin_Ability_Counter.asset` with `AssetDatabase.CopyAsset`:
- sub-assets are copied with it;
- the spawner and AOE prefab are shared by reference, not copied, so a damage change on the counter needs a copied AttrMod later. The implementer reports which references are shared.

No such script exists yet, so this is a new tool. It is one-off and Tier 2 within an approved plan; it is deleted after use or kept under `Editor/`, and the implementer says which.

The other data changes:
- `targetType` 3 → 2 on both presets.
- `Unit_MasherGoblin.prefab`:
  - the root handler's `ability.preset` = the counter. Copy `stateName: PrimaryAttack` and `abilityActivationFrame: 12` from the child handler.
  - remove the child handler `8123456789123456791` from `m_AddedComponents` (`:702-711`) and its block (`:745`). Keep the child FXRunner if anything uses it; the implementer checks.
  - the unit ability list is unchanged.
- T4(a): one catalog line in `AIRegressionTest.cs`.

Accept:
- compiles;
- the warning is gone in Play;
- the AI catalog failure is unchanged from before (only the known red);
- the counter is not on the unit's ability list.

### C4. Handler rewrite (opus; T3)

Keep it a partial-class split: `MasherGoblinFactionRoleHandler.Counter.cs` (queue and trigger) and `.Preview.cs` (C5).

1. **Inputs.**
   - `onUnitDamageDone` where the target is this Masher: classify with C2, using `source.Owner.AbilityOrchestrator.FactionRoleAbility`, `CooperationHandler.TryGetSecondPerformer`, the controller's `ActiveAbility` / `CurrentlySelectedUnit` and `CombatLevelRunHandler.Instance.CurrentFaction`.
   - Ignore `onUnitDamageDone` whose source is a Duo trigger: the trigger's flush credits the activator, not the partner.
2. **Duo tracking.**
   - `onSynergyTriggered` with id `"Duo"` opens a Duo record.
   - `onAbilityEffectPerformedOn` with a partner-owned ability and this Masher, or its cells, as entity marks "struck" and the order.
   - The Masher's HP `onValueDecreased` confirms damage (pattern: `JohnPassiveAbility_Wrath.cs:164-171`).
   - The trigger's `abilityPerformed` closes the record and enqueues one provocation with the D-095 pick.
3. **Queue and pump.**
   - `OnDamaged` enqueues (provoker unit, kind). It never acts directly.
   - On the first enqueue, the handler registers a turn-switch hold (C1).
   - The pump waits until all of these hold:
     - `!SessionLogs.Instance.ActionInProgress` (all controllers);
     - `ActionsInProgress.Length == 0`;
     - `!QuickTimeEventHandler.IsEventActive`;
     - `!SessionLogs.SequenceInProgress`;
     - then one more frame (Continuous Attack waits a frame, `MarkPassiveAbility_ContinuousAttack.cs:333`).
   - Then it dequeues, and drops the entry if the provoker is dead or downed, or the Masher is dead or Stunned.
   - It consumes the chain cap; past the cap it drops the entry and logs a warning.
   - It runs the answer through `TryPlayFactionRole(Unit, onComplete)` (`FactionControllerBase.cs:182`), and re-pumps on `onComplete`.
   - When the queue is empty, it releases the hold.
   - On `turnEnded` it clears the queue and the cap and releases the hold, as a backstop.
   - Remove the `:77` drop guard: hits during an answer now queue.
4. **Root action and cap reset.** The cap resets when the pump finds the queue empty and the whole flow idle. That is the end of the root action.
5. **Step and aim** go through C2 (`PickAttackCell`, `RankStep`):
   - gate the step on `_walk.CheckActivationFeasibility()` (Crippled);
   - the answer slams only when adjacent after the step.
6. **Toggle.**
   - Add the serialized `counterCanProvokeFamilyRoles = true` on the handler.
   - When it is false, skip `abilityStarted` for the answer. Keep `abilityActivationStarted` and `abilityPerformed`, which John's passives need.
   - Per T3(a), register the answer's ability and step in the suppression query, with a check added in Mark's and Linda's role triggers. That check is its own commit (core).
7. **Announce.** `FactionRoleHandlerBase.Activate` still raises `onFamilyRoleActivated`. `JohnTetherPresenter` hides the tether on any handler (`:139,177`); filter it to Bergson handlers there. This is not core; it's a small fix in the same commit as C4.
8. **Base initialization** (C3 review): call `base.Initialize(orchestrator)` and `base.InitializePartially(orchestrator)` from the overrides so `_abilitiesInitialized` is set; this is what removes the "did not initialize its role ability" warning (moved here from C3's acceptance).
9. **Classify doc comment** (C2 review): name every caller-side exclusion (Pass-by, allied AI units) and define `ownerIsPlayerFaction`.
10. **Reviewer constraints from C1** (`reports/masher-c1-review.md`): retry when `TryPlayFactionRole` returns false; hold until the last answer's `onComplete`; frame-based or unscaled pump waits; Duo "reachable" uses the same rule as the step.
11. **Play-mode reset.** No statics, except the T3(a) suppression query if it's static. That one needs a `ResetPlayModeState()` hooked in `PlayModeStaticReset.Reset()`.

Accept: the trigger, timing, Duo, queue, toggle and cap criteria above (play check), and the suite stays green.

### C5. Preview (sonnet)

Changes to the handler's preview (H:367-460), moved to `.Preview.cs`:
- drop the `ActivatedAtThisPhase` gate;
- compute the striker's end tile:
  - basic-attack approach: needs `PlayerController.TryFindApproachCell`, which is private;
  - `IGhostDestinationProvider`: needs `PlayerController.ResolveGhostCell`, which is private;
  - expose both as public, read-only, additive, or move them into a static helper. This is a core API addition (Tier 2, additive, no behaviour change; own commit).
  - other moving abilities use the current tile.
- show the step ghost and path at any range, and slam tiles only when adjacent;
- centre the slam on the striker's tile;
- show damage on every unit in `AbilityDamagePreview.ComputeFor`, tracked in a list for clearing;
- Duo case: if the selected ability is a Duo trigger, preview the D-095 partner pick.

Accept: the preview criteria above, in play.

## Risks

- **Domain reload off.** No new statics, except possibly the T3(a) query, which gets a `PlayModeStaticReset` hook.
- **AI thread safety.** C2 rules are not called from the worker thread. The `targetType` change is read by `AIUnitBrain.cs:411-460, 522-544` on the worker: data only, no new code there. The AI target becomes a `GUnit`, so the slam spawns at the unit's position. Same tile for 1 × 1 targets; check a 2 × 2 target (the Big Ogre) in play.
- **Prefab YAML.** Removing an added component: a small edit, or done via the editor script in C3. The reviewer diffs the prefab.
- **Event cleanup.** Every new subscription is unsubscribed in `OnDisable`/`OnDestroy`. The hold is released on `turnEnded`, level end and destroy, so a stuck hold can't freeze the turn switch.
- **Stuck turn switch** (T2). Worst case, a bug leaves a hold registered and the turn never switches. Mitigations: release on `turnEnded` can't run if the turn never ends, so the pump also releases when it finds the queue empty, and a 5 s real-time watchdog releases the hold with a warning.
- **AIRegressionTest.** Only the T4 catalog line. No re-baseline.
- **Other branches.** `thj/home-test` would need all of this at merge. Note it in `branches.md` once it's built.
- **John relay.** It may never have worked on Masher answers. The verifier checks it; any fix is a follow-up.

## Gates

- Compile: clean console.
- EditMode suite: green except the known red.
- Reviewer: every chunk; C1 and the T3 role-handler commit get extra core scrutiny.
- Play check: **yes, needs THJ's time.**
  - Levels: `Generic Levels/Easy/E3/LevelE3-C1.prefab` or `Medium/M1/LevelM1-C3.prefab`.
  - Cases:
    - melee bait;
    - ranged pull at 2, 4 and 6 tiles;
    - side-of-cross tile (no hit);
    - a slam hitting goblins;
    - Continuous Attack;
    - a Duo with both partners striking;
    - Linda's lane chain;
    - Mark's chain on the enemy turn, with the toggle on and off;
    - Crippled;
    - two answers in one turn with the preview shown;
    - the last action of the turn provoking an answer;
    - the cap (a forced chain via a cheat or a test level, if feasible);
    - a 2 × 2 target.
- Docs: listed under Touches.

## Commit log

- C1 (AI wait + D-106 recheck): `08ca1d819` (2026-10-20)
- C1 (turn-switch hold + tests): `11f64c19f` (2026-10-20)
- C2 (rules class + tests): `212638ad2` (2026-10-20)
- C3 (data: counter preset, targetType, prefab, builder tool): `e409b2c94` (2026-10-20)
- C3 (AIRegressionTest catalog line, D-104): `519e05d9e` (2026-10-20)
- C4 (role suppression query + Mark/Linda checks, D-103): `7556630a6` (2026-10-20)
- C4 (`FactionRoleHandlerBase` super-time null guard, D-116): `d5402d48d` (2026-10-20)
- C4 (handler rewrite, queue, Duo credit, tether filter): `9e6d50f51` (2026-10-20)
