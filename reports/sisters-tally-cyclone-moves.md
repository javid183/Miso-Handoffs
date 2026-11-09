# Report: Sisters' tally counts kills a Cyclone makes on its own moves

Plan: none (S bugfix, Tier 1, dispatched by the coordinator)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: partial (code and tests written; not compiled or run, that is the verifier's)

## What changed

- `Features/Onboarding/SistersTally/SistersTallyListener.cs`: new `RecordEffectOutsideAbility`, a subscription to the raw `onAbilityEffectPerformedOn`, an in-progress ability set (added on `abilityActivationStarted`, removed on `abilityPerformed`, cleared on turn end and `ForgetLevel`), and a `_killedByPlayer` set (filled in `RecordDamage`, cleared on `unitBorn` and `ForgetLevel`). Listener removed symmetrically.
- `Features/Onboarding/SistersTally/Editor/SistersTallyTests.OutOfAbility.cs` (+ `.meta`, hand-written, Unity may regenerate the guid): 13 EditMode tests. They build an ability with an owner by reflection (`RuntimeAbility._owner` -> `AbilityOrchestrator._owner`), no prefabs, no save.

No core file touched.

## Acceptance criteria

- [x] An out-of-ability sister effect kill counts once for her: `OutOfAbility_ASistersEffectKillCountsOnceForHer` (repeated report counts once). Test only, not run.
- [x] During an open Duo it doesn't double count: `OutOfAbility_InsideADuoTheDuoCountsAndThisAddsNothing`.
- [x] Non-sister, non-lethal, player target, self target, ownerless ability count nothing: four tests.
- [x] An in-progress ability's kill counts once (no double): `OutOfAbility_AnAbilityInProgressCountsOnlyThroughTheDamageEvent` (effect report ignored while in progress, damage event counts, later effect report and stale zero report add nothing).
- [x] A Bloom late copy converts per D-449: `OutOfAbility_ABloomCopyLandingAfterTheShootersAbilityEndedCountsForBoth`.
- [ ] Compiles and passes: not verified here.
- [ ] Play check: see How to see it.

## Save reset

no

## Decisions I made

- Ability "in progress" is tracked per ability, so a Cyclone's own report counts even while another sister ability is mid-action.
- `_killedByPlayer` is filled from `RecordDamage` for any player attacker (so John's kill blocks a later Lucy report on the same corpse). It is consulted only by the new path, so existing in-ability behavior is unchanged.
- Duo trigger abilities are skipped in the new path too (same rule as `RecordAbilityDamage`).
- "Dead" uses the existing at-minimum-health check, not `IsAlive`.

## Needs THJ

none

## Docs to update

- `reports/sisters-tally-c1c.md` / tally design: the "late copies count for no one" gap is closed in code (see below), subject to the ordering risk.

## Risks and loose ends

- **Late copies (C1c gap): holds only if `unitDied` is raised before `onAbilityEffectPerformedOn` for the same hit.** `AEffectCompound` raises the effect event right after `effect.Apply` (`AEffectCompound.cs:165-167`), and `GUnit.DieInternal` raises `unitDied`. I could not find from code the call that kills a unit when health hits its minimum (only `AGUnitSpawner`, `DarkWormPassiveAbility` and spawner binding call `Die` in Core), so I could not confirm the order. If death comes later (deferred), a late copy's kill counts for Linda alone and the later death is remembered with nothing to claim it. The Bloom test fakes death first. Worth a play check.
- An ability that starts but never performs (interrupted) stays "in progress" until turn end, so its own kills would still be dropped as before. Rare; unchanged from today.
- Enemy killed by a non-player-owned effect then hit by a sister's out-of-ability report: not counted only if a player's lethal hit reached the damage event; otherwise a corpse still targeted would count. Dead units are unplugged from cells, so unlikely.
- Test `.meta` guid is hand-made.

## Proposed commits

1. `fix(onboarding): sisters' tally counts kills made by an ability's own moves after it finished`: `SistersTallyListener.cs`, `Editor/SistersTallyTests.OutOfAbility.cs`, `Editor/SistersTallyTests.OutOfAbility.cs.meta` (plain)

## Other branches

none

## How to see it

1. Open a tally level (Hearth Memory 3 or 4, or The Trail) with both sisters deployed.
2. Lucy drops a Cyclone near an enemy with low health, end turn.
3. Let the Cyclone's own move kill that enemy: the counter ticks up for Lucy once.
4. Linda shoots through the Cyclone (Tempest Bloom) so a copy lands late and kills: both sisters should tick once.
5. Check the same kill is not counted twice and a Duo kill still counts once each.

## Fix round 1

Applied the review's two must-fixes in `Editor/SistersTallyTests.OutOfAbility.cs` (production code unchanged):
- Line 74: `OutOfAbility_AnAbilityWithoutAnOwnerCountsNothing` now uses `MakeAbilityOwnedBy(null)` instead of `new RuntimeAbility()`.
- Lines 99-101: removed the zero-damage `onUnitDamageDone` assertion in `OutOfAbility_AnAbilityInProgressCountsOnlyThroughTheDamageEvent` and the words "and a stale damage report" from its comment; the late effect report check stays.
Should-fixes skipped. Not compiled or run.

## Verification (coordinator, 2026-11-09 ~14:30, THJ's open editor via computer use)

- Compile: Ctrl+R in the editor, console 0 errors (14 known warnings: serialization depth, `m_LightOverlaySprite`).
- EditMode Run All: **1753 / 1754**, the only red is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. Filter `SistersTally`: 136 / 136 green (13 new).
- Review FIX (`-review.md`) was test-only; fix round 1 applied the two must-fixes as written, confirmed by the green run. Not re-reviewed.
- Not verified: the in-game Cyclone kill (THJ's play check below). The two modified Core AI files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, from 2026-10-29) are not part of this change: keep them out of the commit.
