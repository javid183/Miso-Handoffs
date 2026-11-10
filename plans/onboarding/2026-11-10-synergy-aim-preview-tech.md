# Synergy aim preview (tech plan, build chunk 7)

Size: L    Tier: 3 decided (D-467)    Assigned to: miso-implementer (opus)
Branch: `thj/after-hearth` (scope **all**)
Status: approved (D-486), queued after the Hearth memories

## Why

D-467: when the player's aim would set off a Synergy, the preview shows where the copies go and what they hit (Tempest Bloom, Shield Flare, Catch & Return), no caption. Critics: a new player won't fire at an ally without seeing the outcome. Code facts: [`reports/after-hearth-tech-explore.md`](../../reports/after-hearth-tech-explore.md) §B.

## Goal

While aiming, each Synergy shows its copies' lanes and the usual damage preview on whatever they hit, using the same rules as the real shot.

## Decisions

- **Coordinator (Tier 2): a non-core preview presenter, no core change.** The only existing hook (`IProjectilePreviewRedirect`, core) keys on the aim cell's occupant: it fits Flare, not Bloom (Cyclone mid-lane) or Catch (Mark mid-lane). Extending core preview code (`Projectile.CollectPreviewPathHits`, `AbilityDamagePreview`, `PlayerController`) would be Tier 3; a presenter in the feature folders, modelled on `QuiverAimPresenter`, reads `PlayerController`'s public getters, draws lanes and calls `GUnit.ShowDamagePreview` (core, called only) for copy hits. If the presenter can't clear or merge its damage previews cleanly with `PlayerController`'s, stop and report (that would be a core question for THJ).
- **One geometry source per Synergy**, shared by the real shot and the preview, so they can't disagree: Flare already has `JohnShieldRelay.TryCollectCopyTargetCells`; Bloom and Catch get pure static helpers extracted from `LucyCycloneProjectileScatter.OnTriggerEnter2D` and `ProjectileCatchAndReturn` (`IsOnIncomingPath`, `minTileDistance`, return lane Mark → Linda), with the runtime code calling them.

## Chunks

### C1 · Shared lane drawing + Shield Flare lanes (riskiest first: the presenter and its preview lifecycle)

- A lane presenter (LineRenderer pool, like `QuiverAimPresenter.DrawLines`): shows/hides with the aim; cleared on cancel, ability switch, turn end, level end.
- Flare: when Lucy's aim targets a shielded John, draw each copy's lane from John's cell to its target cell (from `TryCollectCopyTargetCells`). Damage on the copies' targets already works (commit `4e2ac96f0`); keep it.
- Tests: lane endpoints from the shared helper for a few layouts.

### C2 · Tempest Bloom

- Extract the scatter geometry (adjacent cells except back the way it came, each copy running the arrow's radius from the Cyclone cell, Bond unlock check) into a pure helper; the trigger calls it.
- Preview: when Linda's lane enters a Cyclone (and the Bloom is unlocked), the lane stops at the Cyclone and continues as the copies' lanes; damage preview on what each copy reaches, with the same falloff/reach rules as the bow (CR-37).
- Tests: helper geometry (directions, radius, blocked cells).

### C3 · Catch & Return

- Extract a pure "would Mark catch this" check (ally, unlock, distance ≥ 2, on the incoming path) and the return lane.
- Preview: when Linda's lane passes Mark and the catch would trigger, draw the return lane from Mark back toward Linda and preview damage on what it hits. The QTE still decides in play; the preview shows the success case (no text).
- Tests: helper gates and lane.

Acceptance (all chunks):
1. Each Synergy's preview appears only when the real shot would trigger it (locks, Bond unlock, shield up, distance), and its lanes/targets match where the real copies go (play check: aim, fire, compare).
2. Damage previews on copy targets use the normal bars/skull; nothing previews damage on John or Mark.
3. Previews clear on cancel, ability switch, end turn and level end; no leftover lines.
4. No core file edited; EditMode only the known AI red.

## Risks

- **Preview/real mismatch:** solved by shared helpers; any runtime code extracted keeps behaviour (tests before/after).
- **Damage-preview ownership:** `PlayerController.HideDamagePreviews` clears only its own units; the presenter must clear its own.
- **Linda's bow has no lane drawn today** (Direction mode): only the Synergy part of the lane is new; whether to draw her base lane too is out of scope (flag if the copies look detached without it).
- **AI worker thread:** helpers pure, no Unity-object APIs if the AI ever reads them.
- **Prefab/scene edits:** the presenter object placed by an editor menu item (precedent: tally counter).
- Other branches: `main` on merge.

## Gates

Compile / EditMode / review per chunk / THJ play check per chunk / docs: GDD `combat-rules.md` new preview rule beside CR-37 and a pointer in `family-systems.md` (designer), `tech/combat-architecture.md` (coordinator).

## Proposed commits

One per chunk; each runtime extraction in the same commit as its preview (they only work together), tests with it.
