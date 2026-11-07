# Report: Bond Lite C5 (Yard scene hook)

Plan: plans/onboarding/2026-10-26-bond-lite-tech.md    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done, nothing staged. Tests pass; **nothing has been played**, and this chunk commits only after THJ plays it. One review assumption turned out not to hold (the Yard is not guaranteed to come before the tree panel), so the `OnEnable` refresh is in. One placeholder line for narrative.

Paths are under `miso/Assets/_Project/`.

## What changed

- `Features/Onboarding/BondActivitySequence.cs` (+ `.meta`): new. Sequence step: `AddHomeActivity` for a named pair, grants a named resource amount, saves. Guards its own once-only. Warns and goes on when a piece is missing; takes no time.
- `Features/Onboarding/Editor/BondActivitySequenceTests.cs` (+ `.meta`): new, 14 tests, on a local store and tracker; none touches the save file.
- `Features/Onboarding/Editor/HomeVisitsWiring.cs`: builds the chain; `completionSequence` now gets the chain, so a rerun keeps it.
- `Features/Onboarding/Editor/HomeVisitsTests.cs`: the Yard test reads through the chain; 3 more tests (net +3).
- `Resources/Sequences/HomeVisits/Yard_BondAndFamilyPoint_BondActivitySequence.asset` (+ `.meta`): new. Linda, Lucy, `MainResource_FamilySP`, 1, Play Just Once.
- `Resources/Sequences/HomeVisits/Yard_FamilyTreePointer_DialogNodeSequence.asset` (+ `.meta`): new. The one placeholder line.
- `Resources/Sequences/HomeVisits/Yard_Midnight_SequentialSequence.asset` (+ `.meta`): new. The chain: existing Yard lines, Bond step, pointer line. Play Just Once.
- `Content/Levels/M2 - The Trail.asset`: one line, `completionSequence` points at the chain.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.BondLock.cs`: `OnEnable` refresh (see "Stale panel").

All assets came from `Tools/Onboarding/Wire Home Visits`, run through the menu. Run twice: the second run changed nothing, and the first left no noise (the Trail diff is one line; `Yard_Midnight_DialogNodeSequence.asset`, the Searching look, the Workshop and clue assets are unchanged).

Not touched: C4's files, `AIFactionBrain.cs`, `AIUnitBrain.cs`, the TMP font, `PreloadScreen.unity`, `ProjectSettings/*`, `Home - Scene.unity` (hashes of the font, `PreloadScreen`, both settings files, the Home scene and `SaveData.json` match before and after, including after the test run). No core system file changed. No new statics, so no reset hook.

## Acceptance criteria

- [x] Bond added, one Family point granted, saved: `Apply_AddsTheBond_GrantsTheResource_MarksAndSaves`.
- [x] Grants whatever `AddHomeActivity` returns: `Apply_GrantsWhateverTheBondDoes` (still short, crossing, already past).
- [x] Grants once: `Apply_PaysOnlyOnce...`, `Apply_ANewCopyOfTheStepAfterAReload_StillPaysNothing`.
- [x] Null-safe, warns: no store, no tracker, no resource, no pair, no callbacks, throwing level-up listener.
- [x] The real Trail chain has the dialog, the Bond step and the pointer, in order, both flagged once: `TheTrailPlaysTheYardChainWhenItIsWon_LinesThenBondThenThePointer`, `TheYardsBondStep_PaysTheSistersOneFamilyPoint_Once`.
- [x] EditMode suite: 1586 of 1587 passed (C4's 1570 + 17 new). The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, at 42 failures as in C4's run. A `get_test_job` wait dropped once; calling again returned the result. No compile errors.
- [ ] **Needs THJ's play: the whole path below.** `PlaySequence` itself isn't run by any test, since it reaches the real save. So no test catches the chain failing to play, or the `OnEnable` refresh.
- [ ] **Not verified: after the Yard, Linda-Lucy is Lv 2 in the real game and the nodes open.** The arithmetic is tested by C3 (`Asset_ANormalRun...`, 20 to 23 + 5 = 25 to 28).

## Once-only: what can and can't pay twice

Read from code; the step's own part is tested.

**Trap found:** `SequencePlayer` checks `PlayJustOnce` only on the sequence it's handed. `SequentialSequence` calls its children's `Play` directly, so a flag on a nested step does nothing by itself, and the chain is marked only when its last step ends. So the step checks and marks the played list itself, which is why it takes those as arguments. Both the chain and the step are flagged. They have different asset names, since the list goes by name (tested).

| Case | What happens |
| --- | --- |
| Replay of The Trail, Yard finished | The player skips the chain and calls back at once, so no hang. No scene, no grant. |
| Re-enter Home in the same session | `HomeManager` clears the static right after `Play`. Nothing replays. |
| Fail or abandon The Trail | `EndMission(false)` sets the static to null. No Yard. |
| Hold-to-skip during the lines | The chain skips only dialogue and camera entries, so **the Bond step still runs**, but the pointer line is skipped too. |

## Game closed before the Yard finishes

`MissionCompletionSequence` is a plain static, set in `EndMission`, which has already saved the mission as completed and paid its Bond.

| Closed at | Saved state | Next launch |
| --- | --- | --- |
| During the Home intro, or lines 1 to 4 | Trail completed, Bond 20 to 23, no Yard point | **No Yard at all, and nothing says so.** The sisters' nodes stay locked and the Family tab has no story point. The player can go on to the next missions. |
| Then replays The Trail (completed missions stay on the map) | | Mission end pays nothing (a replay), the chain plays in full, +5 gives 25 to 28: Lv 2 and the point. So a replay repairs it, but nothing tells the player to. |
| During the pointer line | Bond, point and step's mark saved; chain not marked | Next launch nothing. A replay plays the lines again and pays nothing. |

This window is about the length of the intro and four lines, but it loses the only source of the point and the unlock on the main path. I left it, as asked: fixing it means saving "the Yard is owed" and asking for it at Home start. See Needs THJ.

## Save with The Trail already completed (accepted; what the player sees)

- No replay: no Yard ever. Sisters at 15, nodes locked with "Opens with Linda & Lucy's Bond, Lv 2".
- Replay: the chain has never played on that save, so it plays. Mission end pays nothing, +5 gives **20: no Lv 2**. The player still gets the scene and the point, and **Lucy's line says the tree has room for the two of them, while all three sisters' nodes are still locked**. The point can go on another Family node. The chain is now marked, so nothing raises the sisters further except later missions with both of them.

**THJ's current save is not affected:** `The Trail` is `completed: false` there, with no `Bond` or `PlayedSequences` entry yet (read only). It can be played on without a reset.

## Level-up queue: left uncalled

`TakeNextLevelUpScene()` keeps no caller. `levelUpScenes` is empty, so calling it could only drop entries, and playing a scene would mean editing `HomeManager` for a path no asset can exercise. The Yard's Lv 2 therefore sits in `pendingLevelUps` in the save, with any free-slot pair's levels: at most 3 per pair, and harmless.

- This corrects C3's note that "C5 must call it". Whoever adds the first scene adds the call.
- **Don't list Linda-Lucy Lv 2 in `levelUpScenes`:** the Yard delivers it, and its queue entry would play the scene again.
- A new test, `NoLevelUpSceneIsListed_WhileNothingPlaysThem`, fails if someone lists a scene before there's a caller.

## Stale panel: the review's assumption doesn't hold

The order in `HomeManager.StartIE` is right: intro, sequence, then `SetInteractionMode(All)`. But **that mode doesn't gate the stations**. `HomeInteractables` takes clicks through `IPointerDownHandler`, and `ActiveCheckGuard` only covers `PlayerInputController`'s own actions. So during the intro and the lines a station can be clicked, unless something covers it. The dialogue panel's only large raycast target is `ImageFramePanel`, a centred 1453 x 880 rect (alpha 0, `blocksRaycasts` on), not the full screen. I read this from code and the prefab; not played.

As the brief says for this case, I added the refresh on enable: tree and points in Family view, the new-points dots always; skipped on the first enable, before `Start`. It covers a panel opened and closed before the Bond step, then reopened.

**Not covered:** the panel left open with the Family tab showing while the step runs. The lock icon and points label stay old until a tab click or reopen. Clicking a node reads the right level and buying works (per C2). Fixing this needs a `BondLevelReached` subscription, beyond the brief; it's cosmetic and narrow.

## Save reset

No. `SaveData.json` is unchanged (same hash, 2026-11-06 17:24).

## Placeholder text

`Yard_FamilyTreePointer_DialogNodeSequence`, Lucy, right side:

> Then we train together. The Family Skill Tree has room for the two of us now.

- The narrative draft has no line that points at the nodes. Y12-8 to Y12-11 are flavour on the dropped choice cards, and Y12-9 to Y12-11 wait on open question 2. So this is new, mine, and for narrative and THJ to replace.
- **It's marked here and not in the asset:** dialogue doesn't strip `[PLACEHOLDER] ` (checked `DialoguePlayerUI`; only barks do, per `conventions.md`), so a tag would show on screen.
- "Family Skill Tree" is the glossary's term.
- Y12-5 to Y12-7 aren't in the scene, including Margaret's line, which the draft ties to the point. The scene stays the four stub lines, as the brief says.

## Decisions I made

- **Play Just Once on the whole chain as well as the step.** The old stub replayed its lines on every Trail win. A replayed pointer line would be false once the nodes are bought. Same rule as the clue scene.
- **Grant, then Bond, then mark, then save.** `Add` saves at once, so that save already holds the grant (tested). A crash between that save and the mark could pay again on a replay; the reverse order could lose the Bond for good. Paying twice is the milder failure, and the gap is one file write.
- **Missing tracker or store still marks the step.** Otherwise a replay would pay the other half twice. Neither can be missing in a real run: `GameHandler.Initialize` prepares every faction after the load. The panel's later `Prepare` builds a new tracker from the last save, which is why the step saves at once.
- **Pair names and resource are data on the asset**, set by the wiring tool.
- **Refresh in the existing `.BondLock.cs` partial**, and only family view rebuilds the tree, so personal trees behave as before.
- One test class per concern: the step's rules in a new file; the real chain in `HomeVisitsTests`.

## Needs THJ

**Should a Yard interrupted by closing the game come back on its own?**
- Context: closing during the intro or the first four lines leaves no Yard, no point and locked nodes, and only an unprompted replay of The Trail repairs it (table above). The window is short.
- (a) **Recommended for now:** leave it, as briefed, and decide after the playtest. It's rare, and it can be repaired.
- (b) Save "the Yard is owed" at mission end and play it at the next Home start. Closes the hole, but touches `GameHandler` (core) or `HomeManager` and adds a saved field.
- Blocked meanwhile: nothing.

Also still open from C2 and C4, unchanged: what locking Marks-Sisters means, and whether Rivalry's cap is per sister.

## Docs to update

- `tech/home-system.md`: `BondActivitySequence`, the chain, nested steps guarding themselves, `TakeNextLevelUpScene` still uncalled.
- `design/gdd/progression-economy.md`: the story Family point, once per save.
- Plan: C5's row still lists "forced-choice fallback" and "level-up scene". Also a correction to the review note: the Yard isn't guaranteed to precede the panel.
- Narrative draft: the pointer line's slot; Y12-8 to Y12-11 have no home now that the choice is gone.
- `branches.md`, at the `thj/home-test` merge: this step uses `BondStore.AddHomeActivity` directly.
- `tech/core-systems.md`: no change.

## Risks and loose ends

- **A station with a first-open page, clicked during the Yard, may hang the Home start.** Read in code, existing, not new to C5, but a longer chain widens the window. `HomeInteractables.OnPointerDown` calls `SequencePlayer.Play(tutorialSequence)`; the player holds one slot, so that replaces `playingSequence` and `_onComplete`, and `HomeManager`'s `_isPlayingSequence` may never clear, leaving input off. The Workshop's page (`Equipments Cabinet`) is such a sequence, and that station is open by The Trail, so this needs a player who hasn't opened it yet. Check in the play pass (step 6). The same click would also leave the chain unmarked; the step's guard still prevents a second grant.
- **Esc > Quit on The Trail's end panel** (C3's open hole): the mission isn't recorded and pays Bond again on re-entry, and that quit plays no Yard. Later completion plays it once. Numbers run higher; nothing breaks.
- **Scene and unlock can disagree** on a Trail-completed save (above). Accepted.
- **Hold-to-skip hides the pointer line.** The point is still granted, and the Family tab's dot still shows.
- The Family tab opens after The Trail through `requiredMissionToUnlock`, read at the panel's `Start`, which comes after the mission is recorded. Fine in normal flow.
- The `Sequence.name`-keyed list means renaming `Yard_BondAndFamilyPoint_BondActivitySequence` after release would pay again on old saves.
- Not mine and left alone: the files listed under "What changed".

## Proposed commits

Nothing staged. **For after THJ's play check.** C4 should land first: this builds on nothing in it, but the play check runs with it, and the line talks about its node.

1. `feat(onboarding): a sequence step that pays a Home activity's Bond and a family resource once` (plain):
   - `miso/Assets/_Project/Features/Onboarding/BondActivitySequence.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/BondActivitySequenceTests.cs` + `.meta`
2. `fix(home): the skill tree panel shows new Bond locks and Family points when reopened` (plain; independent):
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.BondLock.cs`
3. `feat(onboarding): the Yard raises the sisters' Bond and grants a Family point after The Trail` (mission data; own commit so it can be reverted alone; needs 1):
   - `miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsWiring.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsTests.cs`
   - `miso/Assets/_Project/Resources/Sequences/HomeVisits/Yard_BondAndFamilyPoint_BondActivitySequence.asset` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/HomeVisits/Yard_FamilyTreePointer_DialogNodeSequence.asset` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/HomeVisits/Yard_Midnight_SequentialSequence.asset` + `.meta`
   - `miso/Assets/_Project/Content/Levels/M2 - The Trail.asset`

## Other branches

`thj/home-test`, at merge: the step reads `BondStore`, which that branch's `HomeState` absorbs. Classic has no Yard (C2's note on the locks stands).

## How to see it

Your current save hasn't completed The Trail, so it can stay; a fresh save works too (resetting is your call, I didn't). Save file: `%USERPROFILE%/AppData/LocalLow/Dead Mage/miso/SaveData.json`. Don't use the level sandbox: it leaves Play at mission end, so no Yard.

**Main path, from a fresh save:**
1. Play The Hearth, then The River and The Ridge, then The Trail from the map. Before The Trail, note the Family points shown in the skill tree's Family tab if it's open (it opens after The Trail), or `MainResource_FamilySP` in the `Faction.Bergsons.tracker` entry of the save.
2. Win The Trail. Home's intro plays, then the four lines: "It's past midnight." through "Then we'll be ready."
3. The dialogue box closes and reopens (they are two dialogue steps; judge whether that gap reads badly), with no message about the point, then Lucy says "Then we train together. The Family Skill Tree has room for the two of us now." No tab opens by itself. Input comes back afterwards.
4. Check the save: `Bond` shows Linda-Lucy at 25 to 28, and `PlayedSequences` lists `Yard_BondAndFamilyPoint_BondActivitySequence` and `Yard_Midnight_SequentialSequence`. `MainResource_FamilySP` is 1 higher than before.
5. Open the skill tree, Family tab. Its dot is on and the points label counts the new point. Tempest Bloom, Marks-Sisters and Sister's Rivalry show no lock and no "Opens with..." line. Buy one: it costs 1 and nothing forces the choice.

**During the Yard (the panel assumption):**
6. On another run of the Yard (a save from before The Trail), click stations during the intro and the lines, especially where the dialogue doesn't cover the screen.
   - If the skill tree (`Grandma Table`) opens: pick the Family tab, close it, wait for the Yard to end, reopen. The lock must be gone and the points right.
   - If the Workshop's first-open page opens during the lines: **does Home's input come back afterwards?** See Risks.

**Once-only:**
7. Replay The Trail from the map and win. No Yard, no change to `Bond` or `MainResource_FamilySP`, no hang at Home.
8. Pre-Trail save, win The Trail, and stop Play or close the game during the Yard's second line. Relaunch: no Yard, Bond 20 to 23, nodes locked, no new point. Replay The Trail: the Yard plays in full and Lv 2 and the point arrive.
9. Pre-Trail save, stop Play during Lucy's pointer line. Relaunch and replay The Trail: the lines play again, and `Bond` and the point don't change.
10. Hold skip during the lines: the pointer is skipped too, and the Bond and point still land.

**Throughout:** the console shows no `BondActivitySequence` warnings (`Debug.LogWarning` lines would mean a missing piece). Then C4's combat checks, now with a bought Rivalry from the real path.

## Review (coordinator's condensed copy, 2026-11-07)

**FIX.** Read only. Must fix: stale description after `OnEnable`. Should fix: station clicks during Home's opening (D-429). Once-only guard saved under `PlayedSequences`; partial grant impossible in the normal path; a crash between the two saves can pay again on a replay, accepted. Skip path ends cleanly. 16 points add up. Queue bounded at 3 per pair. Open: Yard interrupted before the step leaves no point until a replay; later missions can still lift the Bond and open the nodes. Left, decide after the playtest.
