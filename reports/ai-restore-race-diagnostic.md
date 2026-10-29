# Report: AI restore race diagnostic (temporary)

Plan: coordinator brief for `lucy-cant-target-after-shield-dash` (THJ approved D-312), no plan file    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done (compile checked offline; EditMode run and play check left to THJ)

A temporary diagnostic, not a fix. It stays uncommitted and is removed after THJ plays.

## What changed

- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIFactionBrain.cs` (core, AI): logs `[AI-RESTORE-RACE]` warnings in `PredictAllTargets`. It records where the simulation left each unit and checks the live cell twice: before the unit's own simulation and at restore. It also stores the request frame in `RequestPredictAllTargets` (main thread) and adds the `DiagLogRestoreRace` helper. +42 lines, none removed.
- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.cs` (core, AI): new `internal GridCell DiagLastSimCell`. It is cleared at the start of `PredictNextTargets` and set in `ApplySimAction` when the simulated `SimMoveTo(dest)` succeeds. The return value was discarded before, so capturing it changes nothing.

Every added line carries `// TEMP diagnostic: remove after the restore race is confirmed` (or sits in a block that starts with it). No private IDs. Both files keep CRLF; `AIFactionBrain.cs` keeps its BOM, and `AIUnitBrain.cs` still has none.

## The exact warning

One line per hit, built in `DiagLogRestoreRace`:

```
[AI-RESTORE-RACE] {Nickname} (turn order {TurnOrder}) was moved outside the AI target prediction, detected {phase}. Saved cell {saved}, simulation expected {expected}, live cell {live}. The restore forces it back to {saved} in the grid logic while its sprite stays where it was moved. {thread}, {frame}.
```

- `{phase}`: `at restore` (the case the brief asked for: the live cell isn't the cell the simulation last put the unit on) or `before its own simulation` (see Decisions).
- Cells print as `(x, y)` from `GridCell.Coordinates`, or `none`.
- `{thread}`: `AI worker thread (id N)` on the worker, otherwise `thread '<name>' (id N, not the AI worker)`.
- `{frame}`: on the worker, `prediction requested on frame F`, where F is `Time.frameCount` saved on the main thread when the prediction was requested. Off the worker it adds the live `frame N`. `Time.frameCount` is never read on the worker.

Example of the expected hit for the logged bug:
`[AI-RESTORE-RACE] Archer Goblin (turn order 3) was moved outside the AI target prediction, detected at restore. Saved cell (11, 0), simulation expected (11, 0), live cell (12, 0). The restore forces it back to (11, 0) in the grid logic while its sprite stays where it was moved. AI worker thread (id 42), prediction requested on frame 18231.`

## Acceptance criteria

- [x] Detects the case: at restore, `!ReferenceEquals(unit.CurrentCell, expected)`, where `expected` is the cell the unit's own simulation last moved it to, or the saved cell when the simulation never moved it. The simulation moves only the unit being simulated (`AIUnitBrain.ApplySimAction` is the only `SimMoveTo` besides the restore), so any other cell means something outside the simulation moved the unit.
- [x] Logs the unit name, saved, expected and live cell, the thread, and a frame number (request frame on the worker). See above.
- [x] Worker-safe: the new code reads only plain managed fields (`GUnit.Nickname` is the serialized `title` string, `TurnOrder`, `GridCell.Coordinates`) and uses `ReferenceEquals` for the cell checks. The only Unity-object calls are the `unit && cell` checks the restore loop already made. `Debug.LogWarning` is thread-safe. Allocations: one small dictionary per prediction (not per loop step); the strings are built only when the warning fires.
- [x] No behaviour change: the restore line `if (unit && cell && unit.CurrentCell != cell) unit.SimMoveTo(cell, true);` is untouched. `SimMoveTo(dest)` in the simulation runs exactly as before; only its return value is now read.
- [x] AI regression: `AIRegressionTest` not touched. No test calls `PredictAllTargets`, `RequestPredictAllTargets` or `PredictNextTargets` (grep), and the change only adds logging, so decisions can't move. Needs THJ's EditMode run to confirm (only the known red `Baseline_MatchesCurrentAI` allowed).
- [x] Compiles: offline Roslyn compile of `Assembly-CSharp` (Unity's own rsp, output to scratch, the editor not touched) has 0 errors. The rsp is from 01:23, so I appended the two newer runtime partials of the pause-frame fix. No editor recompile or EditMode run yet: the editor is open, so batch Unity was off limits.
- [ ] Race confirmed: needs THJ's play (below).

No new EditMode test: this is temporary logging, removed after the play check.

## Save reset

No.

## Decisions I made

- **Second check, "before its own simulation".** The brief's restore-time check misses one ordering. If the push re-plugs the enemy after the cells are saved but before its own simulation starts, and its simulation then moves it, the live cell equals the simulation's cell at restore: no warning, yet the restore still drags it back to the old cell. The check before each unit's simulation catches that. Same prefix, different phase text. When the simulation doesn't move the unit, one race can log both phases. Logging only; same behaviour.
- **"Expected" comes from the unit brain** (`DiagLastSimCell`), not from reading `CurrentCell` after the simulation. Reading `CurrentCell` would hide a push that lands during the unit's own simulation.
- **Frame number:** `Time.frameCount` is read only on the main thread (stored when the prediction is requested). It isn't reliably callable off the main thread, so the worker never reads it.
- **Inline edits, not partial files:** neither class is `partial`, and making them partial for a temporary log would be a bigger, longer-lived change. Removal is a plain file restore (below).

## Needs THJ

None for building it. After the play: confirm whether the warning showed up (see "What a hit means").

## Docs to update

- `status.md` (`lucy-cant-target-after-shield-dash`): diagnostic built, uncommitted, waiting on THJ's play.

## Risks and loose ends

- **The window is narrow.** A hit needs the push to re-plug the enemy (`GridCell.PlugEntity`, main thread, once per tile, at the end of each tile's lerp) while the worker is inside `PredictAllTargets`, which usually takes a few ms. "No warning in a few tries" is weak evidence; use the repro boosters below.
- **Other movers can also trigger the warning.** Any main-thread move during a prediction would fire it: a Masher step, a knockback, a pull, a summon pushing out. That is the same bug class (the restore clobbers a real move), so a hit from another source still counts as evidence, but say which ability it was.
- `AEffectPusher.MoveEntity` unplugs the unit at the start of each tile but leaves `CurrentCell` on the old cell until the plug. So during a lerp the occupancy slots are empty while `CurrentCell` is unchanged, which the diagnostic can't see. The restore's `SimMoveTo(old, force)` also re-fills the old cell's slot that the push had just emptied. That is a separate inconsistency for the fix plan.
- Noticed, not touched: in `AIUnitBrain.ApplySimAction`, `sim.Origin = dest` is set even when the simulated `SimMoveTo(dest)` fails.
- `AIUnitBrain.cs` has leftover merge-marker comments (`// <<<<<<< HEAD` around `PredictNextTargets`). Pre-existing, harmless, not touched.

## Proposed commits

None. This diagnostic must not be committed.

**Removal**, once THJ has played. Neither file had other uncommitted changes when I started (`git status` at the start of the session), so a restore is clean:

```
git restore -- miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIFactionBrain.cs miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.cs
```

That discards changes, so it needs THJ's yes. Stop Play mode first, and run `git diff --stat` on the two files to check that only the diagnostic is in them. Without git: delete every line marked `TEMP diagnostic`, the `DiagLogRestoreRace` method and the `{ }` braces added around the `originals.Add` loop, and put back `_unit.SimMoveTo(dest);` in `ApplySimAction`. Then `grep -rn "TEMP diagnostic\|AI-RESTORE-RACE\|DiagLastSimCell\|diagExpected" miso/Assets/_Project/Core/Systems/AISystem` should find nothing.

Keep the pause-frame fix (`EntityAnimationHandler`, `RuntimeAbility` and their new partials and tests) out of this: it is separate and untouched.

## Other branches

None (temporary).

## How to see it

Setup:
1. Stop Play mode, then Ctrl+R to recompile. Check the Console has no compile errors.
2. Optional: Test Runner > EditMode > Run All. Only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` is allowed.
3. In the Console search box, type `AI-RESTORE-RACE` so only hits show. Leave warnings visible and Collapse off.

Cheapest repro (the logged case), "Ryker is lost" level 3:
4. Leave several enemies alive. Prediction time grows with the number of AI units and their abilities, and a longer prediction is a wider window.
5. With John, Shield Dash into an enemy so that its push moves the target, ideally more than one tile. Each tile is one re-plug, so each tile is one more chance.
6. Straight after, act with Lucy so her Family Role follow-up fires, as in the original log. Every finished ability fires `abilityPerformed` → `UpdateFutureTargets` → a new prediction job. The worker runs jobs one after another, so a second job starts later and is more likely to overlap the push's last tile.
7. Then try Lucy's basic attack on the pushed enemy. A warning plus "can't target it" is the bug.

Booster, best first:
- **Deep Profile.** Window > Analysis > Profiler, tick Deep Profile, press Record, then do steps 5 and 6. Deep profiling instruments all managed code, the AI worker included, so `PredictAllTargets` runs many times slower and the window grows to match. Turn it off afterwards (it makes the editor slow).
- A low frame cap (for example 10 fps) helps much less. The push still re-plugs a tile at about the same real time (the lerp is `Time.deltaTime * speed`), and the prediction's length doesn't depend on the frame rate. It mostly makes the plug land in bigger steps. Use it only if Deep Profile isn't practical.

What a hit means:
- An `at restore` or `before its own simulation` warning naming the pushed enemy confirms the race: the restore put it back on the saved cell while its sprite sits on the live cell.
- After a warning, Lucy's clicks on the sprite should hit whatever logically sits on the live cell (in the log, the Cyclone on (12,0)), matching the original bug.
- No warning after several boosted tries makes the race unlikely, and the cause of `lucy-cant-target-after-shield-dash` should be looked for elsewhere.

Send the Console lines (or the `CombatLogs/` file) back for the fix plan.
