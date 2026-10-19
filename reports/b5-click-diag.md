# Report: B5 click diagnostic

Plan: plans/2026-10-18-playtest-batch1-bugfixes.md (chunk C6, B5)    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done

## What changed

- miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs: extended LogB5Diag with collider/layer/position/sorting info; added a click-only Update() diagnostic. Everything new is TEMPORARY and tagged [B5-DIAG].

git diff --stat: `HomeInteractables.cs | 83 +++++` (1 file, 83 insertions, 0 deletions)

## Acceptance criteria

- [x] Compiles clean: Assembly-CSharp.dll rebuilt at 10:22 after the edit; console has no CS errors (only the old warnings). One "Internal error - unexpected guid mismatch" entry is in the console; it is not a compiler error and not from this file (not investigated).
- [x] Lock behaviour unchanged: RefreshLock, OnPointer* untouched; the additions only log.
- [x] All new lines tagged [B5-DIAG].
- [x] Line endings kept: LF, no BOM (checked 0 CR before and after).
- [ ] Runtime output not verified: Play mode was not entered, as instructed.

## Save reset

no

## Decisions I made

- Input API: new Input System (`UnityEngine.InputSystem.Mouse.current.leftButton.wasPressedThisFrame`), same as PlayerInputController and HomeHandler.
- World point uses `ScreenToWorldPoint` with z = |camera z| (2D ortho camera assumption).
- Update() logs per object only if the click is inside this object's colliders, or this object's name contains "Equipments Cabinet" (always). So a click on the cabinet logs once from the cabinet, regardless of overlap. A click on another Home object logs once from that object, with the same global data (EventSystem, raycasters, hits).
- `FindObjectsByType<EventSystem>` runs only on click. No new statics.
- Physics2DRaycaster is looked up on Camera.main's own GameObject only.

## Needs THJ

none

## Docs to update

- none (remove all [B5-DIAG] lines when B5 is fixed; the Update() method and the added block in LogB5Diag go entirely).

## Risks and loose ends

- The Update() runs every frame on every HomeInteractables but returns at once unless the mouse was clicked.
- If the cabinet's component is disabled or its object is inactive, Update will not run, so no click lines appear for it. The Awake/OnEnable line shows activeInHierarchy and the collider state to cover that case.
- If another HomeInteractables does log on the click, its Physics2D/EventSystem lines still show what catches the click.

## Proposed commits

1. chore(home): temporary B5 click diagnostics in HomeInteractables: HomeInteractables.cs (plain, temporary, revert when B5 is fixed)

## Other branches

none

## How to see it

1. Open the Home scene, enter Play, win "M3 - Mark Intro", return Home (reproduce B5).
2. In the Console filter on `B5-DIAG`. Click the Workshop ("Equipments Cabinet") once.
3. Look for the "Click" line and send it with the preceding OnEnable line.

Example lines (format; values illustrative):

```
[B5-DIAG] OnEnable obj=Equipments Cabinet isLocked=False oneEnough=False missions=[M3 - Mark Intro=True] actionMode=Normal homeManager=exists (...) layer=Interactable activeInHierarchy=True pos=(3.200, 1.100, 0.000) colliders=[BoxCollider2D enabled=True isTrigger=False] sortingLayer=Default sortingOrder=2

[B5-DIAG] Click obj=Equipments Cabinet screen=(812.0, 400.0) world=(3.1, 1.0) insideCollider=True colliderEnabled=True isLocked=False
  Physics2D.OverlapPointAll=[Equipments Cabinet layer=Interactable z=0.000, Wall layer=Default z=0.500]
  EventSystem.current=EventSystem count=1 Camera.main=Main Camera Physics2DRaycaster=enabled=True eventMask=-1
  EventSystem.RaycastAll=[HUD Panel module=GraphicRaycaster sortingLayer=0 sortingOrder=0 depth=3 distance=0.000, Equipments Cabinet module=Physics2DRaycaster sortingLayer=0 sortingOrder=2 depth=0 distance=10.000]
```

The first entry of RaycastAll is what receives the click.
