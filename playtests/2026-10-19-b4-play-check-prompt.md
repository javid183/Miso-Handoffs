# Prompt for the desktop-app play check

Paste into a Claude desktop app session opened on `E:\Work\Projects\miso`. Model: Sonnet is enough; switch to Opus only if a step needs diagnosis.

---
You are the Miso verifier (see `.claude/agents/miso-verifier.md`). THJ agrees to a play session now and will stay away from the editor and this window. Use computer use to drive Unity (Game view) and the Unity MCP tools for the console and tests.

Do the play check in `claude-handoff/playtests/2026-10-19-b4-play-check.md`: sections A, B and C, all of it, judging readability by eye where it says so (colours, overlap, crowding). Branch is `thj/fr-readability`; do not switch branches, no git writes, no code or asset edits. Resetting the game save is allowed if testing needs it; say so in the report. Read first: the checklist, `claude-handoff/plans/2026-10-18-family-role-phase0-1.md`, `claude-handoff/tech/editor-checks.md` (including the Batch 1 play-check notes at the bottom), `claude-handoff/reports/playtest-batch1-verify-play.md` (how the last session got around), `CLAUDE.md`. Start Play from `Assets/_Project/Scenes/PreloadScreen.unity`. Write `claude-handoff/reports/b4-play-check.md` (template `claude-handoff/templates/report.md`): each criterion Pass, Fail or Not run with evidence (console lines, numbers, screenshots described), new findings, what you could not verify. Leave the editor in Edit mode with no unsaved changes.
---
