# Onboarding ↔ `thj/home-test`: merge notes

Owner: coordinator. Every edit `thj/onboarding` makes to a file `thj/home-test` also changes, and how to merge it (D-339). Add a row with each chunk that touches a shared file.

## Recipe

1. Merge as usual. For each conflicted file in the table: take `thj/home-test`'s version whole (`git checkout --theirs` or `--ours`, whichever side is home-test).
2. Open Unity, run **Tools › Onboarding › Apply Opening Setup** (built in C1b, `plans/onboarding/2026-10-31-onboarding-merge-safety.md`), save.
3. Run EditMode: `OnboardingMissionGraphTests` and `OnboardingOpeningSetupTests` must pass.
4. Then the design-level questions below.

## Shared-file edits

| File | Onboarding edit | Commit | home-test changes it? | Dry run 2026-10-31 | Builder re-applies |
|---|---|---|---|---|---|
| `Resources/Game Data.asset` | Opening graph: Hearth initial → River, Ridge → AND → Trail → M4; old M1, M2, M3 ×2, M5–M7 nodes removed | `bb9982c87` | Yes: +4 Home sortie nodes | **Conflict** | Yes (keeps unknown nodes) |
| `Home - Scene.unity` | 4 world-map pins re-pointed (Hearth, River, Ridge, Trail) and renamed; M3 Mark Intro, M6, M7 pins hidden; Mark's select button and Upgrades tab unlock after the Hearth | `bb9982c87` | Yes: ~9.8k lines | **Conflict** | Yes (finds pins by mission, not name) |
| `Unit_Mark.prefab` | `unlockedAfterMission` → Hearth | `bb9982c87` | Yes: stat attribute lines | Auto-merges | Yes |
| `Scenes/IntroScreen.unity`, `Scenes/MainMenuScene.unity` | `initialMission` → Hearth | `bb9982c87` | No | Clean | Yes |

New onboarding-only files (no conflict): the 4 Mission assets (`38bc7db73`), `OnboardingMissionGraphTests.cs` (`f36da02f8`).

## Design questions the merge raises (THJ)

- home-test's Home sorties are graph nodes with no incoming edge, so they are open from the start; with the onboarding graph they would be open before the Hearth. Gate them behind the Hearth (or a later mission)?
- home-test's prologue and day loop vs the Hearth memory: which opening wins on the merged branch.
