# Miso: Game Design Document

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 · Mirror: Claude Doc "Miso — Game Design", tab Overview

**Children of Morta: Tactics** (codename Miso) is a grid-based, turn-based tactical RPG about the Bergson family fighting the Corruption. Each chapter sets a main dungeon and a deadline; the family prepares through side missions and life at Home, then goes in together. This page is the front door: what the game is, how it fits together, and where each rule lives.

## How to read this document

- **One home per fact.** Each rule and number lives in one sub-doc. This page summarizes and links (D-044, D-047).
- **Names** follow [`glossary.md`](../../glossary.md). A code name appears in `code style` only when it differs from the player-facing name.
- **Mission numbers vs Home milestones.** M1–M14 and MX are campaign missions (the `Mission` assets). The Home system's build milestones are written "Home M0" to "Home M9".
- **Branches.** Values are read from `main`; Home values from `thj/home-test`, the only branch with the Home system (D-046). A rule that differs is written once, where it lives: "**On `thj/home-test`:** ...". Current branch state: [`branches.md`](../../branches.md).
- **Sources.** Every value table ends with a Source line naming the asset or script it was read from.
- **Rule IDs** are stable: plans, decisions and doc comments can cite them. An ID is never reused; a dropped rule keeps its ID.

| Prefix | Sub-doc | Prefix | Sub-doc |
| --- | --- | --- | --- |
| `CR` | Combat rules | `EN` | Enemies |
| `FR` | Family Roles (Family systems) | `PR` | Progression and economy |
| `DU` | Duos (Family systems) | `MI` | Missions and structure |
| `SY` | Synergies (Family systems) | `HO` | Home |
| `PB` | Pass-by (Family systems) | `NA` | Narrative and world |
| `JO` `LI` `LU` `MA` `TO` | The five character sheets | | |

- **Status** of every rule and value:

| Status | Meaning |
| --- | --- |
| Built | In the assets or code as described |
| Built, differs | Built, but differently from the design; both are shown |
| Planned | Decided, not built yet |
| Deferred | Decided to wait; code may exist |
| Proposed | Not decided; awaiting THJ |
| Open | A question with no proposal yet |
| Dropped | Decided against; kept for history |
| Demo | A number that applies to the Home demo only |

## Pillars and USPs

Summary of [`vision.md`](../../vision.md) (THJ owns it; it wins).

| USP | In one line | Lives in |
| --- | --- | --- |
| Family Roles | Each Bergson has one reactive passive that protects or supports the family | [Family systems](family-systems.md#family-roles) |
| Synergies | Automatic, conditional effects between family members | [Family systems](family-systems.md#synergies) |
| Duos | Deliberate paired abilities, paid with AP and FTP | [Family systems](family-systems.md#duos) |
| Managing the Home as a Family | Between missions, the family lives, works and grows together | [Home](home.md) |

Pillars: grid tactics with reaction timing (QTEs on both turns) · family-driven cooperative combat · emotional narrative, warmth against dread · elevated Children of Morta pixel art.

## How the game is structured

```
 Chapter: a main dungeon + a deadline (the Great Moon)
                     │
                     ▼
 ┌──────────────────────── Home ─────────────────────────┐
 │ Dawn plan → Morning → Afternoon → Dusk → Night         │
 │ stations, Bond, food, study, workshop, training        │
 └──────┬─────────────────────────────────────▲───────────┘
        │ sortie from the map table           │ drops, XP, Wounded
        ▼                                     │
  Side mission: 1–3 combat levels ────────────┘
        │
        ▼ by the deadline
  Main dungeon: a multi-level run with routes, rest rooms
  and in-run upgrades → the chapter ends
```

- **On `main`:** there is no Home system. Missions unlock along the campaign graph (M1 → M2 and M5 → both M3s → M4 and M6 → M7; a second branch holds M8–M14), and the hub's station panels sell family stat upgrades for gold.
- **On `thj/home-test`:** the Home day loop above runs the demo: a 3-mission prologue, then a 7-day moon cycle ending in the Goblin Queen's Warren.

Where each part is designed: [Missions and structure](missions-structure.md) · [Combat rules](combat-rules.md) · [Home](home.md).

## Three layers of power

| Layer | Lasts | Comes from | Lives in |
| --- | --- | --- | --- |
| Permanent | The whole game | Skill trees, family stats, gear, Bond and Duos | [Progression and economy](progression-economy.md), [Home](home.md) |
| Per sortie | One mission | Send-off meal, Omens | [Home](home.md) |
| Per run | One mission or dungeon attempt | Routes, run upgrades (runes), Divine Relics, rations | [Progression and economy](progression-economy.md#run-upgrades) |

## The game at a glance

| Item | Value | Status |
| --- | --- | --- |
| Playable family | John, Linda, Lucy, Mark, Toba. Mark joins after M3 "No More Waiting". Kevin works at Home only (`thj/home-test`) | Built |
| Squad size | Set per mission: 2 to 4 | Built |
| AP | Fixed, per unit (D-037) | Built |
| FTP | A family pool; pays Duos only, 2 each (D-035, D-036) | Built, differs (see [Family systems](family-systems.md)) |
| Family Roles | Free, with a limit per round: Linda 2, Lucy 3, Mark 1, John unlimited (D-036, D-042) | Planned |
| Campaign | 16 mission assets: M1–M14 (two M3s) and MX | Built |
| Character levels | 10 XP thresholds, one skill point each | Built |
| Home cycle | Prologue, then 7 days ending in the Warren | Demo |

Source: `Resources/Game Data.asset`, `Resources/GlobalSettings.asset`, `Content/Levels/M*.asset`, decisions D-035 to D-042.

## Areas and their state

| Area | Sub-doc | Design state | Branch | Checked |
| --- | --- | --- | --- | --- |
| Combat rules | [combat-rules](combat-rules.md) | Built | both | `main` @ `92853a5a9` (presets read) |
| Family systems | [family-systems](family-systems.md) | Built, differs (role limits planned) | both | `main` @ `92853a5a9` (presets read) |
| Characters | [john](characters/john.md) · [linda](characters/linda.md) · [lucy](characters/lucy.md) · [mark](characters/mark.md) · [toba](characters/toba.md) | Built | both | `main` @ `92853a5a9` (presets read) |
| Enemies | [enemies](enemies.md) | Built | both | `main` @ `92853a5a9` (presets read) |
| Progression and economy | [progression-economy](progression-economy.md) | Built (skill-tree values not play-checked) | both | `main` @ `92853a5a9` (presets read) |
| Missions and structure | [missions-structure](missions-structure.md) | Built (M8–M14 unreachable, not rebalanced) | both | `main` @ `92853a5a9` (level prefabs read) |
| Home | [home](home.md) → [Demo Spec](../demo-spec.md) | Built | `thj/home-test` | Demo Spec, 2026-10-16 (branch code not read) |
| Narrative and world | [narrative-world](narrative-world.md) | Proposed | all | `main` @ `92853a5a9` (briefings only) |

## Open design questions

The questions live in each sub-doc's "Open questions"; this list only points to them.

- Toba has no Family Role → [Family systems](family-systems.md#open-questions)
- The on-screen name for FTP → [Combat rules](combat-rules.md#open-questions)
- Whether Trio is a system of its own → [Family systems](family-systems.md#open-questions)
- How Family level and Family Skill Points are earned → [Progression and economy](progression-economy.md#open-questions)
- What else the Fireside can reward → [Home](home.md#open-questions)
- Children of Morta canon to confirm → [Narrative and world](narrative-world.md#open-questions)

## Document map

| Document | Holds | Owner |
| --- | --- | --- |
| This GDD (`design/gdd/`) | Rules and current values, by system | Game designer |
| [`vision.md`](../../vision.md) | Pillars, USPs, the feel | THJ |
| [`glossary.md`](../../glossary.md) | Names and terms, lore canon | Narrative agent |
| [`demo-spec.md`](../demo-spec.md) | Home demo rules and numbers | Coordinator |
| [`m9-readability.md`](../m9-readability.md), [`combat-balance.md`](../combat-balance.md), [`reward-balance.md`](../reward-balance.md), [`player-skill-trees.md`](../player-skill-trees.md) | Reasoning and history behind past passes | Game designer |
| [`decisions.md`](../../decisions.md) | Every decision, with its ID | Coordinator |
| [`tech/`](../../tech/) | How the systems work in code | Coordinator |
