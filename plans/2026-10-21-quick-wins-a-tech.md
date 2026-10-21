# Quick wins bundle A: plain fixes (tech plan)

Size: M    Tier: mixed (per chunk; questions W5 to W8 below)    Assigned to: miso-implementer (one chunk per run)
Branch: all (built on `thj/quick-wins`, created by THJ from `main`, D-111)
Status: approved 2026-10-21 (W5 to W8: D-130 to D-133); in progress

## Why

Playtest Batch 3 quick wins (`playtests/2026-10-playtest-tasks.md`), triaged in `plans/2026-10-20-quick-wins-triage.md` (bundle A). THJ's answers: D-107 to D-111. Code facts re-checked on `main` @ `df58c4c0c` by Explore on 2026-10-21; two triage premises were wrong and are corrected here (Q14 grid fade, Q22 fold timer).

## Goal

Seven small, independent fixes, each its own chunk and commit: one-click cancel, Lucy's target counter, objectives summary, John's shield idle, enemy idle desync, Mark's hit sound, Workshop cleanup and the M1 grid fade.

## Acceptance criteria

- [ ] **Q9:** with a unit selected and an ability armed, one right-click returns to unit selection with no range shown. During multishot target picking, a right-click removes the last picked target (D-130). Right-click does nothing during a QTE, a Family Role prompt, the level intro, or while another faction is acting.
- [ ] **Q10:** while picking targets for any multi-target ability (Lucy's Primary Attack, Mark–Lucy Duos, Dom's Swap, Mark's Command), a label over the counter reads "Target n/N" (n = the target being picked next, N = required count); for Lucy, N equals her orb count at the ability's level (2 to 7). The label updates on pick and undo and hides with the pips.
- [ ] **Q22:** after the objectives panel folds, a one-line summary stays visible showing the first objective that is not yet satisfied; hovering still expands the full list; the line is hidden while expanded and when every objective is satisfied.
- [ ] **Q12 (D-133):** while John has `Status.ShieldUp`, his idle, run and primary attack play `Idle_Shield`, `Run_Shield` and `PrimaryAttack_Shield`, facing the right way in all three directions; a shield gained while idle swaps the pose at once, otherwise at the next animation; when the shield ends he goes back to the normal states. States without a `_Shield` version (hit, Shield Dash, ...) play as before. The primary attack's hit still lands on its activation frame (no freeze). No new animator transitions or parameters.
- [ ] **Q17:** every enemy unit's idle starts at a spread-out phase (no two neighbours in lockstep at level start) and runs at a small per-unit speed variance (±7 %, constant per unit). Players are unchanged. Pause/Resume and the QTE pause still freeze and restore the speed correctly.
- [ ] **Q15:** no Lucy sound plays on Mark: hit = `A_SFX_John_Hit`, Command and Cleanse use John's sounds, Walk keeps only footsteps (D-132).
- [ ] **Q14 (b):** the two shared Workshop items (`Equipment_Shin Armor`, `Equipment_Vitality Brooch`) no longer appear in the Workshop on a fresh save.
- [ ] **Q14 (a):** after M1 level 2 (`Level1C1-2`) ends, the grid stays faded out through the end of that level; the next level shows it as usual (D-131).
- [ ] Compile clean; EditMode suite green except `AIRegressionTest.Baseline_MatchesCurrentAI` (unchanged, not re-baselined).

## Scope

In: the items above.
Out: Q13 (skipped, D-110); Q11 legend/reveal; the dead `ObjectivesPanelUI.InitialWait` (left as is, noted); the ally-near-enemy mis-targeting half of Q9 (needs a repro first); a real Mark audio set; re-enabling the Hidden filter in the character equipment panel (`CharacterSelect_EquipmentsPanelUI.cs:84`, commented out on purpose or not: unknown, not touched).

## Touches

Systems: faction controllers `PlayerController.cs` **(core, private change, no API change: Tier 2)**; `UnitBase.prefab` **(core-listed for its `onMinReached` → `GUnit.Die` wiring; adding a child object only)**; `TargetSelectCounterUI`, `ObjectivesPanelUI` / `ObjectiveEntryUI` and their prefabs; `EntityAnimationHandler` (not core-listed; additive state variant, D-133); `JohnShieldRelay`; `AC_Playable_John.controller` (THJ's new states; not edited); enemy unit prefabs; `Unit_Mark.prefab`; two equipment assets; one M1 sequence asset.
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

### C2. Q12 John's shield variants (opus; animation)

Follows THJ's rule: states are played by name through `EntityAnimationHandler`; no new transitions or parameters (D-133).

- Art is done by THJ (`3ae174a93`): states `Idle_Shield`, `Run_Shield`, `PrimaryAttack_Shield` in `Features/Player/John/Art/Animations/AC_Playable_John.controller` (blend trees on the existing `DirectionX`/`DirectionY`), clips `A_Playable_John_{Idle,Run}_Shield_*`, `A_Playable_John_Shield_PrimaryAttack_*`. Do not edit the controller or the clips.
- `Core/Animation/EntityAnimation/Runtime/EntityAnimationHandler.cs`: additive `SetStateVariant(string suffix)` / `ClearStateVariant()` (suffix like `"_Shield"`). In the single place that resolves a state name before `animator.Play` (`Play`, around `:208-210`), use `stateName + suffix` when a suffix is set and `HasState(stateName + suffix)`, else `stateName`. `_targetStateName` must hold the resolved name so `HandleFrameAction` / `_playReady` and `IsPlaying` keep working; `IsPlaying(stateName)` should answer true for either name. On a variant change while the current state is the idle (resolved or not), replay the idle so the pose swaps at once; otherwise the change applies at the next `Play`. Cache the `HasState` result per name if it shows in profiling (not required).
- `Features/Player/John/Scripts/JohnShieldRelay.cs`: subscribe to `_unit.TagSet.OnTagGained/OnTagRemoved` (unsubscribe in `OnDisable`/`OnDestroy`); when `IsShieldUp` changes, `SetStateVariant("_Shield")` or `ClearStateVariant()`. Also clear on death and level end.
- Check frame timing: for `PrimaryAttack`, compare the ability's activation frame with each `A_Playable_John_Shield_PrimaryAttack_*` clip's frame count. If any shielded clip ends at or before the activation frame (the known freeze, `EntityAnimationHandler.cs:97-100`), stop and report instead of shipping.
- EditMode test: the resolve rule as a pure static (`ResolveStateName(name, suffix, hasState)`).

### C3 (revised 2026-10-21, D-134): multi-target clarity, split in three

THJ's playtest read: while picking several targets, the hover preview shows *confirmed picks + this click* in one colour, and picked targets lose their preview when the cursor leaves, so mid-volley an enemy can look "dead" when it still needs one more click. Facts (Explore 2026-10-21): `PlayerController.ShowDamagePreview` (`:1489-1502`) → `AbilityDamagePreview.ComputeFor(ability, unit, hovered, TargetCells)`; with `oneEffectPerTarget` it maps `effects[i]` to `picks[i]` = committed cells + the hovered cell (`AbilityDamagePreview.cs:27-59`); `ComputeFor(..., hovered: null, TargetCells)` gives the confirmed part. `OnMoveHoverPreview` clears every preview first and returns early for hover-out / out of range / empty cell (`:988-993`, `:1009`). The bar is `EntityInfoPanelUI.ShowHealthMode` (`:55-79`) on `UI_Element_FillBar` (Images `mainBarFill`, `increaseBarFill`, `decreaseBarFill`, `lockedBarFill`; one decrease segment today).

**C3a. Stepped HP preview + lethal skull (opus; core: `PlayerController`, `GUnit` additive)**
- Two tints on the target's bar while picking: confirmed damage (the existing decrease tint) and the hit this click would add (a second, lighter tint), drawn as a second segment after the confirmed one. `EntityInfoData` gets the confirmed amount; `UI_Element_FillBar` gets a second decrease Image (new child, colour serialized) or a `SetSecondaryDecreaseBarFill`. `GUnit.ShowDamagePreview` gets an additive overload `(float total, float confirmed)`; the old one stays (confirmed = 0).
- `PlayerController`: compute confirmed (`hovered: null`) and total (`hovered`) per unit; every already-picked unit keeps its confirmed segment while the cursor is elsewhere (the early-return branches call the confirmed-only preview when `TargetCells.Count > 0`); all cleared on cancel to unit selection, on fire and on turn end.
- Lethal skull (moved here from the feedback pass, F item 1; D-113): on **every** damage preview, an icon (placeholder skull sprite) at the left of the bar, deep-red segment, pulse 2 Hz (scale 1 to 1.12), meaning "kills if it lands". Rule: single-target / normal previews: `damage > 0 && damage >= HP` (same as `PredictsLethalOn`; a test pins them together). Multi-target while picking (D-135): the skull shows in the normal look when the **confirmed** shots on that enemy alone kill it; on the **last pick** (the click that fires), it also shows when confirmed + this click kill, drawn in the second ("this click") tint so it reads as "this click finishes it". Non-final picks never show a skull for a kill that needs the hovered click. Single-target and other normal previews use the normal skull. Option `displayLethalMarkPreview` (default on) on `GlobalSettingsSO`, next to `enableCustomCursor`.
- EditMode tests: confirmed/total split for repeated picks on one cell and across cells; the lethal rule (equal to HP is lethal; multi-target: confirmed kills → normal skull, last pick with confirmed + this click kills → tinted skull, non-final pick needing this click → none).

**C3b. "Fires" cursor (sonnet; not core)**
- `CursorSituationCatalog.cs`: a `finalPick` tri-state axis (as `basicAttack` is done: field, Specificity, `Matches`, snapshot). `CursorSituationDriver.Sample()`: Yes when the inferred ability is `MultipleTargets` and `RequiredTargetCount - TargetCellCount <= 1`, in TargetSelection and in ActionSelection (the first pick via the default ability). Catalog row "Multi Fire" (finalPick = Yes, above Basic Attack Valid) with a placeholder sprite **duplicated from an existing cursor** (`Features/UI/Cursors/Situations/`), so THJ can repaint it later. Multi-confirm abilities (`PossibleMultiActivations`) are out of scope.

**C3c. Counter label, optional (sonnet)**
- As the old C3 below, plus a `showTargetCounterLabel` option (default on) on `GlobalSettingsSO` (D-135), so it can be turned off if C3a and C3b are enough.

Order: C3a, C3b, C3c; one commit each.

### C3c detail (was C3: Q10 Lucy's target counter) (sonnet)

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
- **Animation rule:** C2 plays THJ's `_Shield` states by name; no transitions or parameters (THJ's rule).
- **Other branches:** `thj/home-test` gets all of this when it takes `main`.

## Gates

- Compile; EditMode suite (known red only) after each chunk.
- Reviewer: C1 (core) and C2 (animation + handler API); others on request.
- Play check (THJ's time: yes, one session at the end): cancel in each state and during a role prompt; Lucy's label at two ability levels; objectives line; John shield idle in three directions; enemies' idle spread; Mark hit sound; Workshop on a fresh save; M1 level 2.
- Docs: `build-log.md`, `tech/combat-architecture.md` (cancel, idle variance), `status.md`.

## Questions for THJ

- W5 to W7: answered 2026-10-21 (D-130 to D-132).
- W8: answered 2026-10-21 (D-133, option A).

## Commit log

- C1 (Q9 cancel): `64fbabef5` (2026-10-21). Review APPROVE (`reports/qw-a-c1-review.md`, should-fix applied); compile clean, EditMode passed (known red only) and play-checked by THJ.
- C2 (Q12 shield variants): `dd567cdbc` (handler variant, John's relay, tests, Hit→Idle transition removed), `7716c3a8c` (John's Hit clips play once; needed without the transition), plus THJ's `51058e216` (shielded run faster). Review APPROVE (`reports/qw-a-c2-review.md`, should-fixes applied); EditMode 430/431 (known red only) via the Unity MCP; play-checked by THJ incl. hit while shielded.
