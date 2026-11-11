# The sisters' Bond nodes: node text for `[6]` and `[7]`

Owner: miso-narrative. 2026-11-11. For `plans/2026-11-11-bond-tree-sisters-tech.md` C2 (D-520, D-521).
Status: **working text**, waiting for THJ's pick. Goes into `Unit_Lucy.prefab` with no placeholder tag (D-348); listed here as unfinished until THJ signs it off.

## Style read from the tree

- Duo nodes open with `[Duo]` and say who does what, in one sentence, with no cost or FP numbers: "[Duo] Mark and John shout together, exposing every enemy around them." (Mark), "[Duo] Linda's marked arrows heal allies with Toba's blessing." (Toba).
- Upgrade nodes have no tag and a short, plain line: "Lucy's Cyclone hits harder.", "Lucy can blink more often." Their titles are short and about the effect: Cyclone Power, Rapid Blink, Louder Crescendo.
- The pips already carry `upgradeDescription` "Each upgrade increases the duo's damage." on `[7]` (the same line as Mark's and Toba's Duo upgrades). Keep it.

## Proposed text

| Where | Current | Proposed (recommended) | Alternative | Notes |
| --- | --- | --- | --- | --- |
| `[6]` title | Tempest Bloom | **Marks-Sisters** | (none) | Fixed by D-521: the name moves to the Duo itself |
| `[6]` description | [Synergy] Hitting Lucy's cyclone with a Bergson's projectile makes it split and spread. | **[Duo] Lucy sets Linda's arrow alight, and it pierces through enemies along a row or column.** | [Duo] Linda looses an arrow her sister has set on fire, piercing through enemies down a row or column. | Recommended puts both sisters' names first, as the other Duo nodes do. The alternative leans warmer ("her sister") but hides Lucy's name. Neither claims Burn or "every enemy": I haven't checked the preset for either |
| `[6]` upgradeDescription | (empty) | (leave empty) | | Single-pip unlock node |
| `[7]` title | Marks-Sisters | **Fiercer Flame** | Sisters' Fire | Fiercer Flame: plain upgrade title, like Cyclone Power or Louder Crescendo. Sisters' Fire: warmer and about the pair, but sits close to the Duo's name and could be read as a second Duo (the D-441 misread the design note warns about). Avoided "Kindled" (Kindled Spirits is already on Lucy's tree) and "Burn" (a status name) |
| `[7]` description | Lucy and Linda combine their ranged skills into one powerful coordinated shot. | **The Marks-Sisters arrow hits harder.** | The sisters' fire arrow hits harder. | Recommended names the Duo, so the upgrade card points at the card it needs (the `[6]` → `[7]` edge). The alternative is friendlier to players who don't know the name yet |
| `[7]` upgradeDescription | Each upgrade increases the duo's damage. | (unchanged) | | Lower-case "duo" also appears on Mark's and Toba's nodes. Changing it to "Duo" means changing all three (separate, optional) |

## Glossary rows to change (proposed; not edited)

| Row | Today | Proposed change |
| --- | --- | --- |
| Duo | "Seven in code: John–Lucy, Linda–Lucy, ..." | Add the name: "Linda–Lucy (**Marks-Sisters**: Linda fires a piercing fire arrow along a row or column; a Family-tree node, 1 Family skill point, opens at Linda & Lucy's Bond, Lv 2, D-520)" |
| Synergy | "E.g. Sister's Rivalry (...), Tempest Bloom" | Tempest Bloom: "open by default, no node (D-519)" |
| Bond (Home terms) | "Lv 2 opens Sister's Rivalry and Tempest Bloom" | "Lv 2 opens the Marks-Sisters Duo node and Sister's Rivalry; the Duo's upgrade (<chosen name>) needs Marks-Sisters first (D-520, D-521)" |
| New row: **Marks-Sisters** | (none) | Names the Linda–Lucy Duo and its Family-tree node `[6]`. Before D-521 it named the damage upgrade node `[7]`: don't use it for the upgrade |
| New row: **<chosen `[7]` name>** | (none) | Family-tree node `[7]`, the Marks-Sisters damage upgrade: 2 pips, ×1.2 / ×1.35, 1 Family skill point each, needs Marks-Sisters |
