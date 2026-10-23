# Review: feedback pass C5 (HUD glow, portrait tint, item-pouch bob)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins` (C4 `31b8473d7`).
Plan: `plans/2026-10-22-feedback-pass-tech.md` C5 (D-146 to D-148). Implementer report: `reports/feedback-c5.md`.

**Verdict: APPROVE.** No must-fix. Two should-fixes, sent back to the implementer. In scope, no core systems or AI-read code; LF, BOM on the test like its neighbours, no new statics, no private IDs; one commit.

## Should fix

1. **`UnitPanelUI.LowHealth.cs` ~121-122:** `SetLowHealthShown(false)` toggled the glow/tint children with `SetActive`, reachable from the panel's `OnDisable` (RoleBadge partial) during the parent's deactivation (level exit or scene unload with a low member shown): Unity can log "GameObject is already being activated or deactivated". Fix: children created active once; toggle the `Image` components' `enabled`.
2. **`LowHealthPresenter.cs` ~122:** the Effects presenter depended on the HUD helper `LowHealthHudRules.BeatStrength` for one clamped division. Fix: move it (and its two tests) into C4's `LowHealthRules`.

## Answers

1. **Selection tracking:** `SetupLowHealth` releases first (no double subscription); `Hide`, `OnDisable`, `OnDestroy` release. Death/heal clear via the bar's `OnDisable` → `ClearLowHealth`; dead is not low. A destroyed bar nulls its own event. Deevoted and decoys: bars inactive → not low.
2. **Generated objects:** built once, destroyed with the panel; textures and sprites destroyed in `DisposeLowHealth`; raycasts off; `ignoreLayout`. `SetAsFirstSibling` safe (`UI_Element_FillBar` doesn't use child indices). `CharacterHUD.prefab` has no `RectMask2D` and one `Mask`.
3. **`BeatStrength`:** one field written in `Update`, zeroed in `OnDisable`; C4 unchanged; negligible cost; no presenter → steady alpha.
4. **Pouch bob:** `Populate` → `Clear` ends the bob and restores scale. Healing check = hover preview's (`ItemEffectPreview.GetHealthIncrease`, same `IsHidden` filter). `PausableStep` stops at timeScale 0.
5. **Hooks** minimal; `ForgetLowHealthSelection` runs before `Hide`'s coroutines; `Hide(disableObjectAfter: true)` already cleared, so `OnDisable` returns early.

## Notes for THJ's play check

- **Tint shape:** `UnitAvatar` has no `Mask`, so the tint covers the whole rect; a transparent portrait background would show a red gradient box.
- **Glow** reaches 10 canvas units past the bar and can overlap neighbouring HUD elements. Ring width assumes `referencePixelsPerUnit` 100.
- **Stale presenter reference** only refreshes when the glow goes hidden → shown (harmless unless presenter and panel live in different scenes).
- **Bob** plays while the panel slides in; re-selecting the same low member after another bobs again (intended).
- Tests cover the pure rules; the panel/pouch wiring relies on the play check.
