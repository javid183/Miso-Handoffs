# Linda D1: fetch cue lines and Far strings (placeholders)

Narrative agent, 2026-10-28, branch `thj/linda-quiver`. Read-only on `miso\`. For D1.3 (fetcher cues) and the D1.1 Far strings of [`plans/2026-10-27-linda-distance-design.md`](../plans/2026-10-27-linda-distance-design.md). Builds on [`linda-quiver-text.md`](linda-quiver-text.md) and today's `HandBackLines.cs`.

**Every line is a placeholder.** In data, prefix each with `[PLACEHOLDER] ` (stripped on screen, D-272). The glossary row (section 6) is a Tier 3 proposal and is not added. Everything else is Tier 2: new text in the established voice.

Rules kept:
- Toba isn't family yet (D-048): polite, slightly formal, never a family word for her or for himself.
- No "Dad" anywhere. John's reply set works without it; the old `Thanks, Dad.` stays parked until THJ decides.
- On screen it's **Encore**, never Recall (D-262). No line here names it.
- No line uses the word **Watch** (it's Linda's role name) or names a mechanic. Lucy never says "Catch" (her role bark is `Catch this!`).
- Lines are 1 to 5 words; shouts end in `!`. Each picker line works with each of Linda's replies for that picker.

Character notes (from D1.3's tosses):
- **John**, underhand lob: fatherly, warm, brief. "Love" is his word for her (already in use).
- **Lucy**, flick with a spark trail: teasing; the sparks give her a new joke (the arrow is warm).
- **Mark**, spinning throw caught one-handed: the design asks for **bragging**. Earlier I wrote him calm and koan-like (`Nothing is lost.`). These lines keep the monk's few words but let the pride show: a quiet show-off, and Linda answers in kind (it sets up their catch rivalry). Flagged in Needs THJ.
- **Toba**, short arc wrapped in a leaf: courteous, careful, the leaf is his touch.

## 1. Normal hand-back (picker under 4 cells from Linda)

| Picker | Picker lines | Linda replies | Feel |
| --- | --- | --- | --- |
| John | `Here you go, love.` · `Dropped this, love.` · `Easy now. Here.` | `Always there, aren't you?` · `Thanks.` · `Right where I need it.` | The lob from a father who keeps an eye on her; she half-teases, half-thanks |
| Lucy | `Careful, it's warm!` · `Missed one, sis?` · `You owe me!` | `Show-off.` · `You singed it, Lucy.` · `Keep your sparks off it.` | Sibling tease both ways; the sparks are the joke |
| Mark | `Mind the spin.` · `Effortless.` · `Catch it, if you can.` | `One hand. Easy.` · `Very pretty, Mark.` · `Thank you, Mark.` | His quiet pride, her dry answer; the catch rivalry in miniature |
| Toba | `Your arrow, Linda.` · `This is yours, I believe.` · `Wrapped, so it keeps.` | `Thank you, Toba.` · `That's kind of you.` · `You didn't have to.` | Formal and careful; she is warm to the newcomer without making him family |

Kept from today: `Dropped this, love.`, `You owe me!`, `Show-off.`, `Thank you, Mark.`, `Thank you, Toba.`, `Thanks.` The other current lines (`Catch, Linda!`, `Sis! Yours!`, `Nothing is lost.`, `The ground gives it back.` ...) can stay for instant pickups (G3), which keep today's beat.

Mix: as today, Linda answers with her line for that picker, or a generic one (`Got it.` / `Back where it belongs.` / `Every one counts.`) some of the time if the coder wants variety. With three per picker, the generic pool is optional now.

## 2. Call-out (picker 4+ cells from Linda)

Shouted picker line, long high arc, Linda's catch reply.

| Picker | Shouts | Linda catch replies | Feel |
| --- | --- | --- | --- |
| John | `Linda! Here it comes!` · `Look up, love!` | `Caught it!` · `Good throw!` | A father's long lob across the field; she's proud of the catch and of him |
| Lucy | `Sis! Incoming!` · `Linda! Think fast!` | `Caught it. Barely.` · `Nice try, Lucy!` | Lucy trying to make her fumble; Linda refusing to |
| Mark | `Linda! Not even looking!` · `Sister! All the way!` | `Caught. Lucky spin.` · `One hand, brother.` | He shows off, she matches him one-handed (the catch foreshadowed) |
| Toba | `Linda! It comes to you!` · `Linda, ready your hand!` | `Got it, Toba!` · `Caught! Thank you!` | Even shouting, he's polite; she answers loud and grateful |

`One hand, brother.` echoes Mark's own `Yours, sister.` register. If THJ wants fewer family words in Linda's mouth, use `One hand. Easy.` there.

## 3. Repeat line (same picker, second hand-back this turn)

Replaces the picker line; Linda's reply is chosen as usual (or skipped, if the coder wants the second beat shorter).

| Picker | Lines | Feel |
| --- | --- | --- |
| John | `Another one.` · `And again.` | Patient, a little amused |
| Lucy | `Me again!` · `That's two you owe me.` | Keeping score |
| Mark | `Again.` · `Twice now, sister.` | Fewer words each time; still pleased |
| Toba | `Another, Linda.` · `And this one too.` | Same courtesy, shorter |

## 4. Linda's own pickup (no toss, slips it into the quiver)

| # | Line | Feel |
| --- | --- | --- |
| S1 | `One more.` | The design's example; counting quietly |
| S2 | `Back you go.` | To the arrow, fond |
| S3 | `Still good.` | The archer checking the fletching |

Today's `There you are.` and `Waste not.` can stay in the same pool (five lines, fewer repeats).

## 5. Several stacks at once ("+N" beat), optional

One Linda line shown with the "+N" total, replacing her usual reply:

| Option | Line | Feel |
| --- | --- | --- |
| A (recommended) | `That many? Thank you.` | Surprised and grateful; works for every picker, Toba included |
| B | `Arms full, I see.` | Lighter; a touch teasing, less right for Toba |

Use it only when N ≥ 2. The "+N" itself follows the move-preview format: `+3 arrows`.

## 6. Far strings (D1.1)

| Where | Design text | Proposed text | Notes |
| --- | --- | --- | --- |
| Role badge tooltip | `Watch: 5×. Far (no family within 2 at End Turn): 7.5×.` | **A (recommended):** `Watch: 5×. Far (no squad member within 2 at End Turn): 7.5×.` | Toba counts for "near" (D-285) but isn't family (D-048), so "family" is wrong for this rule. "Squad" is the glossary's word (Sortie) |
| | | B: `Watch: 5×. Far (no one of yours within 2 at End Turn): 7.5×.` | Same meaning, warmer, a little vaguer |
| | | C: `Watch: 5×. Far (nobody close at End Turn): 7.5×.` | Shortest; loses "2", so the outlined box must carry the rule |
| "Far lost" label, over Linda when a ghost move comes within 2 | `Far lost` | `Far lost` | Keep it. Alt: `No longer Far` if the struck-through mark reads badly at size |
| Label when a move takes the last nearby unit away (optional) | (the mark only) | `Far` | Only if the mark alone isn't read in playtest |
| Watch prompt suffix | `· Far 7.5×` / `· 5×` | `· Far 7.5×` / `· 5×` | Format `Arrows {n} → {n-1} · Far 7.5×`. Check the TMP font has `·` (U+00B7) and `×` (U+00D7), like `→` before. Fallbacks: `- Far 7.5x` / `- 5x` |
| Far mark tooltip, optional | (none) | Player phase: `Far: no squad member within 2.` Locked: `Far until your next turn.` | Only if the mark gets a hover |

Factor values in the strings must come from the tuning asset, not typed in, so a retune (7.5× → 7×) doesn't leave stale text.

### Optional: Linda barks when Far locks at End Turn

Used only if cheap; at most once per End Turn, and not every turn (for example, only when the state changes from near to Far).

| # | Line | Feel |
| --- | --- | --- |
| F1 | `Room to breathe.` | Relief at standing apart |
| F2 | `Clear lanes.` | The archer's eye on the field |
| F3 (alt.) | `Just me and the bow.` | A little lonely; the warmth-against-dread note |

## 7. Proposed glossary row (not added; THJ approves)

For the Combat terms table:

| Term (player-facing) | Code name | Meaning |
| --- | --- | --- |
| **Far** [PROPOSED] | Far state (the tech plan names it; toggle on `LindaDistanceTuning` or similar) | Linda's state when no living squad member (John, Lucy, Mark, Toba if in the squad) is within 2 cells of her, radial footprint distance. Decoys, the Cyclone, Toba's wall, other-faction allies and the dead don't count. Checked at End Turn and **locked** until the next player turn; on the player's own turn it is checked live. While Far, her Watch deals 7.5× instead of 5×. Shown as the **Far mark** over her; "Far lost" when a move would end it. Write "squad member", not "family", in its rule text (Toba counts). "Far Watch" is the design name; on screen it's Watch plus Far |

## Data block (paste-ready)

```
Walk, picker:
John:  [PLACEHOLDER] Here you go, love. | [PLACEHOLDER] Dropped this, love. | [PLACEHOLDER] Easy now. Here.
Lucy:  [PLACEHOLDER] Careful, it's warm! | [PLACEHOLDER] Missed one, sis? | [PLACEHOLDER] You owe me!
Mark:  [PLACEHOLDER] Mind the spin. | [PLACEHOLDER] Effortless. | [PLACEHOLDER] Catch it, if you can.
Toba:  [PLACEHOLDER] Your arrow, Linda. | [PLACEHOLDER] This is yours, I believe. | [PLACEHOLDER] Wrapped, so it keeps.
Walk, Linda reply:
John:  [PLACEHOLDER] Always there, aren't you? | [PLACEHOLDER] Thanks. | [PLACEHOLDER] Right where I need it.
Lucy:  [PLACEHOLDER] Show-off. | [PLACEHOLDER] You singed it, Lucy. | [PLACEHOLDER] Keep your sparks off it.
Mark:  [PLACEHOLDER] One hand. Easy. | [PLACEHOLDER] Very pretty, Mark. | [PLACEHOLDER] Thank you, Mark.
Toba:  [PLACEHOLDER] Thank you, Toba. | [PLACEHOLDER] That's kind of you. | [PLACEHOLDER] You didn't have to.
Call-out, picker:
John:  [PLACEHOLDER] Linda! Here it comes! | [PLACEHOLDER] Look up, love!
Lucy:  [PLACEHOLDER] Sis! Incoming! | [PLACEHOLDER] Linda! Think fast!
Mark:  [PLACEHOLDER] Linda! Not even looking! | [PLACEHOLDER] Sister! All the way!
Toba:  [PLACEHOLDER] Linda! It comes to you! | [PLACEHOLDER] Linda, ready your hand!
Call-out, Linda catch:
John:  [PLACEHOLDER] Caught it! | [PLACEHOLDER] Good throw!
Lucy:  [PLACEHOLDER] Caught it. Barely. | [PLACEHOLDER] Nice try, Lucy!
Mark:  [PLACEHOLDER] Caught. Lucky spin. | [PLACEHOLDER] One hand, brother.
Toba:  [PLACEHOLDER] Got it, Toba! | [PLACEHOLDER] Caught! Thank you!
Repeat, picker:
John:  [PLACEHOLDER] Another one. | [PLACEHOLDER] And again.
Lucy:  [PLACEHOLDER] Me again! | [PLACEHOLDER] That's two you owe me.
Mark:  [PLACEHOLDER] Again. | [PLACEHOLDER] Twice now, sister.
Toba:  [PLACEHOLDER] Another, Linda. | [PLACEHOLDER] And this one too.
Linda self-pickup: [PLACEHOLDER] One more. | [PLACEHOLDER] Back you go. | [PLACEHOLDER] Still good.
Linda, several stacks (+N, optional): [PLACEHOLDER] That many? Thank you.
Far tooltip: [PLACEHOLDER] Watch: {base}×. Far (no squad member within 2 at End Turn): {far}×.
Far lost label: [PLACEHOLDER] Far lost
Prompt suffix: [PLACEHOLDER] · Far {far}× | [PLACEHOLDER] · {base}×
Far lock barks (optional): [PLACEHOLDER] Room to breathe. | [PLACEHOLDER] Clear lanes.
```

Notes for the implementer:
- The call-out swaps both the picker line and Linda's reply; a repeat swaps only the picker line. If a second hand-back is also a call-out, the shout wins (it's the bigger moment) but must differ from that picker's last line.
- No line repeats twice in a row per picker per turn: the existing `PickAvoiding` approach covers it per pool.
- Barks respect `GlobalSettingsSO.silenceBarks`.

## Needs THJ

1. **Mark's voice:** the design asks for bragging; earlier lines were calm and koan-like. These are a quiet show-off. Keep, or go back to the calm register?
2. **Far tooltip wording:** "no family within 2" contradicts D-048 now that Toba counts (D-285). Recommend option A, "no squad member".
3. **The Far glossary row** (section 7).
4. Still open from before: the "Dad" question; John's replies here avoid it.
