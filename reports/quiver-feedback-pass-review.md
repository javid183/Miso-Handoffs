# Review: quiver feedback pass

Reviewer: miso-reviewer, 2026-10-28. The reviewer is read-only, so the coordinator saved this.

**Verdict: APPROVE**

**Must fix:** none.

**Should fix** (sent back to the implementer):
1. `UnitPanelUI.Quiver.cs:97-107` `UpdateQuiverReach`: the lift only updates when the hover or selection state changes, so it can come back unlifted after an outside disable. Fix: call `UpdateQuiverLift()` every frame.
2. `GroundedArrowLook.CountLabel` is used by tests only, while the view formats `x{0}` itself. Fix: share one format constant.

**Added by the coordinator:**
3. While Linda's info panel is open, her pip row sits on Overlay order 2, above every unit's info panel, so it can cover a northern neighbour's HP bar. Make it sort only with her own panel.

**Notes:**
- **Core:** none touched. `AbilitiesBarHUDUI` and `UnitAbilityButtonUI` aren't in `core-systems.md`, and the press event added there is additive.
- **Tweens:** every tween is killed and reset on disable, destroy, hide and unit switch.
- **Statics:** no new mutable statics.
- **Allocations:** none per frame.
- **Sorting:** board arrow DynamicTop -4, `xN` -3, pips -1, all under the HP bars (0 and up).
- **Commit units:** each compiles alone, in plan order.
- **Hygiene:**
  - CRLF kept, no BOM.
  - No private IDs.
  - `QuiverUI` is namespaced `MISO.Content.UI.UnitPanel`, keeps its GUID and has no NUnit import.
- **Encore shine:** comes from the threat-line material (time-driven along UV.x), running from the stack to Linda.
- **Nudge:** `IconOffset` went from 0.18 to 0.35, about 0.17 of a cell more.
- **Number key at 0 arrows:** pressing `1` can punch the quiver during a banner. Feedback only; acceptable.
- **Loose ends:**
  - The quiver instance in `CharacterHUD` is active by default; `ClearQuiver` hides it on the first unit.
  - Each `xN` label gets its own TMP material copy, as the return cue does.
