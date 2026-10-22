# Quick wins bundle P: pace (Q3, Q4, Q23)

Size: S/M    Tier: 3 (feel values and core turn flow; decided in D-107)    Assigned to: miso-implementer
Branch: all (built on `main` @ `fc731b0c5`; `thj/home-test` gets it when it takes `main`)
Status: approved 2026-10-22 (D-141; P1: right edge, upper third). C1 in progress

## Why

Playtests found combat slow between actions (`playtests/2026-10-playtest-tasks.md` Q3, Q4, Q23; triage `plans/2026-10-20-quick-wins-triage.md`). THJ set the numbers in D-107: loading pad 1.5 → 0.5 s; EndLevel waits ~2 → ~1 s; AI hold after each action 0.5 → 0.25 s; gap between faction turns 0.5 → 0.25 s; the phase banner runs alongside the turn switch (non-blocking), about 1 s, at the screen's side. The fast-forward toggle is a later M, not this plan.

## Goal

Cut the dead time between turns, after enemy actions and at the end of a level, without changing any combat rule.

## What the code does now (read 2026-10-22)

- **Phase banner.** `CombatLevelRunHandler.SwitchTurnIE` (`Core/Managers/CombatLevelRunHandler.cs:455-499`) does `yield return _uiManager.ShowPhaseAnimation(CurrentFaction)` before `StartTurn()`. `CombatLevelUIManager.ShowPhaseAnimation` (`Core/UI/Runtime/CombatLevelUIManager.cs:188-208`) hides the End Turn panel for non-player factions, calls `PhaseVisualsUI.UpdateValues`, **waits for `animationFinished`**, then shows the End Turn panel for the player. `PhaseVisualsUI` (`Features/UI/Panels/Scripts/PhaseVisualsUI.cs`) is a DOTween sequence: slide in `animationDuration`, hold `waitTime`, slide out. Prefab values (`Features/UI/Panels/Prefabs/UI/PhaseVisuals.prefab:66-70`): ease 4, hidden (0, 200), shown (0, −25), duration 0.8, wait 1.5, so the banner **blocks about 3.1 s** per turn switch (the triage's 2.1 s was low). The root is anchored top-centre, 570 × 170, scaled 1.3 by the `CombatLevelContainerScene` instance. The same root also carries a `UIPanelAnimator` (duration 0.5) and the `InfoPanel`/`LevelNameLbl` children.
- **Gap between faction turns.** `timeBetweenFactionTurns` waits after `EndTurn()` (`CombatLevelRunHandler.cs:467`). Scene values 0.5 in `Scenes/CombatLevelContainerScene.unity:1439` and `Scenes/DevScenes/TestLevel.unity:1576`.
- **Hold after each action.** `FactionControllerBase.holdTimeAfterActionCompletion` (real time, `FactionControllerBase.cs:983`). 0.5 in `Content/Controllers/AIController.prefab:47`, `PlayerController.prefab:202` and `AutoPlayerController.prefab:47`. D-107 changes the AI only. `AIController.waitTimeAfterFocus` is already 0.
- **EndLevel.** `CombatLevelRunHandler.EndLevel` (`:657`): hard-coded `WaitForSeconds(0.5f)`, `HideHUD()` (four panel animators in parallel), `WaitForSeconds(0.5f)`, then the outro.
- **Loading pad.** `ProgramFlowHandler.minimumLoadingTime` (`Core/ProgramFlow/Runtime/ProgramFlowHandler.cs:25, 209`), 1.5 in `Scenes/PreloadScreen.unity:1170`. It only applies in player builds (`#if UNITY_EDITOR` skips it), so it **can't be seen in the editor**.

## Acceptance criteria

- [ ] On every turn switch the next faction's turn starts (units selectable, AI starts planning, `turnStarted` fires) without waiting for the phase banner.
- [ ] The banner still shows the right faction name and colour (blue for the player, red otherwise), at the side position from P1, and takes about 1 s in total (0.25 in, 0.5 hold, 0.25 out).
- [ ] The player's End Turn panel hides at the start of a non-player turn and shows at the start of the player's turn, with no delay; it never reappears during an enemy turn when turns switch quickly (for example a faction with nothing to do).
- [ ] When a new banner starts before the old one has finished, the old one is replaced cleanly (no stuck banner, no DOTween warnings).
- [ ] When the level ends, the banner is hidden at once and does not slide over the end screen; the banner's tween is killed when the object is destroyed.
- [ ] The gap between faction turns is 0.25 s in `CombatLevelContainerScene` and `TestLevel`.
- [ ] The AI holds 0.25 s after each action (`AIController.prefab`); the player's and auto-player's holds stay 0.5 s.
- [ ] EndLevel's two waits are serialized fields on `CombatLevelRunHandler`, default 0.25 s each (total about 1 s with the HUD hide); win, defeat and mission-complete flows still reach their outro and panels.
- [ ] `minimumLoadingTime` is 0.5 in `PreloadScreen.unity`.
- [ ] Compile clean; EditMode suite green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: the non-blocking banner (core code), banner timing and side position (prefab), the EndLevel waits as fields (core code), the four tuning values (prefab/scene).
Out: the fast-forward toggle (later M); the player's own action hold; camera focus speed; `UIPanelAnimator` timings of the other HUD panels; any combat rule.

## Touches

Systems: Level run (core: `CombatLevelRunHandler.cs`), Combat UI manager (core: `CombatLevelUIManager.cs`), `PhaseVisualsUI` (not core), Faction controllers (core, **prefab value only**), `ProgramFlowHandler` (scene value only).
USPs: none directly (Family Roles react on `turnStarted`, which now fires earlier; see Risks).
Docs: `tech/core-systems.md` (Level run and Combat UI manager rows: banner no longer blocks; EndLevel wait fields), `tech/combat-architecture.md` (turn switch sequence), GDD only if a page names the banner timing (check `design/gdd/combat-rules.md`). Owner: coordinator.

## Approach

Three chunks, one commit each, so the core flow change can be reverted alone. Order: riskiest first.

### C1. Non-blocking phase banner (core, `opus`)

Files: `Core/Managers/CombatLevelRunHandler.cs` (or a new partial `CombatLevelRunHandler.PhaseBanner.cs` if it reads cleaner), `Core/UI/Runtime/CombatLevelUIManager.cs`, `Features/UI/Panels/Scripts/PhaseVisualsUI.cs`.

1. `CombatLevelUIManager`: add `public void PlayPhaseAnimation(Faction faction)` that does what `ShowPhaseAnimation` does **without waiting**: hide the End Turn panel for a non-player faction, start the banner, show the End Turn panel for the player, all at once. `SwitchTurnIE` is `ShowPhaseAnimation`'s only caller (grep 2026-10-22); keep it as a thin wrapper that calls `PlayPhaseAnimation` and then waits for the banner, so a future caller can still block on it.
2. `SwitchTurnIE`: replace `yield return _uiManager.ShowPhaseAnimation(CurrentFaction);` with `_uiManager.PlayPhaseAnimation(CurrentFaction);` and go straight on to `StartTurn(); Tick(); UpdateObjectives();`. Nothing else in the method changes.
3. `PhaseVisualsUI`:
   - fold the two duplicated colour branches into one helper (same tweens) so both use the same sequence code;
   - add `public void HideInstant()`: kill the sequence, snap to `hiddenAnchoredPosition`, set `animationFinished = true`;
   - kill the sequence in `OnDestroy` (avoids DOTween warnings on scene unload);
   - fix the existing misplaced `.SetEase(ease)` on the slide-out (it is applied to the sequence, not the tween), so in and out use the same ease.
4. `CombatLevelUIManager.HideHUD`: call `phaseVisualsUI.HideInstant()` first (replaces the commented-out line), so a banner mid-slide is gone when the level ends.

Acceptance: the first five criteria. This is a behaviour change of a core system, already decided by THJ (D-107).

### C1b. No player grid interaction until the player's banner ends (core, `opus`; D-142)

THJ play-tested C1: good, but on the **player's** turn no grid interaction may happen before the banner has finished: no unit selection, ability selection (bar buttons and hotkeys), target selection or confirmation. The whole player input (camera too) is locked for that time, using the existing input lock. Enemy turns are unchanged (they start and play under the banner).

- Use the existing `PlayerInputController.AddInputLock` / `RemoveInputLock` (THJ 2026-10-22: locking the camera too is fine; no new lock type). Check the ability bar's buttons and hotkeys respect it; report any that don't.
- `CombatLevelUIManager.PlayPhaseAnimation` takes the lock when the faction is the player's and releases it when the banner finishes, when `HideInstant` runs, or when another banner replaces it. The release must happen on every path (no stuck lock).
- Acceptance: during the player's banner, clicks on units, cells and ability buttons and ability hotkeys do nothing; the moment the banner ends everything works; enemy turns behave as in C1; a level that ends or hides the HUD mid-banner leaves no lock behind.

### C1c. Turn-start pause after an automatic turn end (core, `opus`; D-143)

THJ play-tested C1b: when the player's turn ends on its own (last AP spent), the enemy turn starting right away is confusing. Add a short pause, set per faction, skipped when the turn was ended with the End Turn button.

- `FactionControllerBase`: a serialized `turnStartPause` (seconds, tooltip in plain words: the pause before this faction's turn when the previous turn ended on its own, skipped after End Turn), default 0 in code. A flag that the turn was ended with the End Turn button, set by a new public method (e.g. `EndTurnFromButton()` that sets the flag then calls `ForceEndTurn()`), cleared at the start of the faction's next turn and whenever it would otherwise go stale (restart, level end).
- `CombatLevelUIManager`: the End Turn panel subscribes the new method instead of `ForceEndTurn`.
- `CombatLevelRunHandler.SwitchTurnIE`: after the shared `timeBetweenFactionTurns` wait and after the next faction is chosen, if the ended faction's controller did not end by the button and the next controller's `turnStartPause` > 0, wait that long (scaled time, like the gap), then re-check `_levelEnded` before the banner and `StartTurn()`. The banner and the turn start come after the pause, unchanged.
- Prefabs: `AIController.prefab` `turnStartPause: 0.5`; `PlayerController.prefab` 0 (the code default; write it explicitly only if the prefab needs the line). `AutoPlayerController.prefab` stays 0.
- Acceptance: player turn ends by running out of AP → ~0.75 s (0.25 gap after C3 + 0.5) before the enemy banner; player presses End Turn → no pause beyond the gap; enemy turn ends → no extra pause before the player's banner; a level that ends during the pause doesn't start a turn; End Turn still locked during the player's banner (C1b).
- Tests: EditMode for any pure logic extracted (e.g. a static "pause for this switch" function taking ended-by-button and the pause value); otherwise none.

### C2. EndLevel waits as fields (core, `sonnet`)

File: `Core/Managers/CombatLevelRunHandler.cs` (fields next to `timeBetweenFactionTurns`).

- Add `[SerializeField] private float endLevelDelayBeforeHudHide = 0.25f;` and `[SerializeField] private float endLevelDelayAfterHudHide = 0.25f;` with tooltips in plain words, and use them in place of the two `WaitForSeconds(0.5f)` in `EndLevel`. The scenes have no saved value for the new fields, so the initialisers apply; do not edit the scenes for this.

Acceptance: the EndLevel criterion.

### C3. Pace values (data, `sonnet`)

Small YAML edits (one line each), in THJ's open editor's project. Prefer editing in the Inspector or a one-off editor script if the editor has the scene open with unsaved changes; otherwise a text edit of the exact line is fine.

| File | Field | From | To |
| --- | --- | --- | --- |
| `Content/Controllers/AIController.prefab:47` | `holdTimeAfterActionCompletion` | 0.5 | 0.25 |
| `Scenes/CombatLevelContainerScene.unity:1439` | `timeBetweenFactionTurns` | 0.5 | 0.25 |
| `Scenes/DevScenes/TestLevel.unity:1576` | `timeBetweenFactionTurns` | 0.5 | 0.25 |
| `Scenes/PreloadScreen.unity:1170` | `minimumLoadingTime` | 1.5 | 0.5 |
| `Features/UI/Panels/Prefabs/UI/PhaseVisuals.prefab:69-70` | `animationDuration` / `waitTime` | 0.8 / 1.5 | 0.25 / 0.5 |
| `PhaseVisuals.prefab` root + the scene instance override | anchors, `hiddenAnchoredPosition`, `shownAnchoredPosition`, `UIPanelAnimator` positions | top-centre | side per P1 |

Before editing, check no level prefab or scene overrides these fields (a grep on 2026-10-22 found none besides the lines above). The banner move is the only non-trivial edit: the scene instance in `CombatLevelContainerScene.unity` (around line 6415) overrides the root's anchors, pivot, size and scale 1.3, so set the new layout on the **scene instance** (or remove those overrides and set it in the prefab, whichever leaves the smaller diff) and say which in the report. The `InfoPanel`/`LevelNameLbl` children move with the root; check they still read well.

Also (from the C1 review): the banner must not catch clicks. Its Images and TMP texts have Raycast Target on, and now that the turn starts under the banner, `PlayerController`'s click and hover checks (`IsPointerOverGameObject`) swallow input there. Add a CanvasGroup with `blocksRaycasts = false` (interactable off) on the PhaseVisuals root, or turn Raycast Target off on its graphics; say which in the report.

Acceptance: the remaining value criteria, and grid cells under the banner take clicks and hovers while it shows.

## P1. Question for THJ (layout, Tier 3)

**Answered (D-141): right edge, upper third.** Which side should the banner sit on? Recommended: **right edge, upper third**, sliding in from off-screen right (hidden x ≈ +width, shown x ≈ −16 from the right edge), because the left and top hold the level info and objectives. Alternative: left edge, below the objectives panel. The implementer checks for overlap with the objectives panel, unit panel and End Turn panel in the Game view at 16:9 and 4:3 and reports.

## Risks

- **Things now happen during the banner.** `turnStarted` listeners (`BarkManager`, `RoleBarkPresenter`, `RoleZonePresenter`, `LevelSpecificBehaviour` tutorials and dialogs, `AIController.UpdateFutureTargetsOnTurnStart`, units' turn ticks) now fire while the banner is on screen, and the AI's camera focus starts at once. That is the point of D-107, but a turn-start tutorial or dialog will overlap the banner; moving the banner to the side keeps it clear of the dialog panel (bottom). The play check looks at a level with a turn-start dialog.
- **Stale End Turn panel.** Today an old `ShowPhaseAnimation` coroutine can still be waiting when the next switch starts. C1 removes the wait, so the panel is set in the same frame as the turn starts; no coroutine is left behind.
- **Statics:** none added. **AI thread:** nothing the AI reads changes; `AIRegressionTest` is not touched and stays known red. **Serialized renames:** none (only new fields with initialisers). **Saves:** unchanged. **Branches:** `thj/home-test` takes this with `main`.
- **Loading pad** only shows in a build; the editor play check can't verify it.
- **Line endings:** `CombatLevelRunHandler.cs`, `CombatLevelUIManager.cs` and `PhaseVisualsUI.cs` are LF (checked 2026-10-22); keep them. C1 and C2 each get their own commit.

## Gates

- Compile clean after each chunk.
- EditMode suite (known red only). No new EditMode tests: the change is coroutine timing and tween values in MonoBehaviours with no logic that runs outside Play; the reviewer and the play check cover it. (If the implementer extracts any pure logic, it gets a test.)
- Reviewer: C1 and C2 (core).
- Play check (THJ's time, about 10 minutes): clicking and hovering grid cells under the banner at the start of the player's turn; a level whose turn-start sequence hides the HUD (the banner goes with it: OK, or keep it?); a level with a turn-start dialog, several player/enemy switches including quick ones, an enemy turn with many actions, a win and a defeat. Feel check: is the new pace right?
- Docs: `tech/core-systems.md`, `tech/combat-architecture.md`, build log, status.

## Commit log

(filled in as chunks are committed)

- C1: committed `5d1456ea3`; built (`reports/quick-wins-p-c1.md`), review APPROVE (`reports/quick-wins-p-c1-review.md`), EditMode 517/518 (known red only).
- C3: committed `e2c9bbf68` after THJ's play test (banner position good); built (`reports/quick-wins-p-c3.md`; 5 data files; also set the scene's existing `animationDuration` override 0.8 → 0.25; banner shown (−16, −260), hidden (+760, −260) from the right edge; CanvasGroup with raycasts off; the root's `UIPanelAnimator` is unused and left at the old positions), EditMode 521/522 (known red only). The Unity MCP stopped answering after the last refresh, so the final console read is missing. Objectives panel may overlap the banner's top ~20 px with three objectives (one wrapped). Waiting on THJ's play test, then the commit.
- C2: committed `b0e58f6f6` after THJ's play test; built (`reports/quick-wins-p-c2.md`; one file, two fields replace the hard-coded waits), EditMode 521/522 (known red only). Reviewed by the coordinator (a two-value swap; no reviewer run). Checked with THJ: level outros start with `IntroCutscene` (input off, grid fade out 0.8 s, HUD hide); the second HUD hide is instant because `UIPanelAnimator.Hide` scales by distance left. `OutroCutscene.asset` closes intro/mid cutscenes and isn't used as a level outro.
- C1c: committed `ff0a9f70f` after THJ's play test; built (`reports/quick-wins-p-c1c.md`), review APPROVE (`reports/quick-wins-p-c1c-review.md`; should-fix for the dev auto-player in the backlog), EditMode 521/522 (known red only).
- C1b: committed `fd52cc377` after THJ's play test (incl. End Turn locked during the banner); built (`reports/quick-wins-p-c1b.md`; existing input lock per banner, ability bar checks the lock), review APPROVE (`reports/quick-wins-p-c1b-review.md`), EditMode 517/518 (known red only). Waiting on THJ's play test, then the commit. Open: End Turn during the banner (THJ). The L reaction key is ATB-only and returns at once on FTP, so no gate is needed on `main`.
