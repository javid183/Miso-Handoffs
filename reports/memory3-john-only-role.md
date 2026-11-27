# Report: Memory 3, only John has a Family Role

Plan: plans/2026-11-27-memory3-john-only-role.md    Agent: miso-implementer    Branch: main
Outcome: done (play check pending)

## What changed

- `miso/Assets/_Project/Features/Onboarding/LevelFamilyRoleSuppression.cs` (+ `.meta`, new): level component; serialized `GUnit[] units`. From its `Start` (and again on `GlobalEventBus.levelStarted`) it suppresses each listed living unit's Family Role through `FactionRoleHandlerBase.SetSuppressed(this, true)` and hides its zone; lets go on disable, destroy and `levelEnded` (main thread only). Never switches suppression on while the player's Family Super Time runs (waits in `Update`). No statics.
- `miso/Assets/_Project/Features/Onboarding/LevelRoleZoneHidden.cs` (+ `.meta`, new): its own `IRoleZoneVisibility` (`Hidden` flag), added to a listed unit at runtime. Separate from `HoldRoleZoneHidden`.
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs`: `RoleSuppressedUnitNames` (Linda, Lucy; a property, not a static field) and `WireRoleSuppression`, called from `WireLevel` after `WireAbilityLock`; gets or adds the component on the level object and sets the two units.
- `miso/Assets/_Project/Features/Onboarding/Editor/LevelFamilyRoleSuppressionTests.cs` (+ `.meta`, new): 12 EditMode tests (namespace `MISO.Core.Features.Onboarding.EditorTests`).
- `miso/Assets/_Project/Content/Levels/Greybox/GB_m3-john.prefab`: wiring output, the new component only (see below).

## Acceptance criteria

- [x] Feature component in `Features/Onboarding/`, serialized unit list, suppresses from level start to level end (owner = the component) and hides the zones: `LevelFamilyRoleSuppression`; tests `Apply_TheListedRolesNeverTriggerAndTheirZonesAreHidden`, `TheLevelEnding_LetsGoOfEverythingForGood`.
  - Own `IRoleZoneVisibility` component: `LevelRoleZoneHidden`. Presenters checked: `RoleZoneVisibility.Hidden` (read by `RoleZonePresenter.HasZone` and `MovePreviewCoverPresenter`) loops over all `GetComponents<IRoleZoneVisibility>()` and returns hidden when any one hides; `RoleZonePresenter.RememberVisibility` also tracks all of them. No core change needed. Test `AHoldsZoneSwitchShowingTheZone_DoesNotShowAZoneTheLevelHides`.
  - Lets go on disable / destroy / level end (main thread only), repeated calls safe, dead or missing units skipped: tests `Disabling_LetsGoOfEverything`, `Destroying_LetsGoOfEverything`, `TheLevelEnding_LetsGoOfEverythingForGood`, `ApplyTwice_LetGoOnce_GivesEverythingBack`, `MissingAndDeadUnits_AreSkipped`, `AUnitThatFallsWhileSuppressed_IsStillLetGo`, `LetGo_LeavesAnotherOwnersSuppressionAlone`.
  - Super Time wait: test `DuringFamilySuperTime_TheRolesWaitForTheEnd` (zone hides at once, role waits, `Update` applies after).
  - No statics: none in either runtime file.
- [x] Wiring adds or updates the component with Linda and Lucy, not John; re-runs keep it: test `Memory3_SwitchesOffTheRolesOfLindaAndLucyOnly`; ran the menu twice, the prefab diff was byte-identical after both runs.
- [x] Prefab diff only the new component: see "Prefab diff" below.
- [x] Edit-mode tests: listed roles never trigger / `IsSuppressed` / `CheckFeasibility` false, John unchanged (`Apply_AnUnlistedUnitKeepsItsRole`), released at disable and level end, zone hidden then visible, wiring lists exactly Linda and Lucy.
- [x] No IDs in code, comments or test names (grep for `D-`/`H-` clean). Line endings: all four files LF, no BOM, like their neighbours (`HearthMemoryWiring.John.cs` was LF without BOM and stays so).

## Prefab diff

Pre-check before running the tool: the prefab and the `Resources/Sequences/Hearth` folder were clean in git; the wiring commits after the prefab's last commit (`0fc14602c`) only touched the start sequence assets, which were committed together with the code (`d42800476`), and the wiring seeds dialogue and step lists only when it creates them. The existing covering fixtures (`HearthMemoryJohnTests`, `HearthMemoryRulesTests`, `HearthMemoryResultLineTests`, `HearthMemoryIntroOrderTests`) passed 33/33 against the unwired prefab, so the tool's settings matched it. A copy of the prefab and the Hearth sequences was kept in the session scratchpad before the run (not needed).

After "Tools/Onboarding/Wire Memory 3 (John)": `git diff --stat` on `miso/Assets` shows only `GB_m3-john.prefab | 18 +++` (plus the wiring script). The 18 added lines are: one `m_AddedComponents` entry on the level object (`targetCorrespondingSourceObject 3765237394018459553`, `addedObject 147272562868792769`) and the new `MonoBehaviour` block `LevelFamilyRoleSuppression` with `units: [7607883068595211265, 505914430083513819]` (Unit_Linda, Unit_Lucy, confirmed by the wiring test). No other asset changed. A second run left the diff unchanged.

## Chunks

### Chunk 1: component, wiring, tests, prefab

- Changed: the files above.
- Criteria met: all, see above.
- Decisions and loose ends: see the sections below.

## Tests run

- EditMode, editor open (Unity MCP): `^MISO.Core.Features.Onboarding.` (all fixtures, incl. `HearthMemoryJohnTests` and the new `LevelFamilyRoleSuppressionTests`), `FactionRoleSuppressionTests`, `^MISO.Core.Systems.RoleZoneSystem.EditorTests.`: **934/934 passed**.
- Focused rerun: `LevelFamilyRoleSuppressionTests` 12/12, `HearthMemoryJohnTests` 9/9, `FactionRoleSuppressionTests` 17/17 (38/38).
- Not run: the full EditMode suite (verifier) and `AIRegressionTest` (no AI graph, AI ability or unit prefab change).

## Reviews and checks

- (written by the coordinator)

## Save reset

no

## Decisions I made

- The role is taken from the unit's orchestrator, or, before the orchestrator is set up, from `GetComponent<FactionRoleHandlerBase>()` on the unit (the same handler the orchestrator picks up in its `Initialize`). It is also re-applied on `levelStarted`. This keeps the "from level start" window closed even when the component's `Start` runs before the units are initialized. Same behaviour, belt and braces.
- Zones hide at once; only the role suppression waits for Family Super Time to end (the plan's wait is about the suppression; hiding a zone cannot upset the Super Time wait).
- A re-enable before the level ends applies again; after `levelEnded` nothing applies any more ("until the level ends").
- The level-end release is forced (does not wait for Super Time), as `HoldPickOutOfCombat` does.
- The wiring test sits in the new test file (class `LevelFamilyRoleSuppressionTests`) rather than in `HearthMemoryJohnTests`, which is not partial.
- `RoleSuppressedUnitNames` is an expression-bodied property returning a new array, so the editor tool adds no static field.

## Needs THJ

none

## Docs to update

- `tech/home-system.md` or the onboarding notes: Memory 3 has `LevelFamilyRoleSuppression` on the level (Linda and Lucy's roles off all level, zones hidden).

## Risks and loose ends

- Not verified in Play: that Linda's Watch and Lucy's follow-up never prompt in `GB_m3-john`, that their zones stay hidden on select / hover / Shift, and that John's Shield still triggers. Needs the verifier's / THJ's play check.
- `RoleZonePresenter` only notices a visibility change for components it saw at its last redraw; a `LevelRoleZoneHidden` added later is picked up at the next redraw (select, hover, Shift). At level start nothing is drawn yet, so this should not show; same as `HoldRoleZoneHidden` today.
- With the sisters suppressed, `PlayerController.SuperTimeUnits` is John alone. If Family Super Time can fire in this memory, it runs with John only. Not checked whether that is reachable here.
- A `levelEnded` raised on the AI worker thread is ignored (same as `HoldPickOutOfCombat`); the claims are then dropped at disable / destroy when the level unloads.
- The unit panel's role badge reads `IsSuppressed` (`UnitPanelUI.RoleBadge.cs`), so it should show the sisters' roles as off; not looked at in Play.
- Console after the last recompile showed Unity's "Objects are trying to be loaded during a domain backup" lines (no CS errors); looks like editor noise unrelated to this change, not investigated.

## Proposed commits

1. `feat(hearth): only John's Family Role works in his memory`: `miso/Assets/_Project/Features/Onboarding/LevelFamilyRoleSuppression.cs`, `.cs.meta`, `miso/Assets/_Project/Features/Onboarding/LevelRoleZoneHidden.cs`, `.cs.meta`, `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/LevelFamilyRoleSuppressionTests.cs`, `.cs.meta`, `miso/Assets/_Project/Content/Levels/Greybox/GB_m3-john.prefab` (plain; feature-side only, no core change)

## Other branches

none (THJ is on `main`)

## How to see it

1. Open `GB_m3-john.prefab`: the level object has a `Level Family Role Suppression` component listing Unit_Linda and Unit_Lucy.
2. Play Memory 3 (John) from the Hearth.
3. Select or hover Linda and Lucy, and hold Shift: no role zone for either; John's zone shows.
4. Let a Claw move into Linda's line and attack next to Lucy's target: no Watch prompt, no follow-up prompt. John's Shield still prompts when a sister is hit near him.
5. Win or lose the memory and play another level: Linda's and Lucy's roles work again there.

## Review should-fixes

Tests only; no production change (no test exposed a bug). Added to `LevelFamilyRoleSuppressionTests.cs` (LF, no BOM, no IDs):

- `TheLevelStarting_SwitchesOffTheRolesTheStartSkipped`: the real level path. All three units dead at `Start` (nothing suppressed), then alive and `OnLevelStarted` invoked: Linda's and Lucy's roles suppressed (never trigger) and zones hidden, John's role and zone untouched; `OnDisable` gives everything back.
- `ReEnablingAfterTheStart_SwitchesTheRolesOffAgain`: `Start`, `OnDisable` (all back), `OnEnable`: both sisters' roles off and zones hidden again, John untouched.
- `TheLevelEndingDuringFamilySuperTime_StillLetsGoAtOnce`: with Family Super Time running (John's role in progress), `OnLevelEnded` releases everything at once.
- The level-end reflection call moved into a small `EndLevel` helper shared by the two level-end tests.

Run in the open editor (EditMode, Unity MCP): `LevelFamilyRoleSuppressionTests` 15/15, `HearthMemoryJohnTests` 9/9, `FactionRoleSuppressionTests` 17/17: **41/41 passed**. Compiled clean (no CS errors). Asset tree unchanged by the run (same `git status` as before). Proposed commit unchanged.
