# Report: Feedback pass C4, low-HP state and presenter

Plan: plans/2026-10-22-feedback-pass-tech.md (section C4; design rev. 2, Systems "Low HP", UX "Heartbeat vignette"; D-113, D-146, D-147)    Agent: miso-implementer    Branch: thj/quick-wins (on top of `ee2613f59`)
Outcome: done (builds, compiles clean, EditMode green except the known red; not play-tested).

## What changed

All new `.cs` files are LF without BOM like their neighbours, except `LowHealthRulesTests.cs`, which has a BOM like `MiniHealthBarRulesTests.cs` beside it. The `.meta` files were made by Unity. Both scenes are LF and stay LF.

| File (under `miso/Assets/_Project/`) | Lines | What |
|---|---|---|
| `Features/UI/Panels/Scripts/MiniHealthBar/UnitMiniHealthBar.cs` | +11 / -2 | class made `partial`; hooks: check low state after a hit and in `LateUpdate`, pulse in `LateUpdate`, clear in `OnDisable`, drop listeners in `OnDestroy` |
| `Features/UI/Panels/Scripts/MiniHealthBar/UnitMiniHealthBar.LowHealth.cs` (+ `.meta`, 2) | 91 | new partial: low state, `LowHealthChanged` event, `IsLow`, amber-red pulse |
| `Features/UI/Panels/Scripts/MiniHealthBar/LowHealthRules.cs` (+ `.meta`, 2) | 52 | pure statics: `IsLow`, `IsCrossing`, `Evaluate`, `PausableStep`, `PulseWeight` |
| `Features/UI/Panels/Scripts/MiniHealthBar/Editor/LowHealthRulesTests.cs` (+ `.meta`, 2) | 117 | 15 EditMode tests |
| `Features/Effects/LowHealth.meta` | 8 | folder meta |
| `Features/Effects/LowHealth/LowHealthCadence.cs` (+ `.meta`, 2) | 161 | `HeartbeatBeat` enum, `LowHealthCadence` (when to play), `HeartbeatSchedule` (the vignette run, never stacks, lub-dub curve) |
| `Features/Effects/LowHealth/LowHealthPresenter.cs` (+ `.meta`, 2) | 309 | scene component: vignette canvas, bus and bar listening, sounds |
| `Features/Effects/LowHealth/Editor.meta` | 8 | folder meta |
| `Features/Effects/LowHealth/Editor/LowHealthCadenceTests.cs` (+ `.meta`, 2) | 186 | 17 EditMode tests |
| `Scenes/CombatLevelContainerScene.unity` | +58 / -0 | new `LowHealthFeedback` object under `---Management---` |
| `Scenes/DevScenes/TestLevel.unity` | +58 / -0 | the same object |

**Scene hunks** (the same two in each scene, nothing else): `---Management---`'s Transform (`&359199996`) `m_Children` gains `- {fileID: 1729346502}` after KillFeedback's; a new block (GameObject `&1729346501` `LowHealthFeedback`, Transform `&1729346502`, MonoBehaviour `&1729346503` with the presenter's defaults) right after the KillFeedback block. I wrote it with a one-off Python script (in the scratchpad, not the repo) while neither scene was open, the way C2 did. Then I opened each scene additively from a script: the component and its values read back, the scene was not dirty, and I closed it without saving. THJ's open scene (PreloadScreen) was not touched.

## How it works

### State (on the mini bar)

- **Player faction only:** `unit.Faction == CombatLevel.Instance.PlayerFaction` (read straight, not through `GUnit.isPlayerUnit`, which throws with no level). Otherwise the bar is never low and raises nothing.
- **Low** = alive, and health ≤ 25% of max (`lowHealthThreshold`, serialized), both measured from the attribute's minimum. Exactly 25% is low.
- **Crossing** = a known state that was not low becomes low. The bar's first check (nothing known yet, e.g. the unit has just been set up) is never a crossing: a member who is already low then is covered by the level-start announcement. Dying clears the state (not a crossing). Healing above clears it; dropping again is a new crossing. A max-HP change is checked every frame in `LateUpdate` (no event needed), so raising max HP can make a crossing and lowering it can clear one.
- Checked in `OnHealthChanged` (so a crossing lands in the same frame as the hit and its red flash) and in `LateUpdate`. Disabling the bar clears the state and forgets it.
- **Event:** `public event Action<UnitMiniHealthBar, bool, bool> LowHealthChanged` (bar, isLow, crossed), raised only on a change; `IsLow` property. Instance event, cleared on destroy. No statics.
- **Look:** while low, the fill pulses between `lowFillColor` (0.95, 0.36, 0.12, amber-red, `#F25C1F`) and `lowFillDimColor` (0.6, 0.12, 0.06, `#991F0F`) every 0.8 s (`lowPulsePeriod`), cosine ease, starting bright. Its clock runs on `Time.unscaledDeltaTime`, but only while `Time.timeScale > 0`, so it freezes under the pause menu and tutorials and ignores slow-mo. Back to the green `fillColor` when no longer low. Enemies never pulse.

### Cadence (`LowHealthCadence`, one per level)

| Moment | Beat |
|---|---|
| A crossing before any turn has started (setup, HP carry-over) | none; folded into the level-start announcement |
| A crossing after a turn has started | **announcement**: the sting now, then 3 heartbeat cycles 0.15 s later |
| The first player turn becomes live (its banner is gone), any member low, and no announcement yet this level | **announcement** (one sting, however many are low) |
| Every later player turn becomes live, any member low | one cycle |
| A low member is selected while the player turn is live | one cycle, at most once per member per player turn |
| A selection while the banner is still up (the automatic turn-start selection) | none, and it doesn't use up that member's cap |

**"Live" = after the banner.** The player's banner holds an input lock until it has slid out (`CombatLevelUIManager.PlayPhaseAnimation`), so the presenter waits after a player `turnStarted` until `PlayerInputController.Instance.IsInputLocked` is false, or 4 s on the pause-aware clock (`bannerWaitLimit`), whichever comes first.

### Vignette (`HeartbeatSchedule` + presenter)

- **Never stacks:** one run at a time. A request for no more cycles than are left is dropped. A request for more (an announcement while a single cycle runs) raises the count left to that many, counting the cycle playing now: no restart, no second vignette. The sting still plays.
- **Lub-dub:** in a 0.8 s cycle, a sine pulse of 0.12 s peaking at alpha 0.25, then 0.15 s of nothing, then a 0.12 s pulse peaking at 0.18 (second pulse 0.27 to 0.39 s), then quiet until 0.8 s. All values are serialized.
- **Clock:** the presenter's own, `Time.unscaledDeltaTime` added only while `Time.timeScale > 0`. A pause freezes the vignette at its current alpha, and it carries on when the game resumes. Slow-mo doesn't slow it.
- **Canvas:** built in `Awake` as a child of the presenter: `LowHealthVignette` (Canvas, Screen Space Overlay, sorting order -1, so HUD and menu canvases at 0 and above draw over it) > `Vignette` (full-screen stretched `Image`, `raycastTarget` off, no `GraphicRaycaster` anywhere: it can't block clicks). The canvas is switched off whenever the alpha is 0. It is its own UI canvas, not a camera volume, so the red hit flash (`PlayerHit_CameraVolumeEffect`, a volume) can't cancel it.
- **Colour:** `vignetteColor` pure red (1, 0, 0), the colour of the hit flash's `BorderOverlay` in `PlayerHit_CV.asset`.
- **Asset:** none added. `vignetteSprite` is serialized and empty by default; when empty, the presenter makes a placeholder in code: a 128 x 128 white texture whose alpha is opaque at the screen edges and fades to clear about a third of the way in (smoothstep per axis, combined so the corners are strongest, squared). Created in `Awake`, destroyed in `OnDestroy`. Art can drop a real gradient sprite into the field later.

### Hooks used

- **Bus** (re-bound in `Update` whenever `GlobalEventBus.Instance` changes, as in C2's presenter; a new bus resets the cadence and the vignette): `turnStarted` (cadence, banner wait, rescan bars), `unitBorn` and `levelStarted` (rescan bars), `unitSelectionChanged` (selection).
- **Selection hook:** `GlobalEventBus.unitSelectionChanged(FactionControllerBase, GUnit)`, raised by `FactionControllerBase`'s unit-selection state and by `PlayerController` after a reactive. The presenter looks the unit up among the bars and asks `IsLow`. Enemy selections are never low, and selections outside a live player turn are ignored.
- **Bars:** `FindObjectsByType<UnitMiniHealthBar>` (active only) on each rescan. Every bar is subscribed, since only player-faction bars ever raise. All bars are unsubscribed before each rescan, on a bus change and on destroy.
- **Sounds:** `stingSfxId` and `heartbeatSfxId`, both empty in the code and in both scenes (D-147: no borrowed placeholders). Empty plays nothing. When set, the heartbeat plays at the start of each cycle.
- No tweens or coroutines anywhere: the pulse, vignette and banner wait are all computed per frame from the clocks, so there's nothing to kill on destroy.

## Acceptance criteria

- [x] Low state, player faction only, exact 25% is low, only on crossing, heal-then-drop re-crosses, dead isn't low, max-HP change: `LowHealthRulesTests` (15 tests). The faction filter and per-frame wiring need the play check.
- [x] Cadence and caps: `LowHealthCadenceTests` (17 tests): level-start folding and a single announcement, a crossing announces, a crossing during an enemy first turn replaces the level-start one, a cycle each later player turn only while someone is low, selection once per member per turn (two members each get one, the cap resets next turn, a selection under the banner doesn't count), never stacks (dropped / extended without restart), the 3-cycle run after 0.15 s, a stopped clock holds the vignette, lub-dub peaks.
- [ ] Mini bar pulse, vignette look, sting/heartbeat timing on screen, "survives the red hit flash", "pauses with the game": by construction (own overlay canvas; pause-aware clock, tested), needs THJ's play check.
- [ ] Enemy-turn length unchanged: nothing waits or locks input. Play check.
- [x] Compile clean: forced refresh plus compile through the Unity MCP; no errors in the console (only the project's existing warnings). EditMode **595/596**; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red, untouched).

## Save reset

No.

## Decisions I made

- **The turn-start cycle waits for the banner too** (the plan only says so for the level-start announcement). At `turnStarted` the banner is still sliding in, and the turn only becomes playable when it ends. Waiting keeps one rule for both cases and stops the automatic turn-start selection from using up a member's selection cycle under the banner. The cycle comes about 1 s later than at the raw `turnStarted`. Easy to change if THJ wants it at the banner's start.
- **An announcement while a cycle runs extends the run** to 3 cycles (counting the one playing) instead of being dropped, and its sting still plays. Read "never stacks" as "one vignette, never restarted or doubled". A single-cycle request while anything runs is dropped, as the design says.
- **A crossing during an enemy turn that comes before the first player turn** gets its own announcement. The first player turn then gives only a cycle, even if other members started low.
- **"0.15 s apart"** read as end of the first pulse to start of the second (lub 0 to 0.12 s, dub 0.27 to 0.39 s). Start to start would leave only 0.03 s between pulses. `pulseGap` is serialized.
- **Vignette canvas built in code**, with an optional serialized sprite. This keeps the scene diff to one plain object, and there is no texture asset to import. Same look as a scene-authored canvas.
- **Sorting order -1** so the HUD and pause menu draw over the vignette's edges.
- **Bars found with `FindObjectsByType`**, not through the player faction controller's `AllUnits`. That controller's `PhaseData` isn't null-safe before it is initialised, and the bar already filters by faction.
- **The pause rule uses `Time.timeScale == 0`**, as the plan and the task say. The design text mentions "the pause state, not the time scale"; I followed the plan.
- **Low colours:** amber-red `#F25C1F` / dim `#991F0F`, picked against the bar green `#0A8D3E`, the damage-preview red `#A60000` and the lethal `#6B0008`. They are placeholders for THJ's eye.

## Needs THJ

None blocking. The calls above (banner wait for every turn-start cycle, extend-not-drop for the announcement) are yours to overrule at the play check.

## Docs to update

- `design/gdd/combat-rules.md` "Combat feedback" (game designer): the low-HP rule (25%, player faction, crossing), the cadence table, the vignette values.
- `tech/pace-timings.md` (coordinator): a row saying the heartbeat is fire-and-forget (the 2.4 s crossing run never holds the turn).
- Plan commit log (coordinator).

## Risks and loose ends

- **Faction check:** units in an allied faction (if `Unit_Toba_Ally` is not in `PlayerFaction`) never go low. Toba as a party member in the player faction does. Worth a look on a level with an allied Toba.
- **A member who joins mid-level already low** (spawned or revived low) is not a crossing. They're picked up by the next turn-start cycle. A unit revived from dead straight to ≤ 25% while known *is* a crossing (dead counts as "not low").
- **Banner-wait fallback:** if some other input lock (enemy introduction, a dialogue) is held after the banner, the turn-start beat waits for it, up to 4 s of unpaused time. That is probably what we want ("after the banner and any intro"), but it's not seen in play.
- **Pause freezes the vignette visible** at its current alpha (under the pause menu, which sorts above it). That's the "pauses with the game" reading. If it should hide while paused, that's a one-line change.
- **Rescan cost:** `FindObjectsByType` on each turn start, `unitBorn` and level start. Fine at our unit counts.
- **Hit slow-mo:** the pulse and vignette ignore slow-mo (real time), as the design asks; the C3 chip still uses scaled time.
- C5 can use `UnitMiniHealthBar.IsLow` and `LowHealthChanged`. If the HUD glow should beat in time with the vignette, it will need a beat signal or the schedule exposed from the presenter. Not added (not in C4).

## Proposed commits

1. `feat(ui): family members at low health pulse and get a heartbeat vignette` (plain; one unit, since the scene objects need the scripts, and the bar's hooks and the presenter only work together; the tests go with it, as the plan asks):
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/MiniHealthBar/UnitMiniHealthBar.cs`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/MiniHealthBar/UnitMiniHealthBar.LowHealth.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/MiniHealthBar/LowHealthRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/MiniHealthBar/Editor/LowHealthRulesTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Effects/LowHealth.meta`
   - `miso/Assets/_Project/Features/Effects/LowHealth/LowHealthCadence.cs` + `.meta`, `LowHealthPresenter.cs` + `.meta`, `Editor.meta`, `Editor/LowHealthCadenceTests.cs` + `.meta`
   - `miso/Assets/_Project/Scenes/CombatLevelContainerScene.unity`
   - `miso/Assets/_Project/Scenes/DevScenes/TestLevel.unity`

   Not `Packages/` or `ProjectSettings/`: those changes were there before this task and are not mine.

## Other branches

`thj/home-test` gets it with `main`, as the plan says.

## How THJ can see it

The object is `---Management--- / LowHealthFeedback` in `CombatLevelContainerScene` (and `TestLevel`). To hear the cues, fill its `Sting Sfx Id` / `Heartbeat Sfx Id` (empty plays nothing). The cheat menu or an enemy can bring a member's HP down.

1. **A member crossing 25%:** let an enemy (or a cheat) take a Bergson from above 25% to 25% or below. You get the red hit flash, then 0.15 s later three red edge "lub-dub" beats (about 2.4 s), and the member's mini bar turns amber-red and pulses every 0.8 s. Hit them again while low: no new beats.
2. **A level started with a member already low:** start a mission with a member at the 20% carry-over floor. Nothing plays during setup. Turn 1 has no banner (the first turn starts without the phase animation), so the one announcement (three beats) plays as turn 1 begins, while the HUD slides in, even with two members low. Their bars pulse from the start.
3. **Selecting a low member twice in one turn:** click the low member: one beat. Click someone else, then them again: nothing. A second low member gets their own one beat. Next player turn, selecting them gives one beat again.
4. **Turn starts while low:** end the turn. After the enemy turn, when your banner has slid out, one beat plays. With nobody low, nothing.
5. **Healing above and dropping again:** heal the member above 25%: the bar goes back to green, no sound. Bring them down to 25% or below again: the full three-beat announcement plays again.
6. **Pause during a heartbeat:** open the pause menu mid-announcement. The vignette freezes where it was (under the menu) and the bar pulses stop. Resume and they carry on from there. The same happens with a tutorial pop-up.
7. **A red hit flash during the vignette:** hit a low member while beats are playing (or cross with a hit): the red flash plays and the beats carry on through it without restarting or doubling.
8. **Enemies:** bring an enemy below 25%: its bar stays green, no beats.
9. **Clicks:** during a beat, clicking tiles, units and HUD buttons works as normal (the vignette blocks nothing).

## Review fixes

After the reviewer's FIX verdict, these three changes and nothing else:

1. **A lethal hit is not a crossing.** `onValueChanged` fires before `onMinReached` leads to `Die`, so the bar saw a unit still alive at health 0 and announced on the death. `LowHealthRules.IsLow` now also requires health above the minimum (`health > 0f`, measured from `MinValue`), and its comment says why. New test `LethalHitFromAbove_IsNotACrossing` (known, was not low, alive, health 0 of 100: not low, not crossed).
2. **One sting per run.** `LowHealthPresenter.Play` plays the sting only when `_schedule.Request(...)` takes the announcement. A fresh run, or an announcement that extends a running single cycle, keeps its sting. A second announcement while a 3-cycle run is going (e.g. two members crossing on one hit) is dropped, sting included.
3. **The turn stops being live at `turnEnded`.** `PlayerController.StartTurn`'s automatic selection fires before `turnStarted`, so when the player plays twice in a row it was treated as a live selection under the banner. New `LowHealthCadence.OnTurnEnded()` clears the flag. The presenter subscribes to `turnEnded` in the bus binding and removes it in `Rebind`, which also runs from `OnDisable`. New test `SelectionAfterTurnEndBeforeNextTurnStart_PlaysNothingAndKeepsTheCap`.

I also fixed step 2 of "How THJ can see it": turn 1 has no banner, so the level-start announcement plays as turn 1 begins.

Files touched (all LF; the test file keeps its BOM): `Features/UI/Panels/Scripts/MiniHealthBar/LowHealthRules.cs`, `.../MiniHealthBar/Editor/LowHealthRulesTests.cs`, `Features/Effects/LowHealth/LowHealthCadence.cs`, `.../LowHealth/LowHealthPresenter.cs`, `.../LowHealth/Editor/LowHealthCadenceTests.cs`. No scene or meta changes, and the commit grouping is unchanged.

**Checks:** forced refresh and recompile with no console errors. EditMode **597/598**; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. Not play-tested.

## Look retune after THJ's play test

THJ: the triggers and conditions are right, but the vignette was too fast, too red, too bright and reached too far in (his reference is a dark, desaturated blood red that stays near the edges and corners, with the centre clear). I changed only the vignette's look and timing. Every trigger, cap and rule is unchanged. The new values are the code defaults and are set on `LowHealthFeedback` in both scenes.

| Value | Old | New |
|---|---|---|
| `vignetteColor` | (1, 0, 0) pure red | (0.42, 0.04, 0.04) dark blood red |
| `edgeReach` (new field, generated placeholder only) | fixed 0.32 in code | 0.25: the tint fades to zero a quarter of the way in from each edge, so the middle half of the screen stays clear |
| `firstPeak` / `secondPeak` | 0.25 / 0.18 | 0.16 / 0.11 |
| `cycleLength` | 0.8 s | 1.2 s |
| `pulseLength` | 0.12 s | 0.2 s |
| `pulseGap` (end of the first pulse to start of the second) | 0.15 s | 0.25 s (lub 0 to 0.2 s, dub 0.45 to 0.65 s) |
| Pulse shape | sine hump | squared sine: eases in and out with zero slope at both ends |
| Announcement | 0.15 s + 3 x 0.8 s = 2.55 s | 0.15 s + 3 x 1.2 s = 3.75 s (still 3 cycles; delay unchanged) |

- **Gradient:** a smoothstep falloff on each axis over `edgeReach`, combined so the corners come out a little stronger than the middle of each edge, then squared for a soft inner fade. The texture is still generated in `Awake` from these values; a sprite set in `vignetteSprite` replaces it.
- **Code:** `LowHealthPresenter.cs` (new `edgeReach` field, new defaults, the texture reads `edgeReach`), `LowHealthCadence.cs` (`HeartbeatSchedule` defaults; `LubDubAlpha` uses a squared sine).
- **Tests:** `LowHealthCadenceTests.cs`. The schedule tests now use 1.2 s cycles, the lub-dub peak test uses the new values, and there is a new `LubDub_EasesInAndOut`.
- **Scenes:** each scene's `LowHealthFeedback` block gets one new line (`edgeReach: 0.25`) and five changed values (colour, cycle, pulse, gap, peaks). Each scene diff against HEAD is still only the new object (now 59 lines). I checked by loading both scenes additively: the values read back and neither scene was dirty.
- Not added: the steady overlay THJ mentioned (after C5).

**Checks:** forced refresh and recompile with no console errors. EditMode **598/599**; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. Not play-tested since the retune. All files keep LF (the one test file that has a BOM keeps it). Nothing staged.
