# Review: onboarding C5a (M4 squad pick + Mark weapon slot)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator) · 2026-11-02 · Branch `thj/onboarding`

**Verdict: FIX**

## Must fix

1. **Hand-edited YAML in the 7 M4 level prefabs: the new stripped-Transform fileIDs break Unity's rule** `(PrefabInstance fileID XOR CorrespondingSourceObject fileID) & 0x7FFFFFFFFFFFFFFF`. All 731 existing stripped objects in the 7 files (and `GB_m2-trailhead.prefab:625`) follow it; only the 7 new slot Transforms don't:
   - `DungeonSafeRooms/LevelDivineRelicRoom 1.prefab:3278` `&5888754783560498592`, expected 6759136686661426643
   - `Level2/Level2-C1-TArtEx.prefab:16661` `&8761568686074522602`, expected 6546682040794475981
   - `Level2/Level2-C2.prefab:10223` `&8156954537061977051`, expected 5037847587925704981
   - `Level2/Level2-C3-1.prefab:3915` `&1478261842605716053`, expected 1250472159171440782
   - `Level2/Level2-C3-2.prefab:2273` `&4306906422018949273`, expected 1299315784577998783
   - `Level2/LevelDomFight.prefab:3623` `&4306906422018949273`, expected 1299315784577998783
   - `Level3/Level3-C1.prefab:4251` `&8761568686074522602`, expected 6546682040794475981
   Unknown whether Unity remaps or drops the cell's `m_AddedGameObjects.addedObject` entry pointing at them; either way the first save rewrites shared files. Conventions: non-trivial asset edits go through a one-off editor script. The merge note (row 22, "redo the swap") also asks for a re-runnable tool.
   Fix: an editor script per level: `PrefabUtility.LoadPrefabContents`, find `Unit_John`, instantiate `Unit_Placeholder` under the same occupant root at local 0, copy facing into `initialDirection` via `SerializedObject`, C3-2 FP filler `[Linda, Lucy, Toba]`, C2 stale decisions entry removed, destroy John, `SaveAsPrefabAsset`. Re-diff.

## Should fix

1. `MarkWeaponSocketTests.cs:48-55` copies `Equip`'s checks instead of calling it; `new EquipmentManager()` neither registers nor saves, so `Assert.IsTrue(new EquipmentManager().Equip(Mark(), Wrap()))` works.
2. `M4SquadPickTests.cs:51-60` doesn't check the slot sits on John's old cell; add the expected `GridCell - (x, y)` per level and assert the ancestor cell name.

## Notes

- Slots are correct `Unit_Placeholder` instances (guid `d12dea6a...`), parent unchanged, local 0, facing kept (-1 in C1-TArtEx and C2, 1 elsewhere). No dangling fileIDs; John's GUID 0 times in the 7 files; no duplicate fileIDs in a file. Lucy, Linda, Toba, TobaEnemy, Ryker untouched. LF, no BOM.
- C2 `decisions`: removing the dead `data[11]` override leaves a harmless gap.
- C3-2 FP filler is now `[Linda, Lucy, Toba]`: the picked unit no longer gets the level-start fill there (John did before); `LevelStartFPFiller` can't point at a slot. For THJ at the play check.
- Roster identical in shape to `M2 - The Trail.asset` (Lucy, Linda fixed, 1 free, Toba excluded).
- Mark socket `data[3].equipmentSocket = 5`, size 3 → 4; `Equip` would accept the Wrap. Old scalar overrides on `equipmentSockets` harmless.
- No private IDs; new `.cs` files CRLF like the folder. Commit split correct. No core, static, AI-thread or serialization changes; M4 levels outside the AI regression set.

## Fix round 1 re-review (2026-11-02): FIX

Prefabs clean now: 731 stripped objects pass the XOR rule, one added-object reference per file to the slot Transform, no dangling or duplicate IDs, John's GUID absent, LF no BOM, hunks only John removal / slot addition / addedObject line (+ C2 stale entry, C3-2 filler). Tests now guard the criteria (`Equip` called for real; slot cell and local 0 asserted against the tool's table).

Must fix: `M4SquadSlots.Apply()` re-creates an existing slot on every run (new fileIDs, block moves, ~132 lines per file per run). Make it a no-op when the level is already right (no John, one `GUnitPlaceHolder` on `level.Cell`, `initialDirection` = `(Facing, 0)`, local 0, C3-2 filler `[Linda, Lucy, Toba]`, C2 entry gone): log "already up to date", no save. Run again, confirm `git diff` unchanged.

Should fix: a cell mismatch must stop that level before any destroy/save (currently only warns); add a Play-mode guard in `Run()`.

Open for THJ's play check: Level2-C3-2 start fill no longer reaches the picked unit.

## Fix round 2 re-review (2026-11-02): APPROVE

`IsUpToDate` covers no John, one slot, table cell (checked first), local 0, facing, prefab-instance root, C2 stale entry gone, C3-2 filler `[Linda, Lucy, Toba]`; returns "already up to date" before any destroy/save. Cell mismatch stops the level before destroy/save; Play-mode guard in `Run()`. Prefabs unchanged since round 1 (same slot instance IDs; diff stat 7 files, +469 −592). Optional: class summary comment wording (sent to the implementer).
