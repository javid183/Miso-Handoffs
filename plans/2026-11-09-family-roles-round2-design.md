# Family Roles, round 2: armed on the hero's turn, fired for the family

Size: L    Tier: 3 (the rule of a main mechanic and a USP; core role handlers and settings for any prototype)    Assigned to: miso-game-designer
Branch: all. `main` since THJ merged `thj/onboarding` on 2026-11-09 (D-456). `thj/home-test` notes in [Branches](#branches).
Status: round 3 reconciled with critics (2026-11-10), waiting on THJ. Round 2 below is history

## Round 3 (THJ's feedback, 2026-11-10)

Status: reconciled with the three round-3 critics (2026-11-10). Round 2's content below ("Why" to "Gates") stays as history. Decision IDs: the kept-AP decisions were renumbered after round 2 was written: D-460 (run the test), D-461 (player-turn roles free in v1), D-462 (John one guard per kept AP), D-463 (the switch in Global Settings). D-464 is new.

### What THJ said, and what it changes

| THJ (2026-11-10, trimmed) | What it changes |
|---|---|
| **Keep (D-464):** "no role works if someone is alone. That was already the exception about Linda, and I failed to see it all along." | The stated principle of every role |
| **John (00:41):** the package "makes John the only exception who has to give up something as valuable as AP in his own round to arm his role"; "If his defence is boiled by Wrath, how does he gain Wrath? And why 3?" | Round 2's Shield-Up gate and Wrath break are dropped |
| **John (00:51):** "Wrath is not a good term then ... a protecting father will never attack when the life of his kids is at stake. It should be themed around stamina or a posture break rather than Wrath, and thus can't strengthen his attack. And about 3: it feels too easy to burn on small attacks and never breaks against bosses." | **Posture**: a damage-based endurance limit on his guard, separate from any attack reward. **Wrath goes** |
| **Lucy (00:41):** "as the youngest, she follows the attack of whoever she's adjacent to. Feels like a little sister." Why does only John reward her? What about far targets, a Dash away from her, before or after? | Edge rules defined |
| **Lucy (00:52):** "Limiting Lucy's range and being beside someone is double gating her role." | **One gate: beside.** Her 3-tile reach goes |
| **Linda:** the filter makes placement "important and complicated"; melee approaching family is "the same problem"; "we are breaking her role in the player turn ... What happens to 'Mark moves, Linda fires'?" | Rebuilt around cause and protection; honest about what that means on each turn |
| **Mark:** "I was hoping for exciting new ideas, and got none." | Four new roles; the Setter recommended, its direction locked |

### Three requirements, and where they pull

1. **No role works alone (D-464).** Every trigger needs another Bergson.
2. **A real decision on the family's turn.** It may belong to the sibling who sets the role up (Mark choosing where to Vault so Linda fires), not only to the role's hero. Both answers must be reasonable.
3. **The combo feeling.** One family member's action causes another's role, on either side's turn: "another member's action made enemies move and Linda fired", "Lucy fired after another member's attack".

| Pair | Tension | How round 3 settles it |
|---|---|---|
| 1 and 3 | None: a combo needs two family members | Every combo passes D-464 for free |
| 2 and 3 | A combo that fires whenever actions happen to line up is free: THJ's "just a click" | The decision is in the setup (who moves first, where the setter aims, where the family stands); the role is its payoff. Accidental line-ups stay free bonuses: accepted |
| 3 and free roles | Combos with no cost become free kills (systems critic: about 20 damage per enemy attack on the S8 formation) | Caps on Mark and Lucy and John's posture ship **with** free roles, not after ([Caps](#caps-free-roles-need-brakes)) |
| 1 and 2 (John) | His role always needs an ally; round 2 made him pay AP | His price is posture (what his body can take) and where he stands |

### Options compared (round 3, after the critics)

| | **A. As built** | **P2. Round 2** | **R3. Round 3 (recommended)** |
|---|---|---|---|
| John | Guards within 2, unlimited, Wrath | Shield Up gate, Wrath breaks at 3, swap | **Swaps anywhere; Posture 12 (18 with Shield Up) of guarded damage, refilled on his turn; Wrath removed; Blood Debt kept** |
| Linda | Any enemy ending in her lines | Ends next to another Bergson | **The family moved it into her lines, or it ends next to another Bergson** (on the family's turn this is the built rule) |
| Lucy | Any family hit within 3 of her | Beside her + within 3 of her | **Follows whoever is beside her where the attack starts; no reach; twice a round; Papa's Shelter John-only** |
| Mark | Counter for hits on others within 2 | As built | **The Setter: his counter knocks the attacker directly away from the family member it hit; once per enemy turn** |
| D-464 | Fails (Linda, Lucy) | Yes | **Yes** |
| Combo feeling | Strong, incidental | Weakened | **Kept on the family's turn; enemy-turn chains, bounded** |
| Brakes | FTP (1 per answer) | None (roles free) | **Posture, Mark 1 per enemy turn, Lucy 2 per round** (or roles keep 1 FTP: Q5) |

### John (round 3): Posture, not Wrath

**Rule.** *"When an enemy attacks a family member, John can switch places with them and take the hit, wherever they are. Each guard costs him Posture equal to the hit; when it's gone, he can't guard again until his turn."*

**Posture (THJ's direction; the values are the systems critic's, checked against the enemy assets).**

| Item | Value | Why |
|---|---|---|
| What drains it | The raw damage of each **guarded** hit: the number the threat preview shows, before John's ×0.5 | Readable ("it empties when he protects"; UX and creative). His own hits don't drain it, so it never "breaks by itself" (UX round-2 misread). Damage-based, so a scratch costs a sliver and a boss blow costs a lot (THJ) |
| Size | **12**, or **18** while Shield Up is on | At Standard: Claws (6) 2 guards, 3 braced; Early (4): 3 / 5; Tutorial (3): 4 / 6; the Queen's charge (10) and one more hit break it. Small hits barely dent it, boss hits break it |
| Refill | Full at the start of John's turn | One enemy turn's budget |
| The breaking guard | The hit that takes it to 0 or below is still guarded; then **his guard breaks**: no swaps until his turn. Nothing else (no damage penalty, nothing on his attack) | A father who can't hold any more, not a punished one |
| Shield Up | ×0.6 damage taken (as built) and **+6 Posture** (12 → 18) while it lasts; it no longer arms Wrath | "Brace before the enemy turn" is a reason to raise it, never a gate |

**Wrath and Blood Debt, plainly.**

- **Wrath is removed** (THJ: a guard can't strengthen his attack). `JohnPassiveAbility_Wrath` comes off John. Its stack class and badge (`WrathStacks`, `JohnWrathBadgeUI`) are reused as the Posture meter. What it took with it: at most +105% on one ability a turn, a balance gain in a game the playtests call too easy (systems critic). JO-1 is retired, and the "Wrath" name goes from the UI.
- **Blood Debt stays** (JO-2: John deals ×1.3 to the last enemy to hurt the family). It rewards *after* the danger, on John's turn, and isn't tied to guarding. It keeps the kill line Wrath used to give: Sword 8 × 1.3 = 10.4, plus Lucy's follow-up 6, makes 16.4 ≥ a 16-HP Claw.
  - **One fix:** on a guard it marks `inProgress[0]` (the oldest action in progress), while John's handler answers the action that triggered him. Mark the same action (`JohnPassiveAbility_BloodDebt.cs:85-87`, not core, S).
- **Revenge** (RV-1) is where anger already lives.
- **Onboarding.** Memory 3's lesson becomes Shield Up (brace) → guard → Blood Debt punish, and the River's ★ "Wrath Shield Dash" becomes "Shield Dash on the Blood Debt Claw". The levels plans need the text changed. The tuning needs a check (the River: 4 × 1.3 = 5.2 a Claw beside the path, against Wrath's up to 8.2).

**The decision.**

- **The press, honestly** (systems critic): without a limit, pressing is close to always right. An attacker that has struck has spent its turn (CR-6), so the child who lands on John's tile is rarely in danger, and every press turns a hit on a 15–20 HP child into half a hit on John's 32. Posture is what makes it a choice: on a turn with more hits than Posture, the player picks which ones John takes (S8's fork).
- **On John's turn:** brace (Shield Up, +6 Posture) or act; and where he stands, which is still where a child lands. That's a smaller cost than round 3's draft claimed, because spent attackers can't follow up.
- **"The swaps limit themselves" is withdrawn** as an argument. Posture is the limit.

**The decision prompt** (UX critic). John's prompt is the only one with a real "no", so it isn't a reflex.

- **Untimed while paused, two answers:** Swap, or Let it land. A "paused" prompt still runs its 1 s window on unscaled time (`QTEButton.cs`), so this needs the profile's duration or an untimed mode (data or small code, **to check**).
- **While it's up:**
  - a ghost of the child on John's tile and of John on the child's;
  - threat arcs (CR-39, re-meant) from the enemies yet to act to John's tile;
  - the camera framing both units (**to check**; otherwise an edge pointer);
  - a cost line, "Take it · Posture 12 → 6", or "Breaks his guard";
  - a hatched segment on the Posture bar.
- **The swap is staged as John running across** (creative), not a teleport; the tether (FR-13) draws the line.

**The web closes** (creative critic's strongest point). In the draft nothing could happen to John. With Posture, when his guard breaks, the roles that already exist become the children covering their father:

- Mark counters hits on John (John is "another family member" to him);
- Linda's protection clause fires on an enemy that ends next to John;
- Lucy beside John is Sheltered.

The break beat is John on one knee, a child's bark ("Papa!"), and the camera holding for a moment. Text "Guard broken" (placeholder, `miso-narrative`).

**Swap edge cases** (systems critic; the cost is now M to M+):
- **Area attacks** (the Queen's strike, the Masher's 2 × 2 slam): John swaps with the primary target only; anyone else in the area is still hit, John too if his new tile is inside.
- **Moving attacks** (the Queen's charge): the swap happens at the action's start (`OnActionStart`) and the charge keeps its destination cell (`keepCellTargets`), so it hits John on the child's old tile (**to check**).
- **Either side's turn:** the handler also answers on the family's turn (the Masher's counter); Posture covers it.

**Code:** M to M+, core (`JohnFactionRoleHandler.Activate` on `AEffectSwapper`; Posture read from the hit's pre-reduction value at the trigger, which `AbilityDamagePreview` computes, **to check**). John's zone and cover marker go; the tether stays.

### Linda (round 3): the family moved it, or it came for the family

**Rule.** *"Linda's Watch fires on an enemy that ends a move in her lines when the family moved it there, or when it ends next to another Bergson."* Alone, nothing fires it: an enemy ending next to Linda alone, or walking into her lines by itself, sets off nothing. Memory 1 stays silent and corridors aren't free kill zones (round 2's gains, kept).

**Honest about the cause clause** (systems critic). On the family's turn, every enemy that moves is moved by the family: pushes, Command, swaps. The one exception is the Masher's counter walk, which ends next to its target and is caught by protection. So **on the family's turn this is the built rule**, and that's the point: it is exactly "Mark moves, Linda fires", which THJ asked to protect.

- The as-built rule only broke D-464 **on the enemy's turn** (enemies walking up to Linda herself).
- So the rule changes nothing on the family's turn and narrows the enemy's. On the enemy's turn Watch fires on Mark's knockback (cause) and on enemies ending next to a sibling (protection).

**Does it still give a decision?**

| Option | Family's turn | Enemy turn | Decision | Verdict |
|---|---|---|---|---|
| **Both clauses (recommended)** | As built: anything the family moves into her lines | Mark's knockbacks + enemies ending next to a sibling | Family's turn: the **setter's** aim (where Mark Vaults, John's Dash path), then the quiver. Enemy turn: where Linda stands, so her lines cross her siblings' flanks | Real for the setter; Linda's own press is mostly yes |
| Cause only | As built | Mark's knockbacks only | The setter's aim | Linda nearly silent on the enemy's turn |
| Protection only | Only enemies ending next to a sibling: **"Mark moves, Linda fires" breaks again** (S5) | Same as both | Where she stands | Fails THJ's requirement 3 |

**The quiver carries the rest, partly.** With 3 arrows, each Watch is an arrow her own turn can't use. Pressing is usually right (a Watch is free in AP, her own shot costs 1 AP and the same arrow), so the quiver is a **brake**, not a decision. Her real decisions are where she stands on the enemy turn and the order of the family's turn (let Mark push first). The draft's "where her lines cross the setters' pushes" belongs to the setter, and the plan says so now.

**Fixes from the critics.**

- **Catch & Return doesn't trigger on Watch arrows.** In S5, Mark lands 2 tiles up her column; with the node bought, a Catch prompt would stop the Watch before it reaches the pushed enemy (systems and creative). One prompt fewer in every chain; the "Watch into Mark" catch of round 1 is lost, while the catch on her own shots stays. Code: a check in `ProjectileCatchAndReturn` (not core; whether the role's shot can be told apart from her bow shot is **to check**).
- **Arrows pass allies** (verified by the systems critic, `Projectile.cs:509-515`; the trigger ignores units in between). Her drawn lines run through allies, matching the arrow (CR-37). Stage the arrow over a sibling's head so it reads as aimed (creative).
- **Vault slides a blocked push sideways** (`AEffectPusher.cs:70-80`), so a Vault can put an enemy in her lines that the player didn't aim there. It's a free bonus, and it shows in the push preview (below).
- **Code: S.** The cause is the owner of the latest action in progress (`SessionLogs.ActionsInProgress`); no "last moved by" record is needed (systems critic).

**Two displays, one per clause** (UX critic; without them, cause-only is the readable fallback).

| Display | What it shows | Where it comes from |
|---|---|---|
| Protection | On End Turn hover and through the enemy turn: her lines dim, and the tiles in them next to a sibling bright | Round 2's hover, re-meant |
| Cause | In any push or Command preview, a landing tile in her lines gets her bow icon | FR-12's cover-marker pattern, re-meant |

- **Ghost reasons:** "Only Linda" and "Not by family".
- **Badge line:** *"In her lines: pushed by family, or next to family."* Her one word, for tooltip and barks: **the finisher** (creative).
- **Toba counts as family for the cause** (both creative and the draft): he fights beside them. THJ to confirm (Q2).

### Lucy (round 3): one gate

**Rule.** *"Lucy follows the attack of whoever is beside her."* Beside: a 4-way neighbour, judged **where the attack starts**. Her 3-tile reach is gone (THJ's single gate): her embers chase the target wherever it is, as her sheet says they do.

| Case | Fires? |
|---|---|
| John beside her swings his Sword | Yes |
| John Shield Dashes away from her side | Yes: the Dash starts beside her |
| John walks two tiles away to attack (CR-7's move-then-attack) | **No**: the attack starts away from her. The preview's arc vanishes the moment the approach leaves her side, which teaches the rule (UX) |
| A sibling walks up beside her, then attacks | Yes |
| Linda beside her shoots an enemy 6 tiles away | Yes (no reach) |
| Mark's counter or Linda's Watch on the enemy turn, from beside her | Yes |
| Her own attacks, the Linda–Lucy Duo | No (as built) |
| A wall between her and the target | Her embers lob: **no line-of-sight gate** (if the code has one, a "Blocked" ghost; **to check**) |

**Twice a round** (systems critic): without the reach, the safest formation (Lucy beside Linda at the back) follows every arrow for free: about 12 a turn against her own 1-AP embers of 7 to 13.

- Her follow-ups are capped at **2 per round** (from the family's turn to the next). FR-4 planned 3; the old balance model counted 2 reactions per hero per round.
- The creative critic's "once per sibling per turn" is the alternative (Q3). It's truer to "beside", but it needs a per-sibling display.
- When spent, the badge reads "Followed twice" and the ghost says so.

**Papa's Shelter stays John's** (systems and creative; the UX critic preferred Family Shelter, outvoted two to one).

- **Why:** Family Shelter would make every Lucy who can follow at all also Sheltered and a level up, so her position stops being a choice, and it flattens three relationships into one stat. Papa's Shelter is what makes "beside John, up front" compete with "beside Linda, at the back".
- **"Why does only John reward her?":** because he's her father, and that's what shelter means.
- **The sibling gifts** come later, as **Bond rewards** (creative): Family-tree nodes opened by a pair's Bond, as Bond Lite already does for Linda & Lucy (BO-4), one at a time over the campaign.
  - Linda's gift: "her ember rides her sister's arrow", hitting the next enemy along the arrow's line too.
  - Mark's gift: "beside Mark, she shares his barrier" (Shared Calm, moved here).

**Preview** (round 2's U1, adjusted): the arc and the "+6" are computed from the tile the attack starts on (the ghost or approach tile, FR-11's logic), drawn on single-target hover and the firing pick.

**Code: S.** The striker's start tile is recorded at action start, like the existing HP snapshot (`_hpAtActionStart`); `GetCellsInRange` changes (her role zone, FR-10/11). Not core: the cap counter.

### Mark (round 3): the Setter, direction locked

**Rule.** *"When an enemy hits a family member within 2 of Mark, he strikes it and knocks it off them."*

| Detail | Locked rule | Why |
|---|---|---|
| Direction | **Directly away from the family member it hit**: the line victim → attacker → landing | Readable from the board (UX); "knocks it off them" means that (creative). The setup becomes one sentence: *"stand in Linda's line, and whatever hits you along it gets knocked down it"* |
| Blocked | **Straight push only**: if the tile beyond is a wall, a gap, a unit or the Cyclone, no knockback (the strike still lands), with a "Blocked" ghost | Vault's push slides sideways; the Setter's must not, or it lands where nobody can predict (systems) |
| Where Mark lands | His Fist Blitz lands on a free neighbour of the attacker **other than the push tile** when one exists | Otherwise Mark coming from the far side blocks his own knockback (systems) |
| Immovable | The Masher and the Deev aren't moved (EN-3); the strike lands. The Queen's 1 × 2: **to check** | — |
| Once per enemy turn | FR-4's designed limit (D-042) | The free-kill brake ([Caps](#caps-free-roles-need-brakes)) |
| Telegraph | For about 0.4 s, a short arrow from the victim through the attacker to its landing, in Mark's colour (after the contrast fix), plus the push visual | A sideways-looking flight after a punch reads as a bug otherwise (UX) |

**What it can't do.** An enemy's attack ends its turn, so the knockback never saves anyone from *that* enemy. Its value is feeding Watch and setting up the family's turn (the Claw lands where Lucy's next embers or John's Dash can take it).

**Mark's decision.** Stand within 2 of the siblings likely to be hit, not behind the attacker. The family's decision is to line up behind the victim in Linda's line. The draft's "which side he stands on" is withdrawn: under the locked rule, Mark's side doesn't change the direction (systems).

**Not in v1, held as options (Q4).**

| Option | Rule | For it | Against it |
|---|---|---|---|
| **The throw** (creative) | The player picks the landing among the tiles not closer to the victim, on a paused prompt with "away from the victim" pre-selected | Gives Mark his own moment and a live decision on the enemy turn | A new pick interaction on the enemy turn; slows it |
| **The arrow catch** (creative, the "new idea") | When an enemy arrow is aimed at a sibling within 2 of Mark, he catches it and returns it along its line | The most "tell a friend" image any Mark option has had | A second clause; `ProjectileCatchAndReturn` pointed at enemy projectiles (**to check**) |
| **Tag-in** (systems' fallback) | Mark follows a sibling's kill on the family's turn | Easiest to read; no enemy-turn chain risk | — |
| Shared Calm | — | — | Moved to Lucy's Bond gift |
| The Call | — | — | Dropped |

Code: S–M with **two core changes**: the push direction measured from a reference unit (`AEffectPusher` measures "away" only from the owner today; `TryGetPushPreview` has an override, `ApplyUnguarded` doesn't), and the landing choice in `AEffectDashAttack`.

### Caps: free roles need brakes

The systems critic's point 4. With roles free, one enemy hit on the S8 formation sets off up to ~20 damage (Mark 8+, Watch 6, Lucy 6), so a Claw dies on its own turn, and the AI doesn't avoid formations. On paper, a Masher can loop: its counter hits a sibling, John swaps, Mark counters John's attacker, the counter provokes the Masher, and so on, to a hidden cap of 10 per root action (`MasherChainCap.Max`). As built, FTP was the brake.

| Brake | Value | What it stops |
|---|---|---|
| John's Posture | 12 / 18 a turn | Unlimited swaps; the Masher loop (the third 8-damage counter breaks 18) |
| Mark | Once per enemy turn | More than one chain per enemy turn |
| Lucy | Twice per round | Free follow-ups from the back line |
| Linda | Her quiver (3), as built | Already a brake |
| Masher | His counter no longer provokes roles: `counterCanProvokeFamilyRoles` 0 on `Unit_MasherGoblin.prefab`, or John's handler checks `FactionRoleProvocationSuppression` like the others | The loop at its root (data or S) |

**The alternative brake is the built one** (Q5): roles keep 1 FTP. No new caps; one brake for all four; Pass-by keeps its payoff and FTP keeps a job. Against it: "running out of FTP flattens combat" (playtests), and roles then compete with Duos for the same points. I recommend the caps, because each one is a sentence on its hero's badge and none drains the Duo meter.

**FTP with free roles** (round 2's Q6, still open): Duo cost 3 (DU-5) if FTP ends most fights above 4; Pass-by's payoff decided from the session log.

### Readability (round 3 additions to round 2's pieces)

Round 2's pieces stand: the contrast fix first, the armed badge with reasons, the End Turn hover, the "would have fired" ghost, Lucy's arc and "+6", the swap beat. Added by the UX critic:

| Piece | What | New or re-meant |
|---|---|---|
| Tether and cause words on **every** role prompt | An arc from the role's hero to its target, and one to two words under the portrait: "Mark moved it", "Next to Lucy", "Linda beside her", "Off Lucy" | Re-meant (FR-13's tether), plus text |
| John's decision prompt | Untimed; child ghost, arcs to John's tile, cost line | Re-meant pieces |
| The Posture bar | A thin bar under John's mini HP bar (CR-49), pale bone or gold (not green, not his dark brown); the panel's Wrath box becomes "Posture 12/18" | **New** (necessary: the cost has to read on the enemy turn) |
| Linda's two displays | Protection tiles on hover; the bow marker on push landings | Re-meant |
| Mark's push telegraph | Victim → attacker → landing arrow, 0.4 s | **New, small** |
| Gaps between chained prompts | At least 0.3 s; the push and the arrow finish first | Timing |
| Ghost reasons | "Guard broken", "Only Linda", "Not by family", "Followed twice", "Nobody beside", "Blocked" | Text |
| Badge states | John: "Guard broken"; Linda: "Empty quiver"; Lucy: "Followed twice" / "Nobody beside"; Mark: "Countered this turn" | Re-meant |

Deferred: the chain count ("×2", "×3"), only if the cold player doesn't notice chaining.

### Complexity (round 3, recounted the UX way: replacements aren't removals)

| Hero | Player learns (+) | Goes away (−) |
|---|---|---|
| John | Swaps anywhere (1); a guard costs Posture equal to the hit, and when it's gone no guards until his turn (2) | "Within 2" (1); Wrath: a stack per hit, the cap, the bonus (3) |
| Linda | Pushed by family (1); next to family (1) | — (her as-built rule is replaced) |
| Lucy | Beside her where the attack starts (1); twice a round (1) | — (her reach is replaced) |
| Mark | Knocks it off them (1); once per enemy turn (1) | — |
| All | — | Roles spend FTP (1) |
| **Total** | **+9** | **−5** |

That's against the UX critic's +6 −3 for THJ's changes alone; the extra three are the caps, the price of free roles. On screen: +2 new (the Posture bar, Mark's telegraph) on top of round 2's three; the rest is re-meant; removed: John's zone and cover marker, the NoFtp state.

**Cut or deferred to stay there:**
- Mark's throw and arrow catch (options, not v1);
- the sibling gifts (Bond, later);
- Family Shelter (dropped);
- the chain count;
- the Catch on Watch arrows (removed);
- Tag-in and the Call.

If THJ takes the FTP brake instead of the caps (Q5), it's +7 −4.

### Paper scenarios (round 3, after the critics)

Same frames and assumptions as round 2 (prefab reads of 2026-11-09; Claws hit 4-way neighbours; shortest paths; order stated). Raw enemy hits (systems critic, from the assets): Claw 6 at Standard, 4 at Early, 3 at Tutorial. Claw HP: Tutorial 10, Early 16. Catch & Return isn't bought before the Family tree opens (after the Yard).

#### S5. The Ridge, turn 1: Mark vaults, Linda fires, as built (grid `rr3-s5-setter`, unchanged)

```grid id=rr3-s5-setter title="S5 The Ridge, round 3: Mark vaults, the push puts 2,4 up Linda's column (GB_s2-ridge)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,2 2,4 2,5 linda her column
arrow 3,1 2,3 mark Vault (3)
arrow 2,4 2,5 mark dx=8 pushed
arrow 2,1 2,5 linda dx=-10 Watch, then her shot
step 2,3 1
step 2,5 2
note 2,3 Mark lands
```


| Line | Family's turn | Enemy turn | Grade |
|---|---|---|---|
| **Vault to 2,3** | Mark Vaults 3,1 → 2,3 (3). 2,4 takes 2 (10 → 8) and is pushed straight north to 2,5 (free, so no slide): moved by the family, in her column: **Watch** (8 → 2; quiver 2). Her own shot finishes it (quiver 1). The Watch arrow passes Mark on 2,3: no Catch (Catch & Return isn't bought yet, and under round 3 it never triggers on Watch) | 1,5 and 3,5 go for Mark. One ending on 2,4 or 2,2 is next to Mark in her column: **Watch** (protection), if an arrow is left | ★ |
| Vault to 3,4 | 2,4 pushed west to 1,4, out of her lines; 3,5 north to 3,6: no Watch | The rush strikes Mark | ● |
| **Honest grading** | On the family's turn this Watch is the **built** rule (any family push into her lines). The decision is the **setter's** (where Mark lands sends 2,4 into her column or out of it), then the quiver (Watch now, or keep the arrow) | | |
| **Count** | 1 setter decision, 1 combo prompt (Linda's own press: yes), 0–1 on the enemy turn | | |

#### S6. Memory 3: Posture at Tutorial (John 1 AP, sisters 0 AP), as built

```grid id=rr3-s6-john title="S6 Memory 3, round 3: John swaps twice, Posture holds (GB_m3-john)"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
arrow 4,4 4,3 4,2 enemy first: John
arrow 6,5 6,4 6,3 6,2 enemy on Lucy: swap 1
arrow 4,1 6,1 john dy=-6 swap 1
arrow 6,1 4,1 lucy dy=6
arrow 7,4 7,3 7,2 7,1 enemy re-plans: John
arrow 2,5 2,4 2,3 2,2 enemy on Linda: swap 2
arrow 6,1 2,1 john dy=-14 swap 2
arrow 2,1 6,1 linda dy=14
arrow 1,4 1,3 1,2 1,1 enemy re-plans: John
step 6,2 1
step 2,2 2
note 4,1 Shield Up
```

| | Round 3 (Posture 18 with Shield Up; Tutorial raw hit 3) | |
|---|---|---|
| Family's turn | John's one AP: Shield Up (hinted): ×0.6 and Posture 12 → 18 | 1 decision, hinted |
| Enemy turn (order: (4,4), (6,5), (7,4), (2,5), (1,4)) | (4,4) → 4,2 strikes John: his own hit, no Posture cost. (6,5) → 6,2 on Lucy: **prompt 1**, press: swap (4,1 ↔ 6,1), John takes 3 × 0.5 × 0.6 ≈ 0.9; Posture 18 → 15. (7,4) re-plans and strikes John on 6,1 (own hit). (2,5) → 2,2 on Linda: **prompt 2**, press (the systems critic is right: the Claws beside 6,1 have both struck, so Linda lands safely): swap (6,1 ↔ 2,1); Posture 15 → 12. (1,4) re-plans: John on 2,1 is 3 steps away, so it strikes him from 1,1 (own hit) | |
| Result | Sisters 0 damage. John ≈ 2 guards × 0.9 + 3 own hits × 1.8 ≈ 7 of 32. Blood Debt: on (2,5)'s Claw (the action John answered last, with the Blood Debt fix). Linda starts turn 2 between two spent Claws, and Harmonic Slam cripples both before she steps away | |
| **Honest grading** | At Tutorial, Posture never comes close to breaking, so **both presses are simply right**. Memory 3 teaches the swap; the Posture decision belongs to harder fights (S8). The draft's "2 real presses" was wrong | |
| **Count** | 2 prompts (today 6), 0 real press choices, all John's. Only John's role fires (no family-moved enemy, no enemy next to a sibling in Linda's lines, nothing for Lucy to follow) | |

#### S7. The River: Lucy's edge rules (John + Lucy), on `rr2-s4-river`'s board

Board and positions as round 2's S4: John 4,3, Lucy 3,3 beside him; Claws 5,3, 6,4, 6,2.

| Case | Result |
|---|---|
| John's Sword on 5,3 (8 → 2) | Lucy follows (he was beside her): 6, dead. Papa's Shelter: her own embers are a level up |
| John Shield Dashes from beside her | She follows, on an enemy the Dash hurt, wherever it is (no reach) |
| John had walked from 1,3 to attack 6,4 via 5,4 | No follow-up: the attack started away from her. The preview arc disappears as the approach leaves her side |
| Lucy hangs back at 2,3 | Not beside him: no follow-up, no Shelter, safer |
| Two follow-ups already this round | No third: "Followed twice" |

#### S8. The family chain, with John as the fork

Tiles from `GB_m2-pile` (prefab coordinates). **Assumed mid-fight state:** Linda 1,2, Lucy 2,2 beside her, Mark 3,0, John 0,4; one awake Claw moved to 6,2. The Archer (8,5) and the Claw on 7,1 are as built. Early tier: Claw 16 HP, raw hit 4. John has no Shield Up (Posture 12).

```grid id=rr3-s8-chain title="S8 The family chain, round 3: John's swap is the fork (GB_m2-pile tiles, assumed mid-fight state)"
. . . . . . . _ _ _
. . . . . . . . a _
J . . . _ _ . . . .
. . . . _ _ . . . .
_ L U . . . c . . .
_ _ . . . . . c . _
_ _ _ M . . . . . _
--
arrow 6,2 5,2 4,2 3,2 enemy dy=-6 hits Lucy
arrow 0,4 2,2 john dx=-6 fork: swap?
arrow 3,0 3,1 mark dx=8 counter
arrow 3,2 4,2 mark dy=6 knocked off
arrow 1,2 4,2 linda dy=14 Watch
arrow 2,2 4,2 lucy dy=-14 follows Linda
step 2,2 1
step 3,1 2
step 4,2 3
```

**Why the Claw attacks from 3,2.** Lucy's free neighbours are 3,2, 2,3 and 2,1. From 6,2, only 3,2 is within its 4 steps: 2,3 and 2,1 are both 5 away. So on this board the chain's start is forced. In general it isn't, and the UX critic is right that the attack tile is the enemy's choice: from 2,1, Mark's knockback would point south into the gap at 2,0 and be blocked; from 2,3, Mark would be out of reach. The readable decision before End Turn is the formation, not the chain.

| Beat | **Fork A: press John's swap** | **Fork B: let it land** |
|---|---|---|
| 1. John's prompt (untimed): "Take it · Posture 12 → 8" | Swap: John on 2,2, Lucy on 0,4. John takes 4 × 0.5 = 2 | Lucy takes 4 (of 15) |
| 2. Mark (3,0; the attacker is 2 away), once this enemy turn | Counter: the victim is now John. Mark lands on 3,1 (not the push tile), strikes 8 (16 → 8), knocks it directly away from John: east to 4,2 | The same, away from Lucy: east to 4,2 |
| 3. Linda | The family moved it into her row: **Watch** 6 (8 → 2). The arrow passes John | **Watch** 6 (8 → 2), passing Lucy |
| 4. Lucy | She's on 0,4, not beside Linda: **no follow-up**. The Claw lives at 2 HP | Linda was beside her: **follow-up** 6: dead |
| Result | **Papa took it, and his children answered.** Lucy unhurt; John 2 damage and Posture 8; Claw at 2 HP on 4,2 for the family's turn | **The little sister lands the kill on the Claw that hit her.** Lucy −4; Claw dead; John's Posture 12 for the next attacker |

**Count:** 1 real press (John's: both answers reasonable), then 2–3 reflex prompts with cause words. The decisions on the family's turn were the formation (Lucy beside Linda in her row, Mark within 2, John's Posture kept). This is the moment: the player chooses between shielding her and trusting the others to punish.

The draft's last line ("if Mark stood north of the attacker the knockback would go south") is deleted: under the locked rule, the direction depends only on the victim and the attacker.

#### Round 3 totals (after the critics)

| | Today | Round 3 draft (as claimed) | **Round 3 (corrected)** |
|---|---|---|---|
| S5 | 1 incidental Watch | 1 setter decision, 1 prompt | **1 setter decision, 1 prompt (the built rule on this turn), 0–1 enemy-turn prompts** |
| S6 | 0 decisions, 6 prompts | 1 decision, 2 real presses | **1 hinted decision, 2 prompts, 0 real presses (Tutorial)** |
| S8 | 1–2 prompts | 3 chained prompts, 0 forks | **1 real press (John), 2–3 chained prompts, two outcomes** |

### Recommendation (round 3, after the critics)

**R3 as revised.** Every role is the family answering together (D-464), and roles are free with brakes.

| Hero | Rule | Decision | Combo it keeps | Brake |
|---|---|---|---|---|
| **John** | Swaps with the family member under attack, anywhere; each guard costs Posture equal to the raw hit (12, 18 braced, refilled on his turn); broken, no guards until his turn. Wrath removed, Blood Debt kept (fixed) | Which hits to take when the turn brings more than Posture; brace or act; where he stands | When he breaks, the children cover him; Blood Debt pays off on his turn | Posture |
| **Linda** | Watch on an enemy ending in her lines that the family moved there, or that ends next to a sibling; no Catch on Watch arrows | The setter's aim, then the order; on the enemy turn, where she stands | "Mark moves, Linda fires", on both turns | Quiver |
| **Lucy** | Follows whoever is beside her where the attack starts; no reach; Papa's Shelter John-only | Beside whom, at 15 HP | "Lucy fires after another's attack" | 2 per round |
| **Mark** | The Setter: strikes and knocks the attacker directly away from the family member it hit; straight push; lands off the push tile | Within 2 of the siblings who'll be hit; the family lines up behind the victim | Feeds Linda and Lucy on the enemy turn | 1 per enemy turn |

### The test (round 3)

**House-rule session (THJ, no code, one evening).**

- **Data, Tier 3 and reversible:**
  - `requiredFTP` 0 on the four role components;
  - Linda's and Lucy's QTE profile `duration` raised. `requiredTimeScale` doesn't buy time: the window runs on unscaled time (UX critic). Note that it changes the feel;
  - John's Wrath component off.

| Hero | House rule |
|---|---|
| John | As built (range 2, no swap), but keep his Posture on paper: subtract each guarded hit's raw damage from 12 (18 with Shield Up), and decline guards once it's gone, until his turn. This tests the budget, without the swap |
| Linda | Press Watch only when the family moved the enemy into her lines (on the family's turn: any push or Command) or it ended next to a sibling |
| Lucy | Press only when the striker was beside her where the attack started; at most twice a round |
| Mark | As built, but press only his first counter each enemy turn |

- **Levels:** the Ridge (and all-alert), the River, The Pile, one M4 or M6 fight.
- **Read-out:**
  - per hero: "did you know why it fired?" and "did you set it up, or not, on purpose?";
  - "did you feel a combo form, and on which turn?";
  - did John's Posture ever make you decline, and was that right?
- **Logs:** FTP at fight end, enemies killed on their own turn, prompts on the busiest enemy turn.

**Code, in order** (each behind its own Global Settings toggle, D-463; the cold player now comes after Linda's and Lucy's rules, UX critic):

| Order | Chunk | Size | Core |
|---|---|---|---|
| 0 | Contrast fix; Lucy's preview | S; S–M | Preview path (additive) |
| 1 | Readability: badge, hover, ghost, tether and cause words on every prompt; roles free; Mark's and Lucy's caps; the Masher counter flag | S–M | Each handler's ghost hook |
| 2 | Linda's cause and protection, her two displays, no Catch on Watch | S | `LindaFactionRoleHandler` |
| 3 | Lucy's one gate and cap | S | `LucyFactionRoleHandler` |
| 4 | John: the swap, Posture, the decision prompt, Wrath off, the Blood Debt fix | M to M+ | `JohnFactionRoleHandler`, `AEffectSwapper` |
| 5 | Mark: the Setter | S–M | `AEffectPusher` (reference unit), `AEffectDashAttack` (landing) |

**Cold player** after chunk 5, asked first (UX critic):
1. On John's prompt: "If you press, where does Lucy end up, and is that safe?"
2. After a chain: "Why did Linda shoot, and why did Lucy follow?"
3. On a fresh board: "Where would you put them to make that happen again?"

**Stop rule:** per hero (round 2); John and Mark are judged only after their chunks.

### Critics (round 3)

| Critic | Strongest point | What I did |
|---|---|---|
| **Systems** | John's free swap is close to dominant: attackers that struck are spent, so landing beside them is safe. S6's second prompt should be pressed. "The swaps limit themselves" doesn't hold. S6's Blood Debt line is wrong | **Accepted.** Posture with the critic's values (12 / 18 of raw guarded damage, refilled on his turn). S6 regraded (0 real presses at Tutorial). The self-limiting argument withdrawn. The Blood Debt line corrected, and the `inProgress[0]` fix added |
| Systems | Wrath goes, Blood Debt stays (it keeps the kill line) | **Accepted**, with THJ's 00:51 note: Wrath removed, its code reused for the Posture meter |
| Systems | On the family's turn, "cause" is the as-built rule; Vault slides; arrows pass allies; Catch stops S5's Watch | **Accepted and said plainly.** Catch no longer triggers on Watch arrows. The cause is read from the action in progress (S, no record) |
| Systems | The Setter needs a locked rule and two core changes; S8's last line is wrong | **Accepted:** directly away from the victim, a straight push, a landing off the push tile, two core changes named; the line deleted |
| Systems | Free roles plus the S8 formation give free kills, and a swap → counter → Masher loop runs to a hidden cap of 10. Caps must ship with free roles | **Accepted:** Posture, Mark 1 per enemy turn, Lucy 2 per round, the Masher counter flag, all in chunk 1 or 4. The FTP brake offered as the alternative (Q5) |
| Systems | Lucy without reach reaches 5–8 tiles: keep Papa's Shelter John-only and cap her at 2 | **Accepted** |
| Systems | Swap cost M to M+ (area and moving attacks) | **Accepted**, edge rules written |
| **Creative** | John sits outside the web: nothing can happen to him. Posture (drained by guarded damage, breaking with him on one knee, attack untouched) lets the children's roles cover their father | **Accepted** as the frame for Posture and its break beat. The size is the systems critic's (12, damage-based, raw) rather than ~8 actually taken, because the raw number is the one the threat preview shows. Wrath goes rather than staying under a new name, by THJ's 00:51 note |
| Creative | S8 is a Rube Goldberg chain of always-yes presses: give it forks | **Accepted:** John's swap is S8's fork (two outcomes, both reasonable). Mark's throw pick held as an option (Q4), not v1 |
| Creative | Mark: the Setter throws (the player picks), plus the arrow catch; cut Tag-in and the Call; Shared Calm → Lucy's gift | **Partly:** direction locked for v1 (UX: predictable formation); the throw pick and the arrow catch are options in Q4; the Call cut; Tag-in kept as the systems critic's fallback; Shared Calm moved to Lucy's Bond gift |
| Creative | Lucy: one gate, no reach; if too strong, once per sibling per turn; keep Papa's Shelter Papa's; gifts earned at Home | **Accepted**, except the cap form: 2 per round (systems; no per-sibling display), with "once per sibling" offered in Q3 |
| Creative | Linda: name her "the finisher"; Toba counts | **Accepted** |
| **UX** | S8's chain can't be predicted before End Turn (the enemy picks the attack tile). It reads as three unexplained presses | **Accepted:** the formation is sold as the decision, not the chain. The tether and cause words on every prompt, a "Blocked" ghost, gaps between prompts. S8 says why its start is forced on that board and not in general |
| UX | John's prompt runs 1 s even when paused: make it an untimed decision prompt with child ghosts and threat arcs. Posture as a bar with a cost line and a break moment, replacing Wrath only if Wrath goes | **Accepted** (Wrath goes) |
| UX | Linda's two clauses need two displays, or take cause-only | **Accepted:** both displays specified; cause-only is the fallback in Q2 |
| UX | Lucy: one gate; the arc from the attack's start tile; no silent line-of-sight gate. Family Shelter | **Accepted**, except Family Shelter (outvoted by systems and creative) |
| UX | The count is about +7 −2 (+6 −3 with THJ's changes) | **Recounted:** +9 −5 including the caps |
| UX | Move the cold player after Linda's and Lucy's rules; the session's `requiredTimeScale` buys no time | **Accepted:** the cold player after chunk 5 (Linda and Lucy are chunks 2–3); the session raises `duration` instead |

### Questions for THJ (round 3)

**Q1. John: Posture instead of Wrath?**
- Context: your 00:51 note. Posture is drained only by the hits he takes for others, by their raw damage (the number the preview shows): 12, or 18 while Shield Up is on, refilled at his turn. When it's gone, no guards until his turn; nothing touches his attack. Wrath is removed; Blood Debt stays (it keeps the Claw kill line with Lucy) and gets a small fix. The swap at any range stays; his prompt becomes an untimed Swap / Let it land, showing where the child lands.
- Options: (a) Posture 12 / 18 as above; (b) smaller, 8 / 12, so it bites in early levels too; (c) Posture plus Wrath kept as a separate reward (+2 rules).
- Recommendation: (a).
- Blocked: chunk 4; the house rule's Posture count; Memory 3's and the River's lesson text.

**Q2. Linda: both clauses (as built on the family's turn), or cause only?**
- Context: on the family's turn every enemy move is family-caused, so her rule there is the built one: "Mark moves, Linda fires" stays whole. On the enemy turn she fires on Mark's knockbacks and on enemies ending next to a sibling, never on one that comes only for her. Her own press is mostly yes; the decisions are the setter's aim and where she stands. Both clauses need two displays to read. Also: does Toba count as family for the cause? And Catch & Return stops triggering on Watch arrows (so it can't cancel a chain).
- Options: (a) both clauses, with both displays; (b) cause only; (c) protection only (breaks "Mark moves, Linda fires").
- Recommendation: (a), Toba counting.
- Blocked: chunk 2; the session's Linda rule.

**Q3. Lucy: one gate (beside), capped how?**
- Context: your 00:52 note: the reach is gone. She follows whoever is beside her where the attack starts, at any distance, which makes the back line beside Linda strong. Papa's Shelter stays John's ("because he's her father"); the sibling gifts come later as Bond rewards.
- Options: (a) twice a round; (b) once per sibling per round; (c) no cap.
- Recommendation: (a).
- Blocked: chunk 3.

**Q4. Mark: the Setter as locked, or with the player's throw, or the arrow catch?**
- Context: v1 knocks the attacker directly off the family member it hit, a straight push, once per enemy turn, so the family's formation decides the chain. The creative critic's two additions are the most exciting ideas so far: the player picks where Mark throws it (a paused pick on the enemy turn), and Mark catches enemy arrows aimed at a sibling and returns them.
- Options: (a) locked v1, add the throw or the catch after the session; (b) the throw in v1; (c) the arrow catch in v1; (d) Tag-in instead (on the family's turn, no enemy-turn chain).
- Recommendation: (a).
- Blocked: chunk 5.

**Q5. The brake: per-hero caps with free roles, or roles keep 1 FTP?**
- Context: free roles plus formations make free kills, and a Masher loop exists on paper. Caps (Posture, Mark 1 per enemy turn, Lucy 2 per round, the Masher's counter not provoking roles) are three sentences on badges and keep FTP for Duos. The built brake (1 FTP each) needs no new rule and keeps Pass-by's payoff, but running dry flattened combat in playtests.
- Options: (a) caps, roles free (Duo cost 3 as the lever if FTP piles up); (b) roles keep 1 FTP, no caps except Posture; (c) free and uncapped, watched in the logs.
- Recommendation: (a).
- Blocked: chunk 1; the session's data.

**Q6. The test as reordered?**
- Context: the session tests Linda, Lucy, Mark's cap and John's Posture budget by hand (data: role FTP 0, longer prompt windows for Linda and Lucy, Wrath off). The swap and the Setter need code. The cold player comes after all five chunks, asked first where the child lands.
- Options: (a) as listed; (b) build John's chunk first and play it alone; (c) skip the session, code all, then play.
- Recommendation: (a).
- Blocked: the session date; tech plans for chunks 0–3.

Grids in round 3, to render: `rr3-s6-john` (changed: both swaps pressed), `rr3-s8-chain` (changed: John added as the fork). `rr3-s5-setter` unchanged.

---

*Round 2 follows, as history (2026-11-09).*

## Why

Round 1 ([`2026-11-09-family-roles-rethink-design.md`](2026-11-09-family-roles-rethink-design.md)) recommended **C, kept AP**, and THJ approved its test (D-457 to D-460), then paused it before playing with an objection: *"What makes players keep their AP instead of using it? If there are enemies alive while shooting with Linda, why should I not spend it right away? ... For John it's a bit different: he's not ranged and might not reach. Does this not require extra AP? Is 2 enough?"* He made a counter-proposal per hero (John: Shield Up gate, stamina, swap at any range; Linda: facing lane, minimum range 2; Lucy: free with better feedback, or an ember pool; Mark: not covered) and asked for a designer and critics discussion before deciding anything. This plan is that discussion: my draft (P), three critics, and the revision (P2).

## Goal

Settle where kept AP stands, turn THJ's proposal into per-hero rules where each hero has a real decision, and recommend one set with a test that needs no code first, under a stop rule that can't kill an idea before it's played.

## Acceptance criteria

- [x] Round 1's scenarios rechecked against THJ's objection, with a plain verdict on C and its variants.
- [x] The per-hero principle compared with A and C.
- [x] Each hero: rules, values, interactions, failure cases, files and core status; THJ's items weighed.
- [x] A complexity count (recounted with the UX critic's numbers), and what to cut.
- [x] S1 and S2 redone, a Linda scenario and a John scenario added, decisions and prompts counted after the critics' corrections.
- [x] The test: what a house-rule session can and can't show, then code in order.
- [x] Critics reconciled; recommendation and at most six questions in the five-part format.

## Scope

In: the arming rule and trigger of each role, John's Wrath as a limit and his swap, Linda's trigger (family filter or facing), Lucy's preview and trigger, Mark's options, the readability the arms need, the FTP economy once roles are free, the test.
Out: role effects beyond what is listed, enemy AI, the Cyclone redesign, level rebuilds (flagged only), the graded QTE (named as the next experiment), the Fireside mapping (noted).

## Touches

Systems: Family Roles (core: `FactionRoleHandlerBase`, the four Bergson handlers, `FactionControllerBase`), settings (core: `GlobalSettingsSO`), `AEffectSwapper` (core, for the swap), John's Wrath and Blood Debt passives, role zones, role badge and the prompt UI (not core), the attack preview (UI plus the core preview path).
USPs: Family Roles (main), Synergies, Duos (FTP), Home (Fireside note).
Docs: [Docs to update](#docs-to-update-if-approved).

## Approach

Recheck round 1, state the principle, design each hero, take the three critics, revise, count the complexity, play it on paper, then a two-step test with a stop rule per hero.

Read for this plan (2026-11-09): round 1; the three critic notes (`2026-11-09-family-roles-round2-critic-creative.md`, `-systems.md`, `-ux.md`); `vision.md`; the GDD (`family-systems.md`, `combat-rules.md`, `enemies.md`, the four character sheets); `combat-balance.md`; `decisions.md` (D-036 to D-042, D-216, D-244, D-246, D-292 to D-295, D-322, D-323, D-350, D-393, D-457 to D-460); the after-Hearth plan; `tech/core-systems.md`; code: `FactionRoleHandlerBase.cs`, the four Bergson role handlers, `JohnPassiveAbility_Wrath.cs`, `JohnPassiveAbility_BloodDebt.cs`, `MarkPassiveAbility_AtmanFocus.cs`, the role components on the four `Unit_*.prefab` (`requiredFTP`, `requiredTimeScale`, `activationPhase`, `oncePerPhase`), `Mark_Ability_Walk.asset`, `John_Ability_Shield.asset`; prefabs `GB_s2-ridge`, `GB_m3-john`, `GB_s1-river` read back with `level_to_grid.py`.

---

## Problem and evidence

### Round 1 revisited: THJ is right

**Kept AP fails where it was supposed to work.** The decision C promised was "spend this AP now, or keep it for the role". That is only a decision when the kept answer is worth about as much as the action it replaces.

- **A kept answer is the same action, later and conditional.** Linda's Watch is her bow shot (6, an arrow; LI-11). Mark's counter is his Fist Blitz preset (8). Lucy's follow-up is about one ember attack. Shooting now hits the target you choose, for sure, and can kill it before it acts. So with a target in reach, **spending now is at least as good, almost always**.
- **Keeping only happens when it is free or when nothing else can do the job.** Nothing in reach: keeping costs nothing, so it isn't a decision. An answer no action can give: only John's guard (you can't prevent a hit on your own turn). Keeping that changes what the enemy does (zone denial): our AI has no role-zone input (`UtilityVariables.cs`), so it doesn't exist.
- **For a melee hero 2 AP is not enough.** A melee turn is move + attack; keeping one AP gives up the attack whenever he has to move.

| Round 1 scenario | Claimed | What holds | Verdict |
|---|---|---|---|
| S1 The Ridge, K1 (Linda keeps 1, Mark keeps 2) | A kill box | Linda's second shot kills 2,4 now, for sure. Mark's keep was free only if he couldn't reach; in fact he can move 3 and Blitz 2,4 (systems critic), so his keep was a mistake | Dominated |
| S1, K3 (Mark Blitzes, Linda keeps both) | Aggressive | Worse for Linda than two shots; the only real choice is Mark's, an ordinary turn | No role decision |
| S1, K2 (spend everything) | Costs HP | The line a good player takes; with C they see no roles | Honest default |
| S2 Memory 3 (Shield Up + keep 1) | The lesson | Real for John (no own-turn way to prevent a hit), but it needed John's turn-1 limit raised and its best part came from the guard being limited, not from AP | John's verb, not AP |
| S3 The River (John step + keep 1) | One choice | Real for John only, for the same reason | John only |

**C, as tested, doesn't survive.** Its one live part was John. Two variants go on the shelf: C1, a kept answer stronger than the action (a new number per role, still a lottery); C2, enemies reading kept zones (core AI, golden-master churn).

### The principle, revised

My draft's principle was *"each role is armed by a choice on the hero's own turn, made with something that hero already does."* The critics broke it from two sides:

- **Systems:** "made with something the hero already does" is exactly the problem. John casts Shield Up for its own value and Mark lands Blitzes because it's his basic attack, so the arm is a by-product: **readable, not decided**.
- **Creative:** every arm was about the hero's own stance (his shield, her facing, his Focus), so nothing depended on where the *other* Bergsons stood. That is overwatch with new art, and the family drops out of the setup. FR-1's fantasy is a role that "protects or supports the family".

Both point to the same fix. **Revised principle:**

> **A role is armed on its hero's own turn and fires for another Bergson. The arm is either an action that competes with attacking, or a position relative to the family, never what the hero would do anyway.**

Every rule below is checked against two questions: what is the hero's real decision on their own turn, where both answers are reasonable? And does the trigger need another family member?

---

## Options compared

| | **A. As built** (free per D-036) **+ Lucy preview** | **C. Kept AP** | **P. My draft** | **P2. Revised (recommended)** | **P+. THJ's full proposal** |
|---|---|---|---|---|---|
| The rule | As built | Roles answer only with kept AP | John: guard with shield up, Wrath breaks it; Linda: faced lane, last arrow; Lucy: as built + preview; Mark: counter spends Focus | **John:** guards while his shield is up, at any range, by switching places; three hits break the shield for a turn. **Linda:** Watch fires on an enemy that ends in her lines **next to another Bergson**. **Lucy:** follows up a Bergson **standing beside her**, shown in previews. **Mark:** as built | P + stamina replacing Wrath, minimum range 2, ember pool |
| Own-turn decision | None | Keep or spend (dominated) | Mostly by-products (systems critic) | John: strike or raise the shield; Linda and Lucy: where to stand relative to the family; Mark: dive or stay by the family (table [below](#the-real-decisions-after-the-critics)) | As P2, plus more resources |
| Press decision | Always yes | Always yes | John only at the breaking hit; Mark's always yes | **John, every press** (he leaves his post); the others always yes (honest) | Same |
| Family-shaped | Incidental | No | Solo stances | **Every trigger needs another Bergson** | Partly |
| New to learn | 0 | 1 | About 8 (UX recount) | About 5, −1 (count [below](#complexity-budget)) | About 12 |
| New on-screen elements | 0 | 0 | About 6 (UX recount) | 3 new, 4 re-meant, 3 removed | 6 or more |
| Implementation | Preview S–M | M, core | S per hero | Readability chunk S–M; John J1+J2 S–M; swap M (core); Linda and Lucy filters S each | Several M chunks, core targeting |
| Risk | THJ's "just a click" stays | Roles vanish | Tests legibility, judged on challenge | The swap's readability; Linda's filter too rare; FTP unbound | Scope; tuned levels break |
| USP | FR as is | FR − | FR + | **FR ++, Synergies +**, Duos + (with an FTP lever) | FR +, Synergies − |

---

## The real decisions, after the critics

The systems critic's test, answered per hero. "Both reasonable" means a player could defend either answer on that board; where there's no decision, it says so.

| Hero | Real decision on their own turn | When both answers are reasonable | Where there isn't one | The press |
|---|---|---|---|---|
| **John** | **Strike, or raise the shield.** When he has to move to reach, his 2 AP buy move + Sword *or* move + Shield Up, not both | Whenever no enemy is beside him at the start of his turn ([S4](#s4-the-river-clearing-turn-1-strike-or-guard), the River) | When an enemy is already beside him: Sword + Shield Up, both. Accepted: holding the line pays. After a break, the next turn is a strike turn (no shield), by rule | **Real every time with the swap:** pressing pulls him off his post and drops the ally on his tile; on the third hit it also costs next turn's shield |
| **Linda** | **Where to stand so her lines cross the tiles beside her siblings**, vs the best tile to shoot from now. The siblings decide too: stand in Linda's line or not | When the best firing tile and the covering tile differ ([S1](#s1-the-ridge-rush-pack-turn-1-linda--mark-as-built), [S3](#s3-the-ridge-with-the-pack-awake-who-does-linda-cover)) | When she is the target herself: her Watch can't fire then. Her own answers (Harmonic Slam, a step away) and John's and Mark's roles cover her. Accepted: it's "Family Watch" | Always yes. Accepted; the graded QTE (FR-2) is the next experiment for presses with no choice |
| **Lucy** | **Stand beside the striker** (her follow-up, Papa's Shelter beside John) at 15 HP, **or stay back** at ember range 3 | Most boards with melee strikers ([S4](#s4-the-river-clearing-turn-1-strike-or-guard)) | When the striker is out of her ember reach anyway | Always yes (as above) |
| **Mark** | **Dive to kill, or stay within 2 of where the siblings will be hit** (his counter is already for others and positional) | When enemies are spread ([S1](#s1-the-ridge-rush-pack-turn-1-linda--mark-as-built): forward or hold) | When enemies come to the family anyway: then the counter is incidental, as today | Always yes. My draft's Focus cost didn't fix this (systems critic) |

So after the changes, three heroes decide by **where the family stands relative to each other**, and John decides by **an action that competes with his attack** and by a press that costs him his post. That is family-shaped and decided. The honest gaps: three of four presses still have one right answer, and Mark stays closest to "incidental".

---

## Per hero (P2)

### John: the shield arms the guard, the guard reaches anyone, Wrath boils over

**Today (verified).** The handler relays any enemy action that targets a family member within 2 (radius held to 1–2), on any phase, unlimited, 1 FTP each; the hit moves to John at ×0.5. Wrath: Shield Up arms it until John's side starts its next turn; **every health loss** while armed, or through the role, adds a stack (max 3), including his own hits, Burn ticks and the Deev's pools (`OnHealthDecreased`); his next damaging ability spends them for +35% each (GDD JO-1; the asset's value; the code default is 0.15). Stacks persist until spent. **Blood Debt already marks the attacker of a guarded hit** (`JohnPassiveAbility_BloodDebt.OnFamilyRoleActivated`, verified), until another enemy hurts family. Shield Up: 1 AP, cooldown 1, ×0.6 damage taken, +1 FTP; its `activationTagQuery` is empty today. John's prompt pauses the game (`requiredTimeScale` 0); the others run in real time (1).

**Rules.**

- **J1. Shield-Up gate.** *"John guards the family while his shield is up."*
- **J2. Wrath boils over (revised).** *"Three hits under the shield fill his Wrath: he throws the shield aside, and can't raise it on his next turn."* Every hit counts, as Wrath does today. On the break, Shield Up ends at once (its ×0.6 too: the dread half), and Shield Up is blocked for John's next turn only. My draft's "can't raise it until he strikes" was free for a front-line John (Sword + Shield Up is his normal turn) and punished a guarding John with no one in reach (systems critic). The one-turn block costs both the same, and it makes declining at Wrath 2 mean "keep next turn's shield".
- **J3. The swap, at any range (in the test).** *"When he guards, John switches places with that family member and takes the hit."* No range: the father reaches the child in danger.

**Why J3 is now in the test, not deferred.** The creative critic: the swap is the heart of THJ's John, it's the only thing that gives *every* press a cost you can see (John leaves the chokepoint, the ally lands on his tile), and a stop rule that judges John without it can end the topic before it's played. The systems critic reached the same place from the other side: "J3 is the next thing to try" if John's press isn't a choice. Without J3 the press is a choice only at the breaking hit. **Accepted**, with the UX critic's readability risk handled as a staging problem (below), and its order in the code moved forward.

| J3 question | Answer |
|---|---|
| Pathing, line of sight | A teleport: no path, ignores walls and gaps (like Encore), on `AEffectSwapper` (core; raises `unitEndMoving` for both, D-322) |
| The attacker's hit | Single target: rewritten to John (today's `RetargetToJohn`). Cell and area attacks land where aimed, on whoever is there now, so the area relay record isn't needed. A charge keeps its destination (`keepCellTargets`) |
| One ally per guard | An area hit on two sisters: John stands in front of one. A father can only stand in front of one child at a time: a feature of the fiction, not a loss (creative critic) |
| Who it can't reach | Toba (another faction), decoys and protectees; John while Crippled or Stunned (**to check** in `AEffectSwapper`) |
| Side effects | The ally lands where John stood, maybe beside other enemies; the next enemy re-plans on the new board. Papa's Shelter forms or breaks. Arrow pickup on a swap: **to check** (LI-7). Linda's Watch: allies don't trigger it |
| Readability | The weakest point (UX critic). Staged: the tether (FR-13, already drawn at any length) shows who; the paused prompt carries a cost line (below); a short swap beat. John's zone and cover marker go (no range), one layer fewer |
| Cost | M, core (`JohnFactionRoleHandler.Activate` rebuilt on the swapper during an enemy action in progress; `GetCellsInRange`; presenters). The riskiest chunk, behind its own toggle |

**Staging the break (creative and UX critics).** My draft's "Shield broken" popup told the player John failed, and today's third stack pops "Max Wrath" in the gain colour, which under J2 is the moment the shield goes: a misread either way. One beat instead: John throws the shield aside with a bark (for `miso-narrative`, e.g. "Get away from them!"), text "Wrath boils over" (placeholder). Shield Up's greyed tooltip reads as a promise: "Wrath first, shield next turn". **The prompt carries the cost** (UX): "Guard Lucy · 1 hit left", and "Guard Lucy · the shield goes" on the breaking guard, so the press is an informed choice.

**Blood Debt (creative point 3): already built.** The guarded Claw already carries Blood Debt (verified), so a Wrath Shield Dash or Sword next turn lands ×1.3 on the Claw that went for the child, until an unguarded hit moves the mark. No change needed; worth one line in the Hearth.

**Levers.** Wrath max and per-stack are a **linked pair** (systems critic): 3 hits / +35% (start); 2 hits / +50% if John becomes a fortress. The block length (1 turn).

**Failure cases.** *John forgotten:* Shield Up never cast: the badge says "Shield down" (below). *Can't control the break:* hits aimed at John drain his guards: true, and in fiction (a father under attack can't cover the others); if it reads as unfair, count only guarded hits (a second counter, against D-295, so only as a lever). *Swap reads as a bug:* if a cold player can't say who swapped with whom after the enemy turn, fall back to range 2 without the swap (creative critic's own stop condition).

**Code.** J1 + J2: **S–M** (systems critic, accepted): the break removes Shield Up's damage-taken modifier in the middle of an enemy action, inside a health callback, which is the code path `JohnFactionRoleHandler` warns about (a shared `Stat_DR` context once caused a StackOverflow with Shield + role together); an area relay can cross the break, so the second hit lands without ×0.6; the block needs a new tag, set and cleared in code. EditMode tests for an area relay across the break. Files: `JohnFactionRoleHandler` (**core**), `JohnPassiveAbility_Wrath` (not core), `John_Ability_Shield.asset` (data). J3: M, core, its own tech plan.

### Linda: Family Watch watches the family

**Today (verified).** Watch fires when an enemy ends a move in her row or column within 4, all four half-lanes, spending an arrow and 1 FTP. FR-10 hides her zone because it equals her bow's reach.

**Rule (revised).** *"Linda's Watch fires on an enemy that ends its move in her lines next to another Bergson."* Next to: the four neighbouring tiles (CR-15). Another Bergson: John, Lucy or Mark (not Toba, not decoys, as John's tag query). Her bow is unchanged.

This is the creative critic's proposal, and it replaces my draft's facing lane. It is THJ's minimum-range intent (Watch shoots at what goes for someone else) moved from the bow to the trigger, which is a filter in `LindaFactionRoleHandler` with **no core targeting work and no preview churn**. What it does:

- **The decision becomes the family's positions.** Linda decides where her lines cross the tiles beside her siblings; her siblings decide whether to stand in her lines.
- **It answers the corridor problem** (systems point 6): on a 1-wide approach, enemies going for Linda end next to Linda only, so they don't set off Watch. Corridors stop being free kill zones.
- **It answers THJ's arrow complaint without a new rule:** Watch fires less, so she keeps arrows for her own turn. L2 (the last arrow) becomes a lever, not a rule (UX: it was an off-by-one rule; systems: its trade was thin).
- **Memory 1 gets no roles for free:** Linda is alone, so Watch can never fire. No per-level switch.
- **No new on-screen element:** her zone becomes the watched tiles (tiles in her lines beside a sibling), drawn with her existing bow icons. It no longer equals her bow reach, so FR-10 stops hiding it.
- **Cost:** she loses her self-defence Watch, so she is weaker up close. That is what THJ's minimum range wanted, and Harmonic Slam, John's guard and Mark's counter are her answers.

**THJ's facing lane** stays as the alternative (Q3), with the UX critic's fixes if chosen: the rule in one line, *"Linda faces the way she last shot, or the way you turn her"* (moves don't change it; a diagonal shot takes the longer axis, a tie keeps the old facing); the picker as a control on her HUD, not arrows on the board; her lane drawn on the family's turn even when she isn't selected; End Turn pulses her badge if her lane holds no enemy that could end in it. **Both together** (lane + family filter) is too narrow to fire.

**Minimum range 2 on the bow:** not recommended. No minimum-range concept exists in the code (core targeting work plus every preview, CR-37), it breaks Memory 1's throat and the Ridge's opening, and the family filter gets its intent without either.

**Interactions.** Tempest Bloom: the Cyclone drifts toward units, so it is often near the family, and the loved shot stays possible and stays a surprise. Catch & Return: a sibling in her line is also where Mark catches (if the node is bought). Pushes, Command moves and Toba's swap still count as moves (D-322), filtered the same way. With the quiver off (LI-14), the filter still limits her.

**Failure case.** Watch fires on under about 1 in 4 enemy turns with enemies awake and in range (the creative critic's own bar). Lever: "within 2 of another Bergson"; then the facing lane alone.

**Code: S.** `LindaFactionRoleHandler.PrepareTargets` and `GetCellsInRange` (the watched tiles; **core** handler); `RoleZonePresenter` draws them (not core).

### Lucy: beside the family, and shown before it happens

**Today (verified).** Her follow-up fires on any phase when a family member's action really lowered an enemy's HP within 3 of her: 2 embers × 3, preferring the aimed enemy (`LucyRoleTargetRanking`), skipping an enemy whose most recent attacker is Lucy. 1 FTP each, no cap.

**The systems critic's point 5 is right:** under my draft Lucy lost her only limit (FTP) while the other three lost uses; she'd fire on every qualifying family hit, both turns: the free reward THJ complained about, on the one role left free.

**U-R. Rule (revised).** *"Lucy follows up a Bergson standing beside her."* The creative critic's replacement for Kindle: armed by keeping her close to family, which a fragile 15-HP child pays for in danger, and which Papa's Shelter already rewards beside John. A filter in her handler; no mark on enemies; her reach to the enemy stays 3. "Beside her": where the striker stood **when its action started** (Mark's Blitz and John's Dash move him; whether the handler can read the start tile at action complete is **to check**). THJ said she can stay free: she stays free, with no counter or pool, just armed by position. Kindle (U3) is rejected: it made her role about herself and made her act first (creative critic).

**U1. Preview (all branches, any time), redesigned with the UX critic.** My draft put her zone glyph on the enemy's tile (reads as "Lucy's zone") and her damage on the target's panel (not open when her pick isn't the hovered target, which is the "random" case).

| When | Shown |
|---|---|
| Another Bergson's damaging ability is previewed on a single target, or on the firing pick of a multi-target one, and Lucy would follow up (the striker beside her, the hit lowers HP and doesn't kill, the enemy within 3 of her, her ranking picks it) | An arc from Lucy to her pick (the tether's look, in her colour); a ghost "+6" in her colour above the pick's **mini HP bar** (CR-49, always visible); on an open panel, her part as a hatched "if pressed" segment |
| Her embers would finish it | No tinted skull: the skull keeps meaning "this hit kills" (CR-46) |
| An enemy in her reach is skipped by the "hit last" rule | A small crossed ember on it, the first time it matters (or the rule goes; why it exists is **to check**) |

Enemy-turn follow-ups (after a Watch or a counter) stay unpreviewed: a surprise. **Code: S–M**, its own tech plan: a preview helper beside `LucyRoleTargetRanking` (not core), a hook in the attack preview path (`PlayerController` / `UnitThreatAnalysis`, **core**, additive), the arc and ghost number (UI).

**Ember pool (U2): rejected.** It reads as the quiver re-themed (THJ's words), adds a fourth counter, caps without choosing, its Focus ability arms the role by giving up an action (the kept-AP problem), and "Focus" is Mark's resource. All three critics agree.

### Mark: as built, honestly

**Today (verified).** Enemy phase only (`activationPhase` 4), after an enemy's action hits a family member other than Mark, if the attacker is within 2; a free Fist Blitz (8 + Focus), which also earns him +1 Focus.

**My draft's M2 (counter spends 1 Focus) is withdrawn.** The systems critic: one Focus is 1–3 HP of barrier against 8+ damage, and hits on Mark drain Focus anyway, so the press is always yes; and his Focus comes from Blitzes he lands anyway, so the arm is a by-product. The UX critic: a cost decision can't live in a 1 s real-time window. The house rule couldn't even simulate it (the counter earns Focus as built).

**Recommended: M1, as built.** Mark's role already passes the revised principle's family test (it fires only for hits on others) and is positional (the attacker within 2 of him). His decision is **dive or stay by the family** (S1). His press has one answer, said plainly. Levers if he still reads as free:

| Lever | Rule | Note |
|---|---|---|
| Designed limit | Once per enemy turn (D-042, never built) | Bounds him; no choice added |
| Focus bet | *"His counter spends all his Focus and adds it to the hit"* | A real bet (a big counter now vs barrier and damage later); needs his prompt paused: `requiredTimeScale` 0 on his role (data, verified field) and a cost line |
| Start Focus 1 | "He arrives centred" (creative) | Only matters with a Focus rule |

### Every role: no FTP, and what FTP is for then

Roles cost no FTP (D-036): `requiredFTP` 0 on the four role components (data). **The systems critic's point 4:** with no role sink, pools start full (River 8, Ridge 5), income keeps coming (Shield Up, Slam, Blink, Pass-by, level fills), Duo cooldowns bind before FTP, and Pass-by's only payoff (FTP) becomes a dead choice. Mark's Continuous Attack still costs FTP (MA-2; D-216's "free" isn't built), so "FTP is the Duo meter only" isn't true yet. That runs against THJ's "Duos as finishers". So:

- In the session, set `requiredFTP` 0 in data (not +99 FTP), and log FTP at fight end and Duos per fight.
- Lever DU-5 (Duo cost 3) comes into this plan, used if FTP ends most fights above 4.
- What Pass-by is for when FTP is never short is a question for THJ (Q6).

---

## Readability the arms need (UX critic)

The UX critic's strongest point: an arm only fixes "you never know what you did" if the player can see, **before End Turn**, which roles are armed, and **on the enemy turn**, why one didn't fire. Today: the role badge is a 14 px dot (Ready / NoFtp / EmptyQuiver, `RoleBadgeRules`), green for John with his shield down once FTP is gone; John's Wrath is "2/3" in a panel box, Mark's Focus is a number, there are no Focus pips; the role-zone glyphs are already the worst-read element on the board (B4 finding 1, `status.md`, 2026-10-21). Accepted, with three pieces on existing layers and one prerequisite:

| # | Piece | What | New or re-meant |
|---|---|---|---|
| 0 | **Contrast fix first** | B4 item 1: role-zone and cover glyphs readable on dark floors | Fixes an existing element. **A blocker for P2, not polish** |
| 1 | **Armed badge with a reason** | `GetRoleBadgeState` (already marks "switch here when roles stop costing FTP") reads the arm: Ready, "Shield down", "Wrath first, shield next turn", "No family beside" (Lucy), "Empty quiver". The tooltip is each hero's one line | Re-meant |
| 2 | **Hovering End Turn shows the armed roles** | The Shift layer (FR-9) limited to armed roles: John's guard targets if his shield is up, Linda's watched tiles, Mark's radius. The same drawing stays up through the enemy turn | Re-meant (an existing layer, a new moment) |
| 3 | **"Would have fired" ghost** | When a trigger happens but its arm is off, the role glyph shows greyed and crossed for about 0.6 s over the unit that would have acted, with two words ("Shield down", "No family beside", "Not next to family"). Each handler evaluates its trigger before its gate, so it's a few lines per handler | **New, necessary**: it teaches the arms without a tutorial, and silence teaches nothing |

Deferred (each listed in [what to cut](#complexity-budget)): the badge row beside End Turn (the hover covers it), threat arcs on John's paused prompt, world-space shield segments on John (the prompt's cost line carries the decision), Focus pips under Mark (Mark has no Focus rule now).

---

## Lens notes (P2)

### Creative

**Target experience.** The family covers each other, and you arrange that: you keep Lucy beside her father so her fire follows his sword, you stand Mark where Linda's arrows cross, and when a Claw goes for the youngest, John comes across the room. Every role on the enemy's turn is someone answering *for* someone.

**The moment designed for:** the enemy turn where John holds the corridor on two Wrath and a Claw lunges at Lucy, three tiles behind. Press, and he leaves the corridor, takes the hit, and throws his shield aside ("Get away from them!"); next turn he strikes the Claw that went for her (Blood Debt). Or let Lucy take it and keep the door.

**Original?** Shield gates and overwatch are known; a role that only fires when the family stands in a certain relation to each other is not. That's the USP made into the setup.

**Creative vs systems, where they disagree:** creative wants the graded QTE on presses with no choice now; systems wants one variable per test. I keep the graded QTE as the next experiment (FR-2's plan), not in this test.

### Systems

**The rules (P2).** (1) Roles cost no FTP. (2) John guards only while his shield is up. (3) Three hits under the shield fill Wrath; the shield goes and is blocked for his next turn. (4) His guard switches places with the ally, at any range. (5) Watch fires only on an enemy that ends in Linda's lines next to another Bergson. (6) Lucy follows up only a Bergson standing beside her. (7) Mark as built.

**Levers and starting values.**

| Lever | Start | Range | Where |
|---|---|---|---|
| Hits before the break / Wrath per stack (linked) | 3 / +35% | 2 / +50% | Wrath passive (data) |
| Shield block after the break | 1 turn | 0–1 | Rule |
| Guard range | Any (swap) | 2 without the swap (fallback) | Handler |
| Linda's "next to" | 1 tile | 2 | Handler |
| Linda's last arrow (L2) | Off | On, if she still runs dry | Quiver rule (data on LI-5) |
| Lucy's "beside" | 1 tile | — | Handler |
| Lucy's cap | None | 3 a round (FR-4) | If her share stays high |
| Mark | As built | Once per enemy turn; Focus bet with a paused prompt | Handler, data |
| Duo cost | 2 FTP | 3 (DU-5) | If FTP ends fights above 4 |

**Interactions.** Shield Up stays the family's defensive hub (guard, Wrath, Shield Flare, and Command Shield Dash after a Command). With the swap, Papa's Shelter can form or break on the enemy turn. Linda's filter and Lucy's beside rule both reward a tight family, which Pass-by also rewards (if Pass-by keeps a payoff, Q6). Masher counters (EN-2) on the player's turn are guarded only if Shield Up is on that turn. A declined guard still silences that target for the turn (as built).

**Failure cases.** *Linda too rare* (under 1 in 4): widen "next to", then the facing alternative. *Lucy too rare*: if follow-ups drop under about one a fight, widen to "within 2", or drop the filter and cap at 3. *Lucy still too strong*: her share of family damage above about a fifth: the cap. *Tight-family dominant*: everyone hugs; enemy area attacks (the Masher slam) are the natural answer, so watch whether hugging is ever wrong. *FTP always full*: DU-5. *John fortress*: the linked lever.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Family's turn | Armed badges with reasons; Linda's watched tiles; the Lucy arc and "+6" on other heroes' attack previews | As now | "Lucy's follow-up is certain": the hatched "if pressed" segment, no skull |
| Hover End Turn | Armed roles only, on the board | End Turn | "Mark's radius is a danger zone": it's in his role colour and quadrant |
| Enemy turn, armed role fires | The prompt; John's with a cost line and the tether to the ally at any range | The key | After a swap, "where did everyone go?": the tether and the swap beat |
| Enemy turn, unarmed role | The ghost with two words | — | None: that's what the ghost is for |
| John's break | "Wrath boils over" beat and bark; Shield Up greyed "Wrath first, shield next turn" | — | Reading Wrath full as good news only: the cost line warned on the breaking guard |

---

## USP check

- **Family Roles:** strengthened, and made family-shaped: every trigger needs another Bergson, every arm is a choice on the hero's turn.
- **Synergies:** strengthened. A tight family arms Linda and Lucy and meets Papa's Shelter, Shield Flare and Catch & Return on the way; the preview shows Lucy's combo before you commit.
- **Duos:** FTP freed from roles; it needs a lever (DU-5) to keep Duos as finishers.
- **Managing the Home as a Family:** neutral on purpose. `thj/home-test`'s Fireside "first Family Role free" means nothing once roles are free; remap on merge (e.g. John starts the sortie with his shield up).

---

## Critics

All three read the draft P independently. Their strongest points and what I did:

| Critic | Strongest point | What I did |
|---|---|---|
| **Systems** | P makes roles readable, not decided: John's Shield Up and Mark's Focus come from what they do anyway; Mark's press is always yes; John's S2 press moves damage without reducing it (and my line saved the guard for the wrong sister) | **Accepted.** Rewrote the principle (an arm must compete with attacking or be a position relative to family). Withdrew M2. Added S4, where John's Shield Up competes with move + Sword. Regraded S1 and S2 (Mark can move and Blitz 2,4; S2's press is small in HP). Added the [real decisions table](#the-real-decisions-after-the-critics), with the gaps stated |
| Systems, point 1 | J2's "strike first" is free at the front and punishing at the back; Wrath counts every hit; Wrath max and per-stack are linked; J2 costs S–M | **Accepted:** the break now blocks the next turn's shield; levers linked; cost raised; area-relay-across-the-break test named. Counting only guarded hits kept as a lever (a second counter) |
| Systems, point 4 | No role sink: FTP always full, Pass-by dead; +99 FTP hides it | **Accepted:** `requiredFTP` 0 in data for the session, FTP logged, DU-5 in the levers, Pass-by to THJ (Q6) |
| Systems, point 5 | Lucy gets stronger while the others get weaker | **Accepted:** her beside rule bounds her; cap 3 as a lever; her damage share read in the log |
| Systems, point 6 | Linda's default facing is already right on one-front boards; corridors become free kill zones; Crescendo has no direction | **Accepted** by changing Linda's rule: the family filter doesn't fire on enemies going for her, so corridors aren't kill zones, and there's no default to get wrong. The facing fixes are kept for the alternative |
| Systems, scenario errors | S1: Mark can Blitz 2,4; S2: Wrath 1 already kills on turn 2; S3: a Claw striking diagonally; S1's Watch depends on enemy order | **Fixed:** S1 redone with Mark's Blitz; S2's turn 2 says the extra Wrath pays only on Shield Dash and through Blood Debt; S3's paths written out tile by tile (every strike from a 4-way neighbour); every Watch states its order and tie-break assumption |
| **Creative** | Every gate was the hero's own stance: overwatch with new art; P cut THJ's two family ideas (the swap, Watch for others) | **Accepted as the new principle.** Swap in the test; Linda's family filter replaces the facing lane (no core work, Memory 1 silent for free); Lucy's beside rule replaces Kindle |
| Creative, point 1 | Don't let the stop rule judge John without the swap | **Accepted:** the stop rule is now per hero, and John isn't judged until J3 has been played. Dropped "any range without the swap" from the questions |
| Creative, point 3 | Stage J2 as Wrath boiling over; Blood Debt on the Claw that went for Lucy | **Accepted** the staging; Blood Debt **already does this** (verified in code), so no change |
| Creative, point 4 | Mark starts at Focus 1 | **Moot** with M2 withdrawn; kept as a lever with the Focus bet |
| Creative, point 6 | Graded QTE for presses with no choice | **Deferred** to the next experiment: one variable per test. Added the session question "did you tell anyone about a role?" |
| **UX** | You can't see which roles are armed before End Turn, or why one didn't fire; the badge stays green; the glyphs are already the worst-read element | **Accepted:** contrast fix as a prerequisite; badge re-meant with reasons; End Turn hover shows armed roles; the "would have fired" ghost |
| UX, point 1 | "Max Wrath" in the gain colour is a misread; the guard choice is made blind | **Accepted:** one "Wrath boils over" beat; a cost line on John's prompt. Threat arcs on the prompt and shield segments deferred (budget) |
| UX, point 2 | Linda's picker on the board misclicks; the default can't be recited | **Moot** for the recommendation (no picker); fixes kept for the facing alternative |
| UX, point 4 | Mark's 1 s prompt can't carry a cost decision | **Accepted:** M2 withdrawn; the Focus bet lever needs a paused prompt (data) |
| UX, point 5 | Lucy's preview as drafted fails in the "random" case | **Accepted** the redesign: an arc, a ghost "+6" over the mini HP bar, a hatched segment, no tinted skull, a crossed ember for the skip rule |
| UX, point 6 | P adds about 8 rules and 6 elements, not 4.5 and 1 | **Accepted** the recount; P2 recounted [below](#complexity-budget) |
| UX, the test | THJ can't test readability: he knows the rules. A cold player is needed | **Accepted:** the session now tests decisions only; readability goes to a cold player after the readability chunk |

**Rejected or not taken:** the creative critic's "both lane and filter" option (too narrow; it's one or the other, Q3); the UX critic's badge row beside End Turn (the hover covers it, within budget); the systems critic's "Focus cost 2" for Mark (still always yes).

---

## Complexity budget

THJ: "too many mechanics, too little challenge"; D-295: one sentence per feature, at most one new element unless necessary, more than one new thing to track goes to THJ as a question.

**Recount, read as a player (the UX critic's method).**

| | P (draft), UX recount | **P2** |
|---|---|---|
| Rules added | About 8: John 3 (gate, three hits, his own hits count), Linda 3 (one lane, the default, last arrow), Mark 2 (spends Focus, earns none) | **5:** John 3 (*guards while his shield is up*; *three hits throw the shield aside for a turn*; *he switches places*), Linda 1 (*watches for enemies next to family*), Lucy 1 (*follows a Bergson beside her*). Mark 0 |
| Rules removed | 1–2 (FTP, FR-10) | **2:** roles spend FTP; John's "within 2" |
| New on-screen | About 6 | **3, each necessary:** the "would have fired" ghost (teaches the arms), Lucy's arc and ghost number (THJ asked for her feedback), the swap beat (the swap can't read without it) |
| Re-meant (existing) | — | **4:** the badge's states, the zones on End Turn hover and through the enemy turn, John's prompt line, the Wrath beat (replaces "Max Wrath") |
| Removed from screen | 0 | **3:** John's zone and cover marker (no range), the NoFtp badge state; plus FR-10's hiding for Linda |

Net: about +3 rules, each one sentence on its hero's badge; John carries three of them, which is THJ's own proposal and goes to him as Q2.

**Cut or deferred to stay there.** From my draft: Linda's facing picker and default (replaced), L2 (lever), M2 and "counters earn no Focus" (withdrawn), J2's "until he strikes" (replaced). From THJ's set: stamina as its own system (Wrath carries it), minimum range on the bow, the ember pool. From the critics: the badge row by End Turn, threat arcs on the prompt, shield segments on John, Focus pips, the graded QTE (next experiment). From the design: Pilot 1's caps (FR-4) and the "Watch 2/2" label (FR-6), never built; kept AP.

---

## Paper scenarios

Frames read from the prefabs on 2026-11-09 with `level_to_grid.py`: `GB_s2-ridge` (plan tiles = prefab + 1 in x, with a border), `GB_m3-john` (+1 in x and y, with a border), `GB_s1-river` (no offset; `#` and `_` both mean no tile). x from the left, y from the bottom. Claws attack **4-way neighbours only** (`DarkClaw_Ability_Attack.asset`, Adjacent; CR-15). **AI paths and order are assumed:** each Claw takes the shortest path to a free 4-way neighbour of its nearest target; ties are stated. Values: Tutorial Claw HP 10, hits ≈3 (round 1's figure, assumed), Linda's bow 6 (×0.6 per further enemy), Crescendo 8 on a cell within 5 and its neighbours, Fist Blitz 8 within 2 (he steps into the cell of a kill, otherwise ends beside the target), Mark's move 3 (`Mark_Ability_Walk.asset`, 3 × `Stat_SPD`, SPD 1 assumed; John and Lucy assumed the same), Claws move 4, Wrath +35% a stack. Catch & Return isn't bought yet at the Ridge (the Family tree opens after the Yard), so arrows pass Mark.

### S1. The Ridge, rush pack, turn 1 (Linda + Mark), as built

Gauntlet (7,1, 8,1) asleep. 2,4 starts Alerted (3 from Linda) and wakes 1,5 and 3,5 (EN-15). The draft missed that Mark can reach 2,4: 3,1 → 3,3 (2 steps), then Blitz (3,3 to 2,4 is 2).

```grid id=rr2-s1-perhero title="S1 The Ridge, P2: forward line, Mark finishes 2,4 (GB_s2-ridge)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,3 2,5 linda watched: her line, beside Mark
arrow 2,1 2,4 linda dx=-8 one shot (10 to 4)
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz: dead, he steps in
arrow 3,5 2,5 enemy Watch if it ends here
arrow 1,5 1,4 enemy
step 2,4 1
step 2,5 2
note 2,1 2 arrows left
```

| Line | Player's turn | Enemy turn (assumed) | Result | Grade |
|---|---|---|---|---|
| **Forward (drawn)** | Linda shoots 2,4 once (10 → 4; quiver 2). Mark moves to 3,3 and Blitzes it (8 ≥ 4, dead) and steps into 2,4 | 1,5 and 3,5 go for Mark. His free neighbours: 1,4, 2,5, 3,4, 2,3. 1,5 picks 1,4 or 2,5; 3,5 picks 3,4 or 2,5 (1 step each; the tie-break is unknown). A Claw ending on 2,5 is in Linda's column next to Mark: **Watch** (6), before it strikes. Mark doesn't counter hits on himself | Linda 0 hits, 2 arrows. Mark 2 hits. 0–1 Watch, depending on the tie | ★ |
| **Hold** | Linda shoots 2,4 twice (dead; quiver 1). Mark stays on 3,1, beside her | 1,5 runs to 1,1 and strikes Linda: **counter** (1,1 is 2 from Mark; 8 → 2). 3,5 reaches 3,2 (3 steps) and strikes Mark, or 2,2 (4 steps) and strikes Linda (**counter** again, 2,2 is 2 from Mark). No Watch: 1,1 and 2,2 are next to Linda only | Linda 1–2 hits, 1 arrow. Mark 0–1 hits. 1–2 counters | ★ |
| Today | Two shots on 2,4 | 3 prompts (Watch, two counters), 0 choices (round 1) | | — |
| **Count (P2)** | **1 real decision:** forward or hold. It's Mark's (where he stands) and Linda's (one arrow or two), and it decides which roles can fire | Forward: 0–1 prompts. Hold: 1–2. **Each traces to where Mark stood** | Both lines reasonable: Linda's HP and arrows vs Mark's | |

*Coordinator, grid check 2026-11-09:* in the forward line, the Watch on 2,5 has to fly past Mark on 2,4 (Linda 2,1 → 2,5 along column 2). **To check** whether her arrow passes an ally; if it doesn't, the forward line has no Watch at all.

My draft counted 2 decisions here, and its ★ was dominated by its own "spend" line (systems critic). Corrected: one decision, and it's a family-position decision.

### S2. Memory 3, John's telling (John 1 AP, sisters 0 AP), as built

Five Claws, all alert. Order: (4,4) first (D-393, `turnOrder` 0); then assumed (6,5), (7,4), (2,5), (1,4).

```grid id=rr2-s2-perhero title="S2 Memory 3, P2: Shield Up, the first guard swaps John and Lucy (GB_m3-john)"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
cells 3,1 5,1 linda watched: beside John
arrow 4,4 4,3 4,2 enemy first: John, Wrath 1
arrow 6,5 6,4 6,3 6,2 enemy on Lucy: guard?
arrow 4,1 6,1 john dy=-8 swap
arrow 6,1 4,1 lucy dy=8 swap
arrow 7,4 7,3 7,2 7,1 enemy re-plans: John, Wrath 3
arrow 2,5 2,4 2,3 2,2 enemy unguarded
arrow 1,4 1,3 1,2 1,1 enemy unguarded
step 6,2 1
step 7,1 2
note 4,1 Shield Up
```

| | P2 (J1, J2, J3; Linda's filter) | |
|---|---|---|
| Player's turn | John: Shield Up (hinted; his only AP). The guard is armed because of it | 1 decision, hinted |
| Enemy turn | (4,4) → 4,2 strikes John (×0.6): Wrath 1. (6,5) → 6,2 on Lucy: **prompt** "Guard Lucy · 1 hit left". Pressed: John and Lucy swap (4,1 ↔ 6,1), John takes ×0.5 × 0.6 (≈0.9): Wrath 2; Blood Debt on that Claw. (7,4) re-plans on the new board: 7,1 is beside John (3 steps), so it strikes him: Wrath 3, **Wrath boils over**, no prompt. (2,5) → 2,2 and (1,4) → 1,1 strike Linda, unguarded (Blood Debt moves to the last of them). No Watch: Linda's watched tiles (3,1, 5,1, next to John or Lucy) stay empty | |
| The press, honestly | At Tutorial damage the HP difference is small, as the systems critic said. What the press changes is visible: pressed, Lucy ends beside (4,4)'s Claw and John on the right; declined, Lucy takes ≈3, John keeps the middle and his shield for one more guard (then (7,4) goes for Lucy: another prompt). It's a tutorial: a small choice you can see | 1 press with a visible consequence |
| Turn 2 | Wrath 1 already lets the Sword kill a Claw (8 × 1.35 = 10.8, systems critic), so the extra Wrath pays only on Shield Dash: 4 × 2.05 = 8.2 to each Claw beside the path, 10.7 on the Blood Debt Claw (kills; at Wrath 1 or 2 it doesn't: 7.0, 8.8). Which Claws a Dash reaches depends on where the swap left John (assumed). His shield is blocked this turn | |
| **Count** | **1–3 prompts** (today 6), all John's; **1 press with a consequence**. Only John's role fires, with no per-level switch: Linda's filter finds no Claw next to a sibling in her lines, and no family damage on the enemy turn means no follow-up | |

### S3. The Ridge with the pack awake: who does Linda cover?

The same as-built tiles with every enemy awake (the level's "all enemies start alert" flag, MI-27; data). Threats come from two directions: the rush down the north pocket, and the gauntlet along row 1, a 1-wide corridor from x 5. Mark's line is fixed so the choice is Linda's: 3,1 → 3,3, Blitz 2,4 (10 → 2), ending beside it on **3,4 (assumed; if he ends on 2,3, he stands in Linda's column and her watched tiles change)**. Order assumed: the gauntlet first, then the rush.

```grid id=rr2-s3-family title="S3 The Ridge, all awake, P2: Linda covers Mark (GB_s2-ridge tiles)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,4 linda watched: beside Mark
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz (10 to 2)
arrow 2,1 2,4 linda dx=-8 kills it
arrow 1,5 2,5 2,4 enemy Watch
arrow 7,1 6,1 5,1 4,1 3,1 enemy dy=6 strikes Linda
arrow 8,1 7,1 6,1 5,1 4,1 enemy dy=14
step 2,4 1
note 3,4 Mark ends here
```

| Line (P2, the family filter) | Linda's turn | Enemy turn | Result | Grade |
|---|---|---|---|---|
| **Cover Mark (drawn)** | Shoots 2,4 (2 HP, 3 away: dead; quiver 2). Now 2,4 is a free tile in her column next to Mark | 7,1 runs to 3,1 (4 steps) and strikes Linda: next to Linda only, no Watch. 8,1 ends on 4,1, can't reach anyone. 1,5 takes 2,5 → 2,4 (2 steps; the shorter way to Mark) and ends in her column next to Mark: **Watch** (10 → 4), then it strikes Mark. 3,5 strikes Mark from beside him (no move) | Linda 1 hit, Mark 2. 2,4 dead; gauntlet untouched; quiver 1 | ★ |
| **Thin the gauntlet** | Crescendo on 7,1 (5 away): 7,1 and 8,1 both 10 → 2 (quiver 2). 2,4 (2 HP) stays beside Mark | 7,1 (2 HP) reaches 3,1 and strikes Linda (no Watch). 8,1 ends on 4,1. 1,5 finds 2,4 taken and takes 1,4 → 1,3 → 2,3 → 3,3 (4 steps), next to Mark but not in her lines: no Watch. 2,4 and 3,5 strike Mark from beside him | Linda 1 hit, Mark 3. Both gauntlet Claws at 2: next turn one bow shot down row 1 pierces both | ● |
| **Count (P2)** | **2 decisions** (north or east; which also decides whom her Watch can cover) | 1 or 0 prompts, each traced to the tile she cleared next to Mark | Both reasonable: Mark's HP now vs a gauntlet set up for one pierce | |

*Coordinator, grid check 2026-11-09:* the drawing shows Mark's move to 3,3 and the Blitz, and notes him ending on 3,4. The enemy lines (3,5 striking without moving, 2,4 and 3,3 "next to Mark") all assume Fist Blitz leaves him on 3,4 beside the target when it doesn't kill. **To check** where a non-lethal Blitz lands him.

**THJ's facing lane on the same board** (the alternative, Q3; drawn in `rr2-s3-lane`). The facing rule lets Linda cover herself, so the corridor works for her: Crescendo east and face east, and the Watch kills 7,1 (2 HP) on 3,1 before it strikes; 8,1 ends on 4,1 with no Watch (with L2) or a second Watch (without L2). North: as "Cover Mark", but Watch fires on any Claw ending in her column. Count: 3 decisions (target, arrows, lane). The difference between the rules is the choice: **facing asks "which way is the danger"; the family filter asks "who am I covering"**. On this board that's Linda or Mark.

```grid id=rr2-s3-lane title="S3 alternative, facing lane: Linda faces east (GB_s2-ridge tiles)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 3,1 4,1 5,1 6,1 linda faced lane: east
arrow 3,1 3,2 3,3 mark dx=8 move
arrow 3,3 2,4 mark Blitz
arrow 2,1 7,1 linda dy=-10 Crescendo on 7,1
arrow 7,1 6,1 5,1 4,1 3,1 enemy dy=6 Watch kills it
arrow 8,1 7,1 6,1 5,1 4,1 enemy dy=14
arrow 1,5 1,4 1,3 2,3 3,3 enemy
step 3,1 1
note 3,4 Mark ends here
```

### S4. The River clearing, turn 1: strike or guard? (John + Lucy), as built

Added for the systems critic: the board where John's Shield Up competes with his attack. Three Claws asleep within 2 of each other (5,3, 6,4, 6,2); Archers far on their islands. John 1,3, Lucy 0,3.

```grid id=rr2-s4-river title="S4 The River clearing, P2: John strikes or raises the shield (GB_s1-river)"
# # . . . . # # . . _ . _ . . # #
# . . . . . . # . a _ . _ a . # #
# . . . . . c # _ _ . . . _ _ . .
U J . . . c . . . . . @ . . . . .
# . . . . . c # _ _ . . . _ _ . .
# . . . . . . # . a _ . _ . . # #
# # . . . . # # . . _ . _ . . # #
--
range 5,3 2 enemy wake together
arrow 1,3 4,3 john dy=8 step
arrow 0,3 3,3 lucy dy=-8 step: beside John
arrow 4,3 5,3 john Sword, or Shield Up
step 4,3 1
step 3,3 2
note 3,3 Sheltered; follows John
```

| Line | Player's turn | Enemy turn (assumed) | Grade |
|---|---|---|---|
| **Strike** | John steps to 4,3 (wakes 5,3 at 1, which spreads to 6,4 and 6,2). Lucy steps to 3,3, beside him (Sheltered). John's Sword on 5,3 (8 → 2): Lucy's **follow-up** (striker beside her, 5,3 is 2 from her): 6, dead. Lucy's second AP: free (6,4 and 6,2 are 4 from her, out of ember reach) | 6,4 and 6,2 come for John or Lucy; no shield, no guard. Lucy (15) takes up to 2 hits | ★ |
| **Guard** | John steps to 4,3 and raises Shield Up. Lucy steps beside him and embers 5,3 (main 4, plus a sidewinder or two: 4–10; how the sidewinders pick is **to check**) | Three Claws (or two) strike. Each hit on Lucy: a **prompt** (swap; they're adjacent, so the board barely moves). The third hit under the shield, his own or a guard, makes Wrath boil over, and the cost line says so: decline it and the shield stays for next turn | ★ |
| Hang back | Lucy stays at 2,3 (out of reach of John's side), embers from range | No follow-up (not beside the striker), no Shelter | ● |
| **Count** | **2 real decisions:** John's (damage now or a guard) and Lucy's (beside him or back). Prompts: strike 1 (follow-up), guard 1–3 (the breaking one is a real press) | | |

### Totals

| | Today | P (draft, as claimed) | **P2 (corrected)** |
|---|---|---|---|
| S1 | 0 decisions, 3 prompts | 2 / 1 | **1 / 0–2** |
| S2 | 0 / 6 | 1 + a press / 2 | **1 hinted + 1 press with a consequence / 1–3** |
| S3 | — / 3–4 | 3 / 1 | **2 / 0–1** (facing alternative: 3 / 1–2) |
| S4 | 0 / 2 (round 1) | — | **2 / 1–3** |

Fewer prompts than today, each traced to where the family stood or what John did, and one or two real decisions per board.

---

## Recommendation

**P2.** Roles cost no FTP. **John** guards while his shield is up, at any range, by switching places; three hits make his Wrath boil over, and the shield is gone for his next turn. **Linda's** Watch fires on an enemy that ends in her lines next to another Bergson. **Lucy** follows up a Bergson standing beside her, and shows it in the other heroes' previews (arc and "+6"). **Mark** as built. Readability first: the glyph contrast fix, the armed badge with reasons, armed roles shown on End Turn hover and through the enemy turn, the "would have fired" ghost. Kept AP withdrawn; THJ's facing lane is the alternative for Linda (Q3); stamina, minimum range, the ember pool, Kindle and Mark's Focus cost are not recommended.

### The stop rule, per hero

D-457's stop rule judged all roles at once after one session. That can kill John before his swap exists (creative critic), and it judges readability with a player who knows the rules (UX critic). Revised:

- **Per hero:** a hero whose rule fails goes back to as built (free); the others carry on.
- **John isn't judged until J3 has been played.**
- **Readability is judged by a cold player**, not by THJ.
- **The full stop** (lock every role as built, ship Lucy's preview, move the energy to Synergies) happens if John with the swap fails *and* the family filters give no decisions.

### Step 1: paper (this plan, ~15 minutes)

S1 to S4. Pass if each P2 line gives at least one real decision and every prompt traces back to one.

### Step 2: house-rule session (THJ, no code, one evening)

**What it can show:** whether the arms and filters change what THJ does on his turn, and whether the presses are choices; the FTP economy with free roles. **What it can't show:** readability (THJ knows the rules), the swap, the ghost, Lucy's preview.

**Data for the session (Tier 3, reversible):** `requiredFTP` 0 on the four role components (not +99 FTP, systems critic), and `requiredTimeScale` 0 on Linda's and Lucy's roles so their prompts pause and the filters can be judged (it changes the feel; note it).

| Hero | House rule |
|---|---|
| John | Press his guard only while Shield Up is on. Count every hit he takes under the shield; on the third, decline every further guard that turn and don't cast Shield Up on his next turn |
| Linda | Press Watch only for an enemy that ended next to John, Lucy or Mark |
| Lucy | Press her follow-up only if the striker stood beside her when it struck |
| Mark | As built |

Levels: Memory 3, the River, the Ridge (as built, then with "all enemies start alert"), one M4 or M6 fight, on `main`.

**Read after the session, two questions per hero** (systems critic): *Did you know why it fired?* (legibility, which THJ can only half-answer), and *Did you ever not arm it, not press it, or stand somewhere else because of it, and was that right?* (decision). And one for the creative critic: *Did you tell anyone about a role afterward? Which one?* Log: FTP at fight end, Duos per fight, Lucy's share of family damage, prompts per enemy turn.

### Step 3: code, in order (each behind its own Global Settings toggle, D-460, defaulting to as built)

| Order | Chunk | Size | Core items (Tier 3) |
|---|---|---|---|
| 0 | Glyph contrast fix (B4 item 1) | S | — |
| 0 | Lucy's preview (U1, redesigned), all branches | S–M | The attack preview path, additive |
| 1 | Readability: the armed badge, End Turn hover, the ghost; roles free (data) | S–M | Each handler's ghost hook |
| 2 | John J1 + J2 (the break, the block, the beat, the cost line) | S–M | `JohnFactionRoleHandler` |
| 3 | **John J3, the swap** | M | `JohnFactionRoleHandler.Activate`, `AEffectSwapper` mid enemy action |
| 4 | Linda's family filter and watched tiles | S | `LindaFactionRoleHandler` |
| 5 | Lucy's beside rule | S | `LucyFactionRoleHandler` |

After chunks 1–3, a **cold player** (not THJ) plays the Ridge and the River: can they say before End Turn which roles are armed, and after the enemy turn why one didn't fire (UX critic's test)? Can they say who John swapped with (creative critic's test)?

**Playtest signal.** *Worked:* players name the family member a role answered for ("he went for Lucy", "she covered Mark"); John's shield goes at least once a fight, and a guard is declined at least once a fight and called right; Linda's Watch fires on at least 1 in 4 enemy turns with enemies in range; Lucy's follow-ups between about one and three a fight, under a fifth of family damage; FTP ends most fights at 4 or less (else DU-5); rounds per fight toward 1.6–2.6. *Failed:* as each failure case above, then that hero's lever, then that hero back to as built.

### What it means for the Hearth

| Memory | Under P2 |
|---|---|
| 1 (Linda alone) | No Watch can fire (no sibling): THJ's "no FR before John" for free. The FP drain can go |
| 3 (John) | Only John's role fires (S2), with no switch. The lesson becomes Shield Up → guard → Wrath boils over → strike the Claw that went for them |
| 4 (Mark) | Linda's Watch can fire next to John, Lucy's follow-ups next to Mark. If THJ wants no roles at all here, it still needs the per-level role switch (after-Hearth F3) |
| River, Ridge | Their ★s hold (Shield Up + Wrath Shield Dash; Explosive Arrow + Blitz). The River gets harder by itself (fewer free guards) |

---

## Questions for THJ

**Q1. Replace the kept-AP test with P2 and its per-hero stop rule?**
- Context: kept AP is dominated whenever a target is in reach (THJ's objection, rechecked). My first per-hero draft made roles readable but not decided (systems critic) and solo-shaped (creative critic); P2 arms each role on the hero's turn and fires it for another Bergson. D-458 (player-turn roles free) still fits; D-459 is replaced; D-460 holds.
- Options: (a) P2: paper, one house-rule session (data: `requiredFTP` 0, prompts paused), code in order, a cold-player check, the per-hero stop rule; (b) P2 with D-457's all-at-once stop rule; (c) lock roles as built now (free) and move to Synergies, keeping Lucy's preview and the readability fixes.
- Recommendation: (a).
- Blocked: every Family Role chunk; the Hearth's role exposure (after-Hearth Q2).

**Q2. John: Shield-Up gate, Wrath boils over (shield gone for a turn), and the swap at any range, all in the test, with John not judged until the swap is played?**
- Context: these are your three John ideas, with Wrath carrying the stamina (one counter, already on the HUD; Memory 3 and the River teach it). The swap is the only thing that makes every guard press a choice (he leaves his post), and the riskiest code (core, mid enemy action). Three rules for one hero exceed D-295's "one new thing", so it's your call.
- Options: (a) all three, the swap as code chunk 3; (b) gate + break only, the swap only if the press still feels like a click; (c) gate only.
- Recommendation: (a).
- Blocked: John's chunks 2 and 3; the session's John rule.

**Q3. Linda: the family filter, or your facing lane?**
- Context: the filter (*"Watch fires on an enemy that ends in her lines next to another Bergson"*) asks "who am I covering": no picker, no core work, Memory 1 silent for free, corridors no longer free kill zones, she keeps arrows; she can't cover herself. The facing lane asks "which way is the danger": one picker on her HUD, works on one-front boards for her own defence; the UX and systems critics found its default already right on most boards. Both together is too narrow to fire. Minimum range on the bow isn't recommended (core targeting work, breaks Memory 1 and the Ridge).
- Options: (a) family filter; (b) facing lane (with the UX fixes and L2 as a lever); (c) filter in the session, facing kept ready as the fallback if it fires too rarely.
- Recommendation: (c), which is (a) with a named fallback.
- Blocked: Linda's chunk 4; the session's Linda rule.

**Q4. Lucy: follows up only a Bergson beside her, plus the preview now?**
- Context: you said she can stay free and needs much better feedback. Free and unlimited, she'd get stronger while the others get weaker (systems critic). The beside rule keeps her free and makes standing near the family the choice, at 15 HP. The ember pool reads as the quiver (all three critics). The preview is wanted under every option.
- Options: (a) beside rule + preview; (b) free + preview, cap 3 a round as a lever; (c) the ember pool.
- Recommendation: (a), with the preview built first, on every branch.
- Blocked: Lucy's preview tech plan; chunk 5.

**Q5. Mark: as built?**
- Context: he wasn't in your proposal. His counter is already for others and positional, so his decision is dive or stay by the family. My Focus-cost idea was always a yes press (systems critic) and can't be decided in a 1 s window (UX critic).
- Options: (a) as built; (b) once per enemy turn (D-042, never built); (c) the Focus bet (*"spends all his Focus and adds it to the hit"*), with his prompt paused.
- Recommendation: (a) for the test, (b) as the first lever if his counters carry fights.
- Blocked: nothing in the first test.

**Q6. Once roles are free, what is FTP for, and what does Pass-by give?**
- Context: with no role sink, pools stay near full and Duo cooldowns bind first, so Duos come often (against your "Duos as finishers"), and Pass-by's only payoff (FTP) stops mattering. Mark's Continuous Attack still costs FTP (D-216's "free" not built).
- Options: (a) Duo cost 3 (DU-5) if FTP ends most fights above 4, and decide Pass-by after the logs; (b) give Pass-by another payoff now (for a later plan); (c) keep roles at 1 FTP after all.
- Recommendation: (a): read the session's FTP log first.
- Blocked: the FTP side of the session read-out.

Names for `miso-narrative` if approved: the "Wrath boils over" beat and John's bark, the ghost's two-word reasons, the badge lines.

## Docs to update (if approved)

After the test, and only for what's adopted:

- `design/gdd/family-systems.md`: FR-3 (no FTP: built), FR-4 and FR-6 (dropped), the role table's trigger column for John, Linda and Lucy, a new **FR-14** for the principle (next free FR ID), FR-9 (armed roles on End Turn hover and through the enemy turn), FR-10 (no longer applies to Linda), FR-12 and FR-13 (John's zone and cover marker go, the tether stays, at any range), a new rule for the "would have fired" ghost and one for Lucy's preview (or CR, beside CR-45, CR-46, CR-49), the Deferred table (kept AP and its variants, the ember pool, Kindle, Mark's Focus cost).
- Character pages: John JO-1 (Wrath boils over, the block), his role line (the swap); Linda LI-11, LI-14 (the filter); Lucy's role line; Mark unchanged.
- `design/gdd/combat-rules.md`: CR-6 (roles free), CR-13 (FTP).
- `design/combat-balance.md`: the "2 reactions per hero per round" assumption.
- Onboarding: the after-Hearth plan's Family Role dependencies (a P2 column), Memory 1's FP drain, Memory 3's lesson text.
- `plans/family-role-chunk.md`: items superseded.
- `decisions.md` (coordinator): Q1 to Q6. Note: D-457 to D-459 are used twice on 2026-11-09 (the Family Roles test and the Lucy-memory gag).

Grids in this plan, to render: `rr2-s1-perhero` (changed), `rr2-s2-perhero` (changed), `rr2-s3-family` (new), `rr2-s3-lane` (kept as the facing alternative, Mark's landing noted), `rr2-s4-river` (new).

## Branches

- **`main`** (and everything that was `thj/onboarding`, D-456): the session and any switch.
- **`thj/home-test`**: no quiver; roles at 1 FTP; the Fireside "first Family Role free" (D-040) to remap once roles are free.

## Risks

- **The swap reads as a bug:** the cold-player check; fallback range 2 without the swap.
- **Linda's filter fires too rarely:** widen "next to", then the facing lane.
- **The tight family dominates:** watch whether hugging is ever wrong (area attacks).
- **FTP unbound:** DU-5, then Q6.
- **The session is half-blind:** THJ can't judge readability; the cold player after chunks 1–3.
- **Paper assumptions:** AI tie-breaks and order, Mark's Blitz landing tile, John's and Lucy's move 3, Claw hits ≈3, sidewinder targeting; the session is the real check.
- **J2's break mid-action:** the `Stat_DR` context history; EditMode tests on an area relay across the break.

## Gates

Design only. Step 1: THJ's time (~15 min). Step 2: THJ's time (one session; data changes on four prefabs, reversible). Step 3: tech plans (coordinator) → implementer (compile, EditMode tests) → reviewer → THJ play check per chunk → a cold player after chunks 1–3. Docs only after adoption.
