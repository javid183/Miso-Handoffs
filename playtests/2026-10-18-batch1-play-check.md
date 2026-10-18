# Play check: Playtest Batch 1 fixes (B1, B3, B6, B8, B5 repro)

Plan: `plans/2026-10-18-playtest-batch1-bugfixes.md`. Branch `thj/oct-build-fixes`. Needs THJ's time (it takes over the editor), so it runs only after he agrees a slot. Start Play from `Scenes/PreloadScreen.unity`. Quiet checks (compile, suite) are already green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

Commits under test: `7f85fbbf7` (C1), `952ab9d5a` (C2), `66481e4e1` (C3), `cabdb63a6` (C4), `01e561ad2` (C5), `47cee8ad9` (C6).

## B1 · Mark's Cleanse (C1, C2)

1. Load *In My Father's Arms* with Mark in the squad. Use a corrupted tile.
2. Cast Cleanse with Mark. **Pass:** the cast plays (John's sprites are expected, placeholder), the corrupted tile clears, the turn goes on, the console has no `ability animation state is missing` error.
3. Safety net (optional, needs a throwaway edit): set Mark's slot 4 `stateName` to a name that doesn't exist, cast again. **Pass:** one error in the console naming ability, unit and state; the ability still resolves; combat doesn't freeze. Revert the edit (don't save the prefab).
4. Cast John's Cleanse once, to confirm the same frame timing as before.

## B3 · HP never reads 0 while alive (C3)

1. In any fight, get an enemy to very low HP (the K cheat or repeated hits).
2. **Pass:** hover panel, unit panel and the mission character icons show 1 or more while the enemy lives, and 0 only when it is dead. Damage preview still shows the expected future HP.

## B6 · Map mission panel (C4)

1. Open the world map and select a mission; repeat on the mission map.
2. In the Game view try 16:9, 16:10 and 4:3. **Pass:** the whole panel is on screen at each ratio, and at 4:3 it doesn't hide map content you need. Known: at 21:9 the world map panel overshoots about 46 px (not fixed, out of scope).

## B8 · Tutorial input lock (C5)

1. Play Level 1 until a tutorial panel opens (also one that opens mid player turn).
2. While it is open try: left click on a tile and a unit, right click (cancel), Switch, Toggle, Pause key. **Pass:** none of them act; the camera doesn't move.
3. Close the tutorial. **Pass:** the unit's turn continues with the same input as before (move/attack work).
4. If a tutorial fires at a turn change, **Pass:** after it closes the new turn's input works and nothing is stuck.
5. Open an enemy introduction fight (first sight of a new enemy) with a tutorial in the same level. **Pass:** input works after both.

## B5 · Workshop repro (C6, diagnostic)

Steps and how to read the logs: `reports/playtest-b5-workshop-diagnostic.md` ("What the logs print"). Filter the Console on `B5-DIAG`, Collapse off. Send the lines back. B5 is not fixed by this commit.

## Report

Verifier writes `reports/playtest-batch1-verify.md` (template `templates/report.md`): each criterion Pass, Fail or Not run, with the console lines as evidence.
