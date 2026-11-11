# Report: M2 Trail C4 (balance values)

Plan: plans/onboarding/2026-11-11-m2-trail-levels-tech.md (C4)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check pending)

## What changed

- Four `GB_m2-*` prefabs rebuilt from the four blocks (`level tier standard`) with `GridToLevelBuilder.Build` (same call the window makes, overwrite on, existing paths, GUIDs unchanged), then `Tools/Onboarding/Wire Search: Trail`.
- `SearchWiring.Trail.cs` (LF, no BOM): removed `TracksClawHealthFactor`; `BlackClawHealthFactor` 0.5 -> 0.75; `SetHealth` now only sets the Black Claw on the tracks (Dark Claws, the hidden pair included, have no override). Comments updated.
- `SearchTrailTests.cs` (LF, no BOM): level tier literal "Standard" on all four (test renamed `EveryLevelIsStandardPlaces...`); Tracks override test: Black Claw literal 0.75, everything else 1 and not overridden; health arithmetic now uses the Standard row (Claw 16 HP, no override); new `LucysCycloneDealsThreeDamagePerHit` asserts the live Cyclone asset's Specs_Health factor `baseFactor` is 3.
- `Lucy_Cyclone_Effect_AttrMod.asset` (Lucy folder): field `attributeModifiers[0].factor.baseFactor` (Specs_Health, policy 4, reading Stat_DMG, bounded) 7 -> 3. Cooldown untouched. Linda-folder copy, `PassByEffect_AttrMod` (also 7) untouched.
- No other test asserted 7 for the Cyclone or Hearth; none updated.

## Acceptance criteria

- [x] Blocks read standard; prefabs rebuilt and rewired. Idempotent: md5 of all 94 files (four prefabs and every Trail sequence asset) identical before and after the second wiring run. Tier asserted by test (EditMode).
- [x] Tracks: no Claw override, Black Claw 0.75 (30 HP at Standard, if base 40: only the factor is asserted; Claw 16 HP asserted). Test-covered. No other level has an override (test).
- [x] Cyclone 3, cooldown unchanged; test-covered.
- [x] Literal asserts in place.
- [x] EditMode: 1877 total, 1876 passed, 1 failed = known red `AIRegressionTest.Baseline_MatchesCurrentAI` (42 failures, all graph-count/fingerprint items, not touched). Console after compile: no compile errors; wiring ran without exception.
- [ ] THJ plays the Trail both picks: needs the play check.

## Save reset

no

## Decisions I made

- Drove the grid builder from the code-execution tool (identical call to the window's Build button) because menu windows can't be clicked from here.
- The prefabs show no `enemyTier` text diff line of their own in grep (Standard = 0, the default); the test reads the serialized value and passes.

## Needs THJ

Play both Trail picks (Standard tier is tougher than Early; Black Claw 30 HP, Cyclone hits for 3).

## Docs to update

Balance design / build log: C4 done pending play.

## Risks and loose ends

- `PassByEffect_AttrMod` still 7 (out of scope, flagged in the plan as orphaned).
- Cyclone 3 is global: Hearth and River content using Lucy's Cyclone get weaker; no test asserted otherwise.
- Prefab diffs are large (rebuilt), as in C3.

## Proposed commits

1. Trail data: `feat(onboarding): the Trail plays at Standard tier, the Tracks' Dark Claws lose their health override and the Black Claw keeps three quarters of its health`
```
 M miso/Assets/_Project/Content/Levels/Greybox/GB_m2-blood.prefab
 M miso/Assets/_Project/Content/Levels/Greybox/GB_m2-pile.prefab
 M miso/Assets/_Project/Content/Levels/Greybox/GB_m2-tracks.prefab
 M miso/Assets/_Project/Content/Levels/Greybox/GB_m2-trailhead.prefab
 M miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Trail.cs
 M miso/Assets/_Project/Features/Onboarding/Editor/SearchTrailTests.cs   (see note)
```
2. Cyclone alone: `balance(combat): Lucy's Cyclone deals 3 damage per hit instead of 7`
```
 M miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Effect_AttrMod.asset
```
Note: `SearchTrailTests.cs` holds both the Trail asserts and the new Cyclone test in one file; to split cleanly, stage it in commit 1 with `git add -p`, or simply put the whole file in commit 1 and accept that commit 1's tests pass only after commit 2 (the Cyclone test would fail between them). Simplest: put the file in commit 2 only if commit order is 1 then 2 and you accept a red middle; otherwise use `git add -p` to put the `LucysCycloneDealsThreeDamagePerHit` hunk in commit 2.
