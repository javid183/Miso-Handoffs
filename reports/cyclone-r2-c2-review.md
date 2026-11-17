# Review: Cyclone round 2, C2 (carry), branch `thj/cyclone`, uncommitted

Reviewer: `miso-reviewer` (saved by the coordinator). Verdict: **FIX**. EditMode not run by the reviewer (the implementer's run: 2046/2047, known red only, count 43).

## Must fix

1. **Watch on a carried enemy fires after the Whirl's pull, not before it; if a pulled enemy also qualifies, the carried enemy's Watch is dropped.** `CycloneEntity.Steer.cs:97-107`, `AEffectCycloneSteer.cs:92-93`, `CycloneSteerRules.cs:53`. The landing raises `unitEndMoving` while the Steer's action is still open (`SteerActionOpen` is true through glide, landing and pull). Linda's role is `WaitForProcessesToComplete`, so `FactionControllerBase.ApplyFactionRolesIfPossible` only queues the landing; the queue is processed on `ActionsProgressComplete`, after the pull; `ProcessFRApplyWaitList` walks newest to oldest, fires the first feasible entry and clears the list. So the pulls' entries are tried first. Breaks "carried land (Watch, hazards), then pull, reactions, hit". Tests miss it (recorder has no Family Roles).
   Fix, in Cyclone code: when at least one enemy landed, close the Steer action right after the landing, not after the pull; the Steer's Whirl waits for `ReactionsSettled()` before it pulls; the pull then runs outside an action like the end-of-turn Whirl's; update `SteerActionOpen` and its cases; add a test: after a landing, the pull waits while reactions are unsettled.

## Should fix

1. `CycloneEntity.Steer.cs:191`, `:207`: putting riders back on their start cells (`Land(false)`, `Abort`) re-fires the start cell's hazard via `GridCell.PlugEntity`. Before `TakeOff`, check the end cell is free or held only by a rider about to leave; if not, skip `TakeOff` and `Land`.
2. `CycloneSteerTests.Carry.cs:234`: `if (around != null)` makes the assertion optional; assert definitively whether (3,2) is reachable and by which first step.
3. `HarmonicSlamThenACarry_CrippledDealsNothingOnTheWay` cannot fail for the reason it names (the recorder involves no pusher); rename it as a data-path guard or drop the redundant half. The 15 to 16 number stays a play-check item.

## Notes

- Carry order and rules match design section 3; unplugged-unit safety holds (riders keep cells during the glide; `TakeOff`/`Relocate`/`Land` in one frame; `finally` handles a throwing landing); events match the pusher (`unitStartMoving`, `unitEndMoving`, `WakeMovedUnit`); hold/watchdog unchanged; no core file edited; `.meta` present; no private IDs, no "Gust".
- Cells past a blocked front enemy reached another way: not a contradiction of the design (its failure case says "the Steer can still go other ways"); put to THJ at play; C4's preview must draw the detour path clearly.
- Check at play: hovering or clicking an enemy standing on a newly offered cell aims the Steer and does not open a unit hover or attack cursor. Riders' facing is not changed (cosmetic).
- **Core limitation (Tier 3 if it must change):** `ProcessFRApplyWaitList` fires one queued Watch per action and clears the rest, so "the Claws ride into Linda's row, Watch fires twice" will not happen within one action; several riders landing together get one Watch. The fix above helps landing-then-pull only. Raise with THJ.
- Rare: a damaging area hazard on one rider's landing cell misses riders not yet put down in the same loop.
- C4 loose ends stand: preview pull ghosts don't know the carry; `PlanPulls` needs an occupancy override. Steer text in `CycloneSteerSetup.cs:31` is for C5. The design says the Whirl's pull "may pay Crippled once"; as built it does not (no per-cell effects on the Whirl pusher): correct the design doc.

## Re-review (fix round): APPROVE

Saved by the coordinator. No must-fix or should-fix left. `SteerActionOpen(isSteering, isWhirling, isPulling, carryLanded)` is `isSteering && !carryLanded && (!isWhirling || isPulling)`; after a landing the Whirl waits for `ReactionsSettled()` before planning the pull (about 0.2 s swell plus 10 frames with no Family Role reacting); abort, rider death and Cyclone destroyed traced, no action left open, no hold leak; the blocked-end-cell safety net skips `TakeOff` and `Land` (only reachable if the board changes mid-Steer). Play checks: act right after a Steer that carried an enemy and confirm nothing interleaves badly (the player gets control before the Whirl ends; both waits hold the pull and hit while a player action runs, 15 s cap). Report correction owed: the fix round says "LF, no BOM", but the touched files are CRLF with no BOM, matching HEAD (do not "fix" line endings). Still open for THJ: the one-Watch-per-action core limit (`ProcessFRApplyWaitList`), cells past a blocked front reached another way (D-553), C4 loose ends (pull ghosts that know the carry, `PlanPulls` occupancy override).
