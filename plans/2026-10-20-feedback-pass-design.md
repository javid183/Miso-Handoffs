# Feedback pass: hits, kills, lethal preview and low HP as one language

Size: M    Tier: 3 (game feel and a new readability feature are THJ's until 2026-10-29)    Assigned to: miso-game-designer (design), then tech plan, then miso-implementer
Branch: all (the build goes on a quick-wins branch from `main`; nothing here differs by branch)
Status: waiting on THJ

## Why

Bundle F of the [quick-wins triage](2026-10-20-quick-wins-triage.md): playtest items **Q5** (juice top-up: Parsa, Oct build, still named hits and kills as the weak spot), **Q6** (always-visible mini HP bars, a lethal-hit preview, a low-HP warning; asked by Al, U, Y, J) and **Q24** (low-HP feedback, "should be designed"). Source text: [`playtests/2026-10-playtest-tasks.md`](../playtests/2026-10-playtest-tasks.md) lines 79, 80, 106.

## Goal

One feedback language in which every hit, kill, lethal preview and low-HP state has a fixed channel, size and priority, so combat lands harder without burying the Shift and preview layers.

## Problem and evidence

**Symptom (playtest):** hits and kills feel weak; HP is hard to read without hovering; nothing says "this one is about to die", on either side.

**Root problem:** the feedback that exists was added piecemeal per prefab, has no owner and no priority, and some of it cancels itself. Kills have no feedback of their own, and HP state lives only in hover panels.

Evidence (verified in code and prefab data on `masher-tweak` = `main` @ `08ca1d819`, 2026-10-20, unless marked):

1. **Hit-stop is already on every enemy, but it's a slow-mo, not a stop.** `UnitBase.prefab` `hitEffects` (line ~2312) calls `PlayHitBlink`, `PlayHitSlowMo`, `PlayHitFX`, `UnitHit_CameraVolumeEffect` and `UnitHit_ShakeCameraEffect`. Every enemy variant inherits it, because each one calls `PlayHit` from HP `onValueDecreased`. Archer and both Claws also call `PlayHitSlowMo` directly, so it runs twice. The triage row's "wired only on UnitBase, Claws and Archer" undercounts this. The curve (`hitSlowMoDuration` 0.2) drops to a time scale of about 0.13 within 0.02 s and holds 0.13 to 0.19 until 0.17 s. It reads as "slow", not as "impact".
2. **Bergsons have no hit-stop and no shake on hits.** `Unit_John.prefab` disables `hitEffects` calls 1 to 3 (slow-mo, hit FX, unit volume) and swaps call 4 (the shake) for `PlayerHit_CameraVolumeEffect`, the red flash (0.05 s in, 0.05 s hold, 0.05 s out). Linda, Lucy, Mark and Toba have the same four overrides. *Assumed to be the same pattern; only John was read line by line.*
3. **No kill feedback.** The death path (`onMinReached`, then `SimplePlayEndFrozen("Die")`, then `GUnit.Die(1)`, then `GlobalEventBus.unitDied`, fired at once in `DieInternal`, `GUnit.cs:762`) has no flash, freeze or shake.
4. **The shakes cancel each other.** `CameraEffectBase.ActiveSCRs` is **static** (`CameraEffectBase.cs:12`), so any non-additive shake stops every running shake. If an area attack kills target 1 and then hits target 2, target 2's small hit shake would cut target 1's kill shake short.
5. **The screen volumes cancel each other.** A non-additive `CameraVolumeEffect.Apply` reverts every active volume through the static `_activeVolumes` (`VolumeCameraEffect.cs:30-37`). A held low-HP volume would be erased by the next red hit flash. So the low-HP overlay can't be a camera volume.
6. **Several systems write the time scale with no shared owner.** `TimeScaleCache` has a lease and notify protocol (`TimeScaleCache.cs`), and `GUnit.PlayHitSlowMo` uses it. But Family Role activation (`PlayerController.cs:1470`), the Duo target pick (`UnitsCooperationHandler.cs:228`, time scale 0), Mark's catch (`ProjectileCatchAndReturn.cs:212`) and pause write `Time.timeScale` directly, without notify. A hit-stop that's running sets the scale every frame and restores the cached value at the end, so it can overwrite a role slow-mo. *That is the code; whether it shows in play today is not verified.*
7. **HP is readable only on hover, Shift or preview.** `EntityInfoPanelUI` has three modes (Global = Shift, FullDetail = hover, Damage = preview) and a **one-slot queue** (`_queueData`, with `Debug.LogError` when a second item is stacked). A fourth "Mini" mode would need a stack.
8. **The lethal data exists but is never shown.** Every damage preview (`PlayerController`, the Duo preview in `UnitsCooperationHandler:610`, the Masher role preview in `MasherGoblinFactionRoleHandler:424`) goes through `GUnit.ShowDamagePreview(amount)`, then `EntityInfoPanelUI.ShowHealthMode()`, which already has `damageValue` and `healthAttribute.Value`. `AbilityDamagePreview.PredictsLethalOn` uses `damage >= hp.Value`. `ComputeFor` returns damage per unit, so area attacks and friendly fire are covered.
9. **No low-HP state anywhere** (no `LowHealth` or `Heartbeat` in code). The selected-unit HUD bar (`UnitPanelUI._healthBarFill`) tracks HP live through `onValueChanged`. On `main` (FTP), the ATB portrait row is not in use, so the only HUD portrait is the selected unit's (`UnitPanelUI.unitImage`). *Assumed from `InitATBGaugeView` being ATB-only; not checked in play.*
10. **HP carries over between levels, with a floor of 20% of max** (CR-24). Any threshold above 20% means a member who starts a level at the floor starts it in the low-HP state.

## Lens notes

### Creative

**Target experience.** Hitting an enemy should feel like the family's strength landing: a short, sharp stop, then release. A kill should be a punctuation mark the player looks forward to. A Bergson in danger should feel like worry for *someone*, not a generic red screen: warmth against dread, as in Children of Morta, where the family's wounds are what the game makes you care about.

**The moment to design for.** Lucy is at 4 HP with a Black Claw two tiles away. The player picks Linda, hovers the Claw, and sees a skull on its bar. The arrow lands: the world stops for a breath, the Claw goes white, the camera kicks, and only then does it crumple. Lucy's bar stops pulsing red at the edges of the screen. Seeing the kill coming, then the kill landing, then relief: that is the over-the-bar beat.

**The language, in one rule:** *the world shows what the family does; the screen shows what happens to the family.* Effects on enemies stay in the world (sprite flash, hit FX, a time stop, a camera kick). Effects on Bergsons may use the screen (red flash, heartbeat vignette, HUD glow). That keeps the screen-level signals rare and personal, and the two never compete for the same space.

### Systems

**Channels.** Each channel carries at most one effect at a time, and a combat feedback director arbitrates them:

| Channel | Carries | Owner today | Owner after |
| --- | --- | --- | --- |
| Time | hit-stop, kill freeze | `GUnit.PlayHitSlowMo` (per unit, from the prefab) | director (Option B) |
| Camera | shake | the prefab `hitEffects` (`UnitHit_ShakeCameraEffect`) | director |
| Screen | red hit flash (family), heartbeat vignette (family) | prefab (`PlayerHit_CameraVolumeEffect`) | flash: unchanged; vignette: new UI overlay |
| Unit body | blink, hit FX, kill flash | prefab | blink and FX: unchanged; kill flash: director |
| World UI | mini bar, damage chip, lethal skull, low-HP pulse | none | mini bar component, info panel |
| HUD | low-HP bar glow, portrait tint, item-pouch nudge | none | `UnitPanelUI` addition |
| Audio | hit SFX (per prefab `PlaySFX`), kill sting, heartbeat | prefab | hit: unchanged; new stings: director and low-HP presenter |

**Event tiers and priority** (highest first). Within one **coalescing window of 0.1 s real time**, each channel plays only the highest tier that fired. A higher tier replaces a lower one that is running; a lower one never interrupts a higher one.

1. **A Bergson falls.** Keeps its existing beat (the death animation, then Revenge, CR-25). The director plays **no** enemy-kill beat on it, and no white flash. *Out of scope beyond that rule.*
2. **Kill** (an enemy, or any unit not in the player faction, dies).
3. **A Bergson crosses the low-HP threshold** on this hit.
4. **Critical hit** (`onCriticalDamageDoneOnUnit`, which fires before the HP change).
5. **A Bergson is hit.**
6. **An enemy is hit.**
7. **Damage over time and push damage** (Burn ticks, collisions). Blink and SFX only, with no time or camera effect. *How the tech plan detects these hits is open; if they can't be told apart cheaply, they play as tier 6.*

**Starting values** (real seconds; a time scale of 1 is normal speed):

| Event | Time | Camera shake (`baseMagnitude`, duration) | Body | Screen | Audio |
| --- | --- | --- | --- | --- | --- |
| Enemy hit | Hit-stop: drop to 0.05 in 0.015 s, hold to 0.09 s, ease back to 1 by 0.14 s (ease-in quad) | 0.02, 0.2 s (current values) | blink (current), hit FX | none | current hit SFX |
| Bergson hit | none (as today) | **new** 0.03, 0.2 s | blink | red flash (current) | current |
| Crit | 0.05 hold for 0.10 s, ease back over 0.08 s | 0.035, 0.25 s | blink | none | crit layer (optional) |
| Bergson crosses low HP | 0.05 hold for 0.08 s, ease back over 0.08 s | 0.035, 0.25 s | blink | red flash, then the heartbeat starts 0.15 s later | low-HP sting |
| Kill | **time scale 0 for 0.12 s**, ease back over 0.15 s (ease-out quad) | 0.05, 0.3 s; +0.01 per extra kill in the window, capped at 0.07 | **kill flash:** the sprite goes to full white (`_ColorOverride`) for 0.12 s, then the death animation runs | none | kill sting on top of the hit SFX |
| Multi-kill (2 or more in one window) | one freeze, extended by 0.03 s per extra kill, capped at a 0.2 s hold | as above | every victim flashes at once | none | one sting, pitched up a semitone per extra kill (max +3) |

**Guards (what keeps it from overloading):**

- **Fatigue cap:** at most **2** time effects per **1.0 s** real time. Later ones in that second are skipped, but their camera, body and audio still play. Multi-hit volleys (Lucy's multishot, area attacks) then stop at most twice.
- **Time-owner guard:** the director plays no time effect while a QTE is active (`qteStarted` to `qteEnded`), while the game is paused, or when `Time.timeScale` is not 1 at trigger time (someone else owns time: a role slow-mo, the Duo pick, Mark's catch). That protects the reaction-timing pillar.
- **Previews never move time or the camera.** Tier 0 (anything shown while the player is choosing) is world UI only.
- **The heartbeat never stacks.** One vignette, whatever the number of low members.

**How each lever fails:**

| Lever | Too high | Too low |
| --- | --- | --- |
| Hit-stop hold | enemy turns drag; area attacks stutter | the stop reads as lag, not impact (today's slow-mo problem) |
| Kill freeze | the death animation looks like a hitch | a kill reads like a hit |
| Shake | nausea; it fights the role-zone icons | no kick |
| Low-HP threshold | permanent alarm (see the 20% floor, evidence 10) | the warning comes after it's too late |
| Heartbeat repeats | noise the player tunes out | a member at low HP is forgotten after one turn |

**Interactions:**

- The hit-stop slows DOTween blinks and `ShakeCameraEffect`, which run on scaled time. A shake keeps jittering during a freeze, because it picks a new random offset every frame, and finishes afterwards. That is the classic look, so keep it. UI pulses and the vignette must run on **unscaled** time.
- The kill flash uses the same material property as the hit blink (`_ColorOverride`, `GUnit.cs:932-946`). The kill flash must replace the blink tween, not fight it. The tech plan decides how; `DOTween.Kill(material)` triggers the blink's `OnKill` reset first, which suits this.
- The Family Role, Duo and Synergy kills all go through the same `unitDied` path, so they get the kill beat with no extra rule.

### UX

**What the player sees, and when:**

| Moment | Shown | Not shown |
| --- | --- | --- |
| Idle on the board | A **mini HP bar** on every unit: no number, side colour. A Bergson at low HP: amber-red fill, pulsing every 0.8 s | Panels, skulls |
| Hovering a unit (FullDetail) or holding Shift (Global) | The info panel **replaces** that unit's mini bar in the same spot (the mini bar hides while the panel is up) | Mini bar and panel together |
| Previewing an ability (Damage mode) | The panel shows the damage segment. **If the damage is at least the target's HP: a skull at the left of the bar, a deep-red damage segment, and the skull pulsing at 2 Hz (scale 1 to 1.12).** The same skull on a Bergson or an ally hit by friendly fire | Any time or camera effect |
| A hit lands | A white **damage chip** on the mini bar that holds 0.2 s and drains over 0.35 s (reuses the bar's decrease fill) | |
| A Bergson crosses low HP | Red flash, short stop, sting, then **3 heartbeat cycles** of the screen-edge vignette, fading out | A constant loop |
| Afterwards, while still low | Quiet signals only: the mini bar pulse; and when that Bergson is selected, the HUD bar glow, the portrait tint and **one** heartbeat cycle. At the start of each player turn, if any Bergson is low: one heartbeat cycle | |
| The low Bergson is selected and holds an item that restores HP | The item-pouch button bobs once (scale 1 to 1.15 to 1, 0.3 s) | A bob when no HP item is held |

**Mini bar look:** about 60% of the footprint's width (multi-tile units get a wider bar), about 4 px tall at 1080p, a 1 px dark outline, no text. It sits at the info panel's anchor, so the panel takes its place, with one place to look. Side colours: the ones the info panel already uses. *Not checked which colours those are; the tech plan confirms them, and they must not clash with the four role colours or the Shift tints (CR-41 to CR-43).*

**Heartbeat vignette:** a screen-edge red gradient (the existing hit-flash red), with a "lub-dub" of two pulses (peak alpha 0.25, then 0.18, each 0.12 s, 0.15 s apart) and a 0.8 s cycle (75 bpm). It's a UI image on its own canvas, not a camera volume (evidence 5).

**Portrait and HUD:** the portrait gets a red tint gradient from the bottom (alpha 0.35). The HUD health bar gets an outer glow pulsing in time with the heartbeat (0.8 s).

**Likeliest misreads:**

1. **"Skull = certain kill."** Evasion (CR-21) can still cancel the HP loss. The preview rule is "what a preview promises, the real action does", and the damage preview already leaves out crit and evasion. The skull means "kills if it lands". See Q6 for THJ.
2. **Mini bar mistaken for the role zone or the Shift tint.** Keep the bar off the tiles (at the panel anchor, above the sprite) and keep its colours out of the tint table.
3. **A low-HP pulse on an enemy read as "about to die".** Low HP is a family-only state. Enemies get no pulse; the lethal skull covers "finish it".
4. **Starting a level already at low HP** (the 20% floor) and hearing the heartbeat at once. That's intended: they *are* hurt. The announce-once rule stops it nagging.

## Options compared

Three decisions really matter. The rest are values for THJ to tune in play.

### 1. Who owns time and the camera (Q5)

| | **A. Retune and add.** Keep `GUnit.PlayHitSlowMo` and the prefab shake on hits, retune the curve on `UnitBase`. A director adds kill and crit only, through the `TimeScaleCache` notify protocol, and fires the kill shake one frame late | **B. One arbiter** *(lean)*. The director owns the time and camera channels for every tier. Disable `PlayHitSlowMo` and the shake in the `UnitBase` `hitEffects` (and the extra direct `PlayHitSlowMo` on Archer and Claws). A small relay component in `hitEffects` tells the director "this unit was hit" | **C. Kills only.** Leave hits as they are, add only the kill beat |
| --- | --- | --- | --- |
| Experience | Better. Hits in later frames can still cut a kill shake (evidence 4) | Consistent: the priority table holds everywhere | Kills land, hits stay mushy (Parsa's complaint stays half fixed) |
| Rules complexity | Two owners, implicit priority | One table | Low |
| Implementation | S: curve data, plus a director for 2 tiers | S–M: director for 6 tiers, plus a one-off editor script for the prefab data | S |
| Risk | Role and QTE time conflicts stay as they are (evidence 6); no fatigue cap on hits | Touches `UnitBase.prefab` (the core death wiring lives there, so it gets its own commit); fixes the conflicts through the guard | Least |
| USP effect | Neutral | Neutral (protects the QTE pillar) | Neutral |

**Lean: B.** The cost gap is one editor script, and only an arbiter can enforce the QTE guard, the fatigue cap and the "lower never interrupts higher" rule that evidence 4 and 6 show are needed. **No `GUnit` code changes in A or B:** `PlayHit`, `hitEffects`, `GetMainVisual()` and the bus events are all public today.

### 2. Mini bar visibility (Q6)

| | **A. Always on, every unit** *(lean)* | **B. Damaged units only** (enemies at full HP show none; Bergsons always) | **C. Status quo** (Shift only) plus a low-HP marker |
| --- | --- | --- | --- |
| Experience | Genre standard (Into the Breach pips, XCOM pips, Fire Emblem bars); what four playtesters asked for | Less clutter at the start of a fight, but "no bar" has to be read as "full HP" | Cleanest board; doesn't answer Q6 |
| Clutter | Highest: 10 to 15 bars on a busy grid | Medium | Lowest |
| Cost | M (one component, the panel-anchor hide) | M plus a rule | S |
| Misread | Few | "Is that enemy unhurt or missing a bar?" | HP is still hidden |

**Lean: A.** It's thin, has no number, and hides under the panel. If it clutters in play, B is a setting flip, not a redesign.

### 3. Low-HP threshold and cadence (Q24)

| | **A. 30% of max, announce once then quiet** *(lean)* | **B. 25% of max, announce once then quiet** | **C. Dynamic: "one hit from death"** (HP at or below the largest damage a threatening enemy can deal next turn) |
| --- | --- | --- | --- |
| Experience | Catches it early; every floor-start (20%) member reads as hurt | Tighter; still catches floor-starts | The most honest ("this enemy can kill her"), Into the Breach style |
| Cost | S | S | M–L: the enemy damage preview for every threat on every HP change; it can disagree with what the AI actually does |
| Risk | Slightly early on high-HP John | May come one hit late for low-HP Lucy | A wrong prediction breaks trust in the skull too |

**Lean: A** for this pass, with C as a later upgrade once the preview pass's threat data (`UnitThreatAnalysis.GetThreateningEnemies`) is proven cheap enough. A constant heartbeat while low was rejected: at the 20% floor it would loop for whole levels.

## Recommendation

**Build B, A and A:** the director owns time and camera; mini bars always on; low HP at 30% of max, announced once, then quiet. The values are in the Systems table. Everything below reuses what exists.

**Cheapest build** (for the tech plan; the order is the suggested commit order):

1. **Lethal skull.** In `EntityInfoPanelUI.ShowHealthMode`, `lethal = damageValue > 0 && damageValue >= healthAttribute.Value` (the same rule as `PredictsLethalOn`), plus a skull image (placeholder sprite) and the deep-red decrease fill. Every preview caller gets it for free (evidence 8). XS, no core change.
2. **Mini HP bar.** A new world-space component on `UnitBase.prefab`, using the `UI_Element_FillBar` prefab, subscribed to the HP attribute's `onValueChanged` (the `UnitPanelUI.TrackHealthAttribute` pattern). It hides while the unit's `EntityInfoPanelUI` is active, and adds the damage chip through `SetDecreaseBarFill`. It owns the low-HP state and raises `LowHealthChanged(unit, isLow, crossedThisHit)`. Not a fourth panel mode (evidence 7).
3. **Combat feedback director.** A scene MonoBehaviour that listens to `unitDied`, `onCriticalDamageDoneOnUnit`, `qteStarted` and `qteEnded`, plus a hit relay called from `hitEffects`. It applies the priority table, the window and the guards. Time goes through `TimeScaleCache` (Cache, Set with notify, Release). Shakes play the existing `ShakeCameraEffect` asset type through `FXRunner.PlayCFX`, with new assets: `BergsonHit_`, `Crit_` and `Kill_ShakeCameraEffect`. The kill flash uses `GetMainVisual().material` and `_ColorOverride`. Needs a `PlayModeStaticReset` hook if it holds statics.
4. **Prefab data** (one-off editor script, its own commit): disable `PlayHitSlowMo` and `UnitHit_ShakeCameraEffect` in the `UnitBase` `hitEffects`; remove the direct `PlayHitSlowMo` on Archer, Dark Claw and Black Claw; add the relay call to `hitEffects` on `UnitBase` and on the five Bergson prefabs, which override that list.
5. **Low-HP presenter.** The vignette on its own overlay canvas (unscaled time), the heartbeat cadence, the `UnitPanelUI` bar glow and portrait tint (a new partial or child component, not edits inside the big file), and the item-pouch bob when the bar's item preview says an item restores HP.
6. **Audio:** kill sting, low-HP sting, heartbeat. They need assets (Q7).

**Playtest signals:**

- **It worked:** without being asked, testers mention kills feeling good. They hover less to check HP (watch how often they use Shift). They heal or retreat a low member within one turn of the warning. Nobody mentions lag.
- **It failed:** "the game stutters" or "hitches" on area attacks or the enemy turn (lower the hit hold to 0.05 s or the fatigue cap to 1). A QTE feels mistimed after a hit (check the guard). Testers say the board is busy (try Option 2B). The heartbeat annoys (cut the turn-start reminder).
- **Measure:** the enemy-turn length in seconds before and after, on the same level. The added time should stay under +10%.

## USP check

- **Family Roles:** strengthens, a little. Role kills (Linda's shots, Mark's counter, Lucy's follow-up) get the kill beat, and the low-HP state makes John's shield role and Mark's protection matter visibly. No new rule.
- **Synergies:** strengthens, a little. The multi-kill scaling celebrates combo kills (Linda shooting into Lucy's cyclone) without a new mechanic.
- **Duos:** neutral, on purpose. Duo kills get the kill beat. The Duo's time-0 target pick is protected by the time-owner guard.
- **Managing the Home as a Family:** neutral, on purpose. HP carries over between levels (CR-24), so the low-HP state carries the run's damage forward. Tying it to the Home's Wounded state on `thj/home-test` is a later idea, not in scope.
- **Pillars:** the QTE pillar is protected by the time-owner guard. The family pillar and emotional narrative: screen-level dread is reserved for the family. The art pillar: all effects are sprite and UI, with no new post-processing.

## Critics

Not run. The size is M, and no `miso-design-critic` agent type is available in this session. If THJ wants one, the systems lens is the one to run (the time-scale owners).

## Acceptance criteria

- [ ] Hitting an enemy gives a stop of at most 0.14 s, a shake and a blink; a Bergson hit gives a shake and the red flash, with no stop.
- [ ] A kill gives a 0.12 s freeze, a white flash on the victim, a 0.3 s shake and a sting. An area attack that kills 3 gives one freeze and 3 flashes.
- [ ] No time effect plays during a QTE, a Duo pick, a role slow-mo or pause. At most 2 time effects play per second.
- [ ] A lower-tier shake never cuts a higher-tier one.
- [ ] Every unit shows a mini bar that hides while its info panel is up (Shift, hover, preview).
- [ ] Any damage preview at or above the target's HP shows the skull, including friendly fire on a Bergson.
- [ ] A Bergson that drops to 30% or below gets the crossing beat once and the quiet signals after; the vignette never stacks and survives a red hit flash.
- [ ] EditMode tests: the lethal rule (equal to HP counts as lethal); the low-HP crossing (only on crossing, not on every hit below the threshold); the priority and window arbitration; the fatigue cap. Kept as plain logic, so they can be tested without a scene.

## Scope

In: hit and kill time, camera and body feedback; the kill sting hook; mini HP bars; the lethal skull; the low-HP state, vignette, HUD glow, portrait tint and item-pouch bob.
Out: the Bergson death beat beyond "no enemy-kill beat" (CR-25 unchanged); a dynamic threshold (Option 3C); barks on low HP (a narrative follow-up); new post-processing; audio asset creation; the Home Wounded link.

## Touches

Systems: `GUnit` (core; no code change, prefab data on `UnitBase.prefab`, which holds the core death wiring), `GlobalEventBus` (core; listen only), `QuickTimeEventHandler` (core; listen only), `AbilityDamagePreview` (core; untouched, its rule mirrored in the panel), `TimeScaleCache` (existing protocol), `ShakeCameraEffect` and `FXRunner` (assets only), `EntityInfoPanelUI`, `UnitPanelUI` (new partial or child), new director, mini bar and low-HP presenter.
USPs: Family Roles, Synergies (light); Duos and Home neutral.
Docs: GDD combat rules (a new section), glossary (if THJ names the low-HP state).

## Risks

- **Core-system impact:** no public API change to any core system. `UnitBase.prefab` gets data edits next to the Inspector-wired `onMinReached → Die` (core-systems.md, "Damage and death" step 3). The editor script must touch only `hitEffects`, and goes in its own commit, flagged Tier 2. The lethal rule is duplicated in the panel; a test pins it to `PredictsLethalOn`.
- **Time-scale writers outside `TimeScaleCache`** (evidence 6): the guard skips rather than fights them. Moving those writers onto `TimeScaleCache` is a separate core-adjacent fix, not in this pass.
- **Enemy-turn pacing:** Bergson hits get no stop, and there's a fatigue cap; measure it as above.
- **Sorting:** mini bars against the CR-38 sword icons drawn above sprites, and against multi-tile footprints. Check in play.
- **Burn and push detection** for tier 7 may not be cheap. The fallback is tier 6.

## Gates

Compile / EditMode tests (all green except the known `AIRegressionTest.Baseline_MatchesCurrentAI`) / review / play check: **yes, it needs THJ's time**, because feel can't be judged in edit mode / docs to update (below).

## Questions for THJ

**Q1. Who owns hit-stop and shake?**
- Context: today every enemy carries its own slow-mo and shake from the prefab. A non-additive shake stops every running shake, and several systems set the time scale without telling each other (evidence 1, 4, 6).
- Options: A (retune and add a kill and crit director), B (one director owns all of it), C (kills only).
- Recommendation: **B.** About one editor script more than A, and it's the only one that can keep hit-stop out of QTEs.
- Blocked: the tech plan for steps 3 and 4.

**Q2. Mini HP bars on every unit, or only damaged ones?**
- Context: four playtesters asked for always-visible bars; the board already carries role zones, intent cells, threat arcs and sword icons.
- Options: A (always, every unit), B (damaged units plus all Bergsons), C (keep Shift-only).
- Recommendation: **A.** Thin, no number, hidden under any panel; fall back to B if it clutters.
- Blocked: step 2.

**Q3. Low-HP threshold?**
- Context: HP carries over with a 20% floor (CR-24), so a threshold above 20% puts floor-start members in the low state from turn 1. That's intended, but the cadence must not nag.
- Options: A (30%), B (25%), C (dynamic, "one enemy hit away").
- Recommendation: **A, 30%**, with C later.
- Blocked: step 5 and the low-HP test values.

**Q4. Should Bergson hits get a hit-stop too?**
- Context: today the Bergsons switch it off, so the enemy turn is never slowed. The plan stops only on crossing the low-HP threshold.
- Options: (a) no stop on Bergson hits, a stop on the crossing *(as planned)*; (b) the same light stop as enemy hits; (c) no stop at all on the Bergson side.
- Recommendation: **(a).** The crossing is the moment that matters; the other hits stay fast.
- Blocked: nothing; it's a value in the director.

**Q5. How loud is the screen heartbeat?**
- Context: Q24 suggested a "constant beating screen overlay". A constant loop at the 20% floor would run for whole levels.
- Options: (a) announce once (3 cycles), then one cycle on selection and at the start of each player turn *(lean)*; (b) constant while low; (c) no screen overlay, only the HUD and the bar.
- Recommendation: **(a).**
- Blocked: step 5.

**Q6. Should the lethal skull show when the target can evade?**
- Context: evasion cancels HP loss (CR-21); the damage preview already ignores crit and evasion.
- Options: (a) always show the skull, meaning "kills if it lands" *(lean)*; (b) a dimmed skull when the target has evasion above 0; (c) hide it when the target has evasion above 0.
- Recommendation: **(a).** Consistent with the existing damage preview; few units carry evasion.
- Blocked: nothing; step 1 can ship (a) and change later.

**Q7. Who supplies the three new sounds** (kill sting, low-HP sting, heartbeat) **and the skull sprite?**
- Context: these are assets, not code. The plan wires the hooks either way.
- Options: (a) THJ or the team sources them; (b) ship with placeholder sounds from the existing library and swap later.
- Recommendation: **(b)**, so the play check isn't blocked.
- Blocked: the audio part of the play check only.

## Docs to update if approved

- `design/gdd/combat-rules.md`: a new section, "Combat feedback", after "Grid previews and the Shift view", with rules **CR-44 onward**: the world/screen rule, the tier and priority table, the guards, the lethal skull, the mini bar, the low-HP threshold and cadence. Values are linked from here, not copied.
- `glossary.md` (narrative agent): only if THJ wants a player-facing name for the low-HP state. Don't reuse "Wounded", which is a Home term.
- `tech/core-systems.md`: no change (no core API touched). If the director becomes something combat depends on, the coordinator may list it.
- `design/demo-spec.md`: no change expected (no rule or number of the demo changes); the coordinator decides.
