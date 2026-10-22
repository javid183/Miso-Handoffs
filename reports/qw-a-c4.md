# Report: C4 objectives summary line (quick-wins A)

Plan: `plans/2026-10-21-quick-wins-a-tech.md`, section C4. Branch `thj/quick-wins`. Nothing committed.

## What changed

- When the Objectives panel is collapsed it now shows one line under the "Objectives" title: the first objective that is not satisfied. It is hidden while the panel is expanded (hover, or the change-reveal), and when every objective is satisfied or there are none.
- `ObjectivesSummaryRules` (new, pure static): `FirstActive(IReadOnlyList<LevelObjective>)` and `SummaryText(LevelObjective)` (line breaks become spaces so the line stays single).
- `ObjectivesPanelUI`: new `[SerializeField] TMP_Text collapsedSummary`. `Shrink()` refreshes and shows it (after the `_forceShowPanel` early-out, and only once `_initialized`); `Expand()` and `SetObjectives()` hide it.
- `ObjectiveEntryUI`: read-only `Objective` getter.
- Prefab `ObjectivesPanel.prefab`: additive child `CollapsedSummary` on the root (outside the Mask). TMP copied from the objective entry style (same font asset, grey 0.81761, size 18, centered, no wrap, ellipsis overflow, raycast off) plus a LayoutElement with ignoreLayout, anchored top-centre at y -76, 260x24. Starts inactive. `collapsedSummary` wired.

## Acceptance

| Criterion | Result |
|---|---|
| First-unsatisfied pick, all satisfied -> none, empty/null safe | Pass (7 EditMode tests, `MISO.Content.UI.UnitPanel.Objectives.EditorTests.ObjectivesSummaryRulesTests`) |
| Compiles, no new console errors | Pass (only pre-existing warnings) |
| Full EditMode suite | Pass: 480/481, only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known) |
| Prefab field wired, prefab diff only additive | Pass (160 insertions, 0 deletions; verified through SerializedObject) |
| Summary visible when collapsed, updates when objectives change while collapsed, hover expand still works, layout/overlap with title | Not run (needs the verifier's play check) |

## Decisions I made

- The summary is an ignore-layout child of the root, not a layout participant: the collapsed panel keeps its existing 90 px minimum height, so the line sits at y -64..-88 inside it. Not tested visually; if it looks cramped, nudge `anchoredPosition` on the child.
- No fade: the line appears the moment `Shrink()` starts (the Mask still tweens closed over 0.75 s), and disappears immediately on `Expand()`.
- Summary shown only after the first reveal (`_initialized`), so a hover-out before the intro cannot show it early.
- Prefab edited by YAML with fresh fileIDs (7312840115526047001..005); Unity did not rewrite anything else.
- No change to `CombatLevelUIManager`, `CombatLevelRunHandler` or the scene.
- No static state added.

## Risks and loose ends

- The summary shows the unsatisfied objective's plain `DisplayText` (no strikethrough/colour).
- Long text ends in an ellipsis at 260 px width.
- `ObjectiveEntry.prefab`'s serialized `m_EditorClassIdentifier` names a different namespace than the class; harmless (GUID is used), not touched.
- `ObjectivesPanelUI.cs` now ends with a trailing newline (original had none).

## Proposed commits

One commit, files:
- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectivesSummaryRules.cs` (+ `.meta`)
- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectivesPanelUI.cs`
- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectiveEntryUI.cs`
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/ObjectivesPanel.prefab`
- `miso/Assets/_Project/Features/UI/Panels/Editor/ObjectivesSummaryRulesTests.cs` (+ `.meta`)

Message: `feat(ui): collapsed objectives panel shows the first active objective`

## How to see it

1. Play a combat level with objectives. After the intro reveal the panel folds; the first unfinished objective appears as one line under "Objectives".
2. Hover the panel: it expands and the line disappears; move away: it folds and the line returns.
3. Complete the first objective: the panel expands, strikes it through, folds, and the line now shows the next unfinished objective. Complete all: no line.
