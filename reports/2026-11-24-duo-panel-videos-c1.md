# Duo panel videos, chunk C1 (panel videos)

Plan: `plans/2026-11-24-duo-panel-videos-tech.md`. Branch `thj/onboarding-demo`. Nothing staged or committed. Editor was open (not in Play at start); I entered Play for the visual check and stopped it.

## What changed, per file (all under `miso/Assets/_Project/`)

- `Features/UI/Panels/Shaders/MaskedVideo.shader` (new): UI shader `MISO/UI/MaskedVideo`. Samples the RawImage texture (video RT) and multiplies alpha by `_MaskTex.a`. Vertex colour alpha, stencil, RectMask2D clip and alpha-clip as in UI/Default.
- `Features/UI/Panels/Shaders/MaskedVideo.mat` (new): template material for the shader.
- `Features/UI/Panels/Scripts/FamilyRoleVideoPanel.cs` (new): component on each character's `FR Image`. On enable: creates a `Video` child RawImage (first sibling, same rect as `FR Image` times `sizeScale`, plus `offset`), a runtime copy of the material with that character's mask, a RenderTexture (clip size) and a VideoPlayer (looped, no audio, `UnscaledGameTime`, frame-ready events). Hides the still `Image` and the sibling `FR BG` image (component `enabled`, not the GameObject: the animator toggles the GameObjects) from the start, shows the video on the first decoded frame. Falls back to the still art if there is no clip/mask/material, on a player error, or if no frame within 2 s. On disable: stops, releases and destroys the RenderTexture, re-enables the still art. OnDestroy destroys the material copy. No statics.
- `Features/UI/Panels/Scripts/FamilyRoleVideoRules.cs` (new): pure decisions (`ShouldShowStillArt`, `ShouldShowVideo`, 2 s timeout constant).
- `Features/UI/Panels/Editor/FamilyRoleVideoRulesTests.cs` (new): 6 EditMode tests of those decisions.
- `Features/UI/Panels/Prefabs/FTPPanel.prefab`: +80 lines, 0 removed: one `FamilyRoleVideoPanel` on each of `MarkRole/JohnRole/LindaRole/LucyRole` > `FR Image`, wired (clip, mask, material, still image, `FR BG` image, `sizeScale`). Done through an editor script run via the MCP (not YAML), then diff checked.
- `Content/FamilySuperTime/Sprites/Masks/{Mark,Lucy,John,Linda}Mask.png` + `.meta` (new, copied from the staged masks; imported as Default texture, alpha from input, alphaIsTransparency, no mipmaps, clamp, bilinear, uncompressed RGBA32, not readable).
- `Content/FamilySuperTime/Sprites/Mark.mp4.meta` (untracked file, edited): frame range Custom, start 3, end 98, and transcoding enabled (see decisions).

## Decisions and deviations (same behaviour)

- **Wired in the prefab, not the scene.** `FTPPanel` in `CombatLevelContainerScene` is a prefab instance of `FTPPanel.prefab` (no overrides on those objects), so adding the components to the prefab reaches the scene. `CombatLevelContainerScene.unity` is unchanged (0 diff). Any other scene using the prefab gets it too.
- **Mark trim needs transcoding.** With the default passthrough import the start/end frame setting is ignored (frame count stayed 97). With transcoding on (`enableTranscoding: 1`, Auto codec, same size, high bitrate and quality) it applies. The end value is not the last frame index: `endFrame: 98` gives 94 frames (frames 3 to 96); 97 gave 93, 99 gave 95 (padding), `-1` ignored the range. So the meta says 98. Mark.mp4 is re-encoded by Unity on import (small quality cost); the other three clips are unchanged (they start dark, no trim, passthrough).
- **Still art hidden from the start.** The plan said show the sprite until prepared. Instead nothing shows during the first frames (measured ~0.2 s to the first video frame when driven by the animator, before the hold at ~0.58 s), so the old sprite does not flash and swap. The still art is the fallback only (error, timeout, missing assets), as in the plan.
- **Size/position:** the video is laid over the old `FR Image` rectangle (the clip's 1.333 aspect is close to the sprites'), with `sizeScale.y` set per character to keep the clip's aspect (Mark/John 0.995, Lucy/Linda 0.971). The panel art of the clip does not match the old sprite panels, so expect to nudge.

## Verification

- Compile clean; console shows only the usual serialization-depth messages that were already there.
- EditMode full suite (editor open): 2644 run, 2634 passed, 1 skipped (Explicit AI regression), 9 failed:
  - the 8 `M1RidgeTests` (the known expected failures);
  - `GridToLevelCameraStartTests.Build_ABigLevelStartsWithThePlayerUnitsInView` ("m_LockCount == 0" in `PrefabUtility.UnloadPrefabContents`), the known editor stall; it passed when re-run alone.
  - The 6 new `FamilyRoleVideoRulesTests` passed. The MCP connection dropped once during the run and recovered by polling.
- Play check (instantiated `FTPPanel.prefab` under a temporary overlay canvas in the running editor, triggered the panel animators with `PlayFRDuo`, since I could not drive a real combat/duo; the temporary canvas was destroyed after):
  - Lucy and Linda duo panels: masked moving clips, no black box (`reports/2026-11-24-duo-panel-video-duo.png`). Mark and John sliding in (`reports/2026-11-24-duo-panel-video-mark-john.png`).
  - Mark loop: sampled a corner pixel of the render texture on every frame across 2 loop wraps, max luminance 0, no white frame. (Mark's first three frames were white outside the panel.)
  - Cleanup: destroying the panel left 0 `FamilyRoleVideo` render textures, 0 VideoPlayers, 0 material copies. Disabling a panel (Lucy/Linda after their animation) released its texture earlier.
  - First frame ~0.2 s after the animator turns `FR Image` on.
- Not checked: Toba panel (no clip, no component, unchanged by construction); solo FR and Family Super Time in a real combat (they use the same `FR Image` objects, so should be identical); leaving combat mid-panel in a real level; trio. One run where I enabled `FR Image` directly from an `execute_code` call (not via the animator) never prepared in 8 s and the component fell back to the still art as designed; the animator route worked each time, so I think it was an artefact of enabling from the editor update, but it is worth watching in a real duo: if a panel ever shows the old sprite, that is this fallback.

## Files for the C1 commit

Code, shader, material, prefab, tests, masks:
- `miso/Assets/_Project/Features/UI/Panels/Scripts/FamilyRoleVideoPanel.cs` + `.meta`
- `miso/Assets/_Project/Features/UI/Panels/Scripts/FamilyRoleVideoRules.cs` + `.meta`
- `miso/Assets/_Project/Features/UI/Panels/Editor/FamilyRoleVideoRulesTests.cs` + `.meta`
- `miso/Assets/_Project/Features/UI/Panels/Shaders.meta`, `Shaders/MaskedVideo.shader` + `.meta`, `Shaders/MaskedVideo.mat` + `.meta`
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/FTPPanel.prefab`
- `miso/Assets/_Project/Content/FamilySuperTime/Sprites/Masks.meta`, `Masks/{Mark,Lucy,John,Linda}Mask.png` + `.meta`

The clips (THJ decides; untracked art, do not mix with the above): `Content/FamilySuperTime/Sprites/{Mark,Lucy,John,Linda}.mp4` and their `.meta`. `Mark.mp4.meta` carries the trim setting, so if the clips are not committed the trim is not either. Never stage: `PreloadScreen.unity`, ProjectSettings, `LevelM2-C1.prefab`, the TMP fallback asset, `DUO/Inserts/`.

## git diff --stat (tracked files)

```
.../Features/UI/Panels/Prefabs/FTPPanel.prefab | 80 ++++++++++++++++++++++
1 file changed, 80 insertions(+)
```
(plus the untracked new files above). The scene is untouched.

## What THJ should tune

On each `FamilyRoleVideoPanel` (prefab `FTPPanel`, `<Name>Role` > `FR Image`): `Size Scale` (multiplier of the `FR Image` rectangle) and `Offset` (canvas units). The slide motion itself is still the existing animator clips on `FR Image`. Masks are re-made from the clips if the art changes (procedure in the plan).

## Risks and loose ends

- Mark.mp4 is re-encoded by the importer; the other clips are played as delivered. If the art team re-exports Mark with the white frames removed, set the meta back to passthrough.
- `FR BG` Image is disabled while the video plays; the `FR BG` GameObject is still toggled by the animator.
- Audio tracks exist in the clips (stereo); audio output is set to none.
- C2 not started.

## Review fixes (applied after the review)

1. `FamilyRoleVideoPanel`: new `Fail()` used by the timeout and the error path: sets failed, unsubscribes `prepareCompleted` and `frameReady`, turns frame events off, `Stop()`. `OnPrepared` returns early when failed, so a late prepare never plays.
2. Frame-ready events are turned on just before `Prepare()` and off again after the first frame shows.
3. The sprite `Image` and `FR BG` image now stay visible until the first video frame is ready, then are hidden and the video shown; on failure/timeout they stay. `FamilyRoleVideoRules.ShouldShowStillArt(hasClip, hasMaterial, failed, videoShowing)` changed to match; tests rewritten.
   - Extra (not asked): the timeout now needs 2 s and 30 frames (`HasTimedOut(seconds, frames, showing)`). In my background editor a few frames took about 0.6 s each and the 2 s limit alone fired before the player could prepare (the clips prepare in about 5 frames), wrongly dropping to the still art.
4. `DuoInsertSequence.mode` has the tooltip (Off also turns off the card-first flow; Full / ShortAfterFirst only matter with Play Comic Insert on).
5. Card title: new pure helper `DuoInsertRules.CardTitle(caption, abilityTitle)` (caption, else the trigger ability's Title, never null) used in `UnitsCooperationHandler.Insert.cs` (`RunCardFirstIE` computes `DuoInsertRules.CardTitle(entry?.caption, triggerPreset ? triggerPreset.Title : null)` and passes it into the static `RunCardQteIE` as `cardTitle`). Glyph check: the card's font (alagard SDF) has no U+2011 and no fallbacks, and the Linda/Lucy trigger title "Marks-Sisters" contains it, so the helper swaps U+2011 for a plain hyphen for display only (ability data untouched). Test added (`CardTitle_...`).
6. `importAudio: 0` on the four clip metas; Mark's trim/transcode kept.

Results: compiles clean. CooperationInsertTests, FamilyRoleVideoRulesTests and DuoInsertRulesTests: 51 of 51 passed. Full EditMode (editor open, final code): 2654 run, 2645 passed, 1 skipped, 8 failed = the 8 known `M1RidgeTests`; the lock-count stall did not appear this time. Play re-check (temporary canvas, animator triggers): Mark and Lucy show the video with the sprite and backdrop hidden and frame events off; stopped Play after. Note: with the editor in the background the game loop runs in bursts, so Play checks need several polls.

## Final file lists

C1 code/assets (commit together): 
- `miso/Assets/_Project/Features/UI/Panels/Scripts/FamilyRoleVideoPanel.cs`, `FamilyRoleVideoRules.cs` (+ .meta)
- `miso/Assets/_Project/Features/UI/Panels/Editor/FamilyRoleVideoRulesTests.cs` (+ .meta)
- `miso/Assets/_Project/Features/UI/Panels/Shaders.meta`, `Shaders/MaskedVideo.shader`, `MaskedVideo.mat` (+ .meta)
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/FTPPanel.prefab` (+80, 0 removed)
- `miso/Assets/_Project/Content/FamilySuperTime/Sprites/Masks.meta`, `Masks/{Mark,Lucy,John,Linda}Mask.png` (+ .meta)

C1 clips (separate group, THJ decides): `Content/FamilySuperTime/Sprites/{Mark,Lucy,John,Linda}.mp4` and `.mp4.meta` (metas carry `importAudio: 0`, and Mark's trim/transcode).

C2 (its own commit): `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`, `UnitsCooperationHandler.Insert.cs`, `Core/Systems/AbilitySystem/Abilities/Editor/CooperationInsertTests.cs`, `Features/UI/DuoInsert/DuoInsertSequence.cs`, `DuoInsertRules.cs`, `Editor/DuoInsertRulesTests.cs` (all under `miso/Assets/_Project/`).

Never stage: `PreloadScreen.unity` (its diff grew from 1 to 15 lines during my Play sessions: editor noise, not mine), ProjectSettings, `LevelM2-C1.prefab`, the TMP fallback asset, `DUO/Inserts/`.

## git diff --stat (tracked files, project assets)

```
CooperationInsertTests.cs                | 74 +++ (C2)
UnitsCooperationHandler.Insert.cs        | 77 +++++--- (C2)
UnitsCooperationHandler.cs               | 17 ++- (C2)
DuoInsertRules.cs                        |  6 + (C2)
DuoInsertSequence.cs                     |  9 + (C2)
Editor/DuoInsertRulesTests.cs            |  9 + (C2)
Features/UI/Panels/Prefabs/FTPPanel.prefab | 80 +++ (C1)
(not ours: LevelM2-C1.prefab 1, PreloadScreen.unity 15)
```
New untracked C1 files are listed above (code, shader, material, masks, clips).
