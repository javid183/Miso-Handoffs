# Review: preview-pass C4 (role badge hover drives the role-zone layer)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **APPROVE**. Must fix: none.

Should fix (folded into C6, which touches the same files):
1. `UnitPanelUI.cs` lines 3-4, 11: `using MISO.Core.Systems.GridSystem;` (and possibly `System.Collections.Generic`) now unused.
2. `RoleZoneBadgeHoverTests.cs` line 79 `AfterExit_BackToSelectedOnly_AndNoFocus`: the first `Show(...)` has no effect (stateless rule); drop it or rename the test.

Checks passed: bus event additive (one field, D-068 pattern); badge no longer writes `SetInAttackRange` (also removes a possible NRE); every hovered=true gets exactly one false (exit, Hide, unit change, OnDisable, OnDestroy; late exits are no-ops); presenter subscribes through `Rebind` (scene reload safe); cleared on unit death and level end; old `OwnersToShow` overload unchanged (pinned by a test); no statics; BOM/LF kept; the two-commit split compiles.

Notes for C9: a brief zone can flash during the panel's 0.5 s hide slide (self-correcting, tooltip did the same); badge zone only for units with `showRoleZone` on (all four Bergsons are); the scene holding the bus gains an empty `onFamilyRoleBadgeHover` entry on next save (expected). Docs: `tech/combat-architecture.md` should mention the new event.
