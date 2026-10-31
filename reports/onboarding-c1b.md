# Report: Onboarding C1b, merge safety (opening setup builder)

Plan: plans/onboarding/2026-10-31-onboarding-merge-safety.md    Agent: miso-implementer    Branch: thj/onboarding (no git writes, nothing staged)
Outcome: done (editor tool and tests; no runtime change, no Play session)

## What changed

New, all under `miso/Assets/_Project/Features/Onboarding/Editor/` (editor-only, namespace `MISO.Core.Features.Onboarding.EditorTools` / `.EditorTests`, LF, no BOM), each with its `.meta`, plus `Features/Onboarding.meta` and `Editor.meta`:
- `OnboardingOpeningSetup.cs`: the table at the top (missions by asset GUID, graph nodes and links, removed missions, pin re-points old to new with the new pin name, pins to hide, recruits by character data GUID with their unit prefab path, scenes whose `initialMission` is set), the target-path redirect (`SetupTargets`), the report type, the two menu items `Tools/Onboarding/Apply Opening Setup` and `Tools/Onboarding/Check Opening Setup` (report only), and `Run(targets, apply)`.
- `OnboardingOpeningSetup.Graph.cs`: mission graph step. Works on a copy of the graph's nodes and edges and writes it back only if something changed. Removes the old missions' nodes and edges, then removes a gate only if it lost an input (or output) to a removal and has none left on that side. Adds the four nodes, sets the Hearth initial, adds the links (River AND Ridge through one gate, found by its exact input set, else created). Every other node stays.
- `OnboardingOpeningSetup.Scenes.cs`: scene and prefab steps. `initialMission` on any component of IntroScreen / MainMenuScene; `unlockedAfterMission` on the Mark unit; Home scene: world map pins found by their mission (`WorldMap_Button.mission`, re-point + rename, hide), Mark's `CharacterSelectButton` and `UpgradesPanel` entry found by `Mark_DialogueCharacter`. Scenes are opened additively, saved only if a change was made, closed if the step opened them. If a target scene is already open with unsaved changes, the run stops before writing anything.
- `OnboardingOpeningSetupTests.cs`: 5 EditMode tests (below).

No edits to existing files. No new statics that hold state: the table is `static readonly` immutable data inside an editor-only class, so no `PlayModeStaticReset` hook is needed.

## Acceptance criteria

- [x] Apply on the committed tree changes nothing: ran `Tools/Onboarding/Apply Opening Setup` on the real project. Log: "nothing to change", every step "already applied". `git status` afterwards shows only the new `Features/Onboarding` files plus THJ's pre-existing `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/EditorSettings.asset`, `ProjectSettings/ProjectSettings.asset`. (The TMP fallback font that was modified at the start no longer shows as modified; I did not touch it, Unity must have restored it.)
- [x] On the pre-C1 copies it reproduces C1's graph and scene wiring: see the proof below.
- [x] Home-test's extra graph nodes survive: `ApplyOnTheGraph_KeepsNodesItDoesNotOwn` (a foreign mission behind an input-less gate, plus a loose mission hanging off the Rootwell; nodes and edges all survive Apply).
- [x] EditMode suite green except the known red test: 1061 total, 1060 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (untouched). 5 of the 1061 are new, all green.

Test coverage: `CheckOnTheProject_ReportsNothingToChange_AndLeavesOpenScenesAlone` (opens/closes scenes additively, asserts the open scenes and their dirty state are identical before and after; reports Inconclusive rather than failing if THJ has a target scene open and dirty), `ApplyOnTheGraph_KeepsNodesItDoesNotOwn`, `ApplyOnTheGraph_ReplacesTheOldOpening` (old M1 gone, Hearth initial and the entry, Rootwell follows the Trail), `ApplyOnTheGraph_SecondRunChangesNothing`, `CheckOnTheGraph_DoesNotModifyIt`. The scene, prefab and pin steps are covered by the proof run and the project no-op, not by unit tests.

## Proof on the pre-C1 state

Copied `Game Data.asset`, `Home - Scene.unity`, `Unit_Mark.prefab`, `IntroScreen.unity`, `MainMenuScene.unity` from `194bd566b` into `Assets/_ScratchMergeProof/`, ran the builder against them through the target redirect, compared with the committed files semantically, then deleted the folder.

- Check-only on the old copies listed exactly C1's edits (7 node removals, 4 gate removals, 4 nodes added, Hearth initial, 4 links, 2 `initialMission`s, Mark prefab, 4 pins re-pointed and renamed, 3 pins hidden, Mark's select button and upgrades entry).
- Apply: 36 changes, 0 problems. Second Apply: 0 changes.
- Comparison (dump of rebuilt copy vs committed file, sets of lines):
  - Mission graph: 30 items vs 30, identical. Covers every node (entity by mission, gates by their input and output missions and AND/OR mode, initial flag, randomized, options), every edge and the entry mission. Node GUIDs and positions of new nodes differ (new random GUIDs; positions follow the table), and are not compared. Dead M8-M14 branch and its input-less gate: identical.
  - Home scene: 34 items vs 34, identical (every `WorldMap_Button` by hierarchy path, mission and active flag, including the renamed pins and the three hidden ones; Mark's `CharacterSelectButton` mission; `UpgradesPanel` entries; Home station unlock lists).
  - IntroScreen and MainMenuScene: `initialMission` = The Hearth, identical. Mark prefab: `unlockedAfterMission` = The Hearth, identical.
- Raw text diff of rebuilt copy vs committed (ignoring CR): Game Data 44 lines (new node GUID/order only), Home scene 27 (the nine empty `GlobalEventBus` UnityEvent fields Unity re-adds when it saves the scene; the same noise C1 stripped by hand), Unit_Mark 4, IntroScreen 0, MainMenuScene 6 (override ordering). No semantic difference.
- Cleanup: `Assets/_ScratchMergeProof` and its meta deleted through the AssetDatabase; verified gone from disk and from `git status`. The proof script lived in that folder and went with it.

## Save reset

No.

## Decisions I made

- Table rows reference missions by asset GUID (labels only for the log), so renames and moves do not break the setup.
- Pin renames (`MapButton Hearth` etc.) are part of the pin row, so the Home scene also ends with C1's names. They are cosmetic; the matching is by mission.
- A gate is removed only when it lost an input to a removed node and has none left, or lost an output and has none left. A plain "gate with no input" rule would have deleted the dead M8-M14 branch's input-less gate.
- A new gate for River AND Ridge is found by its exact set of inputs and its output (so a re-run, or a merged version that already has one, is reused); only created if absent.
- `EditGraph` works on a cloned node/edge list and swaps it in only if changes were made, so Check cannot touch the asset and a no-op Apply writes nothing.
- Deviation noted: C1 edited the graph "through the editor API"; the builder edits `SerializableDependencyGraph` data directly (public lists), same result and no window needed.

## Needs THJ

None.

## Docs to update

- `tech/onboarding-merge.md`: Recipe step 2 and the "Builder re-applies" column can now be filled in as built (menu names above, proof result above). Add the limits listed in the next section.
- `build-log.md` / `status.md`: C1b built, no-op verified, proof done.

## Risks and loose ends

What the builder cannot re-apply (put in the merge notes):
- **Station unlocks** (`HomeInteractables.UnlockAfterMissions`, Bookshelf, Training Field, Cooking Cabinet, Grandma Table, Equipments Cabinet) still point at the removed missions and stay locked; C1 left them, so they are not part of the setup. The Home visits chunk must add rows.
- **`UpgradesPanel` Family tab** (`characters[5]`, M3 Wolf) and the **`HomeStates-Idles/M4..M7`** required-mission lists: untouched by C1, not in the table.
- **Mission assets** (the four new `.asset` files) and **WorldMapPanel.prefab** are not edited by the builder; they must exist (they are onboarding-only files, so no conflict). If a mission asset is missing the step reports a problem instead of guessing.
- **Home sortie nodes** on `thj/home-test` have no incoming edge, so after the merge they are open from the start. The builder deliberately does not gate them (a design question in the merge notes).
- **Pin positions and which pin becomes which mission** follow the table (old mission to new). If home-test moved or re-pointed those pins itself, the builder re-points by the old mission it finds; a pin pointing at neither old nor new mission of a row gives "PROBLEM: no world map pin points at ..." rather than a guess.
- **Home scene save noise:** applying to a scene that actually changes re-serialises the nine empty `GlobalEventBus` UnityEvent fields (visible in a diff). Harmless; strip the added lines if a clean diff matters. A no-op run never saves a scene.
- **Mark prefab save:** applying a change goes through `LoadPrefabContents` / `SaveAsPrefabAsset`; the proof diff was 4 lines, so the prefab is rewritten faithfully, but check its diff after the first real merge run.
- **Both pins and buttons are found in the loaded scene only.** A pin kept in another scene or a prefab asset would not be seen.
- If a target scene is open and dirty, Apply stops with a message and writes nothing (by design); the unit test reports Inconclusive in that case.
- Pre-existing dirty files left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*`.
- The console already shows many "Serialization depth limit 10 exceeded" messages unrelated to this work.

## Proposed commits

1. `feat(onboarding): add an editor setup that re-applies the opening mission graph, pins and unlocks` (plain, editor-only): `miso/Assets/_Project/Features/Onboarding.meta`, `miso/Assets/_Project/Features/Onboarding/Editor.meta`, `miso/Assets/_Project/Features/Onboarding/Editor/OnboardingOpeningSetup.cs` (+ `.meta`), `OnboardingOpeningSetup.Graph.cs` (+ `.meta`), `OnboardingOpeningSetup.Scenes.cs` (+ `.meta`), `OnboardingOpeningSetupTests.cs` (+ `.meta`). Builder and tests are small and only work together; one commit. Do not stage the four pre-existing dirty files. Note: `Features/Onboarding.meta` is the folder meta, `git status` lists it as untracked.

## Other branches

`thj/home-test`: this is the tool for its merge (recipe in `tech/onboarding-merge.md`). Nothing to do there now.

## How to see it

1. Menu **Tools > Onboarding > Check Opening Setup**: Console shows "nothing to change" and each step "already applied". Nothing is written.
2. **Tools > Onboarding > Apply Opening Setup** does the same on the current tree (no file changes).
3. Test Runner > EditMode > `OnboardingOpeningSetupTests` (5 tests).
4. After a merge: take home-test's version of `Game Data.asset` and the Home scene, run Apply, save; the Console lists each change. Run it again: "nothing to change".
