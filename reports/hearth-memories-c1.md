# Report: Memory 4's new ending (Hearth memories, build chunk C1)

Plan: plans/onboarding/2026-11-10-hearth-memories-tech.md (C1 only)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (code, data and tests). THJ's play check still open.

## What changed

- `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`: the `CombatLevel` win stages only, edited in the editor (Unity MCP, `LoadPrefabContents` + `SerializedObject` + `SaveAsPrefabAsset`). I read the stages back before and after, and `git diff` touches only `lObjectives` overrides (+49/-13 lines):
  - Stage 1 (Bloom): its hidden turn-cap objective is removed. Any Bloom Claw dead → `Arrival`, as before.
  - Stage 2 (hold and clear): group `All`, **one objective** with two conditions, both required (`All`, `Reevaluate`): John on (6,5) (the existing `UnitTileOccupiedLOCondition`) and a new `EntitiesDestroyedLOCondition` (`All`) on the Claws at (9,8), (10,7) and the one placed at (6,4), which the PostBloom sequence walks to (7,7). Text: "John holds the mouth. Clear the den." The cap objective is removed. On complete: `Memory4Mark_Hold_SequentialSequence`, unchanged.
  - Stage 3 (the Duo): one objective, the existing destroyed condition cut down to the three `top` Claws (8,7), (9,7), (9,6) (`All`). Its cap and the "Hold the den mouth with John." objective are removed. Text kept: "Kill the dark claws near the cub." There is no on-complete sequence, so winning plays the outro `End`.
  - Nothing else in the prefab changed: units, hidden groups, pools, locks, hints and the `top` tiles at 7 HP are as they were.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_John_DialogNodeSequence.asset`: a second John node, "Here they come.", after "I'll hold them off. You save them." (added in the editor by copying the existing node).
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_End_Mother_DialogNodeSequence.asset`: "She held on until the last Claw fell." → "She held on until we reached her."
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs` (retired tool; the tests read its constants): the turn-cap constants are removed. `HoldObjectiveText` has the new text. `SaveHoldObjectiveText` and `TopClaws` / `SaveStageClaws` are removed, replaced by `HoldStageClaws` (the three Claws stage 2 waits for). The comments now describe the new stages.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Level.cs`: `WireStages` now builds the new three stages with no caps. Stage 2's objective has two conditions (new `JohnOnTheDenMouthAndClawsDead`; `Destroyed` is split so its filling step, `FillDestroyed`, can be reused). The tool stays retired and was not run.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs`: John's hold lines and the outro line updated, so a re-run can't bring back the old text.
- `Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs`: the stage tests are rewritten for the new shape:
  - `ThereAreThreeQueuedStagesWithNoTurnCap`, `StageOneEnds...`, `StageTwoNeedsJohnOnTheDenMouthAndTheClawsNearTheCubDeadAndPlaysTheHold`, `StageThreeWinsWhenTheThreeRevealedClawsAreDead`.
  - The hidden-unit check now looks at every condition.
  - The PostBloom check uses `HoldStageClaws`. The route test is renamed `JohnsRouteToTheDenMouthIsSixSteps`.
  - The hold and outro tests expect the new lines.

All edited files keep LF line endings and have no BOM, as before.

## Acceptance criteria

- [x] 1. Three stages as specified, no caps, no "Turns left" line. Evidence: the prefab read back after the edit, and `ThereAreThreeQueuedStagesWithNoTurnCap` (one objective per stage, no `TurnReachedLOCondition`, no "Turns left"). Memory 4 never had a "Turns left" line.
- [x] 2. Stage 2 completes only with John on (6,5) and the three cub-side Claws dead, in either order. Data: one objective, conditions `All`, both `Reevaluate`; the destroyed set is (9,8), (10,7) and the (6,4)→(7,7) Claw. In code (`LevelObjective.Evaluate`), the check happens whenever objectives are evaluated, so the stage completes on whichever comes last. If John steps off the mouth before the last kill, the stage waits until he is back. Tested by `StageTwoNeeds...` for the data only. **Not verified in play**: the "either order" timing is play-check item 3.
- [x] 3. On completion the order is: John's lines → camera to the den (`Memory4Mark_Hold_CameraUp`, centred between the `top` tiles) → reveal of the `top` group → Mark–Lucy Duo unlock (the `GuidedAbilityHint` is `WhenUnlocked`, so it pulses) → Duo lines → camera back → input and HUD on. This is the existing `Hold` sequence: it already ran in this order. It now plays later because it hangs off the merged stage, so no steps had to move. Tested by `TheHoldRevealsTheTopClawsAndUnlocksOnlyTheMarkLucyDuo` and `TwoHintsPoint...`. **Not verified in play.**
- [x] 4. Stage 3 completes when the three revealed Claws die. Its only condition lists those three units, so the pools and the left-side Claws can't block it. The level checks stage 3 only after the Hold sequence (which reveals them) has finished. Tested by `StageThreeWins...` and `TheSaveStageCannotCompleteBeforeTheTopClawsAreRevealed`. **Not verified in play.**
- [x] 5. Mark tests updated and green: 32/32. Full EditMode suite (Unity MCP, editor open): 1763 tests, 1762 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red; not touched or re-baselined).

## `HiddenLevelUnits` reveal on an occupied `top` tile (checked in code)

`HiddenLevelUnits.RevealUnit` switches the Claw on, initializes it and calls `GridCell.PlugEntity` on its own cell (a core system; I only read it).
- If a hero stands there, `PlugEntityInternal` fails (`CanOccupy` is false). `GetNearestPluggableCell` then does a breadth-first search over the cell's adjacent cells (it passes through occupied cells) and puts the Claw on the first cell it can occupy. The Claw slides there from its own tile (`MoveEntityToCell`).
- The hero is not moved and nothing is skipped. All three Claws still come in and still count for stage 3, wherever they land.
- The only failure case is "no free cell anywhere". The Claw is then switched off again with a warning and would read as dead for stage 3 (the destroyed condition treats inactive or missing units as dead). That can't happen on this map.
- Design risk: a displaced Claw can land outside the safe block. Example: a hero on (8,7) can push the Claw to (7,7) or (8,6), which the design marks as risky tiles. It can then be more than 4 steps from where the Duo is fired, so the Duo may not end the memory in one go. The design's fallback is to move the `top` tiles to (7,8), (8,8) and (10,8). That is THJ's call after the play check; I did not change them.

## Save reset

No.

## Decisions I made

- Stage 2 is **one objective with two conditions** (`All`), not two objectives in an `All` group. Both read as "both at once", and only one objective line shows either way. I picked this because the plan says "one paired objective".
- The John line ("Here they come.") is **added after** the existing "I'll hold them off. You save them.", not used as a replacement: the dispatch marks the other two lines as replacements but not this one. So the beat reads: John commits, warns, the camera pans to the new Claws. If THJ wants only the new line, delete node 0 of `Memory4Mark_Hold_John_DialogNodeSequence` (and the matching line in `Sequences.cs` and the test).
- Stage 3 keeps the existing visible text "Kill the dark claws near the cub." (the narrative gave no new stage 3 line).
- Stage 1's group mode stays `Any` in the prefab (one objective, so it makes no difference). The retired `WireStages` would write `All` there. Same behaviour.
- The camera "to the den" is the existing `Hold_CameraUp`. Kept as is.
- No new runtime code and no new statics.

## Needs THJ

None beyond the play check (text and feel). The open play-check items are in the design plan, "To check in play (Memory 4)" 1 to 5.

## Docs to update

- `plans/onboarding/2026-10-26-onboarding-levels.md` (Hearth tables, Memory 4 rows) and the GDD `missions-structure.md` (Hearth stages): the new three stages, no caps (designer).
- `onboarding-narrative-draft.md`: the three lines are in, in the place the dispatch gave. "Here they come." was added rather than used as a replacement (see Decisions).
- `tech/classic-fallback.md`: no change (no new wiring point).

## Risks and loose ends

- The prefab keeps orphaned override lines for the removed cap conditions and array slots past the new sizes. Unity ignores them, and older ones of the same kind were already there. The diff stays small this way. Cleaning them up would mean reverting overrides, which is wider than this chunk.
- The objectives were evaluated for completion in code only. The win flow (Hold sequence → stage 3 checked only after it → outro) is as built, but not checked in play.
- Displaced reveal (above): if Mark or Lucy end on (8,7), (9,7) or (9,6), a Claw lands one tile over. Watch whether the Duo still ends the memory.
- `AIRegressionTest.Baseline_MatchesCurrentAI`: still red, same test, 42 check failures in this run. Not touched.
- THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font) were not touched; leave them out of the commit.

## Proposed commits

1. `feat(onboarding): Mark's memory ends on John holding the den mouth, then three new Claws for the first Duo`. Files:
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_John_DialogNodeSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_End_Mother_DialogNodeSequence.asset`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Level.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs`

   (plain: level data plus editor code and tests that only work together; no `.meta` changes, no new files)

## Other branches

None.

## How to see it

1. Open Unity on `thj/after-hearth` and play Memory 4 (Mark's telling) from the Hearth.
2. Bloom as before (Linda's arrow through Lucy's Cyclone) → Arrival plays.
3. The objectives panel shows one line: "John holds the mouth. Clear the den." No turn count.
4. Walk John to the den mouth (6,5) (prefab cell; column 7 in the paper drawing) and kill the Claws by the mother, (9,8) and (10,7), plus the Claw that walked to (7,7). Try both orders: the stage completes on whichever comes last. Step John off the mouth before the last kill: nothing should happen until he is back.
5. On completion: John says "I'll hold them off. You save them." then "Here they come.", the camera pans to the den, three Claws appear on (8,7), (9,7), (9,6), the Mark–Lucy Duo unlocks and pulses, and Mark and Lucy's lines play.
   - Also try ending stage 2 with Mark or Lucy standing on one of those tiles: a Claw should slide onto a free cell next to it.
6. Objective: "Kill the dark claws near the cub." Fire the Duo, kill the three, and the memory wins even with left-side Claws and pool Claws still alive. The outro says "She held on until we reached her."

---

## Round 2 (after THJ's hand edits; D-482 to D-484)

Outcome: done. THJ's edits stand. Wiring and tests now follow his prefab. Play check still open.

### Memory 4 structure now (prefab read back after the edit)

| Stage | Objectives (group `All`) | On complete |
|---|---|---|
| 1 Bloom | hidden: any Bloom Claw dead (1,4), (5,4), (3,5), (3,6) | `Arrival` |
| 2 Hold and clear | **A** "John: reach the den mouth.": John on (6,5), `Reevaluate`. **B** "Defeat the dark claws.": THJ's 8 Claws dead (`All`, `Reevaluate`), listed by start tile: (9,8), (10,7), (6,4) (walks to (7,7)), Mark's pair (10,2) and (12,2), Bloom Claws (5,4), (1,4), (3,5). Not listed, on purpose: Bloom (3,6), the den's west Claw, the `left` group, pool Claws. | `Hold` (THJ's order, unchanged: John's lines → **ResetTurn** → camera up → reveal `top` → unlock Duo → Duo lines → camera back → input/HUD on) |
| 3 The Duo | One objective, THJ's version unchanged: "Clear the den while John holds the mouth." = the three `top` Claws dead AND John on (6,5) | none → win → outro `End` |
| Lose | the existing defeat condition (`LivingUnitsLOCondition`, Bergsons) changed from "alive ≤ 0" to **"dead ≥ 1"** (`NotExist`, `GreaterThanOrEqual`, 1) | standard defeat → Try Again |

### What changed in round 2

- `GB_m4-mark.prefab`, edited in the editor (Unity MCP `LoadPrefabContents` + `SerializedObject`). I diffed it against a copy saved just before the edit. Only these overrides moved:
  - Stage 2's single objective split in two. Objective A keeps THJ's John condition. Objective B holds his 8-Claw condition: the same object, re-assigned, so it has a new managed-reference id but the same 8 entities.
  - The defeat condition's `state`, `comparisonStrategy` and `count`.
  - Untouched: stage 1, stage 3, the Hold sequence, the reset step, units, groups.
- Lose rule. The existing defeat group was enough; no new condition type and no runtime code.
  - Dead units stay in the faction controller's `OwnedUnits`, which is never pruned, so `_dead` counts them.
  - Units tagged `EntityState.IgnoreObjective` are skipped. Lucy's decoy carries that tag, so it doesn't trigger a loss.
  - Lost goes through the same defeat path as before (all dead), so Try Again is unchanged. **Not checked in play.**
  - Memories 1 to 3 still have "all Bergsons dead" (read, not changed). That is C2's or THJ's call.
- `HearthMemoryWiring.Mark.cs`:
  - `HoldObjectiveText` is replaced by `HoldJohnObjectiveText` / `HoldClawsObjectiveText`.
  - `SaveObjectiveText` is now THJ's stage 3 text.
  - `HoldStageClaws` is THJ's 8 tiles (`TopVisibleClaws` + den east Claw + `ArrivalClaws` + the first three `BloomClaws`), with a comment on the Claws left out.
  - Summary comment updated.
- `HearthMemoryWiring.Mark.Level.cs` (retired `WireStages`):
  - Stage 2 is built as two objectives.
  - Stage 3 is built as one objective with both conditions (`TopClawsDeadAndJohnOnTheDenMouth`).
  - The defeat group gets "any of the family falls" (`AnyOfTheFamilyFalls`).
  - John's condition is split into a fill helper (`FillJohnOnTheDenMouth`) so it can be the second condition.
  - The C1 helper `JohnOnTheDenMouthAndClawsDead` is gone.
  - Not run.
- `HearthMemoryWiring.Mark.Sequences.cs`: the Hold builder adds `BuildCall("Memory4Mark_Hold_ResetTurn", ResetCallId)` after John's lines, as in the Arrival.
- `HearthMemoryMarkTests.Flow.cs`:
  - The stage tests are rewritten: `StageTwoShowsJohnOnTheDenMouthAndTheClawsAsTwoObjectivesAndPlaysTheHold` and `StageThreeWinsWhenTheThreeRevealedClawsAreDeadWithJohnOnTheDenMouth`.
  - New test `TheMemoryIsLostWhenAnyOfTheFamilyFalls`.
  - The stage-count test allows two objectives per stage.
  - The hidden-unit test lets stage 2 count the `arrival` group, which the Arrival reveals before stage 2 is first checked. Nothing else hidden is allowed.
  - Stage 3 no longer uses `.Single()` on the first condition.
  - The Hold test expects the reset step between John's lines and the camera, calling `reset`.

### Acceptance (round 2)

- [x] Stage 2 has two objectives in the same stage (group `All`), each with one condition, so each ticks on its own. Tested.
- [x] Stage 3 is THJ's version, unchanged. Tested.
- [x] Lose when any Bergson falls. Data plus test. **Not verified in play**, nor Try Again after it.
- [x] Wiring and tests synced to the prefab. Mark tests 33/33.
- [x] Full EditMode suite: 1764 tests, 1763 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, 42 check failures, untouched).

### Risks (round 2)

- With "dead ≥ 1", any hero death now ends Memory 4 at once. That includes deaths during scripted moments: pools spawning next to Linda, Mark's arrival fight.
- The objective panel text for stage 2 is two separate lines now. Check how each ticks in play.
- More orphaned override lines past the array sizes in the prefab (harmless, as in round 1).

### Proposed commit (replaces the round 1 list)

1. `feat(onboarding): Mark's memory ends on John holding the den mouth, a fresh turn and three new Claws for the first Duo; lost if any of the family falls`. Files:
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-mark.prefab`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_ResetTurn.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_ResetTurn.asset.meta`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_John_DialogNodeSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_End_Mother_DialogNodeSequence.asset`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Level.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs`

   Leave THJ's unrelated files out (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, TMP fallback font).

### How to see it (round 2)

1. Play Memory 4. After the Arrival, the panel shows two lines: "John: reach the den mouth." and "Defeat the dark claws.". Each ticks on its own; John stepping off the mouth unticks his.
2. When both are done: the Hold plays with a fresh turn for the Duo. Stage 3 reads "Clear the den while John holds the mouth.".
3. Let any hero die at any point: the memory is lost at once. Try Again restarts it.
