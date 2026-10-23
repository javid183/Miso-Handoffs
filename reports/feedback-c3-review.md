# Review: feedback pass C3 (mini HP bar and damage chip)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22. Branch `thj/quick-wins` (C1 `07f4e44fe`, C2 `8d531ec64`).
Plan: `plans/2026-10-22-feedback-pass-tech.md` C3 (D-146). Implementer report: `reports/feedback-c3.md`.

**Verdict: APPROVE.** No must-fix. Two should-fixes, sent back to the implementer.

## Should fix

1. **Line endings:** the three new `.cs` files under `Features/UI/Panels/Scripts/MiniHealthBar/` were CRLF; every `.cs` in that folder is LF and `.gitattributes` has `*.cs text eol=lf` (the report's "neighbours are CRLF" was wrong). Convert to LF; BOM on the test file only.
2. **`UnitMiniHealthBar.OnHealthChanged` (~187-188):** `ChipTopOnHit` used `_chipShown`, which only updates while the bar is visible; a second hit while the info panel is up restarted the chip from a stale top. Compute the drawn value at `now` with `ChipValueAt` first.

## Notes

- **Prefab:** `UnitBase.prefab` +381/−0: new objects and one `m_Children` entry on `UnitInfoHook`; `hitEffects`, `onMinReached` untouched; unique fileIDs; references resolve (`unit`, `infoPanel` → stripped `EntityInfoPanelUI`, canvas, frame, fill, chip); sorting layer Overlay. Both override hunks target the new `MiniHealthBar` GameObject; both variants source `UnitBase` directly. Prefabs LF.
- **HP subscription:** `Bind` unbinds first; `OnDisable`/`OnDestroy` unbind; binds once the attribute exists (`LateUpdate` `ReferenceEquals`) and rebinds after re-`Initialize`. `SetValue` updates before `onValueChanged`. Death with deactivate unbinds; `Resurrect` shows on the next `LateUpdate`; `FakeDie`/`DieRevivable` hide via `IsAlive`. Summons follow the same path. No leak.
- **Visibility:** `Show`/`Hide` are synchronous; normally no frame with both. A panel `Show` after this `LateUpdate` (another `LateUpdate` or `WaitForEndOfFrame`) could overlap one frame: watch in play. Only Deevoted and `Lucy_Decoy_ValidVariant` lack the info panel reference; all 17 `UnitBase` variants otherwise keep it.
- **Chip rules:** sound (start, drain ≤ 0, heal past the top, max-HP and silent changes caught up without a chip, pauses at timeScale 0). 18 tests exercise the real rules.
- **Layout and cost:** one world-space Canvas per unit (~20 a level), no raycaster/scaler/layout groups; `anchorMax` written only on change and during the 0.4 s chip; no per-frame allocations. Width divides by `lossyScale`. Dark Claw's 0.85 visual scale shrinks its bar the same as its panel. Facing uses `flipX`, so the fill never mirrors.
- **Sorting:** on Overlay, so the bar draws over a neighbouring unit's sprite, as the info panel does. Check in play.
- **Conventions:** namespaces `MISO.Content.UI` / `.EditorTests`; `Editor/` folder; no stateful statics; no private IDs; one commit.
- **Loose ends:** Unity's pending serializer fields on `UnitBase.prefab` and `Deevoted.prefab` (removed by hand) come back on the next save of those prefabs: harmless noise. Side colours: THJ's call before C4.
