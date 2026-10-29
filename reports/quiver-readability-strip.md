# Report: Quiver readability strip

Plan: plans/2026-10-28-quiver-readability-strip.md    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: partial. All the code is written, but it was not compiled or run: the editor is open and the Unity MCP connection failed (ECONNREFUSED), so no compile check, no EditMode run. THJ must focus the editor and run the suite first.

## What changed

New:
- `Features/Player/Linda/Scripts/Quiver/GroundedArrowLook.cs` (+ `.meta`): pure rules for the board arrows: up to 3 arrows per stack, small offsets, stable art variant per arrow, dark tint when locked, sorting (DynamicTop, orders -4 to -2, under the pips at -1 and every HP bar).
- `Features/Player/Linda/Scripts/Quiver/QuiverHudRules.cs` (+ `.meta`): pure layout of the arrows inside the panel quiver, in pixels of the art.

Changed:
- `Scripts/Quiver/GroundedArrowField.cs`: stack views are now up to 3 `SpriteRenderer`s of the new art. TextMeshPro label, badge, outline and orange/red locked colours are gone. The move-preview presenter is no longer added. The icon, tilt and offset constants that only the old view used are gone; `IconSize`, `IconOffset` and the WorldUI constants stay because the hand-back toss and the Encore flight still use them.
- `Scripts/Quiver/QuiverAimPresenter.cs`: the ring and arrow marker is replaced by one faint ghost of the arrow art (no pulse). The Encore lines are now `LineRenderer`s drawn with `ArcLine` (see Decisions).
- `Scripts/Quiver/LindaQuiver.cs`: serialized art (`quiverBodySprite`, `quiverRimSprite`, `arrowSprites`) with `QuiverBodySprite`, `QuiverRimSprite`, `ArrowVariantCount`, `ArrowSprite(variant)`. `RingSprite` and `PixelSprite` removed. `PipSprite` and `GlowSprite` stay (pips under Linda and the "+1" cues).
- `Scripts/Quiver/QuiverSprites.cs`: `Ring()` and `Pixel()` removed.
- `Scripts/Quiver/QuiverTextRules.cs`: `WatchPrompt`, `PromptArrow`, `PreviewLabel` removed. Grey reasons and the badge line stay.
- `Scripts/Quiver/QuiverPipRules.cs`: `PanelLabel` removed.
- `Scripts/Quiver/QuiverPreviewRules.cs`: `QuiverPreviewRules.ArrowsPicked` removed (only the move-preview label used it). `LandingMarkerRules` and `ReturnCueRules` stay.
- `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs`: rewritten. Panel pips, the "Quiver N/size" label and their colours are gone; now body Image, one arrow Image per arrow, rim Image.
- `Features/UI/Panels/Scripts/FactionRoleVisual.cs`: the call to the removed prompt label.
- `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: 5 lines added to the `LindaQuiver` block (the four sprite references, using the fileIDs from the art's `.meta` files). Nothing else in it changed.
- Tests: `Scripts/Quiver/Editor/QuiverReadabilityTests.cs` (removed the panel label, Watch prompt, preview label and move-preview-count tests; added board-arrow, panel-layout and art-wrap tests). `Scripts/Quiver/Editor/QuiverWiringTests.cs`: added `Linda_QuiverHasItsDrawnArt` (this file already had uncommitted changes from before; mine is one added test, placed before `Linda_HandBackBeatTimingsAreSane`).

Removed:
- `Scripts/Quiver/QuiverPromptLabel.cs` and `.meta`
- `Scripts/Quiver/QuiverMovePreviewPresenter.cs` and `.meta`

Not touched: the 5 arrow prefabs, the TMP fallback asset, ProjectSettings, `claude-handoff` docs other than this report and the play check. THJ's art `.meta` files are as they were. No core code. LF kept in every file.

## Acceptance criteria

- [x] No arrow-related text on the board or the panel; only tooltips have words. Evidence: code removal. Needs the play check (steps 1, 6).
- [~] Linda's panel shows the quiver with exactly her arrows, updating on spend, pickup, catch and Encore. Code follows `LindaQuiver.OnChanged`, which all four raise. Play check steps 1 to 5. Layout numbers have unit tests, the look does not.
- [~] Grounded arrows use the new art, stacks overlap, locked are tinted, never cover an HP bar. Rules tested; sorting is DynamicTop below order 0. Play check 7 to 9.
- [~] Aim ghost, no ring. Play check 10.
- [~] Curved Encore lines, same style as John's tether. Play check 11.
- [x] "+1" cues and the pips under Linda are not edited. Play check 12.
- [x] Dead code removed (see Removed and Changed), with tests updated.
- [ ] EditMode passes. Not run (editor open, MCP down). Needs THJ.

Test coverage: `GroundedArrowLook` and `QuiverHudRules` rules, the art wrap on `LindaQuiver`, the prefab wiring, and the surviving text rules. The verifier's play check is needed for everything drawn.

## Save reset

no

## Decisions I made

- Curved lines: John's tether is a `JohnTetherPresenter` in Core, tied to John's role prompt, so I did not call it. I reused the public `ArcLine` utility (the same Bezier it and the threat arc use) inside `QuiverAimPresenter`, with the tether's width, samples and height rule (1 + 0.15 per cell), a plain runtime `Sprites/Default` material, and a warm yellow at 0.85 alpha. No pulse any more. The lines stay on the WorldUI layer. Same behaviour as asked, not a copy of the renderer.
- The art reaches the code through serialized fields on `LindaQuiver`, set in `Unit_Linda.prefab`, since Linda's art is not in a Resources folder and there is only one Linda prefab. A `LindaQuiver` without art draws no board arrows, ghost or panel quiver (and logs nothing).
- Panel quiver placement: parented to the portrait's parent (not the portrait, in case it clips), anchored like the portrait, pivot at its own bottom-right, sitting at the portrait's bottom-right corner plus 14 pixels over it, drawn just above the portrait. Sizes are the sprites' pixel sizes (Image size = `sprite.rect.size`, which equals native size at 100 PPU and the canvas's default reference PPU). I guessed the free space from `CharacterHUD.prefab` (portrait 135 x 135 at x 28, health bar from x 179); I could not look at it in Unity.
- Arrow placement inside the quiver was found by compositing the PNGs outside Unity: arrows lean the same way as the quiver, tips sit under the rim, spread along the mouth (6 px apart, less when the quiver is bigger than 5). The arrows are 87 px tall, so about 55 px of them stand above the quiver body. Arrow variants alternate per slot. Used arrows leave from the last slot.
- Ghost: always `Arrows_0` at 45% alpha on the landing cell's arrow spot; it sits at DynamicTop order -5, under the board arrows.
- Board arrows: variant picked by a hash of cell and index in the stack, so the same arrow keeps its look; a stack shows at most 3, and the 3rd arrow disappears when the stack drops below 3.
- New `.meta` files for the two new scripts were written by hand with fresh GUIDs. Unity will accept them.

## Needs THJ

none

## Docs to update

- `status.md` and `build-log.md`: quiver strip built, waiting on the compile, tests and play.
- `design/demo-spec.md`: if it describes the quiver text, the badges or the ring, it is now out of date.

## Risks and loose ends

- Review fix: the panel quiver comments now say that 71 of its 85 px lie over the portrait and the right edge is 14 px past it; unused `using` removed from `QuiverPreviewRules.cs`. Placement unchanged.
- Nothing compiled. Expect at most small typos.
- The panel quiver may overlap something in the real HUD; it is built from a guess of the layout. Tunable in `UnitPanelUI.Quiver.cs` (`QuiverOverlapRight`) and `QuiverHudRules`.
- The rim art is a black shape; I read it as the dark mouth drawn over the lower ends of the arrows. If THJ meant it differently, only the numbers in `QuiverHudRules` change.
- Hand-back toss and Encore flight still draw the arrow's own projectile sprite, not the new art (not in the plan).
- `QuiverSprites.Arrow()` placeholder still draws the pips and the "+1" cue icon; THJ said keep them.
- `QuiverPreviewRules.cs` now holds only `LandingMarkerRules` and `ReturnCueRules`, so the file name is slightly off. Left alone.
- Noticed: the `QuiverReadabilityTests` header comment and some older doc lines may still mention move-preview text.

## Proposed commits

1. `refactor(linda): remove the quiver's panel text, move-preview label, Watch prompt line and landing ring`: removed `QuiverPromptLabel.cs(.meta)`, `QuiverMovePreviewPresenter.cs(.meta)`; edits to `QuiverTextRules.cs`, `QuiverPipRules.cs`, `QuiverPreviewRules.cs`, `QuiverSprites.cs`, `FactionRoleVisual.cs`, and the matching test deletions in `QuiverReadabilityTests.cs` (plain). Only compiles together with 2 and 3 where they share files (`LindaQuiver.cs`, `GroundedArrowField.cs`), so combine if the build breaks in between.
2. `feat(linda): draw the quiver with the new art`: Arts `Quiver/` folder with its `.meta` files (untracked, THJ's), `LindaQuiver.cs`, `Unit_Linda.prefab` (plain, but a prefab: its own commit with the art).
3. `feat(linda): grounded arrows, aim ghost and curved Encore lines use the new art`: `GroundedArrowLook.cs(.meta)`, `GroundedArrowField.cs`, `QuiverAimPresenter.cs` and the tests for them (plain).
4. `feat(linda): show the quiver on Linda's unit panel`: `QuiverHudRules.cs(.meta)`, `UnitPanelUI.Quiver.cs` and its tests (plain, UI).

Order: 2, 1, 3, 4 builds cleanly in sequence (2 adds fields and removes the ring and pixel sprites; if that breaks 1's dependants, merge 1 into 2). Not part of these commits: the Kinematic Rigidbody2D on the five arrow prefabs and the `QuiverWiringTests.cs` test from before (their own commit; `QuiverWiringTests.cs` now also holds my one test, so stage it with commit 2 or split by hunk), the TMP fallback asset and ProjectSettings.

## Other branches

none

## How to see it

1. Focus the Unity editor, wait for the compile, fix any error the Console shows.
2. Test Runner > EditMode > Run All.
3. Open a level with Linda, enter Play, select Linda, and follow `playtests/2026-10-28-quiver-strip-play-check.md`.

## Play-check tweaks

Not compiled and not run: the editor is open and the Unity MCP connection is down (ECONNREFUSED). THJ must focus the editor, fix any typo the Console shows, and run EditMode.

### Values (before -> after)

- Pips under Linda (`QuiverPipsView`): `PipHeight` 0.26 -> 0.13, `PipSpacing` 0.16 -> 0.08, `BelowFeet` 0.14 -> 0.12 (all in cells; half size, so they sit a little closer to her feet).
- "+1" cue (`QuiverReturnCue`): `IconHeightCells` 0.3 -> 0.15, `FontCells` 4 -> 2, `SideCells` 0.32 -> 0.2, `SlotStepCells` 0.3 -> 0.2. The rise (0.5) and the catch flash are unchanged.
- HUD quiver (`UnitPanelUI.Quiver.cs`): now at the portrait's top-left. The quiver's pivot is its top-left corner; that corner sits `QuiverOverlapLeft` (renamed from `QuiverOverlapRight`, still 14 px) left of the portrait's top-left corner, so 71 of its 85 px lie over the portrait. Same sibling order and arrows-inside look. Header and placement comments updated. Unverified in the real HUD: whether 14 px to the left clips or collides with anything.

### Combat log: how it works

The "Quiver:" lines are gone (spend, land, pickup, round start, level start, Watch prompt, return, recall). The quiver count is added to the line of the action that changed it, as one suffix after " · ". Sample lines:

- `[R2 Player] Linda (7,1) › Bow Attack → Goblin (9,1) · quiver 1/4`
- `[R2 Player] Linda (6,1) › Watch → Goblin (9,1) · quiver 0/4` (her Watch shot; the family-role line gets the suffix)
- `[R2 Player] John (5,1) › Move → (6,1) · +2 arrows, quiver 2/4` (pickup on someone's move; works for any unit)
- `[R3 Player] Linda (7,1) › Recall · +3 arrows, quiver 4/4`
- Mark's catch: `... · +1 arrow, quiver 4/4` on the action it happens in.

One suffix per action: a later annotation replaces the earlier one, so the final count wins (a shot whose arrow is then picked up in the same action shows only the "+N" text). A Watch decline now writes nothing.

### Core change (needs its own commit): generic, additive log annotation

Core, `Core/Systems/CombatLogging` (not on the core list). Imports nothing from Linda.
- `CombatLogEntry.Suffix` (new string).
- `CombatLogFormat.Compose`: action lines append ` · <Suffix>` when set; `ToJson` gains a `suffix` field.
- `CombatLog.Custom.cs` rewritten: `AddCustom` (and its Note lines) removed; new public `AnnotateAction(string text)`. For the note to reach a line, the newest action line is now held back until the next entry is written or its action closes (`AddAction`, `WritePendingAction`; `Add` in `CombatLog.cs`, three call sites in `CombatLog.Actions.cs`). Line order and text are unchanged for lines without a note; the only visible effect is that an action line reaches the UI and the file sinks a moment later (when the next entry or the action's end comes).
- `CombatLogFormat.Tagged` is now unused by game code (only its own test). Left in place; delete if you want.
- Test: `ActionSuffix_ReadsAfterTheLineAndIsInTheJson` in `CombatLogTests.cs`.
- Risk: if a quiver change happens after another entry was already written under the same action (for instance a damage row before the arrow is spent), the note is dropped, not moved. Spend happens at launch, before hits, so I expect that to be rare. Check in the play check, especially Watch (the role line may be followed by a result row before the shot spends).

### Quiver files

- `QuiverLogLines.cs`: now only `Spent(count, size)` and `Returned(amount, count, size)`; `Category` and the other builders deleted.
- `QuiverLogListener.cs`: rewritten to listen to `OnSpent` and `OnReturned` (all kinds, since pickups and Recall add through `Add`) and call `AnnotateAction`. The level, turn, field and role-outcome hooks are gone.
- `Editor/QuiverLogLinesTests.cs`: rewritten for the two builders and a composed line.
- Left alone though now without log subscribers: the field's `OnArrowLanded`, `OnArrowsPickedUp`, `OnRecalled` events and `ArrowPickupMoment` (public API; delete in a later pass if you want).

### Files changed in this round

- `Features/Player/Linda/Scripts/Quiver/QuiverPipsView.cs`, `QuiverReturnCue.cs`
- `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs`
- `Features/Player/Linda/Scripts/Quiver/QuiverLogLines.cs`, `QuiverLogListener.cs`, `Editor/QuiverLogLinesTests.cs`
- `Core/Systems/CombatLogging/Runtime/CombatLogEntry.cs`, `CombatLogFormat.cs`, `CombatLog.cs`, `CombatLog.Actions.cs`, `CombatLog.Custom.cs`
- `Core/Systems/CombatLogging/Editor/CombatLogTests.cs`

LF kept everywhere. No save reset. Not touched: art folder, TMP asset, ProjectSettings, prefabs.

### Updated commit units

1. (new, Core, own commit, first of the log pair) `feat(log): let features annotate the running action's log line`: the five Core Runtime files above and `CombatLogTests.cs`. Replaces the committed `AddCustom`, so it must go before unit 2 and after the commits that still use `AddCustom` (`19e02893a` and earlier).
2. (new) `feat(linda): show the quiver count on the combat log's action lines instead of separate lines`: `QuiverLogLines.cs`, `QuiverLogListener.cs`, `QuiverLogLinesTests.cs`. Does not compile before unit 1.
3. Units 1 to 4 of the earlier list (strip-down) keep their contents, except: unit 4 (panel) now also carries the top-left placement, and the pip and cue size changes go with the draw-art unit (earlier unit 3, or its own small `tweak(linda): halve the pips under Linda and the +1 cue` commit with `QuiverPipsView.cs` and `QuiverReturnCue.cs`; they are separate files, so a split is easy).
Suggested order: log unit 1, log unit 2, then the strip-down commits, then the pip and cue tweak. The arrow prefab Rigidbody2D commit stays separate as before.

### How to see it

1. Focus the editor, wait for the compile, run EditMode.
2. Play a level with Linda: pips under her are about half size; a "+1" cue is smaller.
3. Select Linda: the quiver sits at the top-left of her portrait.
4. Open the combat log: no "Quiver:" lines; shots, Watch, a pickup on a move and Recall show the count after " · ".
