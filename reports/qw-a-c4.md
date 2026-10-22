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

---

# Rev 3 (mask re-measured when entries are revealed while open)

## Cause

`Expand()` reads `objectivesParent.rect.height` once, right after a layout rebuild, and tweens the mask to it. In `UpdateObjectives()` the entries are only revealed afterwards (`Show` calls `UpdateVisuals`, which sets the new text), so an objective whose text or line count changes at reveal time never grows the mask. Before rev 2 the panel folded again right after, so it was never noticed; a toggle (fold/unfold) re-ran `Expand()` and re-measured. Found by reading the code; not reproduced in Play mode.

## Fix (`ObjectivesPanelUI.cs` only)

- New `ResizeToContentIfOpen()`: if open, rebuild the layout, read the content height, and re-run `Expand()` only if it differs from the height the last `Expand()` targeted (`_openTargetHeight`, set in `Expand()`).
- Called after each entry's `Show` and once after the reveal loop in `UpdateObjectives()`.
- Both paths covered: change while open (re-measured per entry), change while folded (`_isOpen` is set true first, `Expand()` runs, then the same re-measure). `SetObjectives` at level start goes through `UpdateEntries` -> `UpdateObjectives`, so it gets the same re-measure.
- No prefab or other file changes in this revision.

## Verification

Compiles, no errors. Full EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known). The mask-height behaviour is UI and needs the play check: change the objective mid-level in LevelMarkIntro-C1 with the panel open, and again with it folded; the new objective should show without a fold/unfold. Proposed commit is unchanged (same files as Rev 2).

---

# Rev 4 (diagnostics, temporary)

`ObjectivesPanelUI.cs` now logs every step with the prefix `[OBJ-DIAG]` (SetObjectives, UpdateEntries per entry, each coroutine step with a counter, Expand/Shrink/Resize heights, OnClick). No other behaviour change, except the reveal loop now skips entries that are already destroyed (and logs them) instead of calling Show on them. The pre-diagnostics file is saved at `/tmp/ObjectivesPanelUI.prediag.cs` (Git Bash tmp). Remove all `[OBJ-DIAG]` lines and `DiagState`/`DiagText`/`Diag`/`_diagCoroutineCounter` once the cause is found. Compiles.

---

# Rev 5 (cause found, fix)

## Cause (from THJ's diagnostics)

At the stage change the new entry's `DisplayText` was still empty when it was revealed, so the open mask was sized for the shorter content (78). A later `UpdateEntries` set the text (content 112), but nothing was unrevealed or newly satisfied, so no coroutine started and nothing re-measured; only a click re-measured.

## Fix

- `UpdateEntries()` now refreshes every entry (it no longer stops at the first one that needs a reveal; the set of entries that get revealed is unchanged) and, when no reveal coroutine is started, calls `ResizeToContentIfOpen()`.
- The resize decision is a pure rule, `ObjectivesFoldRules.ShouldResize(isOpen, lastTarget, measured)` (open and differs by >= 0.5), used by `ResizeToContentIfOpen()`. 3 new tests in `ObjectivesFoldRulesTests` (grew, unchanged, folded).
- Rev 3 resizes kept. All `[OBJ-DIAG]` code removed (file restarted from the pre-diagnostics copy), so the destroyed-entry skip from Rev 4 is gone too (it was diagnostics-only).

## Verification status

Files written. I stopped Play mode once to compile and test, but the editor re-entered Play mode (Time.time ~20 s, not by me) and the test runner refuses to start while in Play mode, so I did NOT get a clean compile check or a test run for this revision. Needed: stop Play mode, let it compile, check the console, then run the EditMode suite (expect only `AIRegressionTest.Baseline_MatchesCurrentAI` red, 481 tests). Proposed commit files unchanged from Rev 2 (`ObjectivesFoldRules.cs` and its tests also changed).

---

# Rev 6 (rebuild the layout root)

## Cause (coordinator's live probe)

`LayoutRebuilder.ForceRebuildLayoutImmediate(mask.rectTransform)` does not recurse into children when the passed rect has no layout controller or element itself, so the content (`objectivesParent`, with its ContentSizeFitter and VerticalLayoutGroup) was not rebuilt and a stale height was measured until the next canvas update.

## Fix

`Expand()`, `Shrink()` and `ResizeToContentIfOpen()` in `ObjectivesPanelUI.cs` now rebuild `objectivesParent` instead of `mask.rectTransform`. No `ForceMeshUpdate` added: the layout reads the text's preferred height directly. Rev 5 `UpdateEntries` change kept; nothing else touched.

## Verification

Play mode was off. Compiles, no errors. Full EditMode suite run (see summary); only `AIRegressionTest.Baseline_MatchesCurrentAI` red. Play check: the stage change in the intro level should show the new objective without a fold/unfold.
