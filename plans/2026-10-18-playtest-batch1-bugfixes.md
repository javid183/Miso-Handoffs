# Playtest Batch 1 bug fixes (first wave: B1, B3, B6, B8)

Size: M    Tier: 3 (decided, D-052 to D-056)    Assigned to: miso-implementer (one chunk per run)
Branch: thj/oct-build-fixes (= `main`); the same code is wanted on `main`, so no other branch needs it first
Status: approved

## Why

Oct 2026 playtests (`playtests/2026-10-playtest-tasks.md`, Batch 1). Root causes found by Explore on 2026-10-18; THJ's calls in D-052 to D-056.

## Goal

Mark's Cleanse stops freezing combat (and no ability can freeze it again), living enemies never show 0 HP, the map mission panel is on screen, and clicks no longer reach the game while a tutorial panel is open.

## Acceptance criteria

- [ ] B1: Mark's animator has a Cleanse state (copy of John's matching motion); `Unit_Mark.prefab` ability slot 4 points at it with an activation frame that fits the clip; Cleanse resolves every time in *In My Father's Arms* and the corrupted tile clears.
- [ ] B1 safety net: an ability whose `stateName` doesn't exist in the animator logs one clear error (ability name, unit, state) and activates and completes immediately, as the `suppressAnimation` path does. An EditMode test covers the missing-state decision.
- [ ] B3: a living unit's HP text never reads 0 (shows 1 while the HP ratio is above 0 and the unit is alive); 0 still shows when dead. Rounding of HP values is not touched (D-054).
- [ ] B6: the mission info panel is fully inside the screen on the world map and the mission map at 16:9 and at 16:10 and 4:3 in the Game view.
- [ ] B8: while a tutorial panel is open, mouse clicks, Cancel, Switch, Toggle and Pause do nothing in combat; when it closes, the input mode that was active before is restored; a turn change while it is open does not re-enable input.
- [ ] Nothing else changes. B9, Q21 and B5 are out (see Scope).

## Scope

In: B1 (data + safety net), B3 (display only), B6, B8.
Out: B9 pushback (held for S3, D-053); Q21 Cyclone (bundled with S10, D-055); B5 Workshop (needs a repro, D-056); changes to HP rounding, `Attributes`, `AbilityDamagePreview`; Mark's real Cleanse animation (THJ does it); AI regression test.

## Touches

Systems: `RuntimeAbility` (core, B1 safety net); `EntityAnimationHandler` (not core); `PlayerInputController`, `PlayerController`, `CombatLevelRunHandler`, `CombatLevelUIManager` (core, B8); `UI_Element_FillBar` (B3); Mark's prefab and animator (B1); `LevelInfoPanel.prefab` (B6)
USPs: none directly (Cleanse is a shared ability)
Docs: `tech/combat-architecture.md` if the input-lock pattern is worth a line; `build-log.md` at the end; `playtests/2026-10-playtest-tasks.md` status marks by the coordinator

## Approach

Chunks run in order; each is one implementer run and one commit.

1. **C1 · B1 data fix** (sonnet). In `AC_Playable_Mark.controller` add a state for Cleanse by duplicating the matching state/clip John uses for his Cleanse slot (his prefab slot 5, `SoulSacrifice`; confirm which clip). Point `Unit_Mark.prefab` `abilityOrchestrator.abilities[4]` `animationData.stateName` at the new state; set `abilityActivationFrame` to the clip's hit frame. Name the state so THJ can swap in Mark's own clip later and say so in the report. Check Mark's other ability slots for states the controller lacks, and list any (don't fix). Use small YAML edits or an editor script; keep GUIDs and `.meta` files intact.
2. **C2 · B1 safety net** (opus; core). In `RuntimeAbility` EventBasedAnimated path (around line 372), or in `EntityAnimationHandler.Play`, check the state exists (`animator.HasState(layer, Animator.StringToHash(name))`). Missing: log an error once per ability and take the existing `suppressAnimation` path so the ability activates and completes. Keep the decision in a small pure helper so an EditMode test can cover it. No other behaviour changes. Own commit.
3. **C3 · B3 display** (sonnet). `UI_Element_FillBar.cs:46`: show `max(1, RoundToInt(...))` while the ratio is above 0 / the unit is alive. Leave the ratio and everything in attributes alone. Check other HP texts that use the same bar (enemy panel, allies, tooltips) and note any that format HP another way.
4. **C4 · B6 map panel** (sonnet). Re-anchor `LevelInfoPanel.prefab` root to the right edge (anchorMin.x = anchorMax.x = 1, pivot.x = 1, small negative x offset). The prefab is shared by `WorldMapPanel.prefab` and `MissionMap.prefab`: check both instances for overrides and check three aspect ratios.
5. **C5 · B8 tutorial input lock** (opus; core input). In `CombatLevelUIManager.ShowTutorial`, save `PlayerInputController.Instance.ActiveActionMode`, set `ActionMode.Pause` (or the mode `EnemyIntroductionController` uses), restore on `OnTutorialClosed`. Guard against `PlayerController` / `CombatLevelRunHandler` calling `SetInteractionMode` while `IsTutorialOpen` (a lock count in `PlayerInputController` if that is the clean way, so the pause menu and the enemy introduction can't clash). Note the `ActiveActionMode` getter returns `None` when input is inactive: restore must handle it. Own commit.

6. **C6 · B5 Workshop diagnostic + hardening** (sonnet; Home UI, not core; added 2026-10-18, THJ's yes). Scope `HomeInteractables.cs` only (`Features/Home - Imported/___Khashayar/`). (a) Move the lock evaluation into `RefreshLock()` and call it from `Awake`, `OnEnable` and the start of each `OnPointer*` handler; re-apply `homeInteractableUI.SetActive(!_isLocked)` when the result changes. (b) Add a temporary diagnostic log, tagged `[B5-DIAG]` so it is easy to remove: on Awake and on every OnPointerEnter/Down, log the object name, `_isLocked`, each `UnlockAfterMissions` entry's name and `Completed`, `PlayerInputController.Instance.ActiveActionMode`, and whether `HomeManager.Instance` is mid-sequence. Explore's candidates (D-056 follow-up): input gated by `HomeManager.StartIE` / the mission-completion sequence, an empty `WorkshopPanelUI.ShowPanel` on first open, or a collider/UI covering the Workshop. THJ repros once and sends the log; the `[B5-DIAG]` lines are removed in the fix chunk. Acceptance: compiles; logs appear in Play; lock behaviour otherwise unchanged. Do not call B5 fixed.

Order: C1, C2, C3, C4, C5, C6. If C5 turns out to need a public API change on `PlayerInputController`, stop and report; that is Tier 3.

## Risks

- `RuntimeAbility` is core: the safety net must not change timing for abilities whose state exists. Reviewer checks this.
- B8: tutorials can fire mid-turn; a stale restored mode would break the turn. Test: open a tutorial mid-player-turn and on turn change.
- Prefab and animator edits in YAML: keep CRLF/LF as each file has it; if an edit isn't clearly safe, use an editor script and report.
- New statics or caches: none expected; if C5 adds a lock count it needs a `PlayModeStaticReset` hook.
- AI content untouched, so `AIRegressionTest` must not move (the known red stays red for its old reason only).
- Other branches: `thj/home-test` will want C1 to C5 on its next merge of `main`.

## Gates

Compile (verifier, via Unity MCP) / EditMode tests (all green except `AIRegressionTest.Baseline_MatchesCurrentAI`) / reviewer on C2 and C5 (core) / play check: yes, B1 (cast Cleanse in *In My Father's Arms*), B8 (tutorial in Level 1), B6 (open the world map) — needs THJ's time, so the verifier asks for a slot / docs: `build-log.md`, task-list marks.

## Commit log (option 1, THJ 2026-10-18: no Co-Authored-By line; hashes recorded here)

Shared repo, branch `thj/oct-build-fixes`, committed by the coordinator after THJ's yes on each.

| Chunk | Hash | Message |
| --- | --- | --- |
| C1 | `7f85fbbf7` | fix: add placeholder SoulSacrifice (Cleanse) state to Mark's animator |
| C2 | `952ab9d5a` | fix: ability fires immediately when its animation state is missing, instead of freezing combat |
| C3 | `66481e4e1` | fix: HP bar text never shows 0 while the unit is alive |
| C4 | `cabdb63a6` | fix: world map mission panel anchored to the right edge |
| C5 | `01e561ad2` | fix: lock player input while a tutorial panel is open (B8) |
| C6 | `47cee8ad9` | chore: Workshop lock refresh and temporary B5 diagnostic logs |
| B7 | `3c02126b8` | fix: safe room objectives name both steps (B7) |
| B7 r2 | `7550ea164` | fix: Divine Relic room objective names both steps (B7) |

C1 to C4 carry a Co-Authored-By line (THJ: fine to keep). Later commits don't.
