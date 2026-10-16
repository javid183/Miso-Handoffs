# Status

Owner: coordinator. Every item has a scope: `all` or a branch. Started 2026-10-15 from the Home handoff (`archive/home-system-handoff.md`).

## Current state

- Working branch: `thj/home-test`. Last commit `e1a2deca8` (Oct 14, Hungry Moon), committed, not pushed.
- Home system M0–M9 and the Oct 13–14 playtest fixes are built and committed (details: `tech/home-system.md`, history: `build-log.md`).
- EditMode tests (Oct 13): 437 run, 436 pass; the one failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.
- Play checks: Part A of `playtests/playtest-plan.md` ran on Oct 13 (Runs 1–3 and a fresh-save run to the Queen). Part B (cold playtest with a new player) has not run.

## Now

| Item | Scope | Size | Owner | State |
| --- | --- | --- | --- | --- |
| Agent workflow setup (pass 3) | all | M | THJ + setup session | In progress |

## Next: pilots

| Item | Scope | Size | Path | Notes |
| --- | --- | --- | --- | --- |
| AP and points model: Fixed vs Shared AP; FTP vs ATB vs no resource at all for passives | all | L | Design | Tests the game designer, critics and Tier 3 format. Inputs: playtest findings in `design/` and the combat notes |
| Home report cards show an image tied to their context when one is assigned (e.g. a finished Workshop item's report card on the dining table shows the equipment's icon) | thj/home-test | M | Code | THJ's words, given as a plain statement on purpose |

## Waiting on THJ

**Workflow**

- Mirror syncs to the "Miso Home System" Claude Doc: the Claude Docs connector on THJ's personal account was refused access to its content on 2026-10-15 (the page itself opens). Run syncs from the company account, or share the doc's content with the personal account.
- Refresh the Claude project "Miso" docs from the new folder layout once setup is done.
- How and when `thj/home-test` merges into `main`, and whether FTP or ATB wins (`branches.md`).
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
- Combat effects per node and save/reload not checked yet.
- Lucy's Sidewinders showed "Maxed Out" with no points spent on Oct 5 (not re-checked).
- `Healing Marks` carries Stat_WIS on both Linda and Toba: watch for a doubled heal.

**Home readability (Minor)**

- The Dining Table card shows raw log tags ("[DawnTick]", "[MorningResolve]").
- The calendar's Day 1 badge is a blank square.
- Mission cards put the purpose tag after the description; the Warren's "Cuts:" line repeats it; the "Weakens the Queen" labels overlap.
- The Care badge repeats its text.
- Kevin appears in every seat picker with a blank portrait and a doubled name.
- Experiment is not marked as a risk.
- The Great Moon looks cyan, not redder, by Day 5.
- After Dusk to Night the camera once framed the Homestead side.

**Presence and barks**

- Linda shows twice at the Day 1 Dawn plan (bed idle plus avatar; recurs).
- Barks: wrong speaker on `assign:Porch`; idle lines from seated characters and at night; idle lines repeat about every 45 s.

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

- 2026-10-15: Agent workflow foundations and agents/loop design (Foundations and Pass 2 docs).
- 2026-10-13 to 14: Home playtest fixes. See `build-log.md`.
