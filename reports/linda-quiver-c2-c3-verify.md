# Report: Verify Linda's Quiver, C2 and C3 (compile and EditMode only)

Plan: plans/2026-10-26-linda-quiver-tech.md (C2, C3)    Agent: miso-verifier    Branch: thj/linda-quiver (uncommitted)
Outcome: done. **Result: PASS** (quiet checks; play criteria are in `playtests/2026-10-26-linda-quiver-play-check.md`)

## What changed

Nothing edited. Command line, Unity 6000.3.4f1, editor closed (`miso\Temp\` absent, no editor process). Results and log are `results.xml` and `test.log` in the scratchpad (`C:/Users/javid/AppData/Local/Temp/claude/E--Work-Projects-miso/038223eb-f0c2-4e68-9c09-24e1fd210f68/scratchpad/`).

## Checks

- **Compile:** clean. 0 `error CS`. 0 `warning CS` lines in the log, but this run's compile was incremental (`CompileScripts: 2119 ms`), so the log carries no warnings at all (C1's full compile showed 102 unrelated ones). Nothing in the Quiver, Recall, Lucy scatter or Mark catch files was reported.
- **Tests:** 849 run, 848 passed, 1 failed, 0 skipped. The failure is `AIRegressionTest.Baseline_MatchesCurrentAI` only.
- **Baseline message (D-255):** compared with the C1 baseline (`before.xml`, timing lines removed) the only differences are `CHECKS 709 to 710`, `FAILURES 38 to 39`, `abilities.count found 96 to 97`, and the one new `abilities.unexpected ...Linda_Ability_Recall.asset: new ability is not in today's baseline` line (shown in the failure list and again in the full FAIL list). Line-for-line equal to the implementer's final C3 run (`c3c.xml`). Matches D-255 exactly.
- **Quiver tests:** 106 ran, 106 passed (C1 had 55). By file: `ArrowLandingRulesTests` 15, `ArrowPickupRulesTests` 21, `GroundedArrowStacksTests` 9, `HandBackLinesTests` 11, `QuiverArrowStateTests` 13, `QuiverStateTests` 8, `QuiverWiringTests` 15, `RecallRulesTests` 14.
- **Re-serialization:** `git status --short -- miso` before and after the run is identical (20 lines, diff empty). Unity re-serialized nothing.

## Acceptance criteria

C2 and C3 criteria are code and EditMode level only; their play parts are steps 12 to 25 in the play-check file.

- [x] C2 pickup rules (extras stay, locked stack, enemies take nothing, dead Linda, G3, self pickup, lines): EditMode, `ArrowPickupRulesTests` and `HandBackLinesTests` pass.
- [ ] C2 John over a 2-stack with toss and two barks; pushed, Commanded, Fist Blitz and Dance pickups; enemy phase pickup; revive onto arrows; locked-look refresh; next level: Not run, needs a play session.
- [x] C3 Recall rules (arithmetic, locked stacks come back, extras stay, needs a grounded arrow and room, closed field reads 0): `RecallRulesTests` pass.
- [x] C3 wiring (1 AP, cooldown 2, `HasGroundedArrows`, `minimumDuration` at least the flight, 10th entry in `Unit_Linda`): `QuiverWiringTests` pass.
- [ ] C3 grey-out look, flight look, cooldown count, turn wait, 10th button with no key, [PLACEHOLDER] in tooltip, Self-cast click: Not run, needs a play session.

## Changed and new files under miso/, by commit unit (D-254)

Paths under `miso/Assets/_Project/` unless stated.

- **(a) Quiver scripts and tests** (all new): `Features/Player/Linda/Scripts/Quiver.meta`; in `Scripts/Quiver/`: `ArrowLandingRules`, `ArrowPickupRules`, `GroundedArrowField`, `GroundedArrowField.Pickup`, `GroundedArrowField.Recall`, `GroundedArrowStacks`, `HandBackLines`, `LindaQuiver`, `QuiverArrow`, `QuiverArrowState`, `QuiverState`, `RecallLines`, `RecallRules` (each `.cs` + `.meta`); `Editor.meta`; `Editor/`: `ArrowLandingRulesTests`, `ArrowPickupRulesTests`, `GroundedArrowStacksTests`, `HandBackLinesTests`, `QuiverArrowStateTests`, `QuiverStateTests`, `RecallRulesTests` (each + `.meta`). Leave `Editor/QuiverWiringTests.cs` + `.meta` for (d).
- **(b) Reset line:** `Core/Managers/PlayModeStaticReset.cs` (core, +1 line).
- **(c) Cloners:** `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`, `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`.
- **(d) Prefabs, data, wiring tests:** `Features/Player/Linda/Prefabs/` `LindaAttackArrow`, `LindaAttackFireArrow`, `LindaAttackHealArrow`, `LindaExplosiveArrow`, `Unit_Linda` (.prefab); the five spawn effects (`Resources/Abilities/Cooperation/Linda_Lucy/Linda/Linda_Lucy_LINDA_Duo_Ability_Effect_Spawn.asset`, `Linda_Toba/Linda/Linda_Toba_LINDA_Duo_Ability_Effect_Spawn.asset`, and under `Resources/UnitSpecific/Player/Linda/`: `Attack/Explosive Arrow/Linda_Ability_ExplosiveArrow_Effect_Spawn.asset`, `Attack/Primary Attack/Linda_Ability_PrimaryAttackM_Effect_Spawn.asset`, `Faction Role/Linda_Ability_FactionRole_Effect_Spawn.asset`); the new Recall data (`Resources/UnitSpecific/Player/Linda/Abilities/Recall.meta`, `Recall/Linda_Ability_Recall.asset`, `Recall/Linda_Ability_Recall_Effect_FunctionCaller.asset`, each asset + `.meta`); `Scripts/Quiver/Editor/QuiverWiringTests.cs` + `.meta`.
- **Fits no unit:** none.
- **Do not stage (Unity noise, pre-existing):** `miso/Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset`, `miso/ProjectSettings/EditorSettings.asset`, `miso/ProjectSettings/ProjectSettings.asset`.

## Bugs found

None.

## Save reset

No.

## Decisions I made

- Exit code 2 from Unity is the expected "a test failed" code; confirmed from the XML totals.
- The play-check list is one page of 25 steps; setup, action and expected result are folded into each step to keep it short.

## Needs THJ

The play check (`playtests/2026-10-26-linda-quiver-play-check.md`), per D-248.

## Docs to update

- `status.md`: C2 and C3 verified in EditMode, play check waiting on THJ.

## Risks and loose ends

- Editor checks corrections: none. (A short incremental compile writes no warning lines, so "no new warnings" can only be asserted from a full compile; C1's full compile was clean for these files.)
- Level picks in the checklist were read from the mission assets: M4 uses Level2-C1/C2/C3, M6 uses LevelE2-C1/C2/C3.

## Proposed commits

none (verifier does not commit); the four units above, in order (a), (b), (c), (d).

## Other branches

none

## How to see it

`playtests/2026-10-26-linda-quiver-play-check.md`.
