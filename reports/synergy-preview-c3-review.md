# Review: Synergy aim preview C3 (Catch & Return), 2026-11-11
(Pasted by the coordinator; the reviewer runs read-only.)

**Verdict: FIX (1 must-fix, 1 should-fix).**

Checked out: extraction (`ProjectileCatchAndReturn.cs:128-211`) behaviour-preserving (early checks, whitelist, `_lastSeen`, QTE flow unchanged; `>= minTileDistance` same; `IsOnIncomingPath` moved verbatim; faction/unlock/distance lookups now always run but are side-effect free; new members read-only; not core). Return math matches (GetClone resets hit count and ledger, falloff restarts, enemies between Mark and Linda hit again; FreezePoint → ReturnDestination; Linda and Mark skipped). Give-back and lifecycle on every exit path; order-independent. Bloom only gains three calls. No statics, no IDs, LF no BOM.

M1. Bloom + Catch bar toggling (`SynergyLanePresenter.Bloom.cs:75-83, 493-500`; `SynergyLanePresenter.Catch.cs:251-265`): each frame ApplyBloomDamage shows Single (deactivates SecondaryDecreaseBarFill), then ApplyCatchDamage shows FinalPick (reactivates). ImageAlphaPulse restarts in OnEnable, so the pink segment is frozen near alpha 0.2 and a coroutine is allocated per frame; LethalMark toggles too. Fix: LateUpdate runs RefreshBloom, RefreshCatch, then ApplyBloomDamage skipping `_catchReturn` units while `_catchAbility != null`, then ApplyCatchDamage and DrawCatchGhosts.

S1. `SynergyLanePresenter.Catch.cs:159`: replace `GetCell(...)?.OccupantEntity` with an explicit Unity-null check.

Notes: give-back on an ability switch can hide a bar the controller just drew (same as C2). Assumed nothing blocks the arrow before Mark. THJ calls: ghost colour field (default green), no return >>>, scene not re-saved (code defaults).

## Re-review after round 2
**APPROVE.**
- M1 fixed: both previews computed before either draws (`SynergyLanePresenter.Bloom.cs:75-85`); while the catch is on the Bloom skips the return's units for shows and hides (`Bloom.cs:495-505`). One look per unit per frame in Bloom only, Catch only, both.
- Toggles clean: catch on → one switch; catch off with Bloom on → hidden by ClearCatch (`Catch.cs:344-347`) and re-shown by the Bloom the same frame; catch alone off → shot value on same aim; Bloom off under catch → one change, then FinalPick.
- No C2 regression. S1 fixed (`Catch.cs:159-160`). LF, no statics, no IDs, no per-frame allocations.
- Play check: Memory 4, Cyclone past Mark: pink segment pulses, skull steady.

## Re-review after round 3
**APPROVE.**
- Chevrons don't clear each other: catch never clears a Bloom-held or shooter cell (`SynergyLanePresenter.Catch.cs:262-274`); Bloom never clears `_catchChevronCell` (`Bloom.cs:345-347`); Linda's own >>> untouched (`Catch.cs:156, 264`).
- Never share a tile (return chevron before Mark; copy chevrons past a Cyclone past Mark); nothing would stick if they did.
- Cleared on every exit (`Catch.cs:307`; polling `Catch.cs:78-81` with `CatchHoldsNothing` counting the chevron; OnDisable/OnDestroy).
- Ghost removal complete (no refs in code, scenes, prefabs); one-bar-per-frame fix intact (`Bloom.cs:496-506`).
- Chevron rule tested (`CatchReturnPreviewTests.cs:63-94`). No core edits; LF no BOM.
- Nit: comment at `Catch.cs:286-290` breaks mid-sentence.
- Open for THJ: tinted chevron needs a small new core method on `GridCell` (Tier 3).

## Re-review after round 4
**APPROVE.**
- `TryGetReturnChevronTile` returns Mark's own tile pointing one step toward Linda; false off a straight line or on a shared tile (`CatchReturnPreviewRules.cs:46-55`); tested (`CatchReturnPreviewTests.cs:63-85`).
- Nothing else draws on Mark's tile while Linda aims (controller: active/approach cell, `PlayerController.cs:1065, 1213, 1216, 1501`; Duo: Linda's cell, `UnitsCooperationHandler.cs:584, 600`; Bloom copy chevrons past the Cyclone).
- Cleared on every exit through ClearCatch, with or without Bloom; previews never clear each other's cells.
- GridCell.cs and Bloom chevron placement unchanged (D-500). No core edits. LF, no BOM.
