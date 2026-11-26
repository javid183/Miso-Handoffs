# M2 The River, round 2: THJ's play-check fixes and the corridor ambush

Size: M    Tier: 2 (THJ approved the Tier 3 points: core fix D-729, layout and ambush D-728, horn D-730, Shelter D-731, potion D-732)    Assigned to: `miso-implementer` (opus), two chunks, one at a time
Branch: all (on `main`)
Status: approved (THJ's answers 2026-11-26); R1 dispatched

## Why

THJ played chunk 3.2 (`reports/onboarding-3-2-m2-river.md`, still uncommitted) and gave seven notes: `playtests/2026-11-26-m2-play-check.md`. Code trace (Explore, 2026-11-26) answered in this plan's Facts.

## Goal

Lucy's follow-up hits a split worm's child; M2 plays THJ's tweaked layout with the rush (Lucy runs to 7,2), the Shelter page, a locked John–Lucy Duo, and a horn ambush after the ring, with a health potion whose tutorial plays once across M1 and M2.

## Acceptance criteria

- [ ] **R1:** after any family hit that splits a Dark Worm, Lucy's follow-up fires on the child standing on the hit worm's tile (both timings: split during the prompt, and split before her role is checked). Other roles unchanged.
- [ ] `GB_m2-river` keeps THJ's tweak (tiles, corridors, the deleted column); nothing rebuilds it from the old block.
- [ ] The John–Lucy Duo is hidden in M2 (Cleanse lock kept).
- [ ] Level start: after Lucy's Family Role page, a "Sheltered by John" page explains Papa's Shelter (next to John, one extra ember). Lucy starts Sheltered (0,2 next to John 1,2).
- [ ] Rush: John walks to 9,2, the ring appears, **Lucy runs to 7,2** (embers reach John, 2), then the turn reset, the lines, Shield Up, and the Fire Embers hint pulses as soon as input returns.
- [ ] Stage 2 "Help John." completes when the **four ring Claws** are dead (the Archer on 12,2 does not count).
- [ ] Then the ambush: the Archer (if alive) walks out through the north-east corridor and leaves the board (no death, no XP); a horn sound (stand-in) and a dialogue line "Horn Sounding" (placeholder); four hidden Archers appear at the corridor ends 6,7 · 15,7 · 6,-3 · 15,-3 and run to 8,4 · 13,4 · 8,0 · 13,0 (mirror of THJ's 15,-3 → 13,0); a wave appears in the middle: Dark Worm 10,2, Dark Claws 11,3 and 11,1 at ×0.45 (taken tiles: nearest free); stage 3 "Clear the river." (defeat all).
- [ ] M2's mission starts with one Health Potion. Right after the ambush starts, the health-potion page and the pouch hint play, **once per save across M1 and M2**: whichever level shows it first, the other skips it. M1's ambush uses the same shared page.
- [ ] The Pile ending is unchanged (camera, clue lines, outro, drops).
- [ ] The five ring units and every new hidden unit are saved inactive (they are active in the prefab today).
- [ ] Covering tests per chunk; full EditMode suite green after each chunk.

## Scope

In: R1 Lucy's follow-up retarget; R2 M2 wiring on THJ's prefab, the shared potion page in M1 and M2.
Out: a real horn clip (THJ later), final text (`miso-narrative`), X-38 pouch work, a fourth worm size (D-727), any other role.

## Facts (Explore 2026-11-26; verify before relying)

- **Worm split** (`Core/Entities/Runtime/DarkWormPassiveAbility.cs`): a lethal hit leaves the worm at min+1, then one frame + Die anim + 0.8 s, then `Split()` (:351-389) kills the parent (`DiePermanently`, `IsAlive` false at once) and spawns child 1 on the parent's tile, child 2 on the nearest free tile (`unitBorn` raised via `RegisterUnit`). Not core.
- **Lucy's follow-up** (`Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs:62-114`, core per `tech/core-systems.md:18`): candidates are living enemies whose HP dropped against a snapshot taken when the partner's action started (:155-183); the target is stored as a unit (`Targets = { target }`, :112). Case (a): parent picked, splits during the 1 s prompt, `KeepLivingTargets` (`FactionRoleHandlerBase.cs:163-167`) drops it, role skipped as `TargetsGone`. Case (b): split first, children have no snapshot, never candidates.
- **Duo lock:** `LevelAbilityLock` on the CombatLevel; M2 already has one (Cleanse, written by `MissionWiringWhiteMothers.LockCleanse`). Add `Resources/Abilities/Cooperation/John_Lucy/Trigger/John_Lucy_Duo_Ability.asset` to John's and Lucy's entries with a merge, not `SearchWiring.Trail.LockSistersDuo` (it overwrites the list).
- **Papa's Shelter:** `LucyPassiveAbility_PapasShelter.cs`; status "Sheltered by John" ("Lucy gains an extra orb to fire."), panel "Papa's Shelter" ("Lucy fires an extra orb with her basic attack while standing next to John."). No tutorial page exists.
- **Potion:** M1 sets `Mission.initialItemsAvailability = [{Bergsons_Ability_HealthPotion, 1}]` (`MissionWiring.Ridge.Layout.cs:329-344`); its page `M1Ridge_Ambush_PotionPage` (`M1Ridge_Potion_Panels`) and `M1Ridge_Ambush_PouchHint` signal sit nested in the ambush sequence (`MissionWiring.Ridge.Sequences.cs:264-283`, text :359-362), so `PlayJustOnce` can't work there.
- **Once per save:** `PlayedSequencesTracker` keys by asset **name**, checked only for top-level plays in `SequencePlayer.Play` (nested steps ignore `PlayJustOnce`). Existing shared pattern: `Search_FirstSleepingEnemy` (`SearchWiring.Shared.cs:58-75`), one asset played through a `SequencePlayHandle` in several levels.
- **Event pieces:** `MoveUnitSequence` (nickname or `findUnitByTile`); `HideUnitsSequence` (`Features/Onboarding/HideUnitsSequence.cs`) takes a `HiddenLevelUnits` group's in-play units off the board (no death event, no XP, no objective count); `AudioSequence` (`Core/Levels/Runtime/AudioSequence.cs`); `RevealUnitsSequence` works mid-level and reveals come in alert. **No horn clip exists.** `HoldUnitsUntilSignal`/`Status.Inactive` does **not** stop enemies (AI skips only Stunned/Unaware), so the corridor Archers are hidden, not held.
- `HiddenLevelUnits.Awake` turns listed active units off with a warning, but the intended saved state is inactive (`M2RiverTests` asserts it).

## Approach

### R1: Lucy's follow-up retargets to a split worm's child (core: Family Roles) — opus, own review, own commit

Only `LucyFactionRoleHandler.cs` (plus tests). No change to `FactionRoleHandlerBase.cs` or `PlayerController.cs`; if the fix needs either, stop and report (Tier 3).
1. Case (a): when the target is chosen, remember its tile. While the role is pending, listen to `unitBorn` (unsubscribe on fire, skip, abort, disable); if the stored target is dead and a hostile unit is born on that tile, it becomes the target.
2. Case (b): store each snapshotted enemy's tile; in `PrepareTargets`, an enemy with no snapshot entry standing on the tile of a snapshotted enemy that is now dead inherits that entry (counts as hit).
3. Tests (EditMode, the existing Lucy role fixtures): both cases with a worm; a plain kill (no child) still skips; non-worm targets unchanged. Then the Lucy/role fixtures and the full suite.

### R2: M2 round 2 wiring + the shared potion page — opus, reviewed with the feature

**Work on THJ's prefab.** Don't run the River "Build Level" step from the block (it would overwrite his tweak); the wiring adds and edits units on the existing prefab, idempotently. Update the paper block in the D3 plan to match after (coordinator).
1. **Units:** re-save the five `ring` units inactive. Put the Archer on 12,2 in its own hidden group `runner` (revealed with the ring) so `HideUnitsSequence` can take it out; or keep it in `ring` if HideUnits only touches units in play: report which. New hidden group `ambush`: Archer Goblins on 6,7 · 15,7 · 6,-3 · 15,-3 (THJ's four, moved into the group, inactive). New hidden group `wave`: Dark Worm 10,2 (no HP override), Dark Claws 11,3 and 11,1 ×0.45.
2. **Locks:** merge the John–Lucy Duo into the level's `LevelAbilityLock` for John and Lucy, keeping Cleanse.
3. **Start:** a "Sheltered by John" `TutorialSequence` page after Lucy's Family Role page (text from the in-game panel/status; untagged, listed in the report, D-348).
4. **Rush:** John → 9,2; reveal `ring` (+ `runner`); `MoveUnitSequence` Lucy → 7,2 (if she already stands there, no move; if blocked, report the fallback used); turn reset; John/Lucy lines; Shield Up; ember hint signal (pulses when input returns). Keep the reset-before-cast order and the lines between them (review fix).
5. **Stage 2:** objective "Help John." = the four ring Claws dead.
6. **Ambush (new stage 2 → 3 sequence):** if the runner Archer is alive, `MoveUnitSequence` it out through the x = 13 corridor to 14,7, then `HideUnitsSequence`; skip both if it's dead. `AudioSequence` with a stand-in clip (closest existing sound; name it in the report) and a camera shake if one exists; dialogue line "Horn Sounding" (no speaker/narrator style as the project allows; placeholder); reveal `ambush` and move each Archer to its stop (6,7 → 8,4, 15,7 → 13,4, 6,-3 → 8,0, 15,-3 → 13,0); reveal `wave`; signal the shared potion page; objective "Clear the river."; input on.
7. **Potion:** `MS1 - The River.asset` `initialItemsAvailability` = one Health Potion (as M1). One shared page asset (e.g. `Resources/Sequences/Shared/Onboarding_HealthPotion_Page.asset`, `PlayJustOnce`, text as M1's page) played at top level through a `SequencePlayHandle`/signal in both levels, followed by the pouch hint only when the page plays. In M1, swap the nested `M1Ridge_Ambush_PotionPage` + pouch hint for the shared trigger; M1's beat order otherwise unchanged. If the tracker can't express "pouch hint only with the page", report the option used.
8. **Pile:** unchanged; check the props still sit east of the last cells (x 13 now) and the camera reaches them.
9. **Tests:** update `M2RiverTests` to THJ's layout and the new groups/stages/locks/potion; a test that the shared page is the same asset (same name) in M1 and M2 and plays once (tracker); M1's tests (`M1RidgeTests` and friends) updated for the swap; rerun test kept. Then the full suite.

## Risks

- **Core (R1):** Family Roles is core; THJ approved the change in Lucy's handler only (D-729). Event subscription must be removed on every exit (fire, skip, abort, unit death, level end). No statics expected; if one appears, `PlayModeStaticReset` hook.
- **THJ's prefab is the master now:** any builder step that rewrites the prefab from the block would lose his tweak. Wiring edits only.
- **M1 touched again** (shared potion page): M1 is committed and played; keep its other beats byte-identical, run its tests, and THJ replays M1's ambush.
- **Saved data:** none new (the tracker already saves by asset name). The shared page's asset name is the save key: never rename it after it ships.
- **Runner Archer:** may be dead, or may block a corridor stop; the sequence must skip cleanly.
- **Revealed units on taken tiles** move to the nearest free tile (wave around John on 9,2).
- **AI content:** none changed; `AIRegressionTest` not needed.
- **Text:** "Horn Sounding", the Shelter page, existing lines: placeholders for `miso-narrative`.

## Gates

Compile clean / R1: Lucy role fixtures + full suite, own review (core) / R2: M2 + M1 fixtures + full suite, review with the feature / play check: yes (THJ: M2 with a win, M1's ambush, then the other mission on the same save to confirm the potion page doesn't repeat) / docs: D3 paper block redrawn to THJ's layout (coordinator), `tech/core-systems.md` note for R1 (coordinator), GDD `enemies.md` worm text and `lucy.md` follow-up note (designer), glossary for "Sheltered by John" if new (narrative).

Commits after THJ's play check: (1) R1 core fix; (2) 3.2 commit 1 (old River rename + old tool trim); (3) 3.2 commit 2 + round 2 M2 (new level, wiring, sequences, tests); (4) M1 shared potion page.
