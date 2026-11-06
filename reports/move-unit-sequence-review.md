# Review: `MoveUnitSequence` fix and wiring tool retirement (2026-11-06)

Reviewer verdict: **FIX**. Read from the code; nothing played. The reviewer can't write files, so the coordinator saved this condensed copy.

## Must fix

1. `MoveUnitSequence.cs:42-43`: the tile lookup can pick a dead unit, because `GUnit.DieInternal` doesn't clear `CurrentCell`. The move then silently does nothing, and the live unit stays put. It also misses big units named by a non-origin tile. Fix: `unitCell.OccupantEntity as GUnit`.

## Should fix

1. `Radius = int.MaxValue` overflows `Radius + 1` at `AEffectTransporter.cs:66` and `:153`, so a Walk transporter with `ignorePathCost` can never move through this sequence. Not reachable with current data. Fix: `int.MaxValue - 1`.
2. `MoveUnitSequenceTests.cs` is in the global namespace; siblings use `MISO.Core.Levels.EditorTests`.
3. Tests stop at the picker; the pre-check and tile lookup are uncovered, though other tests build grid objects in edit mode.
4. Cosmetics in `MoveUnitSequence.cs`: unused `using`, stray blank line, trailing whitespace.
5. `HearthMemoryWiring.Mark.cs:19-21`: the summary still describes a re-runnable tool.

## Verified

- Every early exit ends normally and the parent sequence advances; no hang from them.
- The pre-check agrees with `Apply` for Walk (same path search and cost test).
- `CanOccupy` can't cancel a Walk move that used to work, and it's the same test `PlugEntityInternal` uses for Teleport and Jump. The 8 existing assets aren't affected.
- A cancelled move never calls `GotTargeted` on the occupant.
- No new statics, not on the core list, LF with no BOM, no private IDs, no references to the removed menu path in code.

## Open notes

- **Possible lock, pre-existing:** the `WaitWhile` on `IsInProgress` reads a flag on the shared transporter asset; a mover deactivated mid-walk leaves it true forever. The fallback now exposes shared Claw transporters to this.
- `AEffectBase.CheckApplyConditions` is private, so a failing tag query still makes the move silently do nothing, without a hang.
- The fallback has no Walk preference because `moveMode` has no accessor (core, THJ's call). Safe on current data.
- A run-unlocked ability at `_upgradeLevel` -1 would throw in the fallback scan. Only matters if an enemy faction gets run unlocks.
- `plans/onboarding/2026-11-05-m4-mark-rework-tech.md:46` still names the retired tool as the way to build the level.

## Needs a play check

- The Claws at 6,4, 0,4 and 3,7 are found after `PostBloom_Reveal`.
- `ClawMove2` moves when the 3,5 Claw is dead; otherwise it warns and the chain continues.
- Whether a dying Claw can still be on a looked-up tile during the Bloom.
- The walk animation on Claws, and that the `End_*` and `JohnMove` destinations are reachable.
