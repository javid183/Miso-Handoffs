# Cyclone round 2: Eye of the Storm (tech plan)

Size: L    Tier: 3 (core walk rule CR-58 and AI path; THJ approved the direction and core set in D-548 to D-551, this plan is shown to him before any build)    Assigned to: miso-implementer (opus for C2, C3; sonnet for C1, C4, C5), then miso-reviewer, miso-verifier
Branch: `thj/cyclone` (scope: this branch; other branches get it when it merges)
Status: waiting on THJ (plan approval)

## Why

THJ's first play of the built Cyclone ([`playtests/2026-11-12-cyclone-play-check.md`](../playtests/2026-11-12-cyclone-play-check.md), notes 1 to 11) found it too weak, misleading to read, unpreviewed, and the Masher walled off. Design: [`plans/2026-11-17-cyclone-round2-design.md`](2026-11-17-cyclone-round2-design.md). Decisions: D-547 (Steer hits), D-548 (carry), D-549 (one landing, no hold), D-550 (heavies walk through and burst it), D-551 (no Cyclone hit is anyone's action, "Gust" retired, Cyclone Power flat 3 / 4 / 5).

## Goal

A Steer carries the enemies beside the Cyclone, ends in a full Whirl, and previews every move and hit; heavy enemies walk through the Cyclone and burst it; the cross draws honestly.

## Acceptance criteria

- [ ] Steer = move, then a full Whirl (pull, reactions, hit, beat). The hit is credited to the cast like any Whirl hit (kill XP and gold, stats, barks, sisters' tally once per kill). The log reads "Whirl · Lucy: carried N, pulled N, hit M". No "Gust" in the log, texts, tooltips or code names shown to the player.
- [ ] No Cyclone hit (cast Whirl, Steer Whirl, end-of-turn Whirl, burst) triggers the Masher counter or Lucy's follow-up. Howling Gale's Weak applies on every Cyclone hit, and only on enemies actually hit.
- [ ] Cyclone Power: with `Stat_DMG` 1 the hit is 3 / 4 / 5 at levels 1 / 2 / 3 (a test proves each).
- [ ] Carry: on each Steer step, the enemy in front is shoved one cell ahead, then side enemies move one cell the same way (a blocked side enemy drops out), then the Cyclone, then the rear enemy follows. Enemies that end a step beside the Cyclone ride the next step. Immovable units and units larger than one cell never ride; an Immovable or large unit in front blocks the step.
- [ ] A step whose front enemy is blocked (wall, unit, walk-blocking planted entity, map edge) is never offered: the cursor and range highlight refuse that cell and every cell past it. A Steer never stops short after the player clicked.
- [ ] One landing: a carried enemy moves once along its planned path and lands once. No Crippled damage, no hazard on cells crossed, no pass-through reaction on the way. On landing, a hazard on the landing cell fires, Watch fires if it lands in Linda's lane, and it wakes. Order after the last step: carried enemies land (Watch, hazards), then the Whirl pull, its reactions, then the hit.
- [ ] Harmonic Slam plus a 3-cell carry cannot deal 15 to 16 to a Claw (test with the Crippled data path).
- [ ] Masher, Goblin Queen and any heavy (Immovable tag or footprint larger than one cell) can path and walk through the Cyclone cell (counter walk, Queen's charge, normal enemy turn moves). Entering the Cyclone cell bursts it: one hit (same value as the Whirl hit) on the heavy and every enemy beside the Cyclone, no pull, then the Cyclone is gone and the heavy continues. The cast's cooldown keeps running. Credit, Masher-counter and Weak rules as above.
- [ ] Non-heavy enemies still cannot enter the Cyclone (C2 behaviour unchanged); the family still walks through it and cannot stop on it.
- [ ] AI: a heavy's end-of-turn destination filter no longer refuses the cross; non-heavies keep EN-18. When a heavy's planned intent path crosses a live Cyclone, the Cyclone wobbles and its pips flicker (reuses the sprite and pips, no new element).
- [ ] Cross drawing: the 4 touching cells get one swirl tint in the Cyclone's wind hue (not warm or red); each of the 4 arm tips gets one inward chevron; no "3 ×" label and no streaks on the touching cells. The cross dims during any aim preview. During a Steer aim it is drawn at the landing cell only.
- [ ] Cast aim preview: cross at the aimed cell, a ghost for every enemy the cast Whirl pulls, damage segment and lethal skull on the ghost of every enemy it hits (an enemy pulled in from 2 out shows damage on its ghost).
- [ ] Steer aim preview: only reachable cells; path, landing Cyclone, one ghost per enemy that moves (carried or pulled, final cell only) joined to its start by a faint tether in the eye tint (replaces the step arrow); damage and skull on the ghosts; a landing hazard that will fire is shown. The preview is drawn at once when the cursor already sits on a cell as the Steer is picked (no mouse move needed). Previews survive the player's own hover refresh.
- [ ] The preview, the planner and the execution use one planner and agree (a test compares plan and executed result).
- [ ] Compile clean; EditMode all green except `AIRegressionTest.Baseline_MatchesCurrentAI`, whose inner failure count stays 43 (no new `AbilityPreset`, no unit prefab ability list change). Report the count before and after.

## Scope

In: Steer ends in a Whirl; carry planner and landing; Cyclone Power data; heavies walk through and burst; AI heavy handling and wobble; cross redraw and dimming; cast and Steer previews; first-frame Steer preview fix; log and text changes; tests; docs.
Out: hold (Q4 not adopted); per-cell pushes (D-549); Trailing Gale and Second Cyclone; new chunk grids; the AI regression re-baseline; Cyclone HP or targeting.

## Touches

Systems: Cyclone files in `Features/Player/Lucy/Scripts/Cyclone/` (not on the core list, but the Whirl path uses core hooks below); `GridCell.CheckIfUnitWalkable` / `GridCell.PlantedPass.cs` **(core, CR-58, per-mover heavy exception, approved D-550)**; `AEffectTransporter` stop rule **(core, AEffect family; only if the heavy exception cannot live inside the walkable check)**; `AIEndOfTurnDanger` / `AIUnitBrain.EndOfTurnDanger.cs` **(core, AI; approved D-533/D-550)**; `CombatLevelRunHandler.ReportDamageOutsideAbility` (unchanged, reused); `MasherCounterRules` (unchanged path); `AEffectPusher` and `AbilityDamagePreview` **(core: do not edit, see Approach)**.
USPs: Synergies (Watch, Tempest Bloom, Harmonic Slam), Family Roles (Watch).
Docs: see "Docs to update".

## Approach

Chunks, each one implementer run, each its own commit (C3 is three). Order: C1 first because C2 and C4 build on the Steer's Whirl; C2 then C3 are the risky ones.

**Rules for every chunk:** read `conventions.md`, `tech/core-systems.md`, the design plan, and `reports/cyclone-c2.md` to `cyclone-c5.md` for the existing code. Stop Play mode before editing scripts. No private IDs (D-xxx, plan names) in code, comments, tooltips, test names or commit messages. Keep line endings and BOM. Prefer new partial-class files. Write the report to `reports/cyclone-r2-c<N>.md` from `templates/report.md`. Do not touch THJ's uncommitted files (`PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font).

### C1. Steer ends in a Whirl; one rule; Cyclone Power (sonnet)

Goal: replace `GustRoutine` with the full `WhirlRoutine` at the Steer's destination (swell, pull, reactions, hit, burst, log). Credit through `steps.Report` as the Whirl already does. Retire "Gust": `CycloneSteerSteps.LogId`/`LogGust`, `CycloneSteerRules.GustLogDetail`, comments, test names and any player-visible text; the log line becomes `Whirl · Lucy: carried N, pulled N, hit M` (carried is 0 until C2; build `WhirlLogDetail` to take it now). Make Cyclone Power flat 3 / 4 / 5 (data on `Lucy_Cyclone_Ability.asset` `Stat_DMG` upgradeLevels and/or the hit modifier, whichever gives exact values with `Stat_DMG` 1 without rounding luck; the existing x1.2 / x1.4 both round to 4). Keep `whirlHitTimes` (the old label value) consistent or remove it with the label in C4.
Files: `CycloneEntity.Steer.cs`, `CycloneEntity.Whirl.cs`, `CycloneSteerSteps.cs`, `ICycloneSteerSteps.cs`, `CycloneSteerRules.cs`, `CycloneRules.cs`, `Lucy_Cyclone_Ability.asset`, tests in `Features/Player/Lucy/Scripts/Editor/`.
Checks: Steer hit credited to the cast; Masher counter ignores the Steer's hit; Howling Gale Weak on Steer hits; Cyclone Power 3 / 4 / 5; Steer turn-switch hold and watchdog still hold during the longer Steer (the Whirl already registers a hold; make sure Steer and Whirl do not double-register or leave a hold on abort); `Dispose` stays deferred during the Steer's Whirl.

### C2. Carry (opus)

Goal: the per-step carry planner and its execution and a single plan shared with the preview.
- New pure planner (static, worker-safe, no Unity-object APIs, like `CycloneWhirlPlanner`): given the grid, the path and the enemy positions, returns per step the ordered moves (front, sides, Cyclone, rear), the riders, who drops out, and the final landing cell per carried enemy; plus `CanTakeStep` for the reachability rule. `CycloneSteerRules.CanCross` / `Explore` / `Destinations` use it so unreachable cells are never offered (this changes the range highlight returned by `AEffectCycloneSteer.TryCollectTargetSelectionCells`).
- Execution: carried enemies move once along their planned straight path and land once. **Do not edit `AEffectPusher` or `AEffectTransporter`** (core). Do it in Cyclone code: unplug at start, lerp the visual along the planned cells in step with the Cyclone's glide, plug at the landing cell only (the plug fires landing hazards and planted-entity activation), then raise the move-end events Watch listens for and call `EnemyAlertTracker.WakeMovedUnit`, as `CycloneWhirlSteps.TryPull` does for pulls. `CycloneSteerSteps.Relocate` is the pattern. If raising the events Watch and the alert tracker need cannot be done from Cyclone code, STOP and report the exact core API needed (an additive public entry on `AEffectPusher` taking an explicit cell list, or a public event raiser): that is Tier 3 and comes back to THJ.
- Riders: same filter as the pull (`IsPullable`, footprint 1x1); Immovable or large in front blocks the step; a heavy beside the Cyclone does not ride and does not block.
- Order after the last step: carried land, then the Whirl (pull, reactions, hit). The Whirl's pull stays a push exactly as today (it may pay Crippled once, as built).
- AI worker thread: the planner reads only plain data; the live `CycloneRegistry` stays plain references. No new statics (if one is unavoidable, add a `ResetPlayModeState` and hook it in `PlayModeStaticReset.cs`).
- Failure handling: a rider dies or is removed mid-carry (target dies, hit by something): skip it, never leave a unit unplugged. Abort cleanup (level end, Cyclone destroyed mid-Steer) re-plugs every carried unit on its last valid cell. Steer's hold and watchdog cover the longer carry.
Tests (EditMode, recorder pattern from `CycloneSteerTests`): front shove, side drag, blocked side drops out, rear follows, late joiner, mid-path joiner, large and Immovable never ride, blocked front refuses cell and everything past it, one landing (no hazard on crossed cells, hazard on landing cell), Harmonic Slam plus carry guard via the Crippled data path, plan equals execution, abort re-plugs.

### C3. Heavies walk through the Cyclone and burst it (opus, three commits)

Core, approved D-550; each commit stands alone and builds. Heavy = `EntityState.Unmovable` tag (the same query as `CycloneWhirlSteps.IsPullable`) or `EffectivePlacementSize` larger than 1x1; read from existing data, no new tag. Define it once in a small static helper next to `CycloneRules` (worker-safe) so the walk check, the AI and the burst share it.
- **C3a. Walk exception (core).** Extend the walk check so a heavy mover passes the Cyclone cell: `GridCell.CheckIfUnitWalkable` / `PlantedLetsPass` get the mover (or a heavy flag) through `FindPathTo(mover:)` and the Transporter's footprint check (`IsFootprintWalkable`, `GridPluggableEntity`), additive overloads with the old signatures unchanged. Check every consumer of the pass rule (`GetRangeCells`, `AEffectDashAttack.TryResolveStandableNextTo`, the Mark-Linda Duo loser stop) still behaves; the stop-short rule for non-heavies is unchanged. Cannot-stop-on rule unchanged: a heavy may not END its move on the Cyclone cell unless the Cyclone is gone (it bursts on entry, so it is gone).
- **C3b. Burst.** When a heavy plugs onto or enters the Cyclone cell, the Cyclone bursts: one hit (same compound as the Whirl) on the heavy and each enemy beside the Cyclone, no pull, credited to the cast, then `Dispose`. The planted-entity `Activate(entity)` call in `GridCell.PlugEntityInternal` is the expected hook (`CycloneEntity.Activate` is empty today); confirm it fires for a mid-path cell during a Transporter walk and add a fallback in Cyclone code if it does not. The burst must not double fire with an end-of-turn Whirl in the same moment, and a burst during an enemy turn registers the turn-switch hold like the Whirl does. Masher counter, Lucy follow-up and Weak follow the one rule. Show it with the Whirl's burst beat.
- **C3c. AI heavy handling (core, AI).** `AIUnitBrain.EndOfTurnDanger` filter: a heavy does not refuse the cross. Path planning for heavies treats the Cyclone cell as walkable (same mover-aware check the AI's `FindPathTo` calls take). Worker-thread safe: the per-unit heavy flag comes from data the brain already has (tags and footprint on the blackboard snapshot) with no Unity-object calls. Wobble: when a heavy's intent path crosses a live Cyclone, the Cyclone wobbles and the pips flicker (main thread, from the intent preview; reuse the existing sprite and `CyclonePipsView`).
Tests: heavy passes, non-heavy still blocked, heavy cannot be stopped on the cell, burst hits heavy and neighbours once, Cyclone gone after, no counter, Weak applied, Queen's charge through the cross, Masher counter walk through, AI filter per unit kind, plus a determinism check on the AI path (`AIRegressionTest` count stays 43).

### C4. Cross drawing and previews (sonnet, opus if the preview needs a core hook)

- **Cross (B1).** `CycloneCrossView`: remove the label and the touching-cell streaks; add a wind-hue tint on the 4 touching cells and one inward chevron per arm tip (2 out); dim on aim (`CycloneSteerPreview.IsAiming` / `abilitySelectEnteredTargetSelection` are the aim signals; also dim during the cast's target selection); during a Steer aim draw the cross at the landing cell and hide it at the current cell. Remove `TouchLabel` and its test, or leave the helper unused only if something else reads it.
- **Cast preview.** A Cyclone-aware preview for `AEffectCycloneSpawner` in Cyclone code (a component bound like `CycloneSteerPreview`, listening to the same target-selection and hover events): `CycloneRules.TouchingCells(castCell)` and `CycloneWhirlPlanner.PlanPulls`, ghosts for pulled enemies, damage via the existing public `GUnit.ShowDamagePreview` / `DamagePreviewRules` on the ghost's unit (`AbilityDamagePreview.SimulateApply` is the model for the number; reuse it by calling it, do not edit it). Do not edit `AbilityDamagePreview.cs` or `PlayerController.cs`: they are core. If the number cannot be computed without editing them, STOP and report the minimal additive hook needed.
- **Steer preview.** Rework `CycloneSteerPreview.Show` from the C2 plan: reachable cells only, one ghost per moving enemy (final cell only) with tether (replaces `SetDirectionPreview` arrow), damage and skull on ghosts, landing hazard shown. Fix the first-frame bug: in `OnEnteredTargetSelection` resolve the cell under the cursor and `Show` it (a read-only accessor for the hovered cell on `GridManager` is an additive core change: first try the player's input or raycast route from Cyclone code; ask before touching `GridManager`). Keep the per-frame re-apply so the player's hover previews do not wipe it; make sure `HideDamagePreviews` cleanup removes the Cyclone's damage previews on cancel, click and level end.
- The HP bars show the Whirl hit only, never Watch kills (as Tempest Bloom's preview does).
Tests: pure parts (cell sets, ghost plan equals executed plan, dim state transitions) in EditMode; the visual result needs THJ's play check.

### C5. Texts and docs (sonnet for code strings; narrative and designer for wording)

- `miso-narrative`: Steer title, description and hint line ("Steer drags enemies beside it, then it Whirls."), Cyclone, Cyclone Power (3 / 4 / 5), Howling Gale, burst; retire "Gust" in `glossary.md` and propose "Eye of the Storm" as a name only (THJ approves).
- `miso-implementer`: apply approved strings (ability presets' text fields, `UnlockableSet` titles); no new `AbilityPreset`.
- `miso-game-designer`: GDD pages and `cyclone-redesign.md` as-built note (see list).
- Coordinator: `tech/core-systems.md`, `tech/combat-architecture.md`, build log, status, branches; note mirror syncs.

## Risks

- [x] **Preview trust:** plan, preview and execution use one planner (C2); a test compares them.
- [x] **Core changes:** C3a and C3c are core (approved D-550 and D-533, each its own commit, shown here first). C2 and C4 are written to avoid `AEffectPusher`, `AEffectTransporter`, `AbilityDamagePreview`, `PlayerController` and `GridManager`; if one proves unavoidable the implementer stops and reports, and I ask THJ.
- [x] **AI worker thread:** the planner and the heavy check read plain data only; the AI test count must stay 43.
- [x] **Statics and caches:** none planned; any new static gets a `PlayModeStaticReset` hook.
- [x] **Event subscriptions and abort cleanup:** previews unbind on cancel and level end; a Steer aborted mid-carry re-plugs every unit; turn-switch holds released in `finally`.
- [x] **Unplugged units:** a carried unit must always end plugged on a valid cell (death, level end, Cyclone destroyed mid-Steer).
- [x] **Assets:** one ability asset data edit (Cyclone Power) and text fields: small YAML edits; check with the Unity editor that it still loads.
- [x] **Combo runaway:** Crippled guard (one landing); Watch has no per-round cap (LI-11), the quiver is the limit.
- [x] **Creep:** change one lever per play (design plan §10).
- [x] **Serialized field renames, save data:** none planned (if `whirlHitTimes` is removed, check the prefab; use `[FormerlySerializedAs]` only if renamed).
- [x] **Other branches:** Cyclone work lives on `thj/cyclone` only; its merge to `main` carries it. The core C3 changes are additive overloads so `main`'s other branches merge easily.
- [x] **THJ's test settings commit `b88c004f1`** (intros off) is untouched; revert before a merge to `main`.

## Gates

Per chunk: compile clean; EditMode green except the known red (count 43 reported); `miso-reviewer` (C2 and C3 for sure; C1, C4 too since the Whirl path is shared). After C4: `miso-verifier` final gate. THJ play check: yes, needs his time, once after C4 (D-534 style, he plays everything together); the play list goes to `playtests/2026-11-17-cyclone-round2-play-check.md`. Win playthrough: no (does not touch M2 win path, drops or rollback). Docs updated by owners; mirror sync owed for GDD Lucy, Combat rules, Enemies, Family systems.

## Docs to update

- Designer: GDD `characters/lucy.md` (LU-4 Whirl closes every Steer, LU-5 no Cyclone hit is anyone's action and the burst, LU-6 Steer = carry then Whirl and the preview, LU-7 heavies pass and burst it, value table Cyclone Power 3 / 4 / 5, Howling Gale row); `enemies.md` (EN-2, EN-3, EN-6, EN-18); `combat-rules.md` (CR-58 heavy exception); `design/cyclone-redesign.md` as-built note; `level-chunks.md` chunks 1, 12, 13, 24 text only.
- Narrative: `glossary.md` (retire Gust).
- Coordinator: `tech/core-systems.md` (heavy walk exception, AI heavy filter, the Cyclone note's stale "uncommitted" line), `tech/combat-architecture.md`, `build-log.md`, `status.md`, `branches.md`, `decisions.md`.

## Commit plan (proposed after the play check, one yes each, no attribution trailers, no private IDs)

1. C1 Steer ends in a Whirl; Cyclone Power values; Gust retired.
2. C2 carry planner, execution and tests.
3. C3a walk exception (core).
4. C3b burst.
5. C3c AI heavy handling and wobble (core).
6. C4 cross drawing and previews.
7. C5 texts and data strings.
