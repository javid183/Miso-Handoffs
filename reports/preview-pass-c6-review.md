# Review: preview-pass C6 (focus, P5 hide, tooltip, C4 should-fixes)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **APPROVE**. Must fix: none.

Should fix (folded into C7):
1. `UnitPanelUI.RoleBadge.cs:78`: the D-080 tooltip line is gated only on `state != None`, so an enemy with a role badge (Masher Goblin, `showRoleZone` defaults true) could get "Shift shows them" though Shift never draws enemy zones. Guard to player-faction units, ideally inside `RoleZoneAttackMatch.ZoneEqualsBasicAttack(GUnit)` so presenter and tooltip keep one check.
2. `RoleZoneAttackMatch.cs:61-62`: the empty checks run before the footprint is removed; if both sets are only the footprint, two empty sets compare equal and the zone hides. Return false when the zone minus the footprint is empty.

Notes: Shift no longer narrows; focus = badge hover, else the Shift-hovered shown zone; scale additive across the core partial, layer set and slot fit, clamped inside the quadrant; alpha via the entry colour; hide only without Shift, only for the selected unit, from `CurrentCell`; presenter and tooltip share one check. Leaving the unit's own tiles out of the equality is correct and safe (only the footprint is removed from both sides; any other difference breaks equality); THJ should hear about it; C9 must confirm the hide fires for Linda and Lucy. No statics, encoding kept, the 4-commit split compiles in order. The report's test count is 27, not 28.
