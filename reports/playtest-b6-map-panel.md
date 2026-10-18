# Report: Playtest batch 1, C4 B6 map panel

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md (chunk C4)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (play check of the real Home scene still needed)

## What changed

- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/LevelInfoPanel.prefab`: root RectTransform re-anchored to the right edge: anchorMin/Max (1, 0.5) (was 0.5, 0.5), pivot (1, 0.5) (was 0.5, 0.5), anchoredPosition (-40, 0) (was 746, 0). Size and y unchanged. Plain LF, GUID/.meta untouched.
- `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/WorldMapPanel.prefab`: the "Level Info" instance overrides the root's m_Pivot.x, m_AnchorMin.x, m_AnchorMax.x and m_AnchoredPosition.x with the OLD values (0.5, 0.5, 0.5, 746), so the prefab edit alone would not have fixed the world map. Those four overrides now read 1, 1, 1, -40. Nothing else touched.
- No code change: nothing in `Core/UI/Runtime/Home/WorldMap/` sets the position.
- `MissionMap.prefab` not changed: its instance already overrides the root to anchor (1, 0), pivot (1, 0), pos (-45, 86.2), size (451.8, 285), which is right-edge anchored and unaffected by the base prefab change.

## Acceptance criteria

- [x] B6: mission info panel fully inside the screen on the world map and mission map at 16:9, 16:10, 4:3. Evidence: ran a scratch check in the editor (instances of both prefabs on a 1080-high canvas, matching the scene's CanvasScaler: 1920x1080 reference, match = height; GetWorldCorners compared to the canvas rect; nothing saved, objects destroyed). The world map instance was placed the way `Home - Scene.unity` places it (stretched, scale 1.3 from the prefab root, anchored position x = -280, from the scene's modifications).

| Aspect | Canvas half-width | World map panel x | Mission map panel x |
|---|---|---|---|
| 16:9 | 960 | 328.7 .. 916.0 (inside, 44 margin) | 463.2 .. 915.0 (inside) |
| 16:10 | 864 | 203.9 .. 791.2 (inside) | 367.2 .. 819.0 (inside) |
| 4:3 | 720 | 16.7 .. 604.0 (inside) | 223.2 .. 675.0 (inside) |
| 21:9 (extra) | 1260 | 718.7 .. 1306.0 (46 OUTSIDE) | 763.2 .. 1215.0 (inside) |

  Vertical fits at every ratio (world map -459.6 .. 459.6 of +-540). The plan said ~12 px off at 16:9; the real number before the fix was larger, because the world map root is scaled 1.3 and shifted by the scene (old right edge was about 984 vs 960 at 16:9, by the same formula).
- [x] Overrides in WorldMapPanel.prefab and MissionMap.prefab checked: WorldMapPanel overrode the position (fixed above); MissionMap overrides to its own right-anchored layout (left alone).
- [x] EditMode suite: 67 run, 66 passed, 1 failed, the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Includes C3's tests.
- [ ] Looked at in the real Home scene in Game view: not done (I did not open or modify scenes). Needs the play check.

## Save reset

no

## Decisions I made

- Offset of -40 (plan said -20 to -40): the world map scale of 1.3 turns it into about 52 screen px of margin.
- Edited the four WorldMapPanel override values rather than deleting the override entries, to keep the YAML edit minimal and safe.

## Needs THJ

none

## Docs to update

- `build-log.md`: coordinator adds the C4 line at the end of the batch.

## Risks and loose ends

- 21:9 (and wider) world map: the panel overshoots the screen edge by about 46 px, because `Home - Scene.unity` shows the world map panel scaled 1.3 and shifted -280; anchoring to the parent's right edge cannot compensate for a scale that exceeds the screen. Not in the acceptance ratios; the fix would be a scene or WorldMapPanel root change (out of this chunk). Mission map is fine at 21:9.
- At 4:3 the world map panel is wide (about 588 px on a 1440 canvas) and may overlap map content; I did not check what it covers.
- Working tree also holds C3's uncommitted files (`UI_Element_FillBar.cs`, `FillBarTextFormatter.cs` and `Editor/`) and unrelated package/project-settings changes; I did not touch them.

## Proposed commits

1. `fix: anchor the world map mission info panel to the right edge so it stays on screen`: `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/LevelInfoPanel.prefab`, `miso/Assets/_Project/Features/UI/Panels/Prefabs/UI/Home/WorldMapPanel.prefab` (plain; no new assets, so no .meta files)

## Other branches

none (`thj/home-test` gets it on its next merge of `main`, as the plan says)

## How to see it

1. Open the Home scene, enter Play, open the world map and select a mission: the info panel sits against the right edge with a margin.
2. In the Game view switch between 16:9, 16:10 and 4:3 and check the panel stays fully visible.
3. Open the mission map (MissionMap prefab) the same way; it should look unchanged.
