# Home system

Owner: coordinator. Scope: `thj/home-test`. What the Home system is in code and how to work with it. Current state and open issues live in `status.md`; step-by-step history in `build-log.md`; the rules and numbers in `design/demo-spec.md`.

## Essentials

Moved here from `CLAUDE.md` on 2026-10-15.

- The Home system is the between-missions house: days, stations, Bond, Picnic, Great Moon, Warren. Code: `miso/Assets/_Project/Core/Systems/HomeSystem/{Runtime,Editor}`.
- Pure C# `HomeSimulation` (no Unity types) driven by the scene MonoBehaviour `HomeDayRunner`; ScriptableObject definitions with GUID ids; demo content built by `Tools/Home/Build Demo Content` (`HomeDemoContentBuilder.cs`).
- Folders under `Core/Systems/HomeSystem/`:
  - `Runtime/Simulation`, `Runtime/State`: pure C#, no Unity types.
  - `Runtime/Definitions`: ScriptableObjects with GUID ids.
  - `Runtime/Presentation`, `Runtime/UI`: the scene views.
  - `Runtime/Combat`: the bridge into sorties (`HomeSortieBridge`, the Omen, SendOff and Dungeon appliers, From Home tags, Bond locks, Fireside payoff).
  - `Editor/`: the idempotent builders and the tests.
- `Core/Home/Runtime/` holds only the small idle-list `HomeStateManager` / `HomeState`. Two `HomeState` types exist: `MISO.Core.Home.HomeState` (idle lists) and the Home system's `Runtime/State/HomeState.cs` (simulation state).
- Home scene: `miso\Assets\_Project\Features\Home - Imported\___Khashayar\Home - Scene.unity`; most of what the Home system adds to it comes from the builders.
- Day slots Morning / Afternoon / Dusk / Night. The Warren dungeon opens only on full-moon Day 7. The Picnic (Hold / Skip) comes before the end-of-demo Win screen. Bond locks (`HomeLockRules`) and staged station unlocks (the cycle's `stagedUnlocks`) gate abilities and rooms.
- Effects are written against FTP, which is why `pointConsumptionMode` is FTP on this branch.
- Stat layers: Yard Lessons raise levels on the Bergsons faction stat layer; Home tier upgrades (Kitchen T2, Dining T2) go on a separate "Home" layer (`StatEvaluation` source `Home`, appended only when the context holds a Home source).
- Barks: `Content/Home/Barks/HomeBarks.csv`.
- Unplaced text is tagged `[PLACEHOLDER] ` in data; `HomeText.Display` strips the tag on screen. 24 such lines live in `HomeDemoContentBuilder.cs`.

## Builders and tools

- Builders (Tools/Home menu, Play off), in order: Build Demo Content, Setup Home Scene, Build Presentation UI, Build House View, Camera/Apply Boundary Fit (optional: Build Stat Layers).
- One-time tools after a fresh checkout or a content rebuild: Add Combat Tags, Build House Traces, Add Bond Locks (re-enter Play afterwards).
- Sim Debug window: `Tools/Home/Sim Debug` (live mode attaches to the scene's sim). Test tools: "+5 (test)" Bond per pair, "Grant +5" materials, "Grant study item", "Grant dish (test)", "Unlock the Picnic (test)".
- Combat dev cheats: `tech/combat-architecture.md`.

## What was built

| Step | Date | What it added |
| --- | --- | --- |
| M0 | Sep | Pure C# `HomeSimulation`, ScriptableObject definitions with GUID ids, `HomeDayRunner`, Sim Debug window |
| M1 | Sep | Food loop: Homestead plots and hens, Kitchen, pantry |
| M2 | Sep | Sorties from the map table, squad seats, Wounded, lost sorties |
| M3 | Sep | Study and mission reveals, Workshop weapon orders, Home Upgrades (Kitchen T2, Dining T2) |
| M4 | Sep 29 | Yard Lessons (faction stat layer), Bond, the "Home" stat layer |
| M5 | Sep | Night seats, Stargaze and star charts, Omens, Vigil, Hearth |
| M6 | Sep 30 | Goblin Queen's Warren on full-moon Day 7, threads, rations, Rest Room, attempts |
| M7 | Sep 30 | Prologue: 3 tutorial missions launched from the map table, Great Moon |
| M8 A–I | Oct 1–2 | Presentation: rooms and station windows, house view and avatars, time flow and moons, Send-off, end screen, Picnic, placeholder tag stripping, camera margin 3 |
| J, K, L | Oct 3, 4, 11 | Merges of `origin/main` (skill-tree redesign, combat log, enemy tiers, Lucy + John shield relay) |
| M9 1 | Oct 5 | Forecast and no dead seats, Care as one visit (Vigil on the sortie night fixed), late Workshop orders warned |
| M9 2 | Oct 5 | Goal and calendar: Queen's Might, moon-strip events, nights remain, pinned Warren, war council |
| M9 3 | Oct 5 | Station badges on props, dock with hotkeys, roster strip, overview key O, recap strip, Mary and Ben at work |
| M9 4 | Oct 6 | Placement without wandering, Morta idles chosen by the sim, Home barks (CSV), Kevin, Send-off gathering at the Door, Porch Break / Fireside Talk names |
| M9 5 | Oct 11–12 | "From Home" combat banner and tags, Dusk headline cards, house traces, before → after stats and the Family sheet, SP badges and the route to the trees, the squad's return |
| M9 6 | Oct 12–13 | Linda–Toba showcase pair and Bond locks in combat, Bond previews, night scenes at Dawn, Fireside payoff, staged station unlocks with introductions, Home Guide |
| Playtest fixes | Oct 13–14 | Forecast and "Bond only" in the windows, Dawn card and war council visible (the council holds the moon), nothing drawn over the map, skill trees or pause menu, Escape closes windows, Bond Lv 2 grants the Linda–Toba duo free, Sim Debug "Grant dish", Workshop opens on staged saves, Quickberry Tart turn-1 AP, Hungry Moon in combat |
| Playtest fixes 2 | Oct 15 (`849c318ab`, `2f828e662`) | The day's report is saved (`HomeSaveData.report`), so a sortie day keeps its Dawn lines and the Weapon card; Mary's Kitchen badge reads a morning Kitchen helper and says "tomorrow afternoon" at Dusk and Night; recipes learned in the Study or from drops get a card; Linda no longer shows twice at Dawn (`HomeIdleDirector` re-hides claims); `FPGainAnimation` saved inactive in `Level Info Panel.prefab` |
| Report-card context images | Oct 16 (uncommitted at the time of writing) | The Dusk headline card shows the icon of what it is about beside the speaker portrait, for Weapon, Upgrade, Recipe, Mission and Thread cut (`HomeHeadlineContext` in `Runtime/Simulation` maps kind to source; `HomeDayHUD.Headlines.cs` resolves the sprite from `refId` at display time). No save-format change; hidden when no icon is assigned (D-043) |
| Onboarding Home (`thj/bond-lite`) | Nov 7–8 | Home's opening (`HomeManager.StartIE`): intro, the mission's completion sequence, the (now empty in onboarding) `InitialTutorial`, then **station pages on unlock** (`HomeManager.StationPages.cs`; a station with `playPageOnUnlock` plays its play-once `tutorialSequence` the first load it's unlocked, scene order, no camera move, D-431/D-440; Workshop and Grandma Table flagged by Apply Opening Setup), then `EndOpening()` (stations ignore clicks until here, D-429) and `cameraHandler.Initialize()`. Completion scenes: Hearth close + World map page (`M0 - The Hearth`), the staged Yard (`M2 - The Trail`, own Home state with Lucy training) with `HomeCameraFocusSequence` (calls `Initialize()` before panning; Home only) and a pan back to the start view. Bond Lite: `BondStore`, `BondNodeGate` locks in the skill-tree UI, `BondActivitySequence` |
| Family tree auto-open (`thj/onboarding-demo`) | Nov 24 (uncommitted at writing) | After `EndOpening()` in `StartIE`, `HomeManager.FamilyTreeOpen.cs` opens the upgrades panel on the Family tab and pulses Sister's Rivalry (`FamilyTreeAutoOpen.SistersNodeGuid`) when the last completed mission is the Family tab's unlock mission (The Trail) and the `FamilyTreeAutoOpened` marker (PlayedSequencesTracker) isn't set; 10-frame retry like the guided spend, marker set only once the Family tab opened; edge scroller held off while it is up. Report `reports/onboarding-x25-family-tree-open.md` |

## Testing notes

- Start Play from `Scenes/PreloadScreen.unity`; the Home scene played directly throws (no `GameHandler`).
- Resetting the save is fine when a test needs it; say so in the report.
- Play a win if the work touches M2's win path, per-level drops or rollback.
- Camera moves during Home's opening (any completion sequence) land wrong unless `cameraHandler.Initialize()` has run: before it the MainCamera sits offset (-12.69, -24.38) from the rig and the zoom target is 0. Use `HomeCameraFocusSequence`, not `CameraSequence` (that one touches the stale combat handler after a mission).
