# Verify: Playtest Batch 1 (B1, B3, B6, B8)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md    Agent: miso-verifier    Branch: thj/oct-build-fixes
Result: PARTIAL (quiet checks done; every in-game criterion Not run)

## Why partial

This session has no computer-use tools (no screenshot, click or key tool). I could not drive the Game view. I did not enter Play mode and did not guess any in-game result.

## Compile

Clean. Unity MCP `read_console` (error, warning) returned only CS0108/CS0114/CS8509/CS8524/CS0168 warnings (pre-existing style) and no errors.

## Tests (EditMode, via Unity MCP run_tests)

- Job a183d14f7f7f40aa9b0cd2020c79f64f: total 79, passed 78, failed 1, skipped 0 (7.8 s).
- Failure: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red, 35 of 704 checks; graph node/edge counts changed). Does not fail the gate.
- Note: the total is 79, not the ~447 recorded on 2026-10-16 via command line. The MCP run may filter to a subset (an assembly or filter default). Not investigated. The new tests (`AbilityAnimationSafetyTests`, `FillBarTextFormatterTests`, `InputLockTests`) are in the tree; I did not confirm by name that they were in the 79.

## Acceptance criteria

### B1 Mark's Cleanse (C1, C2)
- Cast Cleanse in In My Father's Arms, cell clears, no `ability animation state is missing` error: **Not run: needs a play session (desktop app)**.
- Static evidence (quiet): `AC_Playable_Mark.controller` (loaded in the editor via execute_code) now has state `SoulSacrifice` with clip `SoulSacrifice`. `Unit_Mark.prefab` overrides: `abilities[4].animationData.stateName = SoulSacrifice`, `abilities[4].abilityActivationFrame = 5`. The other slots' states (PrimaryAttack, Run, Vault, Command) all exist in the controller.
- Safety net (optional throwaway edit): **Not run**. Needs Play. The decision logic has an EditMode test (`AbilityAnimationSafetyTests`, commit 952ab9d5a); see the note above on whether it ran.
- John's Cleanse timing: **Not run: needs a play session (desktop app)**.

### B3 HP never reads 0 while alive (C3)
- **Not run: needs a play session (desktop app)**. Commit 66481e4e1 adds `FillBarTextFormatter` with `FillBarTextFormatterTests`; a one-line change in `UI_Element_FillBar.cs`.

### B6 Map mission panel (C4)
- **Not run: needs a play session (desktop app)** (16:9, 16:10, 4:3 on world map and mission map).

### B8 Tutorial input lock (C5)
- **Not run: needs a play session (desktop app)** (all five steps). Commit 01e561ad2 adds `InputLockSet` with `InputLockTests` (159 lines).

### B5 diagnostic
- Not in scope; `[B5-DIAG]` lines not checked (Home scene not visited).

## Bugs found

None (nothing was played).

## New findings

- The active scene reported by `manage_scene get_active` is unnamed (no path, not dirty), so the editor did not have `PreloadScreen` or another saved scene open when I started. Nothing was changed.
- The MCP test total (79) is far below the 447 recorded for the command-line run; worth checking what the MCP run covers before relying on it as "all tests".

## What I could not verify

All in-game behaviour: B1 cast and safety-net error line, B3 HP text, B6 panel at three ratios, B8 clicks/keys during a tutorial and restore afterwards, turn-change and enemy-introduction cases. These need the Claude desktop app with computer use.

## Branch

thj/oct-build-fixes (not switched; read-only git only).

## Save reset

No.

## Editor state at end

Edit mode, Play never entered, no scene or prefab edited, nothing saved or left unsaved by me.

## Editor checks corrections

- Unity MCP is available and works for compile state (`read_console`), EditMode tests (`run_tests` + `get_test_job`, ~10 s) and scratch inspection (`execute_code`, CodeDom/C# 6). This is a quiet route that needs no computer use. The `get_test_job` output with failed tests can be huge; it is saved to a file and must be read with a script.
- Confirmed: this terminal session had no computer-use tools, so play checks were Not run.
