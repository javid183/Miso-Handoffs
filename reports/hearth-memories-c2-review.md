# Review: Hearth memories C2 (Memories 1–3)

2026-11-10, `miso-reviewer` (read-only; saved by the coordinator). **Verdict: APPROVE.** No must-fix.

## Should fix (after THJ's play, so the editor isn't recompiled mid-play)

1. Lose tests don't check the faction (`HearthMemoryLevelsTests` `NoMemoryEndsOnATurnCountAndEveryOneIsLostWhenAnyOfTheFamilyFalls`; Linda/Lucy/John `TheMemoryIsLostWhenAnyOfTheFamilyFalls`): add `Assert.AreEqual("Bergsons", fallen.factionRef.entityID)` (or read via `SerializedObject`). `Claim<T>` writes "Enemy" into claimed conditions, so a slip would end each memory on the first Claw kill. Data is correct today (inherits `LevelBase` Bergsons on rid 8046274707106824281).
2. `HearthMemoryWiring.Lucy.Defeat.cs:23` fresh `HashSet<long>` claim: a shared reference with a win objective would be overwritten silently. Optional: Levels test asserts the defeat condition's id isn't among win-group ids.
3. Re-wrap the merged `<summary>` lines (`John.cs:19`, `Linda.cs:20`, `Lucy.cs:22`). Cosmetic.

## Notes

- Caps gone (one objective per win group; leftover overrides past array size inert). **Memory 2's stage 1 now ends only on two deaths: a player who kills nothing never sees the gag** (intended; THJ to feel it).
- Memory 1 `fpAmountToFill: -99` (same as the M2 levels); no ability refills FTP. Play check: level-start FP gain / `ResetToInitial` on restart must run before `LevelStartFPFiller`, including after Try Again.
- Memory 2 page step between the opening dialog and input enable; text = AH-2; gag assets unmodified in git.
- Lose rule: rid 281 `Exist <= 0` → `NotExist >= 1`, same as Memory 4; decoys excluded via `IsUnitIgnoredForObjectives`.
- THJ's tuning: only objective sizes, defeat fields, M1 filler moved.
- No private IDs; LF/no BOM; Memory 4 untouched. Shared lose rule as a partial on `HearthMemoryWiringLucy` follows the existing shared-helper pattern (Memory 4 keeps its own private copy; tidy later). One commit fine. AI content untouched.
