# Objective feedback + one result line per level (tech plan, build chunk 6)

Size: M    Tier: 3 decided (design D-466 to D-474 rule list "Small UI rules"; D-477)    Assigned to: miso-implementer (sonnet)
Branch: `thj/after-hearth` (scope **all**: both rules apply on every branch; option off by default for the result line)
Status: approved (D-486), queued after the Hearth memories

## Why

Pacing check: "objective feedback should be more"; the memories' result screens list every stage's conditions. Design: [`2026-11-09-onboarding-after-hearth-design.md`](2026-11-09-onboarding-after-hearth-design.md) "Small UI rules". Code facts: [`reports/after-hearth-tech-explore.md`](../../reports/after-hearth-tech-explore.md) §A.

## Goal

A met objective ticks, pulses once with a short sound, and unfolds the panel; a level can name one summary line that the won / mission-end panel shows alone.

## Decisions

- **D-477 (THJ):** the last objective of a level gets no tick (the HUD hides 0.25 s after the win); the end panel and the result line carry it. No core change.
- **Coordinator (Tier 2):** both pieces stay out of core: the panel side in `ObjectivesPanelUI` / `ObjectiveEntryUI`, the summary line as a level-root component read by `MissionEndPanelUI` (not on the core list; precedent `SistersTallyResultRow`).

## Chunks

### C1 · Tick, pulse, sound (not core)

- In `ObjectivesPanelUI` / `ObjectiveEntryUI`: when an entry turns satisfied, after its strikethrough, scale-pulse the line once (model `QuiverUI.Pulse()`) and play a UI sound through `AudioHandler.PlayUI` with a new `[AudioID(AudioCategory.UI)]` id (placeholder clip; THJ supplies the real one).
- The panel already unfolds on any change (`ObjectivesFoldRules.AfterObjectivesChanged`); keep it.
- Don't replay pulse/sound for earlier stages' lines that rebuild after a stage advance (`SetObjectives` recreates entries; `VisibleWinObjectives` keeps old lines): only a line that changed this update pulses.
- Tests: pure rule for "which entries pulse" (changed to satisfied this update, not rebuilt old lines).

Acceptance: a mid-level objective met → strikethrough, one pulse, one sound, panel open; stage advance doesn't re-pulse finished lines; failure strikethrough has no success sound; tests green.

### C2 · Result summary line (not core)

- New component (e.g. `LevelResultLine`, `Features/UI/...` or `Features/Onboarding/`) on a level root: one localisable-ready string field (plain string like other level text) and an "enabled" flag.
- `MissionEndPanelUI.SetObjectives`: when `CombatLevel.Instance` has the component with a non-empty line on a **win**, show that one line instead of the per-objective rows (one row in the objectives column; stats column untouched). Works on both the level-won panel and the mission-end panel. Loss: unchanged.
- No level gets a line in this chunk except the four Hearth memories, with narrative's lines (placeholders until THJ approves). Memory 2's line quotes no Claw count.
- Tests: the row-choice rule (line set + win → one row; else today's rows).

Acceptance: a memory won shows its single line; any other level unchanged; a loss unchanged; tests green; EditMode only the known AI red.

## Risks

- `SetObjectives` rebuild replays strikethroughs: C1's rule must not double-pulse.
- Sound id: new enum/id entry; no clip yet → placeholder, logged for THJ.
- Prefab edits (`ObjectiveEntry.prefab`, level roots): editor script or Unity MCP, not hand YAML.
- No new statics expected.
- Other branches: `main` will need it when this branch merges.

## Gates

Compile / EditMode / review / THJ play check (a Hearth memory and one normal level) / docs: GDD `missions-structure.md` MI-18 note (designer), `tech/combat-architecture.md` UI note (coordinator).

## Proposed commits

C1 one commit; C2 code + tests, then the Hearth level data.

## Commit log

- C1 `736a39325` (tick/pulse/flash/sound; deferred to HUD return after cut-ins incl. the strikethrough (D-489, D-490); new lines fade in with flash + own sound (D-491); nothing after a win or loss).
