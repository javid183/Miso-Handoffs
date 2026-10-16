# Pass 3 setup brief

For a Claude Code session in `E:\Work\Projects\miso\`. Written 2026-10-15 in a claude.ai chat that couldn't see THJ's disk. **Check everything against what's actually there**, and stop to ask THJ when this brief and the disk disagree.

## What this sets up

A coordinator and six specialist agents for Miso, the docs they work from, and the move of the existing `claude-handoff/` notes into the new layout. The finished `CLAUDE.md` and `.claude/settings.json` are already in this folder, reviewed with THJ; you install them, you don't merge them.

## Ground rules

- Follow THJ's current `CLAUDE.md`, especially the Git rules: read-only git anytime; any write command only after telling him, showing the diff, and his yes.
- Don't touch game code, assets or scenes. This session changes only `claude-handoff/`, `.claude/` and `CLAUDE.md`.
- Move, don't delete. Anything retired goes to `claude-handoff/archive/`.
- Short status messages between steps.

## Step 1 — Preflight (read-only)

1. Compare the current `CLAUDE.md` and `.claude/settings.json` with `_pass3/originals/CLAUDE.md.2026-10-15` and `_pass3/originals/settings.json.2026-10-15`. **If either changed since, stop and show THJ the diff**: the new versions were written from those copies.
2. Read `claude-handoff/README.md`, `claude-handoff/home-system-handoff.md`, and everything in `_pass3/`.
3. List `claude-handoff/` and `.claude/`. Check `.git/info/exclude` lists `.claude/`, `CLAUDE.md` and `claude-handoff/`.
4. If `claude-handoff/` isn't a git repo yet, propose `git init` there and a baseline commit of its current contents, so every change below shows as a diff.
5. Compare `home-system-handoff.md` with `_pass3/docs/status.md` and `_pass3/docs/tech/home-system.md` (written from the Oct 14 version). Note anything newer on disk.
6. Note every file in `claude-handoff/` the move table doesn't cover.

Report the findings in one short message.

## Step 2 — Agent and skill definitions

Target: `claude-handoff/claude-config/{agents,skills}/`, with `.claude/agents` and `.claude/skills` as directory junctions pointing at them, so agent edits get history in the private repo.

1. Move `_pass3/claude-config/` to `claude-handoff/claude-config/`.
2. If `.claude/agents/` or `.claude/skills/` already hold files, move them into the matching `claude-config/` folder first (flag any name clash to THJ). Then remove the empty folders.
3. Create the junctions (PowerShell; no admin rights needed):

   ```powershell
   New-Item -ItemType Junction -Path "E:\Work\Projects\miso\.claude\agents" -Target "E:\Work\Projects\miso\claude-handoff\claude-config\agents"
   New-Item -ItemType Junction -Path "E:\Work\Projects\miso\.claude\skills" -Target "E:\Work\Projects\miso\claude-handoff\claude-config\skills"
   ```

4. Confirm both list the expected files.

## Step 3 — Move existing notes

Show THJ this table as you'll actually apply it (after step 1) and wait for his OK.

| From (`claude-handoff/`) | To | Note |
| --- | --- | --- |
| `Miso-Home-System_Demo-Spec.md` | `design/demo-spec.md` | |
| `Miso-Home-System_M9-Readability.md` | `design/m9-readability.md` | |
| `player-skill-trees.md` | `design/player-skill-trees.md` | |
| `combat-balance.md` | `design/combat-balance.md` | |
| `reward-balance.md` | `design/reward-balance.md` | Check its references to `reward-tools/` still resolve |
| `miso-mechanics-brief.md` | `tech/mechanics-brief.md` | |
| `ai-regression-test-triage.md` | `tech/ai-regression-test-triage.md` | |
| `combat-log.md` | `tech/combat-log.md` | Read it first; if it's design rather than code notes, use `design/` and tell THJ |
| `Playtest-Plan.md` | `playtests/playtest-plan.md` | |
| `account-export-2026-10-14/Miso-Home-System_Build-Log.md` | `build-log.md` | Then append the sections of `Build-Log_additions.md` it doesn't already contain, in date order |
| `Build-Log_additions.md` | `archive/build-log-additions-2026-10-14.md` | After its content is in `build-log.md` |
| `home-system-handoff.md` | `archive/home-system-handoff.md` | After step 5 |
| `account-export-2026-10-14/` (rest) | `archive/account-export-2026-10-14/` | |
| `README.md` (old) | `archive/README-2026-10-14.md` | Replaced by `_pass3/docs/README.md` |
| `reward-tools/` | stays where it is | Its scripts may use relative paths (`_paths.py`) |

Then copy everything in `_pass3/docs/` into `claude-handoff/`, including the empty `plans/`, `reports/`, `playtests/` and `design/` folders (each has a `.gitkeep`). Never overwrite an existing file except the old `README.md`, which you archived.

## Step 4 — Fix references

Grep every file in `claude-handoff/` for the old file names and paths from the table and for the `Build-Log_additions.md` inbox flow, and update them to the new paths. Keep the "Miso Home System" doc link (https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN): that doc is the mirror, not retired.

## Step 5 — Fold in the Home handoff

Merge anything newer from `home-system-handoff.md` (found in step 1) into `status.md` (state, issues, open decisions), `tech/home-system.md` (how it works, what was built) or `decisions.md` (new decisions, as new rows at the top). Then move it to `archive/`.

## Step 6 — Conventions

Check the "Data naming" patterns in `conventions.md` against the assets. Fix the wrong ones; remove the ones that don't hold.

## Step 7 — Core systems sweep (read-only)

1. For each entry in `tech/core-systems.md`, confirm the files exist at those paths and the description holds. Fix paths. Remove *(verify)* where confirmed.
2. Sweep the combat code for what else combat relies on: base classes most abilities, effects or units derive from; singletons the turn flow calls; data types many systems read. Check `Core/Systems/CombatLogging` in particular. Use the Explore agent.
3. Add what you find, marked *(added in setup)*. Don't remove entries; list removal candidates for THJ.

## Step 8 — Install `CLAUDE.md` and settings

1. Show THJ `git diff --no-index` between the current `CLAUDE.md` and `_pass3/CLAUDE.md`, and the same for `.claude/settings.json` and `_pass3/settings.json`.
2. On his yes, copy both into place.

The new `CLAUDE.md` is shorter on purpose: its Home essentials now live in `tech/home-system.md`, and its combat architecture and dev cheats in `tech/combat-architecture.md`.

## Step 9 — Finish

1. Leave `_pass3/` in place for THJ to delete.
2. Report to THJ, briefly: what moved where, core systems added and removal candidates, anything skipped or uncertain.
3. Propose commits in the private `claude-handoff/` repo, split by unit per the Git rules, for example: (1) agent and skill definitions, (2) moved notes, (3) new docs, (4) core-systems sweep results. Each one: files, `git diff --stat`, message, his yes.

## After setup (THJ)

1. Start a coordinated session from the repo root: `claude --agent miso-coordinator`. Pick its model with `--model` or `/model`.
2. Ask it for status. It should report the branch, the setup item, the two pilots, and what's waiting on you.
3. Optional: `"agent": "miso-coordinator"` in `.claude/settings.json` makes every Claude Code session in this folder a coordinator session. It's read by Claude Code only, not by claude.ai chats or Projects. Whether a desktop-app task linked to this folder honors it, the status check above will show.
4. Then Pilot 1: "Run Pilot 1, the AP and points model question in status.md."
