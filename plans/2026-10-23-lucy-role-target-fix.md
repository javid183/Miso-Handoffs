# Lucy's role follow-up hits the wrong enemy: fix plan

Size: S    Tier: 3 (core `GUnit` change; decided D-152)    Assigned to: miso-implementer
Branch: all (built on `thj/quick-wins`)
Status: approved, ready to dispatch

## Why

THJ's play test (2026-10-23): Lucy's Family Role follow-up often hits an enemy other than the one another member just attacked. Cause: [`reports/lucy-role-wrong-target.md`](../reports/lucy-role-wrong-target.md).

## Goal

Lucy's follow-up hits the enemy the triggering action actually targeted; a neighbour only when no targeted enemy qualifies, and the nearest one.

## Acceptance criteria

- [ ] Linda's Bow shot or Explosive Crescendo on B, with C (Linda-tagged or splashed) above or below B, earlier in turn order: Lucy hits **B**.
- [ ] Linda shoots C, then B in the next action: Lucy hits **B**.
- [ ] Lucy has already followed up on B; Linda hits B again: Lucy hits **B** (not skipped, not a neighbour).
- [ ] When the triggering action's targeted unit can't be hit (out of Lucy's zone, downed), the fallback picks the nearest qualifying enemy to the target cell within a tight radius (the triggering attack's own area, not Lucy's role radius), or nothing.
- [ ] Mark's actions still trigger Lucy as before (the reason the fallback was added, `fc4a7dad0`); the radius-4 case from `4f27914d0` still fires.
- [ ] `GUnit.GetMostRecentAttacker()` returns the unit that attacked last, also when it attacked before (moved to newest), with the memory size from `GlobalSettingsSO.unitsAttackMemorySize`.
- [ ] Barks that use the instigator (`BarkManager.cs:164`) still work.
- [ ] Compile clean; EditMode green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not re-baselined).

## Approach

Two commits, core first.

### F1. Ordered attacker memory (core `GUnit`, `opus`)

- `GUnit` (`Core/Units/Runtime/GUnit.cs` ~249, 586-594, 692-695): replace the `HashSet<GUnit>` with an ordered list: on record, remove the attacker if present, append it, evict from the front while over the memory size; `GetMostRecentAttacker()` returns the last (or null). Prefer a new partial file for the logic if it reads cleaner. Same public API; behaviour fix only.
- Pure helper (e.g. `AttackerMemory` static/plain class) with EditMode tests: re-add moves to newest; eviction drops the oldest; size 2; empty → null.
- Thread safety: check whether the AI worker thread reads attacker memory (e.g. `RememberAttack`, memorable attacks, blackboard); keep it main-thread-safe and Unity-object-API-free if so.

### F2. Lucy's candidate ranking (`LucyFactionRoleHandler`, `sonnet`/`opus`)

- `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs:62-92`: keep the existing filters (not downed, in Lucy's zone, `GetMostRecentAttacker() != Unit`), then rank:
  1. units in the last action's targets, or standing on its target cells;
  2. only if none: units hit by the triggering action near its target cells, within a tight radius (the triggering ability's own area/radius, falling back to 1), not Lucy's role radius;
  3. ties broken by distance to the target cell, then a stable order.
- Pure ranking function with EditMode tests covering the acceptance cases (direct target beats earlier-listed neighbour; fallback nearest; no candidate → none).
- Keep the Mark trigger working (check his actions' target types).

## Risks

- **Core `GUnit`:** a behaviour fix with the same API; its own commit. Only `LucyFactionRoleHandler` and `BarkManager` read the memory (grep 2026-10-23).
- **AI thread:** confirm nothing on the worker thread reads the memory.
- **Fallback too tight:** the Mark and radius-4 cases from the two earlier commits must still fire (play check).
- **Statics:** none.

## Gates

Compile; EditMode (known red only); reviewer (F1 core); **THJ's play test before the commits** (the repro from the investigation report, plus Mark triggering Lucy).

## Commit log

(filled in as committed)

- Built (`reports/lucy-role-target-fix.md`): F1 `RecentAttackerMemory` (ordered, locked: the AI worker reads it via `TargetRecentAttackFactor` → `GetRecentAttackFactor`, which now reflects real recency), 10 tests; F2 `LucyRoleTargetRanking` (direct targets first, fallback within the action's own area measured from its effects, +1 when the action pushes so Mark's Vault gets 2, ties by distance), 15 tests. EditMode 649/650 (known red, same 38 checks). In review. THJ's six assets were committed by THJ as `6ef6313bf`.
