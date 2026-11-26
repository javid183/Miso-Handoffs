# Report: M2 River round 2, R1: Lucy's follow-up retargets to a split Dark Worm's child

Plan: plans/2026-11-26-m2-river-round2-tech.md (R1)    Agent: miso-implementer    Branch: main (not switched)
Outcome: done (play check pending)

## What changed

- `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (core, approved D-729; LF, no BOM, kept): +195/-1.
  - :64-65 `PrepareTargets` stops any watch left from an earlier check.
  - :78 reads the action's per-enemy tile reading (`_cellAtActionStart`).
  - :105-120 case (b): an enemy with no HP reading from the action's start that stands on the tile of an enemy from that reading which is no longer living inherits it: `hurt = true`; named/distance 0 if the parent was named in the action's targets; hit-by-this-action if the parent was in `_hitsByAction`. Ranking (`LucyRoleTargetRanking`) unchanged.
  - :134-135 after the target is picked, starts the split watch on it (case (a)).
  - :139-155 `RetargetToChild` (swaps the dead parent for the child in `Targets`, one `Debug.Log`), `IsHostile` (relation `Enemy` via `CombatLevel`), `RoleEndedWithoutFollowUp` (this role's prompt ended without a press, or with a press and no target left).
  - :164-170 `_cellAtActionStart` dictionary, lazy `SplitWatch` instance (plain C# field, no static).
  - :186-209 `Rebind` also listens to `unitDied` (updates the stored tile of a snapshotted enemy to the tile it died on) and stops the watch; clears the new dictionary.
  - :224-248 activation snapshot also stores each enemy's tile; pruned with the HP reading.
  - :288-289 `Activate` stops the watch (fire).
  - :326-450 new `LucySplitFollowUp` class in the same file: `Start(bus, target, owner)` / `Stop()`, listeners on `unitBorn`, `unitDied`, `onFamilyRoleOutcome`, `turnEnded`, `levelStarted`, `levelEnded`; static `Replace` and generic `TryFindParent` (pure, used by case (b)).
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/LucyRoleSplitFollowUpTests.cs` (+ `.meta`, Unity-generated): 23 EditMode tests.

No change to `FactionRoleHandlerBase.cs`, `PlayerController.cs`, `DarkWormPassiveAbility.cs` or any other file.

## Why both timings work

- **(a) Split while the prompt is up.** `PrepareTargets` picks the parent (alive at min+1, HP dropped) and starts the watch with its tile. `DarkWormPassiveAbility.Split` calls `DiePermanently` (raises `unitDied`; `CurrentCell` is not cleared by unplugging, so the watch refreshes the tile to where it died) and then `SpawnHalf` on that tile, whose `SpawnAt` plugs the child before `RegisterUnit` raises `unitBorn`. All in one frame, so the child is in `Targets` before any later `KeepLivingTargets` (press, end of notice steps) can see the parent dead. `KeepLivingTargets` keeps the living child, the role runs, `Activate` fires on it. The second child (nearest free tile) is ignored: by then the target is the living first child. A child that splits again during the wait hands over again.
- **(b) Split before her role is checked.** The parent is in the action's HP and tile readings; it is dead now (`IsLivingTarget` false, also when already destroyed). The child is alive, has no reading, and stands on the parent's last tile → inherits (hurt, plus named/hit from the parent). Without this the child failed `HpDropped(null, …)` and was never a candidate.
- **Plain kill:** the target dies, nothing is born on its tile → no hand-over; `KeepLivingTargets` drops it and the role skips as `TargetsGone` as before. **Non-worm targets:** the watch only acts when the target is dead and a hostile is born on its tile; case (b) only for units that had no reading at the action's start. Every existing Lucy ranking/HP-drop test passes unchanged.

## Subscription cleanup

The watch's six listeners are removed by `Stop()`, called on: fire (`Activate`), prompt ended without a press or with a press and no target left (`onFamilyRoleOutcome`), Lucy's death (`unitDied` of the owner), turn end, level start, level end, handler disable / bus rebind (`Rebind`), and every new `PrepareTargets`. `Start` calls `Stop` first, so no double listeners (tested). The handler's own `unitDied` listener follows the existing `Rebind` pattern (removed on disable). No new statics, so no `PlayModeStaticReset` hook needed.

## Acceptance criteria

- [x] R1: after a family hit that splits a Dark Worm, Lucy's follow-up goes to the child on the hit worm's tile, both timings; other roles unchanged. Evidence: EditMode tests below; code reads `FactionRoleHandlerBase`/`PlayerController` only. In-game: needs the verifier's play check.

## Chunks

### Chunk R1: Lucy's follow-up retarget

- Changed: `LucyFactionRoleHandler.cs`, `Editor/LucyRoleSplitFollowUpTests.cs` (+ .meta).
- Criteria met: R1, by tests (see Tests); play check pending.
- Decisions and loose ends: see below.

## Tests

- New `LucyRoleSplitFollowUpTests`: 23/23 pass. Case (a): split while waiting → first child taken, second child not; a child splitting again hands over again; target moved before dying → child on the death tile taken. Plain kill → no hand-over. Non-worm: living target + unit born elsewhere → unchanged; dead target + unit born on another tile → not taken; friendly unit born on the tile → not taken. Cleanup: Stop, prompt without press, press with every target gone, Lucy dies, turn end, level end, next level start each end the watch and leave no listener (a later split hands nothing over); a press with a target left and another role's outcome keep it; a second Start does not double the listeners. `Replace` (swap, add when dropped). Case (b) `TryFindParent`: child on a dead enemy's tile → parent; enemy still alive → none; second child away from the tile → none; no reading → none; real `GUnit`/`GridCell` version.
- Lucy/role fixtures (`LucyRole*`, `FactionRole*`): 78/78 pass.
- Full EditMode suite: 2912 total, 2903 passed, 8 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit, not run). **All 8 failures are `M2RiverTests`** (the uncommitted chunk 3.2 tests vs THJ's tweaked `GB_m2-river.prefab`: ring Archer expected on 11,2 but is on 12,2; `TileOf`/`CellAt` failing on renamed/removed cells). They don't touch Lucy or roles; R2 updates them to THJ's layout. The `GridToLevel` flake did not show.
- Not covered by EditMode: the handler's own wiring inside `PrepareTargets` (needs SessionLogs, CombatLevel, a grid); the verifier's play check covers it.

## Reviews and checks

- (coordinator)

## Save reset

no

## Decisions I made

- The watch and the split rules are a plain C# class (`LucySplitFollowUp`) in the same file as the handler, not a new file, to stay inside the approved file; it follows the `SistersTallyListener` pattern (bus and checks passed in) so EditMode tests drive it without Play mode.
- The watch starts in `PrepareTargets` (when the target is chosen) rather than on `onFamilyRolePrompt`, so a split in the camera-focus steps before the prompt is also caught. Cost: when `PrepareTargets` succeeds but the role doesn't run (all targets silenced) or the prompt can't start, the watch lingers until the turn ends or the next check; meanwhile it can only rewrite the idle handler's `Targets`, which nothing reads until the next `PrepareTargets` overwrites them.
- Case (b) heir counts as hurt outright (the plan's "counts as hit") instead of comparing the child's HP with the parent's reading; named/hit flags are copied from the parent so the ranking order is unchanged.
- The stored tile is refreshed on `unitDied` (both in the watch and in the action readings), since the worm splits on the tile it dies on.

## Needs THJ

none

## Docs to update

- `tech/core-systems.md`: note that Lucy's handler hands its follow-up to a Dark Worm child born on the target's tile (coordinator, per plan).
- GDD `lucy.md` follow-up note (designer, per plan).

## Risks and loose ends

- **Camera/spotlight during the notice steps:** `PlayerController.ActivateFactionRole` captures the role's entities when the prompt opens; after a split the spotlight shows Lucy only (the dead parent is filtered out), not the child. The fireball does hit the child. Fixing the framing needs `PlayerController` (core, not approved).
- **Generic heir rule:** case (b) is not limited to Dark Worms: any enemy born during the action on the tile of an enemy that died during it inherits its place (a summon dropped where a unit died). Rare; flagged in case THJ wants it worm-only (would need a worm check, e.g. `TryGetComponent<DarkWormPassiveAbility>`).
- **Split after the follow-up fires** (worm still at min+1 when Lucy's fireball lands, split later) is unchanged: the fireball hits the parent, as before.
- The full-suite run happened while the editor was open: `MS1 - The River.asset` has a write time inside the run (14:19) and `GB_m2-river.prefab` one just before (14:18). `M2RiverTests.TheWiringRerunLeavesTheLevelUnchanged` threw in its first, non-saving read, so it did not write them; it may have been THJ's editor or an `AssetDatabase.SaveAssets` in another test flushing a dirty asset. Both are THJ's uncommitted files; worth a glance before R2.

## Proposed commits

1. `fix(lucy): her follow-up passes to the Dark Worm child born on the target's tile when it splits`: `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/LucyRoleSplitFollowUpTests.cs`, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/LucyRoleSplitFollowUpTests.cs.meta` (core, own commit)

## Other branches

none

## How to see it

1. Open a level with a Dark Worm that can split (M2 The River's clearing worm, or any level with one) and Lucy within reach (her role zone, Shift).
2. With John, Linda or Mark, hit the worm down to its last point. When Lucy's prompt appears, press it; the worm splits during the prompt or the notice: Lucy's fireball goes to the child on the worm's tile. The console logs "Lucy's Family Role follows up on '…': '…' split while the role was waiting."
3. Hit a worm so it splits before Lucy's role is checked (a slow action, or a role that waits for processes): her prompt still appears, aimed at the child on the worm's tile.
4. Kill a goblin outright with a family hit: no child, the role skips as before ("targets were killed or removed" log) or doesn't trigger.
