# Home flow: new-game start, visit-1 handover, Family tree auto-open (tech plan, build chunk 8)

Size: M    Tier: 3 decided (D-472, D-478; the after-Hearth plan "Home")    Assigned to: miso-implementer (sonnet; opus for C1 if `StartIE` ordering turns subtle)
Branch: `thj/after-hearth` (scope all)
Status: draft, waiting on THJ's OK to dispatch

## Why

THJ's notes: start at Home with the storytelling idle; nothing happens between the two pair missions; open the Family tree after the Yard. Design: [`2026-11-09-onboarding-after-hearth-design.md`](2026-11-09-onboarding-after-hearth-design.md) "Home". Code facts: [`reports/after-hearth-tech-explore.md`](../../reports/after-hearth-tech-explore.md) §C.

## Decisions

- **D-478 (THJ):** main menu → intro text screen → **Home** (Margaret's story night, her opening lines H0-1 to H0-4) → the Hearth starts by itself.
- **D-472 (THJ):** visit 1 = handover scene at the door, only after the **first** pair mission (River or Ridge), leading into the Workshop page.
- **Coordinator (Tier 2):**
  - The new-game idle is data: a HomeState holding `MargaretStoryNight` as `Game Data.asset`'s `initialHomeState` (today empty).
  - The visit-1 gate is a new non-core conditional `Sequence` (plays its inner sequence only if the other pair mission isn't completed), set as both pair missions' `completionSequence` (both are empty today). Reusable; no core change.
  - The Family tree auto-open runs right after `EndOpening()` in `HomeManager.StartIE`, gated by "last completed mission = The Trail" + a once-per-save marker (pattern `GuidedSkillSpendMarker`), not inside the Yard sequence (opening a panel during the opening is unsafe, `StartIE` comment).

## Chunks

### C1 · New-game start at Home

- `IntroSceneText` end: when the Hearth isn't completed, go Home instead of `InitiateMission(initialMission)`.
- Home on a fresh save: HomeState with `MargaretStoryNight` (data), stations all locked until the Hearth is done (opening setup tool table: `UnlockAfterMissions` includes the Hearth for every station incl. the map table; Family tab already after the Trail), Margaret's H0-1..H0-4 lines (narrative draft; placeholders) as an opening sequence, then the Hearth starts (`InitiateMission(GetInitialMission())`, as `HomeManager.LoadLevel` does). Hook: `PlayInitialSequence` / end of `StartIE` when no mission is completed.
- Returning players (Hearth completed) unchanged: main menu → Home.
- Update `tech/classic-fallback.md` if a wiring point is added.
- Tests: the route rule (fresh vs Hearth done) as a pure function; opening-setup table test.

Acceptance: fresh save → intro text → Home on Margaret's story night, stations not clickable, her lines → the Hearth loads by itself; after the Hearth, Home behaves as today; tests green.

### C2 · Visit-1 handover scene

- New `Sequence` subclass (Features/Onboarding), e.g. "play if mission not completed": inner sequence + the mission to test; plays inner only if that mission isn't completed.
- Handover `DialogNodeSequence` from narrative V1 lines (V1-2a..V1-4a / V1-2b..V1-4b by order, V1-1 Ben; clue line), one per pair mission's order, wrapped by the conditional, set as `MS1 - The River.asset` and `MS2 - The Ridge.asset` `completionSequence` (via an editor menu item, like `HomeVisitsWiring`).
- It plays in `PlayInitialSequence`, before the station pages, so it flows into the Workshop page.
- Tests: the conditional's rule; the wiring tool idempotent.

Acceptance: finish the first pair mission → handover scene → Workshop page; finish the second → no handover (visit 2 as today); tests green.

### C3 · Family tree opens after the Yard

- After `EndOpening()`: if the last completed mission is The Trail and the marker isn't set, `AbilityUpgradePanelUI.OpenOnCharacter(familyData)` (retry ~10 frames as `GuidedSkillSpend.OpenGuided`), `HighlightNode` on the sisters' node (check it finds family-mode nodes; report if not), set the marker.
- Tests: the pure gate (`last == Trail && !marker`).

Acceptance: after the Yard and the pan back, the upgrades panel opens on the Family tab with the sisters' node pulsing, once per save; closing works; later visits don't reopen it.

## Risks

- `StartIE` ordering (intro, sequences, station pages, opening end) is fragile: read it fully; no panel during the opening.
- `Game Data.asset` is a core data asset: data-only change, own commit.
- Save: the marker is a `PlayedSequencesTracker` entry (no save shape change). Reset the save to test; say so.
- Merge with `thj/home-test` conflicts on `Game Data.asset` and the Home scene: note new shared-file edits in `tech/onboarding-merge.md`.
- No new statics expected; if any, PlayModeStaticReset.

## Gates

Compile / EditMode / review / THJ play check (fresh save run to the Hearth; first pair mission; the Yard) / docs: `tech/home-system.md`, `tech/classic-fallback.md`, `tech/onboarding-merge.md` (coordinator); GDD progression/home pages (designer).

## Proposed commits

C1 code + tests, then data (`Game Data.asset`, HomeState, stations); C2 code + tests, then mission data; C3 one commit.
