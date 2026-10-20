# Review: preview-pass C7 (follow zones for every Bergson, cover icon = coverer's icon, C6 should-fixes)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **FIX (commit plan only)**; code approvable.

Must fix (done by the coordinator): `LindaFactionRoleHandler.cs` and `LucyFactionRoleHandler.cs` are core (`tech/core-systems.md` Family Roles), so their new public `GetCellsInRange(GridCell origin)` (UI only, additive, same overload John and Mark already have) goes in its own commit. Committed as three: should-fixes `a7ed7d588`, handlers `5ac017c0e`, presenters `857b05eaa`.

Notes:
- Should-fixes correct (player-faction gate; a footprint-only zone is never a duplicate).
- Follow zones correct for all four, normal style, skipped when equal to the ghost's basic attack. Linda and Lucy show no zone during a move preview (follows D-082 "hidden entirely"; with Shift held their committed zone disappears while others stay: tell THJ).
- Linda's and Lucy's `GetCellsInRange(origin)` give the same cells as `GetCellsInRange()` on the current cell.
- Suppression: no stuck path; worst desync shows the zone, never hides it. The flash on commit is a hide-then-show, acceptable for now; ~6-line fix in `MovePreviewCoverPresenter.Update` (hold suppression during TakeAction) if C9 finds it noticeable.
- Presenter link via `GetComponent` on the same GameObject (both added in `ShowStatsHoverPreview.cs` L27-29) is safe; no statics.
- Cover icon via `SetRoleZone` per coverer; D-067 fist rule untouched; `SetCoverIcons` no longer called.
- Under Shift, a cover icon and the coverer's committed zone in the same quadrant share sorting order −10, so draw order isn't guaranteed: C9 item.
- Docs: `tech/combat-architecture.md` should note all four role handlers have `GetCellsInRange(origin)`.
