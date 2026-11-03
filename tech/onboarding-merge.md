# Onboarding ↔ `thj/home-test`: merge notes

Owner: coordinator. Every edit `thj/onboarding` makes to a file `thj/home-test` also changes, and how to merge it (D-339). Add a row with each chunk that touches a shared file.

## Recipe

1. Merge as usual. For each conflicted file in the table: take `thj/home-test`'s version whole (`git checkout --theirs` or `--ours`, whichever side is home-test).
2. Open Unity, run **Tools › Onboarding › Apply Opening Setup** (commit `509a634dc`, `Features/Onboarding/Editor/`; plan `plans/onboarding/2026-10-31-onboarding-merge-safety.md`). Save or close any target first: Apply stops if a target scene, `Game Data.asset` or Mark's prefab has unsaved changes. Read its report lines, not just the problem count: the scene, pin and prefab steps are proved only on this branch's files.
3. Run EditMode: `OnboardingMissionGraphTests` and `OnboardingOpeningSetupTests` must pass.
4. Then the design-level questions below.

## Shared-file edits

| File | Onboarding edit | Commit | home-test changes it? | Dry run 2026-10-31 | Builder re-applies |
|---|---|---|---|---|---|
| `Resources/Game Data.asset` | Opening graph: Hearth initial → River, Ridge → AND → Trail → M4; old M1, M2, M3 ×2, M5–M7 nodes removed | `bb9982c87` | Yes: +8 Home sortie nodes, no edges | **Conflict** | Yes (keeps unknown nodes) |
| `Home - Scene.unity` | 4 world-map pins re-pointed (Hearth, River, Ridge, Trail) and renamed; M3 Mark Intro, M6, M7 pins hidden; Mark's select button and Upgrades tab unlock after the Hearth | `bb9982c87` | Yes: ~9.8k lines | **Conflict** | Yes (finds pins by mission, not name) |
| `Unit_Mark.prefab` | `unlockedAfterMission` → Hearth | `bb9982c87` | Yes: stat attribute lines | Auto-merges | Yes |
| `Scenes/IntroScreen.unity`, `Scenes/MainMenuScene.unity` | `initialMission` → Hearth | `bb9982c87` | No | Clean | Yes |
| `Unit_Mark.prefab` (again) | Fourth equipment socket (RightHand, empty) so the Wrist Wrap of Power equips; 5-line diff on top of the `unlockedAfterMission` edit | C5a, uncommitted | Possibly (stat attribute lines) | Not run | No: the builder doesn't add the socket; re-check after a merge (`MarkWeaponSocketTests`) |
| `Unit_Mark.prefab` (gear) | Socket defaults: Monk's Tunic (Chest), Wrist Wrap of Power (RightHand); fixed gear, upgrade only | `106edafec` | Possibly (stat attribute lines) | Not run | No: re-check after a merge (`MarkWeaponSocketTests`) |
| `Home - Scene.unity` (guided spend) | Guided skill spend component on `UpgradesPanel`: panel ref, Lucy after The River (Sidewinders), Linda after The Ridge (Longshot) | `14330fd06` | Yes (same file) | Not run | Yes: `OnboardingOpeningSetup.GuidedSpend.cs` (finds the panel by component; `GuidedSkillSpendTests` on a scene copy) |
| `AbilityTreePanelUI.cs`, `AbilityUpgradePanelUI.cs`, `AbilityUpgradeCharacterIconUI.cs` | `partial` keyword (1 line each, `59c5a6a25`); first tab via `SetState(Selected)` and selected tab grows (`35ed82daa`) | `59c5a6a25`, `35ed82daa` | Possibly (home-test UI edits) | Not run | No: code; conflicts only on those lines |
| `M4 - The White Mothers.asset` | Roster: Lucy, Linda fixed + 1 free pick, Toba excluded (was John, Linda, Lucy fixed) | C5a, uncommitted | Unknown | Not run | No (`M4SquadPickTests` checks the shape) |
| M4's 7 level prefabs: `Level2/LevelDomFight`, `Level2/Level2-C1-TArtEx`, `Level2/Level2-C2`, `Level2/Level2-C3-1`, `Level2/Level2-C3-2`, `Level3/Level3-C1`, `DungeonSafeRooms/LevelDivineRelicRoom 1` | Placed John replaced by a `Unit_Placeholder` deploy slot on his cell, facing kept; C2 loses a stale `decisions` override entry that pointed at John; C3-2's FP filler list drops John (Linda stays first) | C5a, uncommitted | Unknown (shared Level2/Level3 prefabs) | Not run | Yes, separate tool: take home-test's version whole, then run **Tools › Onboarding › Apply M4 Squad Slots** (`M4SquadSlots.cs`: re-runnable, replaces a placed John or an existing slot with a fresh one on the expected cell; `M4SquadPickTests` fails until done) |
| `Home - Scene.unity` (again) | Station locks: Workshop (`Equipments Cabinet`) after River or Ridge, Grandma Table after River and Ridge, Bookshelf, Training Field, Cooking Cabinet after M4; Family tab (`UpgradesPanel` entry flagged family) after The Trail; Workshop `tutorialSequence` set to its play-once page | C5b, uncommitted | Yes (same file) | Not run | Yes: `OnboardingOpeningSetup.Stations.cs` (stations found by GameObject name; needs the Workshop page asset from **Tools > Onboarding > Wire Home Visits**); `HomeVisitsTests` proves it on a copy of the scene |

New onboarding-only files (no conflict): the 4 Mission assets (`38bc7db73`), `OnboardingMissionGraphTests.cs` (`f36da02f8`). C5b adds, also onboarding-only: the Searching Home state, the Workshop page, The Trail's clue and Yard sequences (made by **Wire Home Visits**) and the `homeState`, `initiationSequence` and `completionSequence` fields on the Hearth, River, Ridge and Trail Mission assets.

## What the builder does not re-apply (C1b report)

- The `HomeStates-Idles` M4–M7 requirements: not touched. (Station unlock lists and the Family tab are now re-applied: see the C5b row above.)
- Home-test's sortie nodes: kept as they are, not gated (see below).
- Apply on a scene that really changes re-adds Unity's nine empty `GlobalEventBus` UnityEvent fields: strip or accept that noise in the diff.
- `Unit_Mark.prefab` is rewritten through prefab contents (a 4-line diff in the proof run): check its diff after the first real merge run.
- Check and Apply list a Problem when a mission it keeps lost its only prerequisite (it would open from the start).

## Design questions the merge raises (THJ)

- home-test's 8 Home sorties (GoblinCamp, OldWatchtower, MossyHollow, DrownedShrine, DeevBurrow, GoblinQueensWarren, GoblinScoutPost, ShamansCircle) are graph nodes with no incoming edge, so they are open from the start; with the onboarding graph they would be open before the Hearth. Gate them behind the Hearth (or a later mission)?
- home-test's world map in Home mode (`WorldMapPanelUI.RefreshHomeMode`, when a `HomeDayRunner` is present) hides every pin and shows clones bound to the Home sim's missions (prologue: `PrologueMapMission`). So the pins the builder restores only show outside Home mode; which mission the map offers first comes from the Home sim.
- home-test's prologue and day loop vs the Hearth memory: which opening wins on the merged branch.
