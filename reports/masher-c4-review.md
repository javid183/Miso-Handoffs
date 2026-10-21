# masher-c4 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **FIX**

Sound: commit split and order (commit 1 is a no-op when nothing is listed); queue/pump meets every C1 constraint (retry on failed start, hold until last onComplete, frame waits, releases on turnEnded/disable/destroy; watchdog unreachable in normal flow); works with the D-106 recheck; toggle ordering (Mark and Linda checks run while the slam/walk are listed; John gets no abilityStarted); classification, cap, Crippled, step/aim match D-092 to D-100, D-112; only static is hooked in PlayModeStaticReset; no worker-thread Unity APIs.

Must fix
1. Duo partner credit (`MasherGoblinFactionRoleHandler.Counter.cs:190-209`): a partner's splash centred elsewhere leaves pending damage unclaimed and `CloseDuo` credits the earlier partner. Credit the next partner event to that partner whenever pending damage > 0, whatever its target (damage precedes the ability's own event in the same apply, `AEffectCompound.cs:156-162`); drop the `TouchesThisMasher` gate; keep the suspect fallback; comment why.

Should fix
1. Base init swap (`MasherGoblinFactionRoleHandler.cs:53-68`): works today but registers the throwaway copy in `SaveLoadManager` (`StatAttributeSet.cs:130-131`) and is fragile. Cleaner: null guard on `superTimeAbility?.Preset` in `FactionRoleHandlerBase.Initialize`/`InitializePartially` (core, THJ's OK, own commit); also fix the stale comment at `FactionRoleHandlerBase.cs:80-81`. If THJ declines, note the save side effect in the swap's comment.
2. Suppression released too early in rare cases (`Counter.cs:429`): release in the pump after the next idle settle, not in `Finish`.
3. Tether filter (`JohnTetherPresenter.cs:178-183`): use `handler.Unit.Faction == CombatLevel.Instance.PlayerFaction` instead of a closed type list.

Notes: Duo "reachable" reading is THJ's (`IsReachable` vs `slamsAfter`); enemy-turn answer may wait until the current unit's last chained action (watch in play, plus C1 (d)); suppression tests cover the registry only; `counterCanProvokeFamilyRoles` isn't serialized into the prefab yet (defaults true; expect noise on next save); preview still old until C5. Docs: core-systems Family Roles row gets `FactionRoleProvocationSuppression`; branches.md: home-test needs C1–C4.
