# Review: quiver restart fix (D-282), 2026-10-28

Reviewer: miso-reviewer. The coordinator saved this file.

**Verdict: APPROVE**

## Should fix (sent to the implementer)
1. A Linda baked into the level can subscribe to the old or a null bus in `OnEnable`. Use an idempotent `Subscribe()` from `OnEnable` and `Start`, and unsubscribe from the cached `_bus`.
2. `QuiverFieldRules` has a `fieldPresent` parameter that is always false. Drop it, or pass the real value.
3. Stale comments ("level's scene", "warns once").
4. The scale compensation is redundant: every `LevelBase` root has scale 1. Remove it.

## Notes
- The field moves with the level and dies with it. Nothing that enumerates the level picks it up, and the AI is untouched.
- `EnsureForRunningLevel` never runs after the level ends and never makes duplicates.
- No core change. LF, no BOM, no private IDs.
- Commit order:
  1. Catch point
  2. Pips
  3. PlayerFaction fix (only its hunks of `GroundedArrowField.cs` and `QuiverArrow.cs`, staged through a patch and `git apply --cached`)
  4. Restart fix
