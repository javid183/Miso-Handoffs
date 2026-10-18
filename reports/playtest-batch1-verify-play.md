# Report: Playtest Batch 1, play check (B1, B3, B6, B8)

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md    Agent: Claude (main session, computer use; no subagent)    Branch: thj/oct-build-fixes (not switched)
Outcome: partial (core behaviour seen in play for B1, B3, B6 and B8; the parts that need a corrupted tile, a branching mission, a fractional HP or a mid-turn tutorial were not reachable)

Checklist: `playtests/2026-10-18-batch1-play-check.md`. B5 repro skipped as asked (THJ does it). Editor 6000.3.4f1, run from `Scenes/PreloadScreen.unity`. Evidence is from screenshots of the Game view and the Console panel; I did not read `Editor.log`.

## What changed

- `claude-handoff/reports/playtest-batch1-verify-play.md`: this report. Nothing else on disk: no code, prefab, scene or git changes (git status on `ProjectSettings` shows two modified files dated Oct 9, before this run, not mine).
- Editor state outside the project: the game save file was deleted (see Save reset); a custom "4:3 Aspect" entry was added to the Game view size list (editor preference, not a project file); the toolbar level picker was moved and put back to LevelE2-C1.

## Acceptance criteria

### B1 · Mark's Cleanse (C1, C2)

How I got there: toolbar level picker → `LevelE3-C1` (the level named *In My Father's Arms* in the HUD) → Load → "Assign Placeholders" dialog: slot 1 Mark, slot 2 John, slot 3 Toba → Load Scene. Played from the level start sequence to the first player turn.

- [x] **Pass: Mark's Cleanse casts and the turn goes on.** Turn 1: selected Mark, slot 4 tooltip "Cleanse: Cleanses corruption around the unit", cast on Mark's own tile. After about 3 s the ability slot is greyed with cooldown "1", one of Mark's two AP was spent, and I could select another ability (slot 2 preview showed) and cancel it. Turn 2: cast again (the cooldown had expired), same result, second AP spent. No freeze either time.
- [x] **Pass: no `ability animation state is missing` error.** Console after both casts: 2 info, 6 warnings, 0 errors (badge counts). The only entries were `DOTWEEN Max Tweens reached...` and `MasherGoblinFactionRoleHandler on Unit_MasherGoblin did not initialize its role ability...`, neither about animation states. I did not look at the animation itself closely enough to say whether John's sprites showed on Mark.
- [ ] **Not run: the corrupted tile clears.** No corrupted tile or corruption pool appeared on the board in two player turns and two enemy turns (the purple creatures are enemies, not tiles). The Cleanse effect lowers `Specs_CorruptionHealth` on cells within radius 1, so it needs a pool next to the caster. Needs a level or moment with a pool on the board.
- [ ] **Not run: safety net (missing state name).** Optional, and it needs a prefab edit in Prefab Mode. I did not do it, to keep zero risk to the prefab; so the new error line (ability, unit, state) and the "ability still resolves" behaviour are not seen in play. The EditMode test for the decision is covered in the quiet checks, not here.
- [x] **Pass (by eye only): John's Cleanse resolves.** John selected, slot 6 tooltip "Cleanse", cast on his tile: resolved within a few seconds, slot greyed with cooldown 1, AP spent, no console error. "Same frame timing as before" was not measured; there is no old build to compare against here.

### B3 · HP never reads 0 while alive (C3)

- [x] **Pass for whole-number HP; the real bug case was not reproduced.** Cheat `[` (−1) and Shift+`[` (−10) took the hovered units down:
  - Mark, unit panel (bottom left): 8/15 → 2/15 → **1/15**, still alive and selected, bar a thin sliver.
  - Enemy archer, hover panel above it: 2/24, then **1/24** while alive, bar almost empty. It died on the next hit (the unit vanished; no 0 readout to read).
  - The fix is about a fractional HP below 0.5 rounding to 0. The cheats only remove whole points, so I could not make a unit sit at, say, 0.3 HP. A test that would: a hit from a modified-damage ability on a nearly dead unit, or an EditMode test of `UI_Element_FillBar`.
- [ ] **Not run: mission character icons.** Not checked: no icon showed HP in the levels I played. (Top-left shows the level name and FP only.)
- [ ] **Not run: damage preview still shows expected future HP.** I did not select an attack with an enemy in range and read the preview.

### B6 · Map mission panel (C4)

World map: Home → "Start Game" station → world map → clicked mission marker 5 ("The Healer"). Game view maximized, aspect set from the dropdown.

- [x] **Pass: 16:9.** Panel right edge at about x 1330 of a 1388 px wide view, top at y 115, "Continue" button bottom at y 745 of 778: whole panel and the Continue button on screen.
- [x] **Pass: 16:10.** Panel right edge at 1265 of 1322, Continue bottom at 770 of 778: fully on screen.
- [x] **Pass, with a note: 4:3.** Panel right edge at 1135 of 1222, Continue bottom at 770 of 778: fully on screen. It covers the right side of the map, so mission marker 4 and the compass are hidden while a mission is selected (the selected marker, markers 1, 2, 3, 6 and the X button stay visible). I read that as acceptable ("doesn't hide map content you need"), but flagging it in case you want the panel narrower at 4:3.
- [ ] **Not run: mission map (MissionMap prefab).** `CombatLevelUIManager.ShowMissionMapThenLoad` shows it only when the mission's level graph is not linear (`MissionTracker.ShouldShowMissionMap`). *The Healer* (2 levels) and Mission 1 *John's Map* (3 levels) both went straight to the next level after Victory. A non-linear mission (by node count M4, M6, M11, M14 are candidates) is not reachable on a fresh save. Not checked at any aspect.
- [ ] **Not run: 21:9** (known overshoot, out of scope).

### B8 · Tutorial input lock (C5)

Played from a cleared save so the tutorials fired: Level 1 (`Level1-C1`, "John's Map 1/3") and `Level1-C1-2` (2/3).

- [x] **Pass: while a tutorial panel is open nothing acts.**
  - Level 1 start, "Basic Controls" then "Abilities" pages: left click on a unit and on a tile, right click, `D` held 1.5 s, Tab and Left Shift. The panel stayed open, no unit was selected or deselected, the camera did not move (screenshot before and after identical apart from the panel).
  - Level 1-C1-2 start, "Abilities" page: left click, right click, Tab, `D` held 1.5 s, `W` held 1 s, Shift and **Escape (Pause)**. No pause menu appeared, the panel stayed, the camera did not move.
  - Not tried: the Switch / Toggle buttons by their own bindings beyond Tab and Shift (I do not know which keys they are mapped to).
- [x] **Pass: closing the tutorial restores play.** After closing in Level 1: John was selected with his move range, first click picked the Run preview and a second click moved him (AP 2 → 1), right click cancelled a preview. After closing in Level 1-C1-2 (and the enemy introduction): Linda moved with two clicks, selected ability 1 and clicked a target, and Escape opened the pause menu normally (so the Escape sent during the tutorial was not queued). Continue closed the menu and End Turn worked.
- [ ] **Not run: tutorial at a turn change, or one that opens mid player turn.** In Level 1 both tutorials open at level start (they sit in the start sequences `Level1C1_Start` and `Level1C1-2_Start`); the mid sequence has no tutorial. I found no tutorial that fires at a turn change. Those two cases need a different level.
- [x] **Pass: enemy introduction plus tutorial in the same level.** In Level 1-C1-2: tutorial opened, closed, then the "Dark Claw" enemy introduction played, then the first player turn started with Linda selected and input working (move done). Note this is the order tutorial first, introduction second.

## Save reset

yes. I deleted the game save (`...\AppData\LocalLow\Dead Mage\miso\SaveData.json`) with Tools > Save Data > Clear Save Data, because the tutorials are play-once and the existing save had already played them ("Sequence Skipped (PlayJustOnce, already played)" was in the Console). Progress that was in it (Healer mission, Home state) is gone. Resetting was allowed by THJ; there is no backup. After the reset I played a fresh game: intro text, Play, Level 1 tutorial, Level 1-C1-2.

## Decisions I made

- Loaded *In My Father's Arms* through the toolbar level picker (LevelE3-C1) instead of the Home route; it is faster and gave me Mark, John and Toba.
- Used the K cheat to win the fights I needed to pass (The Healer level 1, Level 1-C1). F11 and F12 did not react to my key presses, so I do not know if the cheats work; K did.
- Did not do the optional safety-net test.

## Needs THJ

none

## Docs to update

- `playtests/2026-10-playtest-tasks.md` / `build-log.md`: coordinator, to mark B1 (cast, no freeze) and B8 (lock, restore) as seen in play; B3 seen at whole-number HP only; B6 world map seen at three ratios; the open items below.
- `tech/editor-checks.md`: on this layout the toolbar level picker (`Tools` row: dropdown plus the ▶ button right of it) loads a level straight from PreloadScreen and shows an "Assign Placeholders" dialog; `Tools > Save Data > Clear Save Data` is how to replay the tutorials; the Game view is easiest to read when maximized (double-click the Game tab) and with tiny numbers zoomed at scale 1; the hover panel does not refresh after cheat damage until the cursor leaves and re-enters.

## Risks and loose ends

- Still to see in play: a corrupted tile clearing (B1), the missing-state error line (B1 safety net, optional), a fractional HP just above 0 (B3), the damage preview (B3), the mission map at 16:9, 16:10 and 4:3 (B6), a tutorial at turn change or mid turn (B8).
- Console at Play exit shows `There are no audio listeners in the scene` (several lines), `DOTWEEN SAFE MODE captured 2 errors` and, once, `DOTWEEN Tween startup failed (NULL target/property): The object of type 'UnityEngine.CanvasGroup' has been destroyed` right after opening the world map from Home. They look like teardown or UI-tween noise and I did not trace them or check whether they pre-date these commits.
- Cheat hover panel (`[`, Shift+`[`): after cheat damage the enemy hover panel kept the old value until I moved the cursor away and back. Probably cheat-only, but worth knowing when you read HP in a check.
- The 4:3 custom Game view size stays in the dropdown (editor preference). Remove it from the dropdown if you do not want it.
- The `[B5-DIAG]` lines from C6 print on entering the Home scene (Awake/OnEnable of each interactable) as designed; I did not do the B5 repro.

## Proposed commits

none (no project files changed)

## Other branches

none

## How to see it

1. B1: toolbar picker → LevelE3-C1 → ▶ → Assign Placeholders (Mark, John, Toba) → advance the intro with Space → select Mark → slot 4 → click Mark's tile. Watch the Console for 0 errors.
2. B8: Tools > Save Data > Clear Save Data, Play from PreloadScreen, Start Game → Play; while "Basic Controls" is open try clicks, Tab, WASD and Escape.
3. B6: Home → Start Game station → click a marker; switch the Game view between 16:9, 16:10 and 4:3.
