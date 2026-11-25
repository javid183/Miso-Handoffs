# Report: Family tree opens after the Yard (X-25)

Plan: plans/onboarding/2026-11-10-home-flow-tech.md (C3)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (play check by THJ pending)

## What changed

- `Features/Onboarding/FamilyTreeAutoOpen.cs` (new): the pure gate `ShouldOpen(last, familyTabMission, alreadyShown)` and the node id constant (Lucy's Sister's Rivalry node, `4f6a1c0e-...b814`).
- `Features/Onboarding/FamilyTreeAutoOpenMarker.cs` (new): once-per-save marker as a `PlayedSequencesTracker` entry named `FamilyTreeAutoOpened` (same pattern as `GuidedSkillSpendMarker`; no save-shape change, no statics).
- `Features/Home - Imported/___Khashayar/HomeManager.FamilyTreeOpen.cs` (new partial): coroutine `OpenFamilyTreeAfterTheYard`: gate, `ShowAbilityUpgrades()` (same path as a station click, so the camera stops and closing restores it), retries `OpenOnCharacter(family)` up to 10 frames, `HighlightNode`, then sets the marker.
- `HomeManager.cs`: two small edits. (1) `StartCoroutine(OpenFamilyTreeAfterTheYard())` right after the opening's end block in `StartIE`, so it runs after `EndOpening()`. (2) `DelayedMouseControl` skips turning the edge scroller on if the upgrades panel is already open (closing the panel re-enables it); without it the scroller came back 3 s after the opening while the auto-opened panel was up.
- `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.Guided.cs`: new `TryGetFamilyTab(out character, out opensAfter)`, reads the panel's Family entry.
- `Features/Onboarding/Editor/FamilyTreeAutoOpenTests.cs` (new): 10 tests.

No scene, prefab or asset changed. No new statics (no PlayModeStaticReset hook needed). All files LF, no BOM.

## Acceptance criteria

- [x] Opens on the Family tab with the sisters' node pulsing after the Trail's Home visit Yard: code path built; Family tab found via the panel's Family entry; needs THJ's play check.
- [x] Once per save: marker checked and set; test covers the gate and marker name; play check for reopen.
- [x] Nothing opens during the opening: the coroutine is started after `EndOpening()`, never inside the Yard.
- [x] Closing works: opened through `ShowAbilityUpgrades()`, so `OnPanelClosed` restores input and the scroller.
- [x] Later visits do not reopen: marker; also the gate needs last completed == Trail.

## Findings

- "Last = The Trail" is `M2 - The Trail` (guid 9901650e...). Its `completionSequence` is the Yard chain (`Yard_Midnight_SequentialSequence`, play-once), so the Yard plays in `PlayInitialSequence` at the Home visit after it, before `EndOpening()`. Test covers it.
- The gate's Trail reference is not a new scene field: it is the Family tab entry's own `requiredMissionToUnlock`, which the Home scene sets to The Trail (the opening setup tool writes it). So "opens after the mission that unlocks the Family tab". If the Family tab's mission changes, the auto-open follows it. A test checks the Home scene's entry is The Trail.
- `HighlightNode` does find family-mode nodes: `ShowFamilyAbilityBars` spawns through the same `SpawnNodeButton`, which fills `_nodeEntries`. The highlight is by node id and waits for the node to be shown.
- Which node: the plan said "the sisters' node"; the Yard pays 1 FSP and Sister's Rivalry costs 1 FSP, so I used it (Lucy's tree, family node). Marks-Sisters and Tempest Bloom are the other two sisters' locked nodes. If THJ prefers another, change `FamilyTreeAutoOpen.SistersNodeGuid` (a test checks the node is a visible family node with the Rivalry unlockable).
- Collision with the guided skill spend: none possible on the same visit. The guided spend only fires when the last completed mission is The River or The Ridge (and both done); the auto-open only when it is The Trail. Different last mission, so exclusive. Station page "Skill Tree" (first open page) plays inside the opening, before EndOpening, so also before. If something ever made both apply, my panel open happens after the opening, and the guided spend runs on panel OnEnable and would win its own tab pick; not reachable today, no design call needed.

## Tests

- `FamilyTreeAutoOpenTests`: 10/10 pass (gate cases, marker name and its save-list round trip, node check, Home scene Family tab, Trail's Yard).
- Home fixture `MISO.Core.Systems.HomeSystem.EditorTests` plus `GuidedSkillSpendTests` and `SkillTabSelectedSizeTests`: 108/108 pass. Full suite and AI regression not run, as instructed.
- Not covered by tests (play check): the actual open, pulse and close; the 10-frame retry.

## Save reset

No, not done. Needed to test: the marker is a save entry, and the state must be "Trail completed, Yard not yet played or marker not set".

## Decisions I made

- Gate reference from the Family tab entry instead of a new serialized field plus setup-tool row (same behavior, no scene edit).
- Marker class duplicated from `GuidedSkillSpendMarker` (30 lines) rather than refactoring that class.
- `DelayedMouseControl` guard (small behavior fix described above).

## Needs THJ

none

## Docs to update

- `tech/home-system.md`: "Family tree auto-open: `HomeManager.FamilyTreeOpen.cs`, started after `EndOpening()` in `StartIE`; gate `FamilyTreeAutoOpen.ShouldOpen(last completed, Family tab's unlock mission, marker)`; marker `FamilyTreeAutoOpened` in PlayedSequencesTracker; pulses Sister's Rivalry (`FamilyTreeAutoOpen.SistersNodeGuid`)."
- `tech/classic-fallback.md` (proposed wiring-point note): "`HomeManager.StartIE` end: one call to `OpenFamilyTreeAfterTheYard`; `DelayedMouseControl` has a guard for an open upgrades panel; `AbilityUpgradePanelUI.Guided.cs` has `TryGetFamilyTab`. Drop these if the classic fallback has no Yard."
- `tech/onboarding-merge.md`: HomeManager.cs gets two small edits (merge-sensitive).

## Risks and loose ends

- If the Family tab never builds within 10 frames the panel stays open on the first tab, a warning is logged and the marker is not set (retries next visit); same behavior as the guided spend.
- Unrelated and untouched: THJ's uncommitted files, Cyclone changes, M1 tests.

## Proposed commits

1. `feat(home): the Family skill tree opens by itself after the Yard`: `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.Guided.cs`, `Features/Home - Imported/___Khashayar/HomeManager.cs`, `HomeManager.FamilyTreeOpen.cs(+.meta)`, `Features/Onboarding/FamilyTreeAutoOpen.cs(+.meta)`, `FamilyTreeAutoOpenMarker.cs(+.meta)`, `Features/Onboarding/Editor/FamilyTreeAutoOpenTests.cs(+.meta)` (plain; one commit as planned)

## Other branches

none

## How to see it

1. Save state needed: The River, The Ridge and The Trail completed, the Trail's Yard not yet played, and the marker not set. Fastest: a fresh/reset save, then use the cheats/mission completion to finish Hearth, River, Ridge, Trail in order (or complete the Trail with the existing cheat and return to Home); a save reset is the surest way to clear the `FamilyTreeAutoOpened` and Yard entries.
2. Enter Home after the Trail: Yard plays, the camera pans back, then the upgrades panel opens on the Family tab with Sister's Rivalry pulsing. Stations were not clickable until then.
3. Close it; it works as a normal close. Leave and re-enter Home: it does not open again.

## Review (miso-reviewer, 2026-11-24)

Verdict: APPROVE.
- Not a core change.
- Ordering: the open starts after EndOpening() at the end of StartIE (memoryOpening returns earlier), so nothing opens during the opening.
- Marker set only after OpenOnCharacter succeeds. If the Family tab never builds: warning, panel stays on the first tab, marker unset; retries while last completed is still The Trail (acceptable).
- Edge-scroller guard is restored correctly: OnPanelClosed re-enables it; closing before the delay works as before; scene exit needs nothing.
- Guided spend is exclusive by last mission; old Home flow unaffected.
- No statics, LF/no BOM kept, no private IDs, new partial for HomeManager.
- Play check (open, pulse, close; save reset) still pending with THJ.
