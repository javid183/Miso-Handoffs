# Quiver readability: strip down to one quiet layer

Size: M    Tier: 2 (presentation only, inside THJ's D-293, D-294, D-297)    Assigned to: miso-implementer, reviewer; THJ plays
Branch: all, built on `thj/linda-quiver`
Status: approved by THJ in conversation 2026-10-28; ready to dispatch

## Why

The quiver's feedback grew into many layers of text, rings, badges and labels. THJ: one readable layer, no big texts over the board, it must look like the game (D-293, D-294). He added art: `Features/Player/Linda/Arts/Shootable/Quiver/`.
- `Arrows.png`: sprites `Arrows_0` and `Arrows_1`, two arrow variants.
- `Quiver.png`: `Quiver_0` is the quiver body, `Quiver_1` its front rim.

## Goal

The arrow count reads from one place, the quiver on Linda's unit panel. The board shows only the arrows themselves.

## Changes

**Remove:**
- the panel text "Quiver N/size";
- the Watch prompt line "Arrows N > N−1";
- the "+N arrows" move-preview label;
- every count badge, count label and outline on grounded arrows;
- the landing ring.

**Keep:**
- the "+1" return cues;
- the small pips under Linda's feet (THJ: for now; if too much, later only while Shift is held);
- the grey-button reasons, in the tooltip only.

**Change:**
- **Grounded arrows:** draw the new arrow art, `Arrows_0` or `Arrows_1` chosen per arrow and stable for that arrow.
  - A stack shows up to 3 overlapping arrows, with small offsets, and no number.
  - Arrows under a living enemy get a subtle dark tint, with no badge.
  - Draw them below every HP bar (on the pips' layer, D-280), because they currently hide the HP bar of the enemy they hit.
- **Landing preview:** while aiming, a faint ghost of the arrow art on the landing tile replaces the ring.
- **Encore lines:** curved lines from each stack to Linda, drawn with the same renderer and style as John's role tether or the enemy threat lines. The implementer finds which one and reuses it.
- **HUD quiver** on Linda's unit panel, next to her portrait:
  - `Quiver_0` body, then one arrow sprite per arrow in the quiver drawn inside it, then the `Quiver_1` rim over them.
  - Empty means an empty quiver.
  - It replaces the panel pips and the panel text.
  - It shows only when Linda's panel is shown.
- **Empty-quiver role badge:** it stays as the only empty state on the badge, with its tooltip line.

## Acceptance

- [ ] No arrow-related text is drawn on the board or the panel; only tooltips have words.
- [ ] Linda's panel shows the quiver, with exactly as many arrows as she has. It updates on spend, pickup, catch and Encore.
- [ ] Grounded arrows use the new art. Stacks show as overlapping arrows. Locked arrows are subtly tinted. They never cover an HP bar.
- [ ] The aim preview shows a ghost arrow on the landing tile and no ring.
- [ ] Encore lines are curved, in the same style as John's tether or the threat lines.
- [ ] The "+1" cues and the pips under Linda are unchanged.
- [ ] Dead code from the removed elements is removed, not just hidden. Tests that asserted removed text are updated or deleted.
- [ ] EditMode passes, with only the known red failing.

## Constraints

- Complexity budget (D-295): no new elements beyond the HUD quiver.
- No core code. Core never imports Linda (D-272).
- Lessons from D-280 to D-282: sorting below HP bars, `QuiverLevelAccess`, no root objects created in `Start`.
- No per-frame allocations.

## Gates

THJ compiles and tests in the open editor. Review, then THJ plays. Commits only after his play.

## Commit log

Committed on `thj/linda-quiver` 2026-10-28 after THJ's play check (EditMode 955/956, known red only):
- `d2a377569` core `Projectile` per-frame sweep and hit set (D-300)
- `3fdbb08f1` combat log holds the action line; features annotate it; quiver count suffixes (D-299)
- `ff739b5ae` strip-down to one quiet layer (D-293, D-297, D-298)
- `018b1e5a1` smaller pips and +1 cues (D-299)
- `039697fe2` kinematic bodies on Linda's arrow prefabs (D-296)
- `79ca381e8` arrow and quiver art, wired on Linda, wiring tests
