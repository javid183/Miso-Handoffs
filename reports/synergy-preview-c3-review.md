# Review: Synergy aim preview C3 (Catch & Return), 2026-11-11
(Pasted by the coordinator; the reviewer runs read-only.)

**Verdict: FIX (1 must-fix, 1 should-fix).**

Checked out: extraction (`ProjectileCatchAndReturn.cs:128-211`) behaviour-preserving (early checks, whitelist, `_lastSeen`, QTE flow unchanged; `>= minTileDistance` same; `IsOnIncomingPath` moved verbatim; faction/unlock/distance lookups now always run but are side-effect free; new members read-only; not core). Return math matches (GetClone resets hit count and ledger, falloff restarts, enemies between Mark and Linda hit again; FreezePoint → ReturnDestination; Linda and Mark skipped). Give-back and lifecycle on every exit path; order-independent. Bloom only gains three calls. No statics, no IDs, LF no BOM.

M1. Bloom + Catch bar toggling (`SynergyLanePresenter.Bloom.cs:75-83, 493-500`; `SynergyLanePresenter.Catch.cs:251-265`): each frame ApplyBloomDamage shows Single (deactivates SecondaryDecreaseBarFill), then ApplyCatchDamage shows FinalPick (reactivates). ImageAlphaPulse restarts in OnEnable, so the pink segment is frozen near alpha 0.2 and a coroutine is allocated per frame; LethalMark toggles too. Fix: LateUpdate runs RefreshBloom, RefreshCatch, then ApplyBloomDamage skipping `_catchReturn` units while `_catchAbility != null`, then ApplyCatchDamage and DrawCatchGhosts.

S1. `SynergyLanePresenter.Catch.cs:159`: replace `GetCell(...)?.OccupantEntity` with an explicit Unity-null check.

Notes: give-back on an ability switch can hide a bar the controller just drew (same as C2). Assumed nothing blocks the arrow before Mark. THJ calls: ghost colour field (default green), no return >>>, scene not re-saved (code defaults).
