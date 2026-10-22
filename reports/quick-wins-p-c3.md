# Report: Quick wins P, C3 (pace values, banner layout, banner stops catching clicks)

Plan: plans/2026-10-22-quick-wins-p-pace-tech.md (section C3 + "Also (from the C1 review)"; P1 answered in D-141)    Agent: implementer    Branch: thj/quick-wins
Outcome: done (play check pending)

## What changed

Paths under `miso/Assets/_Project/`. Data only, no C#.

- `Content/Controllers/AIController.prefab`: `holdTimeAfterActionCompletion` 0.5 -> 0.25 (line 47). `turnStartPause: 0.5` from C1c kept. Player and auto-player prefabs untouched (0.5).
- `Scenes/CombatLevelContainerScene.unity`:
  - `GameSessionHandler.timeBetweenFactionTurns` 0.5 -> 0.25.
  - `endLevelDelayBeforeHudHide: 0.25` and `endLevelDelayAfterHudHide: 0.25` written by the editor save (the C2 fields at their initialiser values; expected, no behaviour change).
  - PhaseVisuals instance overrides: `m_Pivot.x` 0.5 -> 1, `m_AnchorMin.x` 0.5 -> 1, `m_AnchorMax.x` 0.5 -> 1, `m_AnchoredPosition` (0, 200) -> (760, -260). Pivot y, anchor y (1), size 570x170 and scale 1.3 overrides unchanged.
  - PhaseVisuals instance override `animationDuration` 0.8 -> 0.25 (see Decisions: the scene already overrode this field, so the prefab change alone would not have applied). The scene's existing `waitTime` override is already 0.5, left as is.
- `Scenes/DevScenes/TestLevel.unity`: `timeBetweenFactionTurns` 0.5 -> 0.25 (one-line YAML edit; the scene was not re-saved, so the C2 fields are not written there and their initialisers apply).
- `Scenes/PreloadScreen.unity`: `ProgramFlowHandler.minimumLoadingTime` 1.5 -> 0.5 (build-only effect).
- `Features/UI/Panels/Prefabs/UI/PhaseVisuals.prefab` (root `PhaseVisuals`):
  - RectTransform: anchors (0.5, 1) -> (1, 1), pivot (0.5, 1) -> (1, 1), anchoredPosition (0, -44.4) -> (760, -260) (rests hidden).
  - `PhaseVisualsUI`: `hiddenAnchoredPosition` (0, 200) -> (760, -260), `shownAnchoredPosition` (0, -25) -> (-16, -260), `animationDuration` 0.8 -> 0.25, `waitTime` 1.5 -> 0.5.
  - New `CanvasGroup`: alpha 1, `interactable` off, `blocksRaycasts` off, ignoreParentGroups off.
  - `UIPanelAnimator`: `visibilityTags: [All]` now serialized (Unity wrote the field's initialiser on save; same value it had at runtime, and the scene instance overrides the array to size 0 anyway). Unavoidable re-save noise in the same file.

Geometry (canvas: Screen Space Overlay, scaler 1920x1080 matching height, so the canvas is always 1080 tall; 1920 wide at 16:9, 1440 at 4:3). The banner rect is 570x170 at scale 1.3 = 741x221 canvas units, pinned by its top-right corner. Shown: right edge 16 px in from the screen edge, top 260 px below the top. The visible part is the TopPanel (faction name, 125 x 1.3 = 162 tall), so the visible band is 260..422 px from the top, centred at about 341 (the upper third ends at 360). Hidden: x = +760, i.e. the banner's left edge sits 19 px past the right screen edge, so it slides in horizontally from off-screen right with no vertical motion.

## Acceptance criteria

- [x] AI hold after action 0.25, player/auto-player 0.5: YAML diff.
- [x] Gap between faction turns 0.25 in both combat scenes: YAML diff; the loaded scene read 0.25 through SerializedObject before saving.
- [x] Loading pad 0.5: YAML diff (build-only; the editor skips it, not play-verifiable in editor).
- [x] Banner 0.25 slide / 0.5 hold: prefab and the scene override both set; read back on the scene instance as dur=0.25, wait=0.5.
- [x] Banner at the right edge, upper third, sliding in from off-screen right: layout set as above; read back on the scene instance. Not seen on screen (see Overlap check).
- [x] Banner does not catch clicks: CanvasGroup `blocksRaycasts` off on the root covers every child graphic (Images, TMP texts, the inactive FTPIndicator). Needs the play check (click/hover grid cells under the banner).
- No EditMode test coverage: data only, nothing testable outside Play.

## Overlap check

Done numerically from the scene's RectTransforms (the editor was not put in Play mode, and the banner rests off-screen in Edit mode, so no Game view screenshot was taken). Banner shown, in canvas units from the top-right: x from W-757 to W-16 (16:9: 1163..1904; 4:3: 683..1424), visible y 260..422 (rect bottom 481, the lower part is the inactive FTP indicator strip, nothing drawn).

- Objectives panel (top-right, 300 wide at x W-350..W-50, top 31 px down, 90 tall folded, grows with its entries): same x range as the banner. Clear while the panel ends above 260 px. I measured entries in the editor (font 20): about 34 px per one-line objective, 58 px for a wrapped one; three objectives with one wrapped gave a list of 166 px, which puts the open panel's bottom at roughly 280 px, about 20 px into the banner's top edge. One or two objectives stay clear. Where they touch, the objectives panel draws over the banner (PhaseVisuals is the canvas's first child). Play check item.
- End Turn panel (bottom-right, 875..1045 px from the top): clear at both ratios.
- Unit panel (CharacterHUD bottom-left, AbilitiesHUD bottom-centre, StatusTooltips bottom-right growing up from 864 px): clear.
- Level info panel (top-left, x 50..400): clear at both ratios (at 4:3 the banner starts at x 683).
- Narrator dialogue box (top-centre, 15..185 px) and dialogue bottom panel (750..1050 px): clear vertically. On-screen avatar (right-middle, 490..590 px): below the banner's visible band.
- `InfoPanel` / `LevelNameLbl`: they sit under `MiddlePanel`, which is inactive in the prefab, and no code turns it on, so they never show; nothing to re-check.

## UIPanelAnimator on the banner root

Unused: nothing calls `Show`/`Hide` on it (`CombatLevelUIManager` only drives `PhaseVisualsUI`; the phase banner lines in `HideHUD`/`ShowHUD` are commented out apart from `HideInstant`), and the scene instance overrides its `visibilityTags` to an empty array, so the dev `HUDVisibilityToggle` never picks it up. Left alone as asked; its positions are still the old top-centre ones ((0, 200) / (0, -25)). If anything ever drives it again, those need aligning.

## Compile, console, tests

- No scripts changed. Recompile requested: no compile errors. Console has only the long-standing "Serialization depth limit" warnings and two "Objects are trying to be loaded during a domain backup" messages (MCP/editor, not from this change).
- EditMode: 522 run, 521 passed, 1 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Not touched.
- After the final asset refresh the Unity MCP stopped answering pings (the editor log shows PreloadScreen reloaded normally); I could not re-read the console after that last refresh. Nothing compiled in that refresh (one scene file only).

## Save reset

No.

## Decisions I made

- Layout set in **both** prefab and scene instance, by editing values the scene already overrode: the prefab got anchors/pivot/rest position and the `PhaseVisualsUI` hidden/shown positions (so the prefab is self-consistent), and the scene's existing overrides got the matching values (5 changed values, no added or removed override entries). Smaller than adding new overrides for the animation positions on the instance.
- Scene override `animationDuration` 0.8 -> 0.25 (not in the plan's file list): the scene instance already overrode it, so changing only the prefab would have left the banner at 0.8 s. Same intended behaviour.
- Raycasts: CanvasGroup on the root (`blocksRaycasts` off, `interactable` off) instead of turning Raycast Target off per graphic: one component, also covers the nested FTPIndicator prefab and any graphic added later.
- Banner top at 260 px below the screen top: the lowest point that keeps the visible band centred inside the upper third while clearing the objectives panel with one or two objectives.
- Layout edits went through the editor (PrefabUtility.LoadPrefabContents / SaveAsPrefabAsset; RectTransform on the scene instance, then EditorSceneManager.SaveScene); the plain value fields were one-line YAML edits (PreloadScreen, which THJ had open, through SerializedObject + save).
- Noise removed by hand: opening `CombatLevelContainerScene` and measuring the objectives panel left a no-op override (`ObjectivesPanel` child `m_SizeDelta.y = 0`, equal to the prefab) that I deleted from the YAML; the Test Runner re-saved the open `PreloadScreen` with TMP/layout-group size and anchor changes on three RectTransforms, which I reverted by restoring the file from HEAD and re-applying the one value line.

## Needs THJ

None blocking. Play check below decides whether 260 px is right with three objectives.

## Docs to update

- None beyond the plan's commit log and the build log (coordinator).

## Risks and loose ends

- With three or more objectives (or long wrapped ones) the open objectives panel can reach about 20 px into the banner's top, drawn over it. If THJ sees that, options: move the banner down (for example y -300, centre about 381, just below the upper third), or fold the objectives during the banner. Tier 3 if it happens.
- The banner's `UIPanelAnimator` keeps stale top-centre positions (unused).
- `TestLevel.unity` was not re-saved, so the C2 fields are still absent there (initialisers apply, same behaviour).
- Other noise in the working tree, not from this chunk, to leave out of the commit: `miso/Packages/manifest.json`, `miso/Packages/packages-lock.json`, `miso/ProjectSettings/EditorSettings.asset`, `miso/ProjectSettings/ProjectSettings.asset`, `miso/Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset` (all were modified before this session).
- The Unity MCP was unresponsive at the end; THJ may see the editor waiting on something. Worth a glance before the play check.

## Proposed commits

1. `tweak(combat): faster turn pace and a shorter, side-mounted turn banner that lets clicks through`: `miso/Assets/_Project/Content/Controllers/AIController.prefab`, `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`, `miso/Assets/_Project/Scenes/DevScenes/TestLevel.unity`, `miso/Assets/_Project/Scenes/PreloadScreen.unity`, `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/PhaseVisuals.prefab` (plain; data only, no `.meta` changes). The banner layout and timing live in both the prefab and the scene instance, so they go together; the pace values could be split into their own commit if THJ prefers (`tweak(combat): shorter AI hold, turn gap and loading pad`: AIController.prefab, TestLevel.unity, PreloadScreen.unity; but `CombatLevelContainerScene.unity` holds both the turn gap and the banner overrides, so it would have to go in one of the two).

## Other branches

`thj/home-test` takes this with `main` (per the plan).

## How to see it

1. Open `CombatLevelContainerScene` (or start a level as usual) and press Play.
2. At the first player turn: the "<Faction> Turn" banner slides in from the right edge, upper third (top about a quarter of the way down), holds about half a second and slides back out to the right. Total about 1 s.
3. While the banner is on screen, hover and click grid cells under it: the hover highlight and the click should work (End Turn stays locked during the player's banner, as before).
4. End the player turn: the enemy banner follows after a short gap (0.25 s); enemy actions follow each other with a shorter hold (0.25 s after each).
5. Check the objectives panel at the top-right against the banner on a level with three objectives; set the Game view to 16:9 and then 4:3 and look for overlap with the objectives, unit panel and End Turn panel.
6. Loading pad (0.5 s) only shows in a build.
