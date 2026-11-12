# The sisters' Bond nodes: Bloom open, the Duo as a node (tech)

Size: M    Tier: 3 (core `RuntimeAbility`; Duos and Synergies)    Assigned to: miso-implementer
Branch: all (built on `thj/after-hearth`)
Status: parked (THJ 2026-11-11: "leave that for now, not critical"); approved, nothing built. C1 was started and stopped; its edits reverted

## Why

THJ, Trail balance round: Tempest Bloom open everywhere (D-519); the Linda–Lucy Duo itself becomes a Family-tree node shut until Linda & Lucy's Bond Lv 2, next to Sister's Rivalry, both buyable (D-520); Marks-Sisters becomes a second node after the Duo (D-521); the Bloom run upgrade and Memory 4's grant retire (D-522); a locked Duo is hidden through a small core check (D-523). Design note: `plans/2026-11-11-bond-tree-sisters-design.md`. Code facts: `tech/duo-unlock-gate.md`.

## Goal

On a fresh save Bloom works with no purchase; the sisters' Duo is never offered until its node is bought after the Yard's Bond Lv 2; its damage upgrade opens after it.

## Acceptance criteria

C1 (core, own commit):
- [ ] `AbilityPreset` has an optional unlockable reference ("requires unlock"), empty by default. Empty = behaviour unchanged for every existing ability.
- [ ] `RuntimeAbility.Available` is false while the reference is set and the owner's faction hasn't unlocked it (`FactionTracker.GetUnlockableState`); true once unlocked (meta purchase, unlocked-by-default or run grant).
- [ ] Safe on the AI worker thread: `Available` is read by `AIUnitBrain` and `UtilityVariables`; the new check reads only plain data (no Unity-object API), and costs nothing when the field is empty (checked first).
- [ ] EditMode tests: empty field → unchanged; set + locked → not available; set + unlocked → available.

C2 (data, wiring, tests):
- [ ] New unlockable `_LindaLucyDuo` in `Resources/Unlockables/UnlockableSet.asset`, 1 FSP, `unlockedByDefault 0`. `CycloneArrowScatter` → `unlockedByDefault 1` (the Catch & Return precedent).
- [ ] `Linda_Lucy_Duo_Ability.asset` (the trigger preset all three carriers share) requires `_LindaLucyDuo`.
- [ ] Lucy's tree (`Unit_Lucy.prefab`): node `[6]` (was Tempest Bloom) becomes the Duo node: UnlockableLiteral `_LindaLucyDuo`, family node, same slot. An edge `[6]` → `[7]` (Marks-Sisters, unchanged StatAttribute, 2 pips), so the upgrade opens only after the Duo. `[8]` Rivalry unchanged. Use an editor script for the prefab edit (non-trivial YAML), idempotent.
- [ ] `HomeLockRules.cs`: Bond Lv 2 locks the Duo node (by its unlockable id) and Rivalry; the Bloom entry goes; Marks-Sisters keeps its guid lock (also gated by the edge).
- [ ] Retired: `RU_LindaLucyCycloneSpreadUnlock` (and anything that lists it) and Memory 4's `LevelStartRunUpgradeGrant` for it. Asset deletions through the AssetDatabase, `.meta` with them; report every reference removed.
- [ ] Node titles and descriptions for `[6]` and `[7]` from `miso-narrative` (working text if not ready; no placeholder tag in asset text, D-348).
- [ ] Tests: Bloom unlocked on a fresh tracker; Duo `Available` false for Linda, Lucy and Mark before `_LindaLucyDuo`, true after; tree edge `[6]` → `[7]`; Bond lock list; no reference left to the retired run upgrade.
- [ ] EditMode: all pass except the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (never re-baselined).

Play (THJ): fresh save → the Trail: Bloom splits, no sisters' Duo; the Yard → buy the Duo → M4 offers it; Marks-Sisters only after.

## Scope

In: the above. Out: Chained Assault numbers (D-517), the Trail values (M2 C4), Bond rules on `thj/home-test` (reconciled when it takes `main`), the `Tutorial_Duo_Abilities` "1 AP" text (separate fix), the shared-SO write in `RangedEnchantDuo_TargetAdjust` (backlog).

## Touches

Systems: `RuntimeAbility` / `AbilityPreset` (core), `FactionTracker` (read only), skill tree data, `HomeLockRules`, run upgrades, Memory 4 wiring.
USPs: Duos, Synergies.
Docs: GDD `family-systems.md` (BO-4, PR-8, Unlocks, Synergy rows; designer), `characters/lucy.md`, `linda.md`, `player-skill-trees.md` (designer); first-hour design rows (designer); glossary (narrative); `tech/core-systems.md` (coordinator: the new field).

## Risks

- AI thread: the check must not touch Unity objects; guard with the empty-field fast path. `AIUnitBrain.cs` is THJ's uncommitted file: don't edit it.
- Saves that bought Bloom keep the literal but lose 1 FSP: reset test saves (no refund code).
- `thj/home-test` has its own Bond rules: list it in the report as needing reconciliation.
- Existing `LevelAbilityLock` entries on the Duo stay (replays after the Yard).

## Gates

Compile clean / EditMode / `miso-reviewer` (C1 core: `model: opus` for the implementer) / THJ play check (fresh save) / docs above. Commits: C1 core alone; C2 data + wiring + tests.
