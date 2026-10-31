# Onboarding: keep the `thj/home-test` merge safe (C1b)

Size: M    Tier: 3, approved by THJ 2026-10-31 (D-339: "anything that can be done to keep the future merge safe and easier ... do it and log")    Assigned to: `miso-implementer` (sonnet) → `miso-reviewer` → coordinator check
Branch: `thj/onboarding` (editor-only code + docs). Status: dispatched 2026-10-31

## Why

C1 (`38bc7db73`, `bb9982c87`, `f36da02f8`) edits files that `thj/home-test` also edits. A dry run (`git merge-tree HEAD thj/home-test`, 2026-10-31) already conflicts on:

- `Home - Scene.unity`: home-test changed ~9.8k lines, including the WorldMapPanel instance's override list where C1's pin overrides sit.
- `Game Data.asset`: home-test added 8 edge-less graph nodes (Home sorties; corrected from 4 by the review); C1 removed the old missions' nodes from the same list.
- `Unit_Mark.prefab` auto-merges (different lines).

C5 (Home visits) will add more Home-scene edits. Hand-merging Unity YAML twice per chunk is the risk.

## Goal

Every onboarding edit to a shared file can be re-applied in one click on either side's version: after a merge, take `thj/home-test`'s file whole and run the builder. A test fails if the committed state drifts from what the builder produces.

## Build

1. **`Tools/Onboarding/Apply Opening Setup`** (editor-only, non-core, under `Features/Onboarding/Editor/`; one idempotent builder, the pattern home-test's Home builders use). Each step reports *changed* / *already applied*; a **Check only** menu item reports without writing.
   - Mission graph (`Game Data.asset`, through the graph's editor API, not YAML): Hearth initial; Hearth → River, Hearth → Ridge, (River AND Ridge) → Trail → M4; remove the old missions' nodes (M1, old M2, both M3s, M5–M7) and the gates left with no purpose. **Leave every other node alone** (home-test's sorties, the dead M8–M14 branch).
   - `IntroScreen` / `MainMenuScene` `initialMission` → Hearth.
   - `Unit_Mark.prefab` `unlockedAfterMission` → Hearth.
   - Home scene: world-map buttons found by what they point at (old mission → new mission; already-new counts as applied), never by GameObject name (home-test's names differ); hide the M3 Mark Intro, M6, M7 buttons; Mark's `CharacterSelectButton` and `UpgradesPanel` entry found by `Mark_DialogueCharacter`.
   - One table at the top of the builder holds every mapping, so C5 adds rows rather than code.
2. **Test** `OnboardingOpeningSetupTests`: Check-only on the project reports nothing to change. Must not dirty or close THJ's open scenes (open additively, close what it opened, never save).
3. **Proof on the old state:** copy the pre-C1 versions (`git show 194bd566b:<path>`) of the Home scene and `Game Data.asset` to a scratch folder inside `Assets`, run the builder against the copies, confirm the result matches C1 (same references and graph), delete the copies. Report the comparison.
4. **Merge note** (coordinator): `tech/onboarding-merge.md` lists every shared-file edit and the recipe.

## Acceptance

- Apply on the committed tree changes nothing (`git status` clean apart from THJ's pre-existing files).
- Run on the pre-C1 copies, it reproduces C1's graph and scene wiring.
- Home-test's extra graph nodes survive (unit test with a graph containing an unknown node).
- EditMode suite green except the known `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Gates

Review / EditMode / coordinator checks the no-op run. No play check needed (editor tool, no runtime change).
