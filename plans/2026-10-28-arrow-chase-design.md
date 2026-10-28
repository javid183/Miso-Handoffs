# Arrow Chase: the Mark–Linda Duo

Size: L    Tier: 3 (Duos; a built Duo in a core script)    Assigned to: game designer
Branch: all (built on `thj/linda-quiver` **after D1** of the [distance plan](2026-10-27-linda-distance-design.md), and after C3b, Mark's QTE catch)
Status: waiting on THJ

## Why

The Family Footrace, the Mark–Linda Duo, ends the pair next to each other: the loser stops on `path[^2]` (V: `UnitsCooperationHandler.Mark_Linda_LoserStop`). Catch & Return needs Linda's arrow to reach Mark in line from 2 or more cells (D-274), so the Duo works against the pair's own Synergy. THJ wants Mark and Linda "distant but synced". He chose **Arrow Chase**, Mark racing Linda's arrow, to replace the Footrace (D-268, D-271). If Catch & Return is unlocked, the catch QTE can happen at its end. He accepts that it sits close to the Linda–Lucy Duo.

## Goal

Rules for Arrow Chase that a tech plan can build:
- Mark and Linda act in one beat and end far apart.
- The Duo is different from Catch & Return and from Marks-Sisters.
- Linda's damage share does not grow.
- The quiver still binds.

## Problem and evidence

- **The Footrace's shape** works against Catch & Return (above). Its rewards are a ×1.5 on the next basic attack and +1 AP for the loser: nothing about distance or arrows.
- **The Footrace's bonus listener** is added to `abilityPerformed` but removed from `abilityActivationStarted` (lines 1395/1408, V). It is never unhooked; the rework removes it.
- **What exists to build on:**
  - The catch (D-260): the arrow freezes at Mark on contact; pressed, it goes to the quiver with a return flight; declined, the same arrow carries on with its range and falloff.
  - The catch's own fast QTE (D-273).
  - Pickup on any Duo move (LI-7).
  - The race code's path, ghost and alternative-path helpers.
- **Damage share:** Linda deals 46–72% of the family's damage; D1 trades her Watch to 5× near and 7.5× Far (D-266). A Duo that adds Linda damage works against both.

## Options compared

| Option | Player experience | Rules complexity | Implementation cost | Risk | USP effect |
| --- | --- | --- | --- | --- | --- |
| A. **Chase to the landing**: Linda shoots; Mark runs to where the arrow lands, snatches it even under a living enemy, sweeps stacks; with Catch & Return, a QTE return flight down the lane | Mark jogs after the arrow; the bundle comes home | Medium: a snatch exception to the lock | Medium–high (core handler) | The snatch makes every shot free, so the quiver gains; the return hits the same line twice (≈12×, all Linda's); one click hides two places (where the arrow lands, where Mark ends) | Duos +, Synergies − (the Duo swallows the catch) |
| B. **Dead heat** (creative critic): Mark sprints to the free cell just before a target enemy on her lane and meets the arrow there. With Catch & Return, a QTE: pressed, he catches it and drives it home by hand; declined, it flies on as a normal shot | A synced, tense beat: his hand closes on the shaft just before it strikes | Medium: one target, one end cell, the catch's own two outcomes | Medium–high (core handler); the catch gains a third outcome, non-core | Free repositioning; QTE density | Duos ++, Synergies + (sets up next turn's catch) |
| C. **Stack fetch** (rev 2's Fetch Race): Mark runs to a grounded stack and throws it back; no shot | Pure housekeeping | Low | Medium | Dead when no arrows are down; competes with Encore | Duos + |
| D. **A real race**: if Mark's path is shorter than the arrow's flight he catches it mid-air, otherwise it lands first | Tension, but a hidden rule | High: two outcomes that depend on geometry | High | Unreadable timing rule | Duos + |
| E. **Footrace, apart**: the loser stops in line, 2 or more cells away | Same Duo, no longer in the way | Low | Low (one function, core) | Adds nothing about distance or arrows | Neutral |

**Recommendation: B.** It is the only option where the race is real, even if staged: the arrow and Mark arrive together, which is the image the name promises. B also answers the strongest point of all three critics:
- No snatch exception: the arrow follows the lock rule, so the quiver still binds.
- No return flight, so no double hit.
- One click, one place: Mark ends where the arrow is met.
- A decline behaves exactly like the Synergy's decline.

## Recommended rules (Arrow Chase, B)

**Availability.**
- A Duo (DU-1, DU-3). Mark or Linda activates it; the activator needs at least 1 AP left; cost 0 AP and 2 FTP (DU-2).
- Linda needs at least 1 arrow (`HasArrow`).
- Shared cooldown 2.
- Mark must be able to move (not Rooted; a Crippled Mark follows the same rule as his walk).

**Targeting (one click).**
- The player clicks an **enemy** on one of Linda's four lanes, within her bow range (4; 5–6 with Longshot).
- The **chase cell** is the free, walkable cell just before that enemy on the lane, on Linda's side.
- The target is valid only if:
  - the chase cell exists;
  - the chase cell is at least 2 cells from Linda (the catch's minimum, D-274), so the target stands 3 or more cells from her;
  - Mark can reach the chase cell (his walk radius + 1, the Footrace's reach today).
- The chase cell is **fixed at aim time** (systems critic): nothing that happens during the Duo moves it.

**Resolution, in order (reactions wait until the Duo ends).**
1. Mark sprints to the chase cell along his path. He picks up every **unlocked** grounded stack on it (LI-7, as any Duo move does). The sprint gives **no Pass-by FTP** (otherwise one pass-by refunds the whole Duo).
2. Linda fires a basic arrow down the lane (spends 1 arrow; 6× bow damage; pierce falloff). It hits every enemy between her and the chase cell as a normal bow shot. Its attacker is Linda.
3. The arrow reaches Mark at the chase cell (hitstop, the dead heat).
   - **Catch & Return locked:** no QTE. Mark lets it pass, and it flies on as a normal shot: the target and anything beyond are hit with falloff, and it lands per LI-6 (locked under a living enemy).
   - **Catch & Return unlocked:** the catch QTE (Mark's profile, D-273).
     - **Pressed:** Mark catches the arrow and **drives it into the target by hand**: one strike at Fist Blitz's 8× with *Mark's* stats (Focus, Heavy Hands). The attacker is Mark, so the damage counts as his. Nothing beyond the target is hit. The arrow stays in his hand and goes back to Linda's quiver with the bundle. The strike doesn't trigger Continuous Attack, and Mark doesn't step into the cell on a kill.
     - **Declined or missed:** the same arrow carries on, exactly like a declined catch (D-260).
4. **Hand-back.** One beat: Mark's throw variant with "+N". N counts the swept arrows, plus the caught arrow if the QTE was pressed. The quiver takes up to its size; extras stay on their tiles (LI-7).
5. **The Duo ends.** Then any queued reactions run (Masher counter, Lucy's follow-up on real damage, D-275/D-277; Mark's Counter as usual).

**What is returned.**

| Arrow | Comes back? |
| --- | --- |
| Swept stacks on Mark's path (unlocked) | Yes, by the normal pickup |
| The Duo arrow, pressed | Yes |
| The Duo arrow, declined or no unlock | No: it lands by LI-6, locked if the target lives |
| Stacks under living enemies | No (the lock holds) |

**After the Duo.**
- Both keep their AP: Mark stands next to the target, ready for a Fist Blitz.
- Mark ends on Linda's lane, 2 or more cells away, so her next basic arrow along that lane sets up Catch & Return. The Duo builds the Synergy's geometry instead of using it up (creative critic).

**Skill node.** *Head Start* (Mark's tree, 1 pip) changes from "cooldown −1" to **"+1 sprint reach"**. Cooldown 1 would make it an every-turn free move.

## How it differs

| | Arrow Chase (Duo) | Catch & Return (Synergy) | Marks-Sisters (Linda–Lucy Duo) |
| --- | --- | --- | --- |
| Chosen? | Yes, 2 FTP | No: happens when Mark stands in her line | Yes, 2 FTP |
| Mark moves? | Across the board, to the front | No, he is already there | Not involved |
| Where the arrow ends | In the target by Mark's hand, or flying on | Back in Linda's hands after a return flight | Lands at the end of the line |
| Damage | One basic arrow up to Mark; Mark's 8× strike on the target (pressed) | The bounce back hits again | 12× fire arrow down the whole lane |
| What it's for | Repositioning, arrows home, setting up the catch | A free extra hit | Burst damage |

## Previews and readability (UX critic)

While aiming:
- **Valid targets:** enemies on Linda's lanes that pass the rules get her target marker. Invalid ones show the reason on hover: "Too far for Mark", "Too close: no room to chase", "No arrows", "Not enough FTP", "Mark can't move".
- **Mark's ghost on the chase cell,** labelled "Mark ends here", with his path highlighted. Tab cycles his routes when routes differ (as the move preview does), and "+N arrows" updates per route. Locked stacks along a route stay visibly locked and add nothing to "+N".
- **The arrow path** from Linda to the chase cell, with a damage number on each enemy it hits.
- **The target,** with two outcomes when Catch & Return is unlocked:
  - the pressed number (Mark's strike, with a small QTE glyph);
  - the declined numbers (the arrow flying on), drawn ghosted.

  Without the unlock, only the flying-on numbers show. The preview never shows a number the action can't produce (CR-17 rule).
- **The catch icon** on Mark's ghost pulses when the unlock is on, with the hint "Press: Mark strikes · Decline: the arrow flies on". This uses the Synergy's decline wording, so a decline means the same thing everywhere.

During the Duo:
- A ring flashes on Mark one beat before the prompt (the catch preload is only about 0.25 s, D-273).
- The prompt reads "Catch".
- The hand-back shows "+N" on Linda (the D-259 cue).

Likeliest misread: "Mark will punch the enemy without the QTE". The ghosted fly-on numbers and the missing glyph cover it.

## Lens notes

- **Creative.** Linda says "Go." and Mark is already running. The arrow and the monk arrive together; his hand closes on the shaft a breath before it strikes, and he drives it home. Calm call-and-response, not trash talk: the creative critic's voice note for Children of Morta's Mark (the disciplined monk) and Linda (the eldest, gently teasing). For example: Linda "Go." / Mark "Early." / Linda "You were late." These go to `miso-narrative`. The memorable moment is the dead heat, so the hitstop is part of the design, not polish.
- **Systems.** The levers:
  - cooldown 2 (to 3 if it is used on more than 80% of the turns it's available);
  - the reach (walk + 1);
  - the pressed strike (8×; credited to Mark, which moves damage *off* Linda's share);
  - no Pass-by FTP.

  Interactions: the chase cell is fixed and reactions are deferred, so the Masher can't empty the cell mid-Duo. Arrows aren't duplicated: the Duo arrow returns only when caught. Encore keeps its job, because declined shots and locked arrows stay out. Failure cases: a free move every 2 turns that dominates the turn (watch the use rate); QTE density with Lucy's prompts.
- **UX.** One click on an enemy; one place where Mark ends; both outcomes previewed; the catch prompt announced.

## USP check

- **Duos:** strengthens. The pair act together at a distance; the Footrace's contradiction is gone.
- **Synergies:** strengthens. The Duo leaves the geometry for Catch & Return, and the unlock adds a choice inside the Duo without consuming the Synergy.
- **Family Roles:** neutral (Mark's Counter and Lucy's follow-up run as usual afterwards).
- **Home:** neutral on purpose.

## Critics

Three critics ran in parallel on 2026-10-28 (read-only Explore agents with critic briefs, each blind to the others), against option A.

| Lens | Strongest point | What I did with it |
| --- | --- | --- |
| Systems | The snatch is the usual case, not an exception (LI-6 lands arrows under the enemy hit), so every shot is free and the sweep makes the quiver grow. The return hits the same line twice (≈12×, Linda's). 0 AP for both partners plus a free move is too good. The Masher order is undefined. Pass-by refunds the FTP | **Accepted:** B removes the snatch and the return; the chase cell is fixed and reactions are deferred; no Pass-by FTP; the strike is Mark's damage; Head Start is no longer cooldown 1; cooldown 3 is the lever. **Not accepted:** Mark paying 1 AP (DU-1 says every Duo costs 0 AP, D-219) |
| Creative | A has no race: Mark jogs after an arrow that always wins. The moment is a dead heat, his hand closing on the shaft. The end QTE uses up the Synergy; the sweep turns the hand-back into a chore; "Too slow, sis" is the wrong voice | **Accepted:** B is the dead heat; the Duo sets up the Synergy; the calm voice. **Partly:** the sweep stays because LI-7 already applies to every Duo move, but it plays one Mark-voiced beat, not a chore list |
| UX | One click, two commitments: the player expects Mark on the clicked cell. The snatch contradicts the locked look. The second hit isn't previewed. "Decline" means something else here. The 0.25 s prompt needs a warning | **Accepted:** the click is on an enemy, with "Mark ends here"; no snatch; both outcomes previewed; decline matches the Synergy; the pulsing icon and the ring |

## Costs and risks

- **Core:** `UnitsCooperationHandler`. The `Mark_Linda_*` targeting, resolution and rewards are replaced: the target is an enemy, the chase cell is computed, the sequence is Mark's move, then the arrow, then the catch outcome. The race rewards and the listener mismatch go. Its own commit. Reusable: `Mark_Linda_Path`, the ghosts, the alternative paths.
- **Non-core:**
  - `ProjectileCatchAndReturn` gains a "strike" outcome for the Duo next to "return" (the arrow is frozen at Mark, D-260, so the strike reuses that point).
  - `QuiverArrow` and `LindaQuiver`: the caught arrow returns with the bundle.
  - Presenters for the previews.
  - `PlayerController.prefab`'s Duo entry and presets (data).
  - Mark's strike animation through `EntityAnimationHandler` (art: an arrow in hand, placeholder first).
- **Sprint without Pass-by:** may need a flag on the Duo move. If the pass-by handler is core and has no such flag, ask THJ (Q5).
- **Arrow hits by grid** (D-279, on `main` later): the chase cell, the pierce list and the previews must come from one route source (`ArrowLandingRules`, `Projectile.CollectPreviewPathHits`), so the move to grid hits doesn't split them.
- **`AIRegressionTest`:** new or renamed presets change the known-red message (as D-255). Compare before and after; no re-baseline.
- **Unlocks and saves:** the Footrace's family-tree entries and Head Start's text change; check saves that bought Head Start.
- **Size:** L. A tech plan of its own after D1 and C3b.

## Playtest signals (after it is built; M4, M6, full squad)

- Used on 30–70% of the turns it's available. Above 80%: cooldown 3.
- Mark ends 3 or more cells from Linda after the Duo, in most uses.
- Catch & Return fires on the turn after an Arrow Chase at least sometimes (the setup works).
- Catch QTE pressed in more than 60% of attempts (readable and reachable).
- Encore at least 0.5 per fight, and the quiver below 2 at some point in at least 60% of fights (it still binds).
- Linda's damage share not above the D1 build; FTP at fight end at most 4 (DU-5).
- Testers describe the dead heat.

## Questions for THJ

1. **Which shape?** *Context:* D-268 describes A (Mark sprints to where the arrow lands and the bundle goes home). All three critics found problems with A: free arrows, a double hit, one click in two places. *Options:* (a) B, the dead heat: Mark meets the arrow before the target; (b) A as described; (c) C, stack fetch. *Recommendation:* (a). *Blocks:* the Arrow Chase tech plan.
2. **What does a pressed catch do?** *Context:* the strike should be Mark's, so Linda's share doesn't grow. *Options:* (a) Mark's 8× strike on the target, and the arrow comes home; (b) the arrow's own hit with no falloff, and the arrow comes home; (c) only the arrow comes home, no extra hit. *Recommendation:* (a). *Blocks:* the rule and its preview.
3. **Without the Catch & Return unlock?** *Context:* D-268 makes the QTE conditional. *Options:* (a) no QTE: the arrow flies on, Mark has still moved and swept; (b) an automatic catch. *Recommendation:* (a): the unlock stays worth buying. *Blocks:* the rule.
4. **Head Start?** *Context:* a cooldown of 1 makes the Duo an every-turn free move. *Options:* (a) +1 sprint reach; (b) keep cooldown −1. *Recommendation:* (a). *Blocks:* the family-tree data.
5. **Pass-by during the sprint?** *Context:* one pass-by gives +2 FTP, the Duo's whole cost; turning it off may need a flag in the pass-by handler (core). *Options:* (a) no Pass-by FTP from the sprint; (b) as normal. *Recommendation:* (a), if it needs no core change; otherwise (b) and watch FTP at fight end. *Blocks:* nothing until the tech plan.

## Docs to update if approved

- [`family-systems.md`](../design/gdd/family-systems.md): the Mark–Linda Duo row (Arrow Chase replaces Family Footrace); a Catch & Return note (the strike outcome inside the Duo); the D-220 note on the race reward removed.
- [`characters/mark.md`](../design/gdd/characters/mark.md): Head Start, MA-3 note.
- [`characters/linda.md`](../design/gdd/characters/linda.md): the Duos line; LI-4 (the Duo spends 1 arrow).
- [`progression-economy.md`](../design/gdd/progression-economy.md): the Head Start unlock.
- `glossary.md` (Arrow Chase; `miso-narrative`), the bark lines, `decisions.md`, `status.md`.
