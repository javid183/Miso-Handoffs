# Report: Hint start mode (G2) and Encore empty-quiver pulse (G3)

Plan: plans/onboarding/2026-11-04-linda-memory-tuning.md (G2, G3)    Agent: implementer    Branch: thj/onboarding
Outcome: done. Compiles clean in the open editor. EditMode Run All: 1334 total, 1333 pass, only `AIRegressionTest.Baseline_MatchesCurrentAI` red. No Play mode, no level prefab/scene/asset touched, AI files untouched, no core file changed, no statics.

## Unit G2: guided hint start mode (onboarding only)
- `Features/Onboarding/GuidedAbilityHint.cs` (LF): new enum `HintStart { Turn = 0, WhenUnlocked = 1 }`, serialized `startMode` defaulting to `Turn` (value 0, so existing John/Mark data without the field stays on Turn; no data edit, no wiring change). Pure rule `ShouldShow(mode, turn, first, last, unlockSeen)`. In WhenUnlocked: turn window ignored (no turn end, first use ends it on any turn). The hint finds the level's `LevelAbilityLock` after the event bus is up and listens to `Changed`; with no lock in the level it starts at once. Unsubscribes in OnDisable. `SetStartMode`, `NotifyUnlocked`, `StartMode` for wiring and tests.
- Hint also takes the button through `AbilityButtonPulse` (see G3 non-stacking). That part makes G2's file depend on G3's component, so commit G3 first.
- `Features/Onboarding/Editor/GuidedAbilityHintTests.cs`: 2 new tests (start rule and default Turn; unlock hint ignores turn window, ends on first use). The 8 existing John/Mark-related hint tests pass unchanged. `HearthMemoryWiring.John/Mark` untouched (they call `Set`, unchanged).
- Design choice: no change to the lock. "Unlocked" = `Changed` fired (or no lock). Any unlock can start the hint, but the pulse still needs the hinted ability's button, and a locked ability has no button, so it cannot pulse early. Consequence: the hinted ability must be locked by the level for WhenUnlocked to be meaningful (if it was never locked and nothing else unlocks, it never starts).

## Unit G3: Encore pulse (general, for main; no onboarding dependency)
New files (LF, with `.meta`):
- `Features/Player/Linda/Scripts/Quiver/EncorePulseRules.cs`: pure `ShouldPulse(quiverInUse, quiverEmpty, buttonShown, buttonInteractable)`, `ScaleAt`, constants 0.15 / 1 s.
- `Features/Player/Linda/Scripts/Quiver/Editor/EncorePulseRulesTests.cs`: 4 tests (decision rule, curve, hold/stop/restore behaviour).
- `Features/UI/Panels/Scripts/AbilityButtonPulse.cs`: small component added on a button only while needed; pulses its scale, remembers rest size, restores on stop, removes itself.
- `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.EncorePulse.cs`: bar partial. `RefreshEncorePulse()` finds the Encore button (`QuiverAbilityInfo.IsRecall`) among the shown buttons, watches the shown Linda's `LindaQuiver.OnChanged` (subscribes/unsubscribes as the shown unit changes), starts/stops the pulse from the rule. No per-frame search.
Edited: `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs` (LF): `Refresh()` ends with `RefreshEncorePulse()`; `Clear()`, `OnDisable()`, `OnDestroy()` call `ClearEncorePulse()`. Populate calls Refresh, so rebuilds (unit change, G1 unlock via `Changed`) re-decide. Locked Encore has no button, so no pulse; after unlock the rebuild pulses if still empty. Greyed button (enemy turn, AP) stops it.

### Non-stacking choice
The hint and G3 both scale the same button transform, so something must arbitrate without G3 knowing onboarding. Chosen: the shared `AbilityButtonPulse` on the button. A guide calls `Hold()` (the reminder stands still, the button is put back to rest size, rest size returned) and `Release()`. The hint does this in `SetTarget`/`RestoreTarget`; works in either order (hint first, or reminder first) and the rest size is never captured mid-pulse. Alternative "G3 never runs together because the hint targets Explosive Arrow" was rejected as a trap for later data.

## Acceptance coverage
- Tested: start rule and default Turn; unlock hint turn handling; pulse decision rule; curve; hold/stop/restore; existing hint tests.
- Needs the verifier's play check: Encore pulses at an empty quiver, stops on arrow/use/unit change/enemy turn; hint (WhenUnlocked) starts on unlock; hint and reminder on the same button do not add up; John and Mark hints still show on their turns.

## Save reset
no

## What the L3 data chunk must set
- On the Linda memory level: a `LevelAbilityLock` entry (Linda + Explosive Arrow preset, and Encore if it should start locked); an unlock sequence at the right moment.
- A `GuidedAbilityHint` on that level: `ability` = Explosive Arrow preset (or whichever ability is unlocked), `startMode` = `WhenUnlocked` (set via `SetStartMode` in a wiring tool, or the inspector field "Start Mode"). `firstTurn`/`lastTurn` ignored in this mode. John/Mark need nothing.
- Encore pulse needs no data.

## Risks and loose ends
- Any unlock (not just the hinted ability's) starts a WhenUnlocked hint; harmless as explained.
- `AbilityButtonPulse` remains attached (idle, disabled never) only while pulsing or held; removed otherwise. Play check will confirm no leftover.
- Panel hide does not stop an Encore pulse (button is hidden with the panel anyway).
- Pre-existing dirty files (AI brains, `HearthMemoryLucyTests.cs`, prefabs) not touched by me.

## Proposed commits (dependency order)
1. G3, general, cherry-pick to `main`: `feat(linda): Encore button pulses while the quiver is empty`
   - `Features/Player/Linda/Scripts/Quiver/EncorePulseRules.cs` + `.meta`
   - `Features/Player/Linda/Scripts/Quiver/Editor/EncorePulseRulesTests.cs` + `.meta`
   - `Features/UI/Panels/Scripts/AbilityButtonPulse.cs` + `.meta`
   - `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.EncorePulse.cs` + `.meta`
   - `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs`
2. G2, branch only: `feat(onboarding): a guided ability hint can start when the level unlocks its ability`
   - `Features/Onboarding/GuidedAbilityHint.cs`
   - `Features/Onboarding/Editor/GuidedAbilityHintTests.cs`
   (all paths under `miso/Assets/_Project/`)

## How to see it
Play the Linda memory once L3 data lands. Quick check now: in any level with Linda, spend all arrows (Encore shown on her bar): the Encore button breathes; picking up/recalling arrows, ending the turn or selecting another unit stops it and its size returns.

## Review fixes
- `AbilityButtonPulse` is never destroyed now: when nobody wants the button it restores the scale and switches itself off; `StartPulse`/`Hold` re-enable it and read the rest size only when it was idle (so never from a half-grown button). Test added: release then re-claim in the same frame, both orders. The earlier "component removed" assertion became "component switched off".
- `GuidedAbilityHint` WhenUnlocked: starts when its own ability is no longer locked (checked on each `Changed`). If at start the level has no lock or does not lock that ability, it starts at once and logs one warning naming the hint object and the ability. Test: unlocking another ability leaves the hinted one locked.
- To support this, two small additive methods in the lock files committed with the lock: `AbilityLockSet.IsAbilityLocked(ability)` and `LevelAbilityLock.IsPresetLocked(preset)` (not core). Both files now show as modified; put them in the G3 commit (general, goes to main) so G2 builds on it:
  `Features/Levels/AbilityLock/AbilityLockSet.cs`, `Features/Levels/AbilityLock/LevelAbilityLock.cs`.
- EditMode Run All after the fixes: only `AIRegressionTest.Baseline_MatchesCurrentAI` red.
