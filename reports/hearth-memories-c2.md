# Report: Memories 1 to 3, caps off, no Watch, Fire Embers page, lose on any fallen Bergson (Hearth memories, build chunk C2)

Plan: plans/onboarding/2026-11-10-hearth-memories-tech.md (C2 only) + D-485    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (code, data, tests). THJ's play check still open.

## What changed

Editor code (wiring tools; all LF, no BOM, as before):
- `Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`: `TurnCaps` and the "Turns left" line removed (each stage has its goal objective alone). Panels: one page, "Moving and AP", with "Each shot spends an arrow." after the AP cost line; the Watch page and its image constant are gone. New `DrainedFpAmount = -99`, written into the level's `LevelStartFPFiller` by `DrainFamilyTimePoints`. Calls the shared lose rule.
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs`: `FirstStageTurnCap` / `SecondStageTurnCap` removed, no turn objectives in either stage. New Fire Embers page (`BuildPanels`, `BuildTutorialSequence`) put in the start sequence after Lucy's line and before `EnablePlayerInput`. Calls the lose rule.
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.Defeat.cs` (new): `LoseWhenAnyOfTheFamilyFalls`, the same condition Memory 4 uses (`LivingUnitsLOCondition`, Bergsons, `NotExist`, `GreaterThanOrEqual`, 1) on the level's one defeat group. Shared by the three tools.
- `Features/Onboarding/Editor/HearthMemoryWiring.John.cs`: `TurnCap` and the turns objective removed; calls the lose rule.

Data (produced by running the three tools through the editor menu, not hand-edited):
- `Content/Levels/Greybox/GB_m1-linda.prefab`, `GB_m2-lucy.prefab`, `GB_m3-john.prefab`: only override changes (objective array sizes 2 to 1; the defeat condition's `state`, `comparisonStrategy`, `count`; and in Memory 1 the filler's `fpAmountToFill` 99 to -99).
- `Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Start_Panels.asset`: Watch page removed, merged text.
- `Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Start_SequentialSequence.asset`: one step added (the tutorial).
- New: `Memory2Lucy_Start_Panels.asset`, `Memory2Lucy_Start_TutorialSequence.asset` (+ `.meta` each).

Tests: `HearthMemoryLindaTests.cs`, `HearthMemoryLucyTests.cs`, `HearthMemoryJohnTests.cs`, `HearthMemoryLevelsTests.cs` (details below).

## Wiring tools: what they would change, checked

I backed up the three prefabs and `Resources/Sequences/Hearth` before running. After running each tool I diffed against the backup and against git. Only the intended lines moved (above); no hand tweak on Memory 1 to 3 was reverted, so nothing was stopped. Per tool: Linda changed the three stages, the filler, the panels; Lucy and John changed the stages and the defeat condition; Lucy also the start sequence. Memory 4 was not touched.

Memory 2's gag after the Lucy re-run: `git status` shows the prefab changed only in the two objective sizes and the defeat condition (the hidden groups `ten` and `four` are not in the diff); the interruption, `Reveal`, `FadeOut`, `RevealFour`, the three dialog steps (`Then ten more!`, `Two.`, `Four.`), camera and reset assets are byte-identical to the backup (`diff -r` lists only the start sequence and the new panel assets). `TwelveCuedClawsAreHiddenInTwoGroupsOnTheirTiles` and `TheInterruptionBringsInTenFadesEightAndBringsInTwoBetweenTheLines` pass.

## Acceptance criteria

- [x] 1. No memory 1 to 3 turn cap or "Turns left" line; each stage advances on its objective. Evidence: prefab read back (win groups have one objective each; no `TurnReachedLOCondition`). Tests `ThreeStagesInAQueue`, `NoStageHasATurnCapOrATurnsLeftLine` (Linda), the Lucy stage tests, `WinningNeedsTheKillCountAloneWithNoTurnCap` (John), and `NoMemoryEndsOnATurnCountAndEveryOneIsLostWhenAnyOfTheFamilyFalls` (all four memories). Stage advance in play: **not verified in play**.
- [x] 2. Memory 1 starts with 0 FTP, Watch can't fire, no Watch page, merged page shows. Evidence: filler `fpAmountToFill` is -99 (`FamilyTimePoints.Produce` goes through `SetValue`, which clamps to 0; the same -99 is already used by other levels), test `TheMemoryStartsWithNoFamilyTimePointsSoWatchCannotPay`; page test `TheStartHasTheHearthLineAndTheMovingAndApPanelAlone` (1 page, arrow line after the AP line, no Watch text). Pool at 0 and Watch not paying: **play check**.
- [x] 3. Memory 2 shows the multi-shot page at level start, gag unchanged. Evidence: start sequence is now dialog, tutorial, input on; tests `TheStartShowsTheFireEmbersPageAfterLucysLineAndBeforeInputReturns`, `TheFireEmbersPageIsShownOnceAtTheStartAndNotInTheInterruption`; gag assets identical (above). The page shows before any unit can act (input is still off) and the interruption is hung on stage 1, which only completes after two Claws die. The page looking right: **play check**.
- [x] 4. Tests updated and green. EditMode full suite: 1772 tests, 1771 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched).
- [x] D-485. Memories 1 to 3 lose when any Bergson falls: the existing defeat condition went from "alive <= 0" to "dead >= 1" (count 1, `NotExist`, `GreaterThanOrEqual`), as in Memory 4. Test in each memory's tests and in `HearthMemoryLevelsTests`. **Not verified in play**, nor Try Again after it.

## The two checks on the Fire Embers page (done in data and code)

(a) Lucy's start loadout. Her primary attack's base level is the main ember plus one sidewinder (2 effects, so 2 targets); `RequiredTargetCount` counts the effects at her current upgrade level (`GetRequiredTargetCount`). The level does not set her level: it comes from her saved skill tree. The Hearth is the first mission, before the River guided spend on Sidewinders, so a fresh save is at base and the page ("a main ember and a sidewinder ember") is right. If someone replays the Hearth after buying Sidewinders she throws more, and the page undercounts. Wording not changed (a Hearth replay with a bought upgrade is the only gap; say if you want "sidewinder embers" to be safe).
(b) Same enemy twice. Target selection adds the clicked cell with no check against earlier picks (`FactionControllerBase`, the target-selection state), `CheckTargetSelectionCondition` is per effect, and the damage preview sums per target (`AbilityDamagePreview` accumulates in a dictionary keyed by unit), which is how a double pick is meant to read. So the code allows it and each ember is its own effect on its pick. **Not played**; confirm that the second ember on the same Claw damages it (play check).
The page text is therefore exactly the narrative text, with no adjustment. The image is the same placeholder panel image Memory 3 uses.

## Tests changed

- Linda: `ThreeStagesInAQueue` (one objective, no turn condition), new `NoStageHasATurnCapOrATurnsLeftLine`, `TheMemoryStartsWithNoFamilyTimePointsSoWatchCannotPay`, `TheMemoryIsLostWhenAnyOfTheFamilyFalls`; the two stage tests lost their cap-visibility lines; the condition-sharing test counts 3; the panel test is now `TheStartHasTheHearthLineAndTheMovingAndApPanelAlone`.
- Lucy: first-stage test renamed `...EndsOnTwoDeathsAndPlaysTheInterruption`, second-stage test `...WinsOnEveryEnemyDeadWithNoTurnCap`; new lose test, `TheStartShowsTheFireEmbersPage...`, `TheFireEmbersPageIsShownOnce...`.
- John: `WinningNeedsTheKillCountAloneWithNoTurnCap`, new lose test.
- Levels: `NoMemoryEndsOnATurnCountAndEveryOneIsLostWhenAnyOfTheFamilyFalls` covers all four memories.

## Save reset

No.

## Decisions I made

- Where the lose rule lives: a new partial `HearthMemoryWiring.Lucy.Defeat.cs` called by the three tools (instead of editing the prefabs by hand), so a re-run keeps it. Memory 4's own copy in `Mark.Level.cs` (retired tool) was left alone (same behaviour, no scope creep).
- The Fire Embers page sits after Lucy's opening line, not before it, matching Memories 1 and 3 (dialog, then page, then input on).
- Group aggregation stays `Any` on the single-objective win groups (same result as `All` for one objective; unchanged by the tools).
- Memory 2 stage 1 now ends only on two deaths. Before, turn 2 also ended it. A player who kills nothing never triggers the interruption.

## Needs THJ

- Play check items: the Fire Embers page and its image, Memory 1 with 0 FTP (and the FP bar looking fine empty), same-Claw double pick, the lose rule on each memory.
- Lose rule risk, as in Memory 4: any hero death ends the memory at once. Memory 3 spawns nothing scripted next to heroes as far as I read, but I did not check for scripted hero deaths in Memories 1 to 3.

## Docs to update

- `plans/onboarding/2026-10-26-onboarding-levels.md` Hearth tables (Memories 1 to 3: no caps, M1 FTP 0 and no Watch, M2 page, lose rule) and the GDD `missions-structure.md` Hearth stages (designer).
- `plans/onboarding/onboarding-narrative-draft.md`: AH-1 and AH-2 are in, with no changes.
- `tech/classic-fallback.md`: no change (no new wiring point).
- Plan commit log: C2 hash after commit.

## Risks and loose ends

- The three prefabs keep orphaned override lines for the removed turn conditions and the objective slots past the new array sizes (harmless, same as in C1; a cleaner diff than reverting overrides).
- `AIRegressionTest.Baseline_MatchesCurrentAI` is still red, same test, untouched.
- THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, TMP fallback font) were not touched; leave them out.
- Unity's console showed a harmless "Objects are trying to be loaded during a domain backup" line during the recompile; not from this chunk.

## Proposed commits

1. `feat(onboarding): the first three Hearth memories lose their turn caps, Memory 1 starts without family time points and Memory 2 opens on a Fire Embers page; any fallen hero loses them`. One commit: the tools, the data they produce and the tests only work together. Files:
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Lucy.Defeat.cs` and `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLindaTests.cs`, `HearthMemoryLucyTests.cs`, `HearthMemoryJohnTests.cs`, `HearthMemoryLevelsTests.cs`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-linda.prefab`, `GB_m2-lucy.prefab`, `GB_m3-john.prefab`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Start_Panels.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Start_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Start_Panels.asset` and `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Start_TutorialSequence.asset` and `.meta`

   (If THJ wants it split: code and tests first, then the three prefabs and sequence assets; the tests need the data, so the two halves would not both be green alone.)

## Other branches

None.

## How to see it

1. Open Unity on `thj/after-hearth`; play the Hearth from its first memory.
2. Memory 1 (Linda): after Margaret's line one page, "Moving and AP", with four bullets including "Each shot spends an arrow."; no Watch page. FTP bar is empty; Watch never offers. The objective panel never shows "Turns left in the memory". Stages move on kills, then Linda reaching the gather tile, then the last Claws. Let any hero die: the memory is lost.
3. Memory 2 (Lucy): the grid fades in, Lucy's line, then the "Fire Embers" page, then control. Attack: pick one target per ember, try the same Claw twice and check it takes both hits. Kill two Claws: the ten, "Two.", fade, "Four." gag plays as before. No turn count, no turn ending the stage.
4. Memory 3 (John): one stage, "Defeat four Claws: x of 4.", no turn count. A fallen hero loses it.
