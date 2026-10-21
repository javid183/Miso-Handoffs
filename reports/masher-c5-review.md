# masher-c5 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **FIX**

Must fix
1. `MasherGoblinFactionRoleHandler.Preview.cs:123-130`: a striker that walks or dashes in alone shows no damage (it isn't in the cross on today's grid; the fallback borrows another unit's number, and there may be none). Fix: when `answeredEnd != answered.CurrentCell` and the striker isn't in `damage`, compute from its own HP with the public `AbilityDamagePreview.ComputeDamage(ability, hp.Value)`, then `hp.NormalizeValueChange(...)`, clamp at 0; drop the borrow path. Still approximate: the striker's own tag mods and guaranteed resists (`AddDamage` is private; an exact public entry would be a core change for THJ).

Should fix
1. `MasherGoblinFactionRoleHandler.cs:42`: `OnDisable` must also call `ClearReactionPreview()`.
2. `Preview.cs:157`: dash landing resolved against the 2 × 2 anchor, not the clicked footprint tile; document it as a D-105 approximation (or track `gridCellHovered`).
3. `MasherGoblinFactionRoleHandler.cs:1-12`: trim unused usings.

Notes: Commit A (`PlayerController.cs`) is visibility only, clean. The `TryPlanAnswer` overlap skip is a no-op for the real answer (live targets' cells are occupied, `IsFootprintEmpty` already rejects them). Preview follows the real plan (gate removed, end-tile order, slam only when adjacent, PickAttackCell with the counter ability, Crippled, lethal check, Duo pick). No new subscriptions or statics; LF/no BOM as HEAD; commits ordered A → B; Packages/ProjectSettings excluded. core-systems.md: note the two PlayerController methods are public (D-105).

## Re-review after revision 1 (2026-10-20)

Verdict: **APPROVE**. Striker damage from its own HP (`Preview.cs:125-137`, normalize then clamp, approximation commented, borrow path gone, `AbilityDamagePreview` untouched); `OnDisable` clears the preview; 2 × 2 dash comment present; trimmed usings unused; commits A then B clean, Packages/ProjectSettings excluded.
