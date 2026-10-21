# Miso — Current Codebase Mechanics Brief

*Compiled from a direct read of the C# source in the repo at `E:\Work\Projects\miso`. The Unity project is one level down at `miso\` and all game code is under `miso\Assets\_Project\`. Last updated 2026-10-03 (branch `thj/home-test`, `HEAD` `59a4f5cde`; §0 covers 04ed2b5f → `59a4f5cde`, and §1–12 are the 2026-09-28 baseline with in-place corrections). This version comes from diffing the 2026-09-07 brief's baseline (`93e42824`) against `HEAD` (`04ed2b5f`, "feat: shop upgrades added"). That covers 245 commits, roughly 184 changed files under `Core/` (+12.4k/−1.2k lines), plus `Features/`. Every section was re-verified against current file contents. Where the 09-07 brief was wrong, not just stale, the text says so.*

## 0. Changes Since 04ed2b5f (2026-09-28 → `59a4f5cde`, 2026-10-03)

*139 commits (129 non-merge) on branch `thj/home-test`, including the merge of `origin/main` (`0ba4bc80d`) into it. Compiled from `git diff` plus current file contents; nothing was run in Unity. The Home System work (`Core/Systems/HomeSystem/`, ~23k lines) is documented in `tech/home-system.md` and `build-log.md`, not here. Sections 1–12 below are the 09-28 baseline; stale statements in them were corrected in place and marked **(updated 10-03)**.*

**Settings and branch differences**

- `GlobalSettings.asset` on this branch has `pointConsumptionMode: 0` (**FTP**), because the Home demo writes effects against FTP. `origin/main` has `1` (ATB). Enums are `PointConsumptionMode { FTP = 0, ATB = 1 }` and `APConsumptionMode { Shared = 0, PerUnit = 1 }`. `aPConsumptionMode` is `1` (PerUnit) on both branches, with escalation `[1,1,2,4]`.
- New settings: `tauntTag`, `homeCycle` (`HomeCycleDefinition`), `homeStateMissionMode` (`FurthestCompleted` default / `MostRecentlyCompleted`, not serialized in the asset), `cheatsEnabled` (1), `showFPGainVFXOnUnits` (0; only shown in the inspector in FTP mode). `enableCustomCursor` is still 0.
- `miso/Assets/MortaStory/` (from main, Morta rebuild export, ~120 runtime scripts, ~570 MB of art): story actors, idles and cutscene tracks, in three assemblies (`Morta.Story`, `Morta.Legacy.Stubs`, `Morta.Story.Editor`). It plays home idles and cutscenes. It has its own `README.md`.
- **Name collision:** there are two `HomeState` types. `MISO.Core.Home.HomeState` (a ScriptableObject of idle lists) and the Home System's `HomeSystem/Runtime/State/HomeState.cs` (simulation state).
- `TimeOfDayTracker` is `[Obsolete]`, replaced by the Home calendar. `GameHandler` no longer exposes it.

**Cooperation (duo) system, rewritten** (`UnitsCooperationHandler`, now 1508 lines)

- Data-driven entries plus hardcoded per-duo logic. Each `CooperationEntry` has `iD`, `triggerPreset`, `partners[]`, `allConsumeAP`, `cooldownForAll`, `executeInParallel`, `fPCost`. Each `CooperationPartner` has `ability`, `ExtraAttribute`, `qteFactor` (renamed from `mashedFactor`, with `FormerlySerializedAs`), `qteProfile`, `qteModifier` and min/max factor.
- **Seven duos** are registered, with init and target-adjust hooks keyed by id string in `Initialize()`: `John_Lucy_Duo`, `Linda_Lucy_Duo`, `Linda_Toba_Duo` (new, shares the "ranged enchant" init and adjuster with Linda-Lucy), `John_Linda_Duo`, `Mark_Lucy_Duo`, `Mark_Linda_Duo`, `Mark_John_Duo`. Adding a duo still needs code.
- Flow: `abilitySelectEnteredTargetSelection` → `HandleTriggerInits` (preview setup) → `Execute(...)` → target adjuster → `ExecuteIE`. The adjuster's return value is ignored by `Execute`. `ExecuteIE` shows the duo visual, focuses the camera, applies the previewed path via `MovePathOverride`, and spends AP through `APConsumer` (all partners if `allConsumeAP`, otherwise the activator) and FP through `PointConsumer`.
- `SquadAllowsTrigger(preset)` hides a duo when a partner isn't in the squad. `RuntimeAbility.Available` now ANDs it in (`IsCooperationAllowedBySquad()`).
- QTEs are per partner. A mash-type result maps to the min/max factor, and other types give 1 or 0. The factor is applied as a temporary `CoopQteMod` modifier. `onSuccessfulQTE` fires only on success. John-Lucy has an extra-decoy QTE. John-Mark has a time-window QTE that adds one extra turn of vulnerability (configured in data). Mark-Linda's QTE was removed.
- Per duo:
  - **John-Lucy:** decoys are previewed as ghost entities, and John's absence is handled.
  - **Linda-Lucy / Linda-Toba:** aim-direction preview plus a damage preview, and the trigger ability's damage factor is copied onto Linda's ability.
  - **John-Linda:** mirrored movement. A held toggle flips the mirror direction, and `OnCycleMovePath` cycles alternative paths.
  - **Mark-Lucy (Fist Blitz):** multi-target. Mark's sprite is hidden while a ghost teleports to each target, nearest first. The `try/finally` is commented out, so an aborted coroutine leaves Mark invisible.
  - **Mark-Linda (race):** the range is the intersection of both walk areas. The winner is picked by path cost, then length, then Mark on a tie. The loser stops one cell short. Rewards apply afterwards: both basic-attack cooldowns reset, the loser gets +1 AP, the winner gets +1 ATB and a one-turn damage bonus consumed on their next basic attack.
  - **Mark-John (shout):** targets every enemy in the union of both radii (default 3).
- `AbilityDamagePreview.AccumulateFromCoOp` sums the partners' previews for `AEffectCoOpTrigger`.

**Movement, paths and previews**

- **Alternative move paths.** `GridCell.FindAlternativePathsTo(...)` (in `GridActions.cs`) returns up to 8 simple paths within budget, adds routes via pass-by waypoints, and sorts by cost, with waypoint-hitting paths first on ties. The default is the shortest path, and among equals the tag-triggering one. Players cycle paths with the new `CycleMovePath` input (`PlayerInputController.OnCycleMovePath`, `Interact` mode only). The chosen path is committed through the new static `MovePathOverride` and consumed by `AEffectTransporter` only if it ends at the destination.
- `AbilityPreset.autoMoveAllowed` (basic attacks only) gates auto move-attack in four `PlayerController` places. **It defaults to false**, so any basic-attack preset not set in data loses auto-move. This was not checked against the assets.
- `AbilityPreset.ghostSource` (`AbilityOwner` / `FirstSelectedUnit`, used by Mark's command) and `affectedAreaPreviewSprite` (custom range icon, e.g. Toba's wall; `GridCell.SetInAttackRange(bool, Sprite)`).
- `AbilityTransporterPreview` (new) holds a simulated occupancy map and the shared transporter walk. Push and damage previews both use it (SEN-3154).
- Silent abilities: `ActivateAbility(..., suppressAnimation, silentActivation)`. Pass-by abilities now use both. A silent activation doesn't set `_currentlyActiveAbility` (SEN-3580).
- `GridPluggableEntity.NotifyIncomingDirection` is called by ability apply and by `Projectile` on arrival. It sets `IncomingDirection`. I found no consumer of it.
- `MathUtils` direction tie-break changed from `>` to `>=`.

**Statuses, taunt and turn ticks**

- `GTagSet.OnTagGained` makes `GUnit.ShowTagGained` float the tag name over the unit (SEN-3587). `GetTagLifeTurns` returns -1 for persistent tags, and the status panel then shows no countdown. `TagTooltipManagerUI` shares one tooltip per tag across panels, shown after `waitTimeForTooltip` (1s).
- New tags in `GTagSet.asset`: Vulnerable, Weak, Burnt, Taunted, Sheltered, **Reckless**. The Unmovable tag's display name is now **Immovable**; I did not check whether the internal name changed. Goblin Masher is Immovable, Mark's command refuses Immovable targets, and "Goblin Queen" was renamed "Goblin Shaman".
- **Taunt:** `GUnit.TauntByAbility` remembers the attack and adds the taunt tag as persistent. `MemorableAttackMemoryShare` calls it. A taunted unit's future targets show its memorised attackers (mood 2, red) in `FutureTargetsPanelUI`. `RememberAttack` now calls `MemorableAttacksMemory.Clear()` first, marked `// todo: temp`, so only the latest attack is remembered. AI drops actions scoring ≤ `CANCEL_ACTION_UTILITY_SCORE_THRESHOLD` (−100).
- New `IHandleEndPhaseTick.EndPhaseTick()`: `CombatLevelRunHandler.EndTick()` calls it on the current faction controller right before `EndTurn()`. The attack-memory tick moved here from `PhaseTick`.
- Stat-modifier duration fields are now `StatBackedValue durationTurnsSb` on `AEffectDurationAttributeModifier` and `AEffectStatAttributeModifier`. 14 assets were migrated, and an unmigrated asset would lose its duration.
- `GUnit.BindToSpawner` makes a spawnee die with its spawner (Lucy's decoy, SEN-3159). `IsUnitIgnoredForObjectives` hides tagged units from objectives, and `BarkManager.ignoredSpeakerTagsQuery` does the same for barks.
- Hit feedback: `GUnit` has blink, `hitFXEntity`, `hitEffects` and a slow-mo curve. `TimeScaleCache` is a lease-counted `Time.timeScale` cache (the speed cheats bypass it).
- Projectiles: `Projectile` gets trails (enabled after `trailActivationDelay`, 0.15s) and `DirectionNormal`. **Behavior change:** the effect faction match is now `TargetFactionRelation.HasFlag(relation)`, so a multi-flag relation matches all its flags.

**Points / AP / FP**

- All AP consumption and production now goes through `APConsumer` (`Produce`, `ResetSharedPool`, `FillToCap` added). `ActionPoints` gets `Produce`, and `EnsureMaxFits` rewrites an overflowing max to a Constant. `UnitKillAbilityPointProvider` (Linda) now calls `APConsumer.Produce` instead of applying a modifier. The shared-AP reset moved into `FactionPhaseState`. `ActionPoints.RestoreAuthoredMax` is dead code.
- FP gain VFX plays on the unit if `showFPGainVFXOnUnits` is set, otherwise on the HUD (`FTPIndicator.PlayFTPGainVFX`). `ftpGainVFX` isn't null-checked and nothing deactivates it.
- `FamilyTimePoints.AddMaxBonus(int)` raises the FP max (used by the Home send-off meal).
- `StatEvaluation` has a new `Home` source id. `StatAttributeHomeLayer` appends it to the source order only when the context really holds a Home source, so enemies don't inherit it.

**New player-side mechanics** (`Features/Player/`)

- `JohnPassiveAbility_CommandShieldDash`: after a unit finishes a Command move, a QTE on John can trigger a free Shield Dash. The dash path is previewed during Command targeting.
- `LucyPassiveAbility_PapasShelter`: Lucy adjacent to John gets the Sheltered tag and +1 upgrade level on her ability. The level is restored when she leaves.
- `ProjectileCatchAndReturn` (Mark): catches allied projectiles coming from at least 2 tiles away when an unlockable is on. Modes are Refund (+1 AP, cooldown reset), BounceBack and both (default), with an optional QTE. A `// _pending.Dispose();` is left commented out.
- `MarkPassiveAbility_AtmanFocus` plays a "ProtectiveWord" VFX and a "Blocked" text. The FX runner isn't null-checked.
- `LucyFactionRoleHandler` returns false when no enemy faction exists (safe rooms). Its trigger now also fires after allied actions that affect an enemy it can reach.

**QTE and input**

- All QTE inputs are now LMB (the F/E to LMB/RMB change is mostly in data and prefabs). `QuickTimeEventHandler.SwallowPointerClick()` disables the UI input module for the frame, so a QTE click doesn't also click the grid or UI. `ConsumedClickThisFrame` lets `PlayerController` ignore the click.
- `QTEProfile.VisualMode` values were renamed (`AutoLookup`, `CustomTextOverride`, `CustomIcon`). `QTEButton` takes `QTEInputVisual[]` overrides. There are no new `BehaviorMode` kinds.

**Levels, missions and UI**

- **Mission map visibility (updated 10-03):** it is now shown only if the active mission's resolved graph has at least one node with multiple entity neighbours (`MissionTracker.ShouldShowMissionMap`, `SerializableDependencyGraph.HasMultipleEntityNeighbors`). That is a mission-level rule, not per-level. It has a "Retreat home" button for Home dungeon runs, and its legend lists only tags present in the map.
- `Mission` gains `HomeState` and `CompletionOrder`. `GameData` has `RecordMissionCompletion`, `GetLastCompletedMission` and `GetFurthestCompletedMission` (topological depth, ties by `CompletionOrder`).
- `CombatLevel.hidePointsBar`, `LevelObjectives.Evaluate(byPassAsTrue)` / `BypassCurrentObjectiveAsSuccess()`, and `CancelTurnActiveSwitch()`. `FactionTracker` now persists picked-up items across restarts through `_persistedPickedUpItems`, and `EndLevel` persists item state only on Win.
- `SafeRoomFunction.healFractionOfMax` plus `IsCampfire`. Dialogue characters `GenericCharacter_1..4` are assigned per mission by `MissionTracker.AssignGenericDialogueCharacters`, seeded by `GraphSeed`.
- Camera: `Focus(..., focusAreaMargin)` and `GUnit.FocusAreaMargin` override the margin. `JumpTo`, `StopMoveNow` and `CameraEdgeScroller.Suspended` were added. The camera stops if the input mode lacks the `Camera` flag.
- Dialogue Excel round-trip (`Core/Levels/Editor/DialogueExport/`, own README): menu `Tools > Dialogues > DialogueExcel`. It has a custom xlsx reader and writer, previews before applying, rejects assets changed since export (SHA256), and backs up to `Library/DialogueExcelBackups`. Batch export is `-executeMethod ExportBatch -dialogueExportPath <xlsx>`.
- `Core/Home/Runtime/`: `HomeStateManager.RefreshFromGameState` plays idle sets by the furthest or most recent completed mission.
- New `GlobalEventBus` events for Home: `homePhaseChanged`, `homeSlotResolved`, `homeDayReportReady`. `PlayModeStaticReset` covers the new statics.
- `AIRegressionTest` skips level prefabs under `/Content/Levels/` and `/Content/Home/Sorties/Levels/`, and its ability catalog includes the new duo abilities. **The 10-03 merge run showed `Baseline_MatchesCurrentAI` failing, as expected. The baked constants need a deliberate refresh.**

**New rough edges (10-03)**

- `Mark_Linda_ConsumeRaceDamage` removes its listener from `abilityActivationStarted`, but `Mark_Linda_ApplyBonus` added it on `abilityPerformed`. The listener leaks, though a null guard likely makes it harmless.
- The `John_Linda_Duo` target adjuster is registered as null, and `John_Linda_Duo_TargetAdjust` is unused.
- `CheatHandler`: K is bound twice (kill and +99 FTP). The speed cheats set `Time.timeScale` directly. *(Out of date: current keys in `tech/combat-architecture.md`.)*
- Unverified: whether `autoMoveAllowed` is set on existing basic-attack presets, `LevelSpecificBehaviour` (one-line change not read), and `Linda_Toba` / `Mark_John` / `Mark_Lucy` ability data.

## 1. Turn / Combat Flow

The core loop is still `Core/Managers/CombatLevelRunHandler.cs` (~1035 lines, 41KB), a `LevelRunHandlerBase` singleton.

- **Setup** (`StartLevelIE`):
  1. Fills roster slots into `GUnitPlaceHolder`s.
  2. Calls `FactionTracker.PrepareLevel(units)`. This replaces the old separate `RestoreUnitPersistedStates`/`RestoreItemState` calls. It also re-applies granted **Run Upgrades** (§5) and assigns the shared **Family AP** pool.
  3. Initializes the `GlobalEventBus` listeners, which are still recreated per level scene.
  4. Initializes the `CombatLevel` and handles branching (linear vs `Decidable` / `LevelDecision`).
  5. Plays the intro `Sequence`.
  6. Runs `AbilityIntroductionTracker.PlayPending(...)`. These are new one-shot ability tutorial sequences, see §6.
  7. Initializes the grid and calls `StartTurn()`.
- **Faction turn order**:
  - `PrepareFactions()` still builds one `FactionControllerBase` per present faction. Order comes from `CombatLevel.FactionTurnOrders` if set, otherwise from `Faction.TurnOrder`.
  - **Factions can now be added mid-level.** `EnsureFactionController` inserts the controller at its turn-order index (`IndexForTurnOrder`) and bumps `_currentTurnIndex` if it lands before the current faction.
  - `ReserveFactionPresence` / `RevokeFactionPresence` set `FactionControllerBase.PresenceReserved`. This keeps a faction with no live units in the rotation.
  - `CombatLevel.reservedPresenceFactions` pre-reserves factions at level load.
  - `CanPlayTurn` is `AliveUnits.Any(has abilities) || HasLiveRegisteredEntities || PresenceReserved`. The skip-turn tag gate is still commented out.
- **Designer phase control** (new):
  - `ResetCurrentPhase()` waits until `CanEndTurn()`, calls `controller.RestartTurn()` (the AI override cancels its worker jobs), then ticks.
  - `EndCurrentPhase()` calls `ForceEndTurnSafe()`.
  - Both are driven by `CurrentPhaseManipulationAction` in `LevelSpecificBehaviour` (§6).
- **ATB fill is now centralized in `HandleATBFill(ATBEventMode)`**, with modes `TurnStart/TurnEnd/AbilityStart/AbilityComplete/QTEStart/QTEEnd`.
  - **Correction:** the 09-07 brief said ATB "only fills on the player's own turn". The code does the opposite, both then and now.
  - During an **enemy** faction's turn, player ATB fills at `CurrentFaction.ATBFillRateFactor`.
  - During the **player's** turn, ATB is paused. While one player unit executes an ability, the *other* player units fill at `ability.ATBFillRateFactor × faction factor`, and the acting unit stays paused.
  - Fill pauses on QTE start. `QTEEnd` is a no-op because its resume is commented out.
  - The whole handler is skipped during a reactive interrupt or revenge sequence, which pause all ATB themselves.
- **Win/loss**: `UpdateObjectives()` → `CombatLevel.EvaluateObjectives()` → `LevelObjectives.Evaluate()`. `Evaluate` no longer takes a turn number; turn limits are now a condition type (§6).
  - Unit deaths no longer evaluate synchronously. `EvaluateObjectivesAfterDeaths` waits one frame so simultaneous deaths and synchronous replacements (e.g. Dark Worm splitting into halves) register first. Other objective triggers wait while this check is pending.
- **`EndLevel`**:
  1. Persists unit and item state and accumulates mission turn stats.
  2. On Win, resurrects the fallen and calls `MissionTracker.MarkCurrentLevelCompleted()`. This replaces the old `//todo GameProgress.MarkLevelCompleted`.
  3. Routes by result:
     - **Win with more levels** → `redirectAction = null`, and `CombatLevelUIManager.ShowMissionMapThenLoad()` shows the new **Mission Map** so the player picks the next level node (§6).
     - **MissionComplete** → `EndMission(true)` plus `AwardMissionCompletionResources`.
     - **Defeat** → `EndMission(false)` plus failure rewards, but only if `GameHandler.CanReturnHome`. During the opening mission (before its first completion), defeat calls `RestartLevel()` instead and gives no failure rewards (SEN-2718).
  4. Sandbox fast-forward runs skip all awards.
- **Per-unit turn FSM** is unchanged in shape: `Core/Interactions/Runtime/FactionControllerBase.cs` (~1005 lines, 44KB) + `FactionPhaseState.cs`, a function-object FSM with `UnitSelection → ActionSelection → TargetSelection → TakeAction`.
  - `FactionPhaseData` gains `ActiveUnitActionPoints` via `APConsumer`.
  - New helpers: `IsLegalAbilityTarget(cell)` (used by the cursor system), `IsSelectableUnitCell`, `RestartTurn()`, and `TryPlayFactionRole(unit)` (lets a faction role fire outside its own turn).
  - AP spending now goes through a virtual `ConsumeActionCost(count)` → `PhaseData.UpdateUnitActionPoints` → `APConsumer.Consume(type, count)`.
  - Multi-target changes: `TakeActionState` builds targets from `preset.OneEffectPerTarget`, which passes each pick as its own target instead of bundling them (§3). Target-count completion uses `RuntimeAbility.RequiredTargetCount` instead of `NextTargets.Length + 1`. Per-index lookups go through `AbilityPreset.GetTargetTypeAt(i)` / `GetTargetFactionRelationAt(i)`.
  - Targeting a shape captures its rotation input (`RuntimeAbility.CaptureShapeInputs`).
- **Player** (`PlayerController`, now **~1526 lines / 67KB**, up from 45KB) keeps everything from before: hover previews, auto-approach-then-attack, action-reversion QTE, revenge on ally death, and Family Super Time. New since 09-07:
  - **Reactive Interrupt** (`Player.ReactiveInterrupt` input, bound to **L**; SEN-2569 "Bergson Time"):
    - It is a toggle and works **only in `PointConsumptionMode.ATB`**. In FTP mode it does nothing.
    - It is available even during an enemy turn. It forces `IsTurnActive = true`, sets `Time.timeScale = reactiveInterruptTimeScale`, pauses all ATB, and plays a `CameraVolumeEffect` (the URP `BorderOverlay` renderer feature under `Features/Effects/ReactiveInterrupt/`).
    - Only units that `CanAffordFactionRole` (ATB gauge ≥ `FactionRoleRequiredFTP`) are selectable. Selecting one jumps straight into target selection for its faction-role ability.
    - `ConsumeActionCost` is overridden so interrupt actions spend ATB via `PointConsumer`, not AP.
    - There is a 0.5s re-entry cooldown. Everything is restored on exit, including the previously selected unit.
  - **End-of-turn AP→ATB conversion**: in `APConsumptionMode.PerUnit`, `EndTurn` calls `GUnit.ConvertUnusedApToAtbSteps()`. The Shared-mode equivalent `ConvertSharedFamilyApToAtbSteps()` is an empty `// todo..` stub.
  - **Enemy introductions** run at the start of the player turn (`StartTurnWithIntroductions`) and block input and `RequestEndTurn` until done (§8).
  - **AoE shape rotation**: the player watches the input actions named by `AEffectCompound.ShapeRotationInputAction` (`WatchShapeRotationInputs`) and re-previews on change.
  - Multi-target UX: `TargetSelectCounterUI` pips (count up/down), per-cell `TargetedCounterUI` repeat-target counts, and a hovered-target AP preview.
  - PassBy ghost preview (`ShowPassByPreview`) while choosing a move destination.
  - Approach-walk and damage preview for auto move-attacks, including correct AP display and handling of insufficient AP.
  - An ATB-usability indicator.
- **AI** (`AIController`) still drives the identical FSM, but asynchronously now. See §7.
- **Faction Roles**: `GlobalEventBus.onActionFlowEvent` → `CheckFactionRoleAbilities` works as before.
  - AI factions now **skip the FTP/ATB payment entirely** (`canPay = ControllerHandler == AI || ...`).
  - In Shared-AP mode, `StartTurn` resets the family pool (`FamilyActionPoints.ResetToInitial()`).

## 2. Grid System

`Core/Systems/GridSystem/Runtime/`:

- **`GridCell.cs`** (~44KB):
  - Core model unchanged: `Coordinates`, `AdjacentCells` (4-dir), `NeighborCells` (8-dir), `_occupantEntity`, `_plantedEntity`, and the stash mechanism.
  - **Made worker-thread-safe for the AI:**
    - `AdjacentCells`/`NeighborCells` return cached arrays (`_adjacentCellsArray`/`_neighborCellsArray`) instead of `.Values.ToArray()` per call.
    - `OccupantEntity`, `IsOccupied`, `PlantedEntity` and `IsWalkable` use `ReferenceEquals(x, null) && x.IsAlive` instead of Unity's overloaded `==`/`activeInHierarchy`. A comment explains why: Unity throws if those are read off the main thread.
    - **Gotcha:** occupancy now depends entirely on `IsAlive` being cleared. A destroyed-but-still-assigned entity reads as present.
  - `GetRangeCells` pure-distance branch: rewritten from a LINQ scan to a `HashSet`-backed loop, and it now honors `includeSelf` for footprint sources.
  - Planted `SpawnableEntity.ActivateOnTile` lets an entity activate on the cell itself instead of on each occupant.
  - New per-cell visuals: `TargetedCounterUI TargetedCounter` and `SetLevelGoalHighlight(bool)`.
  - `GetCellCost()` is **still a stub**: `// todo: calculate cell costs based on tags and attributes`. Only hazard `MovementCostModifier` affects cost.
- **`GridActions.cs`** still holds `GridPathFinding` (A\*, faction-relation-aware, multi-cell footprint via `mover`) and `HighlightPath`. Only minor changes.
- **`GridManager.cs`**: singleton, Tilemap → cell dictionary, row sort layers, hover. Gains `ResetPlayModeState`.
- **`GridPluggableEntity.cs`**: unchanged. Multi-cell footprints plus `Sim*` what-if moves for the AI.
- **`Core/Entities/Runtime/OnGridEntity.cs`**: non-stationary planted entities can apply a **pass-by effect** (`AEffectCompound passByEffect`, optional `preventRepeatPassBy`) when a unit's collider overlaps them in transit. This was added for Lucy's cyclone (SEN-2835).
- Editor tooling under `GridSystem/Editor/`:
  - `GridEntityDragTool`, `GridEntityInspectorWindow` (`Tools/Grid Entity Inspector`), `GridEntityPrefabPickerWindow`, `GridToolsOverlay`, `GridEditorContext`.
  - These got SceneView scan caching and inspector-leak fixes. They are the in-editor way to place and inspect grid entities.
- The grid is still a plain `Vector2Int` square grid: Manhattan distance for `Adjacent`, Chebyshev for `Radial`.

## 3. Ability System

Namespace `MISO.Core.Systems.AbilitySystem.{Abilities,Attributes,Effects,Points}`.

**Per-unit container**: `AbilityOrchestrator` is unchanged in role. It holds `AllAbilities`/`Abilities` (filtered by `.Available`) and `Items`, plus faction-role and super-time passthroughs.

**Data/runtime split**: `AbilityPreset` (~25KB) is authored data and `RuntimeAbility` is the live instance.

- **`RuntimeAbility.Available` is now `_upgradeLevel >= 0 || IsRunUnlocked()`.** A run upgrade can grant an ability the unit hasn't unlocked in meta-progression (§5).
- `Active` and `PossibleMultiActivations` read `GUnit.APConsumer` instead of `ActionPoints`.
- New members:
  - `RequiredTargetCount`.
  - `CheckTargetSelectionCondition(target, effectIndex)`, which is per-effect for one-effect-per-target picks.
  - `GetShapeRotationInputActions` / `CaptureShapeInputs`, which walk nested compounds and spawners.
  - `Copy()`, a MemberwiseClone that nulls runtime state and is used for simulation.
- `AdditionalStatSources` on abilities and units already existed at baseline; the 09-07 brief missed it. It registers extra named stat sources globally (`StatAttributeGlobalSourceRegistry`) so they can be inserted into a unit's Stat Evaluation Profile.

**`AbilityPreset` additions:**

- **`oneEffectPerTarget`** (when `multipleTargets` is on; SEN-2716):
  - Each pick receives one effect from the current level, in order, and the pick count equals that level's effect count.
  - The same target may be picked repeatedly, and extra effects fall onto the last pick.
  - Implemented by `AbilityEffectSetLevel.ApplyMapped(owner, targets[], ...)` and `FlattenMappedTargets`.
  - `GetEffects`/`GetLevelParameters` replace the old inline switch on `AbilityUpgradeMode`.
- **`introducible` + `introductionSequence`** ("First Appearance"): the sequence plays once, the first time a unit with this ability enters a level (§6).
- Surrounding-mode shape resolution now goes through `RunUpgradeTracker.ResolveAreaShape` so runes can swap the AoE shape.

**Effects** (`Effects/Runtime/`): the list from 09-07 is unchanged. Notable changes:

- **`AEffectCompound`** (~27KB, +186):
  - `shapeRotationInputAction`: hold a named input action to rotate the `AreaShapeDefinition` 90° while targeting.
  - `excludeOwner`, and an option to exclude unit-occupied cells from both preview and application.
  - **`lockedByDefault` + `unlockableReference`**: the sub-effect only applies if `FactionTracker.GetUnlockableState(ref)` is true. That now ORs in run-upgrade unlocks, which is how runes such as "Mark Vault Stun/cripple" and "Linda-Lucy cyclone spread" switch on extra effects.
  - Public `GetTargets(owner, target, statCtx)`.
  - Run-upgrade shape override.
- **`AEffectTransporter`**:
  - An option to fire on-tile effects only on the start tile.
  - An optional animator state on movement start (e.g. Evade).
  - `ApplyDirect(owner, destination, ...)`.
- **`AEffectDashAttack`**: a lethal hit now strikes first and then dashes into the vacated cell, so gaps no longer block placement (Mark ghost fix). Non-lethal hits stage beside the target.
- **`AbilityDamagePreview`** (+148): `ComputeFor(...)` returns a per-unit dictionary and mirrors `RuntimeAAttribute.SetValue` integer rounding so the preview bar and lethal checks agree with the real hit.
- New `ItemEffectPreview` (static): computes the HP (clamped to headroom) and FP (by scanning `ProduceFTP` function-caller effects) an item would restore, for the item-button hover preview.

**Attributes**: a new `IAttributeDecrementHandler`. An `AAttributeSetEntry` can reference a MonoBehaviour whose `ProcessDecrement(amount)` runs after damage modifiers (DR, evasion, equipment) but before the pool drops.

- Only `MarkPassiveAbility_AtmanFocus` implements it today (~+203 rewrite). The barrier either absorbs the whole hit, or acts as extra HP and spills the overflow onto health (`barrierActsAsExtraHealth`).
- The Focus damage buff is a single refreshed modifier with ID `MarkAtmanFocus`, applied through a dedicated additional stat source.

**Cooperation ("combo") system (updated 10-03)**: `UnitsCooperationHandler` was rewritten (~1500 lines). It is now data-driven entries plus hardcoded per-duo hooks for **seven** duos, including Mark-Lucy/Linda/John and Linda-Toba. See §0.

**Pass-by system** (existed before but was unmentioned):

- `UnitsPassByHandler` (per faction) activates a per-unit `PassByEntry.ability` when a moving unit crosses an ally. The trigger is `GlobalEventBus.unitsPassedBy`, and each pair fires once per turn.
- `ApplyMode` is `MovingOnOnTile`, `OnTileOnMoving` or `Both`.
- Now has VFX (`GUnit.PlayPassByVFX`), a ghost preview, and barks (§8). Dialogue CSVs live next to it: `Units PassBy Dialogues.csv` and `...Affirmation Dialogues.csv`.

**Faction-role handlers**: `FactionRoleHandlerBase` still gates on activation phase/moment, FTP cost, time-scale, QTE profile and silence.

- **Correction:** the 09-07 brief said `PrepareTargets` was abstract with no concrete override. In fact it is `protected virtual` and throws `NotImplementedException`, and the player overrides already existed at baseline under `Features/`: `JohnFactionRoleHandler`, `LucyFactionRoleHandler`, `LindaFactionRoleHandler`, `MarkFactionRoleHandler`. `GetCellsInRange()` also throws in the base.
- **New and first enemy-side handler:** `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs` (462 lines).
  - On a non-lethal `onUnitDamageDone` against itself, it checks the attacker can be hit in place or finds an approach cell. It then calls `controller.TryPlayFactionRole(Unit)`: walk if needed, then counter-attack.
  - Players get a **reaction preview** (move path, attack cells, predicted damage) when hovering the goblin or entering target selection on it.

**Points economy (substantially reworked):**

- **`APConsumer`** (new, 212 lines) now wraps every unit's AP. `GUnit.ActionPoints` became `GUnit.APConsumer`, and all call sites (FSM, `RuntimeAbility`, AI, co-op) go through it.
  - It still owns an `ActionPoints` internally: the main attribute pool plus `ExternalSourceAP`s. `ActionPoints` gains `OnPointsDrained` and `Unset(silent)`.
  - It branches on the new `GlobalSettingsSO.aPConsumptionMode`:
  - **`PerUnit`**: pure passthrough to `ActionPoints`, which is the old behavior.
  - **`Shared`** (player faction only):
    - The unit's own AP attribute is pinned to its minimum. Any produce on it, or on an external source, is **redirected into the family pool** (`OnSharedProduce`).
    - `Points` = `FamilyActionPoints.Value`, provided the pool can afford a Singular action.
    - **Per-unit escalating cost**: `GetActionCost(base) = base × aPConsumptionEscalationFactors[actionsTakenByThisUnit]`. The asset currently has `[1,1,2,4]`, so a unit's 3rd action costs double and its 4th+ costs 4×. Spreading actions across the family is cheaper.
    - `Closure` is a no-op; `Ineffective` just counts an action.
    - `RevertConsumption` refunds the last shared cost.
- **`FamilyActionPoints`** (new, 71 lines) is the shared pool, created in `FactionTracker.InitializePoints()` next to `FamilyTimePoints`.
  - `AssignUnits` sets max = `aPAvailabilityBasedOnUnitCount[unitCount-1]`, a `StatBackedValue[4]` table (fixed AP by squad size, per commit `1df24249`).
  - `StartTurn` resets it to initial.
  - `SharedAPIndicator` is the HUD view.
- **`ATBGauge`** gained `OnPointsUsable`/`CheckForPointsUsable` (for the ATB-usability indicator) and `SetFullyFilledExtra` hooks.
  - In ATB mode, a player unit with **0 AP on its own turn whose gauge fills gets +1 AP** through the `_atbAp` `ExternalSourceAP`. That AP is paid for by draining the gauge (`GUnit.InitializePartially`).
- `FamilyTimePoints` (FTP) and `PointConsumer` (spends FTP or ATB per `PointConsumptionMode` for faction roles) are unchanged.
- **Current `GlobalSettings.asset` values (updated 10-03)**: on `thj/home-test` `pointConsumptionMode: FTP` (`origin/main` has ATB) and `aPConsumptionMode: PerUnit` (Shared = 0, PerUnit = 1). See §0.

## 4. Units & Stats

**`GUnit`** (`Core/Units/Runtime/GUnit.cs`, ~1192 lines / 49KB) is still the single unit class for both sides. New since 09-07:

- `APConsumer` replaces `ActionPoints`.
- `ConvertUnusedApToAtbSteps()` (PerUnit mode, end of turn).
- `SetTurnStartMinATBFill(int)`: a turn-start ATB floor, set by the "Mark Turn ATB Fill Floor" run upgrade through `SendMessage`.
- `MarkEnergetic`/`MarkExhausted` visuals, reused by the reactive interrupt.
- PassBy and FP-gain VFX.
- `SpawnAt(cell, out unit)` for simplified mid-level spawning.
- **`unlockedAfterMission`** + `IsUnitUnlocked()`: roster units can be gated behind completing a mission. Mark is hidden until unlocked, and locked units don't show equipment.

**Two layered stat systems**: unchanged in design. Raw `AAttribute` pools use a fixed modifier order (`Override → Additive → Subtractive → Multiplicative → PostAdditive → PostSubtractive`), and evaluated `StatAttributeSet` factors use upgrade levels.

**Multi-source resolution (`StatEvaluation.cs`)** is **unchanged**. The order is still **Ability → Unit → Equipment → Faction → SkillTree**, folded in reverse. Equipment is still force-injected after Unit and additive-only. The only diff is a play-mode reset hook.

**New in `StatAttributeSet` — run level bonuses**:

- `_runLevelBonuses` is a `[NonSerialized]` dictionary keyed by attribute id, fed by `AddRunLevelBonus(attr, levels)`.
- The value read is `upgradeLevels[clamp(UpgradeLevel + bonus, 0, MaxUpgradeLevel)]`, so a rune moves the *index* along the same authored levels the skill tree steps through, instead of stacking a multiplier.
- The bonus deliberately isn't in `CaptureState`, so it never touches skill-tree or save data. `PrepareRuntime` re-syncs any bonus added before runtime attributes existed.
- Other helpers: `GetEffectiveUpgradeLevel`, `CanRaiseEffectiveLevel`, `ClearRunLevelBonuses`.

**Equipment**: the `EquipmentSocket` and global `EquipmentManager` design is unchanged. Mark got an equipment set.

**Memory/AI hooks**: `TotalAttacksMemory` / `_recentAttacksMemory` / TTL'd `MemorableAttacksMemory` as before.

- New `MemorableAttackMemoryShare` component (SEN-2697). A unit remembers attacks performed on listed prefab types within `listenRange`, so packs share grudges.
- The `Preset.Memorable` check in it is commented out, so it records *any* ability on those units.

**Death/revive**: unchanged (`Die`/`DiePermanently`/`DieRevivable`/`Resurrect`/`Revive`/`FakeDie`).

**Faction/roster**: `Faction` and `FactionTracker` as before. `FactionTracker` now also owns:

- `FamilyActionPoints`.
- `RunUpgrades` (a `RunUpgradeTracker`, §5).
- `_pickedUpItems`: picked-up relic items are re-added to every unit each level, and uses stack when the same item is picked again.
- `HasMetaUnlockable` (meta-progression only) vs `GetUnlockableState`, which is meta **or** a run-upgrade unlock.

**Player units** are under `Features/Player/{Dom, John, Linda, Lucy, Mark, Shared, Effects, PlaceHolder, _DEV_}`.

- **Dom was renamed Toba** at the prefab/asset level (`Unit_Toba`, `Unit_Toba_Ally`, `Unit_TobaEnemy`, `Avatar_Toba`), but the folder is still `Dom/`.
- Toba has a new **Wall** ability (`Toba_Ability_Wall` + area shape + prefab spawner).

**Enemies** are under `Features/Enemy/{Archer Goblin, Dark Claw (+ new Unit_BlackClaw variant), Dark Shaman, Dark Worm, Deevoted, Goblin Queen, Masher Goblin, Mountain Deev}`.

## 5. Run Upgrades (new system)

A roguelite-style in-mission upgrade layer. **A "run" is one mission**: `FactionTracker.EnterMission()` and `QuitMission()` both call `RunUpgrades.Clear()`. Code is in `Core/Systems/RunUpgrades/Runtime/`, `Core/Entities/Runtime/{Pickup,RunUpgradeAltar}.cs` and `Core/UI/Runtime/RunUpgrades/`.

- **`RunUpgradeSO`** (`[CreateAssetMenu "Game/Upgrades/Run Upgrade"]`, 146 lines):
  - Fields: `Id` (a GUID auto-assigned in `OnValidate`), title, description, icon.
  - `specificToUnit` is matched by `Nickname`.
  - Requirements: `requiredAbility`, optional `requiredUnlockable`, and `requiredSquadUnits`. The squad-units check is offer-time only: it never blocks a pickup already on the ground.
  - `RunUpgradeKind` has four kinds:
    - **`DivineRelic`**: grants a `RuntimeItem` with `relicUses` through `FactionTracker.AddUsableItem`.
    - **`AbilityRune`**:
      - `statLevelUps` (preferred) raise the authored-level index through `StatAttributeSet.AddRunLevelBonus`.
      - `statModifiers` are flat `AAttributeModifier`s tagged with `ModifierId = "RunUpgrade.{Id}"`, for stats without authored levels (e.g. +1 range).
      - `areaShapeOverride` swaps the AoE shape.
      - Targeting: `targetAbility` hits that ability's own stat set. Otherwise the rune hits the unit's set, or with `applyToFaction` it hits `Faction.StatAttributes` (e.g. faction-wide crit).
    - **`NewAbility`**: `unlockAbility` makes `RuntimeAbility.Available` true, and/or `grantUnlockable` adds a literal to `GetUnlockableState`. The literal is what unlocks `AEffectCompound.lockedByDefault` sub-effects.
    - **`Passive`**: `SendMessage(unitFunctionName, typed arg, RequireReceiver)` on each matching unit, e.g. `SetTurnStartMinATBFill`. It is stringly typed, and a typo throws at grant time.
- **`RunUpgradeTracker`** (501 lines, `FactionTracker.RunUpgrades`):
  - Grant checks: `CanGrant(upgrade, unit)`, which checks roster membership, the required ability/unlockable, not already granted, `HasLevelUpHeadroom` (a rune is refused if no affected unit has a higher authored level left) and `IsNewAbilityAlreadyOwned`. `GetBlockReason` returns a readable reason for tooltips and offer logs.
  - `TryGrant` records the grant and applies it to live units.
  - **Units are recreated per level**, so `FactionTracker.PrepareLevel` → `ApplyGrantedToUnits` re-applies every per-unit grant each level.
  - Faction-wide runes are applied once on grant and **inverted on `Clear`**, because faction stat pools persist across levels.
  - The **tracker is not `ISavable`**: it lives in memory only.
- **In-level delivery**:
  - **`Pickup`** (190 lines) is a 2D trigger, so a unit must walk onto it. Options include `playerOnly`. Besides a `RunUpgradeSO` it can grant a `GResource` amount range or `SendMessageUpwards` a function. Its static `Active` list feeds the tooltip.
  - **`RunUpgradeAltar`** (416 lines):
    - On `levelStarted` (or on `Start` / manually via `Roll()`), it builds a pool from `Resources/RunUpgrades` + `extraPool` − `excluded`, filtered by `allowedKinds` and by the same `CanGrant` rules. It Fisher-Yates-shuffles the pool and drops `dropCount` (3) pickups.
    - Drops fly out to `dropPoints` or an auto row, snapped to free walkable cells.
    - It prefers authored `RUP_*` pickup prefabs and falls back to a generic template.
    - Taking one offer withdraws the rest (`LeftoverMode` Destroy/Hide). `Reroll()` exists for debugging.
    - **The pick is uniform random with no rarity weighting, and there is no price/currency anywhere in code.** The "shop" (shopkeeper art in `Features/Levels/Shopkeeper/`, `LevelRunUpgradeRoom`) is presentational.
  - **`RunUpgradeTooltipUI`** (439 lines) polls the mouse itself, so it works while grid interaction is disabled. `Ensure()` builds a default layout at runtime if no prefab is placed.
- **Content**: 14 upgrades under `Resources/RunUpgrades/`:
  - IncreaseCriticalChance, JohnShieldDashRangeIncrease, JohnSwordDamage, LindaArrowDamageDecay, LindaExplosiveArrowDamage, LindaHarmonicSlamRadius.
  - LindaLucyCycloneSpreadUnlock, LucyEmbersDamage, MarkFistBlitzDamage, MarkTurnATBFillFloor, MarkVaultRange, MarkVaultStun, SistersBondDuoDamage, TobaShellRadius.
- **Safe rooms** are in `Content/Levels/DungeonSafeRooms/`: `LevelRunUpgradeRoom` (altar/shop), `LevelDivineRelicRoom`, `LevelHealingRoom`.
  - `SafeRoomFunction` (global namespace) heals all player units by applying an `AAttributeModifier[]`.
  - All three are tagged via level spec tags (§6).

## 6. Missions, Level Graph & Map UI (new/reworked)

- **Missions are now level graphs.** `Mission.LevelDependencyGraph` is a `SerializableDependencyGraph` (`Core/Utilities/`, +556 lines):
  - `Entity` nodes carry a `LevelBase` payload. `InterNode`s have `CombineMode` AND/OR and can be `randomized` with `options`/`selections` and per-output `OutputOption{byChance, chance}` (weighted draw without replacement).
  - `CreateResolvedCopy(seed)` produces a seeded, pruned runtime copy without mutating the authored graph.
  - `Mission.GetNextLevels` (linear) is gone.
- **`MissionTracker`**:
  - `GraphSeed` is rolled on every mission entry and **not persisted**.
  - `CompletedLevelNames` (in-memory) is fed by `MarkCurrentLevelCompleted()`.
  - `GetNextLevel` returns the first `Available` node. It is only a fallback now.
  - `Mission.Visited` (saved; old saves infer it from `completed`) drives "new" badges, and entering a mission persists it immediately.
- **`MissionRouteProgress`** (`Core/Levels/Runtime/`, 101 lines) is shared by gameplay and the map.
  - Node states: `Completed / Available / Current / Unavailable / Missed`.
  - Advancing down one route abandons its siblings, but shared descendants stay reachable.
  - AND gates blocked by an abandoned input are detected by fixed-point evaluation.
- **Flow**: on Win with levels remaining, `CombatLevelUIManager.ShowMissionMapThenLoad()` → `MissionMapUI.Show(mission, GraphSeed, completed, current, onNextSelected)` → the player picks an `Available` node → `GameHandler.LoadLevel(levelName)`, a new public entry point. If no `missionMapUI` is assigned, it falls back to `LoadNextLevel()`.
- **`Core/UI/Runtime/MissionGraph/`** (new namespace):
  - `MissionMapUI` (628 lines):
    - Layout uses authored graph-editor positions, or generated dependency layers when `useAuthoredPositions` is off.
    - Positions get seeded jitter plus minimum-gap overlap correction and are kept inside the scroll view.
    - Connectors are `UILineRenderer` lines, animated by `MissionMapConnectionAnimator`.
    - The legend is built dynamically from level spec tags (`MissionMapLegendRow`, `SpecTagIconSet`).
    - Node info reuses the home map's `MapMissionInfoPanelUI.ShowInfoForLevel(level, canContinue)`, with continue/cancel wired to confirm/cancel selection.
  - `MissionMapNodeUI` (199) handles per-node state, selection animation and icons.
  - `MissionCharacterPanelUI` / `MissionCharacterIconUI` show the mission roster.
  - `_Show(Mission)` is an Alchemy `[Button]` for previewing a mission graph in the editor.
- **Home world map** (`Core/UI/Runtime/Home/WorldMap/`): still the *mission* picker, while `MissionMapUI` is the *level-within-mission* picker.
  - Visual refresh.
  - `WorldMap_Button.SetMissionState(isNew, isCompleted)` plus hover and selection.
  - A loot preview from `Mission.GetCompletionRewardResources()`, which lists possible reward types without rolling them.
- **Level spec tags**:
  - `LevelBase.specTags` is a `GTagReference[]`, with `SetSpecTags`/`AddSpecTag`/`ClearSpecTags` helpers.
  - They drive map icons and the legend (Combat, HealingRoom, etc.; `Resources/Tags/LevelSpecTags.asset`).
  - Batch editing is in `Core/Levels/Utilities/Editor/LevelSpecTagTools.cs` (`LevelSpecTagBatchTool`, 347 lines), with menus under `Tools/Levels/Spec Tags/...`.
- **Randomized formations**: `CombatLevel.variantGroups` (`LevelContentVariantGroup{pickCount, candidates[]}`) keeps a random subset of `GameEntity`s. It is seeded by `GraphSeed ^ Animator.StringToHash(LevelName)`, so the pick is stable within a run (SEN-2884).
- **Objectives**:
  - The turn limit moved out of `LevelObjectives` (the `turnLimit`/`OnTurnLimitReach` fields were deleted) into a proper **`TurnReachedLOCondition`**.
    - It counts from the turn the objective first evaluates, not from level start.
    - It exposes `{turn_i}`, `{target_i}` and `{remaining_i}` to the text.
    - `LevelObjectives.TryGetTurnLimit` serves the UI.
  - `UpdateDisplayText()` is now public so the map can show objectives before a level loads.
  - `CombatLevel.GetVisibleObjectives()` reads authored data for unloaded prefabs.
- **`LevelSpecificBehaviour`** (`Core/Levels/Utilities/Runtime/`, +308) is a data-driven level-scripting system. `ManipulationType` values:
  - `GameObjectActivation`, `MonoBehaviourActivation`, `SpriteRendererColorSetter`.
  - `EntitySpawn`, whose **`Manipulate()` throws `NotImplementedException`**.
  - `GUnitSpawn`: `Specific`/`Random` entries, can execute multiple times.
  - `CurrentPhase`: Reset/End → §1.
  - `FactionPresence`: Reserve/Revoke → §1.
  - The static flag was renamed `LevelSpecificBehaviourInProgress` → `LevelSpecificBehaviour.InProgress`.
- **New sequence steps**:
  - `CFXSequence` (camera shake with an optional duration override).
  - `LSBExecutionSequence` (runs a `LevelSpecificBehaviour` call id and waits for it).
  - `SequencePlayHandle` (a MonoBehaviour for UnityEvent-triggered sequences).
  - `CameraSequence` gained skip support.
  - `AbilityIntroductionTracker` (static `ISavable`) plays each `introducible` preset's `introductionSequence` once ever. Reset it via `Tools/Save Data/Reset Saved Ability Introductions`.

## 7. AI

`Core/Systems/AISystem/Runtime/` is still fully utility-AI (blackboard + strategy planner + per-ability `UtilityScoreEvaluator` node graphs). **It now runs off the main thread.**

- **`AIWorker`** (new, 47 lines): a static single dedicated background thread (`"AIWorker"`, `IsBackground`) consuming a `BlockingCollection<Action>`.
  - The worker loop swallows exceptions ("ponytail" comment).
  - `IsWorkerThread` gates main-thread-only calls such as `Debug.DrawLine` and parts of `AILogService`.
  - **This resolves the old `AIBlackboard.Update // todo: threaded`**, and the comment is gone.
- **`AIFactionBrain`** (+181):
  - Every job runs through `AIWorker.Run`: plan refresh on unit birth/death or objective change, `PrepareUnitTurn(unit)`, `RequestPredictAllTargets()`.
  - Stale jobs are dropped with an `Interlocked` job id; `Cancel()` bumps it.
  - `_brainsGate` locks the unit-brain map.
  - Worker exceptions are stashed and re-thrown on the main thread via `ConsumeWorkerError()`.
  - Results are handed over through the `UnitTurnReady`/`PredictReady` flags and `IsComputing`.
  - This replaces the old per-plan background `Task`.
- **Thread-safety fallout elsewhere**:
  - **`GameEntityMessage`** (`Core/Utilities/`, new) is a reflection-cached `SendMessage`/`SendMessageUpwards` replacement. Entities are `Register`ed on the main thread first because `GetComponentsInParent` can't run on the worker.
  - `GridCell` null checks were rewritten (§2).
  - `UtilityVariables` path cache is under `CacheLock`, and `AIUnitBrain._bestForeSeenPathCache` has locks.
- **`AIBlackboard`**: the influence maps are the same concept (ally/enemy presence plus plan-driven cell/enemy/ally attractiveness). They were rewritten from per-update `Dictionary<GridCell,float>` BFS to flat arrays over a precomputed adjacency index (`_cellIndex`, `_adjacency`, reusable score/dist/queue buffers).
- **`AIUnitBrain`** (+237): perf work with reusable candidate/filter collections and presented-variable collection per evaluator, plus `LogEntityLabel`. Turn-ahead simulation (`PredictNextTargets`/`AITurnSimState`) works as before.
- **`AIController`** (+104):
  - Coroutine handles are tracked, and `RestartTurn` stops them and cancels the brain.
  - `isActionInProgress` includes `IsComputing`.
  - It waits on `OtherControllerBusy()`, so masher reactions and player reactive interrupts don't overlap AI actions.
  - It handles a unit dying mid-loop and supports `OneEffectPerTarget`.
  - Future-target prediction is async (`ApplyPredictedTargetsIE`). Win/defeat inversion for non-player factions and debug `autoPlayer` are unchanged.
- **`AIRegressionTest`** (`AISystem/Editor/`, 1042 lines, new) is a real, usable golden-master suite.
  - Run it from `Tools/AI/Run Regression Test` (dialog + log) or as the NUnit `[Test] Baseline_MatchesCurrentAI`. `com.unity.test-framework` 1.6.0 is installed; there are no asmdefs, so it lives in Assembly-CSharp-Editor.
  - It checks:
    - the expected objective-condition intent types, including `TurnReachedLOCondition`
    - the exact list of utility variable names
    - a **SHA1 of node data plus node/edge counts for every `UtilityScoreEvaluator` graph asset**
    - an ability→evaluator catalog and a unit catalog
    - custom-eval host methods (`GUnit.GetRemainingAP`, `BossMountainDeev.*`, `BossGoblinQueen.*`)
    - a stress pass: 500 iterations × all graphs, and 2500 intent plans. It reports µs/eval, evals/sec, the slowest graph and allocated bytes, and asserts no NaN/∞.
  - Catalogs are baked as string constants in the file, so **any intentional edit to a utility graph, AI ability or unit fails the test until the constants are hand-updated**.
  - `CheckBlackboardNullCell` is commented out.
- Editor-only `AILogService`/`AILogViewer` still work ("bring back AI logs" fix) and are worker-aware.

## 8. Presentation & Feedback Systems

- **Camera** (`Core/Camera/Runtime/CameraHandler.cs`, 620 lines, +303):
  - `FocusAndZoom(pos, zoom, duration)` moves and zooms at the same time for cinematic framing.
  - `Focus(subjects[], duration, ease, priority, minimal)` and `FocusInstant(CameraFocusQuery)`.
  - **Boundary tooling is finished, not "in progress"**:
    - `TryComputeBoundaryFromGrid(levelRoot, margin, out LevelBoundary)` is plain runtime code. It uses tile extents + half a tile + `BoundaryMargin`, widened so it's never smaller than the viewport at `minZoom` (fixes inverted clamps on small levels).
    - The per-level `[Button] AssignBoundaryFromGridEditor` and the batch `CameraBoundaryBatchTool` (`Tools/Levels/Assign Camera Boundaries (All Levels)`) share it.
    - Level boundaries were set in `cfc6994a`.
  - `CameraEdgeScroller` is unchanged.
- **Enemy Introductions** (`Features/Effects/EnemyIntroduction/`):
  - `EnemyIntroductionController` sits on the player controller. At the start of the player's turn, after sequences, QTEs and other controllers settle, it iterates enemy nicknames not yet seen. For each one it:
    - fades the main canvas and locks input
    - `FocusAndZoom`s on the nearest instance
    - applies a `CameraVolumeEffect` with the URP **`SelectiveGrayscale`** renderer feature (everything grey except sprites flagged via the `Selected` MaterialPropertyBlock)
    - shows `EnemyIntroductionUI` and waits for `CompleteCurrentIntroduction()` or an auto-hold
  - Seen state is saved in `EnemyIntroductionTracker` (static `ISavable`). Reset it via `Tools/Save Data/Reset Saved Enemy Introductions`, or disable the whole system with `GlobalSettingsSO.deactivateUnitIntroductions`.
- **Cursor** (`Core/UI/Runtime/Cursor/`):
  - **`CursorSituationCatalog`** (`[CreateAssetMenu "Game/UI/Cursor Situation Catalog"]`, 372 lines) has rows keyed by:
    - `CursorTurnSide`, `CursorPhase` (FSM state), `CursorOverlay` (Paused/Tutorial/Qte/Sequence/LevelDecision/LevelEnd/ReactiveInterrupt/SuperTime)
    - `CursorHoverTarget` (empty cell, selected/player/allied/enemy unit, planted/stashed, ability/end-turn/generic UI)
    - `CursorTargetFit` (Valid/Invalid/InRange/OutOfRange/Approachable), action type, apply mode
  - `TryResolve` picks the most specific matching row, then `priority`, then list order.
  - **`CursorSituationDriver`** (423 lines) renders a software cursor as a UI `Image`, hides the hardware cursor, raycasts UI and snapshots FSM state each frame. `Bind(catalog, parent)` creates it on demand.
  - It is gated by `GlobalSettingsSO.enableCustomCursor`, which is **currently 0 (off) in `Resources/GlobalSettings.asset`**.
- **Bark system** (`Core/Systems/BarkSystem/`, ~4.6k lines; it existed before but was unmentioned):
  - Barks are authored as **Unity GraphToolkit** graphs (`.barkfall/.barkkill/.barkability/...` files).
  - A `ScriptedImporter` (`BarkGraphImporter`) bakes them into `BarkGraphData`, loaded from `Resources/BarkSystemData`. There is also CSV dialogue-table support (`BarkDialogueTable`) and editor seeder/style-injector/unit-catalog helpers.
  - `BarkManager` (1652 lines) is one instance per level scene. It subscribes to `GlobalEventBus` (level start, unit died, ability started/performed, turn start, damage, selection, `unitsPassedBy`, FP changes) and shows text via `DamageNumberManager.ShowText`.
  - Duration and movement presets (Low/Medium/High) can be overridden per bark. There is a global repeat-suppression window, and `PlayOnlyOnce` state persists via `BarkPlayedTracker`.
  - **Not wired**: the `LevelEnd`, `Idle` and `EnemyEncounter` triggers have no engine events. **Authored-but-untracked conditions** (level index, mission visit count, duo/passive details, objective names) **evaluate as pass**, as the class doc comment itself states.
- **QTE**:
  - `QTEBehavior` is now class-per-mode via `QTEBehavior.Create(profile)`: `TimedPressQTE`, `MashQTE`, **`TimeWindowQTE`**, **`TimeWindowMashQTE`**. `QTEProfile.TimeWindowSettings` has `cycles`, `cycleDuration` and `validRange`.
  - `QTEButton` draws the valid band with the new **`RangeFilledImage`** (`Core/Utilities/UI/`, 448 lines). It is an `Image` subclass that fills a parametric `[fillStart, fillEnd]` interval, with an editor drawer.
- **Combat HUD** (`Features/UI/Panels/Scripts/`):
  - **`AbilitiesBarHUDUI`** (363 lines, new) has ability buttons and an item pouch (`UnitItemPouchButtonUI`). Clicking the selected ability again triggers the self/surrounding shortcut. The AP preview is driven centrally through `ShowAbilityAPPreview`, and default move/attack abilities show when auto-selected by a tile click.
  - AP views: `SharedAPIndicator` (family pool, shake on change) and `UnitAP_UI`/`UnitAPIndicator` (consume animation). The per-unit AP preview is kept in shared mode too.
  - Target counters: `TargetSelectCounterUI` and `TargetedCounterUI`.
  - `UnitPanelUI` (+256) got HUD tweaks (SEN-385).
  - `ObjectivesPanelUI`/`ObjectiveEntryUI` show the objectives for a duration when they change or on load. The "enemies remaining" line was removed.
  - `FutureTargetsPanelUI` got a small update.

## 9. Architecture Patterns

- **Global singletons everywhere**: as before (`GameHandler`, `MissionTracker`, `GlobalEventBus`, `GlobalSettingsSO`, `GridManager`, `CombatLevelRunHandler`, `LevelBase`/`CombatLevel`, `PlayerInputController`, `CameraHandler`, `BarkManager`, etc.). No DI.
- **Domain reload is OFF** (`ProjectSettings/EditorSettings.asset`: `m_EnterPlayModeOptionsEnabled: 1`, `m_EnterPlayModeOptions: 1`).
  - **`Core/Managers/PlayModeStaticReset.cs`** runs at `SubsystemRegistration`. It resets `Time.timeScale` and calls `ResetPlayModeState()` on about 40 statics: singletons, `SaveLoadManager`, the intro/bark/sequence trackers, `AIWorker`'s queue, `GameEntityMessage`, `UtilityVariableResolver`, `StatAttributeGlobalSourceRegistry`, `GlobalEventBus`, `HomeManager` and others.
  - A few classes self-reset with their own `[RuntimeInitializeOnLoadMethod]`, e.g. `Pickup`, `RunUpgradeTooltipUI`.
  - **Every new static field, singleton or cache must get a reset hook, or state leaks between Play sessions.**
- **Central event bus**: `GlobalEventBus` has about 40 `UnityEvent`s. Since 09-07 the only additions are the Home events `homePhaseChanged`, `homeSlotResolved` and `homeDayReportReady` (updated 10-03), plus a play-mode reset.
- **ScriptableObject + Referenceable Entity** convention: unchanged. New SO asset types follow it: `RunUpgradeSO`, `CursorSituationCatalog`, and the new `Sequence` subclasses.
- **GameplayTag system**: unchanged. It is now also used for level spec tags.
- **Function-object FSM**: unchanged, with more `protected virtual` hooks (`ConsumeActionCost`, `RestartTurn`, `IsSelectableUnitCell`).
- **Static save-tracker pattern**: `EnemyIntroductionTracker`, `AbilityIntroductionTracker`, `PlayedSequencesTracker` and `BarkPlayedTracker` are static `ISavable` singletons. They call `SaveLoadManager.Register(key, Instance)` before *every* access because `Load` replaces save delegates.
- **Main-thread vs worker discipline**: anything the AI reads (grid, units, abilities, utility variables) must avoid Unity-object APIs (`==` null, `gameObject`, `GetComponent*`, `SendMessage`) or pre-cache on the main thread. See §7.
- **Save system**: `ISavable<T>` + `SaveLoadManager.Register`. `Mission` (now with `visited`), `FactionTracker`, `RuntimeAbility` and the trackers above persist. **`RunUpgradeTracker` and `MissionTracker.GraphSeed`/`CompletedLevelNames` do not.**
- **Editor tooling** (integrated; new items in bold):
  - `LevelFastForwardRoster`, whose statics now reset without wiping the fast-forward EditorPrefs.
  - `SkillTreeEditorWindow`, `DependencyGraphWindow`, `LevelPlaceholderAssignWindow`, `StatBackedEvaluationProbeWindow`.
  - **`Tools/AI/Run Regression Test`**, **`Tools/Levels/Assign Camera Boundaries (All Levels)`**, **`Tools/Levels/Spec Tags/*`**, **`Tools/Save Data/Reset Saved {Enemy,Ability} Introductions`**, **`Tools/Grid Entity Inspector`**.
- **Dev cheats** (`Core/_Dev_/Runtime/CheatHandler.cs`; updated 10-03; *out of date, current keys in `tech/combat-architecture.md`*): enabled when `cheatsEnabled` is set, or at runtime by holding **C+H+T**. **K** kills the unit under the cursor and gives +99 FTP. **H** heals. **J** +1 ATB to all player units. **`[`** −1 HP (**Shift** −10). **`]`** +1 AP (**Shift** fills AP and resets cooldowns). **Numpad +/−/0** change or reset time scale. **Numpad 6** completes the objective. Holding **N** applies a key to the whole faction.

## 10. Known Rough Edges / TODOs (as of this read)

**Still true from 09-07:**

- `GridCell.GetCellCost()` (~line 779): tag/attribute terrain cost is still unimplemented; only hazards affect it.
- `FactionControllerBase.CanPlayTurn`: skip-turn-tag gating is still commented out.
- `FactionPhaseData.UpdateUnitActionPoints` (~line 71): `// todo: take AP Modifiers into account` is still there, now wrapping `APConsumer.Consume`.
- `CombatLevelRunHandler.AwardMissionCompletionResources`/`AwardMissionFailureResources` (~lines 795–826): the XP-split blocks are still commented out. (The level-completion `//todo` in `EndLevel` is resolved, see below.)
- **`AIUnitBrain.cs` (~lines 144–148)**: the commented-out merge-conflict markers (`// <<<<<<< HEAD`, `// =======`, `// >>>>>>> Arsham/ai-improvements`) and the old signature line are **still there**. It is dead-comment cruft that doesn't change behavior; delete the four comment lines.
- `GUnit.RemoveStatAttributeModifier` / `ApplyStatAttributeModifiers` (~line 946) still parse a comma-separated `"source,id"` string.
- `UnitsCooperationHandler` (updated 10-03): entries are data-driven, but the seven duos' init/target-adjust hooks are still registered by id in code. Adding a duo means writing code.
- `Scenes/"Obsolete - HomeScene.unity"` still exists. **Correction:** `Features/"Home - Imported"` is **not** superseded. The live Home scene in Build Settings is `Features/Home - Imported/___Khashayar/Home - Scene.unity` with `HomeManager`/`HomeInteractables`, which recently gained unlock conditions, locks and tutorials. `Features/Home/` holds only animations. The folder name is misleading.

**Resolved since 09-07:**

- `AIBlackboard // todo: threaded`: resolved by `AIWorker` plus the array-based influence maps.
- `FactionRoleHandlerBase.PrepareTargets`: the "no concrete override" claim was wrong. It is virtual, overridden by John/Lucy/Linda/Mark (already at baseline) and now by `MasherGoblinFactionRoleHandler`.
- `PlayerController.ActivateFactionRole` dead code: removed. It now carries an explanatory comment about refreshing the End Turn button.
- `EndLevel` level-completion `//todo`: replaced by `MissionTracker.MarkCurrentLevelCompleted()`.
- Camera boundary work: shipped.

**New:**

- `PlayerController.ConvertSharedFamilyApToAtbSteps()` is an empty `// todo..`. In Shared-AP mode, leftover AP gives no ATB, unlike PerUnit mode.
- `FamilyActionPoints`:
  - The constructor ignores its `units` argument, and `_level` is unused.
  - `AssignUnits` indexes `aPAvailabilityBasedOnUnitCount[count - 1]`, a 4-element array, so a squad of 0 or more than 4 throws `IndexOutOfRange`.
  - `UpdateCap` is **never called**: the call in `PlayerController.OnUnitDeath` (~line 1474) is commented out. The shared AP pool doesn't shrink when a family member falls, although the FTP pool does.
- `CombatLevelRunHandler.HandleATBFill(QTEEnd)`: the resume is commented out, so ATB paused by a QTE stays paused until the next `AbilityStart`/`TurnStart`.
- AI factions pay nothing for faction roles (`canPay` is always true for AI). This may be intentional, but it is undocumented.
- `RunUpgradeTracker` is memory-only. That is only safe while missions can't be resumed from a save.
- `RunUpgradeAltar` has uniform random picks with no rarity and no cost; the "shop" is presentational.
- The Passive run upgrade uses `SendMessage(..., RequireReceiver)` with a string method name.
- `Pickup.TryCollect` has `// todo: refresh unit control panel if active`.
- `EntitySpawnManipulationAction.Manipulate()` throws `NotImplementedException` but is selectable in the `LevelSpecificBehaviour` inspector.
- `MemorableAttackMemoryShare` has its `Preset.Memorable` filter commented out.
- `GridCell` occupancy relies on `IsAlive` because it uses `ReferenceEquals`, not Unity null (§2). Any despawn path that destroys an entity without clearing `IsAlive` or the cell slot leaves a ghost occupant.
- `AIRegressionTest` catalogs are hand-maintained constants, and `CheckBlackboardNullCell` is disabled.
- Bark triggers `LevelEnd`/`Idle`/`EnemyEncounter` are not wired, and untracked bark conditions evaluate as pass.
- `enableCustomCursor` is off in `GlobalSettings.asset`, so the whole cursor catalog is inactive in normal play unless toggled.
- Minor:
  - `SafeRoomFunction` has no namespace.
  - `CameraBoundaryBatchTool`'s header comment still says "place this file under an Editor folder", which it already is.
  - `AIStrategyPlanner` still has `// todo: simplified` and `// todo: add per unit influence maps`.
  - `AIUnitBrain` constructor: `// todo: add metric override + difficulty attributes`.

## 11. Key File Map (all under `miso/Assets/_Project/`)

```
Core/Managers/CombatLevelRunHandler.cs, GameHandler.cs, GlobalEventBus.cs, GlobalSettingsSO.cs, LevelRunHandlerBase.cs,
             MissionTracker.cs, MissionStatsTracker.cs, SaveLoadManager.cs, TimeOfDayTracker.cs, PlayModeStaticReset.cs (new)

Core/Systems/GridSystem/Runtime/GridCell.cs, GridManager.cs, GridActions.cs (A*), GridPluggableEntity.cs, GridEnums.cs
Core/Systems/GridSystem/Editor/GridEntityDragTool.cs, GridEntityInspectorWindow.cs, GridEditorContext.cs,
             GridEntityPrefabPickerWindow.cs, GridToolsOverlay.cs

Core/Systems/AbilitySystem/Abilities/Runtime/AbilityOrchestrator.cs, AbilityPreset.cs, RuntimeAbility.cs,
             UnitsCooperationHandler.cs, UnitsPassByHandler.cs, AreaShapeDefinition.cs, AbilityDamagePreview.cs,
             AbilityPushPreview.cs, FactionRoleHandlerBase.cs, RuntimeItem.cs, AbilityEnums.cs,
             AbilityIntroductionTracker.cs (new), ItemEffectPreview.cs (new)
Core/Systems/AbilitySystem/Effects/Runtime/AEffectBase.cs, AEffectCompound.cs, AEffectStatAttributeModifier.cs,
             AEffectAttributeModifier.cs, AEffectDurationAttributeModifier.cs, AEffectSpawner.cs, AEffectTransporter.cs,
             AEffectCommand.cs, AEffectDashAttack.cs, AEffectPusher.cs, AEffectSwapper.cs, AEffectCoOpTrigger.cs,
             AEffectFunctionCaller.cs, AEffectTagModifier.cs, AEffectResourceCollector.cs, AEffectVFXSpawner.cs,
             AEffectDummyDelay.cs, AGUnitSpawner.cs, AEffectTriggerReaction.cs
Core/Systems/AbilitySystem/Attributes/Runtime/AAttribute.cs, AAttributeSetBase.cs, AAttributeSet.cs (IAttributeDecrementHandler),
             RuntimeAAttributeBase.cs, RuntimeAAttribute.cs, AAttributeModifier.cs
Core/Systems/AbilitySystem/Points/Runtime/APConsumer.cs (new), FamilyActionPoints.cs (new), ActionPoints.cs,
             ATBGauge.cs, FamilyTimePoints.cs, PointConsumer.cs

Core/Systems/RunUpgrades/Runtime/RunUpgradeSO.cs, RunUpgradeTracker.cs                       (new)
Core/Entities/Runtime/Pickup.cs, RunUpgradeAltar.cs (new), OnGridEntity.cs, SpawnableEntity.cs, Projectile.cs
Core/UI/Runtime/RunUpgrades/RunUpgradeTooltipUI.cs                                            (new)

Core/Systems/StatsResourcesSystem/Runtime/StatAttributes/StatAttributeSet.cs (run level bonuses), StatEvaluation.cs,
             StatBackedValue.cs, RuntimeStatAttribute.cs, IHaveStatAttributes.cs
Core/Systems/StatsResourcesSystem/Runtime/SkillTree/SkillTree.cs
Core/Systems/StatsResourcesSystem/Runtime/GResources/, Unlockable/

Core/Systems/AISystem/Runtime/AIUnitBrain.cs, AIFactionBrain.cs, AIBlackboard.cs, AILogService.cs, AIWorker.cs (new),
             ActionPlanning/AIStrategyPlanner.cs
Core/Systems/AISystem/UtilityScore/UtilityVariables.cs, UtilityScoreEvaluator.cs
Core/Systems/AISystem/Editor/AIRegressionTest.cs (new), AILogViewer.cs
Core/Utilities/GameEntityMessage.cs (new), SerializableDependencyGraph.cs

Core/Systems/BarkSystem/Runtime/BarkManager.cs, BarkGraphData.cs, BarkDialogueTable.cs
Core/Systems/BarkSystem/Editor/BarkGraphs.cs, Importers/BarkGraphImporter.cs, Nodes/BarkNodes.cs, Nodes/BarkConditionNodes.cs

Core/Systems/TagSystem/Runtime/GTag.cs, GTagSet.cs, GTagEnums.cs, GTagModifier.cs, GTagQuery.cs, GTagReference.cs,
             GTagRegistry.cs, IOwnGTags.cs

Core/Units/Runtime/GUnit.cs, GUnitPlaceHolder.cs, MemorableAttackMemoryShare.cs (new), FactionsEnums.cs,
             Factions/Faction.cs, Factions/FactionTracker.cs, Factions/FactionDefinition.cs, Factions/FactionRegistry.cs

Core/Interactions/Runtime/FactionControllerBase.cs, PlayerController.cs, AIController.cs, FactionPhaseState.cs,
             PlayerInputController.cs, QTEBehavior.cs, QTEProfile.cs, QuickTimeEventHandler.cs, UnitThreatAnalysis.cs

Core/Camera/Runtime/CameraHandler.cs, CameraEdgeScroller.cs
Core/Camera/Editor/CameraBoundaryBatchTool.cs (new)

Core/Levels/Runtime/CombatLevel.cs, LevelBase.cs, LevelObjectives.cs, LevelObjectiveConditions.cs, LevelFactionRelations.cs,
             Mission.cs, MissionRouteProgress.cs (new), LevelDecisions.cs, LevelEnums.cs, Sequence.cs, SequencePlayer.cs,
             CameraSequence.cs, SequentialSequence.cs, CFXSequence.cs (new), LSBExecutionSequence.cs (new),
             SequencePlayHandle.cs (new), SafeRoomFunction.cs (new), LevelFastForwardRoster.cs
Core/Levels/Utilities/Runtime/LevelSpecificBehaviour.cs
Core/Levels/Utilities/Editor/LevelSpecTagTools.cs (new)

Core/UI/Runtime/CombatLevelUIManager.cs, EnemyIntroductionUI.cs (new)
Core/UI/Runtime/MissionGraph/MissionMapUI.cs, MissionMapNodeUI.cs, MissionCharacterIconUI.cs, MissionCharacterPanelUI.cs,
             MissionMapConnectionAnimator.cs, MissionMapLegendRow.cs                          (all new)
Core/UI/Runtime/Home/WorldMap/WorldMapPanelUI.cs, WorldMap_Button.cs, MapMissionInfoPanelUI.cs
Core/UI/Runtime/Cursor/CursorSituationCatalog.cs, CursorSituationDriver.cs                    (new)
Core/Utilities/UI/RangeFilledImage.cs (+ Editor/RangeFilledImageEditor.cs), UILineRenderer.cs

Core/_Dev_/Runtime/CheatHandler.cs
Core/Editor/SaveDataTools.cs, StatBackedEvaluationProbeWindow.cs
Core/Fundamental/GameEntity.cs, Constants.cs

Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs                        (new)
Features/Player/{John,Lucy,Linda,Mark}/Scripts/*FactionRoleHandler.cs
Features/Player/Mark/Scripts/MarkPassiveAbility_AtmanFocus.cs
Features/Effects/EnemyIntroduction/EnemyIntroductionController.cs, EnemyIntroductionTracker.cs,
             SelectiveGrayscale.cs, SelectiveGrayscaleRendererFeature.cs                       (new)
Features/Effects/ReactiveInterrupt/RendererFeature/BorderOverlay.cs, BorderOverlayRendererFeature.cs (new)
Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs (new), UnitPanelUI.cs, SharedAPIndicator.cs (new), UnitAP_UI.cs (new),
             UnitAPIndicator.cs, TargetSelectCounterUI.cs (new), TargetedCounterUI.cs (new), UnitItemPouchButtonUI.cs (new),
             ObjectivesPanelUI.cs, ObjectiveEntryUI.cs, QTEButton.cs, FutureTargetsPanelUI.cs
Features/Home - Imported/___Khashayar/HomeManager.cs, HomeInteractables.cs, "Home - Scene.unity"  (live Home)
Features/Levels/RunUpgradeAltar/RunUpgradeAltar.prefab, Features/Levels/Shopkeeper/

Resources/GlobalSettings.asset, Resources/RunUpgrades/ (14 RU_* assets + RUP_* pickups), Resources/BarkSystemData/,
             Resources/Tags/LevelSpecTags.asset
Content/Levels/M*.asset (missions M1–M14), Content/Levels/DungeonSafeRooms/{LevelRunUpgradeRoom,LevelDivineRelicRoom,LevelHealingRoom}.prefab

Scenes/: CombatLevelContainerScene.unity, IntroScreen.unity, LoadingScreen.unity, MainMenuScene.unity,
             "Obsolete - HomeScene.unity", PreloadScreen.unity, RosScene.unity, SplashScreen.unity, DevScenes/
```

## 12. How Claude can help going forward

- **Code changes** (new abilities, effects, AI tweaks, bugfixes): edit `.cs` files directly. There's no need to open Visual Studio; Unity recompiles when the Editor regains focus.
  - **Domain reload is off.** Any new static field, singleton `Instance` or static cache needs a `ResetPlayModeState()` registered in `PlayModeStaticReset` (or its own `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]`).
  - **Anything the AI can read runs on the `AIWorker` thread.** Don't add Unity-object calls (`==` null on UnityEngine.Object, `gameObject`, `GetComponent*`, `SendMessage`, `Debug.DrawLine`) to grid, unit, ability or utility-variable code paths without a main-thread guard.
- **After touching AI content or code**: run `Tools/AI/Run Regression Test`. If a failure is intentional, update the baked catalogs in `AIRegressionTest.cs` deliberately.
- **New GameObjects/prefabs/ScriptableObject assets**: Unity scenes, prefabs and `.asset` files are YAML text and can be edited directly for small, well-scoped changes.
  - For anything non-trivial (new enemy variant, new ability preset wiring, new level objective config, new `RunUpgradeSO` + `RUP_` pickup prefab, mission graph edits), a one-off Editor script run once from the Unity menu is safer than hand-editing GUIDs/fileIDs.
  - Batch level edits already have menus: camera boundaries and spec tags.
- **Grid/level layout**: genuinely easier live in the Editor via computer use. Unity and Unity Hub have full computer-use access; Visual Studio is view/click-only, with no typing. The Grid Entity Inspector and drag tool help here.
- **Testing**:
  - Read Unity's own log file directly off disk after a Play session instead of screenshotting the Console. It is faster and has full stack traces.
  - `LevelFastForwardRoster` jumps straight into a specific level with a chosen roster, bypassing the front-end flow. It is the best path for fast iteration; note that sandbox runs skip mission rewards.
  - Dev cheats (J/K/H/`[`/`]`, Shift variants, Numpad time scale and objective bypass; C+H+T enables them at runtime) cover ATB, FTP, HP, AP/cooldowns and objectives.
  - Reset one-shot intro state via `Tools/Save Data/Reset Saved {Enemy,Ability} Introductions`.
  - `GlobalSettings.asset` is where the resource modes are switched (`pointConsumptionMode` FTP/ATB, `aPConsumptionMode` PerUnit/Shared + escalation table), as are custom cursor and unit introductions.
