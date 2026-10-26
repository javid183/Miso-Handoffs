# Onboarding: the first hour, up to M4

Size: L    Tier: 3 (level structure, narrative, one new reusable system: Bond Lite)    Assigned to: miso-game-designer + coordinator (TD notes); miso-narrative for the story layer
Branch: all (built on `main`; a small slice of `thj/home-test`'s Bond is ported)
Status: **direction approved by THJ (2026-10-25)**; details below are the working plan. Nothing is built. Bond Lite needs THJ's yes on its tech plan before any code (new reusable system).

Decided in a design session with THJ, 2026-10-19 to 2026-10-25. Decisions D-168 to D-176.

## Why

Playtests (`playtests/2026-10-playtest-tasks.md`, S1, S8, Q1, Q2): the opening takes more than 2 hours to reach M4, nothing family-specific happens until M2, the first combo payoff comes late (Parsa), two story hooks compete (Ryker vs Adam's trail), and only Lucy seems to care about Ryker.

## Goal

A first hour that hooks the player in gameplay and story, shows every USP, teaches one thing at a time, and reaches M4 in about 45–60 minutes (the aim is pace, not only length).

## Acceptance criteria

- [ ] A cold player meets a Family Role QTE within the first ~5 minutes, a Synergy within ~10, and a Duo within ~15.
- [ ] Every playable Bergson's core loop and Family Role is taught before M4; FTP, pass-by, items, the world map, the mission map, the skill tree, the Workshop, Bond and the Family tree are each introduced once, at the point they're first needed.
- [ ] Each level teaches at most one new thing; its twist is separate from the thing taught.
- [ ] Every first use of a Duo, Synergy or Family Role in real combat gets a story beat (S8).
- [ ] Ryker is the only main story thread; every family member visibly cares.
- [ ] 3 Home visits before M4, each about 2–3 minutes, each adding one thing and asking for one decision that pays off in the next fight.
- [ ] Hearth to M4 plays in about 45–60 minutes in a cold playtest (today: more than 2 hours).

## Scope

In: the opening from the first screen to the M4 send-off; mission graph changes; level reuse and new levels; the Sister's Rivalry arc; Bond Lite; the first-trigger framed beat; the sisters' tally; story spine and clue structure (draft); Home visit content.
Out: M4's own pacing pass (needed, separate); Family Roles' cost (separate topic, D-036/D-042); the final narrative layer (drafted early, **implemented last**, after the level structure and pacing are play-checked); `thj/home-test`'s day loop.

## Touches

Systems: mission graph and roster (`Game Data.asset`, `Mission` assets), level prefabs and sequences, Home hub (Map Table, skill tree, Workshop, Training Ground/Yard), family skill tree and unlockables, `AbilityIntroductionTracker` (first-trigger variant), Q18 insert-shot, results screen MVP row and HUD, Bond Lite (new; the combat gate reads at level start — **core-adjacent**), run upgrades (one-off Tempest Bloom in the memory).
USPs: Family Roles, Synergies, Duos, Home.
Docs: `design/gdd/missions-structure.md`, `narrative-world.md`, `family-systems.md` (Sister's Rivalry unlock, Catch & Return discovery), `progression-economy.md` (FSP from the Yard scene), `glossary.md`, `decisions.md`, `status.md`; `reports/narrative-q1-q2-proposals.md` is partly superseded (see Narrative).

## The flow

| # | Step | Squad | Teaches (the one new thing) | Story beat |
|---|---|---|---|---|
| 0 | **Hearth** (Home state) | — | — | Ryker's anniversary. The family gathers to retell the rescue in the Caeldippo caves; Ryker lies by the fire |
| 1 | Memory: Linda's version | Linda | Basics (move, attack, AP, end turn), piercing lines, **Linda's Family Role** (works solo: first enemy-turn QTE) | "Three claws, one arrow." The Claws line up for her |
| 2 | Memory: Lucy's version | Lucy | Fire Embers (sidewinders), **Cyclone** | "There were at least ten!" More enemies walk in; her fire is bigger |
| 3 | Memory: John's version | John, Linda, Lucy | **John's loop: Family Role → Wrath** (protect, then punish) | The sisters steal kills and bicker in barks. John: "You both did." Neither accepts |
| 4 | Memory: Mark's version (Mark walks in late) | All four | Atman's Focus, Continuous Attack, **Mark–Lucy Duo (Chained Assault)**; every role firing (showcase) | The epic rescue. Tempest Bloom "happens" once. Ends on the cub saved and the mother lost: the one part nobody exaggerates |
| 5 | **Hearth** (Home state) | — | — | Laughter; Ryker goes quiet by the door. Night. Morning: she's gone |
| 6 | **World map** | — | Mission selection; two pins, both needed (AND gate) | Searching in shifts: someone always stays home in case she comes back |
| 7 | **The River** (1 level) | John, Lucy | **Lucy's Family Role**; Papa's Shelter (highlighted); Shield Flare to discover | Clue: Ryker's prints, blood, white fur, Dark Claws killed cleanly by an axe |
| 8 | **Home visit 1** | — | **Workshop** | Gear up the pair going out next (its weapon materials come from The River) |
| 9 | **The Ridge** (1 level) | Linda, Mark | **Mark's Family Role**; Catch & Return to discover | Clue: a man's deep tracks, as if carrying something; crushed healing herbs, a poultice wrapper |
| 10 | **Home visit 2** | — | **Skill tree**: one guided spend on the sister who just came home (she is fixed in M2); other points wait with a badge | Map Table: the clues go together, and the M2 pin appears (Q11 reveal beat) |
| 11 | **M2 · The Trail** (route choice, then one level) | Lucy, Linda + **John or Mark** (first squad pick) | **FTP: pass-by and items** under pressure; the **mission map** (route choice) | The animal pile. The sisters' tally fades out: "Still counting?" / "…No." Tracks lead to the Rootwell |
| 12 | **Home visit 3** | — | **Yard scene** (Bond) → **first Family point** → choose Sister's Rivalry or Tempest Bloom | Lucy can't sleep; Linda joins her at the Yard: "If they've hurt her…" / "Then we'll be ready." |
| → | **M4 send-off** (Map Table) | Lucy, Linda + **John or Mark** + Toba after his duel | First real trigger of the chosen Synergy gets its framed beat | The Rootwell |

Rough length: Hearth ~12–15 min (4 short segments, each 2–4 turns; cutaways 2–4 lines), 4 short levels, 3 Home visits of 2–3 min. About 45–60 minutes to M4.

**Cut from the opening:** the Adam / Margaret's journal / Arcanum arc (M1's story, M5 *The Healer*, M6 *The Arcanum*, M7 *In My Father's Arms*), M3 *A Wolf's Blood* and M3 *No More Waiting* as missions, current M2 *Ryker is lost* as a mission, and the Sister's Rivalry tutorial level (E1-C1). Their levels stay available as maps and chunks.

## Rules that run through it

1. **One new thing per level.** The twist (a clock, a rush, more enemies) is separate from what's taught.
2. **Panels only for rules; combos are discovered** through a bark, a highlight or a level layout that invites them (Papa's Shelter, Shield Flare, Catch & Return).
3. **Layout teaches; guided actions are the fallback.** If a step can't be taught by the layout, a "do this here" prompt is added (new tech, small).
4. **Every first gets a story beat** (S8): in the memory as a joke, in real combat as the framed first-trigger beat.
5. **Crisis framing at Home:** while Ryker is missing, every Home activity is preparing or holding together, never leisure.
6. **Each Home visit: 2–3 minutes, one new thing, one decision, and the decision pays off in the next fight.**
7. **Squads stay small early** (1–2, then 3, then 4 with Toba): fewer units means faster turns and less to read.

## The Hearth prologue (the memory)

- **Frame.** An unreliable-narrator retelling (precedents: *Prince of Persia: Sands of Time*, *Call of Juarez: Gunslinger*). It is canon-friendly: in Children of Morta whichever character the player chose saved Ryker, so every Bergson claiming the rescue is true for some player. Canon kept: the Caeldippo caves, Dark Claws, the mother dying to protect the cub; Lucy the most attached.
- **Build.** One mission, 4 short levels chained. Cutaways between segments are dialogue over a painted hearth still (`DialogNodeSequence` image nodes). A real Home state only at the open (step 0) and the close (step 5). No runtime Morta cutscene player for now (the `Saving_Pet_sequence` original stays an option to revisit).
- **Narrator interruptions** ("there were ten of them!") freeze play, show the change with the camera, then resume. Built from existing pieces: objective stages or trigger tiles → `SequentialSequence` (dialogue, camera, `LSBExecutionSequence` with `GUnitSpawn`).
- **Memory rules.** No XP. FTP kept topped up (`LevelStartFPFiller`, or a fill on cue), so Continuous Attack and the Duo can be used without teaching scarcity yet. Can't be lost in practice (tutorial enemy tier). Abilities used here **don't count as seen** for the first-trigger beat (or the memory clears them when it ends).
- **Unearned power, once.** Tempest Bloom fires once in segment 4 as a narrator's claim, via a one-mission grant of the existing run upgrade (`LindaLucyCycloneSpreadUnlock`). The skill-tree unlock later calls back to it ("Remember that shot?").
- **Enemy alert state.** Memory levels set "all enemies start alert" (memories don't sneak); the real missions use the default.
- **Grid fade.** D-131 hides the grid after M1 level 2; re-place that rule once the memory's levels are set.
- **Each segment teaches the narrator's identity loop, not their ability list.** Signature abilities (1 SP) are not taught here.

| Segment | Map source (to confirm on paper) | Notes |
|---|---|---|
| 1 Linda | `Level1-C1-2` (Linda alone, 4 Dark Claws, cave) | Lanes laid out so Claws end moves in her row: first Watch QTE on turn 1 or 2 |
| 2 Lucy | Showcase draft A "Lucy's Telling"; chunk 1 (sidewinders, Cyclone) | Spawn-on-cue for "ten of them" |
| 3 John | `Level1-C2` (three, cave) or showcase draft B "Papa's Telling"; chunk 3 (the gallery) | Turn 1 Shield Up + role prompt on a lunge at a sister; turn 2 Wrath-charged Shield Dash. One panel, a readable stack counter |
| 4 Mark | New level (cave, larger); chunks 13 (prism) and 21 (Chained Assault) as parts | Showcase, few new rules; the mother's death staged in-engine |

**Morta Story Viewer assets to use** (`Assets/MortaStory/Content/Story/HomeIdles/`; Home on `main` plays these through `HomeStateManager`): `MargaretStoryNight` (the family seated around a teller; the teller is Margaret, so it needs another teller or an edit, or a different answer to Margaret's canon status), `ApanStoryTelling`, `FirePlace`, `MoreFire`, `FamilyDinnerSad`, `LucyWolf`, `WolfSitDoor`, `WolfSadSit`, `WolfSitCliff`.

## The search (steps 6–11)

- **Story spine.** Ryker went out drawn by the memory of her mother, was attacked by Dark Claws, and was saved and carried off by a stranger who is tending her wound (Toba, unseen). This fits M4's "She came willingly" and "Waya, the Fangmother", and gives Lucy a better reason for her M4 anger than "thief": *"If he saved her, why didn't he bring her home?"* The animal pile (goblins taking animals for rituals) keeps the dread and sets up the Pathmother.
- **Clues.** Each pair's clue makes sense alone and means more together; they are combined at the Map Table (step 10), where the M2 pin appears. That is also Q11's one-at-a-time reveal beat.
- **Mark stays** after the Hearth, so the family searches in pairs. *A Wolf's Blood* (John and Linda keeping a secret from Lucy) is cut: the family shares the worry openly (Q2-1).
- **The River** (John, Lucy): forest; source maps `LevelLucyJohn-C1`, chunks 4 (alcoves), 5 (chorus), 6 (pockets, Shield Flare).
- **The Ridge** (Linda, Mark): forest/ridge; source maps `LevelLindaJohn-C1`, chunks 14 (the gauntlet, Catch & Return), 24 (the nook). Mark's role is taught by Linda's fragility (20 HP): an enemy hits her, Mark answers. **Catch & Return is a Family-tree node on `main` (1 FSP)**, so for discovery here it must be open for this mission (a one-mission run-upgrade-style grant, or open by default like Shield Flare). THJ to pick.
- **M2 · The Trail** (Lucy, Linda + John or Mark): a route choice on the mission map ("follow the blood" or "follow the tracks", both short), then the animal pile (from `LevelLucyJohn-C3`). Teaches FTP under pressure: starts low, pass-by refills it, the Health Potion and the Family Trinket. The one left behind "stays home in case she comes back"; write that line for John and for Mark.
- **Rigged rewards.** The River drops the materials for the next pair's weapons (Linda: Timber; Mark: Fabric), not the random pick. Neither trip is framed as a supply run; materials are ordinary rewards.

## Home visits

| Visit | New | Decision | Pays off in |
|---|---|---|---|
| 1 (after the first pair mission) | Workshop | Upgrade the outgoing pair's weapon | The second pair mission |
| 2 (after the second pair mission) | Skill tree, one guided spend; Map Table clue scene | First character skill point (the sister who just returned) | M2 (both sisters are fixed) |
| 3 (after M2) | Yard scene (Bond), Family tree | First Family node: Sister's Rivalry or Tempest Bloom; squad pick at the Map Table | M4 |

- The order of the two pair missions is the player's choice; both pairs contain a sister, so visit 2 always guides the sister who just returned.
- XP tuning: the first character SP must land for that sister by visit 2. John's and Mark's first level-ups can land after M2 to spread the trees.
- The first Family point is a **story reward from the Yard scene**, not from SP spending (PR-8 still applies afterwards).
- Kitchen and the rest of the hub stay as they are; nothing else is introduced before M4.

## The Sister's Rivalry arc (the S8 template)

| Beat | Where | What |
|---|---|---|
| Setup | Hearth | The bragging contest over who saved Ryker; "You both did," and neither accepts |
| Running joke | The River / The Ridge | They're apart but keep score: "Tell Lucy I'm ahead." Mark as go-between: "I'm not keeping score." "Yes, you are." The tally on the HUD and results screen |
| Turn | M2, the animal pile | The barks stop; they fight back to back. The HUD tally fades: "Still counting?" / "…No." |
| Build-up and unlock | Home visit 3, the Yard | Coping, not training: Lucy burns straw targets at night, Linda joins. They find racing works better when they set each other up. Bond Lv 2 → the Family point → both nodes light up → the player chooses. Worst case, the choice is forced to Sister's Rivalry |
| Payoff | M4, first real trigger | Framed beat: pause, both avatars (Q18 insert-shot), "Your turn." / "Watch this." After the fight, a quiet callback: "We both did." The tally returns as flavour |

- **Cap:** 1 per turn at first; higher caps open with more Bond, as skill-tree pips (S5: keep it, cap it).
- If the player picks Tempest Bloom, it gets the same framed first trigger, and its callback is to the memory's one-off shot.
- The same shape (Hearth setup, joke, turn, Home beat, first trigger) is the template for later Duos and Synergies.

## New tech (for the technical director)

| Item | What | Notes |
|---|---|---|
| **Bond Lite** (new reusable system, THJ's yes needed) | Pair Bond store (levels at 10 / 25 / 45, as on `thj/home-test`); sources: mission end for pairs in the squad, a capped bonus when one helps the other (Synergy, Duo, Family Role between the pair), one Home evening activity per visit; lock rules (pair level → node or ability); combat gate read at level start; level-up scenes at Home | Port `HomeLockRules` and the `HomeBondLocks` pattern from `thj/home-test` (read-only check: both are plain data and rules, apart from the day sim); a small standalone store that `HomeState` absorbs on merge. Only Linda–Lucy is gated now; Command Shield Dash and the Linda–Toba Duo stay open on `main` until decided. Tuning: Linda–Lucy start ~15, earn nothing in the pair missions (they're apart), low 20s after M2, the Yard activity crosses 25 |
| **Sister's Rivalry into the Family tree** | A family node plus its Bond lock; cap pips | Open on `main` today |
| **First-trigger framed beat** | Pause, avatars, 2 lines, resume, on the first real trigger of a Synergy, Duo or Family Role | Extend `AbilityIntroductionTracker` (today: introductions at level start) with an on-first-trigger hook; pause pattern from `EnemyIntroductionController`; frame from Q18 |
| **Sisters' tally** | HUD side counter while both sisters are in the squad; results screen's MVP row | Fade-out on a sequence cue (M2) |
| **Hearth cutaways** | Painted still + dialogue between memory levels | Existing image nodes; needs the painting |
| **Narrator interruptions** | Freeze, camera, spawn on cue | Existing sequences and `GUnitSpawn` |
| **One-mission grants** | Tempest Bloom in the memory; possibly Catch & Return in The Ridge | Run upgrade grant at level start or a pickup |
| **Mission graph** | Hearth → (River ∥ Ridge, AND) → M2 → M4; roster rules for M2 (2 fixed + 1 free) and M4 (2 fixed + 1 free + Toba placed) | M4's levels need deploy slots (Missions Q8) |
| **Guided actions** (fallback only) | "Do this here" prompt | Only if layout can't teach a step |

## Narrative work (draft early, implement last)

- Story drafted now; the final narrative layer goes in after the level structure and pacing pass a play check.
- Q1 (directed dialogue) applies to every new scene: no scenery narration, no objective-explaining lines; barks and trigger lines carry the rest.
- Q2 items still live: Ryker's pronoun ("she"), the "thief" line (now motivated by "why didn't he bring her home?"), name "this part of the forest", M4 lines for an absent John (write John and Mark versions of his key M4 lines: "Put Ryker down, Lucy", "We came together. We continue together", "She stays at our house").
- **Superseded by this plan** in `reports/narrative-q1-q2-proposals.md`: the masked-man setup options (now: the River and Ridge clues), "why they go home after A Wolf's Blood" (mission cut), the Q1 M1/M2 slice and its S8 beat placements (the levels are restructured), and the M5 grandma line (M5 cut). Still open there: forms of address, the forest name, the mask's reason, the "Masked Stranger" plate, and **Margaret's canon status** (alive or dead also decides whether `MargaretStoryNight` can be used at the Hearth as is).

## Risks

- **Prologue length.** Four segments plus cutaways can swell past 20 minutes. Hard caps: 2–4 turns a segment, 2–4 lines a cutaway; cut a segment before stretching one.
- **Front-loading in the memory.** Segments 1–3 teach; segment 4 adds almost no rules. Whatever doesn't fit moves to the search.
- **Readability of interruptions.** Always freeze and show the change; never change rules silently.
- **Delayed payoff of Home decisions.** Handled by the visit design (each decision pays off next fight).
- **Tone.** The mother's death is never joked about; the jokes stop when the story reaches it.
- **Merge with `thj/home-test`.** Bond Lite uses the same model and names so the branch folds in.
- **Scope.** New levels: segment 4, the River, the Ridge, M2's branches. Others are reworked from existing maps and chunks.

## Open questions for THJ

Answered 2026-10-25: 1 → open by default, the node upgrades it (D-177); 2 → alive, she hosts (D-178); 3 → yes (D-179). Build order: structure first (D-180, `plans/onboarding/2026-10-25-onboarding-first-hour-workplan.md`).

1. Catch & Return in The Ridge: open by default on `main`, or a one-mission grant?
2. Margaret: alive or dead in Miso's timeline (canon)? It decides the Hearth teller and the `MargaretStoryNight` idle.
3. Bond Lite: OK to go to a tech plan as described?
4. Keep the option of a single combined search mission (no Home between the pairs) as the fallback?
5. The Hearth painting: who paints it, and is one still enough (with the Home state at both ends)?

## Next steps

1. THJ answers the open questions.
2. Paper plans for each level (grids from `design/level-chunks.md`, `tools/grid_render.py`): segments 1–4, the River, the Ridge, M2's branches and the pile.
3. Technical director: tech notes for Bond Lite, the first-trigger beat, the tally, mission graph and rosters.
4. Narrative draft of the Hearth, the clues, the Yard scene and the M4 line variants.
5. Build the structure with placeholder text, play-check the pacing, then the narrative layer.

## Gates

Design only for now. Before build: THJ's yes on Bond Lite's tech plan (Tier 3, new reusable system). Play check: yes, a cold playtest from the Hearth to the M4 send-off, timed. Docs to update after decisions land: the GDD pages listed in Touches, `glossary.md`.
