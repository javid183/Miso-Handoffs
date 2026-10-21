# Review: quick wins C3a (stepped HP preview + lethal skull)

Reviewer: miso-reviewer (read-only; saved by the coordinator)    Branch: thj/quick-wins    Date: 2026-10-21
Verdict: **APPROVE**

## Must fix

None.

## Should fix

1. **Commit grouping.** Core wiring (`GUnit`, `PlayerController`) gets its own commit (CLAUDE.md). Split: (1) settings `GlobalSettingsSO.cs` + `GlobalSettings.asset`; (2) UI and skull: `DamagePreviewRules.cs`, `LethalMarkPulse.cs` (+ .meta), `UI_Element_FillBar.cs`, `EntityInfoPanelUI.cs`, both prefabs, tests (+ .meta) — builds on (1) alone and gives every single-target preview the skull; (3) core wiring `GUnit.cs` + `PlayerController.cs` (stepped preview while picking). The core part can then be reverted without losing the skull.
2. **`PlayerController.cs` ~1199-1201 / 1552-1557.** `ClearMoveHoverPreview` keeps its own copy of the hide loop next to the new `HideDamagePreviews()`; call the helper so they can't drift.
3. **`LethalMarkPulse.OnEnable` resets `_startTime`.** Each hover hides and re-shows the panel in one frame (clear → confirmed-only → full preview), so the pulse restarts at scale 1 on every cell change; sweeping the cursor looks unpulsed. Keep the phase when the skull was already showing for the same unit, or skip the confirmed-only redraw when a full preview follows (also saves a `ComputeFor`).

## Notes

- **GUnit overload (D-136):** agrees with the 3-argument optional-enum form; a bool would need "stepped" inferred from `confirmed > 0` and lose the light tint on a first, unpicked target; a precomputed mark would move the rule into core. `GUnit` already depends on `EntityInfoPanelUI`'s namespace, so `DamagePreviewPick` adds no new dependency direction (could be nested in `EntityInfoPanelUI`; optional).
- `PlayerController` changes private; single-target path untouched; `AbilityDamagePreview.cs` untouched; confirmed = `ComputeFor(..., null, TargetCells)`, total = with the hovered cell.
- Lethal rule matches D-135 (`Single` normal skull at damage ≥ HP > 0; picking: confirmed kills → normal; `FinalPick` only → tinted for confirmed + this click; `Picking` never for a kill needing the hovered click; option off → no skull, tint reset). Same `>=` as `PredictsLethalOn`.
- No stale segments/skulls: undo 2→1 redraws, 1→0 returns to ActionSelection (clears), full cancel, fire (TakeAction), turn end (Cleanup), forced/level end (ForceEndTurn) all clear; `ShowFullMode` hides the second segment and the skull.
- First pick via the default ability and the approach-walk preview: unchanged paths, correct.
- No new mutable statics; not AI-visible; prefab diffs additive; `UnitBase.prefab` untouched; CRLF/BOM kept; new GUIDs unique; no private IDs.
- **Play-check extras:** `Mark_Ability_Attack_Command` and `Dom_Ability_Swap` take the multi-target path but should show no HP preview and no skull. *(Coordinator correction, 2026-10-21: the review first said Command would draw its damage in the "this click" tint. THJ pointed out Command is not an attack; its effects are UnitTransport and a "Weak" `Stat_DMG ×0.6` modifier, no HP change, so there is nothing to preview.)*
- Test pin to `PredictsLethalOn` is by matching cases, not a shared call (would need a grid fixture or a core edit); they can drift until `AbilityDamagePreview` is next touched with THJ's OK.
- `showTargetCounterLabel` unused until C3c; keep it in the settings commit. The two reds are close (0.651,0,0 vs 0.42,0,0.03): THJ to judge.
