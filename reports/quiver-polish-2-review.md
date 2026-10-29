# Review: quiver polish 2

Reviewer: miso-reviewer, 2026-10-29. Saved by the coordinator.

**Verdict: APPROVE**

No compile errors were found by reading the code. No core code changed and no statics were added. CRLF is kept. There are no private IDs. Each commit unit compiles alone.

**Should fix** (sent back to the implementer): `QuiverAimPresenter.cs:322-331` `ShotCellAfterMove` should use `player.CanApproachAttackTarget(target)`. Today it checks only basic attack, auto-move and a living target, so allies, neutrals and untargetable units also get a walk-then-shoot ghost.

**Notes:**
- **Arrow abilities:** `QuiverArrow` sits on all 5 arrow prefabs. Explosive counts (its spawn effect spawns `LindaExplosiveArrow`). The Fire and Heal Duo arrows count. The John–Linda and Mark–Linda Duos are walks and don't count. Encore doesn't count.
- **Hand-back order:** `onUnitDamageDone` fires after `DieInternal`. The stack unlocks first, then `Pickup` removes it, so nothing is counted twice. `CurrentCell` is still valid at that point. The GUIDs point to John's sword and Toba's axe (slot 0 on each).
- **Flicker:** for a moment the stack may draw unlocked between the death and the hand-back. Watch for it in play.
- **Allied Toba:** the hand-back requires the killer to be in Linda's faction (the same rule as pickups). Whether `Unit_Toba_Ally` is in her faction needs confirming.
- **Prefab:** `Unit_Linda.prefab` was edited on disk while the editor was open. Check the Inspector shows two "Kill hand-back" entries before committing.
- **Shot-cell cache:** it isn't refreshed when AP changes outside the events it listens to. Minor.
