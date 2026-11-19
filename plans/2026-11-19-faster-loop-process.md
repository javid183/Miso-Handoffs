# Plan: a faster loop (process changes, draft for THJ)

Branch: all    Type: process    Size: M    Tier: 3 (changes `CLAUDE.md`, the rubric and agent roles)
Status: **ALL FIVE APPROVED by THJ 2026-11-19 and applied to the docs and masters** (D-575 change 1, D-576 change 2, D-577 change 3, D-578 change 4 without its optional Tier 1 item, D-579 change 5). THJ ran the `.claude/` sync; 5a verified and committed as `ecba8ecef` on `thj/cyclone` (report `reports/ai-regression-explicit.md`).

## Why

THJ, 2026-11-19: development has slowed a lot; are all the regression tests needed, and what would make it faster?

What the numbers say (measured 2026-11-19):

- The EditMode suite is 2,174 tests in 4 min 53 s. Four fixtures take half of it: `HomeVisitsTests` 59 s, `GuidedSkillSpendTests` 39 s, `AIRegressionTest` 35 s, `HearthMemoryResultLineTests` 13 s. The tests are not the bottleneck.
- Game commits per week: 109, 87, 88 (W43 to W45), then 37 in W46 and 37 so far in W47. Handoff commits in W46: 159.
- Decisions since 2026-11-05: 153 Tier 3, 35 Tier 2, 2 Tier 1. Four out of five decisions wait on THJ.
- Reviews: roughly a third of the 144 saved review files carry a FIX verdict (rough text search, not read one by one). Reviews do find real problems, so change 1 trims how often they run instead of removing them.

## Change 1: review once per feature, per chunk only for core

**APPROVED by THJ 2026-11-19 (D-575), applied to the masters.** `.claude/` sync still owed.

**Rule.**

- A chunk that touches a core system (`tech/core-systems.md`), changes save data, or where the implementer reports a behavior deviation: reviewed on its own, before the next chunk builds on it (as today).
- Every other chunk: no review of its own. The feature gets one review of the whole diff after its last chunk.
- A size S bugfix or tweak outside core systems: no reviewer. The coordinator reads the diff and the report.

**Edits.**

`claude-config/agents/miso-coordinator.md`, Gates, item 3:

- Now: `3. \`miso-reviewer\` approved (code tasks).`
- New: `3. \`miso-reviewer\` approved: each chunk that touches a core system, changes save data or deviates in behavior is reviewed on its own; other chunks are reviewed together, once, after the feature's last chunk. Size S work outside core systems needs no reviewer: you read the diff and the report.`

Same file, Routing, "Feature with an approved design" row:

- Now: `Your tech plan, then \`miso-implementer\` → \`miso-reviewer\` → \`miso-verifier\``
- New: `Your tech plan, then \`miso-implementer\` per chunk (core chunks → \`miso-reviewer\` right away), then one \`miso-reviewer\` pass on the whole feature → \`miso-verifier\``

`claude-config/skills/miso-tech-plan/SKILL.md`, section 2, the "For each chunk" bullet: add `, review (own review if core, save data or risky; otherwise "with the feature")`.

**Cost.** A problem in a non-core chunk is found at the end of the feature, not right after the chunk, so its fix can touch later chunks. Example of what a per-chunk review caught: the plow candidates skipping the walk's path-cost budget (Masher plow C2).

## Change 2: one report per feature

**Rule.**

- One report file per plan: `reports/<plan slug>.md`. The implementer adds a short section per chunk (files changed, criteria met, decisions) and fills the full template once, on the last chunk.
- The coordinator appends each review verdict to that same file under "Reviews", not a separate `-review.md` file.
- The verifier writes its own `-verify.md` only for a play session or a FAIL or PARTIAL result. A clean quiet check is three lines in the feature report.
- The coordinator commits the handoff repo once per chunk and once at the report, not once per step.

**Edits.**

`claude-config/agents/miso-implementer.md`, "Before you finish", item 2:

- Now: `Write the report to \`claude-handoff/reports/<same slug as the plan>.md\` from \`templates/report.md\`. List every changed file. ...`
- New: `Report in \`claude-handoff/reports/<same slug as the plan>.md\`, one file for the whole plan. If the file exists, append a "Chunk <n>" section: changed files, criteria met with evidence, decisions, loose ends. On the plan's last chunk, also fill the rest of \`templates/report.md\` for the feature as a whole. ...` (the rest of the item is unchanged)

`claude-config/agents/miso-verifier.md`, Output: add before the list: `Write the file only for a play session or a FAIL or PARTIAL result. For a clean quiet check, return the summary alone; the coordinator records it in the feature report.`

`templates/report.md`: add two sections after "Acceptance criteria": `## Chunks` (one short block per chunk) and `## Reviews and checks` (verdicts and quiet-check results, written by the coordinator).

`claude-config/agents/miso-coordinator.md`, Delegating, last bullet: add `; one report file per plan, which you extend with review verdicts and clean quiet-check results`.

**Cost.** Less detail per chunk on disk. Past reports stay as they are.

## Change 3: covering tests per chunk, full suite before the commit

**Rule.**

- After a chunk: run the fixtures that cover the change (named in the plan's test plan).
- The full EditMode suite runs once per feature, after the last chunk and before any commit is proposed. Core-system chunks still run the full suite on their own.

**Edits.**

`CLAUDE.md`, "How to work with me", third bullet:

- Now: `Add edit-mode tests for logic and run the EditMode suite after code changes. ...`
- New: `Add edit-mode tests for logic. After a change, run the tests that cover it; run the whole EditMode suite before a commit and after any change to a core system. ...` (the rest of the bullet is unchanged, or as change 5 leaves it)

`claude-config/agents/miso-implementer.md`, "Before you finish", item 1:

- Now: `Make sure it compiles and the EditMode suite passes (...)`
- New: `Make sure it compiles and the tests the plan names for this chunk pass (...). Run the whole EditMode suite on the plan's last chunk and on any chunk that touches a core system.`

`claude-config/agents/miso-coordinator.md`, Gates, item 2: add at the start: `Full suite once per feature, before the commit proposal; covering tests per chunk.`

`claude-config/skills/miso-tech-plan/SKILL.md`, section 4, "Test plan" bullet: add `Name the test fixtures each chunk runs.`

**Cost.** A chunk can break an unrelated test and nobody sees it until the feature's last chunk. Saves about four minutes per chunk.

## Change 4: fewer Tier 3 questions

**Rule.** Presentation values on a design THJ already approved move to Tier 2 when they are serialized fields he can tune in the Inspector: durations, delays, alphas, tints, preview details, easing, sizes. First pass of a new beat and anything on a dramatic moment stay Tier 3.

**Edits to `escalation.md`.**

"By domain" table, Design row, Tier 2 cell: add `; presentation values on an approved design (durations, delays, alphas, tints, easing, preview details) when each is a serialized field THJ can tune in the Inspector`.

"THJ's areas", Game feel bullet:

- Now: `**Game feel:** timing, feedback, hit reactions, camera and animation pacing.`
- New: `**Game feel:** what a beat is (what plays, in what order, what the player reads from it), hit reactions, camera, and the first pass of any new beat. Tuning values of an approved beat are Tier 2 when they are serialized fields.`

Remove the expired line: `**Until 2026-10-29** (the first two weeks), anything in these areas is Tier 3 even when small.`

Changelog row: `| 2026-11-19 | Presentation values on an approved design move to Tier 2 when serialized; Game feel narrowed to what a beat is and its first pass; the two-week "everything is Tier 3" line removed (expired 2026-10-29). |`

**Optional, same file.** Tier 1 decisions stop getting a row in `decisions.md` (they appear as one line in the feature report). Only two were logged in two weeks, so this saves little; listed for completeness.

**Cost.** THJ sees these values after they are built, in the Tier 2 list of the report, and changes them in the Inspector or asks for a redo.

## Change 5: the AI regression test runs on request

The test costs 35 s in every run and has been red since September, so it reports nothing new. Two steps:

**5a, now (size S, one implementer run, shared repo).** Mark `AIRegressionTest.Baseline_MatchesCurrentAI` `[Explicit]` in `Core/Systems/AISystem/Editor/AIRegressionTest.cs`, with a comment saying why in plain words. It then runs only when selected by name or from `Tools/AI/Run Regression Test`. This changes a test the rest of the team shares, so it needs THJ's OK and its own commit.

**5b, later.** The dedicated fix session already in the backlog (`tech/ai-regression-test-triage.md`): triage the NullReference, confirm each diff, re-baseline, then remove `[Explicit]`.

**Edits that go with 5a.**

- `CLAUDE.md`, same bullet as change 3: replace the "known red" sentence with `\`AIRegressionTest.Baseline_MatchesCurrentAI\` is marked Explicit until its dedicated fix session: it runs only on request. Run it when a change touches AI graphs, AI abilities or unit prefabs, and report its failure count against the last one recorded; do not "fix" or re-baseline it unless I ask for that fix.`
- `miso-coordinator.md` Gates item 2, `miso-implementer.md` "Before you finish" item 1, `miso-verifier.md` Tests: replace the "known red" exception with the same rule (every test in the suite must pass; the AI regression test is run by name only when AI content changed, and its count is compared with the last recorded one, 43 inner failures on 2026-11-18).

**Cost.** A change that newly breaks the AI baseline is seen only when someone runs the test by name. The tech-plan checklist already flags plans that touch AI content.

## How it gets applied

1. THJ approves each change (or edits it).
2. The coordinator edits the masters in `claude-handoff/claude-config/`, `templates/report.md`, `escalation.md` and `CLAUDE.md`, logs one decision row per approved change, and commits the handoff repo.
3. THJ runs the sync command from `README.md` so `.claude/` picks up the agent and skill changes.
4. 5a goes to `miso-implementer` as a size S task; its commit is proposed to THJ on its own.

## Acceptance criteria

- Every approved change is in the files named above, word for word as approved.
- `decisions.md` has a row per approved change; `escalation.md` has its changelog row.
- After the sync, `.claude/agents` and `.claude/skills` match the masters.
- 5a: the full EditMode suite is green with the AI regression test skipped; the test still runs from the menu.

## Check after two weeks

At the Sunday review on or after 2026-12-06: game commits per week, the Tier 2 and Tier 3 counts, any Tier 2 presentation value THJ reversed, and any bug that a per-chunk review or a full-suite run would have caught earlier.
