# Glossary

Owner: narrative agent. Names and terms as the game uses them, with the code name when it differs. This file wins over memory. **Started 2026-10-15 from project notes; nothing here is confirmed Children of Morta canon beyond the names.**

## The family (Bergsons)

| Name | Role | Notes |
| --- | --- | --- |
| John | Father; sword, tank | Family Role: shields a nearby attacked family member. No limit per round; paid with his own HP (D-042) |
| Linda | Ranged, support | Family Role (called Watch in design notes; on screen today "Linda's FactionRole"): attacks enemies who end their move in her row or column. **With the quiver on** (default), each shot spends an arrow and there is no per-round limit: the quiver is her limit (D-244, supersedes D-041's 2 per round); still 1 FTP per shot (D-246). With the quiver off, she plays as before the quiver. See [Linda's Quiver](#lindas-quiver) |
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
| Black Claw | Dark Claw pack leader. Attacking it makes every Dark Claw within 5 cells target the attacker (inverse taunt); never used alone |
| Archer Goblin, Masher Goblin, Dark Shaman | Regular enemies. Masher Goblin counter-attacks (enemy-side faction role) and is Immovable |
| Dark Worm | Minor; splits into halves |

### Enemy abilities and kin

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Dark Mending** | Dark Shaman heal (`DarkShaman/Heal/`, state `Heal`) | The Dark Shaman heals one dark ally at 75% HP or less, within 3 cells (not itself): 10 HP at Standard, 1 AP, cooldown 2 (D-150; stunned or dormant allies too, D-151). Not shown on screen today (enemies.md Q7). Description: "Heals a nearby dark ally for 10 HP." Avoid "wounded" in the text: it's a Home term. Approved by THJ 2026-10-23 (D-153). Not chosen: Brood Mending, Blight Salve |
| **dark enemies** (also **corruption enemies**, **dark brood**) | `Kin.Dark` (hidden GTag) | The units Dark Mending can heal: Dark Claw, Black Claw, Dark Worm (split halves too), Dark Shaman. Stays a hidden tag, never shown on screen today. Player-facing words, in order of preference: **dark enemies** and **corruption enemies** (what Children of Morta 1 called them, per THJ), **dark brood** also fine. Approved by THJ 2026-10-23 (D-153). Not chosen: "the Brood" |

## Combat terms

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| AP | `ActionPoints`, `APConsumer` | Action points for Move, Attack and abilities. Usable only in the player phase |
| Fixed AP / Shared AP | `APConsumptionMode.PerUnit` / `.Shared` | Per-unit AP vs one family pool with escalating cost per unit. **The game uses Fixed AP (PerUnit)** (D-037); Shared AP is not pursued (half-built code remains) |
| FTP; on screen **Family Points (FP)** (D-204); formerly written Family Passive Points | `FamilyTimePoints`, `PointConsumptionMode.FTP` | Family-shared points that pay for Duos only, 2 FTP each (D-035, D-036). Fills on entering a mission, doesn't refill between levels of the same mission. Family Roles no longer cost FTP |
| ATB | `ATBGauge`, `PointConsumptionMode.ATB` | Per-unit gauge; fills while the unit isn't acting; a full gauge converts to an extra AP. **Dropped as the direction** (playtesters found it confusing): the code still runs on `main` until FTP is built out there. Don't use the term in new player-facing text |
| Family Role (family passive) | Faction Role, `FactionRoleHandlerBase`, `*FactionRoleHandler` | Each unit's one reactive passive, triggered by a simple-press QTE prompt (D-034). Costs no FTP; each role has a limit per round instead, refilled at the start of the player turn (Linda 2, Lucy 3, Mark 1, John unlimited, HP-paid) (D-036, D-042). Linda's limit is replaced by her quiver (D-244). **Intended design; the role limits are not built yet** (to be built on `main`; today's code still charges FTP or ATB) |
| Role uses per round: **Watch** [PROPOSED] | (not built yet; planned "uses per round" field) | Player-facing name for a Family Role's uses left this round, e.g. "Watch 2/2"; Linda's become **Watch Shots** ("Watch Shot 1 of 2"). Awaiting THJ. The Watch Shots part is moot while the quiver replaces Linda's per-round limit (D-244) |
| **low HP** (tag name: **Bloodied**) | low-HP state (CR-50) | A Bergson or allied Toba at 25% max HP or less (mini bar turns amber-red and pulses). No name on screen today (combat-rules.md Q12). In descriptions and player text, write plain "low HP". **Bloodied** only if it must be a tag or a forced name. Never "Wounded": that's a Home term. Approved by THJ 2026-10-23 (D-153). Not chosen: Faltering |
| Duo | Cooperation, `UnitsCooperationHandler`, `CooperationEntry` | A deliberate paired ability: 0 AP from the activator (D-219) plus 2 FTP (D-035; code today checks 1 per partner). Seven in code: John–Lucy, Linda–Lucy, Linda–Toba, John–Linda, Mark–Lucy (Chained Assault for now, D-223), Mark–Linda (the race), Mark–John (the shout) |
| Synergy (family combo) | | Automatic, conditional effect between family members. E.g. **Sister's Rivalry** (Lucy/Linda kill chain), **Tempest Bloom** |
| Pass-by / tag | `UnitsPassByHandler` | One Bergson moving through another's tile; fills FTP (ATB in the old code) once per turn per pair |
| QTE | `QuickTimeEventHandler`, `QTEBehavior` | Reaction-timing prompt, including during the enemy phase. Role QTEs are a simple press for now; a graded QTE (a small bonus for pressing inside the window) is a later experiment (D-034) |
| Bergson Time | Reactive Interrupt | **Deferred** (D-038): not available in FTP mode, not removed. In code, ATB mode only (key L): pause the enemy turn and act with a unit whose gauge can afford its role |
| Family Skill Point (FSP) | | Earned at certain character levels; spent in the shared Family Skill Tree |
| Run upgrade (rune, relic) | `RunUpgradeSO`, `RunUpgradeTracker` | In-mission upgrade, lost when the mission ends |

## Linda's Quiver

Built on `thj/linda-quiver`, merged into `main` 2026-10-29 (D-326). Global switch `lindaQuiverEnabled` in GlobalSettings, on by default; off, Linda plays as before the quiver and Encore is hidden (D-314, D-320). The quiver is shown, not written: a HUD quiver by her portrait, small pips under her and arrow art on tiles, with no counts or labels drawn on the board (D-293, D-297, D-301). Every tooltip string below is still tagged `[PLACEHOLDER]` in code.

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **quiver** (Linda's Quiver) | `LindaQuiver`; HUD `LindaQuiver.prefab` with `QuiverUI`; pips `QuiverPipsView` | The arrows Linda carries. Starts every level full. Each arrow ability spends one: Bow Attack, her Family Role shot, Explosive Crescendo, Duos in which she fires. At 0 they grey out (Explosive Crescendo in super time still fires at 0, D-251). Arrows are never lost; they all come back at level end. Approved D-241. Tooltip reasons: "No arrows"; on a shared Duo panel "Linda has no arrows" |
| **Linda Quiver Size** (stat) | `Stat_LQuiverSize` (`LQuiverSize` in `StatAttributes.asset`) | How many arrows the quiver holds. Base 3 (D-316, was 4); a stat so the skill tree, Workshop and run upgrades can change it with ordinary modifiers (D-319). No Workshop item yet. The stat title in data is "Linda Quiver Size"; a shorter "Quiver Size" is proposed, not approved |
| **Encore** | `Linda_Ability_Recall` (**formerly Recall**; code name kept) | Every grounded arrow flies straight back to her quiver, through walls and enemies, locked stacks included, as many as the quiver has room for. No damage. 2 AP (D-302), cooldown 2. Usable only with at least one grounded arrow and room in the quiver (D-256): tooltip reasons "No grounded arrows" / "Quiver full". Name approved D-262 (musical, like her kit). Always write Encore. The data description is stale (still says 1 AP); see the narrative proposal |
| **grounded arrows** | `GroundedArrowField`, `GroundedArrowStacks`, `QuiverArrow` | Arrows lying on tiles after a shot: an arrow lands at the end of its flight, or at the last open cell before something blocks it. The game's wording is "grounded" ("No grounded arrows"). Stacks of two or more show a small `xN`. A stack under a living enemy is **locked** (subtle dark tint): it can't be picked up until the enemy leaves or dies. "Locked" is a design word, not on screen |
| **pickup** (walking over arrows) | `GroundedArrowField.Pickup` | Any living unit of Linda's own faction stepping on an unlocked stack takes it, up to the quiver's room; an arrow landing on a Bergson's tile is taken at once. Other factions' allies (allied Toba) don't pick up (D-254). Empty-quiver hint: "No arrows; walk over them or use Encore." |
| **hand-back** | `HandBackLines`, `HandBackLineChooser`; kills: `LindaQuiver.KillHandBack` | The beat when an arrow comes back to Linda by someone else's hand: the picker's line, the arrow tossed to her, her reply. Non-blocking, about 0.6 s (D-247). Also when John's or Toba's primary attack kills an enemy standing on her arrows: they go straight to the quiver, no step needed (D-307); not allied Toba (D-310). A design word, not on screen. Every hand-back line is still `[PLACEHOLDER]` |
| **Catch & Return** (synergy) | `ProjectileCatchAndReturn` on `Unit_Mark`; synergy event "Catch & Return" | Open by default (D-177). When Linda's basic arrow reaches Mark from 2 or more cells (D-274), a QTE offers the catch. **Quiver on:** pressed, the arrow stops at Mark and flies back, damaging on the way, ending in Linda's hands and going back into her quiver (D-257, D-260, D-261); not pressed, it flies on past him like a normal shot. **Quiver off:** pressed, the copy returns to Linda damaging on the way, no arrow back (D-315, D-320). No AP refund (D-218) |
| **Return to Sender** | Family-tree node (Catch & Return's upgrade) | Once per turn, the catch also refunds Linda's shot (+1 AP). Name approved D-228. **Not built in data yet** (no asset uses the name) |

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
| Daryani's Wares | `LevelRunUpgradeRoom`, tags `P0.RewardRoom` + `P1.Rune` | An altar drops three run upgrades; take one and the rest vanish. Costs nothing. Then reach the exit | **Daryani**: Children of Morta canon, the merchant (THJ). "Wares": Miso (D-060). **Formerly "Daryani's Shop"** (playtest builds; the prefab's `levelName` may still say it until the rename lands) |
| Anahita's Ashiyan | `LevelHealingRoom`, tag `P0.HealngRoom` (the misspelled id is code-only; leave it) | Stepping in front of the glowing statue heals the whole squad once; the light goes out. Then reach the exit | **Anahita**: Children of Morta canon. **Ashiyan**: Miso invention, not canon |
| Mithra's Gift | `LevelDivineRelicRoom`, `LevelDivineRelicRoom 1`, tags `P0.RewardRoom` + `P1.DivineRelic` | Take the Divine Relic from the altar, then reach the exit | **Mithra**: Children of Morta canon |

"Refuge" was the old objective word for these rooms ("Exit the refuge."). It's being retired from the screen; not a player-facing term.

## Children of Morta canon

To fill with THJ. Until then, propose; don't assert.

| Name | Confirmed | Used in Miso as |
| --- | --- | --- |
| Daryani | Canon: the merchant (THJ, 2026-10-18) | Daryani's Wares (formerly Daryani's Shop) |
| Anahita | Name is canon (THJ, 2026-10-18). Canon role not recorded here yet | Anahita's Ashiyan |
| Mithra | Name is canon (THJ, 2026-10-18). Canon role not recorded here yet | Mithra's Gift |
