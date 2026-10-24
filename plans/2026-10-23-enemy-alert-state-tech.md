# Enemy alert state: tech plan

Size: L    Tier: 3 (new mechanic; THJ approves this plan before dispatch)    Assigned to: `miso-implementer` (C1 opus, C2 and C3 sonnet) → `miso-reviewer` → `miso-verifier`
Branch: all (built on `main`)
Status: approved (THJ 2026-10-23), C1 done (commit 2 held), C2 in progress

## Why

THJ 2026-10-23: enemies should hold their tile and not approach until the family comes into sight or something alerting happens near them. Design: `plans/2026-10-23-enemy-alert-state-design.md` (rules EN-12 to EN-17), with THJ's answers D-154 to D-157 on top. **Where the design and these decisions differ, the decisions win.**

## Goal

Every placed and spawned enemy starts Unaware and skips its turns until sight, noise or spread wakes it; the player sees who is Unaware and the moment each one wakes.

## The rules as decided (what the code must do)

1. **Who:** only units of factions hostile to the player faction. Allied AI (Toba ally) and neutrals (Deer) are never Unaware. Rule is **on by default in every level**; no global switch (D-154).
2. **Start:** at level start every such unit is Unaware, except: the level has "all enemies start alert"; the unit has "starts alert"; the unit is "always alert" (bosses); or a hostile unit is already within its sight (Alerted with no pop).
3. **Spawned units follow the same rule** (Shaman summons, corruption pool, wave spawns, Worm split children): Unaware when they appear, Alerted at once (no pop) if a hostile is already in sight (D-156). Revived units keep their previous state.
4. **Sight (EN-13):** Manhattan steps from the enemy's nearest footprint tile, through walls and units. **sight = max(5, walk reach + longest attack reach)** (D-157); a per-unit override replaces it. Walk reach = largest Move ability radius; attack reach = largest radius among its attack abilities. Checked when a hostile unit **stops** on a tile (end of a walk, push or pull, Blink, Dance, Command move, appearing on the board: deploy, decoys) and, as a safety net, at the start of each enemy turn. Passing through mid-walk doesn't count. Hostile units include decoys and protectees.
5. **Alert range:** ceil(sight / 2), at least 2 (so at least 3 with the floor of 5).
6. **Noise (EN-14):** (a) any ability that targets or affects the enemy (damage, status, push, Command; evaded hits too), from anyone, or anything that damages it; (b) an ability used by a player-side unit (Bergson, ally) that affects a tile within the enemy's alert range (the affected tiles, not the flight path). Hazards, status ticks and enemy abilities near it make no noise.
7. **Spread (EN-15):** when an enemy wakes, every Unaware enemy within *its* alert range wakes too, recursively, at that moment only. The Black Claw's Pact Leader call also wakes the units it calls.
8. **Timing (EN-16):** woken in the family's turn → acts on the next enemy turn. Woken during an enemy turn → doesn't act in the rest of that turn, acts on the next one.
9. **Unaware does nothing:** no move, attack, heal or summon. Never goes back to Unaware.
10. **Masher counter:** the hit wakes it first; it then counters as today.

## Architecture

- **The gate is data, not core code.** A new GTag `Status.Unaware` (`showInGame` on, placeholder icon) is added to `GTagRegistry.asset`, and to `skipTurnTagsQuery` on `Content/Controllers/AIController.prefab` (next to `Status.Stunned`). `FactionControllerBase.IsUnitTurnSkipped` then keeps Unaware units out of `PhaseData.ToPlayUnits` and `AIFactionBrain.UpcomingTurnOrder` (turn and next-targets prediction). The tag also gives the info-panel line. No change to `GUnit`, `AIController`, `AIFactionBrain` or `AIUnitBrain`. Check the query's policy means "any entry matches" with two entries.
- **Timing falls out of the gate if** the enemy turn's play list is built once at turn start (`PhaseData.Reinitialize(IsUnitTurnSkipped)`, `FactionControllerBase.cs:224`). Verify that; if the list is rebuilt mid-turn, defer the tag removal for enemy-turn wakes to the enemy turn's end.
- **Rules as pure C#:** `EnemyAlertRules` (static, no Unity objects): sight from walk/attack reach and override, alert range, footprint Manhattan distance on cell coordinates, the spread closure. EditMode-tested.
- **One runtime tracker:** `EnemyAlertTracker` (MonoBehaviour, one per combat level; new folder `Core/Systems/EnemyAlertSystem/`, or `Features/` if that fits conventions better: implementer's call, note it in the report). Main thread only. It:
  - initialises after `CombatLevelRunHandler` has initialised the level's units (find the right hook; `CombatLevelRunHandler.cs:246-258,375`);
  - subscribes to `GlobalEventBus`: `unitEndMoving` (and any other "unit stopped" path: pusher end, Blink/teleport landings, decoy and deploy appearance via `unitBorn`), `unitBorn` (spawns: rule 3), `onAbilityEffectPerformedOn` (entities and cells, caster = `ability.Owner`), and a damage path covering effect-less abilities (`GotTargeted` / `ability.Targets` fallback), `turnStarted` (enemy turn safety net);
  - unsubscribes on disable/destroy and level end; no statics (if one is unavoidable: `ResetPlayModeState()` + `PlayModeStaticReset`).
- **Overrides as small components, not `GUnit` fields:** `EnemyAlertSettings` on a unit prefab or placed instance (`startsAlert`, `alwaysAlert`, `sightOverride` (0 = derived)); `LevelAlertSettings` on a level root (`allEnemiesStartAlert`), following the `LevelStartFPFiller` pattern.
- **Visuals (C2):** a world marker over each Unaware unit (placeholder sprite, sorted like the mini HP bar), removed on wake; a "!" pop on wake, staggered along the spread chain (about 0.1 s per step, one serialized field), using the floating-text path `GUnit.ShowTagGained` uses. No pop for level-start or spawn-time wakes.

## Chunks (one implementer run each, one or two commits each)

### C1: rules, tag gate, tracker, overrides (opus)

- `EnemyAlertRules` + EditMode tests; `Status.Unaware` tag + `AIController.prefab` skip query; `EnemyAlertTracker`; `EnemyAlertSettings`, `LevelAlertSettings`.
- Commits: (1) rules + tests; (2) tag, prefab query, tracker, settings components.

### C2: readability (sonnet)

- The Unaware marker and the staggered "!" pop. Commit on its own.

### C3: data pass (sonnet)

- `EnemyAlertSettings.alwaysAlert` on boss prefabs (Goblin Queen, Mountain Deev, the duel's enemy Toba); `LevelAlertSettings.allEnemiesStartAlert` on: M4 Queen level, M10, M12, M4 Level2-C2, Level2-C3-1, Level2-C3-2, M3 Mark Intro C1 (survive waves), the Dom duel, `LevelHomeDefence`. Implementer confirms each path and lists them. Commit on its own.

### C4: ranges as attributes, Unaware range preview, marker size (opus) — added 2026-10-24 after THJ's first play check (D-164, D-165)

Replaces rule 4's formula and rule 5. Rules 1–3 and 6–10 stay.

1. **Two unit attributes**, `Sight` and `AlertRange` (follow the existing attribute naming and registry). Defaults on `UnitBase.prefab`: sight 3, alert range 2. `Unit_MasherGoblin.prefab`: sight 2. Read them through the normal attribute API, so attribute modifiers apply. Read them at check time, not cached at registration.
2. **Remove** the walk + attack formula, `SightFloor`, `MinAlertRange` and `EnemyAlertSettings.sightOverride`. Clean the `sightOverride` lines from the three boss prefabs. Values below 0 are treated as 0.
3. **`LevelAlertSettings`** gets `sightBonus` and `alertRangeBonus` (int, may be negative; the result is clamped at 0), applied to every enemy in that level.
4. **Range preview:** hovering an enemy, and Shift, draw its sight tiles and its alert-range tiles in two distinct tints, **only while it is Unaware**. Use the existing hover and Shift preview layers (`GridCell.ShiftPreview.cs` and others) through their current API. If this needs a change to `GridCell` or another core system, stop and report the smallest option.
5. **Marker size:** a fixed world size (serialized, about 0.35 of a tile) whatever the sprite's resolution, placed above the unit's head and the mini bar.
6. Update the tests (the rules no longer have a formula; add tests for the bonus and clamp).

Acceptance: changing `Sight` on a prefab or the level's `sightBonus` visibly changes when that enemy wakes and the drawn tiles. The preview never shows on an Alerted enemy. The marker is small and above the head.

Then THJ play-checks (see Gates). **Later, not in this approval:** Shift on an Unaware enemy shows its sight area; "this move will wake X" marker on the move ghost; the ability-targeting wake preview; sound and barks; a level-by-level pass.

## Acceptance criteria

- [ ] A placed enemy with no hostile within sight takes no action on enemy turns, and is absent from the next-targets prediction.
- [ ] Sight = max(5, walk + longest attack reach) or the override; alert = ceil(sight/2), min 2 (tests).
- [ ] A Bergson stopping within sight wakes it; passing through mid-walk doesn't (play).
- [ ] Hitting it from anywhere (incl. Linda from range, a Family Role follow-up, a Duo) wakes it; a player ability hitting tiles within its alert range wakes it; a hazard tick doesn't (tests where pure, play otherwise).
- [ ] Spread wakes Unaware enemies within the waker's alert range, recursively (tests).
- [ ] Woken in the player's turn: acts next enemy turn. Woken during the enemy turn (Masher counter, Lucy's role): doesn't act until the next enemy turn (play).
- [ ] Spawned enemies start Unaware unless a hostile is in sight on arrival.
- [ ] Allied Toba and Deer are never Unaware; bosses and flagged levels start alert.
- [ ] An unalerted Masher hit by an adjacent attack wakes and counters as before.
- [ ] Unaware marker visible; "!" pop on wake, staggered along a chain; no pop at level start.
- [ ] No new `GUnit`, `AIController` or AI-brain code; no utility graph, variable or AI ability edits.
- [ ] Compile clean; EditMode all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: rules 1–10, the tag gate, tracker, overrides, marker and pop, data pass.
Out: global on/off switch (D-154), sight-area preview, move/ability wake previews, sound, barks, level rebalancing, any AI graph change.

## Touches

Systems: AI turn flow (core, behaviour via data only: `AIController.prefab` skip query), `GTagRegistry` (data), `GlobalEventBus` (subscriber only), new tracker; level prefabs and boss prefabs (C3).
USPs: Family Roles, Duos and Synergies unchanged as rules; they make noise like any ability. Home: none.
Docs: designer writes EN-12 to EN-17 into `design/gdd/enemies.md` with D-154 to D-157 applied (spawns follow the rule, sight floor 5, no global switch) and the missions-page level list; coordinator updates `tech/combat-architecture.md` (tracker, tag gate) and `tech/core-systems.md` (note on the AI skip query); narrative proposes player-facing names (working names Unaware / Alerted).

## Risks

- **Missed "stop" paths:** a push or teleport that raises no `unitEndMoving` → the enemy-turn-start sweep catches it a turn late. Implementer lists every stop path found and which event covers it.
- **Event order vs the Masher counter:** wake must land before the counter checks; the counter runs after the current action (D-100), so it should. Verify.
- **Worker thread:** the worker reads `TagSet` (already does, for Stunned). Tags are changed on the main thread only, never while a job is computing? Check whether `TagSet` is safe to change mid-job; if not, defer tag changes until `AIFactionBrain` is idle or during the player's turn only, and say so.
- **Prediction refresh:** after a wake in the player's turn, request the next-targets prediction again so the woken enemy's targets show.
- **Balance:** every Generic Level changes pace. THJ's play check decides.
- **`AIRegressionTest`:** no graph, variable or ability edits planned, so it shouldn't move; if a new tag or prefab change shifts it, report it; **never re-baseline**.
- **Other branches:** `thj/home-test` needs this when it takes `main`.

## Gates

Compile / EditMode (known red only) / reviewer per chunk / play check: yes, THJ after C3 (a Claw level, an Archer level, a Masher level, one protect level) / docs above.

## Commit log

- C1 commit 1 `3378acaca` feat(enemies): enemy alert rules with edit-mode tests (review APPROVE after fix round 1; EditMode 711/712, known red only).
- C1 commit 2 (tag, prefabs, tracker, settings): built and approved, held for THJ's play check after C3.
