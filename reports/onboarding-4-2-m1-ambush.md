# Report: M1 "The Ridge" change round 4.2 (rock animation fix, HP, ledge, ambush, potion page, lines)

Plan: plans/2026-11-24-m1-ridge-4-2-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (both chunks). Built and EditMode-tested; nothing checked in Play mode (no Play session was started in THJ's editor). One side effect to flag: the TextMesh Pro fallback asset was rewritten by Unity (see Findings 1).

## Built

### Chunk 4.2a: rock animation fix

- New `Features/NPCs/Rock/Animations/AC_NPC_Rock.controller` (+ `.meta`): one layer, one state named `Idle`, the default state, plus the `DirectionX`/`DirectionY` float parameters the animation handler sets on every unit.
- New `Features/NPCs/Rock/Animations/A_Rock_Idle.anim` (+ `.meta`): 1 s long, loop on, 12 fps. It keys `Body`'s `SpriteRenderer.m_Sprite` to the rock's current sprite (`CaveRock 01` sub-sprite) at t=0 and t=1.
- `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`: one new override, `m_Controller` on the body Animator (`Visual`, the one `EntityAnimationHandler.animator` points at). THJ's scale overrides (0.07 and 0.5) and every other override are unchanged.
- New partial `Features/Onboarding/Editor/MissionWiring.Ridge.Layout.Rock.cs`: `SyncRockAnimator`. It creates the clip and controller if missing, re-keys the clip if the body sprite changed, and sets the controller on the Animator only when it differs. `EnsureRockPrefab` (in `MissionWiring.Ridge.Layout.cs`, now `partial`) calls it for an existing prefab and for a freshly built one.
- Test: `M1RidgeLayoutTests.TheRockAnimatorPlaysALoopingIdleClipWithALength`.

### Chunk 4.2b: HP, ledge, ambush, potion page, lines

**Layout** (`MissionWiring.Ridge.Layout.cs` + new partial `MissionWiring.Ridge.Layout.Ambush.cs`):
- Pocket Claws (5,-2 and 5,-1) at 0.75; ledge Claw (7,-2) at 0.5.
- New hidden group `ambush`, placed once and then kept:
  - `Unit_BlackClaw` on 1,-1 at 0.45;
  - `Unit_DarkClaw` on 2,-1, 7,-1, 7,-3 and 7,-4 at 0.6;
  - each one inactive in the prefab, with an `EnemyAlertSettings` component added on the placed instance, `startsAlert` on.
- `SetClawHealth` (health by tile) now skips the ambush tiles. Their factors are set explicitly by the ambush code.
- `NameUnnamedCell`: the cell called `GridCell` is renamed `GridCell - (2, 3)`. The tile is read from its grid position, and the tool throws if an unnamed cell sits anywhere else. This runs first in `Apply()`.

**Wiring** (`MissionWiring.Ridge.cs`, `MissionWiring.Ridge.Sequences.cs`):

| Stage | Shown text | Completes when | On complete |
|---|---|---|---|
| S1 | "Mark: reach the ledge." | Mark on prefab **7,-2 or 7,-3** (`UnitTileOccupied`, tile list), or the turn fallback (unchanged) | `M1Ridge_Catch_SequentialSequence` |
| S2 | hidden | the three fall Claws dead (unchanged) | `M1Ridge_Cleared_SequentialSequence`, **potion page removed** |
| S3 | "Clear the ridge. {alive_0} remaining." | Enemy living ≤ 0 (unchanged; the hidden pack isn't registered) | **new** `M1Ridge_ToClue_SequentialSequence` |
| S4 | "Reach the clue together." | **new** `TilesOccupied` Bergsons, `AtLeast` 2, allies excluded, on the 8 top-zone tiles (prefab 1..3,5 and 0..4,4). No turn fallback | **new** `M1Ridge_Ambush_SequentialSequence` |
| S5 | "Drive them off the ridge. {alive_0} remaining." | **new** Enemy living ≤ 0 | none (the level's outro on the win) |

- `M1Ridge_ToClue_SequentialSequence`: input off, then the camera from the plateau to the clue and the top zone, then N1, then input on.
- `M1Ridge_Ambush_SequentialSequence`, in this order:
  1. input off, HUD off;
  2. camera on the clue;
  3. discovery N3a–c and N4 (one dialogue);
  4. camera down the west path (1,-1 and 2,-1);
  5. `RevealUnitsSequence` for `ambush`;
  6. narrator caption N5 (`SearchWiringTrail.BlackClawCaption`, a TopNotification line);
  7. camera on the east path (7,-1, 7,-3, 7,-4);
  8. N6, N7, N8 (one dialogue);
  9. `SignalSequence` `M1Ridge_Reunion` (new asset `M1Ridge_Ambush_Reunion`, same signal);
  10. potion page (`M1Ridge_Ambush_PotionPage` → the existing `M1Ridge_Potion_Panels`);
  11. camera back on the top zone;
  12. input on, HUD on.
- Catch set-up: Mark's K1 only.
- Pocket cleared: P1–P3 (set A), then §5.4 onward unchanged.
- Outro: O1–O4 (close A).
- Potion page text: "carries" → "brought" (N9).

**One-off asset edits.** The wiring seeds dialogue and step lists only once (`WiringSeed`), so assets that already existed kept their old content. I edited them once, through `execute_code` in the editor, to match the new seed text in code:
- `M1Ridge_Cleared_SequentialSequence`: the `M1Ridge_Cleared_PotionPage` step was removed. The wiring had warned that the kept list differed; after the edit, the next run gave no warning.
- `M1Ridge_Catch_DialogNodeSequence`, `M1Ridge_Cleared_DialogNodeSequence` and `M1Ridge_Outro_Clue_DialogNodeSequence` were rewritten with the wiring's own `WriteLines`, called by reflection, so speakers, sides and delays match what a fresh build makes.

A fresh checkout builds the same from code.

## Verified

**Compile:** clean, no errors in the console.

**Tests** (open editor, Unity MCP):

| Run | Result |
|---|---|
| 4.2a: `M1RidgeTests` + `M1RidgeLayoutTests` + `SearchRidgeTests` | 46 run, 45 passed. The failure was `TheTilesAndUnitsMatchThePaperBlock`, a `FormatException` on THJ's unnamed cell. It was there before 4.2 and is fixed by 4.2b's rename. The new rock test passed |
| 4.2b: the same three classes | **52/52 passed** |
| Full EditMode suite | **2676 total, 2675 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit) |
| `AIRegressionTest.Baseline_MatchesCurrentAI` by name | **45 failures, the same count as recorded.** `Unit_Rock` still appears as "new unit prefab" (from 4.1a); no new line from the Black Claw or the rock controller. Not re-baselined |

**Idempotent:** after the one-off edits, two more runs of `Tools/Onboarding/The Ridge: Apply Layout and Wire` left every file byte-identical (md5): every `M1Ridge` sequence asset, the level, the mission, the rock prefab and its animations. The runs gave no warnings.

**Level read-back** (`level_to_grid.py`). Before the build it matched block `m1-ridge-thj-1124` exactly. After the build:

```
_ _ . . . _ _ _ _
. . c . c . c _ _
. . _ . . . _ _ _
. . . . . . . _ _
_ _ . . _ . . . _
_ _ . _ _ _ _ . .
_ _ b c . _ c _ c
_ _ _ _ . . c _ c
_ _ _ _ . _ _ _ c
_ _ _ _ . . _ . c
_ _ _ _ _ . L M _
--
note 6,0 Unit_Rock
level hidden fall 6,3 6,4 8,3
level hidden ambush 2,4 3,4 8,4 8,2 8,1
```

- 48 tiles, the same cell set as THJ's.
- Placed: 1 Black Claw, 10 Dark Claws, Linda, Mark, the rock.
- Objectives: the ledge, Clear, Reach the clue together, Drive them off.
- This matches `m1-ridge-3a`, unit for unit and hidden group for hidden group.
- The tool's line "group rock: a listed unit that is not a placed unit" was there before the build too: the tool doesn't resolve the rock's stripped reference.

**Prefab diff**, `GB_m1-ridge.prefab`:
- Against THJ's version before this build: **820 insertions, 23 deletions**.
- Every deletion is an expected one: three factor values (0.7, 0.7, 0.45), the cell name `GridCell`, the stage count 3, the ledge tile count 1, `m_AddedGameObjects: []` on the five cells that now hold an ambush unit, and diff realignment around one moved PrefabInstance block.
- Against HEAD (4.1 and 4.2 together): 1684 lines changed.
- `Unit_Rock.prefab`: +4 lines, the `m_Controller` override.

### Checks during the build

1. **A second Catch & Return in the same turn is offered: yes, by code; not played.**
   - `ProjectileCatchAndReturn.TryCatch` has no per-turn limit. It refuses only while a catch is in progress (`_qteActive`, freeze phase), for the same projectile twice (`_lastSeen`), or when the return wouldn't hit an enemy (`ReturnWouldHitEnemy`). The freeze rules reset after each catch.
   - So a second arrow from Linda (her second AP, bow cooldown 0) is offered if an enemy is still on the line and she has an arrow. The catch refunds it.
2. **An enemy turn with no living enemy ends cleanly, and nothing ends the level early: yes, by code; not played.**
   - `FactionControllerBase.CanPlayTurn` is false with no live unit, so `SwitchTurnIE` skips the Enemy faction, as it does the Neutral rock.
   - `LevelObjectives.TryEvaluateWin` advances one queued stage per evaluation. While the next stage's on-complete sequence plays, `UpdateObjectives` is held by `_newStageEvalWait`.
   - So S5 can't be evaluated before the pack is revealed, and S4 has no condition that can pass by itself.
   - The only defeat condition is Bergsons living (checked in the prefab).
3. **`startsAlert` takes effect on units revealed from a hidden group: yes, by code; not played.**
   - `HiddenLevelUnits.RevealUnit` → `Faction.Controller.RegisterUnit` raises `unitBorn` (`FactionControllerBase.cs:131`). `EnemyAlertTracker.OnUnitBorn` → `Register` reads the instance's `EnemyAlertSettings.StartsAlert`.
   - The component sits on each placed instance; the test checks it.
4. **The Black Claw's close-up plays at the next family turn start: yes, by code; not played.**
   - `EnemyIntroductionController.PlayPending` picks every alive, active enemy whose nickname hasn't been seen.
   - The Black Claw is revealed during the family turn (S4 completes on a family move), so the close-up comes at the start of the family turn after the enemy turn.
   - `deactivateUnitIntroductions` is 0 in `GlobalSettings`. A cleared save is needed, since what has been seen is saved.
5. **Fist Blitz on the 8 HP ledge Claw is predicted lethal: yes, by the numbers; not played.**
   - Factor 0.5 → 8 HP (Dark Claw base 16 at this tier, from the coordinator's HP investigation; I did not recompute the base).
   - `AbilityDamagePreview.PredictsLethalOn` uses `damage >= hp`, and Blitz deals 8, so the hit is predicted lethal and Mark hops onto 7,-2.
   - If he lands on 7,-3 instead, S1 now completes as well.

## Not verified

- Everything in Play mode:
  - no `IndexOutOfRangeException` after the rockfall reveal (the plan's 4.2a play check);
  - the five checks above;
  - the pack's AI paths and the call to arms;
  - the camera framings;
  - the HUD and input timing;
  - the S3 sequence when the last plateau Claw dies to a Watch or Counter on the enemy turn.
- Nothing was played, because no one said THJ agreed to a Play session. Verifier or THJ.
- The reaction lines after the catch (§12.2, R1/R2) are **not wired.** They need a "first Catch & Return landed" cue, which doesn't exist; it belongs to the planned trigger component. Nothing in the plan's scope can place them.

## Findings

1. **The TextMesh Pro fallback asset (`miso/Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset`) is no longer modified.**
   - It was written at 18:54:42, the same second as my first `AssetDatabase.SaveAssets()` (creating the rock clip).
   - Unity saves every dirty asset on `SaveAssets`, and the dynamic fallback font is dirty whenever glyphs were added in memory. Its content now equals HEAD.
   - I never edited it, but THJ's uncommitted change to it (most likely dynamic-atlas glyphs) is gone. It can't be recovered from git.
   - THJ should know before committing. It is probably noise; if it wasn't, he needs to redo it.
   - `GlobalSettings.asset` is untouched (last written 2026-11-23).
2. **THJ's unnamed cell already broke `TheTilesAndUnitsMatchThePaperBlock`** before 4.2 (`FormatException`). The rename fixes it, and the new test `EveryGridCellCarriesItsGridName` guards it.
3. **The seed-once rule means text changes to existing dialogue need a one-off edit.** That is what I did here (see Built). Any later text pass on the Catch, Cleared or Outro dialogues has to be done in Unity or with the same kind of one-off.
4. **On S3, the hidden pack isn't counted** (it isn't registered until revealed), so the existing "Clear the ridge" condition works as the plateau stage. I didn't switch it to `EntitiesDestroyed`.

## Placeholder lines (THJ hasn't approved §12; dialogue carries no tag, per conventions, this list stands in)

- **K1** (Catch set-up, Mark): "Linda! Shoot through them. At me!"
- **P1–P3** (pocket cleared, set A): Linda "Next time, warn me." / Mark "You'd have argued." / Linda "...I'd have won."
- **N1** (S3 complete, Mark): "The tracks, sister. Together this time."
- **N2** (S4 objective): "Reach the clue together."
- **N3a–c, N4** (ambush, at the clue): Linda "Told you there was something up here." / Mark "A man's tracks. Deep. He was carrying something." / Linda "Healing herbs, crushed fresh. And a leaf wrapper." / Linda "Mark. Listen. Behind us."
- **N5** (caption, narrator, reused from the Trail): "Black Claw. Hit it, and the pack comes for you."
- **N6–N8**: Mark "Five. Hit the big one only at my side." / Linda "Then keep up, little brother." / Mark "Breathe. Back to back."
- **N9** (potion page body): "• The family brought one Health Potion on this mission. • Select the hurt Bergson, then the Health Potion in the abilities bar. It heals them."
- **N10** (S5 objective): "Drive them off the ridge. {alive_0} remaining."
- **N11 / O1–O4** (outro, close A): Linda "Still in one piece, little brother?" / Mark "Side by side. Nothing got through." / Mark "It still smells of salve. He's tending something." / Linda "Or someone."
- Not wired: R1/R2 (see Not verified).

## Chunks

### Chunk 4.2a: rock animation fix

- Changed:
  - `Features/NPCs/Rock/Animations/` (new: controller and clip, + `.meta`, + `Animations.meta`)
  - `Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`
  - `Features/Onboarding/Editor/MissionWiring.Ridge.Layout.cs` (partial, calls the sync)
  - `Features/Onboarding/Editor/MissionWiring.Ridge.Layout.Rock.cs` (new, + `.meta`)
  - `Features/Onboarding/Editor/M1RidgeLayoutTests.cs` (rock test)
- Criteria met: the controller has a default `Idle` state with a 1 s looping clip, set on the body Animator, and THJ's scale is kept. Test `TheRockAnimatorPlaysALoopingIdleClipWithALength`.
- Decisions and loose ends:
  - One plain clip, not a direction blend tree: the rock has one sprite.
  - Named `AC_NPC_Rock` / `A_Rock_Idle` after the conventions.
  - The Play check is open.

### Chunk 4.2b: HP, ledge, ambush, potion, lines

- Changed:
  - `GB_m1-ridge.prefab`
  - `MissionWiring.Ridge.cs`, `MissionWiring.Ridge.Sequences.cs`, `MissionWiring.Ridge.Layout.cs`
  - `MissionWiring.Ridge.Layout.Ambush.cs` (new, + `.meta`)
  - `M1RidgeTests.cs`, `M1RidgeLayoutTests.cs`
  - 16 new `M1Ridge_ToClue_*` / `M1Ridge_Ambush_*` assets (+ `.meta`)
  - 5 edited M1Ridge assets: the Catch, Cleared and Outro dialogues, the Cleared step list, the Potion panels
- Criteria met (all by tests, below):
  - factors;
  - ledge tiles;
  - the `ambush` group (5 units, tiles, factors, alert, hidden);
  - S1 to S5 and their conditions;
  - the potion page in the ambush sequence only;
  - no Linda line in the catch dialogue;
  - the cell rename.
- Decisions and loose ends: see the sections below.

**Tests that cover the criteria:**
- `M1RidgeLayoutTests`: `TheTilesAndUnitsMatchThePaperBlock` (block `m1-ridge-3a` with `b`), `TheMasherIsGoneAndTenDarkClawsAndOneBlackClawRemain`, `EveryGridCellCarriesItsGridName`, `TheAmbushPackWaitsHiddenOnBothPathsAndStartsAlert`, `ClawsCarryTheirHealthFactors`, `ThePlateauClaws…` (3 groups), `TheLastStageIsDrivingThePackOffTheRidge`.
- `M1RidgeTests`: `FiveStagesTheLedgeThePocketThePlateauTheClueTogetherAndThenThePack`, `TheCatchSetUpIsMarksCallAloneWithNoReplyFromLinda`, `ThePocketClearedGivesTheReunionAndThePlateauButNoPotionPage`, `ThePlateauClearedSendsTheCameraUpToTheClueWithOneLine`, `TheAmbushRevealsThePackThenItsCaptionThenTopsUpThenThePotionPageThenGivesControlBack`, `ThePotionPagePlaysOnlyInTheAmbush`, `NoLineCarriesThePlaceholderTag` (now includes ToClue and Ambush).

**Play check needed for:** the rock error, the five checks, the AI, the cameras and the pace.

## Save reset

No. Play mode was never started.

## Decisions I made

- The Catch, Cleared and Outro dialogues and the Cleared step list were edited once, in place, instead of being given new asset names. Without that, the seed-once rule would have kept the old lines and the old potion step. The names stay the same.
- N4 shares a dialogue with N3, as the text's snippet does. N8 is kept, because N7 is kept.
- The ambush camera sequences frame tiles: the clue, the west-path tiles, the east-path tiles, then the top zone. The S3 camera goes from the plateau Claws' tiles to the clue and the top zone.
- `startsAlert` is an `EnemyAlertSettings` component added on each placed instance, not the `Unit_DarkClaw_StartsAlert` variant. This keeps both unit types on the same pattern; the Black Claw has no such variant.
- `SetClawHealth` skips ambush tiles rather than mapping them. The ambush code owns those factors.
- The S4 condition excludes allies, so the Neutral rock can't count toward it.

## Needs THJ

1. **The TextMesh Pro fallback asset** was reset to its committed content by an editor save (Findings 1). Fine to leave it? (Probably yes: dynamic glyph data.)
2. **R1/R2, the reaction after the catch**, wait for the trigger component.

## Docs to update

- `tech/onboarding-merge.md` and `status.md`: M1 now has 5 stages and the ambush. The rock has its own animator. `M1Ridge_Cleared_PotionPage` is an orphan. Owner: coordinator.
- `design/m1-ridge-redesign-text.md`: §12 lines used as recommended, and R1/R2 not placed. Owner: miso-narrative.

## Risks and loose ends

- **To delete** (orphans: nothing references them; I didn't delete anything):
  - `Resources/Sequences/M1Ridge/M1Ridge_Cleared_PotionPage.asset` + `.meta`;
  - plus the 17 old 3.1b sequences listed in `reports/onboarding-4-1b-m1-wiring.md`.
- **S3 completed on the enemy turn** (last plateau Claw killed by Watch or Counter): `M1Ridge_ToClue` runs `EnablePlayerInputSequence` during the enemy turn. That turn then has no living enemy, so it ends. This is the same pattern as S2's fallback, already noted for the trigger chunk.
- AI paths, the call radius and the 10-minute length are as designed and not played. Option B stays parked.

## Proposed commits

To be proposed after THJ's play check (plan: 4.1 build, 4.2 changes, rock fix, then the deletion of the old sequences). 4.2 touches the same files as 4.1, which is uncommitted, so the 4.1 and 4.2 wiring can only go in together. The rock fix separates cleanly:

1. `fix(onboarding): the fallen rock gets an idle animator so it no longer throws when revealed` (plain): `Features/NPCs/Rock/` (the whole folder, `Rock.meta` included, since 4.1 never committed it), `MissionWiring.Ridge.Layout.Rock.cs` + `.meta`. **Caveat:** the layout file's call to `SyncRockAnimator` and the rock test live in files that also carry 4.1 and 4.2 changes. Unless commit 2 comes first, fold this into commit 2.
2. `feat(onboarding): The Ridge ends on an ambush at the clue, with the potion page there and tougher pocket Claws` (plain): `GB_m1-ridge.prefab`, `MS2 - The Ridge.asset`, every `MissionWiring.Ridge*.cs` + `.meta`, `M1RidgeTests.cs`, `M1RidgeLayoutTests.cs` + `.meta`, `Resources/Sequences/M1Ridge/` (4.1b's 33 assets plus the 16 new `ToClue`/`Ambush` assets, each with its `.meta`), the bark graph and CSV + `.meta`.
3. `chore(onboarding): remove The Ridge's unused sequences` (plain): the 17 old 3.1b sequences and `M1Ridge_Cleared_PotionPage`, each with its `.meta`.

Not to stage: `GlobalSettings.asset`, the TextMesh Pro fallback, `LevelM2-C1.prefab`, `miso.slnx`, `.mcp.json`, `claude-handoff/`.

## Other branches

None.

## How to see it

Before you start: set `GlobalSettings` › `deactivateIntroOutroSequences` **off**, and clear the save (this also clears the played barks and the "seen" enemy close-ups). Start `MS2 - The Ridge` the way you usually test a mission.

1. **Rockfall:** the rock appears on 5,-5 (your size), with no `IndexOutOfRangeException` in the console then or later.
2. **Family turn 1:** Mark Moves, then Blitzes the 7,-2 Claw. It dies in one hit (8 HP), and he lands on 7,-2. If he ever ends on 7,-3, the ledge stage still completes.
3. **Catch set-up:** a single Mark line, "Linda! Shoot through them. At me!", with no reply from Linda. Her bar returns.
4. **Two catches:** Linda shoots east along row -2. The catch is offered and hits the pocket Claws (12 HP each). With her second AP, shoot again: the catch is **offered a second time**.
5. **Pocket cleared:** "Next time, warn me." / "You'd have argued." / "...I'd have won.", then "Breathe, sister…", FP full, the plateau and its lines, and **no potion page**.
6. **Plateau:** clear the three Claws. The camera goes up to the clue and Mark says "The tracks, sister. Together this time." The objective reads "Reach the clue together."
7. **Empty enemy turn:** end the turn before going up. The enemy turn shows at most its banner and passes, and the level doesn't end.
8. **The clue:** move only one sibling into the 8 tiles in front of the clue; nothing happens. Move the second one in, and the ambush plays:
   - the clue lines and "Mark. Listen. Behind us.";
   - the camera down the west path, where the Black Claw (1,-1) and a Claw (2,-1) appear;
   - the caption "Black Claw. Hit it, and the pack comes for you.";
   - the camera on the east path (three Claws);
   - Mark's and Linda's lines;
   - FP back to full;
   - the "Health Potion" page ("brought one");
   - the camera back on the family, control returned.
9. **Enemy turn:** the pack climbs straight away (alert, no Unaware skip). No hit lands on the family on this first turn. Watch may trigger on the climbers.
10. **Next family turn:** the Black Claw close-up plays first.
11. **Win:** kill all five. The objective counts down "Drive them off the ridge. N remaining.". Then the camera on the clue, "Still in one piece, little brother?" / "Side by side. Nothing got through." / "It still smells of salve…" / "Or someone.", and the outro.
12. **Timing:** note the total length (the design expects about 10 minutes; option B is parked if it runs long).
13. **A sibling falls → loss** (fix round): in any fight, let Linda or Mark drop to 0 HP. The level ends at once in a defeat, the usual defeat panel and its Retry/Home choice, with no waiting on "Reach the clue together".
14. **Ambush on the enemy turn** (fix round, *not fixed yet*, waits on the decision in "Fix round" item 2): with both siblings already standing in the 8 tiles, kill the last plateau Claw with a Watch on the enemy turn. Today the ambush plays at once, on the enemy turn. Once item 2 is decided and built, it should wait for the family turn.

## Review (miso-reviewer, 4.2a + 4.2b, 2026-11-24), pasted by the coordinator

**Verdict: ESCALATE.** No must-fix defect in the 4.2 code; one softlock missing from plan and design needs a design call.

- **Must fix (decision first):** S4 "Reach the clue together" can never complete if a sibling is down. One sibling down doesn't lose (defeat = Bergsons living ≤ 0, `LevelBase.prefab:779-787`), no mid-level revive, `TilesOccupiedLOCondition` counts living units only (`LevelObjectiveConditions.cs:170-173`), S4 has no turn fallback, no enemy alive: family turns loop forever. Likely on the plateau, where low HP first happens and the potion is no longer taught. Fix options go to THJ.
- **Should fix (play-check item):** if the last plateau Claw dies on the enemy turn (Watch/Counter) with both siblings already in the zone (plateau Claws stand on top-zone tiles 1,4 and 3,4), S3 and S4 complete on the enemy turn; the pack is registered with full AP and acts that same turn (`AIController.cs:77`), and the family's leftover AP is lost. Often S4 completes as soon as it's shown; the empty enemy round may never happen.
- **Notes:** no core code; no new mutable statics; no private IDs; line endings kept; rock controller safe for the `EntityAnimationHandler` throw paths (not seen in Play); THJ's rock scale and 48 cells kept; ambush units, factors, alert flags and sequence order match design; `SetClawHealth` skips ambush tiles by position (a hand-moved ambush unit would get a duplicate; low risk); tests cover the behaviour; AI regression 45; commit split acceptable (rock fix stands alone only after commit 2); TMP fallback reset for THJ to confirm.

## Fix round (miso-implementer, 2026-11-24)

The editor was not in Play mode. No core code, no new statics, no git writes, and none of THJ's files touched.

### 1. One sibling down loses M1 (must-fix, done)

- `MissionWiring.Ridge.cs`:
  - new constant `DefeatAtFamilyStanding = 1`;
  - new `WireDefeat`, called from `WireLevel`. It finds the level's single defeat condition (the template's Bergsons `LivingUnitsLOCondition`) and sets it to `Exist`, `LessThanOrEqual`, count 1. It throws if there isn't exactly one.
  - The template prefab isn't touched.
- Result in `GB_m1-ridge.prefab`: a single new override, `managedReferences[8046274707106824281].count = 1`, on the inherited condition. A second wiring run left the level byte-identical.
- **Loss path:** unchanged. `CombatLevelRunHandler.UpdateObjectives` → `LevelObjectives.Evaluate` returns Defeat → `ForceEndTurnSafe` → `EndLevel(Defeat)`, then the defeat panel and `EndMission(false)` or `RestartLevel`. Only the threshold moved.
- **Defeat while a stage advances:** `TryEvaluateWin` checks defeat before it advances a stage, so a sibling falling on the same hit that clears a stage still loses.
- **Revive on win:** unaffected.
  - `EndLevel` resurrects the dead player units only when the result is Win.
  - With one down the level now loses first, except in one case: the last enemy and a sibling fall in the same evaluation. There, the final-stage win is checked before defeat, so it is still a win and the fallen sibling is revived as before.
- **Test:** `M1RidgeTests.TheLevelIsLostOnceOneSiblingIsDown`.
  - the level has exactly one defeat condition, the Bergsons living-units check, `Exist`;
  - `MathUtils.Compare` with that condition: 1 and 0 standing lose, 2 standing plays on;
  - the mission's family is the two fixed siblings.

### 2. The ambush only on a family turn (should-fix): stopped, options below

**No built condition does it.** The objective conditions are `LivingUnits`, `UnitDeath`, `EntitiesDestroyed`, `EntitiesCaptured`, `TilesOccupied`, `UnitTileOccupied`, `FalseObjective` and `TurnReached`; none reads whose turn it is. No combination of them can tell the family turn from the enemy turn:
- `TurnReached` counts rounds, and with the enemies first a round starts on the enemy turn.
- No built sequence step waits for a faction's turn.
- `LevelSpecificBehaviour`'s `CurrentPhase` action can reset or end the current phase, but not "only if it's the enemy's". Ending the phase in the ambush sequence would end the family's own turn in the usual case.

So nothing is changed for item 2. **Options:**

| | What | Code | Notes |
|---|---|---|---|
| **A (recommended)** | A small new objective condition outside core, e.g. `Features/Onboarding/FactionTurnLOCondition` ("it is [faction]'s turn": `CombatLevelRunHandler.Instance.CurrentFaction == Faction`). S4's one objective holds two conditions, `TilesOccupied AtLeast 2` and "Bergsons' turn", aggregation All | ~15 lines of new game code in `Features/`, plus wiring and a test. It subclasses core's `LevelObjectiveConditionBase` and changes nothing in core; no static | Objectives are re-evaluated right after every `StartTurn` (`SwitchTurnIE`), so a stage that is true on the enemy turn completes at the next family turn start: fresh AP, and the pack doesn't act first. It's needed because otherwise the stage completes the moment both siblings stand in the zone |
| B | A non-core component in the level that delays S3's completion: the S3 condition stays false until a family turn (the same new condition as A, on S3 instead of S4) | Same as A | A puts the gate where the reveal happens. B would also hold back the N1 line and camera |
| C | Change core so queued stages only advance on the player's turn (`LevelObjectives`/`CombatLevelRunHandler`) | Core | Tier 3; affects every level with queued stages. Not recommended |
| D | Accept it for the play check | None | The family loses its leftover AP, and the pack gets a free climb on that enemy turn. The spawn distances still give the family one turn before any hit lands (design §4), but the close-up then plays after the pack's first move |

### Files (fix round)

- `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Ridge.cs` (defeat wiring)
- `miso/Assets/_Project/Features/Onboarding/Editor/M1RidgeTests.cs` (one test)
- `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-ridge.prefab` (one override)

LF, no BOM, as before.

### Tests

- `M1RidgeTests` + `M1RidgeLayoutTests` + `SearchRidgeTests`: **53/53 passed**.
- Full EditMode suite: **2677 total, 2676 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Not re-run by name: no AI graph, AI ability or unit prefab changed in this round. The last run, this session, gave 45.
- `GlobalSettings.asset` and the TextMesh Pro fallback asset were untouched in this round.

"How to see it" has two new steps: 13 for the loss, and 14 for the ambush on the enemy turn, which stays open until item 2 is decided.
