# Review: merge main into thj/home-test (2026-10-26)

Reviewer: miso-reviewer (read-only, so the coordinator saved this file). Verdict: **ESCALATE**. The merge itself is clean; one gameplay question goes to THJ.

## Must fix / Should fix
None.

## Escalate (THJ)
- Main's `EnemyAlertTracker` lives on `LevelBase.prefab`, so it now runs in all 21 Home sortie levels (`Content/Home/Sorties/Levels/**`). None of them has a `LevelAlertSettings`, so their enemies start Unaware and skip turns until they see the family, hear noise, or take damage. Only Queen, Deev and enemy Toba are exempt (`EnemyAlertSettings`).
- Main set `allEnemiesStartAlert` on 11 levels, including `LevelM2-C1`. Home-test's copy, `Goblin Queens Warren/LevelM2-C1 1.prefab`, doesn't have it.
- Options:
  - (a) accept the stealth openings;
  - (b) a separate commit adds `LevelAlertSettings` to some or all sortie levels;
  - (c) choose level by level.
- This doesn't block the merge commit.

## Checked, sound
- **The six conflict files** match the plan (D-181) and the event-bus reorder (D-198).
- **Line endings:** all LF.
- **BOMs** kept in `GlobalEventBus`, `FactionRoleHandlerBase` and `CheatHandler`.
- **Conflict markers:** none left.
- **The 15 files changed on both sides that merged automatically** keep both sides' changes. Prefabs and scene have no duplicate fileIDs or override targets. The scene differs from home-test only by the 4-line Cabinet collider fix. Both package files are valid JSON.
- **Index:** nothing extra staged; THJ's three edits are unstaged.
- **Statics:** every new static from main has a play-mode reset (`IdlePhaseSequence`, `FamilyRoleRelay`, `FactionRoleProvocationSuppression`, `CameraEffectBase`).
- **`HomeFiresidePayoff.SpendRole`** still fires.
- **Omen and From-Home hooks** run before `levelStarted`.
- **From-Home banner:** no overlap with the first-turn banner.
- **Tests:** 1138 of 1139 passed; only `Baseline_MatchesCurrentAI` fails (the known red).

## Notes
- **`GTagRegistry.asset`:** its cached copy has gone stale (pre-existing). Unity rebuilds it on load. If Unity rewrites the file, the rewrite goes in the tag-fix commit (D-198).
- **Markers:** `HomeInteractables.RefreshLock` and `HomeStationProp.LateUpdate` both drive them. Check in play.
- **Private IDs left in shared code** (pre-existing): `FactionControllerBase.cs` ("M9 Step 6c") and `HomeFromHomeTags.cs` lines 56–57. Leave them for a later cleanup.

## Play checks for THJ
1. **A sortie:**
   - Do enemies start Unaware, and is that wanted? Check `LevelM2-C1 1` and the Warren.
   - Does the Queen's Chamber start alert?
   - Do Omen removals leave the alert state looking right?
2. **Home scene:**
   - Hover the props of a room that isn't open yet, and open and close the map. Markers must not flicker.
   - The Workshop Cabinet click works.
3. **A Masher level:**
   - the From-Home banner and Omen tags;
   - the turn-start pause;
   - the banner input lock;
   - role decline barks and zones (Shift);
   - the Masher counter.
4. **Losing a Home attempt:** "Returning home..." and "Retreat home".
5. **Cheat keys:** F12 and numpad6 both complete the objective.
6. **After Ctrl+R:** run `git status` and look for a `GTagRegistry.asset` rewrite.
