# Report: Ability init hardening and level id dirtying

Plan: decisions D-390 (THJ) and D-391; context `reports/hero-animation-events-noise.md`    Agent: miso-implementer    Branch: thj/onboarding (general, cherry-pick to `main`)
Outcome: done

## What changed

Unit A (core, D-390):
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs`: `Initialize` no longer appends to the serialized `animationEvents`. A private `[NonSerialized] UnityEvent _activationFrameEvent` (created once per object, listener `OnActivationFrame`) is appended to `_eventsFrameMap[abilityActivationFrame]` after the authored events of that frame (same order as before). The map is rebuilt from the authored list on each `Initialize`, so a second `Initialize` still holds the event once. `Copy()` nulls `_activationFrameEvent` (otherwise `MemberwiseClone` would share the source's callback). Unused `AddEvent(int)` removed (no caller in `Assets/`). BOM and CRLF kept.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityInitializeTests.cs` (+ `.meta`, new; BOM, CRLF like its neighbours).

Unit B (core file bugfix, D-391):
- `miso/Assets/_Project/Core/Levels/Runtime/LevelBase.cs`: `SetID` computes the id and returns before `EditorUtility.SetDirty` when it equals the current `ID`. CRLF kept.
- `miso/Assets/_Project/Core/Levels/Editor/LevelBaseSetIdTests.cs` (+ `.meta`, new; LF no BOM like `LevelLoadingTests.cs`).

## Reader audit (done before the change)

| Reader | Where | Depends on the activation event being in the serialized list? |
|---|---|---|
| `RuntimeAbility.Initialize` builds `_eventsFrameMap` | `RuntimeAbility.cs` | Only as the vehicle into the map; replaced by the direct map insert |
| `RuntimeAbility.OnAnimationFrame` | `RuntimeAbility.cs` | Reads only `_eventsFrameMap`; fires the same events in the same order |
| `RuntimeAbility.Copy()` (items) | `RuntimeAbility.cs`, called by `RuntimeItem.Copy` ← `AbilityOrchestrator.AddUsableItem` ← `FactionTracker.AddUsableItem/RestorePickedUpItems` (`DivineRelicPickUp`, `RunUpgradeTracker` relics) | No. The sources are never initialized (pickup / run-upgrade data), and the copy is initialized itself. If a source ever had been initialized, the old copy would have carried the source's callback (firing the source's activation): now it can't |
| `AddEvent(int)` | `RuntimeAbility.cs` | No callers; removed |
| `SetActivationFrame` | `RuntimeAbility.cs` | No callers |
| Sprite animator / `EntityAnimationHandler` | `AbilityOrchestrator`/`PlayAbilityAnimation` pass `OnAnimationFrame` as a callback | No: it only calls `OnAnimationFrame(frame)`; nothing registers `animationEvents` with an animator |
| Duo partners | `UnitsCooperationHandler.cs:56` (`ability.Initialize`) | No; benefits (a repeated controller init can no longer double the activation) |
| Pass-by | `UnitsPassByHandler.cs:27` (`ability.Initialize`) | No; same benefit |
| Role handlers | `FactionRoleHandlerBase.cs:107,109` full, `:98,:100` partial | No |
| `RuntimeItem.Initialize` | `RuntimeItem.cs:37` | No |
| AI (worker thread) | grep: no AI code reads `animationEvents` or `_eventsFrameMap` | No. The new code touches no Unity-object API (`UnityEvent` is a plain class) |
| Previews / editor tools | grep over all `Assets/**/*.cs`: none reads either field except the tests below | No |
| `EncoreKitTests` | `Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTests.cs:41` | Reads saved asset sizes only (Encore slot vs default slot); unaffected |
| `FactionRoleHandlerPartialInitTests` | `Abilities/Editor/` | Counts serialized sizes; still green |

## Acceptance criteria

- [x] `Initialize` stops appending to `animationEvents`; activation fires through a runtime-only event in `_eventsFrameMap` under `abilityActivationFrame`, merged after authored events: code + test.
- [x] Repeated `Initialize` idempotent (activation once): test (two full inits, exactly one non-authored event on the frame, and invoking it reaches `OnActivationFrame`, proven by its "reached its activation frame without targets" error for abilities that don't pause for target selection).
- [x] Audit first, no reader depends on the list: table above.
- [x] `AddEvent` removed (no caller).
- [x] Existing junk entries in prefabs/levels untouched.
- [x] `SetID` returns early without `SetDirty` when unchanged: test.
- [x] `Mission.OnValidate` → `AssignIDs` → `SetID` benefits for the levels. Not changed (see Risks: it dirties the Mission asset itself).
- [ ] In-game behaviour (each hero's attack, Super Time, item, Duo, pass-by): needs the verifier's play check (list below).

Tests, red before / green after (new tests run on the old code first):
- `RuntimeAbilityInitializeTests.FullInit_Twice_KeepsAnimationEventsAndHooksActivationOnce` (Linda, Lucy, John): old code red ("Linda_Ability_PrimaryAttack: animationEvents changed, expected 2 but was 4"; Lucy 1 → 3; John `John_Ability_Attack_Sword` 1 → 3). Green after.
- `LevelBaseSetIdTests.SetID_SameValueAgain_DoesNotMarkDirty`: old code red (dirty count 4 → 5). Green after. `SetID_NewValue_UpdatesIdAndMarksDirty`: green before and after (guards the changed-id path).

EditMode Run All after the change: 1360 tests, 1359 passed, 1 failed: the known `AIRegressionTest.Baseline_MatchesCurrentAI` with the same 41 failures. No console compile errors.

## Save reset

No.

## Decisions I made

- Activation event created once per ability object and reused on later inits (instead of a fresh one each time); same behaviour either way since the map is rebuilt.
- `Copy()` clears `_activationFrameEvent`: required, otherwise items copied from an initialized ability would share its callback.
- Tests read the private `animationEvents`, `_eventsFrameMap`, `abilityActivationFrame` and `targetSelectionAnimationMode` by reflection: no test hook or API change needed.
- The ability test calls `RuntimeAbility.Initialize` directly on each event-based ability of the hero copy (orchestrator abilities + role ability + Super Time), after `AbilityOrchestrator.InitializePartially` sets the owner, rather than `AbilityOrchestrator.Initialize` (that also initializes the animation handler and the role handler on a preview-scene copy).

## Needs THJ

none

## Docs to update

- `tech/core-systems.md`, Family Roles row: drop "the full `Initialize` appends to the serialized `animationEvents` list, so never call it on assets"; the full `Initialize` no longer touches serialized data (it still registers save and global stat sources, so the partial init stays the right call on assets). Ability data row: note the runtime-only activation event.
- `build-log.md`: section for this step.

## Risks and loose ends

- `Mission.OnValidate` (`Mission.cs:276-282`) calls `EditorUtility.SetDirty(this)` on the Mission asset itself, independently of `SetID`. It runs on asset load and inspector edits (not every Play), and dirties the Mission `.asset`, not the levels. Not changed, per instructions.
- `LevelBase.ID` is not serialized, so after a script recompile it is null and the first `SetID` per level still marks it dirty once. Expected; later Plays in the same session don't.
- The ability test's `Initialize` registers the copy in `SaveLoadManager` and Linda's role ability in `StatAttributeGlobalSourceRegistry` ("LindaFR") in edit mode, like the existing partial-init test does for the save manager; both are cleared by `PlayModeStaticReset` on the next Play.
- Behaviour change only in a case that was already a bug: an ability initialized more than once (for example a Duo/pass-by entry whose controller initialized twice) used to fire its activation twice per cast; now once.
- Baked junk entries in hero prefabs and level overrides stay (THJ). They remain inert.

## Proposed commits

1. `fix(abilities): an ability's activation-frame event no longer goes into its saved animation events` : `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityInitializeTests.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/RuntimeAbilityInitializeTests.cs.meta` (core)
2. `fix(levels): setting a level's unchanged id no longer marks it dirty` : `miso/Assets/_Project/Core/Levels/Runtime/LevelBase.cs`, `miso/Assets/_Project/Core/Levels/Editor/LevelBaseSetIdTests.cs`, `miso/Assets/_Project/Core/Levels/Editor/LevelBaseSetIdTests.cs.meta` (core file bugfix)

Independent of each other; either order. Do not stage the 7 Greybox prefabs, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, the TMP fallback asset or ProjectSettings.

## Other branches

`main` (cherry-pick both).

## How to see it

Play check (verifier / THJ), from a mission start:
1. Linda: basic attack hits once (one damage number, one arrow), animation finishes, turn continues.
2. Lucy: basic attack hits once.
3. John: sword attack hits once.
4. One Super Time (any hero): fires once on its activation frame; for a pause-for-targets ability, pick targets, confirm, it fires once.
5. One item (pick up a relic or use a run-upgrade relic item): activates once, uses decrement by one.
6. One Duo: both sides activate once.
7. One pass-by: triggers once.
8. After stopping Play: Hierarchy/Project show no newly dirty hero prefab or mission level prefab (no `*` on level prefabs; `git status` shows no new level or `Unit_*` diffs).

Tests: Window > General > Test Runner > EditMode, run `RuntimeAbilityInitializeTests` and `LevelBaseSetIdTests`.
