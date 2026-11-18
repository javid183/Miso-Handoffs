# Play check: Catch & Return offer (C1 + C2)

Branch `main` @ `2cf617358`. Needs THJ (Linda, Mark, the Mark-Linda synergy unlocked, Linda's quiver on). Aim Linda's shot along a line with Mark 2+ cells away on it. Note any wrong thing; each row says what you should see.

| # | Setup | While aiming | After firing |
| --- | --- | --- | --- |
| 1 | Enemy only past Mark | no `>>>` on Mark, no pink bars; normal shot bars on the enemy | no prompt; the arrow flies past Mark and hits |
| 2 | Enemy between Linda and Mark | `>>>` on Mark, pink return bar on the enemy | prompt appears; catching hits the enemy on the way back |
| 3 | Enemies between and past Mark | `>>>`, pink bars between, the past-Mark bars the normal red shot preview | prompt; catch = return hits only; miss = arrow flies on and hits the past-Mark enemies |
| 4 | No enemy on the line | nothing from the catch | no prompt, arrow flies on |
| 5 | Ally between, enemy past Mark | no catch drawing | no prompt |
| 6 | Tempest Bloom on, enemy hit by a copy off the lane | that enemy keeps the normal red shot preview (no pink: the return doesn't hit it) | catch: not hit; miss: hit |
| 7 | Cancel the aim, click elsewhere, end turn, switch ability | nothing stays pink, no chevron left | — |

Look at: do the red past-Mark bars next to the pink between-bars read clearly enough, or does the player still think the arrow will hit past Mark when it won't?
