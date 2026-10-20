# Preview pass: role-badge tooltip line (D-080)

Tier 2, UI line in the established voice. Proposal only; no game file edited.

## Where it lives

The Family Role icon tooltip is `roleAbility.Preset.Title` + `roleAbility.Preset.Description` + `RoleBadgeTooltipSuffix(unit)` (`UnitPanelUI.cs:258`, `UnitPanelUI.RoleBadge.cs:66`). The suffix today is one extra line after `\n`, only in the NoFtp state: `"Needs 2 FTP; Pass-by refills FTP."` (`RoleBadgeRules.TooltipLine`). The new line should be another suffix line in the same style: short, mechanic first, semicolon join, full stop.

Player-facing text says "tiles" (Taunt, Footrace, Vault), so the line uses "tiles", not "cells".

## Options

| # | Scope | Proposed text | Feel |
|---|---|---|---|
| A (recommended) | Shared | `Same tiles as the basic attack; Shift shows them.` | Matches the FTP line's shape exactly; neutral, so it holds if Mark or John ever pass the runtime check |
| B | Shared | `Covers the same tiles as the basic attack. Hold Shift to see it.` | A little more explicit about the hidden zone; longer (two sentences) |
| C | Shared | `Answers on the basic attack's tiles; Shift shows them.` | Warmer verb ("answers" fits a reactive role), slightly less plain |
| L1 | Linda | `Watches the same tiles her bow covers; Shift shows them.` | Character colour; ties to the (proposed) Watch term without using it as a label |
| L2 | Linda | `Same tiles as her arrow; Shift shows them.` | Per-unit version of A |
| U1 | Lucy | `Answers on the same tiles as her embers; Shift shows them.` | Character colour, names her sidewinder embers |
| U2 | Lucy | `Same tiles as her attack; Shift shows them.` | Per-unit version of A; close to the placeholder |

## Recommendation

**Shared line, option A:** `Same tiles as the basic attack; Shift shows them.`

- Shared, not per-unit: D-080 is a runtime check with no new field, so a constant beside `RoleBadgeRules.TooltipLine` fits; a per-handler text field would be new data for a line that says the same thing for both. Per-unit lines (L1, U1) only earn their place if THJ wants character voice in the tooltip.
- Show the line only when the same check that hides the zone in `RoleZonePresenter` passes (from the unit's current cell), so the tooltip never claims a match that isn't there. It can sit alongside the FTP line (two suffix lines).
- Neutral wording avoids "her", so it survives if another unit's zone ever matches.

## Noticed, out of scope (for THJ)

- Linda's role preset still says `(1 FP)` (`Linda_Ability_FactionRole.asset`); per the glossary, Family Roles no longer cost FTP (intended design; code still charges). "FP" is also the older spelling of FTP.
- Role titles are dev labels: `Linda's FactionRole`, `Lucy's FR`. They show as the tooltip title. A naming pass is Tier 3.
