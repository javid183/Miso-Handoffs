# Core systems

Owner: coordinator; THJ approves additions and removals. Paths are under `miso/Assets/_Project/`.

**Why this list matters:** changing the public API or behavior of anything here is **Tier 3** (ask THJ first). Any bugfix inside one is **Tier 2** (flagged in the report). The reviewer checks every change against this list.

**Status:** seed list built on 2026-10-15 from `tech/mechanics-brief.md` (code read of 2026-10-03). The setup session checked every path and description against the code the same day and added what combat relies on that was missing, marked *(added in setup)*, with usage counts as evidence. **[THJ] prune.**

## Abilities and effects

| System | Main files | Why it's core |
| --- | --- | --- |
| Ability data and runtime | `Core/Systems/AbilitySystem/Abilities/Runtime/AbilityPreset.cs`, `RuntimeAbility.cs`, `AbilityOrchestrator.cs` | Every unit action goes through them |
| Effects | `Core/Systems/AbilitySystem/Effects/Runtime/AEffectBase.cs`, `AEffectCompound.cs` (and the `AEffect*` family, 20 files; since 2026-10-21, D-123: `AEffectCompound.ApplyUnguarded` applies John's per-action relay record from `Abilities/Runtime/FamilyRoleRelay.cs`, a static registry reset in `PlayModeStaticReset`, a no-op when no record exists) | Every ability's result; compounds carry shapes, unlocks and sub-effects |
| Area shapes *(added in setup)* | `Abilities/Runtime/AreaShapeDefinition.cs`, `Effects/Runtime/IAffectedAreaProvider.cs` | Where an ability lands; the interface is read in 7 files |
| Duos (cooperation) | `Abilities/Runtime/UnitsCooperationHandler.cs`, `Effects/Runtime/AEffectCoOpTrigger.cs` | USP: Duos |
| Pass-by | `Abilities/Runtime/UnitsPassByHandler.cs` | Tag mechanic; fills FTP/ATB; Synergies |
| Family Roles | `Abilities/Runtime/FactionRoleHandlerBase.cs`; handlers for John, Linda, Lucy and Mark in `Features/Player/<Name>/Scripts/<Name>FactionRoleHandler.cs`, and the enemy-side `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs` (partials `.Counter.cs`; rules `MasherCounterRules.cs`, queue `MasherCounterQueue`). Since 2026-10-20 (D-103): `FactionRoleProvocationSuppression`, a static read-only query (reset in `PlayModeStaticReset`) that Mark's and Linda's handlers check before triggering. Toba has no handler | USP: Family Roles |
| Damage preview | `Abilities/Runtime/AbilityDamagePreview.cs` | Must match the real hit (rounding, lethal checks) |

## Points

| System | Main files | Why it's core |
| --- | --- | --- |
| AP | `Core/Systems/AbilitySystem/Points/Runtime/APConsumer.cs`, `ActionPoints.cs`, `FamilyActionPoints.cs` | Every AP spend and gain; PerUnit vs Shared |
| FTP / ATB | `Points/Runtime/FamilyTimePoints.cs`, `ATBGauge.cs`, `PointConsumer.cs` | Family resource; differs by branch |

## Entities, units, stats and factions

| System | Main files | Why it's core |
| --- | --- | --- |
| Game entity base *(added in setup)* | `Core/Fundamental/GameEntity.cs` | Root of every effect owner and target: tags, attributes, `IsAlive`, phase ticks. GridCell, GridPluggableEntity, GUnit, SpawnableEntity and its subclasses derive from it; referenced in 72 files |
| Phase ticks *(added in setup)* | `Core/Fundamental/IHandlePhaseTick.cs`, `IHandleEndPhaseTick.cs`, `IHandleUnitTick.cs`, `GeneralEnums.cs` (`PhaseTickMoment`) | Turn-timed behavior; implemented by RuntimeAbility, AbilityOrchestrator and several effects (about 10 types) |
| Units | `Core/Units/Runtime/GUnit.cs` (since 2026-10-20, D-121: additive `ShowGhostAt(Vector3, Vector2 facing)` flips the ghost by `EntityAnimationHandler`'s rule; since 2026-10-23, D-152, `b1848c5e8`: the attacker memory is the ordered, locked `RecentAttackerMemory` (`Core/Units/Runtime/RecentAttackerMemory.cs`): a repeat attacker moves to newest, the oldest drops past `unitsAttackMemorySize`, so `GetMostRecentAttacker()` is really the last attacker; same API. Read on the AI worker thread via `TargetRecentAttackFactor` → `GetRecentAttackFactor` (now reflects real recency), by Lucy's role and by `BarkManager`) | The one unit class for both sides |
| Other combat entities *(added in setup)* | `Core/Entities/Runtime/SpawnableEntity.cs`, `OnGridEntity.cs`, `Projectile.cs`, `HazardEntity.cs`, `GameEntityBundle.cs` | Summons, projectiles and hazards; `GameEntityBundle` is the multi-target wrapper `AEffectBase.Apply` unpacks |
| Attributes | `Core/Systems/AbilitySystem/Attributes/Runtime/AAttribute*.cs` (incl. `AAttributeSet`, `AAttributeRegistry`), `RuntimeAAttribute.cs`, `RuntimeAAttributeBase.cs`, `AAttributeModifier.cs` | HP and pools; modifier order. Every hit lands here (see "Damage and death" below) |
| Stat evaluation | `Core/Systems/StatsResourcesSystem/Runtime/StatAttributes/StatEvaluation.cs`, `StatAttributeSet.cs`, `StatBackedValue.cs` | Source order Ability → Unit → Equipment → Faction → SkillTree (+ Home layer) |
| Stat context *(added in setup)* | `StatsResourcesSystem/Runtime/StatAttributes/IHaveStatAttributes.cs` | Passed into every `AEffectBase.Apply`; implemented by GUnit, RuntimeAbility and Faction; used in 45 files |
| Tags *(added in setup)* | `Core/Systems/TagSystem/Runtime/` (`GTag`, `GTagSet`, `GTagQuery`, `GTagReference`, `GTagModifier`, `GTagRegistry`, `IOwnGTags`) (since 2026-10-24, D-166, `b8ea2ff58`: `GTagDefinitionSetSO.GetEntities()` links each root's parents before collecting, so editor IDs no longer depend on the registry's separate serialized copy) | Tags on every entity and the effects' accept filters; imported by 46 files |
| Referenceable ids *(added in setup)* | `Core/Utilities/ReferencableEntities/Runtime/` (`ReferenceableEntity`, `ReferenceableEntityRef`, `ReferenceableEntityRegistry`, `ReferenceableEntityDefinitionSetSO`) | The id system behind tags, attributes, factions, resources and reactions; 25 classes derive from it. Changing it breaks serialized ids |
| Factions | `Core/Units/Runtime/Factions/Faction.cs`, `FactionTracker.cs`, `FactionDefinition.cs`, `FactionRegistry.cs` | Roster, points pools, run upgrades, unlockables |

## Damage and death *(added in setup)*

There is no damage-info type: a hit is a modifier on the target's HP attribute.

1. `AEffectAttributeModifier` calls `target.AttributeSet.ApplyModifiers`.
2. `RuntimeAAttributeBase.ApplyModifier` rolls crit and evade (bus events `onCriticalDamageDoneOnUnit`, `onUnitEvaded`), lets an `IAttributeDecrementHandler` reduce the damage (shields), then sets the value.
3. At the minimum, `RuntimeAAttribute` fires `onMinReached`. It's wired to `GUnit.Die` **in the Inspector, not in code**: `Features/_Common/Prefabs/UnitBase.prefab`, `Unit_GoblinQueen.prefab`, `Lucy_Decoy.prefab`. Renaming `Die` or that event breaks death silently.
4. `GUnit` raises `GlobalEventBus.unitDied`.
5. Separately, `CombatLevelRunHandler.OnAbilityPerformedOn` compares HP snapshots and raises `onUnitDamageDone` (John's and Mark's passives, `BarkManager`, `MissionStatsTracker`, `UnitKillAbilityPointProvider` listen).

## Turn flow and control

| System | Main files | Why it's core |
| --- | --- | --- |
| Level run | `Core/Managers/CombatLevelRunHandler.cs` (incl. its nested `SessionLogs` / `ActionLogEntry`, used in 13 files; partial since 2026-10-20 with `CombatLevelRunHandler.TurnSwitchHolds.cs`: public `RegisterTurnSwitchHold` / `ReleaseTurnSwitchHold` / `HasTurnSwitchHolds` and the public nested `TurnSwitchHoldSet`, a 5 s watchdog; `SwitchTurnIE` waits while any hold is registered, D-102; since 2026-10-22, quick wins bundle P: `SwitchTurnIE` no longer waits for the phase banner (it calls `PlayPhaseAnimation` and starts the turn in the same frame, D-107), and after the gap it waits the next controller's `TurnStartPause` unless the ended turn was ended with the End Turn button, re-checking `_levelEnded` after it (D-143); `EndLevel`'s waits are the fields `endLevelDelayBeforeHudHide`, `endLevelDelayAfterHudHide` and `endLevelDelayBeforeEndPanel`, 0.25 s each, D-144; all pace values: `pace-timings.md`), `LevelRunHandlerBase.cs` | Turn order, ATB fill, win/loss, end of level |
| Combat level *(added in setup)* | `Core/Levels/Runtime/CombatLevel.cs`, `LevelBase.cs` | Singleton for faction relations, the player faction, objectives and the sequence player: 139 `.Instance` calls in 45 files |
| Objectives and relations *(added in setup)* | `Core/Levels/Runtime/LevelObjectives.cs`, `LevelObjectiveConditions.cs`, `LevelFactionRelations.cs` | Win/lose conditions; ally/enemy checks (`FactionsRelationType` in 42 files) |
| Faction controllers | `Core/Interactions/Runtime/FactionControllerBase.cs` (since 2026-10-22, D-143: serialized `turnStartPause` with public `TurnStartPause`, public `TurnEndedByButton`, `EndTurnFromButton()` (the End Turn button's path; marks the turn only when the end request goes out) and the pure static `TurnStartPauseAfter`; the flag is cleared in base `StartTurn`/`EndTurn`. `AIController.RequestEndTurn` doesn't call base, so the dev auto-player never sets the flag (backlog)), `FactionPhaseState.cs`, `PlayerController.cs` (since 2026-10-20, D-105: `TryFindApproachCell` and `ResolveGhostCell` are public, read-only, for previews; since 2026-10-21, D-125/D-128: role QTEs restore the player's in-progress flag instead of clearing it, and the new public `EndTurnAvailable()` keeps End Turn off while another faction acts), `AIController.cs` (since 2026-10-24, D-154, `923ab777b`: `AIController.prefab`'s `skipTurnTagsQuery` matches **any** of Stunned or Unaware, so Unaware enemies skip turns and drop out of `UpcomingTurnOrder`; data only) (since 2026-10-20, D-101/D-106: the per-unit wait also waits on its own action in progress and drops a plan if one started meanwhile) | Per-unit turn FSM, AP spending, player input flow |
| Move preview path *(2026-10-27, D-270, `c7081b76c`)* | `Core/Interactions/Runtime/IMovePreviewPathSource.cs`, implemented by `PlayerController` (`PreviewPath` → read-only `_previewPath`, first cell = mover) | Read by the quiver's "+N arrows" presenter; additive, no behaviour change |
| Player input *(added in setup)* | `Core/Interactions/Runtime/PlayerInputController.cs` | Input singleton: 53 calls in 16 files |
| QTE | `Core/Interactions/Runtime/QuickTimeEventHandler.cs`, `QTEBehavior.cs`, `QTEProfile.cs` | Reaction-timing pillar |

## Grid

| System | Main files | Why it's core |
| --- | --- | --- |
| Grid | `Core/Systems/GridSystem/Runtime/GridCell.cs`, `GridManager.cs`, `GridActions.cs`, `GridPluggableEntity.cs` | Pathfinding, occupancy (thread-sensitive) |

## AI

| System | Main files | Why it's core |
| --- | --- | --- |
| AI | `Core/Systems/AISystem/Runtime/AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIBlackboard.cs`, `AIWorker.cs` | Runs on a worker thread; golden-master tested (`AIRegressionTest`) |

## Infrastructure

| System | Main files | Why it's core |
| --- | --- | --- |
| Event bus | `Core/Managers/GlobalEventBus.cs` | Everything listens to it |
| Game handler *(added in setup)* | `Core/Managers/GameHandler.cs`, `Core/Data/Runtime/GameData.cs` (`GameDataSO`) | Mission start and end, level loading, player faction and first mission: 82 calls in 31 files (`GameDataSO` in 22) |
| Settings | `Core/Managers/GlobalSettingsSO.cs`, `Resources/GlobalSettings.asset` | Resource modes per branch |
| Play-mode reset | `Core/Managers/PlayModeStaticReset.cs` | Domain reload is off |
| Save | `Core/Managers/SaveLoadManager.cs` (+ `ISavable` types) | Save compatibility |
| Missions | `Core/Managers/MissionTracker.cs`, `Core/Levels/Runtime/Mission.cs`, `MissionRouteProgress.cs` | Level graph and progress |
| Entity messages *(added in setup)* | `Core/Utilities/GameEntityMessage.cs` | String-based calls used by `AEffectBase` feasibility checks and function callers; the AI-thread-safe replacement for `SendMessage` |
| Delayed execution *(added in setup)* | `Core/Utilities/ExecutionUtils.cs` | Delay and coroutine runner used by `Die` and 13 files |
| Camera *(added in setup)* | `Core/Camera/Runtime/CameraHandler.cs` | 46 calls in 18 files (14 in `PlayerController`). Has a BOM |
| Combat UI manager *(added in setup)* | `Core/UI/Runtime/CombatLevelUIManager.cs` (since 2026-10-21, D-128: `NotifyStateChange` uses `PlayerController.EndTurnAvailable()` for the player's End Turn button; since 2026-10-22, quick wins bundle P: public `PlayPhaseAnimation(Faction)` starts the banner and sets the End Turn panel without waiting, and on the player's turn holds the existing input lock with a fresh owner per banner until the banner finishes, is hidden or is replaced (D-142); `ShowPhaseAnimation` is a waiting wrapper with no callers; `HideHUD` hides the banner at once; the End Turn panel calls `EndTurnFromButton`), `LevelUIManagerBase.cs` | ATB gauge views and unit panels: 37 calls in 12 files (19 in `PlayerController`) |

**Checked, not core:** `Core/Systems/CombatLogging/` (`CombatLog` partials, `CombatLogBook`, `CombatLogEntry`, `CombatLogFileSink`, `CombatLogFormat`) only listens: it subscribes to 16 bus events and is called from three places (`MissionTracker` owns it, `CombatLevelRunHandler` calls `HookLevelEvents()`, `AudioSettingsPanel` calls `CombatLogFileSink.DeleteAll()`). Nothing in combat depends on it. Renaming or removing a bus event it listens to breaks it, so check it when the bus changes. Design notes: `tech/combat-log.md`.

**Removed by THJ on 2026-10-16 (D-032):** the AI regression test (a test, not a system; its rule is in `CLAUDE.md` and the gates), run upgrades (feature-level; they reach combat through `FactionTracker.PrepareLevel`, covered by Factions) and the Home simulation (a branch feature; the Home is already Tier 3 in `escalation.md`). Changes to them follow the normal tiers.
