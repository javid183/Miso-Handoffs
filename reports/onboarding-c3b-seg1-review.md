# Review: onboarding C3b segment 1 (Linda's memory level)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-01. Plan: `plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md`. Report: `reports/onboarding-c3b-seg1.md`.

**Verdict: APPROVE** (single commit fine: tool, assets, prefab wiring and tests only work together)

## Should fix

1. `HearthMemoryWiring.Linda.cs:122`: "The memory ends in 1 turns." → plural-free wording, e.g. "Turns left in the memory: {remaining_0}."
2. `[PLACEHOLDER] ` shows on screen: `conventions.md:69` says stripped on screen, but only barks strip it (`HandBackLines.Strip`); `DialoguePlayerUI` and the tutorial panel don't. Choose: strip at display (shared Core UI, THJ's OK) or keep the tag out of asset text and track placeholder status in the handoff. Settle before segments 2-4.
3. `HearthMemoryWiring.Linda.cs:126`: new `TurnReachedLOCondition` each run → new managed-reference id, prefab diff noise. Reuse when present, set `turn` only.
4. `HearthMemoryLindaTests.cs:76`: assert `punchline >= 0` before indexing.
5. `HearthMemoryWiring.Linda.cs:254-258`: `SpriteByGuid` returns null silently; warn or throw.

## Notes

- Turn cap correct: `turn=2` fires at the first evaluation of turn 3 (`CombatLevelRunHandler.cs:120,196,487-488`); turn 3's start effects run first (`:503-505`), harmless here. Any wins on either; win checked before defeat (`LevelObjectives.cs:233`).
- Start sequence: input/HUD per scene; restart reloads; nothing can stay locked.
- End order: punchline → `FadeOutGridSequence` → cutaway → `OutroCutsceneKeepGridHidden`; one fade; advances to segment 2.
- Design flags: the punchline plays on a turn-cap win with Claws alive. Narrative placement: M1-1 at start (draft) vs end (levels plan); H0-4 in the Home scene (draft) vs level intro as "Margaret:" under Narrator. Designer to settle.
- Editor-only wiring script, no statics, HP untouched. No core change, LF no BOM, no private IDs, metas present. Cap firing at turn 3 needs the play check.
- Segment 2's start must hide the grid then fade it in (new start sequence).
