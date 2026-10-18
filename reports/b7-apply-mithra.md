# Report: B7 round 2, Divine Relic win objective

Plan: plans/b7-text-fixes.md (Round 2 in reports/b7-text-fixes.md)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

## What changed

- miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom.prefab (l.2005): win-objective displayTextTemplate "Exit the refuge." -> "Take the Divine Relic from the altar, then reach the exit."
- miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom 1.prefab (l.1979): same change.

## Acceptance criteria

- [x] Both prefabs changed, one line each: `git diff --stat` shows 2 files, 1 insertion and 1 deletion each. Line endings (LF) unchanged, no BOM touched.
- [x] No "Exit the refuge" left: grep over miso/Assets returns no hits.
- [x] Unity refresh clean: refresh_unity succeeded, read_console ["error"] returned 0 entries.

## Save reset

no

## Decisions I made

- Edited with a single-line sed on the exact text, so nothing else in the YAML moved.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Not play-checked: the objective text on screen needs a look in the Divine Relic room.

## Proposed commits

1. fix: Divine Relic room objective names both steps (B7): both LevelDivineRelicRoom prefabs listed above (plain)

## Other branches

none

## How to see it

1. Enter a Divine Relic room in a run; the win objective should read "Take the Divine Relic from the altar, then reach the exit."
