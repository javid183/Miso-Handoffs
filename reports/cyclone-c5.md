# Report: Cyclone C5 (checks, texts, small fixes)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: done (play checks pending)

## What changed

- `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.ForcedMove.cs` (+ .meta), new partial: `public void WakeMovedUnit(GUnit)`, one line over the existing private `WakeOne`. Wakes an Unaware unit exactly like a noise report on it (spread included). No-op for a unit that is not Unaware or when no level runs.
- `Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlSteps.cs` (new in tree, part of C1 commit 3): after `TryPull` starts a move, it calls the tracker found on the level's event bus (same lookup as `SleeperSightBeatSequence`). The Whirl and the Gust share this one pull, so both wake.
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs`: the Steer description constant matches the new text (a re-run would otherwise overwrite the asset).
- Texts (assets):
  - `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`: description, option A.
  - `.../Lucy_Ability_Steer.asset`: description as proposed (title unchanged).
  - `Resources/RunUpgrades/LucyCycloneWeak/RU_LucyCycloneWeak.asset`: description "...for 2 turns to every enemy it hits."
  - `Resources/Unlockables/UnlockableSet.asset`, entry `LucyCycloneWeak`: title "Howling Gale", description "Lucy's Cyclone applies Weak to every enemy it hits."
  - Cyclone Power: unchanged. Linda-folder copies and the Tempest Bloom lowercase "cyclone": untouched. Plain scalars, no escaping issue (apostrophe only).
- Tests (new): `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertForcedMoveTests.cs` (+ .meta), `Features/Player/Lucy/Scripts/Editor/CycloneHowlingGaleTests.cs` (+ .meta).

## Acceptance criteria

- [x] **A Cyclone pull wakes an Unaware enemy; no other wake rule changed.** Whirl and Gust both pull through `CycloneWhirlSteps.TryPull`, and the wake happens only when the move started. Tests: no-op cases (no level, null unit). **Play check** for the real wake (a full tracker needs a level, tag registry and unit attributes; the existing tracker tests don't build one either).
- [x] **Howling Gale lands only on enemies the Whirl hits, 2 turns.** Finding: the "radius-1 spread" is not in effect. `Lucy_Cyclone_Effect_WeakCompound` is `applyMode: Targeted`, `targetType: CellOccupant`, enemies only; `radius: 1` is ignored in Targeted mode (AEffectCompound `ResolveTargets`). So it already hits only the target of the Whirl hit, and no data change was needed. Its two effects (Weak tag `lifeTurns` 2, damage cut `durationTurnsSb` 2) are 2 turns. Tests (`CycloneHowlingGaleTests`) lock this in: targeted, occupant only, enemy only, no area shape, locked behind `_LucyCycloneWeak`, both durations 2. I set no radius to 0 because it would be dead data change.
- [x] **Weak applies under `CycloneHitContext`:** by reading. The wrapper forwards `ApplyStatAttributeModifiers`, `CalculateStatFactor` and the stat context to the cast; the nested compound only special-cases `statCtx is RuntimeAbility` for the John relay and the effect-performed event, both intentionally skipped. Unlock check uses the owner (`IsUnlockedFor(owner)`), and the owner passed is Lucy. No functional test (needs a faction tracker); **play check**.
- [x] **Watch fires on pulls (Gust on Lucy's turn, Whirl at enemy-turn end), within its own limits:** by reading. Pulls go through `AEffectPusher.TryMoveTo`, which raises `unitEndMoving` (`AEffectPusher.cs:186`); the bus maps that to `ActionFlowEvent.OnUnitEndMoving` (`GlobalEventBus.cs:172`), which Family Roles with that trigger (Watch) answer; their own activation phases and limits apply. The Steer and cast stay in progress until pulls land (C1b, C3), so the reaction comes after Lucy's action. Not unit-testable (role handler plus real pusher); **play check**.
- [x] **Command Shield Dash does not fire on a pull:** by reading `JohnPassiveAbility_CommandShieldDash.cs`. `OnUnitEndMoving` (:250) returns when `_commandInFlight == null`; it is set only on activation start of John's Command preset by an ally and cleared when that ability performs (:80). A Whirl (enemy turn end) or Gust (Lucy's own action) can't overlap a Command in flight. No bug found, no change.
- [x] Texts applied (D-544).
- [x] EditMode suite: 2015 run, 2014 pass, 1 fail = `AIRegressionTest.Baseline_MatchesCurrentAI` with **43 inner failures, 714 checks (unchanged from C4)**. The new tests are included and green.

## Save reset

no

## Decisions I made

- Wake at pull start (when the move starts), not on landing: the start is guaranteed, and the landing callback also fires on death.
- Put the new public method in a new partial file of the tracker rather than editing its files.
- Left `radius: 1` on the Weak compound: no behaviour effect, and touching the asset gains nothing.

## Needs THJ

none

## Docs to update

- `tech/core-systems.md`: `EnemyAlertTracker` is not listed there. The additive `WakeMovedUnit` could get a line in the Cyclone note (a Cyclone pull wakes Unaware enemies).
- `tech/combat-architecture.md` Cyclone section: pulls wake Unaware enemies; Howling Gale is a targeted Weak on the Whirl's hit target.
- Decision log: the Weak "spread" premise was wrong (it was already targeted).

## Risks and loose ends

- **Core touch:** `EnemyAlertTracker` (Core/Systems/EnemyAlertSystem): additive public method only, no existing rule or signature changed.
- A pull wakes the unit and spreads the wake to Unaware neighbours inside its alert range, the same as any wake. A Gust can therefore wake a pack through one pulled member. This is the existing spread rule; flag if THJ wants pulls to wake only the pulled unit.
- Wake happens at pull start, mid-Whirl; a woken unit in its own faction's turn gets its AP closed (existing rule), not relevant at the Whirl (enemy turn already over).
- The Weak is a fixed 0.6 damage factor; unchanged.
- The tracker is found with `bus.GetComponent<EnemyAlertTracker>()` each pull (cheap, a few units per Whirl).

## Proposed commits

Order from C4: **E1, A, A2, B, D1, C1 1–8, C, D2, D3, E2, E3**. C5 adds one commit and edits files that belong to earlier commits, which stays compilable as follows:

- **F (new, before C1 commit 3; core, additive):** `feat(core): the enemy alert tracker can wake an Unaware unit that a forced move by the player's side moved`. Files: `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.ForcedMove.cs` (+ .meta), `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertForcedMoveTests.cs` (+ .meta). Depends on nothing; inert on its own. Needed before C1 commit 3, because `CycloneWhirlSteps.cs` calls it.
- **C1 commit 3:** whole-file `CycloneWhirlSteps.cs` as it is now (includes the wake), and whole-file `Lucy_Cyclone_Ability.asset` (new description plus the earlier cooldown/radius values; the asset is inert text). Message can mention "pulled enemies wake".
- **D (C3's Steer commit):** whole-file `CycloneSteerSetup.cs` and `Lucy_Ability_Steer.asset` (+ .meta) with the new description; both are new files in C3.
- **G (new, last):** `chore(lucy): Howling Gale's text says it hits every enemy the Whirl hits, and the unlock list names the upgrade`. Files: `Resources/RunUpgrades/LucyCycloneWeak/RU_LucyCycloneWeak.asset`, `Resources/Unlockables/UnlockableSet.asset`, `Features/Player/Lucy/Scripts/Editor/CycloneHowlingGaleTests.cs` (+ .meta). The test depends on the Cyclone effect assets already in the repo (they are), so G can go anywhere after C1 commit 3.

Unity regenerates nothing else. Don't stage PreloadScreen, ProjectSettings or the TMP fallback font.

## Other branches

`thj/home-test` and `thj/onboarding` merge later with the redesign. The Memory 4 / Lucy memory onboarding check (in the plan's C5 line) was not part of this task and is not done.

## How to see it

1. Level with an Unaware enemy on one of the Cyclone's arms (2 cells straight out): cast the Cyclone. The enemy is pulled one cell in and wakes (wake pop); with Howling Gale it also takes the hit and Weak.
2. Steer so an Unaware enemy ends on an arm: the Gust pulls it and it wakes, with no damage.
3. Enemy not on an arm stays Unaware.
4. Linda in the lane of a landing cell: Watch fires after the Gust (Lucy's turn) and after the Whirl (enemy-turn end).
5. John adjacent to an ally in range of Shield Dash: a pull of an enemy shows no Shield Dash prompt; the prompt still shows during a Command move.
6. Howling Gale (Run upgrade): hit enemies show Weak for 2 turns; a neighbour that was not hit does not.
7. Read the Cyclone and Steer tooltips and the Howling Gale text in the run-upgrade list and unlock list.
