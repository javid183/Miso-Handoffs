# Combat architecture

Owner: coordinator. The short map of the combat code; moved here from `CLAUDE.md` on 2026-10-15. Details in `mechanics-brief.md` (2026-10-03). Systems whose API or behavior needs THJ's OK to change: `core-systems.md`.

- **Subsystems** under `Core/Systems/`: `AbilitySystem` (Abilities, Attributes, Effects, Points), `AISystem`, `GridSystem`, `StatsResourcesSystem`, `RunUpgrades`, `TagSystem`, `CombatLogging`. Level and mission flow in `Core/Managers` and `Core/Levels`; units in `Core/Units` (`GUnit`, both sides); player and enemy content in `Features/{Player,Enemy}`.
- **Turn flow:** `CombatLevelRunHandler` (Core/Managers) runs one `FactionControllerBase` per faction (Core/Interactions). Each controller is a per-unit function-object FSM: `UnitSelection -> ActionSelection -> TargetSelection -> TakeAction`. `PlayerController` and `AIController` drive the same FSM.
- **AI** is utility-based (blackboard, strategy planner, per-ability score graphs) and runs on a background thread (`AIWorker`). Code the AI reads (`GridCell`, `GUnit`, stat code) must not use Unity's overloaded `==` or main-thread-only APIs; use `ReferenceEquals` plus `IsAlive`, and `GameEntityMessage` instead of `SendMessage`. `GridCell` occupancy depends on `IsAlive`, so any despawn path must clear `IsAlive` or the cell slot. Changing a utility graph, AI ability or unit also changes `AIRegressionTest`'s baked catalogs (already red).
- **Abilities:** `AbilityPreset` is authored data, `RuntimeAbility` the live instance, `AbilityOrchestrator` the per-unit container. Effects are `AEffect*` classes (`AEffectCompound` composes sub-effects). Duos are data entries plus hardcoded per-duo hooks in `UnitsCooperationHandler`, so a new duo needs code.
- **Points:** AP goes through `APConsumer` (`PerUnit` or `Shared` from `GlobalSettings`). Faction-role and duo spending goes through `PointConsumer` (FTP or ATB per `pointConsumptionMode`; which one depends on the branch, see `branches.md`). The Reactive Interrupt (key L) works only in ATB mode.
- **Stats:** raw `AAttribute` pools (fixed modifier order) plus evaluated `StatAttributeSet` factors. Source order: Ability, Unit, Equipment, Faction, SkillTree (plus `Home` when present), in `StatEvaluation.cs`.
- **Run upgrades:** one mission is one run. `RunUpgradeTracker` (on `FactionTracker`) is in memory only (as are `MissionTracker.GraphSeed` and `CompletedLevelNames`) and re-applies grants to recreated units each level via `PrepareLevel`.
- **Missions** are level graphs (`SerializableDependencyGraph`, seeded by `MissionTracker.GraphSeed`); the in-mission picker is `MissionMapUI`, the world-map picker is separate.
- **Naming:** the unit Dom was renamed Toba, but its folder is still `Features/Player/Dom/`. Static save trackers (`EnemyIntroductionTracker`, `AbilityIntroductionTracker`, `PlayedSequencesTracker`, `BarkPlayedTracker`) are static `ISavable` singletons that call `SaveLoadManager.Register` before every access.

## Dev cheats in combat

`Core/_Dev_/Runtime/CheatHandler.cs`: K kills the hovered unit, F11 on a hovered enemy kills its whole faction, F12 completes the objective, H heal, J ATB, L +99 family points, `[` −1 HP (Shift −10), `]` +1 AP.
