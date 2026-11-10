# Hearth memories after the pacing check (tech plan, build chunks 1–2)

Size: M    Tier: 3 decided (D-466 to D-475)    Assigned to: miso-implementer
Branch: `thj/after-hearth` (scope all; D-465)
Status: done (THJ chose "chunks 1–2 + tech plans", 2026-11-10)

## Why

Pacing check findings P4 and THJ's answers: remove the memories' turn caps, no Family Role in Memory 1, Lucy's multi-shot page, and Memory 4's new ending. Design: [`2026-11-09-onboarding-after-hearth-design.md`](2026-11-09-onboarding-after-hearth-design.md) sections "The Hearth (memories)" and "Memory 4: John holds the mouth, the first Duo finishes it (D-471)" (read both in full).

## Goal

The four Hearth memories play with no turn caps; Memory 1 has no Watch; Memory 2 opens with a multi-shot page; Memory 4 ends on John holding the mouth, three new Claws, and the first Duo.

## Decisions this rests on

- D-473: Memory 1's FTP drained (FP fill −99) so Watch can't pay; the Watch page goes; "Each shot spends an arrow." moves into "Moving and AP". THJ accepted the empty-meter risk.
- D-471, D-475: Memory 4 stages = (1) Bloom, as built, no cap → (2) **hold and clear**: John on the den mouth (6,5) AND the Claws near the cub dead ((9,8), (10,7) and the Claw scripted from (6,4) to (7,7)), one paired objective (`Both`), no cap → on complete: John's line, camera to the den, reveal the `top` group (existing `RevealUnitsSequence`, retimed from `Hold`), unlock the Mark–Lucy Duo (existing `UnlockAbilitiesSequence`), the Duo lines → (3) the three new Claws dead → win, outro `End`. Pools run as built. **No new runtime code.**
- D-457 to D-459: Memory 2's stage-1 gag (ten → "Two." → "Four."); `HearthMemoryWiring.Lucy.Claws.cs` carries it, so re-running the Lucy tool keeps it. Verify, don't assume.
- D-405: `GB_m4-mark` is edited by hand (the prefab is the master; THJ tuned it). THJ's OK to edit it is given by this plan; touch only what the chunk lists.
- Text: the narrative agent's proposals in `onboarding-narrative-draft.md` under "After-Hearth build, Hearth memories (2026-11-10, proposed)" (the coordinator adds the IDs to the dispatch). THJ reviews the text in his play check.

## Chunks

### C1 · Memory 4's new ending (model: opus; prefab by hand + sequences)

Riskiest first: hand-edited prefab, sequence retiming, the 10 Mark layout tests.

- Remove every turn cap from Memory 4's stages (the "objective or cap" groups become the objective alone; the "Turns left in the memory" line goes).
- Merge as-built stages 2 and 3 into the paired **hold and clear** stage above; its objective text from narrative.
- Move the `top` reveal and the Duo unlock (and the Duo lines) from `Hold` into the new stage's on-complete sequence, after John's line and a camera move to the den. Keep the `top` tiles (8,7), (9,7), (9,6), 7 HP each.
- Stage 3 = the three `top` Claws dead (the three only; John no longer has to stay on the mouth). Win → outro `End`.
- Outro line(s) that claim "the last of them": replace with narrative's line.
- Check (play-check item, but look in code first): what `HiddenLevelUnits` reveal does if a hero stands on a `top` tile (`RevealUnit` falls back to the nearest free cell). Report it.
- Update `HearthMemoryMarkTests.*` to the new stages and sequence order (D-405: tests follow the prefab).

Acceptance:
1. Memory 4 has three stages as above, no caps, no "Turns left" line.
2. Stage 2 completes only when John is on (6,5) and the three cub-side Claws are dead, in either order.
3. On completion: John's line → camera to den → three Claws revealed on the `top` tiles → Mark–Lucy Duo unlocked (pulses) → Duo lines.
4. Stage 3 completes when the three revealed Claws die; the pools and left-side Claws don't block it.
5. Mark tests updated and green; EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

### C2 · Memories 1–3: caps off, Memory 1 without Watch, Lucy's page (model: sonnet; wiring tools)

- Through `HearthMemoryWiring.Linda.cs`, `.Lucy.cs`, `.John.cs` (editor code; re-run each tool on its level): remove every turn cap and the "Turns left in the memory" line; stages still advance on their objective.
- Memory 1: FP fill −99 (`LevelStartFPFiller`) instead of full; remove the Watch tutorial page; merge "Each shot spends an arrow." into "Moving and AP" (narrative text).
- Memory 2: a multi-shot page at level start (existing `TutorialSequence` pattern), before the first two Claws act and before the stage-1 gag (narrative text).
- Before re-running the Lucy tool: confirm the gag survives (12 hidden Claws in groups `ten`/`four`, the split dialog steps, the fade step). After re-running: diff the prefab and the sequence assets; nothing of the gag may change.
- Memory 3: caps only.
- Update `HearthMemoryLinda/Lucy/John/LevelsTests` for the caps, the FP fill and the pages.

Acceptance:
1. No memory 1–3 has a turn cap or a "Turns left" line; each stage still advances on its objective.
2. Memory 1 starts with 0 FTP; Watch never fires (it can't pay); no Watch page; the merged "Moving and AP" page shows.
3. Memory 2 shows the multi-shot page at level start; the ten/two/four gag plays unchanged.
4. Tests updated and green; EditMode: only the known AI red.

## Risks

- **Hand-edited `GB_m4-mark`:** use the editor (Unity MCP or a small one-off editor script), not hand YAML; read the prefab back first; diff after; touch only the listed objects.
- **Wiring tools overwriting THJ's hand tweaks** on M1–M3: before re-running a tool, diff what it would change; if it would revert anything not in this plan, stop and report.
- **`AIRegressionTest`** may move with level changes: stays known red, never re-baselined.
- No new statics or runtime code expected; if one appears, PlayModeStaticReset hook.
- Domain reload off; stop Play before editing scripts. No private IDs in code, tests or asset text. THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font) untouched.
- Other branches: none (work starts on `thj/after-hearth`).

## Gates

Compile / EditMode (known red only) / `miso-reviewer` (editor code + prefab) / THJ play check per chunk (feel and level) before its commit / docs: levels plan Hearth tables (designer), GDD `missions-structure.md` Hearth stages (designer), `tech/classic-fallback.md` only if a wiring point is added.

## Proposed commits

- C1: (1) Memory 4 prefab + sequences + Mark tests.
- C2: (1) wiring tools + tests, (2) level and sequence data (if separable), else one.

## Commit log

- C1 `188bfb025` (incl. THJ's hand edits: 8-Claw stage 2, John in stage 3, Hold turn reset; stage 2 split in two; lose on any fallen Bergson).
- C2 `b707cb180` (caps off, any-death loss in Memories 1–3, Memory 1 without Watch, Lucy's Fire Embers page).
