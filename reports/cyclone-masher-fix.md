# Report: Masher stops behind the Cyclone (cyclone-masher-blocked)

Plan: bug brief from the coordinator (status.md Inbox `cyclone-masher-blocked`; round 2 plan `plans/2026-11-17-cyclone-round2-tech.md` C3a to C3c, D-550)    Agent: miso-implementer    Branch: thj/cyclone
Outcome: **blocked (stopped as instructed: the fix needs a core grid change).** Repro test written and proven red for the cause below; no game code changed.

## Root cause (with evidence)

The hypothesis is right about the symptom but the Masher filter is not the only refusal. **Every "can this unit end its move here" check goes through `GridPluggableEntity.IsFootprintEmpty`, which uses `GridCell.IsWalkable`, and the Cyclone's cell is never walkable for stopping.** C3a deliberately kept that rule ("heavies pass through but cannot end on it"; tests in `CycloneHeavyPassTests` assert it). The C3a plan assumed "it bursts on entry, so it is gone", but the stop checks run *before* the step, while the Cyclone is still planted (and the burst keeps it planted 0.3 s for the ring anyway).

So a 2x2 heavy can only burst the Cyclone if one walk carries its footprint over the Cyclone *and off it again*. Crossing a 1-cell Cyclone along x takes a 2x2 three steps (origins 10 and 9 both cover x 10). With SPD 1 (Masher walk radius 1, read from the real prefab) that is impossible, so it never steps toward the target and never bursts.

Evidence (real `Unit_MasherGoblin` prefab, its real walk `MasherGoblin_Ability_Walk`: PathWalkable, Adjacent, radius 1, ignore Ally; THJ's cells: Cyclone [10,-2], Linda [8,-1], Masher origin [11,-2]), from a temporary diagnostic test, since removed:

| Layer (all through `IsFootprintEmpty`) | File (core?) | Result for origin [10,-2] |
| --- | --- | --- |
| Pass check `IsFootprintWalkable` | `GridPluggableEntity.cs` (core) | True: C3a pass works |
| Stop check `IsFootprintEmpty` | `GridPluggableEntity.cs` (core) | **False** |
| Walk range `ComputeTargetSelectionCells` → `GetRangeCellsBFS` final `PassesEmptyFilter` | `GridCell.cs` (core) | **Dropped**: range = only [11,-3] |
| Masher planner filter `Unit.IsFootprintEmpty(cell)` | `MasherGoblinFactionRoleHandler.Counter.cs` | **Dropped** (redundant with the range) |
| `FindPathTo(dest, mover)` goal check | `GridActions.cs` (core) | **null path** |
| Transporter last-step check `i == path.Count-2 && !IsFootprintEmpty` | `AEffectTransporter.cs` (core) | would stop the walk on the cell before |
| Walk feasibility | | True (not Crippled) |

`TryPlanAnswer(linda)` returns false: no answer, no burst. Without the Cyclone the same plan picks origin [10,-2] (control test passes).

The same root applies to (by reading):
- **Masher/Goblin Queen normal AI turns:** `AIUnitBrain.cs:424` filters candidates with `_unit.IsFootprintEmpty(c)`, and the move range is the same BFS. So a heavy's AI move never ends with its footprint over the Cyclone. The C3c end-of-turn danger exemption works, but it cannot help here.
- **Goblin Queen's charge:** a Transporter walk, with the same range, goal and last-step checks. It bursts only when the charge's path goes fully past the Cyclone, never when it would end on it.
- Also `AEffectCommand.cs:185` (last step), `AreaShapeDefinition.cs:149` (SelfWalkable), `PlayerController.cs:1431`, the Masher hover preview (`MasherGoblinFactionRoleHandler.cs` `GetCellsInRange`).

## The exact minimal change I'd suggest (core, needs the coordinator / THJ)

**Option A (recommended): one core rule, in two grid files.** A planted entity may say it clears out of the way for a given mover, and the stop check counts such a cell as empty for that mover.

`GridCell.PlantedPass.cs` (core, additive):
```csharp
// A planted walk blocker that a given mover may end its move on, because it leaves when that mover enters (Lucy's
// Cyclone bursts under a heavy unit). Worker-thread safe: plain fields and references only.
public interface IPlantedClearsOnEntry
{
    bool ClearsOnEntry(GridPluggableEntity mover);
}

// True when the only thing stopping `mover` from ending on this cell is a planted entity that clears for it.
public bool PlantedClearsFor(GridPluggableEntity mover) =>
    ReferenceEquals(StashedEntity, null) && !IsOccupied
    && _plantedEntity is IPlantedClearsOnEntry clears && clears.ClearsOnEntry(mover);
```
`GridPluggableEntity.IsFootprintEmpty` (core, one line):
```csharp
if (!c.IsWalkable && !c.PlantedClearsFor(this)) return false;
```
Cyclone side (not core; a new partial, e.g. `CycloneEntity.ClearsOnEntry.cs`, so the round-3 files are not touched):
`ClearsOnEntry(mover) => IsAlive && !HasBurst && CycloneHeavy.IsHeavy(mover, pullTagQuery)`.

What it fixes in one place: the walk range, the Masher planner filter (so **no Masher code change is needed**), the path goal, the Transporter and Command last steps, the AI candidate filter (Masher and Queen normal turns), and the Queen's charge destination. The burst already fires on the plug (`PlugEntityInternal` → `Activate`), and a unit's `CanOccupy` ignores the planted slot, so the heavy plugs on, bursts it, and the Cyclone is disposed after the ring.

Not changed by it: `IsWalkable` and `FootprintHasWalkBlocker` stay as they are. So ranged reach (jumps, blinks), the dash approach cell and the Mark–Linda loser stop still never end on the Cyclone. Non-heavies are unaffected (`ClearsOnEntry` false). The family is unaffected too: the family is not an enemy of the caster, but `IsHeavy` doesn't check faction, so the Cyclone should add `&& mover is an enemy of the caster` (the same rule `BurstsOn` uses). Otherwise an Immovable or large *family* unit could end on its own Cyclone without bursting it.

**Option B (narrower, more files):** leave `IsFootprintEmpty` alone and add a mover-aware stop check only in `GetRangeCellsBFS` (`GridCell.cs`), the `FindPath` goal (`GridActions.cs`), the Transporter last step (`AEffectTransporter.cs`) and the Masher filter. That is three core files plus the AI candidate filter (`AIUnitBrain.cs`) for normal turns. I don't recommend it: more core surface, easy to miss a caller.

## What changed

- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterCycloneTests.cs` (+ `.meta`, new, LF, no BOM): the repro, through the real planner by reflection on the private `TryPlanAnswer(GUnit, out GridCell, out bool)`, so no code seam was needed. It uses the real Masher prefab (an isolated `LoadPrefabContents` copy, light init, `_walk` set to its real walk) on THJ's exact level coordinates (mapped onto a test board by an offset).
  - `TheCounterStep_TowardATargetPastTheCyclone_WalksOntoTheCyclone`: **red** for the cause above ("the Masher plans a step toward Linda; expected True, was False"). It is marked `[Ignore("Waits for the grid's stop rule to let a heavy end a move on the Cyclone it bursts")]` so the suite stays green. Remove the `Ignore` when the core change lands.
  - `TheCounterStep_WithoutACyclone_IsTheSameStep`: green control (same board, no Cyclone, picks origin [10,-2]).

No runtime file touched: no core, no Masher script, no Cyclone presenter file. THJ's PreloadScreen, ProjectSettings and TMP font untouched.

## Acceptance criteria

- [x] Failing repro through the real planner with THJ's cells, SPD and footprint, failing for the proven reason: see above (red, now `Ignore`d).
- [ ] Heavy may choose a destination covering a live Cyclone: **not done**, needs a core change (Option A).
- [ ] Non-heavies still refused: unchanged today; with Option A guaranteed by `ClearsOnEntry` (heavy enemy only).
- [x] AI end-of-turn / destination filters and the Queen's charge checked: same root (`IsFootprintEmpty`), fixed by the same core line. Not fixable in Masher or Cyclone code alone.

## Test run

Full EditMode suite (MCP, editor open, not in Play mode): **2156 run, 2154 passed, 1 failed, 1 skipped.** The failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner `CHECKS: 714 FAILURES: 43` (unchanged). The skip is the ignored repro. Compile clean.

## Save reset

No.

## Decisions I made

- Reflection on the private planner instead of an internal seam: it has the same effect and needs no game-code edit. Tier 1.
- Repro left in, but `Ignore`d, so the suite stays green until the core change lands. Tier 1.

## Needs THJ

1. **What:** let a heavy enemy *end* a move with its footprint over a live Cyclone (it bursts it on entry), through the core stop check `GridPluggableEntity.IsFootprintEmpty` (Option A).
2. **Why:** with the current rule, a 2x2 heavy needs SPD 3+ to cross a Cyclone and burst it. The Masher (SPD 1) never can, and AI heavies never end a move on it either. That breaks D-550 in practice.
3. **Options:**
   - A: one core line plus an additive interface (recommended).
   - B: mover-aware stop checks in three core files plus the AI.
   - C: keep the rule (heavies burst it only when they cross completely). The Masher then stays stuck as THJ saw.
4. **Rule change it implies:** CR-58 / LU-7 wording changes from "heavies pass but can't stop on it" to "a heavy may step onto it; it bursts". Some C3a and C3c tests that assert the old rule flip and must be updated with the fix: `CycloneHeavyPassTests` (lines ~156-157, 171, 191) and `CycloneAIHeavyTests` ("the heavy's move range never contains the Cyclone cell").
5. **Jump question:** with Option A, a heavy *jump* whose target selection uses the walk range or SelfWalkable shapes could land on the Cyclone and burst it (D-557 says a jump never bursts it). Ranged reach stays protected by `FootprintHasWalkBlocker`. If D-557 must hold strictly, the jump path needs a check. Please confirm.

## Docs to update

- After the fix: `tech/core-systems.md` Grid row (new `IPlantedClearsOnEntry`, `IsFootprintEmpty` consults it); GDD CR-58, LU-7, EN-2/EN-6 (designer).

## Risks and loose ends

- In the repro board the Masher's walk range held only [11,-3] (not [12,-2] or [11,-1]). Its own footprint cells on the hand-built board may read oddly to the BFS. This doesn't affect the finding (the step toward Linda is refused by the stop check, shown directly), but worth a look when the fix test turns green.
- With SPD 1, the step onto the Cyclone leaves the Masher 2 cells from Linda, so it bursts the Cyclone but does **not** slam this answer. THJ's expectation "and attacks" only holds if the target is adjacent after the step.
- The Masher planner's own `IsFootprintEmpty` filter is redundant with the walk range. Leave it; it follows the core rule automatically.

## Proposed commits

1. `test(masher): the counter step toward a target past Lucy's Cyclone, waiting on the grid stop rule` (plain): `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterCycloneTests.cs` + `.meta`. Better committed together with the core fix, once it is approved, with the `Ignore` removed.

## Other branches

None.

## How to see it

1. Test Runner, EditMode: `MasherCounterCycloneTests`. The control test is green and the repro shows as ignored. Remove the `Ignore` attribute to see it fail with "the Masher plans a step toward Linda".
2. In play (`LevelE3-C1`, Lucy and Linda), the current behaviour is unchanged: the Masher stops behind the Cyclone.
