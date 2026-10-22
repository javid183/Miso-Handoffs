# Report: C5b, enemy animator transitions into Idle

Plan: plans/2026-10-21-quick-wins-a-tech.md (C5 commit-log note, follow-up C5b), decision D-140    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (8 transitions removed, 1 clip set to play once, 7 kept with reasons; not play-checked)

## Audit (step 1, before changes)

How the handler ends a state: `EntityAnimationHandler.HandleFrameAction` calls `Stop()` when `normalizedTime >= 1 && !IsLooping`; `Stop()` plays the data's `stopStateName` if set, else the idle data (idle speed spread, `IdlePhaseSequence` start phase, state variant). A `SimplePlay` has no `stopStateName`, so a state played that way returns to the idle data.

Callers found (live read of the prefabs through the editor, not just YAML):
- **Hit**: `UnitBase.prefab` HP `onValueDecreased` call [0] = `EntityAnimationHandler.SimplePlay("Hit")`. Every enemy unit prefab (Archer, Dark Claw, Black Claw, Shaman, Worm, Queen, Masher, Deev, Deevoted) keeps that call unchanged (their overrides start at call [2]).
- **Spawn**: `spawnAnimationData.stateName = Spawn` on Dark Claw (Black Claw inherits), Dark Shaman, Dark Worm, Deevoted; played by `Initialize(spawned: true)` and `PlaySpawnAnimation()` (`GUnit` spawn and revive). Archer, Masher, Queen, Deev have no spawn data.
- **JumpEnd / ChargeAttackEnd**: the Queen's ability [4] `Jump` has `stopStateName: JumpEnd`, ability [3] `ChargeAttack` has `stopStateName: ChargeAttackEnd`; `RuntimeAbility` completion calls `Stop()` / `NotifyStop()`, which `SimplePlay` the end state.
- No level sequence (`UnitAnimationSequence`), scene or asset plays Hit, Spawn, JumpEnd or ChargeAttackEnd by name. No state has StateMachineBehaviours; no Hit, Spawn or End clip has animation events. `BossGoblinQueen` only sets the `IsCharging` bool; no code waits on these state names (`IsPlaying` callers: `UnitAnimationSequence`, `JohnShieldRelay`, neither on enemies' Hit/Spawn).

All transitions below: exit time 1, has exit time, duration 0 (fixed), unless noted.

| Controller | Transition | Source entered by | Source motion loops? | Exit / conditions | Depends on it | Verdict |
|---|---|---|---|---|---|---|
| Dark Claw | Hit → Idle | handler, `SimplePlay("Hit")` (UnitBase HP event) | no (3 × `A_Enemy_DarkClaw_Hit_Side`, loop off) | exit 1, none | nothing | **REMOVE** |
| Dark Claw | Spawn → Idle | handler, `spawnAnimationData` | no (3 × `A_Enemy_DarkClaw_Spawn_Side`) | exit 1, none | nothing | **REMOVE** |
| Archer Goblin | Hit → Idle | handler, `SimplePlay("Hit")` | no (3 × `Hit animation`) | exit 1, none | nothing | **REMOVE** |
| Masher Goblin | Hit → Idle | handler, `SimplePlay("Hit")` | no (3 × `A_Enemy_MasherGoblin_Hit_Side`) | exit 1, none | nothing | **REMOVE** |
| Dark Worm | Hit → Idle | handler, `SimplePlay("Hit")` | no (3 × `A_Enemy_DarkWorm_Hit_Side`) | exit 1, none | nothing | **REMOVE** |
| Dark Worm | Spawn → Idle | handler, `spawnAnimationData` | **yes** (3 × `A_Enemy_DarkWorm_Spawn_Side`, loop on; clip used only by this controller) | exit 1, none | nothing; without the transition a looping spawn never ends | **REMOVE** + set the Spawn clip to play once |
| Dark Shaman | Hit → Idle | handler, `SimplePlay("Hit")` | no (3 × `A_Enemy_DarkShaman_Hit_Side`) | exit 1, none | nothing | **REMOVE** |
| Dark Shaman | Spawn → Idle | handler, `spawnAnimationData` | no (3 × `A_Enemy_DarkShaman_Spawn_Side`) | exit 1, none | nothing | **REMOVE** |
| Goblin Queen | Hit → Idle | handler, `SimplePlay("Hit")` | no | exit 1, **condition `IsCharging` false** | paired with Hit → ChargeAttackLoop (`IsCharging` true, no exit time); `BossGoblinQueen.Charge/ChargeEnd` drive the bool | **KEEP**: bool-conditioned, part of the charge logic |
| Goblin Queen | Hit → ChargeAttackLoop | handler, `SimplePlay("Hit")` | no | no exit time, `IsCharging` true | the charge resumes after a hit | **KEEP** (not into Idle; conditioned) |
| Goblin Queen | JumpEnd → Idle | handler, ability `stopStateName` | no (`A_Enemy_GoblinQueen_Jump-End`) | exit 1, none | last link of the Jump → JumpLoop → JumpEnd end-state sequence | **KEEP**: D-140 keeps end-state sequences (see Risks: it would technically work without it) |
| Goblin Queen | ChargeAttackEnd → Idle | handler, ability `stopStateName` | no (`A_Enemy_GoblinQueen_ChargeAttack-End`) | exit 1, none | last link of the ChargeAttack → ChargeAttackLoop → ChargeAttackEnd end-state sequence | **KEEP**: same reason |
| Goblin Queen | Jump → JumpLoop, ChargeAttack → ChargeAttackLoop | handler (ability `stateName`) | no (start clips) | exit 1, none | chains into the looping middle state | **KEEP** (chains, not into Idle) |
| Mountain Deev | Default → Idle | animator default state (`Default`, no motion) | n/a (no motion) | exit 1, none | the animator's entry before the handler's first play | **KEEP**: not played by the handler |
| Mountain Deev | Idle → Idle Look, Idle Look → Idle | Idle by the handler; Idle Look only by the animator chain | yes (both loop) | exit 1, none | the Deev's idle look cycle | **KEEP**: chain loop, out of scope |

Not unit body controllers (left alone): `AC_Enemy_ArcherGoblin_ShootingArrow` (projectile), `AC_Enemy_DarkShaman_ShootingProjectile` (projectile), `AC_MasherGoblin_Attack` (attack effect; also used by the Queen's AOE variant), `AC_Enemy_MountainDeev_VFX` (VFX child of the Deev). `AC_Deevoted` has no transitions at all.

## What changed

Applied in the open editor through the Unity MCP (`AnimatorState.RemoveTransition`, `AnimationUtility.SetAnimationClipSettings`, `AssetDatabase.SaveAssets`); editor was not in Play mode (checked first).

- `miso/Assets/_Project/Features/Enemy/Dark Claw/Art/Animations/AC_Enemy_DarkClaw.controller`: Hit → Idle and Spawn → Idle removed (both `m_Transitions` now `[]`, both `AnimatorStateTransition` objects deleted). Black Claw uses this controller.
- `miso/Assets/_Project/Features/Enemy/Archer Goblin/Art/Animations/AC_Enemy_ArcherGoblin.controller`: Hit → Idle removed.
- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Art/Animations/AC_Enemy_MasherGoblin.controller`: Hit → Idle removed.
- `miso/Assets/_Project/Features/Enemy/Dark Worm/Art/AC_Enemy_DarkWorm.controller`: Hit → Idle and Spawn → Idle removed.
- `miso/Assets/_Project/Features/Enemy/Dark Worm/Art/A_Enemy_DarkWorm_Spawn_Side.anim`: `m_LoopTime: 1` → `0` (plays once, so the handler ends the spawn).
- `miso/Assets/_Project/Features/Enemy/Dark Shaman/Art/Animations/AC_Enemy_DarkShaman.controller`: Hit → Idle and Spawn → Idle removed.
- `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EnemyIdleReturnTransitionTests.cs` (+ `.meta`): new EditMode tests.

Diff check: `git diff` shows only the removed transition blocks, the `m_Transitions: []` lines and the one `m_LoopTime` line (9 insertions, 193 deletions over 6 files). No resave noise; nothing to restore. Line endings kept (LF, no BOM, as before). Queen, Deev, Deevoted and the four non-body controllers untouched. `Packages/*` and `ProjectSettings/*` were already modified before this task (not mine).

## Acceptance criteria

- [x] Audit table written before any change: above.
- [x] Only REMOVE rows applied; source states with a looping clip set to play once (Dark Worm Spawn only): diff above; the other Hit/Spawn clips already played once.
- [x] KEEP rows, conditioned transitions, chains and the Deev idle look untouched: diff + tests.
- [x] EditMode test guards both directions: `MISO.Core.Animation.EditorTests.EnemyIdleReturnTransitionTests` 26/26 passed (8 no-transition cases, 8 play-once cases, 9 kept-transition cases, 1 Queen `IsCharging` condition check).
- [x] Compile clean (no console errors after refresh; only pre-existing warnings). Full EditMode suite 517/518; the one failure is the known red `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`.
- [ ] Play check (each enemy returns to a spread idle after a hit and a spawn; Queen and Deev unchanged): needs the verifier / THJ.

## Save reset

no

## Decisions I made

- Queen JumpEnd → Idle and ChargeAttackEnd → Idle kept (Tier 2): they meet D-140's conditions 1 to 3 (played by name through the ability's `stopStateName`, clips play once, the handler's end path would return to idle), but D-140 lists end-state sequences as a keep reason, so I kept them rather than widen the change. See Risks.
- Test file placed next to the other handler tests (`Core/Animation/EntityAnimation/Editor/`), namespace `MISO.Core.Animation.EditorTests`, rather than a new folder under `Features/Enemy`.

## Needs THJ

none (optional follow-up under Risks)

## Docs to update

- `build-log.md`, plan commit log (C5b line): transitions removed per the audit; Queen and Deev kept.
- `tech/combat-architecture.md` (idle variance): enemy hit and spawn now return to the idle through the handler; the Queen's hit and end states and the Deev's idle look still return through the animator, at authored speed and frame 0.

## Risks and loose ends

- The Queen still returns to Idle through the animator after a hit (not charging), JumpEnd and ChargeAttackEnd, so she gets no idle speed spread or start phase there. She is a single boss, so lockstep with others is unlikely to show. If wanted: JumpEnd → Idle and ChargeAttackEnd → Idle could be removed on their own (handler path verified in code); Hit → Idle needs care because of the paired `IsCharging` transition to ChargeAttackLoop.
- Pre-existing, not changed: `AC_Enemy_MountainDeev` has no `Hit` state, but `UnitBase`'s HP event still calls `SimplePlay("Hit")` on the Deev, so the animator logs/ignores an unknown state and the handler waits until the next play. Its idle keeps running, so nothing visible breaks.
- Pre-existing, not changed: the Queen's Hit → ChargeAttackLoop has no exit time, so a hit while charging cuts straight to the loop.
- Black Claw relies on the Dark Claw controller, so it gets the change too (intended).
- Timing: without the transition the last Hit/Spawn frame holds until the handler's next `Update` sees `normalizedTime >= 1` (at most one frame), then the idle plays with the spread.

## Proposed commits

1. `fix(animation): enemy hits and spawns return to the idle through the animation handler, so the idle keeps its speed spread and start phase`: (plain, data + test)
   - `miso/Assets/_Project/Features/Enemy/Dark Claw/Art/Animations/AC_Enemy_DarkClaw.controller`
   - `miso/Assets/_Project/Features/Enemy/Archer Goblin/Art/Animations/AC_Enemy_ArcherGoblin.controller`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Art/Animations/AC_Enemy_MasherGoblin.controller`
   - `miso/Assets/_Project/Features/Enemy/Dark Worm/Art/AC_Enemy_DarkWorm.controller`
   - `miso/Assets/_Project/Features/Enemy/Dark Worm/Art/A_Enemy_DarkWorm_Spawn_Side.anim`
   - `miso/Assets/_Project/Features/Enemy/Dark Shaman/Art/Animations/AC_Enemy_DarkShaman.controller`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EnemyIdleReturnTransitionTests.cs`
   - `miso/Assets/_Project/Core/Animation/EntityAnimation/Editor/EnemyIdleReturnTransitionTests.cs.meta`

   One commit: the worm's clip change only matters together with its removed Spawn transition, and the test asserts all of it. Do not stage `Packages/*` or `ProjectSettings/*`.

## Other branches

none (`thj/home-test` gets it when it takes `main`)

## How to see it

1. Open a level with several enemies of one type (e.g. a group of Dark Claws or Goblins). Hit two or three of them in a row and watch them after the hit: each returns to its idle at a slightly different speed and phase, not all on frame 0 together.
2. Do the same for an Archer, a Masher, a Dark Worm and a Dark Shaman: the hit plays once, then the idle. Nothing sticks on the last hit frame.
3. Spawns: let a Dark Shaman summon (or a Dark Worm split) and watch the new unit's Spawn play once and settle into a spread idle. The Dark Worm's spawn no longer loops.
4. Goblin Queen: watch her jump (Jump, loop, land) and charge (start, loop, end): unchanged, and she still returns to her idle after each. Hit her while she is charging and while not: same as before.
5. Mountain Deev: its idle still alternates with the idle look as before.
