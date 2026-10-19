# Playtest notes: grid previews (2026-10-19, THJ)

Source: THJ's play session on `thj/fr-readability` after the role-zone icons (D-075, `a7e28f0f4`). Task: `preview-pass` (status.md). Scope: `all`. THJ is merging `thj/fr-readability` into `main` and starting a new branch, so code work lands there.

## Raw notes (THJ's words, lightly trimmed)

1. John's FR ability on the HUD previews different tiles than his shield-icon role-zone tiles.
2. The line drawn from John to the person he is shielding with his FR is too thick, looks like a debug line, and draws over everything. It should have a curve like the line drawn between enemies and the player when the movement preview shows. Either a chain from under John's feet to under the target's feet, or a thin curved line with some transparency from above his head to above the target's head.
3. John's sword icons (his reachable attack range, shown while holding L-Shift on him) seem to include unreachable tiles.
4. Holding L-Shift shows every member's role zone, until you hover over the selected character. Then everyone's zone is hidden except the selected character's. Intentional?
5. For Lucy and Linda, the attack range is exactly their role zone, so the same tiles are always shown twice. It's a duplicate and should not be shown while they are active, only during L-Shift.
6. Linda's movement preview does not show the sword icon (attack reach) across a gap in the tiles. With her ghost on tile (2,4), there's no attack icon on (4,4) if tile (3,4) doesn't exist, although she can attack it from there.
7. L-Shift doesn't need a sword icon on every tile the unit can reach and attack. It covers most tiles and becomes redundant (Linda covers the whole map). Showing it on the tiles attackable right now from the current tile is enough; the move preview already redraws the sword icons from the ghost tile.

## Structured problems (coordinator)

| # | Kind | Problem | First guess (unverified) |
| --- | --- | --- | --- |
| P1 | Bug, consistency | Two sources disagree on John's role tiles: the HUD ability preview and `RoleZoneRules` / `RoleZonePresenter` | Each computes the tiles separately (the ability's targeting vs the role handler's zone). One source of truth needed |
| P2 | Visual, game feel | John's tether line (`JohnTetherPresenter`, B4 R5) reads as debug: too thick, straight, on top of everything | Restyle: a curve like the enemy-threat lines, thin and translucent above the heads, or a chain at foot level, with correct sorting |
| P3 | Bug, likely | Shift attack reach (sword icons) includes cells John can't actually reach | Reach = move range ⊕ attack range, possibly ignoring blocked or occupied cells, AP, or path cost |
| P4 | Rule question | Shift plus hovering the selected unit narrows the view to that unit only (D-064 says "hovering one Bergson with Shift held shows only that zone") | Matches D-064 as written; THJ is asking whether it should. Design call |
| P5 | Redundancy | Lucy's and Linda's role zones equal their attack range, so the selected-unit zone duplicates the attack highlight | Hide the role zone for the selected unit when it equals what's already drawn; show it on Shift only |
| P6 | Bug | Linda's ghost (move preview) attack icons don't cross gaps in the grid, though a real attack from that tile can | The preview's reach walks connected cells (pathing) where the real attack uses distance or line |
| P7 | Redundancy | Shift draws sword icons on every reachable-and-attackable cell, which is most of the map for Linda | Show only "attackable now from the current tile"; the move-preview ghost covers the rest |

## Ask to the designer

A UI/UX pass over all grid previews (see status `preview-pass`).
