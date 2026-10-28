# Review: D1-C2 (Far readability) and the C1 tweaks, 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: APPROVE**

**Checked, C1 tweaks:**
- The effective upgrade level is used.
- The turn-1 fallback is correct in the enemy phase and on ally turns.
- The decoy cache is safe and resets per level.

**Checked, C2:**
- Placement is on the pips' layer. There's no Core import of Linda, no root objects, and no per-frame allocation.
- Everything sits behind the toggle.
- The simulated ghost positions follow the same rule as End Turn.
- The glyph fallback works, the tooltip wording follows D-291, and the tags are stripped.

**Hygiene and split:** C1 compiles alone, and C2 is a partial. No core change. LF, no BOM, no private IDs.

**Should fix (sent to the implementer):**
1. The "Far lost" label draws on WorldUI 61, above HP bars. Move it onto the pips' layer.
2. A downed Linda still shows the mark and box. Use `IsAlive && !IsDowned`.
3. Re-wrap the comment in `QuiverPromptLabel.cs:10`, and fix the indent at `UnitPanelUI.cs:260`.

**Notes:**
- `MarkOffset` is fixed when the mark is built.
- The box covers Linda's role-zone icons and John's cover icons. Check readability in play.
- The views and `LindaFarState` are covered only by play steps 11–22.
