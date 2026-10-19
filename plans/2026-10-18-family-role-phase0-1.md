# Family Role readability: Phase 0 bug fixes and Phase 1 UI pass (B4, part of Q7)

Size: M    Tier: 3 (approved, D-062, D-063)    Assigned to: miso-implementer (one chunk per run)
Branch: thj/fr-readability (from `thj/oct-build-fixes` = `main`, FTP)
Status: approved by THJ 2026-10-18; chunks R1 to R6 below (R3 and R6 wait on inputs)

Design: [`plans/2026-10-18-family-role-readability-design.md`](2026-10-18-family-role-readability-design.md). Facts: [`reports/b4-family-role-facts.md`](../reports/b4-family-role-facts.md). Everything else in that design (reason-code event, rule changes, queue, Watch wording, Alt view if needed) is batched into the later Family Role chunk (D-062).

## Why

Players can't tell why a Family Role did or didn't fire; the roles also have a few bugs that make them skip silently.

## Goal

Fix the five role bugs and add a UI-only clarity pass (zones, cover icons, badge, tether line, barks) without touching how roles decide to fire.

## Acceptance criteria

**Phase 0 (bugs)**
- [ ] F1: `FactionRoleHandlerBase` no longer throws when `SilencedTargets` is null (null guard at the `Targets.Except(SilencedTargets)` site, :116).
- [ ] F2: Mark's role prompt uses Mark's own QTE key and icon, not `LucyQTE`. If Mark has no QTE input binding yet, stop and report (a new input binding is a separate decision).
- [ ] F3: when a role's QTE can't start because another QTE is active (`PlayerController.cs:1556-1561`), the role is skipped **without** silencing its targets (the same enemy can trigger it on a later event). A real ignored/declined prompt still silences as today. No queue is added.
- [ ] F4 (PULLED OUT, D-065: moves to the Family Role chunk together with a footprint-aware `AEffectDashAttack`): Mark measures the attacker's range from its whole footprint (multi-tile enemies), like Linda and Lucy, not from the anchor cell.
- [ ] F5: Lucy considers every hostile faction, not only the first; within that she keeps today's choice rule (first match in list order). No "nearest" rule (not approved).

**Phase 1 (UI, no change to firing rules)**
- [ ] A: the selected unit's role zone is drawn on the grid (not hover-only): John and Mark as a diamond with the four diagonal neighbours inside, Linda as lines along her row and column to her radius, Lucy as a ring of radius 3. Each role handler has a serialized bool `showRoleZone`, true by default; off hides it for that unit.
- [ ] B: in the move preview, the hovered destination tile shows a shield icon if it lies inside John's zone and a fist icon if inside Mark's; when the unit being moved is John or Mark, their zone follows the preview. Same `showRoleZone` bool turns it off per unit. Separate overlay layer so Q20/S9 can change the preview later.
- [ ] C (D-064): holding Shift also draws every living Bergson's zone as an outline in the character's colour on the new zone layer; hovering one Bergson with Shift held shows only that zone. Shift's existing behaviour (info panels) is unchanged; if the hover move/attack preview (`ShowStatsHoverPreview.cs` L28, inverted `WaitUntil`) is confirmed dead, fix it as a Tier 2 bug in the same chunk.
- [ ] R1+ (D-064): Mark's Continuous Attack passive (`Unit_Mark.prefab` ~l.2914) uses `MarkQTE` too.
- [ ] D: the unit panel shows a role badge: ready, or no FTP (stun waits for the stun rule).
- [ ] F: a short tether line from John to the ally he is covering while his paused prompt is up.
- [ ] E: prompt and execute barks play for John, Linda, Lucy, Mark through the existing `FactionRoleVisual.ShowWithDialogue` path, using the prefab fields; when the QTE ends without a press, a neutral decline bark plays ("Not now"-style, wording from `miso-narrative`, `reports/b4-role-barks.md`); a serialized bool (true by default) turns decline barks off entirely. No "too slow" or failure wording anywhere. Rate limit: at most one decline bark per role per turn.
- [ ] No change to when a role fires, to FTP, to AP, or to AI choices; `AIRegressionTest` does not move beyond its known red.

## Scope

In: F1 to F5, A, B, C (Shift view, D-064), D, F, E.
Out: G (miss logging; THJ: only real misses are logged and none exist); the reason-code event, queue, Mark-also-hit rule, teleports for Linda, miss-silence scope, stun rule, Watch wording, Fireside pip (all in the Family Role chunk); per-round limits (Pilot 1); the mini-HP-bar pip (Q6).

## Touches

Systems: `FactionRoleHandlerBase` and the four handlers (core: null guard, F4/F5 fixes, two additive serialized bools), `PlayerController` (core: F3), `UnitPanelUI`, `FactionRoleVisual`, grid overlay, move-preview overlay, `GUnit` text fields (additive field for decline lines if needed), Mark's prefab data.
USPs: Family Roles.
Docs: `tech/combat-architecture.md` (overlay and bool names), `design/gdd/family-systems.md` (FR rules for zones and decline wording, via the designer), `glossary.md` (narrative, if new terms), `build-log.md`.

## Approach (chunks; one implementer run and one commit each)

1. **R1 · F2 Mark's QTE key** (sonnet, data). Check which QTE binding/input action Mark has or can reuse; if none exists, stop and report.
2. **R2 · Phase 0 bugs F1, F3, F4, F5** (opus, core). Put decision logic in small pure helpers so EditMode tests can cover them (null-safe Except, footprint-distance selection, faction iteration, "skip without silencing"). Reviewer: yes.
3. **R3 · A, B and C zones, cover icons and the Shift view** (opus). First read the Explore facts on the cell highlight system (`reports/b4-lshift-roleicon-facts.md`) so the overlay does not clash with attack/move range highlights. `showRoleZone` bool lives on `FactionRoleHandlerBase`, so every unit's role handler has it (additive serialized field on a core class: approved by THJ in D-063).
4. **R4 · D role badge** (sonnet). Read-only getters for ready/FTP; no handler logic changes.
5. **R5 · F John's tether line** (sonnet). Drawn during the prompt only.
6. **R6 · E barks** (sonnet). Waits for `reports/b4-role-barks.md`. Decline bark toggle bool and a rate limit; detect "QTE ended with no press" from the public events (assumption from the design, to be checked and reported; if unreliable, stop and report).

## Risks

- Phase 0 touches core role code: reviewer on R2 and on any core file in R3.
- New serialized bools on a core base class: missing fields on existing prefabs take the initializer value (true), so no prefab edits are needed; confirm in R3.
- Overlay clutter and highlight-layer clash: check against attack/move highlights (R3).
- Press-less QTE detection (R6) is an assumption.
- Statics/caches: none expected; if any, `PlayModeStaticReset`.
- AI: untouched.
- Other branches: `thj/home-test` needs these on its next merge of `main`.

## Gates

Compile / EditMode tests (all green except the known red) / reviewer on R2 and R3 / play check: yes (acceptance list in the design plan: John fires/can't, Linda fires/diagonal, Mark with Mark's key, big enemy, busy QTE, no spam on a 6-enemy turn) / docs above.

## Commit log

(Hashes recorded here as chunks are committed; no Co-Authored-By.)

| Chunk | Hash | Message |
| --- | --- | --- |
| R1 | `90b3019ea` | fix: Mark's Family Role and Continuous Attack use the MarkQTE binding |
| R2 | `5b401cc80` | fix: Family Role null guard, no muting when a QTE can't start, Lucy searches all hostile factions (F1, F3, F5; F4 pulled, D-065) |
| R3a (a) | `e5c649cb6` | feat(grid): per-owner role-zone layer on GridCell (B4 R3a) |
| R3a (b) | `e7850f406` | feat(roles): showRoleZone toggle and role-zone colour on Family Role handlers (B4 R3a, D-063) |
| R3a (c) | `f620c96de` | feat(ui): draw the selected unit's role zone and every family zone while Shift is held (B4 R3a, D-064) |
| R3a data | `07af236cc` | data: role zone colours on John and Lucy, Lucy's role no longer answers the Mark-Lucy Duo or Mark's Command (D-066) |
| R3b (1) | `e8783d0f3` | feat(roles): John and Mark role zone from a given cell, for the move preview (B4 R3b) |
| R3b (2) | `b6da8869a` | feat(grid): cover-icon overlay layer on GridCell (B4 R3b) |
| R3b (3) | `0d00cf36c` | feat(ui): shield and fist cover icons and the following role zone in the move preview (B4 R3b, D-063, D-067 strict fist) |
| R4 | `8bf2d5314` | feat(ui): role badge (ready / no FTP) next to the Family Role icon on the unit panel (B4 R4) |
