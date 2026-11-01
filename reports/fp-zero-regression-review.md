# Review: FP 0/0 regression and Play hardening

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. **Verdict: APPROVE** (no must-fix).

Root cause confirmed (`Mission.CreateSandbox` roster empty; old `ApplyToMission` returned early with nothing pending → `InitializePoints` 0/0). Real missions unchanged; no double spawns (`FillRosterSlots` skips names already in the scene); restart keeps the roster; statics reset; hardening per plan; editor-only; LF/no BOM in runtime files; commits stand alone.

## Should fix (coordinator: all sent to the implementer)
1. `LevelBase.cs:236`: keys written before Play can survive a refused Play + recompile → next ordinary Play fast-forwards into the old level. Add an `[InitializeOnLoadMethod]` clearing `IdKey`/`PrefabPathKey` when `!isPlayingOrWillChangePlaymode`.
2. `LevelFastForwardRosterTests.cs:57-72`: test re-does `ApplyToMission` by hand; add a seam and call it on a sandbox mission with nothing pending.
3. `LevelFastForwardRoster.cs:126`: `GetComponentsInChildren<GUnit>(true)` counts inactive placed units; pass `false` (FillRosterSlots ignores inactive ones).

## Notes
- The early write doesn't cover a stale `EnteredEditMode` arriving after `EnterPlay`; sturdier: skip `Teardown` when `isPlayingOrWillChangePlaymode`. (Coordinator: included, as part of the approved hardening.)
- New test file is CRLF; folder is LF (coordinator: normalise).
- "All levels" unresolved: THJ's check on a listed level and the main-menu flow decides.
