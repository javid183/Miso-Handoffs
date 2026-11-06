# Memory 4 rework: tech plan

Size: L    Tier: 2 (inside the approved design D-398; no core change)    Assigned to: miso-implementer
Branch: `thj/onboarding` (working main, D-396). R1 is general code; R2 and R3 are onboarding-only.
Status: written 2026-11-05 (coordinator)

Design: `plans/onboarding/2026-11-05-m4-mark-rework.md` (approved, D-398): beat list, grids `m4r-*`, levers, stages, the Player experience section. Tech facts: `reports/m4-mark-rework-tech.md`. If anything in this plan contradicts the design, the design wins; ask.

## Runs (one writer at a time, in order)

### R1 · `CastAbilitySequence` (general; sonnet; S)

Goal: a sequence can make a unit cast one of its abilities on a grid cell, with no player input, and waits until the ability completes.

- New `Features/Levels/Sequences/CastAbilitySequence.cs` (a `Sequence` ScriptableObject, menu like the other sequences). Fields: unit nickname, `AbilityPreset`, target cell (x, y), optional timeout (seconds, default 5).
- Model it on Mark's passive (`Features/Player/Mark/.../MarkPassiveAbility_ContinuousAttack.cs:354-368`): find the unit's runtime ability for the preset, raise the same started and performed events the player path raises, and call `AbilityOrchestrator.ActivateAbility(ability, targets, ...)`. Complete on the completion callback, or on the timeout with a warning.
- No AP spent. Cooldown as normal.
- If the unit, ability or cell is missing: log a warning and complete at once. Never hang a sequence.
- No core file is edited. If one turns out to be needed, stop and report.
- Statics: none. If one appears, add a `PlayModeStaticReset` hook.

Acceptance:
1. With Lucy and her Cyclone preset on a free cell, a Cyclone spawns there, owned by Lucy's faction, and behaves as a player-cast one afterwards (lifetime, drift).
2. A missing unit, ability or cell completes with a warning and does not hang.
3. EditMode tests for target and ability resolution, and for the missing cases. Full suite green except the known AI red.

### R2 · Hearth pool Claws (onboarding data; sonnet; S)

Goal: the memory's pools summon a Claw that gives no XP, on every enemy turn while their own Claw is dead.

- Under `Features/Onboarding/` (pick a sensible subfolder):
  - a `Unit_DarkClaw` prefab variant with `lethalDamageXpBonus` 0;
  - a copy of the spawner effect and of the compound effect that point at it;
  - a `CP_Spawner` variant using them, with `intervalMode = SpecificTurns` listing turns 1–8.
- `spawnLimit` stays 1.
- **Check T10:** do spawned Claws come in alert? Find the alert rules for spawned units (EN-12 says Unaware unless a hostile is within 3). If there's a per-spawner or per-unit way to start alert, use it in the variant. If there's none without core code, stop and report: the design's fallback is a staged reveal.
- `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` must pass once R3 places these pools. The XP checker follows spawn effects.

Acceptance:
1. The variant spawns a 0-XP Claw on each enemy turn while its own Claw is dead.
2. The alert answer, with file:line.
3. Tests where cheap: XP and the turn list on the asset.

### R3 · Memory 4 level, wiring tool and tests (onboarding; **opus**; M–L)

Goal: `GB_m4-mark` plays the design's beat list. Tools › Onboarding › Wire Memory 4 (Mark) (`Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs`) builds all of it idempotently. `HearthMemoryMarkTests` checks it.

Start from THJ's uncommitted `GB_m4-mark.prefab`. Keep his cells and his pool tiles, and replace his two `CP_Spawner`s with R2's variant. Then apply the design's start grid `m4r-start`: units, hidden groups `arrival` (Mark 15,2, Claws 11,2 and 13,2) and `top` (9,8, 10,8, 10,7), visible top Claws 10,9 and 11,8, and John on 10,5. Coordinates are the drawing's, which may be offset from the prefab's (the design notes the offset). Resolve tiles from `GridCell - (x, y)` names, and say in the report how they map.

Wiring:
- **Rules:** as in the other memories: Tutorial tier, no XP, FP full, all alert.
- **Locks:** `LevelAbilityLock` on all four heroes, covering every Duo trigger each one carries and `CleanseAbility`. The list is in `reports/m4-mark-rework-tech.md` §Q7, including Mark's odd `Linda_Lucy_Duo_Ability` and the duplicates.
- **Turn 1:**
  - AP cap (`TurnStartActionPointLimit`): Linda 1, Lucy 0, John 0.
  - `GuidedAbilityHint` on Linda's bow (basic attack), turn 1.
  - A `GuidedAbilityHint` WhenUnlocked on the Mark–Lucy Duo.
- **HP** as in the design's levers table.
- **Stages** (queued win groups, in the design's Turn budget table):
  1. Any of the four Bloom Claws destroyed (`EntitiesDestroyedLOCondition`, Any), hidden, cap 1. On complete, the arrival sequence.
  2. John on 7,5 (`UnitTileOccupiedLOCondition`), text "John: hold the den mouth.", cap 2. On complete, the hold sequence.
  3. All five top Claws destroyed (explicit list), "Save the cub." plus the turns-left line, cap 4. It must not evaluate before the `top` reveal; hidden units may count as destroyed. Win.
- **Sequences** (placeholder lines from the design's beat list; `miso-narrative` polishes them later):
  - **Opening:** lines, then `CastAbilitySequence`: Lucy casts Cyclone on 4,4, then John's second line.
  - **Arrival:** lines, `MoveUnitSequence` Lucy to 9,3 along a free route, camera east, reveal `arrival`, lines, LSB Reset, camera on Mark, input on.
  - **Hold:** John's line, camera up, reveal `top`, `UnlockAbilitiesSequence` for the Mark–Lucy Duo only, lines, camera back.
  - **Outro:** LSB `motherFalls` (kept), level voice, Lucy walks to 8,9 and Mark to 9,9 (`MoveUnitSequence`), lines, grid fade, Hearth cutaway (kept).
  - The "Reach the cub" stage and the old cue-Claw fight are removed (supersedes D-347).
- **Known Reset side effects:**
  - A Reset ticks the player faction once more, so the Cyclone loses one life. That's fine; it only needs to exist on turn 1.
  - AP refills without the cap.
  - Selection is random. The design accepts the camera on Mark (Q8).
- **Open checks**, each with the design's fallback; report what you find:
  - T3: can `HiddenLevelUnits` hide a player unit?
  - T6: does an arrow cross the gap at 4,3?
  - T7: how far do the Bloom copies fly?
  - T12: does a tile objective mark its tile?
  - T13: where is Chained Assault's range measured from?
  - T15: hero walk range.
  - Prefer code reading over guessing. Any check that needs play goes in the report for THJ's play session.
- **Tests:** rewrite `HearthMemoryMarkTests` for the new layout, groups, locks, AP cap, stages and sequences. Re-run the tool and check the prefab is unchanged.
- No core file. Don't touch other levels.

Acceptance: the design's acceptance criteria that can be checked without play, plus:
- the tool is idempotent (md5 before and after a second run);
- the Hearth XP test passes;
- the shared-condition test passes;
- EditMode green except the known AI red.

The rest is THJ's play check: the Bloom kills 4, the arrival plays, Mark's chain works, John's hold, the Duo takes 3, the ending plays, and the caps keep it moving.

## In parallel (read-only to Unity)

- `miso-narrative`: the lines N1, N2, N5 and N7, plus the moved M4 lines, per the design's "Lines needed". A draft for THJ. Placed in the sequences after his OK.

## Risks

- Hidden units counting as destroyed: stage 3 is ordered after the reveal, and a test covers it.
- Silent no-op walks: free routes and end tiles, checked in play.
- The AI regression test may shift (new enemies); it stays known red and isn't re-baselined.
- Other branches: R1 is general and lands here (D-396).
- Statics: none planned.

## Docs to update

- The levels plan, Segment 4 (designer).
- The narrative draft (`miso-narrative`).
- `tech/classic-fallback.md`: nothing (no new wiring point).
- `status.md` and `build-log.md` (coordinator).

## Commit log

- 2026-11-06 R1 `0131dd473` feat(levels): add a sequence that makes a unit cast an ability on a cell
- 2026-11-06 R2 `163e01f56` feat(onboarding): Hearth pool spawner that summons a no-experience alert Claw on turns 1 to 8
