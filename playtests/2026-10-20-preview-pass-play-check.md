# Play check: grid preview pass (C9)

Branch `thj/preview-improvements` (C1–C8 committed 2026-10-19/20; hashes in `plans/2026-10-19-preview-pass-tech.md`). Plan C9. Your notes P1–P7: `playtests/2026-10-19-preview-notes.md`. Tick, or write what you saw.

## Your seven notes

- [ ] **P1 badge:** select John, hover his role badge, first with the badge over empty screen and then with it over board cells. Both show his zone icons (shield, top-left) on the same tiles. No sword icons, and no ghost or follow zone under the HUD.
- [ ] **P2 tether:** on John's role prompt (enemy turn), a thin orange arc runs from John's head to each covered ally's head, with a small shield at the ally's end. It isn't drawn over everything, and tall units don't hide the cap. Does the arc's shine animate while the game is paused? (Either is fine.)
- [ ] **P3 John's dash:** Shift on John shows only what his basic attack reaches from his tile. Hover an enemy with a straight-line attack: no diamond.
- [ ] **P4 focus:** hold Shift. Every Bergson's zone stays, and hovering one enlarges its icons without hiding the others, including when you hover the selected unit.
- [ ] **P5 Linda/Lucy hide:** selected Linda or Lucy without Shift: no zone icons on their attack tiles. Their badge tooltip ends with "Same tiles as the basic attack; Shift shows them." Shift shows the zone again. (If the zone still shows, the hide didn't fire: tell me.)
- [ ] **P6 gap:** Linda's ghost on a tile with a missing cell between it and an enemy in her lane. The sword icon appears beyond the gap, where her real attack can hit.
- [ ] **P7 Shift icons:** Shift on a Bergson: sword icons only from its current tile; no Shift move frames on the selected unit, while other Bergsons still have them. Shift on an enemy: move frames plus a red danger zone covering its ready attacks.

## New behaviour to look at

- [ ] **Follow zones:** preview a move for each of the four Bergsons. John's and Mark's zones are drawn from the ghost tile and their current zone is gone. Linda and Lucy show no zone during the preview (their sword icons from the ghost cover it).
- [ ] **On commit:** does the old zone flash for the length of the walk? (Known; there's a cheap fix if it's noticeable.)
- [ ] **Cover marker:** preview a move for Lucy into John's zone: John's shield icon on the destination, top-left. Into Mark's zone with every melee spot covered: Mark's fist, top-right. With Shift held, does the cover icon sit cleanly on top of John's or Mark's own zone in the same corner?
- [ ] **Allies:** Shift on allied Toba in Level1-C3 and on a Deer in a Level2 map. Bergson colours, no red danger zone.
- [ ] **Masher Goblin:** its role badge tooltip doesn't have the "Same tiles…" line.
- [ ] **HUD gate:** move the pointer from the board onto the HUD. The hover frame, ghost and Shift preview clear, and come back when you leave. Unit info panels over the board don't block hover. The boss health bar does (as the HUD does).
- [ ] **Tints:** do the Shift colours read apart from Linda's blue and Lucy's purple? Is the enemy red strong enough? (The blend lever is `ShiftPreviewTintBlend`, 0.35.)
- [ ] **Dense board:** four Bergsons with overlapping zones next to enemies. Do the move frames hide the zone icons? (If they do, the fix is to raise the zone layer.)
- [ ] **Feel:** any hitch on Shift-hovering an enemy (1.3–3.9 ms measured on test grids)?

## Report back

Write what you saw here or in chat. The coordinator files bugs and follow-ups.

## THJ's first results (2026-10-20)

- P2/C8: John's tether arc is not visible at all.
- P4/C6: the D-064 narrowing (hover under Shift shows only that unit's zone) was better: reverted by D-087.
- Sword icons don't show on the tiles a multi-tile enemy stands on.

## THJ's second results (2026-10-20)

- Confirmed in play after the fixes (`590f0a3c2`, `eddb34e7c`, `3cd8bba21`, `f5d263743`): the Shift narrowing is back, John's tether arc is visible, and sword icons show on every tile of a multi-tile enemy.
