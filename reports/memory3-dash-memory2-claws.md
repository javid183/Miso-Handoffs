# Report: Memory 3 Shield Dash on turn 2, Memory 2 Claw fade fix

Plan: plans/2026-11-27-memory3-dash-memory2-claws.md    Agent: miso-implementer    Branch: main
Outcome: done (play check by THJ / verifier still open)

## What changed

Part A (Memory 3 Shield Dash, D-786)
- `Features/Onboarding/TurnStartAbilityUnlock.cs` (+ `.meta`, new): level component; at one faction's turn N start (once) calls `LevelAbilityLock.Unlock(nickname, presets)`. Same shape as `TurnStartActionPointLimit` (bus subscription with the 600-frame wait, unsubscribes on disable, no statics). Testable core `TryApply(startedFaction, turn, lock)` and static `Matches`.
- `Features/Onboarding/Editor/TurnStartAbilityUnlockTests.cs` (+ `.meta`, new): 6 tests.
- `Features/Onboarding/Editor/HearthMemoryWiring.John.cs`: `ShieldDashPath`, `ShieldDashTurn = 2`; John's lock entry gets Shield Dash; new `WireShieldDashUnlock` (Bergsons, turn 2, John's nickname, Shield Dash); new `WireHints` uses `GetComponents<GuidedAbilityHint>()` and claims each hint by its preset (Shield Up = Turn mode turn 1; Shield Dash = WhenUnlocked), reusing a stray hint or removing extras. Class summary updated. NOTE: this file also carries the earlier, uncommitted role-suppression hunks (`RoleSuppressedUnitNames`, `WireRoleSuppression` and its call); my hunks are the ones above.
- `Features/Onboarding/Editor/HearthMemoryJohnTests.cs`: Claw tiles follow THJ's layout ((4,5) TO 2, (4,6) TO 4 replace (7,4) and (1,4)); Shield Up hint found by preset and checked as Turn mode 1..1; John's lock expectation includes Shield Dash; new `ShieldDashIsLockedForJohnUntilTheSecondTurnAndPulsesWhenItOpens`.
- `Content/Levels/Greybox/GB_m3-john.prefab`: re-wired by "Tools/Onboarding/Wire Memory 3 (John)" (diff below).

Part B (Memory 2 Claws, D-785)
- `Features/Onboarding/Editor/HearthMemoryWiring.Lucy.Claws.cs`: `KeptTiles` (8,3),(8,1); `FadingTiles` (5,1)(5,3)(6,1)(6,2)(6,3)(7,1)(7,2)(7,3); `FourTiles` (9,2),(9,3). Same order as the units already listed in THJ's hidden groups, so the group lists did not reorder.
- `Content/Levels/Greybox/GB_m2-lucy.prefab`: the 12 hidden Claws saved inactive again (diff below).
- `Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Interruption_FadeOut.asset`: keep tiles (9,3),(9,1) -> (8,3),(8,1).
- `Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Interruption_CameraToRoom.asset`: room point (4, 1.25) -> (3.5, 1.25), recomputed by the wiring from the ten Claws' new positions.

Part C (editor button)
- `Features/Onboarding/HiddenLevelUnits.cs`: THJ's `SelectInEditor` (with its `[Button]`) wrapped in `#if UNITY_EDITOR`, one comment line; the file's CRLF lines that came with that method are now LF like the rest of the file (git stores it LF).

## Acceptance criteria

A
- [x] New turn-start unlock component, modelled on `TurnStartActionPointLimit`, main thread, no statics, unsubscribes on disable: `TurnStartAbilityUnlock.cs`.
- [x] Wiring: John's lock entry also locks Shield Dash, unlock component (Bergsons, 2, John, Shield Dash), second hint in WhenUnlocked mode, hints matched by preset: prefab diff and `HearthMemoryJohnTests.ShieldDashIsLockedForJohnUntilTheSecondTurnAndPulsesWhenItOpens`, `TheShieldUpButtonPulsesOnTheFirstTurn`, `EachHeroIsLockedOutOfTheirTwoDuosAndCleanseAllLevel`.
- [x] Wire Memory 3 run on THJ's prefab; diff vs the pre-run copy shows only the lock entry, the new component and the second hint, plus two cell renames by `GridCell.OnValidate` (see below). Board still 32 cells, Claws on (4,5) and (4,6), no position changed.
- [x] Claw-position test follows THJ's layout: `TheClawsAreOnTheBoardFromTheStartAndFirstTurnPointsAreLimited` passes.
- [x] Unlock tests (faction and turn only, once, only listed presets; Duos and Cleanse stay locked; per-unit): `TurnStartAbilityUnlockTests` 6/6.
- [ ] Shield Dash really hidden on turn 1 and pulsing on turn 2 in play: needs the play check.

B
- [x] Tile constants follow THJ's layout; fade keep tiles follow: `FadeOut.asset` diff, `TheInterruptionBringsInTenFadesEightAndBringsInTwoBetweenTheLines`.
- [x] 12 hidden Claws inactive in the prefab: `TwelveCuedClawsAreHiddenInTwoGroupsOnTheirTiles` (checks `activeSelf` false).
- [x] Room camera point recomputed by the wiring: `CameraToRoom.asset` (4 -> 3.5 on x).
- [x] Wire Memory 2 run rather than hand edits; THJ's cells and positions untouched (diff below).
- [x] `HearthMemoryLucyTests` 15/15.
- [ ] Four Claws left after "Two." and "Four." in play: needs the play check.

C
- [x] `SelectInEditor` inside `#if UNITY_EDITOR`; file LF. Compiles in the editor; a player build was not made.

## Chunks

### Chunk 1: whole plan (A, B, C)

- Changed: see "What changed".
- Criteria met: see "Acceptance criteria".
- Decisions and loose ends: see the sections below.

### Prefab diffs against the pre-run copies

Copies taken before any run: scratchpad `pre/GB_m3-john.prefab`, `pre/GB_m2-lucy.prefab`, `pre/m2/*.asset`, `pre/m3/*.asset` (session scratchpad `C:\Users\DEADMA~1\AppData\Local\Temp\claude\7164f0fa72557ceb\1d105d68-3848-4daf-abdd-ef85b8b8daae\scratchpad\`; full diffs `m3-prefab.diff`, `m2-prefab.diff` there).

`GB_m3-john.prefab` (53 diff lines):
- `LevelAbilityLock` John entry: Shield Dash (guid 9958a1ca...) inserted before Cleanse (Duo, Duo, Shield Dash, Cleanse). Sister entries unchanged.
- New `TurnStartAbilityUnlock` on the level object: Bergsons, turn 2, `unitNickname: John`, Shield Dash. Plus its `m_AddedComponents` entry.
- New second `GuidedAbilityHint`: Shield Dash, `startMode: 1` (WhenUnlocked). Plus its `m_AddedComponents` entry. The existing Shield Up hint is unchanged.
- Not planned: two cell instances THJ left named plain `GridCell` were renamed `GridCell - (5, 4)` and `GridCell - (3, 4)` (an `m_Name` override each). This is `GridCell.OnValidate`, which names every cell after its position whenever the prefab is loaded for editing; THJ's own next save in the prefab editor does the same. No cell or unit moved; the board is still 32 cells. I kept the names (they now match the rest of the board and the tests' cell reading); restoring "GridCell" would be undone by the next edit.
- No Memory3John sequence asset changed.

`GB_m2-lucy.prefab` (48 diff lines): only 12 `m_IsActive` overrides 1 -> 0, one per hidden Claw ((8,3) (8,1) (5,1) (5,3) (6,1) (6,2) (6,3) (7,1) (7,2) (7,3) (9,2) (9,3)). The wiring run itself changed nothing further in the prefab (byte-identical to the state after the deactivation step). The two stage-one Claws ((4,2), (3,3)) and Lucy untouched.

How B was run: the wiring's `HiddenClawOn` refuses a tile that holds an active unit, and THJ's Claws were saved active, so running "Wire Memory 2 (Lucy)" first would have thrown. I first set the 12 listed Claws inactive with a one-off editor step (`PrefabUtility.LoadPrefabContents`, `SetActive(false)` on each unit in the hidden groups, save; run through the Unity MCP, no file kept), diffed (12 `m_IsActive` lines only), then ran the wiring.

## Reviews and checks

- (written by the coordinator)

Tests run in THJ's open editor (Unity MCP, EditMode):
- `^MISO.Core.Features.Onboarding.` + `^MISO.Content.Levels.EditorTests.` (all Onboarding fixtures incl. HearthMemoryJohn/Lucy/Levels/Rules, LevelFamilyRoleSuppression, GuidedAbilityHint, TurnStartActionPointLimit, the new TurnStartAbilityUnlock, and the AbilityLock tests): 820/820 passed.
- Then `TurnStartAbilityUnlockTests`, `HearthMemoryJohnTests` (10), `HearthMemoryLucyTests` (15), `HiddenLevelUnitsTests` (4) with details: 35/35 passed.
- Full EditMode suite not run (verifier's step). `AIRegressionTest` not run: no AI graph, AI ability or unit prefab changed.

## Save reset

No.

## Decisions I made

- Unlock component stores the unit as a nickname string (as the plan says); the wiring fills it from the placed John's `Nickname` ("John"). The level's lock is looked up on the same object, falling back to `FindAnyObjectByType`, only when the matching turn starts.
- Turn number: `CombatLevelRunHandler.TurnNumber` increments when the turn index wraps to 0, so "turn 2" is the player's second turn when Bergsons go first (same assumption as the Mark level's turn-1 limit).
- Without a lock in the level the component warns once and counts as applied (no retry each turn).
- Hint matching: a hint is claimed by its preset; failing that, a hint on some other preset is reused; failing that, one is added; leftovers are removed (Mark level does the same by index).
- Memory 2 Claws deactivated with a one-off editor step before the wiring run (the wiring refuses active units on hidden tiles); the outcome is the plan's.
- Kept the two `GridCell` renames that `GridCell.OnValidate` made on load (see diffs).
- Part C: the CRLF lines in THJ's method became LF (plan: keep the file LF as git stores it).

## Needs THJ

none

## Docs to update

- `design/demo-spec.md` / Memory 3 notes: Shield Dash locked on the first player turn, opens and pulses at the start of the second.
- Memory 2 notes, if they list tiles: hidden Claws now kept (8,1)/(8,3), fading in columns 5-7, the "four" on (9,2)/(9,3).

## Risks and loose ends

- `HearthMemoryWiring.John.cs` and `GB_m3-john.prefab` mix the role-suppression change (commit 1) with this one (commit 2). Splitting needs hunk-level staging of the .cs; the prefab can't be split cleanly, so fold commits 1 and 2 or commit the prefab with commit 2.
- `HearthMemoryWiringLucy.HiddenClawOn` throws when a hidden Claw is left active (THJ's "Toggle Visible In Editor" button does exactly that). A re-run after toggling will fail until they are toggled back. Not changed (outside the plan); a small follow-up could let the tool accept and switch off its own Claws.
- The comment "throat mouth (5,2, left free)" in the Lucy Claws file still holds: (5,2) is still free, and the existing test still checks it. Column 4 now has only (4,2), which holds a stage-one Claw.
- The Shield Dash hint runs until Shield Dash is used (WhenUnlocked mode ignores turns), so if John never dashes it keeps pulsing every later turn. That is the existing WhenUnlocked behaviour (Lucy's Cyclone and Mark's Duo do the same).
- No player build was made to confirm Part C; the change is a plain `#if UNITY_EDITOR`.

## Proposed commits

1. `feat(hearth): only John's Family Role works in his memory`: `LevelFamilyRoleSuppression.cs` + `.meta`, `LevelRoleZoneHidden.cs` + `.meta`, `Editor/LevelFamilyRoleSuppressionTests.cs` + `.meta`, the role-suppression hunks of `Editor/HearthMemoryWiring.John.cs` (plain). If hunk staging is not wanted, fold into 2.
2. `feat(hearth): John's Shield Dash opens on his second turn with a pulse`: `Features/Onboarding/TurnStartAbilityUnlock.cs` + `.meta`, `Editor/TurnStartAbilityUnlockTests.cs` + `.meta`, `Editor/HearthMemoryWiring.John.cs` (rest), `Editor/HearthMemoryJohnTests.cs`, `Content/Levels/Greybox/GB_m3-john.prefab` (with THJ's layout) (plain).
3. `fix(hearth): Lucy's memory keeps four Claws after the fade`: `Editor/HearthMemoryWiring.Lucy.Claws.cs`, `Content/Levels/Greybox/GB_m2-lucy.prefab`, `Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Interruption_FadeOut.asset`, `Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Interruption_CameraToRoom.asset` (plain).
4. `tweak(john): Shield role takes the full hit`: `Features/Player/John/Prefabs/Unit_John.prefab` (THJ's; untouched by me).
5. `fix(onboarding): the hidden units' select button is editor-only`: `Features/Onboarding/HiddenLevelUnits.cs` (plain).

All paths under `miso/Assets/_Project/`. `miso/miso.slnx` is IDE noise from before this task; don't stage it.

## Other branches

none

## How to see it

Memory 3 (John):
1. Open the John memory (`GB_m3-john`) from the Hearth, or play it directly.
2. Player turn 1: John's bar shows Shield Up pulsing and no Shield Dash button.
3. End the turn; after the enemies act, at the start of player turn 2 the Shield Dash button appears on John's bar and pulses. Duos and Cleanse stay hidden.
4. Use Shield Dash: the pulse stops.

Memory 2 (Lucy):
1. Play the Lucy memory (`GB_m2-lucy`). The 12 Claws in the right room are not visible at the start.
2. Kill the first two Claws. "Then ten more!" brings in ten; after Linda's "Two." eight fade and two stay, on (8,1) and (8,3).
3. After "Four." two more come in on (9,2) and (9,3): four Claws on the board.
4. The camera move to the room is centred on the ten (half a tile further left than before).
