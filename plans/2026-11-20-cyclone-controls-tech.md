# Cyclone controls: click to Steer, Steer pulse, free first Steer, Mark's Command steers (tech)

Size: L    Tier: 3 (decided by THJ: D-589 to D-593)    Assigned to: miso-implementer, one chunk at a time
Branch: thj/cyclone
Status: waiting on THJ (core hooks: plan shown first, CLAUDE.md)

## Why

THJ, 2026-11-20, after the reset became fun: make the Cyclone more convenient to control. Code map (Explore, 2026-11-20): nothing on the board can take a click except `PlayerController`; no per-use AP waiver exists; Mark's Command and `AEffectCommand` accept units only.

## Goal

1. Clicking the Cyclone (player's turn, Lucy's Steer usable) selects Lucy and opens the Steer's target selection.
2. Selecting the Steer (button, hotkey or click) makes the Cyclone pulse.
3. Steer cooldown 0; the first Steer each family turn costs no AP (switchable), later ones 1 AP.
4. Mark's Command can steer the Cyclone with the Steer's rules, on Mark's cost and cooldown.

## Acceptance criteria

- [ ] Click on the Cyclone's cell in UnitSelection or ActionSelection (any unit selected or none): Lucy becomes selected, the Steer is the selected ability, its range and preview show. Only when Lucy's Steer is `Active` (cooldown 0 ticks, Lucy has AP, Cyclone steerable) and no action is in progress, no reactive interrupt, no input lock. Otherwise the click behaves as today.
- [ ] In another ability's target selection, a click on the Cyclone's cell that is a legal target of that ability does what it does today; only an illegal click goes to the Cyclone hook (then: switch to Lucy's Steer if usable, else nothing new).
- [ ] Entering the Steer's target selection (any route) plays one pulse on that Cyclone: scale bump (serialized, start 1.15 over 0.15 s and back) plus a chevron flare; repeated entries (target undo) don't stack.
- [ ] Steer: cooldown 0. With the checkbox `firstSteerFreeEachTurn` on (default), the first Steer completed in each of Lucy's family turns spends 0 AP; every later Steer that turn spends 1 AP. Off: every Steer 1 AP. The AP preview on hover shows the real cost. Lucy still needs AP > 0 to be selected or to Steer (as today).
- [ ] Mark's Command: the Cyclone can be picked as the first target (when Mark's Command is usable and a Cyclone is on the board); the second step offers exactly the Steer's stops from the Cyclone (`CycloneSteerPlanner`); the Steer preview shows (route, hits, knock ghost, pulls, damage). Executing runs the same Steer (hits on the way, knock, Whirl), credited to Lucy's cast; Mark pays his Command (1 AP, cooldown 1); Lucy's Steer cooldown, free-Steer state and AP are untouched. Command's Weak doesn't apply to the Cyclone.
- [ ] An AI-controlled Lucy or Mark never uses any of this (as today).
- [ ] All EditMode tests pass; full suite after each core chunk. AI regression not needed (no AI content), unless a chunk touches AI code.

## Scope

In: the three core hooks, the click handling and pulse on the Cyclone, the free first Steer and cooldown 0, Mark's Command steering, texts (Steer description; Mark's Command description gets one clause), tests.
Out: route cycling with Space (backlog), AI use, any change to the Steer's rules, the Command's unit behaviour, numbers.

## Touches

Systems: **core** `PlayerController` (new partial), `FactionControllerBase` (target selection and cost), `FactionPhaseState` (cost), possibly `APConsumer` (zero-cost record for undo), `CombatLevelUIManager` (AP preview reads the override); new core interfaces. Feature: Lucy's Cyclone files, Mark's Command preset (new effect added), Lucy's Steer preset.
USPs: Family Roles neutral; Synergies: Mark + Lucy combo (new); Duos neutral.
Docs: GDD `lucy.md` LU-6 (cooldown 0, free first Steer, click), `mark.md` (Command steers the Cyclone), `family-systems.md` if combos are listed; `tech/core-systems.md` (three hooks); glossary (narrative) if "Command" text changes.

## Approach

Order: the two small pairs first so THJ can feel them, the big Command pair last. Core chunks are their own commits and get their own review and a full suite run (D-575, D-577).

### K1. Core: planted entities can take a click (opus, own review, full suite)
- New core interface (e.g. `IClickablePlantedEntity` in `Core/Entities/Runtime/`): `bool TryHandleClick(FactionControllerBase controller)`; returns true when it consumed the click.
- `PlayerController` (new partial, e.g. `PlayerController.PlantedClick.cs`): in `HandleGridCellSelection`, after the existing early returns and before the state branches, if `cell.PlantedEntity is IClickablePlantedEntity` and the state is UnitSelection or ActionSelection, or TargetSelection where the cell is not a legal target of the active ability (`IsLegalAbilityTarget` false), call it; on true, return without further handling. Minimal edit in `PlayerController.cs` itself (one call).
- Tests: a fake planted entity consumes clicks in the allowed states, is never asked when the cell is a legal target, and nothing changes when no planted entity implements it.

### K2. Core: per-use AP cost override (opus, own review, full suite)
- New core interface on effects (e.g. `IAbilityCostOverride` next to `AEffectBase`): `bool TryGetActionCost(RuntimeAbility ability, out int count)`; first effect that answers wins.
- `FactionControllerBase` `TakeActionState` completion: when an override answers, use its count (0 = no AP spent) instead of 1. Make sure 0 is recorded so `CheckForActionReversion` / `RevertConsumption` stays consistent (no extra pop). `CombatLevelUIManager.ShowAbilityAPPreview` shows the overridden cost.
- `Active` keeps requiring AP > 0 (unchanged).
- Tests: an ability with an override of 0 spends nothing and its undo reverts nothing extra; no override = unchanged.

### K3. Feature: click to Steer and the pulse (sonnet, review with the feature)
- `CycloneEntity` implements `IClickablePlantedEntity`: if the controller is the player's and is Lucy's faction controller, Lucy's Steer is `Active`, no action in progress: `TrySelectUnit(lucy)`, then `HandleAbilitySelection(steer)`, then the bar's selected-ability highlight (`CombatLevelUIManager.ShowSelectedAbilities`); return true. Otherwise false.
- Pulse: `CycloneSteerPreview`'s entered-target-selection handler (already identifies this Cyclone's Steer) asks `CycloneCrossView` for a new `PlayPulse()` (serialized scale and seconds, chevron flare); ignore re-entries while a pulse runs.
- Tests: click conditions (usable / on cooldown / no AP / AI Lucy / action in progress), the pulse plays once per entry and not on re-entry mid-pulse.

### K4. Feature: cooldown 0 and the free first Steer (sonnet, review with the feature)
- `AEffectCycloneSteer` implements `IAbilityCostOverride`: serialized `firstSteerFreeEachTurn` (default true); 0 when on and no Steer completed yet this family turn for that Lucy, else no override (normal 1 AP). Per-turn state lives on the Cyclone or a per-caster record reset at Lucy's phase tick (no new statics; if one is needed, `PlayModeStaticReset` hook). A Steer refused or cancelled doesn't use the free one.
- `Lucy_Ability_Steer.asset` cooldown 0 (THJ already set it in the editor, unsaved: make it the saved value) and `CycloneSteerSetup` constant; update `LiveSteer_CostsOneAP…` and related tests.
- Description (working): "Glide the Cyclone up to 3 cells, through enemies, hitting each. An enemy where it stops is knocked onward and hit. Then it Whirls. The first Steer each turn is free."
- Tests: first free, second 1 AP, next turn free again, checkbox off = always 1 AP, Mark's Command steering (K6) doesn't use or reset it.

### K5. Core: a planted entity as a Command target (opus, own review, full suite)
- New core interface (e.g. `IAbilityTargetablePlanted`): `bool IsTargetableBy(RuntimeAbility ability)` and `bool TryCollectNextTargetCells(RuntimeAbility ability, int stepIndex, List<GridCell> cells)`.
- `FactionControllerBase` target selection: for a first target of type CellOccupant, a cell whose occupant is empty but whose planted entity implements it and answers `IsTargetableBy` true is accepted, with that entity as the target (range, legality, `SetObject`, hover). For the next target, if the previous target implements it and returns cells, those cells are the range (instead of the relative PathWalkable range).
- `AEffectCommand` must complete cleanly (call its completion) when the first target isn't a `GUnit`, so another effect on the same ability can act. Verify how effects complete; the smallest safe change.
- Tests: Command-like test ability picks a fake targetable planted entity; next-target cells come from it; a non-implementing planted entity is still refused; unit targets unchanged.

### K6. Feature: Mark's Command steers the Cyclone (opus, review with the feature)
- `CycloneEntity` implements `IAbilityTargetablePlanted`: targetable by Mark's Command (identify the ability by its effect, e.g. a new `AEffectCommandSteersCyclone` present on the preset) when the Cyclone `CanBeSteered`; next-target cells = `CycloneSteerPlanner` stops.
- New feature effect `AEffectCommandSteersCyclone` added to `Mark_Ability_Attack_Command.asset` (small YAML edit or an editor setup tool): on `[CycloneEntity, GridCell]`, plan and run the Cyclone's Steer exactly like Lucy's (same `SteerRoutine`, Whirl, credit), without touching Lucy's Steer cooldown or free-Steer state; waits until the Steer and Whirl finish. Ignores unit targets.
- Preview: `CycloneSteerPreview` also reacts to Mark's Command when its first target is the Cyclone (route, hits, knock ghost, pulls, damage); the Command's own path preview and ghost don't draw for the Cyclone.
- Mark's Command description: add "It can also steer Lucy's Cyclone." (working text).
- Tests: Command picks the Cyclone; stops equal the Steer's; executing runs the Steer and Whirl; Lucy's Steer state untouched; Mark spends his Command cost; AI Mark never targets it.

## Risks

- **Core changes** (K1, K2, K5): additive interfaces, no signature changes; each reviewed alone, full suite each. Record them in `tech/core-systems.md`.
- **Click order:** the hook runs only where the click would otherwise be ignored or select nothing; legal targets keep priority.
- **Undo:** a free Steer records 0 AP; a later undo must not refund AP that was never spent (K2 test).
- **Statics:** none planned; per-turn free-Steer state is instance state.
- **AI thread:** the new range methods may be read in target checks; plain data only, as the Steer planner.
- **Event re-entry:** the target-selection event fires on every re-entry; the pulse guards against stacking.
- **Command preview:** the Command's ghost and path preview assume a unit; K6 must suppress them for the Cyclone without changing them for units.
- **Other branches:** none; the Cyclone exists only on `thj/cyclone`.

## Gates

- Compile and covering fixtures per chunk; full EditMode after K1, K2, K5 and at the end.
- Review: K1, K2, K5 each alone; K3, K4, K6 together at the end.
- Play check: yes, THJ (click, pulse, free first Steer, Mark's steer).
- Docs after the play check: GDD Lucy LU-6, Mark's Command, `tech/core-systems.md`, glossary/narrative texts.
- Commits: K1, K3 (after K1), K2, K4, K5, K6, each its own; the Steer asset and description go with K4, Mark's preset with K6.
