# Verify: B5 diagnostics removal (D-074)

Plan: reports/b5-diag-removal.md    Agent: miso-verifier    Branch: thj/fr-readability
Result: PARTIAL (all quiet gates pass; the play check was not run)

## Compile

Clean. Refresh with compile requested through the Unity MCP; editor state afterwards: not compiling, no pending reload. No `error CS` lines in the Editor.log or the console. Nothing in the console mentions HomeInteractables (errors or warnings). `HomeInteractables.cs` has 0 `B5-DIAG` matches. The console held only the usual project warnings (CS0108, CS0168, CS0414, CS8509, CS8524) and 8 errors that are not compiler errors: 7x "Objects are trying to be loaded during a domain backup" and 1x "Internal error - unexpected guid mismatch". The same "guid mismatch" line appears at several earlier points in the Editor.log, so it is not new. None name HomeInteractables.

## Tests

EditMode, full suite via the Unity MCP: 175 run, 174 passed, 1 failed, 0 skipped (52 s).
Failure: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` only (the known red, left alone). No other failures.

## Acceptance criteria

- Pass: Gate 1, compile clean (above).
- Pass: Gate 2, full EditMode suite green apart from the known red (above).
- Pass: Gate 3, static check. `Home - Scene.unity` line 7981 holds a prefab-instance override: target fileID 61089915482654192, guid db00749da4b5d05438beccde27fe39a2, propertyPath m_Enabled, value 0.
- Not run: Gate 4, after winning M3 - Mark Intro the Workshop opens on click every time, including hover highlight. Needs a play session (not agreed).

## Bugs found

None.

## Save reset

No.

## Editor checks corrections

- The full EditMode suite on this branch is 175 tests (about 52 s through the Unity MCP); tech/editor-checks.md lists 79 and 447 for other branches.
- `refresh_unity` with `compile: request` and `wait_for_ready` returned straight away while compiling. Poll `mcpforunity://editor/state` (`compilation.is_compiling`, `last_compile_finished_unix_ms`) before reading the console. `CompileScripts:` showed about 1.6 ms in the Editor.log, since little had changed.
- `get_test_job` with `wait_timeout` may return a TimeoutError once; call it again. Its output is saved to a file, as the doc already says. The totals are in `result.summary` and the failures in `progress.failures_so_far`.

## Left as found

Play mode off, active scene still PreloadScreen. No code, asset or scene edits and no git write commands.
