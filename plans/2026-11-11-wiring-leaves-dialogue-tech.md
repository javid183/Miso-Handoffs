# Onboarding wiring stops owning dialogue text

Size: M    Tier: 3 (decided by THJ, D-526)    Assigned to: miso-implementer (opus)
Branch: all (on `main` after the merge `b1f9d1f68`)
Status: approved

## Why

After the merge, 13 EditMode tests fail (`reports/merge-main-2026-11-11-tests.md`). THJ's teammate now writes dialogue in Unity by hand (origin/main `ef56cbb07`, `819faab4d`, `05b1eebc4`, `00a389b90`), but the onboarding wiring menus still generate those lines and the tests assert them. A wiring re-run would overwrite the teammate's work. THJ: the wiring keeps building structure but stops owning text (D-526).

## Goal

The teammate's dialogue survives every wiring re-run, and the tests check structure, not wording.

## Acceptance criteria

C1, wiring and tests (`Features/Onboarding/Editor/`: `HearthMemoryWiring.*`, `SearchWiring.River*`, `SearchWiring.Ridge*`, `SearchWiring.Trail*`, the Home visits builder; their tests):
- [ ] **Text:** a dialogue sequence asset that already exists keeps its lines: text, speaker (`characterData`/`characterEnum`), side and node count. The wiring writes lines only when it creates the asset, as seed text. One shared helper, used by every wiring.
- [ ] **Structure:** the wiring still owns what it owns today: cameras, reveals, input locks, objectives, level data and the links between assets. Where the teammate changed a sequential step list (added, removed or reordered steps), find out what changed. Default: the wiring leaves an existing step list alone if it only adds dialogue steps. Report every case where the wiring and the teammate's structure disagree, with a recommendation, and don't silently revert either side.
- [ ] **Tests** stop asserting wording, speaker names and the old `Narrator` name. They assert structure and invariants instead: a line exists where one is needed, the grid fades in before the first line, the end fades out and stays out through the cutaway, the reveal comes before the bark, input comes back on. If the teammate's current assets break a real invariant (for example, a fade now after a line), keep the assert, mark it in the report as a finding for THJ, and don't change the data.
- [ ] **Re-runs:** run every wiring menu twice on the current assets. Neither run changes any dialogue asset, compared by md5 against the merge commit.

C2, the teammate's `HomeMemoryOpeningTests` (3 tests, "This can only be used during play mode", `HomeMemoryOpeningTests.cs:29`):
- [ ] Made edit-mode safe (`EditorSceneManager.NewScene` with an additive setup, and closing the scenes after), keeping each test's intent. Their own commit.

C3, check:
- [ ] Re-run the 3 GridToLevel tests (`m_LockCount == 0`) in the open editor. If they pass, record them as command-line noise. If they fail, report the cause; don't fix them in this plan.
- [ ] Full EditMode: all pass except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (never re-baselined).

## Scope

In: the above. Out: dialogue wording (the teammate's and THJ's), runtime and core code, any data change to the teammate's assets.

## Touches

Systems: editor-only onboarding wiring and tests. No core.
USPs: none.
Docs: `tech/` note on the rule ("wiring seeds dialogue once; Unity edits win"), coordinator; `conventions.md` line, coordinator.

## Risks

- A test loses its teeth: every removed text assert gets a structural assert in its place, and the report lists the pairs.
- Wiring that rebuilt step lists may also drop the teammate's inserted steps: covered by the re-run md5 check.
- Files keep their LF/CRLF/BOM. No private IDs.

## Gates

Compile clean / EditMode / `miso-reviewer` / no play check (no behaviour change) / docs above. Commits: C1 (wiring + tests), C2 (HomeMemoryOpening tests).
