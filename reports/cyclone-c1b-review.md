# Cyclone C1b review (Whirl + C1a fix round)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. Branch `thj/cyclone`, uncommitted tree.

**Verdict: FIX** (one must-fix, within the plan). C1a should-fixes all done. Core changes match D-532/D-533, each its own commit; no-listener turn switch unchanged; no signature changed. Line endings/BOM kept; no private IDs; static resets present.

## Must fix
1. `CycloneEntity.Whirl.cs:20-23, :111-121`: `ReactionTimeoutFrames = 600` / `PullTimeoutFrames = 300` count frames: 2.5 s at 240 Hz, while Watch takes ~3.5-4 s (QTE 1 s, notices ~1.6 s, arrow, camera). Hit can land before Watch → breaks pull → reactions → hit and the Bloom split. Fix: unscaled-seconds caps (e.g. pull 3 s, reactions 15 s), testable clock; keep the 10-quiet-frames settle.

## Should fix
1. Hold watchdog counts real time during pause (`CombatLevelRunHandler.TurnSwitchHolds.cs:56-58`, `realtimeSinceStartup`); Whirl freezes at timeScale 0, watchdog drops the hold after 5 s. Fix: scaled time or skip while timeScale 0 (one-line core).
2. Hit/report/log still run after the level ended (`CycloneEntity.Whirl.cs:123-133`): skip when `IsLevelEnded`.
3. Hold registered before `StartCoroutine` on a possibly inactive object (`:54-60`): early return or register inside the routine.
4. "One damage path only" untested at effect level: test a compound with `CycloneHitContext` asserting no `onAbilityEffectPerformedOn` and no relay.
5. Report's watchdog risk text wrong: the Watch flow blocks through `PhaseData.IsInProgress` (`PlayerController.cs:1592`), not the hold.
6. (Q4) A deferred Dispose waits for the Whirl but not for pull moves (owned by the Cyclone): wait for pending moves == 0 before a deferred dispose.

## Answers
- **Q1 watchdog:** normal Whirl + Watch can't exceed 5 s (Watch blocks via `IsInProgress`; hold-only time < 1 s). Exceeded only under pause (should-fix 1). If exceeded: holds cleared, turn switches, rest of the Whirl lands at family turn start.
- **Q2 tally tests:** legitimate. Old tests modelled re-killing a dead enemy. Resurrect/Revive raise `unitBorn`, listener clears the guard; worm splits are new units. New tests fail without the guard.
- **Q3 Masher:** yes. `MasherGoblinFactionRoleHandler.Counter.cs:105-118` classifies a Whirl hit as Reaction at end of enemy turn (ChosenAbility on the cast Whirl) and answers Lucy if in reach; the switch waits for it. Masher is Immovable, so one next to the Cyclone answers every enemy turn.
- **Q4 dispose:** level end safe (only post-end hits, should-fix 2). Scene unload harmless. Gap: unit mid-pull (should-fix 6).

## Notes
- `onUnitDamageDone` once per hit: `CycloneHitContext` skips `AEffectCompound.cs:165` and the relay (:117). Lucy's role (OnActionComplete) doesn't fire. Enemy attacker memory unchanged.
- New listeners see Whirl damage: Wrath, Atman Barrier, AP provider, Blood Debt filter it out; barks and mission stats count it; `GroundedArrowField.KillHandBack.cs:17-25` now sees Whirl kills (play check). Kill rewards from Cyclone kills are new (were 0).
- Pull + hazards via `AEffectPusher.TryMoveTo` as claimed; Immovable filter like Black Despair; Masher/Deev tagged; large units excluded.
- AOE telegraphs, hazards, `OnGridEntity`, vortex, pusher untouched.
- Design: `WhirlsAtEndOf` true for every enemy faction (two enemy factions = two Whirls a round); a skipped enemy turn raises no `TurnEnding` (no Whirl that round).
- Pre-existing: Watch queued if an AI brain is computing when a pull lands; play-check Watch on end-of-turn pulls.
- `TurnEnding` test uses reflection on `RaiseTurnEnding`; `SwitchTurnIE` wiring covered by play.
