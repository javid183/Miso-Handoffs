# Review: duo insert follow-up F1 (`thj/duo-insert`, uncommitted on top of `5fc81e789`)

Reviewer: miso-reviewer, 2026-11-22 (saved by the coordinator; the reviewer is read-only).

**Verdict: APPROVE** (two low-stakes should-fixes sent back before the commit)

## Must fix
None.

## Should fix
1. `DuoInsertRulesTests` `IsBoundToAny_*` only cover null/empty. Test the real filter in edit mode with `InputSystem.AddDevice<Keyboard>()`, an action bound to `<Keyboard>/space` plus a composite: space (and the composite parts) bound, `a` not; remove the device in TearDown.
2. `DuoInsertLibrary.Entry.WithTransition` copies fields by hand: a later field would be dropped from the forced-style previews. Use `MemberwiseClone` (or a comment).

## Checks
- F1a works without F1b (null list = no filter); commit F1a first.
- Skip filter: every keyboard key checked against the ignored actions' controls (composites included); no `anyKey` bindings in the project's actions; mouse L/R and pad face buttons + Start as before; other presses still skip after `skipDelay`. F1b resolves by name like `QuickTimeEventHandler`/`QTEButton`, guards null profile and missing `PlayerInputController`.
- Abort cleanup unchanged and complete; every new loop exits on abort; speed lines re-enabled after a skip.
- No squeeze (polygon always inside its aspect-filled frame). Solo style zooms/pans the sweeping half (reported; a look call for THJ).
- Serialized: no renames; asset holds only new values (`leadSide: 2` = Right; transition 0 main, 1 clip A); prefab holds exactly the 8 new fields.
- Line endings/BOM kept (asset, prefab, `UnitsCooperationHandler.Insert.cs` CRLF; DuoInsert .cs LF no BOM). No private IDs. No new statics.
- `DuoInsertBuilder.cs` belongs in F1a (re-running it would reset lengths and styles otherwise).

## Risks
- Clips now play from the start of the In phase: a full play needs ~2.85 s of clip from `clipStart` 0.5 (test clips are 8 s: fine; matters for real clips).
- Solo opening zoom ~2× on the lead clip: THJ's look call.
- No `PlayerInputController` → empty list → every input can skip (safe).
- Motion, out phase, mash-without-skip, other-key-skips: THJ's play check. No AI impact.
