# Report: Linda's Quiver, C3 (Recall)

Plan: plans/2026-10-26-linda-quiver-tech.md (chunk C3)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: partial. Built and tested, but the `AIRegressionTest` failure message changed (one new line), so I stopped per instructions; needs the coordinator's decision. No core-system code changed.

## What changed

Paths under `miso/Assets/_Project/`. LF, no BOM, `.meta` for every new file.

New, `Features/Player/Linda/Scripts/Quiver/`:
- `RecallRules.cs`: pure. `CanRecall`, `QuiverAfter` (min(size, count + grounded)), and `Resolve`: takes arrows off the board in a fixed cell order, locked stacks included, capped by quiver room; whatever the quiver refuses (or does not fit) stays on its stack with its lock.
- `RecallLines.cs`: two placeholder cast barks, tagged `[PLACEHOLDER] ` ("Back to me." / "Come home.", the Recall variants from the text report).
- `GroundedArrowField.Recall.cs`: partial of the field. `RecallTo(quiver)`: runs `Resolve`, redraws the stacks, spawns one tween sprite per returned arrow flying in a straight line to Linda (ignores walls and units; the sprite turns along the flight), one cast bark. Flights are tracked in the same list as the toss sprites, so level end stops and destroys them; a flight also ends if Linda dies.
- `Editor/RecallRulesTests.cs` (+ meta): 17 tests (arithmetic, locked, extras, split stack with lock, refusing quiver, lines, closed-field count).

Edited (C1/C2 files, extended):
- `GroundedArrowField.cs`: `GroundedCount` returns 0 once the field is closed (level ended); the `OnLevelEnded` body moved into a public `Close()` (same behavior).
- `LindaQuiver.cs`: `Recall()` (the message the ability's effect sends), serialized `recallFlightSeconds` (0.45, getter `RecallFlightSeconds`; not written into the prefab, the default applies).
- `Editor/QuiverWiringTests.cs`: 4 new wiring tests (preset values, effect, 10th entry, methods exist).

New, `Resources/UnitSpecific/Player/Linda/Abilities/Recall.meta` and `Recall/`:
- `Linda_Ability_Recall.asset`: AbilityPreset. Title "Recall", description tagged `[PLACEHOLDER]`, icon reused from Linda's Explosive Arrow, AP Singular, coolDownV 2, apply mode Self, Instant, `minimumDuration` 0.5.
- `Linda_Ability_Recall_Effect_FunctionCaller.asset`: existing `AEffectFunctionCaller`, `functionName: Recall`, called on Self, `activationFeasibilityCheckFunction: HasGroundedArrows`.
- both `.meta` files.

Edited asset: `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: abilities array size 9 to 10, entry 9 = Recall, with the same disable-target-indication and stat-source overrides as entry 8 (a Duo). Small YAML additions only; no number-key shortcut, existing entries not reordered.

## Acceptance criteria

- [x] **Greyed out with nothing grounded, usable with 1 or more.** Wiring: the effect's feasibility string is `HasGroundedArrows` (test `RecallEffect_CallsRecallAndNeedsGroundedArrows`); C1's `LindaQuiver.HasGroundedArrows` answers it. Pure: `CanRecall_NeedsAGroundedArrowAndALivingLinda`. The visual grey-out is not verified in play.
- [x] **Level-safe check (C1 reviewer note).** `GroundedCount` reads 0 on a closed field (test `GroundedCount_ReadsZeroOnceTheFieldIsClosed`); the field is closed on level end and cleared on destroy; the action itself goes through `Current` (level-matched). Still a plain read, no Unity object calls, safe on the worker thread.
- [x] **1 AP, cooldown 2.** Preset test: AP Singular, `coolDownV` 2. "Unusable on her next turn, usable on the one after" depends on how the engine counts cooldown (Harmonic Slam uses 1); not verified in play.
- [x] **Every grounded arrow flies back, locked or behind walls; quiver = min(size, count + grounded); board empty of her arrows; no damage.** EditMode: `EveryStackComesBack_...`, `LockedStackComesBackToo`, `QuiverAfter_...`. Walls: the flight is a plain tween and `Resolve` never looks at cells, so walls cannot matter. No damage: the only effect is the Function Caller. Flight look and timing not verified in play.
- [x] **Appended as the 10th entry, no shortcut.** Test `Linda_HasRecallAsTheTenthAbility`. How the ability bar shows it is not verified in play.
- [x] **Turn waits for the flight.** Done in data: the preset's `minimumDuration` 0.5 (the engine's own wait in `AbilityPreset`) is longer than the 0.45 s flight; a test checks minimum duration >= flight. The Function Caller never reports "in progress", so no core change was needed.
- [x] **Cleanup.** Level end: `EndHandBackBeats` stops all flights and destroys the sprites. Linda's death: each flight ends and destroys its sprite on the next frame. Barks skip a dead Linda. Not verified in play.
- Extras beyond size: by conservation none exist; if some did, they stay on the board (tested: `MoreArrowsThanRoom_ExtrasStayOnTheBoard`).

## Test results

Full EditMode suite, command line, Unity 6000.3.4f1 (editor closed). Scratchpad `c3b.xml`, `c3b.log`.
- 852 tests, 851 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI`. (An earlier run had my own wiring test failing on `minimumDuration`; fixed.)
- 21 new tests (831 to 852). No compile errors.

### AIRegressionTest: message CHANGED (stopped here, not re-baselined, test not edited)

Diff against the C2 final run (`c2c.xml`, the same as the baseline):
- `CHECKS: 709  FAILURES: 38` becomes `CHECKS: 710  FAILURES: 39`
- `abilities.count: expected 90, found 96` becomes `found 97`
- one new line (in the failures list, and again in the full FAIL list): `abilities.unexpected Assets/_Project/Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset: new ability is not in today's baseline`

Cause: `CheckAbilities` scans every `AbilityPreset` in the project (`FindAssets("t:AbilityPreset")`) and fails any not in the baseline catalog, not just Linda's Duos, so any new preset anywhere adds this line. The class was already red (96 found vs 90), and the new line is the same kind as the existing "abilities.unexpected" ones. Options: accept the extra line until the dedicated baseline fix (add Recall to the catalog there), or something else you decide. I did not edit the test or baseline.

## Save reset

No.

## Decisions I made

- **Wait for the flight through the preset's `minimumDuration`**, not `IsInProgress`; same behavior as the plan, no core code. Flight 0.45 s, wait 0.5 s.
- **Barks** use the same popup as C2 (`DamageNumberManager.ShowText`); one line on cast from the Recall pair; skipped when barks are silenced or Linda is dead.
- **One tween sprite per arrow, all leaving together**, from where the stack's icon sat; arrows of one stack overlap on the way (no stagger). Easing is quadratic in.
- **Description is tagged `[PLACEHOLDER] `**; the field is plain text and I found no stripper for ability descriptions, so the tag may show in the tooltip. Check in play.
- **`GroundedArrowField.Close()`** is public (it was the private level-end handler body), so it is testable.

## Needs THJ

None for this chunk. Still open: final name (Recall or Encore) and the description wording.

## Docs to update

- `tech/combat-architecture.md`: Recall in `GroundedArrowField.Recall.cs`, `RecallRules`, the preset, and the `minimumDuration` wait.
- `status.md` / `build-log.md`: C3 built; play check due (the playable core is C1 to C3).

## Risks and loose ends

- **Not seen in play:** flight look and speed, the cooldown count, the bark, the `[PLACEHOLDER]` tag in the tooltip, how the ability bar shows a 10th ability with no key, and whether the Self-cast confirm feels right (click on Linda). Self-cast with no target is the least certain part.
- **Unit_Linda entry 9** only has the overrides copied from entry 8; its animation fields are empty (no cast animation), like the Duos.
- **Worker thread:** nothing the AI reads changed.
- **Test note:** `GroundedCount_ReadsZeroOnceTheFieldIsClosed` creates a field in edit mode (no Awake) and closes it; the static pointer is left at a closed, destroyed field, which reads 0.
- The AIRegressionTest message change, above.

## Proposed commits

Recall's files fit the merged units; no separate unit is needed and nothing here touches core.

(a) Quiver scripts and tests: `Scripts/Quiver/RecallRules.cs`, `RecallLines.cs`, `GroundedArrowField.Recall.cs` (+ metas), `Editor/RecallRulesTests.cs` (+ meta), and the edits to `GroundedArrowField.cs` and `LindaQuiver.cs`.

(d) Prefabs, data and wiring tests: `Resources/UnitSpecific/Player/Linda/Abilities/Recall.meta` and `Recall/` (2 assets, 2 metas), `Features/Player/Linda/Prefabs/Unit_Linda.prefab`, `Scripts/Quiver/Editor/QuiverWiringTests.cs`.

Never stage the TMP fallback asset or the two ProjectSettings files.

## Other branches

`thj/home-test` and `thj/onboarding` once this reaches `main`, as with C1 and C2.

## How to see it

1. Open Unity, let it compile; open a level with Linda (for example M4).
2. Open Linda's ability list: Recall is greyed out with nothing on the ground.
3. Shoot twice with the bow so two arrows lie on the ground (quiver 2/4), one behind a wall or under an enemy if the level allows. Select Recall and click Linda: all grounded arrows fly in straight lines to her, a short line pops up, the quiver is 4/4 (shoot four times to check), the board shows no arrow icons, nothing took damage.
4. Try Recall on her next turn: unavailable. The turn after: available (if arrows are grounded).
5. End the level mid-flight: no sprites left over. Kill Linda mid-flight: they vanish.
6. Tune `Recall Flight Seconds` on `Unit_Linda`'s `LindaQuiver`; keep it at or under 0.5 (the ability's minimum duration).
