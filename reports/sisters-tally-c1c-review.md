# Sisters' tally C1c (Tempest Bloom): review

Reviewer: `miso-reviewer` (read-only; saved here by the coordinator). Date: 2026-11-08. Branch: `thj/onboarding`.

**Verdict: APPROVE.** No must-fix. Two test should-fixes.

## Should fix

1. `Editor/SistersTallyTests.Bloom.cs:89-97` `Bloom_LindasNormalKillAndLucysFinisherStayTheirs` never raises a Bloom (passes on HEAD too). Run the kills after a window opened and closed (`StartAction(); RaiseBloom(); StartAction();`), or give Lucy's finisher a kill not remembered while a window is open.
2. Missing test: Lucy's report claiming a remembered death (`RaiseBloom(); Die(_goblin); Assert.IsTrue(Kill(_lucy, _goblin)); 1-1`) to pin the "any sister" rule at `SistersTallyListener.cs:197`.

## Notes (verified)

- Bloom mechanics confirmed: `LucyCycloneProjectileScatter.cs:16-39` whitelists only `LindaAttackArrow`, `LindaAttackFireArrow` (fire arrow only from the Linda–Lucy Duo spawn); `Projectile.GetClone` (`:124-132`) keeps owner and firing ability; `RaiseSynergy(..., "Tempest Bloom", ..., null)` names Lucy, after the copies spawn. Damage before `onAbilityEffectPerformedOn` (`AEffectCompound.cs:161-167`), `unitDied` synchronous (`GUnit.cs:774`), flush on the firing ability's `abilityPerformed` (`CombatLevelRunHandler` 761-774 → 812-835): death always precedes the report for buffered hits.
- Late-copy limit confirmed core (`AEffectSpawner.cs:90-91` clears in-progress at the split): a copy landing after `abilityPerformed` counts for no one.
- Window edges: kill before the split stays Linda's; later actions close the window (`FactionControllerBase:726`, both sisters' role handlers, Masher counter, Mark/John passives raise `abilityActivationStarted`); Lucy's finisher stays hers; John's role ability raises neither event (counts nothing); stale entries can't be claimed; `Resurrect`/`Revive` clear them.
- Bloom inside a Duo: no double count (`RecordDeath` first → `_countedForBoth`; Duo trigger report dropped before conversion).
- Accepted edges: Linda-damaged enemy finished by something else inside the window now counts for both; a second activation of the firing ability closes the window early.
- Only new static: `private static readonly string[] BothSisters` (constant, no reset needed). Subscriptions symmetric; `ForgetLevel` clears Bloom fields; guards in place; no core edits; no private IDs; LF.
- Report says 15 tests; the file has 14 (total 1695 matches 14).
- Combined C1b + C1c commit agreed; **9 files**: `SistersTally.cs`, `SistersTallySource.cs`, `SistersTallyListener.cs`, `Editor/SistersTallyTests.cs`, `Editor/SistersTallyTests.Attribution.cs` (+ `.meta`), `Editor/SistersTallyTests.Bloom.cs` (+ `.meta`), `Content/Levels/LevelBase.prefab`.
- Play check still needed: a Bloom copy's kill moves both by 1, Linda not by 2.
