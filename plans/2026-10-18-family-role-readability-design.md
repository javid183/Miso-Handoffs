# Family Role readability under FTP (B4 + Q7)

Size: M    Tier: 3    Assigned to: miso-game-designer (design); implementation later by miso-implementer
Branch: `thj/oct-build-fixes` (= `main`, FTP). Applies equally to `thj/home-test` (also FTP until D-036/D-042 merge). Every rule below is written so it still holds once roles are free with per-round limits (D-036, D-042).
Status: Phases 0 and 1 approved in principle by THJ (D-062), item list awaiting his final look; Phases 2 and 3 and the rule changes batched into the Family Role chunk

Inputs: [`playtests/2026-10-playtest-tasks.md`](../playtests/2026-10-playtest-tasks.md) B4, Q7 (neighbours Q6, Q18, Q19, Q20, S5, S9), fact sheet [`reports/b4-family-role-facts.md`](../reports/b4-family-role-facts.md), [Family systems](../design/gdd/family-systems.md), [Combat rules](../design/gdd/combat-rules.md) CR-11 to CR-13, CR-28, decisions D-034, D-036, D-039 to D-042, D-048, D-051, D-061.

Critics: **not spawned.** I sized this M: Phase 1 is UI-only and reversible, and every rule change that would make it L is split out as its own question for THJ rather than decided here.

---

## Why (problem and evidence)

**Root problem in 3 lines.** The player can't tell *no trigger* from *trigger, but blocked*. Every non-fire is silent, and the rule geometry (John's and Mark's diamond, Linda's cross) appears only when the player hovers a small panel icon. About half of what reads as "missing UI" is actually rules that surprise the player or plain bugs. More feedback can't fix those, so they are listed separately below.

**Which of the fact sheet's five confusion causes matter most:**

| # | Cause (fact sheet) | Weight | Nature |
| --- | --- | --- | --- |
| 5 | No feedback on non-fire or a miss; a miss looks like "nothing happened" | **Highest**: it hides causes 1 to 4 | Missing UI |
| 2 | Linda's lane is a cross (no diagonals); teleports and jumps never trigger her | **High**: it's what S and J reported ("why did Linda's QTE not fire") | Rule (cross: intended) + rule gap (teleports) |
| 1 | FTP empty is indistinguishable from "no trigger" | High today, **gone after D-036**. It becomes "no uses left" under the limits, so the same slot in the UI | Missing UI (the state is readable today) |
| 3 | One role per event; a QTE that can't start is skipped and **silences** the target; a miss silences the enemy for the turn | Medium (narrow collisions), but feels like a bug when seen | Design gap + one bug |
| 4 | John gives no cue until the paused prompt; his diamond ignores his footprint | Medium (John is 1×1, so the footprint part is moot today) | Missing UI |

**Bugs and rule gaps: fix rather than explain.** Owners follow `escalation.md`: data and obvious bugs are TD, Tier 1 or 2 (core bugfix = Tier 2, flagged); rule changes are THJ, Tier 3.

| Item | Verdict | Who decides | My lean |
| --- | --- | --- | --- |
| Mark's prompt uses `LucyQTE` (Lucy's key and icon) | **Bug** (copy-paste in prefab data) | TD, Tier 1 | Fix in Phase 0 |
| A QTE that can't start (another QTE up) runs the *ignore* path and **silences** that target for the turn (verified: `PlayerController.cs:1556-1561` calls `ignoreActions`, which calls `SilenceFactionRole`) | **Bug**: the player didn't miss anything | TD, Tier 2 (core bugfix) | Skip without silencing. Phase 0 |
| `Targets.Except(SilencedTargets)` may be null before the first selection change | Possible bug (unverified) | TD, Tier 2 | Null guard. Phase 0 |
| Mark checks only the attacker's **anchor** cell (big enemies just outside) | **Bug** against the GDD rule "attacker within 2 cells" | TD, Tier 2 | Use footprint distance like Linda and Lucy. Phase 0 |
| Lucy searches only the **first** hostile faction, in list order | Bug-ish; target choice is unspecified | TD, Tier 2 (pick between options the spec leaves open) | All hostile factions; prefer an enemy the action targeted, then the nearest. Phase 0 |
| Mark blocked when the same hit **also targeted Mark** (base guard) | **Rule question**: probably unintended ("attacks anyone who attacks family"; Mark is family) | **THJ** (Q3) | Let Mark strike back; his 1-per-round limit (D-042) caps it |
| Teleports and jumps into Linda's lane raise no event (`AEffectTransporter.cs:243,294`) | **Rule gap** | **THJ** (Q4) | Count them once the limits exist (Linda capped at 2) |
| One role per event: the wait list fires the first feasible role and drops the rest | **Design gap** | **THJ** (Q2) | Queue them (see Option D note) |
| Miss silences that enemy for the rest of the turn | **Rule**, but undocumented | **THJ** (Q5) | Keep the rule, make it visible, scope it to "this turn" for real (today it clears only on a selection change) |
| Stunned or downed role unit: no stun check found | **Rule gap** | **THJ** (Q8) | A stunned unit can't react; show it on the badge |
| Linda's cross (no diagonals) | **Intended** (an archer's lane; D-039 keeps the trigger) | Explain | Make the cross visible |
| John triggers on any enemy action that targets an ally, not only damage | Intended as coded; rarely visible | Explain | Tooltip line; no change |
| FTP checked, not reserved (`TryConsume` ignored) | Bug, moot after D-036 | TD | Leave; Pilot 1 removes the cost |

## Goal

The player can always answer two questions: *who is watching over whom right now*, before the enemy moves, and *why a role did or didn't answer*, right after it happens. The answers come in the family's voice and add no clutter during enemy turns.

---

## Lens notes

### Creative

**Target experience.** The family keeps watch over each other, and you can *see* it: John's shield around Lucy, Linda's arrows lining the corridors. When a role answers, it's a warm beat ("I got you!"). When it can't, the family tells you in their own words ("No clear shot!", "Linda's got it!"), not a system error.

**The moment we design for.** Enemy turn. A wolf lunges at Lucy, who stands diagonal to John. The player already knows she's covered, because her tile sat inside John's shield zone when they moved her there. John: "No!" The prompt appears, the player presses, the insert shows John: "I got you!" The counter-moment: the player misses, and John mutters "Too slow..." while Lucy takes the hit. The player knows exactly why, and that it was on them.

**Originality.** The genre default (XCOM overwatch icons, Fire Emblem danger zones) shows the zones. Our twist: the *reasons* come as family barks. A dropped role acknowledges the one that fired ("Linda's got it!"). That turns a technical limit (one role per event) into a moment of the family covering each other. Barks are cheap: the prompt and execute fields already exist on every Bergson's `GUnit` (`unitFamilyRolePromptText` / `unitFamilyRoleExecuteText`; set on John, Linda, Lucy, Mark; values checked only for John: "No!" / "I got you!"). Nothing plays them today.

### Systems

**Reason-code catalogue (why a role didn't fire).** The player sees five reasons. Everything else stays silent on purpose. Wording is placeholder for `miso-narrative`; the code name is for the TD.

| Code | Player words (glyph + bark example) | When it applies | Who | Tell the player? |
| --- | --- | --- | --- | --- |
| `NoUses` | Glyph: empty pip. Today: "No FTP". After D-036/D-042: "No Watch left" (FR-6 name, proposed). Bark: Linda "Out of shots for now." | The trigger was otherwise valid, but FTP < 1 (today) or the round's uses are spent (later) | Today all four; later Linda, Lucy, Mark (John unlimited) | **Yes**, at most once per role per turn. After that, the panel badge carries it |
| `Missed` | Glyph: cracked prompt. "Missed. Won't react to <enemy> again this turn." Bark: John "Too slow..." | The QTE ran and the press didn't land | All | **Always**: it answers a player input |
| `Busy` | Glyph: two heads. Bark from the dropped member: Lucy "Linda's got it!" | Another role took this event (wait-list drop), or another QTE was already up | Linda, Lucy, Mark (John only on an active QTE) | **Yes**, a bark only. Goes away if THJ picks queueing (Q2) |
| `NoLine` | Glyph: broken arrow on Linda. Bark: Linda "No clear shot!" | An enemy ended its move inside Linda's radius but off her cross, **only on an exact diagonal** (\|dx\| = \|dy\|). If THJ keeps the current teleport rule (Q4), this also covers a teleport or jump that lands in her lane | Linda | **Yes**, at most once per enemy turn, never on the player's turn |
| `CantReact` | Glyph: stun star on the badge | The role unit is stunned or downed (if THJ rules so, Q8) | All | **Badge only**, no popup |
| *Silent* `NothingInRange` | none | No valid trigger in the zone: every ordinary enemy move | All | **No.** The zones teach this |
| *Silent* `WrongTurn` | none | John or Mark on the player or ally turn | John, Mark | **No.** Tooltip says "Enemy turns only" |
| *Silent* `InvalidTarget` | none | Target dead, downed, immune, tag mismatch, Lucy's "hit last" skip | All | **No** |
| *Silent* `OwnAction` | none | The last action was the role unit's own (chain guard) | All | **No** |
| *Silent* `SelfInvolved` | none | Mark: the hit also targeted him | Mark | **No**. Recommend removing the rule instead (Q3) |
| *Silent* `Silenced` | none | Target silenced after an earlier miss | All | **No.** The `Missed` message already said so |

**How it holds once roles are free with limits:** only `NoUses` changes its words (FTP becomes Watch). The code, glyph, rate limit and slot stay the same. Fireside's +1 first-round use (D-040) appears as one extra pip with a fire mark, which makes a Home effect visible in combat (S4's ask).

**Rate limits (anti-spam levers, start values):**
- At most **one** reason popup per role per turn, and at most **two** on screen across the family at once (the newest replaces the oldest).
- Bark and glyph show for **1.2 s** at the unit's head (shorter than the insert's 1.5 s `dialogueDuration`) and never move the camera.
- `NoLine` fires at most once per enemy turn; `NoUses` once per role per turn; `Missed` always (one per QTE by nature).
- Lever if it's still too noisy: limit `Busy` and `NoLine` to the first 3 fights of a run or a toggle ("Family hints"). Don't start there.

**Interactions:**
- **Silencing.** The `Missed` text names the consequence, so the silencing rule becomes learnable. The `Busy` path must not silence (Phase 0 bug).
- **Q19 undo-move.** Undo is already blocked once a move triggers a role QTE. Reason popups must not count as a trigger (no QTE ran).
- **Enemy-turn speed (Q4).** Popups never pause the game and never wait for input. Queueing roles (Q2) adds about 1.5 to 2 s per extra role, the only real cost to pace.
- **Combat log.** The log is an editor window today (`CombatLogWindow`; entries are "what an in-game log panel would show"), so a log line is **for QA, not for players**. Log every reason, silent ones included, as Balance entries. That is also how QA logs the "remaining FTP bugs" B4 asks for.

**Failure cases:**
- *Duplicated rules.* A UI that recomputes "would Linda have fired" drifts from the handlers. That's why every **in-the-moment** reason waits for Phase 2 (reasons come from the handlers). Phase 1 shows only static geometry and the readable resource state.
- *Noise.* Too many barks during a 6-enemy turn. Mitigated by the caps above and by keeping the silent set large.
- *Misleading zone.* John's zone uses his anchor cell. Fine while John is 1×1; if a big John form ever exists, the zone must use his footprint.

### UX

**What's shown when:**

| Moment | Shown | Player clicks |
| --- | --- | --- |
| Player turn, unit selected | That unit's **role zone** drawn faintly on the grid, not hover-only: John and Mark as a filled diamond (radius 2, the four diagonal neighbours included, the (2,1) cells not), Linda as **arrow lines** along her row and column out to her radius, Lucy as a soft ring (radius 3). The diamond-versus-cross contrast *is* the diagonal lesson Q7 asks for | Nothing new |
| Moving a unit (move preview) | On the hovered destination tile: small **cover icons**, a shield if that tile is inside John's zone, a fist if inside Mark's. When the moving unit is John or Mark, the zone moves with the preview so the player sees who they'll cover from there | Nothing new |
| Hold a key (proposed **Alt**, "Family watch") | All living Bergsons' zones at once, each in its character colour (shares Q20's palette) | Hold / release |
| Always (player and enemy turns) | **Role badge** on the unit panel and a small pip beside each Bergson's mini HP bar (Q6): lit = ready; empty pip = `NoUses`; stun star = `CantReact`. Today the pip count is "1 if FTP ≥ 1"; later "Watch 2/2" | Hover the badge for the tooltip (exists) |
| Role triggers | Prompt bark at the role unit ("No!"), then the QTE as today. **John:** a short tether line from John to the ally he's covering, drawn during the paused prompt | Press |
| Press lands | Insert panel plus execute bark ("I got you!") through the existing `FactionRoleVisual.ShowWithDialogue` (verified: it's the path Revenge uses, `CombatLevelUIManager.cs:405`) | — |
| Press missed | `Missed` glyph and bark at the role unit, plus the one-line consequence ("won't react to <enemy> this turn") | — |
| Blocked but eligible | Glyph plus bark at the role unit (table above), 1.2 s, no camera move | — |

**The misread most likely to happen:** reading the zone as *where enemies must stand* when, for John and Mark, it's where the *ally* (John) or the *attacker* (Mark) must be. Mitigation: John's diamond shows a shield glyph on allies standing inside it; Mark's shows a fist on enemies inside it. The glyphs tell "who must be in it". Second misread: thinking `NoUses` means the role is gone for the fight. The tooltip says "refills next turn" once limits exist, and today "needs 1 FTP; Pass-by refills FTP".

**Inspirations used:** XCOM (overwatch and flank icons on the move destination tile, the clearest "what happens if I stand here" in the genre); Into the Breach (everything an enemy-turn reaction depends on is visible before you commit); Fire Emblem (hold-to-show danger zones, our "Family watch" key); Marvel's Midnight Suns and Persona 5 (character inserts and one-liners as reward feedback, which we already have); our own Home M9 rule "dead seats are disabled with a reason" ([`design/m9-readability.md`](../design/m9-readability.md)), the same principle carried into combat.

---

## Options compared

| | A. Tooltips + bug fixes | B. UI-only clarity | **C. B + reason codes from the handlers** | D. C + rule changes + "family pile-on" |
| --- | --- | --- | --- | --- |
| What the player sees | Exact rule text in the hover tooltip; Mark's correct prompt | Always-on zones, destination cover icons, role badges and pips (FTP state), barks on prompt, success and miss | B, plus the in-the-moment reason glyph and bark when a role was eligible but blocked (`NoUses`, `Busy`, `NoLine`) | C, plus every eligible role fires in sequence (no `Busy`), teleports trigger Linda, Mark answers when hit too, and a chained insert when two roles answer one event |
| Experience | Still silent in the moment | Most "why" answered *before* the enemy moves; the miss is visible | The "why not" answered *after*, in the family's voice | Strongest USP moments; longer enemy turns |
| Rules complexity | none | none | none (reporting only) | +3 rule changes |
| Effort | S | M (2 to 3 days) | M + M (about 2 days more, with tests) | L (> 3 days on top of C) |
| Core touched | Phase 0 fixes only (Tier 2) | **No** (`UnitPanelUI`, `FactionRoleVisual`, barks and grid overlay listen and read public getters). One assumption: miss detection from `qteStarted`/`qteEnded`/`onFamilyRoleActivated` (see Risks) | **Yes, Tier 3**: handlers return a reason; a new additive bus event `onFamilyRoleSkipped(handler, reason, target)`; the controller raises it at the FTP check, the wait-list drop, the busy QTE and the miss | Yes, Tier 3 behaviour changes in `FactionControllerBase`, `AEffectTransporter`, the Mark handler |
| Risk | Low | Low; overlay clutter on small boards | Medium: touches the role pipeline the Pilot 1 limits also touch, so build it in the same pass | High: pacing, balance (Linda over-triggers), AI regression |
| Holds up under free + limits | Yes | Yes (pip count switches source) | Yes (`NoUses` reworded only) | Yes |
| USP effect | Neutral | Family Roles + | Family Roles ++ | Family Roles +++, but needs THJ's rule calls |

---

## Recommendation

**Option C, built in phases.** D's rule changes are put to THJ one by one (Q2 to Q4). Each can be added on top of C without redoing it.

| Phase | What | Core? | Effort | When |
| --- | --- | --- | --- | --- |
| **0. Bugs** | Mark's QTE key and icon (data); no silencing when the QTE couldn't start; null guard on `SilencedTargets`; Mark footprint distance; Lucy across all hostile factions (enemy the action targeted first, then nearest) | Tier 1 to 2 (flagged core bugfixes in the handlers and `PlayerController`) | S | Now |
| **1. UI-only** | Role zones for the selected unit (diamond, cross arrows, ring); destination cover icons in the move preview; Alt "Family watch"; role badge and pip (ready / no FTP / stunned); prompt, execute and miss barks via `FactionRoleVisual.ShowWithDialogue` and an over-head bark; QA log of skips where readable | **No** | M | Now: safe, reversible, answers most of B4 and Q7 |
| **2. Reason codes** | `RoleSkipReason` from `CheckFeasibility` and the controller; additive `onFamilyRoleSkipped` bus event; a non-core presenter applies the catalogue's tell/silent filter and rate limits, and shows glyph + bark | **Yes, Tier 3** (Family Roles, controller, bus) | M | **In the same tech pass as Pilot 1's limits on `main`** (D-042, D-061), since both edit `FactionRoleHandlerBase` and the wait list |
| **3. Limits wording** | `NoUses` reads "No Watch left"; pips show uses per round; Fireside extra pip (D-040) | Rides on Pilot 1 | S | With Pilot 1 |

**Playtest signal.**
- *It worked:* testers can say, unprompted, why Linda didn't shoot ("it was diagonal"). Nobody asks "did John defend?". A miss is described as "I missed", not "it bugged".
- *It failed:* testers mention clutter or "too much text" on enemy turns. If so, pull the `Busy` and `NoLine` barks first, then shrink zones to hold-Alt only.
- **Measure:** QA log counts of each reason per fight. If `Busy` exceeds about 1 per fight, Q2 (queueing) matters more than its text.

## USP check

- **Family Roles: strengthens.** A reactive passive is only a USP if the player sees it working and plans around it. The zones turn roles from luck into positioning; the barks make each answer a family beat.
- **Synergies: neutral, with a shared tool.** The bark and insert presenter is the same one Q18 needs (see Overlaps); no synergy rule changes.
- **Duos: neutral, slightly cleaner.** After D-036 the FTP bar means Duos only; showing role readiness as Watch pips, not FTP, keeps the two resources apart in the player's head.
- **Managing the Home as a Family: slightly strengthens.** Fireside's +1 role use (D-040) becomes a visible extra pip in the first round, a Home effect seen in combat (S4).

## Overlaps (build once)

- **Q18 synergy insert-shot.** Q18 asks for a generic insert using the Family Role panel. The pieces exist: `FactionRoleVisual.ShowWithDialogue` (insert + one line; used by Revenge) and `GlobalEventBus.onSynergyTriggered` (raised by Sisters' Rivalry, Catch & Return, Tempest Bloom, Command Shield Dash and more). **Build one "family moment" presenter** (non-core, listens to the bus) with a single queue and priorities: role execute > synergy insert > reason bark. This plan's barks and Q18's inserts are two clients of it. Whoever builds first builds the presenter; the other plugs in.
- **S9 / Q20 move preview.** The destination cover icons sit in the move preview that S9 may turn into a two-click preview and Q20 may tint per character. Keep the cover icons as a separate overlay layer on the tile so they survive either change; reuse Q20's character colours for the Alt view.
- **Q6 mini HP bars.** The role pip lives beside the always-visible mini HP bar; design them together so there's one over-head widget, not two.
- **Q19 undo.** Reason popups don't block undo; only a QTE that actually ran does (as Q19 says).
- **S5 Sisters' Rivalry.** No overlap beyond the shared presenter.

## Acceptance checklist (for QA)

For each of John, Linda, Lucy, Mark: one scripted situation where the role fires and one where it can't, and what the player sees.

- [ ] **John fires:** enemy attacks Lucy standing diagonal to John (inside the diamond). Before the enemy turn, Lucy's tile showed John's shield icon. Prompt bark "No!", tether line, press, insert "I got you!".
- [ ] **John can't:** same, Lucy at (2,1) from John. No popup (silent `NothingInRange`); the move preview had shown no shield icon there.
- [ ] **John missed:** press too late. `Missed` glyph + bark at John, consequence line; Lucy takes the hit.
- [ ] **Linda fires:** enemy walks into her row within 4. Real-time prompt, insert, shot.
- [ ] **Linda can't (diagonal):** enemy ends a walk on her exact diagonal at distance 2. `NoLine` bark once this enemy turn (Phase 2); the cross was visible when Linda was selected (Phase 1).
- [ ] **Linda can't (resource):** FTP 0 (today) / 0 uses (later). Panel pip empty before the enemy turn; `NoUses` bark once on the first valid trigger.
- [ ] **Lucy fires:** Mark hits an enemy within 3 of Lucy. Prompt, embers.
- [ ] **Lucy dropped:** a family push moves an enemy into Linda's lane, so Linda and Lucy both qualify. Linda fires; Lucy barks "Linda's got it!" (`Busy`), unless Q2 chose queueing, in which case both fire in turn.
- [ ] **Mark fires:** enemy within 2 hits John. Mark's prompt shows **Mark's** key and icon (Phase 0).
- [ ] **Mark big enemy:** a 2×2 enemy whose footprint (not anchor) is within 2 hits an ally. Mark fires (Phase 0).
- [ ] **Mark hit too:** AoE hits Mark and Lucy. Behaviour per THJ's Q3.
- [ ] **Busy QTE:** a role triggers while a synergy QTE is up. The role is skipped *without* silencing the target; the same enemy can trigger it again later this turn (Phase 0).
- [ ] **No spam:** a 6-enemy turn with every enemy moving outside all zones shows **zero** popups; at most 2 reason popups are on screen at once.
- [ ] **QA log:** every skip, silent ones included, appears in the combat log window with its reason code (Phase 2).

## Risks

- **Miss detection without core (Phase 1) is an assumption.** `qteEnded` carries no result, and `onFamilyRoleActivated` fires on success only. A non-core listener can infer a miss as "a role QTE started and ended with no activation". Not verified; the TD checks it. If unreliable, the miss bark moves to Phase 2 (the controller raises `Missed` directly).
- **Phase 2 collides with Pilot 1.** Both edit `FactionRoleHandlerBase` and the wait list. Mitigation: one tech plan for both (D-061 already asks Pilot 1's plan to use the fact sheet).
- **AI regression baseline.** Phases 0 and 2 don't change AI choices; Q2 to Q4 rule changes might shift enemy outcomes. `AIRegressionTest.Baseline_MatchesCurrentAI` is already known red, so it can't catch this. QA compares fight logs instead.
- **Overlay clutter on dense boards.** Zones are faint and shown only for the selected unit; the Alt view is opt-in.

## Questions for THJ

**Q1. Approve the reason-code event on the role pipeline (Phase 2)?**
- *Context:* the in-the-moment "why not" needs the handlers and controller to report a reason. Today they return plain bools. It's an additive public event on `GlobalEventBus` plus a reason value from `FactionRoleHandlerBase` and the four handlers: core, Tier 3.
- *Options:* (a) yes, in the Pilot 1 tech pass; (b) yes, now, separately; (c) no, Phase 1 only.
- *Recommendation:* (a), so the role pipeline is touched once.
- *Blocked:* Phase 2 and the `NoUses` / `Busy` / `NoLine` popups. Phase 0 and 1 are not blocked.

**Q2. One role per event: queue the others, or keep one and tell the player?**
- *Context:* when two roles qualify for the same event (mostly Linda + Lucy on a family push or Command move, Linda + Mark on an enemy charge that hits an ally), the first feasible fires and the rest are dropped silently.
- *Options:* (a) keep one, show `Busy` ("Linda's got it!"); (b) queue every eligible role, one QTE after another; (c) queue at most 2 per event.
- *Recommendation:* (c). Two family members answering one threat is exactly the USP moment, and the per-round limits keep it from running away. Cap at 2 to protect enemy-turn pace (Q4).
- *Blocked:* the `Busy` reason's lifetime; part of Phase 2's controller change.

**Q3. Should Mark strike back when the same hit also targets him?**
- *Context:* the base guard blocks every role whose unit the last action targeted. For Mark this means an AoE that hits Mark and Lucy never triggers him. The GDD reads "an enemy's action hits a family member", and Mark is family.
- *Options:* (a) yes, remove the guard for Mark; (b) keep it and leave it silent; (c) keep it and show a reason.
- *Recommendation:* (a). His 1-per-round limit (D-042) caps it.
- *Blocked:* the Mark rows of the acceptance list; the GDD Mark row.

**Q4. Do teleports and jumps into Linda's lane trigger her?**
- *Context:* only walk, push and Command moves raise the end-move event; a jump or teleport that lands in her lane never triggers her, which players read as a bug. Counting them is a core change (`AEffectTransporter`).
- *Options:* (a) count them; (b) don't count them, cover it with `NoLine`; (c) decide after the limits are built.
- *Recommendation:* (a), built with the limits (Linda capped at 2/round, so the balance concern is gone).
- *Blocked:* whether `NoLine` covers teleports; Linda's GDD row.

**Q5. Keep "a missed press silences that enemy for the turn"?**
- *Context:* after a miss, the role ignores that target for the rest of the enemy turn (today until the next selection change, which may not match "the turn"). It avoids re-prompting the same target, but nobody is told.
- *Options:* (a) keep, show it in the `Missed` line, scope it exactly to the current turn; (b) remove silencing (a miss costs nothing anyway, D-034); (c) keep as is.
- *Recommendation:* (a).
- *Blocked:* the `Missed` wording; a small Phase 0/2 fix.

**Q6. How visible should role zones be?**
- *Context:* hover-only today, which is why players never saw John's diamond include diagonals or Linda's cross exclude them.
- *Options:* (a) selected unit's zone always on + Alt for the whole family; (b) Alt only; (c) every zone always on.
- *Recommendation:* (a).
- *Blocked:* Phase 1 overlay scope.

**Q7. Reasons as family barks, or neutral icons only?**
- *Context:* barks carry warmth and fit the pillars; icons are quieter and language-free.
- *Options:* (a) glyph + bark (narrative writes about 3 lines per character per reason); (b) glyph only; (c) glyph always, bark only on the first occurrence per fight.
- *Recommendation:* (c). It keeps the warmth without repeating the same line all fight.
- *Blocked:* narrative brief for `miso-narrative`.

**Q8. Can a stunned or downed Bergson still answer with their role?**
- *Context:* no stun check was found on the role path, so today a stunned John may still redirect hits (unverified in play).
- *Options:* (a) no, show a stun star on the badge (`CantReact`); (b) yes, roles ignore stun; (c) only downed blocks.
- *Recommendation:* (a).
- *Blocked:* the `CantReact` reason; a handler guard (Tier 3).

## Scope

In: role readability (zones, badges, barks, reason codes), the bugs listed in Phase 0, questions on the rule gaps.
Out: graded QTE (D-034 experiment), Linda's real-time vs paused prompt, Bergson Time (D-038), the per-round limit mechanics themselves (Pilot 1), Toba's future role (D-048).

## Touches

Systems: `UnitPanelUI`, `FactionRoleVisual`, grid cell highlight, `DamageNumberManager.ShowText` or an over-head bark widget (Core/FX, not on the core list), bark lines (data), combat log (listener); Phase 0 and 2: `FactionRoleHandlerBase` (core), four role handlers (core), `FactionControllerBase` / `PlayerController` (core), `GlobalEventBus` (core, additive), Mark's prefab data.
USPs: Family Roles (main), Synergies (shared presenter with Q18), Home (Fireside pip).
Docs: see below.

## Gates

Compile / EditMode tests (reason codes: one test per code per handler in Phase 2) / review (core in Phases 0 and 2) / play check: **yes**, THJ's time for the acceptance list / docs below.

## Docs to update if approved

- [`design/gdd/family-systems.md`](../design/gdd/family-systems.md): new rules FR-8 (zones and badges), FR-9 (the reason catalogue and its tell/silent split), any answers to Q2 to Q5 and Q8 in the role table; FR-6 Watch wording.
- [`design/gdd/combat-rules.md`](../design/gdd/combat-rules.md) CR-28: link to the readability rules.
- Character sheets for John, Linda, Lucy, Mark: Family Role rows only if Q3, Q4 or Q8 change a rule.
- `glossary.md` (owned by `miso-narrative`): reason words, "Family watch" (proposed name), Watch.
- Q18's plan, when written, references the shared "family moment" presenter.
