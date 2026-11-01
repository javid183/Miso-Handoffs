# Report: Onboarding structure C2, memory rules (tool + component)

Plan: plans/onboarding/2026-10-31-onboarding-c2-memory-rules.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (one finding needs the coordinator: spawn XP cannot be zeroed per spawn, see "Spawn sources")

## What changed

All new files are LF with no BOM, like the neighbouring GridToLevel and Onboarding files (`file` reports "ASCII text", no CRLF). The four edited files were LF already and still are.

New (each with its `.meta`, written by Unity):

- `miso/Assets/_Project/Features/Onboarding/LevelStartRunUpgradeGrant.cs`: the level component.
- `miso/Assets/_Project/Features/Onboarding/Editor/LevelStartRunUpgradeGrantTests.cs`: 5 tests.
- `miso/Assets/_Project/Core/Levels/Editor/LevelXpChecker.cs`: the XP checker (pure static, read-only).
- `miso/Assets/_Project/Core/Levels/Editor/LevelXpCheckerTests.cs`: 6 tests.
- `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/GridToLevelBuilder.Xp.cs`: new partial of the builder (`ZeroEnemyXp`, `ReportRemainingXp`).
- `miso/Assets/_Project/Core/Levels/Editor/GridToLevel/GridToLevelXpTests.cs`: 6 tests.

Edited (small):

- `GridToLevel/GridBlock.cs`: `GridLevelSettings.NoEnemyXp`.
- `GridToLevel/GridBlockParser.cs`: `level xp none` (anything else is an error); the unknown-setting message now lists `xp`.
- `GridToLevel/GridToLevelBuilder.cs`: class made `partial`; one call to zero XP after the filler rebind; one call after the save to report leftovers (only when the line is set).
- `GridToLevel/GridToLevelWindow.cs`: preview row "Enemy XP".

Not touched: old M1 prefabs, `M0 - The Hearth.asset`, THJ's uncommitted files (AI brains, ProjectSettings, TMP font), any core system.

## Findings

### Level-start hook

`CombatLevelRunHandler.StartLevelIE` calls `GlobalEventBus.Instance.levelStarted.Invoke()` after the intro, grid setup and ability introductions, just before turn 1. The bus is a component of the level prefab, so it is per level. `LevelStartFPFiller` is not self-subscribing: its `OnLevelStarted()` is wired as a persistent call on that bus's `levelStarted` UnityEvent inside the level prefab. Wiring a UnityEvent by hand in every level is awkward for C3, so the new component follows `RunUpgradeAltar` instead: in `Start` it waits for `GlobalEventBus.Instance` (up to 600 frames), subscribes to `levelStarted`, and unsubscribes in `OnDestroy`. Nothing to wire; add the component and fill the list. `OnLevelStarted()` is also public, so it can be wired as a UnityEvent if wanted.

It grants through `GameHandler.Instance.GameData.PlayerFaction.Tracker.RunUpgrades.TryGrant(upgrade)` (same faction lookup the tracker uses for its own player check). `TryGrant` applies the usual rules (already owned, unit-scoped upgrade whose unit is not in the squad, missing requirements are refused). It runs at the level start, with units and roster ready. No statics, so no `PlayModeStaticReset` hook.

Clear on mission change already exists: `FactionTracker.EnterMission` (player faction) and `QuitMission` both call `RunUpgrades.Clear()`. Granted upgrades otherwise live for the whole mission and are re-applied to units by `PrepareLevel` -> `ApplyGrantedToUnits` each level. A defeat-restart of the same level re-fires `levelStarted`, but `Has()` makes the second grant a no-op, so nothing stacks.

### Spawn sources, and how their XP is zeroed

Every way a unit appears in play ends in `GUnit.SpawnAt`, which is `Instantiate(this)` of a unit prefab. Sources found:

1. `GUnitSpawnManipulationAction` (level-specific behaviour action lists, `[SerializeReference]`): entries with a `unitPrefab`. Currently used in one prefab (`LevelMarkIntro-C1`). The checker finds these by walking every behaviour's serialized managed references.
2. `AGUnitSpawner` ability effects (summons, e.g. the Dark Worm split, hazard spawners): effect asset with a `unitPrefab`. The checker follows a placed non-player unit's components to ability assets in the `MISO.Core.Systems.AbilitySystem` namespace (presets and the effects inside them) and reports each spawner effect once per level, with the prefab's XP.
3. `Pickup` (`resource` + `resourceAmountRange`) and `AEffectResourceCollector` can pay a resource, which could be XP. **Not checked** (the plan lists GUnit XP, spawns and mission rewards); say if you want pickups added.

**There is no way to zero a spawn's XP without editing a prefab or core code.** Neither spawn action entries, `AGUnitSpawner`, nor `SpawnAt` carry any XP override or spawned-unit setting; the spawned unit is a plain copy of the prefab, and the XP is read from the GUnit's two serialized fields at damage time (`GetAbilityDamageRewards`). I added nothing to core. The workable content-side answer is a prefab variant of the enemy with both fields 0 (a new asset, the shared enemy prefab stays untouched) and pointing that spawn's `unitPrefab` (or summon effect) at the variant. For summon effects that means a variant of the effect asset too, which is shared by every use of that ability. The grid tool's post-build warning says this ("give that spawn a zero-experience variant of the prefab"). Decision for you: whether C3 uses variants, or whether the memory levels simply avoid spawning enemies.

### FP full (step 4)

Confirmed by reading, not by a play check. `FamilyTimePoints` is created in `FactionTracker.InitializePoints()` (on `EnterMission`) with `Value = MaxValue` = the sum of the roster units' FP attribute, so a mission starts at full FP. `Produce(n)` clamps to `MaxValuePractical`, so `fpAmountToFill >= the pool` also means "full". FP carries over between levels of the same mission. The default template (`LevelM1-C2`) has no `LevelStartFPFiller` at all (the built `GB_m1-linda.prefab` has none), so a built level starts at whatever the mission has, which is full on a fresh mission. The builder's existing warning already lists the filler's `fpAmountToFill` when a custom template has one. So I did **not** add `level fp full`; nothing in a block needs it. If a memory level must refill FP in the middle of a mission, that needs a filler with a large amount, which the grid tool does not create (not asked).

## Acceptance criteria

- [x] `LevelStartRunUpgradeGrant` exists, grants through `TryGrant` at level start, no statics: reading above; `GrantAll` tests cover ordering, null skipping, counts and the refuse-repeat case; the actual in-level firing needs the verifier's play check (not run, per plan: no Hearth play check until C3).
- [x] `QuitMission`/`EnterMission` clear it: test `Granted_UpgradesAreClearedByTheTrackersClear` checks `RunUpgradeTracker.Clear` removes a grant. That `EnterMission` and `QuitMission` call `Clear` is by code reading only (they need `GameHandler` and a mission, not testable in EditMode).
- [x] XP checker: `LevelXpChecker.CheckLevel(path or root)` and `CheckMission(mission)` list placed non-player units (both GUnit fields), spawn actions, summon effects, `completionXPReward`, and walk `levelDependencyGraph`. Tests: XP unit, zero-XP unit, player unit with XP (ignored), spawn source with XP, spawn source for a player unit (ignored), mission with `completionXPReward` 7 and a level in its graph, empty mission clean.
- [x] `level xp none`: parsed (error on a bad value), shown in the preview, zeroes `abilityDamageXpReward` and `lethalDamageXpBonus` on every placed non-player unit as instance overrides, then runs the checker on the saved prefab and adds a warning per remaining source. Tests: parse, bad argument, build leaves 0 XP and the Dark Claw prefab file and `.meta` hash identical, build without the line keeps XP and does not warn, template with a spawn source gets a "SpawnAction" warning.
- [x] FP finding: above.
- [ ] Inspector check of a built block with `level xp none` showing 0: not done by me (THJ's gate). Covered in tests by reading the saved prefab.

## Tests

- New: 17 (5 grant, 6 checker, 6 grid XP), all pass.
- Full EditMode suite (Unity MCP, editor open): 1148 total, 1147 passed, 1 failed, 0 skipped. The one failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (known red, not touched).
- Console compiles clean (no errors from the new code; the only warnings are existing ones). One existing console line during the full run, "Can't remove GUnit (Script) because MemorableAttackMemoryShare (Script) depends on it", comes from the builder's existing stray-entity strip in an existing test, not from this work.
- Test fixtures live in throwaway folders (`Assets/__XpCheckerTest`, `Greybox/__XpTest`) that each test deletes; `git status` shows no leftovers.

## Save reset

no

## Decisions I made

- Component self-subscribes to the level's `levelStarted` (like `RunUpgradeAltar`) rather than relying on a hand-wired UnityEvent (like the FP filler). Same behaviour, nothing to wire in C3.
- Namespace `MISO.Core.Features.Onboarding` to match the neighbouring editor code there.
- Checker in `Core/Levels/Editor/` (namespace `MISO.Core.Levels.CEditor`) rather than inside the GridToLevel folder, since C3's Hearth-wide test will call it and it has no dependency on the grid tool.
- Player units are told apart by the level's own `LevelFactionRelations.playerFactionRef`. A level with none treats every unit as non-player.
- The leftover-XP warning after a build only runs when `level xp none` is set (otherwise every enemy level would warn).
- `GridToLevelBuilder` became `partial` (one word) so the new code is its own file.

## Needs THJ

none (the spawn-XP decision above goes through the coordinator)

## Docs to update

- `tech/level-tools.md`: `level xp none` line and what it does; post-build warning; the `Tools` has no menu entry for the checker (API only).
- `miso-level-chunks` skill master: `level xp none`.
- `tech/combat-architecture.md`: `LevelStartRunUpgradeGrant` (self-subscribes to `levelStarted`, grants to player faction tracker).
- Structure tech C3 bullet: memory blocks use `level xp none` and `level alert all`; spawn XP cannot be zeroed per spawn (use a zero-XP prefab variant or avoid spawns); Hearth-wide test calls `LevelXpChecker.CheckMission`; grant on segment 4.

## Risks and loose ends

- The checker follows ability assets only in the AbilitySystem namespace and only from placed non-player units; a spawner reachable another way (e.g. a hazard's own ability that is not on a placed unit) is not found. Hazards placed by the grid carry their own components; `CP_Spawner` was not specifically checked.
- Pickups/resource collectors that pay XP are not checked (see above).
- Mission `completionSequence`/`initiationSequence` assets are not walked.
- `LevelStartRunUpgradeGrant` was not seen firing in a real level (no play check before C3).

## Proposed commits

1. `feat(onboarding): level component that grants run upgrades to the player at level start`: `Features/Onboarding/LevelStartRunUpgradeGrant.cs`, `Features/Onboarding/Editor/LevelStartRunUpgradeGrantTests.cs`, plus their `.meta` files (plain).
2. `feat(levels): xp checker for levels and missions, and level xp none and level fp full lines in the grid tool`: `Core/Levels/Editor/LevelXpChecker.cs`, `Core/Levels/Editor/LevelXpCheckerTests.cs`, `Core/Levels/Editor/GridToLevel/GridToLevelBuilder.Xp.cs`, `GridToLevelBuilder.Fp.cs`, `GridToLevelXpTests.cs`, `GridToLevelFpTests.cs`, edits to `GridBlock.cs`, `GridBlockParser.cs`, `GridToLevelBuilder.cs`, `GridToLevelWindow.cs`, plus the six new `.meta` files (plain; editor-only).

Stage only these paths; do not stage the AI brain files, ProjectSettings or the TMP font asset.

## Other branches

none known

## How to see it

1. Add a block to a doc with a line `level xp none` after `--`, e.g. grid `. J c c` and open Tools > Levels > Build Level From Grid. The preview shows "Enemy XP: none ...".
2. Build, then Open the prefab. Select a Dark Claw under its cell: Progression > Ability Damage Xp Reward and Lethal Damage Xp Bonus read 0 and are bold (overrides). Check `Unit_DarkClaw.prefab` itself still shows its XP.
3. Remove the line and rebuild: the claws keep their prefab XP.
4. To see the checker: Window > General > Test Runner > EditMode > run `LevelXpCheckerTests`. Calling `LevelXpChecker.CheckLevel("<prefab path>")` from the console or another editor script returns the list; `LevelXpChecker.Format(list)` prints "path: field = value" lines.


## Fix round (after review)

Full EditMode suite after the fixes: 1156 total, 1155 passed, 1 failed (`AIRegressionTest.Baseline_MatchesCurrentAI`, known red), 0 skipped. The 25 tests in the four new test classes pass. Compiles clean. All new files LF; no core change; no private IDs.

Must fix
1. Checker walks ability assets from every project behaviour in the level (hazards included, `CP_Spawner` -> compound effect -> `AGUnitSpawner`), not only placed non-player units. Every spawned or summoned prefab it reports is searched in turn (visited sets for assets and prefabs). Unity's own components (transforms, renderers, tilemaps) are skipped to keep the walk fast. Tests: `CP_Spawner` hazard reports a Dark Claw summon; a zero-XP placed Dark Worm still reports the normal worm it splits into.
2. Added a `Pickup` source kind (placed pickups whose resource is the XP resource with max > 0). `collectableGResources` entries that are the XP resource (max > 0, only when `resourceCollectionCount > 0`) are reported for missions (`CheckMission`) and also for units (spawned or placed). Tests: pickup with XP / other resource / zero max; mission collectables with count 1, count 0, other resource.
3. `level fp full` added (`GridToLevelBuilder.Fp.cs`, parser, preview row "Family time points"). If the template has no `LevelStartFPFiller`, one is added on the level bus object with `fpAmountToFill` 99, `atbGaugeAmountToFill` 0, and wired to `levelStarted` with `UnityEventTools.AddPersistentListener`; the existing rebind then fills its unit list. A template that already has a filler keeps it (other values kept), gets `fpAmountToFill` 99 and is wired if it was not. Unknown value is an error; no event bus in the template is a warning. Tests (4): parse, add + wire on the default template, no line = no filler, existing filler reused.
   This corrects my earlier finding: FP carries over between the levels of a mission and the default template has no filler, so a segment-start top-up needs this line.
4. `LevelStartRunUpgradeGrant` uses Unity null checks for `GameHandler.Instance` and `GameData` (a destroyed instance is not a C# null).

Should fix
1. The repeat-grant test now tests the real tracker (`Tracker_RefusesAnUpgradeItAlreadyHas`).
2. The component caches the bus it subscribed to and unsubscribes from that.
3. The checker uses `is AGUnitSpawner` and `managedReferenceValue is GUnitSpawnManipulationAction` instead of type-name strings.
4. The component warns when fewer upgrades were granted than are listed.

Changed/new files in this round: `LevelStartRunUpgradeGrant.cs`, `LevelStartRunUpgradeGrantTests.cs`, `LevelXpChecker.cs`, `LevelXpCheckerTests.cs`, `GridBlock.cs`, `GridBlockParser.cs`, `GridToLevelBuilder.cs`, `GridToLevelWindow.cs`, and new `GridToLevelBuilder.Fp.cs`, `GridToLevelFpTests.cs` (+ `.meta`). Commit 2's file list above includes them. Docs to add: `level fp full` in `tech/level-tools.md` and the `miso-level-chunks` skill.

Still not covered: mission initiation/completion sequences (no sequence type spawns units today). Spawn XP still cannot be zeroed per spawn without core code; the reviewer recommends keeping memory levels free of spawned enemies.
