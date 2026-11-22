# Duo insert shot, chunk C2 (duo flow: QTE card, insert, then actions)

Plan: `plans/2026-11-22-duo-insert-shot-tech.md`. C1 report: `reports/2026-11-22-duo-insert-c1.md`. Core system touched: Duos `UnitsCooperationHandler` (approved by THJ). Nothing committed. No scene touched, no Play mode entered.

## Files

Changed (under `miso/Assets/_Project/`):
- `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`: +23 / -12. UTF-8 BOM and LF kept. `CooperationEntry` and `UnitsCooperationHandler` made `partial`; `ExecuteIE` picks the insert path or the panels; `ActivateAbility` takes an optional stored-results map; the QTE factor mapping now goes through `CoopQteFactor` (same arithmetic).
- `Content/Controllers/PlayerController.prefab`: +1 line, `duoInsertPrefab` on the `UnitsCooperationHandler` component pointing to the `DuoInsertSequence` component of `Features/UI/DuoInsert/Prefabs/DuoInsertCanvas.prefab`.

New (each with its `.meta`, LF, no BOM):
- `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.Insert.cs` (224 lines) + `.meta`
- `Core/Systems/AbilitySystem/Abilities/Editor/CooperationInsertTests.cs` (157 lines) + `.meta`

Not mine, left alone: `Scenes/PreloadScreen.unity`, `ProjectSettings/*`, the untracked `Content/FamilySuperTime/DUO/Inserts*`.

## What it does

- `ExecuteIE`: if the handler's insert sequence has an entry for the duo id and the mode is not Off (`UnitsCooperationHandler.ShouldPlayInsert`), it runs `RunInsertIE` and skips `ShowDuoVisual`. Otherwise it calls `ShowDuoVisual` and continues exactly as before.
- `RunInsertIE`: `Time.timeScale = 0` (handler flag set); for each partner with `qteFactor`, in partner order: `PlayCardIE(unit, entry.caption, slot)`, then `QuickTimeEventHandler.StartEvent(copy of profile with inUI = true, slot, ...)`; the prompt is centred on the slot (`localPosition = zero` after StartEvent, at the call site); waits for notice/miss; stores `{factor, success}`; waits up to 1.5 s (unscaled) for the prompt's notice/miss animation to finish on the card so the button goes back to its pool, then moves the button out of the card (under the `QuickTimeEventHandler` object) so it never lives or dies with the insert canvas. Then `PlayInsertIE(entry)`, `HideCard()`, `Time.timeScale = 1`.
- Then camera focus, move-path overrides and the partner run are unchanged. `ActivateAbility` for a `qteFactor` partner with a stored result calls the same `ActivateFromQte` (same `CoopQteMod` application, same same-entity spread, `onSuccessfulQTE` only when the prompt succeeded). Mark's blitz branch in Mark–Lucy is checked first, unchanged.
- Factor mapping in one place: `CoopQteFactor.Raw(mode, success, secondaryFill)` (mash modes: SecondaryFill; press modes: 1 on success, 0 on miss) and `CoopQteFactor.Map(min, max, raw)` (`min + (max - min) * raw`). The old board-QTE path uses them too.
- Profile copy: `UnitsCooperationHandler.CopyProfileForScreen` (reflection `MemberwiseClone`, shallow). The serialized profile is never written by the insert path (StartEvent writes `InitialHoldTime` on the copy).
- Finding the sequence: lazy `Instantiate(duoInsertPrefab, transform)` on the first duo, as a child of the PlayerController, so it is destroyed with it. Missing reference: one warning per handler, panels path.

Exit paths:
- QTE could not start (another QTE active, input action missing): warning, counts as missed (factor 0, no `onSuccessfulQTE`), the duo continues.
- Sequence disabled or destroyed mid-card: the running prompt is force-ended (miss), the rest of the card/insert is skipped, timeScale back to 1, the duo continues.
- Handler disabled mid-insert (`OnDisable`, new): force-ends a prompt still on the card and sets timeScale back to 1.
- No new statics.

## Verified

- Unity MCP connected; compiled clean (no errors) after a forced refresh.
- Prefab reference set through the Unity MCP (SerializedObject on the prefab asset). Unity's save also re-serialized unrelated default fields (`turnStartPause`, `preloadOverride`, `showSpeed`: 48 lines of noise), so I rewrote the file as HEAD plus the single new line and reimported; the reference loads as `DuoInsertCanvas (DuoInsertSequence)`. Diff: 1 line.
- `CooperationInsertTests`: 13 tests, all pass. Coverage: mash fill ignores press/miss (Mashing, TimeWindowMash), press 1/0 (TimedPress, TimeWindow), map min/max/middle (0.7..1.5), missed result, profile copy (inUI true on copy, original untouched, fields copied, null), insert decision (entry present, Full mode, entry absent, mode Off, no sequence, destroyed sequence, sequence without library), shipped library has Mark–Lucy and none of the six other real duos.
- Duo/cooperation fixtures (DuoInsertRules, Cyclone, Masher and everything the group regex caught): 572/572 pass.
- Whole EditMode suite: 2456 total, 2455 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). AI regression not run: no AI graph, AI ability or unit prefab changed.

## Not verified (needs THJ in Play mode)

Nothing of the flow was seen on screen. Play-check list:
1. Mark–Lucy: board dims and freezes; no FTPPanel duo panels; Lucy's mash prompt sits centred in the card's slot (not over Lucy, not offset); mash works; the prompt's notice/miss plays on the card; then the split insert (flash, speed lines, caption "Chained Assault", Lucy push-in, Mark clip B without logos); then the camera focus and Lucy's attack scaled by the mash (×0.7 empty to ×1.5 full), then Mark's blitz as today. Time runs normally afterwards.
2. Mark–Lucy again in the same combat: insert plays short (0.6 s).
3. Skip: a key/click after 0.3 s into the insert skips it; the action plays normally.
4. Off mode: set `Mode = Off` on the spawned `DuoInsertCanvas(Clone)` (child of the PlayerController) or on the prefab: Mark–Lucy shows the old panels and the prompt on Lucy, as before.
5. John–Mark and Mark–Linda (Catch & Return): unchanged panels, order and QTE placement. One more duo with a QTE (e.g. John–Lucy): unchanged.
6. Leave combat or stop Play mid-card and mid-insert: no stuck timeScale 0, no QTE errors on the next QTE, no leak warnings.
7. Two QTE duos in a row (Mark–Lucy then another QTE duo or a Catch & Return): the board prompt still shows (pool not lost).

## Decisions and deviations

- Card title is `entry.caption` (same text as the insert caption; C1's preview did the same). The plan did not name the title source.
- The card stays up until the prompt's notice/miss animation ends (max 1.5 s), not hidden right when the QTE result arrives: hiding the card while the button's animator is mid-outro would freeze the animation event that returns the button to the QTE pool (the pool has 2 buttons, so two such duos would block every later QTE). Visible effect: the player sees the notice/miss beat on the card before the insert.
- The button is moved out of the card afterwards to the `QuickTimeEventHandler` object (found once with `FindFirstObjectByType`, main thread). Its parent before the card is private to QTE code, which I was told not to edit; any parent works because `BindPlacement` reparents on every use, and `SetParent(..., true)` keeps world scale, so its size under the default parent does not drift.
- Insert-path detection lazily instantiates the canvas on the first duo of any kind (an idle, hidden overlay canvas). Keeps one reference on the handler; the library is reached through the sequence.
- The missing-prefab warning is per handler (no statics), so it shows once per controller that runs a duo without the reference.

## Risks and loose ends

- Pre-existing, unchanged: on the old board path, a QTE that cannot start leaves `Time.timeScale = 0` and the duo hangs (no ignore callback is called). The insert path does not have this. Worth a small fix later; not done (old path must stay the same).
- Mash spam may skip the insert: the insert's skip check (C1) reads any key after 0.3 s; a player still mashing after Lucy's prompt ends can skip it at once. Design call for THJ (e.g. ignore the QTE's binding, or a longer skip delay).
- If the PlayerController is destroyed while a prompt is on the card, the pooled button is destroyed with the canvas. `OnDisable` force-ends it first, which keeps the QTE handler clean, but the button itself is gone; only matters if the QTE handler outlives the PlayerController (both are in the combat scene).
- An exception thrown inside the card/insert would leave timeScale 0 until the handler is disabled (same class of risk as the old path).
- `DuoInsertSequence` uses-per-combat lives on the spawned instance: it resets when the PlayerController is recreated. If one PlayerController spans several combats, `ShortAfterFirst` would stay short; `ResetUses()` exists if needed.
- Unity logs a pre-existing "Serialization depth limit 10 exceeded" warning for `UnitsCooperationHandler.entries`; not new.
- C3 docs: core-systems Duos row should mention the insert path, the optional `duoInsertPrefab` reference and the new `OnDisable`.

## Proposed commit (C2)

Files:
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.Insert.cs` + `.meta`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/CooperationInsertTests.cs` + `.meta`
- `miso/Assets/_Project/Content/Controllers/PlayerController.prefab`

Do not stage: `Scenes/PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts*`.

Message:
```
feat(duos): duos with a comic insert run their QTE on a framed card, play the insert, then act

Mark-Lucy (the only duo in the insert library) freezes the board, shows Lucy's
mash prompt on the insert card, plays the split insert and then runs both
actions with the stored mash result. Every other duo, and Mark-Lucy with the
insert mode Off, keeps the panels and the prompt on the unit. The QTE factor
mapping is shared by both paths. Time scale returns to 1 on every exit.
```

## How to see it

1. Open `CombatLevelContainerScene` with a squad that has Mark and Lucy (and John or Linda for the comparison duos). Nothing to place: the PlayerController spawns the insert canvas on the first duo.
2. Enter Play mode, trigger Mark–Lucy's duo (Chained Assault), mash Lucy's prompt on the card, watch the insert, then the action.
3. Run the play-check list above. To test Off: select `PlayerController > DuoInsertCanvas(Clone)` in Play mode and set `Mode` to Off.

## Review fixes

From `reports/2026-11-22-duo-insert-c2-review.md`, both should-fix items applied.

1. Inactive sequence: `TryGetDuoInsert` now takes the panels path when the spawned sequence exists but is not `isActiveAndEnabled`, with one warning per handler ("the insert canvas is inactive or disabled; duos use the panels"). The decision helper got an overload `ShouldPlayInsert(sequence, sequenceActive, duoId, out entry)` that takes the active state as a parameter. Unity does not reliably report `isActiveAndEnabled` for components added in Edit mode, so the test passes the flag in rather than reading it. New test `Insert_InactiveSequence_KeepsPanels` checks false gives the panels and true gives the insert.
2. `OnDisable` now calls `ReturnCardQteButton(_cardQteButton)` before clearing the field.

Files and line deltas:
- `Runtime/UnitsCooperationHandler.Insert.cs`: 224 to 242 lines (+18). LF, no BOM.
- `Editor/CooperationInsertTests.cs`: 157 to 166 lines (+9). LF, no BOM.
- No other file changed. The proposed commit file list is unchanged.

Results:
- Compiled clean.
- `CooperationInsertTests`: 14 of 14 pass.
- Duo/cooperation fixtures (same group run as before): 573 of 573 pass.
- Whole EditMode suite: 2457 total, 2456 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit).

New play check (risk): when `OnDisable` runs because the PlayerController is being turned off or destroyed while a prompt is on the card, Unity may refuse `SetParent` during a hierarchy change and log "Cannot set the parent of the GameObject ... while activating or deactivating the parent". If THJ sees that error when leaving combat mid-card, the fix is to skip the reparent in that case. The prompt is force-ended first either way.
