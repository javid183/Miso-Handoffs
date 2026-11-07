# Review: Bond Lite fix C3, station pages on unlock (2026-11-07)

Reviewer verdict: **APPROVE**, no must-fix. Read from the code; nothing played. Coordinator's condensed copy.

## Should fix
1. `HomeVisitsWiring.cs` class summary still says only the Workshop page; say "station pages". (Coordinator: fold into C4's run, not while THJ plays.)
2. Commits: two, not three. (1) runtime `HomeManager.StationPages.cs`, `HomeInteractables.PageOnUnlock.cs`, `HomeStationPageRules.cs` + `HomeStationPageRulesTests`, own commit (every Home load). (2) setup + data + `HomeVisitsTests.StationPages.cs` together (drift test proves they only work together).

## Verified
- No flagged station: unchanged opening (empty list exits; only idempotent `RefreshLock()` added). Classic: field defaults 0, restored scene lacks it.
- Guard holds until pages finish; exceptions in find/focus/Play caught; replayable page skipped with warning; remaining hole: exception inside a page's own coroutine (known opening limit).
- Once per save shared with the click path (`SequencePlayer.cs:21`), distinct page names tested.
- Input re-lock correct; line 156 restores mode All as before.
- GuidedSkillSpend, Hearth close, Yard chain unaffected.
- Scene diff: six `playPageOnUnlock` lines + Grandma Table page GUID. Text matches. No statics, no private IDs, CRLF+BOM like neighbours. `CameraHandler` (core) only called.

## Play-check watch points
- Unplanned zoom: `Focus` before `cameraHandler.Initialize()` with `_targetZoom` still 0, so the first focus zooms in, stays zoomed until `Initialize()` tweens back. If the intro animator still drives ortho size, framing may be off-centre. Probably also true of existing pre-Initialize `CameraSequence` focuses. A fix would be in `CameraHandler` (core, THJ's OK) or an explicit focus-and-zoom.
- Ease-back may still end in a snap: `Initialize()` sets position to `initialLocator`. If seen, drop the ease-back or aim at `initialLocator`.
- Old saves with a station open and its page unseen get it on the next load (intended).

## Docs
`tech/classic-fallback.md` W3 (scene carries `playPageOnUnlock` + Grandma page), `tech/home-system.md` (new opening step).
