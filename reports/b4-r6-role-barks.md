# Report: B4 R6 Family Role barks (item E)

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (play check still needed). Revised after the R6 review: THJ's D-070 is applied.

## What changed

- `Core/Managers/GlobalEventBus.cs` (core, additive, D-069): a new `public UnityEvent<FactionRoleHandlerBase, bool> onFamilyRoleOutcome = new ();`, right under `onFamilyRolePrompt` in "Misc". Its comment gives the contract:
  - It is raised once for each role QTE that started, so always after that QTE's `onFamilyRolePrompt`.
  - `pressed` is true on a press (the notice path); `onFamilyRoleActivated` follows later.
  - `pressed` is false when the prompt ran out or was force-ended without a press (the ignore path). That is a decline, not a failure.
  - It is never raised when the prompt could not start.
  - It comes before the QTE's `qteEnded`.
  - The file keeps its BOM and LF line endings.
- `Core/Interactions/Runtime/PlayerController.cs` (core, additive), in `ActivateFactionRole`:
  - One local `var roleHandler = unit.AbilityOrchestrator.FactionRoleHandler;` before `StartEvent`.
  - The two callbacks became block lambdas. Each one runs its existing `SequentialActionHandler.Execute(noticeActions / ignoreActions)` first. Then it raises `onFamilyRoleOutcome.Invoke(roleHandler, true / false)` inside `try { } catch (Exception e) { Debug.LogException(e); }`, so a listener that throws cannot skip the QTE's `EndEvent()`.
  - The could-not-start path and the R5 prompt line are unchanged. No logic changed.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (core, additive, the same pattern as `showRoleZone`):
  - Two serialized fields after `showRoleZone`, each with a tooltip: `string[] declineTexts = Array.Empty<string>()` and `bool playDeclineBark = true`.
  - Read-only getters `IReadOnlyList<string> DeclineTexts` and `bool PlayDeclineBark`.
- `Core/FX/Runtime/DamageNumber.cs` and `DamageNumberManager.cs` (shared FX, core-adjacent): an optional trailing `bool ignoreTimeScale = false` on `PopText`, `Pop` and `ShowText`. When it is true, the DOTween sequence gets `SetUpdate(true)`, so it runs on unscaled time. The default leaves every existing popup as it was.
- `Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs` (+ `.meta`, new), the pure helpers:
  - `RoleBarkRules`:
    - `BarkDuration` is 1.2 and `FadeOutDuration` is 0.1.
    - `BarkGoneAt(now)` is the end of the popup's move plus its fade.
    - `ExecuteLine(pressed, text)` gives the execute line on a press only, and only when the line has text.
    - The rest: `Clean`, `DeclineLineIndex`, `DeclineAllowed`, `DeclineLine`, `DeclineDelay`.
  - `RoleDeclineTracker`: a plain object that allows one decline bark per role per turn and counts each role's decline barks in this fight. It has `ResetTurn` and `ResetFight`.
- `Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs` (+ `.meta`, new, not core): a MonoBehaviour that follows the bus like the other RoleZoneSystem presenters (polls in Update and rebinds when the bus changes).
  - **Prompt** (`onFamilyRolePrompt`): shows the unit's `unitFamilyRolePromptText` over its head.
  - **Press** (`onFamilyRoleOutcome(true)`, D-070): shows the unit's `unitFamilyRoleExecuteText` as the same over-head popup. The role insert is unchanged.
  - **Decline** (`onFamilyRoleOutcome(false)`): shows a decline line when the tracker allows one. If the same unit's prompt line is still on screen, the decline waits until it has fully faded (`BarkGoneAt`, realtime).
  - All three popups last 1.2 s on unscaled time, respect `GlobalSettingsSO.silenceBarks`, and show only when the line is non-empty and the unit is valid (not null, alive, on the grid).
  - Resets: the per-turn memory on `turnStarted` and `turnEnded`; the per-fight memory on `levelEnded` and whenever the bus changes (a new level).
  - Cleared on `levelEnded`, OnDisable and scene unload. A pending decline is dropped.
  - No statics.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: one idempotent `AddComponent<RoleBarkPresenter>` line and a comment in `Awake`, after the R5 line.
- `Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs` (+ `.meta`, new): 14 EditMode tests.
- Prefab data (small YAML edits, LF kept, nothing else touched):
  - Linda, Lucy and Mark get the new prompt and execute override values from `reports/b4-role-barks.md`. Linda's old execute line `'Have them on my sight! '` and its trailing space are gone. John keeps `No!` and `I got you!`.
  - All four `Unit_<Name>.prefab` files get `declineTexts` (two lines each) and `playDeclineBark: 1`. They are inserted before `superTimeAbility:` in each unit's role handler block.
- `CombatLevelUIManager.cs` and `FactionRoleVisual.cs`: the first version changed them; that change is reverted. Both are byte-identical to HEAD (`git diff` is empty for both).

New `.cs` files are LF with no BOM, and their `.meta` files use the same two-line form as their RoleZoneSystem neighbours. The edited `.cs` files were LF before and still are.

## Acceptance criteria

- [x] **D-069 event and hooks.** The event is declared with its contract and raised only from the two QTE callbacks, each call wrapped in try/catch. `QTEButton.Finish` is guarded by `_eventActive`, so each prompt gets exactly one callback and therefore one outcome. The could-not-start path never reaches a callback. Checked by reading the code.
- [x] **Decline gating:** lines present, the `playDeclineBark` toggle, one bark per role per turn, element 0 for the first decline in a fight and element 1 after, resets per turn and per fight. Covered by EditMode tests.
- [x] **Execute popup gating (D-070):** shown only on a press and only when the line has text. Fade-aware decline delay. Covered by EditMode tests (`RoleBarkRulesTests`, 14/14 pass).
- [x] **No "too slow" or failure wording.** The only decline texts are the narrative lines. `ignoreActions` and silencing are unchanged.
- [x] **Insert timing unchanged:** `CombatLevelUIManager.cs` and `FactionRoleVisual.cs` are identical to HEAD.
- [x] **Compile:** no CS errors after a forced refresh and recompile.
- [x] **EditMode suite:** 175 tests, 174 pass. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, unchanged). AI untouched.
- [ ] **On screen:** needs the verifier's play check (see "How to see it").

## Save reset

no

## Decisions I made

- **Accepted deviation (D-070).** The plan says the barks go through `FactionRoleVisual.ShowWithDialogue`. Instead, the prompt, execute and decline barks are all over-head popups (`DamageNumberManager.ShowText`, the floating text `BarkManager.ShowBark` ends in), and the role insert keeps its current timing and shows no line.
  - Why: the existing insert never showed `unitFamilyRoleExecuteText`. Routing the line through `ShowWithDialogue` would replay the insert, or hold it 1.5 s longer.
- **Opt-in `ignoreTimeScale` on the popups.** DOTween runs on scaled time by default (DOTweenSettings `defaultTimeScaleIndependent: 0`), so a popup at John's timeScale 0 would freeze, still invisible. With the flag, the popup animates on unscaled time.
- **Popup look.** White, Vertical movement, amount 0.5; all three are serialized on the presenter. The popup sits at `DamageNumberTrigger.StartPosition`, or at the unit's position when there is none.
- **Respects `GlobalSettingsSO.silenceBarks`**, as BarkManager does.
- **"First decline in a fight"** counts the decline barks a role actually played. So the first line a player hears is always element 0, even after the toggle was off.
- **The once-per-turn mark is set when a decline is accepted**, even if the delayed popup is then dropped (the unit died, barks are silenced, the level ended). A role never declines twice in a turn.
- **Outcome raised after `Execute(...)` and inside try/catch** in each callback. It is still raised before `qteEnded`, because `EndEvent` runs after the callback returns.
- **Prefab YAML for `string[]`:** edited directly as a plain sequence. It re-imported cleanly. The base default stays empty, as the plan asked.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`:
  - The bus event `onFamilyRoleOutcome(handler, pressed)` and its contract.
  - The handler fields `declineTexts` / `playDeclineBark`.
  - `RoleBarkPresenter` (prompt, execute and decline popups), hosted by `ShowStatsHoverPreview`.
  - `DamageNumberManager.ShowText(..., ignoreTimeScale)`.
- `plans/2026-10-18-family-role-phase0-1.md`, item E: barks are over-head popups, not `ShowWithDialogue` (D-070).
- `design/gdd/family-systems.md` (via the designer): decline barks play at most once per role per turn, element 0 first and element 1 after, with a per-unit toggle.
- `plans/2026-10-18-family-role-readability-design.md`:
  - The "Press lands" row should say "execute bark over the role unit" (D-070).
  - The decline is detected with D-069's event, not inferred from other events.
  - The "Too slow" rows are stale (the R5 report already noted this).
- `build-log.md`: the R6 entry.

## Risks and loose ends

- **Prompt and execute lines can overlap.** A press usually comes within the 1.2 s of the prompt popup, so the execute line pops at the same unit while the prompt line is still rising. They are two separate popups with random-free vertical moves, so they may stack or overlap. D-070 asked for the execute line straight away (no delay, unlike the decline). Play check. If it reads badly, the fix is to give the execute line the same `DeclineDelay` as the decline.
- **No shared repeat timer with BarkManager.** Role barks skip BarkManager's repeat timer, so a graph bark can float at the same unit at the same moment.
- **Popups already on screen at teardown** are not removed on `levelEnded`. They fade out on their own within about 1.3 s.
- **Force-ended prompts count as declines.** `QuickTimeEventHandler.ForceEndEvent` ends a QTE through the ignore path. Today nothing force-ends a role prompt (it is used for the reversion QTE, Command Shield Dash and Catch & Return). A future caller that did would get a decline bark.
- **Dev scene.** `Scenes/DevScenes/TestLevel.unity` has its own LindaFactionRoleHandler, so there Linda uses the code default: no decline lines.
- **Console.** One "Internal error - unexpected guid mismatch" assert appeared again after each refresh (one each time, not two). It has no stack trace and came with no compile errors. The new `.meta` files have fresh uuid4 GUIDs.
- **THJ's Lucy prefab tweak is not in the working tree.** His roleZoneColor alpha change was already gone when this run started: `git status` showed the file clean and `git diff` was empty. Every hunk now in `Unit_Lucy.prefab` is mine: the text values at about l.455 and l.459, and 4 inserted lines at about l.2715. THJ may want to check whether his tweak was lost.
- **Not mine, do not stage:** `ProjectSettings/EditorSettings.asset` (` M`, see D-069), `ProjectSettings.asset`, `Packages/manifest.json`, `packages-lock.json`.

## Proposed commits

Each commit compiles on top of the ones before it. Commit 5 depends on the fields from 2, and commit 4 depends on 1 to 3.

1. `feat(bus): onFamilyRoleOutcome event, raised once per started Family Role prompt with pressed true/false (B4 R6, D-069)` (core, own commit)
   - `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
2. `feat(roles): decline bark lines and playDeclineBark toggle on Family Role handlers (B4 R6, D-063)` (core, own commit)
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
3. `feat(fx): opt-in unscaled time for floating text popups (B4 R6)` (shared FX, core-adjacent, own commit)
   - `miso/Assets/_Project/Core/FX/Runtime/DamageNumber.cs`
   - `miso/Assets/_Project/Core/FX/Runtime/DamageNumberManager.cs`
4. `feat(ui): Family Role prompt, execute and decline barks over the role unit (B4 R6, D-070)` (plain)
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs.meta`
   - `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`
5. `data: Family Role prompt, execute and decline lines for John, Linda, Lucy and Mark (B4 R6)` (data)
   - `miso/Assets/_Project/Features/Player/John/Prefabs/Unit_John.prefab`: one hunk, 4 inserted lines at about l.2825.
   - `miso/Assets/_Project/Features/Player/Linda/Prefabs/Unit_Linda.prefab`: two hunks, the text values at about l.372 and l.376, and 4 lines at about l.2495.
   - `miso/Assets/_Project/Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`: two hunks, the text values at about l.455 and l.459, and 4 lines at about l.2715. All mine (see Risks).
   - `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`: two hunks, the text values at about l.273 and l.277, and 4 lines at about l.2809.

Do not stage `ProjectSettings/*` or `Packages/*`.

## Other branches

`thj/home-test` gets this with the rest of B4 on its next merge of `main`.

## How to see it

1. Open a combat level with John, Linda, Lucy and Mark, with shared FTP of at least 1.
2. **Prompts.** Trigger each role's prompt:
   - an enemy attacks an ally inside John's diamond;
   - an enemy ends a move on Linda's row or column;
   - an enemy attacks an ally near Lucy;
   - an enemy attacks next to Mark's zone.

   When each prompt appears, a short white line floats over the role unit for about 1.2 s: John "No!", Linda "In my sights.", Lucy "Leave some for me!", Mark "Not my family.".
3. **Press.** Press the key. The execute line floats over the same unit: "I got you!", "Clean shot.", "Catch this!", "Breathe. Strike.". The role insert plays exactly as before, with no text and no change in timing. Check how the execute line reads next to the prompt line that may still be fading.
4. **Paused John.** John's prompt pauses the game. His "No!" must still appear and fade during the pause. The camera does not move for it, and the QTE still takes the key.
5. **Decline.** Let a prompt pass without pressing. When the prompt line has fully faded, a decline line shows over the same unit.
   - The first time in this fight: John "Hold fast.", Linda "Not this one.", Lucy "Next time!", Mark "Patience.".
   - Later in the fight: "Hang in there.", "I'll wait.", "Saving it.", "Another moment.".
   - There is no "too slow" or failure wording.
6. **One per role per turn.** Decline the same role twice in one enemy turn, for example two attackers on John's ally. Only the first decline speaks. Next turn it speaks again, with the second line.
7. **Toggle.** Untick `Play Decline Bark` on a unit's role handler (on the Unit_<Name> prefab or the runtime instance) and decline: no decline line. The prompt and execute lines still play.
8. **Edge cases:**
   - No barks when a role prompt could not start because another QTE was up.
   - No delayed decline for a unit that died.
   - No late popup after ending the level during a prompt.
   - The presenter is the `RoleBarkPresenter` component on the ShowStatsHoverPreview object.
