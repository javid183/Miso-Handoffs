# B4 / Q7 · Family Roles under FTP: facts from code

Read-only Explore pass, 2026-10-18, branch `thj/oct-build-fixes` (= `main` @ `97538642c`, FTP). Condensed by the coordinator; line numbers are the agent's. Paths under `miso/Assets/_Project/`. Input for the designer; not a decision. Rules as designed: GDD `design/gdd/family-systems.md`, D-036 to D-042.

## Shared pipeline

- Events become `GlobalEventBus.onActionFlowEvent`; `CombatLevelRunHandler.CheckFactionRoleAbilities` (:919-932) asks each controller to `ApplyFactionRolesIfPossible` and stops at the first that returns true. Roles are enabled only on `Content/Controllers/PlayerController.prefab`.
- **Prefab data per role** (from `Unit_<Name>.prefab`): John fires OnActionStart, Immediately, game paused (`requiredTimeScale 0`); Linda OnUnitEndMoving, wait-for-processes, real time; Lucy OnActionComplete, wait-for-processes; Mark OnActionComplete, enemy turns only, wait-for-processes. All `requiredFTP` 1, `oncePerPhase` 0, cooldown 0, QTE TimedPress ("Activate Passive", 1 s, unscaled).
- **Cost check before the QTE** (`FactionControllerBase.cs:169-180`): needs shared FTP >= 1. If not, nothing happens: no QTE, no log, no message. **Charge after a successful QTE** (:196-201): `TryConsume` result ignored, so the role fires free if the pool dropped meanwhile. A missed QTE costs nothing.
- **No AP, no cooldown, no charges, no per-round limit** are checked on roles. The cooldown is never consulted (`FactionRoleHandlerBase.cs:98` uses `CheckActivationFeasibility`, not `RuntimeAbility.Active`). **D-042's note "the cooldown may already give 1 charge" does not hold in code.** `ActivatedAtThisPhase` is set but unused and is reset on every faction's `turnEnded` (:86), not at the player turn start (D-039).
- **Dispatch:** John (Immediately) tries units in turn order, first feasible fires. Linda, Lucy, Mark go on a wait list processed at `ActionsProgressComplete`: iterates from the end, fires the first feasible only, clears the rest (`FactionControllerBase.cs:142-166`). So only one of the three gets a QTE per event; the others are dropped silently.
- **Base guard** (`FactionRoleHandlerBase.cs:90-99`): blocked if the last completed action was the role unit's own or targeted the unit or its cell.
- **Silencing:** after a miss, the same targets are suppressed for the rest of that enemy turn (`SilencedTargets`, cleared only on unit selection change). No feedback.
- **QTE flow** (`PlayerController.cs:1492-1566`): pause per role, camera focuses the role unit and targets, prompt shows, 1 s window. If another QTE is already active, `StartEvent` returns false and the role is silently skipped (:1556-1561). Press: spotlight, solo insert panel (`FactionRoleVisual.ShowSoloPanel`), effect, FTP charged. Miss: only the QTE "Miss" animation; game unpauses.

## Per role

| Role | Fires when (as coded) | Silent non-fire reasons (besides FTP < 1 and a QTE already active) | Feedback today |
| --- | --- | --- | --- |
| **John** "I got you" | Enemy turns only. An enemy action targets an ally (any effect, not only damage) inside John's Adjacent radius-2 diamond of his single anchor cell (diagonal neighbour = 2 steps, inside; (2,1) and (2,2) outside). Not for himself, not for his own role. Takes a x0.5 damage modifier for 1 duration, ally removed from targets | Player or ally turn; no ally target in the diamond or tag mismatch; last action was his or targeted him; missed earlier QTE on that ally this enemy turn; no stun check found | Game pauses, prompt, shield FX, insert panel, one log line "Family Role: John's FR". Barks "No!" / "I got you!" exist on the prefab but nothing plays them. Nothing when he can't |
| **Linda** arrow | Any turn. A hostile unit **ends a walk, push or Command move** on a cell sharing her row or column, within stat radius (4; 6 with Longshot). No line of sight; **diagonals never count**; **teleports and jumps raise no event** (`AEffectTransporter.cs:243,294`). No per-round or per-enemy cap | Enemy diagonal or off-lane; teleport/jump; last action was hers or targeted her; deferred check finds the enemy moved again or died; another role fired first and her wait-list entry was dropped; missed earlier QTE for that enemy | Real-time prompt (not paused), insert panel, log line. Lane highlight only on hover of the panel icon. Nothing when she can't |
| **Lucy** ember | Any turn. A family action completes (not Lucy's, not the blacklisted Linda–Lucy Duo) and an enemy tied to it is within her radius-3 Adjacent diamond; picks the first match in list order of the first hostile faction only; skips an enemy she hit last | No enemy tied to the action in range; every candidate was hit by Lucy last; second hostile faction ignored; wait list dropped her; last action targeted her | Prompt, insert panel, log line; nothing otherwise |
| **Mark** strike back | Enemy turns only. An enemy action targets an ally other than Mark; the attacker's **anchor cell** is inside Mark's radius-2 Adjacent diamond; reuses Fist Blitz (no AP charged) | **The same action also targeted Mark** (blocks him, likely unintended); attacker dead/downed or its anchor just outside range (big enemies); Fist Blitz target rule rejects (immune); wait list dropped him | Prompt on **`LucyQTE`** (Lucy's key and icon: likely a copy-paste), insert panel, log line |

## HUD

- Panel icon + tooltip with range highlight on hover only (`UnitPanelUI.cs:235-287`), FTP bar (`FTPIndicator`), combat log line on success. **Not found:** any ready / can't-afford / no-valid-trigger state, uses-left readout, skipped or missed log line, role barks, "FTP low" warning. Enemies have `ShowReactionPreview` (Masher Goblin :367); family roles don't.

## Likely confusion causes

1. One shared FTP pool with no refill except pass-by and items: roles stop silently when it is empty, and the player cannot tell "no FTP" from "no trigger".
2. Linda's lane is row/column only (an enemy at diagonal distance 2 never triggers her while it would trigger John and Mark); teleports and jumps never trigger.
3. One role per event and one QTE at a time: the others are dropped without a message; a missed press silences that enemy for the turn.
4. John's diamond ignores his footprint, triggers on any enemy action against an ally, and gives no cue until the paused prompt.
5. No feedback on non-fire or on a miss; the camera and prompt appear before the press, so a miss looks like "nothing happened".

## Bugs and risks seen

1. Possible null: `Targets.Except(SilencedTargets)` (`FactionRoleHandlerBase.cs:116`) with `SilencedTargets` null before the first selection change (unverified).
2. FTP checked, not reserved: result of `TryConsume` ignored.
3. D-042 premise wrong (see above); a per-round counter must be new code; `oncePerPhase` resets on any faction's turn end.
4. ATB-only code dormant under FTP (`PlayerController.cs:388-394`, `HandleReactiveInterrupt` early-returns).
5. Mark blocked when the triggering action also targeted him; Mark checks the attacker's anchor only; Mark uses `LucyQTE`.
6. Lucy searches only the first hostile faction and takes list order, not nearest.
7. `LastActions[0]` is the oldest completed action since the last activation.
8. GDD Q7 note: pass-by and Family Trinket may add 0 FTP (float to int); then the pool only drains. Check the console for "Failed to call function ProduceFTP". Not verified.

## Hooks for a "why not" popup and a diagonal indicator

- Reasons are decided in `FactionControllerBase.ActivateFactionRoleIfFeasible` (:169-180) and `FactionRoleHandlerBase.CheckFeasibility` / `CheckTriggerConditions` and each handler's `PrepareTargets`: all return plain bools, so no reason exists. A popup needs a reason code from the handlers (core, Family Roles: Tier 3).
- Events: `onFamilyRoleActivated` (success only), `onActionFlowEvent`, `qteStarted` / `qteEnded`. A "role skipped" event would be new on the bus (additive, public).
- Diagonal geometry comes from the preset's `cellApplyTraverseMode` (Adjacent = 4-direction on all four presets); Linda hardcodes Radial plus the row/column filter (`LindaFactionRoleHandler.cs:23-32`). The indicator is hover-only today (`UnitPanelUI.SetupFamilyRole`).
- **Core (Tier 3 to change behaviour/API):** `FactionRoleHandlerBase` and the four handlers, `RuntimeAbility`/`AbilityOrchestrator`, `FactionControllerBase`/`PlayerController`/`FactionPhaseState`, QTE classes, `CombatLevelRunHandler`, `FamilyTimePoints`/`PointConsumer`, `GlobalEventBus`, `CombatLevelUIManager`. **Not core:** `UnitPanelUI`, `FactionRoleVisual`, `FTPIndicator`, `QTEButton`, combat log (listens only), barks, prefab data.
- Cheapest UI-only additions: FTP-low / ready badge on `UnitPanelUI`; a combat-log line for misses.
