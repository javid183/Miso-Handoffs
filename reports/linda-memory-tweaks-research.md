# Linda memory tweaks: code facts (2026-11-04)

Explore, read-only, for `linda-memory-tuning` (b). Paths under `miso/Assets/_Project/`. "Core" = listed in `tech/core-systems.md`.

## T1/T2 Ability lock (Explosive Arrow, Encore)

- No per-level or sequence ability lock exists. Only gate: `RuntimeAbility.Available` (`Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs:42`) = `(_upgradeLevel >= 0 || IsRunUnlocked()) && IsCooperationAllowedBySquad()` (core). Setters: `SetUpgradeLevel` :255, `TryAddTemporaryLevel` :268, `RemoveTemporaryLevel` :280.
- Bar hide hook (not core): `AbilitiesBarHUDUI.Populate` (`Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs:57`) skips `QuiverAbilityInfo.HiddenFromBar(ability)` (today: Encore when the quiver is off). `UnitAbilityButtonUI.Refresh` :91 sets `interactable`; `SetInteractable` is overwritten by the next Refresh.
- Run upgrades can unlock (`LevelStartRunUpgradeGrant`, `RunUpgradeTracker.TryGrant`), not lock.
- Sequences: Audio, CFX, Camera, DialogNode, GridVisual, HUD, LSBExecution, MoveUnit, PlayerInput, Signal, Sequential, Tutorial, UnitAnimation; onboarding adds RevealUnits, SleeperSightBeat, GuidedSkillSpendMarker. None locks an ability.
- Objectives play sequences only via `LevelObjectiveGroup.onCompleteSequence` (`LevelObjectives.cs:90`, needs `queueWinGroups`, not the last group); `CombatLevelRunHandler.UpdateObjectives` :640 raises `GlobalEventBus.objectivesSetAdvanced` then plays it. Nothing plays on objective activation.
- Assets: Explosive Arrow `Resources/UnitSpecific/Player/Linda/Attack/Explosive Arrow/Linda_Ability_ExplosiveArrow.asset` (title "Explosive Crescendo"); Encore `Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset`. `GB_m1-linda` doesn't override Linda's kit.
- **Pickup by walking already exists** (`Features/Player/Linda/Scripts/Quiver/GroundedArrowField.Pickup.cs`, `ArrowPickupRules.cs`). T2 = lock Encore only.

## T3/T4 Pulse

- Combat button pulse exists: `Features/Onboarding/GuidedAbilityHint.cs` (fields ability, firstTurn, lastTurn, amplitude, period; finds `UnitAbilityButtonUI` :181; stops on first use or after lastTurn). Turn-gated only. Used in `GB_m3-john`, `GB_m4-mark`.
- Home tree pulse (`AbilityTreePanelUI.Highlight.cs`) not reusable here. Others: `ImageAlphaPulse`, `LethalMarkPulse`, `QuiverUI.Pulse()` :281.
- No "out of arrows" bus event. `LindaQuiver`: `OnChanged` :52, `OnSpent` :56, `OnReturned`, `IsEmpty`, static `IsEmptyFor(GameEntity)` :93; `QuiverHudFeedbackRules.ShowsEmptyTint`. None core.

## T5 Enemy order

- Per-unit order = serialized `GUnit.turnOrder` (`Core/Units/Runtime/GUnit.cs:158`). Prefab defaults: ArcherGoblin 1, Masher 2, DarkWorm 2, Deev 2, Queen 3.
- `FactionControllerBase.Initialize` :96 and `RegisterUnit` :129 stable-sort by TurnOrder; start list from `FindObjectsByType<GUnit>(FindObjectsSortMode.None)` (`CombatLevelRunHandler.cs:249/266`) → **ties play in unspecified order**.
- AI loop: `AIController.HandleUnits` ~:68 takes `ToPlayUnits.First()`. Prediction `AIFactionBrain.UpcomingTurnOrder` :312 uses the same list.
- Mid-level entry (`GUnit.SpawnAt` :405; `HiddenLevelUnits.RevealUnit` :110–127) calls `RegisterUnit` → re-sorted by TurnOrder.
- Per-level override today: factions only (`CombatLevel._overrideTurnOrders`). A prefab-instance override of a unit's `turnOrder` works as is; no level uses one.
- Core: GUnit, FactionControllerBase, FactionPhaseState, AIController, AIFactionBrain, CombatLevel, CombatLevelRunHandler.

## T6 Objectives inspector bug

- Cause: shared `[SerializeReference]` instances, not code. `LevelObjective.conditions` is `[SerializeReference, SubclassSelector] LevelObjectiveConditionBase[]` (`LevelObjectives.cs:19–20`, MackySoft drawer). Unity's list "+" copies the last element as the same reference.
- `GB_m1-linda.prefab` (uncommitted): `winObjectiveGroups[0..2].objectives[1].conditions[0]` all rid `8881842456907219035` (one `TurnReachedLOCondition`, turn 4, line 2353). Runtime too: one `_objectiveStartTurn` for the three stages; `TryGetTurnLimit` reads the first.
- `HearthMemoryWiring.Lucy.cs:237–249` (`Claim<T>`) + `HearthMemoryLucyTests.cs:138–146` guard against it; `HearthMemoryWiring.Linda.cs:124–135` reuses the reference on purpose (re-running it would re-share).
- Other duplicates (quick scan, `main` data too): `Level2/Level2-C2.prefab` (2286948190321115209, …212), `Level2/Level2-C3-2.prefab` (8046274729047228497), `Level2/LevelDomFight.prefab` (8046274707106824280).
- Fix hooks: data fix (new instance per objective); guard by `CombatLevel.OnValidate` dedupe via `Copy()` :58 (core) or an editor test scanning level prefabs (not core).
