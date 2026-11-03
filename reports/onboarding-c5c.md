# Report: Onboarding C5c, guided skill spend

Plan: plans/onboarding/2026-11-02-onboarding-c5-home-visits.md (C5c)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. EditMode: 1301 run, 1300 pass, only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` fails. The pulse look and the live open need THJ's play check.

## What changed

Core-folder UI (not on the core list); the existing files change by the `partial` keyword only:
- `Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.cs`: `class` -> `partial class` (1 line).
- `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.cs`: `class` -> `partial class` (1 line).
- `.../AbilityUpgradePanelUI.Guided.cs` (new): `OpenOnCharacter(CharacterDataSO)` (selects that hero's tab through her icon; returns false if the tabs are not built yet or she has none) and `HighlightNode(string nodeGuid)` (forwards to the tree).
- `.../AbilityTreePanelUI.Highlight.cs` (new): `HighlightNode(guid)`, `HighlightedNodeGuid`; adds an `Update` that pulses the node's button (scale, amplitude 0.15, period 1 s, both serialized) and restores the scale. Kept by node id, so it survives the tree being rebuilt. It stops when the node's level rises (after a purchase), on `HighlightNode(null)`, and on disable. No existing panel behaviour changed.

Onboarding (non-core):
- `Features/Onboarding/GuidedSkillSpend.cs` (new): component on the skill tree panel's GameObject. On enable it reads `GameHandler.Instance.GameData.GetLastCompletedMission()`. `Pick(last, alreadyShown)` returns a guide only if River and Ridge are both completed, the last one completed is River (Lucy) or Ridge (Linda), and it was not shown before. It then waits up to 10 frames for the panel to build its tabs (the panel's first-time setup selects hero 0 last), calls `OpenOnCharacter` then `HighlightNode`, and marks it shown. Data: `lucy` and `linda` fields (`afterMission`, `sister`, `nodeGuid`) plus a `panel` reference. No statics.
- `Features/Onboarding/GuidedSkillSpendMarker.cs` (new): the once-per-save marker (below).
- `Features/Onboarding/Editor/OnboardingOpeningSetup.GuidedSpend.cs` (new): builder step `EditGuidedSpend` (adds the component to the panel, sets the panel ref and both guide rows; Check lists drift, Apply fixes it).
- `Features/Onboarding/Editor/OnboardingOpeningSetup.Scenes.cs`: one line in `RunHomeSceneStep` calling `EditGuidedSpend`.
- `Features/Onboarding/Editor/GuidedSkillSpendTests.cs` (new): 12 test cases.
- `Features/Home - Imported/___Khashayar/Home - Scene.unity`: applied by **Tools > Onboarding > Apply Opening Setup** (no hand edit): +31/-2 lines (the component on the `UpgradesPanel` object plus the prefab-instance bookkeeping Unity writes for an added component). No other Home scene change from the run.
- New `.meta` files with each new file.

## Chosen nodes (first purchasable: unlock level 0, no earlier node needed, upgradeable, shown, not family)

- Lucy (after The River): **Sidewinders**, id `9bc70a86-73f1-4fbb-87bd-833fb2f9ce17` (Ability, 2 levels). Her other level-0 node, Blink, has no upgrade levels; Rapid Blink needs Blink and unit level 2.
- Linda (after The Ridge): **Longshot**, id `66f54db0-e491-4545-a050-68663c4f89de` (stat, 2 levels). Harmonic Slam has no upgrade levels.
- Not checked: whether either sister has a skill point at that moment (depends on the XP/SP grants of the earlier chunks). With no point the node pulses but cannot be bought.

## Once-per-save mechanism

No new saved field. `PlayedSequencesTracker` (already saved under "PlayedSequences", keyed by sequence name) is used with an in-memory `Sequence` named `GuidedSkillSpendShown` (`GuidedSkillSpendMarker`: plays nothing, created and destroyed per call, no asset). It is marked as soon as the guided open succeeds; if the hero has no tab, nothing is marked.

## Acceptance criteria

- [x] First open after both pair missions selects the last-completed sister and highlights her first purchasable node: pick logic and node data have EditMode tests; the live open and pulse need the play check.
- [x] Once per save: the rule (`alreadyShown` -> no guide) is tested; the real tracker and save write are not exercised in EditMode (that would write the player's save file), so they need the play check.
- [x] Later opens behave as now: the component does nothing once marked or when `Pick` is null.
- [x] No unspent-point badge built.
- [x] EditMode tests: River last -> Lucy; Ridge last -> Linda; only one done -> none; already shown -> none; neither pair mission last -> none; marker name; each guide node is the sister's first purchasable node (2 cases); builder drift on a copy of the Home scene (component removed and a wrong node id both repaired, second run has nothing to change); the real Home scene has the component and nothing to change for it.

## Save reset

No. The tests do not touch the save. THJ resets the save for the play check to see the guided open again.

## Decisions I made

- The component sits on the panel's own GameObject and uses `OnEnable` plus a short coroutine, so `HomeManager.ShowAbilityUpgrades` and the station wiring needed no change; the panel builds its tabs in `Start` on first activation, so the component retries for up to 10 frames.
- Once-per-save through an in-memory marker `Sequence` instead of a new asset or save field (same effect as a play-once sequence).
- The highlight stops when the node's level rises above the level seen when the pulse started (level 0 is ambiguous between base and bought).
- The pulse is a scale pulse on the node button (same idea as the level ability hint); greybox.

## Needs THJ

none

## Docs to update

- `tech/onboarding-merge.md`: row below.
- Plan status, `build-log.md`, `status.md` (coordinator).

## Risks and loose ends

- `AbilityTreePanelUI` now has an `Update`; it returns at once when nothing is highlighted.
- Sisters' skill points at that moment not verified (above).
- The builder rows use the node ids and the character asset GUIDs; if a node is deleted and recreated, the row and the node test need the new id.
- After a merge that takes another branch's Home scene, re-run Apply (the component is lost otherwise); `HomeSceneSkillTreePanelHasTheGuidedSpend` fails until then.
- Noticed, not touched: the working tree has other uncommitted changes from before this chunk (Greybox prefabs, AI brain scripts, PreloadScreen, ProjectSettings, Hearth Linda/Lucy tests).

## Merge-notes row (for `tech/onboarding-merge.md`)

| `Home - Scene.unity` (again) | Guided skill spend component added to the skill tree panel's GameObject (`UpgradesPanel`, the one with `AbilityUpgradePanelUI`): panel ref, Lucy after The River (Sidewinders), Linda after The Ridge (Longshot) | C5c, uncommitted | Yes (same file) | Not run | Yes: `OnboardingOpeningSetup.GuidedSpend.cs` (finds the panel by component; `GuidedSkillSpendTests` proves it on a copy of the scene) |

Also: `AbilityTreePanelUI` and `AbilityUpgradePanelUI` became `partial` (1 line each); another branch editing those files conflicts only on that line.

## git

`git diff --stat` for the tracked files of this chunk: `AbilityTreePanelUI.cs` 1, `AbilityUpgradePanelUI.cs` 1, `OnboardingOpeningSetup.Scenes.cs` 1, `Home - Scene.unity` 31+/2-. Untracked: the 6 new .cs files and their .meta files (listed above).

## Proposed commits (dependency order)

1. `feat(home): skill tree panel can open on a chosen hero and highlight a node`: `Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.cs`, `AbilityUpgradePanelUI.cs`, `AbilityTreePanelUI.Highlight.cs(.meta)`, `AbilityUpgradePanelUI.Guided.cs(.meta)` (plain, Core folder UI)
2. `feat(onboarding): guided skill spend after the second pair mission`: `Features/Onboarding/GuidedSkillSpend.cs(.meta)`, `GuidedSkillSpendMarker.cs(.meta)`, `Editor/OnboardingOpeningSetup.GuidedSpend.cs(.meta)`, `Editor/OnboardingOpeningSetup.Scenes.cs` (plain; builds without the scene change)
3. `feat(onboarding): put the guided skill spend on the Home skill tree panel`: `Features/Home - Imported/___Khashayar/Home - Scene.unity` (scene, own commit, shared file)
4. `test(onboarding): guided skill spend pick, node data and builder drift`: `Editor/GuidedSkillSpendTests.cs(.meta)` (after 3, because one test expects the scene component)

Stage only those files; the Greybox prefabs, AI scripts, PreloadScreen and ProjectSettings changes in the tree are not part of this chunk.

## Other branches

`thj/home-test` shares the Home scene and may edit the two panel files (see the row above).

## How to see it

1. Reset the save, then play the opening: Hearth, then River and Ridge in either order.
2. Back at Home after the second of the two, click the Grandma Table. Expect the skill tree to open on Lucy (River was last) with Sidewinders pulsing, or on Linda (Ridge last) with Longshot pulsing.
3. Close the panel and reopen it: it opens as before (first hero, no pulse). Buying the pulsing node (with a point) also stops the pulse.
4. Reset the save and play the other order (Ridge then River, or River then Ridge) to check both sisters. The tree stays locked after only one of the two.
5. Tools > Onboarding > Apply Opening Setup (check) should report nothing to change for the Home scene.
