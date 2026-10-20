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
- The GDD reads its values from here (`main` @ `92853a5a9`), and its Home values from `thj/home-test` (D-046).

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

- **Purpose:** the grid preview pass (`preview-pass`; design `plans/2026-10-19-preview-pass-design.md`, tech plan `plans/2026-10-19-preview-pass-tech.md`).
- Branched from `main` @ `5550286dd` on 2026-10-19 (0 ahead, 0 behind at creation). THJ's working branch.
- Combat resource and AP: same as `main` (FTP, PerUnit).

## `thj/fr-readability`

**Merged into `main` on 2026-10-19 (fast-forward); kept for history, no new work.** Items scoped to it now count as `main`/`all`.

- **Purpose:** Family Role readability (B4, Q7 part) and the Oct 2026 playtest fixes made from `thj/oct-build-fixes`. Plans: `plans/2026-10-18-family-role-phase0-1.md`, `plans/2026-10-18-playtest-batch1-bugfixes.md`.
- Branched from the work on `thj/oct-build-fixes` (= `main` @ `97538642c` plus the Batch 1 fixes and the B4 commits); 0 commits behind `main`. THJ switched to it on 2026-10-18.
- Combat resource and AP: same as `main` (FTP, PerUnit).
- Differences from `main`: Mark's Cleanse placeholder state and the ability animation safety net (D-052), HP bar text fix (D-054), map panel anchor, tutorial input lock (`PlayerInputController` lock), safe-room objective text and the Wares rename (D-057, D-060), Family Role bug fixes F1/F3/F5 (D-062/D-065), Mark's `MarkQTE` binding, role-zone layer and Shift view (D-063/D-064). Commit hashes: the plans' commit logs.
