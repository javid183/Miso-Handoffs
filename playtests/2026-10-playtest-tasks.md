# Playtest Feedback — Oct 2026 · Task List

**Status:** reviewed with THJ (2026-10-17/18); filed in the repo 2026-10-18
**Path:** `claude-handoff/playtests/2026-10-playtest-tasks.md`
**Sources:** U = unnamed list · Y = Yashar · S = Shakib · P = Parsa · A = Anders · Al = Alireza · J = July form · T = THJ notes
**Effort:** S ≤ ½ day · M = 1–3 days · L > 3 days
**Owners:** PM · GD (game designer) · TD (technical director) · QA · NR (narrative)

All playtest builds were from the main branch, so hub feedback is about the old Home, not the redesign.

---

## Decided

- **Fixed AP + FTP is final.** Shared AP and ATB are dropped (S2 closed).
- **Family Roles use FTP today** (`main` runs FTP); D-036/D-042 make them free with a per-round limit once built (confirmed by THJ 2026-10-18, D-051).
- **Attack cooldowns are already cut.**
- **The Linda–Toba duo is the showcase duo** (D-008; the earlier "Mark–Linda replaces Toba–Mark" line was a mistake, corrected by THJ 2026-10-18).

---

## Batch 1 — Blockers (before any external build)

- **B1 · Mark's Cleanse freezes combat.** Reproduce in *In My Father's Arms*. Done when Cleanse resolves every time and the corrupted tile clears. *TD+QA · M · A, U, S*
- **B2 · Verify the Big Ogre ground-slam fix.** Believed fixed. QA confirms it in *In My Father's Arms* and *Into the Rootwell*, then closes it. *QA · S · A, U*
- **B3 · HP shows 0/X on a living enemy.** Likely caused by the recent float change (rounding up → down). Round up for display, or keep HP whole. Check that previews match (e.g. "Mark preview shows 1"). *TD · S · Al, U*
- **B4 · Family Role readability under FTP.** Most of the reported issues were ATB-specific; under FTP the problem is subtler but still real. Make it obvious why Linda's QTE did or didn't fire, and when John defends. QA logs any remaining FTP bugs. *TD+QA · S–M · S, J*
- **B5 · Workshop first-time unlock doesn't work.** *TD · S · U*
- **B6 · Map mission panel pushed off-screen right.** *TD · S · S*
- **B7 · Text errors.** "Exit the refuge" descriptions (Daryani's Shop, Anahita's Ashiyan); "far ther" typo. *NR · S · S*
- **B8 · Input isn't locked while a tutorial panel is showing.** *TD · S · U*
- **B9 · Pushback logic** (was Q16). Pushback pushes even when there's no valid tile, sending units in wrong directions. If the tile in the push direction is blocked or missing, the unit stays put. The preview is already correct; the bug is in pushback itself. First seen with John's Shield Dash. *TD · M · Y, U, J*
- **B10 · Smoke-test gate.** QA plays every level to completion before each external build and logs the run in the build log. *QA · recurring · soft locks in both July and Oct*

## Batch 2 — Priority

- **S1 · Level restructure** (moved up; must-have). The direction is clear and the existing levels are enough material. Plan it on paper first: map existing levels onto the slots below, and decide what to merge, trim and cut. Then build.
  - Remove the Sister's Rivalry tutorial level and the healer level.
  - Keep levels short, merge the tutorials, and use focused challenges with one twist per level.
  - Deliver a combo payoff early (Parsa).
  - *GD+PM · L · P, S, Al, U, Y, T*

  | Slot | Plan |
  |---|---|
  | 1.1 | Current level, as is |
  | 1.2 | Linda-focused |
  | 1.3 | John-focused |
  | 2.1 | Current 2.1, but with Linda |
  | 2.2 | Lucy + John's Family Role + resource regen |
  | 3.1 | Current 3.1, but with Linda |
  | 3.2 | Current 3.2, as is |
  | 3.3 | Duo-focused |

- **S8 · Narrative supports gameplay firsts.** Part of the S1 paper plan.
  - In-level dialogue should frame what the family can do together, not only advance the plot.
  - Give each first use of a duo, synergy or Family Role a story beat. Example: the third node of the Mark intro mission, when Mark joins Lucy.
  - **Sister's Rivalry mini-arc** (the template):
    - *Setup:* the sisters compete over a level or two, with bickering barks about who's the better shot.
    - *Build-up:* a short practice beat at Home in the Training Ground, either automatic or player-placed. The Yard Lessons teacher/student seats may already support this.
    - *Resolution:* the first in-level trigger, with the Q18 insert-shot.
    - Land the payoff around chapter 2 so it isn't too late.
  - This replaces the cut Sister's Rivalry tutorial level. Other duos and synergies can follow the same pattern.
  - *NR+GD · M · U, J (Shakib, Amir, Shayan A), T*

## Batch 3 — Quick wins

- **Q1 · Directed dialogue pass.** Mission openings stay, but every line has to earn its place. Cut scenery-narration and objective-explaining lines, and move what's useful into barks and in-level triggers. Trimmed chatter frees room for S8 beats. *NR · M · nearly all*
- **Q2 · Story logic fixes.**
  - Lucy keeps the Ryker thread, and Ryker and John share the concern.
  - Make Ryker's pronoun consistent.
  - Set up the masked man.
  - Fix the "killing this thief" line.
  - Explain why the family goes home after Blood Wolf.
  - Fix the Mission 5 grandma line.
  - Name "this part of the forest".
  - *NR · M · S, U, Y, J*
- **Q3 · Faster transitions.** Level end and combat ↔ non-combat. *TD · S · Y, U, T*
- **Q4 · Faster enemy turns.** Speed up enemy animations and/or add a fast-forward toggle. *TD · S–M · Al, Y*
- **Q5 · Targeted juice top-up.** A pass already improved this; much of the feedback dates from July. Parsa (Oct build) still named hits and kills as the main weak spot, so focus there: hit-stop, kill flash, punchier impact SFX. *TD+GD · S–M · P, S, A*
- **Q6 · Always-visible mini HP bars.** Add a lethal-hit preview and a low-HP warning. *TD · M · Al, U, Y, J*
- **Q7 · Family Role "why not" feedback.** Show a reason popup when a role can't fire, and show diagonal adjacency on the indicator. *GD+TD · S · S, Al*
- **Q9 · Selection feedback.** Right-click to deselect; fix enemy targeting when an ally is close. Default-action flow is covered in S9. *TD · S · U, Y*
- **Q10 · Lucy clarity.** "Target 1/3" counter on multishot, a visible orb count, and a retarget hint. *TD · S · S, Y, T*
- **Q11 · Map clarity + mission reveal sequence.**
  - New missions are revealed one at a time: camera pans to each point, highlights it, and a short family exchange plays per mission. Two unlocks become two beats, not one mixed reveal.
  - Explain the mission numbers or remove them.
  - *TD+NR · M · S, Y, A, T*
- **Q12 · John holds his shield-idle pose while shielded.** *Art+TD · S · T, A, J*
- **Q13 · Goal tile and Divine Relic visuals.** The goal tile should read as "come here"; the relic shouldn't look like friendly fire. *TD · S · U*
- **Q14 · Cleanup.** Hide the grid after the level 2 tutorial; remove extra Workshop items. ATB-only items are moot now that FTP is final. *TD · S · U*
- **Q15 · Mark's hit sound uses Lucy's voice.** *TD · S · S*
- **Q17 · Enemy idle desync.** Random start frames are already in, but pure random can still cluster. Use evenly spread offsets plus a small speed variance. *TD · S · A*
- **Q18 · Synergy trigger insert-shot.**
  - A short avatar visual every time a synergy fires, reusing the Family Role insert-shot.
  - Build it as a generic system: Sister's Rivalry first, then others (e.g. Mark returning Linda's arrows).
  - It can grow into a bigger sequence later.
  - *TD · S · Y, A, J*
- **Q19 · Turn on undo-move.** The code already exists.
  - Undo must roll back anything the move triggered, e.g. tag passes and their FTP gain.
  - Block undo once a move triggers a Family Role QTE or an enemy reaction.
  - *TD · S · S9*
- **Q20 · Test character-coloured move previews.** Tint move tiles in each character's signature colour. To avoid a rainbow, use outline-only, the path ghost, or muted tones. *TD · S · S9*
- **Q21 · Cyclone deals damage at the start of its turn** (priority fix). *TD · S · Y*

## Batch 4 — Design items (need sign-off)

- **S3 · Combat tweaks.**
  - John's basic attack hits the target tile plus adjacent tiles, as an area hit, not extra actions.
  - **Pushback collision damage:** only when shoved into a wall or a unit. *Undecided.*
  - *GD · M · U, A*
- **S4 · Home and skill trees.** Lower urgency: playtests used the old Home, and the redesign covers most of the hub feedback.
  - Check the redesign against that feedback: no pure numbers game, and Home effects visible in combat.
  - Revamp the Family Skill Tree into fewer, felt additions.
  - Skill tree UI cleanup: nodes shouldn't look locked when they aren't, and the cost should show 0 after an upgrade.
  - *GD+TD · M–L · A, S, U, J, T*
- **S5 · Sister's Rivalry.** Keep it, cap it. Feedback is handled by Q18, the story by S8. *GD · S · U, Y, J*
- **S6 · Objective variety and environment tiles.** Non-elimination objectives; hazard tiles with a risk-and-reward choice. *GD · M · Al, U, J*
- **S7 · Showcase duo** (void as written: the showcase is Linda–Toba, D-008). Nothing to do unless THJ reopens it. *GD · M · T*
- **S9 · Selection and default-action flow.**
  - Selecting a unit auto-arms Move, and one click moves. Players don't understand the preview when switching quickly: the camera doesn't move and the first slot is always highlighted, so the HUD cue doesn't register.
  - Try Q19 (undo-move) and Q20 (coloured previews) first.
  - Fallback: first click on a tile or enemy previews the action (path, AP, damage), second click confirms; double-click acts instantly.
  - *GD+TD · M · S, Y, U, T*
- **S10 · Cyclone movement + pull.** Improve its movement and prototype a pull towards the centre. Test first. *GD+TD · M · U*

## Backlog

- **L1 · Level identity.** Landmarks and palette per level; cover the empty tiles in e1-c1.
- **L4 · More animation.** Per-skill animations, and frame art used earlier.
- **L5 · Free movement outside combat.**
- **L6 · Home stakes.** Wounds, recovery and risk at Home.
- **L7 · Music variety.**
- **L8 · Single timed QTE press instead of button-mash** (was Q8). Only Anders asked for it.
- **L9 · John zone-of-control / Linda pinning** (was in S3). A big design decision, for later.

Dropped: S2 (decided), L2, L3.

## Status (coordinator, 2026-10-18)

- **B1** fix built and committed; Cleanse seen resolving with no freeze (tile clearing not seen, no corruption on that board yet).
- **B3** display fix committed; seen at whole-number HP only.
- **B5** diagnostic committed; waiting on THJ's repro.
- **B6** world map fix committed and seen at 16:9, 16:10, 4:3; mission map not seen.
- **B8** fix committed and seen in play (lock and restore); turn-change and mid-turn cases covered by unit tests only.
- **B9** held for S3 (D-053). **Q21** bundled with S10 (D-055).
- Not started: B2, B4, B7, B10 and Batches 3 and 4.
