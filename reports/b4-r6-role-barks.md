# Report: B4 R6 Family Role barks (item E)

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (play check still needed)

## What changed

- `Core/Managers/GlobalEventBus.cs` (core, additive, D-069): new `public UnityEvent<FactionRoleHandlerBase, bool> onFamilyRoleOutcome = new ();` right under `onFamilyRolePrompt` in "Misc". The comment gives the contract: raised once for each role QTE that started (so always after its `onFamilyRolePrompt`), with pressed true on a press (the notice path, `onFamilyRoleActivated` comes later) and false when the prompt ran out or was force-ended without a press (the ignore path: a decline, not a failure). It is never raised when the prompt could not start, and it comes before the QTE's `qteEnded`. The file keeps its BOM and LF.
- `Core/Interactions/Runtime/PlayerController.cs` (core, additive): in `ActivateFactionRole`, one local `var roleHandler = unit.AbilityOrchestrator.FactionRoleHandler;` before `StartEvent`. The two callbacks became block lambdas: each runs its existing `SequentialActionHandler.Execute(noticeActions / ignoreActions)` first, then `GlobalEventBus.Instance.onFamilyRoleOutcome.Invoke(roleHandler, true / false)`. The could-not-start path and the R5 prompt line are unchanged. No logic changed.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (core, additive, the same pattern as `showRoleZone`):
  - Two new serialized fields after `showRoleZone`, both with tooltips: `string[] declineTexts = Array.Empty<string>()` and `bool playDeclineBark = true`.
  - Read-only getters `IReadOnlyList<string> DeclineTexts` and `bool PlayDeclineBark`.
- `Features/UI/Panels/Scripts/FactionRoleVisual.cs`: new `ShowSoloPanelWithExecuteLine()`.
  - If the role unit has a `UnitFamilyRoleExecuteText`, it plays the same solo insert through the existing `ShowWithDialogue` (the Revenge path) with that line.
  - If not, it falls back to `ShowSoloPanel(true)` as before.
- `Core/UI/Runtime/CombatLevelUIManager.cs`: `ShowFactionRoleExecutionVisual()` now calls `ShowSoloPanelWithExecuteLine()` instead of `ShowSoloPanel(true)`. One line plus a comment.
- `Core/FX/Runtime/DamageNumber.cs` and `DamageNumberManager.cs`: a new optional trailing parameter `bool ignoreTimeScale = false` on `PopText`, `Pop` and `ShowText`. When it is true, the DOTween sequence gets `SetUpdate(true)` (unscaled time). The default leaves every existing popup unchanged.
- `Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs` (+ `.meta`, new): the pure helpers.
  - `RoleBarkRules`: `BarkDuration` = 1.2, `Clean`, `DeclineLineIndex`, `DeclineAllowed`, `DeclineLine`, `DeclineDelay`.
  - `RoleDeclineTracker`: a plain object that keeps one decline bark per role per turn and counts each role's decline barks this fight. It has `ResetTurn` and `ResetFight`.
- `Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs` (+ `.meta`, new, not core): a MonoBehaviour that follows the bus like the other RoleZoneSystem presenters (polls in Update and rebinds).
  - On `onFamilyRolePrompt`: shows the unit's prompt line.
  - On `onFamilyRoleOutcome(false)`: shows a decline line when the tracker allows one. If the same unit's prompt bark is still on screen, the decline waits until it has gone (a realtime coroutine), so the two never overlap.
  - On `onFamilyRoleOutcome(true)`: does nothing (see Decisions).
  - Resets: the turn memory on `turnStarted` and `turnEnded`; the fight memory on `levelEnded` and on every bus change (new level).
  - Cleared on `levelEnded`, OnDisable and scene unload (any pending decline is dropped).
  - It skips null, dead and off-grid units, both when the event arrives and again after the delay.
  - No statics.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: one idempotent `AddComponent<RoleBarkPresenter>` line plus a comment in `Awake`, after the R5 line.
- `Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs` (+ `.meta`, new): 12 EditMode tests.
- Prefab data (minimal YAML edits, LF kept, nothing else touched):
  - Linda, Lucy and Mark: the prompt and execute override values replaced with the lines from `reports/b4-role-barks.md`. Linda's `'Have them on my sight! '` and its trailing space are gone. John keeps `No!` / `I got you!`.
  - All four `Unit_<Name>.prefab`: `declineTexts` (two lines each) and `playDeclineBark: 1`, inserted before `superTimeAbility:` in each role handler's MonoBehaviour block.

New `.cs` files are LF with no BOM, and the `.meta` files use the two-line form, like their RoleZoneSystem neighbours. All the edited `.cs` files were LF before and still are.

## Acceptance criteria

- [x] D-069 event and hooks: declared with its contract and raised from the two QTE callbacks only. `QTEButton.Finish` is guarded by `_eventActive`, so each prompt gets exactly one callback and therefore one outcome. The could-not-start path never reaches a callback. Checked by code read.
- [x] Decline gating (lines present, the `playDeclineBark` toggle, one per role per turn, element 0 for the first decline in a fight and element 1 after, reset per turn and per fight): EditMode tests in `RoleBarkRulesTests` (12/12 pass).
- [x] No "too slow" or failure wording: the only decline texts are the narrative lines. `ignoreActions` and silencing are unchanged.
- [x] Execute line plays once: it rides the existing insert, and no second popup is added (see Decisions).
- [x] Compile: no CS errors after a forced refresh and recompile. The console shows only pre-existing warnings.
- [x] EditMode suite: 173 tests, 172 pass. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, unchanged). AI untouched.
- [ ] On screen: needs the verifier's play check (see "How to see it"). That covers each role's prompt and execute bark, a deliberate decline, the toggle off, one decline per role per turn, and a bark during John's paused prompt.

## Save reset

no

## Decisions I made

- **Execute bark: wired into the existing insert, no second popup.** What happens today:
  - `ShowFactionRoleExecutionVisual` → `ShowSoloPanel(true)` sets the solo animator trigger. It never shows `unitFamilyRoleExecuteText`: nothing read `UnitFamilyRoleExecuteText` or `UnitFamilyRolePromptText` anywhere before this chunk.
  - `ShowWithDialogue` sets the same solo trigger, then shows the line in that insert's bubble.
  - So calling `ShowWithDialogue` from the presenter on `onFamilyRoleOutcome(true)` would have fired the solo trigger twice: once from the presenter and once ~0.4 s later from noticeActions, which replays the insert.
  - Instead, the existing call now goes through `ShowWithDialogue` when the unit has an execute line. One insert, with the line.
  - The presenter ignores `pressed: true`.
  - Same behaviour as the plan asked, by the route the brief preferred.
- **Over-head widget:** `DamageNumberManager.ShowText`, the same floating text `BarkManager.ShowBark` ends in.
  - I did not go through BarkManager: its show method is private, it runs graph and CSV logic, and it applies its own repeat timer.
  - DOTween runs on scaled time by default (DOTweenSettings `defaultTimeScaleIndependent: 0`), so a popup at John's timeScale 0 would freeze invisible (alpha 0). I added the opt-in `ignoreTimeScale` flag; its default is false, so other popups are unchanged.
  - Popup settings: white, Vertical movement, amount 0.5 (all three serialized on the presenter), 1.2 s, anchored at `DamageNumberTrigger.StartPosition`, falling back to the unit's position. No camera calls, no input.
- **Respects `GlobalSettingsSO.silenceBarks`**, as BarkManager does. When barks are silenced, role prompt and decline barks are silent too. The execute line in the insert is UI and still shows.
- **"First decline in a fight"** counts decline barks the role actually played, not prompts that went unpressed. So the first line a player hears is always element 0, even after the toggle was off. With a single line, it is always that line.
- **The once-per-turn mark is recorded when the decline is accepted**, even if the delayed popup is later dropped (the unit died, barks silenced, level ended). It never plays twice.
- **Decline vs prompt overlap:** the prompt bark lasts 1.2 s and the QTE window is about 1 s, so a decline would land on top of the prompt line. The decline is held back by the remaining prompt-bark time (≤ 0.2 s, realtime).
- **Outcome raised after `Execute(...)` in each callback**, not before, so a throwing listener can't stop the role flow and leave `IsInProgress` stuck. It is still raised before `qteEnded` (EndEvent runs after the callback returns).
- **The handler is captured once before `StartEvent`** (`roleHandler`), so the outcome doesn't dereference the unit again when the callback fires.
- **Prefab YAML for `string[]`:** edited directly (a plain sequence; it re-imported without errors). No subclass initialisers were needed. The base default stays empty as specified.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`:
  - The bus event `onFamilyRoleOutcome(handler, pressed)` and its contract.
  - The handler fields `declineTexts` / `playDeclineBark`.
  - `RoleBarkPresenter`, hosted by `ShowStatsHoverPreview`.
  - The execution insert now shows `unitFamilyRoleExecuteText` through `ShowWithDialogue`.
  - `DamageNumberManager.ShowText(..., ignoreTimeScale)`.
- `design/gdd/family-systems.md` (via the designer): decline barks, one per role per turn, element 0 then 1, and the per-unit toggle.
- `plans/2026-10-18-family-role-readability-design.md`: the R5 report already noted the "Too slow" rows are stale. Also, the design's assumption (decline inferred from public events) was replaced by D-069.
- `build-log.md`: the R6 entry.

## Risks and loose ends

- **Insert timing with the line (play check).** `ShowWithDialogue` freezes the insert animator (`speed = 0`) for `dialogueDuration` (1.5 s, scaled `WaitForSeconds`) once the solo clip's animation event fires.
  - The FR animators run on scaled time (`m_UpdateMode: 0` in `FTPPanel.prefab`). During John's paused press, the insert and its bubble only move after noticeActions restores timeScale 1, about 1.2 s real later. This is the same as today's insert.
  - The insert then holds about 1.5 s longer than before, while the role effect plays under it. That is the Revenge behaviour.
- **`ShowWithDialogue` fragility (existing code, unchanged).**
  - It subscribes to `AnimationTrigger.OnAnimationTriggeredEvent` each call and only unsubscribes when the event fires. If a unit's solo clip lacked the event, the line would show at that unit's next insert.
  - It picks the animator by `roleUnit`. If another prompt calls `SetData` before the event fires, the wrong bubble could be used.
  - All four FR animators have an `AnimationTrigger` (4 in `FTPPanel.prefab`), and Revenge uses the same path.
- **No dialogue for an unknown role unit.** `ShowWithDialogue` returns early for a unit that is not John, Linda, Lucy or Mark. That only matters for a future role unit with an execute line; `ShowSoloPanel` does nothing for it today either.
- **Overlap with BarkManager.** Role barks don't go through BarkManager's repeat timer, so a graph bark (e.g. on damage) can float at the same unit at the same moment. Play check.
- **Popups on screen at teardown.** Popups already showing are not killed on `levelEnded`; they fade within 1.2 s. On scene unload they go with the DamageNumberManager.
- **Force-ended prompts count as declines.** `QuickTimeEventHandler.ForceEndEvent` ends the active QTE through the ignore path. Today it is only called for the reversion QTE, John's Command Shield Dash and Catch & Return, not for role prompts. If a future caller force-ends a role prompt, a decline bark would play.
- **Dev scene.** `Scenes/DevScenes/TestLevel.unity` has its own LindaFactionRoleHandler (not the prefab's), so there Linda gets the code default: no decline lines. The prompt and execute lines still come from her GUnit.
- **Console.** One "Internal error - unexpected guid mismatch" assert reappeared after the refresh (one this time, not two). It has no stack trace and comes with no compile errors. The new `.meta` GUIDs are fresh uuid4 values.
- **Lucy prefab.** The roleZoneColor alpha change by THJ was **no longer in the working tree** when I started: `git status` showed `Unit_Lucy.prefab` clean, and `git diff` was empty before my edit. So every hunk in `Unit_Lucy.prefab` now is mine: the two text values at ~l.455/459 and the four inserted lines at ~l.2715. THJ may want to check whether his alpha tweak was saved somewhere else or lost.
- **Working tree, not mine.** `ProjectSettings/EditorSettings.asset` shows ` M` (unstaged; see D-069). `ProjectSettings.asset`, `Packages/manifest.json` and `packages-lock.json` are also modified by the editor. Do not stage any of them.

## Proposed commits

1. `feat(bus): onFamilyRoleOutcome event, raised once per started Family Role prompt with pressed true/false (B4 R6, D-069)` (core, own commit)
   - `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
2. `feat(roles): decline bark lines and playDeclineBark toggle on Family Role handlers (B4 R6, D-063)` (core, own commit)
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
3. `feat(fx): opt-in unscaled time for floating text popups (B4 R6)` (plain, shared FX)
   - `miso/Assets/_Project/Core/FX/Runtime/DamageNumber.cs`
   - `miso/Assets/_Project/Core/FX/Runtime/DamageNumberManager.cs`
4. `feat(ui): Family Role execute line in the role insert, prompt and decline barks over the role unit (B4 R6)` (plain, depends on 1 to 3)
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/FactionRoleVisual.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs.meta`
   - `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`
5. `data: Family Role prompt, execute and decline lines for John, Linda, Lucy and Mark (B4 R6)` (data, depends on 2)
   - `miso/Assets/_Project/Features/Player/John/Prefabs/Unit_John.prefab` (one hunk: 4 inserted lines at ~l.2825)
   - `miso/Assets/_Project/Features/Player/Linda/Prefabs/Unit_Linda.prefab` (two hunks: text values ~l.372/376, 4 lines at ~l.2495)
   - `miso/Assets/_Project/Features/Player/Lucy/Prefabs/Unit_Lucy.prefab` (two hunks: text values ~l.455/459, 4 lines at ~l.2715; all mine, see Risks)
   - `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab` (two hunks: text values ~l.273/277, 4 lines at ~l.2809)

Do not stage `ProjectSettings/*` or `Packages/*`.

## Other branches

`thj/home-test` gets this with the rest of B4 on its next merge of `main`.

## How to see it

1. Open a combat level with John, Linda, Lucy and Mark. Shared FTP must be at least 1.
2. **Prompts and execute lines.** Set up each role's trigger: an enemy attacks an ally inside John's diamond; an enemy ends a move on Linda's row or column; an enemy attacks an ally near Lucy; an enemy attacks next to Mark's zone. When each prompt appears, a short white line floats over the role unit's head for about 1.2 s:
   - John: "No!"
   - Linda: "In my sights."
   - Lucy: "Leave some for me!"
   - Mark: "Not my family."
3. Press the key. The role insert plays with the execute line in its bubble ("I got you!", "Clean shot.", "Catch this!", "Breathe. Strike."). Only one insert should play, not a replayed one.
4. **Paused John.** John's prompt pauses the game. His "No!" must still appear and fade during the pause. The camera does not move for it, and the QTE still takes the key.
5. **Decline.** Let a prompt pass without pressing. Right after the prompt line fades, a decline line shows over the same unit: the first time in this fight John "Hold fast.", Linda "Not this one.", Lucy "Next time!", Mark "Patience.". Later in the fight: "Hang in there.", "I'll wait.", "Saving it.", "Another moment.". No "too slow" or failure wording.
6. **One per role per turn.** Decline the same role twice in one enemy turn (e.g. two attackers on John's ally): only the first decline speaks. Next turn it speaks again, with the second line.
7. **Toggle.** Untick `Play Decline Bark` on a unit's role handler (Unit_<Name> prefab or the runtime instance) and decline: no decline line. Prompt and execute still play.
8. **Edge cases.** No barks when a role prompt could not start because another QTE was up. A unit that died gets no delayed decline. Ending the level during a prompt leaves no late popup. The presenter is the `RoleBarkPresenter` component on the ShowStatsHoverPreview object.
