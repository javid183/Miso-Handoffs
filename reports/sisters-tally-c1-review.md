# Sisters' tally C1: review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Three should-fix, to do with or before C2.

## Should fix

1. `SistersTally.cs:62-63`: public `Run` is unused (comment says the listener reads it; it doesn't) and hands out the live run, so a caller could add kills without the eligibility check or `Changed`. Remove it.
2. `SistersTallyListener.cs:74-75`: the comment above `OnLevelEnded` reads as if it contradicts banking on `Win`. It's right only because the last level's win arrives as `EndLevelResult.MissionComplete`. Say that outright.
3. `Editor/SistersTallyTests.cs`: every kill test injects both the faction and health checks, so the real `health.Value <= health.Bounds.min` check (`SistersTallySource.cs:49-53`, which keeps Dom's fake death out) is never tested. Make it a small public function (e.g. `SistersTally.IsAtMinimum(value, min)`) with a test incl. overkill. `SwitchOff_TheLevelDoesNotConnect_AndNothingCounts` passes because eligibility was never set; optionally start an eligible level first, then reconnect with the switch off.

## Notes (verified)

- Kill rule: the extra minimum-HP check is needed (Dom `FakeDie` above 0 HP while `CombatLevelRunHandler.cs:834` reports lethal; spawner-bound `Die(0)` above 0 HP). Overkill passes (`<=`). Dark Worm split excluded until it really dies. Fully absorbed hits raise nothing. Dead units are deactivated, not destroyed. Lucy's Decoy never counts for Lucy. **Goblin Queen's finishing move (`PerformSuperTime` → `deathEvents` → `Die`) raises no damage event, so that finish counts for no one** (designer FYI).
- Revert: only `AEffectTransporter`, `AEffectCommand`, `AGUnitSpawner` add undo actions; none restore HP. Skipping revert code is right.
- Bank/drop: mid-mission win banks; defeat drops; Restart Level (same seed) drops; restart from the mission-end panel replays only the last level; re-entry rerolls `GraphSeed` → 0; no `onRewardsGranted` listener is fine; `levelEnded` fires after a yield, so the final kill counts first. A mission-failed panel would show won levels only.
- Guards, subscribe/unsubscribe symmetry, `ReleaseFadedCheck`, `PlayModeStaticReset` line: fine. With `Enabled` false, `Connect` returns before subscribing.
- Loose ends for later chunks: `RefreshFaded`, `BankAttempt`, `DropAttempt` raise `Changed` even with the switch off, so C4's steps must check `Enabled` first. A throwing `Changed` listener stops the ones after it: C2/C3 listeners must not throw.
- Prefab YAML valid (fileID unique, `m_GameObject` = GlobalEventBus object, script GUID matches, The Hearth GUID `8b94f6b8c1006aa46a93b879db666882`, LF kept); 7 new `.meta` GUIDs unique; new files LF, no BOM.
- No private IDs. One commit is right (the core line only compiles with the feature files).

Not verified: live play; the reviewer didn't re-run EditMode (report: 1645/1646, known AI red only).
