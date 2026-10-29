# Family Role prompt locks when a target is removed during the prompt

Size: S-M    Tier: 3, approved by THJ 2026-10-29 (D-313); core    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all. Built on `thj/linda-quiver` as its own core commit; THJ ports it to `main`.

## Problem

THJ, "A Wolf's Blood" 2/2, round 6 (log `CombatLogs/20261029-173932_A_Wolf’s_Blood.jsonl`, seq 195-200):
1. John's Shield Dash killed a DarkClaw and pushed two DarkWorms; worm offspring had spawned in Linda's line. Linda's Watch prompt came up.
2. On the press: `MissingReferenceException` at `CameraHandler.GetFocusSubjects` (`CameraHandler.cs:274`), from `CameraHandler.Focus(factionRoleFocus)` in `noticeActions` (`PlayerController.cs:1642`).
3. The exception ended the `SequentialActionHandler` coroutine, so `ClearInProgressAndRefreshEndTurn` / `RestoreTimeScale` never ran. **The game locked.**

**Cause:** `PlayerController.ActivateFactionRole` (around 1614-1617) captures `entities` and `factionRoleFocus.focusTransforms` when the prompt opens. A unit among them was destroyed before the press: most likely the dash's kill, or a dying worm. Which one isn't confirmed; the implementer finds out and reports it.

## Fix (minimal, core)

- **Focus and spotlights:** at each use after the prompt (`Focus(factionRoleFocus)` in `noticeActions`, the spotlight `AddSpotlight` loop, and anything else that touches `entities` or transforms after the QTE), drop destroyed or dead entities. Rebuild `factionRoleFocus.focusTransforms` from the living ones right before focusing.
- **No targets left:** after the press, if no living role target remains, take the clean skip path. Release the flow exactly as the decline or could-not-start path does, without silencing. Decide whether the bus outcome event should still say "pressed": keep it, since the player did press, and log it.
- **Check the rest of the chain:** `base.ActivateFactionRole` with a target that died in the meantime must also not throw. Read the role handlers that `FactionRoleHandlerBase` calls (Linda's Watch, John's, Lucy's and Toba's) for the same assumption, and guard at the shared entry point if it's cheap.
- **`CameraHandler.GetFocusSubjects`:** optionally skip null transforms there too, as a defensive fix, since every caller benefits. Keep it tiny and note it in the report.
- **No safety net:** don't catch errors in `SequentialActionHandler`. THJ chose the targeted fix only.

## Acceptance

- [ ] A role prompt whose target (or one of its targets) dies or is destroyed before the press doesn't throw, and the game continues.
- [ ] If every target is gone, the role is skipped and control returns.
- [ ] If some targets remain, the role runs on the living ones and the camera frames them.
- [ ] Normal role prompts are unchanged.
- [ ] EditMode tests for any pure rule extracted (for example, filtering the living focus subjects, or the "no targets left → skip" decision). Known red only.

## Constraints

- Core (`PlayerController`, `CameraHandler`, possibly `FactionRoleHandlerBase`): only this change, in its own commit.
- The editor is open: no batch Unity.
- Leave out of everything:
  - the uncommitted AI diagnostic in `AIFactionBrain.cs` / `AIUnitBrain.cs`;
  - THJ's local edits (GlobalSettings, John's dash asset, PreloadScreen, LevelLucyJohn prefabs, `EditorFPSLimiter`, ProjectSettings, TMP fallback).
- Keep line endings and BOM. No private IDs. Don't touch the AI regression test.

## Play check (THJ)

- Recreate it: an enemy enters Linda's lane while another effect is killing or pushing units (John's dash next to worms is ideal), then press the Watch prompt late. No lock.
- A normal Watch, John's role and Lucy's role still play the same way.

## Commit log

(empty)
