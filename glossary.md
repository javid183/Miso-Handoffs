# Glossary

Owner: narrative agent. Names and terms as the game uses them, with the code name when it differs. This file wins over memory. **Started 2026-10-15 from project notes; nothing here is confirmed Children of Morta canon beyond the names.**

## The family (Bergsons)

| Name | Role | Notes |
| --- | --- | --- |
| John | Father; sword, tank | Family Role: shields a nearby attacked family member. No limit per round; paid with his own HP (D-042) |
| Linda | Ranged, support | Family Role: attacks enemies who end their move in her row or column. 2 per round from one pool; the same enemy can trigger her more than once (D-041) |
| Lucy | Daughter; skirmisher | Family Role: follows up another family member's attack. 3 per round (D-042) |
| Mark | Monk, Zen master | Family Role: attacks anyone who attacks family. 1 per round (D-042). Unlocked after a mission (`unlockedAfterMission`) |
| Toba | Healer, nature lover; healing scales with Bond | **Formerly Dom.** Assets and folders may still say Dom (e.g. `Features/Player/Dom/`). Prefabs are `Unit_Toba` etc. Always write Toba |
| Kevin | Home-only | Chore seats; no Bond, no sortie |
| Mary | Mother | Does the cooking at Home |
| Ben (Uncle Ben) | Runs the Workshop | Weapon upgrades |

## Enemies

| Name | Notes |
| --- | --- |
| Goblin Queen | Boss (the Warren). Data/logs currently say "Goblin Shaman": a known issue, the player-facing name is Goblin Queen |
| Mountain Deev | Boss |
| Deevoted | Mountain Deev's tentacles; must be destroyed before hitting the boss. Not independent enemies |
| Dark Claw | Pack enemy |
| Black Claw | Dark Claw pack leader. Attacking it makes all Dark Claws target the attacker (inverse taunt); never used alone |
| Archer Goblin, Masher Goblin, Dark Shaman | Regular enemies. Masher Goblin counter-attacks (enemy-side faction role) and is Immovable |
| Dark Worm | Minor; splits into halves |

## Combat terms

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| AP | `ActionPoints`, `APConsumer` | Action points for Move, Attack and abilities. Usable only in the player phase |
| Fixed AP / Shared AP | `APConsumptionMode.PerUnit` / `.Shared` | Per-unit AP vs one family pool with escalating cost per unit. **The game uses Fixed AP (PerUnit)** (D-037); Shared AP is not pursued (half-built code remains) |
| FTP, Family Passive Points (also written FP) | `FamilyTimePoints`, `PointConsumptionMode.FTP` | Family-shared points that pay for Duos only, 2 FTP each (D-035, D-036). Fills on entering a mission, doesn't refill between levels of the same mission. Family Roles no longer cost FTP |
| ATB | `ATBGauge`, `PointConsumptionMode.ATB` | Per-unit gauge; fills while the unit isn't acting; a full gauge converts to an extra AP. **Dropped as the direction** (playtesters found it confusing): the code still runs on `main` until FTP is built out there. Don't use the term in new player-facing text |
| Family Role (family passive) | Faction Role, `FactionRoleHandlerBase`, `*FactionRoleHandler` | Each unit's one reactive passive, triggered by a simple-press QTE prompt (D-034). Costs no FTP; each role has a limit per round instead, refilled at the start of the player turn (Linda 2, Lucy 3, Mark 1, John unlimited, HP-paid) (D-036, D-042). **Intended design; the role limits are not built yet** (to be built on `main`; today's code still charges FTP or ATB) |
| Role uses per round: **Watch** [PROPOSED] | (not built yet; planned "uses per round" field) | Player-facing name for a Family Role's uses left this round, e.g. "Watch 2/2"; Linda's become **Watch Shots** ("Watch Shot 1 of 2"). Awaiting THJ |
| Duo | Cooperation, `UnitsCooperationHandler`, `CooperationEntry` | A deliberate paired ability: AP from the activator plus 2 FTP (D-035; code today checks 1 per partner). Seven in code: John–Lucy, Linda–Lucy, Linda–Toba, John–Linda, Mark–Lucy (Fist Blitz), Mark–Linda (the race), Mark–John (the shout) |
| Synergy (family combo) | | Automatic, conditional effect between family members. E.g. **Sister's Rivalry** (Lucy/Linda kill chain), **Tempest Bloom** |
| Pass-by / tag | `UnitsPassByHandler` | One Bergson moving through another's tile; fills FTP (ATB in the old code) once per turn per pair |
| QTE | `QuickTimeEventHandler`, `QTEBehavior` | Reaction-timing prompt, including during the enemy phase. Role QTEs are a simple press for now; a graded QTE (a small bonus for pressing inside the window) is a later experiment (D-034) |
| Bergson Time | Reactive Interrupt | **Deferred** (D-038): not available in FTP mode, not removed. In code, ATB mode only (key L): pause the enemy turn and act with a unit whose gauge can afford its role |
| Family Skill Point (FSP) | | Earned at certain character levels; spent in the shared Family Skill Tree |
| Run upgrade (rune, relic) | `RunUpgradeSO`, `RunUpgradeTracker` | In-mission upgrade, lost when the mission ends |

## Home terms (scope `thj/home-test`)

Rules and numbers: `design/demo-spec.md`.

| Term | Meaning |
| --- | --- |
| Bond | Relationship level between two family members; unlocks Duos and Synergies at set levels |
| Sortie | Sending a squad on a mission from the map table |
| Station | A Home room or activity a character is seated at (Homestead, Kitchen, Study, Workshop, Yard, ...) |
| Yard Lessons | Training that raises faction stat levels |
| Warren | The Goblin Queen's Warren, on full-moon Day 7 |
| Great Moon | The moon cycle's clock and deadline |
| Omens | Night events; e.g. **Hungry Moon** (Day 7): the Queen gains +1 AP per turn below 50% HP |
| War council, Send-off, Picnic, Fireside Talk, Porch Break | Named Home moments; see the Demo Spec |

## Dungeon safe rooms

Rooms with no fight, in `Content/Levels/DungeonSafeRooms/`. The room name is the level's `levelName`, shown on the mission map node, in the map mission panel and in the combat HUD. Approved by THJ 2026-10-18 (B7).

| Room name | Code | What it does | Source |
| --- | --- | --- | --- |
| Daryani's Shop | `LevelRunUpgradeRoom`, tags `P0.RewardRoom` + `P1.Rune` | An altar drops three run upgrades; take one and the rest vanish. Costs nothing. Then reach the exit | **Daryani**: Children of Morta canon. "Shop": Miso; may be renamed because nothing is sold (see `reports/b7-text-fixes.md`) |
| Anahita's Ashiyan | `LevelHealingRoom`, tag `P0.HealngRoom` (the misspelled id is code-only; leave it) | Stepping in front of the glowing statue heals the whole squad once; the light goes out. Then reach the exit | **Anahita**: Children of Morta canon. **Ashiyan**: Miso invention, not canon |
| Mithra's Gift | `LevelDivineRelicRoom`, `LevelDivineRelicRoom 1`, tags `P0.RewardRoom` + `P1.DivineRelic` | Take the Divine Relic from the altar, then reach the exit | **Mithra**: Children of Morta canon |

"Refuge" was the old objective word for these rooms ("Exit the refuge."). It's being retired from the screen; not a player-facing term.

## Children of Morta canon

To fill with THJ. Until then, propose; don't assert.

| Name | Confirmed | Used in Miso as |
| --- | --- | --- |
| Daryani | Name is canon (THJ, 2026-10-18). Canon role not recorded here yet | Daryani's Shop |
| Anahita | Name is canon (THJ, 2026-10-18). Canon role not recorded here yet | Anahita's Ashiyan |
| Mithra | Name is canon (THJ, 2026-10-18). Canon role not recorded here yet | Mithra's Gift |
