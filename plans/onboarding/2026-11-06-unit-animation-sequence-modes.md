# UnitAnimationSequence: playback modes and facing

Size: M    Tier: 2 (not on the core list; the design was chosen by THJ on 2026-11-06)    Assigned to: miso-implementer (sonnet)
Branch: all (code), thj/onboarding (Memory 4 data)
Status: approved

## Why

THJ added a John gesture to the Bloom cut-in of `GB_m4-mark`: John points his sword at where Lucy's Cyclone will land. Two things look wrong: he points the wrong way, and the animation ends before the dialog does. The sequence today has no facing, always waits for the clip, and stops a looping clip after one cycle.

## Goal

One `UnitAnimationSequence` asset can play a state facing a set direction, either waiting, not waiting, looping or holding the last frame, and another can send the unit back to idle.

## Acceptance criteria

- [ ] `Level3C1_BossIntroAnimationSequence` behaves exactly as before with no asset edit (the default mode is today's behavior).
- [ ] New field `mode` (enum): `OnceAndWait` (value 0, default), `OnceNoWait`, `Loop`, `HoldLastFrame`, `Stop`.
- [ ] `OnceNoWait`, `Loop`, `HoldLastFrame` and `Stop` let the next step start at once.
- [ ] `OnceNoWait` returns the unit to idle after one play of the clip, also when the clip's Loop Time is on, and does not stop a different animation that has taken over meanwhile.
- [ ] `Loop` keeps playing until the unit's next animation or a `Stop` step. A state whose clip isn't Loop Time logs a warning naming unit and state, and plays once.
- [ ] `HoldLastFrame` stays frozen on the last frame until the unit's next animation or a `Stop` step.
- [ ] `Stop` returns the unit to idle and needs no animation name.
- [ ] Optional facing (`setFacing` bool, default off; `facing` Vector2Int) is applied before the state plays, in every mode, and also flips the side sprite for a unit with a side-flip rule. Facing stays after the animation ends.
- [ ] Optional find-by-tile like `MoveUnitSequence` (`findUnitByTile`, `unitTile`). Nickname lookup only finds living units. Reuse `MoveUnitSequence.FindUnitOnCell`.
- [ ] Inspector hides fields that don't apply (no animation name on `Stop`).
- [ ] Memory 4: John's gesture holds through "Lucy! Keep them busy!", pointing at the Cyclone's target (see Approach 3), then he goes back to idle before Lucy casts.
- [ ] EditMode tests cover what can be tested without a running Animator (at least: mode default is 0, which modes wait, unit lookup by tile and by nickname rules). All tests pass except the known AI baseline and the 10 known `HearthMemoryMarkTests` layout reds.

## Scope

In: `Core/Levels/Runtime/UnitAnimationSequence.cs`, a new test file next to `MoveUnitSequenceTests.cs`, John's asset, a new Stop asset, the Bloom parent sequence.

Out: `EntityAnimationHandler` and `GUnit` code (core: **do not change them**; if the goal can't be met without it, stop and report). No new parallel sequence type. No other cutscenes.

## Touches

Systems: level sequences. Uses without changing: `EntityAnimationHandler` (core), `GUnit.SetDirection` (core).
USPs: none.
Docs: coordinator updates status, decisions and the build log, and adds a note to `tech/level-tools.md`.

## Approach

1. **Read first:** `EntityAnimationHandler.cs` (`Play`, `SimplePlay`, `SimplePlayEndFrozen`, `SetDirection`, `Stop`, `IsPlaying`, `IsLooping`, `HandleFrameAction`), `GUnit.SetDirection` (line 536), `MoveUnitSequence.cs`.
2. **Facing trap:** `SimplePlay` creates an `EntityAnimationData` with `sideVisualMode` None, so a `SetDirection` while that data is current doesn't flip the sprite unless the unit has a default side mode. Apply the facing **before** starting the state, so the flip follows the current animation's rule (normally the idle). Use `GUnit.SetDirection` if it is the correct wrapper, otherwise the handler's; say which in the report and why. Check that the facing isn't reset on Play or on the way back to idle.
3. **Memory 4 data.** THJ's saved assets are in the working tree (uncommitted): `Memory4Mark_Bloom_John_UnitAnimationSequence.asset` (John, state `APTransfer`) and `Memory4Mark_Bloom_SequentialSequence.asset`. Keep the existing GUIDs. Steps today: DisableInput, HideHUD, John animation, JohnCallsLucy dialog, LucyCastsCyclone, and so on.
   - John's asset: `mode` HoldLastFrame, `setFacing` on. John starts on prefab cell (4,2) and Lucy's Cyclone target is cell (3,4), so the point is up and to the left. Read which directions the `APTransfer` state actually has (blend tree or a single clip, `AC_Playable_John.controller`; the state's Motion may be a blend tree stored as a separate asset) and pick the closest. Report the value, and whether up-left can be shown at all.
   - New asset `Memory4Mark_Bloom_John_BackToIdle.asset`: John, mode Stop. Insert it right after the JohnCallsLucy dialog in the Bloom list and before LucyCastsCyclone.
4. **OnceNoWait on a looping clip and Loop's clip check** need code that runs after the sequence has ended: run it as a coroutine on `payload.player`, and exit if the unit is gone, disabled or playing another state. Don't keep state on the asset between plays beyond what the base class already does; assets are shared.

## Risks

- Serialized fields: existing names `unitNickname` and `animationName` stay. New fields only; no renames.
- No new statics. If you add one, add the play-mode reset.
- A hold with no Stop step leaves the unit frozen until it next acts. By design; say so in the field's tooltip.
- Skip: `SkipStep` ends the step; a Loop or Hold started before a skip stays until the next animation. Accept for now, and report if a skip can leave a unit stuck through a turn.
- The AI baseline is not touched. Don't fix or re-baseline it.
- Keep the line endings `UnitAnimationSequence.cs` has.

## Gates

Compile / tests / review / play check by THJ: yes (John's gesture in the Bloom; start `GB_m4-mark`) / docs: `tech/level-tools.md`, status, decisions, build log.
