# GDD mirror sync, 2026-10-20 (manual)

Copy each block into the "Miso — Game Design" Claude Doc. Source commits in `claude-handoff`: `6c35455`, `6bf3440`. Links to repo files stay as paths.

## Tab: Family systems

### 1. Header line (top of the tab): replace it with

```markdown
Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); [Role zones on the grid](#role-zones-on-the-grid) read from `thj/preview-improvements` @ `f5d263743`, 2026-10-20 · Mirror: Claude Doc "Miso — Game Design", tab Family systems · Up: [Overview](overview.md)
```

### 2. New section: insert after the Family Roles section's "Source:" paragraph, before "Duos"

```markdown
### Role zones on the grid

A role zone is the set of tiles where a Bergson's Family Role can answer (each handler's own range). The zones are display only: nothing here changes when a role fires. "Built on the branch" means built on `thj/preview-improvements`, not yet merged to `main` ([Branch differences](#branch-differences)). Of those, THJ has confirmed in play only the items marked "play-checked" (the D-087 and D-088 fixes); the rest wait for the C9 play check ([`playtests/2026-10-20-preview-pass-play-check.md`](../../playtests/2026-10-20-preview-pass-play-check.md)).

- **FR-8.** Each Bergson's zone is drawn with its own icon, tinted with its role colour, in a fixed quadrant of every tile in the zone (of the footprint box when a multi-tile unit stands there), so four zones on one tile never overlap (D-075). Icon, quadrant and colour are set per unit on its role handler (table below). The colours are the ones set on the unit prefabs, THJ's own choice (D-091): John dark brown, Mark near-black, Lucy dark red, Linda at the code default. `showRoleZone` off hides that unit's zone, its cover marker and its tether (D-063, D-067). *Built*
- **FR-9.** When a zone is shown (D-064, D-077, D-087):
  - the selected Bergson's zone, except as FR-10 says;
  - holding Shift: every living Bergson's zone;
  - Shift and hovering a Bergson that has a zone: only that zone. Hovering Toba, an enemy or an empty tile keeps every zone;
  - hovering a unit's role badge (on the unit panel's Family Role icon): that unit's zone, drawn like the others, whether it is selected or not, with or without Shift.

  *Built.* Shift narrowing: on the branch, play-checked (D-087 restores `main`'s rule after D-076 was tried). Badge hover: on the branch, not play-checked.
- **FR-10.** Without Shift, the selected Bergson's zone is not drawn when it is the same tiles as its basic-attack reach from the tile it stands on, leaving its own tiles out of the comparison (D-080). Today that hides Linda's and Lucy's. A zone that is only the unit's own tiles is never hidden, and the check applies to player units only. Shift and the badge hover still show it. While the check holds, the role badge tooltip adds the line "Same tiles as the basic attack; Shift shows them." (D-084). It is checked live, so if a run upgrade ever makes the zone differ from the attack, the zone comes back by itself. *Built on the branch, not play-checked*
- **FR-11.** Follow zone: while the player previews a move for any Bergson, its current zone is hidden and its zone is drawn from the ghost tile instead, in the normal style (D-082). The follow zone is skipped when it equals the basic-attack reach from the ghost tile (the FR-10 test), because the ghost's sword icons already show those tiles ([Combat rules](combat-rules.md) CR-37), so Linda and Lucy show no zone during a move preview. Other Bergsons' zones don't move. The current zone comes back on cancel, commit, death and turn end. *Built on the branch, not play-checked* (to check in play: whether the old zone flashes during the walk after a commit)
- **FR-12.** Cover marker: while the player previews a move for any other unit, the destination tile shows the coverer's own zone icon in its own quadrant, at full opacity (D-082): John's shield if the destination is in John's zone, Mark's fist only if every tile a melee attacker could hit the destination from lies in Mark's zone (D-067: ranged attackers don't count, and with no such tile there is no fist). Both are measured from where John and Mark stand now. A unit never covers itself. *Built on the branch, not play-checked*
- **FR-13.** John's tether: while John's role prompt is up (the game is paused), a thin arc in his role colour runs from John's head to the head of each ally he would cover, with a small shield (his zone icon) at the ally's end, drawn just above both units' sprites (D-081, D-088, D-089). It goes when the prompt ends (press, decline or expiry); an ally who dies or leaves the grid loses its arc. Values below. *Built on the branch.* Visible: play-checked; the cap over tall units: not yet.

| Bergson | Icon | Quadrant | Colour (RGBA) |
| --- | --- | --- | --- |
| John | `ShieldOutline` | Top left | 0.35, 0.24, 0.12, 0.75 |
| Mark | `PunchOutline` | Top right | 0.09, 0.04, 0.01, 0.75 |
| Linda | `BowArrow` | Bottom left | 0.34, 0.71, 0.91, 0.75 |
| Lucy | `Fireball` | Bottom right | 0.70, 0.14, 0.14, 0.75 |

| Tether value | Value |
| --- | --- |
| Width | 0.025 world units |
| Opacity | 0.85 |
| Arc | Quadratic curve, 16 samples; control height 1 + 0.15 per tile between John and the ally (radial), so the peak is half that above the chord |
| Anchors | Each unit's head (its `ThreatLineRenderer` point, 0.8 above the pivot) |
| Look | Plain unlit material (`Sprites/Default`); the threat arc's `M_LineShine` turned John's colour near-black (D-088) |
| Draw order | The units' sorting layer, one above the highest sprite of John and that ally; the cap one above the line |
| Cap | John's zone icon, 0.25 world units wide |

Source: `Unit_<Name>.prefab` (role handler: `roleZoneSprite`, `roleZoneSlot`, `roleZoneColor`, `showRoleZone`; the code defaults in `<Name>FactionRoleHandler.cs` differ for John, Mark and Lucy), `Resources/GridOverlays/*.png`, `Core/Systems/RoleZoneSystem/Runtime/` (`RoleZoneRules.cs`, `RoleZonePresenter.cs`, `RoleZoneAttackMatch.cs`, `MovePreviewCoverPresenter.cs`, `CoverIconRules.cs`, `JohnTetherPresenter.cs`), `Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs`, `Features/UI/Panels/Scripts/RoleBadgeState.cs` and `UnitPanelUI.RoleBadge.cs`. How it is wired: [`tech/combat-architecture.md`](../../tech/combat-architecture.md) "Grid previews".
```

### 3. Branch differences: add this bullet at the end of the list

```markdown
- **On `main` (until `thj/preview-improvements` merges):** the role badge hover draws the zone as sword icons instead of FR-9's zone icons; no zone is hidden for matching the attack (FR-10); only John and Mark have a follow zone, drawn opaque, with their current zone still showing (FR-11); the cover markers are separate shield and fist icons in the lower left and lower right instead of FR-12's quadrant icons; and the tether is a straight, opaque line on the Overlay layer (FR-13).
```

### 4. Open questions: add after Q11

```markdown
12. **Q12.** Answered by THJ (D-091): the prefab role colours are his own edits and stay (John dark brown, Mark near-black, Lucy dark red, Linda at the code default), superseding D-066's note on Mark's and Linda's colours (FR-8).
```

### 5. Related: replace the first two bullets (Decisions, Plan) with

```markdown
- Decisions: D-008, D-010, D-034 to D-042, D-048; role zones D-063, D-064, D-066, D-067, D-075, D-077, D-080 to D-082, D-084, D-087 to D-089, D-091 (D-076 reversed by D-087; D-066's colour note superseded by D-091)
- Plans: [`plans/2026-10-16-ap-points-model.md`](../../plans/2026-10-16-ap-points-model.md); role zones [`plans/2026-10-18-family-role-phase0-1.md`](../../plans/2026-10-18-family-role-phase0-1.md), [`plans/2026-10-19-preview-pass-design.md`](../../plans/2026-10-19-preview-pass-design.md), [`plans/2026-10-19-preview-pass-tech.md`](../../plans/2026-10-19-preview-pass-tech.md)
```

## Tab: Combat rules

### 1. Header line: replace it with

```markdown
Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets and core scripts read from the live project); [Grid previews and the Shift view](#grid-previews-and-the-shift-view) read from `thj/preview-improvements` @ `f5d263743`, 2026-10-20 · Mirror: Claude Doc "Miso — Game Design", tab Combat rules · Up: [Overview](overview.md)
```

### 2. New section: insert before "Attacks and damage" (after the movement section's "Source:" paragraph)

```markdown
## Grid previews and the Shift view

The rule for previews: what a preview promises, the real action does. Role zones, follow zones, cover markers and John's tether are in [Family systems](family-systems.md#role-zones-on-the-grid). "Built on the branch" means built on `thj/preview-improvements` (read @ `f5d263743`, 2026-10-20), not yet merged to `main` ([Branch differences](#branch-differences)). THJ has play-checked only CR-38; the rest wait for the C9 play check ([`playtests/2026-10-20-preview-pass-play-check.md`](../../playtests/2026-10-20-preview-pass-play-check.md)).

- **CR-37.** Every preview of where an attack reaches uses the real attack's rules: its shape, straight lines only when the ability has them, the unit's whole footprint, and ranged reach across missing tiles (Linda's arrow crosses a gap). That covers the ghost's sword icons (basic-attack reach from the ghost tile), the approach preview (attack range from the tile the unit would walk to before attacking, CR-7), the Shift view and the enemy threat arcs. Abilities that preview an affected area keep that preview. *Built on the branch, not play-checked*
- **CR-38.** On a multi-tile unit, every tile in reach gets its own sword icon, drawn above the unit's sprite; hovering any of its tiles as a target marks all of them once. The move frame still wraps the whole footprint (D-088, D-089). *Built on the branch, play-checked*
- **CR-39.** Enemy threat arcs: while the player previews a move, a curved line runs from each enemy that could attack the ghost tile after moving, with any Attack ability, without area splash. Like the danger zone (CR-43), the arcs count any Attack ability ready on the enemy's next turn, so an ability with 1 turn of cooldown left draws an arc (D-085, D-090). *Built on the branch, not play-checked*
- **CR-40.** Grid hover stops while the pointer is over the on-screen HUD, and entering the HUD clears the hovered tile, so a ghost, follow zone or Shift preview never fires under a panel (D-078). Unit info panels over the board don't block hover. Clicks are unchanged. *Built on the branch, not play-checked*
- **CR-41.** Holding Shift shows details: info panels, every Bergson's role zone, and for the hovered unit a move and attack preview on its own layer, softer than and under the real highlights, so it never erases them (D-064, D-071). The preview is recomputed on each Shift press and hover, and isn't shown while the player is picking an ability target. *Built*
- **CR-42.** Shift on a unit that is not hostile to the player (Bergsons, the allied Toba, Deer): sword icons where its basic attack reaches from the tile it stands on, plus its move range, except on the selected unit, whose real move range is already drawn (D-079, D-086). *Built on the branch, not play-checked*
- **CR-43.** Shift on a unit hostile to the player: its move range and its danger zone, in enemy tints. The danger zone is every tile it could target after moving with any Attack ability ready on its next turn (cooldowns tick at the start of its turn, so an ability with 1 turn left counts), without area splash: the tiles it can aim at, not those caught next to a target (D-079, D-085, D-086). Its intent cells (its planned action) show as before. *Built on the branch, not play-checked*

| Shift tint | Bergson and allies | Hostile |
| --- | --- | --- |
| Move | Grey-teal (0.6, 0.8, 0.8) | Red-brown (0.7, 0.45, 0.4) |
| Attack | Warm white (1, 0.9, 0.75) | Strong red (1, 0.25, 0.2) |

On screen, each preview tile is the normal overlay colour moved 35% toward its tint, at 0.55 opacity, so the red is softer than its value. The tints sit outside the four role colours. If a tile holds both kinds, the Bergson tint wins. (To check in play: whether the tints read apart from Linda's blue and Lucy's red, and whether the enemy red is strong enough.)

Source: `Core/Interactions/Runtime/UnitThreatAnalysis.cs` (`AttackReachFrom`, `BasicAttackReachFrom`, `GetAttackableCells`, `GetThreateningEnemies`), `ShiftPreviewRules.cs` (`EnemyCooldownTicksAhead` 1, `EnemyIncludeAreaSplash` false), `ShowStatsHoverPreview.cs`, `PlayerController.cs` (ghost, approach, threat arcs), `Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (tints, `ShiftPreviewTintBlend` 0.35, `ShiftPreviewAlpha` 0.55), `GridCell.cs` (per-tile attack icons), `GridManager.HoverGate.cs`. Design and the full list of 23 previews: [`plans/2026-10-19-preview-pass-design.md`](../../plans/2026-10-19-preview-pass-design.md).
```

### 3. Branch differences: add this bullet at the end of the list

```markdown
- **On `main` (until `thj/preview-improvements` merges):** the ghost's sword icons stop at a missing tile; Shift and the threat arcs turn every Attack ability, straight-line ones included, into a diamond from every reachable tile, plus area splash, for Bergsons and enemies alike, in one blue and pink tint pair; the attack icons of a multi-tile unit sit on its anchor tile; and grid hover passes through the HUD (CR-37 to CR-43).
```

### 4. Open questions: add after Q9

```markdown
10. **Q10.** Answered by THJ (D-090): the threat arcs count attacks ready on the enemy's next turn (`cooldownTicksAhead: 1`), like the Shift danger zone, so the two agree (CR-39). Built on `thj/preview-improvements` in `d1254f7c8`.
11. **Q11.** "Danger zone" is a working name. It needs a player-facing name only if it ever appears as text (tutorial, tooltip). Glossary, narrative agent.
```

### 5. Related: replace the Decisions bullet with

```markdown
- Decisions: D-034 to D-038; previews D-064, D-071, D-072, D-078, D-079, D-085, D-086, D-088 to D-090
```
