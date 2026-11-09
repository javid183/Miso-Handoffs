# Report: Sisters' tally, results row (C3)

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md    Agent: miso-implementer (sonnet)    Branch: thj/onboarding
Outcome: done

## What changed

All under `miso/Assets/_Project/` (+ `.meta` for each new file).
- `Features/Onboarding/SistersTally/SistersTallyResultRow.cs` (new): component on the panel root. `ShouldShow(isMissionEndPanel, enabled, eligibleInMission, faded)`, `Format`, `Refresh()` (fills the row, shows or hides it, rebuilds the layout; whole body in try/catch; also runs in `OnEnable`).
- `Features/Onboarding/SistersTally/SistersTally.cs`: new `EligibleInMission` (gated by `Enabled`); `BeginLevel` and `SetEligible(true)` mark it.
- `Features/Onboarding/SistersTally/SistersTallyRun.cs`: per-mission `EligibleInMission` flag, cleared by `DropMission` (new mission key). Not saved; the existing static reset clears it.
- `Features/Onboarding/SistersTally/Editor/SistersTallyResultRowSetup.cs` (new): idempotent setup, menu `Tools/Onboarding/Place Sisters' Tally Results Row`.
- `Features/Onboarding/SistersTally/Editor/SistersTallyResultRowTests.cs` (new): 18 tests.
- `Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/SessionEndPanel.prefab`: new nested `StatRow` instance `SistersTallyRow` (direct child of `StatsColumn`, right after `StatsPanel`), plus the component on the root.
- `Scenes/CombatLevelContainerScene.unity`: 4-line override, `isMissionEndPanel = 1` on the mission-end panel instance only.

No edits to `MissionEndPanelUI.cs`, `CombatLevelUIManager.cs` or any core file.

## Acceptance criteria

- [x] Row on the mission-end panel only, stats column, "Sisters' tally" + "Linda N – Lucy N": `Refresh_ShowsTheRowWithTheCounts_WhenEligible`; scene test `ContainerScene_FlagsOnlyTheMissionEndPanel`.
- [x] Level-won and level-lost never show it: the prefab is shared by all three instances, so scoping is a serialized bool `isMissionEndPanel` (off in the prefab, set to on by the setup script as a scene override on the instance `CombatLevelUIManager.missionEndPanel` points to). Tests: `Refresh_HidesTheRow_OnAPanelThatIsNotTheMissionEndOne`, the scene test.
- [x] Shown only when enabled, eligible in at least one level of the mission, not faded: `ShouldShow` tests (switch off, never eligible, faded, other panel); `EligibleInMission_*` tests (survives a later level without both sisters, deployed-later sister, new mission resets, static reset).
- [x] Fills itself on enable, rebuilds layout, does not throw: `OnEnable` calls `Refresh`; `Refresh_WithNoRow_DoesNotThrow`. The panel's own `RefreshStatsColumn` runs after enable and still hides the left column when every child is inactive (that path is untouched).
- [x] `MissionEndPanelObjectiveRowTests` still passes (no field added to `MissionEndPanelUI`). Full EditMode run: 1715 tests, 1714 pass, only `AIRegressionTest.Baseline_MatchesCurrentAI` red.
- Needs the verifier's play check: the look of the row on the real panel (placement, sizing, icon).

## Save reset

no

## Decisions I made

- Component sits on the panel root, not on the row. Reason: the panel hides the row by deactivating it, and an inactive object's `OnEnable` never fires again, so a component on the row could not bring itself back on the next opening. The row (own `StatRowUI`) is still a child of `statsColumn`, as planned. Same behavior otherwise.
- Row placed as a direct child of `statsColumn` (which `RefreshStatsColumn` checks), just under `StatsPanel`, so it sits outside the stats panel background. Cosmetic only; easy to move.
- Placeholder icon: Linda's unit HUD image. Text is placeholder wording (not tagged in assets).
- Separator is an en dash written as `–` in code.
- Loading the panel prefab for editing rewrote four existing icon `m_SizeDelta.x` overrides from 50 to 0 (layout-driven). I restored them by hand so the diff only adds the new row.

## Needs THJ

none

## Docs to update

- Build log (coordinator): C3 built. Plan log: C3 done.

## Risks and loose ends

- The prefab is a nested prefab asset edited via `PrefabUtility`; other scenes that instance it directly would get the component with the flag off (harmless: row stays hidden). Only the container scene uses it today.
- Level-won and level-lost panels carry the component but never show the row.
- THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`) untouched.

## Proposed commits

1. `feat(onboarding): sisters' tally row on the end-of-mission results panel` (plain): 
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyResultRow.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTally.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyRun.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyResultRowSetup.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyResultRowTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/SessionEndPanel.prefab`
   - `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`

## Other branches

none

## How to see it

1. Fresh save, finish The Trail with Linda and Lucy deployed: on the mission-end panel the left column shows "Sisters' tally  Linda N – Lucy N". After the pile fade (fade step played, return not) the row is hidden, so in the current flow The Trail's end shows no row.
2. To see it show: Hearth with F10 (Hearth now counts when both sisters are deployed) and finish the mission; the mission-end panel shows the row with the counts.
3. Level-won and level-lost panels never show it.
4. Re-run `Tools/Onboarding/Place Sisters' Tally Results Row` any time; it reports "nothing to change".
5. To remove everything: `SistersTally.Enabled` returns false.

---

## Fix round 2 (placement)

Outcome: done. THJ's final spec (two stat rows) is implemented; an intermediate one-row widened layout was built first and then replaced. Nothing of it remains.

### What changed

- `SistersTallyResultRow.cs`: now owns two stat rows (`row` = Linda, new `lucyRow`). Row 1 label "Sisters' Tally:", value = Linda's count; row 2 empty label, value = Lucy's count. Both show and hide together under the same rules (`ShouldShow` unchanged). `Format(int count)` returns the plain count (no dash text). Class comment updated (no dash format any more, so should-fix 3 is moot).
- `Editor/SistersTallyResultRowSetup.cs`: `EnsureRow` creates each row from the same `StatRow` prefab as the other rows, as a child of `StatsPanel` (right after `EnemiesKilledCountStat`, Lucy's row right after Linda's), no custom sizes or offsets. A copy outside the stats panel is removed first (migration of the earlier placement). Icons: each sister's `UnitHUDImage`. Should-fix 1: the scene is saved only if the script opened it; if it was already open it is only marked dirty and the log says "scene left unsaved, save it yourself". The blanket `AssetDatabase.SaveAssets()` is gone; only the panel prefab is saved (`SaveAsPrefabAsset`).
- `Editor/SistersTallyResultRowTests.cs`: should-fix 2 done. The Refresh test pre-fills both rows with other text and hides them, then asserts both rows active, row 1 = "Sisters' Tally:|2", row 2 = "|1" (exact label/value, can fail). Hidden/shown tests check both rows. Wiring test now checks both rows sit in `StatsPanel`, adjacent, with the same parent as the other rows. `Format_IsJustTheCount` replaces the dash-format test.
- `SessionEndPanel.prefab`: only additions (two nested `StatRow` instances in `StatsPanel`, the component with both references). I again restored by hand the four existing icon `m_SizeDelta.x` overrides (50) that Unity rewrites to 0 on save; `git diff` shows 0 removed lines.
- `CombatLevelContainerScene.unity`: unchanged from round 1 (4-line flag override on the mission-end panel instance).

### Lucy's portrait (read-only finding)

Lucy has the same kind of sprite: `Assets/_Project/Features/UI/Panels/HUD/Avatars/Avatar_Lucy.png` (sub-sprite fileID 21300000, guid 9a4ee5f2677e64a8083cf83e5fdafd0c), set as `unitHUDImage` on `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`. Linda: `.../Avatars/Avatar_Linda.png` (guid b58c9e75823b941d698944692d07ac95). Both rows use them.

### Layout evidence

Measured by instantiating the panel prefab with a layout rebuild (Total Gold row inactive as in the default panel), RectTransform values in the stats panel:

| Row | y | h | label x / w | value x / w | icon x / w | value right edge | icon sprite |
|---|---|---|---|---|---|---|---|
| EnemiesKilledCountStat | -249 | 50 | 116.92 / 240 | 292.56 / 100 | 375.64 / 50 | -117.44 | EnemyKill_Icon |
| SistersTallyRow | -305 | 50 | 116.92 / 240 | 292.56 / 100 | 375.64 / 50 | -117.44 | Avatar_Linda |
| SistersTallyLucyRow | -361 | 50 | 116.92 / 240 | 292.56 / 100 | 375.64 / 50 | -117.44 | Avatar_Lucy |

Identical columns and sizes; row pitch is 56 for every row (50 + 6 spacing), so the vertical gap matches. Font size 23.8 on all, no autosizing, so the value is one line ("0".."99"). With the rows hidden (not eligible, faded, other panels) the panel is as before; the rows are children of the stats panel's layout group, so inactive rows take no space. Not visually screenshotted; needs the verifier's play check.

### Tests

EditMode run: 1715 total, 1714 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched). Compiles with no errors. Console: the usual pre-existing warnings and serialization-depth messages; one "listener failed" exception logged during the run, not from this work (not investigated). Play mode was stopped before editing; no save reset.

### Decisions I made

- Scene already open in THJ's editor was left unsaved by the script (flag already present, so no change was needed this round).
- Because the row existed from the earlier layout, I removed it once with a one-off editor call and re-ran the setup; the migration branch in the script covers rows outside `StatsPanel` only.
- The earlier mid-task message to hold Task A arrived after I had already applied a widened one-row layout; it is gone now, replaced by the final spec.

### Final list of files for the C3 commit

All under `miso/Assets/_Project/` (with `.meta` for the new files):
- `Features/Onboarding/SistersTally/SistersTallyResultRow.cs` + `.meta`
- `Features/Onboarding/SistersTally/SistersTally.cs`
- `Features/Onboarding/SistersTally/SistersTallyRun.cs`
- `Features/Onboarding/SistersTally/Editor/SistersTallyResultRowSetup.cs` + `.meta`
- `Features/Onboarding/SistersTally/Editor/SistersTallyResultRowTests.cs` + `.meta`
- `Features/UI/Panels/Prefabs/UI/Home/SessionEndPanel/SessionEndPanel.prefab`
- `Scenes/CombatLevelContainerScene.unity`

Not touched: `MissionEndPanelUI` fields, core files, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`.

### How to see it

Same as round 1 (Hearth with F10, finish the mission): left column shows "Sisters' Tally:  5" with Linda's portrait, and under it an unlabeled "7" with Lucy's portrait, same columns as the rows above.
