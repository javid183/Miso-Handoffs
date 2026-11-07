# Bond Lite (pair Bond on `main`) — tech plan

Size: L    Tier: 3 (new reusable system; Home; save data; THJ's yes before any code, D-179)    Assigned to: `miso-implementer` (opus) → `miso-reviewer` → `miso-verifier`
Branch: all (built on `thj/onboarding`; must fold into `thj/home-test` on merge)
Status: **approved (D-233)**; built after the greybox and the pacing check (D-180). Answers: BL1 nodes only (D-202), BL2 lock in the Home skill-tree UI (D-203), BL3 tooltip + Yard scene, no meter (D-231), BL4 +AP only now, the reset becomes D-220's AP refund once its amounts are set (D-232). C1 adds the silent-lock test (THJ)

Design: `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` ("New tech", "The Sister's Rivalry arc"). Work plan step A4(a), build step B7. Decisions: D-173 (Rivalry to the Family tree, Bond gates the pair's nodes, Yard grants the first Family point), D-179 (go to a tech plan), D-180 (built after the greybox and the pacing check).

## Refresh 2026-11-06 (read this first; it overrides what's below)

Audit of the plan against `thj/bond-lite` @ `58aa10418`, from reading code and YAML; nothing run. Paths under `miso/Assets/_Project/`.

**Order and branch.** Built now on `thj/bond-lite` (D-422, D-423), not after the pacing check. C1 to C3 commit after review and tests; C4 and C5 commit after THJ plays them, with the pacing check. Read "on `main`" below as "on this branch".

**Corrections**

- Rivalry's guard is 2 s of scaled game time (`Time.time`), and its detail string still says "basic attack ready" (D-232's text change isn't done).
- `Level1/Level1-C2` and `Level1-C4` remove Rivalry from both sisters through `m_RemovedComponents`; leave those alone.
- No Rivalry data exists: no `UnlockableSet` entry, no tree node. C4 creates the entry **before** the gate reads it (`FactionTracker.cs:472` dereferences the entry), then a Family node with `unlockLevel` 0 (`GetUnlockLevels` counts every node's level, so a new level changes points awarded) on a free slot such as row 2, column 0. `Unit_Linda` has no Family nodes; `Unit_Lucy` has Tempest Bloom `[6]` and Marks-Sisters `[7]`.
- There is no tooltip to extend. The lock line goes in `AbilityUpgradeDescriptionPanelUI` (D-231's "tooltip" becomes this line; coordinator's call, same meaning). Compute one effective state in `AbilityTreePanelUI.ShowFamilyAbilityBars:107-111` and `AbilityUpgradePanelUI.RefreshDescriptionPanel:162-174`, and guard `UpgradeButtonClickedEvent:176-190`. New partial files like `AbilityUpgradePanelUI.Guided.cs`. `SkillTree` is unchanged (D-203). Editor tools skip the lock; accepted.
- Memory 4's Bloom isn't affected: its grant goes through `RunUpgrades.UnlocksLiteral` and `CanGrant` doesn't check node state. Don't flip `unlockedByDefault` on `CycloneArrowScatter` or add `requireUnlockable` to the upgrade.
- Mission-end source: use the `"Mission complete"` rewards event (`CombatLevelRunHandler.cs:908`), subscribed per level; it carries no squad, so read `ActiveMission.MissionRoster.Units` and check the free slot's assignment at that moment. It's skipped in the sandbox.
- Family points: the story grant uses `FactionTracker.GrantAggregatedResource` with `MainResource_FamilySP`, then a save. Level-ups can already have given points before the Yard.
- `Core/Systems/HomeSystem` is effectively empty here, so C1 creates its contents. `MISO.Core.Home.HomeState` exists; avoid that name.

**Added to the chunks**

- **C1 silent-lock test:** starts with an allow-list and a plain reason for `_DoNotRemove_` and `_JohnResolve`, which have no node or run upgrade.
- **C5 Yard wiring:** `DialogNodeSequence` can't grant, so add a new `Sequence` in `Features/Onboarding` and chain it with `SequentialSequence`; update `HomeVisitsWiring.cs:66` and `HomeVisitsTests.cs:190-195`; once-only guard on the grant (`PlayJustOnce`, `SequencePlayer.cs:21,39`).
- **Classic fallback:** the recipe gets a new wiring point when C4 lands: `unlockedByDefault` 1 on Rivalry's entry, so classic stays as is (M5's tutorial page describes Rivalry, and classic has no Yard).
- **Play check additions:** `GB_m3-john`, `GB_m4-mark` and The Trail with Rivalry locked (they were tuned with it on); Rivalry's worth for Linda under the Quiver (AP, no arrow).
- **Altar route to Tempest Bloom:** M6 only, classic. Accepted, unchanged.

**C3 constraint (from C1's review):** no `BondStore.Add` during combat. `BondSources` keeps an unsaved per-mission help tally with its cap, like `_collectedResources`, and makes one `Add` per pair at `"Mission complete"`. So no mid-combat saves, no restart farming, and failed missions give nothing. `Add` stays for mission end and Home activity.

**C2 and C4 notes:** C2 needs a lock lookup by literal. C4's Rivalry entry id is `SistersRivalry` with the set's empty group title; add Rivalry to the real-entry check and to `RealTrees_MarksSistersAndTempestBloom_AreLockedFamilyNodes`; lock counts stay at 3. Use the glossary's spelling "Sister's Rivalry" (`HomeLockRules.cs:45` differs). `SkillTreeSmokeTest.cs:218,238` hard-codes 9 family nodes and 15 points; update it. Marks-Sisters is a stat node locked by id (`HomeLock.NodeGuid`). C5: if `Add` runs after the panel opened in the same visit, rebuild the tree in `OnEnable`. Scene objects must unsubscribe from `BondLevelReached`. Don't cache `BondStore.Instance`.

**Answered by THJ 2026-11-06:** Marks-Sisters is locked too, at Lv 2 (D-424; check no level or M4 plan expects it bought). The Yard raises the Bond, grants one point and points at the nodes in dialogue, with free spending; item 8's forced choice is dropped (D-425). The Hearth adds no Bond (D-426).

## Why

The Sister's Rivalry arc needs the Family-tree unlock to be a story moment: the sisters' Bond reaches level 2 in the Yard scene, both of their nodes light up, and the player spends a story-granted Family point on one. `main` has no Bond; `thj/home-test` has a full one inside its day simulation. Bond Lite is the smallest slice that does this job and folds into `thj/home-test` later.

## Goal

A saved pair-Bond store with three sources, a lock rule that keeps a Family-tree node shut until its pair's Bond level is reached, a level-up hook for Home scenes, and the story Family point, with Linda–Lucy as the only gated pair.

## What exists (read 2026-10-26)

**On `main`:**
- Family-tree nodes are `SkillTree.NodeData` with `upgradeMode = UnlockableLiteral`; buying one calls `FactionTracker.UnlockLiteral` (saved in `UnlockedLiterals`). `SkillTree.CanUpgrade` checks `IsUnlockedByGraph` and the literal (`SkillTree.cs:189-200`).
- Combat reads those literals through `FactionTracker.GetUnlockableState` (meta unlock **or** a run upgrade). Tempest Bloom already works this way: `LucyCycloneProjectileScatter` reads the literal `_CycloneArrowScatter`, which both `RU_LindaLucyCycloneSpreadUnlock` and a node on `Unit_Lucy.prefab` (line ~1259) can grant.
- Sister's Rivalry is `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`: on a sister's lethal basic attack, the other gets +AP (the modifier) and a basic-attack cooldown reset, at most once every 2 s of real time; it raises the `"Sisters' Rivalry"` synergy event. **It reads no unlockable: it's always on.** (Correction to the work plan's risk: the +1 AP part works on `main`; only the "basic attack ready again" part adds nothing, GDD Q11.)
- Family points come from level-ups (`AbilityUpgradePanelUI.AwardFamilySkillPointsForLevelUps`).
- Events for Bond sources: `GlobalEventBus.RaiseSynergy(unit, id, detail, targets)` (Duos raise `"Duo"`, Rivalry raises its own), `RaiseFamilyRoleActivated(handler)`, `RaiseRewards(..., "Mission complete", ...)` at mission completion.
- Save pattern: `ISavable<T>` + `SaveLoadManager.Register(key, instance)` (e.g. `AbilityIntroductionTracker`).
- Name clash: `main` has `MISO.Core.Home.HomeState` (a ScriptableObject of Home idles); `thj/home-test` has `MISO.Core.Systems.HomeSystem.HomeState` (the simulation state, with `GetBond`, `PairKey`, `BondLevel`).

**On `thj/home-test` (read only):** `HomeLockRules` (plain data: lock id, pair, level, unlockable id; `ForPair`, `OpenedBy`, `IsOpen`), `HomeBondLocks` (combat-side snapshot read by Duos and Pass-by on a worker thread, plus `SyncUnlockables` that turns Home unlockables on/off by Bond level), thresholds `{10, 25, 45}` in `HomeCycleDefinition.bondLevelThresholds`, `BondSceneDefinition` for level-up scenes.

## Design of Bond Lite

**One change from the design's "New tech" row: no combat gate.** On `main` the Linda–Lucy abilities become Family-tree nodes, and combat already reads node literals. So Bond only has to keep the **node** shut until the pair's level; nothing in combat code reads Bond. Command Shield Dash and the Linda–Toba Duo stay open (design), so `HomeBondLocks`' worker-thread snapshot isn't needed yet. (Question BL1.)

Pieces (namespace `MISO.Core.Systems.HomeSystem`, folder `Core/Systems/HomeSystem/Runtime/BondLite/`, same names and formats as `thj/home-test` so the merge is a swap):

1. **`BondStore`** — saved store of pair points. `PairKey(a, b)` (same ordering as `thj/home-test`), `GetBond`, `GetLevel` with thresholds `{10, 25, 45}`, `Add(a, b, points, source)` returning the levels crossed, a per-mission cap for help bonuses. Raises `BondLevelReached(a, b, level)`. `ISavable<BondSaveData>` under a new save key; `ResetPlayModeState()` hooked in `PlayModeStaticReset`. Starting values in a small settings asset (Linda–Lucy 15; others 0 until needed).
2. **`HomeLockRules` (port)** — same file shape and names as `thj/home-test`; on `main` lists only `Sisters' Rivalry` (Linda–Lucy, Lv 2, its unlockable) and `Tempest Bloom` (Linda–Lucy, Lv 2, `_CycloneArrowScatter`). A lock now names a **node literal**.
3. **Node gate** — the Family-tree panel treats a node whose literal has a lock as locked until `BondStore.GetLevel(pair) >= lock.Level`, with "Opens at Bond Lv 2" in its tooltip. Done in the UI/panel layer (`AbilityTreePanelUI` / `UpgradeTreeButtonUI`) or a small check passed into `SkillTree.CanUpgrade`. `SkillTree` is in `StatsResourcesSystem`: if the check must live in `SkillTree`, that's a core change (BL2).
4. **Sources** — a `BondSources` listener (non-core, lives with the store):
   - Mission end: +N to every pair in the squad on a successful mission (`"Mission complete"` rewards event, or the mission-completion path; implementer confirms which is reliable).
   - Help bonus: +n when one member of a pair helps the other (Rivalry synergy, a Duo between them, a Family Role answering for the other), capped per mission.
   - Home activity: an explicit `BondStore.Add` called from a Home scene (the Yard scene).
   Values in the settings asset. Tuning (design): Linda–Lucy start ~15, earn nothing in the pair missions (they're apart), low 20s after M2, the Yard activity crosses 25.
5. **Level-up hook** — when a level is reached, queue the pair's level-up scene for the next Home visit (a `DialogNodeSequence` per pair and level, like `thj/home-test`'s `BondSceneDefinition`, kept as plain `Sequence` references on `main`).
6. **Story Family point** — a "grant N Family points" sequence step (or `BondStore` level-up reward) used by the Yard scene; it goes through the same resource path as level-up FSP so PR-8 still applies afterwards.
7. **Sister's Rivalry gated and capped** — `UnitKillAbilityPointProvider` checks the Rivalry literal through `GetUnlockableState` and replaces the 2 s real-time guard with **once per turn** (D-173 cap). Feature script, non-core. Higher caps as pips: later, not in this plan.
8. **Forced choice fallback** — if the player somehow can't choose, the Yard scene grants Rivalry directly (design: "worst case, the choice is forced").

## Questions for THJ (Tier 3)

**BL1. No combat gate in Bond Lite?** Context: the design's row says "combat gate read at level start"; on `main` the gated abilities become nodes whose literals combat already reads.
- (a) **Recommended:** gate the nodes only; no combat code reads Bond. Smallest, nothing on the AI thread. A combat gate comes with `thj/home-test`'s merge if other locks need it.
- (b) Port `HomeBondLocks` too (snapshot at level start, Duo/Pass-by checks in `UnitsCooperationHandler`/`UnitsPassByHandler`, both core). More code in core for locks that stay open on `main` anyway.
Blocked meanwhile: everything in this plan.

**BL2. Where the node lock lives.**
- (a) **Recommended:** the Home skill-tree UI asks `HomeLockRules` + `BondStore` before allowing a buy, and shows the lock. No core change; the rule lives in one non-core place, but a future non-UI buy path would skip it.
- (b) An optional "extra lock" predicate on `SkillTree.CanUpgrade` (core, `StatsResourcesSystem`). Any caller respects it; small core API change, its own commit.
Blocked meanwhile: C2.

**BL3. How the player sees Bond on `main`.**
- (a) **Recommended:** no meter in v1: the locked node's tooltip ("Opens with Linda & Lucy's Bond, Lv 2") and the Yard level-up scene. Fits "one new thing per visit".
- (b) A small Bond line in the character panel (points / next level). Easier to tune and read; one more UI to introduce before M4.
Blocked meanwhile: C3's UI part.

**BL4. Rivalry's "basic attack ready again" does nothing on `main`** (no basic-attack cooldown, GDD Q11); the +AP part works. The arc's payoff is that trigger.
- (a) **Recommended:** keep +AP only for now and drop the reset text from Rivalry's description; revisit with GDD Q11.
- (b) Replace the reset with something visible on `main` (e.g. +1 more AP, or the next basic attack costs 0 AP). A balance change; the designer proposes values.
Blocked meanwhile: C4's text only.

## Chunks

Order: riskiest first (save data and the store), then the gate, then sources, then content. One implementer run each; model opus for C1–C2.

| # | Chunk | Files (likely) | Acceptance | Tests |
|---|---|---|---|---|
| C1 | `BondStore` + settings asset + save + play-mode reset; `HomeLockRules` port | `Core/Systems/HomeSystem/Runtime/BondLite/*`, `Core/Managers/PlayModeStaticReset.cs` | Pair points saved and loaded; levels at 10/25/45; `Add` reports crossed levels; Linda–Lucy starts at 15 on a new save | EditMode: levels, pair key symmetry, save round trip, reset; **silent-lock check** (THJ, 2026-10-26): fails when an entry in `UnlockableSet.asset` is off by default and no skill-tree node literal and no run upgrade's `grantUnlockable` can unlock it (reads the assets; lists the offending ids) |
| C2 | Node gate per BL2 + lock tooltip | Home skill-tree UI (or `SkillTree.cs` if BL2 b, own commit) | Rivalry and Tempest Bloom nodes can't be bought below Bond Lv 2, can at Lv 2; other nodes unchanged | EditMode on the rule; play check of the panel |
| C3 | Sources: mission end, help bonus (capped), Home activity API; level-up queue | `BondSources`, store | Values per the settings asset; no gain for a pair not in the squad; cap respected | EditMode with fake events |
| C4 | Rivalry: literal gate + once per turn; Rivalry node in the Family tree (data); Tempest Bloom node gated | `UnitKillAbilityPointProvider.cs`, unit prefab / tree data | Rivalry off until bought; fires at most once per player turn; Tempest Bloom off until bought | EditMode for the per-turn guard if testable; play check |
| C5 | Yard scene hook: Bond add, level-up scene, story Family point, forced-choice fallback | Home sequences, a grant-FSP sequence step | After the Yard scene Linda–Lucy is Lv 2, one Family point is granted, both nodes are buyable | Play check (Home visit 3) |

## Risks

- **New statics/singletons:** `BondStore` instance → `ResetPlayModeState()` in `PlayModeStaticReset` (domain reload off).
- **AI thread:** nothing here is read by the AI under BL1 (a). Under (b), snapshot only, no Unity objects.
- **Save data:** a new save key (new format, Tier 3, covered by this plan's yes). Old saves load with an empty store → starting values applied on first read. Testing resets the save; say so in reports.
- **Serialized renames:** none planned. Changing `UnitKillAbilityPointProvider`'s private `_gainSafetyInterval` (not serialized) is safe.
- **Assets/prefabs:** the Rivalry node and the Tempest Bloom gate are tree data on unit prefabs: small YAML edits or the editor; the reviewer checks the diff for scene/prefab noise.
- **AIRegressionTest:** Rivalry becoming locked changes what the sisters get in levels that use it; the test stays known red, not re-baselined.
- **Merge with `thj/home-test`:** same names (`HomeLockRules`, `PairKey`, thresholds); the store is standalone so `thj/home-test`'s `HomeState` absorbs it. Note in `branches.md` once built. Avoid the `HomeState` name on `main`.
- **Core touches:** only if BL1 (b) or BL2 (b). Otherwise `PlayModeStaticReset` (one line) is the only shared file.

## Gates

Compile clean / EditMode (known red only) / review per chunk (opus) / THJ play check of Home visit 3 and the first Rivalry in M4 before the content commits / docs: GDD `family-systems.md` (Rivalry gate, cap, Bond on `main`), `progression-economy.md` (story Family point), `glossary.md` (Bond, if the term surfaces), `tech/home-system.md` (Bond Lite), `tech/core-systems.md` (only if a core API changed), `branches.md` (merge note).
