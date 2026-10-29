# Report: Quiver switch, size as a stat (3), Encore in custom kits, projectile end clamp

Plan: plans/2026-10-29-quiver-switch-size-encore-clamp.md    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 3482eedf5)
Outcome: partial (code and data are done; one level is blocked, see "Needs THJ"; THJ still has to compile, run one Tools menu item and run the tests, because the editor was open)

Decisions: D-314 (global switch), D-315 (Mark's catch with the switch off), D-316 (size 3, Encore in custom kits), D-317 (core projectile clamp), D-319 (quiver size as a stat).

## What changed

### 1. Projectile end clamp (core, D-317)
- `Core/Entities/Runtime/Projectile.cs`: `Update` now caps `_progressTracker` at 1 when it advances: `_progressTracker = Mathf.Min(_progressTracker + _adjustedSpeed * Time.deltaTime, 1f);`, plus a two-line comment. BOM and LF kept.
- Checks:
  - Arrival still fires exactly once. The `>= 1` branch on the next frame calls `Activate`/`Dispose` and sets `IsAlive = false`, as before.
  - The sweep still covers the last segment. `_sweepStep.Begin` runs before the advance, and `SweepLastStep()` at the top of the next `Update` sweeps up to the clamped end point.
  - `_progressTracker` is read only in `Update` (the arrival test, `speed.Evaluate`, `GetPathPointInterpolated`). Nothing else reads it.
  - Trajectory events with `activationTime > 1` would no longer fire. The only one in the project is at 0.5.
  - Mark's freeze (`Projectile.enabled = false`) stops `Update` as before. The clamp doesn't touch it.

### 2. Global switch (core, additive, D-314)
- `Core/Managers/GlobalSettingsSO.cs`: new `[Header("Linda")]` section with `public bool lindaQuiverEnabled = true;` and a tooltip. `GlobalSettings.asset` is not edited. The asset has no value for the field, so the code default (on) applies until THJ saves the asset.
- `Features/Player/Linda/Scripts/Quiver/LindaQuiverSwitch.cs` (new): `IsOn` reads the settings on the main thread. It returns true when the settings can't be loaded. It holds no static state, so it needs no reset hook.

### 3. Quiver size as a stat (D-319, D-316)
- The stat is data only, so the plan's STOP point did not trigger. Attributes are entries in an `AAttributeDefinitionSetSO`, and `AAttributeRegistry` builds its map from the sets at run time. No enum or code list was needed.
  - `Resources/Attributes/StatAttributes.asset`: new entry `id: LQuiverSize`, title "Linda Quiver Size", group Stat, so the id is **`Stat_LQuiverSize`**. Hidden (`indicated: 0`), copied from the `ATBS` entry.
  - `Features/Player/Linda/Prefabs/Unit_Linda.prefab`:
    - Her unit stat set grows from 11 to 12 entries. `data[11]` is `Stat_LQuiverSize`, policy Additive, one level, factor **3**. These are the same four overrides as `data[10]` (`Stat_ATBS`).
    - The `LindaQuiver` block gets `size: 3` (the fallback) and `sizeStat: {entityID: Stat_LQuiverSize}`.
  - No level overrides Linda's stat array or her quiver block, so none needs a change.
- Reading the stat:
  - `QuiverSizeRules.cs` (new): `FromStat(hasStat, value, fallback)` rounds to whole arrows and never goes below 0. `Read(owner, stat, fallback)` evaluates the stat additively from 0 through `CalculateStatFactor`, which is the normal source chain Unit, Equipment, Skill tree, Faction. Without a reference, or when her set has no entry for it, it uses the serialized `size`.
  - `LindaQuiver.Size.cs` (new partial): the `sizeStat` field and `SyncSize()`.
- When the size is read: in `Start` and again on `levelStarted`, by which time her stats and equipment are prepared. Stat attributes raise no change event, so it isn't read again during a level.
- What a size change does:
  - `QuiverState.Resize(size, fillIfFull)` (new).
  - Shrinking drops the arrows that no longer fit.
  - Growing adds empty slots, except at level start, where a full quiver stays full.
  - A size change raises `OnChanged`.
- The views:
  - HUD: `QuiverUI` already shows one object per arrow held, so at size 3 the fourth slot stays hidden. New `QuiverUI.NoteSize(size)` warns once when the size passes the slot count; the extra arrows are not shown. `UnitPanelUI.Quiver.RefreshQuiver` calls it. The rule is `QuiverHudFeedbackRules.HasRoomFor`.
  - Pips: `QuiverPipsView` rebuilds both rows when `OnChanged` brings a new size. It warns once if the size passes the 8-pip cap.
- Tests that hard-coded 4:
  - `QuiverWiringTests.Linda_CarriesAQuiverOfFour` becomes `Linda_CarriesAQuiverOfThree`. It checks the size, the serialized fallback 3 and the stat reference.
  - `QuiverStateTests.LindaQuiver_HasArrow_FollowsTheCount` now uses `quiver.Size`.
  - The other tests that use 4 test rules with a sample size and stay as they are.

### 4. Quiver gating and the catch fallback (D-314, D-315)
- `LindaQuiver.Switch.cs` (new partial):
  - `Awake` stores the switch in `_switchOn`. That is a plain bool per Linda instance, so toggling between levels works with domain reload off.
  - `IsActive` is the main-thread read.
  - `ActiveForChecks` is the stored value for the feasibility checks, which may run on the AI worker thread and never load the asset.
  - `SetActiveForTests` sets the switch for one quiver in tests.
- `LindaQuiver.cs`:
  - `Of()` returns null when the quiver is switched off. Every quiver consumer goes through `Of()`: `QuiverArrow`, the HUD panel, the tooltip grey reason, the aim presenter, the role badge through `IsEmptyFor`, and the Duo lookup. So with the switch off they all see "no quiver", which is main's behavior.
  - `HasArrow` answers true when off, so shots are never blocked at 0.
  - `HasGroundedArrows` answers false when off.
  - `Recall()` does nothing when off.
  - `HidesRoleZone` is `IsActive && IsEmpty`.
  - `Start` and `OnLevelStarted` return early when off, so no grounded-arrow field, aim presenter, pips, "+N" cue or log listener is created.
- `QuiverAbilityInfo.cs`: the Duo partner check uses `LindaQuiver.Of` instead of `TryGetComponent`, so arrow Duos get no quiver HUD feedback when the switch is off.
- Encore with the switch off stays on the bar but **can never be cast**. That is the same state as with the switch on and nothing on the ground, and its tooltip gets no quiver line. I chose this over hiding it because hiding would need ability-bar code; this needs none.
- Mark's catch with the switch off:
  - `ProjectileCatchAndReturn.OnDisable` used to start the pending return flight only when the grounded-arrow field was open. With the switch off there is no field, so a return pending when Mark is disabled would have been dropped.
  - New pure rule `Features/Player/Mark/Scripts/CatchReturnRules.cs`: with the quiver on, the field decides (unchanged). With it off, the level run decides (level present, run active, not ended).
  - Everything else in the catch already works without a quiver: no arrow is held, so none goes to the quiver.
- With the switch off, every behavior the plan lists is off: arrow spending, blocked shots, grounded arrows and pickups, the HUD quiver, pips and "+1" cues, the log suffixes, the kill hand-back (it lives on the field), arrow-ability HUD feedback, and the aim ghost and landing preview (both on the field). Lucy's real-damage rule, the projectile sweep, the arrow bodies and the core fixes are not gated.

### 5. Encore in custom kits (D-316)
- Every level that overrides Linda's kit has a shorter kit (size 4 to 6) and none has Encore. Her default kit has Encore in slot 10 (index 9), past every custom kit's end, so it goes in the next free slot. The kit slot also carries animation, events and SFX. With only a preset override, the slot would inherit the default kit's slot at that index (for a size-4 kit, Dedication's animation and SFX). So this is not a small YAML edit. It goes through a one-off tool:
  - `Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTool.cs`, menu **Tools > Levels > Linda > Add Encore To Custom Kits**.
  - For each listed level, it appends a slot to Linda's kit and copies her default Encore slot into it value by value (preset, profile, animation fields and so on).
  - It skips a Linda that already has Encore, so a second run changes nothing.
  - Afterwards it warns about any other level whose Linda still lacks Encore.
- Levels the tool edits (8):

| Level | Mission | Kit before | Encore slot after |
| --- | --- | --- | --- |
| `Level1/Level1-C1-2.prefab` | M1 | 4 | 5 |
| `Level1/Level1-C1-2 1.prefab` | none (a copy) | 4 | 5 |
| `Level1/Level1-C2.prefab` | M1 | 4 | 5 |
| `Level1/Level1-C4.prefab` | none | 4 | 5 |
| `FamilyLevels/LevelLindaJohn-C2.prefab` | M3 | 5 | 6 |
| `FamilyLevels/LevelLindaJohn-C3.prefab` | none | 6 | 7 |
| `Easy/E1/LevelE1-C1.prefab` | M5 | 4 | 5 |
| `Easy/E1/LevelE1-C2.prefab` | M5 | 4 | 5 |

- **Blocked:** `FamilyLevels/LevelLindaJohn-C1.prefab` (M3, kit size 4) also lacks Encore. It is one of THJ's locally edited prefabs, so it is not in the tool's list. The tool will warn about it.
- No mission overrides kits: `Mission` has only item availability. Missions with no level override use her full default kit, which already has Encore.
- I did **not** run the tool (the editor is open), so the eight level prefabs are unchanged on disk until THJ runs it.

## How a Workshop item adds to the size, as pure data

1. Make an `EquipmentSO` (for example under `Resources/Unit Equipments/Linda/`) with `specificToUnit` = `Unit_Linda` and a socket.
2. In `UpgradeLevels[0].statsToAlter`, add one `AAttributeModifier`: `attributeRef` = `Stat_LQuiverSize`, `factor` Constant 1, `policy` Additive.
3. When the item is equipped:
   - `GUnit.ApplyEquipment` applies the modifiers to Linda's Equipment source. That source is the additive, zero-based mirror of her unit stats, and it has a `Stat_LQuiverSize` entry because her unit set does.
   - `StatResolver` folds Equipment in after Unit, so the stat reads 3 + 1 = 4.
   - The quiver picks that up at the next level start: the pips rebuild, and the HUD shows up to its 4 slots.

No code is needed. Two other routes, also data:
- Skill tree: a node whose `targetStat` is `Stat_LQuiverSize`, plus an Additive entry in `skillTree.statAttributes` with one factor per level. It counts if Linda's stat profile lists the SkillTree source.
- Run upgrade: a stat modifier on the same attribute.

`QuiverSizeTests.Read_AnEquipmentBonus_AddsToTheBase` runs exactly this evaluation path in memory.

## Mark's catch with the switch off, compared with main

Read with `git show main:miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` and `git diff main...HEAD -- .../Unit_Mark.prefab`.
- **Trigger (different from main, not changed):** main has `triggerWithQTE: 0`, so the catch is automatic. This branch has `1`, a QTE prompt ("Catch Arrow"). The QTE profile also gained `preloadOverride: 0.25` and `showSpeed: 2`.
- **The original arrow:**
  - On main it was never stopped. It flew on through Mark to its own target and hit it, so a catch gave the hit plus a bonus copy, and it could hit the enemy behind Mark.
  - On this branch it stops at Mark while the prompt is open. If the catch succeeds, it is hidden at the catch frame and disposed, never activated, when the return flight ends, so Linda's action waits for the return. A declined prompt lets it carry on along its path and land as usual.
  - Kept as the plan says ("no hit on the enemy behind Mark"). In practice, with the switch off a caught arrow no longer reaches its aimed target, unlike main.
- **The return copy:**
  - Main cloned the caught arrow's own prefab, which travels the full radius, so it could overshoot Linda and hit the enemy behind her.
  - This branch uses `LindaAttackArrowReturn`: the same damage effect, hits along its path, ends on Linda's body, and `LateUpdate` clamps it there.
  - Kept. It still damages along the way, and with the switch off no arrow goes into the quiver.
- **Catch point:**
  - Main spawned the copy at `returnSource` (Mark's hand).
  - This branch spawns it on the arrow's own path level with Mark (`CatchPointRules.FreezePoint`).
- **Timing:**
  - Main applied only when the catch animation reported `applyFrame` (3).
  - This branch applies on that frame, or after a 1 s unscaled fallback if the frame never comes.
  - Main's slow-motion was a no-op (timescale 1); this branch never changes time scale.
- **Detection:**
  - Main used Mark's trigger only.
  - This branch adds `CatchSweep` on Linda's arrows, so long frames can't skip Mark, and gives each arrow one chance.
- **Mark disabled mid-catch:**
  - Main dropped the pending copy.
  - This branch starts the return. With the switch off, after this change, it starts it while the level runs.
- **Return mode:** BounceBack, no refund, on both. The refund path only gained null guards.

## Acceptance criteria

- [ ] On a slow frame, Explosive Arrow's sprite ends on its target cell and its grounded arrow lands where it was aimed, and other projectiles look the same at normal fps: clamp done; needs THJ's play check (slow frames via `EditorFPSLimiter`). No EditMode test: extracting the clamp would mean editing a second core file (`ProjectileSweep.cs`), which the constraints rule out.
- [x] Quiver size comes from Linda's stat, base 3, with the HUD and pips matching, and a modifier that raises the stat raises the size: `QuiverSizeTests` (unit modifier and equipment bonus give 4, base 3, fallback, rounding), data tests on the stat definition and Linda's entry, and `QuiverWiringTests`. The HUD and pips at size 3 need the play check.
- [ ] Switch on, everything works as now; switch off, Linda plays as on main with no quiver UI and no errors; toggling between levels works: `QuiverSwitchTests` cover the rules (`Of` null, never empty, shots not blocked, Encore not castable, Watch zone not hidden, quiver that never woke counts as on). The rest needs the play check.
- [ ] With the switch off, Mark's catch returns a damaging copy to Linda and doesn't hit the enemy behind: the disable rule is covered by `QuiverSwitchTests.Catch_...`. The catch itself needs the play check. Differences from main are listed above.
- [ ] Every level that overrides Linda's kit has Encore: 8 of 9 after THJ runs the tool (`EncoreKitTests` checks the 8 and that their Encore slot matches the default one). `LevelLindaJohn-C1` is blocked.
- [ ] EditMode tests cover the clamp (if extractable), the gating rules, and size from the stat (including clamp on shrink), and only the known red test fails: the gating rules, the size and the resize (shrink, grow, level start) are covered; the clamp is not (see the first item). Not run: the editor is open. `EncoreKitTests` stays red until the tool has run.

## Save reset

No. The save shape is unchanged: the stat set's save is a dictionary of upgrade levels, so a new key loads fine and is ignored when missing.

## Decisions I made

- The stat id is `Stat_LQuiverSize`. It follows the unit-specific naming of `Stat_JShieldDR`. Its entry on Linda is Additive with factor 3, read from 0, so every source adds to it. Override would let her unit value wipe the Equipment bonus, because Unit is applied after Equipment.
- The size is read in `Start` and on `levelStarted`. A full quiver stays full at a new size then. Growing mid-level gives empty slots, as the plan says, but nothing triggers a mid-level read today.
- With the switch off, `Of()` returns null rather than the component being removed, so every existing "no quiver" path applies unchanged.
- Encore with the switch off is "not castable", not hidden.
- The switch is read once per Linda in `Awake`. The feasibility checks read only the stored bool, so they are worker-thread safe. A quiver that never woke (prefab checks, tests) counts as on for the checks, and its main-thread `IsActive` reads the settings lazily.
- Mark's disable rule: with the quiver on it behaves exactly as before. With it off, the level run decides, since there is no field.
- Encore goes through an editor tool, not hand-edited YAML. Without the copy, a preset-only override would inherit another ability's animation and SFX in that slot.
- The pips also warn once past their 8-pip cap, alongside the HUD warning.

## Needs THJ

1. **`LevelLindaJohn-C1` (M3) needs Encore.** Linda's kit there is the first 4 abilities. The prefab has your uncommitted local edits, so I left it alone.
   - Options: (a) after you commit or stash your edits, add its path to `EncoreKitTool.Levels` (and to the test through that list) and run the tool; (b) add it by hand in the prefab; (c) leave M3's first chunk without Encore.
   - I suggest (a): it puts the slot in the same way as the other 8.
   - Until then, the tool's end-of-run warning names it.
2. **Mark's catch differs from main even with the switch off.** It is now a QTE, and a caught arrow stops at Mark instead of also reaching its target. The plan said to report, not change. Is that the off-switch behavior you want, or should the switch also restore the automatic trigger (`triggerWithQTE`)?

## Docs to update

- `tech/core-systems.md`:
  - Projectile row: progress capped at 1 (end clamp).
  - Settings row: `lindaQuiverEnabled`.
- Quiver tech note or GDD: size comes from `Stat_LQuiverSize` (base 3); the global switch; Encore gating; the catch with the switch off.
- `build-log.md`: this step.

## Risks and loose ends

- Nothing was compiled or run here, because the editor was open. Known risks:
  - `EncoreKitTool` uses `SerializedProperty` iteration (`enumValueFlag`, `GetCorrespondingObjectFromSourceAtPath` on prefab assets).
  - `QuiverSizeTests` builds `RuntimeStatAttribute` by hand, setting `AAttribute`'s private fields through `JsonUtility`.
- `AIRegressionTest.Baseline_MatchesCurrentAI`: I could not run it, so THJ needs to check whether its known-red message changed. These changes could move it: Linda's default size 4 → 3, if the baseline reads her arrows; the new stat entry on her unit; and the kit change in the 8 levels, if the test loads any of them.
- The size is read on `levelStarted`, assuming units are initialized (stats and equipment) before that event. If some flow raises it earlier, the fallback 3 applies. That is the same value today, but an equipment bonus would be missed until the next level.
- A full quiver at level start fills to the new size. A Linda carried between levels with a partly empty quiver would keep her count. Today she is fresh each level.
- Toggling the switch mid-level does nothing until the next level, by design (read in `Awake`).
- The tool re-saves 8 level prefabs through `SaveAsPrefabAsset`. Expect some YAML reordering noise in their diffs beyond the new slot.
- `Level1-C1-2 1.prefab`, `Level1-C4` and `LevelLindaJohn-C3` aren't used by any mission. They get Encore anyway, for consistency.
- The `core-systems.md` "Move preview path" note (unused since the strip-down) is still open; not touched.

## Proposed commits

1. `fix(projectile): stop a projectile at the end of its path on a long frame`: `miso/Assets/_Project/Core/Entities/Runtime/Projectile.cs` (core)
2. `feat(settings): global switch for Linda's quiver`: `miso/Assets/_Project/Core/Managers/GlobalSettingsSO.cs` (core, additive; compiles alone)
3. `feat(linda): quiver size comes from her Quiver Size stat, base 3` (plain). Files:
   - `miso/Assets/_Project/Resources/Attributes/StatAttributes.asset`
   - `miso/Assets/_Project/Features/Player/Linda/Prefabs/Unit_Linda.prefab`
   - `.../Linda/Scripts/Quiver/QuiverSizeRules.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/LindaQuiver.Size.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/QuiverState.cs`
   - `.../Linda/Scripts/Quiver/QuiverPipsView.cs`
   - `.../Linda/Scripts/Quiver/QuiverHudFeedbackRules.cs`
   - `.../UI/Panels/Scripts/QuiverUI.cs`
   - `.../UI/Panels/Scripts/UnitPanelUI.Quiver.cs`
   - `.../Linda/Scripts/Quiver/Editor/QuiverSizeTests.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/Editor/QuiverStateTests.cs`
   - `.../Linda/Scripts/Quiver/Editor/QuiverWiringTests.cs`
   - **only the size hunks of `LindaQuiver.cs`.** That file mixes units 3 and 4. Stage this unit's part with `git apply --cached <patch>` using the patch below (checked with `git apply --cached --check`), then stage the rest of `LindaQuiver.cs` in commit 4 with a normal `git add`.
4. `feat(linda): global switch turns the quiver off; Mark's catch still returns without it` (plain). Files:
   - `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs` (rest)
   - `.../Linda/Scripts/Quiver/LindaQuiver.Switch.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/LindaQuiverSwitch.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/QuiverAbilityInfo.cs`
   - `.../Player/Mark/Scripts/CatchReturnRules.cs` + `.meta`
   - `.../Player/Mark/Scripts/ProjectileCatchAndReturn.cs`
   - `.../Linda/Scripts/Quiver/Editor/QuiverSwitchTests.cs` + `.meta`
   - Its test `Hud_WarnsOnlyWhen...` uses `HasRoomFor` from commit 3.
5. `feat(levels): Encore in every level that gives Linda a custom kit` (plain). Files:
   - `.../Linda/Scripts/Quiver/Editor/EncoreKitTool.cs` + `.meta`
   - `.../Linda/Scripts/Quiver/Editor/EncoreKitTests.cs` + `.meta`
   - the 8 level prefabs above, after THJ runs the tool.

Patch for commit 3 (`LindaQuiver.cs`, size hunks only, against HEAD):

```diff
--- a/miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs
+++ b/miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.cs
@@ -30,8 +30,8 @@
     [DisallowMultipleComponent]
     public partial class LindaQuiver : MonoBehaviour, IRoleZoneVisibility
     {
-        [Tooltip("Arrows the quiver holds. It starts every level full.")]
-        [SerializeField, Min(0)] private int size = 4;
+        [Tooltip("Arrows the quiver holds when Linda has no Quiver Size stat (see Size Stat below). It starts every level full.")]
+        [SerializeField, Min(0)] private int size = 3;
 
         [Header("Hand-back beat")]
         [Tooltip("Seconds the tossed arrow takes to fly from whoever picked it up to Linda. The beat never blocks input.")]
@@ -109,6 +109,7 @@
         private void Start()
         {
             Subscribe();
+            SyncSize();
             if (!CombatLevel.Instance) return;
             // The field hands picked-up arrows to this quiver.
             GroundedArrowField.GetOrCreate().Register(this);
@@ -142,6 +143,8 @@
         // Hardening: a level that starts without its field gets one (the field is normally made in Start).
         private void OnLevelStarted()
         {
+            // Her stats and equipment are in place by now.
+            SyncSize();
             var field = GroundedArrowField.EnsureForRunningLevel();
             if (field) field.Register(this);
         }
```

(A copy is at `C:/Users/javid/AppData/Local/Temp/claude/E--Work-Projects-miso/038223eb-f0c2-4e68-9c09-24e1fd210f68/scratchpad/split/unit3-LindaQuiver.patch`.)

## Other branches

None. The quiver exists only on `thj/linda-quiver`. The projectile clamp would also help `main` when the sweep (D-300) reaches it.

## How to see it

1. **Compile:** in the open editor press Ctrl+R and check the Console is clear.
2. **Encore tool:** run Tools > Levels > Linda > Add Encore To Custom Kits.
   - Expect "Encore added to 8 kit(s). 1 other level(s) still lack it", with a warning naming `LevelLindaJohn-C1`.
   - Look at the `git diff --stat` of the 8 level prefabs.
3. **Tests:** Window > General > Test Runner > EditMode > Run All.
   - Everything should pass except `AIRegressionTest.Baseline_MatchesCurrentAI`.
   - Note whether its failure message is the same as before.
4. **Size 3:** play a level with Linda (for example M3's second chunk, `LevelLindaJohn-C2`). The HUD quiver shows 3 arrows (no fourth), and the pips under her show 3. Shoot 3 times: the third shot leaves her empty and the bow greys.
5. **Size from the stat:** select `Unit_Linda`. Under its unit stat attributes, set the `Stat_LQuiverSize` entry's level factor to 4, then play: 4 arrows and 4 pips. Set it back to 3 (or discard the change).
6. **Slow-frame clamp:** cap the editor at a low frame rate with the FPS limiter. Fire Explosive Crescendo at a cell: the arrow sprite stops on that cell, doesn't rise past it, and its grounded arrow lies on the aimed cell. Other projectiles at normal fps look the same.
7. **Switch off:** open `Resources/GlobalSettings`, find Linda > Linda Quiver Enabled and untick it. Your other local edits in that asset stay, but don't commit it. Start a level with Linda and check:
   - no HUD quiver, no pips, no "+1";
   - shots are never blocked;
   - no arrows land on the board;
   - Encore is greyed;
   - no quiver notes in the combat log;
   - no aim ghost.
8. **Mark's catch, switch off:** in a level with Mark and Linda (Synergy unlocked), shoot through Mark and press the prompt.
   - The copy flies back to Linda and damages enemies on the way.
   - Nothing goes into a quiver, and the enemy behind Mark and behind Linda is not hit.
9. **Toggle between levels:** tick the switch back on and go to the next level. The quiver is back, full at 3.
