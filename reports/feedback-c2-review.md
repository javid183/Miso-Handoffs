# Review: feedback pass C2 (kill feedback)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22. Branch `thj/quick-wins` (C1 `07f4e44fe`).
Plan: `plans/2026-10-22-feedback-pass-tech.md` C2 (D-146). Implementer report: `reports/feedback-c2.md`.

**Verdict: APPROVE.** No must-fix.

## Should fix (sent back to the implementer)

1. `KillFeedbackPresenter.Flash`: the default colour was read from `visual.sharedMaterial` before `DOTween.Kill(mat)`. After any blink, `sharedMaterial` returns the per-unit instance, so a death raised mid-blink (e.g. Dom's `FakeDie` from `BossDomFight.OnDamaged` running before `PlayHit`, within a previous hit's 0.2 s blink) would fade back to the tint and stay tinted. The common path is fine (`onValueDecreased` → blink resets the default before `onMinReached` → `unitDied`). Fix: get `mat`, `DOTween.Kill(mat)`, then read the default from `mat`; keep the `HasProperty` guard. No `GUnit` change.

## Notes

- **Flash:** `GetMainVisual()` is `bodyVisual` (`GUnit.cs:845-847`), the same instance `PlayHitBlink` tweens. DOTween's `Material.DOColor` sets the material as target, so `DOTween.Kill(mat)` stops the blink and runs its `OnKill`. Nothing else tweens unit body materials. `.material` only instances for units whose blink never ran (same instancing the blink does). `SetLink` = KillOnDestroy; deactivation doesn't stop the tween; destroy is guarded.
- **Bus:** the `Update` re-bind matches `RoleZonePresenter`; `GlobalEventBus.Instance` is cleared by `ResetPlayModeState`; never doubled (old listener removed via `ReferenceEquals`); chain resets on re-bind.
- **Rules and tests:** 0,1,2,2; chain end exclusive; restart; one sting per chain. An area kill shares one `Time.time` and steps 0→1→2. `FakeDie` gets the beat; player faction excluded.
- **Also get the full beat (judge in play):** each Dark Worm split (`DarkWormPassiveAbility.cs:378` → `DiePermanently(.7f)`); reverting an ability that spawned a non-player unit (`AGUnitSpawner.cs:39`); units in factions allied to the player but not the player faction.
- **Assets:** identical to `UnitHit_ShakeCameraEffect.asset` except name, `duration 0.25`, magnitude 0.05/0.06/0.07, `priority 1`. Hand-written NativeFormatImporter metas, well formed.
- **Scenes:** only the new objects under `---Management---` (+53 each), unique fileIDs, fields wired; `A_SFX_John_ShieldImpact` exists (`Resources/Audio/AudioStorage.asset:121`).
- **Conventions:** namespace `MISO.Features.Effects.KillFeedback`; `Editor/` tests in `Assembly-CSharp-Editor`; LF, no BOM like neighbours; no statics; no private IDs. One commit; leave out `Packages/*`, `ProjectSettings/*`.
- **Play test:** the white over the blink; enemy-turn pace.
