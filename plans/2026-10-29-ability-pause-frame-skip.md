# Ability pause-frame skip: an ability fires before its target is picked

Size: S-M    Tier: 3, approved by THJ 2026-10-29 (D-311); core    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all. Built on `thj/linda-quiver` as its own core commit; THJ ports it to `main`.

## Problem

THJ picked Linda's Explosive Arrow at the start of John's Map level 2, on the first run after a save reset, and got a NRE at `AbilityPreset.cs:391` from `RuntimeAbility.OnAnimationFrame`.

- **Abilities affected:** abilities in `TargetSelectionAnimationMode.PauseFrame` play their clip when picked and pause on `targetSelectionAnimPauseFrame` while the player chooses. Linda's Explosive Arrow (and its copies) pauses on 5 and activates on 7.
- **The catch-up:** `EntityAnimationHandler.HandleFrameAction` (around lines 120-140) invokes every frame it missed in one loop, and keeps going after `Pause()` is called inside it.
- **What goes wrong:** on a slow frame the loop runs the pause frame and then the activation frame. `_ActivateAbility` fires with `_targets` null, which is the crash.
- **Hidden variant:** after one use, `_targets` holds the old targets, so the same skip fires silently at them.

Verified in code by the coordinator; the root cause was found by Explore. Not reproducible on demand.

## Fix

1. **Catch-up stops on pause.** In `EntityAnimationHandler.HandleFrameAction`, stop the catch-up loop as soon as `_paused` becomes true inside it. Set `_lastFrame` to the frame that paused, so that a later `Resume()` continues from the next frame and the activation frame fires after the player confirms.
   - Today the only caller of `AnimationHandler.Pause()` is `RuntimeAbility.OnAnimationFrame`, so nothing else changes. Verify this.
2. **Guard.** In `RuntimeAbility`, the activation event does nothing while the ability is in PauseFrame target selection and activation hasn't been requested (`!_activationRequested`), or when `_targets` is null. Make sure a skipped activation can't leave the ability or the unit hanging.
3. **Resume check.** After `Resume()`, the activation frame must still fire exactly once, even if Unity's animator moved past it during the slow frame. Confirm this by reading the resume path. The worst outcome would be an ability that never fires and locks the turn.

## Acceptance

- [ ] A frame jump across both the pause and activation frames stops at the pause. Activation runs once, only after confirmation, on the chosen targets.
- [ ] No NRE, and no firing at stale targets.
- [ ] Abilities that don't use PauseFrame behave exactly as before.
- [ ] EditMode tests cover the catch-up stop and the guard, as pure logic if possible: extract a small rule if needed. Known red only.

## Constraints

- **Core** (`tech/core-systems.md`): this change only, in its own commit.
- No behaviour change for other animations.
- Keep line endings and BOM. No private IDs.
- **The editor is open:** no batch Unity.
- **AI:** don't touch AI code or the AI regression test.

## Play check (THJ)

- Cap the frame rate at 10, then pick Explosive Arrow several times, from a fresh launch too: it always waits for a target and fires on it.
- At normal fps, the bow, Crescendo and other abilities look unchanged.

## Commit log

THJ played 2026-10-29 at 10 fps, no repro; EditMode 1009/1010 (known red only). `8293bd358` (core, alone). Port to `main`: the two edited files are identical there.
