# Enemy alert C4: review

Reviewer: `miso-reviewer`, 2026-10-24. Saved by the coordinator. **Verdict: APPROVE** (no must-fix).

## Should fix
1. Stale preview on wake (`ShowStatsHoverPreview.cs:154-178`): redraws only on Shift/hover change, so a unit woken while Shift is held keeps its sight/alert tiles and its real move layer and danger zone never appear. Watch `UnitAlerted` / `IsUnaware` and redraw; unsubscribe in `Rebind`.
2. `Deevoted.prefab:184-185` overrides `attributeEntries` size to 4, so attribute effects on `Specs_Sight`/`Specs_AlertRange` do nothing on it (falls back to definition defaults 3/2). Drop the size override. `Lucy_Decoy_ValidVariant.prefab:164` same, harmless (player side).

## Notes
- Plan text stale: rules 4–5, the formula acceptance line, "Later"/"Out" still list the sight-area preview. Coordinator to update.
- Hover trigger: built as Shift + hover; THJ to confirm.
- Alert tiles reuse the red `EnemyAttack` icon and may read as a threat zone; a distinct tint needs a `GridCell.ShiftPreview` change (core). Flag at play check.
- Attributes data clean: appended after FP, ids/order intact, no attribute code changed, `Indicated: 0` (hidden in `UnitPanelUI.cs:130`), not saved; AI and `AIRegressionTest` look up by id (38/709 unchanged). Masher override `data[4]` = `Specs_Sight`. Reads via `RuntimeAAttributeBase.Value` on the main thread; `RangeWithBonus` correct; 0–99 bounds.
- Re-serialization noise in UnitBase and Masher harmless (fields at code defaults). Copied `sBBounds` unused while `overrideBounds` is 0 (if turned on, Sight would cap at max FP).
- Removals complete; boss prefabs carry only `startsAlert`/`alwaysAlert`.
- `ShowStatsHoverPreview` not core; branch additive; layer bookkeeping correct.
- Marker: about 0.175 world units (cells 0.5); scale independent of sprite resolution.
- Tests meaningful; LF, no BOM, no statics, no private IDs.
- Five-commit plan compiles in order; commit 3 (C1 commit 2 + C2 + C4, shared files) is large and risky: say so to THJ.
