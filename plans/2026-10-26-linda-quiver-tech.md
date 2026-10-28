# Linda's Quiver: tech plan (prototype)

Size: L    Tier: 3 (Family Roles, a new mechanic; design approved D-241 to D-245)    Assigned to: miso-implementer (chunks below), reviewer, verifier
Branch: all, built on `thj/linda-quiver` (from `main` @ `a1483f0b9`)
Status: approved (THJ, 2026-10-26: TQ1 (a), TQ2 (a), TQ3 play after C3 and C4; D-246 to D-248). C1–C3 committed after THJ's play check (2026-10-27); next: vanished-arrow bug, C4, C5

## Why

Linda deals 46–72% of the family's damage; Watch fires without limit. THJ approved a minimal quiver prototype instead of a per-round cap (design plan [`2026-10-26-linda-quiver-design.md`](2026-10-26-linda-quiver-design.md), "Recommendation" item 1; D-241 to D-245).

## Goal

Linda's shots spend arrows from a quiver of 4. Arrows land on the board, any Bergson walking over them hands them back, Recall pulls them all home, and the player can always see the count and where arrows are. All of this is built with no change to a core system's code.

## Rules being built (from the design plan; IDs are the design's)

- LI-3: Quiver size 4, full at level start.
- LI-4: These spend 1 arrow: bow attack, Watch, Explosive Crescendo, the Linda part of Marks-Sisters and Healing Marks. These spend nothing: Tempest Bloom copies, Catch & Return bounces, Harmonic Slam, Cleanse, movement.
- LI-5: At 0 arrows, the arrow abilities are greyed out and Watch doesn't trigger (no prompt, zone hidden, badge "empty quiver").
- LI-6: An arrow lands on the tile of the last enemy it hit. With no hit, it lands at the end of its range; Explosive Crescendo lands on its centre cell, a Duo arrow at the end of its line. It is never lost: if the landing cell is missing (hole, off grid) or blocked (`DisallowWalk`), it goes to the last valid cell of its path. A tile holds a stack.
- LI-7: Any Bergson whose move enters a tile with arrows picks them all up, up to the quiver size; extras stay. Forced and Duo moves count. Arrows under a living enemy are locked. Enemies ignore arrows. A pickup plays the hand-back beat: a toss, a bark, and Linda's reply.
- LI-8: Recall is its own ability: 1 AP, cooldown 2, usable when at least 1 arrow is grounded. Every grounded arrow flies straight back, including locked ones, and refills the quiver. No damage.
- LI-9: An arrow Mark catches and returns ends in Linda's quiver.
- LI-10: Arrows come back at level end. This is free, because unit prefabs are instantiated fresh per level.
- LI-11: No Watch cap.
- Out of scope: pierce, skill nodes, the workshop quiver, the Fireside arrow (LI-12).

## Gap-fills (Tier 2, flagged to THJ)

- **G1. Tempest Bloom:** the original arrow is disposed at the Cyclone without landing, and the copies never land. The arrow lands on the cell where the original was split, so Linda's total is conserved.
- **G2. Catch & Return:** in BounceBack mode the original keeps flying and a clone flies back. On the catch, +1 goes back to the quiver at once; neither the original nor the clone lands an arrow. The extra damage of the bounce is unchanged.
- **G3.** An arrow that lands on a Bergson's own tile goes straight back to the quiver, with the hand-back beat.
- **G4.** Grounded arrows can share a tile with a hazard, trap or corruption pool, because they don't use `GridCell`'s planted slot.
- **G5.** Recall is appended as Linda's 10th ability, so it gets no number-key shortcut (the shortcuts stop at 9). It is clickable only.
- **G6.** Pickup happens when a Bergson plugs into a cell. Passing through an ally's cell doesn't plug, but such a cell can't hold free arrows (G3 picks them up), so nothing is missed.

## Approach: no core code

| Need | How, without touching a core system | Where |
| --- | --- | --- |
| Quiver state | `LindaQuiver` component on `Unit_Linda.prefab`: `Count`, `Size`, `Spend()`, `Add(n)`, `OnChanged`. Responds to `GameEntityMessage` checks `HasArrow` and `HasGroundedArrows` | `Features/Player/Linda/Scripts/Quiver/` |
| Grounded arrows | `GroundedArrowField`: a per-level, non-core registry (cell → stack) with its own views (icon above sprites, stack number, locked state when a living enemy stands there). Cleared on `levelEnded`. **Not** `GridCell`'s planted slot: that slot holds one entity, silently relocates a second, and is read by the AI worker thread | same folder |
| Landing rule | `ArrowLandingRules`: a pure static that is EditMode-tested. Input: path cells, last enemy-hit cell, end-of-range cell, plus a valid-cell predicate. Output: the landing cell | same folder |
| Spend + land per projectile | `QuiverArrow` sibling component on `LindaAttackArrow`, `LindaExplosiveArrow`, `LindaAttackFireArrow` and `LindaAttackHealArrow` (the heal arrow only when Linda owns it). It spends in `Start()` unless it is flagged as a copy (cloners set the flag in the same frame, before `Start` runs). It tracks the last enemy hit through its own `OnTriggerEnter2D`, and lands through `ArrowLandingRules` in `OnDisable`/`OnDestroy` unless suppressed | prefabs + script |
| Copies | `LucyCycloneProjectileScatter` and `ProjectileCatchAndReturn` (both non-core) flag their clones as copies and apply G1 and G2 | those scripts |
| Gating (LI-5) | Data: set `activationFeasibilityCheckFunction = "HasArrow"` on the spawn effects of the bow, Crescendo, Watch (`Linda_Ability_FactionRole_Effect_Spawn`) and Linda's partner abilities in the two arrow Duos (`PlayerController.prefab`). Watch's `CheckTriggerConditions` already calls `CheckActivationFeasibility`, so at 0 it never prompts, and a Duo greys out through `CooperationEntry.Available` | assets |
| Pickup | Subscribe to the existing `GlobalEventBus.gridCellPlugStateChanged` (cell, type, plugged): when a player-faction `GUnit` plugs into a cell with an unlocked stack, take it. This covers walk, push, Command, dash and Duo moves, which all plug cell by cell | field script |
| Recall | New `AbilityPreset` `Linda_Ability_Recall` (AP 1, `coolDownV` 2, self), effect `AEffectFunctionCaller` → `LindaQuiver.Recall()`, feasibility `HasGroundedArrows`. Return flight = sprites tweened in straight lines, non-blocking for the ability's duration | new asset under `Resources/UnitSpecific/Player/Linda/Abilities/Recall/` |
| Readability | Non-core presenters only: arrow pips under Linda (with `UnitMiniHealthBar` or a sibling) and on `UnitPanelUI`; `RoleBadgeState` empty-quiver state; `RoleZonePresenter` hides Linda's zone at 0; `FactionRoleVisual` prompt reads "Arrows 3 → 2"; ability tooltip says "No arrows" when greyed for that reason; landing-tile marker while aiming (uses the public `Projectile.CollectPreviewPathHits` + `ArrowLandingRules`); "+N arrows" on the move preview (poll the preview path like `MovePreviewCoverPresenter`); Recall return lines while hovering or aiming Recall | UI scripts |
| Metrics | A new `CombatLog` partial (non-core listener) logs spend, land (cell, stack), pickup (who), recall (n), and Watch declined with the arrow count | `Core/Systems/CombatLogging/Runtime/CombatLog.Quiver.cs` |

**If a chunk finds it needs a core-system code change, the implementer stops and reports; the coordinator takes it to THJ (Tier 3).** That includes `Projectile`, `GridCell`, `PlayerController`, `FactionRoleHandlerBase`, `LindaFactionRoleHandler`, `CombatLevelUIManager`, `UnitsCooperationHandler`, `AEffect*`, `GlobalEventBus` and `PlayModeStaticReset` (adding a reset hook there is fine and expected if a static is added).

## Chunks (riskiest first; one implementer run and one commit unit each)

### C1. Quiver, spending, landing, gating: `opus`

- `LindaQuiver`, `GroundedArrowField` (with a placeholder icon and stack number, so it can be checked in play), `ArrowLandingRules`, `QuiverArrow`; G1 and G2 in the two cloner scripts; the gating data on 5 effects; Linda's prefab gets `LindaQuiver`.
- Acceptance:
  - [ ] A bow shot from 4 arrows leaves 3, and an arrow icon appears on the last enemy hit (pierce through 2: on the second), or at the end of range if it misses.
  - [ ] An arrow aimed past a hole or into a wall lands on the last valid cell of its path (EditMode-tested in `ArrowLandingRules`).
  - [ ] Crescendo lands on its centre cell; a Marks-Sisters or Healing Marks arrow lands at the end of its line; each costs 1.
  - [ ] Watch spends 1 per trigger. At 0, no Watch prompt appears, and the bow, Crescendo and both arrow Duos are greyed out.
  - [ ] Tempest Bloom: 1 arrow spent, 1 arrow grounded (G1). Catch & Return: 0 net arrows spent, nothing grounded (G2).
  - [ ] Two arrows on one tile show stack "2"; an arrow under a living enemy shows the locked state.
  - [ ] EditMode tests: landing rules, quiver arithmetic (never above size, never below 0), field stack add/take/lock.

### C2. Pickup and the hand-back beat: `sonnet`

- Pickup through `gridCellPlugStateChanged`; locked stacks unlock when the enemy leaves or dies; G3; field cleared on `levelEnded`. Hand-back beat: a toss tween from the picker to Linda, plus 2 barks through `BarkManager` (picker line + Linda reply, placeholder lines from `miso-narrative`, tagged `[PLACEHOLDER]`), once per pickup, non-blocking (TQ2). Its timing values are serialized fields.
- Acceptance:
  - [ ] John walking over a 2-stack with Linda at 1/4 brings her to 3/4, the icon goes away, and the toss and two barks play.
  - [ ] Extras beyond size stay on the tile with the right stack.
  - [ ] Pushed, Commanded, Fist Blitz and John–Linda Dance moves that end on or pass through an arrow tile pick it up.
  - [ ] A locked stack can't be picked up until its enemy moves or dies.
  - [ ] An enemy walking over arrows takes nothing.
  - [ ] Next level: full quiver, no arrows on the board.

### C3. Recall: `sonnet`

- Preset, effect, feasibility, the prefab entry (G5), the straight-line return flight, refill.
- Acceptance:
  - [ ] Recall is greyed out with nothing grounded, and usable with 1 or more grounded.
  - [ ] It costs 1 AP. It is unusable on her next turn and usable on the one after (cooldown 2).
  - [ ] Every grounded arrow, locked or behind walls, flies back; quiver = min(size, count + grounded); the board is empty of her arrows. No damage is dealt.

### C4. Readability: `sonnet`

- Arrow pips under Linda and on her unit panel; the badge's empty-quiver state; zone hidden at 0; Watch prompt "Arrows N → N−1"; "No arrows" tooltip reason on greyed arrow abilities and Duos; landing-tile marker while aiming the bow, Crescendo and Duos; "+N arrows" on the move preview per path (Tab cycling); Recall return lines while aiming.
- Acceptance: each item seen in play; pure rules (pip state, badge state, preview count) EditMode-tested.

### Added after THJ's play check (2026-10-27)

- **C4 additions (D-258, D-259):** a "+1" return cue on Linda for every return (Mark's catch, any pickup including her own and the instant pickup on landing, Recall); a brighter locked look (today a dark red tint at 0.55/0.3/0.3) with an outline or badge, and a badge even on a single arrow; an arrow landing with the field missing or closed goes back to the quiver.
- **C3b, Mark's catch with a QTE (D-257, THJ's design):** when Linda's arrow reaches Mark, a QTE offers the catch. If pressed, the arrow stops at Mark, flies back to Linda damaging on the way, and returns to her quiver. If not pressed, it passes on as a normal shot. The blocker is the old sync problem: the arrow keeps flying while the QTE and Mark's animation run. A read-only spike looks for a way to hold the arrow at Mark during the window without core code. Spike done (`reports/mark-catch-qte-spike.md`); THJ approved it as found (D-260), with the return ending at Linda (D-261). C3b runs after C4; model `sonnet`. Acceptance: the arrow freezes at Mark during the QTE; pressed → +1 cue, the catch animation, the return flight ends at Linda and damages on the way, Linda's action waits for it; declined → the same arrow carries on and lands normally; nothing past Mark is hit after a press; the fallback timer releases a stuck catch; the QTE failing to start or Mark being disabled re-releases the arrow. Recall shows as "Encore" (D-262).

### C5. Combat log lines: `sonnet`

- `CombatLog.Quiver.cs` lines for spend, land, pickup, recall, and a declined Watch with its count, enough to compute the playtest signals (design plan, "Playtest signals").
- Acceptance:
  - [ ] One level played gives one log line per event.
  - [ ] `CombatLogTests` gets a quiver case.

C1 is used by everything else. C2 and C3 depend on C1. C4 and C5 can follow in either order. If THJ wants the earliest possible play check, C1 + C2 + C3 is the playable core, and C4 is what the cold-player signal needs.

## Risks

- **Statics / domain reload:** prefer instance state on `LindaQuiver` and a field component per level. Any static (for example a field singleton) needs `ResetPlayModeState()` hooked from `PlayModeStaticReset.Reset()`.
- **AI thread:** nothing the AI reads changes (no planted entity, no walkability change). `AIRegressionTest` lists Linda's Duo abilities: appending Recall to `Unit_Linda`'s list could move it. The verifier compares the known red's failure message before and after C3; any new failure fails the gate. No re-baseline.
- **Projectile lifecycle:** `OnDisable` also runs on scene unload and at level end; landing must be skipped when the level is ending (`QuiverArrow` checks a "level ending" flag set on `levelEnded`). Pooled vs destroyed projectiles: the implementer confirms which and lands exactly once.
- **Spend timing:** clones are instantiated inside `GetClone`, which calls `Initialize` before the cloner can flag them, so spending must wait for `Start()`. The implementer confirms that order holds for both cloners.
- **Prefab/asset edits:** small YAML edits or an editor script. `Unit_Linda.prefab`, `PlayerController.prefab` and four arrow prefabs; `.meta` with every new asset.
- **Watch FTP:** depends on TQ1.
- **Hand-back pacing:** non-blocking by default (TQ2). Tunable fields; THJ judges in play.
- **Other branches:** `thj/home-test` and `thj/onboarding` will need this when it lands on `main` (THJ moves it).

## Test plan

- EditMode: `ArrowLandingRules`, quiver arithmetic, field stacks/locks, pip/badge/preview rules, combat-log case. Location: `Features/Player/Linda/Scripts/Quiver/Editor/` (namespace `MISO.Features.Player.Linda.EditorTests` or the house equivalent).
- Full EditMode suite after every chunk: only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` may fail.
- Play check by THJ after C3 (play-test before commit, per THJ's rule for feel/gameplay chunks) and after C4. The M2 win path isn't touched, so no win playthrough is needed.

## Docs to update

- `design/gdd/characters/linda.md`, `family-systems.md`, `combat-rules.md` (rules as *Planned* when C1 starts; settle after the playtest), owned by `miso-game-designer`.
- `glossary.md` (Quiver, Recall) and the bark/UI text, owned by `miso-narrative`.
- `plans/family-role-chunk.md` items 1 and 10 (Linda's part superseded, D-244), `tech/combat-architecture.md` (quiver + field), `status.md`, `decisions.md`, `build-log.md`, owned by the coordinator.

## Questions for THJ

Answered by THJ, 2026-10-26: TQ1 keep 1 FTP (D-246); TQ2 non-blocking (D-247); TQ3 play check after C3 and after C4 (D-248).

- **TQ1. Watch's FTP cost in the prototype?** Today Watch costs 1 FTP. D-225 keeps role FTP costs while your FTP rework is elsewhere, but the design's case for the quiver assumes the arrow is her cost. (a) Keep 1 FTP plus 1 arrow: only one variable changes against the current build. (b) Set Linda's `requiredFTP` to 0 (one prefab value): the "declines to save an arrow" signal is clean.
- **TQ2. Hand-back beat pacing?** (a) Non-blocking: toss and barks play while play continues, about 0.6 s. (b) A short blocking moment (input locked about 0.8 s) so it's seen.
- **TQ3. Chunk order and play checks:** a play check after C3 (the playable core), then C4 and C5? Or build C1–C5 first and play once?

## Commit log

THJ play-checked C1–C3 on 2026-10-27 ("working, seems fun, needs work"; possible vanished arrow under investigation). Committed on `thj/linda-quiver`:

- `c6aade3c9` quiver scripts and logic tests (unit a)
- `502902b38` PlayModeStaticReset line (unit b, core)
- `f6dd15a0f` Cyclone scatter + Mark's catch (unit c)
- `dd95002f8` prefabs, ability data, Recall, wiring test (unit d)

THJ play-checked C4 on 2026-10-27 (works; most elements too big, sizing left until the final decision). EditMode 893/894 (known red only, THJ's Test Runner). Committed:

- `c7081b76c` PlayerController preview-path hook (core, D-270)
- `741ac9dd2` role-zone visibility interface (shared presenters)
- `6e3d92517` quiver readability scripts + arrow-with-nowhere-to-land fix
- `886f32e88` Linda's panel, badge, prompt and reasons
- `7ad75622c` Encore title + wiring test

C3b (Mark's catch QTE) and its play fixes, committed 2026-10-27 after THJ's play checks:

- `d5919c384` catch freeze-and-press script, rules, tests, field `IsOpen`
- `53272e30d` return arrow prefab
- `98f1adf80` per-prompt QTE wait and show speed (core QTE, D-273)
- `81bd8d584` catch sweep, return clamp, freeze at catch point (D-276)
- `680bd4726` Mark prefab (QTE on, return arrow, fast prompt) + wiring tests
- `91f40e903` Lucy follows up on real damage only (core, D-275, D-277)

Play-fix round 2026-10-27/28 (THJ played each):

- `9ba8c9478` caught arrow stops on its own path, return starts there (D-278 catch part; level flight dropped, D-279)
- `6d2388bbf` pips draw under other units' HP bars (D-280)
- `921294cbf` quiver presenters wait for the level's factions (level-start NRE, D-281)
- `4a880f27c` arrow board parented under the level; quiver survives restarts and map entry (D-282)
