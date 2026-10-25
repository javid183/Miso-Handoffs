# Tag registry desync fix: review

Reviewer: `miso-reviewer`, 2026-10-24. Saved by the coordinator. **Verdict: APPROVE** (no must-fix, no should-fix).

- `GTagDefinitionSetSO.GetEntities()` (l.25-29) links roots on the set's own copies before collecting: fixes the root cause; 6 added lines; public API unchanged. Direct readers (`UtilityScoreGraphView.cs:143`, `LevelSpecTagTools.cs:241/296`) now get full IDs (intended).
- Thread-safe: plain C#, every writer writes the same parent, atomic reference writes, link-before-read per call, the map is assigned as one reference. Pre-existing and not worse: the `EntitiesRefMap` swap from several threads; the `L1GTags` re-accumulate at count 0 doing a Unity bool check off the main thread.
- Player builds: one extra relink at load, same result.
- Cost negligible next to the existing per-call map rebuild.
- Tests: two would have failed before the fix (full ID; `KeyNotFoundException`); the idempotency test and the project-registry smoke test don't guard the bug. All depend on `Status.ShieldUp` existing.
- Compiles into Assembly-CSharp-Editor; CRLF/no BOM kept on the runtime file; test file LF; no private IDs.
- Icon line matches `GTagSet.asset:106`; it belongs in the held tag-data commit.
- The fix commit must include `GTagDefinitionSetParentLinkTests.cs.meta` once Unity creates it.
