# Report: B5 diagnostic removal

Plan: none (size S, D-074)    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (compile not verified)

## What changed

- miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs: removed LogB5Diag (and its 4 calls), the click-only Update() diagnostic, and the [B5-DIAG] early-return log (early return restored to the plain `if (_isLocked) return;`). Kept RefreshLock() and its calls. This also dropped the uncommitted working-tree extension of the diagnostics.

## Acceptance criteria

- [x] `grep B5` finds nothing: 0 matches.
- [ ] Compiles: not verified (Unity console not checked; I did not enter Play mode). All usings are still needed (List, Linq .Any/.All, EventSystems for IPointer*), so none were removed; the System.Text and InputSystem uses were fully qualified inline and went with the code.
- [x] Behaviour unchanged apart from logs: RefreshLock and OnPointer* bodies are as in 47cee8ad9 minus log lines.
- [x] `git diff 47cee8ad9~1` shows only the RefreshLock hardening (below).
- [x] LF, no BOM, no trailing-newline change (file still ends `}` with no newline, as before).

## Save reset

no

## Decisions I made

- No using directives removed: none were diagnostic-only.

## Needs THJ

none

## Docs to update

- build-log.md / status.md: B5 diagnostics removed (coordinator).

## Risks and loose ends

- Working tree had more diagnostic code than commit 47cee8ad9 (uncommitted extension); all gone now, so the diff vs HEAD will show a net removal of more than 47cee8ad9 added.
- Scene `Home - Scene.unity` untouched.

## Proposed commits

1. chore: remove temporary B5 diagnostics from HomeInteractables (B5, D-074): HomeInteractables.cs (plain)

## Other branches

thj/oct-build-fixes also contains 47cee8ad9, so it still has the diagnostics; the same removal applies there.

## How to see it

1. Open Unity, let it recompile, confirm no console errors.
2. Enter Play on Home; hovering and clicking Workshop Cabinet logs no [B5-DIAG] lines and still works.

## Diff vs 47cee8ad9~1 (RefreshLock hardening only)

```diff
diff --git a/miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs b/miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs
index 3a49113f5..ce815fa72 100644
--- a/miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs	
+++ b/miso/Assets/_Project/Features/Home - Imported/___Khashayar/HomeInteractables.cs	
@@ -39,14 +39,28 @@ namespace MISO.Core.UI.Runtime.Home
 
         private void Awake()
         {
-            _isLocked = (UnlockAfterMissions != null && UnlockAfterMissions.Length > 0) &&
+            RefreshLock();
+        }
+
+        private void OnEnable()
+        {
+            RefreshLock();
+        }
+
+        // Re-evaluates the lock from the missions' current Completed state.
+        private void RefreshLock()
+        {
+            bool locked = (UnlockAfterMissions != null && UnlockAfterMissions.Length > 0) &&
                 (!oneUnlockedMissionCompletionIsEnough && UnlockAfterMissions.Any(u => u.Completed == false) || UnlockAfterMissions.All(u => u.Completed == false));
-            
-            homeInteractableUI.SetActive(!_isLocked);
+
+            _isLocked = locked;
+            if (homeInteractableUI != null && homeInteractableUI.activeSelf == locked)
+                homeInteractableUI.SetActive(!locked);
         }
 
         public void OnPointerEnter(PointerEventData eventData)
         {
+            RefreshLock();
             if (_isLocked)
                 return;
             foreach (var obj in objectsToActivateOnPointerEnter)
@@ -59,6 +73,7 @@ namespace MISO.Core.UI.Runtime.Home
 
         public void OnPointerExit(PointerEventData eventData)
         {
+            RefreshLock();
             if (_isLocked)
                 return;
             foreach (var obj in objectsToActivateOnPointerEnter)
@@ -71,6 +86,7 @@ namespace MISO.Core.UI.Runtime.Home
 
         public void OnPointerDown(PointerEventData eventData)
         {
+            RefreshLock();
             if (_isLocked)
                 return;
             PointerDown?.Invoke();
```
