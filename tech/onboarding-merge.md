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

## What the builder does not re-apply (C1b report)

- Home station unlock lists, the Family tab (`UpgradesPanel` `characters[5]`) and the `HomeStates-Idles` M4–M7 requirements: C1 didn't change them; C5 re-homes them and adds them to the builder's table.
- Home-test's sortie nodes: kept as they are, not gated (see below).
- Apply on a scene that really changes re-adds Unity's nine empty `GlobalEventBus` UnityEvent fields: strip or accept that noise in the diff.
- `Unit_Mark.prefab` is rewritten through prefab contents (a 4-line diff in the proof run): check its diff after the first real merge run.
- Apply stops before writing if a target scene is open with unsaved changes: save or close it first.

## Design questions the merge raises (THJ)

- home-test's Home sorties are graph nodes with no incoming edge, so they are open from the start; with the onboarding graph they would be open before the Hearth. Gate them behind the Hearth (or a later mission)?
- home-test's prologue and day loop vs the Hearth memory: which opening wins on the merged branch.
