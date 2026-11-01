# Report: FP 0/0 in sandbox levels, plus Play hardening

Plan: `plans/2026-10-31-fp-zero-regression.md`. Branch `thj/onboarding`. Implementer: miso-implementer. 2026-10-31.

## Root cause (with evidence)

The family time points pool is sized in `FactionTracker.InitializePoints` from the sum of the FP attribute of `MissionTracker.ActiveMission.MissionRoster.Units`. An empty roster gives `FamilyTimePoints` 0/0, so the bar shows 0/0 and anything that spends FP (Family Roles, pass-by) cannot run.

A level no mission lists plays in a sandbox mission (`Mission.CreateSandbox`). The sandbox roster was only filled from the placeholder picks (`LevelFastForwardRoster.ApplyToMission`, `Pending`). A `GB_` level places its player units directly (no placeholders), so nothing was picked and the roster stayed empty (`freeSlotsCount` 0).

Evidence, measured in Play from the toolbar loader (`EditorLevelLoader.LoadLevel`):

| Level | Path | Result |
|---|---|---|
| `Level2-C2` (listed in "Into the Rootwell") | real mission, roster John/Linda/Lucy | FTP 10/10 for all, both before and after a sandbox run |
| `GB_24-nook` (before fix) | `__sandbox__`, `units=0 free=0` | Linda, John, Lucy all `ftp=0/0` |
| `GB_24-nook` (after fix) | `__sandbox__`, `units=3` | Linda, John, Lucy `ftp=10/10` |

Every authored mission roster resolves to real units (checked all 20 Mission assets; the ones with null entries are free-slot missions that rely on the placeholder window). The branch did not change `FactionTracker`, `FamilyTimePoints`, `Mission`, or the roster classes (`git diff main` over Core runtime shows only `LevelBase.cs` and the PlayModeStaticReset line besides editor code and the uncommitted AI files).

Introducing commit: `32f532e49` (the loading fix). Before it, `LoadLevel` refused any level not listed in a mission, so `GB_` levels could not be played from the toolbar at all; the sandbox existed on main (`50558f9e1`) but with that gate it was effectively unreachable for these levels. `32f532e49` opened the sandbox to unlisted levels and exposed that its roster was only placeholder picks. The grid-built levels (`24bfcea3e`, `652f2075e`) and the toolbar dropdown (`29cad27cb`) are what made THJ reach it. The onboarding rosters (`bb9982c87`, `38bc7db73`) are not the cause.

Note on "all levels": I could not reproduce 0/0 on a listed level (`Level2-C2`) through the toolbar path, even after a sandbox run. The Hearth/River/Ridge/Trail rosters resolve fine too. If a listed level still shows 0/0 for THJ, I need the level name and the entry route (see play check below). Possible race: the play-hardening below covers a lost fast-forward key, which would fall through to the main menu rather than show 0/0.

## Changed files

- `miso/Assets/_Project/Core/Levels/Runtime/LevelFastForwardRoster.cs` (editor-only code, `#if UNITY_EDITOR`): the sandbox roster is now the player-faction units the level places (mapped back to their source unit prefabs) plus any picked for placeholders, one per unit name. New `ComposeSandboxRoster`, `FindPlacedPlayerUnits`, and a static `_sandboxPlacedUnits` list, reset in the existing `ResetPlayModeStatics` (already called by `PlayModeStaticReset`). Real missions keep the old behaviour.
- `miso/Assets/_Project/Core/Levels/Runtime/LevelBase.cs` (Play hardening): `EnterPlay` now writes the two fast-forward EditorPrefs right before `isPlaying = true` via a small `WriteFastForwardPrefs`; the `ExitingEditMode` handler still writes them and `EnteredEditMode` still tears down.
- `miso/Assets/_Project/Core/Levels/Editor/LevelFastForwardRosterTests.cs` (+ `.meta`): new tests.

No core-system behaviour changed. No temporary logs were added. A temporary EditorPrefs key I used while diagnosing was deleted.

## Tests added

`LevelFastForwardRosterTests` (4): placed units fill the roster; placed then picked is one entry per unit name and drops nulls; nothing placed or picked is empty; a sandbox roster assigned to free slots lists every unit.

EditMode full suite: 1131 run, 1130 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).

## Verified in Play (via Unity MCP)

- `Level2-C2` from the loader: real mission, FTP 10/10, before and after a sandbox run.
- `GB_24-nook`: 0/0 before the fix, 10/10 for the three units after.
- Not verified: Family Roles and pass-by themselves (they spend FP, which now exists); the hardening race (cannot be forced); main menu to mission flow; the other four `GB_` levels; sandbox restart keeping FP.
- No save reset was needed.

## Needs THJ's play check

1. Play `GB_24-nook` and `GB_m1-linda` (Linda-only) from the toolbar: bar shows full FP, Family Roles and pass-by work, and a restart keeps FP.
2. Play a listed level (`Level2-C2` or a Hearth level) and a normal mission from the main menu. If any shows 0/0, tell me the level and route.

## Proposed commits

1. `fix(levels): sandbox levels size the family time points from the player units they place`
   - `miso/Assets/_Project/Core/Levels/Runtime/LevelFastForwardRoster.cs`
   - `miso/Assets/_Project/Core/Levels/Editor/LevelFastForwardRosterTests.cs`
   - `miso/Assets/_Project/Core/Levels/Editor/LevelFastForwardRosterTests.cs.meta`
2. `fix(levels): write the quick-load keys right before entering Play`
   - `miso/Assets/_Project/Core/Levels/Runtime/LevelBase.cs`

THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*`, the TMP fallback font asset) were not touched.

## Risks and loose ends

- A sandbox level with a placed player unit and a placeholder pick of the same name counts once.
- Placed enemies or allies of other factions are not added; only the player faction.
- `level-tools.md` says the sandbox roster is "whoever the level places"; that is now true. No doc edit made.

## Fix round (after review)

Changes, all from the review:
1. Stale keys: `LevelBase.cs` has an `[InitializeOnLoadMethod]` that deletes the two fast-forward keys when Play is not starting or running, so a refused Play or a recompile can't leave them for the next ordinary Play.
2. Test seam: `LevelFastForwardRoster.ApplyToMission(Mission, placed, picked)` is public; the old one-argument form calls it with the sandbox's placed units and the pending picks. The test now calls the seam on a sandbox mission with nothing picked (replaces the hand-written assign test).
3. Placed units are found with `GetComponentsInChildren<GUnit>(false)`, so inactive ones don't count.
(a) `OnPlayModeChange` skips the `EnteredEditMode` teardown and unsubscribe when `EditorApplication.isPlayingOrWillChangePlaymode` is true.
(b) `LevelFastForwardRosterTests.cs` is now LF.

Verified: recompiled clean; EditMode 1131 run, 1130 passed, only `AIRegressionTest.Baseline_MatchesCurrentAI` red. Play: `GB_24-nook` from the loader shows John, Lucy, Linda 10/10; after stopping, the keys are empty and the PreloadScreen is open; an ordinary Play then reached the main menu (no fast-forward). Not verified: forcing the stale `EnteredEditMode` race, and a refused-Play recompile.

Final files (paths under `miso/Assets/_Project/`):
- Commit 1 (`fix(levels): sandbox levels size the family time points from the player units they place`): `Core/Levels/Runtime/LevelFastForwardRoster.cs`, `Core/Levels/Editor/LevelFastForwardRosterTests.cs`, `Core/Levels/Editor/LevelFastForwardRosterTests.cs.meta`
- Commit 2 (`fix(levels): write the quick-load keys right before entering Play`): `Core/Levels/Runtime/LevelBase.cs`
