# claude-handoff

THJ's private working folder for Claude on Miso. It is **excluded from the shared repo** (`.git/info/exclude`) and is **its own private git repo**, so it doesn't change when the shared repo switches branches. Commits follow the Git rules in `CLAUDE.md`, here too: proposed by the main session, shown to THJ, split by unit, made only on his yes.

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
| Design docs | `design/` | Game designer | A design plan is approved |
| Demo Spec | `design/demo-spec.md` | Coordinator | A build changes a rule |
| Combat code map, dev cheats | `tech/combat-architecture.md` | Coordinator | The architecture changes |
| Home code map, builders, test tools | `tech/home-system.md` | Coordinator | The Home system changes |
| Core systems list | `tech/core-systems.md` | Coordinator; THJ approves additions and removals | A class becomes something combat relies on, or stops being one |
| Technical notes | `tech/` | Coordinator | A system is added or its contract changes |
| Plan and report templates | `templates/` | Coordinator | The format changes |
| Task plans | `plans/YYYY-MM-DD-<slug>.md` | The agent that plans | Once per task, revised on review |
| Task reports | `reports/<slug>.md`, `reports/<slug>-verify.md` | The agent that did the work | Once per task |
| Playtest notes | `playtests/` | THJ writes raw; coordinator structures | After each playtest |
| Agent and skill definitions | `claude-config/` (junctioned from `.claude/agents` and `.claude/skills`) | THJ; coordinator proposes | The workflow changes |
| Reward balance tools | `reward-tools/` | Coordinator | The tools change |
| Archive | `archive/` | Nobody: read-only history | Never |

## Mirrors (one way, from here)

- **Claude Docs:** the "Miso Home System" doc (https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN) mirrors `design/demo-spec.md`, `design/m9-readability.md` and `build-log.md`; other design docs can join it as tabs. Sync runs one way, from this folder to the doc, after each approved change; comments made on the doc come back as input, never as direct edits. The sync runs from a Claude chat with the Claude Docs connector on an account that can open the doc's content (the company account, as of 2026-10-15).
- **Claude project "Miso":** a subset of these files is uploaded as project docs for chats. Refresh them from here when they change.

## Layout

```
claude-handoff/
├── README.md  vision.md  escalation.md  status.md  branches.md
├── decisions.md  build-log.md  glossary.md  conventions.md
├── templates/        plan.md, report.md
├── design/           demo-spec.md and the design notes
├── tech/             core-systems.md, combat-architecture.md, home-system.md, mechanics-brief.md, ...
├── plans/  reports/  playtests/
├── claude-config/    agents/, skills/ (what .claude/ points at)
├── reward-tools/
└── archive/
```
