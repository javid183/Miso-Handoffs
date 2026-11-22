# Duo / Family Role insert shot: comic sequence (proposal)

Owner: coordinator. Status: **proposed 2026-11-22, waiting on THJ** (layout, QTE order, length, first test scope).

## Ask (THJ, 2026-11-22)

Replace the sliding avatar panels of duos and Family Roles with a short, comic-like animated insert (anime-style test clips of Mark), closer to Prince of Persia: The Lost Crown's Athra Surge splashes and Marvel's Midnight Suns' combo cinematics. Possibly a full-screen split into two halves. Move the QTE out of the middle of the insert: before or after it, in its own frame.

## How it works today (read in code 2026-11-22)

- **Family Role:** `PlayerController` (around line 1690) focuses the camera, calls `CombatLevelUIManager.ShowFactionRolePromptVisual` (only stores the units), then starts the QTE at the role unit's `UIHook`. `QTEButton` converts that world point to screen every frame, so the prompt sits on the board, mid-screen. On a press: spotlight, then `ShowFactionRoleExecutionVisual` → `FactionRoleVisual.ShowSoloPanel` (animator trigger `PlayFRSolo`), 0.8 s, then the role runs.
- **Duo:** `UnitsCooperationHandler.ExecuteIE` calls `ShowDuoVisual` first (triggers `PlayFRDuo` on both partners' animators in `FTPPanel`), focuses the camera, then activates each partner. A partner with a QTE sets `Time.timeScale = 0` and opens its QTE at its own `UIHook` while the duo panels are still on screen: that is the busy screenshot. Mark-Lucy routes Mark through `ActivateMarkLucyBlitz`.
- **Trio / Family Super Time:** `ActivateFactionSuperTime` shows the Bergsons splash, then `ShowTrioVisual`.
- `HideFactionRoleVisual` is empty (its body is commented out); the panels leave by their own clips. `FactionRoleVisual` picks panels by nickname with hard-coded per-character fields; Mark has special left/right logic.
- Art: `Content/FamilySuperTime/Sprites` (per-character PNG + BG, `AC_<Name>FamilyRole` controllers, Left/Middle/Right clips, `Anim_FR_Letterbox`).
- **StuntCamActorSet** (`Content/FamilySuperTime/DUO/`): an ortho camera (size 1, depth -1, culling mask Everything) renders to `StuntRenderTexture`; a `RawImage` in `CombatLevelContainerScene` shows that texture. The scene instance is **inactive** (`m_IsActive: 0`) and no code turns it on, so nothing is rendered: that is why it never shows. With culling Everything it would also pick up whatever else is near it; it needs its own layer. `PS_SpeedLines` and `speedline.mat` sit next to it and are reusable.

## The test clips (2026-11-22)

Two clips, 640×360, 8.04 s each.
- A (`…52d3cda8`): Mark bust, shaved head, near static (breathing, embers).
- B (`…1f312a26`): Mark waist-up, topknot, red smoke; **Children of Morta and Prince of Persia logos burned into the top corners**: test only, crop them out, never ship.
- The two Marks don't match (hair). Both barely move: on their own they read as an idle, not a hit. 8 s is far too long; a cut of 1 to 1.5 s is the usable part.
- 16:9 frames need a crop to fill a diagonal half. No Lucy clip yet.

## Proposal

Three beats, game paused throughout:
1. **Call (0.2 s):** board dims, freeze.
2. **QTE card (when the move has one):** screen-space and framed (a comic panel with the partner's face, prompt and fill), anchored to a fixed spot, not to the unit. The board behind stays dimmed.
3. **Insert (1 to 1.5 s, skippable, a setting to shorten or turn off):** full screen split on a diagonal, one half per partner, each a clip in a masked panel with an ink border; impact-frame flash on the cut, speed lines, the move name as a caption. The last frame holds a beat, then the panels tear away and the action plays on the board.

Recommended order: **QTE first, insert as the payoff.** The press is the decision; the insert rewards it. A missed Family Role press then plays no insert (no wasted time), and a duo mash result can pick a stronger or weaker insert. Alternative: insert first, freezing on its last frame, which shrinks into the QTE card.

Tech for the test: `VideoPlayer` → RenderTexture → masked `RawImage` per half, driven by a new `DuoInsertSequence` component on its own canvas; `FactionRoleVisual` stays for any pair without clips. Clips by pair in a ScriptableObject. StuntCam stays a later option for in-engine stunts (needs its own layer and activation).

Flags: moving the duo QTE ahead of the actions changes `UnitsCooperationHandler` timing (`timeScale`, per-partner QTE) and the Family Role QTE placement touches `QTEButton` / `PlayerController`: check `tech/core-systems.md` and get THJ's OK. Repeated inserts fatigue (a known complaint about Midnight Suns' combo animations): first use full, later uses short, plus a setting.
