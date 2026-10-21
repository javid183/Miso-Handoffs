# Report: Strip private IDs from code

Plan: none (THJ request, Tier 2, size M)    Agent: miso-implementer    Branch: masher-tweak
Outcome: done

## What changed

Comment, tooltip and test-section-header text only, in 48 `.cs` files under `miso/Assets/_Project/` (147 lines changed after the follow-up). Decision, plan, chunk and playtest IDs (`D-###`, `B4`, `R3a/R3b/R4/R5/R6`, `item A-F`, `C2/C4/C5`, `F1/F3/F5`, `Q20`, `S9`) were removed and the sentences reworded to read on their own. No code, identifiers, test names or log strings changed (no log, header or test-name string held an ID). Line endings and BOM verified identical to HEAD for every file (CR count and first 3 bytes compared). `AIRegressionTest.cs` untouched.

Files:
- Core/FX/Runtime/DamageNumber.cs
- Core/FX/Runtime/DamageNumberManager.cs
- Core/Interactions/Editor/ShiftPreviewRulesTests.cs
- Core/Interactions/Runtime/PlayerController.cs
- Core/Interactions/Runtime/ShowStatsHoverPreview.cs
- Core/Managers/GlobalEventBus.cs
- Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleProvocationSuppressionTests.cs
- Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleRulesTests.cs
- Core/Systems/AbilitySystem/Abilities/Runtime/AbilityAnimationSafety.cs
- Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs
- Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleRules.cs
- Core/Systems/GridSystem/Runtime/GridCell.CoverIcon.cs
- Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs
- Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs
- Core/Systems/GridSystem/Runtime/GridCell.cs
- Core/Systems/RoleZoneSystem/Editor/CoverIconRulesTests.cs
- Core/Systems/RoleZoneSystem/Editor/RoleBarkRulesTests.cs
- Core/Systems/RoleZoneSystem/Editor/RoleZoneAttackMatchTests.cs
- Core/Systems/RoleZoneSystem/Editor/RoleZoneBadgeHoverTests.cs
- Core/Systems/RoleZoneSystem/Editor/RoleZoneFocusTests.cs
- Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs
- Core/Systems/RoleZoneSystem/Editor/TetherRulesTests.cs
- Core/Systems/RoleZoneSystem/Runtime/CoverIconRules.cs
- Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs
- Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleBarkPresenter.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleBarkRules.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleZoneAttackMatch.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs
- Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs
- Core/Systems/RoleZoneSystem/Runtime/TetherRules.cs
- Features/Enemy/Masher Goblin/Editor/MasherCounterQueueTests.cs
- Features/Enemy/Masher Goblin/Editor/MasherCounterRulesTests.cs
- Features/Enemy/Masher Goblin/Editor/MasherDuoCreditTests.cs
- Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs
- Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs
- Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs
- Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs
- Features/Player/John/Scripts/JohnFactionRoleHandler.cs
- Features/Player/Linda/Scripts/LindaFactionRoleHandler.cs
- Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs
- Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs
- Features/UI/Panels/Editor/RoleBadgeRulesTests.cs
- Features/UI/Panels/Scripts/RoleBadgeState.cs
- Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs

- Core/Editor/StatsResourcesTestDashboardWindow.cs (follow-up, see below)

## Follow-up

THJ asked to strip the dashboard warning tags too: removed `P0-2`, `P0-3`, `P0-4`, `P1-3` from the four warning strings in `Core/Editor/StatsResourcesTestDashboardWindow.cs` (each now reads as plain words). File is LF with BOM, both unchanged. Nothing else referenced those strings. Refresh: 0 errors. EditMode re-run: 413 total, 412 passed, 1 failed (known `AIRegressionTest.Baseline_MatchesCurrentAI`). No remaining non-format regex hits other than those listed above.

## Acceptance criteria

- [x] No private IDs left in comments, tooltips, headers, log strings, test names: re-ran the regex plus a wider one (`item A-F`, `R3a`, `phase N`, `chunk`, `playtest`, `revision N`, `(THJ)`); only the items below remain.
- [x] Compiles, console clean: forced refresh + compile, 0 errors (only pre-existing warnings).
- [x] EditMode suite: 413 total, 412 passed, 1 failed = the known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- [x] Comment-only: no non-comment code touched (Tooltip edits changed only the string text, e.g. removed " (B4)" and added a period).

## Remaining regex hits, left on purpose (not private IDs)

- `F0/F1/F2/F6` format specifiers (`ToString("F2")`, `{x:F2}`) in AIRegressionTest.cs (off limits anyway), TimeScaleHandlerEditorTool.cs, CameraHandler.cs, CameraBoundaryBatchTool.cs.
- `P0` in CombatLogFormat.cs and JohnPassiveAbility_Wrath.cs comments: the `ToString("P0")` locale bug, a real format string.
- `[TabGroup("L1", ...)]` in LevelBase.cs and CombatLevel.cs: Odin tab names, serialized UI identifiers.
- `[R1/R2/R3 Player|Enemy]` and `Level2-C1` in CombatLogTests.cs: expected combat-log output (round numbers) and a level name.
- `L={..} R={..} B={..} T={..}` in CameraHandler.cs and CameraBoundaryBatchTool.cs: left/right/bottom/top boundary in a log string.
- GameHandler.cs:158 `back to L0`: level 0 of the family upgrades, a game term.
- (none: the four dashboard warning tags were stripped afterwards, see "Follow-up".)

## Save reset

no

## Decisions I made

- Section-header comments in tests lost their tag but keep the topic (e.g. `---------- strict fist ----------`).
- Where a tag was the only content of a parenthetical it was dropped; where it carried a reason (e.g. the Masher preview's known approximation) the reason stays in words.
- Applied via a throwaway perl script on raw bytes (CRLF/BOM safe) plus literal replacements; reviewed the full added-lines diff by eye.

## Needs THJ

none

## Docs to update

none

## Risks and loose ends

- Since no identifiers were touched, nothing references renamed names. No method or test identifier contained an ID.
- git warns "CRLF will be replaced by LF" on a few files; pre-existing autocrlf behaviour, not caused by this change.

## Proposed commits

1. `chore(comments): replace decision and playtest tags in comments and tooltips with plain wording`: the 48 files listed above (plain, comment-only; no `.meta` files).

## Other branches

Any branch still holding the old comments will conflict textually on these lines when merged; low risk.

## How to see it

1. Open Unity, let it recompile (no errors).
2. Test Runner > EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` fails.
3. `git diff --stat -- miso/Assets/_Project` shows comment-only changes.
