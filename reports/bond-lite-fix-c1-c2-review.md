# Review: Bond Lite fixes C1 and C2 (2026-11-07)

Reviewer verdict: **APPROVE**, no must-fix. Read from the code and asset YAML; nothing played. The reviewer can't write files, so the coordinator saved this condensed copy.

## Should fix
1. Commit order: `HomeVisitsTests.Hearth.cs` uses `OnboardingOpeningSetup.InitialTutorialField` (defined in `HomeIntro.cs`), so the wiring commit alone wouldn't compile. Commit the setup change first (`HomeIntro.cs`+meta, `Scenes.cs`, `Home - Scene.unity`), then wiring, assets, Hearth data and tests.
2. Optional: `WorldMap_FirstOpen_TutorialSequence` (`HomeVisitsWiring.Hearth.cs:26`) is misnamed; it's the Hearth close's last step. Coordinator: not renamed (THJ playing; cosmetic).

## Verified
- Load order after the Hearth: intro animation, `PlayInitialSequence` (mission completion chain: 5 close lines, John's line, page), null `InitialTutorial` skipped, `EndOpening`. The Hearth's memories chain without Home, so this is the first Home load.
- Once per save via `PlayJustOnce` + saved `PlayedSequencesTracker`; the mark is written at the next save (quit right after: replays only if the Hearth is completed again; same as the Trail).
- Station guard holds through the whole chain; closing the page turns on camera input a moment before `EndOpening`, as the old page did.
- Text and speakers match `reports/bond-lite-fixes-text.md`.
- `Home_Tutorial` referenced only by the scene override; scene diff one line. Classic restore brings it back; `TheHomeSceneShowsNoOpeningPage` added to `tech/classic-fallback.md` red list.
- C1 guard correct, highlight stays active; no test (needs a scene).
- No private IDs, LF no BOM kept, no statics, not AI content, no core system.
- `GridToLevelSettingsTests.Settings_MissingTemplateIsAnErrorAndWritesNothing`: not caused by this change (leftover `__SettingsTest` or fixture order).
