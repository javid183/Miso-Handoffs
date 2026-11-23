# Report: Chunk 1.5, the hearth label and Encore's arrow colour

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.5, items X-10 and X-04)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (both need a look in Play)

## What changed

### X-10: "Start Game" over the hearth becomes "World Map"

- `Features/Home - Imported/___Khashayar/Home - Scene.unity`: one override value, `m_Text: Start Game` → `World Map`. It sits on the `HomeIndicator` prefab instance under `WorldCanvas`; the label stands at x −1.53, right above `Fireplace` at x −1.62.
- No code writes this text: only one constant `WorldMapTitle` exists, and it's an onboarding page title.
- The scene was closed in the editor; I edited the line on disk. Nothing else in the scene changed in this chunk.

### X-04: Encore's flying arrows get a visible colour

The arrow art (`Arts/Shootable/Quiver/Arrows.png`) averages RGB about (77, 88, 73), a dark grey-green. A multiply tint would only make it darker. So each returning arrow keeps its art and gets two things behind it, both in one tunable colour:
- a soft glow (the quiver's existing placeholder glow sprite, 1.6× the arrow's size);
- a short trail that fades out (0.18 s, tapering).

The files:
- New `Features/Player/Linda/Scripts/Quiver/LindaQuiver.RecallLook.cs` (+ `.meta`), with two serialized fields on Linda's quiver, under the header "Recall look":
  - `recallFlightColor`, default **warm bright gold `(1, 0.82, 0.2, 1)`, hex `#FFD133`**;
  - `recallTrailWidth`, default 0.14 of a cell (0 = no trail).
- New `Features/Player/Linda/Scripts/Quiver/GroundedArrowField.RecallLook.cs` (+ `.meta`): `DressRecallFlight(view, quiver, spacing)` adds the glow child and the `TrailRenderer`. It also owns one runtime `Sprites/Default` trail material per field, made on first use.
- `GroundedArrowField.Recall.cs`: `RecallFlight` takes the quiver instead of Linda's unit, and dresses the view once it sits at its start, so the trail doesn't streak from the field's origin.
- `GroundedArrowField.cs`: one line, `OnDestroy` destroys the trail material.
- New `Features/Player/Linda/Scripts/Quiver/Editor/RecallFlightLookTests.cs` (+ `.meta`).

`Unit_Linda.prefab` is unchanged: the new fields take their defaults from the code. THJ tunes them on Unit_Linda > LindaQuiver > Recall look. Only the Encore flight is dressed; the hand-back toss keeps its look.

## Acceptance criteria

- [x] X-10: the hearth label reads "World Map". Evidence: the scene diff (one value), and an editor read of the scene (`WorldCanvas/HomeIndicator/Indicator/Text` → "World Map"). **Play check:** see it at Home.
- [x] X-04: Encore's flying arrows carry a clearly visible colour, as a serialized value THJ can tune. Evidence, `RecallFlightLookTests` (5 tests):
  - `TheDefaultColourIsABrightOpaqueGold`;
  - `LindasPrefabUsesABrightColourAndATrail`;
  - `AFlyingArrowGetsAGlowBehindItAndATrailInTheColour`;
  - `ZeroTrailWidthDrawsNoTrailButKeepsTheGlow`;
  - `NothingIsAddedWithoutAQuiver`.
  - **Play check:** contrast on a memory level and on a forest level.
- Tests: the quiver fixtures with the new one passed 102 of 102. Clean compile, no console errors.
- Full EditMode suite (one run after chunks 1.2 and 1.5): 2529 total, 2525 passed, 1 skipped (the Explicit AI regression test), 3 failed, all "m_LockCount == 0" in `GridToLevelFacingTests`, `GridToLevelSettingsTests` and `GridToLevelXpTests` (the known editor-open flake). Rerun alone, those three fixtures passed 34 of 34. So: 0 real failures.

## Chunks

### Chunk 1.5: hearth label and Encore colour

- Changed: see "What changed".
- Criteria met: both, pending the play look.
- Decisions and loose ends: below.

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- Glow plus trail instead of a tint, because the arrow art is too dark for a multiply tint to brighten (Tier 2 presentation). The colour is one field for both.
- The glow size (1.6×), trail time (0.18 s) and start alpha (0.9) are constants, not fields, to keep the inspector to what was asked. They are easy to promote.
- A new public method on the field (`DressRecallFlight`), so the look can be tested in edit mode.

## Needs THJ

none

## Docs to update

- Linda's character page / Encore: the returning arrows glow gold with a short trail (colour and trail width tunable on her quiver).

## Risks and loose ends

- **`Home - Memory.unity` also says "Start Game"** on its own `HomeIndicator` (line 4643). That scene is the game's `introScreen` in `Program Flow Data.asset`. The brief named the Home scene only, so I left it. If the player sees the hearth label there too, it needs the same one-value change; it is Khash's scene as well.
- **Overlap with chunk 1.6:** `Home - Scene.unity` also carries 1.6's three `UnlockAfterMissions` lines (stations). My change is a separate hunk (line 4449). Commit 1.6 first or stage by hunk.
- **No overlap with chunk 1.4's quiver files:** this chunk didn't touch `LindaQuiver.cs`, `RecallRules.cs`, `QuiverTextRules.cs` or `QuiverAbilityInfo.cs`.
- The trail uses `Shader.Find("Sprites/Default")`, the same as the Encore line presenter. In a player build that shader must be included; it already is wherever the line works.

## Proposed commits

1. `tweak(home): the hearth label says World Map` (plain; after chunk 1.6's commit, same file):
   - `miso/Assets/_Project/Features/Home - Imported/___Khashayar/Home - Scene.unity` (this chunk's hunk only)
2. `feat(linda): Encore's returning arrows glow and trail in a tunable gold`:
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.RecallLook.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/GroundedArrowField.RecallLook.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/GroundedArrowField.Recall.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/GroundedArrowField.cs`
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/RecallFlightLookTests.cs` + `.meta`

The brief asked for one commit per chunk. These two are independent (a scene string and a code feature), so I list them apart. They can be squashed if THJ prefers.

## Other branches

none

## How to see it

1. Open Home (from a save past the opening, or start Play from PreloadScreen into Home). The label over the fireplace reads "World Map".
2. Play a memory or level with Linda. Shoot a few arrows so some lie on the ground, then cast Encore. Each arrow flies back with a gold glow and a short fading trail.
3. To tune: select `Unit_Linda` (Features/Player/Linda/Prefabs). On LindaQuiver, under "Recall look", change Recall Flight Color and Recall Trail Width.

## Coordinator check (2026-11-23)

Size S, outside core: no reviewer (gate 3). Read the diff: 1.2's four sequence assets each lose exactly the two step references (input, HUD); 1.5 is one scene string and a small look change with serialized colour and width. Accepted. Look and timing go into THJ's batched Phase 1 play check.
