# Report: Dark Shaman heal, C2 (heal pop-up and next-targets filter)

Plan: `plans/2026-10-23-dark-shaman-heal-tech.md` (C2). Branch `thj/quick-wins`. Nothing staged or committed. Editor was open (`Temp\` exists); no Play mode entered.

## Changed files (all LF, no BOM, as their neighbours)

| File | Lines | Change |
|---|---|---|
| `Core/FX/Runtime/DamageNumberTrigger.cs` | 20 | `class` -> `partial class` (one word) |
| `Core/FX/Runtime/DamageNumberTrigger.Heal.cs` (+meta) | 114 | new: heal tracking and "+N" pop-up, serialized `healColor` (green default) |
| `Core/FX/Runtime/HealPopRules.cs` (+meta) | 17 | new: pure rules (`GainedHp`, `PopAmount`, `Format`) |
| `Core/FX/Editor/HealPopRulesTests.cs` (+meta) | 50 | new: 6 EditMode tests |
| `Features/UI/Panels/Scripts/FutureTargetsPanelUI.cs` | 84 (+20) | filter to hostile targets before showing |
| `Features/UI/Panels/Scripts/FutureTargetsRules.cs` (+meta) | 24 | new: pure filter (`IsListed`, `Filter`) |
| `Features/UI/Panels/Scripts/Editor/FutureTargetsRulesTests.cs` (+meta) | 40 | new: 4 EditMode tests |

No core-system file touched (not `RuntimeAAttribute`, `AEffect*`, `GUnit`, `AIUnitBrain`, `CombatLevelRunHandler`, prefabs or scenes). No statics added, so no `PlayModeStaticReset` hook.

## HP-change path (traced)

- Damage: `AEffectAttributeModifier` -> `AAttributeSet.ApplyModifiers` -> `RuntimeAAttributeBase.ApplyModifiers` -> `RuntimeAAttribute.SetValue`. `SetValue` fires `onValueChanged` / `onValueIncreased` / `onValueDecreased` with `abs(currentValue - newValue)`, where `newValue` is the change-rounded value **before** the min/max clamp. So the event amount is the unclamped difference (a 10 heal at 3 below max reports 10; at full HP it still fires "increased" with 10).
- `ShowDamage` has no C# caller: `UnitBase.prefab` wires the health entry's `onValueDecreased` UnityEvent to `DamageNumberTrigger.ShowDamage`. Increases were never wired, and I did not change that wiring (damage numbers are untouched).
- Heal pop-up design, which uses the real gain and not the event amount: each unit's `DamageNumberTrigger` keeps the health value it last saw. On `onValueChanged` it adds `Value - lastSeen` (never negative, read after the clamp) to a pending gain. When the bus event `onAbilityEffectPerformedOn(ability, entity)` names this unit (raised by `AEffectCompound` right after an ability's effects are applied, same frame), the pending gain is rounded (`RoundToInt`, same as `PopDamage`) and shown with `DamageNumberManager.ShowText` as a green "+N" at the trigger's start position. Nothing shows if the rounded gain is below 1. LateUpdate re-reads the baseline and clears any unclaimed pending gain.
- The trigger follows the unit's current health attribute (rebuilt on each unit init) the same way `UnitMiniHealthBar` does, and re-subscribes if `GlobalEventBus.Instance` changes.

## Sources

Pop (any heal applied by an ability or item effect to a unit that is among the effect's targets):
- Dark Shaman heal (`DarkShaman_Ability_Heal`): yes. Healing at full HP or a capped gain below 1: no number.
- Health potion (`Bergsons_Ability_HealthPotion`): yes by mechanism, when the potion targets the user (an effect on a target).
- Dom heal, Linda–Toba duo arrow heals (Healing Marks, each Bergson in the line): yes by mechanism (compound effect on each target).
- Any other attribute-modifier effect with a positive `Specs_Health` change on a target. Revive-by-heal (`GUnit.OnHeal`) pops the same way if the dead unit's trigger is active (a deactivated dead unit's trigger is disabled, so possibly not; not verified).
- Mechanism-based, not play-verified.

Do not pop:
- Recurring/regen ticks (`PhaseTick` -> `ApplyModifiers` runs outside any ability's effect apply, so the pending gain is dropped at end of frame).
- Level-start HP restore (`LevelStartFPFiller`) and safe-room heal (`SafeRoomFunction`): same, no effect-performed report.
- `Resurrect()` (restores no HP through `SetValue`), silent sets (`SetValue(..., true)`: no event), max-HP / bounds changes (no event; baseline is re-read), cheat heal, `AbilityPreset.selfAttributeModifiers` and passive self-modifiers (owner is not reported as an effect target).
- Edge cases that can't be told apart: a regen tick landing in the same frame as an ability effect on that same unit would be added to that ability's number; a heal given through `selfAttributeModifiers` (owner self-heal as a cost-side modifier) won't pop. Neither is known to exist in current content.

Damage numbers: `ShowDamage`, `onValueDecreased` wiring and the manager are unchanged.

## Next-targets filter

`FutureTargetsPanelUI.Set` now lists only units for which `CombatLevel.Instance.GetFactionsRelation(planner.Faction, target.Faction) == FactionsRelationType.Enemy`. The planner is `GetComponentInParent<GUnit>()` of the panel (the panel sits in the unit prefab). If there is no planner, no `CombatLevel`, or a unit has no faction, nothing is filtered (the old behaviour). An all-ally list hides the panel. `GUnit.SetFutureTargets` and `AIUnitBrain.PredictNextTargets` are unchanged. Applies to both the predicted-targets and the memorable-attack list.

## Compile and tests

Recompiled in the open editor, console clean of errors. EditMode: 619 run, 618 pass, 1 fail = `Baseline_MatchesCurrentAI` (the known red; 10 new tests all pass).

## Proposed commits

1. `feat(fx): green heal pop-up for HP gained from abilities and items` : `DamageNumberTrigger.cs`, `DamageNumberTrigger.Heal.cs` (+meta), `HealPopRules.cs` (+meta), `HealPopRulesTests.cs` (+meta).
2. `feat(ui): the next-targets panel lists only hostile units` : `FutureTargetsPanelUI.cs`, `FutureTargetsRules.cs` (+meta), `FutureTargetsRulesTests.cs` (+meta).

## How THJ can see it

1. Shaman heal near full HP: a Claw at 70% HP healed for 10 shows a green "+N" over it (N = real HP gained). A Claw 3 HP below max shows "+3", not "+10"; at full HP, no number.
2. Potion: use a health potion on a hurt Bergson: green "+N", capped at missing HP.
3. Healing Marks: Linda–Toba duo arrow: each healed Bergson in the line shows its own "+N".
4. Should not pop: wait for any regen/HoT tick if one exists, start a level with the level-start heal on, or use a safe room: HP rises, no number. Damage still shows the normal numbers.
5. Next targets: with a Shaman about to heal a Claw, hover/select the Shaman: the panel lists only player units; the healed Claw is not listed.

## Risks and loose ends

- Heal numbers rely on `onAbilityEffectPerformedOn`; any heal path that doesn't go through an `AEffectCompound` with a `RuntimeAbility` context won't pop.
- The pending-gain window is one frame; fine with current content (see edge cases above).
- Pop colour is the new serialized `healColor` on `DamageNumberTrigger` (prefab default is used; not overridden anywhere).

## Review fixes

1. **Claim source corrected.** The earlier text said the claim always comes from `AEffectCompound` in the same call. Only compound heals (Linda–Toba arrow) work that way. The Shaman heal, the potion and Dom's heal use a bare `AEffectAttributeModifier`, so their `onAbilityEffectPerformedOn` comes from `RuntimeAbility.OnCompletionShared` (`RuntimeAbility.cs:316-318`), only for presets with `actualTargets` on, and after `AbilityPreset.Activate` finishes (`AbilityPreset.cs:368-404`). The comment in `DamageNumberTrigger.Heal.cs` now names both raisers and the condition.
   - **Risk:** the pop-up works only if the completion report arrives in the same frame as the heal: `minimumDuration` and `waitTimeAfterCompletion` at 0 or less, no effect still in progress, and no frame wait in between. If a heal ability has a wait or a longer animation after the effect, the gain is dropped and nothing pops. Not play-verified for the Shaman heal, the potion or Dom's heal; check `actualTargets` and the waits on those presets first if one doesn't pop.
   - **Proposal (not built):** keep an unclaimed gain until the ability completes, for example by listening to `abilityPerformed` and claiming for the ability's targets, and clear it at the next ability start instead of at end of frame. That would pop regardless of waits. The cost is a wider window in which a regen tick could be mis-claimed.
2. **Tracker extracted.** `Core/FX/Runtime/HealPopTracker.cs` (+meta, 36 lines) is a plain class with `Reset`, `OnHealthReading`, `Claim` and `EndFrame`. `DamageNumberTrigger.Heal.cs` uses it and no longer holds pending-gain fields. `Core/FX/Editor/HealPopTrackerTests.cs` (+meta, 6 tests) covers damage then heal, heal at the cap, heal at full HP, unclaimed gain then end of frame then claim giving 0, two gains then one claim, and a silent change before end of frame. The optional next-targets fallback move was not done.
   - New commit unit: add these two files to commit 1.

Compile clean. EditMode: 625 run, 624 pass, 1 fail. The failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, the known red. The console shows its report, and the test-job output didn't list names, so I identified it from the AI report.

## No +N in play: cause and fix

**Cause.** The heal ability presets (`DarkShaman_Ability_Heal`, `Bergsons_Ability_HealthPotion`, `Dom_Ability_Heal_Enemy`) use `activationMode: 2` (event-based animated). Their effect lands on an animation event, and the ability's completion, which raises `onAbilityEffectPerformedOn` for the bare-modifier heals, comes many frames later. My end-of-frame drop (needed for the regen and restore exclusions) therefore discarded the gain before the claim could happen. I found this by reading the presets and `RuntimeAbility.Activate`; I could not confirm it in play. This is the risk the earlier review fix already warned about, and the case I proposed a fix for. Checked and fine: the trigger is on the `UnitBase.prefab` root object with `GUnit`, enabled; it binds the health attribute and the bus in `LateUpdate`; `DamageNumberManager.Instance` exists in the combat container scene; the colour has alpha 1. Sorting and position under the bar are not checked.

**Fix.**
- New `HealPopWindow` (`Core/FX/Runtime/HealPopWindow.cs`, plain class, no statics) tracks which abilities are running: `abilityActivationStarted` opens, `abilityPerformed` closes, and `turnStarted` and `turnEnded` clear it as a safety net.
- `DamageNumberTrigger.Heal.cs` pops a gain at once when it lands while a window is open. Activation start is raised just before the effect is applied, so the pop shows at the heal frame, with the real capped gain from the tracker.
- The `onAbilityEffectPerformedOn` claim stays as a fallback for abilities that never raise the activation start.
- Outside any running ability the gain is still dropped at the end of the frame, so these are still excluded: regen and HoT ticks, level-start restore, safe room, resurrect, silent sets and max-HP changes. Damage numbers are unchanged.
- Side effect: any HP gain that lands while an ability runs pops, including a passive's self-heal triggered by that ability, which is acceptable.
- Not covered: abilities that raise neither the activation start nor the effect report, such as some faction-role abilities, will not pop. The Linda–Toba duo's path is not checked.

**Files.** Added `Core/FX/Runtime/HealPopWindow.cs` (+meta) and `Core/FX/Editor/HealPopWindowTests.cs` (+meta, 5 tests, including a gain outside the window being dropped and one inside it popping at once). Edited `Core/FX/Runtime/DamageNumberTrigger.Heal.cs`. Add these to commit 1.

**Checks.** Not in Play mode (confirmed before compiling). Compile clean. EditMode: 654 run, 653 pass, 1 fail = `Baseline_MatchesCurrentAI` (known red). No diagnostic logs were added.

**To check in play.** Shaman heal on a hurt Claw: green "+N" at the heal frame. Then confirm a turn-start regen or level-start restore shows no number.
