# Arrow Chase: the Mark–Linda Duo

Size: L    Tier: 3 (Duos; a built Duo in a core script)    Assigned to: game designer
Branch: all (built on `thj/linda-quiver` **after D1** of the [distance plan](2026-10-27-linda-distance-design.md), and after C3b, Mark's QTE catch)
Status: rev 3, THJ's shape (D-287 to D-289); five detail questions open

## Why

The Family Footrace, the Mark–Linda Duo, ends the pair next to each other: the loser stops on `path[^2]` (V: `UnitsCooperationHandler.Mark_Linda_LoserStop`). Catch & Return needs Linda's arrow to reach Mark in line from 2 or more cells (D-274), so the Duo works against their own Synergy. THJ wants them "distant but synced". **Arrow Chase** replaces the Footrace (D-268, D-271).

## Goal

Write up THJ's chosen shape (D-287 to D-289) as rules a tech plan can build: lane choice, Mark's run and sweep, the automatic catch, the return, and the mash. Include every edge case, the previews, and the trade-offs THJ has accepted.

## History

- **Rev 1:** the designer's "dead heat" (target an enemy; Mark meets the arrow before it). Critics ran.
- **Rev 2:** THJ's tile click (D-283) and Mark's strike (D-284).
- **Rev 3:** THJ's own shape, which supersedes both (D-287): Mark runs to the end of the lane, catches automatically, and the arrow flies back. With the unlock, a mash on the return (D-288). Cost and Head Start: D-289.

## Problem and evidence

- **The Footrace's shape** works against Catch & Return. Its bonus listener is added to `abilityPerformed` but removed from `abilityActivationStarted` (lines 1395/1408, V): it is never unhooked, and the rework removes it.
- **What exists to build on (V):**
  - The catch freezes the arrow at Mark and sends a return flight that ends at Linda (D-260, D-261, D-276).
  - Duo partners already carry a mash QTE profile with min/max factors (`CooperationPartner.qteProfile`, `qteFactor` applied as `CoopQteMod`; `QTEProfile.BehaviorMode.Mashing`; `MashQTE` fill 0–1 with growth and decay curves). Cooperative abilities read the final fill whether the mash succeeds or times out.
  - Pickup on any Duo move (LI-7).
  - Encore's straight-line return, which ignores locks and walls.
- **Damage share:** Linda deals 46–72%; D1 trades her Watch to 5× / 7.5× (D-266).

## THJ's "why not the end of the lane?": the honest answer

His shape is the clearest of the options:
- 4 choices (a lane), no tile hunting.
- The maximum distance between them, every time.
- The catch always happens, so the sync never fails.

It has three trade-offs, raised by the rev 1 critics:

1. **Mark ends far out and exposed.** He stands at the far end of Linda's range (4–6 tiles), often past the enemies she just hit, with 15 HP and outside John's zone. *What answers it:* it is the player's choice, shown in the preview (John's cover marker on Mark's ghost, FR-12); Mark keeps his AP to act or retreat; his Counter and barrier still work.
2. **The arrow is effectively free.** It costs 1 arrow and always comes home, plus everything on the line. *What answers it:* 2 FTP and cooldown 2 (D-289) limit it to every other turn and against the family's Duo budget; the quiver still binds between uses (her bow, Watch, Crescendo).
3. **The line is hit twice** (D-274), with Linda's arrow both ways. *What answers it:* the cooldown, falloff on both legs, and D1's lower Watch base, which pulls her share down elsewhere.

THJ has accepted all three (D-287). The levers if a playtest shows a problem are listed under Risks.

## Options compared

| Option | Player experience | Rules complexity | Implementation cost | Risk | USP effect |
| --- | --- | --- | --- | --- | --- |
| **THJ's shape (chosen, D-287)**: a lane; Mark runs to its end; automatic catch; the return hits again and brings the line's arrows; a mash with the unlock | Clear, always synced, maximum distance | Low–medium | Medium–high (core handler) | The three trade-offs above (accepted) | Duos ++, Synergies + |
| Rev 1 "dead heat" (target an enemy) | Tense, but it needs an enemy | Medium | Same | Narrow targets | Duos ++ |
| Rev 2 tile click + Mark's strike | Precise | Medium | Same | Two decisions; a strike target rule | Duos + |
| Footrace, apart | Same Duo, out of the way | Low | Low | Adds nothing | Neutral |

## Rules (D-287 to D-289)

**Availability.**
- A Duo (DU-1, DU-3). Mark or Linda activates it; the activator needs at least 1 AP left.
- Cost 0 AP, 2 FTP and 1 arrow; shared cooldown 2 (D-289).
- Linda needs at least 1 arrow (`HasArrow`); Mark must be able to move (not Rooted).

**Targeting: a lane.** The player picks one of Linda's four straight directions (hover or click the lane, like aiming her bow).

**Mark's end tile** is the furthest tile on that lane that is all of:
- at least 2 and at most Linda's bow range from Linda (4; 5–6 with Longshot);
- before the first **blocker** on the lane. Blockers are walls and other cells that stop an arrow, Lucy's Cyclone, Toba's wall, and the grid edge. Holes don't block: the arrow flies over them, though Mark can't stand in one;
- walkable and unoccupied (enemies and allies on the lane don't end it; Mark needs a free tile to stop on);
- reachable by Mark (his walk radius + 1, the Footrace's reach today).

If Linda's range is longer than Mark's reach, the end tile is the furthest valid tile he can reach. If no tile from 2 onward qualifies, the lane is greyed (reasons under Previews).

**Resolution, in order (reactions deferred until the Duo ends).**
1. **The run.** Mark runs to the end tile on a normal path. It can step off the lane to go around enemies or allies (CR-16). He picks up every **unlocked** grounded stack on his path (LI-7).
2. **The shot.** Linda fires her **basic bow arrow** down the lane, spending 1 arrow. It flies to Mark and hits every enemy between them as a bow shot: 6×, pierce falloff ×0.6, attacker Linda. Allies don't stop it (assumed as for her bow; the tech plan checks).
3. **The catch.** The arrow freezes at Mark (D-260's catch point). The catch is **automatic**: no press QTE. The Synergy's own catch prompt doesn't fire inside the Duo.
4. **The mash** (only with the Catch & Return unlock, D-288). Mark's mash QTE runs while the arrow is held (spec below). Without the unlock, there is no mash and the factor is ×1.0.
5. **The return.** The arrow flies back down the lane and ends at Linda (D-261). It hits every enemy between them again: 6× × the mash factor, falloff ×0.6 in the return direction, attacker Linda. As it passes, it **collects every grounded arrow on the lane cells between Mark and Linda** that Mark didn't take, *locked ones included* (Q1).
6. **Home.** The Duo arrow plus everything collected goes into the quiver, up to its size; the extras stay where they were. One hand-back beat: Mark's throw variant, then the return flight, with "+N" on Linda (D-259).
7. **The Duo ends.** Then the deferred reactions run once each:
   - Lucy's follow-up, once for the Duo action, on an enemy whose HP actually dropped (D-275, D-277);
   - Masher counters (EN-2: a Masher hit twice may answer twice; see Risks);
   - Mark's Counter as usual.

**Afterwards.** Both keep their AP. Mark stands on Linda's lane 2 or more tiles out, so her next basic arrow along that lane can trigger the Synergy.

**What comes home.**

| Arrow | Home? |
| --- | --- |
| The Duo arrow | Always |
| Unlocked stacks on Mark's path (on or off the lane) | Yes, by his pickup |
| Grounded arrows on the lane between Mark and Linda, locked included | Yes, by the return (Q1) |
| Arrows off the lane and off his path | No |
| Anything beyond the quiver's size | Stays where it was |

## The mash (D-288; the existing Mashing mode)

- **Profile:** `QTEProfile.BehaviorMode.Mashing` on Mark's partner entry in the Duo. Copy the curves of an existing Duo mash (Marks-Sisters) as the starting point. Duration 1.0 s; Mark's fast preload (D-273, about 0.25 s).
- **Factor:** return damage × (1.0 + 0.5 × fill). Fill is the mash meter at the end (0–1): a full meter ends the mash early at ×1.5. The partner entry's min/max factors are 1.0 and 1.5, so a weak mash never lowers the damage. DU-4's ×0.7 floor isn't used: the unlock should only add (Q4).
- **Cap:** ×1.5. It applies to the return leg only; the outbound shot is unchanged.
- **Seen:**
  - A ring on Mark one beat before the prompt.
  - The usual mash meter.
  - When the return starts, the final factor floats over Mark ("×1.4").
- **Without the unlock:** no prompt, no meter.

## Head Start (D-289)

- **Current:** cooldown −1 (2 → 1), kept for now. That makes Arrow Chase usable every turn, which a playtest must watch.
- **Options THJ named for later:**
  - (a) more arrows returned: the return also collects from the cells next to the lane, one on each side;
  - (b) a longer return reach: it also pulls grounded arrows within 2 tiles of Mark's end tile.

  Both keep the cooldown at 2 (Q3).

## How it differs

| | Arrow Chase (Duo) | Catch & Return (Synergy) | Marks-Sisters (Linda–Lucy Duo) |
| --- | --- | --- | --- |
| Chosen? | Yes, 2 FTP | No: when Mark is already in her line | Yes, 2 FTP |
| Mark | Runs to the end of her lane | Stands still | Not involved |
| The catch | Automatic; a mash with the unlock | A press QTE (D-260) | — |
| Arrows home | The Duo arrow + everything on the line + his path | Only the caught arrow | None (it lands) |
| Damage | The line twice: 6× out, 6× × mash back | The return hits again | 12× fire, whole lane, once |
| What it's for | Mark to the front, arrows home, a double-hit line | A free extra hit | Burst damage |

## Previews and readability

While aiming (lanes highlighted like her bow):
- **A greyed lane** gives its reason on hover: "Blocked within 2", "No free tile for Mark", "Too far for Mark", "No arrows", "Not enough FTP", "Mark can't move".
- **The hovered lane** shows:
  - Mark's ghost on the end tile, labelled "Mark ends here", with his path. Tab cycles routes when they differ.
  - John's cover marker on the ghost if it is covered (FR-12). With no marker, the player sees Mark will be exposed.
  - **"+N arrows"**, split: "+2 run · +3 return". Locked stacks the return will take get a small return arrow on their lock badge (they read as "coming back", not as "stuck").
  - **Damage per enemy on the line:** two stacked numbers, out and back ("6 + 6"). With the unlock, the back number is a range ("6 + 6–9") with a small mash glyph. The preview never shows a number the action can't produce.
- **During the Duo:**
  - The run.
  - The shot.
  - The hitstop at the catch.
  - The ring on Mark, then the mash meter (with the unlock).
  - The return.
  - "+N" on Linda.

**Likeliest misread:** "the return is a separate hit I must earn". The stacked numbers show it always happens, and that the mash only raises it.

## Lens notes

- **Creative.** The target experience and moment: Linda says "Go."; Mark runs her lane, scooping her arrows as he goes, turns at the far end, and her arrow is already in his hand. One breath, and it's flying home through the same goblins, and she catches it. They never stand together; they never miss each other. Calm call-and-response for the voice (the rev 1 creative critic's note for the disciplined monk and the gently teasing eldest): Linda "Go." / Mark "Early." / Linda "You were late." These go to `miso-narrative`. The hitstop at the catch is part of the design.
- **Systems.** The rules: lane, run, shot, catch, mash, return. Interactions: pickup (LI-7), the return borrowing Encore's lock-ignoring rule, Lucy's real-damage rule, Masher counters, Pass-by (Q2). The levers are under Risks.
- **UX.** One choice out of four; the end tile, the exposure, the arrows and both hits are all in the preview.

## USP check

- **Duos:** strengthens. Distant and synced by construction.
- **Synergies:** strengthens. The Catch & Return unlock adds the mash inside the Duo, and Mark ends in her line for the Synergy.
- **Family Roles:** neutral (Lucy, the Masher and Mark's Counter answer afterwards as usual).
- **Home:** neutral on purpose.

## Critics

Three critics ran on 2026-10-28 against rev 1's option A (read-only Explore agents, each blind to the others). Their concerns that still apply to THJ's shape are the trade-offs above:
- **Systems:** a free arrow, the double hit, the Masher order, Pass-by.
- **Creative:** the dead-heat image and the calm voice.
- **UX:** one place Mark ends, both hits previewed.

Kept from them: the deferred reactions, a fixed end tile, "Mark ends here", stacked numbers, and the ring before the prompt. Rev 3 was not re-critiqued: the shape is THJ's decision, and the critics' points are written up as accepted trade-offs and levers.

## Costs and risks

- **Core:** `UnitsCooperationHandler`. The `Mark_Linda_*` targeting (a lane), the resolution (the end tile, the sequence: run, shot, catch, mash, return) and the rewards are replaced; the race rewards and the listener mismatch go. Its own commit. Reusable: `Mark_Linda_Path`, the ghosts, the alternative paths, the partner mash profile and factors.
- **Non-core:**
  - `ProjectileCatchAndReturn`: an "automatic" catch mode for the Duo (no press); the return carries the mash factor and collects arrows on the line.
  - `QuiverArrow`, `LindaQuiver`, `GroundedArrowField`: collect along the line, take locked stacks, respect the size.
  - The presenters.
  - The `PlayerController.prefab` entry and presets (data).
- **Pass-by off during the run** may need a flag in the pass-by handler (core); Q2.
- **Arrow hits by grid** (D-279, on `main` later): the end tile, the out and back hit lists and the line collection must come from one route source (`ArrowLandingRules`, `Projectile.CollectPreviewPathHits`).
- **The Masher on the line** is hit twice and may counter twice (EN-2 has no limit yet; D-274 notes this is being checked). Watch it in play.
- **Levers if it's too strong:**
  - cooldown 3, and Head Start to option (a)/(b) instead of −1;
  - return base 6× → 4×;
  - mash cap ×1.5 → ×1.3;
  - Duo FTP 2 → 3 (DU-5).
- **`AIRegressionTest`:** new or renamed presets change the known-red message (as D-255). Compare; no re-baseline.
- **Unlocks and saves:** the Footrace's tree entries; Head Start's text.
- **Size:** L; its own tech plan after D1 and C3b.

## Playtest signals (after it is built; M4, M6, full squad)

| Signal | Pass | If it fails |
| --- | --- | --- |
| Used on the turns it's available | 30–70% | Above 80%: a lever |
| Encore per fight; quiver below 2 at some point | ≥ 0.5; in ≥ 60% of fights | The arrow is too free: return base or cooldown |
| Linda's damage share | Not above the D1 build | Return base 4× |
| Mark's HP after the Duo; deaths next enemy phase | Deaths under 1 in 3 levels | The exposure is a trap: shorter reach, or a cover rule |
| Average mash factor (with the unlock) | 1.2–1.45 | Easier or harder curves |
| FTP at fight end | ≤ 4 | DU-5 |
| Catch & Return fires the turn after | Sometimes | The setup isn't used |
| Testers | Describe the run and the catch | — |

## Questions for THJ

Answered by THJ, 2026-10-28 (D-290): Q1 yes, the return collects locked arrows; Q2 Pass-by **on** like any move; Q3 keep Head Start −1, watch the 80% use signal; Q4 ×1.0–×1.5; Q5 6×, lever 4×. Status: design approved, built after D1.

Answered: shape (D-287), no unlock = always catch + line arrows home (D-288), cost and Head Start for now (D-289). Superseded: D-283, D-284.

1. **Does the return collect locked arrows on the line?** *Context:* your "returns arrows in the line to Linda"; Encore already pulls locked ones. *Options:* (a) yes, every grounded arrow on the lane between them, locked included; (b) unlocked only. *Recommendation:* (a): one simple line rule, and it reads as "the line comes home". *Blocks:* the return rule and the lock badge preview.
2. **Pass-by during the run?** *Context:* one pass-by gives +2 FTP, the Duo's whole cost; turning it off may need a flag in the pass-by handler (core). *Options:* (a) no Pass-by FTP from the run; (b) as normal. *Recommendation:* (a) if it needs no core change, otherwise (b) and watch FTP at fight end. *Blocks:* nothing until the tech plan.
3. **Head Start after the first playtest?** *Context:* cooldown −1 makes the Duo usable every turn. *Options:* (a) keep −1; (b) more arrows returned (the cells next to the lane); (c) a longer return reach (within 2 of Mark's end). *Recommendation:* keep (a) for the first build, and switch to (c) if the use rate passes 80% with the node. *Blocks:* nothing now.
4. **The mash factor.** *Context:* the Duo mashes today use ×0.7–×1.5 (DU-4); here the unlock should only add. *Options:* (a) ×1.0–×1.5; (b) ×0.7–×1.5 as the other Duos. *Recommendation:* (a). *Blocks:* Mark's partner entry data.
5. **The return's base damage.** *Context:* the line is hit twice with Linda's arrow (accepted, D-287); her share is the quiver's problem. *Options:* (a) 6× like the outbound, with 4× as the lever; (b) start at 4×. *Recommendation:* (a): test your shape as you described it, and watch the share. *Blocks:* the return data.

## Docs to update if approved

- [`family-systems.md`](../design/gdd/family-systems.md): the Mark–Linda Duo row (Arrow Chase replaces Family Footrace: lane, run, auto catch, return, mash with the unlock, 2 FTP + 1 arrow, cooldown 2); a Catch & Return note (the mash inside the Duo); DU-4 note (this Duo's mash is ×1.0–×1.5); the D-220 note on the race reward removed.
- [`characters/mark.md`](../design/gdd/characters/mark.md): Head Start (cooldown −1; later options), MA-3 note.
- [`characters/linda.md`](../design/gdd/characters/linda.md): the Duos line; LI-4 (the Duo spends 1 arrow and returns it).
- [`progression-economy.md`](../design/gdd/progression-economy.md): Head Start.
- `glossary.md` (Arrow Chase; `miso-narrative`), the bark lines, `decisions.md`, `status.md`.
