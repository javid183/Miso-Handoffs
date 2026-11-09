# Sisters' tally C3 (results row), fix round 2: review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Three should-fix.

## Should fix

1. The three new script `.meta` files are hand-written (2 lines, no `MonoImporter`, no final newline). Reimport the scripts so Unity writes the full form; keep the GUIDs (prefab uses `9d42d16f...`).
2. `SessionEndPanel.prefab`: the two rows are saved active; they're hidden only by `OnEnable`. Create them inactive in `SistersTallyResultRowSetup.EnsureRow` (~line 109).
3. `Editor/SistersTallyResultRowSetup.cs:15-16`: the class summary is stale (two rows in `StatsPanel` after `EnemiesKilledCountStat`; saves the scene only if it opened it). Optional: rename `PanelPrefab_HasTheRowUnderTheStatsColumn_AndItIsWired`.

## Notes (verified)

- Plain nested `StatRow` instances under `StatsPanel`, after `EnemiesKilledCountStat`; Linda then Lucy (`Avatar_Lucy`). Width/icon overrides are layout-driven.
- Hidden rows take no space (VerticalLayoutGroup + ContentSizeFitter); `RefreshStatsColumn` unaffected.
- Tests can fail; EditMode 1714/1715 (known AI red only).
- Setup script: no `SaveAssets`; the scene is saved only if it opened it.
- Prefab +276/-0; scene +4 (mission-end flag only). LF, no BOM, no private IDs, no core edits, no new statics.
- Commit list complete (7 files + 3 metas); THJ's files excluded.
- Open: THJ's look (portrait aspect at 50 px, empty label on Lucy's row). The Trail's end shows no rows after C4's fade.
