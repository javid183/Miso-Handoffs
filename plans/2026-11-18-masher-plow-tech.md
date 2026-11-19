# Masher Goblin: the counter step plows through units

Size: M    Tier: 3 (changes an enemy rule; Masher handler; THJ approved the design 2026-11-18, D-566)    Assigned to: miso-implementer (opus)
Branch: `main` (the Masher handler is the same on `thj/cyclone` except the Cyclone pass-through in its walk; expect a merge conflict there later, see Risks)
Status: built, committed (`89bd4763e`, `62ed9b895`, `db9cf6ae9`); play check pending

## Why

THJ's request (2026-11-18): "change the masher goblin's reaction in a way that it pushes back any unit on its way (enemy or player unit that is not the attack target)". Today the counter step needs its whole 2 x 2 footprint on empty cells, so any unit standing there stops the step (`MasherGoblinFactionRoleHandler.Counter.cs`, `TryPlanAnswer`: `Unit.IsFootprintEmpty(cell)`). Rules it builds on: `plans/2026-10-20-masher-reckless-tank-design.md` (D-092 to D-098).

## Goal

When the Masher's counter step enters cells held by other units, it shoves each of them one cell onward in the direction it moves, then takes the step.

## Decisions (THJ, 2026-11-18, D-566)

1. **Scope:** the counter step only. The Masher's own-turn walk is unchanged.
2. **Nowhere to go:** a pushed unit's next cell must be free (walkable for that unit, empty, not outside the grid). If any unit in the entered cells can't be pushed, that step candidate is not valid (as an occupied cell is today); the planner tries the other candidates, and with none left the Masher doesn't step. No chain pushes.
3. **Damage:** none. Displacement only. No per-cell damage, no Crippled penalty, no status.
4. **Reactions:** a pushed unit starts no Family Role (no Linda lane shot, no Mark or John reaction), whatever the `counterCanProvokeFamilyRoles` toggle says. The Masher's own step and slam keep following that toggle.

Plan assumptions (not asked; report if any turns out wrong):
- Only the provoker is exempt from being pushed; it is never in the entered cells anyway (a candidate that overlaps the provoker is skipped today, keep that).
- Only single-cell units are pushed. A multi-cell unit that isn't Immovable (e.g. a 1 x 2 boss) counts as "can't be pushed" and blocks the candidate. Immovable units (another Masher, the Deev) also block (CR-18).
- Things that are not units (planted entities, obstacles, stashed items) are not pushed and block the cell as today.
- Dead units are not on the grid. A Downed unit that still holds its cell: treat like any unit (push it) unless the code shows Downed units don't occupy; report what you found.
- The push direction is the Masher's step direction (a cardinal single step: the footprint shifts one cell). Only single-tile cardinal steps can plow. A longer or non-straight step (a walk with more range) is planned as today: it needs empty cells.

## Acceptance criteria

- [ ] A Masher countering with a free path behaves exactly as before (same step, same slam, same preview).
- [ ] A unit (enemy or player, not the provoker) standing in a cell the Masher's footprint would enter is moved one cell onward in the step direction, then the Masher steps into the freed cells.
- [ ] With a 2 x 2 Masher stepping one cell, up to two units (the two cells on its leading edge) are pushed, each to its own next cell.
- [ ] If any unit in the entered cells has no free next cell, is Immovable, or is multi-cell, that candidate is skipped; the Masher takes another candidate or doesn't step.
- [ ] Pushed units take no damage and get no status.
- [ ] A pushed unit starts no Family Role, with the toggle on or off. The Masher's own step and slam still follow the toggle.
- [ ] The hover preview, when the plan includes pushes, shows each pushed unit's destination (ghost or tile highlight, implementer's choice, consistent with the existing preview style) in addition to the step ghost and slam tiles. The preview and the real answer use one plan (`TryPlanAnswer` and the new rules), as today.
- [ ] The answer still finishes (the pump's `_answerRunning` is cleared and the turn-switch hold released) if a pushed unit dies, is destroyed or can't move mid-way; no stalled turn.
- [ ] The Masher's chain cap, queue, Duo and Stun/Crippled rules are unchanged.
- [ ] New EditMode tests pass; the EditMode suite is green except `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: pure plow rules (which cells are entered, the push direction and destinations, validity) + tests; the plan change in `TryPlanAnswer`; pushing before the step in `Activate`; the preview; role suppression for the pushes; a push asset with no effects on move if the existing pusher needs one; docs.
Out: the Masher's own-turn walk and AI; pushing Immovable or multi-cell units; chain pushes; push damage or statuses; `thj/cyclone` (not touched); changes to `AEffectPusher`, Family Role handlers or other shared Core code (see Risks: stop and report instead).

## Touches

Systems: Masher Goblin handler and rules (`Features/Enemy/Masher Goblin/`); reads the grid (`GridCell`, `GUnit` footprint APIs) and `AEffectPusher` (core, used, not changed); `FactionRoleProvocationSuppression` (core, used, not changed unless it needs only an additive overload: ask first).
USPs: Family Roles (reactions are kept from firing on pushes).
Docs: `design/gdd/enemies.md` (Masher counter rule, new EN entry or edit), `design/gdd/combat-rules.md` (CR-18 note: the Masher's plow is a forced move that never moves Immovable units), `tech/combat-architecture.md` (Masher section), `plans/2026-10-20-masher-reckless-tank-design.md` (a revision note), `decisions.md` (D-566), `build-log.md`, `status.md`.

## Approach

Two chunks, two commits. Read first: `MasherGoblinFactionRoleHandler.Counter.cs` (`TryPlanAnswer`, `Activate`), `.Preview.cs`, `MasherCounterRules.cs`, `Core/Systems/AbilitySystem/Effects/Runtime/AEffectPusher.cs` (`TryMoveTo`, `TryGetPushPreview` with `isEmpty`), `FactionRoleProvocationSuppression.cs`, `FactionRoleHandlerBase.cs` and the Mark and Linda role handlers (how they trigger).

**C1: rules and tests (sonnet).** New file `MasherPlowRules.cs` beside `MasherCounterRules.cs`, pure (Vector2Int and plain flags, no Unity-object APIs, no state). Suggested shape: given the Masher's current footprint coordinates, a cardinal step direction, and a lookup of what is on each cell (empty, pushable unit, blocker), return whether the step is allowed and the list of (from, to) pushes. Tests in `Editor/MasherPlowRulesTests.cs`: free path, one unit pushed, two units pushed (2 x 2 leading edge), next cell blocked, next cell off-grid or non-walkable, Immovable or multi-cell blocks, the provoker's footprint overlap rejected, step into the Masher's own old footprint cells is not "entered".

**C2: runtime (opus).** In a new partial file `MasherGoblinFactionRoleHandler.Plow.cs` (prefer new partials over editing big files; small edits to `.Counter.cs` and `.Preview.cs` are fine):
1. Planning: in `TryPlanAnswer`, candidates whose entered cells hold only pushable units (per C1) become valid and carry their push list; `RankStep` is unchanged (a plow cell ranks like a free one). Find how the walk's cell set is built: if `ComputeTargetSelectionCells(_walk, ...)` drops occupied cells, derive the one-cell cardinal steps from the footprint and the walk's own range and feasibility instead (do not widen the Masher's reach: the step stays the walk's 1 tile).
2. Executing: in `Activate`, before the walk, push each unit with `AEffectPusher.TryMoveTo` (owner = the Masher, destination from the plan), wait for all to finish, then run the walk. Use an `AEffectPusher` asset with no `onMoveEffects` (so no damage); if no such asset exists, create one with the existing builder (`MasherCounterPresetBuilder` or a new editor builder, no hand-edited YAML beyond a one-line reference) and reference it from a serialized field on the handler, set on the Masher prefab. Re-validate just before pushing (a unit may have moved); if the plan no longer holds, fall back to no step and still finish the answer (slam only if already adjacent).
3. Safety: every path out of the push wait must clear `_answerRunning` and the turn-switch hold (dead or destroyed pushed unit: `TryMoveTo`'s `onFinished` fires on death; add a frame or time guard). `StopCounter` also drops any push in flight.
4. Roles: the pushes must not start Family Roles whatever the toggle says. First find how Mark's and Linda's handlers decide (events they listen to, `FactionRoleProvocationSuppression.InvolvesSuppressedAction`). `AEffectPusher` raises `unitStartMoving`, `unitMoveTileStep` and `unitEndMoving` on the global bus. If that can be done inside the Masher's files (e.g. listing the push in the suppression set for its duration), do it. **If it needs a change to a Family Role handler, `AEffectPusher` or `FactionRoleProvocationSuppression`'s behavior, stop and report to the coordinator with the options.**
5. Preview: in `.Preview.cs`, when the plan has pushes, show each pushed unit's destination, using the same plan that `PlanAgainst` returns. Clear it in `ClearReactionPreview`.
6. Tests: any logic that can sit in pure rules does (C1). Add EditMode tests for plan integration if the grid can be built in a test the way `MasherCounterQueueTests` or other existing Masher tests do; otherwise list what only a play check can show.
7. New statics: none expected. If a static is added, add its `ResetPlayModeState()` and the call in `PlayModeStaticReset.Reset()`.

Commits (THJ's yes each, coordinator proposes): C1 rules + tests; C2 runtime + preview + any asset and its `.meta`. Then the docs live in `claude-handoff/` only.

## Risks

- Core: the Masher handler is a core-systems line (counter rules). Public API of `MasherCounterRules`, the handler and `AEffectPusher` must not change; only additive new members.
- AI: `MasherCounterRules` is not read from the AI worker thread; keep it that way. The Masher's own-turn behavior is untouched, so `AIRegressionTest` should not move (it is known red anyway; do not re-baseline).
- Coroutines and events: the push wait lives inside the answer; it must clear on abort (see C2.3).
- Prefab or asset edits: only the pusher asset and one serialized reference; use the editor builder. Prefab files can't be checked in the open editor by text; verify in the editor.
- Family Roles chain (decision 4): the one place that may force a change outside the Masher's files; stop and report rather than editing role handlers.
- Other branches: `thj/cyclone` changes the counter's walk (heavy enemies pass through the Cyclone, CR-58) and lacks 6 recent `main` commits. This work will conflict in `.Counter.cs` when the branches meet; note it in `branches.md`. Keep the edits in `.Counter.cs` small and put the logic in the new partial.
- `thj/home-test` and others: will need this when they take `main`; no extra work now.

## Gates

Compile / EditMode suite (editor is open: Test Runner, or the Unity MCP `run_tests`; all green except `AIRegressionTest.Baseline_MatchesCurrentAI`) / review (miso-reviewer after each chunk) / play check: **yes, short (THJ's time)**: provoke a Masher with a goblin and a family member in its way (corner, wall, two units on the leading edge, an Immovable one) / docs to update: those listed in Touches (coordinator).
