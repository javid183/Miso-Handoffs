# Play check: Mark's Catch & Return with a prompt

Branch thj/linda-quiver. Setup: a level with Linda and Mark, the Mark and Linda synergy unlocked, Mark two or more tiles from Linda and on the line of her shot, an enemy beyond Mark and another one beside Linda's line of flight home.

1. Shoot an arrow along the line through Mark. Expect the arrow to stop at Mark's edge and the catch prompt to open. Nothing past Mark is hit while the prompt is open.
2. Press the prompt in its window. Expect "+1" on Linda at once, Mark turning towards Linda, and the frozen arrow staying visible in Mark's hand until the catch animation's hit frame.
3. After the hit frame the arrow in Mark's hand vanishes and a return arrow flies from Mark to Linda. It stops at Linda and does not overshoot her.
4. During step 3, Linda's action stays in progress (no input, no turn end) until the return arrow arrives. Enemies standing on the way home are hit once by it.
5. After a press, nothing past Mark (the enemy beyond him) takes damage, and the original arrow does not fly on. Count the quiver: it is back at full, one arrow, not two.
6. Shoot again and let the prompt run out without pressing. Expect the same arrow to carry on past Mark with its remaining range, hit the enemy beyond him, and land on the board as usual (the quiver stays one short until pickup). No "+1" cue.
7. Shoot again and press, with a catch animation that cannot reach its hit frame (for example temporarily set the apply frame on Mark's catch component to 99). The return flight must still start after about one second.
8. Start the prompt, then kill or deactivate Mark while it is open (a cheat, or an enemy with a reaction). Expect the arrow to carry on and land normally; Linda's action must not hang.
9. Press the prompt, then kill Mark before the animation's hit frame. Expect the return flight to start at once and Linda's action to finish when it ends.
10. Catch twice (two turns). The second catch behaves like the first: no stuck frozen arrow, and no leftover hidden LindaAttackArrowReturn(Clone) object in the scene hierarchy after a decline.
11. Check that the arrow stops at Mark visibly (it may sit at the edge of his collider, not his centre) and that the stop looks acceptable.
12. Check that the arrow does not open Mark's prompt a second time as it leaves after a decline.
13. When the return arrow reaches Linda's cell, Linda takes no damage.
14. While the original arrow is hidden after the apply frame, it stays hidden (its Animator does not show the sprite again).
15. Balance: the return arrow hits enemies on the way home with falloff starting again at full strength. Note whether the damage feels right.
16. With a slow-motion effect running (for example the reactive interrupt during Watch), open the catch prompt: the prompt must not change the time scale before or after.
17. Leave Play mode, or end the level, while the prompt is open or the catch animation plays: no errors in the console.

## Play findings fixes (catch at low frame rate, return on Linda's body, freeze at Mark, Lucy)

Setup as above, plus Lucy with an enemy inside her zone that is Linda's aimed target beyond Mark. To get a low frame rate in the editor: Window > Analysis > Profiler, turn on Deep Profile and Record while in Play mode; the Game view's Stats overlay should show well under 15 fps. Turn it off again for the normal-rate steps.

18. Low frame rate: shoot through Mark ten times. Every shot must open the catch prompt at Mark (none flies through him without a prompt). Nothing beyond Mark is hit while the prompt is open.
19. Low frame rate, press: the return arrow stops on Linda's body (about her chest, her target point), not at her feet and not past her. Repeat at normal frame rate: same end point.
20. The frozen arrow sits in Mark's hand (the catch point, the same spot the return arrow starts from), not at the edge of his collider. At low frame rate too, even when the arrow had already passed him that frame.
21. Decline at both frame rates: the arrow jumps back onto its line (a small jump is expected), carries on facing forward (no one-frame flip), hits the enemy beyond Mark and lands. The prompt does not open a second time as it leaves Mark.
22. Lucy, caught arrow: Linda shoots at an enemy in Lucy's zone beyond Mark; press the catch, with no enemy on the way home. Lucy does not follow up (the aimed enemy took no damage).
23. Lucy, caught arrow with a hit on the way home: as 22 but with an enemy in Lucy's zone between Linda and Mark, hit by the return flight. Lucy follows up on that enemy.
24. Lucy, real hit: let the prompt run out (or shoot with no Mark on the line) so the arrow hits the aimed enemy in her zone. Lucy follows up on it, as before.
25. Lucy, regression: John, Mark and Toba attacks that damage an enemy in Lucy's zone still get her follow-up; an attack that does no damage (fully blocked, or a status only) does not. Note any ally action that used to get a follow-up and no longer does.
