# Linda memory tuning + what goes to `main` (2026-11-04)

Status: **draft, waiting on THJ** (Tier 3 questions below). Slug `linda-memory-tuning`. Facts: `reports/linda-memory-rework-review.md`, `reports/linda-memory-tweaks-research.md`, `reports/onboarding-commits-for-main.md`.

## Principle (proposed)

Build everything on `thj/onboarding`. General code goes in **its own commits, outside `Features/Onboarding`, with no onboarding dependency**, so it cherry-picks to `main` cleanly. Level data stays on the branch. Data that must also change on `main` is changed by a **tool** that travels with the code and is re-run on each branch (the Apply Opening Setup pattern), so no data-only cherry-picks fight the branch's edits. One cherry-pick session on `main` later (THJ switches, editor closed, tests after). No runtime "onboarding mode" switch: the builder already covers that role and a switch adds a second source of truth.

## Chunks

Onboarding-only (branch):

- **L1 Rework fix-ups** (S): untick the 4 hidden claws; Wire Memory 1 (Linda) builds the 3 stages with a fresh condition per objective; rewrite `HearthMemoryLindaTests` for the stages. Plus THJ's answers on the level questions.
- **L3 Level data**: lock Explosive Arrow + Encore at start, unlock on stage 1's interruption, pulse Explosive Arrow after; per-enemy `turnOrder` overrides for the desired order (T5, no code).

General (branch first, then `main`):

- **G1 Level ability lock** (T1/T2, M): a level component listing unit + abilities locked at start, and an unlock `Sequence` (played from an objective group's `onCompleteSequence`). Non-core route: hide or grey the button in the bar (`AbilitiesBarHUDUI`/`UnitAbilityButtonUI`) and block every other activation path the implementer finds (hotkeys); if a path needs `RuntimeAbility.Available`, stop and ask (core).
- **G2 Ability hint triggers** (T3, S/M): `GuidedAbilityHint` gains a start condition (on unlock / on a signal), not just a turn. Move it out of `Features/Onboarding` if it goes to `main`.
- **G3 Encore pulses when Linda is empty** (T4, S/M): quiver feature (`Features/Player/Linda`), on `LindaQuiver.OnChanged` + `IsEmpty`, only while Encore is usable (so not while locked).
- **G4 Shared objective conditions** (T6, S/M): editor test that scans level prefabs for repeated condition reference ids + a menu tool that gives each a copy. Run it on `GB_m1-linda` here; on `main` for `Level2-C2`, `Level2-C3-2`, `LevelDomFight` (after a check that the sharing there is unintended). Non-core (editor). Optional core guard (`CombatLevel.OnValidate`) only if THJ wants it.
- **G5 Turn-order tie-break** (T5, optional, core, Tier 3): enemies with equal `turnOrder` act in a fixed order (e.g. hierarchy order) instead of `FindObjectsByType` order. Own commit.

Order: L1 → G4 → G1 → G2 → G3 → L3 (→ G5 if approved). One writer at a time.

## To `main`

The 21 commits in `reports/onboarding-commits-for-main.md` (with its splits) + G1–G4 (+ G5), in one cherry-pick session.
