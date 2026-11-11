# Report: M2 The Trail levels rework (C1)

Plan: plans/onboarding/2026-11-11-m2-trail-levels-tech.md    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check by THJ still to do)

## What changed

- `Content/Levels/Greybox/GB_m2-trailhead|tracks|blood|pile.prefab`: rebuilt from the design doc's `m2-*` blocks with the grid tool (same code the Tools > Levels > Build Level From Grid window runs, driven through the editor with overwrite on; GUIDs and `.meta` files unchanged), then wired.
- `Features/Onboarding/Editor/SearchWiring.Trail.cs`: reworked (LF, no BOM, as before). New `WireCommon` on every level (Duo lock, removes any start filler, enemy health factors), Trailhead and Blood win = defeat all, Tracks keeps its two stages, Pile stage 1 = tile search plus reveal, rear wave / starts-alert variant / Pass-by panel / Items panel / drain filler code removed.
- `Features/Onboarding/Editor/SearchTrailTests.cs`: updated to the new rules (see tests below).
- `Resources/Sequences/Search/Trail/`: four new assets with their `.meta` (`Trail_Pile_Search_DialogNodeSequence`, `Trail_Pile_Search_SequentialSequence`, `Trail_Pile_RevealWest`, `Trail_Pile_RevealEast`); `Trail_Pile_Start_SequentialSequence` now has no panel step; `Trail_Tracks_Encore_CameraBack` focus point moved with the new camera start.
- `Content/Levels/M2 - The Trail.asset`: untouched (no diff after three wiring runs).

## Acceptance criteria

All four levels:
- [x] Layout, units, tier, deploy slot, alert match the blocks. Evidence: `EveryLevelPlacesTheUnitsAndCellsOfItsGridBlock` (cell counts 9 / 17 / 23 / 36 and every unit tile), `EveryLevelIsEarlyPlacesTheSistersAndHasOneDeploySlotFacingRight` (slots 0,1 x3, pile 4,6; Early). Linda 2,1 / Lucy 1,1; pile Linda 2,6 / Lucy 3,6 (block's top row).
- [x] All enemies start alert: `level alert all` sets `allEnemiesStartAlert`; `EveryEnemyStartsAlertOnEveryLevel`. Revealed units' alert: per `HiddenLevelUnits` docs and tracker code; needs the play check.
- [x] Linda-Lucy Duo locked for both sisters via `LevelAbilityLock`, nothing else locked (the free pick's Duos untouched): `TheSistersDuoIsLockedForBothSistersOnEveryLevelAndNothingElseIsLocked`. Hidden-from-bar is the existing lock behaviour; play check.
- [x] No FTP drain; FTP full at the Trailhead's first turn. The pool starts full by default (`FamilyTimePoints` sets Value = max at mission start, `InitializePoints`), so no +99 filler was added. The wiring removes any start filler left on a level. `NoLevelDrainsOrRefillsTheFamilyTimePoints`.
- [x] No Pass-by panel on routes, no Items panel on the Pile: `NoLevelShowsAPanelAndTheRoutesPlayOnlyTheirOwnLine`, `ThePileOpensOnTheTwoSistersLinesAndEndsOnTheTallyAndTheClue`.
- [x] HP factors Claws 0.6, Archers 0.25, no other override: `EveryEnemyCarriesItsKindsHealthFactorAndNothingElseIsOverridden` (incl. hidden units; Claw ends at 9.6).

Per level:
- [x] Trailhead: Claws 5,1 / 6,1, 9 cells, exit tile and objective gone, win = defeat all (`TheTrailheadIsAOneStageFightWonByDefeatingEveryEnemy`), intro lines unchanged. Mission map opening is unchanged mechanics; play check.
- [x] Tracks: Archers 4,5 / 4,6, Claws 7,1 / 8,1 / 10,1; stages and Encore cue unchanged (`FollowTheTracksCuesEncoreWhenBothLedgeArchersAreDown`).
- [x] Blood: gully 4,3 / 4,4 / 4,5, side 6,4 / 6,5; "Her blood." intro; win = defeat all.
- [x] Pile: stage 1 "Search the pile." = `TilesOccupiedLOCondition`, Bergsons, Any, tiles 4,5 and 5,5; on complete: Lucy "No white fur… she's not here." then `RevealUnitsSequence` west (Claws 0,4 1,4 2,4) and east (Claws 9,4 9,3, Archer 9,6); stage 2 defeat all; rear wave removed; props re-placed (see decisions). `ThePileSearchesTheTilesBesideItThenRevealsBothAmbushesBeforeTheFightStage`, `TheHiddenGroupsHoldTheWestLaneAndTheEastPerchSwitchedOff`, `ThePileOutroShowsTheTally...` (8 steps, unchanged). Reveal timing (stage 2 starts with units live) and the goal-tile highlight need the play check.
- [x] Mission asset unchanged: no diff against HEAD after the wiring runs; graph tests unchanged and green.

Process:
- [x] Built with the grid tool, wired, wiring re-run: md5 of the four prefabs, the mission and all 58 Trail sequence files identical between the second and third run (a prior run had already settled them).
- [x] `SearchTrailTests` updated.

## Tests and console

- EditMode full suite: 1875 total, 1874 passed, 1 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not touched). Run through the editor's runner (editor open, THJ's uncommitted AI files present).
- Compile: no errors after the final refresh; wiring log "The Trail wired..." with no exception (one failed run earlier, from a wrong pile-corner constant, aborted before saving the pile and was fixed). I cleared the console before the test run, so I did not see its messages; the only warnings seen before were existing ones (UtilityScoreGraphView CS0108, AssetOpener CS0618, serialization depth notices).
- Grid-tool warnings only: "the 'J' drawn there is replaced by a deploy slot" x4 (expected).

## Left on disk, unreferenced (not deleted)

- `Resources/Sequences/Search/Trail/Trail_PassBy_SequentialSequence`, `Trail_PassBy_TutorialSequence`, `Trail_PassBy_Panels` (Pass-by panel; no other reference).
- `Trail_Pile_Start_TutorialSequence`, `Trail_Pile_Start_Panels` (Items panel).
- `Trail_Pile_RearWave` (rear-wave sequence).
- `Features/Enemy/Dark Claw/Prefabs/Unit_DarkClaw_StartsAlert.prefab`: no level or Trail code references it now, but it is still the source variant of `Features/Onboarding/Hearth/PoolClaw/Unit_DarkClaw_Hearth.prefab` (and `HearthPoolClawWiring`/tests use it). Keep it. The Trail wiring no longer creates or repairs it (its `EnsureStartsAlertClaw` is gone; the Hearth wiring owns its path constant).

## Save reset

no

## Decisions I made

- FTP starts full by default, so no +99 filler (plan's alternative not needed).
- `PileCorners` stays (3,3) and (6,4): the pile's 2 x 2 (4,3 to 5,4) is drawn `_` (no cells), so the props' midpoint is taken between these flanking cells (same point as before).
- The search sequence follows the Tracks cue pattern: disable input, Lucy's line, reveal west, reveal east, enable input (no camera move, no HUD hide).
- The Pile's relief line is in as drafted, untagged like the other lines; it is a working line to revisit at the line pass.
- Wiring is the only place that sets win groups for the Trailhead and Blood (explicit "defeat all", not the template's default), so a rebuild plus wire is deterministic.
- Old tests for the starts-alert variant, Pass-by panel and rear wave removed with their features; the spawn-action registry test became "nothing spawns units in play".

## Needs THJ

none

## Docs to update

- Design plan as-built note, `design/gdd/missions-structure.md` M2 rows, `design/level-chunks.md`, superseded marks in `plans/onboarding/2026-10-26-onboarding-levels.md` (designer, per the plan).
- `tech/onboarding-merge.md` / `tech/classic-fallback.md`: no wiring point added; likely nothing.

## Risks and loose ends

- Needs play: the reveal runs inside stage 1's end sequence (the next stage is checked only after it); confirm stage 2 starts with units live and acting on the next enemy turn, revealed units arrive alert, and the goal tiles highlight 4,5 / 5,5.
- Archers' arrows over the `_` gap row and rock (design's "to check" items) are not tested.
- `AIRegressionTest` stays red as before (failure list shows graph baseline drift, unrelated).
- Pre-existing, not mine: prefab reserialization noise in the rebuilt prefabs is expected from the tool.

## Proposed commits

1. `feat(onboarding): The Trail's wiring gives every level the locked sisters' Duo, the health factors and no time-point drain, and the pile a tile search that reveals two ambushes`: `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.Trail.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/SearchTrailTests.cs` (plain)
2. `feat(levels): rebuild The Trail's four levels from their grids and rewire them`: the four `GB_m2-*.prefab` (their `.meta` files are unchanged), `Resources/Sequences/Search/Trail/Trail_Pile_Start_SequentialSequence.asset`, `Trail_Tracks_Encore_CameraBack.asset`, and the four new `Trail_Pile_Search_*` / `Trail_Pile_Reveal*` assets with their `.meta` files (depends on 1; plain, large diff from reserialization)

Do not stage: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, ProjectSettings, the TMP fallback font (THJ's).

## Other branches

none (onboarding content on this branch)

## How to see it

1. Open `GB_m2-trailhead` (Content/Levels/Greybox) in Prefab Mode: 9 cells, two Claws at 5,1 / 6,1, deploy slot at 0,1. Same for tracks, blood, pile.
2. Play the M2 mission: Trailhead (one-turn fight, FTP shows full, Linda-Lucy Duo not on the bar), map opens, pick a route, then the Pile.
3. Pile: walk any Bergson to 4,5 or 5,5 (goal tiles lit); Lucy says the relief line, then the west lane and east perch appear alert; defeat all for the tally outro.
4. Re-run Tools > Onboarding > Wire Search: Trail: nothing should change in `git status`.
