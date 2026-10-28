# Linda at a distance, D1: tech plan

Size: L    Tier: 3 (Family Roles: Watch damage and a positional rule; design approved D-263, D-266, D-267, D-285, D-286)    Assigned to: miso-implementer (chunks below), reviewer; THJ plays
Branch: all, built on `thj/linda-quiver` (after C5)
Status: draft, ready to dispatch (no open Tier 3 questions; see "Decisions I made")

## Why

Everything in the game rewards standing near John, so nobody walks out to Linda's arrows, and Encore becomes the default way to get them back. D1 tests whether a small reward for distance, plus better fetch cues, changes that. Design: [`2026-10-27-linda-distance-design.md`](2026-10-27-linda-distance-design.md) § D1 (rev 3).

## Goal

Four toggled levers on one config asset. With every toggle off, the build plays like C4/C5:
- Far Watch with the trade;
- Encore cooldown 3;
- per-picker fetch cues with a long-distance call-out;
- the D1 log lines.

## Acceptance criteria

The design's D1.1 to D1.4 acceptance lists are the criteria; each chunk below names its share. In short:

- [ ] Toggles off: Watch hits 6×, Encore cooldown 2, today's hand-back, no D1 log lines, no Far visuals.
- [ ] Far Watch:
  - 5× when any counted squad unit is within 2 (radial, footprint) at End Turn, 7.5× when none; locked through the enemy phase.
  - Live on a player-phase Watch.
  - Only Watch changes. Bow, Crescendo and the arrow Duos keep their damage.
- [ ] Far readability: the mark over Linda (with a lock pip in the enemy phase), the ghost-tile mark, "Far lost" on another unit's move preview, the 2-cell box on badge hover or Shift, the prompt "Arrows N > N−1 · Far 7.5×", and the tooltip. The hover damage preview matches the hit.
- [ ] Encore cooldown 3 when on.
- [ ] Hand-back variants:
  - John, Lucy, Mark and Toba each have their own; Linda has her own, with no toss.
  - A picker 4 or more cells away does the call-out.
  - One beat per move, shown as "+N"; no line repeats twice in a row per picker per turn.
  - Instant pickups, Encore and the catch are unchanged.
- [ ] Log: the toggles at level start, Far at each End Turn, the factor and source on each Watch, the pickup kind and distance, and damage Linda takes while Far.
- [ ] EditMode: the Far rule, the factor table, the lock state, the call-out distance rule, the beat merge rule, the log lines.

## Scope

**In:** D1.1 to D1.4.

**Out:**
- Arrow Chase (its own plan after D1).
- The Fetch FTP node (D-264).
- The optional glint. The design allows skipping it; it is built only if reach is cheap to compute (C4 reports).
- John's pull (D-269).
- Grid-based hits (`arrow-hits-by-grid`).

## Touches

**Systems.** Linda's quiver folder (non-core). Data:
- Linda's role ability: the Watch damage value.
- The Encore preset: cooldown.

No core-system code is planned. Reads only: the squad list, footprints and the bus (turnStarted, turnEnded, onFamilyRolePrompt/Outcome).

**USPs:** Family Roles (Watch).

**Docs:**
- GDD Linda (LI-15, LI-8): designer.
- `tech/combat-architecture.md`: coordinator.
- Glossary (Far): narrative.

## Approach

**Config.** A new ScriptableObject `LindaDistanceTuning` in the quiver folder, loaded by `LindaQuiver` through a serialized reference on `Unit_Linda.prefab`, not from Resources. It holds:
- the four toggles;
- the factors: near 5, far 7.5, off 6;
- the radius 2;
- the call-out distance 4;
- Encore cooldown on 3 / off 2.

**Far state.** `FarWatchRules` is a pure static. Inputs: Linda's cell and footprint, plus the counted units' footprints. Output: Far yes/no, the nearest unit and its distance. `LindaFarState` is a component on Linda that:
- computes the live state on request;
- locks the state when the player faction's turn ends (bus `turnEnded` for the player faction, after the last action);
- unlocks at the player's `turnStarted`;
- treats level start as near.

Who counts (D-285): living units of Linda's own faction, excluding Linda, decoys, summons and objects. The implementer finds how decoys and the Cyclone are marked (tags or a unit type) and filters on that. Units of an allied but different faction never count.

**Watch factor, Watch only.** This is the risky part, and it goes first.
- Watch fires `LindaAttackArrow`, the same prefab as the bow, through `Linda_Ability_FactionRole_Effect_Spawn`. Its damage comes from the role ability's effects and the arrow's AttrMod. The implementer reads the chain first: where 6× is set for Watch and for the bow, and whether they share an asset.
- Preferred: a non-core way to scale only the role arrow's damage, using the QuiverArrow-side knowledge that the arrow came from Watch (`StatAttributesContext` is the role's `RuntimeAbility`, as C5 confirmed). Options, in order:
  - (a) separate damage data for the role ability if it has its own AttrMod asset: 5× base, plus a Far multiplier applied through an existing modifier/extra-mod hook that the Projectile reads (`OnHitExtraModifier` is public; check whether a feature can set it per arrow before the first hit);
  - (b) a Watch-only arrow prefab variant with its own damage value, with the Far factor applied the same way;
  - (c) anything else non-core the implementer finds.
- **If only a core change can do it, STOP and report.** That makes it a Tier 3 question for THJ.
- The hover damage preview must match: check how `AbilityDamagePreview` (core) reads the role's damage. If the preview can't show the Far factor without core code, report it; it becomes a question, not a silent mismatch.

**Encore cooldown.** The preset's `coolDownV` becomes 3. When the toggle is off, `LindaQuiver` sets the cooldown back to 2 right after Encore activates, through the public `RuntimeAbility.SetCoolDown`. The implementer confirms the button and tooltip show the real value. A value change on an existing preset doesn't move the known-red AI test; the implementer confirms it.

**Fetch cues.**
- The hand-back already lives in `GroundedArrowField.Pickup` with its `HandBackLines` table.
- Variants per picker: one toss style and line set per picker (John lob, Lucy flick with a spark trail, Mark spinning throw, Toba leaf-wrapped hand-off, Linda no toss).
- A call-out branch at 4 or more cells away.
- A per-move merge: pickups in one move become one beat with "+N". The rules go in a pure `HandBackRules` (distance → call-out, merge, no-repeat).
- Lines from `miso-narrative`, tagged `[PLACEHOLDER]`. Art is placeholder: tween shapes and an existing sprite tint, no new art.

**Logs.** Extend `QuiverLogListener` and `QuiverLogLines` (C5) with the D1 lines. No Core change beyond C5's `AddCustom`.

**Visuals for Far.** Non-core presenters in the quiver folder:
- the Far mark next to the pips;
- the ghost-tile mark through `IMovePreviewPathSource` (D-270);
- "Far lost" over Linda while another unit's move is previewed;
- the box on badge hover or Shift, drawn by Linda's own presenter;
- the prompt text through `QuiverPromptLabel`;
- the tooltip through `QuiverTextRules`.

Core code (`RoleZonePresenter` and others) must not import Linda (D-272).

## Chunks (riskiest first; one implementer run and one commit unit each)

1. **D1-C1: config, Far state and the Watch factor** (opus).
   - Covers `LindaDistanceTuning`, `FarWatchRules` with tests, `LindaFarState`, and the Watch-only factor with a matching damage preview.
   - Accept: the Far acceptance items without visuals. Damage values are checked in the combat log and in play; there are EditMode tests for the rule and the lock.
2. **D1-C2: Far readability** (sonnet): the mark, the lock pip, the ghost mark, "Far lost", the box, the prompt and the tooltip.
3. **D1-C3: Encore cooldown toggle** (sonnet, small; can merge into C2's run if the implementer has room).
4. **D1-C4: fetch cues** (sonnet).
   - Needs the narrative lines first; ask `miso-narrative` in parallel with C1.
   - Covers the variants, the call-out, the merge and the no-repeat rule, with `HandBackRules` tests.
5. **D1-C5: log lines** (sonnet).

**Play checks** (THJ's rule: play before commit): after C1 + C2 together, then after C4, with C3 and C5 folded into either.

## Risks

- **Watch-only damage without core.** This is the main unknown: C1 stops and reports if only core can do it. The damage preview has the same risk.
- **Who counts.** Decoys, summons and the Cyclone need a reliable filter; the implementer cites what they filter on.
- **Lock timing.** "After the last action, before the first enemy acts" depends on bus order. The implementer verifies `turnEnded` order against `CombatLevelRunHandler.SwitchTurnIE` (core, read only).
- **Statics.** None expected. Any static gets a `PlayModeStaticReset` hook.
- **AI thread.** Nothing the AI reads changes.
- **AIRegressionTest.** Data value changes on existing presets: confirm the known-red message is unchanged. A new arrow prefab variant isn't an ability preset, so it shouldn't move either. Confirm.
- **Restart and level start.** Lessons from D-281 and D-282: no `CombatLevel.PlayerFaction` before init (use `QuiverLevelAccess`). Nothing created as its own root in `Start`; parent it under the level or under Linda.
- **Other branches.** `main` and `thj/home-test` get this when the quiver goes there.

## Decisions I made (Tier 2)

- Toggles live on a ScriptableObject referenced by Linda's prefab, not on GlobalSettings, so core settings stay untouched.
- The glint is not built in D1 unless C4 finds reach cheap to compute (the design allows this).
- Placeholder art only for the toss variants and the Far mark.

## Test plan

- **EditMode:** Far rule (who counts, radial ≤ 2, footprints, decoys), factor table, lock state machine, call-out distance, merge and no-repeat, log lines. Full suite after each chunk; known red only.
- **Play:** the design's D1 acceptance lists as numbered steps in `playtests/`, written by each implementer.

## Gates

- **Compile:** THJ's editor; agents can't batch while it's open.
- **Tests:** EditMode, known red only.
- **Review:** each chunk.
- **Play check:** needs THJ's time. Yes, twice.
- **Docs:** GDD Linda LI-15 and LI-8 (designer), glossary "Far" (narrative), `tech/combat-architecture.md` (coordinator).

## Commit log

(empty)
