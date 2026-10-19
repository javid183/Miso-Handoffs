# Editor checks

Owner: coordinator. How a session checks a change in THJ's Unity editor: compiles, logs, tests, play checks. The verifier works from this file. Written 2026-10-16 by the setup session from what was on disk and past Build Log runs; **lines marked *(unconfirmed)* get checked on the first real verifier run (Pilot 2) and fixed here.** House rules (stop Play before editing scripts, test paths) are in `CLAUDE.md`.

## Is the editor open?

- If `miso\Temp\` exists, assume the editor is open. A crash can leave it behind; if unsure, ask THJ. Also check `tasklist | grep -i unity` and the end of the Editor.log (a clean shutdown line means it is closed). Seen on 2026-10-16: `Temp\` was present, then absent at the next run, with no Unity process.
- The command-line test run can't start while the editor has the project open.

## Compile

- **Trigger:** in the editor, Ctrl+R (Assets > Refresh). A compile and domain reload takes about 60–80 s on this project (Playtest Plan). Stop Play mode first. The command-line route (editor closed) took 63 s for the whole EditMode suite of 447 tests including about 16 s of compile (confirmed 2026-10-16; `CompileScripts:` and `error CS` patterns in the log worked).
- Whether Auto Refresh is on (Preferences > Asset Pipeline) isn't stored in the project, so don't count on saves compiling by themselves *(unconfirmed)*.
- A session without computer use can't press Ctrl+R itself: ask THJ to, then read the log.

## Logs

| Log | Where | What to look for |
| --- | --- | --- |
| Editor log | `C:\Users\javid\AppData\Local\Unity\Editor\Editor.log` (the previous editor session: `Editor-prev.log`) | Compile errors are `error CS####` lines; a finished compile and reload writes `CompileScripts: <ms>` and `Domain Reload Profiling: <ms>`. Runtime exceptions and the Home sim's `[Home …]` lines land here too, with full stack traces |
| Command-line run | the `-logFile` you pass (put it in the scratchpad) | Same content as the Editor log, for that run only |
| Combat logs | `C:\Users\javid\AppData\LocalLow\Dead Mage\miso\CombatLogs\` (`Application.persistentDataPath`); one `.log` and `.jsonl` per fight, named `<yyyyMMdd-HHmmss>_<Level>` | What happened in a fight; levels that used a cheat are tagged `CHEATED`. Format: `tech/combat-log.md` |

Read the end of the Editor log after the time you triggered the compile; older errors from earlier in the session don't count.

## EditMode tests

- **Editor open:** Window > General > Test Runner > EditMode > Run All. The results show in the window; a session without computer use asks THJ for the pass/fail counts and the names of any failures *(unconfirmed: whether the run also leaves a results file on disk)*.
- **Editor closed:** the command line in `CLAUDE.md` (Unity 6000.3.4f1 path, `-testResults` and `-logFile` in the scratchpad). The full EditMode run took about 53 s on Oct 4. Read the NUnit XML: totals on the root `test-run` element, failures as `test-case` elements with `result="Failed"`.
- The only accepted failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, until its dedicated fix lands.

## How the editor is driven

- **Quiet checks** (compile result, logs, command-line tests) need only files on disk. Any Claude Code session can do them.
- **Clicks and keys in the editor** (Ctrl+R, Test Runner, Play mode, playing the game) need computer use. Past play checks (Oct 13 and 14) were driven by Claude with computer use from the Claude desktop app, reading the Console from the Editor log.
- Practical rules from those runs (details in `playtests/playtest-plan.md`, "Setup and rules"): start Play from `Scenes/PreloadScreen.unity`; click the Unity toolbar before pressing keys if the Claude window has focus; the Claude desktop window can cover the top-right of the Game view, so clicks there never reach Unity; leave the cursor mid-screen in the Home scene (the screen edge scrolls the camera); hover a unit's feet for the K cheat.

## Desktop-only limit for play checks

- Play checks need computer use, which is available only in the **Claude desktop app**, not in a terminal Claude Code session *(unconfirmed for this account and version)*.
- A verifier running from the terminal does quiet checks only. It marks every criterion that needs Play **"Not run: needs a play session (desktop app)"**, and the coordinator puts the play check under "Waiting on THJ" in `status.md`.
- A play check also takes over THJ's editor: it runs only after he agrees to a time (see the verifier's rules).

## Unity MCP (confirmed 2026-10-18)

- The `unity` MCP server (`.mcp.json`, `http://127.0.0.1:8080/mcp`) reaches subagents (implementer, verifier); the coordinator session did not list the tools. Quiet checks work without computer use: `read_console` (pass `types` as a JSON list, e.g. `["error","warning"]`), `manage_scene` (`get_active`), `refresh_unity`, `run_tests` then `get_test_job` (about 10 s for the whole EditMode suite), `execute_code` (scratch checks such as instantiating prefabs without saving). Failed-test output from `get_test_job` is huge and is saved to a file: read it with a script.
- `manage_editor` has no read action; read Play state from `mcpforunity://editor/state`.
- Suite size depends on the branch: on `thj/oct-build-fixes` (= `main`) the EditMode suite is 79 tests (counted from the `[Test]` attributes on 2026-10-18); the 447 seen on 2026-10-16 included the Home tests of `thj/home-test`. On `thj/fr-readability` the full suite ran 175 tests on 2026-10-19 (about 52 s through the Unity MCP). With the Unity MCP: `refresh_unity` returns while still compiling, so poll `mcpforunity://editor/state` before reading the console; `get_test_job` can time out once on `wait_timeout`, so call it again.
- Clicks and keys in the Game view still need computer use (desktop app). The 2026-10-18 verifier run had none, so every in-game criterion was "Not run".

## Play-check notes (2026-10-18, desktop session)

- The toolbar level picker (Tools row: dropdown plus the ▶ button) loads a level straight from PreloadScreen and shows an "Assign Placeholders" dialog (choose the squad). *In My Father's Arms* is `LevelE3-C1`.
- `Tools > Save Data > Clear Save Data` resets the save so play-once tutorials replay (the save is `...\AppData\LocalLow\Dead Mage\miso\SaveData.json`).
- Cheats seen working: `[` (-1 HP) and Shift+`[` (-10) on the hovered unit, K wins the fight. F11 and F12 didn't react. The hover panel doesn't refresh after cheat damage until the cursor leaves and returns.
- Maximize the Game view (double-click its tab) to read small numbers; a custom "4:3 Aspect" entry was left in the Game view size list.
