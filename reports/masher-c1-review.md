# masher-c1 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **FIX**

- Turn-switch hold (D-102): correct; committable as is. No-hold turn flow identical; watchdog, clearing and tests sound; no statics.
- AI wait (D-101): does not close the race. Two idle samples cannot rule out a fast plan finishing between them (`AIFactionBrain.cs:116-150` clears `_computing` on the worker). Must fix: in `AIController.HandleUnits`, right after `_factionBrain.ConsumeWorkerError();` add `if (PhaseData.IsInProgress) continue;` (drops the stale plan, waits, replans). No behaviour change without an answer. The coordinator's "C4 waits one idle frame" idea is not sufficient.
- Should fix: leave the unrelated Packages/ProjectSettings changes unstaged; the report's line-ending note is wrong (files are BOM + CRLF on disk like their neighbours; no churn); list the public nested `TurnSwitchHoldSet` with the hold API in `tech/core-systems.md`.
- Constraints for C4: (a) retry when `TryPlayFactionRole` returns false (the AI prediction keeps `isActionInProgress` true after `abilityPerformed`); (b) hold until the last answer's `onComplete`, never release after a failed start; (c) pump waits frame-based or unscaled; (d) verifier watches `TrySelectUnit` → `CleanupUnitTurn()` during Mark's enemy-turn chain.
- Other branches: `thj/home-test` needs both commits when the Masher work merges there.
- Open: EditMode suite not run (MCP unavailable this session).
