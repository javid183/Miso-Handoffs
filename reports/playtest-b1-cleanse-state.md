# Report: Playtest Batch 1, C1 (B1 data fix: Mark Cleanse state)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md    Agent: miso-implementer    Branch: thj/oct-build-fixes
Outcome: done (play check pending)

## What changed

- miso/Assets/_Project/Features/Player/Mark/Arts/Animations/AC_Playable_Mark.controller: added state `SoulSacrifice` (placeholder for Mark's Cleanse) with a 3-child blend tree on DirectionY, a copy of John's setup. All three children use John's clip `John-SoulSacrifice-Side.anim` (guid 360bff75c28b0d340ba35676148f8248). The state is registered in the Base Layer's child states. 68 lines were appended or inserted, and nothing existing was touched. LF endings kept.
- `Unit_Mark.prefab`: NOT changed. `abilities[4]` already has stateName `SoulSacrifice` and abilityActivationFrame 5, and that frame fits the clip. John's slot 5 uses the same frame 5 with the same clip (15 frames at 10 fps, 1.5 s, no animation events).

## Acceptance criteria

- [x] Mark's animator has a Cleanse state copied from John's matching motion: verified through the Unity editor API (state `SoulSacrifice`, motion blend tree `SoulSacrifice` present).
- [x] Prefab slot 4 points at it with a fitting activation frame: slot 4 is state=SoulSacrifice, frame=5, and that state exists in the controller.
- [ ] Cleanse resolves in-game and the tile clears: needs the play check (In My Father's Arms). Not run.
- Safety net, B3, B6 and B8 belong to later chunks and were not done.

## Save reset

no

## Decisions I made

- Kept the state name `SoulSacrifice` rather than a new name. It matches John's prefab and needs no prefab edit. The placeholder status is flagged by the blend tree and this report, not by the name. To swap in Mark's own motion, replace the three child clips of blend tree `SoulSacrifice` in `AC_Playable_Mark`, or rename the state and the prefab stateName together.
- Reused John's clip asset directly (no copy, no new .meta). It animates a SpriteRenderer sprite on path `Body`, which is the same binding Mark's clips use, so it works on Mark's rig. It will show John's sprites on Mark until replaced.
- Mark's own `Arts/Animations/Soul Sacrifice/` folder (SoulSacrifice-Side/Up Start/Loop/End.anim) already exists and is unused by this controller. It may be what THJ wants for the real animation, which is his call.
- Fileids for the new objects are hand-picked (7700000000000000001 and ...002) and unique in the file.

## Needs THJ

none

## Docs to update

- build-log.md: coordinator, at the end of the batch.

## Risks and loose ends

- Mark will play John's Soul Sacrifice sprites for Cleanse until you swap the motion.
- Other Mark ability slots with a stateName missing from the controller (list only): abilities[5], [6] and [7] have an empty stateName (no state to play). They look like unused slots on the base prefab. Slots 0 to 4 are all present (PrimaryAttack, Run, Vault, Command, SoulSacrifice). I did not check Mark's `items[].ability` slots (Unit_Mark items [0] and [1] override stateName), so that is not covered.
- If the empty-stateName slots 5 to 7 ever get used, they hit the same freeze. The C2 safety net should cover that.

## Proposed commits

1. fix: add placeholder SoulSacrifice (Cleanse) state to Mark's animator: miso/Assets/_Project/Features/Player/Mark/Arts/Animations/AC_Playable_Mark.controller (plain; no .meta change, the controller's guid is unchanged)

## Other branches

thj/home-test, on its next merge of main.

## How to see it

1. Open `AC_Playable_Mark` in the Animator window: a `SoulSacrifice` state sits at the right of the Base Layer.
2. Play *In My Father's Arms*, select Mark, cast Cleanse on the corrupted tile. It should play John's animation, resolve, and clear the tile. Combat should not freeze.

Verification done: the editor was refreshed, and the console had 0 errors (filter ["error"]). The controller and prefab were inspected via editor code (list above).
Not verified: play behaviour, EditMode suite (no code changed).
