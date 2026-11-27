# Memory 3 Shield Dash on turn 2, Memory 2 Claw fade fix (build)

Size: S    Tier: 2 inside THJ's requests (D-795, D-796)    Assigned to: miso-implementer (sonnet)
Branch: all (THJ is on `main`)
Status: done, THJ played; committed b379e85e0, d8d273083, e91e2cded, a7ab72434, 673e82ac7 (not pushed)

THJ hand-tweaked both levels (uncommitted). His layouts stay. Reads: Memory 3 tweak read and hooks, Memory 2 trace (this session; summarised below).

## A. Memory 3: Shield Dash locked on turn 1, unlocked and pulsed on the player's turn 2

Shield Dash = `Resources/UnitSpecific/Player/John/Attack/Secondary/John_Ability_Attack_Dash.asset`.

- [ ] New feature component in `Features/Onboarding/` (e.g. `TurnStartAbilityUnlock`), modelled on `TurnStartActionPointLimit`: faction id, turn number, unit nickname, presets. At that faction's turn start with `CombatLevelRunHandler.TurnNumber == turn`, once, calls `LevelAbilityLock.Unlock(nickname, presets)`. Main thread only, no statics, unsubscribes on disable.
- [ ] `HearthMemoryWiring.John.cs`: John's `LevelAbilityLock` entry also locks Shield Dash (the tool owns the entries, so re-runs keep it); adds the unlock component (Bergsons, turn 2, John, Shield Dash); adds a second `GuidedAbilityHint` on Shield Dash in WhenUnlocked mode. The tool must use `GetComponents<GuidedAbilityHint>()` and match by preset (Memory 4's pattern, `HearthMemoryWiring.Mark.Level.cs`), so the Shield Up hint (turn 1) stays.
- [ ] Run "Tools/Onboarding/Wire Memory 3 (John)" on THJ's tweaked prefab. The prefab diff vs before the run (stash nothing: snapshot the file to the scratchpad first) shows only the lock entry, the new component and the second hint. THJ's board (32 cells, Claws on (4,5) and (4,6)) unchanged.
- [ ] `HearthMemoryJohnTests.TheClawsAreOnTheBoardFromTheStartAndFirstTurnPointsAreLimited`: follow THJ's layout (TO 2 on (4,5), TO 4 on (4,6)).
- [ ] Tests: unlock component unlocks only at the given faction and turn, only once, only listed presets (Duos and Cleanse stay locked); wiring test: Shield Dash locked at start for John, unlock entry at turn 2, two hints (Shield Up Turn 1, Shield Dash WhenUnlocked).

## B. Memory 2: four Claws after Linda's "Two."

Cause: THJ shifted every hidden Claw one column left and deleted column 10; `Memory2Lucy_Interruption_FadeOut.asset` still keeps tiles (9,3) and (9,1), so all ten fade and only the two "four" Claws remain.

- [ ] `HearthMemoryWiring.Lucy.Claws.cs`: `KeptTiles` (8,3), (8,1); `FadingTiles` the eight in columns 5–7 ((5,1) (5,3) (6,1) (6,2) (6,3) (7,1) (7,2) (7,3)); `FourTiles` (9,2), (9,3). Fade asset keep tiles follow.
- [ ] The 12 hidden Claws were saved active (editor toggle left on): set them inactive again in the prefab.
- [ ] `Memory2Lucy_Interruption_CameraToRoom.asset`: room point recomputed from the new positions (it was computed from the old ones), if the wiring computes it; otherwise report.
- [ ] Prefer running "Tools/Onboarding/Wire Memory 2 (Lucy)" with the new constants over hand edits, if it leaves THJ's layout untouched (snapshot first, compare after). Diff must keep his cells and positions.
- [ ] `HearthMemoryLucyTests` pass (incl. the inactive-Claws check).

## C. THJ's editor button

- [ ] `Features/Onboarding/HiddenLevelUnits.cs` `SelectInEditor`: wrap in `#if UNITY_EDITOR` (it calls `UnityEditor.Selection` in a runtime script; player builds would fail). Keep the file's line endings as git stores them (LF).

## Out of scope

`Unit_John.prefab` (THJ's Shield factor 1, D-794): don't touch. Memory 3 role suppression (done).

## Test plan

Covering: `MISO.Core.Features.Onboarding` (HearthMemoryJohnTests, HearthMemoryLucyTests, HearthMemoryLevelsTests, HearthMemoryRulesTests, LevelFamilyRoleSuppressionTests, GuidedAbilityHint and TurnStartActionPointLimit tests), the AbilityLock tests. Then reviewer, then verifier: full EditMode.

## Proposed commits (after THJ's play check)

1. `feat(hearth): only John's Family Role works in his memory` (role suppression files + `GB_m3-john` with THJ's layout) — or folded with 2 if the prefab can't be split.
2. `feat(hearth): John's Shield Dash opens on his second turn with a pulse` (unlock component, wiring, tests, prefab).
3. `fix(hearth): Lucy's memory keeps four Claws after the fade` (M2 prefab, fade/camera assets, wiring, tests).
4. `tweak(john): Shield role takes the full hit` (`Unit_John.prefab`).
5. `fix(onboarding): the hidden units' select button is editor-only` (`HiddenLevelUnits.cs`).
