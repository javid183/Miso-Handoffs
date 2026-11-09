# Missions and structure

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (every mission level prefab read from the live project); MI-27 from the build report, on `main` @ `dc64f974a`, 2026-10-24 · Mirror: Claude Doc "Miso — Game Design", tab Missions and structure · Up: [Overview](overview.md)

The campaign is a graph of missions. Each mission is one or more combat levels played in a row, sometimes with a choice of route and an enemy-free safe room on the way. The family's HP, FTP, items and run upgrades carry through a mission and reset when it ends. The design's larger loop (chapters, each with a main dungeon and a deadline) exists only in the Home demo so far.

## Campaign

- **MI-1.** At the start only M1 is open. A mission opens when every mission before it in the graph is complete (all gates are AND gates). *Built*
- **MI-2.** Completed missions stay open and can be replayed for full rewards ([Progression and economy](progression-economy.md) PR-23). The order of completion is saved. *Built*
- **MI-3.** Two characters join through missions: Mark after "No More Waiting", Toba after "Into the Rootwell". John, Linda and Lucy are there from the start. A mission's fixed members, and characters a level places itself, play even before they have joined (Mark in his intro; Toba in M9 and in every level of "Into the Rootwell" after his duel). *Built*
- **MI-4.** The design's loop: each chapter sets a main dungeon (a multi-level mission done in one run) and a deadline; side missions are optional preparation ([`vision.md`](../../vision.md)). *Planned* (on `main`; no chapters or deadlines there). **On `thj/home-test`:** built as the moon cycle and the Warren ([Home](home.md)). *Demo*
- **MI-5.** M8 to M14 are unreachable on `main`: the unlock check never passes a gate with no input, so M8, M9 and M11 never open, and M10 and M12–M14 need M9. MX is not in the graph at all. Intended for now: they are a later chapter, left unwired and *Planned* until it is designed; their levels stay as maps and chunks (D-196)

```
 M1 John's Map
  ├─► M2 Ryker is lost ─────┐
  └─► M5 The Healer ────────┤ both
                            ├─► M3 A Wolf's Blood ─────┐
                            └─► M3 No More Waiting ────┤ both
                                                       ├─► M4 Into the Rootwell
                                                       └─► M6 The Arcanum ──► M7 In My Father's Arms

 (gate with no input) ──► M8 The First Path · M9 In the Heart of the Forest · M11 Sisters
 M9 ──► M10 The Sacred Tree's Parasite · M12 The Mountain Deev · M13 Uncharted Lands · M14 Hegmataneh
 MX Another Old Bergson House: not in the graph
```

Source: `Resources/Game Data.asset` (`missionDependencyGraph`), `Core/Managers/GameHandler.cs` (`IsMissionUnlocked`), `unlockedAfterMission` on `Unit_Mark.prefab` and `Unit_Toba.prefab`.

## Missions

| # | Mission | Roster: fixed + free | XP | Gold | Material pick | Items |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | John's Map | John, Lucy | 40 | 5 | — | — |
| M2 | Ryker is lost | Lucy, John | 40 | 5 | Steel 1 | 2 / 1 |
| M5 | The Healer | John, Linda, Lucy | 90 | 5 | Timber 1 | 2 / 0 |
| M3 | A Wolf's Blood | John, Linda | 65 | 10 | Timber 1 | 2 / 2 |
| M3 | No More Waiting | Mark, Lucy | 60 | 10 | Fabric 1 | 2 / 2 |
| M4 | Into the Rootwell | John, Linda, Lucy (+ Toba, placed in every level after his duel) | 120 | 20 | All 4 materials, 1 each | 3 / 4 |
| M6 | The Arcanum | John + 2 free | 90 | 15 | 2 of the 4 materials, 1 each | 2 / 1 |
| M7 | In My Father's Arms | John + 2 free | 165 | 20 | 2 of the 4 materials, 1–2 each | 2 / 1 |
| M8 | The First Path | 4 free | 60 | 12 | 2 of: Gold 5–10, materials 1–3 | 3 / 3 |
| M9 | In the Heart of the Forest | Linda, Toba | 30 | 5 | 2 of: Gold 5–10, Stone 2–3, Timber 1–2, Fabric 1–2 | 2 / 1 |
| M10 | The Sacred Tree's Parasite | 3 free | 50 | 15 | 3 of: Gold 5–15, materials 2–3 | 2 / 1 |
| M11 | Sisters | Linda, Lucy | 20 | 5 | 3 of: Gold 7–12, Fabric 1–3, Timber 1–2, Steel 1–2 | 3 / 2 |
| M12 | The Mountain Deev | John, Linda, Lucy | 50 | 15 | 3 of: Gold 5–15, materials 2–3 | 2 / 1 |
| M13 | Uncharted Lands | John, Linda, Lucy | 50 | 20 | 3 of: Gold 5–10, materials 1–3 (Stone 1–4) | 3 / 4 |
| M14 | Hegmataneh | John, Linda, Lucy | 50 | 20 | as M13 | 3 / 4 |
| MX | Another Old Bergson House | 3 free (not Toba) | 30 | 10 | 3 of: Gold 0–5, Steel 1, Fabric 1–3, Timber 1–3 | 2 / 1 |

"Material pick" is drawn at completion (PR-20); Gold in a pick breaks the design rule (PR-24). "Items" are the family's starting uses of its two items, the Health Potion and the Family Trinket ([Combat rules](combat-rules.md) CR-30). Source: `Content/Levels/M*.asset` (`missionName`, `missionRoster`, `completionXPReward`, `completionGoldReward`, `resourceCollectionCount`, `collectableGResources`, `initialItemsAvailability`).

| # | Levels, in order | Enemy tier | Deploy slots | Notes |
| --- | --- | --- | --- | --- |
| M1 | Level1-C1_TArtEx → Level1-C1-2 → Level1-C2 | Tutorial | 0 | Level 2 places Linda alone. M1's story is cut; the levels stay as maps (D-169) |
| M2 | LevelLucyJohn-C1 → C2 → C3 | Early | 0 | John and Lucy against Archers and Dark Claws; enemies act first in C2 |
| M5 | LevelE1-C1 → C2 | Early | 0 | John, Linda and Lucy |
| M3 Wolf | LevelLindaJohn-C1 → C2 | Early | 0 | John and Linda; enemies act first in C1; C2 adds Dark Worms |
| M3 Mark Intro | LevelMarkIntro-C1 → C2 → C3 | Early | 0 | C1: Lucy alone takes the Heavenly Sword relic to an altar, then survives 3 turns of Dark Claw waves. C2: Mark alone reaches an exit (or defeats every enemy). C3: both, defeat all |
| M4 | LevelDomFight → Level2-C1-TArtEx → Divine Relic room (copy) → Level2-C2 → Level2-C3-1 → Level2-C3-2 → Level3-C1 | Standard | 0 | Toba's duel first (MI-25), then Toba fights with the family. C1-TArtEx: defeat all and reach the 4 exit tiles. C2 and C3-1: the Whitemother stag must survive (C2 has no loss when every hero is down, Q12). C3-2: escort the new Pathmother to an exit. The Goblin Queen last (MI-23). Labels to fix to (1/6)–(6/6); the relic room becomes the 2-relic choice room (D-197, D-186) |
| M6 | LevelE2-C1 → Divine Relic room *or* Run Upgrade room → LevelE2-C2 → Healing Room → LevelE2-C3 | Standard | 3 | The only route choice (MI-14). C3 keeps 1 of 2 Archers and 1 of 2 Dark Claws (MI-19). Cut as a mission; the levels stay as maps (D-169) |
| M7 | LevelE3-C1 | Standard | 3 | Archers, Dark Claws and a Masher |
| M8 | LevelM1-C1 → C2 → C3 | Standard | 4 | Up to 11 enemies a level, with Shamans, Black Claws and a Masher |
| M9 | LevelDomLinda-C1 → C2 | Standard | 0 | Linda and Toba; a Masher in each |
| M10 | LevelM2-C1 | Standard | 3 | The Goblin Queen again, at 150 HP, with four spawners; enemies act first (Q13) |
| M11 | LevelLucyLinda-C1, then 7 test levels with no links | Standard | 0 | Plays one level: 10 Dark Claws and 2 Shamans (Q6) |
| M12 | LevelMountainDeev | Standard | 0 | The Mountain Deev alone; enemies act first (MI-24) |
| M13 | Test_Level_ABK_01 → 01-2 → 02 → 03 | Standard | 0 | Test levels; they also place Mark and Toba |
| M14 | Test_Level_ABK_04 → 05 → 06 → 07 | Standard | 0 | Test levels, plus one unlinked test level |
| MX | LevelE4-C1 twice | Standard | 3 | Plays one level (Q6) |

Some levels give a boost when they load: M2's C1 and C2 and both levels of "A Wolf's Blood" add 3 FTP; C2 of "No More Waiting" adds 5 FTP and its C3 heals 20 HP; M4's Level2-C3-2 adds 5 FTP and heals 7 HP; M1's level 3 heals 30 HP. Many levels also hold Corruption spawners, which add a Dark Claw every 3 turns (one alive per spawner), and hazards such as spider webs and exploding mushrooms. Source: each mission's `levelDependencyGraph` and its level prefabs under `Content/Levels/` (`enemyTier`, `Unit_Placeholder` instances, placed units, objectives, turn-order overrides); `Core/Levels/Runtime/LevelStartFPFiller.cs` (level-start boosts); `Features/Hazards/Corruption Pool/CP_Spawner/CP_Spawner.prefab`.

## Anatomy of a mission

- **MI-6.** A mission sets a roster: fixed members, who always go, and free slots the player fills from the characters who have joined. A mission can also exclude characters (MX excludes Toba). The squad is 2 to 4. *Built*
- **MI-7.** There is no deployment phase. Most levels place their heroes themselves (33 of the 45 levels have no deploy slots); the others have 3 or 4 slots, which roster members fill in order. Characters a level places also play, in the roster or not, and a roster member left without a slot sits out that level. *Built* (Q3, Q8)
- **MI-8.** A mission sets its completion rewards (PR-20) and its starting items (CR-30). *Built*
- **MI-9.** A mission can play an opening scene and a completion scene (shown at Home), and sets the Home's state after it is completed. *Built*
- **MI-10.** A mission has no main/side flag, deadline, replay limit or difficulty of its own; difficulty is set per level (MI-16). *Built*

Source: `Core/Levels/Runtime/Mission.cs`, `Core/Managers/CombatLevelRunHandler.cs` (`FillRosterSlots`).

## Routes and the mission map

- **MI-11.** A mission's levels form a small graph. Winning a level loads the next one; when there is a choice, the mission map opens and the player picks. *Built*
- **MI-12.** Taking one branch closes its siblings (shown as Missed); levels both branches lead to stay open. *Built*
- **MI-13.** No route progress is saved. After a loss or leaving, the next attempt starts again at the first level. *Built*
- **MI-14.** Only M6 offers a choice today: the Divine Relic room or the Run Upgrade room. Random route gates exist in code but no mission uses them. *Built*
- **MI-15.** **On `thj/home-test`:** the Warren's route branches between a Rest Room and an Upgrade Room and hides a Relic Room; the family can retreat home from the mission map ([Home](home.md)). *Demo*

Source: `Core/Levels/Runtime/MissionRouteProgress.cs`, `MissionTracker.cs` (`ShouldShowMissionMap`).

## Levels

- **MI-16.** Each level sets its enemy tier ([Combat rules](combat-rules.md) CR-32). *Built*
- **MI-17.** By default a level is won by defeating every enemy and lost when every family member is down. A level can replace these objectives. *Built*
- **MI-18.** Objectives are built from the conditions below. They can be grouped (all, any, or a number of them) and queued as stages, each stage starting when the previous one is done. The win is checked before the loss. Tiles that a visible win objective needs are highlighted on the grid. *Built*
- **MI-19.** A level can keep a random subset of its enemies or objects (variant groups); the draw holds for the whole attempt. *Built* (only M6's last fight uses it)
- **MI-20.** A level can open with a choice between sets of objectives, with a preview. *Built* (unused)
- **MI-21.** Between levels of a mission, HP carries over (CR-24), and members who fell come back at 20% of max HP. FTP (CR-12), item counts (a restart rewinds them, CR-31), run upgrades and relics (PR-26, PR-31) also carry over. Statuses, AP and cooldowns reset. *Built*

| Condition | Met when |
| --- | --- |
| Units alive or dead | A faction has a set number of units alive or dead |
| Unit dies | A given unit dies |
| Entities destroyed | All, any or a number of listed objects are destroyed |
| Entities captured | A faction collects listed objects |
| Tiles occupied | A faction stands on all, any or a number of listed tiles |
| Unit on tiles | A given unit stands on any of the listed tiles |
| Turn reached | A number of turns has passed, counted from when the objective first checks; drives the turn-limit display |
| Never | Never (a placeholder) |

"Protect a unit" and "defeat the boss" are built from "Unit dies" in a loss or win group. Source: `Core/Levels/Runtime/LevelObjectives.cs`, `LevelObjectiveConditions.cs`, `CombatLevel.cs`, `Content/Levels/LevelBase.prefab`.

- **MI-27.** Enemies start each level Unaware unless the level sets **"all enemies start alert"** ([Enemies](enemies.md) EN-12, EN-17). The setting is for levels where the enemies must come from turn 1: boss fights, protect and escort, survive-N-turns and some reach-the-exit levels. A level can also add a sight bonus and an alert-range bonus to every enemy in it (EN-17); none does yet. The levels that set "all enemies start alert" are listed below. *Built* (D-154, D-163)

| Mission | Level | Why |
| --- | --- | --- |
| M3 Mark Intro | LevelMarkIntro-C1 | Survive 3 turns of Dark Claw waves |
| M3 Mark Intro | LevelMarkIntro-C2 | Mark alone leaves the area to reach Lucy |
| M3 Mark Intro | LevelMarkIntro-C3 | Survive for 3 turns |
| M4 | LevelDomFight | Toba's duel (MI-25) |
| M4 | Level2-C2 | The Whitemother stag must survive |
| M4 | Level2-C3-1 | Escort the fawns; the Pathmother must survive |
| M4 | Level2-C3-2 | Escort the new Pathmother to an exit |
| M4 | Level3-C1 | The Goblin Queen (MI-23) |
| M10 | LevelM2-C1 | The Goblin Queen again (MI-23) |
| M12 | LevelMountainDeev | The Mountain Deev (MI-24) |
| — | LevelHomeDefence | "Defend Home" |

Bosses are always alert in every level, flagged or not: the Goblin Queen, the Mountain Deev and the duel's enemy Toba (EN-17). Not flagged for now (D-163): the `Level1-C3` family ("Allies must survive") and `Level2-C1-TArtEx` (defeat all and reach the exit). Every other level, the `LevelM1-*` and `LevelE*` levels included, starts its enemies Unaware. Source: `LevelAlertSettings` (`allEnemiesStartAlert` 1) on the root of each level prefab above, under `Content/Levels/` (`Generic Levels/FamilyLevels/MarkIntro/`, `Level2/`, `Level3/`, `Generic Levels/Medium/M2/`, `Generic Levels/Medium/MountainDeev/`, `Generic Levels/Easy/`), committed in `dc64f974a`; [`reports/enemy-alert-c3.md`](../../reports/enemy-alert-c3.md).

## Safe rooms

- **MI-22.** Safe rooms are enemy-free levels on a mission's route. The family leaves by stepping onto the exit. *Built*

| Room | Name in game | Offers |
| --- | --- | --- |
| Healing Room | Anahita's Ashiyan | The first member to reach the shrine heals the whole family, once: 0.5 × the HP cap stat, a full heal in effect (Q11) |
| Run Upgrade Room | Daryani's Shop | The altar: pick 1 of up to 3 run upgrades, free (PR-27) |
| Divine Relic Room | Mithra's Gift | The Heavenly Sword relic (PR-30) |

**On `thj/home-test`:** the Warren's Rest Room heals 10% of max HP and is where rations are eaten ([Home](home.md)). Source: `Content/Levels/DungeonSafeRooms/*.prefab`, `Core/Levels/Runtime/SafeRoomFunction.cs`.

## Bosses and special fights

- **MI-23.** The Goblin Queen is fought in the last level of "Into the Rootwell", and again in M10 at 150 HP. In both levels the enemies act first and a boss health bar shows; in M4 her death triggers Family Super Time. Her rules: [Enemies](enemies.md) EN-6. *Built*
- **MI-24.** The Mountain Deev is fought in "The Mountain Deev" (M12), a single level where the enemies act first and the Deev's Summon is removed. Its rules: [Enemies](enemies.md) EN-7. *Built*
- **MI-25.** "Into the Rootwell" opens with Toba's duel. Toba (60 HP there) fights the family as a stranger and acts first; the level makes his faction hostile to the family. He yields instead of dying when his HP drops below 30%. He then fights alongside the family for the rest of the mission and joins after it. *Built*

Source: `Content/Levels/Level3/Level3-C1.prefab`, `Generic Levels/Medium/M2/LevelM2-C1.prefab`, `Level2/LevelDomFight.prefab` (`healthThreshold` 0.3, faction relations, turn order), `Core/Entities/Runtime/Boss/BossDomFight.cs`, `Features/Player/Dom/Prefabs/Unit_TobaEnemy.prefab`, `Resources/Factions/DomAsEnemyFaction.asset`.

## The Home demo's missions

- **MI-26.** **On `thj/home-test`:** a prologue of three missions (M1, M2, M3 "A Wolf's Blood", in that order, skipping M5; `build-log.md` › Home M7), then one 7-day moon cycle. Side missions take 3 seats, can be played once each, take one day, and two have day windows. The Goblin Queen's Warren is open from Day 1 and forced on Day 7. Sortie missions are separate assets that pay through Home. Rules and numbers: [Demo Spec](../demo-spec.md). *Demo*

## The sisters' tally

- **MI-28.** **On `thj/onboarding`:** the sisters' tally, a running joke between Lucy and Linda. Each sister's kills count, last hit = 1. A kill the sisters make together (their Duo, Tempest Bloom) counts +1 for each; Lucy's Family Role finisher counts for Lucy. There is one tally per mission and it is not saved. It shows in levels with both sisters (per-level eligibility, so Hearth segments 3 and 4 show it, with their own count), as a HUD counter at top centre. At mission end it shows as two stat rows ("Sisters' Tally:", Linda's count and portrait, then Lucy's), and the MVP row is hidden while they show. At The Trail's animal pile the counter shows alone with "Still counting?", then fades, then "...No." The fade is saved. A return step is built but not placed: it waits for the first-trigger framed beat, so M4 shows no tally. One switch in code (`SistersTally.Enabled`) turns the whole feature off. Design: [first-hour design](../../plans/onboarding/2026-10-25-onboarding-first-hour-design.md), [attribution design](../../plans/onboarding/2026-11-08-sisters-tally-attribution-design.md); decisions D-444 to D-454. *Built*
  - Known limits: no Duo damage reaches `onUnitDamageDone` (backlog `duo-damage-events`, D-451), so mission stats and MVP miss Duo hits; Bloom copies that land after Linda's ability ends count for no one; the Goblin Queen's finishing move counts for no one; M1's `Level1-C2` also shows the tally (D-452).

Source: `SistersTally` feature folder (counting, HUD counter, `SistersTallyResultRow`), `SessionEndPanel.prefab`, `LevelBase.prefab` (excluded-level list), `CombatLevelUIManager` (HUD extra-panel hook).

## Deferred and dropped

| Item | State |
| --- | --- |
| Random route gates (random branches with weights) | Code only; no mission uses them |
| Objective choice at level start (MI-20) | Code only |
| Retreat home from a mission | `thj/home-test` only, for the dungeon |
| M11, M13 and M14 content | Test levels standing in |

## Branch differences

- **On `main`:** the campaign graph above; no chapters, days or deadline.
- **On `thj/onboarding`:** the sisters' tally (MI-28).
- **On `thj/home-test`:** the prologue and moon cycle (MI-26), the Warren's route (MI-15) and Rest Room, retreat, and sortie rewards that differ (PR-25).

## Open questions

1. **Q1.** M8 to M14 can't be reached on `main` (the gate before M8, M9 and M11 has no input), and MX is outside the graph. Cut content, a later chapter, or a wiring slip? **Answered:** a later chapter; leave unwired, mark Planned (D-196).
2. **Q2.** "No More Waiting" is required for M4 and M6 (both M3s feed one AND gate); [`reward-balance.md`](../reward-balance.md) says Mark's intro gates nothing. Which is intended? **Answered:** superseded: No More Waiting is cut as a mission (D-169); the opening graph is D-170's.
3. **Q3.** M1's roster is John and Lucy, but its second level places Linda alone (no deploy slots) and its third places all three. Is this Linda's introduction? It also gives Linda a share of M1's XP (PR-5). **Answered:** superseded: M1's story is cut; the opening is the Hearth prologue, then The River and The Ridge (D-169, D-170).
4. **Q4.** "Into the Rootwell" has 6 fights and a copy of the Divine Relic room (a second Heavenly Sword). Its labels run (1/5) to (5/5) with a "(4.5/5)" in between. Fix the labels, and keep the relic room? **Answered:** fix the labels to (1/6)–(6/6); the relic room becomes the 2-relic choice room (D-197, D-186).
5. **Q5.** M6: the map shows LevelE2-C2 twice (a false choice), and the Healing Room is forced. `reward-balance.md` describes a different route. Which is intended? **Answered:** superseded: M6 is cut as a mission (D-169).
6. **Q6.** M11's levels have no links, so only the first plays; MX lists the same level twice, and it ends after one. Fix?
7. **Q7.** Text slips: the M2 file says "Ryler" and the title "Ryker"; "No More Waiting" ends with a space (it is also the save key); the M12–M14 titles include the file prefix ("M12 - The Mountain Deev"); M12–M14 reuse other missions' descriptions; M9's description says "Dom"; mission number 3 is used twice and MX is −1. Level labels don't match the routes (LevelE2-C3 says "(2/3)", MX's level "(1/2)"), and C3 of "No More Waiting" shows a literal "{0}" in its objective.
8. **Q8.** Most levels place a fixed cast instead of using deploy slots, so the roster and who actually plays can differ ("No More Waiting", M13, M14). Should levels use deploy slots, as many as the largest squad that can reach them?
9. **Q9.** Toba's duel: answered from the data (the level makes the stranger hostile; Toba yields below 30% of 60 HP and acts first). Close, or tune the threshold?
10. **Q10.** Chapters, a main dungeon and deadlines: planned for `main`, or only through Home?
11. **Q11.** The Healing Room heals 0.5 × the HP cap stat (9999), a full heal in effect; the Demo Spec's Rest Room heals 10%. Which size is intended for `main`?
12. **Q12.** Level2-C2 in "Into the Rootwell" has no loss when every hero is down (its loss objective was re-pointed to the stag), so a wipe may leave the level stuck. Check in play and fix?
13. **Q13.** M10's briefing promises a Corruption beast on the sacred tree; the level holds a Goblin Queen at 150 HP. Which is intended?

## Related

[Combat rules](combat-rules.md) · [Progression and economy](progression-economy.md) · [Enemies](enemies.md) · [Home](home.md) · [`reward-balance.md`](../reward-balance.md) · [`combat-balance.md`](../combat-balance.md) · [Glossary](../../glossary.md)
