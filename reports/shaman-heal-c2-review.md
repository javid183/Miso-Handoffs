# Review: Dark Shaman heal C2 (heal pop-up and next-targets filter)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins` (C1 `2b8e4ea88`, `e81c20f59`, `2095e4eaf`).
Plan: `plans/2026-10-23-dark-shaman-heal-tech.md` C2 (D-150). Implementer report: `reports/shaman-heal-c2.md`.

**Verdict: APPROVE.** No must-fix. Two should-fixes, sent back.

## Should fix

1. **Header comment (`DamageNumberTrigger.Heal.cs` 11-13) and report wrong about the raiser.** Only compound heals (Linda–Toba via the projectile) raise `onAbilityEffectPerformedOn` from `AEffectCompound`. The Shaman heal, potion and Dom heals are bare `AEffectAttributeModifier`s: their event comes from `RuntimeAbility.OnCompletionShared` (`RuntimeAbility.cs:316-318`), only with `preset.actualTargets` on and after `AbilityPreset.Activate` finishes (`AbilityPreset.cs:368-404`). Same frame only if `minimumDuration` and `waitTimeAfterCompletion` ≤ 0, no effect stays in progress, and the coroutine chain resumes without a frame wait. All four current heal presets satisfy it (`actualTargets: 1`, timings −1); a future heal with a minimum duration or `actualTargets` off would silently lose its number.
2. **Tests cover only the arithmetic**, not what pops (noted, claimed only by an event naming this unit, cleared after a claim, dropped at frame end). Suggested: a plain tracker class with sequence tests. The next-targets fallbacks (no planner/level/faction → keep) sit in the panel lambda, untested (acceptable).

## Notes

1. **Play test must confirm:** green "+N" with the real capped gain on a Shaman heal (AI, `EventBasedAnimated`, frame 14), a potion (Self), a Dom heal and a Linda–Toba arrow. If the bare-modifier heals show nothing while Linda–Toba does, see Should fix 1. Checked: the AI turns the cell into its occupant (`FactionControllerBase.cs:566-567`); `DamageNumberTrigger` shares the GameObject with `GUnit`; `SetValue` clamps before `onValueChanged`.
2. **Exclusions hold:** safe room (trigger-overlap UnityEvent; a walk's completion names a cell); ticks, silent sets, bounds changes, self-modifiers land outside any naming event. Damage then heal in one ability pops the real rise (damage and heal numbers can overlap at the same start). A heal-revive on a deactivated unit doesn't pop.
3. **Subscriptions clean:** bus rebinds when `GlobalEventBus.Instance` changes; health listener follows each new attribute; both unbind in `OnDisable`; no leak; mid-level spawns bind on first `LateUpdate`; no statics. Damage numbers unchanged (`ShowDamage`, the `onValueDecreased` wiring and the manager untouched; class only made `partial`).
4. **Next-targets filter** correct for the binary relation model (everything not allied is Enemy; every faction allies itself): the Deer shows only if its faction isn't allied to the planner; player-allied factions hidden from a player-hostile planner. `PredictNextTargets` and `GUnit` untouched. **Hover highlight:** `GUnit.SetFutureTargetsHover` still marks the healed Claw's cell when hovering a Shaman about to heal (not the list in the criteria; a fix would touch `GUnit`, core).
5. Files match; LF, no BOM like neighbours; Unity 6 short metas; no private IDs; nothing on the core list changed. Two independent commits (FX pop-up, UI filter) in the right order; THJ's six assets, `Packages/*`, `ProjectSettings/*` left out.
6. No AI or golden-master effect.
