# Report: onboarding 1.7 Mark avatar padding

Plan: chunk 1.7 (D-652 Option 1)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (needs THJ's eye in Play, see "How to see it")

## What changed

- `miso/Assets/_Project/Features/UI/Panels/HUD/Avatars/Avatar_Mark.png`: 567x567 -> 600x588, original art pasted unscaled and centred on a transparent canvas. `.meta` untouched on disk (GUID `e8a20854988b6974e8b8721fc83cc74e`, import settings the same).
- Backup (byte-identical, verified with cmp): `E:/Work/Projects/miso/claude-handoff/backups/2026-11-24-avatar-mark/Avatar_Mark.png` plus `Avatar_Mark.png.meta`.

## Measurements (alpha > 8 bounds, pixels)

| Art | Size | Opaque bounds | Margins L/T/R/B |
|---|---|---|---|
| John, Linda, Lucy, Toba | 342x335 | 2,2 to 340,333 | 2/2/2/2 (soft shadow; solid black from about 6, gold line at 8, dark 10-12, gold 14, picture from about 15) |
| Mark before | 567x567 | 0,0 to 567,567 | 0/0/0/0, no border |
| Mark after | 600x588 | 16,10 to 583,577 | 16/10/17/11 |

Layout reasoning: the first attempt put the octagon where the others' picture starts (about 4.4 percent, 28 px margin). Rendered, that left a visible ring of ornament around the portrait, so I redid it at the others' baked gold line (about 1.8 to 2.3 percent inset). Final inset is 6 px at 342x335 scale: Mark's art occupies 330x323 of 342x335 (uniform scale, so the face is not squashed). Canvas aspect 1.0204 vs the others' 1.0209. Mark's pixels are not resampled at all (pure paste, no scaling), so there is no quality loss; the sprite is just larger (sprite is 6.00x5.88 units at 100 PPU, but every use is a UI Image sized by rect).

Note: others' 2 percent margin in the earlier report was the soft shadow; the real visible art edge is about 2.3 percent in. I matched that.

## Border

The others have a gold/dark border baked into their art (dark ring with a gold line near the edge). Mark now has no baked border: his octagon's own dark vignette edge sits where their border starts. I did not paint a border (the others' border follows chamfered corners; not a simple exact match). So Mark looks like a darker, borderless octagon in the same window. His octagon chamfers are larger than the others' corner cuts, so slightly more ornament shows at his four corners.

## Where Mark's portrait is used (GUID grep)

`Unit_Mark.prefab` (avatar fields for unit panel and turn bar), `PlayerController.prefab` (two references), `Resources/DialogueCharacters/Mark_DialogueCharacter.asset` (`characterAvatar`). All reference sprite fileID 21300000, which still resolves (single sprite mode regenerates the sprite rect: I checked it reads 600x588 in the editor). The `.meta` still lists a stale sprite rect of 567x567 in its sprites table; Unity ignores it for single-sprite mode and has not rewritten it. Harmless.

## Renders (edit mode, temporary additive scene, closed afterwards, nothing saved; Toba / old Mark / new Mark side by side, scratch only)

- Unit panel (`UnitAvatar` 135x135, preserveAspect off, stretches 342x335 to square, the same for Mark's new aspect): old Mark overflowed the window and covered the ornament edge; new Mark sits just inside the window edge with a thin line of ornament showing, like the others. Corners show slightly more ornament because of his larger chamfers. Looks right.
- Turn-order bar `ATBBar_mod` (Avatar 85x85 in a round AvatarBack): circular ring clips it; no visible difference except the face is about 4 percent smaller. Fine.
- Dialogue panel (`AvatarLeftImg`, preserveAspect on): new Mark has a small margin inside the frame like the Toba comparison; before, his octagon ran to the frame edge. Fine.
- Not rendered: Home or other scenes that might assign Mark's sprite at run time via the unit data (the grep shows only the three assets above).

## Acceptance criteria

- [x] Backup outside Assets, byte-identical.
- [x] Mark's art fits the others' footprint (canvas aspect, inner margin measured).
- [x] Transparency kept (octagon corners still alpha 0).
- [x] `.meta` unchanged (no setting needed changing).
- [x] All uses checked.
- Tests: none added or needed (art file only, no code).

## Save reset

no

## Decisions I made

- Used a higher-resolution canvas (pure paste, no resample) instead of scaling to 342x335, so no blur.
- Matched the inset to the others' baked gold line (about 2 percent) rather than to where their picture starts; the second looked wrong in the render.

## Needs THJ

none (look at it in Play; if the ring of ornament should be thinner or thicker it is a one-line re-pad from the backup).

## Docs to update

- build-log: note Avatar_Mark.png padded, backup path above.

## Risks and loose ends

- Mark has no baked border and larger chamfers than the others; a real match would need art (a framed version).
- Stale 567x567 rect in the `.meta` sprites table (harmless; leave).
- Unity may rewrite the `.meta` on the next reimport; commit the png only unless `git status` shows a `.meta` change.

## Proposed commits

1. `art(ui): pad Mark's HUD avatar to the other heroes' footprint`: `miso/Assets/_Project/Features/UI/Panels/HUD/Avatars/Avatar_Mark.png` (plain, art only)

## How to see it

Open a combat level with Mark in the squad, select Mark: his portrait in the bottom-left unit panel sits inside the ornament window with a thin ornament margin, like John or Toba. Also check the turn-order bar and a dialogue with Mark.

## Review (miso-reviewer, 2026-11-24)

Checked with the code chunks: only the PNG is modified, `.meta` unchanged (stale 567x567 rect ignored in single-sprite mode). Nothing else rides along.
