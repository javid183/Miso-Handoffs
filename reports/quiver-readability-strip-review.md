# Review: quiver readability strip-down, 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: APPROVE**

**Checked:**
- No compile risk found.
- No dangling references to the deleted scripts.
- Unique GUIDs, and the art references match THJ's sprites.
- Every plan item is covered.
- Board arrows draw under the pips and HP bars.
- No per-frame allocations, and no core change.

**Should fix (sent to the implementer):**
- The comment on the HUD quiver's placement doesn't match the code.
- An unused `using`.

**Commit units: the report's order doesn't build.** Use these instead:
- A: THJ's art.
- B: the whole code strip and new look, one unit.
- C: `Unit_Linda.prefab` with the `Linda_QuiverHasItsDrawnArt` hunk of `QuiverWiringTests.cs` (or folded into B).
- D: the kinematic bodies on the 5 arrow prefabs with the `ArrowPrefab_HasAnAwakeKinematicBody` hunk. Independent.

`QuiverWiringTests.cs` has exactly two hunks, one per test.

**Orphans:** `IMovePreviewPathSource` and the `PlayerController` hook (D-270) now have no reader. That's a candidate core revert, which needs THJ's OK. The `core-systems.md` row about it is stale.

**Things to check in play:**
- Arrows draw over unit bodies.
- The panel arrows stand 55 px above the quiver; check nothing clips them.
- The quiver placement.
