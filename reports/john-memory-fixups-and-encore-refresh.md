# Report: John memory fix-ups and Encore kit refresh

Plan: none (coordinator brief, D-393/D-394/D-395)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: partial. All edits made; Unity MCP was down and the editor is open, so NOTHING was compiled or run. Editor run still to do.

## What changed

### Chunk A: John memory (onboarding-only)
- `miso/Assets/_Project/Content/Levels/Greybox/GB_m3-john.prefab`: new claw (instance 2457820463989314698) got a `lethalDamageXpBonus: 0` override (minimal YAML); objective text "Defeat 4 Claws" became `Defeat four Claws: {dead_0} of 4.` Nothing else touched by me (claws, turnOrders, lock untouched). Hash before my edit (THJ's state) 0e59d55cff48..., after db474351ae3c....
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs`: KillsToWin 4, TurnCap 3 (comment: ends when turn 4 begins), new text, and a `WireAbilityLock` step that writes the LevelAbilityLock like Linda's wiring does (reuses the existing component, rebuilds `entries` from scratch so a re-run is idempotent): John locks John_Linda + John_Lucy, Linda locks John_Linda + Linda_Lucy, Lucy locks Linda_Lucy + John_Lucy, in the prefab's order. The tool does not set claw XP, so nothing added there.
- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryJohnTests.cs`: first-turn test now checks 5 claws with tile and turnOrder (1,4)=4, (2,5)=3, (4,4)=0, (6,5)=1, (7,4)=2 (matches the review's table); win test renamed `WinningNeedsTheKillCountOrTheTurnCapAndShowsBoth` and also asserts the new text; new `EachHeroIsLockedOutOfTheirTwoDuosAllLevel`; first-turn points check kept.

### Chunk B: Encore kit refresh (general, goes to main)
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTool.cs`: when a listed level already has Encore, the slot is compared with the default kit's slot (`SlotNeedsRefresh`: state name, activation frame, side visual mode, animation event count) and, only if different, overwritten with `CopySlot` (now public). Other slots and levels are not touched; a second run skips matching slots. Summary line reports added and refreshed counts.
- `.../Quiver/Editor/EncoreKitTests.cs`: the default-kit comparison also checks side visual mode; new `ASlotThatDiffersFromTheDefaultKitIsRefreshedOnceAndThenLeftAlone` (instantiates Unit_Linda in memory, breaks the slot, checks refresh decision true, copies, checks false).
- The 9 levels, hand-edited as minimal YAML (frame 5, state Encore, sideVisualMode 1 on the Encore slot override): `Content/Levels/Level1/Level1-C1-2.prefab`, `Level1-C1-2 1.prefab`, `Level1-C2.prefab`, `Level1-C4.prefab`; `Content/Levels/Generic Levels/FamilyLevels/LevelLindaJohn-C1.prefab`, `-C2.prefab`, `-C3.prefab`; `Content/Levels/Generic Levels/Easy/E1/LevelE1-C1.prefab`, `LevelE1-C2.prefab`. Seven edit existing frame/state overrides and add sideVisualMode (slot 4); LindaJohn-C2 (slot 5) and -C3 (slot 6) had no overrides, so three were added. Hash of each before is not archived in the repo; use `git diff` (66 insertions, 14 deletions total).

## Acceptance criteria

- [ ] Hearth tests pass on the prefab: expected by inspection (override added, text, kills/turn cap already in prefab); not run.
- [ ] Re-run of John tool leaves prefab identical: not run (MCP down). Tool writes the same values by construction.
- [ ] `EncoreKitTests` passes; second tool run changes nothing: expected, not run.
- [ ] Clean recompile and full EditMode suite: not run.

## Save reset

no

## Decisions I made

- The refresh decision compares four fields (the test's three plus side visual mode); on mismatch it copies the whole slot.
- Wiring uses its own private `Preset` helper (Linda's is private) and finds heroes by unit name (`Unit_John`, `Unit_Linda`, `Unit_Lucy`).
- The 9 levels were edited by YAML instead of the tool; the tool would produce the same effective values, but Unity may serialise slightly differently (e.g. omit an override equal to the base slot).

## Needs THJ

none

## Docs to update

- Levels plan Segment 3 (claws far away), per the review.

## Risks and loose ends

- Editor run needed: Ctrl+R recompile, run EditMode suite (only `AIRegressionTest.Baseline_MatchesCurrentAI` may be red), then run Tools > Levels > Linda > Add Encore To Custom Kits (should log nothing refreshed) and Tools > Onboarding > Wire Memory 3 (John) and confirm `git diff` on the prefab shows only `-0` noise. Those two runs are the real idempotency check.
- LindaJohn-C2/C3 slot overrides: base slot values of Unit_Linda at slots 5/6 were assumed equal to the old Encore slot (as the earlier tool run implied); the tests will confirm.
- No core file touched.

## Proposed commits

1. `fix(onboarding): John's memory rewires to four kills and a three-turn cap, locks the Duos and keeps the claws free of experience`: GB_m3-john.prefab, HearthMemoryWiring.John.cs, HearthMemoryJohnTests.cs (plain)
2. `fix(linda): the Add Encore tool refreshes an existing Encore slot, and the custom-kit levels get the animated Encore`: EncoreKitTool.cs, EncoreKitTests.cs, the 9 level prefabs (plain). THJ's own Encore files (animation, controller, Unit_Linda, Recall asset) form their own commit before this one.

## Other branches

main gets chunk B (after THJ's Encore files).

## How to see it

1. Recompile, run EditMode tests (Hearth and EncoreKit suites).
2. Play the John memory: 5 claws, "Defeat four Claws: 0 of 4.", no Duo buttons for any hero.
3. Play Level1-C2 as Linda: Encore plays its animation.

## Review fixes

- `EncoreKitTests.cs`: the refresh test now loads its Linda copy with `PrefabUtility.LoadPrefabContents` and releases it with `UnloadPrefabContents` in the `finally` (no scene dirtying). It also asserts `SlotNeedsRefresh(defaultSlot, levelSlot) == false` for every Linda in every level of `EncoreKitTool.Levels`.
- Line endings: the file is LF (also at HEAD, 0 CRLF), not CRLF as the brief said; I kept LF, no BOM.
- Recompiled; console showed only existing warnings (graph view hiding, obsolete InstanceIDToObject, unused field) plus domain-backup and serialization-depth messages that are not from these files. Ran only `EncoreKitTests`: 2 passed, 0 failed. Full suite and menu tools not run (verifier's job).

## Frame 4 refresh (incomplete, Unity MCP dropped)

- Play mode was off (`manage_editor stop` said already stopped).
- Run 1 of Tools/Levels/Linda/Add Encore To Custom Kits: the MCP call returned "session disconnected while awaiting command_result", but Editor.log shows the tool did finish: `[EncoreKitTool] Encore added to 0 kit(s) and refreshed in 9. 0 other level(s) still lack it`. Each of the 9 levels logged "Encore in slot 5 refreshed to the default kit's." Matches the expected 9.
- After that the MCP never came back (read_console and run_tests-side pings unanswered, several retries over about a minute; Editor.log shows MCP websocket send exceptions). Unity.exe is still running. Per instructions I changed nothing further.
- NOT done: run 2 (expect 0 refreshed), EncoreKitTests, full EditMode suite.
- Diff check is inconclusive: the 9 level prefabs were already modified (uncommitted) before this task, so `git diff` against HEAD mixes Chunk B changes with this run. It shows `value: 4` x9 on the Encore activation frame (good), plus Encore stateName / sideVisualMode additions and a few LindaJohn-C2/C3 extra lines that come from the earlier Chunk B refresh (not isolated; no pre-run snapshot was taken). Needs a check of the frame-only delta by a re-run once the MCP is up (a second run reporting 0 refreshed is the idempotence proof).
