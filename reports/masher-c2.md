# Report: Masher counter, C2 pure rules class and tests

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (chunk C2)    Agent: miso-implementer (sonnet)    Branch: masher-tweak
Outcome: done

## What changed

- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs` (new, BOM + LF): static pure `MasherCounterRules`, plus `MasherProvokerKind`, `MasherStepCandidate`, `MasherDuoPartner` and `MasherChainCap`. No Unity-object APIs (only `Vector2Int` and `Mathf.Abs`), no statics with state.
- `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs` (new, BOM + LF): 44 test cases.
- The handler is untouched (C4 does that). No `.meta` files exist yet: the open editor creates them on its next refresh (the new `Editor/` folder needs one too).

API for C4 (namespace `MISO.Core.Features.Bergsons`, same as the handler; tests in `...EditorTests`):

- `int PickAttackCell(IReadOnlyList<Vector2Int> footprint, IReadOnlyList<Vector2Int> targetCells)`: index of the first target cell that is 4-adjacent to any footprint cell, else -1. `bool IsAdjacent4(...)` wraps it.
- `int RankStep(IReadOnlyList<MasherStepCandidate> candidates, int currentDistance, bool alreadyAdjacent)`: index or -1. `MasherStepCandidate(canAttackAfterStep, distanceToTarget, walkLength)`.
- `MasherProvokerKind Classify(ownerIsPlayerFaction, isOwnersFamilyRoleAbility, isDuoTriggerOrPartner, ownerIsActingUnit, isPlayerPhase)`: `Ignore | ChosenAbility | Duo | Reaction`. Doc comment says burn and other non-ability sources must be filtered out by the caller.
- `int PickDuoPartner(IReadOnlyList<MasherDuoPartner> partners)`: index or -1. `MasherDuoPartner(struck, reachable, actedOrder)`; lower `actedOrder` is earlier.
- `MasherChainCap` (sealed class, not a struct, so a copy can't lose a count): `Max = 10`, `Count`, `TryConsume()`, `Reset()`. The handler owns one instance.

## Acceptance criteria

- [x] Adjacency and attack cell (own tile only, never empty or splash): tests for the four sides, diagonals, two away, same cell, null/empty, 2 x 2 footprint, 2 x 2 target, corner touch.
- [x] Side and back tiles of the cross give no attack cell: `PickAttackCell_SideBackOrFarTile_NoAttackCell`.
- [x] Step ranking (adjacent-capable first and shortest walk, else strictly closer then nearest then shortest walk, else none, none when adjacent): 13 tests including ties.
- [x] Classification: all non-player owners Ignore; chosen and Duo only on the player phase; roles and other reactions in any phase.
- [x] Duo partner D-095: only the striker; both, the reachable one; both reachable, the one who acted first; plus ties.
- [x] Chain cap reaches 10, refuses the 11th and 12th, resets.
- [x] Compiles, and the 44 cases pass. Checked outside Unity: Roslyn from the editor install against Unity's `UnityEngine.CoreModule.dll`, the package NUnit and the bundled Mono, with a small reflection runner (result: 44 pass, 0 fail). Not run in the Test Runner (editor open, not mine to drive): run EditMode > `MasherCounterRulesTests` there. I did not run the full suite; the change adds only new files that nothing references.
- Needs the verifier's play check: none for C2 (pure rules).

## Save reset

no

## Decisions I made

- Namespace is `MISO.Core.Features.Bergsons`, to match the existing handler in this folder (so C4 needs no `using`), rather than a folder-derived name.
- Cells are `Vector2Int`; `PickAttackCell` and `RankStep` return an index (-1 for none) so the handler maps back to its `GridCell`/walk cell without a generic delegate. C4 maps `GridCell` to `Vector2Int` grid coordinates (and Linear distance stays the handler's job, via `GetDistanceTo`).
- `Classify` extra cases the spec left open:
  - an owner's Family Role is Reaction even if that owner is the acting unit;
  - a player-faction hit that is not a role, Duo or the acting unit's chosen ability (a passive or reaction), or the acting unit's ability off the player phase, is Reaction (any phase);
  - a Duo off the player phase is Ignore (D-092/D-094: Duos count on the player's turn only).
- `RankStep` among adjacent-capable cells: shortest walk first, then nearest distance (the spec says shortest walk; the old code ranked distance first, which is equal for 4-adjacent anyway). A non-attack candidate must be strictly closer than `currentDistance`, also when compared with an earlier non-attack pick. Full ties go to the earlier candidate.
- `PickDuoPartner` when both struck and neither is reachable: the one who acted first (the spec was silent). No partner struck gives -1.
- `ChainCap` is a sealed class named `MasherChainCap`, not a struct, to avoid copy bugs.

## Needs THJ

none

## Docs to update

- none (build-log and plan log by the coordinator after the commit).

## Risks and loose ends

- C4 must keep `ActedOrder` and `Reachable` meaningful: "reachable" should be computed the same way as the step (adjacent now, or a `RankStep` hit), so a Duo partner pick and the later step agree.
- The Unity-side `.meta` files appear on the next editor refresh; include them in the commit.

## Proposed commits

1. `feat(masher): add pure counter rules (aim, step, provoker, Duo partner, chain cap) with tests` (plain; not core): 
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs` and `.cs.meta`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor.meta`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs` and `.cs.meta`

   Adds only new files, nothing references them yet. No Co-Authored-By line, no chunk tags, per `conventions.md`.

## Other branches

none

## How to see it

1. Let Unity recompile (Ctrl+R) and confirm no console errors.
2. Window > General > Test Runner > EditMode, filter `MasherCounterRulesTests`, Run: 44 cases should pass.
