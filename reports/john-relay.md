# Report: John's shield relay, any phase and area attacks

Plan: plans/2026-10-20-john-relay-area-tech.md    Agent: miso-implementer    Branch: masher-tweak
Outcome: done. Every chunk compiles and EditMode is green except the known red. The in-game criteria need the play check.

Paths are under `miso/Assets/_Project/`.

## What changed

### J-A, trigger fixes (D-119): committed as `9ec1c4c29`

- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs`: the answer now raises `abilityStarted` inside its `onStart`, after `RuntimeAbility.Activate` has recorded the action and before `abilityActivationStarted`. This is the same order as `FactionControllerBase`. The `counterCanProvokeFamilyRoles` gate is kept.
- `Features/Player/John/Scripts/JohnFactionRoleHandler.cs`, as committed in J-A:
  - The trigger is `obj as RuntimeAbility`.
  - Its owner must be John's enemy (the phase no longer matters), and it must be in progress.
  - John must not be a primary target: not as a unit, not by his cell, and not inside a bundle.
  - `PrepareTargets` and `Activate` use that trigger instead of `ActionsInProgress[0]`.

### J-B, area relay (D-120, D-123): core

- `Core/Systems/AbilitySystem/Abilities/Runtime/FamilyRoleRelay.cs` (+ `.meta`), new. BOM and LF, like `FactionRoleProvocationSuppression.cs`. It holds three things:
  - `FamilyRoleRelay`, a static registry keyed by the attacking `RuntimeAbility`:
    - `Register`, which also prunes stale records;
    - `Clear` and `TryGetActive`, which drop a record once it is no longer live;
    - `Apply(attack, targets)`, which returns the same array when the ability has no record;
    - `IsAreaAttack` (a Surrounding preset, or a Surrounding compound anywhere in the effect chain, spawners included);
    - `ResetPlayModeState`.
  - `FamilyRoleRelayRecord`: John, the covered allies, the "John already hit" flag, and a liveness check. The check is true while the action's `ActionLogEntry` is in progress and John is alive.
  - `FamilyRoleRelayRules`, pure and generic:
    - `SelectCovered`, which builds the covered set;
    - `Filter`, the swap-once rule;
    - and, from J-A review note 2, the trigger rules `ShouldRelay`, `TargetsInclude` and `Flatten`.
- `Core/Systems/AbilitySystem/Effects/Runtime/AEffectCompound.cs`: 5 lines in `ApplyUnguarded`, right after its `GetTargets` call. When `statCtx` is a `RuntimeAbility`, the targets pass through `FamilyRoleRelay.Apply`. BOM and LF kept.
- `Core/Managers/PlayModeStaticReset.cs`: one line, `FamilyRoleRelay.ResetPlayModeState();`. LF kept, matching HEAD.
- `Features/Player/John/Scripts/JohnFactionRoleHandler.cs` (no BOM, LF kept):
  - `CheckTriggerConditions` uses `FamilyRoleRelayRules.ShouldRelay` and `TargetsInclude`.
  - `PrepareTargets` builds the covered set from the primary-target units plus, for an area attack, the occupants of `AbilityPreset.ComputeAffectedCells(trigger, owner, cell)`. It keeps only allies in John's zone that match `targetSelectTagQuery`, and never John.
  - `Activate`:
    - checks once whether the trigger is still in progress, and only then applies the reduction (J-A review note 1) and relays;
    - for an area attack, registers the record (`RelayArea`) and clears it through `OnCompletionPerRun`; the area is not retargeted;
    - otherwise, swaps the covered targets for John as before (`RetargetToJohn`), now including covered allies given as a `GridCell`.
- `Core/Systems/AbilitySystem/Abilities/Editor/FamilyRoleRelayTests.cs` (+ `.meta`), new: 24 tests, covering covered-set selection, the swap-once rule, the trigger rules and the registry lifecycle.

### J2, reduction once per action (D-124): test only

- Finding: the reduction never stacked.
  - `AAttributeSetBase.ApplyDurationModifiers` looks for an existing entry with the same mode, the same attribute and the same modifier ids.
  - John's `receivedDamageModifier` has the unique id `JFR_DR` (`Unit_John.prefab`).
  - So a second relay only resets `RemainingTurns` to 1. It adds nothing to `Stat_DR`.
  - The entry expires at the next `PhaseStart` tick of John's stat set, which is the start of the player phase (`GUnit.PhaseTick`).
- `Core/Systems/StatsResourcesSystem/Editor/DurationModifierRefreshTests.cs` (+ `.meta`), new: 3 tests that pin this behaviour, built in memory. No game code changes.

### J3, John's QTE doesn't release another action's flow (D-125): core

`Core/Interactions/Runtime/PlayerController.cs`, `ActivateFactionRole` (no BOM, LF kept):
- **The in-progress flag.** The role remembers `PhaseData.IsInProgress` from before it started. When it ends, it clears the flag only if the flag was clear before, so it no longer forces false.
- **The End Turn refresh.** It now waits (`ExecutionUtils.WaitWhile`) while `OtherFactionActionInProgress()` is true, so End Turn isn't refreshed in the middle of a Masher answer.
- **Time scale.** The two `Time.timeScale = 1` calls are now `RestoreTimeScale()`:
  - normal speed when no reactive interrupt is active;
  - otherwise the reactive slow motion: the speed from before the role, if the interrupt was already on and that speed was above 0, or else `reactiveInterruptTimeScale`.

## Acceptance criteria

- [ ] **John relays a Masher answer on the player's turn and on the enemy turn, when its target is an ally in his zone.** Play check.
  - Code: the J-A `onStart` order, plus `CheckTriggerConditions`.
  - Tests: `ShouldRelay_*`, `TargetsInclude_*`.
- [ ] **Masher or Queen slam on an ally in John's zone.** Play check. Expected:
  - John takes one hit, at his reduction;
  - covered allies in his zone take nothing;
  - allies outside his zone are hit;
  - John's neighbours are not hit because of the relay.
  - Code: `RelayArea` and the `AEffectCompound.ApplyUnguarded` hook.
  - Tests: `SelectCovered_*`, `Filter_*`, `Registry_*`.
- [ ] **John is the main target.** Play check. He takes his normal damage and nobody is relayed.
  - Code: `ShouldRelay`'s primary-target check.
  - Tests: `ShouldRelay_JohnIsPrimaryTarget_No`, `TargetsInclude_*`.
- [ ] **Single-target attacks relay as today.** Play check.
  - Code: `RetargetToJohn`, the same swap; cell targets are now handled too.
- [x] **Two relays in one phase don't stack the reduction.** Already true in the attribute set. Tests: `DurationModifierRefreshTests` (3).
- [x] **EditMode green except the known red.** Unity MCP, Run All after each chunk:
  - J-A: 365 tests, 364 passed.
  - J-B core parts: 379, 378 passed.
  - J3: 379, 378 passed.
  - J-B complete: 389, 388 passed.
  - J2: 392, 391 passed.

  The only failure each time was `AIRegressionTest.Baseline_MatchesCurrentAI`, with CHECKS 706 and FAILURES 35, unchanged. The console showed no `error CS` after each refresh; the warnings were all there before.
- [ ] **J3: input and End Turn stay locked while a Masher answer runs during John's QTE.** Play check (item 22 area of the Masher play check). Code only.

## Save reset

No.

## Decisions I made

- **The hook is in `ApplyUnguarded`, not inside public `GetTargets`.** The behaviour is the same. The damage, push and transporter previews also call `GetTargets`, and they would use up the record's one hit. The coordinator accepted this.
- **The area units are the union of `ComputeAffectedCells` over every primary target's cell**, not only `Targets[0]`. With one target this is the same as the plan. A Self or Surrounding preset with no targets resolves once around the attacker.
- **The record stops applying on its own** when the action's log entry completes or John dies, as well as through `Clear` from `OnCompletionPerRun`. `UnitsCooperationHandler.cs:671` assigns `OnCompletionPerRun =` for one Duo ability and could overwrite the clear, but that is a player ability, never an attack John relays.
- **Natural hits on John always pass.** John's natural inclusion sets the "hit" flag, so no swap follows it. If a later compound of the same action reaches John naturally again (for example, a charge passing over him), it still hits him, because he was really in its path.
- **Single-target retarget with a cell target:** when the dropped covered target was a `GridCell`, John is added as his cell, so the target keeps its kind. Before, a cell target wasn't dropped at all.
- **When the trigger has ended by the time `Activate` runs, John applies no reduction and relays nothing** (review note 1). The shield FX and his `abilityStarted` still play, as before.
- **The J3 "restore" clears the flag only when the role set it.** It does not write back the old `true`, which could get stuck if its owner had cleared it during the QTE.
- **J2 needed no game code.** I added tests instead of a redundant guard.
- **`FamilyRoleRelay.ResetPlayModeState` is `public`**, so the EditMode tests (in `Assembly-CSharp-Editor`) can call it.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md`, Family Roles row: add `FamilyRoleRelay`, a static registry with its record and pure rules, reset in `PlayModeStaticReset`, read by `AEffectCompound.ApplyUnguarded`. Effects row: `AEffectCompound` filters its targets through it.
- `tech/core-systems.md`, Faction controllers row: John's role QTE in `PlayerController` now keeps the previous in-progress flag, delays the End Turn refresh while another faction acts, and restores the reactive time scale.
- `tech/combat-architecture.md`: how John's relay works, single-target versus area.
- `build-log.md` and the plan's commit log (coordinator).

## Risks and loose ends

- **One hit per action, across all compounds.** If an area attack has several compounds that each reach covered allies (say, damage, then a stun), John takes only the first compound that swaps. The later ones skip the covered allies, so John gets no stun. The Masher and the Queen have a single damage compound.
- **Effects applied after the action completes** (a delayed hazard, a spawned entity that activates later) aren't relayed, because the record is no longer live. The Masher's AOE applies synchronously when it is plugged (`GridCell.PlugEntity` with `ActivateOnTile`), so it is relayed. I didn't audit the Goblin Queen's strike asset: check it in play.
- **Covered allies come from the area preview.** `ComputeAffectedCells` must match the runtime area. The plan's finding 7 confirms this for the Masher. Shape rotation held while targeting is captured differently at runtime, which could matter for a rotated enemy shape.
- **Single-target path:** targets given as a `GameEntityBundle` aren't unpacked by `RetargetToJohn` (same as before).
- **Instant and InstantAnimated attacks** apply before John's QTE ends, so neither path can relay them. This is unchanged, and was noted in the J-A review.
- **End Turn during a Masher answer:** the button is already enabled by the answer's own `abilityStarted` refresh (`CombatLevelRunHandler.OnAbilityStart`, through `CanEndTurn`, which checks only the player's own flag). J3 doesn't fix that pre-existing path; the turn-switch hold still blocks the actual switch.
- `JohnFactionRoleHandler._isActive` is assigned but never read (a pre-existing warning).

## Proposed commits

**Superseded by "Revision 1 > Proposed commits (final)" below.**

Already in: **J-A** `9ec1c4c29` `fix(roles): John relays enemy attacks on either turn, including the Masher's answers`.

1. **J-B** `feat(roles): John takes an area attack once for every covered ally instead of moving the area onto himself` (**core**, risky). Depends on J-A.
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FamilyRoleRelay.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FamilyRoleRelay.cs.meta`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FamilyRoleRelayTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FamilyRoleRelayTests.cs.meta`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectCompound.cs`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnFactionRoleHandler.cs`

   These only work together: the hook and the reset need the registry, and John's handler uses the registry and rules.
2. **J2** `test(stats): a duration modifier applied twice with the same id refreshes instead of stacking` (plain, tests only). Independent.
   - `miso/Assets/_Project/Core/Systems/StatsResourcesSystem/Editor/DurationModifierRefreshTests.cs`
   - `miso/Assets/_Project/Core/Systems/StatsResourcesSystem/Editor/DurationModifierRefreshTests.cs.meta`
3. **J3** `fix(input): a Family Role prompt no longer releases the player's flow or End Turn while another faction is acting` (**core**, own commit). Independent of J-B and J2.
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`

Order: J-B, J2, J3. J2 and J3 can go in any order. Leave `miso/Packages/*` and `miso/ProjectSettings/*` unstaged: they were already dirty and aren't part of this work.

## Other branches

`main` needs J-A, J-B and J3 when `masher-tweak` merges (D-119 and D-120 apply to every branch). `thj/home-test` needs them too, with the Masher work.

## How to see it

1. Test Runner > EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` is red. `FamilyRoleRelayTests` (24) and `DurationModifierRefreshTests` (3) are green.
2. Play a level with the Masher and John (`LevelE3-C1`). Stand Lucy next to the Masher, inside John's zone, with Linda beside her, also in his zone, and Mark next to her outside his zone.
3. Player's turn: hit the Masher with Lucy. When the Masher slams, John's prompt appears; press it. John takes one hit, with his reduction. Lucy and Linda take nothing. Mark is hit. Anyone standing next to John is not hit because of the relay.
4. Enemy turn: let the Masher slam Lucy by its own choice. Same result.
5. Put John next to the Masher, so that he is the slam's target. No prompt appears, John takes his normal hit, and the allies in the slam's area are hit normally.
6. A single-target enemy attack on an ally in John's zone (Archer Goblin): the arrow goes to John, as before.
7. With a Masher answer running on the player's turn, press John's prompt. While the answer is still running, you can't select units or abilities, and End Turn stays disabled until the answer finishes.
8. Goblin Queen strike near John (M4 or M10): John takes one hit, and the covered allies are spared.

## Revision 1 (review FIX; D-126, D-127, D-128)

Review: `reports/john-relay-review.md`. Applied the four should-fixes (D-128) and THJ's two rulings (D-126, D-127). No Play mode, no git writes, save not reset.

### Should-fixes (D-128)

1. **End Turn gated on other factions** (J3).
   - New `PlayerController.EndTurnAvailable()`: true when `CanEndTurn()` and no other faction's action is running.
   - While another faction's action runs, it returns false and schedules one deferred refresh (`ExecutionUtils.WaitWhile(OtherFactionActionInProgress)`), so the button can't stay disabled.
   - `CombatLevelUIManager.NotifyStateChange` uses it when the phase controller is the `PlayerController`. Every other controller still uses `CanEndTurn()`.
   - This covers the refresh after the answer's `abilityStarted` and the refresh at the end of John's role.
   - The turn-flow waits (`ForceEndTurnSafe`, `RequestEndTurnSafe`, `ResetCurrentPhase`) still use `CanEndTurn()`. Gating those could stall the automatic turn end, and the turn-switch hold already covers it.
   - Note: `CombatLevelUIManager.cs` is a core file that the plan didn't name. The change is 5 lines, and the coordinator decided it under D-128.
2. **Null guard.** Both `NotifyStateChange` calls (the role's clear, and the deferred End Turn refresh) go through `var ui = CombatLevelUIManager.Instance; if (ui) ...`.
3. **`IsAreaAttack` tests.** New `FamilyRoleRelayAreaTests.cs`. It covers:
   - a Surrounding preset;
   - a Targeted preset with a Targeted compound;
   - a Surrounding compound, directly and nested in another compound;
   - the transporter case (see D-126);
   - null or presetless abilities;
   - `ClearAll`.

   Presets and effects are built in memory with `CreateInstance`, and their private fields are set by reflection.
4. **Level end.**
   - New `FamilyRoleRelay.ClearAll()`.
   - The first `Register` in a level hooks `GlobalEventBus.Instance.levelEnded` once per bus, and that hook calls `ClearAll`.
   - `ResetPlayModeState` also forgets the hooked bus.

### D-126: the Queen's charge stays out of the area relay

- `HoldsArea` still doesn't look into transporters, so a charge is relayed as a single-target attack.
- **The rule:** a cell target is never dropped or replaced when the attack moves a unit to its target. New `FamilyRoleRelay.MovesToTarget(attack)` checks the effect chain (top-level effects, compounds, spawner contents) for:
  - an `AEffectTransporter`, `AEffectDashAttack`, `AEffectSwapper` or `AEffectCommand`;
  - any `IGhostDestinationProvider`.

  For those attacks, the cell target is the move destination. I chose effect types over target types because the same Cell target means "hit this tile" in a slam but "go here" in a charge, and only the effect chain tells the two apart.
- For such an attack, John keeps the cell, drops only covered **unit** targets, and is added as an extra target. That is exactly the pre-J-B behaviour.
- **What moved:** `RetargetToJohn` now calls a pure `FamilyRoleRelayRules.Retarget(targets, covered, occupantOf, john, johnCell, keepCellTargets)` with `keepCellTargets = MovesToTarget(trigger)`.
- **Tests** in `FamilyRoleRelayTests`:
  - a covered unit becomes John;
  - a covered cell becomes John's cell;
  - for a move attack, the destination cell is not rewritten and John is added;
  - for a move attack, a covered unit is still dropped;
  - John is added only once.

  In `FamilyRoleRelayAreaTests`, the transporter test is now `TargetedPreset_TransporterWithSurroundingCompound_IsNotArea_ChargesStayOut`. It asserts that a charge is intentionally not an area attack and that `MovesToTarget` is true for it. There are also two `MovesToTarget` tests: a plain attack (no), and a dash nested in a compound (yes).

### D-127: the reduction ends when the relayed attack completes

- New pure `Features/Player/John/Scripts/JohnRelayReductionHolds.cs` (+ `.meta`), a set of the relayed attacks still running:
  - `Hold(attack)`;
  - `Release(attack)`, which returns true when none are left;
  - attacks that are no longer active (aborted without a completion) are pruned on every `Hold` and `Release`.
- In `JohnFactionRoleHandler.Activate`, when relaying, the new `ApplyReductionUntilCompleted(trigger)`:
  - applies `JFR_DR` as before, so a second relay still only refreshes it (D-124);
  - holds the trigger;
  - adds to `trigger.OnCompletionPerRun` a step that releases it and, when no relayed attack is left, removes the reduction with `StatAttributes.TryRemoveModifier(JFR_DR)`.
- **Fallbacks:** an aborted attack is pruned at the next completion or relay. The modifier's own one-turn Temporary duration still ends it at the next player phase start at the latest.
- **Tests:**
  - `Features/Player/John/Editor/JohnRelayReductionHoldsTests.cs` (+ `.meta`), 6 tests: one relay; two overlapping relays, where only the last completion ends it; the same attack held twice; an aborted attack pruned at completion and at the next hold; release with nothing held.
  - `DurationModifierRefreshTests`: new `TryRemoveModifier_ById_EndsItBeforeItsDuration`.

### Line endings (correction to the coordinator's note)

`git ls-files --eol` shows `i/lf w/lf attr/text eol=lf` for every modified file:
- `PlayerController.cs`
- `PlayModeStaticReset.cs`
- `AEffectCompound.cs`
- `CombatLevelUIManager.cs`
- `JohnFactionRoleHandler.cs`

So they are LF in HEAD, in the index and in the working tree: `.gitattributes` forces `eol=lf`, and `core.autocrlf` is true. Every edit preserved each file's existing endings and BOM:
- BOM: `AEffectCompound.cs`, `CombatLevelUIManager.cs`, `FamilyRoleRelay.cs`, and both `FamilyRoleRelay*Tests.cs`;
- no BOM: the others.

The original report's "LF kept" is therefore accurate. The review's "CRLF" doesn't match the repository: please check before changing anything.

### Checks

- Unity MCP refresh and recompile after each step: no `error CS` in the console.
- Full EditMode suite:
  - after the should-fixes: 399 tests, 398 passed;
  - final run: **413 tests, 412 passed, 1 failed**.

  The failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, unchanged (CHECKS 706, FAILURES 35).

### Acceptance criteria changes

- **Two relays don't stack:** tests (`DurationModifierRefreshTests`, `JohnRelayReductionHoldsTests`). Still to play check (D-127): John's reduction is gone once the relayed attack has completed, for example on the next enemy hit in the same enemy turn.
- **Queen charge at an ally in John's zone:** play check (D-126). The Queen still charges to the ally's tile, and John is added as an extra target. The area relay doesn't apply to it.
- **End Turn:** play check. The button stays disabled for the whole Masher answer on the player's turn, then re-enables on its own.

### Proposed commits (final)

Already in: J-A `9ec1c4c29`.

`JohnFactionRoleHandler.cs` holds J-B and J2 changes in overlapping lines, so the two can't be split with `git add -p`.
- To stage J-B's version of that file, apply this patch to the index: `git apply --cached "C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\9e47f352-0971-417c-848d-a127a1c717c3\scratchpad\john-relay-jb-JohnFactionRoleHandler.patch"`. It was checked with `git apply --cached --check` against HEAD. It is HEAD plus everything except D-127, and builds without `JohnRelayReductionHolds`.
- Then J2 stages the working-tree file normally, which adds the D-127 hunks.
- If that's too fiddly, merge J-B and J2 into one commit.

1. **J-B** `feat(roles): John takes an area attack once for every covered ally instead of moving the area onto himself` (**core**, risky). Depends on J-A.
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FamilyRoleRelay.cs` (+ `.meta`)
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FamilyRoleRelayTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FamilyRoleRelayAreaTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectCompound.cs`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnFactionRoleHandler.cs`, **J-B version only** (the patch above)
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs` (comment only: a decision ID removed from the J-A line, see "ID cleanup")
2. **J2** `fix(roles): John's damage reduction ends when the attack he took for an ally completes` (plain; John's handler). Depends on J-B.
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnRelayReductionHolds.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/John/Editor/JohnRelayReductionHoldsTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Core/Systems/StatsResourcesSystem/Editor/DurationModifierRefreshTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnFactionRoleHandler.cs` (the rest: the D-127 hunks)
3. **J3** `fix(input): a Family Role prompt no longer releases the player's flow, and End Turn waits for other factions' actions` (**core**, own commit). Independent of J-B and J2.
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs`

Order: J-B, J2, J3 (J3 can go anywhere). Leave `miso/Packages/*` and `miso/ProjectSettings/*` unstaged.

### Docs to update (in addition to the list above)

- `tech/core-systems.md`, Combat UI manager row: `NotifyStateChange` asks `PlayerController.EndTurnAvailable()` for the player's End Turn.
- `tech/core-systems.md`, Family Roles row: `FamilyRoleRelay.MovesToTarget` and `ClearAll` (on level end).
- The GDD or character sheet for John: the reduction lasts until the relayed attack completes (D-127).

### New risks

- **`EndTurnAvailable` depends on a deferred refresh.** If ExecutionUtils' runner were stopped while a refresh waits (a level unload), `_endTurnRefreshWait` would stay set on that `PlayerController`. Controllers are per level, so this shouldn't carry over.
- **`MovesToTarget` lists effect types.** A new movement effect that neither is one of those types nor implements `IGhostDestinationProvider` would have its cell target rewritten for a covered ally.
- **`OnCompletionPerRun` can be overwritten.** `RuntimeAbility.PhaseTick` nulls it, and `UnitsCooperationHandler.cs:671` assigns it with `=` (a player Duo ability, never a relayed attack). Either would skip the early removal. The one-turn fallback still ends the reduction.

### ID cleanup (new house rule)

- I removed every decision and chunk ID I had added in this work from code comments and test-section headers, across J-A, J-B, J2 and J3. Each was replaced with the reason in plain words.
- That includes the J-A comments:
  - in `JohnFactionRoleHandler.cs` (J-B commit);
  - in `MasherGoblinFactionRoleHandler.Counter.cs` ("(John, D-119)" became "(John)"). That is a comment-only change to a file committed in J-A, listed under J-B.
- No test names had IDs. Pre-existing IDs in these files (`D-068`, `D-069`, `D-088`, `D-105` in `PlayerController.cs`; `D-092` to `D-117` in `Counter.cs`) were left for the separate cleanup pass.
- The J-B-only patch for John's handler was rebuilt after the cleanup and re-checked with `git apply --cached --check`.
