# Home Systems — Demo Spec v0

This tab turns the Home design into a buildable demo: fixed content, numbers, data structures and a build order. Every number here is a first-pass value to tune in playtests, not a final balance.

**How to use this doc.** It describes what the demo should do, as currently intended. If a build changes a rule or a number, edit it here, where that rule lives. Build details (code locations, verification, test counts, bugs, commit status) go in `build-log.md`.

## Scope and assumptions

The demo is a short prologue of 3 tutorial missions, then one 7-day moon cycle ending in one dungeon: about 2 hours of play plus about 20 minutes of prologue. It contains everything in the design tab except personal room prop swaps, which come last if time allows.

Assumptions this spec makes (flagged in Open questions if they need your call):

- **Roster:** John, Linda, Lucy, Toba and Mark are playable. Mary (Kitchen) and Uncle Ben (Workshop) are non-playable station owners. Toba's healing in combat scales with his Bond to the target.
- **Squad size is set per mission** (3 seats for every side mission in the demo), shown on the map table. The dungeon takes 4. With 5 characters, 2 always stay home on sortie days.
- **AP/FTP:** effects are written against FTP and AP. Decided 2026-10-16 (D-036, D-037): AP is Fixed, FTP pays Duos only (2 each), and Family Roles cost no FTP but have per-round limits (Linda 2, Lucy 3, Mark 1, John unlimited; D-041, D-042). ATB is dropped, so Swift and Spirited effects stay as written. The role-limit code is built later on `main`, not on `thj/home-test` (D-042); until it merges, roles on this branch still cost 1 FTP as built.
- **Existing combat content is reused:** current enemy types and levels; no new combat mechanics beyond Wounded.

## Day loop state machine

The Home loop is one state machine that runs once per day. It is deterministic: given the same state and assignments it produces the same results, which makes it testable in the Editor without art.

| Phase | Player input | System work |
| --- | --- | --- |
| Dawn tick | None | Crops grow and ripe crops auto-harvest, hens lay, Workshop timers advance, Wounded countdown, Great Moon phase +1, deadline check |
| Dawn plan | Assign seats and tasks; pick a sortie at the map table | Carry over yesterday's assignments; validate seats |
| Send-off (sortie days) | None (scene) | Consume the send-off meal, apply its effects to the squad; load the combat level |
| Sortie | Combat | On return: add drops, mark downed units Wounded |
| Morning resolve | None | Resolve Morning seats in station order (below) |
| Noon (home days only) | Change Afternoon seats, or continue | None |
| Afternoon resolve | None | Resolve Afternoon seats in station order |
| Dusk: Dining Table | Watch or skip | Show results, apply Lessons, play Bond scenes |
| Night plan | Fill up to 2 night seats | None |
| Night resolve | None | Stargaze, Hearth time, Vigil |

On sortie days, the order is Dawn plan → Send-off → Sortie → Morning and Afternoon resolve for the stay-home crew → Dusk.

**Station resolution order within a slot:** Care → Homestead → Kitchen → Workshop → Study → Yard → Porch (including the idle characters who fill its free seats; the rest wander the Hall and quiet rooms with no Bond). Homestead resolves before Kitchen so a crop that ripens from tending can be cooked in the same slot's later station, or in the next slot.

**Deadline rules:**

- The dungeon is on the map table from Day 1. An attempt takes the whole day and that night (see Dungeon and Wounded).
- At Dawn of Day 7 (full moon), the map table offers only the dungeon, with a squad of 4. There is no Home plan that day.
- After the dungeon, the cycle ends: any pending Family Event plays, and the demo ends.

## Data model

A new `Core/Systems/HomeSystem/` module (built in M0). Authored data are standalone ScriptableObjects with a GUID `Id`, the same pattern as `EquipmentSO` and `RunUpgradeSO`, listed on one `HomeCycleDefinition`. The repo's `ReferenceableEntity` + Registry pattern holds plain classes inside definition sets, so it doesn't fit rich content like this. Runtime state is saved through `ISavable<T>`.

### Authored definitions

| Definition | Key fields |
| --- | --- |
| `HomeStationDefinition` | Room id, seats per slot with roles (Helper, Teacher, Student, Carer), allowed while Wounded, resolve order, night-only flag, list of `CharacterAffinity` |
| `CharacterAffinity` | Character ref, affinity type (GrowthBoost, Mutate, ReadKey, ExtraPortion), value |
| `IngredientDefinition` | Nutrition tag, points, source (Grown, Pen, Foraged), grow days, harvest yield, mutates-to ingredient |
| `RecipeDefinition` | Ingredient multiset, known at start, required helper (optional character), send-off and ration effects as a `DishEffect`: flat stat bonuses added like gear, stat-factor modifiers like Revenge, pool modifiers (e.g. +1 AP) and a max-FTP bonus |
| `StudyItemDefinition` | Slots required, default outcomes, per-character outcomes, combo item + combo outcomes |
| `HomeOutcome` | Polymorphic (`[SerializeReference]`): UnlockRecipe, AddMaterials, RevealMission, EnemyIntel, AddItem, Lore, UnlockRestRoom |
| `EquipmentSO` | Character, cost as `GResourceRequirement[]`, existing asset reused as is: linear Lv1–Lv3, Gold plus one themed material per level |
| `LessonDefinition` | Teacher, stat, value per point, cap per Yard tier |
| `HomeUpgradeDefinition` | Room, tier, cost, effects (faction stat modifiers, capacity changes) |
| `StarPatternDefinition` | Visible nights, chart item it produces |
| `OmenDefinition` | Night, affected missions, modifier effects applied at level start |
| `HomeMissionEntry` | Mission ref, squad seats (read from the Mission's MissionRoster; a fallback count only for placeholder entries), level count, availability window, visible from start or revealed by an outcome, drops, dungeon thread it cuts |
| `HomeCycleDefinition` | Day count (7), dungeon available from day (1), dungeon threads, free days per day spared, starting state preset |

### Runtime

- `HomeSimulation`: the day loop and the state machine above as plain C#, with no scene and no randomness, so it runs the same in the Editor debug window, in tests and in play. `HomeDayRunner` is the Home-scene driver: it resumes the sim when the scene reloads after a sortie, relays events to `GlobalEventBus` and saves at each Dawn plan. Gold and materials go through `IHomeWallet`: the player faction's aggregated pool in play, an in-memory wallet in the Editor.
- `HomeState : ISavable<HomeSaveData>`, registered with `SaveLoadManager`. It lives outside any scene, like EquipmentManager, so it survives the Home scene unloading during a sortie. It holds the day, assignments, plots, pen, pantry, inventory, known recipes, study progress, Bond pairs, Wounded timers, Lesson points, upgrades, and revealed missions, omens and charts.
- `HomeDayReport`: the list of results produced during a day. The Dining Table reads it to show bubbles, so the scene never recomputes anything.
- New `GlobalEventBus` events: `homePhaseChanged`, `homeSlotResolved`, `homeDayReportReady`.

### Reusing existing code

| Need | Existing piece |
| --- | --- |
| Gold, Steel, Timber, Stone, Fabric | `GResources` wallets in `FactionTracker` |
| Lesson and upgrade stats | `Faction`'s `StatAttributeSet` (Bergsons faction layer) for Lessons; a separate Home layer for Home Upgrades, so enemies never receive them |
| Dish effects | A `DishEffect` on each recipe, applied by `HomeSendOffApplier` from `FactionTracker.PrepareLevel`, the same level-start path run upgrades and equipment use. Not `AEffectBase`, which needs an in-level owner and target |
| FTP from rations | `FamilyTimePoints` |
| Wounded | `FactionTracker` persisted unit health, plus a Wounded timer per unit |
| Dining Table, Send-off, Bond scenes | `SequencePlayer` with `DialogNodeSequence` |
| Rest Room branch | Mission route selection between levels (as in `M6 - Hidden Sanctuary - Third Step`), with the safe-room levels in `Content/Levels/DungeonSafeRooms/` as the Rest Room base |
| Moon clock | The `HomeState` calendar (day and phase). `TimeOfDayTracker` was replaced: it is marked obsolete and nothing uses it |
| Fast iteration | `HomeStatePreset` assets, like `LevelFastForwardRoster`, to start the sim from any day with a chosen state. `Preset_Day1Start` is the Day 1 starting state |
| Map table and mission selection | `WorldMapPanelUI` (reviewed): it shows missions unlocked by the mission dependency graph and launches them straight away. M2 adds the Home rules on top (day windows, reveals, each side mission once, the forced dungeon). The squad pick reuses `CharacterSelectPanelUI`, which already asks for `MissionRoster.FreeSlotsCount` characters |
| Dungeon Upgrade Rooms | The in-run upgrade items already in testing; Divine Relics as the rare top tier |
| Old Home stat panels | Not reused. The gold-for-stats Family Room, Kitchen and Training Ground panels are unwired, not deleted: the legacyStatUpgradePanelsEnabled box on HomeManager (off) brings them back |

## Roster and missions

### Character affinities

Each playable character has one clear Home identity in the demo.

| Character | Homestead | Kitchen helper | Study key | Yard Lesson | Night |
| --- | --- | --- | --- | --- | --- |
| John | Normal | Batch makes 3 portions instead of 2 | War Journal also points to an old armory: 3 Steel | Toughness | Normal |
| Linda | Violin: tended plot grows 1 day faster | Normal | Mossy Tablet also marks a timber stand: 3 Timber | Footwork | Normal |
| Lucy | Tended Hearty Gourd becomes Soul Gourd | Normal | Only reader who unlocks Soul Flower Tea from the Recipe Scrap | Edge | Normal |
| Toba | Tending adds +2 yield instead of +1; if he tends the pen, the hens lay 1 extra egg | Normal | Normal | Mending | Healer: his Vigil or day Care ends Wounded by the next slot instead of the next Dawn, and the pair gains double Care Bond |
| Mark | Normal | Tea master: a batch of Soul Flower Tea or Moss Broth makes 3 portions | Focused reader: adds 2 progress per slot instead of 1 | Focus | Only watcher who can chart The Crown |

### Missions

Each side mission can be played once. Enemy types reuse existing units. Most side missions are a single level; the hidden Drowned Shrine is 2 levels and the Deev Burrow boss fight is 3, played straight through with no route choices. Route choices, Rest Rooms and in-run upgrades belong to the dungeon alone. Any sortie takes one day, whatever its length.

| Mission | Seats | Available | Enemies | Drops |
| --- | --- | --- | --- | --- |
| Goblin Camp | 3 | From Day 1 | Archer Goblin, Masher Goblin | 40 gold, 3 Steel, 3 feed, 2 Sharproot seeds, Queen's Sigil |
| Old Watchtower | 3 | From Day 1 | A Dark Claw pack led by a Black Claw (attacking it draws every Dark Claw onto the attacker), Dark Shaman | 30 gold, 3 Timber, Weathered War Journal |
| Mossy Hollow | 3 | From Day 1 | Dark Claw, Archer Goblin, with Dark Worm as support | 20 gold, 2 Timber, 3 Calm Moss, 2 feed, 2 Soul Flower seeds, Recipe Scrap, Mossy Tablet |
| Drowned Shrine | 3 | Revealed by Old Map Fragment + Star Chart: The Hound | Dark Worm, Dark Shaman | 50 gold, 3 Stone |
| Deev Burrow | 3 | Revealed by the Weathered War Journal | Mountain Deev (boss) with its Deevoted tentacles, which must be destroyed before the boss can be hit | 60 gold, 4 Stone, 2 Steel |
| Goblin Queen's Warren (dungeon) | 4 | From Day 1; forced on Day 7 | Goblins, Goblin Queen (boss) | Cycle rewards |
| Goblin Scout Post | 3 | Days 1–3 only | Archer Goblin, Masher Goblin | 30 gold, 2 Steel, 1 Fabric, 2 Hearty Gourd seeds, 2 Quickberry seeds |
| Shaman's Circle | 3 | Days 3–5 only | Dark Shaman, Archer Goblin | 20 gold, 3 Fabric, 2 Calm Moss |

With 7 side missions (two of them only available for a window of days) and the dungeon open from Day 1, about 4 sorties fit in the week. Choosing which to skip, and whether to grow stronger or weaken the Queen, is part of the demo.

**Pay and XP.** Home pays everything through the mission entry: drops for each cleared level (paid once per level, even after a loss) plus completion drops. XP is 20 for a single-level side mission, 30 for Drowned Shrine and Deev Burrow, and 60 for the Warren.

## Homestead and Kitchen

### Homestead rules

- **4 plots** (6 after the Garden upgrade). Planting is a task set in the Homestead window and needs no seat. Ripe crops auto-harvest at Dawn.
- **Tending** takes one of 2 tending seats and applies once per slot: anyone tending adds +1 harvest yield to that plot; Linda also advances it 1 day; Lucy turns a Hearty Gourd plot into Soul Gourd.
- **Pen: 2 hens.** At Dawn, each hen eats 1 feed and lays 1 egg. No feed, no egg.

| Ingredient | Tag | Source | Grow days | Base yield |
| --- | --- | --- | --- | --- |
| Hearty Gourd | Hearty | Grown | 2 | 2 |
| Sharproot | Sharp | Grown | 2 | 2 |
| Quickberry | Swift | Grown | 1 | 3 |
| Soul Flower | Spirited | Grown | 3 | 2 |
| Calm Moss | Calm | Foraged (Mossy Hollow) | None | None |
| Egg | Binder | Pen | Daily | 1 per fed hen |
| Soul Gourd | Hearty + Spirited | Lucy tending Hearty Gourd | 2 | 2 |

The tag is shown as a color on the ingredient icon, so the player can guess what a combination might do.

### Kitchen rules

- **Pantry holds 4 portions** (6 after the Kitchen upgrade). Everything in the pantry goes into the dungeon as rations.
- **Mary alone** cooks 1 portion of the chosen daily recipe at Afternoon resolve, if the ingredients are in stock.
- **With a helper**, the slot does one of two things:
  - **Batch:** cook a known recipe, consuming its ingredients once, for 2 portions (3 with John).
  - **Experiment:** pick 1–3 ingredients. An exact match for an unknown recipe teaches it and makes 1 portion; anything else makes 1 Mystery Stew.
- **Send-off meal:** before a sortie, the player may spend 1 portion. Its send-off effect applies to every squad member for that mission.
- **Rations:** in a Rest Room, each portion eaten applies its ration effect to the whole party.

| Dish | Ingredients | How it's learned | Send-off effect | Ration effect |
| --- | --- | --- | --- | --- |
| Gourd Omelette | Hearty Gourd + Egg | Known at start | +10% max HP | Heal 25% HP |
| Hearty Stew | Hearty Gourd ×2 | Experiment | +20% max HP | Heal 40% HP |
| Spiced Stew | Hearty Gourd + Sharproot | Experiment | +10% damage | Heal 20% HP, +10% damage next level |
| Quickberry Tart | Quickberry + Egg | Experiment | +1 AP on turn 1 | +1 AP on turn 1 of next level |
| Hunter's Skewer | Sharproot + Quickberry | Experiment | +5% crit | +5% crit next level |
| Moss Broth | Calm Moss + Egg | Mossy Tablet (any reader) or experiment | +10% evasion | +10% evasion next level |
| Soul Flower Tea | Soul Flower | Recipe Scrap, read by Lucy only | +2 max FTP for the mission | +2 FTP |
| Soul Gourd Pie | Soul Gourd + Egg | Experiment | +10% max HP, +1 max FTP for the mission | Heal 30% HP, +1 FTP |
| Mystery Stew | Any unknown combination | Always | +5% max HP | Heal 10% HP |

Soul Flower Tea is deliberately the hardest dish to get: it needs Mossy Hollow's seeds, 3 days of growing (2 with Linda), and Lucy reading the scrap. It's also the best FTP source for the dungeon, so it's the demo's clearest planning goal.

## Study, Workshop and Home Upgrades

### Study rules

- One item on the desk at a time, with 2 reader seats. Each reader adds 1 progress per slot, so 2 readers finish twice as fast. Progress is kept if the item is swapped out.
- **Combos are never guessed.** Each piece's own result hints at its partner. Once the player owns both pieces and has studied either one, a **Connect** task (for example, "Old Map Fragment + The Hound") appears on the shelf by itself. It counts as the one item on the desk and takes 1 slot. The Dining Table repeats the hint. The demo has one combo.
- **Keyed outcomes never get lost.** If someone other than the key character finishes an item, they get the default outcome, and the item stays on the shelf as partly understood. The key character can claim their bonus later in 1 slot. The key character only gets the bonus if they are seated at the Study in the slot the item finishes; a key reader seated in an earlier slot does not count.

| Item | Source | Slots | Any reader gets | Key reader also gets |
| --- | --- | --- | --- | --- |
| Old Map Fragment | Tutorial 3 (prologue) | 1 | A hint: the map marks a shrine beneath a hound-shaped constellation. Connected with Star Chart: The Hound, it reveals Drowned Shrine | None |
| Queen's Sigil | Goblin Camp | 2 | Goblin Queen intel: her weaknesses show in the combat UI | None |
| Weathered War Journal | Old Watchtower | 2 | Reveals Deev Burrow | John: an old armory, 3 Steel |
| Recipe Scrap | Mossy Hollow | 1 | A hint that someone with a feel for the arcane could read it | Lucy: Soul Flower Tea recipe |
| Mossy Tablet | Mossy Hollow | 2 | Moss Broth recipe | Linda: a timber stand, 3 Timber |
| Star Chart: The Hound | Stargazing | 1 | A hint: the Hound's eye points to a place on an old map. Connects with the Old Map Fragment | None |
| Star Chart: The Lantern | Stargazing | 1 | Quickberry Tart and Hunter's Skewer recipes | None |
| Star Chart: The Crown | Stargazing (Mark only) | 2 | Unlocks a second Rest Room branch in the dungeon | None |

### Workshop rules

- Ben takes one order at a time. Alone, it's ready in 2 Dawns; with a helper seated at the Workshop in a day slot (Morning or Afternoon) of the day it's ordered, it's ready next Dawn. An order is paid when placed and can't be cancelled.
- Each playable character has one weapon-slot item (John's Sword, Linda's Bow, Lucy's Pyromancer's Ring, Toba's Exquisite Stone Axe, Mark's Wrist Wrap of Power). Upgrades are linear — **Lv1 → Lv2 → Lv3**, no branching choice and no blueprint requirement; each level just spends Gold plus a themed secondary material. `EquipmentSO` has an unused `equipmentsToUnlock`/`equipmentsToHide` hook that could power branching or blueprint-gated upgrades later, but nothing in the demo uses it today. Only these five weapons can be ordered; the other gear pieces are not upgradable in the demo. The game's UI already labels the unupgraded weapon Lv.1, so the spec's Lv1 is the button that reads Order Lv.2.
- Ordering is allowed on any day before the full moon. An order that would be ready after the full moon (ready day later than the last Home day, so a Day 7 Dawn delivery is still in time) is flagged "Arrives after the full moon" on the order button, in the report and on the calendar. A helper in the Workshop on the day it is placed brings it one day earlier.

| Weapon | Lv1 | Lv2 | Lv3 |
| --- | --- | --- | --- |
| John's Sword | +3 damage (10 Gold + 1 Steel) | +5 damage (20 Gold + 3 Steel) | +7 damage (40 Gold + 5 Steel) |
| Linda's Bow | +1 damage (10 Gold + 1 Timber) | +3 damage (20 Gold + 3 Timber) | +5 damage (40 Gold + 5 Timber) |
| Lucy's Ring | +10% crit chance (10 Gold + 1 Steel) | +15% crit chance (20 Gold + 3 Steel) | +20% crit chance (40 Gold + 5 Steel) |
| Toba's Axe | +4 damage (10 Gold + 1 Stone) | +6 damage (20 Gold + 3 Stone + 1 Timber) | +8 damage (40 Gold + 3 Stone + 3 Timber) |
| Mark's Wrist Wrap | +2 damage (10 Gold + 1 Fabric) | +4 damage (20 Gold + 3 Fabric) | +6 damage (50 Gold + 5 Fabric) |

Costs follow the same Gold + material shape at every level (10/20/40 Gold, material 1/3/5), with two exceptions: Mark's Wrist Wrap is 50 Gold at Lv3, and Toba's Axe blends Stone and Timber from Lv2 on. Exact values live on each `EquipmentSO` asset in `Resources/Unit Equipments`.

### Home Upgrades

Bought from the room's own window, paid immediately, active from the next Dawn. They don't use Ben or any seat. The effects are permanent for the run: they are written to a separate Home stat layer (Stat\_HP, Stat\_FP) that only the family's heroes receive, not applied as level-start modifiers the way dishes are. Yard Lessons use the Bergsons faction stat layer instead.

| Upgrade | Cost | Effect |
| --- | --- | --- |
| Kitchen T2 | 40 gold, 2 Stone, 1 Timber | +20% max HP for the family (Home layer Stat\_HP level 1); pantry holds 6 |
| Dining Table T2 | 50 gold, 2 Timber, 2 Fabric | +1 FTP per link between squad heroes (Home layer Stat\_FP level 1) |
| Garden T2 | 20 gold, 2 Timber | +2 plots |

### Economy check

The economy uses the four materials the equipment assets already use, and each comes from missions that fit it: **Steel** from goblin sites, **Timber** from Old Watchtower and Mossy Hollow, **Stone** from the Drowned Shrine and Deev Burrow, **Fabric** from Goblin Scout Post and Shaman's Circle. The demo starts with 100 gold, 1 Steel and 1 Timber. About 4 sorties bring roughly 140–180 gold and 8–11 materials of 2–3 kinds. The three Home Upgrades cost 110 gold, 5 Timber, 2 Stone and 2 Fabric, and each weapon level costs 10/20/40 gold plus 1/3/5 of its material. A typical run affords most Home Upgrades, Lv1 for everyone and Lv2 for one or two characters. Which missions the player picks decides which characters and rooms can be upgraded.

## Yard, Bond and Family Event

### Yard Lessons

The Yard has 1 Teacher seat and 2 Student seats (same as the Home design), so a session makes 1 to 3 points. A session needs a Teacher and at least 1 Student; Wounded characters can't take part. Points = number of Students, +1 if any Student has Bond level 2 or higher with the Teacher. Points apply to the family's stats at the Dining Table.

| Lesson | Teacher | Per point (whole family) | Cap at Yard T1 |
| --- | --- | --- | --- |
| Toughness | John | +2% max HP | 6 points |
| Footwork | Linda | +1% evasion | 6 points |
| Edge | Lucy | +2% damage | 6 points |
| Mending | Toba | +2% Health Potion healing | 6 points |
| Focus | Mark | +1% crit | 6 points |

### Bond

Five playable characters make 10 pairs. Levels: **L1 at 10 points, L2 at 25, L3 at 45.** Pairs start at 10 (L1), except the showcase pair, Linda and Toba, which starts at 18 (close to L2), and Toba's other pairs, which start at 6 (L0: he is the newcomer, and the roster shows it).

| Activity | Bond per pair |
| --- | --- |
| Sharing a station in the same slot | +2 |
| Yard: Teacher with each Student | +3 |
| Porch, assigned together | +5 |
| Porch, idle together (only the first idle characters who fit in the Porch's free seats, max 2 on the Porch in all; other idle characters wander the house and earn no Bond; no idle Bond at night) | +1 |
| Hearth time (night) | +5 |
| Care or Vigil (carer and patient) | +8 |
| Family Event | +5 for every pair |

A pair gains at most one entry per slot (the highest). Reaching L2 from the showcase pair's 18 points takes two or three deliberate activities, which fits the week if the player prioritizes it. Toba's other pairs need a few more to reach L1.

A Bond level-up earned at night plays its scene at the next Dawn; one earned by day plays at the next Dusk. The Bond preview shows in the station window when a pair is seated ("Linda & Toba +5 Bond 22 → 27/45 → Lv 2: their duo, a Bond scene"), and the roster hover shows each pair's bar and what its next level opens.

What Bond does in the demo (each lock opens by its pair's Bond level and relocks with a new moon cycle):

- **L2 on the showcase pair, Linda and Toba,** makes their duo (Linda_Toba_Duo) usable in combat and learns it in the Family Skill Tree for free (no Family Skill Point; changed 2026-10-13).
- **L2 on Linda and Lucy** opens Sisters' Rivalry (a kill by one gives the other AP and a ready basic attack). **L2 on John and Mark** opens John's Command Shield Dash after Mark's Command.
- **L1 on a pair** opens Pass-By for that pair. Every pair except Toba's starts at L1, so Toba's pairs earn it.
- **Bond scenes** are written only for the showcase pair (at L2 and L3). Other pairs get a one-line Dining Table remark when they level.
- **The Fireside payoff:** a pair that sits at the Fireside earns one small boost for the next mission, one of three picked per pair (stable per save): their first duo together is free; the first Family Role either of them uses is free (**to be replaced** after the role-limit merge, D-040: each of the pair gets +1 role use in the sortie's first round, and John's first redirect takes no damage); or the family FP cap is +2 for the mission. Only pairs with both members in the squad carry it; an unspent one ends with the sortie, and an interrupted sortie hands it back.

### Family Event: the Picnic

- The demo grants **1 Family Skill Point after the second completed side mission**. That unlocks the Picnic.
- The player schedules it from the Dining Table on any day before the deadline, or leaves it until after the dungeon.
- The Picnic takes the whole day with all 5 characters: +5 Bond for every pair, and the Family Skill Point is spent in the Family Skill Tree during the scene.
- The tradeoff: holding it before the dungeon costs a day, but lets the showcase duo be unlocked for the dungeon if its pair has reached L2.

## Night

Nights 1–6 are playable; the night of Day 7 is the dungeon, and an earlier dungeon attempt also takes its night. At most 2 characters stay up in total, across three activities:

| Activity | Seats | Result |
| --- | --- | --- |
| Stargaze (roof) | 1–2 | Each watcher charts one visible pattern (once per pattern; the seat names it, Auto takes the first chartable one, Mark-only patterns first); reveals tonight's Omen if there is one; 2 watchers also gain +2 Bond |
| Hearth time (Fireside Talk) | Exactly 2 | +5 Bond for the pair, Bond scenes earned at night play at dawn, and the pair earns the Fireside payoff (one person alone gains nothing and is not offered) |
| Vigil (the night version of the Care visit, at the bedside) | 1 carer | Every Wounded patient recovers at the next Dawn; +8 Bond for each carer–patient pair |

Night seats carry over from night to night, like day seats. Each Dawn shows a "Last night" card listing the night's results.

### Star patterns

| Pattern | Visible on nights | Who can chart it | Chart leads to |
| --- | --- | --- | --- |
| The Hound | 2, 3 | Anyone | Drowned Shrine (combo with Old Map Fragment) |
| The Lantern | 3, 4 | Anyone | Two recipes |
| The Crown | 5, 6 | Mark only | A second Rest Room in the dungeon |

Night 3 has two patterns visible at once, so one watcher can chart only one of them. Two watchers can chart both.

Night 1 also shows a lore-only pattern, The Great Moon, which gives no chart.

### Omens

An Omen belongs to a night and affects missions the next day. Unrevealed Omens show as a clouded-sky icon on the affected missions at the map table; revealed ones show the full effect.

| Night | Omen | Affects | Effect |
| --- | --- | --- | --- |
| 2 | Red Veil | Goblin Camp on Day 3 | 1 fewer enemy; the rest have +25% HP |
| 4 | Twin Glow | Mossy Hollow and Drowned Shrine on Day 5 | Mission drop quantities doubled (study items, recipes and reveals are not) |
| 6 | Hungry Moon | The dungeon, only if entered on Day 7 | The Goblin Queen gains +1 AP at the start of each of her turns while below 50% HP (built 2026-10-14) |

The Hungry Moon gives a reason to enter the dungeon early without forcing it.

Implementation: an Omen is an `OmenDefinition` with a `DishEffect` applied to every enemy at level start (the same path the send-off meal uses; Red Veil = Stat\_HP x1.25), `enemiesRemoved` (deactivated at level start, never the last enemy) and `dropMultiplier` (Twin Glow = 2). It applies on its effect day whether or not it was revealed, is recorded on the sortie at departure (which also reveals it), and only changes combat during a Home sortie.

## Dungeon and Wounded

### Dungeon brief

The Goblin Queen is preparing a ritual for the night the Great Moon is full; when it completes, the Corruption she has gathered breaks out of the Warren. Her strength is fed from around the valley: corruption pools, her hunters, a bound guardian and a stolen relic. Every thread the family cuts is strength she no longer has when they walk in.

This frame explains the deadline (the ritual), the Hungry Moon Omen (the ritual nearly done) and why side missions make the dungeon easier. The player learns it in four places:

- **Prologue:** when the Great Moon rises, the family learns of the ritual and where her strength comes from.
- **Mission cards** on the map table name the thread each mission cuts, with a one-line briefing.
- **The dungeon card** lists the threads, crosses off cut ones, and adds ones revealed by Study or stargazing.
- **The Dining Table** reacts when a thread is cut, so progress against the Queen is felt at dinner.

### Threads

| Source | Thread it cuts | Dungeon effect |
| --- | --- | --- |
| Goblin Camp | A corruption pool breeding her soldiers | Fewer goblin reinforcements in Levels 1–2 |
| Old Watchtower | Her hunters, the Black Claw's pack | No Dark Claw pack in the dungeon |
| Mossy Hollow | Reveals an old path into the Warren | A side route that avoids the Masher wave |
| Drowned Shrine | A relic she wanted for the ritual | Secret room with a Divine Relic |
| Deev Burrow | The Mountain Deev bound as her guardian | Removes the mid-dungeon elite |
| Queen's Sigil (Study) | Her plan | Goblin Queen intel in the combat UI |
| Star Chart: The Crown | A hidden campsite | Second Rest Room branch |

Goblin Scout Post and Shaman's Circle cut no thread: they are resource missions, so choosing a sortie means trading "grow stronger" against "weaken the Queen".

### Goblin Queen's Warren

A squad of 4, chosen from the 5 at the map table, across 4 combat levels. Each branch is a route the player picks on the mission map after completing the previous level, using the existing route system. HP and FTP don't refill between levels.

| Step | Content |
| --- | --- |
| Level 1 | Goblins, with reinforcements unless Goblin Camp is done |
| Level 2 | Goblins with Archer support, plus the Dark Claw pack unless Old Watchtower is done |
| Branch 1 | Rest Room or Upgrade Room |
| Level 3 | Masher-heavy wave (a side route around it if Mossy Hollow is done) and the mid-dungeon elite unless Deev Burrow is done; secret room if Drowned Shrine is done |
| Branch 2 (only with Star Chart: The Crown) | Rest Room or Upgrade Room |
| Level 4 | Goblin Queen (boss) |

- **Rest Room (recover now):** a campfire scene. Everyone recovers 10% HP, then the player eats any number of pantry portions, each applying its ration effect to the whole party.
- **Upgrade Room (power for the rest of the run):** choose 1 of 3 in-run upgrades, using the in-run upgrade items already in testing (for example, more damage on Lucy's Sidewinders, family-wide crit, Cripple on Mark's Vault).
- **Secret room:** a Divine Relic, the rare top tier of in-run items.

### Three layers of power

| Layer | Lasts | Comes from |
| --- | --- | --- |
| Permanent | The whole game | Skill trees, Lessons, Home Upgrades, gear, Bond and duos |
| Per sortie | One mission | Send-off meal, Omens |
| Per run | One dungeon attempt | Route choices, in-run upgrades, Divine Relics, rations |

In-run upgrades and relics exist only in the dungeon, so side missions stay quick and the dungeon stays the roguelike run.

### Attempts

- **Available from Day 1.** An attempt takes the whole day and that night, so no night activities happen.
- **Failed attempt before the full moon:** the family retreats home. Drops from cleared levels are kept; in-run upgrades, relics and eaten rations are lost; at most 1 character comes home Wounded. The dungeon card keeps the routes and enemy intel for the levels reached, so a failed attempt works as expensive scouting.
- **Win before the full moon:** each day spared becomes a free Home day before the next cycle. In the demo, it becomes an end-of-demo bonus scene.
- **Full-moon attempt:** the last one. In the demo, a loss offers a retry from the dungeon's start with the same pantry. In the full game, a loss has a story consequence instead of a game over.

### Wounded

- **Trigger:** the first unit downed during a sortie or dungeon attempt comes home Wounded, with a 2-Dawn recovery timer. At most 1 character is Wounded per sortie, win or lose.
- **Restrictions:** no sortie seats and no Yard seats. Study, Kitchen helper, Porch and night activities are allowed.
- **Care:** one visit to the patient, in any slot (Morning, Afternoon or Night). One carer tends every Wounded character that slot, and each carer–patient pair gains the Care Bond. The patient recovers at the next Dawn; with Toba, right after that slot, and the pair gains double Care Bond. A visit is only offered while someone would gain from it ("Already on the mend" otherwise).
- **Several Wounded:** all are tended by the one carer; there is no patient cap and only one carer seat per slot. Patients resting together also gain the shared-station Bond (+2).
- **Dungeon:** a Wounded character still joins, at 50% max HP.
- **Lost sortie:** the squad returns home and the day continues to Dusk. Drops from cleared levels are kept; the completion reward, where key items live, is lost. The mission stays available and restarts from its first level.

## Prologue

The three existing tutorial missions become a prologue that runs before the moon cycle. The Great Moon isn't in the sky yet, so no days pass and there is no deadline. After each mission, a short guided Home beat teaches one Home system, tied to what the mission just taught.

| Step | Teaches in combat | Home beat afterwards | Unlocks |
| --- | --- | --- | --- |
| Tutorial 1 | Basics | The first Dining Table: meet the family; results are shared at dinner. Then the Map Table, the only room left open: the player picks the next mission on the map | Dining Table, Map Table |
| Tutorial 2 | Family passives, FTP | Mary introduces the Kitchen and Homestead; food restores FTP; the player plants a Hearty Gourd. The map stays closed until it is planted, then the player picks the next mission on the map | Kitchen, Homestead |
| Tutorial 3 | Duos | A Porch scene: duos come from time spent together | Porch, Bond; the mission drops the Old Map Fragment |
| Prologue end | None | The Great Moon appears in the sky: the story's inciting event. The family learns of the Goblin Queen's ritual and that her strength is fed from around the valley, and the deadline begins | Day 1 Dawn |

Rules:

- Time doesn't advance during the prologue, and only the room being introduced is clickable.
- Each Home beat lasts 1–2 minutes and ends when the player launches the next tutorial from the map (the beat before the Great Moon ends with one Continue button). A Skip prologue button is always visible in the header, asks for a second click to confirm, and jumps straight to Day 1.
- Stations after the prologue open on a schedule (the cycle's `stagedUnlocks` switch turns it off, and then everything is open from Day 1): Study and Workshop on Day 1, the Yard on Day 2 Dawn, Stargaze and the Fireside on the first night, Care and the Vigil on the first Wounded. Kitchen, Homestead and Porch are open from the prologue. Each opening is introduced by its owner (2–3 lines, the prop outlined, one first action), and a forced first action (Study, Yard, Care) holds the time button until it is done. A Home Guide page per station unlocks with its introduction (what it does, uses and makes, who is good at it).
- The duo taught in Tutorial 3 stays unlocked. The Bond showcase duo, Linda and Toba, is a different one.
- Time budget: about 20 minutes on top of the 2-hour cycle.

Implementation: `HomeCycleDefinition` gets a prologue step list, `HomeState` tracks which stations are unlocked, and each Home beat is a `Sequence`.

## Starting state and schedule

### Starting state (Day 1 Dawn, after the prologue)

| Area | Contents |
| --- | --- |
| Wallet | 100 gold, 1 Steel, 1 Timber |
| Homestead | Plot 1: Hearty Gourd planted in the prologue, ripe at Dawn of Day 2. Plots 2–4 empty. Seeds: 2 Hearty Gourd, 2 Quickberry. 4 feed, 2 hens |
| Kitchen | 1 Hearty Gourd, 2 eggs in stock; pantry has 1 Gourd Omelette; Gourd Omelette known |
| Study | Old Map Fragment on the shelf (found in Tutorial 3) |
| Workshop | No weapon upgrades bought yet |
| Bond | Pairs at 10, showcase pair (Linda–Toba) at 18, Toba's other pairs at 6 |

### 7-day schedule

| Day | Great Moon | Fixed content |
| --- | --- | --- |
| 1 | 1/7 | The first free day. Map table offers Goblin Camp, Old Watchtower, Mossy Hollow, Goblin Scout Post and the dungeon. Night 1: stargazing tutorial (lore only) |
| 2 | 2/7 | The Hound visible (nights 2–3). Omen: Red Veil |
| 3 | 3/7 | The Lantern visible (nights 3–4) |
| 4 | 4/7 | Omen: Twin Glow |
| 5 | 5/7 | The Crown visible (nights 5–6, Mark only) |
| 6 | 6/7 | Omen: Hungry Moon |
| 7 | Full | Forced dungeon departure |

Player-driven events that can land on any day: the Family Skill Point after the second side mission (unlocking the Picnic), hidden mission reveals, Wounded, and Bond level-ups.

## Implementation milestones

The order gets a playable Home-to-combat loop running as early as possible, then layers systems on it. Every milestone ships with graybox UI for what it adds; the art pass comes last.

| Milestone | Builds | Done when |
| --- | --- | --- |
| M0: Core sim (done) | `HomeState`, `HomeSimulation` phases, definition assets, station resolve order, an Editor debug window, `HomeStatePreset` presets | All 7 days can be run in the Editor with the debug window, and each day's `HomeDayReport` is logged |
| M1: Food loop (done) | Homestead, pen, Kitchen, pantry, send-off meal applied at level start | Cook a Gourd Omelette, start a combat level, and the squad has +10% max HP |
| M2: Sorties (done) | Map table built on the existing world map mission selection (`WorldMapPanelUI`), squad seats per mission, launching a combat level from Home and returning with drops, Wounded, lost-sortie handling | A full day with a sortie runs Dawn to Dusk, with the stay-home crew's results arriving at Dusk |
| M3: Knowledge and gear (done) | Study (items, keys, combos), mission reveals, Workshop orders, Home Upgrades | The Weathered War Journal reveals Deev Burrow, and John reading it also yields 3 Steel |
| M4: Family (done) | Yard Lessons, Bond, Porch and idle, Dining Table report scene | A Yard session raises a family stat at Dusk, and the showcase pair reaches L2 with its scene |
| M5: Night (done) | Night seats, stargazing and charts, Omens, Vigil, Hearth time | Charting The Hound on night 2 leads to Drowned Shrine on Day 4 |
| M6: Dungeon (done) | Dungeon threads and dungeon card, Rest Room / Upgrade Room branches, rations, in-run upgrades and relics, attempts and retreat, free days from an early win, forced departure, Picnic | A full 7-day run ends in the dungeon with the pantry's rations usable at the campfire |
| M7: Prologue (done) | Tutorial missions wired to Home, guided Home beats, station unlock flags, Great Moon rise | A new game plays the 3 tutorials and their Home beats, then starts Day 1 with the starting state produced by the prologue |
| M8: Presentation (in progress) | Clickable rooms, station window prefab, character bubbles, both moons, time-lapse, Send-off scene; personal room props as a stretch | The demo plays with no debug UI |

Build details, verification and commit status for each milestone are in `build-log.md`.

M0 is worth doing first even though it shows nothing: a deterministic, Editor-runnable sim lets balance numbers be tuned before any art exists.

## Open questions for this spec

- **Showcase duo:** decided 2026-10-12: the Linda–Toba pair, using the existing Linda_Toba_Duo (this replaces the Toba–Mark decision of 2026-09-29; the Toba–Mark duo is dropped). It differs from the duo taught in Tutorial 3.
- **Fireside payoff, what else can be rewarded:** decide what else a pair can earn. Examples: a paired-ability efficiency bonus (Toba with someone: Toba heals that person more during the next sortie; John with someone: John takes less damage during his Family Role for that person), a stronger duo, an extra pass-by effect. Today only three exist: first duo free, first Family Role free (becomes "+1 role use", D-040), or FP cap +2.
- **Dungeon squad:** take 4 of the 5 characters into the dungeon, or bring the whole family?
- **FTP scale:** the +1/+2 FTP values assume a small FTP cap; they need the real cap to tune.
- **Toba:** the same character as Dom, which was his old name. His affinities, Mending Lesson and Axe are all set.
- **Levels:** decided: a mix. Keep the good existing levels and build new ones only where a mission needs them. M2 uses copies of existing Generic Levels whose enemies differ from the Missions table (mapping in the Build Log). Still open: author matching levels, or change the table.
- **Goblin Queen narrative:** adapt the ritual frame to the existing script, if it already frames her differently.
- **Divine Relics:** which relics appear in the demo, and whether any relic has a drawback.
- **Mid-sortie quit or crash:** for now it rolls back to the Dawn plan and refunds the send-off, because the game only saves at Dawn plan. That suits testing; the real behavior is undecided.
- **Dining T2 scale:** Stat\_FP level 1 adds 1 FTP per link between squad heroes (squad FTP is 3 x (heroes - 1) at level 0, 4 x (heroes - 1) at level 1), so it is +2 for a 3-hero sortie and +3 for the 4-hero dungeon, not a flat +1. Decide whether that is intended or whether it should be a flat bonus.
- **Workshop edge cases:** orders can't be cancelled; whether to allow cancelling is still open. (Late orders are settled: allowed and warned, see Workshop rules.)
- **Faction stat resets:** starting a new cycle sets Lesson, Home Upgrade and weapon levels back to 0. Decide whether the full game keeps that. (The `EquipmentManager` reset bug is tracked in the Build Log.)
- **Mending scope:** as built it scales only Health Potion healing. Should it cover all healing done (Toba's care, abilities, dishes), which needs a new stat?
- **HP stacking:** HP bonuses multiply (Toughness 6 points x1.12 with Kitchen T2 x1.2 = x1.344). Intended, or should they add?
- **Red Veil rounding:** x1.25 leaves fractional enemy max HP (Dark Claw 10 to 12.5). Round, and which way?
- **Resting together at night:** Wounded patients still gain the +2 shared-room Bond at night with no carer. Keep or remove?
