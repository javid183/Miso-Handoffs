# Report: Catch & Return offer rule, C1 (the rule and the runtime)

Plan: plans/2026-11-17-catch-return-offer-tech.md    Agent: miso-implementer (sonnet)    Branch: main
Outcome: partial. Code and tests are written and compile clean in a scratch build; the EditMode suite was NOT run (no way to drive the open editor from this session, see "Not verified").

## What changed

- `miso/Assets/_Project/Features/Player/Mark/Scripts/CatchOfferRules.cs` (new, pure, no Unity calls): `ShouldOffer(returnEnemyHits)` (true when the count is not 0; `Unknown = -1` means "could not work it out", offered as before), and the generic `CountReturnEnemyHits` (contacts in flight order, minus shooter and catcher, counting only hostile targeted ones, via `TempestBloomPreviewRules.CollectHits`).
- `miso/Assets/_Project/Features/Player/Shared/Synergies/CatchReturnHits.cs` (new, main thread, no statics): the one physics contact walk (`CollectContacts`, moved out of the Bloom presenter unchanged), `IsHostileTarget` (alive, relation to the shooter includes Enemy, and the return arrow's effect targets that relation), and `CountReturnEnemyHits(returnArrow, from, to, shooter, catcher)` that the real catch calls and the C2 preview can call.
- `miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (+18): `TryCatch` now calls `ReturnWouldHitEnemy` after `PassesCatchGates` and the catch-point calculation, before `PrepareProjectileClone` and `FreezeArrow`. When no: returns false, nothing frozen, no prompt, no clone made.
- `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.Bloom.cs` (-30/+2): the private `CollectContacts` now just calls `CatchReturnHits.CollectContacts` (same body, same behavior), so the Bloom preview, the Catch preview and the real catch share one walk.
- `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchOfferTests.cs` (new): 14 tests, real colliders on a lane far from the scene origin.
- `.meta` files for the three new files (hand-written MonoImporter metas with fresh GUIDs, since the editor had not refreshed; Unity will keep them).

## Acceptance criteria

(C1 only; preview criteria belong to C2.)

- [x] Offer rule: the prompt opens only if the return copy would hit at least one enemy; no enemy between means no prompt and the arrow flies on, with enemies past Mark or none at all. Evidence: code in `TryCatch`; tests `EnemyPastMarkOnly_IsNotOffered`, `NoEnemiesAtAll_IsNotOffered` (written, not yet run).
- [x] Enemy between and past Mark: offered (`EnemiesOnBothSides_IsOffered`, `EnemyBetweenLindaAndMarkOnly_IsOffered`).
- [x] Allies on the line, Mark adjacent or off the line, Cyclone before Mark: same decision as before (an ally never counts as a hit or blocks one: `AllyBetweenAlongsideAnEnemy_StillOffered`; adjacent / off line / Cyclone before Mark never reach the offer rule: tests named for each). Note: an ally alone in front of Mark with no enemy is now NOT offered (no enemy hit), which is the new rule, not a regression.
- [x] One pure static decision function used by the real catch and available to the preview: `CatchOfferRules.ShouldOffer`. A test (`RealCatchAndPreview_AgreeOnEveryLayoutOfOneLane`, about 2000 layouts) compares the real-order decision (gates then offer) with the preview-order decision (`FindCatchStep` then offer) built from the same shared pieces. The preview itself is wired in C2.
- [x] "Marked as seen so the sweep doesn't re-ask": already true. `_lastSeen = projectile` is set before the gates, so a declined arrow is never asked again. No extra code needed; there is a comment at the new call.
- [x] Enemies dying or moving mid-flight can't freeze the arrow: unchanged (the prediction is only made at the moment of the offer; if it said yes and nothing is hit later, the existing release path applies). Not exercised by a test.
- [ ] Tests listed in the plan: all eight situations are covered (plus several-enemies, shooter/catcher never hits, unknown = offered), but not yet run.
- [ ] Compile clean in the editor / EditMode green except the known red: not run in the editor. Scratch Roslyn build of `Assembly-CSharp` and `Assembly-CSharp-Editor` (with my files added): 0 errors. AIRegressionTest inner failure count before/after: not measured (not run; this change touches no AI code, no `GridCell`/AI-read types).

## Save reset

no

## Decisions I made

- The shared contact walk is now a static in `Shared/Synergies/CatchReturnHits.cs`, and the Bloom presenter's private method delegates to it. Same behavior, one walk for everything (plan: "same contact walk the preview uses, where C2 can reuse it"). It touches `SynergyLanePresenter.Bloom.cs` by 2 lines in place of the 30-line body.
- "Enemy" means: alive, `GetFactionsRelation(entity faction, shooter faction)` has the Enemy flag, AND the return arrow's effect `TargetFactionRelation` has that relation. The existing preview predicate only tested the second part (and `HasFlag(0)` is always true, so a neutral unit would count as targeted); the plan says non-hostile units don't count, so the Enemy test was added. The preview's damage bars (C2) should use `IsHostileTarget` too, or the chevron and bars could disagree on a neutral unit.
- When the return can't be predicted (no return arrow effect to read, no shooter faction, no `CombatLevel`), the catch is offered as before (`CatchOfferRules.Unknown`). Fail-open so a data problem never silently removes Mark's catch.
- The check uses the return arrow's prefab (the serialized return prefab, or the caught arrow's prefab) for collider radius, layer and effect, like the preview; start = the catch point, end = Linda's `ReturnDestination`.
- Counting is per entity (any targeted hostile `GameEntity`), not only `GUnit`; the preview's damage code only prints bars for `GUnit`. A hostile non-unit entity (a summon without a unit) would offer the catch but show no bar. Rare; the C2 preview should decide the chevron from the shared count, not from the bars.

## Needs THJ

none

## Docs to update

- Nothing from C1 (C3 owns the GDD and handoff docs).

## Risks and loose ends

- **Not run in the editor.** The Unity MCP server (127.0.0.1:8080) was down and the open editor had not refreshed (no `.meta` generated, no compile in `Editor.log`), and this session has no computer-use tool. Before committing someone must: open the editor (Ctrl+R, wait for the compile), run EditMode, and confirm all `CatchOfferTests` pass and the suite is green except `AIRegressionTest.Baseline_MatchesCurrentAI` (record its inner failure count; expected unchanged).
- The tests exercise real physics colliders in edit mode at a far-away origin (same trick as `ProjectileSweepTests`). If Physics2D queries behave differently in the editor than expected (for example autosync off), `Physics2D.SyncTransforms()` is already called after placing.
- The real `TryCatch` path (QTE, quiver, freeze) can't run in edit mode. The tests cover the decision pieces `TryCatch` composes (gates, then `ReturnWouldHitEnemy` = hit count via the shared walk + `ShouldOffer`); the faction lookup in `IsHostileTarget` is not covered (needs a `CombatLevel`); it is the same expression the preview already used plus the Enemy flag. Needs the verifier's / THJ's play check: enemy only past Mark, enemy between, both, none.
- `TryCatch`'s doc comment says "True when the arrow was stopped at Mark"; it now also returns false for "not offered", consistent with the comment.
- Behavior to watch in play: the prompt no longer appears for an ally-only or empty lane; the arrow's `_lastSeen` slot means a declined arrow will not be re-asked even if an enemy steps in (an arrow in flight, so not possible in practice).

## Proposed commits

1. `feat(mark): offer Catch & Return only when the thrown-back arrow would hit an enemy`: `Mark/Scripts/CatchOfferRules.cs` (+meta), `Shared/Synergies/CatchReturnHits.cs` (+meta), `Shared/Synergies/SynergyLanePresenter.Bloom.cs` (walk moved), `Mark/Scripts/ProjectileCatchAndReturn.cs`, `Mark/Scripts/Editor/CatchOfferTests.cs` (+meta). Risky (live combat behavior), own commit. All under `miso/Assets/_Project/Features/Player/`. If the reviewer wants the walk move separate: commit A = `CatchReturnHits.cs` + `SynergyLanePresenter.Bloom.cs` (pure refactor; `CatchOfferRules.cs` can ride in A too), commit B = `ProjectileCatchAndReturn.cs` + tests.

## Other branches

`thj/cyclone` has a Cyclone-before-Mark case (`SplitsAt`); this change does not touch it. none otherwise.

## How to see it

1. Open the editor, wait for the compile, run Window > General > Test Runner > EditMode > `CatchOfferTests` (and Run All).
2. In a level with Mark and Linda and the catch unlocked, Linda shoots along a lane over Mark (2+ tiles away): (a) enemy only past Mark: no prompt, the arrow hits them; (b) enemy between Linda and Mark: prompt; (c) enemies on both sides: prompt; (d) nobody in the lane: no prompt, the arrow flies through Mark.

## Fix round (review should-fixes)

Both fixed; behavior elsewhere unchanged. Scratch Roslyn build of `Assembly-CSharp` and `Assembly-CSharp-Editor`: 0 errors. EditMode suite NOT run (THJ's editor is open; he recompiles and runs it). No save reset.

- `miso/Assets/_Project/Features/Player/Shared/Synergies/CatchReturnHits.cs`: the relation test is now the pure overload `IsHostileTarget(bool alive, FactionsRelationType relation, FactionsRelationType targets)`; the entity overload does its null/faction/level checks, looks up the relation and calls it with `alive = true`.
- `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchOfferTests.cs`: the enemy predicate is now `_team.TryGetValue(e, out var team) && team == Team.Enemy`; five new tests for the pure overload: `HostileTarget_EnemyTheEffectTargets_IsHostile` (Enemy targeted, alone and with Ally in the mask), `HostileTarget_Ally_IsNotHostile`, `HostileTarget_NeutralRelation_IsNotHostile_EvenWhenEveryRelationIsTargeted` (relation 0), `HostileTarget_DeadEnemy_IsNotHostile`, `HostileTarget_EnemyTheEffectDoesNotTarget_IsNotHostile`. Added `using MISO.Core.Units;` for the enum.
- No new files, no `.meta` changes.
- Line endings: these files (and their existing neighbours in the same folders) are LF on disk, not CRLF as the brief said; I kept LF so each file stays consistent (checked by bytes: 0 CRLF).
