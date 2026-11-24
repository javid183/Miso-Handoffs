# M1 (The Ridge) play check, 2026-11-23

Scope `thj/onboarding-demo`. Played by THJ on `GB_m1-ridge` as built in 3.1b (`3bf3e14ba`).

## Finding

THJ did not like the level. The Masher was stuck on its tiles with no way out.

## THJ's rough rework (input for the redesign, not final)

THJ edited `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab` (uncommitted in the shared repo as of 2026-11-23). It is a rough first try. Enemy placement in it is a test and a placeholder: both enemies and tiles can be replaced. Coordinates below are in THJ's edited prefab (they include negative rows); the designer should tool-read the edited prefab before drawing anything.

## The beat order THJ has in mind

1. Mark and Linda arrive where they stand and see something in the distance (the search scenery).
2. Linda rushes to search it ("I'll check it out"), Mark warns her to be careful, and Linda runs to 3,-2. The camera shakes, a stone falls on 5,-5 (no tile there; maybe on other tiles too), sealing the two of them apart, and 3 lower Dark Claws appear.
3. The enemy turn begins and the Claws rush Linda.
4. Linda's Family Role tutorial is shown, then she can activate it.
5. The player's turn begins with only Mark selected. He has to take out the wounded Claw on 7,-2 and ends up there. Mark's FP should be 2, so he can't jump to 5,-2.
6. Then it is Linda's turn. She can attack the remaining Claws, and if she does, that triggers Catch & Return.
7. A short narrative beat reacts to it.
8. HP potions: introduce them the first time HP gets low after this, since they may be needed. The level can start with an HP potion available.
9. The rest of the level is up to the designer: change and tweak it, reuse the same pattern as a challenge, or suggest better ideas. The designer may also suggest improvements to THJ's beats 1 to 8.

THJ also said the Masher is no longer a must-have: remove it from the level, or keep it if the designer finds a use for it.

## Open points for the designer to raise

- Beat 2 says the stone falls "between John and Mark", but M1 is Mark and Linda. Check the roster in THJ's edited prefab, and ask THJ if it's still unclear.
- D-638 (Mark starts on 3,2) came from the old layout. THJ's prefab sets the new start positions.
- Beat 5 needs a level-scoped FP cap of 2 for Mark, or a starting FP value. Check whether an existing level rule covers it before proposing code.
- Beats 2, 4, 5 and 7 need sequences: a scripted move, a camera shake, a falling-rock spawn, a mid-level enemy spawn, a selection lock to Mark, and a trigger on Catch & Return. Map each beat to the existing sequence and wiring tools, and list any that need new code.
