# Status

Owner: coordinator. Every item has a scope: `all` or a branch. Started 2026-10-15 from the Home handoff (`archive/home-system-handoff.md`).

## Current state

- Working branch: `thj/home-test`. Last commits `849c318ab` (FP gain animation) and `2f828e662` (Oct 15: day report saved, Kitchen forecast, recipe cards, Linda shown once at Dawn), committed, not pushed.
- Home system M0–M9 and the Oct 13–15 playtest fixes are built and committed (details: `tech/home-system.md`, history: `build-log.md`).
- EditMode tests (Oct 15, THJ): all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. They now include 6 `ReportPersistence` tests. The `HomeIdleDirector` fix landed after that run; it compiles and was Play-checked.
- Play checks: Part A of `playtests/playtest-plan.md` ran on Oct 13 (Runs 1–3 and a fresh-save run to the Queen), and the open checks on Oct 14 (Claude, Days 1–5 with two sorties). The Oct 15 fixes were checked in Play. What's still open is in the playtest plan. Part B (cold playtest with a new player) has not run.

## Now

| Item | Scope | Size | Owner | State |
| --- | --- | --- | --- | --- |
| Agent workflow setup (pass 3) | all | M | THJ + setup session | In progress |
| Pilot 1: AP and points model (`ap-points-model`) | all | L | `miso-game-designer` + critic | Design decided 2026-10-16 (D-034 to D-042, plan revision 4); docs synced. Code is **parked for `main`** (D-042): not built on `thj/home-test`; needs THJ on `main`, which adapts to FTP. Next: tech plan for `main` (check if the existing cooldown covers Mark's 1 charge). D-040 (Fireside) waits on the merge |
| Game Design Document (`gdd`) | all | L | main session | First full draft 2026-10-16 (D-044 to D-047): 14 pages in `design/gdd/`, mirrored to the "Miso — Game Design" Claude Doc. Values checked against `main` @ `92853a5a9`; once `_Project` was connected, every preset, level and core script it depends on was read too. Two independent checks found 27 errors, all fixed. Left to check in play: Pass-by and Family Trinket FTP (a float sent to an int method), Mark's Vault push on Immovable units, a wipe in M4's Level2-C2, and the Taunted status. Each page lists its open questions for THJ. Committed by THJ. 2026-10-17: `combat-balance.md`, `reward-balance.md` and `player-skill-trees.md` now link to the GDD instead of repeating its values (D-047), and `miso-game-designer` reads the GDD first |
| Pilot 2: Home report-card context images (`report-card-images`) | thj/home-test | M | Explore → coordinator tech plan → `miso-implementer` → verifier | Built, compiled, tests green (known red excepted), Play-checked by THJ. Waiting on THJ's yes to commit the code (2 commits proposed) |

## Next: pilots

| Item | Scope | Size | Path | Notes |
| --- | --- | --- | --- | --- |
(Both pilots are in "Now" above.)

## Waiting on THJ

**Workflow**

- GDD scope (raised 2026-10-17): THJ wants the GDD to describe the game as it is now, not future features (Planned/Proposed/Deferred/Dropped items). Options: move them to a `not-built.md`, delete them, or keep. THJ answers the GDD pages' open questions first, then decides. Amends D-044/D-047.
- How and when `thj/home-test` merges into `main` (`branches.md`). FTP wins (D-036 to D-042).
- Fill the "[THJ] To add" part of `vision.md`.

**Home (from the handoff's open decisions)** — scope `thj/home-test`

- Fireside payoff: what else a pair can earn (Demo Spec open questions).
- Family growth: how Family level and FSP are earned, and a demo-sized slice of the family tree.
- Numbers to tune: Linda–Toba start 18/25, Toba's other pairs 6, Fireside FP cap +2, Kevin's yield.
- Whether to shift every Bond lock one level up and grant Lv 1 in the prologue.
- Idle family on the Porch earn Bond while the moon tooltip says "Wandering the house, no Bond" for the others: intended?
- Workshop orders: allow cancelling or not.
- Masher counter limit, Dining T2 FTP scale, seat counts.

## Inbox

(New requests land here before triage.)

## Backlog

Known issues carried over from the Oct 13 runs unless dated otherwise. All scoped `thj/home-test` unless marked. Details in `build-log.md`.

**Combat UI**

- No enemy-info panel on hover or click (Part 0 (k)).
- Stats screen shows "Max Damage Dealt 0" after a duo hit.
- Defeat panel's objective name is empty.
- After a Loss the recap says "The family retreats from the dungeon".
- The AP pip from a dish has no icon yet.
- The Queen is named "Goblin Shaman" in logs.

**Skill trees** (scope: check whether these also apply on `main`)

- The Skill Trees button often needs two clicks; nodes show no description on hover until clicked.
- Suggestion from THJ: hide the level number when it is 0.
- Purchases survive a Play restart and Hide and Seek 1 makes 3 decoys (Oct 14–15); the other nodes' combat effects are not checked yet.
- Lucy's Sidewinders showed "Maxed Out" with no points spent on Oct 5 (not re-checked).
- `Healing Marks` carries Stat_WIS on both Linda and Toba: watch for a doubled heal.
- The combat log's LOADOUT line leaves out unlock nodes (Father's Resolve).

**Home readability (Minor)**

- The Dining Table card shows raw log tags ("[DawnTick]", "[MorningResolve]").
- The calendar's Day 1 badge is a blank square.
- Mission cards put the purpose tag after the description; the Warren's "Cuts:" line repeats it; the "Weakens the Queen" labels overlap.
- The Care badge repeats its text and once showed Kevin's refusal.
- Kevin appears in every seat picker with a blank portrait and a doubled name.
- Experiment is not marked as a risk.
- The Great Moon can't turn red: `HomeSkyDecay.GreatTint` multiplies cyan art (lerp toward red instead).
- "Go into the night" frames the roof, not the overview (3 of 3 nights).
- The lore-only Great Moon counts as chartable, so a lone stargazer on Night 1 is allowed.
- The recap strip's Unlocked column misses learned recipes and revealed missions (`HomeRecap` checks `StartsWith`, but the lines carry a source prefix).
- The Workshop badge says "Ready in 2 Dawns" while a helper works that day.
- Mary's and Ben's cards have no portrait.
- On Night 1 the Great Moon once took no clicks (not reproduced).

**Presence and barks**

- Barks: a character whose avatar is hidden by an idle can't speak, so an uninvolved character takes the line (`assign:Yard(John)` spoken by Toba, `bond:(Mark,Toba)` by Linda); idle lines from seated characters and at night; idle lines alternate two speakers about every 50 s.
- Send-off: the free family at home doesn't walk to the Door.

**Save**

- Hold the Picnic and the finished war council are saved only at the next Dawn, so a Play restart right after shows them again.
- Editor only: Clear Save Data leaves skill-tree levels in memory until the editor restarts or recompiles.

**Environment**

- `InventorySidePanelUI.RefreshItems` throws when the Home scene is played directly (no `GameHandler`); start from PreloadScreen.
- The Claude desktop window can cover the top-right of the Game view during computer-use runs, so clicks there never reach Unity.

**Data**

- `BergsonsFaction.asset` gold costs are mixed after Step L (needs a consistency pass).
- Kevin's chore seats give +4 seat-slots a day where the design counted +2.
- Hens can go hungry by Day 6.
- John & Toba gain +16 Bond from one morning of Care (Toba's double Care Bond).

**Older carry-overs**

- Hard-edged veils over closed rooms; banner "Tutorial 2 of 3" with 4 steps; empty sky above the house.
- `GameHandler.ResetProgress` → `EquipmentManager.Recreate()` reloads old saved equipment (scope: check `main`).
- "Unsupported type Vector2f" errors from `SceneManager.SaveScene`.
- Warren L2 imp summoning; mid-sortie quit.

**Not built yet (by choice or waiting on art)**

- Dawn tick camera glide and sting; the Warren's own icon and corruption overlay; haul icons; the Queen's Might crack animation.
- The John Leaving cutscene (no runtime cutscene player). Candidate to replace the Send-off gathering: the `ToMountain` idle.
- Loot flying into the stores bar; preselecting a hero in the skill-tree panel (needs a Core change).
- Lit windows at night, dinner bell, Mary's and Ben's work idles, walk art for Mary and Ben; Toba has no Morta idle art; dish icons.

**Placeholder text to write** (narrative; propose wording to THJ first)

- 24 lines in `HomeDemoContentBuilder.cs` (prologue beats, room intros, Bond scenes, star charts, send-off lines, Great Moon line), 78 barks in `Content/Home/Barks/HomeBarks.csv`, headline lines, station introductions, the Linda–Toba Bond scenes. All tagged `[PLACEHOLDER] `.

**Workflow**

- The AI regression test fix: dedicated session (scope all; see `tech/ai-regression-test-triage.md`).
- Test headless checks (dotnet build, batchmode, a Unity MCP package) on their own before adding them to the workflow (scope all).

## Done recently

- 2026-10-16: Mirror sync to the "Miso Home System" Claude Doc works again from THJ's personal account (ddgsignin): headers of the three tabs and two new Build Log sections synced.
- 2026-10-16: Claude project "Miso" docs refreshed to the new folder layout (same 8 docs, paths now match `claude-handoff/`; `tech/home-system.md` replaces the Home handoff).
- 2026-10-15: Agent workflow foundations and agents/loop design (Foundations and Pass 2 docs).
- 2026-10-15: Home playtest fixes 2 (`849c318ab`, `2f828e662`): day report saved, Kitchen forecast, recipe cards, Linda no longer shown twice at Dawn, FP gain animation. See `build-log.md`.
- 2026-10-14: Open-checks playtest run (Claude, Days 1–5, two sorties). See `build-log.md`.
- 2026-10-13 to 14: Home playtest fixes. See `build-log.md`.
