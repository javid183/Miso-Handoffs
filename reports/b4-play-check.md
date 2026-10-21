# Report: B4 Family Role readability play check (sections A, B, C) + Masher play check

Plan: plans/2026-10-18-family-role-phase0-1.md    Agent: Claude (main session, computer use)    Branch: thj/fr-readability (not switched)
Outcome: partial (four runs)

Checklists: `playtests/2026-10-19-b4-play-check.md` (A, B, C) and `playtests/2026-10-20-masher-play-check.md`.
`playtests/2026-10-20-preview-pass-play-check.md` was **not re-run**: THJ confirmed every item on it on 2026-10-20 ("the preview pass is done") and chose to skip it when asked at the start of this session.

Editor 6000.3.4f1, Play entered from `Scenes/PreloadScreen.unity` via the toolbar level picker.
**Three runs:**
- Run 1 — `LevelE3-C1`, squad John, Mark, Linda. Linda down in R2, wipe in R3.
- Run 2 — `LevelE3-C1`, squad John, Mark, Toba (Toba added as a genuine non-role unit). Toba down in R3, wipe in R3.
- Run 3 — `LevelM1-C3` *The First Path (3/3)*, squad John, Mark, Linda, Lucy (this level offers **four** placeholder slots and no intro sequence). Stopped voluntarily in R2.
- Run 4 — **THJ's actual save**, played from PreloadScreen through Home → world map → mission 6 *The Arcanum*, squad John, Linda, Lucy. Level 1 cleared, mission map reached, Mithra's Gift safe room entered. Stopped voluntarily.
- Run 5 — same save, The Arcanum replayed from level 1 (mid-mission progress is not saved), Mithra's Gift taken again and completed through the exit.

Evidence is Game-view screenshots, zoomed captures at native resolution, `Editor.log`, and the three fights' combat logs under
`...\LocalLow\Dead Mage\miso\CombatLogs\` (`20261021-012106_*`, `20261021-021607_*`, `20261021-022930_The_First_Path.*`).

**Coverage warning:** still roughly a quarter of the two checklists. Everything I did not actually see is marked **Not run**, never inferred.

## What changed

- `claude-handoff/reports/b4-play-check.md`: this report. No code, asset, scene, prefab or git changes.
- Editor state touched and restored: Game-view Scale slider moved to 2.2x and back to 1x; Console warning filter toggled off and back on; Hierarchy search used and cleared; Game/Scene tab switched back to Scene; level picker switched to `LevelM1-C3` for run 3 and **set back to `LevelE3-C1`**. Editor left in Edit mode on PreloadScreen, no unsaved changes, Console **0 errors**.

## Three limits that shaped these runs

1. **I cannot hold a modifier key across a screen capture.** The remote bridge serialises actions, so Shift is always released before the screenshot is taken (verified as separate calls and inside a single batch). Every Shift-dependent criterion is **Not run**, not failed.
2. **The Editor.log was rotated at the start of the session.** `computer_open_application` launches a second Unity rather than focusing the running one; two short-lived Unity processes started and exited cleanly (return code 0) at 01:16 and 01:18, overwriting the log's earlier content. Live output from 01:18 onward is intact. No project files were touched.
3. **Role QTE prompts last about 2–3 seconds** and my round trip is 2–4 s, so prompts frequently expired before my click landed. Several role triggers therefore produced a prompt but no executed role (the combat log only records a role that takes the hit). The editor's own Pause button *does* freeze a live prompt and is the only reliable way to inspect one.

**A caveat on my own input, so nobody chases a ghost:** in run 3 I could not get an *ability* attack to execute by clicking the target twice (it works for moves). The same failure happened against an archer as against the Masher, so this is my input technique, **not** a game bug. Nothing below is reported as a failure on that basis.

## Acceptance criteria

### A. Phase 0 bug fixes

- [ ] **F3 busy QTE — Not run.** No role trigger ever overlapped a second QTE. Run 2 did produce Synergy QTEs (the jsonl records 2 `Synergy` events in R1), so landing a role trigger during a live Synergy prompt is the way to set this up.
- [ ] **F5 Lucy factions — Not run.** Lucy was finally in the squad in run 3, but `LevelM1-C3` has a single hostile faction and I stopped in R2.
- [ ] **F1 null guard — Not run.** Run 2 was set up precisely for this: fresh level, Toba auto-selected, **no selection change at all**, End Turn pressed immediately. But the combat log shows **no Family Role fired in R1**, so the "first role trigger" condition was never met. Supporting evidence only: **0 console errors across all three runs**, and no genuine `Exception` / `NullReference` / `error CS` in `Editor.log` (the six `NullException` substring hits are all inside the DOTween safe-mode warning text, finding 1).
- [x] **Mark's key (R1) — Pass on the binding, Not run on Mark's own prompt.** Data: `Unit_Mark.prefab` carries `bindingActionID: MarkQTE` at three sites (lines 2786, 2922, 2985 — the role prompt and the Continuous Attack passive), and `Assets/Settings/Input/InputSystem_Actions.inputactions` maps `MarkQTE` → `<Mouse>/leftButton`. In play the QTE glyph is a mouse-button icon and a left click answers the prompt. **0 console errors.** Across three runs the only roles that ever fired were John's and Linda's; Mark's own prompt was never seen.
  - Loose end: `PlayerController.prefab:1447` still carries `bindingActionID: LucyQTE` (alongside a `MarkQTE` entry at line 2119). Worth confirming that is deliberate.

### B. Phase 1 UI

- [~] **Zones (A) — Pass for John, deviates from the checklist for Mark and Linda.**
  - **John: Pass.** Zone draws on selection as faint outlined shield glyphs in the tile corners. Shape verified by native-resolution zoom on a clean 2x2 block: the orthogonal and diagonal neighbours carry the glyph and the (2,1) cell does **not** — the radius-2 diamond including the four diagonals, excluding (2,1), exactly as specified.
  - **Follow zone on move preview: Pass.** The zone redrew from the ghost tile and the old zone cleared — confirmed by a tile in the ghost's zone but not John's current one gaining a glyph, and a tile in John's current zone but excluded from the ghost's zone losing one.
  - **Mark: correction — his zone IS drawn, I could not see it.** I originally reported that selecting Mark draws no zone. THJ confirms Mark does *not* hide his zone (only Lucy and Linda do) and that his zone colour is near-black. At capture resolution I could not distinguish it from the floor and wrongly concluded it was absent instead of recording that I could not tell. Treat Mark's zone as **present and unverified for shape**, and treat the near-invisibility as part of finding 3, not as a behaviour difference.
  - **Linda and Lucy: hide confirmed.** They show no zone on selection; it appears on badge hover or with Shift held, matching the preview-pass rule (P5) rather than the B4 text.
  - **Open question raised by the above:** Mark's *badge* tooltip ends with *"Same tiles as the basic attack; Shift shows them."* — the Linda/Lucy hide wording. If Mark does not hide, that line appears to be wrong on him. (His hotbar *ability* tooltip does not carry it.) Worth checking.
  - My reading: the B4 "Zones (A)" line is out of date for **Linda and Lucy**, which now hide by the later preview-pass rule. Mark is not a deviation — that was my error.
  - [ ] Lucy's radius-3 area — **Not run.** Lucy was in the run 3 squad but I never selected her before stopping.
  - [ ] Zone cleared on deselect / end turn / death / level end — **Not run.**
  - [ ] `Show Role Zone` untick — **Not run.**
- [ ] **Shift view (C) — Not run.** See limit 1.
- [ ] **Shift hover preview layer — Not run.** See limit 1.
- [ ] **Cover icons (B) — Not run.** Attempted in runs 1 and 2 and defeated by the board each time: the reachable tiles inside John's zone sat under the HUD ability bar, the camera panned between actions, and by the turn John's zone had open ground **no member of the party had a single legal move**. No shield was observed on any destination, but I never got a valid move preview onto a confirmed zone tile, so this is **not** a Fail. Still the most important item for a next run.
- [~] **Badge (D) — Pass on the ready state and the no-role case.**
  - [x] Green pip beside the role icon at shared FTP ≥ 1: **Pass** (John and Mark).
  - [x] **A unit without a role (Toba) shows no pip: Pass.** Toba's unit panel has no role badge and no pip at all, against John's blue shield badge + green pip and Mark's red badge + green pip in the same run.
  - [x] No stale pip when switching units: **Pass (weak)** — several cycles across three runs left no leftover pip.
  - [ ] Dim red pip at 0 FTP, and the "Needs 1 FTP; Pass-by refills FTP." tooltip line: **Not run.** FP never reached 0.
- [x] **John's tether (F) — Pass. Legibility depends heavily on the map.** With an enemy attacking an ally inside John's diamond and FTP available, the combat log records e.g. `↳ John (7,-3) › Family Role: John's FR → Mark (takes the hit)` and `✦ Wrath · John: took the hit for family: 1 stack(s)`. I froze the editor mid-prompt and searched the Hierarchy: **`JohnTether_0` and `JohnTetherCap_0` were present and active**, one pair for the single covered ally. It is gone in the frames after the press.
  - **On `LevelE3-C1` (dark cave floor) it is close to invisible** — a thin desaturated line that I first mistook for level art, with the red prompt box sitting on top of it; I had to confirm the cap from the Hierarchy rather than the screen.
  - **On `LevelM1-C3` (lighter brown ground) it reads clearly** as a curved tan/orange arc from John to the covered ally. So the tether itself is fine; the contrast against dark levels is the problem. Worth tuning the colour or adding an outline rather than changing the shape.
  - [ ] No tether during the duo QTE, Catch & Return, Command Shield Dash or the reversion QTE: **Not run.**
- [~] **Barks (E) — Pass for the lines I saw, rest Not run.**
  - [x] John prompt bark **"No!"** — Pass, seen in all three runs, and it shows during his paused prompt as required.
  - [x] John execute bark **"I got you!"** — Pass, on the press, over the same unit, with the cinematic insert (screen dims, spotlight on John).
  - [x] Linda prompt bark **"In my sights."** — Pass (runs 1 and 3).
  - [~] **Execute line next to the fading prompt line — mixed.** In the clean John case the prompt box had cleared before the execute line appeared. But run 2 produced a frame with **two floating lines stacked about one tile apart** — "Another moment." over Toba directly above "No!" over John, with John's prompt still live. Readable, but tight, and exactly the crowding the checklist worried about.
  - [ ] Lucy and Mark lines: **Not run** (neither role ever fired).
  - [ ] Decline barks, the once-per-role-per-turn limit, the absence of "too slow" wording: **Not run.** I deliberately let prompts expire and never caught a decline line in a frame, but at a ~2 s cadence it may simply have fallen between captures. Genuinely unknown.
  - [ ] `Play Decline Bark` untick: **Not run.**
  - Note: **"Hang in there." and "Another moment." are not Family Role barks.** They appear over Toba, who has no role, with no role event in the jsonl. Don't mistake them for the role lines.

### C. Batch 1 items still unseen

Run 4 was done the way THJ specified: from PreloadScreen on the current save, via the map to mission 6 (*The Arcanum*).

- [~] **B3 — damage preview Pass; fractional case not reproduced.**
  - [x] **Damage preview shows expected future HP: Pass.** Linda aiming at a Dark Claw at full health previewed **`9/16`** with the predicted loss drawn as a red segment; the resulting hit was exactly `-7 HP (16→9)` in the combat log. A second preview (run 3) showed the Masher at `76/80` and an archer in the line at `17/24` simultaneously.
  - [x] **Mission character icons read right: Pass.** On the mission map the party icons showed `0/37` (John, downed), `23/23` (Linda) and `11/17` (Lucy) — correct in each case, including 0 for a genuinely downed unit.
  - [ ] **A living unit at fractional HP between 0 and 0.5 showing at least 1: Not run.** THJ expected damage to be fractional at the current faction damage modifiers, but every number I saw in this mission was a whole number (`-7`, `-16`, `-9`, `-6`). The combat log prints exact values and never showed a decimal, so I could not engineer the sub-0.5 case. Either the fractional modifiers apply somewhere other than The Arcanum's faction matchup, or they are not active on this save.
- [x] **B6 mission map at 16:9 / 16:10 / 4:3 — Pass, with a separate defect found.** The mission map appears **between** levels, not before the first one, which is why earlier sessions never saw it. Selecting a route node opens the info panel (name + objective). The panel, the Legend and the party icons are **fully on screen at all three ratios**.
  - **New defect: the node graph is clipped at 4:3.** The first node (left) and the last node (right) are cut off by the map frame — only a crescent of each is visible, confirmed by native-resolution zoom on both edges. At 16:9 and 16:10 every node is fully visible. The criterion as written is about the info panel, so this is a Pass plus a new bug rather than a Fail.
- [x] **Safe rooms (B7) — Mithra's Gift Pass; other two Not run.**
  - **Mithra's Gift:** the route node panel reads *"Mithra's Gift — Take the Divine Relic from the altar, then reach the exit."*, the level HUD title reads **Mithra's Gift**, and the in-level Objectives box reads **"Take the Divine Relic from the altar, then reach the exit."** — exactly the expected wording, laid out over three lines **well inside the box, no clipping or overflow**.
  - [x] **"The exit counts as Success": Pass.** Took the relic off the altar (it disappears from the board and the mid-room sequence fires), then moved onto the exit tile: the Victory card appeared reading *Level Successfully Finished!* with the objective line *"Take the Divine Relic from the altar, then reach the exit"* marked **Success** in green. The full objective text wraps onto two lines on the Victory card and is not clipped.
  - [ ] **Anahita's Ashiyan: Not run** — it sits **one hostile level past Mithra's Gift** on the mission map, so it is roughly one level of play away from the current save. Daryani's Wares is not in this mission's legend at all and needs a different mission.
- [ ] **B8 tutorial at a turn change or mid player turn — Not run.**
- [ ] **Lucy's rule (D-066) — Not run.** Lucy was in the squad but Mark was not, so the Mark-Lucy Duo and Mark's Command could not be exercised.

### Masher play check

- [x] **1. No "did not initialize its role ability" warning on Masher spawn — Pass.** A Masher is in all three runs' LOADOUT (`MasherGoblin #12-m02` on E3-C1, `MasherGoblin #09-00` 80 HP on M1-C3); `Editor.log` has **zero** occurrences of that string across the whole session and **three separate level loads**, and the Console finished at 0 errors. The Batch 1 play report from 2026-10-18 recorded this warning firing, so this is a real change.
- [~] **2. Masher unit panel shows a Family Role badge — present, title not readable.** Hovering the Masher shows its panel with the health bar and two small icons beneath it, the right-hand one looking like a role badge. No tooltip appeared when I hovered that icon. On your open question: I'd lean toward hiding it on enemies, since a badge invites the player to look for a pip and tooltip that do not behave like a Bergson's.
- [ ] **3. Hover preview while aiming — not drawn.** Aiming Linda's Bow Attack at the Masher from 5 tiles showed the target highlight and the damage preview (its bar previewing `76/80`, and the archer in the line previewing `17/24` with a red segment) — but **no step ghost, no path, and no slam tiles**, and no damage shown on units around it. The same was true aiming Mark's Fist Blitz, which would have ended adjacent and so should have shown the slam cross. At 5 tiles the absent *slam* is correct per the rules, but the **step ghost and path should still have been drawn and were not**.
- [ ] **6. Ranged pull — does not happen.** Linda hit the Masher from **5 tiles in the same column** (`Linda (9,-4) › Bow Attack → (9,1) MasherGoblin #09-00`). The combat log records only `ArcherGoblin #09-m01 -7 HP` and `MasherGoblin #09-00 -4 HP (80→76)`: **no step, no drag, no counter of any kind**. Expected per the checklist: dragged 1 tile toward the striker.
- [ ] **4, 5, 7–31 — Not run.** No Bergson reached melee range of the Masher in any run.
  - One relevant scrap from run 2: John's role covering a non-role ally (`John's FR → Toba (takes the hit)`) cut the incoming hit from 6 to 3 on John and granted a Wrath stack — the reduction behaviour item 26 expects of the relay, observed on an ordinary attack.

**Why items 3 and 6 did not happen: unknown.** An earlier version of this report asserted that the Masher's `Immovable` trait was the cause. **That was a guess presented as a finding and it is retracted** — THJ confirms `Immovable` blocks forced movement from Mark's move command and Toba's provoking presence/gambit, and does **not** block the Masher's reactive movement. I had no evidence linking the trait to the missing counter: I never read the counter code, never checked what the trait gates, and never tested it in isolation. The observation below stands on its own and still needs explaining.

Things worth actually testing next, rather than assuming: whether the counter requires the Masher to be activated or aggroed first; whether `counterCanProvokeFamilyRoles` or the counter preset is set on that level's Masher instance; and whether Linda's Bow Attack clipping the archer first changes which unit it treats as the striker.

## Save reset

**No.** The save was never cleared. Run 4 was played on THJ's existing save: level 1 of The Arcanum was completed and the Mithra's Gift route taken. John was killed mid-level by my misuse of the K cheat (finding 9) and was restored to the party when the level ended. Run 5 replayed The Arcanum from level 1 (mid-mission progress is not saved) and completed level 1 plus the Mithra's Gift room, so the save now sits on that mission's map with the party at full HP. Nothing else about the save was altered and it was never cleared.

## New findings

1. **DOTween safe-mode failures on destroyed objects.** **Six** `Tween startup failed … has been destroyed but you are still trying to access it` captures, plus a closing `DOTween safe mode captured 1 errors` summary. Five are `RectTransform` and fire around a unit dying; one is a `CanvasGroup` at level teardown/load. One carries a full stack:
   `ATBGaugeViewMarker.Set(bool)` → `ATBGaugeView.RefreshMarkers()` → `ATBGaugeView.HandleFillChanged(float)` ← `ATBGauge.ApplyFill` ← `ATBGauge.Tick` ← `GUnit.Update()`, tweening `DOFade` on a destroyed `Image`.
   Two things worth a look: the view is not detaching when its unit is destroyed, and `GUnit.Update` is still ticking an **ATB gauge** on a branch that runs on FTP. Warnings only today, but it is a destroyed-object access on essentially every death.
2. **The Masher counter did not fire on a ranged hit, cause unknown.** Observation only — see the Masher section. An earlier draft blamed the `Immovable` trait; that was retracted as an unevidenced guess.
3. **Role-zone and cover glyphs are very low contrast.** John's shields and Mark's fists are small dark-orange / dark-grey outlines in the tile's top-left corner, over a dark mottled floor already carrying move-range frames, threat swords and unit sprites. I needed native-resolution zooms to tell present from absent. **The clearest readability problem in the pass.**
4. **The tether's legibility is map-dependent** — near-invisible on `LevelE3-C1`'s dark floor, clear on `LevelM1-C3`'s lighter ground. Suggests a contrast/outline fix rather than a redesign.
5. **Enemy HP readout is ambiguous at its rendered size.** The Masher's `80/80` reads as `00/00` — the pixel font's 8 and 0 are near-identical at that scale. Relevant to B3 from the opposite direction: a unit at full health can *look* like it is on 0.
6. **The "unexpected guid mismatch" assert did not appear.** 0 errors across all three runs. I cannot answer the "does it persist after a Unity restart" part, because the log rotation removed the pre-01:18 history and I did not restart Unity deliberately.
7. **`LevelM1-C3` is a much better play-check harness than `LevelE3-C1`**: four squad slots instead of three, no intro sequence to click through, an open board, and the Masher in Linda's line of fire from turn 1.
8. **The Masher did not act at all in R1 of run 3** — no move, no attack in the enemy phase, while every other enemy acted. Possibly correct (nothing in reach), but worth a glance.
9. **The `K` cheat kills the hovered unit — it does not win the fight.** `tech/editor-checks.md` records it as "K wins the fight" (carried over from the Batch 1 session, which presumably only ever hovered enemies). Hovering John and pressing K produced `CHEAT Kill → John … -37 HP (37→0) DOWN`. It should read: **K kills whatever unit is under the cursor, allies included.** A unit killed this way is back at full strength after the level ends, so it does not corrupt the save.
10. **The mission map only appears between levels**, after the first level of a multi-level mission is finished — not when the mission is launched. Worth stating in the checklist, since two earlier sessions looked for it at launch and recorded it as unreachable.
11. **The Arcanum level 1 fields reinforcements per turn, not a fixed set.** The opening LOADOUT lists six opponents, but Dark Claws keep spawning `by level` at the start of each enemy phase; clearing it took three turns of kills even with the cheat. Worth knowing when estimating how long a play check on this mission takes.
12. **Mid-mission progress is not saved.** Stopping Play inside The Arcanum put the save back to the mission's start, so run 5 had to replay level 1 before it could reach the mission map again. A play check that needs a mid-mission state has to reach it in one sitting.

## Decisions I made

- Skipped the preview-pass checklist on THJ's instruction (already signed off).
- Run 1 squad for three different zone shapes; run 2 swapped Linda for Toba to get a non-role unit; run 3 moved to `LevelM1-C3` to get four slots and a reachable Masher.
- In run 2, ended turn 1 without touching selection to set up F1; it did not pay off because no role fired in R1.
- Judged Mark's and Linda's missing selection-zones against the branch's actual behaviour rather than the B4 text.
- Stopped run 3 voluntarily in R2 rather than grind several more turns, once the Masher's `Immovable` finding was confirmed and the remaining items clearly needed a different setup.
- Did not toggle `showRoleZone` / `playDeclineBark` in the Inspector; the brief said no asset edits.

## Needs THJ

1. **Why the Masher counter did not fire on Linda's ranged hit.** Observation in the Masher section; I have no supported explanation and will not guess again. Quickest checks are the counter preset / `counterCanProvokeFamilyRoles` on that level's instance, and whether the Masher must be activated first.
2. **Shift items.** Two B4 criteria and several Masher ones need Shift held during capture, which I cannot do. Either you hold Shift on cue in a follow-up and I capture, or they stay permanently Not run for any Claude-driven play check.
3. **Is the B4 "Zones (A)" criterion superseded?** Mark and Linda now hide their zone unless the badge is hovered or Shift is held. If that is the intended end state, rewrite the checklist line; if not, it is a regression from the preview-pass merge.

## Docs to update

- `playtests/2026-10-19-b4-play-check.md`: rewrite the "Zones (A)" line for Mark and Linda; note that `LevelE3-C1` has only three squad slots, so Lucy and Toba items compete for one.
- `playtests/2026-10-20-masher-play-check.md`: record that the ranged counter did not fire in a clean turn-1 test on `LevelM1-C3` (cause unknown), and name that level as the harness (four slots, open board, Masher in range turn 1).
- `tech/editor-checks.md`: add the practical notes from this session — the toolbar picker's ▶ only opens the Assign Placeholders dialog from **Edit** mode; `computer_open_application` launches a second Unity instead of focusing it (and rotates `Editor.log`); the camera pans whenever the cursor nears a screen edge; all QTE bindings are `<Mouse>/leftButton`, so a left click answers any prompt; the QTE window is ~2–3 s and only the **editor's** Pause freezes it; the combat log in `LocalLow\Dead Mage\miso\CombatLogs` records Family Role events by name (`↳ <unit> › Family Role: … → <ally> (takes the hit)`) and is far better evidence than screenshots for the mechanical criteria; `LevelM1-C3` is the better harness.
- `build-log.md` / `playtests/2026-10-playtest-tasks.md`: coordinator, to mark the items above as seen in play and leave the rest open.

## Risks and loose ends

- The bulk of both checklists is still unseen. A next run should: start on `LevelM1-C3`, do the cover-icon test in the first two turns before the board closes, and settle the `Immovable` question before attempting the Masher counter items.
- `PlayerController.prefab:1447` still references `LucyQTE` — confirm it is deliberate.
- The ATB-gauge-on-an-FTP-branch question in finding 1 may be a wider cleanup than this plan.

## Proposed commits

none (no project files changed)

## Other branches

none

## How to see it

1. Toolbar level picker → `LevelM1-C3` → ▶ (from Edit mode) → Assign Placeholders (four slots) → Load Scene. No intro; you are in turn 1 immediately.
2. Masher traits: hover it — `Immovable` and `Reckless` cards appear on the right.
3. Ranged pull: select Linda, basic attack, fire at the Masher from range; read the combat log — damage only, no step.
4. John's zone: select John, zoom the four tiles up-right of him — orthogonal and diagonal neighbours carry a faint shield, the (2,1) cell does not.
5. Mark's zone: select Mark and look very closely at the tiles around him — the zone is drawn in near-black and is easy to miss. Hovering his role badge makes the glyphs legible.
6. Tether: End Turn, and about 3–4 s in press the **editor's** Pause while John's red "No!" prompt is up; search the Hierarchy for `tether` to see `JohnTether_0` / `JohnTetherCap_0`. Compare how it reads on `LevelM1-C3` versus `LevelE3-C1`.
