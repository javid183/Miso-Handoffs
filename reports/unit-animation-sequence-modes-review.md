# Review: `UnitAnimationSequence` modes (2026-11-06)

Reviewer verdict: **FIX**. Read from the code and data; nothing run. The reviewer can't write files, so the coordinator saved this condensed copy.

## Must fix

1. `ModeWaitsForClip` and `ModeNeedsAnimationName` (`UnitAnimationSequence.cs:57`, `:60`) are only called by tests; `PlaySequence` (`:100`, `:112`, `:124`) and `IsStopMode` (`:54`) branch on their own checks, so those tests can't fail when behavior changes. Runtime must use the helpers.

## Should fix

1. `OnceNoWait` can act on the previous play of the same state (`:164`, `:189-198`): a stale `normalizedTime >= 1` stops the new play at once, and a replay of the same state during the poll gets stopped after one cycle. Fix: `yield return null` before the loop; exit if `normalizedTime` drops below the last value. Latent: no asset uses `OnceNoWait` yet.
2. Both John assets look hand-written (field order doesn't match the class; BackToIdle's GUID looks typed). Reimport and force-reserialize before commit.

## Notes

- John on `Loop` rather than `HoldLastFrame`: the reason checks out (all three `APTransfer` clips are Loop Time; `EntityAnimationHandler.cs:126` only freezes non-looping clips). The implementer's "the visible result is the same" is wrong: the clips last about 0.64 s, so the gesture restarts about every 0.64 s through the line. `HoldLastFrame` criterion unmet for Loop Time clips.
- Extra option, not in the implementer's report: `FollowUp` can freeze a looping clip with no core code change, by waiting for the last frame and setting `animator.speed = 0` on the Animator; `Play` (`:224`) and `Stop` (`:306`) restore the speed. It writes to the Animator around the handler, so it needs THJ's OK. `Pause` was rightly rejected.
- Skip can't leave John looping: no script calls `SkipStep` or `ForceStop`; `SequentialSequence.cs:38-52` only drops dialog and camera entries, so BackToIdle always runs. Plan's skip risk closed for the Bloom.
- Boss intro: path unchanged, asset unchanged. Only difference is the living-only lookup (a sequence played before `PrepareUnits` now logs "not found"; nothing does this today). No asset references it, so it can't be play-checked without temporary wiring.
- Checked with no findings: Bloom list order, John's GUID, no renames, `FollowUp` is static with no asset state, each mode's ending, no statics or private IDs, LF kept, no AI impact, no core diff.

## Add to the play check

- Run the cut-in several times: `AutoSelectUnit` (`PlayerController.cs:479`) picks at random and `GUnit.SetSelected` (`:936`) plays John's `Switch`; with pending enemy intros selection is deferred (`PlayerController.cs:225-243`) and could cut the gesture.
- John stays facing Up in idle after BackToIdle until he moves or acts.

## For the Mark test update later

The known red `TheBloomCutInPlays...` also asserts the old line "Lucy! Keep them in their hole!" (`HearthMemoryMarkTests.Flow.cs:212`).
