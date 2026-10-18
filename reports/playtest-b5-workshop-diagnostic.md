# Report: B5 Workshop diagnostic + hardening (chunk C6)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (B5 is NOT claimed fixed; cause unconfirmed, waiting for THJ's repro)

## What changed

- `miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs` (LF, no BOM, kept):
  - Lock expression moved unchanged into `RefreshLock()`. Called from Awake, OnEnable, and the start of OnPointerEnter/Exit/Down. It re-applies `homeInteractableUI.SetActive(!_isLocked)` only when the UI's active state differs from the result (also null-guards the UI field).
  - TEMPORARY `LogB5Diag(source)`; every log line starts with `[B5-DIAG]`.

## Acceptance criteria

- [x] (a) RefreshLock in Awake/OnEnable/pointer handlers, same unlock semantics: code review; expression identical.
- [x] (b) Diagnostic added: see "What the logs print".
- [x] Compiles, console has 0 errors. EditMode suite: 79/79 run, only `AIRegressionTest.Baseline_MatchesCurrentAI` failed (known red).
- [ ] B5 fixed: unknown, needs the repro. No Play check was done.

## What the logs print

One line per event, all prefixed `[B5-DIAG]`, with the HomeInteractables component as the log context (click the line to ping the object):

`[B5-DIAG] <Awake|OnEnable|OnPointerEnter|OnPointerDown> obj=<gameObject name> isLocked=<bool> oneEnough=<bool> missions=[<mission asset name>=<Completed>, ...] actionMode=<PlayerInputController.Instance.ActiveActionMode, or "no PlayerInputController"> homeManager=<"exists (mid-sequence flag is private, not logged)" | "null">`

Plus, in OnPointerDown only when locked: `[B5-DIAG] OnPointerDown early return: locked, obj=<name>`.

Logged: Awake, OnEnable, every OnPointerEnter, every OnPointerDown. Not logged: OnPointerExit, per frame.

HomeManager: only `Instance` and `SequencePlayer` are public; `_isPlayingSequence`, `_isShowingTutorial` and `_isPaused` are private, so that field is skipped (I did not edit HomeManager). `actionMode` is the best proxy: None while StartIE or a sequence holds input.

## Save reset

no

## Decisions I made

- Only toggle the UI object when its active state differs from the lock result, to avoid redundant SetActive calls (same end state).
- Logging in OnEnable too, as asked ("Awake/OnEnable"); both go through the same helper.

## Needs THJ

none

## Docs to update

- build-log: add C6 entry; mark `[B5-DIAG]` as temporary, to be removed once B5 is understood.

## Risks and loose ends

- Diagnostic must be removed later (grep `[B5-DIAG]`, delete `LogB5Diag` and its calls, plus the early-return log).
- RefreshLock on pointer events may itself fix B5 if the cause was a stale `_isLocked`; if so the logs will show `isLocked=false` on the first hover. Explore found no such path though, so don't assume.
- Pointer events reaching the object only if a collider/raycaster hits it: if NO `OnPointerEnter` line appears when hovering the Workshop, the cause is input/covering UI or collider, not the lock.

## Proposed commits

1. fix: re-evaluate Home interactable lock on enable and pointer events, add temporary [B5-DIAG] logging: `miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs` (plain)

## Other branches

none

## How to see it

1. Reset to a state where the Workshop is not yet unlocked (fresh save, or whichever state reproduces B5). Open the Console (clear it, keep Collapse off).
2. Enter Play in the Home scene. Note the `[B5-DIAG] Awake` / `OnEnable` lines for the Workshop object: `isLocked`, mission `Completed` values.
3. Complete the mission that should unlock the Workshop and return Home (the Home scene reloads). Check the new Awake/OnEnable lines: `isLocked` should now be false.
4. Hover the Workshop (expect an `OnPointerEnter` line) and click it (expect `OnPointerDown`). Note whether the Workshop panel opens, opens empty, or nothing happens.
5. Also try waiting until the mission-completion sequence / tutorial finishes before hovering, and compare `actionMode`.
6. Then enter another mission and return, and repeat step 4.
7. Copy all `[B5-DIAG]` lines (filter the Console on `B5-DIAG`) and note which of these happened: no pointer lines at all (input/collider), lines with `isLocked=true` and early return (lock), lines with `isLocked=false` but no panel (WorkshopPanelUI / filters).
