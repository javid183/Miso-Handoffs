# Feedback pass: kills, mini HP bars and low HP as one language

Size: M    Tier: 3 (game feel and a new readability feature are THJ's until 2026-10-29); answered in D-113 and D-145    Assigned to: miso-game-designer (design), then tech plan, then miso-implementer
Branch: all (builds on `thj/quick-wins`, which holds quick wins bundle A and bundle P; bundle P is not on `main` yet; nothing here differs by branch)
Status: ready for tech plan
Revision 2 (2026-10-22)

## Changelog

- **Revision 2 (2026-10-22)**, folding in THJ's answers:
  - **Cut (D-113):** all hit-stop and every time effect (enemy hits, Bergson hits, crits, the low-HP crossing stop, the kill freeze); the combat feedback director that owned them; the fatigue cap and the time-owner guard (nothing left to guard); the `UnitBase.prefab` editor script (the hit slow-mo and hit shake stay as they are). Also cut, because they only existed in the director's table: the new Bergson hit shake, the crit shake, the crossing shake, and the multi-kill sting pitch-up (`AudioHandler.PlaySFX` takes no pitch).
  - **Done (D-134 to D-136, bundle A, on `main`):** the lethal skull on every attack preview and the stepped HP preview. Removed from this plan's build list. Q6 (skull when the target can evade) was answered "show it" and is what bundle A built. The 2 Hz skull pulse from revision 1 was not built and is dropped: THJ play-checked the static skull and found picks clear (D-137).
  - **In (D-145):** the kill flash and the kill camera shake, owned by a small kill-feedback component plus a shake priority, with no director (Recommendation, decision 1).
  - **Settled (D-113):** mini HP bars on every unit; low HP at **25%** of max; the heartbeat announces once, then goes quiet; placeholder sounds and skull sprite.
  - **Re-tuned for bundle P's faster turns:** the kill shake is 0.25 s (was 0.3), the kill flash is 0.2 s in total, the damage chip is 0.4 s, and the "one heartbeat cycle on selection" now plays at most once per unit per player turn.
- Revision 1 (2026-10-20): first design; Q1 to Q7 to THJ.

## Why

Bundle F of the [quick-wins triage](2026-10-20-quick-wins-triage.md): playtest items **Q5** (juice top-up: Parsa, Oct build, still named hits and kills as the weak spot), **Q6** (always-visible mini HP bars, a lethal-hit preview, a low-HP warning; asked by Al, U, Y, J) and **Q24** (low-HP feedback, "should be designed"). Source text: [`playtests/2026-10-playtest-tasks.md`](../playtests/2026-10-playtest-tasks.md) lines 79, 80, 106. The lethal-hit preview part of Q6 shipped in bundle A ([tech plan](2026-10-21-quick-wins-a-tech.md), C3a).

## Goal

Kills land as a punctuation mark, every unit's HP reads at a glance, and a Bergson in danger is announced once and then stays visibly hurt, all without slowing the faster turns of bundle P or burying the Shift and preview layers.

## Problem and evidence

**Symptom (playtest):** hits and kills feel weak; HP is hard to read without hovering; nothing says "this one is about to die", on either side.

**Root problem:** kills have no feedback of their own, the shakes that exist cancel each other with no priority, and HP state lives only in hover panels. (Hits feeling weak is the hit-stop question, postponed by D-113.)

Evidence (revision 1 read `main` @ `08ca1d819`, 2026-10-20; revision 2 rechecked the marked items on `thj/quick-wins` @ `7d4cd90ca`, 2026-10-22):

1. **Hit slow-mo on every enemy, from `UnitBase.prefab` `hitEffects`** (slow-mo, blink, hit FX, unit volume, `UnitHit_ShakeCameraEffect`). Archer and both Claws also call `PlayHitSlowMo` directly. **Left as is:** D-113 postponed hit-stop, so this pass doesn't touch it.
2. **Bergsons have no hit slow-mo and no shake on hits**; their fourth `hitEffects` call is the red flash `PlayerHit_CameraVolumeEffect`. *John read line by line; the other four assumed to match.* **Left as is.**
3. **No kill feedback.** The death path (`onMinReached`, then `Die(1)`, then `DieInternal`, which fires `GlobalEventBus.unitDied` at once, `GUnit.cs:772-778`) has no flash or shake. *Rechecked 2026-10-22.*
4. **The shakes cancel each other.** `CameraEffectBase.ActiveSCRs` is **static** (`CameraEffectBase.cs:12`), and a non-additive `ShakeCameraEffect.Apply` stops every running shake (`ShakeCameraEffect.cs:21-27`). `UnitHit_ShakeCameraEffect` is non-additive (`additive: 0`, 0.2 s, magnitude 0.02). So if an area attack kills target 1 and then hits target 2, target 2's hit shake cuts target 1's kill shake. Eight other shake assets exist (Linda's shot and explosive arrow, the Masher, two Divine Relics, two Super Time, a Mark-intro altar); all would cut a kill shake the same way. *Rechecked 2026-10-22.*
5. **The screen volumes cancel each other** (static `_activeVolumes`, `VolumeCameraEffect.cs:30-37`): a held low-HP volume would be erased by the next red hit flash. So the heartbeat can't be a camera volume.
6. **Time-scale writers without a shared owner** (role slow-mo, Duo pick, Mark's catch, pause). Not this pass's problem any more: it adds no time effect.
7. **HP is readable only on hover, Shift or preview.** `EntityInfoPanelUI` has three modes and a one-slot queue (`_queueData`), so a mini bar can't be a fourth mode.
8. **Lethal skull and stepped preview: built** (bundle A, `EntityInfoPanelUI.ShowHealthMode` with `DamagePreviewRules.DecideLethalMark`, option `GlobalSettingsSO.displayLethalMarkPreview`). The rule ignores evasion, matching D-113. *Verified 2026-10-22.*
9. **No low-HP state anywhere.** The selected-unit HUD bar (`UnitPanelUI._healthBarFill`) tracks HP live. On `main` (FTP) the only HUD portrait is the selected unit's. *Assumed from `InitATBGaugeView` being ATB-only.*
10. **HP carries over with a 20% floor** (CR-24). At a 25% threshold, a member who starts a level at the floor starts it low.
11. **Event order on one unit (new, verified):** `RuntimeAAttribute.SetValue` fires `onValueDecreased` (line 75, which plays the hit: blink and hit shake) **before** `onMinReached` (line 82, which leads to `unitDied`). So on a kill, the victim's own blink and hit shake have already started when the kill feedback runs; the kill feedback replaces them in the same frame.
12. **Shake and camera focus compose (new, verified):** the shake writes the camera's `localPosition` (the child), while `CameraHandler` focus moves the handler's `transform.position` (`CameraHandler.cs:399-405`). A shake that's still running when the next enemy's focus pan starts doesn't fight it.
13. **Shake bookkeeping quirk (new, read, not run):** finished coroutines stay in `ActiveSCRs` (they're never null), so the "reset to the original position when the last shake ends" branch (`Count == 1`) only runs for the first shake of a session. It's harmless today because every curve ends at 0, but a priority change must not rely on `ActiveSCRs.Count`. For the tech plan.
14. **Kill flash access (verified):** `GUnit.GetMainVisual()` is public (`GUnit.cs:845`); the default `_ColorOverride` can be read from `sharedMaterial`, as `GUnit` does (`GUnit.cs:383-384`); the blink tween's `OnKill` restores the default colour (`GUnit.cs:1001`). *Assumed: `DOTween.Kill(material)` kills the blink, since a DOTween material shortcut targets the material.*
15. **Pacing after bundle P** ([`tech/pace-timings.md`](../tech/pace-timings.md)): AI hold after each action 0.25 s (real time), gap between faction turns 0.25 s, enemy turn-start pause 0.5 s after an automatic end, banner about 1 s, end-of-level waits 0.25 s, camera focus 0.5 s. *When "action completed" fires relative to the killing blow is not checked; assumed at or after it.*

## Lens notes

### Creative

**Target experience.** A kill should be a punctuation mark the player looks forward to. A Bergson in danger should feel like worry for *someone*, not a generic red screen: warmth against dread, as in Children of Morta, where the family's wounds are what you care about. Without hit-stop, the kill has to carry the "impact" alone, so it must be clearly bigger than a hit: a white flash and a camera kick no hit ever gets.

**The moment to design for.** Lucy is at 4 HP, her mini bar pulsing amber-red, a Black Claw two tiles away. The player picks Linda, hovers the Claw, and sees the skull (built). The arrow lands: the Claw goes white, the camera kicks, and it crumples. Seeing the kill coming, then the kill landing, then relief.

**The language, in one rule (unchanged):** *the world shows what the family does; the screen shows what happens to the family.* Kills on enemies stay in the world (sprite flash, camera kick). The screen (red flash, heartbeat vignette, HUD glow) belongs to Bergsons in danger.

### Systems

**Channels after revision 2:**

| Channel | Carries | Owner |
| --- | --- | --- |
| Time | hit slow-mo on enemies (unchanged) | prefab, as today. No new time effect (D-113) |
| Camera | hit shake (unchanged), ability shakes (unchanged), **kill shake** (new) | `ShakeCameraEffect` with a new **priority**; the kill shake is played by the kill-feedback component |
| Screen | red hit flash on Bergsons (unchanged), **heartbeat vignette** (new) | flash: prefab; vignette: low-HP presenter, its own UI canvas |
| Unit body | blink and hit FX (unchanged), **kill flash** (new) | kill flash: kill-feedback component |
| World UI | **mini HP bar**, damage chip, low-HP pulse | mini bar component |
| HUD | low-HP bar glow, portrait tint, item-pouch bob | low-HP presenter (`UnitPanelUI` partial or child) |
| Audio | hit SFX (unchanged), **kill sting**, **low-HP sting**, **heartbeat** (placeholders) | kill-feedback component; low-HP presenter |

**Shake priority (the fix for evidence 4, without a director).** `ShakeCameraEffect` gets an int `priority` (default 0, so every existing asset behaves as today). Rule: *an `Apply` whose priority is lower than a shake still running is skipped*; equal or higher behaves as today (non-additive stops the others). The running priority and its end time are tracked in their own static, not through `ActiveSCRs.Count` (evidence 13), and cleared in the existing `CameraEffectBase.ResetPlayModeState`. The kill shake assets get priority 1. Result: once a kill shake starts, no hit or ability shake can cut it; when it ends, everything is as today. Skipped, not queued: a late hit shake is noise after a kill.

**Kill rule.** A kill is a `unitDied` for a unit that is **not in the player's faction** (enemies, and Deer or other neutrals). A Bergson or Toba death keeps its own beat (CR-25) and gets no kill flash or kill shake. `FakeDie` (the Dom boss end) fires `unitDied` too and gets the kill beat; intended.

**Kill values** (scaled time, so pause stops them; matches the blink and shake today):

| Element | Value | Note |
| --- | --- | --- |
| Kill flash | `_ColorOverride` to full white at once, hold **0.1 s**, fade back to the default over **0.1 s** | Replaces the blink: kill the blink tween first (its `OnKill` resets the colour), then flash. Runs on top of the death animation, which starts at the same moment (no freeze any more) |
| Kill shake | `Kill_ShakeCameraEffect`: magnitude **0.05**, **0.25 s**, priority 1, the hit shake's curve shape | 0.25 s matches the AI hold after an action, so the next enemy's focus pan starts on a near-still camera (evidence 12, 15) |
| Extra kill | A kill while a kill shake is still running restarts the shake one step up: `Kill2_` 0.06, `Kill3_` **0.07 cap**, each 0.25 s, priority 1 | Three assets, because `baseMagnitude` is serialized with no setter; this avoids a code change for a runtime magnitude. Chain resets when no kill shake is running |
| Kill sting | Placeholder SFX, **once per chain** (the first kill), no pitch step | Pitch needs an audio API change; not worth it here |

**Area attack that kills several units:** one shake chain (stepped 0.05, 0.06, 0.07, then capped), one sting, **one flash per victim**, each on its own sprite. Worst case the chain runs about 0.25 s past the last kill (for kills in one frame it's exactly 0.25 s).

**Low HP (D-113: 25%, announce once then quiet).** Owned by the mini bar of each unit the player controls (the Bergsons, and Toba when he's in the party; *the tech plan confirms the faction check*). "Bergson" below means any of them:

- **Low** = alive and HP at or below **25%** of max. **Crossing** = the HP change took it from above 25% to at or below. Healing above 25% clears it; dropping again is a new crossing.
- **Crossing beat:** the existing red flash (from the hit), the low-HP sting, then **3 heartbeat cycles** of the vignette starting 0.15 s later.
- **Level start:** members who start at or below 25% (the 20% floor) count as one crossing, announced at the start of the first player turn, after the banner. One announcement whatever their number, one sting.
- **Quiet afterwards:** the mini bar's amber-red pulse; when that member is selected, the HUD bar glow, the portrait tint and **one** heartbeat cycle, **at most once per member per player turn**; at the start of each player turn, if any Bergson is low, one cycle.
- **Never stacks:** one vignette whatever the number of low members. A cycle requested while one is running is dropped.

*Reading of D-113:* "announces once, then goes quiet" is taken as revision 1's Option 3 cadence, which included the selection and turn-start single cycles. The per-turn cap on the selection cycle is new, because faster turns mean more re-selection. If THJ meant "silent" (no further heartbeat cycles at all), cut the two single-cycle triggers; nothing else changes.

**Levers and how they fail:**

| Lever | Too high | Too low |
| --- | --- | --- |
| Kill shake magnitude / length | nausea; runs into the next enemy's pan | a kill reads like a hit |
| Kill flash hold | hides the death animation's first frames | lost on fast deaths |
| Low-HP threshold (25%) | permanent alarm from the 20% floor | warning one hit late for low-HP Lucy |
| Heartbeat single cycles | noise the player tunes out | a member at low HP is forgotten after one turn |
| Mini bar size | clutter with role zones and sword icons (CR-38, CR-41 to CR-43) | unreadable |

**Interactions:**

- **Pacing:** nothing in this pass waits or holds the action flow; every effect is fire-and-forget. The turn length stays what bundle P set. Checked against [`pace-timings.md`](../tech/pace-timings.md): the kill shake (0.25 s) and flash (0.2 s) fit inside the AI hold (0.25 s); a player's last kill before an automatic end is followed by 0.1 s + 0.25 s gap + 0.5 s pause, so the shake is over before the enemy banner; a level-ending kill overlaps the 0.25 s before the HUD hides, and the shake's tail is near zero. The 2.4 s crossing announcement can run into the next banner; that's fine, it is on its own canvas and doesn't lock input.
- The hit slow-mo still runs on enemy hits (unchanged). It slows the scaled-time kill flash and shake for about 0.2 s when the killing blow is also a hit. Accepted: that's today's look, and hit-stop is THJ's later call.
- Family Role, Duo and Synergy kills all go through `unitDied`, so they get the kill beat with no extra rule.
- UI pulses, the vignette and the heartbeat run on **unscaled** time; a tutorial or pause that sets time to 0 must still pause them (the tech plan uses the pause state, not the time scale, for that).

### UX

**What the player sees, and when:**

| Moment | Shown | Not shown |
| --- | --- | --- |
| Idle on the board | A **mini HP bar** on every unit: no number, side colour. A Bergson at low HP: amber-red fill, pulsing every 0.8 s | Panels, skulls |
| Hovering a unit or holding Shift | The info panel **replaces** that unit's mini bar in the same spot | Both at once |
| Previewing an ability | The panel's damage segment, and the skull when it kills if it lands (**built**, bundle A) | Any camera effect |
| A hit lands | A white **damage chip** on the mini bar: hold **0.15 s**, drain over **0.25 s**; a second hit within that time extends the chip rather than restarting it | |
| A kill lands | White flash on the victim, camera kick, sting | |
| A Bergson crosses 25% | Red flash (existing), sting, 3 heartbeat cycles at the screen edges | A constant loop |
| Afterwards, while still low | Mini bar pulse; on selection the HUD glow, portrait tint and one cycle (once per turn); one cycle at each player turn start | |
| The low Bergson is selected and holds an HP-restoring item | The item-pouch button bobs once (scale 1 to 1.15 to 1, 0.3 s) | A bob when no HP item is held |

**Mini bar look:** about 60% of the footprint's width (wider on multi-tile units), about 4 px tall at 1080p, a 1 px dark outline, no text, at the info panel's anchor so the panel takes its place. Side colours: the info panel's own. *Still to confirm in the tech plan: which colours those are, and that they don't clash with the role colours or the Shift tints (CR-41 to CR-43).* Every unit with a health attribute that the info panel would show gets one.

**Heartbeat vignette:** a screen-edge red gradient (the hit-flash red), a "lub-dub" of two pulses (peak alpha 0.25 then 0.18, each 0.12 s, 0.15 s apart) in a 0.8 s cycle. A UI image on its own canvas (evidence 5).

**Portrait and HUD:** the portrait gets a red tint gradient from the bottom (alpha 0.35); the HUD health bar an outer glow pulsing with the heartbeat.

**Likeliest misreads:**

1. **"Skull = certain kill."** Settled by D-113: it means "kills if it lands", like the rest of the damage preview.
2. **Mini bar read as the role zone or the Shift tint.** Keep it off the tiles and its colours out of the tint table.
3. **A low-HP pulse on an enemy read as "about to die".** Low HP is family-only; enemies get no pulse.
4. **A kill shake read as a hit on the family.** The kill has no screen-level effect (no red), only the camera kick and the white flash on the enemy.
5. **Starting a level already low** and hearing the heartbeat at once: intended; announced once.

## Options compared

Revision 1's three decisions are answered (Q1 by D-113 and D-145; Q2 = always on; Q3 = 25%). One new decision is left, and it's an engineering-level one this plan settles.

### 1. Who owns the kill flash and kill shake, and how a kill shake survives later shakes

| | **A. Kill-feedback component + shake priority** *(lean)* | **B. Kill-feedback component + hit-shake relay** | **C. Kill-feedback component, no protection** |
| --- | --- | --- | --- |
| How | A scene component listens to `unitDied`, plays the flash and the stepped kill shake. `ShakeCameraEffect` gets an int `priority` (default 0); a lower one is skipped while a higher one runs | Same component; an editor script swaps the `UnitHit_ShakeCameraEffect` call in `UnitBase.prefab` `hitEffects` for a relay that skips while a kill shake runs | Same component; shakes stay as they are |
| Experience | A kill shake is never cut, by hits **or** ability shakes | Never cut by hits; still cut by Linda's shot, Masher and relic shakes | An area kill's shake is cut by the next target's hit (evidence 4) |
| Complexity | One rule on one asset type | A relay plus a prefab rewire | None |
| Cost | S: a small additive change in `Core/FX` plus assets | S–M: editor script on the prefab that holds the core death wiring | XS |
| Risk | Touches `Core/FX` (not on the core-systems list; default keeps today's behaviour); own commit | Edits next to `onMinReached → Die` on `UnitBase.prefab` | The bug the kill shake is most likely to hit |
| USP | Neutral | Neutral | Neutral |

**Lean: A.** It's the smallest change that covers every shake source, and it leaves `UnitBase.prefab` untouched now that the hit slow-mo stays. The kill flash needs no protection rule: per evidence 11 the blink starts before the kill, the flash kills it, and no later hit reaches a dead unit.

### 2. Multi-kill shake: restart stepped, or one shake after a window

| | **A. Play at once, step up on each extra kill while running** *(lean)* | **B. Wait a 0.1 s window, then one shake sized by the count** |
| --- | --- | --- |
| Experience | The first kill kicks with no delay; extra kills hit harder | 0.1 s late on every kill, even single ones |
| Cost | Three assets | One asset plus a runtime magnitude (needs a setter) |

**Lean: A.** "While a kill shake runs" is the window, so no separate timer is needed, and it works for area damage spread over a few frames.

## Recommendation

**Build A and A**, with the values in the Systems table. The build order (suggested commit order):

1. **Shake priority** (`Core/FX/Runtime/CFX/ShakeCameraEffect.cs`, own commit, flagged Tier 2 as `Core/` code): int `priority`, default 0; skip a lower `Apply` while a higher one runs; track the running priority and end time in a static reset by `CameraEffectBase.ResetPlayModeState`. EditMode test of the rule as plain logic.
2. **Kill feedback.** A scene component in the combat scene (proposed name `KillFeedbackPresenter`; no static state), listening to `unitDied`. Applies the kill rule, the flash (`GetMainVisual().material`, kill the blink tween, white, hold, fade) and the shake chain; plays the placeholder sting once per chain. New assets: `Kill_`, `Kill2_`, `Kill3_ShakeCameraEffect` (priority 1).
3. **Mini HP bar.** A world-space component on `UnitBase.prefab` (a child object and component, not a `hitEffects` edit), using `UI_Element_FillBar`, subscribed to the HP attribute (the `UnitPanelUI.TrackHealthAttribute` pattern). Hides while the unit's info panel is up. Damage chip via the decrease fill. For Bergsons, owns the low state and raises `LowHealthChanged(unit, isLow, crossedThisHit)`.
4. **Low-HP presenter.** Vignette canvas (unscaled, respects pause), heartbeat cadence and its caps, the `UnitPanelUI` glow and portrait tint (new partial or child), the item-pouch bob, the low-HP sting and heartbeat (placeholders).

**Playtest signals:**

- **It worked:** testers mention kills feeling good without being asked; they hover or hold Shift less to check HP; they heal or retreat a low member within a turn of the announcement.
- **It failed:** "the camera is shaky" on area kills or busy enemy turns (lower the step to 0.055/0.06 cap, or the length to 0.2 s); a kill still reads like a hit (raise to 0.06 base); the board looks busy (fall back to bars on damaged units plus all Bergsons, a setting flip); the heartbeat annoys (cut the turn-start cycle).
- **Measure:** the enemy-turn length on the same level before and after: it should not change (this pass adds no wait).

## USP check

- **Family Roles:** strengthens, a little. Role kills (Linda's shots, Mark's counter, Lucy's follow-up) get the kill beat; the low-HP state makes John's shield and Mark's protection visibly matter.
- **Synergies:** strengthens, a little. The stepped multi-kill shake celebrates combo kills (Linda shooting into Lucy's cyclone).
- **Duos:** neutral, on purpose. Duo kills get the kill beat; with no time effect, the Duo's time-0 pick needs no guard.
- **Managing the Home as a Family:** neutral, on purpose. HP carries over (CR-24), so the low state carries a run's damage forward; a link to the Home's Wounded state stays out of scope.
- **Pillars:** the QTE pillar is safe (no time effect at all now); screen-level dread stays reserved for the family; all effects are sprite and UI, no new post-processing.

## Critics

Not run. M size, and the hardest systems question (time ownership) left the pass with D-113.

## Acceptance criteria

- [ ] An enemy kill gives a white flash on the victim (0.2 s in total), a 0.25 s camera shake at 0.05 and the placeholder sting; a Bergson or Toba death gives neither.
- [ ] An area attack that kills 3 gives 3 flashes, one stepped shake chain (0.05, 0.06, 0.07) and one sting; a fourth kill stays at 0.07.
- [ ] While a kill shake runs, no hit shake or ability shake cuts it; with no kill shake running, every existing shake behaves as before.
- [ ] The kill flash replaces the victim's blink: no blink colour shows after the flash, and the colour ends at the material's default.
- [ ] The enemy-turn length on a test level is unchanged within 0.05 s (no added wait).
- [ ] Every unit shows a mini bar that hides while its info panel is up (Shift, hover, preview); a hit shows the damage chip.
- [ ] A Bergson that drops to 25% or below gets the crossing beat once; later hits while low don't repeat it; healing above 25% and dropping again repeats it. Members starting a level low get one announcement at the first player turn.
- [ ] The vignette never stacks, survives a red hit flash, pauses with the game, and the selection cycle plays at most once per member per player turn.
- [ ] EditMode tests (plain logic): the shake priority rule; the kill rule (faction filter) and the chain step and cap; the low-HP crossing (only on crossing; 25% exact counts as low; heal-then-drop re-crosses); the heartbeat caps. Every test passes except the known `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: kill flash, kill shake chain and the shake priority; kill sting hook; mini HP bars and the damage chip; the low-HP state, crossing beat, vignette, heartbeat cadence, HUD glow, portrait tint and item-pouch bob; placeholder sounds.
Done already (bundle A): the lethal skull and the stepped HP preview.
Out: every time effect, including hit-stop and the kill freeze (D-113, D-145); any change to hit feedback (slow-mo, blink, hit shake, red flash); new Bergson or crit shakes; the Bergson death beat beyond "no kill beat" (CR-25 unchanged); a dynamic "one hit away" threshold; low-HP barks; new post-processing; final audio and skull art.

## Touches

Systems: `ShakeCameraEffect` / `CameraEffectBase` (`Core/FX`, additive priority; not on the core-systems list), `GlobalEventBus` (listen only), `GUnit` (no code change; reads `GetMainVisual()` and the HP attribute), `UnitBase.prefab` (adds the mini bar child only; `hitEffects` and the death wiring untouched), `EntityInfoPanelUI` (the mini bar hides when it shows; may need a small "panel visible" signal), `UnitPanelUI` (new partial or child), new kill-feedback, mini bar and low-HP presenter components, new shake assets.
USPs: Family Roles and Synergies (light); Duos and Home neutral.
Docs: GDD combat rules (new section), glossary only if THJ names the low-HP state.

## Risks

- **Core-adjacent change:** the shake priority is in `Core/FX`. Default 0 keeps today's behaviour; its own commit so it can be reverted alone. It must not use `ActiveSCRs.Count` (evidence 13).
- **`UnitBase.prefab`:** adding a child object is a prefab edit on the asset that holds the core death wiring. The tech plan keeps it to the new child and checks the diff touches nothing else.
- **Hit slow-mo stretching kills:** the unchanged enemy-hit slow-mo slows the scaled kill flash and shake for about 0.2 s. Accepted; revisit with hit-stop.
- **Action completion timing** (evidence 15, assumed): if an ability's "completed" fires well after the kill, the kill shake ends even earlier relative to the next pan; if it fires before, the shake overlaps the pan's start, which composes (evidence 12). Check in play.
- **Sorting:** mini bars against the CR-38 sword icons and multi-tile footprints. Check in play.
- **A sequence shake skipped:** a Super Time or cutscene shake (priority 0) that starts within 0.25 s of a kill is skipped. Unlikely; if it shows, give those assets priority 2.

## Gates

Compile / EditMode tests (all green except the known `AIRegressionTest.Baseline_MatchesCurrentAI`) / review / play check: **yes, THJ plays it**, because feel can't be judged in edit mode / docs to update (below).

## Questions for THJ

None blocking. Calls this revision makes on its own, which THJ can overrule at the play check:

- **Recommend keep the single heartbeat cycles (on selection, once per turn; at each player-turn start);** cut both if "goes quiet" meant no heartbeat at all after the announcement. Blocks nothing; two triggers to drop.
- **Recommend no kill beat on Toba's death** (treated like a Bergson's). Blocks nothing; a faction filter.

## Docs to update if approved

- `design/gdd/combat-rules.md`: a new section, "Combat feedback", after "Grid previews and the Shift view", rules **CR-44 onward**: the world/screen rule; the lethal skull and stepped preview (*Built*, D-134 to D-136, not yet in the GDD); the kill beat and the shake priority; the mini bar; the low-HP threshold (25%) and cadence. A line under "Deferred and dropped": hit-stop and all time effects postponed (D-113). Values are linked from here, not copied.
- `tech/pace-timings.md` (coordinator): a row for the kill shake (0.25 s, fire-and-forget, does not hold the turn).
- `glossary.md` (narrative agent): only if THJ wants a player-facing name for the low-HP state; not "Wounded" (a Home term).
- `tech/core-systems.md`: no change unless the coordinator lists `ShakeCameraEffect` after the priority change.
- `design/demo-spec.md`: no change expected; the coordinator decides.
