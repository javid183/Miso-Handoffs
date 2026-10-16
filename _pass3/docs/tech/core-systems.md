# Core systems

Owner: coordinator; THJ approves additions and removals. Paths are under `miso/Assets/_Project/`.

**Why this list matters:** changing the public API or behavior of anything here is **Tier 3** (ask THJ first). Any bugfix inside one is **Tier 2** (flagged in the report). The reviewer checks every change against this list.

**Status: seed list**, built on 2026-10-15 from `tech/mechanics-brief.md` (code read of 2026-10-03). The setup session verifies each entry against the code and adds what combat relies on that's missing. Entries marked *(verify)* weren't confirmed in code yet. **[THJ] prune.**

## Abilities and effects

| System | Main files | Why it's core |
| --- | --- | --- |
| Ability data and runtime | `Core/Systems/AbilitySystem/Abilities/Runtime/AbilityPreset.cs`, `RuntimeAbility.cs`, `AbilityOrchestrator.cs` | Every unit action goes through them |
| Effects | `Core/Systems/AbilitySystem/Effects/Runtime/AEffectBase.cs`, `AEffectCompound.cs` (and the `AEffect*` family) | Every ability's result; compounds carry shapes, unlocks and sub-effects |
| Duos (cooperation) | `Abilities/Runtime/UnitsCooperationHandler.cs`, `AEffectCoOpTrigger.cs` | USP: Duos |
| Pass-by | `Abilities/Runtime/UnitsPassByHandler.cs` | Tag mechanic; fills FTP/ATB; Synergies |
| Family Roles | `Abilities/Runtime/FactionRoleHandlerBase.cs`, `Features/Player/*/Scripts/*FactionRoleHandler.cs` | USP: Family Roles |
| Damage preview | `Abilities/Runtime/AbilityDamagePreview.cs` | Must match the real hit (rounding, lethal checks) |

## Points

| System | Main files | Why it's core |
| --- | --- | --- |
| AP | `Core/Systems/AbilitySystem/Points/Runtime/APConsumer.cs`, `ActionPoints.cs`, `FamilyActionPoints.cs` | Every AP spend and gain; PerUnit vs Shared |
| FTP / ATB | `Points/Runtime/FamilyTimePoints.cs`, `ATBGauge.cs`, `PointConsumer.cs` | Family resource; differs by branch |

## Units, stats and factions

| System | Main files | Why it's core |
| --- | --- | --- |
| Units | `Core/Units/Runtime/GUnit.cs` | The one unit class for both sides |
| Attributes | `Core/Systems/AbilitySystem/Attributes/Runtime/AAttribute*.cs`, `RuntimeAAttribute*.cs`, `AAttributeModifier.cs` | HP and pools; modifier order |
| Stat evaluation | `Core/Systems/StatsResourcesSystem/Runtime/StatAttributes/StatEvaluation.cs`, `StatAttributeSet.cs`, `StatBackedValue.cs` | Source order Ability → Unit → Equipment → Faction → SkillTree (+ Home layer) |
| Factions | `Core/Units/Runtime/Factions/Faction.cs`, `FactionTracker.cs`, `FactionDefinition.cs`, `FactionRegistry.cs` | Roster, points pools, run upgrades, unlockables |

## Turn flow and control

| System | Main files | Why it's core |
| --- | --- | --- |
| Level run | `Core/Managers/CombatLevelRunHandler.cs`, `LevelRunHandlerBase.cs` | Turn order, ATB fill, win/loss, end of level |
| Faction controllers | `Core/Interactions/Runtime/FactionControllerBase.cs`, `FactionPhaseState.cs`, `PlayerController.cs`, `AIController.cs` | Per-unit turn FSM, AP spending, player input flow |
| QTE | `Core/Interactions/Runtime/QuickTimeEventHandler.cs`, `QTEBehavior.cs`, `QTEProfile.cs` | Reaction-timing pillar |

## Grid

| System | Main files | Why it's core |
| --- | --- | --- |
| Grid | `Core/Systems/GridSystem/Runtime/GridCell.cs`, `GridManager.cs`, `GridActions.cs`, `GridPluggableEntity.cs` | Pathfinding, occupancy (thread-sensitive) |

## AI

| System | Main files | Why it's core |
| --- | --- | --- |
| AI | `Core/Systems/AISystem/Runtime/AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIBlackboard.cs`, `AIWorker.cs` | Runs on a worker thread; golden-master tested |
| AI regression test | `Core/Systems/AISystem/Editor/AIRegressionTest.cs` | Baked catalogs; known red until its fix |

## Infrastructure

| System | Main files | Why it's core |
| --- | --- | --- |
| Event bus | `Core/Managers/GlobalEventBus.cs` | Everything listens to it |
| Settings | `Core/Managers/GlobalSettingsSO.cs`, `Resources/GlobalSettings.asset` | Resource modes per branch |
| Play-mode reset | `Core/Managers/PlayModeStaticReset.cs` | Domain reload is off |
| Save | `Core/Managers/SaveLoadManager.cs` (+ `ISavable` types) | Save compatibility |
| Missions | `Core/Managers/MissionTracker.cs`, `Core/Levels/Runtime/Mission.cs`, `MissionRouteProgress.cs` | Level graph and progress |
| Run upgrades | `Core/Systems/RunUpgrades/Runtime/RunUpgradeTracker.cs`, `RunUpgradeSO.cs` | In-mission upgrades applied each level *(verify core status)* |

## Home (scope `thj/home-test`)

| System | Main files | Why it's core |
| --- | --- | --- |
| Home simulation | `Core/Systems/HomeSystem/Runtime/` (`HomeSimulation`, `HomeDayRunner`) *(verify)* | USP: Managing the Home; feeds combat through the Home stat layer |
