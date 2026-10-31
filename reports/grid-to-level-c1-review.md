# Review: grid-to-level C1

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. **Verdict: APPROVE.** Committed `81897bb7c`.

## Should fix (folded into C2)

1. `GridToLevelBuilder.cs:123-134`: the outside-cell entity strip destroys `GetNearestPrefabInstanceRoot(entity)`; a plain entity inside a nested prefab (e.g. the environment) would delete the whole environment. Destroy the target only when it is the entity's own instance root (or carries the `GridPluggableEntity`); otherwise destroy only the entity and warn. No template is affected today.
2. `GridToLevelBuilder.cs:89`: `EnsureFolder` runs before strip/build; a failure leaves an empty `Greybox/`. Create the folder just before saving.

## Notes

- Parser matches `grid_render.py` (fence, `id`/`title`, `--` split, bottom row y 0, 4-way groups, char sets); stricter on doubled terrain, units on `#`/`_`, ragged rows. Two touching Mashers form one invalid group (renderer has the same limit).
- Both deviations correct: load + `SaveAsPrefabAsset` (template never written, GUID kept on rebuild); cells under the Tilemap (`GridManager.GatherCells`, `GridManager.cs:60`).
- Strip list complete for C1. Level ID = `missionName|levelName`, so `levelName` covers it. Template `specTags`/`musicID` carry over (generic).
- C2: decide the tier of a block with no `level tier` line; add the `Assets/_Project/` prefix to `level template` values.
- `LevelStartFPFiller` rebind (D-342) is sound: pick units by player faction (not palette char; `units[0]` decides the controller); rebind after `BuildGrid`, before `FixMissingReferences`; list the template filler's values (`fpAmountToFill`, `atbGaugeAmountToFill`, `heal`) as a build warning. Only the three onboarding templates have it.
- Tests are meaningful and clean up. Doc-parse tests `Assert.Ignore` without `claude-handoff/`.
- `GridPalette.cs:7` cites a `claude-handoff/` path: reword. Test namespace differs from siblings (harmless).
