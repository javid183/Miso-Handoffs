# B4 F4 · Mark measures the attacker's footprint (pulled from R2, parked)

- Pulled from R2 by THJ (D-065) after review. With this change Mark's role fires against a multi-tile enemy when only a non-anchor cell is in range.
- Fist Blitz (`AEffectDashAttack`) still picks its dash destination from the enemy's **anchor** cell, so Mark could then punch from a distance at big enemies.
- Before reapplying, make `AEffectDashAttack` approach/adjacency footprint-aware (shared core code, Tier 3): dash to a cell adjacent to any footprint cell.
- Reapply in the later Family Role chunk, together with that fix, and play-check against a big enemy (Goblin Queen).
- The patch also needs the helper below (it was in `FactionRoleRules.cs` during R2 and was removed with F4), plus its tests.

## Hunk: `miso/Assets/_Project/Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs` (CRLF, no BOM)

```diff
@@ -60,7 +60,8 @@ namespace MISO.Core.Features.Bergsons
                 || !attacker
                 || !attacker.IsAlive
                 || attacker.IsDowned
-                || !GetCellsInRange().Contains(attacker.CurrentCell)
+                // any cell of the attacker's footprint counts, so multi-tile enemies are measured like Linda and Lucy do
+                || !FactionRoleRules.IsFootprintInRange(attacker.OccupiedCells, attacker.CurrentCell, GetCellsInRange())
                 || !ability.CheckTargetSelectionCondition(attacker))
                 return false;
```

## Helper to add back to `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs`

```csharp
        // F4: a unit is in range when any cell of its footprint is one of the range cells. An empty footprint
        // (not placed on the grid properly) falls back to the anchor cell, which is what the check used before.
        public static bool IsFootprintInRange<TCell>(IReadOnlyCollection<TCell> footprint, TCell anchor, ICollection<TCell> rangeCells)
        {
            if (rangeCells == null) return false;
            if (footprint == null || footprint.Count == 0) return rangeCells.Contains(anchor);
            foreach (var cell in footprint)
                if (rangeCells.Contains(cell)) return true;
            return false;
        }
```

## Tests to add back to `Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs` (needs `using System.Collections.Generic;`)

```csharp
        [Test]
        public void IsFootprintInRange_AnchorOutsideButFootprintCellInside_True()
        {
            var anchor = new Item("anchor");
            var other = new Item("other");
            var range = new List<Item> { other, new Item("x") };
            Assert.IsTrue(FactionRoleRules.IsFootprintInRange(new[] { anchor, other }, anchor, range));
        }

        [Test]
        public void IsFootprintInRange_NoFootprintCellInside_False()
        {
            var anchor = new Item("anchor");
            var other = new Item("other");
            var range = new List<Item> { new Item("x") };
            Assert.IsFalse(FactionRoleRules.IsFootprintInRange(new[] { anchor, other }, anchor, range));
        }

        [Test]
        public void IsFootprintInRange_SingleTileAnchorInside_True()
        {
            var anchor = new Item("anchor");
            Assert.IsTrue(FactionRoleRules.IsFootprintInRange(new[] { anchor }, anchor, new List<Item> { anchor }));
        }

        [Test]
        public void IsFootprintInRange_EmptyFootprint_FallsBackToAnchor()
        {
            var anchor = new Item("anchor");
            Assert.IsTrue(FactionRoleRules.IsFootprintInRange(Array.Empty<Item>(), anchor, new List<Item> { anchor }));
            Assert.IsFalse(FactionRoleRules.IsFootprintInRange(Array.Empty<Item>(), anchor, new List<Item> { new Item("x") }));
        }

        [Test]
        public void IsFootprintInRange_NullRange_False()
        {
            var anchor = new Item("anchor");
            Assert.IsFalse(FactionRoleRules.IsFootprintInRange(new[] { anchor }, anchor, null));
        }
```
