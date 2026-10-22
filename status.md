# Status

Owner: coordinator. Every item has a scope: `all` or a branch. Started 2026-10-15 from the Home handoff (`archive/home-system-handoff.md`).

## Current state

- Working branch: `thj/quick-wins` (THJ, 2026-10-21, from `main`). Bundle A plan approved (`plans/2026-10-21-quick-wins-a-tech.md`). C1 (one-click cancel) committed `64fbabef5`, play-checked by THJ. C2 (John's shield variants) committed `dd567cdbc`, `7716c3a8c` (+ THJ's run tweak `51058e216`), play-checked. C3a (stepped HP preview + lethal skull, D-134 to D-136) committed `11af7b05c`, `ef14a0d80`, `127c6964e`, play-checked; C3c (label) dropped (D-137). C3b ("fires" cursor) committed `879f560f9`; THJ repaints `cursor_fire.png` and play-checks it later. C4 (objectives panel open, click toggles, D-138) committed `785374c51`, play-checked. Next: C5 (enemy idle desync). Before that `main` @ `df58c4c0c`. THJ merged `masher-tweak` into it on 2026-10-21 (fast-forward, 18 commits); compiles clean, EditMode as expected (known red only). Next: a quick-wins branch THJ creates from `main` (D-111). Before that `masher-tweak` (2026-10-20, from `main` @ `4f2668918`), and before that `main` (THJ merged `thj/preview-improvements` into it on 2026-10-20; `thj/fr-readability` merged 2026-10-19). `thj/home-test` last commits `849c318ab` and `2f828e662` (Oct 15), committed, not pushed.
- Home system M0–M9 and the Oct 13–15 playtest fixes are built and committed (details: `tech/home-system.md`, history: `build-log.md`).
- EditMode tests (Oct 15, THJ): all green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. They now include 6 `ReportPersistence` tests. The `HomeIdleDirector` fix landed after that run; it compiles and was Play-checked.
- Play checks: Part A of `playtests/playtest-plan.md` ran on Oct 13 (Runs 1–3 and a fresh-save run to the Queen), and the open checks on Oct 14 (Claude, Days 1–5 with two sorties). The Oct 15 fixes were checked in Play. What's still open is in the playtest plan. Part B (cold playtest with a new player) has not run.

## Now

| Item | Scope | Size | Owner | State |
| --- | --- | --- | --- | --- |
| Agent workflow setup (pass 3) | all | M | THJ + setup session | In progress |
| Pilot 1: AP and points model (`ap-points-model`) | all | L | `miso-game-designer` + critic | Design decided 2026-10-16 (D-034 to D-042, plan revision 4); docs synced. Code is **parked for `main`** (D-042): not built on `thj/home-test`; needs THJ on `main`, which adapts to FTP. Next: tech plan for `main` (check if the existing cooldown covers Mark's 1 charge). D-040 (Fireside) waits on the merge |
| Game Design Document (`gdd`) | all | L | main session | First full draft 2026-10-16 (D-044 to D-047): 14 pages in `design/gdd/`, mirrored to the "Miso — Game Design" Claude Doc. Values checked against `main` @ `92853a5a9`; once `_Project` was connected, every preset, level and core script it depends on was read too. Two independent checks found 27 errors, all fixed. Left to check in play: Pass-by and Family Trinket FTP (a float sent to an int method), Mark's Vault push on Immovable units, a wipe in M4's Level2-C2, and the Taunted status. Each page lists its open questions for THJ. Committed by THJ. 2026-10-17: `combat-balance.md`, `reward-balance.md` and `player-skill-trees.md` now link to the GDD instead of repeating its values (D-047), and `miso-game-designer` reads the GDD first |
| Oct 2026 playtest tasks (`playtest-tasks-oct`) | all (code on `main`) | L | Coordinator triage → designer / tech plans | Filed 2026-10-18 in `playtests/2026-10-playtest-tasks.md` (4 batches, 10 blockers). Triage 2026-10-18 on `thj/oct-build-fixes` (= `main`). Root causes found (Explore). THJ decided: B1 placeholder state + safety net (D-052), B9 held for S3 (D-053), B3 display only (D-054), Q21 bundled with S10 (D-055). Plan `plans/2026-10-18-playtest-batch1-bugfixes.md` (B1, B3, B6, B8; chunks C1 to C5, one commit each): **C1 in progress** (implementer). C1 committed (`7f85fbbf7`); C2 committed (`952ab9d5a`, reviewer APPROVE); C3 `66481e4e1`, C4 `cabdb63a6`, C5 `01e561ad2` committed; C6 `47cee8ad9` (B5 diagnostic) committed; waiting on THJ's repro. Play check 2026-10-18: verifier had no computer use, so compile (clean), suite (78/79, known red) and B1 static checks passed and every in-game item is Not run (`reports/playtest-batch1-verify.md`); Desktop play check done (`reports/playtest-batch1-verify-play.md`): B1 no freeze, B8 lock and restore, B6 world map at 3 ratios and B3 at whole-number HP seen in play; still unseen: corrupted tile clearing, fractional HP, mission map, turn-change tutorial. B5 waits for THJ's repro. Commit hashes are logged in the plan (no Co-Authored-By from now on). B5 (Workshop): Explore found no code path where the Workshop looks unlocked while `_isLocked` is stale (`GameHandler.EndMission` sets `Completed` before Home reloads), so the cause is unconfirmed; candidates are input gating after the mission-completion sequence (`HomeManager.StartIE`), an empty panel on first open (`WorkshopPanelUI.ShowPanel` filters), or a collider/UI covering it. Next: a temporary diagnostic log (THJ repro) and a cheap `RefreshLock()` hardening. The first-purchase Owned-not-Equipped behaviour is by design (equip is in the character equipment panel); only a design question remains. Follow-up to schedule after Batch 1: an `abilityActivationFrame` at or past the clip's last frame also freezes an ability (`EntityAnimationHandler.cs:97-100`). Still to route: B2, B10 (QA), B4, B7 (narrative), then Batch 3 quick wins; design items (S1, S8, S3, S4, S6, S9, S10) and new systems (Q18, Q19, Q20) are Tier 3 and go to the designer / THJ |
| Family Role readability (B4, Q7 part) | all (merged into `main` 2026-10-19) | L | coordinator + implementer | Phase 0 (F1, F3, F5) and Phase 1 (zones, Shift view on its own layer, cover icons with strict fist, role badge, John's tether, prompt/execute/decline barks) built, reviewed and committed 2026-10-18/19 (hashes: `plans/2026-10-18-family-role-phase0-1.md`; decisions D-062 to D-072). Play check ready to run (checklist `playtests/2026-10-19-b4-play-check.md`, desktop prompt `playtests/2026-10-19-b4-play-check-prompt.md`); B1 is DONE (THJ tested the corruption pool cleanse and fixed Mark's animation). Not played yet: combined play check (Phases 0 and 1, plus the Batch 1 items still unseen). Batched into the later **Family Role chunk** (index: `plans/family-role-chunk.md`) with Pilot 1 (D-036 to D-042, D-061): F4 (Mark footprint, patch in `reports/b4-f4-mark-footprint.patch.md` plus a footprint-aware `AEffectDashAttack`), the reason-code event, role queue (cap undecided), Mark answering when also hit, teleports for Linda, the miss-silence scope, the stun rule, Watch wording, Fireside pip, Q7 popup. 2026-10-19: per-unit role-zone icons in fixed quadrants (D-075, `plans/2026-10-19-role-zone-unit-sprites.md`): built, reviewed (APPROVE), compile clean, EditMode 190/191 (known red); committed `f2de13678`, `4d2f8c1a4`, `a7e28f0f4`; play check pending. Follow-ups: enemy movement tint on the Shift layer (with Q20); clear the Shift preview when ability targeting starts; Mark's colour is very dark |
| Pilot 2: Home report-card context images (`report-card-images`) | thj/home-test | M | Explore → coordinator tech plan → `miso-implementer` → verifier | Built, compiled, tests green (known red excepted), Play-checked by THJ. Waiting on THJ's yes to commit the code (2 commits proposed) |

## Next: pilots

| Item | Scope | Size | Path | Notes |
| --- | --- | --- | --- | --- |
(Both pilots are in "Now" above.)

## Waiting on THJ

**Workflow**

- GDD open questions are asked on demand (D-050); THJ answers in `design/gdd-open-questions.md` when he likes.
- GDD scope (raised 2026-10-17): THJ wants the GDD to describe the game as it is now, not future features (Planned/Proposed/Deferred/Dropped items). Options: move them to a `not-built.md`, delete them, or keep. THJ answers the GDD pages' open questions first, then decides. Amends D-044/D-047.
- How and when `thj/home-test` merges into `main` (`branches.md`). FTP wins (D-036 to D-042).
- Fill the "[THJ] To add" part of `vision.md`.

**Narrative (Q1/Q2 proposals, 2026-10-20)** — scope all; all Tier 3; details `reports/narrative-q1-q2-proposals.md`

- Q2-1 reading (Lucy and John share the concern), masked man setup + mask reason + "Masked Stranger" plate, thief line, Grandma Margaret alive or dead, why they go home after A Wolf's Blood, forms of address, forest name, Q1 M1/M2 slice and its four S8 beats.

**Feedback pass (Q5/Q6/Q24, 2026-10-20)** — scope all; Tier 3 (game feel); `plans/2026-10-20-feedback-pass-design.md`

- Answered 2026-10-20 (D-113): hit-stop postponed; bars on every unit; 25%; heartbeat once; skull always; placeholders. Open: kill flash + shake in or out. Then designer revises the plan.

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

- 2026-10-21 `b4-masher-play-findings` (all unless noted; from `reports/b4-play-check.md`, not triaged): B4 seen in play: John's zone shape and follow-on-move, Linda/Lucy zone hide, badge pip and no-role case, John's tether (present; near-invisible on dark `LevelE3-C1`), John and Linda prompt/execute barks, B3 damage preview and mission icons, B6 mission map at 3 ratios, B7 Mithra's Gift text and exit Success. Not run: F1, F3, F5, cover icons, all Shift items (Claude can't hold Shift across a capture), Lucy/Mark barks, decline barks, B8, D-066, fractional HP. New issues: (1) role-zone and cover glyphs too low contrast (biggest readability problem); (2) tether contrast on dark floors; (3) mission map clips the first and last node at 4:3; (4) DOTween warnings on every unit death from `ATBGaugeViewMarker` (an ATB gauge still ticks in `GUnit.Update` on FTP); (5) enemy `80/80` reads as `00/00` in the pixel font; (6) two barks stacked a tile apart; (7) Mark's badge tooltip has the Linda/Lucy "Shift shows them" line; (8) `PlayerController.prefab:1447` still binds `LucyQTE`; (9) Masher badge on enemies: Claude leans to hiding it. THJ 2026-10-21: B4 and the Shift/preview items count as done and checked (long play session, nothing off); the "Zones (A)" line is probably not superseded (unsure). Items (1)–(9) still to triage.

- 2026-10-21 `strip-private-ids` (all; tool/cleanup, M, Tier 2, THJ asked): remove decision, plan and playtest IDs from code comments, tooltips, log messages and test names across `_Project` (about 174 hits in 56 files, regex sweep), replacing them with plain descriptions. Done 2026-10-21: `08bb27ac5` (48 files, comment and tooltip text only; EditMode 412/413, known red only). Rule added to `conventions.md`, `CLAUDE.md` and the implementer and reviewer agent masters (THJ to sync `.claude/agents`).

- 2026-10-20 `quick-wins-triage` (all; playtest Batch 3, paper plan + triage, M): THJ asked for it. Triage written: `plans/2026-10-20-quick-wins-triage.md` (bundles A plain fixes, P pace, F feedback design, S9 chain, N narrative). THJ answered W1–W4 (D-107 to D-111). Queued after Masher on a quick-wins branch; N (narrative Q1/Q2) and the F design pass can run in parallel.

- 2026-10-20 `masher-reckless-tank` (**merged into `main` 2026-10-21**; design, M, Tier 3: changes a built enemy rule, EN-2/EN-3, and GDD Q2). THJ: the Masher's counter should hit only its attacker, only during the player's turn, only from an adjacent tile, and not at all when it can't reach; its slam currently hits an area (several targets, its own side too). Goal: a reckless tank that is challenging but that the player can steer around and avoid. Routed to `miso-game-designer` for options and a recommendation (`plans/2026-10-20-masher-reckless-tank-design.md`). Designer plan rev 1 done (Option A); THJ decided D-092 to D-098 (roles/duos provoke, always step, single-target aim then plus splash incl. own side, counter = copy of the slam, Role-provoke bool default true, no limit). Design rev 2 done; THJ answered O1 (cap 10, D-099) and O2 (answer after the current enemy action, D-100). Tech plan `plans/2026-10-20-masher-reckless-tank-tech.md` approved (T1-T4 all (a), D-101 to D-105). Branch `masher-tweak` (THJ). C1 built (`reports/masher-c1.md`); reviewer FIX (`reports/masher-c1-review.md`): hold OK, AI wait needs a same-step recheck (D-106, THJ yes). Fixed; re-review APPROVE; verify PASS (compile clean, EditMode 282/283, known red only; `reports/masher-c1-verify.md`). Commit 1 `08ca1d819` (AI wait + recheck); commit 2 `11f64c19f` (turn-switch hold). C2 committed `212638ad2` (review APPROVE, EditMode 326/327 known red only). C3 committed `e409b2c94`, `519e05d9e` (review APPROVE; Masher panel now shows a role badge, check in play). C4 (handler rewrite) built (`reports/masher-c4.md`; EditMode 344/345, known red only); rev 1–2 (D-115 to D-117), re-review APPROVE, verify PASS (EditMode 356/357). Committed `7556630a6`, `d5402d48d`, `9e6d50f51`. C5 committed `1a0936a28`, `256bcade6` (review APPROVE after D-118). All chunks committed. Play check 2026-10-20 (THJ): items 1–15 pass, 16–23 not run. Bugs found: John's role never relays Masher attacks/answers (pre-existing); Masher move-preview ghost faces the wrong way; red screen overlay stays after a Masher hit (even at full HP, survives unit switch). Fixed: stuck red overlay `f5778df92` and ghost facing `4e51d365f` (review APPROVE, EditMode 364/365). John relay committed (`9ec1c4c29`, `a7ec2f352`, `82ba0b82a`, `a13dd1f6c`; D-119, D-120, D-123 to D-129). THJ `df58c4c0c` (2026-10-21): Mark–Lucy Duo damage up, Masher slam damage down (the counter shares the slam's AttrMod, D-114, so its damage drops too). THJ idea (undecided): Masher tramples whatever is in its way, enemies included → design question. Claude play check 2026-10-21 (`reports/b4-play-check.md`, about a quarter of the checklist): item 1 pass, 2 badge present (title unreadable), **3 fail: no step ghost or path while aiming from 5 tiles; 6 fail: Linda's ranged hit from 5 tiles gave no step and no counter** (`LevelM1-C3`; cause unknown, `Immovable` ruled out by THJ; the level instance has no handler overrides; leads: the report's header names `thj/fr-readability` as the branch, so confirm the editor was on `masher-tweak`; whether the bow hit's damage event carries an owner; the Masher also did nothing in R1). Items 4, 5, 7–31 not run. THJ 2026-10-21: items 3 and 6 work (tested many times), so the Claude-run failure is a harness artefact, not a bug; THJ's long play session stands as the check for the rest. Open: hide the Masher's Family Role badge on enemies? (asked) Note: `AIRegressionTest` references the Masher; the known-red baseline must not be re-baselined by this work.

- 2026-10-19 `b5-workshop-click` (all; bug, S/M, Tier 2): THJ's repro log. Lock is correct (`Equipments Cabinet` isLocked=False on Awake/OnEnable after M3 - Mark Intro), but no `OnPointerEnter`/`OnPointerDown` fired on any `HomeInteractables` after `@Mission3MarkIntro_End_DialogNodeSequence`. So pointer events never reach the colliders: a raycast blocker or disabled input, not the lock. Explore 2026-10-19: dialog/sequence code, dialogue panel and tutorial input lock ruled out (none touch EventSystem/raycaster; panel root deactivated on hide). Lead 1: `Anim_IntroAnimation.anim:652-679` keys MainCamera's `Physics2DRaycaster` enabled 0 until t=5 and the Home Animator (WriteDefaults on) keeps owning it; doesn't yet explain why only M3's end dialog. Lead 2: a collider/canvas over the screen (cabinet indicator object). Lead 3: a second EventSystem. THJ 2026-10-19: every other Home object works, only the Workshop is dead; Stop/Play fixes it (so lead 1 is out). D-073: click-hit diagnostic built (`HomeInteractables.cs` +83, uncommitted, compiles; report `reports/b5-click-diag.md`). THJ rerun 2026-10-19 (it worked this time): the click diagnostic shows two colliders tied at the Workshop spot, `Equipments Cabinet` (HomeInteractables) and `Workshop Cabinet` (Home.prefab, other component), same layer, z, sorting and distance, so the EventSystem's pick between them can flip. Explore 2026-10-19 (re-run): **root cause found.** `Workshop Cabinet` (`Home.prefab:64373`, path `Home/House/Visual/Uncle Ben Room/Workshop Cabinet`) is a leftover BoxCollider2D with no script (4.32 x 5.28, fully contains the cabinet's 2.36 x 3.14 box). Neither object has a renderer on the collider's GameObject and both sit at z 0, so the raycaster tie falls to Physics2D's result order. That order is arbitrary and can change when M3's HomeState spawns the `BenJoeyGrind` idle actors, which have colliders, in Ben's room. A click that lands on Workshop Cabinet finds no handler. Same leftover pattern as the other `* Cabinet` colliders: the scene already removes Training Cabinet's collider (`m_RemovedComponents`) and reuses Cooking Cabinet's. Nothing reads the Workshop one, and no builder exists on this branch. THJ's uncommitted scene override (`m_Enabled: 0` on fileID `61089915482654192`) is exactly the fix. Proposed fix: keep that override (or remove the component, as was done for Training Cabinet), revert every `[B5-DIAG]` line, commit only the scene hunk (the scene diff also carries unrelated empty-UnityEvent noise). Latent: the unused MortaStory actor `Equipments Cabinet.prefab` (id 203, idle `Idle Cabinet Workshop`) has the same big collider, and the bug comes back if that idle is ever spawned. THJ approved (D-074). [B5-DIAG] code removed (`reports/b5-diag-removal.md`); compile clean, EditMode 174/175 (known red only) (`reports/b5-diag-removal-verify.md`). Committed 2026-10-19: `da54e4ec2` (scene override), `b3e4c030e` (diag removal). Not run: Workshop click after M3 in Play. `thj/oct-build-fixes` still carries the C6 diagnostics. Console also shows an "Internal error - unexpected guid mismatch" entry, not investigated.

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

- 2026-10-19 (scope all): the unused MortaStory actor `Assets/MortaStory/Content/Story/Actors/Equipments Cabinet.prefab` (id 203, idle `Idle Cabinet Workshop`) has a 4.28 x 5.2 BoxCollider2D; if that idle is ever spawned it steals the Workshop click again (B5).

- 2026-10-19 (scope all; narrative): Linda's role description still ends "(1 FP)" (old spelling, and roles are meant to be free, D-036 to D-042); the role badge tooltip titles are dev labels ("Linda's FactionRole", "Lucy's FR"). Renaming them is a Tier 3 naming pass.

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

- 2026-10-20: Grid preview pass (`preview-pass`): THJ's notes P1–P7 plus the designer's audit, built in C1–C8 and two rounds of play fixes (about 24 commits, hashes in `plans/2026-10-19-preview-pass-tech.md`; D-076 to D-091). All play-checked by THJ and merged into `main`. GDD FR-8 to FR-13 and CR-37 to CR-43 written; the mirror needs a re-sync for the post-merge status labels. Follow-ups: `GUnit.ShowThreatLineTo` could use `ArcLine` (core); `GridCell.CoverIcon.cs` and the `CoverFist`/`CoverShield` sprites are unused since C7; THJ keeps them for now (2026-10-20).

- 2026-10-16: Mirror sync to the "Miso Home System" Claude Doc works again from THJ's personal account (ddgsignin): headers of the three tabs and two new Build Log sections synced.
- 2026-10-16: Claude project "Miso" docs refreshed to the new folder layout (same 8 docs, paths now match `claude-handoff/`; `tech/home-system.md` replaces the Home handoff).
- 2026-10-15: Agent workflow foundations and agents/loop design (Foundations and Pass 2 docs).
- 2026-10-15: Home playtest fixes 2 (`849c318ab`, `2f828e662`): day report saved, Kitchen forecast, recipe cards, Linda no longer shown twice at Dawn, FP gain animation. See `build-log.md`.
- 2026-10-14: Open-checks playtest run (Claude, Days 1–5, two sorties). See `build-log.md`.
- 2026-10-13 to 14: Home playtest fixes. See `build-log.md`.
