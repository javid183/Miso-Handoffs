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

## C3 · Steer and Gust
- With her Cyclone out, the Cyclone button becomes Steer (same key); back to the cast after it fades. Steer right after a cast in the same turn (2 AP) is clickable.
- Steer: 1 AP, once a turn, up to 3 cells four-way, through the family, not through walls/enemies; ends only on an empty cell with no planted entity. Range highlight centred on the Cyclone.
- Gust at the destination: pull only, no numbers; inward streaks; log "Gust: pulled N"; Watch fires on a Gust pull on Lucy's turn.
- Preview: path, landing cell, ghosts for enemies the Gust moves (shows only after the cursor moves if it already sat on the cell).
- Mark's role doesn't answer a Steer; walk highlight doesn't flicker on the relocate; Tempest Bloom arrow during a Steer glide.
- Placeholders: Steer title/description/icon, cast animation and SFX reused.
- Character select: Steer is Lucy's 9th ability entry; check it doesn't show as a spare button.

## C4 · enemy ranged attacks
- Archers/Dark Shamans don't shoot through the Cyclone: no pick, no intent arrow, threat preview leaves those cells out; a corner graze is allowed (D-541), adjacent shots always allowed.
- Archers move to a cell with a clear line (new move filter); melee enemies behave as before.
- Linda's arrows still pass through and split; Toba/allied shooters unaffected.
- Dark Shaman with a Cyclone out still moves to heal or summon.
- A blocked Archer doesn't back off out of range when a cell with a clear line is reachable.
- Shamans with an ally in heal range don't reposition for a clear shot (support first, D-543).
