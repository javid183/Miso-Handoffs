# Lucy's Cyclone redesign (Pulling Gale v2): tech plan

Size: L    Tier: 3 (core: grid walking, damage reporting, turn switch, AI)    Assigned to: `miso-implementer` (opus for C1–C4, sonnet for C5)
Branch: `all` (code); where it's built is a question for THJ (Q5)
Status: **waiting on THJ** (planned 2026-11-11 at THJ's request: "just plan for it"; nothing dispatched)

## Why

Players can't predict the Cyclone: it moves by itself toward hidden targets, loses life about 3 times a round, hits at two unclear moments, and blocks everyone. THJ picked direction A, Pulling Gale (2026-11-05), and answered the review on 2026-11-10. Design: `design/cyclone-redesign.md` (v2). Closes D-055 (Q21 + S10) and the bug `cyclone-move-damage-events` (status Inbox, 2026-11-09). Code facts: Explore, 2026-11-11 (summarised below).

## Goal

The Cyclone holds a cross: it never moves on its own, Whirls (pull 1, then hit 3×) on cast and at the end of each enemy turn, lasts 3 enemy turns, can be Steered by Lucy, blocks enemies (bodies and ranged lines) and lets the family pass through, and every hit is reported like any other damage.

## Acceptance criteria

C1 (anchored Cyclone + Whirl)
- [ ] The Cyclone never moves by itself; no target choice, no random walk.
- [ ] Life: 3 pips, one lost at the start of each family turn, none on any other turn start; pips shown on it. Cast in round 1 → Whirls at the end of enemy turns 1, 2, 3, fades as round 4 starts.
- [ ] Cast: 1 AP, range 3, cooldown 4, one Cyclone at a time, only on an empty cell with no planted entity and no unit; the preview refuses others. Lucy's Super Time cast picks only valid cells (no silent fail).
- [ ] Whirl on cast and after all enemies have acted, before the turn passes: pull each non-Immovable enemy on an arm (2 cells, straight only) 1 cell toward it if free, nearest first; then 3× on each enemy on a touching cell (large units if any cell touches). Pulls raise `unitEndMoving` (Watch reacts); hazards on the landing cell fire.
- [ ] Whirl damage reaches `onUnitDamageDone` (mission stats, Wrath/Blood Debt, Atman Barrier, barks, AP providers) exactly once per hit; it doesn't trigger Lucy's follow-up role; the sisters' tally counts a Cyclone kill once.
- [ ] Enemies can't target the Cyclone (`isTargetable` off).
- [ ] The cross (wind lines on the arms, "3 ×" on touching cells) is drawn while it's out; the Whirl has its swell → streaks → burst beat; the combat log says "Whirl: pulled N, hit M".
- [ ] Masher/Queen AOE telegraphs, hazards, Toba's wall and relics behave exactly as before (lifetimes unchanged).

C2 (who walks through it)
- [ ] Enemies can't enter or path through the Cyclone's cell; a push or pull into it stops on the cell before.
- [ ] The family, allies, neutrals and decoys path through it but can't end a move on it.
- [ ] Linda's grounded arrow still never lands on it (D-252, LI-6 unchanged).
- [ ] The AI treats the cross as dangerous ground: takes another route when one exists; walks in when that reaches a target it can attack this turn; otherwise waits outside the arms. The family's own move range is unchanged.

C3 (Steer and Gust)
- [ ] While a Cyclone is out, Lucy's Cyclone button is Steer: 1 AP, once per turn, up to 3 cells four-way, not through walls or enemies, through the family; must end on an empty cell with no planted entity.
- [ ] After a Steer, a Gust at the destination: pull only, no hit, once.
- [ ] Steer preview: path, landing cell, a ghost for every enemy the Gust moves.
- [ ] An arrow (Tempest Bloom) never meets a Cyclone mid-move with a null cell.

C4 (enemy ranged attacks)
- [ ] An enemy ranged attack isn't allowed when the grid line from shooter to target crosses the Cyclone's cell: the AI doesn't pick it, execution refuses it, the threat preview and the enemy intent preview don't show it.
- [ ] Ranged enemies move to a cell whose line is clear.

C5 (checks, texts, docs)
- [ ] Command Shield Dash doesn't fire on a pull; Watch fires on pulls on Lucy's turn (Gust) and at the end of the enemy turn (Whirl), within its own limits.
- [ ] Cyclone Power and Howling Gale texts reworded to the Whirl; Howling Gale's Weak applies on Whirl hits.
- [ ] Hearth Memory 4 (Bloom stage, cast at (3,4)) and the Lucy memory still play as intended under the new rules (THJ play check).
- [ ] Every EditMode test passes except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (it will move; never re-baselined here).

## Scope

In: the Cyclone entity, ability and effects; grid walk exception; damage report; Whirl turn-end hold; AI cross danger and line-of-fire; Steer/Gust; previews; tally listener; texts; GDD and chunks.
Out: Trailing Gale and Second Cyclone run upgrades (Q2); deleting the dead Linda-folder Cyclone copies (they're named in the AI test catalog; flag only); the Duo damage bug (D-451) unless Q3's option (b) is chosen, which fixes its reporting path too; any AI regression re-baseline.

## Touches

Systems (core marked): `GridCell` / `GridActions` (core), `OnGridEntity` (core, via a subclass), `AEffectVortexPull` / `AEffectPusher` / `AEffectSpawner` / `AEffectCompound` (core), `CombatLevelRunHandler` + `TurnSwitchHolds` (core), `FactionControllerBase` target checks (core), `AIUnitBrain` / `AIFactionBrain` / `AIBlackboard` (core), `PlayModeStaticReset` (core). Not core: `UtilityVariables`, `UnitThreatAnalysis`, `LucyCycloneProjectileScatter`, Synergy presenters, `SistersTallyListener`, `LucyFactionRoleHandler` Super Time cast (role handlers are core), combat log.
USPs: Synergies (Tempest Bloom better; Watch combo), Family Roles (Watch reacts to pulls; Lucy's role doesn't answer Whirls).
Docs: GDD `characters/lucy.md`, `family-systems.md`, `combat-rules.md`, `enemies.md` (designer); `design/level-chunks.md` chunks **1, 4, 7, 12, 13, 18, 24, 31** (the design lists only 4 of these; designer); `tech/core-systems.md`, `tech/combat-architecture.md` (coordinator); `design/cyclone-redesign.md` as-built note (designer); Claude Docs mirror (Lucy, Family systems, Combat rules).

## Code facts (Explore, 2026-11-11)

- **Live assets:** `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset` → spawn effect → `Features/Player/Lucy/Prefabs/Cyclone.prefab` (`OnGridEntity` + `LucyCycloneProjectileScatter`). Ability: cooldown 2, `radiusV` 4 (GDD 3), targeting Unconstrained (accepts occupied cells). Entity: TowardsUnits, TurnGeneral, move 3, life 5, `disallowWalk` 1, `isTargetable` 1. Dead copies under `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/` and `Features/Player/Linda/Prefabs/Cyclone.prefab`. Unused: `Lucy_Cyclone_PassByEffect_AttrMod`, `Lucy_Cyclone_FC_FPFill`.
- **Damage scale:** Lucy `Stat_DMG` 1 at base, so 7× = 7 HP; 3× = 3 HP per Whirl (3.6/4.2 with Cyclone Power); 4 Whirls = 12 vs a 16-HP Claw.
- **Lifetime/moves:** `Core/Entities/Runtime/OnGridEntity.cs` `PhaseTick` (:250) and `TurnGeneralTick` (:261, always subscribed at :69) are virtual. AOE telegraphs and spawned hazards also get `TurnGeneralTick`: **change the Cyclone through a `CycloneEntity : OnGridEntity` subclass, never the base.**
- **Damage attribution bug:** `AEffectCompound.cs:165` raises `onAbilityEffectPerformedOn` under Lucy's finished RuntimeAbility; `CombatLevelRunHandler.cs:806-848` buffers it until her next cast and resolves to 0.
- **Walk rule:** `GridCell.IsWalkable` (:22, can stop) vs `CheckIfUnitWalkable` (:242-259, can pass; planted `DisallowWalk` ignores faction). Smallest change: one exception in the planted clause (:258) for a new `passRelation` field on the entity, compared against `Owner.GetFaction()`; null faction (pushes, entity moves) stays blocked. Keep `disallowWalk` true (`GroundedArrowField.CanHoldArrow` reads it).
- **Pull:** `AEffectVortexPull` + `VortexPullPlanner` already do nearest-first pulls with ghosts; needs a straight-arms filter and a hand-made Immovable (`EntityState.Unmovable`) filter. `AEffectPusher.MoveEntity` raises `unitEndMoving` (:181-187) → Watch (`Unit_Linda.prefab` :2517, OnUnitEndMoving, all phases); hazards fire per step. Command Shield Dash only reacts while its Command is in flight (:252).
- **AI:** runs on a worker thread (`AIWorker.cs`); no Unity APIs. `GridCell.GetCellCost` is shared by every faction and the real walk budget: **don't use it for the cross**; put danger into AI scoring (a blackboard cell value or a `UtilityVariable`, snapshotted on the main thread). Ranged targets: `AIUnitBrain` candidate loop (:395-450) and `AIFactionBrain.PredictAllTargets` (:213); execution via `AEffectSpawner.CheckTargetSelectionCondition` (:25-49); threat preview `UnitThreatAnalysis` (:129-160, :277-291). Archer arrows are lobbed (TargetReach, `clearPathRequired` 0).
- **Turn end:** `turnEnded` fires inside `SwitchTurnIE` after the hold check (`CombatLevelRunHandler.cs:468-478`): the Whirl must register its hold before the switch; the hold watchdog is 5 s (`TurnSwitchHolds.cs`) and a Whirl + Watch may exceed it.
- **Previews:** `SynergyLanePresenter.Bloom.cs` re-reads the Cyclone each frame (Steer is fine); during a move it's unplugged, and `LucyCycloneProjectileScatter.cs:41` would read a null cell.
- **Dependents:** `SistersTallyListener.RecordEffectOutsideAbility` (:218-233) exists only for unattributed Cyclone hits and `RecordDamage` (:204) has no killed-once guard (double count risk); Memory 4's `Memory4Mark_Bloom_LucyCastsCyclone.asset` (seal at (3,4)); `GB_m2-lucy` lock + hint; Super Time cast (`LucyFactionRoleHandler.cs:237-242`). Tests naming the Cyclone: AIRegression, ArrowLandingRules, CatchReturnWiring, TempestBloomPreview, CatchReturnPreview, HearthMemoryLucy, HearthMemoryMark (+Flow), SistersTally Bloom/OutOfAbility.

## Approach

Build order follows the design (§12): never ship the lifetime fix alone; C1a and C1b are committed together after THJ's play check.

**C1a · opus.** `CycloneEntity` subclass (no self-move; one pip per family turn start; pips visual), swap it onto `Cyclone.prefab`; ability: range 3, cooldown 4, cell must be empty with no planted entity; `isTargetable` off; Super Time picks valid cells; cross drawn. Tests: life counts once a round; AOE/hazard lifetimes unchanged; cast refuses planted/occupied cells.

**C1b · opus.** Whirl: a pull effect (VortexPull with straight arms, Immovable filter, 1 cell) then the 3× hit; on cast and at the end of the enemy turn through a turn-switch hold registered before the switch (watchdog sized for Whirl + Watch). Damage reporting per Q3. Tally listener moved off the workaround (one count per kill). Beat (swell, streaks, burst), log lines. Tests: Whirl order (pull → reactions → hit), pull order and blocking, Immovable, reporting once, tally once.

**C2 · opus.** Walk exception (`passRelation`) in `CheckIfUnitWalkable`; AI cross danger in scoring (main-thread snapshot, `PlayModeStaticReset` hook). Tests: per-faction pass/stop, push into the Cyclone stops before it, grounded arrow still refused, AI route choice in three set-ups (detour / walks in to attack / waits outside).

**C3 · opus.** Steer (button swap while out, 1 AP once a turn, movement rules) and Gust (pull only at the destination), preview with ghosts (`CollectPushPreview`); scatter safe during a move. Tests: Steer refuses planted cells, Gust pulls once at the end.

**C4 · opus.** Grid line-of-fire rule as one pure helper used by the AI candidate loop, intent prediction, execution check and threat preview (worker-safe data). Tests: the line rule (straight, diagonal, adjacent), AI doesn't pick a blocked shot.

**C5 · sonnet + designer.** Watch and Command Shield Dash checks, upgrade texts, onboarding check (Memory 4, Lucy memory), GDD and chunk updates (designer), core-systems and combat-architecture (coordinator); THJ play check.

## Risks

- **Base-class spread** (`OnGridEntity`): subclass only; a test pins AOE and hazard lifetimes.
- **Whirl at turn end:** hold registered too late can't stop the switch; the watchdog may cut a long beat; `ActivatedAtThisPhase` resets on `turnEnded`.
- **Double counting** (tally, stats) if the old event and a new report both fire: one path only, tested.
- **AI thread safety:** plain snapshotted grid data; new statics get a `PlayModeStaticReset` hook.
- **Shared path cost:** never raise `GetCellCost` for the cross (shrinks everyone's moves).
- **Pull via `TryMoveTo`** skips effect guards: filter Immovable by hand; if the Cyclone dies mid-pull, the unit must not be left unplugged.
- **AI regression test** moves (its catalog names both Cyclone paths): stays known red, no re-baseline.
- **Onboarding:** Memory 4's seal and three-arm Claws assume blocking and a 7× landing; replay it. The after-Hearth levels and the challenge round being designed now assume the old Cyclone (Q4).
- **Saved data:** none expected (run upgrade ids unchanged). **Serialized renames:** use `[FormerlySerializedAs]` if any field moves into the subclass.
- **Other branches:** `thj/home-test` lacks it; merges later.

## Questions for THJ (Tier 3)

- **Q1 Design v2 as the build target**, with §11: start numbers as in §7 (cast 1 AP range 3 cooldown 4; 3 pips; arms 2, pull 1; Whirl 3×; Steer 1 AP 3 cells); Q21 read as a complaint about today. Recommended: yes.
- **Q2 Trailing Gale and Second Cyclone:** not now (recommended) / build as run upgrades.
- **Q3 Damage reporting (core):** (a) each Whirl runs as a hidden ability on Lucy's orchestrator (existing snapshot path, but it enters `LastActions`, role triggers, ATB fill); (b) **recommended:** a small additive core API on `CombatLevelRunHandler` to report damage from a non-ability source (raises `onUnitDamageDone`, awards resources), used by the Whirl; also usable later for the Duo bug (D-451).
- **Q4 Core changes (one yes for the set):** the walk exception in `GridCell.CheckIfUnitWalkable`; the Whirl's turn-switch hold (and a longer watchdog if needed); AI cross danger in scoring; the line-of-fire rule in `AIUnitBrain`, `AIFactionBrain` intent, `AEffectSpawner` execution check. Recommended: yes, each in its own commit.
- **Q5 Where and when:** recommended: its own branch (`thj/cyclone`, created by you from `thj/after-hearth`) after the Trail / River / Ridge challenge build, and tell the challenge designer now that the Cyclone will become Pulling Gale so its levels don't lean on the old drift. Alternatives: build now on `thj/after-hearth`; or first, before the challenge round.

## Gates

Per chunk: compile clean / EditMode (known red only) / `miso-reviewer` (core touched: every chunk) / THJ play check (C1 together, C2, C3, C4; then the whole: Watch beat length, AI waiting outside, Archers repositioning, pulls into hazards, Memory 4) / docs above.
