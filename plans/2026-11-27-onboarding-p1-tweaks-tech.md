# Onboarding demo Phase 1 tweaks: Cyclone refund, free Duos, pouch, health potion, Mark's Command clip

Size: M    Tier: 3 (decided)    Assigned to: miso-implementer (one chunk at a time)
Branch: all (built on `main`)
Status: done (D-783 to D-792)

## Why

THJ's demo tweaks X-38, X-41, X-42, X-50, X-51, X-52 (plan `2026-11-22-onboarding-demo.md` chunks 1.10, 1.11, 1.12, 1.17, 1.18, 1.19). 1.13 and 1.16 are parked (D-784, D-788). Code findings from three Explore sweeps on 2026-11-27 are folded in below; the parked items' findings are in `reports/2026-11-27-act-twice-findings.md`.

## Goal

Ship the six small Phase 1 tweaks as three reviewable chunks, the core one first.

## Acceptance criteria

P1-1 Cyclone refund (1.11, D-786)
- [ ] A Cyclone that ends before its lifetime runs out (burst by a heavy: Masher, Goblin Queen; or any other non-fade end) sets Lucy's Cyclone cast cooldown to `min(current remaining, coolDown − lifeTurns)` (with today's data 4 − 3 = 1), clamped at 0 or more, so the cast is ready at the next family turn.
- [ ] A natural fade changes nothing (the cooldown runs from cast as today).
- [ ] The refund never raises a cooldown (if remaining is already lower, it stays).
- [ ] Level teardown / scene unload disposing the Cyclone does not throw and does not need to refund.
- [ ] `RuntimeAbility` gains one additive public method to set the remaining cooldown ticks (clamped 0..coolDown); no existing signature or behaviour changes.
- [ ] EditMode tests: burst on the enemy turn of the cast round → ready next family turn; burst mid-life → remaining 1; fade → unchanged; remaining already 0 → stays 0; the setter clamps.

P1-2 Data: free Duos, pouch, Mark's clip (1.17, 1.18, 1.10, 1.19; D-787, D-789)
- [ ] `Mark_Lucy_MARK_Duo_Ability.asset` and `Mark_Lucy_LUCY_Duo_Ability.asset` (`Resources/Abilities/Cooperation/Mark_Lucy/`) have `apConsumptionType: 0`; a Mark–Lucy Duo charges no AP; the activator still needs 1 AP left (no core change).
- [ ] New wiring test: every Duo entry in `Content/Controllers/PlayerController.prefab` (`UnitsCooperationHandler.entries`) has `allConsumeAP` false, and its trigger and partner presets are `apConsumptionType` 0 (Ineffective); both Divine Relic presets (`DR_Ability_HeavenlySword.asset`, `DR_Ability_BlackDespair.asset`) are 0.
- [ ] `Resources/Tutorials/Tutorial_Duo_Abilities.asset` no longer says Duos cost AP. Replace "Duos consume FP in addition to 1 AP from the activating Bergson." with a line in the page's own voice saying Duos cost FP from both Bergsons and no AP (keep "FP", the page's term). Report the exact before/after text.
- [ ] Every hero item entry (`abilityOrchestrator.items`) on `Unit_John`, `Unit_Linda`, `Unit_Lucy`, `Unit_Mark`, `Unit_Toba`, `Unit_Toba_Ally` has `hideIfUsed: 1`, so a 0-use item has no pouch button from level start in every level (e.g. the FP potion in The River and The Ridge, which hand out only the Health Potion). Leave the stale `remainingUses` overrides alone. The memory-level overrides (`GB_m1..m4`) stay as they are.
- [ ] Test: each hero prefab's items have `hideIfUsed` on (a data test reading the prefabs).
- [ ] Mark's `Command` blend tree in `Features/Player/Mark/Arts/Animations/AC_Playable_Mark.controller` uses `ItemUse/Mark-ItemUse-Down.anim` for its Down child instead of `Pull/Mark-Pull-Down.anim` (which shows Lucy's hit sprites); Side and Up unchanged. `Mark-Pull-Down.anim` itself is not deleted.

P1-3 Health potion on any ally (1.12, X-42)
- [ ] The Health Potion (`Features/Player/Shared/Items/HealthPotion/Bergsons_Ability_HealthPotion.asset`) is targeted: any ally unit (the user included) at any range (radius 99, unconstrained), valid only if that target is below full HP (`targetSelectCustomCall: '!CheckIfHealthFull'`, which runs on the target).
- [ ] The user pays the AP and the use; a target with 0 AP can be healed.
- [ ] A user at full HP can still give the potion: `HealthPotionAttributeModifierEffect.asset`'s `activationFeasibilityCheckFunction: '!CheckIfHealthFull'` is cleared.
- [ ] The heal lands on the target (not the user); the amount stays as today.
- [ ] The heal preview (`ItemEffectPreview.GetHealthIncrease`) previews on the hovered target when there is one, not the user. `UnitPanelUI.LowHealth.HoldsHealingItem` (pouch bob): keep its behaviour unless it now breaks; report what it does after the change.
- [ ] With no ally below full HP, the potion can be selected but has no valid target (or is greyed, whichever the targeted flow already does); report which.
- [ ] EditMode tests: target relation and range from the preset; a full-HP ally is not a legal target; a damaged ally at distance is; the effect has no user-side feasibility check.

## Scope

In: the three chunks above.
Out: 1.13 and 1.16 (parked); free use at 0 AP (D-787); the DU-2 FTP check bug; the Linda copy of the Cyclone preset (`Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/`); a real Command art clip (art team); M3/M4 work.

## Touches

Systems: Ability data and runtime (core: one additive setter on `RuntimeAbility.cs`, P1-1); Cyclone (`Features/Player/Lucy/Scripts/Cyclone/`, not core); Duo data read by Duos (core system, data only); item pouch HUD and preview (not core, `ItemEffectPreview.cs` is not on the core list); hero prefabs; Mark's animator controller.
USPs: Duos (cost data only).
Docs: GDD `lucy.md` (Cyclone cooldown on early end, L67 "keeps running"), `family-systems.md` DU-1 ("as wired … 1 AP in Mark–Lucy" goes), item/pouch rule in `combat-rules.md` if it names the potion's targeting (designer); `tech/core-systems.md` note for the setter (coordinator); glossary unaffected; tweak doc items closed.

## Approach

**P1-1 (opus, own review, own commit for the core setter).** Facts from the sweep: cooldown is set at cast (`RuntimeAbility._ActivateAbility` ~L411, `_coolingDownRemainingTicks = Parameters.coolDown`) and ticks down by 1 at each family-turn start (`PhaseTick` ~L296-301); `ResetCooldown()` ~L307 sets 0, `SetCoolDown()` ~L312 sets full; no arbitrary setter. Lifetime `lifeTurns: 3` on `Cyclone.prefab` ~L372; cast `coolDownV` 4 on `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`. Every end goes through `CycloneEntity.Dispose()` (~L76-102): fade from `PhaseTick` ~L66; burst `CycloneEntity.Burst.cs` (`TryBurst` ~L59, `BurstRoutine` → `Dispose` ~L129); deferred disposes in `CycloneEntity.Whirl.cs` (~L231, L280) and `CycloneEntity.Steer.cs` (~L212). Steps: add the setter to `RuntimeAbility` (additive, a new partial file if that keeps it clean); in `CycloneEntity` mark whether the end is a fade; on a non-fade end in play (not teardown), find the owner's cast ability (`Owner` → `GUnit.AbilityOrchestrator`, the ability where `CycloneRules.IsCycloneCast` is true) and apply the refund rule with `coolDown` and `lifeTurns` read from data, not hard-coded. Read the rule's numbers once and put the pure formula in `CycloneRules` so it is unit-testable. Check that a refund on the enemy turn shows correctly on the button at the next family turn (the button swap `CycloneButtonSwap.cs`).

**P1-2 (sonnet, reviewed with the feature).** Small YAML edits only; keep each file's line endings. Prefab item entries: set the existing `hideIfUsed` field; if an entry is a prefab-instance override, add the override in the same style as the memory levels do (`HearthMemoryWiring.Rules.cs:52` shows the field path). Controller: change the Down child's motion reference (guid/fileID) to `Mark-ItemUse-Down.anim`'s. If a YAML edit is not trivially safe, stop and report instead of guessing.

**P1-3 (sonnet, reviewed with the feature).** Preset fields from the sweep: today `applyMode: 2` (Self), `targetType: 1` (Cell), `targetFactionRelation: 0`, `includeSelf: 0`, `radiusV` constant 0; set `applyMode: 0` (Targeted), `targetType: 2` (CellOccupant), `targetFactionRelation: 1` (Ally), `includeSelf: 1`, `radiusV` constant 99, `targetSelectCustomCall: '!CheckIfHealthFull'` (checked by `AbilityPreset.CheckTargetSelectByCall`, `SendMessageUpwards` on the target; `FactionControllerBase.IsLegalAbilityTarget` ~L240-281). Enum values per `AbilityEnums.cs` and `FactionsEnums.cs`; confirm them before editing. Pouch use flow: `AbilitiesBarHUDUI.AddAbilityButton` ~L157-189 → `HandleAbilitySelection` → `OnCompletionPerRun` → `item.Consume()`; confirm a targeted item consumes once on completion. The preset is also on `Unit_TobaEnemy` (enemy factions never get item uses, so no effect). The AI never uses items.

## Risks

- Statics: none expected; if any are added, `PlayModeStaticReset`.
- AI reads: the AI never uses items or Duos; `RuntimeAbility` cooldown is read by the AI as before. Unit prefabs change (P1-2), so run `AIRegressionTest.Baseline_MatchesCurrentAI` by name once after P1-2 and compare with the last count (51); no re-baseline.
- Serialized renames: none.
- Save data: none (cooldowns are not saved across levels; confirm).
- Prefab/controller YAML: small edits; no prefab resave through the editor unless needed (it reorders); diff must show only the intended lines.
- Coroutines: the refund runs inside `Dispose`, including deferred disposes; it must not run twice for one Cyclone.
- Other branches: none active.

## Gates

Per chunk: compile clean; covering tests (Cyclone/Lucy fixtures for P1-1; new data tests + Duo/Cooperation + Onboarding item/memory-rule tests for P1-2; new potion tests + pouch for P1-3). Full EditMode suite after P1-1 (core) and once after P1-3, before the commit proposal. Review: P1-1 on its own (core); P1-2 + P1-3 together after P1-3. AI regression by name after P1-2. Play check by THJ, batched after P1-3: Cyclone burst by the Masher then cast next turn; Mark–Lucy Duo leaves AP; pouch in The River (no FP potion button); potion on a hurt ally at range, not on a full-HP one; Mark's Command facing down. Docs: listed under Touches.

Unity MCP was down at planning time and the editor is open (`miso/Temp` exists): if Unity isn't reachable, the implementer writes files only, does not start a batch Unity, and reports the tests as not run; the verifier runs them once THJ reconnects.

## Commit plan (proposed)

1. `feat(core): set an ability's remaining cooldown` (setter alone)
2. `feat(lucy): a Cyclone ended early gives back the cast cooldown as if it faded` (+ tests)
3. `tweak(duos): Mark–Lucy Duo costs no AP; tutorial text` (+ wiring test)
4. `tweak(items): pouch hides items with no uses in every level` (+ test)
5. `fix(mark): Command facing down uses Mark's own frames`
6. `feat(items): health potion heals any hurt ally at any range` (+ preview, tests)

## Log

- 2026-11-27 written by the coordinator from three Explore sweeps; THJ's answers D-784 to D-787.
- 2026-11-27 P1-1 built, review APPROVE. P1-2, P1-3 built; feature review FIX → fixed (D-792). Full suite 3090/3091 (1 Explicit), AI 51. THJ played: all work. Commits: `68c3b20ee`, `b67b5a273`, `c57015652`, `92ce2a9a5`, `5690b0a7f`, `05546c8b4`, `9e76224bd` (the EndCycloneSequence comment went into `b67b5a273`; 7 commits, not 8). Status: done; designer GDD updates owed.
