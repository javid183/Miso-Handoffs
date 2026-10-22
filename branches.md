# Branches

Owner: coordinator; THJ approves. `claude-handoff/` doesn't change when the shared repo switches branches, so this file says what's different on each active branch.

**Rules**

- Every task, backlog item and decision is scoped `all` or to one branch.
- Active work = everything scoped `all` + everything scoped to the current branch. Work scoped to another branch is parked.
- A design rule that differs is written once in its design doc, with its variant: "**On `thj/home-test`:** ...".
- Agents never switch branches. THJ does.
- On merge, a branch's differences fold into `all`. If that changes a core rule on `main`, it's Tier 3.

## `main`

- Combat resource: **FTP** since `92853a5a9` (2026-10-16; `GlobalSettings.asset` `pointConsumptionMode: 0`); ATB before that. Duos pay 2 FTP. Family Roles still pay 1 FTP each with no per-round limit; the design (D-036 to D-042) makes them free and limited per round, and that code is built on `main` later, not on `thj/home-test`. Rules as built: GDD [Combat rules](design/gdd/combat-rules.md#family-time-points-ftp) and [Family systems](design/gdd/family-systems.md).
- AP: PerUnit (`aPConsumptionMode: 1`), escalation `[1,1,2,4]`. Fixed AP is the decision (D-037).
- Has the Morta rebuild export (`miso/Assets/MortaStory/`) and the skill-tree redesign, combat log, enemy tiers, Lucy + John shield relay (merged into `thj/home-test` in Steps J, K, L).
- No Home system.
- 2026-10-19: `thj/fr-readability` merged in (fast-forward), plus THJ's `bcf2b263a` and `5550286dd` (Linda's role-zone icon is now `BowArrow`). `main` @ `5550286dd` now has all of it: the Batch 1 fixes (D-052, D-054, D-057, D-060), the Family Role fixes F1/F3/F5, `MarkQTE`, role zones with per-unit icons in quadrants (D-063, D-064, D-075), cover icons (D-067), the Shift preview layer (D-071, D-072), John's tether, role barks and the two additive `GlobalEventBus` events (D-068 to D-070), and the B5 fix (D-074). Commit hashes: the plans' commit logs.
- 2026-10-21: `masher-tweak` merged in (fast-forward): the Masher reckless counter (C1–C5, D-092 to D-118), the hit-flash and ghost-facing fixes (D-121, D-122), John's area relay (D-119, D-120, D-123 to D-129), the private-ID comment cleanup `08bb27ac5`, and THJ's balance tweak `df58c4c0c`. `thj/home-test` will need this when it takes `main`.
- 2026-10-22: `thj/quick-wins` merged in (fast-forward, `main` @ `fc731b0c5`): quick wins bundle A (one-click cancel, John's shield animation variants, stepped damage preview + lethal skull with the `displayLethalMarkPreview` option, the "fires" cursor, objectives panel open/click to fold, enemy idle spread and hit/spawn returns through the handler, Mark's hit sound, Workshop shared items hidden, M1 level 2 grid stays hidden; D-130 to D-140). `main` is ahead of `origin/main` (not pushed). `thj/home-test` will need this when it takes `main`.
- The GDD reads its values from here (`main` @ `92853a5a9`), and its Home values from `thj/home-test` (D-046).

## `thj/quick-wins`

**Merged into `main` on 2026-10-22 (fast-forward to `fc731b0c5`); kept for history, no new work.** Items scoped to it now count as `all`.

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
- Merges `origin/main` periodically through Claude Code; THJ commits. Merges so far: Step J `59a4f5cde` (Oct 3), Step K `182201e82` (Oct 4), Step L `5c8476822` (Oct 11).
- Committed, not pushed. Last commit `2f828e662` (Oct 15, playtest fixes 2).
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
