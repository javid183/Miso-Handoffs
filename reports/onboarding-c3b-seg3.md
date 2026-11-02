# Report: C3b segment 3, John's memory level (`GB_m3-john`)

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. Compiles; EditMode 1194 run, 1193 pass, the one failure is `Baseline_MatchesCurrentAI` (name read from the run). Not play-checked. Save not reset. Nothing committed.

## Built
- **Start:** disable input, hide HUD, grid hidden at once (duration-0 grid sequence) then faded in, John's lines, the one panel, input and HUD back. Lines: "Every Claw in that cave wanted my girls. Not one of them got them." / Lucy "Dad, you were behind us." / "In front. Always in front." (draft M3-1 to M3-3) and then "Stay where I can reach you." (the plan's cue line). Four lines at the start is more than the table's one; trim in the script if too long.
- **Panel (one page, "Shield Up"):** Shield Up arms Wrath until John's next turn; each hit while it lasts stacks Wrath; his next damaging ability spends the stacks for extra damage. Image: `Tut-FR-1.png` (reused).
- **Guided action (Shield Up, turn 1):** new non-core component `GuidedAbilityHint` on the level root, pointed at `John_Ability_Shield`. While John's panel shows that ability's button, the button pulses in size (up 15% each second); it stops when the ability is performed or the level passes turn 1, and the button gets its size back. It only reads the HUD (`UnitAbilityButtonUI` found in the scene, `Ability.Preset` compared) and scales that button's transform; no input, ability or HUD logic changed, no core file touched, no statics. Not built: a spotlight or marker on John himself. The existing `UISpotlightHandler` is a full-screen dim overlay (used by the Family Role notice) and I did not risk it blocking clicks; so the player still has to pick John (the panel says so). If you want John highlighted too, options: select John automatically at level start (touches `PlayerController` selection, core: needs your OK) or a small world-space marker on John (new non-core piece).
- **Win:** one stage, Any: 3 Claws dead (`LivingUnits` Enemy dead >= 3) or turn 2 condition (fires when turn 3 begins). Both lines on the HUD: "Defeat three Claws: {dead_0} of 3." and "Turns left in the memory: {remaining_0}."
- **End:** disable input; Lucy "Dad, who got the most?", John "You both did.", Lucy "I did.", Linda "I did." (back to back, as the draft allows); `FadeOutGridSequence`; cutaway over the placeholder still (Mark "You're all forgetting the best part.", Lucy "You weren't even there.", Mark "I was there for the end. The end is the part that matters.", Margaret "Sit, Mark. Tell it."); `OutroCutsceneKeepGridHidden`.
- **No tag** on any text in the assets.

## Kill barks: not built
The bark system can do this without new runtime code: bark graphs can be scoped to a level (a `LevelCondition` node compares the level name; `MissionCondition` also exists) on the EnemyDeath trigger, and speaker/instigator conditions exist. But a bark graph is a Unity Graph Toolkit asset (`.barkkill`) authored in the bark graph window; its own seeder notes Graph Toolkit 0.4 has no public API to create nodes from code, so an agent cannot author one reliably. What it takes: THJ (or a session in the editor) builds one graph by hand: EnemyDeath trigger, LevelCondition "Memory 3 · John", a speaker choice (Lucy or Linda, ideally the instigator), then the six lines M3-6 to M3-11 as text nodes in order. The draft's open question about "killed an enemy the other sister damaged" would need checking against the available conditions.

## Answers from the code
- **John's move range:** not settled. His Walk preset (`John_Ability_Walk`) sets its range from `Stat_SPD` (base factor 3 times Stat_SPD plus a constant 1, bounded by `StatUB_SPD`); the stat's actual value for John is not in his prefab or the attribute assets I could read, so I could not compute it without a Play session. The plan assumes at most 4: please check by selecting John and hovering Walk in the first play check.
- **Can a Claw reach John on turn 1?** From the grid: John 4,5; Claws 3,0, 5,0 (6 tiles away), 1,1 and 7,1 (7 away). With a Claw move of 4 (plan, `design/level-chunks`) and a melee hit, a Claw must end adjacent, which takes 5 steps from 3,0 or 5,0 (6 away minus 1), 6 from the others: none reaches John on turn 1. They do reach the sisters (1,1 to Linda at 2,5 is 5 away, 4 steps to adjacent). For John's strike on his own turn: his reach is walk range + 1; with walk 4 the nearest Claw (6) is out of reach, with walk 5 or more it is in. Also sensible to confirm in play.

## Files (each with .meta)
New: `Features/Onboarding/GuidedAbilityHint.cs`; `Features/Onboarding/Editor/HearthMemoryWiring.John.cs` (Tools > Onboarding > Wire Memory 3 (John)), `HearthMemoryJohnTests.cs` (6 tests), `GuidedAbilityHintTests.cs` (4 tests); `Resources/Sequences/Hearth/Memory3John/` (+ .meta): `_GridHiddenAtStart`, `_Start_DialogNodeSequence`, `_Start_Panels`, `_Start_TutorialSequence`, `_Start_SequentialSequence`, `_End_Punchline_DialogNodeSequence`, `_End_Cutaway_DialogNodeSequence`, `_End_SequentialSequence`.
Modified: `GB_m3-john.prefab`; `HearthMemoryWiring.Linda.cs` (Mark added to the speaker list); `HearthMemoryWiring.Lucy.cs` (objective helpers made `internal` so this segment reuses them).
Prefab hand edits (script, serialized data): `introSequence`, `outroSequence`, `lObjectives` (one Any group, two objectives), and a `GuidedAbilityHint` component on the level root. A grid-tool rebuild loses them: re-run the menu item. The Unity reimport diffs (`animationEvents`) on `GB_m3` ride along; `GB_m1` and `GB_m4` also show reimport diffs that are not mine.

## Tests
`HearthMemoryJohnTests`: grid hidden at once then faded in, then John's lines and the panel (order); the panel text and image; the hint points at `John_Ability_Shield` for turn 1; win stage conditions and both lines visible; end order with no fade-in and "You both did."; no placeholder tag. `GuidedAbilityHintTests`: the pulse curve, the zero-period case, ending past the last turn only, an unrelated ability not ending it. Not covered (needs play): the pulse on the real button, the turn cap, the cutaway.

## Play check for THJ
New game into the Hearth, past segments 1 and 2. Segment 3: grid fades in with John's lines, then the Shield Up panel. Select John: the Shield Up button pulses (try selecting a sister first: no pulse). Use Shield Up: the pulse stops. If you do not, it stops when turn 2 begins. Enemy turn: the Claws land beside the sisters; John gets hit and Wrath stacks; turn 2 the punish. HUD shows two lines. End: exchange, grid fades out, still plus cutaway (click past the still).

## Placeholder lines (wording not signed off, untagged in the assets)
All the lines above, the panel text, the two HUD lines, and "Margaret: Sit, Mark. Tell it." (Margaret uses the Narrator character with a name prefix).

## Findings for segment 4
- **Duo button on turn 2:** the hint works by ability preset on any `UnitAbilityButtonUI`, and the Duo presets are ordinary entries in the unit's ability list (John's has three), so it should fit: wire a second `GuidedAbilityHint` (or the same component with last turn 2) with the Duo preset. Unconfirmed: whether the Duo button shows in the main abilities bar or in a separate group UI; check in the first play session.
- **Firing an ability from a sequence:** no. The `ManipulationAction` types in `LevelSpecificBehaviour` only activate objects, change colors, and spawn units/entities; nothing casts an ability. A new sequence calling the ability orchestrator would be new non-core code (I did not read the ability execution API for AP and targeting side effects). The fallback in the plan stands: `LevelStartRunUpgradeGrant` with `RU_LindaLucyCycloneSpreadUnlock` plus a `GuidedAbilityHint` on the Tempest Bloom button.
- `CameraSequence`, `RevealUnitsSequence` and the queued-stage interruption from segment 2 are reusable for the mother scene.

## Proposed commits
1. `feat(onboarding): a hint that pulses one ability button` : GuidedAbilityHint.cs(+meta), GuidedAbilityHintTests.cs(+meta). (non-core component, own commit)
2. `feat(onboarding): the third Hearth memory level's start, hint, win stage and end` : HearthMemoryWiring.John.cs, HearthMemoryJohnTests.cs (+metas), Resources/Sequences/Hearth/Memory3John/** (+metas), GB_m3-john.prefab, and the small Linda/Lucy wiring edits (Mark speaker, internal helpers).

## Fix round
- GuidedAbilityHint: OnEnable subscribes (abilityPerformed, unitSelectionChanged, levelEnded), OnDisable unsubscribes and restores the button size; the hint also ends on level end. The pulse is timed from when the target is set (no jump). The button is re-found when the selection changes, with a 1 s fallback poll instead of 4 per second.
- Wiring uses an explicit if (!hint) for the Unity object. Wire Memory 3 (John) re-run.
- Tests: real other-ability / hinted-ability test (RuntimeAbility with a preset set by reflection), restore-size tests (SetTarget/ApplyPulse/ReleaseTarget are now public), placeholder check uses Contains and also covers panel titles and objective texts.
- EditMode re-run: only Baseline_MatchesCurrentAI failed. Two-commit split unchanged.

## Rework: Claws arrive
EditMode 1202 run, 1201 pass; the one failure is `Baseline_MatchesCurrentAI`. Not play-checked.

**What changed**
- `GB_m3-john` rebuilt from the revised block with the grid tool (`GridToLevelBuilder.Build`, overwrite, GUID kept), then Wire Memory 3 (John) re-run. Round trip with `level_to_grid.py`: four Claws, John, Linda, Lucy, `level hidden 0,0 1,1 5,1 6,0` in its offset frame = 1,1 2,2 6,2 7,1; layout as the block. No hand-set HP on this level.
- New non-core `TurnEndSequenceTrigger` (`Features/Onboarding/`): plays a sequence once when a faction's turn N ends. It subscribes in `OnEnable` and unsubscribes in `OnDisable`, holds no statics, and a restart reloads the level and so the trigger. Option to bring a hidden group in first (see below).
- Wiring: the trigger on the level root (Bergsons, turn 1, group "hidden"), and the arrival sequence `Memory3John_Arrival_SequentialSequence` (input off, HUD off, `RevealUnitsSequence` as the spawn-animation wait, narrator "Then they came out of the dark!", input on, HUD on). The hint, start, panel, end and win stage are unchanged.

**Does a sequence started from `turnEnded` hold the enemy turn? Yes, with one catch handled.**
- `turnEnded` fires inside `EndTurn()` in the turn switch, and `SequencePlayer.Play` sets `isPlaying` at once. The AI controller waits on `SequenceInProgress` (= `SequencePlayer.isPlaying`) before each unit, so no Claw acts until the sequence ends. The turn-switch holds do not help here (they are only read before `EndTurn`).
- The catch: with no Enemy controller, or an Enemy controller with no units, the switch right after the wait would skip the enemy (`CanPlayTurn` false) and hand the turn back to the Bergsons, whatever the sequence is doing. So the trigger brings the hidden group in synchronously inside the `turnEnded` handler, before the switch picks the next faction. `HiddenLevelUnits.Reveal` creates the Enemy controller (`AddFactionControllerMidWay`, inserted in turn order) and registers the Claws; the next turn then includes them, they get a normal turn start, and the AI waits for the sequence. No core change.

**Win cannot fire before the arrival (checked in code, not run).** `LivingUnitsLOCondition` counts the enemy faction's registered units; with no Enemy controller it counts 0 alive and 0 dead, so "dead >= 3" is false, and the stage needs a count of 3. The turn cap is `turn=2`, so the earliest end is turn 3. Nothing else ends the level: the defeat group is Bergsons alive <= 0, and no other "all enemies dead" check exists in the turn switch or the AI. Risk noted: if the previous level's destroyed Enemy controller were still referenced, its dead units would count; Unity treats a destroyed object as null so the condition ignores it. HUD on turn 1 reads "Defeat three Claws: 0 of 3." and "Turns left in the memory: 2." A data-only extra guard was considered and rejected because any added "alive >= 1" condition would block the win when all four die at once.

**Watch on the revealed Claws (item 6).** Watch fires when an enemy ends a *move* in Linda's row or column; a reveal is not a move, so nothing fires at the arrival. The Claws are adjacent (1,1 and 2,2 by Linda, 6,2 and 7,1 by Lucy). The AI picks its target and path by its utility graphs, which I did not run: it may attack from where it stands, but it may also walk to a different target (for example John, 3 to 4 tiles away) or reposition first; a Claw that ends a move in Linda's lane would draw a Watch shot. Nothing in the data stops it; to see it in play.

**Files** (each with .meta): new `Features/Onboarding/TurnEndSequenceTrigger.cs`, `Features/Onboarding/Editor/TurnEndSequenceTriggerTests.cs` (4 tests); new assets `Resources/Sequences/Hearth/Memory3John/Memory3John_Arrival_*` (reveal, dialog, sequential); modified `GB_m3-john.prefab` (rebuilt), `HearthMemoryWiring.John.cs`, `HearthMemoryJohnTests.cs` (adds: four Claws hidden and no active enemy at start; trigger settings and arrival order; win count needs at least one dead). Hand edits to the prefab beyond the tool build: introSequence, outroSequence, lObjectives, GuidedAbilityHint and TurnEndSequenceTrigger components, all by the wiring script (re-run after any rebuild).

**Play check**
1. Segment 3 starts with an empty board (four Claws hidden), John line and panel, Shield Up pulse on John's button.
2. HUD shows two lines on turn 1 (0 of 3, turns left 2).
3. End the Bergsons' turn (with or without Shield Up): the narrator line plays, the four Claws appear beside the sisters (alert), HUD hidden during it, then the enemy phase starts after the line.
4. Enemy turn: do they attack where they stand or walk? Does John's Role take hits, Wrath stack, does Watch fire?
5. Turn 2 punish; win by 3 dead or at turn 3; cutaway; restart the level mid-way and check the Claws are hidden again.

**Commit split** (three units, in order): (1) `GuidedAbilityHint` + tests (as before); (2) `TurnEndSequenceTrigger` + `TurnEndSequenceTriggerTests`; (3) segment 3: wiring, tests, assets and the rebuilt `GB_m3-john.prefab` (plus the Linda/Lucy wiring helper edits).
