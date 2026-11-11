# The sisters' Bond nodes: Bloom open, the Duo as the node (D-519, D-520)

Size: M    Tier: 3 (Duos and Synergies; core Duo code)    Assigned to: miso-game-designer
Branch: `thj/after-hearth`, scope **all**. The changes are shared data (`UnlockableSet`, `Unit_Lucy.prefab`) plus the Bond Lite lock list. They reach every branch that merges them. `thj/home-test` gets them only when it takes `main`, and then its own Bond rules (Linda–Toba at L2, D-010) need reconciling.
Status: waiting on THJ (Q1 to Q3)

## Why

THJ decided at the Trail balance round ([`2026-11-11-trail-balance-design.md`](2026-11-11-trail-balance-design.md) Q4) that Tempest Bloom is open everywhere (D-519). The Linda–Lucy Duo becomes a Family-tree node shut until the sisters' Bond Lv 2, next to Sister's Rivalry. Both open at Lv 2 and there is no exclusive pick (D-520). This note checks what that breaks, what happens to the Marks-Sisters upgrade node, and the costs.

## Goal

The Yard's Bond Lv 2 opens two sister nodes, **the Duo** and **Rivalry**. Bloom is simply part of the sisters' kit. No level or tutorial loses something it relies on.

## Acceptance criteria

- [ ] Before the Yard, the Linda–Lucy Duo is never offered in any level, and its node shows "Opens with Linda & Lucy's Bond, Lv 2".
- [ ] After the Yard, the player can buy the Duo node (1 FSP) and/or Rivalry (1 FSP). The Duo upgrade opens only once the Duo is bought.
- [ ] Bloom splits Linda's arrow through the Cyclone on a fresh save, with no purchase, in every level where both sisters fight.
- [ ] The Tempest Bloom run upgrade is never offered as a dead pick.
- [ ] Family nodes still cost 16 FSP in all (PR-8 on Bond Lite).

## Evidence: what I read in the data (verified unless marked)

| Fact | Where |
| --- | --- |
| Lucy's tree: `[6]` Tempest Bloom (UnlockableLiteral `_CycloneArrowScatter`, row 0 col 0); `[7]` Marks-Sisters (StatAttribute `Stat_DMG` on `Linda_Lucy_Duo_Ability`, 2 pips, row 0 col 1, guid `b7089a3f…`); `[8]` Sister's Rivalry (UnlockableLiteral `_SistersRivalry`, row 2 col 0). All three are `familyAbility` | `Unit_Lucy.prefab` skillTree overrides |
| Marks-Sisters pips: ×1.2, ×1.35 at 1 FSP each. Level 3 (×1.5, 1 FSP) is above the node cap and is reached only by the run upgrade `RU_SistersBondDuoDamage` | `Linda_Lucy_Duo_Ability.asset` statAttributes; node `upgradeLevels 2` |
| `CycloneArrowScatter` and `SistersRivalry` cost 1 FSP each and have `unlockedByDefault 0`. `MarkLindaSynergy` (Catch & Return) has `unlockedByDefault 1`, which is the precedent for "open, no purchase" | `Resources/Unlockables/UnlockableSet.asset` |
| Bond locks: Rivalry and Bloom by unlockable id; Marks-Sisters by node guid | `HomeLockRules.cs` |
| The Duo trigger has `lockedByDefault 0`. It is carried by `Unit_Linda`, `Unit_Lucy` and `Unit_Mark`. A Duo is offered when every partner's `RuntimeAbility` is active; `RuntimeAbility.Available` also asks `UnitsCooperationHandler.SquadAllowsTrigger` | `UnitsCooperationHandler.cs` lines 63–72, 424–439; `RuntimeAbility.cs` line 42 |
| **No mechanism today shuts a Duo behind a purchase.** An Ability-mode node with `lockedByDefault` would unlock only the owner's copy (Lucy's), and Linda's and Mark's copies would stay shut. `upgradable 0` also means the unlock isn't saved (`RuntimeAbility.InitializePartially` registers saves only when upgradable) | `SkillTree.cs` `TryGetRuntimeAbility`; `RuntimeAbility.cs` 210–222 |
| `RU_SistersBondDuoDamage` requires the Duo ability `Available`. Once the Duo is shut through `SquadAllowsTrigger`, the altar stops offering it by itself | `RunUpgradeTracker.HasRequiredAbility` |
| `RU_LindaLucyCycloneSpreadUnlock` (Bloom) is blocked only by "already granted this run", not by the permanent unlock. Once Bloom is open by default, an altar could offer it as a dead pick | `RunUpgradeTracker.GetBlockReason`; `RunUpgradeAltar.BuildPool` (`Resources.LoadAll`) |
| The Family panel draws dependency lines between family nodes | `AbilityTreePanelUI.ShowFamilyAbilityBars` |

## 1. Where the sisters' Duo is used or taught today

Who fights where (placed heroes, read from the level prefabs):

| Level | Heroes | Sisters' Duo today | Bloom today | After D-519/D-520 |
| --- | --- | --- | --- | --- |
| Memory 1 (`GB_m1-linda`) | Linda | — | — | No change |
| Memory 2 (`GB_m2-lucy`) | Lucy | — | — (no Linda) | **No change:** Bloom needs Linda |
| Memory 3 (`GB_m3-john`) | Lucy, Linda, John | Locked (`LevelAbilityLock`: all three Duos) | Shut (no node) | Duo: still locked (doubly). **Bloom: new**, if Lucy casts the Cyclone (assumed available; only Memory 2 locks it) |
| Memory 4 (`GB_m4-mark`) | All four | Locked (every Duo except Mark–Lucy) | Granted for the mission (`LevelStartRunUpgradeGrant`), shot by a sequence | Duo: no change. Bloom grant redundant |
| The River (`GB_s1-river`) | Lucy, John | — | — (no Linda) | **No change** |
| The Ridge (`GB_s2-ridge`) | Linda, Mark | — | — (no Lucy) | **No change** |
| The Trail, all four `GB_m2-*` | Linda, Lucy + free pick | Locked in all four (D-470) | Shut | Duo: locked by Bond **and** by level. **Bloom: new** |
| The Yard | — | Bond Lv 2 opens Rivalry, Bloom, Marks-Sisters | — | Opens **the Duo** and **Rivalry** |
| M4 Into the Rootwell (classic levels) | Lucy, Linda + John or Mark (+ Toba) | Open (the planned first real Duo, D-470; its framed beat isn't built) | Shut unless bought | Duo only if bought at the Yard. Bloom open |
| Classic `LevelLucyJohn-C3`, `LevelMarkIntro-C1/C3` | Carry the Duo preset | Open | — | Cut missions (D-169), maps only: no action |

The River and Memory 2 gain nothing: neither has both sisters.

**Nothing loses something it relies on.** No tutorial page or level teaches the sisters' Duo before M4. The only place it was meant to appear first is M4 (D-470), and the Yard now makes that appearance conditional on the player buying the Duo. The first-hour design already planned for this: the framed first trigger plays for whichever node was picked ([first-hour design](onboarding/2026-10-25-onboarding-first-hour-design.md) rows 12 and 122–126).

**Per-mission grants: drop, don't add.** No level needs the sisters' Duo before the Yard, so no grant is needed. Keep the existing `LevelAbilityLock` entries (Memories 3 and 4, all four Trail levels). They are redundant on a first run (Linda–Lucy sit at 15 to 23, under 25, BO-1/BO-2), but they still matter on a **replay** after the Yard (MI-2): they keep the Trail's ending and the memories as authored. Drop Memory 4's Bloom grant, and with it the Bloom run upgrade (Q3).

## 2. The Marks-Sisters upgrade node

Options:

| | A. Second step after the Duo (recommended) | B. Fold into one node | C. Drop it |
| --- | --- | --- | --- |
| Player sees | Duo card → line → upgrade card; Rivalry card | One "Marks-Sisters" card: pip 1 opens the Duo, pips 2–3 add damage; Rivalry card | Duo card, Rivalry card |
| Rule in a sentence | "Buy the Duo, then you can make it hit harder." | "The first point opens the Duo, more points make it stronger." | "Buy the Duo." |
| Precedent | The character trees' template: Signature unlock A, then Signature+ C, which needs A ([`player-skill-trees.md`](../design/player-skill-trees.md)) | None: no node mixes an unlock pip with stat pips | — |
| Build | Data: an edge from the Duo node to `[7]`; the panel already draws family edges | A new node mode in `SkillTree.cs` (core: unlock pip + stat pips) | Data |
| Economy | Unchanged (16 FSP) | Unchanged | 14 FSP of nodes against 16 earned: 2 dead points |
| Risk | D-441's misread: an upgrade card next to the Duo read as "the Duo is shut". The edge and a distinct name answer it | Lowest misread; core code for one node | Sisters' Duo is the only Duo without an upgrade node |
| USP | Duos + | Duos + | Duos − (asymmetry) |

**Recommend A, Tier 3.** It follows the pattern the trees already teach, costs no code beyond the Duo gate (Q2), and keeps the economy whole. The card count stays at three, because Bloom's card leaves. B is the fallback if THJ wants fewer cards and accepts a core `SkillTree` change.

Starting data for A (the implementer checks the details in the tech plan):
- **Repurpose node `[6]`** (Bloom's slot, row 0 col 0) as the Duo node: UnlockableLiteral pointing to a new unlockable for the Duo (placeholder id `SistersDuo`, 1 FSP, `unlockedByDefault 0`), title "Marks-Sisters", the description now on `[7]` ("Lucy and Linda combine their ranged skills into one powerful coordinated shot."). Lock it in `HomeLockRules` by unlockable id, at Linda–Lucy Lv 2.
- **Node `[7]`** stays the damage node: 2 pips, ×1.2 / ×1.35, 1 FSP each. Add an edge `[6]` → `[7]` and give it a distinct name (narrative; placeholder "Marks-Sisters: Fire Arrow"). Keep its Bond lock line too, so before the Yard every sister card shows the same single reason.
- **Node `[8]` Rivalry:** no change.

## 3. What Bloom open by default changes

- **Gains it:** Memory 3 (Lucy and Linda with John), the Trail's four levels, M4, and every later level with both sisters. Not Memory 2, the River or the Ridge (see the table).
- **Memory 3** (tutorial tier, four Claws): Bloom becomes an extra way to clear, and John's lesson is still the way to win. Play check, not a break.
- **Memory 4:** unchanged. The grant just becomes redundant, and the scripted shot still plays.
- **The Trail:** this is what the balance plan's Q4 wanted, now without a grant. Per that plan's numbers, a copy deals 6 and three copies spread, but no copy kills a Standard Claw on its own; a copy plus the follow-up or a Duo slot does. The Cyclone stopgap at 3 (D-518) now has a payoff through Linda, so the Cyclone is weaker alone and strong with her sister, which is the round's thesis. The balance plan's signal stands: "no Cyclone kill of a Claw above 3 HP; kills through Bloom don't count". **Remove "Bloom granted for M2" from the Trail tech plan's C4.**
- **The Pile's ending (D-470):** a Bloom kill counts +1 for each sister in the tally (MI-28). That can't make the last kill a Duo, so the "back to back, tally alone" ending still stands. Watch it in play.
- **M4, once the Duo is bought:** the Duo arrow also splits through the Cyclone (the Synergy table: "the Linda–Lucy Duo arrow enters Lucy's Cyclone"). Three copies at 12 × mash is the sisters' ceiling. That ceiling existed before (both were Lv 2 nodes), only its timing is new. Watch M4 for a one-shot that settles a fight.
- **The data change:** `CycloneArrowScatter` `unlockedByDefault 1`, then remove node `[6]`'s Bloom role (repurposed above). This reverses the Bond Lite tech plan's "don't flip `unlockedByDefault`" note (written before D-519). `SilentUnlockableLockTests` should then pass, since the unlockable no longer needs a node.

## 4. The Yard's Bond Lv 2 reveal: text that names the nodes

Nothing in the build names the three nodes. Read from the wiring:

| Text | File | Change? |
| --- | --- | --- |
| Y12 scene: "…You pin it, I burn it?" / "…That's faster." | `Features/Onboarding/Editor/HomeVisitsWiring.cs` (`EnsureYardScene`) → `Resources/Sequences/HomeVisits/Yard_Midnight_DialogNodeSequence.asset` | **No.** "Pin it, burn it" reads as the fire-arrow Duo and "faster" as Rivalry, so it now sets up both nodes better than before |
| "Linda & Lucy's Bond reached Lv 2." / Margaret's line | `HomeVisitsWiring.Yard.cs` → `Yard_BondReached_DialogNodeSequence.asset` | No |
| "Then we train together. The Family Skill Tree has room for the two of us now." | `HomeVisitsWiring.cs` (`EnsureYardPointer`) → `Yard_FamilyTreePointer_DialogNodeSequence.asset` | No |
| Lock line "Opens with Linda & Lucy's Bond, Lv 2" | `BondNodeGate.LockLine` (generated from `HomeLockRules`) | No (generated) |
| Node titles and descriptions: `[6]` "Tempest Bloom / [Synergy] Hitting Lucy's cyclone…", `[7]` "Marks-Sisters / Lucy and Linda combine…", "Each upgrade increases the duo's damage." | `Unit_Lucy.prefab` skillTree overrides | **Yes:** `[6]` becomes the Duo node (title, description), and `[7]` needs a new title and a one-line description. **miso-narrative** writes these two strings; nothing else |
| `Tutorial_LucyLindaKillAP` (Rivalry page), `Tutorial_Duo_Abilities` | `Resources/Tutorials/` | No change for this task. (`Tutorial_Duo_Abilities` still says Duos cost "1 AP", out of date since D-219: a separate fix) |
| Planned, not built: the "Remember that shot?" callback on buying Bloom | First-hour design, line 77 | **Drop:** Bloom is never bought. If the framed first-trigger beat is built, Bloom's first real trigger is on the Trail (memory uses don't count) |

## 5. FSP costs

Keep them. Duo node **1 FSP** (the same as every unlock node: Bloom was 1, Rivalry 1, Catch & Return 1). Rivalry **1 FSP**. Duo upgrade **2 × 1 FSP**. The sisters' total stays 4 FSP (Bloom 1 → Duo 1), and the family nodes stay at 16 FSP against 15 earned + 1 from the Yard (PR-8).

**Lever:** if play shows the Duo is an automatic pick at the Yard and Rivalry never gets bought first, don't raise the Duo's price. Check FTP first: the Duo costs 2 FTP a use, Rivalry is free. Most players will hold 1 FSP at the Yard, perhaps 2 (to check: SP spent by then), so the choice is real without being exclusive.

## Lens notes

- **Creative.** *Target:* the Trail is the last time the sisters fight apart; the Yard is where they decide to fight together, and the player turns that decision into the first point they spend on the family. *The moment:* after "…That's faster.", the Family tab shows two lit sister cards and one point. Whichever the player picks fires for real in M4. The Duo changes from "locked by the level" (D-470) to **earned through Bond**, which is a better reason for the Pile's sad ending: they haven't trained together yet. Bloom stays something they already do without thinking; it was never a story beat after Memory 4.
- **Systems.** Rules: the Duo is a family node (1 FSP, Bond Lv 2); its upgrade needs it; Bloom is always on. Interactions: run upgrades (Sisters' Bond hides itself; the Bloom run upgrade has to go), `LevelAbilityLock` (kept for replays), the tally (Bloom kills count, as built), Bond help (unchanged: Bloom isn't a help Synergy in `BondSettings`). Failure cases: a dead altar pick (Q3); the Duo unlocked on Lucy only (Q2 avoids it); old saves that spent 1 FSP on Bloom keep the literal and lose the point (test saves only: reset them, no refund code).
- **UX.** Before the Yard: three grey sister cards, each with the one Bond line. After: Duo and Rivalry lit, the upgrade grey with a line from the Duo. The likeliest misread is D-441 again (the upgrade card taken for the Duo), which the edge and a distinct name answer. Bloom is learned from its aim preview (CR-56), which needs no card. **New on screen: nothing.** Bloom's card goes, the Duo card takes its slot, and one line is added between two existing cards.
- **Where the lenses disagree:** the creative lens likes a single fused card (B), which avoids D-441 completely. The systems lens prefers A (no core change, the trees' own pattern). I lean A, and keep B as THJ's alternative in Q1.

## USP check

- **Duos:** strengthened. The sisters' Duo is earned at the Bond moment and gets its first real use in M4.
- **Synergies:** strengthened. Bloom is always available, and it is the Cyclone's payoff now that the Cyclone deals 3.
- **Family Roles:** neutral.
- **Managing the Home as a Family:** strengthened. The Yard's point buys a real choice between the sisters' two ways of fighting together.

## Questions for THJ

**Q1. The Marks-Sisters upgrade node: second step, fused, or gone?**
- Context: the Duo itself is now the node (D-520), and today's Marks-Sisters node only raises the Duo's damage (2 pips).
- Options: (a) a second node after the Duo, joined by a line (data only, the trees' A→C pattern); (b) fuse them into one card where the first pip opens the Duo (core `SkillTree` change); (c) drop it (leaves 2 FSP with nothing to buy).
- Recommendation: **(a)**, with a new name for the upgrade from miso-narrative.
- Blocked: the tree data, the `HomeLockRules` list and its tests.

**Q2. How the Duo is shut: a change to core Duo code.**
- Context: nothing in the game can shut a Duo behind a purchase. The Duo's ability is carried by Linda, Lucy and Mark, so unlocking "the ability" in a node would open only Lucy's copy. `UnitsCooperationHandler` is a core system (`tech/core-systems.md`).
- Options: (a) each Duo entry may name an unlockable it needs, and `SquadAllowsTrigger` refuses the Duo until that unlockable is owned (one generic field, off for every other Duo; the ability bar and the Sisters' Bond run upgrade follow by themselves); (b) Ability-mode node with `lockedByDefault` on the trigger, plus syncing the three copies and making them saved; (c) only per-level locks (no node, contradicts D-520).
- Recommendation: **(a)**. The coordinator's tech plan sets the exact shape.
- Blocked: the whole Duo node.

**Q3. Retire the Tempest Bloom run upgrade and Memory 4's grant?**
- Context: with Bloom open, the grant does nothing, and an altar could offer the run upgrade as a dead pick (its check ignores the permanent unlock).
- Options: (a) remove the grant from the Memory 4 wiring and take `RU_LindaLucyCycloneSpreadUnlock` (and its `RUP_` pickup) out of the pool (delete, or move out of `Resources`); (b) leave both (a possible dead pick); (c) keep the run upgrade and make the altar skip upgrades whose literal is already owned (a small core change, useful for later cases).
- Recommendation: **(a)**. Deleting assets is Tier 3, hence the question.
- Blocked: nothing else. It can follow the Duo node.

## Docs to update if approved

| Doc | What | Owner |
| --- | --- | --- |
| `design/gdd/family-systems.md` | **BO-4** (Lv 2 opens the Duo node and Rivalry; the Duo upgrade needs the Duo; amends D-424, D-441); BO-3 ("points at the sisters' nodes", unchanged wording); Duo table row Linda–Lucy (Unlock: family node, 1 FSP, Bond Lv 2 on Bond Lite); Tempest Bloom row (Unlock: open by default; no node; run upgrade retired if Q3 a); Branch differences | miso-game-designer |
| `design/gdd/progression-economy.md` | **PR-8** (the three shut nodes become the Duo, its upgrade and Rivalry; total still 16); Unlocks table (Bloom row: open, no cost; new Duo row); Lucy's run-upgrade list (line 133, Bloom gone if Q3 a); Source lines | miso-game-designer |
| `design/gdd/characters/lucy.md` | Family nodes line 54; run upgrades table (line 78); Synergies row; Q2 names (add the upgrade's name) | miso-game-designer |
| `design/gdd/characters/linda.md` | Synergies row (Bloom always on) | miso-game-designer |
| `design/gdd/missions-structure.md` | MI-30 (Memory 4's Bloom grant gone, if Q3 a) | miso-game-designer |
| `design/player-skill-trees.md` | Family tree table (Lucy: Duo node, Duo upgrade; Bloom gone); rule line 8 ("Duos and synergies stay unlocked by default…" now except the sisters' Duo) | miso-game-designer |
| `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` | Rows 12, 107, 122–126 (the choice is Duo or Rivalry); line 77 callback dropped | miso-game-designer |
| `plans/onboarding/2026-10-26-bond-lite-tech.md` | Note: superseded on Bloom (`unlockedByDefault` now flipped) and the lock list | coordinator |
| `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` | C4: drop the M2 Bloom grant | coordinator |
| `plans/2026-11-11-trail-balance-design.md` | Q4 answered by D-519 (no grant) | miso-game-designer |
| `glossary.md` | The upgrade node's name; "Marks-Sisters" now names the Duo node | miso-narrative |
| `decisions.md`, `status.md` | The answers to Q1–Q3 | coordinator |

Tests the implementer will touch (for the tech plan): `HomeLockRulesTests`, `BondNodeGateTests`, `SistersRivalryTests` (lines 101–102 use the Bloom literal), `HearthMemoryMarkTests` (grant), `SilentUnlockableLockTests`, and possibly `AIRegressionTest` (it names the Duo; the baseline is known red).

## Risks

- **Core change (Q2):** small and off by default, in its own commit.
- **Old saves:** a save that bought Bloom lost a point. Reset test saves; no refund code.
- **M4 is untested with the Duo bought or not bought:** play check from the Yard into M4, both picks.

## Gates

Compile / EditMode tests / review / play check (yes: the Yard → Family tab → M4, once per pick; one Trail run for Bloom) / docs above.

## Playtest signal

- **Worked:** at the Yard, THJ reads the two lit cards without help and spends the point. The bought node fires in M4. On the Trail, at least one Bloom shot lands and no Cyclone alone kills a full Claw.
- **Failed:** the upgrade card is taken for the Duo (rename it, or Q1 b); Bloom never fires on the Trail because the Cyclone is never placed in Linda's lane (a layout question, not a node question); the M4 Duo-through-Cyclone combo settles a fight in one action (tune the copy damage, later).
