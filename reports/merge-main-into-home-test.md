# Report: Merge main into thj/home-test

Plan: plans/2026-10-26-merge-main-into-home-test.md    Agent: miso-implementer    Branch: thj/home-test
Outcome: done

The merge is still in progress (no commit). All six conflicts are resolved and marked with `git add`. `git diff --name-only --diff-filter=U` is empty. THJ's three uncommitted edits are still unstaged.

## What changed

Conflict resolutions, all as decided in D-181. Each file kept its line endings (all six are LF on both branches, and still are) and its BOM (`GlobalEventBus.cs`, `FactionRoleHandlerBase.cs` and `CheatHandler.cs` have one and still do; `PlayModeStaticReset.cs` and the two assets have none).

- `Core/Managers/GlobalEventBus.cs`: kept both. Main's three Family Role events, with their comments, come right after the Misc events, then `[Space][Header("Home")]` and Home's three events. Against main, the file differs only by home-test's `using MISO.Core.Systems.HomeSystem;` and the Home block. This is the coordinator's reorder of the plan's order; see Decisions I made.
- `Core/Managers/PlayModeStaticReset.cs`: kept both. All the Home resets and `CameraEdgeScroller`, then main's `IdlePhaseSequence.ResetPlayModeState()`. Main's `using MISO.Core.Animation;` and its `FactionRoleProvocationSuppression`/`FamilyRoleRelay` resets came in on their own.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: took main in all three spots. The file now equals main's, except for one blank line (home-test's change from trailing spaces to an empty line, merged on its own).
- `Core/_Dev_/Runtime/CheatHandler.cs`: took main in all three spots (`_nextLevelAction2`, numpad6 + F12, removing the second action on cleanup). Home-test's K-cheat null guard (the family-points cheat) also survived; it is the only difference from main.
- `Resources/GlobalSettings.asset`: added main's `combatLogToFile: 1`. Home-test's `homeCycle` reference is kept.
- `Resources/Tags/GTagSet.asset`: rebuilt from `git show main:` with home-test's `Home` block (lines 150–184 of home-test's file) inserted after main's `Kin`. I did not use git's markers. The `Home` group's fields are exactly as on home-test, including Blood Debt's icon, display name and description (left for the D-182 fix commit). The result differs from main only by the `Home` block, and from home-test only by main's `Status.Unaware` and `Kin` blocks.

No other files changed. I wrote no game code; the only scripts I wrote were check tools in the scratchpad (`tools/resolve.py`, `tools/tags.py`, `tools/mergecheck.py`).

## Acceptance criteria

- [x] The six conflicts are resolved as above, with no markers left. `git diff --check` and a grep for `<<<<<<<`/`>>>>>>>` under `miso/Assets`, `miso/Packages` and `miso/ProjectSettings` find nothing. The only `--check` hits are trailing spaces on empty `displayName:`/`description:` in main's own `Kin` block (Unity's YAML style, identical on main).
- [x] The tag set has every tag from both branches and the registry agrees with it, apart from a stale cache. Details below. **One mismatch is reported, not fixed:** the registry's cached copy has no `Home` group. That was already true on home-test before the merge.
- [x] The prefabs, the Home scene and the packages hold both sides' changes. Details below.
- [x] It compiles and EditMode passes, apart from the known red test: 1139 tests, 1138 passed, 1 failed (`AIRegressionTest.Baseline_MatchesCurrentAI`), no `error CS`.
- [x] The report lists what needs THJ's eyes in play (How to see it).

Test coverage: the merge is checked by the full EditMode suite and the YAML and diff checks below. The feel items (banner timing, Home markers, Family Role prompts in Home sorties) need THJ's play check.

### Tag registry check

- Tag paths in the merged `GTagSet`: 27, no duplicates. They are exactly the union of main's and home-test's sets, including `Status.Unaware`, `Kin`, `Kin.Dark`, `Home`, `Home.Meal`, `Home.Wounded`, `Home.Ration` and `Home.Omen`. `LevelSpecTags`: 12 paths. No name clashes across the two sets.
- `GTagRegistry.asset` (merged on its own) took main's changes: `Status.Unaware` and `Kin`. Home-test never changed this file.
- The registry's `accumulatedL1Tags` (34 paths) equals `GTagSet` plus `LevelSpecTags` **minus the five `Home` paths**. This is not a merge fault: home-test's registry never had them. The field is a cache. `GTagRegistry.Awake` and `OnValidate` rebuild it from `entitySets`, and IDs resolve through `entitySets.GetEntities()`, so the `Home` tags resolve at run time. The cache's `Unaware` icon (`9d7ae78c…`) also differs from the set's icon (`73f8bd11…`), which is main's own staleness.
- Expect Unity to rewrite `GTagRegistry.asset` the first time it saves the registry (adding `Home` and updating `Unaware`'s icon). That would be a new working-tree change after the merge. Leave it out of the merge commit, or let it ride with the D-182 tag fix. I did not hand-edit the registry.
- YAML is well-formed: one document each, no tabs, no markers, LF.

### Prefab, scene and package checks

For each file I diffed the merge against home-test (which should show only main's change) and against main (which should show only home-test's change). I also checked document headers, duplicate fileIDs, local references that point nowhere, tabs and markers.

- `Unit_John`, `Unit_Linda`, `Unit_Lucy`, `Unit_Mark`: main's role-zone fields (`showRoleZone`, `roleZoneSprite`, `roleZoneSlot`, `declineTexts`, `playDeclineBark`, `roleZoneColor`) and main's role texts and Mark's `MarkQTE`/`A_SFX_John_Hit` fixes are present. Home-test's stat-attribute overrides, `baseFactor: 0` and `homeLock` entries are present. Unit_Mark has no `homeLock` on either branch. No duplicate IDs and no dangling references.
- `LevelHealingRoom.prefab`: main's objective text ("Approach the glowing statue to heal, then reach the exit.") and home-test's `healFractionOfMax: 0` are both present.
- `Home - Scene.unity`: **the scene looks sound, so main's scene was not taken.** Against home-test, the only difference is main's 4 lines from `da54e4ec2` (the `m_Enabled: 0` override on target `61089915482654192`). They sit inside the PrefabInstance `&2023361525`, whose source prefab is `Home.prefab` (`db00749…`). That target exists in `Home.prefab` as a `BoxCollider2D` (`&61089915482654192`), and the override is not duplicated. 490 documents, no duplicate IDs, no dangling local references.
- `manifest.json`: valid JSON. It has `com.coplaydev.unity-mcp` (git, `#v10.3.0`) and `com.unity.timeline` 1.8.13.
- `packages-lock.json`: valid JSON. It has the MCP package and its new `com.unity.nuget.newtonsoft-json` 3.2.2 dependency, and Timeline 1.8.13. In the batch run, Unity resolved both: Timeline `1.8.13`, MCP `@da7b9ae4aeeb`.

### Semantic read of the auto-merged C# files

No compile-level or logic clashes. Notes:

- `FactionControllerBase.cs`: main's turn-start pause and End Turn button flag sit beside home-test's `HomeFiresidePayoff.SpendRole` call in the role-spend path. The two don't interact.
- `CombatLevelRunHandler.cs`: main's turn-switch holds, the turn-start pause and the non-waiting `PlayPhaseAnimation` are only in `SwitchTurnIE`. Home-test's Omen and From-Home tag hooks are in prepare-level, and `HomeFromHomeBanner.Show()` runs after `ShowHUD`. The first turn doesn't go through the phase banner, so the two banners don't overlap at level start.
- `GlobalSettingsSO.cs`: main's `displayLethalMarkPreview` and home-test's `homeCycle` are separate fields; both are serialized in the merged asset.
- `CombatLevelUIManager.cs`: main's banner input lock, the End Turn button path and the tutorial input lock sit beside home-test's Retreat-home button on the mission map and its "Returning home..." text on the defeat panel. They are separate paths.
- `GUnit.cs`: home-test only adds the `UnlockedAfterMission` getter. Main's `RecentAttackerMemory` and ghost facing are intact.
- `HomeInteractables.cs`: **one interaction to watch.** Main's new `RefreshLock()` runs in `OnEnable` and on every pointer enter, exit and down, and calls `homeInteractableUI.SetActive(!locked)` when the marker's state differs. Home-test's `HomeStationProp.LateUpdate` hides or shows that same object (`MarkerTransform`) every frame for prologue-closed rooms and while the map is open. `HomeStationProp.Highlight` also calls the spot's `OnPointerEnter`/`OnPointerExit` from the diamond. `LateUpdate` runs after pointer events in the same frame, so it should win with no visible flicker. Still, a hover on a closed room's prop now toggles the marker on and off within a frame. Worth a look in play; I changed nothing.
- `AIRegressionTest.cs`: main added one baseline line (Masher counter); home-test added `IsLevelPrefab`. Both kept. I did not run any fix or re-baseline.

### Test run

Batchmode, Unity 6000.3.4f1, editor closed (no `miso/Temp`). Results: `C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\4a7b2e15-2aac-45e7-9e97-b6e33d04e813\scratchpad\results.xml`, log: `C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\4a7b2e15-2aac-45e7-9e97-b6e33d04e813\scratchpad\test.log`.

- 1139 tests, 1138 passed, 1 failed: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red). Its report shows 709 checks with 38 failures and the usual fatal NRE in `AIStrategyPlanner.HandleLivingUnitsCondition` (`AIStrategyPlanner.cs:163`), already in `tech/ai-regression-test-triage.md`. The call site is now `AIRegressionTest.cs:679` instead of 662, because of home-test's 7-line helper. The new "unexpected" entries come from main's content (Dark Shaman heal ability and evaluator, Mark_Linda duo, Black Despair relic, Toba wall). They belong to that test's fix session.
- The batch run left no new working-tree changes: `git status` shows only THJ's three edits unstaged.

## Save reset

No.

## Decisions I made

- In `GlobalEventBus`, I first put the events in the plan's order (Home's block first), which put main's three Family Role events under the "Home" header in the Inspector. Reordered on the coordinator's decision: main's three Family Role events, with their comments, now come right after the Misc events and before `[Space][Header("Home")]`, so the Home header is last and holds only the Home events. Field declarations were only reordered: LF and the BOM are kept, and the file was staged again. Against main, the staged file now differs only by home-test's 7 lines (the `using` and the Home block).
- `GTagRegistry.asset`: the coordinator says leave it alone. If Unity rewrites it, the rewrite goes in the Home tag-fix commit.
- I treated the registry's missing `Home` cache as a report-only mismatch. It is a rebuilt cache, it predates the merge, and the plan says not to hand-edit it.

## Needs THJ

None. The coordinator settled both open points (see Decisions I made).

## Docs to update

- `branches.md`: home-test now holds main's 128 commits up to `a1483f0b9` (the MCP package, Family Role prompt and outcome events and role zones, turn-start pause and banner input lock, recent-attacker memory, `combatLogToFile`, `Status.Unaware`, `Kin.Dark`/Dark Shaman heal, Workshop Cabinet collider fix, and more). Add it once the merge commit exists.
- `build-log.md`, `status.md`: the merge and its test result (1138/1139, known red only).

## Risks and loose ends

- `GTagRegistry.asset`'s cache is stale (no `Home`, old `Unaware` icon) and will likely be rewritten by Unity; see above.
- `HomeInteractables` and `HomeStationProp` both drive the same marker object (see the semantic read).
- Pre-existing on home-test, untouched: `FactionControllerBase.cs` has a comment `// M9 Step 6c` on the `HomeFiresidePayoff.SpendRole` line. That is a private plan tag in shared code. It is for a later cleanup, not this merge.
- The `Home` tag group still shows Blood Debt's icon, name and description (D-182).

## Proposed commits

1. The merge commit: everything in the index now, which is the 128 incoming commits plus the six resolved files. **Exclude** `miso/Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset`, `miso/ProjectSettings/EditorSettings.asset` and `miso/ProjectSettings/ProjectSettings.asset`, and any registry rewrite Unity makes after opening (that rewrite goes in commit 2). Message suggestion: `Merge branch 'main' into thj/home-test` (risky: merge, core files).
2. The D-182 tag fix (the `Home` group's icon and text), on its own, as the plan says.

## Other branches

None.

## How to see it

1. Open Unity (6000.3.4f1) and press Ctrl+R. Expect a clean compile. Expect a one-time package import (Timeline 1.8.13, the MCP package). Then check `git status` for a `GTagRegistry.asset` change (see above).
2. Optional: Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red.
3. Play the Home scene:
   - Click the Workshop. The cabinet collider no longer steals the click.
   - Hover the station props and diamonds, including a room still closed by the prologue, and open and close the map. The markers should not flicker or reappear on closed rooms.
4. Start a Home sortie into a Masher level:
   - The From-Home banner and Omen tags appear at level start.
   - Turn switches have the short pause after a turn that ended on its own, and none after the End Turn button.
   - The player banner locks input until it ends.
   - Family Role prompts show their decline barks and role zones (hold Shift for the preview).
   - The Masher's counter works.
5. Lose a level in a Home attempt. The defeat button says "Returning home..." and goes back to Home. The mission map still offers "Retreat home".
6. Press F12 and numpad6 in a combat level. Both complete the objective (the dev cheat).
