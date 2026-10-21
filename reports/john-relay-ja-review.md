# John relay J-A review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **APPROVE** (only `JohnFactionRoleHandler.cs` and `MasherGoblinFactionRoleHandler.Counter.cs` reviewed)

Should fix (to fold into J2/J-B):
1. `JohnFactionRoleHandler.cs:146-154`: if the trigger has already finished when `Activate` runs, John skips the retarget but still applies `receivedDamageModifier`, plays the shield and raises `abilityStarted`. Skip the reduction too when `trigger == null || !IsInProgress(trigger)`.
2. The new trigger rules (primary target by unit, cell, bundle) have no tests; move them into a pure helper next to `FactionRoleRules` and test them with J-B.

Confirmed:
- `Counter.cs` raises `abilityStarted` inside `onStart`, after `RecordAction`, matching `FactionControllerBase.cs:679-685`; the toggle gate is kept.
- On a normal enemy turn, John relays exactly as before, apart from two intended differences: allied role events no longer re-trigger him, and nobody is relayed when John is a primary target.
- No false triggers on the player's turn.
- A Masher answer arriving during John's QTE retargets in time.
- J-A compiles alone; stage exactly these two files. No BOM, CRLF kept, no statics.

Notes:
- **J-A alone moves the Masher's area onto John**, so his neighbours get hit. Don't play-check J-A without J-B.
- J-A makes the J3 input risk reachable (`PlayerController.cs:1476/1485`), so J3 must land before the play check.
- Instant or InstantAnimated attacks can't be retargeted late; J-B's `GetTargets` record route avoids this.
- The AI golden master is not expected to move.
