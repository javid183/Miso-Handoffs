# Prompt for the desktop-app play check (paste into a Claude desktop app session opened on E:\Work\Projects\miso)

Run `claude --agent miso-verifier` equivalent: in the desktop app, open the project folder `E:\Work\Projects\miso` and paste:

---
You are the Miso verifier (see `.claude/agents/miso-verifier.md`). THJ agrees to a play session now and will stay away from the editor and this window. Use computer use to drive Unity (Game view) and the Unity MCP tools for the console and tests.

Do the play check in `claude-handoff/playtests/2026-10-18-batch1-play-check.md` for B1, B3, B6 and B8 (skip the B5 repro, THJ does it). Branch is `thj/oct-build-fixes`; do not switch branches, no git writes, no code or asset edits (the optional safety-net test uses a throwaway edit that you revert without saving). Resetting the game save is allowed if testing needs it; say so in the report. Read first: the checklist, `claude-handoff/plans/2026-10-18-playtest-batch1-bugfixes.md`, `claude-handoff/tech/editor-checks.md`, `claude-handoff/playtests/playtest-plan.md` ("Setup and rules"), `CLAUDE.md`. Start Play from `Assets/_Project/Scenes/PreloadScreen.unity`. Write `claude-handoff/reports/playtest-batch1-verify-play.md` (template `claude-handoff/templates/report.md`): each criterion Pass / Fail / Not run with evidence (console lines, numbers, screenshots described), new findings, what you could not verify. Leave the editor in Edit mode with no unsaved changes.
---
