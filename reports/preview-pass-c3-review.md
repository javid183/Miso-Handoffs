# Review: preview-pass C3 (hover gate over the HUD)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **APPROVE**. Must fix: none. Should fix: none.

- Only GraphicRaycaster hits on non-WorldSpace root canvases block. Checked: info panels and barks are World Space (no flicker loop); the software cursor canvas has no raycaster; boss health bars (Level3-C1, LevelM2-C1) now block hover like the rest of the HUD. No Screen Space Camera canvases in combat.
- Clear on enter and resume on leave are correct and cheap. The click path is unaffected (OnMouseClick ignores UI and uses its own position; CommitPreviewedMovePath falls back safely). Harmless edge: up to 10 frames after a HUD element closes under a resting pointer.
- No per-frame GC; RaycastAll only on mouse move or every 10 frames. No EventSystem: gate off, as before. No static state; partial class is serialization-neutral. BOM and LF kept.
- Tests are thin (render-mode predicate only); the C9 play check (report steps 3–6) is the real verification. Watch for a full-screen invisible raycast-target panel on a screen-space canvas, which would now kill hover.
- Known gaps, out of scope: hover still runs under world-space panels where clicks are blocked; the shape-rotation path still checks any UI.
