# Review: Memory 4 rework R3 (2026-11-06)

Reviewer: miso-reviewer (saved by coordinator; reviewer is read-only).

**Verdict: APPROVE.** No must-fix.

Should fix:
1. `HearthMemoryWiring.Mark.Sequences.cs:47-56` intro ends with EnablePlayerInput + ShowHUD, then the level-start cut-in (`:79-89`) hides the HUD, and `CombatLevelRunHandler.cs:195-200` shows it after `levelStarted`. Show/hide flicker; End Turn ignores `SetInputActive` (`PhaseControlPanelUI.cs:41-46`), so a HUD left up lets End Turn be clicked during the cut-in. Fix: drop the intro's trailing two steps; play-check HUD hidden in the cut-in; if not, one-frame wait before the cut-in's HideHUD.
2. `HearthMemoryMarkTests.cs:174-181` `TheMemoryRulesAreTheHearths` checks tier + alert only; add FP full or rename.
3. Report says 29 tests; 28 `[Test]` methods.

Notes: deviation 1 (Mark visible) claim verified (FactionControllerBase.cs:105-106, UnitsCooperationHandler.cs:54/:94, HiddenLevelUnits.cs:127 only RegisterUnit); deviation 2 verified (CombatLevelRunHandler.cs:185/:190); CastAbilitySequence always restores input/HUD on failure; idempotency builders reuse; 9 deleted asset GUIDs unreferenced; stage 3 waits for SequencePlayer (CombatLevelRunHandler.cs:660-670); locks complete, only Mark_Lucy unlocks; lines verbatim; no core, no IDs, no statics, CRLF no BOM kept. Stray `_GuidedSpendScratch.unity` from an interrupted test: don't stage, delete after a clean run. Play-list risks: turn-1 banner / Linda auto-select camera under the cut-in; SequencePlayer one-at-a-time if the Cyclone itself kills a Bloom Claw. Commit: one; stage `Memory4Mark/` with `git add -A` scoped to the folder.
