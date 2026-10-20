# Grid preview pass (UI/UX study of every combat grid preview)

Size: L    Tier: 3    Assigned to: miso-game-designer
Branch: all (code lands on THJ's new branch after the `thj/fr-readability` merge into `main`)
Status: waiting on THJ

## Why

THJ's 2026-10-19 playtest of the role-zone icons (D-075) raised seven notes about grid previews: [`playtests/2026-10-19-preview-notes.md`](../playtests/2026-10-19-preview-notes.md), P1 to P7. Three are bugs (P1, P3, P6), two are about redundancy (P5, P7), one is about visual style (P2) and one is a rule question (P4). He asked for a pass over every grid preview, not just these seven.

## Goal

Each kind of grid information is drawn once, from one source of truth, in one visual language. Whatever a preview promises, the real action does.

## Acceptance criteria

- [ ] The inventory below is confirmed by THJ (or corrected) as the full list of grid previews.
- [ ] THJ answers Q1 to Q6.
- [ ] A tech plan is written from the work breakdown (§6), bugs first.

## Scope

In: every grid preview in combat (cell layers, icons, ghost, lines), the HUD role-badge hover, the Shift view.
Out: info panels and damage numbers (shown only where they affect the grid), Home, QTE timing, Family Role rules (D-062 chunk).

## Touches

Systems: `GridCell` partials (core), `GridManager` (core, hover gate only), `PlayerController` (core, ghost range fix), `UnitThreatAnalysis` (not core), RoleZone presenters (not core), `UnitPanelUI` (not core), `GlobalEventBus` (core, one additive event, if Q2 picks it).
USPs: Family Roles (main), Duos (indirect).
Docs: `design/gdd/family-systems.md` (role-zone display rules), `design/gdd/combat-rules.md` (Shift view), decisions log.

---

## 1. Preview inventory

Sorting orders come from code comments (`GridCell.RoleZone.cs:20`, `GridCell.ShiftPreview.cs:33-35`, `GridCell.CoverIcon.cs:15`). I did not open the prefab to confirm them. "Shared bool" means one flag per cell that several features write: the last writer wins, and turning it off erases every other writer's mark.

| # | Preview | Shows | Trigger | Layer / sorting | Source of truth for its cells | Code |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Move range | Cells the selected unit can walk to | Unit selected (default walk) | `SetHighlight(isMove)`, shared bool, Move frame -8, glow -7 | `FactionControllerBase.ComputeAbilityRangeCells` → `GetRangeCells` (walk radius × multi-activations) | `FactionControllerBase.cs:437-438, 755-770` |
| 2 | Ability range | Cells the chosen ability can target; multi-activation tiers coloured by level | Ability picked (bar, or a click on an enemy) | `SetHighlight`, shared bool, Ability frame -8 (+ arrow for self/surrounding) | `ComputeAbilityRangeCells` → `AbilityPreset.ComputeTargetSelectionCells` | `FactionControllerBase.cs:450, 471-479, 741-753`; `AbilityPreset.cs:458-515` |
| 3 | Approach range | Attack range from the cell the unit would walk to, when it hovers an out-of-range enemy (auto-move) | Hover enemy, basic attack with auto-move | `SetHighlight`, shared bool (replaces #2 while hovered) | `PlayerController.ComputeAttackRangeFromOrigin` (shape, footprint, straight, ranged reach) | `PlayerController.cs:949-961, 1399-1426, 1477-1489` |
| 4 | Path arrows | Walk path to the hovered cell (alt paths) | Hover a move cell | `pathPreviewVisual` per cell | `RebuildAltPaths` | `PlayerController.cs:900-927`; `GridCell.cs:1043` |
| 5 | Ghost | Translucent unit on the destination | Hover a move cell / approach | Unit child object | `ResolveGhostCell` (dash providers) | `PlayerController.cs:965-976, 1438-1443`; `GUnit.cs:840` |
| 6 | Ghost "sword" icons | Basic-attack reach from the ghost tile; affected area for `ShowAffectedArea` abilities | Same as #5 | `SetInAttackRange`, shared bool, -9 (override sprite possible) | Own inline `GetRangeCells` call (**misses ranged reach**, P6) or `AbilityPreset.ComputeAffectedCells` | `PlayerController.cs:990-1031` |
| 7 | Enemy threat arcs | Curved line from each enemy that could hit the ghost tile | Same as #5 | `LineRenderer` on every unit (`UnitBase.prefab` "ThreatLineRenderer", y +0.8, width 0.01, `M_LineShine`, Default layer order 0), quadratic Bézier, arc height 1 | `UnitThreatAnalysis.GetThreateningEnemies` → `GetAttackableCells` (**P3 geometry bugs**) | `PlayerController.cs:981-987`; `GUnit.cs:853-880` |
| 8 | Pass-by VFX | Allies on the path that will be passed by | Same as #4 | Unit VFX | `PassByHandler.CanPassBy` | `PlayerController.cs:1086-1108` |
| 9 | Push arrows / aim arrow | Push direction per cell; aim direction for directional abilities | Hover target | `directionPreviewVisual` / `aimDirectionPreviewVisual` (-1 per comment) | `AbilityPushPreview.ComputeFor` | `PlayerController.cs:1006-1008, 1035-1040`; `GridCell.cs:1010-1036` |
| 10 | Damage preview | HP loss and kills on the info panel | Hover target | World UI (not the grid) | `AbilityDamagePreview` (core) | `PlayerController.cs:1462-1475` |
| 11 | Targeted / counter | Picked target cells, multi-target counter | Target picked | `SetTargeted`, -9 | `PhaseData.TargetCells` | `FactionControllerBase.cs:591, 619, 835` |
| 12 | Potentially targeted | Enemy intent (future action) cells; compound previews | Shift + hover an enemy; some effects | `SetPotentiallyTargeted`, shared bool | `GUnit` future action → `ComputeAffectedCells` | `GUnit.cs:1340-1381`; `ShowStatsHoverPreview.cs:109`; `AEffectCompound.cs:646` |
| 13 | Hover | Cell under the cursor | Mouse over a cell (**also through the HUD**, see G1) | `gridCellHoverVisual` -7 | `GridManager.HandleHovering` (world mouse position, no UI check) | `GridManager.cs:149-175` |
| 14 | Role zone (selected) | The selected Bergson's role zone as its own icon in its own quadrant | Unit selected | Role-zone layer, per owner, -10 | Each handler's `GetCellsInRange()` | `RoleZonePresenter.cs:179-252`; `RoleZoneRules.cs:18-54` |
| 15 | Role zones (Shift) | Every living Bergson's zone; **hovering one shows only it** (P4) | Shift held | Same layer | Same | `RoleZoneRules.cs:34-42` |
| 16 | Follow zone | John's or Mark's zone as it would be from the ghost tile | Move preview of John / Mark | Same layer, owner `int.MinValue`, opaque | `John/MarkFactionRoleHandler.GetCellsInRange(origin)` | `MovePreviewCoverPresenter.cs:222-248` |
| 17 | Cover icons | Shield (lower left) if the destination is in John's zone, fist (lower right) if every melee spot of it is in Mark's | Move preview of any other unit | Own layer, -5, opaque role colour | Handlers' `GetCellsInRange()` + `CoverIconRules` | `MovePreviewCoverPresenter.cs:193-230`; `GridCell.CoverIcon.cs` |
| 18 | HUD badge hover | John's (or any Bergson's) role zone as attack "sword" icons | Hover the Family Role badge on the unit panel | `SetInAttackRange`, shared bool, -9 | The same `GetCellsInRange()` | `UnitPanelUI.cs:254-285` |
| 19 | Shift move/attack | Hovered unit's reachable cells (blue) and every cell it could attack after moving (pink) | Shift + hover any unit | Shift layer (own renderers, alpha 0.55, -9/-8/-10) | `UnitThreatAnalysis.GetReachableCells` / `GetAttackableCells` (**P3**) | `ShowStatsHoverPreview.cs:105-125`; `GridCell.ShiftPreview.cs` |
| 20 | John's tether | Straight line John → each ally he would cover | His role prompt is up (game paused) | `LineRenderer`, width 0.05, opaque, "Overlay" sorting layer | `handler.Targets` | `JohnTetherPresenter.cs:175-249` |
| 21 | Duo previews | Mark–John shout cells (sword icons), duo move ranges, Mark–Lucy targets | Duo targeting | `SetInAttackRange` / `SetHighlight` / `SetTargeted`, shared bools | `UnitsCooperationHandler` (core) | `UnitsCooperationHandler.cs:748-764, 1113-1117, 1419-1441` |
| 22 | Boss warnings | Pulsing warning cells and text | Boss telegraph | `SetWarningHighlight` | Boss scripts | `GridManager.cs:187-230`; `BossGoblinQueen.cs:103`; `BossMountainDeev.cs:57`; `MasherGoblinFactionRoleHandler.cs:417` |
| 23 | Level goal | Goal cells and label | Always (when the level has one) | `gridCellHighlightLevelGoal` | Level objectives | `GridCell.cs:374` |

**"Attack reach from a tile" is computed in five places today**, and they disagree:

| Where | Straight lines | Ranged reach (across gaps) | Shape definition | Footprint | Abilities |
| --- | --- | --- | --- | --- | --- |
| Real targeting, `AbilityPreset.ComputeTargetSelectionCells` | yes | yes | yes | yes | the chosen one |
| Approach preview, `PlayerController.ComputeAttackRangeFromOrigin` (L1399) | yes | yes | yes | yes | the active one |
| Ghost icons (L996-1003) | yes | **no** | **no** | **no** | basic attack |
| Shift and threat arcs, `UnitThreatAnalysis.AttackRangeFrom` (L148-185) | **no, hard-coded `straight: false`** (L167, L177) | **no** | yes | yes | **every Attack ability**, plus AoE splash |
| Role handlers, `GetCellsInRange()` | per handler | per handler | no | Linda and Lucy yes | the role ability |

---

## 2. THJ's seven notes

### P1. John's HUD badge previews different tiles than his zone (bug)

**What the code does (verified).** Both paths call the same handler's `GetCellsInRange()`: `UnitPanelUI.cs:262` and `RoleZonePresenter.cs:223`, with `AbilityOrchestrator.cs:63` resolving the same component. Computed at the same moment, the cell sets are identical, so the coordinator's first guess (two separate computations) is wrong. The difference comes from **drawing**:

1. **Likeliest: hover leaks through the HUD.** `GridManager.HandleHovering` (`GridManager.cs:149-175`) hovers the cell under the world mouse position and never checks whether the pointer is over UI. When the badge sits over the board, hovering it also hovers a grid cell. That fires the move preview there: the ghost, the ghost's sword icons, and John's **follow zone** (shield icons in his quadrant) from that phantom tile (`MovePreviewCoverPresenter.cs:222-223`). At the same time the badge draws sword icons from his real tile. The two sets disagree, which matches THJ's description. *Inferred from code, not reproduced.*
2. **Contributing: the badge draws on the shared `SetInAttackRange` bool.** Its sword icons merge with any already on the grid (ghost icons, Mark–John duo cells). On unhover, `SetInAttackRange(false)` (`UnitPanelUI.cs:281`) also erases the other features' icons on those cells. This is the same bug class D-071 fixed for Shift.
3. **Less likely: a stale committed zone.** `RoleZonePresenter` redraws only on events (selection, turn, death, birth, `unitEndMoving`, `abilityPerformed`, Shift, hover, fade). If a position change or a change to `Stat_RAD` happens without one of those events, its zone lags while the badge computes live.

**Quick repro to confirm (two minutes).** Select John, hover the badge, then compare: (a) the badge over an empty, off-board part of the screen; (b) the badge over board cells. If only (b) differs, cause 1 is confirmed.

**Options.**

| | A. Badge drives the role-zone layer | B. Keep sword icons, fix the shared bool | C. Remove the badge hover preview |
| --- | --- | --- | --- |
| Player sees | The same icons as the zone, emphasised while the badge is hovered | Sword icons that no longer erase anything | Tooltip only |
| One source / one look | Yes / yes | Yes / no (zone = icon, badge = sword) | n/a |
| Cost | S | S | XS |
| USP | Family Roles + (HUD and grid teach one vocabulary) | Neutral | Family Roles − (the badge loses its link to the grid) |

**Recommendation: A, plus the hover gate (G1) as its own core commit.** On badge hover, the presenter shows that unit's zone even if the unit isn't selected and Shift isn't held, in "focus" style (see P4). It never writes `SetInAttackRange`. How the badge tells the presenter is Q2: the systems critic warned that a cached `FindAnyObjectByType` is a hidden coupling, given domain reload is off and scenes are reloaded.

### P2. John's tether reads as a debug line (style)

**What the code does (verified).** It is a straight, two-point `LineRenderer`: width 0.05 (`JohnTetherPresenter.cs:30, 194`), opaque role colour (L181), `Sprites/Default` material, "Overlay" sorting layer (L27, L245), anchored at the middle of each sprite (L266-270). The enemy threat arc it should match is 0.01 wide (`UnitBase.prefab`: `widthMultiplier` 0.1 × curve 0.1), uses `M_LineShine`, is a 16-sample quadratic Bézier with arc height 1 (`GUnit.cs:853-874`), starts 0.8 above the unit's pivot and sits on the Default layer, order 0. So the tether is five times thicker, straight, unlit-opaque and on a higher layer. THJ's read is right.

| | A. Chain at foot level | **B. Thin translucent arc over the heads** | C. Keep, only thinner |
| --- | --- | --- | --- |
| Feel | Physical, "bound to protect". Also reads as captivity, cold against the family's warmth | "I've got you": a gesture reaching over the battlefield, like the existing threat language | Still debug-like |
| Readability | Hidden by any unit between them; competes with zone quadrants, sword icons and target frames on the grid at the very moment the enemy's attack is drawn there | Above the clutter; nothing occludes it | — |
| Art / code | Needs a chain-link sprite (tiled line) and its own sorting on the grid layer | No new art: same Bézier, same material, same anchor height as the threat arc | XS |
| Risk | Medium (art, occlusion) | Being mistaken for an enemy threat arc (UX critic) | — |

**Recommendation: B.** It reuses the threat arc's look, with three differences so it can't be read as a threat:
- **Shared geometry.** Move the Bézier into a small non-core static helper (e.g. `ArcLine.SetQuadratic(line, start, end, height, samples)`). The tether uses it now. `GUnit.ShowThreatLineTo` can switch to it later, as its own core commit, so the geometry has one home. Duplicating it would create two sources of truth (systems critic).
- **Anchors.** From John's head to the ally's head: the same +0.8 anchor as `ThreatLineRenderer` (or the sprite top), not the body centre.
- **Look.** Starting values: John's orange, alpha 0.7, width 0.015 (1.5× the threat arc, so it survives camera distance), arc height 1 plus 0.15 per cell of distance, `M_LineShine` material. At the ally end, a small cap using the existing `GridOverlays/CoverShield` sprite in John's colour, so it reads as "shield goes here".
- **Draw order.** Use the threat arc's sorting (Default, order 0) first. Raise it to `DynamicTop` only if units hide it in play. It must stay below the bark popups and the world UI. Threat arcs are not on screen during John's prompt (they exist only in the player's move preview, `PlayerController.cs:1119-1121`), so the two never compete in practice.

*Unverified:* whether `M_LineShine` animates while `timeScale` is 0 (the prompt pauses the game). If it doesn't animate, the arc is just static, which is fine.

### P3. Shift shows sword icons John can't reach (bug)

**Root cause (verified).** `UnitThreatAnalysis.GetAttackableCells` (`UnitThreatAnalysis.cs:34-53`) gathers, from **every reachable cell**, the targets of **every Attack-type ability**, and its `AttackRangeFrom` forces `straight: false` with no ranged reach and no `requestFaction` (L163-178). `CollectAttackedCells` then adds the AoE splash of each target (L78-91).

For John that includes Shield Dash: straight lines only, radius 3 × `Stat_RANGE` (`John_Ability_Attack_Dash.asset` L78-83, L129), hitting the cells next to its path. It becomes a radius-3 diamond from every reachable cell, plus splash. It also ignores Dash's cooldown of 2.

The coordinator's guess (move ⊕ attack without blocking) is half right. The main error is lost straight-line geometry, plus counting every attack, not just the basic one. The same function drives the **enemy threat arcs** (#7), so they over-report straight-line enemies and under-report ranged enemies across gaps. It is not used by the AI (only `ShowStatsHoverPreview.cs:113-120` and `PlayerController.cs:982` call it).

**Recommendation.** One non-core helper, `UnitThreatAnalysis.AttackReachFrom(unit, ability, origin)`, built from `PlayerController.ComputeAttackRangeFromOrigin` (L1399-1426), the most correct version today. It takes the unit's own faction, **never passes `source: unit`** (`GridCell.cs:827` would restart from the unit's real cell), and honours `IncludeSelf` and `ignoreRelationOnWalk`. The approach preview, the ghost (P6), Shift (P7) and the threat arcs all call it. The basic attack is `GUnit.DefaultOccupiedCellAbility`, the one the ghost already uses (`PlayerController.cs:996`).

**Cost (systems critic).** With ranged reach, each origin loops over every grid cell (`GridCell.cs:833-851`). Threat arcs call this once per enemy per hovered tile with no cache. Cache each unit's reach until the next move, `abilityPerformed`, death or turn change, and profile on the largest map: under 2 ms per Shift refresh or ghost hover.

### P4. Shift + hover narrows to one zone (rule question)

**What happens (verified).** `RoleZoneRules.OwnersToShow` (`RoleZoneRules.cs:34-42`) returns only the hovered Bergson's zone whenever Shift is held and the cursor is on any family member with a zone, not only the selected one. That is D-064 as written. THJ noticed it on the selected unit, where it is most pointless: that zone is drawn anyway.

| | A. Keep (D-064) | **B. Focus: all zones stay, the hovered one stands out** | C. Never narrow, no emphasis |
| --- | --- | --- | --- |
| Reads | Untangles four zones, but hides "who covers where" exactly when you look at a teammate | Keeps the family map and still answers "which is hers?" | Simplest; crowded on four overlapping zones |
| Cost | 0 | S (`RoleZoneRules` returns an emphasis flag; colour/scale per entry, which the layer set already supports) | XS |
| USP | Family Roles − (the whole-family view breaks on hover) | Family Roles + | Neutral |

**Recommendation: B, and it should replace D-064's narrowing.** The UX critic warned that alpha-only dimming of small quadrant icons is unreadable, and that dimmed blue and purple melt into the Shift tints. So emphasise rather than dim: the hovered unit's icons at full alpha and scale 1.15, the others at their normal 0.75 alpha. Do the Shift re-tint (G3) first. Lever, if it's still crowded: others at 0.45 alpha, desaturated.

### P5. Linda's and Lucy's zone duplicates their attack range (redundancy)

**Facts (verified).** The data match exactly: Linda's role ability and her basic attack are both 4 × `Stat_RANGE`, straight with ranged reach. Lucy's are both a constant 3, Adjacent with ranged reach (`Linda_Ability_FactionRole.asset` L53-58, L104-106; `Lucy_Ability_FactionRole.asset` L54-56; their `PrimaryAttack` assets). THJ's read is **partly** right. In the idle selected state only the move range is drawn, so nothing is shown twice. The double draw appears whenever their attack range is on screen: attack targeting (Ability frames + zone icons on the same cells), Shift (sword icons + zone icons) and the ghost (sword icons from the ghost tile, which are her lane from there).

| | A. As is | **B. Hide the selected unit's zone when it equals its basic-attack reach (THJ's ask)** | C. Hide it only while its attack range is drawn |
| --- | --- | --- | --- |
| Reads | Two icons for one fact | Clean selection. Her lane is learned from the ghost (where it will be) and from Shift | Lane visible at idle; icons vanish when the attack frames take over |
| Cost | 0 | S, not core: `RoleZonePresenter` compares the zone with `AttackReachFrom(unit, basic attack, current cell)` | S, polls `PlayerController` state (as `MovePreviewCoverPresenter` does) |
| Risk | Clutter | "Where did my zone go?" if a run upgrade makes them differ and the zone reappears | Flicker on picking the attack |

**Recommendation: B, by runtime equality, not a new handler field.** It stays true to the data: if a run upgrade ever splits Lucy's attack radius from her role radius, her zone comes back by itself, because then it carries new information. Compute it from the committed cell only, never from the ghost (flicker, systems critic). Add one line to the role badge tooltip, "Same tiles as her attack", so the hidden zone is explained (UX critic). On Shift, the zones still draw for everyone. Fallback if THJ wants explicit control: an Inspector bool `showZoneWhenSelected` on the handler (core, additive, the D-063 pattern).

### P6. Linda's ghost loses sword icons across a gap (bug)

**Root cause (verified).** The ghost's icons call `ghostCell.GetRangeCells(radius, traverse, walkability, straight, includeSelf: false)` (`PlayerController.cs:998-1003`) **without `allowRangedReach`**. `GetRangeStraightCells` walks adjacent cells and stops where (3,4) is missing (`GridCell.cs:916-918`). Real targeting passes `allowRangedReach: preset.AllowRangedReach` (`AbilityPreset.cs:513`), and Linda's attack has it on (`Linda_Ability_PrimaryAttack.asset` L108). The coordinator's guess is right. The same call also skips `requestFaction`, shape definitions and multi-cell footprints.

**Recommendation.** Replace the inline call with the shared helper (P3). Tier 2 core bugfix in `PlayerController`. Add an EditMode test for the gap case if a test grid can be built; otherwise a play check on a map with a gap.

### P7. Shift sword icons cover most of the map (redundancy)

**What happens.** P3's bugs inflate it: Linda's straight radius-4 shot becomes a radius-4 diamond from every reachable cell, which covers the whole map. With correct geometry it would be crosses from every reachable cell. That is still most of a small map, so THJ's point stands after the fix.

| | A. Fix geometry only (reach + attack for everyone) | **B. Bergsons: basic-attack reach from the current tile; enemies: reach + attack (danger zone)** | C. Current tile for everyone |
| --- | --- | --- | --- |
| Bergsons | Still huge for Linda | "What I hit if I stay"; the ghost answers "what I hit from there" with the same shape | Same as B |
| Enemies | Danger zone (Fire Emblem) | Danger zone kept: the only way to see an enemy's full threat before you move | Loses the danger zone; only per-tile threat arcs remain |
| Consistency | One meaning | Two meanings: needs a visible difference (UX critic) | One meaning |

**Recommendation: B, with the two meanings told apart by colour.** Enemy attack cells get their own Shift tint, which THJ already asked for (D-072, enemy move cells in a different tint). For Bergsons, also skip the Shift move layer on the **selected** unit, since its real move range is already drawn. For enemies, count every Attack ability that is not on cooldown at the moment Shift is pressed, recomputed per press: Shift is momentary, so there's no staleness. Q4 asks THJ to confirm B over A. The UX critic leaned toward A for Bergsons, because players may read "no red" as "safe". B is THJ's own proposal, and the tint split addresses that misread.

---

## 3. Redundancy and gaps beyond the list

| # | Kind | Finding (verified unless marked) | Proposal | Size |
| --- | --- | --- | --- | --- |
| G1 | Bug, all previews | Grid hover ignores the HUD (`GridManager.cs:149-175`): ghosts, follow zones, Shift previews and hover frames fire under panels and buttons | Gate hover only on hits on screen-space HUD canvases, not world-space info panels (both critics). When the pointer enters the HUD, clear the last hovered cell so a stale ghost goes away (`ClearLastHoveredCell`, L135). Core: own commit | S |
| G2 | Double draw | During John's or Mark's move preview, the committed zone and the follow zone use the same icon in the same quadrant, so you can't tell which one moves | While the follow zone shows, hide the mover's committed zone; draw the follow zone in a "ghost" style (alpha 0.5, like the ghost sprite) so the change shows even with the ghost on the origin tile (UX critic). Restore it on cancel, death and turn end | S |
| G3 | Colour clash | Shift tints sit next to role colours: move blue (0.55, 0.75, 1) ≈ Linda's sky blue; attack pink (0.85, 0.3, 0.65) ≈ Lucy's reddish purple (`GridCell.ShiftPreview.cs:30-32` vs the handlers' `roleZoneColor`) | Shift tints come from outside the Okabe-Ito role set. Starting values: Bergson move = desaturated grey-teal (0.6, 0.8, 0.8), Bergson attack = warm white (1, 0.9, 0.75), enemy move = dull red-brown (0.7, 0.45, 0.4), enemy attack = strong red (1, 0.25, 0.2). Settle together with Q20 | S |
| G4 | Overlap + double meaning | Cover icons sit lower left and lower right (`GridCell.CoverIcon.cs:18-20`), which are Linda's and Lucy's quadrants (D-075). On a destination in John's zone with Shift held, two shields mean the same thing | **Cover icon = the coverer's own zone icon**, drawn on the destination only, in its own quadrant (John TL, Mark TR), full alpha. One vocabulary ("John's shield in the top left = John covers you here"), no quadrant clash, no extra sprite. Moves `MovePreviewCoverPresenter` from `SetCoverIcons` to `SetRoleZone` with a cover owner id; Mark's strict D-067 rule unchanged | S |
| G5 | Shared bools | `SetInAttackRange` is written by the ghost, the HUD badge and the Mark–John duo; `SetHighlight` by move, ability, approach and duo ranges. Turning one off erases the others (D-071 found 19 call sites) | Remove the badge from it (P1). Leave the rest until a real bug shows up; D-071 rejected ref-counting as high risk | — |
| G6 | Missing info | The zone doesn't say *what* triggers it. John's and Mark's zones are about where the **ally** stands; Linda's and Lucy's are about where the **enemy** is (readability plan, UX misread) | No new grid art. The badge tooltip already carries the rule; keep the D-063 role-badge text authoritative. Revisit only if playtests show the misread | — |
| G7 | HUD ↔ grid | The ability bar previews no tiles on hover; only the role badge does (`Features/UI` has a single grid call, in `UnitPanelUI.cs`) | Consistent after P1: hovering the badge shows the zone exactly as the grid does. Ability-bar hover previews are out of scope (S9) | — |
| G8 | Shift clutter | Shift + hover a Bergson today: four zones in quadrants, the Shift move frames, Shift attack icons over most of the map, every unit's info panel and the enemy's intent cells | After P3/P4/P7/G3: zones (one emphasised), the hovered unit's move frames (none if it's the selected unit), attack icons from one tile (Bergson) or a red danger zone (enemy). Quadrants keep zones apart; colours keep layers apart | — |
| G9 | Four Bergsons + enemies | Worst cell: four zone quadrants + move frame + sword icon + hover + target frame. Quadrant icons are fitted inside the 0.9 box and sit under the frames (-10 vs -8), so a filled Move frame could hide them (**unverified: depends on the frame sprite's fill**) | Play check on a dense board; if the frames hide the icons, raise the role-zone layer to -8.5 (between frame and glow) | XS |

## 4. Proposed preview model (one home per cell set)

| State | Drawn | Cell-set source |
| --- | --- | --- |
| **Always** | Level goal; boss warnings | Level, bosses |
| **Unit selected** | Move range (#1); own role zone unless it equals its basic-attack reach (P5) | `ComputeAbilityRangeCells`; handler `GetCellsInRange()` |
| **Hover a move cell (ghost)** | Path, ghost, pass-by; **basic-attack reach from the ghost tile**; enemy threat arcs; follow zone for John/Mark in ghost style, with their committed zone hidden (G2); for other movers, the coverer's zone icon on the destination (G4) | `AttackReachFrom` (shared); handlers' `GetCellsInRange(origin)` |
| **Ability picked** | Ability range (#2); hover: targeted, affected area, push, damage, approach | `ComputeTargetSelectionCells`; `ComputeAffectedCells`; `AttackReachFrom` for the approach |
| **Hover the role badge** | That unit's zone, emphasised, on the role layer (P1) | Handler `GetCellsInRange()` |
| **Shift held** | Every Bergson's zone; info panels | Handlers |
| **Shift + hover a Bergson** | Its zone emphasised (P4); its move layer (none if selected); basic-attack reach from its tile | `GetReachableCells`; `AttackReachFrom` |
| **Shift + hover an enemy** | Move layer and danger zone (reach + ready attacks) in enemy tints; intent cells | `GetReachableCells`; `AttackReachFrom` over reachable cells |
| **John's role prompt** | Arc tether John → covered allies | `handler.Targets` |

Two sources only: **role cells** come from the handlers; **attack cells** come from `AttackReachFrom` (or `ComputeTargetSelectionCells` for the live target pick, which it matches).

## 5. Lens notes

**Creative.** *Target experience:* the board shows the family keeping watch, in one visual vocabulary. Each Bergson's own icon means "I've got this tile", whether on the zone, on the move destination or in the HUD. John's arc is a protective gesture, not a debug wire. *The moment:* enemy turn, the game pauses on John's prompt, and a warm orange arc leaps from his head to Lucy's with a small shield landing over her. The press feels like catching her. Across a run, players should stop reading icons and start reading the family.

**Systems.** Rules above. Levers: tether width 0.015, alpha 0.7, arc height 1 + 0.15/cell; focus scale 1.15; follow-zone alpha 0.5; Shift tints (G3); reach cache until the next state change. Failure cases: preview ≠ action (fixed by one reach helper; any future attack-geometry flag must go through it); performance of ranged reach (profile < 2 ms); a zone hidden by the P5 equality check when it later differs (self-correcting by design); hover gate killing hover over world-space panels (gate screen-space canvases only).

**UX.** What the player clicks doesn't change. Likeliest misreads after the change: (1) reading "no red on a Bergson under Shift" as "safe" (mitigated by the enemy-only red danger zone, G3); (2) a "missing" Linda/Lucy zone on selection (mitigated by the tooltip line); (3) the tether as a threat (mitigated by colour and the shield cap). Where the lenses disagree: P7. UX would keep full reach for Bergsons; I side with THJ's current-tile proposal plus the tint split, because the ghost already answers "from there".

## 6. USP check

- **Family Roles: strengthens.** One icon language for roles across grid, move preview and HUD; the whole-family view no longer collapses on hover; the tether becomes a readable family beat.
- **Synergies: neutral.** No synergy rule or preview changes.
- **Duos: neutral, slightly safer.** Duo previews keep their shared bools; the badge no longer erases the Mark–John shout cells.
- **Home: neutral on purpose.**

## 7. Critics

- **UX critic, strongest point:** P7's "current tile only" for Bergsons gives Shift two meanings, and players may read the missing red as safe. *Done:* kept THJ's proposal, but split the meanings by tint (G3, tied to D-072) and made it Q4. Also adopted: emphasise rather than alpha-dim (P4); the follow zone gets a ghost style (G2); a tooltip line for the hidden zone (P5); a shield cap and colour so the tether isn't read as a threat arc (P2). Rejected: moving cover icons to the cell's bottom centre (my draft). Replaced by G4, which reuses each coverer's own quadrant icon.
- **Systems critic, strongest point:** correct ranged-reach geometry is far costlier (a loop over the whole grid per origin, per enemy, per hovered tile). *Done:* cache plus a 2 ms profile gate in the tech plan. Also adopted: never pass `source:` into the helper (`GridCell.cs:827`); a non-core Bézier helper that the threat arc can share later; equality from the committed cell only; a bus event instead of a `FindAnyObjectByType` coupling (Q2); ready-only filtering recomputed per Shift press. Their correction: my `ComputeTargetSelectionCells(originOverride)` warning is true for the non-shape path, but `ComputeAttackRangeFromOrigin` never uses that path (L1401-1402), so the helper is safe to build from it.

## 8. Recommendation and order of work

| Step | What | Kind | Core? | Size |
| --- | --- | --- | --- | --- |
| 1 | `AttackReachFrom` helper in `UnitThreatAnalysis`, cached; Shift and threat arcs use it (P3) | Bug | No | M |
| 2 | Ghost icons use it (P6); approach preview calls it instead of its private copy | Bug | **Yes**, `PlayerController` (Tier 2 bugfix) | S |
| 3 | Grid hover gate over screen-space HUD (G1) | Bug | **Yes**, `GridManager` (behaviour change, Tier 3: THJ's OK) | S |
| 4 | Badge hover → role-zone layer, focus style (P1) | Bug / design | Only if Q2 = bus event (additive, D-068 pattern) | S |
| 5 | Shift model: Bergson current-tile reach, no move layer on the selected unit, enemy danger zone, new tints (P7, G3, D-072) | Design | No (`ShowStatsHoverPreview`, `GridCell.ShiftPreview.cs` constants are in a core partial: tint values only) | S-M |
| 6 | Focus instead of narrow (P4); P5 equality hide + tooltip line | Design | No (`RoleZoneRules`, `RoleZonePresenter`, `UnitPanelUI`) | S |
| 7 | Follow-zone ghost style and committed-zone hide (G2); cover icon = coverer's quadrant icon (G4) | Design | No (`MovePreviewCoverPresenter`; `GridCell.CoverIcon.cs` falls out of use) | S |
| 8 | Tether arc (P2) with the shared Bézier helper | Design | No (optional later: `GUnit.ShowThreatLineTo` switches to the helper, own core commit) | S |
| 9 | Dense-board play check (G9); profile | Verify | — | XS |

Tests: EditMode for `RoleZoneRules` focus output, the P5 equality rule, and (if a test grid can be built) the gap case and Dash straight-line reach. Then the full EditMode suite (`AIRegressionTest.Baseline_MatchesCurrentAI` stays known red).

**Playtest signal.**
- *Worked:* THJ hovers Linda across a gap and sees the icon where she can shoot; Shift on John shows only lines he can really dash; no one asks "which zone is this?"; the tether is described as "John reaching for her", not as a line.
- *Failed:* "where did Linda's zone go?" (then switch P5 to option C); "I thought I was safe" after Shift on a Bergson (then switch P7 to option A for Bergsons); stutter on hover (cache or reach cost).

## Questions for THJ

**Q1. P4: replace D-064's narrowing with focus?**
Context: Shift + hovering any Bergson hides the others' zones (`RoleZoneRules.cs:34-42`).
Options: A keep narrowing; B all zones stay, the hovered one enlarged at full alpha; C never narrow.
Recommendation: B.
Blocked: step 6.

**Q2. P1: how does the HUD badge reach the zone presenter?**
Context: the badge must stop drawing sword icons and ask the role-zone layer instead.
Options: A additive bus event `onFamilyRoleBadgeHover(GUnit, bool)` (core, additive, reviewed like D-068); B a public method on `RoleZonePresenter`, found by a cached lookup (no core change, hidden coupling, breaks silently across scene reloads with domain reload off).
Recommendation: A.
Blocked: step 4.

**Q3. G1: gate grid hover when the pointer is over the screen-space HUD?**
Context: hover ignores UI today (`GridManager.cs:149-175`), so previews fire under panels. This is likely P1's main cause. Core behaviour change.
Options: A gate on screen-space HUD canvases only; B gate on any UI (risks a dead board under world-space panels); C leave as is.
Recommendation: A, as its own commit.
Blocked: step 3.

**Q4. P7: what does Shift show for attacks?**
Context: after the geometry fix, reach + attack still covers most of the map for Linda.
Options: A reach + attack for everyone; B Bergsons: basic-attack reach from the current tile, enemies: danger zone (reach + ready attacks) in its own red tint; C current tile for everyone.
Recommendation: B (your proposal, plus the tint split).
Blocked: step 5.

**Q5. P5: hide Linda's and Lucy's own zone on selection?**
Context: their zone equals their basic-attack reach by data. The duplicate shows only while their attack range is drawn, not at idle.
Options: A as is; B hide on selection when equal (runtime check), Shift still shows it, tooltip line "Same tiles as her attack"; C hide only while their attack range is drawn; D an Inspector bool per handler (core, additive).
Recommendation: B.
Blocked: step 6.

**Q6. P2: tether style?**
Context: the tether is 5× thicker than the threat arc, straight, opaque, on Overlay.
Options: A chain at foot level (needs a chain sprite, occluded by units); B thin translucent arc over the heads, threat-arc geometry and material, John's orange, small shield cap at the ally; C keep, only thinner.
Recommendation: B.
Blocked: step 8.

(G2 ghost-style follow zone, G3 tints and G4 cover icon = quadrant icon are Tier 3 visual changes too. They ride on approval of this plan as a whole unless THJ wants to rule on them separately.)

## Risks

- P1's root cause is inferred, not reproduced: run the two-minute repro before step 4.
- Ranged-reach performance (step 1): cache and profile.
- The hover gate may block hover over world-space UI: restrict it to screen-space canvases; play check.
- The `thj/fr-readability` merge is in progress: line numbers here are from the working tree on 2026-10-19 and may shift.

## Gates

Compile / EditMode tests / review (steps 2, 3 and 4 touch core) / play check: yes (dense board, gap map, John's prompt, Shift on Linda and on an enemy) / docs below.

## Docs to update if approved

- `design/gdd/family-systems.md`: role-zone display rules (selected, Shift focus, P5 hide, cover icon = quadrant icon, tether).
- `design/gdd/combat-rules.md`: the Shift view (Bergson vs enemy attacks, tints).
- `decisions.md`: new rows for Q1 to Q6 (Q1 supersedes D-064's narrowing; G4 changes D-067's icon, not its rule).
- `glossary.md` (narrative agent): a player name for the enemy "danger zone" if Q4 = B.
