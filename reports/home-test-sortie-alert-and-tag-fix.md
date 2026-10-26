# Report: Home sortie alert settings (D-199) and Home tag group fix (D-182)

Plan: none (coordinator brief)    Agent: miso-implementer    Branch: thj/home-test
Outcome: done

## What changed

Task A (one commit), `miso/Assets/_Project/Content/Home/Sorties/Levels/`:
- `Drowned Shrine/Drowned Shrine 2.prefab`
- `Goblin Queens Warren/LevelM2-C1 1.prefab`
- `Goblin Queens Warren/Queen's Chamber.prefab`

Each got `LevelAlertSettings` (`allEnemiesStartAlert: 1`, bonuses 0) on the LevelBase root, added the way main did it on `LevelM2-C1.prefab` (commit dc64f974a): an `m_AddedComponents` entry on the LevelBase PrefabInstance, a stripped root GameObject, the MonoBehaviour, and the stripped GlobalEventBus component's `m_GameObject` pointing at the root. Same fileIDs as main's change; the diff per file is identical to main's (27 lines). LF endings kept. No `.meta` changes.

Task B (a separate commit):
- `miso/Assets/_Project/Resources/Tags/GTagSet.asset`: top-level `Home` group now `tagIcon: {fileID: 0}`, empty `displayName` and `description`, `showInGame: 0`. 4 lines changed. `GTagRegistry.asset` untouched and needs no change (Unity did not rewrite it).

## Sortie copies matched

I diffed all 21 sortie prefabs against the 11 original levels (main's versions). Only three are close; every other sortie differs by 2300+ lines from every original (different layouts and units), so they are left alone.

| Copy | Original | Evidence |
|---|---|---|
| Goblin Queens Warren/LevelM2-C1 1 | Medium/M2/LevelM2-C1 | Same name; added in 8329bef32 as a copy; diff 105 lines = one extra Unit_Placeholder instance + root name |
| Goblin Queens Warren/Queen's Chamber | Medium/M2/LevelM2-C1 | Same grid and units; diff 111 lines = one extra placeholder instance + root name and level title; it is the Goblin Queen boss room |
| Drowned Shrine/Drowned Shrine 2 | Medium/M2/LevelM2-C1 | Diff 35 lines = only the root name and level title strings (plus the alert component absent); layout and units identical |

Uncertain: Drowned Shrine 2 is an exact layout clone of M2-C1 (including the Goblin Queen unit), so I matched it. If THJ meant it as a non-boss shrine level, revert that one file. No other candidates were uncertain.

## Acceptance criteria

- [x] Confirmed the list: `git grep allEnemiesStartAlert` shows exactly the 11 named levels.
- [x] Copies found and given the same settings, same placement as main.
- [x] Other sorties untouched.
- [x] Home group is a plain group parent (compare `Kin`).
- [x] THJ's 3 uncommitted edits (TMP fallback font, EditorSettings, ProjectSettings) untouched.

## Save reset

no

## Decisions I made

- Used direct YAML edits (clean, mirrors main's diff); no editor script needed.
- Treated Drowned Shrine 2 as a match (see above).

## Needs THJ

Confirm Drowned Shrine 2 should start all enemies alert (it is an M2-C1 clone).

## Docs to update

- combat-architecture.md "Enemy alert state": list the three sortie levels that carry LevelAlertSettings.

## Risks and loose ends

- Future sortie levels cloned from the other 10 originals would need the same component.
- Drowned Shrine 2 and Queen's Chamber both carry the Goblin Queen unit, whose own prefab is always alert on main.

## Proposed commits

1. `feat(home): sortie copies of the Goblin Queen level start enemies alert`: the 3 prefabs above (plain).
2. `fix(tags): Home tag group no longer carries Blood Debt's icon and text`: `GTagSet.asset` (plain).

## Other branches

none

## How to see it

Task A: open each of the three prefabs, select the root (LevelBase instance); the Inspector shows Level Alert Settings with All Enemies Start Alert ticked. In play, start the sortie: enemies are alert from turn 1 (no Unaware state, they act on the first enemy turn).
Task B: open the Tags window or GTagSet asset: `Home` is blank with no icon and not shown in game; Meal, Wounded, Ration, Omen unchanged. Blood Debt on an enemy still shows its icon and text.

## Tests

EditMode run by command line (editor closed): 1139 tests, 1138 passed, 1 failed = the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Results: C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\4a7b2e15-2aac-45e7-9e97-b6e33d04e813\scratchpad\results.xml. The batch run did not modify any other tracked file.
