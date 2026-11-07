# Review: Mark tests, builder facing, John's mode (2026-11-06)

Reviewer verdict: **FIX**. Read from the diff and assets; tests not run by the reviewer. The reviewer can't write files, so the coordinator saved this condensed copy.

## Must fix

1. `HearthMemoryMarkTests.Flow.cs:226,240-243`: the release step isn't pinned, and the comment has the wrong order. Without `Memory4Mark_Bloom_John_BackToIdle`, John stays frozen and the test still passes.
2. `GridToLevelBuilder.Facing.cs:45-46,64`: big enemies are judged by anchor column, not footprint. `GB_33-deev-wave`'s Deev would turn right though its centre is right of the middle.

## Should fix

- No test covers a hidden enemy.
- Mark camera pin dropped with no replacement (exact match rightly gone; keep a loose pin).
- John's geometry check removed; nothing checks he can reach the den mouth.
- Two of three PostBloom Claw walks pinned loosely.
- Stale names and comments, including `SaveCapObjectiveText`.

## Verified

- Facing rule, scored against every prefab with a hand-set facing: middle of group 15/15 on `GB_m4-mark` and 183/226 across 31 prefabs; left edge 12/15 and 166/226; right edge 15/15 and 184/226. Middle stays. Hand-tuned levels are inconsistent, so no rule hits 100%.
- Edge cases: no heroes, or no player faction, left alone; one hero is the middle; tie takes the leftmost; on the middle keeps the default (3 hand-set enemies differ: `Level1-C3` (-3,8), `Level1-C4` (10,5), `LevelM1-C2` (10,2)); no enemy prefab already faces right; deploy slots count as heroes.
- Writes `GridPluggableEntity.initialDirection` on `GUnit`, read at `GUnit.cs:313`. No YAML check by test.
- A rebuild of an older greybox turns its enemies, as expected. No existing level data changed.
- John's asset: only `mode` changed, 2 to 3. All three `APTransfer` clips have Loop Time off. BackToIdle directly follows the dialog.
- Prefab unmodified. Wiring tool still retired. No private IDs, statics, or leftover folders. Commit order 2, 1, 3 correct.

## For the play check

If the (3,5) Claw is alive when the arrival plays (stage 1 ending on the cap), the walk from (3,7) cancels with a warning, and the Claw stays put. Safe.

## Docs

`claude-config/skills/miso-level-chunks/SKILL.md:110,113`, `tech/level-tools.md:42`.
