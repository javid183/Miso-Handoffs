# Mark memory rework: tech check (Explore, 2026-11-05)

Read-only. Paths under `miso/Assets/_Project/`. Summary of the Explore report for `m4-mark-rework`.

- **Forced unit + ability + cell:** nothing exists; gate needs hooks in `PlayerController`, `FactionControllerBase`, `CombatLevelUIManager` (core, M). Pinning control to one unit works by tagging others `Status.Inactive` (not selectable, no AP on start/Reset, `PlayerController.prefab:203-209`, `FactionPhaseState.cs:17-18, 61-66`); no sequence/LSB action to add/remove tags yet (S, not core).
- **Auto-select:** private `AutoSelectUnit` picks at random among units that can act (`PlayerController.cs:473-481`), also after a Reset. Deterministic only by leaving one unit able to act.
- **AP for one turn:** `TurnStartActionPointLimit` runs once on `turnStarted`; a Reset refills AP and raises no `turnStarted` (`CombatLevelRunHandler.cs:543-555`). Needs a sequence that sets AP after a Reset (S) or a "phase restarted" event (core, S).
- **Reset side effect:** ticks the player faction again (`CombatLevelRunHandler.cs:553`): cooldowns, statuses, Cyclone life lose one extra turn.
- **Cast in a sequence:** none; `AbilityOrchestrator.ActivateAbility` supports it (template: Mark's passive `MarkPassiveAbility_ContinuousAttack.cs:354-368`). `CastAbilitySequence` S, not core. Cyclone behaves normally after; no AP spent.
- **Moves:** `MoveUnitSequence` walks by nickname to a fixed cell along a real path; silent no-op if blocked; several units = chained, one after another. Ryker (`Cub (placeholder)`) is a sprite, not a unit. "Next to", lists, parallel: S–M, not core.
- **Pools (`CP_Spawner` = `HazardEntity`):** spawn `Unit_DarkClaw` on own cell if empty, `spawnLimit 1`; level has interval 1 → Enemy turns 1, 3, 5. **Core bug:** `interval = 0` never refires (`HazardEntity.cs:146-150`); workaround `intervalMode = SpecificTurns` listing every turn (data). **Spawned Claws give XP 3** → `NothingInTheHearthGivesExperience` fails now; fix: 0-XP Hearth Claw variant + spawner/compound/pool variants (data, S). Spawned Claws count for `LivingUnitsLOCondition`; a live pool keeps the Enemy faction in turn order. Cleanse removes pools.
- **Mother:** a sprite (`Wolf.prefab`), not a unit; current memory swaps to `Mother (fallen)` via LSB "motherFalls" (still in the prefab; works).
- **Subset objective:** `EntitiesDestroyedLOCondition` (explicit list) works, no "{n} left" counter (new condition class S for one); hidden units likely count as dead before reveal: start that stage after the reveal.
- **Locks:** `LevelAbilityLock` can lock every Duo trigger and `CleanseAbility` (list per hero; shared triggers under both). Unlock applies to all units at once; no re-lock. Duos only cast from the bar/number keys, so the lock covers them. Mark oddly carries `Linda_Lucy_Duo_Ability` (slot 8); John and Lucy carry one Duo twice.

| # | New code | Size | Core |
|---|---|---|---|
| 1 | Forced-action gate | M | yes |
| 2 | Tag add/remove sequence (pin control) | S | no |
| 3 | Set unit AP from a sequence after Reset | S | no |
| 4 | `CastAbilitySequence` | S | no |
| 5 | Move extensions (next-to, many, parallel) | S–M | no |
| 6 | 0-XP Hearth Claw + pool variants (data) | S | no |
| 7 | Pools every turn: SpecificTurns (data) or fix `interval 0` (core, Tier 2) | S | data / yes |
| 8 | Subset objective with counter | S | no |
| 9 | `KillUnitSequence` (optional) | S | no |
| 10 | Unlock per unit / re-lock (optional) | S | no |
