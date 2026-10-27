# Report: Linda's Quiver, C2 (pickup and the hand-back beat)

Plan: plans/2026-10-26-linda-quiver-tech.md (chunk C2)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done (EditMode green except the known red, message unchanged; play criteria not verified in play). No core-system code changed.

## What changed

All paths under `miso/Assets/_Project/Features/Player/Linda/`. LF, no BOM, `.meta` for every new file.

New, `Scripts/Quiver/`:
- `ArrowPickupRules.cs`: pure. `MayPickUp(alive, onOwnersSide)` and `Resolve(stacks, cell, quiverRoom, alive, onOwnersSide)`: takes up to the free room off an unlocked stack, leaves the rest.
- `HandBackLines.cs`: the placeholder lines from the text report, each tagged `[PLACEHOLDER] ` in the data, `Strip` for the screen. `HandBackLineChooser` picks the lines (own reply for Lucy, Mark, Toba half the time, generic otherwise; a picker's line never repeats twice in a row; Linda's self-pickup lines have no picker line). Random source is injected. No line calls John "Dad", and John has no own reply.
- `GroundedArrowField.Pickup.cs`: partial of the field. Listens to `gridCellPlugStateChanged`, takes the stack, adds to the quiver, plays the beat (picker bark, toss tween, Linda's reply; self-pickup: one line, no toss). Non-blocking coroutine on the field.
- `Editor/ArrowPickupRulesTests.cs` (13), `Editor/HandBackLinesTests.cs` (11), one new wiring test in `Editor/QuiverWiringTests.cs`.

Edited (C1 files, extended):
- `Scripts/Quiver/GroundedArrowField.cs`: now `partial`; `Land` takes an optional quiver and calls `TryPickUp` after laying the arrow (the landing-on-a-Bergson case); hooks the pickup listener in `Awake`/`OnDestroy`; ends beats on level end.
- `Scripts/Quiver/LindaQuiver.cs`: three serialized beat fields (`handBackTossSeconds` 0.6, `handBackReplyDelaySeconds` 0.5, `handBackArcHeight` 0.6) with clamped getters; `Start` registers the quiver with the level's field.
- `Scripts/Quiver/QuiverArrow.cs`: passes its quiver to `Land`.
- `Prefabs/Unit_Linda.prefab`: the three beat values added to the existing `LindaQuiver` block (no new component).

Not touched: `PlayModeStaticReset` (no new static; the chooser is instance state on the per-level field).

## Acceptance criteria

- [ ] **John over a 2-stack with Linda at 1/4: 3/4, icon gone, toss and two barks.** Not verified in play. Code: John plugs into the cell, the event reaches `TryPickUp`, `Resolve` takes min(2, room 3) = 2, `Add` refills, `RefreshView` removes the icon, `HandBackBeat` barks John's line, tosses the arrow icon for 0.6 s, and Linda replies at 0.5 s. EditMode: `PickupFeedsTheQuiverUpToItsSize`, `TwoStackWithRoom_...`.
- [x] **Extras beyond size stay with the right stack.** EditMode: `StackBiggerThanTheRoom_...`, `PickupAtThreeOfFour_TakesOneAndLeavesOneOnTheTile`, `FullQuiver_TakesNothing...`. The view is refreshed with the new count.
- [ ] **Pushed, Commanded, Fist Blitz, Dance moves pick up.** Not verified in play. Code check (all read, none changed): `AEffectPusher.MoveEntity` calls `path[i + 1].PlugEntity(entity)` for each step; `AEffectCommand` (same loop shape) does `path[i + 1].PlugEntity(entity)` per step; `AEffectDashAttack` moves only through `AEffectTransporter.Apply/ApplyDirect`, whose walk loop plugs `path[i + 1]` per step and whose teleport and jump plug the destination; the John-Linda Dance is `AEffectTransporter` in Walk mode (`moveMode: 0`, `ignoreAlliesWhileWalking: 1`). `GridCell.PlugEntityInternal` raises `gridCellPlugStateChanged(cell, type, true)` for every plug, after the occupant slot is set, so each cell entered raises it. Gaps: a Transporter or Command step through a cell that cannot be occupied (an ally standing there) does not plug and raises nothing (the plan's pass-through case: no free arrows can rest under an ally, since they are taken on landing). Teleport and jump plug only the destination, as expected. A blocked step re-plugs the previous cell, which raises the event again there; harmless (nothing to take).
- [x] **Locked stack can't be picked up until its enemy moves or dies.** EditMode: `LockedStack_GivesNothing...`, `StackUnlocksWhenTheEnemyLeaves_...`. In play code, `TryPickUp` recomputes the lock from the cell just before taking, so a stale per-frame lock never blocks a unit that has just stepped in.
- [x] **Enemy over arrows takes nothing.** EditMode: `EnemyWalkingOverAStack_TakesNothing`, `AnEnemy_MayNotPickUp`. Play code: `picker.Faction == owner faction` is required.
- [ ] **Next level: full quiver, no arrows.** Not verified in play. Code: the field is emptied and closed on `levelEnded` (C1) and also stops beats and drops tossed arrows in the air; Linda's prefab (and her quiver) is new per level; the next level makes a new field. Test step below.
- [x] **G3 (arrow landing on a Bergson's tile goes straight back, with the beat).** `Land` calls `TryPickUp` right after the stack is added, so the standing Bergson (or Linda herself) takes it and the beat plays. Not verified in play.
- [x] **Self pickup uses her lines, no toss.** `HandBackLineChooser.Choose(..., pickerIsLinda: true)` gives no picker line and one of `S1/S2`; `HandBackBeat` barks and ends. Tested in `SelfPickup_HasNoPickerLineAndOneOfLindasOwn`.
- [x] **A pickup in the enemy phase counts.** The listener is on the event bus, not tied to the player's turn, and does not check whose turn it is. Not verified in play.

## Test results

Full EditMode suite, command line, Unity 6000.3.4f1 (editor closed). Results/log in the scratchpad: `c2.xml`, `c2.log`.

- 823 tests, 822 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI`. Its message (with timing lines removed) is **identical** to the C1 post-fix run (`fix.xml`), which was identical to the baseline.
- 25 new tests (798 -> 823). No compile errors; no warnings in the files of this chunk.

## Save reset

No.

## Decisions I made

- **Barks do not go through `BarkManager`.** It has no public "say this line" call (it plays only its baked graphs, and adding one would be core code). I use the same popup it uses (`DamageNumberManager.ShowText` over the speaker's head), respect `GlobalSettingsSO.silenceBarks`, and skip its repeated-bark timer so the picker's and Linda's lines can both show. Same behavior as the plan intends, same approach as `RoleBarkPresenter`.
- **Lines live in code, tagged**, in `HandBackLines` (one static table), rather than in an asset. They carry the `[PLACEHOLDER] ` tag and `Strip` removes it on screen; no existing stripper exists. Moving them to a data asset later is easy.
- **Timing fields sit on `LindaQuiver`** (no new component, one prefab block edited). Reply defaults to 0.5 s into a 0.6 s toss, so it lands just as the arrow arrives.
- **The quiver is refilled at once**, the toss is only a visual that follows (non-blocking, no input lock).
- **The beat starts one coroutine per pickup**, so several stacks in one move each get a beat (the text report suggests this). The pickup's lines do not repeat twice in a row per picker.
- **Unknown pickers** (a unit that is not John, Lucy, Mark, Toba or Linda): no picker line, a generic reply from Linda.
- **Linda dead:** no pickups (nobody to hand them to); the arrows stay on the board.
- The picker is read from `cell.OccupantEntity` (the event only carries the entity type), which is set before the event is raised.

## Needs THJ

None. (Still open from the text report: whether John's reply may call him "Dad"; that line is left out.)

## Docs to update

- `tech/combat-architecture.md`: pickup in `GroundedArrowField.Pickup.cs`, listener on `gridCellPlugStateChanged`, beat settings on `LindaQuiver`.
- `status.md` / `build-log.md`: C2 built, play check due after C3.

## Risks and loose ends

- **Not seen in play:** timing of the beat (0.6 s, reply at 0.5 s), toss height and sprite size, and whether two beats at once (two stacks in one move) read badly. All tunable on `Unit_Linda`'s `LindaQuiver`.
- **Bark overlap:** the picker's popup and Linda's popup show at different heads; two pickups in the same instant will overlap popups. Not guarded.
- **Quiver count jumps before the toss lands** (the pips arrive in C4; the number is immediate by design).
- **Multi-cell units:** the event gives only the entered cell; a picker is read from that cell's occupant. Bergsons are one-cell units, so no issue now.
- **Undo/revert** of a move re-plugs the start cell and would count as a pickup if an arrow had landed there meanwhile. Not seen as reachable.
- Super time Crescendo behavior unchanged (see C1).
- `AIRegressionTest` message unchanged by this chunk.

## Proposed commits

Merged units (C1 and C2 share files). Paths under `miso/Assets/_Project/`.

1. Quiver scripts and tests, C1 and C2: everything in `Features/Player/Linda/Scripts/Quiver.meta` and `Scripts/Quiver/` except `Editor/QuiverWiringTests.cs`.
2. The `PlayModeStaticReset` line: `Core/Managers/PlayModeStaticReset.cs` (core).
3. The two cloner scripts: `LucyCycloneProjectileScatter.cs`, `ProjectileCatchAndReturn.cs`.
4. Prefabs, data and wiring tests: the five Linda prefabs (including the beat values on `Unit_Linda`), the five spawn effect assets, `Editor/QuiverWiringTests.cs` + `.meta`.

Never stage the TMP fallback asset or the two ProjectSettings files.

## Other branches

`thj/home-test` and `thj/onboarding` once this reaches `main`, as with C1.

## How to see it

1. Open Unity, let it compile; open a level with Linda and John (for example M4).
2. Shoot with Linda so an arrow lies on open ground (quiver 3/4). Walk John onto that tile: the icon goes, John says a line, a small arrow flies to Linda, she answers about half a second later. (No count on screen until C4: check by shooting four times and then using the bow again.)
3. Stack two arrows on one tile (shoot the same empty tile twice) and step on it with Linda at 3/4: one comes off, one stays and the "2" becomes nothing (a single arrow, no number). With Linda at 4/4 nothing comes off.
4. Kill an enemy standing on an arrow (locked, reddish); then walk onto the tile: it is taken. Walk into a locked stack's neighbor first to see nothing happens.
5. Let an enemy walk over a free arrow: it stays.
6. Push or Command a Bergson across an arrow tile, use John's Fist Blitz, or the John-Linda Dance across one: each picks it up.
7. Have Linda walk onto her own arrow: one line from her, no toss.
8. Aim an arrow at a tile where John stands: it goes straight back with the beat.
9. Finish the level and start the next: full quiver, board empty. To silence barks for a check, set `silenceBarks` in the global settings: the toss still plays.

## Review fixes

- **Dead speakers:** `Bark` skips any speaker that is not alive. The toss ends (and its sprite is destroyed) as soon as Linda is dead or destroyed, with no late reply.
- **Pickup decision is pure and tested:** `ArrowPickupRules.Pickup(...)` now holds the whole decision (living Linda, picker present, alive, same side; lock re-read from whether an enemy stands there now; room cap; leftovers back on the tile if the quiver refuses). `TryPickUp` only gathers the facts, calls it, and plays the beat. New tests: stale lock with the enemy gone, enemy there now, dead Linda, no/dead/other-side picker, quiver refusing some, an arrow landing under a friend taken at once, full quiver and no stack. Renamed `StackUnlocksWhenTheEnemyLeaves_ThenItCanBeTaken` to `LockedStackTakenNothing_ThenOnceUnlockedItIsTaken`.
- **Timing test:** renamed `Linda_HandBackBeatTimingsAreSane`; it checks only toss > 0, delay and arc >= 0, and reply delay not after the toss end.
- **Revived unit:** done without core code. The field also listens to `unitBorn` (raised by `Resurrect` and `OnHeal` after the unit is alive again) and runs the pickup on the unit's cell. Not verified in play.
- Left as is: nothing is picked up while Linda is dead; allied units in another faction do not pick up.
- Tests: 830 total, 829 passed; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, message unchanged. 32 new tests for C2 in all. LF, no BOM, no IDs, no core code.

### Stale lock look (second review)

- `TryPickUp` now compares the stack's stored lock before and after `Pickup`. If it changed, it redraws the stack and raises `OnChanged` even when nothing was taken.
- New test `Pickup_ChangesTheStoredLockEvenWhenNothingIsTaken` checks the lock flips both ways with no pickup.
- Tests: 831 total, 830 passed; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, message unchanged. Not verified in play.
