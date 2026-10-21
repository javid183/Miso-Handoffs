# Masher reckless tank: play check

Branch `masher-tweak`. Plan: `plans/2026-10-20-masher-reckless-tank-tech.md` (decisions D-092 to D-117). Run after C5 is committed.

**Levels:** `Generic Levels/Easy/E3/LevelE3-C1.prefab` or `Generic Levels/Medium/M1/LevelM1-C3.prefab` (both have a Masher). The cheats help: F11 kills all, F12 goes to the next level.

Mark each item Pass, Fail (with what you saw) or Not run.

## Basics

1. The console has no "did not initialize its role ability" warning when the Masher spawns.
2. The Masher's unit panel shows a Family Role badge (the slam's icon and title). Is it OK to keep it, or should it be hidden on enemies?
3. Hovering the Masher while aiming an attack shows the preview:
   - the step ghost and path;
   - slam tiles only if it would end next to you;
   - the slam centred on the attacker's tile;
   - damage on every unit in the cross, goblins included.

## The counter (your turn)

4. **Melee bait.** Hit it from an adjacent tile. It slams your tile once, and the units around you are hit too, including goblins.
5. **Side of the cross.** Stand 2 tiles away on a side or back tile of its old cross and hit it with a ranged attack. It steps 1 toward you and does **not** slam unless it ends next to you.
6. **Ranged pull.** Hit it from 2, 4 and 6 tiles. Each hit drags it 1 tile toward the striker; it only slams when it ends next to them.
7. **Continuous Attack** (Mark): the answer comes once, after the whole action, from Mark's final tile.
8. **Approach and dash attacks:** the answer and the preview use the tile the attacker ends on.
9. **Duo, both partners striking:** it answers the partner who struck. On a tie, the one it can end next to and slam; on a further tie, the one who acted first.
10. **Last action of your turn:** the answer still plays before the enemy turn starts.
11. **Crippled** (Linda's Harmonic Slam): no step; it answers only if already next to the striker.
12. **Stunned** (Mark's Stunning Vault): no answer.
13. **Two answers in one turn:** the preview still shows on the second hover.
14. **Burn and Pass-by damage:** no answer.

## Reactions and the enemy turn

15. **John relays an answer** aimed at an ally within 2 tiles. Expected unclear: it may never have worked; report what happens.
16. **Linda's lane chain:** the Masher's step into her lane makes her shoot, and it steps again, until it is next to her.
17. **Mark's chain on the enemy turn, toggle ON** (default): an answer that hits an ally near Mark makes Mark punch, and the Masher answers again. The chain ends by FTP, a declined QTE, HP or reach, or is capped at 10 (a console warning).
18. **Same as 17 with `counterCanProvokeFamilyRoles` OFF** (Inspector on `Unit_MasherGoblin`): Mark and Linda don't react to its answers.
19. **Enemy-turn answer timing:** the answer comes after the current enemy unit's action, and the AI then moves the Masher sensibly from its new tile (no stale move into an occupied tile).
20. **2 × 2 target** (Big Ogre, if a level has both): the slam lands on the right tile.

## Regressions

21. A normal enemy turn without the Masher has the same pace as before (C1 holds and the AI recheck).
22. John's tether still hides while a family role plays, and no longer hides for the Masher's answers.
23. The other family roles (John, Lucy, Linda, Mark) still trigger as before.
