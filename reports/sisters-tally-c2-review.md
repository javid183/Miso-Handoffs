# Sisters' tally C1 fixes + C2: review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. One should-fix.

## Should fix

1. `Features/Onboarding/SistersTally/Editor/SistersTallyCounterTests.cs:86` (asserts 105-112): `Component_FollowsTheTally_AndAThrowFreeUpdateReachesLaterListeners` doesn't test the counter's try/catch (`SistersTallyCounterUI.OnTallyChanged` 131-135); deleting it still passes. Rename to what it checks (e.g. `Component_FollowsTheTally_AndStopsAfterDisable`) and drop "throw-free" from the `later` assert message.

## C1 should-fixes

All three done: `Run` removed; `OnLevelEnded` comment plain (`SistersTallyListener.cs:74-77`); `SistersTally.IsAtMinimum` (`SistersTally.cs:79`) used by `SistersTallySource.DiedFromDamage` (52) with at/below/non-zero-min/above tests; the switch-off test can now fail.

## Notes

- Core hook: `CombatLevelUIManager.cs` diff = one tooltip + field (59-60) and start + guarded yield in `HideHUD`/`ShowHUD` (167/173, 183/189), same pattern as the other panels. Empty field = no change (also in `DevScenes/SampleScene*.unity`, `TestLevel.unity`). BOM + LF kept. Commit 2 compiles alone.
- `HudPanelBase` is a second Core file beyond D-447's wording; acceptable and near minimal (typing the field as the onboarding type couples Core to it; interfaces don't serialize; `UIPanelAnimator` would lose the HUD-shown state `ShowAlone`/`FadeOut` need). Abstract, two methods, no state. Tell THJ when showing commit 2; add to `tech/core-systems.md`.
- Counter: slide (`UIPanelAnimator`) and alpha (`CanvasGroup`) are separate layers; `ShowHUD`, the dev HUD toggle, `HideHUD` while shown alone, and `ShowHUD` during `FadeOut` don't fight. No statics. `Find()` fine for one-off calls only. Level start's `HideHUD(instant)` corrects the initial `_hudShown`.
- **C4 risk:** `FadeOut` uses DOTween in scaled time; if the pile outro runs with `Time.timeScale` 0 the step waits forever. Check in C4's play test.
- Scene: only the counter root + 3 children, `extraHudPanel` wired, one Canvas child entry. 58 "deleted" lines are the `LowHealthFeedback` block moved by Unity's save, byte-identical (noise, goes in commit 3). Script GUIDs match. Counter is after `ObjectivesPanel`, before dialogue UI. Menu item idempotent; caveat: it saves any unsaved edits in an open container scene.
- Report wording slips (harmless): the manager GameObject is `GameSessionUIManager`, component `CombatLevelUIManager`; visibility tags are `All`, not "Generic".
- Three-commit split right; `.meta` files grouped correctly. No private IDs.

Not verified: EditMode not re-run by the reviewer (report: 1657/1658, known AI red only); not played.
