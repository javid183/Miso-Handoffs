# Report: Mark the AI baseline test Explicit

Plan: plans/2026-11-19-faster-loop-process.md (change 5a)    Agent: miso-implementer    Branch: thj/cyclone
Outcome: done (compile and test run not verified)

## What changed

- miso/Assets/_Project/Core/Systems/AISystem/Editor/AIRegressionTest.cs: `Baseline_MatchesCurrentAI` now has `[Explicit("...")]` and a 3-line plain-words comment. 4 lines added, nothing else touched. LF, no BOM kept.

## Acceptance criteria

- [x] `[Explicit]` with reason, `[Test]` kept, only those lines changed: git diff shows 4 added lines.
- [ ] Compiles: not verified. Unity MCP server refused the connection and the editor log was last written 2026-11-18 20:12, so nothing could be read. The change is an attribute from NUnit.Framework, already imported by the file.
- [ ] Full EditMode run skips the test: Not run: THJ runs the Test Runner. Expect the test to show as Ignored/Not run in Run All.

## Decisions I made

- Play mode state could not be confirmed (MCP down, log stale). Nothing suggested Play was running, so I edited anyway as instructed.

## Save reset

no

## Risks and loose ends

- Tools/AI/Run Regression Test is untouched and still works.

## Proposed commits

1. `test(ai): mark the out-of-date AI baseline test Explicit so Run All skips it`: AIRegressionTest.cs (plain)

## Other branches

main (and any other branch that carries AIRegressionTest.cs).

## How to see it

1. In Unity, wait for recompile, open Test Runner > EditMode: `Baseline_MatchesCurrentAI` is not run by Run All; select it by name and Run Selected to run it.
