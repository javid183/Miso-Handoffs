# Review: C4a, The River

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-02. Report: `reports/onboarding-c4a-river.md`.

**Verdict: APPROVE**

## Should fix

1. `SearchWiring.River.cs:142-171`: all five clue pieces share layer 0 / order 0 (Claw sorting −1 resolves to that); draw order undefined, may sit under cell art (`GridPluggableEntity.cs:218` bands units by row). Give each its own order or use the ground renderer's layer.
2. `SearchWiring.River.cs:44`: Lucy's role panel reuses `Tut-FR-1.png` (Linda's Watch image?). Play check.
3. `SearchWiring.River.cs:133-149`: scenery destroyed and rebuilt each run → new fileIDs, prefab diff noise. Reuse pieces when present.

## Notes

- All 79 cells match the block; water seals the islands; units on their tiles; family 4+ from every enemy; 11,3 Manhattan 4 from each Archer (range 3); Tutorial; no `LevelAlertSettings`.
- Start/end order right; `CameraSequence` skip restores flags; editor-only, no statics; props have no colliders or `GUnit`.
- MS1: one node, now `isInitialLevel: 1`; Gold 20 + Timber 1 + Fabric 1 all given (`MathUtils.cs:111-117`); `completionGoldReward` 0 correct (`AwardResources` skips 0, `CombatLevelRunHandler.cs:842`); XP 30. Onboarding graph tests unaffected.
- LF, metas, no private IDs, no tag, no core files. One commit.
- **Plan gap (coordinator):** the "first sleeping enemy" panel + sight beat is Required in whichever pair mission comes first (levels plan §UX, lines 646 and 694); not in C4a/C4b criteria.
- Block id/level lines: fixed by the coordinator (`s1-river`).
