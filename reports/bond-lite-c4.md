# Report: Bond Lite C4 (Sister's Rivalry behind its node, once per turn; the Rivalry node)

Plan: plans/onboarding/2026-10-26-bond-lite-tech.md    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done, nothing staged. The rule is tested; the provider firing in a real level and the node in the panel need THJ's play check. One question for THJ (the cap is per sister).

Paths are under `miso/Assets/_Project/`.

## What changed

- `Resources/Unlockables/UnlockableSet.asset`: new entry `SistersRivalry` at the end of the list, empty group, off by default, cost 1 `MainResource_FamilySP`. 10 added lines.
- `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`: node `[8]` "Sister's Rivalry". 46 insertions, 1 deletion (array size 8 to 9); see "Prefab diff".
- `Features/Player/Linda/Scripts/SistersRivalry.cs` (+ `.meta`): new. `SynergyId`, `IsUnlocked(tracker)` and the plain class `RivalryTurnCap`.
- `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`: reads the literal, uses the cap instead of the 2 s guard, no reset call, "basic attack ready" gone from the detail.
- `Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs`: `Title` spelled "Sister's Rivalry". The id `"Sisters' Rivalry"` stays.
- `Resources/Tutorials/Tutorial_LucyLindaKillAP.asset`: one phrase removed; see "Tutorial text".
- `Core/Editor/SkillTreeSmokeTest.cs`: 10 family nodes, 16 points granted and spent.
- `Core/Systems/HomeSystem/Editor/HomeLockRulesTests.cs`: the real-entry check now covers Rivalry too (test renamed `LiteralLock_NamesARealEntryOfTheUnlockableSet`, two cases).
- `Core/Systems/HomeSystem/Editor/BondNodeGateTests.cs`: test renamed `RealTrees_MarksSistersAndTempestBloomAndRivalry_AreLockedFamilyNodes`, Rivalry added.
- `Features/Player/Linda/Scripts/Editor/SistersRivalryTests.cs` (+ `.meta`, and `Editor.meta` for the new folder): new, 10 tests.

No core system file changed. `Level1-C2` and `Level1-C4` still remove the component; untouched.

## Acceptance criteria

- [x] Off when locked: `Locked_ItIsOff_UntilTheNodeIsBought`, `Locked_ItIsOff_WithNoTracker`, `AnotherUnlockable_DoesNotTurnItOn`.
- [x] On when owned or by a run upgrade: `Bought_ItIsOn`, `RunUpgrade_ItIsOn_WithTheNodeNotBought`.
- [x] Once per turn, with the turn identified by the owner's faction: `Cap_OneUsePerTurnOfTheOwner`, `Cap_AnotherFactionsTurnDoesNotGiveItBack`.
- [x] Entry exists before the gate reads it, cost 1 Family point: `Entry_CostsOneFamilyPoint`, `LiteralLock_NamesARealEntryOfTheUnlockableSet`.
- [x] Node data (family, literal, `unlockLevel` 0, title, no "ready" or "cooldown" in the text): `Node_IsAFamilyNodeWithNoLevelAndNoNewPoints`. `GetUnlockLevels` is distinct and 0 is already in Lucy's list, so points awarded don't change.
- [x] Node is locked at Bond Lv 2 like the other two: `RealTrees_...`. Lock counts stay at 3.
- [x] Silent-lock test passes with the new entry (in the full suite).
- [x] Synergy id tied to Bond: shared constant `SistersRivalry.SynergyId` and `SynergyId_IsTheOneBondSettingsPaysHelpFor`, which reads the real `BondSettings.asset`.
- [x] EditMode suite: 1569 of 1570 passed. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`. A `get_test_job` wait timed out once; calling again returned the result.
- [x] **`AIRegressionTest` didn't move:** ran it before any edit and after: 42 FAIL lines both times, the same lines. Not re-baselined.
- [ ] **Not verified: the provider itself.** Its handlers run only in Play, so no test catches a removed call to the cap or the gate. See "How to see it".
- [ ] **Not run: `SkillTreeSmokeTest`.** It is a Play-mode menu tool; it only compiled.

## Save reset

No. `SaveData.json` keeps its 2026-11-06 17:24 timestamp.

## Decisions I made

- **Lucy's tree.** Tempest Bloom and Marks-Sisters both sit on `Unit_Lucy` as family nodes and Linda has none, so all three locks on the pair stay in one tree. The Family view is one aggregated panel, so the player can't tell the difference. Slot: row 2, column 0 (Toba's Healing Marks is at row 2, column 1; nothing else in row 2). Graph position (640, -1400), next to Marks-Sisters.
- **How entries are indexed:** by string id (`_` + id, through a dictionary), not by position, so nothing can shift. Appended at the end anyway.
- **The literal is a code constant, not a serialized field.** `LucyCycloneProjectileScatter` uses a field; here that would mean editing two more prefabs. `HomeLockRules.SistersRivalryUnlockable` is the same text the lock uses. Combat reads only that string, not Bond.
- **Turn identification:** the bus's `turnStarted` compared with `_owner.Faction`, as `JohnPassiveAbility_Wrath` listens to it. Not `CombatLevelRunHandler.TurnNumber`: it only counts full rounds and doesn't move while the turn index is locked.
- **Reset call removed.** D-232 says +AP only, and nothing depends on the call: both sisters' basic attacks have cooldown 0 at runtime and `initialCooldown` 0 on the prefabs. `AbilityOrchestrator.GetBasicAttackAbility` is still used by others. See the risk on Lucy's data below.
- **Icon:** node and entry use `c93cb2c6...`, the sprite on Lucy's Lingering Embers. Mark's Catch & Return uses a sprite of the same name as a stand-in too. No Rivalry art exists.
- **No new statics.** Only consts; the cap is an instance field. No reset hook needed.
- **Classic:** the two "off" tests use `Assume`, so applying W7b's `unlockedByDefault` 1 makes them inconclusive rather than red. `Entry_` doesn't check the flag.

## Placeholder text

- Node description: `[Synergy] When Linda or Lucy scores a kill with her basic attack, the other gains +1 AP, once per turn.`
- Lock line for this node comes from C2's wording.

## Prefab diff

`Unit_Lucy.prefab`: 46 added lines, all `skillTree.nodes.Array.data[8].*` overrides, plus the size line. Saving through `PrefabUtility` also wrote two lines of Unity defaults into the role's QTE profile (`preloadOverride: -1`, `showSpeed: 1`); I removed those by hand as noise, so they are not in the diff. Unity will likely write them again the next time anyone saves this prefab; they change nothing. `unlockLevel` 0, `upgradeLevels` 0 and the empty text fields don't appear because they equal the defaults.

## Tutorial text

`Tutorial_LucyLindaKillAP.asset`, used by `LevelE1C1_TutorialSequence`. Second bullet was "They gain 1 AP and their attack cooldown is reset." and is now "They gain 1 AP." That is the one phrase removed. Not changed, for narrative or the coordinator to weigh:
- "can attack again when the other scores a kill" is still true through the AP, but doesn't state the once-per-turn cap.
- The second page says "Several of these synergies are pre-unlocked for this demo", which holds only with W7b.

## Worker thread

The AI doesn't read the provider: no reference under `AISystem`, and it only listens to `onUnitDamageDone` and `turnStarted`, both raised on the main thread from `CombatLevelRunHandler`. `FactionTracker.GetUnlockableState` runs inside that handler.

## Needs THJ

**Is the cap per sister, or one for the pair?**
- Context: each sister has her own provider, so Linda's kill gives Lucy +1 AP and Lucy's kill gives Linda +1 AP, each once per turn. That is up to 2 AP per turn between them.
- (a) **Recommended, and what's built:** per sister, as the brief says ("once per owner's turn"). It keeps the back-and-forth of the kill chain.
- (b) One for the pair, 1 AP per turn in total. D-173's "cap 1 per turn" could mean this. Weaker, and needs a shared cap.
- Blocked meanwhile: nothing. Worth judging in the play check.

## Docs to update

- `design/gdd/family-systems.md` line 95: gate, once per turn, +AP only; "at most once every 2 s" and "basic attack ready again" are out of date. Line 132's "open from the start" on this branch too.
- `tech/classic-fallback.md` W7b: the entry now exists; the two tests go inconclusive with it.
- `tech/home-system.md`: Rivalry node and `SistersRivalry`, with the plan's end-of-feature doc pass.

## Risks and loose ends

- **Lucy's upgraded primary has a dormant cooldown.** `Lucy_Ability_PrimaryAttack`'s higher levels hold cooldown 1 with `upgradeMode` 2 (All), but `AbilityPreset.GetParameters` only uses a level's parameters when the mode is exactly `ParameterUpdate`, so it reads the base 0. If that check is ever fixed in core, Lucy with Sidewinders would get a cooldown of 1 and Rivalry's AP couldn't buy a second attack. Read in code, not changed. D-220's refund is where the reset comes back.
- **A kill outside the owner's turn:** the use returns when the owner's faction starts its turn, so a basic-attack kill in an enemy turn can still fire if the use wasn't spent in the player's turn. The old code fired there too. Kept, not restricted. I didn't confirm which reactions count as basic attacks.
- **Scripted phase restart:** `ResetCurrentPhase` (`LevelSpecificBehaviour`, mode Reset) calls `RestartTurn`, which raises no `turnStarted`. A spent cap stays spent through such a restart until the next turn. Fixing it would mean a core change, so I left it.
- **Family points:** the tree now costs 16 to fill and level-ups earn 15 (`SkillTreeSmokeTest:57`). The Yard's point covers it in this order of play; the smoke test grants its own.
- **Help Bond:** with Rivalry locked, it can't pay help in The Trail; only the Duo can. C3's numbers hold (the Yard crosses 25 with no help at all). With the node bought it also fires less often than under the 2 s guard.
- **Test saves:** C3's warning stands. On a save with The Trail completed, the Yard can't reach Lv 2.
- **Console:** after the suite, the console holds errors logged during tests, including "Unsupported type Vector2f". I didn't trace that line; no test failed on it.
- Not mine and left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, the TMP font, `PreloadScreen.unity`, `ProjectSettings/*`.

## Proposed commits

Nothing staged. For after THJ's play check, in this order:

1. `feat(home): Sister's Rivalry gets a Family-tree node behind the sisters' Bond` (prefab and shared data; own commit so it can be reverted alone):
   - `miso/Assets/_Project/Resources/Unlockables/UnlockableSet.asset`
   - `miso/Assets/_Project/Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/HomeLockRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondNodeGateTests.cs`
   - `miso/Assets/_Project/Core/Editor/SkillTreeSmokeTest.cs`
2. `feat(combat): Sister's Rivalry needs its unlock and gives AP once per turn` (behavior change for the sisters in every level; needs 1, because the gate reads the entry):
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/SistersRivalry.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Editor.meta`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Editor/SistersRivalryTests.cs` + `.meta`
3. `fix(tutorial): Sister's Rivalry page no longer promises a cooldown reset` (plain):
   - `miso/Assets/_Project/Resources/Tutorials/Tutorial_LucyLindaKillAP.asset`

## Other branches

`thj/home-test`, at merge: its Bond locks and `HomeBondLocks` read differently; the Rivalry node and the literal gate need carrying over. Classic: W7b, coordinator's.

## How to see it

Nothing raises the sisters to Lv 2 until C5, so opening the node needs a hand step that writes to the save (as in C2). Use a save whose Bond entry you don't mind changing.

**Node:**
1. Play to Home, open the skill tree, select the Family tab. "Sister's Rivalry" sits in row 2, left of Toba's Healing Marks, with a lock icon. Check the layout looks right there; I only read the slot from data.
2. Click it: the placeholder description, then "Opens with Linda & Lucy's Bond, Lv 2". Upgrade is greyed out and spends nothing, even with a point in hand.
3. Add the points from a debug snippet (`BondStore.Instance.Add("Linda", "Lucy", 10, BondSource.HomeActivity)`; this writes to the save). Reopen the tab: it can be bought for 1 Family point. Level-up points awarded stay the same.

**Combat, locked** (don't buy it): in a level with both sisters, kill an enemy with one sister's basic attack. No AP for the other, and no "Sisters' Rivalry" line in the combat log.

**Combat, bought:**
4. Kill with Linda's basic attack: Lucy gains 1 AP; the log shows `Linda kill: +1 AP`, with no "basic attack ready".
5. Kill again with Linda in the same turn, even after a long wait: no second AP. That's the old 2 s guard gone.
6. Then kill with Lucy: Linda gains 1 AP (the question above: is this what you want?).
7. End the turn. On the next player turn, the same kills pay again.
8. A piercing arrow or area basic attack killing two at once pays one AP.

**Levels with Rivalry locked (they were tuned with it on):** `GB_m3-john`, `GB_m4-mark` and The Trail. And Rivalry's worth for Linda under the Quiver: she gets AP, no arrow.

**Other:** `Level1-C2` and `Level1-C4` behave as before, since they remove the component. Tools > Skill Trees > Run Smoke Test in Play mode should pass with 10 nodes and 16 points, but it skips the lock, so run it on a save you don't mind changing.

## Review (coordinator's condensed copy, 2026-11-07)

**APPROVE.** Read only. Should fix: `UnitKillAbilityPointProvider.cs:50-54` spends the turn's use and raises the synergy (paying help Bond) even when `Produce` gives nothing at the cap of 3. Verified: subscription lifecycle, reset before kills, no enemy-turn route found, cooldown removal safe, no AI path, Bloom unchanged, data clean, per-sister cap as built (THJ's question). Scripted restart can cost one AP use in `GB_m4-mark`, only if already bought; left. Family points add up to 16 with no spare; full 15 from level-ups needs all five at 5 SP spent. No test fails if the provider stops calling gate or cap: play check covers it (locked kill gives nothing, second kill in a turn gives nothing, next turn pays). Docs: `design/gdd/progression-economy.md` PR-8 and unlock table, at the close.
