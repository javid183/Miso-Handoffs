# Report: Skill tree highlight no longer throws when its node isn't shown

Plan: plans/onboarding/2026-11-07-bond-lite-play-fixes.md (chunk C1)    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done (compiles by inspection; not run in the editor)

## What changed

- miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.Highlight.cs: in `Update()`, when the highlighted node has no button in the shown tree, stop any pulse and return before the pulse math. Previously `button` and `_pulsing` were both null, so the "button changed" branch was skipped and `_pulsing.transform` threw every frame. The null check moved out of the "button changed" branch (3 lines added, 1 removed). LF endings and no BOM kept.

## Acceptance criteria

- [x] No exception when the highlight is active but its node isn't in the shown tree: `button == null` now returns early, so `_pulsing` is never dereferenced. Needs THJ's play check.
- [x] Highlight stays active: `_highlight` is untouched on that path.
- [x] Switching to the tree that holds the node starts the pulse: next frame `button` is non-null and differs from the null `_pulsing`, so the existing branch sets it up and observes the start level. Needs THJ's play check.
- [x] Other behavior unchanged: the rebuilt-tree, level-check and pulse paths are the same code.

## Save reset

no

## Decisions I made

- No EditMode test. The fix is a null guard in a MonoBehaviour `Update()` that depends on `abilityButtons`, `_nodeEntries`, `Time` and scene objects. `TreeNodeHighlight` (the only pure part) is unchanged and its logic was not the bug. Extracting a decision helper just for one `if` would be more code than the fix.
- EditMode suite not run: `miso/Temp/` exists, so the editor is open and batch mode isn't possible. Run it from THJ's Test Runner. Expected only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- `FindEntryIndex` still runs every frame while a highlight is active and not found (a loop over node entries). It is cheap and was already the case; left alone.

## Proposed commits

1. `fix(home): skill tree highlight no longer throws when its node isn't shown`: miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.Highlight.cs (plain)

## Other branches

none known

## How to see it

1. In Unity, recompile (Ctrl+R) and enter Play.
2. Start a state where the highlight is active (the onboarding step that points at a skill tree node) and open the skill tree on a hero or tree that does not hold the node. The console should stay clean.
3. Switch to the hero or tree that holds the node. Its button should start pulsing.
4. Run the EditMode suite in the Test Runner.
