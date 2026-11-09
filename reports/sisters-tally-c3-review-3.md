# Sisters' tally C3, fix round 3 (MVP row): review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix, no should-fix.

## Notes (verified)

- Nothing re-activates the MVP row: `MissionEndPanelUI.UpdateValues` (117-138) only sets value and icon; its `SetActive` calls are on `objectivesColumn`, `statsColumn` and `resourcesBarUI`. `CombatLevelUIManager` 345-353 runs SetActive, then UpdateValues, then SetObjectives.
- Restore: the row is hidden only while the tally shows; it is restored only if `_hidMvpRow` is set. Level won/lost instances never set the flag; null `mvpRow` is safe; the flag isn't serialized.
- Tests can fail (naive toggle, always-hide, missing restore; wiring asserts `AreSame` and rows inactive).
- Prefab: one expected `m_GameObject` change; `mvpRow` points at `MostKillUnitStat`; new rows `m_IsActive: 0`. Scene still only the `isMissionEndPanel` override.
- Metas full, GUIDs kept. LF, no BOM, no private IDs, no statics, no core edits.
- Commit list complete (7 files + 3 metas); THJ's files excluded.
- Open: play check (MVP gone when the tally shows; present on other panels). The hand-restored icon width overrides on the existing rows will likely be reset to 0 by any later Unity save of the prefab (layout-driven, no visual change).
