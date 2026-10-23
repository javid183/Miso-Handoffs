# Lucy's role follow-up hits the wrong enemy: investigation

Investigator: Explore agent (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins`.
Bug (THJ, play test): Lucy's Family Role follow-up often hits an enemy other than the one another member just attacked (e.g. Linda hit two enemies; Lucy fired at one "in the row above").

## Root cause

Lucy stores no "last attacked" unit. Each check, `LucyFactionRoleHandler.PrepareTargets` (`Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs:62-92`) rebuilds a candidate set from the last completed action's targets (**a cell** for Linda's attacks), a loose "near that cell" clause, and each enemy's `GetMostRecentAttacker()`, then returns the **first enemy in faction list order** (`FactionRoleRules.FirstMatchAcrossGroups`, `FactionRoleRules.cs:36-48`; `AliveUnits` = `PhaseData.OwnedUnits` sorted by `TurnOrder`, `FactionControllerBase.cs:25,129`). Nothing prefers the enemy actually hit.

1. **Over-broad fallback, picked by list order (primary; verified).** Lines 82-86 accept any enemy whose most recent attacker is the acting unit (Linda) and that stands within Lucy's **role radius** (3, `Adjacent`, `Lucy_Ability_FactionRole.asset`) of Linda's target cell. The row above qualifies easily, and wins if it is earlier in `AliveUnits`.
2. **`GUnit.GetMostRecentAttacker()` is unreliable (verified in code; ordering inferred from the runtime).** `RecordGettingTargeted` (`GUnit.cs:586-594`) adds to a `HashSet<GUnit>` (memory size 2, `GlobalSettings.asset:35`) and removes `First()` on overflow; `GetMostRecentAttacker` returns `.Last()` (`GUnit.cs:692-695`). Re-adding an existing attacker doesn't move it, and freed slots are reused, so `Last()` is often Lucy or stale. That **excludes the real target** (line 79, `!= Unit`) and **qualifies stale neighbours** (line 84, `== lastOwner`). Never cleared per turn/action.

- Linda's Bow Attack (`targetType 7`, the Cell flag wins at `FactionControllerBase.cs:564-565`) and Explosive Crescendo (Cell, `applyMode 1` Surrounding, splash) target cells, so line 80 never matches a unit, line 81 matches the occupant, and lines 84-86 are always live. Splash victims are tagged with Linda as attacker (`AEffectBase.cs:100-114`, `AEffectCompound.cs:161-163`).
- Trigger: `Unit_Lucy.prefab` `triggerEvents: 4` (OnActionComplete), `activationMoment: 1`; `GlobalEventBus.cs:168` → `CombatLevelRunHandler.cs:943-956` → `FactionControllerBase.cs:139-193` → `FactionRoleHandlerBase.cs:138-145`. The event's argument is ignored; everything is read from `SessionLogs.Instance.LastActions[0]` at evaluation time.

## Mechanisms

- **A (deterministic, no stale data):** Explosive Crescendo on B's cell splashes C above. Both have most recent attacker Linda; B matches line 81, C matches 84-86; if C is earlier in `AliveUnits`, Lucy hits C. Same with two Bow shots: shoot C, then B → Lucy hits C.
- **B (real target excluded):** after Lucy followed up on B once, B's `Last()` is stuck on Lucy, so line 79 rejects B on Linda's next hit; Lucy falls through to a Linda-tagged neighbour within 3, or doesn't trigger.

## History (read-only git)

- `fc4a7dad0` (2026-09-30) added the fallback (Radial ≤ 2).
- `4f27914d0` (2026-10-07, THJ, "faction role not firing at 4 radius") widened it to Lucy's zone radius and traverse mode: likely why it became frequent (inferred).
- `5b401cc80` (2026-10-18) `FirstMatchAcrossGroups` over all hostile factions; same first-match semantics.
- Ruled out: row/column swap or off-by-one (no coordinate code on this path; `OccupiedCells` handles multi-tile); John's relay.

## Secondary suspects

1. `LastActions[0]` is the oldest completed entry, not the newest (`CombatLevelRunHandler.cs:60-70`): low risk.
2. The wait list is processed in reverse and reads the live log (`FactionControllerBase.cs:153-180`).

## Fix direction (not written)

1. Rank candidates: units in the last action's targets or on its target cells first; only then a fallback; ties by distance to the target cell, not list order.
2. Build the fallback from this action's actual victims (`CombatLevelRunHandler._affectedAbilityEffectPerforms`, fed by `onAbilityEffectPerformedOn`, lines 792-796), or at least a tight radius (the attack's own area), not "most recent attacker == Linda" within Lucy's zone.
3. `GUnit` attacker memory: ordered structure with move-to-end and evict-oldest, or replace the line-79 guard with a direct "Lucy's last role target this action" check. (`GUnit` is a core system.)

Repro: B and C vertically adjacent in Lucy's zone, C earlier in the enemy `OwnedUnits` order; Linda's Explosive Crescendo on B (splash on C) → press Lucy's QTE → she hits C. Debug log of `e.name`, `GetMostRecentAttacker()` and the matching clause at `LucyFactionRoleHandler.cs:76` confirms it.

**Verified vs inferred:** code path, assets, memory size, list order and history verified; HashSet slot reuse in Unity's runtime, the exact playtest board, and `4f27914d0` as the trigger are inferred.
