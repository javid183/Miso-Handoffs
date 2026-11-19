# Review: Masher plow, C1 (pure rules and tests)

Plan: plans/2026-11-18-masher-plow-tech.md    Report: reports/masher-plow-c1.md    Branch: main

## Verdict: APPROVE

(One Should fix worth doing before or at the start of C2; it does not block the commit.)

## Must fix

None.

## Should fix

1. `Scripts/MasherPlowRules.cs`, `Plan` (lines 149-166): the push destination is not checked against `provokerCells`; the rules rely entirely on `canUnitEnter` to know the provoker stands there. For the real answer that works (the provoker is on the grid). For the hover preview it does not: `TryPlanAnswer(List<Vector2Int>, ...)` is called with the striker's predicted end tile, which is empty on the grid, so a handler `canUnitEnter` that reads the grid would let a unit be pushed onto the provoker's predicted cell, and the preview and the real answer would then disagree. The test `ProvokerBeyondAPushedUnit_DestinationBlockedByThem` hides this because the fake board lists the provoker as a unit. Fix: in `Plan`, return `DestinationBlocked` when `to` is in `provokerCells` (before calling `canUnitEnter`), and add a test where the provoker cell is not on the board. Alternative: C2 must treat `provokerCells` as occupied inside its `canUnitEnter`; if so, say it in the XML comment of `canUnitEnter`.

## Notes

- Checked against the plan: pure (only `Vector2Int`, `Mathf.Abs`, delegates; no Unity objects, no statics, so no `PlayModeStaticReset` hook needed). Rules match the decisions: cardinal single step only (`IsCardinalStep`), entered cells = new footprint cells not in the old one (leading edge, deduped), push one cell onward in the step direction, any occupant that can't be pushed or whose destination isn't free invalidates the whole step with no partial list, no chain pushes (a unit on the destination blocks), provoker overlap rejected before anything is classified.
- Tests cover every acceptance case in the plan's C1 list (free path x4 directions, one push, two pushes on the 2 x 2 edge x4 directions, next cell blocked/off-grid/unwalkable, blocker standing for Immovable/multi-cell, provoker overlap, old-footprint cells not entered or classified, bad input). They assert behavior (From/To, verdict, empty push list, lookups made), not just that code runs. Note the rules cannot tell Immovable from multi-cell from obstacle; that mapping is the handler's job in C2 and is only covered there.
- Conventions: namespaces `MISO.Core.Features.Bergsons` and `...EditorTests` match the neighbours; folders right (`Scripts/`, `Editor/`); UTF-8 BOM present. The files are CRLF, the same as `MasherCounterRules.cs` (the report says "LF"; the files are correct, the wording is wrong). No decision, plan, chunk or playtest IDs in comments, test names or strings (grepped). No `P0`. `.meta` files present for both files. Commit grouping (one commit, four files) is right.
- API fit for C2: fits. `FootprintCoords(Unit.CurrentCell)` gives the footprint; the step is the anchor-cell delta; `provokerCells` = `targetCoords`, so the real answer and the preview (predicted striker tile) can share one call. `classify` is only asked about entered cells, so the Masher's own cells need no special case. C2 points: (a) `Plan` must run per one-cell cardinal candidate, and `TryPlanAnswer` has to build those candidates itself because `ComputeTargetSelectionCells` plus `IsFootprintEmpty` (line 513) drops occupied cells; (b) the anchor-cell delta only equals the footprint shift if `FootprintCoords` is a plain translation of the anchor for the Masher's size, which is worth one assert in C2; (c) `canUnitEnter` must answer false for the Masher's own current cells (pushes run before the step), as the report says; (d) `Plan` allocates lists per call, fine for a handful of candidates but watch the per-frame preview.
- No core-systems API touched; no AI worker-thread exposure; no golden-master effect; no other branches affected (new files only, `thj/cyclone` takes them cleanly).
- Not run by me: tests (read-only review). The report claims 48 of 48 green through the Unity MCP.
