# Review: THJ's hand edits to Memory 4 on top of C1

2026-11-10, `miso-reviewer` (read-only; saved by the coordinator). **Verdict: FIX** (tests/wiring out of sync; runtime fine).

THJ changed (11:47–11:48): `GB_m4-mark.prefab`, `Memory4Mark_Hold_SequentialSequence.asset`, new `Memory4Mark_Hold_ResetTurn.asset` (+ meta). Wiring and tests untouched (still C1).

- **Stage 1:** unchanged (Bloom, `Any`, on complete `Arrival`).
- **Stage 2:** group `All`; one objective `All`/`Reevaluate`, text "John reaches the mouth.\nKill the dark claws near the cub." (one entry, two lines); conditions: John on (6,5); `EntitiesDestroyed` All of **8 Claws**: (9,8), (10,7), (6,4) [walks to (7,7)], arrival pair (10,2), (12,2), Bloom Claws (1,4), (5,4), (3,5). Not listed: Bloom (3,6), den west Claw ((0,4) → (2,4)), `left` group, pool spawns. On complete: Hold.
- **Stage 3:** objective `All`, text "Clear the den while John holds the mouth."; conditions: the three `top` Claws dead AND a new John-on-(6,5) (Reevaluate). No on-complete → outro.
- **Reset step:** `Memory4Mark_Hold_ResetTurn` = LSB call `reset` → `CurrentPhaseManipulationAction` Reset for Bergsons (restart the player turn, AP refilled; no-op in an enemy phase). Hold order: disable input → hide HUD → John's lines → **ResetTurn** → camera up → reveal `top` → unlock Duo → Duo lines → camera back → enable input → show HUD. Net: a fresh turn for the Duo.
- **Mismatches (expected 3 Mark test failures):** `Flow.cs:122` stage-2 text; `:138-139` 3 vs 8 entities; `:152` stage-3 text; `:153` `.Single()` on stage 3 now has 2 conditions (name/comment stale); `:184-186` hidden-unit assertion must allow the `arrival` group. Wiring: `HoldObjectiveText`, `SaveObjectiveText`, `HoldStageClaws` (3-tile), stale comments; retired `WireStages` builds C1's stages; retired Hold builder lacks the reset step (copy the Arrival `BuildCall(..., ResetCallId)` pattern).
- **Risks:** runtime fine (`_newStageEvalWait` blocks evaluation during the on-complete sequence). Stage 3 requiring John = softlock if John is displaced or killed. Reset placed mid-cut-in (cosmetic). Text "near the cub" covers Claws across the map.
- **Commit:** stage the ResetTurn asset + meta with the Hold sequence; leave THJ's unrelated files out.
