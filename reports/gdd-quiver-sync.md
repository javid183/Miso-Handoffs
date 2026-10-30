# GDD sync: Linda's Quiver on `main` (D-326)

Designer, 2026-10-29. Doc sync only, no new design. Everything is described as built on `main` @ `8c2e8617c`, checked against the decisions (D-241 to D-326, newest wins), the six plans and the code (read-only).

## Files and sections changed

- **`design/gdd/characters/linda.md`**: header (checked line); intro; top table (new Quiver row; Family Role row); Abilities table (new Encore row: 2 AP, cooldown 2) plus a line on which abilities spend; Source line (Encore asset, kits); **new section "Linda's Quiver"** with LI-3 to LI-11, LI-13, LI-14 (the IDs follow the design plan's numbering, which decisions already cite; LI-12, the Fireside arrow, isn't built and its ID stays reserved), a one-paragraph "what the player sees" and a Source line; Open questions Q2 answered, Q3 to Q6 new; Related (decisions, plan links).
- **`design/gdd/characters/mark.md`**: header; MA-3 rewritten (stop at Mark, press QTE, pressed vs not pressed, the quiver on and off, the planned Return to Sender); Source line (catch settings).
- **`design/gdd/characters/toba.md`**: header; Nature's Gambit row (a swap ends a move for both units, so it can trigger Watch); a line under the table on the Axe Dance kill hand-back.
- **`design/gdd/characters/lucy.md`**: header; Family Role row (only after real HP damage).
- **`design/gdd/family-systems.md`**: header; FR-2 (a target that dies during the prompt means the role is skipped, D-313); FR-4 (Linda's part superseded, D-244); FR-5 (Dropped while the quiver is on); FR-6 (a note); the Linda and Lucy rows of the role table; the Linda–Lucy Duo row (spends an arrow); the Mark–Linda Duo row (Arrow Chase planned, on hold); the Catch & Return synergy row; Branch differences (`thj/home-test` lacks the merge); Related.
- **`design/gdd/combat-rules.md`**: header; CR-6 (Encore's 2-AP exception, and the known limit that it can be cast with 1 AP); CR-28 (the catch QTE); **new CR-55** (projectile sweep, hit-once and end clamp); Source line; Branch differences.
- **`design/gdd/overview.md`**: game-at-a-glance (Family Roles row without Linda; a new Linda's Quiver row); the Areas table (checked notes); Open design questions (a pointer to Linda's).

No other design doc needed a status line. `glossary.md` was not touched.

## Could not confirm

- **Watch FTP:** I read the prefab's `requiredFTP` as constant 1 (with a `Stat_FPC` reference, base factor 2). I assumed constant mode applies, which matches D-246.
- **`Stat_LQuiverSize` base 3:** taken from D-319 and the plan's commit log, plus `size: 3` and `sizeStat` on `Unit_Linda.prefab`. I didn't trace the stat's base value through `StatAttributes.asset`.
- **`lindaQuiverEnabled` value in the asset:** the code default is on. THJ's local `GlobalSettings.asset` edits weren't read, so I wrote "default on in code".
- **Super Time Crescendo at 0 arrows (D-251):** taken from the decision; I didn't trace it in code.
- **Catch & Return on `thj/home-test`:** I wrote "pre-quiver, no stop at Mark", which is safe. I didn't check whether its catch was automatic or a QTE there.
- **Catch & Return open by default (D-177):** that decision was for onboarding. The `main` code still gates the catch on `_MarkLindaSynergy`, so the "Family tree" unlock text stays.
- **Pickup rule in play:** a unit that passes through an ally's cell doesn't pick up arrows there. This comes from the code comment, not from a play check.

## Found while syncing (for the coordinator)

- `Linda_Ability_Recall.asset` description still says "(1 AP, cooldown 2)"; Encore costs 2. Placeholder text: narrative or implementer (Linda Q6).

## Terms relied on (glossary, narrative agent's)

Quiver, grounded arrow, locked stack, hand-back (beat), Encore (code name Recall), Watch, Catch & Return, Return to Sender, Arrow Chase, Family Footrace, Nature's Gambit, Axe Dance, Sword Attack, `lindaQuiverEnabled` (quiver switch).

## Mirror tabs to sync ("Miso — Game Design")

Overview · Combat rules · Family systems · Characters › Linda · Characters › Mark · Characters › Toba · Characters › Lucy.
