# UX critique: onboarding after the Hearth (option B)

2026-11-10. Read-only critic (Explore agent following `.claude/agents/miso-design-critic.md`, lens UX; the critic agent type wasn't available in the session). Saved verbatim by the coordinator.

## 1. Strongest objection

The plan teaches its two new Synergies with spoken lines and a goal tile. Neither shows the rule or what will happen, and the goal tile removes itself at the exact moment the lesson starts.

- **River, beat 2.** The objective is "John: hold the ford." (John on 11,3). When John steps on 11,3 the stage completes. The new objective feedback ticks and pulses ("done"), the goal tile disappears, and stage 3 "Defeat all" takes its place. All of that happens before Lucy has acted, and the step also wakes the far-bank Claws. From then on, the only carrier of "ember John" is three lines played a turn earlier: "If it gets hot, aim at me." / "*At* you?" / "Trust me." Those lines do not say:
  - that Shield Up must be on first (Lucy's targeting offers John only while his Shield Up is on, `characters/lucy.md` Fire Embers);
  - what the fireball will do to John;
  - where the copies go.
- **No preview, and the plan's own logic condemns that.** The plan adds a Tempest Bloom preview because "without it the Bloom is the one shot in the Hearth the player takes on faith". Shield Flare's diagonal copies and Catch & Return's return copy are then the two shots taken on faith, and they are the only things the plan teaches after the Hearth. A cold player has never been asked to target an ally with a damaging attack. Shown no outcome on the ally, they read it as friendly fire and decline.
- **Ridge, beat 2 is worse.** "Shoot at me." / "From the far side." invites a click on Mark, but Linda's bow aims along a row at the Claws. In one turn the player then needs three exact actions: Mark's Vault past the queue, Linda to 4,1 (which wakes the queue), and the bow along row 1. Then comes a catch QTE they have never seen, with a shorter-than-usual prompt wait (D-273, MA-3). If they miss the press, the arrow just flies on, so the player never learns that anything was offered. The plan has no fallback for the Ridge ("No hint planned").

Expected cold-player result: both lessons go unseen, the obvious play wins hurt, and the playtest reads "Synergies unused". That is the same failure THJ reported, in levels that now hurt more.

## 2. Other risks

- **Waking enemies becomes the central decision, and the player cannot see it before clicking.**
  - The Trail's stated "real decision" is that Linda on 4,1 wakes the queue.
  - Ridge beat 2 also depends on a wake.
  - The Asleep panel and the sight beat are cut, and the GDD says there is no wake marker on the move ghost (`enemies.md` Q8): "the player can't see a wake coming before the click, except by reading the Shift sight tiles".
  - Shift on an Unaware enemy draws its alert range with the strong red attack icon (CR-54, `enemies.md` Q10), which reads as "it can hit this tile". At the River ford, Shift on the islands may paint red around the safe goal tile 11,3, telling the player the tile is dangerous.
  - THJ's "sight needs no tutorial" was said while sight was incidental. This plan makes it the question. Either build the Q8 wake marker on the move ghost or don't make the wake the decision.
- **Memory 4: board and line disagree.**
  - The memory ends on the Duo while left-side Claws still stand, over "…and that was the last of them". A new player sees enemies on the board and a line saying there are none.
  - Stage 3's target is "only the three `top` Claws", but the goal highlight marks tiles, not units, so players will spend turns on the left-side Claws thinking every enemy counts.
  - The non-core fade-out step now exists: fade the leftover Claws (and, if wanted, John) out before the outro, so the board shows what the line says.
  - Switching off the pools also needs something on screen, or "cut the line" is invisible.
- **Memory 1: drained FTP bar.** Setting the FP fill to −99 means the first minute of the game shows an empty meter. A cold player reads "out of something" or "broken" before knowing what FTP is. If the FTP bar can't be hidden in Memory 1, prefer Kept AP or a switch over the drain.
- **The Pile's finisher assumes the player knows the sisters' Duo.** The only Duo used so far is Memory 4's Mark–Lucy Chained Assault, which targets differently. Marks-Sisters needs Linda on 3,4, lined up along row 4, while the player watches an ambush from two sides after a quiet grief beat. "It's on both bars" is not teaching. Plan for the `GuidedAbilityHint` from the start, not as a fallback.
- **No panels in levels that now hurt.**
  - With roles as built, the River's awake rush (clearing Claws start alert and reach 2,3 on enemy turn 1) shows Lucy's follow-up prompt and John's guard prompt for the first time while the player is under real damage.
  - The Ridge's family-first fix helps, but Watch and Mark's counter still arrive together there (F4).
  - Smaller: a game opening at Home before the Hearth must lock the stations, or players will click the Workshop. The Family tree auto-open must make "spend the point, then close" obvious.

## 3. Per option

- **A (numbers only):** don't ship. Harder fights do not make Synergies readable.
- **B (recommended):** ship with changes:
  - Keep the goal tile on through Lucy's turn: make stage 2 "Shield Flare hits an Archer", or add a second objective line "Lucy: ember John".
  - Add a Shield Flare preview (the four diagonals and their damage when Lucy hovers a shielded John) and a return-copy preview, alongside the Bloom preview.
  - Allow one-line on-screen captions for the two Synergy lessons. These are not panels.
  - Build the Q8 wake marker on the move ghost, or drop the wake as the Trail's decision.
  - Use the fade-out in Memory 4.
- **C (one combined search mission):** don't ship; both untaught Synergies in one mission.
- **D (do nothing):** don't ship.

**Bearing on THJ's questions:** Q1 (the Trail's decision depends on an unseen wake); Q2 (empty-meter misread if the drain is used); Q4 (use the fade-out; make the Duo's three targets readable); Q6 (harder tiers with no panels and no previews make misreads cost HP; Ridge family-first is right). The acceptance criterion "no tutorial panel after the Hearth, one line or a goal tile per new thing" should itself be a question for THJ: does a preview, a caption or an objective line count as allowed?

## 4. What would change my mind

A cold playtest with 3+ new players, no coaching: most fire Shield Flare on the River within beat 2 unprompted; most land the catch on the Ridge first try and can say what it did; after The Trail they say they woke the queue on purpose; nobody in Memory 4 attacks the left-side Claws thinking they're required; nobody comments on the empty FTP bar in Memory 1.
