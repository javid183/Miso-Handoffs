# Report: onboarding 1.7 (X-34) and 1.8 (X-36) draw order

Status: **stopped, no files changed.** Neither bug matches the description by static inspection or by an editor-side render, so a fix would be a guess. Needs THJ input (below). Tier 1 held; no core file touched. No Play mode entered, no tests run (nothing changed).

## 1.8 Selected-unit indicator on GB_* levels

What I checked (Unity MCP, read-only; renders done in a temporary additive scene that was closed again, git status unchanged):
- The indicator is one prefab (`Features/_Common/Prefabs/SelectedUnitIndicator.prefab`) spawned by `UnitSelectionIndicatorManager` in `CombatLevelContainerScene`, so it is identical on every level. Sprite: Default layer, order -3000. Its Light2D (point) targets only the Ground layer. Khash's commit changed only that light's intensity (4.43 to 1.3) plus the level prefabs' background layers.
- Layer values: Ground -2, UnderObjects -1, Default 0. Ground renders below Default, so Ground backgrounds can never cover the indicator sprite.
- GB_* levels use the same template (`LevelM1-C2`) environment. The `Background` sprite renderer is byte-for-byte the same properties as the template's (Ground, -3000, TestLevel1_0) and as `LevelM1-C1`/`C2`/`C3`, `Level1-C1`, `Level3-C1`. All 14 GB levels: background on Ground, covers every cell, nothing on Default between -3000 and the cell visuals that is large enough to cover a cell. Cells, Grid_Base (semi-transparent outline, Default -11), z positions, SortingGroups (none), Light2Ds: same as older levels. The GB builder sets no sorting values (`GridToLevelBuilder` has none).
- Render check (global light copied from the container scene, indicator prefab placed on a cell and on a hero, URP 2D, no Play): the ring draws above the floor in `GB_m4-mark`, `LevelM1-C2` and `Level2-C1` alike. On the GB level the floor art is darker, so the ring's light pool is faint, but the ring itself is visible and drawn over the ground.

So I could not find a sorting difference between GB and older levels, and the indicator sprite is visible in my render of a GB level. Possible real causes I could not test without Play: something at run time (a memory-level flow hiding or re-selecting the indicator), the faint light pool on the dark GB floor being what "doesn't show", or the specific level THJ saw.

**Needed from THJ:** which GB level and hero (screenshot if possible), and one older level where it looks right. If the missing part is the glow, the fix is the indicator's light (raise intensity or add UnderObjects to its layers), which changes older levels too, so it needs OK.

## 1.7 Mark's avatar and the HUD frame

- The combat unit panel is `Features/UI/Panels/Prefabs/UI/HUD/UnitPanel.prefab` > `CharacterHUD`. The frame (ornament square) is part of the root `HUD_Background_0` image; `UnitAvatar` is its child, so for every hero the avatar draws in front of that image. Order is not hero-specific; `UnitPanelUI` has no Mark-specific avatar code.
- The portrait asset differs: John, Linda, Lucy, Toba are 342x335 with a baked gold border and a 2 percent transparent margin; `Avatar_Mark.png` is 567x567, an unframed octagon touching all four edges (no margin, no border). Rendered, Mark's dark octagon edge sits over the inner gold line of the ornament, the others' baked border sits inside it.
- The frame cannot simply be drawn over the portrait: the ornament's interior is opaque art, it would hide the face. A real "behind the frame" needs either a frame-only sprite (art) or a mask on the window.

**Needed from THJ:** confirm the screen (this unit panel; the turn-order bar `ATBBar_mod` and dialogue panel also show avatars). Proposed fix once confirmed, Mark-only: pad `Avatar_Mark.png` to the others' footprint (2 percent margin) so the octagon sits inside the ring, or add a window mask in `CharacterHUD`. Both are small; the first is an art-file change, the second changes every hero's panel slightly.

## Files changed
None (scratch renders only, in the scratchpad).

## Test results
None run; nothing changed.

## Proposed commits
None.

## How to see it
Not applicable until the above is answered.
