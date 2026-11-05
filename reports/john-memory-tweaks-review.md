# Review: THJ's uncommitted `GB_m3-john` tweaks + Linda Encore animation (2026-11-05)

`miso-reviewer`, read-only, no plan, worked from the files (MCP down). Saved by the coordinator (reviewer has no Write). **Verdict FIX.** All references resolve; structure consistent (each claw an added child of exactly one cell).

## What changed

- **Claws: 5 now** (HEAD had 4; new one `GB_m3-john.prefab:1292-1353`). Tiles from parent `GridCell - (x, y)` names (same as `HearthMemoryJohnTests.CellOf`). No cell edited; the claws moved.

| Claw (instance) | Tile before → after | turnOrder |
|---|---|---|
| 6368691951050935398 | (1,1) → (1,4) | 4 |
| 4161280069119593364 | (2,2) → (2,5) | 3 (+ `Specs_Health` overrides) |
| 5612908644326730095 | (6,2) → (6,5) | 1 (+ `Specs_Health` overrides) |
| 2945259854029956963 | (7,1) → (7,4) | 2 |
| **new** 2457820463989314698 | — → (4,4) | none (0, acts first) |

- Heroes unchanged: Linda (2,1), John (4,1), Lucy (6,1). No inactive/hidden claws; `allEnemiesStartAlert: 1`. Claws now 4 tiles from the sisters (new one 3 from John); before, adjacent.
- Objectives: one Any group, no queue, no sequence, no shared rids. Kills count 3 → **4**, text → "Defeat 4 Claws: {dead_0} of 4."; turn cap 2 → **3** (ends when turn 4 begins). Defeat group untouched.
- **New `LevelAbilityLock`** (`:2331-2355`): each hero loses both their Duos all level (John: John_Linda, John_Lucy; Linda: John_Linda, Linda_Lucy; Lucy: Linda_Lucy, John_Lucy). Nothing unlocks them. Super Time gap does not apply (separate presets).

## Must fix

1. New claw gives XP: no `lethalDamageXpBonus: 0` override (inherits 3). `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` (`:33-37`) fails.
2. Wire Memory 3 (John) re-run wipes the objective edits: `HearthMemoryWiring.John.cs:31` `KillsToWin = 3`, `:32-33` `TurnCap = 2`, `:144` text. Keeps claws, turnOrders, lock (doesn't touch them). Optionally have it write the lock.
3. `HearthMemoryJohnTests`: `WinningNeedsThreeDeadClawsOrTheTurnCapAndShowsBoth` (`:81-102`, fails `:96`, then `:99`; rename); `TheClawsAreOnTheBoardFromTheStartAndFirstTurnPointsAreLimited` (`:131-153`, fails `:136` 5 vs 4, then tiles `:138-140`).
4. Linda: `EncoreKitTests.ListedLevels_GiveLindaEncore_SetUpAsInHerDefaultKit` (`:37-40`) fails. Default kit's Encore (slot [9] `Linda_Ability_Recall`) now state "Encore", frame 5; the 9 custom-kit levels in `EncoreKitTool.Levels` keep the old copy (e.g. `Level1-C2.prefab:3739-3744` frame 0, state ""). In play they warn on the missing state and Encore plays with no animation. Add Encore tool skips levels that have it: extend it to refresh, or one-off script. Belongs to the Linda commit.

## Questions for THJ

- Lesson setup reversed vs the levels plan (D-350: claws adjacent so they hit on enemy turn 1; Role takes hits, Wrath stacks, Watch idle). Now they walk 3–4 tiles; (2,5) claw walks down Linda's column, so Watch fires. Claw SPD not resolved: can they reach on enemy turn 1? If intended, update Segment 3 of `plans/onboarding/2026-10-26-onboarding-levels.md` (~283-305).
- 5 claws, 4 kills to win: intended, or 5 / "all"?
- New claw turnOrder 0 (acts first, straight at John): intended, or 5?
- Text uses a digit ("4 Claws"); other memories spell numbers out.
- Dialogue: nothing contradicts (no count or turn in John's lines).
- `Specs_Health` overrides on two claws: inspector-drawer noise (same in 9 other levels), harmless.
- Recall `activationMode` 0 → 2 = Instant → EventBasedAnimated (`AbilityEnums.cs:42`): Encore fires on frame 5 of the new "Encore" state. Consistent with the new clip (10 fps, path `Body`), png (feet pivot, point, no mips), and the controller's new state; rest of controller diff is reordering. Clip naming follows Linda's existing assets, not the `A_<Name>_…` convention; fine.
- `EditorSettings` `m_PrefabModeAllowAutoSave` 1 → 0: shared or local?

## Noise (leave unstaged)

`LiberationSans SDF - Fallback.asset`; `-0` rotations (inside the real edit, can't split); `Specs_Health` overrides if not reverted; AI diagnostic, `PreloadScreen.unity`, `ProjectSettings.asset`.

## Proposed commits (once fixed)

1. John level: `GB_m3-john.prefab` + `HearthMemoryWiring.John.cs` + `HearthMemoryJohnTests.cs`.
2. Linda Encore animation: `Encore/` + `Encore.meta` + contents + `AC_Playable_Linda.controller` + `Unit_Linda.prefab` + `Linda_Ability_Recall.asset` + custom-kit level refresh.
3. `EditorSettings.asset` alone, if shared.

## Addendum: Encore consistency (reviewer, after THJ confirmed it's his)

- Slot [9] = `Linda_Ability_Recall` (title "Encore"); the 3 new slot lines sit on it. Controller state `Encore` plays `Linda-Encore-Side.anim`; rest of the controller diff is reordering. All metas present (folder, anim, png: 6 sprites, point, no mips, 100 PPU, feet pivot).
- Clip: 6 sprites on `Body`, 10 fps, no loop. **Frame 5 is the last frame**: play-check that Encore fires (SoulSacrifice uses frame 5 fine). sideVisualMode 1 = LeftIsFlippedRight, right for a Side-only sheet.
- activationMode Instant → EventBasedAnimated is required for the animation to play at all; missing state → activates at once with a warning.
- Encore commit is independent of the John commit.

## THJ's answers (D-393, D-394)

Claws stay far (update levels plan Segment 3); 4 of 5 kills, text "Defeat four Claws: {dead_0} of 4."; new claw keeps turnOrder 0; extend the Add Encore tool to refresh existing slots.
