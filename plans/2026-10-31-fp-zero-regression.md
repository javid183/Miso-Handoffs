# FP 0/0, Roles and pass-by dead in every level (and Play hardening)

Size: S–M (unknown until the cause is found)    Tier: 2 for a fix in this branch's own changes; Tier 3 (THJ) if the fix needs a core change beyond the hardening    Assigned to: `miso-implementer` → `miso-reviewer` → THJ play check
Branch: `thj/onboarding`. Status: **done 2026-10-31**, committed `fa6af3fab` (sandbox roster fix + `LevelFastForwardRosterTests`), `08cdf7035` (Play hardening). Review APPROVE + fix round; EditMode 1130/1131 known red only; THJ play-checked OK (GB levels and a normal mission)

## Report (THJ, 2026-10-31, latest playtest)

Every level shows the family time points bar as `0/0`, and Family Roles and pass-by don't work. Not tied to one level or to Linda playing alone (a Linda-only level shouldn't be 0 either). Seen on `GB_24-nook` (sandbox, toolbar) in THJ's screenshot; "all levels" per THJ.

## Do

1. Reproduce: a `GB_` level from the toolbar (sandbox), an old wired level from the toolbar/inspector (e.g. `Level2-C2`), and if possible the normal flow (main menu → a mission). Note which paths show 0/0.
2. Find the cause and the commit that introduced it. Suspects on this branch: the onboarding C1 rosters (`FactionTracker.InitializePoints` builds the FTP pool from the mission roster), `LevelStartFPFiller` (`units[0].Faction.Controller`) and the grid builder's rebind, the sandbox mission's roster (`Mission.CreateSandbox`, `LevelFastForwardRoster.ApplyToMission`), and today's loading fix (`32f532e49`: the level id / prefab path capture, the saved-asset swap). Compare with `main` if useful (`git diff main -- <path>`, read-only).
3. Fix it if the fix is in this branch's own changes or in editor-only code. If it needs a change to a core system's behaviour (`tech/core-systems.md`) beyond restoring what this branch broke, stop and report the cause and the options.
4. **Play hardening (THJ approved):** in `EditorLevelLoader.EnterPlay` (`Core/Levels/Runtime/LevelBase.cs`), write the two fast-forward EditorPrefs (`LevelFastForwardRoster.IdKey`, `PrefabPathKey`) directly just before `EditorApplication.isPlaying = true`, so a load started while the previous run's `EnteredEditMode` is still being delivered can't lose them. Keep the `playModeStateChanged` handler for the teardown.

## Tests

An edit-mode test that fails on the cause if it is logic (e.g. pool size from a roster, the sandbox roster). Full EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

## Gates

Review / EditMode / THJ plays a `GB_` level and a normal mission: FP fills, Roles and pass-by work. Commits: the regression fix on its own (it may need reverting alone), the hardening on its own.
