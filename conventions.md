# Conventions

Owner: coordinator; THJ approves changes. Code and file naming for Miso. **Started 2026-10-15 from project notes; the data patterns were checked against the assets the same day.** House rules that apply to every edit live in `CLAUDE.md` (line endings and BOM, the `PlayModeStaticReset` pattern, stop Play before editing scripts, the `P0` locale bug, partial classes, where tests go); this file doesn't repeat them. Where `CLAUDE.md` and this file disagree, `CLAUDE.md` wins until this file is fixed.

## Repo and project

- Repo root `E:\Work\Projects\miso\`. The Unity project is `miso\` inside it (Unity 6000.3.4f1). Game code: `miso/Assets/_Project/` (`Core/`, `Features/`, `Content/`, `Resources/`).
- Namespaces: `MISO.*`, following folders (e.g. `MISO.Core.Systems.AbilitySystem.Effects`). Legacy: the ATB gauge views use `JRPGCombat`.
- New systems go under `Core/Systems/<SystemName>/{Runtime,Editor}`; per-character content under `Features/Player/<Name>/`.
- Inspector buttons use Alchemy's `[Button]`.

## Code rules

- **Domain reload is off.** Every new static, singleton or cache gets a play-mode reset (`PlayModeStaticReset`, or its own `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]`).
- **AI worker thread.** Code the AI reads (grid, units, abilities, utility variables) uses no Unity-object APIs without a main-thread guard.
- **Serialized renames** keep `[FormerlySerializedAs]`.
- **Definitions** are ScriptableObjects with GUID ids (the `EquipmentSO` pattern).
- **Events** go through `GlobalEventBus` where a system-wide event exists.
- **Editor tools** live in `Editor/` folders and appear under the `Tools/` menu.
- **Non-trivial asset edits** go through a one-off editor script, not hand-edited YAML.

## Data naming

Checked against the assets on 2026-10-15 (setup session). Follow these for new data; older assets that break them are listed so nobody "fixes" them by renaming.

- Stats: ids, not assets. Each stat is referenced by an `entityID` string `Stat_<CODE>`, mostly short upper-case codes (`Stat_HP`, `Stat_DMG`, `Stat_CRC`, `Stat_EVA`, `Stat_DR`, `Stat_SPD`, `Stat_WIS`, `Stat_FP`, `Stat_AP`, `Stat_HPP`, `Stat_CLD`, `Stat_AUXADD`, ...). A few are unit-specific (`Stat_JShieldDR`).
- Units: `Unit_<Name>.prefab` in `Features/{Player,Enemy}/<Name>/Prefab(s)/` (e.g. `Unit_John`, `Unit_BlackClaw`, `Unit_GoblinQueen`). Variants add a suffix (`Unit_Toba_Ally`, `Unit_TobaEnemy`). Exception: `Features/Enemy/Deevoted/Prefabs/Deevoted.prefab`.
- Abilities: `AbilityPreset` assets are `<Unit>_Ability_<Name>` (e.g. `John_Ability_...`, `GoblinQueen_Ability_...`); shared family items use `Bergsons_Ability_<Name>`. Effect sub-assets extend the preset's name (`..._Effect_<Kind>`). Toba's older presets still say `Dom_Ability_*` (only `Toba_Ability_Wall` uses the new name). Older exceptions: `Lucy_Cyclone_Ability`, `John_PassBy_Ability`, `John_APTransfer_Ability`, `<Enemy>_Summon_Ability`, `CleanseAbility`.
- Duos: the cooperation entry `ID` is `<A>_<B>_Duo` (seven: `John_Linda_Duo`, `John_Lucy_Duo`, `Linda_Lucy_Duo`, `Linda_Toba_Duo`, `Mark_John_Duo`, `Mark_Linda_Duo`, `Mark_Lucy_Duo`). Presets: `<A>_<B>_Duo_Ability` plus one per side, `<A>_<B>_<SIDE>_Duo_Ability` (`John_Lucy` uses `John_Lucy_Duo_<SIDE>_Ability`).
- Run upgrades: one folder per upgrade, `Resources/RunUpgrades/<Name>/`, holding `RU_<Name>.asset` and, when it has a pickup, `RUP_<Name>.prefab`.
- Missions (`Mission` assets): campaign missions are `Content/Levels/M<N> - <Title>.asset` (also `MX - Another Sanctuary`); Home sorties are `Content/Home/Sorties/HomeSortie_<Name>.asset`.
- Home definitions (`Content/Home/<Kind>/`): `<Kind>_<Name>.asset`, e.g. `Station_*`, `Recipe_*`, `Ingredient_*`, `Lesson_*`, `Study_*`, `Thread_*`, `Upgrade_*`, `Omen_*`, `Star_*`, `BondScene_*`, `Prologue_*`, `Preset_*`; the cycle is `HomeCycle_Demo.asset`. Built by `HomeDemoContentBuilder`.

## Text

- Unfinished player-facing text is tagged `[PLACEHOLDER] ` (stripped on screen).
- Use `glossary.md`'s term for every mechanic and name.

## `claude-handoff/` files

- Lowercase, hyphenated file names.
- Plans: `plans/YYYY-MM-DD-<slug>.md`. Reports: `reports/<slug>.md`; the verifier's: `reports/<slug>-verify.md`.
- Playtest notes: `playtests/YYYY-MM-DD.md` (raw notes at the top).
- Decision IDs: `D-NNN`, increasing.
- Branch-specific rules are written once, with the variant: "**On `<branch>`:** ...".
