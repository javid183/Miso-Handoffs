# Shutting a Duo behind a Family-tree node (Explore, 2026-11-11)

Question (THJ, D-521): can one asset do unlock (first node) + upgrades (the rest) for the Linda–Lucy Duo? Answer: **not as one node**; as **two nodes it works**, except one gap.

## How it works today
- **Marks-Sisters upgrade** is a StatAttribute node (`Unit_Lucy.prefab` node `data[7]`, `upgradeMode 1`, `Stat_DMG` on the Duo trigger preset `Linda_Lucy_Duo_Ability.asset`, levels ×1 / 1.2 / 1.35 / 1.5). It reaches Linda's and Mark's copies because `StatAttributeSet.Copy()` shares the entry objects and `UpgradeLevel` lives on them (`StatAttributeSet.cs:37, 68-71, 281-287`; `RuntimeAbility.cs:217, 234`). Linda's fire reads it through `UnitsCooperationHandler.RangedEnchantDuo_TargetAdjust` (`:621-640`).
- **Unlock nodes** (Tempest Bloom `_CycloneArrowScatter`, Sister's Rivalry `_SistersRivalry`) are UnlockableLiteral nodes (`upgradeMode 2`): global per faction, saved (`SkillTree.cs:217`; `FactionTracker.cs:448-482`). They work as prerequisites through an edge (`SkillTree.cs:305-308`).
- A node has one `upgradeMode` (`SkillTree.cs:67`); StatAttribute mode has no locked level. Ability mode unlocks only the owner's copy and isn't saved when `upgradable 0` (the designer's claim: right on every point).

## The two-node route
Node A: UnlockableLiteral, new ID (e.g. `_LindaLucyDuo`), 1 FSP, Bond Lv 2. Edge A → node B: the existing Marks-Sisters StatAttribute node, unchanged.

## The gap: nothing makes a Duo unavailable from an unlockable
`RuntimeAbility.Available` (`:42`) ignores unlockables; `SquadAllowsTrigger` (`UnitsCooperationHandler.cs:424-439`) checks partners only. Options:
1. **Core:** `AbilityPreset` gets an optional unlockable field; `RuntimeAbility.Available` also requires `faction.Tracker.GetUnlockableState(it)` when set. A few lines; the Duo is **hidden** while locked. Core system → THJ's OK.
2. **Feature-only:** a small handler on the units (like `LindaQuiver.HasArrow(HBoolean)`, `LindaQuiver.cs:198`) named in the trigger effect's `activationFeasibilityCheckFunction` (`AEffectBase.cs:55, 76-86`). No core change; the Duo shows **greyed out** while locked.
3. Data-only `AEffectCompound` lock on the trigger effect: the button stays live and does nothing. Not acceptable.

## Side finding
`RangedEnchantDuo_TargetAdjust` writes the Duo factor into Linda's partner-ability Stat_DMG entry, which is shared with its preset: it mutates ScriptableObject data at runtime (domain reload is off). Backlog.
