# Report: Catch & Return offer rule, C3 (drop the grey lost-hit tint)

Plan: plans/2026-11-17-catch-return-offer-tech.md (change request from THJ, 2026-11-18)    Agent: miso-implementer (sonnet)    Branch: main
Outcome: done, compiling offline. The EditMode suite and the play check were NOT run (THJ's editor is open).

## What changed

THJ's call: the grey tint is dropped. The forward hits the catch gives up (enemies past Mark) show the normal red shot preview, exactly as with no catch. The second colour (pink return bars + chevron) stays only on the enemies the thrown-back arrow hits (between Mark and Linda, plus the Bloom's off-lane copy hits that the return also reaches).

All files are LF on disk (`git ls-files --eol`: `i/lf w/lf` for all seven; checked by bytes: 0 CRLF in each). `GUnit.cs` keeps its BOM. No `.meta` touched. `miso.slnx` untouched.

### Group A: synergies preview + tests (own commit; no dependency on group B, must go first)

All under `miso/Assets/_Project/Features/Player/Shared/Synergies/`.

- `SynergyLanePresenter.Catch.cs`: removed the lost-hit mechanism: `_catchLost`, `_catchLostGiveBack`, `_laneStepsFn`, `LaneStepsOf`, the lost-set build in `ComputeCatchDamage` (both the Bloom and the no-Bloom branch), the lost give-back loop, the grey draw loop in `ApplyCatchDamage`, the lost restore loop in `ClearCatch`, the "forward damage zeroed on a unit that is both lost and returned" line, the lost term in `CatchHoldsNothing`. Also removed what only they used: `CatchShot.Step`, `CatchShot.CatchStep`, the `catchStep` element of `_catchKey` (back to its earlier four-element form; `WouldOffer`'s own key still holds Mark's cell), the `_walkOrigin`/`_walkStep` assignments in `ComputeCatchDamage` (they stay set in `TryReadCatchShot`, where the lane walk needs them). Header comment rewritten: no grey; every other unit keeps the shot's normal red preview; only the return's units get the second colour.
  - Kept as asked: chevron and pink bars only when the catch would be offered, the shared offer rule and hit counter (`CatchReturnHits.CountReturnEnemyHits`, `CatchOfferRules.ShouldOffer`, `IsHostileTarget` for the bar test), the per-aim offer cache (`WouldOffer` / `ForgetOffer`), cleanup on cancel/click/level end, the Bloom handling (`ApplyCatchDamage` still uses the Bloom's values as the forward part on a return unit).
  - A unit in the return set: unchanged pink treatment, and now its forward part is the shot's own damage (never zeroed). A unit not in the return set: never touched by the catch code at all, so the controller's (or the Bloom's) own preview stays.
- `SynergyLanePresenter.Bloom.cs`: restored byte for byte to its state before the preview commit (`git show 2cf617358^`). That removes the two lines in `ApplyBloomDamage` that skipped lost units (the Bloom now skips only units in the return set, as before) and the two `_catchDirty = true` lines in `ComputeBloomDamage` / `ClearBloomDamage`, which only existed so the lost set was recomputed. Re-checked the three redraw paths: `ApplyBloomDamage` reads `_catchReturn` only; the muted loop reads `_catchReturn` only; `ClearBloomDamage` no longer touches catch state. Nothing reads the removed set. The Bloom's own preview shows normally on every unit except those in the return set (drawn pink by the catch, after it).
- `CatchReturnPreviewRules.cs`: removed `AddLostForwardHits` and `AddLostCopyHits` (restored to its state before the preview commit; nothing else in the file had changed).
- `Editor/CatchPreviewOfferTests.cs`: the three lost-hit tests (`LostHits_AreThePreviewedUnitsPastTheCatcher...`, `LostCopyHits_...`, `LostHits_AddToTheSet...`), the two Bloom lost tests (`WithATempestBloomPastMark_...`, `OffLaneCopyHits_...`) and their helpers (`ShotPreview`, `LostHits`, `EnemiesTheForwardFlightTouchesPastMark`, `CopyHits`, `LostHitsWithBloom`) are deleted. Kept and adapted: the offer-decision situations (real catch vs preview agree; enemy between, enemy past Mark only, nobody, neutral, ally, Mark adjacent / off the line / behind a Cyclone). `AssertAgree` now checks that no return bar is drawn when the catch is not offered (through a new helper `ReturnBarUnits`, which runs the same `TempestBloomPreviewRules.CollectHits` call the presenter runs on the return flight's contacts, with the production hostile test). Renamed/changed: `EnemyBetweenOnly_ShowsTheCatch_WithAReturnBarOnIt`; the both-sides test is now `EnemiesOnBothSides_OnlyTheOneBetweenGetsTheReturnColour_TheOnesPastMarkKeepTheShotsPreview`; the layout sweep (about 3,000 layouts) now asserts real offer == preview offer and that every return bar is on an enemy strictly between Linda and Mark. New: `AUnitInTheReturnSet_KeepsTheShotsDamageInTheNormalColour_AndTheReturnOnTopInTheSecond` (pure `BarFor`: the shot's damage stays the confirmed normal part, the return is added on top; this documents that a return unit keeps its forward damage, not zeroed).

### Group B: core grey removal (own commit, core; after group A)

Each file now equals its state at `5426a16d7^` (`git diff 5426a16d7^ -- <file>` is empty for all three; none was touched by a later commit; restored with `git show 5426a16d7^:<file>`, which keeps bytes, LF and the BOM):

- `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs`: the `ShowDamagePreview(total, confirmed, pick, lost)` overload is gone (core file, back to its pre-commit state; BOM kept).
- `miso/Assets/_Project/Features/UI/Panels/Scripts/EntityInfoPanelUI.cs`: `lostDamage`, the two-argument `ShowLethalMark` and the field init are gone.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs`: `lostDecreaseColor`, `LostDecreaseColor`, `SetDecreaseBarTint` are gone. The field was a new serialized field with an in-code default and no prefab override existed, so no asset holds data for it (Grep over `miso/Assets` for the member names across `.cs`, `.prefab`, `.asset`, `.unity`: no hits).

Not touched: `CatchReturnHits.cs` (still has the scratch-list overload, used by the offer cache), `ProjectileCatchAndReturn.cs`, `CatchOfferRules.cs`, `CatchOfferTests.cs`, `miso.slnx`.

## Acceptance criteria

- [x] No grey tint anywhere: Grep for `lostDecreaseColor|LostDecreaseColor|SetDecreaseBarTint|lostDamage|AddLostForwardHits|AddLostCopyHits|_catchLost|_laneStepsFn|LaneStepsOf` and the four-argument `ShowDamagePreview` over `miso/Assets`: none. The only remaining "grey"/"lost" word search over the Synergies folder: none.
- [x] Past-Mark enemies show the normal red preview: by construction, the catch code no longer touches any unit outside `_catchReturn` (needs the play check to confirm on screen).
- [x] Return bars and chevron only on the return's hits, only when offered: test evidence written (offer situations, layout sweep, `ReturnBarUnits`), not run.
- [x] Offer rule, shared counter, per-aim cache, cleanup, Bloom handling kept: code kept as is; cache and cleanup are presenter-level (not unit-testable in edit mode), play check needed.
- [x] Core files back to pre-`5426a16d7`: `git diff 5426a16d7^ -- <file>` empty for all three.
- [ ] EditMode run: not run.

## Save reset

no

## Decisions I made

- Bloom.cs restored whole rather than edited by hand: the preview commit's only changes to it were the lost-set lines, so the restore is exactly the removal (diff shows only those 8 lines).
- The cache key of the return bars went back to four elements and `CatchShot.Step` / `CatchStep` were removed with it: both existed only for the lost set. Nothing else in the cache key needed them (Mark is part of the key; an aim cannot keep going while Mark moves).
- The pure-rule test for the new behavior is `AUnitInTheReturnSet_...` plus the both-sides test (presenter drawing itself is not unit-testable: it needs a combat level, units with info panels and the HP bar prefab). The "units not in the return set keep the shot's preview" part is not asserted by any test, since it is now the absence of code; it is covered by the play check.

## Needs THJ

none

## Docs to update

- Anything that says the catch preview greys the forward hits (earlier C2 report's "Revision: real grey", the plan, the build log, GDD wording if any): the forward hits past Mark now stay the normal red preview; only the return's hits get the second colour.
- C2's "Proposed commits" (the two feature commits already made) stay as history; C3's two commits follow them.

## Risks and loose ends

- **Not run in the editor.** THJ: Ctrl+R, then Test Runner > EditMode > `CatchPreviewOfferTests` and `CatchOfferTests`, then Run All. Expected: green except `AIRegressionTest.Baseline_MatchesCurrentAI`.
- Play check, in a level with Mark and Linda and the catch unlocked:
  - Enemy between Linda and Mark plus enemy past Mark: chevron on Mark, pink return bar on the enemy between (shot's normal red part plus the pink on top), the enemy past Mark shows the ordinary red shot bar, no grey and no changed skull.
  - Enemy only past Mark: no chevron, no pink, normal red bars (unchanged).
  - Cancel with right-click and click-to-fire: bars go back to normal or clear, nothing stuck.
  - With a Lucy Cyclone past Mark and an enemy beside the Cyclone, off the lane: the Bloom's own red preview shows on it; if a return hit touches a unit that also takes a Bloom copy, that unit gets red (Bloom total) plus pink.
  - HP bar tint after the grey code is gone: normal red segment and normal lethal-dark-red tint as before.
- A unit that is both in the return set and takes forward damage shows the shot's damage (normal colour) plus the return on top, as before the lost-hit work.

## Proposed commits

1. A (plain; feature preview and tests): `fix(synergies): the Catch & Return aim preview leaves the forward hits past Mark in the normal red preview instead of drawing them grey`: `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.Catch.cs`, `SynergyLanePresenter.Bloom.cs`, `CatchReturnPreviewRules.cs`, `Editor/CatchPreviewOfferTests.cs`. Must go first: it stops using the lost overload.
2. B (core, additive code removal; own commit, after 1): `revert(ui): remove the lost-damage tint from the HP bar damage preview`: `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs`, `miso/Assets/_Project/Features/UI/Panels/Scripts/EntityInfoPanelUI.cs`, `miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs`.

`miso/miso.slnx` is modified by Unity; leave it out of both.

## Other branches

none

## How to see it

1. Open the editor, wait for the compile (Ctrl+R), Test Runner > EditMode > run `CatchPreviewOfferTests` and `CatchOfferTests`, then Run All.
2. Play a level with Mark and Linda and the catch unlocked. Aim Linda's arrow along a lane over Mark with an enemy between them and another past Mark: the enemy between shows red plus pink, the one past Mark shows the normal red bar like any shot. Remove the enemy between: no chevron, no pink, same normal bars.

## Verification notes

- Compile: offline Roslyn build in the scratchpad (Unity 6000.3.4f1's `DotNetSdkRoslyn/csc.dll` with the editor's own `Assembly-CSharp.rsp` and `Assembly-CSharp-Editor.rsp`, outputs redirected to the scratchpad, the editor not touched; Unity MCP not used): both assemblies built with 0 errors and no diagnostics from any touched file.
- EditMode tests: not run (editor open; physics tests need the editor). The new and changed tests are therefore unverified by execution.
- Git: read-only commands only (`show`, `diff`, `log`, `ls-files`); the three core files were rewritten from `git show 5426a16d7^:<path>` output, the two preview files from `git show 2cf617358^:<path>`, by plain file writes.
