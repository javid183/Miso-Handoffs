# Home System: handoff (2026-10-15)

One-page snapshot of the Home system. Full history per step: the **Build Log** tab of the "Miso Home System" doc (https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN). Rules and numbers: the **Demo Spec** tab (local copy `claude-handoff/Miso-Home-System_Demo-Spec.md`). M9 design: the **M9 Readability Pass** tab (local copy `Miso-Home-System_M9-Readability.md`). Play checks and their results: `Playtest-Plan.md`.

## State

- Branch `thj/home-test`, code under `miso/Assets/_Project/Core/Systems/HomeSystem/{Runtime,Editor}`.
- **M0–M9 and the Oct 13–15 playtest fixes are built and committed** (not pushed). Last commits: `849c318ab` (FP gain animation) and `2f828e662` (Oct 15: day report saved, Kitchen forecast, recipe cards, Linda, tests). `origin/main` was merged three times: Step J `59a4f5cde` (Oct 3), Step K `182201e82` (Oct 4), Step L `5c8476822` (Oct 11).
- `GlobalSettings.pointConsumptionMode` stays 0 (FTP) on this branch; `origin/main` is ATB.
- EditMode tests (Oct 15, THJ): all green except `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, see `ai-regression-test-triage.md`). They now include 6 `ReportPersistence` tests. The `HomeIdleDirector` fix landed after that run; it compiles and was Play-checked.
- **Play checks:** Part A of the playtest plan was run on Oct 13 (Runs 1–3 and a fresh-save run from Day 1 to the Queen), and the open checks on Oct 14 (Claude, Days 1–5 with two sorties). The Oct 15 fixes were checked in Play. What is still open is listed in `Playtest-Plan.md`. Part B (cold playtest with a new player) has not been run.

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

One-time editor tools after a fresh checkout or a content rebuild (Play off): Build Demo Content, Add Combat Tags, Build House Traces, Add Bond Locks (then re-enter Play). The builder run order is in `CLAUDE.md`.

## Known issues (open)

From the Oct 13 runs unless dated otherwise. Details in the Build Log.

- **Combat UI:** no enemy-info panel on hover or click (Part 0 (k)). The stats screen shows "Max Damage Dealt 0" after a duo hit. The Defeat panel's objective name is empty. After a Loss the recap says "The family retreats from the dungeon". The AP pip from a dish has no icon yet. The Queen is named "Goblin Shaman" in logs.
- **Skill trees:** the Skill Trees button often needs two clicks; nodes show no description on hover until clicked. Suggestion from THJ: hide the level number when it is 0. Purchases survive a Play restart and Hide and Seek 1 makes 3 decoys (Oct 14–15); the other nodes' combat effects are not checked yet. Lucy's Sidewinders showed "Maxed Out" with no points spent on Oct 5 (not re-checked). `Healing Marks` carries Stat_WIS on both Linda and Toba: watch for a doubled heal. The combat log's LOADOUT line leaves out unlock nodes (Father's Resolve).
- **Home readability (Minor):** the Dining Table card shows raw log tags ("[DawnTick]", "[MorningResolve]"); the calendar's Day 1 badge is a blank square; mission cards put the purpose tag after the description, the Warren's "Cuts:" line repeats it, and the "Weakens the Queen" labels overlap; the Care badge repeats its text and once showed Kevin's refusal; Kevin appears in every seat picker with a blank portrait and a doubled name; Experiment is not marked as a risk; the Great Moon can't turn red (`HomeSkyDecay.GreatTint` multiplies cyan art: lerp toward red instead); "Go into the night" frames the roof, not the overview (3 of 3 nights); the lore-only Great Moon counts as chartable, so a lone stargazer on Night 1 is allowed; the recap strip's Unlocked column misses learned recipes and revealed missions (`HomeRecap` checks `StartsWith`, but the lines carry a source prefix); the Workshop badge says "Ready in 2 Dawns" while a helper works that day; Mary's and Ben's cards have no portrait; on Night 1 the Great Moon once took no clicks (not reproduced).
- **Presence:** Barks: a character whose avatar is hidden by an idle can't speak, so an uninvolved character takes the line (`assign:Yard(John)` spoken by Toba, `bond:(Mark,Toba)` by Linda); idle lines from seated characters and at night; idle lines alternate two speakers about every 50 s. Send-off: the free family at home doesn't walk to the Door.
- **Save:** Hold the Picnic and the finished war council are saved only at the next Dawn, so a Play restart right after shows them again. Editor only: Clear Save Data leaves skill-tree levels in memory until the editor restarts or recompiles.
- **Environment:** `InventorySidePanelUI.RefreshItems` throws when the Home scene is played directly (no `GameHandler`); start from PreloadScreen. The Claude desktop window can cover the top-right of the Game view during computer-use runs, so clicks there never reach Unity.
- **Data:** `BergsonsFaction.asset` gold costs are mixed after Step L (needs a consistency pass). Kevin's chore seats give +4 seat-slots a day where the design counted +2. Hens can go hungry by Day 6. John & Toba gain +16 Bond from one morning of Care (Toba's double Care Bond).
- **Older carry-overs:** hard-edged veils over closed rooms; banner "Tutorial 2 of 3" with 4 steps; empty sky above the house; `GameHandler.ResetProgress` → `EquipmentManager.Recreate()` reloads old saved equipment; "Unsupported type Vector2f" errors from `SceneManager.SaveScene`; Warren L2 imp summoning; mid-sortie quit.

## Not built yet (by choice or waiting on art)

- Dawn tick camera glide and sting; the Warren's own icon and corruption overlay; haul icons; the Queen's Might crack animation.
- The John Leaving cutscene (no runtime cutscene player). Candidate to replace the Send-off gathering: the `ToMountain` idle (Build Log, 4e addendum).
- Loot flying into the stores bar; preselecting a hero in the skill-tree panel (needs a Core change).
- Lit windows at night, dinner bell, Mary's and Ben's work idles, walk art for Mary and Ben; Toba has no Morta idle art; dish icons.

## Placeholder text still to write

All tagged `[PLACEHOLDER] ` (stripped on screen): 24 lines in `HomeDemoContentBuilder.cs` (prologue beats, room intros, Bond scenes, star charts, send-off lines, Great Moon line), 78 barks in `Content/Home/Barks/HomeBarks.csv`, headline lines, station introductions, the Linda–Toba Bond scenes. The Home Guide pages are plain text written from the rules. Propose wording to THJ first; edit the builder and re-run it.

## Open decisions (THJ)

- Fireside payoff: what else a pair can earn (Demo Spec open questions).
- Family growth: how Family level and FSP are earned, and a demo-sized slice of the family tree.
- Numbers to tune: Linda–Toba start 18/25, Toba's other pairs 6, Fireside FP cap +2, Kevin's yield.
- Whether to shift every Bond lock one level up and grant Lv 1 in the prologue.
- Idle family on the Porch earn Bond, while the moon tooltip says "Wandering the house, no Bond" for the others: intended?
- Workshop orders: allow cancelling or not.
- Masher counter limit, Dining T2 FTP scale, seat counts.

## Decisions on record

- Roster of 5 fighters (John, Linda, Lucy, Mark, Toba) plus Kevin, home-only (chore seats, no Bond, no sortie).
- Showcase pair Linda–Toba (decided 2026-10-12; the Toba–Mark duo is dropped). Bond Lv 2 grants their duo for free, no Family Skill Point (2026-10-13). Other Bond locks: Sisters' Rivalry and Command Shield Dash at Lv 2; Pass-By at Lv 1.
- Hungry Moon (Day 7 Omen): the Goblin Queen gains +1 AP at the start of each of her turns while below 50% HP (built 2026-10-14).
- The war council holds the moon until "To work" (2026-10-13).
- Stations open on a schedule after the prologue (`stagedUnlocks` on the cycle turns it off).
- Idle rule: the first two idle characters take the Porch seats for the idle Bond; everyone else stays at their own spot (no wandering).
- Picnic before the Win screen, with Skip. Loss at Dusk. "Returning home..." only on the two combat exits.
- Merges of `main` go through Claude Code; THJ commits. Home scene fallback: take main's scene and re-run the builders.
