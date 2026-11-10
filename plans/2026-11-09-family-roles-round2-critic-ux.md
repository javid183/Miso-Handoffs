# Family Roles round 2: UX critic notes

Critic: `miso-design-critic`, UX lens. On: [`2026-11-09-family-roles-round2-design.md`](2026-11-09-family-roles-round2-design.md) (draft, recommendation P). Read: the draft, round 1, `m9-readability.md`, `family-systems.md` FR-2 and FR-8 to FR-13, `combat-rules.md` CR-27 to CR-29 and CR-37 to CR-54, `combat-architecture.md`, `playtests/2026-11-09-pacing-check.md`, `status.md` (B4 findings). Code checked: `RoleBadgeState.cs`, `UnitPanelUI.RoleBadge.cs`, `JohnWrathBadgeUI.cs`, `JohnPassiveAbility_Wrath.cs` (popups), `MarkPassiveAbility_AtmanFocus.cs` and `UnitPanelUI.cs` (Focus label), `QTE_ModeView.cs`.

## Strongest objection: the arm can't be seen at the two moments that teach it

P only fixes "you never know what you did" if the player can see, **before End Turn**, which roles are armed, and **on the enemy turn**, why a role did or didn't fire. Neither is designed.

- **Before End Turn the arm state is spread over four encodings, three of them only on the unit panel of the unit you're looking at.** John's Wrath is a grey box reading "2/3" (`JohnWrathBadgeUI`). Mark's Focus is a number in the sibling box (`markFocusValueLbl`). The draft's UX table says "Focus pips (existing)": there are none. Linda's quiver sits on her portrait. To check the family before ending the turn you have to click through all four Bergsons. The role badge is a 14 px dot with three states: Ready, NoFtp, EmptyQuiver (`RoleBadgeRules`). Once roles cost no FTP, NoFtp never happens, so the dot is green for John with his shield down and for Mark at Focus 0. That is the opposite of what P needs it to say.
- **The board signal P relies on is already the worst-read thing on the board.** B4's first untriaged finding (status.md, 2026-10-21) calls the role-zone and cover glyphs "too low contrast (biggest readability problem)", and the tether is near-invisible on dark floors. John's zone is dark brown and Mark's near-black, both at 0.75 alpha (FR-8). Under J1 and L1, John's zone and Linda's lane become the main sign that a role is armed. A glyph you can't see means a choice you can't read.
- **When an unarmed role would have fired, nothing happens.** A Claw ends in Linda's west line while she faces north. Mark has Focus 0 when Lucy is hit. John's shield has broken when the fourth Claw hits Linda. Each of these is silence, and silence teaches nothing. The player can't learn the arm rule from a prompt that doesn't appear, so THJ's complaint turns into "you never know what you *didn't* do." P also ends the pacing check's "the prompt teaches itself" (2026-11-09 answers): the press still needs no teaching, but the arm conditions do.

**What to change (three pieces, all on existing layers):**
1. **Hovering End Turn previews the enemy turn.** It draws every armed role's zone (John's if his shield is up, Linda's lane, Mark's radius if Focus is 1 or more) and greys the portraits of the unarmed ones. Keep the same drawing up through the whole enemy turn: the draft does this for Linda and John, so add Mark. Bonus: this is also the "what will happen" view M9 asked for at Home ("nothing on screen shows the future").
2. **Rewire the badge to "armed", with a reason per hero:** Ready, "Shield down", "Shield broken: strike first", "Last arrow", "No Focus". Show the four badges next to the End Turn button as well as on the panel, so the family's readiness reads at a glance without selecting anyone. One state source, `GetRoleBadgeState`, already marks the switch point ("Switch here when roles stop costing FTP").
3. **A "would have fired" ghost.** When a role's trigger happens but its arm is off, show its glyph greyed and crossed for about 0.6 s over the unit that would have acted, with a two-word reason ("Not facing", "Shield down", "No Focus", "Last arrow"). Each handler already evaluates its trigger before its gate, so this is a few lines per handler, plus the reason strings for `miso-narrative`. This is how the rule gets taught without a tutorial.

Do the contrast fix (B4 item 1) **before** P's code, not after. It is now a blocker for P, not polish.

## Other points

**1. John: Wrath is both a reward and a fuse, and the guard choice is made blind.**
- *Likeliest misread:* "Max Wrath" means "great, keep guarding." Today the third stack pops "Max Wrath" in the gain colour (`GainStack`). Under J2 the same moment is the shield breaking. A second misread follows: "the shield broke by itself." John's **own** hits count too (in S2 the first Claw hits him for Wrath 1), so his guard budget is "3 minus the hits he took", and he can break before any prompt has appeared.
- *Blind choice:* the S2 ★ ("decline the second Lucy guard to save the shield for Linda") needs to know who acts next and at whom. During the paused prompt the player sees one tether and nothing else, so the ★ is a guess.
- *What to change:*
  - Show the shield as 3 segments on John in the world (on his shield icon over the mini HP bar, or on the tether cap). Each hit, his own included, cracks one segment visibly.
  - On John's prompt, add a cost line: "Guard Lucy · shield 1 left", and "breaks the shield" on the last guard.
  - While the prompt is paused, draw the existing threat arcs (CR-39) from the enemies that haven't acted yet to their likely targets.
  - Replace "Max Wrath" with a single beat: "Shield broken · Wrath ready".
  - Hovering Shield Up shows the guard zone (from the ghost tile when moving) before the player commits.

**2. Linda's facing picker clashes with the board, and the default can't be predicted.**
- Four arrows "at her feet" sit on her tile, ringed by the tiles she moves to and shoots at. That gives misclicks into moves, plus hover fighting the ghost preview.
- The default has three fallbacks (last shot, else last move, else last turn), so no one can recite it.
- Crescendo on a diagonal cell (2,1 → 4,3) has no clear direction.
- A shot that **kills** leaves her watching where the dead enemy was. *Likeliest misread:* "she's still watching that way" after the kill. Players who knew the old rule will also assume she still watches all four lines.
- *What to change:*
  - One rule in one line: *"Linda faces the way she last shot, or the way you turn her."* Moves don't change it, because paths bend and walking away from a threat would turn her away from it. Diagonal targets take the longer axis; a tie keeps the old facing.
  - Put the picker on her HUD as a free ability-bar control that shows her current arrow. Clicking it cycles the direction and hover previews the lane. A direction key works as well (check it against the camera pan keys).
  - Draw her lane on the family's turn whether or not she's selected, as a thin line that snaps visibly after each shot.
  - If her lane holds no awake enemy that could end a move in it, End Turn pulses her badge. Warn only, never turn her automatically. This costs nothing on most turns and catches the dead-lane case.

**3. The last-arrow rule (L2) is an off-by-one rule.**
- The quiver shows one arrow and Watch is off.
- Hiding the lane at 1 looks like "Linda isn't selected", not "Linda is out".
- *Likeliest misread:* "she has an arrow, why didn't she shoot?"
- *What to change:*
  - At 1 arrow, draw the lane dimmed with the crossed-arrow glyph instead of hiding it.
  - Show the last arrow in the quiver strip as a different, reserved arrow (another tint or a small lock), so the count reads "spares + 1 kept".
  - Badge line: "Keeps her last arrow."
  - If the reserved arrow can't be made to read, drop L2 (the draft's own first lever). It is the one rule in P that the house-rule session can't test, because THJ already knows it.

**4. Mark (M2) asks for a real decision inside a 1 s real-time window.**
- FR-2 pauses only John's prompt. Under M2, pressing costs Focus, and Focus is his barrier (3, 5, 7…). Spending 1 → 0 drops the barrier from 3 to 0. So the player is deciding about his HP in one second, with Focus shown only on the unit panel (not on screen during the enemy turn unless Mark happens to be displayed).
- Hits on Mark also cost 2 Focus each, so Focus 1 at End Turn can be 0 by the time the counter triggers.
- *Likeliest misreads:* "pressing is free", and "he had Focus, why no counter?"
- *What to change:*
  - Pause on Mark's prompt as on John's, with a cost line: "Counter · Focus 2 → 1, barrier 5 → 3".
  - Add a world-space Focus pip row under Mark, the same pattern as Linda's pips under her.
  - Draw his zone through the enemy turn only while Focus is 1 or more.
  - If THJ doesn't want a second pausing prompt, make M2's spend automatic: an arm with no press choice. That is one decision fewer, and the arm still reads.

**5. Lucy's preview, as drawn, breaks down in exactly the preview THJ called random.**
- Her FR-8 quadrant glyph on the enemy's tile is her **zone** glyph. On a tile that already carries the CR-37 sword icon and maybe Linda's lane glyph, it reads as "Lucy's zone", not "Lucy will hit this".
- Her segment goes on "the target's info panel". On a pierce or a Shield Dash her pick is often not the hovered target, and that enemy's panel isn't open, so her damage shows nowhere. That is the very case behind "randomly coming about".
- On a multi-target ability, CR-45 already uses two tints (picked, this click). Hers would be a third on the same bar, plus a third skull variant. Her pick can also flicker from pick to pick.
- *What to change:*
  - An arc from Lucy to her pick (ArcLine, the tether's look in her red).
  - A ghost "+6" in her colour above the pick's **mini HP bar** (CR-49, always visible), not inside the panel.
  - Show it on single-target hover and on the firing pick only.
  - Her part of a kill shown as a hatched "if pressed" segment, with no tinted skull: the skull keeps meaning "this hit kills".
  - Where an enemy in her reach is skipped by the "hit last" rule, show a small crossed ember on it, so the hidden rule shows up the first time it matters.
  - Build U1 first, as the draft says; it is the most-wanted fix in the plan.

**6. The complexity count is low.**
- The draft says about +4.5 to learn and one new element. Read as a player, P adds about **8 rules**:
  - John: guards only with the shield up; three hits break it; his own hits count.
  - Linda: one lane; the default; the last arrow.
  - Mark: a counter spends Focus; a counter no longer earns Focus (hits on him costing 2 Focus is old, but now it matters for the arm).
- New or re-meant on-screen items:
  - the picker
  - zones that stay up through the enemy turn
  - three new badge states
  - the "Shield broken" beat
  - Shield Up greyed out
  - Lucy's preview marks
- Removed: the FTP cost, FR-10 for Linda.
- That is against THJ's "too many mechanics" (pacing check). *What to change:*
  - Cut the rules that don't buy a choice. Drop "the counter earns no Focus" (M2 reads the same if counters still earn). Simplify Linda's default as in point 2. Keep L2 only if the reserved arrow reads (point 3).
  - Put the teaching budget into the "would have fired" ghost (strongest objection, piece 3), not tutorials.
  - Each hero's badge tooltip is the one line: *"Guards while his shield is up; three hits break it."* · *"Watches the way she faces; keeps her last arrow."* · *"Counters with Focus."* · *"Follows up the family's hits; shown before you attack."*

## Per option

- **A + Lucy preview:** ship the preview with point 5's changes, on every branch. It fixes Lucy's readability and nobody else's.
- **C (kept AP):** don't ship. Ending a turn with AP left reads as a mistake, as round 1's UX pass already said.
- **P:** ship with changes. Ship it only with the strongest objection's three pieces and the contrast fix. Without them the arms are as invisible as today's triggers, and the session can't show that because THJ knows the rules.
- **P+ (J3 swap, stamina, minimum range, ember pool):** don't ship now. The swap reshuffles the board mid enemy turn, and P+ adds three or more HUD counters. It is the most to read with the least time to read it.

## What would change my mind

- A cold player (not THJ) plays the Ridge and the River after code steps 1 and 2. If they can say, before End Turn, which roles are armed, and after the enemy turn why one didn't fire, without the End Turn preview, the badge row or the ghost, then those three are gold-plating.
- If THJ's house-rule session shows that John's shield break and Mark's spend never change a press, the per-press cost lines (points 1, 4) aren't needed, though the arm display still is.
