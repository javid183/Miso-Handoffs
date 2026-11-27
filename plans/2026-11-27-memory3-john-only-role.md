# Memory 3: only John has a Family Role (build)

Size: S    Tier: 2 inside THJ's approval (D-793; demo tweak H-16)    Assigned to: miso-implementer (sonnet)
Branch: all (THJ is on `main`)
Status: done, THJ played; committed in d8d273083 with the Shield Dash change (not pushed)

## Goal

In Memory 3 (`GB_m3-john`, John + Linda + Lucy) only John's Family Role (Shield) works. Linda's Watch and Lucy's follow-up never trigger, all level long, and their role zones are hidden. No core change: uses the existing public API `FactionRoleHandlerBase.SetSuppressed(owner, on)` / `IsSuppressed` (core 8.1, D-748) and `IRoleZoneVisibility`.

## Acceptance criteria

- [ ] New feature component in `Features/Onboarding/` (e.g. `LevelFamilyRoleSuppression`), serialized list of units. From level start until the level ends it suppresses each listed unit's Family Role (keyed on the component as owner) and hides its role zone.
  - Zone hiding: its own small `IRoleZoneVisibility` component (don't reuse `HoldRoleZoneHidden`: `HoldPickOutOfCombat` sets that one back to visible at its release). Check that the zone presenters handle a unit with more than one `IRoleZoneVisibility` (any one hiding = hidden); if they only read one, report it before changing anything core.
  - Lets go on disable, destroy and level end (`GlobalEventBus.levelEnded`, main thread only, as `HoldPickOutOfCombat` does). Repeated calls safe; dead or missing units skipped.
  - Never changes suppression while Family Super Time runs (follow `HoldPickOutOfCombat`'s wait), though at level start none is running.
  - No statics (or a `PlayModeStaticReset` hook if one is unavoidable).
- [ ] `HearthMemoryWiring.John.cs` (`WireLevel`) adds or updates the component with Linda and Lucy (`LindaUnitName`, `LucyUnitName`), not John; re-runs keep it.
- [ ] The prefab: before running "Tools/Onboarding/Wire Memory 3 (John)", compare the tool's output with THJ's current `GB_m3-john.prefab` (last commit `0fc14602c`, clean in the tree). After the run, the prefab diff must show only the new component(s). Anything else changing → revert the prefab and report.
- [ ] Edit-mode tests: listed units' roles never trigger / `IsSuppressed`, an unlisted unit (John) unchanged, released at disable and at level end, zone hidden then visible; wiring test: Memory 3 lists exactly Linda and Lucy. New partial or new test file, namespace as the existing `HearthMemoryJohnTests`.
- [ ] No IDs (D-, H-) in code, comments or test names. Keep line endings/BOM of edited files.

## Not in scope

Lucy's Papa's Shelter (a Synergy, stays on). Duos (already locked all level). FTP. `GB_m2-lucy` (next request).

## Test plan

Covering: `MISO.Core.Features.Onboarding` fixtures incl. `HearthMemoryJohnTests`, `FactionRoleSuppressionTests`, role zone tests. Then reviewer; then verifier: compile, covering, full EditMode. AI regression not needed (no AI graph, ability or unit prefab change).

## Proposed commit (after THJ's play check)

`feat(hearth): only John's Family Role works in his memory` (component, wiring, tests, prefab).
