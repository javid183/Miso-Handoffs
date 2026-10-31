# Review: grid-to-level C2

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. **Verdict: APPROVE.** Committed `eb40ebcd5` (camera refactor), `459f41428` (the rest).

## Should fix (folded into C3)

1. `GridToLevelBuilder.cs` ~128: the camera fallback warning names `Tools > Levels > Assign Camera Boundary`; the real items are `Assign Camera Boundary (Selected Level)` and `Assign Camera Boundaries (All Levels)`.
2. The C1 folder fix has no real test: `Settings_MissingTemplateIsAnErrorAndWritesNothing` fails in `Validate`, before the old `EnsureFolder` too. Add a case that passes validation and fails in `Strip`/`BuildGrid` (e.g. a template whose GridManager has no tilemap, or a footprint over a missing tile) and assert no folder.
3. `RemoveStrayEntity` component-only branch: `DestroyImmediate(entity)` fails when another component requires it (`MemorableAttackMemoryShare` has `[RequireComponent(typeof(GUnit))]`); check `if (entity)` after and report an Error. No template reaches it today.

## Notes

- Camera refactor behaviour-identical; commit 1 stands alone.
- `level` lines: tier set every build (`?? Standard`), alert adds or reuses `LevelAlertSettings`, origin shifts names and positions (dictionary keyed by block coords), template prefix via `TemplatePathFor`.
- Filler rebind meets every condition (player faction from `LevelFactionRelations`, block order, no nulls, before the missing-reference check, warning lists the values).
- C1 should-fixes all done. Palette fallback sound; asset holds 12 units, 6 hazards.
- Line endings: HEAD/index LF (`.gitattributes` `*.cs text eol=lf`, `core.autocrlf=true`); the working copy CRLF came from the checkout, not the implementer; no churn. The report's "keeps its BOM" is wrong (no BOM), harmless.
- C3 loose end: `Strip_*` tests create GameObjects in the open scene (destroyed in `finally`), which may mark THJ's open scene dirty.
