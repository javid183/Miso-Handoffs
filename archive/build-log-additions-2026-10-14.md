# Build Log additions

New Build Log sections go here, dated, one per step (Built / Verified / Not verified / Findings / Status), oldest first. They get folded into the Build Log tab of the "Miso Home System" doc, and this file is then cleared back to this header.

Last fold: 2026-10-14 (everything through the Hungry Moon and the Oct 14 Playtest Plan update).

## Playtest: open checks, Oct 14 run (Claude, computer use)

2026-10-14, Unity 6000.3.4f1, from PreloadScreen. Sim Debug "New Cycle" (no save reset), +15 Bond John & Linda to set up the capped-Teacher case, then Day 1 → Day 5 Dusk played by hand. Two sorties: Goblin Camp (Day 2, John / Linda / Lucy), Mossy Hollow (Day 5, John / Lucy / Mark). Cheats only in combat (K, L, `]`, F12). Evidence: Editor log `[Home …]` lines, the Dining Table report and the combat logs `CombatLogs/20261014-203100_Goblin_Camp.log` and `20261014-205935_Mossy_Hollow.log`. Nothing in the project was edited. The Badge Side test changed a field in Play only.

### Verified

- **0(e) Stargaze report line.** Night lines "Stargaze: Mark, Lucy watched the sky", "Chart: Mark charted The Hound: Star Chart: The Hound is on the Study shelf", the Omen reveal, and the Overnight recap ("Stargaze: Mark watched the sky", "+1 Star Chart: The Lantern").
- **1.2 Capped Teacher.** After Toughness reached 6/6, John's Teacher tile in the Yard was greyed out (I did not read its tooltip).
- **1.7 Vigil.** On the sortie night (Lucy Wounded), Toba took the Vigil seat; "Toba tended Lucy: recovers at Dawn"; Lucy was in the Yard the next morning.
- **2.4 Little Moon arc.** It moves along its arc from Morning to Night and parks at Night. The arc is small; THJ to judge the look.
- **3.1 Glance test.** From the overview, every badge matched its window: Workshop "Working / Ready in 2 Dawns", Kitchen "Blocked / Pantry full", Study "Needs input / Desk empty", Care "Blocked / No one is Wounded", Porch "Idle".
- **3.2 Badge Side.** On `Prop - homestead`, Top and Left move the badge as expected.
- **3.8 Lapse effects.** During a lapse, `Fx Workshop` and `Fx Study` particles spawn at their props (yellow sparks, pages). They are small and hard to see from the overview.
- **4.2 No wandering.** Unseated characters stay at their spots through the slots (`spot-Lucy`, `spot-Toba`, `spot-Kevin`, porch pair). No wandering in any idle log line.
- **4.6 Send-off (partly).** The squad gathers at the Door with a bark and `JohnGate` plays when John goes.
- **5.1 Headline cards.** The Kitchen discovery card ("A new recipe", Mary), the mission-reveal card ("A new mission", John: Drowned Shrine), Thread-cut and Bond cards all show, one at a time, before the Dining Table. A Play restart at Night did not replay them. Cards not yet dismissed do show again after a restart at Dusk, which is expected.
- **5.2 Traces (placeholders).** Four pantry squares match Pantry 4/4, a green square appears in the planted plot, and a white square sits on the desk while Mark reads.
- **6.3 Shield Dash below Lv 2.** John–Mark at Lv 1: Mark's Command moved John and no Shield Dash followed (combat log: Command → John, moved, nothing after).
- **0(n), partly.** Panel text: Sidewinders "Each upgrade adds 1 sidewinder"; Kindled Spirits "+10% critical chance while Lucy is in the squad"; Marks-Sisters, Hide and Seek and Healing Marks pages read right. Buying works: Sidewinders 1, Father's Resolve (unlocks C, as the A→C edge should), Hide and Seek 1 with the earned Family SP. Healing Marks shows 1 from the free Bond Lv 2 grant. Purchases survive a Play restart (SP count 3 = 2 left + Lucy's level-up; Father's Resolve still unlocked). Lucy's locked Blink is not in her hotbar. Hide and Seek at level 0 makes 2 decoys (Goblin Camp log), which matches the spec.

### Not verified (still open)

- 0(j) Main's idles inside the camera boundary; 3.3 diamond hover outline; Kevin's side-view walk; the weapon on Ben's rack (5.2).
- 1.2 lone stargazer with nothing to chart (see finding 6: Night 1 can't test it).
- 4.4 bark pace: judged only from the log (findings 8 and 9).
- 0(m) FP gain VFX: L (+99 FP) on Lucy showed no HUD VFX in four frames, but the bar may have been full. See finding 10.
- 0(n) combat effect per node. I could not get Lucy's Fire Embers to fire by clicking in Mossy Hollow, so I measured no Sidewinders, Hide and Seek 3 or Father's Resolve effect. The combat log can do this check (sidewinder and decoy lines per cast); it needs a hand-played fight.
- Part B (needs a new player).

### Findings

1. **Major: Dawn-tick report lines are lost on sortie days.** After the combat scene reloads Home, `CurrentReport` starts empty. Day 2's Dining Table and log go straight from `=== Home day 2 ===` to `[Sortie]`, with no harvest, hens, moon or Workshop lines. Both weapon deliveries fell on sortie days (Ancestral Sword Lv 2, Day 2; Crescent Bow Lv 2, Day 5). Neither "Uncle Ben finished …" line nor the "A weapon is ready" card appeared, although the Overnight recap said "Crescent Bow delivered". Likely cause: `HomeDayReport` is not saved, and the reload builds a new one. The same probably hides other Dawn-tick headlines (Upgrade).
2. **Major: The Kitchen forecast ignores the morning batch.** On Day 3 the Kitchen badge and window said "Mary cooks Gourd Omelette in the afternoon" (pantry 2/4). Kevin's morning batch of Hearty Stew made 2 and filled the pantry. The result was "Mary didn't cook: the pantry is full", so the forecast and the recap disagree (1.4).
3. **Minor: A recipe learned in the Study gets no headline card.** "Star Chart: The Lantern: Learned recipe: Quickberry Tart / Hunter's Skewer" appears only in the Dining Table text. `UnlockRecipeOutcome` reports without setting `headline = Recipe`, while `RevealMissionOutcome` sets its headline.
4. **Minor: The Great Moon can't turn red.** `HomeSkyDecay.GreatTint` multiplies the sprite by (1, 1−0.45d, 1−0.55d). The art is cyan (low red), so the result is only a darker teal. Confirmed on Day 5 (2.4). A lerp toward a red target would work.
5. **Minor: The camera does not frame the overview at Night (3.6).** Reproduced on 3 of 3 nights: "Go into the night" frames the roof / Stargaze side, not the overview. If that is intended for night, the plan's rule needs updating.
6. **Minor: The lore-only Great Moon counts as chartable.** On Night 1 a lone Mark is allowed and offered "Chart The Great Moon". The result is lore only ("Mark watched The Great Moon"), and a second watcher is not marked "Bond only". `HomeSeatRules.Stargaze` uses `CanChart`, which does not exclude patterns with no `chartItem`.
7. **Minor: The Care badge showed Kevin's refusal.** On Day 4 the Care badge read "Blocked / No one is Wounded / Kevin only helps with the chores (Homestead or Kitchen, by day)".
8. **Minor: Hidden avatars can't bark, so the wrong person speaks.** While John's `JohnSword` idle hides his avatar, "assign:Yard(John)" was spoken by Toba ("Again. Do it again."), who isn't in the Yard. Also "bond:(Mark,Toba)" was spoken by Linda ("…time like this, Mark"). `HomeBarkPicker` falls back to any speaker when the involved ones can't speak. Suggest dropping the bark instead of handing it to an uninvolved character.
9. **Minor: Idle barks are repetitive.** Over 3 minutes of planning, Kevin and Toba alternated the same two lines about every 50 s ("Can I help with something?", "I will go wherever I am needed.").
10. **Minor: the FP gain VFX plays once at level start (corrected).** `FPGainAnimation` in `Level Info Panel.prefab` is saved active, so its animation plays as the level loads. The `DisableOnAnimationEnd` behaviour on its `AC_FTPPanel_FPGain` state turns it off afterwards, so later gains replay it as they should. My first reading (that nothing turns it off) was wrong. 0(m) was probably not seen because FP was already full, and `PlayerController.ProduceFTP` plays the VFX only when the value goes up. Same files as `origin/main`. Fix if wanted: save `FPGainAnimation` inactive. Also, `FTPIndicator.prefab` has no `ftpGainVFX` assigned and would throw if it were used.
11. **Minor: Linda shows twice at Dawn (recurs).** `Day 3 DawnPlan: LindaInBed (shows Linda) | Linda=shown@bedroom-Linda`.
12. **Minor: Send-off, the family at home stays put.** Toba (free, in her bedroom) did not walk to the Door; Mark and Kevin were seated. Check whether 4.6 means everyone at home or only the free ones.
13. **Minor: The combat log LOADOUT line leaves out unlock nodes.** John: "Tree: Hide and Seek 1" without Father's Resolve.
14. **Still open:** 0(k) enemy info shows only the HP bar on hover (Goblin Camp, Mossy Hollow); "Max Damage Dealt 0" on the stats screen; the Skill Trees button needs two clicks; node descriptions only on click; hens go hungry by Day 4 ("1 went hungry (no feed)"); Toba's double Care Bond (Lucy & Toba +16 at the Vigil).

### Status

Run A done except 0(j), the diamond hover outline, Kevin's walk and the rack trace. Run B done for 6.3 and the 0(n) panel and save. Node combat effects and 0(m) still need a hand-played fight. Part B not run.

## Oct 14 playtest fixes: report kept across sorties, Kitchen forecast, recipe cards

2026-10-15. From findings 1–3 of "Playtest: open checks, Oct 14 run".

### Built

- **The day's report is part of the save.** `HomeSaveData.report` (new) holds today's `HomeDayReport`, and `HomeSimulation.CurrentReport` reads and writes it. `Resume()` keeps it when it is today's and replaces it otherwise (an old save reads day 0). `HomeDayReport` gained a parameterless constructor for JsonUtility. Result: on a sortie day the Dawn lines (harvest, hens, moon, Workshop delivery) and their headlines (the Weapon card) survive the Home scene reload after combat and a Play restart. The "headlines seen" counter now indexes a list that stays the same across reloads.
- **Mary's Kitchen badge sees the morning.** With a Kitchen seat in the Morning, `HomeStationState.DescribeKitchenOwner` judges her afternoon on a forecast copy of the sim after the morning resolves. It reads "Mary won't cook: the morning's cooking fills the pantry" or "…: the morning's cooking uses the ingredients". At Dusk and Night it reads "Mary cooks X tomorrow afternoon".
- **Recipe cards from the Study and missions.** `UnlockRecipeOutcome` marks its line as a Recipe headline (refId = recipe), like a Kitchen discovery. One card per recipe (The Lantern gives two), spoken by Mary.
- **`Level Info Panel.prefab` (THJ):** `FPGainAnimation` is saved inactive, so it no longer plays as the level loads; `PlayFTPGainVFX` turns it on for each gain.
- **Linda shown twice (added at THJ's request):** `HomeIdleDirector.Update` re-hides every claimed character each tick (`Show(c, view, false)`; `SetClaimed` is a no-op when already hidden). Covers an idle claimed before `HomeHouseView` has created the avatars after a scene load.
- Tests: `Editor/HomeSimulationTests.ReportPersistence.cs` (6). The report survives a rebuilt sim and a JsonUtility round trip with its Weapon headline; another day's report is replaced on Resume; a morning batch that fills the pantry stops Mary on the badge and in the result; "tomorrow afternoon" at Dusk; a recipe learned outside the Kitchen gives one Recipe card.

### Verified

- Unity compiles; EditMode suite as expected (all green except `AIRegressionTest.Baseline_MatchesCurrentAI`, known red), per THJ.

- **Play check (Claude, 2026-10-15)**, New Cycle in Sim Debug, Day 1 → Day 2 Dusk with a Goblin Camp sortie:
  - Weapon on a sortie day: sword ordered Day 1 with Mark helping, delivered at Day 2 Dawn, sortie, F12. Back home the Dusk shows "A weapon is ready · Ben · Uncle Ben finished Ancestral Sword Lv.2", and the Dining Table lists the Day 2 Dawn lines (harvest, hens, Ben, moon) above the sortie. The combat LOADOUT shows the sword at Lv1.
  - Mary's badge: pantry 2/4, Kevin batch-cooking Gourd Omelette in the Morning → "Mary won't cook: the morning's cooking fills the pantry". Dining Table: "Mary didn't cook: the pantry is full". At Night: "Mary cooks Gourd Omelette tomorrow afternoon".
  - The Lantern (granted, studied by John): two cards at Dusk, "A new recipe · Mary", Quickberry Tart then Hunter's Skewer, after the skill-point cards.
  - Linda: Day 1 Dawn log `LindaInBed (shows Linda) | Linda=hidden@bedroom-Linda`. After two scene loads (Play start at Dusk, return from the sortie) the idle was claimed while avatars were `none`, and only the dinner idle showed at the table: no extra avatars.
  - Bonus 0(n): Hide and Seek at level 1 spawned 3 decoys (combat log), matching the 2 → 3 → 4 spec.

### Not verified

- The FP gain effect replaying on a gain: FP was full at the start of Goblin Camp (6/6) and at its practical cap after the duo (7/9), so L gave no gain. Not playing at level load follows from the object being saved inactive.

### Findings

- The Kitchen badge builds a forecast copy (a JSON clone of the save) on each refresh only while a Morning Kitchen seat exists. Watch for a hitch on that badge if refreshes are frequent.
- Minor, new: the recap strip's Unlocked column misses learned recipes and revealed missions. `HomeRecap` checks `StartsWith("Learned recipe")` / `"Revealed mission"`, but outcome lines carry their source prefix ("Star Chart: The Lantern: Learned recipe: …").
- Minor, new: the Workshop badge says "Ready in 2 Dawns" while a helper sits there that day; the order is ready at the next Dawn (Noon badge: "Ready at Dawn").
- Minor, new: on Night 1 the Great Moon took no clicks (no tooltip either); Sim Debug "Run to next Dawn" moved on. Not reproduced.
- Minor: Mary's and Ben's headline cards have no portrait.

### Status

Built; EditMode green (THJ); Play-checked except the FP gain replay. Committed by THJ: `849c318ab` (prefab), `2f828e662` (code and tests).
