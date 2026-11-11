# Report: Synergy aim preview, chunk C1 (shared lane drawing + Shield Flare lanes)

Plan: plans/onboarding/2026-11-10-synergy-aim-preview-tech.md    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check pending)

## What changed

Paths under `miso/Assets/_Project/`.

- `Features/Player/Shared/Synergies/SynergyLanePresenter.cs` (new, + `.meta`): non-core presenter, modelled on `QuiverAimPresenter`. Each frame it reads the aimed ability (`QuiverLevelAccess.AimedAbilityOrNull`, the same null-safe read the quiver uses), the hovered cell (bus `gridCellHovered` / `gridCellEntityHovered`) and `PlayerController.IsLegalAbilityTarget` / `TargetCellCount`. When the effect the next click fires is a spawner whose projectile is an `IProjectilePreviewRedirect` (Lucy's fireball) and that redirect accepts the aim cell, it draws one straight gold LineRenderer per copy, from the relaying unit's cell (John) to each target cell. It uses a LineRenderer pool and a runtime Sprites/Default material. It draws lines only and never calls `ShowDamagePreview`, so it shares no damage-preview state with `PlayerController`. No statics.
- `Features/Player/Shared/Synergies/SynergyLaneRules.cs` (new, + `.meta`): pure rules. `ShowLanes(levelEnded, aiming, hoveredIsLegalTarget, triggersSynergy)`, and `EffectsForNextPick`, which picks the effects the next click fires and mirrors `AbilityDamagePreview`'s one-effect-per-target mapping.
- `Features/Player/John/Scripts/ShieldFlareGeometry.cs` (new, + `.meta`): the copy-target walk (`FindTarget`, `Directions`), pulled out of `JohnShieldRelay` and working on grid coordinates only, so it can be tested.
- `Features/Player/John/Scripts/JohnShieldRelay.cs`: `CollectCopyTargetCells` now calls `ShieldFlareGeometry` through a cell classifier (`KindAt`) that keeps the old checks: no cell, an enemy occupant, any other occupant, a targetable planted entity, free. The duplicated direction arrays are removed. Behaviour is unchanged, and `TryCollectCopyTargetCells` (public) is untouched.
- `Features/Player/Shared/Synergies/Editor/SynergyLanePresenterSetup.cs` (new, + `.meta`, + `Synergies.meta`, `Editor.meta`): menu `Tools/Synergies/Place Synergy Lane Presenter`. It puts a `SynergyLanePresenter` root object in `CombatLevelContainerScene.unity` and is safe to run again.
- `Scenes/CombatLevelContainerScene.unity`: the menu item added the `SynergyLanePresenter` root object (GameObject + Transform + MonoBehaviour, plus one `SceneRoots` entry; 45 added lines, nothing else changed). I ran it once.
- `Features/Player/Shared/Synergies/Editor/SynergyLaneTests.cs` (new, + `.meta`): 10 EditMode tests.

All new files are LF without a BOM, like their neighbours. `JohnShieldRelay.cs` stays LF.

## Acceptance criteria

- [x] Flare lanes appear only when the real shot would trigger. The lanes need all of these: the player's own target selection, a hovered cell the click accepts (`IsLegalAbilityTarget`, the check the cursor uses), and the projectile's redirect returning true. That redirect is `JohnShieldRelay.TryCollectCopyTargetCells`: shield up and John on a cell, the same gate as `TryReceive`. *Tests:* the show rule and the effect-per-pick mapping. *Play check:* aim with the shield down (no lanes) and with it up (lanes).
- [x] Lanes match where the copies go. There is one source: the cells come from `TryCollectCopyTargetCells`, which `LaunchCopies` also uses, now through the shared `ShieldFlareGeometry`. *Tests:* lane ends on 7 drawn boards (open board, first enemy wins, an ally next to John drops the lane, a far blocker stops on the last free cell, grid edge and holes, planted target, straight pattern). *Play check:* aim, fire, compare.
- [x] Damage previews use the normal bars and skull, and none falls on John. Unchanged: the copy-target damage still comes from `PlayerController` → `AbilityDamagePreview` (commit `4e2ac96f0`), which returns before adding John. The presenter adds no damage preview. *Play check.*
- [x] Lanes clear on cancel, ability switch, end turn and level end. The presenter polls every frame: the aimed ability turns null outside the player's own `TargetSelection` (cancel, end turn, enemy turn), a different ability fails the redirect check, and `CombatLevelRunHandler.IsLevelEnded` hides them at level end. `OnDisable` and `OnDestroy` hide them too. *Play check* for each case.
- [x] No core file edited. `JohnShieldRelay` is a feature file, not on the core list. Core APIs are only called: `IsLegalAbilityTarget`, `TargetCellCount`, `IProjectilePreviewRedirect`, `GridCell.AnchorPoint`.
- [x] Console clean: no new errors or warnings after the recompile (the pre-existing CS0108, CS8509 and similar warnings remain).
- [x] EditMode: 1826 tests, 1825 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. `SynergyLaneTests` run on their own: 10/10 passed.

## Save reset

No.

## Decisions I made

- Tier 1: I pulled Flare's copy-target walk out into the pure `ShieldFlareGeometry`, called by `JohnShieldRelay`, so the plan's "lane endpoints for a few layouts" tests can run without a level. Behaviour is the same. It is the same kind of extraction the plan prescribes for Bloom and Catch.
- Tier 1: the presenter gets the Flare cells through `IProjectilePreviewRedirect.TryGetRedirectTargetCells`, the exact call `AbilityDamagePreview` makes. It wraps `TryCollectCopyTargetCells`, so lanes and damage bars always agree. The lane origin is the aim cell occupant's `CurrentCell`.
- Tier 1: lanes need `IsLegalAbilityTarget`, a slightly stricter gate than the damage preview, which shows on any in-range cell. So lanes only appear on a cell that can actually be clicked.
- Tier 1: I reused `QuiverLevelAccess` (Linda's quiver folder, same namespace) for the null-safe player and aimed-ability reads instead of copying it. If C2 or C3 want a neutral name, it could move.
- Tier 1: look. Straight lines (the fireball's trajectory is `Direct`), width 0.03, the Flare popup's gold at 85% alpha, sorting layer `WorldUI` order 47 (the same as the quiver lines). Tuning is THJ's call in the play check.
- Folder: `Features/Player/Shared/Synergies/`, so C2 and C3 can add Bloom and Catch beside it. The menu sits under `Tools/Synergies/`.

## Needs THJ

None for C1. One possible follow-up is in loose ends (lanes for earlier picks).

## Docs to update

- `tech/combat-architecture.md` (coordinator): Synergy lanes come from `SynergyLanePresenter` in the combat container scene; Flare geometry lives in `ShieldFlareGeometry`.
- GDD `combat-rules.md` and `family-systems.md` (designer), per the plan's gates.

## Risks and loose ends

- **Lanes for earlier picks.** Lucy's main attack takes two picks (`oneEffectPerTarget`). Lanes follow only the pick being hovered. After John is picked once, the confirmed copy damage stays on the bars (that is `PlayerController`'s preview), but that pick's lanes go away when the cursor moves. Keeping them needs the picked cells, and only `TargetCellCount` is public. Showing them would take a read-only core getter (Tier 3), or tracking clicks in the presenter, which is fragile. Flagging it rather than doing it.
- **Path to John not checked.** Like the existing redirect preview, the lanes assume the fireball reaches John's cell. The fireball's trajectory is `Direct`; I didn't check whether a unit standing between Lucy and John could catch it first. If it can, the damage preview has the same mismatch.
- **Auto-move shots** aren't handled. Lucy's attack has `autoMoveAllowed: 0`, so this can't happen today.
- **Scene save.** The menu item calls `SaveScene` on the container scene. If THJ had unsaved edits open in that scene, they would be saved too. The diff shows only the new object.
- The plan's risk "Linda's bow has no lane today" concerns C2 and C3, not this chunk.

## Proposed commits

1. `feat(combat): aiming Lucy's fireball at a shielded John draws the lanes of the copies his Shield Flare would launch` (plain; one unit: the extraction, the presenter, its placement and its tests only work together)
   - `miso/Assets/_Project/Features/Player/John/Scripts/JohnShieldRelay.cs`
   - `miso/Assets/_Project/Features/Player/John/Scripts/ShieldFlareGeometry.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLaneRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/Editor.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/Editor/SynergyLanePresenterSetup.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/Editor/SynergyLaneTests.cs` + `.meta`
   - `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`

Leave out THJ's uncommitted files: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` and the TMP fallback font.

## Other branches

`main`, when this branch merges (the presenter object is in the shared container scene).

## How to see it

1. Open any combat level where John and Lucy are both in the party (or a sandbox level with both and a few enemies around John), and press Play.
2. On John's turn, raise his shield (Shield Up), then select Lucy and her main attack (fireball).
3. Hover John: gold lanes run from John to the four diagonal cells his copies will fly to, at most 2 cells, stopping on the first enemy. A line blocked right next to John has no lane. Enemies at the lane ends show the normal damage bars and skull; John shows none.
4. Fire and check that the copies follow the lanes.
5. Clearing: hover John, then (a) right-click or cancel, (b) pick another ability, (c) end the turn, (d) finish the level with the aim up if you can. The lanes vanish each time.
6. With John's shield down, hovering John shows no lanes.
7. Console: no new errors or warnings.

## Should-fixes (after review)

- `ShieldFlareGeometry.Directions` now returns `IReadOnlyList<Vector2Int>`, so callers can't change the shared static arrays.
- `JohnShieldRelay`: the line-walk comment sits on `CollectCopyTargetCells`; `KindAt` has its own one-line comment.
- Recompiled: console has no errors and no warnings from these files. `SynergyLaneTests` 10/10 pass. The two-pick gap is left as it is, for THJ to decide.

## Round 2: ghost fireballs instead of lines

THJ's play check: the gold lines looked like a debug drawing. His call: no lines; show each Flare copy as a faint fireball around John, facing the way it will fire.

What changed:
- `SynergyLanePresenter.cs` was rewritten and no longer has any LineRenderer. For each copy it draws one pooled SpriteRenderer "ghost" in the look of the fireball the copies actually use: the relay's `copyPrefab` (`AttackFireBall`), or the incoming fireball when the relay has none. The ghost takes that prefab's sprite, material, tint and scale.
  - **Position:** on a small ring around John's cell, on the side of its copy's direction.
  - **Facing:** rotated along the world direction from John's cell to that copy's target cell, the same way the projectile turns in flight (head axis Right).
  - **Where the data comes from:** directions and targets still come from `TryCollectCopyTargetCells` and `ShieldFlareGeometry`. The show and hide rules and the lifecycle are unchanged.
  - **Reuse:** the presenter now builds a list of generic ghost requests (a projectile look, an anchor, a direction). Bloom and Catch can add their own requests around the Cyclone or Mark. Neither is built.
- Inspector fields on `SynergyLanePresenter`, in the container scene. The scene YAML wasn't touched: the new fields take their code defaults until the scene is next saved.
  - `ghostAlpha` 0.5.
  - `ghostScale` 0.6 (relative to the real projectile).
  - `ringRadiusCells` 0.45.
  - `anchorLiftCells` 0.25 (ring centre slightly above the cell).
  - `bobAmplitudeCells` 0.03 and `bobCyclesPerSecond` 0.6: a slow drift out along the ghost's own direction and back, staggered per ghost. Set either to 0 for still ghosts.
  - `flareHeadAxis` Right.
  - Sorting: layer `WorldUI`, order 47, so the ghosts sit above John and the ground.
- `GhostProjectileRules.cs` (new, + `.meta`): pure `TryPose` (ring position and z rotation per direction, sprite pointing right or up, bob along the direction) and `Bob`.
- `SynergyLaneRules.ShowLanes` was renamed to `ShowCopies`. The rule itself is unchanged.
- Tests: 5 new ones (15 in all). They cover the pose on all 8 directions including diagonals, an up-pointing sprite, the bob going along the direction, a zero direction being rejected, the bob staying within its amplitude or still at 0, and Flare ghosts facing each lane end from the shared geometry.
- Verified: EditMode 1831 run, 1830 pass; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. Compile is clean, with no warnings from these files.
- One console error, `Objects are trying to be loaded during a domain backup`, comes up on every recompile. Only `PreloadScreen.unity` was open, so no `SynergyLanePresenter` instance existed, and these scripts have no serialization callbacks. I believe it isn't from this change, but I didn't confirm it against a build without it. The other errors in the console come from the full test run's own logging.
- THJ was in Play mode when this round came in. I stopped Play before editing scripts, as instructed.

Decisions:
- The ghost shows the prefab's resting sprite, unanimated. Copying the fireball's Animator could fire its animation events on an object without the projectile script and log errors.
- `SynergyLanePresenter`, its file and the menu name are unchanged. Renaming would mean moving the script with its `.meta` to keep the scene reference. Easy to do later if the name matters.

What THJ should look at (same setup as "How to see it"):
1. With John's shield up, aim Lucy's fireball at him. Four faint fireballs ring John, each pointing along its diagonal toward the cell its copy will hit, where the sword markers and damage bars already show. There are no lines.
2. A blocked diagonal shows no ghost on that side. Fire and check that each copy leaves the way its ghost pointed.
3. Read and feel: alpha, size, ring size, lift and bob are tunable live on the `SynergyLanePresenter` object in the combat container scene, during Play. Note the values you like; changes made in Play mode don't persist.
4. Clearing is unchanged: cancel, another ability, end turn and level end all remove the ghosts.

Commit: the same single commit as before, with `GhostProjectileRules.cs` + `.meta` added to the file list.

## Round 3: ghosts sort with John

**Why WorldUI made them nearly invisible:** the fireball's material is URP 2D `Sprite-Lit-Default`, and the combat scene's Global Light 2D lights only Default, DynamicTop and Overlay. A lit sprite on WorldUI gets no light and draws close to black, which at 50% alpha almost disappears. OverObjects probably shows because a level light covers it; I didn't check.

**How units sort here:** there is no SortingGroup. A unit's `Body` is on the **Default** layer with order 1. `GridPluggableEntity.Plug` adds `10 × the cell's vertical layer index` to every visual's order, so raised cells get higher orders. Within one layer and order, the 2D renderer sorts along a custom transparency axis Y (`Renderer2D.asset`), so lower on screen draws in front. The shield visual is on DynamicTop at order 99, above everything.

What changed:
- Each ghost now takes the sorting layer of the launching unit's `GUnit.BodyVisual`, which is John's `Body`, and an order of the body's order ± `depthOrderOffset`. This is read every frame, so it follows John when his order changes with cell height. If there is no body, the ghost keeps the projectile's own layer and order. On Default the ghosts are lit like John.
- Pure rule `GhostProjectileRules.DrawsInFront(direction)`: a direction pointing up the screen (the far side) goes behind John; down (the near side) and pure sideways go in front. `SortingOrder(unitOrder, direction, offset)` applies it, with an offset of at least 1.
- Inspector: `sortingLayerName` and `sortingOrder` are replaced by `depthOrderOffset` (default 1). The other ghost fields are unchanged. The scene YAML wasn't touched; a stale serialized value for a removed field is just dropped on the next save.
- Tests: 2 new (17 in all). One checks in-front or behind for all 8 directions, the other the order offsets, including a raised-cell order and the minimum offset.
- Verified: EditMode 1833 run, 1832 pass; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The compile shows no errors and no warnings from these files.
- The editor was not in Play mode when I checked, so I didn't stop anything this round. That check came after I had written the script edits; the recompile ran with Play off.

What THJ should look at:
1. Shield up, aim Lucy's fireball at John. The two upper ghosts draw behind John's body and the two lower ones in front, with the same lighting as John.
2. On a raised cell, if a level has one, they still sort right around him.
3. With John's sprite in front, the upper ghosts may be mostly covered by him. If so, a larger `ringRadiusCells` or `anchorLiftCells` (tunable live) pushes them out. If the straight Flare pattern is ever used, the left and right ghosts draw in front.

Commit: unchanged, the same single commit and file list.

## Round 4: all ghosts over John

- THJ's call: every ghost now draws at John's body order + `depthOrderOffset`, on his body's layer, lit like him and following his order every frame.
- The far-side-behind rule only applies behind the new inspector toggle `drawFarSideBehind`, which is off by default. `DrawsInFront` and its tests are kept.
- `GhostProjectileRules.SortingOrder` takes a `farSideBehind` flag.
- Tests: 18 in all. A new one checks the default: all 8 directions in front, including from a raised-cell order. The far-side test now runs with the toggle on.
- Verified: EditMode 1834 run, 1833 pass; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The compile shows no errors.
- The editor was in Play mode, so I stopped it before editing scripts.
- Caveat: John's Family Role shield visual (`FRShield/Visual`) is on the DynamicTop layer at order 99, so it still draws over the ghosts. The Shield Up pose is part of his body sprite, so the ghosts now draw over it.
- To see it: shield up, aim at John; all four ghosts, including the top-right one, draw over John.
