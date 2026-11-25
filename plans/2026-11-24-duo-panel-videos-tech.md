# Duo panels play the art team's clips; QTE card first for every duo with a QTE

Size: M    Tier: 3 (C2 changes the duo flow in a core system; THJ approved 2026-11-24: "Yes, build it")    Assigned to: miso-implementer
Branch: thj/onboarding-demo (THJ's current branch; it contains the duo insert work from `main`)
Status: done 2026-11-24. C1 `06604c15b` (with the clips), THJ's timing tune `1ed8b2b9a`, C2 `f39ffe37c`. Review APPROVE, should-fixes applied; THJ play-checked and asked to commit (bigger-monitor look pending).

## Why

THJ, 2026-11-24, after presenting the comic insert at the office: the team found the insert art too separate from the game. The art team animated the old Family Role panel art instead: `Content/FamilySuperTime/Sprites/Mark.mp4`, `Lucy.mp4`, `John.mp4`, `Linda.mp4`. Wanted: the duo shot as before (the `FTPPanel` sliding panels) but with these clips instead of the fixed sprites, and keep the new order (framed QTE card first, then the panels, then the action). THJ chose to mask the clips (no alpha re-export) and approved the plan, including the order for every duo with a QTE and retiring the comic insert (off, not deleted).

## The clips (checked 2026-11-24)

- All four: 1112×834, 4.06 s, H.264, no alpha: the panel art (character + its background, one layer) on solid black, gentle motion, near-seamless loop. Loose dark specks drift outside the panel.
- **Mark.mp4 opens with 3 white frames (~0.1 s)** where the outside of the panel is white: trim with the importer (`startFrame` 3) so loops don't flash.
- They do **not** line up with the `<Name>FamilyRole.png` sprites (different scale/crop; Mark's panel runs off the top-left and bottom-right of the frame). So masks are cut from each clip's own panel outline: union of non-black pixels (sum of RGB > 30) over 7 frames, background = near-black pixels flood-filled from the frame border, keep the largest component, two 3×3 box blurs for a soft edge, pixels on the frame border kept opaque where the panel touches it. Result: `<Name>Mask.png` (1112×834, white RGB, alpha = mask), made by the coordinator and staged at `C:/Users/javid/AppData/Local/Temp/claude/9ec5439f3060d705/f52d4c4f-a306-4328-aebe-71d530e8eab5/scratchpad/masks/`. If a clip changes, the mask is remade the same way (procedure above).

## Goal

Every Family Role panel (duo, solo, trio) plays its character's clip through its mask instead of the still sprite; every duo with a QTE shows its QTE on the framed card first, then the panels, then acts. Duos without a QTE and Toba (no clip) look as before.

## C1. Panel videos (feature code) — opus, review with C2

- Import the masks to `Content/FamilySuperTime/Sprites/Masks/<Name>Mask.png` (texture, alpha from input, no mipmaps, clamp, uncompressed or high quality; `alphaIsTransparency`).
- `Mark.mp4.meta`: trim the first 3 frames (`startFrame: 3`, `endFrame` = last frame); check the others need no trim.
- A small UI shader/material: video RenderTexture × mask alpha (UI default-compatible: stencil/RectMask2D/clip rect, vertex colour alpha so the panel's existing fades still work). Name it plainly (e.g. `MISO/UI/MaskedVideo`).
- A component (new file, e.g. `Features/UI/Panels/Scripts/FamilyRoleVideoPanel.cs`) on each character's `FR Image` object in `FTPPanel` (`CombatLevelContainerScene`, under Canvas HUD): VideoClip + mask texture; creates a RawImage (or uses one) sized to the clip's aspect, plays the clip looped on unscaled time while the panel object is active (OnEnable/OnDisable: prepare/play, stop, release the RenderTexture), hides the sprite `Image` and the sibling `FR BG` while the clip plays, and shows the sprite again if the clip fails to prepare (fallback). No statics.
- Keep `FactionRoleVisual` and the animators as they are (they toggle `FR Image` active and slide it; the clip rides along). If a field is needed there, add it in a new partial file.
- Wire the four characters in the scene (minimal YAML or editor; no unrelated scene noise). Size/position the video so the clip's panel sits where the old sprite panel did as closely as reasonable; THJ nudges the rest in the inspector.
- Acceptance: in Play, a duo, a solo Family Role and Family Super Time show the moving panels with no black box; Mark doesn't flash white on loop; Toba's panel unchanged; leaving combat leaves no running VideoPlayer or RenderTexture. Tests: whatever pure logic exists (e.g. fallback decision); the component itself is a play check.

## C2. Duo order for every duo with a QTE (core: `UnitsCooperationHandler`) — opus, its own review

- Today the card-first path runs only when the duo id has an entry in `DuoInsertLibrary` (and mode ≠ Off), and it then plays the comic insert. New: the card-first path runs for **every duo that has at least one partner with a QTE** (mode ≠ Off): card QTE(s) in partner order (same shallow profile copy, same stored-factor mapping, same skip-filter logic no longer needed for the insert), then `CombatLevelUIManager.ShowDuoVisual` (the old panels, now with clips) and its usual hold, then camera and actions as today with the stored factors. The comic insert is not played (keep its code and library; e.g. a serialized `playComicInsert` on the sequence, default false, or equivalent; say which).
- Duos without any QTE partner: unchanged (panels first, no card). Mode Off: the fully old flow (panels first, QTE on the board).
- Partners with time-window QTEs (John–Lucy, Mark–John) must work on the card too (the card already hosts any profile with `inUI`); check the stored-result mapping for time-window/press modes matches the old board path.
- Keep timeScale/abort safety (OnDisable restore, pooled button return). Linda–Toba: Toba has no clip; the card still runs for Linda's QTE.
- Tests: the "card-first?" decision (no QTE → old; QTE + mode on → card-first; mode Off → old; no sequence → old), update `CooperationInsertTests` that assumed the library entry; run cooperation/duo fixtures, then the whole EditMode suite.

## Risks

- Core behavior (Tier 3, approved): more duos now pause for a card before the panels.
- Scene edit in `CombatLevelContainerScene` (FTPPanel): keep the diff to the added components/references.
- Video cost: four VideoPlayers only while panels are active; prepare on enable can delay the first frame (show the sprite until prepared).
- Statics: none planned. AI: untouched (no AI graph/ability/unit prefab change) unless the unit prefabs are edited; then run `AIRegressionTest` by name.
- THJ has uncommitted files: `PreloadScreen.unity`, ProjectSettings, `LevelM2-C1.prefab` noise, the `DUO/Inserts/` test clips; never stage them.

## Gates

Compile / EditMode (C1 tests, C2 decision tests, cooperation fixtures, full suite) / review: C1+C2 together, C2 core focus / THJ's play check (duo with QTE, duo without, solo FR, Super Time, Toba duo, leave combat mid-panel) / commits: C1 and C2 separate (C2 revertable alone), masks + clips + metas with C1 (THJ decides on committing the clips; they are clean art).
