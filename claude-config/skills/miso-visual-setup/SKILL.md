---
name: miso-visual-setup
description: Set up or extend the visual side of a Miso GameObject — sprite import and slicing, the Visual/Body hierarchy, animation clips, blend trees and animator controllers. Use this whenever work touches a character's or object's sprites, spritesheets, animations, animator controller or visual prefab, including just adding one animation or one direction to something that already exists, and even when the request sounds like plain art or prefab work rather than animation. The conventions here keep pivots, naming and hierarchy consistent across characters; getting them wrong makes sprites jump between clips.
---

# Miso visual setup

Visual objects in Miso follow one shape: an empty parent, a `Visual` child that owns the `Animator` and `EntityAnimationHandler`, and a `Body` sprite renderer under that. Animations are spritesheets, sliced, bound to `Body`'s sprite, and gathered into per-action blend trees that pick a direction from `DirectionY`.

The point of holding to this is mechanical, not tidiness. Clips address `Body` by path, so renaming it silently breaks every clip. Pivots that differ between two sheets of the same character make it hop when the state changes. State names plus `_<Variant>` are how `SetStateVariant` finds a variant at runtime. Each convention is load-bearing in that way, and `claude-handoff/conventions.md` under "Visual and animation assets" is the record: read it first, because it is authoritative and may have moved on since this skill was written.

## Before touching anything

Most requests here are not greenfield. Work out which of these you're in:

- **Adding one animation** to an object that already has a controller, the common case. You're adding a state and its clips, nothing else.
- **Adding a direction or variant** to an existing state. You're adding clips and a blend-tree entry, or a `_<Variant>` state.
- **A new object from scratch**: hierarchy, prefab, controller, the lot.

Then read the nearest existing example rather than working from this file alone. `Features/Player/John/` is the fullest reference: it has variant states (`Idle_Shield`), an NPC controller, and feet pivots. Lucy predates some of the conventions and is a poor model, as her pivots are centered and her clips use an older name scheme.

Check what the object already has before adding: an `Animator` on `Visual`, which states exist in the controller, and whether the sheets are already imported. Assets arrive half-done more often than not.

## The conventions

Read `claude-handoff/conventions.md` under "Visual and animation assets". It carries the hierarchy, import settings, pivot rules, controller and clip naming, and the list of existing assets that break them on purpose. Don't restate it from memory and don't "fix" a listed exception.

Two are worth repeating because they are the easiest to get wrong:

- **Pivots must be identical across every sheet of one object.** A character pivots at the feet. When adding a sheet to an existing character, read the pivot off a sheet that's already imported and match it exactly; don't re-derive it from the new art.
- **Only `Up`, `Side` and `Down` exist.** Left and right are the same Side sheet flipped, via `SideVisualMode`. Don't author a Left sheet or add a fourth blend-tree entry.

## Doing the work

Unity Editor GUI work can't be driven from a session, so asset changes go through an editor script. That is the house rule in `conventions.md` anyway: non-trivial asset edits go through a script, not hand-edited YAML. Hand-editing `.meta`, `.anim` or `.controller` files means inventing GUIDs and file IDs, and it breaks in ways that only show up at runtime.

The tool lives in `Core/Animation/EntityAnimation/Editor/` and appears under `Tools/`. Read its source before using it: it is the executable half of this skill, and what it accepts tells you what the pipeline actually supports.

When the tool can't do what's needed, extend it rather than working around it once. Five one-off scripts that each slice a sheet slightly differently is how the pivot drift in this project happened. If you do extend it, say so in your report so the change gets reviewed like any other tool change.

A few things the tool can't own. They stay manual and belong in your report as such:

- **Sample rate is a judgment call**, 8 to 12 by feel. Pick one, say what you picked, and expect THJ to change it.
- **Sorting order** for a new renderer is relative to `Body` and depends on what the object looks like.
- **Which frame reads as the object at rest** for `Body`'s resting sprite. Frame 0 of the clearest sheet is the default, not a rule.

## Verifying

The editor is normally open, so confirm the work there rather than declaring it done from the file contents:

- The clip plays on the right renderer. If `Body`'s sprite doesn't change, the curve path is wrong.
- Each direction resolves. Drive `DirectionY` to -1, 0 and 1 and watch the blend tree switch.
- The object doesn't jump when the state changes. That's the pivot check, and it is the one that catches real mistakes.
- A variant falls back: with a `_<Variant>` suffix set, states that have no variant still play their plain version.

Report what you verified in the editor and what you only checked in the files. They are not the same claim.
