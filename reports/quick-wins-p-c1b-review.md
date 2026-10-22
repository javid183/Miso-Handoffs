# Review: quick wins bundle P, C1b (player input locked during the player's banner)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22.
Plan: `plans/2026-10-22-quick-wins-p-pace-tech.md` C1b (D-142, existing full input lock). Implementer report: `reports/quick-wins-p-c1b.md`.

**Verdict: APPROVE.** No must-fix or should-fix items.

## Notes

1. **No stuck lock on any path.** Complete: `OnComplete(Finish)`. HideInstant: level end (`CombatLevelRunHandler.cs:669`), level-start instant hide (`:147`) and `HUDSequence.cs:16` all go `HideHUD` → `HideInstant` → `Finish`. Replacement: the new token is added before `UpdateValues` releases the old one (no gap); an enemy banner (also after End Turn during the blue banner) releases the player lock. Destroy order doesn't matter (Unity null check on `PlayerInputController.Instance`, plain field). No new statics; locks are per instance. Nothing calls `DOTween.KillAll`/`Clear`/`DOKill`.
2. **Re-entrancy of `Finish()` in `UpdateValues`:** safe. The old callback only calls `RemoveInputLock`; the `_phaseBannerLock == bannerLock` guard leaves the new token; `Finish` clears `_onFinished` before invoking (one-shot); `Kill()` doesn't fire `OnComplete`.
3. **EnemyIntroductionController (`:93`/`:177`):** saves and restores `None` under the lock; `StartTurnWithIntroductions` then sets `All` if the turn is active (`PlayerController.cs:240-241`). Intros advance through UI/timer, not gated input. Latent: any future save/restore of `ActiveActionMode` under a lock captures `None`.
4. **Tutorials:** `ShowTutorial` is the only other lock holder; no step needs ability clicks while open. The `IsInputLocked` check in `AbilitiesBarHUDUI.cs:136` also closes an old hole (number keys worked behind an open tutorial). A tutorial at turn start sets time scale 0, so the scaled-time banner (and its lock) pauses until the tutorial closes, then finishes. Expected.
5. **Player turn start under the lock:** auto-select and the unit bar are programmatic; camera focus works (only manual movement is masked); Esc blocked for the banner's length; hover, skip and ShowStats are not gated.
6. **Reactive interrupt key (L, ATB only):** not gated (`PlayerInputController.cs:67`); in ATB it would slow the banner and hold the lock longer. Coordinator note: `PlayerController.HandleReactiveInterrupt` returns at once in FTP mode, which `main` uses, so it has no effect on `main`.
7. **End Turn during the banner:** works; the lock is released through the replacement path. THJ's call whether to block it.
8. **Housekeeping:** all three files LF; `CombatLevelUIManager.cs` keeps its BOM, the other two have none (as HEAD). No private IDs. Report matches diff. One core commit is right. Docs (`tech/core-systems.md`, `tech/combat-architecture.md`) still to update. No tests, acceptable per the plan.
