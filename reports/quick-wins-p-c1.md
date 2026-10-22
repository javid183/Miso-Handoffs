# Report: Quick wins P, C1 (non-blocking phase banner)

Plan: plans/2026-10-22-quick-wins-p-pace-tech.md (C1 only)    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (code); play check pending

## What changed

- `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs` (+1 −1, core): `SwitchTurnIE` calls `_uiManager.PlayPhaseAnimation(CurrentFaction);` instead of `yield return _uiManager.ShowPhaseAnimation(...)`. Nothing else in the method changed.
- `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs` (+19 −11, core): new `public void PlayPhaseAnimation(Faction faction)` (hide End Turn panel for non-player, start banner, show End Turn panel for player, no wait). `ShowPhaseAnimation` is now a wrapper: `PlayPhaseAnimation` then `WaitUntil(animationFinished)`. `HideHUD` calls `phaseVisualsUI.HideInstant()` first (replaces the commented-out phaseVisualsUI line; the old `//yield return a;` comment was left as it was).
- `miso/Assets/_Project/Features/UI/Panels/Scripts/PhaseVisualsUI.cs` (+34 −17): both colour branches now call one private `PlaySequence()` (same tweens); new `public void HideInstant()` (kill sequence, snap to `hiddenAnchoredPosition`, `animationFinished = true`); `OnDestroy` kills the sequence; the slide-out tween gets `.SetEase(ease)` itself (it was on the sequence). A private `KillSequence()` kills only when `IsActive()` and nulls the field, so a finished or already-killed sequence never triggers a DOTween warning.

Line endings: all three stay LF. Note: `CombatLevelRunHandler.cs` and `CombatLevelUIManager.cs` **have a UTF-8 BOM** (the brief said no BOM); I kept each file's existing BOM state unchanged. `PhaseVisualsUI.cs` has no BOM and still has none.

## Acceptance criteria (C1's five)

- [x] Next faction's turn starts without waiting for the banner: code path (`StartTurn` runs in the same frame). Needs play check.
- [~] Right faction name and colour: unchanged label/mask code, now through one helper. Side position and ~1 s timing are C3 (prefab values), not done here.
- [x] End Turn panel hides/shows at turn start with no delay; no leftover coroutine waits to reshow it. `UIPanelAnimator.Show/Hide` kill the previous tween, so quick switches take the latest call. Needs play check.
- [x] New banner replaces the old one cleanly: `PlaySequence` kills the running sequence and slides from the current position. Needs play check for warnings.
- [x] Level end hides the banner at once (`HideHUD` -> `HideInstant`); tween killed in `OnDestroy`. Needs play check (win and defeat).

Test coverage: none new (no pure logic extracted, per the plan's Gates). All five need the verifier's play check.

Compile: clean (Unity MCP recompile; no errors; only the existing warnings).
EditMode: 517/518 passed; the only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (untouched).

## Save reset

no

## Decisions I made

- Added a private `KillSequence()` helper (guards with `IsActive()`) used by `PlaySequence`, `HideInstant` and `OnDestroy`; same behaviour as the plan, avoids invalid-tween logs.
- `HideInstant` skips the position snap if `_rectTransform` is null (object never awoke); `animationFinished` is still set.
- Short plain-word comments on `PlayPhaseAnimation`, `ShowPhaseAnimation`, `HideInstant`, `PlaySequence` and the `HideHUD` line. No private IDs.

## Needs THJ

none

## Docs to update

- `tech/core-systems.md`: Level run and Combat UI manager rows: banner no longer blocks the turn switch; `PlayPhaseAnimation` exists, `ShowPhaseAnimation` is a waiting wrapper; `HideHUD` hides the banner instantly.
- `tech/combat-architecture.md`: turn switch sequence (banner runs alongside `StartTurn`).

## Risks and loose ends

- With the prefab still at 0.8 / 1.5 / 0.8 s (until C3), the banner stays on screen ~3 s while the turn already runs; expected until C3 lands.
- Pre-existing, not changed: `UIPanelAnimator`'s `Visible` flag can be set by a superseded Show/Hide coroutine after its tween was killed (the killed coroutine still writes `Visible` when its wait ends). Position is right; only the flag can briefly lag. Worth a look if anything reads `Visible` for the End Turn panel.
- `turnStarted` listeners (dialogs, barks, AI focus) now run while the banner is showing, as the plan's Risks say.

## Proposed commits

1. `feat(combat): the phase banner plays alongside the turn switch instead of blocking it`: `miso/Assets/_Project/Core/Managers/CombatLevelRunHandler.cs`, `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs`, `miso/Assets/_Project/Features/UI/Panels/Scripts/PhaseVisualsUI.cs` (core; one commit since `HideHUD` and the run handler need the new `PhaseVisualsUI`/`PlayPhaseAnimation` APIs)

## Other branches

`thj/home-test` takes this with `main` (per the plan).

## How to see it

1. Open `CombatLevelContainerScene` with any combat level (ideally one with a turn-start dialog) and press Play.
2. End your turn: the "Enemy Turn" banner slides in and the enemy starts acting (camera focus, moves) while it is still on screen; the End Turn panel slides away at once.
3. When the enemy turn ends, the "Player Turn" banner shows and the End Turn panel slides back in at the same time; your units are selectable right away.
4. Do several quick switches (a side with nothing to do): the banner restarts cleanly, no stuck banner, no DOTween warnings in the Console.
5. Win and lose a level: the banner disappears at once when the level ends and never slides over the end screen.
