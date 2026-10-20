# Review: preview-pass C2 (PlayerController ghost and approach reach)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **APPROVE**. Must fix: none. Should fix: none.

- Scope: three call sites (ghost icons L996 → `BasicAttackReachFrom`; `AttackReachesFrom` L1385 and `ShowApproachAttackRange` L1445 → `AttackReachFrom`); private `ComputeAttackRangeFromOrigin` deleted (no other callers; the Masher Goblin method of the same name is unrelated). `ShowAffectedArea` branch unchanged. No statics; LF, no BOM.
- Ghost and approach now match real targeting (straight, ranged reach, IncludeSelf, ignoreRelationOnWalk, faction). The ghost's own approach cell no longer lit for ranged attacks with includeSelf 0: correct (real targeting passes `source`, which removes the unit's tiles), covered by D-085.
- Residual risk (C1 design, not C2): for multi-cell units the helper unions reach over every footprint cell for all walkability modes; the real `GetRangeCells` does so only for Unconstrained. No effect on 1x1 Bergsons; keep in mind for C9 or a C1 follow-up.
- Tests: none added (needs a live scene); C9 covers Linda's gap, Mark's ranged reach, the approach highlight, ShowAffectedArea, and that no basic attack has includeSelf.
