# Report: Preview pass C3, hover gate over the HUD

Plan: plans/2026-10-19-preview-pass-tech.md (C3; design G1, P1)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (code, compile, EditMode suite); the in-game behaviour needs the play check

## What changed

- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridManager.cs` (core): class made `partial`; `HandleHovering` first asks `IsPointerOverScreenSpaceUI()`. If the pointer is over the HUD it calls `ClearLastHoveredCell()` and returns, so nothing gets hovered. +8/-1 lines; BOM and LF kept.
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridManager.HoverGate.cs` (+ `.meta`, new, core partial): `IsPointerOverScreenSpaceUI()` runs `EventSystem.current.RaycastAll` at the pointer. It counts a hit only when `result.module` is a `GraphicRaycaster` whose canvas has a root canvas in Screen Space Overlay or Screen Space Camera mode. The new pure predicate `public static bool BlocksGridHover(RenderMode rootCanvasRenderMode)` makes that call. The raycast runs only when the mouse moved, or every 10 frames while it rests (see Decisions). All state is instance fields, so there are no new statics.
- `miso/Assets/_Project/Core/Systems/GridSystem/Editor/GridHoverGateTests.cs` (+ `.meta`, new): 3 EditMode tests of `BlocksGridHover` (Overlay and Camera block, WorldSpace doesn't).

PlayerController.cs is untouched (the C2 change is still uncommitted there).

## Acceptance criteria

- [x] `HandleHovering` hovers no cell while the pointer is over a raycast-target UI element on a Screen Space Overlay or Camera canvas, and World Space canvases don't block it. Code done; the canvas-mode decision has a test (`GridHoverGateTests`, 3/3 pass). The real HUD and world-space panels in a level still need the play check.
- [x] Entering the HUD clears the last hovered cell. The gate calls `ClearLastHoveredCell()`, which sends `gridCellHovered(cell,false)` and `gridCellEntityHovered(entity,false)`, and every preview listener tears down on those. Normal hover resumes on the first frame the pointer is off the HUD, because `_lastHoveredCell` is null by then and the cell under the pointer differs. This needs the play check (the ghost, follow zone and Shift preview should go away).
- [x] Clicks on the grid are unchanged; only hover is gated. Checked in the code; details below. Play check.

### Click path (checked, no change)

- `PlayerController.OnMouseClick` (L243-253) already returns on `EventSystem.current.IsPointerOverGameObject()` (any UI, world-space panels included). Otherwise it takes the cell from the click's mouse position, not from the hovered cell. A click on a HUD button never selected a grid cell before this change either, so nothing changes there.
- The one place a click uses hover state is `CommitPreviewedMovePath` (L1262-1271). It uses `_previewPath` only when that path ends at the clicked cell. A click that reaches the grid means the pointer is not over any UI, so the gate is open there and hover runs as before. The previewed path is the same as before.
- Over a world-space panel, hover still runs (not gated), and clicks are still blocked by the existing `IsPointerOverGameObject`. Both as before.
- What does change: the hover side effects of the pointer over the HUD (ghost, path preview, sword icons, follow zone, unit hover panels via `gridCellEntityHovered`, duo cell previews, `MovePreviewCoverPresenter`) no longer fire. That is the intended G1 change. A click on the grid right after leaving the HUD still works, because hover resumes in the same frame the pointer is off the HUD.

## Save reset

No.

## Decisions I made

- New partial file instead of growing `GridManager.cs`, so the core diff stays at 8 lines. The two files only work together, so they go in one commit.
- The raycast runs when the mouse moved, and also every 10 frames while it is still. Behaviour is the same as raycasting every frame, except that UI opening or closing under a resting pointer is picked up within about 10 frames. Raycasting only on mouse move would leave the board stuck un-hovered after a HUD element under a still pointer closes. `CursorSituationDriver` already raycasts every frame, so the cost is small either way.
- The canvas check uses `GetComponent<Canvas>()` on the hit's `GraphicRaycaster`, then `rootCanvas`, so nested canvases follow their root's mode. Physics and other raycasters are ignored. There is no UI Toolkit runtime UI in `_Project` (no `UIDocument`/`PanelSettings`), so `GraphicRaycaster` covers the HUD.
- Mouse position comes from `PlayerInputController.GetMousePosition()` (new Input System `Mouse.current`), the same source the grid hover itself uses.
- `BlocksGridHover` is `public static` (pure, no state) because the test assembly (`Assembly-CSharp-Editor`) can't see `internal` members.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md`: grid hover is gated by screen-space UI (`GridManager.HoverGate.cs`); world-space canvases don't gate it; clicks keep their own `IsPointerOverGameObject` check.

## Risks and loose ends

- A world-space panel blocks clicks (existing `IsPointerOverGameObject`) but not hover. That is not new, but after this change it's the only UI that keeps hover alive under the pointer. Unchanged on purpose (plan risk: "a dead board under world-space panels").
- A large invisible raycast-target Graphic on a screen-space canvas (for example a full-screen blocker panel left active) would now also stop hover. The existing click block already treats such panels as UI, so clicks would have died there too. Worth watching in the play check.
- The shape-rotation path in `PlayerController` (L159) still uses `IsPointerOverGameObject` (any UI). It's consistent with the click path and outside C3.
- Not touched: `AIRegressionTest` (still the known red).

## Proposed commits

1. `fix(grid): stop grid hover while the pointer is over the HUD`: `GridManager.cs`, `GridManager.HoverGate.cs`, `GridManager.HoverGate.cs.meta`, `Editor/GridHoverGateTests.cs`, `Editor/GridHoverGateTests.cs.meta` (core, own commit). The tests are three one-liners on the same predicate, so they ride with it. Split them into `test(grid): edit-mode tests for the HUD hover gate` if THJ prefers.

Not in the commit: `PlayerController.cs` (C2, under review) and the pre-existing `Packages/` and `ProjectSettings/` changes.

## Test run

Unity MCP, editor open, no Play mode. Refresh and compile clean (no errors; only the usual warnings). Full EditMode suite: 202 tests, 201 passed, 1 failed, the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. `GridHoverGateTests`: 3/3 passed.

## Other branches

None (merges to `main` with the rest of the branch).

## How to see it

1. Open a level with the HUD (for example from PreloadScreen with the toolbar level picker) and enter Play.
2. Select John and hover a board cell: the ghost, path, sword icons and follow zone show.
3. Move the pointer straight from that cell onto a HUD element that sits over the board (unit panel, role badge, ability bar). The ghost, follow zone and hover highlight should disappear, and no cell under the HUD should light up.
4. Move back onto the board: hover resumes on the cell under the pointer. Click a cell right next to the HUD edge: the move or selection works as before.
5. Hover an enemy's world-space info panel or a bark over the board: the cell under it still hovers.
6. With Shift held, repeat step 3: the Shift preview of the hovered unit clears over the HUD.
7. P1 repro (design P1): hover John's badge over the board and over empty screen; the tiles should now match in both cases. The badge's own sword icons are C4's job.
