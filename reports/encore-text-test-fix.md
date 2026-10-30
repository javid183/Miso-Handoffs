# Encore text test fix

Size S. `QuiverWiringTests.RecallAbility_IsTwoApCooldownTwoSelfCast` no longer asserts the "[PLACEHOLDER] " prefix on Encore's description (final text approved). It now asserts the description is non-empty and contains "2 AP". All other assertions unchanged.

Grep of the quiver tests: no other placeholder assertion on Encore's description or the "Linda Quiver Size" stat title. Tooltip-line placeholder assertions untouched.

File: `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/QuiverWiringTests.cs` (LF, no BOM, preserved).

Not run (editor open; THJ runs the tests).

Proposed commit: `test(linda): Encore description test checks the cost text instead of the placeholder tag`
