# Report: quick wins A, C7 (Workshop shared items) and C8 (M1 grid fade)

Plan: `plans/2026-10-21-quick-wins-a-tech.md` (C7, C8). Branch `thj/quick-wins`. Both changes are data-only. Nothing committed. Paths under `miso/Assets/_Project/`.

Checks: Play mode was off when edited (an earlier attempt stopped because it was on). Compile clean, console has no errors. EditMode 517/518; the only failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red, not touched). No save was reset. No code or tests changed.

## C7. Workshop shared items (Q14 b)

**What changed**
- `Resources/Unit Equipments/Shared/Equipment_Shin Armor.asset` and `Equipment_Vitality Brooch.asset`: `equipmentState: 2` -> `0` (Hidden). One line each, LF kept.

**Checks**
- `WorkshopPanelUI.ShowPanel` (`Core/UI/Runtime/Home/WorkshopPanelUI.cs`, ~129-133, not under Features) lists only items where `EquipmentManager.GetState(e) != Hidden`. Confirmed.
- References: grepped Assets and ProjectSettings for both asset GUIDs, both equipment `id`s and both names (with and without spaces). The only hits are the assets themselves. No shop, reward, starting loadout, level unlock list or test uses them.
- `EquipmentManager.GetState` returns the saved state first and falls back to the asset's state. So an existing save that already has them as Owned keeps showing them; a fresh save no longer does. Not migrated.

**Acceptance (Q14 b):** fresh-save Workshop does not list them: Not run (needs a play check on a fresh save). The filter and reference checks pass by reading.

**Decisions:** none.

**Proposed commit:** `tweak(workshop): hide the two shared equipment items from the Workshop`
- `Resources/Unit Equipments/Shared/Equipment_Shin Armor.asset`
- `Resources/Unit Equipments/Shared/Equipment_Vitality Brooch.asset`

**Risks:** existing saves unchanged (above). The character equipment panel's Hidden filter is commented out (out of scope), so Hidden items may still show there; look when play checking.

**How to see it:** start a fresh save (or clear equipment states), open the Workshop: Shin Armor and Vitality Brooch are not listed.

## C8. M1 level 2 keeps the grid hidden at the end (Q14 a)

**What changed**
- New `Resources/Sequences/Common/OutroCutsceneKeepGridHidden.asset` (+ `.meta`, new GUID `a030f3fedbac455ea1a810a641bf57d4`), a SequentialSequence = [EnablePlayerInputSequence, ShowHUDSequence]. It was copied from `OutroCutscene.asset` with the FadeInGridSequence entry removed; existing sub-sequence assets reused.
- `Resources/Sequences/Mission 1/Level1C1/Level1C1-2_End_SequenctialSequence.asset`: the last entry changed from `OutroCutscene` to the new asset. List is now [IntroCutscene, Level1C1-2_End_DialogNodeSequence, OutroCutsceneKeepGridHidden]. Verified in Unity by loading both assets.

**Checks**
- `OutroCutscene` itself is untouched; the only changed existing file is the one End sequence. It is referenced by `Content/Levels/Level1/Level1-C1-2.prefab` and the duplicate `Level1-C1-2 1.prefab`; both get the change.
- Next level `Level1C2`: its start sequence is [IntroCutscene, dialog, OutroCutscene], so it fades the grid out and back in as usual.
- Flow in `CombatLevelRunHandler` (~660-720): on a win, HUD hides, then `PlayOutro`, then the victory panel (`EndLevel`) is shown through the UI manager. Nothing there reads the grid; the grid fade only drives the role-zone and move-preview presenters (`gridFadeIn/Out` listeners). I did not find a mission-map use of the grid by reading.
- `GlobalSettingsSO.deactivateIntroOutroSequences`: when on, `LevelBase.PlayIntro/PlayOutro` skip the whole sequence, so with it on the grid is never faded out, and the change has no effect (no worse than before). With it off (normal), the new behavior applies.
- Note: the sequence runs through `LevelBase.PlayOutro`; the End sequence's IntroCutscene fades the grid out at the start, so it ends hidden. Whether the next level load resets the grid to visible before its own intro is not verified by reading; Level1C2's intro/outro would restore it either way.

**Acceptance (Q14 a):** after Level1C1-2 ends the grid stays faded through the end of the level; the next level shows it as usual: Not run (play check).

**Decisions:** a separate named sequence asset rather than inline entries, as the brief suggested. Name `OutroCutsceneKeepGridHidden`.

**Proposed commit:** `tweak(level): keep the grid hidden after the end of M1 level 2`
- `Resources/Sequences/Common/OutroCutsceneKeepGridHidden.asset`
- `Resources/Sequences/Common/OutroCutsceneKeepGridHidden.asset.meta`
- `Resources/Sequences/Mission 1/Level1C1/Level1C1-2_End_SequenctialSequence.asset`

**Risks:** if the grid shown by the victory screen was expected, it is now hidden (none found). If a later level start does not fade the grid in itself, it could stay hidden; Level1C2 does fade in.

**How to see it:** play M1 level 2 (Level1C1-2, "John's Map (2/3)") to the win: after the end dialog the grid stays off while input and HUD return; then continue to the next level and check the grid appears after its intro. (Fast path: use the level fast-forward/sandbox tools.)
