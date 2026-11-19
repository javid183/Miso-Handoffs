# Report: Cyclone round 3, C1 fainter cross drawings

Plan: plans/2026-11-18-cyclone-round3-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: done

## What changed

- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCrossView.cs`: tint, chevron and flare alphas are serialized fields (`tintAlpha` 0.18, `chevronAlpha` 0.45, `chevronFlareAlpha` 0.85, Range 0..1, with tooltips). The static colours became hues; alpha is applied in `ApplyLook`. The old `_chevronColor` field became a `_flared` flag. `DimFactor` unchanged (0.4).
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CyclonePreviewTests.cs`: new test `Cross_DrawsFaintTintAndChevronAlphas` (tint 0.18, chevron 0.45). Existing tests needed no change (tint "below 0.5" and dim-factor asserts still hold).

## Acceptance criteria

- [x] Alphas 0.18 / 0.45 / 0.85, serialized, DimFactor unchanged: code and new test. The flare value has no test (needs a live Cyclone; play check).
- [x] No prefab edit: no prefab, scene or asset references `CycloneCrossView` (the view is added at run time), so nothing overrides the defaults.
- [x] Compile clean (console had no errors); EditMode 2114 passed, 1 failed: only `AIRegressionTest.Baseline_MatchesCurrentAI`, inner FAILURES stays 43 (CHECKS 714). Before-count 43 as given in the brief; the run after the change reports 43.

## Save reset

no

## Decisions I made

- Because the view is created with AddComponent, the inspector fields only show on the runtime instance; the tuning THJ gets is by editing the default in code or in Play mode. Same behaviour as the plan's "code defaults, no prefab edit".
- Serialized-field names are new, so no `FormerlySerializedAs`.

## Needs THJ

none

## Docs to update

- none for C1 (value table update comes with the round 3 docs chunk).

## Risks and loose ends

- Inspector tuning only lasts for a Play session unless the component is later put on the Cyclone prefab (not planned).

## Proposed commits

1. `feat(lucy): the Cyclone cross draws fainter, its tint, chevron and flare alphas are tunable fields`: `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCrossView.cs`, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CyclonePreviewTests.cs` (plain)

## Other branches

none

## How to see it

1. Open a level with Lucy, cast the Cyclone: the four touching cells show a fainter blue tint and the arm-tip chevrons are lighter; they brighten (0.85) during the Whirl pull.
2. In Play mode, select the Cyclone and tweak the three alpha fields on its Cyclone Cross View.
