# Review: M2 Trail C4 (balance values)

Reviewer: `miso-reviewer` (read-only; filed by the coordinator from its hand-back, 2026-11-11). Plan: `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` C4. Report: `reports/m2-trail-c4.md`.

**Verdict: APPROVE.** No must-fix, no should-fix.

- Prefabs vs C3 (`9e9e0ca63`): same document types/counts, units, cells, hidden groups, deploy slots, arrivals, objectives (only managed-ref renumbering). Real diffs: the `enemyTier: 1` override removed on all four (Standard = 0 is the default, `CombatLevel.cs:31`); Tracks' five HP overrides → one Black Claw 0.75 (hidden pair has none).
- Tests assert literals (tier Standard ×4, 0.75, no override elsewhere, Claw 16, Cyclone `baseFactor` 3). Black Claw's 30 HP not asserted directly (factor only; enough for the plan).
- Cyclone: `attributeModifiers[0].factor.baseFactor` on `Specs_Health`, reads `Stat_DMG`: the damage multiplier. Cooldown, `PassByEffect_AttrMod`, Linda-folder files unchanged. Reach: the Linda-folder Compound and the OnGridTest `TestSpawn1` compounds point at the same AttrMod, so they also hit 3 (no test depended on 7). "3 per hit" holds if Lucy's `Stat_DMG` is 1 (not checked).
- AI golden master may move (known red; never re-baselined). House rules kept (no IDs, LF/no BOM, seven files only).
- Commit order: Cyclone asset alone first, then prefabs + wiring + whole test file: every commit green bar the known red. Reverting commit 1 alone leaves `LucysCycloneDealsThreeDamagePerHit` red (acceptable). Don't use the implementer's reverse order.
- Plan pointer: C4 criterion 1 names `design/level-chunks.md`; the blocks are in `plans/onboarding/2026-11-11-post-hearth-challenge-design.md` (fixed in the plan).
- Open: THJ's play, both picks.
