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

## Hidden level units and reveal (2026-11-01, `thj/onboarding`)

`Features/Onboarding/HiddenLevelUnits` (non-core MonoBehaviour on the level root, written by the grid tool's `level hidden` line): named groups of placed units whose GameObjects are inactive in the prefab, so every level-start collector skips them (turn order, AI, objectives, `GridCell` occupancy, alert, roles). `Reveal(group)` repeats `GUnit.SpawnAt`'s steps on the existing object: `SetActive(true)`, `Initialize(true)`, `PlugEntity`, `AddFactionControllerMidWay`, `RegisterUnit` (raises `unitBorn`, so AI and alert pick it up). An instance `_revealed` set stops a second reveal reviving a dead unit (`GUnit.Die` deactivates it); no free cell or no faction → warn, deactivate, skip. No statics. `RevealUnitsSequence` is the level-sequence action that calls it. Note: "defeat every enemy" counts only units in play, so a level with hidden enemies needs its own win stages. Commit `3c99b3ee6` (D-346).

## Tutorial level helpers (2026-11-01, `thj/onboarding`)

Both non-core MonoBehaviours on a level root, no statics, subscribe in `OnEnable`/`OnDisable`.

- `Features/Onboarding/GuidedAbilityHint`: pulses the HUD button of one `AbilityPreset` (scale only) while it shows; ends on that ability's `abilityPerformed`, after the hinted turn (`TurnNumber` counts rounds) or on `levelEnded`; always restores the button's scale. Re-finds the button on `unitSelectionChanged` (1 s fallback poll). Commit `ba7d19e66`.
- `Features/Onboarding/TurnStartActionPointLimit`: on the player faction's turn N `turnStarted` (after `PhaseData.Reinitialize`'s refill) spends listed units down to a set AP through `APConsumer.Consume` (the engine's own drain path, no ability events). Family Roles aren't AP-gated, so 0-AP units still react. Skips unless per-unit AP and FTP mode. Not re-applied by `RestartTurn` (no `turnStarted`). Auto-select at turn start lands after it only because `EnemyIntroductionController` delays a frame. Commit `8a443d66c`.

## Synergy aim previews (2026-11-11, `thj/after-hearth`, scope all)

- `Features/Player/Shared/Synergies/SynergyLanePresenter` (partials `.Bloom`, `.Catch`): non-core, one object in `CombatLevelContainerScene` placed by `Tools/Synergies/Place Synergy Lane Presenter`. Polls the aim each `LateUpdate`; gives back everything it drew on the grid's hovered==false pass (order-independent of `PlayerController`'s hover listeners); clears on null/other ability, `IsLevelEnded`, `OnDisable`.
- Flare: ghost projectiles (pooled SpriteRenderers, real projectile sprite/material, on the relayer's body layer at order + offset). WorldUI is not lit by the scene's 2D light, so lit sprites go black there.
- Bloom: dims Linda's range tiles (`GridCell.SetHighlight`) except Linda → Cyclone, lights copy lanes, one `SetAimDirectionPreview` chevron per copy lane (a cell holds one chevron; no multi-chevron API), HP via `GUnit.ShowDamagePreview` with a copy of `AbilityDamagePreview.AddDamage` math.
- Catch: one chevron on Mark's tile toward Linda; return damage via `ShowDamagePreview(total, confirmed, FinalPick)` (the Fire Embers two-colour bar). With both, Bloom skips the return's units so each bar is drawn once per frame (re-showing with a different pick restarts `ImageAlphaPulse`).
- Catch offer (2026-11-17): the catch prompt is offered only if the return copy would hit an enemy. One pure rule `CatchOfferRules.ShouldOffer` and one hit counter `CatchReturnHits.CountReturnEnemyHits` (`IsHostileTarget`: alive, Enemy relation, in the effect's target relations; fail-open when the return can't be predicted) serve both `ProjectileCatchAndReturn.TryCatch` (before `FreezeArrow`; a declined arrow isn't frozen or re-asked) and the preview (`SynergyLanePresenter.Catch`, decision cached per aim, cleared in `ClearCatch`). When not offered: no chevron, no pink bars. When offered: only the units the return hits get the pink bars (the shot's own red part under the return on top); the forward hits past Mark keep the shot's normal preview untouched (D-556; the grey lost-hit tint of 2026-11-17 was built and removed the next day).
- Shared geometry with the real shots: `ShieldFlareGeometry` (John), `TempestBloomGeometry` (Lucy; 'back' read on the grid, shooter cell → Cyclone: 3 copies), `CatchAndReturnRules` (Mark).
- Known gaps: Lucy's two-pick attack shows ghosts only for the hovered pick (needs a read-only picks getter on `FactionControllerBase`, core); previews assume nothing blocks the shot before John/Cyclone/Mark; core bow preview counts falloff on every entity it passes (real arrow: targets only).

## Lucy's Cyclone, Pulling Gale (2026-11-12, `thj/cyclone`, scope all; uncommitted until THJ's play check)

Plan `plans/2026-11-11-cyclone-redesign-tech.md`; reports `reports/cyclone-c1a.md` to `cyclone-c4.md` (+ reviews); core additions listed in `core-systems.md` (note 2026-11-12).
- Code in `Features/Player/Lucy/Scripts/Cyclone/`: `CycloneEntity : OnGridEntity` (partials `.Whirl`, `.Steer`, `.Ready`, `.AIDanger`, `.LineOfFire`; stationary, 3 pips lost on the family turn start only, `isTargetable` off, `passRelation` Ally), `CycloneRegistry` (static, locked, reset hook; one live Cyclone per caster), `CycloneRules` (cast/steer cell rules, worker-safe), `CycloneWhirlPlanner` + `ICycloneWhirlSteps` (pull plan, unscaled-seconds caps, testable clock), `AEffectCycloneSpawner` (cast), `AEffectCycloneSteer` (Steer, `ITargetSelectionRangeProvider`), views for the cross and pips.
- Whirl: on cast and on each enemy faction's `TurnEnding` (hold): pull (via `AEffectPusher.TryMoveTo`, raises `unitEndMoving`, hazards fire) → wait for reactions (Watch blocks via `PhaseData.IsInProgress`) → 3× hit under `CycloneHitContext`, reported by `ReportDamageOutsideAbility`. Dispose waits for the Whirl and pending pulls. Nothing after level end.
- Steer = a second ability `Lucy_Ability_Steer` (cooldown 1) swapped into the Cyclone button's slot by `AbilitiesBarHUDUI.CycloneSteer.cs` while her Cyclone is out; Gust = pull only. AI-controlled Lucy refuses Steer (D-540).
- Setup tools (re-runnable, set values only on create/swap): `Tools/Lucy/Apply Anchored Cyclone Setup`, `Tools/Lucy/Apply Cyclone Steer Setup`.
- Known: AI regression inner count 43 (new Steer preset in the catalog scan; fix session). Dead Linda-folder Cyclone copies untouched.
