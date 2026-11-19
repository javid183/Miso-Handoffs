# Cyclone round 3 + Masher fix: THJ play check list (branch `thj/cyclone`)

Everything is built, reviewed and uncommitted (C1 alphas, C2 cast on an enemy, C3 beats and input lock, a review fix round, the Masher core fix). EditMode 2174 run, only the known AI red failing (count 43). Mark each item OK / not OK with a note. Round 2's list ([`2026-11-17-cyclone-round2-play-check.md`](2026-11-17-cyclone-round2-play-check.md)) is still unmarked; play it in the same session. Setup: a level with Lucy, Linda, a few Claws, and a Masher or the Goblin Queen (`LevelE3-C1`). Start from PreloadScreen (normal flow), not TestLevel.

## A. Masher walks through the Cyclone (the bug)

1. `LevelE3-C1`: Linda [8,-1], Cyclone [10,-2], Masher starts [12,-2]; Linda shoots it to [11,-2]. Its counter now steps onto the Cyclone, bursts it (one hit on the Masher and on each enemy beside it), and ends there. The Cyclone is gone. No second counter answers the burst.
2. Masher speed 1 ends two cells from Linda, so no slam from that spot: note how it reads.
3. Goblin Queen: her walk and charge may end on the Cyclone and burst it once; her jump never lands on it and never bursts it.
4. A Claw (non-heavy) still can't enter the Cyclone. Family units still walk through it and can't stop on it.
5. Mark's Command moving a heavy enemy onto the Cyclone bursts it (combo, by the rule). Note if it feels wrong.
6. The AI's intent preview for a heavy won't show it ending on the Cyclone (known gap).

## B. Cast on an enemy

7. Aim the Cyclone: the range highlight lights only castable cells (new: family, ally, planted and other occupied cells are no longer lit). Is that clear or confusing?
8. Hover a Claw 2 to 3 cells away: the cross at that cell, the Claw's ghost one cell further from Lucy joined by a tether, damage (3) and lethal skull on the ghost if it kills, hazard ring if the landing cell has a hazard; plus ghosts for what the Whirl pulls.
9. Hover a Claw right next to Lucy: castable (disengage and wall). Cast it: the Claw is flung one cell back, the Cyclone stands between you, the Whirl hits it. Does this become the only thing you use the Cyclone for?
10. Diagonal neighbour of Lucy: the Claw goes to the free one of the two cells, else along the row. The ghost shows it before the click.
11. Refused: a Claw with a wall, unit or planted entity behind it (away from Lucy); a Masher, Queen or other large/Immovable enemy; an ally or neutral. Hovering a refused enemy shows the normal unit panel.
12. Hover a castable enemy: no unit hover panel, no attack cursor while aiming. Cancel (right click / Esc): every ghost, tether and damage segment goes.
13. Shove onto a hazard (spikes, pool): fires on landing. Shove into Linda's lane: Watch answers. (Known: one Watch per action, the shove may take it.)
14. Empty cells still castable as before; Super Time still picks empty cells.

## C. The beats (feel)

15. Whirl with a pull: short swell, then the pull, then the enemies still standing beside the Cyclone lean in (inhale), snap back and take the hit as they arrive. Units that already moved this action (carried, shoved, pulled) don't lean again; heavies jolt outward, not in. Reads as wind, not a pawn?
16. Whirl with no pull: no extra wait versus before. End-of-turn Whirl: does the enemy turn feel slower? (Measured: +0.1 s with a pull, plus 0.06 s recoil after the hit, so about +0.16 s on the turn switch.)
17. Steer with riders: grab (riders lean in), drag (riders trail, the front enemy is kicked ahead), fling to the landing cells (stops exactly on the ghost's cell, no overshoot). The cast-on-enemy shove uses the same fling.
18. No input during the breath: clicking or pressing keys between the inhale and the hit does nothing; the lock releases when the hit lands. Round 2 item 25 (act right after a Steer) still holds; pause key is blocked only during the breath. Level end mid-beat: nothing sticks (drawings back on their cells, input free).
19. Combat log and Watch order unchanged: carried units land (Watch, hazards), then the pull, then the hit.

## D. Fainter cross drawings

20. The cross tint, arm-tip chevrons and flare are fainter (tint 0.18, chevron 0.45, flare 0.85) but the pull still reads and the hazard ring stands out. Tune on the runtime instance's `CycloneCrossView` fields (lasts one Play session); tell me the values you want baked in.
21. The cross view's own swell still eases over 0.2 s while the Cyclone swell is now 0.1 s before a pull: does the drawing lag the beat?

## Known gaps, not bugs

- Placeholder sprites; the lean depth (35% of a cell inhale, 30% grab) and times are start values to tune.
- If Lucy is destroyed mid-fling (scene teardown), the shoved enemy's hop offset isn't restored (low risk).

## THJ's play feedback, 2026-11-19 (after `main` was merged in)

THJ stopped the list here: the Cyclone has become too complex to predict. Screenshots in `playtests/img/`.

1. **Row of Dark Claws** (`2026-11-19-cyclone-1-row-of-claws.png`): four Claws in a row ahead of the Cyclone. The intuitive move is to steer the Cyclone along that row, through them, breaking the formation, with the Claws pushed to the row above or below. Today it can't go through them.
2. **Can't steer at all** (`2026-11-19-cyclone-2-cannot-steer.webp`): Cyclone with a Claw on the cell above and family around it; no Steer is offered. Feels very wrong.
3. **No idea what a move will do** (`2026-11-19-cyclone-3-unclear-move.webp`): Cyclone with Claws beside and above; THJ couldn't tell what moving it would do.

**THJ's direction:**
- The rules have lost their simplicity. Go back to the original problems that caused the redesign, solve only those first, then add fun on top with a minimal approach.
- Proposal: the Steer runs through enemies, damaging them as it passes; on its final cell it pushes away any enemy standing there (to any free cell if the natural one isn't free); then, still, its usual Whirl: pull and damage.
- Drop the side drag; only drag the enemies against the direction of the pull (designer to confirm what that should mean).
