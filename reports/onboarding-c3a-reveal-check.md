# Report: C3a step 1, hidden cue enemies and their reveal (read-only check)

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (investigation only, no code or asset changed)

Paths below are under `miso/Assets/_Project/`. Line numbers are from the working tree on 2026-11-01.

## Short answer

An **inactive GameObject** under its cell's occupant root is already out of play in every system the plan lists: each level-start collector either skips inactive objects or reads the faction controllers, which never see the unit. A reveal only needs to do for an existing instance what `GUnit.SpawnAt` does for a new one: activate, `Initialize(true)`, `PlugEntity`, `RegisterUnit`. Those calls are all public and used unchanged, so the reveal fits in **one small non-core component plus a sequence** in `Features/Onboarding/`. No core-system behaviour change is needed (not Tier 3).

## What the level start does with an inactive placed unit

| Collector | Where | What it does with an inactive unit | Result |
| --- | --- | --- | --- |
| Run handler unit list | `Core/Managers/CombatLevelRunHandler.cs:249`, `:266` (`FindObjectsByType<GUnit>`, which skips inactive objects by default) and `:252` (`RemoveAll(!activeInHierarchy)`, the existing filter for units removed by a level decision) | Not in `_units` | Never initialized (`PrepareUnits` `:378`), not given to any controller (`PrepareFactions` `:381-410`) |
| Turn order / unit FSM | `Core/Interactions/Runtime/FactionControllerBase.cs:91-98` (`PhaseData.OwnedUnits` from the list above) | Not owned | No turn, no AP, not in `AllUnits`/`AliveUnits` |
| ATB gauges | `GUnit.Initialize` `Core/Units/Runtime/GUnit.cs:333` (player faction only) | n/a for enemies | none |
| AI faction brain | `Core/Systems/AISystem/Runtime/AIFactionBrain.cs:40-46` (unit brains from the controller's units); targets from `AIBlackboard.cs:90-91` and the turn order `AIFactionBrain.cs:313-327` (`Controller.AliveUnits`/`AllUnits`) | No brain, not a target, not an ally | No AI turn, not considered |
| Grid occupancy | `Core/Systems/GridSystem/Runtime/GridCell.cs:198` (`occupantRoot.GetComponentsInChildren<GridPluggableEntity>()`, active only); occupancy also needs `IsAlive` (`GridCell.cs:43-59`), which stays false until `Initialize` | Not plugged, `CurrentCell` null | The tile is free: walkable, targetable as empty, does not block |
| Targeting / visibility | inactive GameObject: renderers and colliders off | n/a | Not visible, not hit by raycasts, not on any cell |
| Objectives "N units of faction alive/dead" | `Core/Levels/Runtime/LevelObjectiveConditions.cs:85-96` (`controller.AllUnits`) | Not counted | See the objectives risk below |
| Enemy alert | `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.cs:73-91` (`BeginLevel` registers `LevelUnits()`, `:369-377` = controllers' `AliveUnits`) | Not registered, no watch, no Unaware tag | No alert state at all |
| Enemy alert on arrival | `EnemyAlertTracker.Events.cs:98-108` (`unitBorn` → `Register`, `EnemyAlertTracker.cs:119-140`) | On reveal: with `LevelAlertSettings.AllEnemiesStartAlert` (`level alert all`) it registers alert; without it, an `EnemyAlertSettings.StartsAlert` on the unit does the same | Comes in alert |
| Enemy introduction | `Features/Effects/EnemyIntroduction/EnemyIntroductionController.cs:79` (controllers' `AliveUnits`) | Not seen until revealed | After a reveal, a Claw seen for the first time can get its introduction at the next check |
| Present factions | `CombatLevel.ExistingFactions` `Core/Levels/Runtime/CombatLevel.cs:91` (`GetComponentsInChildren<GUnit>()`, active only) and `CombatLevelRunHandler.cs:385-395` | A faction with **only** hidden units has no controller | The reveal must create it (`AddFactionControllerMidWay`, as `SpawnAt` does) or reserve it |
| Camera bounds | `Core/Camera/Runtime/CameraHandler.cs:619` (a serialized `LevelBoundary` computed from the grid in the editor) | Not unit-based | none |
| Fast-forward roster | `Core/Levels/Runtime/LevelFastForwardRoster.cs:131` (`GetComponentsInChildren<GUnit>(false)`, player units only) | Skipped; enemies are not concerned anyway | none |
| `LevelStartFPFiller` | `Core/Levels/Runtime/LevelStartFPFiller.cs:11` (an explicit list of player units) | n/a | none |
| Family Roles / FTP / role zones | Role handlers read the grid and controllers; `RoleZonePresenter` listens to `unitBorn` | Unit is invisible to them | They pick it up on reveal through `unitBorn` |
| Barks, mission stats, combat log, HP snapshots | `BarkManager`, `MissionStatsTracker.cs:100`, `CombatLog.Units.cs:64`, `CombatLevelRunHandler.cs:829`, all `FindObjectsByType` (active only) | Skipped while hidden | Included after reveal |
| `MoveUnitSequence` / `UnitAnimationSequence` | `Core/Levels/Runtime/MoveUnitSequence.cs:17` (active only, by nickname) | Can't find a hidden unit | Works after reveal |
| Save | units are not saved mid-level; a restart reloads the prefab | n/a | Hidden state comes from the prefab, so it survives abort/restart (plan risk covered) |
| Editor XP checker | `Core/Levels/Editor/LevelXpChecker.cs:81` (`GetComponentsInChildren<GUnit>(true)`) | **Includes** hidden units | Good: their per-instance XP is checked, which is why placed hidden units beat spawned ones |
| World map enemy preview | `Mission.cs:210`, `MapMissionInfoPanelUI.cs:130` (include inactive) | Lists hidden Claws among the mission's enemies | Cosmetic; matches what the player fights |

So "while hidden" is fully covered by the inactive GameObject alone, with nothing new.

## What a reveal must do (the spawn path)

`GUnit.SpawnAt` (`GUnit.cs:405-432`) is `Instantiate` → `Initialize(true)` → `spawnCell.PlugEntity(unit)` → `AddFactionControllerMidWay` if the faction has no controller → `Faction.Controller.RegisterUnit(unit)`. `RegisterUnit` (`FactionControllerBase.cs:125-132`) adds the unit to `OwnedUnits` sorted by turn order and raises `unitBorn`, which the AI brain (`AIFactionBrain.cs:51`, adds a unit brain and replans), the alert tracker, role zones, low-health bars, the quiver pick-up and the combat log listen to.

For an existing hidden instance the same steps run in place: `gameObject.SetActive(true)` (runs `Awake`, as `Instantiate` does), `Initialize(true)` (`GUnit.cs:308`; `true` plays the spawn animation, `EntityAnimationHandler.cs:68`), `cell.PlugEntity(unit)` (`GridCell.cs:677`; the cell is the unit's parent `GridCell`, found on the main thread), then the controller part. All of these are public and keep their behaviour. Per-instance HP still applies: `Initialize` reads the instance's serialized stats and fills HP to max; the enemy tier bonus sits on the faction and was applied before, so a late `Initialize` reads it the same way a spawn does.

The only call not reachable as-is is `SpawnAt` itself (it always instantiates). Changing `SpawnAt` into a "reveal existing" would be a core change; it isn't needed.

## Options

| # | Option | Pieces | Non-core? | Size | Verdict |
| --- | --- | --- | --- | --- | --- |
| A | **Inactive placed units + `HiddenLevelUnits` component + `RevealUnitsSequence`** | New MonoBehaviour on the level root, `Features/Onboarding/HiddenLevelUnits.cs`: serialized groups `{ id, GUnit[] units }` and `Reveal(groupId)` doing the steps above, skipping units already revealed, refusing before `levelStarted`. New `Sequence` asset type `RevealUnitsSequence : Sequence` (group id, optional wait for the spawn animation) that finds the active level's component and calls it. The builder: `level hidden x,y …` (optionally with a group name) sets the instance inactive and adds it to the component. | Yes (new files only, uses public core APIs unchanged) | S–M: ~80 lines runtime, ~40 builder, tests | **Recommended** |
| B | Same, triggered from an LSB | A `ManipulationAction` subclass (`UnitRevealManipulationAction`, direct `GUnit[]` refs) in a new file; `LevelSpecificBehaviour.cs:20-28` actions are `[SerializeReference]` and Alchemy's dropdown (`Assets/Alchemy/Editor/Internal/SerializeReferenceDropdown.cs`) lists subclasses. Run through `LSBExecutionSequence`. | Yes (but `Type` is an abstract enum property in a non-core file: return an existing value or add one) | S | Usable as a second trigger; the builder can't easily author LSB `[SerializeReference]` entries, and sequence assets can't hold prefab refs, so A is cleaner for the tool |
| C | `GameObjectActivationManipulationAction` alone (`LevelSpecificBehaviour.cs:31-42`) | existing | Yes | 0 | **No**: the unit shows up uninitialized (`IsAlive` false), unplugged and unregistered: visible but not in play, not targetable, never takes a turn |
| D | `GUnitSpawnManipulationAction` (`LevelSpecificBehaviour.cs:100-200`) | existing | Yes | 0 | **No**: ruled out by the "no spawned enemies" decision (spawned enemies' XP can't be zeroed per spawn) |
| E | Active units hidden by tags (`skipTurnTagsQuery`, `objectivesIgnoreTagsQuery`, `FactionControllerBase.cs:57-60`, `:286`) plus hidden visuals | data only | Yes | S | **No**: still occupies and blocks its tile, still an AI target, still enters alert registration; the skip query is Stunned/Unaware, which fights `alert all` |
| F | A "reveal" mode inside `SpawnAt` or a `GUnit.Reveal()` | core | No (Tier 3) | S | Not needed |

## Recommendation

Option A. The units are inactive in the prefab (the builder sets them up from `level hidden`), so abort and restart are right for free. The component holds no statics (no `PlayModeStaticReset` hook needed). Order inside `Reveal`: activate → `Initialize(true)` → `PlugEntity` on the parent cell (it falls back to the nearest free cell if a player unit stands there, moving the Claw over) → `CombatLevelRunHandler.Instance.AddFactionControllerMidWay(unit.FactionRef)` when `unit.Faction.Controller` is null → `RegisterUnit`. Everything runs on the main thread. The AI picks the unit up on its worker through the existing `unitBorn` path, the same as a summon.

Tests (EditMode): the builder line (parse, error on a tile with no enemy, the instance inactive and listed after the build, round-trip), and the component's pure checks (unknown group, double reveal, a unit with no parent cell) through a small static helper. The real reveal (turn order, AI, alert, objectives) needs the verifier's play check.

## Risks for the build and for C3b

- **Objectives before the reveal.** "Faction has fewer than 1 alive" counts only registered units. If the visible enemies die before the reveal, or a faction has only hidden units (no controller, `LivingUnitsLOCondition` reads 0 alive), that objective is met early. A `UnitDeathLOCondition` or `EntitiesDestroyedLOCondition` naming a hidden unit is met at once (`LevelObjectiveConditions.cs:116-120`, `:131-135`: not `IsAlive`). Segment stages must not use those conditions before the reveal, or the level reserves the faction (`ReservedPresenceFactions`, or `FactionPresenceManipulationAction`).
- **Turn timing.** A unit revealed during the player's turn joins its faction's list and acts on that faction's next turn. If revealed during the enemy turn, it joins the list being played. Segment 2's interruption and segment 4's mother scene both happen in the player's turn, which is the safe case.
- **Enemy introduction pop** may show for a revealed Claw seen for the first time. Check it in the play check; the scene probably wants it off or already shown.
- **`level_to_grid.py`** does not read `m_IsActive`, so a round-trip shows hidden Claws as normal enemies and drops the `level hidden` line. It needs the same line, or the round-trip criterion has to accept that difference.
- `LSBExecutionSequence.cs:13-14` throws a null reference if the call id isn't found (`set` null). Not this task's to fix; worth knowing if option B is used.
- Calling `Initialize` on a placed unit mid-level is new (only spawned instances do it today). It's the same code, but the reviewer should check it against `core-systems.md` as "public API used unchanged".

## Can a sequence fire an ability? (segment 4's Tempest Bloom)

Not with what exists: no `Sequence` or LSB action casts an ability. `MoveUnitSequence` is the nearest case: it calls the move ability's `AEffectTransporter.Apply` directly (`MoveUnitSequence.cs:28-55`). A new non-core sequence could call the public `AbilityOrchestrator.ActivateAbility` (`AbilityOrchestrator.cs:67`), but that skips the controller's action flow. `abilityStarted` is raised by `FactionControllerBase.cs:708`, not by `RuntimeAbility.Activate`, so a sequence cast misses the action-flow events that the HP snapshot (`onUnitDamageDone`), roles, the alert tracker and the combat log rely on, and it spends no AP. Tempest Bloom is a reaction, Linda's arrow entering Lucy's Cyclone (`Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs:35`), so a scripted version needs two such casts in order, plus the unlock. **Recommendation: the plan's fallback**, `LevelStartRunUpgradeGrant` with `RU_LindaLucyCycloneSpreadUnlock` and a guided player action. A scripted cast would be a new, riskier piece; ask before building it.

## Save reset

No (nothing run).

## Decisions I made

- None (investigation only).

## Needs THJ

None. No core change is needed.

## Docs to update

- When built: `tech/level-tools.md` (the `level hidden` line), `tech/combat-architecture.md` (`HiddenLevelUnits`, `RevealUnitsSequence`).

## Proposed commits

None (no files changed).

## Other branches

none

## How to see it

Nothing to see yet. After the build: open a memory segment from the toolbar. The cue Claws are not on the board, and their tiles are walkable. Play the reveal sequence: they appear with the spawn animation, alert, show in the enemy turn, take their turn, and count for "all enemies dead".
