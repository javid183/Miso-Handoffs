# M1 (The Ridge) redesign play check, 2026-11-24

Scope `thj/onboarding-demo`. Played by THJ on the 4.1a + 4.1b build (uncommitted). Result: good overall.

## THJ's own edits after the play (uncommitted, his)

- Slightly tweaked `GB_m1-ridge.prefab`.
- Resized the rock (`Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`, scale overrides).

Re-running `Tools/Onboarding/The Ridge: Apply Layout and Wire` may overwrite these. Read his prefab back before any re-wire.

## Change requests (coordinates are paper / block coords = prefab + (1,5))

1. Killing the Claw on 8,3 sometimes leaves Mark on 8,2 instead of 8,3.
2. Both Claws on 6,3 and 6,4 should die to Catch & Return; now one survives.
3. The lines around Catch & Return should be shorter and sound like they're mid-fight. Now they sound as if no enemies are near.
4. After the Claws are beaten, the family reaches the clue on top. Then 3 or 4 new Claws spawn from behind, probably with a Black Claw and its intro. Swap: the Masher goes to M3 in place of the Black Claw there (the Black Claw moves to M1).
5. Move the HP potion tutorial to after item 4.
6. The beat-2 Dark Claws (the three that fall in) can have slightly more HP.

## Error seen

```
IndexOutOfRangeException: Index was outside the bounds of the array.
MISO.Core.Animation.EntityAnimationHandler.HandleFrameAction () (EntityAnimationHandler.cs:91)
MISO.Core.Animation.EntityAnimationHandler.Update () (EntityAnimationHandler.cs:85)
```

Line 91 is `animator.GetCurrentAnimatorClipInfo(0)[0]`: an animator whose current state has no clip.
