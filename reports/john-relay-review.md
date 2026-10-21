# John relay J-B, J2, J3 review (miso-reviewer, 2026-10-21; saved by the coordinator)

Verdict: **FIX**

## Must fix

1. **The Goblin Queen's charge is not seen as an area attack.**
   - Where: `FamilyRoleRelay.IsAreaAttack` / `HoldsArea` (~:60-90) and `JohnFactionRoleHandler.AreaUnitsOf` (~:86-108).
   - Why it's missed: the charge is Targeted (targetType Cell|CellOccupant). Its Surrounding compounds sit inside an `AEffectTransporter` (on-tile, end-tile and movement-end effects), which `HoldsArea` doesn't look into. `ComputeAffectedCells` can't see the path either.
   - With an empty target cell: nothing is relayed.
   - With an ally on the target cell: the single-target `RetargetToJohn` cell-drop rewrites the destination, so the Queen charges at John.
   - Options (THJ's call):
     - (a) Look inside transporters and build the covered set from the path. Needs a ruling: per-tile compounds can hit John more than once.
     - (b) Leave the charge out of J-B, but never rewrite a cell target the attack uses as its move destination (John added as an extra target, as before J-B).

## Should fix

1. **J3 End Turn** (`PlayerController.cs` ~:1491-1499): the answer's `abilityStarted` refresh can still enable End Turn mid-answer once the flag is cleared. Gate End Turn on `OtherFactionActionInProgress()` (within D-125's intent).
2. **Delayed `NotifyStateChange`** (~:1495): guard against a destroyed `CombatLevelUIManager.Instance` with a Unity null check.
3. **Tests:** no test for `IsAreaAttack`. Add one with a Targeted preset whose transporter holds a Surrounding compound.
4. **Record lifecycle:** clear relay records explicitly at level end. Harmless today, since a liveness check stops stale records applying.

## Confirmed

- The D-120 filter (one swap, covered allies spared, John's natural hit counts as his one hit, no relay when John is the primary target).
- The hook in `ApplyUnguarded` is a no-op without a record. Previews and AI never call `Apply`, so the golden master shouldn't move.
- Record lifecycle: completion, liveness, Play-mode reset.
- Masher slam, Masher answer and Queen strike are detected. Multi-compound: John takes the first swap only.
- Both J-A notes folded in.
- J2: the reduction refreshes by id `JFR_DR`, never stacks, and the tests prove it.
- J3: the flag is cleared only when the role set it; the time-scale restore is correct in all four cases; other QTEs are unchanged.
- Line endings: every modified file is CRLF, as at HEAD; the report's "LF kept" is wrong in the report only.
- Commits separable (J-B 7, J2 2, J3 1); nothing out of scope.

## Design point for THJ

John's +0.5 reduction lasts until the start of the next player phase. A relay on the player's turn (a Masher answer) therefore keeps it for the whole next enemy turn.
