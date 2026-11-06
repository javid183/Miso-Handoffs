# claude-handoff

THJ's private working folder for Claude on Miso. It is **excluded from the shared repo** (`.git/info/exclude`) and is **its own private git repo**, so it doesn't change when the shared repo switches branches. Commits here are made by the main session without asking, split by unit and reported; see `CLAUDE.md`.

## Rules

1. **One home per fact.** Other docs link to it; they never copy it.
2. **Agents work from this folder.** Anything an agent needs mid-task lives here as markdown, readable without a connector.
3. **The canonical doc wins.** When two docs disagree, the coordinator fixes the other one and logs it.
4. **One writer per doc.** Other agents propose changes in their report; the owner writes them.
5. **Grow docs on demand.** One file per topic. Split only when a file passes about 300 lines or tasks keep needing just one part of it (splitting is Tier 3).

## Map

| Document | Home | Owner (writes) | Updated when |
| --- | --- | --- | --- |
| Project rules | `CLAUDE.md` (repo root, excluded from the shared repo; kept short, it loads into every session and agent) | Coordinator; THJ approves changes | A working rule changes |
| Vision, pillars, USPs | `vision.md` | THJ | Rarely, by THJ only |
| Escalation rubric | `escalation.md` | THJ | Sunday review |
| Backlog and status | `status.md` | Coordinator | A task starts, finishes or is blocked |
| Active branches | `branches.md` | Coordinator; THJ approves | A branch is created, merged, or its differences change |
| Decision log | `decisions.md` | Coordinator | Every decision, any tier |
| Build log | `build-log.md` | Coordinator | A milestone or step closes |
| Glossary and lore canon | `glossary.md` | Narrative agent | A name, term or lore fact is approved |
| Naming and code conventions | `conventions.md` | Coordinator; THJ approves | A new prefix, folder or pattern is introduced |
| Game Design Document (GDD): the design source of truth | `design/gdd/` (`overview.md` is the index) | Game designer; coordinator syncs the mirror | A decision changes a rule or value, or the assets change (D-044) |
| Design docs | `design/` | Game designer | A design plan is approved |
| Demo Spec | `design/demo-spec.md` | Coordinator | A build changes a rule |
| Combat code map, dev cheats | `tech/combat-architecture.md` | Coordinator | The architecture changes |
| Home code map, builders, test tools | `tech/home-system.md` | Coordinator | The Home system changes |
| Editor checks (compile, logs, tests, play checks) | `tech/editor-checks.md` | Coordinator; the verifier reports corrections | A check turns out wrong, or the setup changes |
| Combat pace timings (every wait, where to change it, what it affects) | `tech/pace-timings.md` | Coordinator | A timing is added, moved or retuned |
| Core systems list | `tech/core-systems.md` | Coordinator; THJ approves additions and removals | A class becomes something combat relies on, or stops being one |
| Level tools (grid ↔ prefab: renderer, reader, Build Level From Grid) | `tech/level-tools.md` | Coordinator | A level tool changes |
| Onboarding ↔ home-test merge notes (shared-file edits, recipe) | `tech/onboarding-merge.md` | Coordinator | An onboarding chunk edits a file `thj/home-test` also changes |
| Classic-opening fallback recipe (undo the onboarding wiring) | `tech/classic-fallback.md` | Coordinator | An onboarding change adds or moves a wiring point (D-396) |
| Linda's quiver code map | `tech/linda-quiver.md` | Coordinator | The quiver's code or contract changes |
| Technical notes | `tech/` | Coordinator | A system is added or its contract changes |
| Playtest task lists (structured feedback, effort and owners) | `playtests/2026-10-playtest-tasks.md` | THJ writes; coordinator tracks items in `status.md` | After each playtest round |
| GDD open-question answer sheet (temporary) | `design/gdd-open-questions.md` | THJ answers; game designer folds answers into the GDD | Until all are answered |
| Plan and report templates | `templates/` | Coordinator | The format changes |
| Task plans | `plans/YYYY-MM-DD-<slug>.md`; a large topic with several plans gets a folder, `plans/<topic>/YYYY-MM-DD-<slug>.md`, which also holds its images and design drafts (first: `plans/onboarding/`, 2026-10-26; older `decisions.md` rows keep the paths from before the move) | The agent that plans | Once per task, revised on review |
| Task reports | `reports/<slug>.md`, `reports/<slug>-verify.md` | The agent that did the work | Once per task |
| Playtest notes | `playtests/` | THJ writes raw; coordinator structures | After each playtest |
| Agent and skill definitions | `claude-config/` (master; `.claude/agents` and `.claude/skills` are copies, see below) | THJ; coordinator proposes | The workflow changes |
| Reward balance tools | `reward-tools/` | Coordinator | The tools change |
| Archive | `archive/` | Nobody: read-only history | Never |

## Mirrors (one way, from here)

- **Claude Docs, the GDD:** "Miso — Game Design" (https://claude.ai/artifact/3KSS3o9ZPhGK2yqTAntKgh) mirrors `design/gdd/` (one tab per file; the characters as sub-tabs of Characters) and `glossary.md` (last tab). One way, after each approved change; doc comments come back as input (D-045). Each tab names the file it mirrors. Repo links become tab links in the doc; links to files outside the GDD show as paths.
- **Claude Docs:** the "Miso Home System" doc (https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN) mirrors `design/demo-spec.md`, `design/m9-readability.md` and `build-log.md`; other design docs can join it as tabs. Sync runs one way, from this folder to the doc, after each approved change; comments made on the doc come back as input, never as direct edits. The sync runs from a Claude chat with the Claude Docs connector on an account that can open the doc's content (the company account, as of 2026-10-15).
- **Claude project "Miso":** a subset of these files is uploaded as project docs for chats. Refresh them from here when they change.

## Agent and skill definitions

Claude Code reads agents and skills from `.claude/agents` and `.claude/skills` in the repo root. The masters live in `claude-config/` so they get history here. The `E:` drive is exFAT, which has no junctions or symlinks, so `.claude/` holds plain copies (D-030).

- Edit only the files in `claude-config/`, never the copies in `.claude/`: the next sync overwrites them.
- After an approved change, sync. `/MIR` makes each `.claude` folder match its master, deletions included:

  ```
  powershell.exe -NoProfile -Command "robocopy 'E:\Work\Projects\miso\claude-handoff\claude-config\agents' 'E:\Work\Projects\miso\.claude\agents' /MIR /NJH /NJS /NDL; robocopy 'E:\Work\Projects\miso\claude-handoff\claude-config\skills' 'E:\Work\Projects\miso\.claude\skills' /MIR /NJH /NJS /NDL"
  ```

- Claude Code's auto mode refuses writes into `.claude/`, so THJ runs the sync (or a session in manual permission mode does).

## Layout

```
claude-handoff/
├── README.md  vision.md  escalation.md  status.md  branches.md
├── decisions.md  build-log.md  glossary.md  conventions.md
├── templates/        plan.md, report.md
├── design/           gdd/ (the GDD), demo-spec.md and the design notes
├── tech/             core-systems.md, combat-architecture.md, home-system.md, mechanics-brief.md, ...
├── plans/  reports/  playtests/
├── claude-config/    agents/, skills/ (masters; copied to .claude/)
├── reward-tools/
└── archive/
```
