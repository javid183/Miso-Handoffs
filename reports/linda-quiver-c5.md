# Report: Linda's Quiver, C5 combat log lines

Plan: plans/2026-10-26-linda-quiver-tech.md (C5)    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 4a880f27c)
Outcome: done, not compiled or run. The editor is open, so nothing was compiled and no tests were run. THJ runs the tests below.

## What changed

Core (additive only, one unit):
- `Core/Systems/CombatLogging/Runtime/CombatLog.Custom.cs` (+ .meta): new partial with public `AddCustom(string category, GUnit unit, string text)`. It adds a `Note` entry whose text is "<category>: <text>", under the running action (like synergy notes) or at top level between actions. It is ignored outside a level, guarded like every handler, and knows nothing about the quiver.
- `Core/Systems/CombatLogging/Runtime/CombatLogFormat.cs`: new pure `Tagged(category, text)`.
- `Core/Systems/CombatLogging/Editor/CombatLogTests.cs`: case `Tagged_PutsTheCategoryInFrontOfCustomText`.

Quiver side (`Features/Player/Linda/Scripts/Quiver/`):
- `QuiverLogLines.cs` (+ .meta): pure text for every line.
- `QuiverLogListener.cs` (+ .meta): component on Linda that subscribes and writes through `AddCustom`. Added by `LindaQuiver.Start` next to the pips and return cue.
- `LindaQuiver.cs`: new event `OnSpent`, raised after the count drops; one added line in `Start` for the listener.
- `GroundedArrowField.cs`: event `OnArrowLanded(cell, amount, stackAfter)`, raised in `Land` before the instant pickup.
- `GroundedArrowField.Pickup.cs`: enum `ArrowPickupMoment {Walked, OnLanding, Revived}` and event `OnArrowsPickedUp(picker, cell, taken, leftOnTile, moment)`. `TryPickUp` now takes the moment.
- `GroundedArrowField.Recall.cs`: event `OnRecalled(returned, stacks)`.
- `Editor/QuiverLogLinesTests.cs` (+ .meta): 8 tests.

All files keep their existing line endings (LF, no BOM). No statics added, so no `PlayModeStaticReset` change. No prefab or asset edits. I did not touch the TMP fallback asset or the two ProjectSettings files.

## Acceptance criteria

- [x] One level played gives one log line per event: spend, each landing, each pickup, Recall, catch return, straight-back return, Watch prompt outcome, round start and level start each get exactly one line. Needs the verifier's play check.
- [x] `CombatLogTests` gets a quiver case: `Tagged_PutsTheCategoryInFrontOfCustomText` plus `QuiverLogLinesTests` (pure formatter).

## Sample lines (one imagined level)

```
--- Level: Level2-C1
Quiver: Linda starts with 4/4
[R1 Player] -- Player phase
[R1 Player] Quiver: Linda has 4/4 at round start, 0 on the ground
[R1 Player] Linda (3,4) › Bow Attack → DarkClaw #08-02
[R1 Player]   Quiver: Linda spends 1 on Bow Attack, 3/4 left
[R1 Player]   Quiver: arrow lands at (8,2), stack of 1
[R1 Enemy]  -- Enemy phase
[R1 Enemy]  ↳ Linda (3,4) › Family Role: Watch → ArcherGoblin #09-05
[R1 Enemy]  Quiver: Linda Watch prompt accepted with 3/4
[R1 Enemy]    Quiver: Linda spends 1 on Watch, 2/4 left
[R1 Enemy]    Quiver: arrow lands at (9,5), stack of 1
[R2 Player] -- Player phase
[R2 Player] Quiver: Linda has 2/4 at round start, 2 on the ground
[R2 Player] Mark (6,3) › Move
[R2 Player]   Quiver: Mark picks up 1 at (8,2) [walked], quiver 3/4
[R2 Player] Linda (3,4) › Encore
[R2 Player]   Quiver: Linda recalls 1 from (9,5) x1, quiver 4/4
[R2 Enemy]  -- Enemy phase
[R2 Enemy]  Quiver: Linda Watch prompt declined with 1/4
```

(Exact indentation depends on where the combat log files each note. Lines written inside an action sit under it, after its result rows.) Other lines: `Quiver: John picks up 1 at (2,2) [on landing], 1 left on the tile, quiver 4/4`, `Quiver: Linda picks up 1 at (1,1) [self, walked], quiver 2/4`, `Quiver: catch returns 1, quiver 4/4`, `Quiver: arrow had nowhere to land and goes straight back 1, quiver 3/4`.

## How each playtest signal is computed

Search a log for the prefix `Quiver:`. Round and phase come from the `[R# Phase]` tag on each line.
- Linda's damage share: already computable from existing lines. The level and mission summaries have a "Damage by unit" row; share = Linda / sum of the family's rows. Caveat: Duo damage is credited to the acting unit's frame, so Linda's part of Marks-Sisters may be counted under the other Bergson. Not changed here.
- Encore uses per level: count `Quiver: Linda recalls` between a `--- Level:` line and its `--- Level end:`.
- Declined Watch prompts with the count: lines `Watch prompt declined with N/4`. A decline "to save an arrow" is one with N between 1 and 3; N=0 can't prompt. Accepted ones read the same with "accepted".
- Arrows spent per shot type: count `spends 1 on <ability>` grouped by the ability title.
- Where arrows landed: `arrow lands at (x,y), stack of N`.
- Pickups: `<who> picks up N at (x,y) [how]`. How is `walked`, `on landing` (instant) or `revived`; `self,` appears when the picker is Linda. Other Bergsons picking up without being told = pickups whose name is not Linda.
- Mark's catch and return: `catch returns 1`. A failed catch shows as an ordinary landing (and Mark's catch itself has no line of its own).
- Quiver at each round start: `Linda has N/4 at round start, G on the ground`. "Empty or nearly so by round 2" = the R2 Player line with N <= 1 (pick your threshold) across levels.

## Save reset

No.

## Decisions I made

- The shot type is the title of the most recent ability started on the bus (cleared each turn), because the arrow projectile carries no source ability. This is right for the bow, Watch, Crescendo and the Duo trigger when the arrow spends in the same turn step. If an arrow ever spends with no ability started this turn, the line says "a shot". The verifier should check Duo and Watch lines name the right ability.
- Round-start lines subscribe to `turnStarted` from the level-started handler, not in `Start`, so they run after the combat log's own listener and sit under the right round header. If Linda is created after `levelStarted` fires, the round lines would be missing (the other lines still work).
- Recall and Pickup returns have only their detailed line (the generic return line skips them) so nothing is logged twice.
- A landing that goes straight into a Bergson's own tile logs the landing and then the pickup `[on landing]`.
- No level-end quiver line: the combat log closes the level before a later listener would run, and the last round-start line covers the signal.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`: the quiver's log lines and `CombatLog.AddCustom`.
- `build-log.md`: C5 entry.

## Risks and loose ends

- Not compiled. First thing: let Unity recompile and check the console. Likely trouble spots are using-directives in `QuiverLogListener` (`FactionRoleHandlerBase` and `RuntimeAbility` are in `MISO.Core.Systems.AbilitySystem.Abilities`, `Faction` in `MISO.Core.Units.Factions`).
- `AddCustom` is a new public method on a non-core class; it is additive.
- The `Note` kind has no dedicated JSON kind, so balance scripts filter on `kind=Note` plus `detail` starting `Quiver:`.

## Proposed commits

1. `feat(combat-log): AddCustom lets other systems write tagged lines`: `Core/Systems/CombatLogging/Runtime/CombatLog.Custom.cs` + .meta, `CombatLogFormat.cs`, `CombatLogTests.cs` (plain, additive; own unit)
2. `feat(linda): quiver events for the combat log`: `LindaQuiver.cs` (the OnSpent event only; commit its listener line with unit 3 if split by hunk is awkward), `GroundedArrowField.cs`, `GroundedArrowField.Pickup.cs`, `GroundedArrowField.Recall.cs` (plain)
3. `feat(linda): quiver combat log lines`: `QuiverLogLines.cs`, `QuiverLogListener.cs`, `Editor/QuiverLogLinesTests.cs` with their .meta, plus the `LindaQuiver.cs` listener line (plain). Units 2 and 3 can be one commit since `LindaQuiver.cs` has both changes.

## Other branches

`thj/home-test` and `thj/onboarding` when the quiver lands on main.

## How to see it

1. Let Unity recompile; check the console is clean.
2. Test Runner > EditMode: run `MISO.Core.Features.Bergsons.EditorTests.QuiverLogLinesTests` (8 tests) and `MISO.Core.Systems.CombatLogging.EditorTests.CombatLogTests.Tagged_PutsTheCategoryInFrontOfCustomText`; then Run All (only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` may fail).
3. Play a combat level with Linda, with "combat log to file" on in the global settings (or open the Combat Log window from the Tools menu). Fire the bow, accept a Watch, decline one, walk Bergsons over arrows, use Encore, let Mark catch one.
4. Search the log for `Quiver:` and compare each line with what happened. Check the round-start line sits under its `-- Player phase` header and spend lines name the right ability (bow, Watch, a Duo).

## Review fixes

1. Start line: `QuiverLogListener` no longer writes "starts with N/4" in the level-started handler. It writes it once (`_startWritten`) at the first turn start after the level starts, so the log has opened its level.
2. Commit units, replacing "Proposed commits" above:
   1. `feat(combat-log): AddCustom lets other systems write tagged lines`: `CombatLog.Custom.cs` + .meta, `CombatLogFormat.cs`, `CombatLogTests.cs` (additive, first).
   2. `feat(linda): quiver events and combat log lines`: `LindaQuiver.cs`, `QuiverArrow.cs`, `GroundedArrowField.cs`, `.Pickup.cs`, `.Recall.cs`, `QuiverLogLines.cs`, `QuiverLogListener.cs`, `Editor/QuiverLogLinesTests.cs`, with their .meta. One commit, since `LindaQuiver` adds the listener.
   The four new .meta files (`CombatLog.Custom.cs`, `QuiverLogLines.cs`, `QuiverLogListener.cs`, `QuiverLogLinesTests.cs`) were written by hand: stage them only after Unity has recompiled, in case it rewrites them.
3. Per-frame cost: `Update` removed. The listener rebinds to a replaced field lazily (`ReferenceEquals(GroundedArrowField.Current, _field)`) in `OnSpent` and at each turn start.
4. Shot naming: `QuiverArrow.Start` reads `_projectile.StatAttributesContext as RuntimeAbility` and calls `LindaQuiver.Spend(RuntimeAbility source = null)` (existing no-argument calls still compile). `OnSpent` is now `Action<LindaQuiver, RuntimeAbility>`. The listener names the shot from that ability's title; the abilityActivationStarted subscription and the "most recent ability" state are gone. Falls back to "a shot" when there is no source. This replaces the earlier decision on shot type. The verifier should still check the Duo and Watch lines.
5. The core test case uses neutral text ("Tag: some text").

Plan note: the plan names `Core/.../CombatLog.Quiver.cs`; the real split is a generic `CombatLog.AddCustom` in Core (`CombatLog.Custom.cs`) and the quiver's listener and words in `Features/Player/Linda/Scripts/Quiver/`. Still not compiled (editor open).
