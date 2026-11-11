# Report: Synergy aim preview, chunk C3 (Catch & Return preview)

Plan: plans/onboarding/2026-11-10-synergy-aim-preview-tech.md (section "C2 / C3 revised", D-494)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check pending). No core edits were needed.

## Step 1: investigation

**The Fire Embers second colour needs no core change.** It is the stepped HP bar of multi-target picking:
- Core `GUnit.ShowDamagePreview(total, confirmed, DamagePreviewPick pick)` is public. It is the overload `PlayerController.ShowSplitDamagePreview` calls for Lucy's multi-pick.
- With `pick != Single`, the non-core `EntityInfoPanelUI.ShowHealthMode` draws `confirmed` in the normal decrease colour and `total - confirmed` in `UI_Element_FillBar.secondaryDecreaseColor` (pink, `0.97, 0.55, 0.58`, set on `UI_Element_FillBar.prefab`).
- The lethal skull: with `FinalPick`, it is white when `confirmed` alone kills, and in the second colour when only `total` kills (`DamagePreviewRules.DecideLethalMark`).
- The presenter calls `ShowDamagePreview(shot + return, shot, FinalPick)`. Only the existing public overload is called; nothing in core changes.

**The real catch and return** (`ProjectileCatchAndReturn`, Mark's prefab):
- Gates, in order:
  1. no catch in progress, a QTE profile is set and no QTE is running;
  2. the arrow is alive, not Mark's own, and its `PrefabSource` is whitelisted (`LindaAttackArrow` only, so the Duo fire arrow is never caught);
  3. the shooter is an ally on a cell;
  4. the `_MarkLindaSynergy` unlock is open (it is `unlockedByDefault: 1`);
  5. the footprint distance is at least 2 (Adjacent);
  6. `IsOnIncomingPath` passes, with the arrow's `DirectionNormal`.
- Mark's `returnMode` is BounceBack (1): the arrow comes back with no refund.
- The return copy is `LindaAttackArrowReturn`. It is the same arrow and the same effect with the same 0.9 per-hit falloff, but `travelEntireRadius` 0 and destination Occupant.
  - Its flight: from the catch point (`CatchPointRules.FreezePoint` on Linda's flight at Mark's `returnSource`) to Linda's `TargetPoint`, in a straight line.
  - What it hits: every unit its effect targets along the way, so **the enemies between Linda and Mark are hit a second time**. Linda is skipped (owner) and Mark is an ally. Its hit count starts at 0 (a new instance), so the first enemy from Mark takes full damage, then ×0.9, ×0.81 and so on.
  - Reach: it stops on Linda and never goes past her.
- **On a successful catch the original arrow doesn't fly on** (it is frozen, hidden and disposed). On a failed or declined QTE it flies on with its remaining range.

**Bloom together with Catch, as the real shot does it:**
- **Cyclone before Mark:** the arrow splits at the Cyclone and is disposed. Copies have no `PrefabSource` and no `CatchSweep`, so no catch.
- **Mark before a Cyclone:** catch prompt. On success the arrow returns and there is no Bloom. On failure the arrow flies on and blooms.
- The preview matches this:
  - Cyclone first: Bloom only (the catch walk stops at a splitting Cyclone).
  - Mark first: both show. The Bloom preview stands for the failed-prompt case, in normal colours, as the shot's own preview does. The Catch preview is the success case, in the second colour. On units both touch, the return damage goes on top of the Bloom value.

**Core check:**
- Read only: `GUnit.ShowDamagePreview`, `ShowInfoPanel`, `BodyVisual`, `SpawnSource`, `TargetPoint`, `GridPluggableEntity.GetFootprintDistanceTo`, `AbilityDamagePreview.ComputeFor`/`SimulateApply`, `PlayerController.IsLegalAbilityTarget`/`TargetCellCount`, `Projectile` public getters.
- Edited: `ProjectileCatchAndReturn.cs` (Mark feature folder, not core), plus the non-core presenter.

## What changed

Paths under `miso/Assets/_Project/`. All files are LF with no BOM, like their neighbours.

- `Features/Player/Mark/Scripts/CatchAndReturnRules.cs` (new, + `.meta`): pure rules. It holds:
  - `PassesGates` (ally, unlock, distance, on the incoming path);
  - `IsOnIncomingPath`, moved here;
  - `FlightDirectionNormal` (the projectile's own per-axis rounding of its normalised flight);
  - `ReturnFlightStart` (the point of the shot's flight nearest Mark's hand, then `CatchPointRules.FreezePoint`).
- `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (behaviour-preserving refactor):
  - `TryCatch` keeps its early checks and the one-chance `_lastSeen` slot exactly as they were. The trailing owner / ally / unlock / distance / path block is now `PassesCatchGates`, which feeds `CatchAndReturnRules.PassesGates`. Same result. The checks were all read-only, so evaluating them together instead of short-circuiting changes nothing.
  - `IsOnIncomingPath` (public static) now forwards to the rules.
  - New read-only members for the preview: `Catcher`, `ReturnsArrow`, `ReturnSourcePosition`, `ReturnPrefabFor(caught)`, and `WouldCatch(prefab, owner, direction)`. `WouldCatch` runs the same checks without the ones about a catch already in progress.
  - `ReturnDestination` went from private to public static.
- `Features/Player/Shared/Synergies/SynergyLanePresenter.Catch.cs` (new, + `.meta`): the preview. It turns on when all of these hold:
  - the player is aiming in their own turn, and the hovered cell is legal;
  - the next click fires a projectile, and the aim is a straight lane;
  - walking the lane to the arrow's flight end, a unit with `ProjectileCatchAndReturn` whose `WouldCatch` passes comes before any Cyclone that would split the arrow;
  - the catch bounces the arrow back.

  When on:
  - **Ghost arrows:** 2 pooled SpriteRenderers with the return arrow prefab's sprite and material, tinted Mark's colour, at `ghostAlpha`. They run from the catch point to Linda's body at 1.5 cells/s, evenly spaced, fade in and out over the first and last 20%, and loop. They are rotated along the flight and sorted on Mark's body layer at his order + `depthOrderOffset`.
  - **HP:** the return's hits are worked out with the Bloom's physics sampling (`CollectContacts`, the return arrow's own collider and layer mask), the same hit filter (`CollectHits`: owner skipped, only targeted units count toward the falloff; Mark is skipped too), `Falloff` and the shared `HitDamage` (no new copy of the core math). Every frame after the Bloom, each hit unit gets `ShowDamagePreview(shot + return, shot, FinalPick)`. "shot" is the Bloom's value when the Bloom is on, otherwise the normal `ComputeFor` value.
  - **Give-back:** `ClearCatch` runs on the `hovered == false` pass (like the Bloom), from `LateUpdate` when the aim stops leading to a catch (cancel, ability switch, end turn, level end), and in `OnDisable`/`OnDestroy`. It hides the ghosts and gives back each bar. While the same aim is still up (same ability, same hovered cell, no Bloom), the bar goes back to the shot's own value. Otherwise it is hidden, and the controller redraws its own on the next hover.
  - New inspector fields under "Catch & Return": `catchGhostColor`, `catchGhostCount` (2), `catchGhostCellsPerSecond` (1.5), `catchGhostFade` (0.2), `catchHeadAxis` (Right). The scene YAML wasn't touched; the code defaults apply until the scene is next saved.
  - No statics, so no play-mode reset is needed.
- `Features/Player/Shared/Synergies/CatchReturnPreviewRules.cs` (new, + `.meta`): pure rules. `FindCatchStep` (catch before split; a catcher that fails its checks lets the arrow fly on), `BarFor` (total and confirmed), `TryGhostOnFlight` (looping, spaced, faded positions).
- `Features/Player/Shared/Synergies/SynergyLanePresenter.cs`: the hover-out pass, `OnDisable` and `OnDestroy` also call `ClearCatch()`; header comment updated.
- `Features/Player/Shared/Synergies/SynergyLanePresenter.Bloom.cs`: `LateUpdate` also calls `RefreshCatch`, `ApplyCatchDamage` and `DrawCatchGhosts`, after the Bloom.
- Tests (new, + `.meta`):
  - `Features/Player/Mark/Scripts/Editor/CatchAndReturnRulesTests.cs` (9 tests), including an equivalence test of `PassesGates` against the old inline checks over a 6×6 board × 6 directions × 4 distances × all ally/unlock combinations;
  - `Features/Player/Shared/Synergies/Editor/CatchReturnPreviewTests.cs` (11 tests), including a data test that fails if the caught arrow stops flying its full reach or aiming at the cell anchor, or if the return stops being a straight flight that hits on contact.

No scene, prefab or asset edits.

## Acceptance criteria

- [x] **The preview appears only when the real catch could trigger.** The gates are `WouldCatch`, the same `PassesCatchGates` the real `TryCatch` uses, plus the same whitelist and QTE-profile checks. Also required: the arrow reaches Mark (within its flight, with no splitting Cyclone first) and the catch bounces. *Tests:* gate equivalence with the old code, distance/lock/ally/path cases, `FindCatchStep` (Cyclone before or after Mark, out of reach, failing catcher). *Play check:* Mark next to Linda (distance 1) shows nothing; Mark two or more tiles away on the lane shows it; Mark off the lane shows nothing.
- [x] **Ghost arrows run Mark → along the real return lane.** The start is the shared `ReturnFlightStart` (the real `FreezePoint` rule), the end is the real `ReturnDestination` (Linda's body). *Tests:* return start for horizontal and vertical shots, ghost looping, spacing and fade. *Play check:* the look.
- [x] **Return-hit HP previews show in the second colour on the enemies the return would hit, and nothing on Mark or Linda.** The colour is the stepped bar with `FinalPick`. The hit filter skips Linda (the owner, as the real arrow does), skips Mark, and keeps only units the effect targets. *Tests:* `BarFor`. *Play check:* enemies between Linda and Mark show their normal bar segment plus a pink segment, and a kill that needs the return shows a pink skull.
- [x] **Everything clears on cancel, ability switch, end turn and level end.** Same mechanism as the Bloom: hover-out give-back plus `LateUpdate` polling (the aimed ability is null outside the player's target selection, or the level has ended). *Play check* for each case.
- [x] **Bloom still works.** The Bloom code is unchanged apart from the three added calls at the end of `LateUpdate`. Its 19 tests pass. *Play check:* Memory 4.
- [x] **No core edits.** Core is only called.
- [x] **Console clean:** no errors after the recompile, only the existing CS0108/CS8509/CS0168 warnings.
- [x] **EditMode:** 1874 run, 1873 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The Bergsons group alone: 414/414.

## Save reset

No.

## Decisions I made

- **Tier 1: Mark's colour.** The project's only per-character colour is the Family Role colour (`FactionRoleHandlerBase.RoleZoneColor`). Mark's code default is green `(0, 0.62, 0.451)`, but `Unit_Mark.prefab` overrides it with a near-black brown `(0.094, 0.044, 0.013, 0.75)`, which would make a faint, lit arrow almost invisible. So, as the brief allows, it is an inspector colour, `catchGhostColor`, defaulting to the code green. THJ may want a different green.
- **Tier 1: no >>> on the return lane.** The return runs back over Linda's own glowing lane, and a chevron pointing back at her would fight with her >>>. The moving ghosts already show the direction. Easy to add (one chevron on the tile in front of Mark) if THJ wants it.
- **Tier 1: the return damage sits on top of the shot's own damage.** With the Bloom on, that is the Bloom value; otherwise the normal preview. The shot's own segment keeps the normal colour, so "before the catch" stays as it was.
- **Tier 1: `FinalPick` rather than `Picking`.** It gives the second-colour skull when only the return kills. With `Picking` no skull would show for that case.
- **Tier 1: the shot's flight is read on the grid plus the bow.** From Linda's `SpawnSource` to her lane end's anchor, rounded per axis the way the projectile does. A data test pins the arrow settings this relies on.
- **Tier 1: kept `ProjectileCatchAndReturn.IsOnIncomingPath`** as a forwarder, so its public API stays the same.
- **Tier 1: Mark is skipped in the return-hit filter** on top of the real ally filter, so he never shows a bar even if the effect's targets change.

## Needs THJ

None blocking. Look-and-feel calls are listed under "How to see it": the colour, the ghost count and speed, and whether to add the one >>>.

## Docs to update

- `tech/combat-architecture.md` (coordinator): the Catch gates live in `CatchAndReturnRules` (shared by `ProjectileCatchAndReturn` and the preview); the preview is `SynergyLanePresenter.Catch.cs`; the return damage uses the stepped HP bar (`ShowDamagePreview(total, confirmed, FinalPick)`).
- GDD `combat-rules.md` / `family-systems.md` (designer): the preview rule for Catch (success case in the second colour; with a Bloom past Mark, both show).

## Risks and loose ends

- **The physical catch is assumed.** The preview assumes the arrow touches Mark whenever he stands on the lane within its flight, which the trigger plus `CatchSweep` should guarantee. Not play-confirmed for an arrow that leans past a raised cell.
- **The second colour is shared with multi-pick.** That is by design (THJ's reference), but if Lucy's multi-pick and a catch ever show on the same unit, they would look alike. That can't happen on one aim.
- **Same-hover toggles:** if the catch turns off while the cursor stays on one cell with the Bloom on, the bar is hidden for one frame and the Bloom re-applies it. Harmless.
- **Damage math duplication** (from C2) still applies. `HitDamage` mirrors core `AbilityDamagePreview.AddDamage`. C3 reuses it and adds no new copy.
- **The return's falloff over targets only:** the real return counts only targeted units toward its falloff (`ProjectileHitLedger`), and so does the preview. The core bow preview's known over-count (C2 note) doesn't affect the return.
- **`_catchers` cache** keeps one entry per unit hovered over during the level (a few units). It is dropped with the presenter. Not static.
- Not covered: auto-move shots (the bow has none), and the Duo fire arrow (not on Mark's whitelist, so it can't be caught).

## Proposed commits

1. `refactor(combat): Mark's Catch & Return checks move into shared pure rules, with tests` (plain; behaviour-preserving)
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/CatchAndReturnRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchAndReturnRulesTests.cs` + `.meta`
2. `feat(combat): aiming Linda's bow at a lane where Mark would catch the arrow shows ghost arrows flying back from him and the return's damage in the second preview colour` (plain; depends on 1)
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.Catch.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/CatchReturnPreviewRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.cs`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.Bloom.cs`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/Editor/CatchReturnPreviewTests.cs` + `.meta`

Commit 1 adds the preview getters and `WouldCatch` to `ProjectileCatchAndReturn` as well. They are additive and unused until commit 2, so commit 1 still builds and behaves the same.

Leave out THJ's uncommitted files: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` and the TMP fallback font.

## Other branches

`main`, when this branch merges.

## How to see it

Catch & Return is unlocked by default (`MarkLindaSynergy`). Two places to check:
- **MS2 - The Ridge** (`GB_s2-ridge`): the roster is fixed to Linda and Mark.
- **Memory 4** (`GB_m4-mark`): Linda, Lucy and Mark, with Tempest Bloom granted at level start. Use it for the Bloom + Catch case.

1. Press Play in one of those levels. Move Mark so he stands in one of Linda's straight lanes, **at least 2 tiles** from her, ideally with an enemy between them and one past Mark.
2. Select Linda and her bow, and hover a cell in Mark's lane:
   - her lane glow and >>> are as usual;
   - two faint green arrows fly from Mark back to Linda, again and again, fading in at Mark and out at Linda;
   - the enemy between them shows its normal bar segment plus a **pink** segment (the return hit). If the return would kill it, the skull is pink. If the shot alone kills, the skull is white;
   - the enemy past Mark keeps its normal bar (what happens if the prompt fails);
   - Mark and Linda show no bar.
3. Fire and win the prompt: the arrow returns along the ghosts' path, and the damage matches the pink segment. Fire again and fail it: the arrow flies on, matching the normal bars.
4. Gates: with Mark right next to Linda, off her lane, or past the arrow's reach, nothing shows.
5. Bloom together (Memory 4):
   - Lucy's Cyclone in the lane **past** Mark: both previews show. The Bloom lanes and copies are the failed-prompt case; the ghosts and pink segments are the catch.
   - Cyclone **before** Mark: Bloom only, with no ghosts.
   - Lanes without Mark: the Bloom alone, unchanged.
6. Clearing: with the preview up, (a) cancel, (b) pick another ability, (c) end the turn, (d) end the level with the aim up if you can. No ghosts and no pink segments are left, and moving to another lane restores the normal bars.
7. Tuning, live in Play on the `SynergyLanePresenter` object (combat container scene): `catchGhostColor`, `catchGhostCount`, `catchGhostCellsPerSecond`, `catchGhostFade` and the shared `ghostAlpha`/`ghostScale`. Note the values you like; changes made in Play don't persist. Say whether you want the single >>> at the return lane's start.
8. Console: no new errors or warnings.

## Round 2: review fixes

The review (`reports/synergy-preview-c3-review.md`) gave FIX, with one must-fix and one should-fix.

**M1: each bar drawn once per frame, in one look.**
- `SynergyLanePresenter.Bloom.cs` `LateUpdate` now runs in this order:
  1. `RefreshBloom`;
  2. `RefreshCatch`;
  3. `ApplyBloomDamage`;
  4. `ApplyCatchDamage`;
  5. `DrawCatchGhosts`.
- While the catch preview is on, `ApplyBloomDamage` skips every unit in `_catchReturn`. That covers both its re-shown bars and its muted (hidden) ones.
- A unit the return hits now gets only the catch's `FinalPick` bar each frame. Its pink segment's `ImageAlphaPulse` and the lethal mark no longer restart every frame, and no coroutine is allocated per frame.
- It also removes the one-frame hide when the catch turns off on the same hover with the Bloom on: `ClearCatch` hides the bar and `ApplyBloomDamage` re-shows it in the same frame.

Audit of every per-frame bar draw:

| State | Per frame | Changes only when the shot changes |
| --- | --- | --- |
| Bloom alone | Single on its units; hide on its muted units (unchanged) | — |
| Catch alone | `FinalPick` on the return's units | — |
| Both | Bloom only on units the return doesn't hit, catch only on its own (the sets are disjoint) | — |
| Any | — | The recompute hides (`ComputeBloomDamage`, `ComputeCatchDamage`), the give-back in `ClearBloom`/`ClearCatch`, and the controller's Single redraw on each hover: one look change per hover, not per frame |

**S1:** `SynergyLanePresenter.Catch.cs` reads Mark's cell with an explicit Unity-null check (`catchCell ? catchCell.OccupantEntity as GUnit : null`) instead of `?.`.

**Verified:**
- Compile: no errors from these files. The only console error is the known `Objects are trying to be loaded during a domain backup`, from earlier rounds.
- EditMode: 1874 run, 1873 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- The editor was not in Play mode, so I stopped nothing.
- LF, no BOM.

**Files:** the same as round 1. Only `SynergyLanePresenter.Bloom.cs` and `SynergyLanePresenter.Catch.cs` changed again. Commits unchanged.

**Play-check addition:** in Memory 4, with Mark before a Cyclone, the pink return segment on the enemy between Linda and Mark pulses normally (not stuck faint), and a skull that needs the return stays steady.

## Round 3: one return chevron instead of ghost arrows

THJ's play check: the catch preview should match the Bloom's copy lanes. The ghost arrows are removed, and one >>> marks the return lane's start.

**What changed:**

- **The return chevron.** `SynergyLanePresenter.Catch.cs` draws one chevron with `GridCell.SetAimDirectionPreview`, the same call and the same overlay-cell keying as the Bloom copy-lane chevrons.
  - Where: on the tile next to Mark toward Linda, pointing at her. The pure rule is `CatchReturnPreviewRules.TryGetReturnChevronTile`.
  - When there is none: Mark and Linda aren't on one straight line, the tile is Linda's own (they are adjacent), or the tile doesn't exist. The presenter also refuses any cell Linda occupies, and the shooter's own cell, where her >>> sits.
- **Give-back, as for the Bloom chevrons.** The chevron is moved or cleared in `ApplyCatchChevron`.
  - `ClearCatch` clears it. That covers hover-out, and cancel, ability switch, end turn and level end through `LateUpdate`, plus `OnDisable`/`OnDestroy`.
  - **Kept apart from the Bloom:** the catch never clears a cell that is in `_bloomChevrons`, and the Bloom's `ApplyChevrons` never clears `_catchChevronCell`. Neither ever touches Linda's own cell. Geometrically the two sets are disjoint anyway: the return chevron is before Mark, and the copy chevrons are past the Cyclone, which is past Mark.
- **Removed:**
  - the ghost arrows: `DrawCatchGhosts`, the pool, `CreateCatchGhost`, `HideCatchGhosts`;
  - the inspector fields `catchGhostColor`, `catchGhostCount`, `catchGhostCellsPerSecond`, `catchGhostFade`, `catchHeadAxis`. The scene never saved them, so no data is lost;
  - `CatchReturnPreviewRules.TryGhostOnFlight` and its 3 tests.

  The Flare ghosts and `GhostProjectileRules` are untouched.
- **Kept:** the pink return HP preview, unchanged. `ReturnFlightStart`/`ReturnDestination` are still used, now only for the return's hit sampling.
- **No tint on the chevron.** `GridCell` has no public way to tint or fade it. `SetAimDirectionPreview(bool, Vector2)` only switches it on and turns it, and `aimDirectionPreviewVisual` is private. The only way would be to find the core-owned `AimDirectionPreview` child by name and recolour its renderers (and restore them, since the same visual serves Linda's own >>>). That reaches into core internals, so the chevron uses the normal look. A faint, Mark-coloured chevron needs a small additive core API, for example `GridCell.SetAimDirectionPreview(bool, Vector2, Color tint)` (Tier 3). Ask THJ if he wants it.

**Tests:** 3 new in `CatchReturnPreviewTests`:
- the chevron sits next to Mark, pointing at Linda (horizontal and vertical lanes);
- none on Linda's tile or a missing one;
- none off a straight line.

That makes 11 in the file.

**Verified:**
- Compile: no errors, and no warnings from these files.
- EditMode: 1874 run, 1873 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- The editor was not in Play mode, so I stopped nothing.
- LF, no BOM.

**Files:** the same list as before. This round changed `SynergyLanePresenter.Catch.cs`, `SynergyLanePresenter.Bloom.cs` (`LateUpdate`, plus the guard on the catch chevron), `SynergyLanePresenter.cs` (comments), `CatchReturnPreviewRules.cs` and `CatchReturnPreviewTests.cs`. The commits are unchanged. Commit 2's message should now say: `feat(combat): aiming Linda's bow at a lane where Mark would catch the arrow marks the return lane and shows the return's damage in the second preview colour`.

**How to see it (replaces the ghost steps above):**
1. Mark is in Linda's lane, 2 or more tiles away. Hover the lane: one >>> sits on the tile next to Mark on Linda's side, pointing back at her. Her own >>> is unchanged, and the pink segments are as before.
2. Mark 2 tiles away: the chevron sits on the tile between them. Mark adjacent: no catch, no chevron.
3. Memory 4, Cyclone past Mark: the return >>> and one >>> per Bloom copy lane show together. Move off the lane: all of them go, and Linda's >>> stays.
4. Cancel, switch ability, end turn: no chevron left behind.

## Round 4: the return >>> on Mark's own tile

THJ's play check of round 3: everything works and the normal chevron look is fine. The >>> should sit on the lane's origin tile, as Linda's own does on hers.

I first checked whether one tile can show several >>> (for the Bloom on the Cyclone tile). It can't: `GridCell.SetAimDirectionPreview` turns one private arrow. THJ chose **no GridCell change**, so this round moves only the Catch chevron.

**What changed:**
- `CatchReturnPreviewRules.TryGetReturnChevronTile(catcher, shooter, out tile, out direction)` now returns the catcher's own tile, pointing one step toward the shooter. It is false when the two aren't on one straight line or share a tile. The cell-exists parameter is gone: Mark's tile always exists.
- `SynergyLanePresenter.Catch.cs` calls the new rule; the presenter's guard against Linda's tile stays. The header comment is updated, and the `ClearCatch` comment is re-wrapped.
- Bloom chevrons are unchanged, on each copy lane's first tile past the Cyclone. `SynergyLanePresenter.Bloom.cs` differs from the committed version only by the three things the Catch needs:
  - the `LateUpdate` order;
  - skipping the return's units in `ApplyBloomDamage`;
  - never clearing `_catchChevronCell` in `ApplyChevrons`.
- Tests: `CatchReturnPreviewTests` replaces the three chevron tests with two:
  - the chevron sits on Mark's own tile, pointing back at Linda, on horizontal and vertical lanes;
  - none off a straight line or on a shared tile.

**Mark's tile and give-back:**
- Mark's tile carries no controller chevron. The controller's >>> is only on Linda's own cell, and the bow uses no approach cell.
- The chevron is keyed by `OverlayCell` (Mark's anchor cell), the same cell `SetAimDirectionPreview` redirects to.
- It is cleared by `ApplyCatchChevron(null, …)` in `ClearCatch`: on hover-out, and on cancel, ability switch, end turn and level end through `LateUpdate`, plus `OnDisable`/`OnDestroy`. It never touches the shooter's cell.
- With Bloom and Catch together, Mark's tile and the Bloom chevron tiles (past the Cyclone, which is past Mark) are always different cells. Each preview's clear also skips the other's cells, so neither clears the other's, and Linda's own >>> is never touched.

**Verified:**
- Compile: no errors, and no warnings from these files.
- EditMode: 1873 run, 1872 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. That is one test fewer than round 3: three chevron tests became two.
- The editor was not in Play mode, so I stopped nothing.
- LF, no BOM. No core edits.

**Files and commits:** unchanged from round 3 (two commits: the extraction, then the preview with the Bloom file). Commit 2's message as given in round 3.

**How to see it (replaces round 3's step 1 and step 2):**
1. Mark is in Linda's lane, 2 or more tiles away. Hover the lane: Mark's own tile shows a >>> at its edge facing Linda, like hers faces her aim. Her >>> and the pink segments are unchanged.
2. Memory 4, Cyclone past Mark: Mark's >>> and one >>> per Bloom copy lane (first tile past the Cyclone) show together. Move off the lane, cancel, switch ability or end the turn: all go, and Linda's >>> stays as the controller draws it.
