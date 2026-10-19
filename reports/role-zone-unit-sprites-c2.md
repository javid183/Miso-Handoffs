# Report: Role zone unit sprites, C2 (data)

Plan: plans/2026-10-19-role-zone-unit-sprites.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done

## What changed

All under `miso/Assets/_Project/Features/Player/`, two lines each, inserted before `declineTexts:` on the role handler component only (LF files, no BOM, endings kept):
- John/Prefabs/Unit_John.prefab: roleZoneSprite ShieldOutline, roleZoneSlot 0
- Mark/Prefabs/Unit_Mark.prefab: PunchOutline, slot 1
- Linda/Prefabs/Unit_Linda.prefab: Arrow, slot 2
- Lucy/Prefabs/Unit_Lucy.prefab: Fireball, slot 3 (D-066 trigger blacklist untouched)

PNGs and .meta files not touched.

## Acceptance criteria

- [x] Four handlers resolve to the right sprite and slot: after a forced refresh, read through SerializedObject in the editor: John ShieldOutline/0, Mark PunchOutline/1, Linda Arrow/2, Lucy Fireball/3.
- [x] No new console errors: only the known AI regression report (pre-existing).
- [ ] Visual check in Play: not done (no Play mode, per brief).

## Save reset

no

## Decisions I made

- Sprite fileID is 21300000 for all four (confirmed via AssetDatabase.TryGetGUIDAndLocalFileIdentifier; the "internalID" values in the metas are only the name-table ids and are not what Unity references).
- Linda's prefab had no serialized `showRoleZone` (older prefab), so I inserted the two fields right before `declineTexts:` (the next serialized field) instead of after `showRoleZone`. Same field order; Unity will add showRoleZone on its next save.

## Needs THJ

none

## Docs to update

- none from this chunk

## Risks and loose ends

- The four PNG metas are inconsistent: `spriteMode: 1` (single) but with a `spriteSheet` name table (Arrow even lists Arrow_0 and Arrow_1). Unity still imports one sprite per PNG (fileID 21300000), so it works. Possibly worth a re-import cleanup by THJ; I left them as they are.
- BowArrow.png is not used by any prefab and is left out of the commit as instructed.

## Proposed commits

1. `feat(role-zone): give each family member a role-zone icon and slot`: the four prefabs above, plus Resources/GridOverlays/{ShieldOutline,PunchOutline,Arrow,Fireball}.png and their .png.meta (plain). Depends on the C1 code commit.

## Other branches

none known

## How to see it

1. Open Unity, select Unit_John / Mark / Linda / Lucy prefabs, find the faction role handler component: Role Zone Sprite and Role Zone Slot are set (John Shield/TopLeft, Mark Punch/TopRight, Linda Arrow/BottomLeft, Lucy Fireball/BottomRight).
2. Enter Play, select each unit: its role zone cells show that icon in its quadrant.
