# Report: Memory tweaks sync (Linda turn caps, Lucy lock/hint/reset)

Plan: none (coordinator request)    Agent: implementer    Branch: thj/onboarding
Outcome: done (code only, unverified)

## What I read from THJ's data (git diff)

- Linda prefab: two turn conditions changed 3 -> 2 and 4 -> 2. The original caps were 2/3/4, so the second and third stage caps changed; per-stage caps are now 2/2/2 (stage 1 untouched at 2). Inferred from the old values, not from the stage order in the file.
- Linda interruption dialogue: one node's `side` 1 -> 0. That dialogue is hand-made (the Linda wiring never creates it), so nothing to change.
- Lucy prefab, three components added on the level object: `LevelAbilityLock` (unit Unit_Lucy, Cyclone), `GuidedAbilityHint` (Cyclone, startMode 1 = WhenUnlocked, firstTurn 1, lastTurn 1), `LevelSpecificBehaviour` (call "reset", delay 0, one entry at time 0 with `CurrentPhaseManipulationAction`, mode 0 = Reset, requireSpecificFaction off, faction entityID "Bergsons").
- Lucy interruption list, old 8 steps plus two: the reset step (`Memory2Lucy_InterruptionLSBExecutionSequence`, callId "reset") goes after CameraToRoom and before Reveal; the unlock step (`Memory2Lucy_Interruption_UnlockAbilities`, Cyclone, unlockAll off) goes after CameraBack and before EnablePlayerInput.

## What changed

- Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs: `TurnCaps` 2,3,4 -> 2,2,2.
- Features/Onboarding/Editor/HearthMemoryLindaTests.cs: expected caps 2,2,2.
- Features/Onboarding/Editor/HearthMemoryWiring.Lucy.cs: new paths and constants; `EnsureResetStep` and `EnsureUnlockStep` (LoadOrCreate at THJ's paths, contents rewritten to match his); `WireAbilityLock` (lock, hint, reset call; idempotent, reuses existing components); the interruption list now includes both steps in his order; `WireLevel` calls `WireAbilityLock`.
- Features/Onboarding/Editor/HearthMemoryLucyTests.cs: four new tests (lock entry, hint Cyclone/WhenUnlocked, reset call mode Reset, interruption order and contents of both steps).

LF, no BOM kept (all ASCII). No prefab, scene or asset touched.

## Acceptance criteria

- [x] Wiring writes THJ's values: matched against the diff by reading only.
- [ ] Re-run changes nothing: not run.

## Expected change when the tool is run

Nothing intended. Possible noise: serialized `faction.entityID` and managed-reference ids are written the same as his; the unlock/reset assets are rewritten with identical content.

## Save reset

no

## Decisions I made

- Linda stage mapping 2/2/2 inferred from the old values (3 and 4 were the stage 2 and 3 caps).
- Created the two Lucy sequence assets through LoadOrCreate (same as Linda's unlock step) rather than load-only, so a fresh checkout still gets them; the GUIDs are THJ's since the paths match.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Not verified: compile, tool run, tests (Unity MCP down). Likely spots if it fails to compile: `using` of `HintStart` (MISO.Features.UI.TutorialSystem) and `LevelAbilityLock` (MISO.Content.Levels) copied from the Linda file.
- Lucy's reset action uses `requireSpecificFaction` off while the faction field still holds "Bergsons" (as THJ has it).

## Proposed commits

1. fix(onboarding): wiring tools match the tuned Linda turn caps and Lucy's Cyclone lock, hint and reset step: the four Editor files above (plain). Goes with THJ's own prefab and asset changes, or after them.
- Fix after review: the Lucy tests now use `HearthMemoryWiringLinda.ResetCallId` (the constant lives on the Linda class); still not compiled.
