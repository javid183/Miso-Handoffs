# Family Role chunk (batched work, not started)

Size: L    Tier: 3 (core Family Roles, controller, bus, effects)    Assigned to: game designer, then tech plan (coordinator), then implementer
Branch: `main` / `thj/fr-readability` (decide when it starts; Pilot 1 was parked for `main`, D-042)
Status: collecting. THJ's wish (D-062): do all Family Role work in one chunk instead of piecemeal.

This file is the single index. Detail stays in the linked docs; nothing here repeats a rule.

## What is already built (do not redo)

Phase 0 (F1, F3, F5), Phase 1 (zones, Shift view, shift layer, cover icons, badge, tether, barks), the `onFamilyRolePrompt` and `onFamilyRoleOutcome` bus events. Hashes: `plans/2026-10-18-family-role-phase0-1.md` (commit log). Decisions D-062 to D-072.

## Items in the chunk

| # | Item | Source | What it needs | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Pilot 1: per-round limits** (Linda 2, Mark 1, Lucy 3, John unlimited), roles free of FTP | D-036, D-039, D-041, D-042, D-061, `plans/` Pilot 1 | A new per-round counter (the cooldown does NOT give a charge: D-061), reset at the start of the player turn (D-039), `oncePerPhase` resets on any faction's turn end today | Pilot 1's tech plan is not written yet. Touches `FactionRoleHandlerBase`, `FactionControllerBase` (core) |
| 2 | **Fireside payoff** (+1 role use in the sortie's first round, John's first redirect takes no damage) | D-040 | Home effect read at sortie start; merge question open (`branches.md`) | Waits for the merge of `thj/home-test` |
| 3 | **F4: Mark measures big enemies by footprint** | D-065, `reports/b4-f4-mark-footprint.patch.md` | A footprint-aware approach cell and adjacency in `AEffectDashAttack` (shared core effect, also Mark's own Fist Blitz) first, then reapply the patch | Without the dash fix Mark punches from a distance |
| 4 | **Reason-code event** (why a role didn't fire) with the five player-facing reasons and the silent set | Design plan "Reason-code catalogue" | Handlers report a reason; additive bus event `onFamilyRoleSkipped`; non-core presenter applies tell/silent filter and rate limits | Q7 popup. Postponed (D-062) |
| 5 | **Role queue** (several eligible roles fire one after another instead of dropping the rest) | Design plan Q2, D-062 | Controller wait-list change; cap undecided (designer proposes 2) | Pacing cost about 1.5 to 2 s per extra role |
| 6 | **Mark answers when the same hit also targets him** | Design plan Q3, D-062 | Remove the base guard for Mark (his 1-per-round limit caps it) | Agreed in principle |
| 7 | **Teleports and jumps into Linda's lane trigger her** | Design plan Q4, D-062 | `AEffectTransporter` raises the end-move event for teleports and jumps | Do after the limits exist (Linda capped at 2) |
| 8 | **Miss-silence rule** (a declined prompt mutes that enemy for the turn) | Design plan Q5 | Scope it to the current turn for real (today it clears on a selection change); tell the player in the tooltip | A declined prompt is a decision, not a miss (D-063) |
| 9 | **Stun rule** (can a stunned or downed Bergson answer?) | Design plan Q8 | Handler guard; stun star on the badge (`CantReact`) | Undecided |
| 10 | **"Watch" wording and pips** ("No FTP" becomes "No Watch left"; Fireside extra pip) | Design plan Phase 3 | Rides on item 1 | Needs narrative for the term |
| 11 | **Role presenter shared with Q18** (synergy insert-shot) | Design plan Overlaps, `playtests/2026-10-playtest-tasks.md` Q18 | One "family moment" presenter with priorities: role execute > synergy insert > reason bark | Build once |
| 12 | **Mark's hit sound uses Lucy's voice** (Q15) and other role polish from the task list | `playtests/2026-10-playtest-tasks.md` | Data/audio | Check if it belongs here |

## Small follow-ups (can be done before the chunk)

| Item | Source | Size |
| --- | --- | --- |
| Enemy movement cells in a slightly different tint on the Shift layer (best with Q20, coloured move previews) | D-072 | S |
| Clear the Shift preview when ability targeting starts | Shift-layer review | S |
| Queued-target hover (`SetPotentiallyTargeted`) shares a plain flag with other features: rare holes, one rare stuck 2x2 case | Shift-layer review | S to M |
| Mark's role zone colour is very dark (judge in play) | THJ edit 2026-10-19 | S |
| Execute line stacks on the fading prompt line: add a short delay if it reads badly | R6 report | S |
| `abilityActivationFrame` at or past the clip end freezes an ability | Batch 1 review | S |
| A second `ShowTutorial` while one is open leaves `timeScale` at 0 | Batch 1 review | S |
| Fist rule: ranged attackers are not covered; explain in the tooltip text/GDD | D-067 | S |
| "Unexpected guid mismatch" assert after refresh: re-check after a Unity restart | R5/R6 reports | S |

## Docs to update when this chunk lands

`design/gdd/family-systems.md` (FR rules, Lucy's blacklist D-066, zones and Shift view, barks), `combat-rules.md` CR-28, the four character pages, `glossary.md` (Watch, Family watch), `tech/combat-architecture.md` (role zone/cover/tether/bark presenters and bus events), `tech/core-systems.md` only if a new class becomes something combat relies on.
