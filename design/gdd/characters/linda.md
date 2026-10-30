# Linda

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); [Linda's Quiver](#lindas-quiver) and Encore from `main` @ `8c2e8617c`, 2026-10-29 (quiver scripts, arrow prefabs, `Unit_Linda.prefab`, `Linda_Ability_Recall.asset` read); THJ's answers D-327 to D-330 added 2026-10-29 · Mirror: Claude Doc "Miso — Game Design", tab Characters › Linda · Up: [Overview](../overview.md)

Linda is the archer: ranged damage that pierces lines of enemies, and her Family Role, Family Watch ("Watch" for short), that shoots anything moving into her lanes. Every shot spends an arrow from her quiver, and the family brings the arrows back. She was the family's strongest damage dealer (46–72% of damage in the October playtests, before the quiver), which is why her role was the first to get a limit: the quiver is that limit (D-244).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 20 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 2 | Built |
| Joins | From the start | Built |
| Quiver | 3 arrows (stat "Quiver Size", `Stat_LQuiverSize`); each shot spends one ([Linda's Quiver](#lindas-quiver)) | Built |
| Family Role | Family Watch, short form Watch (D-328): shoots enemies that end a move in her row or column ([Family systems](../family-systems.md#family-roles)); limited by her arrows, no per-round cap (LI-11) | Built, differs |
| Duos | John–Linda, Linda–Lucy, Linda–Toba, Mark–Linda | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Lucy), Catch & Return (with Mark) | Built |

Source: `Features/Player/Linda/Prefabs/Unit_Linda.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Bow attack | Basic attack | An arrow along her row or column, 4 cells (5 or 6 with Longshot), that pierces every enemy in line: 6 × damage to the first, then ×0.6 of the previous hit for each next enemy (×0.8 or ×1.0 with Power-Piercing Arrows) | 1 | 0 | Built |
| Explosive Crescendo | Attack | An arrow to any cell within 5: 8 × damage to each enemy on that cell and the 4 next to it (×1.2 with Louder Crescendo) | 1 | 2 | Built |
| Harmonic Slam | Signature (1 SP to unlock) | Enemies next to her are Crippled for 1 turn (and Weak for 2 with Diminishing Blow); then she steps to a free cell within 1 (2 with Echoing Retreat). No damage, by design. +1 FTP | 1 | 1 | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |
| Encore (code name Recall) | Quiver | Every grounded arrow of hers flies straight back to the quiver, through walls and enemies; no damage. Usable while at least one arrow is grounded and the quiver has room (LI-8). Hidden when the quiver is switched off (LI-14) | 2 | 2 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself. Bow attack, Explosive Crescendo and her arrow Duos each spend an arrow (LI-4); at 0 arrows they can't be used.

Duo triggers on her bar: Linda–Lucy, John–Linda, Mark–Linda, Linda–Toba ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Linda.prefab`; presets in `Resources/UnitSpecific/Player/Linda/` (`Attack/Primary Attack/Linda_Ability_PrimaryAttack.asset` with `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab`, `Attack/Explosive Arrow/Linda_Ability_ExplosiveArrow.asset`, `Abilities/HarmonicSlam/Linda_Ability_HarmonicSlam.asset`, `Abilities/Recall/Linda_Ability_Recall.asset`: cost 2, cooldown 2, D-262, D-302); `design/combat-balance.md` (Harmonic Slam is damage-free by design). Every level that overrides Linda's kit carries Encore too (D-316, D-325; `EncoreKitTool`).

## Linda's Quiver

On `main` since 2026-10-29 (D-326; built on `thj/linda-quiver` from D-241); `main` now matches the merge. `thj/home-test` doesn't have it yet. The one rule: **every shot spends an arrow; the family brings the arrows back.** Values are playtest starting points. Reasoning and history: [`plans/2026-10-26-linda-quiver-design.md`](../../../plans/2026-10-26-linda-quiver-design.md) and the simplification (D-292 to D-295: no Far Watch, no distance rules, one layer of feedback).

- **LI-3. Quiver.** Linda holds as many arrows as her Quiver Size stat (`Stat_LQuiverSize`; title D-329), base 3 (D-316, D-319). Skill nodes, gear and run upgrades can change it with ordinary stat modifiers; none does yet. It is read at level start (without the stat, the quiver's own size of 3 applies), and she starts every level full. *Built*
- **LI-4. What spends an arrow.** One per shot: bow attack, Watch, Explosive Crescendo, and the arrow Duos she fires (Marks-Sisters, Healing Marks). Tempest Bloom's split copies and Mark's return copy spend nothing; Harmonic Slam, Cleanse, Encore and moving need no arrow. Exception: her Family Super Time Crescendo fires even at 0 arrows (it then lands nothing; D-251). *Built*
- **LI-5. Empty quiver.** At 0 arrows her arrow abilities can't be used and Watch doesn't trigger; her role zone hides. Pickup (LI-7), the kill hand-back (LI-13), Mark's catch (LI-9) and Encore (LI-8) refill it. *Built*
- **LI-6. Where an arrow lands.** A bow or Watch arrow lands on the tile of the last enemy it hit, or at the end of its flight if it hit none; Explosive Crescendo on its centre cell; a Duo arrow at the end of its line; a Tempest Bloom arrow where it split. An arrow is never lost: on a missing or blocked cell (Lucy's Cyclone included) it lands on the last valid cell of its path toward Linda, and with no valid cell or no grid it goes back to the quiver (D-249, D-252, D-258). A tile holds any number of arrows and may share with a hazard. An arrow that lands under a Bergson is picked up at once. *Built*
- **LI-7. Pickup.** A living unit of Linda's own faction (Linda included) that enters a tile with her arrows takes them all back to her quiver, up to its room; the rest stay. Every cell-by-cell move counts, walk, push, Command, dash and the John-Linda Dance, on either side's turn; passing through an ally's cell doesn't. An arrow under a living enemy is locked until that enemy moves or dies. Enemies, allies of another faction (the allied Toba) and anyone while Linda is dead take nothing (D-254). Each pickup plays a non-blocking hand-back beat of about 0.6 s: the picker's bark, a tossed arrow, Linda's reply (D-247; lines are placeholders). *Built*
- **LI-8. Encore.** 2 AP, cooldown 2 (D-243, D-302). Every grounded arrow of hers, locked ones and those behind walls included, flies straight back, ignoring obstacles; no damage. Usable only while she lives, at least one arrow is grounded and the quiver has room (D-256). Description (final, D-327): "By her call, every grounded arrow flies home to her quiver. (2 AP)". *Built* (`Linda_Ability_Recall.asset`, `main` @ `e5506c1e8`). Known limit: in the PerUnit AP mode it can be cast with 1 AP left, as any ability can (D-304, backlog `ap-overspend-perunit`).
- **LI-9. Catch & Return.** When Mark catches her arrow ([Mark](mark.md) MA-3), the arrow goes straight back into her quiver; neither the arrow nor its return copy lands. *Built*
- **LI-10. Level end.** Every arrow comes back: she starts each level with a full quiver. *Built*
- **LI-11. No round limit on Watch.** The quiver is her limit (D-244: supersedes D-041 and Linda's part of D-042, [Family systems](../family-systems.md) FR-4, FR-5). Watch still costs 1 FTP on top of the arrow (D-246) and is just her shot, with no damage rules of its own (D-294). With the quiver switched off (LI-14) there is no cap either (D-330). To reconsider after the playtest. *Built*
- **LI-13. Melee kill hand-back.** When John's Sword Attack or Toba's Axe Dance kills an enemy standing on her arrows, they go back to her quiver at once, with the hand-back toss and the "+N" cue, no step needed. Only a killer of Linda's own faction counts, so the allied Toba doesn't (D-307, D-310). Any other kill only unlocks the stack. The attacks are a list on her quiver (data). *Built*
- **LI-14. Quiver switch.** `lindaQuiverEnabled` in Global Settings (default on in code; read when each level starts) turns the quiver on or off. Off, Linda plays as before the quiver: free shots, no grounded arrows, no pickups or hand-back, no quiver UI, and Encore hidden from her bar (D-314, D-320); Watch then has no limit at all, by design (D-330). The switch is a test and merge tool, not a game mode. Mark's catch then returns a damaging copy and no arrow (MA-3). Lucy's real-damage rule and the projectile fixes (CR-55) stay on either way. *Built*

LI-12 (the design plan's Fireside arrow) is not built ([Open questions](#open-questions) Q4).

What the player sees (D-293, D-297 to D-301, D-306): a small quiver at the top left of her portrait with one arrow per arrow (it lifts while an arrow ability is hovered or selected, punches at 0, glows on a gain), small pips under her, arrows on their tiles (one icon, "xN" from 2, dark-tinted while locked), a ghost arrow on the landing tile while aiming (from the end cell of a move-then-shoot too), a "+1" cue on every return and thin curved lines from the grounded arrows to her while Encore is hovered or selected; with the quiver empty, one crossed arrow under her feet. The combat log only appends the quiver count to existing lines.

Source: `Features/Player/Linda/Scripts/Quiver/` (`LindaQuiver*.cs`, `QuiverArrow.cs` with `ArrowLandingRules`, `GroundedArrowField*.cs` with `ArrowPickupRules`, `RecallRules`, `KillHandBackRules`, `QuiverSizeRules`, `LindaQuiverSwitch`, `QuiverBarRules`); `LindaQuiver` on `Unit_Linda.prefab` (`size` 3, `sizeStat` `Stat_LQuiverSize`, `handBackOnKillAbilities` John's and Toba's basic attacks, hand-back 0.6 s); `QuiverArrow` on `LindaAttackArrow`, `LindaExplosiveArrow`, `LindaAttackFireArrow`, `LindaAttackHealArrow`, `LindaAttackArrowReturn`; the `HasArrow` / `HasGroundedArrows` checks on the bow, Watch, Crescendo, Duo and Encore effect assets; `Core/Managers/GlobalSettingsSO.cs` (`lindaQuiverEnabled`); `Resources/Attributes/StatAttributes.asset` (`Stat_LQuiverSize`).

## Passives

- **LI-1. Sisters' Rivalry (her half).** When Lucy kills with a basic attack, Linda gets +1 AP and a ready basic attack. *Built* ([Family systems](../family-systems.md#synergies))
- **LI-2. Move as One.** Once bought in her tree, every Bergson gets +1 movement on their first move of each level (the bonus is spent by that move, or ends after 2 turns). *Built*

Source: `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`, `LindaFirstMove.cs` and their components on `Unit_Linda.prefab`.

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Harmonic Slam | 0 | unlock | Unlocks Harmonic Slam | — |
| Longshot | 0 | 2 | +1 arrow range per level (0 / 1 / 2) | — |
| Diminishing Blow | 2 | unlock | Harmonic Slam applies Weak | Harmonic Slam |
| Move as One | 2 | unlock | Family: +1 movement on each Bergson's first move (LI-2) | — |
| Louder Crescendo | 3 | 1 | Explosive Crescendo hits harder | — |
| Power-Piercing Arrows | 5 | 2 | Arrows lose less damage per enemy: decay 0.6 → 0.8 → 1.0 | Longshot |

Linda has no family nodes on her own tree; her Duos and Synergies are bought on John's, Lucy's, Mark's and Toba's trees.

Source: `skillTree` on `Unit_Linda.prefab` (Stat_RANGE 0 / 1 / 2, Stat_DMGD 0.6 / 0.8 / 1.0).

## Revenge

When a family member dies, Linda gets for 2 turns: damage ×1.5, +20% crit chance, +1 AP and +1 to her AP cap. *Built*

## Gear

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Crescent Bow | Right hand (weapon) | Damage | +1 (10 Gold, 1 Timber) | +3 (20 Gold, 3 Timber) | +5 (40 Gold, 5 Timber) |
| Stylish Hairband | Head | Evasion | 0.05 (10 Gold, 1 Fabric) | 0.1 (20 Gold, 3 Fabric) | 0.15 (40 Gold, 5 Fabric) |

One free slot takes the shared Shin Armor. Source: `Resources/Unit Equipments/Linda/*.asset` (the hairband's file is named `Equipment_Styllish Hairband.asset`).

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Power-Piercing Arrows | Arrow damage decay ×1.5 (stacks with the skill node; Q1) |
| Louder Crescendo | Explosive Crescendo damage +1 level |
| Echoing Retreat | Harmonic Slam retreat distance +1 level |
| Diminishing Blow | Harmonic Slam applies Weak for 2 turns (same as the skill node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level (needs both in the squad) |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Linda's Home talents (her violin speeds a tended plot, the Mossy Tablet's timber stand, the Footwork lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities. She is half of the showcase pair with Toba.

## Open questions

1. **Q1.** Power-Piercing Arrows exists as both a skill node and a run upgrade; the run upgrade can push the decay past 1.0 (more damage on later targets). Cap it, or rename one?
2. **Q2.** Her role has no limit yet and costs 1 FTP ([Family systems](../family-systems.md) FR-3 to FR-5). **Answered:** the quiver is her limit, no per-round cap (D-244, LI-11); Watch keeps its 1 FTP until the FTP rework (D-246).
3. **Q3.** With the quiver switched off (LI-14), Watch has no limit at all again. Does the planned per-round cap (FR-4, FR-5) come back for that case, or is the switch only a test tool? **Answered:** no cap; the switch is a test and merge tool (D-330, LI-11, LI-14).
4. **Q4.** Quiver growth: total arrows were to be capped at 6 (3 base now, D-316; Deep Quiver node and a Workshop quiver, D-245), and the plan's Fireside "+1 arrow at sortie start" (LI-12) would replace D-040's third shot (proposed, not decided: D-241 left the Fireside out). None is built, and `Stat_LQuiverSize` has no modifier yet. Which comes first, and does the cap of 6 still hold at base 3?
5. **Q5.** Should a Dark Worm about to split trigger Watch? Today it can, and the target can vanish during the prompt; the role is then skipped cleanly (D-313, FR-2).
6. **Q6.** Encore's description text is a placeholder and still says "1 AP" (it costs 2). Final wording: narrative. **Answered:** "By her call, every grounded arrow flies home to her quiver. (2 AP)", THJ's own text (D-327, LI-8); in the data since `e5506c1e8`.

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [`combat-balance.md`](../../combat-balance.md) · [Glossary](../../../glossary.md)

Quiver decisions: D-241 to D-262, D-270 to D-330 (Far Watch, the distance test and Arrow Chase are not built: D-292). Plans: [design](../../../plans/2026-10-26-linda-quiver-design.md), [tech](../../../plans/2026-10-26-linda-quiver-tech.md), [readability strip](../../../plans/2026-10-28-quiver-readability-strip.md), [feedback pass](../../../plans/2026-10-28-quiver-feedback-pass.md), [polish 2](../../../plans/2026-10-29-quiver-polish-2.md), [switch, size, Encore kits](../../../plans/2026-10-29-quiver-switch-size-encore-clamp.md), [swap ends a move](../../../plans/2026-10-29-swap-ends-move.md).
