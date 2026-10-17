# GDD open questions: answer sheet

For THJ. Collected 2026-10-17 from the Open questions section of each GDD page. Write your answer on the `A:` line under each question and tell the coordinator. Questions are copied verbatim; the source page and ID are in each heading. Some repeat across pages (Revenge: Combat Q5 and Family Q5; Catch & Return: Family Q9 and Mark Q2; Fist Blitz name: Family Q2 and Mark Q5; John's ×0.5: Family Q8 and John Q2; Toba's missing role: Family Q1 and Toba Q1; FTP cap: Combat Q2 and Home Q5; briefing slips: Narrative Q4 and Missions Q7). Answer once and write "see X" on the other. This sheet is temporary: once answered, the answers go into the pages and decisions.md, and this file is deleted.

## Combat rules (`combat-rules.md`)

### Combat rules Q1

FTP's on-screen name: FTP, FP, Family Points (the stat descriptions), Family Time Points (the code) or Family Passive Points (the glossary)?

A: 

### Combat rules Q2

How should the FTP maximum be set? Today it is the sum of the mission roster's FP values (John 5, Linda 2, Lucy 3, Mark 3, Toba 1, plus the family stat), and the pool starts full. The Demo Spec describes 3 × (heroes − 1) on `thj/home-test`.

A: 

### Combat rules Q3

Leftover AP is lost at the end of the turn. Should it do something with FTP (for example, fill FTP)?

A: 

### Combat rules Q4

Family Super Time: on `main` only the Goblin Queen's death triggers it, and it costs nothing. Keep it as a feature? What should it cost, and how should the player trigger it?

A: 

### Combat rules Q5

Revenge on an ally's death: a designed family mechanic, or legacy? Where should it live in this document?

A: 

### Combat rules Q6

Family members tagged Stunned are not skipped (only Inactive skips their turn). Intended?

A: 

### Combat rules Q7

Pass-by and the Family Trinket add FTP through a message that passes a decimal number to a whole-number function. Unity may reject such a call, in which case both add nothing. Check the Console in play ("Failed to call function ProduceFTP").

A: 

### Combat rules Q8

John's Family Super Time pull, and probably Mark's Vault push, move Immovable units (the Masher, the Deev). Fix?

A: 

### Combat rules Q9

After a death, FTP is capped below its maximum until the next level, so the pool can't be full and Family Super Time can't fire for the rest of that level. Intended?

A: 

## Family systems (`family-systems.md`)

### Family systems Q1

Toba has no Family Role and no pass-by entry. Is that intended for the newcomer, or missing?

A: 

### Family systems Q2

The Mark–Lucy Duo's name: Fist Blitz (glossary) or Chained Assault (combat balance notes)? The other Duos need player-facing names too.

A: 

### Family systems Q3

Linda's trigger. Answered from the data: an enemy that *ends* its move in her lane (the glossary's rule), pushes and Command moves included. Close, or did the balance notes' "any move into it" mean a change?

A: 

### Family systems Q4

Are Papa's Shelter and Shield Flare Synergies, or character passives?

A: 

### Family systems Q5

Revenge (on an ally's death) and Family Super Time exist in code. Do they belong here?

A: 

### Family systems Q6

The pillars mention "trio abilities", and the family tree has a Trio group. Is Trio a system of its own?

A: 

### Family systems Q7

Mark's Continuous Attack still costs FTP (1, then +1 per use in the same turn). D-036 keeps FTP for Duos. Make it free with a limit, or keep the cost?

A: 

### Family systems Q8

John's redirected hit: the data uses a fixed ×0.5 (the role preset's 0.3 / 0.2 / 0.1 rows and its radius upgrades are read by nothing); the 2026-10-08 notes say 0.4. Which is intended, and should the role upgrade?

A: 

### Family systems Q9

Catch & Return on `main` bounces the arrow back without the +1 AP refund (`returnMode` BounceBack). Intended?

A: 

### Family systems Q10

Duos cost the activator 0 AP, except Mark–Lucy (1), because the partner presets are free. Should every Duo cost the activator 1 AP as designed?

A: 

### Family systems Q11

Basic attacks have no cooldown on `main`, so rewards that make a basic attack "ready again" (Sisters' Rivalry, the Footrace, Father's Resolve, Revenge) add nothing. Give basic attacks a cooldown, or change the rewards?

A: 

## Progression and economy (`progression-economy.md`)

### Progression and economy Q1

How should FSP and a family level work? As built, a character's tree earns 1 FSP at 2, 3 and 5 SP spent (the design said the first 3 SP). Keep that? And should the hidden family level fed by Bond be built?

A: 

### Progression and economy Q2

Skill-tree tiers: the data unlocks nodes at 0, 0, 2, 2, 3 and 5 SP spent; [`player-skill-trees.md`](../player-skill-trees.md) says one tier per SP spent (0, 1, 2, 3). Which is intended?

A: 

### Progression and economy Q3

Kill XP goes to the whole squad, fallen members included, and completion XP only to the final level's squad. Characters a level places themselves share it too: Linda in M1, Toba in every level of M4 after his duel, before he joins. Intended?

A: 

### Progression and economy Q4

Restarting a level keeps the XP and gold collected in the failed attempt. Close it?

A: 

### Progression and economy Q5

Shin Armor is authored in the chest socket, where Lucy's Robe and Mark's Tunic also go. Legs intended?

A: 

### Progression and economy Q6

Divine Relics: keep the walk-on pickup (3 shared uses, no choice) or move relics to run upgrades (the relic kind)? Black Despair is in no level; place it or cut it?

A: 

### Progression and economy Q7

Always Ready only works with ATB but is still offered on `main`. Remove it from the altar?

A: 

### Progression and economy Q8

The unlock `JohnResolve` is used nowhere, and Cyclone Weak (Howling Gale) exists only as a run upgrade. Keep both?

A: 

### Progression and economy Q9

Answered from the code: flat gear bonuses are added after every multiplier, so the Vitality Brooch adds exactly +3 to +15 max HP and the family Health stat doesn't scale it. Close, or should gear scale?

A: 

### Progression and economy Q10

The Trinket potency stat (`Stat_FPP`) is sold for 10 / 15 / 40 Gold, but nothing reads it: the Family Trinket always gives +5 FTP. Wire it up, or remove it from the Family Room?

A: 

## Enemies (`enemies.md`)

### Enemies Q1

The Goblin Queen is still titled "Goblin Shaman" in the data, which is also her save key. Rename it in a way that keeps saves working?

A: 

### Enemies Q2

Should the Masher's counter have a limit per turn? (open since the October balance pass). The prefab also carries two counter components, one with hand-made ids; if both start, it could counter twice.

A: 

### Enemies Q3

The Worm's split values (12 / 6 / 4 HP) date from before its HP went to 28. Children spawned with odd HP in playtests. Rebalance the split?

A: 

### Enemies Q4

The glossary says attacking a Black Claw turns *all* Dark Claws; the data limits it to those within 5 cells. Which is intended?

A: 

### Enemies Q5

The Deev's tentacles and immunity are unused on `main`: M12 removes the Summon that spawns the Deevoted and switches the immunity on. If it ran, the immunity would end when *any* other enemy dies, and nothing removes the tentacles' Inactive status. Restore the Summon and tie the immunity to the tentacles, as designed?

A: 

### Enemies Q6

Enemy introductions have no text yet. Who writes them (narrative)?

A: 

### Enemies Q7

Some enemy abilities carry copied titles and text: the Queen's charge and the Deev's pools are titled "Shield Dash" with John's description, the Deev's wave "Taunt". Fix before any screen lists enemy abilities?

A: 

## Missions and structure (`missions-structure.md`)

### Missions and structure Q1

M8 to M14 can't be reached on `main` (the gate before M8, M9 and M11 has no input), and MX is outside the graph. Cut content, a later chapter, or a wiring slip?

A: 

### Missions and structure Q2

"No More Waiting" is required for M4 and M6 (both M3s feed one AND gate); [`reward-balance.md`](../reward-balance.md) says Mark's intro gates nothing. Which is intended?

A: 

### Missions and structure Q3

M1's roster is John and Lucy, but its second level places Linda alone (no deploy slots) and its third places all three. Is this Linda's introduction? It also gives Linda a share of M1's XP (PR-5).

A: 

### Missions and structure Q4

"Into the Rootwell" has 6 fights and a copy of the Divine Relic room (a second Heavenly Sword). Its labels run (1/5) to (5/5) with a "(4.5/5)" in between. Fix the labels, and keep the relic room?

A: 

### Missions and structure Q5

M6: the map shows LevelE2-C2 twice (a false choice), and the Healing Room is forced. `reward-balance.md` describes a different route. Which is intended?

A: 

### Missions and structure Q6

M11's levels have no links, so only the first plays; MX lists the same level twice, and it ends after one. Fix?

A: 

### Missions and structure Q7

Text slips: the M2 file says "Ryler" and the title "Ryker"; "No More Waiting" ends with a space (it is also the save key); the M12–M14 titles include the file prefix ("M12 - The Mountain Deev"); M12–M14 reuse other missions' descriptions; M9's description says "Dom"; mission number 3 is used twice and MX is −1. Level labels don't match the routes (LevelE2-C3 says "(2/3)", MX's level "(1/2)"), and C3 of "No More Waiting" shows a literal "{0}" in its objective.

A: 

### Missions and structure Q8

Most levels place a fixed cast instead of using deploy slots, so the roster and who actually plays can differ ("No More Waiting", M13, M14). Should levels use deploy slots, as many as the largest squad that can reach them?

A: 

### Missions and structure Q9

Toba's duel: answered from the data (the level makes the stranger hostile; Toba yields below 30% of 60 HP and acts first). Close, or tune the threshold?

A: 

### Missions and structure Q10

Chapters, a main dungeon and deadlines: planned for `main`, or only through Home?

A: 

### Missions and structure Q11

The Healing Room heals 0.5 × the HP cap stat (9999), a full heal in effect; the Demo Spec's Rest Room heals 10%. Which size is intended for `main`?

A: 

### Missions and structure Q12

Level2-C2 in "Into the Rootwell" has no loss when every hero is down (its loss objective was re-pointed to the stag), so a wipe may leave the level stuck. Check in play and fix?

A: 

### Missions and structure Q13

M10's briefing promises a Corruption beast on the sacred tree; the level holds a Goblin Queen at 150 HP. Which is intended?

A: 

## Home (`home.md`)

### Home Q1

The Fireside payoff: what else can a pair earn (today: first Duo free, first Family Role free, or FP cap +2)?

A: 

### Home Q2

Does the full game keep resetting Lessons, Home Upgrades and weapon levels at each new cycle?

A: 

### Home Q3

Should the dungeon take 4 of the 5 characters, or the whole family?

A: 

### Home Q4

HP bonuses from Lessons and Home Upgrades multiply each other. Intended, or should they add?

A: 

### Home Q5

The FTP values at Home assume a small FTP cap; they need the real cap ([Combat rules](combat-rules.md#open-questions) Q2).

A: 

## Narrative and world (`narrative-world.md`)

### Narrative and world Q1

Canon: the family's relationships, Margaret, Adam (John's father?), Ryker (who or what is she?), the masked man, Waya, the Pathmother and Anai-Mera. Which are Children of Morta canon, and which are new to Miso?

A: 

### Narrative and world Q2

Is the Persian thread (Deev, Anahita, Mithra, Hegmataneh) intended as a world theme, and does it fit Children of Morta's lore?

A: 

### Narrative and world Q3

Toba is new to the family: how does his arc (the duel, then joining) fit the canon family?

A: 

### Narrative and world Q4

Briefing slips: M9's says "Dom"; M11's reads "why Ryker called as Waya"; M12–M14 reuse other briefings; M2's file says "Ryler" ([Missions and structure](missions-structure.md#open-questions) Q7).

A: 

### Narrative and world Q5

Who writes the enemy introductions and Home lines (the narrative agent, THJ, or a writer)?

A: 

## Character sheet: John (`characters/john.md`)

### Character sheet: John Q1

Wrath: +35% per stack in the asset, +40% in the 2026-10-08 notes. Which is intended?

A: 

### Character sheet: John Q2

His Shield role takes the hit at a factor of 0.5; the notes say 0.4 ([Family systems](../family-systems.md#open-questions) Q8).

A: 

### Character sheet: John Q3

The shared ability on every member but Toba is titled Cleanse in the data, while its sounds say Dedication ([Characters](README.md)). Which name should players see?

A: 

## Character sheet: Linda (`characters/linda.md`)

### Character sheet: Linda Q1

Power-Piercing Arrows exists as both a skill node and a run upgrade; the run upgrade can push the decay past 1.0 (more damage on later targets). Cap it, or rename one?

A: 

### Character sheet: Linda Q2

Her role has no limit yet and costs 1 FTP ([Family systems](../family-systems.md) FR-3 to FR-5).

A: 

## Character sheet: Lucy (`characters/lucy.md`)

### Character sheet: Lucy Q1

Sidewinders is set up differently from every other numeric node (upgrade mode 0 instead of 1). It likely explains the "Maxed Out" with no points spent and the "+3 in game" seen in playtests. Fix the data?

A: 

### Character sheet: Lucy Q2

Names for the Linda–Lucy pair: Sisters' Rivalry (synergy), Marks-Sisters (Duo node), Sisters' Bond (run upgrade). Keep three names?

A: 

### Character sheet: Lucy Q3

In the John–Lucy Duo, Lucy's QTE uses Linda's input binding (`LindaQTE`). Data slip?

A: 

## Character sheet: Mark (`characters/mark.md`)

### Character sheet: Mark Q1

Atman's Focus: the tooltip says kills give Focus; the code gives it on every basic attack that lands. Which is intended?

A: 

### Character sheet: Mark Q2

Catch & Return's node says it refunds his attack; the data only bounces the arrow back ([Family systems](../family-systems.md#open-questions) Q9).

A: 

### Character sheet: Mark Q3

The Wrist Wrap of Power uses a weapon slot Mark doesn't have, so it can't be equipped on `main`. The Demo Spec lists it as his Workshop weapon.

A: 

### Character sheet: Mark Q4

Data copied from Lucy: his role and Continuous Attack QTEs use Lucy's input binding (`LucyQTE`), his hit sound is Lucy's, and his revenge line ("Noooo!") is hers. Fix?

A: 

### Character sheet: Mark Q5

The Duo node is named "Chained Assault"; the skill-tree notes say "Sidewinder Blitz" and the glossary says "Fist Blitz" ([Family systems](../family-systems.md#open-questions) Q2).

A: 

## Character sheet: Toba (`characters/toba.md`)

### Character sheet: Toba Q1

Toba has no Family Role, no Pass-by, no Revenge, no ATB gauge, and carries one item where the others carry two. Deliberate for the newcomer, or missing?

A: 

### Character sheet: Toba Q2

The Stone Axe and Tribal Necklace descriptions still say "Dom". Rename to Toba?

A: 

### Character sheet: Toba Q3

Where should Bond-scaled healing live (TO-2)?

A: 

### Character sheet: Toba Q4

Nature's Rhythm only raises his AP cap. Should it give him a third action every turn?

A: 
