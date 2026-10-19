# Report: B4 R5 John's tether line (item F)

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: blocked (stopped before writing code, as instructed: the prompting role is not publicly readable)

## What changed

Nothing. No files touched.

## Why blocked

Targets are readable (`FactionRoleHandlerBase.Targets` is a public getter, `ShowRoleZone` and `RoleZoneColor` too). What is NOT readable is WHICH role the QTE on screen belongs to:
- `qteStarted` carries only a `QTEButton`; it exposes no profile, owner unit or hook (`_positionHook` is private; `Prepare` is the only entry).
- `onFamilyRoleActivated` fires only on success (`Activate`), after the press.
- `CombatLevelUIManager.ShowFactionRolePromptVisual` -> `FactionRoleVisual.SetData` stores `roleUnit` privately and never clears it.
- Inferring it ("a QTE is active, `Time.timeScale == 0`, John has non-empty `Targets`") is unreliable: `Targets` stays set after John's last activation (stale), and other QTEs also run at timeScale 0 (`UnitsCooperationHandler.cs:228` duo QTE, `ProjectileCatchAndReturn`, John's Command Shield Dash passive, reversion QTE). It would draw a tether during the wrong QTE.

## Smallest additive hook (needs coordinator/THJ OK: touches core)

Option B (recommended, precise): in `GlobalEventBus.cs` add `public UnityEvent<FactionRoleHandlerBase> onFamilyRolePrompt = new();` and, in `PlayerController.ActivateFactionRole`, after `var started = QuickTimeEventHandler.StartEvent(...)`, `if (started) GlobalEventBus.Instance.onFamilyRolePrompt.Invoke(unit.AbilityOrchestrator.FactionRoleHandler);` (one line each; no logic change). It fires only when a role prompt really started, so "could not start" never draws. The presenter ends the tether on `qteEnded` (covers press and decline/timer expiry), `levelEnded`, `OnDisable`/scene unload.

Option A (non-core, weaker): additive `public GUnit RoleUnit => roleUnit;` on `FactionRoleVisual` plus the heuristic above; still has the stale-Targets/duo false-positive risk. Not recommended.

Rest of the design is ready once B (or A) is approved: new `JohnTetherPresenter` MonoBehaviour in `Core/Systems/RoleZoneSystem/Runtime`, hosted by one idempotent `AddComponent` line in `ShowStatsHoverPreview.Awake` placed after the existing R3b `MovePreviewCoverPresenter` line (unaltered), LineRenderers pooled per target in `RoleZoneColor`, static (no animation), sorting order above units and below UI, honours `ShowRoleZone`, only for `JohnFactionRoleHandler`, null-safe per target, pure helper `TetherRules` for target filtering + clear flags with EditMode tests. No statics.

## Acceptance criteria

- [ ] F: not built (blocked on the hook above).

## Save reset

no

## Needs THJ

Approve Option B (two additive lines in core `GlobalEventBus` and `PlayerController`, no behaviour change), or choose Option A.

## Docs to update

none yet

## Risks and loose ends

- Tree has uncommitted work from other chunks; untouched.

## Proposed commits

none (no changes)

## Other branches

none

## How to see it

n/a
