# masher-c3 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **APPROVE** (nothing to fix in C3).

1. The "did not initialize its role ability" warning will remain until C4: it comes from `FactionRoleHandlerBase.CanTickAbility()` (`:175-186`) when `_abilitiesInitialized` is false, and the Masher handler overrides `Initialize`/`InitializePartially` without calling the base (`:26-42`). C4 must call `base.Initialize(orchestrator)` and `base.InitializePartially(orchestrator)` (base adds its own `turnEnded` lambda; harmless duplicate). `reports/masher-c3.md`'s claim that the empty preset caused it is wrong.
2. Visible side effect: with the preset set, `UnitPanelUI.SetupFamilyRole` (`:246-256`) now shows a Family Role badge on the Masher's panel (slam icon and title); badge hover shows its zone (D-077, `RoleZoneRules.OwnersToShow`). Before, a null preset likely threw on that path (unconfirmed). Add to the play check / ask THJ.
3. Tool, counter asset, Unity-written defaults, prefab (no references to the removed component remain; FXRunner kept), `sideVisualMode`, the one AIRegressionTest line: all fine. AI can't pick the counter (not on `Abilities` or `DefaultOccupiedCellAbility`; `introducible: 0`).
4. Between C3 and C4 the old handler passes the occupant instead of the cell (same position); 2 × 2 check stays with the verifier.
5. Commits clean and correctly ordered.
