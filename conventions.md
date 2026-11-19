# Conventions

Owner: coordinator; THJ approves changes. Code and file naming for Miso. **Started 2026-10-15 from project notes; the data patterns were checked against the assets the same day.** House rules that apply to every edit live in `CLAUDE.md` (line endings and BOM, the `PlayModeStaticReset` pattern, stop Play before editing scripts, the `P0` locale bug, partial classes, where tests go); this file doesn't repeat them. Where `CLAUDE.md` and this file disagree, `CLAUDE.md` wins until this file is fixed.

## Repo and project

- Repo root `C:\THJ Work Folder\Miso\` (was `E:\Work\Projects\miso\` on the previous machine). The Unity project is `miso\` inside it (Unity 6000.3.4f1). Game code: `miso/Assets/_Project/` (`Core/`, `Features/`, `Content/`, `Resources/`).
- Namespaces: `MISO.*`, following folders (e.g. `MISO.Core.Systems.AbilitySystem.Effects`). Legacy: the ATB gauge views use `JRPGCombat`.
- New systems go under `Core/Systems/<SystemName>/{Runtime,Editor}`; per-character content under `Features/Player/<Name>/`.
- Inspector buttons use Alchemy's `[Button]`.
- Commit messages (shared repo) are for the whole team: `type(area): what changed`, in plain words. No private tracking tags (playtest item IDs like `B5`, decision IDs like `D-074`, chunk names like `R3a`) and no `Co-Authored-By` line. The link between a commit and its task goes the other way: the hash is logged in the plan's commit log and the `build-log.md` section (THJ, 2026-10-19).

## Code rules

- **Domain reload is off.** Every new static, singleton or cache gets a play-mode reset (`PlayModeStaticReset`, or its own `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]`).
- **AI worker thread.** Code the AI reads (grid, units, abilities, utility variables) uses no Unity-object APIs without a main-thread guard.
- **Serialized renames** keep `[FormerlySerializedAs]`.
- **Definitions** are ScriptableObjects with GUID ids (the `EquipmentSO` pattern).
- **Events** go through `GlobalEventBus` where a system-wide event exists.
- **Editor tools** live in `Editor/` folders and appear under the `Tools/` menu.
- **Non-trivial asset edits** go through a one-off editor script, not hand-edited YAML.
- **No private IDs in code.** Comments, tooltips, log messages, test names and commit messages in the shared repo never cite decision, plan, chunk or playtest IDs (`D-125`, `B4`, `C3`, `Q7`, `J-A`, `R3b`, ...). Only THJ can decode them. Say in plain words what the code does and why. The IDs stay in `claude-handoff/` (plans, reports, decisions, build log). THJ, 2026-10-21.

## Data naming

Checked against the assets on 2026-10-15 (setup session). Follow these for new data; older assets that break them are listed so nobody "fixes" them by renaming.

- Stats: ids, not assets. Each stat is referenced by an `entityID` string `Stat_<CODE>`, mostly short upper-case codes (`Stat_HP`, `Stat_DMG`, `Stat_CRC`, `Stat_EVA`, `Stat_DR`, `Stat_SPD`, `Stat_WIS`, `Stat_FP`, `Stat_AP`, `Stat_HPP`, `Stat_CLD`, `Stat_AUXADD`, ...). A few are unit-specific (`Stat_JShieldDR`).
- Units: `Unit_<Name>.prefab` in `Features/{Player,Enemy}/<Name>/Prefab(s)/` (e.g. `Unit_John`, `Unit_BlackClaw`, `Unit_GoblinQueen`). Variants add a suffix (`Unit_Toba_Ally`, `Unit_TobaEnemy`). Exception: `Features/Enemy/Deevoted/Prefabs/Deevoted.prefab`.
- Abilities: `AbilityPreset` assets are `<Unit>_Ability_<Name>` (e.g. `John_Ability_...`, `GoblinQueen_Ability_...`); shared family items use `Bergsons_Ability_<Name>`. Effect sub-assets extend the preset's name (`..._Effect_<Kind>`). Toba's older presets still say `Dom_Ability_*` (only `Toba_Ability_Wall` uses the new name). Older exceptions: `Lucy_Cyclone_Ability`, `John_PassBy_Ability`, `John_APTransfer_Ability`, `<Enemy>_Summon_Ability`, `CleanseAbility`.
- Duos: the cooperation entry `ID` is `<A>_<B>_Duo` (seven: `John_Linda_Duo`, `John_Lucy_Duo`, `Linda_Lucy_Duo`, `Linda_Toba_Duo`, `Mark_John_Duo`, `Mark_Linda_Duo`, `Mark_Lucy_Duo`). Presets: `<A>_<B>_Duo_Ability` plus one per side, `<A>_<B>_<SIDE>_Duo_Ability` (`John_Lucy` uses `John_Lucy_Duo_<SIDE>_Ability`).
- Run upgrades: one folder per upgrade, `Resources/RunUpgrades/<Name>/`, holding `RU_<Name>.asset` and, when it has a pickup, `RUP_<Name>.prefab`.
- Missions (`Mission` assets): campaign missions are `Content/Levels/M<N> - <Title>.asset` (also `MX - Another Sanctuary`); Home sorties are `Content/Home/Sorties/HomeSortie_<Name>.asset`.
- Home definitions (`Content/Home/<Kind>/`): `<Kind>_<Name>.asset`, e.g. `Station_*`, `Recipe_*`, `Ingredient_*`, `Lesson_*`, `Study_*`, `Thread_*`, `Upgrade_*`, `Omen_*`, `Star_*`, `BondScene_*`, `Prologue_*`, `Preset_*`; the cycle is `HomeCycle_Demo.asset`. Built by `HomeDemoContentBuilder`.

## Visual and animation assets

Checked against Lucy's and John's assets on 2026-10-21. The Animator path below is canonical for units, props and VFX. `Core/Animation/SpriteAnimator` (`SpriteAnimationData`, its own fps and direction maps) is a separate live system that this section does not cover; don't mix the two on one object.

### Hierarchy

- A visual object is an empty parent with no renderer, named for the thing (units: `Unit_<Name>`, per Data naming above).
- `Visual`, its child, carries the `Animator` and `EntityAnimationHandler`, plus any other script that drives visuals or audio. Nothing renders on `Visual` itself.
- `Body`, under `Visual`, is the main `SpriteRenderer`. Clips drive it by the curve path `Body`, so the name is load-bearing. Its resting sprite is frame 0 of the sheet that reads most clearly as the object.
- Other renderers sit beside `Body` under `Visual`, named for what they are (`Shadow`, `Glow`, `Body_Overlay`).
- `VFX` is a parent under `Visual` for VFX sprites. It may nest its own children and carry its own `Animator` (`AC_<Name>_VFX`).
- Sorting is per renderer; there is no `SortingGroup` anywhere. Each renderer sets its own layer and order, chosen relative to `Body`'s.

### Sprite import

- Sheets live in `Features/<Area>/<Name>/Art/Animations/<State>/` and keep the artist's file name as delivered. ("Art", singular; Lucy's `Arts/` is left alone.)
- One image is Sprite Mode Single. A sheet is Multiple, sliced Grid by Cell Count.
- Point filter, mipmaps off, 100 pixels per unit, extrude 1, mesh type Full Rect.
- Pivot is Center for symmetric objects, otherwise Custom at a meaningful point that is identical across every sheet of that object, so switching clips doesn't make it jump. Characters pivot at the feet (John is about `[0.53, 0.12]`).
- Lucy's sheets are Center `[0.5, 0.5]` and break the feet rule; her `textureCompression` also differs from John's. Left as they are, because re-pivoting means re-checking every clip.

### Clips and controllers

- Controller: `AC_<Role>_<Name>.controller`, beside the state folders (`AC_Playable_John`, `AC_NPC_John`, `AC_Playable_Lucy`). A VFX controller adds `_VFX`.
- Parameters are `DirectionX` and `DirectionY`, both float.
- One state per action, named for the action (`Idle`, `Run`, `PrimaryAttack`). Each holds a 1D blend tree on `DirectionY`: threshold -1 Down, 0 Side, 1 Up.
- A variant state is the action name plus `_<Variant>` (`Idle_Shield`, `Run_Shield`). `EntityAnimationHandler.SetStateVariant` appends the suffix and falls back to the plain state when that variant doesn't exist, so a variant only needs the states that actually differ.
- Only `Up`, `Side` and `Down` sheets exist; left and right come from flipping Side (`SideVisualMode` on `EntityAnimationData`).
- Clips: `A_<Name>_<State>_<Direction>.anim`, in the state folder, where `<State>` is the animator state name including any variant suffix (`A_John_Idle_Shield_Down.anim`). Sample rate is set by feel, usually 8 to 12, on `m_SampleRate`. THJ, 2026-10-21.
- Older clips use two earlier schemes and stay as they are: `Lucy-Idle-Down.anim`, and John's `A_Playable_John_Action_Idle_Shethed_Down.anim` (which also misspells "Sheathed").

## Text

- Unfinished player-facing text is not tagged in the asset (only barks strip `[PLACEHOLDER] `; dialogue and panels show it). List placeholder lines in the plan or report that owns them (D-348).
- Use `glossary.md`'s term for every mechanic and name.

## `claude-handoff/` files

- Lowercase, hyphenated file names.
- GDD: `design/gdd/<area>.md`, character sheets in `design/gdd/characters/<name>.md`. Rule IDs (`FR-3`), their prefixes and the status labels are defined once, in `design/gdd/overview.md` › How to read. An ID is never reused or renumbered; a dropped rule keeps its ID with the status Dropped.
- Plans: `plans/YYYY-MM-DD-<slug>.md`. Reports: `reports/<slug>.md`; the verifier's: `reports/<slug>-verify.md`.
- Playtest notes: `playtests/YYYY-MM-DD.md` (raw notes at the top).
- Decision IDs: `D-NNN`, increasing.
- Branch-specific rules are written once, with the variant: "**On `<branch>`:** ...".
