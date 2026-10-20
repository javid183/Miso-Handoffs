# Report: Preview pass C7 (follow zones for every Bergson, cover icon = the coverer's quadrant icon)

Plan: plans/2026-10-19-preview-pass-tech.md (C7)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (compiles clean; EditMode suite green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`; nothing played)

## What changed

Should-fixes (separate unit):
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneAttackMatch.cs`: `ZoneEqualsBasicAttack(GUnit)` returns false unless the unit's faction is the player's (new pure `BelongsToPlayer`); the 3-arg overload now uses `RoleZoneRules.ZoneDuplicatesReach`.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`: new `ZoneDuplicatesReach(zone, reach, ignored)` = same cells once the footprint is out of both, and the zone has something left (a footprint-only zone is never a duplicate). `SameCellSet` is unchanged (now unused by game code, still tested).
- `Core/Systems/RoleZoneSystem/Editor/RoleZoneAttackMatchTests.cs` (+ `.meta`): 6 tests (footprint-only zone, empty reach, differing cells, faction gate incl. nulls).

Follow zones and cover icons:
- `Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs`: for any Bergson's move preview, draws the mover's zone from the ghost cell with the handler's colour, alpha, sprite and slot (opaque override dropped, owner id `int.MinValue` kept); skipped when `ZoneEqualsBasicAttack(unit, cells, ghost)`. Tells `RoleZonePresenter` to hide the mover's committed zone. Cover indicator is now `SetRoleZone` on the destination with the coverer's sprite/slot/colour at alpha 1 under `CoverIconRules.CoverOwnerId(icon)`. `SetCoverIcons` calls and the cover-sprite load warning removed. D-067 strict fist rule untouched.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`: `SetSuppressedOwner(GUnit)` (non-static); `Redraw` drops that owner (and its focus) via `RoleZoneRules.WithoutOwner`; reset in `ResetState`.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`: `WithoutOwner` (pure).
- `Core/Systems/RoleZoneSystem/Runtime/CoverIconRules.cs`: `ShowsFollowZone` replaced by `PlanFollowZone` (+ `FollowZonePlan`), added `CoverOwnerId` and `CoverersFor` (`IconsFor` now uses it).
- `Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs`, `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`: added `GetCellsInRange(GridCell origin)` (UI only, same rule as the existing method from the footprint placed on `origin`). Not core; needed because only John and Mark had the overload.
- Tests: `Editor/CoverIconRulesTests.cs` (follow plan, coverers, owner ids replace the old follow-zone tests), `Editor/RoleZoneFocusTests.cs` (4 `WithoutOwner` tests).
- `GridCell.RoleZone.cs` and `GridCell.CoverIcon.cs` are NOT touched; `SetCoverIcons` is now uncalled.

## Acceptance criteria

- [x] Guard `ZoneEqualsBasicAttack(GUnit)` to player faction; false when zone minus footprint is empty: code + tests (`BelongsToPlayer_*`, `Duplicate_ZoneIsOnlyTheFootprint_IsFalse`). The faction lookup itself (`unit.Faction` vs `CombatLevel.PlayerFaction`) is covered only by play check (Masher Goblin badge tooltip).
- [x] All four Bergsons draw a follow zone from the ghost cell in the normal style: code; pure plan tested; visual needs the play check.
- [x] Follow zone skipped when it equals the basic attack from the ghost cell: code + `FollowPlan_EqualsBasicAttack_*`; play check for Linda and Lucy.
- [x] Mover's committed zone hidden during the preview, restored on cancel, commit, death, turn end: code (`_suppressedUnit` is recomputed every Update and released whenever no preview is on; `Rebind` and `OnLevelEnded` release too); `WithoutOwner` tested; restore timing needs the play check.
- [x] Other Bergsons' zones unaffected: only the mover is suppressed.
- [x] Cover indicator = coverer's own icon in its quadrant at alpha 1 (John TL, Mark TR via their slots), per-coverer owner id, `SetCoverIcons` no longer called, D-067 unchanged: code + `Coverers_*`, `CoverOwnerIds_*`; play check for the look.
- [x] No new statics; encodings kept (files LF; the one new test file is LF, no BOM).

Tests: full EditMode suite 262 total, 261 pass; the only failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (known). Console: no errors, only pre-existing warnings. Role-zone namespace alone: 143/143 pass.

## Save reset

no

## Decisions I made

- The committed zone is hidden whenever the mover's follow zone could be computed, even when the follow zone itself is not drawn (equals the basic attack). So Linda/Lucy show neither the old zone nor a new one during a move preview. Same behaviour as asked for "hidden entirely"; say if you want the committed zone kept in that case.
- Suppression path: `MovePreviewCoverPresenter` finds the `RoleZonePresenter` with `GetComponent` on its own GameObject (both are added by `ShowStatsHoverPreview`); no Find calls, no bus event, no core edit.
- Cover owner ids `int.MinValue + 1` (shield) and `+ 2` (fist), alongside the existing follow-zone id `int.MinValue`; relies on the same "handler instance ids never take these" assumption as before.
- `RoleZoneRules.SameCellSet` left in place (unused by game code now) rather than removing a tested public function.
- Linda/Lucy overloads use the unit's footprint at `origin` (`TryGetFootprintCells`, fallback to the single cell), so a multi-cell unit would give the same result as the committed method.

## Needs THJ

none

## Docs to update

- `design/gdd/family-systems.md`: move preview shows the mover's zone from the ghost tile for all four Bergsons (hidden when it equals the basic attack there); the committed zone is hidden during the preview; the cover indicator is the coverer's zone icon at full alpha.
- `tech/combat-architecture.md`: `RoleZonePresenter.SetSuppressedOwner`; `GetCellsInRange(origin)` now on all four role handlers.
- `build-log.md`: C7 entry (coordinator).

## Risks and loose ends

- With Shift held during a move preview, John's or Mark's committed zone (shown by Shift, alpha ~0.75) and their full-alpha cover icon on the destination sit in the same quadrant, so the cover icon draws over it. Not hidden; check in the play check whether it reads fine.
- On commit the suppression is released as soon as target selection ends, so the old committed zone may flash for the length of the walk until `unitEndMoving` redraws it (before C7 it was simply always shown, so this is not new, but it is now a visible hide-then-show). Verify in the play check.
- `GridCell.CoverIcon.cs` and `CoverShield`/`CoverFist` sprites are now unused (deleting is the separate cleanup). `JohnTetherPresenter` (C8) may still want `CoverShield`.
- Cover `Opaque()` forces alpha 1; if a handler colour later carries meaning in alpha, revisit.
- C9 must check: Linda and Lucy follow zone hidden at the ghost (and committed zone gone), John/Mark follow zone drawn, both move overloads match the committed zones from their own cell, multi-cell not testable (no such Bergson).

## Proposed commits

1. fix(roles): hide-on-attack-match only for player units, and never for a zone that is just the unit's own tiles:
   `Core/Systems/RoleZoneSystem/Runtime/RoleZoneAttackMatch.cs`, `Core/Systems/RoleZoneSystem/Editor/RoleZoneAttackMatchTests.cs` + `.meta`, and the `ZoneDuplicatesReach` hunk of `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs` (plain). `RoleZoneRules.cs` also holds the `WithoutOwner` hunk for commit 2, so stage it with `git add -p` (first hunk only), or put the whole file in commit 1 if you prefer; commit 1 compiles with only its own hunk.
2. feat(preview): follow zones for every Bergson and the coverer's zone icon as the cover indicator:
   `Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs`, `RoleZonePresenter.cs`, `CoverIconRules.cs`, the `WithoutOwner` hunk of `RoleZoneRules.cs`, `Editor/CoverIconRulesTests.cs`, `Editor/RoleZoneFocusTests.cs`, `Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs`, `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (plain; no core file touched). Do not stage `Packages/` or `ProjectSettings/`.

## Other branches

none

## How to see it

1. Open the combat scene, Play (the verifier or THJ; I did not enter Play mode).
2. Select Linda or Lucy and hover a tile in her move range: no zone icons appear around her old tile or the ghost (sword icons only). Cancel (right click) or move: her state returns as before.
3. Select John, then Mark, hover a tile: their zone is drawn from the hovered tile in the normal colour and alpha, and their old zone is gone. Move away or cancel: the old zone returns.
4. Select Linda or Lucy and hover a tile inside John's zone: the destination shows John's shield-slot icon in his quadrant (top left) at full alpha; inside Mark's strict fist condition, Mark's icon in his quadrant (top right).
5. Open a Masher Goblin's panel and hover its role badge: no "same tiles as the attack" line.
6. Hold Shift during a move preview and look at the quadrant overlap noted under Risks.
