# Report: Enemy alert state, C2 (Unaware marker and wake pop)

Plan: plans/2026-10-23-enemy-alert-state-tech.md (C2)    Agent: miso-implementer    Branch: main (not switched)
Outcome: done (compiles, EditMode 723/724, only the known red fails; the look and timing need THJ's play check)

## What changed

All under `miso/Assets/_Project/Core/Systems/EnemyAlertSystem/`. New files are LF, no BOM, like the C1 files.

New:
- `Runtime/EnemyAlertVisualRules.cs` (+ `.meta`): pure `PopDelay(step, secondsPerStep)` (step x stagger, never negative) and `ShowsMarker(levelActive, unaware, alive, onBoard)`.
- `Runtime/EnemyAlertTracker.Visuals.cs` (+ `.meta`): partial of the tracker. Marker sync, wake pop, quiet tag add. Serialized fields with defaults: `popSecondsPerStep` (0.1), `popText` ("!"), `popColor`, `markerOffset` (0, 0.25, 0), `markerScale` (1), `fallbackSortingLayerId` / `fallbackSortingOrder`.
- `Editor/EnemyAlertVisualTests.cs` (+ `.meta`): 13 cases (stagger, marker rule, the Unaware tag has an icon).

Changed (small, in C1's uncommitted files, listed separately as asked):
- `Runtime/EnemyAlertTracker.cs`: in `Register`, the `ApplyModifiers(... AddSelf ...)` call became `AddUnawareTagQuietly(unit)`.
- `Runtime/EnemyAlertTracker.Events.cs`: `Subscribe` adds `UnitAlerted += ShowWakePop;`; `Unsubscribe` starts with `UnitAlerted -= ShowWakePop; ClearVisuals();` (it runs on disable and destroy).

No prefab or asset edit: the new serialized fields have in-code defaults, which Unity uses for the tracker already on `LevelBase.prefab` (the values only show in the Inspector after the prefab is next saved). No core-system, AI graph, variable or ability change. AIRegressionTest untouched. No statics.

## How it works

- **Marker:** each `LateUpdate` the tracker reconciles markers with its own Unaware set. Every Unaware, alive, on-board unit gets a `SpriteRenderer` child ("UnawareMarker") of the unit. A marker is destroyed when its unit wakes, dies or leaves the board, or the level ends. So it appears the frame a unit becomes Unaware (level start, spawn) and goes on wake, death or level end with no extra hooks. `Unsubscribe` (disable, destroy) clears all markers.
- **Sprite:** the Unaware tag's own icon (`GTag.TagIcon`, currently C1's placeholder lamp). Swap the tag's icon and the marker follows.
- **Sorting:** copies the sorting layer and order of the unit's mini health bar canvas (root canvas of `UnitMiniHealthBar`); falls back to layer id 1097219007 / order 0 (the bar's values in `UnitBase.prefab`) when a unit has no bar. Position: the bar's world position plus `markerOffset` (the bar sits where the info panel opens), else the popup point, else the unit's feet. Parented to the unit, so it follows pushes.
- **Pop:** on `UnitAlerted(unit, step, showPop)`, only if `showPop`. The int is the spread chain step (`AlertSpreadStep.Depth`: 0 = woken directly, +1 per hop). Step 0 pops at once; step n waits n x 0.1 s (coroutine on the tracker, stops with it). Uses `DamageNumberManager.ShowText` at the unit's `DamageNumberTrigger.StartPosition`, the path `GUnit.ShowTagGained` uses. Skipped if the unit died, was deactivated or the level ended meanwhile.

## D-159 route chosen (no core change)

`GUnit.ShowTagGained` returns early when `!isActiveAndEnabled`. `GUnit` has no `OnEnable`/`OnDisable` (nor do `GameEntity` or `GridPluggableEntity`), so the tracker sets `unit.enabled = false` around the `AddSelf` call and restores the previous value in a `finally`. The tag stays `showInGame`, so the info-panel Unaware line and tooltip are unchanged. `OnTagGained` still fires for other subscribers (combat log, watchers).

Tradeoff: it relies on that guard in `ShowTagGained`. If `GUnit` ever gains an `OnEnable`/`OnDisable`, the toggle would have side effects. Alternatives checked: `showInGame` off (also removes the info line, since panel and tooltip read the same flag); a prefab default tag (silent, because `Initialize` runs before the subscription, but the state is rule-based, so no). Smallest core option if THJ dislikes the toggle: an opt-out check in `ShowTagGained` (one line). Not made.

## Acceptance criteria (C2 part)

- [x] Marker over each Unaware enemy, sorted like the mini HP bar, removed on wake, death, level end: built, rule tested; **needs play** for the look and position.
- [x] "!" pop on wake only when the event's bool is true, staggered about 0.1 s per spread step: stagger tested (`PopDelay_*`); the bool gate and the timing **need play**.
- [x] No "Unaware" text pop on gaining the tag; info panel line stays: quiet add; **needs play**.
- [x] No pop at level start or spawn: C1 passes `showPop: false` for start-alert spreads, and tag gain no longer pops.
- [x] No core change; no AI graph, variable or ability edits; AIRegressionTest untouched.
- [x] Compile clean; EditMode 723/724.

## Test results

Batchmode, Unity 6000.3.4f1, editor closed (no `miso/Temp`); `results.xml` and `test.log` in the scratchpad. 724 tests, 723 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red). The new `EnemyAlertVisualTests` cases all pass. The first run hit a compile error (`GTag` is not a Unity object), fixed. No compiler warnings from the new files. The run changed no other asset (Content and Resources diff is still C1's 36 lines).

## Save reset

No.

## Decisions I made

- Markers are reconciled from tracker state each frame instead of hooking registration and death separately: fewer C1 edits, one place to check.
- Marker sprite is the tag's icon instead of a new serialized sprite (no prefab edit).
- Visual tunables are serialized fields on the existing tracker (partial file) instead of a new component (no `LevelBase.prefab` edit).

## Needs THJ

None blocking. To tune in play: marker offset and scale (the placeholder lamp may look large or overlap the mini bar), pop colour.

## Docs to update

- `tech/combat-architecture.md` (coordinator): C2 visuals (marker from the tag icon, quiet tag add, pop stagger field).

## Risks and loose ends

- The quiet add depends on `GUnit` having no `OnEnable`/`OnDisable` (above).
- Marker position is taken from the mini bar's world position at creation; if a bar moves later, the marker doesn't. Can't judge the look without play.
- `EnemyAlertTracker` now references `MISO.Content.UI.UnitMiniHealthBar` (a Features type) for the sorting; same assembly, and the fallback fields cover a missing bar.
- The marker is a world `SpriteRenderer` while the bar is a world-space canvas; if the order looks wrong in play, adjust the fallback fields or offset.
- A wake pop is silently skipped if `DamageNumberManager` is absent (dev scenes).
- C1 loose ends (Masher preview, deferred sight checks) are unchanged.

## Proposed commits

1. `feat(enemies): an Unaware marker over sleeping enemies and a staggered "!" when they wake` (plain, no assets):
   `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertVisualRules.cs` + `.meta`, `Runtime/EnemyAlertTracker.Visuals.cs` + `.meta`, `Editor/EnemyAlertVisualTests.cs` + `.meta`, plus the two edited C1 files `Runtime/EnemyAlertTracker.cs` and `Runtime/EnemyAlertTracker.Events.cs`.

**Depends on C1's uncommitted commit 2: yes.** `EnemyAlertTracker.cs` and `.Events.cs` are still untracked, and the Visuals partial needs them (private fields, `UnitAlerted`, `_unaware`). Two ways to order it: (a) commit C1's commit 2 first with its files as they are now (they already contain the two small edits), then this commit holds only the six new files; (b) commit 2 and C2 together. Option (a) leaves the tracker referencing `AddUnawareTagQuietly` and `ShowWakePop` before they exist, so it will not compile on its own: commit 2 must either include the Visuals partial or come after it. The clean split is therefore: commit 2 (C1) plus this commit staged together, or one commit holding the tracker files and the six new files. The coordinator should pick; per the play-test-before-commit rule both wait for THJ's play anyway.

## Other branches

`thj/home-test` when it takes `main`, as C1.

## How to see it

1. Open Unity (recompile), open a Generic level with far-away enemies, press Play.
2. Each Unaware enemy has the lamp marker over it (sorted with its mini health bar). No "Unaware" text pops; hover an enemy: the info panel still has the Unaware line.
3. Walk a Bergson to stop within sight of a Dark Claw in a pack: a red "!" pops on it, then on its neighbours one after another about 0.1 s apart; their markers disappear as they wake.
4. Enemies that start alert because they see the family at level start (and anything they wake by spread) wake with no "!".
5. A Shaman summon starts Unaware: marker, no text pop. Kill an Unaware enemy: its marker goes. Win or lose: no markers left.
6. To tune, change Pop Seconds Per Step, Marker Offset and Marker Scale on the `EnemyAlertTracker` of LevelBase.
