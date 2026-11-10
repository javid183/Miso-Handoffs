# Family Roles, round 2: creative critic

Critic: `miso-design-critic`, **creative lens** (player feeling, fantasy, moments, originality, family-under-pressure tone). Reviewed: [`2026-11-09-family-roles-round2-design.md`](2026-11-09-family-roles-round2-design.md) (draft, with S1 to S3), against round 1, `vision.md`, `design/gdd/family-systems.md`, the four character sheets, `narrative-world.md` and the 2026-11-09 pacing check. Read-only; 2026-11-09.

## Strongest objection: P arms every role with a solo stance, so the family drops out of the setup

The draft's principle is "each role is armed by a choice on the hero's own turn, made with something that hero already does". Every arm in P is about **that one hero**: John raises *his* shield, Linda turns *herself* to a lane, Mark has *his* Focus, Lucy has nothing to arm. The FR-1 fantasy is "a reactive passive that **protects or supports the family**", and the USP is that the family fights as a family. In P, nothing in the setup depends on where the *other* Bergsons are or who they are. That is why P lands so near the genre default, as the draft's own creative note admits: a shield stance and an FFT/XCOM facing cone, with skins. It is also where the over-the-bar moments went. THJ's two most family-shaped ideas were the ones that made a role about someone else: **John swaps places at any range** (the father reaching his child) and **Linda's minimum range 2** (the draft says it itself: "Family Watch literally watches over the family"). P defers both. What remains fixes "you never know what you did", but it answers with *"I raised my shield"*, not *"I kept Lucy where Papa could reach her"*. The first sentence is a stance. The second is a family. **Change:** keep THJ's verb gates (Shield Up, facing, Focus), and make each **trigger relational**: John's guard reaches the family member in danger (J3, point 1); Linda's Watch fires for enemies that come for a sibling (point 2); Mark already counters only for hits on others (keep it, point 4); Lucy's fallback joins whoever is beside her (point 5). The rules stay one sentence each, and the setup becomes "where I put the family relative to each other". No other tactics game has that, and it is what players praised in the cyclone shot.

## Points

### 1. The swap is the heart of THJ's John, and the plan's test can kill it without ever playing it

S2 shows the problem. Under J1 + J2 the press has a real cost only at Wrath 2, when the shield is about to break. Every other guard press is still "always yes", which is THJ's "just a click". The swap gives **every** press a consequence you can see: John leaves the chokepoint, Lucy lands beside the Claw that has already struck (S2's J3 row), and the next enemy re-plans around a father who is now in the wrong place. That is warmth against dread inside one prompt, and it is the only moment in the plan that a player would describe to a friend ("Papa crossed the whole room"). The plan defers it (Q3 a: "decide after the session"). But the D-460 stop rule says two clear noes on John and Linda mean **lock roles as built**. So a session that tests a John without his best idea can end the topic before the swap exists. The halfway option, "any range without the swap", is the worst of both: the cost of reach, with no fiction ("how does he take it from across the room?" is the draft's own line).
**Change:** (a) Amend the stop rule: a "no" on John is not final until J3 has been played. (b) Make J3 code chunk 2, behind its own toggle, ahead of L1. Its readability risk is a presentation problem (a swap beat, FR-13's tether already drawing at any length). That is a reason to stage it well, not to test without it. (c) Drop "any range without the swap" from Q3. (d) The area-guard loss (one swap covers one ally) suits the fiction: a father can only stand in front of one child at a time. Say so to THJ as a feature, not a loss.

### 2. Linda's lane is overwatch with a skin. Make Family Watch watch the family.

L1's default (she faces where she last shot) means that most turns the lane is chosen by accident, so "you never know what you did" comes back in a new form ("she happened to shoot north"). And "watches a lane" is the most familiar reaction in the genre. THJ's minimum-range idea was reaching for something better, and the draft names it: Watch then fires "on enemies going for someone else". It is rejected for cost, but only because it was framed as a **bow** rule (core targeting, every preview, Memory 1 retunes).
**Change:** make it a **Watch-only trigger filter**: *"Linda's Watch fires on an enemy that ends its move in her lane next to another Bergson."* Her bow is untouched, so there is no core targeting work and no preview churn: it is a check in `LindaFactionRoleHandler`. Keep THJ's facing on top if he wants it, or let the filter replace the facing (one fewer new on-screen element, and no picker). What it does on the draft's own boards:
- **S1:** 2,4 ends on 2,2, beside Mark: Watch still fires. The ★ line holds.
- **S3:** the east ★ changes. 7,1 ends on 3,1 next to Linda only, so there is no Watch. The north line now fires for the Claw going for Mark. The choice becomes "cover my brother or cover myself", which is a family decision, not a geometry one.
- **Memory 1** (Linda alone): Watch can never fire, which is exactly THJ's "no FR before John", with **no per-level switch**. P otherwise needs that switch (the draft's own Hearth table).
- **Tempest Bloom:** the cyclone drifts toward units, so it is usually near the family, and the loved shot stays possible and stays a surprise.

L2 (the last arrow) is bookkeeping with no fantasy. If it stays, frame it as *"she keeps her last arrow for herself"* and give it a bark.

### 3. J2 is the best fit in the plan. Frame it as Wrath boiling over, not a shield breaking, and pay it off on the right enemy.

A father whose shield fills with anger until he has to strike is John: JO-1 already turns pain into damage. But the draft's beat is "Shield broken" (placeholder popup, greyed "Strike first"), which tells the player John failed. The fiction is the opposite: he has taken three hits for his daughters and **he is done defending**.
**Change:** (a) Name and stage the moment as Wrath overflowing: John lowers or throws aside his shield and barks (for `miso-narrative`, e.g. "Get away from them!"). The greyed Shield Up tooltip reads like a promise ("Wrath first"), not a block. (b) Close the loop with **Blood Debt** (JO-2). Today a guarded hit hurts no family member, so the Claw that went for Lucy carries no mark, and John's punish can land on anyone. Make *an enemy whose attack John took for an ally* carry Blood Debt. Then S2's turn 2 becomes the Sword at Wrath 3 (×2.05) × Blood Debt 1.3 on **the Claw that went for Lucy**. That is the memory's lesson as a story, not as arithmetic. It is a small, non-core change on the Blood Debt passive, to check. (c) Keep the mid-turn loss of the ×0.6. Being unshielded for the rest of the enemy turn is the dread half, and it is right.

### 4. Mark: M2 has the right fiction, but Focus 0 erases him at the moment he rejoins the family

"He spends his calm to strike back for them" fits a Zen monk well, and the barrier dropping as he counters (then the next hit landing on him) is a good small sacrifice. But his story is **how he rejoins the family** (narrative-world), and his first fights under P (the Ridge, after the Hearth) open with no counter at all: S1 confirms he shows nothing on turn 1. His first impression would be a brother who doesn't answer.
**Change:** start Focus at **1** by default, not as a lever ("he arrives centred"). Give the press a visible cost beat: the Focus pip drop is too quiet; add a short barrier-shatter flash on Mark as he dashes. Keep M3 (bodyguard) off. It is relational, but its press is "always yes", and with point 1 John already owns "stand by this one".

### 5. Lucy: the preview is right. Reject Kindle; if a fallback is needed, she joins whoever is beside her.

U1 trades her player-turn surprise for legibility. That's correct: the surprise THJ named was "randomly coming about", not delight. The delight survives on the enemy turn (a Watch or a counter that she chains), and the draft keeps that unpreviewed. But U3 Kindle (*"follows up on enemies her own embers hit"*) makes the youngest daughter's role about herself, and it makes her act **first**, setting up others. Her fire is the opposite: she joins in when the family strikes.
**Change:** replace U3 with *"Lucy follows up the strikes of a Bergson standing beside her."* It is armed by keeping her close to family. That fits a fragile 15-HP child and Papa's Shelter (LU-2) already pays for standing by John. It is a filter in her handler, with no new mark on enemies.

### 6. Where the press has no choice, give it skill. That is the other half of "just a click".

After P, Linda's and Lucy's presses still have one right answer (always press), and so do John's below Wrath 2 unless J3 lands. Pillar 1 is "reaction timing", and FR-2 already lists a **graded QTE** as the next planned experiment. Arming fixes "you never know what you did"; it does not fix "no challenge" at the moment of the press.
**Change:** split the presses in two. Presses with a **choice** (John's guard or swap, Mark's Focus spend) stay a simple press with a 1 s window: the decision is the challenge. Presses **without** a choice (Watch, Lucy's follow-up) get the graded QTE (a small bonus for a tight press). Add one question to the session read: *"Did you tell anyone about a role afterward? Which one?"* P's paper scenarios count decisions and prompts but never test for a moment. S2's J3 row and a River Shield-Up-beside-Lucy chain are the two to watch.

## Per option

- **A (as built + Lucy preview):** ship only as the stop-rule fallback. It keeps the love and leaves THJ's "wrong".
- **C (kept AP):** don't ship. The draft's withdrawal is right. Doing nothing never feels like protecting anyone.
- **P:** ship with changes. J1 + J2 as is, with the Wrath framing and the Blood Debt link (point 3). Replace L1/L2 with, or add, the family-threat filter (point 2). M2 with Focus 1 (point 4). U1, with Lucy's fallback replaced (point 5). Graded QTE on the presses without a choice (point 6). And the stop rule must not judge John without J3.
- **P+ (THJ's full set):** ship the swap; leave the rest. Stamina-replacing-Wrath and the ember pool add counters without fantasy, and the draft is right to fold stamina into Wrath. The minimum range belongs on Watch, not on the bow.

## What would change my mind

- **On the swap:** if, in the J3 play check, THJ or a cold player can't say which ally John swapped with after the enemy turn, or the board after a swap reads as a bug. Then range 2 without the swap is the honest version.
- **On Linda's family filter:** if on the Ridge and the River it fires under about 1 in 4 enemy turns with enemies in range (the draft's own failure bar). Then the facing lane alone is the fallback.
- **On the strongest objection:** if session players describe the solo arms in family terms anyway ("I raised John's shield so he could cover Lucy"). Then relationship is already emerging from the stance, and P stands as drafted.
