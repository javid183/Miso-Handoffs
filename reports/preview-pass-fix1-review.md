# Review: preview-pass play fixes, units 3 and 4 (per-tile sword icons; PlayerController targeted occupant)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **APPROVE**. Must fix: none.

Should fix (sent back to the implementer before commit): `GridCell.cs` `PlugEntityInternal` (~L756) and `UnplugEntity` (~L804) refresh only the anchor, so an attack icon already showing on a non-anchor tile keeps a stale sorting layer when a multi-cell occupant moves on or off or dies. The Shift copy has the same issue. Fix: loop over the footprint cells and reapply the icon sorting.

Notes:
- The redirect removal is correct and set and clear stay balanced per cell. The icon renderers are siblings under the overlay root, so they stay at their tile. Nothing else relied on the redirect for the attack icon.
- On the Shift layer the attack part is set per cell, and the move frames still wrap the footprint.
- `DynamicTop` exists. Every `SetInAttackRange` caller (PlayerController ghost, area and occupant; the Mark–John duo) is per cell and fine.
- PlayerController: correct, minimal, no double marking. It mostly restores the pre-Aug-26 per-footprint loop, but skips the whole occupant if the area already marks any of its tiles. That fits "one icon per covered tile"; switch to the per-tile skip if THJ wants the whole boss marked when targeted. It's a core file the brief didn't name, so it gets its own commit (a Tier 2 core bugfix, flagged to THJ).
- Pre-existing, out of scope: a repeat `SetInAttackRange(true)` doesn't render the override sprite swap; the shared bool lets a hover clear erase a duo icon on the same tile.
- No statics, no serialized changes, AI unaffected, encoding kept, and the commit split compiles in order.
- Play check: the Masher Goblin (2×2), Goblin Queen (1×2) and Mountain Deev (3×2) icons should draw above the boss and below the target counter, and should not cover neighbouring units badly.
