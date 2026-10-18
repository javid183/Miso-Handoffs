# Report: B7 apply safe-room objective text

Plan: reports/b7-text-fixes.md    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

## What changed

- `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelRunUpgradeRoom.prefab` l.1860: `displayTextTemplate` value "Exit the refuge." -> "Choose one of Daryani's wares, then reach the exit."
- `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelHealingRoom.prefab` l.1908: "Exit the refuge." -> "Approach the glowing statue to heal, then reach the exit."

## Acceptance criteria

- [x] Both strings changed: `git diff` shows exactly one line changed per file (2 files, 2 insertions, 2 deletions).
- [x] YAML/line endings kept: field is an unquoted plain scalar (`      value: ...`), so the apostrophe in "Daryani's" needs no escaping. Files are ASCII, LF endings, no BOM; unchanged (checked with `cat -A` on the diff).
- [x] No other change: DivineRelic prefabs untouched.
- [x] Unity refresh done; console has 0 errors.
- [ ] Play check: not done (not requested).

## Save reset

no

## Decisions I made

- Used a one-line sed on the exact line number (verified by grep first) instead of an editor script; trivial, same result.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Remaining "Exit the refuge." copies, deliberately not changed: `LevelDivineRelicRoom.prefab` l.2005 and `LevelDivineRelicRoom 1.prefab` l.1979 (text waits on THJ). No other asset or prefab-instance override in `miso/Assets` contains the string (grep over all of Assets: only these four hits).
- Healing text is 57 chars; not checked in the HUD whether the objective box fits it.

## Proposed commits

1. `fix: clearer win-objective text for Daryani's Shop and Anahita's Ashiyan (B7)`: `LevelRunUpgradeRoom.prefab`, `LevelHealingRoom.prefab` (plain). No `.meta` changes.

## Other branches

none

## How to see it

1. Open a run that rolls the Daryani's Shop safe room (or open `LevelRunUpgradeRoom` and press Play) and read the objective in the HUD: "Choose one of Daryani's wares, then reach the exit."
2. Same for `LevelHealingRoom`: "Approach the glowing statue to heal, then reach the exit." Check the text fits the objective box and the stats panel shows "<text>: Success" after exiting.
