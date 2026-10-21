# Report: Quick wins A, C2 (Q12): John's shield animation variants

Plan: plans/2026-10-21-quick-wins-a-tech.md (C2)    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (code written), **not compiled, tests not run**. The Unity MCP tools didn't connect this session (ECONNREFUSED at session start; `127.0.0.1:8080` answers HTTP 404 now, but no tools were loaded). THJ needs to compile and run the tests.

## What changed

- `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs` (UTF-8 BOM and LF kept): additive state variant (D-133).
  - `SetStateVariant(string suffix)`, `ClearStateVariant()`, and a read-only `StateVariantSuffix`. An empty suffix clears.
  - `public static ResolveStateName(name, suffix, Func<string,bool> hasState)`: returns `name + suffix` when a suffix is set and the state exists, otherwise `name`.
  - `Play` stores the resolved name in `_targetStateName` and passes it to `animator.Play`, so `HandleFrameAction` and `_playReady` follow the state that is really playing. With no suffix set, the old code path runs unchanged: same name, no `HasState` call, no delegate allocation.
  - When the variant changes and the idle is playing (by idle state name), the idle is replayed so the pose swaps at once. If the resolved name is unchanged, nothing is replayed. Any other state keeps playing, and the variant applies at the next `Play`. Before the first `Play` (handler not initialized), only the suffix is stored.
  - `IsPlaying(stateName)` also returns true when `stateName` was requested and its variant is the state playing. The old result (name match and `normalizedTime < 1`) is unchanged.
- `miso/Assets/_Project/Features/Player/John/Scripts/JohnShieldRelay.cs` (LF, no BOM, as before):
  - New `OnEnable` subscribes to `_unit.TagSet.OnTagGained/OnTagRemoved`, `GlobalEventBus.unitDied` and `levelEnded`, then syncs.
  - `OnDisable` unsubscribes and clears the variant. The existing fireball cleanup is unchanged.
  - Sync rule: shield up (`IsShieldUp`) and alive → `SetStateVariant("_Shield")`, otherwise `ClearStateVariant()`. John's own death and level end also clear it.
- New: `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerVariantTests.cs` (+ `.meta`, fresh GUID `71c65080ef9b439eb6d78f496b3aae51`). 8 EditMode tests:
  - 6 for the resolve rule: no suffix, variant exists, variant missing, empty or null name, null lookup, and which name gets looked up.
  - 2 for set/clear on a handler that has never played anything.

No controller, clip, prefab or `PlayModeStaticReset` change. No new statics (`ShieldStateSuffix` is a `const`).

## Frame-timing check (mandatory): passes

| Clip | Frames | Rate | Loop |
|---|---|---|---|
| `A_Playable_John_PrimaryAttack_{Down,Side,Up}_A` (normal) | 12 | 10 | no |
| `A_Playable_John_Shield_PrimaryAttack_Down` | 8 | 10 | no |
| `A_Playable_John_Shield_PrimaryAttack_Side` | 8 | 10 | no |
| `A_Playable_John_Shield_PrimaryAttack_Up` | 8 | 10 | no |

- John's Primary Attack (`Unit_John.prefab`, abilities[0]): `abilityActivationFrame: 4`, its SFX/FX animation event at `frame: 4`. All three shielded clips have frames 0 to 7, so frame 4 is reached before the end. The freeze risk at `EntityAnimationHandler.cs:97-100` doesn't apply.
- Other things that can play a state on John while shielded:
  - His Duo entries in `PlayerController.prefab` play Run, SoulSacrifice and ItemUse, all with activation frame 0. Only Run has a `_Shield` version.
  - The shielded attack is 0.8 s against the normal 1.2 s, so the attack finishes sooner.
- Blend trees: `Idle_Shield`, `Run_Shield` and `PrimaryAttack_Shield` use the same `DirectionY` thresholds as the normal states (-1 Down, 0 Side, 1 Up). Facing and flip come from the ability's `animationData.sideVisualMode` / the idle data, which are unchanged. The three states are in the Base Layer's child states, so `HasState(0, ...)` finds them.
- `Run_Shield` clips carry the same two `PlaySFXSlot` events as `Run` (footsteps stay).

## Acceptance criteria

- [ ] Q12: shielded idle, run and primary attack in three directions; idle swaps at once; back to normal when the shield ends; other states unchanged; hit lands on the activation frame; no new transitions or parameters.
  - **Not run** (needs THJ's play check).
  - By reading: "no transitions or parameters" holds (the controller is untouched), and the activation frame is safe (table above).
  - The resolve rule and the set/clear behaviour are covered by EditMode tests.
- [ ] Compile clean; EditMode suite green except `AIRegressionTest.Baseline_MatchesCurrentAI`.
  - **Not run** (no Unity MCP). Run `MISO.Core.Animation.EditorTests.EntityAnimationHandlerVariantTests`, then the whole suite.
  - The Editor.log showed play mode had been exited before I edited (the last entry is a `0.backup` scene restore).

## Save reset

No.

## Decisions I made

- Tier 1: the "is the idle playing" check compares the current animation data's state name with the idle data's name, so a `SimplePlay("Idle")` counts too. The replay uses `Play(idleAnimationData, null, flushRemainingEvents: false)`, the same call `Stop()` makes.
- Tier 1: the variant follows every tag gain or removal on John (it re-checks `IsShieldUp`), not only the `Status.ShieldUp` tag. This is simpler and can't miss an exclusive-sub removal. It also syncs in `OnEnable`, so a resurrected John with the shield still up gets the pose back.
- Tier 1: with no variant set, `Play` skips the resolve call entirely, so behaviour stays byte-for-byte the same for every other unit.
- Tier 1: no `HasState` cache. It runs once per `Play`, and only while a variant is set, which the plan allows.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md` (or the animation notes): `EntityAnimationHandler` has state variants (`SetStateVariant`/`ClearStateVariant`). `<State><suffix>` is played when the controller has it, and John's `JohnShieldRelay` sets `_Shield` while `Status.ShieldUp` is on.
- `build-log.md`, `status.md`: C2 built, pending compile, tests and play check.

## Risks and loose ends

- Not compiled and not tested by me. This is the first thing to check.
- A variant change during a pause (QTE pause sets animator speed 0) while idle replays the idle. `Play` doesn't touch the speed, so it stays frozen, but `HandleFrameAction` can set `_playReady` back to true while paused. The idle has no frame actions, so I expect no visible effect.
- `PlaySwitchAnimation` still compares the plain switch name. There is no `Switch_Shield`, so this is harmless today. If a `Switch_<suffix>` state is ever added, it would replay each selection.
- `JohnShieldRelay`'s own Taunt (Shield Flare) and `IsPlaying("Taunt")` wait: no `Taunt_Shield` exists, so it is unchanged.
- The shielded primary attack is shorter (8 frames against 12). The hit is still at frame 4, but the recovery is shorter. That is a feel point for THJ, not a bug.
- `GTagSet.RemoveTemporaryTagsSilently` (on death) does raise `OnTagRemoved`, despite its comment. Either way, death clears the variant through `unitDied` too.

## Proposed commits

1. `feat(animation): state variants on EntityAnimationHandler and John's shielded idle, run and attack`. Plain, but under review (animation and handler API). Files:
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnShieldRelay.cs`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerVariantTests.cs`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EntityAnimationHandlerVariantTests.cs.meta`

   If the reviewer wants the handler API on its own, split it in two: the handler and the tests first, then `JohnShieldRelay.cs`.

The pre-existing unrelated changes (`Packages/manifest.json`, `packages-lock.json`, `ProjectSettings/*`) are not mine. Don't stage them.

## Other branches

`thj/home-test` gets this when it takes `main`.

## How to see it

1. Make sure Play mode is off, focus Unity and let it recompile (Ctrl+R). Check the Console for errors.
2. Window > General > Test Runner > EditMode: run `EntityAnimationHandlerVariantTests`, then Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red.
3. Play a level with John (and Lucy, to check the Shield Flare). On John's turn, use his Shield ability. When it ends, his idle should be the shield pose (`Idle_Shield`).
4. Turn him to face down, side (both left and right) and up, for example by moving one cell each way. The shield idle should face the right way, with the side view flipped correctly.
5. Move him: he should play `Run_Shield` with footsteps. Attack with the Primary Attack in each direction: he should play `PrimaryAttack_Shield`, and the damage and hit sound should land mid-swing with no freeze.
6. Get hit while shielded: the normal Hit plays, then he returns to the shield idle.
7. Let the shield expire (or remove it with the cheat panel) while he is idle: the pose should switch back to the normal `Idle` at once. Move and attack again: the normal Run and PrimaryAttack should play.
8. Check another unit (Lucy, an enemy): idle, run and attack look exactly as before.

## Rev 1 (review should-fixes, `reports/qw-a-c2-review.md`)

- `EntityAnimationHandler.ReplayIdleIfPlaying`: returns early when a frame callback (`_actionOnFrame`) or an end freeze (`_freezeOnEnd`) is active, so a variant change never cuts short a play that carries a callback. The variant then applies at the next `Play`.
- `JohnShieldRelay`: the event-bus subscription (`unitDied`, `levelEnded`) is now lazy. `TrySubscribeEventBus()` runs in `OnEnable`, in `Start` and on each tag change, and an `_eventBusSubscribed` flag makes it subscribe only once. `OnDisable` removes the listeners only if it subscribed, then resets the flag. The flag is an instance field, not a static.
- Line endings and BOM kept: the handler still has its BOM, both files are LF. Still not compiled or tested, since the Unity MCP is not connected. The same files and the same single commit as above.

## Rev 2 (Hit transition)

- Removed the legacy `Hit` -> `Idle` transition (exit time 1, duration 0, no conditions, fileID -74881292564830599) from `miso/Assets/_Project/Features/Player/John/Art/Animations/AC_Playable_John.controller`: `Hit` now has `m_Transitions: []` and the `AnimatorStateTransition` object is deleted. Done as a YAML edit (file is LF; line endings kept). Diff vs. before: exactly two hunks (the Hit transitions list and the removed 22-line object); no other `m_Transitions`, state or parameter changed. `AC_NPC_John.controller` not touched.
- Reason: the animator left `Hit` on its own into plain `Idle`, so `EntityAnimationHandler` never reached its end-of-clip `Stop()`, which plays the resolved idle (`Idle_Shield` while shielded).
- Handler check: in `EntityAnimationHandler.Update`, `if (normalizedTime >= 1 && !IsLooping)` calls `Stop()` (unless `_freezeOnEnd`). `Hit` is non-looping, so it now ends through that path like every other state. Not play-checked: needs the verifier to take a hit while shielded and confirm `Idle_Shield` afterwards.
- Unity: forced asset refresh, console has no errors. EditMode suite: 430/431 passed; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- Proposed commit: `AC_Playable_John.controller` alone (animation data fix).
