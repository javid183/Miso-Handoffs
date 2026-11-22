# Review: duo insert, chunk C2 (`thj/duo-insert`, uncommitted on top of `9e992707f`)

Reviewer: miso-reviewer, 2026-11-22 (saved by the coordinator; the reviewer is read-only).

**Verdict: APPROVE** (two should-fix items, sent back to the implementer before the commit)

## Must fix
None.

## Should fix
1. **An inactive insert canvas takes the insert path without a card** (`UnitsCooperationHandler.Insert.cs`, `ShouldPlayInsert` / `TryGetDuoInsert`). If the spawned canvas is inactive, every partner is stored as missed and no prompt shows; Lucy silently gets ×0.7. Fix: return false (old panels path) when `!sequence.isActiveAndEnabled`, log a warning.
2. **The handler's `OnDisable` leaves the pooled QTE button under the card.** The QTE handler's 2-button pool would lose one if it outlives the controller. Fix: call `ReturnCardQteButton(_cardQteButton)` in `OnDisable` before clearing the field.

## Notes
- Non-insert path unchanged: `ShowDuoVisual` first, same camera/move-path/order/parallel; `CoopQteFactor.Raw`/`Map` match the old arithmetic exactly; the board QTE keeps the serialized profile and `UIHook`. Only new side effect: the first duo instantiates the hidden canvas (all `raycastTarget` 0, roots inactive).
- Insert path: same `ActivateFromQte`, `CoopQteMod`, same-entity spread, timeScale 1; `onSuccessfulQTE` only on success; Mark's blitz unchanged.
- timeScale: the coroutine runs on the `UnitsCooperationHandler` MonoBehaviour, so its new `OnDisable` is the right owner. QTE that can't start counts as missed (the old board path still has its pre-existing hang). Exceptions inside the card/insert are not covered (same class as the old path).
- QTE pool/profile: shallow profile copy, never written back; the button waits for unload (≤1.5 s) before returning under the QTE handler.
- Lazy canvas: child of the per-combat PlayerController; count resets per combat; no statics; only the player controller has the handler.
- Files clean: BOM/LF kept, no private IDs, prefab diff one line (the `DuoInsertSequence` component of `DuoInsertCanvas.prefab`).
- Tests cover the mapping, the profile copy, the decision, the shipped library. "Stored result reaches `ActivateFromQte`" needs Play mode (THJ's check).

## Risks beyond the checks
- **Pause during the card/insert** (pre-existing, wider window): the pause handler caches timeScale 0 and restores it on resume; if the insert ends while paused the board stays frozen. Play-check pausing mid-card; the real fix belongs in pause/timeScale ownership.
- **Skip clicks pass through** to the HUD and board (all insert graphics `raycastTarget` 0); Esc both skips and opens pause. If stray actions show, enable raycast on Dimmer/Backdrop.
- Core now references `MISO.Features.UI.DuoInsert` (precedent: QTE handler uses `MISO.Features.UI.QTE`); note in the core-systems Duos row.
- The next editor save of `PlayerController.prefab` brings back ~48 lines of default-field noise; harmless, not part of this change.
- No AI impact.

## Open point: mash spam may skip the insert
Low risk, real, especially on the 0.6 s repeat. Smallest fix if the play check shows it: an optional `InputAction ignoreAction` on `PlayInsertIE`, skip presses from that action, C2 passes the QTE profile's binding (~10 lines, mostly C1's file). Weaker option: measure the 0.3 s gate from the end of the last QTE. Changes the "any key after 0.3 s skips" criterion: THJ decides after the play check.
