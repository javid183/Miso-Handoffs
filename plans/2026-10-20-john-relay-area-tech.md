# John's shield relay: any phase and area attacks (tech plan)

Size: M    Tier: 3 (core: Family Roles, Effects)    Assigned to: miso-implementer (opus)
Branch: masher-tweak (found in the Masher play check; project-wide rule, so `main` gets it on merge)
Status: waiting on THJ (J1 to J3)

## Why

In the Masher play check on 2026-10-20, John's role never relayed the Masher's slam or its answers. THJ's rules are D-119 (any phase) and D-120 (area attacks). Research: Explore, 2026-10-20. Paths are under `miso/Assets/_Project/`.

## Goal

John relays any enemy attack that would hit an ally in his zone, on either turn. For an area attack he takes the hit once and every covered ally is spared. If John himself is the main target, he relays no one.

## Findings

1. **Masher answers raise `abilityStarted` before the action is recorded** (`MasherGoblinFactionRoleHandler.Counter.cs` ~:425-430; `RuntimeAbility.cs:311`). So John sees no action in progress. The normal flow raises it inside `onStart` (`FactionControllerBase.cs:679-685`).
2. **John's phase check:** `JohnFactionRoleHandler.cs:37` requires the current phase to be an enemy's. It should check the triggering action owner's faction instead.
3. **John reads `ActionsInProgress[0]`** (:38, :67, :97, :109). That is the oldest action in progress, not necessarily the one that triggered him; he should use the triggering ability.
4. **Area attacks:** `Activate` retargets the action to John (`ModifyTargets`). For a spawner area attack (the Masher, the Goblin Queen's strike), this moves the whole area onto John, and his neighbours are still hit.
5. **Main target:** if John is the main target and allies are caught in the area, `PrepareTargets` would still relay them once area allies count. He must relay no one.
6. **Every area-damage path runs through `AEffectCompound.GetTargets`** (`AEffectCompound.cs:176-186`; Surrounding resolve :405-546). That covers the Masher and Queen slams, the Queen's charge (one compound per cell passed), and the Deev wave. The attacking ability is available there.
7. **The area is known in advance.** `AbilityPreset.ComputeAffectedCells(action, owner, targetCell)` resolves the Masher's spawner area (the same radius rule as at runtime).
8. **Side risks:**
   - each relay adds another `receivedDamageModifier` (:107), so two relays in one phase may stack John's damage reduction;
   - John's QTE (`requiredTimeScale: 0`, `PlayerController.cs:1472-1524`) sets the **player's** `PhaseData.IsInProgress` true, then false, while a Masher answer may still be running. That could re-enable input mid-answer.

## Approach

### J-A. Trigger fixes (D-119)

- In `Counter.cs`, raise `abilityStarted` inside the answer's `onStart`, before `abilityActivationStarted`. Keep the `counterCanProvokeFamilyRoles` gate.
- In `JohnFactionRoleHandler`:
  - trigger when the triggering ability's owner is an enemy of John, in any phase;
  - use the triggering ability (`obj as RuntimeAbility`), not `ActionsInProgress[0]`;
  - return false if John is a primary target.

Own commit (Family Roles, core).

### J-B. Area relay (D-120)

**Option chosen by THJ in J1.**

- **Recommended: (i-a), a per-action relay record read in `AEffectCompound.GetTargets`.**
  - John's `Activate` stores a record on the attacking ability: John, the covered allies, and a "John already hit" flag.
  - `GetTargets` swaps covered allies for John once per action and skips them afterwards. If John is naturally in the area, that natural hit is his one hit.
  - The record is cleared when the ability completes.
  - `PrepareTargets` builds the covered set from the primary targets plus `ComputeAffectedCells`, limited to allies in John's zone that match his tag query.
  - The retarget (`ModifyTargets`) stays for single-target attacks only.
  - John's one hit is the area's own effect applied to him once, so it equals the main target's amount when one damage modifier covers the area (true for the Masher and the Queen). John's DR +0.5 still applies.
  - Files: `AEffectCompound.cs` and `RuntimeAbility.cs` (core) or a small static registry, plus `JohnFactionRoleHandler.cs`. It does nothing when no record is set. It also covers the Queen's charge and future area attacks with no data edits.
- **Alternative: (i-b), no core effect code.** A temporary "Relayed" tag on covered allies, which every enemy damage effect's tag query must exclude (data edits on every enemy damage asset), plus the handler re-applying the area damage to John. It's fragile: new attacks can forget the filter, and the tag is global, not per action.

### J-C. Side risks

- **Damage reduction stacking** (J2): apply John's reduction once per action. Recommended.
- **The QTE flipping the player's in-progress flag during an enemy answer** (J3): guard it in `PlayerController` so it doesn't release input while another faction's action is running. This is core. Recommended, as its own commit.

## Questions for THJ

- **J1.** Area relay: (i-a) per-action record in `AEffectCompound` (core, recommended), or (i-b) tag plus data filters.
- **J2.** One reduction per action, not stacking across relays in the same phase? Recommended: yes.
- **J3.** Fix the QTE input-flag risk now, in `PlayerController` (core, own commit)? Recommended: yes, since Masher answers now run on the player's turn.

## Acceptance criteria

- [ ] John relays a Masher answer on the player's turn and on the enemy turn, when its target is an ally in his zone.
- [ ] Masher or Queen slam on an ally in John's zone: John takes one hit at his reduction; covered allies in his zone take nothing; allies outside his zone are hit; John's neighbours are not hit because of the relay.
- [ ] John as the main target: he takes his normal damage; nobody is relayed.
- [ ] Single-target attacks relay as today.
- [ ] Two relays in one phase don't stack the reduction (if J2).
- [ ] EditMode green except the known red; new tests for any pure logic (covered-set selection, record lifecycle).

## Gates

Compile / EditMode / reviewer (core) / play check (THJ): items 15 to 23 of `playtests/2026-10-20-masher-play-check.md`, plus a Goblin Queen strike near John (M4 or M10).

## Commit log

(filled as chunks land)
