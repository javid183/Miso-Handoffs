# Review: preview-pass C5 (Shift model and tints)

Reviewer: miso-reviewer (saved by the coordinator). Verdict: **FIX**.

Must fix:
1. `ShowStatsHoverPreview.cs` `IsPlayerUnit` (~L145) / `PlanFor` (~L116): units allied to the player outside the player faction get the enemy model. `LevelBase.prefab` sets Bergsons–Neutral and Bergsons–Stranger to Ally; `Unit_Toba_Ally` (Neutral) is in Level1-C3; `Deer` (Neutral) is in several Level2 maps. `Unit_TobaEnemy` (Stranger) is hostile only via `LevelDomFight.prefab` overrides, so test the relation, not the faction id: `CombatLevel.Instance.GetFactionRelationToPlayer(unit.Faction) == FactionsRelationType.Enemy` → enemy model; anything else → Bergson model. Rename the `PlanFor` parameter to `isHostileToPlayer`, update the class summary and tests (add a non-hostile, unselected unit case).

Should fix (optional): dedupe ready attacks with identical reach specs (no gain on the measured case; only if C9 shows it); `DangerZone_CountsNextTurnCooldowns_WithoutSplash` only guards constants.

Notes: danger zone matches D-085; the selected-unit guard is safe; cleanup on release, exit and Rebind is correct (selection change mid-hold doesn't recompute: acceptable); D-071 mechanics unchanged; the core partial is additive and compiles alone (committed first); no mutable statics; encoding kept; AI untouched. Performance 1.3–3.9 ms one-off per press or hover accepted, profile in C9. C9: Shift-hover Toba in Level1-C3 and a Deer in a Level2 map.
