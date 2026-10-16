# Conventions

Owner: coordinator; THJ approves changes. Code and file naming for Miso. **Started 2026-10-15 from project notes; the setup session checks the data patterns against the assets.** House rules that apply to every edit live in `CLAUDE.md` (line endings and BOM, the `PlayModeStaticReset` pattern, stop Play before editing scripts, the `P0` locale bug, partial classes, where tests go); this file doesn't repeat them. Where `CLAUDE.md` and this file disagree, `CLAUDE.md` wins until this file is fixed.

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

## Data naming (observed patterns; verify before relying on them)

- Stats: `Stat_<Name>` (e.g. `Stat_HP`, `Stat_FP`, `Stat_HPP`, `Stat_WIS`).
- Units: `Unit_<Name>` prefabs (e.g. `Unit_Toba`, `Unit_BlackClaw`).
- Abilities: `<Unit>_Ability_<Name>` presets (e.g. `Toba_Ability_Wall`).
- Duos: `<A>_<B>_Duo` ids (e.g. `Linda_Toba_Duo`).
- Run upgrades: `RU_*` assets, `RUP_*` pickup prefabs, under `Resources/RunUpgrades/`.
- Missions: `Content/Levels/M*.asset`.

## Text

- Unfinished player-facing text is tagged `[PLACEHOLDER] ` (stripped on screen).
- Use `glossary.md`'s term for every mechanic and name.

## `claude-handoff/` files

- Lowercase, hyphenated file names.
- Plans: `plans/YYYY-MM-DD-<slug>.md`. Reports: `reports/<slug>.md`; the verifier's: `reports/<slug>-verify.md`.
- Playtest notes: `playtests/YYYY-MM-DD.md` (raw notes at the top).
- Decision IDs: `D-NNN`, increasing.
- Branch-specific rules are written once, with the variant: "**On `<branch>`:** ...".
