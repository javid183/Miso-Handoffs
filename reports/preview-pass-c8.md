# Report: Preview pass C8, tether arc

Plan: plans/2026-10-19-preview-pass-tech.md (C8)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (compiles; EditMode 267 of 268 pass, the one red is the known `AIRegressionTest.Baseline_MatchesCurrentAI`). Not play-checked.

## What changed

- `miso/Assets/_Project/Core/Utilities/ArcLine.cs` (new, + .meta): stateless static `ArcLine.SetQuadratic(line, start, end, height, samples)`, plus pure `Evaluate` and `FillPoints`. Same curve as `GUnit.ShowThreatLineTo`: control point = chord midpoint + up * height, so the drawn apex is height / 2 above the midpoint. Samples clamp to at least 2.
- `miso/Assets/_Project/Core/Utilities/Editor/ArcLineTests.cs` (new, + .meta): endpoints, apex = height / 2, zero height is straight, SetQuadratic point count and ends, clamp and null line.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs`: arcs instead of straight lines; shield caps; Overlay layer removed.

## Acceptance criteria

- [x] ArcLine helper, no state, matches GUnit's Bezier: test-covered (EditMode).
- [x] Arc from John's head to each ally's head: anchor is the unit's own `ThreatLineRenderer` child position (the +0.8 anchor), fallback pivot + 0.8. Colour `RoleZoneColor` alpha 0.7, width 0.015, height 1 + 0.15 per cell (Radial distance between current cells), 16 samples. Needs play check.
- [x] Material: `M_LineShine` is only referenced from `UnitBase.prefab` (no code or Resources path), so the presenter reads `sharedMaterial` from John's `ThreatLineRenderer` LineRenderer at Show. If a unit lacks one, it falls back to runtime `Sprites/Default` (the previous behaviour). Needs play check to confirm it picks M_LineShine.
- [x] Sorting: Default layer, order 0 (no sorting layer or order set). Overlay gone.
- [x] Shield cap at the ally end: SpriteRenderer with the handler's `RoleZoneSprite` (John's `ShieldOutline`), tinted with the same colour, scaled to `CapWorldWidth = 0.25` world units, sorting order 1 (just above the arc), pooled and disabled with the tether. If the handler has no sprite, no cap is drawn.
- [x] `GUnit.ShowThreatLineTo` untouched. No new statics.

## Save reset

No.

## Decisions I made

- `ArcLine` lives in `Core/Utilities/` (namespace `MISO.Core.Utilities`): a neutral shared place, so GUnit can switch to it later without depending on the RoleZone system. Tests in `Core/Utilities/Editor/`.
- The helper's `height` is the control-point offset (to match GUnit exactly), so John's tether peaks at half of "1 + 0.15 per cell" above the chord, same as the threat arc at height 1 peaks at 0.5. Say if you want the numbers read as the apex instead.
- Head lookup is by child name `ThreatLineRenderer` via `GetComponentsInChildren<LineRenderer>` once per Show (not per frame); the transforms are cached per target.
- Cap width is an absolute world size (assumes about 1 world unit per cell; not verified against the grid scale).

## Needs THJ

none

## Docs to update

- `design/gdd/family-systems.md` (tether look): arc, 70% alpha, shield cap. `tech/combat-architecture.md`: ArcLine helper location.

## Risks and loose ends

- `timeScale` 0: a LineRenderer still draws; if M_LineShine animates through `_Time` it will freeze (static arc), not checked in play (no Play mode this run).
- A target without a ThreatLineRenderer child anchors at pivot + 0.8, which should match; check an ally with a non-UnitBase prefab.
- Cap sorting (order 1, Default layer) may be hidden by tall units; the design allows raising it later.
- John's tether presenter file had no BOM, LF; kept. New files are LF, no BOM.

## Proposed commits

1. `feat(utils): ArcLine helper for quadratic arc line renderers`: `Core/Utilities/ArcLine.cs` + .meta, `Core/Utilities/Editor/ArcLineTests.cs` + .meta (plain)
2. `feat(roles): John's tether is a thin translucent arc with a shield cap`: `Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs` (plain; depends on 1)

## Other branches

none

## How to see it

1. Enter a combat level with John and allies in his cover range; trigger John's family-role prompt (the paused prompt).
2. An orange, thin arc goes from John's head over to each covered ally's head, with a small shield at the ally end. Check it uses the same look as an enemy threat arc and stays visible while paused.
