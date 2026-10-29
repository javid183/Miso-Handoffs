# Report: Quiver feedback pass (deeper feedback in the one layer)

Plan: plans/2026-10-28-quiver-feedback-pass.md    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 79ca381e8, uncommitted)
Outcome: done (two points need THJ's call, see Needs THJ; nothing play-checked yet)

## What changed, per point

1. **Shift shows her arrows (D-301).**
   - **What I found:** on Shift, `GUnit` opens every unit's `EntityInfoPanel` (Global mode). That panel is a world-space canvas on the **Overlay** sorting layer (order 1). On `UnitBase` it hangs from `Visual/UnitInfoHook` at y -0.19, the same anchor as the mini HP bar, and it grows **upward** from there (bottom-anchored `UnitInfoContainer`, about 0.25 to 0.4 world tall at scale 0.005). The pips sit at feet minus 0.12 cell, on **DynamicTop** order -1. So the panel's background sits right over the pip row, on a layer above DynamicTop. The arrows are **covered by her own panel and sorted under it**; nothing hides them. The same happens on hover and on a damage preview (the same panel).
   - **Fix (no core):** `QuiverPipsView` finds her `EntityInfoPanelUI` and its canvas on Start (`GetComponentInChildren`, read-only). While the panel is active, the row moves onto the panel's top edge (the highest laid-out image under the canvas, plus a small gap). It also draws on the panel canvas's layer at its order + 1 (`QuiverPipRules.OrderAbove`), so it reads as part of the panel. When the panel closes, the row goes back under her feet: DynamicTop, below every HP bar.
2. **Empty state under her feet:** at 0 arrows the row hides its four dark outlines and shows one grey arrow with a thin muted-red slash over it. The slash is a code-made thin bar (`QuiverSprites.Slash()`) rotated -40°, owned and released by the view. With 1 or more arrows the row is unchanged. Rules: `QuiverPipRules.ShowsPipRow` / `ShowsEmptyMark`.
3. **HUD quiver feedback** (in THJ's `QuiverUI`, all DOTween, unscaled time, 0.18 s or 0.28 s):
   - **Empty:** the body and rim tint to a muted red-grey (`emptyTint` 0.66/0.42/0.42) while the count is 0, and tint back when an arrow returns.
   - **Lift:** the quiver scales to 1.12 × its own scale (THJ's root is x-flipped at -1.053; the base is captured, never overwritten) while her slot-1 ability is hovered on the bar or is the aimed ability (`QuiverLevelAccess.AimedAbilityOrNull`, read-only, the same check the aim presenter uses).
   - **No arrows:** at 0 arrows the same reach plays a single punch (1.3 out and back) once per hover start, button click or number-key press. A greyed button's click never reaches `onClick`, so I added a feedback-only press event (see Decisions).
   - **Gain:** each newly shown arrow pops in from 1.3× scale and 35 % alpha and settles, and the whole quiver gives a light 1.06 pulse. Pickup, catch and Encore all go through the quiver's change event.
   - **Cleanup:** every tween is killed on `OnDisable`, `OnDestroy`, panel `Hide()` and unit switch (`ResetFeedback` puts scale and colours back). Rules: `QuiverHudFeedbackRules`.
4. **Encore lines:**
   - `LineWidth` goes from 0.025 to 0.0125, and the alpha is 0.6.
   - The shine comes from the material, not from code: `SH_LineShine` lerps `_BaseColor` to `_ShineColor` along UV.x over time. With `textureMode` Stretch, UV.x runs from the first point to the last. The threat line's first point is the enemy; ours is the stack (ArcLine from stack to Linda), so the shine runs stack → Linda.
   - `LindaQuiver.encoreLineMaterial` (a new partial file) is set to `M_LineShine` on `Unit_Linda.prefab`. The presenter makes one runtime copy, recolours it gold (base 1/0.85/0.35, shine 1/0.97/0.85) and lets the line's vertex colour carry the 0.6 alpha. The URP sprite-unlit pass multiplies vertex colour and the graph blends transparently. With no material set it falls back to the old plain Sprites/Default line.
5. **Encore costs 2 AP (D-302):** `Linda_Ability_Recall.asset` `apConsumptionType: 1 → 2`. The AP preview reads `(int)apConsumptionType`, so it shows 2 on hover and on select. Neither the button nor the tooltip shows a cost at all. The enum has no named value for 2, and Per-unit mode doesn't enforce it: see Needs THJ. The known-red `AIRegressionTest` message is **identical** to the pre-change baseline (diffed, timing lines aside).
6. **THJ's HUD prefab:**
   - The run-time HUD building in `UnitPanelUI.Quiver.cs` is gone. The partial now finds the `QuiverUI` instance under the panel once, shows it only for a unit with a `LindaQuiver` (alive, size > 0), drives its count from the quiver event, and hides it for every other unit.
   - `QuiverUI.cs`: no NUnit import; namespace `MISO.Content.UI.UnitPanel` (same GUID, prefab class id updated); serialized `body` and `rim` (wired in the prefab); THJ's `ShowArrowCharges(int)` kept as the no-feedback setter, plus `ChangeArrowCharges(int)`; CRLF kept.
   - Removed: `QuiverHudRules` (all HUD layout, deleted with its four tests), `LindaQuiver.quiverBodySprite/quiverRimSprite` and their properties (and the two orphaned YAML lines on Linda), and the body/rim asserts in two tests. `QuiverSprites` had nothing HUD-only.
   - No object of his was moved or resized. His `CharacterHUD.prefab` edit is untouched and goes into commit 2.
7. **Grounded arrows:**
   - One arrow per stack, with a stable art variant per cell (same hash as before for index 0).
   - For 2 or more arrows, a small world-space `xN` (TextMeshPro, Fairfax SDF, the HUD's font, via `LindaQuiver.stackCountFont`) sits at the arrow's lower right. It is bold, cream, with a thin black outline like the return cue, and is written with `SetText` (no allocations).
   - The arrow is on DynamicTop -4 and the label on -3, both under the pips (-1) and every HP bar (0+). The label takes the dark tint too while an enemy stands on the stack.
   - `IconOffset.x` goes from 0.18 to 0.35 cell-distance units. The ghost, the flights and the Encore line ends all use `StackIconPosition`, so they move with it.

## Acceptance criteria

- [ ] Holding Shift with Linda on the board: her arrow row is visible and correct. Code done (row on her panel's top edge, sorted above it). Needs the play check.
- [x] At 0 arrows the row shows a single crossed arrow; with arrows it's unchanged. Rules tested (`QuiverEmptyRowTests`); the look needs the play check.
- [x] The HUD uses `LindaQuiver.prefab`'s objects (no run-time HUD building remains), shows the exact count and appears only on Linda's panel. Prefab wiring tested (`HudPrefab_HasFourArrowsBodyAndRimWiredAndTakesNoClicks`, `CharacterHud_HoldsTheQuiver`); the panel switch needs the play check.
- [ ] The HUD tints when empty, lifts on primary hover or select, punches at 0 arrows and glows new arrows on gain, and no tween survives a hide or panel switch. Trigger rules tested; the tweens need the play check.
- [ ] Encore lines are thinner, partly transparent and shine from stack to Linda. Material wiring tested (`EncoreLineWiringTests`); the look needs the play check.
- [x] Encore costs 2 AP everywhere it's shown. Data plus test (`RecallAbility_IsTwoApCooldownTwoSelfCast`); the AP preview reads the same value. Caveat in Needs THJ.
- [ ] Grounded arrows: one icon, nudged right, `xN` for N ≥ 2, tint kept, never over an HP bar, ghost matches. `xN` rule and sorting tested (`GroundedArrowStackLookTests`); the look needs the play check.
- [x] `QuiverUI.cs` has no NUnit import and lives in a namespace.
- [x] EditMode passes with only the known red failing: **981 run, 980 passed, 1 failed** = `AIRegressionTest.Baseline_MatchesCurrentAI`. The pre-change baseline was 971/970 with the same failure; its message is unchanged.

## Save reset

No.

## Decisions I made

- **Press event for the no-arrows punch (Tier 1, non-core UI).**
  - `AbilitiesBarHUDUI.AbilityPressed` is raised from the number-key shortcut, and `UnitAbilityButtonUI.Pressed` from `IPointerClickHandler`.
  - Without them, a press on the greyed bow at 0 arrows reaches nothing: `Click()` and `onClick` stop on non-interactable.
  - Both are feedback only and change no flow. Neither file is named in the plan.
- **Hover, select and hide hooks (same behavior):**
  - The selection poll rides on the existing `LateUpdate` in `UnitPanelUI.LowHealth.cs`; a class can have only one.
  - `UnitPanelUI.Hide()` gets one line, `ForgetQuiverFeedback()`.
- **Finding the HUD view (same behavior):** the panel finds `QuiverUI` with `GetComponentInChildren(true)` instead of a serialized reference. The instance is two prefab levels down (UnitPanel → CharacterHUD → LindaQuiver), and wiring that by YAML isn't small.
- **Clicks on the HUD images (same behavior as the old code-built quiver):** `m_RaycastTarget` is set to 0 on the six images of THJ's quiver prefab, so they don't eat clicks over the portrait and role badge. A YAML value, not layout.
- **Tunables:** the tween values are serialized on `QuiverUI` (the prefab carries the plan's numbers) so THJ can tune them in the Inspector.
- **Where the row goes under Shift (point 1):** I chose "on top of the panel's edge and sorted above its canvas" over "inside it", so the row never sits on the panel's HP bar.
- **Nudge size (point 7):** the existing offset was already 0.18 "cell" (the distance between cell anchors, about 0.28 world on this grid). I read the plan's 0.15 to 0.2 of a cell as an extra nudge of about 0.17 in those units, so 0.35 now. One constant, `GroundedArrowField.IconOffset`.
- **Partial files:** `LindaQuiver` became `partial`, with `LindaQuiver.StackLabel.cs` (font) and `LindaQuiver.EncoreLine.cs` (material), so commits 4 and 5 own their own references.
- **Statics:** none new. Only immutable `static readonly` colours and offsets, like the ones already in these files. Material property names are constant strings, not cached static ids.

## Needs THJ

1. **Encore's 2 AP is not enforced in Per-unit AP mode.**
   - **Situation:** `GlobalSettings.aPConsumptionMode` is 1, which is **PerUnit**. In that mode `ActionPoints.CanConsume` returns `Points > 0` whatever the cost (marked "todo: reserved" in core), and `Consume` subtracts 2.
   - **Effect:** with 1 AP left Linda can still cast Encore, and the attribute presumably clamps at 0. The preview shows 2. In Shared mode the cost of 2 is fully enforced, with escalation.
   - **Options:** (a) accept it for now; (b) a core fix so `ActionPoints.CanConsume` checks `Points >= cost`. That is Tier 3, because it changes every Per-unit ability with cost > 1 (none exist today) and what the AI reads.
   - **My recommendation:** (a) for this pass, and (b) as a separate core task if Per-unit mode stays.
2. **No named enum value for 2.**
   - **Situation:** `APConsumptionType` has only Ineffective (0), Singular (1) and Closure (int.MaxValue).
   - **Effect:** the Inspector dropdown for Encore's cost will look blank, and re-picking from the dropdown can't produce 2 again.
   - **Options:** (a) leave the data as it is; (b) add a named value such as `Double = 2` to the core enum (Tier 3, additive).
   - **My recommendation:** (b), if more 2-AP abilities are coming.

## Docs to update

- `status.md`: Encore costs 2 AP. The HUD quiver is THJ's prefab, driven by `QuiverUI`. Grounded stacks show one arrow plus `xN`.
- `tech/` quiver or Linda notes, if any describe "up to three overlapping arrows" or the code-built panel quiver: now one arrow plus `xN`, and the `LindaQuiver.prefab` HUD.
- Note for the core-systems backlog: Per-unit `ActionPoints.CanConsume` ignores the cost (Needs THJ 1).

## Risks and loose ends

- **Nothing was seen in Play.** All visuals (row placement over the panel, slash look, `xN` size and font legibility, tween feel, shine colour) need THJ's play check. Sizes are constants at the top of `QuiverPipsView`, `GroundedArrowField` and `QuiverAimPresenter`, plus the `QuiverUI` Inspector fields.
- **Draw order in THJ's prefab:** the children of `LindaQuiver.prefab` are ordered Rim, Arrow 0-3, Body, so the **body draws over the arrows and the rim**. If the arrows were meant to stand inside the quiver behind the rim, the order would be Body, Arrows, Rim. I left it alone (his layout); worth a glance.
- **THJ's `CharacterHUD.prefab` diff also changes three other sizes** (two `m_SizeDelta.x` to 0, one anchor and position change, and a nested instance's width from 100 to 0). They are his, and they go into commit 2 as he left them.
- **Rows draw over neighbours' panels:** while Shift is up, Linda's row draws on the Overlay layer above every info panel. Where a neighbour's panel overlaps her panel's top edge, her row sits over it.
- **Material instances:** the `xN` outline makes one TMP material instance per stack label, the same as the return cue does. There are few stacks, and they are destroyed with the level.
- **The pointer press event** also fires on the item buttons (their ability); only Linda's slot 1 reacts.

## Proposed commits

The plan's five units in its order. Some files carry hunks for two units; each of those goes with the **first** unit in this order. Every commit still compiles on its own, because the early hunks only drop asserts or tests, or add YAML for a field that comes later (Unity ignores unknown fields). Paths are under `miso/Assets/_Project/`.

1. **`data(linda): Encore costs 2 AP`** (plain)
   - `Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset`
   - `Features/Player/Linda/Scripts/Quiver/Editor/QuiverWiringTests.cs`: the cost test, plus the arrow-art test with its body and rim asserts dropped (part of unit 2; safe here).
2. **`feat(linda): HUD quiver from the hand-placed prefab, with empty tint, lift, no-arrows punch and gain glow`** (plain; UI only)
   - `Features/UI/Panels/Scripts/QuiverUI.cs` and `.meta`
   - `Features/UI/Panels/Prefabs/UI/HUD/LindaQuiver.prefab` and `.meta`
   - `Features/UI/Panels/Prefabs/UI/HUD/CharacterHUD.prefab` (THJ's edit)
   - `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs`, `UnitPanelUI.cs`, `UnitPanelUI.LowHealth.cs`
   - `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs`, `UnitAbilityButtonUI.cs`
   - `Features/Player/Linda/Scripts/Quiver/QuiverHudFeedbackRules.cs` and `.meta`
   - `Features/Player/Linda/Scripts/Quiver/QuiverHudRules.cs` and `.meta` (deleted)
   - `Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs`, `QuiverLevelAccess.cs`
   - `Features/Player/Linda/Scripts/Quiver/Editor/QuiverHudFeedbackTests.cs` and `.meta`
   - `Features/Player/Linda/Scripts/Quiver/Editor/QuiverReadabilityTests.cs`: deletions only; it also drops unit 4's old stack tests.
3. **`feat(linda): arrow row shows over her info panel and a crossed arrow at zero`** (plain)
   - `Features/Player/Linda/Scripts/Quiver/QuiverPipsView.cs`, `QuiverPipRules.cs`, `QuiverSprites.cs`
   - `Features/Player/Linda/Scripts/Quiver/Editor/QuiverEmptyRowTests.cs` and `.meta`
4. **`feat(linda): one arrow per grounded stack with a small count, nudged right`** (plain)
   - `Features/Player/Linda/Scripts/Quiver/GroundedArrowLook.cs`, `GroundedArrowField.cs`
   - `Features/Player/Linda/Scripts/Quiver/LindaQuiver.StackLabel.cs` and `.meta`
   - `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: the font line; it also carries the Encore material line for unit 5 and drops the two orphaned HUD sprite lines.
   - `Features/Player/Linda/Scripts/Quiver/Editor/GroundedArrowStackLookTests.cs` and `.meta`
5. **`feat(linda): thinner, see-through Encore lines with the threat line's shine`** (plain)
   - `Features/Player/Linda/Scripts/Quiver/QuiverAimPresenter.cs`
   - `Features/Player/Linda/Scripts/Quiver/LindaQuiver.EncoreLine.cs` and `.meta`
   - `Features/Player/Linda/Scripts/Quiver/Editor/EncoreLineWiringTests.cs` and `.meta`

Not to stage: `Resources/GlobalSettings.asset`, `Scenes/CombatLevelContainerScene.unity`, the TMP `LiberationSans SDF - Fallback.asset`, and `ProjectSettings/*` (THJ's unrelated local edits).

## Other branches

None. This is branch work on `thj/linda-quiver`.

## How to see it

1. Open Unity and let it compile. Open a level with Linda (intro and outro are already off in THJ's local GlobalSettings).
2. **HUD:**
   1. Select Linda. The hand-placed quiver shows 4 arrows. Select John or Lucy: it disappears. Back to Linda: it returns with no glow.
   2. Hover her slot-1 bow button: the quiver lifts a little. Move off: it settles. Press `1`: it lifts and stays up while aiming. Right-click or cancel: it settles.
   3. Shoot until 0 arrows. The body and rim turn muted red-grey. Hover the greyed bow: one punch per hover. Click it, or press `1`: one punch each time.
   4. Walk a Bergson onto a stack, let Mark catch an arrow, or cast Encore. Each returning arrow pops in, the quiver pulses once, and the tint clears.
   5. End the turn or switch units in the middle of a tween: nothing stays scaled or tinted.
3. **Under her feet:**
   1. With arrows the pip row is unchanged. At 0 arrows it shows a single grey arrow with a thin red slash.
   2. Hold **Left Shift** (and hover Linda): her info panel opens and the row, or the crossed arrow, sits on the panel's top edge, drawn over it. Release: it returns under her feet.
4. **Grounded arrows:**
   1. Shoot so arrows land: each stack shows one arrow, a little right of the tile centre. Land a second arrow on the same tile: a small `x2` appears at its lower right, in the HUD font.
   2. Stand an enemy on a stack: the arrow and the label darken. No arrow or label covers an HP bar.
   3. Aim the bow: the faint ghost sits exactly where the grounded arrow will.
5. **Encore:** with stacks down, hover Encore on the bar. The gold lines are thinner and see-through, and a shine runs along each from the stack to Linda, like an enemy's threat line. The AP preview shows 2.
6. EditMode in the Test Runner: everything green except `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Review fixes (2026-10-28, after the APPROVE)

1. **The lift recovers by itself.** `UnitPanelUI.Quiver.cs` `UpdateQuiverReach` now calls `UpdateQuiverLift()` every frame after the change check. `SetLifted` still does nothing while the state is unchanged, so if anything else disables and re-enables the quiver, the lift comes back the next frame.
2. **One format for the count.** `GroundedArrowLook.CountFormat = "x{0}"` is the single format. The view writes it with `SetText(CountFormat, count)` (no allocations), the rule uses `string.Format(CountFormat, ...)`, and `GroundedArrowStackLookTests.Label_CountsFromTwo` checks the constant.
3. **Shift row sorting: the row now draws only with her own panel.**
   - **What I chose:** while her info panel is open, the row is shown as **UI images inside her panel's own canvas**, as its first child, placed on the panel's top edge and centred on Linda. The sprite row under her feet is hidden meanwhile.
   - **Why it works:** as part of that canvas, the row sorts exactly with her panel. Wherever another unit's panel is drawn over hers, it also covers her row, so the row can never sit over another panel or HP bar. Being the first child, it is drawn before her panel's own parts and tooltips, and it sits outside her panel's rectangle anyway.
   - **Why not the other option:** matching her panel's order (Overlay 1) inside a sorting group would tie with every other panel at the same order. The project's transparency sort is the default (axis z), so who wins that tie isn't deterministic.
   - **Allocations:** the images are built once with the row (`BuildPanelRow`), sized in canvas units from the canvas scale. Following the panel each frame allocates nothing.
   - **What went away:** `QuiverPipRules.OrderAbove` and its test are removed; nothing else used them.
   - **No core code.**
   - **Still to check in Play:** the size and position of the panel row.
4. **Tests:** EditMode **980 run, 979 passed, 1 failed** = the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, with the message still identical to the pre-change baseline. The count is one lower because the `OrderAbove` test was removed. Unity was closed and no `Temp` was left behind.

The commit units are unchanged; no file moved between them. Commit 3 is `QuiverPipsView.cs`, `QuiverPipRules.cs`, `QuiverSprites.cs` and `QuiverEmptyRowTests.cs` (and `.meta`). Commit 4 now also covers the `CountFormat` edits in its own files `GroundedArrowLook.cs`, `GroundedArrowField.cs` and `GroundedArrowStackLookTests.cs`. Commit 2 also covers the `UnitPanelUI.Quiver.cs` change.

How to see fix 3: hold Shift with a unit standing on the tile north of Linda. Her row sits on her panel's top edge, and the neighbour's HP bar is never covered by her pips.
