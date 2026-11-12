# Cyclone C4 review

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. Branch `thj/cyclone`, uncommitted tree.

**Verdict: APPROVE** (no must-fix). Inside D-533's core set; no statics; inert with no blocker on the board.

## Should fix (sent as a short round)
1. `AIUnitBrain.LineOfFire.cs` `RefusesBlockedFiringSpot`: `otherAttackFromThere` counts only enemy attacks, so a Dark Shaman cell where it could heal/summon is dropped when every bolt target there is behind the Cyclone. Keep the destination when any other usable ability has a valid target from there.
2. `AEffectSpawner.cs:31` `IsProjectileShot` reads `EffectSetLevel?.effects`; use `GetEffects(preset.BaseEffectSetLevels)` so ParameterUpdate upgrade levels still count (no enemy upgrades today).
3. Worker cost: early-out when the unit has no projectile ability (cache per turn), reuse buffers.

## Answers
- Line rule: exact integer walk, ties step diagonally (corner graze free), symmetric, adjacent early-out, footprints +x/+y. Reads cleanly.
- Shots: only Archer (`ShootingArrow`) and Dark Shaman (`ShamanShootingProjectile`) spawn projectiles at top level; heal is an attribute modifier (never blocked). Nested compounds not searched (note in `core-systems.md`). Worker-safe.
- All four places correct; Linda/Bloom never refused; allied/neutral AI get an empty snapshot.
- Move filter: can remove every move (unit uses another action or waits); cells with no enemy in reach are kept, so a blocked Archer may back off out of range (play check); melee unaffected; consistent with C2.
- Snapshot per job; no statics; C2 caveat on `PredictNextTargets(GUnit)` stands.
- Tests drive real helpers; brain collection logic left to play (as C2).
- Commit order E1, A, A2, B (widened), D1, C1 1–8, C, D2, D3, E2, E3 compiles with whole files; C1 3 excludes `CycloneEntity.LineOfFire.cs` safely.
- Hygiene OK.

## Notes
- `core-systems.md`: add `GridLineOfFire`, `ILineOfFireBlocker`, `AEffectSpawner.IsProjectileShot` (top-level effects only).
- Play: Shaman still moves to heal/summon with a Cyclone out; blocked Archer doesn't retreat out of range when a clear cell is reachable.
