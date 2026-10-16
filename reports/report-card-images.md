# Report: Report-card context images

Plan: plans/2026-10-16-report-card-images.md    Agent: miso-implementer (saved by the coordinator; the implementer's Write was refused for report files)    Branch: thj/home-test
Outcome: done (code written; not compiled or tested by the implementer)

## What changed

All under `miso/Assets/_Project/Core/Systems/HomeSystem/`. New files are LF with no BOM.

- `Runtime/Simulation/HomeHeadlineContext.cs` (new): pure helper with no Unity types.
  - The `HeadlineContextSource` enum has None, WorkshopItem, Upgrade, Recipe, Mission and Thread.
  - `HomeHeadlineContext` has `SourceOf(kind)` and `ShowsContextImage(kind)`.
- `Editor/HomeSimulationTests.HeadlineIcons.cs` (new): 4 EditMode tests.
  - The kind mapping.
  - Bond level, Skill point and None show no image.
  - `refId` survives `HomeHeadlines.Build` for all five kinds.
  - `FindWorkshopItem(_sword.Id)` resolves with a reachable null `icon`, and an unknown id returns null.
- `Runtime/UI/HomeDayHUD.Headlines.cs` (edited, LF kept): `RefreshHeadlines` now adds a 60 pt "Context Image" after the speaker portrait, inside the rebuilt Speaker Row, when `ContextIconOf` returns a sprite. `ContextIconOf(sim, card)` is a new private static method.
  - Weapon uses `sim.FindWorkshopItem(refId)?.icon`.
  - Upgrade, Recipe, Mission and Thread cut use `sim.Cycle.Find<T>(refId)?.icon`.
  - It returns null for an empty `refId`, an unknown id, or an unassigned icon.

## Acceptance criteria

- [x] Workshop item card shows `EquipmentSO.icon`: code path is `FindWorkshopItem(refId)?.icon`. Needs a Play check.
- [x] Upgrade, Recipe, Mission and Thread cut cards show the definition's `icon`: code path is `Cycle.Find<T>(refId)?.icon`. Needs a Play check.
- [x] A null icon or failed lookup shows nothing: no image is created, so no faint square. Needs a Play check with a null-icon card.
- [x] Bond level and Skill point cards are unchanged: their kinds map to None, covered by a test.
- [x] No stale or duplicate images on Next: the image is a child of the Speaker Row, whose children are destroyed on each rebuild. Needs a Play check.
- [x] No new fields in `HomeReportEntry`, `HomeDayReport` or `HomeSaveData`: none added, and no existing file other than the HUD was touched.
- [x] Pure helper with EditMode tests: yes.
- [ ] Console clean and EditMode suite green: not verified (verifier).

## Save reset

No.

## Decisions I made

- The image is 60 pt, placed after the speaker name, with the portrait still first. This is inside the plan's 56 to 64 range.
- The helper returns a source enum rather than only a bool, so the card's switch and the tests share one mapping.

## Deviations from the plan (no behavior change)

- The plan's "Mission" kind is `HomeHeadlineKind.MissionRevealed` in the code, and the helper maps that.
- `HomeUiKit` is at `Runtime/Presentation/HomeUiKit.cs`, not `Runtime/UI/`. It was not edited.

## Needs THJ

None.

## Docs to update

- `tech/home-system.md`: one line on the context image and `HomeHeadlineContext` (coordinator).
- `build-log.md`, `status.md`, `decisions.md`: coordinator, after verification.

## Risks and loose ends

- Demo content icons may be unassigned. Those cards simply show no image.
- An earlier Edit was refused by the permission classifier. The implementer stopped and made the edits only after THJ changed the permission mode.
- No builders run; no scenes, prefabs or assets touched; no statics added.

## Proposed commits

1. Home: headline context helper and tests (plain). Files: `Runtime/Simulation/HomeHeadlineContext.cs` and `Editor/HomeSimulationTests.HeadlineIcons.cs`, plus their `.meta` files once Unity generates them.
2. Home: show a context image on Dusk headline cards (plain). File: `Runtime/UI/HomeDayHUD.Headlines.cs`.

Keep the `TextMesh Pro` font asset and the `ProjectSettings` changes out; they are unrelated.

## Other branches

None.

## How to see it

1. Open `Scenes/PreloadScreen.unity` and press Play. Reach a Dusk where Ben finishes a Workshop item. The card shows the item's icon beside the portrait.
2. Check a Recipe or Mission card, and a card whose icon is null. The null-icon card should show no image and no blank square.
3. Press Next through several cards. There should be no stale or doubled images. Bond level and Skill point cards show only the portrait.
