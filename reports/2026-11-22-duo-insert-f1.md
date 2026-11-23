# Duo insert shot, follow-up F1 (transitions, longer timing, tunables, skip filter)

Plan: `plans/2026-11-22-duo-insert-shot-tech.md` (section "Follow-up F1"). Nothing committed or staged. No scene or ProjectSettings touched.

## F1a files (feature code, no core), all under `miso/Assets/_Project/Features/UI/DuoInsert/`, LF, no BOM
- `InsertMode.cs` (+10): new enum `InsertTransition { SoloThenSplit, SlideFromSides }`.
- `DuoInsertLibrary.cs` (+32): Entry gets `transition`, `leadSide` (default Right), `transitionIn` 0.35, `transitionOut` 0.3; `fullLength` 1.4 -> 2.0, `shortLength` 0.6 -> 0.9; `WithTransition(style)` copy helper (used by the forced-style previews).
- `DuoInsertRules.cs` (rewritten around the old one): `InsertPhase`, `InsertTiming`, `HalfShape`, `SplitShape`, `SplitLayout`; `TimingFor`, `PhaseAt`, `TransitionScale` (short = 0.6), `ShapeAt` / `SettledShape` (polygon plus picture frame per half, per style and phase), `OutFade`, `CanSkip(elapsed, delay)`, `IsBoundToAny(control, actions)`. Old API kept.
- `DuoInsertHalfGraphic.cs` (+35): `SetPolygon(polygon, frame)`; the picture is fitted to the given frame instead of the animated polygon's bounds.
- `DuoInsertSequence.cs`: `PlayInsertIE(entry, IReadOnlyList<InputAction> ignoreActions = null)`; phases In / Settled / Hold / Out; flash at start (solo) or at contact (slide); caption pops when the split settles and leaves at Out; skip = about 0.12 s fast fade; designer timings are now serialized fields with tooltips; two new preview menus ("Preview Mark-Lucy (solo then split)", "(slide from sides)") force a style on the main entry; the old two menus play the entries' own styles (main = solo, clip A = slide).
- `DuoInsertLibrary.asset`: values written by YAML (Mark_Lucy_Duo: solo; Mark_Lucy_Duo_ClipA: slide; both 2.0 / 0.9 / 0.35 / 0.3, lead Right).
- `Prefabs/DuoInsertCanvas.prefab` (+8 lines): the new component fields written by YAML.
- `Editor/DuoInsertRulesTests.cs`: defaults updated; new tests for timing, phases, fade, shapes of both styles, defaults, copy helper, skip delay.
- `Editor/DuoInsertBuilder.cs` (+14, NOT in the plan's file list): its hard-coded 1.4 / 0.6 would have reset the library on a re-run, so it now writes the new defaults and styles. Tiny; drop from the commit if you prefer, but then re-running the builder resets the lengths.

`git diff --stat` F1a: 9 files, 844 insertions, 123 deletions (DuoInsertHalfGraphic, library asset, library cs, rules, sequence, builder, rules tests, InsertMode, prefab).

## F1b files (core, one call site)
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.Insert.cs`: 13 insertions, 1 deletion. `RunInsertIE` collects each partner's QTE action via `PlayerInputController.Instance.GetInputAction(profile.bindingActionID, ...)` (new `AddPromptAction`) and passes the list to `PlayInsertIE`. Nothing else in core changed. F1a works alone (null list = no filter).

## Decisions
- Skip delay is a serialized field on the component (`skipDelay`, default `DuoInsertRules.SkipDelay` = 0.3); the rule has an overload taking the delay.
- Timing meaning: `fullLength` / `shortLength` is the settled split; transitions, the 0.3 s hold and the out come on top. Full play total = 0.35 + 2.0 + 0.3 + 0.3 = 2.95 s; short = 0.21 + 0.9 + 0.3 + 0.18 = 1.59 s. The clips start playing at the start of the In phase.
- Picture window, deviation in method (same behaviour goal): the picture is fitted to a frame that always contains the polygon. For the half that wipes in or leaves, the frame is its settled box; for the half that sweeps to/from full screen (solo lead in, follower out) the frame is lerped between the settled box and the full-screen box in step with the sweep (uniform zoom/pan, never a squeeze). Slide: polygon and frame move together. This avoids showing outside the clip's crop (logos) or clamped edges while a polygon is larger than its settled box. Side effect: at the start of solo the lead picture is zoomed to fill the screen (about 2x for clip B) and pulls back as it settles.
- Out: solo = first 75 % sweep, last 25 % fade; slide = move over the whole out, fade in the second half.
- Skip filter: any key/mouse/pad press whose control is bound to an ignored action never skips (`action.controls` of the resolved action, so composite parts count).
- Preview of both menus was added; the plan's existing two keep working.
- No statics added.

## Verified
- Compile clean (console read, no errors; the type and library values load).
- `DuoInsertRulesTests`: 40 of 40 pass. `CooperationInsertTests` (14) pass as part of the whole run.
- Whole EditMode suite: 2485 total, 2484 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit).
- Not unit-tested: `IsBoundToAny` with real devices (only the null/empty cases; needs input devices), the skip filter in the sequence, the F1b call (needs a Play combat).
- Play mode (editor was open; entered from the boot scene, prefab instantiated at runtime, then stopped): ran "solo then split" and "slide from sides" previews with the card first. No errors or warnings in the console. Screenshots (Game view captures) showed: the settled split correct for both styles (Lucy left, Mark clip B right, no logos, caption "Chained Assault", speed lines), the flash fading at the start (solo) and at contact (slide), clean exit to the menu behind, Play stopped cleanly. I did not catch the in-between frames of the sweeps and slides by eye, so the motion itself, the out phase look, skip (including mashing the QTE key without skipping) and the real duo flow are THJ's play check. Timescale 0 during preview worked (unscaled time).
- The Play session ran in the boot flow (MainMenuScene); the test object lived only in Play mode, nothing saved to a scene.

## Where to tune
| Field | Where | Default | What it does |
|---|---|---|---|
| transition | library entry | SoloThenSplit (Mark_Lucy_Duo), SlideFromSides (ClipA) | Style of in/out |
| leadSide | library entry | Right (Mark) | Solo: which half fills the screen first |
| fullLength | library entry | 2.0 s | Settled split time, full play |
| shortLength | library entry | 0.9 s | Settled split time, repeat plays |
| transitionIn / transitionOut | library entry | 0.35 / 0.3 s | In and out durations (short play x0.6) |
| ShortTransitionScale | rules const | 0.6 | Transition scale for short plays |
| holdLastFrame | component on DuoInsertCanvas prefab | 0.3 s | Hold on the last frame |
| skipDelay | component | 0.3 s | Time before a key can skip |
| fastOutTime | component | 0.12 s | Fade when skipped |
| cardPopTime | component | 0.12 s | QTE card pop-in |
| flashHold / flashFadeTime | component | 0.05 / 0.12 s | Impact flash |
| spritePushIn | component | 1.08 | Zoom of a still picture (Lucy) by the end |
| speedLineSpeed | component | 2.6 | Speed line rush rate |
| diagonalSkew / inkGap / screenMargin | component | 0.07 / 0.006 / 0.03 | Diagonal, ink gap, margin (existing) |
| Mode | component | ShortAfterFirst | Full / ShortAfterFirst / Off (existing) |
| SoloOutSweepShare / SlideOutFadeStart | rules consts | 0.75 / 0.5 | Where the out fade starts |

## Proposed commits
1. F1a: `feat(ui): duo insert transitions (solo then split, slide from sides), longer timing, tunable fields`: the nine files above (with the `.meta` files unchanged, none new). Do not stage `Content/FamilySuperTime/DUO/Inserts*`.
2. F1b (core, separate): `feat(duos): mashing the duo prompt's own key no longer skips the insert`: `UnitsCooperationHandler.Insert.cs` only.

## How to see it
Play mode, any scene with the prefab `Features/UI/DuoInsert/Prefabs/DuoInsertCanvas.prefab` dropped in (or in a combat, select `PlayerController > DuoInsertCanvas(Clone)` after the first duo). Component context menu: `Preview Mark-Lucy (solo then split)`, `(slide from sides)`; `Reset insert use count` for a full-length replay. In a combat: Mark-Lucy, mash Lucy's prompt into the insert (must not skip), press another key to skip (fast fade).

## Loose ends
- The solo lead's opening zoom (about 2x on clip B) is a look decision for THJ.
- `IsBoundToAny` depends on the action's bindings being resolved; if the player rebinds the QTE key mid-combat the list is built per duo so it follows.

## Review fixes (applied after APPROVE)
1. `IsBoundToAny` now has a real edit-mode test: a Keyboard device is added in SetUp and removed in TearDown; a simple `<Keyboard>/space` action and a 1D-axis composite (q, e) are enabled, then disabled and disposed. Space, q and e count as bound; `a` and "space with only the composite action" do not.
2. `Entry.WithTransition` now uses `MemberwiseClone` and sets the style. The halves are shared with the original (fine: the insert only reads them).

Results: `DuoInsertRulesTests` 41 of 41 pass. Whole EditMode suite: 2486 total, 2485 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Compiled clean.
F1a set diff stat after the fixes: see the final reply (9 files). F1b unchanged.

## Follow-up: speed lines behind, full screen, Mark-Lucy uses slide
- Draw order: `SpeedLines` is now the sibling right after `Backdrop` (prefab `m_Children` reorder, one line; builder creates it before the halves), so lines sit behind both halves, caption and flash.
- `DuoInsertSequence.AnimateSpeedLines`: sized each frame from `speedLineRoot.rect`. Per line: distance to the screen edge along its angle (handles corners), outer end at edge x 1.12 + 40 (always off-screen), tip moves inward to a per-line radius of 8-38 percent of that edge distance, thickness 2-5 percent of the half-height. Alpha, `speedLineSpeed` and the 0.6 max alpha kept. Fixed pixel radii and lengths removed. Count 22 -> 32 to fill a wide screen.
- `Mark_Lucy_Duo` now `SlideFromSides` (library asset and builder default); `Mark_Lucy_Duo_ClipA` now `SoloThenSplit`.
- Prefab and asset files are LF in the repo (not CRLF), kept as they were.
- Results: compiled clean, whole EditMode suite 2486 total, 2485 passed, 0 failed, 1 skipped (Explicit AI baseline). Play preview (slide) screenshot `reports/2026-11-22-duo-insert-speedlines.png`: lines behind both halves, reaching all edges and corners. One frame only; motion is THJ's check.

## Follow-up: speed lines removed

THJ asked for the speed lines to go. Removed from `DuoInsertSequence.cs` (fields, arrays, count constant, ensure/animate methods, the unused fraction helper, and the show/hide calls in the update, skip fast-out and reset paths; header comment updated), from `DuoInsertCanvas.prefab` (the `SpeedLines` object, its child entry and the five serialized fields) and from `DuoInsertBuilder.cs` (object creation, field assignments, texture/material constants). Picture framing, transitions and timing are unchanged. `speedlines.png` and `speedline.mat` are left on disk, now unreferenced by the insert.

Verified (editor open, Play stopped before editing): compiled clean; whole EditMode suite 2485 passed, 0 failed, 1 skipped (the explicit AI baseline); the "Preview Mark-Lucy" context menu run in Play on an instance of the prefab gave no errors or missing-reference warnings, only the existing H.264 timestamp notice for the test clip. Play was stopped afterwards. Grep for "speed" in the DuoInsert folder returns nothing.

## Follow-up: clip C in Mark-Lucy, playback speed per half

- `HalfSource.playbackSpeed` (default 1, tooltip). `DuoInsertRules`: `ClampSpeed` (unset or <= 0 gives 1, else 0.25 to 4), `ClipSecondsNeeded(timing, speed)` = (in + settled) x speed, `ClampClipStart(start, clipLength, needed)` (keeps the start; pulls it back only if the clip would run dry, never later than 0.1 s before the end). `DuoInsertSequence` sets `VideoPlayer.playbackSpeed` and uses the clamp when seeking. New "Preview Mark-Lucy (clip B)" context menu. Three new tests in `DuoInsertRulesTests`.
- Values. The clips run for in 0.35 + settled 2.0 = 2.35 s, then pause on the last frame (hold). Mark_Lucy_Duo = clip C, uv (0.24, 0, 0.52, 1) (centre 52% width, full height, close to the half's proportions), clipStart 0.8, speed 2.0, SlideFromSides: covers clip 0.8 to 5.5 s. Eyes open about 0.1 s in, glow as the halves land, rings/stance around 0.9 to 2.0 s, firestorm (5.3 s) for the last 0.2 s and on the held frame. Speed 1.8 would stop at 5.03 s, short of the firestorm, hence 2.0.
- ClipA (SoloThenSplit, full frame) and new ClipB (SlideFromSides, existing logo crop): start 0.8, speed 1.5, covering 0.8 to 4.3 s, past the punch at about 1.1 s. Not eyeballed in Play (only Mark-Lucy was).
- Builder writes the same entries (clip C loaded by path); rebuilt via the menu, prefab unchanged. Clip C `.meta` is the default importer block, identical to the `_Test` clips, and was not changed by Unity.
- Verified (editor open; Play was not running before): compiled clean; DuoInsertRulesTests 44/44; whole EditMode 2489 total, 2484 passed, 1 skipped, 4 failed in `GridToLevelTests` ("GB_24-nook.prefab already exists", a stale `__Test` output); the fixture re-run alone passes 20/20 and the `__Test` folder is gone, so treat as a one-off leftover. Play preview of "Preview Mark-Lucy": no errors. Frames: `reports/2026-11-22-duo-insert-clipC-start.png` (caught on the white contact flash, so blank), `-middle.png` (eyes glowing, fire rings, mid-pull-back), `-end.png` (stance in the firestorm). Play stopped afterwards. Motion and the A/B looks are THJ's check.

## Lucy clip in the left half (follow-up)

- Changed: `DuoInsertLibrary.asset` and `Editor/DuoInsertBuilder.cs` (new `LucyClip` path const, loaded with the existing `LoadClip`, so a missing clip falls back to the sprite with a warning). The builder was run from the menu and gave the same asset values; the prefab did not change.
- Values (left half of Mark_Lucy_Duo and the clip A and clip B entries): clip = `Sprites/kling_20261123_VIDEO_Lucy__a_yo_3169_0.mp4`, clipStart 1.2, playbackSpeed 1.3, fallbackSprite kept, uvRect x 0.30, y 0, w 0.52, h 1 (right edge 0.82, watermark is past 0.85), mirror off.
- Clip budget: full play needs (0.35 + 2.0) x 1.3 = 3.055 s; 1.2 + 3.055 = 4.255 s of 5.04 s, margin 0.78 s. The short play needs less.
- Clip .meta: it did not exist before (the editor had not imported the clip); the import created it (guid 7747fa5298c872646b2251ff04d46cbf). Do not stage the clip; its .meta is untracked too.
- Verified: compiled clean; whole EditMode suite 2489 total, 2488 passed, 0 failed, 1 skipped (explicit AI baseline). Play preview "Preview Mark-Lucy" on a temp prefab instance: no duo insert errors. Frames: `reports/2026-11-22-duo-insert-lucy-middle.png` (halves just arriving over the card, Lucy sliver with green orb) and `-end.png` (settled split: Lucy in profile facing right, face and raised hand in the left half, green glow, Mark clip right, no watermark visible). Play stopped. The console shows two "Failed to store screen shot" lines from the capture calls (files were still written); not a game issue.
- Motion and how the Lucy clip reads against the Mark clips are THJ's check.

## Lucy starts earlier (follow-up)

- Lucy's left half in all three Mark-Lucy entries (`DuoInsertLibrary.asset`) and in `Editor/DuoInsertBuilder.cs`: clipStart 1.2 -> 0.5, playbackSpeed 1.3 -> 1.2. The builder's explanatory comment was updated to match.
- Coverage: 0.5 + 2.35 x 1.2 = 3.32 s of the 5.04 s clip. Orb burst (about 2.0 s) lands at (2.0 - 0.5) / 1.2 = 1.25 s into the 2.35 s play, i.e. around the middle; head tilt (1.0-1.6 s) at 0.4-0.9 s, during the slide-in; cloak swirl about 1.0 s. Numbers kept as given. The short play scales the needed clip time down, so the burst only gets earlier relative to its end.
- Verified: refresh + compile clean (no console errors); `DuoInsertRulesTests` 44/44. Play preview not run; motion is THJ's check.
