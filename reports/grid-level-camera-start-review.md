# Review: grid-to-level camera start

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. Plan `plans/2026-10-31-grid-level-camera-start.md`, report `reports/grid-level-camera-start.md`.

**Verdict: FIX** (one small must-fix)

## Must fix
1. `CameraStartTool.cs:191`: `AssetDatabase.SaveAssets()` saves every dirty asset (e.g. the TMP fallback font). `SaveAsPrefabAsset` already saves the prefab. Delete it.

## Should fix
1. `CameraStartTool.cs:123-136` (Prefab Mode path): add `Undo.RecordObject` before the move, `PrefabUtility.RecordPrefabInstancePropertyModifications` after, `Undo.RegisterCreatedObjectUndo` for a created locator (the locator sits inside a nested prefab instance; `SetDirty` alone can lose the override).
2. `CameraStartTool.cs:125-126`: a created locator is parented to the `CameraHandler`, which moves onto it (drifts on a second `Initialize`). Parent it to `handler.transform.parent` (fallback: handler), as `LevelBase` templates have it; update the test assert.
3. `CameraStartTool.cs:69`: use `GridManager`'s serialized `grid`, as the builder does, not the first `Grid`.
4. `GridToLevelCameraStartTests.cs:205-214`: assert the exact position for the `level camera` test.
5. `GridBlockParser.cs` `camera`: warn when the tile isn't one of the block's tiles.

## Notes
- GB prefab values check out (parents at 0,0,0, z kept, values match the report; m1-linda recomputed by hand).
- Stale boundary overrides on a removed component come from the template; harmless, pre-existing.
- No core file, no statics, LF/no BOM, no private IDs; both commits stand alone. 16:9 aspect and the preview limit accepted.

## Fix round check (coordinator, 2026-10-31): done

Must-fix and five should-fixes in (spot-checked: no `SaveAssets`, Undo + `RecordPrefabInstancePropertyModifications`, created locator beside the handler). EditMode 1126/1127 known red only; camera-start tests 17/17. Prefab Mode run on `GB_24-nook` saved the same values; close-and-reopen not checked separately.
