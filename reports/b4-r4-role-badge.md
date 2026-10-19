# Report: B4 R4, role badge on the unit panel (item D)

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (play check pending)

## What changed

- `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs` (new): `RoleBadgeState` (None, Ready, NoFtp) and static pure `RoleBadgeRules` (`Evaluate`, `TooltipLine`). No Unity types, no state.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` (new partial): creates a 14x14 square pip at runtime as a child of `familyRoleImage` (bottom-right corner, raycast off, so hover is unchanged and it hides with the icon). Green = READY, dim red = NO FTP. Subscribes to the unit faction's `FamilyTimePoints.OnValueChanged` (event-driven, no per-frame work); resubscribes when the shown unit changes and unsubscribes on clear/destroy. `GetRoleBadgeState` is the single state source (switch it to uses-per-round after Pilot 1).
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs` (5 lines): class made `partial`; `SetupRoleBadge(unit)` after `SetupFamilyRole`; `ClearRoleBadge()` in `ClearUnitControlPanel` and `OnDestroy`; the hover tooltip description gets `+ RoleBadgeTooltipSuffix(unit)` (evaluated at hover time; "\nNeeds N FTP; Pass-by refills FTP." only when NO FTP, empty when READY). The SetInAttackRange hover code is untouched.
- `miso/Assets/_Project/Features/UI/Panels/Editor/RoleBadgeRulesTests.cs` (new, 8 tests).

Read-only APIs used, no core file touched: `AbilityOrchestrator.HasFactionRole` / `FactionRoleRequiredFTP`, `GUnit.PointConsumer.CanConsume` (same check as `FactionControllerBase.cs:171-172`, so it follows the real cost rule incl. mode), `Faction.Tracker.FamilyTimePoints.OnValueChanged`. No getter was missing.

## Acceptance criteria

- [x] D badge ready / no FTP: logic covered by `RoleBadgeRulesTests` (8 pass); visuals need a play check.
- [x] No stun, no cooldown/uses state: none added.
- [x] Updates on FTP change and unit change: event subscription, by code reading; play check needed.
- [x] Tooltip line only when NO FTP, real RequiredFTP: tested as a string rule; in-game wording needs a play check.
- [x] Units without a role show no badge: `GetRoleBadgeState` returns None and the badge is a child of the icon, which is hidden.
- [x] No core change.

Tests: refresh_unity compiled with 0 console errors. Full EditMode run: 143 total, 142 passed, 1 failed (`Baseline_MatchesCurrentAI`, the known red). The 8 new tests also pass when run alone.

## Save reset

no

## Decisions I made

- Used `PointConsumer.CanConsume` instead of comparing the pool myself, so the badge matches the firing check exactly (also in ATB mode).
- Badge made at runtime in code, no UnitPanel prefab edit. Chose a plain square pip (no sprite) because no round sprite is guaranteed at runtime; THJ can swap in a sprite later.
- `UnitPanelUI` made `partial` (one-word change) to keep the logic in a new file.
- A unit with a role but no `FamilyTimePoints` (e.g. ATB mode) shows the badge from `CanConsume` once, with no live updates.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`: note `RoleBadgeRules` / `UnitPanelUI.RoleBadge.cs`.
- `build-log.md`: R4 entry.

## Risks and loose ends

- The pip position (bottom-right of the role icon) and size are guesses; a play check may want a nudge. If the icon's RectTransform is small, the pip may overlap neighbours.
- Tooltip is built at hover time, so it will not change while the cursor stays on the icon.
- The badge refreshes on FTP change and unit selection only; if FTP is spent while a different faction's panel is shown, nothing happens (fine, panel shows player units).
- The `+` onto `Preset.Description` assumes the description is a plain string.

## Proposed commits

1. `feat(ui): role badge (ready / no FTP) next to the Family Role icon on the unit panel (B4 R4)` (plain), files:
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs`
   - `miso/Assets/_Project/Features/UI/Panels/Editor.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Editor/RoleBadgeRulesTests.cs` + `.meta`

## Other branches

`thj/home-test` and `thj/oct-build-fixes` need it on their next merge.

## How to see it

1. Open a combat level and select John, Linda, Lucy or Mark: a small green pip sits at the bottom-right of the role icon while FTP >= 1.
2. Spend FTP to 0 (let roles fire): the pip turns dim red live. A Pass-by refill turns it green.
3. Hover the role icon with 0 FTP: the tooltip ends with "Needs 1 FTP; Pass-by refills FTP." With FTP it has no extra line; the range cells still highlight.
4. Select a unit without a role (e.g. Toba or an enemy-side unit): no pip.
5. Play check also: switching selection between units does not leave a stale pip or stale updates.
