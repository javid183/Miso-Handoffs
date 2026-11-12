# Report: Cyclone redesign, C3 (Steer and Gust)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer (opus)    Branch: thj/cyclone
Outcome: done (THJ play check pending). One small additive core touch (the Steer's target range), flagged below.

## Fix round (after the C3 review)

THJ approved the core hook (D-539); it ships as its own commit D1. Review: `reports/cyclone-c3-review.md` (FIX).

1. **Must fix: the Steer button was greyed for the rest of the turn after a cast.** The cast ends while its first Whirl is still running, and nothing refreshed the bar when the Whirl ended.
   - New partial `Cyclone/CycloneEntity.Ready.cs` with `event ReadyChanged` and `NotifyReadyChanged()`.
   - It is raised at the end of every Whirl, at the end of every Steer (after its Gust) and on Dispose.
   - It refreshes the shown unit's panel (`CombatLevelUIManager.Instance.RefreshUnitControlPanel(SessionLogs.Instance.CurrentSelectedUnit)`). The bar's existing swap check then rebuilds the button when needed.
   - The cast still doesn't wait for the whole Whirl.
   - Super Time is covered: its cast runs the same first Whirl, whose end raises the refresh.
   - Test: `TheEndOfAWhirlOrASteer_SaysTheCycloneIsReady`. The refresh itself is a play check.
2. **Should fix 1 (coordinator): an AI-controlled Lucy never gets the Steer.**
   - `AEffectCycloneSteer.CheckActivationFeasibility` refuses when the owner's faction controller has `ControllerHandler.AI` (`AEffectCycloneSteer.IsAIControlled`). Plain references only, so it is worker-safe.
   - Test: `SteerEffect_IsNeverAvailableToAnAIControlledLucy` (no controller and a Player controller pass; an AI controller refuses).
   - **Correction:** the first build's report said an AI Lucy's candidate cells were filtered by the Steer rule. That was wrong: `AIUnitBrain.GetAbilityCandidateTargets` never calls `CheckTargetSelectionCondition`. Now moot.
3. **The test assertion that couldn't fail was dropped.** It compared the cast's cooldown with a fresh object. The remaining assertion is relabelled: after one use the Steer waits one family turn.
4. **`TargetSelectionRange.TryGetProvided` test:** `TargetSelectionRange_SuppliedByTheSteerOnly_AroundTheCyclone`. False for the cast and for null; true for the live Steer, with exactly the cells the Cyclone can reach and nothing around Lucy.
5. **Main-thread-only doc** on `ITargetSelectionRangeProvider` and `TryGetProvided`.
6. **`|| IsSteering` guards** in `StartWhirl` and `OnTurnEnding`. Test: `WhileSteering_NoWhirlStarts`.
7. **Optional preview item, not done.** `Clear()` already hides only the ghosts of units this preview drew. Telling whether another preview has since redrawn the same unit's ghost would need `GUnit`'s private ghost state (a core change), so I left it. The only preview that ghosts an enemy is the Masher's, and Masher is Immovable, so it is never in the Gust plan.

Files touched in this round:
- New: `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Ready.cs` (+ .meta).
- Edited in `Features/Player/Lucy/Scripts/Cyclone/`: `CycloneEntity.cs`, `CycloneEntity.Whirl.cs`, `CycloneEntity.Steer.cs`, `AEffectCycloneSteer.cs`.
- `Core/Systems/AbilitySystem/Effects/Runtime/ITargetSelectionRangeProvider.cs` (doc comment only).
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs` (now 17 cases).

**EditMode after the fix round:** 1990 run, 1989 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`: 714 checks, still **43** inner failures, not re-baselined. Compile clean.

The sections below describe the first build; where the fix round changed something, the fix round wins.

## Button swap: the design choice

**A second ability, shown in the Cyclone button's place.** `Lucy_Ability_Steer` is a new ability on Lucy (appended to `Unit_Lucy`'s list). The ability bar asks `CycloneButtonSwap` what goes in each slot: while her Cyclone is out, the cast's slot shows the Steer. The Steer has no slot of its own. So the button keeps its position and its number key, and changes icon-less in place (placeholder: same icon, title "Steer").

Why not a mode on the existing ability:
- `RuntimeAbility._ActivateAbility` sets the cast's cooldown on every activation. A Steer through the cast would restart cooldown 4. Avoiding that needs a core change in `RuntimeAbility`, and there's no public setter to restore a partly run cooldown.
- Title, tooltip, cost and the once-a-turn limit would all need runtime overrides.
- With a second ability, the ability system gives everything for free: 1 AP (`apConsumptionType` Singular), once a turn (cooldown 1, ticked at the family phase start like every ability, and shown on the button as "1"), its own title and tooltip. The cast's cooldown is a different counter and is never touched.

The Steer effect's activation check is true only while her Cyclone is out and ready (not whirling, steering or moving pulled units). The cast's existing check is false while the Cyclone is out (C1a). So even outside the bar, only one of the two can be used at a time.

## What changed

Paths under `miso/Assets/_Project/`. New files are LF, no BOM. Edited files keep their endings: `FactionControllerBase.cs` keeps its BOM, the others have none.

### Core (additive; needs THJ's OK per the brief)
- `Core/Systems/AbilitySystem/Effects/Runtime/ITargetSelectionRangeProvider.cs` (+ .meta, new): interface `ITargetSelectionRangeProvider` and a static helper `TargetSelectionRange.TryGetProvided(ability, owner, out cells)`. An effect can supply its ability's target cells. With no such effect, the helper returns false.
- `Core/Interactions/Runtime/FactionControllerBase.cs`: `ComputeAbilityRangeCells` gets one check at the top of the Targeted branch: if an effect supplies the range, use it. Otherwise nothing changes; no ability had such an effect before.
  - Why it was needed: the range highlight and the in-range part of `IsLegalAbilityTarget` are always computed around the caster (or a proxy *unit*). The Steer targets cells around the Cyclone. Without this, the highlight would be a wrong diamond around Lucy.
  - Size: 4 lines plus 1 new file. The AI's own range code is not touched (see risks).

### Lucy feature (`Features/Player/Lucy/Scripts/Cyclone/`, each + .meta)
- `CycloneSteerRules.cs` (new): pure rules.
  - Up to 3 straight steps (never diagonal) over crossable cells.
  - Crossable: not a wall (no cell), no enemy of the caster, no planted walk blocker. The family, allies, neutrals and decoys can be crossed, and so can non-blocking hazards.
  - It ends only on a valid cast cell: no unit, nothing stashed, no planted entity.
  - Breadth-first in a fixed order, so the path is always the same.
  - Worker-safe: `ReferenceEquals` and plain slots only.
- `AEffectCycloneSteer.cs` (new): the Steer effect.
  - Activation: her live Cyclone `CanBeSteered`.
  - Target check: a path exists.
  - Range provider: the cells the Steer can reach from the Cyclone.
  - Apply: starts `CycloneEntity.TrySteer` and stays `IsInProgress` until the Gust ends. It waits on a coroutine running on Lucy, the same pattern as the cast's pull hold.
  - Refused cases log a warning, never silently.
- `CycloneEntity.Steer.cs` (new partial):
  - `TrySteer` / `IsValidSteerPath` / `SteerRoutine`. The routine hides the cross, glides cell by cell on game time (new serialized `steerSecondsPerCell` = 0.15, default value only; the prefab isn't edited), moves the Cyclone from its old cell to its new one in a single frame, redraws the cross, then runs the Gust.
  - `GustRoutine`: the Streaks beat, then `CycloneWhirlPlanner.PlanPulls` from the new cell with the Whirl's `IsPullable` and `TryPull`. Nothing else: no hit, no report, no swell, no burst. The streaks stay up at least 0.35 s, so a Gust that pulls nobody still reads. Then the log line and the Done beat.
  - `CanBeSteered`.
- `ICycloneSteerSteps.cs` + `CycloneSteerSteps.cs` (new): the Steer's contact points with the game: position on a cell, game delta time, relocate (`UnplugEntity` then `PlugEntity`) and the log. The log is the synergy note "Gust · Lucy: pulled N", like the Whirl's line.
- `CycloneSteerPreview.cs` (new, added at run time like the cross and pips views). While the player aims the Steer and hovers a reachable cell, it shows:
  - the path, with the grid's own path arrows;
  - a faint copy of the Cyclone on the landing cell;
  - for every enemy the Gust would move: its ghost (`GUnit.ShowGhostAt`) and the push preview's step arrow on the cell it leaves.

  The Gust is planned by the same Whirl planner, from the landing cell, with the current cell counted as free. Drawings are re-applied each frame while shown, because the player's hover code clears shared cell overlays.
- `CycloneButtonSwap.cs` (new): `IsSteer`, `ShownFor`, `ShowsSteer`, `FindSteer`.
- `CycloneEntity.cs`:
  - `Initialize` adds the Steer preview.
  - `Dispose` also defers while steering, and unbinds the preview.
- `CycloneEntity.Whirl.cs`: the pull-start loop moved into `StartPulls(plan, steps, started)`, shared with the Gust. Same behaviour; the Whirl tests pass unchanged.
- `CycloneWhirlPlanner.cs`: optional `vacating` cell on `PlanPulls` / `IsLandable`. The preview treats the Cyclone's current cell as free; default null, so the Whirl is unchanged.
- `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`: the split reads the cell once (`Cell`), returns if there is none, and uses that cell for the clones and the landing. With the single-frame relocate the cell is never empty anyway; this is the belt-and-braces guard.

### UI (`Features/UI/Panels/Scripts/`)
- `AbilitiesBarHUDUI.CycloneSteer.cs` (+ .meta, new partial). It remembers whether the bar was built with the Steer. On the next `Refresh` after that changes, it rebuilds the bar for the shown unit. A cast or Steer completion refreshes the bar, and so do AP changes and the run handler.
- `AbilitiesBarHUDUI.cs`: two small hunks.
  - `Populate`'s loop asks `ShownInPlaceOf`. The level lock and quiver checks still apply to the slot's own ability (the cast), so a locked Cyclone also hides the Steer.
  - `Refresh` starts with `TryRebuildForCycloneSwap()`.

### Data (created by the new editor tool, run once through the Unity MCP)
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs` (+ .meta): `Tools/Lucy/Apply Cyclone Steer Setup`. Re-runnable; it only creates what is missing.
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer_Effect_Steer.asset` (+ .meta): the Steer effect, reach 3.
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset` (+ .meta): a copy of the Cyclone ability.
  - Title "Steer", 1 AP, cooldown 1, radius 3, the Steer effect only.
  - No AI score graph, `actualTargets` off, not upgradable, not introducible.
  - Same icon and the cast's stat block (unused).
- `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`: a 9th ability entry, a copy of her Cyclone entry. Same `Cyclone` animation state, activation frame 10, the same SFX event, `initialCooldown` 0, preset Steer. The diff is +52/-2: array size 8 → 9 and the stale `data[8].preset` override now points to the Steer.

### Tests
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs` (+ .meta, new, 13 cases).
- `Features/Player/Lucy/Scripts/Editor/CycloneTestGrid.cs`: an optional `holes` parameter (cells left out, as walls). Existing callers are unchanged.

## Acceptance criteria (C3)

- [x] **While a Cyclone is out, the button is Steer; after it fades, the cast again.**
  - Test `CycloneButton_IsSteerWhileTheCycloneIsOut_AndTheCastAgainAfterItFades` checks: no Cyclone shows the cast; out shows the Steer in the cast's slot; after three family turn starts it fades and shows the cast again. Both effects' activation checks flip with it.
  - The bar rebuild itself is a **play check**.
- [x] **Steer costs 1 AP, once per turn, doesn't start the cast cooldown:** `LiveSteer_CostsOneAP_OnceATurn_AndIsSeparateFromTheCast`.
  - It checks the live preset: Singular AP, cooldown 1, radius and reach 3, the Steer effect only, no follow-up target report.
  - The cast keeps cooldown 4. The Steer's `SetCoolDown` leaves the cast's counter at 0.
  - `Unit_Lucy` has both entries.
  - AP spend in a level is a play check (the standard `ConsumeActionCost` path).
- [x] **Up to 3 cells, four-way:** `Steer_ReachesUpToThreeStraightSteps` (3 steps and a corner are fine, 4 is refused, straight steps only).
- [x] **Not through walls or enemies; through the family:**
  - `Steer_CantCrossEnemiesOrBlockingEntities_CrossesTheFamily`: enemy and rock in a corridor refuse; the family and an ally are crossed.
  - `Steer_CantCrossAWall_ADetourCountsItsSteps`: a missing cell; the 4-step detour is refused at reach 3 and found at reach 4.
- [x] **Ends on an empty cell, no planted entity, no unit:** `Steer_RefusesPlantedAndOccupiedCells_ButCrossesAHazardThatDoesntBlock`.
- [x] **Target cells follow the Cyclone, and it's not available while busy:** `SteerEffect_AvailableOnlyWhileHerCycloneIsOutAndReady_TargetsCellsAroundTheCyclone`.
- [x] **Gust: pull only, once, at the destination, no hit, no report, nothing along the path:** `Steer_GustPullsOnceAtTheDestinationOnly_NoHitNoReport`.
  - One pull from the new arms; nothing is pulled from the old arms or beside the path.
  - No hit, 0 reports, no Whirl line, one Gust line ("pulled 1").
  - Beats are exactly Streaks then Done.
  - It plants on the new cell and frees the old one.
- [x] **Pull order and Immovable as the Whirl:** `Gust_PullOrderAndImmovable_AreTheWhirls`. The Gust's pulls equal `CycloneWhirlPlanner.PlanPulls` for the same board: Immovable isn't pulled, a pull into an occupied cell doesn't happen, diagonals are left out.
- [x] **The pull raises `unitEndMoving` (Watch on Lucy's turn):** by construction, through the same pusher `TryMoveTo` as the Whirl (C1b). The Steer ability stays in progress until the Gust's pulls land, so Family Roles answer after Lucy's action. **Play check** with Linda in the lane.
- [x] **Steer preview: path, landing cell, a ghost for every enemy the Gust moves:** `CycloneSteerPreview`.
  - The plan is shared with the real Gust. Test `Steer_GustCanPullIntoTheCellTheCycloneLeft_AndThePreviewPlansTheSame`: the preview's plan, with the vacated cell, matches what the Gust then does.
  - The drawings are a **play check**.
- [x] **The scatter never reads a null cell mid-move:** `DuringASteer_TheCycloneAndItsScatterAlwaysHaveACell`. Every frame of a 3-cell Steer, the Cyclone and `scatter.Cell` are non-null and in play. There is also a guard in `OnTriggerEnter2D`.
- [x] **Pips and cross follow:**
  - The pips are children of the Cyclone (they move with it).
  - The cross is hidden during the glide and redrawn on the new cell (`_cross.Show`). Drawing is a **play check**.
- [x] **AI danger snapshot picks up the new cell:** `AfterASteer_TheAIsDangerIsTheNewCross`. After a Steer, `AIEndOfTurnDanger.Snapshot` returns exactly the new cell's arms and none of the old. The snapshot is taken per AI job (C2), so the next job sees it.
- [x] **Masher counter unchanged:** verified by reading the code. The Masher counter's inputs are `onUnitDamageDone`, `onSynergyTriggered` (Duo id only), `onAbilityEffectPerformedOn` and `abilityPerformed` for Duos.
  - A Gust calls no `Report` (tested: 0 reports) and deals no damage.
  - The Steer ability has `actualTargets` off and targets a cell, so no effect-performed event names a unit.
  - Masher is Immovable, so a Gust never pulls it.
  - No Masher code changed.
- [x] **Dispose during a Steer waits:** `ADisposeDuringASteer_WaitsForItsEnd`.

**EditMode suite:** 1986 run, 1985 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not re-baselined.
- **Its inner count moved 42 → 43 (checks 713 → 714).** The one new entry is `abilities.unexpected …/Lucy_Ability_Steer.asset: new ability is not in today's baseline`. `abilities.count` was already failing.
- The other 42 are the same as before.

Compile clean, with no new warnings.

## Save reset

No.

## Decisions I made

- The button swap is a second ability placed in the cast's slot (reasons above).
- Once a turn is the ability's own cooldown 1, not a flag on the Cyclone. The button shows "1" after a Steer, and the cooldown clears at the next family turn start.
- The Cyclone stays planted on its old cell during the glide and moves to the new cell in one frame. So it always has a cell, and an arrow that met it mid-glide would split from the old cell. Moving it cell by cell would mean planting on cells that already hold a planted hazard, and plug events per step. In practice nothing else acts during Lucy's Steer.
- The Gust shows its streaks even when it pulls nobody (at least 0.35 s), so the player sees it happened.
- The Gust doesn't wait for reactions itself. Like the cast, the Steer ability stays in progress until the pulls land; the reactions (Watch) follow when Lucy's action completes.
- Preview: I reused the Whirl planner, not `CollectPushPreview`, because the Gust is the Whirl's own pull, not a vortex. The visuals are the push preview's step arrow plus `GUnit` move ghosts.
- The Steer entry on Lucy copies her Cyclone entry: the same cast animation, and the Steer starts at its frame 10 with the Cyclone SFX. Placeholder.
- The reach is the effect's field (3). The preset's radius is also 3 but only for consistency; the range comes from the effect.

## Needs THJ

1. **Answered: approved by THJ (D-539).** **Core touch (additive):** `ITargetSelectionRangeProvider` (new file) and the 4-line check in `FactionControllerBase.ComputeAbilityRangeCells`. It is needed so the Steer's range highlight and in-range check are around the Cyclone, not around Lucy. With no effect implementing it, behaviour is identical. Recommend: approve, in its own commit (1 below).

## Docs to update

- `tech/core-systems.md` (coordinator):
  - Effects row: `ITargetSelectionRangeProvider` / `TargetSelectionRange.TryGetProvided`.
  - Faction controllers row: `ComputeAbilityRangeCells` uses an effect-supplied range when there is one.
- GDD `characters/lucy.md` (designer, C5): Steer as built. 1 AP, cooldown 1 (once a turn), 3 straight steps, crosses the family, allies and non-blocking hazards; not walls, enemies or blocking entities; lands only on an empty cell. Gust as built: streaks, pull only, "Gust: pulled N".
- AI regression fix session: the new `Lucy_Ability_Steer` preset belongs in the ability catalog (no evaluator). Count now 43.

## Risks and loose ends

- **Play checks:**
  - the bar swap after the cast and after the fade at the family turn start (Lucy shown);
  - Steer AP spend and the "1" cooldown on the button;
  - the range highlight around the Cyclone;
  - the cursor refusing other cells;
  - the preview (path arrows, landing copy, ghosts and arrows);
  - the glide and the cross redraw;
  - the Gust streaks and the log line;
  - Watch firing after a Gust pull;
  - an enemy pulled onto spikes by a Gust.
- **Placeholder text** (not tagged in the asset, per conventions): Steer title "Steer"; description "Move the Cyclone up to 3 cells, not through walls or enemies. It then pulls enemies on its arms one cell in. Once a turn." The icon is the Cyclone's. The narrative pass is C5.
- **AI-controlled Lucy** (dev auto-player): refused by the Steer's activation check since the fix round. The AI never sees the Steer as available.
- **Memory 4 / scripted casts:** if a level's ability lock hides the Cyclone, the Steer is hidden too. If the Cyclone isn't locked and Lucy is playable after a scripted cast, the Steer appears. Worth a look in the Memory 4 check (C5).
- The bar rebuilds on the next `Refresh` after a change. If some path changes the Cyclone without a following refresh (Super Time cast while Lucy is shown?), the swap shows on the next refresh or selection. Play check.
- Relocation uses `GridCell.PlugEntity`, whose fallback slides an entity to the nearest free cell when the plug fails. The Steer checks the end cell right before relocating and otherwise goes back to its start, so the fallback isn't reached.
- If the Cyclone object were destroyed mid-Steer (scene unload), the Steer effect's wait ends at once (`cyclone` null), so the ability doesn't hang.

## Proposed commits

Full order: **A, A2, B, D1, C1 1–8, C, D2, D3**, with whole files per commit. This builds at every step: D1 adds the core interface that the Steer effect implements, and C1 commit 3 carries the inert Steer code.

- **A, A2, B:** as in `cyclone-c2.md`.
- **D1.** `feat(core): an ability effect can supply its own target cells, used by the player's range highlight and target check` (**core**, approved by THJ): `Core/Systems/AbilitySystem/Effects/Runtime/ITargetSelectionRangeProvider.cs` (+ .meta), `Core/Interactions/Runtime/FactionControllerBase.cs`. Inert on its own.
- **C1 1–8:** as in `cyclone-c1b.md` (2b folded into 2), with one change to commit 3.
  - **C1 commit 3**, with a wider message: `feat(lucy): the Cyclone stays where it is cast, whirls on cast and at the end of each enemy turn (pull one cell in, then 3x on touching enemies), shows its cross and pips, and casts only on an empty cell; carries the Steer and Gust code, unused until Lucy has the Steer ability`.
  - It takes the whole `Features/Player/Lucy/Scripts/Cyclone/` folder, each file with its .meta, **except `CycloneEntity.AIDanger.cs`** (+ .meta), which goes in C.
  - That includes the C3 files: `CycloneSteerRules.cs`, `AEffectCycloneSteer.cs`, `CycloneEntity.Steer.cs`, `CycloneEntity.Ready.cs`, `ICycloneSteerSteps.cs`, `CycloneSteerSteps.cs`, `CycloneSteerPreview.cs`, `CycloneButtonSwap.cs`.
  - The Steer code is inert here: no ability uses the Steer effect, so the preview never sees a Steer, `IsSteering` stays false, and `vacating` defaults to null.
  - The rest of commit 3 is unchanged (setup tool, `Cyclone.prefab`, the cast assets, the pusher). It depends on D1.
- **C:** as in `cyclone-c2.md`.
- **D2.** `feat(lucy): while her Cyclone is out, Lucy's Cyclone button is Steer: 1 AP once a turn, up to three straight cells through the family, then a Gust pulls enemies on its arms one cell in, with an aim preview` (plain; depends on C1 3):
  - `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`
  - `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs`, `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.CycloneSteer.cs` (+ .meta)
  - `Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs` (+ .meta)
  - `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset`, `Lucy_Ability_Steer_Effect_Steer.asset` (+ .meta each)
  - `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`
- **D3.** `test(lucy): Steer rules, Gust, button swap, ready refresh, scatter and AI danger after a Steer` (plain; depends on D2): `Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs` (+ .meta). The `CycloneTestGrid.cs` `holes` change rides whole in C1 commit 4.

Don't stage THJ's files (PreloadScreen, ProjectSettings, the TMP fallback font).

## Other branches

`thj/home-test` lacks the redesign; it merges later with the rest.

## How to see it

1. Open a level with Lucy and enemies (a Trail fight). Cast the Cyclone (Lucy's Cyclone button).
2. After the cast resolves, the same button is now **Steer** (tooltip "Steer"). Same slot, same number key.
3. Click Steer. The highlighted cells are around the Cyclone (up to 3 straight steps), not around Lucy. Cells with units or spikes and cells behind enemies or walls aren't highlighted; cells behind John or Linda are.
4. Hover a highlighted cell with an enemy 2 cells from it in a straight line. You see:
   - the path arrows;
   - a faint Cyclone on the landing cell;
   - the enemy's ghost one cell closer, and an arrow on its cell.
5. Click. Lucy plays her cast animation, the Cyclone glides there, the cross redraws on the new cell, and the arms flash (streaks only, no swell, no ring, no numbers). The enemy slides one cell in. The combat log shows "✦ Gust · Lucy: pulled 1".
6. The button now shows cooldown 1; 1 AP was spent. Next family turn it's usable again. The cast's own cooldown wasn't touched.
7. With Linda in the row or column where the enemy lands: Watch fires after the Gust.
8. End turn: the Whirl happens at the Cyclone's new cell, and enemies avoid its new arms.
9. When the Cyclone fades (round 4 start), the button is the Cyclone cast again (cooldown 1 left).
