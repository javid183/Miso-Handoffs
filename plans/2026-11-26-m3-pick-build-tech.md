# M3 "Hold the yard": the pick and the opening, on the round-two layout (build)

Size: L    Tier: 3 approved (core hook D-748); the rest Tier 2 inside the approved design    Assigned to: miso-implementer (8.1–8.3 opus, 8.4 sonnet)
Branch: all (THJ is on `main`)
Status: approved, building

## Why

THJ's correction (D-739, D-741): his play note asked that the **pusher** (John or Mark) stays pushing and out of combat, not for Mark to be placed. Keep the round-two layout as built (7.1, uncommitted, verified: `reports/onboarding-m3-round-two.md`). Bring back the opening fight, the squad pick and the walk to the stone. Design: `plans/2026-11-26-m3-pick-and-opening.md` (block `m3-defence-4`, gate 7 checked), with THJ's answers D-742..D-745 and D-748..D-750. Tier 2 calls: D-751 and D-752. Code facts: `reports/2026-11-26-m3-pick-hold-code-read.md` (read it, it has the line numbers).

## Goal

M3 plays like this:
1. "Clear the yard.": 3 Claws at the stone, w1 marching in the west lane.
2. "{pick}: push the stone.": the pick walks to 4,11 and the Masher is revealed.
3. Three hold turns. The pick is held, fully out of combat, and the stone moves one notch per family turn (w2 comes at notch 1, w3 at notch 2, and the pick is released at notch 3 with a full turn).
4. "Finish them."
5. The outro and Toba.

The pick falling loses the level at any point.

## Acceptance criteria

**8.1 · Core: per-unit Family Role suppression (opus; own review; full suite)**
- [ ] `FactionRoleHandlerBase` gets an additive public API to suppress and unsuppress one unit's Family Role at runtime, for example `SetSuppressed(object owner, bool on)` or a suppression count, plus `IsSuppressed`. A suppressed handler never triggers: `CheckFeasibility` or `CheckActivationMoment` returns false. This covers John, Linda, Lucy, Mark and the Masher through the base. Nothing changes unless code calls it: same behavior, same serialized data.
- [ ] `PlayerController.SuperTimeUnits` (line 35) skips units whose handler is suppressed.
- [ ] State lives on the instance. If any static is needed, it gets a `PlayModeStaticReset` hook.
- [ ] Code the AI worker thread can reach stays free of Unity-object APIs.
- [ ] EditMode tests: suppressed → no trigger and not in Super Time; unsuppressed → back to normal; default → unchanged.
- [ ] Full EditMode suite green.
- [ ] Update `tech/core-systems.md`: the implementer drafts the line in the report, and the coordinator writes it.
- [ ] Commit unit: core only.

**8.2 · Holding the pick out of combat (opus; reviewed with the feature)**
- [ ] `Features/Levels/AbilityLock/LevelAbilityLock.cs` (not core): an additive runtime `Lock(...)` (unit nickname + presets) that raises `Changed`, the mirror of `Unlock`. `HiddenFromBar` then hides the partner's Duo button, as it does for an Awake lock (D-751).
- [ ] `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (not core): no catch and no catch preview while the catcher is turn-skipped (held). It must work for `TryCatch`, `CatchSweep` and `WouldCatch` (D-751).
- [ ] `Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs` (not core): re-enabling refreshes (`_set` reset or re-evaluated), so the shelter returns at release if Lucy still stands next to John (D-751).
- [ ] `Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` (not core): a suppressed role shows a not-ready badge state, never Ready (D-755).
- [ ] New Onboarding component (for example `Features/Onboarding/HoldPickOutOfCombat.cs`), driven by `SignalAction` steps. It finds the pick at runtime (`PickOnTilesLOCondition.IsPick`, or the unit on the push tile).
  - **Hold():**
    - `HoldUnitsUntilSignal` on the pick. Add the component at hold time, or keep it disabled until then: the code read explains why an empty-list `Hold()` blocks later holds.
    - Persistent tags `EntityState.Unmovable`, `EntityState.Unable to Swap` and `EntityState.IgnoreObjective`.
    - Role suppressed (8.1).
    - Role zone hidden through `IRoleZoneVisibility`.
    - Duos locked both ways (8.2 `Lock`).
    - Lucy's Papa's Shelter off, if the pick is John.
  - **Release():** undoes each of these. The pick gets full AP that same family turn (`HoldUnitsUntilSignal.Release`, code read item 6).
  - Idempotent. Safe if the pick is dead. Unsubscribes on disable. Worker-thread guard on any event handler.
- [ ] EditMode tests for the component (hold/release toggles every item; dead pick; double call) and for the three feature changes.
- [ ] Commit units: the three feature-file changes can share one commit ("a held unit doesn't catch, shelter or Duo") or go one each. The Onboarding component goes in its own commit.

**8.3 · M3 rewired to `m3-defence-4` (opus; reviewed with the feature)**
- [ ] **Layout kept:** the built `GB_m3-defence.prefab` from 7.1 isn't rebuilt from scratch. Change only what `m3-defence-4` changes:
  - 3 Dark Claws on 3,11, 4,11 and 5,11, in play at the start;
  - the `Unit_Placeholder` deploy slot on 4,8;
  - Mark is no longer placed on 4,11;
  - the Masher is hidden at 6,1 until the push (D-743).
  - Everything else stays as built: barricades, w1 in play, w2/w3 hidden, mushrooms, the Sword, the Stranger stone on 4,12, Toba hidden.
  - The read-back must match block `m3-defence-4` (`claude-handoff/tools/level_to_grid.py`).
- [ ] **Roster:** `M2 - The Trail.asset` `freeSlotsCount` goes back to 1, with fixed seats Linda and Lucy. Revert 7.1's roster test changes accordingly.
- [ ] **Mark's 7.1 instance data is gone:** Role off, Duos locked, IgnoreObjective, the Mark hold, `MissionWiring.HoldTheYard.Mark.cs`. Drop `holdFromLevelStart` and its tests (D-752); `HoldUnitsUntilSignal.cs` goes back to HEAD unless 8.2 needs a change.
- [ ] **Stages, per the design plan § 3:**
  - S1 "Clear the yard." (the 3 alcove Claws dead; w1 doesn't count).
  - S2 "{pick}: push the stone." (the pick on 4,11, lit as a goal, like the old greybox's S2). Its end does three things: hold the pick (8.2), reveal the Masher with its close-up, and play M3.0.3–0.5.
  - S3–S5: three hold turns, one notch at each family turn start (`TurnReachedLOCondition turn=1`, as in 7.1).
    - S3: w2 comes in.
    - S4: w3 comes in.
    - S5: the stone rolls away and the pick is released.
    - Countdown texts "3 turns left", "2 turns left", "Last turn.".
  - S6 "Finish them.".
  - Outro as built (tally, Toba).
- [ ] **Loss:** the pick falling loses from level start, via `PickFallenLOCondition`, with the shown objective "Keep {pick} standing.". The defeat line "{pick} has fallen." is 8.4's. If `{pick}` can't show in a defeat objective (T-P4), report it and use the plain text.
  - The template defeat ignores the pick only while held (runtime IgnoreObjective).
- [ ] **Stone notches:** 3 hold notches, not 4. Say which stone variants are used, and whether `Unit_Rock_Stone4` is still needed (drop it if unused).
- [ ] **Idempotent:** a second `Apply Wiring` gives md5-identical files.
- [ ] **Tests:** `M3DefenceTests` updated to the new block, stages, roster and loss. `OnboardingMissionGraphTests`, `SearchTrailTests` and `PickOnTilesLOConditionTests` go back to the free seat. Covering fixtures green.
- [ ] **Report on:** T-P2 (the Masher's 2×2 reveal when a cell is taken), T-P4, T-P5 (Chained Assault range measured from Lucy), and whether enemies attack an Inactive unit. All from reading the code.

**8.5 · Core: big units can walk north and east (opus; own review; full suite; AI regression by name)** (D-758, from THJ's play check; `reports/2026-11-26-masher-stuck-code-read.md`)
- [ ] `GridCell.GetRangeCells`: for walk modes (PathWalkable/SelfWalkable) with a multi-cell source and `includeSelf` off, remove only the anchor cell, not every occupied cell. The Unconstrained branch (attack ranges) is unchanged. Behavior for 1×1 units is identical.
- [ ] A destination overlapping the mover's own footprint is accepted end to end: `IsLegalAbilityTarget`/`OccupantIntersects`, the transporter's `FindPath(mover)`, and the AI `CanEndOn`.
- [ ] The AI next-targets prediction (`AIUnitBrain.cs:291-318`) agrees with the live range for a 2×2 unit, or the gap is reported.
- [ ] EditMode tests: a 2×2 radius-1 unit reaches its N, E, S and W anchors where the cells are free; a 1×2 unit likewise; 1×1 is unchanged.
- [ ] Full suite green. AI regression by name compared with 51 (it may move: the Masher's and Queen's walks change; no re-baseline).
- [ ] `tech/core-systems.md` line (coordinator).
- [ ] Commit unit: core only, before commit 4.

**8.4 · M3 lines (sonnet)**: apply `design/m3-text.md` once THJ's revision is approved (D-749, D-750): the per-pick text option for John's push line, the level-start line, the west-wall pair fired when w1 reaches the west wall (D-753), the countdown, "{pick} has fallen." (loss-panel plumbing if it's needed and stays in Onboarding/UI non-core; if it needs core, stop and report). Planned separately when 8.3 is in.

## Risks

- **New statics:** 8.1 should have none. Any static needs a `PlayModeStaticReset` hook.
- **AI thread:** the suppression flag may be read during planning. Use a plain field, no Unity APIs.
- **AI regression:** unit prefabs aren't changed by 8.1/8.2. 8.3 changes level content only. Run the test by name at the end and compare it with 52 (7.1's count). Expect `Unit_Rock_Stone4` to drop out if it's removed. Don't re-baseline.
- **Event subscriptions:** the hold component unsubscribes on disable. A level abort mid-hold must not leave tags behind, since they're runtime-only on a level unit.
- **The Masher reveal footprint taken (T-P2):** report it; don't fix it in this chunk.
- **Unfiltered pushers** (Queen, Deev, John taunt, Mark vault, Whirl): none of those enemies are in M3, so no change.
- **Other branches:** none active. The work goes on `main`.

## Test plan

- 8.1: new core tests plus the full suite.
- 8.2/8.3: covering fixtures (`MISO.Core.Features.Onboarding`, `MISO.Core.Levels`, the AbilityLock tests, the Mark and Lucy feature tests if present).
- At the end: one `miso-reviewer` pass on 8.2+8.3, then `miso-verifier`: compile, full suite, the AI regression by name.
- Gate 7: read back the prefab against `m3-defence-4`.
- THJ plays M3 from a cleared save, with John and with Mark.

## Docs to update

- `tech/core-systems.md` (coordinator, 8.1).
- `design/m3-text.md` (narrative).
- After the play check: d3 paper levels § M3, the GDD missions-structure M3 row, level-chunks (designer); `tech/onboarding-merge.md` (coordinator).

## Proposed commits (after THJ's play check)

1. `feat(core): a unit's Family Role can be suppressed at runtime` (8.1)
2. `feat: a held unit doesn't catch, shelter or join Duos` (8.2 feature files)
3. `feat(onboarding): hold the pick out of combat` (8.2 component)
4. `feat(onboarding): Hold the yard round two: barricades, lanes, the Masher in the east lane, the pick held on the stone` (7.1 + 8.3 assets and wiring)
5. `feat(onboarding): M3 lines` (8.4)
