# Report: B4 R1 Mark Family Role QTE binding (F2)

Plan: plans/2026-10-18-family-role-phase0-1.md (R1 only)    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done

## What changed

- miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab line 2786: `MarkFactionRoleHandler.qTEProfile.bindingActionID` `LucyQTE` -> `MarkQTE`. One line, LF kept, no GUID or .meta change.

## Findings (how QTE bindings work)

- `QTEProfile.bindingActionID` (string) is resolved at runtime by `QuickTimeEventHandler` via `PlayerInputController.Instance.GetInputAction(id, ...)`. The key and the prompt icon both come from that action's binding. `inputIcon` on the profile is an optional override (fileID 0 on Mark and Lucy), so no icon asset is needed.
- `InputSystem_Actions.inputactions` already has `JohnQTE`, `LindaQTE`, `LucyQTE` and `MarkQTE`. All four are bound to `<Mouse>/leftButton` (I read each action's path from the file). `MarkQTE` is already used by Mark's "Catch Arrow" profile (`Unit_Mark.prefab:2977`, `PlayerController.prefab:2119`). So a Mark binding existed and nothing needed creating; the Input Actions asset is untouched.
- Result: same key as before, and the prompt now resolves through Mark's own action.

## Acceptance criteria

- [x] Mark's Family Role uses a Mark binding: line 2786 now `MarkQTE`; `git diff` shows exactly 1 insertion and 1 deletion in that file.
- [x] Compiles, no errors: refresh_unity ok, read_console ["error"] returned 0 entries.
- [ ] Prompt visual in play: not play-checked (needs the verifier).

## Save reset

no

## Decisions I made

- Left `Unit_Mark.prefab:2914` (`MarkPassiveAbility_ContinuousAttack`, "Continuous Attack" qteProfile) on `LucyQTE`: it is a different ability, not the Family Role, and the task said to change only the role binding.

## Needs THJ

none (optional: see risks, line 2914).

## Docs to update

- reports/b4-family-role-facts.md: Mark "uses LucyQTE" is now fixed for the role (line 2786); Continuous Attack still on LucyQTE.

## Risks and loose ends

- `Unit_Mark.prefab:2914` Continuous Attack also uses `LucyQTE`. Same key either way (left mouse), so no gameplay change expected; it could be switched to `MarkQTE` for consistency if THJ wants.
- No behavior change in key; only the action object differs. Rebinding a Mark action later now affects the role prompt too.

## Proposed commits

1. fix: Mark Family Role QTE uses MarkQTE binding: `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab` (plain, prefab data only)

## Other branches

none checked.

## How to see it

1. Open `Unit_Mark.prefab`, select the Mark root, find `MarkFactionRoleHandler` > QTE Profile: Binding Action ID reads `MarkQTE`.
2. In a fight, trigger Mark's strike back (enemy attacks another ally within 2 tiles of Mark): the "Activate Passive" prompt appears and responds to left mouse.
