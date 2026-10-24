# Enemy alert C1: review

Reviewer: `miso-reviewer`, 2026-10-23. Saved by the coordinator (the reviewer has no write tool).

**Verdict: FIX**

## Must fix

1. Summons and Worm split children wake the moment they appear (breaks rule 3). `EnemyAlertTracker.Events.cs:115-171` (`OnAbilityEffectPerformedOn` → `CollectAffected`, GridCell branch l.157). `GUnit.SpawnAt` raises `unitBorn` (tagged Unaware correctly), then the spawning ability's completion (`RuntimeAbility.cs:316-318`, `actualTargets`; `AEffectCompound.cs:165-167`) raises `onAbilityEffectPerformedOn(ability, targetCell)`; the cell now holds the newborn, so it wakes and spreads. Confirmed on `DarkShaman_Summon_Ability.asset` (`actualTargets: 1`); Mountain Deev summon likely; Worm split depends on its reporting; corruption pool probably not. Fix: a report from the ability that created a unit doesn't wake that unit (e.g. record newborns against `SessionLogs.ActionsInProgress`, or skip units registered this frame); decision as a pure function in `EnemyAlertRules` with a test.

## Should fix

1. Enemy area attacks wake Unaware allies standing in the area (`Events.cs:155-163`): a targeted cell counts as "affected" even when the relation filter applied nothing. Count only real effects on the unit.
2. Status ticks (Burn) wake the unit they damage (`EnemyAlertTracker.cs:207-211`): implementer's choice; confirm.
3. Weak tests: `Timing_*` (`EnemyAlertRulesTests.cs:245-255`) and `Noise_*` check trivial booleans; tracker-side choices (which report wakes whom, spawn handling, AP close) are untested. Move "which units does this report wake" into pure code with tests.

## Notes

- No core code changed. Skip query All→Any: with only Stunned, identical (`GTagRegistry.Match` checked); no other overrides. `core-systems.md` needs a note: skip query is Stunned OR Unaware.
- AP close for a unit woken in its own faction's turn is safe (same public `APConsumer.Consume(Closure)` as `FactionPhaseData.Reinitialize`; shared AP is player-only; Masher counter doesn't check AP). Turn-start sweep wakes act one enemy turn late (accepted safety net).
- Tag removal swaps the list (worker-safe); tag add at spawn edits in place (same exposure as Stunned/Taunted).
- `IsFlowSettled` uses `SessionLogs.ActionInProgress`, which counts AI planning; a small window remains in the mover path. Watch in play.
- YAML minimal, ids intact; `Status.Unaware` appended in both tag assets with a placeholder icon and `[PLACEHOLDER]` description; LevelBase component GUID matches the script meta.
- LF, no BOM, no statics, balanced subscriptions, no private IDs; file list matches; commit split right.
- Visible side effects: "Unaware" gain pop over every enemy at level start; Masher counter preview hidden while Unaware (`MasherGoblinFactionRoleHandler.Preview.cs:69`) yet it counters.
- Other branches: `thj/home-test` needs this when it takes `main`.

## Re-review after fix round 1 (2026-10-24): APPROVE

- Must fix 1 resolved: a unit wakes only when a report names it (`EnemyAlertTracker.Events.cs:159-180`; `AEffectCompound` names units only after `PassesFactionFilter`); Shaman and Deev summon reports name only the tile, and an enemy caster makes no area noise. Second guard: `_bornDuring` + `EnemyAlertRules.WokenByReport` (report fires before `log.Complete()`; `ForgetFinishedBirths` on `abilityPerformed`; instance field, cleared at level end).
- Should fix resolved: enemy area attack over an Unaware ally wakes nobody; Burn ticks wake (D-161); tests now cover `WokenByReport` (9 cases), start-alert spread (3), timing (3).
- `UnitAlerted` third value (`Action<GUnit,int,bool>`): safe, no subscriber yet; false for start-alert spread wakes.
- `CloseActionPointsOnWake(ownTurn, Points)`: safe; closes only with points left; enemies never use the Shared pool; same public `Consume(Closure)`.
- Note: the newborn guard covers any ability running at the birth, not only the spawner (e.g. a family hit in progress when Worm children appear makes no area noise on them; damage still wakes via the HP watch). Acceptable.
- Play check still needed: summons stay Unaware, level-start spread, Masher counter, area noise from projectiles.
