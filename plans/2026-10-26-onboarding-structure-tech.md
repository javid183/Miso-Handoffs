# Onboarding: structure tech notes (greybox)

Size: L    Tier: 3 (milestone content, Home, dramatic moments; two small code items need THJ's yes)    Assigned to: `miso-implementer` (chunks below) → `miso-reviewer` → `miso-verifier`
Branch: all (built on `thj/onboarding`, cut from `main` @ `dc64f974a`)
Status: draft, waiting on THJ (questions T1–T4) and on the paper level plans (`plans/2026-10-26-onboarding-levels.md`, in progress)

Design: `plans/2026-10-25-onboarding-first-hour-design.md`. Work plan: `plans/2026-10-25-onboarding-first-hour-workplan.md` (this is step A3; builds B1–B5). Decisions: D-168 to D-180.

## Why

Build the opening's skeleton (missions, rosters, memory rules, Home visit hooks) with placeholder text, so THJ can play and time Hearth → M4 send-off before the new tech (framed beat, Bond Lite, tally) and the narrative layer go in (D-180).

## Goal

A playable greybox: new game → Hearth memory (4 segments) → world map with The River and The Ridge → Home visits → M2 The Trail → M4 send-off, using existing systems wherever they exist.

## What the code already gives us (read 2026-10-26)

| Need | Existing piece | Notes |
|---|---|---|
| Mission graph, AND gate | `GameData.missionDependencyGraph` (`Resources/Game Data.asset`); `SerializableDependencyGraph` `CombineMode`; `GameHandler.IsMissionUnlocked` | GDD MI-1: all gates are AND today. Edited in the graph window (`Tools/Missions/Open Mission Graph`) |
| Mission with levels, route choice | `Mission` asset: `levelDependencyGraph` (+ mission map when there's a choice, MI-11), `MissionRoster`, `completionXPReward`, `collectableGResources` + `resourceCollectionCount`, `initiationSequence`, `completionSequence`, `homeState` | M2's route choice = two branch nodes in its level graph |
| Rosters 2 fixed + 1 free | `MissionRoster` fixed slots, free slots, forced include/exclude | **Levels place their own heroes in 33 of 45 levels (MI-7)**; a free pick only shows up in a level that has deploy slots. M4 has 0 slots today |
| Who is recruited | `GUnit.unlockedAfterMission` (`Unit_Mark.prefab`, `Unit_Toba.prefab`), `CharacterSelectButton` | Mark must unlock after the Hearth, not M3 Mark Intro |
| World map pins | `WorldMapPanelUI` + one `WorldMap_Button` per mission in the Home scene; state from `IsMissionUnlocked` / `IsNew` | New missions need a button each (scene edit) |
| Home stations open by mission | `HomeInteractables.UnlockAfterMissions` + `oneUnlockedMissionCompletionIsEnough`, `tutorialSequence` (first-open panel) | Workshop after River **or** Ridge; skill tree after both |
| Home look per step | `Mission.homeState` → `HomeState` (idles, `requiredMissions`, idles when (not) completed), `HomeStateManager` | Hearth open/close, "Ryker gone" state, searching-in-shifts idles |
| Rule panels | `TutorialDataSO` pages + `TutorialSequence` | "Panels only for rules" |
| Cutaways, interruptions | `DialogNodeSequence` (image nodes), `SequentialSequence`, `LSBExecutionSequence` + `GUnitSpawn`, `LevelSequenceTrigger`, `LevelObjectives` | All existing; no new code expected |
| Clue scene at the Map Table | `Mission.initiationSequence` plays when the mission is picked on the world map | M2's initiation sequence = the clue-combine scene (Q11 reveal). No new code |
| FTP topped up | `LevelStartFPFiller` (level start, `Produce(n)`; `fpAmountToFill`) | Data per memory level |
| Start alert | `LevelAlertSettings` (EnemyAlertSystem) | Data per level |
| Tempest Bloom once | `RU_LindaLucyCycloneSpreadUnlock.asset`, `RunUpgradeTracker.TryGrant`; `FactionTracker.EnterMission`/`QuitMission` clear run upgrades | Lifetime = the mission, so it can't leak past the memory. A grant at a level's start needs a tiny component (C2) |
| Grid fade (D-131) | `OutroCutsceneKeepGridHidden.asset` in `Level1C1-2_End_SequenctialSequence` | Move it to whichever memory level the paper plan names |
| Rigged materials | `collectableGResources` with `resourceCollectionCount` = the list's length gives every entry | The River: Timber + Fabric, nothing random |

## Questions for THJ (Tier 3)

**T1. No XP in the memory: how?**
Context: XP is earned per hit/kill (`GUnit.abilityDamageXpReward`, `lethalDamageXpBonus`) and levels units up mid-mission (`FactionTracker.CollectResource` → `CheckLevelUps`), plus `completionXPReward`. Spawned enemies come from prefabs.
- (a) **Recommended:** a `grantsXP` bool on `Mission` (default true), checked in `FactionTracker.CollectResource` for the XP resource. ~10 lines + a test, but `Mission` and `FactionTracker` are core (Missions; Factions) → own commit.
- (b) Data only: `completionXPReward` 0 and XP overrides of 0 on every memory enemy instance and every spawn source. No core code; easy to miss a spawn, and a later prefab change can bring XP back.
- (c) Allow XP in the memory and tune the later curve around it. Contradicts D-171.
Blocked meanwhile: C2's XP part only.

**T2. M4 squad pick (John or Mark).** M4's 7 levels place their heroes (0 deploy slots), so a free pick does nothing there today (Missions Q8).
- (a) **Recommended:** give M4's levels 3 deploy slots (Lucy, Linda, the pick) and keep Toba placed after his duel. Level data work on 7 prefabs; it also answers Q8 for M4.
- (b) Place both John and Mark, swap in the one picked via a small "roster filter" component on the level. New code; hides the real problem.
Blocked meanwhile: C5 (M4 send-off) only. M2's levels are new, so they get slots from the start.

**T3. Who authors the new and reworked levels in the editor** (memory 1–4, River, Ridge, M2's three)? (a) THJ builds from the paper plans, the implementer wires missions, sequences and data around them (**recommended**: level layout is feel, and builders for combat levels don't exist); (b) the implementer builds them from the paper plans and THJ adjusts.
Blocked meanwhile: C3 and C4 pace.

**T4. Guided skill spend on "the sister who just returned"** (Home visit 2) needs a small piece of code: pick the sister from the most recent completed pair mission (`Mission.CompletionOrder`) and open the skill tree on her with one node highlighted. (a) **Recommended:** build it in C5 as a Home-side component, non-core. (b) Greybox it with a static panel ("Spend Lucy's point") and build the real thing after the pacing check.
Blocked meanwhile: nothing until C5.

## Chunks

One implementer run each, in this order, each play-checked by THJ before its commit (memory: play-test before commit).

### C1 — Mission graph, missions, recruits, world map (data + scene) · sonnet

- New `Mission` assets (names are placeholders until the narrative pass): `M0 - The Hearth`, `MS1 - The River`, `MS2 - The Ridge`, `M2 - The Trail` (new asset; the old `M2 - Ryler is Lost` is kept and unlinked). Each with placeholder levels (an existing level per node is fine) so the flow runs end to end.
- `Game Data.asset` graph: Hearth → River, Hearth → Ridge, (River AND Ridge) → The Trail → M4. Unlink M1, current M2, both M3s, M5–M7 from the path (D-169); assets stay. Check the old M1's role as `InitialMission` moves to the Hearth.
- Rosters (D-172): Hearth = whatever each memory level places; River = John + Lucy fixed; Ridge = Linda + Mark fixed; The Trail = Lucy + Linda fixed + 1 free from {John, Mark} (`forcedExcludedUnits` Toba); M4 per T2.
- `Unit_Mark.prefab` `unlockedAfterMission` → The Hearth. Toba unchanged (after M4's duel).
- Home scene: `WorldMap_Button` for River, Ridge, The Trail; remove or hide the buttons of unlinked missions.
- Acceptance: on a fresh save the Hearth is the only open mission; after it, River and Ridge both show as new; The Trail opens only when both are complete; M4 opens after The Trail; the character select for The Trail offers John or Mark only.
- Tests: EditMode test over `Game Data.asset` asserting the graph order and the AND gate (reads the asset, no scene).

### C2 — Memory rules (small code + data) · opus if T1 = (a), else sonnet

- XP per T1. If (a): `Mission.grantsXP`, checked in `FactionTracker.CollectResource`; its own commit (core). Test: XP collected in a no-XP mission is zero and no level-up fires.
- `LevelStartRunUpgradeGrant` (new, `Features/Onboarding/`, non-core): grants a list of `RunUpgradeSO` to the player faction at level start via `RunUpgradeTracker.TryGrant`. Used only in memory segment 4 for Tempest Bloom. Test: grant applied; cleared by `QuitMission`.
- Per memory level: `LevelStartFPFiller` full FTP; `LevelAlertSettings` all start alert; the grid-fade sequence moved per the paper plan.
- Acceptance: a full Hearth run grants no XP and no level-up; Tempest Bloom works in segment 4 only and is gone in The River; enemies in memory levels start alert, in The River they start Unaware.

### C3 — Memory levels and sequences (levels per T3, then sequences) · sonnet

- Four segments as one mission, levels from the paper plans. Cutaways between segments as `DialogNodeSequence` image nodes over a placeholder still; Home state at the open and close (`homeState` of the Hearth; the open state is the new-game Home).
- Narrator interruptions: `LevelSequenceTrigger` / objective stage → `SequentialSequence` (dialogue, camera, `LSBExecutionSequence` with `GUnitSpawn`). Always freeze and show the change.
- Placeholder text from `reports/onboarding-narrative-draft.md`.
- Acceptance: each segment plays in 2–4 turns at the planned difficulty; interruptions freeze, show and resume; the mission ends in the Hearth close state.

### C4 — The River, The Ridge, The Trail (levels per T3 + data) · sonnet

- Levels from the paper plans. The River's `collectableGResources` = Timber + Fabric, count 2. Catch & Return open by default (D-177): check it is usable on `main` without the Family-tree node; if not, that's a Tier 3 data change (node becomes an upgrade).
- The Trail: route choice in its level graph (two short branches → the pile); low FTP start; Health Potion and Family Trinket in `initialItemsAvailability`; deploy slots for the free pick.
- Acceptance: both pair missions playable in either order; The River always drops Timber and Fabric; The Trail shows the mission map with two routes and ends at the pile.

### C5 — Home visits and M4 send-off (data + T4 code) · sonnet

- Workshop `UnlockAfterMissions` = River, Ridge, one is enough; its first-open `TutorialSequence` = Workshop panel (visit 1).
- Skill tree after both; guided spend per T4; the unspent-points badge (check one exists; if not, flag, don't build).
- Map Table clue scene = The Trail's `initiationSequence`.
- Visit 3: Yard scene as a placeholder dialogue (the Family point and the choice come with Bond Lite, B7). Family point: until B7, grant nothing; note it in the greybox.
- `homeState` per mission for the crisis framing (idles: someone stays home, Ryker absent).
- M4 send-off: Map Table squad pick per T2.
- Acceptance: each visit adds one thing; the Workshop is open after the first pair mission, the skill tree after the second; the clue scene plays when The Trail is picked; the M4 squad pick offers John or Mark.

## Risks

- **Statics:** `LevelStartRunUpgradeGrant` holds none; any new static gets a `PlayModeStaticReset` hook.
- **Core code:** only T1 (a) (`Mission`, `FactionTracker`). Everything else is data, scenes and one new non-core component. Any change to `MissionTracker`/`MissionRouteProgress` found necessary → stop and ask.
- **Save data:** new missions register under their `missionName`; existing saves will show odd states. Testing resets the save (say so in reports). No migration: pre-demo.
- **Scenes and prefabs:** Home scene buttons and level prefabs via small YAML edits or the editor; `Game Data.asset` graph through the graph window, not by hand-editing YAML.
- **AIRegressionTest:** new levels and alert settings may move it; stays known red, never re-baselined.
- **Unlinked content:** M1/M3/M5–M7 assets stay; tutorials tied to them (e.g. `Tutorial_LucyLindaKillAP`) must be re-homed or dropped deliberately; list each in the C1 report.
- **Other branches:** `thj/home-test` has its own prologue and day loop; this greybox is for `main`'s Home. Fold-in is part of the later merge.

## Gates

Compile clean / EditMode (known red only) / review per chunk (C2 core part: opus review) / THJ play check before each commit / C1–C5 together → the timed pacing play check (workplan) / docs: GDD `missions-structure.md` (graph, rosters), `tech/combat-architecture.md` (new component), `status.md`, `build-log.md`.
