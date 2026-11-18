# Play check: Catch & Return offer (C1 + C2)

Branch `main` @ `2cf617358`. Needs THJ (Linda, Mark, the Mark-Linda synergy unlocked, Linda's quiver on). Aim Linda's shot along a line with Mark 2+ cells away on it. Note any wrong thing; each row says what you should see.

| # | Setup | While aiming | After firing |
| --- | --- | --- | --- |
| 1 | Enemy only past Mark | no `>>>` on Mark, no pink bars; normal shot bars on the enemy | no prompt; the arrow flies past Mark and hits |
| 2 | Enemy between Linda and Mark | `>>>` on Mark, pink return bar on the enemy | prompt appears; catching hits the enemy on the way back |
| 3 | Enemies between and past Mark | `>>>`, pink bars between, the past-Mark bars grey | prompt; catch = return hits only; miss = arrow flies on and hits the past-Mark enemies |
| 4 | No enemy on the line | nothing from the catch | no prompt, arrow flies on |
| 5 | Ally between, enemy past Mark | no catch drawing | no prompt |
| 6 | Tempest Bloom on, enemy hit by a copy off the lane | when the catch is offered, that enemy's bar is grey too | catch: not hit; miss: hit |
| 7 | Cancel the aim, click elsewhere, end turn, switch ability | nothing stays grey or pink | — |

Look at: does grey read as "lost if you catch"? (grey tint is `lostDecreaseColor` on the HP bar prefab, default 0.55.)
