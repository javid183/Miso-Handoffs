# Feedback pass: tech plan (kill beat, mini HP bars, low HP)

Size: M    Tier: 3 (game feel; design approved by THJ as D-146)    Assigned to: miso-implementer, one chunk at a time
Branch: all (built on `thj/quick-wins` @ `7d4cd90ca`, which holds bundle P; `main` is still at `fc731b0c5`; `thj/home-test` gets it when it takes `main`)
Status: approved design; tech plan written 2026-10-22, ready to dispatch C1

## Why

Bundle F of the quick-wins triage (Q5, Q6, Q24). Design: [`2026-10-20-feedback-pass-design.md`](2026-10-20-feedback-pass-design.md) **revision 2**, approved as written by THJ on 2026-10-22 (D-146; single heartbeat cycles kept, no kill beat on Toba). Earlier answers: D-113 (no time effects, bars on every unit, 25%, heartbeat once then quiet, placeholders), D-145 (kill flash and kill shake in, kill freeze out). The lethal skull and stepped preview are already built (bundle A).

## Goal

Kills get a white flash and a camera kick that nothing cuts, every unit shows a mini HP bar, and a family member at 25% HP or lower is announced once and then stays visibly hurt, with no added wait in the turn flow.

## Acceptance criteria

The design's list, per chunk below. Overall:

- [ ] An enemy or neutral kill: white flash on the victim (0.1 s hold, 0.1 s fade back to the material default), a 0.25 s camera shake at 0.05, a placeholder sting. A player-faction death (Bergsons, Toba): none.
- [ ] Kills while a kill shake runs step it up: 0.06, then 0.07 (cap). One sting per chain; one flash per victim.
- [ ] While a kill shake runs, no lower-priority shake (hit, ability, sequence) cuts it; with none running, every existing shake behaves as before.
- [ ] Every unit with a health bar in its info panel shows a mini bar, hidden while its info panel is up; a hit shows the damage chip (0.15 s hold, 0.25 s drain; a second hit extends it).
- [ ] Player-faction units: crossing to ≤ 25% gives the crossing beat once (sting, 3 heartbeat cycles 0.15 s later); healing above and dropping again repeats it; members starting a level low share one announcement at the first player turn, after the banner. Afterwards: mini bar pulse; on selection HUD glow, portrait tint and one cycle (at most once per member per player turn); one cycle at each player turn start while any member is low. The vignette never stacks, survives the red hit flash and pauses with the game.
- [ ] Enemy-turn length on a test level unchanged within 0.05 s.
- [ ] Compile clean; EditMode green except the known red `AIRegressionTest.Baseline_MatchesCurrentAI`; new logic tests listed per chunk.

## Scope

In: shake priority; kill-feedback component and three kill shake assets; mini HP bar and damage chip on `UnitBase.prefab`; low-HP state and presenter (vignette, heartbeat cadence, sounds, HUD glow, portrait tint, item-pouch bob); placeholder SFX.
Out: every time effect (hit-stop, kill freeze); any change to hit feedback (slow-mo, blink, hit shake, red flash, `hitEffects`); new Bergson or crit shakes; final art and audio; a player-facing name for the low state.

## Touches

Systems: `Core/FX/Runtime/CFX/ShakeCameraEffect.cs` and `CameraEffectBase.cs` (additive priority; not on the core-systems list, but in `Core/`, own commit); `GlobalEventBus` (listen only: `unitDied`, `turnStarted`); `GUnit` (read only: `GetMainVisual()`, `GetHealthAttribute()`, `isPlayerUnit`, `Faction`; **no code change**); `Features/_Common/Prefabs/UnitBase.prefab` (one new child; `hitEffects` and the death wiring untouched); `UnitPanelUI` (new partial); `UnitItemPouchButtonUI` (bob); new components and assets; `CombatLevelContainerScene.unity` (scene objects for the two presenters).
USPs: Family Roles and Synergies (light).
Docs: `design/gdd/combat-rules.md` new "Combat feedback" section (CR-44 on, game designer); `tech/pace-timings.md` kill-shake and feedback rows (coordinator); `tech/core-systems.md` only if `ShakeCameraEffect` is listed.

## What the code does now (read 2026-10-22, `thj/quick-wins` @ `7d4cd90ca`)

- **Shakes:** `ShakeCameraEffect.Apply` (`Core/FX/Runtime/CFX/ShakeCameraEffect.cs`) stops every coroutine in the static `CameraEffectBase.ActiveSCRs` unless `additive`, then starts its own. Finished coroutines stay in the list (never null), so `Count` checks are unreliable. `CameraEffectBase.ResetPlayModeState` is already called from `PlayModeStaticReset` (line 51). Played through `FXRunner.PlayCFX(effect)` (`Core/FX/Runtime/FXRunner.cs:77`). Hit shake: `Resources/UnitSpecific/Common/UnitHit_ShakeCameraEffect.asset` (0.2 s, 0.02, non-additive).
- **Death:** `GlobalEventBus.unitDied` (`UnityEvent<GUnit>`, line 49), fired from `GUnit.DieInternal` (`GUnit.cs:772`) and `FakeDie` (`:792`). On one unit the hit (blink, hit shake) fires before `unitDied` (design evidence 11).
- **Blink:** `GUnit.PlayHitBlink` (`:985`) tweens `mat.DOColor(hitBlinkTint, "_ColorOverride", …)` on `bodyVisual.material`; its `OnKill` restores the default. `GetMainVisual()` is public (`:845`). The default `_ColorOverride` is on `sharedMaterial`.
- **Info panel:** each unit has an `EntityInfoPanelUI` child on `UnitBase.prefab` (`entityInfoPanelUI`, prefab line ~2153); visible = its GameObject active (`Show` → `SetActive(true)`, `Hide` → `SetActive(false)`).
- **HUD:** `UnitPanelUI` (partial; `UnitPanelUI.RoleBadge.cs` is the pattern) tracks the selected unit's HP with `TrackHealthAttribute` and `UI_Element_FillBar` (`Features/UI/Panels/Scripts/Elements/UI_Element_FillBar.cs`); portrait `unitImage`. Item pouch: `UnitItemPouchButtonUI`.
- **Pause:** `CombatLevelRunHandler` sets `Time.timeScale = 0` for the pause menu (`:1014`); tutorials do the same. Slow-mo uses a time scale above 0.
- **Audio:** `AudioHandler.Instance.PlaySFX(string clipID)`; no pitch.

## Approach

Five chunks, one commit each (C4's tests with it). Riskiest first. **Each chunk is play-tested by THJ before its commit** (his flow since 2026-10-22).

### C1. Shake priority (Core/FX, `opus`)

- `ShakeCameraEffect`: `[SerializeField, Tooltip] int priority` (default 0). In `Apply`: if a shake with a **higher** priority is still running (its end time, in scaled time, not passed), skip this one entirely (no stop, no start). Otherwise behave exactly as today, and record this shake's priority and end time if it is now the highest running.
- Track the running priority and its end time in **new statics** on `ShakeCameraEffect` (or `CameraEffectBase`), cleared in the existing `CameraEffectBase.ResetPlayModeState`. Don't use `ActiveSCRs.Count`. Clear them in `Revert` too.
- Put the decision in a pure static (e.g. `ShouldSkip(int incoming, int runningPriority, float runningEnd, float now)`) with EditMode tests: lower skipped while running; equal and higher play; anything plays once the running one has ended; default 0 vs 0 always plays.
- Acceptance: no existing asset changes; with priorities all 0, behaviour is identical (play a level with Linda's shots and the Masher: shakes as before).

### C2. Kill feedback (`sonnet`)

- New `KillFeedbackPresenter` (Features side, e.g. `Features/Effects/KillFeedback/`), a scene component in `CombatLevelContainerScene` (and `TestLevel`), no statics. Subscribes to `GlobalEventBus.Instance.unitDied` in `OnEnable`, unsubscribes in `OnDisable`.
- **Kill rule** (pure static, tested): a kill if the unit is not null and not in the player's faction (`unit.Faction != CombatLevel.Instance.PlayerFaction`). Toba and Bergsons excluded by that.
- **Flash:** on `unit.GetMainVisual()`'s `material` (only if it has `_ColorOverride`): `DOTween.Kill(material)` (the blink's `OnKill` resets the colour), set `_ColorOverride` to white, hold 0.1 s, tween back to the `sharedMaterial` default over 0.1 s (scaled time). Serialized timings. If `DOTween.Kill(material)` doesn't stop the blink in practice, report it instead of touching `GUnit`.
- **Shake chain:** three new assets next to the hit shake (`Kill_ShakeCameraEffect` 0.05, `Kill2_` 0.06, `Kill3_` 0.07; 0.25 s; the hit shake's curve; non-additive; **priority 1**). Chain step = 0 when no kill shake is running, else min(step + 1, 2) (pure static, tested: 1st, 2nd, 3rd, 4th kill → 0, 1, 2, 2; resets after 0.25 s with no kill). Played via the camera's `FXRunner`/`CameraHandler` the way the hit shake is.
- **Sting:** placeholder SFX id, serialized, played once per chain (the first kill). Reuse an existing clip id; say which.
- Acceptance: the C2 criteria above; an area kill of 3 gives 3 flashes, 0.05 → 0.06 → 0.07, one sting.

### C3. Mini HP bar and damage chip (`opus`: prefab edit on the asset with the core death wiring)

- New `UnitMiniHealthBar` component on a new child of `UnitBase.prefab`, world-space, at the info panel's anchor, using `UI_Element_FillBar` (or a minimal equivalent), about 60% of the footprint's width (wider on multi-tile units), ~4 px tall at 1080p, 1 px dark outline, no text. Side colours: the info panel's own; list the colours in the report and check they don't clash with the role colours and Shift tints.
- Subscribes to the unit's HP attribute (the `UnitPanelUI.TrackHealthAttribute` pattern), unsubscribes on disable/destroy. Damage chip: hold 0.15 s, drain 0.25 s; a hit during the chip extends it.
- Hidden while the unit's info panel GameObject is active (serialized reference to the sibling `EntityInfoPanelUI`; poll in `LateUpdate` or hook its enable/disable without changing `EntityInfoPanelUI`'s API). Hidden when the unit is dead.
- Prefab diff: only the new child and its components. Check variants (enemies, bosses, multi-tile units, Toba) inherit it correctly and report sorting against the sword icons.
- Acceptance: every unit shows a bar; it hides under hover, Shift and preview; a hit shows the chip.

### C4. Low-HP state and presenter (`opus`)

- **State** on the mini bar, player-faction units only: low = alive and HP ≤ 25% of max. Crossing = from above to at or below. Pure static for the rule, tested (25% exact is low; only on crossing; heal above then drop re-crosses; dead isn't low). The bar raises a C# event `LowHealthChanged(unit, isLow, crossed)` (instance event, no static).
- **Presenter** `LowHealthPresenter`, scene component, no statics: finds the player faction's units at level start (and units that join later, e.g. on `turnStarted`), subscribes to their bars. Owns:
  - the vignette: a full-screen UI image on its own screen-space canvas (not a camera volume; design evidence 5), screen-edge red gradient, "lub-dub" (peaks 0.25 then 0.18, 0.12 s each, 0.15 s apart) in a 0.8 s cycle; never stacks (a cycle requested while one runs is dropped);
  - cadence: crossing → sting, then 3 cycles 0.15 s later; level start → members already low announced once together at the first player turn, after the banner; selection → one cycle, at most once per member per player turn; each player turn start → one cycle while any member is low. The caps as a pure tested function;
  - timing on **unscaled** time, but not advancing while `Time.timeScale == 0` (pause menu, tutorials);
  - placeholder sting and heartbeat SFX ids (reuse existing clips; say which).
- Mini bar pulse for low members: amber-red fill pulsing every 0.8 s (unscaled, same pause rule).
- Acceptance: the low-HP criteria above.

### C5. HUD glow, portrait tint, item-pouch bob (`sonnet`)

- New partial `UnitPanelUI.LowHealth.cs`: while the selected unit is low, the HP bar's outer glow pulses with the heartbeat and the portrait (`unitImage`) gets a bottom-up red tint (alpha 0.35); both clear when not low or another unit is selected.
- `UnitItemPouchButtonUI`: one bob (scale 1 → 1.15 → 1, 0.3 s) when a low member is selected and holds an HP-restoring item (find how items expose healing; report the check used).
- Acceptance: the HUD lines of the low-HP criteria.

## Risks

- **New statics** (C1's running priority and end time): cleared in `CameraEffectBase.ResetPlayModeState`, already called by `PlayModeStaticReset`.
- **AI thread:** nothing the AI reads changes. `AIRegressionTest` untouched.
- **Serialized fields:** only new ones; no renames. **Saves:** unchanged.
- **Prefab and scenes:** `UnitBase.prefab` gets one child (C3; check the diff touches nothing else, especially `hitEffects` and `onMinReached`). Scene objects for the two presenters (C2, C4): small diffs; Unity will also write any pending field values, list unrelated noise.
- **Events:** every subscription removed in `OnDisable`/`OnDestroy`; DOTween tweens killed on destroy (the flash's material tween, the chip, the pulses).
- **Hit slow-mo** still slows the scaled kill flash and shake on enemy hits (accepted in the design).
- **A sequence shake within 0.25 s of a kill is skipped** (priority 0 under 1). If it shows in play, give those assets priority 2.
- **Pacing:** nothing waits; check the enemy-turn length in play.
- **Other branches:** `thj/home-test` takes it with `main`.

## Gates

Per chunk: compile; EditMode (known red only); reviewer (C1 and C3 always; others too, they're new systems); **THJ's play test before each commit**; docs at the end (GDD section by the game designer, `pace-timings.md` and this plan's commit log by the coordinator).

## Commit log

(filled in as chunks are committed)

- C2: built (`reports/feedback-c2.md`; 10 tests; sting placeholder `A_SFX_John_ShieldImpact`; presenter re-binds when the level's bus appears), review APPROVE (`reports/feedback-c2-review.md`) with one should-fix applied (default colour read after the blink is killed), EditMode 545/546 (known red only). THJ play-tested it (looks good) and asked for slightly shorter and softer: flash 0.07 + 0.07 s, kill shakes 0.04/0.05/0.06 at 0.2 s (chain window 0.2 s), sting placeholder `A_SFX_Enemy_MasherGoblin_AttackImpact` (THJ's pick), then THJ chose **no sting** for now (empty id plays nothing). Committed `8d531ec64` on `thj/quick-wins`.
- C1: committed `07f4e44fe` on `thj/quick-wins` after THJ's play test (shakes look the same); built (`reports/feedback-c1.md`; 11 tests), review APPROVE (`reports/feedback-c1-review.md`; edge case for later: a priority-2 additive shake over a running priority-1 one), EditMode 535/536 (known red only).
