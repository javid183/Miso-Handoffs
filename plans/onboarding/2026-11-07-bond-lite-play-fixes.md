# Bond Lite play fixes (THJ's first full play, 2026-11-07)

Branch: `thj/bond-lite`. Size L (four chunks). Status: approved (THJ's answers D-430 to D-433; coordinator D-434).
Source: THJ's nine findings (status `bond-lite-play-findings`); Explore trace of each (summarised below).

## Findings and answers

| # | Finding | Cause | Answer |
|---|---|---|---|
| 1 | No Ryker lost or sad beat after the memory | Hearth close H5-4 to H5-7 never owned by a chunk; `M0 - The Hearth.completionSequence` empty | Build it (D-434), C2 |
| 2 | Upgrades page after the memory, should be the map | Legacy `HomeManager.InitialTutorial` = `Home_Tutorial` ("Bergson's Home"), PlayerPrefs once per machine; no map page exists | Clear it, add a World map page after the Hearth close (D-434), C2 |
| 3, 4 | Workshop and skill-tree pages only on click | Built as specified ("first open") | Pages auto-play on unlock (D-431), C3 |
| 5 | Null ref opening the skill tree | `AbilityTreePanelUI.Highlight.cs:59`: highlight active, node not in the shown tree, `button` and `_pulsing` both null skip the rebuild branch | Guard (D-434), C1 |
| 6 | Home idles never vary | One shared Searching state (D-358, THJ swaps idles later) | THJ's data task; C4 adds The Trail's own state |
| 7 | Yard station always closed | Training Field opens after M4 (D-357) | Stays (D-430) |
| 8 | No visible Bond | The Yard lifts Bond before the Family tab opens, so no lock is ever seen; Y12-5 to Y12-7 unbuilt | Stage the Yard (D-433), C4 |
| 9 | All four heroes have a point at the first skill-tree open | First XP gives 1 SP (threshold 0), XP split across participants | Keep (D-432); designer corrects first-hour design line 110 |

## Chunks (one implementer run each, one commit each unless noted)

### C1 · Highlight null ref (S, sonnet)
- `Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.Highlight.cs` `Update`: return when no button is pulsing (e.g. `if (_pulsing == null) return;` before the pulse math, or handle `button == null` before the comparison). The highlight stays active so it picks the node up when its tree is shown.
- Acceptance: with a highlighted node not in the shown tree, no exception; switching to the tree that has it starts the pulse. EditMode test if the class can be driven without a scene; otherwise say so.
- Commit: `fix(home): skill tree highlight no longer throws when its node isn't shown`.

### C2 · Hearth close and World map page (M, sonnet)
- `HomeVisitsWiring`: `EnsureHearthClose()` — `DialogNodeSequence` with H5-4 to H5-7 (text from the narrative draft, Margaret as narrator with "Margaret: " prefix, as the seg-4 cutaway does), then a `TutorialSequence` for a new `TutorialDataSO` "World map" (text from narrative, `plans/onboarding/onboarding-narrative-draft.md` W6-1 plus the page body from `reports/bond-lite-fixes-text.md`), chained in a `SequentialSequence`, `PlayJustOnce`, set as `M0 - The Hearth.completionSequence`.
- `OnboardingOpeningSetup.Stations.cs` (or the setup's scene part): clear `HomeManager.InitialTutorial` in the Home scene so the drift test covers it.
- Tests next to The Trail's in `HomeVisitsTests`: the Hearth's completion sequence, its order, PlayJustOnce; the setup leaves `InitialTutorial` empty.
- Acceptance: fresh save, after the Hearth: H5-4 to H5-7 play at Home, then the World map page; no "Bergson's Home" page.
- Commits: wiring + assets + Hearth data; setup change separate.

### C3 · Station pages on unlock (M, opus: Home opening, after D-429's guard)
- `HomeInteractables`: a serialized bool (default off) to play its `tutorialSequence` on the first Home load where it is unlocked.
- `HomeManager.StartIE`: after the initial/completion sequence and before `EndOpening`, for each unlocked flagged station whose page hasn't played this save: camera focus on it, play the page (once per save, via `PlayJustOnce` or the save's played list; not PlayerPrefs). One station per load is enough if two open at once? No: play each in scene order.
- Grandma Table gets a skill-tree page (`TutorialDataSO` + `TutorialSequence`, text from narrative). Flags set on Equipments Cabinet and Grandma Table by the opening setup.
- Must not break: D-429 guard (stations stay blocked until the pages finish), `GuidedSkillSpend` on first open, the Yard chain on The Trail's visit (pages come after it).
- Tests: the selection rule (unlocked, flagged, not played) as a pure function; setup sets the flags.
- Acceptance: the Workshop page plays by itself on the first Home load after the Hearth; the skill-tree page on the first load after River and Ridge; neither plays again; clicking still works after.
- Commit: own commit (every Home load).

### C4 · Yard staging (M, sonnet)
- A new Home state for The Trail's visit (copy of Searching, Lucy's idle swapped for `LucyTraining`, Linda placed near; THJ swaps idles after). `HomeVisitsWiring` points The Trail at it instead of Searching.
- Yard chain: a camera-focus step on the yard before Y12-1; after the Bond step, Y12-5 to Y12-7 (Margaret as narrator) and a placeholder Bond line from narrative ("Linda & Lucy's Bond: Lv 2" style); then the pointer line. Step order: focus, Y12-1 to Y12-4, Bond step, Y12-5 to Y12-7 + Bond line, pointer.
- Tests in `HomeVisitsTests`: chain order, The Trail's Home state.
- Acceptance: after The Trail, Home opens with Lucy training in the yard, the camera on the yard, the lines and the Bond line play, then stations work.

## Narrative needed first (miso-narrative)
World map page (title + body), skill-tree page (title + body), Bond level-up placeholder line, any trim of Y12-5 to Y12-7 and H5-4 to H5-7 for dialogue. Written to `reports/bond-lite-fixes-text.md`.

## Risks
- No new statics planned; if any, `PlayModeStaticReset`.
- Home opening coroutine (C3): an exception leaves stations dead (known D-429 limit); keep pages inside the same guard.
- Classic fallback: the opening setup is onboarding-only; `Home_Tutorial` stays in classic. Note in `tech/classic-fallback.md`.
- Not AI content; regression test unaffected.

## Docs to update
`tech/home-system.md` (pages on unlock), `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` line 110 (designer), narrative draft status of H5/W6/Y12 (narrative), `tech/classic-fallback.md`, build log.

## Text and adjustments (2026-11-07, after narrative)
Text: `reports/bond-lite-fixes-text.md` (placeholder grade). Coordinator choices (D-436): the bridge line "The fire burned low. By morning, the door stood open." goes in as a narrator node between H5-5 and H5-6 (Home can't change state mid-scene); Yard order becomes focus, Y12-1 to Y12-6, Bond step, Bond line "Linda & Lucy's Bond reached Lv 2.", Y12-7, pointer; night lines kept. C3: the Workshop opens after River or Ridge, not after the Hearth, so its page plays on that load; its text gets "This is the Workshop." and "Bergson" for "hero". Open for THJ (non-blocking): "Family point" vs the combat "Family Points (FP)".
