# Review: onboarding wiring stops owning dialogue text

Reviewer: `miso-reviewer` (read-only; filed by the coordinator, 2026-11-11). Plan: `plans/2026-11-11-wiring-leaves-dialogue-tech.md`. Report: `reports/wiring-leaves-dialogue.md`.

**Verdict: APPROVE.** No must-fix.

- Every dialogue write goes through `WiringSeed.Dialogue`, including the Trail's `SpeakAsThePick` calls, which now run only through `onSeed`. Every step-list write goes through `WiringSeed.StepList`, and an existing list is returned untouched. The caption speaker path is fixed. `EnsureUnlockStep` (`HearthMemoryWiring.Linda.cs:304`) still inserts into an existing list, which is pre-existing behaviour, idempotent and covered by the md5 check.
- The tests still have teeth: each removed text assert has a structural replacement that can fail, and none runs on an empty collection.
- Deliberately weaker:
  - the "fade after punchline" and "fade between cub and cutaway" orders are gone;
  - the cutaway-still checks are gone;
  - "speaks through `GenericCharacter_1`" became "not John or Mark by name".

  All of these match the teammate's flow and the no-speaker-names rule.
- C2: `NewPreviewScene` and `ClosePreviewScene` are paired in TearDown, and each test keeps its intent. The commit split is sound.

## Should fix
1. `WiringSeedTests.cs:100`: `LogAssert.NoUnexpectedReceived()` ignores warnings, so the "kept quietly" half can't fail. Being fixed in a follow-up.
2. The report claimed LF; the files are CRLF on disk (unchanged for the edited ones). Being corrected in the report.

## For THJ
Plan deviation (Tier 2): an existing step list is never rewritten, even when its structure differs. The wiring warns instead, so future structure changes in the wiring reach only newly created assets. Plus the report's "Needs THJ" items 1–6 (Hearth endings restructured by the teammate; Linda's end no longer re-enables input and the HUD; Lucy's cutaway is unused; Mark's walks play over a faded grid; the River and Ridge's old dialogues are unused; `TransitionToNextLevel` isn't placed last).
