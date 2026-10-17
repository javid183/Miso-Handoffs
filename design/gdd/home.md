# Home

Owner: game designer (THJ approves) · Scope: `thj/home-test` · Checked against: [`demo-spec.md`](../demo-spec.md) and [`tech/home-system.md`](../../tech/home-system.md), 2026-10-16 (branch code not read: no git access this session) · Mirror: Claude Doc "Miso — Game Design", tab Home · Up: [Overview](overview.md)

Managing the Home as a Family is the fourth USP: between missions the family lives, works and grows together, and what happens at Home shapes the next fight. The Home system exists only on `thj/home-test`, as a demo of one chapter. **The [Demo Spec](../demo-spec.md) is the home of its rules and numbers (D-047);** this page is the map. It names the parts, states the few rules that tie Home to the rest of the game, and links to where each part is specified.

## Rules that tie Home to the game

- **HO-1.** A chapter is one Great Moon cycle: a prologue of tutorial missions, then 7 days ending at the full moon in the chapter's dungeon, the Goblin Queen's Warren. *Demo*
- **HO-2.** Home runs one day at a time: Dawn, Morning, Afternoon, Dusk at the Dining Table, then Night. The day's simulation is deterministic, so the same plan always gives the same result. *Demo*
- **HO-3.** Each slot, the player seats characters at stations. Each character has one clear Home identity (an affinity per station), so who goes where matters. *Demo*
- **HO-4.** A sortie sends a squad from the map table; the others stay home and keep working. Side missions seat 3, the dungeon 4 ([Missions and structure](missions-structure.md) MI-26). *Demo*
- **HO-5.** Home builds the three layers of power ([Overview](overview.md#three-layers-of-power)): permanent (Lessons, Home Upgrades, gear, Bond), per sortie (the send-off meal, Omens) and per dungeon run (routes, in-run upgrades, relics, rations). *Demo*
- **HO-6.** Bond between two family members unlocks their pass-by, Duo and Synergy at set levels ([Family systems](family-systems.md) PB-4). *Demo*
- **HO-7.** The first member downed in a sortie comes home Wounded: no sortie or Yard seat until they recover after 2 Dawns (sooner with Care), and they join the dungeon at 50% HP ([Combat rules](combat-rules.md) CR-26). *Demo*
- **HO-8.** On `main` there is no Home system; the hub sells family stats and gear between missions ([Progression and economy](progression-economy.md) PR-33). *Built*

## The parts of Home

| Part | What it does | Specified in the Demo Spec |
| --- | --- | --- |
| Day loop | Dawn tick, Dawn plan, sortie, Morning and Afternoon resolve, Dusk report, Night | Day loop state machine |
| Characters at Home | Each playable character's Homestead, Kitchen, Study, Yard and Night talent. Mary cooks, Uncle Ben runs the Workshop, Kevin does chores | Roster and missions › Character affinities |
| Homestead | Plots, tending, hens and eggs | Homestead and Kitchen |
| Kitchen | Dishes from tagged ingredients; the send-off meal and dungeon rations | Homestead and Kitchen › Kitchen rules |
| Study | Reading items that reveal missions, recipes and resources | Study, Workshop and Home Upgrades |
| Workshop | Weapon upgrade orders that take Dawns to finish | Study, Workshop and Home Upgrades › Workshop rules |
| Home Upgrades | Room tiers that raise family stats or capacity | Study, Workshop and Home Upgrades › Home Upgrades |
| Yard Lessons | Training that raises family stats | Yard, Bond and Family Event |
| Bond | Pair levels that unlock pass-by, Duos and Synergies | Yard, Bond and Family Event › Bond |
| The Picnic | The Family Event, bought with a Family Skill Point | Yard, Bond and Family Event › The Picnic |
| Night | Stargazing (star patterns, Omens), Hearth time (Fireside Talk), Vigil | Night |
| Omens | Night signs that change the next day's missions | Night › Omens |
| Dungeon | Threads cut by side missions, the Warren's route, attempts | Dungeon and Wounded |
| Wounded | Recovery and Care | Dungeon and Wounded › Wounded |
| Prologue and schedule | The three tutorial missions, the starting state, the 7-day schedule | Prologue; Starting state and schedule |

How it is built (milestones Home M0–M9, all built and committed): [`tech/home-system.md`](../../tech/home-system.md); history in `build-log.md`.

## Where Home touches other systems

| Home gives | To | Rule |
| --- | --- | --- |
| Send-off meal effects, Omens, Wounded members at 50% HP in the dungeon, the "From Home" banner | Combat at level start | [Combat rules](combat-rules.md) branch differences |
| Bond levels | Pass-by, Duos, Synergies | [Family systems](family-systems.md) PB-4 |
| Lessons and Home Upgrades in place of the gold stat panels | Family stats | [Progression and economy](progression-economy.md) PR-13 |
| Weapon orders | Gear | [Progression and economy](progression-economy.md) PR-18 |
| Sortie pay (drops per level, XP) | The wallet | [Progression and economy](progression-economy.md) PR-25 |
| The prologue, side missions and the Warren | Missions | [Missions and structure](missions-structure.md) MI-26 |
| Character talents at Home | Character sheets | [Characters](characters/README.md) (each sheet's Home section) |

## Open questions

The Demo Spec keeps the full list (Demo Spec › Open questions for this spec). The ones that reach beyond Home:

1. **Q1.** The Fireside payoff: what else can a pair earn (today: first Duo free, first Family Role free, or FP cap +2)?
2. **Q2.** Does the full game keep resetting Lessons, Home Upgrades and weapon levels at each new cycle?
3. **Q3.** Should the dungeon take 4 of the 5 characters, or the whole family?
4. **Q4.** HP bonuses from Lessons and Home Upgrades multiply each other. Intended, or should they add?
5. **Q5.** The FTP values at Home assume a small FTP cap; they need the real cap ([Combat rules](combat-rules.md#open-questions) Q2).

## Related

[Demo Spec](../demo-spec.md) · [`m9-readability.md`](../m9-readability.md) · [`tech/home-system.md`](../../tech/home-system.md) · [Missions and structure](missions-structure.md) · [Glossary](../../glossary.md)
