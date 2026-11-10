# Family Roles round 3: UX critic notes

Critic: `miso-design-critic`, UX lens. On: the "Round 3" section of [`2026-11-09-family-roles-round2-design.md`](2026-11-09-family-roles-round2-design.md) (draft R3). My round-2 notes: [`2026-11-09-family-roles-round2-critic-ux.md`](2026-11-09-family-roles-round2-critic-ux.md). Also weighed: THJ's two messages of 2026-11-10 00:51–00:52 (John: posture or stamina instead of Wrath, damage-based; Lucy: reach plus beside is a double gate). Read: `vision.md`, `family-systems.md` FR-2 and FR-8 to FR-13, `combat-rules.md` CR-18, CR-37 to CR-54, `reports/b4-family-role-facts.md`, `status.md` (B4 findings). Code checked: `QTEButton.cs`, `QTE_ModeView.cs`, `QTEPromptTiming.cs`, `FactionRoleHandlerBase.cs` (`requiredTimeScale`), `JohnWrathBadgeUI.cs`. S8 tiles re-read from the `rr3-s8-chain` grid.

**Two code facts that change the readings below:**
- **A "paused" prompt still gives one second.** The QTE countdown runs on `Time.unscaledTime` (`QTEButton.cs` ~380–392), after a `WaitForSecondsRealtime` preload (0.6 s default). `requiredTimeScale` 0 freezes the world, not the window. John's prompt is paused today, but he still has 1 s to read it. The round-3 house-rule session sets Linda and Lucy to `requiredTimeScale` 0 "so the rules can be judged". That gives THJ no extra time.
- **The prompt shows a key and up to a few portraits, nothing else.** It sits at a fixed screen spot (`inputPromptPosition`), and the portraits come from the profile's `relatedImages`. Whether each role profile sets its own hero's portrait is to check. No reason, no target and no cost are shown.

## Strongest objection: S8's chain can't be predicted before End Turn, and on the enemy turn it reads as three unexplained presses

S8 is round 3's showcase: one hit, three roles. Before End Turn, the player would have to know four things. Who the Claw attacks (Lucy). **Which tile it attacks from** (3,2). Which way Mark's knockback goes. Whether the landing tile is free and in Linda's lines. Nothing on screen shows the second, and the design text gives two answers for the third.

- **Where the Claw stands decides the chain, and the enemy chooses it.** Lucy on 2,2 can be hit from 3,2, 2,3 or 2,1 (Linda holds 1,2).
  - From **3,2** (S8): the knockback away from Lucy goes east to 4,2, in Linda's row. Chain.
  - From **2,3**: it goes north to 2,4. Mark is 4 away (3,0 to 2,3), so there's no counter anyway.
  - From **2,1**: Mark counters (2 away), but 2,0 is a missing tile, so the Claw isn't moved, and nothing shows why the punch didn't send it.
  - S8 works because the shortest path from 6,2 runs along Linda's row. That is the enemy's pathing, not the player's setup. CR-39's threat arcs show which enemies can hit a ghost tile. They don't show where an enemy will stand, and the End Turn hover (round 2's piece 2) draws zones, not chains.
- **The direction rule is still two rules** (the coordinator's flag). Under "away from Mark", Mark on 3,1 (south of the Claw) sends it north to 3,3, and S8 ends at beat 1. Under "away from the victim" it goes east and S8 works. The "real decision" row and S8's last line follow the first reading; the rule and S8's beats follow the second. A player can't learn a rule the design hasn't settled.
- **Then the enemy turn plays three 1-second prompts in the same screen spot, ~1.6 s each, with animations in between.** Mark's prompt fires on `OnActionComplete`, real time; Linda's on the push's `unitEndMoving`, real time; Lucy's on the arrow's `OnActionComplete`, real time. Each prompt shows a key and maybe a portrait. Nothing on screen says Linda fired *because Mark moved it* (the cause clause) or Lucy fired *because Linda was beside her*. The player presses three times by reflex, and the read-out's "did you know why it fired?" will fail on beat 2. It's the round-2 complaint again ("you never know what you did"), now in a chain.

**What to change:**
1. **Lock "directly away from the victim"** and fix S8's last line and the Setter's "real decision" row. It's the reading players can work out from the board: victim, then attacker, then landing, in one straight line. It turns the setup into one sentence they can learn: *"Stand in Linda's line; whatever hits you along it gets knocked down it."* Mark's own part is only "within 2". Under "away from Mark", the player has to combine Mark's tile with an attack tile they can't see.
2. **Don't sell the chain as predictable. Make the formation readable and the chain explained.** Before End Turn, the readable decision is the formation: a sibling in Linda's line with Mark within 2. On the enemy turn, the chain has to explain itself.
3. **Give every role prompt the tether while it's up** (FR-13, today John's only). An arc in the hero's colour from the role hero to the role's target, plus a one-to-two-word cause under the portrait: "Mark moved it", "Next to Lucy", "Linda beside her". The arc is re-meant (an existing element, a new use). The words are the ghost's reason strings in their positive form, one string table, written by `miso-narrative`.
4. **When a link fails, show the ghost** (round 2's piece 3). For Mark's knockback with no tile to land on, the ghost reads "Blocked". Today the Claw just stays put after the punch.
5. **Leave at least 0.3 s between chained prompts** (the next prompt's preload already gives most of it; check that the push and the arrow finish first). Show a small chain count ("×2", "×3") at the second and third links, so the player learns that chains are a thing. The count is new, so it's THJ's call (D-295). Leave it out first and add it if the cold player doesn't notice chaining.

## Other points

**1. John: the swap at any range is a decision squeezed into a reflex window. If THJ's posture meter replaces Wrath, it carries the answer.**
- *What the decision needs.* "Where will Lucy land, and is it safe?" means reading John's tile (possibly across the board, possibly off-screen), the enemies that haven't acted yet, and whether they can reach that tile. All of it in 1 s, because the pause doesn't stop the window (see the code facts above). Today's prompt shows the tether to the ally and nothing at John's end.
- *Likeliest misread:* "pressing saves her." The press reads as protection, but at S6's second prompt it puts Linda between two Claws.
- *What to change:*
  - **Make John's prompt a decision prompt.** No countdown while paused, two answers: Swap, or Let it land (another key, or the expiry key). It's the only prompt with a real "no" (S6), so it shouldn't be timed like a reflex. The other three stay 1 s reflexes (pillar 1). Data or small code: `duration` on John's QTE profile, or an untimed mode.
  - **While John's prompt is up:**
    - a ghost of the child on John's tile and a ghost John on the child's tile;
    - CR-39's threat arcs from the enemies yet to act **to John's tile**: the arcs exist and are computed for a ghost tile, so they're re-meant, not new;
    - **the camera frames both units** (to check whether the camera can; otherwise an edge pointer).
  - Round 2 deferred the threat arcs on the prompt "for budget". In round 3 they *are* John's decision, so they're necessary now.
- *THJ's posture or stamina meter, as UX:*
  - **Where it shows.** A thin bar under John's mini HP bar (CR-49), always visible, in a pale bone or gold tint. Not his dark-brown role colour: B4 finding 1 is low-contrast glyphs, and green is HP's. The panel's Wrath box ("2/3", `JohnWrathBadgeUI`) becomes Posture "6/10".
  - **How it previews a hit.** John's role fires on `OnActionStart`, so the hit's damage is known before he answers. The prompt adds one cost line, "Take it · posture 10 → 6", plus a hatched segment on the bar: the same "if pressed" hatching as Lucy's preview, one language for both.
    - If the guard would break it: "Breaks his guard", and the bar shows fully hatched with a crack.
    - Damage-based is what makes THJ's case readable: a Claw costs a sliver, a boss blow shows "breaks" before the press, so the player sees why a boss hit is different. Like every preview it leaves crit out (CR-21); accept the rare surprise.
    - If Shield Up's ×0.6 also lowers the posture cost, the cost line shows it, and that gives Shield Up a reason that reads.
  - **The break moment.** One beat, "Guard broken": John staggers, the bar greys. While broken, a swap that would have happened shows the ghost "Guard broken". Recovery needs one sentence, shown as the bar refilling (e.g. "recovers at the start of his turn"). "Broken" must read as "no swaps", not "hurt"; if it also means taking more damage, that's a second state to draw, so ask THJ.
  - **Which hits drain it.** Readability says guards only. If his own hits count too, it can break before any prompt, which was my round-2 misread ("broke by itself"). If THJ wants all hits for the endurance theme, the same chip has to show on his own hits.
  - **Adds or replaces?** It replaces Wrath only if Wrath's attack bonus goes, as THJ's message implies. Wrath is three rules (a stack per hit, cap 3, +35% on the next damaging ability); the meter is two (a guard costs posture equal to the hit; at 0 the guard breaks until recovery). That's −1 rule. On screen, the panel box is re-meant, "Max Wrath" becomes "Guard broken", and the world bar is +1. The bar is necessary: the prompt's cost must read on the enemy turn, and the panel isn't on screen then. Keeping Wrath as a reward *and* adding the meter is +2 rules and +1 element, so it goes to THJ as a question.
  - **Bonus.** The meter caps John's prompts per enemy turn (point 4) with no "once per turn" rule.

**2. Linda: two clauses fit in one line only if each clause gets its own display, at the moment it matters.**
- *The line (badge tooltip):* **"Shoots an enemy in her lines that the family pushed there, or that stops next to family."** Or shorter: "In her lines: pushed by family, or next to family."
- *Likeliest misread:* "she shoots anything in her lines" (the built rule, and drawing the whole line suggests it). Then: "the Claw stopped in her line, right next to her, why no shot?"
- *What to change: two displays, one per clause:*
  - **"Next to family" (the protection clause)** is static and can be drawn ahead. On End Turn hover and through the enemy turn, show her lines dim and the tiles in them **next to a sibling** bright. Those are the tiles that fire on their own.
  - **"Pushed by family" (the cause clause)** is shown while it's being set up. In any push or Command preview (Vault, Shield Dash, Command), a landing tile in her lines gets her bow icon at full opacity. That's the FR-12 cover-marker pattern, re-meant: "this push makes Linda fire". On the enemy turn, Mark's knockback can't be previewed, so the dim lines (above) let the player see the Claw land in them.
  - **Ghost reasons:** "Only Linda" (an enemy next to her alone) and "Not by family" (it walked in by itself). These replace round 2's "Not next to family", which no longer covers both cases.
  - **The drawn line has to match the arrow** (CR-37). S8 shoots *through* Lucy. Whether arrows pass allies is unchecked. If they stop, the lines must stop at allies and S8 breaks; if they pass, the line must visibly pass through.
- *On Q3:* cause-only (b) is one clause and the easiest to read. I'd keep (a) only with both displays built. Without them, (b).

**3. Lucy: "beside when they acted" reads when the preview arc is computed from where the attack starts. THJ's single gate is the better read.**
- *Dash:* John Dashes from beside her and ends 3 tiles away; her embers fly to the target anyway. It reads right **only if** the arc appeared while the player aimed the Dash from his current tile. Then the follow-up is what was shown, not a surprise.
- *The real trap is the approach move (CR-7), not the Dash.* The player hovers an enemy with John beside Lucy, and the approach preview walks John two tiles away to attack. "When they acted" means at the attack tile, so no follow-up. **Likeliest misread:** "she follows John." She follows whoever is beside her *at the attack's start*.
- *What to change:*
  - Compute the arc and the "+6" from the **ghost or approach tile** (FR-11's follow-zone logic). The arc then vanishes in the preview the moment the approach leaves her side, which teaches the rule.
  - State "when they acted" as "where the attack starts" (the Dash starts beside her; the approach ends before the attack starts).
- *THJ's single gate (drop the 3-tile reach):* better for reading.
  - The rule is one sentence, **"Lucy follows the attack of whoever is beside her"**, and needs only one check, adjacency, which the board already shows.
  - The badge loses "Out of reach" and keeps one reason, "Nobody beside".
  - The arc may now cross the board on Linda's long shots. That's fine: it's drawn only on a single-target hover and on the firing pick.
  - Two conditions:
    1. **No hidden third gate.** If her embers need line of sight, a blocked follow-up comes back as a silent gate. Lob them (her arc already reads as a lob), or show a ghost "Blocked".
    2. **Family Shelter keys off the same adjacency.** One signal then carries two effects; say it on the badge as "Beside Linda: follows, embers +1".
- Per-sibling gifts (Q4 b) are three rules against one. From the UX side, don't ship them unless Family Shelter reads flat.

**4. Mark: the knockback flies sideways from the punch, and with John on the board every hit starts a fourth prompt that can undo the formation.**
- *Likeliest misread:* "it goes away from Mark." In S8, Mark dashes to 3,1, south of the Claw, punches north, and the Claw flies **east**. A sideways slide after a punch reads as a bug.
- *What to change:*
  - Keep the rule "directly away from the victim" (the strongest objection).
  - **Telegraph the push from the victim.** For about 0.4 s draw a short arrow starting at Lucy, through the Claw, to its landing tile, in Mark's colour (once B4's contrast fix lands; Mark's near-black can't carry it on dark floors), plus the existing push visual. The wording on the badge does the rest: "knocks it **off them**".
- *Four heroes, one hit:* S8 has no John. With John fielded, the Claw's strike on Lucy first raises John's paused prompt (`OnActionStart`, any range). If pressed, Lucy lands on John's tile, no longer beside Linda, and beat 3 is gone. Then Mark, Linda (and Lucy) follow: up to four prompts per enemy hit, on a turn with five enemies.
  - The player built a formation for the chain, and the first prompt asks whether to break it. That's a fine decision only if it reads (point 1's ghost and arcs).
  - It's also the busiest stretch of the game. Count prompts per enemy turn in the session, not just per scenario. If one turn shows more than ~6 prompts, apply John's limit (posture, or round 3's "once per enemy turn" lever).

**5. Complexity recount, and what round 3 kept from the readability fixes.**
- *Rules, read as a player.* Round 3 says +4 −2. Counted the way a player has to learn them, it's about **+7 −2**:
  - John: switches places, anywhere (1);
  - Linda: two clauses (2), since each fails differently and gets its own ghost;
  - Lucy: beside when acting (1), plus reach 3 from her (1, which THJ's single gate removes);
  - Mark: knocks it off (1), plus the direction (1; "blocked tile, no push" is CR-18's general rule).
  - Removed: FTP and John's "within 2". Linda's and Papa's Shelter's rules are replaced, not removed. With THJ's single gate and posture replacing Wrath, it's about **+6 −3**.
- *On screen:* round 2's three pieces plus Lucy's arc and "+6" and the swap beat, plus round 3's needs:
  - the role tether on every prompt and the cause words (re-meant, plus text);
  - Linda's bow marker on push landings (re-meant FR-12);
  - John's ghosts and arcs on the prompt (re-meant);
  - Mark's push telegraph (new, small);
  - the posture bar (new, if adopted).
  - Removed: John's zone and cover marker, the NoFtp state, the Wrath box (re-meant).
- *Kept from round 2:* the contrast fix first (chunk 0, as promised), the armed badge with reasons, the End Turn hover, the "would have fired" ghost, Lucy's arc and "+6", the swap beat.
- *Dropped or not carried over:*
  - **John's prompt cost line** went with the break, but the swap's new cost (where the child lands) has no display. Point 1 replaces it.
  - **"The same drawing stays up through the enemy turn"** isn't restated for Linda. Point 2 needs it.
  - **The ghost's reason strings aren't updated for the new rules.** Only "Nobody beside" and "Out of reach" are listed. Missing: "Only Linda", "Not by family", "Blocked", "Guard broken"; and "Out of reach" goes if THJ's single gate is taken.
  - **The badge states lose their meaning.** With no arms and no FTP, John's and Mark's badges have no "not ready" state except posture broken. Say so, or the dot is always green.

**6. The test order can't check the misreads most at risk.**
- *The order doesn't fit:* the cold player comes "after chunks 1–3", but Linda's cause rule (chunk 4) and Lucy's beside rule (chunk 5) come after, so the cold player never sees S8's links 2 and 3, the riskiest reads in the plan. Move the cold player after chunk 5, or build 4 before 3: Linda's cause can be checked with Vault and Shield Dash before Mark's knockback exists.
- *Fix the session's data:* `requiredTimeScale` 0 doesn't buy THJ time to judge a two-clause house rule (the window is unscaled). Raise the QTE profile's `duration` for Linda and Lucy in the session (data, reversible) and note it changes the feel.
- **What a cold player must be checked on first:**
  1. **John's prompt, asked while it's up: "If you press, where does Lucy end up, and is that safe?"** It's the one press with a real "no" and the costliest misread (sending a child into danger). If they can't answer inside the window, the swap is a reflex and point 1's decision prompt is required.
  2. **After S8 plays once: "Why did Linda shoot, and why did Lucy follow?"** Tests the cause words and the tether.
  3. **On a fresh board, before End Turn: "Where would you put Linda, Lucy and Mark to make that happen again?"** If they can't, the chain is a lucky moment and not a decision.

## Per option

- **A, as built:** don't ship. Linda and Lucy fire alone (fails D-464), and nothing explains any prompt.
- **P2:** superseded. Its readability pieces carry over.
- **R3:** ship with changes. It needs the direction rule locked to "away from the victim"; John's decision prompt with the child ghost and the arcs to John's tile; Linda's two displays; Lucy's arc from the approach tile; the tether and cause words on every prompt; and the cold player moved after chunk 5.
- **Lucy:** take THJ's single gate, Family Shelter, and no per-sibling gifts.
- **Linda:** (a) both clauses only if both displays are built, otherwise (b) cause only.
- **John:** posture replacing Wrath, yes from the UX side, with the bar, the cost line and the break beat. Not as an addition on top of Wrath.
- **Mark:** the Setter (M-S) reads well once the direction is settled and telegraphed. Tag-in (M-T) is the easiest to read: player-turn, in the open, no direction rule. The Call (M-R) is the hardest: an ally moves mid-enemy-action with no preview. Shared Calm (M-C) is fine, but the barrier on another unit needs its own visual.

## What would change my mind

- A cold player predicts, before End Turn, whether S8's chain will happen, and says afterwards why each link fired, **without** the tether, the cause words or the push telegraph. Then those are gold-plating, and the chain explains itself through animation alone.
- A cold player answers "where does Lucy land?" correctly inside today's 1 s window on John's prompt in most presses. Then the decision prompt isn't needed; the ghost and the arcs may still be.
- The session counts at most 4–5 prompts on the busiest enemy turn with all four heroes. Then John's limit is a balance question, not a readability one.
