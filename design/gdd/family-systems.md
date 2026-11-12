# Family systems

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); [Role zones on the grid](#role-zones-on-the-grid) read from `thj/preview-improvements` @ `f5d263743`, 2026-10-20, now merged into `main`; Linda's and Lucy's role rows, FR-2, Catch & Return and the quiver notes from `main` @ `8c2e8617c`, 2026-10-29 (the `thj/linda-quiver` merge, D-326); the `thj/cyclone` notes (Lucy's Cyclone redesign) from its build reports C1b to C3, 2026-11-12 (not play-checked yet) · Mirror: Claude Doc "Miso — Game Design", tab Family systems · Up: [Overview](overview.md)

The family fights as a family through four systems. Family Roles react on their own during anyone's turn. Duos are paired abilities the player chooses and pays FTP for. Synergies fire automatically when two members line up. Pass-by lets members tag each other while moving. On `thj/home-test`, Bond earned at Home unlocks some of them; on `thj/bond-lite`, Bond Lite shuts three of the sisters' Family-tree nodes until their Bond reaches Lv 2 ([Bond](#bond)).

| System | Player chooses it? | Designed cost and limit | On `main` today | Status |
| --- | --- | --- | --- | --- |
| Family Role | No: it triggers, the player presses a QTE | Free, a limit per round (D-036, D-042) | 1 FTP per use, no limit | Built, differs |
| Duo | Yes | 0 AP + 2 FTP (D-219, amends D-035) | 2 FTP (1 per partner; the check before use tests only 1). The activator pays 0 AP, or 1 in Mark–Lucy | Built, differs |
| Synergy | No: automatic | Free | Free | Built |
| Pass-by | Yes, through the move path | Free; fills FTP | Free; fills FTP | Built |

## Family Roles

- **FR-1.** John, Linda, Lucy and Mark each have one Family Role: a reactive passive that protects or supports the family. Toba has none: he isn't officially part of the family yet (FR-7). *Built*
- **FR-2.** A trigger shows a QTE prompt, "Activate Passive": a simple press within 1 s. Pressing fires the role and pays for it; a missed press skips the role and costs nothing (D-034). The game pauses during John's prompt; the others run in real time. Only one QTE can be up at a time. If the role's target dies or is destroyed during the prompt (a Dark Worm splitting), the role is skipped cleanly and control comes back (D-313). *Built.* A graded QTE (a small bonus for pressing inside the window) is the next experiment. *Planned*
- **FR-3.** Roles cost no FTP (D-036). *Planned.* Built today: 1 FTP per use on all four roles (`requiredFTP` 1).
- **FR-4.** Each role has a limit per round, refilled at the start of the player turn: Linda 2, Lucy 3, Mark 1, John unlimited (D-042). *Planned.* Built today: no limit (`oncePerPhase` 0). **Linda's part superseded (D-244):** her quiver is her limit, with no per-round cap ([Linda](characters/linda.md) LI-11). With the quiver switched off there is no cap either: the switch is a test and merge tool (D-330, LI-14).
- **FR-5.** Linda's two uses come from one pool, and the same enemy can trigger her more than once (D-041). *Dropped* (D-244), with the quiver switch on or off (D-330); to reconsider after the playtest. The same enemy can still trigger her more than once, an arrow each time.
- **FR-6.** The uses left this round are shown as **Watch** ("Watch 2/2"; Linda's are Watch Shots). *Proposed.* Linda's count is now her quiver on her portrait ([Linda](characters/linda.md#lindas-quiver)), so the label would only serve Lucy and Mark. Note: "Watch" is now the approved short form of Linda's role name, Family Watch (D-328), so this label needs another word if it is built.
- **FR-7.** Toba gains a Family Role, and his own pass-by entry, when he officially becomes part of the family later in the game (D-048). He earns them as Bond grows (D-224). *Planned* (neither that moment nor his role is designed yet)

| Character | Trigger | Effect | Limit per round (design) | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| John | An enemy starts an action that targets a family member within 2 cells of John | The hit moves to John, who takes it × 0.5 (a fixed factor); the ally takes nothing | Unlimited, paid with his HP | Built, differs | ×0.5 is the base; tree upgrades lower it (e.g. 0.5 → 0.4 → 0.3) by wiring the preset rows (D-217) |
| Linda | An enemy *ends* a move in her row or column within her arrow's range (4 cells, up to 6 with Longshot); units in between don't block the lane. Pushes (John's Shield Dash included), Command moves and Toba's swap count (D-039, D-318, D-322). One swap that puts two enemies in her lines can trigger her twice, and an enemy Toba swaps with Linda herself can trigger her (D-323) | She shoots it with her basic arrow (6 × damage, piercing), spending an arrow; with an empty quiver she doesn't trigger ([Linda](characters/linda.md) LI-4, LI-5) | 2, one pool; superseded by her quiver (D-244) | Built, differs | No per-round cap: the quiver limits her (LI-11). **On `thj/cyclone`:** the Cyclone's pulls count like pushes: a Gust on Lucy's turn, a Whirl at cast and at the end of the enemy turn, where Watch fires after the pull and before the hit ([Lucy](characters/lucy.md) LU-4, LU-6; play check pending) |
| Lucy | A family member finishes an action (not Lucy, not the Linda–Lucy Duo) that took HP from at least one enemy | She fires 2 sidewinder embers (3 × damage each) at one enemy within 3 cells whose HP that action really lowered (the aimed one included), skipping an enemy she hit last. No follow-up on a hit blocked to 0, a status only, a miss or evade, a net heal, or an arrow Mark caught before it reached anyone (D-275, D-277). **On `thj/cyclone`:** none on a Cyclone Whirl hit, which is no one's action ([Lucy](characters/lucy.md) LU-5) | 3 | Built, differs | No limit yet. The real-damage rule is on `main` since 2026-10-29 (D-326) |
| Mark | An enemy's action hits a family member | He strikes back with Fist Blitz (8 × damage) if the attacker is within 2 cells | 1 | Built, differs | No limit yet; check whether the cooldown already gives 1 (D-042) |

Source: `Features/Player/<Name>/Scripts/<Name>FactionRoleHandler.cs`, `Core/Interactions/Runtime/PlayerController.cs` (prompt, pause, charge on success); the role component on `Features/Player/<Name>/Prefabs/Unit_<Name>.prefab` (cost, limit, QTE, John's `receivedDamageModifier`, Lucy's blacklist). Role presets under `Resources/UnitSpecific/Player/`: `John/FactionRole/John_Ability_FR_Shield.asset` (radius 2, held to 1–2 whatever its upgrade rows say), `Linda/Faction Role/Linda_Ability_FactionRole.asset`, `Lucy/FactionRole/Lucy_Ability_FactionRole.asset`; Mark's role uses his Fist Blitz preset. Linda's trigger is `OnUnitEndMoving` (`LindaFactionRoleHandler`).

### Role zones on the grid

A role zone is the set of tiles where a Bergson's Family Role can answer (each handler's own range). The zones are display only: nothing here changes when a role fires. These rules are on `main` since the merge of `thj/preview-improvements` (2026-10-20).

- **FR-8.** Each Bergson's zone is drawn with its own icon, tinted with its role colour, in a fixed quadrant of every tile in the zone (of the footprint box when a multi-tile unit stands there), so four zones on one tile never overlap (D-075). Icon, quadrant and colour are set per unit on its role handler (table below). The colours are the ones set on the unit prefabs, THJ's own choice (D-091): John dark brown, Mark near-black, Lucy dark red, Linda at the code default. `showRoleZone` off hides that unit's zone, its cover marker and its tether (D-063, D-067). *Built*
- **FR-9.** When a zone is shown (D-064, D-077, D-087):
  - the selected Bergson's zone, except as FR-10 says;
  - holding Shift: every living Bergson's zone;
  - Shift and hovering a Bergson that has a zone: only that zone. Hovering Toba, an enemy or an empty tile keeps every zone;
  - hovering a unit's role badge (on the unit panel's Family Role icon): that unit's zone, drawn like the others, whether it is selected or not, with or without Shift.

  *Built* (the Shift narrowing is D-087, which restored the earlier rule after D-076 was tried)
- **FR-10.** Without Shift, the selected Bergson's zone is not drawn when it is the same tiles as its basic-attack reach from the tile it stands on, leaving its own tiles out of the comparison (D-080). Today that hides Linda's and Lucy's. A zone that is only the unit's own tiles is never hidden, and the check applies to player units only. Shift and the badge hover still show it. While the check holds, the role badge tooltip adds the line "Same tiles as the basic attack; Shift shows them." (D-084). It is checked live, so if a run upgrade ever makes the zone differ from the attack, the zone comes back by itself. *Built*
- **FR-11.** Follow zone: while the player previews a move for any Bergson, its current zone is hidden and its zone is drawn from the ghost tile instead, in the normal style (D-082). The follow zone is skipped when it equals the basic-attack reach from the ghost tile (the FR-10 test), because the ghost's sword icons already show those tiles ([Combat rules](combat-rules.md) CR-37), so Linda and Lucy show no zone during a move preview. Other Bergsons' zones don't move. The current zone comes back on cancel, commit, death and turn end. *Built*
- **FR-12.** Cover marker: while the player previews a move for any other unit, the destination tile shows the coverer's own zone icon in its own quadrant, at full opacity (D-082): John's shield if the destination is in John's zone, Mark's fist only if every tile a melee attacker could hit the destination from lies in Mark's zone (D-067: ranged attackers don't count, and with no such tile there is no fist). Both are measured from where John and Mark stand now. A unit never covers itself. *Built*
- **FR-13.** John's tether: while John's role prompt is up (the game is paused), a thin arc in his role colour runs from John's head to the head of each ally he would cover, with a small shield (his zone icon) at the ally's end, drawn just above both units' sprites (D-081, D-088, D-089). It goes when the prompt ends (press, decline or expiry); an ally who dies or leaves the grid loses its arc. Values below. *Built*

| Bergson | Icon | Quadrant | Colour (RGBA) |
| --- | --- | --- | --- |
| John | `ShieldOutline` | Top left | 0.35, 0.24, 0.12, 0.75 |
| Mark | `PunchOutline` | Top right | 0.09, 0.04, 0.01, 0.75 |
| Linda | `BowArrow` | Bottom left | 0.34, 0.71, 0.91, 0.75 |
| Lucy | `Fireball` | Bottom right | 0.70, 0.14, 0.14, 0.75 |

| Tether value | Value |
| --- | --- |
| Width | 0.025 world units |
| Opacity | 0.85 |
| Arc | Quadratic curve, 16 samples; control height 1 + 0.15 per tile between John and the ally (radial), so the peak is half that above the chord |
| Anchors | Each unit's head (its `ThreatLineRenderer` point, 0.8 above the pivot) |
| Look | Plain unlit material (`Sprites/Default`); the threat arc's `M_LineShine` turned John's colour near-black (D-088) |
| Draw order | The units' sorting layer, one above the highest sprite of John and that ally; the cap one above the line |
| Cap | John's zone icon, 0.25 world units wide |

Source: `Unit_<Name>.prefab` (role handler: `roleZoneSprite`, `roleZoneSlot`, `roleZoneColor`, `showRoleZone`; the code defaults in `<Name>FactionRoleHandler.cs` differ for John, Mark and Lucy), `Resources/GridOverlays/*.png`, `Core/Systems/RoleZoneSystem/Runtime/` (`RoleZoneRules.cs`, `RoleZonePresenter.cs`, `RoleZoneAttackMatch.cs`, `MovePreviewCoverPresenter.cs`, `CoverIconRules.cs`, `JohnTetherPresenter.cs`), `Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs`, `Features/UI/Panels/Scripts/RoleBadgeState.cs` and `UnitPanelUI.RoleBadge.cs`. How it is wired: [`tech/combat-architecture.md`](../../tech/combat-architecture.md) "Grid previews".

## Duos

- **DU-1.** A Duo is a deliberate paired ability started by one partner, who needs at least 1 AP left. Every Duo costs the activator 0 AP: FTP only (D-219, amending D-035). As wired, the activator pays its partner preset's cost: 0 AP in six Duos, 1 AP in Mark–Lucy. The cooldown applies to both partners (`cooldownForAll` on). *Built, differs* (Mark–Lucy drops to 0)
- **DU-2.** A Duo costs 2 FTP (D-035). *Built, differs:* each partner pays its entry's `fPCost` of 1, so 2 in all, but the check before use tests only 1 per partner (a known bug, [`plans/2026-10-16-ap-points-model.md`](../../plans/2026-10-16-ap-points-model.md)).
- **DU-3.** A Duo is offered only when both partners are in the squad. *Built*
- **DU-4.** Some partners get a QTE. A mash QTE scales the effect between ×0.7 and ×1.5; a time-window QTE adds one extra (a decoy, a turn of Vulnerable). *Built*
- **DU-5.** Lever: raise the cost to 3 FTP if FTP stays above 4 at the end of fights (D-035). *Proposed*

| Duo | ID | What it does (data title) | QTE | Cooldown | Partners act together | Unlock | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| John–Linda | `John_Linda_Duo` | **John-Linda Dance.** John moves to a cell within 4 (5 or 6 with the Dance node) and Linda moves the mirrored offset at the same time; a held key flips the mirror, and the player can cycle paths | None | 2 | Yes | Open | Built |
| John–Lucy | `John_Lucy_Duo` | **Hide and Seek.** 2 decoys (3 or 4 with the Hide and Seek node) appear on free cells within 2 of Lucy and John, about half around each | Lucy: time window, 2 cycles, hit at 0.7–0.9 → +1 decoy | 3 | No | Open | Built |
| Linda–Lucy | `Linda_Lucy_Duo` | **Marks-Sisters.** Linda fires a fire arrow along a row or column (5 cells) that pierces: 12 × damage to every enemy, with no falloff (×1.2 or ×1.35 with the Marks-Sisters node). Spends one of Linda's arrows, which lands at the end of the line (as Healing Marks; [Linda](characters/linda.md) LI-4, LI-6) | Linda: mash → damage ×0.7 to ×1.5 | 2 | No | Open. **On `thj/bond-lite`:** the Duo stays open; its Marks-Sisters node is shut until Bond Lv 2 (BO-4) | Built |
| Linda–Toba | `Linda_Toba_Duo` | **Healing Marks.** The same piercing arrow, charged by Toba: 12 × damage to enemies, and every Bergson in the line, Linda included, heals 10 × `Stat_WIS` (×1.5 or ×2 with the Healing Marks node) | Linda: mash → WIS ×0.7 to ×1.5 | 2 | No | **On `thj/home-test`:** Bond L2 (D-010) | Built |
| Mark–Lucy | `Mark_Lucy_Duo` | **Chained Assault.** Up to 3 targets within 4: Lucy fires a sidewinder at each (3 × damage) and Mark's ghost strikes each, nearest first (8 × damage); ×1.2 or ×1.35 with the Chained Assault node | Lucy: mash → damage ×0.7 to ×1.5 (Mark's hits too) | 2 | No | Open | Built |
| Mark–Linda | `Mark_Linda_Duo` | **Family Footrace.** A race to a point within both runners' reach. The winner deals ×1.5 damage until their next basic attack (or 1 turn); the loser gets +1 AP; both basic attacks reset, which becomes an AP refund (D-220) | None | 2 (1 with Head Start) | Yes | Open | Built. **On `thj/cyclone`:** the loser never stops on the Cyclone (CR-58). **Planned (D-268, D-271):** Arrow Chase replaces it; designed, on hold since the simplification (D-292 to D-294) |
| Mark–John | `Mark_John_Duo` | **Family Watchers.** A shout: every enemy within 3 cells of Mark or of John (4 or 5 with the Family Watchers node) becomes Vulnerable for 2 turns; no damage | Mark: time window, 2 cycles, hit at 0.1–0.3 → +1 turn of Vulnerable | 2 | Yes | Open | Built |

Source: `Content/Controllers/PlayerController.prefab` (`UnitsCooperationHandler`: entries, `fPCost`, QTE profiles, `markLindaRaceBonus` ×1.5); `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs` (AP, cooldown sharing, decoys, race, shout); trigger presets `Resources/Abilities/Cooperation/<A>_<B>/Trigger/<A>_<B>_Duo_Ability.asset` and their partner presets (cooldowns, damage).

## Synergies

- **SY-1.** A Synergy is automatic and conditional, and costs nothing. *Built*. Papa's Shelter and Shield Flare are Synergies, not character passives, because they involve another family member (D-214).

| Synergy | Between | When | Effect | Unlock | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Sisters' Rivalry | Linda, Lucy | One sister kills an enemy with a basic attack | The other gets +1 AP and her basic attack is ready again, at most once every 2 s (the reset adds nothing on `main`; it becomes an AP refund, D-220). **On `thj/bond-lite`:** +1 AP only, no cooldown reset (D-232); at most once per turn per sister, so up to 2 AP a turn between them (D-173, D-437); a kill while the other sister is at the AP cap keeps the use | **On `thj/home-test`:** Bond L2 (D-010). **On `thj/bond-lite`:** a Family-tree node on Lucy's tree, 1 FSP, shut until Bond Lv 2 (BO-4) | Built | Glossary spelling: Sister's Rivalry |
| Tempest Bloom | Linda, Lucy | Linda's basic arrow (also her role arrow) or the Linda–Lucy Duo arrow enters Lucy's Cyclone | The arrow splits into copies toward each neighbouring cell except back the way it came; each copy keeps the damage | Family tree; also a run upgrade (`LindaLucyCycloneSpreadUnlock`). **On `thj/bond-lite`:** the node is shut until Bond Lv 2 (BO-4); the run upgrade still grants it | Built | **On `thj/cyclone`:** the split is unchanged. The Cyclone no longer moves on its own, so it stays in Linda's lane, and its Whirl pulls enemies onto the arms the copies fly down ([Lucy](characters/lucy.md) LU-4). Enemy shots, not family ones, are stopped by it (CR-57) |
| Papa's Shelter | John, Lucy | Lucy stands next to John | Lucy is Sheltered and her basic attack gains a level (one more ember) | Open | Built | |
| Shield Flare | John, Lucy | Lucy's fireball reaches John while his Shield Up is on | John absorbs it and launches copies along the four diagonals; each hits the first enemy within 2 cells | Open | Built | |
| Command Shield Dash | John, Mark | A unit finishes a move made by Mark's Command | Press QTE on John ("Shield Dash"): a free Shield Dash | **On `thj/home-test`:** Bond L2 (D-010) | Built | **On `thj/cyclone`:** a Cyclone pull is not a Command move (the synergy listens only while a Command is in flight; read in code, play check pending). The dash never stops on the Cyclone: it attacks from the nearest standable cell next to the target ([Combat rules](combat-rules.md) CR-58, D-538) |
| Catch & Return | Mark, Linda | Linda's bow or Watch arrow reaches Mark from 2 or more cells away | The arrow stops at Mark and a press QTE offers the catch. Pressed: a damaging return copy flies back to Linda and the arrow goes back into her quiver; nothing behind Mark is hit. Not pressed: the arrow flies on ([Mark](characters/mark.md) MA-3, [Linda](characters/linda.md) LI-9) | Family tree (`_MarkLindaSynergy`) | Built | QTE since D-257/D-260 (on `main` since D-326). With the quiver off, the same catch without the arrow (D-315, D-320). Bounce only, no AP refund: a refund could loop (Linda fires and spends an AP, Mark returns the arrow with a new AP, and so on); fix the node text (D-218); Return to Sender planned (D-228) |

Aim preview: Tempest Bloom, Shield Flare and Catch & Return each show their effect on the board while the shot is aimed ([Combat rules](combat-rules.md) CR-56). Tempest Bloom makes three copies (the three neighbouring cells other than back the way the arrow came) and never sends one back toward Linda.

Source: `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs` (on Linda and Lucy), `Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs`, `Features/Player/John/Scripts/JohnShieldRelay.cs` (pattern Diagonal, range 2), `Features/Player/John/Scripts/JohnPassiveAbility_CommandShieldDash.cs`, `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (`returnMode` BounceBack), `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs` (on `Cyclone.prefab`) and their components on the `Unit_*` prefabs.

Character passives that touch the family but belong to one character (Wrath, Blood Debt, Linda's First Move, Atman's Focus, Continuous Attack) live on the character sheets.

## Revenge

- **RV-1.** When a family member dies, each other living member takes Revenge after a short beat: for 2 turns, ×1.5 damage, +20% crit chance, +1 AP and +1 to the AP cap, plus a ready basic attack (which adds nothing on `main`: basic attacks have no cooldown; it becomes an AP refund, D-220). The values are the same for John, Linda, Lucy and Mark; Toba neither gives nor takes Revenge. *Built* Moved from [Combat rules](combat-rules.md) CR-25 (D-208).

## Pass-by

- **PB-1.** When a Bergson moves through another Bergson's cell, the pass-by ability fires for that pair, once per pair per turn. Both units get it (`applyMode` Both). *Built*
- **PB-2.** Each unit in a pass-by adds 1 FTP, so a pair of John, Linda, Lucy or Mark adds 2. They share one pass-by ability; Toba has no entry until he becomes family (FR-7), so a pair with Toba adds 1. Each unit also gives the other 0.3 ATB, which nothing spends with FTP. *Built* (to check in play, then fix: [Combat rules](combat-rules.md) CR-11, D-210)
- **PB-3.** The player can cycle alternative move paths to route through allies. *Built*
- **PB-4.** **On `thj/home-test`:** a pair needs Bond L1 for its pass-by. Every pair starts at L1 except Toba's pairs other than Linda–Toba, so only those earn it (D-010). *Demo*

Source: `Content/Controllers/PlayerController.prefab` (`UnitsPassByHandler`: 4 entries, one preset, excluded tag `Status.Inactive`), `Features/Player/Shared/Abilities/TagFPFill/Bergson_PassBy_Ability_PointsFill.asset` (data title "Father's Resolve", copied).

## Bond

Bond Lite, **on `thj/bond-lite` only** (D-422, D-423). The full Bond of the Home demo is on `thj/home-test` ([Home](home.md) HO-6, PB-4); Bond Lite uses the same names and thresholds so it folds into it later. Plan: [`plans/onboarding/2026-10-26-bond-lite-tech.md`](../../plans/onboarding/2026-10-26-bond-lite-tech.md).

- **BO-1.** Each pair of family members has a saved Bond score. Levels are reached at 10, 25 and 45 points (Lv 1, 2, 3). Linda–Lucy start at 15 (Lv 1); other pairs at 0 (D-233). *Built*
- **BO-2.** Sources: a mission's **first** completion gives 5 to each pair in the mission's squad (D-427); help between a pair gives 1 per event, at most 3 per pair per mission: Sister's Rivalry, a Duo between them, and John's Family Role covering the other (the other roles don't name the helped ally, D-428); a Home activity gives 5 (the Yard scene). Finishing the Hearth gives none (D-426). Bond is never added during combat: help is tallied and paid once at mission complete, so a failed or restarted mission gives nothing (C3 constraint). The arc: 15 at start, 20 to 23 after The Trail, the Yard crosses 25. *Built*
- **BO-3.** Bond shows only in two places: the locked node's line in the skill-tree description ("Opens with Linda & Lucy's Bond, Lv 2"), and the staged Yard scene after The Trail: The Trail's Home visit has its own Home state (Lucy training in the yard, Linda near), the camera moves to the yard, and after Y12-6 the scene says "Linda & Lucy's Bond reached Lv 2.", then Margaret gives the Family skill point and points at the sisters' nodes; the spend is free (D-425, D-433, D-436). No meter (D-231 stands). The Yard plays once per save. *Built* (the Yard staging is in build, C4)
- **BO-4.** Bond gates Family-tree nodes only; combat reads no Bond (D-202). Linda & Lucy's Bond Lv 2 opens three nodes on Lucy's tree: Sister's Rivalry, Tempest Bloom and Marks-Sisters (D-173, D-424). The Linda–Lucy Duo itself stays open; the Marks-Sisters node upgrades it (D-441). Command Shield Dash and the Linda–Toba Duo stay open. *Built*

Source: `Resources/BondSettings.asset` (thresholds, start, source values, no-Bond missions, help synergies), `Core/Systems/HomeSystem/Runtime/BondLite/` (`BondStore`, `BondSettingsSO`, `HomeLockRules`, `BondSources`), `Features/Onboarding/BondActivitySequence.cs` (the Yard's step), `Features/Onboarding/Editor/HomeVisitsWiring*.cs` (the Yard chain); read from the Bond Lite reports C1 to C5, 2026-11-06 to 2026-11-07, not from a fresh asset pass.

## Deferred and dropped

| Item | State | Why | Decision | Notes |
| --- | --- | --- | --- | --- |
| Bergson Time (pause the enemy turn and act) | Deferred | Untested, adds complexity | D-038 | ATB-only code remains (key L) |
| ATB as the role resource | Dropped | Playtesters found it confusing | D-036 | `main` switched to FTP in `92853a5a9` |
| Shared AP | Dropped | Fixed AP already runs | D-037 | Half-built code remains |
| Toba–Mark Duo | Dropped | Linda–Toba became the showcase pair | D-008 | |
| Family Super Time | Deferred | Like Bergson Time: the code stays, out of the design for now | D-207 | `main` fires it once, on the Goblin Queen's death ([Combat rules](combat-rules.md) CR-14) |
| Trio abilities | Deferred | A later system of its own | D-215 | The family tree's Trio group stays as a placeholder |

## Branch differences

- **On `main`:** no Bond locks, so Sisters' Rivalry, Command Shield Dash and the Linda–Toba Duo are open from the start. Roles pay 1 FTP; before `92853a5a9` they paid 1 ATB step.
- **On `thj/bond-lite`:** Bond Lite (BO-1 to BO-4): Sister's Rivalry, Tempest Bloom and Marks-Sisters are Family-tree nodes shut until Linda & Lucy's Bond Lv 2; Rivalry is +1 AP once per turn per sister. Command Shield Dash and the Linda–Toba Duo stay open.
- **On `thj/cyclone`:** Lucy's Cyclone redesign ([Lucy](characters/lucy.md#cyclone-pulling-gale) LU-3 to LU-7): Watch answers its pulls, Lucy's follow-up ignores its Whirl hits, Command Shield Dash ignores its pulls, and dashes and the Footrace loser never stop on it. Otherwise as `main`.
- **On `thj/home-test`:** roles pay 1 FTP until the role limits are built on `main` and merged (D-042). Bond locks are active (`HomeLockRules`). It doesn't have the `thj/linda-quiver` merge yet (D-326): no quiver, the pre-quiver Catch & Return (no stop at Mark), Lucy's follow-up without the real-damage rule, and no Watch on Toba's swap.
## Open questions

1. **Q1.** Answered by THJ (D-048): Toba has no Family Role and no pass-by entry on purpose. He isn't officially part of the family yet, and gains both when he becomes family later in the game (FR-7). Not designed yet. Refined (D-224): he earns them as Bond grows.
2. **Q2.** Duo names. THJ: the Mark–Lucy Duo is Chained Assault for now (the glossary's "Fist Blitz" is out of date). No Duo name is final: some have names on their assets, and all need a narrative pass toward a family theme; for Mark–Lucy, a name that reflects the two of them. Open to suggestions.
3. **Q3.** Linda's trigger. Answered from the data: an enemy that *ends* its move in her lane (the glossary's rule), pushes and Command moves included. Close, or did the balance notes' "any move into it" mean a change? **Answered:** close: ends-in-lane, pushes and Command moves included (D-039 stands; D-213).
4. **Q4.** Are Papa's Shelter and Shield Flare Synergies, or character passives? **Answered:** Synergies, because they involve another family member (D-214).
5. **Q5.** Revenge (on an ally's death) and Family Super Time exist in code. Do they belong here? **Answered:** Revenge belongs here (RV-1, D-208); Family Super Time is deferred (D-207).
6. **Q6.** The pillars mention "trio abilities", and the family tree has a Trio group. Is Trio a system of its own? **Answered:** yes, a later system: deferred, the Trio group stays as a placeholder (D-215).
7. **Q7.** Mark's Continuous Attack still costs FTP (1, then +1 per use in the same turn). D-036 keeps FTP for Duos. Make it free with a limit, or keep the cost? **Answered:** make it free, with a per-turn limit (value not set); FTP is for Duos only (D-216).
8. **Q8.** John's redirected hit: the data uses a fixed ×0.5 (the role preset's 0.3 / 0.2 / 0.1 rows and its radius upgrades are read by nothing); the 2026-10-08 notes say 0.4. Which is intended, and should the role upgrade? **Answered:** ×0.5 base, lowered by tree upgrades; wire the preset rows (D-217).
9. **Q9.** Catch & Return on `main` bounces the arrow back without the +1 AP refund (`returnMode` BounceBack). Intended? **Answered:** bounce only, as built; fix the node text. A refund could loop (D-218).
10. **Q10.** Duos cost the activator 0 AP, except Mark–Lucy (1), because the partner presets are free. Should every Duo cost the activator 1 AP as designed? **Answered:** no: every Duo costs 0 AP, FTP only; Mark–Lucy drops to 0 (D-219, amends D-035).
11. **Q11.** Basic attacks have no cooldown on `main`, so rewards that make a basic attack "ready again" (Sisters' Rivalry, the Footrace, Father's Resolve, Revenge) add nothing. Give basic attacks a cooldown, or change the rewards? **Answered:** change the rewards: each "ready again" becomes an AP refund (D-220).
12. **Q12.** Answered by THJ (D-091): the prefab role colours are his own edits and stay (John dark brown, Mark near-black, Lucy dark red, Linda at the code default), superseding D-066's note on Mark's and Linda's colours (FR-8).

## Related

- Decisions: D-008, D-010, D-034 to D-042, D-048; Linda's Quiver and its family edges D-244, D-246, D-257, D-260, D-268, D-271, D-274, D-275, D-277, D-313, D-315, D-318, D-320, D-322, D-323, D-326; role zones D-063, D-064, D-066, D-067, D-075, D-077, D-080 to D-082, D-084, D-087 to D-089, D-091 (D-076 reversed by D-087; D-066's colour note superseded by D-091); Bond Lite D-173, D-202, D-231 to D-233, D-422 to D-428, D-433, D-436, D-437, D-441
- Plans: [`plans/2026-10-16-ap-points-model.md`](../../plans/2026-10-16-ap-points-model.md); role zones [`plans/2026-10-18-family-role-phase0-1.md`](../../plans/2026-10-18-family-role-phase0-1.md), [`plans/2026-10-19-preview-pass-design.md`](../../plans/2026-10-19-preview-pass-design.md), [`plans/2026-10-19-preview-pass-tech.md`](../../plans/2026-10-19-preview-pass-tech.md)
- Detail: [`combat-balance.md`](../combat-balance.md) (Linda's damage share), [`player-skill-trees.md`](../player-skill-trees.md) (family tree), [Demo Spec](../demo-spec.md) (Bond)
- Characters: [John](characters/john.md) · [Linda](characters/linda.md) · [Lucy](characters/lucy.md) · [Mark](characters/mark.md) · [Toba](characters/toba.md)
- Code: [`tech/mechanics-brief.md`](../../tech/mechanics-brief.md) §0 and §3
