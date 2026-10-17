# Family systems

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Family systems · Up: [Overview](overview.md)

The family fights as a family through four systems. Family Roles react on their own during anyone's turn. Duos are paired abilities the player chooses and pays FTP for. Synergies fire automatically when two members line up. Pass-by lets members tag each other while moving. On `thj/home-test`, Bond earned at Home unlocks some of them.

| System | Player chooses it? | Designed cost and limit | On `main` today | Status |
| --- | --- | --- | --- | --- |
| Family Role | No: it triggers, the player presses a QTE | Free, a limit per round (D-036, D-042) | 1 FTP per use, no limit | Built, differs |
| Duo | Yes | Activator's AP + 2 FTP (D-035) | 2 FTP (1 per partner; the check before use tests only 1). The activator pays 0 AP, or 1 in Mark–Lucy | Built, differs |
| Synergy | No: automatic | Free | Free | Built |
| Pass-by | Yes, through the move path | Free; fills FTP | Free; fills FTP | Built |

## Family Roles

- **FR-1.** John, Linda, Lucy and Mark each have one Family Role: a reactive passive that protects or supports the family. Toba has none (Q1). *Built*
- **FR-2.** A trigger shows a QTE prompt, "Activate Passive": a simple press within 1 s. Pressing fires the role and pays for it; a missed press skips the role and costs nothing (D-034). The game pauses during John's prompt; the others run in real time. Only one QTE can be up at a time. *Built.* A graded QTE (a small bonus for pressing inside the window) is the next experiment. *Planned*
- **FR-3.** Roles cost no FTP (D-036). *Planned.* Built today: 1 FTP per use on all four roles (`requiredFTP` 1).
- **FR-4.** Each role has a limit per round, refilled at the start of the player turn: Linda 2, Lucy 3, Mark 1, John unlimited (D-042). *Planned.* Built today: no limit (`oncePerPhase` 0).
- **FR-5.** Linda's two uses come from one pool, and the same enemy can trigger her more than once (D-041). *Planned*
- **FR-6.** The uses left this round are shown as **Watch** ("Watch 2/2"; Linda's are Watch Shots). *Proposed*

| Character | Trigger | Effect | Limit per round (design) | Status |
| --- | --- | --- | --- | --- |
| John | An enemy starts an action that targets a family member within 2 cells of John | The hit moves to John, who takes it × 0.5 (a fixed factor); the ally takes nothing | Unlimited, paid with his HP | Built (Q8) |
| Linda | An enemy *ends* a move in her row or column within her arrow's range (4 cells, up to 6 with Longshot); units in between don't block the lane; pushes and Command moves count (D-039) | She shoots it with her basic arrow (6 × damage, piercing) | 2, one pool | Built, differs (no limit yet) |
| Lucy | A family member finishes an action (not Lucy, not the Linda–Lucy Duo) | She fires 2 sidewinder embers (3 × damage each) at one enemy within 3 cells that the action targeted or hit near, skipping an enemy she hit last | 3 | Built, differs (no limit yet) |
| Mark | An enemy's action hits a family member | He strikes back with Fist Blitz (8 × damage) if the attacker is within 2 cells | 1 | Built, differs (no limit yet; check whether the cooldown already gives 1, D-042) |

Source: `Features/Player/<Name>/Scripts/<Name>FactionRoleHandler.cs`, `Core/Interactions/Runtime/PlayerController.cs` (prompt, pause, charge on success); the role component on `Features/Player/<Name>/Prefabs/Unit_<Name>.prefab` (cost, limit, QTE, John's `receivedDamageModifier`, Lucy's blacklist). Role presets under `Resources/UnitSpecific/Player/`: `John/FactionRole/John_Ability_FR_Shield.asset` (radius 2, held to 1–2 whatever its upgrade rows say), `Linda/Faction Role/Linda_Ability_FactionRole.asset`, `Lucy/FactionRole/Lucy_Ability_FactionRole.asset`; Mark's role uses his Fist Blitz preset. Linda's trigger is `OnUnitEndMoving` (`LindaFactionRoleHandler`).

## Duos

- **DU-1.** A Duo is a deliberate paired ability started by one partner, who needs at least 1 AP left. By design the activator spends AP; as wired, the activator pays its partner preset's cost: 0 AP in six Duos, 1 AP in Mark–Lucy. The cooldown applies to both partners (`cooldownForAll` on). *Built, differs* (Q10)
- **DU-2.** A Duo costs 2 FTP (D-035). *Built, differs:* each partner pays its entry's `fPCost` of 1, so 2 in all, but the check before use tests only 1 per partner (a known bug, [`plans/2026-10-16-ap-points-model.md`](../../plans/2026-10-16-ap-points-model.md)).
- **DU-3.** A Duo is offered only when both partners are in the squad. *Built*
- **DU-4.** Some partners get a QTE. A mash QTE scales the effect between ×0.7 and ×1.5; a time-window QTE adds one extra (a decoy, a turn of Vulnerable). *Built*
- **DU-5.** Lever: raise the cost to 3 FTP if FTP stays above 4 at the end of fights (D-035). *Proposed*

| Duo | ID | What it does (data title) | QTE | Cooldown | Partners act together | Unlock | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| John–Linda | `John_Linda_Duo` | **John-Linda Dance.** John moves to a cell within 4 (5 or 6 with the Dance node) and Linda moves the mirrored offset at the same time; a held key flips the mirror, and the player can cycle paths | None | 2 | Yes | Open | Built |
| John–Lucy | `John_Lucy_Duo` | **Hide and Seek.** 2 decoys (3 or 4 with the Hide and Seek node) appear on free cells within 2 of Lucy and John, about half around each | Lucy: time window, 2 cycles, hit at 0.7–0.9 → +1 decoy | 3 | No | Open | Built |
| Linda–Lucy | `Linda_Lucy_Duo` | **Marks-Sisters.** Linda fires a fire arrow along a row or column (5 cells) that pierces: 12 × damage to every enemy, with no falloff (×1.2 or ×1.35 with the Marks-Sisters node) | Linda: mash → damage ×0.7 to ×1.5 | 2 | No | Open | Built |
| Linda–Toba | `Linda_Toba_Duo` | **Healing Marks.** The same piercing arrow, charged by Toba: 12 × damage to enemies, and every Bergson in the line, Linda included, heals 10 × `Stat_WIS` (×1.5 or ×2 with the Healing Marks node) | Linda: mash → WIS ×0.7 to ×1.5 | 2 | No | **On `thj/home-test`:** Bond L2 (D-010) | Built |
| Mark–Lucy | `Mark_Lucy_Duo` | **Chained Assault.** Up to 3 targets within 4: Lucy fires a sidewinder at each (3 × damage) and Mark's ghost strikes each, nearest first (8 × damage); ×1.2 or ×1.35 with the Chained Assault node | Lucy: mash → damage ×0.7 to ×1.5 (Mark's hits too) | 2 | No | Open | Built |
| Mark–Linda | `Mark_Linda_Duo` | **Family Footrace.** A race to a point within both runners' reach. The winner deals ×1.5 damage until their next basic attack (or 1 turn); the loser gets +1 AP; both basic attacks reset (Q11) | None | 2 (1 with Head Start) | Yes | Open | Built |
| Mark–John | `Mark_John_Duo` | **Family Watchers.** A shout: every enemy within 3 cells of Mark or of John (4 or 5 with the Family Watchers node) becomes Vulnerable for 2 turns; no damage | Mark: time window, 2 cycles, hit at 0.1–0.3 → +1 turn of Vulnerable | 2 | Yes | Open | Built |

Source: `Content/Controllers/PlayerController.prefab` (`UnitsCooperationHandler`: entries, `fPCost`, QTE profiles, `markLindaRaceBonus` ×1.5); `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs` (AP, cooldown sharing, decoys, race, shout); trigger presets `Resources/Abilities/Cooperation/<A>_<B>/Trigger/<A>_<B>_Duo_Ability.asset` and their partner presets (cooldowns, damage).

## Synergies

- **SY-1.** A Synergy is automatic and conditional, and costs nothing. *Built*

| Synergy | Between | When | Effect | Unlock | Status |
| --- | --- | --- | --- | --- | --- |
| Sisters' Rivalry | Linda, Lucy | One sister kills an enemy with a basic attack | The other gets +1 AP and her basic attack is ready again, at most once every 2 s (the reset adds nothing on `main`, Q11) | **On `thj/home-test`:** Bond L2 (D-010) | Built |
| Tempest Bloom | Linda, Lucy | Linda's basic arrow (also her role arrow) or the Linda–Lucy Duo arrow enters Lucy's Cyclone | The arrow splits into copies toward each neighbouring cell except back the way it came; each copy keeps the damage | Family tree; also a run upgrade (`LindaLucyCycloneSpreadUnlock`) | Built |
| Papa's Shelter | John, Lucy | Lucy stands next to John | Lucy is Sheltered and her basic attack gains a level (one more ember) | Open | Built |
| Shield Flare | John, Lucy | Lucy's fireball reaches John while his Shield Up is on | John absorbs it and launches copies along the four diagonals; each hits the first enemy within 2 cells | Open | Built |
| Command Shield Dash | John, Mark | A unit finishes a move made by Mark's Command | Press QTE on John ("Shield Dash"): a free Shield Dash | **On `thj/home-test`:** Bond L2 (D-010) | Built |
| Catch & Return | Mark, Linda | Linda's basic arrow reaches Mark from 2 or more cells away | Mark catches it and bounces it back | Family tree (`_MarkLindaSynergy`) | Built (Q9) |

Source: `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs` (on Linda and Lucy), `Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs`, `Features/Player/John/Scripts/JohnShieldRelay.cs` (pattern Diagonal, range 2), `Features/Player/John/Scripts/JohnPassiveAbility_CommandShieldDash.cs`, `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs` (`returnMode` BounceBack), `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs` (on `Cyclone.prefab`) and their components on the `Unit_*` prefabs.

Character passives that touch the family but belong to one character (Wrath, Blood Debt, Linda's First Move, Atman's Focus, Continuous Attack) live on the character sheets.

## Pass-by

- **PB-1.** When a Bergson moves through another Bergson's cell, the pass-by ability fires for that pair, once per pair per turn. Both units get it (`applyMode` Both). *Built*
- **PB-2.** Each unit in a pass-by adds 1 FTP, so a pair of John, Linda, Lucy or Mark adds 2. They share one pass-by ability; Toba has no entry (Q1), so a pair with Toba adds 1. Each unit also gives the other 0.3 ATB, which nothing spends with FTP. *Built (to check in play: [Combat rules](combat-rules.md) Q7)*
- **PB-3.** The player can cycle alternative move paths to route through allies. *Built*
- **PB-4.** **On `thj/home-test`:** a pair needs Bond L1 for its pass-by. Every pair starts at L1 except Toba's pairs other than Linda–Toba, so only those earn it (D-010). *Demo*

Source: `Content/Controllers/PlayerController.prefab` (`UnitsPassByHandler`: 4 entries, one preset, excluded tag `Status.Inactive`), `Features/Player/Shared/Abilities/TagFPFill/Bergson_PassBy_Ability_PointsFill.asset` (data title "Father's Resolve", copied).

## Deferred and dropped

| Item | State | Why | Decision |
| --- | --- | --- | --- |
| Bergson Time (pause the enemy turn and act) | Deferred; ATB-only code remains (key L) | Untested, adds complexity | D-038 |
| ATB as the role resource | Dropped; `main` switched to FTP in `92853a5a9` | Playtesters found it confusing | D-036 |
| Shared AP | Dropped; half-built code remains | Fixed AP already runs | D-037 |
| Toba–Mark Duo | Dropped | Linda–Toba became the showcase pair | D-008 |

## Branch differences

- **On `main`:** no Bond locks, so Sisters' Rivalry, Command Shield Dash and the Linda–Toba Duo are open from the start. Roles pay 1 FTP; before `92853a5a9` they paid 1 ATB step.
- **On `thj/home-test`:** roles pay 1 FTP until the role limits are built on `main` and merged (D-042). Bond locks are active (`HomeLockRules`).

## Open questions

1. **Q1.** Toba has no Family Role and no pass-by entry. Is that intended for the newcomer, or missing?
2. **Q2.** The Mark–Lucy Duo's name: Fist Blitz (glossary) or Chained Assault (combat balance notes)? The other Duos need player-facing names too.
3. **Q3.** Linda's trigger. Answered from the data: an enemy that *ends* its move in her lane (the glossary's rule), pushes and Command moves included. Close, or did the balance notes' "any move into it" mean a change?
4. **Q4.** Are Papa's Shelter and Shield Flare Synergies, or character passives?
5. **Q5.** Revenge (on an ally's death) and Family Super Time exist in code. Do they belong here?
6. **Q6.** The pillars mention "trio abilities", and the family tree has a Trio group. Is Trio a system of its own?
7. **Q7.** Mark's Continuous Attack still costs FTP (1, then +1 per use in the same turn). D-036 keeps FTP for Duos. Make it free with a limit, or keep the cost?
8. **Q8.** John's redirected hit: the data uses a fixed ×0.5 (the role preset's 0.3 / 0.2 / 0.1 rows and its radius upgrades are read by nothing); the 2026-10-08 notes say 0.4. Which is intended, and should the role upgrade?
9. **Q9.** Catch & Return on `main` bounces the arrow back without the +1 AP refund (`returnMode` BounceBack). Intended?
10. **Q10.** Duos cost the activator 0 AP, except Mark–Lucy (1), because the partner presets are free. Should every Duo cost the activator 1 AP as designed?
11. **Q11.** Basic attacks have no cooldown on `main`, so rewards that make a basic attack "ready again" (Sisters' Rivalry, the Footrace, Father's Resolve, Revenge) add nothing. Give basic attacks a cooldown, or change the rewards?

## Related

- Decisions: D-008, D-010, D-034 to D-042
- Plan: [`plans/2026-10-16-ap-points-model.md`](../../plans/2026-10-16-ap-points-model.md)
- Detail: [`combat-balance.md`](../combat-balance.md) (Linda's damage share), [`player-skill-trees.md`](../player-skill-trees.md) (family tree), [Demo Spec](../demo-spec.md) (Bond)
- Characters: [John](characters/john.md) · [Linda](characters/linda.md) · [Lucy](characters/lucy.md) · [Mark](characters/mark.md) · [Toba](characters/toba.md)
- Code: [`tech/mechanics-brief.md`](../../tech/mechanics-brief.md) §0 and §3
