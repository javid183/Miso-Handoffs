# Review: Synergy aim preview C2 (Tempest Bloom)
Reviewer: miso-reviewer    Branch: thj/after-hearth    Verdict: APPROVE
(Pasted by the coordinator.)

Scope checked: TempestBloomGeometry.cs (new), LucyCycloneProjectileScatter.cs, SynergyLanePresenter.cs, SynergyLanePresenter.Bloom.cs (new), TempestBloomPreviewRules.cs (new), Editor/TempestBloomPreviewTests.cs (new). File list matches git status. No core edits; core only called.

Findings
- Scatter extraction is behaviour-identical: same gate order (WouldScatter = old whitelist + unlock checks), same adjacency loop, IsScatterDirection == old `adj.Key != -currentDir`. Covered by the original-split equivalence test.
- 4-copy claim verified: Projectile.Direction takes per-axis sign, zero only when exact (Projectile.cs:62-65); flight runs from SpawnSource (AEffectSpawner.cs:82-84) to the end cell's anchor (DestinationMode.Cell). Linda's SpawnSource is at (0.009, 0.245) (Unit_Linda.prefab:270-277); rectangular grid. Every straight shot reads diagonal, no neighbour is skipped, so the real Bloom makes 4 copies, one flying back toward Linda. Needs THJ (keep or fix).
- Damage ownership: presenter-before-controller hover order holds today (PlayerController.cs:861-873 re-adds its listeners on each target-selection entry; the presenter subscribes once). No double counting; clears via LateUpdate. Fragile only to future core changes; see S1.
- Lane tiles and chevrons: give-back guarded; GridManager sends (old,false) to all listeners before (new,true). No tiles left wrong.
- HitDamage matches core AbilityDamagePreview.AddDamage step for step; falloff and target filter match the runtime hit.
- LF, no BOM; no private IDs; no mutable statics; nothing read by AI.

Should fix
S1. SynergyLanePresenter.cs:103-110 / Bloom.cs:85-103: give back bars, tiles and chevrons on the hovered==false pass, so nothing depends on listener order.
S2. Bloom.cs:144,199-208,231-232,243 and TempestBloomPreviewRules.cs:75: cache delegates/predicates, reuse the HashSet, or skip BuildLanes when the shot key is unchanged.
S3. LucyCycloneProjectileScatter.cs:30: null-guard selfEntity/Owner in WouldScatter (now polled every frame).
S4. Multi-cell targets: entity hover uses the anchor cell; overlay-keyed hiding can hide footprint tiles before the Cyclone. Add a boss to the play check.

Notes
- Copies count falloff like the real arrow; the core bow preview counts every entity (Projectile.cs:257-302). Core preview bug, Tier 2, out of scope.
- Duo arrow (Linda–Lucy) and Mark's catch are not previewed.
- Single commit acceptable; optionally split the extraction.
- No AI-regression impact.

## Re-review after round 2
Verdict: APPROVE.

- Back-skip fix: the real split reads "back" from the shooter's cell to the Cyclone's cell along the main axis (LucyCycloneProjectileScatter.cs:58-64), the same helper the preview uses (Bloom.cs:214). Straight lanes give 3 copies. Both whitelisted arrows (LindaAttackArrow, LindaAttackFireArrow) are owned by Linda, including the Duo (UnitsCooperationHandler.cs:621-625); she doesn't move while her arrow flies. Fallback to projectile.Direction only with no shooter cell (doesn't happen today). Mark's returned copies never split.
- Give-back on hover-out (SynergyLanePresenter.cs:107-109), redraw in LateUpdate; listener order no longer matters; approach-preview transitions traced both ways. Possible glow-animation restart on cell change: play check.
- Caching: shot re-read every frame; range list and count in the lane key. Unit dying/moving with the same shot stays stale until next hover (doesn't happen during the player's aim).
- WouldScatter null guards fine. Tests behavioural; trigger shooter lookup untested (MonoBehaviour), minor.
- No core edits, no private IDs, LF no BOM.
- Suggest two commits: (1) scatter fix + TempestBloomGeometry + tests, (2) preview.
