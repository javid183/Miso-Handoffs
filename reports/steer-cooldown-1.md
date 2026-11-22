# Report: Steer cooldown 1

Plan: none (size S, D-601)    Agent: implementer    Branch: main
Outcome: done

## What changed

- Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs: SteerCooldown = 1; comments and the setup message now say one-turn cooldown.
- Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSteer.cs: comment says one-turn cooldown.
- Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs: test renamed to LiveSteer_CostsOneAP_HasAOneTurnCooldown_FirstIsNotFree_AndIsSeparateFromTheCast; expects cooldown 1 ("one Steer a turn"); runtime check now expects RemainingCooldown 1 after SetCoolDown, then ResetCooldown so the later steps are unchanged.
- Asset untouched. Files are LF; endings kept.

## Acceptance criteria

- [x] Code agrees with cooldown 1: setup constant, comments, test.
- [x] Gate: batch run of MISO.Core.Features.Bergsons.EditorTests: 900/900 passed, 0 failed, no `error CS`.

## Decisions I made

- CycloneSteerTests.Command.cs line 255 ("her Steer gets no cooldown") left alone: it asserts Mark's Command puts no cooldown on her Steer, still true.

## Save reset

no

## Proposed commit

fix(lucy): the Steer's setup tool, comments and test now agree it has a one-turn cooldown
