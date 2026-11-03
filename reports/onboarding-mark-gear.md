# Report: onboarding-mark-gear

Scope: thj/onboarding (Mark's prefab is shared with main / thj/home-test). Size S.

## What changed
- `Unit_Mark.prefab`: socket defaults `equippedItem` set through Unity (LoadPrefabContents + SerializedObject + SaveAsPrefabAsset):
  - data[3] RightHand -> Equipment_Wrist Wrap Of Power (guid 751a6dd8...)
  - data[2] Chest -> Equipment_Monk's Tunic (guid 1faca5c8...)
  (Sockets: 0 Ring, 1 Head, 2 Chest, 3 RightHand.) `GUnit.ApplyDefaultEquipment` then equips both once per save.
- `MarkWeaponSocketTests.cs`: replaced the "starts empty" assertion; added `MarkStartsWearingTheWrapOnHisRightHand` and `MarkStartsWearingTheMonksTunicOnHisChest` (CRLF kept).
- `CharacterSelect_EquipmentsPanelUI` untouched (as decided).

## Diff stat
- Unit_Mark.prefab: 5 insertions, 1 deletion (one overridden objectReference changed, one new override entry).
- MarkWeaponSocketTests.cs: 19 insertions, 3 deletions.
- Noise: Unity also added `preloadOverride: -1` / `showSpeed: 1` in two serialized blocks of the prefab (new defaults of existing fields). I removed them by hand so the diff is only the two equippedItem changes; Unity will re-add them the next time anyone re-saves the prefab.

## Tests
EditMode full run: 1291 total, 1289 passed, 2 failed. Failures: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, and `HomeVisitsTests.ApplyOpeningSetup_RepairsAStationLockInACopyOfTheScene` (unhandled log "[Error] Unsupported type Vector2f" during the full run; passes when run alone; unrelated to this change, likely flaky/related to THJ's modified scene or editor state). Compiled clean. Coverage: both equip defaults covered by tests; combat stats need a play check.

## Proposed commit (one)
`fix(onboarding): Mark starts wearing his Wrist Wrap of Power and Monk's Tunic`
- miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab
- miso/Assets/_Project/Features/Onboarding/Editor/MarkWeaponSocketTests.cs
(no new assets, so no .meta files)

## How to see it
1. Clear the save (defaults equip once per save).
2. Play Hearth -> River; open the character select for the M-level.
3. Mark shows the Wrist Wrap on RightHand and the Monk's Tunic on Chest; in combat the Wrap's stats apply.

## Risks and loose ends
- Existing saves that already ran ApplyDefaultEquipment for Mark will not get the items; clear the save.
- Mark's prefab is shared with main/thj/home-test: they get the same default gear on merge.
