# Duo insert shot: comic sequence test (Mark–Lucy)

Size: M    Tier: 3 (chunk C2 changes a core system's behavior)    Assigned to: miso-implementer
Branch: thj/duo-insert (created 2026-11-22 at THJ's request)
Status: approved 2026-11-22 (THJ: "Approve, start C1"; C2 core change and untracked test clips approved). C1 committed `9e992707f`, C2 committed `5fc81e789` (review APPROVE, both should-fixes applied), C3 docs done. Waiting on THJ's preview and play check.

## Why

THJ, 2026-11-22: the duo insert (sliding avatar panels in `FTPPanel`) should become a short, comic-like animated insert, closer to Lost Crown's Athra Surge splash and Midnight Suns' combo cinematics, filling the screen in two halves. The duo QTE currently opens on the board mid-screen while the panels are up, which makes the screen too busy; it should be its own framed beat. THJ approved the defaults: QTE first, then a diagonal full-screen split, 1–1.5 s, skippable. Design note and current-flow read: `design/duo-insert-shot.md`.

## Goal

Playing the Mark–Lucy duo shows a framed QTE card, then a full-screen two-half comic insert built from the test clips, then the action on the board; every other duo is unchanged.

## Acceptance criteria

- [ ] Mark–Lucy duo, in play: board dims and freezes; Lucy's mash QTE appears inside a framed comic card at a fixed screen spot (not over a unit); the old `FTPPanel` duo panels do not appear.
- [ ] After the QTE ends (pressed or not), a full-screen insert plays: the screen splits on a diagonal, the left half shows Lucy (sprite placeholder with a slow push-in, no clip exists yet), the right half shows Mark's test clip; ink borders, a white impact flash on entry, speed lines, the duo's name as a caption.
- [ ] The insert lasts its configured length (default 1.4 s, unscaled time), holds the last frame ~0.2 s, then clears; the board action then plays as today, with Lucy's ability scaled by the mash result exactly as before (×0.7 to ×1.5).
- [ ] Any key/click after 0.3 s skips the rest of the insert; the action then plays normally.
- [ ] Insert mode on the component: `Full`, `ShortAfterFirst` (first use in a combat full, later uses 0.6 s), `Off` (old panels and old QTE placement). Default `ShortAfterFirst`.
- [ ] Every duo without an insert entry (all others) plays exactly as today: same panels, QTE still on the unit, same order.
- [ ] Clip B's burned-in logos are not visible (cropped by the half's UV rect).
- [ ] Escaping mid-sequence (combat ends, scene unloads) leaves no running VideoPlayer, no leaked RenderTexture, `Time.timeScale` back to 1.
- [ ] EditMode tests below pass; the whole suite passes after C2.

## Scope

In: an insert player component and canvas prefab; a pair → insert data asset; the framed QTE card; Mark–Lucy wired as the only pair; the test clips imported for local testing.
Out: Family Role (solo) inserts and moving the Family Role prompt (follow-up once this test reads well); Family Super Time; a player-facing settings entry (the mode is a serialized field for now); final art, sound, a Lucy clip; the StuntCam actor set (stays off).

## Touches

Systems: Duos `UnitsCooperationHandler` (core), QTE (core, used through its existing `inUI` path, not changed), Combat UI manager (core, read only: `ShowDuoVisual` simply not called for an insert pair), camera (unchanged calls).
USPs: Duos.
Docs: `tech/core-systems.md` (Duos row), `design/gdd/family-systems.md` (Duos: insert + QTE order, marked test/Mark–Lucy only), `design/duo-insert-shot.md` (status), `build-log.md`, `status.md`.

## What the implementer needs to know (read 2026-11-22)

- `UnitsCooperationHandler.ExecuteIE` (Core/Systems/AbilitySystem/Abilities/Runtime): calls `CombatLevelUIManager.Instance.ShowDuoVisual(partners[0].Unit, partners[1].Unit)`, focuses the camera, then runs partners in order (or parallel). `ActivateAbility` per partner: Mark in `Mark_Lucy_Duo` goes to `ActivateMarkLucyBlitz`; a partner with `qteFactor` sets `Time.timeScale = 0` and calls `QuickTimeEventHandler.StartEvent(partner.qteProfile, partner.Unit.UIHook, ...)`; `ActivateFromQte` sets timeScale 1, maps the factor, applies `CoopQteMod` (also to same-entity partners without their own QTE), then activates.
- `Mark_Lucy_Duo` in `Content/Controllers/PlayerController.prefab`: partner 0 is Lucy (`qteFactor: 1`, mash, `inUI: 0`), partner 1 is Mark (blitz).
- `QTEButton.BindPlacement`: when `profile.inUI` is true the button is parented to the hook transform (a UI slot) instead of following a world point. That is how the card hosts the prompt; QTE code is not edited.
- `FactionRoleVisual` / `FTPPanel`: untouched. `HideFactionRoleVisual` is empty today; leave it.
- `com.unity.modules.video` is in the manifest; `TutorialViewManager` already uses `VideoPlayer`.
- Pixel style: no new fonts; reuse the HUD's TMP font for the caption.

## Approach

### C1. Insert player and QTE card (no core code) — sonnet, review with the feature

New files under `Features/UI/DuoInsert/` (namespace `MISO.Features.UI.DuoInsert`):
- `DuoInsertLibrary` (ScriptableObject): entries `{ duoId, leftUnitNickname, left: HalfSource, right: HalfSource, caption, fullLength = 1.4, shortLength = 0.6 }`; `HalfSource = { VideoClip clip, float clipStart, Sprite fallbackSprite, Rect uvRect, bool mirror }`.
- `DuoInsertRules` (pure, static methods only, no state): `TryGetEntry(entries, duoId)`; `LengthFor(mode, entry, usesThisCombat)`; `CanSkip(elapsed)` (≥ 0.3 s); `SideOf(entry, nickname)`.
- `DuoInsertSequence` (MonoBehaviour on its own overlay canvas above the HUD, sorting above `FTPPanel` and the QTE canvas while the card shows): `IEnumerator PlayCardIE(GUnit qteUnit, string title, Action<Transform> withSlot)` shows the dimmer and the framed card (portrait from the unit's existing FR sprite, title, an empty slot transform for the QTE button) and hands the slot out; `HideCard()`; `IEnumerator PlayInsertIE(DuoInsertLibrary.Entry entry)` runs the split: two masked halves (diagonal via a rotated mask or a sliced sprite mask), each a `RawImage` fed by a `VideoPlayer` (render mode API-only/RenderTexture created at runtime at clip size, `timeUpdateMode = UnscaledGameTime`, muted, prepared before the flash) or the fallback sprite with a scale 1.0→1.08 push-in; flash 2 frames, `PS_SpeedLines`/`speedline.mat` reused from `Content/FamilySuperTime/DUO`, caption; skip on any input after `CanSkip`; uses-per-combat count is an instance field (no statics).
- Mode field `InsertMode { Full, ShortAfterFirst, Off }`, default `ShortAfterFirst`.
- `OnDisable`/`OnDestroy`: stop players, release RenderTextures, hide everything.
- A context-menu "Preview Mark–Lucy" that plays card (with a dummy slot) + insert in Play mode, so THJ can judge the look before C2.
- Prefab `Features/UI/DuoInsert/Prefabs/DuoInsertCanvas.prefab`, library asset `Resources`-free, referenced by the prefab. Place one instance in `CombatLevelContainerScene` under the HUD canvas root (small YAML add, or THJ drops it in; the implementer says which).
- Clips: copy the two test MP4s into `Content/FamilySuperTime/DUO/Inserts/_Test/` (`Mark_TestA.mp4`, `Mark_TestB.mp4`); Mark's right half uses clip B with a UV rect that crops the top logos (start ~0.5 s in); keep A as an alternative entry for A/B looks.

Acceptance: compiles; the context-menu preview shows the card, then the split with flash, speed lines, caption, Lucy push-in and Mark's clip without logos; skip works; leaving Play mode mid-preview logs no leak warnings. Tests: `DuoInsertRulesTests` (Editor folder next to it): entry lookup hit/miss, length per mode and use count, skip gate, side lookup.

### C2. Duo flow: QTE card first, insert, then actions (core: `UnitsCooperationHandler`) — opus, its own review

Only when the duo id has an entry in the library and the mode is not `Off`; otherwise the current path runs unchanged.
1. `ExecuteIE`: skip `ShowDuoVisual`; set `Time.timeScale = 0`.
2. Up-front QTEs: for each partner with `qteFactor`, in partner order, show the card (`PlayCardIE`) and start its QTE with the card slot as hook (pass the slot; make the profile's `inUI` true for this call only, e.g. a shallow copy of the profile, so the serialized data and the non-insert path are untouched). Store the resulting factor per partner (mash: `SecondaryFill`; press: 1/0, same mapping as today). Hide the card.
3. `PlayInsertIE(entry)`; then `Time.timeScale = 1`.
4. Camera focus and the partner run as today; `ActivateAbility` uses the stored factor (apply `CoopQteMod` the same way, including the same-entity spread, and invoke `onSuccessfulQTE` only on success) instead of starting a QTE. Mark's blitz path unchanged.
5. A stored-factor helper is a small pure function so it can be tested; keep `ActivateFromQte`'s mapping in one place shared by both paths.
6. Abort safety: if the sequence object is missing, fall back to the old path (log once). A `try/finally`-style guard (coroutine-safe: a flag checked in `OnDisable` of the sequence + timeScale restore) so timeScale returns to 1.
Put the new code in a new partial file `UnitsCooperationHandler.Insert.cs` if the class can be made partial cheaply; otherwise keep the edit small in place.

Acceptance: the Mark–Lucy criteria above in play; John–Mark, Mark–Linda (Catch & Return), and one more duo with a QTE play unchanged. Tests: the stored-factor mapping (mash fill → factor min/max, press success/fail) and "no entry → old path" decision; run the cooperation/duo fixtures, then the whole EditMode suite.

### C3. Docs and handoff (coordinator)

core-systems Duos row, GDD Duos note (test, Mark–Lucy only), design note status, build log, status.

## Risks

- **Core behavior (Tier 3):** C2 moves the QTE ahead of the actions for insert pairs. Limited to pairs with a library entry and mode ≠ Off, so every other duo keeps today's order. Needs THJ's OK before dispatch.
- **timeScale:** the card and insert run while time is 0; everything in them uses unscaled time (`WaitForSecondsRealtime`, VideoPlayer unscaled, animator `UnscaledTime`). Restored on every exit path.
- **Statics:** none planned. Uses-per-combat lives on the scene instance. If the implementer adds any static, it needs `ResetPlayModeState` and a line in `PlayModeStaticReset.Reset()`.
- **Serialized data:** no field renames. New fields only on new types. The QTE profile is copied, not edited.
- **Scenes/prefabs:** one prefab instance added to `CombatLevelContainerScene`; small YAML add or THJ places it. THJ has `PreloadScreen.unity` and settings changes uncommitted; agents leave them alone.
- **Test media in the shared repo:** clip B has Children of Morta and Prince of Persia logos burned in. Proposal: the `_Test` clips are not committed (left untracked); the library's entries reference them locally. Commit only code, prefab and the library asset; THJ decides whether any clip goes in later.
- **AI:** no AI graph, AI ability or unit prefab changes; `AIRegressionTest` not needed.
- **Other branches:** none active besides `main`.
- **Repeat fatigue:** handled by `ShortAfterFirst` and skip.

## Gates

Compile / EditMode: `DuoInsertRulesTests` (C1), cooperation fixtures + stored-factor tests + full suite (C2) / review: C1 with the feature, C2 its own (core) / play check: yes, THJ's time (C1 preview look, then C2 in a combat with Mark–Lucy plus two other duos) / docs: C3 list. Commits: C1 and C2 separate (C2 revertable alone), each with its `.meta` files, shown to THJ per CLAUDE.md.

## Follow-up F1 (THJ, 2026-11-22, after reading the results; not played yet)

THJ: "yes skip the player's own qte key. make the duration a bit longer. tell me where they are if I can tune them." Plus start and end transitions instead of the halves just appearing and disappearing, two ideas: (a) one character fills the screen, then the screen halves on the diagonal while the other fills its half; (b) both start from their sides and meet in the centre, then go back out. THJ didn't pick one, so both get built as a per-entry style for an A/B look (like clip A/B).

### F1a. Insert player: transitions, longer timing, tunables, skip filter (feature code, no core) — opus, review with F1b

Files: `Features/UI/DuoInsert/` (`DuoInsertSequence.cs`, `DuoInsertLibrary.cs`, `DuoInsertRules.cs`, `DuoInsertHalfGraphic.cs` if needed, the library asset, the prefab if new serialized fields need values, `Editor/DuoInsertRulesTests.cs`).
- New per-entry `InsertTransition transition` enum: `SoloThenSplit` (default for `Mark_Lucy_Duo`) and `SlideFromSides` (default for `Mark_Lucy_Duo_ClipA`, so both are visible from the two existing preview menus; also add preview menus that force each style on the main entry).
  - SoloThenSplit, in: the lead half (new per-entry `leadSide`, default Right = Mark's clip) starts full screen with the flash; then its inner edge sweeps to the diagonal while the other half wipes in from its screen edge to the diagonal (ease-out, ink border along the moving edge). Out: hand-over, the other half sweeps across to full screen and the lead is pushed off, then a quick fade.
  - SlideFromSides, in: both halves start off-screen on their own sides and slide in, meeting on the diagonal with the impact flash at contact. Out: both slide back out to their sides, with a fade.
  - The picture must not squeeze or re-crop while a half's polygon moves: the half's picture window is computed against its final (settled) polygon or a fixed frame, not the animated polygon's bounds.
- Timing (new defaults, all in the library entry unless said): `fullLength` 1.4 → 2.0 s (the settled split), `shortLength` 0.6 → 0.9 s, new `transitionIn` 0.35 s and `transitionOut` 0.3 s; short plays scale both transitions by 0.6. The hold on the last frame 0.2 → 0.3 s.
- Move the timing constants in `DuoInsertSequence` that a designer would tune (card pop, flash fade, hold, sprite push-in, speed-line speed) to serialized fields with tooltips on the component (values on the prefab); keep the technical ones (prepare/seek timeouts) as constants. Skip delay (0.3 s) stays in `DuoInsertRules` but becomes a serialized field on the component passed in, or stays a const: implementer's call, say which.
- Skip: `PlayInsertIE(entry, IReadOnlyList<InputAction> ignoreActions = null)`. A press on any control bound to one of the ignored actions never skips; any other key/click/pad button still skips after the delay. A skip plays a fast out (about 0.12 s) instead of a hard cut.
- Pure, testable pieces in `DuoInsertRules`: phase timing (which beat at time t for a length, transitions and short scale) and the polygon edges per style and phase. Tests for both, plus the ignored-control filter if it can be tested without devices (otherwise say so).
- No statics. Keep LF line endings and no BOM in the new files (match the existing ones).
Acceptance: compiles; both preview menus show their style in and out; picture doesn't stretch during the moves; existing rules tests updated for the new defaults; leaving Play mode mid-transition leaves nothing behind.

### F1b. Duo flow passes the QTE's own action (core, one call) — with F1a's review

`UnitsCooperationHandler.Insert.cs`: resolve each card QTE's `bindingActionID` through `PlayerInputController.Instance.GetInputAction` (as `QuickTimeEventHandler` does) and pass the collected actions to `PlayInsertIE`. Nothing else in the core changes. THJ approved this ("yes skip the player's own qte key").

Commits: F1a and F1b separate (F1b revertable alone); F1a works on its own (null = no filter).
Gates: DuoInsertRulesTests + CooperationInsertTests + whole EditMode suite; review; THJ's play check (the existing list plus: both transition styles, mash through the card and into the insert without skipping, another key still skips).
