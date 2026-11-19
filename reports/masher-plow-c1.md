# Report: Masher plow, C1 (pure rules and tests)

Plan: plans/2026-11-18-masher-plow-tech.md    Agent: miso-implementer (sonnet)    Branch: main
Outcome: done (C1 only; C2 not started)

## What changed

All under `miso/Assets/_Project/Features/Enemy/Masher Goblin/`. New files only, UTF-8 BOM and LF like the neighbouring `MasherCounterRules.cs` and its tests. Unity created the `.meta` files.

- `Scripts/MasherPlowRules.cs`: namespace `MISO.Core.Features.Bergsons`. Pure static class `MasherPlowRules`, no statics, no state, no Unity-object APIs (only `Vector2Int` and `Mathf.Abs`).
- `Scripts/MasherPlowRules.cs.meta`
- `Editor/MasherPlowRulesTests.cs`: namespace `MISO.Core.Features.Bergsons.EditorTests`, class `MasherPlowRulesTests`.
- `Editor/MasherPlowRulesTests.cs.meta`

### API (what C2 fills in)

```
MasherPlowRules.Plan(IReadOnlyList<Vector2Int> footprint, Vector2Int step,
    IReadOnlyList<Vector2Int> provokerCells,
    Func<Vector2Int, MasherPlowCell> classify,
    Func<int, Vector2Int, bool> canUnitEnter) -> MasherPlowPlan
MasherPlowRules.EnteredCells(footprint, step) -> List<Vector2Int>
MasherPlowRules.IsCardinalStep(step) -> bool
```

- `MasherPlowCell`: readonly struct. `Empty`, `Blocker`, `PushableUnit(int unitId)`; `Kind` is `MasherPlowCellKind { Empty, PushableUnit, Blocker }`.
- `classify` is called only for entered cells, never for cells the Masher already holds. The handler returns `Blocker` for: Immovable units, multi-cell units, planted entities, obstacles, stashed items, cells off the grid, cells the Masher cannot stand on. `PushableUnit(id)` for a single-cell non-Immovable unit. `Empty` for a free cell.
- `canUnitEnter(unitId, cell)` is asked once per pushed unit for the cell one step onward: the handler answers "on the grid, walkable for that unit, holds nothing".
- `MasherPlowPlan`: `Allowed`, `Verdict` (`Allowed`, `InvalidInput`, `ProvokerInWay`, `Blocked`, `DestinationBlocked`), `Pushes` (list of `MasherPush { UnitId, From, To }`, empty unless allowed, in footprint order), `EnteredCells` (filled whenever the input was usable).
- Invalid input (null or empty footprint, null delegate, step not exactly one axis cell) returns `InvalidInput` and looks nothing up. No exceptions.
- No chain pushes: a destination that is not free blocks the whole step; no partial push list is returned.
- Provoker overlap with any entered cell rejects the step, checked before anything is classified, even if the provoker's cell would be classified as a pushable unit.

## Tests run and results

Unity MCP `run_tests`, EditMode, filter `MISO.Core.Features.Bergsons.EditorTests.MasherPlowRulesTests` (editor open, compiled clean; console shows only pre-existing warnings, none from the new files): first run 48 of 48 passed; **after the review fix below: 51 of 51 passed** (counting TestCase rows), 1.2 s.

## Review fix applied

The reviewer's should-fix: `Plan` now returns `DestinationBlocked` when a push destination is one of `provokerCells`, checked before `canUnitEnter` is called (private helper `IsProvokerCell`; the `canUnitEnter` comment now says the rules refuse provoker cells themselves). This matters for the hover preview, where the provoker's predicted tile is empty on the grid. Three tests added: a provoker cell that is not on the fake board still blocks a push destination (and the board's `CanEnter` is asserted to say free, so the test proves the new check), the destination lookup is never asked for a provoker cell, and a provoker on a different cell leaves the push allowed.

Line endings: I kept the files as they were, UTF-8 BOM and LF. The coordinator's message said the Masher files are CRLF; they are not. `tr` byte counts show 0 CR bytes in `MasherCounterRules.cs` and `MasherCounterRulesTests.cs` (and the other Masher `.cs` files), and `git ls-files --eol` reports `i/lf w/lf attr/text eol=lf` for every Masher `.cs` (the repo `.gitattributes` forces LF). The new files therefore match their neighbours exactly; converting them to CRLF would make them differ from the neighbours and from git's normalization. (Git Bash `grep -c` can mislead here: it reported 0 for everything, so I re-checked with `tr`.)

Coverage: entered cells per direction, old-footprint cells not entered or classified, free path in four directions, one push, unit behind or beside the edge not in the way, two pushes on a 2 x 2 leading edge in each of the four directions (each to its own next cell, footprint order), destination held by a unit or an obstacle, destination off-grid, destination not walkable for that unit, one unit movable and the other not (nothing listed), blocker (Immovable / multi-cell / obstacle stand-in), entered cell off the grid, provoker overlap (single and multi-cell, and a provoker that is classified pushable), provoker beside the edge but not entered is fine, non-cardinal, zero and long steps, null and empty inputs.

The full EditMode suite was not run for this chunk (only new files were added; the plan's suite gate belongs to the end of C2).

## Acceptance criteria (the C1 share)

- [x] Pure plow rules (entered cells, push direction and destinations, validity) + tests: above.
- [ ] Everything else in the plan is C2.

## Save reset

no

## Decisions I made

- Input shape: one `classify` delegate over entered cells plus one `canUnitEnter(unitId, cell)` delegate for the push destination. Unit identity is an `int` id the handler maps back to its `GUnit` (index into a list is enough), so the rules stay free of Unity objects.
- Immovable, multi-cell and non-unit things are all just `Blocker` at the rules level; the handler decides which is which. The rules do not distinguish them.
- A returned verdict enum rather than only a bool, so tests and a later debug log can say why a candidate was skipped.
- Provoker is checked by cell overlap before classification (rules-level guard), in addition to the handler being free to classify the provoker as `Blocker`. Its cells also count as taken for push destinations (review fix).

## Needs THJ

none

## Docs to update

- none from C1 itself. C2/coordinator docs per the plan's Touches list.

## Risks and loose ends

- Findings for C2: the "destination is another entered cell or inside the new footprint" case from the design cannot occur for any footprint shifted by one cell (an entered cell plus the step lands outside the shifted footprint by construction), so the rules do not check it. The only way a destination lands on the Masher's own cells is a gapped footprint and the old footprint; the grid lookup in `canUnitEnter` should answer false there since the Masher still stands on its cells when the pushes run (they run before the step).
- `Plan` allocates lists; it is called from the counter planner and the hover preview on the main thread, not the AI worker. Fine at that frequency, noted in case the preview calls it per candidate per frame.
- Not verified: how `TryPlanAnswer` will obtain one-cell cardinal candidates (the walk's cell list may drop occupied cells); that is C2 step 1.
- Pre-existing and untouched: the new-file `.meta` files were generated by Unity as expected; nothing else in the folder changed.

## Proposed commits

1. `feat(masher): pure rules for the counter step plowing through units, with tests`: `Scripts/MasherPlowRules.cs`, `Scripts/MasherPlowRules.cs.meta`, `Editor/MasherPlowRulesTests.cs`, `Editor/MasherPlowRulesTests.cs.meta` (plain; new files, no behavior change).

## Other branches

none for C1 (new files; `thj/cyclone` merges them cleanly).

## How to see it

1. Unity > Window > General > Test Runner > EditMode, search `MasherPlowRulesTests`, Run: 51 green.
2. Nothing visible in the game yet: the handler does not call the rules until C2.
