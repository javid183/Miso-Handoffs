# Cyclone C2 review

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. Branch `thj/cyclone`, uncommitted tree.

**Verdict: FIX.** Root: `PlantedLetsPass` ignores the mover's `ignoreRelation`, and older code treats "path-walkable" as "can land".

## Must fix
1. Blink/teleports (`Lucy_Ability_Teleport`, `John_Ability_Teleport`) and Mark's Vault/Primary and Mark–Lucy Duo can target and land on the Cyclone cell: `GridCell.cs:873-892` ranged-reach block of `GetRangeCells` (line 885) re-adds any cell passing `CheckIfUnitWalkable` for non-Unconstrained modes; `AEffectTransporter`/`TeleportEntity`/`JumpEntity` don't re-check. Allied AI too (`AIUnitBrain.GetAbilityRangeCells:278-302`). Fix: skip cells whose planted `OnGridEntity` has `DisallowWalk` when mode ≠ Unconstrained (restores old behaviour). Test: SelfWalkable + ranged reach, family source, excludes the Cyclone cell.
2. Mark's dash approach cell `path[^2]` can be the Cyclone cell (`AEffectDashAttack.cs:69-77`); the walk can't end there, attack fires from where Mark stands. Also Command Shield Dash preview (`JohnPassiveAbility_CommandShieldDash.cs:210-217`) and `TryResolveGhostCell`. Fix: use the nearest standable cell next to the target when `path[^2]` isn't `IsFootprintEmpty`. **Core file outside D-533 → THJ.**

## Should fix
1. `UnitsCooperationHandler.cs:1292-1296, :1361`: Mark–Linda Duo `LoserStop` uses `path[^2]` (same issue; core, outside D-533).
2. `CycloneAIDangerTests` rebuild the keep/drop rule in the test; deleting `AIUnitBrain.cs:345` keeps them green. Move the decision into a pure helper the brain calls and tests drive, or label them as rule-shape tests. "Decoys pass" duplicates "family passes".
3. `AIUnitBrain.EndOfTurnDanger.cs:57`: add `a.Active` on the live turn (`sim == null`).
4. `AIUnitBrain.EndOfTurnDanger.cs:72`: area-attack range measured from the destination cell, not the whole footprint (large units).

## Answers
1. Neutral is an ally of the family in all 68 levels (`LevelBase.prefab` entries, not overridden); if not, neutrals would be blocked like enemies, no crash. Strangers allied in 201/204 entries. Enemies blocked; pushes/pulls stop before. Ending on the cell: walk end no, deploy no, swap no, Blink/Vault **yes** (MF1), dash breaks (MF2), movement block/death mid-pass leaves the unit there (reported).
2. AI filter: detour / walk in to attack / wait outside hold in logic; melee and ranged attack checks right (no line of fire until C4); all filtered → unit stays put. Snapshot per job on main thread; no statics; unused `AIFactionBrain.PredictNextTargets(GUnit)` (:266) would read the last job's danger. Only "not on the arms" is guaranteed, not "3+ cells away" (holds along arm lines; diagonal-adjacent waiting possible in open ground). An enemy already on an arm with nothing to attack isn't made to leave.
3. AI regression 41→42: C2 can't move it; C1 most likely not; likeliest main drift since early Nov.
4. Commit order (whole files): A core walk (`OnGridEntity.cs`, `GridCell.cs` incl. MF1, `GridCell.PlantedPass.cs`); A2 core dash (if MF2 lands); B core AI (`AIEndOfTurnDanger.cs`, `AIBlackboard.cs`, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIUnitBrain.EndOfTurnDanger.cs`); then C1 commits 1, 2, 3–8 (commit 3 takes the whole `Cyclone/` folder except `CycloneEntity.AIDanger.cs`, and the whole prefab); C Lucy C2 (`CycloneEntity.AIDanger.cs`, `CycloneTestFactions.cs`, `CyclonePassTests.cs`, `CycloneAIDangerTests.cs`).
5. LF everywhere; BOMs match; no private IDs. Play-check list: enemies end off the cross with a way round; step on an arm only to attack; corridor wait distance; intent preview matches; AI log "Skipped: ends on dangerous ground…"; Archer on an arm; large enemy; after fixes: Blink/Vault never offer the cell; Mark's dash beside the Cyclone; John/Linda walk through; Command Shield Dash crossing the cell.

## Re-review of the fix round (2026-11-12): APPROVE
Both must-fixes and all four should-fixes done. "Planted walk blocker" test = exact pre-C2 result; used in all four stop pickers (`GridCell.cs:887-888`, `AEffectDashAttack.cs:79-80`, `UnitsCooperationHandler.cs:1291-1317, :1381-1386`). `FootprintHasWalkBlocker` worker-safe (add to the Grid row in `core-systems.md`). `PredictNextTargets(GUnit)` snapshots only off the worker; no callers. Reflection tests acceptable. Step-back loop terminates. Commit order A, A2, B, C1 1–8, C builds at every step. AI regression still 42, same list.
Notes: dash detour around the Cyclone can exceed dash range at max reach (transporter refuses, attack from where Mark stands; pre-existing with any blocker; play check, fix for all blockers if it shows). Fallback approach uses the large target's anchor cell only (pre-existing limit).
