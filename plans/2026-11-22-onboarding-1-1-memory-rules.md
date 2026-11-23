# Onboarding demo 1.1: memory rules

Size: M    Tier: 2 (new Pass-by level switch, data on a core prefab; D-610, D-614)    Assigned to: `miso-implementer` (opus)
Branch: `thj/onboarding-demo` (D-604)
Status: approved, in progress

## Why

Tweak doc items H-03, H-04, H-05, X-01, H-06, H-07 (parent plan `plans/2026-11-22-onboarding-demo.md`, Phase 1). In the four Hearth memories the player should not meet Revenge, Pass-by or Cleanse. The empty item bag should not show. Memories 3 and 4 should start with the family at full HP.

## Goal

In memories 1 to 4 (`GB_m1-linda`, `GB_m2-lucy`, `GB_m3-john`, `GB_m4-mark`): no Revenge, no Pass-by, no Cleanse button, no empty item bag, and full HP at the start of memories 3 and 4. Every other level behaves as before.

## Acceptance criteria

- [ ] No placed hero in memories 3 and 4 can cause Revenge (`GUnit.canCauseRevenge` off on the placed instances). Memories 1 and 2 have one hero each, so Revenge can't happen there; set it anyway if the tool makes that free.
- [ ] Pass-by never fires in any memory: no Pass-by FTP and no Pass-by feedback when a hero walks past or next to an ally. Pass-by works unchanged in every other level (a test proves the tag gate).
- [ ] Cleanse is not on any hero's ability bar in memories 1 to 4 (`LevelAbilityLock`). The corruption pools in memory 4 stay as they are (D-614).
- [ ] The item bag doesn't show in any memory: per placed hero `items[i].hideIfUsed` (D-610), or the closest per-level switch that hides a bag with no uses left. Other levels unchanged.
- [ ] Heroes start memories 3 and 4 at full HP (`minHpFractionOnLevelLoad` = 1 on the placed instances, D-610). Confirm it in Play or with a test of the restore rule.
- [ ] Memories 1 to 3 get these through their `HearthMemoryWiring.*` tools, so a re-run keeps them. Memory 4 is edited by hand in `GB_m4-mark.prefab` (it's the master, D-405; its `Run()` has no menu).
- [ ] Covering EditMode tests pass (the wiring tests for memories 1 to 3, a new Pass-by gate test, any memory 4 prefab test). Full EditMode suite green, because this touches a core prefab's data. The AI regression test is not run: no AI content changes.

## Scope

In: the five rules above, in the four memory levels only.
Out:
- Cleanse in the search levels and in M4. D-614 places Cleanse only in mission M4's first fight. The search levels and M4 are rebuilt in Phase 3, so they get it then.
- Any global HUD change.
- Any code change in a core system.

## Touches

Systems:
- `UnitsPassByHandler` (core): **data only**, a new tag in its `excludedTags` on `PlayerController.prefab`. No code change.
- The tag definitions (core data: one new tag).
- A new small level component, not core, that tags the heroes at level start.
- `HearthMemoryWiring.Linda/Lucy/John.cs`, `GB_m4-mark.prefab`, `LevelAbilityLock`, `GUnit` fields (data only).

USPs: Family Roles, Synergies (Pass-by fills FTP; off only in the memories).
Docs: GDD `family-systems.md` (Pass-by and Revenge are off in the memories), `missions-structure.md` memory rows (game designer, from the report); `tech/onboarding-merge.md` if it lists memory rules (coordinator).

## Findings to build on (Explore, 2026-11-22; verify before relying on them)

- **Heroes per memory:** M1 Linda only; M2 Lucy only; M3 John, Linda and Lucy; M4 four heroes. All are placed prefab instances.
- **Revenge:** `GUnit.canCauseRevenge` (`GUnit.cs:213`); read at `PlayerController.cs:1835`.
- **Pass-by:**
  - `UnitsPassByHandler` sits on `PlayerController.prefab` and has no on/off switch.
  - Disabling the component does not stop its listener (`:94-112`).
  - `excludedTags` currently holds `Status.Inactive` (prefab around line 2336).
  - **Plan:** add a new tag (a name like `Status.NoPassBy`; follow the existing tag naming) to the definitions and to `excludedTags`. Add a small level component, for example `LevelPassByOff` in the onboarding or level feature folder, that applies the tag to every family unit at level start and to any unit added later. Put it on the four memory prefabs.
  - First check whether `excludedTags` excludes the mover, the passed ally, or both, and tag accordingly.
  - If the tag can't stop Pass-by without a core code change, **stop and report**. That would be Tier 3.
- **Cleanse:** `LevelAbilityLock` matches by nickname.
  - M1: `HearthMemoryWiring.Linda.cs:270-290`, `arraySize=2`. Add Cleanse in the tool, or a re-run drops it.
  - M2: `Lucy.cs:238-256`.
  - M3: `John.cs:140-170`.
  - M4 already locks Cleanse for every hero (`GB_m4-mark.prefab:2275-2300`); just confirm it.
- **Item bag:**
  - Each hero prefab carries 2 items, and the Hearth has `initialItemsAvailability: []`, so the pouch shows with 0-use items (`AbilitiesBarHUDUI.cs:81`, `RuntimeItem.cs:12`).
  - Set per-instance `hideIfUsed = 1` on the placed heroes.
- **Heal:**
  - `minHpFractionOnLevelLoad` (`GUnit.cs:162`, base 0.2). The restore uses `Max(saved, current × fraction)` (around `:63`), and `persistHealthsThroughMission` is on.
  - Assumed: HP is already full when the restore runs. Verify.

## Approach

One chunk, one commit if it stays small. If the Pass-by tag needs more than data plus the new component, split it into its own commit (core data).

1. Pass-by switch: the tag, the component and an EditMode test showing a tagged unit is skipped and an untagged one still counts.
2. Wiring tools for memories 1 to 3: Revenge, Cleanse lock, item bag, heal (memory 3), the Pass-by component. Then run each Wire Memory menu.
3. Memory 4 by hand: the same fields in `GB_m4-mark.prefab`, with small YAML edits or an editor script. Never re-run a tool over it.
4. Tests, then the report.

## Risks

- New statics: none expected. If you add one, add a `PlayModeStaticReset` hook.
- Core prefab data: only `excludedTags` changes, so Pass-by elsewhere is untouched. Prove it with the test.
- `WiringSeed` never rewrites an existing step list. The tools set fields on hero instances, not step lists, so this should be fine. Say so in the report if a tool only applies to new assets.
- THJ's uncommitted files (leave them alone): `LevelM2-C1.prefab`, `GlobalSettings.asset`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`.

## Gates

- Compile with a clean console.
- Covering tests, then the full EditMode suite.
- `miso-reviewer` on this chunk alone (core prefab data).
- Every criterion checked with evidence.
- Play check: yes, batched with the other Phase 1 chunks.
- Docs as listed.
