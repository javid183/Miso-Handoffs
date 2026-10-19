# Report: B4 R5 John's tether line (item F)

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (play check still needed)

This replaces the blocked report from the first attempt. THJ approved the hook in D-068.

## What changed

- `Core/Managers/GlobalEventBus.cs` (core, additive): new `public UnityEvent<FactionRoleHandlerBase> onFamilyRolePrompt = new ();` in the "Misc" group next to `qteStarted`/`qteEnded`. Its comment sets the contract: raised once for each role QTE that actually started, right after `StartEvent` returned true (so after `qteStarted`), never on the "could not start" path. It says nothing about the outcome, so pair it with `qteEnded` (press, decline or expiry) and `onFamilyRoleActivated` (later, only on a press). The file keeps its BOM and LF line endings.
- `Core/Interactions/Runtime/PlayerController.cs` (core, additive): in `ActivateFactionRole`, after the existing `if (!started) ... couldNotStartActions` line, one comment and `if (started) GlobalEventBus.Instance.onFamilyRolePrompt.Invoke(unit.AbilityOrchestrator.FactionRoleHandler);`. No logic changed.
- `Core/Systems/RoleZoneSystem/Runtime/TetherRules.cs` (+ `.meta`, new): a pure helper.
  - `TetherExit` flags give the reason the tether is not shown or was taken down: NotJohnRole, RoleZoneHidden, JohnGone, NoTargets, QteEnded, RoleActivated, LevelEnded, Disabled, SceneUnloaded.
  - `ExitForPrompt(isJohnRole, showRoleZone, johnValid)` decides whether a prompt shows the tether. `Clears(exit)` and `EndOfPrompt` cover the exits.
  - `SelectTargets` picks which targets get a line: each valid target once, in order, never John, and it is null-safe.
- `Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs` (+ `.meta`, new, not core): a MonoBehaviour that follows the bus the same way RoleZonePresenter and MovePreviewCoverPresenter do (polls in Update, rebinds when the bus changes).
  - It listens to `onFamilyRolePrompt`, `qteEnded`, `onFamilyRoleActivated` and `levelEnded`, and to `SceneManager.sceneUnloaded`.
  - On a prompt from a `JohnFactionRoleHandler` with `ShowRoleZone` on and John alive and on the grid, it draws a straight line from John to each valid ally in `handler.Targets`. The line runs between sprite-bounds centres.
  - The lines are pooled LineRenderers (child objects, created on first need and then reused), 0.05 wide (serialized `lineWidth`), opaque `RoleZoneColor`, with a runtime "Sprites/Default" material. That shader is in Always Included Shaders and draws unlit under URP.
  - They sit on the "Overlay" sorting layer: above Default and DynamicTop, where the units are, and below OverObjects, Roof, Fog, WorldUI and UI. If that layer is missing, the lines fall back to Default with order 32000.
  - The lines are static, with no animation. LateUpdate only refreshes the two endpoints, with no per-frame allocation (cached validity delegate, reused lists).
  - A target that dies or leaves the grid loses its line. The whole tether comes down if John dies or no line is left, on `qteEnded`, on `onFamilyRoleActivated`, on `levelEnded`, on a prompt from another role, on OnDisable and on scene unload.
  - No statics. The material is destroyed in OnDestroy.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: one idempotent `AddComponent<JohnTetherPresenter>` line and a comment in `Awake`, after the two existing R3a/R3b presenter lines, which are unchanged.
- `Core/Systems/RoleZoneSystem/Editor/TetherRulesTests.cs` (+ `.meta`, new): 14 EditMode tests for TetherRules (`MISO.Core.Systems.RoleZoneSystem.EditorTests`).

All new `.cs` files are LF with no BOM, like their RoleZoneSystem neighbours. The `.meta` files use the same two-line form as the neighbours.

## Acceptance criteria

- [x] D-068 hook: the event is declared and raised only when `started` is true. The "could not start" path (R2/F3) does not raise it. Checked by code read (two added lines, diff above).
- [x] Adding the event breaks no listener. Nothing enumerates the bus's fields: the only reflection `GetFields` in the project is `StatBackedEvaluationProbe`, which walks ability presets, not the bus. CombatLog subscribes by name to 16 existing events, all unchanged. `CombatLevelRunHandler` and `CursorSituationDriver` use `qteStarted`/`qteEnded`, also unchanged. Missing serialized UnityEvent data on `LevelBase.prefab` and the scenes takes the field initializer, so no asset edit is needed.
- [x] F, which targets get a line, and the show/exit rules: covered by EditMode tests (TetherRulesTests, 14/14 pass).
- [ ] F, the line on screen: needs the verifier's play check (see "How to see it"). That covers the colour, thickness, drawing order against units and UI, that it shows only during John's prompt, and that it clears.
- [x] Compile: no CS errors after a forced refresh.
- [x] EditMode suite: 161 tests, 160 pass. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, unchanged, AI untouched).
- [x] No change to when a role fires, FTP, AP or AI: the presenter only reads public getters and bus events, and the AI never touches it.

## Save reset

no

## Decisions I made

- Event placement: in the "Misc" group next to `qteStarted`/`qteEnded`, not under the "Combat Log events (record-only)" header, because it is not a log event.
- Raised through `GlobalEventBus.Instance` directly, as the brief says. I added no `Raise*` helper; `QuickTimeEventHandler` already relies on the bus at that point.
- The hook is a two-line edit in `PlayerController`, not a partial file. The call site is inside a local lambda, so a partial file would need more code than the edit.
- Line ends: from the centre of John's main sprite to the centre of each target's sprite (pivot if there is no sprite), so the line does not run along the floor. Straight line, no arc.
- Sorting: the "Overlay" sorting layer, which already exists in TagManager but nothing uses yet. This meets "above units, below UI" without touching the project settings.
- Static line, no animation: one of the two options the brief allowed.
- The line goes to every ally in `Targets`, including one silenced earlier this turn. `Targets` is the same list the role's camera focus uses, and `SilencedTargets` is protected, so I can't filter on it without a core change.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`: the new bus event `onFamilyRolePrompt` and its contract (raised only when a role prompt started; pair with `qteEnded` and `onFamilyRoleActivated`), and `JohnTetherPresenter` on the "Overlay" sorting layer, hosted by `ShowStatsHoverPreview`.
- `build-log.md`: the R5 entry.
- `plans/2026-10-18-family-role-phase0-1.md`: the R5 commit hashes once they are committed.

## Risks and loose ends

- For the reviewer, on event order: when John's prompt starts, the order is `qteStarted`, then `onFamilyRolePrompt` (same frame, inside the same lambda). On a press: the notice callback, then `qteEnded`, then later `onFamilyRoleActivated`. On no press: the ignore callback, then `qteEnded`. R6 can rely on this: a prompt followed by `qteEnded` with no `onFamilyRoleActivated` before the next prompt means a decline. But `onFamilyRoleActivated` comes after `qteEnded`, so R6 has to wait for the notice sequence and can't decide at the moment `qteEnded` fires. Report this to R6.
- Drawing order: "Overlay" sits above every Default/DynamicTop renderer. If a world-space HP bar or unit label renders on Default or DynamicTop instead of WorldUI/UI, the tether draws over it. Screen-space UI is unaffected. Play check.
- Material: `Shader.Find("Sprites/Default")` at runtime. It is in Always Included Shaders, so builds are fine. If it were ever removed from there, the lines would draw with no material (magenta). Low risk.
- The prompt lasts about 1 s (TimedPress, unscaled), so the tether is short-lived by design.
- During the prompt itself, `UISpotlightHandler` is not shown (it is commented out in `loadActions`; it runs only after a press), so nothing dims the line during the prompt.
- Console after the refresh: two Unity asserts, "Internal error - unexpected guid mismatch". They have no stack trace, appear with no compile errors, and the serialization-depth warnings before them are old. They don't look tied to these files, whose `.meta` files are well formed and unique, but the reviewer may want to re-check after a restart.
- Working tree, not mine and not touched: `miso/ProjectSettings/EditorSettings.asset` shows as a **staged deletion** in the index (`D `), although the file is still on disk. It was ` M` (unstaged) at the start of this run, and I ran no git write command. It must not go into an R5 commit; the coordinator should ask THJ about it. `Unit_Lucy.prefab`, `Packages/manifest.json`, `packages-lock.json` and `ProjectSettings.asset` also have changes from THJ's editor.

## Proposed commits

1. `feat(bus): onFamilyRolePrompt event, raised when a Family Role prompt really started (B4 R5, D-068)` (core, own commit)
   - `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
2. `feat(ui): John's tether line to the allies he covers while his role prompt is up (B4 R5)` (plain, depends on 1)
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/TetherRules.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/TetherRules.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/TetherRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/TetherRulesTests.cs.meta`
   - `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`

Do not stage `EditorSettings.asset`, `Unit_Lucy.prefab`, `Packages/*` or `ProjectSettings.asset`.

## Other branches

`thj/home-test` gets this with the rest of B4 on its next merge of `main`.

## How to see it

1. Open a combat level with John and at least one ally. Shared FTP must be at least 1.
2. Put an ally inside John's zone (a diamond of radius 2 around him; the zone outline shows when John is selected) and end the turn.
3. When an enemy attacks that ally, the game pauses and John's prompt appears. While it is up, a thin orange line (John's zone colour) runs from John's body to the ally. With two covered allies in one hit (an area attack), there are two lines.
4. Press the key: the line disappears at once and the shield plays. Run it again without pressing: the line disappears when the prompt times out.
5. Check that no tether appears in these cases:
   - a Duo QTE;
   - Lucy's Catch & Return (projectile) QTE;
   - John's Command Shield Dash passive QTE;
   - the reversion QTE;
   - Linda's, Lucy's or Mark's role prompts;
   - a John trigger that could not start because another QTE was active.
6. Untick `Show Role Zone` on John's `JohnFactionRoleHandler` (Unit_John prefab or the runtime instance) and repeat step 3: there should be no tether.
7. Drawing order: the line draws over units and tiles but under the HUD, unit panels and world-space bars. Check it against an ally standing on a higher tile, if the level has one.
8. Leaving the level while a prompt is up (or ending the level) should leave no stray line. The lines are children `JohnTether_N` of the ShowStatsHoverPreview object in the hierarchy, and they should all be disabled.
