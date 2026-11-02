# Report: C3b segment 4, Mark's memory level (`GB_m4-mark`)

Plan: plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md (C3b)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: built. Compiles; EditMode 1210 run, 1209 pass, the one failure is `Baseline_MatchesCurrentAI` (name read from the run). Not play-checked, nothing committed, save not reset. The prefab was not rebuilt with the grid tool; its hand edits (prism HP 0.625, gallery and hall 0.8333, the wolf and cub scenery with the wolf's collider off and material replaced) are intact (the diff touches none of them).

## Built
- **Start:** disable input, hide HUD, grid hidden at once (duration-0 grid sequence) then faded in; Mark "And Linda shot straight into Lucy's fire, and the whole cave bloomed." / Linda "Did I?" / Mark "In my version, you did."; `MoveUnitSequence` walks Mark from 14,2 to 13,2; Mark "Then I arrived." / Lucy "Late." / Mark "Exactly on time."; input and HUD back.
- **Tempest Bloom (a sequence cannot cast an ability):** `LevelStartRunUpgradeGrant` with `RU_LindaLucyCycloneSpreadUnlock` on the level, plus two `GuidedAbilityHint` pulses on turn 1: Lucy's **Cyclone** button and Linda's **Bow Attack** button (the upgrade's own "required ability" and "target ability").
- **Chained Assault, turn 2:** a third `GuidedAbilityHint` on `Mark_Lucy_Duo_Ability` from turn 2 to turn 2. To make "from turn 2" possible the hint got a first-turn field (`firstTurn`, default 1; `Set` takes it as an optional third argument; `ShowsOnTurn` is the pure rule) and tests.
- **Stage 1** (queued, Any): every Claw in play dead (`LivingUnits` Enemy alive <= 0; the two hidden Claws are not registered, so they are not counted) or the turn cap (turn 3 begins). HUD: "Defeat the Claws in the cave: {alive_0} left." and "Turns left in the memory: {remaining_0}." Its `OnCompleteSequence` is the mother's scene: input off, HUD off, camera to the ledge, `RevealUnitsSequence` (the two Claws by the mother, alert, stay and fight under the normal AI), Mark "Then her mother came." / "She stood over the cub until the last Claw fell.", the mother falls, Mark "She didn't get up again.", narrator "The cub cried out.", Lucy "She saved her. We only carried her home.", camera back to a point between the opening view and the ledge, input and HUD on. The grid is not touched.
- **The mother's fall:** the Wolf has only Move and Stand animations, and it is scenery, not a unit, so `UnitAnimationSequence` does not fit. Stand-in: a lying copy ("Mother (fallen)", the placeholder turned 90 degrees, inactive) is made once next to "Mother (placeholder)", and the level's `LevelSpecificBehaviour` (new on the level root) holds a call `motherFalls` that deactivates the standing one and activates the lying one; a `LSBExecutionSequence` in the scene plays it. Replace with a real fall animation when the art exists.
- **Stage 2 (win):** one objective "Reach the cub." with one `UnitTileOccupied` condition per Bergson (Linda, John, Lucy, Mark), each listing 6,9 / 7,9 / 8,9, the objective set to Any. The listed tiles are highlighted as level goals by the existing goal marker (`CombatLevel.RefreshGoalHighlights`), which is the "marker" for where to go; there is no extra marker on the cub. No turn cap on stage 2 (the table has none).
- **End:** disable input, `FadeOutGridSequence` on the win (after the walk), cutaway over the placeholder still, `OutroCutsceneKeepGridHidden`. Cutaway lines (the draft's Hearth close, as there is no Home state yet): "Margaret: Every one of you saved her. That's the only version I believe." / John "Ten Claws, Lucy." / Lucy "At least."
- **Not done:** the optional FTP refill at stage 1 (needs a filler reachable from a signal; not data-only as far as I could tell); the Home open/close states; M4-4 to M4-7 (Atman's Focus and Chained Assault story barks) and the Bloom's M4-8 line coming after the Bloom instead of before it (here it is the opening line).

## What the player does for the Bloom
Turn 1: select **Lucy**, press **Cyclone** (pulses) and put it on the prism's middle tile (3,4); select **Linda**, press **Bow Attack** (pulses) and shoot so the arrow flies through the Cyclone (a Claw beyond it, such as the one on 3,6, or the Cyclone's tile). The arrow entering the Cyclone splits into copies; the original lands before it.

## Answers from the code
- **Grant and squad:** `RunUpgradeTracker.TryGrant` needs the player faction, an active mission, the upgrade's unit (Lucy) in the squad, her required ability (the Cyclone) and no existing grant. The Hearth's roster has Lucy and Linda (its fixed slots are the John, Lucy and Linda unit prefabs), and Lucy has `Lucy_Cyclone_Ability`; so it should pass. Not run, so unverified at runtime; the grant logs a warning if it is refused.
- **No leak into The River:** upgrades are cleared on `FactionTracker.EnterMission` and `QuitMission`, and the River is a different mission, so the grant ends with the Hearth.
- **Does a Bloom copy fly 2 tiles past the Cyclone?** From `LucyCycloneProjectileScatter`: when a whitelisted projectile enters the Cyclone, a copy is launched from the Cyclone's cell toward each neighbouring cell except the one it came from. With `Projectile.travelEntireRadius` (checked in the projectile's `Initialize`) each copy goes the full radius of the caller's parameters in that direction, so two tiles or more if the arrow's radius is at least 2. I did not check Linda's arrow radius or its `travelEntireRadius` flag: confirm in play.
- **Chained Assault "within 4" measured from whom:** the data does not say 4. Both Duo presets (the trigger and Lucy's part) have an activation radius of 5 as a constant; Mark's part reads `Stat_RANGE`. I did not read the code that measures it, so the origin (Lucy as activator, or Mark) is open; the plan's "within 4" differs from the data's 5.
- **The Duo button and the hint:** the abilities bar builds a button for every ability in the unit's list (`AbilitiesBarHUDUI.Populate`), and `Mark_Lucy_Duo_Ability` is on both Mark's and Lucy's lists, so the hint can find it when either is selected. No core work.

## Files (each with .meta)
New: `Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs` (Tools > Onboarding > Wire Memory 4 (Mark)), `HearthMemoryMarkTests.cs` (8 tests); `Resources/Sequences/Hearth/Memory4Mark/` (+ folder .meta): `_GridHiddenAtStart`, `_Start_Opening_DialogNodeSequence`, `_Start_MarkWalksIn` (MoveUnitSequence), `_Start_Arrival_DialogNodeSequence`, `_Start_SequentialSequence`, `_MotherScene_CameraToLedge`, `_MotherScene_Reveal`, `_MotherScene_Comes_DialogNodeSequence`, `_MotherScene_MotherFalls` (LSB call), `_MotherScene_After_DialogNodeSequence`, `_MotherScene_CameraBack`, `_MotherScene_SequentialSequence`, `_End_Cutaway_DialogNodeSequence`, `_End_SequentialSequence`.
Modified: `GB_m4-mark.prefab`; `Features/Onboarding/GuidedAbilityHint.cs` and `Editor/GuidedAbilityHintTests.cs` (the first-turn field).

**Prefab hand edits by the wiring script** (re-run the menu item after any change; do not rebuild with the grid tool): `introSequence`, `outroSequence`, `lObjectives` (two queued stages), components on the level root: `LevelStartRunUpgradeGrant`, three `GuidedAbilityHint`, `LevelSpecificBehaviour`; a new child "Memory Scenery/Mother (fallen)". `GB_m1-linda.prefab` shows Unity reimport noise only (88 added override lines on unit instances); not mine.

## Tests
`HearthMemoryMarkTests`: start order, the walk's nickname and destination match Mark's unit; the grant and the three hints (presets, turns); stage 1 conditions, the scene's step order and the reveal group; the two cue Claws inactive, the fallen copy inactive and the LSB call id present on both ends; stage 2 (four unit conditions, three tiles each, none shared); end order; the scene touches no grid sequence; no placeholder tag. `GuidedAbilityHintTests` extended (first and last turn). Not covered: everything at runtime.

## Play check for THJ
1. Segment 4 opens with the grid fading in, Mark's three lines, Mark stepping from 14,2 to 13,2, his arrival lines.
2. Turn 1, Bloom: select Lucy (Cyclone pulses), place it at 3,4; select Linda (Bow Attack pulses), shoot through it: the Bloom split should kill the prism Claws (HP 0.625 of the base, 6). Check the grant took effect (no Bloom means it was refused: look for the warning).
3. Mark's Blitz chain on the gallery; turn 2: the Chained Assault button pulses (Mark or Lucy selected), hall Claws.
4. When the seventh Claw dies, or at turn 3: camera goes to the ledge, two Claws appear (alert) beside the mother, lines, the mother lies down, the cub's line, camera returns; input back. The two Claws attack on the enemy turn.
5. Walk any Bergson to 6,9 / 7,9 / 8,9 (tiles highlighted): the level ends, the grid fades out, the cutaway.
6. Restart mid-way: the two cue Claws are hidden again, the mother standing.

## Placeholder lines (wording not signed off, untagged in the assets)
All lines above. Added or changed against the draft: the narrator line "The cub cried out." (no cub line in the draft); the end cutaway uses H5-1 to H5-3 (a Home scene in the draft; H5-4 to H5-7 wait for the Home close); "Margaret:" is a name prefix on the Narrator character.

## Commit split (read-only git, nothing staged)
1. `GuidedAbilityHint` first-turn field + its test changes (own commit; the component is already committed).
2. Segment 4: `HearthMemoryWiring.Mark.cs`, `HearthMemoryMarkTests.cs`, `Resources/Sequences/Hearth/Memory4Mark/**` (+ metas), `GB_m4-mark.prefab`. Leave out the `GB_m1-linda.prefab` reimport noise.
