# Report: B7 rename Daryani's Shop to Daryani's Wares

Plan: none (size S, direct request)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

## What changed

- miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelRunUpgradeRoom.prefab (line 1772): `levelName` override value "Daryani's Shop" -> "Daryani's Wares". Nothing else touched (root GameObject name, objective text at line 1860, tags unchanged).

## Acceptance criteria

- [x] Only the override value changed: `git diff --stat` shows 1 insertion, 1 deletion; diff output shows only that line, LF ending kept (file is LF, no BOM change).
- [x] Name unique and no '|': grep of miso/Assets for "Daryani's" finds only this prefab (line 1772, and the unchanged objective text at 1860). No other level uses "Daryani's Wares".
- [x] No console errors: refresh_unity succeeded, read_console ["error"] returned 0 entries.
- [ ] LevelNameUniquenessCheck run: not run. Uniqueness confirmed by grep only.

## Save reset

no

## Decisions I made

- Skipped running LevelNameUniquenessCheck (no known menu item or entry point checked); grep covers the same property for this one name.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- levelName feeds the per-level random seed, so this level's variants reshuffle once.

## Proposed commits

1. fix: rename Daryani's Shop room to Daryani's Wares (B7): miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelRunUpgradeRoom.prefab (plain)

## Other branches

none known

## How to see it

1. Open Unity, select LevelRunUpgradeRoom.prefab and check the `levelName` value reads "Daryani's Wares".
2. Optionally run the Validation Dashboard level-name uniqueness check.
