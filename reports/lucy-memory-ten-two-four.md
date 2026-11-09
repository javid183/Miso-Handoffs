# Report: Lucy's memory: "ten" → "Two." → "Four."

Plan: plans/onboarding/2026-11-09-lucy-memory-ten-two-four.md    Agent: miso-implementer    Branch: main (working tree, nothing committed)
Outcome: done (code, data and edit-mode tests). The play check is still open: AC 1–5 need THJ or the verifier in Play mode.

## What changed

All paths are under `miso/Assets/_Project/`.

New, non-core (`Features/Onboarding`, namespace `MISO.Core.Features.Onboarding`):
- `Features/Onboarding/UnitOutOfPlay.cs` (+ `.meta`): static helper that takes a unit off the board without killing it. In order: removes it from its faction controller's unit list (`controller.AllUnits`, the same list as `PhaseData.OwnedUnits`), frees its tile with the grid's own `GridCell.UnplugEntity`, hides its threat line and ghost, then switches its GameObject off. It raises no bus event. Also holds `PickToHide` (a group's in-play units minus kept tiles, each once, in list order) and `IsInPlay`. The overload `TakeOut(unit, list, freeTile)` exists so tests can run it without a level. No static state.
- `Features/Onboarding/HideUnitsSequence.cs` (+ `.meta`): the sibling of `RevealUnitsSequence`. It takes a group id from `HiddenLevelUnits`, kept tiles (`Vector2Int[]`) and fade seconds (default 0.8), plus a short wait afterwards (0.2). It fades every `SpriteRenderer` of the picked units from its own alpha to 0, then calls `UnitOutOfPlay.TakeOut` on each. `SkipStep` cuts the fade short. Menu: Game/Sequence/HideUnitsSequence.
- `Features/Onboarding/Editor/HideUnitsSequenceTests.cs` (+ `.meta`): 7 tests (listed under Acceptance criteria).

Level and sequence wiring:
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs`: the class is now `partial`. `Run()` first lays out the hidden Claws. The interruption becomes: input/HUD off → camera to room → reset call → reveal `ten` → Lucy "Then ten more!" → Linda "Two." → fade-out step → Lucy "Four." → reveal `four` → camera back → unlock Cyclone → input/HUD on. New helpers `EnsureReveal` and `EnsureFadeOut`. `FocusPoints` now averages group `ten`.
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.Claws.cs` (+ `.meta`, new partial): tile layout constants (`KeptTiles`, `FadingTiles`, `FourTiles`, `TenGroupId`, `FourGroupId`) and `LayOutHiddenClaws()`. It reuses the Claw already on a tile, or else instantiates `Unit_DarkClaw.prefab` under the cell's `OccupantRoot`, then sets it inactive with `lethalDamageXpBonus` 0 (the same overrides as the three hidden Claws had). It also sets the two groups on `HiddenLevelUnits`. `TryTileOf` reads coordinates from the cell name, because `_coordinates` isn't saved in the prefab. Re-runnable.
- `Features/Onboarding/Editor/HearthMemoryLucyTests.cs`: the old "3 in default group" test is replaced by `TwelveCuedClawsAreHiddenInTwoGroupsOnTheirTiles`. Added `TheInterruptionBringsInTenFadesEightAndBringsInTwoBetweenTheLines`. The first-stage test now expects the first dialog step to hold only "Then ten more!".
- Data, produced by running the wiring (Tools › Onboarding › Wire Memory 2 (Lucy), invoked through Unity MCP):
  - `Content/Levels/Greybox/GB_m2-lucy.prefab`: 9 new hidden Dark Claw instances. `HiddenLevelUnits` groups are `ten` (9,3 / 9,1 / 6,1 / 6,3 / 7,1 / 7,2 / 7,3 / 8,1 / 8,2 / 8,3) and `four` (10,2 / 10,3); the old group `hidden` is gone. The 3 existing hidden Claws were reused (9,3 and 9,1 into `ten`, 10,2 into `four`). The diff is additions only, apart from the groups block (checked).
  - `Resources/Sequences/Hearth/Memory2Lucy/`:
    - modified: `Memory2Lucy_Interruption_SequentialSequence.asset` (4 more steps), `Memory2Lucy_Interruption_DialogNodeSequence.asset` ("Three." removed; it now holds only "Then ten more!"), `Memory2Lucy_Interruption_Reveal.asset` (group `hidden` → `ten`), `Memory2Lucy_Interruption_CameraToRoom.asset` (focus x 4.917 → 4.0, the centre of the ten).
    - new (+ `.meta` each): `Memory2Lucy_Interruption_Two_DialogNodeSequence.asset` (Linda, left, "Two."), `Memory2Lucy_Interruption_Four_DialogNodeSequence.asset` (Lucy, right, "Four."), `Memory2Lucy_Interruption_FadeOut.asset` (HideUnitsSequence: group `ten`, keep 9,3 and 9,1, 0.8 s), `Memory2Lucy_Interruption_RevealFour.asset` (RevealUnitsSequence, group `four`, 0.6 s).

THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font) were not touched.

## Acceptance criteria

- [ ] 1. Stage 1 plays in order and leaves 4 Claws: **data verified, play not verified.** `TheInterruptionBringsInTenFadesEightAndBringsInTwoBetweenTheLines` checks this order: camera to room → reveal `ten` → "Then ten more!" → "Two." → fade step → "Four." → reveal `four` → camera back. Also checked: the fade's group and kept tiles, and that each line has its own dialog step. `TwelveCuedClawsAreHiddenInTwoGroupsOnTheirTiles` checks 10 + 2 Claws, all inactive, on the planned tiles, with the throat mouth 5,2 free. That 4 Claws remain afterwards needs a Play check.
- [ ] 2. The faded 8 leave no trace: **logic tested, play not verified.** `TakeOut_LeavesTheFactionFreesTheTileAndSwitchesTheUnitOff` checks the unit leaves the faction list, its cell is no longer occupied, and it is switched off. `TakeOut_RaisesNoDeathBirthOrDamageEvent` checks that no `unitDied`, `unitBorn` or `onUnitDamageDone` fires. The kill feedback, XP, barks, mission stats and tally all hang off those events. Why nothing else sees the 8, from reading the code:
  - Turn order, the AI, `UpcomingTurnOrder`, objectives and utility variables all read `Faction.Controller.AllUnits` / `AliveUnits`.
  - Barks, the combat log and the mission stats use `FindObjectsByType<GUnit>`, which skips inactive objects.
  - Cell occupancy is the cell's own slot, which `UnplugEntity` clears.

  In the tests, a test double stands in for the real `UnplugEntity` (it redraws cell visuals that don't exist in edit mode). Walking, targeting and the Cyclone over the freed tiles need a Play check.
- [ ] 3. Stage 2 wins when the 4 die: **not verified in play.** By code: `LivingUnitsLOCondition` counts `controller.AllUnits`, which no longer holds the 8. Its count is therefore the 2 first Claws (dead) plus the 2 kept plus the 2 new. Stage 2's "alive ≤ 0" is met when the 4 die, and `{alive_0}` should read 4 after the cut-in (`WaitThenEvaluateNewStage` re-evaluates once the sequence ends).
- [ ] 4. Skip gives the same state: **by code, not verified in play.** `SequentialSequence`'s fast-forward skips only dialog and camera steps. The reveal and fade steps still run, so a skipped cut-in ends with the same 4 Claws. Under a skip the fade still takes its 0.8 s.
- [ ] 5. Restart starts clean: **by code, not verified in play.** The hidden state lives in the prefab (inactive), and Try Again / the level button reload the level through `ProgramFlowHandler.LoadLevel`. A faded unit ends up the way a dead unit does: unparented by `UnplugEntity` and switched off.
- [x] 6. Edit-mode tests and suite:
  - New `HideUnitsSequenceTests` (7): `TakeOut_LeavesTheFactionFreesTheTileAndSwitchesTheUnitOff`, `TakeOut_RaisesNoDeathBirthOrDamageEvent`, `TakeOut_AUnitAlreadyOffOrMissingIsLeftAlone`, `PickToHide_KeepsTheKeptTilesAndSkipsUnitsNotInPlay`, `IsInPlay_NeedsAnActiveLivingUnitOnACell`, `FadeFactor_RunsFromFullToClear`, `Set_StoresGroupKeptTilesAndFade`.
  - `HearthMemoryLucyTests`: 12 tests, 2 of them new.
  - Full EditMode suite through Unity MCP in THJ's open editor: **1762 tests, 1761 passed, 1 failed**. The failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red; 42 failures in its report). It was not touched.
  - A second run of just these two fixtures: 19/19 passed.
- [x] 7. No core-system API or behaviour change: none of the files in `tech/core-systems.md` was edited. The step only calls existing public members (`FactionControllerBase.AllUnits`, `GridCell.UnplugEntity`, `GUnit.HideThreatLine` / `HideGhost`, `GameObject.SetActive`). No Tier 3 stop was needed.

## Save reset

No.

## Decisions I made

- **The 8 stay "alive" but off the board.** `GameEntity.IsAlive` has a protected setter. Every public path that clears it (`Die`, `DiePermanently`, `DieRevivable`, `FakeDie`) raises `unitDied`. Clearing it without the event would need a core API, so the unit leaves every list and cell and is switched off instead. Same behaviour as the plan (Tier 2). Risk noted below.
- **How the step chooses units:** group id plus kept tiles (`keepTiles` = 9,3 and 9,1), as the plan allowed ("a group plus which to keep"). Tiles are compared against the runtime `GridCell.Coordinates` (`grid.WorldToCell`, the same source as the cell names).
- **Which tiles the fading 8 use:** 6,1 / 6,3 / 7,1 / 7,2 / 7,3 / 8,1 / 8,2 / 8,3. That is all of 6..8 × 1..3 except 6,2, leaving column 5 (the throat mouth and both sides of it), 6,2 and 10,1 empty. The plan only said "fill room 2's free tiles" (Tier 2 detail).
- **Hidden Claws placed by the Lucy wiring script, not the grid-to-level tool.** The tool can express two groups (`level hidden [group] X,Y ...`, `GridBlockParser.ReadHidden`). But a rebuild would replace the whole level and could lose hand-set data such as the in-play Claws' HP factor overrides. So the re-runnable `HearthMemoryWiring.Lucy` now places them; no prefab YAML was edited by hand.
- **Assets reused:** the existing reveal and dialog assets keep their names. `Memory2Lucy_Interruption_DialogNodeSequence` now holds only "Then ten more!", and `Memory2Lucy_Interruption_Reveal` reveals `ten`.
- **Camera to room** now centres on the ten (world x 4.0, was 4.917, the centre of the old three). This follows from `FocusPoints` averaging the revealed group. Room 2 (6 tiles) fits the view, since the whole 10 × 3 level fits one view.
- **Fade curve** is `1 − t²` over 0.8 s, then a 0.2 s wait. Feel values, to tune in play.

## Needs THJ

None.

## Docs to update

- `plans/onboarding/2026-10-26-onboarding-levels.md`, Segment 2 (designer):
  - Grid block: draw the hidden Claws on room 2. Replace `cells 9,3 10,2 9,1 enemy hidden until the cue` and `level hidden 9,3 10,2 9,1` with `level hidden ten 9,3 9,1 6,1 6,3 7,1 7,2 7,3 8,1 8,2 8,3` and `level hidden four 10,2 10,3`. Add a note that 9,3 / 9,1 stay and the 8 fade.
  - Table, Enemies: 2 in play plus 12 hidden in groups `ten` (10) and `four` (2), default Tutorial HP 10, no kill XP bonus.
  - Table, Interruption: the new order (reveal ten → "Then ten more!" → Linda "Two." → 8 fade, no death → Lucy "Four." → reveal four → camera back). The fight is against 4 Claws.
  - Add: the hidden Claws are placed and grouped by Tools › Onboarding › Wire Memory 2 (Lucy) (`HearthMemoryWiring.Lucy.Claws.cs`). The grid tool can express both groups, but rebuilding the prefab from the block replaces the hand-set level and needs the wiring re-run.
- `plans/onboarding/onboarding-narrative-draft.md`, M2 lines (narrative): Linda "Three." becomes Linda "Two." then Lucy "Four.". "Then ten more!" is kept.
- `tech/classic-fallback.md`: no change (no new wiring point outside the level and its sequences).
- `tech/core-systems.md`: no change. A possible line under "Checked, not core": `UnitOutOfPlay` removes units through `AllUnits` and `UnplugEntity`, with no bus event.

## Risks and loose ends

- **A faded unit keeps `IsAlive == true`.** Anything that grabbed a reference to it earlier and checks only `IsAlive` would still treat it as alive. Known holder: `AIFactionBrain._unitBrains` (removed only on `unitDied`). Its turn order and prediction iterate the controller list, so the stale brains are never asked to act. `RequestPredictAllTargets` does re-register them with `GameEntityMessage` on the main thread, which is harmless. The AI plan is marked expired again by the `four` reveal's `unitBorn` right after the fade. If a later use needs a clean `IsAlive = false` without a death event, that is a core API (Tier 3).
- The fade drives `SpriteRenderer.color` alpha. If an Animator state animated the colour of a Claw's renderers, it would override the fade until the unit switches off. The Dark Claw idle doesn't appear to (not checked clip by clip).
- `GridCell._coordinates` is not saved in prefabs. Tile lookups in editor code have to read the cell name. My first in-editor read hit this; `TryTileOf` handles it.
- Seen, not changed: `AIFactionBrain.NotifyUnitsPresenceChange` does a Unity-null check (`unit &&`) and reads `unit.Faction` inside `AIWorker.Run` (worker thread). It's existing code and in THJ's uncommitted file.
- The Tools menu item did not run through MCP's `execute_menu_item` (no log, no change). I ran `HearthMemoryWiringLucy.Run()` by reflection through MCP `execute_code` instead. Same code path.

## Proposed commits

1. `feat(onboarding): a sequence step fades units out and takes them off the board without a death` (plain):
   - `miso/Assets/_Project/Features/Onboarding/UnitOutOfPlay.cs`, `UnitOutOfPlay.cs.meta`
   - `miso/Assets/_Project/Features/Onboarding/HideUnitsSequence.cs`, `HideUnitsSequence.cs.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HideUnitsSequenceTests.cs`, `HideUnitsSequenceTests.cs.meta`
2. `feat(onboarding): Lucy's memory brings in ten Claws, fades eight and brings in two more` (plain; needs 1):
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Lucy.Claws.cs`, `.cs.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLucyTests.cs`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m2-lucy.prefab`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory2Lucy/`:
     - modified: `Memory2Lucy_Interruption_SequentialSequence.asset`, `Memory2Lucy_Interruption_DialogNodeSequence.asset`, `Memory2Lucy_Interruption_Reveal.asset`, `Memory2Lucy_Interruption_CameraToRoom.asset`
     - new, each with its `.meta`: `Memory2Lucy_Interruption_Two_DialogNodeSequence.asset`, `Memory2Lucy_Interruption_Four_DialogNodeSequence.asset`, `Memory2Lucy_Interruption_FadeOut.asset`, `Memory2Lucy_Interruption_RevealFour.asset`

Per THJ's play-test-before-commit rule, commit 2 should wait for THJ's play check.

## Other branches

None (on `main` since the onboarding merge).

## How to see it

1. Open the Hearth memory mission at Memory 2 · Lucy (level `GB_m2-lucy`), or press the level's play button.
2. Turn 1: kill the two Claws with Fire Embers (or end the turn to reach the turn-2 cap).
3. The cut-in should play in this order:
   - The camera moves to room 2 and ten Claws come in.
   - Lucy "Then ten more!", then Linda "Two.".
   - Eight Claws fade out over about a second. No death animation, kill flash, shake, XP or bark.
   - Lucy "Four.", then two Claws come in at the far end (10,2 and 10,3).
   - The camera comes back and the Cyclone hint starts.
4. Check:
   - The objective reads "4 remaining".
   - Only 4 Claws act on the enemy turn.
   - The faded tiles can be walked on and targeted, and the Cyclone can move over them.
   - Killing the 4 wins the level.
   - The sisters' tally and the results show no kills for the 8.
5. Replay with the skip (hold skip during a line): the end state should be the same 4 Claws.
6. Lose or use Try Again: all 12 should be hidden again at the start.

## Fix round (review verdict FIX, one must-fix)

Review: `reports/lucy-memory-ten-two-four-review.md`. The must-fix: the fade only faded the bodies. The Claw's idle animation writes the `Shadow` colour alpha every frame, after the coroutine, so the shadow stayed opaque. The mini health bars (Canvas/Image) stayed visible too. Both then vanished at once when the unit switched off.

What changed:
- `Features/Onboarding/HideUnitsSequence.cs`: the fade now goes through a new nested `HideUnitsSequence.FadeTargets`. `FadeTargets.Prepare(units)` does three things:
  - disables every enabled `Animator` under each picked unit (`GetComponentsInChildren<Animator>`). They are not re-enabled, because the units leave the board when the fade ends.
  - collects every `SpriteRenderer` with its starting alpha.
  - gets or adds a `CanvasGroup` on each outermost `Canvas` under the unit. Nested canvases fade with their parent's group, so their alpha isn't multiplied twice.

  `Apply(factor)` sets each sprite's and each group's alpha to its start value × factor. Canvases are never switched off (`UnitMiniHealthBar.Refresh` turns them back on itself). The old private `SetAlpha` is gone; nothing else in the step changed.
- `Features/Onboarding/Editor/HideUnitsSequenceTests.cs`: new `FadeTargets_StopTheAnimatorsAndFadeSpritesAndTheOuterHealthBarCanvas`. It builds a unit with an Animator, a body sprite (alpha 0.5), a shadow sprite and a health-bar canvas with a nested canvas, then checks:
  - the animator is stopped
  - 2 sprites and 1 canvas group are collected
  - the group is added to the outer canvas only
  - at factor 0.5 the body reads 0.25, the shadow 0.5 and the group 0.5
  - at factor 0 all read 0
  - a null list is handled

Tests: full EditMode suite via Unity MCP, **1763 run, 1762 passed, 1 failed**. The failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI` (42 failures in its report, unchanged and not touched).

Not verified: how the fade looks in play (shadow and bars fading together with the body). That needs the play check.

Proposed commits: unchanged. Both changed files are already in commit 1.
