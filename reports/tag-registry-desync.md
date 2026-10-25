# Tag registry desync: diagnosis (Explore, 2026-10-24)

Symptom: `KeyNotFoundException: 'Status.ShieldUp'` at `ReferenceableEntityRegistry.cs:23`, via `GTagRegistry.ResolveEntity` (`GTagRegistry.cs:72`) ← `JohnShieldRelay.IsShieldUp` (`JohnShieldRelay.cs:160`) on Play, after `GTagSet.asset` and `GTagRegistry.asset` were edited outside Unity (the Unaware tag).

Root cause (pre-existing):
- `GTag.GetID()` = `Parent == null ? name : Parent.GetID() + "." + name` (`GTag.cs:63-66`); `Parent` is runtime only (`GTag.cs:22`), set by `RebuildParentLinks` (`GTag.cs:43-50`).
- Editor `GTagRegistry.ResolveEntity` (`GTagRegistry.cs:66-73`) links parents on `accumulatedL1Tags` (`RebuildHierarchyLinks`, l.75-81; the getter re-accumulates only at count 0, l.13-19), then `BuildEntitiesRefMap` keys the map from `entitySets[*].GetEntities()` = `GTagDefinitionSetSO.gTags` (`GTagDefinitionSetSO.cs:17-26`).
- These are the same objects only right after `AccumulateTags()` (Awake/OnValidate, l.26-38, 48-52). Unity serializes `[Serializable]` by value, so after a reimport of either asset they are separate copies: GTagSet's copies have no parents → keys "ShieldUp" not "Status.ShieldUp".
- Domain reload is off, so Play doesn't re-run Awake/OnValidate. Player builds are fine (Awake gathers, links and maps in one pass).

Workaround: Reimport `GTagRegistry.asset` (or recompile).

Lasting fix (THJ approved D-166, core): in `GTagDefinitionSetSO.GetEntities()` call `RebuildParentLinks()` on each root before collecting, so IDs never depend on the registry's copy. Also fixes `UtilityScoreGraphView.cs:143`, which reads `GetEntities()` directly.

Side finding: the Unaware tag's icon differs between the copies (registry 9d1441b5… Home lamp; GTagSet 9d7ae78c… SaveLoad-Circle1). Use the GTagSet one in both (D-167).
