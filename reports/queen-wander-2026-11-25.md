# Goblin Queen wanders without attacking + info-panel console error (2026-11-25)

Read-only Explore trace after THJ's M4 play (thj/onboarding-demo @ `4ed943758`). Cause of the wandering **unknown**; nothing ties it to the M4 commits.

## Ruled out (with evidence)
- **Planner skip (D-686):** Level3-C1's objectives are LevelBase's two `LivingUnitsLOCondition` (LevelBase.prefab:771, 780), which have a handler (AIStrategyPlanner.cs:115). No AI worker exception in Editor.log. The override at Level3-C1.prefab:3319 targets a stale field (no effect).
- **Targets / factions:** Queen attack/charge target relation Enemy (GoblinQueen_Ability_Attack.asset:653); Bergsons–Enemy hostile (LevelBase.prefab:802); Toba is Bergsons (Unit_Toba.prefab:196); no unit-specific targeting; `alwaysAlert`, level starts all alert.
- **Queen files:** `Features/Enemy/Goblin Queen`, `BossGoblinQueen.cs`, `Resources/UnitSpecific/Enemy/GoblinQueen` unchanged since October; the origin/main merges touched the awareness display (`14242a127`) and the Archer Goblin (`f04e9b0ae`) only.
- **`LevelAbilityLock`:** action bar only (AbilitiesBarHUDUI.AbilityLock.cs, GuidedAbilityHint), not AI.
- M4's Level3-C1 delta: the title `(5/5)` → `(3/3)` and the Cleanse lock. Toba has been placed there since May.

## Candidates (unverified)
1. **End-of-turn danger filter** (`1b22ca01c`, AIUnitBrain.EndOfTurnDanger.cs:20-36; AIEndOfTurnDanger.cs:11-60): a plain move ending on a dangerous cell (e.g. next to Lucy's Cyclone) is dropped unless the unit can attack from there. Lucy is fixed in M4 now. A Queen with no reachable attack from allowed cells looks like wandering.
2. **Charge cycle stall:** Jump to a pre-charge zone, then Charge; `PreChargeEvaluateDestinationScore` returns 0 for occupied zone cells (BossGoblinQueen.cs:~139-146). Heroes standing in `preChargeZones` could stall it.
3. Other Nov AI filters (`c9ad26e7e` Cyclone burst, `f04e9b0ae` AIUnitBrain.cs:~343-350): probably not hit by the Queen's abilities.

## Confirmation steps
- Play Level3-C1 with the AI log (AILogService) and look for "Skipped: ends on dangerous ground…" / "Skipped: the line of fire is blocked" for the Queen.
- Replay without casting the Cyclone.
- Check whether a hero starts on a `preChargeZones` cell.
- Replay with Toba not deployed.

## Console error
Same as known error 2 (`reports/console-errors-2026-11-24.md`, D-658): Shift `performed` (PlayerInputController.cs:82) → `GUnit.ShowInfoPanelGlobal` (437) → `ShowInfoPanel` (488) → `EntityInfoPanelUI.Show:176`; a Global request while the single queue slot is full. Seen right after `@Level3C1_StartSequence`. Khash's code (`ef3c7a9066`); log noise; not ours.

## Second trace, from THJ's combat log (20261125-154053_Into_the_Rootwell)

THJ clarified: only the first Queen fight; he stopped her charge with Toba's Wall; the console error happened in that run. The log shows one idle turn: R2 the charge stops at 10,-2 (wall), Mark's Command moves her to 10,-3; **R3 she Walks to 11,-3 and doesn't attack** though Lucy (9,-3) and Mark (10,-4) are orthogonally adjacent; R4 normal (walk + attack Mark). Later runs: normal (in 162906 the charge was also wall-blocked and Command moved her, and she attacked).

- **Not the Queen script:** `BossGoblinQueen.cs:19-25` state enum commented out, `Charge()` (:124-130) resets `_preChargeDone`; charge data only read by PreCharge/Charge evaluators.
- **Not Command:** `Mark_Ability_Attack_Command.asset:146` any faction; only `EntityState.Unmovable` blocks it (set by PreCharge, cleared by Charge). Intended (D-213).
- **Not the wall, danger filter (no Cyclone until R4), line of fire, AP/escalation (player only), cooldowns.**
- **Mechanism (~80%):** the AI chose Walk over Attack (Walk evaluator `Generic_P_Walk_Melee_UtilityScoreEvaluator.asset` can outscore the Attack's `Generic_RangedSurroundingAttack_UtilityScoreEvaluator.asset` with a target adjacent); the walk ended out of reach (footprint 1x2, attack orthogonal radius 1), Walk has cooldown 1, so the turn ended. Why Walk won is unrecorded (`AILogService` in-memory, `MAX_LOGS=10`).
- **Repro:** the bad run's positions to R3 with the AI Log window open; compare Walk and Attack scores; again with the Queen placed on 10,-3 without Command.
- Console error: unrelated (13x in all four Level3-C1 runs).
