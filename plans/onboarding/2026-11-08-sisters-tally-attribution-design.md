# Sisters' tally: who gets the kill, and is the window enough

Size: M    Tier: 3 (game feel, USP touch)    Assigned to: miso-game-designer (design); implementer later if approved
Branch: thj/onboarding (the tally is onboarding-only; the core bug in "Code facts" exists on every branch that has Duos)
Status: waiting on THJ

## Why

THJ play-checked the HUD counter on 2026-11-08 and asked four questions: who gets a Linda–Lucy Duo kill (today: no one), who gets a kill when Linda wounds and Lucy's Family Role finishes, who gets Tempest Bloom kills, and whether the short visible window makes the player feel anything. Built tally: [tech plan](2026-11-08-sisters-tally-tech.md), D-444 to D-448. Design source: [first-hour design](2026-10-25-onboarding-first-hour-design.md) › The Sister's Rivalry arc, [narrative draft](onboarding-narrative-draft.md) T11-3 to T11-6, F-SR, F-SR2, [levels plan](2026-10-26-onboarding-levels.md) › M2 · The Trail.

## Goal

One attribution rule the player can say in a sentence, and a visible tally that gets at least one memorable moment before "Still counting?" / "…No.", with no new level.

## Code facts behind Q1–Q3

Read on `thj/onboarding` @ `6af47eeb6` plus the working tree, 2026-11-08. **V** = verified by reading the code; **A** = assumed or inferred, needs a play check.

How a kill reaches the tally: `CombatLevelRunHandler` takes an HP snapshot on `abilityActivationStarted` and, on `abilityPerformed`, compares each affected enemy's HP with it and raises `onUnitDamageDone(ability, target, amount, lethal)` (lines 761–837). The tally reads `ability.Owner`. (V)

1. **The Linda–Lucy Duo counts for no one: its damage never reaches `onUnitDamageDone`.** (V, by reading; matches THJ's play check)
   - The Duo runs as: the trigger ability (`Linda_Lucy_Duo_Ability`, owned by whichever sister pressed it) → `AEffectCoOpTrigger` → `UnitsCooperationHandler.Execute` → each partner's own `RuntimeAbility` through `AbilityOrchestrator.ActivateAbility` (`CooperationEntry.ExecuteIE`, `ActivateAbility`). Linda's partner ability spawns the fire arrow (`LindaAttackFireArrow` projectile); Lucy's partner ability only targets Linda (the enchant VFX).
   - `abilityActivationStarted` and `abilityPerformed` are raised only for the player's chosen ability (`FactionControllerBase` lines 726, 1014) and by the role handlers for their own ability. The partner abilities raise neither. So Linda's arrow hits are buffered under her partner ability, never get a snapshot, never get flushed, and no damage event fires for them.
   - The arrow's owner is Linda (the projectile and its clones keep the spawner's owner and stat context: `AEffectSpawner`, `Projectile.GetClone`). So the attacker *would* be Linda if the event fired.
   - Possible exception (A): the trigger ability has `actualTargets: 1` and stays in progress until the Duo ends, so its own flush may report the **aimed** enemy with attacker = the sister who pressed the button. THJ saw no count, so either it doesn't fire in practice or his test kill wasn't the aimed enemy. Whatever we choose, the implementer must check this and ignore the trigger ability's report, or it double counts.
   - **Wider bug, not the tally's to fix:** every Duo's damage is invisible to every `onUnitDamageDone` listener: `MissionStatsTracker`, John's Wrath and Blood Debt, Mark's Atman Barrier, `BarkManager`, Masher Goblin's counter, the grounded-arrow pickup. Same for the Mark–Lucy Duo's sidewinders and Mark's ghost hits. Flag to the coordinator for a separate core plan (see THJ question C).
2. **Linda wounds, Lucy's Family Role finishes: Lucy gets the kill today.** (V) `LucyFactionRoleHandler.Activate` raises `abilityActivationStarted` and `abilityPerformed` for its own ability (lines 220–235), owner Lucy. Her ember is a separate action with its own snapshot, so the lethal hit is Lucy's. The reverse holds too: Lucy wounds, Linda's Watch arrow kills on the enemy turn → Linda (`LindaFactionRoleHandler` lines 76–91, V). Lucy's role never follows the Linda–Lucy Duo (FR table; GDD).
3. **Tempest Bloom kills are probably lost today.** (A) The split copies keep Linda's owner and her firing ability as stat context (V), so their hits are attributed to Linda's basic, Watch or Duo ability. But the original arrow is disposed at the Cyclone, which ends the spawner's "in progress", so the firing ability can complete before the copies land. A late hit goes into the buffer after the flush and is compared against no snapshot later, so it raises nothing (A, from reading `CombatLevelRunHandler`; Lucy's handler has a comment that late projectile hits happen). Needs a play check: Lucy's Cyclone, Linda shoots through it, a copy kills; does the counter move?
   - **It can't happen in the window that matters yet:** on `thj/onboarding` (Bond Lite merged), Tempest Bloom and Sister's Rivalry are shut until Linda & Lucy's Bond Lv 2, reached at the Yard *after* The Trail (GDD [family-systems](../../design/gdd/family-systems.md) BO-4). The Hearth's one-mission Bloom grant falls in The Hearth, which the tally leaves out. So Bloom only matters once Tally: return is placed (D-448). (V from the GDD; the grant scope not re-read in code.)
4. **Is the "other sister" contribution recoverable?** (V)
   - `GUnit.TotalAttacksMemory` (per attacker, a count of hits) and the ordered recent-attacker memory (`GetMostRecentAttacker`) are filled by `AEffectBase` whenever an enemy effect is applied to the unit (`GotTargeted`). So at a kill, the tally can ask "did the other sister ever hit this enemy?". It is per level, not per turn, and counts effect applications, not damage.
   - The Duo's partners are named in the bus: `GlobalEventBus.RaiseSynergy(activator, "Duo", id, partners)` fires at Duo start (`UnitsCooperationHandler.Execute`), and the trigger ability's `abilityPerformed` fires after the whole Duo, because `AEffectCoOpTrigger` keeps it in progress until then. That gives a clean bracket, the pattern `MarkPassiveAbility_ContinuousAttack` already uses (`unitDied` inside an activation bracket).
   - Tempest Bloom raises `RaiseSynergy(owner, "Tempest Bloom", ...)` at the split (`LucyCycloneProjectileScatter`), so a split is visible on the bus; the end of the copies' flight is not (no event; an implementer would need the copies' `onDestroy`).
   - `CombatLog` also records actions (not read in depth).

## Problem and evidence

**Symptom:** the counter barely moves before the pile fade, and the Duo, the one ability built for both sisters, adds nothing.

**Root problems:**

1. **The tally's biggest moment is silent.** Both Trail routes were designed around the Linda–Lucy Duo fired up a column: route A hits 3 Dark Claws in column 4 (kills at a median mash), route B hits 2 stacked Archers ([levels plan](2026-10-26-onboarding-levels.md), first-trigger rows; built in `d72204178`, enemy counts not re-read in the assets). That *is* THJ's "line of enemies that screams shoot them". It's already in the game, and today it counts 0–0.
2. **The tally has no setup.** The arc's beats are Setup (the Hearth's bragging contest), Running joke (River/Ridge, apart: "Tell Lucy I'm ahead"), Turn (the pile). As built, the tally first appears in The Trail and fades at the end of that same mission. The player meets the number and loses it within one mission, about 11 minutes of play (route ≈ 4, pile ≈ 6.75; counter visible through the pile until its end dialogue). The setup lives only in dialogue lines (V1-2a/b, G9-9 to G9-12, M3 barks), not on the HUD.
3. The window isn't really short in minutes (~11 min, ~8–10 enemies). The trouble is that it is a single mood: the pile opens on "Then we find her. Together." (T11-4) and the barks stop, so the only lively stretch with the counter on is the route level, and its main kill counts for nobody.

## Options compared

### A. Attribution (Q1–Q3)

| Option | Rule in a sentence | On screen | Arc | Complexity | Cost | USP effect |
|---|---|---|---|---|---|---|
| **A1 Last blow; the Duo counts for Linda** (her arrow) | "The sister whose attack lands the kill gets it." | Route A Duo: Linda +3, Lucy +0 | Rivalry fuel ("my fire, your kill"), but turns the first real Duo into a Linda solo | None new | Duo bracket (below), Linda only | Weakens Duos: a paired ability reads as one sister's |
| **A2 Last blow; a kill made together counts for both** (rec.) | "A kill counts for the sister who made it; a kill they make together (their Duo, Tempest Bloom) counts for both." | Route A Duo: both numbers tick +3 at once | The only time both numbers move together is when they act together: a quiet foreshadow of "We both did", unspoken | None new: same two numbers | Duo bracket; Bloom window later | Strengthens Duos and the Bloom Synergy |
| **A3 A third "together" number** | "Shared kills go into a third count." | A third label ("Together N") on the HUD and the results row | Strongest theme; could become the return's headline after "We both did" | +1 element, +1 thing to track: over budget (D-295) | Bracket + UI work in C2/C3 | Strengthens Duos; more to read |
| **A4 Counts for whoever pressed the button** | "The Duo's kills go to the sister who started it." | Depends on the button pressed | Arbitrary: the arrow is always Linda's | None new | Bracket | Neutral to weak; reads as a bug |
| A0 Do nothing | "The Duo doesn't count." | 0–0 after the big shot | Kills the route level's moment | — | 0 | Weakens Duos |

Q2 inside every option: **Lucy's role finishing Linda's wounded enemy stays Lucy's** (as built). It's the Hearth's "the sisters steal kills" ([first-hour design](2026-10-25-onboarding-first-hour-design.md), segment 3) made mechanical: Linda does the work, Lucy's embers snatch it, Lucy's number moves. Counting it for both would pre-empt the Yard's discovery, "You pin it, I burn it?" (Y12-5), which has to come *after* the pile. A role reaction is one sister's choice. A Duo or a Synergy is the pair's.

### B. The window (Q4)

| Option | What | Player experience | Level work | Pacing | Complexity |
|---|---|---|---|---|---|
| **B1 Fix the Duo, nothing else** (rec., base) | A2 makes the route level's column shot the tally's spike | One clear moment: big shot, both numbers jump, then the grim pile, then "Still counting?" | None | 0 min | None |
| **B2 The tally in the Hearth's segments 3–4** (rec. as a question) | Eligibility per level ("both sisters deployed here") instead of per mission roster; The Hearth leaves the excluded list. Segments 1–2 stay silent (one sister) | The counter is born in the bragging contest ("You both did." / neither accepts), so the Trail's fade lands on something the player has seen twice, in two moods | None | 0 min | No new rule; changes eligibility data. Risk: one more HUD item during John's lesson |
| B3 Solo scores in River/Ridge carried into The Trail | Each sister's count while apart, carried across missions | Matches the design's "Running joke" placement | None | 0 min | New: cross-mission carry (a save or session field), a one-name layout, mission order. Over budget |
| B4 Barks on the score | A short pair on the Duo's jump or a lead change | Adds voice | None | ~0 | A tally-driven bark trigger is new tech (A); a "Linda kill" scoped bark may already exist (G9-9) |
| B5 A new or reshaped Trail level as a rivalry showcase | E.g. 5–6 enemies in a line | Duplicates what the route levels already do | Grids, wiring, play check | +3–4 min, before the timed check ("cut before stretching") | Reject |

## Lens notes

**Creative.** Target: before the pile, the score is a game the sisters play while they hunt. It's loud, petty, theirs. At the pile the game stops mattering. The moment to design for is the route level's column shot. Lucy lights the arrow, Linda looses it, three Claws drop, and **both numbers jump together**. Nobody comments. Minutes later, over the pile, Linda asks "Still counting?" and the player has watched the number that just faded move. A2 makes the only shared tick the shared act, so "We both did" (F-SR2) later reads as something the player already saw. With B2 the counter's first life is in the memory, where John says "You both did." and neither accepts. The line and the number sit side by side, and the M4 callback closes the loop. The genre default is an MVP stat. This is a scoreboard that a story beat switches off, which fits Children of Morta's warmth against dread.

**Systems.**
- Rule (A2): a kill counts 1 for the sister whose ability made the lethal hit. A kill made by the sisters' Duo counts 1 for each sister in that Duo (Linda–Lucy: both; Mark–Lucy: Lucy). A kill made by a Tempest Bloom copy counts 1 for both.
- Duo detection (feature-local, no core edit): open a bracket on `onSynergyTriggered` with id `"Duo"` naming a sister among its partners; close it on `abilityPerformed` for the trigger ability. Inside it, an enemy `unitDied` whose HP is at its minimum (the tally's existing `IsAtMinimum` check) counts for each sister among the partners. Ignore `onUnitDamageDone` from the trigger ability inside the bracket (the possible aimed-target report, fact 1). Nothing else can kill during a Duo: Lucy's role skips this Duo, and John's and Mark's roles and Linda's Watch need an enemy action or move (A: a burn tick or hazard inside the bracket would be miscounted; the implementer checks whether any can fire there).
- Tempest Bloom: a window from the split's `onSynergyTriggered("Tempest Bloom")` until its copies are gone. Build it with Tally: return (D-448), after the play check in fact 3. Before the Yard it can't fire.
- Levers: none numeric. The rule is attribution only; nothing in combat reads the tally.
- Failure cases: totals exceed the kills (a Duo 3-kill shows 3–3). That's harmless and intended. Restart farming is already handled (attempt dropped). Double count via the trigger report is handled by the ignore rule. Revert of a Duo kill: Duo partners are not revertible (`revertible: 0` on the spawn effect), so no undo path (V for the spawn asset).
- Expected numbers by "Still counting?" (A, from the paper levels): route A ≈ Linda 4, Lucy 4 (Duo 3–3 plus one each); route B tilts to Linda (the Duo doesn't kill the Archers at 12 damage, so her arrows finish them); the pile adds 5 enemies shared with John or Mark.

**UX.**
- Shown: the existing counter, "Linda N  Lucy N". On a Duo or Bloom kill, both numbers update in the same frame. If the counter already pulses on a change, both pulse (C2's widget; no new element). The results row is unchanged.
- The player clicks nothing new.
- Likeliest misread: "it counted six for three kills: bug?" It's flavour and the counter doesn't claim to be a total, so this is acceptable. The second misread is Linda's number not moving when Lucy's embers finish her target. That's the joke, and if testers read it as a bug, a narrative bark can name it ("That was mine." / "Was it?"), as B4.
- B2 adds the counter to the HUD in segments 3–4. During John's Role → Wrath lesson, the counter is passive and teaches nothing, but it is one more thing on screen in minute ~8. Watch for it in the timed check.

**Where the lenses disagree.** Creative wants A3, the visible "together" number, as the strongest theme. Systems and UX say a third number is a second thing to track (D-295). I lean A2: it gets most of the theme with zero new elements, and A3 stays available as the *return*'s design (the tally could come back after "We both did" as one number), which is a separate decision (D-448).

## USP check

- **Duos:** strengthens. Today the first real-combat Duo erases its own kills from the tally. With A2 it's the tally's biggest, most visibly shared moment.
- **Synergies:** strengthens, later. Tempest Bloom kills count for both once it unlocks; the tally foreshadows Sister's Rivalry's "We both did" payoff without a new rule.
- **Family Roles:** slight strengthen. Lucy's role snatching Linda's kills turns her role into a character beat (the kill-stealing joke).
- **Home:** neutral on purpose. The Yard's "You pin it, I burn it?" stays the discovery.

## Critics

Not run: size M (coordinator), no L stakes.

## Recommendation

**A2 + B1, with B2 as THJ's call (my lean: yes).**

- Rule: "A kill counts for the sister who made it; a kill they make together counts for both." Lucy's role finisher stays Lucy's (Q2). The Duo counts for both (Q1). Tempest Bloom counts for both, built with the return (Q3).
- Build (one chunk, C5, feature folder only): the Duo bracket and the trigger-report ignore, plus EditMode tests for the rule (bracket open/close, both credited, Mark–Lucy credits Lucy only, fake death inside the bracket doesn't count, trigger report ignored). Tempest Bloom's window goes with Tally: return.
- No new level, no grid changes. If B2 is approved: eligibility from the level's deployed player units instead of the mission roster, and an empty excluded list (or one kept for other memories).
- Before building: one play check of the aimed-target report (fact 1, route A, aim at a Claw that dies), and later the Bloom late-hit check (fact 3).

**Playtest signal (timed pacing check):** after The Trail, ask "what was the counter by the sisters' portraits?". Success: the player names it, and at least one remembers the Duo making both numbers jump, or reads "…No." as the score stopping mattering. Failure: nobody noticed the counter before the pile, or testers call the 3–3 jump a bug. If so, try B4 (one bark pair on the jump) before anything bigger. If the counter goes unnoticed even with B2, the tally is a cut candidate under the off switch (D-446), not a candidate for a new level.

## Questions for THJ

**A. The attribution rule**
- Question: Who gets a kill the sisters make together, and who gets a Family Role finisher?
- Context: today the Duo counts for no one (its damage never reaches the event the tally listens to), and Lucy's role finisher counts for Lucy. Tempest Bloom can't fire before the pile (Bond Lv 2 comes at the Yard).
- Options: A1 last blow, the Duo for Linda; **A2 last blow, together kills (Duo, Tempest Bloom) count for both**; A3 a third "together" number (adds an element); A4 whoever pressed the Duo button.
- Recommendation: A2. Lucy's role finisher stays Lucy's, since kill-stealing is the joke. Tempest Bloom built with Tally: return.
- Blocked: the C5 counting change; the route level's tally moment.

**B. The tally in the Hearth memory**
- Question: Should the counter also show in the Hearth's segments 3 and 4, where both sisters fight?
- Context: as built, the tally first appears in The Trail and fades at its end, so it has no setup on screen. Segment 3 is the bragging contest ("You both did."). No time cost. One more HUD item during John's lesson.
- Options: (a) yes, segments 3–4: eligibility per level by deployed units, The Hearth no longer excluded; (b) no, The Trail only, as built; (c) B3, solo scores in River/Ridge carried into The Trail (new cross-mission state; over budget).
- Recommendation: (a), checked in the timed pacing run; (b) if the counter clutters segment 3.
- Blocked: the eligibility part of C5 (small).

**C. The Duo damage bug outside the tally**
- Question: Open a separate core plan so Duo damage raises `onUnitDamageDone`?
- Context: no Duo's damage reaches that event today, so mission stats, John's Wrath and Blood Debt, Mark's Atman Barrier and barks ignore it (fact 1). Fixing it is core (`CombatLevelRunHandler` or `UnitsCooperationHandler`) and changes those passives' behaviour. The tally doesn't need it: the bracket works without it.
- Options: (a) a separate plan now (TD, Tier 3); (b) log it in the backlog for after the pacing check; (c) leave it.
- Recommendation: (b). It's a real bug with balance side effects, and fixing it before the timed check could shift numbers the check is meant to read.
- Blocked: nothing in the tally.

## Docs to update if approved

- GDD [family-systems.md](../../design/gdd/family-systems.md): a short "Sisters' tally" subsection (onboarding only, "**On `thj/onboarding`:**") with the attribution rule under a new rule prefix defined in [overview.md](../../design/gdd/overview.md) › How to read (proposed `ST-1` to `ST-3`: what counts, together kills, eligibility). Or [missions-structure.md](../../design/gdd/missions-structure.md) if THJ prefers the tally as mission UI; one home only.
- [First-hour design](2026-10-25-onboarding-first-hour-design.md): the "Sisters' tally" new-tech row and the Running joke row (as built + this rule; Hearth if B2).
- [Tally tech plan](2026-11-08-sisters-tally-tech.md): acceptance criterion on what counts, a C5 chunk (coordinator).
- `glossary.md` "Sisters' tally" (narrative, if the definition changes for B2).
- Backlog entry for question C (coordinator), if (b).
- No grids changed; nothing to render.
