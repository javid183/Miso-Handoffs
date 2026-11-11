# Review: M2 Trail levels C1

Reviewer: `miso-reviewer` (read-only; filed by the coordinator from its hand-back, 2026-11-11).
Plan: `plans/onboarding/2026-11-11-m2-trail-levels-tech.md`. Implementer report: `reports/m2-trail-levels-c1.md`.

**Verdict: APPROVE.** No must-fix.

## Checked

- Layouts: cell counts 9 / 17 / 23 / 36 match the blocks; unit tiles, deploy slots (0,1 ×3; Pile 4,6), tier Early, `allEnemiesStartAlert: 1` in all four. Pile hidden groups `west` / `east`; props centred on 4,3–5,4.
- Duo lock: `LevelAbilityLock` (pattern `HearthMemoryWiring.John.cs`), only `Linda_Lucy_Duo_Ability`, for Linda and Lucy.
- No GUID references left to the Pass-by sequence, Items tutorial or rear wave; no `fpAmountToFill`, no `LevelSpecificBehaviour`.
- FTP full: `FactionTracker.InitializePoints` → new `FamilyTimePoints`, constructor sets value to max.
- Pile search: stage 1 onComplete = input off → Lucy's line → reveal west → reveal east → input on; `RevealUnitsSequence` reveals synchronously then waits, so stage 2 starts with the units live.
- `Trail_Tracks_Encore_CameraBack` camera point moved (explained); mission asset unchanged.
- No core or grid-tool changes, no new mutable statics, LF / no BOM kept, no private IDs. Tests assert real values and can fail.

## Should-fix

1. Blood's win is untested: in `SearchTrailTests.cs` (`TheTrailheadIsAOneStageFightWonByDefeatingEveryEnemy`, ~line 220) run the same asserts on `BloodPath` (one group, no queued groups, `LivingUnitsLOCondition` Enemy count 0).
2. The proposed commit split leaves tests red after commit 1: wiring, tests, prefabs and sequence assets only work together → one commit (coordinator: adopted).

## Notes

- `Unit_DarkClaw_StartsAlert.prefab` is no longer created/repaired by any wiring; `HearthPoolClawWiring.EnsureClaw` uses it as the source without setting the flag. Backlog line.
- Wiring doesn't remove a stale Pass-by `SequencePlayHandle` (safe: rebuild from template; test checks it's gone), unlike `RemoveStartFiller`.
- HP factors match exact unit names; a rename would fail the placement test.
- Left for THJ's play: revealed units alert and acting next enemy turn; goal tiles on 4,5 / 5,5; FTP 5 at the Trailhead; Duo hidden; arrows over the gap row and rock.
- Not re-run by the reviewer: the EditMode suite (1874/1875, known red) and idempotence (md5 identical on runs 2 and 3).
