# Glossary

Owner: narrative agent. Names and terms as the game uses them, with the code name when it differs. This file wins over memory. **Started 2026-10-15 from project notes; nothing here is confirmed Children of Morta canon beyond the names.**

## The family (Bergsons)

| Name | Role | Notes |
| --- | --- | --- |
| John | Father; sword, tank | Family Role: shields a nearby attacked family member. No limit per round; paid with his own HP (D-042) |
| Linda | Ranged, support | Family Role **Family Watch**, short form **Watch** (D-328): attacks enemies who end their move in her row or column. **With the quiver on** (default), each shot spends an arrow and there is no per-round limit: the quiver is her limit (D-244, supersedes D-041's 2 per round); still 1 FTP per shot (D-246). With the quiver off, she plays as before the quiver. See [Linda's Quiver](#lindas-quiver) |
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
| Archer Goblin, Masher Goblin, Dark Shaman | Regular enemies. Masher Goblin counter-attacks (enemy-side faction role) and is Immovable. Its first appearance in the demo is M3 (Hold the yard), walking up the east lane; its counter is taught in a line as "every hit brings it a step closer" (`design/m3-text.md` M3.0.1). Its close-up shows the name only |
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
| FTP; on screen **Family Points (FP)** (D-204); formerly written Family Passive Points | `FamilyTimePoints`, `PointConsumptionMode.FTP` | Family-shared points that pay for Duos only, 2 FTP each (D-035, D-036). Fills on entering a mission, doesn't refill between levels of the same mission. Family Roles no longer cost FTP. Not the **Family skill point** (the Family-tree currency, D-439): never call that one "FP" or "Family point" |
| ATB | `ATBGauge`, `PointConsumptionMode.ATB` | Per-unit gauge; fills while the unit isn't acting; a full gauge converts to an extra AP. **Dropped as the direction** (playtesters found it confusing): the code still runs on `main` until FTP is built out there. Don't use the term in new player-facing text |
| Family Role (family passive) | Faction Role, `FactionRoleHandlerBase`, `*FactionRoleHandler` | Each unit's one reactive passive, triggered by a simple-press QTE prompt (D-034). Costs no FTP; each role has a limit per round instead, refilled at the start of the player turn (Linda 2, Lucy 3, Mark 1, John unlimited, HP-paid) (D-036, D-042). Linda's limit is replaced by her quiver (D-244). **Intended design; the role limits are not built yet** (to be built on `main`; today's code still charges FTP or ATB) |
| **Family Watch** (short: **Watch**) | Linda's `*FactionRoleHandler` | Linda's Family Role: the screen name has been "Family Watch"; "Watch" is its approved short form (D-328). Canon. Use only for Linda's role, not as a generic word for any role's uses per round (that counter, not built yet, has no approved name; the old "Watch 2/2" / "Watch Shots" proposal is dropped) |
| **low HP** (tag name: **Bloodied**) | low-HP state (CR-50) | A Bergson or allied Toba at 25% max HP or less (mini bar turns amber-red and pulses). No name on screen today (combat-rules.md Q12). In descriptions and player text, write plain "low HP". **Bloodied** only if it must be a tag or a forced name. Never "Wounded": that's a Home term. Approved by THJ 2026-10-23 (D-153). Not chosen: Faltering |
| Duo | Cooperation, `UnitsCooperationHandler`, `CooperationEntry` | A deliberate paired ability: 0 AP from the activator (D-219) plus 2 FTP (D-035; code today checks 1 per partner). Seven in code: John–Lucy, Linda–Lucy, Linda–Toba, John–Linda, Mark–Lucy (Chained Assault for now, D-223), Mark–Linda (the race), Mark–John (the shout) |
| Synergy (family combo) | | Automatic, conditional effect between family members. E.g. **Sister's Rivalry** (Lucy/Linda kill chain), **Tempest Bloom** |
| Pass-by / tag | `UnitsPassByHandler` | One Bergson moving through another's tile; fills FTP (ATB in the old code) once per turn per pair |
| QTE | `QuickTimeEventHandler`, `QTEBehavior` | Reaction-timing prompt, including during the enemy phase. Role QTEs are a simple press for now; a graded QTE (a small bonus for pressing inside the window) is a later experiment (D-034) |
| Bergson Time | Reactive Interrupt | **Deferred** (D-038): not available in FTP mode, not removed. In code, ATB mode only (key L): pause the enemy turn and act with a unit whose gauge can afford its role |
| **Family skill point** (FSP); formerly "Family point" in the Bond Lite plans | | On screen **Family skill point**, lower-case "skill point" (THJ, D-439). Earned at certain character levels and as story rewards (the Yard, D-173); spent in the shared Family tree (the Family tab of the skill tree). **Never shorten it to "Family point" or "FP" on screen:** **Family Points (FP)** is the combat pool that pays for Duos (D-204), a different thing. Plans and code may still say "Family point"; write Family skill point |
| **skill points** | | Points each Bergson earns on level-up, spent in their own skill tree at the Grandma Table. On screen in the Skill Tree page: "Bergsons earn skill points as they level up." (placeholder, `thj/bond-lite`). Approved by THJ 2026-11-08 |
| Run upgrade (rune, relic) | `RunUpgradeSO`, `RunUpgradeTracker` | In-mission upgrade, lost when the mission ends |

## Linda's Quiver

Built on `thj/linda-quiver`, merged into `main` 2026-10-29 (D-326). Global switch `lindaQuiverEnabled` in GlobalSettings, on by default; off, Linda plays as before the quiver and Encore is hidden (D-314, D-320). The quiver is shown, not written: a HUD quiver by her portrait, small pips under her and arrow art on tiles, with no counts or labels drawn on the board (D-293, D-297, D-301). Every tooltip string below is still tagged `[PLACEHOLDER]` in code (not signed off); Encore's description is final (D-327).

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **quiver** (Linda's Quiver) | `LindaQuiver`; HUD `LindaQuiver.prefab` with `QuiverUI`; pips `QuiverPipsView` | The arrows Linda carries. Starts every level full. Each arrow ability spends one: Bow Attack, her Family Role shot, Explosive Crescendo, Duos in which she fires. At 0 they grey out (Explosive Crescendo in super time still fires at 0, D-251). Arrows are never lost; they all come back at level end. Approved D-241. Tooltip reasons: "No arrows"; on a shared Duo panel "Linda has no arrows" |
| **Quiver Size** (stat) | `Stat_LQuiverSize` (`LQuiverSize` in `StatAttributes.asset`; id unchanged) | How many arrows the quiver holds. Base 3 (D-316, was 4); a stat so the skill tree, Workshop and run upgrades can change it with ordinary modifiers (D-319). No Workshop item yet. Stat title "Quiver Size" (D-329), formerly "Linda Quiver Size" |
| **Encore** | `Linda_Ability_Recall` (**formerly Recall**; code name kept) | Every grounded arrow flies straight back to her quiver, through walls and enemies, locked stacks included, as many as the quiver has room for. No damage. 2 AP (D-302), cooldown 2. Usable only with at least one grounded arrow and room in the quiver (D-256): tooltip reasons "No grounded arrows" / "Quiver full". Name approved D-262 (musical, like her kit). Always write Encore. Description (THJ's final text, no placeholder, D-327): "By her call, every grounded arrow flies home to her quiver. (2 AP)" |
| **grounded arrows** | `GroundedArrowField`, `GroundedArrowStacks`, `QuiverArrow` | Arrows lying on tiles after a shot: an arrow lands at the end of its flight, or at the last open cell before something blocks it. The game's wording is "grounded" ("No grounded arrows"). Stacks of two or more show a small `xN`. A stack under a living enemy is **locked** (subtle dark tint): it can't be picked up until the enemy leaves or dies. "Locked" is a design word, not on screen |
| **pickup** (walking over arrows) | `GroundedArrowField.Pickup` | Any living unit of Linda's own faction stepping on an unlocked stack takes it, up to the quiver's room; an arrow landing on a Bergson's tile is taken at once. Other factions' allies (allied Toba) don't pick up (D-254). Empty-quiver hint: "No arrows; walk over them or use Encore." |
| **hand-back** | `HandBackLines`, `HandBackLineChooser`; kills: `LindaQuiver.KillHandBack` | The beat when an arrow comes back to Linda by someone else's hand: the picker's line, the arrow tossed to her, her reply. Non-blocking, about 0.6 s (D-247). Also when John's or Toba's primary attack kills an enemy standing on her arrows: they go straight to the quiver, no step needed (D-307); not allied Toba (D-310). A design word, not on screen. Every hand-back line is still `[PLACEHOLDER]` |
| **Catch & Return** (synergy) | `ProjectileCatchAndReturn` on `Unit_Mark`; synergy event "Catch & Return" | Open by default (D-177). When Linda's basic arrow reaches Mark from 2 or more cells (D-274), a QTE offers the catch. **Quiver on:** pressed, the arrow stops at Mark and flies back, damaging on the way, ending in Linda's hands and going back into her quiver (D-257, D-260, D-261); not pressed, it flies on past him like a normal shot. **Quiver off:** pressed, the copy returns to Linda damaging on the way, no arrow back (D-315, D-320). No AP refund, for bow and Watch arrows alike, ever (D-218, D-332) |
| **Return to Sender** | Family-tree node (Catch & Return's upgrade) | **Effect withdrawn (D-332, reverses D-228):** Catch & Return never refunds AP, so this node's effect is open again; the name was approved for the refund and may not fit the new effect. Don't use "Return to Sender" or "shot back" in text until the designer's new effect is decided. **Not built in data** (no asset uses the name) |

## Lucy's Cyclone

Scope all: built on `thj/cyclone`, merged into `main` 2026-11-22 (`049897aae`, D-600); rows below match that build (the 2026-11-19 reset, D-580 to D-588, and the controls, D-589 to D-597, D-601). Round 2 texts were proposed in `plans/2026-11-17-cyclone-round2-texts.md`; the shipped descriptions are still working text (D-544). Rows marked **proposed** are not approved; the rest are names already in the game.

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Cyclone** | `Lucy_Cyclone_Ability`, `CycloneEntity` | Lucy's storm, summoned on a cell within 3. Lasts 3 enemy turns. Cast on an empty cell, or on an enemy to knock it away and hit it (D-585, D-587). Most enemies can't walk or shoot through it; the family passes (D-584). Enemies no longer avoid it (D-588). Clicking it in the player's turn, when the Steer is usable, selects Lucy and opens the Steer (D-589). Always capital C ("Lucy's Cyclone"); the Tempest Bloom node text still writes "cyclone" (to fix) |
| **Whirl** (proposed as an on-screen verb: "it Whirls") | `CycloneWhirlSteps`, log id `Whirl` | What the Cyclone does on cast, after each enemy turn and at the end of every Steer: pulls enemies on its arms 1 cell in, then hits the enemies beside it. After a Steer, it also hits the enemies hit on the way if they end up beside it, as it does the knocked enemy (D-648, D-587). Capital W, used as a verb ("then it Whirls") and a noun ("the Whirl"). The log already says "Whirl" |
| **Steer** | `Lucy_Ability_Steer` | Takes the Cyclone's button while it is out. 1 AP, cooldown 1: one Steer per turn (D-601, reversing D-591's cooldown 0; no free first Steer, D-597). Glides the Cyclone along any route up to 3 cells, turns allowed, around walls, through enemies and the family, hitting each enemy it passes once on the way (D-586); the Whirl hits them again if they end up beside it (D-648, reversing D-583). An enemy on the stop is knocked onward and hit (D-581, D-587). Then it Whirls. Nothing rides along (D-582). Mark's Command can also steer it (D-592). Picking the Steer makes the Cyclone pulse (D-590) |
| **knock / knocked** | Steer knock, cast knock; log id `Knock` (cast), "knocked N and hit it" (Steer line) | The enemy on the Steer's stop is moved one cell onward along the last step; if blocked, to the Cyclone's right, else its left (relative to the move); with no free cell, that stop isn't offered (D-581). Casting the Cyclone on an enemy knocks it the same way, onward meaning away from Lucy (D-585). Either way the knocked enemy takes a full Cyclone hit, and after a Steer also the Whirl's hit (D-587). On screen: "knocked onward and hit" (Steer), "knock it away and hit it" (Cyclone). The decisions' word; the on-screen lines are working text. Not "push" or "shove" on screen (`CycloneShoveSteps` is code only) |
| **Command** (Mark's, steering the Cyclone) | `Mark_Ability_Attack_Command`, effect `AEffectCommandSteersCyclone` | Mark's Command can pick Lucy's Cyclone as its first target, then a stop the Steer could reach: same route, hits, knock and Whirl as Lucy's Steer, credited to Lucy's Cyclone. Mark pays his own Command (1 AP, cooldown 1); Lucy's Steer, AP and cooldown are untouched (D-592). With Mark's Weak upgrade, the knocked enemy on the stop also becomes Weak; the Cyclone never does (D-594). The Command's first pick reaches any cell within Mark's range, across missing tiles, for every target (D-596). Description (working text): "Command another unit to move. It can also steer Lucy's Cyclone." Lower-case "steer" there is the verb; "Steer" capitalised is Lucy's ability |
| **beside it** (proposed) | touching cells, `CycloneRules.TouchLabel` | The 4 cells touching the Cyclone: where the Whirl hits and where a burst hits. On screen always "beside it" / "beside the Cyclone"; "touching cells" is a design word |
| **arms** (proposed) | arm cells | The 4 straight lines out from the Cyclone, 2 cells long; enemies on them are pulled 1 cell in. Already on screen in the Cyclone description ("enemies on its arms"). Keep it |
| ~~carry / carried~~ (**dropped**) | carry planner (removed) | Dropped with the 2026-11-19 reset (D-580, D-582): nothing rides with a Steer; the Whirl's pull at the new spot is the only movement. Never write "carry" or "carried" for the Cyclone. The log no longer says "carried N" |
| ~~drag / drags~~ (**dropped**) | riders' grab/drag beats (removed) | Was flavour for the carry. Dropped with it (D-580, D-582). Don't write "drags" for the Cyclone; the Whirl "pulls" |
| ~~wobble~~ (**dropped**; design word, never on screen) | heavy-warning wobble (D-558, removed) | The Cyclone shook when a heavy enemy could reach it. Dropped (D-580, D-584): it could warn wrongly |
| **burst** (proposed) | C3b burst | When a heavy enemy walks into the Cyclone, it bursts: one hit on that enemy and every enemy beside it, then it is gone (kept in the reset, D-584) |
| heavy (design word, not on screen) | `EntityState.Unmovable` or footprint larger than 1 cell | Masher Goblin, Goblin Queen, Mountain Deev. On screen, name the enemy or write "this enemy"; don't show "heavy" |
| cross (design word, not on screen) | `CycloneCrossView` | The Cyclone's area (arms plus the cells beside it). The board no longer draws a cross shape (eye tint and arm-tip chevrons), so keep it off screen |
| **Cyclone Power** | skill-tree node `Stat_DMG` on the cast | Cyclone hits deal 3 times Lucy's damage without it, 4 at level 1, 5 at level 2 |
| **Howling Gale** | `LucyCycloneWeak` (unlockable and `RU_LucyCycloneWeak`) | Weak for 2 turns on every enemy a Cyclone hit lands on (cast, Steer, end of turn, burst) |
| ~~Gust~~ (**retired**) | | The old name for the Steer's closing pull. Retired everywhere by THJ (2026-11-17, round 2): a Steer ends in a Whirl. Never write "Gust" |
| Eye of the Storm (suggestion only) | | Was suggested for the carry rule (now dropped) or round 2 as a whole. A design label for now, with nothing to name since the reset; not on screen unless THJ picks it |

## M3: Hold the yard

Scope all (`main`). Approved by THJ 2026-11-26 with `design/m3-text.md` (D-731 to D-735). Toba, the Rootwell and Ryker first appear here, but their rows stay proposed (`m4-text.md` §6, `m1-ridge-redesign-text.md` §10): no canon is claimed.

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Hold the yard** | mission asset still `M2 - The Trail`; level prefab `GB_m3-defence-3` | M3's on-screen name |
| **Barricade** | `Unit_Barricade` (a `Unit_Rock` variant) | M3's breakable barrier unit: Neutral, Unmovable, 8 HP in M3. Goblins can't pass it and attack it; the family walks through it, can't stop on it and can't hurt it; no repair. On screen: unit title "Barricade" and "the barricades". Not "barrier" on screen (D-731). Not chosen: Palisade, Stakes |
| **the wall** (speech only) | | A row of three barricades across a neck, as the characters say it. A spoken word only, never a term on screen (D-735) |
| **the stone** | stone units at 4,12 (five variants) | The rock on the cave mouth that **Mark** pushes in M3: one notch at each family turn start for 4 turns, then it rolls away. Written "the stone" in lines; unit title "Stone" (placeholder). Not "Fallen Rock" (that is M1) |
| the pick (design word, not on screen) | | The free squad seat in the old M3 draft. No longer used in M3 (the squad is Linda and Lucy, fixed); still used in `m4-text.md` if M4 keeps a free seat |

## Home terms (scope `thj/home-test`; Bond row also `thj/bond-lite`)

Rules and numbers: `design/demo-spec.md`.

| Term | Meaning |
| --- | --- |
| Bond | Relationship level between two family members; unlocks Duos and Synergies at set levels. **On screen on `thj/bond-lite`** (Bond Lite), written `<A> & <B>'s Bond, Lv N`: the locked Family-tree node line "Opens with Linda & Lucy's Bond, Lv 2" (`BondNodeGate.LockLine`) and the Yard narrator line "Linda & Lucy's Bond reached Lv 2." (placeholder). Keep that exact shape (ampersand, "'s Bond", "Lv N") so the two lines read as one thing. In Bond Lite it opens Family-tree nodes for that pair (Linda & Lucy only; Lv 2 opens Sister's Rivalry and Tempest Bloom), it is raised by Home scenes (the Yard), and there is no Bond meter (D-433). Approved by THJ 2026-11-08 |
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
