# Combat Log: Technical Design

Branch `thj/combat-logs` (from `main`), written 2026-10-07. **Status: code written, not compiled, not tested in Unity, not committed.** A tree-sitter syntax check of all new and edited files passed. Next steps: recompile (Ctrl+R), run the EditMode tests, then play one mission and read the log.

**Update 2026-10-08:** John's Wrath and Blood Debt (new passives, §4.4) raise synergy records, and Blood Debt is a status tag (§4.3). See §4.3, §4.4, §11 and §12. Not compiled or verified against a full log read either.

**Update 2026-10-09:** the Lucy + John shield relay (`JohnShieldRelay`, `LucyFireballProjectile`) raises a `Shield Flare` synergy record (§4.4). Checked in code: no log changes needed. Not verified in a real log.

**Update 2026-10-10:** dev cheats are logged (§4.5). Their effects sit under a `CHEAT` line and are left out of all totals, and levels or missions that used one are tagged `CHEATED`. Not compiled yet.

All paths are relative to `miso/Assets/_Project/` unless noted otherwise. `claude-handoff/` is excluded from the shared repo (it is its own private repo); never stage this file there.

## 1. Purpose

The combat log is a short, readable record of what happens in combat. It has two uses:

1. **Balance:** rounds per fight, damage per unit, damage taken, kills, rewards per mission, and the loadout each fight was played with. The `.jsonl` output feeds the Python tools in `claude-handoff/reward-tools/`.
2. **Player-facing combat log (phase 2):** the same entries, filtered to `Visibility.Player`, can drive an in-game log panel.

What it records:
- Mission, level, round and acting phase.
- Acting unit, its cell, the ability used, and the targets (units or cells).
- Per target: HP change, crit, evade, statuses gained or lost, death, movement, spawns and revives.
- Family roles, duos, synergies and passives.
- Rewards (kills, pickups, mission completion or failure), run upgrades, level-ups.
- The loadout at level start, and totals at level and mission end.

## 2. Design rules

- **Decoupled.** The log lives in its own folder and only *listens*. It subscribes to `GlobalEventBus` and to each unit's `GTagSet`. Gameplay code only *raises* events, through one-line static helpers. Gameplay does not listen to the new events, with one exception since 2026-10-08: `onFamilyRoleActivated` drives John's Wrath and Blood Debt, so it must keep firing from `FactionRoleHandlerBase.Activate` even without the log (the bus comment says so).
- **Never breaks combat.** Every handler is wrapped in `Guard` (try/catch plus `Debug.LogException`). File sinks are guarded the same way.
- **No statics.** `MissionTracker` (DontDestroyOnLoad) owns one `CombatLog`, so with domain reload off, nothing needs a `PlayModeStaticReset` hook.
- **Main thread only.** Bus events are raised on the main thread. Tag handlers return early when `AIWorker.IsWorkerThread` is true.
- **Locale-safe text.** All numbers go through `CultureInfo.InvariantCulture`; no `"P0"`.
- **Line endings and BOM.** Edited files kept their BOM and LF endings. New files are UTF-8 without BOM, LF.

## 3. Architecture

```
GlobalEventBus (per level scene)       GTagSet (per unit)
  existing events + 5 new ones            OnTagGained / OnTagRemoved (new)
            │                                    │
            └──────────────┬─────────────────────┘
                           ▼
              CombatLog (recorder, Unity glue)          owned by MissionTracker.CombatLog
              frames · rows · labels · stats              hooked by CombatLevelRunHandler.InitializeEvents
                           │
                           ▼
              CombatLogBook (plain storage + context)
              Entries · EntryAdded event · sinks
                 │                │                │
                 ▼                ▼                ▼
       CombatLogFileSink   CombatLogWindow     (phase 2) in-game panel
       .log + .jsonl       Tools > Combat Log
```

### Files (`Core/Systems/CombatLogging/`)

| File | Role |
|---|---|
| `Runtime/CombatLogEntry.cs` | `CombatLogEntry` (one line), `CombatLogKind`, `CombatLogVisibility`. Plain strings and ints only. |
| `Runtime/CombatLogBook.cs` | `CombatLogBook`: entries, context (mission, level, round, phase), sequence numbers, `EntryAdded`, sinks. `ICombatLogSink`. `CombatLogFrameStack<T>` (attribution logic, §5). |
| `Runtime/CombatLogFormat.cs` | Pure helpers: unit labels, cells, composing a line (`Compose`), JSON (`ToJson`), safe file names. |
| `Runtime/CombatLogFileSink.cs` | Appends each entry to `.log` and `.jsonl`. It opens and closes the file on every write, so nothing stays locked if Play stops mid-mission. |
| `Runtime/CombatLog.cs` | Recorder: mission lifecycle, bus subscription, level end, `Guard`. |
| `Runtime/CombatLog.Units.cs` | Labels, last known HP and cell, tag subscriptions, level start, spawns, target description, loadout. |
| `Runtime/CombatLog.Actions.cs` | Frames and rows: ability start and finish, family roles, crit, evade, death, flushing rows. |
| `Runtime/CombatLog.Events.cs` | Synergies, run upgrades, level-ups, rewards. |
| `Runtime/CombatLog.Summary.cs` | Level and mission totals. |
| `Editor/CombatLogWindow.cs` | `Tools > Combat Log` live window. |
| `Editor/CombatLogTests.cs` | Edit-mode tests (§10). |

Namespaces: `MISO.Core.Systems.CombatLogging`, `.EditorTools` (window) and `.EditorTests` (tests). No asmdef, as elsewhere under `_Project`.

## 4. Event sources

### 4.1 Existing bus events used (no code change)

| Event | Used for |
|---|---|
| `levelStarted` | Level header, labels for every live unit, start HP and cells, tag subscriptions, loadout. |
| `turnStarted(Faction)` / `turnEnded(Faction)` | Round and phase header; flush of anything not caused by an ability. |
| `abilityActivationStarted(RuntimeAbility)` | Opens a frame and writes the action line (actor, cell, ability, targets). |
| `abilityPerformed(RuntimeAbility)` | Closes the frame and writes its result rows. |
| `onCriticalDamageDoneOnUnit` / `onUnitEvaded` | `CRIT` / `EVADED` flags on the target's row. |
| `unitDied` | `KILLED` (or `DOWN` for a family roster unit) on the row. |
| `unitBorn` | Spawn row (new unit) or `revived` (known unit). Ignored before `levelStarted`. |
| `onUnitLevelUp(GUnit, int)` | `LEVEL UP` line. Raised from `FactionTracker.CollectResource`, during awards. |

### 4.2 New bus events (`Core/Managers/GlobalEventBus.cs`, header "Combat Log")

| Event | Helper | Raised from |
|---|---|---|
| `onSynergyTriggered(GUnit unit, string id, string detail, GameEntity[] targets)` | `RaiseSynergy(...)` | Synergy, combo and passive scripts (§4.4) |
| `onFamilyRoleActivated(FactionRoleHandlerBase)` | `RaiseFamilyRoleActivated(...)` | `FactionRoleHandlerBase.Activate`. **Also a gameplay hook:** `JohnPassiveAbility_Wrath` and `JohnPassiveAbility_BloodDebt` listen to it |
| `onRewardsGranted(GUnit receiver, GUnit source, string kind, CollectedResource[])` | `RaiseRewards(...)` | `CombatLevelRunHandler` award methods, `Pickup.TryCollect` |
| `onRunUpgradeGranted(RunUpgradeSO, GUnit)` | `RaiseRunUpgradeGranted(...)` | `RunUpgradeTracker.TryGrant` on success (covers altar picks, pickups, relics) |
| `onCheatUsed(string cheat, string detail, GUnit[] targets)` | `RaiseCheat(...)` | `Core/_Dev_/Runtime/CheatHandler.cs`, before each cheat is applied (§4.5) |
| `levelEnded(EndLevelResult)` | (direct `Invoke`) | `CombatLevelRunHandler.EndLevel`, after awards, before the UI end screen |

The helpers check `Instance != null`, so calls outside a combat level (menus, Home) do nothing. Reward kinds: `"Kill"`, `"Hit"`, `"Pickup"`, `"Mission complete"`, `"Mission failed"`.

### 4.3 Status changes

`GTagSet` gained `public event Action<GTag> OnTagRemoved`. It is raised next to `InvokeWatcherRemoved`, so it covers removals and expiries, and the tag is resolved only when someone is subscribed. `RemoveTemporaryTagsSilently` (on death) stays silent. The log subscribes to each tracked unit's tag set directly and logs only tags with `ShowInGame`. Today those are Crippled, Stunned, Vulnerable, Weak, Burnt, Taunted, Sheltered, Reckless, Immovable, Pact Leader and **Blood Debt** (added 2026-10-08, `showInGame`). Blood Debt is applied as a persistent tag, so the debtor's row shows `+Blood Debt` when John marks it and `-Blood Debt` when the mark moves to a newer attacker. It has no life-turn count, and a debtor that dies is cleared silently (see `RemoveTemporaryTagsSilently`).

### 4.4 Synergy, combo and passive records

Each is a single `GlobalEventBus.RaiseSynergy(...)` line. It only records that the effect triggered.

| Id in log | Script | When |
|---|---|---|
| Duo (detail = duo id) | `UnitsCooperationHandler.Execute` | Any duo starts; targets = partners |
| Mark-Linda Race | `UnitsCooperationHandler.Mark_Linda_ApplyStoredRewards` | Race rewards applied (winner, loser) |
| Pass-By | `UnitsPassByHandler.HandleOverlap` | A valid pass-by overlap |
| Family Super Time | `PlayerController.ActivateFactionSuperTime` | Super time starts |
| Sisters' Rivalry | `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider` | Basic-attack kill gives the sister AP and resets her basic attack cooldown |
| Linda First Move | `LindaFirstMove.Apply` | Family buff applied at level start (when unlocked) |
| Papa's Shelter | `LucyPassiveAbility_PapasShelter.RefreshState` | Shelter on/off |
| Tempest Bloom | `LucyCycloneProjectileScatter` | Projectile split by the cyclone |
| Atman Focus | `MarkPassiveAbility_AtmanBarrier`, `MarkPassiveAbility_AtmanFocus` | Focus gained |
| Atman Barrier | `MarkPassiveAbility_AtmanFocus.ProcessDecrement` | Damage absorbed / barrier broken |
| Continuous Attack | `MarkPassiveAbility_ContinuousAttack.PerformFollowUpAttack` | Follow-up basic attack |
| Catch & Return | `ProjectileCatchAndReturn.Apply` | Projectile caught (mode: refund / bounce) |
| Command Shield Dash | `JohnPassiveAbility_CommandShieldDash.PerformShieldDash` | Free dash after Command |
| Wrath | `Features/Player/John/Scripts/JohnPassiveAbility_Wrath` (new) | A stack is gained when John's health drops under Shield Up or through his family role (detail: `took damage under Shield Up: N stack(s)` or `took the hit for family: N stack(s)`), and when the stacks are spent by his next damaging ability (detail: `spent N stack(s), +X% damage`) |
| Shield Flare | `Features/Player/John/Scripts/JohnShieldRelay.LaunchCopies` (2026-10-09) | Lucy's fireball reaches John while Shield Up is on: it is absorbed and relaunched along the diagonals or straight lines (detail: `<pattern> burst, range N`, no targets). The absorbed fireball keeps Lucy's attack open until all copies land, so their damage is credited to her attack's frame; John takes none, so he gets no HP row. The line is queued after that frame's rows |
| Blood Debt | `Features/Player/John/Scripts/JohnPassiveAbility_BloodDebt` (new) | John's side takes a hit from a new enemy, or his family role activates: that enemy becomes the debtor (detail: `new debtor`, target = the debtor's label, e.g. `✦ Blood Debt · John: new debtor → DarkClaw #10-03`). Only when the debtor changes |

**Family roles** (John, Lucy, Linda, Mark, and the enemy Masher counter) are hooked once, in `FactionRoleHandlerBase.Activate`. The log writes one reaction line, `↳ Unit (cell) › Family Role: <ability> → targets`. Non-family units show `Reaction:` instead. The ability's later `abilityActivationStarted` does not write a second action line, but it still opens a frame so its damage is attributed to it.

**John's family role** never activates its ability or raises `abilityPerformed`. It redirects the attacker's targets to John and gives him a damage-reduction modifier. Raising `abilityPerformed` there was rejected: `CombatLevelRunHandler.OnAbilityComplete` would then re-enable grid input, re-check objectives and fill ATB in the middle of an enemy attack. Instead, the base hook records the reaction, and `JohnFactionRoleHandler` overrides the new `virtual string CombatLogNote => "takes the hit"`. The damage then shows on John's row under the enemy's action.

**John's Wrath and Blood Debt (2026-10-08)** hang off that same role. Neither raises `abilityPerformed` or any other new event; both only raise synergy lines:
- When the role activates, `JohnPassiveAbility_BloodDebt` reads the enemy ability in progress (`SessionLogs.ActionsInProgress[0]`) and marks its owner as debtor. This happens before the redirected hit lands, which is why a late-arriving arrow is still attributed. Like any note raised while a frame is open, the `✦ Blood Debt` line is queued and written after the rows of the enemy action in progress, not right after the role's reaction line.
- The redirected hit is a health drop on John, so `JohnPassiveAbility_Wrath` counts it from his health (`onValueDecreased`), not from `onUnitDamageDone`. It appears as a `✦ Wrath` line queued after the frame's rows.
- Damage dealt to a debtor is logged as ordinary HP rows. The ×1.3 is not logged separately; it is already inside the logged numbers.

### 4.5 Dev cheats (2026-10-10)

`CheatHandler` raises `RaiseCheat` once per use, only when the cheat actually does something, and before it is applied. Cheats: `Kill`, `Heal`, `Damage` (detail `-1 HP` / `-10 HP`), `AP` (`+1 AP` / `fill AP, reset cooldowns`), `ATB` (whole family), `Family points` (`+99 FP`), `Game speed` (`x1.3`, `reset to x1`), `Complete objective`. (Before 2026-10, K was bound to both Kill and Family points; Family points is now on L.)

- The log flushes pending changes to their real owner first, then writes `[R2 Player] CHEAT Kill → DarkClaw #10-03`, and credits every change up to the next flush point to the cheat. Those rows are written under the CHEAT line (`CombatLog.Cheats.cs`, cheat frame with `IsCheat`).
- Cheat rows never count: they are skipped in dealt, taken, healed, kills, family downs and the per-unit tables.
- `LevelEnd` and `MissionEnd` get ` · CHEATED: Kill ×2, Complete objective` in the text and a `CHEATED` flag in JSON. Balance scripts should drop (or separate) levels whose `LevelEnd` has that flag: a cheat can still change what follows, e.g. an enemy killed early never attacks.
- Editor window: CHEAT lines and the `CHEATED` tag are bold magenta.
- Enabling cheats (C+H+T or the `cheatsEnabled` setting) is not logged; only uses are.

## 5. Attribution model (frames and rows)

The existing `onUnitDamageDone` event was **not** used for HP. It fires only for enemy-relation targets, only for HP loss (no heals, no friendly fire, and the Masher's area attack hits its own side), and only after the ability is complete. Instead:

- **Known state.** For every tracked unit, the log keeps its last known HP (`GetHealthAttribute().Value`, rounded) and cell.
- **Frames.** `abilityActivationStarted` opens a frame (ability, owner, owner label, title, is-move, depth); `abilityPerformed` closes it. Frames can nest: a Linda reaction fires inside an enemy move, and Lucy's role fires during the dispatch of an ally's `abilityPerformed`.
- **Rows.** Per-unit pending results: CRIT, EVADED, statuses, killed, spawned, revived, kill rewards, pickups. HP and cell differences are found at flush time by comparing against the known state.
- **Flush points.** Pending rows are written under the **innermost open frame** at each of these moments:
  - A frame opens: pending changes belong to the frame that was on top before it.
  - A frame closes: if it is innermost, the changes are its own; otherwise they belong to the innermost frame still open. This is `CombatLogFrameStack.Close`.
  - Turn start/end and level end: everything is flushed, and changes with no open frame are written **unattributed** (prefixed `~`), e.g. Burn ticks.
- **Notes** (synergies, run upgrades, level-ups, mission rewards) raised while a frame is open are queued and written after that frame's rows. With no frame open, they are written immediately.

Why it is ordered this way: `GlobalEventBus.Awake` adds the `onActionFlowEvent` forwarders first, `CombatLevelRunHandler` subscribes next, and the log subscribes last. So within one `abilityPerformed` dispatch, family-role triggers and kill rewards (raised from `OnAbilityComplete` → `OnAbilityPerformedOn`) happen before the log closes the frame. That is why kill drops attach to the victim's row under the right action.

## 6. Naming and formatting

- **Family roster units** (player faction at level start): nickname (`John`).
- **Everyone else**: compact nickname plus start tile, `DarkClaw #10-03`. Coordinates are two digits; negatives use `m` (`#m02-05`), so `-` stays the separator. Duplicates get `·2`, `·3`, and so on.
- **Summoned or spawned units** (born after `levelStarted`, of any faction, including Lucy's decoy) are named after their spawn tile. Their row says `spawned at (x,y) by <frame owner · ability | bound spawner | level>, N HP`. A spawn seen before it has a cell gets a provisional `Name #??` label, which is fixed at the next flush.
- **Cells**: `(x,y)`. Each action line shows the actor's cell. Cell targets are listed with their occupant's label. More than 4 cells collapse to `N cells (x1,y1)..(x2,y2)`.
- **Moves**: the Move ability line shows the destination cell. Forced or other movement shows on the moved unit's row as `moved (a)→(b)`. The mover's own row is skipped for its own Move ability.

### Line formats (`CombatLogFormat.Compose`)

```
=== Mission: <name> · seed <n> · <date>[ · sandbox]
--- Level: <level>[ · attempt n]
LOADOUT <subject>: <detail>
[R<round> <Phase>] -- <Phase> phase
[R<round> <Phase>] <Actor> (<x,y>) › <Ability> [flags] → <targets> (<note>)
[R<round> <Phase>]   ↳ <Actor> (<x,y>) › Family Role: <Ability> → <targets> (<note>)
[R<round> <Phase>]     <Subject>  -12 HP (16→4)  CRIT · +Burnt (2) · KILLED · +3 XP (2 each), +1 Gold
[R<round> <Phase>]   ~ <Subject>  -1 HP (5→4)  -Burnt                (no ability caused it)
[R<round> <Phase>]     ✦ <Synergy> · <Unit>: <detail> → <targets>
[R<round> <Phase>] REWARD <kind>: <rewards>
[R<round> <Phase>] RUN UPGRADE <title> → <unit|family> · <kind>
[R<round> <Phase>] LEVEL UP <unit> +1 (skill point)
[R<round> <Phase>] CHEAT <cheat> → <targets> · <detail>
--- Level end: WIN · 3 rounds · dealt 142 · taken 23 · healed 10 · kills 6 · family down 0
    Damage by unit: John 54 · Linda 40 · ...
=== Mission end: COMPLETE · 6 levels · 14 rounds · ... · 12m05s
```

Indentation is 2 spaces per depth. Result rows add 2 more. Phase is `Player`, or the faction's relation to the player (`Enemy`, `Ally`). The round is `CombatLevelRunHandler.TurnNumber`, which counts full rounds of all factions.

## 7. Entry model (`CombatLogEntry`)

| Field | Meaning |
|---|---|
| `Seq` | Sequence number within the mission (from 1) |
| `Mission`, `Level`, `Round`, `Phase` | Context, stamped by `CombatLogBook.Add` |
| `Kind` | `MissionStart, MissionEnd, LevelStart, LevelEnd, Loadout, Round, Action, Result, Synergy, Spawn, Reward, RunUpgrade, LevelUp, Summary, Cheat, Note` |
| `Visibility` | `Player` (in-game panel) or `Balance` (loadouts, per-unit damage and kill tables) |
| `Depth` | 0 = top level; 1+ = nested reaction or result row |
| `Actor`, `ActorCell`, `Ability`, `Targets` | Who did what to whom. On result rows, `Actor`/`Ability` = the owning frame (null = unattributed) |
| `Subject`, `HasHp`, `HpBefore`, `HpAfter`, `HpDelta` | Result-row subject and HP change |
| `Flags` | CRIT, EVADED, ±Status (life turns), KILLED/DOWN, moved, spawned, revived, friendly fire, picked up, rewards, item uses left |
| `Detail` | Free text (notes, summaries, loadout) |
| `Text` | Composed line |

## 8. Output

- **Memory:** `MissionTracker.Instance.CombatLog.Book.Entries` holds the current mission. `EntryAdded` fires for each new entry (for UI). Entries are cleared when the next mission starts.
- **Files:** `Application.persistentDataPath/CombatLogs/<yyyyMMdd-HHmmss>_<Mission>.log` and `.jsonl`. These are written only when **GlobalSettings > DEV > Combat Log To File** (`combatLogToFile`, default true) is on at mission start. `CombatLog.CurrentTextFile` holds the current path.
- **Deleting log files:** `CombatLogFileSink.DeleteAll()` removes only `*.log` / `*.jsonl` in `CombatLogs` (then the folder if it is empty). It runs from **Tools > Combat Log > Delete Log Files...** (confirmation dialog with the file count; in Play mode the mission in progress keeps its files) and from the main menu's **ResetSettings** button (`AudioSettingsPanel.ResetSaveData`, after the confirmed progress reset, before quitting). **Tools > Combat Log > Open Log Folder** opens the folder. (2026-10-10)
- **JSONL schema:** one object per line with keys `seq, mission, level, round, phase, kind, visibility, depth, actor, actorCell, ability, targets[], subject, hpBefore, hpAfter, hpDelta (only when HP changed), flags[], detail, text`.
- **Editor window:** `Tools > Combat Log > Open Window` (was `Tools > Combat Log` before 2026-10-10). Toggles for balance lines, auto-scroll and colours, a search box, Copy (copies the plain visible lines) and Open folder. It keeps showing the last log after Play stops.
  - Colouring is display-only (`Editor/CombatLogRichText.cs`, one regex pass over `Text`; entries and files stay plain). Family names (taken from the level's LOADOUT lines) are blue; opponent and summon labels (`Name #xx-yy`) are red. Damage is orange and healing green. CRIT, KILLED and DOWN are bold. Statuses are purple (gained) or muted purple (lost). Rewards are gold. Cells and the `[R# Phase]` prefix are grey. Ability and synergy names are bold. Headers are bold gold, and balance lines are grey. There are dark-skin and light-skin palettes.

## 9. Lifecycle

- **Hook:** `CombatLevelRunHandler.InitializeEvents` calls `MissionTracker.Instance.CombatLog.HookLevelEvents()`, right after the existing `Stats.HookLevelEvents()`. A guard ensures one subscription per bus instance.
- **New mission:** detected when the `ActiveMission` or `GraphSeed` differs from the open log. The seed is rerolled on every mission entry. An open previous log is closed as `UNFINISHED (left, quit or replaced)`.
- **Level restart** (same seed, e.g. a defeat in the opening mission): same mission log, with `--- Level: X · attempt 2`.
- **Level start** (`levelStarted`): labels (family by nickname, others ordered by y then x), HP and cells, tags, loadout.
- **Level end** (`levelEnded`): flush everything, then the level summary. `MissionComplete` closes the mission as `COMPLETE`. `Defeat` with `CanReturnHome` closes it as `FAILED`. A plain win or a restart-defeat keeps it open.
- **Loadout (Balance)**, one line per family unit: HP current/max, skill tree nodes with level > 0 (`GetSkillTreeNodes`), equipped items and levels (`EquipmentManager`), items with uses left. Then a `Family` line (faction stat levels, shown as `L1→2` when a run upgrade raises the effective level, plus granted run upgrades) and an `Opponents` line (label + HP).
- **Totals:**
  - Per level: rounds, damage dealt to opponents by family, damage taken by family roster, healing on family, kills, family downs, and damage and kills per unit.
  - Per mission: the sum of the levels, plus all rewards and elapsed time (`MissionStatsTracker.ElapsedSeconds`).
  - Friendly fire is flagged on the row but not counted as damage dealt.
  - Summons (e.g. decoys) don't count as family for taken, downs or XP split.

## 10. Tests (`Core/Systems/CombatLogging/Editor/`: `CombatLogTests.cs` 12 tests, `CombatLogRichTextTests.cs` 5 tests)

- Unit labels: padding and negative coordinates.
- Cell lists and area collapse.
- `Compose`: result row, unattributed row, nested reaction.
- JSON: escaping, and HP keys left out when there is no HP change.
- `CombatLogBook`: context stamping, sequence, sinks, and closing on `Begin`.
- `CombatLogFrameStack`: nested-reaction attribution, and closing an unknown frame.
- `SafeFileName`.

The expected suite grows by 10 tests; `AIRegressionTest.Baseline_MatchesCurrentAI` stays the only red one.

## 11. Changes to existing files (additions only: 21 files, +83 lines)

| File | Change |
|---|---|
| `Core/Managers/GlobalEventBus.cs` | 5 events + 4 static raise helpers |
| `Core/Managers/CombatLevelRunHandler.cs` | Hook call; `RaiseRewards` in kill / completion / failure awards; `levelEnded` invoke |
| `Core/Managers/MissionTracker.cs` | `CombatLog` property |
| `Core/Managers/GlobalSettingsSO.cs` | `combatLogToFile` (DEV) |
| `Core/Systems/TagSystem/Runtime/GTagSet.cs` | `OnTagRemoved` event + raise |
| `Core/Systems/RunUpgrades/Runtime/RunUpgradeTracker.cs` | Raise on successful grant |
| `Core/Entities/Runtime/Pickup.cs` | Raise rewards for resource pickups |
| `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` | `CombatLogNote` virtual + raise in `Activate` |
| `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs` | Duo + Mark-Linda race records |
| `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsPassByHandler.cs` | Pass-by record |
| `Core/Interactions/Runtime/PlayerController.cs` | Family Super Time record |
| `Features/Player/John/Scripts/JohnFactionRoleHandler.cs` | `CombatLogNote => "takes the hit"` |
| `Features/Player/John/Scripts/JohnPassiveAbility_CommandShieldDash.cs` | Record |
| `Features/Player/John/Scripts/JohnPassiveAbility_Wrath.cs`, `JohnPassiveAbility_BloodDebt.cs` | New scripts (2026-10-08); each raises `RaiseSynergy` (see §4.4). Not edits to existing files, so they are not in the +83 lines count above |
| `Features/Player/John/Scripts/JohnShieldRelay.cs`, `Features/Player/Lucy/Scripts/LucyFireballProjectile.cs` | New scripts (2026-10-09, Lucy + John shield relay); `JohnShieldRelay` raises `RaiseSynergy` ("Shield Flare", §4.4). Not in the +83 lines count |
| `Core/_Dev_/Runtime/CheatHandler.cs` | `RaiseCheat` in each cheat (2026-10-10, §4.5) |
| `Resources/Tags/GTagSet.asset` (data) | New `BloodDebt` tag with `showInGame` on, which the log picks up as a status (§4.3) |
| `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`, `LindaFirstMove.cs` | Records |
| `Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs`, `LucyCycloneProjectileScatter.cs` | Records |
| `Features/Player/Mark/Scripts/MarkPassiveAbility_AtmanBarrier.cs`, `MarkPassiveAbility_AtmanFocus.cs`, `MarkPassiveAbility_ContinuousAttack.cs`, `ProjectileCatchAndReturn.cs` | Records |

When committing, also stage the `.meta` files Unity creates for the new `CombatLogging` folder and files.

## 12. Known limitations and open items

- [ ] Compile in Unity, run EditMode tests, play one mission and read the log (line order around reactions especially).
- Silent abilities (pass-by effects, duo partner abilities, the Masher's approach walk) raise no bus events. Their effects are attributed to the enclosing frame (e.g. the move or the duo trigger), or show up unattributed.
- If an inner frame opens while an outer ability still has effects to apply, some of the outer ability's changes can be credited to the inner one. Abilities don't interleave in practice, so this should be rare.
- `LindaFirstMove` is recorded only if its `levelStarted` listener runs after the log's (true for spawned roster units).
- Pickups that only call a function are not logged, unless they also grant resources or a run upgrade.
- A frame closes only on `abilityPerformed`. An ability that starts but never fires it keeps its frame open until the next phase change, and lines in between nest under it. Cancelled targeting opens no frame (frames open on `abilityActivationStarted`), and none has been seen in play; check in play if line depth looks wrong.
- Mark's Continuous Attack follow-up reuses the basic-attack `RuntimeAbility` object. Frames match by reference, so nested copies resolve last-in-first-out, with the same owner label either way.
- John's Wrath and Blood Debt: the order of the `✦ Wrath` and `✦ Blood Debt` lines relative to the enemy's rows has not been checked in a real log. Wrath is counted from John's health, so any health loss while Shield Up is active counts, including from sources other than enemy attacks (e.g. hazards). If a stack is spent by an ability that finishes the same frame, the `spent` line is queued after that frame's rows.
- Shield Flare: the copies' damage rows sit under Lucy's attack, so the per-unit damage table credits it to Lucy, not John. Whether the line order reads well (Lucy's rows, then `✦ Shield Flare`) has not been checked in a real log.
- Not logged yet: duo QTE results, stat-modifier effects (e.g. John's DR, Mark's Focus buff value; Wrath's current stack count is only in its synergy lines, not on the unit's rows), ATB/AP/FP changes, Home-side purchases (skill tree, stations, equipment). The loadout snapshot covers the latter.
- Phase 2: an in-game panel bound to `CombatLog.Book.EntryAdded`, filtered to `Visibility.Player`, probably with friendlier wording.

## 13. Extending

- **Record a new synergy or passive:** add `GlobalEventBus.RaiseSynergy(ownerUnit, "Name", "detail", targets)` where it fires. Nothing else is needed.
- **Add a family-role note:** override `CombatLogNote` on the handler.
- **New reward source:** call `GlobalEventBus.RaiseRewards(receiver, source, "<Kind>", rewards)`. `"Kill"`/`"Hit"` attach to the source's row, `"Pickup"` to the receiver's row; any other kind gets its own `REWARD` line.
- **New entry kind:** add it to `CombatLogKind`, add a `case` in `CombatLogFormat.Compose`, and add a test.
- **Another output:** implement `ICombatLogSink` and add it in `CombatLog.BeginMission`.
