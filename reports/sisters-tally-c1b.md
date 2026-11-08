# Report: Sisters' tally C1b: Duo attribution and per-level eligibility

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md (C1b)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done

## What changed

- `Features/Onboarding/SistersTally/SistersTallyListener.cs`: the Duo bracket (open on the synergy event "Duo" with a sister among the partners, close on the trigger ability's `abilityPerformed`, also on any `turnEnded`; an enemy `unitDied` at minimum HP inside it counts once per sister partner); trigger-ability damage reports always ignored; later lethal reports on an enemy the Duo already counted ignored; per-level eligibility (both sisters deployed as player units: read at `levelStarted`, then `unitBorn`). All new handlers go through the existing guard (AI worker thread, exceptions); subscribe/unsubscribe symmetric; all per-level state cleared on `Connect` and `Disconnect`.
- `Features/Onboarding/SistersTally/SistersTally.cs`: `IsEligible(mission, excluded)` (roster-based) replaced by `IsMissionIncluded(mission, excluded)` + `BothSistersDeployed(nicknames)` + `IsSister(nickname)`; new `SetEligible(bool)` (raises `Changed` only on a change).
- `Features/Onboarding/SistersTally/SistersTallySource.cs`: supplies the real providers: deployed player units from `CombatLevelRunHandler.Instance.PlayerUnits`, Duo trigger detection (the ability's effects contain an `AEffectCoOpTrigger`, matched on `TriggerID` when given), enemy check via `GetFactionRelationToPlayer`. Tooltip of the excluded list reworded (not serialized).
- `Content/Levels/LevelBase.prefab`: `excludedMissions` emptied (The Hearth removed); the field stays.
- `Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs`: class made `partial`; setup now starts a level with Linda, Lucy and John deployed; eligibility tests rewritten for the new helpers; asset test now expects an empty excluded list; change-count test expects 3 (level start, then eligibility).
- `Features/Onboarding/SistersTally/Editor/SistersTallyTests.Attribution.cs` (+ `.meta`, new): 23 tests for the Duo bracket, per-level eligibility and the Hearth's deployments.

No core files touched.

## Acceptance criteria

- [x] Bracket opens on a sister's Duo and closes only on its own trigger: `Duo_OpensOnASistersDuo_AndClosesOnlyOnItsOwnTrigger`, `Duo_OtherSynergiesAndDuosWithNoSisterDoNotOpen`.
- [x] Linda–Lucy Duo kill counts for both: `Duo_LindaAndLucysDuoKillCountsForBoth` (2 kills → 2–2, `Changed` per count, same frame).
- [x] Mark–Lucy credits Lucy only: `Duo_MarkAndLucysDuoKillCountsForLucyOnly`.
- [x] Fake death / above-minimum death inside the bracket doesn't count: `Duo_ADeathAboveTheMinimumInsideTheDuoCountsNothing`; player unit dying inside doesn't count: `Duo_APlayerUnitDyingInsideTheDuoCountsNothing`; the same enemy only once: `Duo_TheSameEnemyCountsOnce`.
- [x] Trigger's own damage report not double counted, before or after the close (either listener order): `Duo_TheTriggersOwnReportOnTheAimedEnemyIsNotCountedAgain`, `Duo_TheTriggersReportCountsNothingEvenOnAnEnemyTheDuoDidNotCount`, `Duo_ALaterLethalReportOnAnEnemyTheDuoCountedIsIgnored`.
- [x] Deaths outside a bracket follow the lethal-damage rule only: `Duo_DeathsOutsideTheBracketCountNothing_TheLethalHitRuleStillDoes`.
- [x] A bracket doesn't survive a level change (abort/restart): `Duo_ABracketDoesNotSurviveALevelChange`, `Duo_ReconnectingTheSameListenerForgetsAnOpenBracket`; safety close at turn end: `Duo_ATurnEndClosesABracketLeftOpen`.
- [x] Eligibility per level from deployed player units: `Level_NotEligibleUntilItsStartReadsTheDeployedUnits`, `Level_OneSisterDeployed_IsNotEligible`, `Level_ASisterRevealedLater_MakesItEligibleFromThen`, `Level_AnEnemyNamedLikeASisterDoesNotMakeItEligible`, `Level_StaysEligibleWhenASisterFalls`, `Level_InAnExcludedMission_IsNotEligibleEvenWithBothSisters`, `Level_EachLevelDecidesForItself_AndTheMissionsCountCarriesOn`, `Duo_InALevelThatIsNotEligibleCountsNothing`.
- [x] The Hearth leaves the excluded list, list feature kept: `Asset_EveryLevelHasTheSource_NextToTheBus_LeavingOutNoMission`.
- [x] Hearth segments 3–4 show it, 1–2 don't (data): `Asset_TheHearthsLaterSegmentsDeployBothSisters_TheFirstTwoOne`; full mission table under "What I verified" below.
- [x] HUD counter updates when eligibility is decided at level start: `SetEligible` raises `Changed`, which the C2 counter already listens to (`Level_ASisterRevealedLater_MakesItEligibleFromThen` asserts one `Changed`). The on-screen part needs the verifier's play check.
- [ ] Play checks (verifier/THJ): a Duo kill in The Trail moves both numbers; Hearth segment 3 shows the counter, segments 1–2 don't.

Tests: tally group 63/63 green. Full EditMode suite via Unity MCP: 1680 run, 1679 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched). Compile clean (no console errors).

## What I verified

**The trigger's own report (by reading, V; not play-checked).** The Duo trigger presets (`Linda_Lucy_Duo_Ability`, `Mark_Lucy_Duo_Ability`) have `actualTargets: 1`. `RuntimeAbility.Activate` → `OnCompletionShared` raises `onAbilityEffectPerformedOn(trigger, target)` for each selected target when the trigger completes, which is after the whole Duo (`AEffectCoOpTrigger` holds it in progress). `CombatLevelRunHandler.OnAbilityComplete` (listener of `abilityPerformed`) then flushes: it compares the target's HP with the snapshot taken at the trigger's `abilityActivationStarted` (all units) and raises `onUnitDamageDone(trigger, aimedTarget, loss, lethal)` with attacker = the sister who pressed the button. So **it does fire** whenever the aimed entity is an enemy unit that lost HP during the Duo (lethal if it died). It fires from the same `abilityPerformed` that closes the bracket, so the order versus the tally's close is not guaranteed; the listener therefore ignores any damage report whose ability carries a CoOp trigger, whatever the bracket state, and also ignores later lethal reports on an enemy the Duo already counted. THJ's 0 in his play check is consistent with the aimed target being a cell/bundle or an enemy that wasn't hit.

**Hearth deployments (data read in the editor).** Units placed active in each level prefab, sisters only (faction `Bergsons`, the player's):

| Mission | Level | Sisters at start | Tally |
|---|---|---|---|
| M0 The Hearth | GB_m1-linda | Linda | no |
| | GB_m2-lucy | Lucy | no |
| | GB_m3-john | Linda, Lucy | yes |
| | GB_m4-mark | Linda, Lucy (hidden groups are Dark Claws only) | yes |
| M2 The Trail | all 4 levels | Linda, Lucy (+1 roster slot) | yes |
| M4 The White Mothers | all 7 levels | Linda, Lucy (+1 slot) | yes |
| MS1 The River | GB_s1-river | Lucy | no |
| MS2 The Ridge | GB_s2-ridge | Linda | no |

No sister is hidden in the Hearth, so the reveal path isn't used there today; it's handled anyway (below).

## Save reset

No.

## Decisions I made

- **A sister revealed mid-level:** the level becomes eligible from the moment the second sister is in play (`unitBorn`, which `HiddenLevelUnits.Reveal` and spawns raise through `RegisterUnit`). Kills before that count for no one; the counter appears then. Once eligible, a level stays eligible even if a sister falls.
- **Before `levelStarted`** every level reads not eligible (counter content hidden; the HUD is hidden then anyway). Eligibility is read from `CombatLevelRunHandler.PlayerUnits` at `levelStarted` (placed units + roster slots, branches already applied).
- **Trigger identity** is "the ability's effects contain an `AEffectCoOpTrigger` with this trigger id" (the synergy's detail is the same id), not "owner == activator", so tests don't need an ability owner. Only one Duo runs at a time.
- **Extra guard:** a lethal damage report on an enemy the Duo already counted is ignored (covers a partner's report in any order, not only the trigger's). Same behaviour as asked, stricter.
- **Safety close on `turnEnded`:** a Duo never spans a turn end, so a bracket left open (Duo interrupted) can't credit later deaths.
- **Enemy check for deaths** uses the faction relation to the player (`Enemy`), like Mark's continuous attack; the damage rule keeps its old "not a player unit" check (the run handler only reports enemy-relation hits).
- **No mission (level played on its own):** stays not eligible, as in C1.
- New tests in a new partial file; the old test class became `partial`.

## Needs THJ

None for the build. One side effect to know (below, first risk).

## Docs to update

- Tally tech plan: C1b done; acceptance "eligibility = both sisters deployed in the level".
- `tech/` note or GDD tally subsection (if/when written): the Duo bracket rule, the reveal choice above, and that the trigger's report is ignored.
- Backlog item "Duo damage never reaches `onUnitDamageDone`" (design question C) stays open; this build doesn't fix it.

## Risks and loose ends

- **Per-level eligibility changes other missions too** (the source is on every level): M1 Hidden Sanctuary – First Step, level `Level1-C2`, places both sisters, so the tally now shows there (roster John + Lucy, before: never). In M11/M13/M14 test levels with one sister (`Test_Level_ABK_02`, `_05`, `Level1-C1 Test Khashayar`) it now hides where the roster rule showed it. Harmless for the onboarding flow; add M1 to the excluded list if it shouldn't show.
- A burn tick, hazard or other death inside a Duo would be credited to the sister partners. By reading, ticks run on phase/turn ticks, not mid-ability; not play-checked.
- Tempest Bloom's window is not built (with Tally: return, per plan).
- Once C4 wires the fade step, a replay of the Hearth after The Trail would read faded (fade is global). Probably unreachable; noting it.
- Eligibility relies on `levelStarted` firing after the source's `OnEnable` (the level prefab is enabled before `StartLevel`; true by reading `ProgramFlowHandler`/`CombatLevelRunHandler`).

## Proposed commits

1. `feat(onboarding): sisters' tally counts Duo kills for each sister in the Duo and is decided per level by the deployed sisters` (plain):
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTally.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyListener.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallySource.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.Attribution.cs`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.Attribution.cs.meta`
   - `miso/Assets/_Project/Content/Levels/LevelBase.prefab`

   Leave out THJ's uncommitted `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`.

## Other branches

None (the tally is onboarding-only).

## How to see it

1. Stop Play mode, Ctrl+R if needed. Start from a save that reaches The Trail (or fast-forward to it).
2. **Duo kill in The Trail:** in the route level (`GB_m2-blood`, column of Dark Claws), fire the Linda–Lucy Duo up the column. When the Claws die, both numbers in "Linda N · Lucy N" go up by the number of kills at once (3 kills → +3 each). Aim at a Claw that dies to check the trigger's own report doesn't add a second count to the presser.
3. A normal kill afterwards still counts for the sister who landed it; Lucy's Family Role finishing Linda's target counts for Lucy only.
4. **Hearth:** play The Hearth memory. Segments 1 (Linda alone) and 2 (Lucy alone): no counter. Segment 3 (`GB_m3-john`): the counter appears at the level start and counts from 0; segment 4 (`GB_m4-mark`): it keeps the Hearth's count. Then The Trail starts again from 0.
5. The River and The Ridge: no counter.
