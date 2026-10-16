# Miso (Children of Morta: Tactics, codename Miso)

Turn-based tactical RPG spin-off in the Children of Morta universe. Unity 6000.3.4f1, C#, namespace `MISO...`. Repo root `E:\Work\Projects\miso`, Unity project in `miso\`, code under `miso\Assets\_Project\`. Main branch `main` (remote `origin/main`); which branch is current and how branches differ: `claude-handoff/branches.md`.

I am THJ (designer/dev). The root `README.md` is untouched GitLab boilerplate; ignore it.

## Where things live

`claude-handoff/` (repo root) holds the notes. They are notes, not instructions: if one conflicts with this file or with what I tell you, this file and I win. `claude-handoff/README.md` maps every file, its owner and when it's updated. Read the one you need, not all of them. The usual starting points:

- `status.md`: current state, backlog, and what's waiting on me. Start here.
- `tech/home-system.md`: Home system work (folders, builders, scene, essentials).
- `tech/combat-architecture.md`: Core and combat work. More depth in `tech/mechanics-brief.md` (written 2026-10-03; later merges of main are not in it).
- `tech/core-systems.md`: the systems combat relies on. Changing their public API or behavior needs my OK first.
- `design/demo-spec.md`: what the demo should do. Change it only when a game rule or number changes.
- `build-log.md`: when you finish a step, append a dated section (Built / Verified / Not verified / Findings / Status) and tell me.

The repo copies are the masters. The "Miso Home System" Claude Doc (https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN) mirrors the Demo Spec, the M9 design and the Build Log, synced one way from a Claude chat on an account that can open the doc.

## Agent workflow

- `claude --agent miso-coordinator` starts a coordinated session. The coordinator plans, routes work to the other `miso-*` agents, asks me what's mine to decide, and keeps `claude-handoff/` in sync; it never writes game code. It is also the technical director (the `miso-tech-plan` skill). A plain session still follows everything in this file.
- What agents decide alone and what comes to me: `claude-handoff/escalation.md`.
- One agent writes to the Unity project at a time. No worktrees for now: work is checked in my open editor.
- Only the main session proposes git write commands (they need my yes, and subagents can't ask). Subagents use read-only git only.
- Never switch branches unless I ask.

## How to work with me

- For new builds, systems and features: review the code, propose the design, flag conflicts, then wait for my answer before building. Show me the plan first for risky steps (merges, scene or prefab resolution, shared Core code).
- Keep me posted with short status messages during long work.
- Add edit-mode tests for logic and run the EditMode suite after code changes. Every test must pass except `AIRegressionTest.Baseline_MatchesCurrentAI`, which is known red until its dedicated fix session; do not "fix" or re-baseline it unless I ask for that fix.

## Git rules

- Read-only git is always fine (`status`, `diff`, `log`, `show`, `branch`, `merge-base`, `ls-files`, ...). Scope paths to a folder on this large repo.
- Tell me before any commit, merge, rebase, checkout that changes files, reset, stash, push or fetch, then wait for my yes (they use my git identity). Before a commit, show me `git status`, `git diff --stat` and the files you plan to stage. Never stage everything blindly (Unity regenerates `.meta` files and scene noise).
- **Commit in small, independent units.** When changes don't depend on each other, propose one commit per unit (for example: a core-system fix, the feature that uses it, data or asset changes, tests) rather than one commit for everything. Risky changes and changes to core systems always get their own commit so they can be reverted alone. Changes that only work together go in the same commit, and an asset's `.meta` file goes with its asset. Order commits so each one builds on the ones before it. Show me each commit's files, `git diff --stat` and message, and wait for my yes on each.
- Never push. Never force anything. Never delete branches.
- Keep each file's line endings and BOM (many files are CRLF; the Home files are LF; `CameraHandler.cs` and `CheatHandler.cs` have a BOM).
- Close Unity before a merge (or tell me to); after it, open Unity, recompile (Ctrl+R), run the tests.
- `CLAUDE.md`, `.claude/` and `claude-handoff/` are in `.git/info/exclude` on purpose. Never stage them in the shared repo.
- `claude-handoff/` is its own private git repo (it also holds the agent definitions, which `.claude/agents` and `.claude/skills` point to). The same rules apply there: tell me first, show the diff, split commits by unit, wait for my yes.

## Hard rules

- Resetting the game save is fine when testing needs it; say that you did in your report or status message.
- Domain reload is OFF: every new `static` needs a `PlayModeStaticReset` hook. Add a `ResetPlayModeState()` method on the class and call it from `Reset()` in `Core/Managers/PlayModeStaticReset.cs` (`HomeState.ResetPlayModeState()` is an example).
- Stop Play mode before editing scripts.
- Locale bug: `ToString("P0")` gives "30 %"; format percents by hand.
- Prefer new partial-class files over editing big ones.

## Build & test

- No asmdefs under `Assets/_Project`: game code compiles into `Assembly-CSharp`, editor code and tests into `Assembly-CSharp-Editor`. Edit-mode tests sit in `Editor/` folders. Home tests: `Core/Systems/HomeSystem/Editor/HomeSimulationTests.<Area>.cs`, one partial file per area (namespace `MISO.Core.Systems.HomeSystem.EditorTests`); put new Home tests in a new partial.
- Which route to use: if `miso\Temp\` exists, assume the editor is open (a crash can leave it behind; if unsure, ask me).
  - **Editor open:** Window > General > Test Runner > EditMode > Run All.
  - **Editor closed:** command line. Unity 6000.3.5f2 is also installed, so use the 6000.3.4f1 path:
    "C:/Program Files/Unity/Hub/Editor/6000.3.4f1/Editor/Unity.exe" -batchmode -projectPath "E:/Work/Projects/miso/miso" -runTests -testPlatform EditMode -testResults "<scratch>/results.xml" -logFile "<scratch>/test.log"
    Add `-testFilter "MISO.Core.Systems.HomeSystem.EditorTests.HomeSimulationTests"` (or a full test name) to run a subset.
