# Crippled forced-move damage: fix, extend to every forced move, feedback (tech plan)

Size: L    Tier: 3 (THJ chose "every forced move pays", which needs additive hooks in the core `AEffect` family and the damage preview; each core chunk is shown to him before it is built)    Assigned to: miso-implementer (sonnet for C1 and C3, opus for C2 and C4), then miso-reviewer, miso-verifier
Branch: `main` (scope: all)
Status: waiting on THJ (plan approval, and the open questions at the end)

## Why

THJ (2026-11-17): enemies with Crippled (Linda's Harmonic Slam) should take damage when moved unwillingly; "it seems something has stopped it from working", and it needs better feedback. He only noticed the Taunt's damage missing. Explore report (2026-11-17): the rule is data wiring over one generic hook (`AEffectPusher.onMoveEffects`, `applyEffectsPerTile`); only John's Dash push, John's Taunt pull and Dom's Taunt pull are wired; Mark's Vault, Mark's Command, Dom's Swap and the others never were (the GDD line overclaims). No test covers any of it.

Likely cause of the regression (to confirm by test in C1): the 2026-10-05 tag-lifetime rework (`6d42d337e`, `ff1066ca3`) changed `GTagSet.PhaseTick` to `--LifeTurns > 0` and gave `Linda_Ability_HarmonicSlam_Effect_TagMod.asset` `lifeTurns 1`, `tickMoment 1` (PhaseEnd). Slam in the player phase puts Crippled on the enemy; the enemy's own end of phase ticks it away; so on your next player turn the tag is gone and nothing is paid. Before that rework the tag ticked at PhaseStart and survived into the next player turn. Only a push in the same turn as the Slam still pays.

## Goal

Crippled enemies take 4 x the mover's damage for every cell any friendly ability pushes, pulls, swaps or drags them, through your next turn, and the player sees it coming and sees it happen.

## Acceptance criteria

- [ ] **Lifetime.** Slam in player phase T: the enemy can't walk in its phase T (GDD: "can't walk for 1 turn"), Crippled is still on it during player phase T+1, and it is gone before it walks in its phase T+1. A second Slam refreshes, never stacks. A test proves each step on `GTagSet`/the entity tick. Other sources of Crippled (traps, Goblin Queen, Masher tag mods) keep their own lifetime unless THJ says otherwise (Q3).
- [ ] **Regression test** for the data wiring: John Dash push, John Taunt, Dom Taunt each reference the Crippled compound; the compound is gated on `Status.Crippled`. A mover test shows a Crippled target loses health per cell and a non-Crippled one does not.
- [ ] **Every forced move pays.** Each friendly ability that relocates another unit against its will pays 4 x the owner's `Stat_DMG` per cell moved to a Crippled target: John Dash push, John and Dom Taunt (already), Mark's Vault push, Mark's Command move, Dom's Swap, any player-side vortex/relic pusher, the Duo moves that displace an enemy. The implementer first lists every such ability in a table (`reports/crippled-c2.md`); THJ confirms the list before C3 wires data. Self-moves, willing moves and enemy-on-player pushes never pay (Q1).
- [ ] The damage is one compound asset reused everywhere (no per-ability copies of the numbers), uses the same formula as today (4 x `Stat_DMG`, capped at `StatUB_DMG`, crit and Blood Debt extras as John's compound has them), and is credited to the ability's owner (kill credit and the XP rule: Q2).
- [ ] **Feedback, when it fires:** a "Crippled" pop-up on the hit (distinct label or colour from a normal hit), a combat log line attributed to the mover ("Crippled · John: Claw -8 (2 cells)"), and a short jolt on the target's Crippled icon. Existing damage-number and HP-bar code is reused, not rewritten.
- [ ] **Feedback, before it fires:** the push/pull aim preview shows the Crippled damage on the target's HP bar (the stepped HP preview) with the lethal skull when it would kill, for the cells the push will actually cover. The preview matches the real number (a test compares them).
- [ ] No change to a non-Crippled unit's push, and no change to the AI's decisions: `AIRegressionTest` inner failure count stays as before (report before and after).
- [ ] Compile clean; EditMode all green except `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Scope

In: lifetime fix (data); regression tests; additive per-move hook on the movers that lack one; data wiring; the "Crippled" pop-up, log line, icon jolt; the push/pull HP preview; GDD fixes.
Out: enemies pushing players; Lucy's Cyclone on `thj/cyclone` (its Whirl pusher has `onMoveEffects: []`; wire it by data when that branch merges, and its docs say "pays once, as built", which is false today; the Cyclone session is told in `status.md`); other statuses; re-baselining the AI test; a general "forced move" event for other systems.

## Touches

Systems: `AEffectPusher` (core, AEffect family; already has the hook, only its feedback call changes), `AEffectCompound` (core), `AEffectSwapper` and `AEffectCommand` (core, additive serialized field, empty by default so behavior is unchanged until data wires it), `AbilityDamagePreview` / `AbilityPushPreview` (core; preview only), `GTagSet` (core, not edited: lifetime is data), the three existing compound assets, Mark's Vault, Command and Dom's Swap assets. Tag lifetime data on the Slam tag mod.
USPs: Synergies (Linda's Slam into John's Dash/Taunt, Mark's Vault), Family Roles.
Docs: see "Docs to update".

## Approach

Chunks, each one implementer run, each its own commit. Rules for every chunk: read `conventions.md` and `tech/core-systems.md`; stop Play mode before editing scripts; no private IDs (D-xxx, plan names) in code, comments, tooltips, test names or commit messages; keep line endings and BOM; prefer new partial-class files; new tests in a new file; report in `reports/crippled-c<N>.md` from `templates/report.md`; do not touch THJ's uncommitted files.

### C1. Lifetime fix and regression tests (sonnet; data only, no core code)

1. Write the tests first and run them: (a) a `GTagSet`/entity-tick test that reproduces today's lifetime (tag from the Slam tag mod is gone after the enemy faction's end of phase); (b) the data-wiring test above. Report what each shows. If the lifetime test does NOT reproduce, stop and report: the regression is elsewhere and the plan changes.
2. Change only the Slam tag mod's `lifeTurns` and `tickMoment` so the lifetime acceptance criterion holds. Expected from the code as read: `tickMoment` PhaseStart with `lifeTurns` 2 (tick at the enemy's phase start: 2 -> 1 keeps it for the enemy phase T, 1 -> 0 removes it at the start of the enemy's phase T+1). Verify with the test rather than trusting this. Check the status icon's turn counter still reads sensibly and that Linda's other uses of the tag mod (upgrades) are unchanged.
3. List every other asset that applies `Status.Crippled` (traps, Goblin Queen, Masher tag mods) with its lifetime in the report, and leave them alone.
Gate: THJ plays: Slam, end turn, next turn Taunt or Dash a Crippled enemy: it takes damage.

### C2. Mover table and the additive hook (opus; core, shown to THJ first)

1. Build the table of every ability or effect that relocates a unit (pusher, swapper, command, transporter with a target other than the owner, vortex, Duo moves): owner side, target side, whether it already has `onMoveEffects`. Write it to `reports/crippled-c2.md` and stop for THJ's confirmation of the "pays / doesn't pay" column before any code.
2. Then, for each core mover that lacks the hook (`AEffectSwapper`, `AEffectCommand`, others from the table): add an additive serialized `onMoveEffects`-style array, empty by default, applied per cell moved (path length, or straight-line cells for a swap: Q4), through one shared helper so the pusher and the others call the same code (and the feedback in C4 has one place to hang). No change to existing signatures. One commit per mover so each reverts alone.
3. Tests: each mover with an empty array behaves exactly as before; with the compound wired, a Crippled target pays per cell and a non-Crippled one doesn't; a dead target mid-move stops paying; Swap pays both ways only for the enemy side.

### C3. Data wiring (sonnet)

Wire the one Crippled compound into every ability the confirmed table marks "pays" (Vault, Command, Swap, relic/vortex, Duo displacements), with small YAML edits to the effect assets and a check in the Unity editor that each still loads. Add a data test per ability (compound present and referenced) so a future re-save can't silently drop it. One commit.

### C4. Feedback (opus; core preview files need THJ's OK first)

- Pop-up, log line and icon jolt hang off the shared helper from C2 (or the pusher's existing call site for the already-wired moves): a "Crippled" damage-number variant (label or colour; reuse `DamageNumber`), one log line attributed to the mover (see `tech/combat-log.md`; extend with one line type, update the doc), and a short icon jolt (reuse the existing status icon; no new asset).
- Preview: `AbilityPushPreview` already knows the push path; add Crippled damage for the covered cells to the target's stepped HP preview and the lethal skull, computed by the same function the real hit uses (test: preview number equals executed number). If this needs an edit to `AbilityDamagePreview.cs` or `AbilityPushPreview.cs`, the implementer stops and reports the minimal additive hook before editing: that is a core change THJ approves first.
- HP bars show the Crippled damage only for cells the move will really cover (a blocked push shows less).

## Risks

- [x] **Lifetime changes balance.** A longer Crippled changes how many pushes pay, not how long the enemy is stuck (still its next phase only, as the GDD says). C1 verifies with tests; THJ plays it.
- [x] **Core hooks.** All additive, empty by default, one commit each, shown to THJ first (C2, C4). Existing push behavior is unchanged without data.
- [x] **Kill credit and XP.** Balance doc says Crippled kills give no XP today; whether they should is Q2 (Tier 3).
- [x] **Combo runaway.** Crippled pays per cell per hit; John's Dash into a Slam combo can kill a Claw outright. THJ tunes the 4x after play; the multiplier is data.
- [x] **AI.** No AI content changes; enemies' own pushes don't pay. `AIRegressionTest` count is reported before and after.
- [x] **Statics, serialized renames, save data:** none planned.
- [x] **Assets.** YAML edits to effect assets; the Unity editor reload check is part of C3. THJ's editor is open, so the implementer works in it and doesn't batch-run Unity.
- [x] **Other branches.** `thj/cyclone` has its own Whirl pusher; wire by data after it merges. `thj/home-test` gets this through its next merge of `main`.

## Gates

Per chunk: compile clean; EditMode green except the known red (report the AI count before and after); `miso-reviewer` (C2 and C4 for sure; C1 and C3 too since the assets are shared); `miso-verifier` after C4. THJ play check: yes, once after C1 (the regression), once after C4 (feedback and the new movers); list in `playtests/2026-11-17-crippled-play-check.md`. Win playthrough: no.

## Docs to update

- Designer: GDD `combat-rules.md` (status table row "Crippled": lifetime and the exact list of moves that pay), `characters/john.md`, `toba.md`, `mark.md` (Vault, Command), `family-systems.md` if Swap changes; `design/combat-balance.md` Crippled lines.
- Coordinator: `tech/core-systems.md` (the new per-move hook on the movers), `tech/combat-log.md` (the new line), `tech/combat-architecture.md`, `build-log.md`, `status.md`, `decisions.md`.

## Open questions for THJ

- **Q1.** Which relocations count? Default: every friendly ability that moves an enemy against its will; not self-moves, not enemies pushing players, not Lucy's Cyclone until `thj/cyclone` merges.
- **Q2.** Should a kill by Crippled push give XP and gold to the mover's owner? Today it gives none (balance doc). Default: yes, credit the owner like any ability kill.
- **Q3.** Should traps and the Queen's and Masher's Crippled last as long as the Slam's? Default: leave them alone.
- **Q4.** For a Swap (teleport-like), count cells as the straight-line distance between the two units? Default: yes.
