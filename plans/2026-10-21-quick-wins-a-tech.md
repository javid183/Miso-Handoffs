# Quick wins bundle A: plain fixes (tech plan)

Size: M    Tier: mixed (per chunk; questions W5 to W8 below)    Assigned to: miso-implementer (one chunk per run)
Branch: all (built on a `quick-wins` branch THJ creates from `main` @ `df58c4c0c`, D-111)
Status: waiting on THJ (W8: shield animation approach); W5 to W7 answered (D-130 to D-132)

## Why

Playtest Batch 3 quick wins (`playtests/2026-10-playtest-tasks.md`), triaged in `plans/2026-10-20-quick-wins-triage.md` (bundle A). THJ's answers: D-107 to D-111. Code facts re-checked on `main` @ `df58c4c0c` by Explore on 2026-10-21; two triage premises were wrong and are corrected here (Q14 grid fade, Q22 fold timer).

## Goal

Seven small, independent fixes, each its own chunk and commit: one-click cancel, Lucy's target counter, objectives summary, John's shield idle, enemy idle desync, Mark's hit sound, Workshop cleanup and the M1 grid fade.

## Acceptance criteria

- [ ] **Q9:** with a unit selected and an ability armed, one right-click returns to unit selection with no range shown. During multishot target picking, a right-click removes the last picked target (D-130). Right-click does nothing during a QTE, a Family Role prompt, the level intro, or while another faction is acting.
- [ ] **Q10:** while picking targets for any multi-target ability (Lucy's Primary Attack, Mark–Lucy Duos, Dom's Swap, Mark's Command), a label over the counter reads "Target n/N" (n = the target being picked next, N = required count); for Lucy, N equals her orb count at the ability's level (2 to 7). The label updates on pick and undo and hides with the pips.
- [ ] **Q22:** after the objectives panel folds, a one-line summary stays visible showing the first objective that is not yet satisfied; hovering still expands the full list; the line is hidden while expanded and when every objective is satisfied.
- [ ] **Q12:** while John has `Status.ShieldUp` and is idle, he plays the shield-idle pose (the `John - Ability - InStand - *` sheets, D-109) facing the right way in all three directions; when the shield ends he returns to the normal idle at his next idle. Other animations (attacks, hit, walk) are unchanged and still return to the right idle. No new animator transitions or parameters.
- [ ] **Q17:** every enemy unit's idle starts at a spread-out phase (no two neighbours in lockstep at level start) and runs at a small per-unit speed variance (±7 %, constant per unit). Players are unchanged. Pause/Resume and the QTE pause still freeze and restore the speed correctly.
- [ ] **Q15:** no Lucy sound plays on Mark: hit = `A_SFX_John_Hit`, Command and Cleanse use John's sounds, Walk keeps only footsteps (D-132).
- [ ] **Q14 (b):** the two shared Workshop items (`Equipment_Shin Armor`, `Equipment_Vitality Brooch`) no longer appear in the Workshop on a fresh save.
- [ ] **Q14 (a):** after M1 level 2 (`Level1C1-2`) ends, the grid stays faded out through the end of that level; the next level shows it as usual (D-131).
- [ ] Compile clean; EditMode suite green except `AIRegressionTest.Baseline_MatchesCurrentAI` (unchanged, not re-baselined).

## Scope

In: the items above.
Out: Q13 (skipped, D-110); Q11 legend/reveal; the dead `ObjectivesPanelUI.InitialWait` (left as is, noted); the ally-near-enemy mis-targeting half of Q9 (needs a repro first); a real Mark audio set; re-enabling the Hidden filter in the character equipment panel (`CharacterSelect_EquipmentsPanelUI.cs:84`, commented out on purpose or not: unknown, not touched).

## Touches

Systems: faction controllers `PlayerController.cs` **(core, private change, no API change: Tier 2)**; `UnitBase.prefab` **(core-listed for its `onMinReached` → `GUnit.Die` wiring; adding a child object only)**; `TargetSelectCounterUI`, `ObjectivesPanelUI` / `ObjectiveEntryUI` and their prefabs; `EntityAnimationHandler` (not core-listed; additive); `JohnShieldRelay`; `AC_Playable_John.controller` (new state, no transitions); enemy unit prefabs; `Unit_Mark.prefab`; two equipment assets; one M1 sequence asset.
USPs: none directly (Q12 is John's shield, not his Family Role).
Docs: `build-log.md`; `tech/combat-architecture.md` (cancel behaviour, idle variance); `design/gdd` combat UI page if it describes cancel or objectives (designer to check); `status.md`.

## Approach

Chunks, riskiest first. One implementer run and one commit each. Paths under `miso/Assets/_Project/`.

### C1. Q9 one-click cancel (opus; core)

- `Core/Interactions/Runtime/PlayerController.cs:117`: replace `_inputController.OnCancel += () => GoBackToPreviousState();` with a named `OnCancelInput()` handler (subscribe/unsubscribe symmetrically).
- Early return when any of: `IntroductionInProgress`, `QuickTimeEventHandler.IsEventActive`, `PhaseData.IsInProgress`, `!_reactiveInterrupt && OtherFactionActionInProgress()`.
- (D-130) If the current state is `TargetSelectionState` with `TargetCells.Count > 0`: one `GoBackToPreviousState()` (undo the last pick). Otherwise `while (GoBackToPreviousState()) ;` (the existing full-deselect pattern, e.g. `:564`), which stops at `UnitSelectionState` (its `GetPreviousState` is null).
- Put the decision in a small pure static helper (e.g. `CancelInputRules.Decide(bool blocked, bool pickingWithTargets) → None | StepOnce | ToUnitSelection`) with EditMode tests; no state in it.
- Check by reading: the reactive-interrupt path (`:776-780`), the approach-attack pending fields cleared by the existing per-state `Cancel()`, and `TakeActionState.CancelCondition = false` (mid-action cancel stays a no-op).

### C2. Q12 John's shield idle (opus; animation)

Follows THJ's rule: states are played by name through `EntityAnimationHandler`; no new transitions or parameters.

- Clips: duplicate the three looping `Idle/A_Playable_John_Action_Idle_Weapon_{Down,Side,Up}.anim` as `A_Playable_John_Idle_Shield_{Down,Side,Up}.anim` and point their sprite curves at the sliced `John - Ability - InStand - {Down,Side,Up}.png` sprites `_0` to `_7` (D-109). Frame rate: keep the Weapon clips' (7/9/7 fps) unless the frame count differs; if the sprite mapping is ambiguous, stop and ask THJ to assign them (D-109).
- Controller `Features/Player/John/Art/Animations/AC_Playable_John.controller`: add a state `IdleShield` whose motion is a 2D blend tree on the existing `DirectionX`/`DirectionY`, built like the `Idle` state's tree (`:712`). No transitions. Prefer an editor script or the Animator API over hand-written YAML for the blend tree; delete the script after if it is one-off.
- `EntityAnimationHandler`: additive `SetIdleState(string stateName)` that swaps the idle state name used when a clip ends and by `Stop()`; if the unit is idle right now, play the new idle immediately. Default unchanged.
- `Features/Player/John/Scripts/JohnShieldRelay.cs`: subscribe to `_unit.TagSet.OnTagGained/OnTagRemoved` (unsubscribe in `OnDisable`/`OnDestroy`); on a change of `IsShieldUp` call `SetIdleState(IsShieldUp ? "IdleShield" : "Idle")`. Guard with `HasState("IdleShield")` so a missing state never breaks idle.

### C3. Q10 Lucy's target counter (sonnet)

- `Features/UI/Panels/Scripts/TargetSelectCounterUI.cs`: optional `[SerializeField] TMP_Text label` (null-safe). In `Populate`, `CountUp`, `CountDown`: `label.text = FormatLabel(picked, total)`; hidden with the pips in `Reset`/hide. `FormatLabel` is a pure static: "Target n/N" with n = picked + 1 clamped to N. EditMode test for it.
- `Features/_Common/Prefabs/UnitBase.prefab`: add a TMP child under the `TargetSelectCounter` world-space canvas, above the pips, and wire `label`. Additive child only; do not touch the attribute wiring. Use the project's existing world-space font/material.
- No `PlayerController` change (the counter already gets `RequiredTargetCount`).

### C4. Q22 objectives summary (sonnet)

- `Features/UI/Panels/Scripts/ObjectivesPanelUI.cs`: add `[SerializeField] TMP_Text collapsedSummary` placed outside the Mask. In `Shrink()`: set it to the first entry whose objective is not `Satisfied` and show it (hide if none). In `Expand()`: hide it. `ObjectiveEntryUI` gets a read-only `Objective` getter. The pick is a pure static (`FirstActive(IReadOnlyList<LevelObjective>)`) with an EditMode test.
- `Features/UI/Panels/Prefabs/UI/ObjectivesPanel.prefab`: add the TMP line (same style as `objectiveText`, one line, ellipsis overflow).

### C5. Q17 enemy idle desync (sonnet)

- `EntityAnimationData` / `EntityAnimationHandler`: when `randomizeStartFrame` is on, the start phase comes from a golden-ratio sequence instead of `Random.value`: `phase = frac(seed + i × 0.618034)`. The index `i` is a per-handler counter **stored as a static** → add `ResetPlayModeState()` on the class and call it from `Core/Managers/PlayModeStaticReset.cs` `Reset()`. A random seed per level start is fine.
- Speed jitter: an opt-in serialized `idleSpeedJitter` (default 0); when > 0, a per-unit factor in `[1 − j, 1 + j]` is rolled once in `Initialize` and applied as the handler's default speed, so `Pause`/`Resume` restore it (they use `_defaultAnimatorSpeed`).
- Data: enemy unit prefabs get `randomizeStartFrame: 1` and `idleSpeedJitter: 0.07`: Archer, Dark Claw (Black Claw inherits), Dark Shaman, Masher, Goblin Queen, Dark Worm, Deevoted, Deev. `UnitBase.prefab` and players unchanged.
- EditMode test for the phase sequence helper (pure static) and for the jitter range.

### C6. Q15 Mark's hit sound (sonnet; data)

- `Features/Player/Mark/Prefabs/Unit_Mark.prefab:2412`: `A_SFX_Lucy_Hit` → `A_SFX_John_Hit` (the HP `onValueDecreased` PlaySFX call).
- D-132: `:2532` `A_SFX_Lucy_Dedication` (Cleanse, ability [4]) → the ID John's own Cleanse slot uses (read `Unit_John.prefab`; it has `A_SFX_John_Dedication` and `A_SFX_Generic_Cleanse` on its Cleanse-family slots, pick the one on `CleanseAbility.asset`); `:2528` `A_SFX_Lucy_Decoy` (Command) → `A_SFX_John_Attack`; `:2504` `A_SFX_Lucy_FireShoot` (Walk event 0, before three `A_SFX_Generic_Footstep`) → removed if John's Walk has no start sound, else John's. Report the final mapping (Tier 2).

### C7. Q14 (b) Workshop shared items (sonnet; data)

- `Resources/Unit Equipments/Shared/Equipment_Shin Armor.asset` and `Equipment_Vitality Brooch.asset`: `equipmentState: 2` → `0` (Hidden). `WorkshopPanelUI.cs:129-133` already filters Hidden. Saved states override the asset (`EquipmentManager.GetState`), so an existing save that owns them still shows them: acceptable for a demo cleanup; say so in the report.

### C8. Q14 (a) M1 grid fade (sonnet; data)

Correction: `FadeOutGridSequence.asset` is not unused; every `IntroCutscene` fades the grid out and every `OutroCutscene` fades it back in. M1's second level is `Level1C1-2` ("John's Map (2/3)"): start = [IntroCutscene, Start_Dialog, Start_Camera, `Level1C1-2_TutorialSequence`, OutroCutscene]; end = [IntroCutscene, End_Dialog, OutroCutscene]. Asset-only edit (D-131): in `Resources/Sequences/Mission 1/Level1C1/Level1C1-2_End_SequenctialSequence.asset`, replace the final `OutroCutscene` with a sequence that restores input and the HUD but not the grid (a new `OutroCutsceneNoGrid` = [EnablePlayerInput, ShowHUD], or the two entries inline). Check the next level's own intro/outro still fades the grid back in, and that nothing between level end and the next level needs the grid.

## Risks

- **Statics:** C5 adds one static counter → `PlayModeStaticReset` hook (above). No other new statics; C1 reads the existing `QuickTimeEventHandler.IsEventActive`.
- **AI:** none of this is read by the AI. `AIRegressionTest` should not move; if it does, stop and report (no re-baseline).
- **Serialized renames:** none; new fields only.
- **Saved data:** none. C7's asset change doesn't migrate saved equipment states (noted).
- **Assets/prefabs:** small YAML edits; C2's blend tree via an editor script or the Animator API. `UnitBase.prefab` (C3) is the base of every unit: add the child only, check one player and one enemy still die and show the counter.
- **Subscriptions:** C1 handler and C2 tag events unsubscribe on disable/destroy.
- **Animation rule:** C2 adds a state but no transitions or parameters, played by name (THJ's rule).
- **Other branches:** `thj/home-test` gets all of this when it takes `main`.

## Gates

- Compile; EditMode suite (known red only) after each chunk.
- Reviewer: C1 (core) and C2 (animation + handler API); others on request.
- Play check (THJ's time: yes, one session at the end): cancel in each state and during a role prompt; Lucy's label at two ability levels; objectives line; John shield idle in three directions; enemies' idle spread; Mark hit sound; Workshop on a fresh save; M1 level 2.
- Docs: `build-log.md`, `tech/combat-architecture.md` (cancel, idle variance), `status.md`.

## Questions for THJ

- W5 to W7: answered 2026-10-21 (D-130 to D-132).
- **W8 (Q12):** confirm the approach: a new `IdleShield` state played by name via an additive `EntityAnimationHandler.SetIdleState`, no transitions.

## Commit log

(filled as chunks land)
