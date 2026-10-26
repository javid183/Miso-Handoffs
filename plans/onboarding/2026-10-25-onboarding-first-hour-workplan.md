# Onboarding: the first hour — work plan

Size: L    Tier: 3 (parts; see each chunk)    Assigned to: coordinator (routing, TD notes), `miso-game-designer`, `miso-narrative`, `miso-implementer` → `miso-reviewer` → `miso-verifier`
Branch: all (code lands on `thj/onboarding`, cut from `main` @ `dc64f974a`)
Status: approved order (D-180). Design Q1–Q3 answered (D-177 Catch & Return open by default, node becomes an upgrade; D-178 Margaret alive, hosts; D-179 Bond Lite to a tech plan). Still open: Q4 (single combined search mission as fallback), Q5 (Hearth painting), Rivalry's empty reward on `main`, who authors the levels

Design: `plans/onboarding/2026-10-25-onboarding-first-hour-design.md` (D-168 to D-176). This file says **who does what, in what order, and what each step waits on**. It does not change the design.

## Why

The design is approved as a direction; nothing is built. It touches levels, missions, Home content, narrative and three pieces of new tech, so it needs an order that keeps one writer in the Unity project at a time, lets the paper and text work run alongside, and gets to a timed cold playtest of the structure before the narrative layer goes in (D-168).

## Goal

A greybox opening (Hearth → River ∥ Ridge → M2 → M4 send-off) with placeholder text that THJ can play and time, then the new tech, then the narrative layer.

## Code facts checked 2026-10-25 (on `thj/onboarding`)

| Plan relies on | What's there | Effect on the plan |
|---|---|---|
| Mission graph AND gate (River ∥ Ridge → M2) | `SerializableDependencyGraph` has a per-node `CombineMode` (any/all of the previous nodes, `:247-259`); `GameData` holds the mission graph | Data only, no code |
| M2/M4 rosters "2 fixed + 1 free" | `MissionRoster` has fixed slots, free slots, forced include/exclude (`Mission.cs:33-60`) | Data only. "Toba placed after his duel" in M4 and M4 deploy slots (Missions Q8): still to check |
| No XP in the memory | `Mission.completionXPReward` exists; per-kill/level XP not checked | Check in the structure tech notes |
| FTP topped up in the memory | `LevelStartFPFiller` (level start only, `Produce(n)`) | Enough for "start full"; "refill on cue" may need a small hook |
| One-mission Tempest Bloom | `RU_LindaLucyCycloneSpreadUnlock.asset` + `RunUpgradeTracker.TryGrant` | Grant at level start (data or a tiny component). Run upgrades last a run; check they clear after the memory |
| First-trigger framed beat | `AbilityIntroductionTracker` only plays intros at level start (`PlayPending`), saved seen-set keyed by preset name | Needs an on-first-trigger hook + a "memory doesn't count" rule. New code |
| Bond Lite | `HomeLockRules.cs`, `HomeBondLocks.cs`, `BondSceneDefinition.cs` exist only on `thj/home-test` | Port as plain data + rules, per the design. Tier 3 tech plan |
| Sister's Rivalry in the Family tree | Open from the start on `main` (GDD Family systems:126); Family points come from level-ups (`AbilityUpgradePanelUI.AwardFamilySkillPointsForLevelUps`) | Needs a family node + Bond lock + a story-granted Family point. Rivalry's reward adds nothing on `main` (GDD Q11, no basic-attack cooldown): **flag**, see Risks |
| Missions core | `MissionTracker`, `Mission`, `MissionRouteProgress` are in `tech/core-systems.md` | Data changes are fine; any code change there is Tier 3 |

## The work, in order

Phases A run now, mostly in parallel (no Unity writes). Phase B is one writer at a time. Phase C closes it.

### Phase A — decide and draw (no game code)

| # | Step | Owner | Waits on | Output |
|---|---|---|---|---|
| A1 | THJ answers the design's open questions Q1–Q5 | THJ | — | `decisions.md` rows |
| A2 | **Paper level plans**: memory segments 1–4, The River, The Ridge, M2's two route levels and the animal pile. Grids from `design/level-chunks.md`, `tools/grid_render.py`; per level: the one thing taught, the twist, turn budget (memory 2–4 turns), where the first Role/Synergy/Duo trigger happens, interruption cues, start-alert setting, rigged drops | `miso-game-designer` (critic pass: UX lens for "one thing per level") | Q1 for The Ridge only | `plans/2026-10-2x-onboarding-levels.md` + grid images |
| A3 | **Structure tech notes** (`miso-tech-plan`): mission graph and Mission assets, rosters, memory rules (no XP, FTP, "doesn't count as seen", start alert, grid-fade rule D-131 re-placed), narrator interruptions from existing sequences, one-mission grants, Home visit hooks (guided Workshop, guided skill spend, Map Table clue scene, M2 pin reveal), what's cut from the graph. Mostly data; list every code touch and its tier | Coordinator | — | `plans/2026-10-2x-onboarding-structure-tech.md` |
| A4 | **New-tech plans**: (a) Bond Lite + Sister's Rivalry family node + story Family point; (b) first-trigger framed beat; (c) sisters' tally (HUD + results MVP row, fade cue). One plan file each, so each gets its own yes | Coordinator | (a) Q3 yes to go to a tech plan | three tech plans, each Tier 3 |
| A5 | **Narrative draft, placeholder grade first**: one line per beat for the greybox (Hearth cutaways, the 4 narrator jokes, clues, Map Table, "stays home" lines for John and Mark, Yard scene, framed-beat lines). Full draft later, in parallel with B | `miso-narrative` | Q2 (Margaret) for the Hearth teller | `plans/onboarding/onboarding-narrative-draft.md` |

### Phase B — build the greybox (one writer at a time, each chunk play-checked by THJ before its commit)

| # | Chunk | Depends on | Tier | Notes |
|---|---|---|---|---|
| B1 | Mission graph + Mission assets + rosters; cut missions unlinked (assets kept) | A3 | 2 (data) / 3 if code | Smallest playable path first: empty levels allowed |
| B2 | Hearth memory: 4 segments as one mission, cutaways with a placeholder still, memory rules, Tempest Bloom one-off, interruptions | A2, A3, B1 | 3 (dramatic moments, until 2026-10-29 all of it) | Largest chunk; split per segment if the paper plan is big. Segment 4 is a new level |
| B3 | The River, The Ridge (incl. Catch & Return open per Q1), rigged drops | A2, B1 | 3 | Two new levels |
| B4 | M2 The Trail: route choice + pile level, FTP-low start | A2, B1 | 3 | |
| B5 | Home visits 1–3 with placeholder text: guided Workshop, guided skill spend + badge, Map Table clue scene + M2 pin, Yard scene stub, M4 send-off | A3, B1 | 3 (Home) | Yard scene's Family point can be a stub until B7 |
| — | **Pacing play check** (THJ plays, then a cold player, timed Hearth → M4 send-off). Cut before stretching (design Risks) | B1–B5 | — | Gate for the narrative layer |
| B6 | First-trigger framed beat | A4(b) yes | 3 (core-adjacent: ability events) | Can start right after B1 if THJ prefers tech first |
| B7 | Bond Lite + Rivalry node + story Family point | A4(a) yes | 3 (new reusable system) | `model: opus`; must fold into `thj/home-test` on merge |
| B8 | Sisters' tally | A4(c) yes | 3 (game feel) | |

### Phase C — close

| # | Step | Owner |
|---|---|---|
| C1 | Narrative layer in (replaces placeholders) after the pacing check | `miso-narrative` text → `miso-implementer` |
| C2 | Final timed cold playtest against the design's acceptance criteria | THJ (+ `miso-verifier` for compile/tests) |
| C3 | Docs: GDD `missions-structure.md`, `narrative-world.md`, `family-systems.md`, `progression-economy.md`, `glossary.md`; `status.md`, `build-log.md`; mark the superseded parts of `reports/narrative-q1-q2-proposals.md`; GDD mirror sync noted | Owners per `README.md` |

**Recommended order:** A1–A5 now → B1 → B2 → B3/B4 → B5 → pacing check → B6 → B7 → B8 → C. Structure first because pacing is the main goal and every new-tech piece is easier to judge inside a real flow. The alternative (B6/B7 right after B1) front-loads the risky code but delays the first timed play.

## Risks

- **Half of Sister's Rivalry's reward is empty on `main`**: the +AP works, the "basic attack ready again" adds nothing (no basic-attack cooldown, GDD Q11). Corrected 2026-10-26 from "the reward is empty". Asked as BL4 in `plans/onboarding/2026-10-26-bond-lite-tech.md`.
- **Level authoring load.** Five new levels (segment 4, River, Ridge, two M2 branches) plus reworks. Who builds levels in the editor (THJ or the implementer with builders) decides the B pace; ask before B2.
- **Run-upgrade lifetime.** The one-off Tempest Bloom must not leak past the memory; check in A3.
- **Missions core.** Any code change in `MissionTracker`/`Mission`/`MissionRouteProgress` is Tier 3; A3 aims for data only.
- **`AIRegressionTest`** may shift with new levels or alert settings; it stays known red, never re-baselined.
- **Branch.** `thj/onboarding` is not in `branches.md` yet, and its working tree has THJ's uncommitted `Packages/` and `ProjectSettings/` edits; agents leave them alone.

## Gates

Compile / EditMode tests (known red only) / review for every code chunk / THJ play check before each commit (feel and gameplay chunks) / timed cold playtest before C1 and at the end / docs per C3.
