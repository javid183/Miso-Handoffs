# Report: Linda's Quiver C3b, Mark's Catch & Return with a prompt

Plan: plans/2026-10-26-linda-quiver-tech.md (C3b)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done in code, not compiled and not run (the editor is open; nothing was executed). Needs the Test Runner and the play check.

## What changed

- miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs: freeze-and-press flow. Contact disables the original Projectile component (collider stays on, no slow-mo added), builds the return copy from the new `returnPrefab` field, holds the landing, turns Mark and starts the prompt. Decline, prompt failing to start, or OnDisable releases (component back on, landing released, unused copy destroyed). Press returns the arrow to the quiver (existing "+1" cue), keeps the original visible in Mark's hand, and at the apply frame (or the 1 s unscaled fallback in Update) hides the original, activates the copy and wires `copy.onDestroy` to dispose the original. The dead `_pending.Dispose()` comment and the unused `BounceBack` method are gone.
- miso/Assets/_Project/Features/Player/Mark/Scripts/CatchFreezeRules.cs (+ .meta): pure state for freeze, release, press, apply-once and the fallback timer.
- miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchFreezeRulesTests.cs (+ .meta) and Editor.meta: 10 EditMode tests.
- miso/Assets/_Project/Features/Player/Linda/Prefabs/LindaAttackArrowReturn.prefab (+ .meta): copy of LindaAttackArrow with `travelEntireRadius: 0`, new guid a6b15f946c59438ca55d8906cb35b92c. In no whitelist.
- miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab: `triggerWithQTE: 1`, `returnPrefab` set to the new prefab.
- miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/CatchReturnWiringTests.cs (+ .meta): 3 wiring tests.
- claude-handoff/playtests/2026-10-27-mark-catch-qte-play-check.md: numbered play steps.

No core-system code touched (Projectile, QuickTimeEventHandler, EntityAnimationHandler used through public API only). LF endings, no BOM, as the files were. No new statics.

## Acceptance criteria

- [ ] Arrow freezes at Mark during the prompt: `Projectile.enabled = false` on contact. Play steps 1, 11.
- [ ] Pressed: +1 cue, catch animation, return flight ends at Linda and damages on the way, Linda's action waits: quiver return reuses the existing path; the return prefab has `travelEntireRadius 0` (wiring test); `onDestroy` is wired to dispose the original. Play steps 2-5.
- [ ] Declined: same arrow carries on and lands normally: `enabled = true` plus `ReleaseLanding`. Rules tested; play step 6.
- [ ] Nothing past Mark is hit after a press: the original stays frozen, then is disposed. Play step 5.
- [ ] Fallback timer releases a stuck catch: rules tested (applies once, silent after the frame); play step 7.
- [ ] Prompt failing to start or Mark disabled re-releases: rules tested; play steps 8, 9.
- [x] Prefab wiring (prompt on, return prefab set, radius 0, not whitelisted by Mark or the Cyclone): wiring tests, not yet run.
- Recall showing as "Encore": untouched here.

## Save reset

no

## Decisions I made

- The freeze applies in every return mode, not only the bounce ones. In Refund-only mode a press refunds, disposes the copy and disposes the original (it lands where it stopped). Mark's prefab uses BounceBackAndRefund, so this only affects an unused mode.
- Mark's trigger ignores new arrows while a catch is frozen or waiting for its frame.
- A declined catch now destroys the unused hidden copy (it used to stay inactive in the scene).
- The return arrow is a plain prefab copy, not a variant, as the plan allowed. If LindaAttackArrow is edited later, the copy must follow.
- The existing slow-mo code stays as it is (timescale is 1 on Mark's prefab, so it does nothing).

## Needs THJ

Run in Test Runner, EditMode: `MISO.Core.Features.Bergsons.EditorTests.CatchFreezeRulesTests` (10), `CatchReturnWiringTests` (3), then the whole suite. Then the play check.

## Docs to update

- build-log.md: C3b section after the play check.
- status.md: C3b built, awaiting the play check.

## Risks and loose ends

- Not compiled. Signatures checked by reading: `Projectile.GetClone(SpawnableEntity, GridCell, Vector3, GridCell)`, `SpawnableEntity.onDestroy`, `Dispose`, `GetMainVisual`, `EntityAnimationHandler.Play(EntityAnimationData, Action<int>)`.
- `returnPrefab` is typed Projectile; the YAML reference points at the Projectile component of the copy (fileID -6961319225189814693, the same id the original prefab's whitelist reference uses). If Unity shows it as missing, reassign it in the Inspector.
- Spike risks still open: the arrow freezes at the edge of Mark's collider; a disabled component may still get triggers (the arrow's QuiverArrow is a separate component and stays on); the return flight re-hits enemies with falloff restarting at 1.0 (balance); one prompt and one held arrow per Mark.
- The animation handler's Play flushes the previous animation's remaining frames; the apply-once rule covers a late or repeated apply frame.

## Proposed commits

1. feat(mark): freeze Linda's arrow at Mark during the catch prompt and fly it home: CatchFreezeRules.cs(+meta), ProjectileCatchAndReturn.cs, Mark Scripts/Editor.meta, Editor/CatchFreezeRulesTests.cs(+meta), Linda Scripts/Quiver/GroundedArrowField.cs (plain)
2. feat(linda): a return arrow that ends its flight at Linda: LindaAttackArrowReturn.prefab(+meta) (plain)
3. feat(mark): make the catch a prompt and use the return arrow: Unit_Mark.prefab, Editor/CatchReturnWiringTests.cs(+meta) (plain; needs 1 and 2)

## Other branches

none

## How to see it

Follow playtests/2026-10-27-mark-catch-qte-play-check.md.

## Review fixes

- Time scale: the prompt path no longer touches `Time.timeScale` (slow-mo methods and their state removed). The `timescale` field stays serialized and unused, with a comment, so the prefab is unchanged.
- Teardown: `RefundShot` guards a null owner and a missing `CombatLevelUIManager`. When Mark is disabled while an arrow is caught, the return flight starts only if a grounded-arrow field is open (the level is running); otherwise the copy is destroyed and the original disposed. Mid-level behaviour is unchanged, so no hang.
- `CatchReturnWiringTests.cs` converted to LF.
- The two duplicate rules tests are merged into `ReleasedArrow_NeverStartsAReturnFlight` (now 9 tests in `CatchFreezeRulesTests`).
- Play check: items 13-15 are the reviewer's, 16-17 cover the time scale and teardown fixes.
- Still not compiled or run.
- Re-review fix: `GroundedArrowField.IsOpen` (true until the level ends) added; the disable check now tests `Current is { IsOpen: true }`, since a field stays "current" after the level ends. `GroundedArrowField.cs` goes in commit 1.
