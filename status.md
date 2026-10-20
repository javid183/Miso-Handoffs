# Status

Owner: coordinator. Every item has a scope: `all` or a branch. Started 2026-10-15 from the Home handoff (`archive/home-system-handoff.md`).

## Current state

- Working branch: `thj/preview-improvements` (from `main` @ `5550286dd`, 2026-10-19). `thj/fr-readability` is merged into `main` (fast-forward). `thj/home-test` last commits `849c318ab` and `2f828e662` (Oct 15), committed, not pushed.
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
| Grid preview pass (`preview-pass`) | thj/preview-improvements | L | `miso-game-designer` (UI/UX study) → THJ → coordinator tech plan → implementer | Filed 2026-10-19 from THJ's playtest notes (`playtests/2026-10-19-preview-notes.md`, P1–P7: John's HUD FR tiles vs his zone, the tether line style, Shift sword reach, the Shift-hover narrowing, duplicate zones on Lucy and Linda, Linda's ghost reach over gaps, Shift sword icons everywhere). Design plan done 2026-10-19 (`plans/2026-10-19-preview-pass-design.md`, UX and systems critics ran): 23 previews inventoried, attack reach computed in 5 disagreeing places; bugs P1 (HUD hover leaks to the grid), P3 (`UnitThreatAnalysis` reach), P6 (ghost ignores ranged reach). THJ answered Q1 to Q6 (D-076 to D-081). Tech plan `plans/2026-10-19-preview-pass-tech.md`: C1–C8 built, reviewed (core chunks) and committed 2026-10-20 (17 commits, hashes in the plan; D-083 to D-086). EditMode 267/268 (known red). Play fixes after THJ's first check committed and confirmed in play 2026-10-20 (D-087 to D-089). GDD updated 2026-10-20 (`6c35455`: FR-8 to FR-13, CR-37 to CR-43). Open: the rest of the C9 checklist; the "Miso — Game Design" mirror tabs Family systems and Combat rules need syncing; merge to `main` |
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

- 2026-10-16: Mirror sync to the "Miso Home System" Claude Doc works again from THJ's personal account (ddgsignin): headers of the three tabs and two new Build Log sections synced.
- 2026-10-16: Claude project "Miso" docs refreshed to the new folder layout (same 8 docs, paths now match `claude-handoff/`; `tech/home-system.md` replaces the Home handoff).
- 2026-10-15: Agent workflow foundations and agents/loop design (Foundations and Pass 2 docs).
- 2026-10-15: Home playtest fixes 2 (`849c318ab`, `2f828e662`): day report saved, Kitchen forecast, recipe cards, Linda no longer shown twice at Dawn, FP gain animation. See `build-log.md`.
- 2026-10-14: Open-checks playtest run (Claude, Days 1–5, two sorties). See `build-log.md`.
- 2026-10-13 to 14: Home playtest fixes. See `build-log.md`.
