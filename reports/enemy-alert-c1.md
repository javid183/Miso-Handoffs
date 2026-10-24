# Report: Enemy alert state, C1 (rules, tag gate, tracker, overrides)

Plan: plans/2026-10-23-enemy-alert-state-tech.md (C1)    Agent: miso-implementer    Branch: main (not switched)
Outcome: done (compiles, EditMode 703/704, only the known red fails; the runtime behaviour still needs THJ's play check)

## What changed

All paths under `miso/Assets/_Project/`. New folder `Core/Systems/EnemyAlertSystem/{Runtime,Editor}` (the convention for new systems; it isn't per-character content, so not `Features/`).

New:
- `Core/Systems/EnemyAlertSystem.meta`, `.../Runtime.meta`, `.../Editor.meta`: folder metas (made by Unity).
- `Runtime/EnemyAlertRules.cs` (+ `.meta`): the pure rules (static methods, no state, no Unity objects): `Sight` (floor 5, override), `AlertRange` (ceil half, min 2), `FootprintDistance` / `WithinRange` (Manhattan between nearest tiles of two footprints), `StartsUnaware`, `ClosesTurnOnWake`, `AreaNoiseWakes`, `Spread` (breadth-first, returns each woken index with its step depth). Structs `AlertSpreadNode`, `AlertSpreadStep`.
- `Runtime/EnemyAlertTracker.cs` (+ hand-written `.meta`, guid `7b33b11caf6b46d19e4d00dbede4f2a6`, referenced by LevelBase.prefab): state, registration, wake, spread, per-unit watches, sight checks. Public: `UnawareTagId`, `IsUnaware(GUnit)`, `event Action<GUnit,int> UnitAlerted` (unit, spread depth; for C2's pop).
- `Runtime/EnemyAlertTracker.Events.cs` (+ `.meta`): the bus subscriptions and the noise handler (partial file).
- `Runtime/EnemyAlertSettings.cs` (+ `.meta`): per unit `startsAlert`, `alwaysAlert`, `sightOverride` (0 = derived).
- `Runtime/LevelAlertSettings.cs` (+ `.meta`): per level `allEnemiesStartAlert` (on the level root; found with `CombatLevel.Instance.GetComponentInChildren`).
- `Editor/EnemyAlertRulesTests.cs` (+ `.meta`): 46 cases on the rules.
- `Editor/EnemyAlertDataTests.cs` (+ `.meta`): 4 tests on the data (tag in registry and shown; AI skip query has Stunned + Unaware with policy Any; the query matches an Unaware-only, Stunned-only and both tag set, not an empty one; LevelBase has exactly one tracker).

Changed:
- `Resources/Tags/GTagSet.asset` and `Resources/Tags/GTagRegistry.asset` (its serialized copy, same 9 lines, as the Kin.Dark commit did): `Status.Unaware`, appended after `ShieldUp`, `showInGame: 1`, placeholder icon = the Stunned/Burnt sprite (`9d1441b5…`, fileID 21300000), display name `Unaware`, description `[PLACEHOLDER] Has not noticed the family yet…`.
- `Content/Controllers/AIController.prefab`: `skipTurnTagsQuery` gains `Status.Unaware` (Self, Present) and its policy goes **0 (All) → 1 (Any)** (see assumption 1).
- `Content/Levels/LevelBase.prefab`: one `EnemyAlertTracker` component added to the `GlobalEventBus` GameObject (13 lines). All 58 level prefabs are variants of LevelBase (no other prefab carries `CombatLevel`), and none removes that object, so every combat level gets one tracker.

Not mine (already modified at session start): TextMesh Pro fallback asset, `Packages/manifest.json`, `packages-lock.json`, `EditorSettings.asset`, `ProjectSettings.asset`. The batchmode run did not change any of my edited assets (diff stat is exactly my lines).

No change to GUnit, AIController code, AIFactionBrain, AIUnitBrain, FactionControllerBase or any core file; no graph, utility variable or AI ability edit.

## Where the tracker lives (and why)

On `LevelBase.prefab`, next to the level's `GlobalEventBus`. The bus is created and destroyed with each level prefab, so the tracker's lifetime matches the bus it listens to: no re-hooking per level (the run handler in `CombatLevelContainerScene` outlives levels and would need it), no static, no core edit. On the AIController prefab it would be instantiated once per AI faction (Enemy, Neutral, Stranger), so it would need an election. Dev scenes (`SampleScene`, `TestLevel`) don't use LevelBase and have no tracker: enemies there behave as today.

## Assumption checks

1. **Skip query policy with two entries means "any": false as it was.** The prefab's policy was `0` = `GTagQueryPolicy.All`; with two entries All would need Stunned **and** Unaware. I set it to `1` (Any). With the single Stunned entry, All and Any were equivalent, so Stunned behaves as before. Covered by `EnemyAlertDataTests`.
2. **Enemy play list built once at turn start: not quite, but the timing holds.** `FactionPhaseData.ToPlayUnits` is a live property (`IsAlive && AP > 0 && !IsUnitTurnSkipped`, `FactionPhaseState.cs:17`), recomputed every time `AIController.HandleUnits` picks the next unit. What makes it work: `Reinitialize` (`FactionControllerBase.cs:224`) spends all AP (`Closure`) of every unit skipped at turn start, so a unit Unaware at the enemy turn's start has 0 AP and can't enter the list when it wakes mid-turn. The one gap: a unit that becomes Unaware *during* its own faction's turn (spawned mid-turn with AP) and wakes in the same turn. So the tracker closes the AP of any unit woken during its own faction's turn (`EnemyAlertRules.ClosesTurnOnWake`, only if AP > 0). Same behaviour the plan asked for, without deferring the tag removal; noted under Decisions.
3. **TagSet changes on the main thread while the worker reads TagSet: removal is safe, adding shares an existing race.** `GTagSet.ApplyModifiers` removes by building a new list and swapping the field (`tagEntries = tagEntries.Except(...).ToList()`), so a worker enumerating the old list is unaffected: every wake is safe at any time. Adding does `tagEntries.Add` in place. The tracker adds the tag only at level start (no AI job is queued before the first `turnStarted`) and when a unit spawns. At spawn `AIFactionBrain` itself has just queued a `PlanStrategy` job (its `unitBorn` listener), and any other tag effect (Stunned, Taunted) already has the same exposure. Worst case is an exception inside a worker job, which the worker catches; the plan stays expired and is redone. I didn't defer adds (that would let a spawned unit act before it is gated).
4. **Wake lands before the Masher counter decides: yes.** The Masher queues on `onUnitDamageDone` (raised at `abilityPerformed`) and only checks `CanAnswer` → `IsUnitTurnSkipped` in its pump after the flow is idle (`MasherGoblinFactionRoleHandler.Counter.cs:256-270, 309-313`). The tracker wakes on the HP drop itself (`onValueDecreased`, during the hit), on the effect report and on an evade, all earlier. The counter doesn't need AP (`TryPlayFactionRole`), so the AP close of rule 8 doesn't block it. Not checked in play.
5. **Next-targets prediction re-requested after a wake in the player's turn: yes for wakes inside an action, which is nearly all.** `AIController.UpdateFutureTargets` (private) runs on `abilityPerformed`. The tracker can't call it, so it wakes *before* that listener: during the action (effect reports, HP drops, `unitEndMoving`) or on `onActionFlowEvent(OnActionComplete)`, which `GlobalEventBus.Awake` wires as the first `abilityPerformed` listener, so it runs before the AIController's. Exceptions (prediction stays stale until the next action): a deferred sight check (below), and a wake at the player's turn start (e.g. a player-owned hazard tick damaging an Unaware enemy after `turnStarted` already asked for the prediction).

Also found:
- **The AI moves units in its simulation.** `AIFactionBrain.PredictAllTargets` and `PrepareUnitTurn` call `SimMoveTo` on the worker, which really changes `CurrentCell` until restored. The Neutral brain (allied Toba, Deer: both hostile to enemies, so they count for sight) predicts on every `abilityPerformed` and `turnStarted`. To avoid reading a simulated cell, sight checks skip units of an AI faction that is planning and isn't the current one, and defer a full check to `Update`, run once no action and no AI planning is in progress (`SessionLogs.ActionInProgress` false).
- `IsUnitTurnSkipped` and `UpcomingTurnOrder` use Unity's `!unit` on the worker thread (pre-existing; not touched).

## Stop paths (sight) and what covers them

| Stop path | Code | Event the tracker uses |
| --- | --- | --- |
| End of a walk | `AEffectTransporter.MoveEntity` → `MovementEnd` (raises `unitEndMoving`) | `unitEndMoving` (pairs with the mover), then the end-of-action check |
| Walk stopped early by a blocking tag | `AEffectTransporter` l.382, `MovementEnd(..., false)`: **no** `unitEndMoving` | end-of-action check |
| Teleport (John, Lucy "Blink") | `AEffectTransporter.TeleportEntity`: **no** `unitEndMoving` | end-of-action check |
| Jump (Mark's Vault, Queen) | `AEffectTransporter.JumpEntity`: **no** `unitEndMoving` | end-of-action check |
| Push / pull (incl. Lucy's Cyclone pull via its pusher) | `AEffectPusher` l.186, `unitEndMoving` per pushed unit (if moved ≥ 1 tile) | `unitEndMoving`, end-of-action check |
| Command move | `AEffectCommand.MovementEnd` (`unitEndMoving` when `invokeEndMovement`) | `unitEndMoving`, end-of-action check |
| Swap | `AEffectSwapper`: no event | end-of-action check |
| Dance, Footrace (Duos) | walk transporters (`John_Linda_*_Duo_Ability_Walk`, `Mark_Linda_*`) | `unitEndMoving`, end-of-action check |
| John's shield dash, Mark's continuous attack, role follow-ups, Masher counter | raise `abilityPerformed` themselves | end-of-action check (`onActionFlowEvent`) |
| Appearing: deploy, decoys, summons, pools, waves, Worm split | `GUnit.SpawnAt` → `RegisterUnit` → `unitBorn`; revive/resurrect also raise `unitBorn` | `unitBorn` (registers new units, checks the newcomer's pairs) |
| Anything missed | | `turnStarted` of a faction hostile to the player (full check; deferred if the Neutral AI is still predicting) |

The end-of-action check is a full check of every Unaware unit against every hostile unit at their final cells, so it catches every stop made during an action, whatever moved the unit. It runs only when no other action is running, so a partner still mid-walk doesn't count as stopped (otherwise it is deferred). Passing through mid-walk never counts.

## Noise as built

- **On the unit (rule 6a):** any `onAbilityEffectPerformedOn` naming the unit or a tile it stands on (all its footprint), from anyone (an awake Shaman's heal included, per the tech plan); any HP drop (`onValueDecreased`, so spikes and Burn too); an evade (`onUnitEvaded`); gaining the taunt tag (`GlobalSettingsSO.tauntTag`), which is how the Black Claw's pact call reaches its Dark Claws (`MemorableAttackMemoryShare` → `TauntByAbility`).
- **Near it (rule 6b):** tiles reported by `onAbilityEffectPerformedOn` (cells, or the footprint of a reported unit) within the Unaware unit's alert range, when the caster is on the player's side (player faction or any faction allied to it), the ability is not a Move, and the ability is still being performed (`SessionLogs.ActionsInProgress`). The last check is what keeps hazard and status ticks quiet: a hazard reports with the ability that created it, but after that ability finished.
- Spread runs from every unit that wakes, through `EnemyAlertRules.Spread`.

## Acceptance criteria (C1 part)

- [x] Placed enemy with no hostile in sight takes no action and is absent from the next-targets prediction: the gate is the tag + skip query (`IsUnitTurnSkipped` drives `ToPlayUnits`, `Reinitialize` and `UpcomingTurnOrder`). Data tested; **needs play**.
- [x] Sight = max(5, walk + longest attack reach) or the override; alert = ceil(sight/2), min 2: `EnemyAlertRulesTests`. Walk/attack reach = largest `Parameters.radius` among unlocked Move / Attack abilities (`UnitThreatAnalysis.PickMoveAbility`'s rule).
- [ ] Bergson stopping within sight wakes it; passing through doesn't: built (table above); **needs play**.
- [ ] Hit from anywhere wakes it; player ability on tiles in alert range wakes it; hazard tick doesn't: rule part tested (`Noise_*`); hookup **needs play** (Linda from range, role follow-up, Duo, a Lucy hazard tick).
- [x] Spread, recursive: tested (`Spread_*`, multi-tile included).
- [ ] Timing (player's turn → next enemy turn; enemy turn → the turn after): rule tested (`Timing_*`), mechanism above; **needs play** (Masher counter, Lucy's role in the enemy turn).
- [ ] Spawned enemies start Unaware unless a hostile is in sight: rule tested (`Start_SpawnedWithAHostileAlreadyInSight_StartsAlert`); **needs play** (Shaman summon, Worm split).
- [ ] Allied Toba and Deer never Unaware: both are `Neutral`, allied to `Bergsons` in LevelBase's relations, so `GetFactionRelationToPlayer` is Ally; rule tested. Bosses and flagged levels: components built; data is C3.
- [ ] Unalerted Masher hit by an adjacent attack wakes and counters: order checked in code (assumption 4); **needs play**.
- [x] No new GUnit, AIController or brain code; no graph, variable or AI ability edits.
- [x] Compile clean; EditMode 703/704. The one failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, still 38 failures out of 709 checks, as in the last report; none mentions the tag, the controller or the level prefab. Not re-baselined.

## Test results

Batchmode, Unity 6000.3.4f1, editor closed (no `miso/Temp`). `results.xml` and `test.log` in the implementer's scratchpad. 704 tests, 703 passed, 1 failed (the known red). The 50 new cases all pass. No compiler warnings from the new files.

## Save reset

No.

## Decisions I made

- **AP close instead of deferring the tag removal** for wakes in the unit's own faction's turn (same behaviour; see assumption 2). It also means C2's marker and pop can follow the tag at the real wake moment.
- **No spread from units that start alert** (level start or spawn with a hostile in sight): they aren't waking, so they don't wake their neighbours. A pack with one member in sight at level start: that one comes, the rest sleep until noise or sight. Coordinator/THJ may want the opposite (one line to change: call `Wake` instead of skipping in `Register`).
- **Moves make no area noise**, only sight (the design's "the Dance and the Footrace are moves: sight only"). It only differs from "noise on the destination" when a sight override is below 4 (alert range then exceeds sight).
- **"Player-side"** = player faction or any faction allied to it. The Deer is `Neutral` like the allied Toba, so its walk counts too; it only has a walk, which makes no area noise anyway.
- **Hazard ticks wake the unit they hit** (rule 6a "anything that damages it"), never its neighbours.
- Sight and alert range are computed once per unit when it is first seen (level start or spawn), as the design said ("read at level start").
- A unit seen before (revived or resurrected) keeps its state; a unit that dies Unaware stays Unaware if revived.
- If `Status.Unaware` were missing from the registry, the tracker logs one error and leaves every enemy alert, instead of throwing in `GTagSet`.

## Needs THJ

None blocking. Two choices for the coordinator to confirm or flip (both one-line changes): no spread from units that *start* alert; and the floating "Unaware" text (next item).

## Docs to update

- `tech/combat-architecture.md` (coordinator): the tracker (on LevelBase next to the bus), the tag gate, the stop-path table, the simulated-cells caution.
- `tech/core-systems.md` (coordinator): the AI controller's skip query is now `Stunned` OR `Unaware` (policy Any); a new skip tag needs no policy change.
- `design/gdd/enemies.md` (designer): Source lines for EN-12 to EN-17 once played: `Core/Systems/EnemyAlertSystem/`, `Status.Unaware`.

## Risks and loose ends

- **"Unaware" floating text.** `GUnit.ShowTagGained` pops the name of any `showInGame` tag on gain, so every enemy shows a white "Unaware" pop at level start, and each spawn that starts Unaware shows one. Not a wake pop, but visible. For C2 / THJ to decide; turning `showInGame` off also removes the info-panel line.
- **`[PLACEHOLDER] ` stripping:** I found no code that strips the prefix (only data uses it, e.g. the Shaman heal description). The tag's display name is the plain working name `Unaware`; only the description carries the prefix, so it shows in the tooltip as written.
- **Masher preview vs real counter:** `MasherGoblinFactionRoleHandler.Preview.cs:69` shows no counter preview for a skipped (Unaware) Masher, but hitting it wakes it and it counters. The preview promises less than happens. For C2 or a small follow-up.
- **An all-Unaware enemy turn still plays its banner and turn-start pause**, then ends at once (no camera visits). The design asked for such turns to end at once; the banner is the existing flow.
- **Deferred sight checks** (only while a non-current AI faction is predicting or another action runs) wake a frame or more later, and that wake doesn't refresh the next-targets prediction until the next action.
- **Pact call side effect (pre-existing):** `MemorableAttackMemoryShare` taunts nearby Dark Claws on *any* ability performed on the Black Claw, including an awake Shaman's heal; that taunt now also wakes them.
- **Area noise needs the ability to be in progress at impact.** Projectiles (Linda's arrow) are assumed to land before their ability completes (`AbilityPreset.Activate` waits on its effects). If one lands after, its hit still wakes the target but not the neighbours. Play check.
- Placeholder icon is the Stunned/Burnt sprite (an outdoor lamp); C2 can swap it.
- Spawn-time add of the tag shares the existing worker race (assumption 3).

## Proposed commits

1. `feat(enemies): enemy alert rules with edit-mode tests` (plain):
   `Core/Systems/EnemyAlertSystem.meta`, `Core/Systems/EnemyAlertSystem/Runtime.meta`, `Core/Systems/EnemyAlertSystem/Editor.meta`, `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertRules.cs` + `.meta`, `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertRulesTests.cs` + `.meta`.
2. `feat(enemies): enemies start unaware and skip their turns until they see or hear the family` (risky: changes every level's pace; touches the AI skip query, behaviour via data only):
   `Resources/Tags/GTagSet.asset`, `Resources/Tags/GTagRegistry.asset`, `Content/Controllers/AIController.prefab`, `Content/Levels/LevelBase.prefab`, `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.cs` + `.meta`, `Runtime/EnemyAlertTracker.Events.cs` + `.meta`, `Runtime/EnemyAlertSettings.cs` + `.meta`, `Runtime/LevelAlertSettings.cs` + `.meta`, `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertDataTests.cs` + `.meta`. Depends on 1.

Per the play-test-before-commit rule, commit 2 should wait for THJ's play (or for C2/C3 if the coordinator bundles the play check).

## Other branches

`thj/home-test` when it takes `main` (as the plan says).

## How to see it

1. Open Unity (recompile), open any Generic level whose enemies start well away from the family (more than 5 steps from every Bergson), press Play.
2. At level start: each far enemy shows a white "Unaware" pop and, on hover, an "Unaware" line in its info panel. An enemy within 5 steps (Manhattan, through walls) of a family member has no Unaware line.
3. End the turn without moving: the enemy turn ends at once; Unaware enemies don't move. Their next-targets list is empty.
4. Walk a Bergson so it **stops** 5 steps from a Dark Claw (6 for an Archer): the Claw loses Unaware; Claws within 3 of it lose it too (spread). It acts on the next enemy turn. Walking past it and stopping farther away does nothing.
5. From out of sight, hit an Unaware enemy (Linda's arrow): it wakes, and Unaware enemies within its alert range of the hit tile wake too.
6. Wait next to a Lucy fire hazard or spike tile near (not on) an Unaware enemy across turns: it stays Unaware.
7. Hit an Unaware Masher with an adjacent attack: it wakes and counters as before.
8. In a level with the allied Toba or the Deer: neither shows Unaware.
9. Optional: add `EnemyAlertSettings` to a placed enemy (`startsAlert`) or `LevelAlertSettings` (`allEnemiesStartAlert`) to the level root: those start alert, with no "Unaware" pop.
