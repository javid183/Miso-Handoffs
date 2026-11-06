# R1 `CastAbilitySequence` review (miso-reviewer, 2026-11-05)

**FIX.** Scope, namespace, LF/no BOM, no statics, no core, no IDs: OK.

Must fix:
1. Event order (`CastAbilitySequence.cs:101-111`): copies Mark's passive; the player path raises `abilityStarted` in `onStart` (after `SessionLogs.RecordAction`, `RuntimeAbility.cs:319`) and `abilityActivationStarted` in `onActivation` (`FactionControllerBase.cs:721-727`; Masher counter `:423-432`). As written, John's role (OnActionStart) reads stale `LastActions`; camera/HP snapshot fire at cast start.
2. An exception inside the synchronous invoke/activate kills `PlaySequence` and `Sequence.Play` never ends (`Sequence.cs:29`): try/catch, log, `yield break`.

Should fix:
1. Target always the `GridCell`: map the target like the player path (`FactionControllerBase.cs:574-588, 703-718`; Masher `AbilityTargetFrom` `Counter.cs:458-466`) or validate (Cell + Targeted) in `TryResolve`, with a test.
2. `FindUnit` accepts dead/downed units; warn on duplicate nicknames.
3. Tests: add a successful resolve; exercise the real lookup or say why not.
4. Optional `canProvokeFamilyRoles` (default on), as the Masher counter does.

Notes: event set right; ATB fill on the ATB branch; cooldown only on the animation event (timeout leaves the ability half-active); fpFill granted; lookup order abilities → items → role (abilities win); casts through `LevelAbilityLock` (wanted). AI never reads it.

## Re-review after fixes (2026-11-05)

**R1 APPROVE** (all six fixed; no compile errors found by reading). Optional: use `FactionRoleProvocationSuppression.Suppress/Release` (public API, not a core edit) when the toggle is off, for generality; not needed for M4 (Mark's role needs an enemy action, Linda's an enemy in lane; John is covered by the toggle). R3: set `canProvokeFamilyRoles = false` on the opening cast; check the grid doesn't react to hover mid-cutscene.

**R2 APPROVE** (not yet run): effects single-document, references overwritten; variant pattern as the Trail tool; idempotent by design. Test fixes requested: shared refs intact, variant check, null assert. Fires-every-turn timing vs `TurnNumber` to the play check.
