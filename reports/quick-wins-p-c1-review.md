# Review: quick wins bundle P, C1 (non-blocking phase banner)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22.
Plan: `plans/2026-10-22-quick-wins-p-pace-tech.md` (D-141). Implementer report: `reports/quick-wins-p-c1.md`.

**Verdict: APPROVE.** No must-fix items.

## Should fix

1. **The banner swallows grid clicks during the player's turn.** `PhaseVisuals.prefab` Images/TMP have `m_RaycastTarget: 1` (lines 153, 275, 401, 787, 924, 1061, 1200, 1288, 1364). `PlayerController.OnMouseClick` (`PlayerController.cs:278`) and the hover preview (`:159`) return early on `EventSystem.current.IsPointerOverGameObject()`. Before C1 the player had no input while the banner showed; now `StartTurn()` runs in the same frame, so clicks and hovers under the banner are eaten for ~3 s (≈1 s after C3). Fix, data only: a CanvasGroup with `blocksRaycasts = false` on the PhaseVisuals root, or Raycast Target off on its graphics. **Folded into C3** by the coordinator.
2. **A HUD-hiding sequence at turn start now cuts the banner at once.** `HideHUD` (which now calls `HideInstant`) is called at level start (`CombatLevelRunHandler.cs:147`, instant, harmless), `EndLevel` (`:669`, intended) and `HUDSequence` (`Core/Levels/Runtime/HUDSequence.cs:16`). A turn-start sequence that hides the HUD removes the banner, and `ShowHUD` doesn't replay it. Arguably right ("a cutscene hides the banner"). Play-check it; if THJ wants the banner kept, move `HideInstant` from `HideHUD` to the `EndLevel` path.

## Answers

1. **Turn flow.** Nothing depends on the banner having finished. `animationFinished` is read only by the `ShowPhaseAnimation` wrapper (now without callers); nothing else references `PhaseVisualsUI`. `StartTurn()` → `UpdatePhaseVisuals` Shows/Hides the End Turn panel a second time in the same frame, as before C1; harmless (`UIPanelAnimator` kills and restarts the tween). End Turn clicks during the enemy turn do nothing (`TrySwitchTurn` returns when `CurrentFactionController != caller`); interactability comes from `NotifyStateChange`. C1 also closes an old window where `SessionLogs.CurrentPhaseFaction` kept the player faction for the whole banner.
2. **Stale `UIPanelAnimator.Visible`.** Can be wrong: Show/Hide coroutines wait on the shared `tween` field, so back-to-back Hide then Show wake together and write `Visible` in resume order. Only reader: `Core/_Dev_/Runtime/HUDVisibilityToggle.cs:37` (dev toggle key). No gameplay bug. Minimal fix if wanted (outside C1, `Core/UI/Runtime/UIPanelAnimator.cs`): keep the local tween, wait on it, write `Visible` only if `tween == t`. Backlog at most.
3. **`PhaseVisualsUI`.** Correct: `KillSequence` guarded by `IsActive()` and clears the field (`defaultRecyclable: 0`); `HideInstant` null-guarded before `Awake`; a mid-banner `HideInstant` ends `ShowPhaseAnimation`'s wait; `OnDestroy` kills the sequence. Ease: the old code put `ease` on the whole sequence and left the slide-out on DOTween's default; now both slides use `ease` and the sequence is linear (feel differs slightly). Pre-existing: `PlaySequence` would throw before `Awake` on an inactive object.
4. **Line endings/BOM** unchanged: all LF; `CombatLevelRunHandler.cs` and `CombatLevelUIManager.cs` keep their BOM; `PhaseVisualsUI.cs` has none.

## Notes

File list matches the diff; one core commit is right (the three files depend on each other). No statics, AI-thread code, serialized-field changes or private IDs. Docs (`core-systems.md`, `combat-architecture.md`) are the coordinator's.
