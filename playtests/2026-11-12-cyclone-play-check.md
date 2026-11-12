# Cyclone redesign: THJ play check list (branch `thj/cyclone`)

Built back to back without per-chunk play (D-534). THJ plays everything here, then the commits are proposed. Collected from the chunk reports and reviews (`reports/cyclone-c1a*.md`, `cyclone-c1b*.md`, `cyclone-c2*.md`, ...).

## C1 · anchored Cyclone + Whirl
- Cast: range 3, only empty cells (cursor refuses units, planted entities); button off while hers is out; cooldown 4.
- Pips: 3, one lost at each family turn start; cast in round 1 → Whirls end of enemy turns 1–3, gone at round 4.
- Cross drawing (wind lines on arms, "3 ×" on touching cells), pips readable. Hovering the Cyclone shows no info panel (isTargetable off): OK?
- Whirl beat (swell → streaks → burst) on cast and after all enemies act; combat log "Whirl · Lucy: pulled N, hit M".
- Pull: 1 cell, nearest first, straight arms only; Masher/Deev/large units not pulled; pulls into hazards fire them.
- Watch fires on end-of-turn pulls, before the hit; Tempest Bloom split into freshly pulled enemies.
- Kill hand-back for Linda's grounded arrow on Whirl kills; sisters' tally counts a Whirl kill once; kill rewards now given.
- Masher next to the Cyclone does NOT counter Whirl hits (D-537).
- Super Time with her Cyclone out: Lucy's part skips (D-535); Super Time with none: lands on a valid cell.
- Pause during an end-of-turn Whirl: turn doesn't switch early (D-536).
- Two enemy factions → two Whirls a round (design edge); skipped enemy turn → no Whirl.
- Memory 4 Bloom stage (cast at 3,4) and the Lucy memory; the Trail levels (tuned for the old drifting Cyclone).

## C2 · walking + AI
- John/Linda/Mark/decoys walk through the Cyclone, can't stop on it; enemies can't; pushes stop before it.
- Blink (Lucy, John) and Mark's Vault/Primary never offer the Cyclone cell.
- Mark's dash on an enemy beside the Cyclone attacks from a side cell (preview + Command Shield Dash ghost); at full range with the Cyclone in front (may fall short; pre-existing with any blocker).
- Mark–Linda Duo where the loser's last step would be the Cyclone.
- Enemies with a way round end off the cross; step on an arm only to attack; 1-wide corridor: wait outside; AI log "Skipped: ends on dangerous ground…"; intent preview matches; Archer on an arm; large enemy near an arm. Open ground: enemies may wait diagonal-adjacent (design said 3+ away).
- Command Shield Dash when a family unit crosses the Cyclone cell.
