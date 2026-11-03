# Onboarding structure C5: Home visits and the M4 send-off

Size: L (three chunks)    Tier: 3 (Home, D-180 workplan B5; questions Q1–Q4 below)    Assigned to: `miso-implementer` (sonnet) → `miso-reviewer` → THJ play check per chunk
Branch: `thj/onboarding`
Status: **approved 2026-11-02** (Q1 panel API D-356, Q2 stations locked until after M4 D-357, Q3 "Searching" HomeState D-358, Q4 clue scene on the Trail pin click D-359; details D-360). **C5a done**, committed `8826a11f1` (Mark weapon slot + test), `cafb8de97` (Apply M4 Squad Slots tool), `f6648ed08` (M4 roster, 7 levels, tests); review FIX ×2 → APPROVE; EditMode 1273/1274 known red only; THJ played M4 with John and with Mark OK (D-361 withdrawn by D-363, D-362). **C5b done**, committed `67b07c7f8` (Home visit data), `b2659da27` (Home scene), `cb85c30fe` (builder + wiring + tests); review FIX ×2 → APPROVE; EditMode 1288/1289 known red only; THJ played Hearth → River → Ridge → Trail OK (D-365, D-366). Open from the C5a carry-over: the Wrist Wrap upgrades but doesn't equip/show equipped on Mark (bug, investigating). C5c next

Rests on: structure tech § C5 (`plans/onboarding/2026-10-26-onboarding-structure-tech.md`), D-227 (M4 3 deploy slots, Toba placed), D-229 (Mark weapon slot, Wrist Wrap), D-230 (guided spend built, non-core Home component), D-231 (no Bond meter; Yard scene only), D-339/D-341 (shared-file edits go through Apply Opening Setup, light touch). Code facts: Explore check 2026-11-02 (summary under "Code facts").

## Why

C1–C4 made the missions playable, but Home between them still runs the old game: stations unlock after unlinked missions (never open), every new mission shows M4's Home look (fallback), there is no clue scene, and M4 places John so the squad pick does nothing. C5 is the last greybox chunk before the timed pacing check.

## Goal

Hearth → River ∥ Ridge → Trail → M4 send-off plays with three Home visits that each add one thing: Workshop after the first pair mission, skill tree with a guided spend after the second (plus the Map Table clue scene), Yard scene and Family tab after The Trail; M4 lets the player take John or Mark.

## Code facts (Explore, 2026-11-02, `thj/onboarding` @ `d72204178`)

- Home scene: `Features/Home - Imported/___Khashayar/Home - Scene.unity`. Station locks are scene components (`HomeInteractables.UnlockAfterMissions` + `oneUnlockedMissionCompletionIsEnough`): Workshop = `Equipments Cabinet` (old M3s, any), skill tree = `Grandma Table` (old M2 / M5, any), Bookshelf, Training Field, Cooking Cabinet (old missions, all). Fireplace (world map) open. None has a `tutorialSequence`.
- Family tab: scene override on `UpgradesPanel` `characters[5].requiredMissionToUnlock` = M3 Wolf (never opens). The builder (`OnboardingOpeningSetup.Scenes.cs:285`) already edits that array.
- `tutorialSequence` takes a `TutorialSequence` (pages) only; `PlayJustOnce` makes it once per save.
- No `homeState` on Hearth/River/Ridge/Trail → falls back to the scene default `M4 - HomeState` (Boardgame, MaryJohnFurniture). The `Mission.homeState` tooltip is wrong about "clears idles".
- `Mission.completionSequence` (any Sequence, e.g. `DialogNodeSequence`) plays on the next Home load after a won mission. `initiationSequence` plays when a pin is clicked, before the info panel.
- No pin reveal animation: a new pin glows (`isNewLevelButton`).
- Skill tree: `AbilityUpgradePanelUI` (`Core/UI/Runtime/Home/UpgradePanel/`) always selects `characterIcons[0]`; no API to preselect a hero or highlight a node. Not in `tech/core-systems.md`. Unspent-point badge exists only inside the panel (per-hero `newIndicator`); none on the Grandma Table.
- Last completed mission: `GameDataSO.GetLastCompletedMission()`.
- M4 (`M4 - The White Mothers.asset`): roster 3 fixed (John, Linda, Lucy), 0 free; 7 levels place their heroes, 0 deploy slots. Slot = `Unit_Placeholder` instance (as written by `level deploy`, example `GB_m2-trailhead.prefab:563`); `CombatLevelRunHandler.FillRosterSlots` fills it. Toba: `Unit_TobaEnemy` in `LevelDomFight`, placed `Unit_Toba` in levels 2–7.
- Mark: 3 sockets (Ring, Head, Chest), no weapon. Wrist Wrap of Power is RightHand (5), Mark only; adding a RightHand socket on `Unit_Mark.prefab` is prefab data.

## Acceptance criteria

C5a · M4 squad pick + Mark's weapon slot
- [ ] M4 roster: Lucy, Linda fixed + 1 free from {John, Mark} (Toba excluded from the pick); the character select offers John or Mark.
- [ ] Each of M4's 7 levels: John's placed instance replaced by a deploy slot on his cell, facing kept; Lucy, Linda, Toba/TobaEnemy and the Ryker NPC unchanged. **First check every sequence, trigger, objective or LSB in those levels for references to John's placed instance; if any, stop and report (don't rewire).**
- [ ] With John picked and with Mark picked, each M4 level loads with the pick on the slot (EditMode test: each M4 level has exactly one `Unit_Placeholder` and no placed John; roster shape).
- [ ] `Unit_Mark.prefab` gets a RightHand socket; the Wrist Wrap of Power equips on Mark in the Workshop (test: socket present, `Equip` accepts the Wrap).
- [ ] Logged in `tech/onboarding-merge.md` (M4 levels and the Mark prefab are shared with `main`/`thj/home-test`).

C5b · Home visits as data (stations, Home look, scenes)
- [ ] Workshop opens after River **or** Ridge; first open shows a new Workshop page once per save (`TutorialDataSO` + `TutorialSequence` with `PlayJustOnce`), placeholder text: gear up the pair going out next.
- [ ] Skill tree (Grandma Table) opens after River **and** Ridge. Family tab opens after The Trail. Bookshelf, Training Field, Cooking Cabinet open after M4 (D-357).
- [ ] New `Searching` HomeState (existing wolf-free quiet idles, e.g. LucySadSit, JohnWatchCliff, LindaSadLay, quiet Mary/Ben/Kevin idles; no Wolf idle) set as `homeState` on Hearth, River, Ridge and Trail (D-358); none falls back to `M4 - HomeState`.
- [ ] Map Table clue scene: `M2 - The Trail.initiationSequence` = a `DialogNodeSequence` with V2-3 to V2-7 (D-359).
- [ ] Yard scene stub: `M2 - The Trail.completionSequence` = a `DialogNodeSequence` with Y12-1 to Y12-4 (+ Q-4 if cheap). No Family point (B7).
- [ ] Every scene edit is applied by Apply Opening Setup (`OnboardingOpeningSetup.Scenes.cs`) and covered by its drift test; rows added to `tech/onboarding-merge.md`.
- [ ] Play check carried from C5a: the Wrist Wrap of Power equips on Mark in the Workshop.
- [ ] EditMode tests: station unlock lists, Family tab requirement, each new mission's `homeState`, Trail initiation/completion sequences set.

C5c · Guided skill spend (per Q1)
- [ ] After the second pair mission, the first open of the skill tree selects the sister from `GetLastCompletedMission()` (Lucy after River, Linda after Ridge) and highlights one node (her first purchasable node, data on the component); once per save. Later opens behave as now.
- [ ] No unspent-point badge on the Grandma Table is built (none exists; flagged, not built, per structure tech § C5).
- [ ] EditMode test for the sister pick (River last → Lucy, Ridge last → Linda) and the once-per-save rule.

All chunks: compile clean, EditMode with only `AIRegressionTest.Baseline_MatchesCurrentAI` red, private IDs out of code/assets, placeholder lines untagged (D-348) and listed in the report.

## Scope

In: the above. Out: the Family point and Sister's Rivalry choice (Bond Lite, B7); framed beats (B6); tally (B8); "stays home" lines S11-J/M (sequences can't branch on roster; leftover); a Grandma Table badge; the Hearth open Home state (C3 leftover, unless Q3's state covers it cheaply); final text and art; M2 XP/Gold values.

## Touches

Systems: Home scene (`HomeInteractables`, `UpgradesPanel` overrides), `HomeState` assets (data), Mission assets (data), M4 level prefabs (data), `Unit_Mark.prefab` (data), `AbilityUpgradePanelUI` / `AbilityTreePanelUI` (C5c, `Core/` folder UI, not on the core list), Apply Opening Setup builder. Core-list systems: Missions, GUnit, Level run read only; no change.
USPs: Home, Family Roles (indirect).
Docs: `tech/onboarding-merge.md`, `tech/home-system.md` note? (no, that is home-test's), `tech/combat-architecture.md` (only if a component is added), structure tech § C5 status, `status.md`, `build-log.md`; GDD `missions-structure.md` (M4 roster) via the designer later.

## Approach

C5a first (riskiest: John references in M4's sequences), then C5b, then C5c. One implementer run each, review, THJ play check, commits split (Mark prefab apart from M4 levels; builder/tool code apart from data).

## Risks

- **M4 sequences referencing John:** checked first in C5a; stop if found.
- **Shared files:** Home scene, Mark prefab, M4 levels → builder + merge notes (light touch, D-341).
- **Statics:** the C5c component holds none, or gets a `PlayModeStaticReset` hook.
- **Save:** once-per-save flags use the existing played-sequence tracker or the save; testing may reset the save (reports say so).
- **AI content:** M4 levels are not in `AIRegressionTest`'s set (to confirm); stays known red, never re-baselined.

## Questions for THJ

Answered 2026-11-02: Q1 (a) panel API in partials (D-356); Q2 locked until after M4 (D-357); Q3 new shared "Searching" HomeState (D-358); Q4 Trail initiationSequence (D-359).

## Gates

Per chunk: compile / EditMode (known red only) / review / THJ play check (C5a: M4 level 1–2 with John and with Mark; C5b: Hearth → River → Ridge → Trail Home visits; C5c: the guided spend after each order) / docs above.
