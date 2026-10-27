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
