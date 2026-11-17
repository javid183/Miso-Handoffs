# Report: Onboarding wiring stops owning dialogue text

Plan: plans/2026-11-11-wiring-leaves-dialogue-tech.md    Agent: miso-implementer    Branch: main
Outcome: done (C1, C2, C3). Several structure disagreements are listed under "Needs THJ". No data was changed.

## What changed

Every path is under `miso/Assets/_Project/Features/Onboarding/Editor/`. All files are LF with no BOM, the same as before.

- `WiringSeed.cs` (new) + `.meta`: the shared helper. `Dialogue(path, seed)` creates the asset and runs the seed only when the asset is missing. An existing dialogue comes back untouched: text, speaker, side and node count all stay. `StepList(path, steps)` writes a step list only when it creates it. An existing list is kept. If the existing list differs from the wiring's in more than its dialogue steps, the helper logs a warning that names both versions. `SameApartFromDialogue` is the comparison it uses.
- `HearthMemoryWiring.Linda.cs`: `BuildDialog` and `BuildSequential` now go through `WiringSeed`, so every wiring uses the same rule. `BuildDialog` takes an optional `onSeed` that runs only on a new asset. The caption speaker's asset path is fixed: the teammate renamed `Narrator_DialogueCharacter.asset` to `TopNotification_DialogueCharacter.asset`. Before the fix, seeding any `Who.Narrator` line threw FileNotFound. The class summary is updated.
- `SearchWiring.Trail.cs`, `SearchWiring.Trail.Arrivals.cs`: `SpeakAsThePick` (which routes a line to the generic slot) now runs through `onSeed`. It applies only to a new dialogue, so speaker edits made in Unity win.
- `HomeVisitsWiring.cs`, `SearchWiring.River.cs`: doc comments updated to the new rule.
- `WiringStructureAsserts.cs` (new) + `.meta`: shared structural test checks:
  - `AssertSpokenLine`: the step is a dialogue with at least one line, and every line has text and a speaker.
  - `AssertEndFadesOutAndStaysOut`: the grid fade-out comes before the last line, and nothing fades the grid back in. The end must either have `OutroCutsceneKeepGridHidden` after the last line, or finish on a TransitionToNextLevel step.
  - `AssertNoNamedPickSpeaker`: no line is spoken by John or Mark by name.
- `WiringSeedTests.cs` (new) + `.meta`: 6 tests for the helper. They use a temporary `Assets/WiringSeedTests_Temp` folder that is deleted in TearDown.
- Tests that stopped asserting wording, speakers and `Narrator`: `HearthMemoryJohnTests`, `HearthMemoryLindaTests`, `HearthMemoryLucyTests`, `HearthMemoryMarkTests.Flow`, `HomeVisitsTests`, `HomeVisitsTests.Hearth`, `SearchRiverTests`, `SearchRidgeTests`, `SearchTrailTests`.
- `HomeMemoryOpeningTests.cs` (C2): replaced the Play-mode-only `SceneManager.CreateScene` with `EditorSceneManager.NewPreviewScene()`. TearDown closes the scenes with `ClosePreviewScene`. The test bodies are unchanged.

## Acceptance criteria

- [x] **Text:** existing dialogue keeps its lines, and the seed is written only when the wiring creates the asset. One shared helper serves every wiring. Evidence: `WiringSeedTests.AnExistingDialogueKeepsItsLinesSpeakersSidesAndNodeCount`, `ANewDialogueGetsTheSeedLines`, and the re-run below.
- [x] **Structure:** the wiring still writes cameras, reveals, input steps, panels, objectives, level data and mission data, as before. An existing step list is never rewritten. When only its dialogue steps differ (River and Ridge: the teammate swapped in their own `MS1_*` and `MS2_*` dialogues), the wiring keeps it without a message. When the structure differs, the wiring keeps it and warns in the console. On the current assets it warns three times: Memory 1, 2 and 3 end. Every disagreement is listed below under "Needs THJ". Neither side was changed.
- [x] **Tests:** they now assert structure and invariants. The pairs are listed below. No current asset breaks an invariant from the plan, so no test is red as a finding. The places where I loosened an order assert are listed as disagreements.
- [x] **Re-runs:** I snapshotted the md5 of all 396 `.asset` files under `Resources/Sequences/` (Hearth, Search, HomeVisits, MS3, Common) and `Content/Levels/*.asset`. They matched HEAD (`b1f9d1f68`, the merge commit) before the runs. I then ran Wire Memory 1, 2 and 3, Wire Hearth Result Lines, Wire Search: River, Ridge and Trail, and Wire Home Visits, twice. After each pass the md5 check matched, and `git status` showed no change to any asset, prefab or mission. No revert was needed. Memory 4 has no menu, because that wiring is retired.
- [x] **C2:** the 3 `HomeMemoryOpeningTests` pass in edit mode, with each test's intent unchanged.
- [x] **C3 GridToLevel:** `CameraStart`, `Facing` and `Settings` all pass in the open editor. The `m_LockCount == 0` failure only happens on the command line.
- [x] **Full EditMode in the editor:** 1893 tests, 1892 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, which was not touched.

Coverage: all criteria are covered by EditMode tests or by the md5 re-run check. No play check is needed, because there is no runtime change.

### Removed assert → structural replacement

| Test | Removed | In its place |
| --- | --- | --- |
| John `TheGridIsHiddenAtOnceThenFadesInBeforeJohnSpeaks` | contains "Stay where I can reach you." | `AssertSpokenLine` on the opening. The hide, fade-in, line, panel order is kept. |
| John `TheEndFadesTheGridOut...` | contains "You both did."; cutaway opens on the still image; punchline before fade | punchline before cutaway, `AssertSpokenLine` on both, `AssertEndFadesOutAndStaysOut` |
| Linda `TheEnd...` (renamed from `TheEndPlaysThePunchlineThenFades...` to `TheEndFadesTheGridOutAndKeepsItOutThroughTheCutaway`) | finds the punchline by "Seven Claws. One arrow."; fade after punchline; still image plus its sprite; keep-hidden after cutaway | punchline before cutaway, the fade is a GridVisualSequence, `AssertSpokenLine` on both, `AssertEndFadesOutAndStaysOut` |
| Linda `TheStartHasTheHearthLine...` | the single line contains "Linda" | `AssertSpokenLine`. There is still exactly one dialogue step, before the panel. |
| Lucy `TheGridIsHiddenAtOnceThenFadesInBeforeLucySpeaks` | contains "Very brave" | `AssertSpokenLine`. The hide, fade-in, line order is kept. |
| Lucy `TheInterruptionBringsInTen...` | "Then ten more!", "Two.", "Four." | `AssertSpokenLine` on each of the 3 dialogue steps. The step count and the reveal, fade and camera order are kept. |
| Lucy `TheFirstStageEndsOnTwoDeaths...` | "Then ten more!" | `AssertSpokenLine` |
| Lucy `TheEndFadesTheGridOut...` | the punchline, fade, cutaway, keep-hidden order; still image | `AssertSpokenLine` on every end dialogue, `AssertEndFadesOutAndStaysOut` |
| Mark `TheIntroFadesTheGridInUnderMarksOpening` | the two opening lines | `AssertSpokenLine`. The order is kept. |
| Mark `TheBloomCutIn...` | the three calls' texts | `AssertSpokenLine` on each. The order is kept. |
| Mark `TheArrival...` | the boast and arrival texts | `AssertSpokenLine` on each |
| Mark `TheHold...` | John's lines and the Duo lines | `AssertSpokenLine` on each |
| Mark `TheEnding...` | mother and cub texts; fade after the cub; still image; "Ten Claws, Lucy." spoken by John | `AssertSpokenLine` on mother, cub and cutaway. The ledge, fall, mother, Lucy walk, Mark walk, cub, cutaway order is kept. `AssertEndFadesOutAndStaysOut` |
| HomeVisits Hearth close | speakers Lucy, Narrator, Narrator, Lucy, Mark; "Margaret:", "fire burned low", "Ryker"; one rule line spoken by John | `AssertSpokenLine` on the close and on the rule. The 3-step chain, play-once and page step are kept. |
| HomeVisits clue scene | speakers Lucy, Mark, Linda, John, Lucy | `AssertSpokenLine`. Play-once is kept. |
| HomeVisits Yard chain | the speakers and two texts of the Yard lines; Narrator x2, "Bond reached Lv 2.", "Margaret:"; one pointer line | `AssertSpokenLine` on the Yard lines, the Bond lines and the pointer. The 6-step chain and its step types are kept. |
| River `TheStart...` (renamed to `TheStartVisitsTheClueAndComesBackThenShowsLucysRole`) | a line before the camera and "Stay by me." after the panel | camera to clue, camera back, panel order; at least one dialogue; `AssertSpokenLine` on each. The first and last steps are kept. |
| River `TheClueStands...` | contains "Someone was here with her." | `AssertSpokenLine`. Close-up before the line is kept. |
| Ridge `TheClueLies...` | contains "Whoever he is, he's tending something." | `AssertSpokenLine`. Close-up before the line is kept. |
| Trail `NoLevelShowsAPanel...` | exact route openings, including the caption and leader line; the Trailhead's two texts; the pick's line on GenericCharacter_1 | Each route has one opening dialogue, spoken, with no John or Mark by name, and the two routes' openings are different assets. The Trailhead has 2 dialogues, both spoken with no named pick. Camera before the call is kept. |
| Trail `AssertArrival` (both routes) | the exact remark; GenericCharacter_1 | `AssertSpokenLine` and `AssertNoNamedPickSpeaker`. The 6-step shape is kept. |
| Trail blood end | the exact clue line | `AssertSpokenLine` |
| Trail pile search | `SearchLine` | `AssertSpokenLine`. Line before the reveals is kept. |
| Trail `ThePileOpens...` | the sisters' two lines; "Still counting?" before "…No."; the "Rootwell" line on GenericCharacter_1 | `AssertSpokenLine` on the opening. The end has 2 dialogues, both spoken with no named pick. |
| Trail `ThePileOutroShowsTheTally...` | dialogue kinds named by their first line; the exact texts | The 8 steps are matched by type, with dialogues at 4 and 6, `AssertSpokenLine` on both, and the two are different assets. The tally steps are kept. |

## Save reset

No.

## Decisions I made

- Tier 2: an existing step list is never rewritten. The plan's default only covered lists that add dialogue. When the structure differs, rewriting the list would undo the teammate's work, and the brief says to leave both sides as they are. The wiring therefore keeps the asset and logs a console warning. This is how the re-run stays md5-clean.
- Tier 1: "differs only in dialogue" means the two lists match once all DialogNodeSequence steps are left out of both. So dialogue that is added, removed, replaced or moved counts as no structural change.
- Tier 1: C2 uses `EditorSceneManager.NewPreviewScene()` instead of `NewScene(..., Additive)`. Each test needs two new scenes, and additive untitled scenes can't be stacked while another untitled scene is open. Preview scenes are isolated, work outside Play mode and are closed in TearDown. The behaviour under test is the same.
- Tier 1: fixed the caption speaker's character path to `TopNotification_DialogueCharacter.asset`. This is needed for seeding and is editor-only. The `Who.Narrator` enum name in the wiring is unchanged.
- Tier 1: `AssertEndFadesOutAndStaysOut` accepts an end that finishes on TransitionToNextLevel instead of `OutroCutsceneKeepGridHidden`. That covers Linda's end, as noted below.
- Tier 1: renamed two tests to match what they now check: Linda `TheEndFadesTheGridOutAndKeepsItOutThroughTheCutaway` and River `TheStartVisitsTheClueAndComesBackThenShowsLucysRole`.

## Needs THJ

These are the places where the wiring and the teammate's structure disagree. Both sides were left as they are. The wiring warns about the first three every time it runs.

1. **The Hearth endings now go to Home for the cutaway (Memory 1, 2, 3 and 4 end).**
   - Wiring: punchline, then fade out, then cutaway over the hidden grid opening on the still, then `OutroCutsceneKeepGridHidden`.
   - Teammate: fade out first, punchline, `TransitionToHome`, cutaway (now without the still), `TransitionToNextLevel`, and on John, Lucy and Mark also `OutroCutsceneKeepGridHidden`.
   - Recommendation: adopt the teammate's flow and update the wiring's step lists to it in a follow-up, so a newly created list matches. Until then, the tests check only what both versions share: the fade comes before the last line, nothing fades the grid back in, and the end either hands control back hidden or loads the next level.
   - Options: (a) update the wiring to the teammate's flow, (b) keep the wiring as is and accept the console warnings.
2. **Linda's end no longer turns input or the HUD back on itself.** It finishes on `TransitionToNextLevel` with no `OutroCutsceneKeepGridHidden`, so it relies on the next level's start (Lucy's start re-enables input). Recommendation: confirm in play that input and the HUD come back after Memory 1. If they don't, the teammate should add `OutroCutsceneKeepGridHidden` before the transition.
3. **John's and Mark's ends put `TransitionToNextLevel` before `OutroCutsceneKeepGridHidden`.** `TransitionScene`'s tooltip says "Place TransitionToNextLevel last". The code waits for the enclosing sequence anyway, so this is probably harmless. Recommendation: the teammate moves it last for consistency.
4. **Lucy's end lost its cutaway.** `Memory2Lucy_End_Cutaway_DialogNodeSequence` is no longer in any list, and Margaret's handoff to John is gone. The asset still exists, and the wiring keeps "seeding" it (as a no-op, since it already exists). Recommendation: the teammate confirms it's intended, then the asset can be deleted along with the wiring's line.
5. **Mark's end fades the grid right after the mother falls**, before the mother line and before Lucy and Mark walk to the cub. So the walks play over a faded grid. Units stay visible and cell lookups still work, so I didn't treat this as broken. Recommendation: THJ looks at it in play.
6. **River and Ridge**: the teammate replaced the wiring's dialogues in the step lists with their own (`MS1_Level1_*`, `MS2_Level1_*`). The River start now has one dialogue before the camera visit instead of a call before the camera and John's line after the panel. This is a dialogue-only difference, so the wiring keeps it quietly. Left behind: `River_Start_Call`, `River_Start_StayByMe`, `River_End_Clue`, `Ridge_Start_Opening` and `Ridge_End_Clue` (`_DialogNodeSequence`) are no longer used by the levels. The wiring still references them as seeds. Recommendation: clean these up once the teammate's lines are final.

## Docs to update

- `tech/` note (coordinator): the wiring seeds dialogue once and edits made in Unity win. Existing step lists are kept, and the console warns when one differs beyond its dialogue. `WiringSeed` is the helper.
- `conventions.md` line (coordinator), per the plan.

## Risks and loose ends

- Because existing step lists are never rewritten, a future change to the wiring's own step list only reaches new assets. To apply it to an existing level, update or delete that asset, or change the wiring to match.
- `HearthMemoryWiring.Mark.*` is retired (no menu), but it calls the same helpers, so its rules match the rest.
- Panel text, objective text and `LevelResultLine` text are still written by the wiring. They are not dialogue assets and were out of scope. The teammate hasn't edited them.
- The wiring still says `Who.Narrator` for the top-notification speaker. Renaming it would be cosmetic.

## Proposed commits

1. `refactor(onboarding): wiring seeds dialogue once and keeps step lists edited in Unity; tests check structure, not wording`
   Files: `WiringSeed.cs`, `WiringSeed.cs.meta`, `WiringSeedTests.cs`, `WiringSeedTests.cs.meta`, `WiringStructureAsserts.cs`, `WiringStructureAsserts.cs.meta`, `HearthMemoryWiring.Linda.cs`, `SearchWiring.Trail.cs`, `SearchWiring.Trail.Arrivals.cs`, `SearchWiring.River.cs`, `HomeVisitsWiring.cs`, `HearthMemoryJohnTests.cs`, `HearthMemoryLindaTests.cs`, `HearthMemoryLucyTests.cs`, `HearthMemoryMarkTests.Flow.cs`, `HomeVisitsTests.cs`, `HomeVisitsTests.Hearth.cs`, `SearchRiverTests.cs`, `SearchRidgeTests.cs`, `SearchTrailTests.cs` (all under `miso/Assets/_Project/Features/Onboarding/Editor/`). Plain, editor-only.
2. `test(onboarding): Home memory opening tests use preview scenes so they run in edit mode`
   Files: `miso/Assets/_Project/Features/Onboarding/Editor/HomeMemoryOpeningTests.cs`. Plain.

Both messages have no attribution trailers. Do not stage THJ's uncommitted files: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` and the TMP fallback font.

## Other branches

None. Only `main` has the teammate's dialogue.

## How to see it

1. Open Unity and clear the Console.
2. Run Tools > Onboarding > Wire Memory 1 (Linda). The Console shows "Kept the hand-edited step list of ...Memory1Linda_End_SequentialSequence.asset" with both step lists. Memory 2 and Memory 3 show the same for their ends.
3. Run Wire Search: River, Ridge, Trail and Wire Home Visits. There are no warnings, and `git status` shows no asset changes.
4. Open `Resources/Sequences/Hearth/Memory1Linda/Memory1Linda_Start_DialogNodeSequence.asset`. It still has the teammate's line ("I remember… I saw Ryker…").
5. Test Runner > EditMode > Run All. Everything passes except `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Follow-up (2026-11-11)

- `AnExistingStepListThatDiffersOnlyInDialogueIsKeptQuietly` now subscribes to `Application.logMessageReceived` around the `WiringSeed.StepList` call and asserts that no Warning arrived. The old `LogAssert.NoUnexpectedReceived()` only catches errors, asserts and exceptions, so it could not fail on a warning. Checked by reasoning, not by flipping the test: the sibling test shows the changed-structure path logs a Warning through the same log pipe, so the handler would have caught it. WiringSeedTests 6/6 pass, full EditMode 1892/1893 (only the known red AIRegressionTest.Baseline_MatchesCurrentAI).
- Line endings: the claim above stays as written for these files. I checked on disk (no CR bytes) and with `git ls-files --eol` (`attr/text eol=lf`, working copy `w/lf`) for the new and the changed Onboarding Editor files. They are LF, not CRLF. Likely the CRLF figure came from other files in the repo, not these.
