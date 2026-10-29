# Quiver polish 2: arrow abilities, melee recovery, auto move-attack preview

Size: M    Tier: 2 for presentation (D-308); point 3 is a rule THJ decided (D-307)    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all, built on `thj/linda-quiver` (after `7c6f5e57c`)
Status: done 2026-10-29

## Why

These come from THJ's play check of the feedback pass (2026-10-29): "All work great. A few improvements."

## Changes

1. **Every arrow ability gets the bow's HUD feedback.** The lift while hovered or selected (bar hover, number key, click) and the punch at 0 arrows apply to every ability that spends a quiver arrow:
   - the bow;
   - Explosive, Fire and Heal arrows;
   - Crescendo, if it spends;
   - the arrow Duos, if they spend.

   Decide "spends an arrow" from the same source the quiver uses to spend (`QuiverArrow` on the ability's projectile, or the quiver's own rule). Don't keep a hand-made list. The number-key and press paths cover each ability's own slot. Encore is not an arrow ability.
2. **`xN` closer to its arrow.** Move the count left by about its own width as drawn today (THJ: "left about equal to the width of x2"). It still never overlaps the arrow art badly and stays under HP bars.
3. **Melee kills hand the arrows back (THJ, D-307).** When John's or Toba's primary attack kills an enemy standing on a tile with Linda's arrows, those arrows return to her quiver right away, with the normal hand-back toss and "+N" cue, without anyone stepping on the tile.
   - Which attacks count is data on Linda's quiver: a serialized list of ability presets (John's and Toba's primaries), not code that names units.
   - Kills by anything else (her arrows, Lucy, hazards, Mark, whose strike already moves him onto the tile) work as today: the arrows unlock and stay on the tile.
   - The combat log gets the existing pickup suffix on the killing action (`· +N arrows, quiver N/4`) if that falls out naturally; no new log lines.
   - Find the kill event and the killing ability through existing events (death event with source or context). If the killer's ability can't be known without core code, STOP on this point and report.
4. **Auto move-attack previews the landing.** When Linda targets an enemy that needs a move first (auto move then shoot), the ghost arrow and the landing preview must show where the arrow will land, measured from the cell she will shoot from.
   - The unused core hook `IMovePreviewPathSource` (implemented by `PlayerController`) may already expose that path. Use it if it fits, reading only.
   - If only a core change can expose the shot cell, STOP on this point and report.
5. **Outline on the HUD quiver.** Try a narrow black contour around the quiver on her portrait so it stands out from the avatar: the body, the rim and the arrows sticking out. Start with uGUI's built-in `Outline` effect (1 to 1.5 px, black, alpha about 0.9) on the quiver's images. If that doubles up badly where images overlap, use one silhouette copy behind the group instead. Keep it subtle, don't move THJ's layout, and make sure the tint, lift and glow still look right.

## Acceptance

- [ ] Hovering or selecting any arrow-spending ability lifts the quiver. At 0 arrows, any of them punches it. Encore and non-arrow abilities don't.
- [ ] `xN` sits about one label width closer to its arrow.
- [ ] Killing an enemy standing on arrows with John's or Toba's primary returns them to Linda at once, with the toss and the "+N" cue, and the quiver feedback shows the gain. Any other kill leaves them on the tile, unlocked.
- [ ] An auto move-then-shoot target shows the ghost arrow on the true landing tile.
- [ ] The HUD quiver has a thin black outline. The tint, lift and glow still look right.
- [ ] EditMode passes, with only the known red failing. Tests cover:
  - the arrow-ability rule;
  - the melee-recovery rule: listed ability plus a kill on arrows returns them; anything else doesn't;
  - the landing-from-the-move-end-cell rule, if it is pure.

## Constraints

- No core code (`tech/core-systems.md`). Core never imports Linda (D-272). STOP on any point that needs core.
- Complexity budget (D-295): no new on-screen element. Point 3 reuses the existing toss and cue.
- No statics without a reset hook. No per-frame allocations. Every tween is killed on disable.
- Keep line endings and BOM. No private IDs in code.
- **Unity is open:** don't run batch Unity. THJ compiles and runs the tests.
- Don't touch THJ's local edits (`GlobalSettings.asset`, TMP fallback, `ProjectSettings`).

## Commit units

1. Arrow abilities feedback.
2. `xN` nudge (may fold into 1 if tiny).
3. Melee recovery.
4. Auto move-attack landing preview.
5. HUD outline.

## Commit log

THJ play-checked 2026-10-29, EditMode 994/995 (known red only). `99ae9ff09` arrow-ability feedback; `ebbd4fe68` xN nudge; `e201fb245` melee kill hand-back; `26371cc8d` move-then-shoot ghost; `19f75ff0d` HUD outline.
