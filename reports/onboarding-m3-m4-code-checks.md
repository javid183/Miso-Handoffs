# M3 / M4 code checks (2026-11-25)

Read-only Explore pass for the to-checks of `plans/2026-11-22-onboarding-d3-paper-levels.md` §5, after D-688 to D-690. Code reading only; nothing run in Unity. Coordinates: y=0 is the bottom row (the grid parser and the doc agree).

## T-8 · Tally credit for a mushroom blast: nobody (with one race)
- Mushroom = `HazardEntity` (`MushroomExplosion.prefab`, faction Enemy, `mainEffectDelay 1.5`), set off by `Specs_Health.onValueDecreased` → `PerformMainEffect`; the blast has the hazard as owner, no `RuntimeAbility`.
- `SistersTallyListener.cs:321`: hazard / ownerless damage counts for no one. `RecordDamage` (:199) needs an attacker; `RecordDeath` counts only inside a Duo bracket.
- Race: a Claw also hit by the arrow is credited if the blast lands before her ability reports. Blast-only kills: nobody.
- Smallest fix (not core): `SistersTallyListener` watches `onAbilityEffectPerformedOn` for a sister's ability touching a `HazardEntity`, opens a window (like the Bloom window) crediting enemies that die in the blast to her.

## T-9 · The pick on 5,7: partly
- `UnitTileOccupiedLOCondition` (`LevelObjectiveConditions.cs:183`) needs a serialized `GUnit`; the pick is spawned at runtime (`FillRosterSlots`, `CombatLevelRunHandler.cs:~317`), so it can't be referenced.
- Data-only: `TilesOccupiedLOCondition` faction Bergsons on 5,7 (any Bergson; M1's `FamilyOnTiles`, `MissionWiring.Ridge.cs:~244`).
- Exact pick: new feature-side condition (a Bergson whose Nickname isn't Linda/Lucy), a few lines like `FactionTurnLOCondition`; not core.
- The AI planner turns active `TilesOccupied` objectives into intents (`AIStrategyPlanner.cs:251`); how much that steers enemies to 5,7 is unread.

## T-10 · The stone
- **Paper is wrong:** the Deer ("Stag") is not Unmovable (only `Unable to Swap`).
- Template: `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab` (Neutral, `Unmovable`, `Unable to Swap`, titled "Fallen Rock": retitle).
- M1 only reveals its rock (`RevealUnitsSequence`, `MissionWiring.Ridge.Sequences.cs:106`).
- Sequences: `HideUnitsSequence` (off the board, no death), `RevealUnitsSequence` (onto a taken cell → nearest free cell), `UnitAnimationSequence` (core; animator state, HoldLastFrame; the rock's controller has only Idle), `MoveUnitSequence` (needs a walk ability + transporter; the rock has none).
- Cheapest data route for notches: one rock variant per notch, each its own group, Hide + Reveal per notch.
- Relations (`LevelBase.prefab`): Enemy–Neutral hostile, Bergsons–Neutral ally. Set Enemy–Neutral to Ally in M3 (as D-672) so Claws ignore the stone.
- Masher slams hit every faction; S1 kills it before the push.

## T-11 · Roster Toba + placed Toba: one unit
- `FillRosterSlots` (`CombatLevelRunHandler.cs:~263, ~317`) skips roster units whose Nickname is already in the level (`existingUnitNames`).
- `Level3-C1` and `LevelDivineRelicRoom 1` both place Toba.
- `GB_m4-cleanse`: place Toba, Linda, Lucy + one `Unit_Placeholder` for the pick. Placeholder fill order is unspecified, so an unplaced fixed unit could take the pick's slot.
- `M4SquadPickTests` asserts `forcedExcludedUnits == [Unit_Toba]` and 2 fixed slots: must be rewritten. `M4SquadSlots.FpFillerNicknames` = Linda, Lucy, Toba.

## T-12 · Mithra's relic: **paper is wrong**
- A `DR_PickUp_HeavenlySword` is already in `LevelDivineRelicRoom 1.prefab` (PrefabInstance ~line 1091, under a cell); also in `LevelDivineRelicRoom.prefab` and `LevelMarkIntro-C1.prefab`.
- `DivineRelicPickUp.cs`: `OnTriggerEnter2D` tag "Player" → `Faction.Tracker.AddUsableItem(item, 3)` → destroys itself. Walking through counts.
- Place one: instantiate `Features/Player/Shared/DivineRelics/Heavenly Sword/DR_PickUp_HeavenlySword.prefab` under the target GridCell at local zero (M3's 8,6 the same).
- Heal: Healing Room uses `TriggerOverlapTerminal` (2D trigger) → `SafeRoomFunction.OnFunctionTriggered`; `healHpModifer` `baseFactor 0.5` on `StatUB_HP`. `LevelDivineRelicRoom 1` has no `SafeRoomFunction`: add one + a trigger (data).

## T-14 · Turns-passed stage: partly (changes the push design)
- Only `TurnReachedLOCondition` (`LevelObjectiveConditions.cs:209`), relative: records `TurnNumber` at first `Evaluate`, completes when `current - start >= turn`. No "on the tile for N turns".
- `_turnNumber++` when the turn index wraps to faction 0 (`CombatLevelRunHandler.cs:505-507`); `UpdateObjectives()` right after `StartTurn` (:535) and after every ability and death. Family first (M3): ticks at the family turn start; the stage completes then.
- A new stage first evaluates after its predecessor's `onCompleteSequence` + epsilon (`WaitThenEvaluateNewStage`, :~680).
- **Gotcha:** the count runs while the pusher is off the tile; back on after two turns away → completes the instant he arrives, maybe mid-turn. "The stone waits" is only roughly true.
- `FactionTurnLOCondition` is not needed with family first; outside the planner's list (D-687), harmless.

## T-15 · Shots across a gap: yes by code (play-check still)
- `GetRangeStraightCells` (`GridCell.cs:952`) stops at a missing cell, but `allowRangedReach` (`GridCell.cs:878-896`) adds every existing cell in range on the row/column. Linda primary: `straightDirectionCellsOnly 1, allowRangedReach 1`; Lucy: `0, 1`.
- `Projectile.cs` flies world-space, hits by trigger + sweep; Linda's arrows `travelEntireRadius 1` pick the farthest existing cell, skipping gaps (:154-165).
- Unconfirmed: walkability filter on the pick step; Linda's primary `radiusV` reads 5, not the paper's 4.

## Barriers (deferred, D-689): nothing built
- Relatives: `Toba_Wall.prefab` (Bergsons hazard, HP, `disallowWalk`, `isTargetable 0`, `lifeTurns 3`), `CP_Spawner` (Enemy hazard, HP 10), `Unit_Rock`.
- Claw attack `targetType 2` (CellOccupant), `targetFactionRelation 2` (Enemy): can't target a hazard. A neutral GUnit barrier would be a Claw target whenever utility allows, not only when blocked.
- "Attack when blocked" belongs in `AIUnitBrain` candidate collection (~:420-470) or utility variables: core AI.

## Masher: yes
- `GridBlockParser.ResolveBigUnits` (:165) groups four `O` cells, anchor bottom-left, must be exactly 2x2. `m3-defence` → anchor 3,6.
- `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab` exists; palette `O` maps to it.
- EN-10 close-up: `EnemyIntroductionController` introduces each unseen hostile Nickname at the next player phase (saved in `EnemyIntroductionTracker`); name only (`EnemyIntroductionUI.nameText`). A returning save won't replay it (`ResetSeen` is a dev tool).

## Cleanse lock: data
- `LevelAbilityLock` (`Features/Levels/AbilityLock`), per level, by Nickname; no component = no locks. Patterns: `HearthMemoryWiring.Rules.LockCleanse`, `MissionWiring.Ridge` (`CleansePath`).
- M3 and M4-2/M4-3 need a lock entry (unit prefabs, so the pick is covered); `GB_m4-cleanse` none (or `UnlockAbilitiesSequence` + `GuidedAbilityHint` WhenUnlocked).
