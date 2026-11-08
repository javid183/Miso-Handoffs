# Report: Sisters' tally C1c: Tempest Bloom kills count for both sisters

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md (C1b paragraph; rule D-449), design plans/onboarding/2026-11-08-sisters-tally-attribution-design.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done

## Findings on Tempest Bloom (verified by reading the code and assets)

- **Trigger.** `LucyCycloneProjectileScatter.OnTriggerEnter2D` (on `Features/Player/Lucy/Prefabs/Cyclone.prefab`) fires when a whitelisted projectile enters Lucy's Cyclone and the faction has the `_CycloneArrowScatter` unlockable. The whitelist holds only Linda's two arrows: `LindaAttackArrow.prefab` and `LindaAttackFireArrow.prefab` (the Duo's fire arrow). So a Bloom is always Linda's arrow in Lucy's Cyclone.
- **The copies.** One `Projectile.GetClone` per adjacent cell except backwards. A clone gets the original's `owner` (Linda), `callerParameters` and stat context (the firing `RuntimeAbility`). The copies are marked `QuiverArrow.MarkAsCopy` (they never land as pickups).
- **The synergy event.** `GlobalEventBus.RaiseSynergy(selfEntity.Owner, "Tempest Bloom", "projectile split by the cyclone")` is raised after the copies spawn. The unit is the **Cyclone's owner, Lucy**, not Linda. There are no targets. Then the original arrow lands at the split cell and is disposed.
- **Who gets the damage.** A copy's hit runs `AEffectCompound.Apply`: the damage goes first (the enemy reaches its minimum HP, and `GUnit.Die` raises `unitDied` synchronously from the health's min-reached callback), then `onAbilityEffectPerformedOn(firingAbility, target)`. `CombatLevelRunHandler` buffers that report and flushes it on the firing ability's `abilityPerformed` (`OnAbilityComplete` → `onAbilityPerformedOn` → `OnAbilityPerformedOn` → `onUnitDamageDone(firingAbility, target, loss, lethal)`). The attacker is `ability.Owner` = Linda. That is why THJ saw only Linda's number move.
- **When it ends.** There is no event for the copies' end. `AEffectSpawner` keeps the firing ability in progress until the **original** projectile's `onDestroy`, which happens at the split, so the ability completes after its hold time. A copy that lands later than that gives a report nobody flushes, so that kill counts for no one, today and after this fix. This is the design's fact 3, and it is still unconfirmed in play. THJ's test shows the copies near the Cyclone land in time.
- **Firing abilities.** Linda's basic attack is chosen by the player, so `FactionControllerBase` raises `abilityActivationStarted`/`abilityPerformed`. Linda's Watch reaction raises both itself (`LindaFactionRoleHandler`). The Duo's partner ability raises neither, so a fire arrow split during the Duo never gets a report, and the Duo bracket counts its deaths.

## What changed

- `Features/Onboarding/SistersTally/SistersTallyListener.cs`: the Tempest Bloom window.
  - **Opens** on `onSynergyTriggered` with id `"Tempest Bloom"`.
  - **Closes for new deaths** on the next `abilityActivationStarted` (a new action), on `turnEnded`, or on a level change.
  - **Inside the window**, an enemy `unitDied` at minimum HP is remembered (`RecordBloomDeath`). When a sister's lethal damage report then names that enemy, it counts once for Linda and once for Lucy instead of once for the shooter. The enemy joins the "counted for both" set, so no later report counts it again.
  - **The close never races with the report.** Remembered deaths stay claimable after the window closes, because the report comes on the shooter's `abilityPerformed`.
  - **Other changes in this file:**
    - The Duo-counted set was renamed `_countedByDuo` → `_countedForBoth`. It is a private field and now serves both rules.
    - The Duo's per-sister loop moved into a shared `CountForBoth`.
    - A new `abilityActivationStarted` subscribe/unsubscribe pair, kept symmetric.
    - `ForgetLevel` also clears the Bloom state.
    - A revived enemy is dropped from the remembered set.
    - The class summary has a Bloom paragraph.
  - All new handlers go through the existing `Guard` (AI worker thread skip, exception catch).
- `Features/Onboarding/SistersTally/Editor/SistersTallyTests.Bloom.cs` (+ `.meta`, new): 15 tests, listed under Tests.

No core edits, no prefab or scene edits, no new statics.

## Acceptance criteria

- [x] A Bloom kill gives both sisters +1, once: `Bloom_ACopysKillCountsOnceForEachSister` (1–1, two `Changed`), `Bloom_TheSameKillIsNeverCountedTwice` (repeat reports by Linda or Lucy add nothing), `Bloom_TheShootersReportArrivingAfterTheNextActionStartsStillCountsForBoth`.
- [x] No double count for Linda (her own lethal report becomes the shared count): same tests. The total is exactly 1–1.
- [x] Linda's normal arrow kill stays Linda's, and Lucy's finisher stays Lucy's: `Bloom_LindasNormalKillAndLucysFinisherStayTheirs`, `Bloom_ADeathAfterTheNextActionStartsIsLindasAlone`, `Bloom_AKillBeforeTheSplitIsLindasAlone`, `Bloom_ATurnEndClosesTheWindow`.
- [x] A death outside the Bloom is unaffected, and a death inside it with no sister's report counts nothing: `Bloom_ADeathNoSisterReportsCountsNothing`, `Bloom_ADeathAboveTheMinimumOrOfAPlayerUnitCountsNothing`.
- [x] The Duo and the Bloom together don't double up: `Bloom_InsideTheirDuoTheKillCountsOnceForEachSister`.
- [x] Nothing leaks across levels or after disconnecting: `Bloom_NothingCarriesIntoTheNextLevel`. Not eligible means nothing counts: `Bloom_InALevelThatIsNotEligibleCountsNothing`.
- [x] The guards are the same as the rest of the listener (`Guard`), subscribe/unsubscribe are symmetric, and there are no core edits.
- [ ] Play check (THJ/verifier): a Bloom copy kill moves both numbers by 1. The real event order (synergy → death → report on `abilityPerformed`) is covered only by fakes in EditMode.

## Tests

- **Full EditMode suite via Unity MCP, after a forced refresh and recompile:** 1695 run, 1694 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, untouched). The count is 1681 from C1b plus these tests.
- **Console:** no compile errors.
- **New tests:** `Bloom_OpensOnlyOnItsOwnSynergy`, `Bloom_ACopysKillCountsOnceForEachSister`, `Bloom_TheShootersReportArrivingAfterTheNextActionStartsStillCountsForBoth`, `Bloom_TheSameKillIsNeverCountedTwice`, `Bloom_ADeathAfterTheNextActionStartsIsLindasAlone`, `Bloom_AKillBeforeTheSplitIsLindasAlone`, `Bloom_LindasNormalKillAndLucysFinisherStayTheirs`, `Bloom_ADeathNoSisterReportsCountsNothing`, `Bloom_ADeathAboveTheMinimumOrOfAPlayerUnitCountsNothing`, `Bloom_ATurnEndClosesTheWindow`, `Bloom_InsideTheirDuoTheKillCountsOnceForEachSister`, `Bloom_InALevelThatIsNotEligibleCountsNothing`, `Bloom_NothingCarriesIntoTheNextLevel`, `Bloom_AnEnemyRevivedAfterABloomKillCountsAfreshWhenKilledAgain`.

## Save reset

No.

## Decisions I made

- **Count at the report, not at the death** (unlike the Duo). The copies' kills already reach the damage event as Linda's, so converting her report counts only kills the Bloom's ability really made. A burn tick or hazard death inside the window counts nothing, which is stricter than the Duo bracket. The death is still needed to separate "after the split" from "before it": an arrow that pierced an enemy on its way to the Cyclone keeps that kill Linda's.
- **The window closes on the next action start**, not on the shooter's `abilityPerformed`. The synergy event doesn't name the firing ability, and the report rides on that same `abilityPerformed`, so listener order would race. Remembered deaths stay claimable until reported, revived or the level ends. A stale entry can't be claimed later: a dead enemy can't lose HP in a later snapshot.
- **No check on which sister is involved.** The Cyclone's whitelist holds only Linda's arrows, so every Bloom is Linda's arrow in Lucy's Cyclone. The conversion requires the reporting ability's owner to be a sister. A non-sister report on a remembered enemy counts nothing, as before.
- The private field rename `_countedByDuo` → `_countedForBoth` (the set now serves both rules).

## Needs THJ

None.

## Docs to update

- Tally tech plan: C1c done. Acceptance: "a Tempest Bloom copy's kill counts once for each sister".
- Attribution design, fact 3: the copies' reports do arrive (THJ's play check). The unit on the synergy event is Lucy (the Cyclone's owner).
- The tally `tech/` note or the GDD subsection, if written: the Bloom window rule above.

## Risks and loose ends

- **Late copies.** A copy that lands after the firing ability completed gives no damage report, so that kill counts for no one. This is core behaviour (`AEffectSpawner` ends "in progress" on the original's destroy). Fixing it needs a core change, outside this chunk. It is worth a long-range play check: Cyclone far from the targets.
- **An ability that starts between the split and a copy's hit** closes the window early. That copy's kill then counts for Linda only. An example is a reaction triggered by the first copy hit, such as the Masher counter.
- **Other damage from the same ability after the split** would also count for both, for example a multi-arrow shot where another arrow kills directly. No such ability exists today by reading.
- The fire arrow inside the Duo: the Duo bracket counts it, as before. The rule still holds there.

## Proposed commits

`SistersTallyListener.cs` holds both C1b's Duo/eligibility code and C1c's Bloom code. C1c rewrites C1b lines: the field rename and the shared `CountForBoth`. The two can't be split without partial staging, which isn't available here. C1b's Attribution tests also won't compile without the listener. **Proposal: one combined commit.**

1. `feat(onboarding): sisters' tally counts Duo and Tempest Bloom kills for both sisters and is decided per level by the deployed sisters` (plain):
   - C1b only: `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTally.cs`, `.../SistersTally/SistersTallySource.cs`, `.../SistersTally/Editor/SistersTallyTests.cs`, `.../SistersTally/Editor/SistersTallyTests.Attribution.cs`, `.../SistersTally/Editor/SistersTallyTests.Attribution.cs.meta`, `miso/Assets/_Project/Content/Levels/LevelBase.prefab`
   - C1b + C1c: `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyListener.cs`
   - C1c only: `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.Bloom.cs`, `.../SistersTally/Editor/SistersTallyTests.Bloom.cs.meta`

   **Alternative, if separate history matters:**
   - **Commit 1** (C1b message): all of the above except the two `SistersTallyTests.Bloom.cs*` files. The listener goes in whole, Bloom code included.
   - **Commit 2:** `test(onboarding): Tempest Bloom kills in the sisters' tally` with the Bloom tests.

   This compiles at each step, but commit 1 then carries the Bloom logic under a Duo-only message. I'd take the combined one.

   Leave out THJ's uncommitted `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`.

## Other branches

None (the tally is onboarding-only).

## How to see it

1. Stop Play mode, and press Ctrl+R if needed. Use a save where Linda & Lucy's Tempest Bloom is unlocked (Bond Lv 2, after the Yard) or the Hearth's last segment (`GB_m4-mark`), which grants the Bloom for that mission. Both sisters must be deployed so the counter shows.
2. With Lucy, place a Cyclone next to an enemy, or between Linda and a group.
3. With Linda, shoot through the Cyclone so a split copy kills an enemy. Both numbers in "Linda N · Lucy N" go up by 1 at the same moment. Linda's number must **not** go up by 2.
4. With Linda, kill an enemy with a normal shot (no Cyclone). Only Linda's number moves. Let Lucy's Family Role finish a wounded enemy: only Lucy's number moves.
5. Optional: with the Cyclone far from the targets, check whether a far copy's kill counts at all. If neither number moves, that is the late-copy loose end above.

## Fix round (review's two should-fixes)

Changed only `SistersTallyTests.Bloom.cs` (no runtime code):
- `Bloom_LindasNormalKillAndLucysFinisherStayTheirs` now opens and closes a Bloom window first (`StartAction(); RaiseBloom(); StartAction();`, asserts it is closed), then runs Linda's normal kill and Lucy's finisher. A leaking window would make the result 2 for Lucy, so it now fails without the isolation.
- New `Bloom_LucysReportOfARememberedDeathCountsOnceForEachSister`: Bloom raised, goblin dies, Lucy's report claims it, tally 1-1.

Result: SistersTallyTests 69/69 passed (Unity MCP, EditMode). Play mode was stopped first. Full suite not re-run.
