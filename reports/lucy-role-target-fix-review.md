# Review: Lucy role wrong-target fix (F1 core attacker memory, F2 Lucy ranking)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-23. Branch `thj/quick-wins`.
Plan: `plans/2026-10-23-lucy-role-target-fix.md` (D-152). Implementer report: `reports/lucy-role-target-fix.md`.

**Verdict: APPROVE.** No must-fix. Three should-fixes; the coordinator sent back #1 (which settles #2 and #3): the fallback uses this action's actual victims via `onAbilityEffectPerformedOn`.

## Should fix

1. **The fallback could still pick an enemy this action never touched** (`LucyFactionRoleHandler.cs:93`, `GetMostRecentAttacker() == lastOwner` means "the acting unit hit it last, at any time"). Case: Linda shot C last turn; now her Bow kills B next to C; B is gone, C at distance 1 qualifies. Fix without core: collect units hit by the current action from the public `GlobalEventBus.onAbilityEffectPerformedOn` (as `MasherGoblinFactionRoleHandler.Counter.cs:77/87` does), reset per action (`RuntimeAbility` instances are reused).
2. **Fallback distance used Lucy's Adjacent metric**, so a Radial compound's diagonal victims (Manhattan 2) fall outside radius 1 (only `Linda_Ability_HarmonicSlam_CompundEffect` is Radial).
3. **Harmonic Slam probably stopped triggering Lucy via the fallback:** cell-targeted, Linda moves with `AEffectTransporter`, damage from on-start-tile spawned entities; measured area 0 → radius 1 from the landing cell. Not in Lucy's blacklist (`Unit_Lucy.prefab:2827`).

## Notes

- **F1 core, AI thread:** one private lock per operation, no nesting or callbacks inside: correct, no deadlock; main-thread writes wait only a tiny critical section. `GetRecentAttackFactor` no longer allocates (old per-call `ToList()` gone). No new Unity-object API on the worker path (correction: `GlobalSettingsSO.Instance` does a `UnityEngine.Object` bool check and lazy load; pre-existing, harmless once loaded). Same formula, now correct meaning: an enemy that keeps hitting an AI unit always scores `fade^0` on `TargetRecentAttackFactor` (steadier revenge targeting): an **AI behaviour change** for THJ to know (golden master still 38/709). API unchanged; `RememberAttack` untouched; `BarkManager.cs:164` instigator now truly newest. No statics; size from `unitsAttackMemorySize`; size 0 remembers nothing as before.
- **F2:** matched the plan. Knockback +1 sound for current assets (Vault `EndDamageCompound` Adjacent radius 1 + push 1 = 2, as `fc4a7dad0`; only John and Dom have other pushers; Linda's Bow and Explosive Arrow stay 1). Lucy's preset Adjacent. The radius-4 zone check (`4f27914d0`) untouched. Explosive Arrow is cell-targeted.
- **Tests (25):** memory tests are real behaviour; ranking tests cover the rules; `MeasureActionArea` untested (Unity assets).
- **Housekeeping:** no private IDs; LF; BOM on the Core files like `GUnit.cs`, none on the Lucy files like neighbours; folder metas present; split F1 then F2 each compiles alone. `FactionRoleRules.FirstMatchAcrossGroups` now has no runtime caller (harmless). Update `core-systems.md` (Units/GUnit) after commit. Secondary suspect (`LastActions[0]` oldest entry) still open, out of scope.
