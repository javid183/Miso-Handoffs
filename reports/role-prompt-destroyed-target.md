# Report: Family Role prompt locks when a target is removed during the prompt

Plan: plans/2026-10-29-role-prompt-destroyed-target.md    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 8293bd358)
Outcome: done (not compiled or run yet: the editor is open, so THJ compiles and runs the tests)

## Confirmed cause: which target it was

**Most likely DarkWorm #08-m03, destroyed by its own split. Not the DarkClaw.**

How a dead unit leaves the scene:
- The normal death, `GUnit.Die(delay)` → `DieInternal(deactivate: true)`, only calls `SetActive(false)` after the delay. The GameObject is **never destroyed**, so `transform.position` still works and can't throw `MissingReferenceException`. The DarkClaw killed by the dash (seq 196) died this way. It also ended at (7,-1), which is outside Linda's lane: she stands at (6,-3), and her zone is her row and column (`LindaFactionRoleHandler.GetCellsInRange`).
- Only `GUnit.DiePermanently(delay)` destroys a unit. It has two callers: a spawner's revert (`AGUnitSpawner`) and **`DarkWormPassiveAbility.Split()`**.
- A Dark Worm that takes damage while it has a next level splits even when the hit doesn't kill it (`lethalDamagePreventsSplit: 0` on `Unit_DarkWorm.prefab`). `HandleDamaged` waits one frame plus 0.8 s of scaled time, then `Split()` calls `DiePermanently(.7f)`. `IsAlive` becomes false right then, and the GameObject is destroyed 0.7 s later. That's about 1.5 s after the hit. Linda's role runs at time scale 1 and the QTE doesn't change it, so that time passes during the prompt.

The sequence in the log:
- The worms spawned in round 5 (#07-m03 and #08-m03, 6 HP) are level 1 of 3 (`darkWormDataList`: 12 / 6 / 4 HP), so they still have a next level.
- Seq 198-199: the dash hit both worms (6→1 HP), so both started a split. It pushed #07 to (7,-4), outside the lane, and #08 from (8,-2) to **(8,-3), in Linda's row**.
- Linda's role triggers on `OnUnitEndMoving` (`triggerEvents: 64`) and waits for processes (`activationMoment: 1`). `ProcessFRApplyWaitList` offered the prompt for #08 once the dash finished. At that moment #08 was still `IsAlive` (1 HP, split pending), so `PrepareTargets` accepted it.
- The split ran during the prompt and destroyed #08. On the press, `Focus(factionRoleFocus)` read the destroyed transform at `CameraHandler.cs:274`.
- The log shows no KILLED for either worm in round 6, but that fits this cause. `CombatLog` only marks deaths (`OnUnitDied` sets `row.Killed`) and writes them at the next flush (the next ability activation, completion or turn change). The press would have been that flush, and it threw first.

The other worm (#07) split too, but it was never a role target.

`GetFactionRoleTargets` returns `FactionRoleHandlerBase.Targets`, which `PrepareTargets` set when the feasibility check ran just before the prompt. `PlayerController.ActivateFactionRole` copied that list, plus the role's unit, into `entities` and `factionRoleFocus.focusTransforms` once, when the prompt opened, and never checked it again.

## What changed

- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`: new outcome `FactionRoleQTEOutcome.TargetsGone`, added after the existing values (`ShouldSilence` is false for it). New pure rules: `Living<T>(items, isLiving)` (drops null and gone items, keeps their order) and `CanRunAfterPress(ownerLiving, livingTargetCount)`.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: new `static bool IsLivingTarget(GameEntity)`. A unit counts while it exists and `IsAlive`; a cell or other entity counts while it exists. New `int KeepLivingTargets()`, which drops gone entries from `Targets` and returns how many are left. Both are additive; nothing calls them except the player flow below.
- `Core/Interactions/Runtime/PlayerController.cs` (`ActivateFactionRole` only):
  - **At the press:** `RoleCanStillRun()` checks that the role's unit is alive and calls `KeepLivingTargets()`. If nothing is left, it logs and runs the new `targetsGoneActions`. That is `BuildSkipActions(TargetsGone)`: the same release as decline or could-not-start (cleanup, camera back, `ClearInProgressAndRefreshEndTurn`, `RestoreTimeScale`), without silencing. Otherwise the notice steps run as before.
  - **Notice steps:** the camera focus and the spotlight loop now use `LivingEntities()`. It filters `entities` and rebuilds `factionRoleFocus.focusTransforms` right before each use.
  - **Right before `base.ActivateFactionRole`** (about 1.4 s of notice steps after the press): `RoleCanStillRun()` again. If the targets are gone by then, it logs and runs `completionActions` (camera back and release). The role doesn't run, so no FTP is spent.
  - The outcome event still reports `pressed = true` in both skip cases, because the player did press.
- `Core/Camera/Runtime/CameraHandler.cs` (defensive): `GetFocusSubjects` skips destroyed transforms and treats a null `focusPoints` as empty. `Focus(query)` and `FocusInstant(query)` return without moving when no subjects are left. Before, every one of these cases threw (a `MissingReferenceException`, or `Min` on an empty sequence), so no working call changes.
- New `Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleLivingTargetsTests.cs` (+ `.meta`, hand-written with a fresh GUID): 13 EditMode tests.

No new static state (only a static pure method), so no `PlayModeStaticReset` hook is needed. No serialized fields changed. The AI doesn't read any of this code.

## Every path checked for the same assumption

| Path | Uses role targets after a wait? | Result |
| --- | --- | --- |
| `PlayerController.ActivateFactionRole` `loadActions` focus | No. It runs when the prompt opens, right after `PrepareTargets` checked `IsAlive` | Unchanged |
| `noticeActions` focus and spotlight loop (`e.transform`, `e.GetMainVisual()`) | Yes | **Fixed:** they use `LivingEntities()` |
| `base.ActivateFactionRole` → `AbilityOrchestrator.ActivateFactionRole` → handler `Activate` | Yes: it passes `Targets` to `Orchestrator.ActivateAbility` | **Fixed:** `KeepLivingTargets()` runs at the press and again right before activation |
| `BuildSkipActions` (decline, could not start, targets gone) | Only the role's unit (silence) | Unchanged; the new skip doesn't silence |
| Linda `Activate` | Passes `Targets` (one enemy) to `ActivateAbility` | Covered by the shared filter; with no target left the role is skipped |
| Lucy `Activate`, Mark `Activate` | Same pattern, one target | Covered |
| John `Activate` | Puts `Targets` (covered allies) in a `HashSet` and the relay record; already skips relaying when the triggering attack ended (`IsInProgress`) | Covered: it now gets only living allies. `RetargetToJohn`'s lambda already checks `c &&` |
| Masher (enemy) role, AI path (`FactionControllerBase.ActivateFactionRoleIfFeasible` → base `ActivateFactionRole`) | No prompt: it activates in the same call as the feasibility check | Unchanged |
| `FactionControllerBase.TryPlayFactionRole` | Goes through the virtual `ActivateFactionRole` | Covered by the `PlayerController` override |
| `_unitsFRApplyWaitList` | Holds the trigger object; feasibility (with Linda's `IsAlive` check) runs again when it's processed | Fine |
| `JohnTetherPresenter` (per-frame lines to John's targets) | Yes | Already guarded: `IsJohnValid` and `_isValidTarget` every `LateUpdate` |
| `RoleBarkPresenter` | Only the role's unit and its handler texts | Fine |
| `CameraHandler.Focus(CameraFocusQuery)` for every caller | Yes, any query with transforms | **Defensive fix**, see above |
| `PlayerController.ActivateFactionSuperTime` | Focuses `SuperTimeUnits` transforms across delays | Same assumption, but those are family units and none gets destroyed. Left alone (see loose ends) |

## Acceptance criteria

- [x] A role prompt whose target (or one of several) dies or is destroyed before the press doesn't throw, and the game continues. Evidence: code. The focus, spotlights and handler targets use only living entities after the press, and the camera skips destroyed transforms. **Needs THJ's play check.**
- [x] If every target is gone, the role is skipped and control returns. Evidence: code (`targetsGoneActions` at the press, `completionActions` before activation); the rule `CanRunAfterPress` is tested. **Play check.**
- [x] If some targets remain, the role runs on the living ones and the camera frames them. Evidence: code (`KeepLivingTargets` and `LivingEntities`); `Living` is tested with destroyed and dead units. Only John's role can have several targets. **Play check (hard to reproduce on purpose).**
- [x] Normal role prompts are unchanged. Evidence: with every target alive, `Living` returns the same list in the same order and `CanRunAfterPress` is true, so the flow is the same as before. **Play check.**
- [x] EditMode tests for the extracted rules. Not run yet: the editor is open. THJ: Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red.

## Tests

`FactionRoleLivingTargetsTests`:
- `Living`: null list → empty; drops null and gone items and keeps the order; every item gone → empty; a mixed list with a destroyed unit, a dead unit and a living unit keeps only the living one.
- `CanRunAfterPress`: runs with the role's unit alive and one target left; skips with no target; skips when the role's unit is gone.
- `ShouldSilence(TargetsGone)` is false.
- `IsLivingTarget`: null → false; alive unit → true; dead unit → false; destroyed unit (`DestroyImmediate`) → false; existing `GridCell` → true.

Units are built the way `AIRegressionTest` builds them: an inactive GameObject, `AddComponent<GUnit>`, and `IsAlive` set by reflection.

## Save reset

No.

## Decisions I made

- A new enum value `TargetsGone` instead of reusing `CouldNotStart` for the skip at the press. The behavior is the same (no silence); the name says why. It's added after the existing values, and nothing serializes this enum.
- The skip also covers the role's own unit being gone (`CanRunAfterPress(ownerLiving, ...)`), not only its targets. It's the same crash class, and the check is cheap.
- The second check right before `base.ActivateFactionRole` covers a target that goes during the roughly 1.4 s of notice steps after the press (a split worm's timing makes this realistic). That skip releases through `completionActions`, as a finished role does, and spends no FTP.
- The filter lives at the start of the player flow and on the handler (`KeepLivingTargets`), not inside `AbilityOrchestrator.ActivateFactionRole`. The AI path has no wait, so it doesn't need it, and this way I didn't change its behavior.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` › Family Roles: add that `FactionRoleHandlerBase` has `IsLivingTarget` and `KeepLivingTargets` (the player flow re-reads living targets after the press), and that `FactionRoleQTEOutcome` has `TargetsGone`. Faction controllers row: `PlayerController.ActivateFactionRole` skips without silencing when the targets are gone at the press or before activation. Camera row (if listed): `GetFocusSubjects` skips destroyed transforms, and an empty focus doesn't move the camera.

## Risks and loose ends

- Not compiled by me (the editor is open). Watch for compile errors in the four edited files and the new test.
- `ActivateFactionSuperTime` has the same "transforms read after delays" pattern (`SuperTimeUnits`), unguarded. It's not in scope, and family units aren't destroyed.
- The two skip logs are `Debug.Log` lines (plain words, no IDs). Remove them if they're too noisy.
- The root cause is that a splitting Dark Worm stays `IsAlive` for about 0.8 s after a non-lethal hit, so it can still be offered as a role target. That's a gameplay rule I didn't change. Linda may still get a prompt for a worm that's about to split; now it just doesn't lock. Whether `PrepareTargets` should reject a worm with a split pending is a design call.
- `LevelLindaJohn-C1.prefab` also shows as modified in `git status`. It isn't mine and isn't on the hands-off list in the brief; leave it out.

## Proposed commits

1. `fix(roles): a role prompt whose target is gone by the press skips cleanly instead of locking the game` (core), files:
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Core/Camera/Runtime/CameraHandler.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleLivingTargetsTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleLivingTargetsTests.cs.meta`

   Stage only these six. `AIFactionBrain.cs` and `AIUnitBrain.cs`, GlobalSettings, the dash asset, PreloadScreen, the `LevelLucyJohn`/`LevelLindaJohn` prefabs, `EditorFPSLimiter` and ProjectSettings stay out. If Unity rewrote the `.meta` on import, it should keep the GUID `c6193110f9734755bbceefe90b353dc9`.

## Other branches

`main` (THJ ports it, per the plan). The code touched has no branch-specific parts that I know of.

## How to see it

1. In Unity, Ctrl+R to recompile. Then Window > General > Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red; `FactionRoleLivingTargetsTests` (13) should be green.
2. Play "A Wolf's Blood" 2/2 (or any level with Dark Worms) with Linda and John.
3. Get a level-1 worm (6 HP, after a first split) next to Linda's row. Hit it with John's Shield Dash so the push ends in Linda's row, then wait about 2 seconds before pressing Linda's Watch prompt.
4. Expected: no exception and no lock. The Console shows "Family Role of 'Unit_Linda…' skipped at the press: …", the camera returns, and you can keep acting and end the turn. No silence is applied.
5. Press the prompt quickly instead: the role fires as normal. If the worm splits during the notice steps, the role is skipped with "skipped after the press" and control still returns.
6. Check that the usual roles play the same as before: a normal Linda Watch on a living enemy, John's role covering an ally, and Lucy's role.

## Review fix

The review found one must-fix: `UISpotlightHandler.Update()` read `_spotlights[i].target.position` every frame. If a target was destroyed after it got its spotlight (a split worm during the roughly 0.8 s execution visual and the fade), this threw `MissingReferenceException` every frame and froze the mask.

- `Features/UI/Spotlight/Scripts/UISpotlightHandler.cs`: `Update()` now skips destroyed targets and packs the rest at the front of the arrays (write index `n`), then calls `SetInt(MatSpotCount, n)`, so no empty entry draws a spotlight at the screen origin. The existing per-frame `Vector4[16]` allocations are left as they were. The file stays LF with no BOM.
- Tests: none added. No pure helper came out of this naturally; the packing is a few lines inside `Update`. **Play check:** in step 5 of "How to see it", the mask stays smooth and the Console shows no per-frame errors when the worm vanishes during the notice steps.

Updated commit 1 (core), 7 files:
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
- `miso/Assets/_Project/Core/Camera/Runtime/CameraHandler.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`
- `miso/Assets/_Project/Features/UI/Spotlight/Scripts/UISpotlightHandler.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleLivingTargetsTests.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleLivingTargetsTests.cs.meta`

The hands-off list now also includes `LevelLindaJohn-C1.prefab`.
