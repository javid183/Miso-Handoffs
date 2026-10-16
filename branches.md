# Branches

Owner: coordinator; THJ approves. `claude-handoff/` doesn't change when the shared repo switches branches, so this file says what's different on each active branch.

**Rules**

- Every task, backlog item and decision is scoped `all` or to one branch.
- Active work = everything scoped `all` + everything scoped to the current branch. Work scoped to another branch is parked.
- A design rule that differs is written once in its design doc, with its variant: "**On `thj/home-test`:** ...".
- Agents never switch branches. THJ does.
- On merge, a branch's differences fold into `all`. If that changes a core rule on `main`, it's Tier 3.

## `main`

- Combat resource: **ATB** (`GlobalSettings.asset` `pointConsumptionMode: 1`).
- AP: PerUnit (`aPConsumptionMode: 1`), escalation `[1,1,2,4]`.
- Has the Morta rebuild export (`miso/Assets/MortaStory/`) and the skill-tree redesign, combat log, enemy tiers, Lucy + John shield relay (merged into `thj/home-test` in Steps J, K, L).
- No Home system.

## `thj/home-test`

- **Purpose:** the Home system demo (M0–M9 and playtest fixes). See `tech/home-system.md`.
- Combat resource: **FTP** (`pointConsumptionMode: 0`), because the Home demo writes its effects against FTP.
- New Home rules apply (see `design/demo-spec.md`).
- AP: PerUnit, same as `main`.
- Merges `origin/main` periodically through Claude Code; THJ commits. Merges so far: Step J `59a4f5cde` (Oct 3), Step K `182201e82` (Oct 4), Step L `5c8476822` (Oct 11).
- Committed, not pushed. Last commit `2f828e662` (Oct 15, playtest fixes 2).
- Home scene fallback after a merge: take `main`'s scene and re-run the builders (order in `CLAUDE.md`).
- **[THJ]** How and when is this expected to merge into `main`? Does FTP or ATB win on merge?
