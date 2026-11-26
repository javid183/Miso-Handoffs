# M3 "Hold the yard" greybox play check (THJ, 2026-11-25)

Build: thj/onboarding-demo, M3 6.1–6.3 + review fixes (uncommitted in the shared repo; THJ declined the commit popup at shutdown). Raw words (THJ):

> hold was not hard at all, it was actually too easy. the yard was. Mark should stay pushing the stone and be taken out of the squad as a playable character. He should only be a target of enemy attack. Yes, build the barriers, but put the masher on the other side. Yard was too difficult and too small for his aggressive reaction. he can also easily break barriers and push claws. lets make the corridors 3. and enemies tougher. But do not do it now.

## Structured (coordinator)

1. **The hold is too easy** (the wave fights). → enemies tougher.
2. **The yard opening is too hard / too small** for the Masher's reactive counter.
3. **The pusher:** Mark stays on the stone and leaves the playable squad; he is only a target for enemy attacks. (Today: the pick, John or Mark, is playable and pushes; D-622.) Open: Mark fixed instead of the pick (what about John in M3?), how "not playable" is built (Inactive like M1's held Linda, D-712?), whether the pick-falls defeat (D-718) stays as "Mark falls".
4. **Barriers: build them** (chunk 3.0; reverses D-689's "greybox first, decide later"). Core AI (`AIUnitBrain`, a blocked enemy attacks the blocker).
5. **The Masher moves to the other side** (outside the yard, in a lane, coming as an attacker): he breaks barriers easily and pushes Claws (plow, D-573). Reverses D-688's yard placement.
6. **Corridors 3 wide** (the lanes and necks; today 1-wide necks 2,3 / 8,3). Needed for the 2×2 Masher to come through (D-688 §11 option b).
7. **Not now.** Next session: designer reworks `m3-defence` (layout, Masher, enemy factors, Mark's role) → THJ approves → barrier tech plan (core, Tier 3) → build.

Also seen: the mushroom tally credit was broken in this build (re-check must-fix; fix dispatched, D-720).
