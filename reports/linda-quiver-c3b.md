# Report: Linda's Quiver C3b, Mark's Catch & Return with a prompt

Plan: plans/2026-10-26-linda-quiver-tech.md (C3b)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done in code, not compiled and not run (the editor is open; nothing was executed). Needs the Test Runner and the play check.

## What changed

- miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs: freeze-and-press flow. Contact disables the original Projectile component (collider stays on, no slow-mo added), builds the return copy from the new `returnPrefab` field, holds the landing, turns Mark and starts the prompt. Decline, prompt failing to start, or OnDisable releases (component back on, landing released, unused copy destroyed). Press returns the arrow to the quiver (existing "+1" cue), keeps the original visible in Mark's hand, and at the apply frame (or the 1 s unscaled fallback in Update) hides the original, activates the copy and wires `copy.onDestroy` to dispose the original. The dead `_pending.Dispose()` comment and the unused `BounceBack` method are gone.
- miso/Assets/_Project/Features/Player/Mark/Scripts/CatchFreezeRules.cs (+ .meta): pure state for freeze, release, press, apply-once and the fallback timer.
- miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchFreezeRulesTests.cs (+ .meta) and Editor.meta: 10 EditMode tests.
- miso/Assets/_Project/Features/Player/Linda/Prefabs/LindaAttackArrowReturn.prefab (+ .meta): copy of LindaAttackArrow with `travelEntireRadius: 0`, new guid a6b15f946c59438ca55d8906cb35b92c. In no whitelist.
- miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab: `triggerWithQTE: 1`, `returnPrefab` set to the new prefab.
- miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/CatchReturnWiringTests.cs (+ .meta): 3 wiring tests.
- claude-handoff/playtests/2026-10-27-mark-catch-qte-play-check.md: numbered play steps.

No core-system code touched (Projectile, QuickTimeEventHandler, EntityAnimationHandler used through public API only). LF endings, no BOM, as the files were. No new statics.

## Acceptance criteria

- [ ] Arrow freezes at Mark during the prompt: `Projectile.enabled = false` on contact. Play steps 1, 11.
- [ ] Pressed: +1 cue, catch animation, return flight ends at Linda and damages on the way, Linda's action waits: quiver return reuses the existing path; the return prefab has `travelEntireRadius 0` (wiring test); `onDestroy` is wired to dispose the original. Play steps 2-5.
- [ ] Declined: same arrow carries on and lands normally: `enabled = true` plus `ReleaseLanding`. Rules tested; play step 6.
- [ ] Nothing past Mark is hit after a press: the original stays frozen, then is disposed. Play step 5.
- [ ] Fallback timer releases a stuck catch: rules tested (applies once, silent after the frame); play step 7.
- [ ] Prompt failing to start or Mark disabled re-releases: rules tested; play steps 8, 9.
- [x] Prefab wiring (prompt on, return prefab set, radius 0, not whitelisted by Mark or the Cyclone): wiring tests, not yet run.
- Recall showing as "Encore": untouched here.

## Save reset

no

## Decisions I made

- The freeze applies in every return mode, not only the bounce ones. In Refund-only mode a press refunds, disposes the copy and disposes the original (it lands where it stopped). Mark's prefab uses BounceBackAndRefund, so this only affects an unused mode.
- Mark's trigger ignores new arrows while a catch is frozen or waiting for its frame.
- A declined catch now destroys the unused hidden copy (it used to stay inactive in the scene).
- The return arrow is a plain prefab copy, not a variant, as the plan allowed. If LindaAttackArrow is edited later, the copy must follow.
- The existing slow-mo code stays as it is (timescale is 1 on Mark's prefab, so it does nothing).

## Needs THJ

Run in Test Runner, EditMode: `MISO.Core.Features.Bergsons.EditorTests.CatchFreezeRulesTests` (10), `CatchReturnWiringTests` (3), then the whole suite. Then the play check.

## Docs to update

- build-log.md: C3b section after the play check.
- status.md: C3b built, awaiting the play check.

## Risks and loose ends

- Not compiled. Signatures checked by reading: `Projectile.GetClone(SpawnableEntity, GridCell, Vector3, GridCell)`, `SpawnableEntity.onDestroy`, `Dispose`, `GetMainVisual`, `EntityAnimationHandler.Play(EntityAnimationData, Action<int>)`.
- `returnPrefab` is typed Projectile; the YAML reference points at the Projectile component of the copy (fileID -6961319225189814693, the same id the original prefab's whitelist reference uses). If Unity shows it as missing, reassign it in the Inspector.
- Spike risks still open: the arrow freezes at the edge of Mark's collider; a disabled component may still get triggers (the arrow's QuiverArrow is a separate component and stays on); the return flight re-hits enemies with falloff restarting at 1.0 (balance); one prompt and one held arrow per Mark.
- The animation handler's Play flushes the previous animation's remaining frames; the apply-once rule covers a late or repeated apply frame.

## Proposed commits

1. feat(mark): freeze Linda's arrow at Mark during the catch prompt and fly it home: CatchFreezeRules.cs(+meta), ProjectileCatchAndReturn.cs, Mark Scripts/Editor.meta, Editor/CatchFreezeRulesTests.cs(+meta), Linda Scripts/Quiver/GroundedArrowField.cs (plain)
2. feat(linda): a return arrow that ends its flight at Linda: LindaAttackArrowReturn.prefab(+meta) (plain)
3. feat(mark): make the catch a prompt and use the return arrow: Unit_Mark.prefab, Editor/CatchReturnWiringTests.cs(+meta) (plain; needs 1 and 2)

## Other branches

none

## How to see it

Follow playtests/2026-10-27-mark-catch-qte-play-check.md.

## Review fixes

- Time scale: the prompt path no longer touches `Time.timeScale` (slow-mo methods and their state removed). The `timescale` field stays serialized and unused, with a comment, so the prefab is unchanged.
- Teardown: `RefundShot` guards a null owner and a missing `CombatLevelUIManager`. When Mark is disabled while an arrow is caught, the return flight starts only if a grounded-arrow field is open (the level is running); otherwise the copy is destroyed and the original disposed. Mid-level behaviour is unchanged, so no hang.
- `CatchReturnWiringTests.cs` converted to LF.
- The two duplicate rules tests are merged into `ReleasedArrow_NeverStartsAReturnFlight` (now 9 tests in `CatchFreezeRulesTests`).
- Play check: items 13-15 are the reviewer's, 16-17 cover the time scale and teardown fixes.
- Still not compiled or run.
- Re-review fix: `GroundedArrowField.IsOpen` (true until the level ends) added; the disable check now tests `Current is { IsOpen: true }`, since a field stays "current" after the level ends. `GroundedArrowField.cs` goes in commit 1.

## Faster catch prompt

THJ found the catch prompt slow. The prompt waited 0.05 s, then played Show, then waited the button's `preloadTime` (0.6 s) before input opened, so about 0.65 s. Now each QTE profile can override both values; Mark's catch uses 0.25 s preload and 2x show speed, so input opens about 0.3 s after the arrow touches Mark. Every other profile keeps the defaults (-1 and 1), so role QTEs are unchanged. Not compiled or run (editor is open).

### Files
- Core/Interactions/Runtime/QTEProfile.cs: two optional serialized fields, `preloadOverride = -1f`, `showSpeed = 1f` (Min 0.01), with getters `PreloadOverride`, `ShowSpeed`. Unserialized fields on old data take the initializers.
- Core/Interactions/Runtime/QTEPromptTiming.cs (+meta, new): pure helper `ResolvePreload(override, default)` (negative uses the default; 0 counts as a real value) and `ResolveShowSpeed(speed)` (non-positive falls back to 1).
- Features/UI/Panels/Scripts/QTEButton.cs: `Prepare` resolves both from the profile. `Initialize` remembers the animator's own speed. `Prepare` resets `animator.speed`; `ProcessIE` sets speed x showSpeed for Show, waits the resolved preload, then restores the speed; `Finish` restores it too, so pooled buttons never carry it over and Notice/Miss play at normal speed. `QuickTimeEventHandler.cs` is untouched (the profile already reaches the button via `Prepare`). `QTEButton.prefab` and the show clip are untouched.
- Core/Interactions/Editor/QTEPromptTimingTests.cs (+meta, new): 7 tests (negative uses default, 0.25 used, 0 used, speed 1, speed 2, non-positive speed, default profile unchanged).
- Features/Player/Mark/Prefabs/Unit_Mark.prefab: the profile is inline in the ProjectileCatchAndReturn component; added `preloadOverride: 0.25` and `showSpeed: 2` after `validRange` (2 lines, only that one profile; the other two MarkQTE profiles in the prefab are unchanged).
- Linda/Scripts/Quiver/Editor/CatchReturnWiringTests.cs: new `MarksCatch_PromptAppearsFast` (preload 0.25, show speed 2).

### Exact core diff
```
QTEProfile.cs  (before [NonSerialized] public float InitialHoldTime;)
+ [Header("Prompt timing (optional)")]
+ [Tooltip("Seconds between the prompt showing and input opening. Negative uses the button's own preload time.")]
+ [SerializeField] private float preloadOverride = -1f;
+ [Tooltip("Speed multiplier for the prompt's Show animation. 1 leaves it unchanged.")]
+ [SerializeField, Min(0.01f)] private float showSpeed = 1f;
+ public float PreloadOverride => preloadOverride;
+ public float ShowSpeed => showSpeed;

QTEButton.cs
+ private float _defaultAnimatorSpeed = 1f; private float _preloadTime; private float _showSpeed = 1f;
Initialize:  + if (animator) _defaultAnimatorSpeed = animator.speed;
Prepare:     + _preloadTime = QTEPromptTiming.ResolvePreload(profile.PreloadOverride, preloadTime);
             + _showSpeed = QTEPromptTiming.ResolveShowSpeed(profile.ShowSpeed);
             + animator.speed = _defaultAnimatorSpeed;   (after updateMode)
ProcessIE:   + animator.speed = _defaultAnimatorSpeed * _showSpeed;   (before SetTrigger("Show"))
             - yield return new WaitForSecondsRealtime(preloadTime);
             + yield return new WaitForSecondsRealtime(_preloadTime);
             + animator.speed = _defaultAnimatorSpeed;
Finish:      + animator.speed = _defaultAnimatorSpeed;   (before the Notice/Miss trigger)
```

### Tests for THJ
EditMode > Run All: `QTEPromptTimingTests` (7) and `CatchReturnWiringTests.MarksCatch_PromptAppearsFast`. Everything else should stay green apart from the known `AIRegressionTest.Baseline_MatchesCurrentAI`. Check the console for the new `Min` attribute or serialization warnings after recompile.

### Updated commit units (build order)
0. NEW, own commit, core QTE: feat(qte): let a prompt override its preload and Show speed: Core/Interactions/Runtime/QTEProfile.cs, Core/Interactions/Runtime/QTEPromptTiming.cs(+meta), Features/UI/Panels/Scripts/QTEButton.cs, Core/Interactions/Editor/QTEPromptTimingTests.cs(+meta)
1. feat(mark): freeze Linda's arrow at Mark during the catch prompt and fly it home (unchanged)
2. feat(linda): a return arrow that ends its flight at Linda (unchanged)
3. feat(mark): make the catch a prompt and use the return arrow: Unit_Mark.prefab (now also carries the 0.25 / 2 values), Editor/CatchReturnWiringTests.cs(+meta) (needs 0, 1 and 2, since the prefab keys name fields from 0)

### Play step
Play a level with Linda and Mark with the synergy active. Shoot an arrow that Mark catches from 2+ tiles. From the arrow touching Mark, the catch prompt should show and be pressable in about 0.3 s (Show animation visibly quicker, finished before input opens). Press it and confirm the catch and return still work, and after it the next QTE is normal. Then trigger a role QTE (any other unit's prompt): it must look and time exactly as before (about 0.65 s to input, normal animation speed). Also check a prompt right after a catch prompt (pooled button) is not sped up.

## Play findings fixes

From `reports/mark-catch-play-findings.md` and D-273 to D-276. Four fixes:
- A1: the return arrow stops on Linda's body.
- A2: a long frame can no longer skip Mark.
- E: the frozen arrow sits in Mark's hand.
- B: Lucy follows up only on enemies whose HP really dropped.

`Projectile.cs` is untouched. The only core change is Lucy's Family Role handler (D-275, THJ-approved). Not compiled or run: the editor is open, so no batch Unity. Every API used was checked by reading the source (listed under Risks).

### Files
- `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`:
  - (A2) The body of `OnTriggerEnter2D` is now `public bool TryCatch(Projectile)`, with the same checks in the same order. The trigger only fetches the projectile and calls it.
  - (A2) A one-chance-per-arrow guard, `_lastSeen`. The first call that gets past the "alive" check marks the arrow; every later call for that arrow returns false. That covers the trigger and the sweep both reporting one pass, and an arrow that a decline lets go flying on through Mark.
  - (E) `FreezeArrow` saves the arrow's path position, then moves it to `returnSource.position`, keeping the arrow's own z. `ReleaseFrozenArrow` puts it back on the path position before turning the projectile back on (see Decisions).
  - (A1) `PrepareProjectileClone` records the copy's start and end:
    - start: `spawnAt`;
    - end: `ReturnDestination(cell)`, which is the occupant's `TargetPoint` and otherwise `AnchorPoint` (the same rule `Projectile.Initialize` uses for Occupant).
  - (A1) `Apply` hands both points to `_inFlight*`. A new `LateUpdate` puts the flying copy on its end once it is at or past it, and stops once the copy is no longer alive.
- `Features/Player/Mark/Scripts/ReturnFlightClamp.cs` (+meta, new): pure `TryClamp(from, to, position, out clamped)`. It projects onto the line from start to end and clamps at or past the end. A path with no length always counts as at the end.
- `Features/Player/Mark/Scripts/CatchSweep.cs` (+meta, new), on Linda's arrow:
  - In `LateUpdate` it runs `Physics2D.CircleCast(from, radius, dir, ContactFilter2D{useTriggers=true}, RaycastHit2D[8], distance)` from the previous position to the current one.
  - It calls `TryCatch` on the `ProjectileCatchAndReturn` of the hit collider's object or of its attached rigidbody. Mark's root has his box collider and rigidbody.
  - It skips arrows that are disabled (frozen) or dead, and copies: `QuiverArrow.IsCopy`, or a null `PrefabSource` (the Cyclone splits). It also skips the first frame after enable.
  - The radius is the arrow's CircleCollider2D radius × scale (0.1), unless set.
  - It allocates nothing per frame: preallocated buffer, struct filter, `TryGetComponent`.
- `Features/Player/Mark/Scripts/Editor/ReturnFlightClampTests.cs` (+meta, new): 6 tests.
- `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab`: adds the `CatchSweep` component (fileID 7547959531454712506, script guid 377bfd22b253484f871d38542a3b6405, `radius: 0`). A 14-line edit.
- `Features/Player/Linda/Prefabs/LindaAttackArrowReturn.prefab`: `destinationMode: 0` → `1` (Occupant).
  - In `Projectile.Initialize` (lines 160-168), Occupant aims at `GUnit.TargetPoint` when the target cell's occupant is a unit, and at the cell anchor otherwise.
  - The return copy's target cell is Linda's cell (`travelEntireRadius: 0`), so the arrow now ends on her body.
- `Features/Player/Linda/Scripts/Quiver/Editor/CatchReturnWiringTests.cs`: 3 new tests:
  - `ReturnArrow_EndsOnLindasBody`: destinationMode is 1.
  - `EveryCatchableArrow_SweepsForTheCatch`: every whitelisted prefab has a CatchSweep.
  - `ReturnArrow_DoesNotSweep`.
- Lucy (core, its own unit): `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`, `LucyRoleTargetRanking.cs`, `Editor/LucyRoleHpDropTests.cs` (+meta, new, 7 tests).

### Exact Lucy diff summary
```
LucyRoleTargetRanking.cs
  header comment: ranking only among enemies whose HP actually dropped during the action
+ public static bool HpDropped(float? hpAtActionStart, float hpNow)
+     => hpAtActionStart.HasValue && hpNow < hpAtActionStart.Value;
+ public static Candidate<T> FromAction<T>(T unit, bool isAimedAt, bool reportedHit, bool hpDropped, int distance)
+     => new(unit, isAimedAt && hpDropped, reportedHit && hpDropped, distance);
  (Pick and Candidate unchanged)

LucyFactionRoleHandler.cs
+ private readonly Dictionary<ActionLogEntry, Dictionary<GUnit, float>> _hpAtActionStart = new();
  Rebind: also Remove/AddListener abilityActivationStarted -> OnAbilityActivationStarted; clears _hpAtActionStart
+ OnAbilityActivationStarted(RuntimeAbility):
      entry = ActionsInProgress.LastOrDefault(a => a.Ability == ability); none -> return
      prune entries no longer in the session log (same rule as _hitsByAction)
      first activation of an entry only (ContainsKey -> return)
      snapshot[e] = e.GetHealthAttribute().Value for every AliveUnit of every faction hostile to Lucy
  PrepareTargets:
+     _hpAtActionStart.TryGetValue(lastAction, out var hpAtStart);
      per candidate:
+     float? hpBefore = hpAtStart has e ? its HP : null;  hurt = HpDropped(hpBefore, health.Value)
-     new Candidate(e, namedTarget || onTargetCell, hitByThisAction, distance)
+     LucyRoleTargetRanking.FromAction(e, namedTarget || onTargetCell, hitByThisAction, hurt, distance)
```
- **Ordering.** The D-152 ordering is unchanged: aimed target first, then an enemy this action hit, then distance and list order. Both ranks now also need a real HP drop.
- **Completion echo.** `RuntimeAbility.OnCompletionShared` raises `onAbilityEffectPerformedOn` on the targets, so the aimed occupant is still recorded as hit. Without an HP drop it no longer counts.
- **Snapshot timing.** The snapshot is taken before any damage.
  - `abilityActivationStarted` is raised from the activation callback, before `preset.Activate` runs the effects (`RuntimeAbility._ActivateAbility`).
  - Every path that raises `abilityPerformed` also raises `abilityActivationStarted` first. `abilityPerformed` is what triggers Lucy's role (triggerEvents 4). The paths are: the faction controller; the Linda, Lucy and Mark handlers; John's Shield Dash; Mark's Continuous Attack; the Masher counter.
  - Lucy reads at completion, and the HP drop is visible by then. `CombatLevelRunHandler.OnAbilityPerformedOn` reads the same live value later in that same completion to work out the damage.
- **Threads.** Everything runs on the main thread, from bus events. The AI never reads Family Role handlers (only `AIRegressionTest` mentions them). No new statics.
- **Other branches.** Main and the other branches need this too (D-275). It is self-contained: these three files plus the test.

### Decisions I made
- **A1, the clamp.** It lives in `ProjectileCatchAndReturn.LateUpdate` (the plan's first option), with the math in a pure class. It mirrors the Occupant rule for the end point, so if the return prefab were set back to Cell, the clamp would still stop the arrow on Linda's body. The wiring test guards Occupant.
- **E, a decline.** The arrow is put back on its saved path position before it resumes, rather than jumping on the projectile's next Update. The behaviour is the same: it jumps back onto its path. This avoids a one-frame backwards flip: the arrow is `headAxis: Right` and faces from its current position to its next one, and seen from the catch point that next step can point backwards.
- **A2, the guard.** It marks the arrow on its first evaluation, even when the catch is then refused (wrong owner, off the path, too close). Each pass gets one decision, as with the single trigger enter before.
  - The early checks (a prompt already open, Mark mid-catch) run before the marking, as they did. So while the arrow still overlaps Mark, the sweep can try again the next frame if another prompt has just closed.
  - Trigger-only behaviour is unchanged.
- **Sweep location.** The sweep is in Mark's Scripts folder: it belongs to his catch and sits next to `ProjectileCatchAndReturn`.
- **Lucy, edge cases.** An enemy with no HP reading from the action's start counts as not hurt (for example one spawned mid-action). The hit record still matters for rank 2 (`reportedHit && hpDropped`), so an HP drop during the action from something else doesn't count as this action's hit.

### Risks and loose ends
- Not compiled. Signatures checked by reading:
  - `Physics2D.CircleCast(Vector2, float, Vector2, ContactFilter2D, RaycastHit2D[], float)`, the non-obsolete form of CircleCastNonAlloc;
  - `ContactFilter2D.useTriggers`, `Collider2D.attachedRigidbody`;
  - `SpawnableEntity.PrefabSource` (public field), `Projectile.IsAlive`;
  - `GUnit.TargetPoint` (Vector3), `GridCell.AnchorPoint` (Vector3), `GridCell.OccupantEntity`;
  - `GUnit.GetHealthAttribute().Value` (float), `Faction.Controller.AliveUnits`, `CombatLevel.GetFactionEnemies`;
  - `GlobalEventBus.abilityActivationStarted` (UnityEvent<RuntimeAbility>).
- **Lucy, behaviour change beyond the catch.** An ally attack that lands but does no HP damage no longer gets her follow-up, even on the aimed target. That covers a fully absorbed hit, a status-only hit, and a move whose target takes no damage.
  - Damage dealt after its action completed would not count either. I found none: a projectile spawn keeps its action open until the projectile is destroyed. Play step 25 checks it.
- **Skipped enemies on a long frame.** The sweep catches at the arrow's first touch of Mark's box, as the trigger does. Enemies between the previous position and Mark that a long frame skipped are still missed. That is the core projectile's discrete movement, not changed here.
- **Mark disabled mid-flight.** If Mark is disabled while the return copy is flying, the clamp stops with his LateUpdate. Only at level end.
- **Hand position.** `returnSource` may sit outside Mark's collider. That is harmless: the guard prevents a re-trigger.
- **Pre-existing, unchanged.** `Projectile.OnTriggerEnter2D` still runs on a disabled (frozen) projectile.

### Tests for THJ
EditMode > Run All. New or changed:
- `MISO.Core.Features.Bergsons.EditorTests.ReturnFlightClampTests` (6).
- `MISO.Core.Features.Bergsons.EditorTests.LucyRoleHpDropTests` (7):
  - aimed target not hurt: no follow-up;
  - aimed target hurt: rank 1;
  - aimed target not hurt and another enemy hurt: the other is picked;
  - no HP change anywhere: none;
  - hit reported without damage: none;
  - `HpDropped` edge cases;
  - hurt but not reported as this action's hit: stays out of the fallback.
- `CatchReturnWiringTests`: the existing four, plus the new `ReturnArrow_EndsOnLindasBody`, `EveryCatchableArrow_SweepsForTheCatch` and `ReturnArrow_DoesNotSweep`.
- The existing `LucyRoleTargetRankingTests` (14) should still pass unchanged: `Pick` and `Candidate` didn't change.

Everything else should stay green apart from the known `AIRegressionTest.Baseline_MatchesCurrentAI`. After the recompile, check that the console shows no "missing script" warning on `LindaAttackArrow`; if it does, re-add CatchSweep in the Inspector.

Covered by tests:
- A1: the clamp math, and the return prefab's Occupant mode.
- A2: the sweep is wired on the arrow.
- B: Lucy's rule.

Play check only:
- A2: a real catch at low fps.
- A1: the end point on Linda's body.
- E: the hand position.
- B: Lucy in play.

### Play steps
Added as steps 18-25 to `playtests/2026-10-27-mark-catch-qte-play-check.md`:
- low fps via the Profiler's Deep Profile;
- the return arrow ends on Linda's body;
- the freeze is in Mark's hand;
- a decline gives no flip and no second prompt;
- Lucy after a caught arrow, after a caught arrow whose return hits someone, and after a real hit;
- Lucy regressions.

### Updated commit units (build order)
1. **Core QTE**, its own commit (pending, unchanged). feat(qte): let a prompt override its preload and Show speed.
   - `Core/Interactions/Runtime/QTEProfile.cs`
   - `Core/Interactions/Runtime/QTEPromptTiming.cs` (+meta)
   - `Features/UI/Panels/Scripts/QTEButton.cs`
   - `Core/Interactions/Editor/QTEPromptTimingTests.cs` (+meta)
2. **Catch fixes** (non-core). fix(mark): catch Linda's arrow even on a long frame, hold it in Mark's hand and stop the return on Linda.
   - `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`
   - `Features/Player/Mark/Scripts/CatchSweep.cs` (+meta)
   - `Features/Player/Mark/Scripts/ReturnFlightClamp.cs` (+meta)
   - `Features/Player/Mark/Scripts/Editor/ReturnFlightClampTests.cs` (+meta)
   - `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab`
   - `Features/Player/Linda/Prefabs/LindaAttackArrowReturn.prefab`
3. **Mark prefab and wiring tests** (pending, now with more tests). feat(mark): make the catch a fast prompt that uses the return arrow.
   - `Features/Player/Mark/Prefabs/Unit_Mark.prefab`
   - `Features/Player/Linda/Scripts/Quiver/Editor/CatchReturnWiringTests.cs` (+meta)
   - Needs 1, because the prefab names the new profile fields. Needs 2, because the tests reference `CatchSweep` and check the arrow prefabs. That is why it now comes after the catch fixes.
4. **Lucy**, core, its own commit. fix(lucy): follow up only on enemies the ally's action actually hurt.
   - `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
   - `Features/Player/Lucy/Scripts/LucyRoleTargetRanking.cs`
   - `Features/Player/Lucy/Scripts/Editor/LucyRoleHpDropTests.cs` (+meta)
   - Independent of 1-3. Main and the other branches need it too.

Don't stage: the TMP fallback font asset, `ProjectSettings/EditorSettings.asset`, `ProjectSettings/ProjectSettings.asset`.

Save: not reset.
