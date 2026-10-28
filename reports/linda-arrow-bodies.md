# Report: Linda arrow bodies (D-296)

**Outcome:** done by YAML edit, not compiled or run (editor open, no batch). Test not yet run: THJ please run it.

**Files changed** (all under miso/Assets/_Project/Features/Player/Linda/)
- Prefabs/LindaAttackArrow, LindaAttackFireArrow, LindaAttackHealArrow, LindaExplosiveArrow, LindaAttackArrowReturn (.prefab): +28 lines each. Rigidbody2D (fileID 7340000000000000001) on the root with the Projectile and collider, listed in m_Component. Field set copied from UnitBase. Kinematic, gravity 0, simulated, interpolation none, Discrete, sleeping mode Never Sleep (0), constraints none, full kinematic contacts off. LF kept, no .meta changes.
- Scripts/Quiver/Editor/QuiverWiringTests.cs: new `ArrowPrefab_HasAnAwakeKinematicBody` (5 cases: Kinematic, gravity 0, NeverSleep, simulated).

**Docs answers (from memory, not checked online)**
- Kinematic-vs-Dynamic trigger contacts work by default: a trigger collider on a kinematic body does get enter/stay/exit against dynamic bodies. useFullKinematicContacts only matters for non-trigger kinematic-vs-static/kinematic collisions, so off is right.
- Continuous: only matters for non-trigger dynamic bodies tunnelling. For a kinematic trigger it doesn't help. A transform-moved trigger is not swept either way; Discrete stays.

**Code check**
- No code reads or adds a Rigidbody2D on the arrows. Projectile.cs, QuiverArrow.cs and SpawnableEntity have none. CatchSweep only reads `collider.attachedRigidbody` on the colliders it hits (Mark's), not the arrow's own; its CircleCast and Projectile's OverlapCircle queries are not affected by sleep.
- Triggers go to the collider's object, then its body's: same object here, so OnTriggerEnter2D routing is unchanged.
- Projectile moves by `transform.position`. On a kinematic body that works (Unity syncs the transform to the body before physics). `Rigidbody2D.MovePosition` would be the proper call: it moves the body with a velocity so contacts and swept overlap are cleaner. It is a core Projectile change, so not made.
- GetClone uses Instantiate(prefab), which keeps the body. Mark's freeze (Projectile.enabled = false and a transform move) stays fine; the body just sits at the transform.

**Test for THJ:** Test Runner > EditMode > QuiverWiringTests.ArrowPrefab_HasAnAwakeKinematicBody (5 cases). Whole suite as usual (the known red AIRegressionTest stays).

**Play steps:** Mark out of line, Lucy out of the party. Shoot Dark Worms that haven't moved for a while (more than 0.5 s). Shoot a column of two worms. All should be hit. Check the combat log's damage lines. Try the fire, heal, explosive and return arrows too.

**Main:** needs the same change for its 4 arrows (the return arrow doesn't exist there).

**Proposed commit:** `fix(linda): arrows get an awake kinematic body so sleeping enemies are always hit`. Files: the 5 prefabs and QuiverWiringTests.cs.
