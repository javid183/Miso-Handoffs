# Lucy's Cyclone, round 2: player-facing texts (proposal)

Size: S    Tier: 2 for ability text in the established voice; Tier 3 for "Eye of the Storm" and any new on-screen term    Assigned to: miso-narrative
Branch: `thj/cyclone` (scope: this branch)
Status: waiting on THJ
Inputs: `plans/2026-11-17-cyclone-round2-design.md`, `plans/2026-11-17-cyclone-round2-tech.md` (C5). Mechanics as decided by THJ; nothing here changes them.

## Style read from the current strings

- Ability descriptions are present-tense, subject dropped, one to three short sentences, about 100 to 180 characters: "Shoots a fire ember followed by sidewinders at an enemy." The current Cyclone text is 182 characters, the Steer 155.
- Unlock texts are one sentence, "Lucy's X does Y.": "Lucy's Fire Embers apply Burn." "Lucy's Cyclone applies Weak to every enemy it hits."
- Already on screen and kept: **arms** ("enemies on its arms"), **beside it** ("hits those beside it"), "3 enemy turns", "one cell", "Once a turn."
- No AP in descriptions except Encore's "(2 AP)". I follow the majority and leave AP out.
- New terms kept to one: **Whirl**, used as a verb ("then it Whirls"). The log already says "Whirl", so the word the player reads in the tooltip matches the log. "Carried" matches the log's "carried N".

## Strings

Recommended option first. Lengths are approximate character counts.

| # | Where it appears | Current text | Proposed text | Notes |
| --- | --- | --- | --- | --- |
| 1 | Steer title (`Lucy_Ability_Steer.asset` › `title`) | Steer | **Steer** (no change) | Short and plain, and already in the log, tests and setup tool. Alternatives, if THJ wants more storm: "Ride the Wind" (playful, Lucy's age), "Eye of the Storm" (see §Name). I'd keep Steer: it's the button's verb |
| 2a | Steer description (`Lucy_Ability_Steer.asset` › `description`) | Moves the Cyclone up to 3 cells, not through walls or enemies. Then it pulls enemies on its arms one cell in, without hitting them. Once a turn. | **Glides the Cyclone up to 3 cells, carrying the enemies beside it. Then it Whirls. Once a turn.** (~95) | Recommended. What it does in three beats; the cursor shows which cells are reachable, so the blocking rule doesn't need words |
| 2b | same | same | Glides the Cyclone up to 3 cells. Enemies beside it are carried along: shoved ahead, dragged beside, following behind. Then it Whirls. Once a turn. (~150) | Spells out the three rider cases. Same length as today; teaches more, reads slower |
| 2c | same | same | Moves the Cyclone up to 3 cells. Enemies beside it ride along and land at the end. Then it Whirls. Once a turn. (~110) | Says "land once" outright (the Watch timing). Plainer, less storm |
| 3a | Steer hint line (onboarding / first-use hint; where it's shown is the implementer's call) | none | **Steer carries the enemies beside it, then it Whirls.** | Recommended. Uses "carries", like the description and the log ("carried N") |
| 3b | same | none | Steer drags enemies beside it, then it Whirls. | The working line. "Drags" has more feel, but it's a second verb for one rule, and only the side enemies are really dragged |
| 3c | same | none | Enemies beside the Cyclone ride along when you Steer it. | Puts the enemies first; leaves the Whirl for the description to teach |
| 4a | Cyclone description (`Lucy_Cyclone_Ability.asset` › `description`) | Summons a Cyclone for 3 enemy turns. On cast and after each enemy turn, it pulls enemies on its arms one cell in, then hits those beside it. Enemies can't pass or shoot through it. | **Summons a Cyclone for 3 enemy turns. It Whirls on cast and after each enemy turn: pulls enemies on its arms one cell in, then hits those beside it. Most enemies can't walk or shoot through it.** (~185) | Recommended. Defines "Whirl" where the player first meets it, so the Steer's "then it Whirls" reads. **Fixes a now-false line:** heavies walk through and burst it, and only enemy shots are stopped (the family's arrows pass). "Most" leaves room for the burst without spelling it out |
| 4b | same | same | Summons a Cyclone for 3 enemy turns. It Whirls on cast and after each enemy turn: pulls enemies on its arms one cell in, then hits those beside it. It blocks enemy paths and shots; the heaviest burst it. (~200) | Names the burst on Lucy's side too. Longest; "heaviest" is a soft hint, not a term |
| 4c | same | same | Summons a Cyclone for 3 enemy turns. On cast and after each enemy turn, it Whirls: pulls enemies on its arms in, then hits those beside it. (~140) | Shortest. Drops the blocking sentence; only if the tooltip is cramped |
| 5 | Cyclone Power, skill-tree `description` (`Unit_Lucy.prefab` node 5) | Lucy's Cyclone hits harder. | **Lucy's Cyclone hits harder: 4, then 5 times her Damage.** | "Damage" is the stat's on-screen title (`StatAttributes` DMG). The base without the node is 3 times |
| 6 | Cyclone Power, skill-tree `upgradeDescription` | Each upgrade increases Cyclone damage. | **Each level adds one more times Lucy's Damage to every Cyclone hit.** Or simpler: **Each level makes every Cyclone hit stronger.** | Second line is safe if the panel shows the numbers elsewhere |
| 7 | Cyclone Power level lines, if the panel can show one per level | none | Without it: **Cyclone hits deal 3 times Lucy's Damage.** · Lv 1: **4 times Lucy's Damage.** · Lv 2: **5 times Lucy's Damage.** | `SkillTree.NodeData` has only `description` and `upgradeDescription`, no field per level. These fit only if the UI builds the line from the level; otherwise use rows 5 and 6. Mapping read from `CyclonePower_HitIsThreeFourFiveTimesDamage`: level 0 = 3, 1 = 4, 2 = 5 (node has 2 upgrades). "Lucy's Damage" stays true when her Damage stat grows; a flat "hits for 4" would not |
| 8 | Howling Gale, run upgrade (`RU_LucyCycloneWeak.asset` › `description`) | Lucy's Cyclone applies Weak for 2 turns to every enemy it hits. | **No change.** | "Every enemy it hits" already covers cast, Steer, end-of-turn Whirls and the burst |
| 9 | Howling Gale, unlock list (`UnlockableSet.asset`, id `LucyCycloneWeak`) | Lucy's Cyclone applies Weak to every enemy it hits. | **Lucy's Cyclone applies Weak for 2 turns to every enemy it hits.** | Same sentence as the run upgrade, so the two screens agree. Optional: the other unlock lines ("Mark's Command applies Weak to enemies.") don't give durations either |
| 10a | Burst note, enemy side (Masher Goblin, Goblin Queen: enemy info or hover line; where it's shown is the implementer's call) | none | **Walks through Lucy's Cyclone and bursts it, taking one hit.** (~60) | Recommended. Short; the hit on the others beside it shows in the preview |
| 10b | same | none | Walks through Lucy's Cyclone and bursts it: it hits this enemy and every enemy beside it once. (~95) | Complete rule, for an info panel with room |
| 10c | same | none | Too heavy to stop: bursts Lucy's Cyclone by walking through it, taking one hit. | More voice. "Heavy" reads as flavour here, not a tag |
| 11 | Tempest Bloom, skill-tree `description` (outside this task, noticed) | [Synergy] Hitting Lucy's cyclone with a Bergson's projectile makes it split and spread. | [Synergy] Hitting Lucy's Cyclone with a Bergson's projectile makes it split and spread. | Capital C only, for consistency. Apply only if the implementer is editing that prefab anyway |

Not mine, already set by the tech plan: the log line "Whirl · Lucy: carried N, pulled N, hit M".

## Name: "Eye of the Storm" (suggestion only)

It could name the carry rule (what's beside the Cyclone moves with it), or a later upgrade. A design label only, not on screen, until THJ picks it. Options if a name is wanted on screen:
- **Eye of the Storm**: classic and readable; the calm centre that holds what's caught.
- **Caught in the Wind**: plainer, says what happens to the enemies.
- **Storm's Hold**: shorter, firmer, but it suggests the "hold" rule THJ didn't choose (Q4).

## Glossary

Updated `glossary.md` with a new **Lucy's Cyclone** section: Gust marked retired (THJ's decision); Whirl, beside it, arms, carry, burst marked proposed; heavy and cross listed as design words to keep off screen; Eye of the Storm as a suggestion only.

## Needs THJ

1. Pick 2a/b/c, 3a/b/c, 4a/b/c, 10a/b/c (recommended: a in each).
2. Approve "Whirl" as an on-screen verb and "carried" over "drags".
3. Confirm the Cyclone line "Most enemies can't walk or shoot through it" (replaces a line that is no longer true).
4. Where the hint line (3) and the burst note (10) show: no field for either exists today; implementer or UX to say.
5. Eye of the Storm: use it on screen, keep it as a design label, or drop it.
