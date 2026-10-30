# Report: Encore text and Quiver Size title

Plan: none (size S data task)    Agent: implementer    Branch: main
Outcome: done

## What changed

- `miso/Assets/_Project/Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset` (LF, line 16):
  - `description: "[PLACEHOLDER] Every grounded arrow returns to her quiver, flying straight past walls and enemies. (1 AP, cooldown 2)"`
  - becomes `description: "By her call, every grounded arrow flies home to her quiver. (2 AP)"`
- `miso/Assets/_Project/Resources/Attributes/StatAttributes.asset` (line 1005, id `LQuiverSize` unchanged):
  - `title: Linda Quiver Size` becomes `title: Quiver Size`

Line endings kept (sed substring replace only); diff is exactly these two lines.

## Acceptance criteria

- [x] Both text edits made, YAML quoting valid.
- [x] No test or code asserts the old description or the old title. Grep of `*.cs` found only code comments that say "Quiver Size stat" (LindaQuiver.Size.cs, QuiverSizeRules.cs, QuiverPipsView.cs, LindaQuiver.cs tooltip, QuiverSizeTests.cs, QuiverUI.cs). They describe the stat in prose and are still accurate; left alone.
- Not run: EditMode suite (Unity closed, text-only edit).

## Save reset

no

## Decisions I made

- Left the code comments mentioning "Linda's Quiver Size stat" as they are (not assertions; out of scope).

## Needs THJ

Check that the new text says "2 AP": see the cost note in my reply (the asset's real AP cost and cooldown were not changed, since the task was text only).

## Docs to update

- glossary / Linda sheet: Recall description and stat display name now "Quiver Size" (if they quote the old text).

## Proposed commit

Files:
- miso/Assets/_Project/Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset
- miso/Assets/_Project/Resources/Attributes/StatAttributes.asset

Message: `content(linda): final Recall description and shorter Quiver Size stat title`
