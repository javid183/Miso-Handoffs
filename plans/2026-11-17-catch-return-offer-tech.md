# Catch & Return: offer the catch only when it hits something, and say so (tech plan)

Size: M    Tier: 3 (a game-rule change, answered by THJ 2026-11-17); code is feature-folder only    Assigned to: miso-implementer (sonnet), then miso-reviewer, miso-verifier
Branch: `main` (scope: all)
Status: approved by THJ 2026-11-17; C1 `521742a74`, C2 `5426a16d7` + `2cf617358`, C3 docs done. **2026-11-18 (D-564): the grey lost-hit tint was dropped after THJ saw it; forward hits past Mark show the normal red preview, and the core grey overload was removed (`baa77da19`, `9e8d82434`). The grey wording below is history.**

## Why

THJ (2026-11-17): Mark's catch prompt appears even when no enemy stands between Linda and Mark while enemies stand past Mark. The player presses it, the arrow stops at Mark and comes back to the quiver, and the forward damage on the enemies behind Mark is lost. The prompt should show or hide itself sensibly, with better feedback. Explore report (2026-11-17): `ProjectileCatchAndReturn.TryCatch` opens the prompt whenever the arrow reaches Mark and the static gates pass (allied shooter, Mark-Linda synergy unlocked, 2+ cells away, Mark on the incoming path). It never looks at enemies, and the aim preview doesn't either (it draws the ">>>" on Mark's tile even when the catch would do nothing).

## Goal

The catch prompt, the ">>>" on Mark and the pink return bars appear only when the return flight would hit an enemy; when the catch is offered and enemies stand past Mark, the preview shows the forward hits the catch gives up.

## Acceptance criteria

- [ ] **Offer rule (D-560):** the prompt opens only if the return copy (Mark's hand to Linda) would hit at least one enemy. No enemy between: no prompt, the arrow flies on exactly as if Mark weren't there, including with enemies past Mark and including with no enemies at all.
- [ ] Both sides present (enemy between and past Mark): offered (the return hits), as today.
- [ ] Allies on the line, Mark adjacent or off the line, a Cyclone before Mark: unchanged from today.
- [ ] The decision is one pure static function (like `CatchAndReturnRules`), used by the real catch and by the aim preview, so they never disagree. A test feeds both the same situations and compares.
- [ ] **Preview (D-561):** when the rule says no, the ">>>" chevron on Mark's tile and the pink return HP bars are not drawn; the lane shows the normal shot. When the rule says yes, the chevron and pink bars show as today.
- [ ] **Lost hits (D-561):** when offered and the shot would also hit enemies past Mark, their forward HP previews are greyed or struck through (they are lost if the catch is taken); the pink return bars show what the catch gives instead.
- [ ] Enemies dying or moving mid-flight can't leave the arrow frozen: if the prediction was yes and nothing is hit when the arrow arrives, the existing miss path releases it.
- [ ] Tests cover: enemy before Mark only, past Mark only (no prompt), both, neither (no prompt), ally in the way, Mark adjacent, Mark off the line, a Cyclone before Mark. Real and preview agree in each.
- [ ] Compile clean; EditMode all green except `AIRegressionTest.Baseline_MatchesCurrentAI` (count before and after reported). No change to the prompt text.

## Scope

In: the offer rule, its use at runtime and in the preview, hiding the chevron and bars, greying the lost forward hits, tests, GDD wording.
Out: the prompt text and its visuals (`QuickTimeEventHandler`, `QTEBehavior`, `QTEProfile` are core; THJ did not ask for it); the quiver, AP refund, return damage values; what Catch & Return does when it fires; Focus Catch.

## Touches

Systems (feature-folder, plus one additive core overload approved by THJ 2026-11-17 for the grey lost-hit bars, D-563: `GUnit.ShowDamagePreview(..., lost)` and a grey tint in the HP bar UI; own commit): `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (`TryCatch`, `PassesCatchGates`, `CatchSweep.LateUpdate` caller), `CatchAndReturnRules.cs`, `Features/Player/Shared/Synergies/SynergyLanePresenter.Catch.cs` (`TryReadCatchShot`, `ComputeCatchDamage`, `ApplyCatchDamage`), `CatchReturnPreviewRules.cs`, `TempestBloomPreviewRules.CollectHits` (reused read-only), the existing editor tests in those folders. Core files listed in `tech/core-systems.md` (`Projectile.cs`, QTE files) are read but not edited; if the prediction can't be made without editing one, stop and report the minimal additive hook (that is a core change THJ approves first).
USPs: Synergies (Mark and Linda), Family Roles untouched.
Docs: see below.

## Approach

Rules for every chunk: read `conventions.md`, `tech/core-systems.md`, `design/gdd/characters/mark.md` (MA-3), `linda.md`, `design/gdd/family-systems.md` and `plans/onboarding/2026-11-10-synergy-aim-preview-tech.md` (C3 Catch & Return preview); stop Play mode before editing scripts; no private IDs in code, comments, tooltips, test names or commit messages; keep line endings and BOM; prefer new partial-class files; report in `reports/catch-offer-c<N>.md` from `templates/report.md`.

### C1. The rule and the runtime (sonnet)

- New pure static (worker-safe, plain data in, bool out), e.g. `CatchOfferRules.ShouldOffer(returnHitCount)`, plus the helper that counts enemy hits on the return flight (Mark's hand to Linda's position) with the same contact walk the preview uses: `CollectContacts(arrow, From, To)` and `TempestBloomPreviewRules.CollectHits` (the Explore report names the lines in `SynergyLanePresenter.Catch.cs` around 211-217). Allies and non-hostile units don't count.
- `TryCatch` asks the rule after `PassesCatchGates` and before `FreezeArrow`. When the answer is no: do not freeze, do not open the prompt, and mark the arrow as seen so `CatchSweep.LateUpdate` doesn't re-ask every frame.
- Tests as listed; the real-path test builds the same grid situations as the preview test.
Commit 1 (own commit: it changes live combat behavior).

### C2. Preview and feedback (sonnet)

- `TryReadCatchShot`/`ComputeCatchDamage` use the same rule: when no, return false for the catch (no chevron, no pink bars); the normal shot preview stays.
- When yes: mark the forward hits past Mark as lost: grey or strike the second-colour/stepped bar for those enemies (the bar had no grey: a serialized grey tint with a code default, no prefab edit, was added with THJ's OK, D-563). The pink return bars stay.
- The preview survives the player's hover refresh as it does today and clears on cancel, click and level end.
- Tests: preview decision equals the runtime decision; lost-hit set equals the forward hits past Mark.
Commit 2.

### C3. Docs (designer, coordinator)

Designer: `mark.md` MA-3 and `linda.md` LI-9 (the catch is offered only when the return copy would hit an enemy; with no enemy between, the arrow flies on), `family-systems.md` (line near 100), `combat-rules.md` CR-56; check the "neither the arrow nor its return copy lands" wording. Coordinator: `tech/combat-architecture.md`, `build-log.md`, `status.md`, `decisions.md`, and note the Claude Docs mirror resync (Combat rules, Family systems, Characters).

## Risks

- [x] **Prediction vs reality:** one rule, one hit walk, a test comparing real and preview. A frozen arrow is the worst case, so the miss path releases it.
- [x] **Every-frame re-asking:** the arrow is marked seen when declined.
- [x] **Statics:** none planned.
- [x] **Quiver:** when no catch happens nothing changes for the quiver; when it does, as today.
- [x] **Design creep:** "catch as a refund when nothing is hit" is gone by THJ's choice; if players miss it later it is a new design item, not a quiet re-add.
- [x] **Other branches:** `thj/cyclone` has a Cyclone-before-Mark case (`SplitsAt`); this change doesn't touch it. Merge conflicts are unlikely (different files).

## Gates

Compile / EditMode (known red excepted, count reported) / `miso-reviewer` (feature code, runtime combat path) / `miso-verifier` / THJ play check: yes, short: Linda shoots past Mark with (a) enemy only past Mark: no prompt, arrow hits them; (b) enemy between: prompt and chevron; (c) both: prompt, past-Mark bars greyed; (d) nothing hit: no prompt. List in `playtests/2026-11-17-catch-offer-play-check.md`. Win playthrough: no.

## Docs to update

See C3 above (Mark MA-3, Linda LI-9, family-systems, combat-rules CR-56; mirror resync owed).
