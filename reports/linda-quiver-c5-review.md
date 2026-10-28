# Review: Linda's Quiver C5 (combat log lines), 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: FIX** (the implementer has applied the fixes; re-review pending)

## Must fix
1. A baked Linda's "starts with N/4" line can run before the log opens its level, so it is dropped. Write it on the first `turnStarted`.
2. Commit units 2 and 3 must merge, because `LindaQuiver` adds the listener.

## Should fix
3. Drop `QuiverLogListener.Update`, the per-frame check, and rebind lazily.
4. Shot naming by "most recently started ability" is wrong for Duos and isn't filtered by owner. Use `_projectile.StatAttributesContext as RuntimeAbility` and pass it through `Spend`.
5. Use neutral text in the Core `CombatLogTests` case.

## Notes
- No Core file imports Features. `AddCustom` is additive and generic.
- The Watch prompt line logs the count before the spend, which is right.
- The hand-written metas: stage them after Unity recompiles.
- The plan's `CombatLog.Quiver.cs` is really a generic `AddCustom` in Core plus the listener in Features.

---

# Re-review after fixes

**Verdict: APPROVE.**

- The StatAttributesContext route is confirmed for the bow, Watch (its role ability) and Linda's Duo part.
- All five fixes are correct, and there are no compile risks.
- Commit order: Core `AddCustom` first, then the merged quiver commit. Stage the metas after Unity recompiles.
