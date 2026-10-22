# Report: quick wins A, chunks C5 and C6

Plan: `plans/2026-10-21-quick-wins-a-tech.md` (C5 enemy idle desync, C6 Mark's sounds). Branch `thj/quick-wins`, nothing committed. Editor was open and not in Play mode; Play was never touched. Compiled clean; EditMode suite 490/491, the only red is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. No save reset needed.

---

## C5. Enemy idle desync

### What changed
- New static helper `IdlePhaseSequence` (`Core/Animation/EntityAnimation/Runtime/IdlePhaseSequence.cs`): `Next()` returns `frac(seed + i * 0.618034)`, seed random once per play session, `i` a static counter; pure `Phase(seed, i)`; pure `SpeedFactor(jitter, roll)`; `ResetPlayModeState()`.
- `EntityAnimationHandler.Play`: `Random.value` replaced by `IdlePhaseSequence.Next()` when `randomizeStartFrame` is on (the state-variant name resolution above it is untouched).
- `EntityAnimationHandler`: new `[SerializeField, Range(0, 0.5)] idleSpeedJitter` (default 0). `Awake` stores `_authoredAnimatorSpeed`; `Initialize` calls `ApplySpeedJitter()`, which rolls once per handler (guard `_speedJitterApplied`), sets `_defaultAnimatorSpeed = authored * factor` and `animator.speed`. Re-initialising does not stack; `Pause`/`Resume`/`Stop` restore the jittered speed (including the QTE pause, which goes through `Pause`/`Resume`).
- `PlayModeStaticReset.Reset()` calls `IdlePhaseSequence.ResetPlayModeState()` (plus `using MISO.Core.Animation;`).
- Data: the 8 enemy prefabs got `idleSpeedJitter: 0.07`; `randomizeStartFrame: 1` added to Masher, Goblin Queen, Dark Worm, Deevoted, Deev (Archer, Dark Claw, Dark Shaman already had it). Done as inserted `m_Modifications` entries, no resave. Verified by loading each prefab: all 8 plus Unit_BlackClaw (inherits) read rand=true, jitter=0.07; `UnitBase` and `Unit_John` read false / 0.
- Tests: `Core/Animation/EntityAnimation/Editor/IdlePhaseSequenceTests.cs` (9 cases, all pass): range [0,1), determinism, spread (min gap > 0.05 over 8 values), `Next` step is the golden step and reset restarts, jitter range and exact bounds, zero jitter = 1.

### Acceptance
- Phase comes from the golden-ratio sequence, static counter reset in `PlayModeStaticReset`: Pass (code + test).
- Jitter opt-in, default 0, in [1-j, 1+j], Pause/Resume restore it: Pass for range (test); the Pause/Resume/QTE path is by code reading only, needs play check.
- Enemy prefabs set, players and `UnitBase` unchanged: Pass (checked by loading).
- Visible desync of a group of enemies: Not run (play check).

### Decisions I made
- The helper lives in its own class rather than on `EntityAnimationData` (keeps the data class plain-serializable and the static in one place).
- Jitter scales the whole animator, so it also affects walk/attack clips of those units, not only the idle (the plan says "default animator speed"). If attacks should stay at exact speed, the jitter needs to apply per state instead; say so if wanted.
- The counter also advances whenever an enemy idle is re-played (after an attack, variant swap), so the phase on those replays differs from the first one; still evenly spread.
- Jitter range slider capped at 0.5.

### Proposed commit
`feat(animation): spread enemy idle phases and speeds so groups stop moving in lockstep`
Files (LF, BOM kept on edited files):
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/IdlePhaseSequence.cs` + `.meta`
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`
- `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/IdlePhaseSequenceTests.cs` + `.meta`
- Enemy prefabs: `Features/Enemy/{Archer Goblin/Prefabs/Unit_ArcherGoblin, Dark Claw/Prefabs/Unit_DarkClaw, Dark Shaman/Prefabs/Unit_DarkShaman, Masher Goblin/Prefabs/Unit_MasherGoblin, Goblin Queen/Prefab/Unit_GoblinQueen, Dark Worm/Prefabs/Unit_DarkWorm, Deevoted/Prefabs/Deevoted, Mountain Deev/Prefabs/Unit_Deev}.prefab`
(Could be split code / prefab data if preferred; they only work together.)

### Risks
- Statics: one new (`_seed`, `_index`, `_seeded`), reset hooked.
- Not a core system; AI does not read any of it.
- A unit whose `Pause` is called while already paused would store speed 0 as default (existing behaviour, untouched).

### How to see it
Start a level with several goblins or claws side by side. Their idles should start at visibly different frames and drift apart slowly (speeds 93% to 107%). Pause for a QTE and resume: speeds return. Players and John's shield idle look the same as before.

---

## C6. Mark's sounds (data only)

### What changed (`Features/Player/Mark/Prefabs/Unit_Mark.prefab`)
Final mapping:
- Hit (HP `onValueDecreased` PlaySFX): `A_SFX_Lucy_Hit` -> `A_SFX_John_Hit`.
- Cleanse (ability [4], `CleanseAbility.asset`): `A_SFX_Lucy_Dedication` -> `A_SFX_John_Dedication`. In `Unit_John.prefab` the slot whose preset is `CleanseAbility.asset` is ability [5] and it uses `A_SFX_John_Dedication` (slot [4], the APTransfer, also uses it; `A_SFX_Generic_Cleanse` is on slot [6], a different preset).
- Command (ability [3]): `A_SFX_Lucy_Decoy` -> `A_SFX_John_Attack`.
- Walk (ability [1]) event 0 `A_SFX_Lucy_FireShoot`: removed. John's Walk (slot [1], `John_Ability_Walk`) has no sound at its start, only a `PlayVFX` call; so the event was dropped and the three footsteps renumbered 1..3 -> 0..2 (their frames and `A_SFX_Generic_Footstep` kept). 9 override entries removed, 3 groups renamed; nothing else touched.

### Acceptance
- Hit plays John's hit sound: Not run (play check).
- Cleanse / Command / Walk mapping as above, no other Lucy sound ids left in `Unit_Mark.prefab` (grep: none): Pass.
- Prefab loads, only `Unit_Mark.prefab` changed: Pass.

### Finding (needs a decision, not fixed)
The `animationEvents` overrides for Mark's abilities [1], [3], [4] (and the matching John-side ones) look dead: they include `animationEvents.Array.size = 0` before the element overrides, and loading both the HEAD copy and the edited prefab in the editor shows `animationEvents` with 0 elements for abilities [1], [3], [4] (only [0] and [2] have 1). So the Lucy walk start sound, Command sound and Cleanse sound probably never played on Mark, and the footsteps override may not either. The hit sound (HP event) is a real override and does work. My edit follows the plan and is harmless, but the Cleanse/Command/Walk remap may have no audible effect until those events are set up properly. The same-looking pattern may exist on other units; I did not check.

### Decisions I made
- Walk event removed by renumbering (not left as an empty event) so the list stays clean.

### Proposed commit
`feat(audio): Mark uses John's hit, cleanse and command sounds as placeholders until his own exist`
Files: `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`.

### Risks
- See finding above. Diff is 5 insertions / 41 deletions of override entries.

### How to see it
Play a level with Mark: take a hit and listen for John's hit sound; use Cleanse, Command, Walk and check there is no Lucy sound (and see whether any sound plays at all, per the finding).

---

## Loose end
I created a scratch folder `miso/Assets/_Project/ZZ_TmpCheck/` (one prefab, `MarkHead.prefab`, a copy of the HEAD Mark prefab, plus Unity's `.meta`) to compare against HEAD. My `rm` was denied by the permission system and I did not work around it. It is untracked; please delete it (in Unity or the file system). It must not be committed.

---

## Rev 1 (THJ's answers)

Editor checked first: not in Play mode, never toggled. Compiled clean, no console errors; EditMode suite 492 tests (491 pass), the one failure being the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (new `StateSpeed_OnlyTheIdleIsJittered` passes).

### C5: jitter applies to the idle only
- `IdlePhaseSequence.StateSpeed(isIdle, authoredSpeed, idleFactor)` (pure, tested): idle gets authored x factor, every other state the authored speed.
- Handler: `Initialize` only rolls `_idleSpeedFactor` once (no stacking). `Play` sets `_defaultAnimatorSpeed` from `StateSpeed` for the state being played (idle = `idleAnimationData`, which also covers `Stop()` and variant replays; `SimplePlay` and ability states get the authored speed) and applies it to the animator unless paused.
- `Pause`/`Resume`: new `_paused` flag; `Pause` only captures the speed the first time (a second Pause no longer stores 0 as the default), `Resume` restores the speed of whatever is playing. This is a small change to existing behaviour, flagged.
- Other states, including attacks, keep their authored speed, so hit frames do not move.
- Not run: play check of a QTE pause/resume on an enemy mid-idle and mid-attack.

### C6: reverted to the hit sound only
`Unit_Mark.prefab` restored from HEAD (LF, as HEAD) and `A_SFX_Lucy_Hit` -> `A_SFX_John_Hit` re-applied. `git diff` vs HEAD is that single value line. The Walk/Command/Cleanse remap is dropped.

### Final proposed commits
1. `feat(animation): spread enemy idle phases and speeds so groups stop moving in lockstep`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/IdlePhaseSequence.cs` + `.meta`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/IdlePhaseSequenceTests.cs` + `.meta`
   - the 8 enemy prefabs under `miso/Assets/_Project/Features/Enemy/` (Unit_ArcherGoblin, Unit_DarkClaw, Unit_DarkShaman, Unit_MasherGoblin, Unit_GoblinQueen, Unit_DarkWorm, Deevoted, Unit_Deev)
2. `feat(audio): Mark uses John's hit sound as a placeholder until his own exists`
   - `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`

The earlier loose end (scratch folder) is resolved: THJ deleted it.
