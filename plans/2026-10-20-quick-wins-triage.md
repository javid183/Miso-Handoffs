# Quick wins (playtest Batch 3): paper plan and triage

Size: M (triage), the items S–M each    Tier: mixed (per item)    Assigned to: coordinator
Branch: all (code lands on whatever branch THJ picks, see W4)
Status: waiting on THJ (W1 to W4)

## Why

THJ asked on 2026-10-20 for a paper plan and triage of Batch 3 in `playtests/2026-10-playtest-tasks.md`. Two Explore sweeps on 2026-10-20 traced every code item. Their findings are summarised per item below. Paths are under `miso/Assets/_Project/`.

## Tier note

Until 2026-10-29, THJ's areas are Tier 3 even when small (`escalation.md`). Several quick wins are **game feel**: timing, feedback, hit reactions, camera and animation pacing. Where the task list already says *what* to do (THJ reviewed it on 2026-10-17/18), the direction is approved. The **values** (durations, thresholds) and any core change are still asked.

## Triage table

| Item | What the code says | Smallest change | Core? | Size | Tier | Owner | Bundle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Q1** Directed dialogue pass | Content pass over sequences | Narrative proposes cuts per mission, THJ approves | – | M | 3 (story beats) | narrative | N |
| **Q2** Story logic fixes | 7 named line fixes | Narrative proposes wording | – | M | 3 (lore/names) | narrative | N |
| **Q3** Faster transitions | No fade. `minimumLoadingTime` 1.5 s (`Scenes/PreloadScreen.unity:1170`; release builds only). `CombatLevelRunHandler.EndLevel` has about 2 s of hard-coded waits (0.5 + 0.5 + 1) | Lower the loading pad. Expose and shorten the EndLevel waits | EndLevel: yes (Level run) | S | 3 (feel values, core) | implementer | P |
| **Q4** Faster enemy turns | AI `holdTimeAfterActionCompletion` 0.5 s real time (`AIController.prefab:47`), `timeBetweenFactionTurns` 0.5 (scene), camera focus 0.5 s unscaled. No in-game fast-forward | Tune the values now. A speed toggle later needs real-time waits scaled (M) | Prefab/scene values; a toggle touches core | S (tune) / M (toggle) | 3 (feel) | implementer | P |
| **Q5** Juice top-up | Hit-stop exists (`GUnit.PlayHitSlowMo`, 0.2 s curve) but is wired only on UnitBase, Claws and Archer. Camera shake exists (`ShakeCameraEffect`) but is used only by Super Time and relics. No kill flash, freeze or shake | Wire the hit-stop on all units. Add a kill hook (freeze, shake, flash). Swap SFX | GUnit death hook: yes | S–M | 3 (feel) | designer → implementer | F |
| **Q6** Mini HP bars, lethal preview, low-HP warning | No world-space mini bar; `EntityInfoPanelUI` shows on hover, Shift or preview only. `AbilityDamagePreview.PredictsLethalOn` exists, with no lethal visual | Persistent "Mini" mode on the info panel. Skull or tint when the preview is lethal | Light | M | 3 (new readability feature, feel) | designer → implementer | F |
| **Q7** Family Role "why not" | Already in the Family Role chunk (`plans/family-role-chunk.md`) | – | – | – | – | – | elsewhere |
| **Q9** Selection feedback | Right-click already cancels, but steps back one state only, so it takes two clicks with Move auto-armed (`PlayerController.cs:117`, `FactionControllerBase.cs:987`). Ally-near-enemy mis-targeting: clicks resolve by `WorldToCell` only. The cause is unconfirmed (a tall sprite overlaps the tile, or an ally click switches unit) | Cancel loops `GoBackToPreviousState()` (pattern at `:564`). Mis-targeting: repro first | Yes (`PlayerController`), bugfix | S | 2 (bugfix in core) | implementer (+ QA repro) | A |
| **Q10** Lucy clarity | `TargetSelectCounterUI` already draws pips. No text, no orb count, no retarget hint | Add a "Target n/N" label. Show the orb count from `RequiredTargetCount`. Add a hint line | No | S | 2 (UI text in an established voice) | implementer (+ narrative for the hint) | A |
| **Q11** Map clarity + reveal | `WorldMapPanelUI.Start` turns on every unlocked mission at once. No pan, no per-mission beat. Numbers come from `WorldMap_Button.cs:114,128`. "Mithra's Gift" in the legend is the shared tag `P0.RewardRoom` (Daryani's room + relic rooms) | Legend: a new shop-room tag, retag `LevelRunUpgradeRoom`, add its legend icon (S). Reveal: a queued pan, highlight and beat per mission (M). Numbers: explain or remove | No | M (legend S) | 3 (reveal = first-time reveal; names) | implementer + narrative | R |
| **Q12** John shield idle | No shield-idle state in `AC_Playable_John.controller`. Three unused `Idle_Weapon_{Down,Side,Up}` clips might be the pose (check visually). Precedent: `GUnit.External_SetAnimatorBoolParameter` (Goblin Queen) | Add an IdleShield bool or state, toggled on the ShieldUp tag | No | S if the art exists | 3 (animation feel) | THJ (art check) → implementer | A* |
| **Q13** Goal tile + relic | Goal = a static `gridCellHighlightLevelGoal` sprite (`GridCell.SetLevelGoalHighlight`). The relic's "friendly fire" read is unconfirmed (the Heavenly Sword is enemy-only) | Goal: a pulse tween, arrow or beacon. Relic: repro in play first | Grid (visual only) | S | 3 (feel) / art | THJ art + implementer | A* |
| **Q14** Cleanup | `FadeOutGridSequence.asset` exists, unused. The Workshop lists all 12 `Resources/Unit Equipments` assets unless Hidden | Add the fade-out after the level-2 tutorial (which sequence: THJ). Set the extras to Hidden (which items: THJ) | No | S | 1 once THJ names them | implementer | A |
| **Q15** Mark hit sound | `Unit_Mark.prefab:2411-2412` plays `A_SFX_Lucy_Hit`. Also Lucy SFX on Mark's abilities (`:2504, :2528, :2532`). No Mark audio exists | Placeholder: John's hit clip until Mark audio exists. Clear the other Lucy leftovers | No | S | 2 (placeholder) | implementer | A |
| **Q17** Enemy idle desync | `EntityAnimationHandler.cs:200` uses `Random.value`, and only Archer, Dark Claw and Shaman enable it. It re-rolls after every action | Spread offsets (golden ratio), ±5–10 % speed jitter, flag on every enemy | No | S | 1 (THJ specified it) | implementer | A |
| **Q18** Synergy insert-shot | `FactionRoleVisual.ShowWithDialogue` exists, unused (avatar + bubble). `onSynergyTriggered` has only the combat log as listener. Sister's Rivalry raises it (`UnitKillAbilityPointProvider.cs:50`). Toba is missing from `FactionRoleVisual` | A `SynergyInsertShotPresenter` with an id whitelist calling `ShowWithDialogue` | Bus listener only | S | 3 (new reusable system; showcase moment) | implementer (+ narrative lines) | S9 |
| **Q19** Undo-move | Built but off: `enableActionReversion: 0` (`PlayerController.prefab:263`). The revert restores the cell and AP only. Pass-by FTP gain, phase overlaps and the ATB fill aren't rolled back | Snapshot FTP, AP and overlaps at move start and restore them. Block after a role QTE or enemy reaction | Yes (`PlayerController`, `RuntimeAbility`, Pass-by, FTP) | M | 3 (core behaviour) | tech plan → implementer | S9 |
| **Q20** Coloured move previews | Move tiles use a fixed sprite (`GridCell.SetHighlight` isMove). A per-unit colour exists (`FactionRoleHandlerBase.RoleZoneColor`; Toba has none) | Optional tint on the move or path highlight, muted or outline-only | Yes (Grid API addition) | S | 3 | tech plan → implementer | S9 |
| **Q21** Cyclone damage timing | Bundled with S10 (D-055) | – | – | – | – | – | elsewhere |
| **Q22** Objective readability | `ObjectivesPanelUI` exists but folds to zero height after 5 s (`Shrink`) | Keep a one-line collapsed summary (first active objective) instead of folding away | No | S | 2 (UI behaviour within the ask) | implementer | A |
| **Q23** Phase-switch visual | `PhaseVisualsUI` takes about 2.1 s, top-centre, and **blocks** the turn switch (`CombatLevelRunHandler.cs:490` `yield return ShowPhaseAnimation`) | Run it in parallel (`StartCoroutine`), shorten it, move it to the side | Yes (Level run turn flow) | S | 3 (feel + core) | implementer | P |
| **Q24** Low-HP feedback | No low-HP state anywhere. The red hit flash is `PlayerHit_CameraVolumeEffect`. HUD bar `UnitPanelUI._healthBarFill` | A `LowHealthPresenter`: held heartbeat volume, HUD glow, one SFX. Threshold to design | No | S–M | 3 ("should be designed") | designer → implementer | F |

## Bundles (paper plan)

- **A, plain fixes** (no design questions once THJ names the items; mostly non-core). Q9 (Cancel), Q10, Q14, Q15, Q17, Q22. One tech plan, one chunk per item, sonnet, one commit each. Q12 and Q13 (A*) join once THJ checks the art or the relic. Roughly 2 days in total.
- **P, pace** (one set of numbers for THJ, then one chunk). Q3, Q4 (tuning), Q23. Core: the EndLevel waits and the non-blocking phase banner. The fast-forward toggle stays a later M.
- **F, feedback** (one design pass so it reads as one language). Q5, Q6, Q24. The designer proposes hit, kill and low-HP feedback together, then a tech plan.
- **S9 chain** (the task list says try Q19 and Q20 before the S9 fallback). Q20, Q19, Q18. Each needs a tech plan. Q20 and Q18 are S; Q19 is M and core.
- **N, narrative.** Q1, Q2 to `miso-narrative` (proposals only). The Q11 legend tag rides with A; the Q11 reveal sequence is its own M.
- **Elsewhere:** Q7 (Family Role chunk), Q21 (S10).

## Recommended order

1. **A** (fast, visible, low risk) after the Masher C-chunks, since there is one writer at a time.
2. **P** (one decision from THJ, about half a day).
3. **N** runs in parallel any time: it's narrative proposals, with no Unity writes.
4. **F** design pass in parallel with A (designer, no Unity writes), then build.
5. **S9 chain:** Q20 → Q19 → Q18.
6. **Q11** reveal.

## Questions for THJ

**W1. Pace numbers (Q3, Q4, Q23).**
- *Recommended:*
  - loading pad 1.5 → 0.5 s;
  - EndLevel waits about 2 → about 1 s;
  - AI hold after each action 0.5 → 0.25 s;
  - gap between faction turns 0.5 → 0.25 s;
  - phase banner non-blocking, about 1 s total, at the screen's side.
- *Other options:* tune only (keep the banner blocking), or build a fast-forward toggle instead (M, core).

**W2. Bundle A details.**
- (a) Q14: which Workshop items are "extra", and which tutorial is "level 2" for the grid fade-out?
- (b) Q15: John's hit clip as a placeholder for Mark until Mark audio exists? (Recommended.)
- (c) Q12: are the unused `Idle_Weapon_*` clips the shield pose?
- (d) Q13: can you repro the relic "friendly fire" look, and do you want a pulse or a beacon on the goal tile?

**W3. Order.** Recommended: A → P → S9 chain → Q11, with N and the F design pass in parallel.

**W4. Branch.** The quick wins are scoped `all` (main). `masher-tweak` is the current branch, and the Masher implementer is writing there. Options:
- (a) **Recommended:** after the Masher chunks are committed, you create a `quick-wins` branch from `main`.
- (b) Build them on `masher-tweak` too: one merge, but mixed history.

## Gates

Per bundle:
- compile;
- EditMode suite (known red only);
- reviewer for core items (Q9 Cancel, P, Q19, Q20);
- a play check for every feel item (THJ's time).

Docs:
- `tech/combat-architecture.md` (P timings);
- GDD combat-rules where a rule or value changes (designer);
- `build-log.md`.
