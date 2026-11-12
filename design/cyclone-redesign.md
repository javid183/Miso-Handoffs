# Lucy's Cyclone: redesign (Pulling Gale, version 2)

> **As built (2026-11-12, `thj/cyclone`, not merged, not play-checked; D-529 to D-545).** Built to version 2 with the §7 numbers (D-530). The rules as built live in the GDD: [Lucy](gdd/characters/lucy.md#cyclone-pulling-gale) LU-3 to LU-7, [Combat rules](gdd/combat-rules.md) CR-3 (end-of-turn note), CR-57 (line of fire), CR-58 (pass-through cells), [Enemies](gdd/enemies.md) EN-18, EN-19. This page stays as the reasoning. Where the build differs from the text below:
> - **Not built:** Trailing Gale and Second Cyclone (D-531); the camera ease and wind sound in §6. Cross, pips and beat are placeholder art. Combat log lines read "✦ Whirl · Lucy: pulled N, hit M" and "✦ Gust · Lucy: pulled N".
> - **Pulls (§4.3):** units larger than one cell aren't pulled, as well as Immovable ones. A non-blocking hazard on the landing cell is fine and fires.
> - **Whirls per round (§4.3, §4.5):** one at the end of each enemy faction's turn, so two enemy factions make two a round; an enemy turn that is skipped makes none. On cast, the hit lands just after Lucy's action ends.
> - **Damage (§4.7):** Whirl hits are reported like ability hits, credited to the cast (stats, barks, kill XP and gold, the sisters' tally). Besides Lucy's follow-up, the Masher's counter also ignores them (D-537).
> - **Waking (§4.7):** as designed: a Whirl hit or a pull (Whirl or Gust) wakes an Unaware enemy, and the wake spreads as any wake does (D-542, built in C5), so a Gust can wake a pack through one pulled member.
> - **Howling Gale (§7):** as designed: Weak for 2 turns on every enemy a Whirl hits, and only those (D-545); a Gust applies nothing. Texts applied as working text (D-544).
> - **Steer (§4.4):** it also can't cross planted entities that block walking, and it crosses allies and non-blocking hazards. It's a second ability shown in the Cyclone's slot (its own cooldown 1), never offered to an AI-controlled Lucy (D-540).
> - **What it stops (§4.6):** ranged moves (Blink, Vault, teleports) never land on it; a dash attack or the Footrace loser that would stop on it uses the nearest standable cell next to the target (D-538). Enemy shots are blocked only when the centre-to-centre line passes through the tile's inside; corner grazes and neighbours (diagonal too) can shoot (D-541).
> - **Enemy behaviour (§5):** built as a filter on where a move ends, not as a move cost. Only "not on the arms" is guaranteed; in open ground an enemy can wait diagonally next to the Cyclone, not "3 or more cells away". Immovable enemies avoid the cross too. A ranged enemy drops firing spots where every shot is blocked, but isn't forced to move to a clear line (EN-19). The Dark Shaman keeps any spot with an ally in heal range even when its bolt is blocked (support first, D-543).
> - **Family Super Time:** Lucy's cast lands only on an empty cell, and is skipped while her Cyclone is out (D-535).
> - **§10:** `radiusV` is now 3. The live hit was already 3 × before this build (D-518), not 7 × as §2 says.

Status: **Built on `thj/cyclone`** (see the note above). Earlier: **Direction picked by THJ** (2026-11-05: A, Pulling Gale; blocks enemies only; stops enemy ranged attacks). Version 2 folds in the review of 2026-11-06 and THJ's answers of 2026-11-10 (AI treats the cross as dangerous ground; a visible Whirl beat; Steer pulls once, at the end; Linda's Watch reacts to pulls). Numbers still to tune; nothing built; not yet in `decisions.md` · Owner: game designer (THJ approves) · Closes the open pass from D-055 (Q21 damage timing, S10 movement and pull) · Read from: `main` code and presets in the working tree, GDD `characters/lucy.md`, `characters/linda.md`, `family-systems.md`, `combat-rules.md`, `enemies.md`, decisions D-055, D-188, D-249, D-252, `level-chunks.md`.

## 1. The problem

Players can't predict the Cyclone because four rules are hidden (movement, target choice, damage moments, lifetime), and two of them are accidents of the code. A fixed rule set that is drawn on the board fixes this better than retuning numbers.

## 2. What it does today (read from the code)

| What players see | Why | Where |
| --- | --- | --- |
| It moves at the start of each faction's turn | Its move listens to the global turn-start event, which fires for every faction | `OnGridEntity.TurnGeneralTick`, `moveBaseMode = TurnGeneral` |
| It dies early and the length feels random | Life 5, minus 1 on Lucy's phase start **and** 1 on every faction's turn start: about 3 a round, so about 1.7 rounds (D-055's finding holds) | `PhaseTick` + `TurnGeneralTick` |
| Targets look random | Enemies scored by four-way distance **+10, or +20 if already visited**; lowest wins; search range `3 × turns left` | `OnGridEntity.Move`, `TowardsUnits` |
| **It walks away from enemies, or wanders** | An enemy on a cell that holds a planted entity is dropped from the candidates, so one already inside doesn't count; with no candidate it picks a **random free cell within 3** | `.Where(c => !c.CurrentCell.PlantedEntity)`, `RandomElement()` |
| It sometimes ends on a different cell than expected | A cell holds one planted entity. If the target cell already has one (spikes, webs, pools, mushrooms), the plug fails and it slides to the nearest free cell | `GridPluggableEntity.CanOccupy`, `GridCell.PlugEntity` fallback |
| Hits come at unclear moments | Two paths, same 7×: the main effect on whoever is in the cell where it stops, and the pass-by on enemies whose collider it touches on the way | `PlugEntityInternal`, `OnTriggerEnter2D` |
| It blocks everybody, but not units already inside | `IsWalkable` refuses entry while a `disallowWalk` planted entity is there; a unit already inside isn't walking | `GridCell.IsWalkable` |
| It moves up to 3 cells | Four-way path, cut at 3 | `FindPathTo`, `path[min(count-1, 3)]` |
| Projectiles ignore it (except Tempest Bloom) | It has no faction, so the contact filter skips it; only Linda's two whitelisted arrows react, through `LucyCycloneProjectileScatter`. Archer arrows are lobbed arcs that act only at their target (`TargetReach`, `VerticalFactor`, no clear path needed) | `Projectile.TryHitOnContact`, `ShootingArrow.prefab` |

Numbers today: cast 1 AP, cooldown 2, 7 × (Cyclone Power ×1.2 / ×1.4), life 5, move 3; Howling Gale (run upgrade) adds Weak.

## 3. Principles

1. **Every hit has one named moment, drawn before it happens.**
2. **No randomness, no hidden choice.** It moves only when Lucy moves it.
3. **One sentence tells you what it stops and what it spares.**
4. **It sets up the family.** Its job is to bunch and hold enemies for the family's turn (Tempest Bloom, Watch, area attacks).
5. Lucy has 15 HP and 2 AP: what it costs her must be worth more than an ember.

## 4. The rules

> **Lucy's Cyclone holds a cross. At the end of the enemy turn, enemies on its arms are dragged in and hit. The family passes through but can't stop in it.**

### 4.1 The cross
The Cyclone sits on one cell. Its **arms** run 2 cells in each of the four straight directions (8 cells); diagonals are outside. The **touching cells** are the 4 cells next to it. The cross is always drawn on the ground (section 6).

### 4.2 Cast
1 AP, an empty cell within 3 with no planted entity (no spikes, webs, pools, mushrooms, traps), cooldown 4. One Cyclone at a time. The cast does a Whirl at once.

### 4.3 Whirl: the only damage
On cast, and at the **end of every enemy turn** (after all enemies have acted):
1. **Pull.** Each enemy on an arm moves 1 cell toward the Cyclone if that cell is free; nearest first. Immovable units (Masher, Deev, bosses) aren't pulled. A pull is a forced move, built on the existing push effect.
2. **Reactions.** Family Roles react to the pull as they react to a push (see 4.7 for Watch).
3. **Hit.** Each enemy on a touching cell takes **3 ×**. A large unit is hit if any of its cells touches.

An enemy 2 cells out on an arm is pulled in and hit in the same Whirl. Because the Whirl comes after the enemies act, the family starts its turn with them bunched on the cross.

### 4.4 Steer and Gust
While a Cyclone is out, Lucy's Cyclone button becomes **Steer**: 1 AP, once per turn.
- It moves up to 3 cells, four-way. It can't cross walls or enemies; it can cross the family.
- It must end on an empty cell with no planted entity.
- Then a **Gust**: the Pull step only, no hit, applied **once, at the destination**. Nothing is pulled along the path.
- The Steer preview shows the path, the landing cell, and a ghost for every enemy the Gust will move.

It never moves on its own and never picks a target.

### 4.5 Lifetime
3 enemy turns. It loses a pip at the start of each family turn and at no other time; the pips show on the Cyclone. Cast in round 1, it Whirls at the end of enemy turns 1, 2 and 3 and fades as round 4 starts; cooldown 4 leaves one round without a Cyclone.

### 4.6 What it stops

| | Rule |
| --- | --- |
| Enemy bodies | Can't enter or path through it. A push or a Command walk into it stops on the cell before it, as a push into rock does (CR-18) |
| Family, allies, neutrals, decoys | Pass through, can't end a move in it (the rule for walking through an ally) |
| Enemy ranged attacks | Not allowed if the line from shooter to target crosses its cell. Checked on the grid (not by physics, since Archer arrows are lobbed), used by the AI's target check and shown in the threat preview |
| Family projectiles | Pass through. Linda's straight arrows split (Tempest Bloom) |
| Enemy attacks on the Cyclone | None: enemies can't target it |

### 4.7 Reactions
- **Linda's Watch reacts to pulls.** Watch fires when a unit ends a move in her row or column, in any phase (`triggerEvents` = OnUnitEndMoving, `activationPhase` = all, on `Unit_Linda.prefab`). Pushes already raise that event (`AEffectPusher`), so a pull built on the push effect feeds Watch with no new hook. Two moments come out of it:
  - **Lucy's turn:** Steer, the Gust drags an enemy into Linda's lane, Watch fires. Setup and payoff inside one family turn.
  - **End of the enemy turn:** pull, then Watch, then hit. A Watch arrow that crosses the Cyclone with Tempest Bloom unlocked splits down the arms into the enemies just pulled there.
  Watch's own limits (shots a round, the quiver) cap it.
- **Other Roles** react to a pull wherever they already react to a push. Command Shield Dash also listens to the same event: check that a pull doesn't count as a finished Command move.
- **Whirl damage is no one's action.** It doesn't trigger Lucy's follow-up, which answers other family members' actions (D-277).
- **Waking.** A pull or a hit wakes an Unaware enemy (EN-14). Cast 3 plus arms 2 reach 5 cells, beyond enemy sight (3): the Cyclone can wake a pack from far away.

## 5. Enemy behaviour

**The cross is dangerous ground, not forbidden ground.** For enemies, the cross cells carry an extra move cost (the hazard cost mechanism of CR-16):
- **Another route exists:** they take it.
- **Walking in reaches a target they can attack this turn:** they walk in and accept the Whirl.
- **Sealed off, nothing reachable** (a 1-tile corridor): they wait outside the arms, 3 or more cells away, instead of standing in the damage. Lucy then Steers forward, the Gust drags them in, the family cashes in. The seal still holds; the damage has to be earned.
- **Ranged enemies** move to a cell whose line doesn't cross the Cyclone.
- They never target the Cyclone.

Today's AI already treats the Cyclone's cell as unwalkable; the new part is the cost on the cross and the line-of-fire check. The AI regression test (already red) will change with this; its fix session should know.

## 6. How it reads

**Always on the board:** faint wind lines along the arms with inward arrows, "3 ×" on the four touching cells, pips on the Cyclone.

**Whirl** (the loudest second on the board):
1. **Swell:** the Cyclone grows about a third, spins faster, the wind sound rises; the camera eases toward it, as at the phase switch.
2. **Pull:** wind streaks run inward along the arms; pulled enemies slide one cell.
3. **Burst:** a gust ring on the touching cells, hit flashes and numbers; it shrinks back.

**Gust:** the inward streaks only, no swell, no burst, no numbers.

**Combat log:** its own lines, "Whirl: pulled 2, hit 3" and "Gust: pulled 1", which also ends today's unattributed Cyclone damage.

| | Whirl | Gust |
| --- | --- | --- |
| When | Cast; end of each enemy turn | After a Steer, on Lucy's turn |
| Does | Pull, then hit | Pull only |
| Looks like | Swell, streaks, burst ring, numbers | Streaks only |

## 7. Numbers (starting values, to tune in play)

| | Value |
| --- | --- |
| Cast | 1 AP, range 3, cooldown 4 |
| Lifetime | 3 enemy turns (one pip a round) |
| Arms / pull | 2 cells / 1 cell per Whirl or Gust |
| Hit | 3 × per Whirl; at most 4 Whirls a cast (cast + 3 enemy turns), so 12 × to an enemy that stays on the cross (today: 7 × per landing) |
| Steer | 1 AP, 3 cells, once a turn, Gust at the end, no hit |
| Cyclone Power | Hit ×1.2 / ×1.4 |
| Howling Gale | Every enemy a Whirl hits is Weak for 2 turns |
| Trailing Gale (new run upgrade, optional) | Steer also pulls enemies next to its path one cell toward the path |
| Second Cyclone (run upgrade, optional) | Two Cyclones at once (chunk 12) |

Lucy's base damage stat was not read, so these are relative values. Read it before tuning against Dark Claw (16 HP).

## 8. Combos and synergies

| Piece | Effect | Action |
| --- | --- | --- |
| **Tempest Bloom** | Better. Copies fly beyond the Cyclone and to both sides: down the arms, where the pull puts enemies. The Cyclone stays in Linda's lane | None to the trigger (collider + two-prefab whitelist). The split arrow lands on the cell before the Cyclone as today, since the family can't stop in it: **D-252 and LI-6 unchanged** |
| **Linda's Watch** | New combo (4.7): Gust or Whirl pulls feed Watch | Build the pull on `AEffectPusher`; play-check the end-of-turn beat length |
| Linda's basic and Marks-Sisters arrows | Pass through and split; unchanged | None |
| **Lucy's Role** | Whirl damage doesn't trigger it | State it in the GDD |
| **Sisters' Rivalry** | A Cyclone kill isn't a basic attack; a Whirl can still set up Linda's basic kill | None |
| **Explosive Crescendo, Chained Assault, Family Watchers, Shield Flare** | The bunch is there at the start of the family's turn | Show it in a chunk |
| **Shield Dash, Vault, Harmonic Slam, Command** | Push enemies onto an arm for the next Whirl; a push into the Cyclone stops before it | Wall rule in the GDD |
| **Command Shield Dash** | Listens to the same end-of-move event as Watch | Check a pull doesn't count as a Command move |
| **Catch & Return / "Mark catches Cyclone copies"** | Copies still can't be caught; a still Cyclone makes the suggestion easier | Keep as the open suggestion |
| **Papa's Shelter, Blink, decoys** | The family is never walled off | None |
| **Cyclone Power, Howling Gale** | Both move to the Whirl | Reword node and upgrade texts |
| **Hazards** | A pull is a forced move: pulling into spikes or beside a mushroom cap is a combo | Check hazard rules for forced moves (CR-18) |

## 9. Alternatives considered

- **B. Deterministic drifter:** moves 2 cells a round toward the nearest enemy by a fixed rule, with a ghost of its next cell. Kept self-movement, but the player watches instead of deciding, and it leaves Linda's lane.
- **C. Controllable unit** with Move and Explode: most agency, but needs a unit's AP, turn slot, HP, UI and onboarding. Worth it only if the Cyclone should become a second character.

## 10. Levels, tech, tests, onboarding

- **Level chunks 1, 12, 13, 24** use the old rules. Throats still seal; "drifts into them" becomes "pulls them in"; chunk 12's two Cyclones need the run upgrade. The chunks' "to check" row 2 (what it drifts toward) is answered here.
- **Core systems (needs THJ's OK, `tech/core-systems.md`):** per-faction blocking and "pass through, can't stop" touch grid walkability. Add a new option; don't change `disallowWalk`, which other blockers share. The cross move cost and the line-of-fire check touch the AI.
- **Other tech:** life counts only on the family's phase (drop the `turnStarted` countdown); remove target choice and random walk; cast and Steer refuse cells with a planted entity, so the slide-to-nearest fallback never happens; the pull reuses `AEffectPusher`; Domain reload is off, so any new static needs its reset hook. Check which Cyclone assets Lucy's prefab uses: a second copy sits under `Resources/UnitSpecific/Player/Linda/Abilities/Cyclone/` and `Features/Player/Linda/Prefabs/`. The ability asset's `radiusV` reads 4 while the GDD says cast range 3.
- **Edit-mode tests:** life counts once a round; Whirl order (pull, reactions, hit); pull order and blocking; per-faction walk rules; Steer refuses planted cells; line-of-fire rule.
- **Play-checks:** the Whirl beat and its length with Watch; AI waiting outside the cross; Archers repositioning; pulls into hazards; Command Shield Dash not firing on pulls.
- **Onboarding** (`thj/onboarding` unlocks the Cyclone after the interruption): the one-line rule fits the unlock hint.

## 11. Still to decide

1. Numbers in section 7.
2. Ship Trailing Gale and Second Cyclone as run upgrades, or not.
3. Q21's wording ("damage at the start of its turn"): confirm it was a complaint about today, not a request, since version 2 hits at the end of the enemy turn.

## 12. Build order (once approved)

Don't ship the lifetime fix on its own: under the old rules it would give the hunting Cyclone 5 full rounds.

1. Anchored Cyclone: no self-movement, life once a round, cast refuses planted cells, the cross drawn, Whirl (pull + hit) with its beat and log lines.
2. Per-faction walking (enemies blocked; others pass, can't stop) and the AI's cross cost.
3. Steer and Gust, with the preview.
4. Line-of-fire rule for enemy ranged attacks.
5. Watch and pull checks, upgrade texts, GDD (`lucy.md`, `family-systems.md`, `combat-rules.md`), chunks 1, 12, 13, 24, then a play-check.
