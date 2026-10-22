# Pace timings

Owner: coordinator. Where every combat-pace wait lives, what it does, and what changing it affects. Started 2026-10-22 from quick wins bundle P (`plans/2026-10-22-quick-wins-p-pace-tech.md`, D-107, D-141 to D-144). Update this file when a timing is added, moved or retuned.

Paths are under `miso/Assets/_Project/`. "Scaled" waits stop when `Time.timeScale` is 0 (pause menu, tutorials) and slow down with it (slow-motion); "real time" waits don't. Values checked against `thj/quick-wins` @ `7d4cd90ca` (2026-10-22). Bundle P is on `thj/quick-wins` only until it merges into `main`; `main` @ `fc731b0c5` still has the old values.

## The order of one turn switch

`FactionControllerBase` (last action) → hold after action → `CombatLevelRunHandler.SwitchTurnIE`: wait for actions, sequences and turn-switch holds → `EndTurn` → gap between faction turns → choose next faction → turn-start pause (only after an automatic end) → banner starts **and** the next turn starts in the same frame → on the player's turn, input stays locked until the banner ends.

## Turn flow

| What | Value | Where to change it | Kind | Affects | Notes |
| --- | --- | --- | --- | --- | --- |
| Hold after each AI action | **0.25 s** | `Content/Controllers/AIController.prefab` → `holdTimeAfterActionCompletion` (field on `FactionControllerBase`) | Inspector, real time | Every enemy action; the pause before the next enemy acts | Set in bundle P (was 0.5) |
| Hold after each player action | 0.5 s | `Content/Controllers/PlayerController.prefab` → `holdTimeAfterActionCompletion` | Inspector, real time | Every player action, before the next selection | Untouched |
| Hold after each auto-player action | 0.5 s | `Content/Controllers/AutoPlayerController.prefab` → `holdTimeAfterActionCompletion` | Inspector, real time | Dev auto-player only | Untouched |
| Delay before an automatic end-turn request | 0.1 s | `Core/Interactions/Runtime/FactionControllerBase.cs` (`ExecuteWithDelay(RequestEndTurnSafe, CustomRealTime, .1f)`, in the action-completion callback) | Code, real time | When a faction has no units left to play | Untouched |
| AI wait after camera focus | 0 s | `AIController.prefab` / `AutoPlayerController.prefab` → `waitTimeAfterFocus` | Inspector, scaled | Before each AI unit plans | Untouched |
| Gap between faction turns | **0.25 s** | `Scenes/CombatLevelContainerScene.unity` (and `Scenes/DevScenes/TestLevel.unity`) → the level run handler (`GameSessionHandler` object) → `timeBetweenFactionTurns` | Inspector, scaled | Every turn switch, both sides, End Turn included | Set in bundle P (was 0.5) |
| Turn-start pause, enemy | **0.5 s** | `AIController.prefab` → `turnStartPause` (field on `FactionControllerBase`) | Inspector, scaled | Before the enemy's banner when the player's turn ended on its own (out of AP); skipped after the End Turn button | Added in bundle P (D-143) |
| Turn-start pause, player | 0 s | `PlayerController.prefab` → `turnStartPause` (code default) | Inspector, scaled | Before the player's banner; the enemy never presses End Turn, so it always applies if set | If raised, the player can't act during it (End Turn refused, input on Camera and Pause) |
| Turn-switch hold watchdog | 5 s | `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs` → `TurnSwitchHoldSet.TimeoutSeconds` | Code const | Safety net: a turn-switch hold (Masher answers) is dropped after 5 s | Holds are only checked before `EndTurn`, not during the gap or pause |
| New-stage objective re-check | 0.05 s | `CombatLevelRunHandler.cs` → `NewStageEvalEpsilon` | Code const | Objectives re-evaluated after a stage sequence | Untouched |

## Turn banner (`Features/UI/Panels/Prefabs/UI/PhaseVisuals.prefab`, script `Features/UI/Panels/Scripts/PhaseVisualsUI.cs`)

The `CombatLevelContainerScene` instance overrides some of these; check the scene instance before the prefab.

| What | Value | Where to change it | Kind | Affects | Notes |
| --- | --- | --- | --- | --- | --- |
| Slide in / slide out | **0.25 s** each | `animationDuration` (prefab **and** a scene override) | Inspector, scaled | Banner length; on the player's turn, how long input stays locked | Was 0.8 |
| Hold on screen | **0.5 s** | `waitTime` (prefab; scene override 0.5) | Inspector, scaled | Same as above | Was 1.5. Total ≈ 1 s |
| Ease | `ease` (4) | `ease` | Inspector | Both slides | Since C1 both slides use it |
| Side | Right | `side` (Left/Right), scene override | Inspector | Mirrors anchors, pivot and the shown/hidden x at scene load | Takes effect on the next scene load, not mid-Play |
| Shown / hidden position | (−16, −260) / (+760, −260) | `shownAnchoredPosition` / `hiddenAnchoredPosition` (prefab) and the root RectTransform overrides in the scene | Inspector | Where the banner rests and starts | Authored for Right; Left mirrors them |
| Input lock during the player's banner | banner length | `Core/UI/Runtime/CombatLevelUIManager.cs` → `PlayPhaseAnimation` (existing input lock) | Code | No unit, ability, target or End Turn input; camera and Esc locked too | Enemy banners take no lock |
| Unused `UIPanelAnimator` on the banner root | 0.5 s, old positions | Same prefab | Inspector | Nothing calls it | Dead config |

A tutorial that opens at turn start sets the time scale to 0, so the banner (and the player's input lock) pauses until the tutorial closes.

## End of a level (`CombatLevelRunHandler.EndLevel`)

Order: objectives met → wait → HUD hides → wait → outro sequence → rewards → wait → end panel.

| What | Value | Where to change it | Kind | Affects | Notes |
| --- | --- | --- | --- | --- | --- |
| Before the HUD hides | **0.25 s** | Level run handler → `endLevelDelayBeforeHudHide` | Inspector, scaled | Win, defeat, mission complete | Was 0.5 hard-coded |
| HUD hide | ≈ 0.5 s | Each HUD panel's `UIPanelAnimator.animationDuration` (see HUD panels below) | Inspector, scaled | Panels slide out in parallel | A second hide (from the outro) is instant: the duration scales with the distance left |
| After the HUD hides | **0.25 s** | Level run handler → `endLevelDelayAfterHudHide` | Inspector, scaled | Before the outro or end panel | Was 0.5 hard-coded |
| Outro sequence | per level | The level prefab's `outroSequence` (`Resources/Sequences/<Mission>/<Level>/*_End_SequenctialSequence.asset`) | Asset | Most start with `Common/IntroCutscene` (input off, grid fade out 0.8 s, HUD hide), then the end dialog | `Level1C1-2_End` uses `OutroCutsceneKeepGridHidden` |
| Dialogue panel slide out after the last line | 0.5 s | `Features/UI/Panels/DialogPanel/DialoguePanel.prefab` → `UIPanelAnimator.animationDuration` (two animators) | Inspector, scaled | Every dialog sequence's end waits for it (`DialogNodeSequence`) | Untouched; all dialogs, not just level ends |
| Pause between dialog lines | 0 s | `Core/Levels/Runtime/DialogNodeSequence.cs` → `DIALOGUE_DELAY` | Code const | Every dialog | Untouched |
| Before the end panel | **0.25 s** | Level run handler → `endLevelDelayBeforeEndPanel` | Inspector, scaled | After the outro, before win / defeat / mission-complete panel | Was 1 s hard-coded (D-144) |

The level run handler fields live on the `GameSessionHandler` object in `CombatLevelContainerScene.unity` (and `TestLevel.unity`).

## Sequences (`Resources/Sequences/Common/`)

| Asset | Steps | Time |
| --- | --- | --- |
| `IntroCutscene` | Input off → grid fade out → HUD hide | Grid fade 0.8 s (`FadeOutGridSequence.duration`) |
| `OutroCutscene` | Input on → grid fade in → HUD show | Grid fade 0.8 s (`FadeInGridSequence.duration`); ends intro/mid cutscenes, not used as a level outro |
| `OutroCutsceneKeepGridHidden` | Input on → HUD show | HUD slide |
| `HideHUDSequence` / `ShowHUDSequence` | `HUDSequence` (`show`, `instant`) | HUD slide; a hide also hides the turn banner at once |

## HUD panels (`UIPanelAnimator.animationDuration`)

All 0.5 s, untouched: `EndTurnPanel.prefab`, `HUD/AbilitiesHUD.prefab`, `HUD/UnitPanel.prefab` (two), `Level Info Panel.prefab`, `ObjectivesPanel.prefab` (all under `Features/UI/Panels/Prefabs/UI/`). They drive the HUD hide/show at level start, level end and in cutscenes. `UIPanelAnimator.Visible` can go stale after a quick hide then show (backlog; only the dev HUD toggle reads it).

## Camera

| What | Value | Where to change it | Kind | Affects |
| --- | --- | --- | --- | --- |
| Default focus duration | 0.5 s | `CameraHandler.focusDefaultDuration` on `Content/Levels/LevelBase.prefab` (level variants may override; also `TestLevel.unity`) | Inspector | Every camera focus (AI unit focus, auto-select); the AI waits for focus before planning |
| Override focus expiry | 3 s | `CameraHandler.overrideFocusWaitExpiration`, same place | Inspector | How long a forced focus holds |
| Enemy introduction focus | 0.5 s | `PlayerController.prefab` → `EnemyIntroductionController.focusDuration` | Inspector | Enemy intro camera moves |

## Loading

| What | Value | Where to change it | Kind | Affects | Notes |
| --- | --- | --- | --- | --- | --- |
| Minimum loading screen time | **0.5 s** | `Scenes/PreloadScreen.unity` → `ProgramFlowHandler.minimumLoadingTime` | Inspector | Every scene load **in player builds only** (the editor skips it) | Was 1.5 |
| Preload (splash) screen time | 3 s | `PreloadScreen.unity` → `ProgramFlowHandler.preloadScreenShowTime` | Inspector | Game start | Untouched |

## Player-only sequences (code, real time unless noted)

`Core/Interactions/Runtime/PlayerController.cs` has hard-coded steps in its Super Time and spotlight sequences (around lines 1610–1720): spotlight hide 0.2 s, camera focus 0.3 s, splash unload 0.7 s (scaled), focus 0.6 s, target-selection anim 0.5 s, zoom 0.3 s (scaled). The reactive interrupt (`reactiveInterruptCooldown` 0.5 s on `PlayerController.prefab`) is ATB-only and does nothing on FTP (`main`).

## Not yet built

A fast-forward toggle for enemy turns (D-107: later, M). It would need the real-time waits above (`holdTimeAfterActionCompletion`, the 0.1 s end-turn delay, the player sequences) scaled with it.
