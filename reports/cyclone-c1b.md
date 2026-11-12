# Report: Cyclone redesign, C1b (Whirl) + C1a review fixes

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer (opus)    Branch: thj/cyclone
Outcome: done, fix round applied (THJ play check pending for C1 as a whole). Reviews: `reports/cyclone-c1a-review.md`, `reports/cyclone-c1b-review.md` (FIX, addressed below).

## Fix round (after the C1b review)

Every item from the C1b review, plus THJ's Masher decision:
1. **Must fix: Whirl caps in real seconds.** `CycloneEntity.Whirl.cs` caps are now `PullTimeoutSeconds = 3` and `ReactionTimeoutSeconds = 15`, counted on the steps' clock: `ICycloneWhirlSteps.DeltaTime()`, which in the real steps is `Time.unscaledDeltaTime` and 0 while the time scale is 0, so a pause never uses up a cap. The settle rule is unchanged (10 quiet frames). Tests step the clock: `Whirl_AReactionLongerThanManyFastFrames_IsStillWaitedFor` (4 s of reactions at 1000 frames a second is waited out), `Whirl_AStuckReaction_HitsAfterTheReactionCap`, `Whirl_PausedTime_DoesNotRunOutTheReactionCap`, `Whirl_AStuckPull_StopsHoldingAfterThePullCap`.
2. **Watchdog (core).** `TurnSwitchHoldSet.IsHeld` has a new overload with `paused`; while paused, held time doesn't grow and counting resumes where it stopped. `IsTurnSwitchHeld` passes `Time.timeScale == 0f`. Otherwise the watchdog is unchanged (5 s real time). The old signature stays and forwards with `paused: false`. Test: `TurnSwitchHoldTests.Watchdog_DoesNotCountPausedTime`; all earlier hold tests pass.
3. **After the level ended** the Whirl lands no hit, reports nothing and logs nothing (`ICycloneWhirlSteps.LevelEnded()`, the real steps read `CombatLevelRunHandler.IsLevelEnded`). Test: `Whirl_AfterTheLevelEnded_NoHitNoReportNoLog`.
4. **Hold registration.** `StartWhirl` returns early when the Cyclone isn't `isActiveAndEnabled`; the routine registers its own hold when it starts and releases it in `finally`.
5. **Effect-level test** `CycloneHitContextTests`: a compound run with the cast raises `onAbilityEffectPerformedOn` and uses John's relay (control); the same compound run with `CycloneHitContext` does neither.
6. **Deferred Dispose waits for pull moves too.** The Cyclone counts pull moves still under way (`HasPendingPulls`; each move's landing counts once). A `Dispose` while a Whirl runs waits for the Whirl; a `Dispose` while moves are still under way (they can outlast the 3 s pull cap) waits for them, queued once. Test: `Dispose_WithAPullStillMoving_WaitsForItToLand`.
7. **Watchdog risk text** in this report corrected (Risks below).
8. **Masher ignores Whirl hits (THJ).** `MasherCounterRules.Classify` gains an overload with `isCycloneWhirlHit`: a Whirl hit is `Ignore`, everything else is passed to the unchanged rule. `MasherGoblinFactionRoleHandler.Counter.ClassifyHit` passes `CycloneRules.IsCycloneCast(source)`. The new `CycloneRules.IsCycloneCast` is true when the ability's effects hold the Cyclone spawner; the cast itself deals no damage, so any damage credited to it is a Whirl, on cast or at the end of the enemy turn. Tests `MasherCounterWhirlTests`: Ignore in every case for a Whirl hit; every other hit classified as before (all 32 combinations); the live Cyclone ability is recognised and another of Lucy's abilities is not. The existing Masher tests pass. This is a rules-level test; that no provocation is actually queued in a level is a play check.

Files touched in this round: `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs`, `Core/Interactions/Editor/TurnSwitchHoldTests.cs`; in `Features/Player/Lucy/Scripts/Cyclone/`: `CycloneEntity.cs`, `CycloneEntity.Whirl.cs`, `ICycloneWhirlSteps.cs`, `CycloneWhirlSteps.cs`, `CycloneRules.cs`; `Features/Player/Lucy/Scripts/Editor/CycloneWhirlTests.cs`; new `Features/Player/Lucy/Scripts/Editor/CycloneHitContextTests.cs` (+ .meta); `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `MasherGoblinFactionRoleHandler.Counter.cs`; new `Features/Enemy/Masher Goblin/Editor/MasherCounterWhirlTests.cs` (+ .meta).

Super Time stays skip (THJ).

**EditMode after the fix round:** 1947 run, 1946 passed; the only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not re-baselined). That full run came before a final edit that only moved the new Masher overload below the original method (no logic change). After it, the whole `MISO.Core.Features.Bergsons.EditorTests` namespace was rerun: 459 run, 459 passed (Lucy, Masher, Linda and the rest). Compile clean.

## What changed

Paths under `miso/Assets/_Project/`. New files are LF; the new core partial is LF with a BOM like its siblings.

### A. C1a review fixes
- `Features/Player/Lucy/Scripts/Cyclone/CycloneRules.cs`: `IsValidCastCell` no longer does a Unity null check (only `ReferenceEquals`, plain slots and flags).
- `Features/Player/Lucy/Scripts/Editor/CycloneAnchoredSetup.cs`: each step sets its starting values only when it actually does its switch or creation. The prefab gets the anchored values only when its script is switched; the ability gets range/cooldown only when the spawn effect's script is switched; the pusher is created only when missing; the prefab's pusher and pull filter are filled only when empty. A re-run reports "nothing changed" and never undoes tuning.
- `Features/Player/Lucy/Scripts/Editor/CycloneCastTests.cs`: two new tests for the execution-time refusals (`LogAssert.Expect` on the warning, nothing spawned, cast not held open).
- The optional Initialize/Dispose registry test was **not** added: `Initialize` plugs into a real cell and runs the grid's plug path (visuals, occupant root), which a hand-built test cell can't take. Disposal during a Whirl is covered (below).

### B. C1b
New (`Features/Player/Lucy/Scripts/Cyclone/`, each with .meta):
- `CycloneEntity.Whirl.cs`: the Whirl as a partial of `CycloneEntity` (now `partial`). Swell → pull → wait for reactions → hit → burst → log. Runs on cast (from `Initialize`) and at the end of every enemy turn (from the run handler's new `TurnEnding` event), with a turn-switch hold for its whole length. New serialized fields `whirlPusher`, `pullTagQuery`, `swellSeconds` (no field moved). `Dispose` during a Whirl waits until the Whirl ends, so a pulled unit is never left between cells.
- `CycloneWhirlPlanner.cs`: pure grid planner. Pulls only enemies on a straight arm, 1 cell in, through `VortexPullPlanner` (nearest first, claimed cells, the centre blocked). A cell a nearer unit leaves becomes free for the one behind it. Lands only where nobody stands, nothing is stashed and no planted entity blocks walking; a non-blocking hazard is fine and fires on landing. Hit targets are the enemies on the 4 touching cells, once each; a large unit counts if any of its cells touches.
- `ICycloneWhirlSteps.cs` + `CycloneWhirlSteps.cs`: the Whirl's contact points with the game (enemy/pullable checks, pull, reactions settled, hit, report, beat, log), swappable for tests. The real pull calls `AEffectPusher.TryMoveTo` with the Cyclone as the move's owner, so `unitEndMoving` is raised (Watch) and hazards fire on plug. The Immovable filter is done by hand (`pullTagQuery`, leaving out `EntityState.Unmovable`, same query as Black Despair's pusher), because `TryMoveTo` skips effect guards. "Reactions settled" uses the same idle test as the Masher counter (no action in progress, no QTE, no sequence) and must hold for 10 frames.
- `CycloneHitContext.cs`: wraps the cast's `RuntimeAbility` as a plain `IHaveStatAttributes`. The hit keeps Lucy's damage and Cyclone Power, but `AEffectCompound` doesn't see an ability, so it skips `onAbilityEffectPerformedOn` (the old buffered path, Lucy's role hit list, the tally workaround) and John's relay.
- `Lucy_Cyclone_Whirl_Pusher.asset` (+ .meta, in `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/`): created by the setup tool. Speed 4 (Black Despair's), distance 1, pull towards, straight only, no on-move effects.

Modified:
- `CycloneEntity.cs`: `partial`; `Initialize` subscribes to `TurnEnding` and starts the cast Whirl; `Dispose` defers during a Whirl and unsubscribes.
- `AEffectCycloneSpawner.cs`: `HoldCastWhileWhirlPulls`. The cast stays in progress while the first Whirl is pulling, so the pull belongs to Lucy's action; the reactions and the hit follow once her action is over (this is what lets Watch answer a cast-time pull before the hit).
- `CycloneCrossView.cs`: the beat. Swell (the Visual scales ×1.33 over 0.2 s), streaks flare while pulling, then a ring bursts over the touching cells (0.3 s) and the Cyclone shrinks back. All placeholder; no camera ease.
- `CycloneRegistry.cs`: `LiveFor(owner)`. `CycloneRules.cs`: `WhirlLogDetail`. `CycloneSprites.cs`: `Ring()`.
- `Features/Player/Lucy/Prefabs/Cyclone.prefab`: `whirlPusher` → the new pusher; `pullTagQuery` leaves out `EntityState.Unmovable`; `swellSeconds` 0.2 (written by the setup tool).
- **Core** `Core/Managers/CombatLevelRunHandler.DamageReport.cs` (new partial, + .meta): additive `public bool ReportDamageOutsideAbility(RuntimeAbility source, GUnit target, float healthBefore)`. It raises `onUnitDamageDone` once and calls the existing `AwardAbilityDamageResources`, with the same rules as an ability hit (enemy only; lethal when dead or at minimum health). It also adds `public static TryMeasureDamage(...)`, the pure measuring rule. No existing method or signature changed; it doesn't touch the snapshot dictionaries.
- **Core** `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs`: new `public event Action<Faction> TurnEnding` plus private `RaiseTurnEnding`. **Core** `CombatLevelRunHandler.cs`: the `SwitchTurnIE` wait condition is moved into `IsTurnSwitchBlocked()` with the same terms in the same order. After that wait, `TurnEnding` is raised once; if a listener registered a hold, the switch waits on the same condition again. With no listener, behaviour is identical. Watchdog unchanged at 5 s (see risks).
- `Features/Onboarding/SistersTally/SistersTallyListener.cs`: killed-once guard in `RecordDamage` (`_killedByPlayer.Add` must succeed); class and method docs updated. Cyclone hits now count through the damage event; `RecordEffectOutsideAbility` stays for Tempest Bloom copies that land late.
- Tests: `Features/Player/Lucy/Scripts/Editor/CycloneWhirlTests.cs` (+ .meta, new, 13 cases), `Features/Onboarding/SistersTally/Editor/SistersTallyTests.Whirl.cs` (+ .meta, new, 3), `CycloneCastTests.cs` (+2 refusals, prefab checks for the Whirl fields and the 3× hit). **Two existing tally tests changed fixture**: `SistersTallyTests.Kill_ASistersLethalHitOnAnEnemyCountsForHer` and `SistersTallyTests.Attribution.Level_ASisterRevealedLater_MakesItEligibleFromThen` reused one goblin for several kills, which the new one-kill-counts-once rule refuses. They now kill distinct enemies; what they check is otherwise unchanged.

Not touched: `OnGridEntity`, `AEffectVortexPull`, `VortexPullPlanner`, `AEffectPusher`, `AEffectCompound`, AOE warnings, hazards, Toba's wall, relics, the Linda-folder copies, THJ's uncommitted files.

**Finding: the hit effect was already 3×.** `Lucy_Cyclone_Effect_AttrMod` reads `baseFactor: 3 × Stat_DMG` (lowered in the after-Hearth merge), not 7× as the plan's code facts say. The prefab's `effect` (`Lucy_Cyclone_Effect_Compound`: the 3× hit plus Howling Gale's locked Weak compound) is therefore exactly the Whirl hit and is used as is; nothing stale is left for previews. The prefab test pins 3 × `Stat_DMG`.

## Acceptance criteria (C1, Whirl share)

- [x] Whirl on cast and after all enemies have acted, before the turn passes. The cast Whirl starts from `Initialize`. The end-of-turn Whirl starts from `TurnEnding`, raised only after the switch's own wait (actions, sequences, holds) and only for factions that are enemies of the caster. Tests: `CycloneWhirlTests.TurnEnding_RaisedToListeners_AndAHoldTheyRegisterMakesTheSwitchWait`, `Cast_HoldsTheActionWhileItsWhirlPulls`. Timing in a real level: play check.
- [x] Pull each non-Immovable enemy on an arm (2, straight only) 1 cell in if free, nearest first: `Pull_OnlyEnemiesTwoCellsOutOnAStraightArm_OneCellIn`, `Pull_BlockedByAUnitOrABlockingEntity_NotByAHazard`, `Pull_ImmovableNotPulled`, `Pull_NearestFirst_AFurtherUnitTakesTheCellANearerOneLeft`. Immovable filter on the live prefab: `LivePrefab_IsAnAnchoredCyclone`.
- [x] Then 3× on each enemy on a touching cell, large units if any cell touches: `Hit_EnemiesOnTouchingCellsOnce_ALargeUnitOnce`; 3× pinned in the prefab test.
- [x] Order pull → reactions → hit: `Whirl_PullsThenWaitsForReactionsThenHits_EachHitReportedOnce` (a unit pulled in is hit by the same Whirl).
- [x] Pulls raise `unitEndMoving`; hazards on the landing cell fire: by construction (`AEffectPusher.TryMoveTo` → `MoveEntity` → `PlugEntity` → planted `Activate`). Play check (Watch, spikes).
- [x] Whirl damage reaches `onUnitDamageDone` exactly once per hit: one `Report` per hit (test above); the measuring rule is `DamageReport_MeasuresTheHit` (4 cases). It never goes through `onAbilityEffectPerformedOn` (`CycloneHitContext`). The real report is a play check: needs a level's run handler and registries.
- [x] Doesn't trigger Lucy's follow-up: no flow events and no effect-performed event come from a Whirl. Play check.
- [x] The sisters' tally counts a Cyclone kill once: `SistersTallyTests.Whirl_ACycloneKillReportedAfterTheCastCountsOnceForLucy`, `Whirl_ANonLethalCycloneHitCountsNothing`, `AKillReportedTwiceCountsOnce`. All Bloom / OutOfAbility tally tests still pass.
- [x] Beat (swell → streaks → burst) and the log line: placeholder beat in `CycloneCrossView`. The log line is a synergy note, so the combat log shows "✦ Whirl · Lucy: pulled N, hit M → targets" (no combat-log code changed). Play check.
- [x] If the Cyclone dies mid-Whirl no unit is left unplugged: `Whirl_DisposeDuringAWhirl_WaitsForItsEnd`. Pull moves run on the Cyclone, which now outlives its Whirl.
- [x] AOE warnings, hazards, Toba's wall, relics unchanged: no shared file touched; `GridEntityLifetimeTests` still pass.

**EditMode suite:** 1935 run, 1934 passed, 1 failed: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Not re-baselined. All 35 Cyclone tests pass (20 from C1a, 2 refusals, 13 Whirl), plus 3 new tally tests. Compile clean.

## Save reset

No.

## Decisions I made

- End-of-enemy-turn timing is a small additive event on the run handler (`TurnEnding`), raised after the switch's existing wait. A listener registers a hold there and the switch waits again. This needs no polling for "all enemies have acted". It's the turn-hold change approved for this redesign, in its own commit.
- The pull is my own straight-arm planner on `VortexPullPlanner` + `AEffectPusher.TryMoveTo`, instead of `AEffectVortexPull`. The vortex has no straight-only option, so using it would have meant a core edit; the behavior asked for is the same.
- Whirl damage goes through the existing hit compound, run with a stats wrapper (`CycloneHitContext`) so it isn't treated as the cast's own hit, and is reported once through the new core API, credited to the cast's `RuntimeAbility`. Damage listeners already require an ability (`ability.Preset`, `ability.Owner`). Passing the cast keeps them working and gives Lucy the credit in stats and barks.
- The log line is a synergy note (`GlobalEventBus.RaiseSynergy(lucy, "Whirl", "pulled N, hit M", targets)`). The combat log stays record-only and unchanged; no listener reacts to that id.
- The cast stays open only while its first Whirl pulls; the hit lands after Lucy's action ends. Reason: Family Roles (Watch) run when actions complete, so this keeps the pull → reactions → hit order on cast too. Side effect: the hit lands a moment after the cast ends.
- Reaction wait: 10 quiet frames, capped at 15 s; pull wait capped at 3 s. Both caps run on real seconds that stop while paused, read through the steps so tests can step the clock (fix round).
- The Whirl does nothing if its caster's object is gone (no pull, no hit: the enemy check needs her faction). A downed Lucy still exists, so her Cyclone keeps whirling.

## Needs THJ

None. Both earlier questions are answered: Super Time stays skip; the Masher ignores Whirl hits (built in the fix round).

## Docs to update

- `tech/core-systems.md` (coordinator): `CombatLevelRunHandler.ReportDamageOutsideAbility` / `TryMeasureDamage` (new partial `CombatLevelRunHandler.DamageReport.cs`); `TurnEnding` event + `IsTurnSwitchBlocked` in `SwitchTurnIE`; `PlayModeStaticReset` resets `CycloneRegistry`; Lucy's Super Time cell rule (from C1a). Step 5 of "Damage and death" gains the outside-ability report.
- `tech/combat-architecture.md` (coordinator): end-of-turn effects via `TurnEnding` + a hold.
- Plan code facts: the Cyclone hit is 3× already, not 7×.
- GDD (designer, C5): Whirl timing on cast (the hit lands just after the cast ends); Whirl damage now reported (stats, barks, Masher provocation).

## Risks and loose ends

- **Hold watchdog (5 s).** The watchdog counts only frames where the hold is the switch's sole blocker. Linda's Watch runs as a player-controller action (`PhaseData.IsInProgress`, `PlayerController.cs:1592`), which the switch's own condition (`isActionInProgress`) already waits on, so Watch's time doesn't count toward the 5 s. The hold-only time of a normal Whirl (swell, pull, the 10 quiet frames) is under a second. The watchdog could have fired during a pause; it no longer counts paused time (fix round). If it ever fires, the holds are cleared, the turn switches, and the rest of the Whirl lands at the start of the family turn.
- **Not playtested at all.** Every runtime path (real pusher move, hazards on landing, Watch timing, the report's resource awards, the beat) is a play check.
- `CycloneHitContext` hides the cast from effects. Anything in the hit compound that needs the `RuntimeAbility` itself (area-shape run upgrades via `RunUpgradeTracker.ResolveAreaShape`) doesn't apply to Whirl hits. Nothing in today's compound uses it.
- Howling Gale's Weak compound has radius 1 and runs per hit as before; whether its area matches "every enemy a Whirl hits" is a C5 check.
- The cast Whirl's pull holds Lucy's ability open. If a pull's move never finishes, the 300-frame cap releases it.
- `ReportDamageOutsideAbility` raises `onUnitDamageDone` from outside any action, so listeners that expect an action in flight (Wrath, Blood Debt, Atman Barrier, AP providers) filter by basic attack or owner and ignore it. Barks and mission stats now see Cyclone damage.
- The cross and beat still don't hide in cutscenes (from C1a).
- The AI doesn't know the cross yet (C2). Enemies still can't walk through the Cyclone (`disallowWalk`).

## Proposed commits

C1a + C1b together, in dependency order. Core changes each in their own commit.

1. `feat(core): report damage dealt outside an ability's span, credited to the ability that left its source on the board` (**core**): `Core/Managers/CombatLevelRunHandler.DamageReport.cs` (+ .meta).
2. `feat(core): raise an end-of-turn event after the turn's actions finish, so an end-of-turn effect can hold the switch` (**core**, risky: turn flow): `Core/Managers/CombatLevelRunHandler.cs`, `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs` (the `TurnEnding` event and `RaiseTurnEnding` hunks only).
2b. `fix(core): the turn-switch hold watchdog doesn't count time while the game is paused` (**core**): `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs` (the `IsHeld` overload, `_lastCheckTime` and the `IsTurnSwitchHeld` call hunks), `Core/Interactions/Editor/TurnSwitchHoldTests.cs`. It shares a file with 2, so stage it by hunk (`git add -p`, which THJ runs) or fold it into 2; the change stands alone (no dependency on 2).
3. `feat(lucy): the Cyclone stays where it is cast, whirls on cast and at the end of each enemy turn (pull one cell in, then 3x on touching enemies), shows its cross and pips, and casts only on an empty cell` (plain; depends on 1 and 2):
   - `Features/Player/Lucy/Scripts/Cyclone.meta` and `Features/Player/Lucy/Scripts/Cyclone/` (each with .meta): `CycloneEntity.cs`, `CycloneEntity.Whirl.cs`, `CycloneRules.cs`, `CycloneRegistry.cs`, `AEffectCycloneSpawner.cs`, `CycloneCrossView.cs`, `CyclonePipsView.cs`, `CycloneSprites.cs`, `CycloneWhirlPlanner.cs`, `ICycloneWhirlSteps.cs`, `CycloneWhirlSteps.cs`, `CycloneHitContext.cs`.
   - `Features/Player/Lucy/Scripts/Editor/CycloneAnchoredSetup.cs` (+ .meta).
   - `Features/Player/Lucy/Prefabs/Cyclone.prefab`.
   - In `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/`: `Lucy_Cyclone_Effect_Spawn.asset`, `Lucy_Cyclone_Ability.asset`, `Lucy_Cyclone_Whirl_Pusher.asset` (+ .meta).
4. `test(lucy): Cyclone life, cast, Whirl, hit-context and shared grid-entity lifetime tests` (plain; depends on 3): `Features/Player/Lucy/Scripts/Editor/CycloneTestGrid.cs`, `CycloneLifeTests.cs`, `CycloneCastTests.cs`, `CycloneWhirlTests.cs`, `CycloneHitContextTests.cs`, `GridEntityLifetimeTests.cs` (+ .meta each).
5. `chore(core): reset the live Cyclone list between play sessions` (**core**; depends on 3): `Core/Managers/PlayModeStaticReset.cs`.
6. `fix(lucy): Super Time casts the Cyclone only on an empty cell and skips with a warning when none is free or hers is already out` (**core**: role handler; depends on 3): `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`.
7. `fix(onboarding): the sisters' tally counts each kill once; Cyclone kills count through the damage report` (plain; depends on 1 and 3 for the Cyclone path): `Features/Onboarding/SistersTally/SistersTallyListener.cs`, `Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs`, `SistersTallyTests.Attribution.cs`, `SistersTallyTests.Whirl.cs` (+ .meta).

8. `fix(masher): the reckless counter ignores hits from Lucy's Cyclone` (plain; depends on 3 for `CycloneRules.IsCycloneCast`): `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs`, `Features/Enemy/Masher Goblin/Editor/MasherCounterWhirlTests.cs` (+ .meta).

Commits 3 and 5 can merge if THJ prefers (3 adds the static that 5 resets). Don't stage THJ's uncommitted files (AI brains, PreloadScreen, ProjectSettings, TMP fallback font).

## Other branches

`thj/home-test` lacks the redesign; it merges later with the rest (plan).

## How to see it

1. Open a level with Lucy and enemies (e.g. a Trail fight). Cast Cyclone on an empty cell within 3, with one enemy 2 cells away in a straight line and one right next to that cell.
2. On cast: the Cyclone swells, the arm streaks flare, the far enemy slides one cell in, then a ring bursts and both enemies take the hit (3 × Lucy's damage; numbers show). The combat log (Tools > Combat Log > Open Window) shows "✦ Whirl · Lucy: pulled 1, hit 2".
3. End turn. After the last enemy acts and before your turn starts, the Cyclone Whirls again. The turn waits for it. An enemy that walked onto an arm cell 2 out is pulled in and hit.
4. With Linda in the same row or column as a pull's landing cell: Watch fires after the pull and before the hit.
5. A Masher or other Immovable enemy on an arm isn't pulled (still hit if touching). An enemy pulled onto spikes takes the spikes.
6. Kill an enemy with a Whirl in a level where the sisters' tally runs: Lucy's count goes up by one.
7. Round 4 start: the Cyclone fades (End animation). Masher/Queen area warnings, hazards and Toba's wall behave as before.
