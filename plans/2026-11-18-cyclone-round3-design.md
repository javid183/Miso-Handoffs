# Lucy's Cyclone, round 3: Drop on a foe, breathe in and out (design)

Size: L    Tier: 3 (item 3 changes an approved rule, LU-3; items 1 and 2 are game feel, THJ's area)    Assigned to: miso-game-designer
Branch: `thj/cyclone` (scope: this branch until it merges)
Status: waiting on THJ

## Why

THJ's feedback on the round 2 play check ([`playtests/2026-11-17-cyclone-round2-play-check.md`](../playtests/2026-11-17-cyclone-round2-play-check.md) › THJ Playtest feedback, notes 1 to 4):
1. Enemies about to take the Whirl's hit should be sucked toward the centre, spat back to their cell, then take the damage.
2. The carry should feel like push, pull and drag, not a chess pawn lifted and placed.
3. Let the Cyclone be cast on a cell held by an enemy; that enemy is pushed to a cell next to it.
4. More transparency on the arm-tip arrows and on the tint on the touching cells (visual tweak, no design).

Round 2's rules stand (D-547 to D-559: carry, one landing, heavies walk through and burst it, Gust retired, Cyclone Power 3 / 4 / 5). This plan changes one rule (LU-3's empty-cell cast) and adds presentation.

## Goal

Casting the Cyclone onto an enemy is one more sentence shared with the Steer, previewed with what exists, and every Cyclone move and hit reads as wind: grab, drag, fling, breathe in, spit out.

## Acceptance criteria (for the design, once approved)

- [ ] Item 3 is one rule the player can say in a sentence, and the same rule as the Steer's front shove (LU-6 step 1).
- [ ] No new on-screen element: the shoved enemy uses the existing ghost, tether, damage segment and hazard ring.
- [ ] Items 1 and 2 change no outcome, no order of events and no rule: only drawings and waits.
- [ ] A Whirl with no pull is no longer than today; a Whirl with a pull adds at most 0.1 s; a Steer with riders adds at most 0.2 s (see §6 timings).
- [ ] Each beat of each unit plays once per action: no unit is flung and then sucked in again in the same Whirl.

## Scope

In: the cast-on-an-enemy rule and its edges (direction, ties, blocked, heavies, damage, reactions, preview, AI, Steer, exploits); the presentation of the Whirl hit, the carry and the cast shove, with timings; item 4 as a data list.
Out: hold; per-cell pushes (D-549 stands); new chunk grids (no grid changes in this plan); the AI regression re-baseline; round 2's open items (one Watch per action, detour reachability, intent for heavies), which stay open for THJ.

## Touches

Systems: `AEffectCycloneSpawner` (cast check and apply order), a new cast-only cell check next to `CycloneRules.IsValidCastCell` (which stays the empty-cell check for the Steer's `CanEndOn` and Super Time), `CycloneCastPreview`, `CycloneCarryPlanner` (reused for the one shove), `CycloneEntity.Whirl.cs` / `.Steer.cs` (presenter waits), `CycloneCrossView` (alphas). No core system needs to change for the rule; the input hold in §6 may (see Risks).
USPs: Family Roles (Watch), Synergies (Tempest Bloom, bunching).
Docs: GDD `characters/lucy.md` LU-3, LU-4, LU-6, value table; `design/cyclone-redesign.md` round 3 note.

## Approach

### 1. Problem and evidence

**Symptom (3):** "much more fun if the Cyclone could be placed on enemies." **Root:** the cast is the only Cyclone move that can't touch an enemy where it stands. The Steer already shoves the enemy in front of it (LU-6 step 1), and it already ends on cells enemies stood on (verified: `CycloneCarryPlanner.TakeStep` shoves the front enemy before `CanEnd` checks the cell). Only the cast keeps LU-3's empty-cell rule, so the best spot (the middle of a pack, the enemy on Lucy's toes) is never castable. The rule is inconsistent, not missing.

**Symptom (1, 2):** "too mechanical, a chess pawn." **Root:** the Whirl's hit and the carry have no anticipation or follow-through. Verified: riders' drawings lerp in lockstep with the Cyclone (`CarryLanding.Glide`), then land in one frame; the hit is applied in the frame after the reactions settle, with only the Cyclone's swell before the pull (0.2 s, `swellSeconds`) as a tell. The wind never seems to act on bodies.

Evidence read: LU-3 to LU-7 and the value table (`characters/lucy.md`); `CycloneCarryPlanner.cs`, `CycloneEntity.Steer.cs`, `CycloneEntity.Whirl.cs`, `AEffectCycloneSpawner.cs`, `CycloneRules.IsValidCastCell` (three callers: the spawner, `CycloneSteerRules.CanEndOn`, Super Time in `LucyFactionRoleHandler.cs:246`); `CycloneCrossView.cs` colours; cast range on `Lucy_Cyclone_Ability.asset` (`radiusV` 3, `cellApplyTraverseMode` 1 = Adjacent, so four-way steps, Manhattan 3; verified in the asset and `GridEnums.cs`, the step count assumed from the mode's name).

### 2. Options compared (item 3)

| | 3A. Shoved on, the way it came (leaning) | 3B. 3A, with a fallback cell | 3C. Player picks the cell | 3D. Nearest free cell | 3E. Do nothing |
| --- | --- | --- | --- | --- | --- |
| Rule | The enemy is shoved one cell straight away from Lucy. Blocked: the cell isn't offered | As 3A; if blocked, the next free touching cell in a fixed turn order, never toward Lucy | Click the enemy, then click one of its free neighbours | Any free neighbour by a fixed scan | Empty cells only |
| Player experience | Into the Breach's push from the source: Lucy throws a storm and it knocks the foe back. Predictable before the hover | More castable cells, but where it goes is a second rule to learn | Most control; a second click every cast, and a choice most players don't care about | Feels random (the old slide fallback D-529 removed) | THJ's note stays |
| Rules | One sentence, the same as the Steer's front shove | One sentence plus an order | One sentence plus a second input | A hidden rule | None |
| Build | Small: one shove with the carry planner's move, a cast check, the preview | Small plus the order | Medium: two-step targeting | Small | None |
| Risk | Cells refused when blocked; ties at 4 cells | Order misreads | Slower turns, onboarding | Breaks principle 2 ("no hidden choice") | Stays less fun |
| USP | Watch gets cast setups; packs get centred (Tempest Bloom) | Same | Same | Same | Neutral |

**Leaning: 3A.** All three critics agreed; none wanted the fallback, the second click or the scan.

### 3. The 3A rules (proposed)

> **Player sentence:** "Drop the Cyclone on an enemy and it's knocked one cell away from Lucy."
> **Rule (LU-3 amended, shared with LU-6 step 1):** where the Cyclone arrives on an enemy, it shoves that enemy one cell onward, the way it came: on a cast, straight away from Lucy; on a Steer, the way it steps.

- **Direction.** Along the larger axis from Lucy to the cell. With Manhattan range 3, the only ties are Lucy's 4 diagonal neighbours (offset 1, 1). At a tie: the free one of the two; if both are free, one fixed order (proposal: along the row). The preview shows the result; no text explains it (UX critic).
- **Blocked.** If the shove cell is a wall, the map edge, a unit, a walk-blocking planted entity or a stashed entity, the enemy's cell isn't offered (the same check as the Steer's front shove, `CanTakeStep`). No chain pushes.
- **Who can be shoved.** The units the pull and the carry can move: enemies hostile to Lucy's faction, one cell in size, not Immovable. Heavies (Masher, Goblin Queen, Deev), large units, neutrals, allies and the family are never offered. A cell with a planted entity stays refused, an enemy standing on it included (unchanged LU-3: the Cyclone never shares a cell with one).
- **Heavies.** No special case beyond "not offered". Casting on a heavy to burst it at once was considered and rejected: a cooldown-4 cast spent for one hit.
- **Damage.** The shove is free. The enemy then stands on a touching cell, so the cast Whirl hits it (one damage moment, principle 1).
- **How it moves.** Like a carried enemy (D-549): one landing. A hazard on the landing cell fires, Family Roles answer the move (Watch, if it lands in Linda's lane), it wakes (EN-14, EN-15). No Crippled damage.
- **Order of the cast.** Shove lands → the Cyclone is planted → the cast Whirl: pull, reactions, hit (LU-4 unchanged).
- **One Watch per action** (known core limit, round 2 open item 1): the shove's landing can take the cast's one Watch answer, so an enemy the same cast pulls into Linda's lane gets none. Accepted. It is the same limit THJ will judge for the Steer.
- **Steer: unchanged.** It already ends on a cell an enemy stood on by shoving it (LU-6 step 1). The new sentence only names that.
- **Family Super Time and an AI-controlled Lucy:** empty cells only, as today (D-535). Super Time picks a random cell, and a random shove would be a hidden choice. An AI-controlled Lucy's evaluator would need the shove simulated (systems critic: assumed it would otherwise pick enemy cells; AI regression count risk). Invisible to the player, the same pattern as the Steer never being offered to the AI (D-540).
- **AI danger prediction and enemy intent:** nothing new to predict. The shove happens on Lucy's turn, and enemies plan from the board after it, as after any push. EN-18 is unchanged (the shoved enemy stands on a touching cell, which is already dangerous ground for its next move).

**Exploits and failure cases (systems critic and mine):**

| Case | Verdict |
| --- | --- |
| **Disengage and wall:** an adjacent Claw is shoved 1 away, and the Cyclone stands between it and Lucy (enemies can't enter it, LU-7), plus 3 damage | The strongest new use. Accepted as the fantasy (a fragile daughter's storm shoves danger off her). Limits: cooldown 4; one blocked cell is walked around in open ground; Blink is already a stronger escape. THJ decides: Q2 |
| Centring on a pack: up to 4 hit at the cast (the shoved one plus 3 neighbours already touching) | Possible today with 4 enemies round an empty cell; now easier. 12 damage for 1 AP at most, once per cooldown. Lever: watch it in play |
| Shove into spikes or a pool | A combo, like the pull (LU-4). The preview shows the hazard ring |
| The landing hazard kills the shoved enemy before the Whirl | Fine; the preview's HP bars show the Whirl hit only, as today. The hit simply finds no one |
| Shoving an enemy off a captive or objective tile | Allowed; the shove is a normal forced move |
| Waking an Unaware pack from range 3 | Already possible with a hit or a pull |
| Bosses | Immovable, never offered |

### 4. Items 1 and 2: the beats

All of this is presenter: drawings move, cells don't. Every unit keeps its cell until the one landing frame (D-549), the Whirl keeps its order (landings, pull, reactions, hit; D-555), and the hit is the same hit on the same targets. Two waits get longer (the hit and the landing come later), which is the only part that touches a routine.

**One breath per unit per action** (creative critic): a unit that already moved in this action (carried, shoved by the cast, pulled in from an arm) skips the inhale; its arrival was the breath, and at the hit it only recoils. Only enemies that stood still beside the Cyclone are sucked in and spat out. Only units the pull could move breathe: heavies don't lean (they resist the wind), they just recoil at the hit. That keeps the visual true to the rule.

**Whirl** (cast, after a Steer, end of each enemy turn):

| Beat | What the player sees | Time |
| --- | --- | --- |
| Swell | Only when a pull is planned: the Cyclone swells, the chevrons brighten | 0.1 s (was 0.2) |
| Pull | As today (pusher speed 4, one cell) | 0.25 s |
| Reactions | As today (Watch, hazards; settle 10 quiet frames) | as today |
| **Inhale** | The Cyclone swells (this replaces the old swell when nothing is pulled). Each still-standing pullable enemy beside it slides its drawing 35% of a cell toward the centre, ease-in, all together | 0.12 s |
| **Exhale and hit** | They snap back onto their cells (ease-out, no overshoot), and the hit lands as they arrive: flash, number, chip. Moved units and heavies recoil only (a 0.06 s jolt outward with the hit) | 0.08 s |
| Shrink | As today | as today |

Net: a Whirl with no pull: 0.2 s now, 0.2 s after (the inhale replaces the swell). With a pull: +0.1 s. With nobody to hit: no inhale at all. End-of-turn Whirls run every enemy turn, so this is the budget that matters (pace bundle P halved every turn wait; `tech/pace-timings.md`).

**Steer with riders** (grab, drag, fling):

| Beat | What the player sees | Time |
| --- | --- | --- |
| **Grab** | Before the glide, riders' drawings lean 30% toward the Cyclone (sides and rear). The front enemy doesn't lean: it gets shoved | 0.08 s |
| **Drag** | The glide as today (0.15 s a cell). Riders keep the lean and trail the Cyclone by a short lag, with a small tilt. The front enemy is kicked ahead at the start of each step (ease-out), a push, not a pull. A rider that joins part-way is grabbed during that step (no extra time) | 0.15 s a cell |
| **Fling** | Riders and the front enemy are thrown out of the lean to their landing cells: ease-out with a small hop arc, stopping exactly on the cell the ghost showed (no overshoot: it must not look like it went one cell further, UX critic). Then the one landing frame: plug, hazard, Watch, wake | 0.12 s |
| Whirl | As above; riders skip the inhale (they just moved) and recoil at the hit | |

Net: +0.2 s for a Steer with riders; nothing added to a Steer with none. A 3-cell Steer with riders and a pull is about 1.5 s before reactions; that's Lucy's showpiece action.

**Cast on an enemy:** the Cyclone appears, the enemy is flung one cell (the same fling, 0.12 s), then the landing frame, the Cyclone is planted, and the cast Whirl plays. The shoved enemy skips the inhale and recoils at the hit.

**Burst** (a heavy walks in): unchanged. The burst lands at once in the middle of the heavy's walk; no inhale (it would stall a core walk). Neighbours recoil with the hit.

**Rules the presenter must respect** (systems critic, verified in `CycloneEntity.Whirl.cs`):
- The burst check and the target list come **after** the inhale, just before the hit, so a burst during the inhale can't hit twice and a target that died or moved isn't hit.
- **No player input between the inhale and the hit.** On Lucy's turn the cast releases her action once the pull ends (`HoldCastWhileWhirlPulls`), so the player could act inside the 0.2 s. The tech plan picks the means (keep the action open until the hit, or a short input lock like the turn banner's). Round 2's play-check item 25 ("the pull and hit wait for your action") must still pass.
- The lean moves a visual child, not the unit's root, where possible (projectiles and the hover read the root; tech to confirm). Today's glide moves the root, so this is no new risk class.
- Abort (level end, the Cyclone destroyed, a unit dying mid-beat) snaps every drawing back to its cell.

**Considered, not in the plan:** ember flecks in the exhale and a short hitstop on a Whirl that hits 3 or more (creative critic). Both are art and feel levers for THJ after this play, not rules. A Cyclone "strain" wobble when a heavy resists: rejected, since the wobble already means "a heavy is coming through" (LU-7). Reusing it would be the misread.

### 5. Item 4: visual tweak (no design)

Values in `CycloneCrossView.cs` (code constants today; placeholder art):

| Element | Now (alpha) | Start value | Note |
| --- | --- | --- | --- |
| Touching-cell swirl tint (`TintColor`) | 0.3 | 0.18 | Keep the hue cool so the orange hazard ring stands out |
| Arm-tip chevron at rest (`ChevronColor`) | 0.75 | 0.45 | |
| Chevron flare in the beat (`ChevronFlareColor`) | 1.0 | 0.85 | Keep it brighter than at rest so the pull still reads |
| Dim under aim (`DimFactor`) | × 0.4 | unchanged | |

THJ tunes by eye. Making them serialized fields would let him tune without code (implementer's call, Tier 2).

### 6. Lens notes

**Creative.** *Target:* the storm feels alive: it reaches out, grabs bodies, hurls them and breathes. Lucy's wind shoves danger away from her (warmth against dread: the smallest Bergson pushing back). *The moment:* a Claw lunges at Lucy. On her turn she drops the Cyclone on it: the Claw is hurled one cell back, the cross catches its two packmates, the Whirl inhales, and all three are spat out and hit. The family's turn starts with the pack bunched in front of a storm wall. The creative critic's merge rule ("one breath per unit") is what keeps it reading as one confident storm, not a storm that changes its mind.

**Systems.** *Rule:* §3. *Levers:* shove distance 1 (fixed); whether distance-1 cells are castable (Q2); inhale depth 35% and times in §4; hit 3 × unchanged. *Interactions:* Watch (one answer per action, the shove may take it); hazards (landing only); Crippled (none: one landing); Howling Gale (Weak on the hit, as today); the burst (unchanged); EN-18 (unchanged). *Failure cases:* §3 table; the timing inserts (burst during the inhale, player input during the inhale), handled in §4. *Implementation notes (verified):* `IsValidCastCell` has three callers that need the empty-cell answer, so the cast gets its own check and the spawner shoves before it spawns, then re-checks that the cell is empty. The rider filter reads a live Cyclone (`IsPullable` uses `PullTagQuery` and the caster); at cast time there is none, so the cast check must use the prefab's query with plain references, as `CycloneCastPreview` already does, and stay safe on the AI worker thread.

**UX.**

| When | Shown |
| --- | --- |
| Cast aim, range | The range highlight includes castable enemy cells (they are in range and pass §3); refused enemies aren't highlighted |
| Hover a castable enemy | The cross at that cell, the enemy's ghost on its shove cell with the existing tether, the damage segment and lethal skull on the ghost, the hazard ring if it lands on one; ghosts for anything the Whirl pulls. The cursor aims the cast: no unit hover panel, no attack cursor (the same fix as round 2's Steer item 20) |
| Hover a refused enemy | Today's normal unit hover panel. The contrast ("this is a unit, not a target") is the signal, at no cost (UX critic) |
| Click | One click, as today |

*Likeliest misread:* at Lucy's 4 diagonal neighbours the player expects to pick the direction. The ghost shows it before the click. If play shows confusion, the fallback is to refuse ties (Q3). *Learning:* the Cyclone's description gains one clause (narrative); the ghost teaches the rest. *Budget:* one rule (a sentence, shared with the Steer); new on-screen elements: none; the beats are motion, not UI.

**Where the lenses disagree.** The creative side wanted fire flecks, hitstop and a strain wobble. The systems and UX sides want fewer seconds and fewer signals. I lean to the budget: the motion THJ asked for, merged so each unit breathes once, and the extras left as levers after he plays it.

### 7. USP check

- **Family Roles:** strengthened. The cast can now drop an enemy into Linda's lane on Lucy's turn (Watch answers the landing). Limited by the one-answer-per-action core rule.
- **Synergies:** strengthened. Centring on a pack bunches enemies on the cross for Tempest Bloom, Explosive Crescendo and Shield Flare.
- **Duos:** neutral on purpose.
- **Managing the Home:** neutral on purpose.

### 8. Critics

The `miso-design-critic` type isn't installed in this session. As in round 2, three read-only Explore agents ran one lens each, in parallel, without seeing each other.

| Critic | Strongest point | What I did |
| --- | --- | --- |
| Creative | Merge the double motion: one breath per unit per action. Fling then inhale reads as the storm changing its mind. "Away from Lucy" is the right fantasy. Add fire (ember flecks, hitstop) and show heavies straining | **Took** the merge, as "a unit that moved this action skips the inhale and recoils at the hit". It did *not* move the hit to the landing, which would break D-555's order. **Took** "away from Lucy". **Left** fire and hitstop as levers. **Rejected** the strain wobble (it already means "heavy coming") |
| Systems | It's a 1 AP disengage and wall: shove an adjacent enemy and the Cyclone stands between them. Don't offer distance 1. `IsValidCastCell` has three callers; the rider filter needs a live Cyclone; the inhale can double-hit on a burst or let the player act mid-beat; the shove can take the one Watch | **Took** the tech notes (own cast check, shove before spawn, plain-reference filter, burst check and targets after the inhale, no input mid-beat, Watch note). **Distance 1:** raised as Q2, with my lean to allow it. Removing it wouldn't remove the ties either: offset (1, 1) is Manhattan 2. **Rejected** greyed-out cells with a reason text (no more text) |
| UX | The ghost already answers the direction, so the rule stays one sentence, if the shove ghost is drawn exactly like a pull ghost. Keep the unit panel on refused enemies as the signal. Let the inhale replace the swell. The fling must not overshoot. Pulled units skip the inhale | **Took all of it.** Its tie rule ("the side with more room, else Lucy's facing") was replaced by "the free one, else one fixed order", which is simpler and also unexplained on screen |

What changed my mind: the double motion (I had planned fling, then a full inhale for riders) and the swell overlap (I had added the inhale on top of the swell).

### 9. Recommendation

**3A**, with the §4 beats and the §5 alphas.

Starting values: shove 1 cell, away from Lucy; ties: the free one, else along the row; distance-1 cells offered (Q2); swell 0.1 s before a pull, none without; inhale 35% of a cell, 0.12 s; exhale and hit 0.08 s; recoil 0.06 s; grab 30%, 0.08 s; fling 0.12 s, no overshoot; tint alpha 0.18, chevron 0.45, flare 0.85.

**Playtest signals:**
- **Worked:** THJ casts on an enemy at least once a level unprompted, and for a reason (to wall, to centre a pack, to feed Watch or a hazard). He predicts the shove before hovering. He calls the carry and the hit "storm-like", with no "it stalls". The enemy turn feels no slower.
- **Failed:** "why can't I cast there?" on blocked or heavy enemies (consider 3B's fallback); the diagonal tie surprises (refuse ties, Q3); the cast is used mainly as a disengage every cooldown (drop distance 1, Q2); the end-of-turn Whirl feels slow (cut the inhale to 0.08 s, or play it only when 2 or more are hit).

## Questions for THJ

**Q1. Should the Cyclone be castable on an enemy, which is then shoved one cell straight away from Lucy (3A)?** *Tier 3 (changes the approved LU-3).*
- Context: note 3. It is the Steer's front-shove rule applied to the cast (one sentence for both), previewed with the existing ghost. Touches Watch and bunching.
- Options:
  - (a) 3A, away from Lucy; a blocked shove refuses the cell (small build);
  - (b) 3B, the same with a fallback to another free touching cell in a fixed order;
  - (c) 3C, the player clicks the cell the enemy goes to (medium build, a second click);
  - (d) keep empty cells only.
- Recommendation: (a). Predictable, one rule, no new element.
- Blocked: the cast-shove tech plan and the preview change. Items 1, 2 and 4 don't wait on it.

**Q2. Should the 4 cells next to Lucy be castable on enemies (the "disengage and wall": an adjacent foe knocked back, the Cyclone left between them)?** *Tier 3 (changes what the player can do; Lucy's survival).*
- Context: the systems critic's strongest point. Lucy has 15 HP; Blink is her escape (cooldown 2); the Cyclone's cooldown is 4.
- Options:
  - (a) yes, any enemy cell in range;
  - (b) no, enemy cells only at distance 2 to 3 (empty cells next to Lucy stay castable);
  - (c) yes for now, cut if it becomes the main use.
- Recommendation: (a), read as (c). It is the strongest moment of the rule, and the wall is one cell that enemies walk around.
- Blocked: nothing beyond Q1 (it is one condition in the cast check).

**Q3. At Lucy's diagonal neighbours, where both directions are "away", which way does the enemy go?** *Tier 2 detail (asked because it touches the same rule).*
- Context: the only cells where the direction ties (Manhattan range 3). The preview shows the result either way.
- Options:
  - (a) the free one; if both are free, along the row;
  - (b) refuse those 4 cells for enemies;
  - (c) the player chooses (second click).
- Recommendation: (a).
- Blocked: nothing.

**Q4. Do you want the beats in §4 (one breath per unit; inhale replaces the swell; grab, drag, fling) at the starting times given?** *Tier 3 (game feel and pacing of the end-of-turn beat).*
- Context: notes 1 and 2. Presenter only: no outcome or order changes. Net time: a Whirl without a pull +0 s, with a pull +0.1 s, a Steer with riders +0.2 s.
- Options:
  - (a) as written, tuned in play;
  - (b) inhale for every unit hit, carried ones included (your note's literal reading; a double motion and +0.2 s on every Whirl);
  - (c) inhale only on Lucy's own Whirls (cast and Steer), not at the end of enemy turns (protects the enemy-turn pace).
- Recommendation: (a). Your request, merged so each unit moves once a beat, with no extra wait on the enemy turn.
- Blocked: the presenter chunk. Item 4 doesn't wait.

**Q5. Should ember flecks and a short hitstop on big Whirls be added now, or after this play?** *Tier 3 (game feel), low stakes.*
- Options: (a) after this play, if the wind still feels thin; (b) now.
- Recommendation: (a). Change one feel layer at a time.
- Blocked: nothing.

## Docs to update if approved

- **GDD `characters/lucy.md`:**
  - LU-3: cast on an enemy (the sentence, the direction and tie, blocked cells refused, who can be shoved, a free shove landing once); Super Time and an AI-controlled Lucy keep empty cells; the cast aim preview gains the shove ghost.
  - LU-4: the inhale and exhale before the hit (presentation), and the swell only before a pull.
  - LU-6: step 1 named as the same rule as the cast; grab, drag, fling.
  - Value table: swell 0.1 s, inhale and exhale times, fling, alphas (Source: `CycloneCrossView.cs`, `Cyclone.prefab`).
  - Card sentence: unchanged unless the narrative pass adds a clause.
- **`enemies.md`:** no change (EN-18 already covers the shoved enemy).
- **`design/cyclone-redesign.md`:** a round 3 note linking here.
- **Narrative (`miso-narrative`):** one clause in the Cyclone's description ("Cast it on an enemy to knock it away."), a proposal.
- **Level chunks:** no grids changed.

## Risks

- **Preview trust:** the shove must come from the same planner move the execution uses (the carry planner's front shove), with a test comparing them.
- **Input during the beat** may need a core input hook: the tech plan says which, and asks first if it touches `PlayerController` (core).
- **AI worker thread:** the cast check reads plain references only; an AI-controlled Lucy is kept to empty cells, so the AI regression count shouldn't move (verify: 43).
- **Creep:** change one lever per play (the alphas and times are separate from the rule).

## Gates

Design only: THJ answers Q1 to Q5 → tech plan (coordinator) → build (rule chunk, presenter chunk, alpha data) → compile, tests, review → THJ play check (needs his time) → docs above.
