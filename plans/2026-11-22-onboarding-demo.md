# Onboarding demo: the Hearth to the end of M4

Size: L    Tier: mixed (each chunk carries its own; Tier 3 ones are marked)    Assigned to: coordinator → `miso-implementer`, `miso-game-designer`, `miso-narrative`; Khash, Art and the narrative designer for their items
Branch: `thj/onboarding-demo` (D-604, reverses D-602's `main`; created 2026-11-22 from `main` @ `551685704`). A chunk with vital or risky new tech gets its own branch, asked first
Status: approved for structure (THJ 2026-11-22). Each chunk starts once its questions (below) are answered
Progress: `status.md` (row `onboarding-demo`) is the live record; decisions D-602 to D-639. As of 2026-11-23: Phase 1 built and committed except X-25 (waiting on THJ's play check); 3.1a (Mark's kit) and 3.1b (M1) committed; next 3.1a-2, 3.2 (M2); M3 and M4 paper levels waiting on THJ's approval

## Why

THJ's demo tweak list (2026-11-19, added to on 2026-11-20 and 2026-11-22), tidied into the Claude Doc **"Demo tweaks: Hearth to the end of M4"** (https://claude.ai/artifact/Eg7iNf37y7FnydDpnNWXYH; snapshot copy in THJ's Google Drive; a markdown snapshot for agents at `design/demo-tweaks-snapshot.md`). THJ answered 18 of its 20 questions in the doc's comment threads on 2026-11-20. That doc is the source for every item ID used here (H-, E-, W-, M1- to M4-, X-); this plan only orders the work.

## Goal

A demo that plays from a new game through the Hearth, M1 ∥ M2, M3 and M4's end sequence, with every item in the tweak doc done, cut by THJ, or handed to its owner with its container in place.

## Acceptance criteria

- [ ] Every ID in the tweak doc is done, cut by THJ, or handed over (Khash, Art, narrative designer) with the container built and a `[PLACEHOLDER]` in it.
- [ ] A cold play-through on `main` from a new save to M4's end sequence, with intro and outro sequences on, no debug UI and a clean console.
- [ ] Full EditMode suite green (the AI regression test is Explicit, D-579).
- [ ] The docs listed under Touches match what was built.

## Scope

In: every item in the tweak doc.
Tracked here but built by others: Khash's W-02, W-03, W-05, W-06, W-08, X-07, X-09; Art's final art (H-10 pictures, H-11 after the first pass, W-04, X-06, portraits, animations); the narrative designer's final words (doc section 8).
Out: the Home demo's systems (`thj/home-test`) except what X-19 picks; Bond Lv 3 knots; Trios.

## Touches

Systems: the memory levels `GB_m1-linda` to `GB_m4-mark` and their `HearthMemoryWiring.*` tools; `GB_s2-ridge` (M1), `GB_s1-river` (M2), the Trail prefabs (become M3); the M4 Mission asset, its level graph and roster; the Home scene's states, idles and sequences; `LevelAbilityLock`, `GuidedAbilityHint`, `UnlockAbilitiesSequence`, `MoveUnitSequence`, `CastAbilitySequence`; a new "ability used → play a sequence" trigger (not core); barriers and enemy targeting **(core: `AIUnitBrain`)**; `LevelStartFPFiller` and FTP (until X-27); skill tree data; Workshop item data; dialogue characters; the duo insert player (built on `main` 2026-11-22, Mark–Lucy).
USPs: all four. Family Roles (H-16, M1-03, M2-06, X-15), Synergies (M1-02, M2-02/03, X-02, X-21), Duos (X-23, X-27 to X-29), Home (E-*, M3-07, X-11, X-18, X-19, X-24, X-25, X-30, X-31).
Docs: GDD `missions-structure.md` (MI-29 to MI-31, the mission table, M4), `family-systems.md` (Roles, Pass-by, Revenge in memories), character pages (Lucy's Cyclone page, Mark's Move vs Vault, Linda's Encore), `enemies.md` and the glossary (enemy names, Mary as the Hearth's host), the onboarding levels plan, `tech/onboarding-merge.md`, `tech/core-systems.md` (if the AI changes), `branches.md`, `status.md`, `decisions.md`, and the tweak doc itself (mark items done).

## Approach

One writer in the Unity project at a time. Design work (paper levels, X-15, X-27's design) and narrative placeholders are read-only for the project, so they run alongside a build chunk. Every chunk follows the coordinator loop: tech plan only for M and L, review for code (always for core), THJ's play check, docs.

### Before the first play check

- **P0. Sequences on.** Done 2026-11-22: THJ turned intro and outro sequences back on (they were off on `main` since D-600).

### Phase 1: fixes and switches (no design; S each)

| Chunk | IDs | What | Tier | Notes |
| --- | --- | --- | --- | --- |
| 1.1 | H-03, H-04, H-05, X-01, H-06, H-07 | Memory rules: no Revenge, no Pass-by, no Cleanse in any player kit (Cleanse only where a cleansable circle is, M4 level 1), hide the empty item bag, heal at the start of memories 3 and 4 | 1, or 2 if Revenge or Pass-by needs a new level switch | Through the wiring tools where they own the data, by hand in the prefab for memory 4 (the master, D-405) |
| 1.2 | H-01 | Enemy intro sequences play last, right before the player gets control (all memories; check the search levels too) | 1 | Sequence order only |
| 1.3 | H-08 | Linda's grounded arrows return to her quiver when a level is won, before its ending sequence, in every level | 2 | Small code, reuses Encore's return |
| 1.4 | H-09 | Encore's 2 AP: find what's broken, then fix it or drop the cost and its text | 1 to fix; 3 to drop (cost change, D-302, D-327, D-383) | |
| 1.5 | X-10, X-04 | "Start Game" over the hearth becomes "World Map"; Encore's flying arrows get a visible colour | 1 / 2 (visual values) | |
| 1.6 | X-24, X-25 | Bugs: the Kitchen and stat-up stations don't open or give no feedback; the Family tree doesn't open after M3's Linda–Lucy scene | 1 (2 if a core file) | Explore first. X-24 first suspect: the onboarding station locks (Bookshelf, Training Field, Cooking Cabinet until after M4) |

### Phase 1 follow-ups (added 2026-11-23; S each)

| Chunk | IDs | What | Tier | Notes |
| --- | --- | --- | --- | --- |
| 1.7 | X-34 | Mark's avatar draws behind the HUD frame, not in front | 1 | Draw order |
| 1.8 | X-36 | The selected-unit indicator (`SelectedUnitIndicator`) shows under the hero's feet in every level | 1 (2 if a core file) | Explore which levels fail and why (layer, sort order) first |
| 1.9 | X-35 | The Whirl at the end of a Steer also hits the enemies the Steer passed through (rule change, D-648, reverses D-583) | 3, decided | Cyclone code and tests; designer updates GDD `lucy.md` LU-4/LU-6; check the damage in play (lever: a lighter graze on the pass) |

### Phase 2: the Hearth (narrative tech; M)

| Chunk | IDs | What | Tier | Notes |
| --- | --- | --- | --- | --- |
| 2.1 | for H-19, H-21 | New trigger: "ability X used → play a sequence" | 3 (new reusable piece); asked once with the chunk | S, not core. Also usable for future tutorials |
| 2.2 | H-02, H-14, H-15, H-16, H-17, H-21 | Memories 1 to 3: Ryker as a prop in each; memory 1 opens on her (camera); memory 2 opens with her mother's body in view; memory 3: only John has a Role; Mark interrupts at its end; the Cyclone steer page after Lucy's first cast (needs 2.1) | 2 | Placeholders by `miso-narrative` |
| 2.3 | H-18, H-19, H-20 | Memory 4: Linda only shoots until the Cyclone part; after Mark's entrance, his kit locked to the primary attack for one action (needs 2.1), with the pulse; John's line at the den mouth | 2 | |
| 2.4 | H-12, H-13, H-22, E-01 to E-04, part of X-12 | The storytelling cutscene and ending: Ryker lies by the fire and slips out before the last memory; Margaret leaves the idle, Mary takes her lines (Mary's dialogue character with a placeholder portrait); the next teller stands before each memory; back at Home: they notice Ryker isn't there, everyone stands, Lucy walks out, fade, "The day after", the morning worry | 3 for the beat order (game feel, story beat) | Uses existing animations where they exist; missing ones listed for Art |
| 2.5 | H-11 | First art pass on the memory levels: a background and a couple of props copied from a matching level, skipped wherever it would mean rework | 2 | THJ looks before Art takes over |

### Phase 3: the missions (design first; L)

**D3, paper levels** (`miso-game-designer`, skill `miso-level-chunks`), one per mission, with the coordinator rendering every grid (gate 7) and THJ approving each before it's built:

| Mission | IDs | Questions to answer before its paper level is final |
| --- | --- | --- |
| M1 · Linda & Mark (The Ridge reworked) | M1-01 to M1-03, X-26 | Does the Masher and Catch & Return beat replace today's corridor beat? With Move instead of Vault (X-26), how does Mark set up the catch? |
| M2 · Lucy & John (The River reworked) | M2-01 to M2-06 | Q10: the Pile here is Ryker's clue only and "Still counting?" stays in M3? |
| M3 · Defence (replaces The Trail) | M3-01 to M3-05 | Q12: does the stone push take his actions each turn, or run by itself? |
| M4 · 3 levels | M4-01 to M4-03 | Q14: is "Mithra's Rest" the campfire Rest Room? Q15: the Goblin Queen as the boss, and 4 seats with Toba fixed? |

The designer also writes two short notes in the same pass: X-20 (where a Divine Relic is introduced before M4) and X-19 (which `thj/home-test` station, if any, joins cheaply).

| Chunk | IDs | What | Tier | Notes |
| --- | --- | --- | --- | --- |
| 3.0 | M3-03 | Barriers: an object with HP on the waves' path; an enemy whose way is blocked attacks it. Tech plan first | 3 (core: AI) | Own commit, review, full suite. Own branch if the plan shows risk to the AI (D-602 exception) |
| 3.1 | M1 | Build from the paper level (grid-to-level, wiring, sequences) | 2 | |
| 3.2 | M2 | Same; the rush is a sequence (MoveUnitSequence), the player casts Shield Flare | 2 | |
| 3.3 | M3, M3-06, M3-07 | Same, plus Toba's appearance and the Home beat after it (the house reacts to Toba, then the Linda–Lucy scene) | 3 for the story beats | Needs 3.0 |
| 3.4 | M4 | Mission asset with 3 levels; roster Toba fixed + picks; the cleanse fight, the rest level, the boss and the end sequence | 3 (roster and story beat) | Changes C5a's roster and `M4SquadPickTests`; Toba now joins before M4, so the Bond Threads plan's demo section changes too |

### Phase 4: presentation and text

| Chunk | IDs | What | Tier |
| --- | --- | --- | --- |
| 4.1 | X-12 | Dialogue characters for Kevin and Ben (Mary is done in 2.4), placeholder portraits | 2 |
| 4.2 | X-02, X-03 | Synergy barks (check for a hook first) and fewer, more directed barks (data) | 2 |
| 4.3 | X-11, X-18 | Idles per Home state; the skill tree tutorial | 2 |
| 4.4 | X-22, X-21, X-23 | The coordinator lines up the insert-shot options for THJ (OnScreenAvatar, FTPPanel, StuntCamActorSet, and the Mark–Lucy duo insert built on 2026-11-22); after THJ picks, Synergy inserts and the other Duo inserts | 3 (game feel) for the pick, then 2 |
| 4.5 | X-08 | Workshop: a quiver item for Linda in place of her ribbon | 2 (name and text by narrative) |
| 4.6 | X-17 | Tutorial pages: draft screenshots captured in Play (check whether a page can play video) | 2 |

Narrative runs alongside: `miso-narrative` writes each placeholder as its container is built; the narrative designer gets the doc's section 8 list (X-05 enemy names, X-16 ability descriptions in one voice, W-01, W-07, H-10 texts and the final lines).

### Phase 5: system decisions (THJ-led; design in parallel, build late)

| Item | IDs | Order |
| --- | --- | --- |
| Family Roles final decision | X-15 | First. Until then H-16, M1-03 and M2-06 are built with the Roles as they are, and revisited after |
| New Duo resource | X-27, then X-28, X-29, X-30 | After X-15. Design plan with critics, then a tech plan (core), likely on its own branch. X-28 is a sweep over every demo level's FTP fill and its tutorial pages; X-29 rides the first Duo (memory 4); X-30 only if FTP goes |
| Skill trees | X-13, X-26 | With the Bond Threads decision (plan `2026-11-18-bond-threads-design.md`, waiting on THJ) |
| Home stat upgrades | X-31 | With X-24 and X-30 |

### Phase 6: balance and the full play-through

| Chunk | IDs | What | Tier |
| --- | --- | --- | --- |
| 6.1 | X-32 | On game start, check the save data on the player's machine and delete it if it's too old for the demo, so an old save can't break the onboarding | 3 (deletes player data; can't be undone) |
| 6.2 | X-33 | Final check of the combat log: every ability, Synergy, Duo, Family Role and new piece in the demo (Cyclone, barriers, the new Duo resource) writes its lines | 1 |
| 6.3 | X-14 | Final balance after a full play-through on `main` | 2 (values) |
| 6.4 | — | A cold playtest with a new player; docs and the Claude Docs mirror synced | — |

### Order

Phase 1 now. Phase 2 after it (2.1 first). D3 paper levels start alongside Phase 1, since they don't touch the project. Phase 3 builds in the order M1, M2 (side by side in the game, so either first), M3 (after 3.0), M4. Phase 4 fills gaps between level chunks. Phase 5 decisions can come at any time; X-27's build waits until Phase 3 is done so the levels are retuned once.

## Risks

- **The new Duo resource lands late** (X-27): every level's FTP fill and the tutorials that mention FTP get redone. Kept small by keeping each level's FTP in its `LevelStartFPFiller` and the wording in tutorial pages, so X-28 is one sweep.
- **Family Roles undecided** (X-15): the Role intros in M1 and M2 may be redone. They are built small for that reason.
- **Barriers touch the AI** (core): own commit, review, full suite; a branch if the tech plan shows real risk.
- **Wiring tools and hand edits**: the wiring keeps hand-edited dialogue (D-526) and never rewrites an existing step list, so structure changes in a memory need either the tool's new-asset path or a hand edit in the prefab (memory 4 is hand-owned, D-405). Each chunk says which.
- **M4 roster change** breaks C5a's tests and `tech/onboarding-merge.md`'s M4 row; both are updated in 3.4.
- **The Pile moves** from The Trail to The River: the tally's "Still counting?" fade is saved per save; 3.2 and 3.3 keep it with the sisters.
- **Shared scenes**: the Home scene and the world map are also Khash's (W-02 to W-08, X-09). The coordinator checks with THJ before a chunk edits a scene Khash may have open.
- **Intro and outro sequences are off on `main`** (D-600): see P0.

## Gates

Per chunk: compile with a clean console; full EditMode suite green; `miso-reviewer` for code (always for core); every acceptance item checked with evidence; grids rendered for level chunks (gate 7); THJ's play check (yes, every chunk needs his time; the coordinator batches small chunks into one check); docs updated by their owners. The tweak doc is marked as items close.

## Open questions, answered when their chunk comes up

| Q | Question | Chunk |
| --- | --- | --- |
| Q7 | Build the "ability used" trigger so Mark's lock lasts one action (recommended), or lock until the Hold? | 2.1, 2.3 |
| M3-07 | The Linda–Lucy scene = today's Yard scene? | 3.3 |
| H-22 | Does the player see Ryker walk out between memories 3 and 4, or is she just gone? Note: `MargaretStoryNight` has Margaret as the teller, so H-22 and H-12 change the same idle | 2.4 |
| X-32 | What makes a save "too old": a save version stamped by the build (recommended), or its date? And is the player told before it's cleared? Related: old dev saves aren't migrated after Mark's kit change (D-636), and Vault gets a new save key (D-637); X-32 is the player-facing version of that rule | 6.1 |

Answered (see `decisions.md`): Q10 (D-607), Q12 (D-608, D-622), Q14 (D-612, D-626), Q15 (D-613), M1-02 (D-605), X-26 (D-606, then D-633: Move = Command; D-637: Vault buyable), X-20 (D-625), X-24 stations after M3 (D-618), Cleanse only in M4's first fight (D-614).
