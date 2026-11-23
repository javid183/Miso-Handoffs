# Report: Chunk 1.2, enemy intros play last in the memories

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.2, item H-01, decision D-611)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (data and tools); one residual HUD timing sits in core and is listed under "Needs THJ"

## What changed

- `Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Start_SequentialSequence.asset`, `Memory2Lucy/Memory2Lucy_Start_SequentialSequence.asset`, `Memory3John/Memory3John_Start_SequentialSequence.asset`: the last two steps (`EnablePlayerInputSequence`, `ShowHUDSequence`) are removed. Two-line YAML edits each; nothing else in them changed.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Bloom_SequentialSequence.asset`: the same two steps removed. Memory 4's intro already left input and the HUD off. They came back at the end of the Bloom cut-in, which plays when the level starts and before the first turn, so the Bloom list is memory 4's real "start" list.
- `Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`, `.Lucy.cs`, `.John.cs`: a fresh start asset gets the new order (no input or HUD steps at the end), plus a two-line comment.
- `Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs`: the Bloom list in the tool matches the asset, and the two comments now say why. The tool has no menu and memory 4 is hand-owned. This change keeps `WiringSeed` from warning about a structure mismatch if it is ever run.
- Tests:
  - New `Features/Onboarding/Editor/HearthMemoryIntroOrderTests.cs` (+ `.meta`, 12 cases over the four memories).
  - `HearthMemoryLucyTests.cs`: the start-page test no longer needs an input step. It is renamed `TheStartShowsTheFireEmbersPageAfterLucysLineAsItsLastStep`.
  - `HearthMemoryMarkTests.Flow.cs`: the Bloom test now asserts that neither step is there. One comment in the intro test changed.

No core file, prefab or scene changed.

## Cause, verified

- `CombatLevelRunHandler.StartLevelIE` runs in this order:
  1. `PlayIntro` (the memory's start list).
  2. `AbilityIntroductionTracker.PlayPending`.
  3. `levelStarted` (memory 4's Bloom).
  4. `StartTurn()`.
  5. `ShowHUD()`.
- `PlayerController.StartTurn` starts `StartTurnWithIntroductions`. That coroutine waits for any sequence in progress, plays the cards, and then calls `SetInteractionMode(All)`.
- The cards (`EnemyIntroductionController.PlayPending`) fade `MainCanvas` to 0.01 and set Pause mode, then put both back.
- So the start lists' `EnablePlayerInputSequence` / `ShowHUDSequence` handed input and the HUD back at the end of the intro. They stayed on through the ability introductions and up to the cards.

**Does the turn start show the HUD?** `StartTurnWithIntroductions` does not. But `StartLevelIE` always calls `ShowHUD()` right after `StartTurn()`, with or without cards, so a level still gets its HUD. Input comes back on its own too:
- `SetInteractionMode(All)` also sets `_inputActive` (`PlayerInputController.SetInteractionMode`: `_inputActive = _inputActive || mode != None`).
- That covers the card path (after the cards) and the no-card path (straight away in `StartTurn`).

That is why `ShowHUDSequence` could go.

**The Dark Claw intro:** none of the four start lists reveals or introduces a Claw. Memories 1 to 3 hold only dialogue and tutorial pages (plus the grid fade in 2 and 3). Memory 4 holds the grid fade, Mark's opening and two camera moves. The Dark Claw card is an enemy introduction card, so it already plays after the opening sequences. Nothing to move. A new test keeps it that way (`NoEnemyIsRevealedInTheIntro`).

## Acceptance criteria

- [x] In each memory, no input shows before the enemy cards. Evidence:
  - `HearthMemoryIntroOrderTests.NothingThatPlaysAtTheStartGivesInputOrTheHudBack` (4 memories). It walks the intro and every level-start `SequencePlayHandle` sequence, recursively.
  - `TheIntroTakesInputAndTheHudAwayFirst` (4).
  - Code read of the input path above.
- [~] In each memory, no HUD shows before the cards: **the memories no longer show it, but core still starts it early.**
  - The start lists no longer show the HUD (same tests).
  - Core `StartLevelIE` still starts `ShowHUD()` in the same frame as `StartTurn()`. The cards wait one frame plus `startupDelay` (0.25 s), then fade the main canvas out over 1 s.
  - So the HUD panels begin to slide in about a quarter second before the dim begins, and fade with the canvas.
  - Before this change, the HUD was fully up from the end of the intro, through any ability introduction, until the cards.
  - Removing the rest needs core or the cards' controller: see "Needs THJ". **Play check:** judge whether the remaining slide-in reads as a flash.
- [x] A level with no pending cards still gives input and HUD. Code read:
  - `PlayerController.StartTurn`'s no-card branch calls `SetInteractionMode(All)`.
  - `StartLevelIE` calls `ShowHUD()` unconditionally after `StartTurn()`.
  - Memory 4 already relied on this on every replay with no new names. **Play check:** replay a memory whose enemies are already seen.
- [x] Wiring tests updated and pass:
  - Covering fixtures (IntroOrder, Linda, Lucy, John, Mark, Levels, WiringSeed): 95 of 95 passed.
  - `HearthMemoryIntroOrderTests` alone: 12 of 12 passed (checked by full class name).
  - Clean compile, no console errors.
  - Full EditMode suite: see the next line.
- Full EditMode suite (one run after chunks 1.2 and 1.5): 2529 total, 2525 passed, 1 skipped (the Explicit AI regression test), 3 failed, all "m_LockCount == 0" in `GridToLevelFacingTests`, `GridToLevelSettingsTests` and `GridToLevelXpTests` (the known editor-open flake). Rerun alone, those three fixtures passed 34 of 34. So: 0 real failures.

## Chunks

### Chunk 1.2: enemy intros play last

- Changed: see "What changed".
- Criteria met: input and the no-card case met; the HUD criterion met on the data side, with the core timing above left.
- Decisions and loose ends: below.

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- Memory 4: the steps came off the Bloom cut-in, not the intro. The intro already ended without them; the Bloom (played on `levelStarted`, before the first turn) handed them back right before the cards. Same intent as the brief.
- I updated the memory 4 tool's Bloom list too, though the brief named only memories 1 to 3. It has no menu and doesn't own the asset; this only keeps its structure check quiet. Equivalent behaviour.
- The new checks sit in one new fixture over the four memories rather than four edits to the per-memory files. The per-memory files were only touched where an existing assertion broke.

## Needs THJ

**The HUD still starts to slide in a quarter second before the enemy cards.**
1. **What:** core `CombatLevelRunHandler.StartLevelIE` calls `ShowHUD()` right after `StartTurn()`. The cards begin their dim after one frame plus 0.25 s.
2. **Why it matters:** in every level with new enemies, the HUD panels begin to appear and then fade out with the canvas. It is much shorter than before, but it may still read as a flash.
3. **Options:**
   - (a) Leave it and judge it in the play check.
   - (b) Non-core: in `EnemyIntroductionController` (Features), start the canvas fade before the startup wait when cards are pending (Tier 2). This changes the cards' own timing.
   - (c) Core: `StartLevelIE` shows the HUD only after the player controller's introductions finish (Tier 3, core).
4. **Recommendation:** (a) first, then (b) if it shows.
5. **Default if no answer:** (a).

## Docs to update

- `tech/onboarding-merge.md` or the memory notes, if they describe the start lists: they now end on the last page or line. The turn start gives input back after the enemy cards, and core shows the HUD.

## Risks and loose ends

- **Overlap with chunk 1.1** (uncommitted): `HearthMemoryWiring.Linda.cs`, `.Lucy.cs`, `.John.cs` and `HearthMemoryLucyTests.cs` also hold 1.1's hunks. My hunks are separate (start lists, comments, one test method), so 1.1 should be committed first, or staged by hunk. No overlap in the prefabs: this chunk changed none.
- **Memory 4, pre-existing:** core's `ShowHUD()` after `StartTurn()` already runs while the Bloom cut-in is still playing (the Bloom's `HideHUD` starts first, then core's `ShowHUD` overrides it, because `UIPanelAnimator.Show` kills the hide tween). So the HUD may be visible during the Bloom; this change doesn't make that worse. Worth a look in the play check.
- **Memory 4, input during the Bloom:** when no cards are pending (all names seen), `StartTurn` sets input to All while the Bloom still plays. This is pre-existing: before, the Bloom's own Disable step came first too.
- **Mid-level interruptions** (memories 1 and 2: reveal, turn reset) still end with Enable and ShowHUD. Their reset gives a fresh turn, so any new name's card would play after them. Out of scope (H-01 is about the start); the Claws are already seen by then in the normal flow.
- **Search levels** (left alone, rebuilt in Phase 3). What they'd need under the same rule:
  - Ridge (`SearchWiring.Ridge.cs`) and River (`SearchWiring.River.cs`): start lists end with Enable and ShowHUD. Drop both. The `SearchRidgeTests:247` and `SearchRiverTests:144` asserts (`ShowHUDSequence` last) change with them.
  - Trail's Trailhead (`SearchWiring.Trail.cs:193-198`): the same; `SearchTrailTests:333` checks step 5 is Enable.
  - The first-sleeper beat (`SearchWiring.Shared.cs:63`, played on `levelStarted`) and the Trail arrivals (`SearchWiring.Trail.Arrivals.cs:34`) end with Enable only. The first-sleeper one plays before the first turn, so it would need its Enable dropped as well. The arrivals play mid-level.
- Unity may rewrite the TMP fallback font asset during a session; it isn't part of this work.

## Proposed commits

1. `tweak(onboarding): memory openings leave input and the HUD to the turn start, so enemy intros come first` (plain; after chunk 1.1's commits, because the three wiring tools and the Lucy tests share files with it):
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Start_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory2Lucy/Memory2Lucy_Start_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory3John/Memory3John_Start_SequentialSequence.asset`
   - `miso/Assets/_Project/Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Bloom_SequentialSequence.asset`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs` (this chunk's hunk)
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs` (this chunk's hunk)
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs` (this chunk's hunk)
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Mark.Sequences.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLucyTests.cs` (this chunk's hunk)
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryMarkTests.Flow.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryIntroOrderTests.cs` + `.meta`

## Other branches

none

## How to see it

1. `Tools > Save Data > Clear Save Data`, so the enemy cards (and memory 4's Bloom) play again.
2. Start a new game and play into memory 1. After Margaret's line and the "Moving and AP" page, the HUD should stay hidden and clicks should do nothing. Then the Dark Claw card dims the screen. When it ends, the HUD is up and you can play.
3. Watch the quarter second between the page closing and the dim. Report whether the HUD's slide-in reads as a flash (see "Needs THJ").
4. Replay memory 1 without clearing the save (no new names, so no card). Input and the HUD come back right after the page.
5. In memory 4, after the Bloom cut-in (John's call to Linda), any new enemy's card plays before input returns.
