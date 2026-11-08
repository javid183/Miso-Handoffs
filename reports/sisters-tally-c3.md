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
