# Report-card context images

Size: M    Tier: 3 (Home presentation, decided by THJ 2026-10-16, D-043)    Assigned to: miso-implementer (sonnet)
Branch: thj/home-test (Home system; scope `thj/home-test`)
Status: ready to dispatch

## Why

THJ's request (backlog, pilot 2): Home report cards show an image tied to their context when one is assigned. Example: a finished Workshop item's report card shows the equipment's icon.

## Goal

At Dusk, a headline card shows a context image beside the speaker portrait for these kinds: Weapon, Upgrade, Recipe, Mission, Thread cut. The image is hidden when no icon is assigned. Bond level and Skill point cards are unchanged (portrait only).

## Decisions already made (do not reopen)

- Surface: the Dusk headline card only (`HomeDayHUD.Headlines.cs`). Not the Dining Table text, not the recap strip.
- Kinds: Weapon, Upgrade, Recipe, Mission, Thread cut. Placement: beside the portrait in the "Speaker Row".
- No save-format change. Resolve the sprite at display time from the existing `refId`; do not add a field to `HomeReportEntry` or a `Sprite` to `HomeHeadline`.

## Acceptance criteria

- [ ] A finished Workshop item's card shows the equipment's `EquipmentSO.icon` (via `sim.FindWorkshopItem(card.refId)`).
- [ ] Upgrade, Recipe, Mission and Thread cut cards show the definition's `icon` (via `sim.Cycle.Find<T>(refId)`).
- [ ] When the icon is null (or the lookup fails), no image is shown and no error or blank square appears.
- [ ] Bond level and Skill point cards look as before.
- [ ] Cards that change with the next headline (Next button) never leave a stale image or duplicate images (the row rebuild cleans up the new element).
- [ ] No new fields in `HomeReportEntry`, `HomeDayReport` or `HomeSaveData`; existing `ReportPersistence` tests still pass.
- [ ] A pure helper decides which kinds show a context image and which definition type to look up, and has EditMode tests (new partial file, see below).
- [ ] Console clean; EditMode suite green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: `HomeDayHUD.Headlines.cs` (rendering), a small pure helper (kind to "has context image" mapping) in the Simulation or Presentation folder following `tech/home-system.md`, tests.
Out: Dining Table, recap strip, Station window, save data, demo content icons (do not assign new art), builders, scene or prefab changes.

## Touches

- Systems: Home presentation only. No core system from `tech/core-systems.md` (the Home simulation was removed from that list in D-032; the Home is still Tier 3 for design changes, which THJ decided).
- USP: Managing the Home as a Family (presentation only).
- Docs: `tech/home-system.md` (one line on the context image and its helper), `build-log.md` (dated section), `status.md`.

## Chunk 1 (one implementer run, sonnet)

Goal: context image on Dusk headline cards.

Files likely touched (code under `miso/Assets/_Project/Core/Systems/HomeSystem/`, call it `HS`):
- `HS/Runtime/UI/HomeDayHUD.Headlines.cs`: in `RefreshHeadlines` (about lines 40-74), after the speaker portrait (`HomeUiKit.Portrait(row, sprite, 72f)` at about 58-59), add the context image using the same helper. The Upgrade branch (about 64-69) shows how to do a per-kind extra. The row rebuild destroys all children except the speaker text (about 55-56): make sure the new image is created inside the rebuilt row so it is cleaned up each time. `_headlineKey` already includes `refId`.
- Sprite lookup: Weapon: `sim.FindWorkshopItem(card.refId)?.icon` (`EquipmentSO.icon`). Others: `sim.Cycle.Find<T>(card.refId)?.icon` with the right `HomeDefinition` type (`HomeUpgradeDefinition`, `RecipeDefinition`, `HomeMissionEntry`, `DungeonThreadDefinition`; all have `icon`, see `HS/Runtime/Definitions/HomeDefinition.cs`). Precedent: `HomeFromHomeBanner.cs:69` draws `recipe.icon` with `HomeUiKit.Portrait(row, ..., 36f)`.
- Size: pick a size that sits with the 72 pt portrait (about 56 to 64). Use `HomeUiKit.Portrait`; if it tints a null sprite faint, skip creating the image when the sprite is null instead.
- Pure helper (no Unity types): maps `HomeHeadlineKind` to "shows a context image" (true for Weapon, Upgrade, Recipe, Mission, ThreadCut). Put it with `HomeHeadlines` or a new small static class in `HS/Runtime/Simulation/` (no `Sprite` there).
- Tests: new partial `HS/Editor/HomeSimulationTests.HeadlineIcons.cs` (namespace `MISO.Core.Systems.HomeSystem.EditorTests`, partial class `HomeSimulationTests`): the kind mapping; `FindWorkshopItem` resolves an ordered item's `refId` to an item whose icon field is reachable (use `NewKnowledgeSim()` and `_sword`); a headline for each kind keeps its `refId` through `HomeHeadlines.Build`.
- Model: sonnet.

Risks and how the plan handles them (from `miso-tech-plan` checklist):
- New statics or caches: none. Do not cache sprites in a static.
- AI: not touched.
- Serialized field renames or saved data shape: none (by decision).
- Assets, prefabs, scenes: none. The headline card is built at runtime; do not run any Home builder (Setup Home Scene, Build Presentation UI, Build House View).
- Event subscriptions or coroutines: none new.
- Line endings: files are LF (verified for `HomeDayReport.cs`, `HomeHeadlines.cs`, `HomeSimulation.Knowledge.cs`, `HomeUiKit.cs`, `HomeDayHUD.Headlines.cs`, `HomeSimulationTests.Headlines.cs`). Keep LF; new files LF.
- `refId` means different things per kind (character name for SkillPoint, equipment id for Weapon, none for BondLevel): resolve per kind only, never by a generic lookup.
- Demo content may not assign icons for every definition: the null case must be handled and checked in Play.
- Other branches: scope is `thj/home-test` only (no Home on `main`).

## Test plan

- EditMode: the new partial plus the existing `Headlines`, `ReportPersistence` and `Knowledge` tests. Run through the Test Runner if the editor is open (see `CLAUDE.md`).
- Play check (needs THJ's time, started from `Scenes/PreloadScreen.unity`): play to a Dusk where Ben finishes a Workshop item and check the card; check one Recipe or Mission card; check a card whose icon is null; check Next through several cards for stale images.
- No win path, drops or rollback are touched, so no win playthrough.
- The verifier run also confirms each line of `tech/editor-checks.md` on THJ's machine and reports corrections (D-031).

## Docs to update

- `tech/home-system.md` (coordinator): one line on the context image.
- `build-log.md` (coordinator): dated section after verification.
- `status.md`, `decisions.md` (coordinator).
- No design doc change; the Demo Spec does not describe card visuals.

## Proposed commits (for the report)

1. Helper plus its tests (pure C#).
2. Card rendering in `HomeDayHUD.Headlines.cs`.
(Keep `TextMesh Pro` font and `ProjectSettings` assets out; they show as modified for unrelated reasons.)

## Gates

Compile clean; tests pass (known red excepted); reviewer not required (no core system); every criterion checked with evidence; docs updated; Play check by THJ.
