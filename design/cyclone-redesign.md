# Lucy's Cyclone: redesign proposal

Status: **Direction picked 2026-11-05** (THJ chose A, Pulling Gale; blocks enemies only; swallows enemy projectiles). Numbers, one-or-two Cyclones and the build plan are still open. Nothing built; not yet in `decisions.md` · Written 2026-11-05 · Owner: game designer (THJ approves) · Closes the open pass from D-055 (Q21 damage timing, S10 movement and pull) · Read from: `main` code and presets in the working tree, GDD `characters/lucy.md`, `family-systems.md`, decisions D-055, D-188, D-249, D-252, `level-chunks.md`.

## 1. The problem in one paragraph

Players can't predict the Cyclone because it has four hidden rules (movement, target choice, damage moments, lifetime) and none of them is shown. Two of those rules are accidents of the code, not design. A fixed, previewable rule set fixes this better than any retuning of numbers.

## 2. What it does today (read from the code)

| What players see | Why it happens | Where |
| --- | --- | --- |
| It moves "at the start of each faction's turn" | Its move is wired to the global turn-start event, which fires for every faction | `OnGridEntity.TurnGeneralTick`, `moveBaseMode = TurnGeneral` |
| It dies "too soon" and the length feels random | Life is 5, but it loses 1 on Lucy's own phase start **and** 1 on every faction's turn start: about 3 per round with two factions, so about 1.7 rounds, 2 enemy phases (D-055's finding holds) | `PhaseTick` + `TurnGeneralTick` |
| It picks "random" targets | It scores enemies by four-way distance, **+10, or +20 if it already visited that unit**, and takes the lowest; search range is `3 × turns left` (about the whole map at first) | `OnGridEntity.Move`, `TowardsUnits` |
| **It walks away from enemies, or wanders with none near** | An enemy standing on a cell that has a planted entity is dropped from the candidates, so an enemy already inside it doesn't count. With no candidate left it picks a **random free cell within 3** | `.Where(c => !c.CurrentCell.PlantedEntity)`, then `RandomElement()` fallback |
| Hits happen at unclear moments | Two paths, same 7× hit: the **main effect** on whoever is in the cell where it stops, and the **pass-by** on any enemy whose collider it touches on the way (not on its destination unit) | `PlugEntityInternal`, `OnTriggerEnter2D` |
| An enemy "walks into it" rarely hurts | The cell is unwalkable, so enemies can't walk in; in practice damage only comes when the Cyclone moves | `GridCell.IsWalkable` |
| It blocks everybody, but not units already inside | `IsWalkable` refuses any entry while a `disallowWalk` planted entity is there; a unit already standing in it isn't "walking" | `GridCell.IsWalkable` |
| It moves up to 3 cells, "Manhattan" | Path is found with four-way steps and cut at 3 (`moveRadius`) | `FindPathTo`, `path[min(count-1, 3)]` |

Numbers: cast 1 AP, cooldown 2, damage 7 × (Cyclone Power ×1.2 / ×1.4), lifetime 5, move 3, Howling Gale (run upgrade) adds Weak.

**Not verified:** whether enemy projectiles stop on it; whether the AI avoids it; whether Linda's Watch fires at units moved by something other than themselves; the ability asset's `radiusV` reads 4 while the GDD says cast range 3 (I did not trace which field is the cast range). A second copy of the Cyclone assets sits under `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/` and `Features/Player/Linda/Prefabs/`; I did not compare it with Lucy's. Check which one Lucy's prefab uses before editing.

## 3. Principles for the redesign

1. **Every hit has one named moment, and it is shown before it happens.**
2. **No randomness.** If it chooses, the choice follows a stated order that the player can read off the board.
3. **One sentence tells you what it stops and what it spares.**
4. **It is a setup tool for the family**, not a solo damage dealer: its job is to bunch, hold and expose enemies so the area combos pay off (Tempest Bloom first).
5. Lucy has 15 HP and 2 AP: whatever it costs her must be worth more than an ember.

## 4. Recommended: "Pulling Gale" (anchored, steered by Lucy)

> **The Cyclone is Lucy's weather: it stops and pulls the enemy and lets the family through.**

**Cast.** 1 AP, a free cell within 3, cooldown 3. One Cyclone at a time (a run upgrade could allow two). It resolves a Whirl at once (below), so the cast has an immediate payoff.

**Lifetime.** 3 enemy phases. It counts down **once per round**, at the start of the family's turn, and the Cyclone shows its remaining pips. It never counts on other factions' turns.

**Whirl (the only damage moment).** On cast, on a Steer, and at the start of every enemy turn, in this order:
1. **Pull:** each enemy within 2 cells of it (four-way) is pulled 1 cell straight toward it. A pull stops at a wall, a unit or another blocked cell. Immovable enemies (Masher, Deev, bosses) are not pulled.
2. **Hit:** each enemy in the four cells touching it takes 3 ×.
Pulling doesn't use up the enemy's own turn.

**Steer.** While a Cyclone is out, Lucy's Cyclone button becomes Steer: 1 AP, once per turn, move it up to 3 cells along a free four-way path (walls stop it; units don't), then it does a Whirl. This is the only way it moves. It never moves on its own and never picks a target.

**What it blocks.**

| | Blocks? | Notes |
| --- | --- | --- |
| Enemy bodies (walking, pushes, Command walks) | **Yes** | a wall for them; a push into it stops like a push into rock (CR-18) |
| The family's bodies (and allies, decoys) | **No** | they walk through, stand in it, are never hurt by it |
| Enemy projectiles | **Yes, swallowed** | an arrow that crosses its cell is destroyed; gives Lucy an answer to Archers. Needs a play check (see 7) |
| The family's projectiles (embers, Linda's arrows, Duo arrows) | **No** | they pass; Tempest Bloom still splits Linda's arrows |

**Preview (a requirement, not an extra).** Hover or selection shows: the pull range (a diamond of radius 2 with arrows pointing in), the four "3 ×" cells, the pips, and on Steer the path and landing cell. This is what makes it predictable.

**Starting numbers (to tune in play).** Whirl 3 × (about 4 Whirls over a cast, so up to 12 ×, but only for enemies that stay touching it; today one landing is 7 × and it lives about 1.7 rounds). Cyclone Power: ×1.2 / ×1.4 on the Whirl. Howling Gale: Weak for 2 turns on every enemy the Whirl hits. Pull 1 cell, range 2. Steer 3 cells.

**Why this one.** It answers the pull everybody expects, removes every random choice, and gives Lucy one meaningful decision a turn (where to put it) instead of a launch-and-hope. Its cost: Lucy spends AP to move it, and she loses the "it hunts for me" feel; the passive pull and Whirl are what make up for that.

## 5. Alternatives

**B. Deterministic drifter (keeps self-movement).** At the start of the family's turn it moves 2 cells along a four-way path toward the **nearest enemy by path length** (ties: the one closest to Lucy, then the lowest HP). Never toward an enemy it already touches; with no enemy in reach it stays. The next destination is drawn as a ghost with an arrow. Hits only when it stops: 4 × to enemies touching it; no pull, or a 1-cell pull as an upgrade. Blocking as in A. Cheap to build (a fixed target rule plus a preview), but the player still doesn't control it and can be surprised by the first-in-line choice.

**C. A controllable unit (ally faction or player unit, with Move and Explode).** Strongest agency and a fresh tactical layer, but it needs a unit with its own AP, turn slot, HP, targeting by enemies, a UI selection and the onboarding to teach it. Explode (a one-time big hit that ends it) is a good ending. Recommend it only if THJ wants Cyclone to become a second character; otherwise A gets most of the control for a fraction of the work.

| | A. Pulling Gale | B. Drifter | C. Unit |
| --- | --- | --- | --- |
| Predictable | Yes: it never moves alone | Yes, if the ghost is shown | Yes |
| Readable | Pull and hit cells are drawn | One ghost and one arrow | Familiar (a unit) |
| Fun / agency | Medium-high (placement + steer) | Medium (watching) | High |
| Effective for Lucy | High with area combos | Medium | High, but costs AP |
| Tempest Bloom | Better (stays in the lane, pulls into it) | Worse (leaves the lane) | Controllable, fine |
| Build size | Medium: pull, per-faction blocking, preview, life fix | Small-medium | Large |

## 6. Effect on combos and synergies

| Piece | Effect | Action |
| --- | --- | --- |
| **Tempest Bloom** (Linda, Lucy; also a run upgrade) | Better. The Cyclone stays where Linda's lane is, and the pull puts enemies on the three cells the arrow splits into (the cell behind it and the two sides): a setup (Lucy) and payoff (Linda) beat. The trigger is the Cyclone's collider and a two-prefab whitelist; this stays as is | Because the family can now walk through it, the split arrow's landing rule changes: today it lands on the last cell before the Cyclone because the Cyclone blocks (D-252, LI-6). Proposed: it lands **on the Cyclone's own cell**, and the family can walk in and pick it up. Update D-252 and LI-6 |
| Linda's basic and Marks-Sisters arrows through the Cyclone | Pass through and split; unchanged | None |
| **Linda's Watch** (Role) | A pulled enemy is moved by the Cyclone during the enemy phase. If Watch fires on forced moves, pulls will feed Watch Shots (and spend the quiver) | Check in play; decide whether pulls count |
| **Lucy's Role** (follow-up) | Fires after a family member's action that did real damage (D-277). The Whirl is not a family member's action | State it: Whirl damage never triggers her Role |
| **Sisters' Rivalry** | A Cyclone kill is not a basic attack, so no AP gift. A Whirl that softens an enemy for Linda's basic kill still sets it up | None |
| **Explosive Crescendo, Chained Assault, Family Watchers, Shield Flare** | Pull clumps enemies next to the Cyclone, which is exactly what these area effects want | Make the clump the showcase in a chunk |
| **Catch & Return / "Mark catches Cyclone copies" suggestion** | Copies still can't be caught today. With an anchored Cyclone Mark can stand beside it, which makes the suggestion easier to build | Keep as the open suggestion |
| **Shield Dash, Vault, Command, Harmonic Slam** | Pushing or walking an enemy into the Cyclone's cell stops at the cell before it. Pushing an enemy toward it from 2 cells works with the pull | Document as a wall rule |
| **Papa's Shelter, Blink, decoys** | The family isn't blocked, so Blink and walking next to John aren't affected (today the Cyclone can wall Lucy off) | None |
| **Cyclone Power, Howling Gale** | Both move to the Whirl; Gale's Weak applies to every enemy the Whirl hits | Reword both node and upgrade texts |
| **Hazards (spikes, mushrooms)** | A pull moves an enemy like any forced move; pulling into spikes or a mushroom cap is a combo | Check hazard rules for forced moves (CR-18) |

## 7. Chunks, tests and onboarding

- **Level chunks 1, 12, 13, 24** use the old rules ("nothing walks through it, it drifts into the three", "two stand at once from turn 3"). A throat seal still works (enemies can't pass), but "it drifts" becomes "it pulls", and chunk 12's two Cyclones need the run upgrade or a rewrite. The "to check" row 2 (what does the Cyclone drift toward?) is answered by this doc.
- **Tech notes.** `disallowWalk` is shared with other planted blockers, so per-faction blocking has to be a new option, not a change to `IsWalkable` for everyone. The life fix is to stop the `turnStarted` countdown and count only on the family's phase. A pull is a forced move; it should use the existing push/pull code. Domain reload is off, so any new static needs its reset hook.
- **Tests.** Edit-mode: life counts once per round; Whirl order (pull, then hit); blocking per faction; D-252 landing. Play-check: enemy arrows vs the Cyclone; Watch vs pulls; the preview. The AI regression test stays red as it is today.
- **Onboarding** (`thj/onboarding` unlocks the Cyclone after the interruption): the one-line rule above fits the unlock hint.

## 8. Decisions needed from THJ

1. A, B or C?
2. Block the family: no (recommended) or yes?
3. Swallow enemy projectiles: yes (recommended) or no?
4. Cyclone allowed twice at once only through a run upgrade, or always?
5. Whirl numbers: start from 3 ×, pull 1, range 2, lifetime 3 rounds, cooldown 3?

## 9. Build order (once approved)

1. Fix the life count, add the preview, and log Whirl damage as its own entry (small, safe on its own).
2. Per-faction blocking and the landing-rule change (D-252, LI-6).
3. Pull and Whirl, then Steer.
4. Rewrite chunks 1, 12, 13, 24 and the GDD (`lucy.md`, `family-systems.md`), then play-check.
