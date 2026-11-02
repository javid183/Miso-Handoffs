# Onboarding structure C4: The River, The Ridge, The Trail

Size: L (one risk check + three chunks)    Tier: 2 (content + editor tool; THJ: "Start C4"; any core change found → stop, Tier 3)    Assigned to: `miso-implementer` (C4-0 check, C4a, C4b, C4c) → `miso-reviewer` → THJ play check per chunk
Branch: `thj/onboarding`. Status: **approved 2026-11-01** (D-351: `level deploy` grid line; order River → Ridge → Trail). C4-0 done (`reports/onboarding-c4-0-check.md`); **C4a done**, committed `3289158db` (River level, wiring, shared sleeping-enemy panel, MS1 data; review APPROVE + fix round; EditMode 1222/1223 known red only; THJ play-checked OK); **C4b done**, committed `a7320be82` (Catch & Return open by default, D-352), `eda1d6df6` (`SleeperSightBeatSequence` in the shared panel), `51f109672` (Ridge level, wiring, MS2 data; enemy turn first D-353; gauntlet at the Claw's own HP D-354); review APPROVE + fixes; EditMode 1240/1241 known red only; THJ play-checked OK. Arrow damage has no falloff without `RU_LindaArrowDamageDecay` (catch 12 per Claw). Next: C4c; C4b starts with D-352 (Catch & Return open by default, its own commit); C4c: `level deploy` replaces a drawn hero with a warning

## Why

C3 made the Hearth playable. The search comes next. Two pair missions, MS1 The River (John + Lucy) and MS2 The Ridge (Linda + Mark), are playable in either order, then M2 The Trail (route choice → the pile). The mission assets already exist from C1 (`Content/Levels/MS1 - The River.asset`, `MS2 - The Ridge.asset`, `M2 - The Trail.asset`), but they still point at placeholder levels. C4 builds their levels from the paper blocks with the grid tool and wires the data (structure tech § C4; paper plan `plans/onboarding/2026-10-26-onboarding-levels.md` § The search, § Rigged drops, § M2 · The Trail).

## Goal

From the world map: The River and The Ridge each play their level, teach their Family Role, drop their rigged materials and play their clue. The Trail opens with a trailhead, shows the mission map with two routes, plays the chosen route, and ends at the pile.

## Acceptance criteria

C4a The River (`GB_s1-river`):
- [ ] Built from the `river` block. Tutorial tier, default alert (enemies start Unaware). Family starts 4+ from every enemy. Clearing Claws on 5,3 / 6,4 / 6,2 wake together. Archers on the islands 9,5 / 13,5 / 9,1, out of walking reach. 11,3 is safe from all three.
- [ ] Level start: camera pans to the clue on the far bank (16,3) and back. Lucy's Family Role panel. John's line "Stay by me." The clue props stand on 16,3 (placeholder), and the end sequence shows them up close.
- [ ] Win: defeat all. Mission: `collectableGResources` Gold 20 + Timber 1 + Fabric 1 (Timber and Fabric always given), `completionXPReward` 30.
- [ ] **First sleeping enemy** (levels plan §UX, Required): one shared panel ("Asleep: they act once they see you, 3 tiles, or are hit; Shift shows their sight") shown once in whichever pair mission comes first, plus the nearest sleeper's sight tiles for one beat. Same asset at the start of both River and Ridge, shown once per save if a once-only flag exists (`PlayJustOnce`, `AbilityIntroductionTracker` seen-set); the sight beat as data if possible, else report.
- [ ] Can a bark condition test "Lucy within 3" (Shield Flare discovery bark)? Answer only. Bark graphs are built by hand.

C4b The Ridge (`GB_s2-ridge`):
- [ ] Built from the `ridge` block. Tutorial, default alert. The rush pack (1,5 / 2,4 / 3,5) wakes at start by sight. Gauntlet Claws on 7,1 / 8,1, asleep, per-instance HP 8.
- [ ] Mission drops Gold 20 + Steel 2, XP 30. Clue props on 13,1, plus the end sequence.
- [ ] Checks: Vault over units; Catch & Return usable with no Family-tree node (D-177: open by default; if it isn't, stop, it's Tier 3); the returned arrow's damage.

C4c The Trail (M2):
- [ ] Trailhead (enemy-free; the exit opens the mission map) → mission map with two branches, "Follow the blood" and "Follow the tracks" → the pile. The level graph is in `M2 - The Trail.asset`.
- [ ] Roster: Lucy and Linda fixed, plus John or Mark (free pick). Each level places the two sisters and gives the pick a deploy slot (question 1).
- [ ] FTP drained to 0 at the trailhead (`LevelStartFPFiller` −99, clamped; check that a negative amount works). Health Potion 2 and Family Trinket 1 in `initialItemsAvailability`. Early tier.
- [ ] Route A: one FTP/Pass-by panel; gully Claws HP 12, side gully HP 16.
- [ ] Route B: Archers on the ledge. The Encore cue is the "both Archers dead" stage's `OnCompleteSequence`: the camera rests on the ledge, then Linda's line.
- [ ] Pile: rear wave of 2 Claws spawned on 0,6 / 0,5 at turn 2 (stage `Turn reached 2` → `GUnitSpawn`), using a starts-alert prefab variant (`EnemyAlertSettings.startsAlert`). The items panel at start. The tally lines. The end clue.
- [ ] EditMode tests for the wiring (as C3: stages, drops, graph shape, roster). Full suite: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.

## Approach

**C4-0 · opus, read-only risk check (before any building).** Answer, each with file:line:
1. Does the grid tool's default template (`LevelM1-C2`) let a pair mission's level work in MS1/MS2: rosters, placed heroes, `level fp full` not needed (FTP "starts full")?
2. Deploy slots: how a level declares them (`MissionRoster` free slots ↔ level deploy cells). Can the grid tool add them, or is it a hand edit? See question 1.
3. Mission map with two branches (MI-11): what makes the map open after the trailhead, and how branches are marked in `levelDependencyGraph`.
4. `LevelStartFPFiller` with a negative amount: does `Produce(-99)` clamp to 0, or is there a `Consume` path?
5. Catch & Return and the Vault over units on this branch.
6. Archer Goblin: range 3, at Tutorial and Early tiers. Can it shoot over water/rock gaps? Does the grid tool's `a` place it?
7. Bark conditions (`Lucy within 3`, `Linda has ≥ 1 arrow`): what exists.
Report → coordinator. A core change → stop.

**C4a · sonnet.** The River: build, wire (editor wiring partial as in C3, `Wire Search: River`), set the mission's level graph and drops, add tests.

**C4b · sonnet.** The Ridge, the same way.

**C4c · sonnet.** The Trail: five levels (trailhead, blood, tracks, pile) plus the mission graph, roster, items, FTP drain, the starts-alert Claw variant (new prefab variant beside the Claw, not an edit of the shared prefab), and tests.

Each chunk: review, THJ play check, commits (any tool or component change first, then levels + wiring + tests per level).

## Scope

In: the six levels and their wiring, the three missions' data (graph, roster, drops, items, XP), placeholder clue props, panels and lines from `plans/onboarding/onboarding-narrative-draft.md` (untagged, D-348; placeholders listed in reports).
Out:
- Home visits, Workshop unlock, skill tree (C5).
- Final art and narrative.
- Discovery barks: Shield Flare "Lucy, at me!" and Mark's "Send one my way." Bark graphs are built by hand (the bark seeder can't create Graph Toolkit nodes); C4 lists the steps.
- Framed first-trigger beats (later tech; greybox uses the QTE plus a panel).
- The timed pacing run.

## Touches

Systems: Levels/Mission (data), LevelObjectives stages, sequences (use, not change), GridToLevel tool (a `level deploy` line if question 1 says so), EnemyAlertSettings (data), Resources/drops (data). Core: none expected. `GUnit`, `FactionTracker`, `MissionRoster` or `MissionTracker` behaviour changes → stop and ask.
USPs: Family Roles (Lucy, Mark), Synergies (Shield Flare, Catch & Return), Duos (Marks-Sisters), Continuous Attack, Pass-by, items.
Docs: `tech/level-tools.md` (any new line), `tech/combat-architecture.md` (any new component), the structure tech § C4 status, `status.md`, `build-log.md`.

## Risks

- **Pair missions in either order:** each mission's drops are fixed; neither depends on the other's completion.
- **Spawns in M2:** XP is allowed outside the memory. The rear wave spawns from a starts-alert variant, so the shared Claw prefab stays unchanged.
- **Shared prefabs:** no edits to `Unit_DarkClaw` or `Unit_ArcherGoblin`; variants or per-instance overrides only.
- **Statics:** any new component holds none, or gets a `PlayModeStaticReset` hook.
- **AI content:** new levels don't change `AIRegressionTest`'s levels; it stays known red.
- **Prefab hand edits:** logged per level (a rebuild loses them); a wiring menu item re-applies the wiring.
- **Save:** testing may reset the save; reports say so.

## Questions for THJ

1. **Deploy slots for The Trail's free pick (John or Mark).** The grid tool has no way to mark one today.
   - (a) **Recommended:** a `level deploy x,y` grid line (tool + tests) that places a deploy slot instead of a hero.
   - (b) Hand-add the slot to each of the 4 Trail levels after the build (lost on a rebuild).
2. **Order:** River → Ridge → Trail, one chunk at a time, with a play check each. OK?

## Gates

Per chunk: compile clean / EditMode (only the known AI test red) / review / THJ play check (C4a the River from the world map; C4b the Ridge; C4c the Trail from the map, both routes) / commits split / docs above.
