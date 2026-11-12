# EditMode after merging thj/after-hearth into main (b1f9d1f68), 2026-11-11

Command line, editor closed. 1887 tests: 1867 passed, 20 failed. Results: scratchpad `merge-results.xml`.

## Failures
- Known red: `AIRegressionTest.Baseline_MatchesCurrentAI`.
- **13: teammate's hand-edited dialogue vs the onboarding wiring and its tests.** The teammate's commits on origin/main (`ef56cbb07`, `819faab4d`, `05b1eebc4`, `00a389b90`) rewrote dialogue assets in Unity: new texts, speakers, node order; `Narrator` → `TopNotification`; a Hearth close speaker now `Textbox`. The wiring (`HearthMemoryWiring.*`, `SearchWiring.River/Ridge`, the Home visits builder) still generates the old lines and the tests assert them. Tests: HearthMemoryJohnTests ×2, HearthMemoryLindaTests ×2, HearthMemoryLucyTests ×2, HearthMemoryMarkTests ×2, HomeVisitsTests ×2 (Hearth close, Yard chain), SearchRidgeTests ×1, SearchRiverTests ×2. **Running those wiring menus now would overwrite the teammate's dialogue.**
- **3: teammate's new `HomeMemoryOpeningTests`** throw "This can only be used during play mode" (`HomeMemoryOpeningTests.cs:29`: a play-mode scene API in an edit-mode test). Broken on origin/main itself.
- **3: GridToLevel** (`CameraStart`, `Facing`, `Settings`): unhandled Unity log `Assertion failed on expression: 'm_LockCount == 0'`. Neither side changed these tests; likely batch-mode / asset-lock noise or a side effect of the teammate's scene changes. To re-run in the editor.

None of the 19 comes from the Trail work.
