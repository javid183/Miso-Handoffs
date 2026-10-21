# Report: Masher play-check fixes 1 (hit flash, ghost facing)

Plan: decisions D-122 (flash) and D-121 (ghost), coordinator brief    Agent: miso-implementer    Branch: masher-tweak
Outcome: done

Revision 1 (review should-fixes, `reports/masher-playfix1-review.md`):
- (2) Applied. For a vertical facing (x about 0), the ghost now takes the body's side: first the handler's `CurrentFaceDirection.x`, then `_lastNonUpFaceDirection.x`, and the authored flip when neither is set. The rule lives in a new pure static, `EntityAnimationHandler.ResolveSideX(float facingX, int currentSideX, int lastSideX, float epsilon = 0.01f)`, covered by 2 new tests.
- (1) Same behavior, different form. `abilityOrchestrator ? ... : null` doesn't compile: `AbilityOrchestrator` is a plain C# class, not a `UnityEngine.Object` (CS0029, which I hit in the first pass). The Unity lifetime check is on the `EntityAnimationHandler` itself (`if (!handler)`); with no handler the ghost keeps its authored flip. I added a comment saying so.
- `GUnit.cs` gained `using MISO.Core.Animation;`.
- Console: no errors. EditMode: 365 tests, 364 passed; only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known). The file lists in Proposed commits are unchanged.

## What changed

Fix 1, hit flash (D-122, not core):
- `miso/Assets/_Project/Core/FX/Runtime/CFX/VolumeCameraEffect.cs`:
  - `RevertIE` no longer sets `volume.profile = volumeProfile`, so a volume keeps its own profile while it fades.
  - Apply, hold and revert run on unscaled time (`Time.unscaledDeltaTime`, `WaitForSecondsRealtime`).
  - The non-additive `Apply` prunes destroyed volumes, then reverts a snapshot of `_activeVolumes` (it used to iterate the live list). The revert coroutines it starts now go into `ActiveVCRs`.
  - The hold-end revert starts once (it started twice), and that one coroutine is tracked in both lists.
  - `RevertIE` stops cleanly if its volume is destroyed under it.
- `miso/Assets/_Project/Core/FX/Editor/CameraVolumeEffectTests.cs` (+ `.meta`, and the new folder `Core/FX/Editor.meta`): new EditMode test that a revert keeps the volume's own profile.

Fix 2, ghost facing (D-121, core: `GUnit`, `PlayerController`):
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`:
  - new `public bool? GetIdleFlipX(int directionX)`. It returns the flip the idle sprite takes for an x direction, or null when x is 0 or the idle mode doesn't flip.
  - `SetDirection` now uses the same private helpers (`EffectiveSideVisualMode`, `FlipXFor`), so the rule lives in one place. This is a behavior-preserving refactor; the same cases still throw.
- `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs`:
  - new overload `ShowGhostAt(Vector3 worldPos, Vector2 facing)`. It flips the ghost `SpriteRenderer` with `GetIdleFlipX` on the sign of `facing.x`. When x is about 0 it uses the unit's current face direction. When that is also 0, or the mode doesn't flip, it uses the ghost's authored flip.
  - The old `ShowGhostAt(Vector3)` now restores the authored flip, so a ghost flipped by an earlier preview doesn't carry over. Before this change the flip was never touched, so this is the same behavior as before.
  - The ghost renderer is cached lazily (instance fields, no statics).
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`:
  - Target-cell ghost (~:974): faces from the unit toward the ghost, which is the move or dash direction.
  - Approach-walk ghost (~:1420): faces the attacked cell. If `targetCell` is null, it falls back to the walk direction.
- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs` (~:105): the step ghost faces the striker's predicted footprint centroid when a slam follows, and the step direction otherwise.
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerFlipTests.cs` (+ `.meta`, and the new folder `Core/Animation/EntityAnimation/Editor.meta`): 5 EditMode tests of `GetIdleFlipX`.

## Acceptance criteria

- [x] (a) A revert never reassigns a volume's profile: covered by the test `CameraVolumeEffectTests.Revert_KeepsTheVolumesOwnProfile`.
- [x] (b) Apply, hold and revert run on unscaled time: checked in code review. There is no test, because it needs running coroutines.
- [x] Any other path that leaves a weight above 0 with no revert pending: I found two and fixed both (see Decisions). No test, because they need `StartCoroutine` and a live frame loop. **Verifier play check.**
- [x] `ShowGhostAt` takes an optional facing and flips the ghost by the body's rule. The rule itself is covered by `EntityAnimationHandlerFlipTests` (left/right flip, x = 0 keeps the facing, `None` with and without a default). The wiring in `GUnit` and the callers needs a play check.
- [x] Public helper on `EntityAnimationHandler`, with the rule in one place: `GetIdleFlipX`, which `SetDirection` shares.
- [x] Existing signature unchanged: Duo previews (`UnitsCooperationHandler`) and John's Command Shield Dash still call `ShowGhostAt(Vector3)` and look as before.
- [x] Called from the Masher preview and both player move-ghost calls.
- [x] Units whose ghost sprite isn't a side sprite: every unit's idle data uses `LeftIsFlippedRight` (on `UnitBase.prefab`; every unit prefab also overrides `useDefaultSideVisualMode`/`defaultSideVisualMode` to 1). So the ghost flips exactly when the idle body would. A unit whose ghost sprite isn't a side view will mirror the same way its body does. I can't tell which ghost sprites aren't side views from the YAML. **Verifier play check** (Goblin Queen, Dark Worm and Toba have custom ghost sprites).
- [x] Compiles: Unity refreshed through MCP, no CS errors.
- [x] Full EditMode suite: 363 tests, 362 passed. Only `AIRegressionTest.Baseline_MatchesCurrentAI` is red (known). The 6 new tests pass, confirmed in a separate run.

## Save reset

no

## Decisions I made

- **Second stuck-overlay path, a clear bug, fixed.** The non-additive `Apply` iterated `_activeVolumes` by index while `RevertIE` ran synchronously.
  - For a volume whose weight was already 0 or below, `RevertIE` removed it from the list before its first yield. That shifted the list, so the next volume was skipped.
  - That next volume's apply or hold coroutine had just been stopped through `ActiveVCRs`, so it stayed at its weight (up to 1) with no revert pending, until some later non-additive apply.
  - Weight ≤ 0 happens on the last frame of a fading flash, or at time scale 0, because the apply curve starts at 0. That fits successive hits from one slam.
  - Fix: iterate a snapshot (`ToArray()`).
- **Duplicate hold revert, fixed.** At the end of the hold, `ApplyIE` started `RevertIE` twice: one coroutine went into `ActiveVCRs`, the other into `SelfActiveCRs`. The two faded the volume twice as fast and destroyed it twice. Now one coroutine is started and tracked in both lists.
- **Reverts started by a non-additive Apply are now tracked in `ActiveVCRs`,** so the next non-additive apply stops them and restarts one revert from the current weight. Before, it stacked parallel reverts on the same volume. Same visible result, without overlapping coroutines.
- **Destroyed volumes are pruned before the revert loop,** and `RevertIE` exits if its volume disappears. This avoids `MissingReferenceException` after a scene change, or after `Revert` destroys extra volumes.
- **No `useUnscaledTime` flag.** Five assets use `CameraVolumeEffect`; none needs scaled time:
  - `UnitHit_CameraVolumeEffect` (UnitBase) and `PlayerHit_CameraVolumeEffect` (the five player units): non-additive hit flashes.
  - `DeathEffect` and `ReactiveInterruptEffect` (PlayerController): additive, persistent.
  - `CameraVolumeEffect_Grayscale` (EnemyIntroductionController): non-additive, persistent.
  - One visible difference: the reactive border used to fade in over 0.5 s of game time at time scale 0.5 (about 1 s real time). It now fades in over 0.5 s real time.
- **Ghost facing vector:**
  - The overload takes a world-space facing (`Vector2`, only the x sign counts), not a target point, so a move and an attack-then-face can share it. Body facing also comes from world x (`MathUtils.GetDirection`).
  - It uses the idle animation's side mode, because the ghost is the unit standing at its destination, not the body's current clip.
  - The Masher ghost faces the striker when a slam follows (that's its final facing), not strictly the step direction. Without a slam it faces the step direction. Same sign in the common case.
- `GUnit` isn't partial, so I edited the ghost methods in place rather than splitting the class.

## Needs THJ

none

## Docs to update

- `tech/core-systems.md` (Units row): `GUnit.ShowGhostAt(Vector3, Vector2 facing)` added (D-121, additive).

## Risks and loose ends

- `CameraEffectBase.SelfActiveCRs` is an instance list on a ScriptableObject asset. It is never cleared, and with domain reload off it survives Play sessions. `ActiveVCRs` grows the same way: its `Where(c => c != null)` never drops finished coroutines, because `Coroutine` isn't a `UnityEngine.Object`. Both are unbounded leaks of stale handles, harmless for the overlay. Not fixed; out of scope.
- `Revert()` still starts a second revert on a volume that another effect's non-additive apply is already fading. Two parallel fades, harmless.
- Ghost facing uses the sign of x, not `GetDirection`'s dominant-axis rule. For a mostly vertical plain move with a small x offset, the ghost picks the x side while the body might face up or down. That's minor and only for previews.
- Not changed: the Duo ghosts (`UnitsCooperationHandler`) and John's Command Shield Dash ghost still don't pass a facing, so they show the authored flip as before. A follow-up could pass a facing there too.
- During the reloads the console showed "Objects are trying to be loaded during a domain backup" (editor errors, no CS errors). It looks like editor-window noise during the domain backup; I didn't confirm whether it was there before.

## Proposed commits

1. `fix(fx): hit flash never sticks on screen: reverts keep each volume's profile, run on unscaled time, and no volume is skipped`. Files:
   - `miso/Assets/_Project/Core/FX/Runtime/CFX/VolumeCameraEffect.cs`
   - `miso/Assets/_Project/Core/FX/Editor.meta`
   - `miso/Assets/_Project/Core/FX/Editor/CameraVolumeEffectTests.cs`, `.cs.meta`

   (plain)
2. `fix(preview): move ghost faces the way the unit will, flipped by the same rule as its body`. Files:
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`
   - `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor.meta`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerFlipTests.cs`, `.cs.meta`

   (core, additive: approved in D-121)

The two commits are independent. Leave the `Packages/` and `ProjectSettings/` changes unstaged.

## Other branches

`main` has the same `VolumeCameraEffect` (the flash fix applies there too). The ghost fix depends on the Masher preview only for its third caller; the `GUnit`/`PlayerController`/`EntityAnimationHandler` part applies to any branch with the move ghost.

## How to see it

1. Open a mission with a Masher Goblin (masher-tweak), then press Play.
2. Flash: hit the Masher with a basic attack so it steps in and slams several units. The red flash should fade every time, with no overlay left. Do the same while John's role prompt is up (time scale 0): the flash still fades. Trigger a reactive interrupt (border) and then take a hit: when the interrupt ends the border clears, with no red tint left.
3. Ghost: with a player unit selected, hover an empty tile to the left of the unit. The move ghost should face left (flipped), like the body after walking. Then hover a tile to the right.
4. Hover an enemy out of reach with a basic attack: the ghost at the approach tile faces the enemy.
5. Aim at a Masher from its left or right: its step ghost faces the striker.
6. Check Goblin Queen, Dark Worm and Toba ghosts look right when flipped.
