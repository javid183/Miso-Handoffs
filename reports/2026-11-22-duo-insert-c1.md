# Duo insert shot, chunk C1 (insert player and QTE card)

Plan: `plans/2026-11-22-duo-insert-shot-tech.md`. No core code touched. Nothing committed.

## Chunk 1: files

New, all under `miso/Assets/_Project/` (each with its `.meta`):
- `Features/UI/DuoInsert/InsertMode.cs` (InsertMode, InsertSide enums)
- `Features/UI/DuoInsert/DuoInsertLibrary.cs`, `DuoInsertRules.cs`, `DuoInsertHalfGraphic.cs`, `DuoInsertSequence.cs`
- `Features/UI/DuoInsert/Editor/DuoInsertBuilder.cs` (menu `MISO/Duo Insert/Build Canvas Prefab and Library`), `Editor/DuoInsertRulesTests.cs`
- `Features/UI/DuoInsert/Prefabs/DuoInsertCanvas.prefab`, `Features/UI/DuoInsert/DuoInsertLibrary.asset`
- UNTRACKED, never stage: `Content/FamilySuperTime/DUO/Inserts.meta`, `Inserts/_Test/Mark_TestA.mp4(.meta)`, `Mark_TestB.mp4(.meta)`. (Inserts.meta and the `_Test` folder meta: `_Test` folder's contents are untracked; the folder `.meta` files can stay out of the commit too.)

No existing file edited. Line endings LF, no BOM. THJ's uncommitted files untouched. No scene touched.

## Verified
- Unity MCP connected. Compiled via forced refresh: no errors from the new code.
- `DuoInsertRulesTests`: 12 of 12 pass (lookup hit/miss/null, length per mode and use count, off, negative clamp, skip gate at 0.3 s, side lookup).
- Builder menu ran twice without errors: prefab and library asset created. Library entries checked in the YAML: `Mark_Lucy_Duo` (left: Lucy FR sprite; right: clip B, start 0.5 s, uvRect x 0.26..0.72, y 0.10..1.0) and `Mark_Lucy_Duo_ClipA` (clip A, full frame). Caption is "Chained Assault", read from the duo's trigger preset title (`Mark_Lucy_Duo_Ability`).
- Unity logs "Unexpected timestamp values" warnings for both MP4s (H.264 profile); harmless, playback is skew-corrected.

## Not verified (needs THJ, Play mode)
I did not enter Play mode (THJ's editor). Not seen on screen: the look, the crop of clip B's logos (estimated from a GIF frame: logos sit in x < ~20% and x > ~74%), speed lines, flash, skip, no-leak on leaving Play mid-preview, timeScale returning to 1. Rules logic has test coverage; everything else is a play check.

## How THJ previews it
1. Drag `Features/UI/DuoInsert/Prefabs/DuoInsertCanvas.prefab` into any open scene (e.g. temporarily into CombatLevelContainerScene, do not save the scene) at the scene root, or under the root that holds the HUD canvas. It is its own canvas (Screen Space Overlay, sorting order 300, above the HUD at 100/101), so the parent does not matter; scene root is fine. For the final placement (C2): scene root of `CombatLevelContainerScene`, sorting order 300 is already set.
2. Enter Play mode. Select the instance, open the `DuoInsertSequence` component's context menu (three dots): `Preview Mark-Lucy` (card with a yellow dummy slot for 1.2 s, then the insert; runs with timeScale 0 to prove unscaled time) or `Preview Mark-Lucy (clip A)`. `Reset insert use count` makes the next play full length again (default mode ShortAfterFirst: first 1.4 s, then 0.6 s).
3. Skip: press any key/click after 0.3 s. Exit Play mid-preview to check the console for leak warnings.
4. If the prefab or library need rebuilding (tweak layout in the script), run the menu item again; ids are kept.

## API for C2 (`MISO.Features.UI.DuoInsert.DuoInsertSequence`)
- `bool TryGetEntry(string duoId, out DuoInsertLibrary.Entry entry)`: false if no entry or Mode is Off (use this as the "insert path?" check).
- `float EffectiveLength(Entry)`: seconds for the next play (full or short).
- `IEnumerator PlayCardIE(GUnit qteUnit, string title, Action<Transform> withSlot)`: shows dimmer and card (portrait = `qteUnit.UnitFamilyRoleImage`), pops in 0.12 s, then calls `withSlot(slot)` and ends. The QTE is NOT started or waited on by the card: the callback should start it, and the caller waits for the QTE itself.
- `void HideCard()`. `PlayInsertIE` also hides the card first, so no gap frame.
- `IEnumerator PlayInsertIE(Entry)`: counts one use, returns at once if length is 0. Ends with everything hidden.
- `Mode` (get/set), `ResetUses()`, `IsPlayingInsert`.
- Abort: `OnDisable`/`OnDestroy` set an aborted flag, stop and destroy the VideoPlayers, release the RenderTextures, hide everything, restore timeScale only if the preview set it. A nested enumerator that the handler is running ends at its next step. C2 must still restore `Time.timeScale = 1` itself on its own exit paths.
- Slot note for C2: the QTE button is parented with `SetParent(hook)` (world position kept) and nothing resets its anchored position in `BindPlacement` for `inUI`; check the button lands centered on the slot (the slot is a 240x240 rect, right side of the card). It may need `anchoredPosition = zero` after parenting, which belongs in the C2 call site, not in QTE code.
- No statics added; uses-per-combat is an instance field.

## Decisions and deviations
- Speed lines: `PS_SpeedLines` is a world-space particle system and cannot render on an overlay canvas without a second camera. Instead the canvas spawns 22 UI streaks from the same sprite (`speedlines.png`) with `speedline.mat`, rushing inward. Same assets, different carrier. Needs a look; the material is the sprite shader, tell me if it renders oddly.
- Diagonal halves: a small custom `MaskableGraphic` (`DuoInsertHalfGraphic`) draws each half as a clipped polygon with aspect-fill UVs, instead of a rotated mask. One batch per half, no stencil.
- Lucy's half is a transparent sprite on the black backdrop (no BG sprite); `LucyFamilyRole_BG.png` can be added later.
- Preview context-menu names use an ASCII hyphen ("Mark-Lucy") instead of an en dash.
- `SideOf`: returns Left for the entry's left nickname, Right for any other non-empty nickname, None for null/empty (the plan gave only a left nickname field).
- Test clips are in `Inserts/_Test/` as asked; byte-identical to the scratchpad copies.
- Input skip uses the new Input System (project is Input System only): keyboard any key, mouse left/right, gamepad face/start buttons.

## Risks and loose ends
- The TMP fallback font file showed as modified at session start and is no longer in `git status`; not mine.
- Caption/title use `alagard SDF` (the HUD's main TMP font).

## Proposed commits (C1)
1. `feat(ui): duo insert player, QTE card and Mark-Lucy test entry`: everything under `Features/UI/DuoInsert/` with its `.meta` files (code, Editor, prefab, library asset). The library asset references the untracked test clips by GUID, so on a clean checkout the right half falls back to a blank sprite; acceptable per plan (clips stay local). Do NOT stage `Content/FamilySuperTime/DUO/Inserts*`.

## How to see it
See "How THJ previews it".
