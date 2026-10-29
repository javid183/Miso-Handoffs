# Review: strip-down play tweaks (D-299), 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: FIX**

## Must fix
1. **The commit units don't build.** Log unit 1 removes `AddCustom`, which HEAD's `QuiverLogListener` still calls. Split into three:
   - (a) Core: add `Suffix`, `AnnotateAction` and the held line, keeping `AddCustom`.
   - (b) Linda: switch the listener, lines and tests.
   - (c) Core: remove `AddCustom` and `Tagged`.
2. **A held action line leaks into the next attempt on a pause-menu restart.** Call `WritePendingAction()` in `HookLevelEvents` before `ResetLevelState()`.

## Should fix
1. **The hold behaviour has no test.** Move it into a small pure helper and test it.
2. **Dead code (D-295).** Remove:
   - `CombatLogFormat.Tagged` and its test;
   - `GroundedArrowField.OnArrowLanded`, `OnArrowsPickedUp` and `OnRecalled`;
   - `ArrowPickupMoment` and `TryPickUp`'s moment parameter.
3. **Unused `using`** in `CombatLog.Custom.cs`.

## Notes
- **Suffix kept on:** bow, Watch, pickup on a move, Encore, and Mark's catch.
- **Suffix can be lost:** a quiver change after a nested ability closes in the same action, which is likely in Duo flows.
- **JSON:** every line gains `"suffix":null`.
- **HUD quiver placement:** correct only if the portrait's anchors are a point. Check it in play.

---

# Re-review after fixes

**Verdict: APPROVE.**

- The restart flush is correct. The hold logic lives in `CombatLogBook`, with its tests.
- No references to removed members remain.
- Flushes run on level end, turn change, ability close, mission end and restart. Quit was never flushed, before or after this change.

**Commit list** (builds in order, no hunk splits):
1. Core Projectile sweep, alone.
2. The combat log annotation plus the quiver count on action lines (Core log files and the Linda listener and lines).
3. The quiver strip-down code, including the field-event removal and the HUD placement.
4. Pip and "+1" size.
5. Rigidbody2D bodies on the 5 arrow prefabs.
6. THJ's art plus the `Unit_Linda.prefab` wiring plus `QuiverWiringTests.cs`.

Play check: include one pause-menu restart taken mid-action.
