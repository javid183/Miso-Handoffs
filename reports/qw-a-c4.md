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

---

# Rev 2 (panel open, click toggles)

Supersedes the summary-line design above; everything from Rev 1 was removed. Nothing committed.

## What changed

- Removed: `CollapsedSummary` child, `collapsedSummary` field and logic, `ObjectivesSummaryRules.cs` + tests (+ .meta), the `Objective` getter. `ObjectiveEntryUI.cs` is back to HEAD.
- `ObjectivesFoldRules` (new, pure static): `StartsOpen` (true), `AfterClick(isOpen)` toggles, `AfterObjectivesChanged(isOpen)` always open.
- `ObjectivesPanelUI`: `_isOpen` replaces `_isHovering`. `UpdateObjectives()` (reached from `SetObjectives` + `UpdateEntries`, and from mid-level changes) marks the panel open, expands, reveals new/changed entries as before, and no longer shrinks afterwards. New public `OnClick()` toggles Expand/Shrink (ignored while a reveal is running). `OnHover`/`OnUnhover` removed.
- Prefab: only the `HoverInteraction` events changed: the enter/exit calls (OnHover/OnUnhover) are cleared and `OnPointerClickEvent` calls `ObjectivesPanelUI.OnClick`. No other diff vs HEAD (verified by `git diff`).
- Clicks land through the existing raycast-target Images (Art, Background, Mask) that bubble to the root `HoverInteraction`; no new raycast target added. Not play-checked.

## Decisions I made

- Deleted the dead `InitialWait()` coroutine: it called the removed hover flag and was never started. `initialShowDuration` field is kept (now unused) to avoid losing serialized data.
- Clicks during an entry reveal are ignored (existing `_forceShowPanel` guard), so a click can't fight the tween.
- Only the first reveal after `SetObjectives` expands an initially-open panel; the panel's initial mask height is whatever the prefab/scene has today.

## Acceptance

- Compile OK, no errors. `ObjectivesFoldRulesTests` (5 tests: start open, click toggles both ways, change while folded opens, change while open stays open): Pass.
- Full EditMode suite: 478/479 pass, only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known).
- Play check needed: panel open at level start and stays open, click folds/unfolds, hover does nothing, mid-level objective change re-opens a folded panel.

## Proposed commit (one)

Files:
- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectivesFoldRules.cs` (+ `.meta`)
- `miso/Assets/_Project/Features/UI/Panels/Scripts/ObjectivesPanelUI.cs`
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/ObjectivesPanel.prefab`
- `miso/Assets/_Project/Features/UI/Panels/Editor/ObjectivesFoldRulesTests.cs` (+ `.meta`)

Message: `feat(ui): objectives panel stays open and folds on click`
