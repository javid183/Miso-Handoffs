# Duo panel videos, chunk C2 (card first for every duo with a QTE)

Plan: `plans/2026-11-24-duo-panel-videos-tech.md`. Branch `thj/onboarding-demo`. Nothing staged or committed. Editor open, not in Play. C1 files untouched.

## What changed, per file (all under `miso/Assets/_Project/`)

- `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs` (BOM + LF kept; core edit is small): `ExecuteIE` asks the handler for the duo's start flow. If it is a card flow, `RunCardFirstIE` runs and the results are stored; `ShowDuoVisual` (the panels) then runs unless the flow is the comic insert. Added `using MISO.Features.UI.DuoInsert;`. Everything after (camera focus, partner activation with stored factors, `ActivateFromQte`) is unchanged.
- `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.Insert.cs` (all new logic):
  - `enum DuoStartFlow { Panels, CardThenPanels, CardThenInsert }`.
  - `UnitsCooperationHandler.ChooseFlow(hasQtePartner, sequence, sequenceActive, duoId, out entry)`, the pure decision: no QTE partner, no/inactive sequence, or mode Off gives `Panels`; otherwise `CardThenInsert` only if the sequence's opt-in is on and the library has an entry, else `CardThenPanels` (no library entry needed).
  - `CooperationEntry.HasQtePartner(partners)`: a partner with `qteFactor` and a non-null profile.
  - `GetDuoFlow(duo, ...)` replaces `TryGetDuoInsert` (creates the sequence, keeps the existing "inactive/missing canvas" warnings, then calls `ChooseFlow`).
  - `RunInsertIE` renamed `RunCardFirstIE`: same hold, QTEs on the card in partner order, stored results, release; the comic insert plays only if an entry was passed (`PlayInsertIE(entry, promptActions)` and its skip filter unchanged). The card caption is `entry?.caption`, so empty when there is no entry.
  - `ShouldPlayInsert` overloads kept (used by the opt-in check and tests); tooltip of `duoInsertPrefab` reworded.
- `Features/UI/DuoInsert/DuoInsertSequence.cs`: `[SerializeField] bool playComicInsert` (default false) + public `PlayComicInsert`. No prefab change needed: the value defaults to false, so `DuoInsertCanvas.prefab` and `PlayerController.prefab` are unchanged.
- `Core/Systems/AbilitySystem/Abilities/Editor/CooperationInsertTests.cs`: 9 new tests (flow decision, `HasQtePartner`). The existing `ShouldPlayInsert` tests stay valid (they describe "has an insert entry", which is now the opt-in's second condition), so none needed changing.

## Decisions

- Opt-in for the comic insert: a serialized bool `playComicInsert` on `DuoInsertSequence` (default false). On, a duo with a library entry (today only Mark-Lucy) plays card, then insert, with no panels, as before C2. Off, Mark-Lucy gets card then panels like the others.
- Card with no library entry has an empty title (the portrait of the QTE unit and the prompt still show). Say if you want a title (e.g. the duo's name).
- Timing: the old path shows the panels at time scale 1 and then waits on the camera focus before acting. The new path releases time (`ReleaseTimeForInsert`, scale 1) after the card, then shows the panels, then the same camera focus wait, so the panels get exactly the old hold.
- Data check (`PlayerController.prefab`): QTE duos are John-Lucy (Lucy, time window), Linda-Lucy (Linda, mash), Linda-Toba (Linda, mash), Mark-Lucy (Lucy, mash; Mark has none), Mark-John (Mark, time window). No QTE: John-Linda, Mark-Linda. Matches the brief.
- Stored-result mapping vs the old board path: both feed `ActivateFromQte(CoopQteFactor.Raw(mode, success, SecondaryFill), ...)`; the card passes `partner.onSuccessfulQTE` only on success and a no-op on a miss, as the board does; the same-entity `CoopQteMod` spread is inside `ActivateFromQte`, which both paths share. Time-window and press modes use 1/0 by success, mash modes use the fill, in both. Unchanged code, so no behaviour difference (not play-tested).
- Time scale / abort safety unchanged (`OnDisable` restore, pooled QTE button return).

## Tests

- Compile clean.
- `CooperationInsertTests`: 23/23 passed (including the 9 new). `DuoInsertRulesTests` is inside the full run below.
- Whole EditMode suite: 2653 run, 2643 passed, 1 skipped (Explicit AI baseline), 9 failed: the 8 known `M1RidgeTests`, and `GridToLevelFpTests.Build_WithoutTheLineAddsNoFiller` (m_LockCount editor stall), which passes alone.
- `AIRegressionTest` not run (no AI graph/ability/unit prefab touched).

Criteria with test coverage: the flow decision (QTE + mode on = card first with no library entry; no QTE, mode Off, no sequence, inactive sequence = old; opt-in + entry = insert after the card). Needs THJ's play check: the real flow in combat.

## Not checked

A real combat with a QTE duo (card, then clip panels, then action) and one without; the opt-in insert on Mark-Lucy; leaving combat mid-card. Unity MCP could not drive a real duo.

## Files for the C2 commit

- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.Insert.cs`
- `miso/Assets/_Project/Features/UI/DuoInsert/DuoInsertSequence.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/CooperationInsertTests.cs`

```
 .../Abilities/Editor/CooperationInsertTests.cs     | 74 ++++++++++++++++++++++
 .../Runtime/UnitsCooperationHandler.Insert.cs      | 71 ++++++++++++++++-----
 .../Abilities/Runtime/UnitsCooperationHandler.cs   | 17 +++--
 .../Features/UI/DuoInsert/DuoInsertSequence.cs     |  8 +++
 4 files changed, 149 insertions(+), 21 deletions(-)
```

## Risks and loose ends

- Core behaviour (approved): John-Lucy, Linda-Lucy, Linda-Toba, Mark-John now pause for a card before the panels; Mark-Lucy no longer shows the comic insert unless the opt-in is turned on.
- The card has no title for duos without a library entry.
- `GetDuoFlow` creates the card canvas on the first QTE duo (as before for insert duos); a missing canvas on the handler logs the existing warning once and keeps the old flow.
