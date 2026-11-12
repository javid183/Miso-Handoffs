# Cyclone C1a review

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. Branch `thj/cyclone`, uncommitted tree.

**Verdict: APPROVE.** No must-fix.

## Should fix (folded into the C1b round)
1. Cast refusals untested: `AEffectCycloneSpawner.cs:166-183` (cell no longer empty; Cyclone already out). One EditMode test each: `LogAssert.Expect` the warning, no spawn.
2. `CycloneRules.cs:226` `IsValidCastCell` uses `|| !cell` (Unity null check) in code reachable from `CheckTargetSelectionCondition` / AI thread; drop it (`ReferenceEquals` covers null) or justify in the comment.
3. `CycloneAnchoredSetup.cs:54-60, 101-104`: every re-run rewrites lifeTurns, motionMode, isTargetable, applyPassByEffect, range, cooldown: would undo tuning. Set values only when the swap happens, or document, or drop the menu item after C1b.

## Notes
- Super Time while her Cyclone is out: warning only, nothing on screen (`LucyFactionRoleHandler.cs:240-251`); THJ's rule to pick (skip vs replace). Skip doesn't hang `ActivateFactionSuperTimeIE`.
- Super Time race: the random cell is picked before John's/Linda's Super Time actions; if one moves onto it, the cast is refused with a warning. Rare; play check.
- Claims checked: script GUID swaps keep values and references (file ID unchanged, `LucyCycloneProjectileScatter.selfEntity` intact); Stationary motion, no move coroutine; only baseLevel range/cooldown changed; no `OnGridEntity` edit; Linda copies untouched; LF, no BOM; no private IDs; `CycloneRegistry` reset hook present; registry thread-safe reads.
- `isTargetable` off side effects: no hover info panel on the Cyclone; Shield Flare treats its cell as Free; family `CellPlantedEntity` targeting skips it. Intended; check hover in play.
- Previews still read the 7× compound through `AEffectSpawner.NestedCompound` (damage preview, `GUnit` highlights, `UtilityVariables`, push preview, `FamilyRoleRelay`); no area shape and empty cell, so nothing shows. C1b replaces it.
- Memory 4: (3,4) empty at start, cast in range; play-check after C1b. Lucy memory reset re-runs the family phase tick (extra pip) but is wired before the Cyclone unlocks: no impact today.
- No level places a Cyclone. AI regression may move (stays red).
- Missing low-risk test: Initialize/Dispose path (register, unregister, IsTargetable forced off).
- Cosmetic: stale `m_EditorClassIdentifier` on the spawn asset and prefab; Unity rewrites on save.
- Ability description text now wrong (C5).
- Proposed commits fine.
