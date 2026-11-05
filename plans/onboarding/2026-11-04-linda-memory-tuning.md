# Linda memory tuning + what goes to `main` (2026-11-04)

Status: **approved 2026-11-04** (D-372 to D-375). L1 dispatched. Open level questions for THJ: `reports/linda-memory-rework-review.md`. Slug `linda-memory-tuning`. Facts: `reports/linda-memory-rework-review.md`, `reports/linda-memory-tweaks-research.md`, `reports/onboarding-commits-for-main.md`.

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

## Commit log

- L1 (+ D-376 no-XP follow-up): `67fb2d3bf` (THJ's rework prefab + 6 interruption assets + wiring + tests). EditMode 1309/1310 known red only; THJ played OK 2026-11-04.

## Tech plan: G1, G2, G3 (written 2026-11-04, coordinator)

Branch `thj/onboarding`. G1 and G3 are general (go to `main`, D-372): new files outside `Features/Onboarding`, no onboarding dependency. G2 edits `GuidedAbilityHint` (onboarding-only today) and stays on the branch unless THJ moves the hint to `main`. No core system touched (D-373: bar-level lock); if any chunk finds it needs a file in `tech/core-systems.md`, it stops and reports.

### G1 Level ability lock (sonnet; M)

Goal: a level can lock chosen abilities of chosen units at level start; locked abilities are absent from the action bar (and every other player path to cast them); an unlock sequence brings them back, and the bar rebuilds at once if that unit is shown.

- New `Features/Levels/AbilityLock/`: `LevelAbilityLock` MonoBehaviour on the level (entries: `GUnit unit`, `AbilityPreset[] abilities`; locked from level start; `IsLocked(RuntimeAbility)`; `Unlock(AbilityPreset[] or all)`; C# event `Changed`). A pure rules class (no Unity objects) holding the locked set, for EditMode tests. `UnlockAbilitiesSequence : Sequence` (fields: abilities to unlock, or "all"); finds the level's lock and unlocks, completes at once. Optional `LockAbilitiesSequence` only if trivial (THJ may want re-locking later; not required).
- Lookup: no static. The bar finds the level's `LevelAbilityLock` when it populates (level-scoped `FindAnyObjectByType` is fine; Populate runs on selection) or via the current level instance if one is exposed cheaply.
- `AbilitiesBarHUDUI.Populate` (`Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs:57`): skip locked abilities next to the `QuiverAbilityInfo.HiddenFromBar` check; subscribe to `Changed` and repopulate the shown unit when its abilities change. Number shortcuts map to shown buttons, so they follow; verify.
- Audit every other player route that casts an ability without the bar (Family Role prompts/follow-ups, Duos, cooperation, QTE, `PlayerController` paths, quiver UI). List them in the report. A route that can cast a locked ability and can only be blocked in a core file: stop, report (Tier 3).
- Subscriptions removed on disable/destroy; nothing persists after the level (component lives on the level).

Acceptance: (1) with Linda's Explosive Arrow and Encore listed, her bar at level start lacks both buttons and shortcuts don't reach them; (2) after `UnlockAbilitiesSequence` plays, both appear without reselecting Linda; (3) no route in the audit casts a locked ability; (4) levels without the component behave exactly as before; (5) EditMode tests for the rules class and the bar's hide decision; full EditMode green except the known red.

### G2 Hint starts on unlock (sonnet; S; onboarding-only)

- `Features/Onboarding/GuidedAbilityHint.cs`: add a start mode: `Turn` (today's behaviour, default, existing levels unchanged) or `WhenUnlocked` (starts when the level's `LevelAbilityLock` unlocks its ability; ends on first use as today; `lastTurn` ignored or optional cap). Uses G1's `Changed` event.
- Acceptance: John/Mark memory hints unchanged (tests); a `WhenUnlocked` hint pulses Explosive Arrow right after the unlock and stops on its first use; EditMode tests for the start decision.

### G3 Encore pulses while Linda is out of arrows (sonnet; S/M; general)

- In `Features/Player/Linda/Scripts/Quiver/` (find the quiver HUD/bar code): while the shown unit is Linda, her quiver `IsEmpty`, and her Encore button is on the bar and interactable, the Encore button pulses (size pulse like the hint: own small pulse math, not a dependency on `Features/Onboarding`); stops as soon as she has an arrow, Encore is used, or the button is gone (locked, hidden with the quiver off). Driven by `LindaQuiver.OnChanged` / bar rebuilds, not per-frame searches. Restores the button's scale.
- Must not fight a `GuidedAbilityHint` on the same button (if both target one button, the hint wins or they don't stack; pick one and say which).
- Acceptance: empty quiver → Encore pulses; one arrow back → stops; Encore locked (G1) → no pulse, appears pulsing after unlock if still empty; quiver off → nothing; EditMode test for the pulse decision rule.

### Risks

- Statics: none planned (PlayModeStaticReset if any appear). AI: untouched (player bar only; `RuntimeAbility.Available` unchanged, so AI threat sims still see Linda's full kit; acceptable, and noted). Serialized renames: none. Saved data: none. Assets: level data in L3 by THJ or a small wiring change. Subscriptions: cleaned on disable. Other branches: G1, G3 to `main` per D-372.

### Then L3 (data, onboarding)

`GB_m1-linda`: `LevelAbilityLock` with Linda: Explosive Arrow + Encore; `UnlockAbilitiesSequence` added to stage 1's interruption (`Memory1Linda_Interruption_SequentialSequence`, before EnableInput/ShowHUD); `GuidedAbilityHint` (`WhenUnlocked`, Explosive Arrow); claw `turnOrder`: THJ tunes it himself (D-380), L3 leaves it alone. Wired through Wire Memory 1 (Linda) so re-runs keep it. THJ play-checks.
- L1 follow-up (D-377, caps 2/3/4, claws inactive): `4d4e78424`.
- G4 checker/tool/tests (review APPROVE + 2 fixes): `83aa585f0` → **to `main`**.
- `Level2-C2` split (D-378): `9ba3b8421` → **to `main`** (re-check `Level2-C3-2`, `LevelDomFight` there with the scan test).
- EditMode before these: 1314/1315, known red only.
- G1 level ability lock (review APPROVE + 2 fixes; EditMode 1327/1328): `266a3985c` → **to `main`**. Play check owed with L3. Super Time gap accepted (D-381).
- G3 Encore pulse (+ lock query methods; review APPROVE + fixes D-382; EditMode 1335/1336): `ccfbb36d2` → **to `main`** (after `266a3985c`).
- G2 hint WhenUnlocked: `ced039945` (onboarding-only, D-380).
- L3 Linda memory lock/unlock/hint data + THJ's claw turnOrder + camera tweaks: `0aa549bc6` (review APPROVE + test fixes; THJ played OK; EditMode 1337/1339: known red + `QuiverWiringTests.RecallAbility_IsTwoApCooldownTwoSelfCast`, red since THJ's `87174b9fc` dropped "(2 AP)" from Encore's description; his call).
