# Escalation rubric

Owner: THJ. The coordinator sorts every decision into a tier. All three tiers get a row in `decisions.md`, so nothing is invisible.

- **Tier 1, decide and log:** act, write one log line, no mention in the report.
- **Tier 2, decide and flag:** act, then list it under "Decisions I made" in the next report so THJ can reverse it.
- **Tier 3, ask first:** stop that item, ask THJ, keep working on anything it doesn't block.

## By domain

| Domain | Tier 1: decide and log | Tier 2: decide and flag | Tier 3: ask first |
| --- | --- | --- | --- |
| Design | Tune a value inside an agreed range; fill a gap the spec clearly implies | Pick between options the spec leaves open; clarify a rule without changing how it feels | Anything touching Family Roles, Synergies, Duos or the Home; a new mechanic; changing an approved design; pacing of a key moment |
| Code | Bugfix with obvious intent; refactor inside an approved plan; tests; internal naming | Deviate from the tech plan with the same behavior; add a helper or pattern inside one system; any bugfix inside a core system | New package or dependency; save-data format; changing the public API or behavior of a core system (listed in `tech/core-systems.md`); deleting scenes, prefabs or assets |
| Content and narrative | Typo and consistency fixes against the glossary | New ability or UI text in an established voice; placeholder names | Character names, lore facts, story beats; anything touching Children of Morta canon |
| Scope and schedule | Reorder tasks inside a milestone | Split a task; defer a nice-to-have within the milestone | Milestone order or content; cutting a feature; work outside the backlog |
| Process | Update status, plans and reports; commit in `claude-handoff/` | Change a template or checklist | Change `CLAUDE.md`, this rubric or an agent's role; any session that needs THJ's machine; splitting a doc or renaming a section |

## Always Tier 3

- It can't be undone with a revert.
- Two agents disagree and this rubric doesn't settle it.
- It falls in one of THJ's areas (below).
- The coordinator isn't sure which tier applies. When unsure, go one tier up.

## THJ's areas

First version, 2026-10-15. Start tight, loosen at the Sunday review.

- **Core mechanic rules:** how combat, AP, Family Roles, Synergies, Duos and the Home work, and any change to them.
- **Major design decisions:** anything that changes what the player can do, choose or own.
- **Game feel:** timing, feedback, hit reactions, camera and animation pacing.
- **Dramatic moments:** boss beats, story beats, first-time reveals, Duo and Synergy showcases.
- **New reusable systems:** anything other features will build on, including core systems.
- **New tools and technology:** editor tools, pipelines, packages, Unity features, outside services.
- **Past calls:** prologue flow, Home presentation rules, showcase duo choice.

**Until 2026-10-29** (the first two weeks), anything in these areas is Tier 3 even when small.

## How to ask

Every Tier 3 question has five parts:

1. **Question** in one sentence.
2. **Context:** what triggered it and what it affects (systems, USPs, docs), three lines or fewer.
3. **Options:** two to four, each with its consequence and rough cost.
4. **Recommendation** and why.
5. **Blocked meanwhile:** what waits on the answer, and what continues without it.

In session, the question comes as a multiple-choice prompt. When THJ is away, it goes under "Waiting on THJ" in `status.md`. Non-urgent questions are batched. A Tier 3 question is never decided by timeout.

## Sunday review (about 15 minutes)

1. The coordinator posts the week's Tier 1 and Tier 2 counts, every Tier 2 item, every decision THJ reversed, and any skipped gate.
2. Each reversal moves that kind of decision up a tier.
3. Tier 3 questions THJ always answered with the recommendation become candidates to move down a tier.
4. Agreed changes are dated in the changelog below.

## Changelog

| Date | Change |
| --- | --- |
| 2026-10-15 | First version. THJ's areas set; Tier 3 for anything in them until 2026-10-29. |
