# Review: THJ's uncommitted `GB_m1-linda` rework (2026-11-04)

`miso-reviewer`, read-only, no plan. **Verdict FIX.** All references resolve.

## What changed

- `queueWinGroups` 0→1, 3 stages: (0) kill enemies, turn cap hidden; (1) "Gather your arrows": `UnitTileOccupiedLOCondition`, Linda on (2,7) (a claw starts there); on complete plays `Memory1Linda_Interruption_SequentialSequence`; (2) "Eliminate all enemies", turn cap visible. Turn cap 2→4.
- Grid: 12 new cells (room right: row 7 cols 4–9, (6..8,6), (6..8,8)). 4 new Dark Claws (6,7), (7,6), (7,8), (8,7) in `HiddenLevelUnits` group "hidden".
- New LSB call "reset" = `CurrentPhaseManipulationAction` mode 1 = **End** (not Reset).
- `allEnemiesStartAlert` 1→0.
- Interruption chain (6 new assets, all referenced): DisableInput+HideHUD → CameraToRoom (7,7) → LSB "reset" → Reveal "hidden" 0.6 s → 2 Linda lines → CameraBack → EnableInput+ShowHUD.

## Must fix

1. The 4 hidden claws are active in the prefab (no `m_IsActive: 0`; `GB_m2-lucy` does it); `HiddenLevelUnits.Awake` warns per unit.
2. `HearthMemoryWiring.Linda.cs:28,103-137` (Wire Memory 1 (Linda)) forces 1 group, no queue, TurnCap 2: re-running wipes the rework. It also reuses the condition reference on purpose.
3. `HearthMemoryLindaTests.WinningNeedsAllEnemiesDeadOrTheTurnCap` (:43-67) now fails.

## Questions for THJ

- Turn condition rid `8881842456907219035` shared by all 3 stages; enemies-dead `8046274707106824280` by stages 0 and 2 (= T6).
- Turn cap on every stage: at turn 4 the stages can chain-complete (interruption plays without gathering, then instant win).
- Completed stages stay visible: "Eliminate all enemies" shows twice in stage 2.
- "reset" call ends the phase: End or Reset intended?
- `allEnemiesStartAlert` off: intended?
- Outro "Three Claws. My last arrow." vs 7 claws now.
- `Level1-C1-2.prefab`: six "Square (3..8)" sprites reparented to `Environment` (real edit, unrelated).
- `EditorSettings` `m_PrefabModeAllowAutoSave: 0`: team-wide?

## Noise (leave unstaged)

`GB_m2-*`, `GB_m3-john` (+ `firstTurn: 1` default), `GB_s1-river`, `GB_s2-ridge` (`animationEvents`); `PreloadScreen` `applyFPSLimit`; `ProjectSettings` `preloadedAssets` (Input System adds them); the two test files (stat-only dirty); the AI diagnostic (D-312).
