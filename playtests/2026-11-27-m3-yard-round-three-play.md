# Hold the yard round three: THJ's play check (2026-11-27)

Build: plan `plans/2026-11-27-m3-yard-round-three.md`, report `reports/m3-yard-round-three.md`. THJ played it, then asked to log the findings without fixing them and to commit what is built. Not yet planned. Each needs a look before building; 5 and 6 may touch AI (core: THJ's OK first).

1. **Walk-in idle run.** In the arrival sequence the heroes walk together; the one who arrives first keeps playing the run animation in place until the last one arrives. (`MoveUnitsTogetherSequence`: each walker should go to idle on its own arrival.)
2. **Fresh turn after the arrival.** After the arrival sequence, reset the turn and the heroes' AP: the fight starts on a fresh family turn.
3. **Shrine light off.** When the sword (DR) is picked up, switch off the light at the top of the Shrine art. (The pickup raises no event today.)
4. **No Masher in the bottom-right lane.** Remove the east Masher (hidden, came in at the push). The lower lanes are for dark enemies only; the west-corridor Masher is the only one.
5. **Barricades only when blocked.** Enemies should not target the barricades when their way to the family is open.
6. **Mashers don't approach.** Mashers don't come at the players; they walk one tile back and forth, or don't move at all. (Seen earlier: the stuck Masher, core walk fix D-758; the Queen idle walk, D-716.)

Also still open from the build: Toba's call line before the rush is a placeholder (narrative pass). Review and verifier have not run (THJ plays first).
