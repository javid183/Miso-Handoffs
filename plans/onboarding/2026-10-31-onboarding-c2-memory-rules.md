# Onboarding structure C2: memory rules (tool + component)

Size: S–M    Tier: 2 (editor tool + one new non-core component; THJ: "Start C2", scope D-344)    Assigned to: `miso-implementer` (sonnet) → `miso-reviewer` → THJ check
Branch: `thj/onboarding`. Status: **built, waiting on THJ check**. Review FIX → fix round → APPROVE (+3 small fixes done); EditMode 1155/1156 known red only. Added `level fp full` (template `LevelM1-C2` has no filler; FP carries over between segments). Open for C3: spawned enemies can't be zeroed per spawn (no-spawn memory levels vs zero-XP prefab variants)

Parent: `plans/onboarding/2026-10-26-onboarding-structure-tech.md` § C2 (T1 = data only, D-200). Level rules per segment: `plans/onboarding/2026-10-26-onboarding-levels.md` (segment 4 = Tempest Bloom).

## Scope (D-344)

The Hearth still plays three old M1 levels as placeholders (`Level1-C1_TArtEx`, `Level1-C1-2`, `Level1-C2`); C3 replaces them with the four memory levels built by the grid tool. So C2 builds the lasting pieces and C3 applies them. **Don't edit the old M1 prefabs or the Hearth's level list.**

## Build

1. **`LevelStartRunUpgradeGrant`** (new, `Features/Onboarding/`, non-core MonoBehaviour on a level): a list of `RunUpgradeSO`; at level start grants each to the player faction through `RunUpgradeTracker.TryGrant`. Find the level-start hook the way `LevelStartFPFiller` does it. No statics (or a `PlayModeStaticReset` hook if one is unavoidable). Used in C3 on memory segment 4 with `RU_LindaLucyCycloneSpreadUnlock`.
2. **XP checker** (editor, pure static, beside the grid tool or `Core/Levels/Editor/`): given a level prefab, lists every XP source above 0: placed units of non-player factions (`GUnit.abilityDamageXpReward`, `lethalDamageXpBonus`, and any other XP field on `GUnit`) and every spawn source in the level's sequences/spawners (`GUnitSpawn` and whatever else spawns units; find them all). Given a `Mission`, also checks `completionXPReward` and walks its `levelDependencyGraph`. Report lists unit/spawn path + field + value. C3 adds the Hearth-wide test that calls it.
   - Spawned units come from prefabs: if a spawn source has no per-spawn XP override, the checker reports the prefab's XP. Say in the report how a spawn's XP can be zeroed without editing the shared enemy prefab (an override on the spawn, a spawned-unit setting, or none exists → flag it, don't add core code).
3. **Grid tool line `level xp none`**: zeroes the XP fields on every placed non-player unit as prefab-instance overrides (the enemy prefabs stay unchanged). Parsed with the other `level` lines; shown in the preview; after the build the builder runs the XP checker on the result and warns on anything left above 0 (template spawn sources included).
4. **Alert and FP check for the tool:** `level alert all` and the FP filler rebind exist (D-342). Confirm the filler fills to full (`fpAmountToFill` vs the pool) on a built level; if a block needs a line for that, add `level fp full` the same way. Report what you found.

## Tests

- Grant: the upgrade is applied at level start; `QuitMission`/`EnterMission` clear it (no leak into the next mission).
- Checker: fixtures with an XP unit, a zero-XP unit, a player unit (ignored), a spawn source with XP, a mission with `completionXPReward` > 0.
- Grid tool: `level xp none` parses (and errors on a bad argument); a build with it leaves 0 XP on placed enemies and the enemy prefab asset unchanged.
- Full EditMode suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

## Docs (coordinator)

`tech/level-tools.md` and the `miso-level-chunks` skill master: `level xp none` (and `level fp full` if added). `tech/combat-architecture.md`: the new component. Structure tech C3 bullet: memory blocks use `level xp none`, `level alert all`; Hearth-wide XP test; grant on segment 4.

## Gates

Review / EditMode / THJ check: build one block with `level xp none` and see 0 XP in the inspector (no Hearth play check until C3). Commits: the component + its tests; the checker + grid line + tests.
