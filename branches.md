# Branches

Owner: coordinator; THJ approves. `claude-handoff/` doesn't change when the shared repo switches branches, so this file says what's different on each active branch.

**Rules**

- Every task, backlog item and decision is scoped `all` or to one branch.
- Active work = everything scoped `all` + everything scoped to the current branch. Work scoped to another branch is parked.
- A design rule that differs is written once in its design doc, with its variant: "**On `thj/home-test`:** ...".
- Agents never switch branches. THJ does.
- On merge, a branch's differences fold into `all`. If that changes a core rule on `main`, it's Tier 3.

## `thj/onboarding-demo`

- Created 2026-11-22 by the coordinator at THJ's request ("Before you commit anything create a branch. I said main, but now that i think it is safer to create a branch") from `main` @ `551685704`. THJ's working branch. Reverses D-602's "build on `main`" (D-604).
- **Purpose:** the onboarding demo, the Hearth to the end of M4 (`plans/2026-11-22-onboarding-demo.md`).
- Combat resource and AP: same as `main`.
- 2026-11-23: Phase 1, Mark's kit, M1 and two play-check fixes committed (`c9bdad3c6`..`500bfd1e0`); `32c7e3cf2` intro/outro sequences on; **`origin/main` merged in** (`55f51381b`, D-642: Khash's save-file restructure, enemy awareness and future-target displays off by default, custom cursor off, Archer Goblin WebThrow assets added, ability removed from the prefab). 11 ahead of `origin/thj/onboarding-demo`, not pushed. Local `main` is still behind `origin/main` (not moved).
- 2026-11-24: THJ committed `f20f9a5ab` (M1 ridge level) and `db4a47acd` (Vault in Mark's tree), pulled `origin/thj/onboarding-demo` (`ce501c603`), then **`origin/main` merged in again** (`5a47ca5e0`, D-649: Khash's pixel warning sign and backgrounds on the Ground layer; clean). Not pushed. Compiled and tested 2026-11-24 (8 `M1RidgeTests` fail on THJ's M1 rework, expected, D-651). Then `8b76218b4` Whirl hits passed enemies, `13f354a8c` Family tree auto-open, `b55771c90` core: late ability completion charges the unit that acted (also needed on `main`). Not pushed.
- 2026-11-25: **`origin/main` merged in again** (`bb62bdd2d`, at THJ's request; Khash's Family menu / Bonds menu, pause-menu Family entry, `showSelectionIndicatorForAllFactions` setting; 7 commits, 94 files; no conflicts). THJ had reset their local `GlobalSettings.asset` edit (`deactivateIntroOutroSequences: 1`) first because main also edits that file, so the merged value is `0`. THJ compiled it and ran the EditMode suite in the editor on 2026-11-25 and reports it ran cleanly (I haven't seen the results file; the batch-mode run failed on a Unity license error, not on the code). Pushed: `origin/thj/onboarding-demo` = `bb62bdd2d` (checked 2026-11-25). Local `main` is still behind `origin/main`.
- Uncommitted in the tree (came along, THJ's, agents leave them alone): `LevelM2-C1.prefab`, `PreloadScreen.unity`, the TMP fallback font, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, untracked `Content/FamilySuperTime/DUO/Inserts/`.

## `thj/duo-insert` (merged into `main` 2026-11-22)

- Created 2026-11-22 by the coordinator at THJ's request ("Go to a new branch then commit it") from `main` @ `6474ed314` (61 ahead of `origin/main`, not pushed). THJ's working branch.
- **Purpose:** the duo insert shot test, Mark–Lucy (`plans/2026-11-22-duo-insert-shot-tech.md`, `design/duo-insert-shot.md`).
- `9e992707f` C1: insert player, QTE card, Mark–Lucy test entry. `5fc81e789` C2: the duo flow (QTE card first, insert, then act; Mark–Lucy only). `02b727e2b` start/end transitions, longer timing, tunables; `58ecd7ec8` the QTE's own keys don't skip (core). THJ has not previewed or played it yet. `2383b461c` speed lines behind and full screen, Mark–Lucy slides from the sides. `6fbb67456` speed lines removed. `9dc33ad79` playback speed, Mark clip C. `6eaaa105b` clip C (LFS). `7251ce52f` Lucy clip in her half. `663c62b2a` Lucy starts earlier. `29d2c03ca` THJ's clip retime. **Merged 2026-11-22: `main` fast-forwarded to `29d2c03ca` at THJ's request; THJ is on `main` (11 ahead of `origin/main`, not pushed). The branch is kept (never deleted by agents).**
- Test clips in `Content/FamilySuperTime/DUO/Inserts/_Test/` stay untracked (clip B has burned-in logos).
- Combat resource and AP: same as `main`. Uncommitted in the tree (came along, THJ's, agents leave them alone): `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, the TMP fallback font.

## `thj/cyclone`

**Merged into `main` on 2026-11-22 (`049897aae`, merge commit, D-600); kept for history.** Items scoped to it now count as `all`. Last branch commits: the controls' should-fixes `29ab5c8d6`, the Command crash fix `e993069bf`, Command reach across gaps `96ecee6d0`, free Steer off + Steer cooldown 1 `13e8bab62` (D-597, D-601), tether arrowhead `155021c02`. THJ's test settings `b88c004f1` (intro/outro off) went to `main` as they are (D-600).

- Created 2026-11-12 by the coordinator at THJ's request ("create a new branch for it") from `main` @ `aaae8a7db` (0 ahead, 0 behind at creation; `main` matches `origin/main`). THJ's working branch (D-529).
- **Purpose:** Lucy's Cyclone redesign, Pulling Gale v2 (`plans/2026-11-11-cyclone-redesign-tech.md`; design `design/cyclone-redesign.md`; D-529 to D-533).
- 2026-11-16: the 20 Cyclone commits landed (`281d33866`..`e1203b02d`, D-546); plus THJ's test settings `b88c004f1` (intro/outro sequences off; revisit before merging to `main`); 21 ahead of `main`, no upstream, not pushed.
- **2026-11-19: `main` merged in** (`db9cf6ae9`, 9 commits: Masher plow, Catch & Return offer and preview, a dialogue fix; merge commit `ff16e25b4`, not pushed, 10 ahead of `origin/thj/cyclone` which sits at `031c3a5a1`). Git merged `MasherGoblinFactionRoleHandler.Counter.cs` with no conflict (the two sides touched different lines). Read-through: the plow's free-step test and the Cyclone fix both go through `IsFootprintEmpty`, so a heavy Masher's free step onto a Cyclone stays a walk step and the plow only plans steps over units. Not compiled or played yet.
- Combat resource and AP: same as `main`.
- Uncommitted in the tree (came along, THJ's, agents leave them alone): `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, the TMP fallback font. The AI diagnostic was discarded 2026-11-12 before C2 (D-534); backup `reports/ai-diagnostic-backup-2026-11-12.patch`.

## `thj/after-hearth`

**Merged into `main` on 2026-11-11 (`b1f9d1f68`, D-525); kept for history.** Items scoped to it now count as `all`. Before that: THJ's working branch from 2026-11-10 (D-465).

- Created 2026-11-10 by the coordinator at THJ's request ("create a new branch before starting new changes") from `main` @ `e9bd6e885` (0 ahead, 0 behind; `main` has the onboarding, Bond Lite, the tally and the Lucy memory gag; `e9bd6e885` and `25eca99d4` not pushed).
- **Purpose:** the onboarding after-the-Hearth rework (`plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`) once THJ answers its questions.
- Combat resource and AP: same as `main`. Uncommitted in the tree (came along): THJ's AI diagnostic (`AIFactionBrain.cs`, `AIUnitBrain.cs`), `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, the TMP fallback font; agents leave them alone.

## `main`

- **2026-11-22: the onboarding demo is built here** (D-602, `plans/2026-11-22-onboarding-demo.md`); risky new tech gets its own branch, asked first.
- Combat resource: **FTP** since `92853a5a9` (2026-10-16; `GlobalSettings.asset` `pointConsumptionMode: 0`); ATB before that. Duos pay 2 FTP. Family Roles still pay 1 FTP each with no per-round limit; the design (D-036 to D-042) makes them free and limited per round, and that code is built on `main` later, not on `thj/home-test`. Rules as built: GDD [Combat rules](design/gdd/combat-rules.md#family-time-points-ftp) and [Family systems](design/gdd/family-systems.md).
- AP: PerUnit (`aPConsumptionMode: 1`), escalation `[1,1,2,4]`. Fixed AP is the decision (D-037).
- Has the Morta rebuild export (`miso/Assets/MortaStory/`) and the skill-tree redesign, combat log, enemy tiers, Lucy + John shield relay (merged into `thj/home-test` in Steps J, K, L).
- No Home system.
- 2026-10-19: `thj/fr-readability` merged in (fast-forward), plus THJ's `bcf2b263a` and `5550286dd` (Linda's role-zone icon is now `BowArrow`). `main` @ `5550286dd` now has all of it: the Batch 1 fixes (D-052, D-054, D-057, D-060), the Family Role fixes F1/F3/F5, `MarkQTE`, role zones with per-unit icons in quadrants (D-063, D-064, D-075), cover icons (D-067), the Shift preview layer (D-071, D-072), John's tether, role barks and the two additive `GlobalEventBus` events (D-068 to D-070), and the B5 fix (D-074). Commit hashes: the plans' commit logs.
- 2026-10-21: `masher-tweak` merged in (fast-forward): the Masher reckless counter (C1–C5, D-092 to D-118), the hit-flash and ghost-facing fixes (D-121, D-122), John's area relay (D-119, D-120, D-123 to D-129), the private-ID comment cleanup `08bb27ac5`, and THJ's balance tweak `df58c4c0c`. `thj/home-test` will need this when it takes `main`.
- 2026-10-22: `thj/quick-wins` merged in (fast-forward, `main` @ `fc731b0c5`): quick wins bundle A (one-click cancel, John's shield animation variants, stepped damage preview + lethal skull with the `displayLethalMarkPreview` option, the "fires" cursor, objectives panel open/click to fold, enemy idle spread and hit/spawn returns through the handler, Mark's hit sound, Workshop shared items hidden, M1 level 2 grid stays hidden; D-130 to D-140). `main` is ahead of `origin/main` (not pushed). `thj/home-test` will need this when it takes `main`.
- 2026-10-23: `thj/quick-wins` fast-forwarded in again (in place, `main` @ `f4e9d9158`, 21 commits): bundle P pace (non-blocking banner, player input locked during the banner, turn-start pause, end-of-level fields, values, banner side; D-141 to D-144), the feedback pass (shake priority, kill flash and shake, mini HP bars, low-HP state and heartbeat, HUD low-HP signs; D-145 to D-149), the Dark Shaman heal with the `Kin.Dark` tag, heal "+N" numbers and the next-targets filter (D-150, D-151), the Lucy role targeting fix with the ordered attacker memory in `GUnit` (D-152), and THJ's balance tweaks `6ef6313bf`. Every value: `tech/pace-timings.md`. `main` matches `origin/main` minus these 21 (not pushed). `thj/home-test` will need this when it takes `main`.
- **2026-11-09: `thj/onboarding` merged in by THJ (fast-forward; `main` = `thj/onboarding` = `d5e8c8b86`, matches `origin/main`).** `main` now has everything listed under `thj/onboarding` and `thj/bond-lite` below: the onboarding opening (Hearth memories, River ∥ Ridge, The Trail, Home visits, M4 send-off), Bond Lite, the sisters' tally (with its Cyclone-move fix), enemy-alert levels, grid-to-level tool and the other onboarding-era core fixes. The classic opening is reachable only through tag `classic-intro-base` and `tech/classic-fallback.md`. Items scoped `thj/onboarding` or `thj/bond-lite` now count as `all` (D-456). `thj/home-test` lacks all of this; merge notes in `tech/onboarding-merge.md`. THJ is checked out on `main`. Uncommitted in the tree (THJ's, leave alone): the AI diagnostic (`AIFactionBrain.cs`, `AIUnitBrain.cs`).
- **2026-11-11: `thj/after-hearth` merged in (D-525).** Local `main` first fast-forwarded to `origin/main` @ `00a389b90` (8 teammate commits: TransitionPlus + Home Idle + temp Home, scene transitions, sequence icons, Narrator → TopNotification, mission/level graph windows, MS1/MS2 and Memory dialogue fixes), then `thj/after-hearth` merged (`b1f9d1f68`, not pushed; `main` 15 ahead of `origin/main`). Conflicts: `CombatLevelContainerScene.unity` roots (kept both), Memory 4 mother dialogue (main's rewrite kept; Hearth wiring + test follow-up owed). THJ checked out on `main`. Uncommitted in the tree (THJ's, leave alone): AI diagnostic, `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, the TMP fallback font.
- **2026-11-18: Masher plow** (`89bd4763e`, `62ed9b895`, D-573): the counter step shoves units in its way. `thj/cyclone` changes the same counter walk (Cyclone pass-through); `main` was merged into it on 2026-11-19 with no text conflict in `MasherGoblinFactionRoleHandler.Counter.cs` (see `thj/cyclone` below); play check of Masher + Cyclone + plow still owed.
- **2026-11-22: `thj/cyclone` merged in** (`049897aae`, D-600; `main` had teammate commit `377ab26fd` selected-unit indicator; clean, `AbilitiesBarHUDUI.cs` auto-merged). Brings Lucy's Cyclone redesign (reset, controls, Mark's Command steering it), its core hooks (`tech/core-systems.md`), the AI regression test as Explicit (`ecba8ecef`), and intro/outro sequences off in `GlobalSettings.asset`. 60 ahead of `origin/main`, not pushed. THJ is on `main`. Uncommitted in the tree (THJ's, leave alone): `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`, the TMP fallback font.
- The GDD reads its values from here (`main` @ `92853a5a9`), and its Home values from `thj/home-test` (D-046).

## `thj/onboarding`

**Merged into `main` by THJ on 2026-11-09 (fast-forward, `d5e8c8b86`; D-456); kept for history.** Items scoped to it now count as `all`. Before that: active, approved 2026-11-08 (D-443), THJ's working main while he worked solo (D-396).

- Created by THJ around 2026-10-30 from `main` @ `e8cb8a3d7`. Checked 2026-10-30: now at `194bd566b`, same as `main` (0 ahead, 0 behind), so it has the Encore text and its test fix.
- **Purpose (2026-10-30, THJ asked to start the onboarding implementation here):** the onboarding greybox, `plans/onboarding/` (structure C1 first). Uncommitted in the tree: THJ's AI restore-race diagnostic (`AIFactionBrain.cs`, `AIUnitBrain.cs`), `ProjectSettings/` and the TMP fallback font; agents leave them alone.
- Commits so far: C1 `38bc7db73`, `bb9982c87`, `f36da02f8` (opening mission graph). Merging with `thj/home-test` conflicts on `Game Data.asset` and the Home scene: recipe and every shared-file edit in `tech/onboarding-merge.md` (D-339).
- Combat resource and AP: same as `main`.
- **2026-11-05 (D-396): the working main while THJ works solo.** No cherry-picks; `main` (still @ `194bd566b`, 0 commits the branch lacks) is fast-forwarded later. Tag `classic-intro-base` marks the classic opening. Fallback recipe: `tech/classic-fallback.md` (every onboarding change that adds a wiring point updates it).
- Checked 2026-11-06: at `03cb1a97f`, 85 ahead of `main` and 0 behind, so `main` can still fast-forward.
- 2026-11-08: `thj/bond-lite` merged in (fast-forward, D-442), so the branch now carries Bond Lite. Checked 2026-11-08: at `6af47eeb6`, 109 ahead of `main` (still @ `194bd566b`) and 0 behind, so `main` can still fast-forward. Uncommitted in the tree: THJ's AI diagnostic (`AIFactionBrain.cs`, `AIUnitBrain.cs`), `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset` and `ProjectSettings.asset`; agents leave them alone.

## `thj/bond-lite`

- Created 2026-11-06 by THJ's choice (D-423) from `thj/onboarding` @ `58aa10418`, 0 ahead and 0 behind at creation. His uncommitted AI diagnostic, TMP font, `PreloadScreen` and `ProjectSettings` came along.
- **Purpose:** Bond Lite (`plans/onboarding/2026-10-26-bond-lite-tech.md`). `thj/onboarding` stays the build without Bond, and merges as a fast-forward if nothing is committed there meanwhile. Until then, tweaks go here.
- **Bond Lite done 2026-11-08** (C1–C5, then the fixes from THJ's first full play: highlight null ref, Hearth close + World map page, station pages on unlock, Marks-Sisters text, staged Yard with pan back; THJ's F10 win cheat). **Merged into `thj/onboarding` 2026-11-08 by THJ** (fast-forward; both at `6af47eeb6`; THJ is on `thj/onboarding`). Items scoped `thj/bond-lite` now count for `thj/onboarding`. `main` is 109 behind `thj/onboarding`, 0 ahead, so it can still fast-forward. Classic fallback recipe updated (`tech/classic-fallback.md`).
- Combat resource and AP: same as `main`.

## `thj/linda-quiver`

**Merged into `main` on 2026-10-29** (fast-forward in place with `git fetch . thj/linda-quiver:main`, `a1483f0b9..8c2e8617c`, 47 commits: the quiver, its core fixes, the swap fix). Afterwards THJ committed `341ac3d0d` (enemy alert on 4 levels), `c3ca01367` and `a94240034` (EditorFPSLimiter in PreloadScreen) on the branch, and is switching to `main` to merge those himself. Not pushed. The quiver is on in `main` by the code default (`lindaQuiverEnabled`); `GlobalSettings.asset` doesn't store it. Items scoped to this branch now count as `all`.

- **Purpose:** the Linda's Quiver prototype (`linda-quiver`; design `plans/2026-10-26-linda-quiver-design.md`, D-241 to D-245; tech plan `plans/2026-10-26-linda-quiver-tech.md`).
- Created by THJ on 2026-10-26 from `main` @ `a1483f0b9` (0 ahead, 0 behind at creation). THJ's working branch.
- Combat resource and AP: same as `main` (FTP, PerUnit). No differences from `main` yet.

## `thj/quick-wins`

**Merged into `main` twice:** on 2026-10-22 (fast-forward to `fc731b0c5`, bundle A), and on 2026-10-23 (fast-forward in place with `git fetch . thj/quick-wins:main`, to `f4e9d9158`, 21 commits: bundle P, the feedback pass C1–C5, the Dark Shaman heal, the Lucy role fix and THJ's balance tweaks `6ef6313bf`). `main` and `thj/quick-wins` point at the same commit; THJ is still checked out on `thj/quick-wins`. Quick wins are done; no new work planned here.

- **Purpose:** playtest Batch 3 quick wins (`plans/2026-10-20-quick-wins-triage.md`; bundle A tech plan `plans/2026-10-21-quick-wins-a-tech.md`; D-107 to D-111, D-130 to D-133).
- Created by THJ on 2026-10-21 from `main` (0 ahead, 0 behind at creation; `main` includes THJ's John shield clips `3ae174a93`). THJ's working branch.
- Combat resource and AP: same as `main` (FTP, PerUnit).

## `masher-tweak`

**Merged into `main` by THJ on 2026-10-21 (fast-forward, `main` @ `df58c4c0c`); kept for history, no new work.** Items scoped to it now count as `all`.

- **Purpose:** the Masher reckless-tank rework (`masher-reckless-tank`; design `plans/2026-10-20-masher-reckless-tank-design.md`, tech `plans/2026-10-20-masher-reckless-tank-tech.md`; D-092 to D-105).
- Created by THJ on 2026-10-20 from `main` @ `4f2668918` (0 ahead, 0 behind). THJ's working branch.
- Combat resource and AP: same as `main` (FTP, PerUnit).
- Differences from `main`: Masher C1–C3 committed (`08ca1d819`, `11f64c19f`, `212638ad2`, `e409b2c94`, `519e05d9e`): `AIController` wait + recheck, `CombatLevelRunHandler` turn-switch hold, Masher rules, counter preset and prefab. C4 committed (`7556630a6`, `d5402d48d`, `9e6d50f51`: Mark/Linda suppression check, `FactionRoleHandlerBase` null guard, handler rewrite). C5 committed (`1a0936a28`, `256bcade6`: PlayerController lookups public, Masher preview). Play-check fixes `f5778df92` (hit flash, carry to `main`) and `4e51d365f` (ghost facing). John relay in progress. `thj/home-test` will need C1–C4 when it takes this work.

## `thj/home-test`

- **Purpose:** the Home system demo (M0–M9 and playtest fixes). See `tech/home-system.md`.
- Combat resource: **FTP** (`pointConsumptionMode: 0`), because the Home demo writes its effects against FTP.
- New Home rules apply (see `design/demo-spec.md`).
- AP: PerUnit, same as `main`.
- Merges `origin/main` periodically through Claude Code; THJ commits. Merges so far: Step J `59a4f5cde` (Oct 3), Step K `182201e82` (Oct 4), Step L `5c8476822` (Oct 11), and `ee126a407` (Oct 26: `main` @ `a1483f0b9`: everything listed under `main` above through the enemy alert state, plus THJ's Unity MCP package; D-181, D-198). Since that merge, all `main` work through `a1483f0b9` is also on home-test, and the earlier "home-test will need this" notes are done. Then `93d414dd5` (2026-10-30: `main` @ `e5506c1e8`, the Linda's Quiver merge and its core fixes, the swap fix, THJ's enemy-alert and FPS-limiter commits; clean merge, 6 files changed on both sides auto-merged; D-331). The quiver is on by the code default here too.
- Committed, not pushed. Last commit `93d414dd5` (Oct 30, merge of main). Then `cfa297659` (Encore test fix). EditMode 1441/1442 (known red only).
- Home scene fallback after a merge: take `main`'s scene and re-run the builders (order in `CLAUDE.md`).
- FTP wins on merge (D-036 to D-042). **[THJ]** Still open: how and when is this expected to merge into `main`?

## `thj/preview-improvements`

**Merged into `main` by THJ on 2026-10-20; kept for history, no new work.** Items scoped to it now count as `all`.

- **Purpose:** the grid preview pass (`preview-pass`; design `plans/2026-10-19-preview-pass-design.md`, tech plan `plans/2026-10-19-preview-pass-tech.md`).
- Branched from `main` @ `5550286dd` on 2026-10-19 (0 ahead, 0 behind at creation). THJ's working branch.
- Combat resource and AP: same as `main` (FTP, PerUnit).

## `thj/fr-readability`

**Merged into `main` on 2026-10-19 (fast-forward); kept for history, no new work.** Items scoped to it now count as `main`/`all`.

- **Purpose:** Family Role readability (B4, Q7 part) and the Oct 2026 playtest fixes made from `thj/oct-build-fixes`. Plans: `plans/2026-10-18-family-role-phase0-1.md`, `plans/2026-10-18-playtest-batch1-bugfixes.md`.
- Branched from the work on `thj/oct-build-fixes` (= `main` @ `97538642c` plus the Batch 1 fixes and the B4 commits); 0 commits behind `main`. THJ switched to it on 2026-10-18.
- Combat resource and AP: same as `main` (FTP, PerUnit).
- Differences from `main`: Mark's Cleanse placeholder state and the ability animation safety net (D-052), HP bar text fix (D-054), map panel anchor, tutorial input lock (`PlayerInputController` lock), safe-room objective text and the Wares rename (D-057, D-060), Family Role bug fixes F1/F3/F5 (D-062/D-065), Mark's `MarkQTE` binding, role-zone layer and Shift view (D-063/D-064). Commit hashes: the plans' commit logs.
