# Combat Balance M1–M7: proposal companion

Proposal written 2026-10-06 on `main` (`f531b4d4b`). Applied 2026-10-07 on `thj/enemy_variations`; THJ committed it as `f55fa95ef` (enemy tiers), `89bfb13c6` (save reset), `ff48490fd` (health rounding + preview), with `4f27914d0` on top. **Review follow-ups (2026-10-07, below) are uncommitted in the working tree.** THJ playtested M1, M2, M5 and both M3s on 2026-10-08 (see "Playtest 2026-10-08").
Design doc: "Miso Combat Balance M1–M7", https://claude.ai/code/artifact/3ebcf248-26be-45a3-8f5b-b4df479ba411
Master: this file (`claude-handoff/design/combat-balance.md`). The claude.ai project "Miso" holds a copy (`design/combat-balance.md`), refreshed from here. `claude-handoff/` is excluded from the shared repo; never stage this file there.
v2 (2026-10-06): after THJ review. v1 cut enemy damage; that was wrong because it ignored Family Roles, duos and synergies. Playtests say the game is already too easy (back when Claw damage was halved).
v2.1: THJ confirmed Harmonic Slam is deliberately damage-free (cripple + reposition; Explosive Crescendo is Linda's AoE). The Masher's area attack hits enemies too.

## How the numbers work (read from code/data)
- Damage = effect `baseFactor` × Stat_DMG, folded Faction → Equipment (flat add) → Unit → Ability (`StatResolver.Resolve`). Health changes are rounded per hit (RoundToInt, halves to even); integer attributes (health) also start and clamp on whole numbers.
- HP = `attributeSet` entry 1 (Specs_Health) `defaultSbValue.baseFactor` × Stat_HP. (The legacy `defaultValue` / `bounds.max` overrides on enemy prefabs are unused leftovers and already disagree with the real values.)
- AP: 2 per unit. Enemy attacks are `Closure` (end turn). Player attacks cost 1 AP.
- Family Roles (`Features/Player/<Unit>/Scripts/*FactionRoleHandler.cs`): each costs 1 ATB step (`requiredFTP` 1), `oncePerPhase: 0` on all four (no per-turn limit). ATB gauge: 3 steps (`atbSteps` 3 × Stat_ATBS), fill 0.2 × Stat_ATBFR (unit 2 × faction 0.5) steps per real second during enemy turns / ally actions; unspent AP converts 1:1 into steps at end of turn (PerUnit mode). `pointConsumptionMode: 1` (ATB) on main.
  - Linda: shoots (6× bow effect) any enemy that moves into her straight lines within range.
  - Lucy: after an ally attack, hits a target in range with the sidewinder effect (3× per orb).
  - John: takes the ally's hit himself with DR modifier 0.2 (`JFR_DR`); ally takes nothing.
  - Mark: counter-attacks (Fist Blitz 8×) the enemy that hit an ally, in range. Plus continuous attack / Atman Focus passives.
- Sister's Rivalry = `UnitKillAbilityPointProvider`: a basic-attack kill by one sister gives the other +1 AP and resets her basic attack cooldown; only limit is a 2 s real-time timer.
- Faction relations (`LevelBase.prefab` LevelFactionRelations; `FactionsRelationType` Ally = 1, Enemy = 2): Bergsons–Enemy 2, Bergsons–Neutral 1, Bergsons–Stranger 1 by default; the M1–M3 tiered levels keep those. So in tiered levels only the Enemy faction is hostile; Neutral and Stranger are only cleared.

## Model (rough, in the doc)
Family damage per round ≈ own attacks (1.5 per hero) + 2 reactions per hero (assumption) + damage duo (~10) + Papa's Shelter (~3). John–Linda–Lucy ≈ 71/round vs ≈32 from basic attacks alone. Before the change, M4–M7 regular fights cleared in 1.1–1.8 rounds; target 1.6–2.6.

## What was applied
- Heroes: unchanged (John 32, Linda 20, Lucy 15, Mark 15, Toba 24). Harmonic Slam stays damage-free.
- Enemy prefab HP (`defaultSbValue.baseFactor` + `sBBounds.maxV.baseFactor`): Dark Claw 10→16, Black Claw 25→40, Archer 20→24, Worm 20→28, Shaman 35→50, Masher 50→80, Goblin Queen 200→320. Mountain Deev untouched (not in M1–M7). These also apply to M8+ levels.
- Archer damage 5→6 (`ArcherGoblin_Ability_Attack_Effect_AttrMod`).
- Toba duel HP override 40→60 (`Level2/LevelDomFight.prefab`).
- Tiers (enemyTier on the level, factors on `EnemyFaction`):
  - `Resources/Factions/EnemyFaction.asset`: `Stat_HP` levels 1 / 1 / 0.6 / 1.2, `Stat_DMG` 1 / 0.75 / 0.5 / 1 (index = tier: 0 Standard, 1 Early, 2 Tutorial, 3 Late).
  - `Core/Levels/Runtime/CombatLevel.cs`: `enum EnemyTier`, serialized `enemyTier` (General box), property `Tier`.
  - `Core/Managers/CombatLevelRunHandler.cs`: `ApplyEnemyTier()` called in `InitializeSessionContent` right before `PrepareUnits()`. For every non-player faction in the FactionRegistry it calls `public static ApplyEnemyTierTo(StatAttributeSet, int tier, bool hostile, string factionName)`: clear run-level bonuses; if tier > 0 and hostile (relation Enemy, via `GetFactionsRelation` because `GetFactionEnemies` filters on controllers that don't exist yet), add `tier` levels to Stat_HP and Stat_DMG. Warns when a stat entry is missing or when the tier is past the authored rows (StatAttributeSet clamps to the last row).
  - Level prefabs: Tutorial (2) on Level1-C1_TArtEx, Level1-C1-2, Level1-C2; Early (1) on LevelLucyJohn-C1..C3, LevelE1-C1..C2, LevelLindaJohn-C1..C2, LevelMarkIntro-C1..C3. M4/M6/M7 stay Standard (no edit).
  - Removed from those levels: all per-instance Stat_DMG overrides (0.25 / 0.5); HP overrides equal to the old prefab default (Claws at 10, the E1-C1 Archer at 20) and the M1 Archer HP overrides (10/15). Kept: Mark Intro C2 Claws at 8 HP, player-unit overrides.
- Not applied: Masher `oncePerPhase: 1` (THJ's call), Late tier on M6/M7 (only if playtests show level-ups make them easy).

## Fixes after playtests (committed in ff48490fd / 89bfb13c6)
1. **Enemy alive at "0 HP".** Health with a fractional max (24 × 0.6 = 14.4) could end at 0.4: shown 0, alive. `RuntimeAAttribute` snaps start value and min/max for entries with `changeInInteger` (only Specs_Health has it: `UnitBase.prefab` + three level/test overrides of the same entry; no code sets it). `RuntimeAAttributeBase`: `Reset` virtual; virtual `MinValue` / `MaxValue`; `Percentage` uses them. `ItemEffectPreview` (HP) and `MissionCharacterPanelUI` read `MaxValue`.
2. **Faction HP ×1.25 after a save reset.** Faction stat levels are `[NonSerialized]` on the faction assets and survived save deletion / Play sessions. `StatAttributeSet.ResetUpgradeLevels()`; `GameHandler.Initialize` resets before `Prepare`; `GameHandler.ResetProgress` resets after `ClearSaveData`; `SaveLoadManager.ClearSaveData` nulls in-memory `LastSave`.
3. **Hover preview 1 HP short.** `AbilityDamagePreview` compound branch dropped a compound's own HP mods when it had a nested compound, and counted locked compounds. Now skips locked compounds (`AEffectCompound.IsUnlockedFor`) and applies own mods alongside nested ones. Affected: Lucy ember M/S orbs (+ locked Burn), Lucy Cyclone (previewed 0), Mark Vault (previewed 0).

## Review follow-ups (2026-10-07, uncommitted)
- **Review 1 (tier past authored rows is silent):** confirmed — `GetEffectiveLevel` clamps `UpgradeLevel + bonus` to `MaxUpgradeLevel`. Fixed with the warning in `ApplyEnemyTierTo` (and a warning for a missing Stat_HP/Stat_DMG entry). No spam in current content: only the Enemy faction is hostile in tiered levels and it has 4 rows.
- **Review 2a (Reset clamps only in the forceDefault case):** not a bug — the override always clamps (`forceDefault` only decides whether to reset to the default first); `SetValue` clamps every change to `MinValue`/`MaxValue`. No change.
- **Review 2b (raw `Bounds` readers):** grep done. Moved display-only health readers to `MaxValue`: `EntityInfoPanelUI` (5 uses: bar ratio + max), `UnitPanelUI` (3), `UnitAttributeIndicator` (2; it showed `(int)Bounds.max`, which would read "37 / 36" with a 36.8 max). Left as is (equal or harmless): `CombatLevelRunHandler` lethal check and `DarkWormPassiveAbility` death check (min is 0), `GUnit` heal-to-full and Dark Worm `SetValue(Bounds.max)` (SetValue clamps to the snapped max), `GUnit` HP-gain factor (< 0.5 HP), AI `UtilityScoreEvaluator` Upper/Lower Bound (AI input; < 0.5 HP; left to avoid touching AI), all AP readers (`APConsumer`, `ActionPoints`, `ItemEffectPreview` AP — flag off, identical).
- **Review 3 (neutral factions cleared):** harmless. Clearing only drops run-level bonuses, and nothing else puts run bonuses on non-player factions (`RunUpgradeTracker` targets units and the player faction). Neutral/Stranger are allies of the family in the tiered levels, so they are only cleared.
- **Review 4 (tests):** `Core/Systems/StatsResourcesSystem/Editor/StatAttributeSetLevelTests.cs` (6 tests: ResetUpgradeLevels; tier row read; clearing between levels; non-hostile only cleared; tier past rows warns; missing entry warns). It required `CombatLevelRunHandler.ApplyEnemyTierTo`, which did not exist (would not compile); now added with matching warning text. The test file, its `.meta` and the new `StatsResourcesSystem/Editor.meta` folder meta are untracked: stage all three.

## Playtest 2026-10-08 (THJ, combat logs in `%USERPROFILE%\AppData\LocalLow\Dead Mage\miso\CombatLogs`)
THJ (long-time player): felt the difference, still easy, fine as a tutorial. No deaths, no mission completed twice; repeated short logs are experiments.

| Mission | Levels / rounds | Dealt / taken | Closest call | Time |
|---|---|---|---|---|
| M1 John's Map | 3 / 7 | 113 / 15 | John 26/32 | 3m |
| M2 Ryker is Lost | 3 / 10 | 221 / 48 (+20 potions) | Lucy 3/15 in C3 | 7m |
| M5 The Healer | 2 / 5 | 200 / 32 | John 16/32 after C1 | 12m |
| M3 No More Waiting | 3 / 11 | 172 / 16 | Mark 11/17 | 9m |
| M3 A Wolf's Blood | 2 / 7 | 240 / 51 (+20 potions) | John 3/37 in C2 | 6m |

Takeaways:
- Rounds per level 2–5 (avg ~3). Gold earned 61, matching the three purchases seen (Family HP L1, Bow Lv1, Ring Lv1).
- Real pressure comes from attrition (HP persists between levels): Ryker C3 and Wolf C2 both needed potions. Two-hero levels with 6–8 enemies are the right kind of hard.
- Linda deals 46–72% of damage wherever she is: pierce (one shot hits 2–4, e.g. 7/4/3) plus her family role firing 3× in one enemy phase.
- Sisters' Rivalry chains: M5 C2 R1, Linda attacked 5 times, 4 kills in one turn.
- Lucy Fire Embers at Sidewinders 2 + Papa's Shelter = 4 orbs, 13 single-target damage for 1 AP (more than John's 10). Sidewinders is likely the strongest SP pick.
- Mark–Lucy duo (Chained Assault): 0 AP, 11–16 per target × 3 (QTE spread).
- John's family role makes ally hits cost him 1 (0 with Shield Up); most of his damage taken came from Shield Dashing into packs.
- Mark Intro C2: the 8-HP Claw override equals Fist Blitz 8, so every hit kills and chains Continuous Attack (6 kills, 0 damage taken). Raise to 9–10 if the auto-chain is not intended.
- Early tier: 6 × 0.75 = 4.5 rounds to 4 (effectively ×0.67). The M4 jump to 6 is +50%.

Noteworthy issues (not fixed):
- Kills from friendly fire, Crippled movement or unattributed damage give no XP or gold (M1 C3, M2 C2 ×2, Mark Intro C3 Worms).
- Dark Worm split in Mark Intro C3: placed Worm has a 12-HP override, children spawn with max 28 and 6/4/1/0 current; one spawned at 0 HP and died at once; a Claw's move caused friendly-fire splits. Check `DarkWormPassiveAbility` against the new HP and rounding.
- Mark Intro C1 can be won without fighting (relic + altar objective; one run ended R2, 0 kills).
- Wolf's level labels say "(1/3)" but the mission has 2 levels.
- Combat log: unattributed `~` damage at phase start (Linda's role during enemy moves, Cyclone pass-by, Crippled); Worm spawn HP counted as damage dealt ("other 103"); Shield Up logged as an item; loadout line includes Papa's Shelter's temporary +1 ability level.

Watch in M4/M6: first M4 fight (damage 4→6, 8 enemies); first Masher counter loop; Linda's damage share in a full squad (if > 50%, her uncapped family role is the lever); whether level-ups make M6 easier than M4 (then add the Late tier).

## THJ design changes 2026-10-08 (John; not reviewed in code)
- **Wrath:** John gains a stack when he takes damage under Shield Up or through his Shield role; stacks add damage to his next attack (0.4 per stack, cap 3). HUD box with tooltip.
- **Blood Debt:** the last enemy to hurt a family member other than John carries the tag; John deals x1.3 to it until it is replaced or the debtor dies.
- **Shield role:** John now takes 0.4 of the redirected hit (was 0.2).
- **Sword:** 10 -> 8.
- Implications noted at the time: sword (8) + Lucy's follow-up orbs (6) = 14 no longer kills a 16-HP Claw; one Wrath stack or Blood Debt restores the kill. M1 Tutorial Claws (10 HP) are no longer one-shot by the sword. Shield-role hits now cost John about 2 (Claw/Archer 6) or 4 (Masher 10). Open questions: does a hit that rounds to 0 give a Wrath stack; does Shield Dash consume Wrath; is Wrath/Blood Debt shown in the hover preview; do Wrath and Blood Debt multiply or add.

## To do
- [ ] Recompile, run EditMode tests (expect the 6 new tests green; `AIRegressionTest.Baseline_MatchesCurrentAI` is the known red one).
- [ ] Re-test the hover preview on Lucy's embers, Cyclone and Mark's Vault; HP texts after Family HP L1 (e.g. John 37/37).
- [ ] Play M4, M6, M7 (Standard tier); read the combat logs for rounds per fight, reactions per round and Linda's damage share.
- [ ] Re-run `Tools/AI/Run Regression Test` (unit catalog may include HP).
- [ ] Decide on the Masher counter limit.
- [ ] Look at the Dark Worm split, the no-reward kills and the Mark Intro C2 8-HP chain.
- [ ] Rebalance M8–M14 against the new enemy HP.

## Gotchas found
- `Linda_Ability_FactionRole_Effect_AttrMod` (7×), `Lucy_Ability_FactionRole_Effect_AttrMod` (5×) and `Linda_Ability_HarmonicSlam_Effect_AttrMod` (7.5×) are unused assets.
- Masher counter fires on every non-lethal hit, reactions included, and its area hits both sides.
- Throwaway tools used: `tier_levels.py` (level override edit) and the YAML readers lived in the device session home, not in the repo.
