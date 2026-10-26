# Merge main into thj/home-test (2026-10-26)

Branch: `thj/home-test`. Scope: this branch. Tier 3, approved by THJ (D-181). Size L. Implementer model: opus (core files).

## State at start

- THJ ran `git checkout thj/home-test && git merge --no-ff --no-commit main`, through the coordinator, with his yes.
- `main` @ `a1483f0b9` (includes THJ's "unity mcp" package commit); `thj/home-test` @ `46c9a88ab`. 128 commits come in; home-test has 59 of its own.
- The merge is in progress. Six files are in conflict; everything else merged on its own.
- Three uncommitted edits by THJ came across unchanged and must stay out of the merge: `LiberationSans SDF - Fallback.asset`, `ProjectSettings/EditorSettings.asset`, `ProjectSettings/ProjectSettings.asset`.
- The Unity editor is closed.

## Conflict resolutions (THJ decided, D-181)

1. `Core/Managers/GlobalEventBus.cs`: keep both. Home's three events (`homePhaseChanged`, `homeSlotResolved`, `homeDayReportReady`, under their `[Space][Header("Home")]`) first, then main's three Family Role events with their comments (`onFamilyRolePrompt`, `onFamilyRoleOutcome`, `onFamilyRoleBadgeHover`).
2. `Core/Managers/PlayModeStaticReset.cs`: keep both. All Home resets and `CameraEdgeScroller`, plus main's `IdlePhaseSequence.ResetPlayModeState()`.
3. `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: take main in all three spots (the comment, and the `superTimeAbility?.Preset != null` guard twice).
4. `Core/_Dev_/Runtime/CheatHandler.cs` (has a BOM, keep it): take main in all three spots (`_nextLevelAction2`, numpad6 + F12, and removing the second action on cleanup).
5. `Resources/GlobalSettings.asset`: add main's `combatLogToFile: 1`.
6. `Resources/Tags/GTagSet.asset`: keep both top-level groups after `BloodDebt`, main's `Kin` (with `Dark`) and home-test's `Home` (Meal, Wounded, Ration, Omen). Rebuild this section from `git show main:` and `git show thj/home-test:` rather than from git's markers, which line up the wrong lines. Keep home-test's `Home` group fields exactly as they are on home-test, even though they look wrong (Blood Debt's icon and text); that is fixed later in its own commit (D-182). Make sure every tag on either branch is present exactly once, including `Status.Unaware` from main.

## Checks after resolving

- `GTagRegistry.asset` merged on its own: check it matches the merged `GTagSet` (every tag on both branches, `Status.Unaware` included, no duplicates, the YAML well-formed). Report any mismatch; do not hand-edit IDs without reporting.
- Merged on its own but changed on both sides; check that each side's changes survived and the YAML is well-formed:
  - `Unit_John`, `Unit_Linda`, `Unit_Lucy`, `Unit_Mark` prefabs
  - `LevelHealingRoom.prefab`
  - `Home - Scene.unity`: main's only change is `da54e4ec2` (the Workshop Cabinet collider turned off, +4 lines). If the scene looks broken, stop and report; do **not** take main's scene (THJ wants to look at it first).
  - `manifest.json`, `packages-lock.json`: the MCP package plus home-test's Timeline 1.8.13, and valid JSON.
- Also merged on their own, worth a read for semantic clashes: `FactionControllerBase.cs`, `CombatLevelRunHandler.cs`, `GlobalSettingsSO.cs`, `CombatLevelUIManager.cs`, `GUnit.cs`, `HomeInteractables.cs`, `AIRegressionTest.cs`. Do **not** fix or re-baseline the AI regression test.
- No conflict markers left anywhere under `miso/` (`git diff --check`, plus a grep for `<<<<<<<`).
- Keep each file's line endings and BOM.

## Rules

- Resolve the files, then `git add` only the six resolved files to mark them resolved. That is allowed for this task only: it records the resolution and commits nothing. No `git commit`, `merge --abort`, `checkout`, `restore`, `reset` or `stash`. Never stage THJ's three uncommitted edits.
- Then run the EditMode suite from the command line (the editor is closed; see `CLAUDE.md`, 6000.3.4f1 path). Results go in the scratchpad. Every test passes except `AIRegressionTest.Baseline_MatchesCurrentAI`. If anything else fails because of the merge, report it; fix it only if it is a direct merge mismatch (for example a missing call or a member renamed on one side).

## Acceptance

- [ ] The six conflicts are resolved as above, with no markers left.
- [ ] The tag set and tag registry agree, and both branches' tags are present.
- [ ] The prefabs, Home scene and packages hold both sides' changes.
- [ ] It compiles and EditMode passes (known red only).
- [ ] The report lists anything that needs THJ's eyes in play.

## Then

Reviewer (read-only) → THJ opens Unity, Ctrl+R, and plays Home plus one combat level (a Masher level and the Shift preview) → merge commit (one popup) → D-182 tag fix commit → `branches.md` and build log.

## Docs to update

`branches.md` (home-test merge list, `main` features now on home-test), `build-log.md`, `status.md`.
