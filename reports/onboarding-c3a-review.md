# Review: onboarding structure C3a (memory levels, hidden units)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-01. Plan: `plans/onboarding/2026-11-01-onboarding-c3-memory-levels.md`. Reports: `reports/onboarding-c3a-reveal-check.md`, `reports/onboarding-c3a.md`.

**Verdict: FIX**

Reveal matches `GUnit.SpawnAt` step for step (`SetActive(true)` in place of `Instantiate`); all core calls public and unchanged; not Tier 3.

## Must fix

1. `HiddenLevelUnits.cs:70`: "still hidden" = `!activeSelf`, but `GUnit.Die` deactivates the dead unit (`GUnit.cs:758,779`), so a second `Reveal(group)` revives dead Claws (full HP, double bus listeners, no `unitBorn`). Keep an instance `HashSet<GUnit> _revealed`; test "revealed, then deactivated, not revealed again".

## Should fix

1. `GridToLevelBuilder.Hidden.cs:37`: deactivates the instance root; runtime checks the `GUnit`'s own object. Use `unit.gameObject` or refuse when they differ.
2. `HiddenLevelUnits.cs:85-88`: no guard when `PlugEntity` finds no free cell (`CurrentCell` null → NRE in `DieInternal`, `GUnit.cs:770`); warn, deactivate, skip. Same for `Faction == null` (`:90`).
3. `GridBlockParser.cs:316,329`: bad first token read as a group name (wrong error); a line whose only tile is a duplicate leaves an empty group. Create the group only once it has a tile.
4. `GridBlock.cs:109`: `FindHiddenAt` unused.

## Notes

- Inactive units skipped by every level-start collector (`CombatLevelRunHandler.cs:249/252`, `PrepareUnits`, `GridCell` plugging); restart and sandbox restart reload the prefab. Only editor/preview code sees inactive units.
- `RegisterUnit` re-sorts `OwnedUnits`: safe in the player turn (both C3b cues); in the enemy turn same as `SpawnAt`. AI thread exposure same as summons.
- Levels match the blocks via `level_to_grid.py`; tier/alert set; HP factors on the right cells (`Mathf.Round` snaps 1.9997 → 2). Wolf/Ryker have no scripts. Hearth payloads resolve to `Level`; `completionXPReward` 0.
- `level_to_grid.py`: sound; `mods_of` keeps the first `m_IsActive` override per instance (harmless now).
- LF, no BOM, no statics, no private IDs; 3-commit split builds in order. `HiddenLevelUnitsTests` cover pure helpers only; the reveal at runtime needs the play check.
- C3b: template "defeat every enemy" can be met before the reveal (m2, m4); check Linda/Lucy squad membership for the Bloom grant.

## Fix round re-check (2026-11-01): APPROVE

Must-fix (`_revealed` set, `MarkRevealed` before `Initialize`) and all four should-fixes correct; LF, no BOM, no statics, no private IDs; commit 1 grouping holds. Notes: on the very unlikely failure path (no free cell anywhere) the skipped unit keeps its bus listeners (possible "coroutine on inactive object" logs); `Parser_NoTilesOrABadTileIsAnError` name over-describes. Runtime reveal needs THJ's play check (and a reveal sequence, C3b).
