# Review: Bond Lite fix C4, Yard staging (2026-11-08)

Reviewer verdict: **APPROVE**, no must-fix or should-fix. Read from the code; framing checked by the implementer in Play only. Coordinator's condensed copy.

- `Initialize()` twice is safe: `SetInputs()` guarded by `_inputsSet`, `SetZoom` stops the previous coroutine, no tweens; input mode None during the opening so the pan isn't fought. The second call (`HomeManager.StartIE:159`) snaps back about 34 units: THJ's call (keep the cut or pan back).
- Reached only via The Trail's `completionSequence` in Home's opening; no camera in payload: warns and ends. In another scene `Initialize()` would snap that camera; class doc limits it to Home (note in `tech/home-system.md`).
- Skip: `FocusInstant`, never left mid-pan. Limit: `SequentialSequence` fast-forward only starts on dialog or `CameraSequence` steps, so a hold during the pan only snaps the camera; one-hold skip would need shared `SequentialSequence`.
- The Trail's Home state shows from The Trail's win until M4 is won; Hearth, River, Ridge keep Searching. 7 Searching idles with `LucyTraining` and `LindaHair` (offset 17, -5.5). Classic unaffected.
- Order and text match D-436, D-439 (test guards no on-screen "Family point"). Bond step unchanged, once only.
- No statics, LF, no private IDs; two commits: step alone, then wiring + data + tests.
