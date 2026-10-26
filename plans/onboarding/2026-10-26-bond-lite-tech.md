# Bond Lite (pair Bond on `main`) — tech plan

Size: L    Tier: 3 (new reusable system; Home; save data; THJ's yes before any code, D-179)    Assigned to: `miso-implementer` (opus) → `miso-reviewer` → `miso-verifier`
Branch: all (built on `thj/onboarding`; must fold into `thj/home-test` on merge)
Status: **approved (D-233)**; built after the greybox and the pacing check (D-180). Answers: BL1 nodes only (D-202), BL2 lock in the Home skill-tree UI (D-203), BL3 tooltip + Yard scene, no meter (D-231), BL4 +AP only now, the reset becomes D-220's AP refund once its amounts are set (D-232). C1 adds the silent-lock test (THJ)

Design: `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` ("New tech", "The Sister's Rivalry arc"). Work plan step A4(a), build step B7. Decisions: D-173 (Rivalry to the Family tree, Bond gates the pair's nodes, Yard grants the first Family point), D-179 (go to a tech plan), D-180 (built after the greybox and the pacing check).

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
