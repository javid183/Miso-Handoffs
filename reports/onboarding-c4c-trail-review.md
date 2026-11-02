# Review: onboarding C4c The Trail

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-02. Plan: `plans/onboarding/2026-11-01-onboarding-c4-search-levels.md` § C4c. Report: `reports/onboarding-c4c-trail.md`.

**Verdict: APPROVE** (4 should-fix, sent as a fix round)

## Should fix
1. `SearchWiring.Trail.cs:375`: pile stage 1 objective `visible: false`, so turn 1 HUD shows only the defeat condition (`LevelObjectives.cs:129-132`). Give stage 1 a visible text objective; extend the rear-wave test.
2. `SearchWiring.Trail.cs:213`: blood panel says "The pool is empty", but FTP carries over (`FactionTracker.cs:195-213`: load gain with `Stat_FPG`; route restart keeps leftover FTP). Coordinator choice: −99 drain filler on both route levels too; assert in tests.
3. `SearchTrailTests.cs:144` drain check covers Blood only (loop Blood/Tracks/Pile, updated for fix 2); `:165` asserts a constant against itself (read Claw `Stat_HP` + Early row, as the Ridge HP test, or drop).
4. `GridBlockParser.cs:394-406` / `GridToLevelBuilder.Hidden.cs:27-29`: `level hidden` + `level deploy` on one tile silently drops the hidden unit or misreports. `ReadDeploy` errors when the tile is in a hidden group; one parser test.

## Notes
- Deploy slots match hand-made levels (`LevelE2-C3.prefab:1984-2040`); `FillRosterSlots` (`CombatLevelRunHandler.cs:264-313`) fills them with the free pick.
- AI regression 39 → 41: `AIRegressionTest.CheckUnits` (`:546-566`) catalogs every unit prefab outside `/Content/Levels/`; the variant adds `units.count` + `units.unexpected`. Catalog only, golden master unchanged. Acceptable; the AI fix session adds the variant to the catalog. Variant is a true variant, `Unit_DarkClaw` untouched.
- `Produce(-99)` clamps (`FamilyTimePoints.cs:51,71`). Turn-2 spawn fires once; spawned Claws count for defeat-all; an occupied spawn cell (0,6 / 0,5) is skipped silently (play-check item).
- Pick line on `GenericCharacter_1` filled by `MissionTracker.AssignGenericDialogueCharacters`.
- Graph 5 nodes / 5 edges, OR InterNode, only trailhead initial; items resolve (Trinket +5 FTP); roster Lucy + Linda fixed, 1 free slot, Toba excluded. John/Mark availability: play check.
- Deviations reported: no "stays home" line; tally at end; one merged pick line; Encore opens with Lucy before Linda. XP/Gold left 40/5 (THJ).
- LF, no BOM, no private IDs, no mutable statics, no core runtime code. Three-commit split builds in order.
