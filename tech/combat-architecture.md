# Combat architecture

Owner: coordinator. The short map of the combat code; moved here from `CLAUDE.md` on 2026-10-15. Details in `mechanics-brief.md` (2026-10-03). Systems whose API or behavior needs THJ's OK to change: `core-systems.md`.

- **Subsystems** under `Core/Systems/`: `AbilitySystem` (Abilities, Attributes, Effects, Points), `AISystem`, `GridSystem`, `StatsResourcesSystem`, `RunUpgrades`, `TagSystem`, `CombatLogging`. Level and mission flow in `Core/Managers` and `Core/Levels`; units in `Core/Units` (`GUnit`, both sides); player and enemy content in `Features/{Player,Enemy}`.
- **Turn flow:** `CombatLevelRunHandler` (Core/Managers) runs one `FactionControllerBase` per faction (Core/Interactions). Each controller is a per-unit function-object FSM: `UnitSelection -> ActionSelection -> TargetSelection -> TakeAction`. `PlayerController` and `AIController` drive the same FSM.
- **Turn switch** (`CombatLevelRunHandler.SwitchTurnIE`, as of 2026-10-22, quick wins bundle P): wait while any controller acts, a sequence plays, a level behaviour runs or a turn-switch hold is set → read the ended controller's `TurnEndedByButton` → `EndTick`, `EndTurn` → gap (`timeBetweenFactionTurns`) → pick the next faction that can play → turn-start pause (the next controller's `TurnStartPause`, skipped after the End Turn button) → `PlayPhaseAnimation` and `StartTurn` in the same frame. The banner (`PhaseVisualsUI`) never blocks the turn; on the player's turn the input lock is held until it ends, and the ability bar and End Turn button check that lock themselves (they bypass the input modes). Every wait with its value and location: `pace-timings.md`.
- **End of a level** (`CombatLevelRunHandler.EndLevel`): wait → `HideHUD` (also hides the banner at once) → wait → the level's outro sequence → rewards and `levelEnded` → wait → the win / defeat / mission-complete panel. The three waits are Inspector fields on the level run handler (`GameSessionHandler` object in `CombatLevelContainerScene`).
- **AI** is utility-based (blackboard, strategy planner, per-ability score graphs) and runs on a background thread (`AIWorker`). Code the AI reads (`GridCell`, `GUnit`, stat code) must not use Unity's overloaded `==` or main-thread-only APIs; use `ReferenceEquals` plus `IsAlive`, and `GameEntityMessage` instead of `SendMessage`. `GridCell` occupancy depends on `IsAlive`, so any despawn path must clear `IsAlive` or the cell slot. Changing a utility graph, AI ability or unit also changes `AIRegressionTest`'s baked catalogs (already red).
- **Abilities:** `AbilityPreset` is authored data, `RuntimeAbility` the live instance, `AbilityOrchestrator` the per-unit container. Effects are `AEffect*` classes (`AEffectCompound` composes sub-effects). Duos are data entries plus hardcoded per-duo hooks in `UnitsCooperationHandler`, so a new duo needs code.
- **Points:** AP goes through `APConsumer` (`PerUnit` or `Shared` from `GlobalSettings`). Faction-role and duo spending goes through `PointConsumer` (FTP or ATB per `pointConsumptionMode`; which one depends on the branch, see `branches.md`). The Reactive Interrupt (key L) works only in ATB mode (`PlayerController.HandleReactiveInterrupt` returns at once on FTP).
- **Stats:** raw `AAttribute` pools (fixed modifier order) plus evaluated `StatAttributeSet` factors. Source order: Ability, Unit, Equipment, Faction, SkillTree (plus `Home` when present), in `StatEvaluation.cs`.
- **Run upgrades:** one mission is one run. `RunUpgradeTracker` (on `FactionTracker`) is in memory only (as are `MissionTracker.GraphSeed` and `CompletedLevelNames`) and re-applies grants to recreated units each level via `PrepareLevel`.
- **Missions** are level graphs (`SerializableDependencyGraph`, seeded by `MissionTracker.GraphSeed`); the in-mission picker is `MissionMapUI`, the world-map picker is separate.
- **Naming:** the unit Dom was renamed Toba, but its folder is still `Features/Player/Dom/`. Static save trackers (`EnemyIntroductionTracker`, `AbilityIntroductionTracker`, `PlayedSequencesTracker`, `BarkPlayedTracker`) are static `ISavable` singletons that call `SaveLoadManager.Register` before every access.

## Dev cheats in combat

`Core/_Dev_/Runtime/CheatHandler.cs` (checked 2026-10-21, `main` @ `df58c4c0c`). On when `GlobalSettingsSO.cheatsEnabled` is set, or at runtime by holding **C+H+T** together. "Hovered" means the unit on the grid cell under the cursor; no unit there, no effect. Every use is logged (`tech/combat-log.md` §4.5).

| Key | Effect |
| --- | --- |
| **K** | Kills the hovered unit, **allies included**. With **N** held: every living unit of the hovered unit's faction |
| **F11** | Kills every living unit of the hovered unit's faction (same as N+K). Hovering a family member wipes the family |
| **H** | Heals the hovered unit (N: its whole faction) |
| **`[`** | −1 HP on the hovered unit, **Shift** −10 (N: its whole faction) |
| **`]`** | +1 AP on the hovered unit; **Shift** fills AP to the cap and resets all its cooldowns (N: its whole faction) |
| **L** | +99 FTP, given through the hovered unit (N: its faction) |
| **J** | +1 ATB to every player unit (no hover needed; moot on FTP) |
| **F12** or **Numpad 6** | Completes the current objective as a success (`BypassCurrentObjectiveAsSuccess`) |
| **Numpad + / −** | Game speed ±0.1 (`Time.timeScale`, clamped 0–5, bypasses `TimeScaleCache`) |
| **Numpad 0** | Game speed back to ×1 |

A unit killed by K or F11 is restored when the level ends; it does not change the save.

## Enemy alert state (2026-10-24)

- Code: `Core/Systems/EnemyAlertSystem/` (`EnemyAlertRules` pure rules; `EnemyAlertTracker` + `.Events`, `.Visuals` partials; `EnemyAlertSettings` per unit: `startsAlert`, `alwaysAlert`; `LevelAlertSettings` per level root: `allEnemiesStartAlert`, `sightBonus`, `alertRangeBonus`).
- The tracker sits on `LevelBase.prefab` (the `GlobalEventBus` object), main thread only, no statics. It tags player-hostile units `Status.Unaware` at level start and on `unitBorn`; the AI skips them through `AIController.prefab`'s `skipTurnTagsQuery` (no AI code). Wakes: stop events + a full sight check after each action and at enemy turn start; noise from `onAbilityEffectPerformedOn` (units named directly; cells only from family-side casters; never the ability that spawned the unit), HP/tag/evade watches; recursive spread. A unit woken in its own faction's turn has its AP closed. `UnitAlerted(GUnit, depth, showPop)` drives the "!" pop and the Shift-hover redraw.
- Ranges: unit attributes `Specs_Sight` (default 3, Masher 2) and `Specs_AlertRange` (2) in `AAttributes.asset`, read at check time, plus the level bonus, clamped at 0.
- No "Unaware" gain pop: the tracker disables the unit for the moment it adds the tag (`ShowTagGained` skips inactive units), guarded by a test that `GUnit` and its bases have no `OnEnable`/`OnDisable` (D-162).
- Preview: `ShowStatsHoverPreview.cs` draws sight (enemy-move frame) and alert (enemy-attack icon) tiles while Unaware; redraws on wake.

## Grid previews (2026-10-20, `thj/preview-improvements`)

Design and inventory of all 23 previews: `plans/2026-10-19-preview-pass-design.md`. Tech plan and commit hashes: `plans/2026-10-19-preview-pass-tech.md`.

- **Attack reach from a tile:** one helper, `UnitThreatAnalysis.AttackReachFrom` / `BasicAttackReachFrom` (`Core/Interactions/Runtime`). It is used by the ghost sword icons, the approach preview, Shift, the enemy threat arcs and the role-zone equality checks. Any new attack-geometry flag must go through it.
- **Hover gate:** `GridManager.HoverGate.cs` stops grid hover over screen-space HUD canvases. World-space panels don't block.
- **Role-zone layer:** `GridCell.RoleZone.cs` holds one entry per owner (sprite, quadrant, colour, scale). It is fed by `RoleZonePresenter` (selected unit, Shift, badge hover via `GlobalEventBus.onFamilyRoleBadgeHover`, focus, the D-080 hide) and by `MovePreviewCoverPresenter` (follow zones from the ghost tile for all four Bergsons, and the cover markers). The two presenters sit on one GameObject added by `ShowStatsHoverPreview`. All four role handlers have `GetCellsInRange(GridCell origin)`.
- **Shift preview layer:** `GridCell.ShiftPreview.cs`, with Bergson and enemy kinds. `ShiftPreviewRules` decides by relation: a unit hostile to the player gets the danger zone; any other unit gets current-tile reach.
- **Arcs:** `Core/Utilities/ArcLine.cs` (a quadratic Bézier) draws John's tether. `GUnit.ShowThreatLineTo` still has its own copy (switching it is a later core commit).

## Level start run upgrade grant (2026-11-01, `thj/onboarding`)

`Features/Onboarding/LevelStartRunUpgradeGrant` (non-core MonoBehaviour on a level): a list of `RunUpgradeSO`; subscribes itself to the level's `GlobalEventBus.levelStarted` (caches that bus) and grants each through the player faction's `RunUpgrades.TryGrant`. Mission lifetime: `FactionTracker.EnterMission`/`QuitMission` clear it; a restart is refused by `Has`. Warns when fewer were granted than listed (no mission, unit not in squad). Used on memory segment 4 for Tempest Bloom (C3). Commit `c772bbf34`.
