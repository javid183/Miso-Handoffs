# Save restructure vs onboarding (read-only, 2026-11-23)

Explore read after merging `origin/main` into `thj/onboarding-demo` (`55f51381b`, D-642). Khash's commits `ac833ac32`, `78397a310`.

## Verdict

Nothing on our branch breaks. The file layout changed (grouped JSON `{"Version":1,"Systems":{...}}`, `Core/Managers/SaveFileSerializer.cs`); save keys, payloads and `ISavable` did not. Old `SaveData.json` files are migrated on load. Our branch adds no save code. Keys checked: `PlayedSequences`, mission entries (completed/visited/order), `Bond`, `FactionTrackData.unlockedLiterals`, ability `"{Nickname}-{preset}-sd"` `{upgradeLevel}`. Not saved: sisters' tally, quiver, onboarding features.

3.1a-2 (Vault `upgradable: 1`): plan holds. Key `Mark-Mark_Ability_Attack_Vault-sd`, no registration or version bump needed; old saves load Vault locked. The old-save risk is 3.1a's (a save holding Command at -1 keeps it locked), already covered by D-636 (demo checks from a cleared save).

## Risks (Khash's core code; not ours to change without THJ)

- **Medium:** one bad entry, an unsupported version or an empty/corrupt file sets `_loadFailed`; every `Save` then returns false for the session, only a console line shows it (`SaveLoadManager.cs:83,131,180`). An empty file used to fall back to a fresh save.
- **Medium:** `Normalize` throws on a duplicate dictionary key (e.g. two resources with the same `entityID`), so that save writes nothing (`SaveFileSerializer.cs:174-175`).
- **Low-medium (pre-existing):** `Tools > Save Data > Clear Save Data` in Play mode doesn't clear in-memory progress, and the next autosave writes it back. Clear outside Play mode, or use the new in-game reset (`AudioSettingsPanel` → `ProgramFlowHandler.ResetSaveDataAndReload()`).
- **Low:** the in-game reset skips classes that reset themselves via `[RuntimeInitializeOnLoadMethod]` (`HomeMemoryOpening`, `HomeMemoryTransition`, `Pickup`, `RunUpgradeTooltipUI`, `EnemyIntroductionController`). Smoke test: reset at Home during the Memory opening.
- **Low:** the serializer groups entries by field shape; a non-wrapper class with exactly `keys`/`values` fields would not round-trip. None exists today.
