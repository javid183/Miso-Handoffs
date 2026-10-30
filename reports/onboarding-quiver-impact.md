# Onboarding vs Linda's Quiver (2026-10-29)

Check of the onboarding plans against Linda's Quiver, now on `main` (D-326; GDD Linda LI-3 to LI-14, Mark MA-3). By the coordinator (tech plans), the game designer (levels and design) and the narrative agent (texts). Nothing edited yet: every change below is Tier 3 and waits for THJ.

## No change

- Structure tech plan, Bond Lite tech plan, Grid → Level tech plan. Tempest Bloom's split copies spend no arrows. Rivalry's +AP is still useful at 0 arrows. The Grid → Level tool places the plain `Unit_Linda` prefab, which carries Encore.
- Narrative draft: no line is now false. Every quiver term is already in the glossary.
- M2 route A, the pile (LI-10 refills her quiver at each level start).

## Changes (designer's findings, with numbers)

| # | Where | Finding | Recommended fix |
| --- | --- | --- | --- |
| 1 | Memory 1 | Up to 3 Watch shots on enemy turn 1 empty her quiver; one arrow stays locked under a live Claw, so the turn-2 punchline arrow can't be fired. Watch also pierces, so "6 each → 2 HP" is wrong. The fallback still cites the dropped FR-4 limit | **A:** put the third Claw deeper so only 2 Watch shots fire; the turn-2 shot is her last arrow and teaches the rule. Retune HP in play. (B: +2 Quiver Size for that segment hides the rule. C: quiver switch, rejected, D-330) |
| 2 | The Ridge | 2 opening shots + 1 Watch empty her before the gauntlet (to check in play; pickups and Encore recover). The plan says the catch has "no QTE": it has one now. Out-and-back damage is 9.6 per Claw against 10 HP | Per-instance HP 8 on the two gauntlet Claws; fix the stale QTE text; optionally gate Mark's "Send one my way" bark on ≥ 1 arrow |
| 3 | M2 route B | Every arrow lands on the unreachable Archer ledge, so only Encore recovers them: an untaught second lesson | Tune the Archers' HP so the Duo + 2 arrows or Lucy's embers finish both; accept stranded arrows (alt.: make route B the Encore lesson) |
| 4 | Memories 3 and 4 | Watch may empty her in 3; John's Wrath kill may play the hand-back. Segment 4's scripted Bloom spends one arrow; whether a scripted cast respects `HasArrow` is to check | None; check in play |
| 5 | Teaching | Nothing teaches arrows, pickup or Encore | No new panel: add "Each shot spends an arrow" to segment 1's Watch panel; pickup taught by play (hand-back beats); Encore by its tooltip (alt.: a first-empty-quiver panel, or the Ridge carries it) |
| 6 | Return to Sender (D-228) | The catch already returns the arrow; it also catches Watch arrows, which cost no AP, so a refund there is free AP | "Once per her turn, catching her **bow** shot refunds 1 AP"; check what `BounceBackAndRefund` refunds after the merge |

## Texts (narrator's findings)

- Memory 1's "Three claws. One arrow." holds only with fix 1A (1 arrow left). Options: "Three Claws. My last arrow." (recommended), keep the line, or "Three arrows. Three Claws. I'm counting the first ones." if 3 Watch shots stay.
- The levels plan says "Watch Shots" (lines 175, 186, 407); the glossary dropped the term: "Watch shots".
- The Return to Sender node text should say "+1 AP" only.
- Proposed panel texts and six optional quiver beats (M1 close, a segment 3 hand-back, the Ridge catch, the pile, the Yard, first Encore) are in the narrator's report; none added.

## Branch

`thj/onboarding` (`a1483f0b9`) is behind `main` (`e5506c1e8`), which has the quiver. The onboarding build needs `main` merged into `thj/onboarding` (or the branch recut) before any chunk is dispatched. Needs THJ's yes.
