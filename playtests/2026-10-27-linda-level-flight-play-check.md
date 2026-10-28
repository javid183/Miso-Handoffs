# Play check: Linda's level arrows and the catch point

For THJ, 2026-10-27. Branch `thj/linda-quiver`; the change is uncommitted. Decision D-278; report `reports/linda-level-flight.md`.

## Before playing

1. Let Unity recompile and send me any errors.
2. Run Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. The new tests are `LevelFlightWiringTests` and `CatchPointRulesTests`.

## Steps

1. **Bow, all four directions.** Fire left, right, up and down. The arrow flies level, with no dip toward the floor.
2. **Landing.** A shot that hits nobody lands on the last tile in range, never one past it. A shot that hits lands on the last enemy hit. The aim marker shows the same tile in both cases.
3. **Upward misses at two frame rates.** Fire up at an empty column several times at about 60 fps, then at about 30 fps (cap it with `Application.targetFrameRate` or check the Game view stats). Repeat for down, left and right. The arrow must land on the end-of-range tile every time.
4. **Watch.** Let an enemy step into her lane. The Watch arrow flies level and lands as in step 2.
5. **Both arrow Duos** (Linda–Lucy, Linda–Toba): level flight, and the arrow lands at the end of the line.
6. **Crescendo:** it still arcs, and its marker sits on the aimed tile.
7. **Catch, pressed.** Put Mark in line with the shot, at least 2 tiles from Linda. The arrow stops in front of him at its own height, with no jump up and no V in the trail. The return arrow leaves from that exact spot and ends on Linda.
8. **Catch, declined.** The arrow carries on from where it stopped and lands as usual.
9. **Low enemies.** On horizontal shots, check that small or low enemies still get hit: the arrow now flies a little higher (about 0.19 to 0.245).
