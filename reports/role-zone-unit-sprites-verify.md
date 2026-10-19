# Verify: Role zone unit sprites, C1 + C2 (D-075)

Plan: plans/2026-10-19-role-zone-unit-sprites.md    Agent: miso-verifier    Branch: thj/fr-readability (uncommitted working tree)
Outcome: partial (quiet checks pass; play checks not run)

**Result: PARTIAL.** Every quiet check passes. The play-only criteria were not run (no play session agreed).

## Compile

Clean. `refresh_unity` with a forced compile ran and finished, the editor went idle, and the console has no `error CS` and no compile warnings.

Console (errors/warnings) after the refresh, 14 entries:
- 13 x "Serialization depth limit 10 exceeded at ... StatBackedValueBase.factorReadMode". They come from the existing AbilityOrchestrator / RuntimeAbility._owner cycle (GUnit, JohnPassiveAbility_CommandShieldDash, MarkPassiveAbility_ContinuousAttack, LucyPassiveAbility_PapasShelter, PlayerController, DivineRelicPickUp, UnitsPassByHandler, UnitsCooperationHandler). Five of them start at `FactionRoleHandlerBase.ability`, which is the existing `ability` field and not one of the new fields. The change adds no new serialized class, so these look pre-existing. I did not compare against a build without the change.
- 1 x "Internal error - unexpected guid mismatch" (known).
- Nothing mentions RoleZone, GridCell, or the four Unit prefabs.

## Tests

Full EditMode suite via the Unity MCP: 191 run, 190 passed, 1 failed, 0 skipped (41 s).
The one failure is the known `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (checks 704, failures 35; not touched). No other failure.

## Acceptance criteria

- **Gate 1, compile clean:** Pass (see above).
- **Gate 2, suite green except the known red:** Pass (190/191).
- **Gate 3, prefab data:** Pass. Read through `execute_code` from the saved prefabs (AssetDatabase), role handler `RoleZoneSprite` / `RoleZoneSlot`:
  - Unit_John (JohnFactionRoleHandler): ShieldOutline, TopLeft
  - Unit_Mark (MarkFactionRoleHandler): PunchOutline, TopRight
  - Unit_Linda (LindaFactionRoleHandler): Arrow, BottomLeft
  - Unit_Lucy (LucyFactionRoleHandler): Fireball, BottomRight
- **Gate 3 optional, `RoleZoneSlotLayout.Fit`** on a unit box with padding 0.03, using each sprite's `bounds.size` (all have a bounds centre of 0, so the pivot is centred):
  - ShieldOutline: centre (-0.25, 0.25), size 0.39 x 0.44
  - PunchOutline: centre (0.25, 0.25), size 0.33 x 0.44
  - Arrow: centre (-0.25, -0.25), size 0.44 x 0.24
  - Fireball: centre (0.25, -0.25), size 0.37 x 0.44

  The four rects do not overlap (0 overlapping pairs). Each stays in its quadrant, and the aspect is kept.
- **Gate 4, not run (needs THJ in Play):**
  - Shift view with all four Bergsons.
  - Overlapping zones on one cell.
  - Mark's footprint and a big enemy's footprint.
  - Selected-unit zone.
  - Move-preview follow zone.
  - Jaggedness or shimmer of the downscaled icons.
  - Whether a lone corner icon reads well.
  - The once-per-handler "no roleZoneSprite" warning should now not appear, since all four are set. This is also a play check.

## Bugs found

None.

## Branch

thj/fr-readability. The editor stayed in Edit mode on `PreloadScreen.unity` (the scene it was already on). Nothing was changed or saved.

## Save reset

No.

## Editor checks corrections

- `refresh_unity` with `compile: request` returned "compiling"; the first state poll already showed the compile and reload done, with `ready_for_tools:false` and "stale_status" for a few seconds. The console could be read anyway. `get_test_job` disconnected once ("session disconnected while awaiting command_result"), and the second call returned the result.
- The `get_test_job` payload has `result.results = null`. The failures are in `progress.failures_so_far[].full_name`, and `result.summary` holds the counts. The file is one huge line, and `jq` is not installed here (use `python -I`).
- `execute_code` needs `action: "execute"`. The code is a method body, so `using` lines fail and types must be fully qualified.
- On this branch the suite is 191 tests (it was 175 on 2026-10-19 before C1's tests).
