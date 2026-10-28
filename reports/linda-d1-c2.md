# Report: Linda at a distance, D1-C2: Far readability

Plan: plans/2026-10-28-linda-distance-d1-tech.md (chunk D1-C2; design D1.1 "What the player sees")    Agent: miso-implementer    Branch: thj/linda-quiver (on top of D1-C1, uncommitted)
Outcome: done. Compiled offline; the Unity Test Runner and the play check are for THJ.

No core-system code changed. Core doesn't import Linda: the box is drawn by a Linda-side view, and the badge-tooltip line sits in the unit panel (`Features/UI/Panels`, not on the core list), which already reads `LindaQuiver`.

## What changed

All new scripts are in `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/` unless another path is given, and each has a .meta.

**New**
- `FarDisplayRules.cs`: pure rules for what is shown.
  - The mark state (none / Far / Far locked).
  - The ghost-tile mark.
  - The other-unit move cue (none / Far lost / Far gained).
  - When the box shows, and which cells it covers.
  - The text: factor formatting with an invariant dot, the prompt suffix in fancy and plain forms, the whole prompt line, the tooltip line, and "Far lost".
  - Every string is `[PLACEHOLDER]`-tagged. Factors and the radius are always passed in from the tuning asset.
- `FarTextGlyphs.cs`: whether a TMP font (with its fallbacks) has `·` (U+00B7) and `×` (U+00D7).
- `LindaFarMarkView.cs`: the mark by the pips.
  - An eye ring around a tilted arrow, in Linda's role colour (from her role handler).
  - A lock pip while the state is locked.
  - The strike-through and "Far lost" label for the move cue.
  - It also builds the mark for the ghost tile.
  - Drawn on the pips' layer and order (`DynamicTop` −1, below HP bars). Its objects are Linda's children, built once she stands on a cell. State changes are applied only when they change.
- `LindaFarPreviewPresenter.cs`: polls the player controller each frame, like the "+N arrows" preview.
  - Same conditions: player's turn, `TargetSelection`, a move ability, path from `IMovePreviewPathSource`, path end = hovered cell.
  - For Linda's own move: the ghost-tile mark via `LindaFarState.EvaluateAt(destination)`.
  - For another squad unit's move: `FarDisplayRules.OtherMoveCue` from `Reading.Far` and `EvaluateWithMove(mover, destination)`, passed to the mark view.
- `LindaFarBoxView.cs`: the box while Linda's badge is hovered (`onFamilyRoleBadgeHover`) or Shift is held (`toggleShowStats`).
  - A faint tint on each existing tile within the radius, her footprint left out.
  - On `Default` at order −9: above the tile base (−11) and the role-zone icons (−10), below the units.
  - Pooled tiles under Linda; their world positions are put back each frame, so the box doesn't slide while she walks.
- `LindaQuiver.FarViews.cs`: implements `LindaQuiver.AddFarViews()` (declared in C1) and adds the three views.
- `Features/UI/Panels/Scripts/UnitPanelUI.FarWatch.cs`: `FarWatchTooltipLine(unit)`.
  - Linda's Far line from her tuning asset; empty for anyone else or with Far Watch off.
  - Checks the tooltip's TMP labels for the glyphs once per panel and uses `x` if any label lacks them.
- `Editor/FarDisplayRulesTests.cs`: 39 cases.
- `Editor/FarDisplayWiringTests.cs`: the tooltip from the asset, and the default font has the glyphs.

**Modified**
- `QuiverPromptLabel.cs`:
  - Refreshes the Far state, then shows `Arrows N > N−1 · Far 7.5×` / `· 5×` (plain `- Far 7.5x` if the label's font lacks the glyphs).
  - With Far Watch off it is the old `Arrows N > N−1`.
  - Rect width 3 → 5 cells for the longer line (no wrap, left pivot, so nothing else moves).
- `QuiverPipsView.cs`: four constants (sorting layer and order, pip spacing, below-feet offset) from `private` to `internal`, so the mark sits on the same layer and next to the row.
- `Features/UI/Panels/Scripts/UnitPanelUI.cs`: the badge hover appends `FarWatchTooltipLine(unit)` to the tooltip text (one line).

## Glyph check

- **World labels** (the prompt) use TMP's default `LiberationSans SDF` (static atlas). It has `·` and `×`, but not `→`, which is why the prompt keeps `>`. `FarDisplayWiringTests.DefaultFont_HasTheFarGlyphs` covers it.
- **The unit panel prefab** uses `LiberationSans SDF` and Fairfax SDF. Fairfax, Pixelify and alagard have neither glyph. The tooltip line checks its own labels at run time: if any lacks them, it says `5x` / `7.5x`.
- **The prompt** checks its label's font the same way.

## Strings (from `reports/linda-d1-fetch-lines.md`, tooltip wording per D-291)

- Tooltip: `[PLACEHOLDER] Watch: {near}×. Far (no squad member within {radius} at End Turn): {far}×.`
- Prompt suffix: `[PLACEHOLDER] … · Far {far}×` / `… · {near}×`. The tag is on the whole line, which `QuiverTextRules.WatchPrompt` starts.
- `[PLACEHOLDER] Far lost`.
- "Far" gained shows the mark only. The design says "(the mark)", and narrative's optional "Far" label is not added.

## Acceptance criteria (C2's share)

- [x] **The Far mark over Linda next to the pips; nothing when near; lock pip in the enemy phase.** Rules in `FarDisplayRulesTests.Mark`; view needs play (steps 11–12).
- [x] **The ghost-tile mark** when that tile would be Far, with the others where they stand. Covered by `GhostMark_*` and `GhostTile_MatchesTheRuleForThatPosition`; it uses the same rule as End Turn (`FarWatchRules.Evaluate` via `LindaFarState`). Play step 13.
- [x] **"Far lost" (struck mark) / the mark** on another unit's move preview. Covered by `OtherMoveCue`. Play steps 14–15.
- [x] **The 2-cell box on badge hover or Shift.** Covered by `ShowBox`, `BoxCells_*`. Play step 16.
- [x] **Prompt `Arrows 3 > 2 · Far 7.5×` / `· 5×`**, factor from the asset, glyph fallback. Covered by `PromptSuffix_*`, `WatchPrompt_*`, `DefaultFont_HasTheFarGlyphs`. Play step 17.
- [x] **Tooltip line** with numbers from the asset and the D-291 wording. Covered by `TooltipLine_*`, `TooltipLine_FromTheAsset`. Play step 18.
- [x] **Everything behind the Far toggle.** Rules take `enabled`; covered by the `_Off_` tests. Play step 19.
- [x] **No core change; D-281** (`QuiverLevelAccess` for the squad and the turn) and **D-282** (every object is Linda's child, nothing at the root).
- [x] **No per-frame allocations:** the per-unit spawned cache (C1 tweak) and text set only on change. Play step 22 (Profiler).
- [ ] **Run in Unity:** THJ.
  - Offline compile with the editor's own Roslyn and `.rsp` files: C1 + C2, game and editor assemblies, 0 errors and no warnings in these files.
  - The pure tests run outside Unity (real test code, Unity's NUnit): rules 29, lock 12, display 39, 80 of 80 pass.
  - The wiring tests need the Test Runner.

**Tests for THJ:** Test Runner > EditMode > Run All (known red only). Quick filter: `MISO.Core.Features.Bergsons.EditorTests`.

**Play steps:** `playtests/2026-10-28-linda-d1-far-play-check.md`. It has 22 steps covering C1 and C2, including the reviewer's turn-1 check (step 6) and the damage numbers near, Far and off.

## Save reset

No.

## Decisions I made

- **The box tints each tile instead of outlining the 5×5.** The design says "outlined, faint ... only the tiles that must stay clear". Tiles are exact on any grid spacing and show precisely which tiles count. The tint is easy to swap for an outline if THJ prefers.
- **The mark's position:** to the right of the pip row at the pips' height. The lock pip is a small white square at the mark's lower right, and the strike is a red diagonal bar.
- **The ghost mark and the move cue cover move abilities only.** The condition is the one the "+N arrows" preview uses (`DefaultEmptyGridCellAction`). An attack's auto-approach ghost and Duo moves get no Far cue.
- **"Far gained" shows the mark without text,** as in the design table.
- **The prompt label is 5 cells wide** (was 3) for the longer line.
- **The C2 views are wired through a partial method in `LindaQuiver`,** so C1 can be committed and compiled alone.

## Needs THJ

None. If the tooltip shows `x` (Fairfax in the panel), THJ may want the panel font to gain `×` rather than the plain form.

## Docs to update

- `tech/combat-architecture.md` (coordinator): Far readability views on Linda; badge tooltip line in `UnitPanelUI.FarWatch.cs`; `FarTextGlyphs` fallback.
- Glossary "Far" (narrative): the proposed row in `linda-d1-fetch-lines.md` §7.

## Risks and loose ends

- **Placeholder art.** The eye-and-arrow mark is drawn from the quiver's procedural sprites.
- **Overlap.** The "Far lost" label sits beside the mark at her feet and may overlap the "+N" return cue or a damage number; check in play.
- **The move cue needs the hovered cell to be the end of the preview path** (as for "+N arrows"), so it doesn't show while the cursor is off the grid.
- **No Far mark hover tooltip.** Narrative's optional "Far: no squad member within 2." / "Far until your next turn." isn't built.
- **No Far lock barks.** The optional "Room to breathe." lines aren't built.
- **The box ignores other units' zones and covers.** It is a tint on Default −9; check readability against John's cover icons.

## Proposed commits

After C1's commit (see `linda-d1-c1.md`, "Proposed commits (C1, final)"):

2. `feat(linda): show Far Watch on the board, the prompt and the role tooltip`. Files, with their .meta:
   - `Features/Player/Linda/Scripts/Quiver/`:
     - new: `FarDisplayRules.cs`, `FarTextGlyphs.cs`, `LindaFarMarkView.cs`, `LindaFarPreviewPresenter.cs`, `LindaFarBoxView.cs`, `LindaQuiver.FarViews.cs`;
     - modified: `QuiverPromptLabel.cs`, `QuiverPipsView.cs`;
     - tests: `Editor/FarDisplayRulesTests.cs`, `Editor/FarDisplayWiringTests.cs`.
   - `Features/UI/Panels/Scripts/`: new `UnitPanelUI.FarWatch.cs`; modified `UnitPanelUI.cs`.

   Kind: plain (UI only; it changes no rule). Per THJ's rule, commit both after the play check.

## Other branches

`main` and `thj/home-test` get this when the quiver goes there.

## How to see it

Follow `playtests/2026-10-28-linda-d1-far-play-check.md`, steps 11–22 (readability). Steps 1–10 are C1's damage numbers.

## Review should-fixes (after APPROVE)

- **"Far lost" label sorting:** the label now uses the pips' sorting layer and order (`QuiverPipsView.SortingLayer`, `DynamicTop` −1), so HP bars stay on top (D-280). The `WorldUI` 61 constants are gone.
- **Downed Linda:** the mark view and the box view count Linda as alive only when `IsAlive && !IsDowned`, as `LindaFarState` does, so a downed Linda shows no mark, cue or box.
- **Formatting:** the header comment of `QuiverPromptLabel.cs` is re-wrapped to the 120-column style. The `ShowTooltip` call in `UnitPanelUI.cs` now breaks after the title argument with a normal continuation indent. The box view's `ShowBox` call is also wrapped, via a local `alive`.
- **Re-check:** offline compile, C1 alone (HEAD copies of the C2-touched files) and C1 + C2: 0 errors. All edited files are LF. These fixes touch only C2 files.
