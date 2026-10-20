# Grid preview pass: tech plan

Size: L    Tier: 3 (Family Roles UI; three core files)    Assigned to: miso-implementer (one chunk per run)
Branch: thj/preview-improvements
Status: approved 2026-10-19 (D-082; C7 revised); in progress

## Why

THJ's preview playtest notes P1–P7 (`playtests/2026-10-19-preview-notes.md`), studied in the design plan `plans/2026-10-19-preview-pass-design.md` (the source for every cause, file:line and value below). THJ decided Q1 to Q6: D-076 to D-081. The designer's G1 to G4 and G9 ride on this plan's approval.

## Goal

Each kind of grid information is drawn once, from one source, in one visual language, and every preview matches what the real action does.

## Acceptance criteria (by chunk)

**C1 Shared attack reach (P3).**
- [ ] `UnitThreatAnalysis.AttackReachFrom(GUnit unit, RuntimeAbility ability, GridCell origin)` returns the cells that ability can target from `origin`. It is built from `PlayerController.ComputeAttackRangeFromOrigin` (L1399-1426): shape definitions, footprint, straight lines, ranged reach, the unit's own faction as `requestFaction`, `IncludeSelf` and `ignoreRelationOnWalk` honoured. It never passes `source: unit` (`GridCell.cs:827`).
- [ ] `GetAttackableCells` and `GetThreateningEnemies` use it, so John's Shield Dash gives straight lines, not a diamond, and ranged reach crosses gaps. The AoE splash and every-attack logic is removed from the Bergson path, but stays available for the enemy danger zone (C5) as "ready Attack abilities" (not on cooldown).
- [ ] EditMode tests on a small built test grid if feasible: a straight-only ability gives a cross; ranged reach crosses a missing cell; a footprint origin. If a test grid can't be built in EditMode, say so and cover it in the play check.
- [ ] Performance: no cross-frame cache in the first pass (no static state). Measure one Shift refresh and one ghost hover on the largest available level (Stopwatch log, removed before commit). If either is over 2 ms, add a per-refresh memo (instance-scoped, no statics) and report the numbers.

**C2 Ghost and approach previews use it (P6).** Core `PlayerController`, Tier 2 bugfix.
- [ ] The ghost sword icons (L990-1031, the inline `GetRangeCells` call at L998-1003) and the approach preview (L1392, L1481) call `AttackReachFrom`. `ComputeAttackRangeFromOrigin` is removed or becomes a one-line forward.
- [ ] Linda's ghost on (2,4) shows a sword icon on (4,4) when (3,4) is missing, as her real attack does. This is a play check.
- [ ] `ShowAffectedArea` abilities keep their current path (`ComputeAffectedCells`).

**C3 Hover gate over the HUD (G1, D-078).** Core `GridManager`, behaviour change, own commit.
- [ ] `GridManager.HandleHovering` (L149-175) does not hover a cell while the pointer is over a raycast-target UI element on a Screen Space (Overlay or Camera) canvas. World-space canvases (unit info panels) don't block it.
- [ ] Entering the HUD clears the last hovered cell (`ClearLastHoveredCell`, L135), so a stale ghost, follow zone or Shift preview goes away.
- [ ] Clicks on the grid are unchanged; only hover is gated. Check that the existing click path doesn't depend on the hovered cell. If it does, say so and stop for a decision.

**C4 Badge drives the role-zone layer (P1, D-077).** Core `GlobalEventBus`, additive.
- [ ] A new event `GlobalEventBus.onFamilyRoleBadgeHover(GUnit unit, bool hovered)`, declared like `onFamilyRolePrompt` (D-068), raised by `UnitPanelUI` on badge enter and exit (L254-285).
- [ ] `UnitPanelUI` no longer calls `SetInAttackRange` for the badge.
- [ ] `RoleZonePresenter` shows that unit's zone while the badge is hovered, even if the unit isn't selected and Shift isn't held, in focus style (C6). It clears on exit, on presenter disable, and on scene change. Subscribe and unsubscribe in OnEnable and OnDisable through the existing `Rebind`.
- [ ] Badge hover and the zone show the same cells (they share `GetCellsInRange()`).

**C5 Shift model and tints (P7, G3, D-079; D-072's enemy tint).**
- [ ] Shift on a Bergson: attack icons = `AttackReachFrom(unit, unit.DefaultOccupiedCellAbility, unit.CurrentCell)`. No Shift move layer on the **selected** unit (its real move range is already drawn). Other Bergsons keep their Shift move layer.
- [ ] Shift on an enemy: move layer plus a danger zone (the union of `AttackReachFrom` for every ready Attack ability from every reachable cell), recomputed on each Shift press or hover.
- [ ] Tints are constants in `GridCell.ShiftPreview.cs` (core partial, values only, plus the enemy/Bergson split). Starting values from design §3 G3: Bergson move (0.6, 0.8, 0.8), Bergson attack (1, 0.9, 0.75), enemy move (0.7, 0.45, 0.4), enemy attack (1, 0.25, 0.2). If the layer has no per-kind enemy split yet, add one the smallest way (a kind enum value or a bool parameter), additive.

**C6 Focus instead of narrowing (P4, D-076), and the P5 hide (D-080).**
- [ ] `RoleZoneRules.OwnersToShow` keeps every zone under Shift and reports a focused owner (the hovered Bergson, or the badge-hovered unit). The focused entry draws at full alpha and scale 1.15 in its quadrant; the others are unchanged. This needs per-entry scale and alpha in `RoleZoneLayerSet`/`GridCell.RoleZone.cs` (core partial, additive). EditMode tests for the new rules output.
- [ ] Selected-unit zone hidden when its cell set equals `AttackReachFrom(unit, basic attack, committed cell)` (computed from the committed cell only, never the ghost). Shift and badge hover still show it. EditMode test of the equality rule as a pure function over cell sets.
- [ ] Also fold in the C4 review's should-fixes: remove the now-unused usings in `UnitPanelUI.cs`; fix or rename `RoleZoneBadgeHoverTests.AfterExit_BackToSelectedOnly_AndNoFocus` (its first call has no effect).
- [ ] Role-badge tooltip gains one line when the zone is hidden for that reason. Wording proposed by `miso-narrative` before the build (an established-voice UI line, Tier 2). Placeholder until then: "Same tiles as her attack." (gendered: Linda and Lucy; make it per-unit or neutral per the narrative proposal).

**C7 Follow zones for every Bergson, cover icon = the coverer's quadrant icon (G2 as revised by THJ, D-082; G4).**
- [ ] During any Bergson's move preview (John, Mark, Linda, Lucy), the mover's committed zone is hidden entirely and its zone is drawn from the ghost tile (`GetCellsInRange(origin)`) in the normal zone style (same icon, quadrant, colour and alpha as a committed zone; no faint ghost style, no opaque override).
- [ ] The D-080 equality rule applies to the follow zone: if it equals `AttackReachFrom(unit, basic attack, ghost cell)`, it is not drawn (the ghost's sword icons already show those tiles). Today that hides Linda's and Lucy's follow zone. Use the same pure equality function as C6.
- [ ] Other Bergsons' zones are unaffected (shown only under Shift, as before). The mover's committed zone comes back on cancel, on commit (normal redraw), on death and on turn end.
- [ ] For other movers, the cover indicator on the destination is the coverer's own zone icon in the coverer's quadrant at full alpha (John TL, Mark TR, via `SetRoleZone` with a cover owner id per coverer), replacing `SetCoverIcons`. D-067's strict fist rule is unchanged. `GridCell.CoverIcon.cs` falls out of use; leave the file and remove its calls (deleting it is a separate cleanup THJ can OK later).

**C8 Tether arc (P2, D-081).**
- [ ] A new non-core static helper `ArcLine.SetQuadratic(LineRenderer line, Vector3 start, Vector3 end, float height, int samples)` with no state, matching `GUnit.cs:853-874`'s Bézier. EditMode test of the points (start, end, apex height).
- [ ] `JohnTetherPresenter` draws John's head (+0.8, same anchor as `ThreatLineRenderer`) to each covered ally's head as an arc. Starting values: John's `RoleZoneColor` with alpha 0.7, width 0.015, height 1 + 0.15 per cell of distance, 16 samples. Material: the threat line's `M_LineShine` if it can be loaded the same way the threat line gets it; otherwise keep `Sprites/Default` and report it. Sorting: Default layer, order 0 (the threat arc's). The Overlay layer goes.
- [ ] A small shield cap at the ally end: a SpriteRenderer with `GridOverlays/CoverShield`, or John's own `ShieldOutline` if CoverShield is dropped in C7, tinted the same.
- [ ] `GUnit.ShowThreatLineTo` is not touched (switching it to the helper is a later, separate core commit).

**C9 Play check and profile (G9).** Verifier with THJ's agreed time, or THJ himself.
- [ ] Dense board (four Bergsons and enemies on overlapping zones): do the Move frames hide zone icons? If yes, raise the role-zone sorting to between frame and glow (design G9). That is a follow-up, not part of C9.
- [ ] Multi-cell ghost sources: the helper unions reach over the whole footprint for every walkability mode (C2 review); check a multi-cell unit's ghost if one exists.
- [ ] A gap map for Linda, John's dash under Shift, Shift on an enemy, the badge hover over and off the board, John's prompt tether, cancel and commit of a John or Mark move.

**All chunks:** compile clean; EditMode suite passes except the known red; reviewer on C2, C3, C4 and C6 (core files); commit messages without private tags (conventions).

## Scope

In: the chunks above.
Out: `GUnit.ShowThreatLineTo` switching to the helper; ref-counting the shared highlight bools (D-071); the ability-bar hover previews (S9); a player-facing name for "danger zone" (only needed if it ever appears as text); deleting `GridCell.CoverIcon.cs`; the role pipeline rules (Family Role chunk, D-062).

## Touches

Systems: `PlayerController` (core), `GridManager` (core), `GlobalEventBus` (core, additive), `GridCell.ShiftPreview.cs` and `GridCell.RoleZone.cs` (core partials, additive or values only), `UnitThreatAnalysis`, `ShowStatsHoverPreview`, RoleZoneSystem presenters and rules, `UnitPanelUI`, `JohnTetherPresenter`.
USPs: Family Roles (main), Duos (the badge no longer erases the Mark–John shout cells).
Docs: GDD `family-systems.md` (zone display, focus, P5 hide, cover icon, tether) and `combat-rules.md` (Shift view), by the designer after the build; `tech/combat-architecture.md` (one reach helper, hover gate); `build-log.md`; the glossary only if a name is needed.

## Approach

Order: C1 → C2 → C3 → C4 → C5 → C6 → C7 → C8 → C9. One implementer run per chunk, one commit per chunk (C1 may be two if tests stand apart). Opus for C1 to C4 and C6 (core or subtle), Sonnet for C5, C7 and C8. The reviewer runs after each core chunk; the verifier runs compile and the suite after each chunk, and the play check at C9. C1 and C2 can't run in parallel (one writer). C4 waits for the narrative tooltip line only for its text; it can use the placeholder and the text can change in C6.

## Risks

- **Statics:** `UnitThreatAnalysis` is a static class. No static cache (C1 stays stateless; any memo is instance-scoped). `ArcLine` is stateless. No `PlayModeStaticReset` change expected; if one appears, add the hook.
- **AI:** `UnitThreatAnalysis` isn't used by the AI (its only callers are `ShowStatsHoverPreview` and `PlayerController`; recheck in C1). No re-baseline.
- **Events (C4):** unsubscribe on disable; a hover that ends while the panel is hidden must not leave a zone on screen (clear on presenter disable and on a unit change).
- **Hover gate (C3):** a dead board under world-space panels. Gate screen-space canvases only, play check. Behaviour change in core: own commit, revertible.
- **Cause of P1 is inferred:** the two-minute repro (design P1) goes into the C9 play check; C3 and C4 are wanted either way.
- **Performance (C1, C5 enemy danger zone):** measure, memo only if needed.
- **Serialized fields:** none renamed. **Save data:** none. **Other branches:** none (work lives on this branch and merges to `main` later).

## Gates

Compile / tests / review (C2, C3, C4, C6) / play check: yes, needs THJ's time (C9) / docs as listed.

## Commit log

(Hashes recorded here as chunks are committed.)

| Chunk | Hash | Message |
| --- | --- | --- |
| C1 | `b678aeecc` | fix(preview): share one attack-reach helper for Shift and enemy threat arcs |
| C1 tests | `e48f2f58d` | test(preview): edit-mode tests for attack reach geometry |
| C2 | `90a4908a3` | fix(preview): ghost and approach previews use the shared attack reach |
| C3 | `663a2b1d4` | fix(grid): stop grid hover while the pointer is over the HUD |
| C4 (a) | `16b33cfac` | feat(events): role badge hover event on the global event bus |
| C4 (b) | `744cd8fc8` | feat(ui): role badge hover shows the unit's role zone instead of sword icons |
| C5 (a) | `ce104f51e` | feat(grid): split Shift preview tints into Bergson and enemy kinds |
