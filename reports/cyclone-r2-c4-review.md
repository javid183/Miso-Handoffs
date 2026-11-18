# Review: Cyclone round 2, C4 (branch `thj/cyclone`, uncommitted)

Reviewer: `miso-reviewer` (saved by the coordinator). Verdict: **FIX**. EditMode not run by the reviewer.

## Must fix
1. `CycloneCastPreview.cs` ~26-43: the component is never attached in the normal flow. It is added to `GlobalEventBus.Instance` at `AfterSceneLoad` / `sceneLoaded`, but the bus lives in `LevelBase.prefab` and `ProgramFlowHandler` instantiates the level after the scene loads (lines 92, 198, 264). Works only when Play starts in a scene that already holds a bus (TestLevel, SampleScene). Fix in Cyclone code, no core edit: e.g. a hidden `DontDestroyOnLoad` watcher created at `AfterSceneLoad` that adds the component whenever a live bus without it exists (no static field), or a lazy attach per level. If only a core/prefab hook is clean, stop and report. Verify in play through Preload, Home, level.

## Should fix
1. `CycloneSteerPreview.LateUpdate` (~176-198): the cross can stay dimmed if the aim ends without cancel/abilityStarted/levelEnded (e.g. End Turn mid-aim). Before the `_path.Count` early return: if `_aim.Aiming` and the player is no longer selecting a target, call `Stop()`.
2. `CyclonePreviewTests.cs` 144-148 `TheCrossBurstRing_LastsAsLongAsTheBurst` asserts a constant equals itself: remove.
3. `CyclonePreviewTests.cs` ~388 `Assume.That` should be `Assert`.
4. No test for moving the health panel to the ghost and back (`CycloneOutcomeView.MovePanel/Apply/Clear`). Add one (offset on Show, `localPosition` restored on Clear; `GetComponentInChildren<EntityInfoPanelUI>(true)` is the same panel as `GUnit.entityInfoPanelUI`).

## Notes
- No core file has C4 edits; no new statics; board override identical when null (`ForCast` passes `cell => cell.OccupantEntity`, passing null would match execution exactly: cosmetic).
- Cleanup paths, subscriptions, wobble stop/restore, LF/no BOM, no private IDs all fine. Wobble has no test for stop/restore (play check).
- `Cyclone.prefab` keeps an orphan `whirlHitTimes` key: harmless.
- Commit split: four shared files need hunk-level staging (pre-C4 copies and `c4-shared-hunks.diff` in the scratchpad).

## Re-review (fix round): APPROVE

Saved by the coordinator. All five findings resolved. Watcher `CycloneCastPreviewAttach`: one per Play session, no statics, attaches to each new bus, trivial cost, no leak. Open: live Preload > Home > level check (play-check item 0). Optional nit: `CycloneCastPreview.OnEnable/OnDisable` could subscribe via `GetComponent<GlobalEventBus>()` instead of `Instance`.
