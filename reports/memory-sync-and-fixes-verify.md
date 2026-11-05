# Report: Memory wiring sync, dialogue image-first and RestartTurn tint verify

Plan: reports/memory-tweaks-sync.md, reports/level-end-box-and-reset-overlay-fix.md    Agent: miso-verifier    Branch: thj/onboarding
Outcome: done

Result: PASS (quiet checks only, no Play mode; editor was in Edit mode on PreloadScreen, no Prefab Mode open).

## What changed

Nothing edited by QA except this report. Scratch files (before/after md5 and diffs) are in the session scratchpad.

## Acceptance criteria

- [x] Step 1, compile: forced refresh with compile request; the editor was ready, Editor.log has 0 `error CS` lines, console errors = 0 (only pre-existing CS0108, CS0114, CS8509, CS8524, CS0168 warnings). The log's last `CompileScripts` was about 1 ms, so the changed scripts were already compiled before the refresh.
- [x] Step 2, wiring idempotence: saved before-state (diffs of `GB_m1-linda.prefab` and `GB_m2-lucy.prefab`, `git status --short` of Resources/Sequences/Hearth, plus md5 of all 106 files under Hearth and both prefabs). Ran Tools > Onboarding > Wire Memory 1 (Linda), then Wire Memory 2 (Lucy), then `AssetDatabase.SaveAssets()`. Result: NO difference. md5 of all 106 files identical, both prefab `git diff` outputs identical, Hearth `git status` identical (it still shows the already-modified Linda and Lucy interruption sequences and the untracked Lucy `InterruptionLSBExecutionSequence` and `Interruption_UnlockAbilities` assets, as before). Console confirmed "Memory 2 (Lucy) wired: start, interruption, win stages and end."
- [x] Step 3, EditMode Run All: 1355 run, 1354 passed, 1 failed, 0 skipped (224 s). The only failure is the known red `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (41 failures of 712 checks). No GridToLevel leftover problem.

## Save reset

no

## Decisions I made

- Ran both wiring menu items through `execute_menu_item` (Prefab Mode confirmed closed first via `PrefabStageUtility`).

## Needs THJ

none

## Docs to update

- `tech/editor-checks.md`: the whole EditMode suite on `thj/onboarding` is 1355 tests, about 224 s through the Unity MCP; `get_test_job` disconnects/times out once or twice, and with `include_details` off the saved result has `results: null` (only the summary and the failure list).

## Risks and loose ends

- I didn't confirm the new `DialogueOpeningTests` and `RestartTurnTintTests` by name (the result file had no per-test list); they sit inside the 1354 passes.
- Neither prefab nor any Hearth asset changed on disk from the wiring, so the working-tree edits there are exactly what was already pending.

## Proposed commits

none (QA)

## Other branches

none

## How to see it

1. Tools > Onboarding > Wire Memory 1 (Linda) / Wire Memory 2 (Lucy), then `git status`: nothing new.
