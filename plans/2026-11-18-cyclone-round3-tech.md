# Cyclone round 3: drop on a foe, breathe in and out (tech plan)

Size: L    Tier: 3 (the rule change and the feel were approved by THJ in D-566 to D-568; no core API change planned, see Risks)    Assigned to: miso-implementer (opus for C2 and C3, sonnet for C1), then miso-reviewer, miso-verifier
Branch: `thj/cyclone` (scope: this branch; checked out 2026-11-18)
Status: approved by THJ 2026-11-18 (all chunks one after the other, he plays them together)

## Why

THJ's play feedback on round 2 ([`playtests/2026-11-17-cyclone-round2-play-check.md`](../playtests/2026-11-17-cyclone-round2-play-check.md), notes 1 to 4). Design: [`plans/2026-11-18-cyclone-round3-design.md`](2026-11-18-cyclone-round3-design.md). Decisions: D-566 (cast on an enemy shoves it one cell away from Lucy), D-567 (cells next to Lucy allowed), D-568 (beats approved).

## Goal

The Cyclone can be cast on an enemy's cell (the enemy is shoved one cell away from Lucy first), and the Whirl hit, the carry and the shove read as wind (grab, drag, fling, inhale, exhale), with fainter cross drawings.

## Acceptance criteria

- [ ] **Rule (C2).** Cast on a one-cell, non-Immovable enemy hostile to Lucy: that enemy is shoved one cell along the larger axis away from Lucy, then the Cyclone is planted on its old cell, then the cast Whirl plays (pull, reactions, hit). The shove is free (no damage), lands once (hazard on the landing cell fires, Watch answers a landing in Linda's lane, the enemy wakes, no Crippled damage, no hazard on cells crossed).
- [ ] Diagonal neighbour of Lucy (offset 1,1): the enemy goes to whichever of the two candidate cells is free; both free: along the row (x axis; the implementer confirms the grid's row axis and writes it in a comment-free test name).
- [ ] The enemy's cell is not offered (range highlight and click refused) when the shove cell is a wall, map edge, unit, walk-blocking planted entity or stashed entity; for heavies (Immovable tag or footprint larger than 1x1, via `CycloneHeavy`), large units, neutrals, allies and the family; and for any cell holding a planted entity, an enemy on it included. No fallback cell, no chain pushes.
- [ ] Empty cells are still castable exactly as before. Cells next to Lucy are castable on enemies (D-567).
- [ ] Family Super Time and the Steer's end-cell check keep the empty-cell rule (`CycloneRules.IsValidCastCell` is unchanged for its other two callers). An AI-controlled Lucy only picks empty cells.
- [ ] **Preview (C2).** Hovering a castable enemy cell draws the cross there, the enemy's ghost on its shove cell with the existing tether, damage segment and lethal skull on the ghost, the hazard ring if it lands on one, plus ghosts for what the Whirl pulls. The shove in the preview comes from the same planner move the execution uses (a test compares them). While aiming the cast, an enemy on a castable cell does not open the unit hover panel or an attack cursor; a refused enemy shows the normal panel.
- [ ] **Beats (C3).** Whirl: swell 0.1 s only before a pull; inhale 0.12 s (still-standing pullable enemies beside the Cyclone lean 35% of a cell toward the centre, ease-in; this replaces the swell when nothing is pulled); exhale and hit 0.08 s (snap back, ease-out, no overshoot; the hit lands as they arrive); recoil 0.06 s for moved units and heavies. A unit that already moved in this action (carried, shoved by the cast, pulled in) skips the inhale. Heavies never lean. No inhale when nobody is hit.
- [ ] Steer with riders: grab 0.08 s (riders lean 30%; the front enemy does not), drag at 0.15 s per cell (riders trail with a small lag and tilt, the front enemy is kicked ahead at the start of each step, a late joiner is grabbed during its step), fling 0.12 s to the landing cell (ease-out, small hop, stops exactly on the ghost's cell), then the one landing frame. The cast-on-enemy shove uses the same fling.
- [ ] Net time: a Whirl without a pull adds 0.0 s, with a pull +0.1 s, a Steer with riders +0.2 s (measure and report).
- [ ] No outcome and no order of events change from round 2: landings, pull, reactions, hit; the Watch order fix and the one-landing rule hold; round 2 play-check item 25 still holds (the player cannot act between the inhale and the hit). Burst check and the target list are taken after the inhale, so nothing is hit twice and a target that died or moved is not hit. A burst during a heavy's walk has no inhale.
- [ ] Abort (level end, Cyclone destroyed, a unit dying mid-beat) snaps every drawing back to its cell and leaves every unit plugged on a valid cell.
- [ ] **Alphas (C1).** Touching-cell tint alpha 0.18 (was 0.3), arm-tip chevron 0.45 (was 0.75), chevron flare 0.85 (was 1.0); `DimFactor` unchanged. The three values become serialized fields on the cross view so THJ can tune without code (code defaults equal the new values, so no prefab edit is needed).
- [ ] Compile clean; EditMode green except `AIRegressionTest.Baseline_MatchesCurrentAI`, whose inner failure count stays 43. Report the count before and after.

## Scope

In: the cast check for enemy cells, the shove, spawner order, preview, tests (C2); presenter beats and the input guard (C3); alpha fields (C1); docs.
Out: hold; per-cell pushes; fire flecks and hitstop (later levers); the strain wobble; changes to Super Time or the AI's cast choice; the one-Watch-per-action core limit; the AI regression re-baseline; any new `AbilityPreset`, new on-screen element or text.

## Touches

Systems: all in `Features/Player/Lucy/Scripts/Cyclone/`: `AEffectCycloneSpawner`, `CycloneRules` (new cast-only check beside `IsValidCastCell`), `CycloneCarryPlanner` (reused for the one shove), `CycloneCastPreview` and `CycloneCastPreviewAttach`, `CycloneCursor`/`CycloneAimState` (hover on enemy cells), `CycloneEntity.Whirl.cs` and `CycloneEntity.Steer.cs` (waits and presenter), `CycloneWhirlSteps`/`ICycloneWhirlSteps` and `CycloneSteerSteps`/`ICycloneSteerSteps` (recorder seams), `CycloneCrossView`. Core files that the Whirl path already uses (not edited here): `AEffectPusher`, `AEffectTransporter`, `AbilityDamagePreview`, `PlayerController`, `GridManager`. If any proves necessary (most likely for the input guard or the enemy hover, see C2 and C3), the implementer STOPS and reports the exact additive hook; that is a Tier 3 question to THJ. No core system in `tech/core-systems.md` is to change.
USPs: Family Roles (Watch on the shove landing), Synergies (bunching for Tempest Bloom, Explosive Crescendo, Shield Flare).
Docs: see "Docs to update".

## Approach

Chunks, each one implementer run, each its own commit. Order: C1 is tiny and independent (a visible quick win); C2 (rule) before C3 (beats) because the cast shove uses C3's fling, and C3 then upgrades it; C2 is the riskier one and goes before C3's feel work.

**Rules for every chunk:** read `conventions.md`, `tech/core-systems.md`, the design plan, the round 2 tech plan and `reports/cyclone-r2-c1.md` to `cyclone-r2-c4.md` for the existing code. Stop Play mode before editing scripts. No private IDs (D-xxx, plan names) in code, comments, tooltips, test names or commit messages. Keep line endings (the Cyclone files are LF) and any BOM. Prefer new partial-class files. Write the report to `reports/cyclone-r3-c<N>.md` from `templates/report.md`. Do not touch THJ's uncommitted files (`PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font).

### C1. Fainter cross drawings (sonnet)

Goal: the alphas above as serialized fields in `CycloneCrossView.cs` with code defaults at the new values. Check the existing view tests (colour or alpha asserts) and update them to the new values. No prefab or scene edit unless a serialized value already overrides the old constants (check `Cyclone.prefab`; if it does, a small YAML edit or editor script, say which).
Checks: existing cross tests pass; compile clean.

### C2. Cast on an enemy: rule, shove, preview (opus)

- **Cast check.** New static in `CycloneRules` (or a new partial file), e.g. `IsValidCastCell(GridCell cell, GridCell lucyCell, ...)`: empty-cell rule as today, or an enemy cell that passes the shove rules. It must read plain references only (worker-safe, like `CycloneCastPreview`), use the prefab's pull tag query and the caster's faction (a live Cyclone does not exist at cast time, so `IsPullable` cannot be used as is; share the filter by extracting its core into a plain-argument function and have both call it), and use `CycloneHeavy` for the heavy test. `IsValidCastCell(cell)` keeps its meaning for `CycloneSteerRules.CanEndOn` and Super Time (`LucyFactionRoleHandler`).
- **Direction.** One pure function: the shove cell for (Lucy's cell, target cell), larger axis, the diagonal tie rule above, returning "none" when blocked. Reuse `CycloneCarryPlanner.CanTakeStep`/`TakeStep` for the blocked test so the cast and the Steer's front shove are literally the same rule.
- **Spawner.** `AEffectCycloneSpawner.CheckTargetSelectionCondition` uses the new check; `Apply` does: shove (unplug, move the drawing, plug at the landing cell only, raise the move-end events Watch listens for, `EnemyAlertTracker.WakeMovedUnit`, exactly as the carry does) → re-check the cell is empty → spawn and plant → the existing Whirl. A unit that dies or vanishes during the shove must not leave a unit unplugged; if the cell is no longer valid after the shove, abort cleanly (re-plug, no Cyclone, no cooldown spent is not required: report what the code does and keep the existing "cast failed" behaviour). `HoldCastWhileWhirlPulls` and the turn-switch hold behave as today.
- **Target range cells.** The range highlight must include castable enemy cells and exclude refused ones (find where the spawner builds its target cells; if it only filters through `CheckTargetSelectionCondition`, no more is needed).
- **Preview.** `CycloneCastPreview` plans the shove with the same function, shows the enemy's ghost on the shove cell with tether, damage and skull on the ghost, the hazard ring if it lands on one, then the existing pull ghosts and damage for the Whirl run on the board after the shove (plan on a copy of positions with the shoved enemy moved). The HP bars show the Whirl hit only. Hovering a castable enemy while aiming the cast aims the cast (no unit panel, no attack cursor), the same fix as the Steer's (round 2 play-check item 20: find how `CycloneCursor`/`CycloneAimState` did it for the Steer and reuse it from Cyclone code). If that needs `PlayerController` or `GridManager`, STOP and report.
- **Order and Watch.** Under the known one-Watch-per-action limit, the shove's landing may take the cast's one Watch answer; accepted (design), do not change `ProcessFRApplyWaitList`.
- **Do not** make Super Time or the AI evaluator pick enemy cells. AI worker thread: nothing new reads Unity objects from AI code.
Tests (EditMode, recorder pattern from `CycloneCastTests` and `CycloneSteerTests`): every acceptance case above (direction on each axis and the four diagonal cases, tie with one or both free, blocked by wall, edge, unit, planted entity, stashed entity; heavy, large, neutral, ally, family, Immovable not offered; planted-entity cell with an enemy refused; empty cell as before; adjacent cell allowed; hazard on landing; Watch lane landing; one landing; no Crippled damage; shove then Cyclone then Whirl order; preview plan equals executed shove; `IsValidCastCell` unchanged for Steer and Super Time).

### C3. The beats: inhale, exhale, grab, drag, fling (opus)

- **Constants** as serialized fields on `CycloneEntity` with the code defaults of the acceptance list (swell moves from 0.2 s to 0.1 s; keep `swellSeconds` as the field and change its default only if the prefab does not override it; check `Cyclone.prefab`; if it does, edit that one value).
- **Presenter state per action.** Track which units moved in this action (carried, shoved by the cast, pulled in) so the inhale skips them and heavies never lean. The lean moves a visual child, not the unit's root, where one exists (the hover and projectiles read the root); if the unit has no visual child usable for this, move the root as the round 2 glide does and say so in the report. Every drawing is restored to its cell on every exit path (`try/finally`); abort snaps back.
- **Whirl.** `WhirlRoutine`: pull as today; reactions as today; then inhale (all together), then recompute the burst check and the target list, then exhale and the hit as the lean snaps back; recoil for moved units and heavies. If nobody is hit, no inhale and no wait. The inhale replaces the swell when nothing is pulled.
- **Steer.** Grab before the glide (riders only); drag with the trailing lag and tilt; fling to the landing cells with a small hop and no overshoot, then the single landing frame. The cast-on-enemy shove calls the same fling. A rider that joins part-way is grabbed during that step with no extra time.
- **Input guard.** The cast releases Lucy's action when the pull ends (`HoldCastWhileWhirlPulls`), so the player could act inside the inhale. Choose the smallest means: keep the cast's hold until the hit lands (preferred, Cyclone code only), else a short input lock like the turn banner's. If the lock needs `PlayerController` or `PlayerInputController` (core), STOP and report; do not edit them. Round 2's check 25 must still pass.
- **Seams.** Add the new waits and presenter calls behind the existing `ICycloneWhirlSteps` and `ICycloneSteerSteps` so tests can record them without time.
- **Burst.** Unchanged: no inhale, neighbours recoil with the hit.
Tests (EditMode): the unit-moved set (carried, shoved, pulled skip the inhale; still-standing pullable ones lean; heavies never lean), no inhale when nobody is hit, burst check and targets computed after the inhale (a unit killed or moved during the inhale is not hit, a burst during the inhale does not double hit), outcome and event order identical to round 2 (reuse the round 2 recorder tests), abort restores every drawing and leaves units plugged, the hold lasts until the hit. The look and the times need THJ's play check; the implementer reports measured durations from the recorder.

### C4. Docs (coordinator and designer)

See below. After THJ's play check.

## Risks

- [x] **Preview trust:** the cast shove, the preview and the execution share the carry planner's move; a test compares them.
- [x] **Core touch points:** the enemy-hover fix and the input guard may want `PlayerController` or `GridManager`; written to avoid them, the implementer stops and reports the minimal additive hook, I ask THJ (Tier 3). The rule itself needs no core change.
- [x] **AI worker thread:** the cast check and the shove planner read plain references only; an AI-controlled Lucy is kept to empty cells; AI count must stay 43.
- [x] **Statics and caches:** none planned; any new static gets a `ResetPlayModeState` hooked in `PlayModeStaticReset.cs`.
- [x] **Event subscriptions, coroutines and abort cleanup:** presenter and holds released in `finally`; previews unbind on cancel and level end; a shove or carry aborted mid-way leaves no unplugged unit.
- [x] **Double hit and input race:** burst check and targets after the inhale; no action between inhale and hit (see C3).
- [x] **Assets:** `Cyclone.prefab` may override `swellSeconds` or the cross colours; check before changing defaults. No new ability asset, no text change in code (the Cyclone's description clause "Cast it on an enemy to knock it away." is a narrative proposal for THJ's approval, applied after the play check).
- [x] **Serialized field renames, save data:** none.
- [x] **Creep:** C1 (data), C2 (rule) and C3 (feel) are separate commits so THJ plays one lever at a time if he wants.
- [x] **Other branches:** Cyclone work lives on `thj/cyclone` only; its merge carries it. THJ's test-settings commit `b88c004f1` (intros off) stays until the merge to `main`.

## Gates

Per chunk: compile clean (Unity MCP console), EditMode green except the known red (count 43 reported before and after), `miso-reviewer` after each chunk (C2 and C3 for sure), then `miso-verifier` for the final gate after C3. THJ play check: yes, needs his time, once after C3 (checklist added to `playtests/2026-11-17-cyclone-round2-play-check.md` or a new file `playtests/2026-11-18-cyclone-round3-play-check.md`; I write it). Win playthrough: no. Grids: no changes. Round 2's play check is still unmarked; THJ's results on it are wanted before the round 2 commits are treated as final.

## Docs to update

- Designer (after the play check): GDD `characters/lucy.md` (LU-3, LU-4, LU-6, value table), `design/cyclone-redesign.md` round 3 note.
- Narrative: one clause for the Cyclone's description (proposal, THJ approves).
- Coordinator: `tech/combat-architecture.md` (cast shove, presenter beats), `build-log.md`, `status.md`, `branches.md`, `decisions.md`; note the Claude Docs mirror sync owed for `gdd/characters/lucy.md`.

## Commit plan (proposed after THJ's play, one yes each, no attribution trailers, no private IDs)

1. C1 fainter cross drawings.
2. C2 cast on an enemy: rule, shove, preview, tests.
3. C3 beats and input guard, tests.
