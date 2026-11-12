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

## Notes from the stopped C1 run (implementer, 2026-11-11; nothing was built)
- `FactionTracker.GetUnlockableState` isn't strictly plain data: it goes through `GlobalSettingsSO.Instance` (getter does a Unity-object null check and may `Resources.Load`) and `GetRegistry<UnlockableRegistry>().ResolveEntity`. The AI already does the same on the worker (`UtilityVariables.cs:332, 387`; `GTagSet`), so it's safe once the settings asset is loaded on the main thread — needs an explicit OK when the work resumes.
- In the editor `ResolveEntity` rebuilds its lookup on every call: cache the resolved unlockable, or resolve it once per check.
- A missing ID throws `KeyNotFoundException` (would kill AI planning): C2 data must use a valid ID; consider a safe lookup.
- Reach the faction with `_owner?.Unit?.Faction?.Tracker` (as `IsRunUnlocked` does), not `AEffectCompound`'s Unity-object check.
- `AbilityPreset` isn't partial: field goes in `AbilityPreset.cs` or the class gets `partial`. `AbilityPreset.cs` and `RuntimeAbility.cs` are LF with BOM.
