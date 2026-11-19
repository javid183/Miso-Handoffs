# Home Systems — Build Log

**How to use this log.** This is the record of what was built: where it lives in code, how it was verified, deviations from the spec, known bugs and commit status. `design/demo-spec.md` says what the game should do. Sections dated before 2026-10-15 name files by their old paths (`Playtest-Plan.md`, `Miso-Home-System_Demo-Spec.md`, ...); the map in `README.md` gives the current ones. If a build changes a rule or a number, edit the Demo Spec where that rule lives and note the change here; everything else goes here, one section per milestone.

## M0: Core sim

- Definition assets are built by **Tools/Home/Build Demo Content**; the Editor debug window is **Tools/Home/Sim Debug**.
- `HomeStatePreset` assets start the sim from any day; `Preset_Day1Start` is the Day 1 starting state.
- 42 edit-mode tests as of M4 (60 in the project after M5).

## M1: Food loop

Done. No separate build notes were recorded.

## M2: Sorties

**Build notes.** The eight missions are real Mission assets (`Content/Home/Sorties/HomeSortie_*.asset`, built by **Tools/Home/Build Demo Missions**), each with its own copy of a level prefab so the originals stay untouched. Missions carry no gold or collectable pay of their own: Home pays everything through the mission entry.

**Level mapping.** Only levels with placeholder slots can take a chosen squad, so every mission uses a Generic Levels prefab and the enemy mixes do not match the spec's table (no Dark Worm levels exist, and the Warren's fourth level repeats its first).

| Mission | Levels used (copies) |
| --- | --- |
| Goblin Camp | E3-C1 |
| Old Watchtower | E4-C1 |
| Mossy Hollow | E2-C1 |
| Drowned Shrine | E2-C3, then M2-C1 |
| Deev Burrow | E2-C2, E3-C1, E4-C1 |
| Goblin Queen's Warren | M1-C1, M1-C2, M1-C3, M1-C1 again |
| Goblin Scout Post | E2-C3 |
| Shaman's Circle | E2-C2 |

**Flow.** A sortie is launched from the world map in Home mode (only missions the sim lists as available), and the squad is picked in the existing character select. On return the sim resumes at the Sortie phase with Won, FirstDowned and LevelsCleared. Quitting mid-sortie rolls back to the Dawn plan and refunds the send-off.

**Dev tools.** **Tools/Home/Dev: Mark Opening Mission Completed (Play mode)** lets a fresh save reach Home from the main menu, and `unlockRosterForDemo` marks the Toba and Mark gate missions completed.

**Verified.** Play-tested: launch, defeat and return, the Dusk report with a lost sortie, first-downed Wounded, and the Wounded squad block. Unit-tested only: per-level drops and the rollback. A real win and its drops were later played in M3 (Old Watchtower: 30 Gold, 3 Timber and the Weathered War Journal, shown in the Dusk report).

## M3: Knowledge and gear

**Build notes.** The Study shelf, desk and Connect tasks live in `HomeStudy`; Workshop orders and Home Upgrades in `HomeSimulation.Knowledge`. Weapon levels go through `IHomeEquipment` (the real `EquipmentManager`, plus one new `GrantUpgradeLevel` that grants a level without charging), and Home Upgrade effects through `IHomeFactionStats` into the Bergsons faction stat set. The HUD has graybox Study and Home Upgrades panels (top right); the Workshop button opens the existing Workshop panel in order mode. Readers are still seated in Sim Debug, which also has a desk picker, an order button, upgrade buy buttons and test grants for study items and materials.

**Verified in the Editor.** The Old Watchtower win paid the Journal; John reading it over Morning and Afternoon gave 3 Steel and revealed Deev Burrow at the next Dawn. An Ancestral Sword Lv.2 order placed on Day 5 arrived at the Day 7 Dawn. Garden T2 opened 6 plots. Kitchen T2 and Dining T2 took effect in combat (Lucy 15 to 18 max HP; squad FTP 6 to 8 with 3 heroes, 12 with 4). THJ tested the upgraded sword's damage in an actual fight and it worked.

**Findings.** A new cycle resets weapon levels and the two faction stats to 0. The Workshop review confirmed the real equipment system is linear (Lv1 → Lv2 → Lv3, Gold plus a themed material, no blueprints); `EquipmentSO`'s `equipmentsToUnlock`/`equipmentsToHide` hook is unused.

**Status.** Committed on thj/home-test.

## M4: Family

**Build notes.** Yard lessons do not modify units at level start. Lesson points raise levels on the existing Bergsons Faction stat layer (Toughness = Stat\_HP x1.02 per point, Focus = Stat\_CRC +1%, Footwork = Stat\_EVA +1%, Edge = Stat\_DMG x1.02, Mending = Stat\_HPP x1.02, levels 0 to 6). Home Upgrades (Kitchen T2 = Stat\_HP level 1, Dining T2 = Stat\_FP level 1) moved to a new "Home" stat layer that the stat resolver adds automatically, but only for evaluation contexts that hold a Home source, so enemies never receive it. The old 4-tier faction stat tables were replaced and their panels unwired.

Reaching Bond L2 on the showcase pair (Toba and Mark, changed from Mark and Lucy on 2026-09-29) sets the duo flag `duo:Mark+Toba` and queues the scene at the Dining Table. The Toba–Mark duo ability itself still has to be authored; neither has one in code yet. Bond scenes are graybox text cards with placeholder lines (`BondSceneDefinition.sequence` is the hook for a real Sequence).

**Verified in Play on a restarted live cycle.** Yard sessions at Dusk gave Toughness 5/6 (Stat\_HP faction level 5). The Dining Table card showed the lessons and the per-pair "Bond today" list. Toba and Mark went 8 to 28 (L2) and the "Under the Lantern" card appeared in the HUD with a Continue button. In the next combat John had 35 HP (32 x 1.10) and Linda 22 (20 x 1.10), so the Faction layer flows to every hero; Kitchen T2 alone gave John 38 (32 x 1.2) through the Home layer.

**Fixes.** The first M4 build had 4 Yard Student seats by mistake; corrected on 2026-09-29 (builder, test fixture and the Station\_Yard asset) to the spec's 1 Teacher + 2 Students.

**Status.** Committed on thj/home-test. The Picnic is left for M6.

## M5: Night

**Build notes.** `nightSeatCap` limits night seats to 2 in total. Night 1 shows a fourth, lore-only pattern (The Great Moon, no chart). An Omen's `DishEffect`, `enemiesRemoved` and `dropMultiplier` replace the planned `AEffectBase` list and reuse the send-off path; removed enemies are deactivated at level start, never the last one.

**Verified.** 59 of 60 edit-mode tests pass (the red one is AIRegressionTest); 16 of them are in `HomeSimulationTests.Night.cs`. In Play on a fresh cycle, Lucy charted the Hound on night 2, John studied it and connected it with the Old Map Fragment on Day 3, and Drowned Shrine was on the map table on Day 4 (which also fixed the Stone supply for Kitchen T2 without the Sim Debug grant). A Hearth night showed +5 Bond in the Dawn card. A Day 3 Goblin Camp fight logged "Red Veil: Unit\_ArcherGoblin stays out of Goblin Camp (4 enemies left)" with enemy max HP x1.25 (Archer 20 to 25, Masher 50 to 62.5). Twin Glow and Vigil are covered by edit tests only.

**Status.** The Hungry Moon's Queen effect is data and map display only until M6.

## M6: Dungeon

Built in four steps THJ approved: A threads and card, B branch graph and rooms, C campfire and rations, D retreat, relics, free days and Picnic.

**Step A build notes (threads and dungeon card).** `DungeonThreadDefinition` (listed on `HomeCycleDefinition.threads`, seven assets from **Tools/Home/Build Demo Content**) is cut by a completed mission or a Home flag. Hidden threads (Her plan, A hidden campsite) stay off the card until the Queen's Sigil is owned or The Crown is charted. Nothing is stored per thread except `announcedThreads`, so the Dining Table remarks once at Dusk when a thread is cut. Static `HomeThreads` derives thread state from a save so the combat side reads the same rules. `HomeDungeonApplier` (hooked in `CombatLevel.Initialize` after the Omen hook) deactivates the enemies a cut thread names, matched by a substring of the unit name, on the dungeon's level copies only; the last enemy stays. The dungeon card is the Warren's map-table card (`DescribeForMap`): "The Queen's threads (N cut)" with `[x]` and `[ ]` lines. Level names the effects refer to: Warren Gate, Warren Barracks, Warren Deep Tunnels, Queen's Chamber (the levels themselves are renamed in Step B).

**Step A verified.** Compile clean; 68 of 69 edit-mode tests pass (9 new in `HomeSimulationTests.Dungeon.cs`; the red one is AIRegressionTest). Not yet played in combat: the enemy removal needs the Step B level copies.

**Step B build notes (branch graph and rooms).** The Warren is the mission entry `warren` (available from Day 1, map node 106). Its mission graph is built by `HomeDemoMissionBuilder.Warren.cs` from level copies: Warren Gate, Warren Barracks, Warren Rest Room, Warren Deep Tunnels, Warren Upgrade Room (placeholder), Old Path, Queen's Chamber, plus a Hidden Camp and a Relic Room that only appear once their threads are cut. Route gates live on `HomeMissionEntry.routeGates` and are applied by `HomeDungeonRoutes.Apply`, called from one added line in `SerializableDependencyGraph.CreateResolvedCopy`; the authored graph is never changed. Thread effects borrow other levels' prefabs, but always as copies, so the originals are untouched. The Old Path is an easier copy of E3-C1 that skips the Masher wave; the Relic Room is an optional detour before the Queen; Branch 2 is skipped unless the Crown is charted. Queen's Chamber uses 4 placeholder slots.

**Rest Room heal.** The Rest Room heals 10% of max HP. `StatUB_HP` is additive (value = base + max HP), so the authored modifier with a 0.1 factor was a full heal. `SafeRoomFunction` now has `healFractionOfMax` (0.1 on the Warren Rest Room and Hidden Camp); when it is above 0 the function heals that fraction of each unit's max instead of applying the modifiers as authored. `IsCampfire` is true for those rooms.

**Base-game bugfix.** `LucyFactionRoleHandler.PrepareTargets` threw `IndexOutOfRangeException` on every ally action in safe rooms (no enemy faction). It now returns false when there is none (+4/−1 lines).

**Step B verified.** Play-tested: Warren Gate, Barracks, Rest Room (all four squad members including Lucy, exit completes, map advances), Deep Tunnels loads with the Black Claws when the Burrow thread is uncut, thread-cut logging, and the Dining Table thread lines at Dusk. 6 new edit tests. Not yet played: Upgrade Room, Old Path, Queen's Chamber (placeholders), Branch 2 and Relic Room appearing once their threads are cut, mission end after the Queen.

**Step B known gaps.** The Masher wave is not represented (the Masher sits in Warren Gate M1-C3). The Hungry Moon Queen effect (+1 AP below 50% HP) is data only. On the between-levels map card the dungeon card text overlaps the "Enemies to encounter" header (graybox layout; fixed by THJ on 2026-09-30).

**Step C build notes (campfire and rations).** A dish's `RecipeDefinition.ration` (`DishEffect`) now has `healFraction` and `ftpGain` besides the buff lists. Eating happens at a campfire Rest Room (`HomeCampfirePanel`, a code-built panel on the left, shown when the level starts): the heal and FTP apply on the spot, the buff waits in `sortie.pendingRations` and is applied at the start of the next level (`HomeDungeonApplier`), then cleared. `HomeRations` holds the rules (portions, `TryEat`, heal amount with a floor of 1). Eating removes a portion from the pantry and records it in `sortie.rationsEaten`; an interrupted attempt refunds them, a failed attempt loses them. Wounded squad members join a dungeon attempt at `woundedDungeonHpFactor` (50%) HP on the first level (`sortie.woundedJoin`). Percent text is formatted by hand because `:P0` is locale-dependent ("30 %"). FTP does little in ATB mode (check how it feels).

**Step C verified so far.** 11 new edit tests; 85 of 86 pass (the red one is AIRegressionTest). In Play, the campfire panel appeared in the Warren Rest Room and eating a Gourd Omelette healed Toba 14 to 20 of 24 and took one portion (4 to 3).

**Step C Play check (2026-09-29).** In the Warren Rest Room the campfire panel appeared with Gourd Omelette x4. Toba was at 14/24; stepping to the statue gave 16/24 (10% of max, rounded), and eating an omelette gave 22/24 (+25%) and took a portion (4 to 3). Quitting the run refunded the portion (pantry back to 4). The Wounded join at 50% HP, the next-level buff of a ration with buffs, and FTP from a ration are covered by edit tests only; they get a Play check in the final full run (grant a Spiced Stew in Sim Debug first). Cheat note: N+K in a fight kills the hovered unit's whole faction, including our own squad if a hero is hovered.

**Step D build notes (retreat, scouting, free days, Picnic).** `HomeRetreat` puts a "Retreat home" button (bottom right) on the between-levels mission map, only while a Home dungeon attempt is active; it ends the attempt as a loss through `GameHandler.EndMission(false)`. In-run upgrades and relics vanish on their own because `RunUpgradeTracker` is cleared when the mission ends; per-level drops already paid are kept. `HomeSortieBridge.ReportResult` records the levels reached (`sortie.levelsVisited`), and a dungeon result merges them, without duplicates, into `scoutedLevels`; the dungeon card ends with "Scouted so far: ...". An early win becomes free days, shown as "Days spared: N" on the end-of-cycle report. The Picnic unlocks after `picnicAfterSideMissions` (2) side-mission wins and grants 1 Family Skill Point. "Plan the Picnic" sits beside Clear sortie; a planned Picnic takes the whole day (no sortie, no day seats; Mary still cooks) and gives every roster pair `bondFamilyEvent` (+5) Bond. At Dusk a scene card offers "Open the Family Skill Tree" (the Home overlay hides while the tree is open so the tree is not drawn behind it), "Hold the Picnic" and Close; a Picnic left unheld can be held after the dungeon at the end of the cycle. Sim Debug has a test button "Unlock the Picnic (test)".

**Step D verified.** Compile clean; 93 of 94 edit-mode tests pass (8 new; the red one is AIRegressionTest). One new test caught a real bug (the same level counted twice in one attempt), fixed with `Distinct()`. In Play: the Retreat button appeared after clearing Warren Gate; retreating logged "Scouted in the dungeon: Warren Gate" and "the dungeon attempt failed on the full moon", and the full moon allowed a second attempt. The Picnic was planned, took the day, showed the Bond line and the scene card, and opened the Family Skill Tree (Points to Spend: 1), which closes back to the Dusk report.

**Full 7-day run (done-when).** New Cycle, then "Run to next Dawn" six times reached Day 7, the full moon, with 4 Gourd Omelettes in the pantry and the dungeon as the only way out. Warren Gate (a Dark Claw hunter appeared because that thread was uncut), Warren Barracks, then the Rest Room: the campfire panel listed Gourd Omelette x4; eating one healed everyone 25% and left x3.

**Step D not yet played.** Upgrade Room altar, Relic Room (Heavenly Sword pickup), Branch 2 and Relic Room appearing after threads are cut, Old Path, Queen's Chamber, mission end after the Queen, a ration's buff on the next level (Spiced Stew), the Wounded join at 50% HP, FTP from a ration, and the "Days spared" card at a real cycle end (edit tests cover the numbers). Known layout gaps: the Picnic scene card covers part of the Dusk report text, and the Warren card text overlapped "Enemies to encounter" (THJ fixed this in LevelInfoPanel.prefab on 2026-09-30 by shrinking the Enemies section and keeping the full text).

**M6 Play checklist (still to test).**

- Upgrade Room: the altar offers 3 run upgrades and one can be taken
- Relic Room: the Heavenly Sword pickup can be taken; a retreat or loss removes it
- Cut the Drowned Shrine thread: the Relic Room appears in the Warren graph; without the cut it does not
- Chart The Crown: Branch 2 appears; without it it does not
- Old Path: reachable when its thread is cut and skips the Masher wave
- Queen's Chamber (placeholder slots) loads with the chosen squad
- Mission end after the Queen returns to Home as a win: dungeonWon, then the "Days spared" line at the end of the cycle
- Ration buff: grant a Spiced Stew in Sim Debug, eat it at the campfire, and check the buff on the next level and that it is gone one level later
- FTP from a ration (and how it feels in ATB mode)
- Wounded join: a Wounded hero joins a dungeon attempt at 50% HP on the first level
- Picnic unlock through two real side-mission wins (1 Family Skill Point granted)
- Picnic held after the dungeon at the end of the cycle

**Step D status.** Committed on thj/home-test with the rest of M6 (files under `Core/Systems/HomeSystem`, plus `CombatLevelUIManager.cs` for the Retreat button).

## M7: Prologue

Built in four steps (A data and sim, B game wiring, C Home presentation, D Play verification). A new game now plays the three tutorial missions with a Home beat after each, then the Great Moon card, then Day 1 Dawn with the starting state the prologue produced.

**Build notes.** `HomePhase.Prologue` is a real sim phase. `PrologueStepDefinition` (listed on `HomeCycleDefinition.prologueSteps`) has a mission, beat lines, an optional Sequence, a crop to plant, stations and features to unlock, outcomes, an exact wallet and an `endsPrologue` flag. Each step runs in two stages, Mission then Beat. The game owns `Mission.Completed`; the sim owns the step. `SyncPrologueMissions` bridges them when Home loads, so a tutorial won in combat moves the sim on in order. `HomeDayRunner` launches the current tutorial (`LaunchPrologueMission`), saves on every prologue change, and unlocks the gate missions when Day 1 starts. Locks apply only while the save is initialized and in Prologue (`HomeState.InPrologue`): `IsStationUnlocked` needs the station id in the unlocked list, `IsFeatureUnlocked` needs the feature id (`feature.diningTable`, `feature.bond`, `feature.mapTable`, `feature.upgrades`). Outside the prologue an empty list means everything is open, so old saves and New Cycle are unaffected. `HomeManager` blocks the Workshop, World Map and Ability Upgrades rooms with a toast until they are open, and shows a one-line first-click introduction per room (`HomeCycleDefinition.roomIntros`, shown once, stored in `introducedRooms`).

Demo content (`HomeDemoContentBuilder`): tutorials are M1 Hidden Sanctuary - First Step, M2 Ryler is Lost and M3 Blood Trail of A Wolf, in that order. Step 1 unlocks the Dining Table and the Map Table. Step 2 unlocks Kitchen and Homestead, asks the player to plant the Hearty Gourd, and grants 1 Gourd Omelette in the pantry, 1 gourd, 2 eggs and the daily recipe Gourd Omelette. Step 3 unlocks the Porch and Bond, and puts the Old Map Fragment on the Study shelf. Step 4 is the Great Moon card with no mission: it sets the wallet to exactly 100 gold, 1 steel, 1 timber, 0 stone, 0 fabric (overriding the base mission pay on purpose) and ends the prologue. `Preset_PrologueStart` seeds gourd seeds 3 and quickberry seeds 2, feed 4, default hens. The result equals `Preset_Day1Start` and the spec table. The HUD is a graybox card (`HomeDayHUD.Prologue.cs`): Play tutorial (only on the step-1 dev path), then beat pages with Next, Plant where a crop is required, and Continue only on the beat before the Great Moon, then Begin Day 1; see the map-driven amendment below. A step's `sequence` plays before its card if one is assigned (none are yet). All beat lines are `[PLACEHOLDER]` text.

Spec note, not a spec change: planting the gourd in the prologue counts as 1 day grown (`growDays` minus 1), so it is ripe at Dawn of Day 2 and the Demo Spec stays as written. Dev tools: Sim Debug has a new row (New Game prologue, live or not; Skip prologue; Mark tutorial won; Complete beat) and a prologue status line. The existing New Cycle button still starts straight at Day 1, bypassing the prologue. `HomeDayRunner.playPrologue` (default on) switches the prologue off for demos.

**Map-driven amendment.** Requested after the first cut: the tutorials are started from the Map Table instead of a Play button. A beat no longer has a Continue button; it ends when the player launches the next tutorial from the world map (`HomeSimulation.TryLaunchPrologueMission`, reached through `HomeDayRunner.LaunchPrologueFromMap`), so the beat's ask and then the map are the only way forward. Tutorial 1's beat teaches the Dining Table and then the Map Table (`feature.mapTable` now unlocks with step 1). Tutorial 2's beat asks for the Hearty Gourd first and keeps the map closed with the toast "Plant a Hearty Gourd first" until it is planted. Because the map has to be open during a beat, a step's stations and features now open when its beat starts (`OpenStepRooms`) instead of when it completes; this is a behavior change from the first cut, and the lock and resume tests were updated for it. In the prologue the world map shows only the next tutorial (`PrologueMapMission`) and launches it through the normal mission panel and character select. The beat before the Great Moon has no map target, so it keeps one Continue button, and the Great Moon card still ends with Begin Day 1. Guidance is a header hint line plus a pulsing marker on the Map Table, found by scanning `HomeInteractables` for the PointerDown that calls `HomeManager.ShowWorldMap`. The per-page Skip and its PlayerPrefs flag are removed: a Skip prologue button now sits in the header card at all times, with a two-click confirm (`HomeDayRunner.SkipPrologue`, which also marks the tutorial missions completed in memory so the map stays consistent). The Demo Spec was edited where these rules changed (Map Table opens in Tutorial 1, beats end on map launch, Skip prologue button); no number changed. Files touched: `HomeSimulation.Prologue.cs`, `HomeDayRunner.cs`, `HomeDayHUD.Prologue.cs`, `HomeDayHUD.cs`, `HomeDemoContentBuilder.cs`, `HomeSimulationTests.Prologue.cs`, `WorldMapPanelUI.cs`, `HomeManager.cs`, `HomeInteractables.cs`.

**Verified, map-driven flow.** Compile clean. 115 edit-mode tests, 114 pass; the only red test is `AIRegressionTest.Baseline_MatchesCurrentAI`, left alone as instructed. New tests cover the map target per stage, launch-ends-beat, wrong-mission refusal, rooms opening at beat start, and skip. In Play on the real first-launch path (IntroScreen, then Home with no tutorial done) I played all three tutorials with the K cheat: after M1 the header shows the hint and the Skip prologue button, the beat card's last page has no Continue, the Map Table marker pulses and opens a world map with exactly one node (M2), the room-intro toast shows, and selecting the node, Continue and character select launched M2 from the map. After M2 the beat card reads Next then Plant; clicking the Map Table before planting gives the toast "Plant a Hearty Gourd first"; after planting the header changes to "Open the Map Table to choose the next mission" and the map offers only M3, which launched from the map. After M3 the beat shows one Continue, then the Great Moon card (Next, then Begin Day 1), then Day 1 of 7, Dawn, Gold 100, Pantry 1/4. Console after the run showed no errors.

**Finding.** The kill cheat missed an archer standing in a cell at the far right edge of the Game view, twice in this run (M2 level 3 and M3 level 2); panning the camera so the unit is near the middle fixed it. Camera keys and screen-edge scroll are laggy and overshoot, so pan in short bursts.

**Verified.** Compile clean. 111 edit-mode tests, 110 pass at the original cut (115 and 114 after the amendment below); the only red test is `AIRegressionTest.Baseline_MatchesCurrentAI`, left alone as instructed. Prologue tests cover step order, both stages, the wallet override, plant gating, outcomes, skip, `SyncPrologueMissions`, `TryPlantPrologueCrop` and room introductions. In Play mode on the Unity 6000.3.4f1 editor I played all three tutorials in real combat (enemies removed with the K cheat) through the real `GameHandler.EndMission` to `HomeSortieBridge` to Home path. After M1 and M2 the completion sequence plays, then the beat card; the gourd Continue button stays disabled until the plant button is pressed. After M3 the beat card appears, then the Great Moon card, then Day 1 Dawn with Gold 100, Pantry 1/4, Mary's recipe Gourd Omelette and the Study button showing its introduction toast on first click. Sim Debug (live) shows the starting state: wallet 100 / 1 timber / 1 steel / 0 / 0; inventory gourd seeds 2, quickberry seeds 2, feed 4, Hearty Gourd 1, Egg 2, Old Map Fragment 1; pantry Gourd Omelette; plot 1 Hearty Gourd with 1 day left; pen 2 hens, 4 feed; bonds at default (Toba and Mark showcase pair at 5). Console after the run: 0 errors, 43 warnings (not triaged).

**Findings.** M3's second level spawns a reinforcement after the first end of turn (enemies left went 1, then 2), so the level cannot be cleared by killing what is on screen at the start. The game's own completion sequence shows a "New Mission Unlocked!" box after each tutorial, independent of the Home card. The kill cheat (`CheatHandler`) only works when the mouse is over the exact grid cell of a unit, so it needs several small mouse moves first.

**Not verified.** The Skip prologue header button was not clicked in Play (skip logic is unit-tested; the two-click confirm and its label change are code review only). The Sim Debug starting state was read after the original cut, not re-read after the amendment; after it, only the Day 1 header (Gold 100, Pantry 1/4) was checked in Play, and the unit tests assert the exact starting state. The Workshop and Upgrades locked-room toasts were not re-clicked after the amendment. The Yard room introduction has no Play check (no UI caller until M8). The Great Moon rise is a card, not an animation; M8 replaces the cards with the real Home presentation.

**Status.** Committed by THJ, including the map-driven amendment. New and changed files sit under `Core/Systems/HomeSystem/`, plus `Features/Home - Imported/___Khashayar/HomeManager.cs`. Unity generated `.meta` files for the new scripts and for the assets in `Content/Home/Prologue/` and `Content/Home/Presets/`. Next milestone: M8.

## M8: Presentation

**Decisions (THJ).** Both moons (Great Moon 7 phases, Little Moon). Characters slide to room anchors. The meal is picked in the door Send-off scene. The date is shown by the moons only, no date text. Porch seats changed from 5 to 2 to match the design tab. Steps: A rooms and station windows, B house view and character bubbles, C time (moons, time-lapse, Noon pause, family meal), D Send-off scene, prologue on the new presentation, end-of-demo screen, full run with Sim Debug closed.

### Step A: rooms and station windows

**Build notes.** Nine clickable room hotspots (`HomeRoomHotspot`, trigger colliders at z=1 so the old interactable markers still win where they overlap) open one code-built station window (`HomeStationWindow`, shell saved as prefab `Content/Home/Presentation/HomeStationWindow.prefab`, contents rebuilt from the sim every 0.2 s). The window has a task side (plots and planting, pantry and daily recipe, Ben's order, shelf and desk, lessons, patients, patterns) and a seat side with Morning and Afternoon columns (Night only for night stations); every seat shows the candidate tiles, and a blocked character gives the sim's own reason. Seating goes through `HomeSeatPlanner` into `TryAssign`, so no rule changed: Homestead defaults to tending a planted plot (else the pen), Kitchen to the daily recipe (else a known recipe), Experiment takes 1 to 3 ingredient chips. Care and Vigil share the room; the window has a tab for each. The Workshop marker and the toolbar Study and Workshop buttons open the window (the old Workshop panel opens from its "Open the workshop" button). `HomeUiKit` is the shared uGUI kit. New statics are reset in `PlayModeStaticReset`. Editor menu: `Tools/Home/Build Presentation UI` (rebuilds the prefab and hotspots), `Log Room Bounds`, and Play-mode `Dev: Open Window`.

**Step A verified.** Compile clean. Edit tests: 126, 125 pass (AIRegression red as before); 11 new tests (station seats against the design tab, 10 planner tests). Play from Preload with Sim Debug closed: Kitchen (seat, default task, Experiment ingredients, Stand up, Mark's afternoon seat), Homestead (plant, tend a plot), Study (desk), Yard (teacher and student seats, intro toast), Care and Vigil tabs, Workshop, Stargaze at night, Porch (2 seats). A full Day 1 Dawn to Dusk to night to Dawn resolved the seated work: the Dusk report showed John and Mary batch-cooked 3 Gourd Omelette, Mark's afternoon batch refused for a missing Hearty Gourd, and the Dawn report showed Linda watching the sky.

**Not verified in Play (Step A).** Hotspot clicks in the world for study, care, porch, hearth and roof, and the hover label look; the Hearth window; the Noon and Wounded states; locked rooms during the prologue. Note: the first click after Unity regains focus is sometimes swallowed (an editor focus effect, not seen as a window bug).

**Open items (Step A).** Saving the Home scene logs six "Unsupported type Vector2f" errors (likely older than M8). The old Workshop panel's close button sits behind the HUD Plan panel (older; goes away when the Plan panel is replaced in Step C). The graybox Study panel code in `HomeDayHUD.Knowledge.cs` is now unreachable and goes with the toolbar in Step C. Toba and Mark still have no Home entities (Step B placeholders). Hotspot z-ordering against the markers is an assumption that held in the rooms tried. For THJ to commit: the new `Runtime/Presentation/` and `Editor/` files with their metas, the prefab, the modified Home scene, `Station_Porch.asset`, `HomeManager.cs`, `HomeDayHUD.Knowledge.cs`, `PlayModeStaticReset.cs`.

### Resources overview (THJ's change after Step A)

**Decisions:** a slim top bar plus a "Stores" popover for the overview, and a right-hand side panel in the station windows for what that room uses. **Build notes:** `HomeStores` (Runtime/Presentation) is read-only and turns the wallet and the Home inventory into rows (`StoreRow`: label, count, optional "/cap" suffix, icon). `Overview` lists everything (Gold and materials, ingredients, seeds, the farm's feed and hens, the study shelf, the pantry with each dish, and any unknown inventory key under Other); `ForStation` lists only what a station uses: Homestead = seeds, feed, hens; Kitchen = ingredients and the pantry; Workshop = Gold and materials; Study = the shelf; every other station has no panel. Gold, Timber, Steel, Stone and Fabric always show, dimmed at 0; Family Skill Points show once above 0. Wallet rows take their name and icon from the GResource asset (icons exist, so the bar shows icon and count). `HomeResourceBar` is its own overlay canvas (sorting order 18, created by `HomeDayHUD.Ensure`): icons and counts, `Pantry n/cap`, and a Stores button that opens a three-column popover (click elsewhere to close). It hides in the prologue and while the world map is open. The HUD header line now shows only Wounded (Gold and Pantry moved to the bar). The station window is 1500 wide with a 250 wide Stores column (hidden when empty); the prefab was rebuilt with `Tools/Home/Build Presentation UI`. Nothing in the sim changed. The old Workshop panel still has its own `InventorySidePanelUI`; it was not touched.

**Resources overview verified.** Compile clean. Edit tests: 135, 134 pass (AIRegression red); 9 new (`Stores_*`: materials always listed, Kitchen ingredients and pantry dishes, Homestead seeds and feed, Workshop, Study, stations with no panel, nothing hidden in the overview, signature changes with wallet or inventory). Play from Preload with no Sim Debug: the bar (Gold 100, Timber 1, Steel 1, Stone 0, Fabric 0, Pantry 4/4), the popover with real save data (Hearty Gourd 1, Quickberry 6, Egg 5, two shelf items, Gourd Omelette 4), the Kitchen, Homestead and Workshop side panels, the Yard with no panel, the bar hiding when the map opens. Not verified in Play: live refresh while a day resolves (covered by the signature test only), the bar on the prologue-to-Day 1 switch, seeds rows with seeds in stock, and how the bar sits next to the new time HUD (Step C replaces the header).

### Step B: house view and character bubbles

**Decisions (THJ):** avatars use the heroes' combat Idle and Run side art, characters slide between room anchors, the idle stand on the Porch by day and by night, Toba and Mark are placeholder entities built from their combat art.

**Build notes.** The sim is untouched. HomeHouseLayout (Runtime/Presentation, pure logic) decides where each character stands and what the bubble says: the seat for the current phase's slot at that room's anchor; the squad waits at the Door and is Away (walks to the Door and hides) from Send-off to the afternoon resolve; a Wounded character without a seat lies at the Care bed anchor; everyone else is on the Porch; nobody is placed in the prologue. The bubble is two chips, Morning and Afternoon, at Dawn (none on a full-moon day), only the Afternoon chip at Noon, only the Night chip in the night plan, a single Sortie chip for the squad, and "?" for an empty slot. Chips are a short word on a colour (Care, Farm, Cook, Work, Read, Train, Chat, Stars, Fire, Vigil) until the stations have icons; HomeBubble uses the station icon as soon as one is set. Clicking a chip opens that station's window (the Sortie chip and "?" chips only show a toast); hovering shows a caption. HomeAvatar walks to its target with the Run animation and flips to face the way it walks. Dragging an avatar onto a room seats it through the same rules as the windows: HomeSeatPlanner.PickStation (night station at night, locks honoured through HomeDayRunner.RoomBlockReason) and TrySeatForPhase (every slot that can still be planned, first free seat; at Noon only the Afternoon; at Dusk it refuses with the sim's reason). HomeHouseView owns the avatars, polls HomeHouseLayout.Signature every 0.2 s, and hides the old static John, Linda and Lucy figures from Day 1. Figures sit on the DynamicTop sorting layer (the room art reaches order 1000 on Default), bubbles on Overlay with an unlit material, and a silent receiver on each Animator swallows the footstep events the combat Run clips carry. Tools/Home/Build House View (new) builds one prefab and controller per roster hero under Content/Home/Presentation/Avatars, the Room Anchors object (only missing anchors are created, so anchors nudged in the Scene view are kept; to reset one, delete it and rebuild) and the House View object; anchors show as labelled rings in the Scene view. Tools/Home/Dev: Dump Entities (HomeEntityDump) is a temporary aid and can be deleted. PlayModeStaticReset resets HomeHouseView and HomeBubble.

**Step B verified.** Compile clean. Edit tests: 148, 147 pass (AIRegression red); 13 new (House\_\*: placements at Dawn, Noon and night, the wounded bed, squad at the Door then Away, Dawn bubble with "?", Noon collapse and hidden at Dusk, night bubble and Sortie chip, signature, drag at Dawn, at Noon and Dusk, onto a full room, PickStation with night and locks). Play from Preload with no Sim Debug, Day 3: avatars render at real size in the yard, workshop, porch and kitchen with bubbles; Start the day walked everyone to their afternoon room with the Run animation and the bubbles collapsed to one chip; clicking the Cook chip opened the Kitchen window; Stand up in the window sent Mark to the Porch with a "?" chip; dragging Mark from the Porch onto the Kitchen showed "Mark goes to the Kitchen.", he walked there and his chip became Cook; the night plan showed single "?" chips at the Porch; the old static John, Linda and Lucy were hidden.

**Not verified in Play (Step B):** the squad at the Door and leaving (covered by tests; the visual belongs to the Step D Send-off), the Wounded bed, the hearth, roof and homestead anchors against the art (study, care, care-bed and kitchen were nudged from the Scene view, the rest were only seen in passing), the bubble hover caption, dropping on a locked room.

**Open items (Step B):** characters walk in a straight line, so they cross walls and walk outside the house between the yard and the kitchen (waypoints are a Step C polish); the two-chip bubbles are wide for a crowded room (spacing 2.2); Toba and Mark still use combat art, not house art; at Dusk everyone stays where they were until Step C's Dining Table meal; the old graybox night and Dusk panels still cover the world (Step C); walking is silent; Shader.Find("Sprites/Default") for the unlit chips needs to stay in Always Included Shaders. Editor note: I switched the Game view to Play Focused to read the Console while testing and switched it back to Play Maximized. For THJ to commit: HomeHouseLayout, HomeAvatar, HomeBubble, HomeHouseView (Runtime/Presentation), HomeHouseBuilder, HomeEntityDump, HomeSimulationTests.House (Editor), the HomeSeatPlanner and PlayModeStaticReset changes, Content/Home/Presentation/Avatars, and the modified Home scene (House View and Room Anchors objects).

### Step C: time

**Build notes.** Decisions (THJ): generated placeholder moon art, bubbles from a store diff around each slot, the Dining Table in the Hearth room where the family gathers at Dusk, a time-lapse of about 6 s per half-day that can be skipped. The Great Moon (`HomeSkyView`, a camera-child world sprite) is the only time control and one click runs the next step (`HomeTimeFlow.Activate`): Begin the day (Dawn to Noon), Continue to the afternoon (Noon to Dusk), Go into the night (Dusk to Night), Go to sleep (Night to the next Dawn), or Depart on a sortie day. The sim still resolves a slot at once on `Advance`; the lapse is presentation only: `HomeHouseLayout.PhaseOverride` keeps the house showing the slot being worked, the Little Moon and the night veil animate over 6 s (day halves), 5 s (night) or 2.5 s (Dusk), capped at 8 s, and result pops (`HomeGainPop`: the store diff around the slot, shown over the characters seated at the matching station, and Bond over both characters) are spread through it. Skip (button or Space) finishes at once. `HomeTimeFlow.Busy` locks the room hotspots, bubble chips, avatar drag and the HUD cards. `HomeTimeRules` (pure) writes the moon's hover text for each step: the plan, and warnings such as "Nobody is planned for the morning"; a full-moon day is disabled with a Map Table hint, and Go into the night and End the day are disabled while a Bond scene or Picnic scene is waiting. `HomeTimeHud` (top-left) shows the seven Great Moon phases (today larger, past ones dim), the Little Moon on a four-stop ring (Dawn left, Noon top, Dusk right, Night below), Skip while a lapse plays and Cancel sortie on a sortie-day Dawn; there is no date text. At Dusk every character who is not wounded walks to a new `dining` anchor (-3, -4.2) and a Dining Table hotspot (-3, -3.4, 4.5 by 2.6) opens the Dining card: the Dusk report with Go into the night or End the day, and at other times the Picnic plan and undo. `HomeDayHUD` lost the plan panel, Depart, the Dusk graybox, the Night panel and the Study and Workshop buttons; the Last night card at Dawn and the Upgrades button stay. The send-off meal cannot be picked until Step D. The Home scene's camera edge-scroll hot zones are 25% (top, bottom) and 30% (sides), which covers the moon, so `HomeSkyView` polls the mouse and pauses the scroller while the moon is hovered (pointer events flickered while the camera moved). New statics are reset in `PlayModeStaticReset`. Builders `Build House View` and `Build Presentation UI` were re-run for the dining anchor and hotspot.

**Step C verified.** Compile clean. Edit tests: 165, 164 pass (AIRegression red); 17 new (`Time_*`: the moon's text at dawn, noon, dusk, night, sortie day, full moon and prologue, the stops, darkness, ring angle, lapse phases, the lapse keeping the morning rooms, the Dusk gathering with the wounded kept in bed, store-diff attribution, the snapshot seeing a wallet grant, moon phases waxing, and the moon sprite being clear outside its disc). Play from Preload with no Sim Debug, Day 3 to 4: the time strip and Little Moon ring; moon hover text for Begin the day (morning and afternoon plan), Continue to the afternoon, Go into the night and Go to sleep; the morning lapse with +Bond pops over the Yard characters and the Skip button; Space skips; the pause at Noon; the afternoon lapse; Dusk with the family standing in the Hall and the Dining card with Go into the night; the night veil, stars and the Little Moon at the bottom of its ring; the sleep lapse; the next Dawn with the Last night card (chart, Omen, Bond) and the moon text beside it, not over it.

**Not verified and open items (Step C).** Not verified in Play: a sortie day (Depart, Cancel sortie), a full-moon day, the Dining Table hotspot at Dawn (Picnic plan), the Bond scene and Picnic scene cards at Dusk, store-gain pops at the Kitchen and Homestead (covered by the store-diff tests), seating the night by drag, the Upgrades button. The camera still glides for a couple of seconds after the pointer lands on the moon (the camera's own inertia). THJ reported once that every avatar animation stayed on one frame after playing while movement worked; I did not reproduce it and have not investigated it (suspects: the Animator after a disable and enable when avatars are placed or hidden, `SetRun` only applying while active). Open: the dining anchor and hotspot are defaults for THJ to nudge; moon art is generated placeholder; pops overlap when several characters share a station; the Bond and Picnic scene cards are still graybox; the send-off meal picker returns in Step D. Editor note: I used Play Focused for testing and restored Play Maximized. For THJ to commit: `HomeMoonArt`, `HomeTimeRules`, `HomeGainPop`, `HomeSkyView`, `HomeTimeFlow`, `HomeTimeHud` (new, Runtime/Presentation); `HomeHouseLayout`, `HomeHouseView`, `HomeRoomHotspot`, `HomeBubble`, `HomeAvatar`, `HomeDayHUD` with its Knowledge, Night and Prologue parts, `HomeHouseBuilder`, `HomePresentationBuilder`, `PlayModeStaticReset`; `HomeSimulationTests.Time` (new) and the `HomeSimulationTests` TearDown; and the modified Home scene (dining anchor and hotspot).

**Step C feedback round build notes (THJ, 8 points).** (1) Hovering the top-left moon bar or the time panel shows the day line, for example "Day 3 / 7 - Morning" (`HomeTimeRules.DayLine`); the moon tooltip starts with it too. (2) The current day's moon is bigger, with a pulsing shine and a gold ring; past days dim, future days dimmer. (3) The moon states and the time of day are now two separate panels (a cooler blue "Time of Day" panel with four labelled stops and the Little Moon sliding along it). (4) Hovering either Great Moon suspends the camera edge scroll and hard-stops its glide (`CameraEdgeScroller.Suspended`, `CameraHandler.StopMoveNow`, set through `HomeMoonFocus`). (5) The screen Great Moon shows the day line on hover. (6) Resource gain pops that are off-screen get an edge chip with a small arrow and "Label: Message" (`HomeOffscreenPops`); the chip disappears when the world pop is in the camera. (7) THJ's "Moon 04" and "Moon 05" are now the real Great and Little Moon (`HomeWorldMoons`, added by `HomeTimeFlow.Ensure` only when Moon 04 exists): his sprites, my generated phase shadow on top (the disc is found in the sprite, ignoring the floating rocks, and the UI moons reuse his base sprite with the same mask), a ring that pulses gold when the moon is live, hover scale, and click to Activate (the same as the corner moon). The corner moon fades out while the painted one is in view and fades back when it leaves, so the button always reads as that moon. The Little Moon stays at a fixed spot to the right of the Great Moon (I moved Moon 05 to 4.5, 27.5 for THJ to nudge) and changes tint, brightness and glow with the time of day. (8) Mountain Light: its two Vivid children go warm at dusk and cold and dim at night; the night veil is lighter (0.55) so the moons sit above it.

**Step C feedback round verified.** Compile clean. Edit tests: 174, 173 pass (AIRegression red, the known baseline); 9 new tests (day line and part of day, the phase shadow, ring and arrow shapes, the disc finder ignoring rocks, the Little Moon looks, night strength, time track positions, edge chip points and in-view test, hovering a moon stopping the camera scroll). Play from Preload with no Sim Debug on Day 7: top bar tip, current moon ring and shine, the time panel apart from the moon bar, camera standing still while the pointer is over the painted moon, edge chips with arrows at the bottom-right with per-edge separation, the painted full moon on Day 7 with its gold ring, the corner moon hand-off, the night and dusk look.

**Not verified and open items (Step C feedback round).** Not verified in Play: the corner moon stopping the camera in the house view's hot zone (same code path as the painted one), the Mountain Light look by day against night side by side, two chips on one edge overlapping slightly in one case. Looks to review: in daylight the painted Great Moon is pale (THJ's haze layers sit over it, base alpha 0.69), and the day-6 shadow is a thin crescent that is hard to read; stars are small white squares. Gotcha: a `SpriteRenderer` created active with its sprite assigned before its material can draw as a flat cream square until it is toggled; assign the material first, then the sprite (fixed in `HomeSkyView`, `HomeBubble` and `HomeGainPop`, plus a one-time enable toggle in `HomeSkyView`). New static state resets are in `PlayModeStaticReset`. For THJ to commit: `HomeWorldMoons` and `HomeOffscreenPops` (new, Runtime/Presentation); `HomeMoonArt`, `HomeTimeRules`, `HomeTimeHud`, `HomeSkyView`, `HomeGainPop`, `HomeBubble`, `HomeTimeFlow`, `CameraEdgeScroller`, `CameraHandler`, `PlayModeStaticReset`, `HomeSimulationTests.Time`; and the Home scene (Moon 05 position).

**Status.** Step A built and verified, the resources overview built and verified, Step B (house view, character bubbles, drag onto a room) built and verified. Step C (time: moons, time-lapse, Noon pause, Dusk Dining Table, night and sleep) built and verified apart from the items listed above; THJ's 8-point feedback on it (moon hovers, current-moon outline, separate time panel, camera stop on the moons, off-screen pop chips, his painted Moon 04 and 05 as the real moons, Mountain Light) built and verified apart from its open items. Step D not started. Waiting for THJ's check.

## Known bugs

- The Dusk report keeps the line "A Bond scene waits at the Dining Table" after the scene has been watched.
- The existing `EquipmentManager` reset bug: it reloads old saved equipment.

## Resolved questions (history)

- **`TimeOfDayTracker`:** replaced by the `HomeState` calendar; the old class is marked obsolete, unused and safe to delete.
- **Old Home stat panels:** the gold-for-stats Family Room, Kitchen and Training Ground panels are out of the demo. They are unwired, not deleted; ticking `legacyStatUpgradePanelsEnabled` on `HomeManager` brings them back.
- **Dish HP scale:** unit max HP is 15–32, so every HP bonus became a percentage of max HP.
- **New missions:** Goblin Scout Post uses LevelE2-C3 and Shaman's Circle uses LevelE2-C2 (copies).
- **Weapons:** all five come from the existing equipment assets.

**Idle characters and the Porch (THJ's change after Step C, uncommitted at export time).** Decision (THJ): idle characters no longer all gather on the Porch. The first idle characters (roster order) fill the Porch's free seats (2 seats in total, seated ones count) and earn the +1 idle Bond; everyone else wanders the Hall and quiet rooms (hearth, study, care, kitchen, workshop) with no Bond, by day and at night (at night nobody is idle: the night seat counts, the rest wander). Build notes: `HomeSimulation.UnseatedToday(slot)` and `IdleOnPorch(slot)`; `ResolveSlot` uses `IdleOnPorch`; `PorchResolver` bonds pairs among seated plus idle-on-porch (seated-seated `bondPorchAssigned`, any pair with an idle `bondPorchIdle`); `HomeHouseLayout` gets `WanderEpoch`, `WanderRooms`, `WanderRoom` and falls back to a wander room, with the epoch in `Signature`; `HomeHouseView` bumps the epoch every 11–19 s so wanderers drift (not while dragging); `HomeTimeRules.AddIdle` warns "On the Porch: ..." and "Wandering the house, no Bond: ...". Verified: compile clean, edit tests 177, 176 pass (AIRegression red); new tests `House_TheFirstIdleFillThePorchSeats_TheRestWander_NoTwoInTheSameRoom`, `House_TheWanderersMoveOnWhenTheEpochTurns_ButStayApart`, `Bond_OnlyTheIdleOnThePorchBond_TheWanderersDoNot`, and the night test renamed `House_AtNight_OnlyTheNightSeatCounts_ElseTheyWander`. Not verified in Play: the visual wandering. Files changed: `StationResolvers.cs`, `HomeSimulation.cs`, `HomeHouseView.cs`, `HomeTimeRules.cs`, `HomeHouseLayout.cs`, `Editor/HomeSimulationTests.House.cs`. Open: the first two idle are always the same two in roster order.

**Step D decisions (THJ, not started).** Door Send-off window with mission preview, meal pick and a short family line at the Door (placeholder lines); prologue as a narrator banner with dimmed rooms and a two-click Skip prologue at top left; Great Moon rise as a camera glide to the painted Moon 04 that rises with a glow and phase shadow (\~6 s, skippable); end-of-demo full-screen results (Win: Queen defeated, day, days spared, Bond highlights, final stores; loss on full moon: cycle ended plus Retry dungeon with the same pantry; both with Start a new moon cycle and Back to the main menu); a full run with Sim Debug closed; personal room props as a stretch. Plan: `HomeSpeech` (world speech balloon), `HomeSendOffWindow` (canvas 21), `HomeTimeFlow.Activate` Depart opens the window, `HomeBubbleChip` Sortie chip opens it.

**Step D: built (uncommitted at export time).** Build notes: all new files are in `HomeSystem/Runtime/Presentation/` unless noted. `HomeModal` (static counter that locks the world while the Send-off, the rise or the end screen is open). `HomeSendOffRules` (meal pick, mission preview, Omen, family line; lines are `[PLACEHOLDER]`; `HomeCycleDefinition.sendOffLines`). `HomeSpeech` (world speech balloon). `HomeSendOffWindow` (canvas 21, panel on the right, Esc/Cancel closes, Depart closes then `HomeDayRunner.Advance`; the camera frames the squad member speaking at the Door). `HomeTimeFlow` Depart and the Sortie chip open the window. Prologue is a narrator banner (`UI/HomeDayHUD.Prologue.cs`) with `HomeRoomDim` veils over closed rooms. `HomeGreatMoonRise`: after "Begin Day 1" the camera glides to the painted moon (boundary widened during the shot via the new `CameraHandler.Boundary` getter, then restored), the moon rises with halo and phase shadow (`HomeWorldMoons.BeginRise/SetRise/EndRise`), a hold, then the camera returns; \~6 s, a click skips; a 0.5 s arm delay stops the Begin click from skipping it; HUD hidden meanwhile. `HomeEndRules` + `HomeEndScreen` (canvas 30): Win and Loss (at Dusk, no sim change) with Retry, Start a new moon cycle (`HomeDayRunner.StartNewCycle`, Day 1, no prologue) and Back to the main menu. `PlayModeStaticReset` hooks added for all new statics. Only change outside the Home folder: `Core/Camera/Runtime/CameraHandler.cs` (the `Boundary` getter). 15 new edit tests in `Editor/HomeSimulationTests.SendOff.cs`.

**Step D verified.** Compile clean; 192 edit tests, 191 pass (AIRegression red as expected). Played from PreloadScreen: Send-off window (layout, balloon, camera framing, Cancel, Depart), prologue banner with dimmed rooms, Great Moon rise (glide, rise, return).

**Step D not verified.** The Win and Loss end screens and their three buttons were never seen (reaching them needs the full PreloadScreen run: intro, three tutorial combats, a week of days; playing the Home scene directly throws a NullReferenceException in `WorldMapPanelUI.Start`, existing code). The final "no debug UI" run is therefore still to do.

**Step D findings.** Veil rectangles are hard-edged; the banner reads "Tutorial 2 of 3" while there are 4 steps (older label); the world moon sprite can overlap room hotspots, so a click on it may hit the room below.

**Step D status.** Built and tested, not committed. Files to commit: all of `Runtime/Presentation/` new files above, `Runtime/UI/HomeDayHUD.cs`, `HomeDayHUD.Prologue.cs`, `HomeDayRunner.cs`, `HomeCycleDefinition.cs`, `HomeTimeFlow.cs`, `HomeBubble.cs`, `HomeRoomHotspot.cs`, `HomeAvatar.cs`, `HomeSkyView.cs`, `HomeTimeHud.cs`, `HomeResourceBar.cs`, `HomeWorldMoons.cs`, `Core/Managers/PlayModeStaticReset.cs`, `Core/Camera/Runtime/CameraHandler.cs`, `Editor/HomeSimulationTests.SendOff.cs` (and their .meta files).

## Step E: full-demo playtest and fixes

**Build notes.** Played the demo from PreloadScreen with Sim Debug closed (fresh save, 3 tutorials, prologue, Home days, Warren sortie) and checked both end screens. Five small changes, no rule changes. (1) `HomeEndRules`: the Loss subtitle no longer says "The cycle ends here" under a Retry button; it now offers a retry or a new moon cycle. (2) `HomeDayHUD.Family.cs` (`RefreshPicnic`): the "A Picnic still waits" card is hidden while `HomeEndScreen.Showing`, because it showed through the end screen's 0.97 background. (3) `HomeRoomHotspot.OnPointerClick`: ignores a click while `HomeMoonFocus.Any`, so clicking the Great Moon no longer also opens the room under it (the Workshop). (4) `HomeSendOffWindow`: the speech bubble over the speaker strips the ` [PLACEHOLDER]  ` tag, as the window's own quote line already did. (5) Tests in `Editor/HomeSimulationTests.EndFixes.cs` (2 tests).

**Verified.** Edit tests: 194, 193 pass, the red one is `AIRegressionTest.Baseline_MatchesCurrentAI` as expected. In Play: Loss screen text, columns and all three buttons; Retry the dungeon (screen hides, Home returns to Day 7 Morning with the dungeon open); Start a new moon cycle (from Loss and from the saved Win screen, Day 1 Morning, first moon lit); Win screen (title, facts, bonds, stores list) after beating the Warren, and its Start a new moon cycle and Back to the main menu buttons (menu loads, save written); the Win screen loads from the saved game; the Picnic card no longer shows through the Win screen.

**Not verified.** In Play: the Great Moon vs Workshop click fix and the Linda bubble fix (compiled and covered by reading the code only; the New Cycle save restarts at the prologue, where the moon is not clickable). The new Loss subtitle on screen. Skip prologue button. M6 checklist.

**Findings.** (a) The Home camera has a huge boundary, so edge-scroll can drift into the sky or forest, and the prologue starts at the Porch; not fixed, a boundary change is a design decision. (b) After a win the Picnic is still pending but the end screen blocks it, so a player can never hold it before starting the next cycle; needs a spec decision. (c) Return Home after a dungeon takes many seconds with no feedback. (d) Warren level 2: the casters keep summoning imps, which makes the level slow with the K cheat. (e) The 1.04 moon hit radius is polled, so any other world-space click handler under it needs the `HomeMoonFocus.Any` check (only room hotspots have it).

**Step E status.** Built and tested, not committed. Files to commit: `HomeEndRules.cs`, `HomeSendOffWindow.cs`, `HomeRoomHotspot.cs`, `Runtime/UI/HomeDayHUD.Family.cs`, `Editor/HomeSimulationTests.EndFixes.cs` (and their .meta files).

## Step F: Step E follow-ups (Oct 1)

**Built.** (1) A Picnic still waiting when the Queen falls now plays first; the Family tab has a "Skip the Picnic" button (`HomeSaveData.picnicDeclined`, `HomeSimulation.TryDeclinePicnicAfterCycle`, `HomeEndRules` Win case waits for it). (2) Moon guard: avatar drag and bubble chips are ignored while a moon is in focus. (3) "Returning home..." label on the Loss panel and mission-end panel close buttons when Return Home is on (`CombatLevelUIManager`, `MissionEndPanelUI`). (4) Camera boundary fit tool `Tools/Home/Camera` (Log / Apply). Applied: L -23.84, R 38.10, B -23.09, T 35.90 (was 91.4 x 62.4, now 61.9 x 59.0); the far Mountain Light is excluded from the fit and the top edge is kept as it was.

**Verified in Play.** Great Moon click vs Workshop (moon wins), Linda's send-off bubble, new Loss subtitle, Skip prologue button (4 s confirm window). Camera edge-scroll with the new boundary: left stops at the forest margin, the top still reaches the Great Moon. Edit-mode tests: 198 run, 197 pass, only AIRegressionTest.Baseline\_MatchesCurrentAI red (expected).

**Not verified in Play.** Picnic-first/Skip flow and the "Returning home..." label are unit-tested only. Stargaze after the new boundary was not re-walked. SaveScene logged "Unsupported type Vector2f/Vector3f" errors while saving the Home scene; the scene diff is only the three boundary overrides, so they look like save-time noise.

**Findings.** Warren L2 imp summoning logged as a gameplay-data item (not changed). Return Home was not reproduced as slow. Other close handlers may still want the same label (e). Step D and E were already committed.

**Step F status.** Built, tested and committed (THJ confirmed on Oct 2). Files in the commit: `HomeSaveData.cs`, `HomeSimulation.Picnic.cs`, `HomeEndRules.cs`, `HomeDayHUD.Family.cs`, `HomeAvatar.cs`, `HomeBubble.cs`, `CombatLevelUIManager.cs`, `MissionEndPanelUI.cs`, `Editor/HomeSimulationTests.EndFixes.cs`, `Editor/HomeCameraFit.cs`, and `Home - Scene.unity` (and their .meta files).

## Step G: Placeholder tag stripped, Play checks attempted (Oct 2)

**Built.** `HomeText.Display(string)` (new `Runtime/Presentation/HomeText.cs`) removes the "\[PLACEHOLDER\] " tag at display time; the tag stays in the data so unwritten lines are still easy to search for. Used by: prologue beat lines (`HomeDayHUD.Prologue.cs`), Bond scene text card (`HomeDayHUD.Family.cs`), room intros (`HomeSimulation.TryIntroduceRoom`), star chart text in the Chart report line (`NightResolvers.cs`), the Great Moon toast (`HomeGreatMoonRise.cs`), and the Send-off window (`HomeSendOffWindow.cs`, replaces the two inline Replace calls). Two new tests in `Editor/HomeSimulationTests.Text.cs`. THJ decided this (strip the tag) instead of leaving it visible or writing the final lines now.

**Verified.** Edit-mode tests: 200 run, 199 pass; the single red one is the expected `AIRegressionTest.Baseline_MatchesCurrentAI` (I read the 199/1 counters, I did not open the failed entry). The tag was visible on screen in the Tutorial 1 beat box before the change; the on-screen result after the change was not re-checked in Play.

**Not verified in Play.** Picnic-first/Skip flow, the "Returning home..." label, Stargaze with the new camera boundary, and the stripped text on screen. The attempt: Sim Debug live (Skip prologue, Unlock the Picnic (test), Run to next Dawn x6, Warren with 4/4, Advance), then Gate, Barracks, Upgrade Room and Deep Tunnels were cleared with the K cheat (exit-the-refuge rooms end by moving a unit onto the exit tile), but in the Queen's Chamber K and End Turn stopped responding (console: no errors), so Play was stopped. Cause not found.

**Findings.** (1) Cheat tip from THJ: while hovering an enemy, K kills only that unit; N+K kills all units of the hovered faction. (2) The Claude desktop window can take keyboard focus mid-batch (key presses are then refused); click the Unity toolbar before key presses. (3) Close-button labels: only the two combat exits (Loss panel, mission-end panel) are Return Home exits and carry "Returning home..."; the Home buttons (Family Continue/Close, Dining report Go into the night/Close, prologue Continue/Begin Day 1) do not load a scene and stay; the Warren map has a "Retreat home" button that was left as is (THJ's call). (4) `[PLACEHOLDER]` inventory in data: 24 lines in `HomeDemoContentBuilder.cs` (rebuild source), Prologue beats (7), room intros (5), Bond scenes Toba-Mark L2/L3 (8), star charts (4), send-off lines (4), Great Moon line (1). (5) Mission map: picking a node that is not Available (e.g. a sibling of a route already taken) shows its info panel with no Continue button.

**Step G status.** Built, tested and committed (THJ confirmed on Oct 2). Files to commit (plus .meta): `Runtime/Presentation/HomeText.cs`, `HomeSendOffWindow.cs`, `HomeGreatMoonRise.cs`, `Runtime/UI/HomeDayHUD.Prologue.cs`, `Runtime/UI/HomeDayHUD.Family.cs`, `Runtime/Simulation/HomeSimulation.Prologue.cs`, `Runtime/Simulation/NightResolvers.cs`, `Editor/HomeSimulationTests.Text.cs`.

## Step H: Play checks, camera margin 3 (Oct 2)

**Built.** One change: `Margin` in `Editor/HomeCameraFit.cs` went from 6 to 3. THJ ran Log Boundary Fit and Apply Boundary Fit; the Home scene's CameraHandler boundary changed from L=-23.84 R=38.10 B=-23.09 T=35.90 (61.9 x 59.0) to L=-20.84 R=35.10 B=-20.09 T=35.90 (55.9 x 56.0), and the scene was saved. The top edge is kept on purpose (headroom above the moons). No rule changed, so the Demo Spec was not touched.

**Verified in Play.** (1) Picnic-first flow: with a Picnic waiting when the Queen fell on Day 7, the panel "A Picnic still waits" with Hold the Picnic / Skip the Picnic showed before anything else; Skip the Picnic led to the end-of-demo screen with "Start a new moon cycle" and "Back to the main menu", and a new cycle started at Day 1. (2) No `[PLACEHOLDER]` tag on any screen seen: the Home beat box ("Next: John's Map..."), Tutorial 1 combat dialogue, the Victory panel, the Dusk and Win screens, and the Stargaze window. (3) Tutorial 1 (John's Map 1/3) was won with K; the Victory panel and John's Map came up. (4) Stargaze opens from its hotspot ("Tonight: The Great Moon, not yet charted"); its X button closed the window on this run.

**Not verified.** The "Returning home..." label on the Loss / mission-end close buttons (the Tutorial 1 Victory panel's button reads "Continue"; the mission-end Stats close button was not reached). The Stargaze chart report line with a watcher on a night. The Hold the Picnic path. How the camera feels at the new edges beyond what was seen. The Queen's Chamber was skipped: the Warren sortie was resolved with Sim Debug "sortie won", so last session's freeze was not retried.

**Findings.** (a) The Picnic overlaps the Dining Table report card ("The Goblin Queen is defeated"), not the Win panel; the Win screen itself was clean. Cause: in `HomeDayHUD.Refresh` the card shows when `(dusk || ended || _diningOpen) && !mapOpen && !resultsUp`, and `resultsUp` (`HomeEndRules.KindOf != None`) stays false while a Picnic is waiting, so the card stays up under it. Proposed one-line fix: also hide the card while the Picnic panel shows. Not applied; the earlier idea of hiding the Picnic when the end screen is near was wrong, because `HomeEndRules` only returns Win after the Picnic is resolved. (b) Stargaze X button: not reproduced. An earlier run saw it not close; the code wires X and the backdrop to the same `Close()`. Treat as a one-off until it happens again. (c) A new cycle leaves the camera wherever it was (seen again: porch, then edge-scroll to empty sky above the house). Not fixed. (d) K on the Goblin Queen threw a NullReferenceException in the K cheat callback (dev cheat only; `FamilyPointCheat` / `ProduceFTP` is the suspect, undetermined); she was killed with Shift+\[ instead. (e) The Unity Console shows "Unsupported type Vector2f" errors from `SceneManager.SaveScene` around each scene save; not checked whether they predate this step.

**Step H status.** Built (camera margin only), not committed. Files to commit: `Editor/HomeCameraFit.cs` and the Home scene (CameraHandler boundary). Remaining M8 work: the Picnic/report-card fix (a), camera reset on a new cycle (c), the 24 placeholder text lines, and the carried cosmetic items.

## Step I: Picnic card, camera reset, Queen K cheat (Oct 2)

**Built.** (1) `HomeEndRules.PicnicShowing(sim)` (new, pure): true while the Picnic scene is due at Dusk/CycleEnded or a Picnic still waits after the cycle. `HomeDayHUD.Refresh` now hides the Dining Table report card while it is true, so the card no longer sits under the Picnic card (Step H finding a). (2) `CameraHandler.JumpTo(Vector2)` (new: stops movement, clamps to the boundary, sets position); `HomeDayRunner` remembers the camera position at `Start` and `StartNewCycle` jumps back to it. The Home scene never calls `CameraHandler.Initialize()`, so its `initialPosition` is zero: that is why the runner stores its own start position. (3) `CheatHandler.FamilyPointCheat` now skips units that are destroyed, have no faction, or are not in a `PlayerController` faction (family points only exist for the player), which is the suspected cause of the NullReferenceException on the Goblin Queen; the cause was not reproduced or confirmed.

**Verified.** Compiled clean. Edit-mode tests: 203 run, 202 pass, 1 fail; the failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (filtered by name in the Test Runner: 1 test, failed), as expected. 3 new tests in `Editor/HomeSimulationTests.PicnicCard.cs`: Picnic showing is false without a Picnic; true while a Picnic waits after the Queen falls and false once skipped; true during the held Picnic scene and false once closed.

**Not verified in Play (batched for the post-merge pass).** The report card actually hiding under the real Picnic card on Day 7; the camera returning to the house view after "Start a new moon cycle" (including that the saved start position is the house view, not a drifted one); K on the Goblin Queen no longer throwing; K still giving family points on a player unit.

**Findings.** The Stargaze X button was not reproduced (unchanged from Step H). The `Vector2f` SaveScene errors were not investigated.

**Step I status.** Built and tested; committed (f8faebb17, 2b82ffc40; see Step J). Files to commit (plus .meta): `Runtime/Presentation/HomeEndRules.cs`, `Runtime/UI/HomeDayHUD.cs`, `Runtime/HomeDayRunner.cs`, `Camera/Runtime/CameraHandler.cs`, `_Dev_/Runtime/CheatHandler.cs`, `Editor/HomeSimulationTests.PicnicCard.cs` (new), plus the Step H files (`Editor/HomeCameraFit.cs`, Home scene).

## Step J: merge origin/main into thj/home-test (Oct 3)

**Built.** Fetched `origin` first (nothing new: `origin/main` stayed `0ba4bc80d`), then merged it into `thj/home-test` (merge-base `694a7a152`; main 104 commits, branch 24). Merge commit `59a4f5cde` (parents `3ffd7df39` "feat: Moons.prefab added" and `0ba4bc80d`). Main brought about 14,150 new files, mostly a new `Assets/MortaStory/` folder (story art, content and about 120 runtime scripts). Six files conflicted, all with small hunks, so the Home scene fallback in MERGE-BRIEF §3 was not needed:

- `Core/Managers/GlobalSettingsSO.cs`: kept main's `tauntTag` and the Home `homeCycle` field. The branch header was renamed from `[Header("Home")]` to `[Header("Home Cycle")]`, because main added its own `[Header("Home")]` (for `homeStateMissionMode`, used by its Idles).
- `Resources/GlobalSettings.asset`: kept `homeCycle` and main's `tauntTag`, `cheatsEnabled` and `showFPGainVFXOnUnits: 0`. **`pointConsumptionMode` stays 0 (FTP)** (THJ's call; main has 1, ATB). The Demo Spec writes effects against FTP and the recipe FTP bonuses only apply in FTP mode.
- `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`: main's new trigger logic ("Lucy FR now triggers after Mark's actions") with the Home M6 safe-room guard (no enemy faction, return false) placed first, before main's `SessionLogs` read.
- `Unit_Linda.prefab`, `Unit_Lucy.prefab`: took main's side for the 4 hunks of empty `animationEvents` entries on the faction-role ability (the branch's extra entries were re-serialization growth). The Stat\_FP overrides from `150b659ff` (additive policy, base factor 0, level-0 factor 0) are intact; compared with main, those overrides are the only difference.
- `Home - Scene.unity` (8 hunks, all in prefab overrides): kept both sides' `WorldMapPanel` overrides; the two enemy-info panels use **main's** Y positions (−290 / −510; branch had −440 / −570) with the branch's 80-px height (THJ's call); the Home camera fit kept (`maxZoom 20`, boundary L −20.84 R 35.10 B −20.09 T 35.90; main had widened top to 25.9 and left to −45.1 in its "idles for M4 to M7" commit).
- Merged cleanly: Unit\_John, Unit\_Mark, Unit\_Toba, `PlayerController.prefab`, `BergsonsFaction.asset` (Faction layer and "Home" stat source intact). The merged scene still has `HomeDayRunner`, the hotspots and anchors, the `Moons` prefab instance under `Home` > `Landscape`, and main's `Idles` object.

**Verified.** Unity reimported and compiled with no compile errors (Editor log). Edit-mode tests from the command line (Unity 6000.3.4f1 batchmode, editor closed): 203 run, 202 pass, 1 fail; the failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, as expected. Main added no edit-mode tests. This also confirms the command-line test command in CLAUDE.md works (about 53 s for the run).

**Not verified in Play (batched).** Main's idles visible inside the Home camera boundary (main had widened it for them); the enemy-info panels at main's positions with the smaller height (no overlap); Lucy's faction role in combat with main's new trigger, and no throw on ally actions in Rest/Upgrade rooms; FP gain VFX now showing on the HUD (FTP mode makes `showFPGainVFXOnUnits` apply, set to 0). The Step I checks are still open: report card hidden under the real Picnic card on Day 7, camera back to the house view after "Start a new moon cycle", K on the Goblin Queen not throwing, K still giving family points on a player unit. Plus the rest of the MERGE-BRIEF §4.3 checklist.

**Findings.** (a) Git stores these files as LF (`* text=auto` plus `core.autocrlf true`); the working copies are CRLF, so endings never show in diffs. (b) Auto mode blocked overwriting the conflicted files during resolution; the resolved files were made in the scratchpad and copied in with THJ in manual mode. (c) The merge brief's earlier scene numbers were out of date after the Moons.prefab commit (re-measured: branch +1899 / −101, main +185 / −10); the brief was updated before the merge.

**Step J status.** Merged and committed (`59a4f5cde`), not pushed. Steps H and I were already committed (`f8faebb17`, `2b82ffc40`) before the merge. Next: the batched play-through, then the 24 placeholder text lines.

## Step K: second merge of origin/main into thj/home-test (Oct 4)

**Built.** Fetched `origin` (`origin/main` at `ead061cb2`, 11 new commits since Step J, all THJ's: skill tree rework and smoke test, Black Despair Divine Relic, Mark HUD icons and tags, unit HUD index fix, Toba unlocked after Rootwell). Merged into `thj/home-test`: merge commit `182201e82` (parents `59a4f5cde`, `ead061cb2`); 102 files changed on main. Four conflicts, all hero prefabs, none a real disagreement:

- `Unit_Toba`, `Unit_John`, `Unit_Linda`, `Unit_Lucy`: main's skill-tree rework rewrote the `skillTree.*` overrides, and the branch's Stat\_FP overrides sat on the neighbouring lines. Each line was checked against the merge-base: every `skillTree.*` line in the conflicts existed before and main removed it; every `statAttributes.attributeEntries[2]` line is the branch's (`150b659ff`). Kept main's side for `skillTree.*` and kept the Stat\_FP overrides. The stat order in `UnitBase.prefab` is unchanged, so `[2]` is still `Stat_FP`. Compared with main, each resolved prefab differs only by the three Stat\_FP overrides (additive policy, `defaultSbValue.baseFactor` 0, level-0 factor 0); Toba also keeps a branch-side `attributeSet [3] factorReadMode` override that merged cleanly. The `skillTree.*` override count matches main's in all four.
- `Unit_John` also had a hunk of empty `animationEvents` entries on the faction-role ability (merge-base 17, branch 27, main 19): took main's side, as for Linda and Lucy in Step J.
- Merged cleanly: the Home scene (main added only `characters[5].requiredMissionToUnlock`, the Toba unlock), `Unit_Mark` (Stat\_FP overrides intact), and everything else.

**Verified.** Unity reimported and compiled with no compile errors. Edit-mode tests from the command line: 212 run, 211 pass, 1 fail; the failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, as expected. The 9 new tests are main's `VortexPullPlannerTests` (all pass). CLAUDE.md's expected test state is updated to 212 / 211.

**Not verified in Play (batched).** Each hero's skill tree opens and reads right with the resolved prefabs (main's new skill-tree data plus the Stat\_FP overrides); `Tools/Skill Trees/Run Smoke Test (Play Mode)` (a menu tool, not an edit-mode test); Dining Table Tier 2 still gives +1 FP through the "Home" stat source (relies on Stat\_FP additive). The Step J and Step I checks are still open.

**Findings.** (a) Unity left two local changes that are not part of the merge and were not committed: the TMP `LiberationSans SDF - Fallback.asset` had its dynamic glyph table cleared (Unity noise), and `ProjectSettings/EditorSettings.asset` has `m_PrefabModeAllowAutoSave` 1 → 0 (the auto-save toggle in the Prefab Mode header). THJ to keep or discard. (b) The first in-memory preview listed only `propertyPath` lines and missed John's animation-event hunk; the resolver stopped on it and it was handled as above.

**Step K status.** Merged and committed (`182201e82`), not pushed. Next: the batched play-through (Steps I, J, K checks), then the 24 placeholder text lines.

## M9 Step 1a: forecast and no dead seats (Oct 5)

**Built.** Pure C# in `Core/Systems/HomeSystem/Runtime/Simulation/`, no scene, prefab or UI change.

- `IHomeWallet.Fork()` and `IHomeEquipment.Fork()`. The in-memory classes copy themselves; the production wallet forks into an in-memory wallet seeded from its `Snapshot()` (the wallet is keyed by `EntityID` strings, so no resource lookup was needed); `EquipmentManagerHomeEquipment.Fork()` returns the new `OverlayHomeEquipment` (reads through to EquipmentManager, writes stay local).
- `HomeSeatRules` (new): one rule source, `Evaluate(sim, seat)` returns Ok, BondOnly, NeedsPartner or Blocked plus a reason. Covers every row of the design's D table (see the test names below). Helpers for the UI: `CookableNow`, `AnyIngredientInStock`, `PenFeedWarning`, `SendOffMealReason`.
- `HomeSimulation.CheckTask` now also asks the rules, so `TryAssign` and `HomeSeatPlanner.WhyNot` refuse dead seats with the same reason. `ValidateAssignments` re-checks the rules, so a carried-over seat that became dead is released at Dawn with a report line (`"X unseated (Slot): reason"`). When a slot resolves, that slot's seats that still lack a partner (lone Teacher or Student, lone Porch seat, lone Fireside seat, a lone Stargaze watcher with nothing new) are released too; later slots keep theirs, since the partner can still be seated at Noon.
- `HomeSeatPlanner.BuildSeat`: a Kitchen seat with no task now picks a recipe the kitchen can cook from stock (the daily recipe first); only when none is cookable is it refused ("Nothing you know how to cook is in stock").
- `HomeForecast` (new) with `HomeSimulation.ForkForForecast()` / `ForecastResolve(slot)`: `HomeForecast.Run(sim)` dry-runs the slots still to plan (Dawn: Morning and Afternoon, Noon: Afternoon, Night plan: Night) on a deep copy of the state, with the real resolve code. Per slot it returns the report lines, per-seat results (lines, "produces" or the reason it does nothing, released or not), store changes (wallet, inventory, pantry, plots, study, lessons, order, wounded) and Bond deltas. The fork has its own wallet and equipment, no faction stat layer and no event subscribers, so it never reaches the live save, report, GlobalEventBus, EquipmentManager or the player faction.

**Interpretation to confirm (THJ).** The D table says a lone Porch, Fireside or Yard seat is "disabled until its partner is seated". Taken literally nobody could seat the first of a pair. So these seats are allowed while the plan is being built (verdict NeedsPartner, shown as "needs a partner") and released when the slot is committed. "Stargaze, one watcher with nothing new" follows the same rule; with two watchers the second is "Bond only". "Nothing new" counts an unrevealed Omen tonight as something new (the table said "no Omen tonight").

**Verified.** Edit-mode tests from the command line (6000.3.4f1, editor closed): **235 run, 234 pass, 1 fail** (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). 23 new tests in `HomeSimulationTests.Forecast.cs`: fork independence (2), one test per D-table row (Homestead x2, Kitchen x3, Workshop, Study x2, Yard x2, Porch, Fireside, Stargaze x2, Care "no one Wounded", Send-off), Dawn release of a stale carried seat, slots ahead per phase, forecast equals the real resolve for Morning, Afternoon and Night of a full day (report lines for all three, stores for Morning and Afternoon), no side effects (live save byte-identical, live report untouched, wallet and equipment untouched, no sim event raised), and the nothing-reason and Bond deltas.

**Existing tests changed (rule change, not regressions).** About 30 existing tests seated people at stations that now have nothing to do. The shared fixture got `PutWorkOnTheDesk` (a never-finishing Study item on the desk in `NewSim` and `NewFamilySim`) and `DefaultLessons` (one Lesson per roster member in `MakeCycle`). Individual tests got stock (gourd and egg for kitchen seats, feed for the pen, a planted plot for plot seats) or new expectations: `Tending_OnePlotTakesOneBonusPerSlot` now expects the second tender to be refused; `Workshop_HelperOnALaterDay...` expects the seat to be closed; `Study_OtherReaders...` expects Mark to be refused on a finished item only John can claim; `Night_Hearth_NeedsExactlyTwo...` and `Night_TheCrown...` expect the release and the refusal; `Stations_ResolveInSpecOrder` uses a 7-person roster so the Porch and Yard seats have partners; the Study tests that swap the desk re-seat the reader, because a finished item clears the desk and now releases the carried seat at Dawn.

**Not verified.** No Play check (no UI changed). The Care rows are partial: "no one Wounded" is covered; "already tended today" and the carer-per-patient seat come with 1b (Care rework). Nothing reads `HomeForecast` yet: the station window, the moon's Begin tooltip and the late-order warning are wired in 1b/1c and later steps. `HomeForecast.Run` constructs a `HomeSimulation` per call (it calls `cycle.RebuildLookup()`); cache or throttle it when the UI starts calling it every refresh.

**Findings.** (a) `ValidateAssignments` previously checked only `CheckSeat`; it now also applies the rules, so a Stargaze seat that names an already-charted pattern is still kept (the resolver falls back to Auto, as before). (b) The Workshop rule closes a Morning helper seat unless an order was placed that day, so at Dawn a helper can only be seated after the order is placed; carried-over Workshop seats are released at Dawn. (c) `Preset_Day1Start` is a builder asset no test uses; the "forecast equals the real resolve" test runs on the throwaway test cycle. A version on the real demo asset is not written yet.

**Demo Spec edits owned by 1a.** None. (Step 1 as a whole owns the Workshop late-order and Wounded/Care edits; those land with 1b and 1c.) Proposed note for the Study and Yard rules once THJ confirms the interpretation above: "A seat that would produce nothing is refused; pair seats (Teacher/Student, Porch, Fireside, lone Stargaze) wait for their partner and are released when the slot starts if none came."

**Files to commit** (not committed; nothing staged):

- Modified: `Runtime/Simulation/HomeSimulation.cs`, `Runtime/Simulation/IHomeWallet.cs`, `Runtime/Simulation/HomeKnowledgeAdapters.cs`, `Runtime/Presentation/HomeSeatPlanner.cs`, `Editor/HomeSimulationTests.cs`, `.House.cs`, `.Night.cs`, `.Presentation.cs` (all under `miso/Assets/_Project/Core/Systems/HomeSystem/`).
- New (with their `.meta`): `Runtime/Simulation/HomeSeatRules.cs`, `HomeForecast.cs`, `HomeSimulation.Forecast.cs`, `Editor/HomeSimulationTests.Forecast.cs`.
- Not mine, leave out: the TMP `LiberationSans SDF - Fallback.asset` change.

**Step 1a status.** Done and green; next is 1b (Care rework), then 1c (late orders). Both need the minimal carer-picker UI, which should wait for the Play pass.

## M9 Step 1b: Care is one visit to the patient (Oct 5)

**Built.**

- `CareResolver` (Care and Vigil): a carer seated in the slot tends **every** Wounded character, with no cap and no `patientsPerCarer` chunking. Each carer-patient pair gets the Care Bond (Toba's doubling and FastCare unchanged). A tended patient is set to recover at the next Dawn (`min(dawnsLeft, 1)`); a FastCare carer by day heals them on the spot. "Not enough carers" is gone.
- Seat model (design answer: carer seat with `targetId` = patient): a Care or Vigil Carer seat optionally names the patient whose badge it was opened from; empty means "tends all" (so old saves stay valid). One Carer seat per slot: `Station_Care.asset` and the builder go from 2 seats to 1 (Vigil was already 1). `patientsPerCarer` stays in `HomeRules` but is unused (tooltip says so).
- `HomeSeatRules.Care`: refused when no one is Wounded, when a named patient isn't Wounded, and "Already on the mend: recovers at Dawn" when every patient already recovers at the next Dawn and the carer isn't a fast one. That last rule is how "already tended today" is detected without a new save field (untended patients drop to 1 Dawn left the morning after the sortie, so a visit then gains nothing).
- Migration: no version field needed. Old Care or Vigil seats without a patient are valid; a second carer in a slot fails the new seat-count check and is released at the next commit with a report line.
- Minimal UI: the Care window's side panel text now describes the rule ("one carer tends every Wounded character", recovery per patient, the cost line). In the house view (`HomeHouseLayout`): the carer stands at the patient (bedside when resting, or at the patient's own station), and a Wounded character with no seat gets a chip: "Needs care" (click opens the Care window, which is the carer picker), "Tended" once a carer is seated, "Rest" when they already recover at Dawn. The layout signature now includes each patient's `dawnsLeft` so the chip redraws.

**Verified.** Edit-mode tests (command line): 243 run, 242 pass, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). New in `HomeSimulationTests.Care.cs`: one carer tends three Wounded with Bond each; only one carer seat per slot; the seat closes when the patient already recovers at Dawn (but not for Toba); Toba heals right after the slot and the afternoon seat closes; a named patient must be Wounded; old-save seats (no patient; a second carer released); the carer's placement; the three chip states and the signature change. `HomeSimulationTests.Presentation` now expects 1 Care seat.

**Not verified in Play (batched, add to M9-Playtest-Plan Part A, Step 1).** A Wounded character's bubble shows "Needs care" and clicking it opens the Care window; seating a carer turns the chip to "Tended" and the carer walks to the bed; at night the Vigil chip does the same; "Rest" shows the morning after a sortie. `Build Demo Content` was not re-run: `Station_Care.asset` was edited by hand (seat count 2 to 1), so re-run it once to confirm the asset and the builder agree.

**Findings.** (a) A Wounded character at Dawn the day after a sortie already has 1 Dawn left, so by day the only visit that shortens recovery is the Vigil on the sortie night (or Toba's FastCare). That is how the existing numbers work; the "Rest" chip makes it visible. (b) Fast recovery mid-day still changes later seat validity in the same day (the patient becomes eligible for Yard and sorties), as before.

**Demo Spec edits owned by 1b.** Applied to the Demo Spec tab on Oct 5 (Wounded, Night Vigil row, several Wounded).

## M9 Step 1c: late Workshop orders are allowed and warned (Oct 5)

**Built.** `HomeSimulation.Knowledge.cs`: `ArrivesAfterFullMoon(order)` (ready day greater than `DayCount`), `OrderReadyDayIfPlacedNow(withHelper)`, `WouldArriveLateIfPlacedNow`, and `LateOrderWarning` ("Arrives after the full moon"). `TryOrderUpgrade` adds a Warning line to the report when the order is late, and says a same-day helper would still make it when that is true. `WorkshopPanelUI.RefreshHomeOrderSection`: the order button reads "Order Lv.N: ready Day D" plus "(Arrives after the full moon)" when late; an order in progress shows its ready day and the same warning. Ordering stays allowed.

**Verified.** 245 run, 244 pass, 1 fail (the AI baseline). New tests (in `HomeSimulationTests.Care.cs`, section 1c): a Day 6 order is allowed, warned and never delivered within the cycle (still on the bench on Day 7, level unchanged); a Day 5 order is in time and delivered at Dawn of Day 7; a same-day helper rescues a Day 6 order (ready Day 7).

**Not verified in Play (batched).** The Workshop panel's button text and the toast or report line on Day 6. The calendar icon for deliveries comes with Step 2.

**Findings.** The late rule counts delivery at Dawn of Day 7 as in time (the Warren is fought that day), so only a ready day of 8 or more is flagged. If you want Day 7 deliveries flagged too, it is a one-character change (`>` to `>=` in `ArrivesAfterFullMoon` and `WouldArriveLateIfPlacedNow`).

**Demo Spec edits owned by 1c.** Applied to the Demo Spec tab on Oct 5 (Workshop rules, Open questions).

**Files to commit for Step 1 as a whole** (nothing committed or staged).

- Modified under `miso/Assets/_Project/`: `Core/Systems/HomeSystem/Runtime/Simulation/{HomeSimulation.cs, HomeSimulation.Knowledge.cs, IHomeWallet.cs, HomeKnowledgeAdapters.cs, StationResolvers.cs}`, `Runtime/Presentation/{HomeSeatPlanner.cs, HomeHouseLayout.cs, HomeStationWindow.Tasks.cs}`, `Runtime/Definitions/HomeCycleDefinition.cs`, `Editor/{HomeDemoContentBuilder.cs, HomeSimulationTests.cs, .House.cs, .Night.cs, .Presentation.cs}`, `Core/UI/Runtime/Home/WorkshopPanelUI.cs`, `Content/Home/Stations/Station_Care.asset`.
- New (with `.meta`): `HomeSeatRules.cs`, `HomeForecast.cs`, `HomeSimulation.Forecast.cs`, `Editor/HomeSimulationTests.Forecast.cs`, `Editor/HomeSimulationTests.Care.cs`.
- Leave out: the TMP `LiberationSans SDF - Fallback.asset` change.

**Step 1 status.** 1a, 1b and 1c done and green (245 run, 244 pass, AI baseline red). Open for you: confirm the lone-seat interpretation (1a), run the batched Play checks for the Care chip and the Workshop button, re-run Build Demo Content once. Next: Step 2 (goal and calendar).

## M9 Playtest: Step 1 (Part A), first run (Oct 5)

**Setup.** Unity 6000.3.4f1, Home scene played directly (not from PreloadScreen), Sim Debug live. `Tools/Home/Build Demo Content` re-run first: clean, only the known "Unsupported type Vector2f" noise; `Station_Care.asset` still has one Carer seat, so asset and builder agree.

**Verified.**

- Item 1, empty Study: seating a reader on an empty desk is refused with "Nothing to read".
- Item 5, carry-over release: two readers seated on a 1-slot item; after Run to next Dawn the item is understood, the desk is empty and no stale seat remains.
- Item 6, care by day (partial): after a sortie (Linda downed with Sim Debug "First downed" + Win) Linda lies in the bed with a "Needs care" chip; clicking it opens the Care/Vigil window with one Carer seat per slot. The morning after, her chips read "Rest" and the window says "recovers at Dawn"; John is refused with "Already on the mend: recovers at Dawn".
- Item 7, Toba by day: Toba seated in the Morning Care slot clears Linda's Wounded right after the slot (Sim Debug: Wounded "-"), the Afternoon seat reads "Nobody is hurt", and the Linda-Toba Bond rose 11 to 27 (Lv 2).
- Item 8, late order: on Day 6 the Workshop button reads "Order Lv.2: ready Day 8 (Arrives after the full moon)", the order is allowed, and afterwards the panel reads "Ordered: ready at Dawn of Day 8 (Arrives after the full moon)".

**Not verified.** Item 2 (only the empty-Study row was tried; full pantry, lone Porch/Fireside, capped Teacher, lone stargazer not tried; no working-Kitchen click, see finding 3); item 3 (Experiment); item 4 (forecast is not displayed yet); the "Tended" chip, the carer standing at the bedside and the "Recovers at Dawn" badge (unreachable, see finding 1); the Vigil seat (refused, finding 1).

**Findings.**

1. **Major: Vigil (and a non-Toba Care visit) can never be seated.** On the night of a sortie, every carer (John, Toba tried) is refused with "No one is Wounded" while the same window lists Linda as Wounded, 2 dawns. Cause: `HomeSeatRules.Care` (line 250) drops patients for whom `IsInSquadToday` is true, and `Data.sortie.squad` stays set through Dusk and Night. `CareResolver` (`StationResolvers.cs` line 123) and the care bubbles in `HomeHouseLayout.cs` (line 119) use the same filter. The next morning the patient is "Already on the mend", so the only visit that ever shortens recovery is Toba by day. The design (and the Build Log 1b finding a) expects the Vigil on the sortie night to work. Suggested fix, for THJ to approve: ignore the squad filter once the squad is home (Dusk, Night), i.e. only apply it in Morning and Afternoon of the sortie day; add a test with a sortie squad member who is Wounded at Night.
2. **Minor: no reason before the click.** Seats for an empty desk and a second reader on a 1-slot item are not greyed out; the refusal shows only after the click, and "Bond only" never appears. Probably expected until the forecast reaches the windows (steps 2 and 3).
3. **Minor, needs a second look: Kitchen hotspot.** Clicking the Kitchen hotspot icon (and the kitchen floor beside it) opened the Workshop window twice; once the Workshop window did not close with its X or Escape. Could be the Kitchen and Workshop hotspot rectangles overlapping, or a stuck window after finding 4.
4. **Environment: NullReferenceException in `InventorySidePanelUI.RefreshItems` (line 45)**, twice, when the Upgrades panel opened from the Workshop. `playerFaction` is null because `GameHandler` is not loaded when the Home scene is played directly (Sim Debug says "GameHandler / MissionTracker aren't loaded"). Probably not reachable from PreloadScreen, but a null guard would make direct Home-scene testing clean. Next runs start from PreloadScreen.
5. Observation, not in scope: by Day 6 the pen showed "2 hens, 0 feed" and the log said "1 egg(s); 1 went hungry (no feed)".

### M9 Playtest: Session 2 start (Oct 5), combat via PreloadScreen

- Setup: played from PreloadScreen (GameHandler loaded). Start Game opens the intro and tutorial level 1 (Level1C1). Cheat key moved to F9 (the key tool cannot send numpad keys). F9 ends the level and the end sequence plays.
- Finding 6 (Minor, cheat timing only, THJ reproduced): F9 pressed before the level intro sequence has fully ended completes the objective before it is initialized. The Victory panel then shows "Objective / Failed", Continue does nothing, and MissionEndPanelUI.AddObjectives (line 153) throws because `objective.DisplayText` is null (it is only set by LevelObjective.Evaluate/UpdateDisplayText). Not reachable in a normal win. Workaround: wait for the intro sequence to end before F9. Optional hardening, not applied: `if (string.IsNullOrEmpty(objective.DisplayText)) objective.UpdateDisplayText();`.
- Fix applied for Finding 6 (THJ approved, Oct 5): MissionEndPanelUI.AddObjectives now calls `objective.Objective.UpdateDisplayText()` when `DisplayText` is empty, before the "." lookup. Compiles clean. Not yet verified in Play (re-test: F9 right after the tutorial panels close). Not committed.
- Verified in Play (Oct 5): with the fix, F9 on Level1C1 shows "Eliminate all enemies: Success" and Continue leads to Level 1C2 (the next tutorial level). Not committed.
- Session 2 progress (Oct 5): played the three tutorial levels from PreloadScreen with F9. Each Victory/Stats panel showed "Eliminate all enemies: Success" and Continue worked. After level 3 the flow reaches the Home scene with GameHandler loaded: Mission1\_End dialogue, then "New Mission Unlocked!".
- Observation (check (b), first arrival, not a new cycle): once the dialogue ends the camera sits on the front yard south of the house (gate and path in view, house cut off at the top), not on the house. Needs a look: is this intended, and does a new cycle behave the same?
- Still to run this session: (a), (f), (d), (e), (j), (k), (m) on the Day 7 route, then combat checks (c), (l), (g), skill trees (n).
- Day 7 route via the real flow (Oct 5, F9 for each level): Sim Debug "Run to next Dawn" gave Day 7/7 FULL MOON; picked all four, chose Goblin Queen's Warren (4/4), Advance (Depart). Warren Gate, Warren Barracks and Warren Rest Room all completed ("Eliminate all enemies: Success" / "Exit the refuge: Success"). NOTE: the live Home state was the old Session 1 state (Goblin Camp done, Linda-Toba 27), not a fresh cycle: playing the tutorial from PreloadScreen does not reset the Home save.
- (l) Lucy in the Rest Room: Lucy's ally action "Hide and Seek" (slot 5) could be selected and targeted in the Warren Rest Room with no exception (status bar clean, no red Console line). The action itself did not fire (AP stayed 2, no target highlight); probably needs John adjacent. Treat as "no IndexOutOfRange", not as "ally action works".
- (k) enemy-info panels: not verified. Hover shows a small HP bar; a click shows nothing; I could not capture the Shift-held stats.
- Environment: the Claude overlay masks the bottom-right of my screen, so the map-node Start buttons are hidden from me; THJ pressed them.
- Day 7 route continued (Oct 5): Warren Deep Tunnels completed (F9); the map then went straight into Queen's Chamber (so Anahita's Ahiyan / Mithra's Gift nodes were not visited on this route).
- (c) K on the Goblin Queen (Queen's Chamber, 156/156): worked, but not on the first presses. The edge of the Game view scrolls the camera, so early hovers missed; K on an imp killed it. With the hover on the Queen (HP bar visible) K removed her within a couple of presses; her telegraphed attack tiles (warning markers) stayed on the board afterwards (stale telegraph, Minor, check whether it clears on the next turn). Level did not end on her death (3 imps left, "Eliminate all enemies"), as designed. F9 then showed the Stats panel with "Eliminate all enemies: Success". No softlock seen at this point.
- Finding 7 (Minor): the left-side "Campfire / Gourd Omelette" panel stayed on the dungeon map after leaving the Warren Rest Room. It was gone in the next level.
- End of the Day 7 route: Dusk report listed the sortie result ("The Goblin Queen is defeated on Day 7") and the scouted levels. Ending the day showed the cycle-end screen: "The Goblin Queen is defeated / The family comes home. The moon cycle is over." with How it went (fell on Day 7 of 7, Days spared 0, Threads cut 1 of 7), Bond highlights and the stores list; buttons "Start a new moon cycle" and "Back to the main menu".
- (b) camera after "Start a new moon cycle": Day 1, Morning, Gold 100 and the Home overlay come up correctly, but the camera is on the front yard, to the left and below the house (only the top rooms are in view), not on the house. Same view as the first Home arrival, which THJ said is fine. If the intended view is the house, this is a miss.
- Still open from Part 0: (a) report card vs the Picnic card (Picnic never unlocked on this run), (d) "Returning home..." labels on Loss/Retreat, (e) Stargaze report line, (f) Hold the Picnic, (g) Queen's Chamber retry, (j), (m), (n) skill trees.
- Skill-tree pass (n), attempt 1 (Oct 5): not started in the UI. The Home HUD "Upgrades" button opens only Home Upgrades (Kitchen T2 / Dining Table T2 / Garden T2, with costs and "paid now, active from the next Dawn"); that panel also stayed open after I pressed Upgrades again. The skill trees live behind the Workshop window.
- Finding 8 (Minor/observation, Home camera): while the cursor is near the top or right of the Game view, or right after a click, the Home camera keeps scrolling by itself and overshoots (it went up into the empty sky above the house more than once, with no boundary stop). With the camera moving, hotspot clicks miss. Related to check (j) (camera boundary). Needs a look at the camera clamp.

### M9 Playtest: Skill trees (n), first pass, panel text only (Oct 5)

- How to open: the Home HUD "Upgrades" button is Home Upgrades only and the Workshop's "Open the workshop" is the equipment upgrade screen. The skill-tree panel (AbilityUpgradePanelUI) is reached with the editor menu Tools > Skill Trees > Open Upgrades Panel (Play Mode, Home), or from the Family Picnic's "Open Tree" button. The node description panel appears after a node is selected (hover shows nothing).
- Verified (text, in Play): John, Linda, Mark and Toba each show 6 nodes in 4 tiers with the design's names and text: John (Father's Resolve, Shield Up, Decisive Resolve "2 AP", Of the Same Blood "every Bergson gains 20% max HP", Sundering Strikes, Battering Charge "+1 dash range per upgrade"); Linda (Harmonic Slam, Longshot "+1 arrow range", Diminishing Blow "Harmonic Slam applies Weak", Move as One, Louder Crescendo, Power-Piercing Arrows); Mark (Command, Heavy Hands, Sapping Order, Flowing Guard "+5% evasion", Stunning Vault, Atman Body); Toba (Protective Shell, Healing Wind, Guardian's Reach "+1", Provoking Presence "taunt radius +1", Nature's Rhythm "+1 AP", Nature's Gambit "+1 swap distance"). Lucy: Blink, Sidewinders, Rapid Blink "cooldown -1", Kindled Spirits "+10% crit", Lingering Embers (Burn), Cyclone Power. Each node costs "Skill Point x1". Points to Spend on a fresh cycle: John 1, Linda 1, Lucy 1, Mark 0, Toba 1.
- Findings:
  - (n1) Major, matches THJ's +3 suspicion: Lucy's Sidewinders node (B) shows "Maxed Out" with no points spent (its pip shows 2), so it cannot be bought; the design says +1/+2. The Upgrade Levels cap is probably being counted as already-bought levels, or the base levels count toward the cap.
  - (n2) Minor: some node texts do not state the numbers, e.g. Shield Up and Atman Body only say "Each upgrade reduces damage taken" (design: 0.6 -> 0.5 -> 0.4, DR 0.1/0.2); Heavy Hands, Healing Wind, Cyclone Power, Louder Crescendo say "increase" without the factor.
  - (n3) The family tab was not found: the prefab lists a sixth entry (isFamilyAbilitiesBtn = 1), but the sidebar shows only the five portraits, so the family tree (9 nodes, 15 FSP) was not checked. A Console error counter of 1 is showing; not tied to this.
- Not verified: buying any node, prerequisite gates in action (A->C, B->F), pip counts after purchase, combat effects, persistence across save and reload, and Mark's SP (0).

### M9 Playtest: Skill trees (n), purchase test

- n4 PASS: John, node A "Father's Resolve", Skill Point x1. Upgrade pressed with 1 point: Points to Spend 1 -> 0, node button became "Maxed Out", pip shows 0 on the bought node, the spine fills up to row 1, and node C "Decisive Resolve" (A's child) lost its padlock. So purchase and the A -> C unlock work in the panel.
- n5 NOTE: "Maxed Out" is the normal state after a one-level purchase (max level 1), which supports the n1 guess that Lucy's Sidewinders showing "Maxed Out" with an unbought pip came from the cap/pips count, not a bug in the button. Still unconfirmed in code.
- n6 TOOLING: the floating Unity Console window ignored its close/minimize buttons; dragging its title bar out of the way worked.
- Still open for (n): B -> F gate, persistence after save/reload, family tab, combat effect.
- n7 PASS: Linda, 1 SP, selected locked node F "Power-Piercing Arrows" and pressed Upgrade: Points to Spend stayed 1, pip stayed 0, so the prerequisite gate blocks a locked purchase. Minor UX: the Upgrade button still looks active on a locked node (no "Locked" state).
- n8 TOOLING: Console error filter toggles did not respond (floating Console window seems stale); the 1 error was not read. textinputhost.exe again stole focus until THJ clicked in Unity.
- n9 OPEN: the family entry in UpgradesPanel.prefab (6th, isFamilyAbilitiesBtn=1) has NO requiredMissionToUnlock, so the mission gate is not why it is missing from the sidebar; the 5th entry (a45e197c...) is the only gated one. Cause not found (suspect an exception in AbilityUpgradePanelUI.Start or the icon sitting off-screen). Needs a Console look by THJ or a debugger.
- n10 NOT RUN: save/reload persistence of the John node purchase, combat effect of Father's Resolve (both need a level; folded into the full-run check).

### M9 Playtest: Session 3 (Queen's Warren, Oct 5) - results so far

- Route: new cycle, Sim Debug "Run to next Dawn" x6 to Day 7 (FULL MOON), Start Game fireplace marker > Queen's Warren > 4 heroes (Toba, Linda, Mark, John) > Sim Debug "Advance (Depart)" loaded the combat scene. F9 after the intro finished: Warren Gate, Barracks and Rest Room all showed "Victory ... Success" with their objective names (no NRE, the earlier fix holds). Map Continue button at the bottom right is now clickable.
- k (enemy info) FAIL / NOT FOUND: at Warren Gate, hover, left-click and right-click on an enemy Goblin archer showed only the HP bar and the tile cursor; no info panel appeared. If a panel is supposed to exist on hover, it is not showing in this build.
- Queen's Chamber intro: two dialogue beats play ("You shall not!" with John's portrait, then "Enough!" with Lucy's/Mary's portrait) while the player turn UI is already visible. N+K pressed during these beats killed my units without the level ending until a further K; the Defeat panel then showed "Mission Failed!" with the objectives row showing only the red "Failed" and NO objective name (empty label), and the only button is "Return Home".
- g (retry) PARTIAL: "Return Home" led to the cycle-end style screen "The full moon rose, and the Queen stands" with How it went (Day 7 of 7: the dungeon attempt failed; Threads cut 0 of 7), Bond highlights, stores list, and buttons "Retry the dungeon", "Start a new moon cycle", "Back to the main menu". Retry result below.
- Bond highlights show only John pairs (John & Linda 22, John & Lucy 10, John & Toba 10), likely it lists the top three only.
- g (retry) PASS (mostly): "Retry the dungeon" returned Home at Day 7/7 DawnPlan FULL MOON (not Day 1), Pantry 4/4 unchanged, and the Sim Debug shows Wounded: Mark (2) after the forced Loss (only one of four squad members Wounded; the cheat killed all four, so expect all four Wounded unless the rule is "first downed"). A "FamilySP 1" wallet entry appeared (earned by the failed run?). Day, wallet (Gold 100) and inventory were preserved.
- Not run yet in this session: (a) report card vs Picnic card, (d) "Returning home..." labels, (e) Stargaze report, (f) Hold the Picnic, (j) idles inside camera bounds, (m) FP gain VFX.

### Picnic and family tab (Day 2 of a new cycle, Oct 5)

- How to reach it: Dining Table hotspot in the Home view opens "The Dining Table" card (Dawn); "Plan the Family Picnic" there turns into "Picnic planned (undo)". Clicking the big moon in the sky starts the day (HomeSkyView). At Dusk "The Family Picnic" card appears: "+5 Bond", buttons "Open the Family Skill Tree" and "Close".
- (a) NOTE: the Dawn Dining Table card has a 400 px empty body (the min-height body text) between its intro line and the Picnic note and button, so it looks mostly empty; the Picnic button/note sit at the bottom. Dusk shows the separate Picnic card (centre) while the Go into the night prompt shows above it. No overlap of the two cards seen.
- n3 CONFIRMED (major): "Open the Family Skill Tree" opens the same Upgrades panel on John's tree with only five portraits; there is no family tab/6th portrait, so the Family Skill Point (wallet shows FamilySP 1 after the Picnic day and after a failed run) cannot be spent. The prefab lists a 6th entry with isFamilyAbilitiesBtn=1 and no mission gate, so something drops it at runtime (check AbilityUpgradePanelUI.Start around lines 299-319 and the Console error).
- Camera drift (Finding 8) happened again after clicks on the right-hand cards: the Home camera slid up to the sky.
- (a) PASS: Picnic planned at Dawn, day run with a click on the sky moon; at Dusk the Family Picnic card showed first, and after Close the Dusk report card ("Dusk: the family gathers", Bond today +5 for all ten pairs, "Go into the night") replaced it with no overlap. Note: report lines show raw debug prefixes ("\[DawnTick\] Station:", "\[MorningResolve\] Scene:", "\[Dusk\] Dusk:") in the player-facing card.
- Night: no Night panel at Night (design: the Great Moon puts the family to sleep; Stargaze is seated from the room window). Clicking the moon at Night while the camera had drifted opened the Homestead window instead (hotspot under the click); Finding 8 camera drift is what causes mis-clicks.
- NOT RUN (Home flow needs reliable camera control): (e) Stargaze report line, (d) "Returning home..." on Loss/Retreat, (f) Hold the Picnic after a failed cycle, (j) idles inside camera bounds, (m) FP gain VFX, (h) full demo run from PreloadScreen.

### Fix: family tab missing (n3), Oct 5 - code edited, NOT yet verified in Play, uncommitted

- Root cause: `Home - Scene.unity` overrides the UpgradesPanel prefab with `characters.Array.data[5].requiredMissionToUnlock = M3 - Blood Trail of A Wolf` (the prefab has none). Entry 5 is the Family button (`isFamilyAbilitiesBtn`), so `AbilityUpgradePanelUI.Start` skipped it until that story mission is completed, which never happens in the Home demo. Entries 3 and 4 (Mark, M4 White Mothers) are gated the same way by design.
- Fix (one condition, `AbilityUpgradePanelUI.cs` Start loop): `if (!character.isFamilyAbilitiesBtn && character.requiredMissionToUnlock != null)`. The Family button is never gated; the Home Picnic awards the Family SP and sends the player to this tab. The scene override itself is untouched (alternative: delete that override from the scene).
- To verify: Picnic > "Open the Family Skill Tree" shows a sixth portrait; selecting it shows the family tree with FamilySP 1 as Points to Spend; buying a family node spends it.
- UPDATE (THJ, Oct 5): the family tab is confirmed fixed. THJ reverted the `AbilityUpgradePanelUI.cs` condition and instead deleted the `characters.Array.data[5].requiredMissionToUnlock` override (M3 - Blood Trail of A Wolf) from `Home - Scene.unity`. The code change described above is NOT in the repo; the scene edit is the fix.

### M9 Playtest: Session 3b, Stargaze (e), Oct 5

- Route: Start Game from PreloadScreen now lands in Home on Day 3 (existing save, not fresh). Sim Debug Advance x2 reached Dusk. Night seats can only be set after "Go into the night" (Night phase); in Dawn, Noon and Dusk both the Sim Debug "Assign" and the Stargaze window refuse ("Seats can't be changed right now"). The window's own text "Night seats are set at dusk" contradicts that (Minor).
- Stargaze hotspot is the floating "Stargaze" label above the house (camera must be panned up); clicking the room under it at Dawn opened the Stargaze window too.
- Seated Linda on "Watch the sky (auto)" at Night, Advance to next Dawn: Day 4, Charted "The Hound", inventory gained "Star Chart: The Hound x1", Study desk lists it. (e) the report line itself NOT confirmed: the Stargaze window stayed open after the day change, would not close with X or Escape (Finding 3 again), and covered the Last Night card. Sim Debug "Today's report" at Dawn shows only the DawnTick lines.
- Also seen: Linda's night seat carried into the next day's Stargaze window (Night seat persists after Dawn); the Great Moon moon-row highlight moved to the correct day.
- Still NOT run: (d), (f), (h), (j), (m). Stuck window blocks further Home clicks; Play restart needed.

### M9 Playtest: Session 3c, (d) and (f), Oct 5

- Route: restart Play, New Cycle in Sim Debug, "Run to next Dawn" x6 to Day 7 (no Picnic planned, Picnic not unlocked this cycle), picked John/Linda/Lucy/Toba in the Sortie section, Warren, Advance (Depart). Combat at Warren Gate; K on each of my four units. First downed "Lucy" showed in the status bar. Defeat panel: "Mission Failed!", objective row blank with red "Failed", button "Return Home" (same blank-label finding as before).
- (d) PARTIAL: after pressing Return Home a black screen shows with a falling/white silhouette for \~1-2 s, then the end screen. No "Returning home..." text was visible in the screenshots taken right after the click; the button label read "Return Home" before the click. Retreat button not tried.
- End screen after the loss: "The full moon rose, and the Queen stands", How it went (Day 7 of 7: dungeon attempt failed, Threads 0 of 7), Bond highlights (only three John pairs again), stores, buttons Retry the dungeon / Start a new moon cycle / Back to the main menu.
- (f) NOT REACHED: no "A Picnic still waits" card or "Hold the Picnic" button appeared. By code (`HomeDayHUD.Family.RefreshPicnic`) that card needs `PicnicPendingAfterCycle` and is hidden while `HomeEndScreen.Showing`, so it can only show after leaving the end screen (Retry) and only if the Picnic was unlocked. Needs a run with "Unlock the Picnic (test)" pressed first, then lose, then Retry. Not done.
- Sim Debug note: "Run whole cycle" is greyed in live mode; unticking "sorties are won" did not change that.

## Session 3d: (f) Picnic card after a win — PASS (with findings)

- Code finding: the "A Picnic still waits" card (`PicnicPendingAfterCycle`) needs Phase == CycleEnded, so it only exists after a WIN. A loss + Retry never shows it (a loss does not end the cycle). The earlier "Retry should show the card" assumption was wrong, not a bug.
- Run: New Cycle, Unlock the Picnic (test), 6 Dawns to Day 7, squad John/Linda/Lucy/Toba on Queen's Warren, F9 on each level, Queen's Chamber F9 -> Stats -> Close -> Home Dusk. Report: "The Goblin Queen is defeated on Day 7 (0 days spared)". Click "End the day" -> card "A Picnic still waits" with "Hold the Picnic" / "Skip the Picnic".
- Hold the Picnic -> "The Family Picnic" panel (+5 Bond per pair, "Open the Family Skill Tree" / "Close"). Open the Family Skill Tree opens the Upgrades panel; Points to Spend shows 0 there (not verified whether the FP was spent or the panel opened on a different tab). Skip button not tested.
- Findings: (1) Warren map: the Upgrade Room (refuge) node cannot be started (clicks do nothing, "Exit the refuge" panel only); the boss node can be selected and a "Continue" button appears in the panel's place, and the path works. (2) A stale "Pact Leader" enemy-info tooltip overlays the objective panel on the map when clicking a node — possibly the missing enemy-info panel (k), but it appears on the map, not in combat. (3) Day 7 Dusk report still shows raw tags "\[Sortie\]", "\[Morning\]" etc.

## M9 Playtest: Step 1 (Part A), second run (Oct 5)

Setup: Play from PreloadScreen (Start Game resumed the saved Day 7 night), then "Start a new moon cycle" from the end screen. Day 1 Morning.

**Verified (again).**

- Item 1: empty Study, seating John gives "Nothing to read" (shown at the bottom of the window after the click). With the Old Map Fragment (1 slot) on the desk, two readers (John, Lucy) could be seated in the same Morning slot; no "Bond only" text appears anywhere (consistent with finding 2 of the first run: needs the forecast in the windows).
- Item 2, Workshop helper with no order: Linda in the Morning Workshop seat is refused with "No order to speed up" (after the click, the seat is not greyed out beforehand).

**Not verified.** Item 2 rows full pantry / capped Teacher / lone Porch-Fireside / lone stargazer; item 3 Experiment; item 4 (no forecast display yet); Vigil retest and "Tended" chip. Cause: the Kitchen could not be opened by clicking (clicks on the stove and counter did nothing) and the Home camera keeps drifting between screenshots, so click targets move. The Sim Debug "Assign (open)" button gave no feedback line in the report, so it is not usable for refusal text.

**Findings.**

1. Minor: Hold the Picnic is not remembered across a Play restart. After stopping Play and resuming from PreloadScreen, the Day 7 night showed "A Picnic still waits" again although the Picnic had been held. Check whether `picnicHeld` is saved at the moment of holding (the save may only happen at the Dawn plan).
2. Minor (repeat of Stargaze finding): the Study window did not close at once with its X or Escape; it closed after a click outside the window.
3. Minor (repeat, Finding 8): the Home camera drifts continuously on its own.

### M9 Playtest: Step 1, second run, continued (Kitchen)

**Verified.**

- Item 3, Experiment: with John as Afternoon Kitchen helper the seat offers "Cook Gourd Omelette" and "Experiment"; Experiment opens an ingredient picker ("Ingredients (1/3): tap to add, tap again past three to start over"). With only Hearty Gourd picked and the day run (Sim Debug Run to next Dawn), Day 2 Dawn shows the pantry at 2/4 (was 1/4) and Mystery Stew in the pantry, and one Hearty Gourd was consumed. Experiment stays available with stock.
- Item 5 again: the Old Map Fragment read by two readers on Day 1 is "understood" at Day 2 Dawn and the desk is empty. **Findings.**

1. Minor: Experiment is not visibly marked as a risk (no label or warning on the button or picker); the plan expects "marked as a risk".
2. Minor: Mary's daily recipe shows "None" at Day 1 although the Gourd Omelette button is highlighted and the Sim Debug says Gourd Omelette; the window text did not update after clicking the recipe (it did show "John: take this seat" as a stale line).
3. Minor: clicking the sky moon opens the Workshop under it (expected until step 3). **Still not verified:** item 2 rows (full pantry, capped Teacher, lone Porch/Fireside, lone stargazer), item 4, Vigil retest and "Tended" chip.

### M9 Playtest: Step 1, second run, Care retest (Oct 5)

Setup: Day 2, Goblin Camp with John/Linda/Lucy; Linda downed (K) then F9 win. Dusk report: "Linda comes home Wounded (2 Dawns)". Night opened with the Vigil window (the user opened it, since the camera had flown off). **Not fixed, reproduced: Major, Vigil can't be seated.** Vigil window lists "Resting: Linda, 2 dawns to recover" and one Carer seat, but seating John gives "No one is Wounded: John: No one is Wounded". Same as finding 1 of the first run (squad filter `IsInSquadToday` still applies at night). So the "Tended" chip, the carer at the bedside and "Recovers at Dawn" remain untestable. Fix suggestion unchanged (apply the squad filter only in Morning and Afternoon of the sortie day), needs THJ's yes. **New finding, Minor-Major: Home camera has no limits or reset.** Dragging and scrolling flew it past the house into the sky/Stargaze ledge; there is no key or button to return. Related to Finding 8 (drift). **Step 1 result:** verified 1, 3, 5, 6 (day, partial), 7 (Toba), 8; blocked 7 (night Vigil, finding above); not testable 4; item 2 only 2 of 5 rows tried.

## M9 Step 1b fix: the Vigil on the sortie night (Oct 5)

**Cause (playtest finding 1, Major).** `Data.sortie.squad` stays set through Dusk and Night, and the Care rules filtered patients with `IsInSquadToday`. At night a Wounded squad member therefore counted as "away on the sortie": `HomeSeatRules.Care` refused every carer with "No one is Wounded", and `CareResolver` and the carer positioning in `HomeHouseLayout` would have skipped them too. The Vigil on the sortie night, the one visit that shortens recovery, could never be seated. The 1b tests missed it: none had a Wounded squad member at night.

**Fix.** New `HomeSimulation.Care.cs`: `IsAwayOnSortie(character, slot)` is true only for day slots (the squad is home by Dusk). Used instead of `IsInSquadToday` where Care picks its patients: `HomeSeatRules.Care`, `CareResolver`, `HomeHouseLayout.PatientAnchor`. The sortie-day rules for day slots are unchanged (`CheckSeat`, the idle lists and the house placement still use `IsInSquadToday`).

**Verified.** Edit-mode tests (command line, editor closed): **246 run, 245 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). New test `Vigil_OnTheSortieNight_CanSitUpWithTheSquadMemberWhoCameHomeWounded`: Goblin Camp sortie with John, Linda and Lucy, Linda first downed; at NightPlan John takes the Vigil seat, the John-Linda Bond rises by `bondCare`, and Linda is no longer Wounded after the next Dawn.

**Not verified in Play (add to the next batch).** The Vigil retest from the second Step 1 run: on the sortie night the Vigil seat accepts John, the chip over Linda changes from "Needs care" to "Tended", the carer walks to the bedside, and Linda recovers at Dawn. This also covers the "Tended" chip and the "Recovers at Dawn" badge, which were unreachable before.

**Files (not committed).** Modified: `Runtime/Simulation/HomeSeatRules.cs`, `Runtime/Simulation/StationResolvers.cs`, `Runtime/Presentation/HomeHouseLayout.cs`, `Editor/HomeSimulationTests.Care.cs`. New (with `.meta`): `Runtime/Simulation/HomeSimulation.Care.cs`.

## M9 Step 2: Goal and calendar (Oct 5)

**Built.**

- Pure logic (new, tested): `Runtime/Simulation/HomeGoal.cs` (Queen's Might pips, hover lines, nights-remain text, "Days left · Open missions" line, mission purpose and label, closing note "Gone after tomorrow", haul entries, war council lines), `HomeCalendar.cs` (`EventsFor(day)` with priority Queen > closing mission > delivery > ripening > Omen > star, 2 icons then "+N", hover text; revealed Omens only; past days empty), `HomeSimulation.Goal.cs` (`NeedsWarCouncil`, `CompleteWarCouncil`), `Presentation/HomeSkyDecay.cs` (decay amount, Great Moon tint, light chill, Little Moon arc).
- `HomeMissionEntry`: new `purpose` field (Auto derives: dungeon = The Queen, thread = Weakens the Queen, hidden = Secret, else Supplies). `DescribeForMap` now leads with the purpose, adds the closing note, "(only here)" on study items, and on the Warren a "Danger: N of M threads stand" line plus the "Scouting run" label while any thread stands.
- `HomeSaveData.warCouncilHeld` (new, defaults false).
- Time HUD (`HomeTimeHud.Goal.cs`, partial; hooks in `HomeTimeHud.cs`): every moon cell is now a moon box plus a 24 px icon row (placeholder letter badges), per-day hover list, Queen's Might panel (known pips, "?" for hidden threads, grey for cut) with a hover list, and a "N nights remain" Dawn card with the moon face (4 s, once per day).
- World map (`WorldMapPanelUI.cs`): the Warren is pinned at `warrenOffset` (default 0,230) scale `warrenScale` 1.4 and no longer takes a grid cell; each node has a label with the purpose, the closing note and, on the Warren, the nights-remain text; a "Days left · Open missions" line shows at the Dawn plan.
- War council: `HomeDayHUD.Council.cs`, a banner in the prologue's style at the Day 1 Dawn plan (two placeholder lines, John and Mary), once.
- Sky (`HomeWorldMoons.cs`): Great Moon redder per day, Mountain Light colder per day, Little Moon moves along an arc by the clock.

**Verified.** Edit-mode tests (command line, editor closed): **265 run, 264 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Was 246 before; +19 new tests in `HomeSimulationTests.Calendar.cs` (Might counts and hidden threads, scouting run, nights-remain text, days-left line, calendar priority, "+N", hidden Omen never shown, stars until charted, ripening and delivery days, purpose derivation and override, closing note, haul, card text, Warren danger, war council once and saved, sky numbers).

**Not verified.** Nothing from step 2 was seen in Play (see the status note under "After step 2" in M9-Playtest-Plan.md).

**Not built.**

- The Dawn tick camera glide and sting (first two Dawns). It needs camera bounds tuning like `HomeGreatMoonRise`.
- The Warren's own large icon and the corruption overlay that grows per day (no art).
- Haul icons with counts on the mission node or card: the haul is text in the card's "Drops:" line.
- The Queen's Might "crack" animation and the dinner reaction when a thread is cut.
- Map table moon countdown beyond the text label.
- Tooltips on the pips are shared with the day hover; no pip-level detail.

**Findings.**

- The Home HUD's moon cells used to ignore the mouse; they now take hover, so the moon strip blocks clicks like the panel always did. Watch for the camera edge scroller while hovering the strip.
- A resumed Day 1 save shows the war council once (the flag defaults false). Later days never show it.
- Little Moon arc dimensions are a guess (4 radii wide, 1.5 high); the Moon 05 object may be sized differently in the scene.
- Session note: edits were repeatedly blocked by the auto-mode classifier ("no verdict") and prompted per file; it did not affect the code.

**Demo Spec edit (owned by step 2), ready to paste. Missions:**

> The Warren has a fixed node on the world map: it keeps its authored position every day and never shifts with the side missions. Its card shows the Queen's remaining threads as a danger rating and labels any attempt made while a thread stands as a "Scouting run: you'll face her at full strength."

**Files for THJ to commit.** New (each with `.meta`): `Runtime/Simulation/HomeGoal.cs`, `Runtime/Simulation/HomeCalendar.cs`, `Runtime/Simulation/HomeSimulation.Goal.cs`, `Runtime/Presentation/HomeSkyDecay.cs`, `Runtime/Presentation/HomeTimeHud.Goal.cs`, `Runtime/UI/HomeDayHUD.Council.cs`, `Editor/HomeSimulationTests.Calendar.cs`. Modified: `Runtime/Definitions/HomeMissionEntry.cs`, `Runtime/State/HomeSaveData.cs`, `Runtime/Presentation/HomeTimeHud.cs`, `Runtime/Presentation/HomeWorldMoons.cs`, `Runtime/UI/HomeDayHUD.cs`, and `Core/UI/Runtime/Home/WorldMap/WorldMapPanelUI.cs`. No scene, prefab or demo-content changes: the new serialized fields default in code (the world map's `warrenOffset` and `warrenScale` are on the panel component; the scene keeps the defaults until you tune them). Existing `HomeMissionEntry` assets get `purpose = Auto`.

## M9 Step 3a: Station badge state (Oct 5)

**Built.** `Runtime/Simulation/HomeStationState.cs` (pure C#, no scene or prefab changes). `HomeStationState.All(sim)` returns one `StationBadge` per room in cycle order (a room with a day and a night station shows the one that fits the phase); `For(sim, station)` and `ForRoom` give one. A badge carries:

- seat pips: `Filled` of `Seats` for the first slot still open to planning (`FocusSlot`, null when nothing can be planned);
- `State`: Locked (prologue), Working (someone seated or the owner works), Ready (an order or crop lands at the next Dawn; a late order never counts), NeedsInput (Ben has no order, Mary has no daily recipe, the Study desk is empty), Blocked (no free character can take any seat; `Reason` is the most common refusal), else Idle;
- `Progress` ("Study 1/2", "Ripe tomorrow", "Ripe in N dawns", "Ready at Dawn", "Ready in N Dawns", "No order", "Pantry x/y", "Desk empty", the Wounded line);
- `Warning` ("Feed runs out: no eggs tomorrow", "Arrives after the full moon");
- `Owner`, `OwnerWorking`, `OwnerLine` ("Mary cooks 1 Gourd Omelette this afternoon", "Uncle Ben is idle. Place an order."). Blocked reuses `CheckSeat` plus `HomeSeatRules.Evaluate` (the rules `TryAssign` uses), so a badge and its window cannot disagree. It changes nothing in the sim.

**Verified.** Edit-mode tests (command line, editor closed): **277 run, 276 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Was 265; +12 in `HomeSimulationTests.Badges.cs` (one badge per room in cycle order, reading changes nothing, Study idle/working/empty desk, Care blocked/idle/working, Homestead blocked and ripe lines, hen feed warning, Mary works only when her recipe can be cooked, a helper takes over from Mary, Workshop idle/working/ready/late, prologue lock, no planning phase).

**Not verified.** Nothing is visible in Play yet (3a has no UI).

**Findings.**

- First run had one real bug: the blocked check used `CheckTask`, which refuses a seat with no plot or recipe chosen, so every Kitchen/Homestead seat looked blocked. Fixed to use the seat rules.
- A Wounded character at 1 dawn left is already recovering, so the Care carer seat is closed (Step 1 rule); the badge shows Blocked then.
- Not tested: the night-phase room pick (Vigil badge in the Care room), which needs a fixture advanced to NightPlan.
- Recap grouping (gained, spent, progressed, unlocked) moved to 3d, where the strip needs it.

**Decisions (THJ, Oct 5) for 3b.** Prop indicators open the Home station windows. The Map Table stays on the Fireplace ("Start Game", `ShowWorldMap`). Hearth / Fireside Talk gets its own placeholder indicator. Grandma Table / Alchemy Bench keeps opening the character skill-tree upgrade menu (`ShowAbilityUpgrades`) as before. Home camera gets soft bounds and a reset with the overview key (3c).

**Demo Spec edits.** None.

**Files for THJ to commit.** New (each with `.meta`): `Runtime/Simulation/HomeStationState.cs`, `Editor/HomeSimulationTests.Badges.cs`.

## M9 Step 3b: Props are the stations, badges (Oct 5)

**Built.**

- `Runtime/Presentation/HomeStationProp.cs`: `HomeStationProp` (click opens the room's station window through the new shared `HomeRoomHotspot.OpenRoom`; hover enlarges the indicator 15%; the main instance veils the indicator while the prologue keeps the room closed) and `HomeStationBadgeView` (world-space panel in the Bubble layer, unlit material set before the sprite: seat pips, state word on a colour stripe, progress line, one note line = Blocked reason, else Warning, else owner line). It refreshes 4 times a second from `HomeStationState.ForRoom`, which now works out one room only.
- `HomeRoomHotspot`: new `opensOnClick` switch (default true) and a public static `OpenRoom(roomId)`. The room boxes stay as drag-and-drop targets until 3c; they stop opening windows (and showing their hover label) once a room has a prop. The Dining Table box is untouched.
- `Editor/HomePropBuilder.cs`, menu `Tools/Home/Build Station Props` (idempotent, adds only what is missing, never moves a nudged object):
  - Study, Workshop, Kitchen and Yard: the existing `HomeInteractables` on Bookshelf, Equipments Cabinet, Cooking Cabinet and Training Field get a `HomeStationProp`; their old `HomeManager` PointerDown call and the old mission-unlock gate are cleared (the sim's prologue gates them now); each indicator gets its own collider so the diamond is clickable.
  - New placeholders (a `HomeIndicator` duplicate named `Indicator - <label>` under the same world canvas, plus an empty `Prop - <room>` with a collider under `Station Props` to drop art on): Care (-11.6,-2.6), Hearth / Fireside Talk (-5.5,-2.0), Porch (-0.2,-9.6), Homestead (32.1,-7.1), Stargaze (-1.0,11.0). Positions are guesses from the room table; nudge them in the Scene view.
  - Left as they were (per THJ): Fireplace = Map Table ("Start Game", ShowWorldMap), Grandma Table = Alchemy Bench (ShowAbilityUpgrades), Dining Table box.
- The builder was run once (batch mode): "4 existing props retargeted, 5 placeholder indicators added, 9 room boxes now drop-only".

**Verified.** Code compiles; edit-mode tests unchanged: **277 run, 276 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). The builder ran without errors.

**Not verified.** Nothing seen in Play (see "After step 3" in M9-Playtest-Plan.md, items 1, 2 and 4). Especially check: indicators clickable and opening the right window; badge position and readability (offset is `badgeOffset`, default 0,3.9 above the indicator root); no double click (old screens must not open); placeholder positions; prologue veil hides indicator and badge; Great Moon focus still blocks clicks.

**Findings.**

- Scene diff check: no object was removed (every object id from HEAD is still there; 63 added, prefab instances 45 to 50). `git diff` shows the Mary-Entity and Fireplace instances as changed only because the new indicator instances sit next to them; both are identical to HEAD. The only removals are inside the four retargeted `HomeInteractables`: their `PointerDown` calls and their `UnlockAfterMissions` lists.
- The Workshop prop used to open the old equipment-upgrade screen and the Kitchen and Study props the old stat-upgrade screens; those paths are now only reachable through the sim's windows.
- Still to do for the same step: the dock, roster and overview (3c), the recap strip (3d), Mary and Ben at work and lapse effects (3e). Mary/Ben badges show in the badge note line for now.

**Demo Spec edits.** None.

**Files for THJ to commit.** New (each with `.meta`): `Runtime/Presentation/HomeStationProp.cs`, `Editor/HomePropBuilder.cs`. Modified: `Runtime/Presentation/HomeRoomHotspot.cs`, `Runtime/Simulation/HomeStationState.cs` (3a file, ForRoom change), and the scene `Features/Home - Imported/___Khashayar/Home - Scene.unity`.

**3b follow-up after the first Play look (Oct 5).**

- Badge now sits under the diamond (the indicator's name floats above it), 1.4x larger with bigger text; rows that are empty are left out, so a station with nothing to say is a one-line badge. New serialized field `badgeOffsetBelow` (default 0,0.95) replaces `badgeOffset`.
- Care was placed on top of the Alchemy Bench (the old Care box was also measured on the lab room, not the bed room). Care indicator and prop now at (-6.8,5.0); the Care drop box at (-5.3,6.5, 8x6.4); `HomePresentationBuilder`'s room table updated to match. `HomePropBuilder` moves a placeholder only while it is still exactly at its old default, so nudged ones stay. The Alchemy Bench (Grandma Table) still opens the skill-tree menu; it was only hidden under Care's indicator and collider.
- Hover outline: hovering a diamond now lights the prop's orange outline (the prop's own `HomeInteractables` overlay, called from the diamond); the placeholder props with no art get a generated orange box around their collider. Fireplace and Grandma Table are unchanged.
- Tests unchanged: 277 run, 276 pass (AI baseline red). Builder re-run: 0 new indicators, Care moved.

## M9 Step 3 (rest): badges tuned, dock, roster, overview, recap, workers and effects (Oct 5)

**Built.**

- **Badge (3b tuning, after Play looks).** Rows are measured so they never overlap (the note wraps to two lines when needed); the badge sits under the diamond, scale 1.1, smaller fixed text; empty rows are left out. New per-prop option **Badge Side** (Bottom default = the old spot, Top, Right, Left, Custom + Badge Custom Offset); selecting a prop shows the badge box as a gizmo. Care indicator, prop and drop box moved to the bed room (it sat on the Alchemy Bench); `HomePresentationBuilder`'s room table updated. Hovering a diamond lights the prop's orange outline (its own `HomeInteractables` overlay, or a generated box around the collider for the placeholders).
- **3c Dock, roster, overview.** `Runtime/Presentation/HomeStationDock.cs`, an overlay canvas at sorting order 18 along the bottom:
  - station dock: one button per room in cycle order (state word and colour from `HomeStationState`), then the Map Table; click or hotkeys 1-9 then 0 glide the camera to the prop and open its window (the Map button clicks the Fireplace's own interactable); hovering a button lights the prop's outline; locked rooms are disabled;
  - roster strip: a portrait per family member with Morning / Afternoon / Night chips (station, Free, Hurt, Away, Picnic, "-" when closed); drag a portrait onto a dock button to seat the character through `HomeSeatPlanner` (same rules and toast as dropping on a room);
  - overview: the O key or the first dock button frames the house (room boxes inside the walls, not Yard, Homestead or Roof) with `CameraHandler.FocusAndZoom`; the camera returns there at each phase change once nothing else moves it (time-lapse, windows, Great Moon focus or rise, world map);
  - it hides during the prologue, a time-lapse, the world map and the Great Moon's rise. The edge scroll already blocks over UI, so no extra suspension was needed.
  - Pure logic in `Runtime/Simulation/HomeRoster.cs` (`HomeRoster.Chips`, `HomeOverviewMath.Frame`, `HomeDockKeys`).
- **3d Recap strip.** `Runtime/Simulation/HomeRecap.cs` (pure: two snapshots plus report lines give Gained, Spent, Progressed, Unlocked, plus a small Notes list for warnings) and `Runtime/Presentation/HomeRecapStrip.cs` (overlay canvas, order 19). After every time-lapse `HomeTimeFlow` shows the strip titled "Dawn to Noon" and so on, or "Overnight" for the sleep lapse (the night's lines, charts, Omens, Bond and warnings fold into the Dawn recap). It hides after 10 s (hover keeps it open), collapses into a "Recap" tab that reopens it, and after a reload the first Dawn plan builds it from last night's lines alone. The "Last night" card is gone (`HomeDayHUD.Night.cs` hooks are no-ops).
- **3e Mary and Ben, work effects.** `Runtime/Presentation/HomeWorkFx.cs`: `HomeOwnerWorker` (on the scene's `Mary-Entity` and `Ben-Entity`: they slide to the kitchen or workshop indicator when the badge says the owner works, else back to where they were authored; no walk art yet) and `HomeWorkFx` (placeholder squares during a lapse while a kind is being worked: smoke at the Kitchen, sparks at the Workshop, pages in the Study, dust in the Yard, leaves in the Homestead). `HomeTimeFlow.IsWorking(kind)` is the switch. The builder attaches both (`Tools/Home/Build Station Props`, now: 4 retargeted, 9 room boxes drop-only, 2 owners at work, 5 work effects).
- New statics have `PlayModeStaticReset` hooks (`HomeStationDock`, `HomeRecapStrip`; `HomeTimeFlow`'s reset now also clears the working set).

**Verified.** Edit-mode tests (command line, editor closed): **288 run, 287 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Was 277; +11 in `HomeSimulationTests.Recap.cs` (recap empty, stores gained and spent, crop and recovery progress, workshop order progress and delivery, report lines to Unlocked and Bond sums, a real slot's study progress, roster chips for seats, Hurt, Away, Picnic and closed slots, skill points unknown, overview framing, dock keys). The builder ran twice without errors; no scene object was removed (checked against HEAD).

**Not verified.** None of the UI was seen in Play: dock layout and hotkeys, camera glide and overview, drag to dock, the recap strip (timing, content, the Dawn fold), Mary and Ben moving, the effects. See "After step 3" in M9-Playtest-Plan.md.

**Not built / findings.**

- Skill-point badge on the roster: `HomeRoster.UnspentSkillPoints` returns -1 (hidden) until Step 5 wires the skill-tree count and the route to the trees.
- Lit windows at night and the dinner bell: no art or objects for them yet.
- Mary and Ben have only an Idle clip each, so they slide without a walk; Ben has a "work" idle sprite sheet and Mary a "cooking" one that are not used yet (Step 4 idle wiring).
- Overview key is O (not in the design); the Dusk report and the other cards are unchanged.
- Camera limits: the existing boundary fit stays; the overview does not change it.
- The roster drag only targets dock buttons (dropping on the world still works through the avatars).

**Demo Spec edits.** None.

**Files for THJ to commit.** New (each with `.meta`): `Runtime/Simulation/HomeRecap.cs`, `Runtime/Simulation/HomeRoster.cs`, `Runtime/Presentation/HomeStationDock.cs`, `Runtime/Presentation/HomeRecapStrip.cs`, `Runtime/Presentation/HomeWorkFx.cs`, `Editor/HomeSimulationTests.Recap.cs`. Modified: `Runtime/Presentation/HomeTimeFlow.cs`, `Runtime/UI/HomeDayHUD.Night.cs`, `Editor/HomePropBuilder.cs`, `Editor/HomePresentationBuilder.cs` (care row), `Core/Managers/PlayModeStaticReset.cs` (two lines), and the scene `Features/Home - Imported/___Khashayar/Home - Scene.unity`.

## M9 Step 4a: placement without wandering (Oct 6)

**Built.**

- `HomeHouseLayout`: `WanderEpoch`, `WanderRooms`, `WanderRoom` and `Wanders` are gone. `Place` now decides in this order: squad (Door / away), Dusk (Dining), a seat (the station room; a carer at the patient), Wounded (care bed), then **Dawn plan and night: `bedroom-<Name>`**; by day the first idle characters on the Porch (Bond), everyone else at **`spot-<Name>`** for the whole slot. `FallbackAnchor` names the room a missing `spot-` / `bedroom-` anchor stands in for (Linda and Toba homestead, Mark yard, Lucy roof, John workshop; every bedroom the hearth). The signature no longer carries an epoch.
- `HomeHouseView`: the wander timer is gone; `AnchorOf` uses the fallback when the scene lacks the anchor.
- `HomeHouseBuilder`: adds 5 `spot-*` and 5 `bedroom-*` anchors (only missing ones; builder run once in batch mode: 22 anchors). **Coordinates are guesses**; 4b proposes better ones from the idle data.

**Verified.** Edit-mode tests (command line, editor closed): **289 run, 288 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Was 288. In `HomeSimulationTests.House.cs` the Wander tests are replaced (Dawn bedroom, night bedroom, Porch then own spot, no position change inside a slot and distinct spots, fallback anchors). Net +1.

**Not verified.** Nothing seen in Play (Dawn bedrooms, spots, nobody moving mid-slot).

**Findings.** Running the builder rewrote the five `AC_HouseAvatar_*.controller` files (it recreates them each run): commit noise, not a change.

**Demo Spec edits.** None yet (Step 4 owns Kevin and the Porch / Fireside names).

**Files for THJ to commit.** Modified: `Runtime/Presentation/HomeHouseLayout.cs`, `Runtime/Presentation/HomeHouseView.cs`, `Editor/HomeHouseBuilder.cs`, `Editor/HomeSimulationTests.House.cs`, the Home scene (anchors). Optional noise: the five avatar controllers.

## M9 Step 4b: idle inventory and mapping proposal (Oct 6) - NOT WIRED, waiting for THJ

### What MortaStory ships (447 `HomeIdleDefinition`s in `MortaStory/Content/Story/HomeIdles`)

Actors use Morta's names. Mapping to Home characters: **Father = John, Mother = Mary, Uncle = Ben, Daughter 01 = Linda, Son 01 = Mark, Son 02 = Kevin, Lucy = Lucy, Cousin = Joey (dropped, no Home role), Grandma = Margaret (no Home role), Siou = the baby.** Toba has no actor.

Fields that matter: `_actors` (who it uses), `_area` (the rect where it plays, **in manor coordinates, which are the Home scene's coordinates**: the Dining anchor sits inside the WarReport rect), `_areaType` (1 John, 2 Mary, 4 Ben, 5 Joey, 6 Mark, 7 Linda, 8 Kevin, 9 Lucy = that person's own area; 10 = hall pair or group; 11 = scene with 2+ actors (`_isHie`); 12 Siou; 15 Amir; 0 = a prop idle at 0,0), `_busyPriority`, and `_conditions` / `_moods` (Morta story conditions: the Home system would ignore them and choose by its own rules).

| Kind | Count | Notes |
| --- | --- | --- |
| Solo, per character | John 16, Mary 18, Ben 16, Linda 13, Mark 12, Lucy \~23, Kevin 17, Joey 17 (unused) | e.g. `MarkMeditate`, `LindaPlayViolin`, `LucyPaint`, `BenWorking`, `MaryCook`, `JohnReading`, `KevinTraining` |
| Pairs and groups | \~45 | `JohnBenTalk`, `LindaLucyFish`, `LindaKevinCat`, `MaryLindaCombing`, `MaryJohnFurniture`, `MarkLucyPlay`, `RopePlaying`, `Boardgame`, `FamilyHope` (8+ actors by the fireplace) |
| Family scenes at the Dining Table | 10 | `FamilyDinnerPray`, `FamilyDinnerSad`, **`WarReportCA1-3`, `WarReportMA1-2`, `WarReportWA1-3`** (the "war report" idle: the family sits around the table) |
| Bed props | \~12 | `Idle <Name> Bed` (absolute position, no area), plus `LindaInBed`, `JoeySleep`, `MaryCleanBed`, `MaryMarkCare` |
| Props, animals, portals, corruption | \~330 | Not characters. Ponds, corruption and portals belong to the world, not to this step |
| Cutscenes | 614 folders | `John_Leaving_sequence` (48 s, skippable, 15 actors: John says goodbye at the Door to Mary, Ben, Linda, Grandma, Joey...) |

### What plays today

`HomeStateManager` (`Core/Home/Runtime`) picks a `HomeState` asset by the furthest (or most recent) completed mission and plays its idle list (`M1` to `M7 - HomeState.asset`). **`M4 - HomeState` contains `WarReportMA1`**: that is the table scene, and it plays whenever M4 is the active state, whatever the Home sim does. Two `HomeState` types exist (`MISO.Core.Home` idle lists vs the sim's `Runtime/State/HomeState.cs`).

### Proposal

**A. A director on top of `HomeStateManager`.** A small `HomeIdleDirector` (scene MonoBehaviour next to `HomeDayRunner`) works out the wanted idle set from the sim and hands it to the manager. Changes to `HomeStateManager` (shared file, small): a flag `externalControl` that stops `RefreshFromGameState` from loading a mission state (this removes `WarReportMA1` by default), and a public `ApplyIdles(list of (HomeIdleDefinition, offset))` that `ApplyState` also uses. The manager already skips an idle whose actors are already in use, so the director only has to order its list by priority.

**B. One owner per character: hide the avatar while an idle claims them.** The director maps each idle actor to a roster character (table above) and tells `HomeHouseView`: this character is in an idle, hide their `HomeAvatar` (and, for Mary and Ben, their `-Entity` figure and `HomeOwnerWorker`); when the idle ends, show it again at the same spot. That ends the double (seated at the table and wandering). Rule: an idle plays only if every roster actor in it is free for it; otherwise the group falls back to solo idles or plain avatars. Non-roster actors (Grandma, Siou) are scenery.

**C. Mapping** (what plays when):

| Where / when | Idle | Who |
| --- | --- | --- |
| **Dusk, Dining Table** | `FamilyDinnerPray` Days 1-3, `WarReportWA1` Days 4-5, `WarReportCA3` Days 6-7 (all include Grandma and none include Joey; Toba, with no art, stands at the table's edge) | the whole family |
| **Night, bedroom** | the `Idle <Name> Bed` props and `LindaInBed` etc. for a character without a night seat; the lights go out | Linda, Lucy, Mark, John, Kevin |
| **Personality spot (day)** | Linda `LindaPlayViolin` (10.8,6.2), Mark `MarkMeditate` (-15.5,-5.9), Lucy `LucyPaint` (-0.8,-5.9) or `LucyFishes` (6.0,7.4), John `JohnReading` (0.3,-2.7) or `JohnWatchCliff`; Toba keeps combat art at the barnyard (about 19,1, where `KevinBarnyard` and `LucyBarnyard` play) | solo |
| **Stations** | Kitchen `MaryCook`; Workshop `BenWorking` / `BenForge`; Study `MarkStudy`, `JohnBookShelf`, `MaryReading`; Yard `LucyTraining`, `KevinTraining`, `JohnSword`, `JoeyMarkTrain` style trainers; Care `MaryMarkCare`, `KevinMaryCare`; Stargaze `KevinWatch`, `AmirKabirTelescope`; Homestead `KevinBarnyard`, `LucyBarnyard` | the seated character; pair idles play when both seats are filled |
| **Porch Break / Fireside Talk** | Porch pairs `LindaLucyFish`, `MarkLucyPlay`, `LindaKevinCat`; Fireside `FamilyHope`, `MaryJohnFurniture` or `MaryLindaCombing` by the fireplace | the two or more seated |
| **Door / send-off** | `JohnGate` while the squad waits; **`John_Leaving_sequence`** (48 s, skippable) as the Send-off scene the first time, later days a short see-off from the family idles at the Door | the squad and those at home |

Toba has no Morta art: he keeps the combat-art `HomeAvatar` everywhere (no group idle can include him). Joey's actor appears in some scenes (`FamilyDinnerSad`, `WarReportCA1`...): the proposal avoids those.

**D. Bedroom and spot anchors from the data.** Replace my guessed bedroom anchors with where the idles put people: Linda (10.8,6.3), Lucy (10.5,4.2), Mark (-12.2,-8.2), Kevin (-12.3,8.0), Mary and John (-8.4,5.9, the parents' bed), Toba in Joey's room (-15.7,-7.4). Spots as in the table. The builder would only move anchors still at their default and leave nudged ones alone.

### Questions for THJ

1. Dining: `FamilyDinnerPray` / `WarReportWA1` / `WarReportCA3` by day as above, or one scene for all days?
2. Send-off: the 48 s John Leaving scene on the first sortie only (skippable), or every sortie (too long, I think)?
3. Group idles: play only when all their roster actors are free (my proposal), or also when one is missing (the missing one would show as an avatar next to the idle)?
4. Spots: OK to move Linda's to her room (violin there, not in a garden), Mark's to his meditation corner and Toba's to the barnyard? And Lucy: paint (hall), fish (pond) or stay on the roof (no idle there, so avatar only)?
5. `HomeStateManager`: OK to add `externalControl` and `ApplyIdles` (shared file, about 30 lines, no behaviour change when the flag is off)?

**Not built.** No idle is wired. No file under `MISO.Core.Home` or `MortaStory` was changed.

## M9 Step 4b (wired): Morta idles chosen by the Home system (Oct 6)

THJ's answers: Dining scene by day; send-off scene first time only and short later, using the prefab's content rather than the whole cutscene (4e); group idles play even when one character is missing, as a switch; Linda, Mark, Toba spots moved to the idle positions, Lucy paints; `HomeStateManager` may get the two additions.

**Built.**

- `HomeStateManager` (shared, additive): `ExternalControl` (when true, `RefreshFromGameState` does nothing, so a mission's state such as M4's `WarReportMA1` no longer plays by itself) and `ApplyIdles(list)`; `ApplyState` now builds its list and goes through the same private `Apply` (same validation and warnings). No change while `ExternalControl` is false.
- `Runtime/Definitions/HomeIdleCatalog.cs`: ScriptableObject of `HomeIdleRule`s (idle, context Dining / Door / Pair / Station / Spot / Bed, key, day range, cast). Asset: `Content/Home/Presentation/HomeIdleCatalog.asset` (15 rules).
- `Runtime/Simulation/HomeIdlePlanner.cs` (pure): from the same placements the avatars use (`HomeHouseLayout.Place`), picks the idles to play and who each one shows (`Leaders`, `Claims`). Order Dining, Door, Pairs, Stations, Spots, Beds; a character is claimed once; the squad away is never claimed. `strictGroups` off (default) = a group idle plays even if some of its characters are busy elsewhere; on = only when all are free.
- `Runtime/Presentation/HomeIdleDirector.cs` (scene, "Idle Director"): every 0.25 s plans, waits until the leaders have stopped walking, hands the idles to `ApplyIdles`, and hides every claimed figure (`HomeAvatar.SetClaimed`; Mary-Entity and Ben-Entity for Mary and Ben). In the prologue it hands control back to the manager (old behaviour). Inspector switch **Strict Groups**.
- `HomeAvatar`: `SetClaimed` / `Claimed`; `PlaceAt` and `WalkTo` respect it.
- Catalog contents: Dusk Dining `FamilyDinnerPray` D1-3, `WarReportWA1` D4-5, `WarReportCA3` D6+; Door `JohnGate`; spots `LindaPlayViolin`, `MarkMeditate`, `LucyPaint`, `JohnReading` (Toba keeps his avatar, at the barnyard); bed `LindaInBed`; stations `MarkStudy`, `JohnBookShelf` (Study), `LucyTraining`, `JohnSword` (Yard); pairs `LindaLucyFish`, `MarkLucyPlay` (Porch or Hearth).
- Anchors moved to the idle positions (spots and bedrooms; `HomeHouseBuilder` moves only those still exactly at the 4a guesses; builder run: 23 anchors). Tools: `Tools/Home/Build Idle Director` (idempotent, adds missing rules only).

**Verified.** Edit-mode tests (command line, editor closed): **298 run, 297 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Was 289; +9 in `HomeSimulationTests.Idles.cs` (nothing in the prologue or without rules, Dawn bed idle, spots by day, pair claims once, station idle, Dining by day and who it claims, Door and never the away, strict vs lenient, stable signature). Both builders ran without errors; all 15 idles were found.

**Not verified.** Nothing seen in Play. Check: no figure appears twice; the avatar hides when its idle starts and returns at its spot when it ends; the Dusk table scene and its position; `WarReportMA1` is gone; Mary and Ben vanish from their scene spot while the Dining idle plays and come back after; the prologue still plays the old idles.

**Findings and limits.**

- The idle plays at its authored position, not at the station anchor: a seated Mark walks to the Study anchor, then the `MarkStudy` idle appears a few metres away (and the avatar returns to the anchor when it ends). Nudge the anchors or accept.
- A claimed character's bubble is hidden with the avatar.
- Mary's and Ben's own work idles (`MaryCook`, `BenWorking`) are not wired: the slide-to-work stand-in stays.
- Only Linda has a "person in bed" idle; the others stay avatars in their bedroom at night. The `Idle <Name> Bed` props are not used (they would show an empty bed under an avatar).
- Joey and Grandma appear in no chosen scene except Grandma at the table (scenery).
- The send-off scene (4e) and Kevin (4d) come next.

**Demo Spec edits.** None.

**Files for THJ to commit.** New (each with `.meta`): `Runtime/Definitions/HomeIdleCatalog.cs`, `Runtime/Simulation/HomeIdlePlanner.cs`, `Runtime/Presentation/HomeIdleDirector.cs`, `Editor/HomeIdleDirectorBuilder.cs`, `Editor/HomeSimulationTests.Idles.cs`, `Content/Home/Presentation/HomeIdleCatalog.asset`. Modified: `Core/Home/Runtime/HomeStateManager.cs` (shared), `Core/Managers/PlayModeStaticReset.cs` (one line), `Runtime/Presentation/HomeAvatar.cs`, `HomeHouseLayout.cs`, `HomeHouseView.cs`, `Editor/HomeHouseBuilder.cs`, `Editor/HomeSimulationTests.House.cs`, the Home scene. Noise to skip: the five avatar controllers.

## M9 Step 4c: Home barks (Oct 6)

**Built.**

- **CSV** `Content/Home/Barks/HomeBarks.csv`, the bark system's format (Unit, Tag, Weight, PlayOnce, Dialogue) plus an ignored Notes column. **78 placeholder lines**, all tagged `[PLACEHOLDER]` (stripped on screen by `HomeText.Display`). Unit is the speaker (John, Linda, Lucy, Mark, Toba, Mary, Ben, Kevin). **Tag = `trigger[:detail][@fromDay-toDay]`**, e.g. `dawn@1-2` (calm), `dawn@6-7` (the last days), `assign:Kitchen`, `result:Study`. A line may use `{who}` (the other character involved; lines with `{who}` are skipped when there is no one else), `{day}`, `{left}` (days to the full moon). Weight is the pick weight; PlayOnce plays once per session.
- **Triggers** (all fire from the sim, nothing else): `dawn`, `noon`, `dusk`, `night`, `pantrylow` (Mary, at Dawn with 0-1 portions), `daysleft` (at Dawn, 3 or fewer days left), `assign:<station kind>` (a new seat, with the others at the station and a character target as `{who}`), `result:<station kind>`, `bond`, `bondlevel`, `wounded`, `recovered`, `sortiewon`, `sortielost`, `queen`, `omen`, `chart`, `scene`, `threadcut` (an Outcome line containing "thread"), `warning`, `idle` (45 s of quiet while planning). Not built: a "new unlock" trigger (no clean event to hang it on).
- **Code.** `Runtime/Simulation/HomeBarks.cs` (pure): `HomeBarkTable.Parse` (reuses `BarkDialogueCsvParser`), `HomeBarkTriggers` (`FromEntry` reads report lines, `ForPhase`), `HomeBarkPicker` (deterministic: seeded by day, trigger and a counter, never by the clock; no repeat among the last 14 lines until the pool runs out; the exact detail beats a row with no detail; characters involved speak first; the speaker must be on screen). `Runtime/Presentation/HomeBarkDriver.cs` (scene object "Bark Driver"): one balloon at a time through `HomeSpeech`, at least 5 s apart, higher priority first, held while a window is open or a time-lapse plays, anything older than 20 s dropped. Reload after editing the CSV in Play: component menu **Reload barks**. Tool: `Tools/Home/Build Bark Driver` (idempotent; never touches the CSV).
- Speakers who are hidden (inside an idle, away on the sortie) are skipped; a line goes to another speaker.

**Verified.** Edit-mode tests (editor closed): **313 run, 312 pass**, 1 fail (`AIRegressionTest.Baseline_MatchesCurrentAI`, as expected). Barks: 8 tests in `HomeSimulationTests.Barks.cs` (tag syntax, the shipped CSV parses with no warnings and only known speakers and triggers and the placeholder tag, determinism, no repeats, filters by day, detail, speaker and PlayOnce, involved first and `{who}`, report to trigger mapping, Dawn pantry and days-left). Builder ran: driver in the scene with 78 lines.

**Not verified.** Nothing seen in Play: balloon timing and position, how often it speaks, whether the idle bark is too chatty (`idleAfter`, `gap` are inspector fields), whether `bond` fires too often (one per pair gain). The 24 placeholder lines in `HomeDemoContentBuilder.cs` are unchanged: they stay for you to fold in with the CSV.

**Demo Spec edits.** None.

## M9 Step 4d: Kevin (Oct 6)

**Built.**

- **Sim.** `HomeCycleDefinition.homeOnlyCharacters` (keys; the demo cycle has "Kevin"). `HomeSimulation.Roster` is the fighters then the home-only family; new `HomeOnly` and `Fighters`. Kevin: **chore seats only** (`CheckSeat`: Helper seat at the Homestead or the Kitchen, a day slot, else "Kevin only helps with the chores (Homestead or Kitchen, by day)"), so not the Study, Yard, Care, Porch or any night seat; **no sortie** ("Kevin never goes on a sortie"); **no Bond** (`ClaimBond` ignores any pair with him; the starting-Bond loop uses `Fighters`; the Picnic and every resolver go through `ClaimBond`); never fills a Porch seat while idle. He shows as Free in the roster strip.
- **Content.** Homestead helper seats 2 to 3 and Kitchen helper seats 1 to 2 (his chore seats; the fighters can use them too). `Tools/Home/Apply Step 4 Content (Kevin, names)` applied it to the existing assets (idempotent); `HomeDemoContentBuilder` carries the same for a rebuild. The Demo Content test was updated to 3 and 2.
- **Look.** `HomeHouseBuilder` builds Kevin's avatar from `Features/NPCs/Kevin/Stand` and `Move` side sprites (6 and 8 frames, clips and controller in `Content/Home/Presentation/Avatars`; scale 3.5 like the scene's `Kevin-Entity`, which is hidden once the house view is on). His spot is the barnyard (`spot-Kevin`, plays `KevinBarnyard`), his bedroom `bedroom-Kevin`; he sits at the Dining Table scene.
- Not built: his Up/Down sprites are unused (the avatar is side view like the others); no talents or affinities (base effect).

**Balance check (estimate, NOT run through the forecast).** Seats per day (2 day slots): Homestead 2 to 3 and Kitchen 1 to 2 means +2 chore seats in each of the 2 slots, +4 seat-slots a day, not +2: the design doc counts "+2 chore seats a day", so one of the two numbers has to change. If you want exactly +2 a day, make only the Homestead 3 and leave the Kitchen at 1. A plot takes one tending per slot and the pantry caps the Kitchen, so the extra Kitchen seat helps little. The doc's worst case (+14 crop yield a week) assumes one extra Homestead seat. I did not run a with/without-Kevin forecast; the pieces for it exist (`Forecast`), and I can do it when the number is decided.

**Verified.** Edit-mode tests as above; `HomeSimulationTests.Kevin.cs`: on the roster but not a fighter, chore seats in both slots, refused everywhere else with the reason, never on a sortie, no Bond and not on the Porch, his placement (bedroom at Dawn, spot by day). Builders ran without errors: 6 avatars, 24 anchors, 16 idle rules.

**Not verified.** Nothing seen in Play: Kevin's avatar size, facing (the art is assumed to face right) and walk, whether the sprite sheets loop correctly, whether the old `Kevin-Entity` figure hides, the roster strip and dock with a sixth character.

**Demo Spec edits (ready to paste).**

- *Roster:* "Kevin is a home-only family member. He takes only chore seats: a Helper seat at the Homestead or the Kitchen, in either day slot. He has no talents (base effect), earns no Bond, takes no Porch, Study, Yard, Care or night seat, and never goes on a sortie."
- *Homestead and Kitchen:* "Homestead: 3 Helper seats (2 + Kevin). Kitchen: 2 Helper seats (1 + Kevin)." (change the Kitchen to 1 if you want exactly +2 chore seats a day, see the balance note).
- *Stations:* "The Porch is called Porch Break (costs a day work slot). Hearth Time is called Fireside Talk (costs one of the two night seats)."

## M9 Step 4e: the Send-off at the Door, names (Oct 6)

**Built.**

- **Gathering.** While the Send-off window is open (`HomeHouseLayout.SendOffOpen`, set by `HomeSendOffWindow`), everyone who stays home walks to the Door to see the squad off (the Wounded stay in bed); when the window closes they go back to their rooms or stations. `JohnGate` plays at the Door when John is in the squad. The family's spoken line, the meal and the mission preview in the window are unchanged.
- **Names.** Porch Break and Fireside Talk (assets, builder, and the windows' texts), each window with a "Costs:" line (a day work slot; one of the two night seats). Station ids are unchanged.

**Not built (needs your decision): the John Leaving scene.** `John_Leaving_sequence` is a Timeline cutscene (director prefab with a `PlayableDirector`, `CutsceneBindings`, camera rigs, 48 s). This project has no runtime player for it: Morta's player lives in the editor-only Story Viewer (`StoryStage.LoadCutscene`, about 100 lines of loading: spawn the actors from the registry, bind them, point the rigs at the camera, drive the director). A runtime port is doable, but it takes over the camera (`CutsceneCameraRig`) from `CameraHandler`, and I cannot check that in Play from here, so I did not ship it. What I can build next, if you want it: a `HomeCutscenePlayer` that plays only a time range of that director (the goodbyes, markers "10. His Mission" to "13. His Wife") once, first sortie only, skippable, with the camera handed back after. Until then the see-off is the family at the Door plus `JohnGate`.

**Verified.** Test `SendOff_WhileTheWindowIsOpen_...` (the family gathers, the Wounded stay in bed, the signature changes, back to their rooms when closed). Suite: **313 run, 312 pass**, only the AI baseline red.

**Not verified.** Nothing seen in Play: how the family crowd at the Door (spacing is 2.2 per avatar), the camera frame, the walk back.

**Files for THJ to commit (steps 4c to 4e).** New (each with `.meta`): `Runtime/Simulation/HomeBarks.cs`, `Runtime/Presentation/HomeBarkDriver.cs`, `Editor/HomeSimulationTests.Barks.cs`, `Editor/HomeSimulationTests.Kevin.cs`, `Editor/HomeStep4ContentTool.cs`, `Content/Home/Barks/HomeBarks.csv`, the Kevin avatar assets in `Content/Home/Presentation/Avatars` (`HouseAvatar_Kevin.prefab`, `AC_HouseAvatar_Kevin.controller`, `Kevin_Idle.anim`, `Kevin_Run.anim`). The `Features/NPCs/Kevin/Move` and `Stand` folders are untracked art: commit them too. Modified: `Runtime/Definitions/HomeCycleDefinition.cs`, `Runtime/Simulation/HomeSimulation.cs`, `HomeSimulation.Family.cs`, `Runtime/Presentation/HomeHouseLayout.cs`, `HomeHouseView.cs`, `HomeSendOffWindow.cs`, `HomeStationWindow.Tasks.cs`, `Editor/HomeDemoContentBuilder.cs`, `HomeHouseBuilder.cs`, `HomeIdleDirectorBuilder.cs`, `HomeSimulationTests.Presentation.cs`, the demo content assets (`HomeCycle_Demo.asset`, `Station_Homestead/Kitchen/Porch/Hearth.asset`), `HomeIdleCatalog.asset`, the Home scene.

### M9 Step 4e addendum: replacement candidate for the Send-off scene (Oct 6)

Decision (THJ): keep the Send-off as built (the family who stay home walk to the Door, `JohnGate` plays when John goes). **Candidate to replace it later: the idle `ToMountain`** (state "HIE - ToTheMountainGodHalls", `MortaStory/Content/Story/HomeIdles`): a family farewell scene with John, Mark, Lucy, Mary, Linda, Ben, Kevin and Joey (scenery), plus Left and Right Furniture props. It plays in the hall (area -3.7, -4.95, 5.3 x 2.75), about 7 units north of the Door anchor, not at the door. Keep it where it was authored: moving it would take the furniture props with it.

- **How to wire it (not done):** a new `HomeIdleContext.SendOff` in `HomeIdlePlanner`, considered while `HomeHouseLayout.SendOffOpen` is true; claim everyone in the cast whatever their status (the Wounded and the squad included: the squad is who is being seen off), so their avatars hide while it plays; one catalog rule (`ToMountain`, key empty); one test. The `JohnGate` rule and the walking gathering stay as the fallback.
- **Other candidates checked:** `MoreFire` (a campfire gathering outside, south of the door at -3.9, -22.7, not a farewell), `CorruptionGate2` (Linda and Lucy at the gate) and `JohnGate` (John alone): too small or off-theme. `John_Leaving_sequence` stays unbuilt (no runtime cutscene player; see 4e).

### M9 Step 4: fixes after the first Play look (Oct 6)

- **Barks seemed absent.** Cause found by reading the driver: it only heard phase changes after it started watching, so the Dawn plan already running on entering Play (or after a load) produced no `dawn` bark; the next lines came only from new seats, results, or 45 s of quiet. Fixed: on start it also queues the barks of the phase already running. Barks do not play in the prologue, while a window is open, during a time-lapse, or less than 5 s after the last line. New inspector switch **Log Barks** (on) on the Bark Driver prints every bark, or "no line" with the reason, to the Console (`[Home barks]`).
- **Linda shown twice, Kevin badly placed (reported from Play).** Added **Log Changes** (on) on the Idle Director: each plan change prints the idle, who it shows, and each avatar as hidden / shown / walking with its anchor (`[Home idles]`). The duplicate is not yet explained: send the Console lines for that moment (day, phase). Kevin's spot is a guess (`Anchor - spot-Kevin` under Room Anchors, 16.5, 1.3): nudge it in the Scene view; the builder never moves an anchor it did not place at the old defaults.
- **Homestead has 3 seats.** Base content, not an upgrade: 2 + the chore seat added for Kevin (Kitchen 2 = 1 + 1). They are ordinary Helper seats, so the fighters can use them too. Option if you want Kevin's seats to be his alone: a separate "Chore" seat role that only he can take (small change in `CheckSeat` and the content tool).

## Step L: third merge of origin/main into thj/home-test (Oct 11)

**Built.** Fetched `origin` (`origin/main` at `709714961`, 113 commits since Step K's merge-base `ead061cb2`; the branch had 36). Merged into `thj/home-test`: merge commit `5c8476822`. A dry run (`git merge-tree`) first showed 7 conflicts, none a real disagreement of intent except the faction asset:

- `Unit_Toba`, `Unit_John`, `Unit_Linda`, `Unit_Lucy`: the same adjacent-line pattern as Step K (the branch's Stat\_FP overrides next to lines main added). Kept both sides. Each prefab now differs from main only by the three Stat\_FP overrides (additive policy, `baseFactor` 0, level-0 factor 0), plus Toba's `attributeSet [3] factorReadMode`. `Unit_Mark` merged cleanly.
- `MX - Another Sanctuary.asset`: kept the branch's `completionSequence` (THJ's call; main's new guid dropped). `homeState: {fileID: 0}` stays.
- `LucyFactionRoleHandler.cs`: took main's version. It has its own no-enemy-faction guard (`enemyFactions.Length <= 0`), so the Home M6 safe-room guard is no longer needed there.
- `BergsonsFaction.asset`: in the 5 conflicting blocks kept the branch's values (1.02-step upgrade levels, Stat\_FP 3/4/5/6); main's gold-cost retune (Oct 6, `0ccfd8b0a`) applied elsewhere. The "Home" additional stat source is intact. Result: gold costs are mixed (e.g. Stat\_FP levels 4 and 5 cost 10 / 15 from the branch, level 6 costs 50 from main). A consistency pass over the costs is open.

**Verified.** Edit-mode tests from the command line (Unity 6000.3.4f1, editor closed): 354 run, 353 pass, 1 fail; the failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, as expected. No compile errors in the log. Main added 5 test files (`TagBasedExtraModTests`, `CombatLogTests`, `CombatLogRichTextTests`, `StatAttributeSetLevelTests`, `WrathStacksTests`). Expected state in CLAUDE.md is now 354 / 353.

**Not verified in Play (batched).** Main's `GameHandler` now calls `faction.StatAttributes?.ResetUpgradeLevels()` at startup and after Clear Save Data; it resets the main set only, so check that the "Home" layer and the "faction stat resets on new cycle" item still behave (and `HomeState.Recreate(discardSaved: true)` next to it). Main's `GUnit` phase tick rewrite and the per-level `EnemyTier` (reads EnemyFaction Stat\_HP / Stat\_DMG levels) against the Home Omen / Send-off / Dungeon appliers on a Warren sortie. Lucy's faction role with main's new range check. Each hero's skill tree and Dining Table Tier 2 (+1 FP via the "Home" source). Lucy + John shield relay in a sortie from Home. `pointConsumptionMode` should still be 0 (FTP).

**Findings.** (a) Unity re-dirtied `TextMesh Pro/.../LiberationSans SDF - Fallback.asset` during the test run (dynamic glyph noise, not part of the merge, not committed). (b) `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset` still carry THJ's uncommitted changes, left in place on THJ's instruction. (c) MERGE-BRIEF.md is out of date and was not used.

**Step L status.** Merged and committed (`5c8476822`), not pushed. Next: the batched play-through, then the gold-cost consistency pass on `BergsonsFaction.asset`.

## M9 Step 5c: "From Home" in combat (Oct 11)

**Built.**

- `HomeFromHomeSummary` (pure, `Runtime/Simulation`): the lines for a level, in the order Meal, Omen, Wounded, Ration. An Omen with a combat effect that is not revealed reads "Unknown Omen in effect" (once, however many are in play); a revealed one shows its name and effect text. Wounded shows the names and the cycle's HP factor ("Starts at 50% HP."). Placeholders are stripped with `HomeText.Display`.
- `HomeFromHomeTags` (`Runtime/Combat`): at level start builds the lines, puts a persistent display-only GTag on the affected units (Home.Meal on the squad, Home.Wounded on the Wounded, Home.Ration on the squad, Home.Omen on enemies), and records the dish whose Specs\_AP pool modifier gives the turn-1 surplus AP (`BonusApSource`, `BonusApIcon`). Missing tags log one warning and nothing breaks.
- `HomeFromHomeBanner` (`Runtime/Presentation`): self-building overlay (sorting 21) shown once the HUD is up; hides after 7 s or on the first click. Nothing is shown when Home gave nothing.
- Turn-1 AP pip: `UnitAPIndicator` marks the top full pip above the unit's default AP with the dish icon (a gold placeholder tint until dishes have icons) and "\<dish> +N AP" on hover.
- Editor tool `Tools/Home/Add Combat Tags`: adds Home.Meal / Wounded / Ration / Omen to `Resources/Tags/GTagSet.asset` (idempotent, showInGame on). **Run it once**, or no tags show (the log warns).
- Core edits (approved): `CombatLevelRunHandler` (+2 lines: `OnPrepareEnemies` after the Omen applier, `Banner.Show()` after `ShowHUD`), `FactionTracker.PrepareLevel` (+1 line, before the dungeon applier, which clears the pending rations), `UnitAPIndicator` (+49, additive), `PlayModeStaticReset` (+2 hooks).

**Verified.** 9 new tests in `HomeSimulationTests.FromHome.cs`. **Not run yet**: the editor is open, so the command line cannot run; run EditMode in the Test Runner. Expected 363 run, 362 pass if all compile and pass (only the AI baseline red).

**Not verified (Play, batched).** Add Combat Tags first. Then: a Home sortie with a send-off meal (banner, Home.Meal tag, AP pip on the unit with the dish, hover text), an Omen night (revealed and not), a dungeon with a Wounded member and a ration (banner lines, tags), a non-Home mission (no banner, no pip). Check the banner position against the objectives panel, that a click dismisses it, and that the pip clears after the AP is spent. A Revenge surplus on a non-Home mission must not show the pip.

**Findings.** Placing the tag hook before the dungeon applier was needed to read `pendingRations`. The pip is detected as available AP above `InitialValue`, so a surplus from another source during a Home dish would be labelled with the dish.

**Files to commit (with .meta).** New: `HomeFromHomeSummary.cs`, `HomeFromHomeTags.cs`, `HomeFromHomeBanner.cs`, `HomeCombatTagsTool.cs`, `HomeSimulationTests.FromHome.cs`. Modified: the four Core files above and, after running the tool, `Resources/Tags/GTagSet.asset`.

**Status.** Built, not compiled or tested yet. Next: 5a (headlines and traces).

## M9 Step 5a: Dusk headline cards (Oct 11) - traces NOT built, waiting for THJ

**Built.**

- `HomeHeadlineKind` and `HomeReportEntry.headline` (default None, so old saves are fine). The sim flags: recipe discovered (Experiment), mission revealed (RevealMissionOutcome), thread cut (Dusk dinner), weapon delivered (Dawn Workshop), Home upgrade active (Dawn), Bond level-up. `HomeOutcomeContext.Report` now returns the entry.
- `HomeHeadlines.Build` (pure): ordered Thread, Mission, Upgrade, Weapon, Recipe, Bond; stable within a kind; one card per subject; speaker is the character in the entry, else a default (Linda thread, John mission, Ben weapon and upgrade, Mary recipe). Spoken lines are `[PLACEHOLDER]` text (stripped on screen).
- `HomeSimulation.Headlines / PendingHeadline / AckHeadline` and two save fields (`headlinesDay`, `headlinesSeen`): cards are shown at Dusk only, acknowledged per day, so a reload does not replay them.
- `HomeDayHUD.Headlines.cs`: a full card (speaker portrait for fighters, line, what happened, "Next (n more)" / "Continue") built at runtime, drawn above the Dining Table, Bond scene and Picnic cards, which wait behind it. No scene change needed.
- 8 tests in `HomeSimulationTests.Headlines.cs`. Expected suite: 371 run, 370 pass (not run yet).

**Not built: traces in the house** (pantry shelf, weapon rack, plot growth, open book). They need world objects at anchors that do not exist yet, i.e. scene edits through the idempotent builders. Proposal sent to THJ in chat.

**Not verified (Play).** Dusk after a day with an Experiment discovery, a delivered order or a cut thread: cards one at a time, in order, then the Dining Table. Reload at Dusk after the first card: it must not replay. Check the card does not overlap the Picnic card at Dusk.

**Findings.** "Skill point earned" has no report entry yet (Faction SP comes from the skill-tree side), so it is not a headline; it belongs with 5d's SP badges. Bond level-up headlines fire per level, so one big claim can queue several cards for a pair.

**Files to commit (with .meta).** New: `HomeHeadlines.cs`, `HomeDayHUD.Headlines.cs`, `HomeSimulationTests.Headlines.cs`. Modified: `HomeDayReport.cs`, `HomeSaveData.cs`, `FoodResolvers.cs`, `HomeSimulation.Dungeon.cs`, `.Family.cs`, `.Knowledge.cs`, `HomeResolveContext.cs`, `HomeOutcome.cs`, `HomeDayHUD.cs`, `HomeDayHUD.Prologue.cs`.

### M9 Step 5a (traces): the house shows what the family did (Oct 11)

**Built.**

- `HomeTraces.Compute(sim)` (pure): one dish per pantry portion, upgraded workshop weapons (level > 0), each garden plot's stage (Empty, Sprout, Growing, Ripe, from `daysLeft` against the crop's `growDays`), and the study item on the desk.
- `HomeTraceView` (scene component, redraws twice a second and only when something changed): dishes on a 6-column shelf grid, weapons in a row on the rack, a plant that grows per plot, an open page on the desk. Placeholder art: a dish or weapon uses its icon when it has one, else a coloured square. Hidden in the prologue. Sorting layer "Default", order 90 (fields on the component; avatars are at 100).
- Editor `Tools/Home/Build House Traces` (Play off; run after Build Station Props): creates "House Traces" with the view and 9 anchors (pantry shelf next to the Kitchen prop, rack by the Workshop, book by the Study, 6 plots by the Homestead). Idempotent; an anchor that exists is never moved, so nudge them in the Scene view. The positions are guesses relative to each prop's indicator.
- 5 tests in `HomeSimulationTests.Traces.cs`. Expected suite: 376 run, 375 pass.

**Not verified (THJ checks in Play).** Run the builder, then look at each anchor in the Scene view and nudge it onto the shelf, rack, desk and garden. Check sorting (traces behind the avatars but in front of the room art; change the order on the component if not), the pantry growing after a Kitchen batch, a plant growing and ripening, the rack after a delivered order, and the book appearing when an item is put on the desk.

**Hand edits.** None by me. The scene is changed by the builder only (Home scene: new "House Traces" object).

**Files to commit (with .meta).** New: `HomeTraces.cs`, `HomeTraceView.cs`, `HomeTraceBuilder.cs`, `HomeSimulationTests.Traces.cs`. Modified: `PlayModeStaticReset.cs`, the Home scene.

## M9 Step 5b: before to after on a person, and the Family sheet (Oct 12)

**Built.**

- `HomeStatBreakdown` (pure, `Runtime/Simulation`): folds a base value through the stat sources one at a time and keeps what each did. Headlines read "HP 32 → 38" or "Damage +10%" (percents formatted by hand); the breakdown line reads "Lessons +3, House +7". Source names for players: Unit = Hero, Equipment = Weapon, Faction = Lessons, Home = House, SkillTree = Skill tree.
- `HomeStatSheet` (`Runtime/Presentation`): feeds it the real sources of a hero's unit prefab, in the combat code's own order (`StatResolver.Resolve`: profile order, Equipment after Unit, Home layer added; folded in reverse). Rows: max HP (base from the health attribute's max bound), Damage (base 1), Crit and Evade (base 0). It prepares the prefab once per Play session with `InitializePartially`, the same call the Home upgrade panels make, inside a try/catch (a failure logs one warning and shows no sheet). Nothing in `Core/` changed.
- Roster strip (`HomeStationDock`): each fighter's card shows an HP line ("HP 32 → 38"); hovering the portrait opens the Family sheet (`HomeFamilySheet`): the four rows with the per-source breakdown. The dock redraws when an HP line changes, and closes the sheet before a rebuild.
- Upgrade headline (5a): the Dusk card for a house upgrade now adds "John 32 → 38 HP, Linda 20 → 24 HP" (the heroes the House source changed; "before" is the value without the House source).
- 6 tests in `HomeSimulationTests.StatSheet.cs` (Kitchen T2 alone 32 → 38; Lessons only 32 → 35; both 32 → 42 with "Lessons +3, House +7"; percent rows; unchanged stat; labels). Expected suite: 382 run, 381 pass (not run yet).

**Not verified (Play).** The numbers against combat: with Kitchen T2 John must read 32 → 38 in the sheet and have 38 HP in a fight; with 5 Toughness points 35; both 42. Check the sheet hover opens and closes cleanly, does not stay after the roster redraws, and that the roster card HP line follows a Yard Lesson at Dusk. Check no errors in the Console from `InitializePartially` on the prefabs when the Home scene starts (the first hover or dock draw calls it for each hero).

**Findings.** The sheet shows max HP, Damage, Crit and Evade only; FP (Dining Table T2) is a faction value, not a hero stat, so it is not a row. Damage is the stat factor (x1.10 reads +10%), not a damage number: abilities have their own bases. Rounding: each source's share is rounded separately, so a part can differ by 1 from the headline's exact sum; the headline is always the true total.

**Files to commit (with .meta).** New: `HomeStatBreakdown.cs`, `HomeStatSheet.cs`, `HomeFamilySheet.cs`, `HomeSimulationTests.StatSheet.cs`. Modified: `HomeStationDock.cs`, `HomeDayHUD.Headlines.cs`, `PlayModeStaticReset.cs`.

## M9 Step 5d: skill points, the route to the trees, the squad's return (Oct 12)

**Built.**

- **Real SP count.** `HomeRoster.UnspentSkillPoints` now asks `HomeRoster.SkillPointSource` (a delegate, so the sim stays pure; tests install a fake). `HomeSkillPoints` (Presentation) installs itself at Play start and reads a hero's points from their unit prefab the way the skill-tree panel does (`GetCollectedResourceAmount` of `GlobalSettings.sPResource`, prefab prepared once with `InitializePartially`, shared with the Family sheet). Cached for 0.25 s per hero because the house view asks every frame; cleared when the tree panel closes.
- **Badges.** Portrait: the roster card's "SP n" (it was dead code returning -1) now shows. Avatar: a blue "SP n" chip on the bubble over the character, next to the day's slots, and alone at Dusk; clicking it opens the trees. The house signature includes the counts, so the chip follows spending.
- **Route to the trees.** The toolbar button "Upgrades" is now "House Upgrades" (the Home Upgrades panel, unchanged) and a new "Skill Trees (n SP)" button opens the existing skill-tree panel (`HomeDayHUD.OpenSkillTrees`, the same call the Picnic uses; the HUD hides while it is open and comes back on close).
- **The Dining Table announces.** New headline kind `SkillPoint` (after mission-revealed, before upgrades): at Dusk, a fighter whose unspent count went up since the table last spoke gets a card, spoken by them ("John has 2 skill points to spend"). New save list `skillPointsSeen` ("Name=count"). Silent when the count is unknown or only went down (spending).
- **The squad's return at Dusk.** `HomeHouseView`: on the first Arrange at Dusk of a day with a sortie, the squad appears at the Door and walks in to the table; the sortie's rewards (the report's Outcome lines, at most 4) rise over them one after another (`HomeGainPop`, "Loot"). `HomeReportOrder.ResultsFirst`: the Dining Table card now lists Sortie, Outcome and Wounded lines first (gold), then the rest, and when it has to cut lines it drops the oldest others, never the results.
- 6 new tests in `HomeSimulationTests.SkillPoints.cs`. Expected suite: 388 run, 387 pass (not run yet).

**Not built / differs from the design.**

- The loot rises as pops at the Door; it does not fly into the stores bar. Doing that needs the pop to travel to the resource bar's icons on screen (HomeResourceBar positions), which I did not guess at.
- No SP badge on a "room": there is no personal room in the house; the chip on the avatar, the roster portrait and the toolbar button are the three routes.
- The tree panel opens on its first hero; it has no call to preselect one, so the badge on a specific hero cannot jump to that hero's tree (a Core change to `AbilityUpgradePanelUI`, not made).
- The walk-in plays once per Home scene load per day, so reloading a save at Dusk replays it.

**Not verified (Play, batched).** Earn SP in a sortie and return: the squad should walk in from the Door, the loot lines rise, the Dusk table shows the sortie lines first, an SP headline card comes up per hero with new points, then the usual table. SP chip on the bubble and the roster card; clicking either, and "Skill Trees (n SP)", opens the tree; spend a point and the badges drop after closing. Check the toolbar fits two buttons and the HUD returns after the tree closes. Check `InitializePartially` raises no errors in the Console for each hero.

**Files to commit (with .meta).** New: `HomeSkillPoints.cs`, `HomeReportOrder.cs`, `HomeSimulationTests.SkillPoints.cs`. Modified: `HomeRoster.cs`, `HomeStatSheet.cs`, `HomeHouseLayout.cs`, `HomeBubble.cs`, `HomeHouseView.cs`, `HomeStationDock.cs`, `HomeDayHUD.Family.cs`, `HomeDayHUD.Knowledge.cs`, `HomeDayReport.cs`, `HomeHeadlines.cs`, `HomeSimulation.Family.cs`, `HomeSaveData.cs`.

## M9 Step 6a: Linda–Toba lock and Bond start values (2026-10-12)

**Built**

- `HomeRules.showcaseStartBond` is now 18 (was 5) and new `newcomerStartBond` = 6. `HomeCycleDefinition.newcomer` (GUnit) with `newcomerKeyOverride` for tests and `NewcomerKey`.
- `HomeSimulation.StartCycle`: every pair of the newcomer (Toba) starts at 6, the showcase pair after that at 18, everyone else at 10.
- `HomeDemoContentBuilder`: showcase pair is Linda–Toba, newcomer Toba, rules set explicitly (old asset kept 5). The stale `BondScene_TobaMark_L2/L3` assets are deleted and `BondScene_LindaToba_L2/L3` are generated (placeholder lines, ids/titles new). Run `Tools/Home/Build Demo Content` to regenerate.
- The duo flag follows the showcase pair, so it is now `duo:Linda+Toba` (nothing else changed in the sim).
- Tests: `HomeSimulationTests.BondLocks.cs` (4 new); existing Bond tests re-pointed from Toba–Mark to Linda–Toba and Toba's new start values (also the prologue start-state test).

**Not built / not verified**

- Compile and EditMode not run yet. Expected suite: 392 run, 391 pass (388 + 4) with only the AI baseline red.
- Nothing in combat reads the flag yet: `Linda_Toba_Duo` is still open from the start. That is 6b.
- Hand-edit: none. Existing saves keep their old Bond values; a new cycle uses the new ones.
- The Demo Spec needs: showcase pair Linda–Toba (about 18/25), Toba's other pairs about 6, Toba–Mark duo dropped.

**Files to commit:** HomeCycleDefinition.cs, HomeSimulation.cs, HomeDemoContentBuilder.cs, the BondScene assets after the rebuild, HomeSimulationTests.cs, .Prologue.cs, .BondLocks.cs.

## M9 Step 6b: Bond locks in combat (2026-10-12)

**Built**

- `HomeLockRules` (pure, `Runtime/Simulation`): the table of what opens at which Bond level. Linda–Toba duo, Sisters' Rivalry (Linda–Lucy) and Command Shield Dash (John–Mark) open at Bond Lv 2; Pass-By opens at Lv 1 for every pair (so only Toba's pairs earn it, they start at 6). Shifting everything a level up for the prologue is a change of these numbers.
- `HomeBondLocks` (`Runtime/Combat`): a plain static snapshot (open lock ids, Pass-By pairs) refreshed at level start from `HomeFromHomeTags.OnPrepareLevel`. It holds no Unity objects, so the AI worker thread may read it. No Home cycle, or an uninitialised Home state: the snapshot is null and everything is open (non-Home scenes and main behave as before). Hooked in `PlayModeStaticReset`.
- Independent scripts use the UnlockableRegistry, as the other passives do: `HomeBondLocks.Sync...` turns the literals `Home_SistersRivalry` and `Home_CommandShieldDash` on or off in the player's `FactionTracker` from the Bond level, so a new moon cycle re-locks them. The skill-tree literals are untouched.
- `Tools/Home/Add Bond Locks` (`HomeBondLocksTool`, idempotent): creates `Resources/Unlockables/HomeUnlockableSet.asset` (group "Home", both `unlockedByDefault` off), adds it to the registry and sets the new `homeLock` field on the Linda, Lucy and John prefabs.
- Dining Table: a Bond level-up that reaches a lock adds "A & B: \<ability> now works in combat" (the Linda–Toba duo keeps its existing line).

**Core / Features edits (approved in chat)**

- `FactionTracker.SetLiteralUnlocked(string, bool)`: sets or removes one meta literal.
- `UnitsCooperationHandler.SquadAllowsTrigger`: `DuoOpen(entry.iD)` (so `RuntimeAbility.Available` honours it).
- `UnitsPassByHandler.CanPassBy`: `PassByOpen(moving, onTile)` (also covers the hover preview).
- `UnitKillAbilityPointProvider` (Sisters' Rivalry) and `JohnPassiveAbility_CommandShieldDash`: new `homeLock` UnlockableReference field and an early return when it is set and not unlocked. Empty = always on.

**Tests:** 6 new in `HomeSimulationTests.CombatLocks.cs`. Expected suite: 398 run, 397 pass (392 after 6a, not run yet).

**Before Play:** compile, run `Tools/Home/Add Bond Locks`, then leave and re-enter Play mode (the registry builds its id map when the asset loads, so a lookup of the new ids right after the tool run may need a fresh load).

**Not verified (Play):** with Linda–Lucy below Bond Lv 2 a kill gives no AP or ready attack; above it, it does. Same for John's Shield Dash after Mark's Command (John–Mark Lv 2), the Linda–Toba duo trigger (Lv 2) and Pass-By with Toba (Lv 1). A new cycle locks them again. Check the combat log's Synergy lines.

**Known limits:** the unlockables sync at level start only; a Home screen reading them later (previews, the Guide) uses `HomeLockRules` and the Bond level directly. The Linda–Toba duo still also needs the Family Skill Point as before, if the tree requires it.

**Files to commit:** HomeLockRules.cs, HomeBondLocks.cs, HomeBondLocksTool.cs, HomeSimulationTests.CombatLocks.cs, HomeFromHomeTags.cs, HomeSimulation.Family.cs, PlayModeStaticReset.cs, FactionTracker.cs, UnitsCooperationHandler.cs, UnitsPassByHandler.cs, UnitKillAbilityPointProvider.cs, JohnPassiveAbility\_CommandShieldDash.cs, plus the HomeUnlockableSet asset, UnlockableRegistry.asset and the three prefabs after the tool run (with .meta).

## M9 Step 6c: Bond previews, night scenes, Fireside payoff state (2026-10-12)

**Built**

- `HomeBondPreview` (pure, `Runtime/Simulation`): the seat preview and the roster bars. `ForStation(sim, station)` runs the forecast fork for the open slot and lists the seated pairs' gains ("Linda & Toba  +5 Bond  22 → 27/45  → Lv 2: Linda & Toba's duo, a Bond scene"); `PairLines(sim, who)` gives "with Linda   18/25   Lv 2: ..." for each other fighter.
  - Station window: a "Bond" section at the bottom of the Task column (`HomeStationWindow.Tasks.cs`). Roster hover card (`HomeFamilySheet`): a "Bond" block under the stats. The Fireside Talk text now mentions the dawn scene and the payoff.
- Bond scenes earned in the Night slot are listed in `Data.nightScenes` and play at the next Dawn (`HomeSimulation.ScenesDueNow`: Dusk = all pending, Dawn = the night ones). The day-earned ones still wait for Dusk. The Dining Table HUD now shows `ScenesDueNow`. The report line says "plays at dawn" for night scenes. Any Night level-up counts (Fireside, Stargaze, Vigil), not only the Fireside.
- Fireside payoff (state only): the Hearth resolver grants the sitting pair `Data.firesidePairs` ("A+B", once per pair, report line "their first duo or Family Role together next mission costs 1 less FP"). At departure (`SendOff`) the pairs with both members in the squad move to `sortie.payoffPairs` (the others keep waiting), report line "The Fireside carries on". `sortie.payoffUsed` is ready for the combat side.
- New save fields (default empty): `nightScenes`, `firesidePairs`, `sortie.payoffPairs`, `sortie.payoffUsed`.

**Not built: the combat discount.** It needs a Core edit where FP is charged (duos in `CooperationEntry`, Family Roles in `FactionControllerBase`/`PlayerController`); waiting for THJ's answer on the open questions in chat.

**Tests:** 8 new in `HomeSimulationTests.Fireside.cs` (payoff once, lone seat, armed only for squad pairs, night vs day scene timing, seat preview, roster bars). Expected suite: 406 run, 405 pass (398 after 6b, not run yet).

**Not verified (Play):** the Bond section in the Porch and Fireside windows while seating a pair; the roster hover; a night level-up shows its scene card at the next Dawn (and not at Dusk); a day level-up still at Dusk; the time button at Dawn is not blocked by it.

**Files to commit:** HomeBondPreview.cs, HomeSimulation.Fireside.cs, HomeSimulationTests.Fireside.cs, HomeSaveData.cs, HomeSimulation.cs, HomeSimulation.Family.cs, NightResolvers.cs, HomeDayHUD.Family.cs, HomeStationWindow.Tasks.cs, HomeFamilySheet.cs.

### M9 Step 6c addendum: the Fireside payoff in combat (2026-10-12)

Decided with THJ: the payoff is one of three, picked per pair; free rather than "1 less"; a Family Role counts when either member uses it; the FP-cap option needs both in the squad (every payoff does: it is armed only for pairs fully in the squad).

- **The three kinds** (`HomeFiresideKind`): DuoFree (the pair's first duo costs 0 FP), RoleFree (the first Family Role either member uses costs 0), FpCap (+`HomeRules.firesideFpCapBonus` = 2 max FP for the mission). `HomeFiresideRules.Pick(day, a, b)` is a stable FNV hash, so the same save always rolls the same kind (the sim has no randomness). Stored as `"Linda+Toba=DuoFree"` in `firesidePairs`, then `sortie.payoffPairs` / `payoffUsed`.
- `HomeFiresidePayoff` (`Runtime/Combat`): an immutable snapshot (AI-thread safe) rebuilt at level start from the sortie; `DuoCost`, `RoleCost` return 0 for an unspent payoff; `SpendDuo` / `SpendRole` record it in `payoffUsed` (survives levels and reloads); `OnEnterMission` applies the FpCap through the existing `FamilyTimePoints.AddMaxBonus`, once. Hooked in `HomeFromHomeTags.OnPrepareLevel`, `HomeSendOffApplier.OnEnterMission`, `PlayModeStaticReset`.
- **Core edits (approved in chat):**
  - `UnitsCooperationHandler.CooperationEntry`: new private `FpCostFor(activator)` used by `Available` and the charge, and `SpendDuo(...)` after the charge. On this branch the duo charge is taken from each partner's `PointConsumer` (the shared FTP pool, so twice); a free duo costs 0 on both.
  - `AbilityOrchestrator.FactionRoleRequiredFTP` now goes through `RoleCost` (all four read sites, and the cost label, follow).
  - `FactionControllerBase.ActivateFactionRole`: `SpendRole(unit.Nickname)` after the charge (player faction only). The ATB-only Reactive Interrupt charge (PlayerController `ConsumeActionCost`) does not spend it; that mode is off on this branch.
- Design docs updated: the payoff rule, the decided extra locks, and a new open question in the doc and the brief: **what else can be rewarded here** (examples: Dom heals that person more during the next sortie; John takes less damage during his Family Role for that person).
- Tests: 10 in `HomeSimulationTests.Fireside.cs` now (the payoff rules and cost reads added). Expected suite: 408 run, 407 pass (398 after 6b, not run yet).
- Not verified (Play): sit a pair at the Fireside, send them on a sortie together, check the Dining Table/report line, then in combat: DuoFree = their duo shows 0 FP and works at 0 FP, only the first time; RoleFree = the first Family Role by either is free; FpCap = the FP bar is 2 higher from level 1. The From Home banner does not list the Fireside payoff yet (not requested; easy to add as a line kind).
- Extra files to commit: HomeFiresideRules.cs, HomeFiresidePayoff.cs, HomeCycleDefinition.cs (new rule field), UnitsCooperationHandler.cs, AbilityOrchestrator.cs, FactionControllerBase.cs, HomeSendOffApplier.cs, HomeFromHomeTags.cs, PlayModeStaticReset.cs.

### M9 Step 6c fix: an interrupted sortie hands the Fireside payoff back (2026-10-13)

Found in play: after the Masher Goblin error (see below) Play was stopped; on the next run `HomeSimulation.RollBackSortie` cleared the sortie state, which also held the armed Fireside payoff, so the pair lost it. `RollBackSortie` now calls `RefundFiresidePayoff()` (`HomeSimulation.Fireside.cs`): every payoff the sortie carried, spent or not, goes back to `Data.firesidePairs` (one per pair), and the retry arms it again, unspent. Lifetime otherwise: spent when used (FpCap at mission start, first duo when paid, first Family Role when used); unspent ones end with the sortie; not carried to a later sortie. Test: `Fireside_AnInterruptedSortie_HandsThePayoffBack_SpentOrNot` (11 tests in `HomeSimulationTests.Fireside.cs`; expected suite 409 run, 408 pass).

Also in this session: a combat NullReference every phase tick when a Masher Goblin is in the level. Cause is on `main` (commit 6d42d337e made `FactionRoleHandlerBase.PhaseTick` tick `ability`; `MasherGoblinFactionRoleHandler` overrides `Initialize` without the base, so `ability` is never initialized). Fixed in `FactionRoleHandlerBase.cs` (`_abilitiesInitialized` flag, `CanTickAbility()` with a one-time warning); the lines were handed to THJ to put on `main`. Expect one yellow warning per Masher per combat.

## M9 Step 6d-1: staged station unlocks and introductions (2026-10-13)

**Built**

- Data (`Runtime/Definitions/HomeStationUnlock.cs`, `HomeCycleDefinition`): `stagedUnlocks` (bool, **the off switch**: false = everything open from Day 1, no introductions, nothing forced), `stationSchedule` (station + trigger Day / Night / FirstWounded + day) and `stationIntros` (station, speaker, lines, `actionHint`, `forced`). Stations that are not scheduled open as soon as the prologue ends.
- Save (`HomeSaveData`, all default empty/false, so old saves behave as before): `stagedUnlocks`, `everWounded`, `introQueue` (opened, not yet introduced), `introActive` (introduced, first action pending), `introDone`. An empty `unlockedStations` still means "all open" for old saves and presets; staging applies only to a game that ran the prologue on a staged cycle (`FinishPrologue` -> `BeginStagedUnlocks`).
- `HomeSimulation.Schedule.cs`: `RefreshStationSchedule` (called from `Enter` at DawnPlan, Dusk and NightPlan) opens due stations, writes "X is open" and queues the introduction; `PendingIntro`, `AckIntro`, `IsIntroDone` / `SyncIntroDone` (the action is recorded while the seats still exist, at slot resolve), `BlockingIntro` (a forced action not yet done, only while it can be done now: day seats at Dawn/Noon, night seats at night, never a dead end), `IsGuideUnlocked` (scheduled stations need their introduction).
  - First actions: Study = something on the desk or a study seat; Workshop = an order or the room opened; Yard, Care, Vigil, Stargaze, Fireside = a seat at the station.
- Presentation: `HomeTimeRules` disables the time button with "\<speaker> is waiting for you: \<hint>." while an intro blocks; `HomeRoomDim` also veils closed staged rooms; `HomeIntroDirector` (driven every frame from `HomeDayHUD.Update`, waits for a quiet moment: input phase, no modal/time-lapse/headline/scene/picnic card) plays the owner's lines in a `HomeSpeech` balloon over their figure (toast if they have none, e.g. Ben and Mary), outlines the prop, advances on click or after 5 s, then `AckIntro` and a toast with the first-action hint.
- `HomeDemoContentBuilder`: schedule Study and Workshop Day 1, Yard Day 2, Stargaze and Fireside at Night 1, Care and Vigil at the first Wounded. Introductions (placeholder lines): Linda (Study, forced), Ben (Workshop), John (Yard, forced), Mark (Stargaze), Mary (Fireside), Toba (Care, forced). Vigil has none (opens silently with Care). Run `Tools/Home/Build Demo Content` to write them to the cycle asset.
- Hook: `PlayModeStaticReset` -> `HomeIntroDirector`.

**Tests:** 8 new in `HomeSimulationTests.Schedule.cs` (staging off = old behaviour; closed after the prologue with the owner queued; Day 2 / first night / first Wounded triggers; Ack opens the Guide and a forced action blocks until done and is recorded; an unforced one never blocks; never blocks where it cannot be done; save and reload; Guide availability). Expected suite: 417 run, 416 pass (409 before, not run yet).

**Not built:** the Home Guide pages and panel (6d-2). The Guide check `IsGuideUnlocked` is ready for it.

**Not verified (Play):** new game: after the prologue Day 1 Dawn shows the Study and Workshop open and the others veiled; Linda's balloon then Ben's toast; Day 2 Dawn: John's Yard intro, the time button is held until a lesson is seated; first night: Mark and Mary; first Wounded: Toba and Care. The veil on the Yard, Care, roof and hearth rooms lifts when they open. Set `stagedUnlocks` off on the cycle (or rebuild with it false) to confirm the old all-open behaviour.

**Files to commit:** HomeStationUnlock.cs, HomeSimulation.Schedule.cs, HomeIntroDirector.cs, HomeSimulationTests.Schedule.cs, HomeCycleDefinition.cs, HomeSaveData.cs, HomeSimulation.cs, HomeSimulation.Prologue.cs, HomeTimeRules.cs, HomeRoomDim.cs, HomeDayHUD.cs, HomeDemoContentBuilder.cs, PlayModeStaticReset.cs.

## M9 Step 6d-2: the Home Guide (2026-10-13)

**Built**

- `HomeGuide` (pure, `Runtime/Simulation/HomeGuide.cs`): `PageFor(sim, station)` builds a page from the station's kind, the cycle's rules (Porch Bond, Care Bond, Hearth Bond, Stargaze Bond, the Yard Student bonus level) and its affinities ("Good at this": `Toba: the Wounded recover right after the slot`, `Toba: double Bond from caring`, ...), plus an "Opens" line from the schedule ("Open from the start." / "Opens at Dawn on Day 2." / "Opens on the first night." / "Opens when someone is first Wounded."). `Pages(sim)` lists the pages `sim.IsGuideUnlocked` allows: stations that are open and, for scheduled ones with an introduction, introduced by their owner.
- `HomeDayHUD.Guide.cs`: a "Home Guide" button on the top-right toolbar (under House Upgrades and Skill Trees) opens a centre panel: a grid of page buttons (5 per row) and the page text. `HomeDayHUD.OpenGuide(stationId)` opens it at a page. Hidden with the other toolbar panels.
- `HomeStationWindow`: a "?" button beside the close button (added on first use, so a window baked into the scene earlier gets it too); greyed out when the page is not unlocked yet. It closes the window and opens the guide at that station.
- Tests: 3 new in `HomeSimulationTests.Schedule.cs` (which lists only readable pages; rules numbers and the "Opens" line; "Good at this" from affinities). With 6d-1, 11 tests in that file. Expected suite: 420 run, 419 pass (409 before 6d, not run yet).

**Not verified (Play):** the Guide button opens the panel with Kitchen, Homestead and Porch at the start; Study and Workshop appear after their owners have introduced them, the Yard after Day 2's introduction, and so on; the "?" in a station window jumps to its page; the panel fits above/next to the toolbar and closes with Close or the button.

**Limits:** page texts are plain placeholders-in-spirit (no `[PLACEHOLDER]` tag, written from the rules); the writers' pass can replace them. Pages are per station, not per room (Care and Vigil share a room but have separate pages).

**Files to commit (6d-2):** HomeGuide.cs, HomeDayHUD.Guide.cs, HomeDayHUD.Knowledge.cs, HomeStationWindow.cs, HomeSimulationTests.Schedule.cs.

## 2026-10-13 Playtest: Run 1 (Sim Debug, no combat; Part A steps 1-4)

Setup: Unity 6000.3.4f1, Play from PreloadScreen, Start Game, then New Cycle in Sim Debug (the save was on Day 5; no save reset). Setup tools run first, Play off: Build Demo Content, Add Combat Tags (already present), Build House Traces (0 new anchors), Add Bond Locks (registry ready). Played Day 1 to Day 2 by hand, then Run to next Dawn to Day 5. Driven by Claude with computer use; Console read from Editor.log. No exceptions logged in the session.

### Verified

- 1.2 Dead seats: Kevin refused in the Study ("Kevin only helps with the chores (Homestead or Kitchen, by day)"); lone Porch seat and lone Fireside seat allowed while planning, then released at slot start with "Needs a partner on the Porch" / "Needs a partner by the fire"; full pantry refuses a Kitchen helper ("Pantry full") and releases a carried-over helper at slot start; dock shows Kitchen "Blocked".
- 1.5 Carry-over release: Linda and Lucy released after finishing Old Map Fragment ("Nothing to read").
- 2.1 Calendar on Day 1: gourd (R) Day 2, stars nights 2-6, X on Day 3 (Scout Post last day), Q on Day 7, "+1" on Day 3 with three events; hover lists all. After planting on Day 2 the R moved to Day 4. Charted patterns drop off.
- 2.2 Today's moon larger with gold ring, past days dimmed, icons clear of the moons.
- 2.6 Warren: top centre of the map with "5 nights remain" on Day 2; its card shows the danger list (7 of 7 threads) and "Scouting run".
- 2.7 Scout Post card: "Supplies" and "Gone after tomorrow" on Day 2.
- 3.2 Badges: seat pips match; "Study 0/1", "Ripe tomorrow", "Ripe in 2 dawns", "Pantry 4/4 / Pantry full" match the windows.
- 3.3 Clicking the Great Moon never opened the room under it (about 10 clicks).
- 3.4 Dock: keys 2 and 3 open Homestead and Kitchen; dock buttons open their windows.
- 3.5 Roster drag: Toba onto Kitchen seats him ("Toba goes to the Kitchen."); Lucy onto Workshop is refused (wrong reason, see findings).
- 3.7 Recap strip: "Dawn to Noon", "Noon to Dusk", "Overnight" with gained / spent / progressed / unlocked; hides by itself; Recap tab reopens it; no "Last night" card.
- 3.8 Mary at the stove with a "Cook" tag on a cooking day.
- 4.1 Dawn: everyone starts in their bedroom (log); at night the unseated go to their rooms.
- 4.3 Dusk table: Pray on Days 1 and 2.
- 4.5 Kevin: Homestead accepted, Study refused with the reason; Free in the roster.
- 4.7 Names: "Porch Break" and "Fireside Talk", each with a "Costs:" line.

### Not verified

- 1.2 capped Teacher, lone stargazer with nothing to chart (every night so far had a pattern), Workshop with no order (already verified Oct 5); 1.3 Experiment risk marking; 1.6 Care / 1.7 Vigil (nobody Wounded without a sortie).
- 2.5 Queen's Might after a Goblin Camp win (needs combat: Run 3). Hover list itself reads right: 7 of 7, five lines plus "2 more things feed her".
- 2.4 Little Moon arc (it moves between slots; arc shape not judged).
- 3.1 glance test, 3.2 Badge Side, 3.3 diamond hover outline (not conclusive), 3.6 overview after a lapse with no window open, Ben at his bench (no order placed), lapse effects (not seen clearly).
- 4.2 no-wandering per character in full, 4.6 Send-off (needs a sortie), Kevin's side-view walk.
- Clouds on nights 4 and 6 after "Omen revealed: Red Veil" (only the revealed night may be meant to show).

### Findings

Blocker

- None.

Major

- **War council hidden (2.8).** At the Day 1 Dawn plan only the "War council" title strip shows; the body and the Next button sit under the roster/dock canvas. They become visible only while the morning lapses (dock hidden), and then the phase leaves DawnPlan so `NeedsWarCouncil` is false and the beat is lost for the cycle. Cause: `HomeDayHUD.BuildCouncil` anchors the card at bottom centre (y 36) on a canvas drawn under `HomeStationDock`. (Section B.)
- **Dawn card not seen (2.3).** Over four Dawns (by hand and with Run to next Dawn, screenshots every 0.5-1.5 s) no "N nights remain" card appeared. It is placed top centre (`HomeTimeHud.Goal`, y -40) where the Overnight recap strip opens at the same moment, and lasts 4 s; likely covered, possibly suppressed by `HomeTimeFlow.Busy`. The map's Warren countdown does show "5 nights remain". (B.)
- **No per-seat forecast on screen (1.4).** The seat cards and the moon's Begin tooltip list who sits where ("Morning: Study (Linda, Lucy)") but not the result ("+1 progress, finishes this slot"). Only the Kitchen badge forecasts. The forecast also missed a release: at Noon on Day 2 the tooltip and the Kitchen badge still promised "Afternoon: Kitchen (Toba)" / "Mary lets the helper cook this afternoon" with the pantry already 4/4; at slot start Toba was released ("Pantry full") and nothing was cooked. (D.)
- **"Bond only" never shown (1.2).** A second reader (Lucy) on a 1-slot item (Old Map Fragment, Linda already seated) is accepted with only the Bond preview; no "Bond only" in the window, the hover hint or the tooltip. `HomeSeatRules` returns `BondOnly`; no UI reads it. (D.)
- **World badges and bubbles draw over the Map Table (3.x / 2.6).** Station badges ("No one is Wounded", "Desk empty", "No order") and the "? ? SP" bubbles render on top of the map and on top of the mission card text; the Great Moon button covers the card title ("…in Scout Post"). (C.)
- **Station window X and ? ignore clicks (recurring Part 0 (i)).** Fireside and Homestead: X and ? did nothing over 4-5 clicks each (Study needed two). Escape never closes a window; it opens the pause menu behind it. Workaround: the Overview dock button closes the window. Possibly a raycast blocker over the window's top-right corner (the Home toolbar box ends just above the X). (C.)

Minor

- Calendar Day 1 badge is a blank yellow square ("The Great Moon in the sky tonight" has no letter).
- Mission card puts the description first and the purpose tag ("Supplies") after it; spec says purpose tag first. Warren card "Cuts:" line repeats the description ("The Goblin Queen's ritual completes on the full moon").
- Map labels "Weakens the Queen" for 101/102/103 overlap into one line.
- Drag refusal reason is wrong: Lucy onto Workshop says "Workshop has no free seat for Lucy (Morning)"; the real reason is "No order".
- Kevin is listed (blank white portrait) in every seat picker, including stations he can never take; the refusal line doubles the name ("Kevin: Kevin only helps…"). Kevin's roster portrait is blank too.
- Care badge text repeats itself ("No one is Wounded / No one is Wounded").
- Seat pickers do not dim a character already seated in that slot elsewhere (Linda and Lucy shown normally in the Porch morning seats while in the Study; Mark at Fireside while at Stargaze).
- Dining Table card shows raw log tags ("\[DawnTick\] Cycle started from preset 'Day 1 start'", "\[MorningResolve\]").
- Barks: wrong speaker ("assign:Porch(John): Linda: Come, John, sit with me." while Linda is in the Study); idle lines from seated characters; Lucy's idle "Are we going anywhere today?" at night; idle lines repeat every \~45 s (Lucy 4 times on Day 1) because the idle pool is small.
- Linda on screen twice at the Day 1 Dawn plan: `LindaInBed (shows Linda)` with `Linda=shown@bedroom-Linda` (recurs from Oct 5). Not seen at Night (avatar hidden correctly).
- 2.4: the Great Moon on Day 5 is a brighter cyan than Day 1, not redder.
- 3.6: after Dusk to Night the camera framed the Homestead side, not the house overview.
- Pantry traces are plain yellow squares under the kitchen (one per portion); white square particles over the yard at Dusk/Night. Placeholder art, noted only.
- Question for THJ: idle family on the Porch earn Bond ("John & Toba +1 (idle together)") while the Begin tooltip says "Wandering the house, no Bond" for others. Intended?

### Status

Run 1 partly done. Next: decide on the six Major findings (council layering, Dawn card, forecast display, Bond only, badges over the map, window X), then Run 2 (Day 7 route).

## 2026-10-13 Run 1 fixes (Home readability, after Playtest: Run 1)

### Built

- **War council above the dock.** `HomeDayHUD.Council` stands the card on top of the dock (`HomeStationDock.TopEdge` + 14) instead of behind it, and hides it while time is passing. New: `HomeStationDock.TopEdge`.
- **Dawn card visible.** `HomeTimeHud.Goal` moves the "N nights remain" card from the top centre (under the resource bar and the Dawn recap strip) to the upper middle of the screen (`DawnCardY` 150); hidden while a station window is open.
- **Forecast in words.** New pure `HomeForecastText` (Runtime/Simulation): `SeatLine` ("→ Linda, Lucy studied Old Map Fragment (1/1)", "Bond only: the work is already covered", "Stands up when the slot starts: Pantry full", "Does nothing: …"), `Results`, `Warnings`, `Reason`, `PlanKey`. Shown under every seated character in the station window (new partial `HomeStationWindow.Readability.cs`, one `HomeForecast.Run` per rebuild) and in the Great Moon's tooltip under the plan (new partial `HomeTimeHud.Forecast.cs`, recomputed only when `PlanKey` changes).
- **Bond only before seating.** `SeatCandidate.BondOnly` / `HomeSeatPlanner.IsBondOnly`; the candidate hover reads "Lucy: take this seat (Bond only: the work is already covered)".
- **Study Bond-only rule is order-aware** (`HomeSeatRules.Study`): of two readers on a one-slot item only the later one is Bond only (before, each counted the other, so both were). A probe seat counts as last. Acceptance is unchanged (Bond only was always allowed).
- **Nothing world-space over the Map Table.** New `HomeMapView.IsOpen` (static, reset hook added to `PlayModeStaticReset`). While the map is open: station badges and indicators hide (`HomeStationProp`), character bubbles hide (`HomeBubble`), the world moons hide (`HomeWorldMoons`), and the sky's Great and Little Moon hide (`HomeSkyView`, veil and stars stay).
- **Escape closes a station window** and no longer opens the pause menu behind it: the window holds the Pause flag of `PlayerInputController` while open and gives it back on close (`HoldPause`). Escape with no window still pauses.

### Verified

- EditMode: 425 tests, 424 pass, 1 fail = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red). New partial `HomeSimulationTests.Readability.cs` (5 tests): Reason parsing; second reader reads Bond only and the first reads its result; an afternoon helper stands up with "Pantry full" when the morning fills the pantry; PlanKey changes with the seats; candidates mark the second reader Bond only.
- Play (New Cycle, Day 1): the Dawn card shows "6 nights remain" with the moon; the War council shows above the dock, Next and "To work" work; Study seat cards show the forecast and "Bond only" on Lucy, the hover hint says Bond only; the moon tooltip lists "→ Linda, Lucy studied Old Map Fragment (1/1)" and "Lucy: Bond only"; Escape closes Kitchen with no pause menu; Escape with no window opens the pause menu; X closes Study, Kitchen and Homestead in one click; on the Map Table no badges, bubbles or moon over the map or the Scout Post card title.

### Not verified

- The Kitchen "Pantry full" release line on screen in Play (covered by the edit-mode test only).
- The Dawn card on a Dawn after a night lapse (seen after New Cycle only).

### Findings

- **Correction to Run 1, window X (was Major):** not a game bug. A raycast log showed those clicks never reached Unity: the Claude desktop window was popping up over that corner of the screen during the automated run. X works (three windows, one click each). The Escape half of the finding was real and is fixed.
- **Correction to Run 1, seat pickers not dimming seated characters (was Minor):** intended; the hover says "move here from Study".
- New, Major: **the pause menu is drawn under the house badges and the Home HUD** (badges, dock and council over its buttons), same cause as the map: the scene's camera-space UI sits under world sprites and the Home overlay canvases. Not fixed (shared scene canvas); a `HomeMapView`-style check for the pause menu, or raising that canvas, would do it.
- New, Minor: finishing the War council is saved only at the next Dawn save, so stopping Play right after shows it again on reload.
- If the player starts the day without clicking through the council, it is still lost (it only shows at the Day 1 Dawn plan). Hold the moon until "To work"? Open question.

### Status

The six Major findings from Run 1 are closed: five fixed, one (the X) was tooling. Uncommitted: 12 modified files, 5 new files (+ .meta). Next: Run 2 (Day 7 route).

## 2026-10-13 War council holds the moon (THJ decision)

### Built

- `HomeTimeRules.Describe`: while `NeedsWarCouncil` the moon's step is disabled with `WarCouncilHold` ("The war council is gathered: read it and click "To work"."). Two Time tests now finish the council first; new test `WarCouncil_HoldsTheMoon_UntilToWork` (Readability partial).

### Verified

- EditMode 426: 425 pass, 1 fail = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red). Play: the council shows on New Cycle and after "Start a new moon cycle"; Next / "To work" dismiss it.

### Status

Done. Uncommitted, waiting for THJ's commit approval (14 modified, 5 new + .meta).

## 2026-10-13 Playtest: Run 2 (Day 7 route)

Setup: Play from PreloadScreen, New Cycle, then Grant +5 test resources, Kitchen T2, a Workshop order (Ancestral Sword) with John helping, Old Map Fragment read by Linda. Day 1 played by hand, then Unlock the Picnic (test), Run to next Dawn to Day 7, Warren picked in Sim Debug (John, Linda, Lucy, Toba), Advance (Depart). All four Warren levels played: K on every enemy, and in the Rest Room Lucy walked to the goal tile (Numpad 6 can't be sent remotely). Skip the Picnic, end screen, Start a new moon cycle.

### Verified

- Part A 5.3 Before → after: after Kitchen T2 the roster reads "HP 32 → 38" (Linda 20 → 24, Lucy 15 → 18, Toba 24 → 29, Mark 15 → 18). In the Warren John is 38/38 (Linda 24/24, Lucy 18/18, Toba 29/29). Hovering John's portrait opens the Family sheet: "HP 32 → 38, House +6", Damage, Crit, Evade, Bond lines with the next level's unlock.
- Part A 5.1 headline cards (Skill point kind): "Skill points to spend" cards, one per hero with their line, at Dusk before the Dining Table (Day 1 and Day 7).
- Part A 5.5 SP badges: the bubble chip "SP" opens the skill-tree panel; the roster shows "SP n"; the toolbar reads "Skill Trees (2 SP)", later "(4 SP)".
- Part A 5.6 (part): on Day 7 the sortie result leads the Dining Table card in gold ("The Goblin Queen is defeated on Day 7 (0 day(s) spared)"), with the levels scouted.
- Part A 5.7: no `InitializePartially` errors with the Family sheet or the SP chip.
- Part A 4.3: Day 7 Dusk table scene is WarReportCA3 (log), Mary and Ben included.
- Part 0 (f) Skip the Picnic: PASS (straight to the end screen).
- Part 0 (b): "Start a new moon cycle" now frames the house overview, and the War council shows. PASS.
- The Workshop seat card shows the forecast ("→ John helped Uncle Ben with Ancestral Sword: ready at the next Dawn"); the sword arrives the next Dawn ("Ancestral Sword delivered").

### Not verified

- 5.1 recipe / mission-reveal / thread-cut headlines (none earned this run), "a reload does not replay them".
- 5.2 traces (sword on the rack, book on the desk) and 5.6 squad walking in with loot lines (the camera was framed on the Dining Table).
- Part 0 (e) Stargaze report line on the end screen; (j) idles inside the camera boundary; (m) FP gain VFX; (l) Lucy's role in the Rest Room (Run 3).
- Part 0 (d): no "Returning home..." text was seen on the Queen's Chamber stats Close (log has no such line either). Still open.

### Findings

Major

- **Home overlays draw over full-screen panels**: the skill-tree panel (opened from the SP chip) has station badges and the Great Moon on top of it, same cause as the pause menu found earlier. `HomeMapView`-style hiding needs extending to the skill-tree panel and the pause menu (or the house badges must sit under those canvases).
- **"Run to next Dawn" in Sim Debug did nothing on Day 2** while its window was parked at the screen corner, then worked once the window was moved into view. Most likely the click landed on a hidden part of a minimized/clipped window rather than a sim bug; noting it in case it recurs.

Minor

- Mark's "days left" bark on Day 7: "Only 0 nights remain. We cannot waste them." Needs a full-moon row or a guard for 0.
- The rest room's Campfire panel stays on screen over the mission map after leaving the room (and during the next level's load).
- The Queen's telegraph tiles stayed after a missed K (she was still alive, so this run doesn't confirm or refute Part 0 (c)'s "stay after she dies").
- K on the Queen needs the cursor right at her feet; the first try missed and she moved and hit Toba (13/29). Tooling note, not a game bug.
- The end screen's "Threads of her strength cut: 0 of 7" (expected for this route).
- 4 DOTween safe-mode warnings: a `DOShakeAnchorPos` tween on a destroyed RectTransform / CanvasGroup during level changes (caught by DOTween, no exception).
- Tooling: the remote keyboard can't send Numpad keys or chords (N+K). K one by one and walking to the goal tile work.

### Status

Run 2 done except the items above. Next: Run 3 (combat: Part 0 (d), (k), (l); 5.4 banner, step 6 items 1–4).

## 2026-10-13 Run 2 follow-up fixes (committed 139caeee5)

### Built

- `HomeMapView` extended: `TreeOpen` (AbilityUpgradePanelUI), `PauseOpen` (PauseMenu), `CoversHouse`. Badges, bubbles, world and sky moons, dock, time HUD, resource bar and recap strip hide under the Map Table, the skill-tree panel and the pause menu; the HomeDayHUD canvas hides under the pause menu.
- `HomeBarkPicker.Pick`: no "daysleft" line when 0 nights remain. Test `Barks_DaysLeft_IsNeverSpokenWithNoNightsLeft`.
- `HomeCampfirePanel`: hides on `levelEnded` (it stayed over the mission map).

### Verified

- EditMode 427: 426 pass, 1 fail = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red). Play: pause menu and skill-tree panel clean (no badges, dock, council or moon over them).

### Not verified

- Campfire panel hiding (needs a rest room).

### Status

Committed `139caeee5` on thj/home-test (29 files, author THJ). Built with write-tree / commit-tree: `git commit` itself ran past the 3-minute limit of the remote shell over the folder link. The LFS post-commit hook did not run.

## 2026-10-13 Playtest: Run 3 (combat), part 1

Cheat keys now: F12 completes the objective, F11 on a hovered enemy kills its whole faction (THJ changed them; both confirmed in Play from the remote keyboard).

Setup: Play from PreloadScreen (save continued from the earlier New Cycle). Linda & Toba +5 (test) to 23, Fireside with both on Night 1, Run to next Dawn, Day 3 Goblin Camp (Linda, Lucy, Toba, Gourd Omelette send-off), Day 4 Old Watchtower (John, Linda, Toba, Gourd Omelette).

### Verified

- 6.1: Toba's Family sheet Bond line "with Linda 18/25 Lv 2: Linda & Toba's duo, a Bond scene"; Fireside preview "Linda & Toba +5 Bond 23 → 28/45 → Lv 2: Linda & Toba's duo, Lv 2: a Bond scene"; the Fireside seat card reads "Stands up when the slot starts: Needs a partner by the fire" until the partner sits.
- 6.2: L2 reached at the Fireside; the Bond scene "Linda and Toba: The Song and the Stranger" plays at the next Dawn; the Overnight recap lists it under Unlocked.
- 6.4 (part): the Night report names the boost ("Linda & Toba: their first duo next mission is free").
- 5.4 (part): From Home banner "From Home / Gourd Omelette +10 max HP / Click to dismiss" at level start (about 4 s). Send-off +10 max HP on each squad member (log and HUD: Toba 34/34).
- Omen Red Veil applied at Goblin Camp (Masher out, enemy max HP +25%).
- 5.1 thread-cut headline: "A thread is cut", spoken by Linda, before the Dining Table (Goblin Camp and Old Watchtower).
- 2.5: Queen's Might 7 → 6 after Goblin Camp; the hover list loses the Corruption pool line; one pip shows an X.
- 5.6 (part): loot lines rise over the returning squad ("Camp: +3 Steel", "Old Watchtower: +Weathered …").

### Not verified

- 6.1/6.3 duo works after L2: at L2 the duo is only learnable ("their duo can now be learned in the Family Skill Tree (it still needs a Family Skill Point)"); not bought this run. Sisters' Rivalry / Shield Dash locks not tried.
- 6.4 the boost applying once in combat (no duo to use it on).
- 5.4 Quickberry Tart turn-1 AP pip; banner with a revealed Omen line.
- Part 0 (l) Lucy in a rest room (both missions were single-level).

### Findings

Major

- **Fireside "first duo free" can't apply** when the duo isn't learned yet: Bond L2 only makes the duo learnable (needs a Family Skill Point), so the Night 1 boost was wasted. Either the boost should pick FP cap +2 / first Family Role free when the pair has no usable duo, or L2 should grant the duo. Design question for THJ.
- **Part 0 (d) still FAIL**: no "Returning home..." text after closing the mission stats (Goblin Camp, Old Watchtower, Queen's Chamber).
- **Part 0 (k) still FAIL**: hovering or clicking an enemy shows only its HP bar, no info panel.

Minor

- Hovering an ability on the bar (Healing Marks) shows no tooltip until it is selected.

### Status

Run 3 part 1 done. Left: duo after buying it (6.1/6.3), Sisters' Rivalry and Shield Dash locks, Quickberry AP pip, Retreat on a multi-level mission (d), Lucy in a rest room (l).

## 2026-10-13 Playtest: Run 3 (combat), part 2

Setup: same save. Day 4 Dusk: bought Healing Marks \[Duo\] (Linda & Toba) in the Family Skill Tree with a Family Skill Point (2 left). Linda & Toba stayed at the Fireside (carried over). Day 5 Mossy Hollow: Linda, Lucy, Toba, Gourd Omelette.

### Verified

- 6.1: after the purchase the duo works in combat at Bond Lv 2: Toba's slot 7 "Healing Marks" fires on a column of tiles ("Active: Toba, Role: Linda"), then shows a 2-turn cooldown.
- 6.4: the Fireside boost applies: the duo fired with FP 0/6 ("first duo next mission is free").
- From Home banner again at Mossy Hollow; F11 kills the faction.

### Not verified

- The boost applying only once (a second duo in the same mission needs FP; no second cast tried).
- 6.3 Sisters' Rivalry / Command → Shield Dash locks (cheat kills don't count as a unit's own kill).
- Part 0 (d) Retreat and (l) Lucy in a rest room (no multi-level mission this run).

### Findings

- Minor: the stats screen shows "Max Damage Dealt 0" after a fight where the duo hit.
- Minor: the Skill Trees toolbar button sometimes needs two clicks (the first only focuses the window); hovering a tree node shows no description until it is clicked.

## 2026-10-13 Bond Lv 2 grants the showcase duo (THJ decision)

### Built

- New `Runtime/Presentation/HomeDuoGrant.cs`: once `sim.IsDuoAvailable(Linda, Toba)` (Bond Lv 2 flag), the Family Skill Tree node whose ability is `Linda_Toba_Duo_Ability` (Healing Marks, on Unit\_Toba) is learned for free, the way the skill-tree panel does a family purchase, minus the cost (`GUnit.TryUpgradeSkillTreeNode(guid, consumeResources: false)`), then `SaveLoadManager.Save`. Already-learned nodes are left alone (no refund for an earlier purchase).
- `HomeDayRunner.OnPhaseChanged` calls `HomeDuoGrant.Apply` at every phase change (the Bond level-up lands at a slot resolve, so the next phase grants it).
- Report line: "Linda & Toba: their duo is learned and now works in combat" (was "can now be learned in the Family Skill Tree (it still needs a Family Skill Point)").
- The combat gate (`HomeBondLocks.DuoOpen`) is unchanged: below Lv 2 the duo stays shut, and a new moon cycle shuts it again (the learned node stays learned).
- Test `DuoGrant_BondLv2_SaysTheDuoIsLearned_AndNamesItsPreset` (Readability partial).

### Verified

- EditMode 428: 427 pass, 1 fail = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).
- Play smoke: Day 5 Dusk → Night with the flag set and the node already bought: no warning, no error.

### Not verified

- The free grant itself in Play: this save already bought the node. Needs a save where Linda & Toba reach Lv 2 without the purchase (a save reset or a fresh save: THJ's call).

### Play check after a save reset (THJ approved the reset)

- Tools/Save Data/Clear Save Data → PreloadScreen → the three tutorials (F12) → Skip prologue → Day 1 → Linda & Toba +5 (test) to 23 (Linda & Mark +5 by a misclick: 15) → Fireside on Night 1 → Dawn: Lv 2, Bond scene, report "their duo is learned and now works in combat"; the Family tree shows Healing Marks at 1 with 0 points to spend.
- Not conclusive: no "\[Home\] … grants" log line. The grant ran but found the node already at 1. The level is runtime state on the Unit\_Toba prefab left from the purchase earlier in this editor session (domain reload is off), and Clear Save Data does not reset it.
- Finding (Minor, editor only): Clear Save Data leaves the skill trees' ability levels in memory until a domain reload or editor restart, so a "fresh" save inherits them in the same session.

### Status

Committed `16355c249` on thj/home-test (on top of THJ's `fe936d1ec`). Demo Spec copy updated (L2 grants the duo, no Family Skill Point). A clean Play check of the grant needs an editor restart (or a recompile), then Clear Save Data, then a fresh run to Lv 2.

## 2026-10-13 — Duo grant clean Play check (after editor restart + Clear Save Data) + 6.5 / 6.6

### Verified

- Fresh save, Day 1: Family tree shows Healing Marks 0, Points to Spend 0 (baseline).
- 6.5 staged unlocks: Day 1 moon held until the Old Map Fragment went on the desk ("Linda is waiting for you…"). Night 1: Stargaze and Fireside Talk open; Care shows as Vigil (Locked). Day 2: Yard opens with its banner ("Yard: seat a teacher and a student for a lesson") and the moon holds with "John is waiting for you: seat a teacher and a student for a lesson."
- Grant path: Linda & Toba +5 (test) to 23 → Fireside (forecast "23 → 28/45 → Lv 2") → Dawn: Lv 2 unlocked, Bond scene, report "their duo is learned and now works in combat", and the log line `[Home] Linda & Toba: Bond Lv 2 grants Healing Marks (no Family Skill Point spent)`. No exceptions from Home code.

### Findings

- ~~Major: the duo level is never saved~~ **Retracted (same evening).** Healing Marks is a StatAttribute node (Stat\_WIS on the duo ability, 2 levels), not an Ability-level node, so `upgradable` does not apply. SaveData.json has `Toba.Healing Marks.statAttrs` Stat\_WIS = 1 (written at the grant), and THJ sees 1 after closing and reopening the tree. The grant works and persists.
- Minor (unconfirmed): the first time I opened the Family tree after the grant it showed Healing Marks at 0; THJ's reopen shows 1. Likely a stale panel on that open (the Skill Trees button needed two clicks). Not reproduced.
- Note: `Linda.Healing Marks.statAttrs` is also Stat\_WIS = 1 (both units carry the duo ability). Harmless as far as seen; worth knowing if the duo heal ever looks doubled.
- UI suggestion (THJ): hide the node level number when it is 0 (and keep locked nodes at -1 blank, the padlock covers them).
- ~~Minor (6.6): Home Guide lists Workshop and Study on Day 1~~ **Withdrawn:** works as designed. A page opens when its owner's introduction is acknowledged (`IsGuideUnlocked`: introActive or introDone; tests `Schedule_GuidePages_*`, `Guide_PagesListOnlyWhatMayBeRead_*`), and I looked after both Day 1 introductions had played. The plan's "at the start" means before those introductions.
- ~~Minor: Yard intro camera ends on an empty sky view~~ **Withdrawn:** not the intro (HomeIntroDirector never moves the camera). My cursor was left about 60 px below the top of the Game view after clicking the recap's Hide, inside CameraEdgeScroller's 10 % top hot zone, so the camera edge-scrolled up until I clicked a tab.
- Known: the Skill Trees button needed two clicks again.

### Not verified

- The healing value of the duo at level 1 in combat.

### Status

No code changed this step. No data fix needed for the grant.

## 2026-10-13 Playtest: Run 3 leftovers (Bond combat locks, rest room, Retreat, Loss)

Same fresh save as the duo-grant check, played on from Day 2. Sorties: Day 2 Goblin Camp (John, Mark, Lucy; F12), Day 3 Warren (Linda, Mark, John, Lucy) with both pairs at Bond 10 (Lv 1), then Sim Debug +5 x3 to John & Mark and Linda & Lucy (25, Lv 2), Day 4 Warren again with the same squad. Mark's Command bought in his tree on Day 2 (it is a signature ability, locked until bought). Evidence from CombatLogs/\*.log.

### Verified

- 6.3 Sisters' Rivalry below L2: Linda's Bow Attack kill (ArcherGoblin #11, 6→0, Warren Gate R2) logs no synergy line and Lucy gets no AP.
- 6.3 Sisters' Rivalry at L2: the same kind of kill logs "✦ Sisters' Rivalry · Lucy: Linda kill: +1 AP, basic attack ready".
- 6.3 Command → Shield Dash at L2: after Mark's Command moved Lucy, John's Shield Dash QTE prompt appeared over him for a few seconds (not pressed, so no dash).
- 6.3 Dining Table at Dusk after the bond rise: "John & Mark: John's Shield Dash after Mark's Command now works in combat" and "Linda & Lucy: Sisters' Rivalry now works in combat", plus a "A closer bond" card for each pair.
- Bond locks re-sync only at level start (HomeBondLocks.OnPrepareLevel); the Sim Debug window shows "No cycle running" during a sortie, so bonds cannot be changed mid-sortie.
- Part 0 (l) Lucy in a rest room: Warren Rest Room entered (Anahita's Ashiyan, after Warren Barracks), Linda moved, Mark commanded Lucy, turns ended: no exception. Her role is a follow-up attack on an enemy an ally just hit, so with no enemies it has nothing to do. The Campfire panel was gone on the Victory card and the mission map (Run 1 fix holds).
- Part 0 (d) Retreat: "Retreat home" on the mission map returns to Home at once; the recap says "The family retreats from the dungeon" and lists the scouted levels; that night is taken ("No night activities after a dungeon attempt", per spec). Loss: K on all four → Defeat panel "Return Home" → Home. Both loads finished in under a second, so the "Returning home..." label (MissionEndPanelUI / CombatLevelUIManager) was never on screen long enough to see; no dead button either way.
- 6.5 First Wounded: the Loss sent John home Wounded (2 Dawns); Care and Vigil opened at Dusk; at Day 5 Dawn the moon holds with "Toba is waiting for you: seat a carer." (Toba's intro balloon is not logged, not confirmed.)
- Ability tooltips show on hover in combat (Bow Attack, Command, Fire Embers).

### Not verified

- Command → Shield Dash below L2: no QTE was seen, but my screenshot came 4 s after the move and the prompt only lasts a few seconds, so it is not conclusive. Covered by the code gate (CanShieldDashTo checks the Home unlockable) and HomeSimulationTests.CombatLocks.
- 5.4 Quickberry Tart AP pip: no Quickberry Tart on a fresh save by Day 4 (needs the recipe and grown quickberries); Sim Debug has no pantry grant.

### Findings

- Minor: the Defeat panel's Objectives list shows "Failed" with an empty objective name.
- Minor: after a Loss the recap still says "The family retreats from the dungeon".
- Note: MasherGoblin warning in the status bar on the Warren level ("did not initialize its role ability…"), as expected by 6.4.

### Status

No code changed. Save left at Day 5 Dawn, held for a carer.

## 2026-10-13 Sim Debug: Grant dish (test) + send-off popup fix; Quickberry pip check

### Built

- `Editor/HomeSimDebugWindow.Pantry.cs` (new partial; the window class is now `partial`): "Grant dish (test)" row under Mary's daily recipe. Pick any non-fallback cycle recipe (known or not) and "+1" puts one portion in the pantry through `HomeSimulation.AddPortions` (respects the pantry's capacity; says "Pantry full (n)" otherwise).
- Fix in `HomeSimDebugWindow.DrawSortie`: the "Send-off meal" popup re-applied its own last pick and called Persist() on every repaint while a sortie was chosen at Dawn, silently overriding the in-game send-off card. It now shows the sim's current meal and only changes it when the popup itself is changed. Found because the card said "Quickberry Tart (chosen)" but the sortie left with a Gourd Omelette while the Sim Debug window was open. This also explains why earlier send-off cards opened with "Gourd Omelette (chosen)" instead of "No meal".
- Test `GrantDish_AddsAPortionOfAnUnknownRecipe_UntilThePantryIsFull` (`HomeSimulationTests.DebugTools.cs`).

### Verified

- EditMode suite: 429 tests, 428 passed, only `AIRegressionTest.Baseline_MatchesCurrentAI` failed (known red).
- Play: Grant dish → Quickberry Tart in the pantry; the send-off card now opens on "No meal", Quickberry Tart chosen sticks, `[Home] Send-off Quickberry Tart on Linda/Mark/Lucy` in the log (Old Watchtower, Day 5).

### Findings

- **Major: 5.4 Quickberry Tart gives no AP on turn 1.** With the Tart applied (log above), Linda, Mark and Lucy all show 2 AP pips on turn 1 and no food-icon pip. The sendOff has a Specs\_AP +1 pool modifier and HomeFromHomeTags sets BonusApSource for UnitAPIndicator, so the surplus is probably applied at PrepareLevel and then lost when the turn's AP is set (APConsumer reset/shared Family AP). Not investigated further.

### Not verified

- The "From Home" banner on that level (not caught on screen); a revealed Omen line.

### Status

Committed `547749bb4` on thj/home-test (on top of THJ's `5a7f758da`). Play stopped mid-sortie (the sortie and the Tart come back on the next Play). The turn-1 AP issue goes to THJ / Claude Code for debugging.

## 2026-10-13 Playtest: remaining Home checks + Day 7 (same save, Day 5 → end of cycle)

Day 5: Workshop order via Sim Debug, forecast vs result, pantry full. Night 5: Linda & Lucy at the Fireside. Day 6: Mossy Hollow (Linda, Mark, Lucy, Quickberry Tart). Day 7: the Warren (Toba, Linda, John, Lucy, Gourd Omelette), F12 through Gate → Barracks → Rest Room → hostile → Queen's Chamber, Skip the Picnic, end screen. Not started a new cycle.

### Verified

- 2.5 Queen's Might after the Goblin Camp win: "6 of 7 threads stand", one pip crossed, the Corruption-pool line gone from the hover list. End screen: "Threads of her strength cut: 2 of 7" (Goblin Camp, Mossy Hollow).
- 1.4 Forecast vs result (Day 5 morning): Study "Linda studied Old Map Fragment (1/1)", Yard "Lucy taught Edge to Mark: +1, now 1/6", Homestead "Kevin tended plot 1 (Quickberry): +1 yield", Care "Toba tended John: recovered". The moon tooltip listed all four; the slot's recap and the Dusk report matched each (the +1 yield shows in the Dusk report and Sim Debug, not in the "Dawn to Noon" strip).
- Kitchen with a full pantry: badge and tab "Blocked / Pantry full"; Dusk report "Mary didn't cook: the pantry is full".
- Workshop order (placed in Sim Debug): badge "Working, Ready in 2 Dawns, Uncle Ben is working on Ancestral Sword"; Day 7 Dawn "Ancestral Sword delivered".
- 6.4 Fireside payoff (Linda & Lucy, RoleFree): at Mossy Hollow Mark downed (K) → Lucy's Family Role fired with FP staying 6/6 (free); then Lucy downed → the next role took FP 6 → 3 (normal cost). Applies once.
- 5.4 banner: "From Home / Gourd Omelette +10 max HP / Click to dismiss" on Warren Barracks (it hides after 7 s, so the first level's banner was gone by my first screenshot).
- 5.6 (part): the sortie results lead the Dusk card in gold. 4.6 (part): the squad gathers at the Door with a bark during the Send-off window.
- Part 0 (f) Skip the Picnic: goes straight to the end screen ("The Goblin Queen is defeated", How it went / Bond highlights / stores).
- Dawn cards read "5 / 2 / 1 nights remain" on the right days.

### Findings

- **Major: "Open the workshop" refuses on a staged save** with "Not yet: the family hasn't opened this room." `HomeManager.ShowWorkshopPanel` calls `RoomOpen("workshop")` with the room id, but `HomeDayRunner.IsRoomOpen` checks it as a station id (`State.IsStationUnlocked`), and station ids are GUIDs. With `stagedUnlocks` on, `unlockedStations` is filled, so "workshop" is never in it and Ben's order screen can't be opened. (Saves without staged unlocks pass because the list is empty.) Fix idea: let `IsRoomOpen` map a room id to its stations (`cycle.stations` with that `roomId`) before the station check.
- **Major: night seats carried over from the previous night can't be stood up.** Night 6 opened with Linda & Lucy already at the Fireside (from Night 5; they had been on a sortie that day). "Stand up" did nothing and showed no message, so the Vigil refused John ("At most 2 can stay up at night"). Blocked 1.7 (Vigil) and the lone-stargazer check.
- Minor: the Warren's send-off card listed "Omens of the day: A clouded sky hangs over this place." but the From Home banner showed only the meal, no "Unknown Omen in effect" line.
- Minor: the Fireside forecast/recap lines and "Assignment: Toba unseated (Morning): No one is Wounded" / "Linda unseated: Nothing to read" appear right after the work was done (noise in the Dusk report).
- Note: Care gave "+16 Bond: John & Toba" in one morning (Toba's double care bond), which jumps John & Toba most of a level.

### Not verified

- 5.2 traces (the sword on the rack was not clear in a screenshot), 5.6 squad walking in (the Dusk cards cover the house), 5.1 recipe / mission-reveal headlines (none earned; the Old Map Fragment gave a lore line, no card).
- 1.2 capped Teacher / lone stargazer, 1.7 Vigil (blocked by the finding above).
- 3.1 glance test, 3.2 Badge Side, 3.3 diamond hover, 4.2 no wandering, Kevin's walk, 2.4 Little Moon arc, Part 0 (j), (m).
- Part 0 (e) Stargaze line on the end screen (no stargazing this run).
- Part B (needs a new participant).

### Status

No code changed. Play stopped on the end screen; the save is at the end of the cycle (Queen defeated, Picnic skipped), not reset.

## 2026-10-13 Fixes after the Day 7 run

### Built

- `HomeDayRunner.IsRoomOpen` now goes through a new `RoomOpenIn(sim, id)`, which also takes a room id ("workshop") and answers for that room's stations. `HomeManager.ShowWorkshopPanel` passes the room id, so "Open the workshop" works on a staged save again. Station ids and HomeFeatures ids behave as before.
- `HomeSimulation.ValidateAssignments(committing)`: a seat of a slot that already resolved today is still dropped when it no longer fits, but no longer reported ("Toba unseated (Morning): No one is Wounded" right after she tended the patient).
- Tests (`HomeSimulationTests.Playtest4.cs`): `RoomOpen_TakesARoomId_ForItsStations_OnAStagedSave`, `ADoneMorningSeat_IsNotReportedAsUnseated_WhenTheAfternoonResolves`, `NightSeats_CarriedOverToTheNextNight_CanBeStoodUp`.

### Verified

- EditMode suite: 432 tests, 431 passed, only `AIRegressionTest.Baseline_MatchesCurrentAI` failed (known red).

### Findings revised

- **Withdrawn: "night seats carried over can't be stood up".** The sim stands a carried-over Fireside seat up fine (new test). The "Stand up" buttons sat in the top-right corner of the Game view, which the Claude desktop window covers on this machine (the same cause as Run 1's "X button ignores clicks"), so my clicks never reached Unity. The Vigil and lone-stargazer checks are still to do, by hand or with the window moved.
- **Not a banner bug: the Omen line.** The Day 7 Omen is the Hungry Moon ("The Goblin Queen gains +1 AP below 50% HP"), which is still data and display only (no enemyEffect; see HomeDemoContentBuilder: "until M6 builds the Queen level"). The banner lists only Omens with a combat effect, so it correctly leaves it out, while the send-off card and mission card still announce it. Open question for THJ: implement it, or stop announcing it.

### Not verified

- "Open the workshop" in Play on a staged save (the current save is at the end of the cycle); covered by the new test.

### Status

Committed `8bc1231e8` on thj/home-test.

## 2026-10-13 Quickberry Tart gave no extra AP on turn 1

### Built

- Root cause: `Specs_AP` is clamped to its upper bound (`StatUB_AP`, via `RuntimeAAttribute.SetValue`), so the dish's `Specs_AP` +1 pool modifier was clamped away the moment `HomeSendOffApplier` applied it. Nothing overwrote it at turn start (`ActionPoints.ResetToInitial` keeps a value above the default). A modifier that wants AP above the cap must raise both `StatUB_AP` and `Stat_AP`.
- `DishEffect.statModifierTurns` (0 = permanent, as before). Above 0 the stat modifiers are applied Temporary for that many turns (the Revenge pattern, `GUnit.cs` Revenge) via the new `HomeSendOffApplier.ApplyStat`, used by the send-off, ration and Omen appliers.
- Quickberry Tart (send-off and ration) now: `statModifierTurns` 1, `StatUB_AP` +1 and `Stat_AP` +1 (Additive), then the `Specs_AP` +1 pool modifier (stat modifiers are applied before pool modifiers). Builder helper `ApDish` in `HomeDemoContentBuilder`.
- Tests (`HomeSimulationTests.SendOffAp.cs`): tart data shape. They read the asset, so they pass only after Build Demo Content is re-run.

### Verified

- Nothing yet: not compiled, tests not run, not played.

### Not verified

- That "1 turn" lasts through the player's turn 1 and not just until the next phase tick (tickMoment PhaseStart). If the bonus is gone on turn 1, try 2 turns or tickMoment.
- The AP pip and "Quickberry Tart +1 AP" hover in Play; the "From Home" banner.

### Findings

- `StatUB_AP`/`Stat_AP` are in `UnitBase.prefab`'s Specs\_AP entry (max and default). The tart is the only recipe with a `Specs_AP` modifier.
- Related to the open tech ticket on the AP cap: this fix deliberately avoids `ActionPoints.EnsureMaxFits` (the temporary-UB raise inside `Produce`).

### Status

Edited, uncommitted on thj/home-test.

## 2026-10-13 Quickberry AP fix confirmed + Hungry Moon implemented

### Built

- Quickberry timing (risk 1 in the section above): a timed dish modifier now counts down at PhaseEnd (`HomeSendOffApplier.StatTickMoment`). The send-off is applied at level start, and the run handler calls `Tick()` (PhaseStart) right after `StartTurn()` on turn 1, so a PhaseStart countdown of 1 would have expired before the player's first action. Test `SendOffAp_TimedModifiers_CountDownAtTheEndOfTheUnitsTurn`.
- Hungry Moon: `OmenDefinition.bossApBonus` / `bossHpBelow` (counted in `HasCombatEffect`). `HomeOmenApplier.ArmBossBonus` (from `OnPrepareLevel`) finds the enemy with `BossGoblinQueen` and, on each `turnStarted` of its faction, gives it `APConsumer.Produce(bonus)` while HP < max × threshold. Static state reset in `PlayModeStaticReset`. `Omen_HungryMoon.asset` and the builder: bonus 1, below 0.5. Tests `HungryMoon_ABossApBonus_IsACombatEffect_AndShowsOnTheFromHomeBanner`, `HungryMoon_AppliesOnlyBelowTheThreshold_AndNeverToADeadBoss`.

### Verified

- EditMode suite: 437 tests, 436 passed, only `AIRegressionTest.Baseline_MatchesCurrentAI` failed (known red).
- Play, Goblin Camp with the Quickberry Tart (Linda, Mark, Lucy): turn 1 each unit shows 3 AP pips, the third a placeholder-tinted pip with "Quickberry Tart +1 AP" on hover. Turn 2: back to 2 AP pips (risk 2: the surplus is gone, nothing broken).
- Play, Day 7 Warren: the From Home banner now lists "Hungry Moon / The Goblin Queen gains +1 AP below 50% HP". In the Queen's Chamber the log reads "\[Home\] Omen Hungry Moon: Goblin Shaman gains +1 AP each turn below 50% HP" at level start; damaged to 70/150 (cheat), her next turn logged "+1 AP (HP 70/150)". She acted (Shield Dash on Linda).

### Findings

- Minor: the Queen's unit is named "Goblin Shaman" / "GoblinShaman" in logs (Nickname on the Queen prefab).
- Minor: the Warren map view changed size between levels this run (larger map, info card lower right); the boss node's info card had no Continue until the previous level was done (expected), but it looked like a dead card.
- Note: the AP pip has no icon yet (Recipe icon empty: placeholder tint).

### Not verified

- The Queen actually spending the extra AP on a second action (she was killed with F12 after one turn).

### Status

Committed on thj/home-test (see git log).

## 2026-10-14 Demo Spec: Hungry Moon row

- `Miso-Home-System_Demo-Spec.md`, Omens table (night 6): "the effect itself comes with M6" replaced by "The Goblin Queen gains +1 AP at the start of each of her turns while below 50% HP (built 2026-10-14)". No other rule or number changed this session besides the Bond Lv 2 duo grant (line 251, 2026-10-13).

## 2026-10-14 Playtest Plan updated

- `Playtest-Plan.md`: status table, Part 0 results (Oct 13), a status note on every Part A item, Run order marked done, cheat keys (F11 / F12), Sim Debug test tools and the Claude-window click trap added to Setup.

## 2026-10-14 Playtest: open checks, Oct 14 run (Claude, computer use)

2026-10-14, Unity 6000.3.4f1, from PreloadScreen. Sim Debug "New Cycle" (no save reset), +15 Bond John & Linda to set up the capped-Teacher case, then Day 1 → Day 5 Dusk played by hand. Two sorties: Goblin Camp (Day 2, John / Linda / Lucy), Mossy Hollow (Day 5, John / Lucy / Mark). Cheats only in combat (K, L, `]`, F12). Evidence: Editor log `[Home …]` lines, the Dining Table report and the combat logs `CombatLogs/20261014-203100_Goblin_Camp.log` and `20261014-205935_Mossy_Hollow.log`. Nothing in the project was edited. The Badge Side test changed a field in Play only.

### Verified

- **0(e) Stargaze report line.** Night lines "Stargaze: Mark, Lucy watched the sky", "Chart: Mark charted The Hound: Star Chart: The Hound is on the Study shelf", the Omen reveal, and the Overnight recap ("Stargaze: Mark watched the sky", "+1 Star Chart: The Lantern").
- **1.2 Capped Teacher.** After Toughness reached 6/6, John's Teacher tile in the Yard was greyed out (I did not read its tooltip).
- **1.7 Vigil.** On the sortie night (Lucy Wounded), Toba took the Vigil seat; "Toba tended Lucy: recovers at Dawn"; Lucy was in the Yard the next morning.
- **2.4 Little Moon arc.** It moves along its arc from Morning to Night and parks at Night. The arc is small; THJ to judge the look.
- **3.1 Glance test.** From the overview, every badge matched its window: Workshop "Working / Ready in 2 Dawns", Kitchen "Blocked / Pantry full", Study "Needs input / Desk empty", Care "Blocked / No one is Wounded", Porch "Idle".
- **3.2 Badge Side.** On `Prop - homestead`, Top and Left move the badge as expected.
- **3.8 Lapse effects.** During a lapse, `Fx Workshop` and `Fx Study` particles spawn at their props (yellow sparks, pages). They are small and hard to see from the overview.
- **4.2 No wandering.** Unseated characters stay at their spots through the slots (`spot-Lucy`, `spot-Toba`, `spot-Kevin`, porch pair). No wandering in any idle log line.
- **4.6 Send-off (partly).** The squad gathers at the Door with a bark and `JohnGate` plays when John goes.
- **5.1 Headline cards.** The Kitchen discovery card ("A new recipe", Mary), the mission-reveal card ("A new mission", John: Drowned Shrine), Thread-cut and Bond cards all show, one at a time, before the Dining Table. A Play restart at Night did not replay them. Cards not yet dismissed do show again after a restart at Dusk, which is expected.
- **5.2 Traces (placeholders).** Four pantry squares match Pantry 4/4, a green square appears in the planted plot, and a white square sits on the desk while Mark reads.
- **6.3 Shield Dash below Lv 2.** John–Mark at Lv 1: Mark's Command moved John and no Shield Dash followed (combat log: Command → John, moved, nothing after).
- **0(n), partly.** Panel text: Sidewinders "Each upgrade adds 1 sidewinder"; Kindled Spirits "+10% critical chance while Lucy is in the squad"; Marks-Sisters, Hide and Seek and Healing Marks pages read right. Buying works: Sidewinders 1, Father's Resolve (unlocks C, as the A→C edge should), Hide and Seek 1 with the earned Family SP. Healing Marks shows 1 from the free Bond Lv 2 grant. Purchases survive a Play restart (SP count 3 = 2 left + Lucy's level-up; Father's Resolve still unlocked). Lucy's locked Blink is not in her hotbar. Hide and Seek at level 0 makes 2 decoys (Goblin Camp log), which matches the spec.

### Not verified (still open)

- 0(j) Main's idles inside the camera boundary; 3.3 diamond hover outline; Kevin's side-view walk; the weapon on Ben's rack (5.2).
- 1.2 lone stargazer with nothing to chart (see finding 6: Night 1 can't test it).
- 4.4 bark pace: judged only from the log (findings 8 and 9).
- 0(m) FP gain VFX: L (+99 FP) on Lucy showed no HUD VFX in four frames, but the bar may have been full. See finding 10.
- 0(n) combat effect per node. I could not get Lucy's Fire Embers to fire by clicking in Mossy Hollow, so I measured no Sidewinders, Hide and Seek 3 or Father's Resolve effect. The combat log can do this check (sidewinder and decoy lines per cast); it needs a hand-played fight.
- Part B (needs a new player).

### Findings

1. **Major: Dawn-tick report lines are lost on sortie days.** After the combat scene reloads Home, `CurrentReport` starts empty. Day 2's Dining Table and log go straight from `=== Home day 2 ===` to `[Sortie]`, with no harvest, hens, moon or Workshop lines. Both weapon deliveries fell on sortie days (Ancestral Sword Lv 2, Day 2; Crescent Bow Lv 2, Day 5). Neither "Uncle Ben finished …" line nor the "A weapon is ready" card appeared, although the Overnight recap said "Crescent Bow delivered". Likely cause: `HomeDayReport` is not saved, and the reload builds a new one. The same probably hides other Dawn-tick headlines (Upgrade).
2. **Major: The Kitchen forecast ignores the morning batch.** On Day 3 the Kitchen badge and window said "Mary cooks Gourd Omelette in the afternoon" (pantry 2/4). Kevin's morning batch of Hearty Stew made 2 and filled the pantry. The result was "Mary didn't cook: the pantry is full", so the forecast and the recap disagree (1.4).
3. **Minor: A recipe learned in the Study gets no headline card.** "Star Chart: The Lantern: Learned recipe: Quickberry Tart / Hunter's Skewer" appears only in the Dining Table text. `UnlockRecipeOutcome` reports without setting `headline = Recipe`, while `RevealMissionOutcome` sets its headline.
4. **Minor: The Great Moon can't turn red.** `HomeSkyDecay.GreatTint` multiplies the sprite by (1, 1−0.45d, 1−0.55d). The art is cyan (low red), so the result is only a darker teal. Confirmed on Day 5 (2.4). A lerp toward a red target would work.
5. **Minor: The camera does not frame the overview at Night (3.6).** Reproduced on 3 of 3 nights: "Go into the night" frames the roof / Stargaze side, not the overview. If that is intended for night, the plan's rule needs updating.
6. **Minor: The lore-only Great Moon counts as chartable.** On Night 1 a lone Mark is allowed and offered "Chart The Great Moon". The result is lore only ("Mark watched The Great Moon"), and a second watcher is not marked "Bond only". `HomeSeatRules.Stargaze` uses `CanChart`, which does not exclude patterns with no `chartItem`.
7. **Minor: The Care badge showed Kevin's refusal.** On Day 4 the Care badge read "Blocked / No one is Wounded / Kevin only helps with the chores (Homestead or Kitchen, by day)".
8. **Minor: Hidden avatars can't bark, so the wrong person speaks.** While John's `JohnSword` idle hides his avatar, "assign:Yard(John)" was spoken by Toba ("Again. Do it again."), who isn't in the Yard. Also "bond:(Mark,Toba)" was spoken by Linda ("…time like this, Mark"). `HomeBarkPicker` falls back to any speaker when the involved ones can't speak. Suggest dropping the bark instead of handing it to an uninvolved character.
9. **Minor: Idle barks are repetitive.** Over 3 minutes of planning, Kevin and Toba alternated the same two lines about every 50 s ("Can I help with something?", "I will go wherever I am needed.").
10. **Minor: the FP gain VFX plays once at level start (corrected).** `FPGainAnimation` in `Level Info Panel.prefab` is saved active, so its animation plays as the level loads. The `DisableOnAnimationEnd` behaviour on its `AC_FTPPanel_FPGain` state turns it off afterwards, so later gains replay it as they should. My first reading (that nothing turns it off) was wrong. 0(m) was probably not seen because FP was already full, and `PlayerController.ProduceFTP` plays the VFX only when the value goes up. Same files as `origin/main`. Fix if wanted: save `FPGainAnimation` inactive. Also, `FTPIndicator.prefab` has no `ftpGainVFX` assigned and would throw if it were used.
11. **Minor: Linda shows twice at Dawn (recurs).** `Day 3 DawnPlan: LindaInBed (shows Linda) | Linda=shown@bedroom-Linda`.
12. **Minor: Send-off, the family at home stays put.** Toba (free, in her bedroom) did not walk to the Door; Mark and Kevin were seated. Check whether 4.6 means everyone at home or only the free ones.
13. **Minor: The combat log LOADOUT line leaves out unlock nodes.** John: "Tree: Hide and Seek 1" without Father's Resolve.
14. **Still open:** 0(k) enemy info shows only the HP bar on hover (Goblin Camp, Mossy Hollow); "Max Damage Dealt 0" on the stats screen; the Skill Trees button needs two clicks; node descriptions only on click; hens go hungry by Day 4 ("1 went hungry (no feed)"); Toba's double Care Bond (Lucy & Toba +16 at the Vigil).

### Status

Run A done except 0(j), the diamond hover outline, Kevin's walk and the rack trace. Run B done for 6.3 and the 0(n) panel and save. Node combat effects and 0(m) still need a hand-played fight. Part B not run.

## 2026-10-15 Oct 14 playtest fixes: report kept across sorties, Kitchen forecast, recipe cards

2026-10-15. From findings 1–3 of "Playtest: open checks, Oct 14 run".

### Built

- **The day's report is part of the save.** `HomeSaveData.report` (new) holds today's `HomeDayReport`, and `HomeSimulation.CurrentReport` reads and writes it. `Resume()` keeps it when it is today's and replaces it otherwise (an old save reads day 0). `HomeDayReport` gained a parameterless constructor for JsonUtility. Result: on a sortie day the Dawn lines (harvest, hens, moon, Workshop delivery) and their headlines (the Weapon card) survive the Home scene reload after combat and a Play restart. The "headlines seen" counter now indexes a list that stays the same across reloads.
- **Mary's Kitchen badge sees the morning.** With a Kitchen seat in the Morning, `HomeStationState.DescribeKitchenOwner` judges her afternoon on a forecast copy of the sim after the morning resolves. It reads "Mary won't cook: the morning's cooking fills the pantry" or "…: the morning's cooking uses the ingredients". At Dusk and Night it reads "Mary cooks X tomorrow afternoon".
- **Recipe cards from the Study and missions.** `UnlockRecipeOutcome` marks its line as a Recipe headline (refId = recipe), like a Kitchen discovery. One card per recipe (The Lantern gives two), spoken by Mary.
- **`Level Info Panel.prefab` (THJ):** `FPGainAnimation` is saved inactive, so it no longer plays as the level loads; `PlayFTPGainVFX` turns it on for each gain.
- **Linda shown twice (added at THJ's request):** `HomeIdleDirector.Update` re-hides every claimed character each tick (`Show(c, view, false)`; `SetClaimed` is a no-op when already hidden). Covers an idle claimed before `HomeHouseView` has created the avatars after a scene load.
- Tests: `Editor/HomeSimulationTests.ReportPersistence.cs` (6). The report survives a rebuilt sim and a JsonUtility round trip with its Weapon headline; another day's report is replaced on Resume; a morning batch that fills the pantry stops Mary on the badge and in the result; "tomorrow afternoon" at Dusk; a recipe learned outside the Kitchen gives one Recipe card.

### Verified

- Unity compiles; EditMode suite as expected (all green except `AIRegressionTest.Baseline_MatchesCurrentAI`, known red), per THJ.

- **Play check (Claude, 2026-10-15)**, New Cycle in Sim Debug, Day 1 → Day 2 Dusk with a Goblin Camp sortie:
  - Weapon on a sortie day: sword ordered Day 1 with Mark helping, delivered at Day 2 Dawn, sortie, F12. Back home the Dusk shows "A weapon is ready · Ben · Uncle Ben finished Ancestral Sword Lv.2", and the Dining Table lists the Day 2 Dawn lines (harvest, hens, Ben, moon) above the sortie. The combat LOADOUT shows the sword at Lv1.
  - Mary's badge: pantry 2/4, Kevin batch-cooking Gourd Omelette in the Morning → "Mary won't cook: the morning's cooking fills the pantry". Dining Table: "Mary didn't cook: the pantry is full". At Night: "Mary cooks Gourd Omelette tomorrow afternoon".
  - The Lantern (granted, studied by John): two cards at Dusk, "A new recipe · Mary", Quickberry Tart then Hunter's Skewer, after the skill-point cards.
  - Linda: Day 1 Dawn log `LindaInBed (shows Linda) | Linda=hidden@bedroom-Linda`. After two scene loads (Play start at Dusk, return from the sortie) the idle was claimed while avatars were `none`, and only the dinner idle showed at the table: no extra avatars.
  - Bonus 0(n): Hide and Seek at level 1 spawned 3 decoys (combat log), matching the 2 → 3 → 4 spec.

### Not verified

- The FP gain effect replaying on a gain: FP was full at the start of Goblin Camp (6/6) and at its practical cap after the duo (7/9), so L gave no gain. Not playing at level load follows from the object being saved inactive.

### Findings

- The Kitchen badge builds a forecast copy (a JSON clone of the save) on each refresh only while a Morning Kitchen seat exists. Watch for a hitch on that badge if refreshes are frequent.
- Minor, new: the recap strip's Unlocked column misses learned recipes and revealed missions. `HomeRecap` checks `StartsWith("Learned recipe")` / `"Revealed mission"`, but outcome lines carry their source prefix ("Star Chart: The Lantern: Learned recipe: …").
- Minor, new: the Workshop badge says "Ready in 2 Dawns" while a helper sits there that day; the order is ready at the next Dawn (Noon badge: "Ready at Dawn").
- Minor, new: on Night 1 the Great Moon took no clicks (no tooltip either); Sim Debug "Run to next Dawn" moved on. Not reproduced.
- Minor: Mary's and Ben's headline cards have no portrait.

### Status

Built; EditMode green (THJ); Play-checked except the FP gain replay. Committed by THJ: `849c318ab` (prefab), `2f828e662` (code and tests).

## Report-card context images (2026-10-16, pilot 2)

Plan `plans/2026-10-16-report-card-images.md`; reports `reports/report-card-images.md` and `reports/report-card-images-verify.md`. Decision D-043.

### Built

- The Dusk headline card shows a context image (60 pt, beside the speaker portrait) for Weapon, Upgrade, Recipe, Mission and Thread cut. The sprite is resolved at display time from `refId` (`FindWorkshopItem(refId)?.icon`, or `Cycle.Find<T>(refId)?.icon`); no image when there is no icon. No save-format change.
- New: `Runtime/Simulation/HomeHeadlineContext.cs` (pure kind-to-source mapping), `Editor/HomeSimulationTests.HeadlineIcons.cs` (4 tests). Edited: `Runtime/UI/HomeDayHUD.Headlines.cs` (+19 lines).

### Verified

- Compile clean; EditMode 447 run, 446 passed, 1 failed (the known red `AIRegressionTest.Baseline_MatchesCurrentAI`), via the command-line route (63 s).
- Play-checked by THJ: "it worked".

### Not verified

- The verifier did not drive the editor (it was closed). The null-icon card and per-kind detail were not reported separately by THJ.

### Findings

- `tech/editor-checks.md` corrected (editor-open check, command-line timing).
- Workflow: subagents' Write of report files was refused; the coordinator saved the reports. The auto-mode classifier skipped several writes until the permission mode was switched.

### Status

Built and checked; code not yet committed (proposed: helper plus tests, then card rendering).

## 2026-10-18 · Playtest Batch 1 fixes (B1, B3, B6, B8, B5 diagnostic) · `thj/oct-build-fixes`

Plan `plans/2026-10-18-playtest-batch1-bugfixes.md` (commit hashes in its log); reports `playtest-b1-cleanse-state`, `playtest-b1-safety-net`, `playtest-b3-hp-display`, `playtest-b6-map-panel`, `playtest-b8-tutorial-input-lock`, `playtest-b5-workshop-diagnostic`, `playtest-batch1-verify`, `playtest-batch1-verify-play`. Decisions D-052 to D-056.

### Built

- B1: placeholder `SoulSacrifice` state in Mark's animator (John's clip) plus a safety net: an ability whose animation state is missing logs one error and activates at once (`RuntimeAbility`, core; reviewer APPROVE).
- B3: HP bar text shows at least 1 while the unit is alive (`FillBarTextFormatter`); HP rounding untouched (D-054).
- B6: mission info panel anchored to the right edge (`LevelInfoPanel.prefab`, `WorldMapPanel.prefab` override).
- B8: owner-keyed input lock on `PlayerInputController` (core, approved by THJ), taken by `CombatLevelUIManager.ShowTutorial`.
- B5: `HomeInteractables.RefreshLock()` plus temporary `[B5-DIAG]` logs; cause unconfirmed.

### Verified

- Compile clean; EditMode 79 run, 78 passed, 1 failed (the known red). 79 is the full suite on this branch (the 447 of Oct 16 included the Home tests).
- Played by Claude (desktop, computer use, fresh save): Mark's and John's Cleanse resolve with no freeze and no console error; Mark and an enemy archer read 1 HP, not 0; the mission panel is fully on screen at 16:9, 16:10, 4:3 on the world map; with a tutorial open, clicks, right click, Tab, WASD, Shift and Escape do nothing, and input is back after closing (also with an enemy introduction in the same level).

### Not verified

- A corrupted tile clearing; the safety-net error line; a fractional HP below 0.5; the damage preview; the mission map (MissionMap prefab) at any ratio; a tutorial at a turn change or mid turn; 21:9; the B5 repro.

### Findings

- Play-check run deleted the game save (Clear Save Data) to replay tutorials; THJ allowed it.
- 4:3 world map: the panel hides mission marker 4 and the compass while a mission is selected.
- Open follow-ups: `abilityActivationFrame` at or past the clip end freezes an ability; a second `ShowTutorial` leaves `timeScale` 0; 21:9 world-map panel overshoots ~46 px; hover panel keeps old HP after cheat damage until the cursor moves; DOTween noise on opening the world map from Home (not traced).

### Status

Committed (6 commits). B1 (freeze), B8 (lock and restore) and B6 (world map) seen in play; B3 seen at whole-number HP only; B5 waits for THJ's repro.

## 2026-10-19 · B5 Workshop click fix · `thj/fr-readability`

Plan `plans/2026-10-18-playtest-batch1-bugfixes.md` (B5; hashes in its commit log); reports `b5-click-diag`, `b5-diag-removal`, `b5-diag-removal-verify`. Decisions D-073, D-074.

### Built

- Root cause: `Home.prefab`'s `Workshop Cabinet` has a leftover script-less BoxCollider2D (4.32 x 5.28) that fully covers `Equipments Cabinet`'s collider. Neither has a renderer on the collider's object and both sit at z 0, so the Physics2D raycast tie falls to an arbitrary order (likely reshuffled when M3's HomeState spawns the `BenJoeyGrind` actors); when Workshop Cabinet wins, the click has no handler.
- Fix (THJ's edit): a scene override in `Home - Scene.unity` sets that collider's `m_Enabled: 0`. All `[B5-DIAG]` code removed from `HomeInteractables.cs`; the C6 `RefreshLock()` hardening stays.

### Verified

- Compile clean; EditMode 175 run, 174 passed, 1 failed (the known red). Override present in the scene file.

### Not verified

- In Play: after winning M3 - Mark Intro, the Workshop opens and highlights on every click.

### Findings

- The unused MortaStory actor `Equipments Cabinet.prefab` (id 203) has the same oversized collider (backlog).
- `thj/oct-build-fixes` still carries the C6 diagnostics.
- Console: "Internal error - unexpected guid mismatch" and 7x "Objects are trying to be loaded during a domain backup" (not new, not traced).

### Status

Committed: `da54e4ec2` (scene override), `b3e4c030e` (diagnostics removed). Play check pending.

## 2026-10-19 · Role zones: each unit's own icon in its own quadrant · `thj/fr-readability`

Plan `plans/2026-10-19-role-zone-unit-sprites.md` (hashes in its commit log); reports `role-zone-unit-sprites-c1`, `-c2`, `-c1-review`, `-verify`. Decision D-075.

### Built

- C1 (code): `FactionRoleHandlerBase` gains `roleZoneSprite` and `roleZoneSlot` (Inspector, UI only). `GridCell.SetRoleZone` takes a sprite and a slot and draws each entry as a Simple sprite, aspect kept, in its quadrant of the cell or footprint box (`RoleZoneSlotLayout.Fit`), instead of nested outlines. An empty sprite falls back to `RoleZoneOutline` with a warning once per handler. Both presenters pass the handler's sprite and slot.
- C2 (data): John ShieldOutline TopLeft, Mark PunchOutline TopRight, Linda Arrow BottomLeft, Lucy Fireball BottomRight. The four PNGs are added with their metas.

### Verified

- Compile clean. EditMode 191 run, 190 passed, the known red failed. The prefabs resolve to the right sprite and slot. The four fitted rects don't overlap. Reviewer APPROVE.

### Not verified

- In Play: Shift view with all four, overlapping zones, Mark's and a big enemy's footprint, the follow zone, downscaled icons (jagged or shimmering?), whether a lone corner icon reads.

### Findings

- The pivot is assumed to be the centre (true for all five sprites). Reviewer's optional fix noted.
- 13 "Serialization depth limit 10" console messages, apparently pre-existing (they start at `FactionRoleHandlerBase.ability`), not compared against a build without the change.
- `BowArrow.png` is untracked and unused.

### Status

Committed `f2de13678`, `4d2f8c1a4`, `a7e28f0f4`. Play check pending.

## 2026-10-20 · Grid preview pass (C1–C8) · `thj/preview-improvements`

Notes `playtests/2026-10-19-preview-notes.md`; design `plans/2026-10-19-preview-pass-design.md`; tech plan `plans/2026-10-19-preview-pass-tech.md` (17 commits, hashes in its log); reports `reports/preview-pass-c1.md` to `-c8.md`, with reviews for C2 to C7. Decisions D-076 to D-086.

### Built

- C1/C2: one attack-reach helper. John's dash is straight lines, ranged reach crosses gaps, and the ghost and approach previews match the real attack.
- C3: grid hover gated over the screen-space HUD.
- C4: the role badge drives the role-zone layer through a new additive bus event.
- C5: Shift shows current-tile reach for Bergsons and allies, and a danger zone for hostile units, with new tints.
- C6: under Shift all zones stay and the hovered one is enlarged. A selected unit's zone that equals its basic attack is hidden, with a tooltip line.
- C7: every Bergson's zone follows the move ghost. The cover marker is the coverer's own icon.
- C8: John's tether is a thin translucent arc with a shield cap.

### Verified

- Compile clean after each chunk. EditMode 267/268 (known red only), with 69 new tests across the chunks. Reviewer: APPROVE on C2, C3, C4, C6. FIX on C5 (allies got the enemy model) and C7 (commit split for core handlers), both fixed before commit.

### Not verified

- Everything in play. Checklist: `playtests/2026-10-20-preview-pass-play-check.md`. That includes P1's inferred cause, whether the Linda/Lucy hide fires, the commit flash, cover-icon draw order under Shift, and dense-board readability.

### Findings

- Enemy danger zone costs 1.3–3.9 ms per Shift hover (synthetic). Profile in play.
- Multi-cell ghost reach may over-report for non-Unconstrained walkability (C2 review).
- Narrative backlog: Linda's "(1 FP)" text and the dev tooltip titles.

### Status

Built and committed; play check pending (THJ).

## 2026-10-20 · Preview pass play fixes · `thj/preview-improvements`

Decisions D-087 (D-064 narrowing restored, reversing D-076), D-088 and D-089. Reports `preview-pass-fix1-explore.md`, `preview-pass-fix1.md`, `preview-pass-fix1-review.md`.

### Built

- Shift hover narrows to the hovered unit's zone again (`590f0a3c2`).
- John's tether uses a plain material, 0.025 wide, alpha 0.85, drawn above its two units (`eddb34e7c`). It had been invisible because the borrowed `M_LineShine` turned the orange near-black and it sorted under the units.
- Per-tile sword icons on multi-tile units, raised to `DynamicTop` on covered tiles, with the sorting refreshed on plug and unplug (`3cd8bba21`, core). A targeted multi-tile unit is marked on every tile (`f5d263743`, core).

### Verified

- EditMode 272/273 (known red). Reviewer APPROVE (core). **THJ confirmed all three in play on 2026-10-20.**

### Status

Done. The rest of the C9 checklist is not reported yet.

## 2026-10-20 · Grid preview pass closed · `main`

### Verified

- THJ played the whole C9 checklist (`playtests/2026-10-20-preview-pass-play-check.md`). Every item is confirmed; no flash on commit, so the follow-zone hold fix isn't needed. Earlier: threat arcs count next-turn attacks (`d1254f7c8`, D-090), and the role colours stay (D-091).

### Status

Done. THJ merged `thj/preview-improvements` into `main` on 2026-10-20. The GDD labels were updated after the merge; the "Miso — Game Design" mirror needs a re-sync of Family systems and Combat rules.

## 2026-10-20 · Masher reckless tank (`masher-tweak`)

**Built.** The Masher Goblin's counter rework (design `plans/2026-10-20-masher-reckless-tank-design.md`, tech `plans/2026-10-20-masher-reckless-tank-tech.md`, D-092 to D-118), in five chunks and ten commits:
- C1, core turn flow: the AI waits on its own action and replans if one started meanwhile (`08ca1d819`); turn-switch holds with a watchdog (`11f64c19f`).
- C2: pure rules for aim, step, provokers, the Duo partner and the cap of 10, with tests (`212638ad2`).
- C3, data: the counter is a copy of the slam, both slams target units only, and the prefab has one counter handler (`e409b2c94`); one AI catalog line (`519e05d9e`).
- C4: the role-suppression check in Mark and Linda (`7556630a6`); a null guard on the base role handler's super-time ability (`d5402d48d`); the handler rewrite: queued answers after the whole action, reactions in any phase, Duo credit, Crippled, the cap, the toggle, and the tether filter (`9e6d50f51`).
- C5: the `PlayerController` lookups made public (`1a0936a28`); the hover preview now follows the real answer (`256bcade6`).

**Verified.** Each chunk: clean compile, and EditMode green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (356/357 at C5). Reviewer APPROVE on every chunk, after FIX rounds on C1, C4 and C5.

**Not verified.** Everything in game. Checklist: `playtests/2026-10-20-masher-play-check.md`.

**Findings.**
- John's relay of Masher answers may never have worked.
- The Masher panel now shows a Family Role badge; THJ to keep or hide it.
- The Unity MCP tools are fixed at session start. `/mcp` reconnects reach subagents launched after the reconnect.

**Status.** Waiting on THJ's play session. `thj/home-test` needs all ten commits when it takes this work.


## 2026-10-21: Quick wins bundle A, C1 (one-click cancel)

- **Built:** `PlayerController.OnCancelInput()` replaces the one-step right-click; `CancelInputRules` (pure static) decides: undo the last picked target while targets are picked, else deselect fully; ignored during the level intro, a QTE or Family Role prompt, the unit's own action and while another faction acts (allowed in a reactive interrupt). 10 EditMode tests. Commit `64fbabef5` on `thj/quick-wins`. Plan `plans/2026-10-21-quick-wins-a-tech.md`, D-130.
- **Verified:** reviewer APPROVE (should-fix applied); THJ: compile clean, EditMode suite passed (known red only), played and it works.
- **Not verified:** nothing open for C1.
- **Findings:** undoing the only picked target drops back to unit selection with the move range (existing behaviour, kept).
- **Status:** C1 done; C2 next.

## 2026-10-21: Quick wins bundle A, C2 (John's shield animation variants)

- **Built:** `EntityAnimationHandler` state variant (additive `SetStateVariant`/`ClearStateVariant`; a state plays its `_Shield` version when the animator has one); `JohnShieldRelay` sets it with the shield and clears it on shield end, death, level end and disable. John's `Hit` state lost its leftover transition to `Idle`, and his Hit clips now play once, so the handler ends Hit and returns to the right idle. 8 EditMode tests. Commits `dd567cdbc`, `7716c3a8c`; THJ's shielded run tweak `51058e216`. D-133.
- **Verified:** reviewer APPROVE (two should-fixes applied); compile clean and EditMode 430/431 (known red only) through the Unity MCP; THJ play check: idle, run, attack shield poses, hit while shielded returns to `Idle_Shield`.
- **Not verified:** nothing open for C2.
- **Findings:** the shielded attack is 0.8 s against 1.2 s (THJ: feels fine). The switch animation and a QTE-pause swap don't use the variant (known edges, left).
- **Status:** C2 done; C3 next.

## 2026-10-21: Quick wins bundle A, C3a (stepped HP preview + lethal skull)

- **Built:** while picking several targets, HP bars show confirmed hits (red) and this click's hit (light orange); picked targets keep their confirmed segment while the cursor is elsewhere. A pulsing lethal skull on every damage preview (placeholder sprite `Epic skull.png`): confirmed kills show the normal skull, the firing click shows it in the light tint when that click finishes the kill. Option `displayLethalMarkPreview` on `GlobalSettingsSO`. `GUnit.ShowDamagePreview(total, confirmed, pick)` additive overload; `AbilityDamagePreview` math unchanged. Commits `11af7b05c`, `ef14a0d80`, `127c6964e`. D-134 to D-137.
- **Verified:** reviewer APPROVE (should-fixes applied); EditMode 462/463 (known red only) through the Unity MCP; THJ play check passed.
- **Not verified:** nothing open for C3a.
- **Findings:** the planned target-counter label (C3c) was not needed and is dropped. `ef14a0d80` carries harmless Unity resave noise in two prefabs. THJ may want a stronger deep red on lethal segments and final skull art.
- **Status:** C3a done; C3b next.

## 2026-10-21: Quick wins bundle A, C3b ("fires" cursor)

- **Built:** a final-pick axis in the cursor catalog (yes when a multi-target ability has one pick left, including the first pick via the default ability) and a "Multi Fire" row (priority 66) with placeholder `cursor_fire.png` (a copy of the attack cursor). 11 EditMode tests incl. the real catalog asset. Commit `879f560f9`. D-134.
- **Verified:** compile clean; EditMode 473/474 (known red only).
- **Not verified:** the cursor in play (looks like the attack cursor until THJ repaints it).
- **Findings:** none.
- **Status:** C3b done pending art; C4 next.

## 2026-10-21: Quick wins bundle A, C4 (objectives panel)

- **Built:** the objectives panel stays open (no auto-fold), a click folds/unfolds it, an objectives change re-opens it, hover does nothing; the first try (a one-line summary when folded) was dropped after THJ's play check. `ObjectivesFoldRules` with EditMode tests. Commit `785374c51`. D-138.
- **Verified:** compile clean; EditMode 481/482 (known red only); THJ play check incl. the mid-level objective change in LevelMarkIntro-C1.
- **Not verified:** nothing open for C4.
- **Findings:** in LevelMarkIntro-C1 the queued win set's new objective gets its text only after the stage's sequence and LevelSpecificBehaviour (`WaitThenEvaluateNewStage`). The panel's resize called `LayoutRebuilder.ForceRebuildLayoutImmediate` on the mask, which has no layout controller, so nothing rebuilt and the old height was measured; rebuilding the objectives container fixes it. Found with temporary `[OBJ-DIAG]` logs (removed) and a read-only live probe through the Unity MCP. Process note: an implementer edited scripts during THJ's Play session and stopped Play once; implementers now never toggle Play mode.
- **Status:** C4 done; C5 next.

## 2026-10-22: Quick wins bundle A, C5 (enemy idle spread) and C6 (Mark's hit sound)

- **Built:** C5: `IdlePhaseSequence` (golden-ratio start phases, reset each play session) replaces `Random.value` in `EntityAnimationHandler.Play`; opt-in per-unit speed spread on the idle only (others keep authored speed); Pause captures once, Resume restores the playing state's speed. 8 enemy prefabs at ±15 %. C6: Mark's hit plays `A_SFX_John_Hit`. Commits `74aa5f23f`, `f234f7259`. D-139.
- **Verified:** EditMode 491/492 (known red only, confirmed by name); THJ play check passed.
- **Not verified:** the ±15 % value in play (raised at commit time).
- **Findings:** (1) enemy controllers still have animator transitions into Idle (Hit/Spawn, Queen jump/charge ends, Deev Idle Look), which bypass the handler: after a hit or spawn the idle plays at authored speed from frame 0. (2) Mark's Walk/Command/Cleanse sound overrides are empty (backlog). (3) An implementer left a scratch prefab copy in `Assets/`; deleted with THJ's OK.
- **Status:** C5, C6 done; C5b proposed; C7, C8 next.

## 2026-10-22: Quick wins bundle A, C5b (enemy idle returns) and boss idle revert

- **Built:** removed the animator's own Hit → Idle (Dark Claw, Archer, Masher, Dark Worm, Shaman) and Spawn → Idle (Dark Claw, Dark Worm, Shaman) transitions so the handler ends those clips and plays the spread idle; the Dark Worm's looping spawn clip now plays once. Kept, with reasons in `reports/qw-a-c5b.md`: the Queen's Hit/JumpEnd/ChargeAttackEnd → Idle and her chains, the Deev's entry and Idle Look loop. `EnemyIdleReturnTransitionTests` pins both. Then the Queen and Deev prefabs were put back to their pre-C5 idle (no spread). Commits `8924cbe2b`, `ba186931e`. D-140.
- **Verified:** guard test 26/26; EditMode 517/518 (known red only); THJ play check passed.
- **Not verified:** nothing open.
- **Findings:** the Mountain Deev has no `Hit` state though `UnitBase` plays one (backlog).
- **Status:** done; C7 and C8 next.

## 2026-10-22: Quick wins bundle A, C7 and C8; bundle A complete

- **Built:** C7: `Equipment_Shin Armor` and `Equipment_Vitality Brooch` start Hidden. C8: `OutroCutsceneKeepGridHidden` (input + HUD, no grid fade-in) ends `Level1C1-2`'s end sequence. Commits `945067759`, `fc731b0c5`. D-108, D-131.
- **Verified:** EditMode 517/518 (known red only); THJ play check (fresh save Workshop; M1 level 2 end).
- **Not verified:** the character equipment panel (its Hidden filter is commented out, so the two items may show there).
- **Findings:** none new.
- **Status:** bundle A done on `thj/quick-wins`: C1 cancel, C2 shield poses, C3a stepped preview + lethal skull, C3b fires cursor (art pending), C4 objectives panel, C5/C5b idle spread, C6 Mark hit sound, C7, C8 (C3c dropped). Next: bundle P.

## 2026-10-22: `thj/quick-wins` merged into `main`

- **Built:** fast-forward of `main` from `3ae174a93` to `fc731b0c5` (15 commits, 68 files); THJ's uncommitted package/ProjectSettings changes carried over untouched. Not pushed.
- **Verified:** Unity reopened on `main`, compile clean, no console errors; EditMode 517/518, the only failure the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (run through the Unity MCP after THJ reconnected it with /mcp).
- **Not verified:** nothing open.
- **Findings:** closing Unity drops this session's Unity MCP connection; it comes back only when THJ reconnects it via /mcp (a fresh subagent doesn't reconnect it).
- **Status:** `main` carries bundle A. Next: bundle P (pace).

## 2026-10-22: Quick wins bundle P, C1 (non-blocking phase banner)

**Built:** the turn switch starts the phase banner without waiting for it (`CombatLevelRunHandler.SwitchTurnIE` → new `CombatLevelUIManager.PlayPhaseAnimation`); the End Turn panel hides/shows in the same frame; `HideHUD` hides the banner at once; `PhaseVisualsUI` shares one sequence helper, adds `HideInstant`, kills its tween on destroy, eases both slides. Commit `5d1456ea3`. Plan `plans/2026-10-22-quick-wins-p-pace-tech.md` (D-141).
**Verified:** compile clean; EditMode 517/518 (known red only); reviewer APPROVE (`reports/quick-wins-p-c1-review.md`).
**Not verified:** nothing played yet; the banner keeps its old 3 s timing and top-centre spot until C3.
**Findings:** the banner's graphics catch raycasts, so clicks under it are swallowed now that the turn runs underneath (fix folded into C3); a turn-start HUD-hiding sequence now cuts the banner (play check); `UIPanelAnimator.Visible` can go stale (backlog, dev toggle only).
**Status:** C2 next.

## 2026-10-22: Quick wins bundle P, C1b (no player input during the player's banner)

**Built:** the player's banner holds the existing input lock (one owner per banner, released on finish, hide, replacement or destroy); the ability bar (buttons and 1–9) and the End Turn button check the lock themselves. Commit `fd52cc377`. D-142.
**Verified:** compile clean; EditMode 517/518 (known red only); reviewer APPROVE (`reports/quick-wins-p-c1b-review.md`); THJ play-tested it: works.
**Not verified:** nothing open.
**Findings:** the lock also blocks the ability bar and End Turn behind an open tutorial (closes an old gap). The L reaction key is ATB-only and does nothing on FTP. THJ asked next for a short pause before a faction's turn when the previous turn ended on its own (not by End Turn), set per faction and independent of the banner.
**Status:** pause design proposed to THJ; then C2.

## 2026-10-22: Quick wins bundle P, C1c (turn-start pause after an automatic end)

**Built:** `FactionControllerBase.turnStartPause` (per controller prefab; AI 0.5 s, player 0), waited in `SwitchTurnIE` after the shared gap and before the banner, skipped when the previous turn was ended with the End Turn button (`EndTurnFromButton` marks it only when the request goes out; cleared on turn end and start). 4 EditMode tests for the rule. Commit `ff0a9f70f`. D-143.
**Verified:** compile clean; EditMode 521/522 (known red only); reviewer APPROVE (`reports/quick-wins-p-c1c-review.md`); THJ play-tested it: good.
**Not verified:** nothing open.
**Findings:** with the dev auto-player as the player faction, End Turn still gets the pause (`AIController.RequestEndTurn` skips base; backlog). Turn-switch holds added during the gap or pause aren't respected (pre-existing for the gap).
**Status:** C2 next.

## 2026-10-22: Quick wins bundle P, C2 (end-of-level waits)

**Built:** `CombatLevelRunHandler.endLevelDelayBeforeHudHide` / `endLevelDelayAfterHudHide` (0.25 s each, code defaults; scenes not edited) replace the two hard-coded 0.5 s waits in `EndLevel`. Commit `b0e58f6f6`.
**Verified:** compile clean; EditMode 521/522 (known red only); THJ play-tested it: good.
**Not verified:** nothing open.
**Findings:** level outros start with `IntroCutscene` (input off, grid fade out 0.8 s, HUD hide); that second HUD hide is instant. Saving `CombatLevelContainerScene` / `TestLevel` next time writes the two new fields (expected noise).
**Status:** C3 next (values, banner to the right edge, banner stops catching clicks).

## 2026-10-22: Quick wins bundle P, C3 (pace values, banner timing and position)

**Built:** AI hold 0.25 s; gap between faction turns 0.25 s (`CombatLevelContainerScene`, `TestLevel`); loading pad 0.5 s (`PreloadScreen`); banner 0.25 / 0.5 / 0.25 s (prefab and the scene's existing duration override), anchored to the right edge, shown (−16, −260), hidden (+760, −260); CanvasGroup with raycasts off. Commit `e2c9bbf68`. D-107, D-141.
**Verified:** EditMode 521/522 (known red only); THJ play-tested it: good.
**Not verified:** the final console read (the Unity MCP stopped answering after the last refresh); the loading pad (player builds only).
**Findings:** the banner root's `UIPanelAnimator` is unused (old top-centre positions left). The objectives panel may cover the banner's top ~20 px with three objectives. THJ asked next for a left/right option for the banner, and about a long pause between the last end-of-level dialog line and the end-level menu: the dialogue panel's hide animation (0.5 s, `DialogNodeSequence` waits for it) plus a hard-coded 1 s in `CombatLevelRunHandler.EndLevel` before `_uiManager.EndLevel`.
**Status:** banner side option and end-panel delay proposed to THJ.

## 2026-10-22: Quick wins bundle P, C4 (banner side) and C5 (end-menu delay)

**Built:** C4: `PhaseVisualsUI.side` (Left/Right, default Right) mirrors the authored right-edge layout at load; `MirrorX` with 3 EditMode tests in a new `Features/UI/Panels/Scripts/Editor/`. Commit `4c57f870f`. C5: `CombatLevelRunHandler.endLevelDelayBeforeEndPanel` 0.25 s replaces the hard-coded 1 s before the end panel. Commit `7d4cd90ca`. D-144.
**Verified:** compile clean; EditMode 524/525 (known red only); reviewer APPROVE (`reports/quick-wins-p-c4-c5-review.md`); THJ play-tested both: good.
**Not verified:** nothing open.
**Findings:** the end-of-level pause was the dialogue panel's 0.5 s slide-out plus the 1 s; now about 0.75 s. Reference of every pace timing written: `tech/pace-timings.md`.
**Status:** bundle P done. Doc updates still owed: `tech/core-systems.md`, `tech/combat-architecture.md` (banner no longer blocks, turn-start pause, End Turn → `EndTurnFromButton`, the EndLevel fields). (Done later on 2026-10-22.) **Branch note:** bundle P's commits are on `thj/quick-wins` (THJ checked it out at 10:27), not `main`.

## 2026-10-22: Feedback pass C1 (shake priority)

**Built:** `ShakeCameraEffect.priority` (default 0); a shake is skipped while a higher-priority one still runs; running priority and end time tracked in statics on `CameraEffectBase`, cleared by `ResetPlayModeState` and `Revert`; pure `ShouldSkip` / `NextRunning` with 11 EditMode tests. Commit `07f4e44fe` on `thj/quick-wins`. Plan `plans/2026-10-22-feedback-pass-tech.md` (D-146).
**Verified:** compile clean; EditMode 535/536 (known red only); reviewer APPROVE (`reports/feedback-c1-review.md`); THJ play-tested it: shakes look the same.
**Not verified:** nothing open (no asset uses a priority yet).
**Findings:** tracking isn't cleared on scene load (≤ 0.25 s carry-over, harmless); a future priority-2 additive shake over a priority-1 one would leave the latter unprotected early (only if sequence shakes get priority 2).
**Status:** C2 (kill feedback) next.

## 2026-10-22: Feedback pass C2 (kill feedback)

**Built:** `Features/Effects/KillFeedback/` (`KillFeedbackPresenter`, `KillFeedbackRules`, 10 EditMode tests): on `unitDied` outside the player's faction, a white flash (0.07 s hold, 0.07 s fade; blink killed first, default read after) and a stepped kill shake (`Kill_`/`Kill2_`/`Kill3_ShakeCameraEffect`, 0.04/0.05/0.06, 0.2 s, priority 1). Optional sting once per chain, left empty (THJ). `KillFeedback` object under `---Management---` in `CombatLevelContainerScene` and `TestLevel`. Commit `8d531ec64` on `thj/quick-wins`. D-146.
**Verified:** compile clean; EditMode 545/546 (known red only); reviewer APPROVE (`reports/feedback-c2-review.md`, one should-fix applied); THJ play-tested it: looks good, asked for slightly shorter and softer values (applied).
**Not verified:** the tuned values were committed on THJ's say-so without a second full play.
**Findings:** Dark Worm splits, a boss's `FakeDie`, reverted spawns and player-allied non-player factions also get the beat. No placeholder sting fits; a real kill sound is wanted.
**Status:** C3 (mini HP bar) next. `pace-timings.md` needs the kill-feedback rows (done).

## 2026-10-22: Feedback pass C3 (mini HP bar)

**Built:** `Features/UI/Panels/Scripts/MiniHealthBar/` (`UnitMiniHealthBar`, `MiniHealthBarRules`, 18 EditMode tests); a `MiniHealthBar` child on `UnitBase.prefab` under `Visual/UnitInfoHook` (world-space canvas, Overlay order 0, two Images); hidden while the info panel is up and when dead; damage chip 0.15 s hold, 0.25 s drain, computed from timestamps on game time; off on Deevoted and Lucy's decoy (no info panel). One green for all (D-147). Commit `616af0754` on `thj/quick-wins`.
**Verified:** compile clean; EditMode 563/564 (known red only); reviewer APPROVE (`reports/feedback-c3-review.md`, two should-fixes applied); THJ play-tested it: good.
**Not verified:** nothing open.
**Findings:** Unity's pending serializer fields on `UnitBase.prefab` and `Deevoted.prefab` were removed by hand and come back on the next save (noise). The bar draws over a neighbouring unit's sprite like the info panel.
**Status:** C4 (low-HP state and presenter) next.

**Follow-up (2026-10-22, `ee2613f59`):** bar length 0.25 of the footprint (THJ: "a bit more than halved"); canvas moved from Overlay to DynamicTop order 0, under the text pop-ups (order 10) and the info panel (order 1), above unit sprites and the sword/role/cover icons. Image pop-ups (Default, 0) now draw under the bar; tile arrows tie at DynamicTop 0. No bug behind "no visible change at 0.39": the fraction applies in `Awake`; Edit-mode views show the authored 83. The 0.25 length is not play-checked.

## 2026-10-23: Feedback pass C4 (low-HP state and heartbeat)

**Built:** low state on the mini bar for player-faction units (≤ 25%, alive, above 0 HP; crossing rule in `LowHealthRules`, partial `UnitMiniHealthBar.LowHealth.cs`), amber-red pulsing bar. `Features/Effects/LowHealth/` (`LowHealthPresenter`, `LowHealthCadence`): edge vignette generated in code on its own overlay canvas (order −1, raycasts off); crossing → 3 cycles; level start → one shared announcement as turn 1 begins (no banner on turn 1); selection → one cycle, once per member per player turn; each player turn start → one cycle after the banner (max 4 s wait); never stacks; unscaled time stopped at `timeScale` 0. Sound ids empty. `LowHealthFeedback` object in both scenes. Commit `31b8473d7` on `thj/quick-wins`. D-146 to D-148.
**Verified:** compile clean; EditMode 598/599 (known red only); reviewer FIX → fixed (lethal hit not a crossing; one sting per accepted announcement; live turn cleared on `turnEnded`), checked by the coordinator; THJ play-tested: triggers good, look retuned and re-tested good.
**Not verified:** Toba joining mid-level then crossing; resurrect paths (revived in place announces, full resurrect doesn't).
**Findings:** max-HP changes can cross without a hit (by design). Steady low-HP overlay deferred until after C5 (D-148).
**Status:** C5 (HUD glow, portrait tint, pouch bob) next; then ask THJ about the steady overlay.

## 2026-10-23: Feedback pass C5 (HUD low-HP signs)

**Built:** `UnitPanelUI.LowHealth.cs` (built in code, no prefab change) following the selected unit's mini bar low state: a blood-red overlay on the HP bar's empty track (`LowHealthTrack`, alpha 0.45, inside `Mask_Shape`, under the fill and text), a portrait tint from the bottom (alpha 0.5, fading two-thirds up), a glow around the bar that flashes only on the heartbeat (`LowHealthPresenter.BeatStrength`, steady alpha 0). Item-pouch bob once per selection for a low member with a healing item (`ItemEffectPreview.GetHealthIncrease`). Rules in `LowHealthHudRules` (tests); `BeatStrength` in `LowHealthRules`. Commit `403de3bf8` on `thj/quick-wins`.
**Verified:** compile clean; EditMode 606/607 (known red only, read from the results file); reviewer APPROVE (`reports/feedback-c5-review.md`, two should-fixes applied); THJ play-tested and tuned it (track overlay, live tint, glow only on beats): good.
**Not verified:** leaving a level with a low member selected (console clean expected).
**Findings:** `Mask_Shape`'s `Mask` has `showMaskGraphic` off; the bar's black comes from the frame art `Panel_Fat_0`. The bob plays while the panel slides in; a member who turns low while selected doesn't bob until reselected.
**Status:** feedback pass C1–C5 done.

## 2026-10-23: Dark Shaman heal C1 (ability and AI, data only)

**Built:** hidden tag `Kin.Dark` (`GTagSet`, `GTagRegistry`) on Dark Claw, Black Claw, Dark Worm, Dark Shaman; `Resources/UnitSpecific/Enemy/DarkShaman/Heal/`: effect (+10 × caster `Stat_DMG` on `Specs_Health`, clamped at max), preset (targeted Kin.Dark ally, not self, range 3 Manhattan, 1 AP, cooldown 2, camera focus, classed Ability), utility graph (valid ≤ 75% HP, score 3.5 + 2 × missing + 0.5 Leader); `Heal` clip and state (copy of `SpawnEnemy`, frame 14); fourth Shaman ability. Commits `2b8e4ea88`, `e81c20f59`, `2095e4eaf` on `thj/quick-wins`. D-150, D-151.
**Verified:** compile clean; EditMode 608/609 (known red; `AIRegressionTest` also flags the new graph and ability, no re-baseline); reviewer APPROVE (`reports/shaman-heal-c1-review.md`); THJ play-tested: good.
**Not verified:** AI log scores in numbers.
**Findings:** the HP-changed event reports the unclamped amount (C2 must use the real gain). Stunned/dormant dark allies can be healed (D-151). THJ's play session left six unrelated asset edits uncommitted (Mark–Lucy duo, Claw walks, Dom Swap, Lucy Cyclone).
**Status:** C2 (heal pop-up, next-targets filter) next.

## 2026-10-23: Dark Shaman heal C2 and the Lucy role fix

**Built:** C2: green "+N" on HP gains from abilities and items (real capped gain; `HealPopTracker`, `HealPopWindow` keeps gains during a running ability since animation-event heals report completion frames later; gains outside abilities dropped), `ec664b5fc`; next-targets panel lists only hostile units, `f4e9d9158`. Lucy (D-152, `reports/lucy-role-wrong-target.md`): ordered, locked attacker memory in `GUnit` (core) `b1848c5e8`; Lucy takes the action's target first, then an enemy that action hit, nearest first `4982d3b80`. All on `thj/quick-wins`.
**Verified:** compile clean; EditMode 653/654 (known red only); reviewer APPROVE on C2 and the Lucy fix (`reports/shaman-heal-c2-review.md`, `reports/lucy-role-target-fix-review.md`); THJ play-tested both: Lucy solved, +N numbers show (after the `HealPopWindow` fix).
**Not verified:** the Linda–Toba duo heal number path; a passive self-heal during an ability also pops.
**Findings:** the AI's recent-attack factor now reflects real recency (steadier revenge targeting). Hovering a Shaman still highlights the healed Claw's cell (`GUnit.SetFutureTargetsHover`, core; follow-up). An implementer recompile once landed during THJ's Play session (agents must check Play mode first).
**Status:** quick wins done; `thj/quick-wins` is 21 commits ahead of `main`, ready to merge (THJ). Docs: EN-11 "Dark Mending" in `enemies.md`, `core-systems.md` (GUnit attacker memory), glossary name. Open: the steady low-HP screen overlay (D-148), the GDD "Combat feedback" section (game designer), real kill and low-HP sounds.

## 2026-10-23: GDD mirror re-sync

**Built:** the "Miso — Game Design" Claude Doc brought up to `design/gdd/` and `glossary.md` at `50752ac`. Replaced the whole body of four tabs from the repo files: Combat rules (grid previews now Built, the Combat feedback section CR-44 to CR-53, Q12), Family systems (role zones post-merge labels, Q12; it had a half-done earlier sync), Enemies (EN-11 Dark Mending), Glossary (last synced 2026-10-16: enemy abilities and kin, low HP, dungeon safe rooms, canon table). Overview: the two "Checked" cells for Combat rules and Enemies. Tab headers rewritten as one "Checked against ..." line.
**Verified:** none of the five tabs had comments, so nothing was detached. The other tabs last changed in the repo on 2026-10-17 and match (spot-checked Toba).
**Not verified:** a line-by-line read of the rendered tabs.
**Status:** mirror in sync with `claude-handoff` @ `50752ac`.

## 2026-10-24: Enemy alert state (Unaware / Alerted)

**Built:** enemies of player-hostile factions start Unaware (a `Status.Unaware` tag the AI controller skips like Stunned) and wake by sight (a hostile stops within `Specs_Sight`, Manhattan through walls), noise (an ability affecting them, or a family ability within `Specs_AlertRange`) or spread (recursive, within the waker's alert range; start-alert units spread too). Woken in the family's turn: act next enemy turn; woken in the enemy turn: from the following one. Spawns follow the rule. Defaults sight 3, alert 2 (Masher sight 2), per-level bonus on `LevelAlertSettings`; `EnemyAlertSettings` for starts/always alert (bosses). Marker over sleeping enemies, staggered "!" on wake, Shift-hover draws sight and alert tiles while Unaware. 11 objective/boss levels start alert. Plus a core tag fix: tag sets link their own parents (IDs no longer depend on the registry's copy). Commits: `3378acaca` rules + tests; `b8ea2ff58` tag-set parent links (core, D-166); `2bea515d5` sight/alert attributes; `923ab777b` Unaware tag + AI skip query; `0d3427685` tracker, rules, visuals, settings, LevelBase, tests; `af04281a7` Shift-hover range preview; `dc64f974a` boss and level start-alert data. Decisions D-154 to D-167. Plans: `plans/2026-10-23-enemy-alert-state-design.md`, `plans/2026-10-23-enemy-alert-state-tech.md`.
**Verified:** EditMode 738/739 in batchmode before the tag fix (known red only); review APPROVE on every chunk and fix round; THJ's play checks 2026-10-24 (first: sleep/wake in `LevelE3-C1`; second, after C4 and the tag fix: "works great").
**Not verified:** the EditMode count after the tag fix (THJ ran it with the play check; count not reported); every stop path in play (pushes, teleports, Dance, Command); Worm splits; the corruption pool.
**Findings:** derived sight (walk + attack) was unreadable in play, replaced by attributes (D-164). The tag registry desync was pre-existing and editor-only.
**Status:** done on `main` (not pushed). `thj/home-test` needs it when it takes `main`.

## 2026-10-26: Merge main into thj/home-test

**Built:** `ee126a407` "Merge main into thj/home-test" brings `main` @ `a1483f0b9` into home-test @ `46c9a88ab` (128 commits in, 59 on home-test). Six conflicts were resolved as decided in D-181 and D-198 (event bus, play-mode resets, `FactionRoleHandlerBase`, `CheatHandler`, `GlobalSettings`, `GTagSet`). Report: `reports/merge-main-into-home-test.md`; review: `reports/merge-main-into-home-test-review.md` (clean; one question escalated to THJ, which became D-199).
**Verified:** EditMode 1138/1139 (known red only); THJ's play check of Home and a sortie: "looks good". After opening Unity there was no `GTagRegistry.asset` rewrite.
**Not verified:** a Masher level on home-test (THJ couldn't find one; the names are now known); losing a Home attempt.
**Findings:** main's alert tracker runs in every sortie (D-199: home-test's copies of main's start-alert levels get the setting). The `Home` tag group's fields are wrong (D-182). There are private plan IDs in `FactionControllerBase.cs` and `HomeFromHomeTags.cs` (pre-existing).
**Status:** merged, not pushed. Next: the sortie start-alert commit, then the Home tag fix.
**Follow-ups (same day):** `5d19e30cf`: `LevelAlertSettings.allEnemiesStartAlert` on the three sortie copies of LevelM2-C1 (`LevelM2-C1 1`, `Queen's Chamber`, `Drowned Shrine 2`; THJ kept Shrine 2). `1d91791b7`: the `Home` tag group is now a plain hidden parent. EditMode 1138/1139 (known red only). Report: `reports/home-test-sortie-alert-and-tag-fix.md`. Not play-checked yet: the three levels starting alert.

## 2026-10-27: Linda's Quiver C1–C3 (`thj/linda-quiver`)

**Built:** quiver of 4 (spend per shot, landing on last enemy hit or end of range, never lost), grounded stacks with a locked state, pickup by any squad member with a non-blocking hand-back beat, Recall (1 AP, cooldown 2), Cyclone split and Mark's catch conserving arrows. No core code except one reset line. Plan `plans/2026-10-26-linda-quiver-tech.md`; decisions D-241 to D-256.
**Verified:** compile clean; EditMode 848/849 (known red only; its message gains one accepted line for the Recall preset, D-255); 106 quiver tests; reviews APPROVE per chunk.
**Not verified:** readability UI (C4) and combat log (C5) not built.
**Findings:** THJ play check: working, fun, needs work; a shot arrow sometimes seemed to land nowhere (under investigation).
**Status:** committed `c6aade3c9`, `502902b38`, `f6dd15a0f`, `dd95002f8`; not pushed.

## 2026-10-27: Linda's Quiver C4 readability (`thj/linda-quiver`)

**Built:**
- arrow pips under Linda and on her panel
- empty-quiver badge, and her zone hidden at 0
- "Arrows 3 > 2" on the Watch prompt
- grey reasons
- landing marker
- "+N arrows" on the move preview
- Encore return lines
- a "+N" return cue (Mark's glow on a catch)
- a clearer grounded/locked look with a count badge
- an arrow with nowhere to land goes back to the quiver
- Encore title

Core: one additive `PlayerController` hook (D-270). Core never imports Linda (D-272).

**Verified:** THJ's Test Runner gave EditMode 893/894 (known red only). Review APPROVE. THJ played it: works.

**Not verified:** sizes; THJ finds most elements too big and leaves it for the final decision.

**Status:** committed `c7081b76c`, `741ac9dd2`, `6e3d92517`, `886f32e88`, `7ad75622c`; not pushed.

## 2026-10-27: Mark's QTE catch and play fixes (`thj/linda-quiver`)

**Built:**
- Linda's arrow freezes at Mark during a quick-press prompt. A press sends it back to the quiver, and a return arrow stops on Linda. A decline lets the same arrow carry on.
- The prompt is faster (per-profile wait and show speed, core QTE).
- A path sweep stops a long frame skipping the catch.
- Lucy follows up only on real damage (core).

Fixes today's double damage past Mark.

**Verified:**
- EditMode passes (THJ's Test Runner; known red only).
- Reviews APPROVE.
- THJ played every step.

**Not verified:** balance of the return re-hits.

**Findings:**
- The trail kinks where the arrow snaps up to Mark's catch point.
- Linda's arrows fly on a slope (pre-existing).

**Status:** committed `d5919c384`, `53272e30d`, `98f1adf80`, `81bd8d584`, `680bd4726`, `91f40e903`; not pushed. Lucy's fix is also needed on `main`.

## 2026-10-28: Linda's Quiver play-fix round (`thj/linda-quiver`)

**Built:**
- A caught arrow freezes on its own path (no V).
- The pips draw under other units' HP bars.
- The level-start NullReferenceException is gone.
- The arrow board lives under its level, so the quiver survives restarts and map entry.
- The level-flight attempt was reverted (D-279).

No core code.

**Verified:** EditMode 938/939 (THJ's Test Runner; known red only). Reviews APPROVE. THJ played restarts, map entry, the catch and the pips.

**Not verified:** -

**Findings:** occasional misses during lag (a claw mid-path, a far worm) are the physics-hit weakness, filed as `arrow-hits-by-grid` (main, core). Core follow-ups filed: `combatlevel-playerfaction-before-init`, `level-start-objects-in-loading-scene`.

**Status:** committed `9ba8c9478`, `6d2388bbf`, `921294cbf`, `4a880f27c`; not pushed.

## 2026-10-28: Linda's Quiver C5, combat log lines (`thj/linda-quiver`)

**Built:** "Quiver:" lines for:
- the count at level and round start
- spends, with the firing ability
- landings
- pickups: who and how
- Encore
- catch returns
- Watch prompts, with the count

Core gets one additive, generic `CombatLog.AddCustom`.

**Verified:** EditMode 947/948 (known red only). Review APPROVE. THJ checked a level's log.

**Status:** committed `9b104608b`, `19e02893a`. The quiver plan's chunks are all done.

## 2026-10-28 · Quiver strip-down round (thj/linda-quiver)

**Built:**
- the strip-down to one quiet layer: no arrow text, a HUD quiver on her portrait, grounded arrows in the new art, a ghost arrow when aiming, curved Encore lines;
- smaller pips and +1 cues;
- kinematic bodies on Linda's arrows;
- a core `Projectile` sweep with a per-projectile hit set;
- combat log annotation (a quiver count suffix on action lines).

**Verified:** EditMode 955/956 (known red only). Each part had review APPROVE. THJ played the round check ("think they work").

**Not verified:** a 10 fps column test as a separate step (THJ's overall OK covers the round).

**Findings:** THJ wants deeper feedback in the same layer. See `plans/2026-10-28-quiver-feedback-pass.md` (D-301 to D-303).

**Status:** committed `d2a377569`, `3fdbb08f1`, `ff739b5ae`, `018b1e5a1`, `039697fe2`, `79ca381e8`. `main` still needs the sweep, the bodies and Lucy's fix ported (THJ's call).

## 2026-10-29 · Quiver feedback pass and polish 2 (thj/linda-quiver)

**Built:**
- **Feedback pass:**
  - Encore costs 2 AP.
  - The HUD quiver comes from THJ's hand-placed prefab, with the empty tint, the lift, the punch at 0 and the gain glow.
  - Her arrow row shows on her Shift panel, and a crossed arrow appears at 0.
  - One grounded arrow per tile, with `xN`.
  - Thinner Encore lines with the threat-line shine.
- **Polish 2:**
  - Every arrow ability drives the HUD feedback.
  - `xN` moved closer to its arrow.
  - John's and Toba's primary kills hand the arrows back.
  - The move-then-shoot ghost.
  - A dark outline on the HUD quiver.

**Verified:**
- EditMode 980/981 for the feedback pass, then 994/995 for polish 2 (known red only).
- Review APPROVE on both rounds.
- THJ played both rounds.

**Not verified:** none.

**Findings:**
- In PerUnit mode any ability can be cast at 1 AP (`ap-overspend-perunit`, D-304).
- Allied Toba doesn't hand back arrows (D-310).

**Status:** committed `661890964`, `51954e2c6`, `45cb29d76`, `d8651dd3c`, `7c6f5e57c`, `99ae9ff09`, `ebbd4fe68`, `e201fb245`, `26371cc8d`, `19f75ff0d`.

## 2026-10-29 · Ability pause-frame skip fix (core, thj/linda-quiver)

**Built:** the animation catch-up stops at the target-selection pause, and the activation frame waits for confirmed targets (D-311).

**Verified:**
- EditMode 1009/1010 (known red only).
- Review APPROVE: no turn lock on cancel, hit, restart or replay.
- THJ played Explosive Arrow at 10 fps: no stray fire.

**Not verified:** the original crash was intermittent, so its absence is weak evidence.

**Findings:** follow-ups for THJ:
- `_paused` stays set into a later `Play`, so a hurt or death clip played while held can freeze.
- A long hitch can skip the activation frame for any ability.
- A held ability stays set across the end of the turn.

**Status:** committed `8293bd358`. Needs porting to main.

## 2026-10-29 · Quiver switch, size stat, Encore in kits, projectile cap (thj/linda-quiver)

**Built:**
- Core: `Projectile` caps flight progress at 1 (D-317); `GlobalSettingsSO.lindaQuiverEnabled`, default on (D-314).
- Quiver size from the new `Stat_LQuiverSize` attribute on Linda, base 3, fallback serialized 3 (D-316, D-319).
- Switch off: no quiver at all, Encore hidden from her bar, Mark's catch sends a damaging copy back (D-315, D-320).
- Editor tool Tools > Levels > Linda > Add Encore To Custom Kits; run on 8 levels.

**Verified:**
- EditMode 1045/1046 (known red only, message unchanged: CHECKS 710 FAILURES 39).
- Review APPROVE.
- THJ played the 9-step check: all fine.

**Not verified:** none.

**Findings:** `LevelLindaJohn-C1` still lacks Encore (THJ's local edits). A Workshop quiver item would be an `EquipmentSO` with an Additive +1 modifier on `Stat_LQuiverSize`.

**Status:** committed 0424e80b8, 012790d11, 8070b76a0, 214d8325e, 55cde5ce5. The projectile cap needs porting to main.

## 2026-10-29 · Swap ends a move (core, thj/linda-quiver)

**Built:** `AEffectSwapper` raises `unitEndMoving` for both live swapped units after a successful swap (D-322), so Toba's swap can trigger Linda's Watch. Edges allowed: two Watches from one swap, and Watch on an enemy swapped with Linda (D-323).

**Verified:**
- EditMode 1045/1046 (known red only, unchanged).
- Review APPROVE.
- THJ played the 7-step check: all pass.

**Not verified:** no EditMode test (the swap coroutine needs a grid, VFX and the event bus).

**Findings:** Papa's Shelter now refreshes when Lucy or John is swapped (was missed). The header comment in `EnemyAlertTracker.Events.cs` doesn't list the swap yet.

**Status:** committed `e76b5da70`. Needs porting to main.

## 2026-10-29 · Encore in LevelLindaJohn-C1

**Built:** the level added to `EncoreKitTool.Levels`; THJ ran the tool.

**Verified:** EditMode 1045/1046 (known red only); EncoreKitTests pass.

**Not verified:** none.

**Findings:** none.

**Status:** committed `8c2e8617c`. Every level that overrides Linda's kit now has Encore.

## 2026-10-29 · thj/linda-quiver merged into main

**Built:** `main` fast-forwarded in place to `8c2e8617c` (47 commits). No checkout, no working-tree change, not pushed.

**Verified:** last EditMode on that commit 1045/1046 (known red only). `main` = `thj/linda-quiver` (0 files differ).

**Not verified:** no fresh run after the merge (no files changed).

**Findings:** the quiver is on in `main` by the code default.

**Status:** merged locally; pushing is THJ's.

## 2026-10-30 · main merged into thj/home-test

**Built:** merge commit `93d414dd5` (`main` @ `e5506c1e8` into `thj/home-test` @ `1d91791b7`). No conflicts; files changed on both sides and auto-merged: `CameraHandler.cs`, `GlobalSettingsSO.cs`, `PlayModeStaticReset.cs`, `FactionRoleHandlerBase.cs`, `Unit_Linda.prefab`, `Unit_Mark.prefab` (stat override indices checked: main appends at the end, home-test edits index 2/3).

**Verified:** clean merge; uncommitted files carried over unchanged.

**Verified (later):** EditMode 1441/1442 after `cfa297659`, the Encore description test fix (the test still required the placeholder tag); cherry-picked to `main` as `194bd566b`.

**Not verified:** a play smoke test on home-test.

**Findings:** the quiver is on in home-test by the code default.

**Status:** merged locally, not pushed.

## 2026-10-31 · Onboarding structure C1: opening mission graph (thj/onboarding)

**Built:** four placeholder missions (the Hearth, The River, The Ridge, The Trail) on existing levels; mission graph Hearth (initial) → River, Ridge → AND → Trail → M4, with M1, old M2, both M3s and M5–M7 removed from the graph (assets kept); New Game starts the Hearth; Mark unlocks after it; four world-map pins re-pointed, the M3 Mark Intro, M6 and M7 pins hidden; 10 graph tests. Commits `38bc7db73`, `bb9982c87`, `f36da02f8`.

**Verified:** review FIX then fixed (`reports/onboarding-c1-review.md`); EditMode 1055/1056 (known red only); THJ's play check after a save reset: all confirmed.

**Not verified:** nothing open from the C1 list.

**Findings:** five Home stations, the Family tab and M4's HomeState idles stay locked until C5; old-mission tutorials unreachable; The Ridge's placeholder level has one spare placeholder; graph-reading editor tools (Quick Level Loader, the level's Load Level button) no longer list the removed missions' levels. Dry-run merge with `thj/home-test` conflicts on `Game Data.asset` and the Home scene (`tech/onboarding-merge.md`).

**Status:** committed, not pushed. Next: C1b merge-safety builder (D-339), then the grid-to-level tool.

## 2026-10-31 · Onboarding C1b: merge-safety builder (thj/onboarding)

**Built:** `Tools › Onboarding › Apply / Check Opening Setup` (editor-only, `Features/Onboarding/Editor/`): one table of mappings; re-applies the opening graph (keeps nodes it doesn't own, clears other start flags, warns on missions left without prerequisites), New Game's first mission, Mark's unlock, the world-map pins (by mission) and Mark's select button and Upgrades tab; stops before writing over unsaved edits. 8 tests. Commit `509a634dc`.

**Verified:** run on the pre-C1 copies of the five files, it reproduced C1 (36 changes, a second run 0); Apply on the project is a no-op; review FIX then fixed (`reports/onboarding-c1b-review.md`); EditMode 1063/1064 (known red only).

**Not verified:** a run on `thj/home-test`'s real files (only reasoned through by the reviewer); the proof wasn't re-run after the fix round.

**Findings:** home-test adds 8 sortie nodes with no edges (open from the start); its Home-mode world map shows the Home sim's missions instead of the pins; its Family tab has no unlock mission. All in `tech/onboarding-merge.md`.

**Status:** committed, not pushed. Next: the grid-to-level tool (D-337).

## 2026-10-31 · Grid-to-level C1: parser and builder core (thj/onboarding)

**Built:** editor-only `Core/Levels/Editor/GridToLevel/`: grid-block parser, code palette (the `level_to_grid.py` table; default template `LevelM1-C2`), builder (template loaded and saved to the output path, template grid content and extras stripped, cells under the Grid's Tilemap, units under each cell's occupant root at the footprint centroid), 20 tests. Commit `81897bb7c`.

**Verified:** chunk 24 builds 37 cells and 6 units on the right tiles, no trigger left, no missing references, round trip matches; all 48 blocks in the catalogue and the onboarding levels plan parse; review APPROVE (`reports/grid-to-level-c1-review.md`); EditMode 1083/1084 (known red only).

**Not verified:** a built level played (C3 adds Play; the verification set comes after C3).

**Findings:** three onboarding templates carry a `LevelStartFPFiller` pointing at their own heroes (would throw at level start once stripped): C2 rebinds it (D-342). The plan's round-trip and cell-parent wording corrected.

**Status:** committed, not pushed. Next: C2.

## 2026-10-31 · Grid-to-level C2: level settings, palette asset, camera bounds (thj/onboarding)

**Built:** camera boundary tool's per-prefab step extracted (`eb40ebcd5`, behaviour unchanged); `GridLevelPalette.asset` with the code table as fallback; `level` lines applied (tier, Standard when unset; all-start-alert; origin; template); camera bounds after save; a template's level-start FP filler pointed at the placed player units (D-342); C1 review fixes (`459f41428`).

**Verified:** a tier-tutorial, alert-all probe reads back "enemy tier Tutorial; all enemies start alert: yes"; bounds match the boundary tool; review APPROVE (`reports/grid-to-level-c2-review.md`); EditMode 1094/1095 (known red only).

**Not verified:** a built level played.

**Findings:** three small should-fixes go to C3.

**Status:** committed, not pushed. Next: C3.

## 2026-10-31 · Grid-to-level C3 and level loading fixes (thj/onboarding)

**Built:** Build Level From Grid window (preview, rebuild confirm, Open, Play; `24bfcea3e`). Level loading fixes (`32f532e49`): the loader read the level's id and prefab path after opening the preload scene, which unloaded the prefab asset, so toolbar/inspector/window Play fell to the main menu; now captured first; `UnpackID` null-safe; unlisted levels play in a sandbox; a Prefab Mode copy loads as its saved asset. Level toolbar dropdown (`29cad27cb`): folder submenus, ★ favourites, `Recent/` (5), per machine.

**Verified:** EditMode 1109/1110 (known red only). Reviews: C3 APPROVE; loading fixes FIX → APPROVE. THJ played `GB_24-nook` and the paths: all good.

**Not verified:** a scripted load right after a play-stop once lost the handler and went to the main menu (pre-existing subscribe pattern; hardening is a follow-up).

**Findings:** built levels kept the template's `InitialCameraPosition`, so the opening view was off; fixed in the camera start step (in progress). The five `GB_` levels are not committed yet (they wait for it).

**Status:** camera start with `miso-implementer`.

## 2026-10-31 · Grid-to-level camera start (thj/onboarding)

**Built:** builds place the Camera's `InitialCameraPosition` (whole level if it fits one screen at the default zoom, else pulled toward the player units, clamped in the boundary); `level camera x,y` override; **Tools › Levels › Place Camera Start** for existing prefabs. Placed on the five `GB_` levels. Commits `9d3ac5623` (tool + tests), `652f2075e` (levels).

**Verified:** EditMode 1126/1127 (known red only); 17 camera-start tests. Review FIX (global `SaveAssets`, Undo, locator parent, grid source, test precision, camera-tile warning), fixed. THJ played the opening views: good.

**Not verified:** Place Camera Start's Prefab Mode close-and-reopen round trip (saved values checked only).

**Status:** grid-to-level tool done. Next per D-337: structure C2.

## 2026-10-31 · FP 0/0 in sandbox levels and Play hardening (thj/onboarding)

**Built:** a level played outside any mission got an empty sandbox roster, so the family time points pool was 0/0 and Roles and pass-by did nothing (exposed by `32f532e49`, which made unlisted levels play in a sandbox). The sandbox roster now holds the placed player units plus the placeholder picks (`fa6af3fab`, with `LevelFastForwardRosterTests`). Play hardening (`08cdf7035`): the quick-load keys are written right before Play starts and cleared after an edit-mode recompile; the stale stop handler can't unsubscribe a new run.

**Verified:** EditMode 1130/1131 (known red only). Review APPROVE, fix round done. Implementer: `GB_24-nook` 10/10 for John, Lucy, Linda; keys cleared after stop; plain Play reaches the main menu. THJ played the GB levels and a normal mission: all good.

**Not verified:** a Play Unity refuses, and a load right after a play-stop (both rare, couldn't be forced).

**Status:** committed, not pushed. Next per D-337: structure C2.

## 2026-11-01 · Onboarding structure C2: memory rules (thj/onboarding)

**Built:** `LevelStartRunUpgradeGrant` (a level grants run upgrades at level start; mission lifetime; `c772bbf34`). `LevelXpChecker` (every XP source of a level or mission), grid tool lines `level xp none` (zero placed enemies' XP as instance overrides, warn on what's left) and `level fp full` (add or set a start filler to full) (`16eee4aad`). Per D-344 the old M1 placeholder levels are untouched; C3 applies the rules to the real memory levels.

**Verified:** EditMode 1155/1156 (known red only). Review FIX (checker missed spawning hazards, nested summons, reward/pickup XP; `fp full` was skipped; Unity null check) → fixed → APPROVE, plus three small fixes. THJ checked a build with both lines: good.

**Not verified:** the grant firing in a real level in Play.

**Findings:** spawned enemies' XP can't be zeroed per spawn without core code (plain `Instantiate`); the default template has no FP filler, so FP carried over between segments without `level fp full`.

**Status:** committed, not pushed. Next: structure C3 (memory levels and sequences); THJ's spawn call first.

## 2026-11-01 · Onboarding structure C3a: the Hearth memory levels (thj/onboarding)

**Built:** `HiddenLevelUnits` + `RevealUnitsSequence` (placed units start out of play; a level sequence reveals a group the way a spawn does) and the grid line `level hidden [group] x,y …` (`3c99b3ee6`). The four memory levels `GB_m1-linda`, `GB_m2-lucy`, `GB_m3-john`, `GB_m4-mark` from their blocks (tutorial tier, alert, no XP, full FP; per-unit HP by hand; hidden cue Claws in segments 2 and 4; Wolf/Ryker scenery for the mother and cub) (`a161e0956`). The Hearth plays them in order with no completion XP, plus a mission-wide no-XP test (`9ace80c28`). D-345: no spawned enemies; D-346: reveal route.

**Verified:** EditMode 1172/1173 (known red only). Review FIX (a second reveal could revive dead Claws; deactivate the unit's own object; no-cell/no-faction guard; parser edge cases) → fixed → APPROVE. THJ play-checked the four levels and a new game into the Hearth: good.

**Not verified:** a reveal at runtime (no reveal sequence asset until C3b).

**Findings:** "defeat every enemy" counts only units in play, so segments 2 and 4 can be won before their reveal until C3b gives them their stages. Hand edits after the build (HP factors, Wolf/Ryker) live in the prefabs; a rebuild loses them.

**Status:** committed, not pushed. Next: C3b (sequences and stages); open: segment 4's revealed Claws after the mother falls.

## 2026-11-01 · Onboarding structure C3b segment 1: Linda's memory scenes (thj/onboarding)

**Built:** `GB_m1-linda`: Margaret's opening line and two panels (move and AP; Watch, "Each shot spends an arrow."), one win stage (all enemies dead or `TurnReachedLOCondition` turn 2, so it ends as turn 3 starts; HUD "Turns left in the memory"), end = punchline → `FadeOutGridSequence` → Hearth cutaway over a placeholder still → `OutroCutsceneKeepGridHidden`. Assets in `Resources/Sequences/Hearth/`; Tools > Onboarding > Wire Memory 1 (Linda) re-applies the wiring after a grid-tool rebuild (HP untouched). Commit `848a67fd2`. D-347: segment 4's revealed Claws stay and fight.

**Verified:** EditMode 1175/1176 (known red only, checked by name). Review APPROVE + four small fixes. THJ play-checked: good.

**Not verified:** —

**Findings:** `[PLACEHOLDER]` shows on screen (only barks strip it; `conventions.md` says otherwise). Margaret has no character asset (Narrator + "Margaret:"). Each memory level is its own scene, so segment 2 needs a hide-then-fade-in start for the grid fade-in. Home open/close states wait for a HomeState asset. Unity reimport wrote small diffs on `GB_m2/m3/m4` (left unstaged).

**Status:** committed, not pushed. Next: segments 2-4.

## 2026-11-01 · Onboarding structure C3b segment 2: Lucy's memory scenes (thj/onboarding)

**Built:** D-348: no `[PLACEHOLDER]` tag in dialogue/panel asset text; Linda's text untagged, Watch panel image fixed (old guid pointed at nothing), wiring helpers shared (`911a5def2`). `GB_m2-lucy`: grid hidden at start (`GridVisualSequence` duration 0) and faded in under Lucy's opening line; stage 1 (2 dead or turn 2) → input + HUD off, camera to room 2, `RevealUnitsSequence` reveals the three hidden Claws, "Then ten more!" / "Three.", camera back to the opening view, input + HUD on; stage 2 all dead or cap (counts from stage 2's start); end as segment 1. Tools > Onboarding > Wire Memory 2 (Lucy) (`59103e227`).

**Verified:** EditMode 1183/1184 (known red only). Review FIX (commit grouping; HUD stale during the reveal; camera back on Lucy) → fixed. THJ play-checked: good, including the first live reveal.

**Not verified:** —

**Findings:** a stage's turn cap counts from that stage's start. Segment 2's lines follow the levels plan, not the narrative draft; its punchline is a borrowed Cyclone bark. `GB_m1/m3/m4` still carry Unity reimport diffs (unstaged).

**Status:** committed, not pushed. Next: segments 3-4.

## 2026-11-01 · Onboarding structure C3b segment 3: John's memory level (thj/onboarding)

**Built:** `GB_m3-john`: Claws visible beside the sisters (1,1 2,2 6,2 7,1); player turn 1 caps AP (John 1, Linda and Lucy 0) with `TurnStartActionPointLimit` (`8a443d66c`); Shield Up pulses via `GuidedAbilityHint` (`ba7d19e66`); grid fade-in, John's lines, Shield Up panel; win 3 dead or turn 3; end exchange, grid fade, Mark and Margaret cutaway; Wire Memory 3 (John) (`29cbcd7ed`). Grid tool places camera bounds and start before its single save (`3153906dd`). Decisions D-349 (Claws arrive hidden, dropped after play) and D-350.

**Verified:** EditMode 1200/1201 (known red only), run twice by the implementer and once by the coordinator. Reviews: FIX → fixed (hint lifecycle); APPROVE (arrive version); APPROVE + small fixes (redo). THJ play-checked: good.

**Not verified:** John's Walk range (stat not in assets); auto-select at turn start if unit introductions are off.

**Findings:** first layout: the sisters' openers and Roles killed Claws before John's Role; the empty-board version let everyone wander. The `m_LockCount` assert came from the grid tool reopening a just-saved prefab during reimport. Kill barks need a hand-built bark graph. A sequence can't fire an ability (segment 4 uses the grant + hint).

**Status:** committed, not pushed. Next: segment 4.

## 2026-11-01 · Onboarding structure C3b segment 4: Mark's memory level (thj/onboarding)

**Built:** `GuidedAbilityHint` first-turn window (`3835af7f6`). `GB_m4-mark` (`1bf976b13`): grid fade-in, Mark's lines, Mark walks 14,2 → 13,2; `LevelStartRunUpgradeGrant` with the Bloom upgrade, Cyclone and Bow hints on turn 1, Chained Assault hint on turn 2; stage 1 (seven dead or turn 3) → mother's scene: camera to the ledge, the two hidden Claws revealed (stay and fight, D-347), lines, the mother's fall (rotated Wolf copy via LSB), the cub's line, camera back; stage 2 a Bergson on 6,9 / 7,9 / 8,9 (goal highlight); grid fades on the win; Hearth close. C3a hand edits kept (no grid-tool rebuild). Wire Memory 4 (Mark).

**Verified:** EditMode 1210/1211 (known red only). Review APPROVE + three small fixes. THJ play-checked: good.

**Not verified:** Bloom absent in The River at runtime (cleared on mission enter/quit in code).

**Findings:** Chained Assault's radius is 5 in data (plan said 4). The Wolf placeholder has only Stand/Move. Not done: Home open/close states, M4-4 to M4-7, optional FTP refill.

**Status:** committed, not pushed. **Structure C3 done.** Next: C4.

## 2026-11-02 · Onboarding structure C4a: The River (thj/onboarding)

**Built:** C4-0 risk check (`reports/onboarding-c4-0-check.md`). `GB_s1-river` from the `s1-river` block (Tutorial, default alert): sleeping clearing Claws, Archers on sealed islands. Wire Search: River: start (Lucy's line, pan to the clue and back, Lucy's Role panel with her follow-up clip, "Stay by me."), placeholder clue props, end close-up; shared once-per-save "first sleeping enemy" panel via `SequencePlayHandle` on `levelStarted` (`PlayJustOnce` persists in the save only when played directly). `MS1 - The River`: initial level, Gold 20 + Timber 1 + Fabric 1 fixed, XP 30, completion gold 0. Commit `3289158db`. Decisions D-351, D-352.

**Verified:** EditMode 1222/1223 (known red only). Review APPROVE + fix round (prop sorting, re-run noise, the panel, Lucy's image). THJ play-checked: good.

**Not verified:** —

**Findings:** Catch & Return was locked by an unlockable (D-352 opens it). The panel's sight-tile beat needs a small new sequence (`EnemyAlertTracker.TryGetUnawareRangeTiles`, `GridCell.SetShiftPreview`). No bark condition for distance or arrow count.

**Status:** committed, not pushed. Next: C4b.

## 2026-11-02 · Onboarding structure C4b: The Ridge (thj/onboarding)

**Built:** Catch & Return open by default (`a7320be82`, D-352; Mark's tree node shows owned). `SleeperSightBeatSequence`: the shared sleeping-enemy panel lights the nearest sleeper's sight tiles for 1.5 s (`eda1d6df6`). `GB_s2-ridge` from the `s2-ridge` block, Wire Search: Ridge: enemy turn first (D-353), rush pack awake at start, gauntlet asleep at the Claw's own HP (9.6 in play, D-354), Mark's Counter panel, the shared panel, clue props on 13,1 and the end close-up; `MS2 - The Ridge`: Gold 20 + Steel 2 fixed, XP 30 (`51f109672`).

**Verified:** EditMode 1240/1241 (known red only). Review APPROVE + small fixes. THJ play-checked twice (the first found the player-first rush too easy and the gauntlet Blitz-able): good.

**Not verified:** —

**Findings:** Linda's arrow has no per-hit falloff without `RU_LindaArrowDamageDecay` (an early report said 0.9). Shift preview and the sight beat share a cell flag (cosmetic). The implementer overwrote `GB_s1-river` with its committed version twice to drop reimport noise; told not to without THJ's yes. John/Lucy levels re-serialize `animationEvents` overrides on save.

**Status:** committed, not pushed. Next: C4c The Trail.

## 2026-11-02 · Onboarding structure C4c: The Trail (thj/onboarding)

**Built:** `level deploy x,y` grid line: a `Unit_Placeholder` slot per tile for the roster's free pick, replacing a drawn hero with a warning (`6184486d4`). `Unit_DarkClaw_StartsAlert` variant (`c4f85e804`). `GB_m2-trailhead`, `-blood`, `-tracks`, `-pile` (Early tier, Lucy + Linda + deploy slot) and Wire Search: Trail: trailhead drains FTP and wins on the exit tile; both routes drain FTP and share a once-per-save Pass-by panel (D-355); blood gully Claws 12 / side gully 16 HP; tracks Encore cue on both ledge Archers dead; pile items panel, "Search the pile." stage, rear wave of 2 alert Claws on 0,6 / 0,5 at turn 2, tally and the pick's line via the generic slot. `M2 - The Trail`: trailhead → blood | tracks → OR → pile, Health Potion 2 + Family Trinket 1 (`d72204178`).

**Verified:** EditMode 1265/1266 (known red only; `AIRegressionTest` now 41 inner failures, the variant adds two unit-catalog entries). Review APPROVE + fix round (pile objective visible, route drains, tests, deploy on hidden tile). THJ play-checked both routes: good after two fixes.

**Not verified:** River/Ridge sleeping-enemy panel after the shared `WirePlayOnLevelStart` refactor (tests pass; not replayed).

**Findings:** The rear wave threw `KeyNotFoundException` (empty `intervalFaction` on `GUnitSpawnManipulationAction`; the registry resolves it unconditionally); fixed in data (`Bergsons`). An empty `ReferenceableEntityRef` throwing in `ReferenceableEntityRegistry.ResolveEntity` is a core hardening candidate. One flaky `m_LockCount == 0` grid test while the Unity plugin was disconnecting. The implementer edited scripts during Play mode once. Not built: "stays home" line. M2 XP/Gold left at 40/5.

**Status:** committed, not pushed. **Structure C4 done.** Next: C5.


## 2026-11-02 · Onboarding C5a: M4 squad pick + Mark's weapon slot (`thj/onboarding`)

**Built:** M4 roster Lucy + Linda fixed, 1 free pick (John or Mark, Toba excluded); John's placed unit in M4's 7 levels replaced by a deploy slot (editor tool Tools > Onboarding > Apply M4 Squad Slots, idempotent); `Level2-C2` stale decision entry removed; `Level2-C3-2` FTP filler = Linda, Lucy, Toba; Mark gets a RightHand socket. Commits `8826a11f1`, `cafb8de97`, `f6648ed08`. Plan `plans/onboarding/2026-11-02-onboarding-c5-home-visits.md`.
**Verified:** compile clean; EditMode 1273/1274 (known red only); review APPROVE after two fix rounds; THJ played M4 with John and with Mark.
**Not verified:** Wrist Wrap equip on Mark in the Workshop (Workshop locked until C5b).
**Findings:** `Level3-C1`'s hero HP overrides (150–320) use pre-rename attribute field names and are ignored (D-363; backlog sweep). Mark has no default equipment.
**Status:** C5a done; C5b next.

## 2026-11-02 · Onboarding C5b: Home visits as data (`thj/onboarding`)

**Built:** Searching HomeState on Hearth/River/Ridge/Trail; Workshop opens after River or Ridge with a once-per-save page; Grandma Table after both; Family tab after The Trail; Bookshelf, Training Field, Cooking Cabinet after M4; Trail clue scene (initiation, play once) and Yard stub (completion). Builder step `OnboardingOpeningSetup.Stations.cs` re-applies the station locks, Family tab and Workshop page; Tools > Onboarding > Wire Home Visits; 15 tests. Commits `67b07c7f8`, `b2659da27`, `cb85c30fe`.
**Verified:** compile clean; EditMode 1288/1289 (known red only); review APPROVE after two fix rounds; THJ played Hearth → River → Ridge → Trail from a reset save.
**Not verified:** Ridge-first order by THJ (covered by tests).
**Findings:** Mark's Wrist Wrap of Power can be upgraded in the Workshop but doesn't equip or doesn't show as equipped (the data-level `Equip` test passes); under investigation. Home scene save re-adds nine empty `GlobalEventBus` fields (known noise, committed).
**Status:** C5b done; Wrist Wrap bug, then C5c.

## 2026-11-02 · Mark's default gear (`thj/onboarding`)

**Built:** `Unit_Mark.prefab` sockets default to Monk's Tunic (Chest) and Wrist Wrap of Power (RightHand), like the other heroes (D-367, D-369: fixed gear, upgrade only); test extended. Commit `106edafec`.
**Verified:** prefab diff only the two lines; EditMode 1289/1291 (known red + flaky `HomeVisitsTests` repair test, passes alone); THJ played: both items equipped.
**Not verified:** the Wrap's stat bonus in combat.
**Findings:** the Workshop only upgrades; equip lives in character select (not a player path under D-369). Unity re-adds `preloadOverride`/`showSpeed` lines on the next Mark prefab save.
**Status:** done. Flaky test fix next.

## 2026-11-03 · Onboarding C5c: guided skill spend (`thj/onboarding`)

**Built:** `AbilityUpgradePanelUI.OpenOnCharacter` / `HighlightNode` and a node pulse in new partials (`59c5a6a25`); `GuidedSkillSpend` + once-per-save marker via `PlayedSequencesTracker` + builder step (`4dd76b498`); Home scene component (`14330fd06`); 15 tests (`1f3df84ac`). First Grandma Table open after River and Ridge opens on the sister who returned last (Lucy Sidewinders / Linda Longshot pulsing).
**Verified:** EditMode 1303/1304 (known red only); review FIX (pulse never stopped; came back on reopen) → APPROVE; THJ played: right tree, node pulses.
**Not verified:** —
**Findings:** the sister's hero tab doesn't look selected (tab selection look is the hover size only); fix next. If The Trail is played before the table is opened, the guide never shows (by plan wording).
**Status:** C5 done except the tab fix; then the timed pacing play check.

## 2026-11-03 · Skill tree tab looks selected (`thj/onboarding`)

**Built:** a hero tab selected from code grows like a clicked one; the first tab on a normal open is marked Selected (D-371). 2 tests. Commit `35ed82daa`.
**Verified:** EditMode 1305/1306 (known red only); coordinator read the diff; THJ played OK.
**Status:** structure C5 done. Next: timed pacing play check.

## 2026-11-04: Linda memory rework committed (L1)

**Built:** THJ reworked `GB_m1-linda` into 3 queued win stages (clear claws, Linda gathers on (2,7), interruption reveals 4 hidden claws, finish; turn cap 4). Wire Memory 1 (Linda) now rebuilds that design with a separate condition per objective, hidden claws inactive and worth no XP (D-376); tests rewritten (5 new). Commit `67fb2d3bf`.
**Verified:** compile clean; tool run twice, second run byte-identical; EditMode 1309/1310 (known red only); review APPROVE; THJ played OK.
**Not verified:** nothing open for L1.
**Findings:** shared `[SerializeReference]` conditions came from the list "+" copy (T6, G4 next); same sharing in `main`'s `Level2-C2`, `Level2-C3-2`, `LevelDomFight`.
**Status:** next G4. THJ's level questions open (`reports/linda-memory-rework-review.md`).

## 2026-11-04: Shared objective conditions (G4) + Linda caps follow-up

**Built:** editor checker + Tools > Levels > Split Shared Objective Conditions + scan test (`83aa585f0`); `Level2-C2` split (`9ba3b8421`); Linda wiring per-stage caps 2/3/4, hidden claws inactive (`4d4e78424`).
**Verified:** compile clean; EditMode 1314/1315 (known red only); G4 review APPROVE; tool runs idempotent.
**Not verified:** no play check of the inactive-claw save (runtime already hid them on load).
**Findings:** `67fb2d3bf` had shipped 2 red tests (THJ's play-tuned save after the verify); rule D-379 added. Only `Level2-C2` truly shared a condition; the other two suspects were variant override entries.
**Status:** next G1 (level ability lock).

## 2026-11-04: Ability lock, Encore pulse, hint on unlock (G1–G3)

**Built:** level ability lock (`266a3985c`), Encore pulse while empty (`ccfbb36d2`), hint start mode WhenUnlocked (`ced039945`).
**Verified:** compile clean; EditMode 1335/1336 (known red only); reviews APPROVE (fixes applied).
**Not verified:** no play check yet; comes with L3 (Linda memory data).
**Findings:** Family Super Time can still cast a locked `superTimeAbility` (core; accepted for now, D-381). `GB_m4-mark` re-save writes `startMode: 0` (noise).
**Status:** next L3.

## 2026-11-04: Linda memory lock/unlock (L3)

**Built:** `GB_m1-linda` locks Explosive Arrow + Encore, unlock step in the interruption, Explosive Arrow hint on unlock; THJ's claw turnOrder and camera tweaks (`0aa549bc6`).
**Verified:** tool idempotent; review APPROVE; THJ played OK (locks, unlock, pulses, order); EditMode 1337/1339.
**Not verified:** Super Time reach in the memory (gap accepted, D-381).
**Findings:** `QuiverWiringTests.RecallAbility_IsTwoApCooldownTwoSelfCast` red since `87174b9fc` (Encore text no longer states 2 AP).
**Status:** onboarding-side tweaks T1–T4, T6 done; T5 data done (tie-break core fix later, D-374). Next: THJ on the Encore text test; the cherry-pick session to `main` when he wants.

## 2026-11-04: Linda memory follow-up

**Built:** THJ's objective texts, interruption phase call Reset (fresh turn after the reveal), punchline "Seven Claws. One arrow.", all through the wiring (`aff7dabec`); `Level1-C1-2` sprite reparent + `GB_m4-mark` default (`89f4981fe`).
**Verified:** tool idempotent; THJ played OK; EditMode 1340/1341 (known red only).
**Not verified:** nothing open.
**Findings:** hero `animationEvents` overrides keep appearing in several Greybox levels on save; held back, backlog `hero-animation-events-noise`.
**Status:** Linda memory tuning done. Next: THJ's pick (next level, cherry-pick session, tie-break plan, noise investigation). Narrative draft M1-1 note needs the new punchline (narrative agent).

## 2026-11-05: Hero animation-event growth fixed at the source

**Built:** `FactionRoleHandlerBase.InitializePartially` uses the light ability init (`73fa9050e`, core, D-387) + test. Levels plan's Linda section rewritten as built; grid rendered and checked.
**Verified:** review APPROVE; EditMode 1343/1344 (known red only, same 41 mismatches); test red before, green after.
**Not verified:** a long play session confirming no new overrides on level save (expected; restart the editor first, since prefabs already grown in memory stay grown).
**Findings:** 30 committed levels on `main` and `Unit_Linda.prefab` (15 entries) carry inert junk; left as is by THJ's choice.
**Status:** done. Next: THJ's pick.

## 2026-11-05: Lucy/Linda memory tweaks; narrator box; tint after Reset

**Built:** THJ's tweaks (Lucy: Cyclone lock, hint, reset call, unlock; Linda caps 2/2/2) + wiring/tests sync (`97f4a7653`); image-first dialogues skip the empty text box (`82734b642`, D-388); `RestartTurn` refreshes the exhausted tint (`02ef3195e`, core, D-389).
**Verified:** reviews APPROVE (sync after one compile fix); tools re-run change nothing; EditMode 1354/1355 (known red only), rerun after THJ's play; THJ played OK.
**Not verified:** a phase reset during the AI phase (no level does it today).
**Findings:** the cutaway image is `HearthStill_Placeholder.png` (85 bytes, blank) until the Hearth painting exists (design Q5). Dialogue edge cases backlogged. animationEvents noise remains on 7 Greybox levels until the editor restarts.
**Status:** done; next THJ's pick.

## 2026-11-05: Animation-event growth closed for good

**Built:** `RuntimeAbility.Initialize` uses a runtime-only activation event (`98574aaab`, core, D-390); `LevelBase.SetID` returns early when unchanged (`eb10f1c5a`, core, D-391).
**Verified:** reviews APPROVE; EditMode 1359/1360 (known red, 41 mismatches); THJ played attacks, a Super Time, an item, a Duo, a pass-by; after Play + Ctrl+S, 0 of 111 level/hero prefabs changed (md5 baseline).
**Not verified:** nothing open.
**Findings:** `73fa9050e` alone wasn't enough (source of the residual growth not pinned). `Mission.OnValidate` still dirties Mission assets (backlog).
**Status:** done.

## 2026-11-05 · John memory tuning (THJ) + fix-ups

- Built: THJ's `GB_m3-john` tuning (5 far Claws, per-claw turn order, 4 kills / turn cap 3, Duos locked all level, D-393); fix-ups (new Claw no XP, text, Wire Memory 3 (John) writes it all incl. the lock, tests; D-395). Commit `0cfba55c8`.
- Verified: review APPROVE; both tools idempotent (md5); EditMode 1361/1362, known red only; THJ played OK.
- Encore: THJ's animation (frame 4) + Add Encore refreshes existing slots, 9 custom-kit levels refreshed: `4a0c8c080` (→ `main`). EditMode 1361/1362 known red.
- Status: done.

## 2026-11-06 · Memory 4 rework: R1 cast sequence, R2 Hearth pool Claws

- **Built:** `CastAbilitySequence` (general; a sequence makes a unit cast an ability on a cell) and Tools > Onboarding > Wire Hearth Pool Claws (0-XP alert Claw variant, spawner on turns 1-8).
- **Verified:** clean compile; pool tool idempotent (md5 of 8 files unchanged on rerun); 11/11 + 6/6 new tests; THJ Run All 1375/1379.
- **Not verified:** play (comes with R3).
- **Findings:** `GridToLevelTests` has no stale-folder cleanup in SetUp: an interrupted run leaves `Greybox/__Test` and the next run fails two tests once. Backlog candidate. `NothingInTheHearthGivesExperience` red until R3 swaps THJ's stock spawners.
- **Status:** committed `0131dd473`, `163e01f56`. R3 next.

## 2026-11-06 · Memory 4 rework: R3 level

- **Built:** `GB_m4-mark` rebuilt by Wire Memory 4 (Mark): Bloom opening (Lucy's Cyclone by sequence at level start), Mark visible with 0 AP and his two Claws revealed on arrival (D-400), John's hold, Mark-Lucy Duo unlock, wolf falls and walk to the cub. Locks, AP cap, hints, Hearth pools.
- **Verified:** review APPROVE + 3 fix-ups; tool idempotent (md5); Mark/Levels/Pool tests 38/38; THJ Run All (AI red only); THJ played it through.
- **Findings:** hand-placed cells outside `Grid/Tilemap` are ignored by the grid with everything on them (`GridManager.cs:58-60`); the tool now reparents them. No other level has stray cells. Hidden heroes lose Duo bindings (core; D-400).
- **Status:** committed `b18b2b6c7`. THJ tuning next.
## 2026-11-06: UnitAnimationSequence modes and two-column end panel

**Built:** `UnitAnimationSequence` playback modes, facing and find-by-tile (`8a5cc1fb4`); John's Bloom gesture and BackToIdle (`ffc182379`); THJ's Loop Time off on APTransfer (`3706b47ab`); objective row truncation (`decb77658`); two-column end panel, empty rows hidden, input lock while open, stale scene overrides removed (`7e5d28da5`).

**Verified:** full EditMode 1433 run, 1422 passed, 11 known reds (AI baseline, 10 Mark layout tests). THJ played both: "all fine". Reviews: `reports/unit-animation-sequence-modes-review.md`, `reports/end-panel-two-columns-review.md`.

**Not verified:** suite not re-run after THJ's clip change (no code). Input lock read and unit-tested, not re-reviewed. Boss intro sequence can't be played (nothing uses it).

**Findings:** with Loop Time off, John's Loop mode logs a warning and plays once. Every win objective shows Success (unchanged). The Hearth's `completed` in a test save makes the Lost panel offer Return Home, by the existing rule.

**Status:** done; other branches need the panel and sequence when merged.

## 2026-11-06: Select a unit from a sequence; Mark selected after his arrival

**Built:** `TrySelectUnit` and the one-shot preferred auto-select unit (`4b0237c01`, core); `SelectUnitSequence` (`c2b2f467b`); Memory 4's arrival step.

**Verified:** full EditMode 1452 run, 1441 passed, 11 known reds, before a comment-only fix (12 related tests re-run after). Re-review approved. THJ played it and saw nothing wrong.

**Not verified:** `Clear` and `Take` call sites have no automated test. Whether THJ tried the last-AP kill and hold-to-skip cases wasn't stated.

**Findings:** `GridToLevelCameraStartTests` teardown ignores `DeleteAsset`'s result and once left `__CameraStartTest` behind (now gone). `HearthMemoryWiring.Mark.Sequences.cs` omits this step.

**Status:** done; project-wide code goes to other branches when merged.

## 2026-11-06: Memory 4 settled: tests follow the prefab, builder sets enemy facing

**Built:** John's gesture on Once No Wait (`ac1293445`); Mark tests pin THJ's prefab (`8da7747fa`); Build Level From Grid sets enemy facing by footprint centre against the main group's middle (commit after `8da7747fa`). Segment 4 and the narrative draft synced.

**Verified:** full EditMode 1466/1467, known AI red only. Reviewer's fixes applied (reviewer didn't re-read them; coordinator spot-checked the footprint fix). THJ played John's gesture. Drawing checked against the prefab.

**Not verified:** facing on a real rebuilt level in play; no test checks the saved YAML override.

**Findings:** the (6,4) Claw has about 12.5 HP, the level's highest; flagged to THJ. If the (3,5) Claw lives into the arrival, the (3,7) walk cancels with a warning. Rebuilding an older greybox turns its left enemies.

**Status:** done; next is the timed pacing check.


## 2026-11-08: Bond Lite done, with the fixes from THJ's first full play

**Built:** C4 Rivalry (`f64dc3424`, `b4525d46e`, `fa1fbcbb6`) and C5 Yard Bond and point (`c0e91e97c`, `72ed77108`, `a75c19680`, `59a527d4c`), committed after THJ's play. Then fixes from his nine findings (`plans/onboarding/2026-11-07-bond-lite-play-fixes.md`): skill-tree highlight null ref (`b14e52fe7`); Home opens without the old house page (`18f73aaeb`); Hearth close at Home with Ryker's loss and the World map page (`eb3ba2406`); station pages play by themselves when a station first opens, no camera move (`67fd68a04` runtime, `32ac85086` data); Marks-Sisters drops "[Duo]" (`eeb2a1c4a`); THJ's F10 win-level cheat (`47a9139cb`); Home camera step for scenes in Home's opening (`6998ba019`); the Yard staged: own Home state with Lucy training and Linda near, camera to the yard, Y12-1 to Y12-6, Bond step, "Linda & Lucy's Bond reached Lv 2.", Margaret, pointer, pan back (`6af47eeb6`).

**Verified:** reviews APPROVE (C1–C4 fixes). THJ played every fix. Final EditMode Run All by THJ: all pass except the known AI red. Pan back checked frame by frame in Play (no jump).

**Not verified:** one-hold skip of the whole Yard (a hold during the pan only finishes the pan; shared `SequentialSequence`). Page images are placeholders.

**Findings:** before `cameraHandler.Initialize()` the Home MainCamera sits offset (-12.69, -24.38) from its rig with zoom target 0, so any focus in Home's opening frames the wrong place (`tech/home-system.md`). `CameraSequence` reaches the stale combat handler after a mission. Rare test flakes: `GridToLevelSettingsTests` and `GridToLevelFpTests` (leftover folder, Unity assert); a stalled run left `_GuidedSpendScratch.unity` (gone after the rerun).

**Docs:** GDD progression-economy (PR-6, PR-8, unlock table), family-systems (BO-1 to BO-4), overview (BO prefix), glossary (Bond, skill points, Family skill point), narrative draft, first-hour design, `tech/home-system.md`, `tech/classic-fallback.md`, `branches.md`. Claude Doc mirror: this build-log section needs syncing.

**Status:** Bond Lite done on `thj/bond-lite`. THJ's: fast-forward `thj/onboarding`, idles per visit (Linda's yard stand-in), page images. Open: Lucy's pointer says "Family Skill Tree" vs the glossary's "Family tree".


## 2026-11-08: Sisters' tally built (running joke of the first hour)

**Built** (plan `plans/onboarding/2026-11-08-sisters-tally-tech.md`, D-444 to D-454), on `thj/onboarding`:
- Counting: per-mission kill tally for Lucy and Linda, off switch `SistersTally.Enabled` in code (`74c97e819`).
- Core hook: the combat HUD can hide and show one extra panel (`HudPanelBase`; `c0d623cc2`).
- HUD counter, top centre (`e0d09f5f6`).
- Kills made together count for both: Duo bracket and the Tempest Bloom window; per-level eligibility, so Hearth segments 3–4 show it (`d1c178f4c`).
- Mission-end panel: two stat rows with portraits, and MVP hidden while they show (`2c698e997`).
- Steps: show alone, fade out (saved, unscaled time) and return; return is built but not placed (`036e4ca20`).
- The Trail's pile: "Still counting?" with the counter alone, then the fade, then "…No." (`b07870da4`).

**Verified:** every chunk reviewed APPROVE. Final EditMode 1740/1741, known AI red only. THJ played the counter, the Duo, Bloom, the Hearth results panel (layout, MVP hidden) and The Trail's pile fade.

**Not verified:** M4 after the fade (no counter expected until return is placed); ATB mode.

**Findings:**
- No Duo's damage reaches `onUnitDamageDone`, so mission stats, John's Wrath and Mark's Barrier miss Duo hits. Backlog `duo-damage-events`; revisit MVP with it.
- Bloom copies landing after Linda's ability ends count for no one (core limit).
- Goblin Queen's finishing move counts for no one.
- M1 `Level1-C2` also shows the tally (D-452).
- Unity resets four existing icon width overrides on `SessionEndPanel.prefab` saves (layout-driven, no visual change).

**Docs:** `tech/core-systems.md` (HUD extra panel). Design and glossary docs routed (first-hour design tally row, GDD); glossary row "Sisters' tally" still waits on THJ's glossary approval. Claude Doc mirror: this build-log section needs syncing.

**Status:** done. Return step to place with the framed beat (D-448). Window-length concern (THJ) in backlog after the pacing check.

## 2026-11-10 · Objective feedback C1 (thj/after-hearth)

- Built: met objective line strikes, pulses (1.2/0.4 s), flashes gold and plays `A_UI_ObjectiveMet`; new lines after a stage advance fade in from gold with `A_UI_ObjectiveNew`, after the met feedback; while the HUD is hidden (cut-ins) both wait and play on return in that order, 1 s apart; once the level ends lines strike at once, silent, nothing replayed (win outros' ShowHUD). Pure rules in `ObjectiveFeedbackRules` + tests.
- Verified: EditMode 1803/1804 (known AI red only); review APPROVE after 8 rounds; THJ play check OK.
- Not verified: real clips (placeholders = click).
- Status: committed `736a39325`.

## 2026-11-10 · Objective feedback C2 (thj/after-hearth)

- Built: `LevelResultLine` (Core/UI/Runtime/SessionEndPanel, not core-list) shows one line instead of objective rows on a win; four Hearth memory lines (D-487) via `Tools/Onboarding/Wire Hearth Result Lines` + Linda/Lucy/John tools.
- Verified: EditMode 1815/1816 (known AI red only); review APPROVE; THJ play check OK.
- Findings: green Success tag shows beside the line (THJ: remove later); readability should-fix at `MissionEndPanelUI.cs:188` open.
- Status: committed `089bd17af`, `2001fef06`.

## 2026-11-10 · Synergy aim preview C1 (thj/after-hearth)

- Built: Shield Flare preview as ghost fireballs around John facing each copy's flight (no lines), on John's layer in front of him; shared geometry with the real shot.
- Verified: EditMode 1833/1834 (known AI red only); review APPROVE (4 rounds); THJ play check OK.
- Not verified: two-pick persistence (ghosts follow the hovered pick only); fireball blocked before John.
- Status: committed `79e7ced64`.

## 2026-11-11 · Synergy aim preview C2, Tempest Bloom (thj/after-hearth)

- Built: Bloom preview in Linda's lane look (other lanes dark, copy lanes lit, one >>> each, HP bars on copy hits); real Bloom fixed to 3 copies (back copy skipped).
- Verified: EditMode 1853/1854 (known AI red only); review APPROVE (3 rounds); THJ play check OK.
- Not verified: multi-cell (boss) targets past a Cyclone.
- Status: committed `22a3d1dc0`, `9054a0fea`.

## 2026-11-11 · Synergy aim preview C3, Catch & Return (thj/after-hearth)

- Built: catch preview (>>> on Mark's tile toward Linda, return damage in the pink second colour, works alongside the Bloom); catch checks extracted to pure rules.
- Verified: EditMode 1872/1873 (known AI red only); review APPROVE (4 rounds); THJ play check OK.
- Not verified: lanes blocked before Mark (assumed clear, as Bloom).
- Status: committed `6cdd53f33`, `d13e76155`. Synergy aim preview complete.

## 2026-11-11 · M2 The Trail rebuilt (after-Hearth chunk 3)

**Built:** the four Trail levels rebuilt from the after-Hearth design's `m2-*` grid blocks (one-turn Trailhead fight; both routes reworked; The Pile with a tile search, Lucy's working line, then hidden west/east groups revealed). All enemies alert, sisters' Duo locked, no FTP drain, Pass-by/Items panels and the rear wave removed; Claw factor 0.6, Archer 0.25. `Wire Search: Trail` and `SearchTrailTests` updated. Commit `e3a45983b` (shared repo, `thj/after-hearth`). Plan `plans/onboarding/2026-11-11-m2-trail-levels-tech.md`.
**Verified:** compile clean; EditMode 1875/1876 (known AI red only); wiring idempotent; review APPROVE; THJ played both picks and both routes to a win.
**Not verified:** nothing open on the build itself.
**Findings:** THJ: no challenge ("all HP"); the first volley decided every fight (`playtests/2026-11-11-trail-rework-play.md`). Starts-alert Claw prefab has no repair path.
**Status:** base committed; challenge redesign in design (D-505).

## 2026-11-11 · M2 Trail C3: the challenge rebuild (D-511, D-513 to D-515)

**Built:** the four Trail levels rebuilt from revision 2 of the post-Hearth challenge design: Trailhead front and back; Follow the tracks with a Black Claw leader and a turn-2 pair; Follow the blood as a two-hero reach (end tiles 18,1 / 19,1 / 19,0, hidden kill-all fallback) with a turn-2 pair; the Pile without the Archer. Arrivals: input off → camera on group → reveal → bark → camera on Linda → input on. Blood's stage-2 row has the working line "Keep moving. Claws on both sides." Committed `9e9e0ca63` (one commit: prefabs, wiring, tests, sequence assets).
**Verified:** EditMode 1875/1876 (known AI red only); wiring idempotent (md5); review FIX → must-fixes done (literal asserts), coordinator read; THJ played C3 both picks before the fix round (`playtests/2026-11-11-trail-c3-play.md`).
**Not verified:** the camera on Linda after arrivals and its dead-Linda path (in THJ's C4 replay).
**Findings:** still low threat in play (Cyclone walked into by the AI, Mark–Lucy Duo wipe, free reactions, Claw hits 3–4) → balance round (D-512, D-516 to D-520). Possible bug: Lucy's skill-tree point gone after level 1.
**Status:** C3 done. Next: C4 values (Standard tier, Tracks HP, Cyclone damage 3); Bond tree note (Bloom open, sisters' Duo as a Lv 2 node).

## 2026-11-11 · M2 Trail C4: balance values (D-516, D-518)

**Built:** the Trail at Standard tier (Claw 6, Black Claw 10); Tracks' Claws at 16 HP, Black Claw ×0.75 (30); Lucy's Cyclone damage factor 7 → 3 (global, cooldown 2). Committed `33fdb4566` (Cyclone, alone) and `75d97cd05` (Trail prefabs, wiring, tests).
**Verified:** EditMode 1876/1877 (known AI red only); wiring idempotent; review APPROVE; THJ's replay (Mark pick): 28 taken (was 14), "much much better, okay for now".
**Not verified:** John pick and blood route at Standard (not replayed).
**Status:** the Trail's challenge is okay for now. Next: the Bond tree change (Bloom open, sisters' Duo node).

## 2026-11-11 · Merge into main + wiring leaves dialogue (D-525 to D-527)

**Built:** local `main` fast-forwarded to `origin/main` (8 teammate commits), `thj/after-hearth` merged (`b1f9d1f68`; conflicts: scene roots kept both, Memory 4 mother dialogue kept main's). The wiring seeds dialogue and step lists only when it creates them (`27030ad4e`); the teammate's HomeMemoryOpening tests run in edit mode (`228b830c1`). Nothing pushed (`main` 17 ahead of `origin/main`).
**Verified:** EditMode 1892/1893 in the editor (known AI red only); all 8 wiring menus run twice, 396 sequence/mission assets unchanged by md5; review APPROVE (should-fixes done).
**Not verified:** the teammate's restructured Hearth endings in play (Linda's end no longer re-enables input/HUD itself; Mark's walks over a faded grid; Lucy's cutaway unused).
**Findings:** the 3 GridToLevel `m_LockCount` failures are command-line only. The wiring warns on Memories 1–3 (structure differs from the teammate's); a follow-up could align the wiring with the teammate's flow.
**Status:** done.

## 2026-11-12 · Hearth Memory 4 no longer stuck at Home (D-528)

**Built:** `HomeMemoryTransition.TransitionToNextLevel` on a mission's completed last level ends the mission from the Home view (`EndMission(true)`, timer frozen as the panel did), no panel; pure `ResolveNextStep` + 4 tests. Committed `aaae8a7db`.
**Verified:** EditMode 1896/1897 (known AI red only); review APPROVE; THJ played the Hearth through Memory 4 into Home: works.
**Findings:** cause was the teammate's Memory 4 end (`TransitionToNextLevel` on the mission's last level), not the merge. Backlog: `HomeMemoryTransition.ResetPlayModeState` uses `[RuntimeInitializeOnLoadMethod]` instead of the `PlayModeStaticReset` hook.
**Status:** done. `main` 18 ahead of `origin/main` (not pushed).

## 2026-11-12 · Lucy's Cyclone redesign, Pulling Gale v2 (`thj/cyclone`, D-529 to D-545)

**Built** (uncommitted, built back to back without per-chunk play, D-534; plan `plans/2026-11-11-cyclone-redesign-tech.md`; reports `reports/cyclone-c1a.md` to `cyclone-c5.md`):
- C1: anchored `CycloneEntity` (3 pips, one per family turn start; cast 1 AP, range 3, empty cell, cooldown 4; enemies can't target it; cross and pips drawn). Whirl on cast and on each enemy faction's turn end (pull 1 on straight 2-cell arms, Immovable and large units not pulled, then 3× to touching enemies), reported once per hit through the new `ReportDamageOutsideAbility`; `TurnEnding` hold; watchdog ignores paused time (D-536); Masher ignores Whirl hits (D-537); tally counts a kill once.
- C2: family/allies/neutrals pass through, can't stop; enemies and pushes blocked; Blink/Vault/dash/Duo stops kept off it (D-538); AI drops end-of-turn spots on the cross unless it can attack from there.
- C3: Steer (second ability on the same button, 1 AP, once a turn, 3 cells, range centred on the Cyclone via `ITargetSelectionRangeProvider`, D-539) + Gust (pull only); bar refresh when ready; AI-controlled Lucy refuses Steer (D-540).
- C4: enemy projectile shots blocked through the Cyclone tile (centre-to-centre, corner grazes allowed, D-541) in AI pick, intent, execution and threat preview; firing-spot filter (Shaman support first, D-543).
- C5: pulls wake Unaware enemies (D-542); Howling Gale hit-only confirmed and tested (D-545); Watch/Command Shield Dash checked by reading; working texts (D-544).
- 20 proposed commits, exact files and messages in `reports/cyclone-verify.md`. THJ's AI diagnostic discarded before C2 (backup `reports/ai-diagnostic-backup-2026-11-12.patch`).
**Verified:** every chunk reviewed (APPROVE after fix rounds); final gate (`reports/cyclone-verify.md`): compile clean, EditMode 2015/2016 (only the known AI red, 43 inner: was 41 earlier from main drift, +1 from the new Steer preset); every changed file in exactly one commit, no missing metas.
**Not verified:** anything in play. Full list: `playtests/2026-11-12-cyclone-play-check.md` (Whirl beat with Watch, AI waiting outside the cross, Archers repositioning, pulls into hazards and waking, Steer button after a cast, Memory 4 and the Lucy memory, the Trail levels).
**Findings:** design §5 holds only as "not on the arms" (diagonal waiting possible); a blocked Archer may stay or back off; camera ease and wind sound not built; Steer icon, animation and SFX are placeholders; two enemy factions → two Whirls a round. Docs synced: GDD Lucy, Combat rules, Enemies, Family systems, level chunks (designer), `core-systems.md`, `combat-architecture.md`.
**Status:** built and reviewed; waiting on THJ's play check, then the commits (Claude Docs mirror sync owed for the four GDD pages).

## 2026-11-16 · Cyclone redesign committed before the full play (D-546)

**Built:** nothing new. The 20 Cyclone commits landed on `thj/cyclone` as planned in `reports/cyclone-verify.md`: `281d33866` (grid line of fire) through `e1203b02d` (Howling Gale text and tests); core changes each in their own commit. Not pushed.
**Verified:** every changed Cyclone file in exactly one commit, every new file with its `.meta`; tree left with only THJ's local files (TMP fallback font, `PreloadScreen.unity`, two `ProjectSettings` files, `GlobalSettings.asset` test settings, then committed at THJ's request as `b88c004f1`: intro/outro sequences off; revert before merging to `main` if intros should play).
**Not verified:** the full play check (THJ played part of it); intermediate commits were not compiled one by one, only the final tree.
**Status:** committed so THJ can test from the office PC; play findings go in new commits.

## 2026-11-17 · Cyclone round 2 built, not yet played or committed (D-547 to D-559)

**Built:** C1 Steer ends in a Whirl and Power 3/4/5; C2 carry; C3a-c heavies walk through and burst it (core Grid and AI additions); C4 cross redraw, cast and Steer previews with ghosts and damage, first-frame fix, Cyclone-only wobble; C5 texts (D-559) and GDD sync. Reports `reports/cyclone-r2-c1.md` to `-c5.md`, reviews beside them.
**Verified:** every chunk reviewed (several fix rounds); final gate `reports/cyclone-r2-final-verify.md`: compile clean, EditMode 2114 run, only the known AI red, inner count 43; C5 re-run the same.
**Not verified:** all Play-mode behavior; item 0 of `playtests/2026-11-17-cyclone-round2-play-check.md` first (cast preview in the normal Preload > Home > level flow).
**Findings:** the Cyclone files are LF, not CRLF. One-Watch-per-action core limit; AI intent prediction ignores the Cyclone as a mover; detour reachability (D-553) to judge in play. Backlog: stray old Cyclone assets under `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/`.
**Status:** built and reviewed, uncommitted; waiting on THJ's play check, then commits (shared files C1/C2/C3b/C4 need hunk-level staging; `Lucy_Cyclone_Ability.asset` carries both Power factors and description). Claude Docs mirror sync owed: GDD Lucy, Enemies, Combat rules, Family systems.


## 2026-11-17 · Cyclone round 2 committed before play (THJ: commit, play tomorrow)

**Built:** nothing new. Five commits on `thj/cyclone`: `5f89cca91` core Grid (mover pass, burst hook), `6a6bbbd27` core AI (danger cells per source), `a427a08b2` Cyclone gameplay (C1 to C3b, tests, Cyclone description), `54e03cd94` visuals and previews (C4), `6990b93a2` texts (Steer, Power, Howling Gale, Tempest Bloom). Not pushed.
**Verified:** the working tree afterwards holds only THJ's four local files (TMP fallback font, `PreloadScreen.unity`, two `ProjectSettings`), so the committed tree is the one that passed the full EditMode run (2114, known red only, count 43).
**Not verified:** commits 3 and 4 were staged with pre-C4 copies of shared files, so commit 3 was not compiled on its own; only the final tree was. Play check still owed (`playtests/2026-11-17-cyclone-round2-play-check.md`, item 0 first).
**Status:** committed; play findings go in new commits. Revert `b88c004f1` intro/outro settings before any merge to `main`.

## 2026-11-17 · Catch & Return offer, C1 (rule and runtime; on `main`)

**Built:** Mark's catch prompt opens only if the return copy would hit an enemy (`CatchOfferRules`, `CatchReturnHits` shared hit walk, `TryCatch` asks before freezing; declined arrows fly on and aren't re-asked). Bloom preview's contact walk moved into the shared helper unchanged. 19 edit-mode tests (`CatchOfferTests`). Plan `plans/2026-11-17-catch-return-offer-tech.md`; decisions D-560, D-561. Review APPROVE (3 should-fixes: slnx kept out of the commit, enemy/ally/neutral/dead check made a pure function with tests, safe test lookup; all done).
**Verified:** THJ recompiled and ran EditMode: all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. **Committed `521742a74`** (8 files, `miso.slnx` left out).
**Not verified:** the real freeze/prompt path and the faction lookup in play (enemy only past Mark, between, both, none); inner failure count of the known red not recorded.
**Findings:** an ally alone in front of Mark with no enemy no longer gets the prompt (follows the rule). The C2 preview must call the shared hit counter so neutral units can't get a pink bar with no chevron.
**Status:** C2 (preview: hide chevron and pink bars when not offered, grey the lost forward hits) dispatched; C3 docs after; one play check at the end.

## 2026-11-17 · Catch & Return offer, C2 (preview, real grey; on `main`)

**Built:** the aim preview asks the same shared rule and hit counter as the real catch: no chevron and no pink bars when the catch isn't offered; when it is, the forward hits past Mark (and every Tempest Bloom copy hit, on or off the lane) show in grey, because taking the catch gives them up. First built as hidden bars, escalated by the reviewer (a missed prompt hits them at full damage while the preview showed nothing); THJ chose real grey (D-563). Additive core overload `GUnit.ShowDamagePreview(..., lost)` + grey tint (`lostDecreaseColor`, 0.55, serialized, no prefab edit). Offer decision cached per aim. Reviews: C2 ESCALATE (grey), revision APPROVE (3 should-fixes, done). 14 `CatchPreviewOfferTests`.
**Verified:** THJ recompiled and ran EditMode: all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. **Committed** `5426a16d7` (core overload + HP bar tint, own commit) and `2cf617358` (preview + tests); `miso.slnx` left out.
**Not verified:** all drawing in play (grey, chevron, pink bars, clearing on cancel/click/level end, off-lane Bloom copy enemy grey); the real freeze/prompt path; inner failure count of the known red not recorded.
**Findings:** the refund-only branch of `TryCatch` is not used by any shipped unit (Mark's prefab is BounceBack; reachable from the Inspector only). A "CRLF" claim in two implementer reports was wrong: all files are LF (a `grep -c $'\r'` check miscounts; use `git ls-files --eol`).
**Status:** C3 docs (designer GDD pages running; tech docs done); then THJ's short play check (`playtests/2026-11-17-catch-offer-play-check.md`).

## 2026-11-18 · Catch & Return offer, C3 (grey tint removed; on `main`)

**Built:** THJ played the preview and did not like the grey (D-564). The forward hits past Mark, and any Bloom copy hit the return doesn't reach, now keep the shot's normal red preview; only the units the return hits keep the pink bar. The lost-hit bookkeeping and helpers in the presenter, the preview rules and their tests were removed; the unused core grey overload, `lostDamage` and `lostDecreaseColor` were removed by hand to the pre-`5426a16d7` state. **Committed** `baa77da19` (synergies preview + tests) and `9e8d82434` (core revert, own commit); `miso.slnx` left out. Report: `reports/catch-offer-c3.md`.
**Verified:** offline Roslyn build of both assemblies, 0 errors; the three core files diff-empty against `5426a16d7^`; no references left to the removed members.
**Not verified:** EditMode after the change (THJ runs it); the drawing in play; cache and cleanup have no edit-mode tests (the presenter can't be unit-tested).
**Findings:** the C2 reports' "core files are CRLF" was wrong, all LF (`git ls-files --eol`). GDD CR-56, Mark MA-3, `tech/` notes, decisions, status and the play check updated for D-564.
**Status:** waiting on THJ's play check; Claude Docs mirror resync still owed (Mark, Linda, Family systems, Combat rules).

## 2026-11-18: Cyclone round 3 and the Masher fix (thj/cyclone)

**Built:** C1 fainter cross alphas (serialized fields); C2 cast on an enemy (shove one cell away from Lucy, preview, own range provider); C3 inhale/exhale, grab/drag/fling, input lock held until the hit (public `PlayerInputController` lock, `swellSeconds` 0.1); fix round for review findings; Masher core hook (`IPlantedClearsOnEntry`, `FootprintEndsOnClearing`, AI landing filter) so a heavy enemy can end a walk on a live Cyclone and burst it, jumps, summons and teleports still refused. Plans: `plans/2026-11-18-cyclone-round3-design.md`, `-tech.md`. Reports: `reports/cyclone-r3-*.md`, `cyclone-masher-*.md`. Decisions D-566 to D-572.
**Verified:** compile clean; EditMode 2174 run, only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner count 43); every chunk reviewed (C1, C2, C3 APPROVE; core fix FIX then fixed).
**Not verified:** nothing played; verifier play session not run. Play list: `playtests/2026-11-18-cyclone-round3-play-check.md` (plus round 2's).
**Findings:** the Masher bug was `IsFootprintEmpty` refusing the Cyclone cell for every can-end-here check (speed 1, 2x2). Cast range highlight never filtered before; now lights only castable cells.
**Commits (not pushed):** `76cd17c77`, `c9ad26e7e`, `031c3a5a1`.
**Status:** committed, awaiting THJ's play check. Docs owed: GDD lucy.md, CR-58, EN-2/EN-6, cyclone-redesign.md note, narrative clause, Claude Docs mirror.

## 2026-11-18: Masher counter step plows through units (branch `main`)

Plan `plans/2026-11-18-masher-plow-tech.md`, decision D-573.

**Built.** Two commits. `89bd4763e`: pure `MasherPlowRules` (which cells a one-cell cardinal step enters, who stands there, where each is pushed, whether the step is allowed) with tests. `62ed9b895`: the runtime. `TryPlanAnswer` also plans steps whose entered cells hold only pushable units (single-cell, not `Unmovable`, a free cell behind, and the walk's own path-cost budget allows it); `Activate` shoves them with `AEffectPusher.TryMoveTo` (new no-effect push asset `MasherGoblin_Ability_Counter_Effect_Push`, built by the Masher preset builder, referenced on the handler of `Unit_MasherGoblin.prefab`) and then walks; the hover preview shows where each pushed unit lands. New partial `MasherGoblinFactionRoleHandler.Plow.cs` and `MasherPlowGrid.cs`. Reports: `reports/masher-plow-c1.md`, `-c1-review.md`, `-c2.md`, `-c2-review.md`.

**Verified.** Compile clean. EditMode suite in THJ's open editor: 2000 of 2001, the only failure the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Reviewer: C1 approved after one fix; C2 one must-fix (the walk's path-cost budget) and two should-fix, all fixed and re-run by the implementer; the fixes were not re-reviewed.

**Not verified.** No play check yet (hazard cell in the way, wall and grid edge, two units on the leading edge, an Immovable unit, Linda in lane with the toggle on and off, the preview). No handler-level test of `TryPlanAnswer`.

**Findings.** (1) With `counterCanProvokeFamilyRoles` on, a shoved enemy landing in Linda's lane can still draw her lane shot, because she reacts to `unitEndMoving`; THJ declined the additive fix (small `SuppressMover` set plus one check in Linda's handler). With the toggle off there is also a small gap when pushes happen but neither walk nor slam follows. (2) A later push failing after an earlier started leaves units shoved and the Masher not stepping (rare). (3) If the Masher is torn down mid-push, the pushed unit may be left between cells. (4) `AEffectPusher` plugs a unit that dies mid-lerp onto the destination (existing behavior). (5) The builder re-saved `Move/MasherGoblin_Ability_Walk.asset` with new default fields; not committed, left modified in the tree for THJ to discard. (6) `thj/cyclone` changes the counter's walk and will conflict in `MasherGoblinFactionRoleHandler.Counter.cs` (`TryPlanAnswer`, `Activate`).

**Status.** Built and committed on `main`, not pushed. Waiting on THJ's play check.

### 2026-11-18, later: Masher plow overlap (`db9cf6ae9`)

**Why.** THJ's first play check of the plow: it works, but the shoved units slid away alone and only then did the Masher walk. THJ chose "overlap only" before any animation (if it isn't enough: a wind-up animation on the activation-frame mechanism, or a real ability, are the fallbacks; options discussed 2026-11-18).

**Built.** The walk starts `plowWalkLeadSeconds` (serialized on the Masher handler, default 0.05 s, 0 = same frame, negative acts as 0) after the shoves start; the answer goes on when both have ended; the footprint-free check before the walk stays (a unit that has not left in time means no step). The walk cannot start before the shoves: it checks and claims its cells in the same call that starts it. Pure timing decisions in `MasherPlowTiming` (15 tests). The safety stop is 10 s of game time (not frames), covering the push and the walk wait. Files: `MasherPlowTiming.cs`, `MasherPlowTimingTests.cs` (+ metas), `.Plow.cs`, `.Counter.cs` (the walk takes its completion callback).

**Verified.** Compile clean; EditMode 2015 of 2016 (only the known red). Reviewer APPROVE, its one should-fix (frame guard) applied.

**Not verified.** The look (bulldozer or not, which lead reads best), a unit dying mid-slide, the Masher disabled mid-walk. Tuning knobs: `plowWalkLeadSeconds`; the push speed on `MasherGoblin_Ability_Counter_Effect_Push.asset` is 5 against the walk's 2.5 (set 2.5 to move as one block).

**Status.** Committed on `main`, not pushed. Waiting on THJ's second play check.

## 2026-11-19: faster loop, and the AI regression test runs on request (all; built on thj/cyclone)

Plan `plans/2026-11-19-faster-loop-process.md`, decisions D-575 to D-579.

**Built:** five process changes in `CLAUDE.md`, `escalation.md`, `templates/report.md`, the coordinator, implementer and verifier definitions and the tech-plan skill (reviews once per feature, one report per plan, covering tests per chunk, serialized presentation values at Tier 2, the AI regression test out of the suite). Game code: `[Explicit]` plus a comment on `AIRegressionTest.Baseline_MatchesCurrentAI`.
**Verified:** verifier quiet check through the Unity MCP: compile clean, console 0 errors; full EditMode run 2174 total, 2173 passed, 0 failed, 1 skipped (the Explicit test, `runstate="Explicit" result="Skipped"` in `TestResults.xml`), 403 s. THJ ran the `.claude/` sync.
**Not verified:** Play mode state was not read before the script edit or the run (no resource-read tool); the test by name and the `Tools/AI/Run Regression Test` menu were not run after the change. No reviewer (size S outside core systems, D-575).
**Findings:** the run was 403 s against 293 s on 2026-11-18, so no time saving is shown yet; the verifier's guess is the editor running in the background. An Explicit test still counts in `total`, as skipped. The editor-open Test Runner writes `%USERPROFILE%/AppData/LocalLow/Dead Mage/miso/TestResults.xml`.
**Commit (not pushed):** `ecba8ecef` on `thj/cyclone`. `main` gets it when the branch merges.
**Status:** done. Effect of the five changes is checked at the Sunday review on or after 2026-12-06.

## 2026-11-19: `main` merged into `thj/cyclone`

**Built.** At THJ's go, `git merge main` on `thj/cyclone` (merge commit `ff16e25b4`, no trailers). It brings in `main`'s 9 commits (`db9cf6ae9` and back to `ce7be3800`): the Masher plow with its overlap, the Catch & Return offer and preview, and a teammate's MS1/MS2 dialogue fix. 33 files changed, no conflicts (a `merge-tree` dry run before the merge said the same). When the merge started, THJ was already on `thj/cyclone` and the shared tree held only the untracked `.mcp.json` (the earlier font and slnx edits were gone); `origin/thj/cyclone` now exists at `031c3a5a1`.

**Verified.** Read the one file both sides changed, `MasherGoblinFactionRoleHandler.Counter.cs`: the sides touched different lines (the Cyclone side only passes `IsCycloneCast` into `Classify`; the plow side adds the push plan, `StopPlow` and the walk callback). The plow's free-step check and the Cyclone fix both use `GridPluggableEntity.IsFootprintEmpty`, which now accepts a clearing planted cell for a heavy mover, so a free step onto a live Cyclone stays an ordinary walk step and the plow plans only steps over units.

**Not verified.** No compile and no EditMode run (Unity closed, nothing run); nothing played. Open question for the play check: a 2x2 Masher step that covers a Cyclone cell and a pushable unit at once (the plow sees a non-free footprint, the Cyclone fix treats the Cyclone part as free).

**Status.** Merged locally, not pushed (10 ahead of `origin/thj/cyclone`). THJ: open Unity, recompile (Ctrl+R), run EditMode (expect only the known red, AI count about 43), then the Masher + Cyclone + plow play check (Linda [8,-1], Cyclone [10,-2], Masher [12,-2], units in its way).

### 2026-11-19, later: `thj/cyclone` after the `main` merge, compile and EditMode

**Verified.** Forced refresh and recompile in THJ's open editor (Unity MCP): no console errors. EditMode suite: 2293 run, 2292 passed, 1 failed, the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (714 checks, 43 failures, the same count as before the merge). So the merge compiles and the Masher plow, Catch & Return, Cyclone and Masher-on-Cyclone tests all pass together (about 138 s).

**Not verified.** Nothing played: the Masher + Cyclone + plow check (including the 2x2 step that covers a Cyclone cell and a pushable unit) is still THJ's.
