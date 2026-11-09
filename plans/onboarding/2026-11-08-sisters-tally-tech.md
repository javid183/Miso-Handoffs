# Sisters' tally

Size: M    Tier: 3    Assigned to: miso-implementer (C1 opus, C2–C4 sonnet)
Branch: thj/onboarding (feature code is onboarding-only; nothing to carry to other branches unless onboarding merges)
Status: approved 2026-11-08 (Q1 = A, D-447; Q2 = A, D-448); C1 in progress

## Why

The running joke of the first hour (first-hour design, "Running joke / Turn / Payoff"; narrative draft T11-5, T11-6, F-SR2): the sisters keep score, the score fades at The Trail's pile ("Still counting?" / "…No."), and comes back as flavour after M4's "We both did". THJ asked to build it now, before the pacing check, with an easy off switch (D-444, D-445, D-446).

## Goal

A per-mission kill count for Lucy and Linda, shown on the HUD and on the mission-end panel while both sisters are in the squad, with level steps that fade it out and bring it back, and one code switch that removes all of it.

## Acceptance criteria

- [ ] `SistersTally.Enabled` (a property returning a literal, in `Features/Onboarding/SistersTally/`) set to `false` hides the HUD counter and the results row, makes both tally steps finish at once with no effect, and stops counting. Tested.
- [ ] A kill counts 1 for Lucy or Linda when her ability deals the lethal damage to an enemy unit (`GlobalEventBus.onUnitDamageDone` with `lethal == true`, attacker = `ability.Owner`, matched by `Nickname`). Other units' kills, ally kills, fake deaths (`FakeDie`, the Dom fight), Dark Worm split parents, spawner-bound deaths and hazard kills with no owner count for no one. Tested where the rule is logic.
- [ ] One tally per mission, across its levels (mission key = active mission + graph seed, as `BondSources` does). A won level banks its kills; a lost level or Restart Level drops that attempt's kills. A new mission starts at 0. Not saved. Tested.
- [ ] If a lethal hit is undone (action reversion revives the target), its kill is removed. Implementer checks first whether reversion can undo a kill in play; if it can't, say so in the report and skip the code.
- [ ] Eligible only when the active mission's roster has both Lucy and Linda and the mission is not in the source's excluded list (The Hearth, `M0 - The Hearth.asset`). In The River and The Ridge (sisters apart) and in the Hearth memory, nothing shows. Tested.
- [ ] HUD: a small counter (Linda N, Lucy N; placeholder layout and portraits/icons from existing sprites) shows while eligible and not faded, updates on each counted kill, and hides and shows with the rest of the HUD (`HideHUD`/`ShowHUD`, the HUD sequence). See Q1.
- [ ] Results: on the **mission-end** panel only, one extra row in the stats column ("Sisters' tally" + "Linda N – Lucy N", placeholder text), from a separate component on `SessionEndPanel.prefab`; `MissionEndPanelUI.cs` is not edited, and `MissionEndPanelObjectiveRowTests` still passes. Hidden when not eligible or faded. The level-won and level-lost panels never show it.
- [ ] Two sequence steps (`Sequence` assets, `Game/Sequence/Onboarding/...`): **Tally: fade out** (shows the counter on its own if the HUD is hidden, then fades it over a set time) and **Tally: return**. Each marks itself played in `PlayedSequencesTracker` (already saved). "Faded" = fade step played and return step not played, so the fade lasts across missions with no new save field.
- [ ] The Trail's pile outro (`SearchWiring.Trail.cs`, `Trail_Pile_End_SequentialSequence`) becomes: DisableInput, HideHUD, CameraOnPile, Linda "Still counting?" (counter visible alone), Tally: fade out, Lucy "…No." and the rest unchanged. The end dialogue splits into two nodes for this; the wiring script stays the source and is idempotent.
- [ ] Tally: return is built and tested, not placed in any level yet (D-448: placed with the framed beat). Until then M4 shows no tally after The Trail.
- [ ] EditMode suite: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: counting, the switch, eligibility, HUD counter, results row, the two steps, the pile wiring.
Out: the framed beat and F-SR/F-SR2 lines (B6), final text and art (narrative layer), summons crediting their owner (Lucy's Decoy credits itself; no change), sounds, saving the count.

## Touches

Systems: `GlobalEventBus` (core, listen only), `MissionTracker` (core, read only), `PlayedSequencesTracker` (read/mark, existing API), `LevelBase.prefab` (one new component, like `BondSources`), `CombatLevelContainerScene` (HUD counter), `SessionEndPanel.prefab` (one row), `CombatLevelUIManager` (core, **only if Q1 = A**), Trail wiring script and its assets, `PlayModeStaticReset` (one line).
USPs: Synergies/Family (Sister's Rivalry arc), none mechanically.
Docs: first-hour design tally row (designer: as built), GDD `missions-structure.md` or `family-systems.md` (designer), glossary "Sisters' tally" (narrative: proposed → used), `tech/classic-fallback.md` if a wiring point is added (coordinator), status, build log.

## Approach

All new code in `Features/Onboarding/SistersTally/`, namespace per conventions.

**C1 Counting core (opus).** `SistersTally` (static: `Enabled`, current state, `Changed` event, `ResetPlayModeState`), `SistersTallyRun` (banked + attempt, like `BondMissionRun`), `SistersTallySource` (MonoBehaviour on `LevelBase.prefab`, copy of the `BondSources` / `BondLevelListener` pattern: connect on enable with the mission key, `onUnitDamageDone`, `levelEnded`, `onRewardsGranted` "Mission complete"/"Mission failed", every handler in a guard that skips the AI worker thread and catches exceptions; serialized excluded-missions list and the two step assets for the faded check). Revert handling per the criterion. EditMode tests for the rules. Prefab edit by editor script or a minimal YAML add.

**C1b Attribution + Hearth opt-in (opus; added 2026-11-08, D-449, D-450; design `plans/onboarding/2026-11-08-sisters-tally-attribution-design.md` § Lens notes/Recommendation).** (a) Duo bracket, feature-local: open on `onSynergyTriggered` id "Duo" with a sister among the partners, close on the trigger ability's `abilityPerformed`; inside it, an enemy `unitDied` with HP at its minimum (`IsAtMinimum`) counts for each sister among the partners (Linda–Lucy: both; Mark–Lucy: Lucy only); the trigger ability's own `onUnitDamageDone` inside the bracket is ignored (no double count). Lucy's role finisher stays hers. Tempest Bloom's window waits for Tally: return (Bloom locked until the Yard). (b) Eligibility from the level's deployed player units (both sisters deployed) instead of the mission roster; The Hearth leaves the excluded list, so segments 3–4 show it and 1–2 don't. Tests for each rule.

**C2 HUD counter (sonnet).** Widget modelled on `LevelInfoPanelUI` (TMP labels, `UIPanelAnimator`, `Show`/`Hide`), placed in `CombatLevelContainerScene` by an editor script; follows the HUD through the core hook (D-447): one optional serialized field on `CombatLevelUIManager` and one null-safe call each in `HideHUD`/`ShowHUD`, nothing else in that file; its own commit.

**C3 Results row (sonnet).** `SistersTallyResultRow` component with its own `StatRowUI`, child of `statsColumn`; fills itself on enable, active only on the mission-end panel instance, then rebuilds the layout.

**C4 Steps and wiring (sonnet).** The two `Sequence` steps; the Trail wiring change; Tally: return not placed (D-448).

Commits: one per chunk (C1 code + tests + prefab; C2 widget + scene; C3 row + prefab; C4 steps + Trail assets; Q1 core hook, if any, alone and first in C2).

## Risks

- Statics (`SistersTally` state, event) → `ResetPlayModeState()` registered in `PlayModeStaticReset`.
- Bus handlers can run on the AI worker thread → guard as Bond does; no Unity APIs there.
- Double counting: count only on `lethal` damage, never on `unitDied` (fake deaths, splits, spawner deaths raise it without a kill).
- Restart farming → attempt dropped on defeat/restart (Bond pattern).
- `MissionEndPanelObjectiveRowTests` checks every serialized reference on `MissionEndPanelUI` → separate component, no new field there.
- Scene and prefab edits → editor scripts, re-runnable; no hand-edited big YAML.
- The pile outro is THJ-tuned wiring → only the dialogue split and two inserted steps; everything else stays in order.
- AI content not touched; `AIRegressionTest` must not move.
- Classic fallback: if a new wiring point is added, `tech/classic-fallback.md` gets a line.

## Gates

Compile / EditMode (known red only) / review per chunk / THJ play check before each feel commit (C2, C4: needs his time, a fresh save, The Trail with John or Mark) / docs above.

## Open questions (THJ)

- **Q1** How the counter hides with the HUD: (A) one optional field and one call each in `CombatLevelUIManager.HideHUD`/`ShowHUD` (core, additive, own commit) — needed for the counter to show alone over the pile during "Still counting?"; (B) no core edit: the counter is a child of an existing HUD panel and hides with it; the fade then plays only if the pile lines run before HideHUD (reorders his outro) or isn't seen.
- **Q2** Where Tally: return goes. The tally is only eligible in The Trail before the pile and in M4; after the pile fade it stays hidden until return plays. F-SR2 ("We both did") belongs to the framed beat, not built. (A) build return now, place it later with the framed beat: until then M4 shows no tally; (B) place return now at the end of M4's first level with F-SR2 as placeholder lines; (C) no persistence: the fade lasts only for The Trail and M4 shows the tally from its start.

## Log

- 2026-11-08: approved by THJ (D-444 to D-448). C1 dispatched (implementer, opus).
- 2026-11-08: C1 review APPROVE + 3 should-fixes (done); C2 review APPROVE + 1 should-fix (done). THJ play-checked the counter OK. **Committed** `74c97e819` (counting core), `c0d623cc2` (core HUD hook, D-447), `e0d09f5f6` (counter + scene).
- 2026-11-08: THJ's attribution questions → design; D-449 to D-451. C1b added; dispatched (implementer, opus).
- 2026-11-08: C1b fix round done. THJ played: Duo OK; Tempest Bloom raises only Linda's. C1c added (Bloom kills count for both, per D-449; brought forward from "with Tally: return"); dispatched (implementer, opus).
- 2026-11-08: C1c review APPROVE + test fixes; THJ played Bloom OK. **Committed** `d1c178f4c` (C1b + C1c combined: the listener holds both). C3 dispatched (implementer, sonnet): results row shown if the tally was eligible in any level of the mission and isn't faded.
- 2026-11-08: C3 placement reworked to two StatRow rows (D-453), MVP hidden while they show (D-454); reviews 2 and 3 APPROVE; THJ played OK. **Committed** `2c698e997`. Next: C4 (fade/return steps).
