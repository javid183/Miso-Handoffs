# Report: Playtest B3, HP text never reads 0 on a living unit (chunk C3)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

## What changed

- `miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/FillBarTextFormatter.cs` (new, + .meta): pure static helper. `CurrentValue(ratio, max)` = RoundToInt(ratio*max), but at least 1 while ratio > 0; 0 when ratio is 0 or max <= 0. `Format` builds "cur/max".
- `.../Elements/UI_Element_FillBar.cs`: line 46 now `FillBarTextFormatter.Format(fillValue, _maxValue)`. Ratio, bar fill and everything else untouched.
- `.../Elements/Editor/FillBarTextFormatterTests.cs` (new, + .meta, + `Editor.meta` folder): 6 EditMode tests (0 -> 0, 0.2 HP of 10 -> 1, 0.5 HP -> 1, full -> max, normal rounding unchanged, max 0). Namespace `MISO.Core.UI.EditorTests`.

No HP rounding, Attributes, AbilityDamagePreview or core system changed (D-054). Line endings kept (LF file, new files LF).

## Acceptance criteria

- [x] B3: living unit's HP text never reads 0, 0 still shows when dead: covered by the 6 tests (logic). The on-screen check needs the verifier's play check.
- [x] Rounding of HP values not touched: only the text formatting changed.
- [x] Nothing else changes.

Tests: the 6 new tests pass. The full EditMode run (67 tests, taken just before my test files were compiled in) had 66 pass and only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known). Unity console shows only that AI regression report as an error.

## Save reset

no

## Decisions I made

- The ratio is the test for "alive" (ratio > 0), as in the plan. Dead units have ratio 0, so they still show 0.
- Added a guard: max <= 0 shows 0, never "1/0".
- The helper sits in the same namespace as the bar (`MISO.Core.UI.Runtime`).

## Needs THJ

none

## Docs to update

- `build-log.md`: add a C3 entry (coordinator).

## Risks and loose ends

Every user of `UI_Element_FillBar.SetMainBarFill(..., true)` gets the new rule, not only HP bars:
- `EntityInfoPanelUI.ShowHealthMode` / `ShowFullMode` (enemy/ally hover panel, the reported case). In damage-preview mode the text shows the future HP, so a hit leaving 0.3 HP would show 1; a hit that kills (ratio 0) shows 0.
- `UnitPanelUI` (lines ~133, ~164; player unit panel): same bar, same fix.
- `MissionCharacterIconUI` (line ~114; mission graph portrait): same bar, same fix.
- `SharedAPIndicator` and `FTPIndicator` use the same bar for AP/FTP. These are integers, so ratio > 0 already means at least 1; no visible change. Only a fractional AP/FTP below 0.5 would now show 1.
Other HP text found by grep: none that formats HP another way in `Features/UI` (the only other "x/y" text is `SharedAPIndicator.cs:78`, AP, unchanged). I did not search combat log or tooltip code beyond a grep for HP formatting; nothing found.
- The underlying fractional HP (D-054) still exists; the bar fill for 0.3/10 is a sliver, as before.

## Proposed commits

1. fix(ui): HP bar text shows at least 1 while a unit is alive (plain):
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/FillBarTextFormatter.cs
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/FillBarTextFormatter.cs.meta
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/Editor.meta
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/Editor/FillBarTextFormatterTests.cs
   - miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/Editor/FillBarTextFormatterTests.cs.meta

## Other branches

`thj/home-test` gets it on its next merge of `main`.

## How to see it

1. Test Runner > EditMode > run `MISO.Core.UI.EditorTests` (6 green).
2. In combat, get an enemy to a fractional HP between 0 and 0.5 (or temporarily set its HP in the inspector) and hover it: the bar text reads 1/X, not 0/X. A killed unit still reads 0.
