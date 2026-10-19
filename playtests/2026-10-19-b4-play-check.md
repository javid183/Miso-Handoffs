# Play check: Family Role readability (B4 Phases 0 and 1) plus the Batch 1 items still unseen

Branch `thj/fr-readability`. Plan: `plans/2026-10-18-family-role-phase0-1.md` (commit hashes in its log); design: `plans/2026-10-18-family-role-readability-design.md`; decisions D-062 to D-072. Needs THJ's time (it takes over the editor). Start Play from `Scenes/PreloadScreen.unity`; load levels with the toolbar level picker (LevelE3-C1 = *In My Father's Arms*); `Tools > Save Data > Clear Save Data` if a save blocks a check (allowed, say so in the report). Cheats: `[` is -1 HP and Shift+`[` is -10 on the hovered unit, K wins the fight. Quiet checks are already green (suite: all pass except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`). One Unity assert "unexpected guid mismatch" appears after a refresh (no stack trace): note whether it persists after a Unity restart.

Colours (placeholders): John dark brown, Linda sky blue #56B4E9 (default), Lucy red, Mark very dark brown. Judge readability against the grid.

## A. Phase 0 bug fixes

- [ ] **F3 busy QTE:** trigger a role while another QTE is up (e.g. a duo or synergy QTE) so the role is skipped. **Pass:** no hang; camera, timeScale and pause return to normal; the same enemy can trigger that role on a later event the same turn (it is not muted). A real no-press still mutes that enemy for the rest of the turn.
- [ ] **F5 Lucy factions:** in a level with more than one hostile faction (if one exists), Lucy's ember can pick an enemy of any hostile faction. If no such level is reachable, mark Not run.
- [ ] **F1 null guard:** the first role trigger of a fresh level, before any unit selection change: no exception in the console.
- [ ] **Mark's key (R1):** Mark's role prompt and his Continuous Attack prompt use Mark's QTE binding (left mouse); no console errors.

## B. Phase 1 UI

- [ ] **Zones (A):** select John (diamond including the four diagonal neighbours, not the (2,1) cells), Mark (diamond), Linda (lines along her row and column to radius 4), Lucy (radius-3 area). Zones are faint outlines, readable, and gone when deselecting, ending the turn, a unit dying, or the level ending. Move the selected unit: the zone redraws after the move. Untick `Show Role Zone` on a handler: no zone (and no cover icons) for that unit.
- [ ] **Shift view (C):** hold Shift: every living Bergson's zone in its own colour, overlapping outlines distinguishable; hover one Bergson with Shift held: only that zone; release: back to the selected unit's zone. Works during an enemy turn without errors (hover-to-isolate may not work then).
- [ ] **Shift hover preview layer:** with nothing selected, Shift-hover a unit: its move and attack cells show softly; release or unhover clears them. With a unit selected and its range lit, Shift-hover a nearby unit and release: the selected unit's range stays lit. Hover the selected unit itself with Shift: its range stays. A 2x2 unit looks right. Note any stuck tile. Known and accepted: starting ability targeting while Shift-hovering can leave the preview until release.
- [ ] **Cover icons (B):** select Lucy (or any non-role unit), enter the move preview and hover tiles: a shield appears inside John's zone; a fist only when EVERY melee-adjacent free cell of that tile is inside Mark's zone (strict rule). Select John or Mark and preview a move: their zone follows the hovered tile, their current zone stays; no cover icon on their own destination. Leaving the grid, cancel, confirm, Tab, end turn: nothing stays behind. During the enemy turn: no icons.
- [ ] **Badge (D):** select a unit with a role: a small pip beside the role icon, green when shared FTP is at least 1, dim red at 0 (use the cheats or play until FTP is spent). Hover the role icon at 0 FTP: the tooltip has the extra line "Needs 1 FTP; Pass-by refills FTP." and the range cells still highlight on hover. A unit without a role (Toba) shows no pip. Switching units leaves no stale pip.
- [ ] **John's tether (F):** make an enemy attack an ally inside John's diamond with FTP at least 1: while the paused prompt is up, a thin line connects John to the ally he would cover; it disappears after the press or expiry. No tether during the duo QTE, Catch & Return, Command Shield Dash or the reversion QTE.
- [ ] **Barks (E):** each role's prompt shows a short line over the unit: John "No!", Linda "In my sights.", Lucy "Leave some for me!", Mark "Not my family."; on a press the execute line shows over the same unit ("I got you!", "Clean shot.", "Catch this!", "Breathe. Strike.") and the insert plays as before (1.28 s, no dialogue hold). Check how the execute line reads next to the fading prompt line (if it stacks badly, give it a short delay). John's "No!" shows during his paused prompt. Let a prompt pass without pressing: a neutral decline line shows ("Hold fast." / "Not this one." / "Next time!" / "Patience."; the second one later in the fight), at most once per role per turn, never "too slow". Untick `Play Decline Bark` on a handler: no decline for that unit.

## C. Batch 1 items still unseen

- [ ] **B3:** a living unit at a fractional HP between 0 and 0.5 shows at least 1 on the bar (try a modified-damage hit on a nearly dead unit); the damage preview and the mission character icons still read right.
- [ ] **B6 mission map:** a non-linear mission's mission map (e.g. M4, M6, M11, M14 are candidates) with its info panel fully on screen at 16:9, 16:10 and 4:3.
- [ ] **B8:** a tutorial that fires at a turn change or mid player turn, if one can be reached (the Level 1 start tutorials were already seen working).
- [ ] **Safe rooms (B7):** read the objective text in Daryani's Wares ("Choose one of Daryani's wares, then reach the exit."), Anahita's Ashiyan ("Approach the glowing statue to heal, then reach the exit.") and Mithra's Gift ("Take the Divine Relic from the altar, then reach the exit."): it fits the HUD box, and the exit counts as Success. Daryani's room shows the name "Daryani's Wares" on the map node, the map panel and the HUD, and its layout may differ from before (the name seeds the variants).
- [ ] **Lucy's rule (D-066):** Lucy's ember does not follow the Mark–Lucy Duo or Mark's Command attack.

## Report

`reports/b4-play-check.md` (template `templates/report.md`): each line Pass, Fail or Not run with evidence, new findings, whether the save was reset, and the screenshots described for any visual judgement (colours, overlap, readability).
