# Review: quick wins bundle P, C4 (banner side) and C5 (end-menu delay)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22.
Plan: `plans/2026-10-22-quick-wins-p-pace-tech.md` C4, C5 (D-144). Implementer report: `reports/quick-wins-p-c4-c5.md`.

**Verdict: APPROVE.** No must-fix or should-fix items.

## Notes

- **C4 layout:** correct for the real layout (prefab shown (−16, −260), hidden (+760, −260); root 570 wide × 1.3 = 741 px). Right: rests 16 px in from the right edge; hidden, its left edge is 19 px past the right edge. Left: anchors/pivot x 0, shown (16, −260), hidden (−760, −260); rests 16 px in from the left edge; hidden, fully off-screen left. Scale grows from the pivot, so it mirrors too. The root starts at the hidden x and `Awake` mirrors it, so no flash on the wrong side.
- **C4 children:** none need mirroring. Top/Bottom panels, Mask, both faction-name panels and their labels stretch full width (labels anchored 0.165–0.835). Only MiddlePanel (Faction Logo Frame, InfoPanel) uses left anchors, and it's inactive. The only asymmetry left is the background/mask sprite art (D-144: content not flipped).
- **C4 timing:** the scene's PhaseVisuals is active, so `Awake` runs at scene load, once. `UIPanelAnimator` doesn't move the rect. `HideInstant` on an inactive object is null-guarded; `UpdateValues` before `Awake` would throw (pre-existing, not reachable). Changing `Side` during Play applies from the next scene load.
- **C4 tests:** the new `Features/UI/Panels/Scripts/Editor/` folder compiles into `Assembly-CSharp-Editor`; namespace, header and names match `TurnStartPauseTests`/`GridHoverGateTests`; tests check real values. `using MISO.Content.UI;` is redundant, harmless.
- **C5:** field next to C2's two, replaces the hard-coded `1`; `CustomTime` = scaled `WaitForSeconds`, as before; initialiser applies with no scene edit. No statics, AI-read code, renames or save changes.
- **Housekeeping:** line endings/BOM kept (`PhaseVisualsUI.cs` LF no BOM; `CombatLevelRunHandler.cs` LF with BOM; test file LF with BOM). No private IDs. Commits: C4 with its test and both `.meta` files; C5 alone.
- **Not verified:** the Left slide and the end-menu timing in Play. The root's unused `UIPanelAnimator` still holds old positions (dead config, noted in C3).
