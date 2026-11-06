# Memory 4 rework: Mark's telling, "And then I arrived"

Size: L    Tier: 3    Assigned to: miso-game-designer (plan); miso-implementer (wiring, after approval)
Branch: `thj/onboarding` (the working main, D-396)
Status: waiting on THJ

## Why

THJ wants the fourth Hearth memory rebuilt around his edits to `GB_m4-mark` (drawing `m4-rework/m4now.png`, grid `m4-rework/m4.md`): the player plays Tempest Bloom instead of being handed it with two pulses, Mark arrives late with the boast, John holds a den mouth against summoning pools, and the Mark–Lucy Duo saves the cub. Today's wiring (`HearthMemoryWiring.Mark.cs`) has the Bloom as a one-mission grant with two turn-1 pulses, a two-stage fight and a "Reach the cub" walk. The design in the [levels plan, Segment 4](2026-10-26-onboarding-levels.md#segment-4--marks-telling-and-then-i-arrived) is older than both.

## Goal

A ~5-minute telling where the player does three family things in order, each with Mark's voice on top: the Bloom (Synergy), Mark's arrival chain (his kit), and Chained Assault (Duo), while John holds the door.

## Acceptance criteria

- [ ] A cold player fires the Tempest Bloom arrow themselves on the first turn, without a forced-target tool, in at least 4 of 5 tries.
- [ ] Mark's arrival is followed by a fresh player turn with the camera on Mark (selection after a Reset is random today; see Q8), and his Blitz plus Continuous Attack clear the two Claws that came with him.
- [ ] John standing on 7,5 plays his line, reveals the Claws by the mother and unlocks the Mark–Lucy Duo, which pulses until it is used.
- [ ] From the stage that unlocks it, Lucy and Mark can reach a tile where Chained Assault has 3 targets in the same turn.
- [ ] The last Claw by the mother dying plays her fall, the walk to the cub and the end, and the level is won. No "reach the cub" objective is left.
- [ ] Every stage moves on at a turn cap, so a slow or lost player still reaches the end.
- [ ] No Duo other than Mark–Lucy, and no Cleanse, can be used in the level.

## Scope

In: the level's flow, layout and per-unit values, stages, sequences, locks, hints, AP caps, the lines needed, and the tech each beat depends on.
Out: game code, prefab edits, the Cyclone redesign (not built; this plan uses the Cyclone as built, `cyclone-redesign.md` §2), the narrative's final wording (for `miso-narrative`).

## Touches

Systems: level objectives (stages, conditions), level sequences (reveal, move, phase reset, dialogue, camera), `LevelAbilityLock`, `GuidedAbilityHint`, `TurnStartActionPointLimit`, `HiddenLevelUnits`, Corruption pool `CP_Spawner` (data), and from the tech check ([`reports/m4-mark-rework-tech.md`](../../reports/m4-mark-rework-tech.md)) one small new sequence, `CastAbilitySequence` (S, not core), plus data: a 0-XP Hearth Claw and pool variants, and pool turns listed as `SpecificTurns`. No core system is changed by the recommended design. A phase reset (`CurrentPhaseManipulationAction` Reset) is used as it is today in Memory 1.
USPs: Synergies (Tempest Bloom), Duos (Chained Assault), Family Roles (Watch, Counter, John's hold)
Docs: levels plan Segment 4, narrative draft Step 4, the Hearth time table; no GDD rule changes (all of this is level data)

---

## Problem and evidence

**What THJ reported:** the telling should *show* the family doing what Mark boasts about, and the boasts should be things the player does. Today the Bloom is a grant plus two pulses on turn 1. Nothing orders the two clicks, nothing makes the Cyclone tile obvious, and the arrival line plays in the opening before anything has happened.

**Root problem:** the segment has three lessons (Bloom, Mark's chain, the Duo) and one emotional beat (the mother). They all sit on one undirected board. The player can do them in any order, or miss them. Each needs its own stage: one beat, one action, then Mark's line. The layout should make the right action the obvious one, so the guidance never has to force it.

**Evidence:**

- The levels plan's UX critic: "Segment 4 taught nothing: a Synergy, a Duo, Continuous Attack and Focus in 4 min, cued only by boast lines" (levels plan, critics table).
- Today's wiring pulses Cyclone and Bow Attack on turn 1 at the same time (`WireHints`: `hints[0].Set(cyclone, 1)`, `hints[1].Set(bowAttack, 1)`). Nothing makes the Cyclone come first. **Verified** in `HearthMemoryWiring.Mark.cs`.
- The vision's playtest list names "Linda shooting into Lucy's cyclone" among the moments players liked. It deserves to be the player's own act.
- Memories 1 and 3 already use the tools this needs: hidden groups revealed by a sequence, a phase reset in a cut-in, ability locks that unlock and pulse, turn-1 AP caps (D-350, D-373, D-380, D-384, D-393).

---

## My reading of THJ's request

Coordinates are the drawing's (`m4now`). The prefab's top room sits one column right of the old `m4head` grid, so the wiring constants (`MarkWalkTo` 13,2, `CubTiles` 6..8,9) are stale and must be re-read from the prefab. The `note 7,10 Ryker` in `m4.md` points at a tile with no cell. I assume the cub is at **8,10** and the mother at **9,10** (the old 7,10 and 8,10 moved one column right). To check in the prefab.

| # | THJ's item | My reading | Confirm / correct |
|---|---|---|---|
| 1 | Mark and the two bottom-right Claws hidden at start | One reveal group `arrival`: Mark 15,2, Claws 11,2 and 13,2 | **Confirm.** Tech T3: can `HiddenLevelUnits` hide a *player* unit? (not covered by the tech check) |
| 2 | Play Tempest Bloom after the opening line | See [Item 2 options](#item-2-how-the-player-plays-tempest-bloom). **Correction to B as drawn:** Lucy on 7,2 can't reach the den. The Bloom tile is 4,4 (the corridor crossing, where the old prism was), 5 tiles from 7,2, and her Cyclone reaches 3 (GDD; the asset may say 4, T8). Lucy must start in the bottom room, and A's "she runs right" becomes part of the arrival | Correct |
| 3 | Mark appears, turn resets, Mark selected, Mark and Lucy in front in the narrow path | **Selection:** after a Reset the game auto-selects a random unit that can act (tech check). Making it Mark takes two new small sequences (tag the others `Status.Inactive`, then give them AP back), so I propose the camera on Mark instead (Q8). **Narrow path = the x = 9 passage (9,2 → 9,3 → 9,4) up to the top room.** Lucy runs to 9,3 during the arrival sequence. Mark's arrival chain (Blitz 13,2, Continuous Attack 11,2) ends on 11,2, 2 tiles from the passage. Both are then one move from the Duo tiles | Propose (Q4) |
| 4 | All Duos and Cleanse locked | All seven Duos and all four Cleanse buttons locked all level; only Mark–Lucy unlocks (at John's line). Reason for Cleanse: one Cleanse destroys a Corruption pool (`level-chunks.md` hazard table), which would make John's hold pointless | Confirm |
| 5 | John to 7,5 → his line → new Claws on top → Duo hint → Duo unlocks and pulses | **Correction: John can't start on 7,5** (drawn there), or the objective is done at once. He starts on **10,5**, 3 steps away, in the top room. "New Claws appear on top" = **the Claws by the mother start hidden** and appear at his line. Otherwise they walk down at the family before the Duo exists, and the player kills them with basic attacks (Q2) | Correct, propose |
| 6 | Top Claws dead → mother dies → success | Stage 3 = "every Claw by the mother dead". It must count only that group, because the pools keep Claws alive in the den (T5) | Confirm |
| 7 | Pools keep one Claw each | The `P` tiles are the existing Corruption pools (`CP_Spawner`, `spawnLimit` 1). Tech check: as placed they refill on enemy turns 1, 3 and 5 only. Listing every turn (`intervalMode = SpecificTurns`) makes them check each enemy turn (data; `interval = 0` is a core bug that never refires). Spawned Claws give 3 XP today, so they need a **0-XP Hearth Claw plus pool variants** (data). That is an exception to **D-345** (no spawned enemies in the memory). Still open: whether spawns come in Alerted (EN-12: spawns are Unaware unless a hostile is within 3, and both pools are 5+ from everyone) | Confirm, with Q3 |
| 8 | Heroes walk to the cub in a sequence, no "reach the cub" goal | Fixed walkers: **Lucy and Mark** (the Duo pair, nearest after the Duo, and Lucy is the cub's future owner). Tech check: `MoveUnitSequence` walks a unit by nickname to a fixed cell along a real path, one unit after another, and does **nothing, silently, if the path is blocked**. The cub and the mother are sprites, not units; the mother's fall already works (LSB `motherFalls`). "Closest" or "next to" is new code (S–M) | Propose (Q5) |

---

## Item 2: how the player plays Tempest Bloom

### The geometry that makes it work (all options)

The left corridor (y = 4) and its spur (x = 4, up to the pool on 4,7) cross at **4,4**. A Cyclone there, hit by an arrow coming up column 4, splits left, right and up along the three arms where THJ put the Claws. That is chunk 13 (the prism) in its new place. Linda on **4,2** shoots up column 4. 4,3 is a gap, so the arrow must cross it (T6). The Cyclone is 2 tiles away. Her range is 4, so if a copy keeps the arrow's remaining range (T7), each copy flies 2 tiles past the Cyclone:

| Arm | Tiles from the Cyclone | Claws hit (first at 6, next ×0.6 = 3.6) |
|---|---|---|
| Left | 3,4 (1), 2,4 (2), 1,4 (3) | 2,4 |
| Right | 5,4 (1), 6,4 (2), 7,4 (3) | 6,4 |
| Up | 4,5 (1), 4,6 (2), 4,7 pool (3) | 4,5 then 4,6 |

With in-play HP **2,4 = 6, 6,4 = 6, 4,5 = 6, 4,6 = 3**, four Claws die. **1,4 and 7,4 keep 10 HP**: they are 3 out and survive under either copy-range model (3.6 at most if copies fly the full 4). 7,4 stays as the Claw at the den mouth that John will face. Linda's arrow numbers are the levels plan's (arrow 6, ×0.6 per next enemy, GDD Linda LI-3 to LI-6).

**The reach trick.** Lucy on **4,1** is exactly 3 from 4,4. Every other den tile is 4 or more away (3,4, 5,4, 4,5). Every other tile in her reach is in the empty bottom room. So if the player places the Cyclone (option D), the only tile that faces an enemy is the right one, and the layout does the choosing. If the cast range is really 4 (T8), Lucy starts on **4,0** and the trick holds the same way (4,4 is 4 away, 3,4 and 5,4 are 5). Linda's lanes from 4,2: only column 4 has an enemy in range (row 2 is empty while the arrival group is hidden). So her only shot is the right one too.

**What the tech check changed** ([`reports/m4-mark-rework-tech.md`](../../reports/m4-mark-rework-tech.md)):

- No forced action exists. Building one is a core change (M, Tier 3).
- A sequence *can* cast Lucy's Cyclone on a cell with a new `CastAbilitySequence` (S, not core). That makes A cheap.
- `LevelAbilityLock` has **one unlock moment for all heroes and no re-lock**, so it can't unlock "Linda's bow, then the kits, then the Duo" in steps. D's ordering guard via locks is gone.
- There is no "ability used → play a sequence" trigger.
- Auto-selection picks at random among the units that can still act. With **only one unit holding AP, that unit is selected**, and `TurnStartActionPointLimit` sets turn 1's AP (built).
- A Reset ticks the player faction once more (the Cyclone loses a turn of life). It refills AP without re-firing the AP limit.

From these facts, the **cheapest version that teaches is A+**: the sequence casts the Cyclone at John's call, and the player fires the arrow, the act that *triggers* the Synergy.

### Options compared

| | A. Scripted Cyclone, Lucy runs off (THJ) | **A+. Lucy casts on John's call, the player shoots (recommended)** | B. Two guided casts with a reset between (THJ) | C. Forced action | D. Layout-led, both clicks by the player | E. Full cutscene (old plan) |
|---|---|---|---|---|---|---|
| What happens | A sequence casts the Cyclone, walks Lucy right; control returns with the Cyclone there | Opening: John "Lucy, shut the den!", and the sequence casts her Cyclone on 4,4 in view (Lucy stays on 4,1; she runs ahead later, in the arrival). Turn 1: **only Linda has AP (1)**, so she is the one auto-selected; her bow pulses; her only lane with a target runs through the Cyclone | Lucy 1 AP, Cyclone pulses; Reset; Linda 1 AP, bow pulses | Only the right unit, button and tile can be clicked | Lucy 1 AP and Linda 1 AP; Lucy's reach leaves 4,4 as the only den tile; Linda shoots after | A sequence fires both |
| Teaching (learns the Bloom by doing it?) | ● The Cyclone appears with no cause shown | ★ Sees Lucy cast it on John's call, then fires the arrow that *triggers* the Synergy (the GDD's "when": Linda's arrow enters the Cyclone) | ★ Both halves | ● Clicks a glowing tile | ★ Both halves | ✗ Watches |
| The boast's comedy | ● The "forgot the combo" gag is invisible | ★ The player made the shot, then "Did I?" / "In my version, you did." | ★ | ★ | ★ | ● |
| Pace | ★ | ★ One click | ● Two prompts and a Reset in between read as a glitch; the Reset also costs the Cyclone a turn of life | ★ | ★ | ★ |
| Rules the player tracks | none new | none new | a mid-turn Reset | a target lock | none new | none |
| Tech (tech check) | `CastAbilitySequence` S + `MoveUnitSequence` ✓ | **`CastAbilitySequence` S** (not core); AP cap ✓ and pulse ✓ built; deterministic selection ✓ (one unit with AP) | Set AP after a Reset (S) + a trigger on "Cyclone used" (new, S) + pinning (tag sequence S) | Core, M, Tier 3 | Trigger on "Cyclone used" (new, S); without it the order isn't guarded; staged unlocks impossible (one unlock, no re-lock) | `CastAbilitySequence` ×2 |
| Risk | Low | Linda walks instead of shooting (1 AP); the stage cap covers it | Two new pieces for one beat | Core change for one beat | Lucy may walk or Linda shoot first; random first selection | No lesson |
| USP | Synergy half-taught | **Synergy taught** | Synergy taught | Synergy taught, low agency | Synergy taught | Synergy shown |

**Recommendation: A+.** It costs one small non-core sequence, and the player performs the act that defines the Synergy. Lucy's cast is shown, not skipped, so the cause and effect read: John calls, Lucy's storm lands in the den mouth, my arrow goes into it and splits. It keeps A's "Lucy runs right", moved to the arrival so she ends up in front for the Duo.

**Upgrade path, D:** both clicks by the player. Choose it if THJ wants Lucy's click too. It needs one more new piece (a "Cyclone used → sequence" trigger, S), and with no ordering guard, a player who shoots first loses the Bloom. Even then the boast covers the miss ("Did I?" / "In my version, you did.").

---

## Lens notes

**Creative.** Target: *a tall tale the player is in on.* Mark tells it big, and the player makes his claims come true one by one: the cave blooms, Mark walks in and drops two Claws in one breath, John plants himself in the den mouth, and Lucy and Mark save the cub together. Then the jokes stop, the mother lies down, and the two who saved her cub walk up to it. Over the bar: the Bloom splitting down three arms of the den on the first click, and the Duo's ghost fists landing around the mother. The original element is the comic structure. The boast lines come *after* the player has done the thing, so the player is complicit, not lectured. The family-under-pressure note is John: "I'll hold them off. You save them." The father takes the dull, dangerous job so the children can do the rescue.

**Systems.** Rules: four stages (below). Each is an existing condition or a turn cap. The levers:

| Lever | Start value | Why |
|---|---|---|
| Den Claws' HP | 2,4 / 6,4 / 4,5 = 6; 4,6 = 3; 1,4 / 7,4 = 10 | The Bloom kills 4 under either copy-range model; 7,4 survives to face John |
| Arrival Claws' HP | 11,2 / 13,2 = 8 | Each Blitz (8) kills, so Continuous Attack chains (old plan's gallery values) |
| Top Claws | 3, at 9,8 / 10,8 / 10,7, HP 7 | From 9,5 all three are within 4 (3, 4, 3). Chained Assault at ×0.7 does 2.1 + 5.6 = 7.7 (≥ 7, even rounded down per hit: 2 + 5 = 7). The Duo ends the fight |
| Pool cadence | 1 (a Claw each enemy turn when the pool's own Claw is dead) | THJ's "each turn"; was 3 |
| Turn-1 AP | Linda 1, Lucy 0, John 0 (Mark hidden) | One action, and Linda is the only unit that can act, so she is auto-selected (tech check) |
| Caps | Stage 1: 1; stage 2: 2; stage 3: 4 (as `Turns` caps: "when turn N+1 begins") | Every stage moves on |

Interactions:

- The Cyclone stays on 4,4 and drifts toward enemies afterwards (it may finish 7,4 or 1,4, which is fine).
- Linda's **Watch** fires on pool Claws walking down column 4 (4,6 is 4 from 4,2; 4,5 is 3).
- Lucy's **follow-up** may hit 11,2 when Mark Blitzes 13,2 (she is 3 away on 9,3). It's harmless, and if it kills, the QTE swing has no target.
- Mark's **Counter**: if the Duo is delayed and a top Claw hits Lucy on 9,5, Mark on 9,4 is within 2 of every tile next to her.
- Pass-by: Lucy walks through Mark, and John through anyone.

Failure cases:

- The player spends Lucy's or Mark's AP before moving John. The Duo is unlocked with nobody able to use it, so it waits a turn; the hint keeps pulsing (WhenUnlocked ignores turns).
- John never goes to 7,5. Den Claws pour into the top room. Stage 2's cap plays the beat anyway.
- A dominant strategy is possible: Mark could kill the top Claws alone with Blitz. With only 1 AP left after his chain that can't happen on the unlock turn, and the Duo's 3 targets beat 1 Blitz.

**UX.** What the player sees, in order:

1. John's call, then Lucy's Cyclone landing in the den mouth (sequence).
2. Linda selected (the only one with AP), her bow pulsing.
3. One lane with a target, through the storm.
4. The split.
5. The arrival cut-in, then a fresh turn framed on Mark.
6. The objective line "Hold the den mouth" with the tile marked (T12), then John's line and the reveal.
7. The Duo button pulses on Lucy and Mark, and the Duo preview shows the three targets (CR-37 to CR-43).
8. The ending plays out with no input.

New on-screen elements: **one**, the Corruption pool, which is existing art new to the player. It needs no explanation: Claws come out of it, and John is between them and the cub. The objective tile marker is the existing objective UI, if T12 holds.

Likeliest misread: **after the reset, the player thinks Mark is the one who should go to 7,5** ("the camera is on Mark, the objective says hold the mouth"). After a Reset the auto-selection is random, so it may even pick John or Linda. Mitigation: the objective text names John ("John: hold the den mouth") and the marker sits on 7,5. Second misread: the reset itself ("did I lose my turn?"). The arrival cut-in ends on Mark's "Exactly on time." over a full AP bar, as Memory 1's cut-in does (D-384), so players have seen this once already.

**Where the lenses disagree.** Creative wants the four top Claws visible from the start, menacing the mother. Systems and UX want them hidden: visible and alert, they walk down before the Duo unlocks, and the player kills them with basic attacks, which spends the Duo's lesson. I lean hidden (Q2). The mother and cub stand alone at the top from the start, and the Claws that "come for her" at John's line are the threat that makes him say it.

---

## The beat list

`[S]` is a sequence (input off, HUD hidden), `[P]` the player's turn. Tech dependencies are tagged T*n* ([list below](#tech-dependencies-for-the-explores-findings)).

| # | Beat | On screen | Player does | Systems |
|---|---|---|---|---|
| 0 | **[S] Opening** | Grid fades in on the bottom room, the den across the gap, John up top, the mother over the cub | — | Intro sequence. Mission rules as the other segments: Tutorial tier, `level xp none`, `level fp full`, all alert. `LevelAbilityLock` from the start: every Duo trigger and every `CleanseAbility` (tech check: it can). No kit locks: turn 1 is held by AP alone |
| 0b | Lines (N1): Mark sets the scene. John: "Lucy, shut the den!" (in-character, not an instruction). **`CastAbilitySequence`: Lucy casts Cyclone on 4,4** (no AP spent; it then behaves as normal, tech check). John: "Linda, through her storm!" (N2) | | | AP cap turn 1 (`TurnStartActionPointLimit`, built): Linda 1, Lucy 0, John 0 |
| 1 | **[P] Turn 1, the Bloom** | Linda auto-selected (the only unit with AP); her bow pulses (`GuidedAbilityHint`, turn 1); one lane has a target, column 4 through the storm | Shoots; the arrow splits three ways; 4 Claws die | Stage 1 completes: "any of 2,4 / 6,4 / 4,5 / 4,6 destroyed" (`EntitiesDestroyedLOCondition`, aggregation Any), hidden objective. Cap 1 as fallback (if she walks instead, the turn ends with no AP left) |
| 4 | **[S] Arrival** (stage 1's complete sequence) | Mark: "And Linda shot straight into Lucy's fire, and the whole cave bloomed." · Linda: "Did I?" · Mark: "In my version, you did." → Lucy runs 4,1 → 9,3 (`MoveUnitSequence`; route 5,1 / 5,2 / 9,2 / 9,3 is clear of allies, since a blocked path is a silent no-op) → camera east → reveal `arrival` (Mark 15,2, Claws 11,2, 13,2) → Mark: "And then I arrived." · Lucy: "Late." · Mark: "Exactly on time." | — | LSB **Reset** (fresh player turn, everyone's AP refilled; the AP limit doesn't re-fire; the player faction ticks once more, so cooldowns and the Cyclone lose a turn) → camera on Mark → input on. Selection is random among the units that can act (Q8). Stage 2 objective shows |
| 5 | **[P] Turn 1 again: Mark's entrance** | Camera on Mark; objective "John: hold the den mouth." with 7,5 marked (T12) | Mark Blitzes 13,2 (2 away), QTE swing kills 11,2 (2 away), ends on 11,2 with 1 AP | Continuous Attack 1 FTP (MA-2 as built). Atman's Focus +1 per hit, not pointed at |
| 6 | **[P] John to the mouth** | | John 10,5 → 7,5 (3 steps: 9,5 / 8,5 / 7,5) | Stage 2 completes: John on 7,5 (`UnitTileOccupiedLOCondition`), or cap 2 |
| 7 | **[S] The hold** (stage 2's complete sequence) | John: "I'll hold them off. You save them." → camera to the top → reveal `top` (9,8, 10,8, 10,7) → Mark: "Lucy's fire, my fists. As we practiced." · Lucy: "We never practiced that." · Mark: "I practiced. You followed." (M4-5 to M4-7, moved here) → camera back | — | Unlock the Mark–Lucy Duo (`LevelAbilityLock` unlock; T2: the tech check says an unlock applies to all heroes at once with no re-lock. If that means the whole lock list opens, the other Duos and Cleanse open here too, and keeping them shut needs "unlock per preset", S) → its WhenUnlocked hint pulses until used. Stage 3 objective shows: "Save the cub." (an explicit-list condition has no "{n} left" counter; a counter is a new small condition class, S) + "Turns left in the memory: {remaining_0}." **Stage 3 must activate after the reveal**: hidden units probably count as destroyed before they are revealed (tech check) |
| 8 | **[P] The Duo** | Duo button pulses on Lucy and on Mark | Mark 11,2 → 9,4 (4 steps, his last AP). Lucy 9,3 → 9,5 (2 steps), then Chained Assault with her last AP: 3 targets within 4, mash, all three die | DU-1: activator needs ≥ 1 AP and pays 1 AP in Mark–Lucy; 2 FTP. Range origin T13: from 9,5 the targets are 3 / 4 / 3 |
| 9 | **[S] Ending** (stage 3 complete = win; played in the outro) | Camera to the ledge → the mother falls (LSB `motherFalls`, kept) → Mark, level voice (N7, rewritten: she was there all along) → Lucy walks to 8,9, Mark to 9,9 → "The cub cried out." → Lucy: "She saved her. We only carried her home." → grid fades → Hearth cutaway (kept: Margaret, "Ten Claws, Lucy." / "At least.") | — | No jokes from the mother's fall on (D-171). The pool Claws are still in the den, and input is off |

**Reset count: one** (beat 4, THJ's). I don't add a second at John's line (Q6). Beats 2 and 3 of the first draft (a Cyclone cast by the player, then an unlock of Linda's bow) are folded into 0b and 1 by the A+ choice.

---

## Grids

Coordinates as `m4now` (16 × 11, x from the left, y from the bottom). **Don't rebuild the prefab from these:** `GB_m4-mark` is hand-edited and is the master (skill rebuild rule). They are the brief for the edit and for the wiring tool. `_` is no cell. 4,3 stays a gap that the arrow must cross (T6). If arrows don't cross gaps, 4,3 becomes a cell with an obstacle that blocks walking but not arrows, so that the den stays sealed from the bottom room.

### 1 · Start (player turn 1, before the Bloom)

```grid id=m4r-start title="Memory 4 rework · start (hidden units drawn, tinted)"
_ _ _ _ _ _ _ _ . . _ _ _ _ _ _
_ _ _ _ _ _ _ . . . . _ _ _ _ _
_ _ _ _ _ _ _ . . c c . _ _ _ _
_ _ _ _ P _ _ . . . c . _ _ _ _
_ _ _ _ c _ _ . . . . . _ _ _ _
_ _ _ _ c _ _ . . . J . _ _ _ _
P c c . . . c c _ . _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _
_ _ . . L . . . . . . c . c . M
_ _ . . U . . _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _ _ _ _ _ _ _
--
cells 9,8 10,8 10,7 enemy hidden: top
cells 11,2 13,2 15,2 mark hidden: arrival
cells 7,5 john den mouth
note 8,10 cub
note 9,10 mother
note 4,3 gap
level name Memory 4 · Mark
level tier tutorial
level alert all
level xp none
level fp full
level hidden top 9,8 10,8 10,7
level hidden arrival 11,2 13,2 15,2
```

Note: Lucy 4,1 and Linda 4,2 (Lucy 4,0 if the Cyclone reaches 4, T8). John 10,5. Den Claws 1,4 / 2,4 / 6,4 / 7,4 / 4,5 / 4,6, pools 0,4 and 4,7. Alert check (skill): everyone starts alert by the mission rule, but no enemy turn comes before the Bloom and the reset, so the first enemy turn sees John already at the mouth if the player follows the flow. Nearest visible threat to the family: 4,5 is 3 from Linda, across the gap. The top room's fourth Claw (THJ's 10,9) is dropped (lever: keep it if THJ wants Mark's Counter or a turn-2 clean-up).

### 2 · The Bloom (turn 1)

```grid id=m4r-bloom title="Memory 4 rework · the Bloom: Cyclone on 4,4, arrow up column 4"
_ _ _ _ _ _ _ _ . . _ _ _ _ _ _
_ _ _ _ _ _ _ . . . . _ _ _ _ _
_ _ _ _ _ _ _ . . . . . _ _ _ _
_ _ _ _ P _ _ . . . . . _ _ _ _
_ _ _ _ c _ _ . . . . . _ _ _ _
_ _ _ _ c _ _ . . . J . _ _ _ _
P c c . ~ . c c _ . _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _
_ _ . . L . . . . . . . . . . .
_ _ . . U . . _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _ _ _ _ _ _ _
--
arrow 4,2 4,4 linda bow
arrow 4,4 2,4 linda dy=-10 copy
arrow 4,4 6,4 linda dy=-10 copy
arrow 4,4 4,6 linda dx=10 copy
cells 2,4 6,4 4,5 4,6 enemy die
step 4,4 1
step 4,2 2
```

Note: step 1 is Lucy's Cyclone from 4,1, cast by the opening sequence (A+). It's 3 away, inside her own reach, so the cast looks legal. Step 2 is Linda's shot, 2 to the Cyclone across the gap. Copies fly 2 past (T7) and kill 2,4, 6,4, 4,5 (6 each) and 4,6 (3.6 against 3). 1,4 and 7,4 survive.

### 3 · Arrival (after the reset; still turn 1)

```grid id=m4r-arrival title="Memory 4 rework · arrival: Mark's chain, John to the mouth"
_ _ _ _ _ _ _ _ . . _ _ _ _ _ _
_ _ _ _ _ _ _ . . . . _ _ _ _ _
_ _ _ _ _ _ _ . . . . . _ _ _ _
_ _ _ _ P _ _ . . . . . _ _ _ _
_ _ _ _ . _ _ . . . . . _ _ _ _
_ _ _ _ . _ _ . . . J . _ _ _ _
P c . . ~ . . c _ . _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ U _ _ _ _ _ _
_ _ . . L . . . . . . c . c . M
_ _ . . . . . _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _ _ _ _ _ _ _
--
arrow 4,1 5,1 5,2 9,2 9,3 lucy dy=8 scripted run
arrow 15,2 13,2 11,2 mark dy=-10 Blitz, then QTE swing
arrow 10,5 9,5 7,5 john dy=-10 hold the mouth
step 13,2 1
step 11,2 2
step 7,5 3
cells 7,5 john
```

Note: Lucy ran to 9,3 in the cut-in. Mark Blitzes 13,2 (2 away), steps in, and the Continuous Attack QTE takes 11,2 (2 away), leaving him on 11,2 with 1 AP. John walks 3 to 7,5 (assumed move 4, T15). The Cyclone is drawn where it was cast; after the reset it may have drifted (T9).

### 4 · The hold and the Duo (after John's line; still turn 1)

```grid id=m4r-hold title="Memory 4 rework · the hold: top Claws revealed, Chained Assault from 9,5"
_ _ _ _ _ _ _ _ . . _ _ _ _ _ _
_ _ _ _ _ _ _ . . . . _ _ _ _ _
_ _ _ _ _ _ _ . . c c . _ _ _ _
_ _ _ _ P _ _ . . . c . _ _ _ _
_ _ _ _ . _ _ . . . . . _ _ _ _
_ _ _ _ . _ _ J . U . . _ _ _ _
P c . . ~ . . c _ M _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _
_ _ . . L . . . . . . . . . . .
_ _ . . . . . _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _ _ _ _ _ _ _
--
range 9,5 4 lucy Chained Assault reach
arrow 9,3 9,5 lucy dx=10
arrow 11,2 9,2 9,4 mark dy=10
cells 7,4 enemy one at a time
step 9,5 1
```

Note: Lucy walks 2 (9,3 → 9,5) and keeps 1 AP for the Duo. Mark walks 4 (11,2 → 9,4) on his last AP. From 9,5 the targets are 10,7 (3), 9,8 (3) and 10,8 (4): all three, nearest first. From 9,4 only two are in reach (4, 4; 10,8 is 5). So if the reach is measured from Mark (T13), the two swap tiles. John on 7,5 has one attacker tile, 7,4. The den is sealed: 7,4 → 7,5 is its only link to the top room.

### 5 · Ending (sequence, no input)

```grid id=m4r-end title="Memory 4 rework · ending: the mother falls, Lucy and Mark walk to the cub"
_ _ _ _ _ _ _ _ . . _ _ _ _ _ _
_ _ _ _ _ _ _ . . . . _ _ _ _ _
_ _ _ _ _ _ _ . . . . . _ _ _ _
_ _ _ _ P _ _ . . . . . _ _ _ _
_ _ _ _ . _ _ . . . . . _ _ _ _
_ _ _ _ . _ _ J . U . . _ _ _ _
P c . . . . . c _ M _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _
_ _ . . L . . . . . . . . . . .
_ _ . . . . . _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _ _ _ _ _ _ _
--
arrow 9,5 9,7 8,7 8,9 lucy walk
arrow 9,4 9,9 mark dx=12 walk
cells 8,9 9,9 note walk-to tiles
note 8,10 cub
note 9,10 mother falls
step 8,9 1
step 9,9 2
```

Note: Lucy moves first, then Mark (so Mark's path up column 9 is clear). The walk tiles depend on where the cub and mother scenery really are (assumed 8,10 and 9,10).

**Distances checked (counted on the axes, in text only; the drawings are not rendered yet):**

- Lucy's cast: 4,1 → 4,4 = 3. Other den tiles 4+.
- Linda's shot: 4,2 → 4,4 = 2 (gap at 4,3).
- Mark's chain: Blitz 2 + swing 2.
- John: 10,5 → 7,5 = 3, one move.
- Lucy to the Duo tile: 2. Mark: 4.
- Duo targets from 9,5: 3 / 4 / 3.
- Pools to John: 4,7 → 7,5 = 5. 0,4 → 7,5 = 8. Both outside the 3-tile sight, hence T10.

---

## Turn budget, win and loss

| Stage | Done when | Cap (fallback) | Visible text | On complete |
|---|---|---|---|---|
| 1 Bloom | any of 2,4 / 6,4 / 4,5 / 4,6 destroyed (`EntitiesDestroyedLOCondition`, Any) | 1 (turn 2 begins) | hidden | Arrival sequence (beat 4), including the reset |
| 2 Hold | John on 7,5 (`UnitTileOccupiedLOCondition`) | 2 (turn 3 begins) | "John: hold the den mouth." | The hold sequence (beat 7) |
| 3 Save | 9,8 / 10,8 / 10,7 all destroyed (`EntitiesDestroyedLOCondition`, explicit list; the pools' Claws would break a "living units" count) | 4 (turn 5 begins) | "Save the cub." + "Turns left in the memory: {remaining_0}." | Win → the outro holds the whole ending (beat 9) |

Loss: the template's (family down). At Tutorial damage (about 3 a Claw) it's unlikely.

**Expected:** the Bloom turn, then one full turn (the chain, the hold and the Duo all on turn 1 after the reset), then the end. That's **one player turn plus the reset turn**. A player who delays the Duo finishes on turn 2.

**A slow player:**

- If Linda walks instead of shooting, the turn ends. The den Claws (alert) walk toward the family via 7,5 and the passage, and on turn 2 the cap plays the arrival anyway. The boast lines cover the missing Bloom.
- If John never goes to 7,5, the den Claws and the pool spawns (one per pool, at most two at a time plus 1,4 and 7,4) come up through 7,5 into the top room and down the passage at Lucy and Mark. At turn 3 the cap plays John's line wherever he stands, and the reveal and the Duo follow.
- If the Duo isn't used, the hint keeps pulsing, the top Claws attack Lucy, Mark Counters, and the turn-5 cap ends the telling. Pools never empty the den, but the den is sealed as long as John stands on 7,5.

**Time (cold player, the levels plan's rates):** opening and lines 0.5, Bloom turn 0.75, arrival cut-in 0.5, Mark/John/Duo turn 1.5, enemy turn 0.3, ending 0.75 ≈ **4.5 min** (+0.4 cutaway). That's within the plan's 5.0 for the segment.

---

## Tech dependencies

Answered rows are from the tech check ([`reports/m4-mark-rework-tech.md`](../../reports/m4-mark-rework-tech.md)). Open rows are still to check, each with a no-tech fallback.

| ID | Needed for | Question | Answer / if no |
|---|---|---|---|
| T1 | Option D only | A trigger "ability X used → play a sequence"? | **None exists** (new, S). A+ doesn't need it |
| T2 | Beats 0, 7 | `LevelAbilityLock`: Duos and Cleanse, then Mark–Lucy alone? | **Locks every Duo trigger and `CleanseAbility`; one unlock for all heroes, no re-lock.** Open: does the unlock open the whole list? If so, "unlock per preset" (S, the report's #10) |
| T3 | Beat 4 | Can a player unit be hidden and revealed (`HiddenLevelUnits`)? | Open. If no: Mark stands on 15,2 off-camera and walks in (old wiring); the two Claws stay hidden |
| T4 | Beats 1, 4 | Can a sequence select a unit? | **No.** Auto-selection is random among units that can act. Turn 1: deterministic, since only Linda has AP. After the Reset: random (Q8) |
| T5 | Stages 1, 3 | A condition over a listed set of units? | **Yes:** `EntitiesDestroyedLOCondition` (explicit list), no counter (new condition with a counter, S). Hidden units probably count as destroyed before the reveal, so stage 3 must start after it |
| T6 | Beat 1 | Does an arrow cross a tile with no cell (4,3)? | Open. If no: a cell with a walk-blocking obstacle that arrows pass |
| T7 | Beat 1 | Bloom copies' range: the remainder (2 here) or the full 4? | Open. Retune HP; at range 1 only 4,5 dies (the stage still completes) |
| T8 | Option D only | Cyclone cast range 3 or 4? | Open; irrelevant to A+ (the sequence casts on 4,4) |
| T9 | Beat 4 | What a Reset does | **Refills AP, raises no turn start (the AP limit doesn't re-fire), ticks the player faction once more** (cooldowns, statuses, Cyclone life). Turn number: assumed unchanged |
| T10 | Pools | `CP_Spawner` cadence, XP, alert | **Cadence:** `SpecificTurns` listing every turn (data). **XP:** 3 today, so a 0-XP Hearth Claw plus pool variants (data). Spawns count for living-unit conditions, and Cleanse removes pools (locked). **Open:** do spawns come in Alerted? If not, they sit Unaware at 5+ tiles and never reach John |
| T11 | Beats 4, 9 | `MoveUnitSequence` | **Fixed cell, real path, chained one after another, silent no-op if blocked.** Routes and end tiles must be free (as drawn) |
| T12 | Beat 5 | Does a tile objective mark its tiles on the board? | Open. If no: objective text only |
| T13 | Beat 8 | Chained Assault "within 4" measured from Lucy, Mark or the activator (level-chunks To check 16)? | Open. If from Mark, swap Lucy's and Mark's tiles |
| T15 | Beats 5, 6, 8 | Hero walk range (assumed 4; John's from `Stat_SPD`) | Open. At 3: Mark reaches 9,3 instead of 9,4 (Duo from Lucy still fine) |
| T16 | Beat 0b | Can a sequence cast Lucy's Cyclone on a cell? | **Not today; `CastAbilitySequence` is S, not core** (`AbilityOrchestrator.ActivateAbility`, as Continuous Attack uses it). No AP spent; the Cyclone then behaves normally |

---

## USP check

- **Family Roles:** strengthened. Linda's Watch covers John's den from below. Mark's Counter guards Lucy on the top. John's role here is his position more than his Role: the family's shield standing in the door.
- **Synergies:** strengthened. Tempest Bloom goes from a grant the player may not find to the player's own shot through Lucy's storm, the moment the vision names as a playtest favourite.
- **Duos:** strengthened. Chained Assault is the climax and the only Duo, unlocked by the story, with 3 guaranteed targets.
- **Home:** neutral on purpose (a memory level). The cutaway and the Hearth frame are unchanged.

## Complexity budget

The one sentence: *"John holds the den while Lucy and Mark save the cub."* New on-screen element: the Corruption pool (existing art, new to the player). It replaces nothing because the old segment had no hold; it's needed so the hold has a reason. Everything else reuses this memory's own tools (locks, pulses, AP caps, reveals, a reset). The one item that adds tracking is the pools, which is why Q3 asks rather than decides.

## Risks

- **New pieces on one level.** The recommended version needs one new sequence (`CastAbilitySequence`, S, not core) and data: the 0-XP pool Claws and `SpecificTurns`. "Unlock per preset" (S) is needed only if T2's unlock opens the whole list. Every open T row has a no-tech fallback, and the flow still ends at every cap.
- **Stage 3 completes at once.** Hidden units probably count as destroyed before their reveal, so the queued stage 3 must not be evaluated until the hold sequence has revealed the `top` group. Check this in the wiring tests.
- **A blocked scripted walk does nothing, silently.** Lucy's run and the cub walk need free routes and end tiles. A pool Claw that slipped into the top room could stand on 8,9 or 9,9: the outro then skips that walker. Pick end tiles in the sequence's own order, and check them in the play check.
- **The reset reads as a bug.** Memory 1 already uses one at its cut-in, so it's the second time the player sees it. Keep it inside a cut-in with Mark's line on top.
- **Lucy is fragile at the front (15 HP).** The top Claws can only reach her after the Duo turn, and at about 3 each, two hits leave her at 9.
- **The mother's fall moves to the very end, right before the win.** That suits D-171 (the jokes stop there), but the cutaway follows fast. Narrative may want a beat of silence (a camera hold) before the fade.
- **Lucy's follow-up steals Mark's kill on 11,2.** The chain then has no second target. The impact is cosmetic, but note it for the play check.
- **Pool spawns and D-345.** Spawns give 3 XP today, and `NothingInTheHearthGivesExperience` would fail. The 0-XP variants fix it (data). See Q3.

---

## Recommendation

Build:

- **Option A+** for the Bloom: the opening sequence casts Lucy's Cyclone on 4,4 at John's call, then turn 1 gives only Linda AP, and her bow pulses.
- The three-stage flow above, with **one reset** (at Mark's arrival) and the **camera on Mark** after it.
- John starting on **10,5**.
- The **three** top Claws **hidden until John's line**.
- Lucy and Mark as the **fixed walkers** to the cub.
- The pools as **real Corruption pools refilling every enemy turn** (`SpecificTurns`, 0-XP Claw variants), if T10's open point (spawns come in Alerted) holds. Otherwise Q3's option b.

New code: `CastAbilitySequence` (S, not core), plus "unlock per preset" (S) only if T2 needs it. Starting values are in the levers table above.

**Playtest signal:**

- **Worked:** the cold player shoots through the storm without help, laughs or reacts at "Did I?", uses Mark's chain on the entrance turn, moves John without being told twice, and uses the Duo on the turn it unlocks. The segment takes ≤ 5 min.
- **Failed:** Linda walks instead of shooting (strengthen the pulse, or the line), they move Mark to 7,5 (objective text unclear), or they go a turn without using the Duo (Lucy or Mark out of AP: think about a reset at John's line, Q6). If players say the Bloom felt "done for them", that's the case for the D upgrade.

---

## Questions for THJ

**Q1. How does the player play Tempest Bloom?**
- Context: a forced unit, ability and cell is a core change (M, Tier 3; tech check). A sequence can cast the Cyclone with a new `CastAbilitySequence` (S). Locks unlock only once for everyone, and nothing fires a sequence when an ability is used. THJ's B can't work as drawn: Lucy on 7,2 is 5 from the den crossing, her Cyclone reaches 3, and B needs two new pieces (set AP after a Reset, a trigger on "Cyclone used"), while the Reset costs the Cyclone a turn of life.
- Options: A (scripted Cyclone, Lucy runs off, the player shoots); **A+ (John calls, the sequence casts Lucy's Cyclone on 4,4 in view, and only Linda has AP on turn 1, so she is auto-selected with her bow pulsing; Lucy runs ahead later, in the arrival)**; B; C (forced action); D (both clicks by the player: Lucy's reach leaves 4,4 the only den tile, plus a new trigger to order them); E (cutscene).
- Recommendation: **A+**. D is the upgrade if you want Lucy's click too (+1 small new piece).
- Blocked: the wiring of beats 0 to 1; `CastAbilitySequence`.

**Q2. Are the Claws by the mother there from the start, or are they the "new Claws" at John's line?**
- Context: alert and visible, they walk down before the Duo unlocks, and get killed by basic attacks.
- Options: (a) **hidden until John's line** (the mother and cub alone at the top before that); (b) visible from the start but Unaware, waking at the line (fragile: any ability within 2 or a family member within 3 wakes them); (c) visible plus 2 more at the line (more enemies, longer).
- Recommendation: **(a)**, with **3** Claws (9,8 / 10,8 / 10,7), not 4, so the Duo's three targets end the fight. Keep 10,9 if you want a turn-2 clean-up or a Counter moment.
- Blocked: the `top` group and stage 3.

**Q3. Pools: real spawners or a staged reveal?**
- Context: the drawn `P` are Corruption pools (`CP_Spawner`). D-345 bans spawned enemies in the memory. The tech check found they refill only on enemy turns 1, 3 and 5 as placed. Every turn is data (`SpecificTurns`; `interval 0` is a core bug). Spawns give 3 XP, so 0-XP Hearth Claw and pool variants are needed (data, S). Still open: spawns may come in Unaware (EN-12), since both pools are 5+ from everyone, and then they'd never reach John.
- Options: (a) **real pools**, every enemy turn, 0-XP variants, Cleanse locked (a D-345 exception for these two), if spawns come in Alerted; (b) no spawning: the pool art stays, and 2 hidden Claws on the pool tiles are revealed at John's line ("more kept coming"); (c) no pools.
- Recommendation: **(a)** if the alert point holds. Otherwise **(b)**: it keeps D-345, and for a 2-turn hold it plays almost the same.
- Blocked: the den's data; the slow-player pressure.

**Q4. Which narrow path?**
- Context: you asked for Mark and Lucy in front in the narrow path.
- Options: (a) **the x = 9 passage**: Lucy runs to 9,3 in the arrival cut-in, and Mark's chain ends 2 tiles from it on 11,2; (b) the bottom corridor (y = 2), with Mark arriving nearer the passage (for example on 12,2, with the two Claws at 10,2 and 11,2 between him and Lucy).
- Recommendation: **(a)**.
- Blocked: the arrival sequence's run destination.

**Q5. Who walks to the cub?**
- Context: "closest heroes" needs new logic; fixed walkers are a built `MoveUnitSequence`.
- Options: (a) **Lucy and Mark, fixed**; (b) the two closest (new logic); (c) all four.
- Recommendation: **(a)**.
- Blocked: the ending sequence.

**Q6. A second reset at John's line?**
- Context: if the player spent Lucy's or Mark's AP before moving John, the Duo waits a turn (its pulse persists).
- Options: (a) **no** (control just returns, as you wrote); (b) reset at John's line so the Duo is always usable at once.
- Recommendation: **(a)**. Add (b) only if the play check shows players stranded without AP.
- Blocked: nothing now.

**Q7. John's start tile.**
- Context: drawn on 7,5, which would complete his objective at once.
- Options: (a) **10,5 in the top room**, 3 steps from the mouth; (b) with the sisters in the bottom room, 6+ steps through the passage, his whole turn.
- Recommendation: **(a)**.
- Blocked: the start layout.

**Q8. Must Mark be *selected* after the reset, or is the camera on him enough?**
- Context: after a Reset the game auto-selects a random unit that can act (tech check).
- Options: (a) **camera on Mark** plus his line, and the player clicks him (no new code); (b) true selection: tag the others `Status.Inactive` during the Reset so only Mark gets AP and is selected, then untag them and give their AP back with a "set AP" sequence (two new small sequences); this also means Mark acts first, alone.
- Recommendation: **(a)**. Take (b) if the play check shows players starting with John or Linda and missing Mark's entrance.
- Blocked: nothing; (b) is additive.

---

## Lines needed (for `miso-narrative`)

| ID | Where | Need |
|---|---|---|
| N1 | Opening | 1 to 2 lines, Mark (off): sets the den and the cub without explaining anything. Then John's call to Lucy ("shut the den" in spirit), played just before the sequence casts her Cyclone |
| N2 | Right after the scripted Cyclone, still in the opening | John's call to Linda ("through her storm" in spirit) |
| M4-8 to M4-10 | After the Bloom | Kept, moved from the opening to after the act |
| M4-1 to M4-3 | Arrival | Kept ("And then I arrived." per THJ) |
| N5 | John on 7,5 | THJ's "I'll hold them off. You save them." Polish only |
| M4-5 to M4-7 | The hold | Kept, moved from "first Chained Assault bark" to the Duo hint |
| N7 | Ending | **Rewrite M4-11 and M4-12.** "Then her mother came" no longer fits: she is there from the start. Something like "She'd stood over the cub the whole time. Until the last Claw fell." Then M4-13, the narrator's "The cub cried out.", and Lucy's line as today. No jokes (D-171) |
| Cutaway | End | Unchanged. "Ten Claws, Lucy." still works: 6 in the den, 2 with Mark, 3 by the mother, plus pool spawns |

## What changes in the levels plan (Segment 4)

- **Grid and table replaced** by this plan's grids and stages.
- **Teaches:** Tempest Bloom by the player (was scripted), Continuous Attack on the entrance, Chained Assault.
- **Enemies:** 6 den + 2 arrival + 3 top, plus pools (Q3).
- **Stages:** 3 instead of 2. The "Reach the cub" stage is removed, and **D-347 (the cue Claws fight during the walk) is superseded**: there is no player walk.
- **The mother's scene** moves from the end of stage 1 to the outro.
- **D-345:** an exception is proposed for the pools (Q3a), or kept (Q3b).
- **To check rows:** 2 resolved by design (scripted Bloom, the quiver question); T1 to T16 added.
- **Hearth time:** 5.0 → 4.5 + 0.4.

---

## Player experience

- The memory fades in. I'm in a small cave room with Linda and Lucy. Across a gap there's a corridor full of Claws, with two dark pools at its ends. Up top, a big wolf stands over a cub, and Dad is up there too.
- Mark (telling the story) sets the scene. Dad shouts at Lucy to shut the den, and she throws a storm right where the corridors cross.
- Dad shouts to Linda. She's the only one who can act, and her bow button glows. I shoot up at the storm, and the arrow splits three ways down the corridors. Four Claws drop.
- Mark: "And Linda shot straight into Lucy's fire, and the whole cave bloomed." Linda: "Did I?" Mark: "In my version, you did."
- Lucy runs ahead toward the passage to the cub. At the far end of the tunnel, Mark appears behind two Claws. "And then I arrived." "Late." "Exactly on time."
- It's my turn again with everyone fresh, and the camera is on Mark. I click him. He jumps one Claw, a button prompt lets him swing again, and the second drops.
- The goal says John must hold the den mouth, and the tile is marked. I walk Dad there, three steps.
- Dad: "I'll hold them off. You save them." Three Claws appear around the wolf. Mark: "Lucy's fire, my fists. As we practiced." Lucy: "We never practiced that." Mark: "I practiced. You followed."
- A new button glows on Lucy and Mark, their Duo. I step them up the passage and fire it: Lucy's embers and Mark's ghost fists hit all three Claws, and they fall.
- The jokes stop. The wolf lies down and doesn't get up. Lucy and Mark walk up to the cub, and it cries out. Lucy: "She saved her. We only carried her home."
- The grid fades back to the hearth. "Ten Claws, Lucy." "At least."

## Docs to update if approved

- `plans/onboarding/2026-10-26-onboarding-levels.md` Segment 4 (grid, table, Hearth time, To check), with a history line pointing here.
- `plans/onboarding/onboarding-narrative-draft.md` Step 4 (via `miso-narrative`: N1, N2, N5, N7, the moved lines).
- `design/level-chunks.md`: optional new pattern "hold the door" (a 1-wide mouth, a sealed spawner den, one defender), plus a coverage row for John. Only if THJ wants it catalogued.
- GDD: **no rule changes** (all level data). If Q3a is chosen, `missions-structure.md` gets no change either, because the pool cadence is per-level data. The decision log gets the D-345 exception (coordinator).
- `HearthMemoryWiring.Mark.cs` and `HearthMemoryMarkTests.cs` (implementer, after approval): stages, sequences, locks, AP limit, hints, hidden groups, re-read tile constants.

## Gates

Compile / tests / review: for the wiring, later. Play check: **yes** (THJ plays the segment cold-style before commit). Docs: above. Drawings: the coordinator renders this doc's 5 grid blocks and checks them.
