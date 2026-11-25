# Review: duo panel videos (C1) and card-first duo order (C2), `thj/onboarding-demo`, uncommitted

Reviewer: miso-reviewer, 2026-11-24 (saved by the coordinator; the reviewer is read-only).

**Verdict: APPROVE** (should-fixes sent back before the commit)

## Must fix (commit grouping)
- `FTPPanel.prefab` references the four clips by GUID; the `.mp4` + metas are untracked. Committing C1 without them leaves missing references (panels silently show the still art) and drops Mark's trim. Commit the clips with C1 or hold C1 (THJ).

## Should fix
1. `FamilyRoleVideoPanel`: after the 2 s timeout or an error, `prepareCompleted` stays subscribed and a late prepare still calls `Play()` (decodes unseen). Return early in `OnPrepared` when failed; unsubscribe and `Stop()` on both failure paths.
2. `FamilyRoleVideoPanel`: `sendFrameReadyEvents` stays on for the whole playback (per-frame callback × 4). Turn it off after the first frame; back on before `Prepare()`.
3. `DuoInsertSequence.mode`: tooltip saying `Off` also switches off the card-first flow and `Full`/`ShortAfterFirst` only matter with `playComicInsert`.
4. Card title: use `entry?.caption ?? triggerPreset?.Title` (shipped: "Hide and Seek", "Marks‑Sisters" (U+2011, check the TMP glyph), "Healing Marks", "Chained Assault", "Family Watchers"); not the `iD`.

## Notes
- Deviation from the plan: the sprite and `FR BG` hide as soon as the panel turns on; the sprite comes back only on failure or after 2 s, longer than the panel hold (~0.58 s): a slow prepare (first load of Mark's re-encoded clip) shows a blank panel.
- Mark.mp4.meta: frame range 3–98, transcode on (needed for the trim). `importAudio: 1` on all four clips is unused.
- Masks: import settings fine; leftover `spriteMode: 2` entries harmless. Shader UI/Default-compatible; mask uses the video UVs.
- Panel animations only touch `m_IsActive` and anchored position; no conflict.
- C2: old paths untouched (no QTE, Off, no/inactive sequence); card path stored factor via `CoopQteFactor.Raw`, `onSuccessfulQTE` on success only, shared same-entity spread; timeScale restored on all exits; pooled button returned; unstartable QTE = missed. John–Lucy, Linda–Lucy, Linda–Toba, Mark–John now pause for a card; Mark–Lucy loses the comic insert unless `playComicInsert`. Time-window QTEs on the card untested in play. Canvas now created only for QTE duos. `ShouldPlayInsert` only used by tests.
- After commit: core-systems Duos row (card-first no longer needs a library entry; the board-path hang now only in mode Off).
- No statics, no private IDs, line endings/BOM kept, no AI impact.
