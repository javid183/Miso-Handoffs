# Report: Encore in LevelLindaJohn-C1

Plan: none (size S)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done

## What changed

- miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTool.cs: added LevelLindaJohn-C1.prefab to `Levels` (now 9), before C2.

```diff
+            "Assets/_Project/Content/Levels/Generic Levels/FamilyLevels/LevelLindaJohn-C1.prefab",
```

EncoreKitTests.cs: no change needed. It loops over `EncoreKitTool.Levels` and has no exclusion or skip text. No exclusion text in the tool either.

## Acceptance criteria

- [x] Tool lists 9 levels: array has 9 entries; prefab path exists on disk.
- [x] EncoreKitTests covers C1 through the same list: it iterates `EncoreKitTool.Levels`.

## Save reset

no

## Decisions I made

- none

## Needs THJ

Run Tools > Levels > Linda > Add Encore To Custom Kits, then save. Until then `ListedLevels_GiveLindaEncore_SetUpAsInHerDefaultKit` will fail on C1, because the prefab has no Encore yet.

## Docs to update

- none from me (D-320 logging is the coordinator's).

## Risks and loose ends

- Not compiled or tested: editor is open and I did not run it. One-line array change; line endings kept (LF, no BOM, as before).

## Proposed commits

1. `feat(linda): Encore also added to LevelLindaJohn-C1's custom kit`: EncoreKitTool.cs (plain). The prefab change from running the tool goes in its own commit afterwards.

## Other branches

none

## How to see it

1. Let Unity recompile, run Tools > Levels > Linda > Add Encore To Custom Kits, check the console for 9 levels, then run EncoreKitTests in EditMode.
