# Review: onboarding structure C2 (memory rules)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. Plan: `plans/onboarding/2026-10-31-onboarding-c2-memory-rules.md`. Report: `reports/onboarding-c2.md`.

**Verdict: FIX**

## Must fix

1. `LevelXpChecker.cs:69-75,166-186`: misses hazards that spawn units (`CP_Spawner` → `CP_SpawnerCompoundEffect` → `GUnitSpawnerEffect`, an `AGUnitSpawner`), and doesn't follow into spawned/summoned prefabs (a zero-XP Dark Worm variant's Split still summons the normal worm). Walk ability assets from every behaviour in the level; recurse into reported prefabs with a visited set; fixture with `CP_Spawner`.
2. `LevelXpChecker.cs:86-103`: `CheckMission` ignores `collectableGResources` (`Mission.cs:246-247`) that can be the XP resource. Report entries with `resourceRef == xPResource`, max > 0, when `resourceCollectionCount > 0`. Also placed `Pickup`s with XP. Tests.
3. FP step 4 answered wrong: FP carries over between the four segment levels; the paper plan wants a top-up each segment; `LevelM1-C2` has no filler. Add `level fp full`: the builder adds a `LevelStartFPFiller` when missing (`fpAmountToFill` 99, `atbGaugeAmountToFill` 0, units as `RebindStartFiller`, wired to `levelStarted` with `UnityEventTools.AddPersistentListener`), preview line, parse + build tests.
4. `LevelStartRunUpgradeGrant.cs:55`: `?.` on Unity objects; after a Play session `GameHandler.Instance` is destroyed-but-non-null, so `OnLevelStarted_WithoutAPlayerFactionWarnsAndGrantsNothing` fails. Use Unity null checks.

## Should fix

1. `LevelStartRunUpgradeGrantTests.cs:63-80`: repeat-grant test tests its own lambda; rename or drop.
2. `LevelStartRunUpgradeGrant.cs:29-33,48`: cache the subscribed bus, unsubscribe from it.
3. `LevelXpChecker.cs:52,177`: type-name string match; use `is AGUnitSpawner` / the action type.
4. `LevelStartRunUpgradeGrant.cs:62`: warn when fewer upgrades were granted than listed.

## Notes

- LF, no BOM, no private IDs, no core change, no statics; `level xp none` writes instance overrides only (prefab + meta hash unchanged). Level-start subscription, restart and mission clear all fine (Clear read, not tested in play). Commit split compiles in order; `level fp full` goes in commit 2.
- Finding 1 confirmed: no per-spawn XP override without core code (`GUnit` fields private, `SpawnAt` plain `Instantiate`, no spawned event). Options: (a) zero-XP prefab variants (summons also need an effect-asset variant); (b) no spawning enemies in memory levels. Reviewer recommends (b), (a) only where needed. Per-spawn override = core, Tier 3.
- Mission initiation/completion sequences not walked; no sequence type spawns units today (low risk).

## Fix round re-check (2026-10-31): APPROVE

All must- and should-fixes correct; split compiles in order (commit 2 adds `GridToLevelBuilder.Fp.cs`, `GridToLevelFpTests.cs` + metas). Small should-fixes: (1) `LevelStartRunUpgradeGrant.cs` and `GridToLevelBuilder.Fp.cs` are CRLF, neighbours LF; (2) `RebindStartFiller` warns "keeps its template values" for a filler just added; warn instead when it lists 0 player units; (3) repeat-grant test also assert `GetBlockReason` == "Already owned". Note: `XpResourceId()` null skips pickup/reward checks silently; C3's Hearth test should assert it isn't empty.
