# Lucy's memory: "ten" → "Two." → "Four." (plan)

Scope: all (on `main` since D-456). Size M (small new sequence step + level/sequence data). Decisions: D-457 (beat and lines, THJ), D-458 (the 8 fade out, THJ), D-459 (layout and build details, coordinator).

## Goal

In Memory 2 · Lucy (`GB_m2-lucy`), stage 1's interruption becomes a running gag played on the board:

1. Lucy: "Then ten more!" → **10 Claws appear** in room 2.
2. Linda (at the hearth): "Two." → **8 of them fade out**; 2 stay.
3. Lucy: "Four." → **2 new Claws appear**. The fight continues against 4 Claws (was 3).

Today: camera to room 2, reveal 3 hidden Claws (9,3 / 10,2 / 9,1), lines "Then ten more!" / "Three.", camera back (`Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Interruption_*`).

## Decisions

- **D-457 (THJ):** the beat and the words as above. Exact text: Lucy "Then ten more!" (kept), Linda "Two.", Lucy "Four.". The fight after it has 4 Claws.
- **D-458 (THJ):** the 8 leave by **fading out** (a memory correcting itself): no death, no XP, no kill event, no kill flash/shake, no barks, no mission stats, no objective count, no tally.
- **D-459 (coordinator, Tier 2):**
  - All 12 Claws are placed hidden in the level (D-345: no spawns in memories): group `ten` (10 Claws) and group `four` (2 Claws). The 2 that stay are on 9,3 and 9,1; the 2 new ones on 10,2 and 10,3 (room 2's far end, 7+ tiles from Lucy, so the throat lesson still holds). The other 8 fill room 2's free tiles (5..10 × 1..3, keeping the throat mouth 5,2 free).
  - Same Claw variant and HP as today's hidden three.
  - Fading is a new non-core sequence step in `Features/Onboarding` (sibling of `RevealUnitsSequence`), e.g. `HideUnitsSequence`: takes a list of units (or a group plus which to keep), fades them out over a short time, then takes them out of play cleanly.
  - Each line gets its own dialog step so the board changes between lines.

## Acceptance criteria

1. Stage 1 plays: camera to room 2 → 10 Claws come in → "Then ten more!" → "Two." → 8 fade out → "Four." → 2 Claws come in → camera back → play resumes. 4 Claws remain in play.
2. The faded 8 leave no trace: their tiles are free for walking, targeting and the Cyclone; they never act, are not targetable, not in turn order; no death event, kill feedback, XP, barks, mission stat or tally entry.
3. Stage 2's win ("all dead") completes when the 4 remaining Claws die; the faded 8 don't block it or count toward it.
4. Skipping the sequence (if skip exists there) ends in the same state as playing it.
5. Restarting the memory (Lost → Try Again, and the level play button) starts clean: all 12 hidden again.
6. Edit-mode tests for the new step's logic (removal leaves nothing behind; no kill events). EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.
7. No core-system API or behaviour change (`tech/core-systems.md`). If clean removal needs one, stop and report: it's Tier 3.

## Docs to update

- `plans/onboarding/2026-10-26-onboarding-levels.md` Segment 2 grid and table (designer).
- `plans/onboarding/onboarding-narrative-draft.md` M2 lines (narrative: "Three." → "Two." / "Four.").
- `tech/classic-fallback.md` only if a new wiring point is added.
- If the grid-to-level tool can't express two hidden groups, the report says so (the level prefab then differs from its doc block; rebuilding it from the doc would lose the groups).

## Commits (proposed in the report)

1. The new hide step + tests. 2. Level and sequence data.
