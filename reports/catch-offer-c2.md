# Report: Catch & Return offer rule, C2 (preview and feedback)

Plan: plans/2026-11-17-catch-return-offer-tech.md    Agent: miso-implementer (sonnet)    Branch: main
Outcome: partial. Built and compiling in a scratch build; the EditMode suite and the play check were NOT run (THJ's editor is open). One open point for THJ: the lost forward hits are taken off the HP bar (muted), not greyed or struck through, because the bar has no grey option (see "Needs THJ").

## What changed

All under `miso/Assets/_Project/Features/Player/Shared/Synergies/` (LF files, kept LF; no core file touched).

- `SynergyLanePresenter.Catch.cs`:
  - `TryReadCatchShot` now calls `CatchReturnHits.CountReturnEnemyHits(returnArrow, From, To, Linda, Mark, ...)` and `CatchOfferRules.ShouldOffer` (the same two calls the real catch's `ReturnWouldHitEnemy` makes, same arguments: Mark's catch point to Linda's `ReturnDestination`). When the rule says no it returns false, so no chevron on Mark's tile, no pink return bars, no lost-hit work, and the controller's normal shot preview stays untouched. The check runs after the "catch only refunds" and "no return arrow" bails.
  - The return bars now use `CatchReturnHits.IsHostileTarget` as their hit test (was: alive and targeted by relation). A neutral (relation 0) unit no longer gets a pink bar, and the bars are drawn on exactly the kind of unit that makes the catch offered.
  - New lost-hit set `_catchLost` (unit -> the damage the shot's own preview showed): units past Mark on the shot's lane (steps from Linda greater than Mark's step) that the normal preview shows damage on; with a Tempest Bloom on, the Bloom's units past Mark too. Worked out in `ComputeCatchDamage` (cached with the same key as the return bars, which now also holds Mark's lane step).
  - `ApplyCatchDamage` (every frame, after the Bloom's draw) takes the lost units' bar off (`ShowInfoPanel(false, Damage)`, the same call the Bloom uses for units it mutes). If the return also hits a lost unit, the pink bar is drawn with 0 forward damage.
  - `ClearCatch` gives lost units back: the shot's own preview while the same aim is up and the Bloom is off, hidden otherwise (the controller redraws on hover). `CatchHoldsNothing` includes the lost set, so cancel, ability switch, click, end of turn, level end, `OnDisable` and `OnDestroy` (all already routed to `ClearCatch` via `RefreshCatch` or the lifecycle) cover the muted state. A unit that stops being a lost hit between recomputes gets its normal bar back.
  - Header comment updated.
- `CatchReturnPreviewRules.cs`: new pure `AddLostForwardHits<T>(forwardPreview, stepsAlongLane, catchStep, into)` (adds, never clears; units with damage > 0 and lane step > the catch step; keeps the damage shown so the bar can be given back).
- `CatchReturnHits.cs`: new overload of `CountReturnEnemyHits` that takes the caller's scratch lists (the preview asks every frame; same body, the 5-argument version delegates to it, so the real catch is unchanged).
- `SynergyLanePresenter.Bloom.cs`: `ApplyBloomDamage` also skips units in the lost set (the catch preview draws them, after it), same pattern as the existing skip for return units.
- `Editor/CatchPreviewOfferTests.cs` (+ `.meta`, hand-written MonoImporter meta with a fresh guid): 11 edit-mode tests, real colliders on a lane far from the origin (the C1 setup), the shared count and the production `IsHostileTarget` for the hostile test.
- Not touched: `ProjectileCatchAndReturn.cs`, `CatchOfferRules.cs`, `CatchOfferTests.cs`, every core file, `miso.slnx`.

## Acceptance criteria

(C2 only; the runtime criteria were C1's.)

- [x] Preview uses the same rule and hit counter as the real catch: the code calls `CountReturnEnemyHits`, `IsHostileTarget` (through it and in the bar test) and `ShouldOffer`; nothing is copied. Test evidence (written, not run): `CatchPreviewOfferTests` situations and `TheLostSet_IsEveryEnemyTheForwardFlightTouchesPastMark_ForEveryLayoutOfOneLane` (about 3,000 layouts of Mark plus two units, asserting real offer == preview offer in each).
- [x] Rule says no: no chevron, no pink bars, normal shot preview stays (`TryReadCatchShot` returns false before any catch state is set). Tests: enemy past Mark only, nobody, ally only, neutral only, Mark adjacent, Mark off the line, Cyclone before Mark: real and preview agree and the lost set is empty.
- [x] Neutral (relation 0) units get no pink bar and no offer: `ANeutralUnitBetween_IsNoHit_SoNothingIsDrawn`, `ANeutralUnitBetween_NextToAnEnemy_AddsNoHit`, and C1's `HostileTarget_NeutralRelation_...`.
- [~] Rule says yes, lost forward hits: the set is computed and tested (`EnemiesOnBothSides_ShowTheCatch_AndLoseTheOnesPastMark`, `LostHits_AreThePreviewedUnitsPastTheCatcher_OnTheShotsLane`, and the layout test comparing it with an independent contact walk of the arrow from Mark to the end of its reach). The pink return bars stay. The lost bars are removed, not greyed or struck through: see "Needs THJ".
- [x] Survives the hover refresh as today: the lost bars are re-applied every frame in `ApplyCatchDamage`, like the return bars (the controller redraws only on hover).
- [x] Clears on cancel, click and level end: the lost state is part of what `ClearCatch` and `CatchHoldsNothing` cover (by reading; the Play check must confirm the bars return).
- [ ] Compile clean in the editor / EditMode all green except the known red: not run. Scratch Roslyn build of `Assembly-CSharp` and `Assembly-CSharp-Editor` with my changes: 0 errors, 0 warnings from these files. The pure logic (`AddLostForwardHits`, `ShouldOffer`) was also run in a throwaway console harness outside the project: results as the tests expect. AIRegressionTest inner failure count: not measured (no AI code touched).

## Save reset

no

## Decisions I made

- **Lost hits are muted, not greyed** (deviation in look, needs THJ's call): the HP bar's existing colour options are the red decrease segment, the pink second segment (the return bars) and the dark-red lethal tint. There is no grey, and drawing the forward damage in pink would read as "happens if the catch works", the opposite of lost. A true grey or strike needs a bar tint that doesn't exist yet (see Needs THJ). Muting reuses the call the Bloom already uses for "this shot won't hurt this unit", needs no asset and no core change, and the lost set is one dictionary, so swapping the look later touches only `ApplyCatchDamage`, `ClearCatch` and `ComputeCatchDamage`'s give-back.
- The lost set is derived from lane steps (units past Mark's step on the shot's lane that the shot's own preview shows damage on), the same arithmetic the Bloom preview uses for "past the Cyclone", rather than a second physics walk. A test compares it with an independent contact walk from Mark to the end of the arrow's reach.
- With a Tempest Bloom on past Mark, the lost set also takes the Bloom's units past Mark (their damage only happens if the arrow flies on). Bloom copy damage on units BEFORE Mark is left as it was (a copy never spawns if the catch happens, but that is the existing both-previews design).
- The offer check runs every frame the aim leads to a catch (a 50-point overlap walk over a short lane), through the scratch-list overload so the contact lists don't allocate each frame; not cached, because a cached "no" could go stale when the shot resolves and the same ability and cell come round again.
- `shot.CatchStep` joined the cache key of the return bars so a moved Mark recomputes them.
- Line endings: all these files are LF on disk (checked by bytes), kept.

## Needs THJ

1. **Decision:** the lost forward hits are currently hidden while the catch is previewed, because the bar can't show grey or struck through. Options: (A) keep the hidden bar (done, no further work); (B) real grey or strike: add a tint to the bar (non-core: `UI_Element_FillBar` gets a `lostDecreaseColor` with an in-code grey default plus `SetDecreaseBarLost(bool)` like the lethal one, and `EntityInfoPanelUI` / `EntityInfoData` carries a flag) and a core additive hook so the presenter can set it: `GUnit.ShowDamagePreview` gets one more overload with a "struck" flag (`GUnit` is on the core list; the panel field in it is private, so the presenter has no other way in). No prefab edit needed (the colour default lives in code). That is a Tier 3 edit to `GUnit`. **Recommendation:** ship A for the play check; take B only if THJ finds the vanishing bar unclear. Reversibility: B is additive and A is a few lines to switch.

## Docs to update

- Nothing from C2 (C3 owns the GDD and handoff docs). For C3: the preview shows the catch only when it would be offered; past-Mark forward damage bars are removed while the catch is previewed (or greyed if option B is taken).

## Risks and loose ends

- **Not run in the editor.** THJ (or the coordinator) must recompile (Ctrl+R), run EditMode and confirm all `CatchPreviewOfferTests` and `CatchOfferTests` pass and the suite is green except `AIRegressionTest.Baseline_MatchesCurrentAI`. The new test file has a hand-written `.meta`; if Unity regenerates it that is fine.
- The presenter wiring (muting, restoring, pink bar on a unit both touch) can't run in edit mode (needs a combat level, units with info panels). Play check, with the plan's four situations: (a) enemy only past Mark: no chevron, no pink bars, normal shot bars, the arrow hits them; (b) enemy between: chevron, pink bars; (c) both: chevron, pink bars on the between enemy, the past-Mark enemy's bar gone; cancel or click and the bars go/return correctly; (d) nobody: nothing at all. Also: ally on the line with no enemy: no chevron.
- Prediction vs reality: a unit can move or die between the aim and the arrow reaching Mark only through something other than the player's own action; if the prediction said yes and nothing is hit, the existing release path applies (unchanged, as in C1).
- Multi-cell units are placed by their `CurrentCell` (as the Bloom preview does); a big unit straddling Mark's step could be classed either side.
- A hostile non-`GUnit` entity (summon without a unit) offers the catch but draws no bar (C1 note, unchanged; the chevron decision uses the shared count).
- The overlap walk now runs each frame while the aim leads to a catch; negligible, but if profiling ever shows it, cache per (ability, aim, cell, Mark) and clear on `ClearCatch`.

## Proposed commits

1. `feat(mark): the Catch & Return aim preview shows the catch only when it would be offered, and takes off the forward hits it gives up`: `Shared/Synergies/SynergyLanePresenter.Catch.cs`, `SynergyLanePresenter.Bloom.cs`, `CatchReturnPreviewRules.cs`, `CatchReturnHits.cs`, `Editor/CatchPreviewOfferTests.cs` (+ `.meta`). All under `miso/Assets/_Project/Features/Player/Shared/Synergies/`. Plain (feature code, preview only; it depends on the committed C1). If the reviewer wants it split: `CatchReturnHits.cs` + `CatchReturnPreviewRules.cs` + tests first, the two presenter files second.

## Other branches

`thj/cyclone` touches the Cyclone-before-Mark case (`SplitsAt`); not touched here. Otherwise none.

## How to see it

1. Open the editor, wait for the compile (Ctrl+R), run Window > General > Test Runner > EditMode > `CatchPreviewOfferTests` and `CatchOfferTests`, then Run All.
2. In a level with Mark and Linda and the catch unlocked, aim Linda's arrow along a lane over Mark (2+ tiles away) and watch Mark's tile and the enemy HP bars: enemy only past Mark (no chevron, no pink, the normal bars), enemy between (chevron and pink bars), both (chevron, pink bar on the between enemy, the past-Mark enemy's bar gone), nobody (nothing). Cancel with right-click and click-to-fire: the bars go back to normal or clear. Put a neutral unit between: no chevron.

## Revision: real grey (2026-11-17)

THJ decided (2026-11-17): the forward hits the catch gives up are drawn as a real grey preview, not hidden (if the prompt is missed the arrow flies on and hits them at full damage). He approved the additive core change for it. Also fixes the review findings on C2. Agent: miso-implementer.

### Built

**GROUP 1: core, additive only (own commit; behavior unchanged when the flag is off)**

- `miso/Assets/_Project/Core/Units/Runtime/GUnit.cs` (core list): new overload `ShowDamagePreview(float total, float confirmed, DamagePreviewPick pick, bool lost)`, placed after the existing two, which are untouched. It builds the same `EntityInfoData` with `lostDamage = lost`. CRLF and BOM kept.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/EntityInfoPanelUI.cs`: `EntityInfoData` gets a public `bool lostDamage` field. The existing constructor's signature is unchanged; its body sets the field to false, which C# 9 requires for a struct constructor. `ShowHealthMode` passes the flag to a new private `ShowLethalMark(mark, lost)`. The old one-argument `ShowLethalMark(mark)` now calls it with false (used by `ShowFullMode`, same result). When lost is set, the decrease segment and the skull, if shown, take the lost tint.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs`: new serialized `lostDecreaseColor` (Colors foldout, in-code default grey `0.55, 0.55, 0.55`, so no prefab edit and no asset), getter `LostDecreaseColor`, and `SetDecreaseBarTint(bool lethal, bool lost)`. With lost false it calls the unchanged `SetDecreaseBarLethal`. With lost true it sets the grey, which wins over lethal, and the alpha stays with the pulse as before.
- Cleanup confirmed by reading: the tint is written again on every `ShowHealthMode` (Damage) and `ShowFullMode` (Global/FullDetail, through `ShowLethalMark(None)`), and every `Show` goes through one of the two. `Hide` deactivates the panel or shows the queued mode through `ShowFullMode`. So `PlayerController.HideDamagePreviews`, `ShowInfoPanel(false, Damage)`, the presenter's `ClearCatch` and give-back paths, and any later normal `ShowDamagePreview` all leave the bar in its normal tint. No new statics, no new files.

**GROUP 2: presenter, `miso/Assets/_Project/Features/Player/Shared/Synergies/` (depends on group 1)**

- `SynergyLanePresenter.Catch.cs`:
  - `ApplyCatchDamage` now draws each lost unit with `ShowDamagePreview(value, 0, Single, lost: true)` instead of hiding its bar. A unit the return also hits still gets its pink two-colour bar (forward part 0), as before.
  - **(must-fix) Off-lane Bloom hits:** with a Tempest Bloom on, the lost set is now the Bloom's preview past Mark on the lane, plus every unit the copies hit (`_copyDamage`), on the lane or off it, through the new rule `AddLostCopyHits`. With the Bloom on, the shot's own `normal` preview is no longer used for the lost set. That also stops a unit the Bloom mutes (past the Cyclone, hit by no copy) from being drawn as a lost hit it would never take. With the Bloom off, the lost set is still `normal` past Mark.
  - **(must-fix) Header comment** rewritten for the final behavior: the preview shows the branch where the prompt is missed (the arrow flies on and hits those units), and they are drawn grey because taking the catch gives them up. The line saying the shot's own preview is "unchanged" now says "up to Mark".
  - **(should-fix) Per-frame allocation:** the offer decision is cached per (ability, aim, Linda's cell, Mark, Mark's cell, return arrow) in `WouldOffer`. `ForgetOffer` clears it when there is no aimed ability, when the level has ended, and in `ClearCatch`, which also runs on every cursor-leave. So the contact walk, its closures and `CatchOfferRules`' list now run once per aim, not every frame. The real catch still asks fresh on every arrow.
  - Comments on `_catchLost` and `ClearCatch` updated.
- `SynergyLanePresenter.Bloom.cs`: **(should-fix)** `ComputeBloomDamage` and `ClearBloomDamage` set `_catchDirty = true`, so the lost set is worked out again whenever the Bloom's values change or the Bloom turns off. `ComputeBloomDamage` runs before `RefreshCatch` in the same `LateUpdate`, so the lost set is never a frame behind.
- `CatchReturnPreviewRules.cs`: new pure `AddLostCopyHits<T>(shownDamage, copyHits, into)`. It adds every unit a copy damages, with the damage the Bloom preview shows on it (or the copies' own damage when that shows none). It adds to the set and never clears it.
- `Editor/CatchPreviewOfferTests.cs`: 3 new tests (14 in total):
  - `WithATempestBloomPastMark_EveryUnitTheCopiesHit_IsLost_OnTheLaneOrOffIt`: real colliders, Cyclone past Mark, copies walked with the shared contact walk and the real scatter-direction rule. Off-lane copy hits above and below the Cyclone, the forward copy and the unit between Mark and the Cyclone are lost. The hit before Mark and an untouched off-lane unit are not.
  - `OffLaneCopyHits_AreMissedByTheLaneRuleAlone`: shows the bug the fix closes.
  - `LostCopyHits_TakeTheDamageShown_OrTheCopiesOwn_AndSkipUnitsTheyDontDamage`: pure.
- `CatchReturnHits.cs`: not touched in this revision. It still has C2's scratch-list overload. That overload's comment says the lists aren't allocated each time, which stays true.
- `miso/miso.slnx`: not touched and not in any file list. It shows as modified in `git status` because Unity regenerates it; leave it out of every commit.

### Verified

- Offline Roslyn build in the scratchpad: Unity 6000.3.4f1's `DotNetSdkRoslyn/csc.dll` with the editor's own `Assembly-CSharp.rsp` and `Assembly-CSharp-Editor.rsp`, outputs redirected to the scratchpad, the editor not touched. Both assemblies built with 0 errors and no warnings in the touched files. Unity MCP was not used (not available in this session).
- Line endings: every touched file is CRLF on disk, and stayed CRLF (`GUnit.cs` keeps its BOM). C2's report said these files were LF; they are CRLF on disk (`core.autocrlf` is false).
- Refund-only branch: Mark's catch uses `returnMode: 1` = `BounceBack` (`Unit_Mark.prefab` line 2970). `ProjectileCatchAndReturn`'s script GUID appears in no other prefab, scene or asset, no code adds the component at runtime, and no prefab variant overrides `returnMode`. The script default is `BounceBackAndRefund`. So the `Refund` mode, where `TryCatch` would ask the offer rule about a return that never flies, is used by no shipped unit. It can be reached only if someone sets a catcher to `Refund` in the Inspector. In that case the refund would happen only when enemies stand between Linda and Mark (worth knowing; no change made).

### Not verified

- Recompile in the editor and the EditMode suite: not run (THJ's editor is open). THJ: Ctrl+R, then Test Runner > EditMode > `CatchPreviewOfferTests` (14) and `CatchOfferTests`, then Run All. Expected: all green except `AIRegressionTest.Baseline_MatchesCurrentAI`.
- The overload, the grey tint and the presenter's drawing can't run in edit mode (they need a combat level, units with info panels, the HP bar prefab). Play check, in a level with Mark and Linda and the catch unlocked:
  - Enemy between and enemy past Mark: chevron, pink bar on the one between, grey bar with the full forward damage on the one past.
  - Cancel and click: bars back to red or cleared, no grey left behind.
  - Both enemies plus a Lucy Cyclone past Mark with an enemy beside the Cyclone, off the lane: that enemy's bar is grey too.
  - Enemy only past Mark: normal red bar, no chevron.
- How the grey reads on screen (contrast with the pulse) is THJ's eye. The colour is a serialized field on `UI_Element_FillBar` (Colors > Lost Decrease Color) and can be tuned on the HP bar prefab without code.

### Findings

- Design detail I chose: a lost hit that would kill shows its skull in the same grey (the kill happens only if the arrow flies on). The HP number on the bar shows the HP left after that damage, as the normal preview does.
- The offer cache assumes units don't move or die while the player keeps aiming at one cell. Any change of cell, cancel, fire, end of turn or end of level forgets it.
- A unit that both the return and a copy would hit gets the pink bar with 0 forward damage, as before; the copy damage on it isn't shown.
- Proposed commits, in order:
  1. `feat(ui): HP bar damage preview can draw damage that may not land in a grey tint`: `Core/Units/Runtime/GUnit.cs`, `Features/UI/Panels/Scripts/EntityInfoPanelUI.cs`, `Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs`. Core and additive, so it gets its own commit.
  2. `feat(mark): the Catch & Return aim preview shows the catch only when it would be offered, and greys the forward hits it gives up`: `Features/Player/Shared/Synergies/SynergyLanePresenter.Catch.cs`, `SynergyLanePresenter.Bloom.cs`, `CatchReturnPreviewRules.cs`, `CatchReturnHits.cs`, `Editor/CatchPreviewOfferTests.cs` and `Editor/CatchPreviewOfferTests.cs.meta`. This replaces C2's proposed commit; it needs commit 1.

### Status

Built and compiling offline. Waiting on THJ's recompile, his EditMode run and the play check. No save reset. No git write commands run.
