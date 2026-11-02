# Review: C4b, The Ridge

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-02. Report: `reports/onboarding-c4b-ridge.md`.

**Verdict: APPROVE**

## Should fix

1. `SearchWiring.Ridge.cs:33-34`: comment uses the paper falloff (3.6); measured 0.9 → 6 then 5.4, 11.4 per Claw. (Levels plan lines 451/454 fixed by the coordinator.)
2. `SearchRidgeTests.cs:129`: assertion multiplies constants only; read HP and tier factor from data or drop.

## Notes

- Unlock: one line; node owned and Maxed (`SkillTree.cs:199`), no refund, no edges on node 9; Mark's total upgrade count +1 (editor dashboard only).
- `SleeperSightBeatSequence`: non-core, no statics, clears exactly what it lit on end/skip/level end; stale refs after a mid-beat destroy are harmless. Timing after the intro, rush pack already awake; nearest sleeper is the gauntlet.
- Shift clash: the player's held Shift preview and the beat share a bit flag, whichever clears first wipes the other's tiles until the next hover (cosmetic; a fix is core `GridCell`).
- Shared sequence restores input on every path; once-per-save key unchanged; `GB_s1-river` matches HEAD.
- Ridge matches the block; HP factor only on 7,1/8,1; MS2 data right. Clue props share one sorting order (cosmetic).
- LF, metas, no private IDs, no tag. Commit 2 builds alone; commit 3 depends on it. Falloff and return copy read from code, not seen in play.
