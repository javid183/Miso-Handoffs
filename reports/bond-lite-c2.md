# Report: Bond Lite C2 (Family-tree node gate and lock text)

Plan: plans/onboarding/2026-10-26-bond-lite-tech.md    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done, with one plan fact corrected (Marks-Sisters has no literal) and one question for THJ. The panel itself still needs the play check.

Paths are under `miso/Assets/_Project/`.

## What changed

- `Core/Systems/HomeSystem/Runtime/BondLite/BondNodeGate.cs`: new. The one effective state: `EffectiveState` (`GetNodeState` plus Locked when shut), `IsShut`, `LockOf(node)`, `LockLine`. Pure overloads take the lock and the level, for tests; the node overloads read `BondStore.Instance` each time and only for a node with a lock.
- `Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs`: `FindByUnlockable` (the literal lookup), `FindByNodeGuid`, new `HomeLock.NodeGuid`, Marks-Sisters in `All`.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.cs`: `ShowFamilyAbilityBars` spawns with the effective state.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.BondLock.cs`: new partial. A node with levels already bought shows them under the lock.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.cs`: `RefreshDescriptionPanel` uses the effective state and adds the line; `UpgradeButtonClickedEvent` returns early when shut.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.BondLock.cs`: new partial with those two helpers.
- `Core/UI/Runtime/Home/CharacterSelect/AbilityUpgradeDescriptionPanelUI.cs`: `partial` keyword only.
- `Core/UI/Runtime/Home/CharacterSelect/AbilityUpgradeDescriptionPanelUI.BondLock.cs`: new partial, `ShowLockLine`.
- `Core/UI/Runtime/Home/UpgradePanel/UpgradeTreeButtonUI.cs`: new `ShowLevelInsteadOfLock`; `SetData` unchanged.
- `Core/Systems/HomeSystem/Editor/HomeLockRulesTests.cs`: counts 2 to 3, Marks-Sisters added to the level check.
- `Core/Systems/HomeSystem/Editor/BondNodeGateTests.cs`: new, 11 tests.
- No prefab or scene edit, so `Home - Scene.unity` and `UpgradesPanel.prefab` are untouched. `SkillTree`, `FactionTracker` and every core system are untouched.

## Acceptance criteria

- [x] Tempest Bloom and Marks-Sisters can't be bought below Bond Lv 2 and can at Lv 2. Rule covered by `BelowTheLevel_AnUpgradableNodeIsLocked_AndCantBeBought` and `AtOrAboveTheLevel_TheNodeKeepsItsOwnState`. **The panels calling it (button, description, click guard) need the verifier's play check.**
- [x] Sister's Rivalry is in the list and found by its literal (`Lookups_FindEachLockOnlyByItsOwnName`). Its node arrives with its data later, so it can't be seen in the panel yet.
- [x] Other nodes unchanged: `ANodeWithNoLock_IsNeverChanged`, and `RealTrees_MarksSistersAndTempestBloom_AreLockedFamilyNodes` reads the real trees and finds only those two nodes locked.
- [x] A bought node stays owned below the level: `ABoughtNode_StaysOwnedBelowTheLevel`. The gate writes nothing, so no level or literal can be lost.
- [x] Lock line says "Opens with Linda & Lucy's Bond, Lv 2": `LockLine_UsesTheApprovedWording`. How it looks in the panel needs the play check.
- [x] `unlockIcon` in the locked state: fine, see below; `TreeButton_Locked_ShowsOnlyTheLock_AndABoughtLevelReplacesIt` instantiates the real prefab.
- [x] `BondStore.Instance` isn't cached: `BondNodeGate` holds no state.
- [x] EditMode suite: 1516 of 1517 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. The plugin session dropped once during the wait; calling again returned the result. No `__*` folder left under Greybox. Console shows no errors after compile.

## `unlockIcon` when locked (`UpgradeTreeButtonUI.SetData:70-74`)

The locked branch never sets `unlockIcon`, and that's harmless: `UnlockedIcon` is inactive in the prefab and buttons are spawned new on each tree refresh, so only `LockIcon` shows. Lock, unlock and level all sit on the same spot under the button (same anchor and position), so they must not show together. The icon keeps full alpha, because only `LevelBlocked` dims it; a Bond-locked node looks like any graph-locked node today.

## Does anything expect the Duo bought? No

- The Marks-Sisters **node isn't the Duo** (see Needs THJ). The Duo comes from the level's and `PlayerController`'s ability lists, which is how `GB_m3-john`, `GB_m4-mark`, `LevelLucyJohn-C3` and the two `LevelMarkIntro` chunks refer to the preset. None of that reads the node.
- The node id appears only in `Unit_Lucy.prefab`. The name "Marks-Sisters" is used in `_Project` only there and in the description of `RU_SistersBondDuoDamage`, which requires the ability, not the node.
- The level plans (`2026-10-26-onboarding-levels.md`, the search-levels plan) use the base Duo at 12 damage. None uses the node's ×1.2 or ×1.35.
- `GuidedSkillSpend` points at a sister's own non-family node. No sequence or test buys this node, except the editor `SkillTreeSmokeTest` menu tool, which skips the lock (accepted in the plan).

Checked by search of code, assets and plans, not by playing.

## Save reset

No. `SaveData.json` still has its 17:24 timestamp and no `Bond` key.

## Decisions I made

- **Marks-Sisters is named by node id.** The brief said "by its real literal", but node `[7]` has none: it's `StatAttribute` (`Stat_DMG` on `Linda_Lucy_Duo_Ability`, 2 levels). Same behavior as asked, so I added `HomeLock.NodeGuid`. Literal nodes look up by literal and all others by id, so a stat node with a leftover literal can't match by accident.
- **Partly bought Marks-Sisters (1 of 2) below Lv 2:** further levels stay shut, and the level keeps its effect. The button shows the level number instead of the lock, since they share a spot; clicking shows the line and a disabled Upgrade. It can only happen on a save from before the gate. Exempting bought nodes would have been simpler, but it would allow a purchase below the level.
- **The line goes in the existing upgrade description label**, after any upgrade text. `abilityUpgradeLbl` was the other choice, but it has a "Requires:" child title and would hide the cost. This needs no new serialized field and no prefab edit. The line is plain text in the label's style.
- **Upgrade button stays visible but disabled** on a shut node, and the cost still shows. That's `ShowPanelFor`'s existing behavior for any non-upgradable state.
- **Placeholder text isn't tagged:** `conventions.md` says panels show the tag, so list it here instead. Line: `Opens with Linda & Lucy's Bond, Lv 2`, built from the lock's pair and level. Changing the wording means updating `LockLine_UsesTheApprovedWording`.
- **Only the Family view asks the gate.** Personal trees skip family nodes, so they need no change. The real-tree test fails if a lock lands on a non-family node.

## Needs THJ

**Is locking only the Duo's damage upgrades what you meant by locking Marks-Sisters?**
- Context: D-424 calls it "the Lucy and Linda Duo node". The node only adds Duo damage (×1.2, ×1.35). The Duo itself can be used in combat from the start and stays so; combat doesn't read Bond (D-202).
- (a) **Recommended, and what's built:** lock the node. A point can't go there before the Yard (D-424's reason), and the levels keep their Duo.
- (b) Lock the Duo itself. That needs a combat gate, against D-202, and the level plans that use the Duo at The Trail would have to change.
- Worth a look under (a): the node's text starts "[Duo] Lucy and Linda combine their ranged skills...", so with a lock on it a player may think the Duo is shut. Its description could say it's an upgrade. Not changed; it's existing data and wording.
- Blocked meanwhile: nothing. (a) stands unless he says otherwise.

## Docs to update

- `tech/home-system.md`: Bond Lite node gate (`BondNodeGate`, the lock is in the panels, id or literal lookup). The plan puts this at the end of the feature.
- `tech/classic-fallback.md`: see the first risk below.
- `design/gdd/family-systems.md`: with the Bond docs, note that the Marks-Sisters node opens at Bond Lv 2.
- Plan: "Family-tree nodes are `UnlockableLiteral`" and "by its literal" don't hold for Marks-Sisters.

## Risks and loose ends

- **Classic fallback:** classic has no Yard. Tempest Bloom and Marks-Sisters now stay shut there until sources give the sisters 10 more points. The plan's classic note only covers Rivalry's `unlockedByDefault`, and that flag wouldn't help Marks-Sisters. The recipe needs a wiring point for these locks, or a raised starting Bond in `BondSettings.asset`. Coordinator's call.
- **Until C3 and C5 nothing raises the Bond,** so on this branch both nodes stay shut on every save unless already bought. Expected for now.
- **Family tab's new-points dot:** `RefreshNewPointsIndicators` only checks for points. With a point and only shut nodes left, the dot stays on with nothing to buy. Six other family nodes can be bought today (Toba, John, Mark; Catch & Return is on by default), so it's unlikely early on, though the Family view only shows nodes of heroes the player has unlocked. Left as is.
- **For C5, stale tree:** the panel rebuilds its tree only when a tab is selected, not when it's re-enabled. If the Yard raises the Bond after the panel has been opened in the same Home visit, the old lock icon stays until another tab is clicked. Clicking the node does read the new level, so the description and purchase are right. The Yard runs on arrival, so it probably doesn't arise; check it in C5's play pass. If it does, refresh the tree on enable or on `BondLevelReached`, and unsubscribe.
- **Other ways to raise those levels:** `RU_SistersBondDuoDamage` still raises Duo damage for a run, and the Altar still grants Tempest Bloom. Both skip the lock, as decided.
- **For C4:** Rivalry's node is found by literal, so it needs no change here beyond its entry and node. `RealTrees_MarksSistersAndTempestBloom_AreLockedFamilyNodes` then needs "Sister's Rivalry" (the node's title) added, and that test will fail until it is.
- `thj/home-test` merge: `BondNodeGate` is new there, and `HomeLock.NodeGuid` must carry over if its `HomeLockRules` replaces this one.
- Not mine and left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, the TMP font, `PreloadScreen.unity`, `ProjectSettings/*`.

## Proposed commits

1. `feat(home): Bond keeps the sisters' Family-tree nodes shut until its level, with a line saying what opens them` (plain, no core):
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondNodeGate.cs` + `.meta`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityTreePanelUI.BondLock.cs` + `.meta`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.BondLock.cs` + `.meta`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/UpgradePanel/UpgradeTreeButtonUI.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/CharacterSelect/AbilityUpgradeDescriptionPanelUI.cs`
   - `miso/Assets/_Project/Core/UI/Runtime/Home/CharacterSelect/AbilityUpgradeDescriptionPanelUI.BondLock.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/HomeLockRulesTests.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondNodeGateTests.cs` + `.meta`

One commit: the rule, its panels and its tests only work together, and the count changes in `HomeLockRulesTests` follow the new list entry.

## Other branches

`thj/home-test`, at merge (see Risks).

## How to see it

Needs a save where the skill tree and the Family tab are open. Nothing raises the Bond yet, so the sisters are at Lv 1 (15 points).

1. Play to Home, open the skill tree and select the Family tab.
2. Tempest Bloom and Marks-Sisters each show a lock icon, with no unlock icon or level number on top. If you bought either already, Tempest Bloom shows as owned, and Marks-Sisters shows its level.
3. Click Tempest Bloom: below the description you read "Opens with Linda & Lucy's Bond, Lv 2", the cost still shows, and Upgrade is greyed out and does nothing, with points in hand.
4. Click Marks-Sisters: the same line comes after "Each upgrade increases the duo's damage."
5. Click another Family node (for example Chained Assault): no line, and it behaves as before.
6. To see it open, add points to `BondStore` by hand and replay, for example with `BondStore.Instance.Add("Linda", "Lucy", 10, BondSource.HomeActivity)` from a debug snippet. **That writes to the save.** The nodes then open and can be bought. C5's Yard does this for real.

## Review (coordinator's condensed copy, 2026-11-06)

**APPROVE.** Read only. One should-fix: a test for the node overloads. No test catches a gate removed from a call site (`AbilityTreePanelUI.cs:112,113`, `AbilityUpgradePanelUI.cs:172,176,182`), so the play check names each: below Lv 2 with a point in hand, lock icon, description line, Upgrade greyed, no point spent; same at Lv 2. Other buy paths: editor tools only. Guided spend's nodes aren't locked. New-points dot left as it is. `NodeGuid` is sound and merge-safe. A stat node whose ability isn't found would read Maxed and dodge the lock; Lucy's lookup should find it (read, not played).
