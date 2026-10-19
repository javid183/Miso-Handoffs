# Report: B4 R3a · Role zones for the selected unit (A) and the Shift family view (C)

Plan: plans/2026-10-18-family-role-phase0-1.md (chunk R3a = items A and C)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (compiles, EditMode suite green except the known red; play check still needed)

## What changed

Paths under `miso/Assets/_Project/`.

**Core (Grid and Family Roles)**
- `Core/Systems/GridSystem/Runtime/GridCell.cs`: `class` becomes `partial class` (one word, no other change).
- `Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs` (+ `.meta`), new partial: the role-zone layer. New public API: `GridCell SetRoleZone(int ownerId, bool show, Color color)`. It returns the cell that holds the entry. Also `internal const string RoleZoneSpritePath`. Entries are kept per owner in a `RoleZoneLayerSet`. Each owner gets its own child `SpriteRenderer`, created on first use under a `RoleZone` child of the cell's overlay space. The renderers are 9-sliced, sorting order -10 on the base sprite's sorting layer, and use the base sprite's material. Each further owner on the same cell is drawn one inset step inside the previous one (0.94, 0.80, 0.66, ... of the Move frame size), so overlapping zones show as nested outlines in different colours. Cells covered by a multi-cell occupant redirect to `OverlayOrigin` and the outline wraps the whole footprint, the same rule as `FitOverlaysToOccupantFootprint`. Removal is done locally first, so an entry is always cleared from the cell it was set on.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: adds `[SerializeField] protected bool showRoleZone = true` with a tooltip, the getter `public bool ShowRoleZone`, and `public virtual Color RoleZoneColor` (white, alpha 0.75, for handlers without their own colour, e.g. Masher Goblin). All additive.
- `Features/Player/{John,Linda,Lucy,Mark}/Scripts/<Name>FactionRoleHandler.cs`: each gets `[SerializeField] private Color roleZoneColor = <default>` and `public override Color RoleZoneColor => roleZoneColor;`. Nothing else changed.

**Non-core**
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs` (+ `.meta`): pure C#. Per-cell owner→colour set, sorted by owner id. Set, remove and clear return "changed".
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs` (+ `.meta`): pure C#. `OwnersToShow(selected, showAllHeld, hovered, family, hasZone)` decides which zones to draw.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs` (+ `.meta`): MonoBehaviour with no statics. Listens to the bus: `unitSelectionChanged` (from `PlayerController` only), `turnStarted`, `turnEnded`, `unitDied`, `unitBorn`, `unitEndMoving`, `abilityPerformed`, `toggleShowStats`, `gridCellEntityHovered`, `gridFadeIn`/`gridFadeOut`, `levelEnded`. Events set a dirty flag, and `Update` redraws (clear all, then apply). `Update` also re-subscribes whenever `GlobalEventBus.Instance` changes, because the bus lives on the level prefab, which is spawned after the container scene loads. It reads cells only through each handler's `GetCellsInRange()`. It is null-safe: unit dead, off the grid (`CurrentCell` null), no role, handler not initialized. A throwing `GetCellsInRange()` (for example the base `NotImplementedException`) is caught and logged once per handler.
- `Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs` (+ `.meta`): 19 EditMode tests.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: new `Awake()` that adds a `RoleZonePresenter` to the same GameObject (`StatsHoverHandler` in `CombatLevelContainerScene`), plus one `using`. The existing Shift behaviour is untouched, including the L28 bug below.
- `Resources/GridOverlays/RoleZoneOutline.png` (+ `.meta`), and the folder metas `Resources/GridOverlays.meta`, `Core/Systems/RoleZoneSystem.meta`, `.../Runtime.meta`, `.../Editor.meta`: **new minimal outline sprite**. 16×16 white, a 2 px border with the corner pixels cut, PPU 100, 9-slice border 4, point filter (import settings copied from `Grid_2.png`). It's new because every existing frame sprite is already in use by another cell layer: `Grid_2` = Targeted / PotentiallyTargeted / LevelGoal, `Grid_Normal` = Move / Ability, `Grid_Off` = base, `Grid_3` = Hover. Tinting one of those would look like that layer. Loaded with `Resources.Load` per cell on first use, so there's no prefab or scene wiring.

Line endings (corrected after review): the repo's `.cs` files are LF (`.gitattributes` `text eol=lf`). Every edited file is still LF with its original BOM state (`git ls-files --eol`: `i/lf w/lf`). My first report wrongly said CRLF; that check was broken. All five new `.cs` files are LF. `GridCell.RoleZone.cs` has a BOM like its neighbour `GridCell.cs`; the `RoleZoneSystem` files have no BOM (new folder, no neighbours).

## Bool and colour names

- Bool: `showRoleZone` (serialized, on `FactionRoleHandlerBase`), getter `ShowRoleZone`. It turns off both A and C for that unit (no second bool, as briefed).
- Colours: `roleZoneColor` on each Bergson handler, getter `RoleZoneColor`. No per-character palette exists in the project (I checked UnitPanel, DialogueCharacters, cheats, combat-log colours; the Q20 palette isn't defined yet), so the defaults are Okabe-Ito (colour-blind safe), alpha 0.75:

| Unit | Colour | RGBA |
| --- | --- | --- |
| John | orange `#E69F00` | 0.902, 0.624, 0.000, 0.75 |
| Linda | sky blue `#56B4E9` | 0.337, 0.706, 0.914, 0.75 |
| Lucy | reddish purple `#CC79A7` | 0.800, 0.475, 0.655, 0.75 |
| Mark | bluish green `#009E73` | 0.000, 0.620, 0.451, 0.75 |

**Existing prefabs, verified:** the new fields are absent from `Unit_John/Linda/Lucy/Mark.prefab`, and Unity keeps the initializer values. I loaded each prefab in the editor and read the handler: all four give `ShowRoleZone = True` and the colours above. No prefab was edited or dirtied.

## Acceptance criteria

- [x] A: the selected player unit's zone is drawn continuously on a new `GridCell` layer, not on `SetInAttackRange`. The cell set is the handler's own `GetCellsInRange()`: John and Mark diamond, Linda row/column lanes, Lucy radius-3 area. The zone is cleared on deselection, when the selected unit's faction's turn ends, on the unit's death and on level end. It is redrawn after moves, abilities, births and turn start. *Test coverage: selection rules (4 tests). Geometry and visuals: play check.*
- [x] `showRoleZone` bool on `FactionRoleHandlerBase`, true by default, with a read-only getter. Off hides A and C for that unit. Existing prefabs read true (verified above). *Rules covered by tests (`Shift_SkipsMembersWithoutZone`, `NoShift_SelectedWithoutZone_ShowsNothing`); the inspector toggle needs a play check.*
- [x] C: while Shift is held, every living family unit with a zone is outlined in its colour on the same layer. Hovering a family unit that has a zone shows only that unit's zone. Hovering a unit without a zone (Toba, an enemy) keeps the full view (my call, see Decisions). *Covered by tests (9).*
- [x] Overlaps are distinguishable and don't erase each other: a per-cell owner set, nested insets, a colour per owner, the same nesting order on every cell. *Covered by tests (6, `RoleZoneLayerSet`).*
- [x] Shift's existing behaviour (info panels, `ShowStatsHoverPreview`) is unchanged. The HUD role-icon hover (`UnitPanelUI`, `SetInAttackRange`) is unchanged.
- [x] Null-safe while Shift is unguarded (enemy turns, QTEs): checked in code (`HasZone`, the try/catch around `GetCellsInRange`). *Play check.*
- [x] No change to when a role fires, FTP, AP or AI. The new code only reads the handlers. `AIRegressionTest` failure count is the same as R2 (35).
- [x] Compiles with no console errors (only the existing warnings). EditMode: **112 tests, 111 passed, 1 failed** = the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, the same count as in the R2 report). 93 → 112 = the 19 new `RoleZoneTests`.

## Shift hover preview (`ShowStatsHoverPreview.cs` L28): confirmed dead, not fixed (as briefed)

```csharp
int infiniteLoopGuard = 1000;
yield return new WaitUntil(() => GlobalEventBus.Instance == null && infiniteLoopGuard-- > 0);
GlobalEventBus.Instance.toggleShowStats.AddListener(OnToggleShowStats);
```

`WaitUntil` resumes once the predicate is **true**, so the coroutine continues only while the bus is null:
- **Bus exists at `OnEnable`:** `Instance == null` is false, and `&&` short-circuits, so the guard never counts down. The predicate stays false forever, and the coroutine never subscribes.
- **Bus missing at `OnEnable`** (the normal combat flow): `ProgramFlowHandler.HandleSceneLoading` loads `CombatLevelContainerScene` first and spawns the level prefab afterwards. `GlobalEventBus` lives on `Content/Levels/LevelBase.prefab` and sets `Instance` in `Awake`. So `Instance` is either real null, which throws a NullReferenceException on `AddListener`, or the previous level's destroyed bus. A destroyed bus passes Unity's `== null`, and the listeners get attached to that dead object.

So in every path, `toggleShowStats` and `gridCellEntityHovered` are never received from the live bus. The move/attack hover preview under Shift is dead. The world-space info panels still work because `GUnit` listens on its own.

**Suggested fix (Tier 2, its own commit):**
```csharp
yield return new WaitUntil(() => GlobalEventBus.Instance != null || --infiniteLoopGuard <= 0);
if (GlobalEventBus.Instance == null) yield break;
```
Better still, re-bind when the bus instance changes, the way `RoleZonePresenter.Update` does, because the 1000-frame guard (about 16 s) could run out on a slow level load. Once it is alive, its attack cells use `SetInAttackRange` (a plain bool shared with the role-icon hover and the ability AoE preview), so check that clash in the same pass. The role zones are on their own layer, so they are not affected.

## Save reset

No.

## Decisions I made

- **Presenter hosting:** added at runtime from `ShowStatsHoverPreview.Awake` instead of a scene YAML edit or a hook in `CombatLevelUIManager` (core). Same behaviour, no scene or core wiring. `StatsHoverHandler` is active and exists only in `CombatLevelContainerScene`, the one combat container.
- **API shape:** `SetRoleZone(int ownerId, bool show, Color color)` keyed by owner (the handler's instance id), not `SetRoleZone(bool, Color)`, because the brief asked for ref-counting or per-unit layers. Returning `GridCell` follows `SetSelected`.
- **Colour fields per handler** (as briefed): additive serialized fields on the four core handler classes, and one additive virtual getter on the base.
- **Hover with Shift on a unit that has no zone** (Toba, enemies, a Bergson with `showRoleZone` off): keep the full family view rather than show nothing.
- **"Turn ends":** the selected zone clears when the selected unit's faction ends its turn. Any other faction's turn end only triggers a redraw.
- **Grid fade (cutscenes, `GridVisualSequence`):** zones are hidden on `gridFadeOut` and come back on `gridFadeIn`, so outlines don't float over a faded grid.
- **Sorting order -10:** above `Grid_Base` (-11), below Targeted / InAttackRange (-9), Move / Ability (-8) and Hover (-7). It ties with PotentiallyTargeted and LevelGoal (-10). Those are also outlines, but the draw order between them is not fixed.
- **The zone does not follow a unit while it walks:** it redraws on `unitEndMoving`.
- **Shift with nothing hovered** draws all the family zones plus the selected unit's (the selected unit is normally one of the family).

## Needs THJ

None. The colours are placeholders for Q20; they are tweakable per prefab in the Inspector.

## Docs to update

- `tech/combat-architecture.md`: the role-zone layer (`GridCell.SetRoleZone`, sorting order -10, the Resources sprite), `RoleZonePresenter` and where it is hosted, the `showRoleZone` / `roleZoneColor` names.
- `design/gdd/family-systems.md` (designer): zones shown for the selected unit and under Shift (FR-8 draft).
- `build-log.md`: R3a entry (coordinator).

## Risks and loose ends

- **Reviewer, core:** `GridCell` is thread-sensitive for the AI. The new fields are touched only from the main thread (presenter); the AI never calls `SetRoleZone`. `GridCell` field initializers (`new RoleZoneLayerSet()`, `new List<SpriteRenderer>()`) also run for `AIRegressionTest`'s `AddComponent<GridCell>()`, which is harmless.
- **Visual tuning untested:** inset sizes, alpha 0.75, 2 px line width, and readability against Move / Ability frames and the base grid. Four nested outlines on one cell get small (innermost 0.52 of the frame).
- **Footprint redirect:** a zone that touches one cell of a 2×2 enemy outlines the whole enemy, like the other layers do. That is consistent, but it can read as "the zone reaches further". Look at it with a big enemy in Linda's lane.
- **Redraw triggers:** stat changes that change a radius (Linda's Longshot) redraw only on the next listed event (ability performed, move end, turn start, selection). Pushes and teleports that don't raise `unitEndMoving` redraw on the next `abilityPerformed`.
- **Ability target selection:** the selected unit's zone stays visible under the Ability highlight while you pick a target. Check that it isn't cluttered.
- **Nesting order:** by handler instance id. It is the same on every cell in a session, but not fixed across sessions.
- **Not touched, noticed:** `UnitPanelUI.ClearUnitControlPanel` still doesn't clear the role-icon hover cells (from the facts sheet). `ShowStatsHoverPreview` is dead (above).

## Proposed commits

Reviewer's three-commit split. Paths are under `miso/Assets/_Project/`. Each commit compiles on top of the ones before it: (a) is self-contained; (b) needs nothing new; (c) uses `GridCell.SetRoleZone` from (a) and `ShowRoleZone` / `RoleZoneColor` from (b).

a. `feat(grid): per-owner role-zone layer on GridCell (B4 R3a)` (**core**, Grid):
   - `Core/Systems/GridSystem/Runtime/GridCell.cs`
   - `Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs` + `GridCell.RoleZone.cs.meta`
   - `Core/Systems/RoleZoneSystem.meta`
   - `Core/Systems/RoleZoneSystem/Runtime.meta`
   - `Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs` + `RoleZoneLayerSet.cs.meta`
   - `Resources/GridOverlays.meta`
   - `Resources/GridOverlays/RoleZoneOutline.png` + `RoleZoneOutline.png.meta`
b. `feat(roles): showRoleZone toggle and role-zone colour on Family Role handlers (B4 R3a, D-063)` (**core**, Family Roles):
   - `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `Features/Player/John/Scripts/JohnFactionRoleHandler.cs`
   - `Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs`
   - `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
   - `Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`
c. `feat(ui): draw the selected unit's role zone and every family zone while Shift is held (B4 R3a, D-064)` (plain):
   - `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs` + `RoleZonePresenter.cs.meta`
   - `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs` + `RoleZoneRules.cs.meta`
   - `Core/Systems/RoleZoneSystem/Editor.meta`
   - `Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs` + `RoleZoneTests.cs.meta`
   - `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`

Review fixes applied: new `.cs` files converted to LF; `FitRoleZoneRenderers` now starts with `if (!gridCellHighlightMoveVisual || !_roleZoneRoot) return;`. After the fixes: no console errors; EditMode 112 tests, 111 passed, only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` failing (35 failures). Should-fix 4 (zones popping back in on `gridFadeIn`) is left for the play check.

Do not stage the unrelated working-tree changes (`Packages/manifest.json`, `packages-lock.json`, `ProjectSettings.asset`).

## Other branches

`thj/home-test` on its next merge of `main`.

## How to see it

1. Open Unity, recompile (Ctrl+R), and start any combat level with John, Linda, Lucy and Mark.
2. Select **John**: a faint orange outline on his radius-2 diamond, the four diagonal neighbours inside, the (2,1) cells outside. Select **Mark**: a green diamond. Select **Linda**: blue outlines only along her row and column out to radius 4. Select **Lucy**: a purple radius-3 area. The outline sits under Move / Ability frames and hover.
3. Move the selected unit: the zone redraws at the end of the move. Deselect and end the turn: the zone disappears.
4. Hover the role icon on the unit panel: the old red-sword `SetInAttackRange` highlight still appears on top. Unhover: the zone outline stays.
5. Hold **Shift**: all living Bergsons' zones in four colours. Overlapping cells show nested outlines. Hover one Bergson while holding Shift: only that zone. Release Shift: back to the selected unit's zone.
6. Hold Shift during an enemy turn and during a role QTE: no errors in the console.
7. Kill or down a Bergson (cheats): its zone goes away on death. Put a 2×2 enemy inside Linda's lane: the outline wraps the enemy's footprint.
8. On a unit prefab, untick `Show Role Zone` on its role handler: no zone for that unit, selected or under Shift.
9. Win or lose the level: no outlines remain.
