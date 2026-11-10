# Review: Hearth memories C1 (Memory 4's new ending)

2026-11-10, `miso-reviewer` (read-only; saved by the coordinator). **Verdict: APPROVE.** No must-fix, no should-fix.

- Prefab: every fileID resolved. Stage 1 `Any`, Bloom destroyed, cap removed, on complete `Arrival`. Stage 2: one `All`/`Reevaluate` objective "John holds the mouth. Clear the den." = John on GridCell (6,5) AND `EntitiesDestroyed` (All, Reevaluate) of the Claws under (9,8), (10,7), (6,4) (the den-edge Claw PostBloom walks to (7,7)); completes on whichever comes last, John stepping off undoes it; on complete the Hold sequence (unchanged). Stage 3: the three `top` Claws (8,7), (9,7), (9,6), no on-complete (win → outro). No `TurnReachedLOCondition` left. All diff hunks under the CombatLevel's objectives / managed references; nothing else moved.
- Sequences: new John node copies node 0 with "Here they come."; outro "She held on until we reached her."
- Wiring constants and tests match the prefab; a re-run won't bring old text back; tests would fail on a wrong Claw, a leftover cap or Latch mode.
- No private IDs; LF, no BOM, as HEAD; no runtime code; one commit.

Notes: retired `WireStages` would write stage 1 as `All` (prefab `Any`; same behaviour, cosmetic). Orphaned overrides past the new array sizes remain (ignored by Unity, older ones already there). Either-order / leaving-undoes is data-tested only (THJ play item 3). "I'll hold them off. You save them." now plays after the den is clear, before "Here they come." (THJ may keep one). Displaced reveal risk: THJ's call after play. Test helper `Objectives()` pairs objective with condition [0] only; harmless now.
