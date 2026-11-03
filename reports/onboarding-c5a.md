# Report: onboarding C5a (M4 squad pick + Mark's weapon slot)

Status: **built, compile clean, full EditMode 1273 of 1274 pass** (only the known `AIRegressionTest.Baseline_MatchesCurrentAI` red). **One decision is not built: the slot max-HP component (see "Needs a decision").** No play check was run; nothing staged or committed. The game save was not reset.

## John-reference check (first brief)

Every M4 level places John as one `Unit_John` instance. Two referenced his placed GUnit:
- `Level2/Level2-C2.prefab` (old line 7903): LevelBase `decisions.decisions.Array.data[2].toOmiEntities.Array.data[11]`. Dead data as the coordinator found (Linear branching, array size 2). The stale entry was removed, the other stale `data[2]` entries left.
- `Level2/Level2-C3-2.prefab` (old line 536): `LevelStartFPFiller.units[0]` = John. Now `units` is `[Linda, Lucy, Toba]` (see Decisions).
No name or nickname references. The other 5 levels had only the cell's own added-object entry, which now points at the slot.

## John's per-instance overrides, per level (what the swap drops)

All instances sat at local position 0 under the cell's occupant root (kept: the slot sits there too). Skill-tree and `superTimeAbility.animationEvents` size lines are leftovers of old prefab states.

| Level | Overrides on John | Swap |
|---|---|---|
| LevelDomFight | animationEvents size 0; no facing override (John's prefab faces x = 1) | slot facing (1,0) |
| Level2-C1-TArtEx | animationEvents size 0; `initialDirection.x = -1` | slot facing (-1,0) kept |
| LevelDivineRelicRoom 1 | animationEvents size 24 and 5 frame overrides (`data[19..23].frame = 0`) | dropped (cosmetic, super-ability animation events) |
| Level2-C2 | animationEvents size 0; `m_Size` 301 x 294; `initialDirection.x = -1` | facing kept; `m_Size` dropped |
| Level2-C3-1 | animationEvents size 0 | slot facing (1,0) |
| Level2-C3-2 | animationEvents size 0 | slot facing (1,0) |
| Level3-C1 | animationEvents size 0; `attributeSet...data[1].bounds.max = 320` and `.defaultValue = 320` | dropped, but see below: these never applied |

Facing: John's prefab default is x = 1, so levels without an override got (1,0) on the slot; the two with -1 keep -1. `M4SquadPickTests` checks each.

## Needs a decision: the slot max-HP component is NOT built, and Level3-C1's 320 is dead data

1. **The 320 never applied.** The override paths `bounds.max` and `defaultValue` are old field names; `AAttributeSetEntry` now serializes `sBBounds` and `defaultSbValue`, and Level3-C1 contains neither, so Unity ignores them. The same dead pair appears on the other four units in that level. Unit_John is `overrideBounds = 1` with its prefab values. So John's effective HP in Level3-C1 today is whatever his prefab gives (not 320); the swap changes nothing in play. The same applies to the premise of THJ's HP decision. Applying 320 would be a behavior change, not a preservation.
2. **It cannot be done safely with public API.** `GUnit.GetHealthAttribute()` returns `RuntimeAAttribute`; max is `Bounds.maxV`, a shared class reference. When a unit does not override bounds (any pick other than one with `overrideBounds`), `maxV` is the `AAttribute` asset's own object, so changing it in play would corrupt the asset and leak across Play sessions (domain reload is off). The runtime attribute has no max setter and no way to tell whether it overrides. A safe version needs a small change inside `Core/Systems/AbilitySystem/Attributes/` (a core-adjacent attribute change, e.g. a max-override API), which the brief forbids.
So I stopped on this item, built nothing for it and applied nothing in any level. Options: (a) drop it, since nothing is lost (recommended); (b) approve a small attribute API addition and I build the component, with 320 only if THJ still wants John buffed in that level; (c) author a real HP value on the placed John variant instead (not possible any more, he is a slot now).
Acceptance for the component's test is therefore not covered; the commit "slot HP component + test" does not exist.

## Built

- `Unit_Mark.prefab`: `equipmentSockets` size 3 to 4, new `data[3].equipmentSocket = 5` (RightHand), item empty. 5 added lines, 1 changed; file kept LF.
- `M4 - The White Mothers.asset`: roster `freeSlotsCount 1`, fixed Lucy then Linda, `forcedExcludedUnits` = Toba (same shape as The Trail). The character select therefore offers John or Mark (the others are fixed or excluded).
- The 7 level prefabs: John's `Unit_John` instance replaced in place by a `Unit_Placeholder` instance (same shape as `GB_m2-trailhead.prefab:563`: name override, zero local transform, `initialDirection.x`), same parent; the cell's added-object entry re-pointed to the slot. Lucy, Linda, Toba, `Unit_TobaEnemy` and the Ryker NPC were not touched. Done with a throwaway script on the YAML (kept LF, no Unity save), not an editor tool; the editor reimported them without extra changes.
- Tests (new files, LF, no IDs): `Features/Onboarding/Editor/M4SquadPickTests.cs` (5 tests: the mission lists the 7 levels; each has exactly one slot and no placed John; slot facing per level; Lucy and Linda stay placed and no FP filler holds a missing unit; roster shape) and `MarkWeaponSocketTests.cs` (3 tests: RightHand socket present, 4 sockets and the weapon socket empty, the Wrap is RightHand and Mark-only and his socket matches). The new tests do not call `Equip` (it writes the persistent equipment state).
- `claude-handoff/tech/onboarding-merge.md`: three rows added (Mark prefab again, M4 mission asset, the 7 level prefabs).

## Decisions I made

- Level2-C3-2 FP filler: re-pointing `units[0]` from John to Linda would have put Linda in the list twice (she was already `units[1]`), which heals and fills her ATB twice. I re-pointed and removed the duplicate, so the list is `[Linda, Lucy, Toba]`, same set and same first unit as the intent.
- Slot facing for John-without-override is (1,0), his prefab default, not the builder's constant (also (1,0)).

## Checks

- AIRegressionTest level set: M4's levels are **not** in it. The test skips everything under `Content/Levels/` and covers unit and ability prefabs. `Unit_Mark.prefab` is in its prefab list but only abilities and evaluators are read, which the socket edit does not touch.
- Compile: clean (console had only my one missing `using`, fixed).
- EditMode full suite (Unity MCP): 1274 total, 1273 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (known). The 8 new tests pass.
- Not covered (verifier play check): M4 level 1 and 2 loading with John on the slot and with Mark; Mark equipping the Wrap in the Workshop; character select showing John or Mark; Level2-C2's objectives with the picked unit.

## Files changed (`git diff --stat`, mine only; the four dirty `GB_*` prefabs, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/` and the two Hearth tests were left alone)

```
.../Features/Player/Mark/Prefabs/Unit_Mark.prefab            |   6 +-
.../Content/Levels/M4 - The White Mothers.asset              |  11 +--
.../DungeonSafeRooms/LevelDivineRelicRoom 1.prefab           |  70 +++---
.../Content/Levels/Level2/Level2-C1-TArtEx.prefab            |  54 ++---
.../Content/Levels/Level2/Level2-C2.prefab                   | 101 +++------
.../Content/Levels/Level2/Level2-C3-1.prefab                 |  50 ++---
.../Content/Levels/Level2/Level2-C3-2.prefab                 |  66 +++---
.../Content/Levels/Level2/LevelDomFight.prefab               |  74 +++---
.../Content/Levels/Level3/Level3-C1.prefab                   |  58 +++---
9 files changed, 185 insertions(+), 305 deletions(-)
```
New (untracked): `Features/Onboarding/Editor/M4SquadPickTests.cs` (+`.meta`), `Features/Onboarding/Editor/MarkWeaponSocketTests.cs` (+`.meta`). Handoff: `tech/onboarding-merge.md`.

## Proposed commits (dependency order; paths under `miso/Assets/_Project/`)

1. Mark's weapon socket: `Features/Player/Mark/Prefabs/Unit_Mark.prefab`, `Features/Onboarding/Editor/MarkWeaponSocketTests.cs` (+`.meta`). Message idea: `feat(mark): add a weapon socket so the Wrist Wrap can be equipped`.
2. M4 squad pick: `Content/Levels/M4 - The White Mothers.asset`, the 7 level prefabs above, `Features/Onboarding/Editor/M4SquadPickTests.cs` (+`.meta`). Message idea: `feat(onboarding): M4 lets the player take John or Mark`.
There is no HP-component commit (not built, see above).

## How to see it

1. Unity: Window > General > Test Runner > EditMode, run `M4SquadPickTests` and `MarkWeaponSocketTests` (8 tests).
2. Open `Level2/Level2-C2.prefab` in Prefab Mode: one `Unit_Placeholder` on John's old cell, Lucy and Linda still placed.
3. Play: reach M4 (or use the toolbar level picker on `LevelDomFight`), pick John, then restart with Mark: the pick lands on the slot facing the same way. The character select should offer only John or Mark.
4. Home > Workshop with Mark: the Wrist Wrap of Power should be equippable in his weapon slot.
