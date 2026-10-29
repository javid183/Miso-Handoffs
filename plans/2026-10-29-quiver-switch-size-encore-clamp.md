# Quiver switch, size as a stat (3), Encore in custom kits, projectile end clamp

Size: M    Tier: 3, approved by THJ 2026-10-29 (D-314 to D-317, D-319)    Assigned to: miso-implementer (opus), miso-reviewer; THJ plays
Branch: all, built on `thj/linda-quiver` (HEAD `3482eedf5`)

## Changes

1. **Projectile end clamp** (core, D-317, its own commit).
   - In `Core/Entities/Runtime/Projectile.cs` `Update` (around lines 376-391), clamp `_progressTracker` to 1.
   - Why: on a long frame progress went past 1, so the sprite overshot its target (and rose, since the `verticalFactorCurve` post-infinity loops). Linda's `QuiverArrow` (EndOfFlight landing) then grounded the arrow under that wrong spot.
   - Check that:
     - reaching progress 1 still activates exactly once;
     - the sweep (`TargetReachAndHit`) still covers the last segment;
     - nothing reads progress beyond 1;
     - Mark's catch freeze/resume (`Projectile.enabled = false`) still works.
2. **Global quiver switch** (D-314).
   - Add `lindaQuiverEnabled` (bool, default **true** in code, with a tooltip) to `Core/Managers/GlobalSettingsSO.cs`. It's an additive core settings field, so it gets its own commit, unless it can't compile without change 4. In that case, say so.
   - **Don't edit `Resources/GlobalSettings.asset`.** It holds THJ's uncommitted local edits, and the code default applies.
3. **Quiver size as a stat** (D-319). Linda's quiver size comes from a stat attribute on Linda, so the skill tree, Workshop equipment and run upgrades can modify it with the existing attribute modifiers.
   - **The stat:** a new attribute, say "Quiver Size", with base **3** on Linda (D-316). Find how stat attributes are defined and registered (`Core/Systems/StatsResourcesSystem/`: `StatAttributeSet`, `AAttributeRegistry`, and how Linda's existing stats are set up) and add it as data the same way.
   - **If code is required:** if a new attribute needs a code change (an enum or a hard-coded list), that's core. STOP on this point, keep the serialized `size` = 3 for now, and report what it would take.
   - **Reading it:**
     - `LindaQuiver` reads the stat at level start, and when it changes if the attribute set raises a change event.
     - If the stat is missing, fall back to the serialized `size`.
     - When the size shrinks below the current count, clamp the count; when it grows, the new slots start empty.
   - **The view:**
     - The HUD prefab has 4 arrow slots; at size 3 the extra slot stays hidden.
     - If the size ever goes past the slot count, show as many as fit and log a warning once.
     - The pips follow the size: rebuild them when it changes, since they are built once today.
   - **Tests:** fix any that hard-code 4 when they aren't testing a rule.
   - **Not now:** no Workshop item. In the report, explain how one would be added as pure data.
4. **Gate the quiver on the switch.** With the switch **off**, Linda plays as on `main`:
   - no arrow spending and no blocked shots at 0;
   - no grounded arrows or pickups;
   - no HUD quiver, pips or "+1" cues;
   - no quiver log suffixes;
   - Encore not available (hidden from the bar or not castable, whichever is cleanest; say which);
   - no kill hand-back;
   - no arrow-ability HUD feedback;
   - no aim ghost or landing preview from the quiver.

   Mark's catch with the switch off (D-315): it stays as it was before the quiver. The return copy flies back to Linda and damages along the way, and no arrow goes into the quiver.
   - Keep this branch's fixes against hitting the enemy behind Mark or Linda.
   - Compare with `main`'s catch (`git show main:<files>`) and report every remaining difference (QTE or automatic, timing, catch point). If the trigger differs from `main`, report it; don't change it.

   These stay on whatever the switch says: Lucy's real-damage rule, the projectile sweep, the arrow bodies, and the core fixes. Toggling the switch between levels must work (domain reload is off).
5. **Encore in custom kits** (D-316). Find every level or mission that overrides Linda's ability kit and lacks Encore (`Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset`), and add it in the same slot as in her default kit, or the next free one.
   - List every changed level.
   - With the switch off, Encore isn't usable there either.

## Acceptance

- [ ] On a slow frame, Explosive Arrow's sprite ends on its target cell and the grounded arrow lands where it was aimed. Other projectiles look the same at normal fps.
- [ ] Quiver size comes from Linda's stat, base 3, with the HUD and pips matching. A modifier that raises the stat raises the size (tested).
- [ ] With the switch on, everything works as now. With it off, Linda plays as on `main`, with no quiver UI and no errors. Toggling between levels works.
- [ ] With the switch off, Mark's catch returns a damaging copy to Linda and doesn't hit the enemy behind. Differences from `main` are listed.
- [ ] Every level that overrides Linda's kit has Encore.
- [ ] EditMode tests cover the clamp (if extractable), the gating rules, and size from the stat (including clamp on shrink). Only the known red test fails.

## Constraints

- **Core:** only `Projectile.cs` and `GlobalSettingsSO.cs`, each minimal. Everything else goes in the quiver folder or in data. A new stat attribute that is data only is fine; one that needs code means STOP.
- **Hands off:**
  - the AI diagnostic: `AIFactionBrain.cs`, `AIUnitBrain.cs`;
  - THJ's local edits: `GlobalSettings.asset`, `John_Ability_Attack_Dash.asset`, `PreloadScreen.unity`, the `LevelLucyJohn-C1`/`C2`, `LevelLindaJohn-C1` and `LevelE2-C1` prefabs, `EditorFPSLimiter.cs`, ProjectSettings, the TMP fallback;
  - if a level needed for change 5 is one of THJ's locally edited prefabs, STOP and report it.
- No statics without a reset hook. Keep line endings and BOM. No private IDs.
- Don't touch the AI regression test, but confirm its known-red message is unchanged. A new stat or a kit change could move it; if it does, report it.
- **The editor is open:** no batch Unity.

## Commit units

1. Projectile clamp (core).
2. GlobalSettings field (core, additive).
3. Quiver size as a stat (3).
4. Quiver gating and the catch fallback.
5. Encore in custom kits.

## Commit log

(empty)
